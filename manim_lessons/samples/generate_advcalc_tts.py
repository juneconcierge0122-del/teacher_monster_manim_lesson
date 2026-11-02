"""Narration audio for one advcalc episode, one language.

    python samples/generate_advcalc_tts.py 89 en samples/audio_e89/en

edge_tts raises NoAudioReceived intermittently -- the service accepts the
handshake and then sends no audio frames.  It is not a bad parameter and not a
bad sentence: the same text saved a second later works.  Without a retry the
loop aborts on the first one and leaves a zero-length file behind, and because
the whole thing still exits 0 the only thing that notices is tools/ttscheck.py.
So each beat is retried, and a beat already on disk and non-empty is left alone,
which makes re-running the command the way to fill in a partial run.
"""
import argparse, asyncio, pathlib, sys, edge_tts

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim_lessons.localization.advcalc import TOPICS_ADVCALC

VOICES = {"zh": "zh-TW-HsiaoChenNeural", "en": "en-US-AndrewNeural"}
TRIES = 5


async def beat(text, voice, path):
 for k in range(TRIES):
  try:
   await edge_tts.Communicate(text, voice, rate="-4%").save(str(path))
   if path.stat().st_size > 0:
    return True
  except Exception as exc:                       # noqa: BLE001 -- retry anything
   print(f"  {path.name} attempt {k + 1}: {type(exc).__name__}", flush=True)
   await asyncio.sleep(2.0 * (k + 1))
 return False


async def run(n, lang, out):
 out.mkdir(parents=True, exist_ok=True)
 bad = []
 for i, s in enumerate(TOPICS_ADVCALC[n][lang][1]):
  p = out / f"{i:02d}.mp3"
  if p.exists() and p.stat().st_size > 0:
   continue
  if not await beat(s, VOICES[lang], p):
   bad.append(p.name)
 if bad:
  sys.exit(f"no audio after {TRIES} tries: {', '.join(bad)}")


if __name__ == "__main__":
 p = argparse.ArgumentParser()
 p.add_argument("episode", type=int)
 p.add_argument("language", choices=["zh", "en"])
 p.add_argument("output", type=pathlib.Path)
 a = p.parse_args()
 asyncio.run(run(a.episode, a.language, a.output))
