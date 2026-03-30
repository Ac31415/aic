# Technical Architecture: Scene Generation Automation

This document describes the architecture, design, and implementation of the automated Gazebo to MuJoCo scene generation system.

## Overview

The system automates Steps 1-5 of the "Scene Generation Workflow" from the [aic_mujoco README](../README.md#scene-generation-workflow):

1. **Export from Gazebo** → Launches Gazebo and captures exported SDF
2. **Fix SDF** → Applies URI corrections  
3. **Convert to MJCF** → Uses `sdf2mjcf` tool
4. **Organize Assets** → Moves meshes to proper directory
5. **Process with Cable Plugin** → Runs `add_cable_plugin.py`

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  automate_scene_generation.py                  │
│                    (Main Orchestrator)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SceneGenerator ──────┐                                         │
│  (Unique configs)     │                                         │
│                       ├──→ OrchestrationManager                │
│  GazeboExporter ───────┤    (Processes scenes)                 │
│  (Launch & export)     │                                         │
│                        ├──→ SDF Pipeline                        │
│  SDFProcessor ─────────┤    ├─ SDF Fixes                       │
│  (Fix & rename)        │    ├─ MJCF Conversion                 │
│                        ├──→ Asset Management                    │
│  MJCFConverter ────────┤    ├─ Asset Organization              │
│  (sdf2mjcf tool)       │    ├─ Cable Plugin Processing         │
│                        ├──→ Export                              │
│  MJCFOrganizer ────────┤    └─ Directory Structure             │
│  (File management)     │                                         │
│                        │                                         │
│  CablePluginProcessor ─┼────→ add_cable_plugin.py              │
│  (Wrapper for script)  │                                         │
│                        │                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. SceneGenerator

**Purpose:** Generate unique random scene configurations.

**Key Methods:**
- `generate_random_config()` - Creates a random `SceneConfig` with unique parameters
- Prevents duplicate configurations

**Randomization Ranges:**
- Robot position: x ∈ [-0.3, -0.1], y ∈ [0.1, 0.3], z = 1.14
- Task board: x ∈ [0.1, 0.3], y ∈ [-0.3, -0.1], yaw ∈ [-0.5, 0.5]
- Cable parameters: All randomized (type, position, orientation)
- Mount configurations: Presence, translation, and rotation randomized

**Configuration Constraints:**
- Ensures each generated config is unique by tracking `scene_name`
- Updates based on task board and joint limits from documentation

### 2. GazeboExporter

**Purpose:** Launch Gazebo simulation and export SDF.

**Key Methods:**
- `export_scene(config, timeout)` - Launches Gazebo with parameters, exports SDF
- Uses ROS 2 launch with Zenoh communication

**Process:**
1. Builds ros2 launch command with parameters
2. Spawns subprocess with environment setup
3. Waits for SDF export (~30-60 seconds typically)
4. Terminates Gazebo process
5. Verifies SDF exists at `/tmp/aic.sdf`

**Timeout Handling:**
- Default: 120 seconds per scene
- Customizable via `--export_timeout` parameter
- Forcefully terminates if timeout exceeded

### 3. SDFProcessor

**Purpose:** Fix exported SDF and organize files.

**Key Methods:**
- `fix_sdf(sdf_path)` - Applies URI corrections (Issue 1 & 2 from README)
- `rename_sdf(source_sdf, scene_name, dest_dir)` - Renames and copies SDF

**Fixes Applied:**
```
Issue 1: file://<urdf-string>/model:// → model://
Issue 2: file:///lc_plug_visual.glb → model://LC Plug/lc_plug_visual.glb
         file:///sc_plug_visual.glb → model://SC Plug/sc_plug_visual.glb
         file:///sfp_module_visual.glb → model://SFP Module/sfp_module_visual.glb
```

**File Naming:**
- Original SDF: `/tmp/aic.sdf`
- Destination: `mjcf/{scene_name}/{sdf_name}.sdf`
- Scene name derived from configuration parameters

### 4. MJCFConverter

**Purpose:** Convert corrected SDF to MJCF format.

**Key Method:**
- `convert_to_mjcf(sdf_path, output_dir)` - Wraps `sdf2mjcf` CLI tool

**Process:**
1. Creates output directory
2. Executes: `sdf2mjcf {input.sdf} {output_dir}/aic_world.xml`
3. Waits up to 300 seconds for conversion
4. Verifies output files created

**Output Files:**
- `aic_world.xml` - Monolithic MJCF file
- `*.obj` - Mesh geometry files
- `*.png` - Texture files
- `*.mtl` - Material definitions

### 5. MJCFOrganizer

**Purpose:** Copy and organize MJCF files and assets.

**Key Method:**
- `organize_assets(source_dir, dest_dir)` - Copies .xml, .obj, .png files

**Destination Structure:**
```
mjcf/
└── {scene_name}/
    ├── mjcf/
    │   ├── aic_world.xml
    │   ├── *.obj
    │   ├── *.png
    │   └── *.mtl
```

### 6. CablePluginProcessor

**Purpose:** Apply cable plugin post-processing.

**Key Method:**
- `process_mjcf(mjcf_dir)` - Executes `add_cable_plugin.py`

**Process:**
1. Verifies script exists
2. Executes with parameters:
   - `--input mjcf/aic_world.xml`
   - `--output mjcf/aic_world.xml`
   - `--robot_output mjcf/aic_robot.xml`
   - `--scene_output mjcf/scene.xml`
3. Waits up to 300 seconds
4. Logs errors if processing fails

**Output Files Created:**
- `aic_robot.xml` - Robot-only definition
- `aic_world.xml` - Updated world file
- `scene.xml` - Top-level scene file (includes both)

### 7. ExportOrganizer

**Purpose:** Copy finalized scenes to export directory.

**Key Method:**
- `organize_scene(mjcf_dir, export_base_dir, scene_name)` - Copies to `/mnt/hgfs/exported mujoco training envs/`

**Export Structure:**
```
/mnt/hgfs/exported mujoco training envs/
└── {scene_name}/
    ├── scene.xml ★
    ├── aic_robot.xml
    ├── aic_world.xml
    ├── *.obj
    └── *.png
```

### 8. OrchestrationManager

**Purpose:** Orchestrates entire workflow for multiple scenes.

**Key Method:**
- `process_single_scene(config, index)` - Processes one scene through all steps
- `run()` - Main orchestration loop

**Workflow per Scene:**
1. Generate unique configuration
2. Export SDF from Gazebo
3. Apply SDF fixes
4. Create scene-specific directories
5. Convert to MJCF
6. Organize assets
7. Apply cable plugin
8. Copy to export directory
9. Cleanup temporary files

**Manifest Generation:**
- Saves `scene_manifest.json` with all configurations
- Enables scene reproduction and analysis

## Data Structures

### SceneConfig

```python
@dataclass
class SceneConfig:
    # Robot pose (6 DOF)
    robot_x, robot_y, robot_z: float
    robot_roll, robot_pitch, robot_yaw: float
    
    # Task board pose (6 DOF)
    task_board_x, task_board_y, task_board_z: float
    task_board_roll, task_board_pitch, task_board_yaw: float
    
    # Cable (when spawned)
    spawn_cable: bool
    cable_type: str  # 'sfp_sc_cable' or 'sfp_sc_cable_reversed'
    cable_x, cable_y, cable_z: float
    cable_roll, cable_pitch, cable_yaw: float
    attach_cable_to_gripper: bool
    
    # Mount rails (up to 5 each)
    sfp_mount_rail_0_present: bool
    sfp_mount_rail_0_translation: float
    sfp_mount_rail_0_roll: float
    # ... (SC, LC, NIC, SC port mounts follow same pattern)
```

## File Organization

### Workspace (Development)
```
ws_aic/
└── src/aic/aic_utils/aic_mujoco/
    ├── scripts/
    │   ├── automate_scene_generation.py
    │   ├── test_scene_generation.py
    │   ├── reproduce_scenes.py
    │   ├── add_cable_plugin.py (existing)
    │   └── QUICKSTART.md
    └── mjcf/
        ├── scene_manifest.json
        └── {scene_name}/
            ├── sdf/
            │   └── *.sdf
            └── mjcf/
                ├── *.xml
                ├── *.obj
                └── *.png
```

### Export Directory (Training)
```
/mnt/hgfs/exported mujoco training envs/
└── {scene_name}/
    ├── *.xml
    ├── *.obj
    └── *.png
```

## Error Handling

### Component-Level Errors

| Error | Component | Handling |
|-------|-----------|----------|
| SDF export timeout | GazeboExporter | Logs warning, returns RuntimeError |
| SDF fixes fail | SDFProcessor | Logs fix operations, continues |
| sdf2mjcf not found | MJCFConverter | Logs error, raises RuntimeError |
| MJCF files missing | MJCFOrganizer | Logs warning, skips missing files |
| add_cable_plugin not found | CablePluginProcessor | Logs warning, skips processing |
| Export dir doesn't exist | ExportOrganizer | Logs warning, skips export |

### Orchestration-Level Error Handling

- `process_single_scene()` catches exceptions and returns (success, message)
- Continues with next scene if one fails
- Generates summary report at end
- Returns non-zero exit code if any scene fails

## Uniqueness Guarantee

**Challenge:** Generate N unique scenes without duplicates.

**Solution:** 
- Generate random config
- Compute `scene_name` digest from key parameters
- Track used names in `self.used_configs`
- Retry up to 100 times if duplicate
- Raise error if max attempts exceeded

**Scene Name Composition:**
Critical parameters included: robot position, task board pose/yaw, cable config, mount translations

## ROS 2 Integration

**Environment Setup:**
- RMW Implementation: `rmw_zenoh_cpp` (efficient communication)
- Zenoh config: Shared memory enabled (536MB buffer)
- Launch system: ros2 launch with parameter substitution

**Launch Command Format:**
```bash
ros2 launch aic_bringup aic_gz_bringup.launch.py \
  robot_x:=VALUE \
  robot_y:=VALUE \
  ... (all parameters) ...
  spawn_task_board:=true \
  ground_truth:=true
```

## Parallelization Considerations

**Current Design:** Sequential processing of scenes
- Each scene waits for Gazebo export (120s default)
- Could be parallelized at scene level, but:
  - Each Gazebo instance needs unique resources
  - `/tmp/aic.sdf` would conflict between instances
  - Current timeout-based approach is simpler

**Future Optimization:**
- Run multiple Gazebo instances with different temp directories
- Use process pool for independent scenes
- Would require careful resource management

## Performance Characteristics

### Per-Scene Timing
- Gazebo export: 60-120 seconds (configurable)
- SDF fixes: <1 second
- MJCF conversion: 5-30 seconds
- Asset organization: 1-5 seconds  
- Cable plugin processing: 5-15 seconds
- **Total: 2-3 minutes per scene**

### Memory Usage
- Per Gazebo instance: ~500MB-1GB
- Per script process: ~50-100MB
- Temp files: ∼10-50MB per scene

### Disk Space
- Per scene: 50-200MB (depends on mesh complexity)
- Example: 100 scenes = 5-20GB total

## Testing Infrastructure

### test_scene_generation.py

Four levels of testing:

1. **Dependencies** - Check system packages and Python modules
2. **Gazebo Launch** - Verify Gazebo can export SDF
3. **SDF Conversion** - Test sdf2mjcf tool
4. **Cable Plugin** - Check script exists and is valid Python
5. **Full Suite** - Run all tests sequentially

### reproduce_scenes.py

Utility for scene analysis:
- Load manifest JSON
- List all scenes with configurations
- Extract specific scene parameters
- Help verify saved configurations

## Configuration Examples

### Minimal Scene
```python
SceneConfig(
    robot_x=-0.2, robot_y=0.2, robot_z=1.14, ...,
    task_board_x=0.2, task_board_y=-0.2, task_board_z=1.14, ...,
    spawn_cable=False,  # No cable
    sfp_mount_rail_0_present=False,  # No mounts
    # ... all other mounts False
)
```

### Complex Scene
```python
SceneConfig(
    robot_x=-0.15, robot_y=0.25, robot_z=1.14, ...,
    task_board_x=0.25, task_board_y=-0.15, task_board_z=1.14, ...,
    spawn_cable=True,
    cable_type='sfp_sc_cable',
    cable_x=0.17, cable_y=0.03, ...,
    attach_cable_to_gripper=True,
    sfp_mount_rail_0_present=True,
    sfp_mount_rail_0_translation=-0.05,
    sc_mount_rail_0_present=True,
    sc_mount_rail_0_translation=0.04,
    # ... more mount configurations
)
```

## Extension Points

### Custom Randomization

Edit `generate_random_config()` to customize parameter ranges:

```python
def generate_random_config(self):
    config = SceneConfig(
        robot_x=random.uniform(-0.5, 0.0),  # Custom range
        # ...
    )
```

### Custom Post-Processing

Add new processing steps in `process_single_scene()`:

```python
# After cable plugin processing
custom_post_processor.process(scene_mjcf_dir)
```

### Alternative Export Paths

Modify `ExportOrganizer.organize_scene()` to use different export location:

```python
scene_export_dir = custom_export_path / scene_name
```

## Dependencies

### System
- Python 3.7+
- ROS 2 (Kilted)
- Gazebo (with aic_bringup)
- sdf2mjcf tool

### Python Modules
- subprocess (stdlib)
- json (stdlib)
- pathlib (stdlib)
- logging (stdlib)
- tempfile (stdlib)
- shutil (stdlib)
- time (stdlib)
- random (stdlib)
- dataclasses (stdlib)

### Python Bindings
- sdformat16 (Python SDFormat bindings)
- gz.math9 (Gazebo Math Python bindings)

## Future Improvements

1. **Parallel Processing** - Process multiple scenes simultaneously
2. **Custom Randomization API** - Allow users to specify parameter distributions
3. **Scene Validation** - Verify SDF/MJCF validity before export
4. **Resume Capability** - Continue from partial generation if interrupted
5. **Progress Tracking** - Database to track generation progress
6. **Visualization** - Web dashboard for monitoring scene generation
7. **Parameter Presets** - Save/load common parameter configurations
8. **Scene Comparison** - Tools to compare generated scenes

---

For usage information, see [QUICKSTART.md](QUICKSTART.md) or [AUTOMATE_README.md](AUTOMATE_README.md).
