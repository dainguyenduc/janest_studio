# Stack inventory — janest_studio

Installed 2026-11-18. Everything below is version-pinned on purpose; reproduce with the
commands in each section.

## 1. Engine — Godot 4.7.2-stable

| | |
|---|---|
| Version | `4.7.2.stable.official.ed1daf0bf` (released 2026-08-18) |
| App | `/Applications/Godot.app` |
| CLI | `/opt/homebrew/bin/godot` (Homebrew cask symlink) |
| Install | `brew install --cask godot` — the cask is exactly 4.7.2 |

Export templates are **not** installed (1.2 GB). Needed only when exporting builds:
`Godot_v4.7.2-stable_export_templates.tpz` from the
[4.7.2-stable release](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable),
then Editor → Manage Export Templates → Install from file.

## 2. Engine MCP — Godot AI (hi-godot/godot-ai) v4.4.2 · MIT

The main MCP. 46 tools / 120+ operations against a **live editor**.

- Addon: `addons/godot_ai/` — from `godot-ai-v4-plugin.zip`, release `v4.4.2` (2026-11-16).
  sha256 `93b976b68df03352073d36c30b6daa593cdc42322cd10f6dacdec10d049ac9a0`, verified against
  the release's signed `godot-ai-v4-plugin.manifest.json`.
- Enabled in `project.godot` → `[editor_plugins] enabled=PackedStringArray("res://addons/godot_ai/plugin.cfg")`.
- Bridge: `.mcp.json` → server `godot-ai`, a pinned `uvx --from godot-ai==4.4.2 godot-ai attach
  --port 8000 --ws-port 9500` stdio command (the shape the dock's *Run this manually* produces).
  A bare `http://127.0.0.1:8000/mcp` entry cannot authenticate — don't use one.
- Path: MCP client → `godot-ai attach` (stdio) → Python server (HTTP :8000) → editor plugin
  (WebSocket :9500, loopback only). Both hops use rotating capabilities, published by the editor
  into `~/Library/Application Support/godot-ai/capabilities/`.
- **The editor must be running** for any tool to answer: `tools/godot-editor.sh`.
- **uv ≥ 0.9.25 required.** The plugin launches its server with `--exclude-newer-package
  godot-ai=false`, which older uv rejects (`invalid value 'godot-ai=false'`) — the editor then
  loads the plugin but the server never binds :8000. Hit on install with Homebrew's uv 0.9.21;
  fixed with `brew upgrade uv` → **0.13.9**. `uv self update` is a no-op on a Homebrew install.
- Python: the plugin asks for `>=3.11,<3.15`; system python3 is 3.15.1, so `uv` resolves its own
  interpreter. Verified working (`godot-ai 4.4.2`).
- Launch the editor with `open -na` (as `tools/godot-editor.sh` does), not `nohup … &`: a child
  of an agent's shell dies with that shell's process group.
- Diagnostics when `:8000` stays closed:
  `~/Library/Application Support/Godot/app_userdata/Janest Studio/godot_ai_server_startup.json`
  (startup report) and `…/godot_ai_server.pid`. The first start on a machine is slow — uv
  downloads an interpreter plus ~66 packages before binding.
- The plugin added `[autoload] _mcp_game_helper` to `project.godot` and the editor normalized the
  file on first open (settings equal to Godot's defaults are dropped). Both are expected.
- Updating: use the dock's **Update** button (it verifies signatures). Never extract a new
  version over the existing `addons/godot_ai/`. After updating, repin the version in `.mcp.json`
  and here.
- Telemetry is on by default; opt out with `GODOT_AI_DISABLE_TELEMETRY=true`.
- **Verified end to end** 2026-11-18: server bound `127.0.0.1:8000` + `:9500`, capability record
  written to `~/Library/Application Support/godot-ai/capabilities/http-8000.json`, and
  `tools/smoke-mcp.py` got 47 tools plus a live `editor_state` naming `res://scenes/main.tscn`.

## 3. Code skills — awesome-gamedev-agent-skills · Apache-2.0

Installed as Claude Code plugins from the repo's own marketplace, **router + godot only**
(not the 79-skill `gamedev` bundle).

```bash
claude plugin marketplace add gamedev-skills/awesome-gamedev-agent-skills
claude plugin install router@awesome-gamedev-agent-skills
claude plugin install godot@awesome-gamedev-agent-skills
```

- Commit `c6ca6c41c839b68319ffc08430b99ab768debc32`, scope `user`.
- `router` → 1 skill (~150 tok always-on). `godot` → 16 skills (~2.6k tok always-on):
  gdscript, nodes-scenes, signals-groups, 2d-movement, tilemap, physics, ui-control, animation,
  shaders, 3d-essentials, resources, audio, multiplayer, export, csharp, gdscript-headless-testing.
- Engine pin: Godot 4.7 (4.7.2 stable), engines checked 2026-11-11.
- Verify what loads: `claude plugin details godot@awesome-gamedev-agent-skills`.
- Update: `claude plugin marketplace update awesome-gamedev-agent-skills`.

## 4. Game lifecycle + tools — PixelStrata v0.3.0 · Apache-2.0

Tag `v0.3.0`, commit `8abb96d229f93482bcf5128825c1b77d7dfd37d1` (2026-11-02), from
`jasonmello/pixelstrata`. Installed as **project** skills — only the three requested:

```
.claude/skills/pixelstrata/   lifecycle, style-first planning, assets.json manifest
.claude/skills/pixelorama/    pixel-art cleanup, CLI spritesheet export
.claude/skills/godot-mcp/     engine-in-the-loop workflows (tool names overridden → Godot AI)
```

Not installed: `material-maker`, `terrain3d`, `jolt-physics`, `three-quarks` (3D / three.js).
Installing them later = copy the dir from the same tag into `.claude/skills/`.

`doctor.py` is patched to honour `CLAUDE_CONFIG_DIR`; see `CLAUDE.md` → Overrides.
Run it with `python3 -I .claude/skills/pixelstrata/scripts/doctor.py`.

## 5. Art — local pixel-art MCP + pixel-art-game-style skill

- MCP server `pixel-art` in `.mcp.json` → `npx tsx /Volumes/DATA/personal_project/pixel_art/apps/mcp/src/index.ts`
  (the local project at `/Volumes/DATA/personal_project/pixel_art`, same entry as its own `.mcp.json`).
  Verified: `pixel-art-mcp 0.0.0`, 24 `pyxel_*` tools (generate, draw, ingest, flood_fill,
  remove_duplicate_tiles, export_png/sheet, render_png, preview, validate, analyze, batch, …).
- Skill `pixel-art-game-style` is installed user-level in `~/.claude-account3/skills/`.
- This replaces PixelLab in the PixelStrata flow — see `CLAUDE.md` → Overrides.

## 6. Pixel editor — Pixelorama 1.2.4 · MIT

- `/Applications/Pixelorama.app`, from `Pixelorama-Mac.dmg` of release `v1.2.4` (2026-11-03),
  sha256 `aef909572cb008174e758fbc36998823363e44d9eaffa974b156d4284c549ce7`.
- Installed by hand because the Homebrew cask was **disabled on 2026-09-01** (fails the macOS
  Gatekeeper check). The app is unsigned, so the quarantine flag was cleared
  (`xattr -dr com.apple.quarantine /Applications/Pixelorama.app`). macOS may still ask on first
  launch → right-click → Open, once.
- CLI: `/Applications/Pixelorama.app/Contents/MacOS/Pixelorama --headless --export ...`

## 7. Delivery skills (pre-existing, user-level)

`p2p-explore`, `p2p-plan`, `p2p-build`, `p2p-fix`, `p2p-investigate`, `p2p-review`,
`p2p-commit`, `p2p-challenge` in `~/.claude-account3/skills/`. Untouched by this install.

## Claude Code config

This machine runs with `CLAUDE_CONFIG_DIR=/Users/toptop/.claude-account3`, **not** `~/.claude`.
Anything that hardcodes `~/.claude` (PixelStrata's `doctor.py`, some upstream install scripts)
needs the override.

Project-local config:

- `.mcp.json` — `godot-ai`, `pixel-art`
- `.claude/settings.json` — `enabledMcpjsonServers` so both are trusted without a prompt
- `.claude/skills/` — the three PixelStrata skills

## Not installed (deliberate)

| Thing | Why | How to add |
|---|---|---|
| Coding-Solo `godot-mcp` | Godot AI is the main MCP and covers it; it would be a second overlapping server. Its one real advantage: headless runs with no editor open | `claude mcp add godot -e GODOT_PATH=/opt/homebrew/bin/godot -- npx @coding-solo/godot-mcp` |
| PixelLab MCP | Paid credits; local `pixel-art` MCP does the art | per `pixelstrata/references/pixellab.md` |
| ElevenLabs | No API key | `export ELEVENLABS_API_KEY=...` |
| Godot export templates | 1.2 GB, only needed to ship builds | see §1 |
| `gamedev` 79-skill bundle | Only Godot is in scope | `claude plugin install gamedev@awesome-gamedev-agent-skills` |

## Sources

- <https://github.com/gamedev-skills/awesome-gamedev-agent-skills>
- <https://github.com/jasonmello/pixelstrata/releases/tag/v0.3.0>
- <https://github.com/hi-godot/godot-ai>
- <https://godotengine.org/download/archive/4.7.2-stable/>
- <https://github.com/Orama-Interactive/Pixelorama>
