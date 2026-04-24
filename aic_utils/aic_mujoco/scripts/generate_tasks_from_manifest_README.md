# generate_tasks_from_manifest.py

This document explains all features of [generate_tasks_from_manifest.py](generate_tasks_from_manifest.py), including exactly how to run it step by step.

## What This Script Does

The script can generate three kinds of YAML outputs:

1. Task-only YAML from scene manifest JSON.
2. Full engine config YAML from manifest scenes, with output format matching [sample_config.yaml](../../../aic_engine/config/sample_config.yaml).
3. Full engine config YAML from freshly randomized scenes (no manifest input required), also matching [sample_config.yaml](../../../aic_engine/config/sample_config.yaml).

It supports normal cable scenes and reversed cable scenes:

- Normal cable type: sfp_sc_cable
- Reversed cable type: sfp_sc_cable_reversed

## Key Features And Functionalities

### 1. Multi-mode operation

- Mode tasks: emits only the trials.tasks hierarchy.
- Mode engine_config: builds a full engine configuration by selecting random trials from manifest data.
- Mode random_engine_config: builds a full engine configuration from freshly randomized scene values.

### 2. Task generation rules

For each scene config:

- If cable_type is sfp_sc_cable:
  - Creates tasks for each present nic_card_mount_i.
  - Uses both sfp_port_0 and sfp_port_1 for each present NIC target.
- If cable_type is sfp_sc_cable_reversed:
  - Creates tasks for each present sc_port_i.
  - Uses sc_tip -> sc_port_base insertion semantics.

### 3. Full engine config compatibility

When output is engine_config or random_engine_config:

- The script loads [sample_config.yaml](../../../aic_engine/config/sample_config.yaml) internally via a default path.
- You do not need to pass a sample config argument.
- It preserves top-level schema fields from the sample and replaces only trials.

### 4. Randomized scene generation for random_engine_config

The script randomizes scene geometry and entity states using ranges aligned with automation scripts:

- Task board x: [0.1, 0.3]
- Task board y: [-0.3, -0.1]
- Task board yaw: [-0.5, 0.5]
- Cable xyz and rpy around the expected nominal values
- Mount, SC port, and NIC translations and yaws within configured limits
- Gripper offset randomized in bounded ranges

It enforces at least one valid target per generated trial:

- Normal cable trial requires at least one nic_card_mount_i_present true.
- Reversed cable trial requires at least one sc_port_i_present true.

### 5. Trial selection behavior

- engine_config mode creates exactly 3 trials:
  - trial_1 and trial_2 from normal cable scenes
  - trial_3 from reversed cable scenes
- random_engine_config mode also creates exactly 3 trials with the same cable-type pattern.
- Exactly one task is chosen per trial in engine config outputs.

### 6. Optional tasks reuse

In engine_config mode, you can pass tasks YAML with --tasks_yaml.

- If provided, the script pulls task candidates for a selected scene from that file.
- If not provided, it computes task candidates directly from the selected scene config.

### 7. YAML formatting behavior

- Uses explicit True and False booleans in output.
- Preserves key order for full engine config output.
- Uses readable block-style YAML.

## File Inputs And Outputs

### Required and optional inputs by mode

- tasks
  - Required: --manifest (or --normal_manifest alias)
  - Optional: --time_limit
- engine_config
  - Required: --manifest (or --normal_manifest alias)
  - Optional: --reversed_manifest
  - Optional: --tasks_yaml
  - Optional: --time_limit
- random_engine_config
  - No manifest required
  - Optional: --time_limit

Always required:

- --output

### Typical input examples in this workspace

- Normal manifest: /mnt/hgfs/exported mujoco training envs/normal cable scenes/scene_manifest_cable_5.json
- Reversed manifest: /mnt/hgfs/exported mujoco training envs/reversed cable scenes/scene_manifest_cable_reversed_5.json

## CLI Reference

Run with:

```bash
python3 src/aic/aic_utils/aic_mujoco/scripts/generate_tasks_from_manifest.py [options]
```

Options:

- --mode
  - choices: tasks, engine_config, random_engine_config
  - default: tasks
- --manifest, --normal_manifest
  - path to normal or combined manifest JSON
- --reversed_manifest
  - optional reversed-cable manifest JSON
- --tasks_yaml
  - optional YAML generated in tasks mode
- --output
  - required output YAML path
- --time_limit
  - per-task time limit (seconds), default 180

## Step-by-step: How To Run

### Step 1: Open a terminal at workspace root

```bash
cd ~/ws_aic
```

### Step 2: (Optional) Verify Python dependencies

```bash
python3 -c "import yaml; print('PyYAML OK')"
```

If missing:

```bash
python3 -m pip install pyyaml
```

### Step 3: Generate task-only YAML from a manifest

```bash
python3 src/aic/aic_utils/aic_mujoco/scripts/generate_tasks_from_manifest.py \
  --mode tasks \
  --manifest "/mnt/hgfs/exported mujoco training envs/normal cable scenes/scene_manifest_cable_5.json" \
  --output /tmp/aic_tasks_from_manifest.yaml \
  --time_limit 180
```

Expected result:

- The script writes a trials.tasks YAML file.
- You may see WARNING lines for scenes that produce no valid tasks.

### Step 4: Generate full engine config from manifests

```bash
python3 src/aic/aic_utils/aic_mujoco/scripts/generate_tasks_from_manifest.py \
  --mode engine_config \
  --manifest "/mnt/hgfs/exported mujoco training envs/normal cable scenes/scene_manifest_cable_5.json" \
  --reversed_manifest "/mnt/hgfs/exported mujoco training envs/reversed cable scenes/scene_manifest_cable_reversed_5.json" \
  --output /tmp/aic_engine_config_from_manifests.yaml \
  --time_limit 180
```

Optional variant using pre-generated task candidates:

```bash
python3 src/aic/aic_utils/aic_mujoco/scripts/generate_tasks_from_manifest.py \
  --mode engine_config \
  --manifest "/mnt/hgfs/exported mujoco training envs/normal cable scenes/scene_manifest_cable_5.json" \
  --reversed_manifest "/mnt/hgfs/exported mujoco training envs/reversed cable scenes/scene_manifest_cable_reversed_5.json" \
  --tasks_yaml /tmp/aic_tasks_from_manifest.yaml \
  --output /tmp/aic_engine_config_from_manifests_with_tasks.yaml \
  --time_limit 180
```

Expected result:

- Full engine config YAML with scoring, task_board_limits, robot, and trials.
- Exactly three trials with one task per trial.

### Step 5: Generate full engine config from fresh random scenes

```bash
python3 src/aic/aic_utils/aic_mujoco/scripts/generate_tasks_from_manifest.py \
  --mode random_engine_config \
  --output /tmp/aic_random_engine_config.yaml \
  --time_limit 180
```

Expected result:

- Full engine config YAML in sample-config-compatible structure.
- Three randomized trials (2 normal cable, 1 reversed cable).

### Step 6: Inspect generated YAML

```bash
sed -n '1,220p' /tmp/aic_engine_config_from_manifests.yaml
```

or:

```bash
sed -n '1,220p' /tmp/aic_random_engine_config.yaml
```

## Error Handling And Validation Rules

The script raises explicit errors for common issues:

- Missing required manifest in tasks or engine_config mode.
- Manifest path does not exist.
- Internal sample config path does not exist.
- Invalid YAML top-level type when loading YAML files.
- Non-positive time limit.
- Not enough compatible scenes for engine_config mode:
  - fewer than 2 normal scenes
  - fewer than 1 reversed scene
- No task candidates for a selected scene.

## Notes

- In engine_config and random_engine_config modes, there is no sample config CLI argument anymore.
- The output keeps the same top-level format as [sample_config.yaml](../../../aic_engine/config/sample_config.yaml).
- For manifest-driven generation, scene selection and task selection are randomized, so repeated runs produce different trial picks.