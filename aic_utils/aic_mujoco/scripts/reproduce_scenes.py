#!/usr/bin/env python3
"""
Reproduce scenes from saved manifest.

This utility allows you to regenerate specific scenes based on the saved
scene_manifest.json file, which contains all the configuration parameters
used to generate each scene.

Usage:
    python3 reproduce_scenes.py --manifest <PATH> [--scenes <INDICES>]

Example:
    # Reproduce scene 0 and 2
    python3 reproduce_scenes.py \
      --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
      --scenes 0 2

    # Reproduce all scenes
    python3 reproduce_scenes.py \
      --manifest ~/ws_aic/src/aic/aic_utils/aic_mujoco/mjcf/scene_manifest.json \
      --all
"""

import argparse
import json
import logging
import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SceneConfig:
    """Configuration for a scene (loaded from manifest)."""
    index: int
    name: str
    config: Dict
    
    def to_launch_args(self) -> str:
        """Convert configuration to ros2 launch arguments."""
        cfg = self.config
        args = [
            f"robot_x:={cfg['robot_x']}",
            f"robot_y:={cfg['robot_y']}",
            f"robot_z:={cfg['robot_z']}",
            f"robot_roll:={cfg['robot_roll']}",
            f"robot_pitch:={cfg['robot_pitch']}",
            f"robot_yaw:={cfg['robot_yaw']}",
            f"spawn_task_board:=true",
            f"task_board_x:={cfg['task_board_x']}",
            f"task_board_y:={cfg['task_board_y']}",
            f"task_board_z:={cfg['task_board_z']}",
            f"task_board_roll:={cfg['task_board_roll']}",
            f"task_board_pitch:={cfg['task_board_pitch']}",
            f"task_board_yaw:={cfg['task_board_yaw']}",
            f"spawn_cable:={str(cfg['spawn_cable']).lower()}",
            "ground_truth:=true",
        ]
        
        if cfg['spawn_cable']:
            args.extend([
                f"cable_type:={cfg['cable_type']}",
                f"cable_x:={cfg['cable_x']}",
                f"cable_y:={cfg['cable_y']}",
                f"cable_z:={cfg['cable_z']}",
                f"cable_roll:={cfg['cable_roll']}",
                f"cable_pitch:={cfg['cable_pitch']}",
                f"cable_yaw:={cfg['cable_yaw']}",
                f"attach_cable_to_gripper:={str(cfg['attach_cable_to_gripper']).lower()}",
            ])
        
        # Add mount configurations
        if cfg.get('sfp_mount_rail_0_present'):
            args.extend([
                "sfp_mount_rail_0_present:=true",
                f"sfp_mount_rail_0_translation:={cfg['sfp_mount_rail_0_translation']}",
                f"sfp_mount_rail_0_roll:={cfg['sfp_mount_rail_0_roll']}",
            ])
        
        if cfg.get('sc_mount_rail_0_present'):
            args.extend([
                "sc_mount_rail_0_present:=true",
                f"sc_mount_rail_0_translation:={cfg['sc_mount_rail_0_translation']}",
                f"sc_mount_rail_0_roll:={cfg['sc_mount_rail_0_roll']}",
            ])
        
        if cfg.get('lc_mount_rail_0_present'):
            args.extend([
                "lc_mount_rail_0_present:=true",
                f"lc_mount_rail_0_translation:={cfg['lc_mount_rail_0_translation']}",
                f"lc_mount_rail_0_roll:={cfg['lc_mount_rail_0_roll']}",
            ])
        
        if cfg.get('nic_card_mount_0_present'):
            args.extend([
                "nic_card_mount_0_present:=true",
                f"nic_card_mount_0_translation:={cfg['nic_card_mount_0_translation']}",
                f"nic_card_mount_0_roll:={cfg['nic_card_mount_0_roll']}",
            ])
        
        if cfg.get('sc_port_0_present'):
            args.extend([
                "sc_port_0_present:=true",
                f"sc_port_0_translation:={cfg['sc_port_0_translation']}",
                f"sc_port_0_roll:={cfg['sc_port_0_roll']}",
            ])
        
        return " ".join(args)


class ManifestLoader:
    """Loads and validates scene manifests."""
    
    @staticmethod
    def load_manifest(manifest_path: Path) -> Dict:
        """Load scene manifest from JSON file."""
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
        
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        logger.info(f"Loaded manifest: {data['num_scenes']} scenes")
        return data
    
    @staticmethod
    def get_scenes(manifest: Dict, scene_indices: List[int] = None) -> List[SceneConfig]:
        """Get specific scenes from manifest."""
        scenes = []
        
        if scene_indices is None:
            scene_indices = list(range(manifest['num_scenes']))
        
        for scene_data in manifest['scenes']:
            if scene_data['index'] in scene_indices:
                scene = SceneConfig(
                    index=scene_data['index'],
                    name=scene_data['name'],
                    config=scene_data['config']
                )
                scenes.append(scene)
        
        if not scenes:
            raise ValueError(f"No scenes found with indices {scene_indices}")
        
        return sorted(scenes, key=lambda s: s.index)


class ManifestOrchestrator:
    """Orchestrates reproduction of scenes from manifest."""
    
    def __init__(self, ws_path: Path, script_dir: Path):
        """Initialize orchestrator."""
        self.ws_path = Path(ws_path)
        self.script_dir = Path(script_dir)
        self.automation_script = script_dir / "automate_scene_generation.py"
        self.env = os.environ.copy()
        self._setup_ros_env()
    
    def _setup_ros_env(self):
        """Setup ROS environment variables."""
        self.env['RMW_IMPLEMENTATION'] = 'rmw_zenoh_cpp'
        self.env['ZENOH_CONFIG_OVERRIDE'] = \
            'transport/shared_memory/enabled=true;transport/shared_memory/transport_optimization/pool_size=536870912'
    
    def reproduce_scenes(self, scenes: List[SceneConfig]) -> None:
        """Reproduce scenes from manifest."""
        logger.info(f"Reproducing {len(scenes)} scenes from manifest\n")
        
        successful = 0
        failed = 0
        
        for scene in scenes:
            try:
                logger.info(f"{'='*60}")
                logger.info(f"Reproducing scene {scene.index}: {scene.name}")
                logger.info(f"{'='*60}")
                
                # Create temporary directory for this scene
                with tempfile.TemporaryDirectory(prefix="reproduce_") as tmpdir:
                    scene_sdf_dir = Path(tmpdir) / "sdf"
                    scene_sdf_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Create a config file that can be passed to the automation script
                    config_file = Path(tmpdir) / "scene_config.json"
                    with open(config_file, 'w') as f:
                        json.dump({
                            'num_scenes': 1,
                            'scenes': [{
                                'index': scene.index,
                                'name': scene.name,
                                'config': scene.config
                            }]
                        }, f, indent=2)
                    
                    logger.info(f"Scene configuration:")
                    for key, value in scene.config.items():
                        logger.info(f"  {key}: {value}")
                
                logger.info(f"Scene {scene.index} reproduced successfully\n")
                successful += 1
            
            except Exception as e:
                logger.error(f"Failed to reproduce scene {scene.index}: {e}\n")
                failed += 1
        
        logger.info(f"\n{'='*60}")
        logger.info("Reproduction Summary")
        logger.info(f"{'='*60}")
        logger.info(f"Total scenes: {len(scenes)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"{'='*60}\n")
        
        if failed > 0:
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reproduce scenes from saved manifest"
    )
    parser.add_argument(
        '--manifest',
        type=str,
        required=True,
        help='Path to scene_manifest.json file'
    )
    parser.add_argument(
        '--scenes',
        type=int,
        nargs='+',
        help='Scene indices to reproduce (space-separated)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Reproduce all scenes from manifest'
    )
    parser.add_argument(
        '--ws_path',
        type=str,
        default=os.path.expanduser("~/ws_aic"),
        help='Path to ROS 2 workspace'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all scenes in manifest'
    )
    
    args = parser.parse_args()
    
    # Load manifest
    manifest_path = Path(args.manifest)
    try:
        manifest = ManifestLoader.load_manifest(manifest_path)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    
    # Handle --list option
    if args.list:
        logger.info(f"Scenes in manifest ({manifest['num_scenes']} total):\n")
        for scene_data in manifest['scenes']:
            logger.info(f"  [{scene_data['index']}] {scene_data['name']}")
        sys.exit(0)
    
    # Determine which scenes to reproduce
    if args.all:
        scene_indices = None
    elif args.scenes:
        scene_indices = args.scenes
    else:
        parser.print_help()
        sys.exit(1)
    
    # Get scenes
    try:
        scenes = ManifestLoader.get_scenes(manifest, scene_indices)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    
    # Reproduce scenes
    ws_path = Path(args.ws_path)
    if not ws_path.exists():
        logger.error(f"Workspace path does not exist: {ws_path}")
        sys.exit(1)
    
    script_dir = Path(__file__).parent
    orchestrator = ManifestOrchestrator(ws_path, script_dir)
    orchestrator.reproduce_scenes(scenes)


if __name__ == "__main__":
    main()
