#!/usr/bin/env bash
# Self-check for the janest_studio AI game-build stack. See docs/STACK.md.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail=0
ok()   { printf '[ok] %s\n' "$1"; }
bad()  { printf '[!!] %s\n' "$1"; fail=1; }
note() { printf '[--] %s\n' "$1"; }

# 1. Engine
GODOT="${GODOT:-/opt/homebrew/bin/godot}"
if [ -x "$GODOT" ]; then
  v="$("$GODOT" --version 2>/dev/null | head -1)"
  case "$v" in 4.7.2*) ok "Godot $v" ;; *) bad "Godot is $v, expected 4.7.2.stable" ;; esac
else
  bad "Godot CLI not found at $GODOT (brew install --cask godot)"
fi

# 2. Project
[ -f project.godot ] && ok "project.godot present" || bad "project.godot missing"
grep -q 'addons/godot_ai/plugin.cfg' project.godot 2>/dev/null \
  && ok "godot-ai enabled in project.godot" \
  || bad "godot-ai not enabled in project.godot [editor_plugins]"

# 3. Godot AI addon
if [ -f addons/godot_ai/plugin.cfg ]; then
  av="$(sed -n 's/^version="\(.*\)"/\1/p' addons/godot_ai/plugin.cfg)"
  ok "godot-ai addon $av ($(find addons/godot_ai -type f | wc -l | tr -d ' ') files)"
else
  bad "addons/godot_ai missing"
fi

# 4. Bridge — needs uv >= 0.9.25 or the plugin's server launch options are rejected
if command -v uv >/dev/null 2>&1; then
  uvv="$(uv --version 2>/dev/null | awk '{print $2}')"
  if [ "$(printf '%s\n0.9.25\n' "$uvv" | sort -V | head -1)" = "0.9.25" ]; then
    ok "uv $uvv (>= 0.9.25)"
  else
    bad "uv $uvv is too old for godot-ai 4.4.2 (needs >= 0.9.25) — brew upgrade uv"
  fi
else
  bad "uv not found"
fi

if command -v uvx >/dev/null 2>&1; then
  bv="$(uvx --isolated --no-config --no-env-file --no-sources --no-build \
        --index-strategy first-index --keyring-provider disabled \
        --index https://pypi.org/simple --default-index https://pypi.org/simple \
        --find-links https://pypi.org/simple/godot-ai/ --link-mode copy \
        --from godot-ai==4.4.2 godot-ai --version 2>/dev/null | tail -1)"
  [ -n "$bv" ] && ok "godot-ai bridge: $bv" || bad "godot-ai bridge failed to run via uvx"
else
  bad "uvx not found (godot-ai bridge needs uv)"
fi

# 5. Is the editor up? (tools only answer with a live editor)
if pgrep -f "Godot.*--path ${ROOT}" >/dev/null 2>&1; then
  ok "Godot editor is running (MCP tools can answer)"
else
  note "Godot editor not running — start it with tools/godot-editor.sh before MCP calls"
fi

# 6. MCP config
python3 -I - <<'PY'
import json, sys
try:
    s = json.load(open(".mcp.json"))["mcpServers"]
except Exception as e:
    print(f"[!!] .mcp.json unreadable: {e}"); sys.exit(0)
for name in ("godot-ai", "pixel-art"):
    print(f"[{'ok' if name in s else '!!'}] .mcp.json server {name}" + ("" if name in s else " MISSING"))
try:
    en = json.load(open(".claude/settings.json")).get("enabledMcpjsonServers", [])
    miss = [n for n in ("godot-ai", "pixel-art") if n not in en]
    print("[ok] both servers trusted in .claude/settings.json" if not miss
          else f"[!!] not in enabledMcpjsonServers: {miss}")
except Exception as e:
    print(f"[!!] .claude/settings.json: {e}")
PY

# 7. Project skills (pinned in-repo; see docs/SKILLS-PINNED.md)
for s in pixelstrata pixelorama godot-mcp \
         p2p-explore p2p-plan p2p-build p2p-fix p2p-investigate p2p-review p2p-commit \
         p2p-challenge pixel-art-game-style; do
  [ -f ".claude/skills/$s/SKILL.md" ] || bad "pinned skill $s missing"
done
ok "pinned skills: $(find .claude/skills -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
if [ -x tools/skills-diff.sh ]; then
  d="$(./tools/skills-diff.sh 2>/dev/null | grep -c '^\[!!\]' || true)"
  [ "${d:-0}" -eq 0 ] && ok "no skill drift vs user-level" \
    || note "$d pinned skill(s) drifted from user-level (tools/skills-diff.sh)"
fi

# 8. gamedev plugins
if command -v claude >/dev/null 2>&1; then
  for p in router godot; do
    claude plugin details "$p@awesome-gamedev-agent-skills" >/dev/null 2>&1 \
      && ok "plugin $p@awesome-gamedev-agent-skills" \
      || bad "plugin $p@awesome-gamedev-agent-skills not installed"
  done
fi

# 8b. Test harness (TEST_CMD for /p2p-build and /p2p-fix)
if [ -f tests/run_tests.gd ] && [ -x tools/run-tests.sh ]; then
  n="$(./tools/run-tests.sh --list 2>/dev/null | grep -c '\.' || true)"
  if [ "${n:-0}" -gt 0 ]; then ok "test harness: $n tests listed (tools/run-tests.sh)"
  else bad "tools/run-tests.sh --list found no tests"; fi
else
  bad "test harness missing (tests/run_tests.gd + tools/run-tests.sh) — /p2p-build will block"
fi

# 9. Art pipeline
[ -f /Volumes/DATA/personal_project/pixel_art/apps/mcp/src/index.ts ] \
  && ok "pixel-art MCP source present" || bad "pixel-art MCP source not found"
[ -d /Applications/Pixelorama.app ] && ok "Pixelorama installed" || note "Pixelorama not installed"

# 10. Optional keys
[ -n "${ELEVENLABS_API_KEY:-}" ] && ok "ELEVENLABS_API_KEY set" || note "ELEVENLABS_API_KEY unset (audio generation off)"

# 11. PixelStrata doctor
if [ -f .claude/skills/pixelstrata/scripts/doctor.py ]; then
  echo "--- pixelstrata doctor (duplicate-skill warnings are false positives, see CLAUDE.md) ---"
  python3 -I .claude/skills/pixelstrata/scripts/doctor.py 2>&1 | grep -v "installed twice"
fi

echo
[ "$fail" -eq 0 ] && echo "stack OK" || echo "stack has problems (see [!!] above)"
exit "$fail"
