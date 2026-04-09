# Setup Workflow

## Prerequisites
- Ros2 kilted (ideal but not exclusive - alternatively robostack/pixi workflow to be included)
- Setup aic workspace
- Test evaluation container with example policies
- [rmw_zenoh](https://github.com/ros2/rmw_zenoh) if not on your system
- [oculus_reader](https://github.com/S-abk/oculus_reader) - take a look at [this section](#First-time-setup)

---

Open 3 shell windows accordingly:


## Terminal 1 - Simulation


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
This is an example configuration, change the argument values to vary the scene configuration

---

## Terminal 2 - oculus_reader

Source ros2 setup.bash and set ros middleware as zenoh:
```bash
source /opt/ros/kilted/setup.bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
```

### (Optional) ROS2 sanity check
Ensure availability of topics to confirm ros2 communication with sim container:
```bash
ros2 topic list
```
If topics are not populating, restart ros2 daemon and check again:
```bash
ros2 daemon stop
ros2 daemon start
```

### First time setup
After cloning [oculus_reader](https://github.com/S-abk/oculus_reader) and installing [ADB](https://github.com/rail-berkeley/oculus_reader?tab=readme-ov-file#setup-of-the-adb), in a virtual environment, install the oculus_reader python package in editable mode from the repo root:
```bash
cd ~/oculus_reader/
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```
### Connect Headset
Put headset on your forehead so you can view your monitor directly with bare eyes. Connect USB C data cable and run
```bash
cd ~/oculus_reader/
source ~/oculus_reader/.venv/bin/activate
python3 oculus_reader/viz_transforms.py 
```



---

## Terminal 3 - Telop Interface
```bash
cd ~/ws_aic/src/aic/aic_utils/aic_teleoperation/aic_teleoperation
pixi run python3 vr_aic.py 
```



# Controller Guide — AIC UR5e Teleoperation

Quick reference for operating the Oculus Quest right controller with `vr_aic.py`


On launch the node automatically switches the AIC controller to Cartesian mode and tares the F/T sensor. If the force reading in the HUD is non-zero after startup, press **`t`** to re-tare manually.

---

## Control Modes

Press **A** on the right controller to cycle through modes:

```
IDLE  ──[A]──▶  VR TRACKING  ──[A]──▶  ANALOGUE  ──[A]──▶  IDLE
```

| Mode | Behaviour |
|------|-----------|
| **IDLE** | Robot holds last commanded pose. Safe starting state. |
| **VR TRACKING** | Full 6-DOF wrist mirroring. Reference pose is captured on entry. |
| **ANALOGUE** | Fine-grained stick control. VR tracking is off. |

Both modes can be combined — enable VR tracking first, then analogue mode adds stick offsets on top each tick.

---

## Right Controller Buttons

| Button | Action |
|--------|--------|
| **A** | Cycle mode: IDLE → VR TRACKING → ANALOGUE → IDLE |
| **B** | Toggle orientation follow on / off |
| **RJ** (stick click) | Toggle analogue frame: `base_link` ↔ TCP |

---

## Analogue Stick Modes

With no modifier held the stick provides yaw and vertical control. Hold **grip** or **trigger** to change behaviour:

| Modifier | Stick left/right | Stick forward/back |
|----------|-----------------|-------------------|
| None | Yaw | Z (up / down) |
| **Grip** held | X translation | Y translation |
| **Trigger** held | Pitch | Roll |

Stick offsets persist when released — the robot holds its nudged position. Offsets reset when analogue mode is re-enabled (A) or when a new VR reference is captured (keyboard `e`).

### Frame selection (RJ)

| Frame | Stick axes relative to… |
|-------|------------------------|
| `base` | World / robot base (default) |
| `tcp` | Gripper tip — "forward" always means along the approach direction |

TCP frame is useful for insertion tasks where you want to nudge along the tool axis.

---

## Keyboard Reference

| Key | Action |
|-----|--------|
| `e` | Enable VR tracking (capture reference) |
| `q` | Disable VR tracking |
| `o` | Toggle orientation follow |
| `g` | Toggle gripper open / closed |
| `f` | Toggle force-feedback stiffness modulation |
| `l` | Toggle workspace limits |
| `t` | Re-tare F/T sensor |
| `x` | Exit |

---

## Terminal HUD

A live status bar is rendered at the bottom of the terminal:

```
  ─────────────────────────────────────────────────  [x] quit
  MODE   VR ● TRACKING   ANALOGUE ○ OFF   FRAME: base   ORI: off
  F/T    ████████░░░░░░░░░░░░░░░░░░░░░░    6.2 N   contact
                  2N              20N
```

| Colour | Meaning |
|--------|---------|
| 🟢 Green | Free — below 2 N contact threshold |
| 🟡 Yellow | Contact — stiffness begins reducing |
| 🔴 Red | High force — at minimum stiffness (20 N+) |

If the reading is non-zero at rest, press **`t`** to re-tare.

---

## Force Feedback

When enabled (`f`), Cartesian stiffness reduces automatically with contact force:

| Force | Stiffness |
|-------|-----------|
| < 2 N | 60 (full teleop) |
| 2 – 20 N | 60 → 15 (linear) |
| > 20 N | 15 (maximum compliance) |

For cable and connector insertion where high stiffness would resist the environment.

---

## Tips

- Always start in **IDLE** and verify the F/T reading is near zero before enabling motion.
- Use **VR TRACKING** to move to the task area, then switch to **ANALOGUE** for fine positioning.
- **TCP frame** (RJ toggle) makes insertion nudges intuitive — you push toward the connector regardless of gripper orientation.
- Workspace limits are off by default. Enable with `l` to constrain motion to the defined safe volume.
- Press `t` any time the force reading looks wrong — re-taring takes effect immediately.
