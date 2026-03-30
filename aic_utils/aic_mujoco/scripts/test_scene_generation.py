#!/usr/bin/env python3
"""
Test and validation utility for scene generation automation.

Helps verify the setup and test individual components before running full automation.

Usage:
    python3 test_scene_generation.py --test <test_name>

Available tests:
    - dependencies: Check if all required packages are installed
    - gazebo: Test Gazebo launch and SDF export
    - sdf_conversion: Test SDF to MJCF conversion
    - cable_plugin: Test cable plugin processing
    - single_scene: Generate and export a single test scene
"""

import argparse
import logging
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestRunner:
    """Runs diagnostic tests for scene generation setup."""
    
    def __init__(self, ws_path: Path):
        """Initialize test runner."""
        self.ws_path = Path(ws_path)
        self.env = os.environ.copy()
        self._setup_ros_env()
    
    def _setup_ros_env(self):
        """Setup ROS 2 environment."""
        self.env['RMW_IMPLEMENTATION'] = 'rmw_zenoh_cpp'
        self.env['ZENOH_CONFIG_OVERRIDE'] = \
            'transport/shared_memory/enabled=true;transport/shared_memory/transport_optimization/pool_size=536870912'
    
    def test_dependencies(self) -> bool:
        """Test if all required packages are installed."""
        logger.info("Testing dependencies...")
        
        dependencies = {
            "sdf2mjcf": "sdformat_mjcf tool",
            "python3": "Python 3",
            "sdformat16": "Python SDFormat bindings",
            "gz.math9": "Gazebo Math Python bindings",
        }
        
        all_ok = True
        
        for dep, desc in dependencies.items():
            if dep.startswith("python"):
                # Python modules
                try:
                    __import__(dep.replace(".", "_"))
                    logger.info(f"✓ {desc} ({dep})")
                except ImportError:
                    logger.error(f"✗ {desc} ({dep}) - NOT FOUND")
                    all_ok = False
            else:
                # System commands
                result = subprocess.run(
                    ["which", dep],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info(f"✓ {desc} ({result.stdout.strip()})")
                else:
                    logger.error(f"✗ {desc} ({dep}) - NOT FOUND")
                    all_ok = False
        
        # Test Python imports
        logger.info("\nTesting Python imports...")
        python_imports = {
            "sdformat16": "SDFormat",
            "gz.math9": "Gazebo Math",
        }
        
        for module, desc in python_imports.items():
            try:
                __import__(module)
                logger.info(f"✓ {desc} ({module})")
            except ImportError as e:
                logger.error(f"✗ {desc} ({module}) - {e}")
                all_ok = False
        
        if all_ok:
            logger.info("\n✓ All dependencies found")
            return True
        else:
            logger.error("\n✗ Some dependencies missing. Install with:")
            logger.error("  sudo apt install -y python3-sdformat16 python3-gz-math9")
            return False
    
    def test_gazebo_launch(self) -> bool:
        """Test Gazebo launch and SDF export."""
        logger.info("Testing Gazebo launch and SDF export...")
        logger.info("This will launch Gazebo for 30 seconds...")
        
        cmd = [
            "bash", "-c",
            f"source {self.ws_path}/install/setup.bash && "
            "ros2 launch aic_bringup aic_gz_bringup.launch.py "
            "spawn_task_board:=true ground_truth:=true"
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(30)
            process.terminate()
            process.wait(timeout=10)
            
            sdf_path = Path("/tmp/aic.sdf")
            if sdf_path.exists():
                file_size = sdf_path.stat().st_size
                logger.info(f"✓ Gazebo launch successful")
                logger.info(f"✓ SDF exported: {sdf_path} ({file_size} bytes)")
                return True
            else:
                logger.error("✗ SDF export failed - file not found")
                return False
        
        except Exception as e:
            logger.error(f"✗ Gazebo launch failed: {e}")
            return False
    
    def test_sdf_conversion(self) -> bool:
        """Test SDF to MJCF conversion."""
        logger.info("Testing SDF to MJCF conversion...")
        
        sdf_path = Path("/tmp/aic.sdf")
        if not sdf_path.exists():
            logger.error("✗ SDF file not found at /tmp/aic.sdf")
            logger.info("Run test_gazebo_launch first")
            return False
        
        with tempfile.TemporaryDirectory(prefix="test_mjcf_") as tmpdir:
            output_dir = Path(tmpdir)
            
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
                
                if result.returncode == 0:
                    output_file = output_dir / "aic_world.xml"
                    if output_file.exists():
                        file_size = output_file.stat().st_size
                        logger.info(f"✓ SDF conversion successful")
                        logger.info(f"✓ MJCF file generated: {output_file.name} ({file_size} bytes)")
                        
                        # Count mesh files
                        mesh_files = list(output_dir.glob("*.obj"))
                        logger.info(f"✓ Mesh files: {len(mesh_files)}")
                        return True
                    else:
                        logger.error("✗ MJCF output file not created")
                        return False
                else:
                    logger.error(f"✗ SDF conversion failed: {result.stderr}")
                    return False
            
            except subprocess.TimeoutExpired:
                logger.error("✗ SDF conversion timed out")
                return False
            except Exception as e:
                logger.error(f"✗ SDF conversion failed: {e}")
                return False
    
    def test_cable_plugin(self) -> bool:
        """Test cable plugin processing."""
        logger.info("Testing cable plugin processing...")
        
        script_path = Path(__file__).parent / "add_cable_plugin.py"
        if not script_path.exists():
            logger.warning(f"✗ Cable plugin script not found: {script_path}")
            return False
        
        logger.info(f"✓ Cable plugin script found: {script_path}")
        
        # Try to import it to verify it's valid Python
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("add_cable_plugin", script_path)
            module = importlib.util.module_from_spec(spec)
            logger.info("✓ Cable plugin script is valid Python")
            return True
        except Exception as e:
            logger.error(f"✗ Cable plugin script has errors: {e}")
            return False
    
    def test_single_scene(self) -> bool:
        """Generate and export a single test scene."""
        logger.info("Testing single scene generation...")
        
        script_path = Path(__file__).parent / "automate_scene_generation.py"
        if not script_path.exists():
            logger.error(f"✗ Automation script not found: {script_path}")
            return False
        
        test_output_dir = self.ws_path / "test_scene_output"
        
        try:
            cmd = [
                "python3", str(script_path),
                "--num_scenes", "1",
                "--ws_path", str(self.ws_path),
            ]
            
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info("✓ Single scene generation successful")
                logger.info(f"Output:\n{result.stdout}")
                return True
            else:
                logger.error(f"✗ Single scene generation failed")
                logger.error(f"Error:\n{result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("✗ Single scene generation timed out (>10 minutes)")
            return False
        except Exception as e:
            logger.error(f"✗ Single scene generation failed: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test and validate scene generation setup"
    )
    parser.add_argument(
        '--test',
        type=str,
        choices=['dependencies', 'gazebo', 'conversion', 'plugin', 'full', 'all'],
        default='dependencies',
        help='Test to run (default: dependencies)'
    )
    parser.add_argument(
        '--ws_path',
        type=str,
        default=os.path.expanduser("~/ws_aic"),
        help='Path to ROS 2 workspace'
    )
    
    args = parser.parse_args()
    
    ws_path = Path(args.ws_path)
    if not ws_path.exists():
        logger.error(f"Workspace path does not exist: {ws_path}")
        sys.exit(1)
    
    runner = TestRunner(ws_path)
    
    tests = {
        'dependencies': runner.test_dependencies,
        'gazebo': runner.test_gazebo_launch,
        'conversion': runner.test_sdf_conversion,
        'plugin': runner.test_cable_plugin,
    }
    
    results = {}
    
    if args.test == 'all':
        # Run all tests in sequence
        logger.info("\n" + "="*60)
        logger.info("Running all tests")
        logger.info("="*60 + "\n")
        
        test_names = ['dependencies', 'gazebo', 'conversion', 'plugin']
        for test_name in test_names:
            logger.info(f"\n--- Test: {test_name} ---")
            results[test_name] = tests[test_name]()
        
        logger.info("\n" + "="*60)
        logger.info("Test Summary")
        logger.info("="*60)
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            logger.info(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
    
    elif args.test == 'full':
        # Run dependencies, gazebo, conversion, plugin
        logger.info("\n" + "="*60)
        logger.info("Running full test suite")
        logger.info("="*60 + "\n")
        
        test_names = ['dependencies', 'gazebo', 'conversion', 'plugin']
        for test_name in test_names:
            logger.info(f"\n--- Test: {test_name} ---")
            results[test_name] = tests[test_name]()
        
        logger.info("\n" + "="*60)
        logger.info("Test Summary")
        logger.info("="*60)
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            logger.info(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
    
    else:
        # Run single test
        logger.info(f"Running test: {args.test}\n")
        result = tests[args.test]()
        sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
