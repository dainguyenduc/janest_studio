---
name: pixelstrata
description: >
  Entry point for making a game with Claude Code end to end. Start here for any new game,
  prototype, jam entry, vertical slice or asset batch; it plans first in plan mode, asks the visual
  style first, picks mechanics from Gameplay Atlas, then calls the gamedev router for code. Owns
  asset generation and the build lifecycle: pixel art via the PixelLab MCP server, SFX, music and
  voice via ElevenLabs, an assets.json manifest, engine import and run checks via godot-mcp, and
  the companion tool skills pixelorama, material-maker, terrain3d, jolt-physics, three-quarks and
  godot-mcp. Use when the user wants to make or continue a game, or asks for sprites, walk
  cycles, tilesets, pixel-art UI, VFX, sound effects, music or voice lines for a game. For a pure
  code question in an existing project, the gamedev router alone is enough.
---

# PixelStrata — plan, code, art and audio in one pipeline

PixelStrata sits **above** the other game skills and decides which to use, in which order, and
how their outputs connect.

| Layer | Provider | Owns |
|-------|----------|------|
| Lifecycle & planning | this skill | phases, gates, plan mode, style lock, manifest |
| Code & design | `gamedev` router, named `router` in some installs (dependency: [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills)) | engine detection, gameplay code, genres, disciplines, shipping |
| Pixel art generation | PixelLab MCP (`mcp__pixellab__*`) | characters, animations, tilesets, props, UI, VFX sheets |
| Pixel art editing | `pixelorama` | hand clean-up, palettes, CLI spritesheet export |
| Audio generation | ElevenLabs (`scripts/elevenlabs_gen.py`) | SFX, music, voice lines |
| 3D world | `material-maker`, `terrain3d`, `jolt-physics` | procedural materials, terrain, 3D physics |
| Web VFX | `three-quarks` | particles for three.js |
| Engine loop | `godot-mcp` (`mcp__godot__*`) | run, read errors, scenes, sprite import |

**Ownership on overlap:** `create-game-assets` owns art direction and style bibles; PixelStrata owns
*generating* the assets. `audio-design` owns mixing, buses and adaptive music in the engine; PixelStrata
owns *generating* the audio. Engine skills own APIs. Load the owner, not both, when a step belongs
to one of them.

The glue is **`assets.json`** at the game's root: every asset, its prompt, provider id, file path
and the gameplay event that uses it. Nothing is generated that isn't in the manifest.

## 0. Kickoff — always plan first, always ask the visual style first

Every PixelStrata session starts here. Planning before generating avoids paying in tokens and credits
for assets in the wrong style.

1. **Enter plan mode.** In Claude Code call `EnterPlanMode` (or ask the user to press Shift+Tab).
   In plan mode only read, research and ask. No files are written, no PixelLab or ElevenLabs jobs
   run. In clients without plan mode, follow the same rule until the user approves the plan.
2. **First question: the visual style.** Before anything else, ask which graphic look the game
   should have, using `references/visual-styles.md` (≤4 options picked for the idea, one marked
   Recommended). Then ask only the details that style needs: palette, sprite/tile size, camera,
   a reference game.
3. **Then the mechanics.** Use [Gameplay Atlas](https://gameplayatlas.loopyhop.com/) to choose
   2–3 core mechanics (`references/gameplay-atlas.md`). Ask the engine only if the project
   doesn't already decide it.
4. **Write the plan** and present it with `ExitPlanMode`: style brief, mechanics with Atlas links,
   engine and tool stack (`references/claude-code-workflow.md` → stack table), the skills to load,
   slice scope and cut list, asset manifest draft, estimated PixelLab generations and ElevenLabs
   characters, milestones.
5. Only after approval: preflight (§0.1), then follow the lifecycle.

**Existing project:** read `CLAUDE.md`, `docs/gdd.md`, `assets.json` and `docs/devlog.md` first.
If `style.visual` is set, don't ask again; plan only the new work. Still plan first for anything
that generates assets or touches several systems. A pure code fix may skip plan mode and go
straight to the router.

## 0.1 Preflight (after the plan is approved)

```bash
python3 <skill-dir>/scripts/doctor.py
```

It checks the `gamedev` router is installed, `ELEVENLABS_API_KEY` is set, no skill is installed
twice, and `assets.json` is valid. Check the MCP tools yourself: no `mcp__pixellab__*` → no art
generation; no `mcp__godot__*` → run Godot from the shell instead. Tell the user what is missing
(`references/setup.md`) and continue with what works. Call `mcp__pixellab__get_balance` before a
large batch.

## 1. Lifecycle

Follow `references/claude-code-workflow.md`: **0 Setup → 1 Concept → 2 Prototype → 3 Vertical
slice → 4 Production → 5 Polish → 6 Ship**, each with a gate the user passes. Short version:

- **Setup:** doctor, git, copy `assets/CLAUDE.template.md` to the game root as `CLAUDE.md`.
- **Concept:** §0 above. Writes `docs/gdd.md`, `assets.json`, `CLAUDE.md` after approval.
- **Prototype:** greybox, no paid assets, prove the core loop is fun.
- **Vertical slice:** anchor asset → batch → import → one complete level.
- **Production:** feature loop of plan → implement → generate → run and verify → commit.
- **Polish and Ship:** feel, mix, performance, export, itch/Steam.

## 2. Classify each request inside a phase

| Request looks like | Route |
|--------------------|-------|
| gameplay, engine API, bug, physics code, UI code, saving, AI, shipping | **Code** → `gamedev` router, follow it |
| sprite, character, walk cycle, tileset, prop, icon, HUD art, VFX sheet | **Art** → §3 + `references/pixellab.md` |
| fix or redraw generated pixel art, spritesheet export | `pixelorama` |
| sound effect, music, ambience, voice | **Audio** → §4 + `references/elevenlabs.md` |
| 3D material or texture | `material-maker` |
| terrain, landscape, heightmap, foliage (Godot) | `terrain3d` |
| 3D physics engine choice or Jolt behaviour | `jolt-physics` (+ `godot-physics`) |
| particles in three.js / R3F | `three-quarks` |
| run the game, read errors, import into scenes (Godot) | `godot-mcp` |
| publish | router → `itch-publish` / `steam-publish` |

Mixed requests ("add a dash with a whoosh and a dash animation") run code, then art, then audio,
then wire them together (§5).

## 3. Art with PixelLab — the short rules

Full tool map, costs and gotchas: `references/pixellab.md`.

- **Characters:** `create_character` (default `mode="v3"`). Same `view` for every character and
  tileset. Animate with a **template id** first (`walking-6-frames`, `breathing-idle`,
  `taking-punch`, `falling-back-death`); use v3 `action_description` only when no template fits.
- **Tilesets:** top-down `create_topdown_tileset` (chain with `lower_base_tile_id`); platformer
  `create_sidescroller_tileset`; isometric `create_isometric_tile`.
- **Props:** `create_map_object` or `create_8_direction_object`. **UI:** `create_ui_asset` with
  the palette. **Effects:** `vfx_workbench`. **Exact pixel edits:** `pixelart_workbench`, or
  `pixelorama` for hand work.
- Async: queue → `wait_for_jobs` → `get_*` → download to the manifest path. Never re-queue a job
  that is still processing.

## 4. Audio with ElevenLabs — the short rules

Full guide and loudness targets: `references/elevenlabs.md`.

```bash
python3 <skill-dir>/scripts/elevenlabs_gen.py sfx   "short 8-bit coin pickup, bright" -o audio/sfx/coin.mp3 --duration 0.6
python3 <skill-dir>/scripts/elevenlabs_gen.py music "chiptune dungeon loop, 110 bpm, tense" -o audio/music/dungeon.mp3 --length 60 --instrumental
python3 <skill-dir>/scripts/elevenlabs_gen.py tts   "You shouldn't be here." -o audio/vo/guard_01.mp3 --voice <voice_id>
python3 <skill-dir>/scripts/elevenlabs_gen.py manifest assets.json   # every pending audio entry
```

Describe the **sound**, not the event. Use one voice id per character, stored in the manifest.
An ElevenLabs MCP server may be used instead if connected; the manifest stays the source of truth.

## 5. Import, wire, verify

Engine skill from the router + `references/engine-import.md`: nearest filtering for pixel art,
slicing by the frame size PixelLab reports, tileset terrains, audio buses and loop flags. In Godot
use `godot-mcp` to create scenes, load sprites, then `run_project` → `get_debug_output`. Wire
SFX to the manifest's `trigger` events. A change is done when the game ran and the errors were read.

## 6. Rules

- **Plan before spending:** plan mode for new work. State the estimated PixelLab generations and
  ElevenLabs characters for any batch over ~5 assets and wait for a yes.
- **Consistency over novelty:** one view, palette, outline and sprite scale per game; the anchor
  asset drives the rest.
- **Files are the memory:** keep `assets.json`, `docs/gdd.md`, `docs/devlog.md` and `CLAUDE.md`
  current, and read them instead of re-asking.
- **Load only what the step needs:** never bulk-load skills; the router's progressive disclosure
  applies here too.
- **Licensing:** generated assets follow the PixelLab and ElevenLabs terms of the user's plan.
  Remind the user before a commercial release.

## References

- `references/claude-code-workflow.md`: lifecycle phases, gates, project memory files, stack by style.
- `references/visual-styles.md`: the style catalog for the first question and what each locks.
- `references/gameplay-atlas.md`: using Gameplay Atlas to pick and describe core mechanics.
- `references/pixellab.md`: tool selection, cost ladder, animation templates, gotchas.
- `references/elevenlabs.md`: SFX, music and voice prompting, formats, loudness.
- `references/asset-manifest.md`: `assets.json` schema and an example.
- `references/engine-import.md`: import checklists for Godot, Unity, Phaser and others.
- `references/setup.md`: installing the router, MCP servers and keys.
- `assets/CLAUDE.template.md`: per-game `CLAUDE.md` template.
