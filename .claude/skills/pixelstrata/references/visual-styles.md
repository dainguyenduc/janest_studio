# Visual style catalog

The first question of every PixelStrata session (SKILL.md §0). Offer these as options, recommend one
that fits the user's idea, and record the answer in `assets.json` → `style.visual`. The choice
decides the whole asset pipeline, so nothing is generated before it is locked.

| Key | Style | Looks like | Camera | Asset pipeline | Engine fit |
|-----|-------|-----------|--------|----------------|------------|
| `pixel-8bit` | 8-bit pixel art | NES, Game Boy, PICO-8; 8–16 px tiles, ≤16 colours | side / top-down | PixelLab, named `palette` (pro modes), `size` 16–32 | any 2D; Godot, Phaser, LÖVE, pygame |
| `pixel-16bit` | 16-bit pixel art | SNES / Mega Drive; 16–32 px tiles, 32–64 px characters | side / low top-down | PixelLab v3 characters, standard tilesets | any 2D |
| `pixel-hibit` | Hi-bit pixel art | modern pixel art with rich lighting, 64–128 px sprites | side / top-down | PixelLab v3/pro + `create_normal_map` for 2D lights | Godot 2D (PointLight2D), Unity 2D URP |
| `pixel-iso` | Isometric pixel art | tactics / city builders | isometric | `create_isometric_tile`, `create_8_direction_object` | Godot TileMapLayer (isometric), Phaser |
| `pixel-3d` | Pixel sprites in 3D (2.5D) | pixel sprites in a lit 3D world, depth of field, bloom | 3D perspective, fixed angle | PixelLab sprites (billboards) + `terrain3d` + `material-maker` | Godot 3D, Unreal |
| `hand-drawn` | Hand-drawn / painted 2D | cartoon, ink, watercolour, vector | side / top-down | not PixelLab: `create-game-assets` skill + an image generator or the user's artist | any 2D (smooth filtering) |
| `low-poly` | Low-poly 3D | flat-shaded facets, simple palettes | any 3D | modelling tool + `material-maker` (flat colours, gradients) | Godot 3D, Unity, three.js |
| `retro-3d` | PS1 / N64 retro 3D | low-res textures, vertex jitter, dithering, fog | any 3D | `material-maker` at 64–128 px with nearest filtering, or PixelLab textures + `shader-programming` | Godot 3D, Unity |
| `toon` | Stylized / cel-shaded 3D | anime / comic outlines, banded light | any 3D | toon shader (`shader-programming`) + `material-maker` stylized | Godot, Unity, Unreal |
| `realistic` | Realistic PBR 3D | physically based materials, large terrains | any 3D | `material-maker` PBR + `terrain3d` + `jolt-physics` | Godot 3D, Unreal, Unity |
| `voxel` | Voxel | cubes (MagicaVoxel style) | 3D, often isometric | MagicaVoxel export (external) + engine import | Godot, Unity |
| `minimal` | Minimalist / geometric | shapes, neon, flat colour, particles | 2D or 3D | procedural only: shaders, particles, `game-feel` — no asset generation | anything; best for jams |

## How to ask

Use the client's question tool (in Claude Code: `AskUserQuestion`) with at most 4 options, picked
from the table to fit what the user already said. The client adds "Other" automatically. Example
for "a cozy farming game":

1. `pixel-16bit` (Recommended): cozy, readable, cheapest to generate with PixelLab
2. `pixel-hibit`: same look with richer light; more generations per sprite
3. `toon`: stylized 3D; needs models plus Material Maker
4. `hand-drawn`: painted 2D; needs an image generator or an artist

After the answer, ask only what that style still needs: palette (pixel styles), sprite/tile size,
camera (if not implied), and a reference game or image.

## What each choice locks into `style`

```json
"style": { "visual": "pixel-16bit", "view": "low top-down", "sprite_size": 48, "tile_size": 16,
           "palette_name": "Endesga 32", "outline": "single color black outline",
           "references": ["Stardew Valley", "https://..."] }
```

3D styles record `texture_size`, `filter` (`nearest` or `linear`) and `shading` instead of
`sprite_size` and `outline`.
