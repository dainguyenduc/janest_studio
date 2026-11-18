#!/usr/bin/env bash
# Open the Godot editor for this project. Required before any mcp__godot-ai__* call:
# Godot AI talks to the live editor over a loopback WebSocket, it is not headless.
#
# Uses `open -na` on macOS so the editor is owned by launchd, not by this shell — a
# nohup'd child dies with the calling shell's process group when run from an agent task.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GODOT_APP="${GODOT_APP:-/Applications/Godot.app}"
GODOT="${GODOT:-/opt/homebrew/bin/godot}"

if pgrep -f "Godot.*--path ${ROOT}" >/dev/null 2>&1; then
  echo "Editor already running for ${ROOT}"
  exit 0
fi

echo "Launching Godot editor: ${ROOT}"
if [ "$(uname)" = "Darwin" ] && [ -d "$GODOT_APP" ]; then
  open -na "$GODOT_APP" --args -e --path "$ROOT"
else
  setsid "$GODOT" -e --path "$ROOT" >/dev/null 2>&1 < /dev/null &
fi

# Godot AI starts its Python server through uvx. The first run on a machine also downloads an
# interpreter and ~66 packages, so allow a few minutes; later runs take seconds.
WAIT="${WAIT:-300}"
for _ in $(seq 1 "$WAIT"); do
  if lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1 \
     && lsof -nP -iTCP:9500 -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Godot AI up: HTTP :8000, editor socket :9500 — MCP tools can answer."
    exit 0
  fi
  sleep 1
done

echo "Editor launched, but Godot AI did not open :8000/:9500 within ${WAIT}s." >&2
echo "Check the startup report:" >&2
echo "  ~/Library/Application Support/Godot/app_userdata/Janest Studio/godot_ai_server_startup.json" >&2
echo "and the Godot AI dock's server row. See docs/STACK.md §2." >&2
exit 1
