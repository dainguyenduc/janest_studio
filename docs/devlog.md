# Devlog

## 2026-11-18 — Phase 0: AI build stack installed

The whole toolchain for building this game with agents is in place and self-checks green
(`tools/verify-stack.sh`). Inventory and version pins: `docs/STACK.md`.

- Godot **4.7.2-stable** via Homebrew cask (`/opt/homebrew/bin/godot`).
- Godot project scaffolded: 384×216 base resolution, viewport stretch, nearest filtering,
  2D pixel snap. Headless import clean, addon GDScript compiles with no errors.
- **Godot AI v4.4.2** (hi-godot) vendored into `addons/godot_ai/`, enabled in `project.godot`,
  bridged in `.mcp.json` with a version-pinned `uvx … godot-ai attach` stdio command. This is
  the main MCP for engine-in-the-loop work.
- **awesome-gamedev-agent-skills** (Apache-2.0, commit `c6ca6c41`, engines checked 2026-11-11):
  only the `router` + `godot` plugins (1 + 16 skills), not the 79-skill bundle.
- **PixelStrata v0.3.0** (tag `v0.3.0`, 2026-11-02): only `pixelstrata`, `pixelorama`,
  `godot-mcp`, installed as project skills in `.claude/skills/`.
- Art pipeline wired to the local **pixel-art MCP** + `pixel-art-game-style` skill instead of
  PixelLab. **Pixelorama 1.2.4** installed for hand-fixes and CLI spritesheet export.

Verified end to end, not just installed: the Godot AI server binds :8000/:9500 against the live
editor and `tools/smoke-mcp.py` gets 47 tools plus a real `editor_state` response. The local
pixel-art MCP answers with its 24 `pyxel_*` tools.

One real blocker found and fixed on the way: Homebrew's **uv 0.9.21 was too old** for Godot AI
4.4.2 — the plugin loads but its server launch options are rejected, so :8000 never opens and the
MCP looks dead with no obvious cause. `brew upgrade uv` → 0.13.9. `tools/verify-stack.sh` now
checks the uv version so this can't bite silently again.

Two deviations from the vendored skills, both recorded in `CLAUDE.md` → Overrides:

1. The `godot-mcp` skill's `mcp__godot__*` tools don't exist here; a mapping table sends them to
   the equivalent `mcp__godot-ai__*` tools.
2. `pixelstrata/scripts/doctor.py` was patched to honour `CLAUDE_CONFIG_DIR`, because this
   machine runs on `~/.claude-account3` and upstream hardcodes `~/.claude`.

No game design yet — visual style and mechanics are still open. Next step is `/pixelstrata`,
which must ask for the visual style before generating anything.
