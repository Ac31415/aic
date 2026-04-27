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

import os

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

import time
import torch
import numpy as np
import cv2
from pathlib import Path
from typing import Callable, Dict, Any, List
from rclpy.node import Node
from geometry_msgs.msg import Pose, Vector3, Wrench
from sensor_msgs.msg import JointState

from aic_model.policy import (
    GetObservationCallback,
    MoveRobotCallback,
    Policy,
    SendFeedbackCallback,
)
from aic_model_interfaces.msg import Observation
from aic_task_interfaces.msg import Task

from aic_control_interfaces.msg import (
    MotionUpdate,
    TrajectoryGenerationMode,
)

# LeRobot PI05 & Safetensors
from lerobot.policies.pi05.modeling_pi05 import PI05Policy
from lerobot.utils.constants import OBS_LANGUAGE_TOKENS, OBS_LANGUAGE_ATTENTION_MASK
from safetensors.torch import load_file
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer


class pi05_base_trained_0(Policy):
    def __init__(self, parent_node: Node):
        super().__init__(parent_node)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # -------------------------------------------------------------------------
        # 1. Load PI05 Policy from HuggingFace
        # -------------------------------------------------------------------------
        repo_id = "Ac31415/trained_models_pi05_base_sfp_to_sfp_port_0_of_nic_card_mount_0_sc_to_sc_port_base_of_sc_port_0_4"

        # Download checkpoint files
        policy_path = Path(
            snapshot_download(
                repo_id=repo_id,
                allow_patterns=["config.json", "model.safetensors", "*.safetensors"],
            )
        )

        # Load PI05 policy weights
        self.policy = PI05Policy.from_pretrained(repo_id)
        self.policy.eval()
        self.policy.to(self.device)

        self.get_logger().info(f"PI05 Policy loaded on {self.device} from {policy_path}")

        # -------------------------------------------------------------------------
        # 2. Normalization Stats Loading
        # -------------------------------------------------------------------------
        # PI05 uses QUANTILES normalization (q01/q99) for both state and action.
        # The state is normalized to [-1, 1] before being discretized into the prompt.
        # The action is unnormalized from [-1, 1] back to robot-space after inference.
        stats_path = (
            policy_path / "policy_preprocessor_step_3_normalizer_processor.safetensors"
        )
        stats = load_file(stats_path)

        # Helper to extract and shape stats for broadcasting
        def get_stat(key, shape):
            return stats[key].to(self.device).view(*shape)

        # State quantile stats — normalize state to [-1, 1] before discretization
        self.state_q01 = get_stat("observation.state.q01", (1, -1))
        self.state_q99 = get_stat("observation.state.q99", (1, -1))

        # Action quantile stats — unnormalize model output to robot-space
        self.action_q01 = get_stat("action.q01", (1, -1))
        self.action_q99 = get_stat("action.q99", (1, -1))

        # -------------------------------------------------------------------------
        # 3. Load PaliGemma Tokenizer
        # -------------------------------------------------------------------------
        # PI05 encodes the task description and discretized robot state as a text
        # prompt tokenized by the PaliGemma tokenizer.
        self.tokenizer = AutoTokenizer.from_pretrained("google/paligemma-3b-pt-224")
        self.tokenizer_max_length = self.policy.config.tokenizer_max_length

        # Config
        self.image_scaling = 0.25  # Must match AICRobotAICControllerConfig

        # Publisher for gripper commands (VR dataset includes gripper position)
        self.gripper_pub = parent_node.create_publisher(
            JointState, "/gripper_commands", 10
        )

        self.get_logger().info("PI05 policy node initialized successfully.")

    @staticmethod
    def _img_to_tensor(
        raw_img,
        device: torch.device,
        scale: float,
    ) -> torch.Tensor:
        """Converts ROS Image -> Resized -> Permuted -> [0, 1] Tensor (1, C, H, W).

        PI05Policy._preprocess_images normalizes images from [0, 1] to [-1, 1]
        internally, so no manual mean/std normalization is applied here.
        """
        # 1. Bytes to Numpy (H, W, C)
        img_np = np.frombuffer(raw_img.data, dtype=np.uint8).reshape(
            raw_img.height, raw_img.width, 3
        )

        # 2. Resize
        if scale != 1.0:
            img_np = cv2.resize(
                img_np, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA
            )

        # 3. To Tensor -> Permute (HWC -> CHW) -> Float -> Div(255) -> Batch Dim
        tensor = (
            torch.from_numpy(img_np)
            .permute(2, 0, 1)
            .float()
            .div(255.0)
            .unsqueeze(0)
            .to(device)
        )

        return tensor

    def _build_state_vector(self, obs_msg: Observation) -> np.ndarray:
        """Construct flat state vector matching training order."""
        tcp_pose = obs_msg.controller_state.tcp_pose
        tcp_vel = obs_msg.controller_state.tcp_velocity

        return np.array(
            [
                # TCP Position (3)
                tcp_pose.position.x,
                tcp_pose.position.y,
                tcp_pose.position.z,
                # TCP Orientation (4)
                tcp_pose.orientation.x,
                tcp_pose.orientation.y,
                tcp_pose.orientation.z,
                tcp_pose.orientation.w,
                # TCP Linear Vel (3)
                tcp_vel.linear.x,
                tcp_vel.linear.y,
                tcp_vel.linear.z,
                # TCP Angular Vel (3)
                tcp_vel.angular.x,
                tcp_vel.angular.y,
                tcp_vel.angular.z,
                # TCP Error (6)
                *obs_msg.controller_state.tcp_error,
                # Joint Positions (7)
                *obs_msg.joint_states.position[:7],
            ],
            dtype=np.float32,
        )

    def _tokenize_prompt(
        self, task_text: str, state_np: np.ndarray
    ) -> Dict[str, torch.Tensor]:
        """Build and tokenize the PI05 language prompt encoding the task and robot state.

        Mirrors Pi05PrepareStateTokenizerProcessorStep:
        1. Quantile-normalize state to [-1, 1] using q01/q99 stats.
        2. Discretize normalized state into 256 bins (matching the training pipeline).
        3. Build prompt: "Task: {task_text}, State: {state_str};\\nAction: "
        4. Tokenize with the PaliGemma tokenizer.
        """
        # 1. Quantile-normalize state to [-1, 1]: normalized = 2*(x - q01)/(q99 - q01) - 1
        raw_state = torch.from_numpy(state_np).float().unsqueeze(0).to(self.device)
        denom = (self.state_q99 - self.state_q01).clamp(min=1e-8)
        normalized_state = 2.0 * (raw_state - self.state_q01) / denom - 1.0
        normalized_state = normalized_state.clamp(-1.0, 1.0)

        # 2. Discretize into 256 bins
        state_np_norm = normalized_state[0].cpu().numpy()
        discretized = np.digitize(state_np_norm, bins=np.linspace(-1, 1, 257)[:-1]) - 1

        # 3. Build full prompt
        cleaned_text = task_text.strip().replace("_", " ").replace("\n", " ")
        state_str = " ".join(map(str, discretized))
        full_prompt = f"Task: {cleaned_text}, State: {state_str};\nAction: "

        # 4. Tokenize
        encoded = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            padding="max_length",
            max_length=self.tokenizer_max_length,
            truncation=True,
        )

        return {
            OBS_LANGUAGE_TOKENS: encoded["input_ids"].to(self.device),
            OBS_LANGUAGE_ATTENTION_MASK: encoded["attention_mask"].to(self.device),
        }

    def prepare_observations(
        self, obs_msg: Observation, task_text: str
    ) -> Dict[str, torch.Tensor]:
        """Convert ROS Observation message into a batch dict for PI05Policy.select_action.

        Images are returned as [0, 1] CHW tensors (PI05Policy normalizes them to [-1, 1]
        internally). The language prompt encodes the task description and current robot
        state as discretized tokens.
        """
        # --- Process Cameras ---
        obs = {
            "observation.images.left_camera": self._img_to_tensor(
                obs_msg.left_image,
                self.device,
                self.image_scaling,
            ),
            "observation.images.center_camera": self._img_to_tensor(
                obs_msg.center_image,
                self.device,
                self.image_scaling,
            ),
            "observation.images.right_camera": self._img_to_tensor(
                obs_msg.right_image,
                self.device,
                self.image_scaling,
            ),
        }

        # --- Build and Tokenize Language Prompt (includes discretized robot state) ---
        state_np = self._build_state_vector(obs_msg)
        obs.update(self._tokenize_prompt(task_text, state_np))

        return obs

    def insert_cable(
        self,
        task: Task,
        get_observation: GetObservationCallback,
        move_robot: MoveRobotCallback,
        send_feedback: SendFeedbackCallback,
        **kwargs,
    ):
        self.policy.reset()
        self.get_logger().info(f"pi05_base_trained_0.insert_cable() enter. Task: {task}")

        port_frame = f"task_board/{task.target_module_name}/{task.port_name}_link"
        cable_tip_frame = f"{task.cable_name}/{task.plug_name}_link"

        # Build task description prompt from task fields
        task_text = (
            f"Insert {task.plug_name} of {task.cable_name} "
            f"into {task.port_name} of {task.target_module_name}"
        )
        self.get_logger().info(f"Task prompt: '{task_text}'")

        start_time = time.time()

        # Run inference for 30 seconds
        while time.time() - start_time < 30.0:
            loop_start = time.time()

            # 1. Get & Process Observation
            observation_msg = get_observation()

            if observation_msg is None:
                self.get_logger().info("No observation received.")
                continue

            obs_batch = self.prepare_observations(observation_msg, task_text)

            # 2. Model Inference
            with torch.inference_mode():
                # Returns shape [action_dim] — one action popped from the predicted chunk
                normalized_action = self.policy.select_action(obs_batch)

            # 3. Un-normalize Action using quantile stats
            # Formula: unnorm = (norm + 1) * (q99 - q01) / 2 + q01
            action_q01 = self.action_q01[0]
            action_q99 = self.action_q99[0]
            action_dim = normalized_action.shape[-1]
            raw_action = (
                (normalized_action + 1.0)
                * (action_q99[:action_dim] - action_q01[:action_dim])
                / 2.0
                + action_q01[:action_dim]
            )
            action = raw_action.cpu().numpy()

            self.get_logger().info(f"Action: {action}")

            # 4. Extract and Command
            # action: [0:3] TCP position (x, y, z), [3:7] TCP orientation quat (x, y, z, w)
            pose = Pose()
            pose.position.x = float(action[0])
            pose.position.y = float(action[1])
            pose.position.z = float(action[2])
            pose.orientation.x = float(action[3])
            pose.orientation.y = float(action[4])
            pose.orientation.z = float(action[5])
            pose.orientation.w = float(action[6])

            motion_update = self.set_vr_cartesian_pose_target(pose)
            move_robot(motion_update=motion_update)
            send_feedback("in progress...")

            # Maintain control rate (approx 4Hz loop = 0.25s sleep)
            elapsed = time.time() - loop_start
            time.sleep(max(0, 0.25 - elapsed))

        self.get_logger().info("pi05_base_trained_0.insert_cable() exiting...")
        return True

    def set_vr_cartesian_pose_target(
        self, pose: Pose, frame_id: str = "base_link"
    ) -> MotionUpdate:
        """Build and publish a pose-based MotionUpdate matching VR teleop recordings.

        Mirrors the behaviour of ``send_action_vr_cartesian`` in
        ``AICRobotAICController``: sends an absolute Cartesian pose target via
        ``MODE_POSITION`` and publishes a gripper command on ``/gripper_commands``.
        Stiffness / damping values match those used during VR data collection.
        """
        motion_update_msg = MotionUpdate()
        motion_update_msg.header.frame_id = frame_id
        motion_update_msg.header.stamp = self.get_clock().now().to_msg()

        motion_update_msg.pose = pose

        motion_update_msg.target_stiffness = np.diag(
            [60.0, 60.0, 60.0, 60.0, 60.0, 60.0]
        ).flatten()
        motion_update_msg.target_damping = np.diag(
            [50.0, 50.0, 50.0, 50.0, 50.0, 50.0]
        ).flatten()

        motion_update_msg.feedforward_wrench_at_tip = Wrench(
            force=Vector3(x=0.0, y=0.0, z=0.0), torque=Vector3(x=0.0, y=0.0, z=0.0)
        )

        motion_update_msg.wrench_feedback_gains_at_tip = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        motion_update_msg.trajectory_generation_mode.mode = (
            TrajectoryGenerationMode.MODE_POSITION
        )

        # # Publish gripper command — hande_left_finger_joint, right finger is a mimic
        # gripper_msg = JointState()
        # gripper_msg.header.stamp = motion_update_msg.header.stamp
        # gripper_msg.name = ["hande_left_finger_joint"]
        # gripper_msg.position = [gripper_pos]
        # self.gripper_pub.publish(gripper_msg)

        return motion_update_msg