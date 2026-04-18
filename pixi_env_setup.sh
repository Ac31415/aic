#!/usr/bin/bash
set -e

export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE="${ZENOH_CONFIG_OVERRIDE:-transport/shared_memory/enabled=false}"

# On macOS, ROS setup scripts can prepend .pixi env libs to DYLD_LIBRARY_PATH.
# That can make PyAV load duplicate FFmpeg dylibs (objc AVF* duplicate-class warnings).
# Keep this as a function so users can re-run it after sourcing install/setup.zsh.
aic_fix_macos_dyld_library_path() {
	if [[ "$(uname -s)" != "Darwin" ]]; then
		return 0
	fi

	local bad='/.pixi/envs/default/lib'
	local current="${DYLD_LIBRARY_PATH:-}"
	local cleaned
	cleaned="$(python - <<'PY'
import os

bad = '/.pixi/envs/default/lib'
parts = [p for p in os.environ.get('DYLD_LIBRARY_PATH', '').split(':') if p and bad not in p]
print(':'.join(parts))
PY
)"

	export DYLD_LIBRARY_PATH="$cleaned"
	if [[ "$current" != "$cleaned" ]]; then
		echo "[aic] macOS DYLD_LIBRARY_PATH sanitized for LeRobot/PyAV compatibility"
	fi
}

aic_fix_macos_dyld_library_path
