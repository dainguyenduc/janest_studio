#!/usr/bin/env bash
# TEST_CMD for this project — headless GDScript suites, no editor needed.
#
#   tools/run-tests.sh                  run everything
#   tools/run-tests.sh -t "<pattern>"   run tests whose method name contains <pattern>
#   tools/run-tests.sh --suite <name>   run one suite
#   tools/run-tests.sh --list           list "<suite>.<test>" (filter verification)
#
# Exit 0 = green. Exit 1 = a failure, a load error, or a filter that matched
# nothing (0 matches is never a pass).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GODOT="${GODOT:-/opt/homebrew/bin/godot}"

if [ ! -x "$GODOT" ]; then
  echo "Godot not found at $GODOT (brew install --cask godot)" >&2
  exit 1
fi

# Strip Godot's progress/verbose chatter, keep the runner's own output.
"$GODOT" --headless --path "$ROOT" --script res://tests/run_tests.gd -- "$@" 2>&1 \
  | grep -vE '^\[[ 0-9]+%\]|^\[ DONE \]|^Godot Engine v|^Metal |^ *$|^MCP \||^\[godot_ai '
exit "${PIPESTATUS[0]}"
