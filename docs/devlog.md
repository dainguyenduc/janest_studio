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

## 2026-11-18 — Phase 0b: GDScript test harness (unblocks /p2p-build and /p2p-fix)

The p2p delivery skills turned out to be only half usable here. `/p2p-plan`, `/p2p-explore`,
`/p2p-commit`, `/p2p-review` and `/p2p-investigate` are stack-agnostic and fine. But
`/p2p-build`'s Foundation Gate refuses to enter the TDD loop unless `TEST_CMD` resolves from a
project marker, and its table has no Godot/GDScript row — so the two skills that actually write
and fix code would have reported BLOCKED on every story. `/p2p-fix` reads the same table.

Fixed by giving the project a real runner rather than by loosening the gate:

- `tests/run_tests.gd` — headless runner over `res://tests/test_*.gd`, driving the Godot AI
  addon's own `McpTestRunner`. Suites are `McpTestSuite` subclasses, so **the same file runs
  headless and through `mcp__godot-ai__test_run`** in the editor. One suite, two ways to run it.
- `tools/run-tests.sh` — the `TEST_CMD` wrapper: `-t <pattern>`, `--suite <name>`, `--list`.
- `tests/test_project_setup.gd` — 6 tests pinning the pixel-art rendering contract, so a silent
  change to base resolution, stretch mode, texture filter or pixel snap fails here instead of
  showing up as mush in a screenshot three phases later.

Deliberately checked the red paths, since a test harness that can only go green is worthless:
a failing assert exits 1 and names `<suite>.<test>`, and a filter matching 0 tests exits 1
instead of reporting a false green — the exact trap `/p2p-build` warns about.

`CLAUDE.md` → Test Command declares the commands so the skills skip auto-detection.
`mcp__graphatlas__*`, which both skills prefer for symbol lookup and blast radius, is not
configured; their grep fallback applies.

## 2026-11-18 — Phase 0c: skills pinned in-repo; graphatlas does not exist

**Skills pinned.** The 8 `p2p-*` skills and `pixel-art-game-style` are copied from
`~/.claude-account3/skills/` into `.claude/skills/`, joining the three vendored from PixelStrata
— 12 pinned skills, 516K. The repo copy is what runs, so editing the user-level skills no longer
changes this project's pipeline. The source dir is not a git repo and the skills carry no version
field, so they are pinned by content hash in `docs/SKILLS-PINNED.md`.
`tools/skills-diff.sh` reports drift against user-level and `--pull <skill>` adopts a change
deliberately; nothing syncs on its own. Verified in all three modes, including the drift path
(temporarily edited a pinned copy → reported DRIFTED → restored → clean).

**graphatlas: nothing to install.** `p2p-build`, `p2p-fix` and `p2p-explore` probe for
`mcp__graphatlas__*` and reference 10 `ga_*` tools (architecture, symbols, callers, callees,
impact, importers, hubs, risk, file_summary, reindex). Checked: not on npm, not on PyPI, no such
GitHub project, and not configured in either Claude config dir. It is an interface the skills
were written against, not a shipped server. No action needed — their Phase 0a probe already
degrades to grep + `git log`, which is the documented fallback.

Substituting a real code-graph MCP server was considered and rejected: CodeGraph,
code-graph-mcp, grapha and codegraph-mcp were all checked and **none supports GDScript**, so the
index would be blind to this project's code. `scene_get_hierarchy` / `node_get_properties` from
Godot AI serve the same purpose for scene structure and are already in CLAUDE.md. Worth
revisiting only if a GDScript-aware code graph appears or this project grows a C# surface.
