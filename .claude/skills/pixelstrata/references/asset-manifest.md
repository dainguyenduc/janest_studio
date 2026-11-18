# `assets.json` — the asset manifest

One file at the game's root. Every generated asset has an entry; the agent updates `status`, `id`
and `path` as it works. JSON (not YAML) so the bundled scripts need no dependencies. The idea follows
the asset manifest in awesome-gamedev-agent-skills' `create-game-assets` skill; this schema adds
providers, prompts and gameplay triggers for generation.

```json
{
  "game": "Moss Knight",
  "engine": "godot",
  "style": {
    "view": "side",
    "sprite_size": 48,
    "tile_size": 16,
    "palette_name": "PICO-8",
    "palette": ["#000000", "#1d2b53", "#7e2553", "#008751", "#ab5236", "#5f574f", "#c2c3c7", "#fff1e8",
                "#ff004d", "#ffa300", "#ffec27", "#00e436", "#29adff", "#83769c", "#ff77a8", "#ffccaa"],
    "outline": "single color black outline",
    "audio": "retro 16-bit, dry, no reverb"
  },
  "assets": [
    {
      "key": "player",
      "type": "character",
      "provider": "pixellab",
      "prompt": "small knight in mossy green armor with a short sword",
      "params": { "mode": "v3", "size": 48, "view": "side", "n_directions": 4 },
      "animations": ["breathing-idle", "running-6-frames", "jumping-1", "taking-punch", "falling-back-death"],
      "path": "assets/sprites/player/",
      "status": "pending",
      "id": null
    },
    {
      "key": "ground",
      "type": "sidescroller_tileset",
      "provider": "pixellab",
      "prompt": { "lower": "mossy stone brick", "transition": "grass with small flowers" },
      "params": { "tile_size": 16, "transition_size": 0.25 },
      "path": "assets/tiles/ground/",
      "status": "pending",
      "id": null
    },
    {
      "key": "sfx_jump",
      "type": "sfx",
      "provider": "elevenlabs",
      "prompt": "short springy jump, rising pitch",
      "params": { "duration": 0.4, "variants": 2 },
      "trigger": "player.jumped",
      "path": "assets/audio/sfx/jump.mp3",
      "status": "pending"
    },
    {
      "key": "music_level1",
      "type": "music",
      "provider": "elevenlabs",
      "prompt": "upbeat chiptune adventure, 120 bpm, seamless loop",
      "params": { "length": 60, "instrumental": true },
      "path": "assets/audio/music/level1.mp3",
      "status": "pending"
    },
    {
      "key": "vo_guard_01",
      "type": "voice",
      "provider": "elevenlabs",
      "prompt": "Halt! Nobody passes the gate after dark.",
      "params": { "voice_id": "<voice id>" },
      "trigger": "guard.dialogue.greet",
      "path": "assets/audio/vo/guard_01.mp3",
      "status": "pending"
    }
  ]
}
```

## Fields

| Field | Required | Meaning |
|-------|----------|---------|
| `key` | yes | unique id used in code (`"sfx_jump"`) |
| `type` | yes | `character`, `animation`, `topdown_tileset`, `sidescroller_tileset`, `isometric_tile`, `object`, `object_8dir`, `ui`, `vfx`, `sfx`, `music`, `voice`, `material` |
| `provider` | yes | `pixellab`, `elevenlabs`, `material-maker`, `pixelorama` or `manual` |
| `prompt` | yes | text sent to the provider (string, or object for two-terrain tilesets) |
| `params` | no | provider parameters (see the provider reference) |
| `trigger` | no | gameplay event that plays/uses it — used when wiring the engine |
| `path` | yes | file or folder inside the project |
| `status` | yes | `pending` → `queued` → `done` / `failed` |
| `id` | no | PixelLab character/tileset/object id, for re-download and style matching |
| `source` | no | editable master, e.g. a Pixelorama `.pxo` or Material Maker `.ptex`, re-exported to `path` |

Top-level keys besides `assets`: `game`, `engine`, `style` (see `visual-styles.md`, with
`style.visual` set to a style key) and `mechanics` (Gameplay Atlas slugs, e.g.
`["farming-growth-care", "relationships-gift-allocation"]`). For a `material` entry the
provider is `material-maker` and `path` is the export folder.

`python3 scripts/doctor.py --manifest assets.json` validates the file and prints a summary.
