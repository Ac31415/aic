# Quick Start: Automated Scene Generation

This guide gets you started with automated Gazebo to MuJoCo scene generation in minutes.

## Prerequisites

Ensure you have:
- ✓ ROS 2 (Kilted) installed
- ✓ Gazebo with the AIC simulation environment set up
- ✓ MuJoCo conversion tools (`sdf2mjcf`)
- ✓ Cable plugin script (`add_cable_plugin.py`)

> **First time?** Run the test suite first to verify everything is set up correctly:
> ```bash
> cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
> python3 test_scene_generation.py --test dependencies
> ```

## Quick Start Steps

### 1. Test Your Setup (Optional but Recommended)

On your **first run**, test all components:

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts

# Test dependencies
python3 test_scene_generation.py --test dependencies

# Test full pipeline (takes ~15 minutes)
python3 test_scene_generation.py --test all
```

Expected output:
```
✓ All dependencies found
✓ Gazebo launch successful
✓ SDF export successful  
✓ SDF conversion successful
✓ Cable plugin script found
```

### 2. Generate Scenes

Generate 5 unique scenes:

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts

python3 automate_scene_generation.py --num_scenes 5
```

**Expected behavior:**
- Gazebo launches for each scene (~2-3 minutes per scene)
- SDF files are exported and processed
- MJCF files are generated with assets
- Cabinet plugin processing is applied
- Files are organized and exported

**Monitor progress:** The script logs detailed progress to the terminal. Each scene takes approximately 2-3 minutes.

### 3. Generate More Scenes

To generate 10, 50, 100, or more scenes:

```bash
# Generate 10 scenes
python3 automate_scene_generation.py --num_scenes 10

# Generate 100 scenes (takes ~3-5 hours)
python3 automate_scene_generation.py --num_scenes 100
```

> **Tip:** Run in a terminal multiplexer (tmux/screen) or background process:
> ```bash
> nohup python3 automate_scene_generation.py --num_scenes 100 > generation.log 2>&1 &
> # View progress: tail -f generation.log
> ```

## Where Are My Files?

After generation, files are organized in two locations:

### Local (for development/viewing):
```
~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/
├── scene_manifest.json              # All scene configurations
├── robot_x=0p100_robot_y=0p200_.../
│   ├── sdf/
│   │   └── *.sdf                    # Original exported SDF
│   └── mjcf/
│       ├── scene.xml                # Main scene file ★ Use this
│       ├── aic_robot.xml            # Robot definition
│       ├── aic_world.xml            # Environment definition
│       └── *.obj, *.png             # Mesh assets
└── ... more scenes ...
```

### Exported (for training):
```
/mnt/hgfs/exported mujoco training envs/
├── robot_x=0p100_robot_y=0p200_.../
│   ├── scene.xml                    # Main scene file ★ Use this
│   ├── aic_robot.xml
│   ├── aic_world.xml
│   └── *.obj, *.png
└── ... more scenes ...
```

## View Generated Scenes

### Option 1: Using MuJoCo Viewer (Python)

```bash
# Activate Python environment
pixi shell

# View a specific scene
python -m mujoco.viewer ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=0p100_.../mjcf/scene.xml
```

**Controls in viewer:**
- **Space**: Start/pause simulation
- **Right-click drag**: Rotate view
- **Scroll**: Zoom
- **Backspace**: Reset

### Option 2: Using MuJoCo Simulate Binary

```bash
# If Part 2 is set up (with ros2_control)
source ~/ws_aic/install/setup.bash
simulate ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=0p100_.../mjcf/scene.xml
```

### Option 3: Drag and Drop

```bash
# Open MuJoCo viewer
pixi shell
python -m mujoco.viewer

# Then drag scene.xml file into the viewer window
```

## Common Tasks

### Find a Specific Scene

List all scenes and their configurations:

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts

python3 reproduce_scenes.py \
  --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
  --list
```

Output:
```
Scenes in manifest (5 total):

  [0] robot_x=0p100_robot_y=0p200_robot_z=1p140_tb_x=0p200_...
  [1] robot_x=0p150_robot_y=0p250_robot_z=1p140_tb_x=0p180_...
  [2] robot_x=0p120_robot_y=0p180_robot_z=1p140_tb_x=0p220_...
  [3] robot_x=0p130_robot_y=0p220_robot_z=1p140_tb_x=0p210_...
  [4] robot_x=0p140_robot_y=0p190_robot_z=1p140_tb_x=0p230_...
```

### Get Scene Configuration Details

The manifest JSON contains all parameters for each scene:

```bash
cat ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json | python -m json.tool | head -80
```

### Increase Export Timeout

If scenes aren't exporting properly, increase the timeout:

```bash
python3 automate_scene_generation.py --num_scenes 5 --export_timeout 180
```

### Use Custom Workspace Path

If your workspace is in a non-standard location:

```bash
python3 automate_scene_generation.py \
  --num_scenes 5 \
  --ws_path /path/to/my/workspace
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "sdf2mjcf not found" | Install: `sudo apt install python3-sdformat16 python3-gz-math9` |
| "Gazebo export timeout" | Increase timeout: `--export_timeout 180` |
| "Cable plugin not found" | Verify path: `ls ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/add_cable_plugin.py` |
| "Export directory not mounted" | Create dir: `mkdir -p /mnt/hgfs/exported\ mujoco\ training\ envs` |
| "Gazebo crashes during export" | Try with `--export_timeout 60` to end faster |

## Performance Notes

- **Per scene:** ~2-3 minutes (depends on hardware)
- **Total time:** ~(2-3) * num_scenes minutes
- **5 scenes:** ~10-15 minutes
- **10 scenes:** ~20-30 minutes  
- **100 scenes:** ~3-5 hours

**Run in background:**
```bash
nohup python3 automate_scene_generation.py --num_scenes 100 > scene_gen.log 2>&1 &

# Monitor progress
tail -f scene_gen.log

# Get just errors
grep -i error scene_gen.log
```

## Next Steps

- **View scenes** in MuJoCo viewer (see "View Generated Scenes" above)
- **Use scenes for training** by pointing your training script to the export directory
- **Analyze configurations** using the manifest JSON file
- **Reproduce specific scenes** using the manifest and `reproduce_scenes.py`
- **Customize parameters** by editing `automate_scene_generation.py`

## Files Reference

| File | Purpose |
|------|---------|
| `automate_scene_generation.py` | Main automation script |
| `test_scene_generation.py` | Testing and validation utility |
| `reproduce_scenes.py` | Regenerate scenes from manifest |
| `AUTOMATE_README.md` | Detailed automation documentation |
| `add_cable_plugin.py` | Cable plugin post-processor |

## More Information

- **Detailed documentation:** [AUTOMATE_README.md](AUTOMATE_README.md)
- **Scene generation workflow:** [README.md](../README.md#scene-generation-workflow)
- **Task board constraints:** [task_board_description.md](../../docs/task_board_description.md)
- **Launch parameters:** [aic_bringup README](../../aic_bringup/README.md)

---

**Ready?** Start generating scenes now:
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 automate_scene_generation.py --num_scenes 5
```

**Questions?** Check the [AUTOMATE_README.md](AUTOMATE_README.md) for comprehensive documentation.
