# Automated Randomised Cheatcode Recording

## What this does

`recording_randomized_framework.py` is a copy of `recording_framework.py` extended to record datasets **without any human input**. Instead of a VR controller, it uses the `aic_cheatcode` teleop, which drives the arm using ground-truth TF frames read directly from the simulation.

Each iteration of the loop:
1. Generates a random scene (random task board pose, cable type, which components are present, and their positions).
2. Picks an insertion target that the cheatcode can actually reach and guarantees it is present in the scene.
3. Launches Gazebo with those parameters.
4. Runs `lerobot-record` with the cheatcode teleop for one episode.
5. Tears the scene down and repeats.

### Changes made relative to `recording_framework.py`

**`SceneConfig`** — four new fields were added to carry the cheatcode target for each generated scene:
- `task_cable_name` — always `cable_0`
- `task_plug_name` — `sfp_tip` for `sfp_sc_cable`, `sc_tip` for `sfp_sc_cable_reversed`
- `task_module_name` — the randomly selected port module (e.g. `nic_card_mount_2`, `sc_port_0`)
- `task_port_name` — the port on that module (`sfp_port_0`, `sfp_port_1`, or `sc_port_base`)

**`generate_random_config`** — after randomising component presence, a new block selects the insertion target and guarantees at least one compatible port module is present in the scene (NIC card mounts for `sfp_sc_cable`, SC ports for `sfp_sc_cable_reversed`). For NIC card mounts, the port is also randomised between `sfp_port_0` and `sfp_port_1` for additional trajectory variety.

**`RecordingTask.cheatcode_lerobot_command`** — new method that builds the `lerobot-record` command with `aic_cheatcode` as the teleop type and passes the four TF frame names from the `SceneConfig`.

**`main_cheatcode`** — new fully-automated entry point. No Quest prompt, no task menu, no episode prompt.

---

## How to run

```bash
pixi run python3 recording_randomized_framework.py
```

That runs the original interactive VR flow (unchanged). To run the automated cheatcode loop, call `main_cheatcode` directly:

```bash
pixi run python3 - <<'EOF'
from recording_randomized_framework import main_cheatcode
raise SystemExit(main_cheatcode())
EOF
```

Or add a small launcher script and invoke it:

```bash
pixi run python3 -c "from recording_randomized_framework import main_cheatcode; raise SystemExit(main_cheatcode())" \
  --repo-id caai-aic/aic-cheatcode-random \
  --num-scenes 50
```

### CLI arguments

| Argument | Default | Description |
|---|---|---|
| `--repo-id` | `caai-aic/aic-cheatcode-random` | Hugging Face dataset repo to write into |
| `--task-description` | `insert plug` | Single-task string stored in the dataset |
| `--num-scenes` | `0` | Number of scenes to record; `0` runs until Ctrl-C |
| `--ws-path` | AIC repo root | Path to `ws_aic_caai/src/aic` |
| `--hf-token-path` | *(none)* | Path to a file containing your HF token |

### Example: record 100 scenes into a custom repo

```bash
pixi run python3 -c "
from recording_randomized_framework import main_cheatcode
raise SystemExit(main_cheatcode())
" -- --repo-id caai-aic/my-dataset --num-scenes 100
```

Press **Ctrl-C** at any time to stop cleanly after the current episode finishes.
