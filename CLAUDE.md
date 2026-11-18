# Janest Studio — AI-driven pixel-art game

Pixel-art game built end-to-end by agents. Engine: **Godot 4.7.2-stable**.
Stack inventory and version pins: `docs/STACK.md`.

## How to work on this game

- **Entry point:** start every game request with the `pixelstrata` skill. It plans first (plan
  mode), asks for the visual style before anything else, picks mechanics from Gameplay Atlas,
  and hands code off to the `gamedev` router.
- **Current phase:** 0 Setup (stack installed, no game design yet)
- **Read first:** `docs/gdd.md` (design), `assets.json` (style + asset manifest),
  `docs/devlog.md` (decisions). Don't re-ask anything these files already answer.
  None of the three exist yet — `/pixelstrata` creates them in the planning step.

## Locked decisions

- Engine: **Godot 4.7.2** (pinned; `/opt/homebrew/bin/godot`) · 2D pixel-art first
- Base resolution **384×216**, window 1152×648 (3×), `stretch/mode=viewport`, nearest-neighbour
  texture filter, 2D pixel snap on, file logging on — in `project.godot`. `aspect=keep` and
  `msaa_2d=0` are Godot's defaults, so the editor strips them from the file; they still apply.
  Do not change any of this without a line in `docs/devlog.md`.
- `[autoload] _mcp_game_helper` is added and owned by the Godot AI plugin. Leave it alone.
- Visual style: **not chosen yet** — `/pixelstrata` must ask before generating any art.
- Core mechanics (Gameplay Atlas): not chosen yet.
- Art pipeline: **local `pixel-art` MCP + `pixel-art-game-style` skill** (not PixelLab —
  see Overrides). Cleanup / spritesheet export: `pixelorama`.
- Audio: ElevenLabs via the `pixelstrata` skill, **disabled until `ELEVENLABS_API_KEY` is set**.
- Engine-in-the-loop: **Godot AI MCP** (`mcp__godot-ai__*`), not Coding-Solo godot-mcp
  (see Overrides).

## Skills are pinned in this repo

Every skill the pipeline depends on lives in `.claude/skills/` and the repo copy is what runs —
the `p2p-*` set and `pixel-art-game-style` snapshotted from `~/.claude-account3/skills/`, plus
the three vendored from PixelStrata. Editing the user-level copies does **not** change this
project. Inventory + hashes: `docs/SKILLS-PINNED.md`. Drift check: `tools/skills-diff.sh`
(`--pull <skill>` to adopt a user-level change deliberately). When a pipeline skill needs a
change for this project, edit the repo copy and commit it.

## Pipeline (who does what)

| Stage | Use |
|-------|-----|
| 1. Discovery | `/p2p-explore` for vague ideas → concrete requirements |
| 2. Spec | `/p2p-plan` → `docs/specs/<feature>/<feature>.md` (Given/When/Then) |
| 3. Game plan | `/pixelstrata` → visual style, mechanics, lifecycle phase, `assets.json`, `docs/gdd.md` |
| 4. Art | `pixel-art-game-style` skill + `mcp__pixel-art__pyxel_*` (24 tools: `pyxel_generate`, `pyxel_draw`, `pyxel_export_sheet`, `pyxel_validate`, …) → `assets/sprites`, `assets/tilesets`; hand-fix / export with `pixelorama` |
| 5. Code | `gamedev` router → the right `godot-*` skill; implement with `/p2p-build` (TDD, story by story) |
| 6. Verify | Godot AI MCP: `project_run` → `logs_read` → `project_manage(op="stop")`. Also `test_run` for GDScript suites in `tests/` |
| 7. Bugs | `/p2p-investigate` (hard ones) → `/p2p-fix` (test-first) |
| 8. Commit | `/p2p-commit`, one feature per commit |

## Commands

- **Run the editor** (required before any `mcp__godot-ai__*` call): `tools/godot-editor.sh`
  or `godot -e --path .`
- **Run the game (agent):** `mcp__godot-ai__project_run` → `mcp__godot-ai__logs_read`
- **Run the game (CLI):** `godot --path . ` · headless: `godot --headless --path .`
- **Tests:** `tools/run-tests.sh` (headless, no editor) or `mcp__godot-ai__test_run` (live editor)
- **Reimport assets:** `godot --headless --import --path .`
- **Stack self-check:** `tools/verify-stack.sh`
- **MCP chain check:** `python3 -I tools/smoke-mcp.py` (editor must be running)
- **Pixelorama CLI:** `/Applications/Pixelorama.app/Contents/MacOS/Pixelorama --headless ...`

## Test Command (for `/p2p-build`, `/p2p-fix` and anything else that needs `TEST_CMD`)

The p2p skills auto-detect `TEST_CMD` from project markers and their table has **no Godot /
GDScript row** — without this section their Foundation Gate reports BLOCKED. This project's
marker is `project.godot` + `tests/run_tests.gd`. Use these commands and skip the auto-detect:

| | Command |
|---|---|
| `TEST_CMD` (run all) | `tools/run-tests.sh` |
| Run filtered | `tools/run-tests.sh -t "<pattern>"` (matches the `test_*` method name) |
| Run one suite | `tools/run-tests.sh --suite <suite_name>` |
| **Filter verification** (mandatory before trusting a filtered run) | `tools/run-tests.sh --list -t "<pattern>"` — prints `<suite>.<test>` per match and **exits 1 on 0 matches** |
| `E2E_CMD` | none. A gameplay flow is verified in-engine instead: `mcp__godot-ai__project_run` → `logs_read` → `editor_screenshot`. Report that as the E2E evidence; don't downgrade it to a mocked unit test |

Harness properties, verified: green → exit 0; one failing assert → exit 1 with the failing
`<suite>.<test>` named; a filter matching nothing → exit 1 (never a false green).

**Writing a test:** `tests/test_<thing>.gd`, `@tool extends McpTestSuite`, a `suite_name()`, and
`test_*` methods using `assert_eq` / `assert_true` / `assert_ne` / `assert_gt` /
`assert_contains` / `assert_has_key` / `skip()` / `track()` (frees nodes after the test). Top
level of `tests/` only — subdirectories are not scanned. Test methods must be synchronous: the
runner does not await coroutines. The same file runs headless **and** through
`mcp__godot-ai__test_run` in the editor, so write each suite once.

## Overrides (read before following a vendored skill verbatim)

These three skills come from PixelStrata v0.3.0 unmodified; this project's stack differs from
their defaults. The override wins.

**1. `godot-mcp` skill → use Godot AI instead.** The skill documents Coding-Solo's
`mcp__godot__*` server. That server is **not installed**. The installed engine MCP is
Godot AI (`mcp__godot-ai__*`). Follow the skill's *workflows*, but translate the tools:

| `godot-mcp` skill says | Use instead |
|---|---|
| `get_godot_version`, `get_project_info` | `editor_state` |
| `launch_editor` | `tools/godot-editor.sh` (the editor must already run) |
| `run_project` | `project_run` |
| `get_debug_output` | `logs_read` (`source="game"` / `"editor"` / `"combined"`) |
| `stop_project` | `project_manage(op="stop")` |
| `create_scene`, `save_scene` | `scene_manage`, `scene_open` |
| `add_node` | `node_create`, `node_manage` |
| `load_sprite` | `node_manage` (set `texture`) / `resource_manage` |
| `export_mesh_library` | `gridmap_manage` |
| `get_uid`, `update_project_uids` | `filesystem_manage` |
| — (no equivalent) | `editor_screenshot`, `test_run`, `signal_manage`, `tilemap_manage`, `tileset_manage`, `animation_create`, `input_map_manage`, `autoload_manage` |

Godot AI needs the **editor open** with the plugin enabled; it is not headless. For unattended
runs without the editor, fall back to the CLI (`godot --headless`) and the
`godot-gdscript-headless-testing` skill.

**2. `pixelstrata` skill → art comes from the local `pixel-art` MCP, not PixelLab.**
PixelLab (`mcp__pixellab__*`) is not configured and costs credits. Generate sprites, tilesets and
animations through `mcp__pixel-art__*` plus the `pixel-art-game-style` skill, then record every
file in `assets.json` exactly as the skill's manifest reference requires. Keep the manifest
rule: nothing is generated outside `assets.json`. If the user later adds a PixelLab key, the
skill's own path applies again.

**3. p2p skills: two gaps, both handled.** `/p2p-plan`, `/p2p-explore`, `/p2p-commit`,
`/p2p-review`, `/p2p-investigate` are stack-agnostic and work here as-is. The other two need
this project's answers:

- `/p2p-build` and `/p2p-fix` resolve `TEST_CMD` from a marker table with no Godot row — use the
  **Test Command** section above instead of auto-detecting, or the Foundation Gate blocks.
- Both probe for a `mcp__graphatlas__*` code-graph server (10 `ga_*` tools). **That server does
  not exist** — not on npm, not on PyPI, not on GitHub, not configured anywhere. Don't try to
  install it and don't wait on it: the skills' own Phase 0a probe fails `ga_architecture` → GA
  unavailable → grep + `git log` fallback, which is the supported path. For scene/node structure
  use `mcp__godot-ai__scene_get_hierarchy` and `node_get_properties` rather than grepping
  `.tscn` text — that is this project's substitute for a code graph. Details and the rejected
  alternatives: `docs/SKILLS-PINNED.md`.

**4. `pixelstrata` doctor is patched.** `.claude/skills/pixelstrata/scripts/doctor.py` honours
`CLAUDE_CONFIG_DIR` (upstream hardcodes `~/.claude`; this machine uses `~/.claude-account3`).
Original kept as `doctor.py.orig`. Its `installed twice` warnings are false positives — it
scans every `SKILL.md` on disk, including the marketplace clone; only `router` + 16 `godot-*`
skills actually load.

## Rules

- Never change `project.godot` display/rendering settings without a line in `docs/devlog.md`.
- Never call a change done from code inspection alone: run it, read the log, then report.
- Every generated asset is listed in `assets.json`; nothing is generated outside it.
- One feature per commit; update `docs/devlog.md` at the end of each milestone.
- `addons/godot_ai/` is vendored third-party code — never hand-edit it. Update it from the
  Godot AI dock's **Update** button, then repin the version in `.mcp.json` and `docs/STACK.md`.
- Specs are only written by `/p2p-plan`. Code never edits a spec.
