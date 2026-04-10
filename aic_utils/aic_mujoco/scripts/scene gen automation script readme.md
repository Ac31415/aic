# MuJoCo Scene Automation Scripts Usage

This document covers usage for both scripts:

- `src/aic/aic_utils/aic_mujoco/scripts/automate_scene_generation.py`
- `src/aic/aic_utils/aic_mujoco/scripts/automate_scene_generation_macos_vmware_fusion_ubuntu24_arm.py`

Both scripts automate the Gazebo -> SDF -> MJCF pipeline with randomized scene parameters.

## What The Scripts Do

- Generate randomized AIC scene configurations.
- Launch Gazebo using `aic_bringup` with generated launch args.
- Wait for `/tmp/aic.sdf` export.
- Apply required SDF URI fixes.
- Convert SDF to MJCF via `sdf2mjcf`.
- Organize mesh and texture assets into scene output folders.
- Use compact scene folder names with a hash suffix to avoid filesystem path-length failures.
- Run `add_cable_plugin.py` post-processing.
- Save a manifest file: `src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json`.

## Script Differences

- `automate_scene_generation.py`
- Writes scene outputs under `src/aic/aic_utils/aic_mujoco/mjcf`.
- Export-to-VMware folder copy step is currently disabled as this script is for development that's local to ubuntu OS.

- `automate_scene_generation_macos_vmware_fusion_ubuntu24_arm.py`
- Writes scene outputs under `src/aic/aic_utils/aic_mujoco/mjcf`.
- Also tries to copy outputs to `/mnt/hgfs/exported mujoco training envs` for transferring exported mujoco scene files to host system.

## Required Two-Terminal Setup

Use exactly 2 terminals.

### Terminal 1: Start Zenoh Daemon

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
ros2 run rmw_zenoh_cpp rmw_zenohd
```

### Terminal 2: Run Automation Script

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
```

Then run one of the scripts (examples below).

## CLI Options

Both scripts support:

- `--num_scenes <int>`
- Required. Number of scenes to generate.

- `--ws_path <path>`
- Optional. Workspace path. Default: `~/ws_aic`.

- `--export_timeout <seconds>`
- Optional. Timeout for each Gazebo export. Default: `120`.

- `--gazebo_gui <true|false>`
- Optional. Show Gazebo GUI. Default: `true`.

- `--launch_rviz <true|false>`
- Optional. Launch RViz. Default: `false`.

- `--enabled_present_params <csv|none>`
- Optional. Controls which `*_present` flags are allowed to randomize to `True`.
- Any listed flag can be `True` or `False` randomly.
- Any unlisted flag is forced to `False`.
- If omitted: all supported `*_present` flags are enabled.
- If `none`: all supported `*_present` flags are forced `False`.

- `--cable_types <csv>`
- Optional. Allowed cable types: `sfp_sc_cable`, `sfp_sc_cable_reversed`.
- If omitted: cable type remains randomized between both types.

Supported `*_present` names for `--enabled_present_params`:

- `lc_mount_rail_0_present`
- `sfp_mount_rail_0_present`
- `sc_mount_rail_0_present`
- `lc_mount_rail_1_present`
- `sfp_mount_rail_1_present`
- `sc_mount_rail_1_present`
- `sc_port_0_present`
- `sc_port_1_present`
- `nic_card_mount_0_present`
- `nic_card_mount_1_present`
- `nic_card_mount_2_present`
- `nic_card_mount_3_present`
- `nic_card_mount_4_present`

## Example Usage

### 1) Default Randomization (both cable types)

```bash
python3 automate_scene_generation.py \
	--num_scenes 5 \
	--gazebo_gui false \
	--launch_rviz false
```

### 2) macOS/VMware variant with default randomization

```bash
python3 automate_scene_generation_macos_vmware_fusion_ubuntu24_arm.py \
	--num_scenes 5 \
	--gazebo_gui false \
	--launch_rviz false
```

### 3) Allow only specific `*_present` parameters to be enabled

```bash
python3 automate_scene_generation_macos_vmware_fusion_ubuntu24_arm.py \
	--num_scenes 5 \
	--gazebo_gui false \
	--launch_rviz false \
	--enabled_present_params sc_port_0_present,nic_card_mount_2_present
```

### 4) Force cable type to normal only

```bash
python3 automate_scene_generation.py \
	--num_scenes 5 \
	--gazebo_gui false \
	--launch_rviz false \
	--cable_types sfp_sc_cable
```

### 5) Force cable type to reversed only

```bash
python3 automate_scene_generation.py \
	--num_scenes 5 \
	--gazebo_gui false \
	--launch_rviz false \
	--cable_types sfp_sc_cable_reversed
```

### 6) Combined controls

```bash
python3 automate_scene_generation.py \
	--num_scenes 10 \
	--gazebo_gui false \
	--launch_rviz false \
	--enabled_present_params sc_port_0_present,sc_port_1_present,nic_card_mount_2_present \
	--cable_types sfp_sc_cable,sfp_sc_cable_reversed
```

<!-- ## Known Limitation (add_cable_plugin)

Due to current behavior in `src/aic/aic_utils/aic_mujoco/scripts/add_cable_plugin.py`, the following error can occur, especially when cable type is `sfp_sc_cable_reversed`:

```text
2026-04-05 03:49:08,179 - __main__ - ERROR - Cable plugin processing failed: Traceback (most recent call last):
	File "/home/intrinsic/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/add_cable_plugin.py", line 784, in main
		xml_str = world_spec.to_xml()
							^^^^^^^^^^^^^^^^^^^
ValueError: Error: engine error: This body does not have the requested plugin instance
```

If you need stable generation runs, prefer normal cable only:

```bash
--cable_types sfp_sc_cable
``` -->

## Output Layout

Generated content is organized under:

- `src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json`
- `src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/sdf/`
- `src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/mjcf/`

## Compact Scene Folder Names (New)

To prevent `File name too long` errors, scene folder names are compact and include a short hash.

Format:

```text
rz=<...>_tbx=<...>_tby=<...>_tbyaw=<...>_c=<...>_<hash10>
```

Example:

```text
rz=1p140_tbx=0p168_tby=m0p273_tbyaw=0p067_c=sfp_sc_cable_411807b54e
```

Token meaning:

- `rz`: `robot_z` rounded to 3 decimals.
- `tbx`: `task_board_x` rounded to 3 decimals.
- `tby`: `task_board_y` rounded to 3 decimals.
- `tbyaw`: `task_board_yaw` rounded to 3 decimals.
- `c`: `cable_type`.
- `<hash10>`: first 10 chars of SHA-1 over the full config JSON, used to keep names short and unique.

Encoding used in compact names:

- `p` means decimal point (`.`).
- `m` means minus sign (`-`).

So:

- `1p140` means `1.140`
- `m0p273` means `-0.273`

Important:

- Folder name tokens are a compact summary only (rounded values).
- The canonical exact values are in `scene_manifest.json`.

## How To Find Exact Parameter Values

Use this workflow to get exact (non-rounded) values for any scene folder:

1. Identify the scene folder name, for example:
	`rz=1p140_tbx=0p168_tby=m0p273_tbyaw=0p067_c=sfp_sc_cable_411807b54e`
2. Open `src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json`.
3. Find the matching scene object where `name` equals that folder name.
4. Read all exact values under that scene's `config` object.

Quick command (requires `jq`):

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf
jq '.scenes[] | select(.name=="rz=1p140_tbx=0p168_tby=m0p273_tbyaw=0p067_c=sfp_sc_cable_411807b54e") | .config' scene_manifest.json
```

You can also inspect per-scene generated files:

- `src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/sdf/<scene_name>.sdf`
- `src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/mjcf/scene.xml`

But for exact randomization parameters used by the generator, `scene_manifest.json` is the source of truth.

## Use Exported Scenes In `aic_mujoco`

This section explains how to run MuJoCo with scene assets generated by the automation scripts.

### macOS (VMware export path)

On macOS, it is highly recommended to do this from a `pixi` shell environment.

1. Move or copy all exported scene assets from your saved export location (for example `ws_aic/exported mujoco training envs/<scene_name>` or any equivalent location on your system) into:
	`~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf`
2. The target `mjcf` folder should contain `scene.xml`, `aic_world.xml`, `aic_robot.xml`, plus referenced meshes/textures for the scene you want to run.

Example copy command:

```bash
cp -r "/path/to/exported mujoco training envs/<scene_name>/"* ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/
```

Then use two terminals.

Terminal 1:

```bash
source ~/ws_aic/install/setup.zsh
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
ros2 run rmw_zenoh_cpp rmw_zenohd
```

Terminal 2:

```bash
colcon build --packages-select aic_mujoco

source ~/ws_aic/install/setup.zsh
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
ros2 launch aic_mujoco aic_mujoco_bringup.launch.py
```

### Ubuntu (native source build or pixi)

On Ubuntu, you can do the same either natively (if built from source) or from the `pixi` environment.

1. Move or copy all generated scene assets from:
	`~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/mjcf/`
	to:
	`~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf`
2. This places the scene entry files and assets where `aic_mujoco_bringup` expects them.

Example copy command:

```bash
cp -r ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/<scene_name>/mjcf/* ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/
```

Then use two terminals.

Terminal 1:

```bash
source ~/ws_aic/install/setup.zsh
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
ros2 run rmw_zenoh_cpp rmw_zenohd
```

Terminal 2:

```bash
colcon build --packages-select aic_mujoco

source ~/ws_aic/install/setup.zsh
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'
ros2 launch aic_mujoco aic_mujoco_bringup.launch.py
```
