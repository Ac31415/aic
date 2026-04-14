#
#  Copyright (C) 2026 Intrinsic Innovation LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import math
import threading
from dataclasses import dataclass, field
from threading import Thread
from typing import Any, cast

import pyspacemouse
import rclpy
from geometry_msgs.msg import Twist
from lerobot.teleoperators import Teleoperator, TeleoperatorConfig
from lerobot.teleoperators.keyboard import (
    KeyboardEndEffectorTeleop,
    KeyboardEndEffectorTeleopConfig,
)
from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError
from lerobot_teleoperator_devices import KeyboardJointTeleop, KeyboardJointTeleopConfig
from rclpy.duration import Duration
from rclpy.executors import SingleThreadedExecutor
from sensor_msgs.msg import Joy, JointState
from tf2_ros import Buffer, LookupException, ExtrapolationException, TransformListener

from .aic_robot import arm_joint_names
from .types import JointMotionUpdateActionDict, MotionUpdateActionDict, VRMotionUpdateActionDict


# =============================================================================
#  Private VR math utilities (ported from vr_aic.py)
#  All quaternions are (x, y, z, w) tuples.  Poses are (p, q) pairs.
# =============================================================================

def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _quat_norm(q: tuple) -> tuple:
    x, y, z, w = q
    n = math.sqrt(x * x + y * y + z * z + w * w)
    if n < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    return (x / n, y / n, z / n, w / n)


def _quat_mul(a: tuple, b: tuple) -> tuple:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    )


def _quat_inv(q: tuple) -> tuple:
    x, y, z, w = q
    return (-x, -y, -z, w)


def _rotate_vec_by_quat(v: tuple, q: tuple) -> tuple:
    vx, vy, vz = v
    qv = (vx, vy, vz, 0.0)
    qi = _quat_inv(q)
    r = _quat_mul(_quat_mul(q, qv), qi)
    return (r[0], r[1], r[2])


def _tf_to_T(tf: Any) -> tuple:
    t = tf.transform.translation
    r = tf.transform.rotation
    p = (t.x, t.y, t.z)
    q = _quat_norm((r.x, r.y, r.z, r.w))
    return p, q


def _T_inv(p: tuple, q: tuple) -> tuple:
    qi = _quat_inv(q)
    pr = _rotate_vec_by_quat(p, qi)
    return (-pr[0], -pr[1], -pr[2]), qi


def _T_mul(p1: tuple, q1: tuple, p2: tuple, q2: tuple) -> tuple:
    p2r = _rotate_vec_by_quat(p2, q1)
    return (
        (p1[0] + p2r[0], p1[1] + p2r[1], p1[2] + p2r[2]),
        _quat_norm(_quat_mul(q1, q2)),
    )


def _quat_from_axis_angle(ax: float, ay: float, az: float, angle: float) -> tuple:
    s = math.sin(angle * 0.5)
    return _quat_norm((ax * s, ay * s, az * s, math.cos(angle * 0.5)))


def _stick_ramp(v: float, deadzone: float, exponent: float = 1.5) -> float:
    if abs(v) < deadzone:
        return 0.0
    sign = 1.0 if v > 0.0 else -1.0
    normalised = (abs(v) - deadzone) / (1.0 - deadzone)
    return sign * (normalised ** exponent)


@TeleoperatorConfig.register_subclass("aic_keyboard_joint")
@dataclass
class AICKeyboardJointTeleopConfig(KeyboardJointTeleopConfig):
    arm_action_keys: list[str] = field(
        default_factory=lambda: [f"{x}" for x in arm_joint_names]
    )
    high_command_scaling: float = 0.05
    low_command_scaling: float = 0.02


class AICKeyboardJointTeleop(KeyboardJointTeleop):
    def __init__(self, config: AICKeyboardJointTeleopConfig):
        super().__init__(config)

        self.config = config
        self._low_scaling = config.low_command_scaling
        self._high_scaling = config.high_command_scaling
        self._current_scaling = self._high_scaling

        self.curr_joint_actions: JointMotionUpdateActionDict = {
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": 0.0,
            "elbow_joint": 0.0,
            "wrist_1_joint": 0.0,
            "wrist_2_joint": 0.0,
            "wrist_3_joint": 0.0,
        }

    @property
    def action_features(self) -> dict:
        return {"names": JointMotionUpdateActionDict.__annotations__}

    def _get_action_value(self, is_pressed: bool) -> float:
        return self._current_scaling if is_pressed else 0.0

    def get_action(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError()

        self._drain_pressed_keys()

        for key, is_pressed in self.current_pressed.items():

            if key == "u" and is_pressed:
                is_low_scaling = self._current_scaling == self._low_scaling
                self._current_scaling = (
                    self._high_scaling if is_low_scaling else self._low_scaling
                )
                print(f"Command scaling toggled to: {self._current_scaling}")
                continue

            val = self._get_action_value(is_pressed)

            if key == "q":
                self.curr_joint_actions["shoulder_pan_joint"] = val
            elif key == "a":
                self.curr_joint_actions["shoulder_pan_joint"] = -val
            elif key == "w":
                self.curr_joint_actions["shoulder_lift_joint"] = val
            elif key == "s":
                self.curr_joint_actions["shoulder_lift_joint"] = -val
            elif key == "e":
                self.curr_joint_actions["elbow_joint"] = val
            elif key == "d":
                self.curr_joint_actions["elbow_joint"] = -val
            elif key == "r":
                self.curr_joint_actions["wrist_1_joint"] = val
            elif key == "f":
                self.curr_joint_actions["wrist_1_joint"] = -val
            elif key == "t":
                self.curr_joint_actions["wrist_2_joint"] = val
            elif key == "g":
                self.curr_joint_actions["wrist_2_joint"] = -val
            elif key == "y":
                self.curr_joint_actions["wrist_3_joint"] = val
            elif key == "h":
                self.curr_joint_actions["wrist_3_joint"] = -val
            elif is_pressed:
                # If the key is pressed, add it to the misc_keys_queue
                # this will record key presses that are not part of the delta_x, delta_y, delta_z
                # this is useful for retrieving other events like interventions for RL, episode success, etc.
                self.misc_keys_queue.put(key)

        self.current_pressed.clear()

        return cast(dict, self.curr_joint_actions)


@TeleoperatorConfig.register_subclass("aic_keyboard_ee")
@dataclass(kw_only=True)
class AICKeyboardEETeleopConfig(KeyboardEndEffectorTeleopConfig):
    high_command_scaling: float = 0.1
    low_command_scaling: float = 0.02


class AICKeyboardEETeleop(KeyboardEndEffectorTeleop):
    def __init__(self, config: AICKeyboardEETeleopConfig):
        super().__init__(config)
        self.config = config

        self._high_scaling = config.high_command_scaling
        self._low_scaling = config.low_command_scaling
        self._current_scaling = self._high_scaling

        self._current_actions: MotionUpdateActionDict = {
            "linear.x": 0.0,
            "linear.y": 0.0,
            "linear.z": 0.0,
            "angular.x": 0.0,
            "angular.y": 0.0,
            "angular.z": 0.0,
        }

    @property
    def action_features(self) -> dict:
        return MotionUpdateActionDict.__annotations__

    def _get_action_value(self, is_pressed: bool) -> float:
        return self._current_scaling if is_pressed else 0.0

    def get_action(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError()

        self._drain_pressed_keys()

        for key, is_pressed in self.current_pressed.items():

            if key == "t" and is_pressed:
                is_low_speed = self._current_scaling == self._low_scaling
                self._current_scaling = (
                    self._high_scaling if is_low_speed else self._low_scaling
                )
                print(f"Command scaling toggled to: {self._current_scaling}")
                continue

            val = self._get_action_value(is_pressed)

            if key == "w":
                self._current_actions["linear.y"] = -val
            elif key == "s":
                self._current_actions["linear.y"] = val
            elif key == "a":
                self._current_actions["linear.x"] = -val
            elif key == "d":
                self._current_actions["linear.x"] = val
            elif key == "r":
                self._current_actions["linear.z"] = -val
            elif key == "f":
                self._current_actions["linear.z"] = val
            elif key == "W":
                self._current_actions["angular.x"] = val
            elif key == "S":
                self._current_actions["angular.x"] = -val
            elif key == "A":
                self._current_actions["angular.y"] = -val
            elif key == "D":
                self._current_actions["angular.y"] = val
            elif key == "q":
                self._current_actions["angular.z"] = -val
            elif key == "e":
                self._current_actions["angular.z"] = val
            elif is_pressed:
                # If the key is pressed, add it to the misc_keys_queue
                # this will record key presses that are not part of the delta_x, delta_y, delta_z
                # this is useful for retrieving other events like interventions for RL, episode success, etc.
                self.misc_keys_queue.put(key)

        self.current_pressed.clear()

        return cast(dict, self._current_actions)


@TeleoperatorConfig.register_subclass("aic_spacemouse")
@dataclass(kw_only=True)
class AICSpaceMouseTeleopConfig(TeleoperatorConfig):
    operator_position_front: bool = True
    device: str | None = None  # only needed for multiple space mice
    command_scaling: float = 0.1


class AICSpaceMouseTeleop(Teleoperator):
    def __init__(self, config: AICSpaceMouseTeleopConfig):
        super().__init__(config)
        self.config = config
        self._is_connected = False
        self._device: pyspacemouse.SpaceMouseDevice | None = None

        self._current_actions: MotionUpdateActionDict = {
            "linear.x": 0.0,
            "linear.y": 0.0,
            "linear.z": 0.0,
            "angular.x": 0.0,
            "angular.y": 0.0,
            "angular.z": 0.0,
        }

    @property
    def name(self) -> str:
        return "aic_spacemouse"

    @property
    def action_features(self) -> dict:
        return MotionUpdateActionDict.__annotations__

    @property
    def feedback_features(self) -> dict:
        # TODO
        return {}

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, calibrate: bool = True) -> None:
        if self.is_connected:
            raise DeviceAlreadyConnectedError()

        if not rclpy.ok():
            rclpy.init()

        self._node = rclpy.create_node("spacemouse_teleop")
        if calibrate:
            self._node.get_logger().warn(
                "Calibration not supported, ensure the robot is calibrated before running teleop."
            )

        self._device = pyspacemouse.open(
            dof_callback=None,
            # button_callback_arr=[
            #     pyspacemouse.ButtonCallback([0], self._button_callback),  # Button 1
            #     pyspacemouse.ButtonCallback([1], self._button_callback),  # Button 2
            # ],
            device=self.config.device,
        )

        if self._device is None:
            raise RuntimeError("Failed to open SpaceMouse device")

        self._executor = SingleThreadedExecutor()
        self._executor.add_node(self._node)
        self._executor_thread = Thread(target=self._executor.spin)
        self._executor_thread.start()
        self._is_connected = True

    @property
    def is_calibrated(self) -> bool:
        # Calibration not supported
        return True

    def calibrate(self) -> None:
        # Calibration not supported
        pass

    def configure(self) -> None:
        pass

    def apply_deadband(self, value, threshold=0.02):
        return value if abs(value) > threshold else 0.0

    def get_action(self) -> dict[str, Any]:
        if not self.is_connected or not self._device:
            raise DeviceNotConnectedError()

        state = self._device.read()

        clean_x = self.apply_deadband(float(state.x))
        clean_y = self.apply_deadband(float(state.y))
        clean_z = self.apply_deadband(float(state.z))
        clean_roll = self.apply_deadband(float(state.roll))
        clean_pitch = self.apply_deadband(float(state.pitch))
        clean_yaw = self.apply_deadband(float(state.yaw))

        twist_msg = Twist()
        twist_msg.linear.x = clean_x**1 * self.config.command_scaling
        twist_msg.linear.y = -(clean_y**1) * self.config.command_scaling
        twist_msg.linear.z = -(clean_z**1) * self.config.command_scaling
        twist_msg.angular.x = -(clean_pitch**1) * self.config.command_scaling
        twist_msg.angular.y = clean_roll**1 * self.config.command_scaling  #
        twist_msg.angular.z = clean_yaw**1 * self.config.command_scaling

        if not self.config.operator_position_front:
            twist_msg.linear.x *= -1
            twist_msg.linear.y *= -1
            twist_msg.angular.x *= -1
            twist_msg.angular.y *= -1

        self._current_actions = {
            "linear.x": twist_msg.linear.x,
            "linear.y": twist_msg.linear.y,
            "linear.z": twist_msg.linear.z,
            "angular.x": twist_msg.angular.x,
            "angular.y": twist_msg.angular.y,
            "angular.z": twist_msg.angular.z,
        }

        return cast(dict, self._current_actions)

    def send_feedback(self, feedback: dict[str, Any]) -> None:
        pass

    def disconnect(self) -> None:
        if self._device:
            self._device.close()
        self._is_connected = False
        pass


# =============================================================================
#  VR (Oculus Quest) teleoperator
# =============================================================================

@TeleoperatorConfig.register_subclass("aic_vr")
@dataclass(kw_only=True)
class AICVRTeleopConfig(TeleoperatorConfig):
    """Configuration for the Oculus Quest VR teleoperator.

    Produces ``VRMotionUpdateActionDict`` actions (absolute TCP pose in
    ``base_link`` plus gripper position).  Pair with
    ``AICRobotAICController(teleop_target_mode="vr_cartesian")``.

    Joy message layout (``/oculus/right/joy`` from oculus_reader):
      axes[0]  rightJS X  · axes[1]  rightJS Y
      axes[2]  rightTrig  · axes[3]  rightGrip
      buttons[0] A   buttons[1] B   buttons[2] RJ   buttons[3] RG
    """

    # TF frame identifiers
    base_frame: str = "base_link"
    ctrl_frame: str = "oculus_r"
    tcp_frame: str = "gripper/tcp"
    joy_topic: str = "/oculus/right/joy"

    # Control rate (Hz) — must be ≤ 30 for AIC impedance controller
    rate_hz: float = 30.0

    # Safety: maximum per-tick position increment (m/tick) and sphere radius (m)
    max_step_xyz: float = 0.020
    max_total_offset: float = 0.35

    # First-order low-pass coefficient applied to position target [0, 1]
    pos_lpf_alpha: float = 0.55

    # Gripper finger-slider positions (metres)
    gripper_open_pos: float = 0.025
    gripper_closed_pos: float = 0.0

    # Analogue stick shaping
    stick_deadzone: float = 0.15
    stick_ramp_exp: float = 2.0
    stick_mod_thresh: float = 0.30  # grip/trigger threshold to enter modifier mode
    stick_yaw_speed: float = 8.5e-3
    stick_pitch_speed: float = 8.5e-3
    stick_roll_speed: float = 8.5e-3
    stick_z_speed: float = 3.5e-4
    stick_xy_speed: float = 3.5e-4


class AICVRTeleop(Teleoperator):
    """LeRobot teleoperator for the Oculus Quest right controller.

    Subscribes to TF transforms (``oculus_r`` → ``base_link``) and
    ``/oculus/right/joy``, mirrors wrist motion to an absolute TCP target,
    and returns the target as a ``VRMotionUpdateActionDict`` on each
    ``get_action()`` call.

    Controller bindings
    -------------------
    Button A   Cycle mode: IDLE → VR TRACKING → ANALOGUE → IDLE
    Button B   Toggle orientation follow
    Button RJ  Toggle analogue-stick frame (``base_link`` ↔ TCP)
    Button RG  Toggle gripper open / closed

    Analogue stick (when VR tracking or analogue mode is active):
      Default        yaw (X) + Z translation (Y)
      Grip held      XY translation
      Trigger held   pitch (X) + roll (Y)
    """

    def __init__(self, config: AICVRTeleopConfig):
        super().__init__(config)
        self.config = config
        self._is_connected = False
        self._lock = threading.Lock()

        # VR reference transforms
        self._have_ref: bool = False
        self._p_base_ctrl0: tuple | None = None
        self._q_base_ctrl0: tuple | None = None
        self._p_base_tcp0: tuple | None = None
        self._q_base_tcp0: tuple | None = None

        # Last commanded pose (used for step-cap and analogue fallback)
        self._last_cmd_p: tuple | None = None
        self._last_cmd_q: tuple | None = None
        self._p_tgt_filt: tuple | None = None

        # Control mode flags
        self._vr_enabled: bool = False
        self._analogue_enabled: bool = False
        self._follow_orientation: bool = False
        self._analogue_frame: str = "base"  # "base" or "tcp"

        # Analogue stick state
        self._analogue_ref_p: list | None = None
        self._analogue_ref_q: tuple | None = None
        self._stick_p_offset: list = [0.0, 0.0, 0.0]
        self._stick_q_offset: tuple = (0.0, 0.0, 0.0, 1.0)
        self._latest_joy: Joy | None = None

        # Gripper
        self._gripper_closed: bool = False

        # Joy rising-edge detection
        self._btn_a_prev: bool = False
        self._btn_b_prev: bool = False
        self._btn_rj_prev: bool = False
        self._btn_rg_prev: bool = False

        # Latest action (updated by 30 Hz timer, read by get_action)
        self._current_action: VRMotionUpdateActionDict = {
            "pose.position.x": 0.0,
            "pose.position.y": 0.0,
            "pose.position.z": 0.0,
            "pose.orientation.x": 0.0,
            "pose.orientation.y": 0.0,
            "pose.orientation.z": 0.0,
            "pose.orientation.w": 1.0,
            "gripper.position": config.gripper_open_pos,
        }

    # ── Teleoperator interface ────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "aic_vr"

    @property
    def action_features(self) -> dict:
        return VRMotionUpdateActionDict.__annotations__

    @property
    def feedback_features(self) -> dict:
        return {}

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def is_calibrated(self) -> bool:
        return True

    def calibrate(self) -> None:
        pass

    def configure(self) -> None:
        pass

    def connect(self, calibrate: bool = True) -> None:
        if self._is_connected:
            raise DeviceAlreadyConnectedError()

        if not rclpy.ok():
            rclpy.init()

        self._node = rclpy.create_node("aic_vr_teleop")
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self._node)

        self._joy_sub = self._node.create_subscription(
            Joy, self.config.joy_topic, self._joy_callback, 10
        )

        self._timer = self._node.create_timer(1.0 / self.config.rate_hz, self._update)

        self._executor = SingleThreadedExecutor()
        self._executor.add_node(self._node)
        self._executor_thread = Thread(target=self._executor.spin, daemon=True)
        self._executor_thread.start()

        self._is_connected = True
        self._node.get_logger().info(
            "AICVRTeleop connected. Waiting for Oculus TF and Joy...\n"
            "  Button A  — cycle mode (IDLE → VR TRACKING → ANALOGUE → IDLE)\n"
            "  Button B  — toggle orientation follow\n"
            "  Button RJ — toggle analogue frame (base_link ↔ TCP)\n"
            "  Button RG — toggle gripper open / closed"
        )

    def get_action(self) -> dict[str, Any]:
        if not self.is_connected:
            raise DeviceNotConnectedError()
        with self._lock:
            return dict(self._current_action)

    def send_feedback(self, feedback: dict[str, Any]) -> None:
        pass

    def disconnect(self) -> None:
        if not self._is_connected:
            raise DeviceNotConnectedError()
        self._executor.shutdown()
        self._executor_thread.join()
        self._node.destroy_node()
        self._is_connected = False

    # ── Joy callback ──────────────────────────────────────────────────────────

    def _joy_callback(self, msg: Joy) -> None:
        def _btn(i: int) -> bool:
            return bool(msg.buttons[i]) if len(msg.buttons) > i else False

        # Button A — cycle mode: IDLE → VR TRACKING → ANALOGUE → IDLE
        a_now = _btn(0)
        if a_now and not self._btn_a_prev:
            if not self._vr_enabled and not self._analogue_enabled:
                self._vr_enabled = True
                self._have_ref = False
                self._node.get_logger().info("Mode → VR TRACKING [A]")
            elif self._vr_enabled and not self._analogue_enabled:
                self._vr_enabled = False
                self._analogue_enabled = True
                self._analogue_ref_p = list(self._last_cmd_p) if self._last_cmd_p else None
                self._analogue_ref_q = self._last_cmd_q
                self._stick_p_offset = [0.0, 0.0, 0.0]
                self._stick_q_offset = (0.0, 0.0, 0.0, 1.0)
                self._node.get_logger().info("Mode → ANALOGUE [A]")
            else:
                self._vr_enabled = False
                self._analogue_enabled = False
                self._node.get_logger().info("Mode → IDLE [A]")
        self._btn_a_prev = a_now

        # Button B — toggle orientation follow
        b_now = _btn(1)
        if b_now and not self._btn_b_prev:
            self._follow_orientation = not self._follow_orientation
            state = "ON" if self._follow_orientation else "OFF"
            self._node.get_logger().info(f"Orientation follow → {state} [B]")
        self._btn_b_prev = b_now

        # Button RJ (joystick click) — toggle analogue command frame
        rj_now = _btn(2)
        if rj_now and not self._btn_rj_prev:
            self._analogue_frame = "tcp" if self._analogue_frame == "base" else "base"
            self._node.get_logger().info(f"Analogue frame → {self._analogue_frame} [RJ]")
        self._btn_rj_prev = rj_now

        # Button RG (grip digital) — toggle gripper
        rg_now = _btn(3)
        if rg_now and not self._btn_rg_prev:
            self._gripper_closed = not self._gripper_closed
            state = "CLOSED" if self._gripper_closed else "OPEN"
            self._node.get_logger().info(f"Gripper → {state} [RG]")
        self._btn_rg_prev = rg_now

        self._latest_joy = msg

    # ── 30 Hz timer: compute target pose ─────────────────────────────────────

    def _update(self) -> None:
        """Compute the latest VR target pose and update ``_current_action``."""
        gripper_pos = (
            self.config.gripper_closed_pos
            if self._gripper_closed
            else self.config.gripper_open_pos
        )

        if not self._vr_enabled:
            # Analogue-only mode: nudge the last commanded pose with the stick
            if self._analogue_enabled and self._analogue_ref_p is not None:
                try:
                    p_tgt, q_tgt = self._apply_stick_nudge(
                        tuple(self._analogue_ref_p), self._analogue_ref_q
                    )
                    self._last_cmd_p = p_tgt
                    self._last_cmd_q = q_tgt
                    with self._lock:
                        self._current_action = self._make_action(p_tgt, q_tgt, gripper_pos)
                except (LookupException, ExtrapolationException, ValueError) as e:
                    self._node.get_logger().debug(f"Analogue stick nudge failed: {e}")
            elif self._last_cmd_p is not None:
                # Hold last pose
                with self._lock:
                    self._current_action = self._make_action(
                        self._last_cmd_p, self._last_cmd_q, gripper_pos
                    )
            return

        try:
            if not self._have_ref:
                self._capture_reference()

            # Step 1: compute controller motion delta from captured reference
            tf_bc = self._lookup(self.config.base_frame, self.config.ctrl_frame)
            p_base_ctrl, q_base_ctrl = _tf_to_T(tf_bc)

            p0i, q0i = _T_inv(self._p_base_ctrl0, self._q_base_ctrl0)
            p_delta, q_delta = _T_mul(p0i, q0i, p_base_ctrl, q_base_ctrl)

            # Step 2: remap controller axes to robot base_link axes.
            # Empirically determined for the AIC UR5e workcell:
            #   X_robot =  Y_ctrl  (controller left/right → robot forward/back)
            #   Y_robot =  X_ctrl  (controller forward    → robot lateral)
            #   Z_robot = -Z_ctrl  (controller up         → robot up, sign flipped)
            p_delta_mapped = (p_delta[1], p_delta[0], -p_delta[2])
            q_delta_mapped = (q_delta[1], q_delta[0], -q_delta[2], q_delta[3])

            # Step 3: apply delta to reference TCP pose
            p_tgt = (
                self._p_base_tcp0[0] + p_delta_mapped[0],
                self._p_base_tcp0[1] + p_delta_mapped[1],
                self._p_base_tcp0[2] + p_delta_mapped[2],
            )
            q_tgt = _quat_mul(q_delta_mapped, self._q_base_tcp0)

            # Step 4: apply analogue stick offsets when analogue mode is active
            if self._analogue_enabled:
                p_tgt, q_tgt = self._apply_stick_nudge(p_tgt, q_tgt)

            # Step 5: safety limits
            dx = p_tgt[0] - self._p_base_tcp0[0]
            dy = p_tgt[1] - self._p_base_tcp0[1]
            dz = p_tgt[2] - self._p_base_tcp0[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist > self.config.max_total_offset:
                scale = self.config.max_total_offset / max(1e-9, dist)
                p_tgt = (
                    self._p_base_tcp0[0] + dx * scale,
                    self._p_base_tcp0[1] + dy * scale,
                    self._p_base_tcp0[2] + dz * scale,
                )

            if self._last_cmd_p is not None:
                sx = _clamp(
                    p_tgt[0] - self._last_cmd_p[0],
                    -self.config.max_step_xyz,
                    self.config.max_step_xyz,
                )
                sy = _clamp(
                    p_tgt[1] - self._last_cmd_p[1],
                    -self.config.max_step_xyz,
                    self.config.max_step_xyz,
                )
                sz = _clamp(
                    p_tgt[2] - self._last_cmd_p[2],
                    -self.config.max_step_xyz,
                    self.config.max_step_xyz,
                )
                p_tgt = (
                    self._last_cmd_p[0] + sx,
                    self._last_cmd_p[1] + sy,
                    self._last_cmd_p[2] + sz,
                )

            if not self._follow_orientation:
                q_tgt = self._q_base_tcp0

            # Step 6: first-order low-pass filter on position
            if self._p_tgt_filt is None:
                self._p_tgt_filt = p_tgt
            else:
                a = self.config.pos_lpf_alpha
                self._p_tgt_filt = (
                    a * p_tgt[0] + (1 - a) * self._p_tgt_filt[0],
                    a * p_tgt[1] + (1 - a) * self._p_tgt_filt[1],
                    a * p_tgt[2] + (1 - a) * self._p_tgt_filt[2],
                )
            p_tgt = self._p_tgt_filt

            self._last_cmd_p = p_tgt
            self._last_cmd_q = q_tgt

            with self._lock:
                self._current_action = self._make_action(p_tgt, q_tgt, gripper_pos)

        except (LookupException, ExtrapolationException):
            # TF lookup failures are expected transiently at startup or when
            # the oculus_reader node is not yet publishing transforms.
            pass

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _make_action(
        self, p: tuple, q: tuple, gripper_pos: float
    ) -> VRMotionUpdateActionDict:
        return {
            "pose.position.x": float(p[0]),
            "pose.position.y": float(p[1]),
            "pose.position.z": float(p[2]),
            "pose.orientation.x": float(q[0]),
            "pose.orientation.y": float(q[1]),
            "pose.orientation.z": float(q[2]),
            "pose.orientation.w": float(q[3]),
            "gripper.position": float(gripper_pos),
        }

    def _lookup(self, target: str, source: str) -> Any:
        return self._tf_buffer.lookup_transform(
            target, source, rclpy.time.Time(), timeout=Duration(seconds=0.05)
        )

    def _capture_reference(self) -> None:
        tf_bc = self._lookup(self.config.base_frame, self.config.ctrl_frame)
        tf_bt = self._lookup(self.config.base_frame, self.config.tcp_frame)
        self._p_base_ctrl0, self._q_base_ctrl0 = _tf_to_T(tf_bc)
        self._p_base_tcp0, self._q_base_tcp0 = _tf_to_T(tf_bt)
        self._have_ref = True
        self._last_cmd_p = self._p_base_tcp0
        self._last_cmd_q = self._q_base_tcp0
        self._p_tgt_filt = None
        self._stick_p_offset = [0.0, 0.0, 0.0]
        self._stick_q_offset = (0.0, 0.0, 0.0, 1.0)
        self._node.get_logger().info("VR reference captured.")

    def _apply_stick_nudge(self, p_tgt: tuple, q_tgt: tuple) -> tuple:
        """Apply accumulated analogue stick offsets to a pose and return the result."""
        if self._latest_joy is None:
            p_out = (
                p_tgt[0] + self._stick_p_offset[0],
                p_tgt[1] + self._stick_p_offset[1],
                p_tgt[2] + self._stick_p_offset[2],
            )
            return p_out, _quat_norm(_quat_mul(self._stick_q_offset, q_tgt))

        axes = self._latest_joy.axes

        def _ax(i: int) -> float:
            return axes[i] if len(axes) > i else 0.0

        sx = _stick_ramp(_ax(0), self.config.stick_deadzone, self.config.stick_ramp_exp)
        sy = _stick_ramp(_ax(1), self.config.stick_deadzone, self.config.stick_ramp_exp)
        grip_held = _ax(3) >= self.config.stick_mod_thresh
        trigger_held = _ax(2) >= self.config.stick_mod_thresh

        def _frame_axis(local_axis: tuple) -> tuple:
            if self._analogue_frame == "tcp":
                return _rotate_vec_by_quat(local_axis, q_tgt)
            return local_axis

        if grip_held:
            # XY translation in the horizontal plane
            dx = sx * self.config.stick_xy_speed
            dy = sy * self.config.stick_xy_speed
            local = (
                _rotate_vec_by_quat((dx, dy, 0.0), q_tgt)
                if self._analogue_frame == "tcp"
                else (dx, dy, 0.0)
            )
            self._stick_p_offset[0] += local[0]
            self._stick_p_offset[1] += local[1]
            self._stick_p_offset[2] += local[2]
        elif trigger_held:
            # Pitch (stick X) + roll (stick Y)
            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 1.0, 0.0))
                dq = _quat_from_axis_angle(*axis, -sx * self.config.stick_pitch_speed)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))
            if abs(sy) > 0.0:
                axis = _frame_axis((1.0, 0.0, 0.0))
                dq = _quat_from_axis_angle(*axis, -sy * self.config.stick_roll_speed)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))
        else:
            # Yaw (stick X) + Z translation (stick Y) — default mode
            dz = sy * self.config.stick_z_speed
            local_z = (
                _rotate_vec_by_quat((0.0, 0.0, dz), q_tgt)
                if self._analogue_frame == "tcp"
                else (0.0, 0.0, dz)
            )
            self._stick_p_offset[0] += local_z[0]
            self._stick_p_offset[1] += local_z[1]
            self._stick_p_offset[2] += local_z[2]

            if abs(sx) > 0.0:
                axis = _frame_axis((0.0, 0.0, 1.0))
                dq = _quat_from_axis_angle(*axis, -sx * self.config.stick_yaw_speed)
                self._stick_q_offset = _quat_norm(_quat_mul(dq, self._stick_q_offset))

        p_out = (
            p_tgt[0] + self._stick_p_offset[0],
            p_tgt[1] + self._stick_p_offset[1],
            p_tgt[2] + self._stick_p_offset[2],
        )
        return p_out, _quat_norm(_quat_mul(self._stick_q_offset, q_tgt))
