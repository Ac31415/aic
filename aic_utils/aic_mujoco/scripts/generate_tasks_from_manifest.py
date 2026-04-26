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
import hashlib
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
    normal_manifests: List[Dict],
    reversed_manifests: Optional[List[Dict]],
    tasks_yaml: Optional[Dict],
    time_limit: int,
) -> Dict:
    """Build a full engine config with three randomized trials."""
    trials: Dict[str, Dict] = {}

    normal_scenes: List[Dict] = []
    for manifest in normal_manifests:
        normal_scenes.extend(_scene_candidates(manifest, "sfp_sc_cable"))

    reversed_source = (
        reversed_manifests
        if reversed_manifests is not None and len(reversed_manifests) > 0
        else normal_manifests
    )
    reversed_scenes: List[Dict] = []
    for manifest in reversed_source:
        reversed_scenes.extend(_scene_candidates(manifest, "sfp_sc_cable_reversed"))

    if len(normal_scenes) < 2:
        raise ValueError("Need at least two normal cable scenes to build trial_1 and trial_2")
    if len(reversed_scenes) < 1:
        raise ValueError("Need at least one reversed cable scene to build trial_3")

    selected_normal = random.sample(normal_scenes, 2)
    selected_reversed = random.choice(reversed_scenes)
    chosen_scenes = [selected_normal[0], selected_normal[1], selected_reversed]

    for trial_index, scene_entry in enumerate(chosen_scenes, start=1):
        scene_config = scene_entry["config"]
        scene_index = int(scene_entry.get("index", -1))
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


def _task_candidates_for_scene_entry(
    scene_entry: Dict,
    tasks_yaml: Optional[Dict],
    time_limit: int,
) -> List[Dict[str, object]]:
    """Resolve task candidates for a scene entry from tasks YAML or scene config."""
    scene_config = scene_entry["config"]
    scene_index = int(scene_entry.get("index", -1))
    if tasks_yaml is not None:
        return _tasks_from_tasks_yaml(tasks_yaml, scene_index)
    return _build_tasks_for_scene(scene_config, time_limit=time_limit)


def _estimate_max_unique_engine_configs(
    normal_manifests: List[Dict],
    reversed_manifests: Optional[List[Dict]],
    tasks_yaml: Optional[Dict],
    time_limit: int,
) -> int:
    """Estimate discrete max unique full configs from manifest pool.

    This estimate uses scene-task combinations only and ignores randomized gripper
    offset values in scene blocks.
    """
    normal_scenes: List[Dict] = []
    for manifest in normal_manifests:
        normal_scenes.extend(_scene_candidates(manifest, "sfp_sc_cable"))

    reversed_source = (
        reversed_manifests
        if reversed_manifests is not None and len(reversed_manifests) > 0
        else normal_manifests
    )
    reversed_scenes: List[Dict] = []
    for manifest in reversed_source:
        reversed_scenes.extend(_scene_candidates(manifest, "sfp_sc_cable_reversed"))

    if len(normal_scenes) < 2 or len(reversed_scenes) < 1:
        return 0

    normal_task_counts: List[int] = [
        len(_task_candidates_for_scene_entry(scene, tasks_yaml, time_limit))
        for scene in normal_scenes
    ]
    reversed_task_counts: List[int] = [
        len(_task_candidates_for_scene_entry(scene, tasks_yaml, time_limit))
        for scene in reversed_scenes
    ]

    # Ordered trial pairs (trial_1, trial_2) use distinct normal scenes: i != j.
    normal_sum = sum(normal_task_counts)
    normal_square_sum = sum(count * count for count in normal_task_counts)
    normal_ordered_pair_task_combos = normal_sum * normal_sum - normal_square_sum
    reversed_task_combo_sum = sum(reversed_task_counts)

    return normal_ordered_pair_task_combos * reversed_task_combo_sum


def _load_manifest_json(path: Path) -> Dict:
    """Load and validate one manifest file."""
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Manifest must be a JSON object: {path}")
    return loaded


def _build_indexed_output_path(base_output: Path, index: int, total: int) -> Path:
    """Build output path for one file, adding an index suffix when total > 1."""
    if total == 1:
        return base_output
    return base_output.with_name(
        f"{base_output.stem}_{index:03d}{base_output.suffix}"
    )


def _engine_config_signature(engine_config: Dict) -> str:
    """Create a stable fingerprint for uniqueness checks across generated files."""
    normalized = json.dumps(engine_config, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


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
        nargs="+",
        default=None,
        help="One or more paths to normal or combined scene manifest JSON files",
    )
    parser.add_argument(
        "--reversed_manifest",
        type=Path,
        nargs="+",
        default=None,
        help="Optional one or more paths to reversed-cable scene manifest JSON files",
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
    parser.add_argument(
        "--num_engine_configs",
        type=int,
        default=1,
        help=(
            "Number of full engine config files to generate "
            "(applies to engine_config and random_engine_config modes only; default: 1)"
        ),
    )
    parser.add_argument(
        "--estimate_max_unique_only",
        action="store_true",
        help=(
            "Engine-config helper: print estimated discrete maximum number of unique "
            "full engine configs from manifest pool, then exit"
        ),
    )

    args = parser.parse_args()

    if args.time_limit <= 0:
        raise ValueError("--time_limit must be > 0")
    if args.num_engine_configs <= 0:
        raise ValueError("--num_engine_configs must be > 0")
    if args.estimate_max_unique_only and args.mode != "engine_config":
        raise ValueError("--estimate_max_unique_only is only valid when --mode engine_config")

    if args.mode == "tasks":
        if args.num_engine_configs != 1:
            raise ValueError("--num_engine_configs is only valid for full engine config modes")
        if args.normal_manifest is None:
            raise ValueError("--manifest is required when --mode tasks")
        if len(args.normal_manifest) != 1:
            raise ValueError("--mode tasks currently supports exactly one --manifest file")
        normal_manifest = _load_manifest_json(args.normal_manifest[0])
        trials, warnings = _manifest_to_trials(normal_manifest, time_limit=args.time_limit)
        yaml_text = _emit_trials_yaml(trials)
        output_paths = [args.output]
    elif args.mode == "engine_config":
        if args.normal_manifest is None:
            raise ValueError("--normal_manifest is required when --mode engine_config")
        normal_manifests = [_load_manifest_json(path) for path in args.normal_manifest]

        reversed_manifests = None
        if args.reversed_manifest is not None:
            reversed_manifests = [_load_manifest_json(path) for path in args.reversed_manifest]

        if not DEFAULT_SAMPLE_CONFIG.exists():
            raise FileNotFoundError(f"Sample config not found: {DEFAULT_SAMPLE_CONFIG}")

        sample_config = _load_yaml(DEFAULT_SAMPLE_CONFIG)
        tasks_yaml = _load_yaml(args.tasks_yaml) if args.tasks_yaml is not None else None

        estimate = _estimate_max_unique_engine_configs(
            normal_manifests=normal_manifests,
            reversed_manifests=reversed_manifests,
            tasks_yaml=tasks_yaml,
            time_limit=args.time_limit,
        )
        if args.estimate_max_unique_only:
            print(
                "Estimated max unique full engine configs from manifest pool "
                f"(discrete scene/task combinations, ignoring randomized gripper offsets): {estimate}"
            )
            return

        unique_signatures = set()
        generated_yaml_texts: List[str] = []
        max_attempts = max(200, args.num_engine_configs * 200)
        attempts = 0

        while len(generated_yaml_texts) < args.num_engine_configs and attempts < max_attempts:
            attempts += 1
            engine_config = _build_engine_config_from_manifests(
                sample_config=sample_config,
                normal_manifests=normal_manifests,
                reversed_manifests=reversed_manifests,
                tasks_yaml=tasks_yaml,
                time_limit=args.time_limit,
            )
            signature = _engine_config_signature(engine_config)
            if signature in unique_signatures:
                continue
            unique_signatures.add(signature)
            generated_yaml_texts.append(
                yaml.dump(
                    engine_config,
                    Dumper=EngineConfigDumper,
                    sort_keys=False,
                    default_flow_style=False,
                    width=120,
                )
            )

        if len(generated_yaml_texts) < args.num_engine_configs:
            raise RuntimeError(
                "Could not generate enough unique engine config files with the provided "
                f"manifest pool. Requested={args.num_engine_configs}, "
                f"generated={len(generated_yaml_texts)}"
            )

        output_paths = [
            _build_indexed_output_path(args.output, i + 1, args.num_engine_configs)
            for i in range(args.num_engine_configs)
        ]
        warnings = []
    else:
        if not DEFAULT_SAMPLE_CONFIG.exists():
            raise FileNotFoundError(f"Sample config not found: {DEFAULT_SAMPLE_CONFIG}")
        sample_config = _load_yaml(DEFAULT_SAMPLE_CONFIG)

        unique_signatures = set()
        generated_yaml_texts: List[str] = []
        max_attempts = max(200, args.num_engine_configs * 200)
        attempts = 0

        while len(generated_yaml_texts) < args.num_engine_configs and attempts < max_attempts:
            attempts += 1
            engine_config = copy.deepcopy(sample_config)
            engine_config["trials"] = _generate_random_engine_trials(time_limit=args.time_limit)
            signature = _engine_config_signature(engine_config)
            if signature in unique_signatures:
                continue
            unique_signatures.add(signature)
            generated_yaml_texts.append(
                yaml.dump(
                    engine_config,
                    Dumper=EngineConfigDumper,
                    sort_keys=False,
                    default_flow_style=False,
                    width=120,
                )
            )

        if len(generated_yaml_texts) < args.num_engine_configs:
            raise RuntimeError(
                "Could not generate enough unique random engine config files. "
                f"Requested={args.num_engine_configs}, generated={len(generated_yaml_texts)}"
            )

        output_paths = [
            _build_indexed_output_path(args.output, i + 1, args.num_engine_configs)
            for i in range(args.num_engine_configs)
        ]
        warnings = []

    if args.tasks_yaml is not None and not args.tasks_yaml.exists():
        raise FileNotFoundError(f"Tasks YAML not found: {args.tasks_yaml}")

    for output_path in output_paths:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.mode == "tasks":
        output_paths[0].write_text(yaml_text, encoding="utf-8")
    else:
        for output_path, yaml_text in zip(output_paths, generated_yaml_texts):
            output_path.write_text(yaml_text, encoding="utf-8")

    if args.mode == "tasks":
        print(f"Wrote {len(trials)} trial entries to: {output_paths[0]}")
    elif args.mode == "engine_config":
        if len(output_paths) == 1:
            print(f"Wrote engine config YAML to: {output_paths[0]}")
        else:
            print(
                f"Wrote {len(output_paths)} unique engine config YAML files with base: {args.output}"
            )
            for output_path in output_paths:
                print(f"  - {output_path}")
    else:
        if len(output_paths) == 1:
            print(f"Wrote engine config YAML to: {output_paths[0]}")
        else:
            print(
                "Wrote "
                f"{len(output_paths)} unique random engine config YAML files with base: {args.output}"
            )
            for output_path in output_paths:
                print(f"  - {output_path}")
    for warning in warnings:
        print(f"WARNING: {warning}")


if __name__ == "__main__":
    main()
