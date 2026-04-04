# Vr Teleop Workflow

Prerequisites:
- Setup aic workspace
- Test evaluation container with example policies
- Install [rmw_zenoh](https://github.com/ros2/rmw_zenoh) if not on your system
- Clone and setup [oculus_reader](https://github.com/S-abk/oculus_reader)

Open 3 shell windows and run these in order:


### Terminal 1 - Simulation


```bash
#Enter AIC root directory
cd ~/ws_aic/src/aic

# Indicate distrobox to use Docker as container manager
export DBX_CONTAINER_MANAGER=docker

# Enter the eval container
distrobox enter -r aic_eval
```


(Optional) Enable Nvidia gpu for Gazebo and Rviz:
```bash
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
```

Start sim:
```bash
/entrypoint.sh spawn_task_board:=true     task_board_x:=0.3 task_board_y:=-0.1 task_board_z:=1.2     task_board_roll:=0.0 task_board_pitch:=0.0 task_board_yaw:=0.785     sfp_mount_rail_0_present:=true sfp_mount_rail_0_translation:=-0.08     sc_mount_rail_0_present:=true sc_mount_rail_0_translation:=-0.09     nic_card_mount_0_present:=true nic_card_mount_0_translation:=0.005     sc_port_0_present:=true sc_port_0_translation:=-0.04     spawn_cable:=true cable_type:=sfp_sc_cable attach_cable_to_gripper:=true     ground_truth:=true start_aic_engine:=false
```
This is an example configuration, change the argument values to vary the scene configuration:


### Terminal 2 - oculus_reader

Source ros2 setup.bash and set ros middleware as zenoh:
```bash
source /opt/ros/kilted/setup.bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
```

#### (Optional) ros2 sanity check
Check availability of topics to confirm ros2 communication with sim container:
```bash
ros2 topic list
```
If topics list is not populating, restart ros2 daemon and check again:
```bash
ros2 daemon stop
ros2 daemon start
```

#### Connect Headset
Put on headset on forehead so you can view your monitor through bare eyes. Connect USB C data cable
```bash
cd oculus_reader/
python3 oculus_reader/viz_transforms.py 
```


### Terminal 3 - Telop Interface
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_teleoperation/aic_teleoperation
pixi run python3 vr_aic.py 
```
