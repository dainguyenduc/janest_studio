---
name: pixelorama
description: >
  Edit, animate and export pixel art with Pixelorama (MIT, free, built on Godot): clean up and
  touch up AI-generated sprites, draw frames with onion skinning, manage palettes and tilemap
  layers, and batch-export .pxo projects to PNG frames, spritesheets, GIFs or JSON from the
  command line (--export, --spritesheet, --headless). Use when the user mentions Pixelorama or
  .pxo files, wants a free Aseprite alternative, needs to fix or redraw PixelLab output by hand,
  or wants a scripted spritesheet export for a game engine.
---

# Pixelorama

[Pixelorama](https://github.com/Orama-Interactive/Pixelorama) (MIT) is a free, open-source
pixel-art editor built on Godot 4.7. Latest release **v1.2.3** (Sep 2026). It runs on Windows,
macOS, Linux, Android and the web. Get it from GitHub releases, itch.io, Steam, Flathub or WinGet.
Features: layers and frames timeline, onion skinning, frame tags, audio sync, palettes (Lospec
import), tilemap layers (rectangular, isometric, hexagonal), 3D layers, non-destructive layer
effects (outline, gradient map, drop shadow), extensions, and a **command-line exporter**.

## When to use

- In the PixelStrata pipeline, between PixelLab and the engine: fix stray pixels, recolour to the game
  palette, add a missing frame, or draw a sprite the AI can't get right.
- The user draws their own pixel art and wants a free editor plus scripted exports.
- Batch-exporting `.pxo` projects to spritesheets for the engine.

**Not this skill:** AI generation → PixelLab via `pixelstrata`; exact per-pixel edits an agent
can make without a GUI → PixelLab's free `pixelart_workbench`; engine import → `engine-import.md`
in `pixelstrata` and the engine skill.

## Workflow

1. **Bring art in.** Open the PNG frames or spritesheet PixelLab produced (File → Import,
   choosing spritesheet slicing with the frame size from the manifest), or open an existing `.pxo`.
2. **Edit in the UI** (this part is the user's or yours via instructions): lock the project
   palette first, then fix the frames, then name animations with frame tags (`idle`, `walk`…).
3. **Save as `.pxo`** next to the source art (for example `art/src/player.pxo`). It's the
   editable master. Exports are disposable.
4. **Export from the CLI** into the engine's asset folder (below), then re-run the engine import.
5. Record the `.pxo` path in the manifest entry (`source`) so later edits re-export the same way.

## Command line

Flags from Pixelorama's `src/Main.gd` (v1.2.3). Run `Pixelorama --help` for the installed version.

```bash
# every frame as numbered PNGs
pixelorama art/src/player.pxo --export --output assets/sprites/player/player.png
# one horizontal spritesheet, scaled 2x, frames 1-6 only
pixelorama art/src/player.pxo --spritesheet --output assets/sprites/player_walk.png --frames 1-6 --scale 2
# plus a JSON file describing the frames
pixelorama art/src/player.pxo --spritesheet --json --output assets/sprites/player.png
# on a machine without a display
pixelorama --headless art/src/player.pxo --export --output out/player.png
```

| Flag | Meaning |
|------|---------|
| `--export`, `-e` | export the project (frames, or a GIF/APNG by output extension) |
| `--spritesheet`, `-s` | export as a spritesheet |
| `--output`, `-o` | output path with extension |
| `--scale` | integer upscale |
| `--frames`, `-f` | frame range, e.g. `2-7` |
| `--direction`, `-d` | `0` forward, `1` backward, `2` ping-pong |
| `--json` | also write the project's JSON data |
| `--split-layers` | export each layer separately |
| `--sheet_layers_as_separate_files` | with split layers, one sheet file per layer |
| `--size`, `--framecount`, `--version` | print info and exit |
| `--headless` | Godot's headless mode, no window |

The executable name depends on the platform: `Pixelorama.exe` on Windows, inside
`Pixelorama.app/Contents/MacOS/` on macOS, the extracted binary on Linux. Ask the user for the
install path. An unknown flag stops the export and prints similar options.

## Pitfalls (symptom → cause → remedy)

- **Blurry sprites in the engine** → linear filtering, or a non-integer scale → export at
  `--scale 1`, set nearest filtering in the engine.
- **Spritesheet frames misaligned in the engine** → slicing doesn't match the export layout →
  use `--json` and read frame rects from it, or slice by the exact frame size.
- **Colours drift from the game palette** → edits made outside the locked palette → use the
  palette tools before exporting.
- **CLI export does nothing** → an unknown flag aborted it → check the printed "Similar option".

## References

- Repo and docs: https://github.com/Orama-Interactive/Pixelorama · https://orama-interactive.github.io/Pixelorama-Docs/
- Related: `pixelstrata` (PixelLab pipeline), `create-game-assets`, `godot-animation`,
  `godot-tilemap`.
