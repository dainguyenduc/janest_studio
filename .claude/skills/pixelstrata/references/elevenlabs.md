# ElevenLabs reference

The bundled `scripts/elevenlabs_gen.py` calls the ElevenLabs REST API with only the Python
standard library. It needs `ELEVENLABS_API_KEY` in the environment. If an ElevenLabs MCP server is
connected you may use it instead; keep writing results into the manifest either way.

| Kind | Endpoint | Script subcommand | Limits |
|------|----------|-------------------|--------|
| Sound effect | `POST /v1/sound-generation` | `sfx` | 0.5–30 s, `loop`, `prompt_influence` 0–1 |
| Music | `POST /v1/music` | `music` | 3 s–10 min, `force_instrumental` |
| Voice line | `POST /v1/text-to-speech/{voice_id}` | `tts` | model `eleven_multilingual_v2` by default |
| List voices | `GET /v1/voices` | `voices` | |

Output format defaults to `mp3_44100_128`. WAV/PCM 44.1 kHz needs a higher plan tier; for most
engines MP3/OGG is fine for music and MP3/WAV for SFX (convert with `ffmpeg` if the engine prefers
OGG: `ffmpeg -i in.mp3 -c:a libvorbis -q:a 5 out.ogg`).

## Prompting

**SFX — describe the sound, not the story.**

| Weak | Strong |
|------|--------|
| player jumps | short springy 8-bit jump, rising pitch, 0.3 s |
| enemy dies | retro squelch with a descending blip, dry, no reverb |
| door opens | heavy wooden door creak, slow, medium room reverb |
| forest | gentle forest ambience, birds and light wind, seamless loop (`--loop`) |

Style words that keep a set coherent: `8-bit`, `chiptune`, `16-bit SNES-style`, `retro arcade`,
`orchestral foley`, `lo-fi`, `dry` / `no reverb`. Put the shared words in `style.audio` in the
manifest; the script prepends them to every prompt automatically.

Generate 2–3 variants of frequent sounds (footsteps, hits) with `--variants 3` and randomise
between them in the engine.

**Music.** Genre + tempo + mood + instrumentation + structure:
`"chiptune boss battle, 150 bpm, urgent, square leads and noise drums, seamless loop"`.
Use `--instrumental` for in-game tracks. 30–90 s loops are enough for a slice.

**Voice.** Pick one voice per character (`voices` lists ids), store it in the manifest entry's
`voice_id`, and keep lines short (one sentence per file) so they can be triggered individually.
Punctuation drives delivery ("No… not again!").

## Loudness targets (rough)

Music −16 to −14 LUFS, SFX peaks around −3 dBFS, dialogue around −16 LUFS. Normalise in a batch:
`ffmpeg -i in.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11 out.mp3`. Final balance belongs on engine
audio buses (see the `audio-design` skill from the router).
