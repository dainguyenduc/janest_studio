# Gameplay Atlas — the mechanics reference

[Gameplay Atlas](https://gameplayatlas.loopyhop.com/) is a field guide to game mechanics for
solo developers and small teams: 280 mechanics in 28 groups. Each entry gives a one-line summary,
the core loop in four steps, how it plays, the decisions the player weighs up, and sourced
examples from real games.

PixelStrata uses it during planning (SKILL.md §0, step 3) to choose and describe the game's core
mechanics. **Link to it and read it live; do not copy its text into the project or this repo.**
The site states no reuse licence.

## How to read it

- Index of every entry: `https://gameplayatlas.loopyhop.com/sitemap.xml`. Slugs look like
  `<group>-<mechanic>`, for example `combat-stamina-budget`.
- One entry: `https://gameplayatlas.loopyhop.com/mechanic/<slug>/`. It renders as plain HTML, so
  a web fetch works. The home page needs JavaScript to filter, so use the sitemap instead.
- Fetch only the 3–6 entries you are about to propose. Don't crawl the whole site.

## The 28 groups (slug prefix → typical genres)

| Prefix | Fits | Prefix | Fits |
|--------|------|--------|------|
| `allocation` | strategy, management | `exploration` | metroidvania, open world |
| `automation` | factory, sim | `farming` | cozy, life sim |
| `building` | city builder, survival | `fishing` | cozy, minigames |
| `combat` | action, soulslike | `gathering` | survival, crafting |
| `command` | RTS, tactics | `incremental` | idle, clicker |
| `commerce` | shop sim, trading | `inventory` | RPG, survival, horror |
| `cooking` | cozy, time management | `matching` | match-3, puzzle |
| `cooperation` | co-op, party | `movement` | platformer, traversal |
| `deckbuilding` | roguelike deckbuilder | `narrative` | visual novel, RPG |
| `defense` | tower defense | `progression` | RPG, roguelite |
| `driving` | racing, vehicles | `projectiles` | shooter, shmup |
| `ecology` | sim, survival | `puzzles` | puzzle, adventure |
| `relationships` | dating sim, life sim | `rhythm` | rhythm, music |
| `stealth` | stealth, horror | `survival` | survival, crafting |

## Using it in a plan

1. From the user's idea and the chosen genre, pick 1–2 groups.
2. Read the sitemap and shortlist 4–6 slugs whose names fit.
3. Fetch those entries and propose **2–3 core mechanics** in the plan, each with its link, its
   four-step loop in your own words, and the gameplay skill that implements it (for example
   `combat-stamina-budget` → `game-feel` + the engine's movement skill).
4. Record the chosen slugs in `assets.json` → `mechanics` so later sessions reuse them.
