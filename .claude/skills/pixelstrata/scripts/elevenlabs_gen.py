#!/usr/bin/env python3
"""Generate game audio with the ElevenLabs API (standard library only).

Subcommands:
  sfx      PROMPT -o FILE [--duration S] [--loop] [--influence 0-1] [--variants N]
  music    PROMPT -o FILE [--length S] [--instrumental]
  tts      TEXT   -o FILE --voice VOICE_ID [--model MODEL]
  voices   list available voices
  manifest assets.json [--only KEY ...] [--force]   generate every pending audio entry

Needs ELEVENLABS_API_KEY in the environment.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get("ELEVENLABS_API_BASE", "https://api.elevenlabs.io")
DEFAULT_FORMAT = "mp3_44100_128"
AUDIO_TYPES = {"sfx", "music", "voice"}


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set. See references/setup.md.")
    return key


def request(method, path, body=None, query=None):
    url = API + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("xi-api-key", api_key())
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {detail}") from None


def save(audio, out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(audio)
    print(f"wrote {out} ({len(audio) // 1024} KB)")


def variant_path(out, i, n):
    if n == 1:
        return out
    root, ext = os.path.splitext(out)
    return f"{root}_{i + 1}{ext}"


def gen_sfx(prompt, out, duration=None, loop=False, influence=None, variants=1, fmt=DEFAULT_FORMAT):
    body = {"text": prompt, "loop": loop}
    if duration is not None:
        body["duration_seconds"] = max(0.5, min(30.0, float(duration)))
    if influence is not None:
        body["prompt_influence"] = float(influence)
    paths = []
    for i in range(variants):
        path = variant_path(out, i, variants)
        save(request("POST", "/v1/sound-generation", body, {"output_format": fmt}), path)
        paths.append(path)
    return paths


def gen_music(prompt, out, length=None, instrumental=False, fmt=DEFAULT_FORMAT):
    body = {"prompt": prompt, "force_instrumental": instrumental}
    if length is not None:
        body["music_length_ms"] = int(max(3, min(600, float(length))) * 1000)
    save(request("POST", "/v1/music", body, {"output_format": fmt}), out)
    return [out]


def gen_tts(text, out, voice, model="eleven_multilingual_v2", fmt=DEFAULT_FORMAT):
    body = {"text": text, "model_id": model}
    save(request("POST", f"/v1/text-to-speech/{voice}", body, {"output_format": fmt}), out)
    return [out]


def list_voices():
    data = json.loads(request("GET", "/v1/voices"))
    for v in data.get("voices", []):
        labels = ", ".join(f"{k}={val}" for k, val in (v.get("labels") or {}).items())
        print(f"{v['voice_id']}  {v['name']:<24} {labels}")


def run_manifest(path, only=None, force=False):
    with open(path) as f:
        manifest = json.load(f)
    root = os.path.dirname(os.path.abspath(path))
    style = (manifest.get("style") or {}).get("audio", "")
    failures = 0
    for asset in manifest.get("assets", []):
        if asset.get("provider") != "elevenlabs" or asset.get("type") not in AUDIO_TYPES:
            continue
        if only and asset["key"] not in only:
            continue
        if asset.get("status") == "done" and not force:
            continue
        p = asset.get("params") or {}
        out = os.path.join(root, asset["path"])
        prompt = asset["prompt"]
        print(f"[{asset['key']}] {asset['type']}: {prompt}")
        try:
            if asset["type"] == "sfx":
                full = f"{style}, {prompt}" if style else prompt
                gen_sfx(full, out, p.get("duration"), p.get("loop", False),
                        p.get("influence"), int(p.get("variants", 1)))
            elif asset["type"] == "music":
                gen_music(prompt, out, p.get("length"), p.get("instrumental", False))
            else:
                if not p.get("voice_id"):
                    raise RuntimeError("voice entry needs params.voice_id (run `voices`)")
                gen_tts(prompt, out, p["voice_id"], p.get("model", "eleven_multilingual_v2"))
            asset["status"] = "done"
        except RuntimeError as e:
            asset["status"] = "failed"
            asset["error"] = str(e)
            failures += 1
            print(f"  failed: {e}", file=sys.stderr)
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sfx")
    s.add_argument("prompt")
    s.add_argument("-o", "--out", required=True)
    s.add_argument("--duration", type=float)
    s.add_argument("--loop", action="store_true")
    s.add_argument("--influence", type=float)
    s.add_argument("--variants", type=int, default=1)
    s.add_argument("--format", default=DEFAULT_FORMAT)

    m = sub.add_parser("music")
    m.add_argument("prompt")
    m.add_argument("-o", "--out", required=True)
    m.add_argument("--length", type=float, help="seconds (3-600)")
    m.add_argument("--instrumental", action="store_true")
    m.add_argument("--format", default=DEFAULT_FORMAT)

    t = sub.add_parser("tts")
    t.add_argument("text")
    t.add_argument("-o", "--out", required=True)
    t.add_argument("--voice", required=True)
    t.add_argument("--model", default="eleven_multilingual_v2")
    t.add_argument("--format", default=DEFAULT_FORMAT)

    sub.add_parser("voices")

    mf = sub.add_parser("manifest")
    mf.add_argument("path")
    mf.add_argument("--only", nargs="*")
    mf.add_argument("--force", action="store_true")

    a = ap.parse_args()
    try:
        if a.cmd == "sfx":
            gen_sfx(a.prompt, a.out, a.duration, a.loop, a.influence, a.variants, a.format)
        elif a.cmd == "music":
            gen_music(a.prompt, a.out, a.length, a.instrumental, a.format)
        elif a.cmd == "tts":
            gen_tts(a.text, a.out, a.voice, a.model, a.format)
        elif a.cmd == "voices":
            list_voices()
        else:
            sys.exit(1 if run_manifest(a.path, a.only, a.force) else 0)
    except RuntimeError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
