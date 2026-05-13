# Automated Randomised Cheatcode Recording

## What this does

`recording_randomized_framework.py` records robot arm datasets **without any human input**. Instead of a VR controller, it uses the `aic_cheatcode` teleop, which drives the arm using ground-truth TF frames read directly from the simulation. The script is designed to run overnight and collect large amounts of data fully autonomously.

Each episode is automatically routed to the correct dataset based on the target port and card mount — no `--repo-id` needed.

---

## Quick start

```bash
cd ~/ws_aic_caai/src/aic
pixi run python3 recording_randomized_framework.py
```

This runs indefinitely (until Ctrl-C) in headless mode, distributing episodes across all 12 target datasets automatically.

---

## What always happens (mandatory behavior)

Every iteration of the recording loop does the following unconditionally:

1. **Dataset selection** — the script picks whichever of the 12 datasets currently has the fewest saved episodes. The insertion target (cable type, module, port) is fixed by that dataset's definition.

2. **Random scene generation** — a new `SceneConfig` is drawn with random task board pose and random presence/positions of all board components. The cable type and insertion target are locked to the selected dataset, so only the surrounding scene geometry is randomised.

3. **Scene launch** — Gazebo is launched inside the `aic_eval` Docker container with the generated parameters.

4. **Scene readiness check** — the script blocks until Gazebo is confirmed fully loaded. It polls two independent signals; whichever reaches 3 consecutive positive detections first wins:
   - `gzserver` process detected inside the container via `docker exec aic_eval pgrep -f gzserver`
   - `/tmp/aic.sdf` present on the host filesystem (written by Gazebo after it exports the full world — a stronger signal that all objects are spawned)

5. **Object spawn confirmation** — a TF lookup confirms the cable's plug frame is visible before lerobot starts.

6. **Force-torque sensor tare** — `ros2 service call /aic_controller/tare_force_torque_sensor` is called before recording begins, zeroing any baseline drift.

7. **lerobot-record launch** — starts with `--teleop.type=aic_cheatcode`, passing the four TF frame names from the scene config so the cheatcode knows exactly which port to target.

8. **Episode end detection** — the cheatcode drives the episode to completion entirely on its own:
   - **Success**: subscribes to `/scoring/insertion_event` (Gazebo's CablePlugin ground-truth signal). The moment the plug physically seats, the cheatcode transitions to `DONE` and signals lerobot to save via a shared Python flag (`events["exit_early"]`).
   - **Failure**: each phase has a hard timeout (configurable at the top of `aic_teleop.py` as `APPROACH_TIMEOUT_S`, `ALIGN_TIMEOUT_S`, `INSERT_TIMEOUT_S`, all defaulting to 60s). If a phase exceeds its timeout, the cheatcode signals lerobot to discard the episode and exit cleanly — no wall-clock timer in the framework script is involved.

9. **Episode outcome** — if lerobot exits with code 0, the episode is saved. If the timeout expires before lerobot exits, the episode is discarded and the scene config is logged to `--failure-log`.

10. **Scene teardown** — Gazebo is stopped and processes are cleaned up before the next iteration.

11. **Dataset state management** — before each episode, the script checks `meta/info.json` in the dataset directory:
    - If `total_episodes > 0` → lerobot is started with `--resume=true`, preserving all prior data.
    - If the directory exists but has no completed episodes (e.g. a previous run crashed mid-initialisation) → the directory is deleted and lerobot starts fresh.

---

## Datasets recorded

The script automatically records into these 12 datasets:

| Cable type | Target | Dataset repo |
|---|---|---|
| SFP | sfp_port_0 of nic_card_mount_0 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_0` |
| SFP | sfp_port_1 of nic_card_mount_0 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_0` |
| SFP | sfp_port_0 of nic_card_mount_1 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_1` |
| SFP | sfp_port_1 of nic_card_mount_1 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_1` |
| SFP | sfp_port_0 of nic_card_mount_2 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_2` |
| SFP | sfp_port_1 of nic_card_mount_2 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_2` |
| SFP | sfp_port_0 of nic_card_mount_3 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_3` |
| SFP | sfp_port_1 of nic_card_mount_3 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_3` |
| SFP | sfp_port_0 of nic_card_mount_4 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_0_of_nic_card_mount_4` |
| SFP | sfp_port_1 of nic_card_mount_4 | `caai-aic/corrected_lab_collected_sfp_to_sfp_port_1_of_nic_card_mount_4` |
| SC | sc_port_base of sc_port_0 | `caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_0` |
| SC | sc_port_base of sc_port_1 | `caai-aic/corrected_lab_collected_sc_to_sc_port_base_of_sc_port_1` |

All datasets are stored locally under `~/.cache/huggingface/lerobot/<repo-id>/`.

---

## What you can configure (optional behavior)

### `--num-scenes`
**Default:** `0` (run forever)

Target number of **successful episodes per dataset**. Set to `0` to run until Ctrl-C.

When set to `N` the script keeps running until every dataset has at least `N` saved episodes. On each iteration it picks whichever dataset currently has the fewest episodes, so all 12 datasets fill up evenly. For example `--num-scenes 5` records 5 episodes for each of the 12 datasets (60 episodes total).

Failed scenes (insertion timeout) do **not** count toward the target — only successful insertions produce saved episodes.

```bash
# Record 5 episodes for each of the 12 datasets (60 total)
pixi run python3 recording_randomized_framework.py --num-scenes 5
```

---

### `--failure-log`
**Default:** `failed_scenes.jsonl`

Path to a file where failed scene configs are appended. Each failed attempt writes one JSON line containing the full `SceneConfig` (all positions, angles, component presence flags, cable type, insertion target) plus a timestamp. The file is created if it does not exist.

```bash
pixi run python3 recording_randomized_framework.py --failure-log /tmp/failures_run1.jsonl
```

Example entry:
```json
{"timestamp": "2026-05-12T22:30:00", "task_cable_name": "cable_0", "task_plug_name": "sfp_tip", "task_module_name": "nic_card_mount_2", "task_port_name": "sfp_port_1", "robot_z": 1.14, "task_board_x": 0.21, "task_board_yaw": 1.05, ...}
```

---

### `--headless` / `--no-headless`
**Default:** `--headless`

Controls whether Gazebo opens a GUI window.

```bash
# Watch the simulation (requires active display)
pixi run python3 recording_randomized_framework.py --no-headless --num-scenes 10
```

---

### `--push-to-hub` / `--no-push-to-hub`
**Default:** `--no-push-to-hub`

When enabled, lerobot uploads each completed episode to the Hugging Face Hub after it is saved locally. Requires HuggingFace authentication (see below).

```bash
pixi run python3 recording_randomized_framework.py --push-to-hub
```

---

### `--hf-token-path`
**Default:** *(none — reads from `~/.cache/huggingface/token` automatically)*

Path to a file containing a HuggingFace API token. Only needed if your token lives somewhere non-standard.

---

### `--ws-path`
**Default:** `~/ws_aic_caai/src/aic`

Path to the AIC workspace root. Only needed if you run the script from a non-standard location.

---

## HuggingFace setup

By default the script records **locally only** — no HuggingFace account is needed. If you want episodes pushed to the Hub (via `--push-to-hub`), follow these steps once per machine:

### 1. Create a HuggingFace account and get a token

Go to [huggingface.co](https://huggingface.co), create an account, and generate a token at **Settings → Access Tokens**. The token needs **write** access to the target repositories.

### 2. Log in on the machine

```bash
pixi run huggingface-cli login
```

Paste your token when prompted. This writes it to `~/.cache/huggingface/token`, which the script reads automatically.

### Notes

- Episodes are pushed incrementally after each successful episode — if the run is interrupted, all previously pushed episodes are safe.
- The dataset is always written to local cache first regardless of whether push is enabled.
- If you are on a machine without internet access, omit `--push-to-hub` and sync manually later using `huggingface-cli upload-large-folder`.

---

## Usage examples

### Overnight run — 50 episodes per dataset, local only

```bash
pixi run python3 recording_randomized_framework.py \
  --num-scenes 50 \
  --failure-log ~/logs/overnight-run-01-failures.jsonl
```

### Overnight run — upload to Hub

```bash
pixi run python3 recording_randomized_framework.py \
  --num-scenes 50 \
  --push-to-hub \
  --failure-log ~/logs/overnight-run-01-failures.jsonl
```

### Quick test — 5 episodes per dataset, interactive

```bash
pixi run python3 recording_randomized_framework.py \
  --no-headless \
  --num-scenes 5
```

### Run forever until manually stopped

```bash
pixi run python3 recording_randomized_framework.py
```

Press **Ctrl-C** at any time to stop cleanly after the current episode finishes.
