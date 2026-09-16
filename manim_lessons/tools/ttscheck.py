"""Check every narration file of an episode, not just that the files exist.

    python tools/ttscheck.py 75 76

Counting files passes when one of them is broken, and that has happened twice.
E72's English beat 10 was 7.2 s for a 276-character line because the generator
was moved to the background by a 120 s tool timeout and wrote the last mp3
corrupt -- all eleven files present, one of them raising InvalidDataError on
av.open.  E75 was worse: edge_tts raised NoAudioReceived on the fifth Chinese
line and left a zero-byte file, and because the command was
`zh && en && echo DONE` the whole English batch never ran at all -- while the
tool reported exit 0, since what exited was the launcher.

So this checks four things per file (exists, non-empty, decodable, longer than
six seconds), prints the total per language, and exits nonzero if anything is
wrong.  Run it after generating, and do not trust the generator's return value.
"""
import av, pathlib, sys

# resolved from the script, like the other tools here, so it runs from either
# the repo root or manim_lessons/
ROOT = pathlib.Path(__file__).resolve().parents[1]
ok = True
for ep in sys.argv[1:]:
 for lang in ("zh-TW", "en"):
  d = ROOT / f"samples/audio_e{ep}" / lang
  if not d.is_dir():
   print(f"e{ep} {lang}: MISSING DIR"); ok = False; continue
  tot, rows, bad = 0.0, [], []
  for k in range(11):
   f = d / f"{k:02d}.mp3"
   if not f.exists() or f.stat().st_size == 0:
    bad.append(f"{k:02d} empty/missing"); continue
   try:
    with av.open(str(f)) as c:
     s = float(c.duration / av.time_base)
   except Exception as e:
    bad.append(f"{k:02d} unreadable"); continue
   rows.append(s); tot += s
   if s < 6.0:
    bad.append(f"{k:02d} only {s:.2f}s")
  print(f"e{ep} {lang}: {len(rows)}/11 files, {tot:6.1f}s = {int(tot // 60)}:{int(tot % 60):02d}"
        + ("   BAD: " + ", ".join(bad) if bad else "   all good"))
  if bad or len(rows) != 11:
   ok = False
sys.exit(0 if ok else 1)
