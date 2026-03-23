#!/bin/bash

# Change to workspace directory
cd $HOME/ws_aic

# Source ROS 2 workspace FIRST
source $HOME/ws_aic/install/setup.zsh

# Gazebo system plugin path
export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/ws_aic/install/lib

# Library path for dynamic loading
export DYLD_LIBRARY_PATH=$HOME/ws_aic/install/lib:$HOME/ws_aic/src/aic/.pixi/envs/default/lib:$DYLD_LIBRARY_PATH

# Gazebo rendering resource path
export GZ_RENDERING_RESOURCE_PATH=$HOME/ws_aic/src/aic/.pixi/envs/default/lib/gz-rendering-9

echo "✓ Gazebo environment configured"
echo "  Working directory: $(pwd)"
echo "  ROS_DISTRO: $ROS_DISTRO"
echo "  GZ_SIM_SYSTEM_PLUGIN_PATH: $GZ_SIM_SYSTEM_PLUGIN_PATH"

# Verify aic packages are available
if ros2 pkg list | grep -q aic_bringup; then
    echo "✓ aic_bringup package found"
else
    echo "✗ ERROR: aic_bringup package not found!"
    echo "  Run 'colcon build' in ~/ws_aic first"
fi