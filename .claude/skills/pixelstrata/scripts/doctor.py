#!/usr/bin/env python3
"""Check that PixelStrata's three layers are ready and validate assets.json.

Usage: doctor.py [--manifest assets.json]
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROUTER_NAMES = ("gamedev", "router")
TYPES = {"character", "animation", "topdown_tileset", "sidescroller_tileset", "isometric_tile",
         "object", "object_8dir", "ui", "vfx", "sfx", "music", "voice", "material"}
PROVIDERS = {"pixellab", "elevenlabs", "material-maker", "pixelorama", "manual"}
STATUSES = {"pending", "queued", "done", "failed"}


def config_home():
    """Claude Code config dir. Honours CLAUDE_CONFIG_DIR (janest_studio patch)."""
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env).expanduser() if env else Path.home() / ".claude"


def skill_dirs():
    home = config_home()
    yield Path.cwd() / ".claude" / "skills"
    yield home / "skills"
    plugins = home / "plugins"
    if plugins.is_dir():
        for p in plugins.rglob("SKILL.md"):
            yield p.parent.parent


def router_installed():
    for d in skill_dirs():
        for name in ROUTER_NAMES:
            skill = d / name / "SKILL.md"
            if skill.is_file() and "Routing algorithm" in skill.read_text(errors="ignore"):
                return skill
    return None


def skill_name(skill_md):
    for line in skill_md.read_text(errors="ignore").splitlines()[1:6]:
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return skill_md.parent.name


def duplicate_skills():
    """Skill names installed in more than one place (e.g. install.sh *and* a plugin)."""
    home = config_home()
    roots = [Path.cwd() / ".claude" / "skills", home / "skills"]
    found = {}
    for root in roots:
        for p in root.glob("*/SKILL.md") if root.is_dir() else []:
            found.setdefault(skill_name(p), set()).add(str(root))
    plugins = home / "plugins"
    if plugins.is_dir():
        for p in plugins.rglob("SKILL.md"):
            # one plugin may keep several cached versions; count each plugin once
            parts = p.relative_to(plugins).parts
            found.setdefault(skill_name(p), set()).add("plugin:" + "/".join(parts[:3]))
    return {n: sorted(w) for n, w in found.items() if len(w) > 1}


def check_manifest(path):
    problems = []
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot read {path}: {e}"], {}
    seen = set()
    counts = {}
    for i, a in enumerate(data.get("assets", [])):
        where = a.get("key", f"assets[{i}]")
        for field in ("key", "type", "provider", "prompt", "path", "status"):
            if field not in a:
                problems.append(f"{where}: missing '{field}'")
        if a.get("key") in seen:
            problems.append(f"{where}: duplicate key")
        seen.add(a.get("key"))
        if a.get("type") not in TYPES:
            problems.append(f"{where}: unknown type {a.get('type')!r}")
        if a.get("provider") not in PROVIDERS:
            problems.append(f"{where}: unknown provider {a.get('provider')!r}")
        if a.get("status") not in STATUSES:
            problems.append(f"{where}: unknown status {a.get('status')!r}")
        if a.get("type") == "voice" and not (a.get("params") or {}).get("voice_id"):
            problems.append(f"{where}: voice needs params.voice_id")
        key = (a.get("provider"), a.get("status"))
        counts[key] = counts.get(key, 0) + 1
    return problems, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="assets.json")
    args = ap.parse_args()
    ok = True

    router = router_installed()
    print(f"[{'ok' if router else '!!'}] gamedev router: {router or 'not found — see references/setup.md §1'}")
    ok &= bool(router)

    has_key = bool(os.environ.get("ELEVENLABS_API_KEY"))
    print(f"[{'ok' if has_key else '!!'}] ELEVENLABS_API_KEY {'set' if has_key else 'missing — audio generation disabled'}")
    ok &= has_key

    print("[??] PixelLab / godot-mcp: the agent checks for mcp__pixellab__* and mcp__godot__* tools")

    dupes = duplicate_skills()
    for name, where in sorted(dupes.items()):
        print(f"[!!] skill '{name}' installed twice: {', '.join(where)} — keep one install method")
    if not dupes:
        print("[ok] no duplicate skill installs")
    ok &= not dupes

    if Path(args.manifest).is_file():
        problems, counts = check_manifest(args.manifest)
        for p in problems:
            print(f"[!!] {p}")
        summary = ", ".join(f"{prov}/{st}: {n}" for (prov, st), n in sorted(counts.items(), key=str))
        print(f"[{'ok' if not problems else '!!'}] {args.manifest}: {summary or 'no assets'}")
        ok &= not problems
    else:
        print(f"[--] no {args.manifest} yet (see references/asset-manifest.md)")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
