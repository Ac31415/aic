#!/usr/bin/env python3
"""
AIC Oculus Teleop — LeRobot Teleoperator
========================================

Streams Cartesian velocity commands from an Oculus Quest right controller
to the AIC UR5e impedance controller, exposed as a LeRobot
``Teleoperator`` so ``lerobot-record`` can call ``get_action()`` each step,
record the action to the dataset, and dispatch it via ``send_action()``.

Design
------
Each tick runs a pose-based pipeline to compute an absolute TCP target:

    VR wrist delta  (+ analogue stick nudges)
        │
        ├─ axis remap     (X_r = Y_c, Y_r = X_c, Z_r = −Z_c)
        ├─ sphere clamp   (max displacement from capture)
        ├─ per-tick step cap
        ├─ orientation-off override
        ├─ workspace box clamp
        └─ first-order low-pass filter
        ↓
    absolute TCP target  (p_tgt, q_tgt)

The action emitted to lerobot-record depends on ``cartesian_command_mode``:

    velocity  (default)
        The target is differentiated tick-to-tick:
            v  = (p_tgt_new − p_tgt_old) / dt
            ω  = rotvec(q_tgt_new ⊗ q_tgt_old⁻¹) / dt
        The robot receives MODE_VELOCITY; closed-loop impedance control
        tracks the rate command.

    position
        The target pose is emitted directly.  The robot receives
        MODE_POSITION; the controller tracks the absolute pose.  The
        dataset records the full pose trajectory, which is typically
        richer supervision for policy learning than velocity.

Because both modes derive from the same clamped + filtered target, every
safety layer takes effect before anything reaches the robot, regardless
of mode.  The robot-side ``AICRobotAICControllerConfig.cartesian_command_mode``
must match the teleop's — a mismatch will cause a schema error at record
time.

Usage with lerobot-record
-------------------------
Place this file inside the ``lerobot_robot_aic`` package and export the
classes from ``__init__.py``::

    from .aic_oculus_teleop import AICOculusTeleop, AICOculusTeleopConfig

Record with::

    pixi run lerobot-record \
        --robot.type=aic_controller --robot.id=aic \
        --teleop.type=aic_oculus   --teleop.id=aic \
        --robot.teleop_target_mode=cartesian \
        --robot.cartesian_command_mode=position \
        --teleop.cartesian_command_mode=position \
        --robot.teleop_frame_id=base_link \
        --dataset.repo_id=<hf-user>/<dataset-name> \
        --dataset.single_task="insert cable" \
        --dataset.push_to_hub=false \
        --play_sounds=false \
        --display_data=true

Standalone
----------
Running the module directly (``python -m aic_oculus_teleop``) drives the
robot without the lerobot-record stack by publishing MotionUpdate messages
at the nominal rate — useful for smoke-testing the teleop pipeline on
its own.  The publish path follows the config's ``cartesian_command_mode``
(velocity → MODE_VELOCITY, position → MODE_POSITION).

Action schema
-------------
``get_action()`` returns a ``MotionUpdateActionDict`` + gripper::

    {
        "linear.x":  float,   # m/s in base_link X
        "linear.y":  float,   # m/s in base_link Y
        "linear.z":  float,   # m/s in base_link Z
        "angular.x": float,   # rad/s about base_link X
        "angular.y": float,   # rad/s about base_link Y
        "angular.z": float,   # rad/s about base_link Z
        "gripper":   float,   # 0.0 = open, 1.0 = closed
    }

Controls
--------
Keyboard:
  e  Enable VR tracking (captures reference)
  q  Disable VR tracking (zero velocity → robot holds pose)
  o  Toggle orientation follow
  t  Re-tare F/T sensor
  g  Toggle gripper open/closed
  f  Toggle force-feedback stiffness (standalone only — the lerobot-record
     action dict doesn't carry stiffness)
  l  Toggle workspace box limits
  x  Exit (raises SIGINT so both standalone and lerobot-record end cleanly)

Right Oculus controller:
  A                  cycle mode: IDLE → VR TRACKING → ANALOGUE → IDLE
  B                  toggle orientation follow
  RJ (stick click)   toggle analogue frame (base_link ↔ TCP)
  stick              yaw (X) + Z translation (Y)
  grip + stick       XY translation
  trigger + stick    pitch (X) + roll (Y)
"""

from __future__ import annotations

# Remove this file's directory from sys.path so the package's local
# ``types.py`` (if present) doesn't shadow the stdlib ``types`` module.
import os as _os
import sys as _sys
_here = _os.path.dirname(_os.path.abspath(__file__))
if _here in _sys.path:
    _sys.path.remove(_here)

import atexit
import math
import shutil
import signal
import sys
import termios
import threading
import time
import tty
import select
from dataclasses import dataclass
from typing import Any

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.duration import Duration
from rclpy.qos import QoSProfile, ReliabilityPolicy

from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState, Joy
from tf2_ros import Buffer, TransformListener

from aic_control_interfaces.msg import ControllerState
from aic_control_interfaces.srv import ChangeTargetMode
from std_srvs.srv import Trigger


# ----------------------------------------------------------------------------
# Lazy lerobot base-class imports.  When imported via lerobot-record (normal
# use) the real classes are available.  When run standalone, the stubs allow
# class definition to succeed without a lerobot install.
# ----------------------------------------------------------------------------

def _get_lerobot_bases():
    try:
        from lerobot.teleoperators import Teleoperator, TeleoperatorConfig  # noqa: PLC0415
        return Teleoperator, TeleoperatorConfig
    except (ImportError, Exception):
        class _TeleopStub:
            def __init_subclass__(cls, **kw): pass
            def __init__(self, config=None): pass
            @classmethod
            def register_subclass(cls, name):
                def _d(c): return c
                return _d
        class _CfgStub(_TeleopStub):
            pass
        return _TeleopStub, _CfgStub

_Teleoperator, _TeleoperatorConfig = _get_lerobot_bases()


def _get_lerobot_errors():
    try:
        from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError  # noqa: PLC0415
        return DeviceAlreadyConnectedError, DeviceNotConnectedError
    except (ImportError, Exception):
        return RuntimeError, RuntimeError


# ----------------------------------------------------------------------------
# Action schema.  The real lerobot_robot_aic.types uses dotted keys
# ('linear.x', etc.) so the functional TypedDict syntax is used in the
# fallback to preserve them; ordinary class-style TypedDict would require
# valid Python identifiers.
# ----------------------------------------------------------------------------

try:
    from lerobot_robot_aic.types import (
        MotionUpdateActionDict,
        PoseMotionUpdateActionDict,
    )
except (ImportError, Exception):
    from typing import TypedDict
    MotionUpdateActionDict = TypedDict('MotionUpdateActionDict', {
        'linear.x':  float, 'linear.y':  float, 'linear.z':  float,
        'angular.x': float, 'angular.y': float, 'angular.z': float,
    })
    PoseMotionUpdateActionDict = TypedDict('PoseMotionUpdateActionDict', {
        'pose.position.x': float,
        'pose.position.y': float,
        'pose.position.z': float,
        'pose.orientation.x': float,
        'pose.orientation.y': float,
        'pose.orientation.z': float,
        'pose.orientation.w': float,
    })


# =============================================================================
#  Quaternion / rigid-body transform helpers
# =============================================================================
# All quaternions are (x, y, z, w) tuples.  Poses are (p, q) pairs where p is
# a 3-tuple of metres and q is a unit quaternion.

def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _quat_norm(q):
    x, y, z, w = q
    n = math.sqrt(x*x + y*y + z*z + w*w)
    if n < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    return (x/n, y/n, z/n, w/n)


def _quat_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz,
    )


def _quat_inv(q):
    x, y, z, w = q
    return (-x, -y, -z, w)


def _rotate_vec(v, q):
    vx, vy, vz = v
    qv = (vx, vy, vz, 0.0)
    qi = _quat_inv(q)
    r = _quat_mul(_quat_mul(q, qv), qi)
    return (r[0], r[1], r[2])


def _tf_to_pose(tf):
    t = tf.transform.translation
    r = tf.transform.rotation
    return (t.x, t.y, t.z), _quat_norm((r.x, r.y, r.z, r.w))


def _pose_inv(p, q):
    qi = _quat_inv(q)
    pr = _rotate_vec(p, qi)
    return (-pr[0], -pr[1], -pr[2]), qi


def _pose_mul(p1, q1, p2, q2):
    p2r = _rotate_vec(p2, q1)
    return (
        (p1[0] + p2r[0], p1[1] + p2r[1], p1[2] + p2r[2]),
        _quat_norm(_quat_mul(q1, q2)),
    )


def _quat_from_axis_angle(ax, ay, az, angle):
    s = math.sin(angle * 0.5)
    return _quat_norm((ax * s, ay * s, az * s, math.cos(angle * 0.5)))


def _quat_to_rotvec(q):
    """
    Convert a unit quaternion to a rotation vector (axis * angle, radians).
    Picks the shorter arc so small rotations map to small vectors regardless
    of the quaternion's double-cover sign.
    """
    x, y, z, w = q
    if w < 0.0:
        x, y, z, w = -x, -y, -z, -w
    w = _clamp(w, -1.0, 1.0)
    angle = 2.0 * math.acos(w)
    s = math.sqrt(max(0.0, 1.0 - w*w))
    if s < 1e-10:
        return (0.0, 0.0, 0.0)
    return (x / s * angle, y / s * angle, z / s * angle)


def _stick_ramp(v, deadzone, exponent=1.5):
    """
    Dead zone + power-law ramp on an analogue stick axis.  Returns a value in
    [-1, 1]: zero for |v| < deadzone, smooth growth to ±1 at full deflection;
    exponent > 1 compresses small deflections for finer near-centre control.
    """
    if abs(v) < deadzone:
        return 0.0
    sign = 1.0 if v > 0.0 else -1.0
    n = (abs(v) - deadzone) / (1.0 - deadzone)
    return sign * (n ** exponent)


# =============================================================================
#  Non-blocking keyboard listener
# =============================================================================

class _KeyWatcher:
    """
    Daemon-thread keyboard listener.  Prints a confirmation on each key so
    the operator always sees that input registered.

    Keys
    ----
      e  Enable VR tracking  (captures wrist + TCP reference)
      q  Disable VR tracking (zero velocity out → robot holds pose)
      o  Toggle orientation follow
      t  Re-tare F/T sensor
      g  Toggle gripper open/closed
      f  Toggle force-feedback stiffness (standalone main() only)
      l  Toggle workspace box limits
      x  Exit  (raises SIGINT so both standalone and lerobot-record shut down)
    """

    def __init__(self):
        self.enabled            = False
        self.exit               = False
        self.gripper_closed     = False
        self.gripper_toggled    = False   # edge flag cleared by snapshot()
        self.follow_ori_toggled = False   # edge flag
        self.tare_requested     = False   # edge flag
        self.force_feedback     = False
        self.limits_enabled     = True
        self._lock              = threading.Lock()
        self._thread            = threading.Thread(target=self._run, daemon=True)
        self._term_fd           = None
        self._term_old          = None
        self._restore_registered = False

    def start(self):
        with self._lock:
            # Allow reconnect cycles: after disconnect() sets exit=True, start()
            # must clear it and use a fresh Thread object.
            self.exit = False
            if self._thread.is_alive():
                return
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

        if not self._restore_registered:
            atexit.register(self._restore)
            self._restore_registered = True

    def _restore(self):
        """Restore terminal on exit so the shell isn't left in cbreak mode."""
        if self._term_fd is not None and self._term_old is not None:
            try:
                termios.tcsetattr(self._term_fd, termios.TCSADRAIN, self._term_old)
            except Exception:
                pass
            self._term_fd = self._term_old = None

    def set_enabled(self, val: bool):
        with self._lock:
            self.enabled = val

    def _run(self):
        # Skip entirely in non-TTY environments (piped subprocess, etc.).
        if not sys.stdin.isatty():
            return
        fd = sys.stdin.fileno()
        try:
            old = termios.tcgetattr(fd)
        except termios.error:
            return
        self._term_fd, self._term_old = fd, old
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
                        self.force_feedback = not self.force_feedback
                        print(f"\n[KEY] force_feedback = {self.force_feedback} (f)")
                    elif ch == 'l':
                        self.limits_enabled = not self.limits_enabled
                        state = "ON" if self.limits_enabled else "OFF  [limits suppressed]"
                        print(f"\n[KEY] workspace_limits = {state} (l)")
                    elif ch == 'x':
                        self.exit = True
                        print("\n[KEY] EXIT (x) -- shutting down")
                        # Raise SIGINT so both the standalone main() loop
                        # AND lerobot-record's record_loop shut down cleanly.
                        # Python delivers signals to the main thread, so
                        # this safely interrupts the loop wherever it is.
                        try:
                            signal.raise_signal(signal.SIGINT)
                        except Exception:
                            pass
                        return
        finally:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except Exception:
                pass
            self._term_fd = self._term_old = None

    def snapshot(self):
        """Return a dict of current state and reset edge-triggered flags."""
        with self._lock:
            gt = self.gripper_toggled
            ot = self.follow_ori_toggled
            tr = self.tare_requested
            self.gripper_toggled = self.follow_ori_toggled = self.tare_requested = False
            return dict(
                enabled         = self.enabled,
                exit            = self.exit,
                gripper_closed  = self.gripper_closed,
                gripper_toggled = gt,
                follow_ori_tog  = ot,
                tare_requested  = tr,
                force_feedback  = self.force_feedback,
                limits_enabled  = self.limits_enabled,
            )


# =============================================================================
#  Impedance parameter presets
# =============================================================================
# The AIC impedance controller accepts per-command 6x6 stiffness and damping
# matrices as flat float64[36] arrays (row-major).  Only the standalone main()
# uses these: the lerobot-record action dict carries velocities only.

def _diag6x6(v):
    m = [0.0] * 36
    for i in range(6):
        m[i * 6 + i] = v
    return m


DEFAULT_STIFFNESS   = _diag6x6(85.0)
DEFAULT_DAMPING     = _diag6x6(75.0)
TELEOP_STIFFNESS    = _diag6x6(60.0)
TELEOP_DAMPING      = _diag6x6(50.0)
INSERTION_STIFFNESS = _diag6x6(30.0)
INSERTION_DAMPING   = _diag6x6(25.0)


# =============================================================================
#  Config
# =============================================================================

@_TeleoperatorConfig.register_subclass("aic_oculus")
@dataclass(kw_only=True)
class AICOculusTeleopConfig(_TeleoperatorConfig):
    # TF frames
    base_frame: str = "base_link"
    ctrl_frame: str = "oculus_r"
    tcp_frame:  str = "gripper/tcp"

    # Cartesian command emission mode:
    #   "velocity"  emit 6-DOF velocity (MODE_VELOCITY on the robot side).
    #               Target pose is differentiated each tick.
    #   "position"  emit the absolute target pose (MODE_POSITION).  Records
    #               the full pose trajectory into the dataset, which is
    #               typically richer for policy learning.
    # The robot-side config must match — see AICRobotAICControllerConfig.
    cartesian_command_mode: str = "velocity"

    # Output velocity safety clamps.  The target-pose pipeline (step cap,
    # LPF, sphere, workspace) is the primary safety layer — these are final
    # defense in depth applied after differentiation.
    max_linear_speed:  float = 0.60      # m/s ceiling
    max_angular_speed: float = 2.0       # rad/s ceiling
    min_dt:            float = 5.0e-3    # s — floor on dt to prevent 1/dt blow-up

    # Target-pose safety parameters.  max_step_xyz is defined per-tick at
    # nominal_rate_hz; it gets scaled by dt at runtime so the effective
    # speed ceiling (~0.60 m/s) is rate-independent if lerobot-record calls
    # get_action at a different rate.
    max_step_xyz:      float = 0.020     # m per tick at nominal rate
    nominal_rate_hz:   float = 30.0      # reference rate for scaling
    max_total_offset:  float = 0.35      # m — sphere clamp from capture
    pos_lpf_alpha:     float = 0.55      # first-order LPF on target position

    # Workspace box (base_link, metres).  Master switch is OFF by default;
    # flip to True here to enable, then 'l' gates it at runtime.
    limit_x: tuple[float, float] = (-0.65, -0.15)
    limit_y: tuple[float, float] = (-0.45,  0.45)
    limit_z: tuple[float, float] = ( 0.05,  0.50)
    enable_workspace_limits: bool = False

    # Analogue stick — per-second rates at full deflection, so feel is
    # rate-independent.  Translation speeds are the fine-control nudges
    # applied on top of (or instead of) VR tracking; angular speeds match.
    stick_xy_speed:    float = 0.080     # m/s at full deflection (XY nudge)
    stick_z_speed:     float = 0.040     # m/s at full deflection (Z nudge)
    stick_yaw_speed:   float = 0.150     # rad/s at full deflection
    stick_pitch_speed: float = 0.075     # rad/s at full deflection
    stick_roll_speed:  float = 0.075     # rad/s at full deflection
    stick_deadzone:    float = 0.15
    stick_ramp_exp:    float = 2.0
    stick_mod_thresh:  float = 0.30

    # Force-feedback stiffness interpolation band (N).  Used only by the
    # standalone main()'s MotionUpdate publisher — the lerobot-record
    # action dict doesn't carry stiffness.
    force_lo: float = 2.0
    force_hi: float = 20.0

    # Terminal HUD.  Skipped automatically if stdout isn't a TTY, so
    # lerobot-record subprocess output isn't clobbered.
    enable_hud: bool = True

    # Whether this teleop should open a local stdin keyboard watcher.
    # Keep this OFF by default so lerobot-record's own keyboard listener
    # (right/left arrows + esc for episode/reset flow) remains the sole
    # owner of keyboard control, matching aic_keyboard_ee behavior.
    #
    # When running this module standalone, main() enables it explicitly.
    enable_local_keyboard_controls: bool = False


# =============================================================================
#  AICOculusTeleop — LeRobot Teleoperator streaming Cartesian velocity
# =============================================================================

#
# Note: the Teleoperator class itself is NOT decorated with register_subclass.
# On the real lerobot base class that method only exists on TeleoperatorConfig
# (draccus uses it to resolve `--teleop.type=...` to the config class).  The
# Teleoperator implementation is discovered via `config_class` on the config.

class AICOculusTeleop(_Teleoperator):
    """
    LeRobot Teleoperator driving the AIC UR5e via Oculus Quest VR.

    ``get_action()`` runs an absolute-pose pipeline each tick (VR delta +
    stick nudges + sphere clamp + step cap + workspace box + LPF) and
    emits the result as either a velocity action (target differentiated
    tick-to-tick) or a position action (target emitted directly),
    depending on ``cartesian_command_mode``.
    """

    config_class = AICOculusTeleopConfig
    name = "aic_oculus"

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self, config: AICOculusTeleopConfig):
        super().__init__(config)
        self.config = config

        if self.config.cartesian_command_mode not in ("velocity", "position"):
            raise ValueError(
                f"Invalid cartesian_command_mode: "
                f"{self.config.cartesian_command_mode!r}. "
                "Supported modes are 'velocity' and 'position'."
            )

        self._is_connected = False

        # ROS 2 runtime (created in connect())
        self._node        = None
        self._tf_buffer   = None
        self._executor    = None
        self._exec_thread = None
        self._gripper_pub = None
        self._switch_cli  = None
        self._tare_cli    = None

        # VR reference transforms (captured on 'e' / A-button)
        self._have_ref      = False
        self._p_base_ctrl0  = None
        self._q_base_ctrl0  = None
        self._p_base_tcp0   = None
        self._q_base_tcp0   = None

        # Last commanded target pose.  Seeded by _capture_reference() to the
        # current TCP pose; updated every tick to the target we just emitted.
        # Used for step cap, velocity differentiation, and analogue-only mode.
        self._last_cmd_p = None
        self._last_cmd_q = None

        # First-order LPF state on target position
        self._p_tgt_filt = None

        # Monotonic timestamp of the last tick (for dt)
        self._last_t = None

        # Orientation follow toggle (keyboard 'o' / controller B)
        self._follow_ori = False

        # Analogue stick state
        self._analogue_enabled = False
        self._analogue_frame   = 'base'   # 'base' | 'tcp'
        self._analogue_ref_p   = None     # captured on entry to analogue mode
        self._analogue_ref_q   = None
        self._joy_btn_a_prev   = False
        self._joy_btn_b_prev   = False
        self._joy_btn_rj_prev  = False
        self._latest_joy       = None

        # Accumulated stick offsets (persistent; zeroed on reference
        # capture or on A-button entry to analogue mode).
        self._stick_p_offset = [0.0, 0.0, 0.0]
        self._stick_q_offset = (0.0, 0.0, 0.0, 1.0)

        # F/T state
        self._latest_wrench = None
        self._ft_bias       = (0.0, 0.0, 0.0)
        self._latest_ctrl   = None

        # Gripper state (returned as extra key in action dict)
        self._gripper_closed = False

        # Keyboard watcher
        self._keys = _KeyWatcher()

        # HUD shadows
        self._hud_limits_active = True

    # ------------------------------------------------------------------

    def connect(self, calibrate: bool = True) -> None:
        DeviceAlreadyConnectedError, _ = _get_lerobot_errors()
        if self._is_connected:
            raise DeviceAlreadyConnectedError()

        if not rclpy.ok():
            rclpy.init()

        self._node = rclpy.create_node("aic_oculus_teleop")

        # TF listener
        self._tf_buffer = Buffer()
        TransformListener(self._tf_buffer, self._node)

        # Subscribers
        self._node.create_subscription(
            Joy, '/oculus/right/joy', self._joy_cb, 10)
        self._node.create_subscription(
            WrenchStamped, '/fts_broadcaster/wrench', self._ft_cb, 10)
        self._node.create_subscription(
            ControllerState, '/aic_controller/controller_state', self._ctrl_cb, 10)

        # Gripper publisher
        self._gripper_pub = self._node.create_publisher(
            JointState, '/gripper_commands', QoSProfile(depth=10))

        # Long-lived service clients
        self._switch_cli = self._node.create_client(
            ChangeTargetMode, '/aic_controller/change_target_mode')
        self._tare_cli = self._node.create_client(
            Trigger, '/aic_controller/tare_force_torque_sensor')

        # Spin in background so callbacks run continuously
        self._executor = SingleThreadedExecutor()
        self._executor.add_node(self._node)
        self._exec_thread = threading.Thread(
            target=self._executor.spin, daemon=True)
        self._exec_thread.start()

        # Let TF and subscribers populate before we tare
        time.sleep(1.0)

        # Switch the AIC controller to Cartesian target mode
        self._set_cartesian_mode()

        # Hardware + software F/T tare
        self._tare_ft()

        # Optional local keyboard watcher.  Disabled by default in
        # lerobot-record to avoid competing with its episode-control
        # keyboard listener.
        if self.config.enable_local_keyboard_controls:
            self._keys.start()

        self._is_connected = True

        print("\n[aic_oculus] Connected.")
        if self.config.enable_local_keyboard_controls:
            print("Keyboard:")
            print("  e  enable VR tracking   q  disable")
            print("  o  orientation follow   t  re-tare F/T")
            print("  g  gripper              f  force-feedback (standalone only)")
            print("  l  workspace limits     x  exit")
        else:
            print("Keyboard:")
            print("  local keyboard controls disabled (use controller buttons)")
        print("Right controller:")
        print("  A              cycle: IDLE → VR → ANALOGUE → IDLE")
        print("  B              toggle orientation follow")
        print("  RJ (click)     toggle analogue frame (base ↔ TCP)")
        print("  stick          yaw (X) + Z (Y)")
        print("  grip + stick   XY translation")
        print("  trigger+stick  pitch (X) + roll (Y)\n")

    def disconnect(self) -> None:
        _, DeviceNotConnectedError = _get_lerobot_errors()
        if not self._is_connected:
            raise DeviceNotConnectedError()
        # Signal the key thread to exit and restore the terminal.  Don't
        # shutdown rclpy — other nodes (e.g. the robot adapter in
        # lerobot-record) may still be using the default context.
        try:
            self._keys.exit = True
            self._keys._restore()
        except Exception:
            pass
        if self._executor is not None:
            try:
                self._executor.shutdown(timeout_sec=1.0)
            except Exception:
                pass
        if self._node is not None:
            try:
                self._node.destroy_node()
            except Exception:
                pass
        self._is_connected = False

    # ------------------------------------------------------------------
    # LeRobot protocol
    # ------------------------------------------------------------------

    @property
    def action_features(self) -> dict:
        """Schema of the action returned by get_action()."""
        if self.config.cartesian_command_mode == "position":
            base_features = PoseMotionUpdateActionDict.__annotations__
        else:
            base_features = MotionUpdateActionDict.__annotations__
        return {
            **base_features,
            "gripper": float,
        }

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    # ------------------------------------------------------------------
    # Abstract methods required by lerobot.teleoperators.Teleoperator
    # but not meaningful for VR-style pose teleop.
    # ------------------------------------------------------------------

    @property
    def is_calibrated(self) -> bool:
        """
        VR teleop has no persistent calibration — the operator captures a
        fresh wrist + TCP reference every time they press 'e'.  Report
        calibrated so lerobot-record doesn't try to run a calibration flow.
        """
        return True

    def calibrate(self) -> None:
        """No-op: reference pose is captured at enable time, not here."""
        return

    def configure(self) -> None:
        """No-op: all setup already happened in connect()."""
        return

    @property
    def feedback_features(self) -> dict:
        """No haptic / force feedback channel exposed to the operator."""
        return {}

    def send_feedback(self, feedback) -> None:
        """No-op: the Oculus controllers aren't wired for feedback here."""
        return

    # ------------------------------------------------------------------
    # The main tick  — runs the absolute target-pose pipeline, then
    # differentiates the target into a velocity action.
    # ------------------------------------------------------------------

    def get_action(self) -> dict[str, Any]:
        _, DeviceNotConnectedError = _get_lerobot_errors()
        if not self._is_connected:
            raise DeviceNotConnectedError()

        # ── Timing ──────────────────────────────────────────────────────
        now = time.monotonic()
        if self._last_t is None:
            dt = 1.0 / self.config.nominal_rate_hz
        else:
            dt = now - self._last_t
        dt = max(dt, self.config.min_dt)

        # ── Key + edge events ───────────────────────────────────────────
        snap = self._keys.snapshot()

        if snap['follow_ori_tog']:
            self._follow_ori = not self._follow_ori
            print(f"[aic_oculus] orientation follow -> "
                  f"{'ON' if self._follow_ori else 'OFF'}  [o]")

        if snap['tare_requested']:
            self._tare_ft()

        if snap['gripper_toggled']:
            self._gripper_closed = snap['gripper_closed']
            self._send_gripper_command(self._gripper_closed)

        # The KeyWatcher.enabled flag may also be toggled by the controller
        # A button via _joy_cb — read it fresh from the watcher, not snap.
        enabled         = self._keys.enabled
        limits_enabled  = snap['limits_enabled']
        self._hud_limits_active = limits_enabled

        if self.config.enable_hud:
            self._render_hud()

        # ── Idle action template ───────────────────────────────────────
        # In velocity mode this is zero-velocity; in position mode it's
        # the current TCP pose (so a "no input" tick holds the robot at
        # wherever it is rather than snapping to the origin).
        action = self._make_idle_action()

        # Fast-exit if 'x' was pressed — emit the idle action and let the
        # standalone main() loop see the flag and break.
        if snap['exit']:
            self._last_t = now
            return action

        # --------------------------------------------------------------
        # Analogue-only mode: VR is off but the stick is active.  Run
        # the analogue reference through the stick nudge, clamp, and
        # diff — produces a velocity action every tick so the controller
        # keeps receiving a fresh target even when VR is off.
        # --------------------------------------------------------------
        if not enabled:
            self._have_ref = False
            self._p_tgt_filt = None   # clean LPF restart on next VR enable

            if self._analogue_enabled and self._analogue_ref_p is not None:
                try:
                    p_tgt, q_tgt = self._apply_stick_nudge(
                        tuple(self._analogue_ref_p), self._analogue_ref_q, dt)

                    if self.config.enable_workspace_limits and limits_enabled:
                        p_tgt = self._clamp_box(p_tgt)

                    self._write_cartesian_action(action, p_tgt, q_tgt, dt)
                except Exception as e:
                    _sys.stderr.write(f"\n[aic_oculus] analogue tick error: {e!r}\n")
            # else: idle — emit the idle template, don't advance last_cmd_*.

            self._last_t = now
            return action

        # --------------------------------------------------------------
        # VR tracking enabled
        # --------------------------------------------------------------
        try:
            # Capture reference on first tick after enable (or after
            # controller A button re-entry).  Emit zero velocity that tick.
            if not self._have_ref:
                self._capture_reference()
                self._last_t = now
                return action

            # ── Step 1: controller delta since capture ──────────────────
            p_base_ctrl, q_base_ctrl = self._lookup_pose(
                self.config.base_frame, self.config.ctrl_frame)

            p0i, q0i = _pose_inv(self._p_base_ctrl0, self._q_base_ctrl0)
            p_delta, q_delta = _pose_mul(p0i, q0i, p_base_ctrl, q_base_ctrl)

            # ── Step 2: remap controller axes to base_link ──────────────
            #   X_r =  Y_c,  Y_r =  X_c,  Z_r = -Z_c
            p_delta_mapped = (p_delta[1], p_delta[0], -p_delta[2])
            q_delta_mapped = (q_delta[1], q_delta[0], -q_delta[2], q_delta[3])

            # ── Step 3: apply delta to reference TCP pose ───────────────
            p_tgt = (
                self._p_base_tcp0[0] + p_delta_mapped[0],
                self._p_base_tcp0[1] + p_delta_mapped[1],
                self._p_base_tcp0[2] + p_delta_mapped[2],
            )
            q_tgt = _quat_norm(_quat_mul(q_delta_mapped, self._q_base_tcp0))

            # ── Step 4: analogue stick offsets (if active) ──────────────
            if self._analogue_enabled:
                p_tgt, q_tgt = self._apply_stick_nudge(p_tgt, q_tgt, dt)

            # ── Step 5a: sphere clamp about capture reference ───────────
            dx = p_tgt[0] - self._p_base_tcp0[0]
            dy = p_tgt[1] - self._p_base_tcp0[1]
            dz = p_tgt[2] - self._p_base_tcp0[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist > self.config.max_total_offset:
                s = self.config.max_total_offset / max(1e-9, dist)
                p_tgt = (
                    self._p_base_tcp0[0] + dx * s,
                    self._p_base_tcp0[1] + dy * s,
                    self._p_base_tcp0[2] + dz * s,
                )

            # ── Step 5b: per-tick step cap on target ────────────────────
            # 0.020 m/tick tuning assumed the nominal rate; scaling by
            # dt × nominal_rate_hz preserves the effective ~0.60 m/s
            # ceiling when called at a different rate.
            step_cap = self.config.max_step_xyz * (dt * self.config.nominal_rate_hz)
            if self._last_cmd_p is not None:
                sx = _clamp(p_tgt[0] - self._last_cmd_p[0], -step_cap, step_cap)
                sy = _clamp(p_tgt[1] - self._last_cmd_p[1], -step_cap, step_cap)
                sz = _clamp(p_tgt[2] - self._last_cmd_p[2], -step_cap, step_cap)
                p_tgt = (
                    self._last_cmd_p[0] + sx,
                    self._last_cmd_p[1] + sy,
                    self._last_cmd_p[2] + sz,
                )

            # ── Step 5c: orientation-off override ──────────────────────
            if not self._follow_ori:
                q_tgt = self._q_base_tcp0

            # ── Step 5d: workspace box clamp ───────────────────────────
            if self.config.enable_workspace_limits and limits_enabled:
                p_tgt = self._clamp_box(p_tgt)

            # ── Step 6: first-order LPF on target position ─────────────
            if self._p_tgt_filt is None:
                self._p_tgt_filt = p_tgt
            else:
                a = self.config.pos_lpf_alpha
                self._p_tgt_filt = (
                    a * p_tgt[0] + (1.0 - a) * self._p_tgt_filt[0],
                    a * p_tgt[1] + (1.0 - a) * self._p_tgt_filt[1],
                    a * p_tgt[2] + (1.0 - a) * self._p_tgt_filt[2],
                )
            p_tgt = self._p_tgt_filt

            # ── Step 7: emit Cartesian action in the configured mode ────
            self._write_cartesian_action(action, p_tgt, q_tgt, dt)

        except Exception as e:
            # TF lookup transiently fails during startup — emit the idle
            # action and keep the loop alive.  Log other exceptions to
            # stderr so they surface during recording.
            _sys.stderr.write(f"\n[aic_oculus] tick exception: {e!r}\n")

        self._last_t = now
        return action

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Cartesian action emission.  _write_cartesian_action dispatches to
    # the mode-specific writer; _make_idle_action builds a "no input"
    # action (zero velocity, or current-pose hold).
    # ------------------------------------------------------------------

    def _write_cartesian_action(self, action, p_tgt, q_tgt, dt):
        if self.config.cartesian_command_mode == "position":
            self._write_position_action(action, p_tgt, q_tgt)
        else:
            self._write_velocity_action(action, p_tgt, q_tgt, dt)

    def _current_tcp_pose_for_idle(self):
        """
        Best-effort "where is the TCP right now?" for building an idle
        position-mode action.  Tries, in order: the latest controller
        state, the last commanded target, the VR reference pose,
        finally the identity as a last resort.
        """
        if self._latest_ctrl is not None:
            try:
                pose = self._latest_ctrl.tcp_pose
                return (
                    (pose.position.x, pose.position.y, pose.position.z),
                    (pose.orientation.x, pose.orientation.y,
                     pose.orientation.z, pose.orientation.w),
                )
            except AttributeError:
                pass
        if self._last_cmd_p is not None and self._last_cmd_q is not None:
            return self._last_cmd_p, self._last_cmd_q
        if self._p_base_tcp0 is not None and self._q_base_tcp0 is not None:
            return self._p_base_tcp0, self._q_base_tcp0
        return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)

    def _make_idle_action(self) -> dict[str, Any]:
        """
        Action template for "no operator input this tick".

        Velocity mode: six zeros.  The robot holds pose under impedance
        control because zero commanded velocity.

        Position mode: current TCP pose.  A constant pose is interpreted
        by the controller as "hold here", so the robot doesn't move on
        idle ticks — critical because position mode doesn't have an
        obvious "zero action" representation.
        """
        if self.config.cartesian_command_mode == "position":
            p_ref, q_ref = self._current_tcp_pose_for_idle()
            return {
                "pose.position.x": float(p_ref[0]),
                "pose.position.y": float(p_ref[1]),
                "pose.position.z": float(p_ref[2]),
                "pose.orientation.x": float(q_ref[0]),
                "pose.orientation.y": float(q_ref[1]),
                "pose.orientation.z": float(q_ref[2]),
                "pose.orientation.w": float(q_ref[3]),
                "gripper": 1.0 if self._gripper_closed else 0.0,
            }

        return {
            "linear.x":  0.0, "linear.y":  0.0, "linear.z":  0.0,
            "angular.x": 0.0, "angular.y": 0.0, "angular.z": 0.0,
            "gripper":   1.0 if self._gripper_closed else 0.0,
        }

    # ------------------------------------------------------------------
    # Velocity writer — differentiates target pose and updates last_cmd_*
    # so that the integral of the emitted velocity reproduces the target.
    # ------------------------------------------------------------------

    def _write_velocity_action(self, action, p_tgt, q_tgt, dt):
        if self._last_cmd_p is None or self._last_cmd_q is None:
            # First tick of a new session — seed last_cmd_* and publish zero.
            self._last_cmd_p = p_tgt
            self._last_cmd_q = q_tgt
            return

        vmax = self.config.max_linear_speed
        wmax = self.config.max_angular_speed

        vx = _clamp((p_tgt[0] - self._last_cmd_p[0]) / dt, -vmax, vmax)
        vy = _clamp((p_tgt[1] - self._last_cmd_p[1]) / dt, -vmax, vmax)
        vz = _clamp((p_tgt[2] - self._last_cmd_p[2]) / dt, -vmax, vmax)

        # q_tgt = q_delta ⊗ q_last  =>  q_delta = q_tgt ⊗ q_last⁻¹
        q_delta = _quat_norm(_quat_mul(q_tgt, _quat_inv(self._last_cmd_q)))
        rv = _quat_to_rotvec(q_delta)
        wx = _clamp(rv[0] / dt, -wmax, wmax)
        wy = _clamp(rv[1] / dt, -wmax, wmax)
        wz = _clamp(rv[2] / dt, -wmax, wmax)

        action["linear.x"]  = vx
        action["linear.y"]  = vy
        action["linear.z"]  = vz
        action["angular.x"] = wx
        action["angular.y"] = wy
        action["angular.z"] = wz

        self._last_cmd_p = p_tgt
        self._last_cmd_q = q_tgt

    # ------------------------------------------------------------------
    # Position writer — emits the absolute TCP target directly.  The
    # target pose is already fully clamped + filtered by the pipeline
    # that produced it, so no additional safety clamp is applied here.
    # ------------------------------------------------------------------

    def _write_position_action(self, action, p_tgt, q_tgt):
        action["pose.position.x"]    = float(p_tgt[0])
        action["pose.position.y"]    = float(p_tgt[1])
        action["pose.position.z"]    = float(p_tgt[2])
        action["pose.orientation.x"] = float(q_tgt[0])
        action["pose.orientation.y"] = float(q_tgt[1])
        action["pose.orientation.z"] = float(q_tgt[2])
        action["pose.orientation.w"] = float(q_tgt[3])

        self._last_cmd_p = p_tgt
        self._last_cmd_q = q_tgt

    def _clamp_box(self, p):
        return (
            _clamp(p[0], self.config.limit_x[0], self.config.limit_x[1]),
            _clamp(p[1], self.config.limit_y[0], self.config.limit_y[1]),
            _clamp(p[2], self.config.limit_z[0], self.config.limit_z[1]),
        )

    # ------------------------------------------------------------------
    # Reference capture
    # ------------------------------------------------------------------

    def _capture_reference(self):
        """
        Snapshot the current controller and TCP poses as the VR reference.
        Called on the first tick after 'e' / A-button re-enable.  Zeroes
        stick offsets and the LPF so stale state doesn't leak in.
        """
        tf_bc = self._lookup_tf(self.config.base_frame, self.config.ctrl_frame)
        tf_bt = self._lookup_tf(self.config.base_frame, self.config.tcp_frame)
        self._p_base_ctrl0, self._q_base_ctrl0 = _tf_to_pose(tf_bc)
        self._p_base_tcp0,  self._q_base_tcp0  = _tf_to_pose(tf_bt)
        self._have_ref     = True
        self._last_cmd_p   = self._p_base_tcp0
        self._last_cmd_q   = self._q_base_tcp0
        self._p_tgt_filt   = None
        self._stick_p_offset = [0.0, 0.0, 0.0]
        self._stick_q_offset = (0.0, 0.0, 0.0, 1.0)
        print("[aic_oculus] Reference captured: controller + TCP poses recorded.")

    def _lookup_tf(self, target, source):
        return self._tf_buffer.lookup_transform(
            target, source, rclpy.time.Time(),
            timeout=Duration(seconds=0.05))

    def _lookup_pose(self, target, source):
        return _tf_to_pose(self._lookup_tf(target, source))

    # ------------------------------------------------------------------
    # ROS 2 callbacks
    # ------------------------------------------------------------------

    def _joy_cb(self, msg: Joy):
        def _btn(i):
            return bool(msg.buttons[i]) if len(msg.buttons) > i else False

        # Button A — cycle control mode (IDLE → VR → ANALOGUE → IDLE)
        a_now = _btn(0)
        if a_now and not self._joy_btn_a_prev:
            if not self._keys.enabled and not self._analogue_enabled:
                # IDLE → VR TRACKING
                self._keys.set_enabled(True)
                self._analogue_enabled = False
                self._have_ref = False   # reference captured next tick
                print("[aic_oculus] Mode -> VR TRACKING  [A]")
            elif self._keys.enabled and not self._analogue_enabled:
                # VR → ANALOGUE
                self._keys.set_enabled(False)
                self._analogue_enabled = True
                self._analogue_ref_p = list(self._last_cmd_p) \
                    if self._last_cmd_p is not None else None
                self._analogue_ref_q = self._last_cmd_q
                self._stick_p_offset = [0.0, 0.0, 0.0]
                self._stick_q_offset = (0.0, 0.0, 0.0, 1.0)
                print("[aic_oculus] Mode -> ANALOGUE  [A]")
            else:
                # ANALOGUE → IDLE
                self._keys.set_enabled(False)
                self._analogue_enabled = False
                print("[aic_oculus] Mode -> IDLE  [A]")
        self._joy_btn_a_prev = a_now

        # Button B — toggle orientation follow
        b_now = _btn(1)
        if b_now and not self._joy_btn_b_prev:
            self._follow_ori = not self._follow_ori
            print(f"[aic_oculus] Orientation follow -> "
                  f"{'ON' if self._follow_ori else 'OFF'}  [B]")
        self._joy_btn_b_prev = b_now

        # Button RJ (joystick click) — toggle analogue command frame
        rj_now = _btn(2)
        if rj_now and not self._joy_btn_rj_prev:
            self._analogue_frame = 'tcp' if self._analogue_frame == 'base' else 'base'
            print(f"[aic_oculus] Analogue frame -> {self._analogue_frame}  [RJ]")
        self._joy_btn_rj_prev = rj_now

        self._latest_joy = msg

    def _ft_cb(self, msg: WrenchStamped):
        self._latest_wrench = msg

    def _ctrl_cb(self, msg: ControllerState):
        self._latest_ctrl = msg

    # ------------------------------------------------------------------
    # Analogue stick  — accumulates pose offsets under operator control,
    # parameterised by dt so the per-second speeds in config translate to
    # rate-independent feel regardless of how often get_action() is called.
    # ------------------------------------------------------------------

    def _apply_stick_nudge(self, p_tgt, q_tgt, dt):
        """
        Apply accumulated analogue stick offsets to a pose and return the
        result.  Offsets are persistent — the robot holds its nudged
        position when the stick returns to centre.  They are zeroed when
        analogue mode is entered (Button A) or when the VR reference is
        re-captured ('e').

        Modes (right thumbstick):
          no modifier   -- yaw (stick X) + Z translation (stick Y)
          grip held     -- XY translation in the horizontal plane
          trigger held  -- pitch (stick X) + roll (stick Y)

        Frame ('base' | 'tcp'):
          'base'  deltas applied directly in base_link axes.
          'tcp'   deltas rotated into the current target orientation so
                  "forward" follows the gripper approach axis regardless
                  of wrist orientation.
        """
        if self._latest_joy is None:
            return (
                (p_tgt[0] + self._stick_p_offset[0],
                 p_tgt[1] + self._stick_p_offset[1],
                 p_tgt[2] + self._stick_p_offset[2]),
                _quat_norm(_quat_mul(self._stick_q_offset, q_tgt)),
            )

        axes = self._latest_joy.axes
        def _ax(i): return axes[i] if len(axes) > i else 0.0

        sx = _stick_ramp(_ax(0), self.config.stick_deadzone, self.config.stick_ramp_exp)
        sy = _stick_ramp(_ax(1), self.config.stick_deadzone, self.config.stick_ramp_exp)
        grip_held    = _ax(3) >= self.config.stick_mod_thresh
        trigger_held = _ax(2) >= self.config.stick_mod_thresh

        def _frame_axis(local_axis):
            if self._analogue_frame == 'tcp':
                return _rotate_vec(local_axis, q_tgt)
            return local_axis

        if grip_held:
            # XY translation.  Stick X is inverted so a left push maps to
            # robot +X (forward in the operator's frame) and a right push
            # to −X; this matches the "reach away / pull back" convention
            # most operators expect.
            dx = -sx * self.config.stick_xy_speed * dt
            dy =  sy * self.config.stick_xy_speed * dt
            local = _rotate_vec((dx, dy, 0.0), q_tgt) \
                if self._analogue_frame == 'tcp' else (dx, dy, 0.0)
            self._stick_p_offset[0] += local[0]
            self._stick_p_offset[1] += local[1]
            self._stick_p_offset[2] += local[2]

        elif trigger_held:
            # Pitch (stick X) + roll (stick Y).
            # Stick X sign convention: a right push rotates +pitch, a left
            # push rotates −pitch.  Stick Y is kept inverted (up = −roll).
            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 1.0, 0.0))
                dq = _quat_from_axis_angle(*axis, sx * self.config.stick_pitch_speed * dt)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))
            if abs(sy) > 0.0:
                axis = _frame_axis((1.0, 0.0, 0.0))
                dq = _quat_from_axis_angle(*axis, -sy * self.config.stick_roll_speed * dt)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))

        else:
            # Yaw + Z
            dz = sy * self.config.stick_z_speed * dt
            local_z = _rotate_vec((0.0, 0.0, dz), q_tgt) \
                if self._analogue_frame == 'tcp' else (0.0, 0.0, dz)
            self._stick_p_offset[0] += local_z[0]
            self._stick_p_offset[1] += local_z[1]
            self._stick_p_offset[2] += local_z[2]

            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 0.0, 1.0))
                dq = _quat_from_axis_angle(*axis, -sx * self.config.stick_yaw_speed * dt)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))

        p_out = (
            p_tgt[0] + self._stick_p_offset[0],
            p_tgt[1] + self._stick_p_offset[1],
            p_tgt[2] + self._stick_p_offset[2],
        )
        return p_out, _quat_norm(_quat_mul(self._stick_q_offset, q_tgt))

    # ------------------------------------------------------------------
    # Services  (Cartesian mode + F/T tare)
    # ------------------------------------------------------------------

    def _set_cartesian_mode(self):
        if self._switch_cli is None:
            return
        if not self._switch_cli.wait_for_service(timeout_sec=3.0):
            print("[aic_oculus] WARNING: change_target_mode service unavailable.")
            return
        try:
            from aic_control_interfaces.msg import TargetMode  # noqa: PLC0415
            mode_val = TargetMode.MODE_CARTESIAN
        except Exception:
            mode_val = 1  # documented value
        req = ChangeTargetMode.Request()
        req.target_mode.mode = mode_val
        self._switch_cli.call_async(req)
        print("[aic_oculus] AIC controller set to Cartesian mode.")

    def _tare_ft(self):
        """
        Hardware tare via service + software bias capture from the latest
        wrench.  Together they zero any residual gravity/cable-load offset
        so bias-corrected force magnitude starts near zero.
        """
        if self._tare_cli is not None and self._tare_cli.wait_for_service(timeout_sec=2.0):
            self._tare_cli.call_async(Trigger.Request())
            print("[aic_oculus] F/T hardware tare requested.")
        else:
            print("[aic_oculus] WARNING: tare service unavailable -- skipping hardware tare.")
        if self._latest_wrench is not None:
            f = self._latest_wrench.wrench.force
            self._ft_bias = (f.x, f.y, f.z)
            mag = math.sqrt(f.x*f.x + f.y*f.y + f.z*f.z)
            print(f"[aic_oculus] F/T software bias set: "
                  f"({f.x:.2f}, {f.y:.2f}, {f.z:.2f}) N  (mag {mag:.2f} N)")
        else:
            print("[aic_oculus] F/T software tare: no wrench yet -- bias unchanged.")

    # ------------------------------------------------------------------
    # Gripper
    # ------------------------------------------------------------------

    def _send_gripper_command(self, close: bool):
        """
        Command the Robotiq Hand-E to a binary open/closed position via
        JointState on /gripper_commands.  Position range per finger slider:
        0.0 m = closed, 0.025 m = open.  The right finger is a mimic.
        """
        if self._gripper_pub is None or self._node is None:
            return
        msg = JointState()
        msg.header.stamp = self._node.get_clock().now().to_msg()
        msg.name     = ['hande_left_finger_joint']
        msg.position = [0.0 if close else 0.025]
        msg.velocity = []
        msg.effort   = []
        self._gripper_pub.publish(msg)
        print(f"[aic_oculus] Gripper -> {'CLOSED' if close else 'OPEN'}")

    # ------------------------------------------------------------------
    # Force feedback
    # ------------------------------------------------------------------

    def _corrected_force_mag(self):
        """Bias-corrected contact force magnitude in Newtons."""
        if self._latest_wrench is None:
            return 0.0
        f = self._latest_wrench.wrench.force
        fx = f.x - self._ft_bias[0]
        fy = f.y - self._ft_bias[1]
        fz = f.z - self._ft_bias[2]
        return math.sqrt(fx*fx + fy*fy + fz*fz)

    def _compute_force_adjusted_stiffness(self):
        """
        Linear interpolation between TELEOP and INSERTION stiffness as
        contact force rises from ``force_lo`` to ``force_hi``.  Used by the
        standalone main() when publishing MotionUpdate directly.
        """
        fm = self._corrected_force_mag()
        flo, fhi = self.config.force_lo, self.config.force_hi
        if fm < flo:
            return list(TELEOP_STIFFNESS), list(TELEOP_DAMPING)
        t = min(1.0, (fm - flo) / (fhi - flo))
        return (
            _diag6x6(60.0 * (1.0 - t) + 15.0 * t),
            _diag6x6(50.0 * (1.0 - t) + 12.0 * t),
        )

    # ------------------------------------------------------------------
    # Terminal HUD
    # ------------------------------------------------------------------

    def _render_hud(self):
        """
        Four-line status HUD anchored to the bottom of the terminal.
        Skipped when stdout isn't a TTY so lerobot-record subprocess
        output isn't clobbered.
        """
        if not sys.stdout.isatty():
            return
        try:
            term = shutil.get_terminal_size((80, 24))
            cols = term.columns
            rows = term.lines
        except Exception:
            return

        GRN  = '\033[32m'; YLW  = '\033[33m'; RED  = '\033[31m'
        CYN  = '\033[36m'; DIM  = '\033[2m';  BOLD = '\033[1m'
        RST  = '\033[0m'

        vr_on  = self._have_ref
        an_on  = self._analogue_enabled
        ori_on = self._follow_ori
        lim_on = self._hud_limits_active

        def _indicator(active, label_on, label_off, col_on, col_off=DIM):
            dot = '●' if active else '○'
            col = col_on if active else col_off
            lbl = label_on if active else label_off
            return f"{col}{dot} {lbl}{RST}"

        mode_parts = [
            f"  {BOLD}MODE{RST}",
            f"VR {_indicator(vr_on, 'TRACKING', 'IDLE    ', GRN)}",
            f"ANALOGUE {_indicator(an_on, 'ON ', 'OFF', CYN)}",
            f"FRAME {CYN}{self._analogue_frame:<4}{RST}",
            f"ORI {_indicator(ori_on, 'on ', 'off', CYN)}",
            f"LIM {_indicator(lim_on, 'on ', 'off', CYN)}",
        ]
        mode_line = "   ".join(mode_parts)

        # Force bar
        f_mag = self._corrected_force_mag()
        bar_width   = 30
        f_scale_max = 25.0
        filled      = int(min(1.0, f_mag / f_scale_max) * bar_width)
        empty       = bar_width - filled

        if f_mag < self.config.force_lo:
            bar_col, status = GRN, 'free   '
        elif f_mag < self.config.force_hi:
            bar_col, status = YLW, 'contact'
        else:
            bar_col, status = RED, 'LIMIT  '

        bar        = f"{bar_col}{'█' * filled}{'░' * empty}{RST}"
        force_line = (
            f"  {BOLD}F/T {RST}  {bar}  "
            f"{bar_col}{f_mag:5.1f} N{RST}  {DIM}{status}{RST}"
        )

        bar_offset = 9
        mark_lo    = bar_offset + int(self.config.force_lo / f_scale_max * bar_width)
        mark_hi    = bar_offset + int(self.config.force_hi / f_scale_max * bar_width)
        scale_row  = [' '] * (bar_offset + bar_width + 14)
        for i, label in [(mark_lo, f'{self.config.force_lo:.0f}N'),
                         (mark_hi, f'{self.config.force_hi:.0f}N')]:
            for j, ch in enumerate(label):
                if 0 <= i + j < len(scale_row):
                    scale_row[i + j] = ch
        scale_line = f"  {DIM}{''.join(scale_row)}{RST}"

        quit_tag = f"  {BOLD}[x]{RST}{DIM} quit{RST}"
        dash_w   = max(0, cols - 4 - 10)
        sep_line = f"  {DIM}{'─' * dash_w}{RST}{quit_tag}"

        hud_lines = [sep_line, mode_line, force_line, scale_line]
        n = len(hud_lines)
        buf = '\033[s'   # save cursor
        for i, line in enumerate(hud_lines):
            row = rows - n + i + 1   # 1-indexed terminal row
            buf += f'\033[{row};1H\033[2K{line}'
        buf += '\033[u'  # restore cursor
        sys.stdout.write(buf)
        sys.stdout.flush()


# =============================================================================
#  Standalone runner
# =============================================================================

def main():
    """
    Standalone direct-drive runner.  Publishes MotionUpdate messages to
    /aic_controller/pose_commands at the nominal rate so the robot moves
    without the full lerobot-record stack — useful for smoke-testing the
    teleop pipeline.  The trajectory generation mode matches the config's
    ``cartesian_command_mode`` (velocity → MODE_VELOCITY, position → MODE_POSITION).

    See the module docstring for the full keyboard + controller mapping.
    Exit with 'x' or Ctrl-C.
    """
    # Real lerobot TeleoperatorConfig requires 'type' and 'id' fields; the
    # stub takes no arguments — try the real form first.
    try:
        config = AICOculusTeleopConfig(
            type="aic_oculus",
            id="aic",
            enable_local_keyboard_controls=True,
        )
    except TypeError:
        config = AICOculusTeleopConfig(enable_local_keyboard_controls=True)

    teleop = AICOculusTeleop(config)
    teleop.connect()

    from aic_control_interfaces.msg import MotionUpdate  # noqa: PLC0415
    try:
        from aic_control_interfaces.msg import TrajectoryGenerationMode  # noqa: PLC0415
        mode_vel = TrajectoryGenerationMode.MODE_VELOCITY
        mode_pos = TrajectoryGenerationMode.MODE_POSITION
    except Exception:
        # Fallback values — only used if the enum import above fails.
        # The real values come from the TrajectoryGenerationMode message
        # when it's available, so these only matter in degraded setups.
        mode_vel = 3
        mode_pos = 2

    pub = teleop._node.create_publisher(
        MotionUpdate, '/aic_controller/pose_commands',
        QoSProfile(reliability=ReliabilityPolicy.RELIABLE, depth=10))

    position_mode = (teleop.config.cartesian_command_mode == "position")

    def _publish(action, stiff, damp):
        msg = MotionUpdate()
        msg.header.stamp = teleop._node.get_clock().now().to_msg()
        msg.header.frame_id = teleop.config.base_frame
        if position_mode:
            msg.pose.position.x    = action["pose.position.x"]
            msg.pose.position.y    = action["pose.position.y"]
            msg.pose.position.z    = action["pose.position.z"]
            msg.pose.orientation.x = action["pose.orientation.x"]
            msg.pose.orientation.y = action["pose.orientation.y"]
            msg.pose.orientation.z = action["pose.orientation.z"]
            msg.pose.orientation.w = action["pose.orientation.w"]
            msg.trajectory_generation_mode.mode = mode_pos
        else:
            msg.velocity.linear.x  = action["linear.x"]
            msg.velocity.linear.y  = action["linear.y"]
            msg.velocity.linear.z  = action["linear.z"]
            msg.velocity.angular.x = action["angular.x"]
            msg.velocity.angular.y = action["angular.y"]
            msg.velocity.angular.z = action["angular.z"]
            msg.trajectory_generation_mode.mode = mode_vel
        msg.target_stiffness   = stiff
        msg.target_damping     = damp
        msg.feedforward_wrench_at_tip.force.x  = 0.0
        msg.feedforward_wrench_at_tip.force.y  = 0.0
        msg.feedforward_wrench_at_tip.force.z  = 0.0
        msg.feedforward_wrench_at_tip.torque.x = 0.0
        msg.feedforward_wrench_at_tip.torque.y = 0.0
        msg.feedforward_wrench_at_tip.torque.z = 0.0
        msg.wrench_feedback_gains_at_tip = [0.0] * 6
        pub.publish(msg)

    period = 1.0 / config.nominal_rate_hz
    try:
        while True:
            if teleop._keys.exit:
                break

            action = teleop.get_action()

            if teleop._keys.force_feedback:
                stiff, damp = teleop._compute_force_adjusted_stiffness()
            else:
                stiff, damp = list(TELEOP_STIFFNESS), list(TELEOP_DAMPING)

            _publish(action, stiff, damp)
            time.sleep(period)
    except KeyboardInterrupt:
        print()
    finally:
        try:
            teleop.disconnect()
        except Exception:
            pass
        if rclpy.ok():
            try:
                rclpy.shutdown()
            except Exception:
                pass


if __name__ == '__main__':
    main()
