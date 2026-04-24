#!/usr/bin/env python3
"""Generate trial task YAML from a scene manifest JSON file.

The generated YAML follows the `tasks` structure used by
`src/aic/aic_engine/config/sample_config.yaml`.

Task generation rules:
- For `sfp_sc_cable`: generate all (`nic_card_mount_i`, `sfp_port_0|1`) tasks
  where `nic_card_mount_i_present == true`.
- For `sfp_sc_cable_reversed`: generate all (`sc_port_i`, `sc_port_base`) tasks
  where `sc_port_i_present == true`.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


class EngineConfigDumper(yaml.SafeDumper):
    pass


def _represent_bool(dumper: yaml.Dumper, data: bool) -> yaml.nodes.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:bool", "True" if data else "False")


EngineConfigDumper.add_representer(bool, _represent_bool)


GRIPPER_OFFSET_RANGES = {
    "x": (-0.002, 0.002),
    "y": (0.015385 - 0.002, 0.015385 + 0.002),
    "z": (0.04245 - 0.002, 0.04245 + 0.002),
    "roll": (0.4432 - 0.04, 0.4432 + 0.04),
    "pitch": (-0.4838 - 0.04, -0.4838 + 0.04),
    "yaw": (1.3303 - 0.04, 1.3303 + 0.04),
}

TASK_BOARD_X_RANGE = (0.1, 0.3)
TASK_BOARD_Y_RANGE = (-0.3, -0.1)
TASK_BOARD_YAW_RANGE = (-0.5, 0.5)
ROBOT_Z = 1.14
ROBOT_ROLL = 0.0
ROBOT_PITCH = 0.0
ROBOT_YAW = -3.141
CABLE_X_RANGE = (0.172 - 0.002, 0.172 + 0.002)
CABLE_Y_RANGE = (0.024 - 0.002, 0.024 + 0.002)
CABLE_ROLL_RANGE = (0.4432 - 0.04, 0.4432 + 0.04)
CABLE_PITCH_RANGE = (-0.48 - 0.04, -0.48 + 0.04)
CABLE_YAW_RANGE = (1.3303 - 0.04, 1.3303 + 0.04)
MOUNT_TRANSLATION_RANGE = (-0.09625, 0.09625)
MOUNT_YAW_RANGE = (-1.047, 1.047)
SC_PORT_TRANSLATION_RANGE = (-0.06, 0.055)
NIC_TRANSLATION_RANGE = (-0.0215, 0.0234)
NIC_YAW_RANGE = (-0.175, 0.175)

DEFAULT_SAMPLE_CONFIG = (
    Path(__file__).resolve().parents[3] / "aic_engine/config/sample_config.yaml"
)


def _build_tasks_for_scene(scene_config: Dict, time_limit: int) -> List[Dict[str, object]]:
    """Build all valid insertion tasks for one scene configuration."""
    cable_type = scene_config.get("cable_type")
    tasks: List[Dict[str, object]] = []

    if cable_type == "sfp_sc_cable":
        present_targets = [
            f"nic_card_mount_{i}"
            for i in range(5)
            if bool(scene_config.get(f"nic_card_mount_{i}_present", False))
        ]

        for target_module_name in present_targets:
            for port_name in ("sfp_port_0", "sfp_port_1"):
                tasks.append(
                    {
                        "cable_type": "sfp_sc",
                        "cable_name": "cable_0",
                        "plug_type": "sfp",
                        "plug_name": "sfp_tip",
                        "port_type": "sfp",
                        "port_name": port_name,
                        "target_module_name": target_module_name,
                        "time_limit": time_limit,
                    }
                )

    elif cable_type == "sfp_sc_cable_reversed":
        present_targets = [
            f"sc_port_{i}"
            for i in range(2)
            if bool(scene_config.get(f"sc_port_{i}_present", False))
        ]

        for target_module_name in present_targets:
            tasks.append(
                {
                    "cable_type": "sfp_sc",
                    "cable_name": "cable_1",
                    "plug_type": "sc",
                    "plug_name": "sc_tip",
                    "port_type": "sc",
                    "port_name": "sc_port_base",
                    "target_module_name": target_module_name,
                    "time_limit": time_limit,
                }
            )

    return tasks


def _random_gripper_offset() -> Dict[str, float]:
    """Generate a gripper offset within the requested bounds."""
    return {
        axis: random.uniform(low, high)
        for axis, (low, high) in GRIPPER_OFFSET_RANGES.items()
    }


def _random_scene_config(cable_type: str) -> Dict[str, object]:
    """Generate a fresh random scene config using the automation script ranges."""
    if cable_type not in {"sfp_sc_cable", "sfp_sc_cable_reversed"}:
        raise ValueError(f"Unsupported cable type: {cable_type}")

    cable_z = 1.508 if cable_type == "sfp_sc_cable_reversed" else 1.518
    scene_config = {
        "robot_z": ROBOT_Z,
        "robot_roll": ROBOT_ROLL,
        "robot_pitch": ROBOT_PITCH,
        "robot_yaw": ROBOT_YAW,
        "task_board_x": random.uniform(*TASK_BOARD_X_RANGE),
        "task_board_y": random.uniform(*TASK_BOARD_Y_RANGE),
        "task_board_z": ROBOT_Z,
        "task_board_roll": 0.0,
        "task_board_pitch": 0.0,
        "task_board_yaw": random.uniform(*TASK_BOARD_YAW_RANGE),
        "spawn_cable": True,
        "cable_type": cable_type,
        "cable_x": random.uniform(*CABLE_X_RANGE),
        "cable_y": random.uniform(*CABLE_Y_RANGE),
        "cable_z": random.uniform(cable_z - 0.002, cable_z + 0.002),
        "cable_roll": random.uniform(*CABLE_ROLL_RANGE),
        "cable_pitch": random.uniform(*CABLE_PITCH_RANGE),
        "cable_yaw": random.uniform(*CABLE_YAW_RANGE),
        "attach_cable_to_gripper": True,
    }

    for prefix, count in (
        ("sfp_mount_rail", 2),
        ("sc_mount_rail", 2),
        ("lc_mount_rail", 2),
        ("nic_card_mount", 5),
        ("sc_port", 2),
    ):
        for index in range(count):
            scene_config[f"{prefix}_{index}_present"] = random.choice([True, False])
            if prefix == "sc_port":
                scene_config[f"{prefix}_{index}_translation"] = random.uniform(
                    *SC_PORT_TRANSLATION_RANGE
                )
                scene_config[f"{prefix}_{index}_roll"] = 0.0
                scene_config[f"{prefix}_{index}_pitch"] = 0.0
                scene_config[f"{prefix}_{index}_yaw"] = 0.0
            elif prefix == "nic_card_mount":
                scene_config[f"{prefix}_{index}_translation"] = random.uniform(
                    *NIC_TRANSLATION_RANGE
                )
                scene_config[f"{prefix}_{index}_roll"] = 0.0
                scene_config[f"{prefix}_{index}_pitch"] = 0.0
                scene_config[f"{prefix}_{index}_yaw"] = random.uniform(*NIC_YAW_RANGE)
            else:
                scene_config[f"{prefix}_{index}_translation"] = random.uniform(
                    *MOUNT_TRANSLATION_RANGE
                )
                scene_config[f"{prefix}_{index}_roll"] = 0.0
                scene_config[f"{prefix}_{index}_pitch"] = 0.0
                scene_config[f"{prefix}_{index}_yaw"] = random.uniform(*MOUNT_YAW_RANGE)

    required_prefix = "nic_card_mount" if cable_type == "sfp_sc_cable" else "sc_port"
    required_count = 5 if cable_type == "sfp_sc_cable" else 2
    while not any(
        scene_config[f"{required_prefix}_{index}_present"] for index in range(required_count)
    ):
        for index in range(required_count):
            scene_config[f"{required_prefix}_{index}_present"] = random.choice([True, False])

    return scene_config


def _load_yaml(path: Path) -> Dict:
    """Load a YAML file into a dictionary."""
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"YAML file must contain a mapping at top level: {path}")
    return loaded


def _normalize_task_list(tasks_value: object) -> List[Dict[str, object]]:
    """Normalize a task container into a list of task dictionaries."""
    if isinstance(tasks_value, dict):
        return [tasks_value[key] for key in sorted(tasks_value.keys())]
    if isinstance(tasks_value, list):
        return [task for task in tasks_value if isinstance(task, dict)]
    return []


def _tasks_from_tasks_yaml(tasks_yaml: Dict, scene_index: int) -> List[Dict[str, object]]:
    """Load the task list for a scene from the generated tasks YAML file."""
    trial_key = f"trial_{scene_index + 1}"
    trials = tasks_yaml.get("trials", {})
    if not isinstance(trials, dict):
        raise ValueError("Tasks YAML field 'trials' must be a mapping")
    trial_entry = trials.get(trial_key)
    if not isinstance(trial_entry, dict):
        return []
    return _normalize_task_list(trial_entry.get("tasks"))


def _scene_candidates(manifest: Dict, cable_type: str) -> List[Dict]:
    """Return all scenes in a manifest matching a cable type."""
    scenes = manifest.get("scenes", [])
    if not isinstance(scenes, list):
        raise ValueError("Manifest field 'scenes' must be a list")
    return [
        scene
        for scene in scenes
        if isinstance(scene, dict)
        and scene.get("config", {}).get("cable_type") == cable_type
    ]


def _select_random_task(scene_config: Dict, time_limit: int) -> Dict[str, object]:
    """Choose one task from the full valid task set for a scene."""
    tasks = _build_tasks_for_scene(scene_config, time_limit=time_limit)
    if not tasks:
        raise ValueError(
            "Selected scene does not contain any valid target modules for this cable type"
        )
    return random.choice(tasks)


def _build_scene_block(scene_config: Dict) -> Dict[str, object]:
    """Build a sample-config-style scene block from a manifest config."""
    cable_type = scene_config["cable_type"]
    cable_name = "cable_0" if cable_type == "sfp_sc_cable" else "cable_1"
    plug_type = "sfp" if cable_type == "sfp_sc_cable" else "sc"
    plug_name = "sfp_tip" if cable_type == "sfp_sc_cable" else "sc_tip"

    def module_entry(prefix: str, index: int, entity_name: str) -> Dict[str, object]:
        present_key = f"{prefix}_{index}_present"
        return {
            "entity_present": bool(scene_config.get(present_key, False)),
            "entity_name": entity_name,
            "entity_pose": {
                "translation": scene_config.get(f"{prefix}_{index}_translation", 0.0),
                "roll": scene_config.get(f"{prefix}_{index}_roll", 0.0),
                "pitch": scene_config.get(f"{prefix}_{index}_pitch", 0.0),
                "yaw": scene_config.get(f"{prefix}_{index}_yaw", 0.0),
            },
        }

    scene = {
        "task_board": {
            "pose": {
                "x": scene_config["task_board_x"],
                "y": scene_config["task_board_y"],
                "z": scene_config["task_board_z"],
                "roll": scene_config["task_board_roll"],
                "pitch": scene_config["task_board_pitch"],
                "yaw": scene_config["task_board_yaw"],
            },
            "nic_rail_0": module_entry("nic_card_mount", 0, "nic_card_0"),
            "nic_rail_1": module_entry("nic_card_mount", 1, "nic_card_1"),
            "nic_rail_2": module_entry("nic_card_mount", 2, "nic_card_2"),
            "nic_rail_3": module_entry("nic_card_mount", 3, "nic_card_3"),
            "nic_rail_4": module_entry("nic_card_mount", 4, "nic_card_4"),
            "sc_rail_0": {
                "entity_present": bool(scene_config.get("sc_port_0_present", False)),
                "entity_name": "sc_mount_0",
                "entity_pose": {
                    "translation": scene_config.get("sc_port_0_translation", 0.0),
                    "roll": scene_config.get("sc_port_0_roll", 0.0),
                    "pitch": scene_config.get("sc_port_0_pitch", 0.0),
                    "yaw": scene_config.get("sc_port_0_yaw", 0.0),
                },
            },
            "sc_rail_1": {
                "entity_present": bool(scene_config.get("sc_port_1_present", False)),
                "entity_name": "sc_mount_1",
                "entity_pose": {
                    "translation": scene_config.get("sc_port_1_translation", 0.0),
                    "roll": scene_config.get("sc_port_1_roll", 0.0),
                    "pitch": scene_config.get("sc_port_1_pitch", 0.0),
                    "yaw": scene_config.get("sc_port_1_yaw", 0.0),
                },
            },
            "lc_mount_rail_0": module_entry("lc_mount_rail", 0, "lc_mount_0"),
            "sfp_mount_rail_0": module_entry("sfp_mount_rail", 0, "sfp_mount_0"),
            "sc_mount_rail_0": module_entry("sc_mount_rail", 0, "sc_mount_0"),
            "lc_mount_rail_1": module_entry("lc_mount_rail", 1, "lc_mount_1"),
            "sfp_mount_rail_1": module_entry("sfp_mount_rail", 1, "sfp_mount_1"),
            "sc_mount_rail_1": module_entry("sc_mount_rail", 1, "sc_mount_1"),
        },
        "cables": {
            cable_name: {
                "pose": {
                    "gripper_offset": _random_gripper_offset(),
                    "roll": scene_config["cable_roll"],
                    "pitch": scene_config["cable_pitch"],
                    "yaw": scene_config["cable_yaw"],
                },
                "attach_cable_to_gripper": bool(
                    scene_config.get("attach_cable_to_gripper", True)
                ),
                "cable_type": cable_type,
            }
        },
    }

    return {
        "scene": scene,
        "cables": scene["cables"],
        "cable_name": cable_name,
        "plug_type": plug_type,
        "plug_name": plug_name,
    }


def _generate_random_engine_trials(time_limit: int) -> Dict[str, Dict]:
    """Generate the three-trial engine config using fresh random scenes."""
    trials: Dict[str, Dict] = {}
    trial_specs = [
        (1, "sfp_sc_cable"),
        (2, "sfp_sc_cable"),
        (3, "sfp_sc_cable_reversed"),
    ]

    for trial_index, cable_type in trial_specs:
        scene_config = _random_scene_config(cable_type)
        scene_block = _build_scene_block(scene_config)
        task = random.choice(_build_tasks_for_scene(scene_config, time_limit=time_limit))
        trials[f"trial_{trial_index}"] = {
            "scene": scene_block["scene"],
            "tasks": {
                "task_1": {
                    "cable_type": task["cable_type"],
                    "cable_name": task["cable_name"],
                    "plug_type": task["plug_type"],
                    "plug_name": task["plug_name"],
                    "port_type": task["port_type"],
                    "port_name": task["port_name"],
                    "target_module_name": task["target_module_name"],
                    "time_limit": task["time_limit"],
                }
            },
        }

    return trials


def _manifest_to_trials(manifest: Dict, time_limit: int) -> Tuple[Dict[str, Dict], List[str]]:
    """Convert manifest scene entries into a `trials` mapping for YAML output."""
    trials: Dict[str, Dict] = {}
    warnings: List[str] = []

    scenes = manifest.get("scenes", [])
    if not isinstance(scenes, list):
        raise ValueError("Manifest field 'scenes' must be a list")

    for scene in scenes:
        scene_index = scene.get("index")
        scene_name = scene.get("name", "")
        scene_config = scene.get("config", {})

        if not isinstance(scene_config, dict):
            warnings.append(
                f"Skipping scene index={scene_index}: 'config' is not an object"
            )
            continue

        cable_type = scene_config.get("cable_type")
        if cable_type not in {"sfp_sc_cable", "sfp_sc_cable_reversed"}:
            warnings.append(
                f"Skipping scene index={scene_index} name='{scene_name}': "
                f"unsupported cable_type='{cable_type}'"
            )
            continue

        tasks = _build_tasks_for_scene(scene_config, time_limit=time_limit)
        if not tasks:
            warnings.append(
                f"Scene index={scene_index} name='{scene_name}' produced no tasks "
                f"(no compatible target modules present)"
            )

        trial_key = f"trial_{int(scene_index) + 1}" if scene_index is not None else f"trial_{len(trials) + 1}"
        trials[trial_key] = {
            "tasks": {
                f"task_{i + 1}": task for i, task in enumerate(tasks)
            }
        }

    return trials, warnings


def _build_engine_config_from_manifests(
    sample_config: Dict,
    normal_manifest: Dict,
    reversed_manifest: Optional[Dict],
    tasks_yaml: Optional[Dict],
    time_limit: int,
) -> Dict:
    """Build a full engine config with three randomized trials."""
    trials: Dict[str, Dict] = {}

    normal_scenes = _scene_candidates(normal_manifest, "sfp_sc_cable")
    reversed_source = reversed_manifest if reversed_manifest is not None else normal_manifest
    reversed_scenes = _scene_candidates(reversed_source, "sfp_sc_cable_reversed")

    if len(normal_scenes) < 2:
        raise ValueError("Need at least two normal cable scenes to build trial_1 and trial_2")
    if len(reversed_scenes) < 1:
        raise ValueError("Need at least one reversed cable scene to build trial_3")

    selected_normal = random.sample(normal_scenes, 2)
    selected_reversed = random.choice(reversed_scenes)
    chosen_scenes = [selected_normal[0], selected_normal[1], selected_reversed]

    for trial_index, scene_entry in enumerate(chosen_scenes, start=1):
        scene_config = scene_entry["config"]
        scene_index = int(scene_entry["index"])
        if tasks_yaml is not None:
            task_candidates = _tasks_from_tasks_yaml(tasks_yaml, scene_index)
        else:
            task_candidates = _build_tasks_for_scene(scene_config, time_limit=time_limit)
        if not task_candidates:
            raise ValueError(
                f"No task candidates available for scene index {scene_index}"
            )
        task = random.choice(task_candidates)
        trial_scene = _build_scene_block(scene_config)

        trials[f"trial_{trial_index}"] = {
            "scene": trial_scene["scene"],
            "tasks": {
                "task_1": {
                    "cable_type": task["cable_type"],
                    "cable_name": task["cable_name"],
                    "plug_type": task["plug_type"],
                    "plug_name": task["plug_name"],
                    "port_type": task["port_type"],
                    "port_name": task["port_name"],
                    "target_module_name": task["target_module_name"],
                    "time_limit": task["time_limit"],
                }
            },
        }

    engine_config = copy.deepcopy(sample_config)
    engine_config["trials"] = trials
    return engine_config


def _emit_trials_yaml(trials: Dict[str, Dict]) -> str:
    """Serialize trials mapping to YAML with task formatting matching sample config."""
    lines: List[str] = ["trials:"]

    for trial_key in sorted(trials.keys(), key=lambda k: int(k.split("_")[1])):
        lines.append(f"  {trial_key}:")
        lines.append("    tasks:")

        tasks = trials[trial_key]["tasks"]
        if not tasks:
            lines.append("      {}")
            continue

        for task_key in sorted(tasks.keys(), key=lambda k: int(k.split("_")[1])):
            task = tasks[task_key]
            lines.append(f"      {task_key}:")
            lines.append(f"        cable_type: \"{task['cable_type']}\"")
            lines.append(f"        cable_name: \"{task['cable_name']}\"")
            lines.append(f"        plug_type: \"{task['plug_type']}\"")
            lines.append(f"        plug_name: \"{task['plug_name']}\"")
            lines.append(f"        port_type: \"{task['port_type']}\"")
            lines.append(f"        port_name: \"{task['port_name']}\"")
            lines.append(f"        target_module_name: \"{task['target_module_name']}\"")
            lines.append(f"        time_limit: {task['time_limit']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate task YAML, manifest-based engine config YAML, or random engine config YAML."
        )
    )
    parser.add_argument(
        "--mode",
        choices=("tasks", "engine_config", "random_engine_config"),
        default="tasks",
        help="Output mode: task-only YAML or full engine config YAML",
    )
    parser.add_argument(
        "--manifest",
        "--normal_manifest",
        type=Path,
        dest="normal_manifest",
        default=None,
        help="Path to the normal or combined scene manifest JSON file",
    )
    parser.add_argument(
        "--reversed_manifest",
        type=Path,
        default=None,
        help="Optional path to a reversed-cable scene manifest JSON file",
    )
    parser.add_argument(
        "--tasks_yaml",
        type=Path,
        default=None,
        help="Optional tasks YAML generated by this script for validation or reuse",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output YAML path",
    )
    parser.add_argument(
        "--time_limit",
        type=int,
        default=180,
        help="Task time limit in seconds (default: 180)",
    )

    args = parser.parse_args()

    if args.time_limit <= 0:
        raise ValueError("--time_limit must be > 0")

    if args.mode == "tasks":
        if args.normal_manifest is None:
            raise ValueError("--manifest is required when --mode tasks")
        if not args.normal_manifest.exists():
            raise FileNotFoundError(f"Manifest not found: {args.normal_manifest}")
        normal_manifest = json.loads(args.normal_manifest.read_text(encoding="utf-8"))
        trials, warnings = _manifest_to_trials(normal_manifest, time_limit=args.time_limit)
        yaml_text = _emit_trials_yaml(trials)
    elif args.mode == "engine_config":
        if args.normal_manifest is None:
            raise ValueError("--normal_manifest is required when --mode engine_config")
        if not args.normal_manifest.exists():
            raise FileNotFoundError(f"Manifest not found: {args.normal_manifest}")
        normal_manifest = json.loads(args.normal_manifest.read_text(encoding="utf-8"))

        reversed_manifest = None
        if args.reversed_manifest is not None:
            if not args.reversed_manifest.exists():
                raise FileNotFoundError(f"Manifest not found: {args.reversed_manifest}")
            reversed_manifest = json.loads(args.reversed_manifest.read_text(encoding="utf-8"))

        if not DEFAULT_SAMPLE_CONFIG.exists():
            raise FileNotFoundError(f"Sample config not found: {DEFAULT_SAMPLE_CONFIG}")

        sample_config = _load_yaml(DEFAULT_SAMPLE_CONFIG)
        tasks_yaml = _load_yaml(args.tasks_yaml) if args.tasks_yaml is not None else None
        engine_config = _build_engine_config_from_manifests(
            sample_config=sample_config,
            normal_manifest=normal_manifest,
            reversed_manifest=reversed_manifest,
            tasks_yaml=tasks_yaml,
            time_limit=args.time_limit,
        )
        yaml_text = yaml.dump(
            engine_config,
            Dumper=EngineConfigDumper,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        warnings = []
    else:
        if not DEFAULT_SAMPLE_CONFIG.exists():
            raise FileNotFoundError(f"Sample config not found: {DEFAULT_SAMPLE_CONFIG}")
        sample_config = _load_yaml(DEFAULT_SAMPLE_CONFIG)
        engine_config = copy.deepcopy(sample_config)
        engine_config["trials"] = _generate_random_engine_trials(time_limit=args.time_limit)
        yaml_text = yaml.dump(
            engine_config,
            Dumper=EngineConfigDumper,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        warnings = []

    if args.tasks_yaml is not None and not args.tasks_yaml.exists():
        raise FileNotFoundError(f"Tasks YAML not found: {args.tasks_yaml}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml_text, encoding="utf-8")

    if args.mode == "tasks":
        print(f"Wrote {len(trials)} trial entries to: {args.output}")
    elif args.mode == "engine_config":
        print(f"Wrote engine config YAML to: {args.output}")
    else:
        print(f"Wrote engine config YAML to: {args.output}")
    for warning in warnings:
        print(f"WARNING: {warning}")


if __name__ == "__main__":
    main()
