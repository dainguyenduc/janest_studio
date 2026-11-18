# PixelLab reference

PixelLab is reached through its MCP server (`https://api.pixellab.ai/mcp`). Tool names below are
the server's own; in Claude Code they appear as `mcp__pixellab__<name>`. Costs are in PixelLab
"generations" and change over time — the tool descriptions and each job receipt are authoritative.
Call `get_balance` before a batch.

## Which tool for which asset

| Asset | Tool | Notes |
|-------|------|-------|
| Hero / NPC / enemy (humanoid) | `create_character` | default `mode="v3"` (≈2 gens ≤88 px). `standard` = 1 gen, cheapest. `pro` = 10–25 gens, use `style_character_id` to match an existing character. |
| Animal | `create_character` `body_type="quadruped"` + `template` (bear, cat, dog, horse, lion) | or `create_character_pro_flash(template_id=...)` |
| Turn an existing sprite into 8 directions | `create_character` `mode="v3"` + `reference_image_url` | the reference **must face the viewer** (south) or every direction is mislabeled |
| Animation | `animate_character` | template id first (1 gen/direction), then `v3` custom, then `pixminimax` for long clips |
| Top-down terrain | `create_topdown_tileset` | two terrains per set; chain with `lower_base_tile_id` |
| Platformer terrain | `create_sidescroller_tileset` | chaining a new top onto the same body needs `mode="pro"` |
| Isometric | `create_isometric_tile` | `tile_shape`: thin / thick / block |
| Prop, single view | `create_map_object` | transparent up to 200×200 area; pass `background_image` to match a map |
| Prop, rotating | `create_8_direction_object` | 10–25 gens; `style_object_id` for a matching family |
| UI panel / HUD frame | `create_ui_asset` | 10 gens up to 256², pass `palette` / `style_image_base64` |
| Whole map / room | `create_map`, `create_room` | then `place_map_object`, `view_map` |
| Font | `create_font` | |
| Portrait / talking head | `create_portrait_character`, `create_talking_gif`, `create_vocal_animation` | pair with ElevenLabs voice lines |
| Spell, hit, explosion | `vfx_workbench(argv=['describe','start'])` | free tool, you are the artist |
| Exact pixel edits, cleanup | `pixelart_workbench(argv=['describe','start'])`, `reduce_colors`, `correct_pixelart` | free |
| Convert an image | `image_to_pixelart`, `unzoom_image` | |

Help is built in: `search_help` and `search_knowledge` answer questions about the tools.

## Animation templates (humanoid)

Common ids with frame counts: `breathing-idle` (4), `walking-6-frames` (6), `walking-8-frames` (8),
`running-6-frames` (6), `running-8-frames` (8), `jumping-1` (9), `two-footed-jump` (7),
`lead-jab` (3), `cross-punch` (6), `high-kick` (7), `fireball` (6), `throw-object` (7),
`taking-punch` (6, use for hurt), `falling-back-death` (7), `getting-up` (5),
`running-slide` (6, use for dash), `crouching` (5), `picking-up` (5).

Names like `hurt`, `dashing`, `casting`, `shooting` do **not** exist — map them to the ids above.
`get_character` lists the clips available for a specific character (quadrupeds differ).

## Async workflow

1. Queue (`create_*` / `animate_*`) → returns an id immediately.
2. `wait_for_jobs(min_finished=N, timeout_seconds=<under the client timeout>)` — free, no polling.
3. `get_character` / `get_topdown_tileset` / `get_map_object` / … → URLs and a download link.
4. Download into the manifest's `path` (e.g. `curl -L -o assets/sprites/player.zip <url>`),
   unzip, record frame size and directions in the manifest.

If an animation lands only some directions (rate limit), append the rest with the same
`animation_group_id` **and** the same `animation_name`.

## Consistency checklist

- One `view` for characters, props and tilesets (`create_character` defaults to `low top-down`;
  standard top-down tilesets always draw `high top-down` — use `mode="pro"` tilesets with
  `view="low top-down"` if the characters are low top-down).
- One sprite size class; animations grow the canvas (a 96 px character often animates at ~132 px),
  so size collision shapes from the idle frame, not the canvas.
- Palette: only `pro` modes and tools without a standard mode accept `palette` / `max_colors`.
- Generate the anchor character first; derive the rest with `style_character_id` /
  `style_object_id` / `style_image_base64`.

## Cost control

- Prefer `standard` tilesets and template animations while prototyping; upgrade to `pro` for the
  final pass only for assets the player sees most.
- Animate only the directions the game uses (side-scroller: `east` + mirror in engine).
- Ask before any batch whose total exceeds ~20 generations.
