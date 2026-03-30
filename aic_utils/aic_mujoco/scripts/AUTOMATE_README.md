# Automated Scene Generation Script

This script automates the complete Gazebo to MuJoCo scene generation workflow.

## Overview

The automation script performs the following steps for each scene:

1. **Export from Gazebo**: Launches Gazebo with randomized parameters and exports the scene to `/tmp/aic.sdf`
2. **Fix SDF**: Applies fixes for corrupted URIs and broken mesh references
3. **Convert to MJCF**: Uses `sdf2mjcf` to convert SDF to MJCF format
4. **Organize Assets**: Copies mesh assets (.obj, .png) to the scene directory
5. **Apply Cable Plugin**: Runs `add_cable_plugin.py` to split and refine MJCF files
6. **Export**: Copies organized scenes to `/mnt/hgfs/exported mujoco training envs`

## Usage

### Quick Start

Generate 5 unique scenes:

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 automate_scene_generation.py --num_scenes 5
```

### Advanced Usage

```bash
python3 automate_scene_generation.py \
  --num_scenes 10 \
  --ws_path ~/ws_aic \
  --export_timeout 120
```

### Parameters

- `--num_scenes` (required): Number of unique scenes to generate
- `--ws_path` (optional): Path to ROS 2 workspace (default: `~/ws_aic`)
- `--export_timeout` (optional): Timeout in seconds for each Gazebo export (default: 120)

## Output Directory Structure

After running the script, the following structure is created:

### In `~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/`

```
mjcf/
├── scene_manifest.json                    # Manifest of all generated scenes
├── robot_x=X_robot_y=Y_..../
│   ├── sdf/
│   │   └── robot_x=X_robot_y=Y_....sdf    # Original exported SDF
│   └── mjcf/
│       ├── scene.xml                      # Top-level scene file
│       ├── aic_robot.xml                  # Robot definition
│       ├── aic_world.xml                  # World/environment definition
│       ├── *.obj                          # Mesh assets
│       └── *.png                          # Texture assets
├── robot_x=X2_robot_y=Y2_..../
│   ├── sdf/
│   └── mjcf/
└── ...
```

### In `/mnt/hgfs/exported mujoco training envs/`

```
exported mujoco training envs/
├── robot_x=X_robot_y=Y_..../
│   ├── scene.xml
│   ├── aic_robot.xml
│   ├── aic_world.xml
│   ├── *.obj
│   └── *.png
├── robot_x=X2_robot_y=Y2_..../
│   ├── scene.xml
│   ├── aic_robot.xml
│   ├── aic_world.xml
│   ├── *.obj
│   └── *.png
└── ...
```

## Scene Naming Convention

Scenes are named based on key configuration parameters to ensure uniqueness:

```
robot_x=0.100_robot_y=0.200_robot_z=1.140_tb_x=0.200_...
```

Parameters included in the name:
- Robot position (x, y, z)
- Task board position (x, y) and orientation (yaw)
- Cable configuration (if present)
- Mount rail translations (if present)

## Randomization Ranges

The script generates scenes with parameters within these ranges:

- **Robot Position**:
  - x: [-0.3, -0.1] meters
  - y: [0.1, 0.3] meters
  - z: 1.14 m (fixed)
  - Roll, pitch: 0.0 (fixed)
  - Yaw: -π (fixed)

- **Task Board Position**:
  - x: [0.1, 0.3] meters
  - y: [-0.3, -0.1] meters
  - z: 1.14 m (fixed)
  - Roll, pitch: 0.0 (fixed)
  - Yaw: [-0.5, 0.5] radians

- **Cable Configuration**:
  - spawn_cable: Randomly true/false (higher probability true)
  - cable_type: Randomly `sfp_sc_cable` or `sfp_sc_cable_reversed`
  - cable_x: [0.15, 0.19] meters
  - cable_y: [0.0, 0.05] meters
  - cable_roll: [0.3, 0.6] radians
  - cable_pitch: [-0.6, -0.3] radians
  - cable_yaw: [1.0, 1.66] radians
  - attach_cable_to_gripper: Randomly true/false

- **Mount Rails**:
  - LC/SFP/SC mounts: Randomly present
  - SFP/SC translation: [-0.09625, 0.09625] meters
  - LC translation: [-0.188, 0.188] meters
  - Mount rotations: [-60°, +60°] in radians

See [Task Board Description](../../docs/task_board_description.md) for detailed constraints.

## Manifest File

The script generates a `scene_manifest.json` file containing:

```json
{
  "num_scenes": 5,
  "scenes": [
    {
      "index": 0,
      "name": "robot_x=0.100_robot_y=0.200_...",
      "config": {
        "robot_x": 0.1,
        "robot_y": 0.2,
        ...
      }
    },
    ...
  ]
}
```

This manifest allows you to:
- Reproduce specific scenes
- Track which parameters were used
- Analyze scene statistics

## Troubleshooting

### Gazebo Export Timeout

If scenes are not exporting within the timeout:

```bash
# Increase timeout to 180 seconds
python3 automate_scene_generation.py --num_scenes 5 --export_timeout 180
```

### Cable Plugin Processing Fails

Ensure the `add_cable_plugin.py` script exists:

```bash
ls -la ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/add_cable_plugin.py
```

If it doesn't exist, the script logs a warning and skips cable plugin processing.

### Missing Export Directory

The script logs a warning but continues if `/mnt/hgfs/exported mujoco training envs` doesn't exist. Create it or mount the network drive before running:

```bash
# Check if mounted
ls -la /mnt/hgfs/

# If not mounted, mount the network share (adjust path as needed)
sudo mount -t vmhgfs .host:/ /mnt/hgfs
```

### SDF Export Not Found

If Gazebo doesn't export the SDF:

1. Check that Gazebo is properly installed and can be launched manually
2. Verify the workspace is properly sourced
3. Try manually launching with one of the generated parameter sets
4. Increase the export timeout: `--export_timeout 180`

## Viewing Generated Scenes

After generation, you can view scenes in MuJoCo:

```bash
# Enter pixi shell
pixi shell

# View a specific scene
python -m mujoco.viewer ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=0p100_.../mjcf/scene.xml

# Or use the simulate binary (if Part 2 is set up)
simulate ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=0p100_.../mjcf/scene.xml
```

## Modifying Randomization

To customize randomization ranges, edit the `generate_random_config()` method in the script:

```python
def generate_random_config(self) -> SceneConfig:
    """Generate a unique random scene configuration."""
    config = SceneConfig(
        # Modify these ranges:
        robot_x=random.uniform(-0.4, 0.0),  # Wider range
        robot_y=random.uniform(0.0, 0.4),
        # ...
    )
```

Then run the script again with the modified ranges.

## Performance Notes

- Each scene export takes approximately 2-3 minutes (120s Gazebo launch + processing)
- Total time for N scenes: approximately 2-3N minutes
- For 10 scenes: 20-30 minutes
- For 100 scenes: 200-300 minutes
- Run with `--num_scenes 1` first to verify setup

## Logging

All operations are logged with timestamps and levels (INFO, WARNING, ERROR). Check the terminal output for detailed progress information.

## Contact

For issues or questions about this automation script, refer to the main [aic_mujoco README](../README.md) and [Scene Generation Workflow](../README.md#scene-generation-workflow) section.
