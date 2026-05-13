#!/usr/bin/env bash
set -euo pipefail

PIXI_SITE=~/ws_aic_caai/src/aic/.pixi/envs/default/lib/python3.12/site-packages

TELEOP=$PIXI_SITE/lerobot_robot_aic/aic_teleop.py
RECORD=$PIXI_SITE/lerobot/scripts/lerobot_record.py
FRAMEWORK=~/ws_aic_caai/src/aic/recording_randomized_framework.py

# --- 1. aic_teleop.py: deeper insertion + wider spiral ---
sed -i 's/insertion_depth: float = -0.035/insertion_depth: float = -0.080/' "$TELEOP"
sed -i 's/insertion_depth: float = -0.050/insertion_depth: float = -0.080/' "$TELEOP"
sed -i 's/spiral_radius: float = 0.003/spiral_radius: float = 0.006/' "$TELEOP"
rm -rf "$(dirname "$TELEOP")/__pycache__"

# --- 2. lerobot_record.py: add _recording_events bridge ---
python3 - <<'EOF'
import pathlib, os

f = pathlib.Path(os.path.expanduser(
    "~/ws_aic_caai/src/aic/.pixi/envs/default/lib/python3.12/site-packages"
    "/lerobot/scripts/lerobot_record.py"
))
txt = f.read_text()
if "_recording_events" in txt:
    print("Bridge already present — skipping")
else:
    target = "        listener, events = init_keyboard_listener()"
    patch = (
        "\n        try:\n"
        "            import lerobot_robot_aic as _aic\n"
        "            _aic._recording_events = events\n"
        "        except ImportError:\n"
        "            pass"
    )
    f.write_text(txt.replace(target, target + patch, 1))
    print("Bridge added")
EOF
rm -rf "$(dirname "$RECORD")/__pycache__"

# --- 3. recording_randomized_framework.py: streaming encoding ---
python3 - <<'EOF'
import pathlib, os

f = pathlib.Path(os.path.expanduser(
    "~/ws_aic_caai/src/aic/recording_randomized_framework.py"
))
txt = f.read_text()
if "--dataset.streaming_encoding=true" in txt:
    print("Streaming encoding already present — skipping")
else:
    target = '            f"--teleop.task_port_name={config.task_port_name}",'
    patch = (
        '\n            "--dataset.streaming_encoding=true",'
        '\n            "--dataset.encoder_threads=2",'
    )
    updated = txt.replace(target, target + patch, 1)
    if updated == txt:
        print("ERROR: could not find insertion point in recording_randomized_framework.py")
    else:
        f.write_text(updated)
        print("Streaming encoding added")
EOF

# --- 4. Verify ---
echo ""
echo "=== aic_teleop.py ==="
grep "insertion_depth\|spiral_radius" "$TELEOP"

echo ""
echo "=== lerobot_record.py ==="
grep "_recording_events" "$RECORD"

echo ""
echo "=== recording_randomized_framework.py ==="
grep "streaming_encoding\|encoder_threads\|dataset.fps" "$FRAMEWORK"
