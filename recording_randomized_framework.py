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
import shutil
import re
import signal
import tempfile
import select
import subprocess
import sys
import threading
import time
import termios
import tty
from collections import deque
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REPO_IDS = [
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_0",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_0",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_1",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_1",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_2",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_2",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_3",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_3",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_4",
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_4",
    "caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_0",
    "caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_1",
]

AIC_ROOT = Path.home() / "ws_aic_caai" / "src" / "aic"
HF_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "lerobot"
HF_HUB_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "hub"
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

DATASET_SCENE_OVERRIDES = {
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_0": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_0_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_0": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_0_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_1": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_1_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_1": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_1_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_2": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_2_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_2": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_2_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_3": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_3_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_3": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_3_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_4": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_4_present": True,
    },
    "caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_4": {
        "cable_type": "sfp_sc_cable",
        "nic_card_mount_4_present": True,
    },
    "caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_0": {
        "cable_type": "sfp_sc_cable_reversed",
        "sc_port_0_present": True,
    },
    "caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_1": {
        "cable_type": "sfp_sc_cable_reversed",
        "sc_port_1_present": True,
    },
}

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

    # Cheatcode teleop target: which cable, plug end, module, and port were
    # selected as the insertion goal for this scene. Populated by
    # generate_random_config so callers can pass them straight to lerobot-record.
    task_cable_name: str
    task_plug_name: str
    task_module_name: str
    task_port_name: str

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
        # if name in self.enabled_presence_params:
        #     return True
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

    def generate_random_config(self, target: Optional[dict] = None) -> SceneConfig:
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
            cable_type = target["cable_type"] if target is not None else random.choice(self.allowed_cable_types)
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

            # --- Target selection ---
            task_cable_name = "cable_0"
            if target is not None:
                task_plug_name = target["task_plug_name"]
                task_module_name = target["task_module_name"]
                task_port_name = target["task_port_name"]
                # Force the target component present regardless of random flags.
                if task_module_name == "nic_card_mount_0":
                    nic_card_mount_0_present = True
                elif task_module_name == "nic_card_mount_1":
                    nic_card_mount_1_present = True
                elif task_module_name == "nic_card_mount_2":
                    nic_card_mount_2_present = True
                elif task_module_name == "nic_card_mount_3":
                    nic_card_mount_3_present = True
                elif task_module_name == "nic_card_mount_4":
                    nic_card_mount_4_present = True
                elif task_module_name == "sc_port_0":
                    sc_port_0_present = True
                elif task_module_name == "sc_port_1":
                    sc_port_1_present = True
            elif cable_type == "sfp_sc_cable":
                task_plug_name = "sfp_tip"
                nic_flags = [
                    ("nic_card_mount_0", nic_card_mount_0_present),
                    ("nic_card_mount_1", nic_card_mount_1_present),
                    ("nic_card_mount_2", nic_card_mount_2_present),
                    ("nic_card_mount_3", nic_card_mount_3_present),
                    ("nic_card_mount_4", nic_card_mount_4_present),
                ]
                present_nic = [name for name, p in nic_flags if p]
                if not present_nic:
                    forced = random.choice([name for name, _ in nic_flags])
                    if forced == "nic_card_mount_0":
                        nic_card_mount_0_present = True
                    elif forced == "nic_card_mount_1":
                        nic_card_mount_1_present = True
                    elif forced == "nic_card_mount_2":
                        nic_card_mount_2_present = True
                    elif forced == "nic_card_mount_3":
                        nic_card_mount_3_present = True
                    else:
                        nic_card_mount_4_present = True
                    present_nic = [forced]
                task_module_name = random.choice(present_nic)
                task_port_name = random.choice(["sfp_port_0", "sfp_port_1"])
            else:
                task_plug_name = "sc_tip"
                sc_flags = [
                    ("sc_port_0", sc_port_0_present),
                    ("sc_port_1", sc_port_1_present),
                ]
                present_sc = [name for name, p in sc_flags if p]
                if not present_sc:
                    forced = random.choice([name for name, _ in sc_flags])
                    if forced == "sc_port_0":
                        sc_port_0_present = True
                    else:
                        sc_port_1_present = True
                    present_sc = [forced]
                task_module_name = random.choice(present_sc)
                task_port_name = "sc_port_base"

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
                task_cable_name=task_cable_name,
                task_plug_name=task_plug_name,
                task_module_name=task_module_name,
                task_port_name=task_port_name,
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
            local_count = _find_episode_count_in_local_cache(repo_id)
            if local_count is not None:
                return local_count
            if not _has_local_cache(repo_id):
                _ensure_local_dataset_cache(repo_id, self.hf_token)
                local_count = _find_episode_count_in_local_cache(repo_id)
                if local_count is not None:
                    return local_count
            return self._fetch_episode_count(repo_id)
        except Exception as exc:
            print(f"[warn] Could not fetch info for {repo_id}: {exc}")
            return None

    def _fetch_episode_count(self, repo_id: str) -> Optional[int]:
        api = self._get_hf_api()
        info = api.dataset_info(repo_id=repo_id)
        if info.card_data:
            for key in ("total_episodes", "num_episodes", "episodes", "episode_count"):
                if key in info.card_data:
                    try:
                        return int(info.card_data[key])
                    except (TypeError, ValueError):
                        pass

        files = api.list_repo_files(repo_id=repo_id, repo_type="dataset")
        if files and all(name == ".gitattributes" for name in files):
            return 0
        json_candidates = [
            "episodes.json",
            "episode_index.json",
            "meta.json",
            "metadata.json",
            "meta/info.json",
            "meta/stats.json",
        ]
        for filename in json_candidates:
            if filename in files:
                data = _download_json(repo_id, filename, self.hf_token)
                if data is None:
                    continue
                for key in ("total_episodes", "num_episodes", "episodes"):
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

    def _should_resume(self) -> bool:
        info_path = self.definition.dataset_root / "meta" / "info.json"
        if not info_path.exists():
            return False
        try:
            info = json.loads(info_path.read_text())
            return int(info.get("total_episodes", 0)) > 0
        except Exception:
            return False

    def prepare_dataset_root(self) -> None:
        root = self.definition.dataset_root
        if self._should_resume():
            return  # valid dataset with at least one episode — keep it
        if root.exists():
            shutil.rmtree(root)  # partial or empty state — wipe so lerobot starts fresh

    def cheatcode_lerobot_command(
        self, num_episodes: int, config: "SceneConfig", push_to_hub: bool = False, display_data: bool = True
    ) -> List[str]:
        # Like lerobot_command but uses the aic_cheatcode teleop, which drives
        # the arm using ground-truth TF frames from the simulation instead of
        # the VR controller. The four target frame names come from the
        # SceneConfig that was generated for this episode so the teleop knows
        # exactly which port to insert into.
        cmd = [
            "pixi",
            "run",
            "lerobot-record",
            "--robot.type=aic_controller",
            "--robot.id=aic",
            "--teleop.type=aic_cheatcode",
            "--teleop.id=aic",
            "--robot.teleop_target_mode=cartesian",
            "--robot.teleop_frame_id=gripper/tcp",
            f"--dataset.push_to_hub={'true' if push_to_hub else 'false'}",
            "--dataset.private=true",
            f"--dataset.num_episodes={num_episodes}",
            "--dataset.episode_time_s=3600",
            "--play_sounds=false",
            f"--display_data={'true' if display_data else 'false'}",
            f"--dataset.repo_id={self.definition.repo_id}",
            f"--dataset.single_task={self.definition.single_task}",
            f"--dataset.root={self.definition.dataset_root}",
            f"--teleop.task_cable_name={config.task_cable_name}",
            f"--teleop.task_plug_name={config.task_plug_name}",
            f"--teleop.task_module_name={config.task_module_name}",
            f"--teleop.task_port_name={config.task_port_name}",
            "--dataset.streaming_encoding=true",
            "--dataset.encoder_threads=2",
            "--dataset.fps=20",
        ]
        if self._should_resume():
            cmd.append("--resume=true")
        return cmd


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


def _count_episodes_from_parquet_path(path: Path) -> Optional[int]:
    if not path.exists():
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


def _count_episodes_from_json_path(path: Path) -> Optional[int]:
    if not path.exists():
        return None
    if path.suffix == ".jsonl":
        try:
            with path.open("r", encoding="utf-8") as handle:
                return sum(1 for line in handle if line.strip())
        except OSError:
            return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    for key in ("total_episodes", "num_episodes", "episodes", "episode_count"):
        if key in data:
            try:
                return int(data[key])
            except (TypeError, ValueError):
                return None
    if isinstance(data, list):
        return len(data)
    return None


def _iter_local_cache_paths(repo_id: str) -> Iterable[Path]:
    repo_slug = repo_id.replace("/", "--")
    hub_root = HF_HUB_CACHE_ROOT / f"datasets--{repo_slug}"
    lerobot_root = HF_CACHE_ROOT / repo_id
    if lerobot_root.exists():
        yield lerobot_root

    if hub_root.exists():
        snapshots = hub_root / "snapshots"
        if snapshots.exists():
            for snapshot in sorted(snapshots.iterdir(), reverse=True):
                if snapshot.is_dir():
                    yield snapshot


def _has_local_cache(repo_id: str) -> bool:
    return any(_has_candidate_files(path) for path in _iter_local_cache_paths(repo_id))


def _ensure_local_dataset_cache(repo_id: str, token: Optional[str]) -> None:
    try:
        from huggingface_hub import snapshot_download
    except Exception:
        return

    allow_patterns = [
        "**/episodes.json",
        "**/episodes.jsonl",
        "**/episode_index.json",
        "**/episode_index.jsonl",
        "**/episode_index.parquet",
        "**/meta.json",
        "**/metadata.json",
        "**/dataset_info.json",
        "**/info.json",
        "**/stats.json",
    ]
    try:
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            allow_patterns=allow_patterns,
            token=token,
        )
    except Exception as exc:
        print(f"[warn] Could not cache dataset {repo_id}: {exc}")
        return


def _find_episode_count_in_local_cache(repo_id: str) -> Optional[int]:
    json_candidates = [
        "episodes.json",
        "episodes.jsonl",
        "episode_index.json",
        "episode_index.jsonl",
        "meta.json",
        "metadata.json",
        "dataset_info.json",
        "info.json",
        "meta/info.json",
        "meta/stats.json",
        "data/episodes.json",
        "data/episodes.jsonl",
        "data/episode_index.json",
        "data/episode_index.jsonl",
        "data/meta.json",
        "data/metadata.json",
    ]
    parquet_candidates = [
        "episode_index.parquet",
        "episode_index/episode_index.parquet",
        "data/episode_index.parquet",
    ]

    for root in _iter_local_cache_paths(repo_id):
        for filename in json_candidates:
            count = _count_episodes_from_json_path(root / filename)
            if count is not None:
                return count

        for filename in parquet_candidates:
            count = _count_episodes_from_parquet_path(root / filename)
            if count is not None:
                return count

    return None


def _has_candidate_files(root: Path) -> bool:
    if not root.exists():
        return False
    candidates = [
        "episodes.json",
        "episodes.jsonl",
        "episode_index.json",
        "episode_index.jsonl",
        "meta.json",
        "metadata.json",
        "dataset_info.json",
        "info.json",
        "meta/info.json",
        "meta/stats.json",
        "episode_index.parquet",
        "episode_index/episode_index.parquet",
        "data/episodes.json",
        "data/episodes.jsonl",
        "data/episode_index.json",
        "data/episode_index.jsonl",
        "data/episode_index.parquet",
        "data/meta.json",
        "data/metadata.json",
    ]
    return any((root / path).exists() for path in candidates)


def _is_empty_dir(path: Path) -> bool:
    if not path.exists() or not path.is_dir():
        return False
    return not any(path.iterdir())


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
                "caai-aic/corrected_lab_collected_sfp_to_sfp_port_"
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
        repo_id = f"caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_{port}"
        tasks.append(
            RecordingTask(
                TaskDefinition(
                    repo_id=repo_id,
                    single_task=SC_TASK_TEMPLATE.format(port=port),
                )
            )
        )

    return tasks



def build_scene_generator() -> SceneGenerator:
    return SceneGenerator()


def apply_scene_overrides(repo_id: str, config: SceneConfig) -> SceneConfig:
    overrides = DATASET_SCENE_OVERRIDES.get(repo_id)
    if not overrides:
        return config
    return replace(config, **overrides)


def launch_scene_for_episode(
    repo_id: str,
    config: SceneConfig,
    ws_path: Path,
    scene_holder: Dict[str, object],
    headless: bool = True,
) -> SceneProcess:
    config = apply_scene_overrides(repo_id, config)
    launch_args = config.to_launch_args(gazebo_gui=not headless, launch_rviz=False)
    scene_holder["scene_config"] = config
    scene_holder["scene_launch_args"] = launch_args
    scene = start_scene(launch_args, ws_path, headless=headless)
    scene_holder["scene"] = scene
    return scene


def start_scene(launch_args: str, ws_path: Path, headless: bool = True) -> SceneProcess:
    launch_cmd = f"/entrypoint.sh {launch_args} start_aic_engine:=false"
    print(f"[info] Scene launch command: {launch_cmd}")
    if headless:
        command = f"docker exec aic_eval {launch_cmd}"
    else:
        command = f"docker exec -e DISPLAY=$DISPLAY -e XAUTHORITY=$XAUTHORITY aic_eval {launch_cmd}"
    process = _launch_terminal(
        command, title="AIC Scene", cwd=ws_path, keep_open=False
    )
    print("[info] Scene launch started in a new terminal.")
    return SceneProcess(process=process, detached=True)


def _gz_topic_list(container: str = "aic_eval") -> List[str]:
    """Return the list of active gz topics inside the container, or []."""
    try:
        result = subprocess.run(
            [
                "docker", "exec", container,
                "bash", "-c",
                "export GZ_IP=127.0.0.1; "
                "source /opt/ros/kilted/setup.bash; "
                "source /ws_aic/install/setup.bash; "
                "gz topic -l 2>/dev/null",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.splitlines()
    except Exception:
        return []


_RCLPY_TF_CHECK = """\
import rclpy, sys, time
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from tf2_ros import Buffer, TransformListener
rclpy.init()
node = Node('spawn_check')
tf_buf = Buffer()
TransformListener(tf_buf, node)
executor = SingleThreadedExecutor()
executor.add_node(node)
deadline = time.time() + {timeout}
while time.time() < deadline:
    executor.spin_once(timeout_sec=0.5)
    try:
        tf_buf.lookup_transform('world', '{frame}', rclpy.time.Time())
        rclpy.shutdown(); sys.exit(0)
    except Exception:
        pass
rclpy.shutdown(); sys.exit(1)
"""

_RCLPY_INSERTION_WAIT = """\
import rclpy, sys, time
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from tf2_ros import Buffer, TransformListener
rclpy.init()
node = Node('insertion_wait')
tf_buf = Buffer()
TransformListener(tf_buf, node)
executor = SingleThreadedExecutor()
executor.add_node(node)
plug_frame = '{plug_frame}'
port_frame = '{port_frame}'
# Warm up the TF buffer and let the arm start moving before checking.
warmup_end = time.time() + 20
while time.time() < warmup_end:
    executor.spin_once(timeout_sec=0.5)
# Now poll: compare both frames in world Z (same as cheatcode does in base_link).
# Require 3 consecutive detections to avoid TF glitches.
deadline = time.time() + {timeout}
consecutive = 0
while time.time() < deadline:
    executor.spin_once(timeout_sec=0.5)
    try:
        tp = tf_buf.lookup_transform('world', plug_frame, rclpy.time.Time())
        tr = tf_buf.lookup_transform('world', port_frame, rclpy.time.Time())
        z_diff = tp.transform.translation.z - tr.transform.translation.z
        if z_diff <= -0.010:
            consecutive += 1
            if consecutive >= 3:
                rclpy.shutdown(); sys.exit(0)
        else:
            consecutive = 0
    except Exception:
        consecutive = 0
rclpy.shutdown(); sys.exit(1)
"""


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
        gz_running = False
        try:
            result = subprocess.run(
                ["docker", "exec", "aic_eval", "pgrep", "-f", "gzserver"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                gz_running = True
        except Exception:
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

        if not gz_running and not sdf_ready:
            print(
                f"[info] Gazebo not ready yet (attempt {attempt}); "
                "gzserver/SDF not detected"
            )

        time.sleep(poll_interval)

    print("[warn] Timed out waiting for Gazebo readiness.")
    return False


def wait_for_objects_spawned(
    config: "SceneConfig",
    timeout_s: int = 120,
) -> bool:
    """Wait until the cable's TF frame appears, confirming the scene is spawned."""
    import rclpy
    from rclpy.node import Node
    from rclpy.executors import SingleThreadedExecutor
    from tf2_ros import Buffer, TransformListener

    frame = f"{config.task_cable_name}/{config.task_plug_name}_link"
    print(f"[info] Waiting for objects to spawn (TF frame: {frame})...")

    ctx = rclpy.Context()
    rclpy.init(context=ctx)
    node = Node("spawn_check", context=ctx)
    tf_buf = Buffer()
    TransformListener(tf_buf, node)
    executor = SingleThreadedExecutor(context=ctx)
    executor.add_node(node)

    found = False
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        executor.spin_once(timeout_sec=0.5)
        try:
            tf_buf.lookup_transform("world", frame, rclpy.time.Time(clock_type=rclpy.clock.ClockType.ROS_TIME))
            found = True
            break
        except Exception:
            pass

    node.destroy_node()
    ctx.try_shutdown()

    if found:
        print("[info] Scene objects confirmed spawned.")
    else:
        print("[warn] Could not confirm object spawning; proceeding anyway.")
    return True


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
    scene_generator: SceneGenerator,
    ws_path: Path,
    scene_holder: Dict[str, object],
) -> RecordingResult:
    task.prepare_dataset_root()
    # For multi-episode sessions we run `lerobot-record` as separate
    # processes with `--dataset.num_episodes=1` and restart it per episode.
    initial_num = 1 if num_episodes > 1 else num_episodes
    cmd = " ".join(shlex.quote(arg) for arg in task.lerobot_command(initial_num))
    record_process = _launch_terminal(
        cmd,
        title="LeRobot Record",
        cwd=AIC_ROOT,
        keep_open=False,
    )
    # expose record process so the control loop can restart it
    scene_holder["record"] = record_process
    print("[info] Recording launched in a new terminal.")
    print(
        "Press Right Arrow to restart the scene for the next episode, "
        "Left Arrow to relaunch the current scene parameters, or Enter here to finish recording."
    )
    _wait_for_recording_controls(
        task,
        num_episodes,
        scene_generator,
        ws_path,
        scene_holder,
    )
    # Ensure recording process is terminated when session finishes
    proc = scene_holder.get("record")
    if isinstance(proc, subprocess.Popen):
        if proc.poll() is None:
            # For multi-episode sessions, give more time for the last episode to be processed
            timeout_s = 120 if num_episodes > 1 else 10
            print(f"[info] Waiting for lerobot-record to finish (timeout: {timeout_s}s)...")
            try:
                proc.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                print(f"[warn] lerobot-record did not finish within {timeout_s}s, terminating...")
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
    if start_episode_count is not None:
        print("[info] Waiting for local dataset metadata to update...")
        _wait_for_local_episode_update(
            task.definition.repo_id,
            start_episode_count,
            expected_new_episodes=num_episodes,
        )
    return RecordingResult(completed_episodes=num_episodes, exit_code=0)


def _wait_for_local_episode_update(
    repo_id: str,
    previous_count: int,
    timeout_s: int = 300,
    poll_interval_s: int = 5,
    expected_new_episodes: Optional[int] = None,
) -> Optional[int]:
    deadline = time.time() + timeout_s
    latest_count = previous_count
    stable_count = None
    stable_checks = 0
    required_stable_checks = 3  # Require 3 consecutive checks with same count
    
    expected_final_count = None
    if expected_new_episodes is not None:
        expected_final_count = previous_count + expected_new_episodes
    
    while time.time() < deadline:
        current = _find_episode_count_in_local_cache(repo_id)
        if current is not None:
            latest_count = current
            # If we know the expected count, wait for it to be reached
            if expected_final_count is not None:
                if current >= expected_final_count:
                    # Once we reach expected count, verify it's stable
                    if current == stable_count:
                        stable_checks += 1
                        if stable_checks >= required_stable_checks:
                            print(f"[info] Dataset metadata updated: {previous_count} → {current} episodes")
                            return current
                    else:
                        stable_count = current
                        stable_checks = 1
                else:
                    # Haven't reached expected count yet, reset stable counter
                    stable_count = None
                    stable_checks = 0
            elif current != previous_count:
                # If no expected count specified, return on any change (original behavior)
                return current
        time.sleep(poll_interval_s)
    
    if latest_count > previous_count:
        print(f"[info] Dataset metadata updated: {previous_count} → {latest_count} episodes (timeout)")
    return latest_count


def _build_terminal_cmd(title: str, script_path: str) -> List[str]:
    """Return the argv to open a terminal running script_path.

    Checks $TERMINAL first, then known Ubuntu terminals, then
    x-terminal-emulator.  All entries use a plain script path so there are
    no shell-quoting differences between terminals.
    """
    known: List[Tuple[str, Any]] = [
        ("gnome-terminal", lambda: ["gnome-terminal", f"--title={title}", "--", script_path]),
        ("tilix",          lambda: ["tilix", "-t", title, "-e", script_path]),
        ("terminator",     lambda: ["terminator", "-T", title, "-x", script_path]),
        ("xfce4-terminal", lambda: ["xfce4-terminal", f"--title={title}", "-x", script_path]),
        ("xterm",          lambda: ["xterm", "-title", title, "-e", script_path]),
    ]

    candidates: List[Tuple[str, Any]] = []
    env_term = os.environ.get("TERMINAL", "").strip()
    if env_term:
        match = next(((n, f) for n, f in known if n == env_term), None)
        if match:
            candidates.append(match)
        elif shutil.which(env_term):
            candidates.append((env_term, lambda t=env_term: [t, "-e", script_path]))

    for entry in known:
        name, _ = entry
        if name not in {n for n, _ in candidates} and shutil.which(name):
            candidates.append(entry)

    if shutil.which("x-terminal-emulator"):
        candidates.append(("x-terminal-emulator", lambda: ["x-terminal-emulator", "-e", script_path]))

    if not candidates:
        raise RuntimeError("No terminal emulator found. Install one or set $TERMINAL.")

    _, builder = candidates[0]
    return builder()


def _launch_terminal(
    command: str, title: str, cwd: Path, keep_open: bool = True
) -> subprocess.Popen:
    tail = "; exec bash" if keep_open else ""
    shell_cmd = f"cd {shlex.quote(str(cwd))} && {command}{tail}"

    # Write a self-deleting temp script so no terminal needs quoting tricks.
    script = tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", prefix="aic_term_", delete=False
    )
    try:
        script.write(
            f"#!/bin/bash\n"
            f'export PATH="$HOME/.pixi/bin:$PATH"\n'
            f"rm -f {shlex.quote(script.name)}\n"
            f"{shell_cmd}\n"
        )
        script.close()
        os.chmod(script.name, 0o755)
    except Exception:
        script.close()
        os.unlink(script.name)
        raise

    terminal_cmd = _build_terminal_cmd(title, script.name)
    try:
        return subprocess.Popen(terminal_cmd)
    except FileNotFoundError as exc:
        os.unlink(script.name)
        raise RuntimeError(f"Could not launch terminal ({terminal_cmd[0]}): {exc}") from exc


def _terminate_processes(patterns: Iterable[str]) -> None:
    for pattern in patterns:
        try:
            subprocess.run(
                ["pkill", "-f", pattern],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass


def _terminate_gazebo_in_distrobox() -> None:
    try:
        subprocess.run(
            ["docker", "exec", "aic_eval", "pkill", "-9", "-f", "gzserver|gzclient|gazebo|gz sim|ros_gz_container|component_container|aic_adapter|kilted"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass
    time.sleep(3)  # give the container time to fully release resources




def _read_episode_count(task: "RecordingTask") -> int:
    info_path = task.definition.dataset_root / "meta" / "info.json"
    if not info_path.exists():
        return 0
    try:
        return int(json.loads(info_path.read_text()).get("total_episodes", 0))
    except Exception:
        return 0


def _log_failed_scene(config: "SceneConfig", log_path: Path) -> None:
    import dataclasses, json
    entry = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), **dataclasses.asdict(config)}
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[warn] Failed scene config logged to {log_path}")


def cleanup_session_processes(*, include_distrobox: bool = True, include_visualization: bool = True) -> None:
    patterns = ["gzclient", "gzserver", "gazebo", "aic_adapter", "kilted"]
    if include_visualization:
        patterns = ["rerun", "re_viewer"] + patterns

    _terminate_processes(patterns)
    if include_distrobox:
        _terminate_gazebo_in_distrobox()


def _wait_for_recording_controls(
    task: RecordingTask,
    num_episodes: int,
    scene_generator: SceneGenerator,
    ws_path: Path,
    scene_holder: Dict[str, object],
) -> None:
    restart_event = threading.Event()
    relaunch_event = threading.Event()
    finish_event = threading.Event()
    episodes_completed = 0
    listener = None
    use_global_hotkeys = False
    try:
        from pynput import keyboard

        def on_press(key: keyboard.Key) -> Optional[bool]:
            if key == keyboard.Key.right:
                restart_event.set()
            if key == keyboard.Key.left:
                relaunch_event.set()
            return None

        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        use_global_hotkeys = True
    except Exception:
        use_global_hotkeys = False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            if finish_event.is_set():
                return
            if relaunch_event.is_set():
                relaunch_event.clear()
                scene = scene_holder.get("scene")
                if isinstance(scene, SceneProcess):
                    scene.stop()
                cleanup_session_processes(include_distrobox=True, include_visualization=False)

                current_config = scene_holder.get("scene_config")
                if not isinstance(current_config, SceneConfig):
                    print("[warn] No active scene configuration available to relaunch.")
                    continue

                print("[info] Relaunching scene with the current episode parameters...")
                scene_holder["scene"] = launch_scene_for_episode(
                    task.definition.repo_id,
                    current_config,
                    ws_path,
                    scene_holder,
                )
                wait_for_scene_ready(ws_path, scene_holder["scene"])
                continue
            if restart_event.is_set():
                restart_event.clear()
                episodes_completed += 1
                scene = scene_holder.get("scene")
                if isinstance(scene, SceneProcess):
                    scene.stop()
                if episodes_completed >= num_episodes:
                    print("[info] Episode quota reached; stopping session.")
                    return
                # Keep visualization (e.g. rerun) running between episode restarts
                cleanup_session_processes(include_distrobox=True, include_visualization=False)

                # Restart the recording process (run single-episode recorder)
                rec_proc = scene_holder.get("record")
                if isinstance(rec_proc, subprocess.Popen):
                    try:
                        if rec_proc.poll() is None:
                            rec_proc.terminate()
                            rec_proc.wait(timeout=5)
                    except Exception:
                        try:
                            rec_proc.kill()
                        except Exception:
                            pass
                try:
                    rec_cmd = " ".join(shlex.quote(arg) for arg in task.lerobot_command(1))
                    new_rec = _launch_terminal(
                        rec_cmd,
                        title="LeRobot Record",
                        cwd=AIC_ROOT,
                        keep_open=False,
                    )
                    scene_holder["record"] = new_rec
                except Exception as exc:
                    print(f"[warn] Could not relaunch recording: {exc}")
                print("[info] Restarting scene for next episode...")
                config = scene_generator.generate_random_config()
                scene_holder["scene"] = launch_scene_for_episode(
                    task.definition.repo_id,
                    config,
                    ws_path,
                    scene_holder,
                )
                wait_for_scene_ready(ws_path, scene_holder["scene"])
                continue

            ready, _, _ = select.select([fd], [], [], 0.2)
            if not ready:
                continue
            ch = sys.stdin.read(1)
            if ch in ("\n", "\r"):
                return
            if not use_global_hotkeys and ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[C":
                    restart_event.set()
                elif seq == "[D":
                    relaunch_event.set()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if listener is not None:
            listener.stop()


def read_hf_token(path: Optional[Path]) -> Optional[str]:
    if path is None:
        default_path = Path.home() / ".cache" / "huggingface" / "token"
        if default_path.exists():
            return default_path.read_text(encoding="utf-8").strip()
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
            scene_holder: Dict[str, object] = {}
            scene = launch_scene_for_episode(
                task.definition.repo_id,
                config,
                ws_path,
                scene_holder,
            )
            ready = wait_for_scene_ready(ws_path, scene)
            if not ready:
                scene.stop()
                print("[warn] Scene did not start; returning to menu.")
                continue

            start_count = episode_counts.get(task.definition.repo_id)
            result = run_recording(
                task,
                num_episodes,
                start_count,
                scene_generator,
                ws_path,
                scene_holder,
            )
            print(
                f"[info] Recording finished with code {result.exit_code}; "
                f"episodes completed: {result.completed_episodes}"
            )

            scene = scene_holder["scene"]
            scene.stop()
            print("[info] Scene stopped.")

            cleanup_session_processes(include_distrobox=False)

            print("[info] Refreshing dataset info...")

    except KeyboardInterrupt:
        print("\n[info] Interrupted by user.")
    finally:
        cleanup_session_processes(include_distrobox=False)

    return 0


def _target_for_task(task: RecordingTask) -> dict:
    """Derive the fixed cheatcode target parameters from a task's repo_id."""
    repo_id = task.definition.repo_id
    if "sfp_to_sfp" in repo_id:
        # e.g. caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_2
        parts = repo_id.split("sfp_to_")[1]       # "sfp_port_0_of_nic_card_mount_2"
        port_part, mount_part = parts.split("_of_")  # "sfp_port_0", "nic_card_mount_2"
        return {
            "cable_type": "sfp_sc_cable",
            "task_plug_name": "sfp_tip",
            "task_module_name": mount_part,
            "task_port_name": port_part,
        }
    else:
        # e.g. caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_1
        sc_num = repo_id.split("sc_port_")[-1]  # "0" or "1"
        return {
            "cable_type": "sfp_sc_cable_reversed",
            "task_plug_name": "sc_tip",
            "task_module_name": f"sc_port_{sc_num}",
            "task_port_name": "sc_port_base",
        }


def main_cheatcode() -> int:
    """Fully automated recording loop using the cheatcode teleop.

    For each iteration the script:
      1. Generates a random scene configuration (random board pose, cable type,
         component presence, and a guaranteed insertion target).
      2. Launches the Gazebo scene in a new terminal.
      3. Waits until the scene is ready.
      4. Runs lerobot-record with the aic_cheatcode teleop for one episode.
      5. Tears the scene down and repeats.

    No human interaction is required after the script starts — there is no VR
    controller and no task-chooser menu.
    """
    parser = argparse.ArgumentParser(
        description="Automated cheatcode dataset recording with randomised scenes."
    )
    parser.add_argument(
        "--ws-path",
        type=Path,
        default=AIC_ROOT,
        help="Path to ws_aic_caai/src/aic",
    )
    parser.add_argument(
        "--num-scenes",
        type=int,
        default=0,
        help=(
            "Target number of episodes per dataset (0 = run forever). "
            "When set to N the script keeps running until every dataset has at "
            "least N saved episodes, choosing whichever dataset has the fewest "
            "episodes on each iteration."
        ),
    )
    parser.add_argument(
        "--hf-token-path",
        type=Path,
        default=None,
        help="Optional Hugging Face token path",
    )
    parser.add_argument(
        "--failure-log",
        type=Path,
        default=Path("failed_scenes.jsonl"),
        help="File to append failed scene configs to (default: failed_scenes.jsonl)",
    )
    parser.add_argument(
        "--push-to-hub",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Push dataset to Hugging Face Hub after each episode (default: off). Requires HF authentication.",
    )
    parser.add_argument(
        "--force-repo-id",
        type=str,
        default=None,
        help="Pin every iteration to a specific dataset repo-id (useful for targeted testing).",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Headless mode (default: on). Controls whether Gazebo opens a GUI window. "
            "Pass --no-headless when running from a desktop to see the Gazebo simulation. "
            "lerobot is always controlled via key events (uinput) regardless of this flag."
        ),
    )
    args = parser.parse_args()

    ws_path = args.ws_path
    if not ws_path.exists():
        print(f"Workspace path not found: {ws_path}")
        return 1

    hf_token = read_hf_token(args.hf_token_path)

    all_tasks = build_tasks()

    print("[info] Cleaning up any leftover Gazebo processes before starting...")
    cleanup_session_processes(include_distrobox=True)

    scene_generator = build_scene_generator()
    unlimited = args.num_scenes == 0
    print("[info] Cheatcode recording started.")
    print(f"[info] {len(all_tasks)} datasets | target: {'unlimited' if unlimited else f'{args.num_scenes} episodes each'}")

    episodes_total = 0
    round_robin_index = 0
    try:
        while True:
            # Select the next dataset in round-robin order.
            if args.force_repo_id:
                eligible = [t for t in all_tasks if t.definition.repo_id == args.force_repo_id]
                if not eligible:
                    print(f"[error] --force-repo-id '{args.force_repo_id}' not found in task list.")
                    break
            else:
                eligible = [
                    t for t in all_tasks
                    if unlimited or _read_episode_count(t) < args.num_scenes
                ]
                if not eligible:
                    print("[info] All datasets have reached the target episode count.")
                    break
            task = eligible[round_robin_index % len(eligible)]
            round_robin_index += 1
            current_count = _read_episode_count(task)

            print(f"\n[info] === Episode {episodes_total + 1} — {task.definition.repo_id} ({current_count} episodes so far) ===")

            # Generate a scene whose target is fixed to this dataset's port/module.
            target = _target_for_task(task)
            config = scene_generator.generate_random_config(target=target)
            print(
                f"[info] Target: cable={config.task_cable_name}  "
                f"plug={config.task_plug_name}  "
                f"module={config.task_module_name}  "
                f"port={config.task_port_name}"
            )

            task.prepare_dataset_root()

            scene_holder: Dict[str, object] = {}
            scene = launch_scene_for_episode(
                task.definition.repo_id,
                config,
                ws_path,
                scene_holder,
                headless=args.headless,
            )

            ready = wait_for_scene_ready(ws_path, scene)
            if not ready:
                scene.stop()
                print("[warn] Scene did not start; skipping and retrying.")
                cleanup_session_processes(include_distrobox=True)
                continue

            wait_for_objects_spawned(config)

            print("[info] Taring force-torque sensor before recording...")
            tare_cmd = ["pixi", "run", "ros2", "service", "call",
                        "/aic_controller/tare_force_torque_sensor", "std_srvs/srv/Trigger"]
            tare_ok = False
            for tare_attempt in range(3):
                result = subprocess.run(tare_cmd, cwd=AIC_ROOT, capture_output=True, text=True)
                if result.returncode == 0 and "success=True" in result.stdout:
                    tare_ok = True
                    break
                print(f"[warn] Tare attempt {tare_attempt + 1}/3 failed — retrying in 5s...")
                time.sleep(5)
            if not tare_ok:
                print("[error] Tare failed after 3 attempts — aborting scene.")
                scene = scene_holder["scene"]
                scene.stop()
                cleanup_session_processes(include_distrobox=True)
                _log_failed_scene(config, args.failure_log)
                continue

            lerobot_cmd = task.cheatcode_lerobot_command(1, config, push_to_hub=args.push_to_hub, display_data=not args.headless)
            print(f"[info] Launching lerobot-record: {' '.join(shlex.quote(a) for a in lerobot_cmd)}")
            record_process = subprocess.Popen(lerobot_cmd, cwd=AIC_ROOT)
            scene_holder["record"] = record_process

            episodes_before = _read_episode_count(task)
            record_process.wait()
            if _read_episode_count(task) > episodes_before:
                episodes_total += 1
                new_count = _read_episode_count(task)
                print(f"[info] Episode saved → {task.definition.repo_id} now has {new_count} episodes (total across all datasets: {episodes_total})")
            else:
                print("[warn] Episode not saved (cheatcode timed out or lerobot error) — discarding.")
                _log_failed_scene(config, args.failure_log)

            scene = scene_holder["scene"]
            scene.stop()
            print("[info] Scene stopped.")
            cleanup_session_processes(include_distrobox=True)

    except KeyboardInterrupt:
        print(f"\n[info] Interrupted. Episodes recorded this run: {episodes_total}")
    finally:
        cleanup_session_processes(include_distrobox=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main_cheatcode())
