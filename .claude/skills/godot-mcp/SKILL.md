---
name: godot-mcp
description: >
  Drive the Godot engine from the agent through the godot-mcp server (Coding-Solo, MIT): run a
  project and read its debug output and errors, launch the editor, create scenes, add nodes with
  properties, load textures into Sprite2D nodes, save scene variants, export MeshLibrary for
  GridMap, and fix UIDs. Use when verifying a Godot change by running it, importing generated
  sprites into scenes, reading runtime errors, or when the user mentions godot-mcp or the
  mcp__godot__ tools.
---

# godot-mcp

[godot-mcp](https://github.com/Coding-Solo/godot-mcp) (MIT, npm `@coding-solo/godot-mcp`) is an
MCP server that lets the agent run and inspect a real Godot install. It closes the loop:
write code or import assets, **run the game, read the errors**, fix, repeat. In Claude Code its
tools appear as `mcp__godot__<name>`.

## Setup

```bash
claude mcp add godot -e GODOT_PATH=/path/to/godot -- npx @coding-solo/godot-mcp
```

Needs Node.js 18+ and Godot installed. `GODOT_PATH` is optional (auto-detected otherwise).
`DEBUG=true` logs more. PixelStrata's plugin `.mcp.json` declares it already. Restart the
client after adding it.

## Tools

| Tool | Required args | Use |
|------|---------------|-----|
| `get_godot_version` | — | confirm the engine version before choosing APIs |
| `list_projects` | directory | find `project.godot` folders |
| `get_project_info` | projectPath | project structure overview |
| `launch_editor` | projectPath | open the editor for the user |
| `run_project` | projectPath (scene optional) | run in debug mode |
| `get_debug_output` | — | console output and errors of the running game |
| `stop_project` | — | stop it |
| `create_scene` | projectPath, scenePath (rootNodeType optional) | new `.tscn` |
| `add_node` | projectPath, scenePath, nodeType, nodeName (parentNodePath, properties optional) | add a node with properties |
| `load_sprite` | projectPath, scenePath, nodePath, texturePath | put a texture on a Sprite2D |
| `save_scene` | projectPath, scenePath (newPath optional) | save, or save as a variant |
| `export_mesh_library` | projectPath, scenePath, outputPath | build a MeshLibrary for GridMap |
| `get_uid`, `update_project_uids` | projectPath (+ filePath) | Godot 4.4+ UID fixes |

Paths for scenes and textures are relative to the project (`res://` without the prefix), and
`projectPath` is the absolute folder that contains `project.godot`.

## Workflows

**Verify a change (do this after every gameplay edit):** `run_project` → wait briefly →
`get_debug_output` → `stop_project`. Read errors and warnings, fix, run again. Report what ran
and what didn't. Don't call a change done from code inspection alone.

**Import a generated sprite (PixelStrata):**
1. Download PixelLab output into `assets/sprites/...` (path from `assets.json`).
2. `create_scene` (`rootNodeType: "CharacterBody2D"`) or open the existing scene.
3. `add_node` → `Sprite2D` or `AnimatedSprite2D`; `load_sprite` for a single texture. Build
   `SpriteFrames` for animations in a `.tres` with the engine skill (`godot-animation`).
4. `add_node` → `CollisionShape2D` sized from the idle frame.
5. `run_project` + `get_debug_output` to confirm it loads.

**3D tiles for GridMap:** model scene → `export_mesh_library` → assign the `.res` to a GridMap.

## Pitfalls (symptom → cause → remedy)

- **Tools missing** → server not added or client not restarted → `claude mcp list`, restart.
- **"Godot not found"** → no auto-detected binary → set `GODOT_PATH`.
- **Empty debug output** → read too early, or the project crashed at load → run again, check
  `project.godot` main scene.
- **Scene edits lost** → the editor had the scene open and saved over it → close the scene in the
  editor, or edit there instead.
- **Broken `uid://` references after moving files** → `update_project_uids`.

## References

- https://github.com/Coding-Solo/godot-mcp
- Related: `godot-nodes-scenes`, `godot-animation`, `godot-gdscript-headless-testing`,
  `pixelstrata` (import step).
