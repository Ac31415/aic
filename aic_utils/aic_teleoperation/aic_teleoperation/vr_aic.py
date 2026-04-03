#!/usr/bin/env python3
"""
Oculus Quest VR Teleoperation — AIC UR5e Impedance Controller
=============================================================

Streams Cartesian pose targets from an Oculus Quest right controller to the
AIC UR5e impedance controller via aic_control_interfaces/msg/MotionUpdate.
Pose targets are expressed in base_link and include per-command stiffness and
damping matrices, allowing compliant behaviour to be modulated in real time.

Architecture overview
---------------------
  oculus_reader (viz_transforms.py)
      ├─ TF: world → oculus_r          (6-DOF wrist pose at ~20 Hz)
      └─ /oculus/right/joy             (axes + buttons at ~20 Hz)

  This node (30 Hz timer)
      ├─ Reads wrist TF delta from capture reference → maps to robot TCP delta
      ├─ Adds analogue stick fine-control offsets (when enabled)
      ├─ Applies safety limits (sphere radius, per-axis workspace, step cap)
      ├─ Applies first-order low-pass filter on position target
      └─ Publishes MotionUpdate → /aic_controller/pose_commands

Control modes
-------------
  VR tracking (keyboard e/q):
      Full 6-DOF wrist mirroring.  Press 'e' to capture the reference pose;
      subsequent hand motion drives the TCP relative to that snapshot.

  Analogue stick (controller A button):
      Fine-grained incremental control, independent of VR tracking.
      Operates on a fixed reference pose captured at enable time, so offsets
      never compound between ticks.  Modes (right thumbstick):
        default         — yaw (X-axis) + Z translation (Y-axis)
        grip held       — XY translation
        trigger held    — pitch (X-axis) + roll (Y-axis)
      Frame (controller B button): base_link or TCP-relative.

  Both modes can be active simultaneously; stick offsets are applied on top
  of the wrist-tracking target each tick.

Impedance parameters
--------------------
  Commands carry 6x6 stiffness and damping matrices (flat float64[36]).
  TELEOP values (stiffness=60, damping=50) are used during normal operation.
  When force feedback is enabled ('f'), stiffness reduces linearly from 60 to
  15 as contact force rises from 2 N to 20 N, increasing compliance during
  insertion tasks.

Requirements
------------
  - ROS 2 Kilted Kaiju
  - aic_control_interfaces  (MotionUpdate, ControllerState, ChangeTargetMode)
  - oculus_reader (rail-berkeley)  — viz_transforms.py publishing TF + Joy
  - std_srvs
"""

import atexit
import math
import shutil
import sys
import threading
import termios
import tty
import select

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.qos import QoSProfile, ReliabilityPolicy

from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState, Joy
from tf2_ros import Buffer, TransformListener

from aic_control_interfaces.msg import MotionUpdate, ControllerState
from aic_control_interfaces.srv import ChangeTargetMode
from std_srvs.srv import Trigger


# =============================================================================
#  Quaternion / rigid-body transform helpers
# =============================================================================
# All quaternions are (x, y, z, w) tuples.  Poses are (p, q) pairs where p is
# a 3-tuple of metres and q is a unit quaternion.

def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def quat_norm(q):
    """Normalise a quaternion, returning identity if near-zero."""
    x, y, z, w = q
    n = math.sqrt(x*x + y*y + z*z + w*w)
    if n < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    return (x/n, y/n, z/n, w/n)


def quat_mul(a, b):
    """Hamilton product of two quaternions."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz
    )


def quat_inv(q):
    """Conjugate of a unit quaternion (= inverse for unit quaternions)."""
    x, y, z, w = q
    return (-x, -y, -z, w)


def rotate_vec_by_quat(v, q):
    """Rotate vector v by unit quaternion q using the sandwich product."""
    vx, vy, vz = v
    qv = (vx, vy, vz, 0.0)
    qi = quat_inv(q)
    r = quat_mul(quat_mul(q, qv), qi)
    return (r[0], r[1], r[2])


def tf_to_T(tf):
    """Extract (position, quaternion) from a geometry_msgs TransformStamped."""
    t = tf.transform.translation
    r = tf.transform.rotation
    p = (t.x, t.y, t.z)
    q = quat_norm((r.x, r.y, r.z, r.w))
    return p, q


def T_inv(p, q):
    """Invert a rigid-body transform (p, q)."""
    qi = quat_inv(q)
    pr = rotate_vec_by_quat(p, qi)
    return (-pr[0], -pr[1], -pr[2]), qi


def T_mul(p1, q1, p2, q2):
    """Compose two rigid-body transforms: T1 * T2."""
    p2r = rotate_vec_by_quat(p2, q1)
    return (p1[0] + p2r[0], p1[1] + p2r[1], p1[2] + p2r[2]), quat_norm(quat_mul(q1, q2))


def quat_from_axis_angle(ax, ay, az, angle):
    """Construct a quaternion from a unit axis (ax, ay, az) and angle in radians."""
    s = math.sin(angle * 0.5)
    return quat_norm((ax * s, ay * s, az * s, math.cos(angle * 0.5)))


def _stick_ramp(v, deadzone, exponent=1.5):
    """
    Apply a dead zone then a power-law ramp to an analogue stick axis value.

    Returns a value in [-1, 1]:
      - Zero for |v| < deadzone (dead zone suppresses resting drift).
      - Grows smoothly from 0 to +/-1 as the stick moves to full deflection.
      - exponent > 1 compresses small deflections for finer near-centre control;
        exponent = 1 gives a linear response.
    """
    if abs(v) < deadzone:
        return 0.0
    sign = 1.0 if v > 0.0 else -1.0
    normalised = (abs(v) - deadzone) / (1.0 - deadzone)
    return sign * (normalised ** exponent)


# =============================================================================
#  Keyboard interface
# =============================================================================

class KeyWatcher:
    """
    Non-blocking keyboard listener running on a daemon thread.

    Keys
    ----
      e  Enable VR tracking -- captures the wrist + TCP reference pose.
      q  Disable VR tracking -- robot holds its last commanded position.
      o  Toggle orientation following (translation-only when off).
      g  Toggle gripper open / closed.
      f  Toggle force-feedback stiffness modulation.
      l  Toggle workspace box limits on / off.
      x  Exit.

    State is read by the main thread via snapshot(), which is lock-protected
    and resets edge-triggered flags (e.g. gripper_toggled) on each read.
    """

    def __init__(self):
        self.enabled = False
        self.exit = False
        self.gripper_closed = False
        self.gripper_toggled = False        # edge flag -- cleared on each snapshot
        self.follow_ori_toggled = False     # edge flag for 'o' key
        self.tare_requested = False         # edge flag for 't' key
        self.force_feedback_enabled = False
        self.limits_enabled = True
        self._lock     = threading.Lock()
        self._thread   = threading.Thread(target=self._run, daemon=True)
        self._term_fd  = None   # saved before setcbreak; restored on exit
        self._term_old = None

    def start(self):
        self._thread.start()
        atexit.register(self.restore_terminal)

    def restore_terminal(self):
        """Restore terminal settings -- called via atexit so Ctrl+C never leaves
        the terminal in cbreak mode, which would require a shell reset."""
        if self._term_fd is not None and self._term_old is not None:
            try:
                termios.tcsetattr(self._term_fd, termios.TCSADRAIN, self._term_old)
            except Exception:
                pass

    def set_enabled(self, val: bool):
        """Thread-safe write to enabled flag (used by joy_callback)."""
        with self._lock:
            self.enabled = val

    def _run(self):
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        self._term_fd  = fd
        self._term_old = old
        try:
            tty.setcbreak(fd)
            while True:
                r, _, _ = select.select([sys.stdin], [], [], 0.1)
                with self._lock:
                    if self.exit:
                        return
                if not r:
                    continue
                ch = sys.stdin.read(1)
                with self._lock:
                    if ch == 'e':
                        self.enabled = True
                        print("\n[KEY] ENABLE (e) -- capturing reference")
                    elif ch == 'q':
                        self.enabled = False
                        print("\n[KEY] DISABLE (q)")
                    elif ch == 'o':
                        self.follow_ori_toggled = True
                        print("\n[KEY] orientation follow toggled (o)")
                    elif ch == 't':
                        self.tare_requested = True
                        print("\n[KEY] F/T tare requested (t)")
                    elif ch == 'g':
                        self.gripper_closed = not self.gripper_closed
                        self.gripper_toggled = True
                        state = "CLOSE" if self.gripper_closed else "OPEN"
                        print(f"\n[KEY] gripper -> {state} (g)")
                    elif ch == 'f':
                        self.force_feedback_enabled = not self.force_feedback_enabled
                        print(f"\n[KEY] force_feedback = {self.force_feedback_enabled} (f)")
                    elif ch == 'l':
                        self.limits_enabled = not self.limits_enabled
                        state = "ON" if self.limits_enabled else "OFF  [limits suppressed]"
                        print(f"\n[KEY] workspace_limits = {state} (l)")
                    elif ch == 'x':
                        self.exit = True
                        print("\n[KEY] EXIT (x)")
                        return
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self._term_fd  = None   # mark as already restored so atexit is a no-op
            self._term_old = None

    def snapshot(self):
        """Return current state and reset edge-triggered flags."""
        with self._lock:
            gripper_tog   = self.gripper_toggled
            follow_tog    = self.follow_ori_toggled
            tare_req      = self.tare_requested
            self.gripper_toggled   = False
            self.follow_ori_toggled = False
            self.tare_requested    = False
            return (self.enabled, self.exit,
                    self.gripper_closed, gripper_tog,
                    follow_tog, tare_req,
                    self.force_feedback_enabled, self.limits_enabled)


# =============================================================================
#  Impedance parameter presets
# =============================================================================
# The AIC impedance controller accepts per-command 6x6 stiffness and damping
# matrices as flat float64[36] arrays (row-major).  Diagonal matrices are used
# here; off-diagonal coupling terms can be added if needed.

def make_diagonal_6x6(diag_val):
    """Return a flat float64[36] diagonal 6x6 matrix."""
    m = [0.0] * 36
    for i in range(6):
        m[i * 6 + i] = diag_val
    return m


# Conservative defaults matching AIC controller documentation
DEFAULT_STIFFNESS   = make_diagonal_6x6(85.0)
DEFAULT_DAMPING     = make_diagonal_6x6(75.0)

# Reduced stiffness for open-loop teleoperation -- improves compliance and
# reduces the risk of large contact forces during unconstrained motion
TELEOP_STIFFNESS    = make_diagonal_6x6(60.0)
TELEOP_DAMPING      = make_diagonal_6x6(50.0)

# Minimum stiffness applied at high contact forces during force-feedback mode;
# provides maximum compliance for constrained insertion tasks
INSERTION_STIFFNESS = make_diagonal_6x6(30.0)
INSERTION_DAMPING   = make_diagonal_6x6(25.0)


# =============================================================================
#  Main node
# =============================================================================

class OculusTFToAICController(Node):
    def __init__(self):
        super().__init__('oculus_tf_to_aic_controller')

        # ── TF frame identifiers ──────────────────────────────────────────────
        # base_link  : UR5e robot base frame (REP-103: X forward, Y lateral, Z up)
        # oculus_r   : right controller wrist frame published by oculus_reader
        # gripper/tcp: end-effector TCP frame including Robotiq Hand-E offset
        self.base_frame = 'base_link'
        self.ctrl_frame = 'oculus_r'
        self.tcp_frame  = 'gripper/tcp'

        # ── Command rate ──────────────────────────────────────────────────────
        # The AIC impedance controller accepts policy commands at 10-30 Hz and
        # internally interpolates to its 500 Hz servo loop.  30 Hz gives tight
        # tracking responsiveness while remaining within the supported range.
        self.rate_hz = 30.0

        # ── Wrist-tracking safety parameters ─────────────────────────────────
        # max_step_xyz caps the per-tick position increment to prevent large
        # jumps caused by TF latency spikes or sudden wrist movements.
        # At 30 Hz, 0.020 m/tick corresponds to a 0.60 m/s speed ceiling.
        #
        # pos_lpf_alpha is the first-order low-pass coefficient applied to the
        # position target before publishing.  Higher values pass more of the
        # new sample (more responsive); lower values smooth more aggressively.
        # alpha = 0.55 gives ~65 ms settling at 30 Hz while suppressing TF jitter.
        self.max_step_xyz  = 0.020   # m/tick
        self.pos_lpf_alpha = 0.55    # [0, 1] -- higher is more responsive
        self._p_tgt_filt   = None    # running filter state

        # Maximum Euclidean displacement from the capture reference.
        # Acts as a hard safety sphere -- motion beyond this radius is clamped.
        self.max_total_offset = 0.35  # metres

        # ── Workspace box limits in base_link (metres) ────────────────────────
        # Restrict the commanded TCP position to a safe operating volume.
        # Limit X is negative because the task board is in front of the robot
        # along the negative X direction in this workcell configuration.
        # Adjust to suit the physical mounting and task layout.
        self.limit_x = (-0.65, -0.15)   # forward / back
        self.limit_y = (-0.45,  0.45)   # left / right
        self.limit_z = ( 0.05,  0.50)   # up / down
        self.enable_workspace_limits = False  # master switch (also toggled by 'l')

        # ── TF listener ───────────────────────────────────────────────────────
        self.tf_buffer   = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # ── Pose command publisher ────────────────────────────────────────────
        # MotionUpdate carries the target pose plus per-command stiffness and
        # damping matrices.  The AIC controller requires RELIABLE QoS.
        qos = QoSProfile(depth=10)
        qos.reliability = ReliabilityPolicy.RELIABLE
        self.pose_pub = self.create_publisher(
            MotionUpdate,
            '/aic_controller/pose_commands',
            qos
        )

        # ── Gripper publisher ─────────────────────────────────────────────────
        # Commands the Robotiq Hand-E via a JointState message.
        # Joint: hande_left_finger_joint (right finger is a mimic).
        # Range: 0.0 m (fully closed) to 0.025 m (fully open) per finger slider.
        # Note: verify the command interface against the aic_eval package --
        # it may be a ros2_control GripperActionController or a custom topic.
        self.gripper_pub = self.create_publisher(
            JointState,
            '/gripper_commands',
            10
        )

        # ── Software F/T bias ─────────────────────────────────────────────────────
        # Subtracted from all wrench readings to remove residual gravity and
        # cable-load terms the hardware tare may leave behind.  Without this,
        # a constant bias vector causes force magnitude to decrease under
        # contact as the applied force partially cancels the bias.
        self._ft_bias = (0.0, 0.0, 0.0)

        # ── Axia80 force-torque subscriber ────────────────────────────────────
        # Used to modulate impedance stiffness during contact-rich tasks.
        # Force magnitude drives a linear interpolation between TELEOP and
        # INSERTION stiffness presets (see _compute_force_adjusted_stiffness).
        self.latest_wrench = None
        self.ft_sub = self.create_subscription(
            WrenchStamped,
            '/fts_broadcaster/wrench',
            self._ft_callback,
            10
        )

        # ── AIC controller state subscriber ───────────────────────────────────
        # Provides tracking error, current TCP pose, and controller diagnostics.
        self.latest_ctrl_state = None
        self.ctrl_state_sub = self.create_subscription(
            ControllerState,
            '/aic_controller/controller_state',
            self._ctrl_state_callback,
            10
        )

        # ── Switch controller to Cartesian target mode ────────────────────────
        # mode=1: Cartesian pose tracking (required for MotionUpdate commands)
        # mode=2: joint-space tracking
        self.switch_cli = self.create_client(
            ChangeTargetMode,
            '/aic_controller/change_target_mode'
        )
        self._switch_to_cartesian()

        # ── Tare the F/T sensor ───────────────────────────────────────────────
        # Zeros the Axia80 bias at startup so gravity and cable loads are
        # removed before contact force feedback is used.
        self.tare_cli = self.create_client(
            Trigger,
            '/aic_controller/tare_force_torque_sensor'
        )
        self._tare_ft_sensor()

        # ── Keyboard watcher ──────────────────────────────────────────────────
        self.keys = KeyWatcher()
        self.keys.start()
        print("\nKeyboard controls:")
        print("  e  enable VR tracking  (captures wrist + TCP reference)")
        print("  q  disable VR tracking (robot holds last commanded pose)")
        print("  o  toggle orientation follow")
        print("  t  tare F/T sensor (re-zero Axia80 bias)")
        print("  g  toggle gripper open / closed")
        print("  f  toggle force-feedback stiffness modulation")
        print("  l  toggle workspace box limits")
        print("  x  exit")
        print("\nRight controller:")
        print("  A              cycle mode: IDLE -> VR TRACKING -> ANALOGUE -> IDLE")
        print("  B              toggle orientation follow")
        print("  RJ (stick click) toggle analogue frame (base_link <-> TCP)")
        print("  stick          yaw (X-axis) + Z up/down (Y-axis)")
        print("  grip + stick   XY translation (horizontal plane)")
        print("  trigger + stick  pitch (X-axis) + roll (Y-axis)")
        print("  (stick offsets persist until analogue is re-enabled or 'e' recaptures)\n")

        # ── VR reference transforms ───────────────────────────────────────────
        # Captured on the first tick after 'e' is pressed.  The delta between
        # the current controller pose and this reference drives the TCP target.
        self.have_ref      = False
        self.p_base_ctrl0  = None   # controller position at capture (base_link)
        self.q_base_ctrl0  = None   # controller orientation at capture
        self.p_base_tcp0   = None   # TCP position at capture (base_link)
        self.q_base_tcp0   = None   # TCP orientation at capture

        # Last pose sent to the controller -- used for the step-size clamp and
        # as the starting point when VR tracking is re-enabled after a pause.
        self.last_cmd_p = None
        self.last_cmd_q = None

        # Stiffness / damping state (updated each tick based on force feedback)
        self.active_stiffness = list(TELEOP_STIFFNESS)
        self.active_damping   = list(TELEOP_DAMPING)

        # Orientation follow -- toggled by keyboard 'o' or controller B
        self.follow_orientation = False

        # HUD display state -- shadows of runtime flags kept for the renderer
        self._hud_follow_ori    = False
        self._hud_limits_active = True

        # ── Analogue stick configuration ──────────────────────────────────────
        # Joy message layout published by viz_transforms.py (oculus_reader):
        #   Topic: /oculus/right/joy
        #   axes[0]    rightJS X   (-1 = left,     +1 = right)
        #   axes[1]    rightJS Y   (-1 = backward, +1 = forward)
        #   axes[2]    rightTrig   ( 0 = released,  1 = fully pulled)
        #   axes[3]    rightGrip   ( 0 = released,  1 = fully squeezed)
        #   buttons[0] A
        #   buttons[1] B
        #   buttons[2] RJ  (joystick click)
        #   buttons[3] RG  (grip button digital)
        #   buttons[4] RTr (trigger button digital)
        #   buttons[5] RThU
        self.joy_topic          = '/oculus/right/joy'
        self.stick_axis_x       = 0   # rightJS horizontal
        self.stick_axis_y       = 1   # rightJS vertical
        self.stick_axis_trigger = 2   # rightTrig  (analogue 0-1)
        self.stick_axis_grip    = 3   # rightGrip  (analogue 0-1)
        self.btn_a_idx          = 0   # A -- mode cycle (IDLE → VR → ANALOGUE → IDLE)
        self.btn_b_idx          = 1   # B -- toggle orientation follow
        self.btn_rj_idx         = 2   # RJ (joystick click) -- toggle command frame

        # Stick response shaping.
        # dead zone:      suppresses resting controller drift
        # ramp exponent:  2.0 = quadratic (fine near centre, fast near edges)
        # mod threshold:  grip/trigger analogue level required to enter a mode;
        #                 0.30 is deliberately low because grip analog can dip
        #                 when the hand shifts to push the thumbstick
        self.stick_deadzone    = 0.15
        self.stick_ramp_exp    = 2.0
        self.stick_mod_thresh  = 0.30

        # Maximum incremental change per tick at full stick deflection.
        # At 30 Hz these correspond to:
        #   2.5e-3 rad/tick ~= 4.3 deg/s  (rotation axes)
        #   1.5e-4 m/tick   ~= 4.5 mm/s   (translation axes)
        # Scale in x1.5 steps to adjust feel.
        self.stick_yaw_speed   = 2.5e-3   # rad/tick
        self.stick_pitch_speed = 2.5e-3   # rad/tick
        self.stick_roll_speed  = 2.5e-3   # rad/tick
        self.stick_z_speed     = 1.5e-4   # m/tick
        self.stick_xy_speed    = 1.5e-4   # m/tick

        # ── Analogue stick runtime state ──────────────────────────────────────
        self.analogue_enabled = False
        self.analogue_frame   = 'base'   # 'base' = base_link axes, 'tcp' = TCP-relative
        self._joy_btn_a_prev  = False
        self._joy_btn_b_prev  = False
        self._joy_btn_rj_prev = False

        # Fixed TCP pose captured when analogue mode is enabled.  All stick
        # offsets are applied relative to this reference rather than to
        # last_cmd_p, which prevents the offset from compounding every tick.
        self.analogue_ref_p = None
        self.analogue_ref_q = None

        # Accumulated stick offsets -- zeroed when analogue is enabled or when
        # 'e' re-captures the VR reference.
        self.stick_p_offset = [0.0, 0.0, 0.0]          # metres, base_link
        self.stick_q_offset = (0.0, 0.0, 0.0, 1.0)     # quaternion delta

        self.latest_joy = None
        self.joy_sub = self.create_subscription(
            Joy,
            self.joy_topic,
            self._joy_callback,
            10
        )

        self.timer = self.create_timer(1.0 / self.rate_hz, self.tick)

    # =========================================================================
    #  Service helpers
    # =========================================================================

    def _switch_to_cartesian(self):
        """Request Cartesian target mode from the AIC controller (mode=1)."""
        if not self.switch_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn("ChangeTargetMode service unavailable -- will retry later.")
            return
        req = ChangeTargetMode.Request()
        req.target_mode.mode = 1
        future = self.switch_cli.call_async(req)
        future.add_done_callback(
            lambda f: self.get_logger().info("AIC controller switched to Cartesian mode.")
        )

    def _tare_ft_sensor(self):
        """
        Zero the F/T sensor via hardware tare service and software bias capture.

        Hardware tare resets the sensor's internal offset registers.
        Software bias captures the current wrench and subtracts it from all
        subsequent readings, correcting any residual gravity or cable load the
        hardware tare leaves behind.  Together they ensure that corrected force
        magnitude is near zero at rest and increases correctly under contact.
        """
        if not self.tare_cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn("F/T tare service unavailable -- skipping hardware tare.")
        else:
            req = Trigger.Request()
            future = self.tare_cli.call_async(req)
            future.add_done_callback(
                lambda f: self.get_logger().info("F/T hardware tare complete.")
            )
        self._tare_ft_software()

    def _tare_ft_software(self):
        """
        Capture the current wrench as a software bias to subtract from all
        subsequent readings.  Safe to call at any time; if no wrench has
        arrived yet the bias stays at zero and a warning is logged.
        """
        if self.latest_wrench is None:
            self.get_logger().warn("F/T software tare: no wrench received yet -- bias unchanged.")
            return
        f = self.latest_wrench.wrench.force
        self._ft_bias = (f.x, f.y, f.z)
        mag = math.sqrt(f.x**2 + f.y**2 + f.z**2)
        self.get_logger().info(
            f"F/T software bias set: x={f.x:.2f} y={f.y:.2f} z={f.z:.2f} N  (mag {mag:.2f} N)"
        )

    def _corrected_force_mag(self):
        """
        Return the bias-corrected contact force magnitude in Newtons.

        Subtracts the stored software bias from the raw wrench before computing
        the Euclidean norm, so gravity and cable-load offsets are removed and
        only genuine contact forces contribute to the reading.
        """
        if self.latest_wrench is None:
            return 0.0
        f = self.latest_wrench.wrench.force
        fx = f.x - self._ft_bias[0]
        fy = f.y - self._ft_bias[1]
        fz = f.z - self._ft_bias[2]
        return math.sqrt(fx**2 + fy**2 + fz**2)

    # =========================================================================
    #  Subscriber callbacks
    # =========================================================================

    def _ft_callback(self, msg: WrenchStamped):
        self.latest_wrench = msg

    def _ctrl_state_callback(self, msg: ControllerState):
        self.latest_ctrl_state = msg

    # =========================================================================
    #  TF helpers
    # =========================================================================

    def _lookup(self, target, source):
        """Look up the most recent transform from source to target frame."""
        return self.tf_buffer.lookup_transform(
            target, source, rclpy.time.Time(), timeout=Duration(seconds=0.05)
        )

    def _capture_reference(self):
        """
        Snapshot the current controller and TCP poses as the VR reference.

        Called on the first tick after 'e' is pressed.  Subsequent ticks
        compute a delta from this snapshot and apply it to p_base_tcp0 to
        derive the commanded TCP pose.  Stick offsets are also zeroed here
        so any accumulated analogue adjustment does not carry into the new
        wrist-tracking session.
        """
        tf_bc = self._lookup(self.base_frame, self.ctrl_frame)
        tf_bt = self._lookup(self.base_frame, self.tcp_frame)
        self.p_base_ctrl0, self.q_base_ctrl0 = tf_to_T(tf_bc)
        self.p_base_tcp0,  self.q_base_tcp0  = tf_to_T(tf_bt)
        self.have_ref       = True
        self.last_cmd_p     = self.p_base_tcp0
        self.last_cmd_q     = self.q_base_tcp0
        self._p_tgt_filt    = None
        self.stick_p_offset = [0.0, 0.0, 0.0]
        self.stick_q_offset = (0.0, 0.0, 0.0, 1.0)
        self.get_logger().info("Reference captured: controller + TCP poses recorded.")

    # =========================================================================
    #  Gripper
    # =========================================================================

    def _send_gripper_command(self, close: bool):
        """
        Command the Robotiq Hand-E to a binary open or closed position.

        Publishes a JointState for hande_left_finger_joint.  The right finger
        joint is a mimic and follows automatically in the controller.

        Position range: 0.0 m (closed) to 0.025 m (open) per finger slider.

        Note: confirm the command interface against the aic_eval package.
        Depending on integration, this may need to target a
        ros2_control GripperActionController or a different topic.
        """
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name     = ['hande_left_finger_joint']
        msg.position = [0.0 if close else 0.025]
        msg.velocity = []
        msg.effort   = []
        self.gripper_pub.publish(msg)
        self.get_logger().info(f"Gripper -> {'CLOSED' if close else 'OPEN'}")

    # =========================================================================
    #  Force-feedback stiffness modulation
    # =========================================================================

    def _compute_force_adjusted_stiffness(self):
        """
        Linearly reduce Cartesian stiffness with increasing contact force.

        Below 2 N  -- full teleop stiffness (compliant but responsive).
        At    20 N -- minimum stiffness (highly compliant for constrained insertion).
        Above 20 N -- clamped at minimum.

        This trades position accuracy for compliance during contact, which is
        desirable for cable and connector insertion tasks where high stiffness
        would cause the robot to fight back against the environment.
        """
        force_mag = self._corrected_force_mag()

        force_lo = 2.0    # N -- below this, no reduction
        force_hi = 20.0   # N -- above this, maximum reduction

        if force_mag < force_lo:
            return list(TELEOP_STIFFNESS), list(TELEOP_DAMPING)

        t = min(1.0, (force_mag - force_lo) / (force_hi - force_lo))
        stiff_val = 60.0 * (1.0 - t) + 15.0 * t
        damp_val  = 50.0 * (1.0 - t) + 12.0 * t
        return make_diagonal_6x6(stiff_val), make_diagonal_6x6(damp_val)

    # =========================================================================
    #  Analogue stick
    # =========================================================================

    def _joy_callback(self, msg: Joy):
        """
        Process incoming Joy messages from the right Oculus controller.

        All buttons use rising-edge detection to avoid repeated toggles
        from a single physical press.

        Button assignments
        ------------------
          A   Cycle control mode: IDLE -> VR TRACKING -> ANALOGUE -> IDLE
          B   Toggle orientation follow
          RJ  Toggle analogue command frame (base_link <-> TCP)
        """
        def _btn(i):
            return bool(msg.buttons[i]) if len(msg.buttons) > i else False

        # Button A -- cycle control mode (mutually exclusive)
        a_now = _btn(self.btn_a_idx)
        if a_now and not self._joy_btn_a_prev:
            if not self.keys.enabled and not self.analogue_enabled:
                # IDLE -> VR TRACKING
                self.keys.set_enabled(True)
                self.analogue_enabled  = False
                self.have_ref          = False   # reference captured next tick
                self.get_logger().info('Mode -> VR TRACKING  [A]')
            elif self.keys.enabled and not self.analogue_enabled:
                # VR TRACKING -> ANALOGUE
                self.keys.set_enabled(False)
                self.analogue_enabled = True
                self.analogue_ref_p   = list(self.last_cmd_p) \
                    if self.last_cmd_p is not None else None
                self.analogue_ref_q   = self.last_cmd_q
                self.stick_p_offset   = [0.0, 0.0, 0.0]
                self.stick_q_offset   = (0.0, 0.0, 0.0, 1.0)
                self.get_logger().info('Mode -> ANALOGUE  [A]')
            else:
                # ANALOGUE -> IDLE
                self.keys.set_enabled(False)
                self.analogue_enabled = False
                self.get_logger().info('Mode -> IDLE  [A]')
        self._joy_btn_a_prev = a_now

        # Button B -- toggle orientation follow
        b_now = _btn(self.btn_b_idx)
        if b_now and not self._joy_btn_b_prev:
            self.follow_orientation = not self.follow_orientation
            state = 'ON' if self.follow_orientation else 'OFF'
            self.get_logger().info(f'Orientation follow -> {state}  [B]')
        self._joy_btn_b_prev = b_now

        # Button RJ (joystick click) -- toggle analogue command frame
        rj_now = _btn(self.btn_rj_idx)
        if rj_now and not self._joy_btn_rj_prev:
            self.analogue_frame = 'tcp' if self.analogue_frame == 'base' else 'base'
            self.get_logger().info(f'Analogue frame -> {self.analogue_frame}  [RJ]')
        self._joy_btn_rj_prev = rj_now

        self.latest_joy = msg

    def _apply_stick_nudge(self, p_tgt, q_tgt):
        """
        Apply accumulated analogue stick offsets to a pose and return the result.

        Offsets are persistent -- the robot holds its nudged position when the
        stick returns to centre.  They are zeroed when analogue mode is enabled
        (Button A) or when the VR reference is re-captured ('e').

        Modes
        -----
          No modifier  -- yaw (stick X) + Z translation (stick Y)
          Grip held    -- XY translation in the horizontal plane
          Trigger held -- pitch (stick X) + roll (stick Y)
          Grip takes priority when both grip and trigger exceed the threshold.

        Frame
        -----
          'base'  Deltas applied directly in base_link axes.
          'tcp'   Deltas rotated into the current TCP frame, so "forward" means
                  along the gripper approach axis regardless of wrist orientation.
        """
        if self.latest_joy is None:
            return (
                (p_tgt[0] + self.stick_p_offset[0],
                 p_tgt[1] + self.stick_p_offset[1],
                 p_tgt[2] + self.stick_p_offset[2]),
                quat_norm(quat_mul(self.stick_q_offset, q_tgt))
            )

        axes = self.latest_joy.axes

        def _ax(i):
            return axes[i] if len(axes) > i else 0.0

        sx = _stick_ramp(_ax(self.stick_axis_x), self.stick_deadzone, self.stick_ramp_exp)
        sy = _stick_ramp(_ax(self.stick_axis_y), self.stick_deadzone, self.stick_ramp_exp)
        grip_held    = _ax(self.stick_axis_grip)    >= self.stick_mod_thresh
        trigger_held = _ax(self.stick_axis_trigger) >= self.stick_mod_thresh

        def _frame_axis(local_axis):
            """Express a local-frame axis in base_link, rotating by TCP orientation if needed."""
            if self.analogue_frame == 'tcp':
                return rotate_vec_by_quat(local_axis, q_tgt)
            return local_axis

        if grip_held:
            # XY translation -- stick X/Y map to robot X/Y (or TCP X/Y in TCP frame)
            dx = sx * self.stick_xy_speed
            dy = sy * self.stick_xy_speed
            local = rotate_vec_by_quat((dx, dy, 0.0), q_tgt) \
                if self.analogue_frame == 'tcp' else (dx, dy, 0.0)
            self.stick_p_offset[0] += local[0]
            self.stick_p_offset[1] += local[1]
            self.stick_p_offset[2] += local[2]

        elif trigger_held:
            # Pitch + roll -- stick X drives pitch (rotation about Y axis),
            # stick Y drives roll (rotation about X axis).  Signs are tuned for
            # intuitive feel relative to the operator's perspective.
            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 1.0, 0.0))
                dq = quat_from_axis_angle(*axis, -sx * self.stick_pitch_speed)
                self.stick_q_offset = quat_norm(quat_mul(dq, self.stick_q_offset))
            if abs(sy) > 0.0:
                axis = _frame_axis((1.0, 0.0, 0.0))
                dq = quat_from_axis_angle(*axis, -sy * self.stick_roll_speed)
                self.stick_q_offset = quat_norm(quat_mul(dq, self.stick_q_offset))

        else:
            # Yaw + Z -- default mode for repositioning without a modifier
            dz = sy * self.stick_z_speed
            local_z = rotate_vec_by_quat((0.0, 0.0, dz), q_tgt) \
                if self.analogue_frame == 'tcp' else (0.0, 0.0, dz)
            self.stick_p_offset[0] += local_z[0]
            self.stick_p_offset[1] += local_z[1]
            self.stick_p_offset[2] += local_z[2]

            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 0.0, 1.0))
                dq = quat_from_axis_angle(*axis, -sx * self.stick_yaw_speed)
                self.stick_q_offset = quat_norm(quat_mul(dq, self.stick_q_offset))

        p_out = (
            p_tgt[0] + self.stick_p_offset[0],
            p_tgt[1] + self.stick_p_offset[1],
            p_tgt[2] + self.stick_p_offset[2],
        )
        return p_out, quat_norm(quat_mul(self.stick_q_offset, q_tgt))

    # =========================================================================
    #  Terminal HUD
    # =========================================================================

    def _render_hud(self):
        """
        Render a live status HUD anchored to the bottom of the terminal.

        Uses ANSI escape sequences to write into the terminal's bottom rows
        without disturbing the scrolling log output above.  Redraws every tick
        (30 Hz) so any glitch from a concurrent print() self-corrects within
        one frame.

        Layout (4 lines from bottom):
          ─────────────────────────────────────  separator
          MODE   VR ● TRACKING   ANALOGUE ● ON   FRAME: tcp   ORI: on
          F/T    ████████████░░░░░░░░░░░░░░░░   12.4 N   contact
                 0          2N               20N          scale
        """
        try:
            term   = shutil.get_terminal_size((80, 24))
            cols   = term.columns
            rows   = term.lines
        except Exception:
            return

        # ANSI colour codes
        GRN  = '\033[32m'
        YLW  = '\033[33m'
        RED  = '\033[31m'
        CYN  = '\033[36m'
        DIM  = '\033[2m'
        BOLD = '\033[1m'
        RST  = '\033[0m'

        # ── Mode line ─────────────────────────────────────────────────────────
        vr_on   = self.have_ref
        an_on   = self.analogue_enabled
        ori_on  = self._hud_follow_ori
        lim_on  = self._hud_limits_active

        def _indicator(active, label_on, label_off, col_on, col_off=DIM):
            dot = '●' if active else '○'
            col = col_on if active else col_off
            lbl = label_on if active else label_off
            return f"{col}{dot} {lbl}{RST}"

        mode_parts = [
            f"  {BOLD}MODE{RST}",
            f"VR {_indicator(vr_on, 'TRACKING', 'IDLE    ', GRN)}",
            f"ANALOGUE {_indicator(an_on, 'ON ', 'OFF', CYN)}",
            f"FRAME {CYN}{self.analogue_frame:<4}{RST}",
            f"ORI {_indicator(ori_on, 'on ', 'off', CYN)}",
        ]
        mode_line = "   ".join(mode_parts)

        # ── Force bar ─────────────────────────────────────────────────────────
        f_mag = self._corrected_force_mag()

        bar_width   = 30          # characters
        f_scale_max = 25.0        # N — full bar at this force
        filled      = int(min(1.0, f_mag / f_scale_max) * bar_width)
        empty       = bar_width - filled

        if f_mag < 2.0:
            bar_col = GRN;  status = 'free   '
        elif f_mag < 20.0:
            bar_col = YLW;  status = 'contact'
        else:
            bar_col = RED;  status = 'LIMIT  '

        bar       = f"{bar_col}{'█' * filled}{'░' * empty}{RST}"
        force_line = (
            f"  {BOLD}F/T {RST}  {bar}  "
            f"{bar_col}{f_mag:5.1f} N{RST}  {DIM}{status}{RST}"
        )

        # Threshold tick marks aligned under the bar
        # Bar starts at col 9 (after "  F/T  "), width=30, scale 0–25 N
        # 2 N mark  = 2/25 * 30 ≈ 2 chars in
        # 20 N mark = 20/25 * 30 = 24 chars in
        bar_offset  = 9   # chars before bar starts
        mark_2n     = bar_offset + int(2.0  / f_scale_max * bar_width)
        mark_20n    = bar_offset + int(20.0 / f_scale_max * bar_width)
        scale_row   = [' '] * (bar_offset + bar_width + 14)
        for i, label in [(mark_2n, '2N'), (mark_20n, '20N')]:
            for j, ch in enumerate(label):
                if i + j < len(scale_row):
                    scale_row[i + j] = ch
        scale_line  = f"  {DIM}{''.join(scale_row)}{RST}"

        quit_tag = f"  {BOLD}[x]{RST}{DIM} quit{RST}"
        dash_w   = max(0, cols - 4 - 10)   # 10 = len('  [x] quit')
        sep_line = f"  {DIM}{'─' * dash_w}{RST}{quit_tag}"

        # ── Write to terminal bottom ───────────────────────────────────────────
        hud_lines = [sep_line, mode_line, force_line, scale_line]
        n         = len(hud_lines)

        buf = '\033[s'   # save cursor position
        for i, line in enumerate(hud_lines):
            row = rows - n + i + 1   # 1-indexed terminal row
            buf += f'\033[{row};1H\033[2K{line}'
        buf += '\033[u'   # restore cursor position
        sys.stdout.write(buf)
        sys.stdout.flush()

    # =========================================================================
    #  Main control tick  (30 Hz)
    # =========================================================================

    def tick(self):
        (enabled, do_exit,
         gripper_closed, gripper_toggled,
         follow_ori_toggled, tare_requested,
         force_fb, limits_enabled) = self.keys.snapshot()

        # Keyboard 'o' edge flag -- merge with controller B state
        if follow_ori_toggled:
            self.follow_orientation = not self.follow_orientation
            state = 'ON' if self.follow_orientation else 'OFF'
            self.get_logger().info(f'Orientation follow -> {state}  [o]')

        # Keyboard 't' edge flag -- manual F/T tare
        if tare_requested:
            self._tare_ft_sensor()

        # Mirror KeyWatcher enabled flag (can be set by controller A)
        enabled = self.keys.enabled

        # Keep HUD shadows in sync
        self._hud_follow_ori    = self.follow_orientation
        self._hud_limits_active = limits_enabled

        self._render_hud()

        if do_exit:
            rclpy.shutdown()
            return

        if gripper_toggled:
            self._send_gripper_command(gripper_closed)

        if not enabled:
            self.have_ref = False

            # Analogue-only mode -- VR tracking is off but the stick is active.
            # Nudges the last commanded pose and republishes every tick so the
            # impedance controller continues to receive a stable target.
            # Requires at least one prior VR session to establish analogue_ref_p.
            if self.analogue_enabled and self.analogue_ref_p is not None:
                try:
                    p_tgt, q_tgt = self._apply_stick_nudge(
                        tuple(self.analogue_ref_p), self.analogue_ref_q)
                    if self.enable_workspace_limits and limits_enabled:
                        p_tgt = (
                            clamp(p_tgt[0], self.limit_x[0], self.limit_x[1]),
                            clamp(p_tgt[1], self.limit_y[0], self.limit_y[1]),
                            clamp(p_tgt[2], self.limit_z[0], self.limit_z[1]),
                        )
                    stiffness = list(TELEOP_STIFFNESS)
                    damping   = list(TELEOP_DAMPING)
                    msg = MotionUpdate()
                    msg.header.stamp    = self.get_clock().now().to_msg()
                    msg.header.frame_id = 'base_link'
                    msg.pose.position.x    = float(p_tgt[0])
                    msg.pose.position.y    = float(p_tgt[1])
                    msg.pose.position.z    = float(p_tgt[2])
                    msg.pose.orientation.x = float(q_tgt[0])
                    msg.pose.orientation.y = float(q_tgt[1])
                    msg.pose.orientation.z = float(q_tgt[2])
                    msg.pose.orientation.w = float(q_tgt[3])
                    msg.target_stiffness = stiffness
                    msg.target_damping   = damping
                    msg.feedforward_wrench_at_tip.force.x  = 0.0
                    msg.feedforward_wrench_at_tip.force.y  = 0.0
                    msg.feedforward_wrench_at_tip.force.z  = 0.0
                    msg.feedforward_wrench_at_tip.torque.x = 0.0
                    msg.feedforward_wrench_at_tip.torque.y = 0.0
                    msg.feedforward_wrench_at_tip.torque.z = 0.0
                    msg.wrench_feedback_gains_at_tip = [0.0] * 6
                    msg.trajectory_generation_mode.mode = 2
                    self.pose_pub.publish(msg)
                    self.last_cmd_p = p_tgt
                    self.last_cmd_q = q_tgt
                except Exception:
                    pass
            return

        try:
            if not self.have_ref:
                self._capture_reference()

            # ── Step 1: compute controller motion delta since reference capture ──
            tf_bc = self._lookup(self.base_frame, self.ctrl_frame)
            p_base_ctrl, q_base_ctrl = tf_to_T(tf_bc)

            p0i, q0i = T_inv(self.p_base_ctrl0, self.q_base_ctrl0)
            p_delta, q_delta = T_mul(p0i, q0i, p_base_ctrl, q_base_ctrl)

            # ── Step 2: remap controller axes to robot base_link axes ─────────
            # The Oculus controller frame and the UR5e base_link frame are not
            # aligned in this workcell.  The mapping below was determined
            # empirically with the operator facing the task board:
            #
            #   X_robot =  Y_ctrl   (controller left/right -> robot forward/back)
            #   Y_robot =  X_ctrl   (controller forward    -> robot lateral)
            #   Z_robot = -Z_ctrl   (controller up         -> robot up, sign flipped)
            #
            # To re-derive this mapping, move the controller in each axis and
            # observe the resulting TCP motion direction in RViz or the terminal.
            p_delta_mapped = (p_delta[1], p_delta[0], -p_delta[2])
            q_delta_mapped = (q_delta[1], q_delta[0], -q_delta[2], q_delta[3])

            # ── Step 3: apply delta to reference TCP pose ─────────────────────
            p_tgt = (
                self.p_base_tcp0[0] + p_delta_mapped[0],
                self.p_base_tcp0[1] + p_delta_mapped[1],
                self.p_base_tcp0[2] + p_delta_mapped[2],
            )
            q_tgt = quat_mul(q_delta_mapped, self.q_base_tcp0)

            # ── Step 4: apply analogue stick offsets (when enabled) ───────────
            if self.analogue_enabled:
                p_tgt, q_tgt = self._apply_stick_nudge(p_tgt, q_tgt)

            # ── Step 5: safety limits ─────────────────────────────────────────
            # Sphere clamp -- limit total displacement from reference pose
            dx = p_tgt[0] - self.p_base_tcp0[0]
            dy = p_tgt[1] - self.p_base_tcp0[1]
            dz = p_tgt[2] - self.p_base_tcp0[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist > self.max_total_offset:
                scale = self.max_total_offset / max(1e-9, dist)
                p_tgt = (self.p_base_tcp0[0] + dx*scale,
                         self.p_base_tcp0[1] + dy*scale,
                         self.p_base_tcp0[2] + dz*scale)

            # Per-tick step cap -- limits effective velocity to prevent jumps
            if self.last_cmd_p is not None:
                sx = clamp(p_tgt[0] - self.last_cmd_p[0], -self.max_step_xyz, self.max_step_xyz)
                sy = clamp(p_tgt[1] - self.last_cmd_p[1], -self.max_step_xyz, self.max_step_xyz)
                sz = clamp(p_tgt[2] - self.last_cmd_p[2], -self.max_step_xyz, self.max_step_xyz)
                p_tgt = (self.last_cmd_p[0] + sx,
                         self.last_cmd_p[1] + sy,
                         self.last_cmd_p[2] + sz)

            # Hold reference orientation when orientation tracking is off
            if not self.follow_orientation:
                q_tgt = self.q_base_tcp0

            # Workspace box clamp (suppressed when 'l' is toggled off)
            if self.enable_workspace_limits and limits_enabled:
                p_tgt = (
                    clamp(p_tgt[0], self.limit_x[0], self.limit_x[1]),
                    clamp(p_tgt[1], self.limit_y[0], self.limit_y[1]),
                    clamp(p_tgt[2], self.limit_z[0], self.limit_z[1]),
                )

            # ── Step 6: first-order low-pass filter on position ───────────────
            # Attenuates high-frequency TF jitter before the target reaches the
            # impedance controller.  Orientation is not filtered.
            if self._p_tgt_filt is None:
                self._p_tgt_filt = p_tgt
            else:
                a = self.pos_lpf_alpha
                self._p_tgt_filt = (
                    a * p_tgt[0] + (1 - a) * self._p_tgt_filt[0],
                    a * p_tgt[1] + (1 - a) * self._p_tgt_filt[1],
                    a * p_tgt[2] + (1 - a) * self._p_tgt_filt[2],
                )
            p_tgt = self._p_tgt_filt

            # ── Step 7: select stiffness / damping ───────────────────────────
            if force_fb:
                stiffness, damping = self._compute_force_adjusted_stiffness()
            else:
                stiffness = list(TELEOP_STIFFNESS)
                damping   = list(TELEOP_DAMPING)

            # ── Step 8: build and publish MotionUpdate ────────────────────────
            # The pose is expressed as an absolute target in base_link.
            # trajectory_generation_mode = 2 (MODE_POSITION) instructs the
            # controller to track the pose directly rather than integrating a
            # velocity input.  Feedforward wrench is zero for standard teleop;
            # populate it to bias the controller during contact tasks.
            msg = MotionUpdate()
            msg.header.stamp    = self.get_clock().now().to_msg()
            msg.header.frame_id = 'base_link'

            msg.pose.position.x    = float(p_tgt[0])
            msg.pose.position.y    = float(p_tgt[1])
            msg.pose.position.z    = float(p_tgt[2])
            msg.pose.orientation.x = float(q_tgt[0])
            msg.pose.orientation.y = float(q_tgt[1])
            msg.pose.orientation.z = float(q_tgt[2])
            msg.pose.orientation.w = float(q_tgt[3])

            msg.target_stiffness = stiffness
            msg.target_damping   = damping

            msg.feedforward_wrench_at_tip.force.x  = 0.0
            msg.feedforward_wrench_at_tip.force.y  = 0.0
            msg.feedforward_wrench_at_tip.force.z  = 0.0
            msg.feedforward_wrench_at_tip.torque.x = 0.0
            msg.feedforward_wrench_at_tip.torque.y = 0.0
            msg.feedforward_wrench_at_tip.torque.z = 0.0
            msg.wrench_feedback_gains_at_tip = [0.0] * 6

            msg.trajectory_generation_mode.mode = 2

            self.pose_pub.publish(msg)
            self.last_cmd_p = p_tgt
            self.last_cmd_q = q_tgt

        except Exception:
            # TF lookup failures are expected transiently at startup and when
            # the oculus_reader node is not yet publishing transforms.
            return


def main(args=None):
    rclpy.init(args=args)
    node = OculusTFToAICController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
