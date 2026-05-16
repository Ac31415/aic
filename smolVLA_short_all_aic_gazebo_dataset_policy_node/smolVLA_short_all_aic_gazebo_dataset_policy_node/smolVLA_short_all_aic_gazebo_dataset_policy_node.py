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
from geometry_msgs.msg import Twist, Vector3, Wrench
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

# LeRobot SmolVLA & Safetensors
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.utils.constants import OBS_LANGUAGE_TOKENS, OBS_LANGUAGE_ATTENTION_MASK, OBS_STATE, OBS_IMAGES
from safetensors.torch import load_file
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

import json
import draccus
from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig


class smolVLA_short_all_aic_gazebo_dataset_policy_node(Policy):
    def __init__(self, parent_node: Node):
        super().__init__(parent_node)
        print("cuda: ", torch.cuda.is_available())
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("device: ", self.device)

        # -------------------------------------------------------------------------
        # 1. Load SmolVLA Policy from Local Files
        # -------------------------------------------------------------------------
        # Resolve the model directory outside the installed package.
        # Set OFFLINE_POLICY_PATH to point at the exported SmolVLA checkpoint.
        default_model_path = Path(__file__).resolve().parent / "trained model"
        local_model_path = Path(
            os.environ.get("OFFLINE_POLICY_PATH", str(default_model_path))
        ).expanduser()

        if not local_model_path.exists():
            raise FileNotFoundError(
                f"SmolVLA model directory not found: {local_model_path}. "
                "Set OFFLINE_POLICY_PATH to the local checkpoint folder."
            )

        print(f"Loading SmolVLA policy from: {local_model_path}")
        self.policy = SmolVLAPolicy.from_pretrained(
            str(local_model_path),
            local_files_only=True
        )
        
        print("Setting policy to eval mode")
        self.policy.eval()
        self.policy.to(self.device)
        print(f"SmolVLA Policy loaded on {self.device} from {local_model_path}")

        self.get_logger().info(f"SmolVLA Policy loaded on {self.device} from {local_model_path}")

        # -------------------------------------------------------------------------
        # 2. Get Normalization Stats from Policy Config
        # -------------------------------------------------------------------------
        # SmolVLA uses MEAN_STD normalization for state and action
        # Stats are stored in the policy's config and preprocessor
        self.config = self.policy.config

        stats_path = (
            local_model_path / "policy_preprocessor_step_5_normalizer_processor.safetensors"
        )
        stats = load_file(stats_path)

        def get_stat(key: str, shape: tuple[int, ...]) -> torch.Tensor:
            return stats[key].to(self.device).view(*shape)

        self.state_mean = get_stat("observation.state.mean", (1, -1))
        self.state_std = get_stat("observation.state.std", (1, -1))
        self.action_mean = get_stat("action.mean", (1, -1))
        self.action_std = get_stat("action.std", (1, -1))
        
        # -------------------------------------------------------------------------
        # 3. Load Tokenizer from Local Files
        # -------------------------------------------------------------------------
        # SmolVLA uses the SmolVLM tokenizer
        from transformers import AutoTokenizer
        # Try to load tokenizer from local cache or specify a local path
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.vlm_model_name,
                local_files_only=True
            )
        except Exception as e:
            print(f"Warning: Could not load tokenizer from local files: {e}")
            print(f"Attempting to load from HuggingFace...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.vlm_model_name)
        self.tokenizer_max_length = self.config.tokenizer_max_length

    # Config
        self.image_scaling = 0.25  # Must match AICRobotAICControllerConfig

        # Publisher for gripper commands (VR dataset includes gripper position)
        self.gripper_pub = parent_node.create_publisher(
            JointState, "/gripper_commands", 10
        )

        self.get_logger().info("SmolVLA policy node initialized successfully.")

    @staticmethod
    def _img_to_tensor(
        raw_img,
        device: torch.device,
        scale: float,
    ) -> torch.Tensor:
        """Converts ROS Image -> Resized -> Permuted -> [0, 1] Tensor (1, C, H, W).

        SmolVLAPolicy expects images in [0, 1] range. Internal preprocessing
        will handle any additional normalization if needed.
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

    def _tokenize_prompt(self, task_text: str) -> Dict[str, torch.Tensor]:
        """Tokenize the task description for SmolVLA.

        SmolVLA does not discretize robot state into the prompt.
        It simply encodes the task/language instruction.
        """
        # Clean up task text
        cleaned_text = task_text.strip().replace("_", " ").replace("\n", " ")

        # Tokenize with the SmolVLM tokenizer
        encoded = self.tokenizer(
            cleaned_text,
            return_tensors="pt",
            padding="max_length",
            max_length=self.tokenizer_max_length,
            truncation=True,
        )

        return {
            OBS_LANGUAGE_TOKENS: encoded["input_ids"].to(self.device),
            OBS_LANGUAGE_ATTENTION_MASK: encoded["attention_mask"].to(torch.bool).to(self.device),
        }

    def _build_state_vector(self, obs_msg: Observation) -> np.ndarray:
        """Construct the 26D robot state vector used during training."""
        tcp_pose = obs_msg.controller_state.tcp_pose
        tcp_vel = obs_msg.controller_state.tcp_velocity

        return np.array(
            [
                tcp_pose.position.x,
                tcp_pose.position.y,
                tcp_pose.position.z,
                tcp_pose.orientation.x,
                tcp_pose.orientation.y,
                tcp_pose.orientation.z,
                tcp_pose.orientation.w,
                tcp_vel.linear.x,
                tcp_vel.linear.y,
                tcp_vel.linear.z,
                tcp_vel.angular.x,
                tcp_vel.angular.y,
                tcp_vel.angular.z,
                *obs_msg.controller_state.tcp_error,
                *obs_msg.joint_states.position[:7],
            ],
            dtype=np.float32,
        )

    def prepare_observations(
        self, obs_msg: Observation, task_text: str
    ) -> Dict[str, torch.Tensor]:
        """Convert ROS Observation message into a batch dict for SmolVLAPolicy.select_action.

        SmolVLA expects:
        - Images as [0, 1] CHW tensors
        - Language tokens encoding the task description
        """
        # --- Process Cameras ---
        obs = {
            f"observation.images.{camera}": self._img_to_tensor(
                getattr(obs_msg, image_field),
                self.device,
                self.image_scaling,
            )
            for camera, image_field in [
                ("camera1", "center_image"),
                ("camera2", "left_image"),
                ("camera3", "right_image"),
            ]
        }

        state_np = self._build_state_vector(obs_msg)
        raw_state_tensor = torch.from_numpy(state_np).float().unsqueeze(0).to(self.device)
        obs[OBS_STATE] = (raw_state_tensor - self.state_mean) / self.state_std

        # --- Tokenize Language Prompt ---
        language_obs = self._tokenize_prompt(task_text)
        obs.update(language_obs)

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
        self.get_logger().info(f"smolvla_base.insert_cable() enter. Task: {task}")

        port_frame = f"task_board/{task.target_module_name}/{task.port_name}_link"
        cable_tip_frame = f"{task.cable_name}/{task.plug_name}_link"

        # Build task description prompt from task fields
        task_text = (
            f"Insert {task.plug_name} of {task.cable_name} "
            f"into {task.port_name} of {task.target_module_name}"
        )
        self.get_logger().info(f"Task prompt: '{task_text}'")

        start_time = time.time()

        # Run inference for 60 seconds
        while time.time() - start_time < 60.0:
            loop_start = time.time()

            # 1. Get & Process Observation
            observation_msg = get_observation()

            if observation_msg is None:
                self.get_logger().info("No observation received.")
                continue

            obs_batch = self.prepare_observations(observation_msg, task_text)

            # 2. Model Inference
            with torch.inference_mode():
                # Returns shape [action_dim] — one action from the predicted sequence
                normalized_action = self.policy.select_action(obs_batch)

            # 3. Un-normalize Action using the checkpoint's mean/std stats.
            raw_action = normalized_action * self.action_std + self.action_mean
            action = raw_action.squeeze(0).cpu().numpy()

            print("action (numpy): ", action)

            self.get_logger().info(f"Action: {action}")

            # 4. Extract and Command
            # SmolVLA outputs a 6D cartesian twist: linear xyz + angular xyz.
            twist = Twist(
                linear=Vector3(
                    x=float(action[0]), y=float(action[1]), z=float(action[2])
                ),
                angular=Vector3(
                    x=float(action[3]), y=float(action[4]), z=float(action[5])
                ),
            )

            motion_update = self.set_cartesian_twist_target(twist)
            move_robot(motion_update=motion_update)
            send_feedback("in progress...")

            # Maintain control rate (approx 4Hz loop = 0.25s sleep)
            elapsed = time.time() - loop_start
            time.sleep(max(0, 0.25 - elapsed))

        self.get_logger().info("smolvla_base.insert_cable() exiting...")
        return True

    def set_cartesian_twist_target(
        self, twist: Twist, frame_id: str = "base_link"
    ) -> MotionUpdate:
        """Build and publish a cartesian twist MotionUpdate matching the SmolVLA action space.

        SmolVLA was trained on 6D velocity actions, so this sends a twist target
        via ``MODE_VELOCITY``.
        """
        motion_update_msg = MotionUpdate()
        motion_update_msg.header.frame_id = frame_id
        motion_update_msg.header.stamp = self.get_clock().now().to_msg()

        motion_update_msg.velocity = twist

        motion_update_msg.target_stiffness = np.diag(
            [100.0, 100.0, 100.0, 50.0, 50.0, 50.0]
        ).flatten()
        motion_update_msg.target_damping = np.diag(
            [40.0, 40.0, 40.0, 15.0, 15.0, 15.0]
        ).flatten()

        motion_update_msg.feedforward_wrench_at_tip = Wrench(
            force=Vector3(x=0.0, y=0.0, z=0.0), torque=Vector3(x=0.0, y=0.0, z=0.0)
        )

        motion_update_msg.wrench_feedback_gains_at_tip = [0.5, 0.5, 0.5, 0.0, 0.0, 0.0]

        motion_update_msg.trajectory_generation_mode.mode = (
            TrajectoryGenerationMode.MODE_VELOCITY
        )

        # # Publish gripper command — hande_left_finger_joint, right finger is a mimic
        # gripper_msg = JointState()
        # gripper_msg.header.stamp = motion_update_msg.header.stamp
        # gripper_msg.name = ["hande_left_finger_joint"]
        # gripper_msg.position = [gripper_pos]
        # self.gripper_pub.publish(gripper_msg)

        return motion_update_msg