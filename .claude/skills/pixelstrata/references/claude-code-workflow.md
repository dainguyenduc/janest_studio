# Building a game with Claude Code — the PixelStrata lifecycle

A game is built in **phases with gates**. Each phase has a goal, the skills and tools it loads, the
files it leaves behind, and a gate the user must pass before the next phase. Plan mode guards
every phase start; files on disk carry the state between sessions, so the conversation can be
cleared without losing anything.

```
 0 Setup ─► 1 Concept ─► 2 Prototype ─► 3 Vertical slice ─► 4 Production ─► 5 Polish ─► 6 Ship
   doctor     PLAN MODE    greybox,        first real art      feature loop    feel, mix,    export,
   CLAUDE.md  style+Atlas  no paid assets  + audio, one level  (repeat)        perf, a11y    itch/Steam
       gate:  plan OK      "is it fun?"    slice approved      milestone done  checklist     live build
```

## Project memory (create in phase 0, keep current)

| File | Holds | Updated |
|------|-------|---------|
| `CLAUDE.md` | rules for every session: entry point, engine, style key, commands to run/test | phase 0, when a rule changes |
| `docs/gdd.md` | one-page design: pitch, pillars, Atlas mechanics, core loop, scope cut list | phase 1, on design changes |
| `assets.json` | style lock, mechanics slugs, every asset and its status | every generation |
| `docs/devlog.md` | dated decisions and what changed per milestone (short lines) | end of each phase/milestone |

Template: `assets/CLAUDE.template.md` (copy to the game root and fill in).

**Token economy:** read these four files at session start instead of re-deriving context; load
only the skills the current step needs (router §4 "progressive disclosure"); run `/clear` between
phases. The files are the memory. Prefer `wait_for_jobs` over polling, the CLI exporters
(Material Maker, Pixelorama, ElevenLabs script) over GUI back-and-forth, and subagents for broad
research or large asset batches so their output stays out of the main context.

## Phase 0 — Setup

- `doctor.py`: router, keys, MCP servers, duplicate installs.
- `git init` if needed, `.gitignore` for the engine (Godot: `.godot/`, `*.import` is kept),
  copy `CLAUDE.template.md` → `CLAUDE.md`.
- Godot projects: confirm `mcp__godot__get_godot_version`. Godot is the default engine for a new
  project when the user has no preference (router §6).
- **Gate:** doctor green or each gap stated (e.g. "no ElevenLabs key: audio skipped").

## Phase 1 — Concept (plan mode, nothing written)

1. Visual style first (`visual-styles.md`).
2. 2–3 core mechanics from Gameplay Atlas (`gameplay-atlas.md`). Genre skill via the router.
3. Engine and tool stack from the style (table below).
4. Scope: what the vertical slice contains, and an explicit cut list.
5. Present with `ExitPlanMode`: style brief, mechanics with links, stack, slice scope, manifest
   draft, credit estimate, milestones.
- **Gate:** the user approves the plan. Then write `docs/gdd.md`, `assets.json` and `CLAUDE.md`.

## Phase 2 — Prototype (greybox, free)

- `prototype-fast` + engine skill + genre skill. Coloured boxes and placeholder beeps only: **no
  PixelLab or ElevenLabs credits yet.**
- Build only the core loop. Verify by running: `run_project` → `get_debug_output` (godot-mcp), or
  the engine's own run command.
- **Gate:** the user plays it and answers "is it fun?" Keep → phase 3. Kill or pivot → back to
  phase 1 with what was learned in `devlog.md`.

## Phase 3 — Vertical slice (first real assets)

1. Anchor asset first (the player character), approved by the user.
2. Batch the slice's assets (subagent or parallel PixelLab jobs + ElevenLabs script), then
   clean-ups in `pixelorama` if needed.
3. 3D styles: `material-maker` materials, `terrain3d` ground, `jolt-physics` settings.
4. Import (`engine-import.md`, `godot-mcp`), wire SFX to manifest `trigger`s, one complete level.
- **Gate:** a playable slice that looks and sounds like the final game, screenshot + short
  capture shown to the user.

## Phase 4 — Production (the feature loop, repeated)

For each feature or content batch from the milestone list:

1. **Plan** (plan mode for anything touching more than one system or spending credits).
2. **Implement** with the minimal skills (router).
3. **Generate** any assets it needs (manifest first).
4. **Verify**: run the game, read errors; headless tests where they exist
   (`godot-gdscript-headless-testing`).
5. **Commit** one feature per commit; note decisions in `devlog.md`.

Independent features can run in parallel in separate git worktrees or sessions, one writer per set
of files. Review a milestone's diff with `/code-review` before calling it done.
- **Gate:** milestone list complete and the build runs clean.

## Phase 5 — Polish

`game-feel` (juice), `camera-systems`, `audio-design` (bus mix, ducking, loudness),
`game-ui-ux` (menus, settings, accessibility), `performance-optimization` (profile first),
`three-quarks` / engine particles for VFX. Replace any remaining placeholder assets.
- **Gate:** polish checklist in `devlog.md` ticked by the user.

## Phase 6 — Ship

Engine export skill (`godot-export`, `unity-build-pipeline`, `unreal-packaging`), then
`itch-publish` (butler channels) and/or `steam-publish`. Licence check for generated assets
(PixelLab / ElevenLabs plan terms) before a commercial release. Page art from the same
PixelLab style anchor.
- **Gate:** the live build downloads and runs on a clean machine.

## Stack by visual style

| Style key | Engine (default) | Art | 3D materials / world | Physics | VFX |
|-----------|------------------|-----|----------------------|---------|-----|
| `pixel-8bit`, `pixel-16bit`, `pixel-iso` | Godot 2D | PixelLab → Pixelorama | — | Godot 2D | PixelLab `vfx_workbench` |
| `pixel-hibit` | Godot 2D + lights | PixelLab + normal maps → Pixelorama | — | Godot 2D | `vfx_workbench` |
| `pixel-3d` | Godot 3D | PixelLab billboards | Material Maker + Terrain3D | Jolt | GPUParticles3D |
| `low-poly`, `toon`, `retro-3d`, `realistic` | Godot 3D | models (external) | Material Maker + Terrain3D | Jolt | GPUParticles3D |
| any style, web target | three.js / Phaser | as above | Material Maker → glTF/PNG | Jolt (JoltPhysics.js) or Phaser Arcade | `three-quarks` |
| `hand-drawn`, `voxel` | Godot | external art, `create-game-assets` | Material Maker (voxel/3D) | engine default | engine particles |
| `minimal` | any | none (procedural) | shaders | engine default | particles + `game-feel` |

Audio is ElevenLabs for every style, mixed with `audio-design` + the engine's audio skill.
