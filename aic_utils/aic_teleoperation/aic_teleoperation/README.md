# Vr Workflow

Open 3 shell windows


### Terminal 1 Gazebo sim

####


#### (Optional) Enable Nvidia gpu for gazebo
```bash
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia

```



```bash


/entrypoint.sh spawn_task_board:=true     task_board_x:=0.3 task_board_y:=-0.1 task_board_z:=1.2     task_board_roll:=0.0 task_board_pitch:=0.0 task_board_yaw:=0.785     sfp_mount_rail_0_present:=true sfp_mount_rail_0_translation:=-0.08     sc_mount_rail_0_present:=true sc_mount_rail_0_translation:=-0.09     nic_card_mount_0_present:=true nic_card_mount_0_translation:=0.005     sc_port_0_present:=true sc_port_0_translation:=-0.04     spawn_cable:=true cable_type:=sfp_sc_cable attach_cable_to_gripper:=true     ground_truth:=true start_aic_engine:=false
```


### Terminal 2 

```bash
# source ros2 setup.bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
cd oculus_reader/
python3 oculus_reader/viz_transforms.py 

```


### Terminal 3
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_teleoperation/aic_teleoperation
pixi run python3 vr_aic.py 
```
