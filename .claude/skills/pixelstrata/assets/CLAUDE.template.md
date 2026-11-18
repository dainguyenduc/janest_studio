# <Game name>

<One-line pitch.>

## How to work on this game

- **Entry point:** start every request with the `pixelstrata` skill. It plans first (plan mode),
  asks before spending PixelLab/ElevenLabs credits, and calls the `gamedev` router for code.
- **Current phase:** <0 Setup | 1 Concept | 2 Prototype | 3 Vertical slice | 4 Production | 5 Polish | 6 Ship>
- **Read first:** `docs/gdd.md` (design), `assets.json` (style + assets), `docs/devlog.md` (decisions).
  Don't re-ask anything these files already answer.

## Locked decisions

- Engine: <Godot 4.x> · Visual style: <style key from assets.json> · View: <side / top-down / 3D>
- Core mechanics (Gameplay Atlas): <slug>, <slug>
- Tools: <PixelLab, Pixelorama, ElevenLabs, Material Maker, Terrain3D, Jolt, three.quarks — keep only those used>

## Commands

- Run: <`mcp__godot__run_project` with projectPath <abs path> | `npm run dev` | ...>
- Tests: <`godot --headless -s tests/run.gd` | ...>
- Export: <command or preset>

## Rules

- One feature per commit; update `docs/devlog.md` at the end of each milestone.
- Every generated file is listed in `assets.json`; nothing is generated outside it.
- Verify changes by running the game and reading errors before calling them done.
