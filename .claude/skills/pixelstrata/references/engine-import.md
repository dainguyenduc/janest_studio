# Importing generated assets

The engine skill loaded by the `gamedev` router owns the API details; this is the checklist of
what generated pixel art and audio specifically need.

## Godot 4

- Pixel art: Project Settings → Rendering → Textures → Default Texture Filter = **Nearest**;
  Display → Window → Stretch Mode `viewport` (or `canvas_items`) with integer scaling.
- Character frames: `AnimatedSprite2D` + `SpriteFrames`, one animation per PixelLab clip and
  direction (`walk_east`, `idle_south`…). Mirror `east` with `flip_h` for side-scrollers.
- Tilesets: `TileMapLayer` + `TileSet` atlas at the manifest's `tile_size`; set up a terrain set
  (Match Corners) for 16/25-tile Wang sets (`godot-tilemap` skill).
- Audio: `AudioStreamPlayer` on `Music` / `SFX` buses; enable `loop` in the import dock for
  music and ambiences (`godot-audio` skill).

## Unity 6

- Sprites: Texture Type *Sprite (2D and UI)*, Filter Mode **Point**, Compression **None**,
  Pixels Per Unit = `tile_size`; slice sheets with Sprite Editor → Grid By Cell Size.
- Tilesets: Tile Palette + Rule Tile for Wang sets (`unity-tilemap-2d`).
- Audio: Music → *Streaming*, SFX → *Decompress On Load*; route through an AudioMixer.

## Phaser / PixiJS / web

- Phaser: `pixelArt: true` in the game config; `this.load.spritesheet(key, url, {frameWidth, frameHeight})`.
- PixiJS: `TextureStyle.defaultOptions.scaleMode = 'nearest'`.
- Browsers block audio until a user gesture — start music on the first click/keypress.

## Other engines

- LÖVE: `love.graphics.setDefaultFilter("nearest", "nearest")`.
- pygame: scale with `pygame.transform.scale` (not `smoothscale`).
- Unreal (Paper2D): texture group *2D Pixels (unfiltered)*, then *Extract Sprites*.

## Verify in context

After import, run the game and take a screenshot: check scale (no blurry or half pixels),
that every animation plays at a sane FPS (8–12 for pixel art), that tiles connect, and that audio
levels feel balanced. Fix, then mark the manifest entries `done`.
