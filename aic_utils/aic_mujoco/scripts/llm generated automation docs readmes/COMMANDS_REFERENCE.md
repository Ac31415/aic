# Quick Command Reference

## Location
```
~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/
```

## Core Commands

### Generate Scenes
```bash
# Generate 5 scenes (default)
python3 automate_scene_generation.py --num_scenes 5

# Generate 10 scenes with longer timeout
python3 automate_scene_generation.py --num_scenes 10 --export_timeout 180

# Generate 100 scenes in background
nohup python3 automate_scene_generation.py --num_scenes 100 > gen.log 2>&1 &

# Get help
python3 automate_scene_generation.py --help
```

### Test Setup
```bash
# Quick dependency check
python3 test_scene_generation.py --test dependencies

# Full diagnostic (recommended first-time)
python3 test_scene_generation.py --test full

# Individual tests
python3 test_scene_generation.py --test gazebo
python3 test_scene_generation.py --test conversion
python3 test_scene_generation.py --test plugin
```

### Analyze Scenes
```bash
# List all generated scenes
python3 reproduce_scenes.py \
  --manifest mjcf/scene_manifest.json \
  --list

# Get specific scenes (0, 1, and 3)
python3 reproduce_scenes.py \
  --manifest mjcf/scene_manifest.json \
  --scenes 0 1 3

# Get all scenes details
python3 reproduce_scenes.py \
  --manifest mjcf/scene_manifest.json \
  --all
```

## File Navigation

### Check Generation Status
```bash
# List generated scenes with sizes
ls -lh ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/

# Count scenes
ls ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/ | grep ^robot_ | wc -l

# Check export directory
ls -lh /mnt/hgfs/exported\ mujoco\ training\ envs/
```

### Monitor Long-Running Generation
```bash
# Start in background
nohup python3 automate_scene_generation.py --num_scenes 100 > gen.log 2>&1 &

# Monitor progress
tail -f gen.log

# Check for errors only
grep -i error gen.log

# Check completion
grep -i "completed\|workflow completed" gen.log
```

## View Generated Scenes

### Option 1: MuJoCo Viewer (Python)
```bash
# Activate Python environment
pixi shell

# View scene from local directory
python -m mujoco.viewer \
  ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=.../mjcf/scene.xml

# Exit: Ctrl+C
```

### Option 2: MuJoCo Simulate (if Part 2 installed)
```bash
source ~/ws_aic/install/setup.bash
simulate ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=.../mjcf/scene.xml
```

### Option 3: Drag and Drop
```bash
pixi shell
python -m mujoco.viewer
# Then drag scene.xml file into window
```

## Documentation

### Quick Navigation
- **Getting Started:** QUICKSTART.md
- **Detailed Reference:** AUTOMATE_README.md  
- **Technical Details:** ARCHITECTURE.md
- **Overview:** DELIVERY_SUMMARY.md
- **Navigation Index:** README_AUTOMATION.md

### Open Documentation
```bash
# Open in editor
code ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/QUICKSTART.md

# Or view in terminal
cat ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/QUICKSTART.md
```

## Configuration

### Customize Randomization Ranges
Edit this method in `automate_scene_generation.py`:
```python
def generate_random_config(self) -> SceneConfig:
    config = SceneConfig(
        robot_x=random.uniform(-0.5, 0.0),  # Edit ranges here
        robot_y=random.uniform(0.0, 0.5),
        # ... edit more ranges ...
    )
```

### Change Export Timeout
```bash
# Use longer timeout (for slower systems)
python3 automate_scene_generation.py --num_scenes 5 --export_timeout 180

# Default is 120 seconds
python3 automate_scene_generation.py --num_scenes 5  # Same as --export_timeout 120
```

### Custom Workspace
```bash
python3 automate_scene_generation.py --num_scenes 5 --ws_path /path/to/workspace
```

## Troubleshooting Cheat Sheet

| Issue | Fix |
|-------|-----|
| "sdf2mjcf not found" | `sudo apt install python3-sdformat16 python3-gz-math9` |
| Timeout during export | `--export_timeout 180` |
| add_cable_plugin.py missing | Check: `ls scripts/add_cable_plugin.py` |
| Export directory not found | Create: `mkdir -p /mnt/hgfs/exported\ mujoco\ training\ envs` |
| Setup issues | Run: `test_scene_generation.py --test full` |

## Performance Baseline

```
Single Scene:        2-3 minutes
5 Scenes:           ~15 minutes
10 Scenes:          ~30 minutes
100 Scenes:         ~3-5 hours
1000 Scenes:        ~30-50 hours
```

## One-Liner Examples

```bash
# Quick 2-scene test
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts && python3 automate_scene_generation.py --num_scenes 2

# Generate 50 scenes with logging
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts && nohup python3 automate_scene_generation.py --num_scenes 50 > gen_$(date +%s).log 2>&1 &

# Test everything then generate 10 scenes
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts && python3 test_scene_generation.py --test dependencies && python3 automate_scene_generation.py --num_scenes 10

# Count generated scenes
ls ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/ | grep ^robot_ | wc -l

# View first generated scene
python -m mujoco.viewer $(ls -d ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_*/mjcf/scene.xml | head -1)
```

## Environment Variables

```bash
# Set for scene generation (usually set automatically)
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true;transport/shared_memory/transport_optimization/pool_size=536870912'

# Set for viewing scenes
source ~/ws_aic/install/setup.bash  # If using simulate binary
```

## File Manifest

```
scripts/
├── automate_scene_generation.py (26 KB) ← Main script
├── test_scene_generation.py     (12 KB) ← Testing
├── reproduce_scenes.py          (11 KB) ← Analysis
├── QUICKSTART.md                (7 KB)  ← Start here
├── AUTOMATE_README.md           (7 KB)  ← Reference
├── ARCHITECTURE.md              (15 KB) ← Technical
├── DELIVERY_SUMMARY.md          (13 KB) ← Overview
└── README_AUTOMATION.md         (~10KB) ← Index (this file)
```

## Quick Start Checklist

- [ ] `cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts`
- [ ] `python3 test_scene_generation.py --test dependencies`
- [ ] `python3 automate_scene_generation.py --num_scenes 2`
- [ ] Check `/mnt/hgfs/exported mujoco training envs/` for results
- [ ] View scene: `python -m mujoco.viewer <path>/scene.xml`
- [ ] Read QUICKSTART.md for more details

---

**Pro Tip:** Bookmark this file or keep it open while generating scenes!

For comprehensive documentation, see README_AUTOMATION.md
