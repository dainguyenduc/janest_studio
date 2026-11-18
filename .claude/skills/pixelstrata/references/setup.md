# Setup

Every layer degrades gracefully: without a key or a server, the skill still does the rest and
tells you what it skipped. **Pick one install method** (`install.sh` *or* the plugins). Both at
once install every skill twice; `doctor.py` warns about that.

## 1. Skills

PixelStrata needs the router and engine/genre/discipline skills from
[awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills).
`./install.sh` installs them from upstream when they are missing, then copies the PixelStrata skills to
`~/.claude/skills/` (any PixelStrata skill you changed is backed up to
`~/.claude/skills-backup/<timestamp>/` first). Manual install of the dependency:

```bash
npx skills add gamedev-skills/awesome-gamedev-agent-skills -a claude-code -g
```

As plugins instead (both, or neither):

```bash
claude plugin marketplace add gamedev-skills/awesome-gamedev-agent-skills
claude plugin install gamedev@awesome-gamedev-agent-skills
claude plugin marketplace add jasonmello/pixelstrata
claude plugin install pixelstrata@pixelstrata
```

## 2. MCP servers (configured once, at user scope)

The plugin does **not** declare MCP servers, so it never duplicates ones you already have.
`install.sh` adds each server only if it is missing.

**PixelLab** (pixel art). Get an API key at <https://pixellab.ai> (account → API):

```bash
claude mcp add --transport http pixellab https://api.pixellab.ai/mcp \
  --header "Authorization: Bearer $PIXELLAB_API_KEY" -s user
```

**godot-mcp** (run Godot, read errors, edit scenes). Needs Node.js 18+ and Godot:

```bash
claude mcp add godot -s user -e GODOT_PATH=/path/to/godot -- npx -y @coding-solo/godot-mcp
```

`GODOT_PATH` is optional when Godot is on the default path.

## 3. ElevenLabs API key

Create a key at <https://elevenlabs.io/app/settings/api-keys> with Sound Effects, Music and Text
to Speech access:

```bash
export ELEVENLABS_API_KEY=...   # add to ~/.zshrc or ~/.bashrc
```

## 4. Desktop tools (optional, per style)

| Tool | For | Get it |
|------|-----|--------|
| Pixelorama | pixel-art clean-up and spritesheet export | https://github.com/Orama-Interactive/Pixelorama/releases |
| Material Maker | procedural 3D materials | https://github.com/RodZill4/material-maker/releases |
| Terrain3D | Godot terrain addon (per project) | Godot AssetLib or https://github.com/TokisanGames/Terrain3D/releases |
| Jolt Physics | 3D physics: built into Godot 4.4+ | nothing to install for Godot |
| three.quarks | three.js VFX (per project) | `npm install three.quarks` |
| butler | itch.io uploads | https://itch.io/docs/butler/ |

## Check

```bash
python3 ~/.claude/skills/pixelstrata/scripts/doctor.py
```
