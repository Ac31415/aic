#!/usr/bin/env python3
"""
Automated scene generation and export from Gazebo to MuJoCo.

This script automates the complete workflow:
1. Generate random scene configurations with unique parameters
2. Launch Gazebo with parameters and export SDF
3. Fix SDF URIs
4. Convert SDF to MJCF
5. Organize mesh assets
6. Run add_cable_plugin processing
7. Copy final outputs to export directory

Usage:
    python3 automate_scene_generation.py --num_scenes <N> [--output_dir <DIR>]

Example:
    python3 automate_scene_generation.py --num_scenes 5
"""

import argparse
import json
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_bool_arg(value: str) -> bool:
    """Parse common string boolean values for argparse options."""
    normalized = value.strip().lower()
    if normalized in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(
        f"Invalid boolean value: {value}. Use true/false."
    )


@dataclass
class SceneConfig:
    """Configuration for a single scene."""
    # robot_x: float
    # robot_y: float
    robot_z: float
    robot_roll: float
    robot_pitch: float
    robot_yaw: float
    
    task_board_x: float
    task_board_y: float
    task_board_z: float
    task_board_roll: float
    task_board_pitch: float
    task_board_yaw: float
    
    spawn_cable: bool
    cable_type: str
    cable_x: float
    cable_y: float
    cable_z: float
    cable_roll: float
    cable_pitch: float
    cable_yaw: float
    attach_cable_to_gripper: bool
    
    # Mount configurations
    sfp_mount_rail_0_present: bool
    sfp_mount_rail_0_translation: float
    sfp_mount_rail_0_roll: float
    sfp_mount_rail_0_pitch: float
    sfp_mount_rail_0_yaw: float
    
    sc_mount_rail_0_present: bool
    sc_mount_rail_0_translation: float
    sc_mount_rail_0_roll: float
    sc_mount_rail_0_pitch: float
    sc_mount_rail_0_yaw: float
    
    lc_mount_rail_0_present: bool
    lc_mount_rail_0_translation: float
    lc_mount_rail_0_roll: float
    lc_mount_rail_0_pitch: float
    lc_mount_rail_0_yaw: float
    
    nic_card_mount_0_present: bool
    nic_card_mount_0_translation: float
    nic_card_mount_0_roll: float
    nic_card_mount_0_pitch: float
    nic_card_mount_0_yaw: float
    
    sc_port_0_present: bool
    sc_port_0_translation: float
    sc_port_0_roll: float
    sc_port_0_pitch: float
    sc_port_0_yaw: float
    
    @property
    def scene_name(self) -> str:
        """Generate a unique scene name from configuration."""
        params = []
        # Key parameters that define the scene
        # params.append(f"robot_x={self.robot_x:.3f}")
        # params.append(f"robot_y={self.robot_y:.3f}")
        params.append(f"robot_z={self.robot_z:.3f}")
        params.append(f"tb_x={self.task_board_x:.3f}")
        params.append(f"tb_y={self.task_board_y:.3f}")
        params.append(f"tb_yaw={self.task_board_yaw:.3f}")
        
        if self.spawn_cable:
            params.append(f"cable={self.cable_type}")
            params.append(f"cable_x={self.cable_x:.3f}")
            params.append(f"cable_y={self.cable_y:.3f}")
            params.append(f"cable_z={self.cable_z:.3f}")
        
        if self.sfp_mount_rail_0_present:
            params.append(f"sfp_trans={self.sfp_mount_rail_0_translation:.3f}")
            params.append(f"sfp_rpy={self.sfp_mount_rail_0_roll:.2f},{self.sfp_mount_rail_0_pitch:.2f},{self.sfp_mount_rail_0_yaw:.2f}")
        
        if self.sc_mount_rail_0_present:
            params.append(f"sc_trans={self.sc_mount_rail_0_translation:.3f}")
            params.append(f"sc_rpy={self.sc_mount_rail_0_roll:.2f},{self.sc_mount_rail_0_pitch:.2f},{self.sc_mount_rail_0_yaw:.2f}")
        
        if self.lc_mount_rail_0_present:
            params.append(f"lc_trans={self.lc_mount_rail_0_translation:.3f}")
            params.append(f"lc_rpy={self.lc_mount_rail_0_roll:.2f},{self.lc_mount_rail_0_pitch:.2f},{self.lc_mount_rail_0_yaw:.2f}")

        if self.nic_card_mount_0_present:
            params.append(f"nic_rpy={self.nic_card_mount_0_roll:.2f},{self.nic_card_mount_0_pitch:.2f},{self.nic_card_mount_0_yaw:.2f}")

        if self.sc_port_0_present:
            params.append(f"sc_port_rpy={self.sc_port_0_roll:.2f},{self.sc_port_0_pitch:.2f},{self.sc_port_0_yaw:.2f}")
        
        name = "_".join(params).replace(".", "p")
        return name
    
    def to_launch_args(self, gazebo_gui: bool = True, launch_rviz: bool = False) -> str:
        """Convert configuration to ros2 launch arguments."""
        args = [
            # f"robot_x:={self.robot_x}",
            # f"robot_y:={self.robot_y}",
            f"robot_z:={self.robot_z}",
            f"robot_roll:={self.robot_roll}",
            f"robot_pitch:={self.robot_pitch}",
            f"robot_yaw:={self.robot_yaw}",
            f"spawn_task_board:=true",
            f"task_board_x:={self.task_board_x}",
            f"task_board_y:={self.task_board_y}",
            f"task_board_z:={self.task_board_z}",
            f"task_board_roll:={self.task_board_roll}",
            f"task_board_pitch:={self.task_board_pitch}",
            f"task_board_yaw:={self.task_board_yaw}",
            f"spawn_cable:={str(self.spawn_cable).lower()}",
            f"gazebo_gui:={str(gazebo_gui).lower()}",
            f"launch_rviz:={str(launch_rviz).lower()}",
            "ground_truth:=true",
        ]
        
        if self.spawn_cable:
            args.extend([
                f"cable_type:={self.cable_type}",
                f"cable_x:={self.cable_x}",
                f"cable_y:={self.cable_y}",
                f"cable_z:={self.cable_z}",
                f"cable_roll:={self.cable_roll}",
                f"cable_pitch:={self.cable_pitch}",
                f"cable_yaw:={self.cable_yaw}",
                f"attach_cable_to_gripper:={str(self.attach_cable_to_gripper).lower()}",
            ])
        
        # Add mount configurations
        if self.sfp_mount_rail_0_present:
            args.extend([
                "sfp_mount_rail_0_present:=true",
                f"sfp_mount_rail_0_translation:={self.sfp_mount_rail_0_translation}",
                f"sfp_mount_rail_0_roll:={self.sfp_mount_rail_0_roll}",
                f"sfp_mount_rail_0_pitch:={self.sfp_mount_rail_0_pitch}",
                f"sfp_mount_rail_0_yaw:={self.sfp_mount_rail_0_yaw}",
            ])
        
        if self.sc_mount_rail_0_present:
            args.extend([
                "sc_mount_rail_0_present:=true",
                f"sc_mount_rail_0_translation:={self.sc_mount_rail_0_translation}",
                f"sc_mount_rail_0_roll:={self.sc_mount_rail_0_roll}",
                f"sc_mount_rail_0_pitch:={self.sc_mount_rail_0_pitch}",
                f"sc_mount_rail_0_yaw:={self.sc_mount_rail_0_yaw}",
            ])
        
        if self.lc_mount_rail_0_present:
            args.extend([
                "lc_mount_rail_0_present:=true",
                f"lc_mount_rail_0_translation:={self.lc_mount_rail_0_translation}",
                f"lc_mount_rail_0_roll:={self.lc_mount_rail_0_roll}",
                f"lc_mount_rail_0_pitch:={self.lc_mount_rail_0_pitch}",
                f"lc_mount_rail_0_yaw:={self.lc_mount_rail_0_yaw}",
            ])
        
        if self.nic_card_mount_0_present:
            args.extend([
                "nic_card_mount_0_present:=true",
                f"nic_card_mount_0_translation:={self.nic_card_mount_0_translation}",
                f"nic_card_mount_0_roll:={self.nic_card_mount_0_roll}",
                f"nic_card_mount_0_pitch:={self.nic_card_mount_0_pitch}",
                f"nic_card_mount_0_yaw:={self.nic_card_mount_0_yaw}",
            ])
        
        if self.sc_port_0_present:
            args.extend([
                "sc_port_0_present:=true",
                f"sc_port_0_translation:={self.sc_port_0_translation}",
                f"sc_port_0_roll:={self.sc_port_0_roll}",
                f"sc_port_0_pitch:={self.sc_port_0_pitch}",
                f"sc_port_0_yaw:={self.sc_port_0_yaw}",
            ])
        
        return " ".join(args)


class SceneGenerator:
    """Generates unique random scene configurations."""
    
    def __init__(self):
        """Initialize scene generator with default ranges."""
        self.used_configs: List[str] = []
    
    def generate_random_config(self) -> SceneConfig:
        """Generate a unique random scene configuration."""
        max_attempts = 100
        
        for attempt in range(max_attempts):
            config = SceneConfig(
                # Robot position (fixed for baseline)
                # robot_x=random.uniform(-0.3, -0.1),
                # robot_y=random.uniform(0.1, 0.3),
                robot_z=1.14,  # Fixed
                robot_roll=0.0,
                robot_pitch=0.0,
                robot_yaw=-3.141,
                
                # Task board position with some randomization
                task_board_x=random.uniform(0.1, 0.3),
                task_board_y=random.uniform(-0.3, -0.1),
                task_board_z=1.14,  # Fixed
                task_board_roll=0.0,
                task_board_pitch=0.0,
                task_board_yaw=random.uniform(-0.5, 0.5),

                # Cable configuration
                # spawn_cable=random.choice([True, False]) if random.random() > 0.3 else True,
                spawn_cable=True,
                cable_type=random.choice(["sfp_sc_cable", "sfp_sc_cable_reversed"]),
                cable_x=0.172,
                cable_y=0.024,
                cable_z=1.508 if random.random() > 0.5 else 1.518,
                # cable_z=1.508 if cable_type == "sfp_sc_cable" else 1.518,
                cable_roll=0.4432,
                cable_pitch=-0.48,
                cable_yaw=1.3303,
                # attach_cable_to_gripper=random.choice([True, False]),
                attach_cable_to_gripper=True,
                
                # # Cable configuration
                # # spawn_cable=random.choice([True, False]) if random.random() > 0.3 else True,
                # spawn_cable=True,
                # cable_type=random.choice(["sfp_sc_cable", "sfp_sc_cable_reversed"]),
                # cable_x=random.uniform(0.15, 0.19),
                # cable_y=random.uniform(0.0, 0.05),
                # cable_z=1.508 if random.random() > 0.5 else 1.518,
                # # cable_z=1.508 if cable_type == "sfp_sc_cable" else 1.518,
                # cable_roll=random.uniform(0.3, 0.6),
                # cable_pitch=random.uniform(-0.6, -0.3),
                # cable_yaw=random.uniform(1.0, 1.66),
                # # attach_cable_to_gripper=random.choice([True, False]),
                # attach_cable_to_gripper=True,
                
                # Mount rails (presence and positioning)
                sfp_mount_rail_0_present=random.choice([True, False]),
                sfp_mount_rail_0_translation=random.uniform(-0.09625, 0.09625),
                sfp_mount_rail_0_roll=random.uniform(-0.175, 0.175),  # ~+/-10 degrees
                sfp_mount_rail_0_pitch=random.uniform(-0.175, 0.175),
                sfp_mount_rail_0_yaw=random.uniform(-0.175, 0.175),
                
                sc_mount_rail_0_present=random.choice([True, False]),
                sc_mount_rail_0_translation=random.uniform(-0.09625, 0.09625),
                sc_mount_rail_0_roll=random.uniform(-0.175, 0.175),
                sc_mount_rail_0_pitch=random.uniform(-0.175, 0.175),
                sc_mount_rail_0_yaw=random.uniform(-0.175, 0.175),
                
                lc_mount_rail_0_present=random.choice([True, False]),
                lc_mount_rail_0_translation=random.uniform(-0.188, 0.188),
                lc_mount_rail_0_roll=random.uniform(-1.047, 1.047),  # ~+/-60 degrees
                lc_mount_rail_0_pitch=random.uniform(-1.047, 1.047),
                lc_mount_rail_0_yaw=random.uniform(-1.047, 1.047),
                
                nic_card_mount_0_present=random.choice([True, False]),
                nic_card_mount_0_translation=random.uniform(0.0, 0.062),
                nic_card_mount_0_roll=random.uniform(-0.175, 0.175),
                nic_card_mount_0_pitch=random.uniform(-0.175, 0.175),
                nic_card_mount_0_yaw=random.uniform(-0.175, 0.175),
                
                sc_port_0_present=random.choice([True, False]),
                sc_port_0_translation=random.uniform(0.0, 0.115),
                sc_port_0_roll=random.uniform(-0.175, 0.175),
                sc_port_0_pitch=random.uniform(-0.175, 0.175),
                sc_port_0_yaw=random.uniform(-0.175, 0.175),
            )

            # Note: set cable_z to 1.508 if cable_type is sfp_sc_cable_reversed, according to the readme.
            if config.cable_type == "sfp_sc_cable_reversed":
                config.cable_z = 1.508
            else:
                config.cable_z = 1.518
            
            # Check uniqueness
            config_hash = config.scene_name
            if config_hash not in self.used_configs:
                self.used_configs.append(config_hash)
                return config
        
        raise RuntimeError(f"Could not generate unique config after {max_attempts} attempts")


class GazeboExporter:
    """Handles Gazebo simulation and SDF export."""
    
    def __init__(self, ws_path: Path, gazebo_gui: bool = True, launch_rviz: bool = False):
        """Initialize exporter."""
        self.ws_path = ws_path
        self.gazebo_gui = gazebo_gui
        self.launch_rviz = launch_rviz
        self.env = os.environ.copy()
        self._setup_ros_env()
    
    def _setup_ros_env(self):
        """Setup ROS 2 environment variables."""
        self.env['RMW_IMPLEMENTATION'] = 'rmw_zenoh_cpp'
        self.env['ZENOH_CONFIG_OVERRIDE'] = \
            'transport/shared_memory/enabled=true;transport/shared_memory/transport_optimization/pool_size=536870912'

    def _terminate_process_group(self, process: subprocess.Popen, timeout: int = 30) -> None:
        """Terminate ros2 launch and all spawned children (Gazebo, RViz, etc.)."""
        if process is None or process.poll() is not None:
            return

        try:
            # start_new_session=True makes PID the process-group id.
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=timeout)
            logger.info("✓ Gazebo/RViz process group terminated gracefully")
            return
        except subprocess.TimeoutExpired:
            logger.warning("Launch process group did not exit after SIGTERM, forcing SIGKILL...")
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
            logger.info("✓ Gazebo/RViz process group killed")
        except ProcessLookupError:
            # Process group already exited.
            pass
    
    def export_scene(self, config: SceneConfig, timeout: int = 120) -> Path:
        """
        Launch Gazebo with given configuration and export SDF.
        
        Polls for SDF file creation and shuts down Gazebo immediately after export,
        rather than waiting for the full timeout period.
        
        Returns:
            Path to exported SDF file
        """
        logger.info(f"Exporting scene: {config.scene_name}")
        
        # Build launch command
        cmd = [
            "bash", "-c",
            f"source {self.ws_path}/install/setup.bash && "
            f"ros2 launch aic_bringup aic_gz_bringup.launch.py "
            f"{config.to_launch_args(gazebo_gui=self.gazebo_gui, launch_rviz=self.launch_rviz)}"
        ]
        
        logger.info(f"Launching Gazebo with parameters: {config.scene_name}")
        
        def _sdf_seems_complete(path: Path) -> bool:
            """Heuristic completeness check to avoid consuming partial exports."""
            try:
                content = path.read_text()
            except (OSError, UnicodeDecodeError):
                return False

            if "</sdf>" not in content:
                return False

            # A valid AIC export should include robot/tabletop content.
            return ("tabletop" in content) or ("shoulder_link" in content)

        process = None
        try:
            sdf_path = Path("/tmp/aic.sdf")
            if sdf_path.exists():
                logger.info(f"Removing stale SDF before launch: {sdf_path}")
                sdf_path.unlink()

            launch_start_time = time.time()

            # Launch Gazebo process
            process = subprocess.Popen(
                cmd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            logger.info(f"Gazebo process started (PID: {process.pid})")
            
            # Poll for SDF file with intelligent detection
            poll_interval = 1.0  # Check every 1 second
            elapsed_time = 0.0
            last_file_size = 0
            stable_size_count = 0
            
            logger.info(f"Polling for SDF export (timeout: {timeout}s, poll interval: {poll_interval}s)...")
            
            while elapsed_time < timeout:
                if process.poll() is not None and not sdf_path.exists():
                    raise RuntimeError(
                        "Gazebo launch exited before producing /tmp/aic.sdf"
                    )

                if sdf_path.exists():
                    stat = sdf_path.stat()

                    # Ignore stale files that predate this launch.
                    if stat.st_mtime < launch_start_time:
                        time.sleep(poll_interval)
                        elapsed_time += poll_interval
                        continue

                    # File exists, check if it's stable (size not changing)
                    current_size = stat.st_size
                    
                    if current_size > 0:  # Ensure file is not empty
                        if current_size == last_file_size:
                            # File size unchanged, means export likely complete
                            stable_size_count += 1
                            if stable_size_count >= 2:  # Size stable for 2 consecutive checks
                                if _sdf_seems_complete(sdf_path):
                                    logger.info(f"✓ SDF file detected at {sdf_path} ({current_size} bytes)")
                                    logger.info(f"✓ File size stable - export completed after {elapsed_time:.1f}s")
                                    logger.info("Shutting down Gazebo...")
                                    break
                                logger.info(
                                    "SDF file is stable but appears incomplete; waiting for full export..."
                                )
                                stable_size_count = 0
                        else:
                            # File size changed, it's still being written
                            logger.debug(f"SDF file size: {last_file_size} → {current_size} bytes (still writing)")
                            stable_size_count = 0
                        
                        last_file_size = current_size
                
                # Wait before next poll
                time.sleep(poll_interval)
                elapsed_time += poll_interval
            
            # Verify SDF was created before terminating
            if not sdf_path.exists():
                logger.warning(f"SDF file not found after {elapsed_time:.1f}s - continuing with graceful shutdown")
            elif sdf_path.stat().st_size == 0:
                logger.warning(f"SDF file exists but is empty - may indicate incomplete export")
            
            # Gracefully terminate launch tree (ros2 launch + Gazebo + RViz)
            logger.info("Terminating Gazebo/RViz launch process group...")
            self._terminate_process_group(process, timeout=30)
            
            # Verify SDF was created
            if not sdf_path.exists():
                raise RuntimeError(f"SDF export failed - file not found at {sdf_path} after {timeout}s")
            
            file_size = sdf_path.stat().st_size
            if file_size == 0:
                raise RuntimeError(f"SDF export produced empty file at {sdf_path}")
            
            logger.info(f"✓ Scene export complete: {sdf_path} ({file_size} bytes)")
            return sdf_path
        
        except Exception as e:
            logger.error(f"Gazebo export failed: {e}")
            # Ensure full launch tree is terminated even on error.
            if process is not None:
                logger.info("Cleaning up: terminating Gazebo/RViz launch process group...")
                self._terminate_process_group(process, timeout=10)
            raise


class SDFProcessor:
    """Processes and fixes exported SDF files."""
    
    @staticmethod
    def fix_sdf(sdf_path: Path) -> Path:
        """
        Fix corrupted SDF URIs.
        
        Fixes:
        1. <urdf-string> in mesh URIs
        2. Broken relative mesh URIs for plugs and modules
        
        Returns:
            Path to fixed SDF file
        """
        logger.info(f"Fixing SDF: {sdf_path}")
        
        with open(sdf_path, 'r') as f:
            content = f.read()
        
        # Fix Issue 1: <urdf-string> in mesh URIs
        content = re.sub(
            r'file://<urdf-string>/model://',
            'model://',
            content
        )

        # # Fix Issue 1: <urdf-string> in mesh URIs
        # content = content.replace(
        #     'file://<urdf-string>/model://',
        #     'model://'
        # )
        
        # Fix Issue 2: Broken relative mesh URIs
        content = content.replace(
            'file:///lc_plug_visual.glb',
            'model://LC Plug/lc_plug_visual.glb'
        )
        content = content.replace(
            'file:///sc_plug_visual.glb',
            'model://SC Plug/sc_plug_visual.glb'
        )
        content = content.replace(
            'file:///sfp_module_visual.glb',
            'model://SFP Module/sfp_module_visual.glb'
        )
        
        with open(sdf_path, 'w') as f:
            f.write(content)
        
        logger.info("SDF fixes applied")
        return sdf_path

    # @staticmethod
    # def fix_sdf(sdf_path: Path) -> Path:
    #     """
    #     Fix corrupted SDF URIs.
        
    #     Fixes:
    #     1. <urdf-string> in mesh URIs
    #     2. Broken relative mesh URIs for plugs and modules
        
    #     Returns:
    #         Path to fixed SDF file
    #     """
    #     logger.info(f"Fixing SDF: {sdf_path}")
        
    #     cmd = [
    #         "bash", "-c",
    #         f"sed -i 's|file://<urdf-string>/model://|model://|g' {sdf_path} && "
    #         f"sed -i 's|file:///lc_plug_visual.glb|model://LC Plug/lc_plug_visual.glb|g' {sdf_path} && "
    #         f"sed -i 's|file:///sc_plug_visual.glb|model://SC Plug/sc_plug_visual.glb|g' {sdf_path} && "
    #         f"sed -i 's|file:///sfp_module_visual.glb|model://SFP Module/sfp_module_visual.glb|g' {sdf_path}"
    #     ]
        
    #     try:
    #         result = subprocess.run(
    #             cmd,
    #             capture_output=True,
    #             text=True,
    #             timeout=300
    #         )
            
    #         if result.returncode != 0:
    #             logger.error(f"sed fix failed: {result.stderr}")
    #             raise RuntimeError(f"sed fix failed")
        
    #     except subprocess.TimeoutExpired:
    #         raise RuntimeError("sed fix timed out")
        
    #     logger.info("SDF fixes applied")
    #     return sdf_path
    
    @staticmethod
    def rename_sdf(source_sdf: Path, scene_name: str, dest_dir: Path) -> Path:
        """
        Rename SDF file based on scene configuration.
        
        Returns:
            Path to renamed SDF file
        """
        dest_sdf = dest_dir / f"{scene_name}.sdf"
        shutil.copy2(source_sdf, dest_sdf)
        logger.info(f"SDF renamed and moved to {dest_sdf}")
        return dest_sdf


class MJCFConverter:
    """Handles SDF to MJCF conversion."""
    
    def __init__(self, ws_path: Path):
        """Initialize converter."""
        self.ws_path = ws_path
    
    def convert_to_mjcf(self, sdf_path: Path, output_dir: Path) -> Path:
        """
        Convert SDF to MJCF using sdf2mjcf tool.
        
        Returns:
            Path to output directory containing MJCF and assets
        """
        logger.info(f"Converting SDF to MJCF: {sdf_path}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "bash", "-c",
            f"source {self.ws_path}/install/setup.bash && "
            f"sdf2mjcf {sdf_path} {output_dir}/aic_world.xml"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                logger.error(f"sdf2mjcf failed: {result.stderr}")
                raise RuntimeError(f"sdf2mjcf conversion failed")
            
            logger.info(f"MJCF conversion completed to {output_dir}")
            return output_dir
        
        except subprocess.TimeoutExpired:
            raise RuntimeError("sdf2mjcf conversion timed out")


class MJCFOrganizer:
    """Organizes MJCF files and mesh assets."""
    
    @staticmethod
    def organize_assets(source_dir: Path, dest_dir: Path) -> None:
        """
        Copy MJCF files and mesh assets to destination directory.
        
        Moves .xml, .obj, and .png files to the mjcf folder.
        """
        logger.info(f"Organizing MJCF assets from {source_dir} to {dest_dir}")
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all relevant files
        for file_pattern in ['*.xml', '*.obj', '*.png', '*.mtl', '*.stl']:
            for src_file in source_dir.glob(file_pattern):
                if src_file.is_file():
                    dst_file = dest_dir / src_file.name
                    shutil.copy2(src_file, dst_file)
                    logger.info(f"Copied {src_file.name}")
        
        logger.info(f"Assets organized in {dest_dir}")


class CablePluginProcessor:
    """Applies cable plugin and other post-processing."""
    
    def __init__(self, ws_path: Path, script_dir: Path):
        """Initialize processor."""
        self.ws_path = ws_path
        self.script_dir = script_dir
        self.add_cable_script = script_dir / "add_cable_plugin.py"
    
    def process_mjcf(self, mjcf_dir: Path) -> None:
        """
        Apply cable plugin processing and post-processing.
        
        This runs add_cable_plugin.py to split and refine MJCF files.
        """
        logger.info(f"Processing MJCF with cable plugin: {mjcf_dir}")
        
        if not self.add_cable_script.exists():
            logger.warning(f"Cable plugin script not found: {self.add_cable_script}")
            logger.info("Skipping cable plugin processing")
            return
        
        # Verify input files exist
        input_file = mjcf_dir / "aic_world.xml"
        if not input_file.exists():
            logger.error(f"Input MJCF file not found: {input_file}")
            raise FileNotFoundError(f"Input MJCF file not found: {input_file}")
        
        cmd = [
            "python3",
            str(self.add_cable_script),
            "--input", str(input_file),
            "--output", str(mjcf_dir / "aic_world.xml"),
            "--robot_output", str(mjcf_dir / "aic_robot.xml"),
            "--scene_output", str(mjcf_dir / "scene.xml"),
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.script_dir.parent)
            )
            
            if result.returncode != 0:
                logger.error(f"Cable plugin processing failed: {result.stderr}")
                if result.stdout:
                    logger.error(f"Stdout: {result.stdout}")
                raise RuntimeError("Cable plugin processing failed")
            
            logger.info("Cable plugin processing completed")
        
        except subprocess.TimeoutExpired:
            raise RuntimeError("Cable plugin processing timed out")


class ExportOrganizer:
    """Organizes exported scenes in the final export directory."""
    
    @staticmethod
    def organize_scene(mjcf_dir: Path, export_base_dir: Path, scene_name: str) -> Path:
        """
        Copy scene files to export directory organized by scene name.
        
        Returns:
            Path to organized scene directory
        """
        logger.info(f"Organizing scene for export: {scene_name}")
        
        scene_export_dir = export_base_dir / scene_name
        scene_export_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all MJCF and asset files
        for src_file in mjcf_dir.glob('*'):
            if src_file.is_file():
                dst_file = scene_export_dir / src_file.name
                shutil.copy2(src_file, dst_file)
                logger.info(f"Copied {src_file.name} to {scene_export_dir}")
        
        logger.info(f"Scene organized at {scene_export_dir}")
        return scene_export_dir


class OrchestrationManager:
    """Orchestrates the entire scene generation workflow."""
    
    def __init__(
        self,
        ws_path: Path,
        num_scenes: int,
        output_dir: Path,
        export_timeout: int = 120,
        gazebo_gui: bool = True,
        launch_rviz: bool = False,
    ):
        """Initialize orchestration manager."""
        self.ws_path = Path(ws_path)
        self.num_scenes = num_scenes
        self.output_dir = Path(output_dir)
        self.script_dir = Path(__file__).parent
        self.export_timeout = export_timeout
        self.gazebo_gui = gazebo_gui
        self.launch_rviz = launch_rviz
        
        # Create output directory structure
        self.mjcf_base_dir = self.ws_path / "src/aic/aic_utils/aic_mujoco/mjcf"
        self.export_base_dir = Path("/mnt/hgfs/exported mujoco training envs")
        
        # Initialize components
        self.scene_generator = SceneGenerator()
        self.gazebo_exporter = GazeboExporter(
            self.ws_path,
            gazebo_gui=self.gazebo_gui,
            launch_rviz=self.launch_rviz,
        )
        self.mjcf_converter = MJCFConverter(self.ws_path)
        self.cable_processor = CablePluginProcessor(self.ws_path, self.script_dir)
    
    def process_single_scene(self, config: SceneConfig, scene_index: int) -> Tuple[bool, str]:
        """
        Process a single scene through the entire workflow.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing scene {scene_index + 1}/{self.num_scenes}: {config.scene_name}")
            logger.info(f"{'='*60}")
            
            # Step 1: Export from Gazebo
            sdf_path = self.gazebo_exporter.export_scene(config, timeout=self.export_timeout)
            
            # Step 2: Fix SDF
            SDFProcessor.fix_sdf(sdf_path)
            
            # Create scene-specific directories
            scene_sdf_dir = self.mjcf_base_dir / config.scene_name / "sdf"
            scene_mjcf_dir = self.mjcf_base_dir / config.scene_name / "mjcf"
            scene_temp_dir = Path(tempfile.mkdtemp(prefix=f"mujoco_{config.scene_name}_"))
            
            scene_sdf_dir.mkdir(parents=True, exist_ok=True)
            scene_mjcf_dir.mkdir(parents=True, exist_ok=True)
            
            # Save renamed SDF
            SDFProcessor.rename_sdf(sdf_path, config.scene_name, scene_sdf_dir)
            
            # Step 3: Convert to MJCF
            self.mjcf_converter.convert_to_mjcf(sdf_path, scene_temp_dir)
            
            # Step 4: Organize assets
            MJCFOrganizer.organize_assets(scene_temp_dir, scene_mjcf_dir)
            
            # Step 5: Process with cable plugin
            self.cable_processor.process_mjcf(scene_mjcf_dir)
            
            # Step 6: Copy to export directory
            if self.export_base_dir.exists():
                ExportOrganizer.organize_scene(scene_mjcf_dir, self.export_base_dir, config.scene_name)
                logger.info(f"Scene exported to {self.export_base_dir / config.scene_name}")
            else:
                logger.warning(f"Export directory not found: {self.export_base_dir}")
            
            # Cleanup temporary directory
            shutil.rmtree(scene_temp_dir, ignore_errors=True)
            
            logger.info(f"Scene {scene_index + 1} completed successfully")
            return True, f"Scene {config.scene_name} completed successfully"
        
        except Exception as e:
            logger.error(f"Scene {scene_index + 1} processing failed: {e}")
            return False, str(e)
    
    def run(self) -> None:
        """Run the entire scene generation workflow."""
        logger.info(f"Starting automated scene generation: {self.num_scenes} scenes")
        logger.info(f"Workspace: {self.ws_path}")
        logger.info(f"MJCF output: {self.mjcf_base_dir}")
        logger.info(f"Export directory: {self.export_base_dir}")
        
        # Generate all unique configurations first
        logger.info("Generating unique scene configurations...")
        configs = []
        for i in range(self.num_scenes):
            config = self.scene_generator.generate_random_config()
            configs.append(config)
            logger.info(f"  [{i+1}/{self.num_scenes}] {config.scene_name}")
        
        # Save configuration manifest
        manifest_path = self.mjcf_base_dir / "scene_manifest.json"
        manifest_data = {
            "num_scenes": self.num_scenes,
            "scenes": [{"index": i, "name": c.scene_name, "config": asdict(c)} 
                      for i, c in enumerate(configs)]
        }
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=2)
        logger.info(f"Scene manifest saved to {manifest_path}")
        
        # Process each scene
        successful = 0
        failed = 0
        
        for i, config in enumerate(configs):
            try:
                success, message = self.process_single_scene(config, i)
                if success:
                    successful += 1
                else:
                    failed += 1
                    logger.error(message)
            except Exception as e:
                failed += 1
                logger.error(f"Unexpected error processing scene {i}: {e}")
        
        # Print summary
        logger.info(f"\n{'='*60}")
        logger.info(f"Scene generation workflow completed")
        logger.info(f"{'='*60}")
        logger.info(f"Total scenes: {self.num_scenes}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"MJCF output directory: {self.mjcf_base_dir}")
        logger.info(f"Export directory: {self.export_base_dir}")
        logger.info(f"{'='*60}\n")
        
        if failed > 0:
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automate scene generation and export from Gazebo to MuJoCo"
    )
    parser.add_argument(
        '--num_scenes',
        type=int,
        required=True,
        help='Number of unique scenes to generate'
    )
    parser.add_argument(
        '--ws_path',
        type=str,
        default=os.path.expanduser("~/ws_aic"),
        help='Path to ROS 2 workspace'
    )
    parser.add_argument(
        '--export_timeout',
        type=int,
        default=120,
        help='Timeout in seconds for each Gazebo export'
    )
    parser.add_argument(
        '--gazebo_gui',
        type=parse_bool_arg,
        default=True,
        help='Whether to show Gazebo GUI (true/false)'
    )
    parser.add_argument(
        '--launch_rviz',
        type=parse_bool_arg,
        default=False,
        help='Whether to launch RViz (true/false)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    ws_path = Path(args.ws_path)
    if not ws_path.exists():
        logger.error(f"Workspace path does not exist: {ws_path}")
        sys.exit(1)
    
    if args.num_scenes < 1:
        logger.error("Number of scenes must be >= 1")
        sys.exit(1)
    
    # Run orchestration
    manager = OrchestrationManager(
        ws_path=ws_path,
        num_scenes=args.num_scenes,
        output_dir=ws_path / "src/aic/aic_utils/aic_mujoco/mjcf",
        export_timeout=args.export_timeout,
        gazebo_gui=args.gazebo_gui,
        launch_rviz=args.launch_rviz,
    )
    
    manager.run()


if __name__ == "__main__":
    main()