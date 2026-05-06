#!/usr/bin/env python3
"""
CLI framework for recording AIC robot arm datasets to Hugging Face.

launch with 'pixi run python3 recording_framework.py'

"""

from __future__ import annotations

import argparse
import json
import os
import math
import random
import shlex
import re
import signal
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


REPO_IDS = [
    "caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_0",
    "caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_0",
    "caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_1",
    "caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_1",
    "caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_2",
    "caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_2",
    "caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_3",
    "caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_3",
    "caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_4",
    "caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_4",
    "caai-aic/corrected_sc_to_sc_port_base_of_sc_port_0",
    "caai-aic/corrected_sc_to_sc_port_base_of_sc_port_1",
    "caai-aic/test-dataset",
]

AIC_ROOT = Path.home() / "ws_aic_caai" / "src" / "aic"
OCULUS_DIR = AIC_ROOT / "oculus_reader"
HF_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "lerobot"
RMW_IMPLEMENTATION = "rmw_zenoh_cpp"
ZENOH_CONFIG_OVERRIDE = (
    "transport/shared_memory/enabled=true;"
    "transport/shared_memory/transport_optimization/pool_size=536870912"
)

SFP_TASK_TEMPLATE = (
    "Insert sfp_tip of sfp_sc into sfp_port_{port} of nic_card_mount_{mount}"
)
SC_TASK_TEMPLATE = "Insert sc_tip of sfp_sc into sc_port_base of sc_port_{port}"
TEST_TASK_PROMPT = "insert cable"

PRESENCE_PARAM_NAMES = {
    "lc_mount_rail_0_present",
    "sfp_mount_rail_0_present",
    "sc_mount_rail_0_present",
    "lc_mount_rail_1_present",
    "sfp_mount_rail_1_present",
    "sc_mount_rail_1_present",
    "sc_port_0_present",
    "sc_port_1_present",
    "nic_card_mount_0_present",
    "nic_card_mount_1_present",
    "nic_card_mount_2_present",
    "nic_card_mount_3_present",
    "nic_card_mount_4_present",
}

SC_REQUIRED_FOR_REVERSED = {
    "sc_mount_rail_0_present",
    "sc_mount_rail_1_present",
    "sc_port_0_present",
    "sc_port_1_present",
}

SFP_REQUIRED_FOR_NORMAL = {
    "lc_mount_rail_0_present",
    "sfp_mount_rail_0_present",
    "lc_mount_rail_1_present",
    "sfp_mount_rail_1_present",
    "nic_card_mount_0_present",
    "nic_card_mount_1_present",
    "nic_card_mount_2_present",
    "nic_card_mount_3_present",
    "nic_card_mount_4_present",
}

ROBOT_BASE_CENTER_X = 0.0
ROBOT_BASE_CENTER_Y = 0.0
ROBOT_BASE_RADIUS_M = 0.06
TASK_BOARD_HALF_X_M = 0.30 / 2.0
TASK_BOARD_HALF_Y_M = 0.425 / 2.0
TASK_BOARD_CLEARANCE_M = 0.1


@dataclass(frozen=True)
class TaskDefinition:
    repo_id: str
    single_task: str

    @property
    def dataset_root(self) -> Path:
        return HF_CACHE_ROOT / self.repo_id

    @property
    def label(self) -> str:
        return self.repo_id


@dataclass(frozen=True)
class SceneConfig:
    robot_z: float
    robot_roll: float
    robot_pitch: float
    robot_yaw: float

    task_board_x: float
    task_board_y: float
    task_board_z: float
    task_board_roll: float
    task_board_pitch: float
    task_board_yaw: float

    spawn_cable: bool
    cable_type: str
    cable_x: float
    cable_y: float
    cable_z: float
    cable_roll: float
    cable_pitch: float
    cable_yaw: float
    attach_cable_to_gripper: bool

    sfp_mount_rail_0_present: bool
    sfp_mount_rail_0_translation: float
    sfp_mount_rail_0_roll: float
    sfp_mount_rail_0_pitch: float
    sfp_mount_rail_0_yaw: float

    sfp_mount_rail_1_present: bool
    sfp_mount_rail_1_translation: float
    sfp_mount_rail_1_roll: float
    sfp_mount_rail_1_pitch: float
    sfp_mount_rail_1_yaw: float

    sc_mount_rail_0_present: bool
    sc_mount_rail_0_translation: float
    sc_mount_rail_0_roll: float
    sc_mount_rail_0_pitch: float
    sc_mount_rail_0_yaw: float

    sc_mount_rail_1_present: bool
    sc_mount_rail_1_translation: float
    sc_mount_rail_1_roll: float
    sc_mount_rail_1_pitch: float
    sc_mount_rail_1_yaw: float

    lc_mount_rail_0_present: bool
    lc_mount_rail_0_translation: float
    lc_mount_rail_0_roll: float
    lc_mount_rail_0_pitch: float
    lc_mount_rail_0_yaw: float

    lc_mount_rail_1_present: bool
    lc_mount_rail_1_translation: float
    lc_mount_rail_1_roll: float
    lc_mount_rail_1_pitch: float
    lc_mount_rail_1_yaw: float

    nic_card_mount_0_present: bool
    nic_card_mount_0_translation: float
    nic_card_mount_0_roll: float
    nic_card_mount_0_pitch: float
    nic_card_mount_0_yaw: float

    nic_card_mount_1_present: bool
    nic_card_mount_1_translation: float
    nic_card_mount_1_roll: float
    nic_card_mount_1_pitch: float
    nic_card_mount_1_yaw: float

    nic_card_mount_2_present: bool
    nic_card_mount_2_translation: float
    nic_card_mount_2_roll: float
    nic_card_mount_2_pitch: float
    nic_card_mount_2_yaw: float

    nic_card_mount_3_present: bool
    nic_card_mount_3_translation: float
    nic_card_mount_3_roll: float
    nic_card_mount_3_pitch: float
    nic_card_mount_3_yaw: float

    nic_card_mount_4_present: bool
    nic_card_mount_4_translation: float
    nic_card_mount_4_roll: float
    nic_card_mount_4_pitch: float
    nic_card_mount_4_yaw: float

    sc_port_0_present: bool
    sc_port_0_translation: float
    sc_port_0_roll: float
    sc_port_0_pitch: float
    sc_port_0_yaw: float

    sc_port_1_present: bool
    sc_port_1_translation: float
    sc_port_1_roll: float
    sc_port_1_pitch: float
    sc_port_1_yaw: float

    def to_launch_args(self, gazebo_gui: bool = True, launch_rviz: bool = False) -> str:
        args = [
            f"robot_z:={self.robot_z}",
            f"robot_roll:={self.robot_roll}",
            f"robot_pitch:={self.robot_pitch}",
            f"robot_yaw:={self.robot_yaw}",
            "spawn_task_board:=true",
            f"task_board_x:={self.task_board_x}",
            f"task_board_y:={self.task_board_y}",
            f"task_board_z:={self.task_board_z}",
            f"task_board_roll:={self.task_board_roll}",
            f"task_board_pitch:={self.task_board_pitch}",
            f"task_board_yaw:={self.task_board_yaw}",
            f"spawn_cable:={str(self.spawn_cable).lower()}",
            f"gazebo_gui:={str(gazebo_gui).lower()}",
            f"launch_rviz:={str(launch_rviz).lower()}",
            "ground_truth:=true",
        ]

        if self.spawn_cable:
            args.extend([
                f"cable_type:={self.cable_type}",
                f"cable_x:={self.cable_x}",
                f"cable_y:={self.cable_y}",
                f"cable_z:={self.cable_z}",
                f"cable_roll:={self.cable_roll}",
                f"cable_pitch:={self.cable_pitch}",
                f"cable_yaw:={self.cable_yaw}",
                f"attach_cable_to_gripper:={str(self.attach_cable_to_gripper).lower()}",
            ])

        if self.sfp_mount_rail_0_present:
            args.extend([
                "sfp_mount_rail_0_present:=true",
                f"sfp_mount_rail_0_translation:={self.sfp_mount_rail_0_translation}",
                f"sfp_mount_rail_0_roll:={self.sfp_mount_rail_0_roll}",
                f"sfp_mount_rail_0_pitch:={self.sfp_mount_rail_0_pitch}",
                f"sfp_mount_rail_0_yaw:={self.sfp_mount_rail_0_yaw}",
            ])

        if self.sfp_mount_rail_1_present:
            args.extend([
                "sfp_mount_rail_1_present:=true",
                f"sfp_mount_rail_1_translation:={self.sfp_mount_rail_1_translation}",
                f"sfp_mount_rail_1_roll:={self.sfp_mount_rail_1_roll}",
                f"sfp_mount_rail_1_pitch:={self.sfp_mount_rail_1_pitch}",
                f"sfp_mount_rail_1_yaw:={self.sfp_mount_rail_1_yaw}",
            ])

        if self.sc_mount_rail_0_present:
            args.extend([
                "sc_mount_rail_0_present:=true",
                f"sc_mount_rail_0_translation:={self.sc_mount_rail_0_translation}",
                f"sc_mount_rail_0_roll:={self.sc_mount_rail_0_roll}",
                f"sc_mount_rail_0_pitch:={self.sc_mount_rail_0_pitch}",
                f"sc_mount_rail_0_yaw:={self.sc_mount_rail_0_yaw}",
            ])

        if self.sc_mount_rail_1_present:
            args.extend([
                "sc_mount_rail_1_present:=true",
                f"sc_mount_rail_1_translation:={self.sc_mount_rail_1_translation}",
                f"sc_mount_rail_1_roll:={self.sc_mount_rail_1_roll}",
                f"sc_mount_rail_1_pitch:={self.sc_mount_rail_1_pitch}",
                f"sc_mount_rail_1_yaw:={self.sc_mount_rail_1_yaw}",
            ])

        if self.lc_mount_rail_0_present:
            args.extend([
                "lc_mount_rail_0_present:=true",
                f"lc_mount_rail_0_translation:={self.lc_mount_rail_0_translation}",
                f"lc_mount_rail_0_roll:={self.lc_mount_rail_0_roll}",
                f"lc_mount_rail_0_pitch:={self.lc_mount_rail_0_pitch}",
                f"lc_mount_rail_0_yaw:={self.lc_mount_rail_0_yaw}",
            ])

        if self.lc_mount_rail_1_present:
            args.extend([
                "lc_mount_rail_1_present:=true",
                f"lc_mount_rail_1_translation:={self.lc_mount_rail_1_translation}",
                f"lc_mount_rail_1_roll:={self.lc_mount_rail_1_roll}",
                f"lc_mount_rail_1_pitch:={self.lc_mount_rail_1_pitch}",
                f"lc_mount_rail_1_yaw:={self.lc_mount_rail_1_yaw}",
            ])

        if self.nic_card_mount_0_present:
            args.extend([
                "nic_card_mount_0_present:=true",
                f"nic_card_mount_0_translation:={self.nic_card_mount_0_translation}",
                f"nic_card_mount_0_roll:={self.nic_card_mount_0_roll}",
                f"nic_card_mount_0_pitch:={self.nic_card_mount_0_pitch}",
                f"nic_card_mount_0_yaw:={self.nic_card_mount_0_yaw}",
            ])

        if self.nic_card_mount_1_present:
            args.extend([
                "nic_card_mount_1_present:=true",
                f"nic_card_mount_1_translation:={self.nic_card_mount_1_translation}",
                f"nic_card_mount_1_roll:={self.nic_card_mount_1_roll}",
                f"nic_card_mount_1_pitch:={self.nic_card_mount_1_pitch}",
                f"nic_card_mount_1_yaw:={self.nic_card_mount_1_yaw}",
            ])

        if self.nic_card_mount_2_present:
            args.extend([
                "nic_card_mount_2_present:=true",
                f"nic_card_mount_2_translation:={self.nic_card_mount_2_translation}",
                f"nic_card_mount_2_roll:={self.nic_card_mount_2_roll}",
                f"nic_card_mount_2_pitch:={self.nic_card_mount_2_pitch}",
                f"nic_card_mount_2_yaw:={self.nic_card_mount_2_yaw}",
            ])

        if self.nic_card_mount_3_present:
            args.extend([
                "nic_card_mount_3_present:=true",
                f"nic_card_mount_3_translation:={self.nic_card_mount_3_translation}",
                f"nic_card_mount_3_roll:={self.nic_card_mount_3_roll}",
                f"nic_card_mount_3_pitch:={self.nic_card_mount_3_pitch}",
                f"nic_card_mount_3_yaw:={self.nic_card_mount_3_yaw}",
            ])

        if self.nic_card_mount_4_present:
            args.extend([
                "nic_card_mount_4_present:=true",
                f"nic_card_mount_4_translation:={self.nic_card_mount_4_translation}",
                f"nic_card_mount_4_roll:={self.nic_card_mount_4_roll}",
                f"nic_card_mount_4_pitch:={self.nic_card_mount_4_pitch}",
                f"nic_card_mount_4_yaw:={self.nic_card_mount_4_yaw}",
            ])

        if self.sc_port_0_present:
            args.extend([
                "sc_port_0_present:=true",
                f"sc_port_0_translation:={self.sc_port_0_translation}",
                f"sc_port_0_roll:={self.sc_port_0_roll}",
                f"sc_port_0_pitch:={self.sc_port_0_pitch}",
                f"sc_port_0_yaw:={self.sc_port_0_yaw}",
            ])

        if self.sc_port_1_present:
            args.extend([
                "sc_port_1_present:=true",
                f"sc_port_1_translation:={self.sc_port_1_translation}",
                f"sc_port_1_roll:={self.sc_port_1_roll}",
                f"sc_port_1_pitch:={self.sc_port_1_pitch}",
                f"sc_port_1_yaw:={self.sc_port_1_yaw}",
            ])

        return " ".join(args)


class SceneGenerator:
    def __init__(
        self,
        enabled_presence_params: Optional[Iterable[str]] = None,
        allowed_cable_types: Optional[List[str]] = None,
    ) -> None:
        self.used_configs: List[str] = []
        self.enabled_presence_params = (
            set(PRESENCE_PARAM_NAMES)
            if enabled_presence_params is None
            else set(enabled_presence_params)
        )
        self.allowed_cable_types = (
            ["sfp_sc_cable", "sfp_sc_cable_reversed"]
            if not allowed_cable_types
            else list(allowed_cable_types)
        )
        self._validate_generation_constraints()

    def _validate_generation_constraints(self) -> None:
        invalid_presence = self.enabled_presence_params - PRESENCE_PARAM_NAMES
        if invalid_presence:
            raise ValueError(
                "Unknown presence parameters in enabled list: "
                f"{sorted(invalid_presence)}"
            )

        invalid_cables = set(self.allowed_cable_types) - {
            "sfp_sc_cable",
            "sfp_sc_cable_reversed",
        }
        if invalid_cables:
            raise ValueError(
                "Unknown cable types in allowed list: "
                f"{sorted(invalid_cables)}"
            )

        if "sfp_sc_cable_reversed" in self.allowed_cable_types and not (
            self.enabled_presence_params & SC_REQUIRED_FOR_REVERSED
        ):
            raise ValueError(
                "Configuration impossible: 'sfp_sc_cable_reversed' requires at least "
                "one enabled parameter from sc_mount_rail_0_present, "
                "sc_mount_rail_1_present, sc_port_0_present, sc_port_1_present."
            )

        if "sfp_sc_cable" in self.allowed_cable_types and not (
            self.enabled_presence_params & SFP_REQUIRED_FOR_NORMAL
        ):
            raise ValueError(
                "Configuration impossible: 'sfp_sc_cable' requires at least one "
                "enabled parameter from lc/sfp rails or nic_card mounts."
            )

    def _randomize_presence(self, name: str) -> bool:
        if name in self.enabled_presence_params:
            return True
        return random.choice([True, False])

    def _task_board_intersects_robot_base(
        self,
        task_board_x: float,
        task_board_y: float,
        task_board_yaw: float,
    ) -> bool:
        dx = task_board_x - ROBOT_BASE_CENTER_X
        dy = task_board_y - ROBOT_BASE_CENTER_Y
        cos_yaw = math.cos(task_board_yaw)
        sin_yaw = math.sin(task_board_yaw)
        local_x = cos_yaw * dx + sin_yaw * dy
        local_y = -sin_yaw * dx + cos_yaw * dy
        clamped_x = max(-TASK_BOARD_HALF_X_M, min(local_x, TASK_BOARD_HALF_X_M))
        clamped_y = max(-TASK_BOARD_HALF_Y_M, min(local_y, TASK_BOARD_HALF_Y_M))
        dist_x = local_x - clamped_x
        dist_y = local_y - clamped_y
        radius = ROBOT_BASE_RADIUS_M + TASK_BOARD_CLEARANCE_M
        return (dist_x * dist_x + dist_y * dist_y) <= (radius * radius)

    def generate_random_config(self) -> SceneConfig:
        max_attempts = 1000

        for _ in range(max_attempts):
            robot_z = 1.14
            robot_roll = 0.0
            robot_pitch = 0.0
            robot_yaw = -3.141

            task_board_x = random.uniform(0, 0.3)
            task_board_y = random.uniform(-0.3, 0.3)
            task_board_z = 1.14
            task_board_roll = 0.0
            task_board_pitch = 0.0
            task_board_yaw = random.uniform(-math.pi, math.pi)

            if self._task_board_intersects_robot_base(
                task_board_x,
                task_board_y,
                task_board_yaw,
            ):
                continue

            spawn_cable = True
            cable_type = random.choice(self.allowed_cable_types)
            cable_x_mean = 0.172
            cable_y_mean = 0.024
            cable_z_mean = 1.508 if cable_type == "sfp_sc_cable_reversed" else 1.518
            cable_roll_mean = 0.4432
            cable_pitch_mean = -0.48
            cable_yaw_mean = 1.3303
            attach_cable_to_gripper = True

            cable_x = random.uniform(cable_x_mean - 0.002, cable_x_mean + 0.002)
            cable_y = random.uniform(cable_y_mean - 0.002, cable_y_mean + 0.002)
            cable_z = random.uniform(cable_z_mean - 0.002, cable_z_mean + 0.002)
            cable_roll = random.uniform(cable_roll_mean - 0.04, cable_roll_mean + 0.04)
            cable_pitch = random.uniform(cable_pitch_mean - 0.04, cable_pitch_mean + 0.04)
            cable_yaw = random.uniform(cable_yaw_mean - 0.04, cable_yaw_mean + 0.04)

            lc_mount_rail_0_present = self._randomize_presence("lc_mount_rail_0_present")
            lc_mount_rail_0_translation = random.uniform(-0.09625, 0.09625)
            lc_mount_rail_0_roll = 0.0
            lc_mount_rail_0_pitch = 0.0
            lc_mount_rail_0_yaw = random.uniform(-1.047, 1.047)

            sfp_mount_rail_0_present = self._randomize_presence("sfp_mount_rail_0_present")
            sfp_mount_rail_0_translation = random.uniform(-0.09625, 0.09625)
            sfp_mount_rail_0_roll = 0.0
            sfp_mount_rail_0_pitch = 0.0
            sfp_mount_rail_0_yaw = random.uniform(-1.047, 1.047)

            sc_mount_rail_0_present = self._randomize_presence("sc_mount_rail_0_present")
            sc_mount_rail_0_translation = random.uniform(-0.09625, 0.09625)
            sc_mount_rail_0_roll = 0.0
            sc_mount_rail_0_pitch = 0.0
            sc_mount_rail_0_yaw = random.uniform(-1.047, 1.047)

            lc_mount_rail_1_present = self._randomize_presence("lc_mount_rail_1_present")
            lc_mount_rail_1_translation = random.uniform(-0.09625, 0.09625)
            lc_mount_rail_1_roll = 0.0
            lc_mount_rail_1_pitch = 0.0
            lc_mount_rail_1_yaw = random.uniform(-1.047, 1.047)

            sfp_mount_rail_1_present = self._randomize_presence("sfp_mount_rail_1_present")
            sfp_mount_rail_1_translation = random.uniform(-0.09625, 0.09625)
            sfp_mount_rail_1_roll = 0.0
            sfp_mount_rail_1_pitch = 0.0
            sfp_mount_rail_1_yaw = random.uniform(-1.047, 1.047)

            sc_mount_rail_1_present = self._randomize_presence("sc_mount_rail_1_present")
            sc_mount_rail_1_translation = random.uniform(-0.09625, 0.09625)
            sc_mount_rail_1_roll = 0.0
            sc_mount_rail_1_pitch = 0.0
            sc_mount_rail_1_yaw = random.uniform(-1.047, 1.047)

            sc_port_0_present = self._randomize_presence("sc_port_0_present")
            sc_port_0_translation = random.uniform(-0.06, 0.055)
            sc_port_0_roll = 0.0
            sc_port_0_pitch = 0.0
            sc_port_0_yaw = 0.0

            sc_port_1_present = self._randomize_presence("sc_port_1_present")
            sc_port_1_translation = random.uniform(-0.06, 0.055)
            sc_port_1_roll = 0.0
            sc_port_1_pitch = 0.0
            sc_port_1_yaw = 0.0

            nic_card_mount_0_present = self._randomize_presence("nic_card_mount_0_present")
            nic_card_mount_0_translation = random.uniform(-0.0215, 0.0234)
            nic_card_mount_0_roll = 0.0
            nic_card_mount_0_pitch = 0.0
            nic_card_mount_0_yaw = random.uniform(-0.175, 0.175)

            nic_card_mount_1_present = self._randomize_presence("nic_card_mount_1_present")
            nic_card_mount_1_translation = random.uniform(-0.0215, 0.0234)
            nic_card_mount_1_roll = 0.0
            nic_card_mount_1_pitch = 0.0
            nic_card_mount_1_yaw = random.uniform(-0.175, 0.175)

            nic_card_mount_2_present = self._randomize_presence("nic_card_mount_2_present")
            nic_card_mount_2_translation = random.uniform(-0.0215, 0.0234)
            nic_card_mount_2_roll = 0.0
            nic_card_mount_2_pitch = 0.0
            nic_card_mount_2_yaw = random.uniform(-0.175, 0.175)

            nic_card_mount_3_present = self._randomize_presence("nic_card_mount_3_present")
            nic_card_mount_3_translation = random.uniform(-0.0215, 0.0234)
            nic_card_mount_3_roll = 0.0
            nic_card_mount_3_pitch = 0.0
            nic_card_mount_3_yaw = random.uniform(-0.175, 0.175)

            nic_card_mount_4_present = self._randomize_presence("nic_card_mount_4_present")
            nic_card_mount_4_translation = random.uniform(-0.0215, 0.0234)
            nic_card_mount_4_roll = 0.0
            nic_card_mount_4_pitch = 0.0
            nic_card_mount_4_yaw = random.uniform(-0.175, 0.175)

            if cable_type == "sfp_sc_cable_reversed":
                while not (
                    sc_mount_rail_0_present
                    or sc_mount_rail_1_present
                    or sc_port_0_present
                    or sc_port_1_present
                ):
                    sc_mount_rail_0_present = self._randomize_presence(
                        "sc_mount_rail_0_present"
                    )
                    sc_mount_rail_1_present = self._randomize_presence(
                        "sc_mount_rail_1_present"
                    )
                    sc_port_0_present = self._randomize_presence("sc_port_0_present")
                    sc_port_1_present = self._randomize_presence("sc_port_1_present")

            if cable_type == "sfp_sc_cable":
                while not (
                    lc_mount_rail_0_present
                    or sfp_mount_rail_0_present
                    or lc_mount_rail_1_present
                    or sfp_mount_rail_1_present
                    or nic_card_mount_0_present
                    or nic_card_mount_1_present
                    or nic_card_mount_2_present
                    or nic_card_mount_3_present
                    or nic_card_mount_4_present
                ):
                    lc_mount_rail_0_present = self._randomize_presence(
                        "lc_mount_rail_0_present"
                    )
                    sfp_mount_rail_0_present = self._randomize_presence(
                        "sfp_mount_rail_0_present"
                    )
                    lc_mount_rail_1_present = self._randomize_presence(
                        "lc_mount_rail_1_present"
                    )
                    sfp_mount_rail_1_present = self._randomize_presence(
                        "sfp_mount_rail_1_present"
                    )
                    nic_card_mount_0_present = self._randomize_presence(
                        "nic_card_mount_0_present"
                    )
                    nic_card_mount_1_present = self._randomize_presence(
                        "nic_card_mount_1_present"
                    )
                    nic_card_mount_2_present = self._randomize_presence(
                        "nic_card_mount_2_present"
                    )
                    nic_card_mount_3_present = self._randomize_presence(
                        "nic_card_mount_3_present"
                    )
                    nic_card_mount_4_present = self._randomize_presence(
                        "nic_card_mount_4_present"
                    )

            config = SceneConfig(
                robot_z=robot_z,
                robot_roll=robot_roll,
                robot_pitch=robot_pitch,
                robot_yaw=robot_yaw,
                task_board_x=task_board_x,
                task_board_y=task_board_y,
                task_board_z=task_board_z,
                task_board_roll=task_board_roll,
                task_board_pitch=task_board_pitch,
                task_board_yaw=task_board_yaw,
                spawn_cable=spawn_cable,
                cable_type=cable_type,
                cable_x=cable_x,
                cable_y=cable_y,
                cable_z=cable_z,
                cable_roll=cable_roll,
                cable_pitch=cable_pitch,
                cable_yaw=cable_yaw,
                attach_cable_to_gripper=attach_cable_to_gripper,
                sfp_mount_rail_0_present=sfp_mount_rail_0_present,
                sfp_mount_rail_0_translation=sfp_mount_rail_0_translation,
                sfp_mount_rail_0_roll=sfp_mount_rail_0_roll,
                sfp_mount_rail_0_pitch=sfp_mount_rail_0_pitch,
                sfp_mount_rail_0_yaw=sfp_mount_rail_0_yaw,
                sfp_mount_rail_1_present=sfp_mount_rail_1_present,
                sfp_mount_rail_1_translation=sfp_mount_rail_1_translation,
                sfp_mount_rail_1_roll=sfp_mount_rail_1_roll,
                sfp_mount_rail_1_pitch=sfp_mount_rail_1_pitch,
                sfp_mount_rail_1_yaw=sfp_mount_rail_1_yaw,
                sc_mount_rail_0_present=sc_mount_rail_0_present,
                sc_mount_rail_0_translation=sc_mount_rail_0_translation,
                sc_mount_rail_0_roll=sc_mount_rail_0_roll,
                sc_mount_rail_0_pitch=sc_mount_rail_0_pitch,
                sc_mount_rail_0_yaw=sc_mount_rail_0_yaw,
                sc_mount_rail_1_present=sc_mount_rail_1_present,
                sc_mount_rail_1_translation=sc_mount_rail_1_translation,
                sc_mount_rail_1_roll=sc_mount_rail_1_roll,
                sc_mount_rail_1_pitch=sc_mount_rail_1_pitch,
                sc_mount_rail_1_yaw=sc_mount_rail_1_yaw,
                lc_mount_rail_0_present=lc_mount_rail_0_present,
                lc_mount_rail_0_translation=lc_mount_rail_0_translation,
                lc_mount_rail_0_roll=lc_mount_rail_0_roll,
                lc_mount_rail_0_pitch=lc_mount_rail_0_pitch,
                lc_mount_rail_0_yaw=lc_mount_rail_0_yaw,
                lc_mount_rail_1_present=lc_mount_rail_1_present,
                lc_mount_rail_1_translation=lc_mount_rail_1_translation,
                lc_mount_rail_1_roll=lc_mount_rail_1_roll,
                lc_mount_rail_1_pitch=lc_mount_rail_1_pitch,
                lc_mount_rail_1_yaw=lc_mount_rail_1_yaw,
                nic_card_mount_0_present=nic_card_mount_0_present,
                nic_card_mount_0_translation=nic_card_mount_0_translation,
                nic_card_mount_0_roll=nic_card_mount_0_roll,
                nic_card_mount_0_pitch=nic_card_mount_0_pitch,
                nic_card_mount_0_yaw=nic_card_mount_0_yaw,
                nic_card_mount_1_present=nic_card_mount_1_present,
                nic_card_mount_1_translation=nic_card_mount_1_translation,
                nic_card_mount_1_roll=nic_card_mount_1_roll,
                nic_card_mount_1_pitch=nic_card_mount_1_pitch,
                nic_card_mount_1_yaw=nic_card_mount_1_yaw,
                nic_card_mount_2_present=nic_card_mount_2_present,
                nic_card_mount_2_translation=nic_card_mount_2_translation,
                nic_card_mount_2_roll=nic_card_mount_2_roll,
                nic_card_mount_2_pitch=nic_card_mount_2_pitch,
                nic_card_mount_2_yaw=nic_card_mount_2_yaw,
                nic_card_mount_3_present=nic_card_mount_3_present,
                nic_card_mount_3_translation=nic_card_mount_3_translation,
                nic_card_mount_3_roll=nic_card_mount_3_roll,
                nic_card_mount_3_pitch=nic_card_mount_3_pitch,
                nic_card_mount_3_yaw=nic_card_mount_3_yaw,
                nic_card_mount_4_present=nic_card_mount_4_present,
                nic_card_mount_4_translation=nic_card_mount_4_translation,
                nic_card_mount_4_roll=nic_card_mount_4_roll,
                nic_card_mount_4_pitch=nic_card_mount_4_pitch,
                nic_card_mount_4_yaw=nic_card_mount_4_yaw,
                sc_port_0_present=sc_port_0_present,
                sc_port_0_translation=sc_port_0_translation,
                sc_port_0_roll=sc_port_0_roll,
                sc_port_0_pitch=sc_port_0_pitch,
                sc_port_0_yaw=sc_port_0_yaw,
                sc_port_1_present=sc_port_1_present,
                sc_port_1_translation=sc_port_1_translation,
                sc_port_1_roll=sc_port_1_roll,
                sc_port_1_pitch=sc_port_1_pitch,
                sc_port_1_yaw=sc_port_1_yaw,
            )

            config_id = str(config)
            if config_id not in self.used_configs:
                self.used_configs.append(config_id)
                return config

        raise RuntimeError(
            f"Could not generate unique config after {max_attempts} attempts"
        )


@dataclass
class SceneProcess:
    process: Optional[subprocess.Popen]
    detached: bool = True

    def stop(self, timeout: int = 20) -> None:
        if self.process is None:
            return
        if self.process.poll() is not None:
            return
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait()


@dataclass
class VRTeleopProcess:
    process: subprocess.Popen

    def stop(self, timeout: int = 10) -> None:
        if self.process.poll() is not None:
            return
        try:
            self.process.terminate()
            self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


@dataclass
class RecordingResult:
    completed_episodes: int
    exit_code: int


class DatasetInfoFetcher:
    def __init__(self, hf_token: Optional[str] = None):
        self.hf_token = hf_token
        self._hf_api = None

    def _get_hf_api(self):
        if self._hf_api is None:
            try:
                from huggingface_hub import HfApi
            except Exception as exc:
                raise RuntimeError(
                    "huggingface_hub is required to fetch dataset info"
                ) from exc
            self._hf_api = HfApi(token=self.hf_token)
        return self._hf_api

    def fetch_episode_count(self, repo_id: str) -> Optional[int]:
        try:
            return self._fetch_episode_count(repo_id)
        except Exception as exc:
            print(f"[warn] Could not fetch info for {repo_id}: {exc}")
            return None

    def _fetch_episode_count(self, repo_id: str) -> Optional[int]:
        api = self._get_hf_api()
        info = api.dataset_info(repo_id=repo_id)
        if info.card_data:
            for key in ("num_episodes", "episodes", "episode_count"):
                if key in info.card_data:
                    try:
                        return int(info.card_data[key])
                    except (TypeError, ValueError):
                        pass

        files = api.list_repo_files(repo_id=repo_id, repo_type="dataset")
        json_candidates = [
            "episodes.json",
            "episode_index.json",
            "meta.json",
            "metadata.json",
        ]
        for filename in json_candidates:
            if filename in files:
                data = _download_json(repo_id, filename, self.hf_token)
                if data is None:
                    continue
                for key in ("num_episodes", "episodes"):
                    if key in data:
                        try:
                            return int(data[key])
                        except (TypeError, ValueError):
                            pass
                if isinstance(data, list):
                    return len(data)

        parquet_candidates = [
            "episode_index.parquet",
            "episode_index/episode_index.parquet",
        ]
        for filename in parquet_candidates:
            if filename in files:
                count = _count_episodes_from_parquet(
                    repo_id, filename, self.hf_token
                )
                if count is not None:
                    return count

        return _fallback_count_with_datasets(repo_id)


@dataclass
class RecordingTask:
    definition: TaskDefinition

    def lerobot_command(self, num_episodes: int) -> List[str]:
        return [
            "pixi",
            "run",
            "lerobot-record",
            "--robot.type=aic_controller",
            "--robot.id=aic",
            "--teleop.type=aic_oculus",
            "--teleop.id=aic",
            "--robot.teleop_target_mode=cartesian",
            "--robot.cartesian_command_mode=position",
            "--teleop.cartesian_command_mode=position",
            "--robot.teleop_frame_id=base_link",
            "--dataset.push_to_hub=true",
            "--dataset.private=true",
            f"--dataset.num_episodes={num_episodes}",
            "--play_sounds=false",
            "--display_data=true",
            "--dataset.reset_time_s=30",
            "--dataset.episode_time_s=600",
            "--resume=true",
            f"--dataset.repo_id={self.definition.repo_id}",
            f"--dataset.single_task={self.definition.single_task}",
            f"--dataset.root={self.definition.dataset_root}",
        ]


def _download_json(
    repo_id: str, filename: str, token: Optional[str]
) -> Optional[dict]:
    try:
        from huggingface_hub import hf_hub_download
    except Exception:
        return None

    try:
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            token=token,
        )
    except Exception:
        return None

    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None


def _count_episodes_from_parquet(
    repo_id: str, filename: str, token: Optional[str]
) -> Optional[int]:
    try:
        from huggingface_hub import hf_hub_download
    except Exception:
        return None

    try:
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            token=token,
        )
    except Exception:
        return None

    columns = ["episode_index", "episode_id", "episode"]
    try:
        import pandas as pd

        df = pd.read_parquet(path, columns=columns)
        for column in columns:
            if column in df.columns:
                return int(df[column].nunique())
    except Exception:
        pass

    try:
        import pyarrow.parquet as pq

        table = pq.read_table(path, columns=columns)
        for column in columns:
            if column in table.column_names:
                return int(table.column(column).unique().length())
    except Exception:
        return None

    return None


def _fallback_count_with_datasets(repo_id: str) -> Optional[int]:
    try:
        from datasets import load_dataset
    except Exception:
        return None

    try:
        dataset = load_dataset(repo_id, split="train", streaming=True)
    except Exception:
        return None

    episode_keys = ["episode_index", "episode_id", "episode"]
    seen = set()
    limit = 500000
    count = 0
    for idx, row in enumerate(dataset):
        for key in episode_keys:
            if key in row:
                seen.add(row[key])
                break
        else:
            count += 1

        if idx + 1 >= limit:
            break
    if seen:
        return len(seen)
    if count:
        return count
    return None


def build_tasks() -> List[RecordingTask]:
    tasks: List[RecordingTask] = []
    for mount in range(5):
        for port in range(2):
            repo_id = (
                "caai-aic/corrected_sfp_to_sfp_port_"
                f"{port}_of_nic_card_mount_{mount}"
            )
            tasks.append(
                RecordingTask(
                    TaskDefinition(
                        repo_id=repo_id,
                        single_task=SFP_TASK_TEMPLATE.format(
                            port=port, mount=mount
                        ),
                    )
                )
            )

    for port in range(2):
        repo_id = f"caai-aic/corrected_sc_to_sc_port_base_of_sc_port_{port}"
        tasks.append(
            RecordingTask(
                TaskDefinition(
                    repo_id=repo_id,
                    single_task=SC_TASK_TEMPLATE.format(port=port),
                )
            )
        )

    tasks.append(
        RecordingTask(
            TaskDefinition(
                repo_id="caai-aic/test-dataset",
                single_task=TEST_TASK_PROMPT,
            )
        )
    )

    return tasks


def prompt_connect_quest() -> None:
    print("Connect the Quest 3 headset, then press Enter to continue.")
    input("→ ")


def start_vr_teleop() -> VRTeleopProcess:
    command = "pixi run python3 oculus_reader/viz_transforms.py"
    process = _launch_terminal(command, title="AIC VR Teleop", cwd=OCULUS_DIR)
    print("[info] VR teleop launched in a new terminal.")
    return VRTeleopProcess(process=process)


def build_scene_generator() -> SceneGenerator:
    return SceneGenerator()


def start_scene(launch_args: str, ws_path: Path) -> SceneProcess:
    launch_cmd = f"/entrypoint.sh {launch_args} start_aic_engine:=false"
    print(f"[info] Scene launch command: {launch_cmd}")
    command = (
        "export DBX_CONTAINER_MANAGER=docker; "
        f"distrobox enter -r aic_eval -- {launch_cmd}"
    )
    process = _launch_terminal(command, title="AIC Scene", cwd=ws_path)
    print("[info] Scene launch started in a new terminal.")
    return SceneProcess(process=process, detached=True)


def wait_for_scene_ready(
    ws_path: Path,
    scene: SceneProcess,
    timeout_s: int = 300,
) -> bool:
    print("[info] Waiting for Gazebo to fully load...")
    deadline = time.time() + timeout_s
    poll_interval = 5
    attempt = 0
    gz_ready_count = 0
    sdf_ready_count = 0
    while time.time() < deadline:
        if not scene.detached and scene.process is not None:
            if scene.process.poll() is not None:
                print(
                    "[warn] Scene process exited with code "
                    f"{scene.process.returncode}"
                )
                return False
        attempt += 1
        gz_cmd = (
            "export DBX_CONTAINER_MANAGER=docker; "
            "distrobox enter -r aic_eval -- pgrep -f gzserver"
        )
        gz_running = False
        try:
            gz_result = subprocess.run(
                ["bash", "-c", gz_cmd],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if gz_result.returncode == 0 and gz_result.stdout.strip():
                gz_running = True
        except subprocess.TimeoutExpired:
            gz_running = False

        sdf_ready = Path("/tmp/aic.sdf").exists()

        if gz_running:
            gz_ready_count += 1
            if gz_ready_count >= 3:
                print("[info] Gazebo is ready (gzserver running).")
                return True
        else:
            gz_ready_count = 0

        if sdf_ready:
            sdf_ready_count += 1
            if sdf_ready_count >= 3:
                print("[info] Gazebo is ready (SDF exported).")
                return True
        else:
            sdf_ready_count = 0
            print(
                f"[info] Gazebo not ready yet (attempt {attempt}); "
                "gzserver/SDF not detected"
            )

        time.sleep(poll_interval)

    print("[warn] Timed out waiting for Gazebo readiness.")
    return False


def choose_task(
    tasks: List[RecordingTask],
    episode_counts: Dict[str, Optional[int]],
) -> Optional[RecordingTask]:
    print("\nAvailable datasets:")
    for idx, task in enumerate(tasks, start=1):
        repo_id = task.definition.repo_id
        count = episode_counts.get(repo_id)
        suffix = ""
        if count is not None:
            remaining = max(0, 100 - count)
            if remaining:
                suffix = f" (episodes: {count}, left to 100: {remaining})"
            else:
                suffix = f" (episodes: {count})"
        else:
            suffix = " (episodes: unknown)"
        print(f"  [{idx}] {repo_id}{suffix}")
    print("  [q] Quit")

    while True:
        choice = input("Select a task: ").strip().lower()
        if choice in {"q", "quit", "exit"}:
            return None
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(tasks):
                return tasks[index - 1]
        print("Invalid selection. Try again.")


def prompt_num_episodes() -> int:
    while True:
        value = input("Number of episodes to record: ").strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Enter a positive integer.")


def run_recording(
    task: RecordingTask,
    num_episodes: int,
    start_episode_count: Optional[int],
) -> RecordingResult:
    cmd = " ".join(shlex.quote(arg) for arg in task.lerobot_command(num_episodes))
    _launch_terminal(cmd, title="LeRobot Record", cwd=AIC_ROOT)
    print("[info] Recording launched in a new terminal.")
    input("Press Enter here after recording finishes to continue... ")
    return RecordingResult(completed_episodes=num_episodes, exit_code=0)


def _launch_terminal(command: str, title: str, cwd: Path) -> subprocess.Popen:
    terminal_cmd = [
        "gnome-terminal",
        f"--title={title}",
        "--",
        "bash",
        "-lc",
        f"cd {shlex.quote(str(cwd))} && {command}; exec bash",
    ]
    try:
        return subprocess.Popen(terminal_cmd)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "gnome-terminal is required to launch new terminals."
        ) from exc


def read_hf_token(path: Optional[Path]) -> Optional[str]:
    if path is None:
        return None
    if not path.exists():
        print(f"[warn] HF token path not found: {path}")
        return None
    return path.read_text(encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record AIC datasets with VR teleop and HF sync."
    )
    parser.add_argument(
        "--ws-path",
        type=Path,
        default=AIC_ROOT,
        help="Path to ws_aic_caai/src/aic",
    )
    parser.add_argument(
        "--hf-token-path",
        type=Path,
        default=None,
        help="Optional Hugging Face token path",
    )
    args = parser.parse_args()

    ws_path = args.ws_path
    if not ws_path.exists():
        print(f"Workspace path not found: {ws_path}")
        return 1

    hf_token = read_hf_token(args.hf_token_path)
    fetcher = DatasetInfoFetcher(hf_token=hf_token)

    prompt_connect_quest()
    vr_process = start_vr_teleop()

    scene_generator = build_scene_generator()
    print("[info] Scene generator initialized.")

    print("[info] Updating task list...")
    tasks = build_tasks()

    try:
        while True:
            episode_counts = {
                task.definition.repo_id: fetcher.fetch_episode_count(
                    task.definition.repo_id
                )
                for task in tasks
            }

            task = choose_task(tasks, episode_counts)
            if task is None:
                break

            num_episodes = prompt_num_episodes()

            config = scene_generator.generate_random_config()
            launch_args = config.to_launch_args(gazebo_gui=True, launch_rviz=False)
            scene = start_scene(launch_args, ws_path)
            ready = wait_for_scene_ready(ws_path, scene)
            if not ready:
                scene.stop()
                print("[warn] Scene did not start; returning to menu.")
                continue

            start_count = episode_counts.get(task.definition.repo_id)
            result = run_recording(task, num_episodes, start_count)
            print(
                f"[info] Recording finished with code {result.exit_code}; "
                f"episodes completed: {result.completed_episodes}"
            )

            scene.stop()
            print("[info] Scene stopped.")

            print("[info] Refreshing dataset info...")

    except KeyboardInterrupt:
        print("\n[info] Interrupted by user.")
    finally:
        vr_process.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
