# Automated Scene Generation System - Documentation Index

## Overview

This directory contains a complete automation system for generating unique Gazebo scenes and exporting them to MuJoCo MJCF format. All components work together to streamline the scene generation workflow.

**Location:** `~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts/`

## Quick Navigation

### ⚡ I want to... 

- **Get started in 5 minutes** → Read [QUICKSTART.md](#1-quickstartmd)
- **Understand what was delivered** → Read [DELIVERY_SUMMARY.md](#7-delivery_summarymd)
- **Generate scenes now** → Run `automate_scene_generation.py --help`
- **Test my setup first** → Run `test_scene_generation.py --test dependencies`
- **Customize parameters** → Edit [automate_scene_generation.py](#2-automate_scene_generationpy) or read [ARCHITECTURE.md](#4-architecturemd)
- **Troubleshoot issues** → See [AUTOMATE_README.md](#3-automate_readmemd) Troubleshooting section
- **Understand the system** → Read [ARCHITECTURE.md](#4-architecturemd)
- **Find where my files are** → See [QUICKSTART.md](#1-quickstartmd) "Where Are My Files?" section
- **Analyze generated scenes** → Use `reproduce_scenes.py --manifest <path> --list`

---

## Documentation Files

### 1. QUICKSTART.md
**Status:** ✅ START HERE  
**File Size:** ~7.2 KB  
**Target Audience:** Everyone (especially first-time users)  
**Reading Time:** ~10 minutes

**Contents:**
- Prerequisites checklist
- 3-step quick start
- Where files are located
- How to view scenes in MuJoCo
- Common tasks and usage patterns
- Performance expectations

**When to Read:**
- First time setting up the system
- Want quick reference on common tasks
- Need troubleshooting for common issues

**Key Sections:**
```
- Prerequisites
- Quick Start Steps
- Where Are My Files?
- View Generated Scenes
- Common Tasks
- Troubleshooting
- Performance Notes
- Next Steps
```

**Example Workflow:**
1. Follow "Test Your Setup" section
2. Follow "Generate Scenes" section
3. Check "Where Are My Files?" for outputs
4. Use "View Generated Scenes" to see results

---

### 2. automate_scene_generation.py
**Status:** ✅ READY TO USE  
**File Size:** ~26 KB  
**Type:** Python 3 Executable Script  
**Target Audience:** Developers, data generation engineers  
**Execution Time:** 2-3 minutes per scene

**Purpose:**
Main automation script that orchestrates the entire workflow.

**Key Classes:**
- `SceneGenerator` - Generates unique random configurations
- `GazeboExporter` - Launches Gazebo and exports SDF
- `SDFProcessor` - Fixes and renames SDF files
- `MJCFConverter` - Converts SDF to MJCF format
- `MJCFOrganizer` - Manages mesh assets
- `CablePluginProcessor` - Applies cable plugin post-processing
- `ExportOrganizer` - Organizes final outputs
- `OrchestrationManager` - Coordinates entire workflow

**Usage:**
```bash
# Generate 5 scenes
python3 automate_scene_generation.py --num_scenes 5

# Generate with custom timeout
python3 automate_scene_generation.py --num_scenes 10 --export_timeout 180

# Get help
python3 automate_scene_generation.py --help
```

**Parameters:**
- `--num_scenes` (required): Number of scenes to generate (int)
- `--ws_path` (optional): ROS 2 workspace path (default: ~/ws_aic)
- `--export_timeout` (optional): Gazebo timeout in seconds (default: 120)

**Output:**
- Organized MJCF scenes with assets
- Scene manifest JSON
- Exported copies to `/mnt/hgfs/exported mujoco training envs/`
- Detailed logging to console

**Customization:**
Edit `generate_random_config()` method to customize parameter ranges:
```python
def generate_random_config(self) -> SceneConfig:
    config = SceneConfig(
        robot_x=random.uniform(-0.5, 0.0),  # Custom range
        # ... edit more ranges ...
    )
```

---

### 3. AUTOMATE_README.md
**Status:** ✅ REFERENCE  
**File Size:** ~6.9 KB  
**Target Audience:** Users needing detailed reference  
**Reading Time:** ~15 minutes

**Contents:**
- Detailed overview of complete workflow
- All command-line parameters explained
- Output directory structure
- Scene naming convention
- Randomization ranges and constraints
- Manifest file details
- Troubleshooting guide with solutions
- Performance notes
- Information on viewing scenes
- Customization guide

**When to Read:**
- Need detailed reference on parameters
- Want to understand randomization ranges
- Debugging specific issues
- Want to customize behavior

**Key Sections:**
```
- Overview
- Usage
- Output Directory Structure
- Scene Naming Convention
- Randomization Ranges
- Manifest File
- Troubleshooting
- Viewing Generated Scenes
- Modifying Randomization
```

---

### 4. ARCHITECTURE.md
**Status:** ✅ TECHNICAL REFERENCE  
**File Size:** ~15 KB  
**Target Audience:** Developers, system architects  
**Reading Time:** ~20 minutes

**Contents:**
- Component architecture with diagrams
- Detailed component descriptions
- Data flow and interactions
- Data structures (SceneConfig, etc.)
- File organization semantics
- Error handling strategy
- Performance characteristics
- Testing infrastructure details
- Extension points for customization
- Future improvements
- ROS 2 integration details

**When to Read:**
- Want to understand internal architecture
- Planning extensions or modifications
- Debugging complex issues
- Contributing to the system
- Performance optimization

**Key Sections:**
```
- Overview
- Component Architecture
- Component Descriptions (9 detailed sections)
- Data Structures
- File Organization
- Error Handling
- Performance Characteristics
- Testing Infrastructure
- Extension Points
- Future Improvements
```

**Useful for Understanding:**
- How each component works
- Data flow through the system
- Why decisions were made
- Where to add custom processing
- Performance bottlenecks

---

### 5. test_scene_generation.py
**Status:** ✅ TESTING UTILITY  
**File Size:** ~12 KB  
**Type:** Python 3 Executable Script  
**Target Audience:** Everyone (especially troubleshooting)  
**Execution Time:** Varies (2-15 minutes depending on tests)

**Purpose:**
Diagnostic tool to test individual components and verify setup.

**Key Methods:**
- `test_dependencies()` - Verify packages installed
- `test_gazebo_launch()` - Test Gazebo export
- `test_sdf_conversion()` - Test sdf2mjcf tool
- `test_cable_plugin()` - Verify cable plugin
- `test_single_scene()` - Full single-scene workflow

**Available Tests:**
- `dependencies` - Check all required packages (fast, ~5 seconds)
- `gazebo` - Test Gazebo launch (medium, ~60 seconds)
- `conversion` - Test SDF→MJCF conversion (medium, ~30 seconds)
- `plugin` - Test cable plugin script (fast, ~5 seconds)
- `full` - Run all tests sequentially (slow, ~15 minutes)
- `all` - Same as full

**Usage:**
```bash
# Check dependencies first
python3 test_scene_generation.py --test dependencies

# Full diagnostic (recommended for first-time)
python3 test_scene_generation.py --test full

# Individual component tests
python3 test_scene_generation.py --test gazebo
python3 test_scene_generation.py --test conversion
```

**Output:**
✓ or ✗ status for each component, with error details.

**When to Run:**
- First-time setup verification
- After dependency installation
- Before generating many scenes
- When troubleshooting issues

---

### 6. reproduce_scenes.py
**Status:** ✅ UTILITY SCRIPT  
**File Size:** ~11 KB  
**Type:** Python 3 Executable Script  
**Target Audience:** Analysts, researchers  
**Execution Time:** <1 second

**Purpose:**
Load and analyze scene manifest for extracting scene configurations.

**Key Methods:**
- `load_manifest()` - Load scene_manifest.json
- `get_scenes()` - Extract specific scenes
- `reproduce_scenes()` - Prepare for re-export

**Usage:**
```bash
# List all scenes
python3 reproduce_scenes.py \
  --manifest scene_manifest.json \
  --list

# Get specific scenes
python3 reproduce_scenes.py \
  --manifest scene_manifest.json \
  --scenes 0 2 5

# Get all scenes
python3 reproduce_scenes.py \
  --manifest scene_manifest.json \
  --all
```

**Output:**
Scene index and configuration details.

**When to Use:**
- Analyze generated scene diversity
- Extract parameters from saved scenes
- Plan scene re-export
- Verify configuration uniqueness

---

### 7. DELIVERY_SUMMARY.md
**Status:** ✅ OVERVIEW (This File)  
**File Size:** ~13 KB  
**Target Audience:** Everyone  
**Reading Time:** ~15 minutes

**Contents:**
- Summary of what was delivered
- Quick reference commands
- File structure overview
- Key features
- Workflow stages
- Performance expectations
- Customization options
- Troubleshooting table
- Next steps
- Documentation cross-reference

**When to Read:**
- Understanding complete delivery
- Getting overview of capabilities
- Quick reference for common tasks
- Navigating to specific docs

---

## File Organization

### Core Automation Files
```
scripts/
├── automate_scene_generation.py   (26 KB, 550 lines) - MAIN SCRIPT
├── test_scene_generation.py       (12 KB, 350 lines) - Testing utility
└── reproduce_scenes.py            (11 KB, 300 lines) - Scene analysis
```

### Documentation Files
```
scripts/
├── QUICKSTART.md                  (7.2 KB) ← START HERE
├── AUTOMATE_README.md             (6.9 KB) - Detailed reference
├── ARCHITECTURE.md                (15 KB)  - Technical deep dive
└── DELIVERY_SUMMARY.md            (13 KB)  - This file
```

### Additional Scripts (Pre-existing)
```
scripts/
├── add_cable_plugin.py            (29 KB) - Post-processor
├── load_aic_world.py              (4.5 KB) - MuJoCo loader
└── view_scene.py                  (3.2 KB) - Scene viewer
```

---

## Learning Path

### Path 1: Fast Track (15 minutes)
1. Read: [QUICKSTART.md](#1-quickstartmd) - Quick Start Steps
2. Run: `test_scene_generation.py --test dependencies`
3. Run: `automate_scene_generation.py --num_scenes 2`
4. Run: View scenes using instructions from QUICKSTART
5. Done! Generate more as needed.

### Path 2: Thorough Understanding (45 minutes)
1. Read: [DELIVERY_SUMMARY.md](#7-delivery_summarymd) - Overview
2. Read: [QUICKSTART.md](#1-quickstartmd) - Quick start
3. Read: [AUTOMATE_README.md](#3-automate_readmemd) - Complete reference
4. Run: Test suite `test_scene_generation.py --test full`
5. Run: Generate some scenes `automate_scene_generation.py --num_scenes 5`
6. Read: [ARCHITECTURE.md](#4-architecturemd) - Internals (optional)

### Path 3: Developer/Customizer (90 minutes)
1. Read: [ARCHITECTURE.md](#4-architecturemd) - Complete architecture
2. Read: [automate_scene_generation.py](#2-automate_scene_generationpy) - Source code
3. Study: Component classes and methods
4. Plan: Customizations needed
5. Edit: `generate_random_config()` method
6. Test: `test_scene_generation.py --test full`
7. Run: Modified script

---

## Common Workflows

### Workflow 1: Generate Default Scenes
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 automate_scene_generation.py --num_scenes 10
# Files appear in:
# - ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/
# - /mnt/hgfs/exported mujoco training envs/
```

### Workflow 2: Test Setup
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 test_scene_generation.py --test full
# If all pass ✓, ready to generate scenes
```

### Workflow 3: Analyze Generated Scenes
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 reproduce_scenes.py \
  --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
  --list
# Prints all scene configurations
```

### Workflow 4: Customize Parameters
```
1. Edit automate_scene_generation.py generate_random_config()
2. Modify ranges as needed
3. Run: python3 test_scene_generation.py --test dependencies
4. Run: python3 automate_scene_generation.py --num_scenes 5
```

### Workflow 5: Scale Up Generation
```bash
# Run in background
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
nohup python3 automate_scene_generation.py --num_scenes 100 > gen.log 2>&1 &

# Monitor progress in another terminal
tail -f gen.log

# Check completion
grep -i "completed\|failed" gen.log
```

---

## Technical Stack

**Languages & Tools:**
- Python 3.7+
- ROS 2 (Kilted)
- Gazebo (with aic_bringup)
- MuJoCo (sdf2mjcf converter)
- Zenoh (ROS 2 middleware)

**Python Modules Used:**
- subprocess, json, pathlib, logging, tempfile, shutil, time, random, dataclasses

**External Dependencies:**
- sdformat16 (Python bindings)
- gz.math9 (Gazebo Math Python bindings)

---

## Performance Summary

| Aspect | Value |
|--------|-------|
| Time per scene | 2-3 minutes |
| Total for 5 scenes | ~15 minutes |
| Total for 10 scenes | ~30 minutes |
| Total for 100 scenes | ~3-5 hours |
| Disk space per scene | 50-200 MB |
| Total for 100 scenes | ~5-20 GB |

---

## Support & Resources

**Documentation:**
- [QUICKSTART.md](#1-quickstartmd) - Fast start
- [AUTOMATE_README.md](#3-automate_readmemd) - Detailed reference
- [ARCHITECTURE.md](#4-architecturemd) - Technical details

**Related Documentation:**
- Parent README: `../README.md`
- Scene Description: `../../docs/scene_description.md`
- Task Board: `../../docs/task_board_description.md`
- Launch parameters: `../../aic_bringup/README.md`

**Scripts:**
- Main: `automate_scene_generation.py`
- Testing: `test_scene_generation.py`
- Analysis: `reproduce_scenes.py`

---

## Summary

✅ **You have:**
- Fully automated scene generation system
- Comprehensive documentation
- Testing and validation tools
- Scene analysis utilities
- Ready to generate thousands of unique training scenarios

✅ **Quick start:**
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_mujoco/scripts
python3 automate_scene_generation.py --num_scenes 5
```

✅ **Learn more:**
See [QUICKSTART.md](#1-quickstartmd) for detailed walkthrough.

---

**Created:** March 30, 2026  
**Version:** 1.0  
**Status:** Production Ready
