# Automated Scene Generation System - Complete Delivery

## Summary

You now have a fully automated system for generating unique Gazebo scenes and exporting them to MuJoCo format. This system handles the entire workflow end-to-end, allowing you to generate hundreds of diverse training scenarios with a single command.

## What Was Delivered

### Core Scripts

#### 1. **automate_scene_generation.py** (Main Automation)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/automate_scene_generation.py`

**Purpose:** Primary automation script that orchestrates the entire Gazebo-to-MuJoCo workflow.

**Features:**
- Generates unique random scene configurations
- Launches Gazebo with configured parameters
- Exports and processes SDF files
- Converts to MJCF with asset organization
- Applies cable plugin post-processing
- Exports to training directory with proper organization
- Generates scene manifest for reproduction

**Usage:**
```bash
python3 automate_scene_generation.py --num_scenes 5
```

**Output:**
- Organized scenes in `~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/`
- Exported scenes in `/mnt/hgfs/exported mujoco training envs/`
- Scene manifest JSON for tracking

---

#### 2. **test_scene_generation.py** (Validation & Testing)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/test_scene_generation.py`

**Purpose:** Comprehensive testing utility to verify setup and diagnose issues.

**Tests Available:**
- `dependencies` - Verify all packages installed
- `gazebo` - Test Gazebo launch and SDF export
- `conversion` - Test SDF to MJCF conversion
- `plugin` - Verify cable plugin processing
- `full` - Run all tests sequentially (recommended for first-time use)
- `all` - Same as full

**Usage:**
```bash
# First-time setup check
python3 test_scene_generation.py --test dependencies

# Full test pipeline
python3 test_scene_generation.py --test full
```

**Output:**
Clear pass/fail status for each component, helping diagnose setup issues.

---

#### 3. **reproduce_scenes.py** (Scene Reproducibility)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/reproduce_scenes.py`

**Purpose:** Load and analyze scene manifest to extract scene configurations.

**Capabilities:**
- List all scenes from manifest
- Extract specific scene parameters
- Validate saved configurations
- Prepare for scene re-export (future enhancement)

**Usage:**
```bash
# List all scenes
python3 reproduce_scenes.py \
  --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
  --list

# Get details for specific scenes
python3 reproduce_scenes.py \
  --manifest scene_manifest.json \
  --scenes 0 2 5
```

**Output:**
Scene configuration details in JSON format for analysis.

---

### Documentation Files

#### 4. **QUICKSTART.md** (Getting Started Guide)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/QUICKSTART.md`

**Purpose:** Fastest path to getting scenes generated.

**Contents:**
- Step-by-step quick start (3 steps)
- Common commands with examples
- File locations and structure
- Troubleshooting common issues
- Next steps and context

**Best For:** Users who want to start immediately without deep understanding.

---

#### 5. **AUTOMATE_README.md** (Comprehensive Guide)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/AUTOMATE_README.md`

**Purpose:** Detailed reference documentation for the automation system.

**Sections:**
- Overview of the complete workflow
- Usage with all parameters
- Output directory structure
- Randomization ranges and constraints
- Manifest file details
- Troubleshooting guide
- Performance notes
- Scene customization

**Best For:** Users who need detailed reference or want to customize behavior.

---

#### 6. **ARCHITECTURE.md** (Technical Deep Dive)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/ARCHITECTURE.md`

**Purpose:** Technical architecture and design documentation.

**Sections:**
- Component architecture and data flow
- Detailed component descriptions
- Data structures
- File organization
- Error handling strategy
- Performance characteristics
- Testing infrastructure
- Extension points for customization

**Best For:** Developers who need to understand internals or modify the system.

---

#### 7. **DELIVERY_SUMMARY.md** (This File)
**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/DELIVERY_SUMMARY.md`

**Purpose:** Overview of the complete delivery package.

---

## Quick Reference

### Installation & Setup

```bash
# Make scripts executable (if needed)
chmod +x ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/*.py

# Verify setup
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 test_scene_generation.py --test dependencies
```

### Generate Scenes

```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts

# Generate 5 scenes
python3 automate_scene_generation.py --num_scenes 5

# Generate 100 scenes with longer timeout
python3 automate_scene_generation.py --num_scenes 100 --export_timeout 180
```

### Inspect Results

```bash
# List all generated scenes
python3 reproduce_scenes.py \
  --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
  --list

# View directory structure
ls -la ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/

# Check exported files
ls -la /mnt/hgfs/exported\ mujoco\ training\ envs/
```

### View Scenes in MuJoCo

```bash
# Activate Python environment
pixi shell

# View a scene
python -m mujoco.viewer ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=.../mjcf/scene.xml
```

## File Structure

### Scripts Directory
```
~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/
├── automate_scene_generation.py    ★ Main script
├── test_scene_generation.py         ★ Testing utility
├── reproduce_scenes.py              ★ Scene analysis
├── add_cable_plugin.py              (existing)
├── load_aic_world.py                (existing)
├── view_scene.py                    (existing)
├── QUICKSTART.md                    ★ Quick start guide
├── AUTOMATE_README.md               ★ Detailed reference
└── ARCHITECTURE.md                  ★ Technical docs
```

### MJCF Output Directory
```
~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/
├── scene_manifest.json              # All configurations
├── robot_x=0p100_robot_y=0p200_.../
│   ├── sdf/
│   │   └── robot_x=0p100_....sdf    # Original SDF
│   └── mjcf/
│       ├── scene.xml               # ★ Use this to load
│       ├── aic_robot.xml
│       ├── aic_world.xml
│       └── *.obj, *.png            # Assets
└── ... (more scenes)
```

### Export Directory
```
/mnt/hgfs/exported mujoco training envs/
├── robot_x=0p100_robot_y=0p200_.../
│   ├── scene.xml                   # ★ Use this to load
│   ├── aic_robot.xml
│   ├── aic_world.xml
│   └── *.obj, *.png
└── ... (more scenes)
```

## Key Features

### 1. Unique Scene Generation ✓
- Generates N unique scenes with random parameters
- Ensures no duplicate configurations
- Tracks all parameters in manifest

### 2. Full Workflow Automation ✓
- Gazebo launch and export
- SDF corrections (URI fixes)
- MJCF conversion
- Asset organization
- Cable plugin processing
- Final export organization

### 3. Organized Output ✓
- Scenes named by their parameters
- Easy to identify scene characteristics
- Both local and network export paths
- Manifest JSON for tracking

### 4. Parameter Randomization ✓
- Robot position: x, y (z fixed for consistency)
- Task board position and orientation
- Cable configuration (type, position, orientation)
- Mount rail presence and positioning
- Randomization ranges match documented constraints

### 5. Testing & Validation ✓
- Comprehensive test suite
- Dependency verification
- Component-level testing
- Error reporting

### 6. Scene Reproducibility ✓
- Scene manifest saves all configurations
- Can extract parameters from any scene
- Enables analysis of generated diversity

## Workflow Stages (What Happens When You Generate)

### Stage 1: Configuration Generation
```
Generate N unique random configurations
↓
Verify uniqueness
↓
Save to scene_manifest.json
```

### Stage 2: Per-Scene Processing (repeated N times)
```
1. Launch Gazebo with parameters
        ↓
2. Wait for SDF export to /tmp/aic.sdf
        ↓
3. Fix SDF URIs (Issue 1 & 2)
        ↓
4. Create scene-specific directories
        ↓
5. Convert SDF → MJCF via sdf2mjcf
        ↓
6. Copy mesh assets (.obj, .png)
        ↓
7. Run add_cable_plugin.py
        ↓
8. Copy to /mnt/hgfs/exported mujoco training envs/
        ↓
9. Cleanup temp files
```

### Stage 3: Summary Report
```
Print processing statistics
Print file locations
Report success/failure count
```

## Performance Expectations

| Metric | Value |
|--------|-------|
| Time per scene | 2-3 minutes |
| 5 scenes | ~10-15 minutes |
| 10 scenes | ~20-30 minutes |
| 50 scenes | ~1.5-2.5 hours |
| 100 scenes | ~3-5 hours |

**Tip:** Run in background with nohup or tmux for long runs.

## Customization Options

### Parameter Ranges
Edit `generate_random_config()` in `automate_scene_generation.py`:

```python
def generate_random_config(self):
    config = SceneConfig(
        robot_x=random.uniform(-0.5, 0.0),  # Custom range
        # ... edit more ranges ...
    )
```

### Export Directory
Change export path in `OrchestrationManager.__init__()`:

```python
self.export_base_dir = Path("/your/custom/path")
```

### Timeout Values
Command-line parameter:

```bash
python3 automate_scene_generation.py --num_scenes 5 --export_timeout 180
```

## Troubleshooting

### Common Issues

| Issue | Fix |
|-------|-----|
| "sdf2mjcf not found" | `sudo apt install -y python3-sdformat16 python3-gz-math9` |
| Gazebo export timeout | Increase: `--export_timeout 180` |
| "Cannot find add_cable_plugin.py" | Verify: `ls -la scripts/add_cable_plugin.py` |
| Export directory not mounted | Create: `mkdir -p /mnt/hgfs/exported\ mujoco\ training\ envs` |
| Scene generation fails | Run: `python3 test_scene_generation.py --test full` |

### Debug Mode

Monitor progress in real-time:
```bash
# Terminal 1: Run generation
python3 automate_scene_generation.py --num_scenes 10 | tee generation.log

# Terminal 2: Monitor progress
tail -f generation.log

# Terminal 3: Check disk usage
watch -n 2 'du -sh ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf'
```

## Next Steps

1. **Verify Setup**
   ```bash
   cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
   python3 test_scene_generation.py --test dependencies
   ```

2. **Generate Test Scenes**
   ```bash
   python3 automate_scene_generation.py --num_scenes 2
   ```

3. **View Generated Scenes**
   ```bash
   pixi shell
   python -m mujoco.viewer ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/robot_x=.../mjcf/scene.xml
   ```

4. **Scale Up**
   ```bash
   python3 automate_scene_generation.py --num_scenes 100
   ```

## Documentation Cross-Reference

| Need | Document | Section |
|------|----------|---------|
| Quick start | QUICKSTART.md | Quick Start Steps |
| Detailed parameters | AUTOMATE_README.md | Randomization Ranges |
| File locations | QUICKSTART.md | Where Are My Files? |
| Architecture | ARCHITECTURE.md | Component Architecture |
| Error solutions | AUTOMATE_README.md | Troubleshooting |
| Customization | ARCHITECTURE.md | Extension Points |
| Performance info | QUICKSTART.md | Performance Notes |
| Testing | QUICKSTART.md | Test Your Setup |

## Support Resources

- **Main README:** `/home/intrinsic/ws_aic/src/aic/aic_utils/aic_mujoco/README.md`
- **Scene Description:** `/home/intrinsic/ws_aic/src/aic/docs/scene_description.md`
- **Task Board Details:** `/home/intrinsic/ws_aic/src/aic/docs/task_board_description.md`
- **Launch Parameters:** `/home/intrinsic/ws_aic/src/aic/aic_bringup/README.md`

## Summary

You have everything needed to:
✓ Generate unique Gazebo scenes
✓ Export to MuJoCo MJCF format
✓ Organize scenes by parameters
✓ Create diverse training datasets
✓ Reproduce specific scenes
✓ Validate your setup

**Ready to start?** See the Quick Start section or run:
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 automate_scene_generation.py --num_scenes 5
```

---

**Questions?** Check the relevant documentation file or review the script comments for implementation details.

**Issues?** Run diagnostic tests:
```bash
python3 test_scene_generation.py --test full
```
