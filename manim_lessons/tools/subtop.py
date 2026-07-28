"""Print the top edge of every subtitle, so animation elements can be kept clear.

    python tools/subtop.py 49 53

No rendering involved: it builds the same Text the scene would and reads its
bounding box. Measure rather than guess -- four-line English subtitles top out
around y = -2.0 to -2.3, not the -1.55 a line count would suggest, and the
Chinese ones sit lower still.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim import tempconfig
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.lib.design_tokens import FS_BODY, INK

lo = int(sys.argv[1]) if len(sys.argv) > 1 else 49
hi = int(sys.argv[2]) if len(sys.argv) > 2 else lo

with tempconfig({"quality": "low_quality"}):
 for n in range(lo, hi + 1):
  tops = {}
  for lang in ("zh", "en"):
   sc = type("S", (LandauBatchBase,), {"EPISODE": n, "LANGUAGE": lang})()
   sc.setup()
   tops[lang] = []
   for line in sc.lines:
    m = sc.text(line, FS_BODY, INK)
    m.to_edge([0, -1, 0], buff=.5)
    tops[lang].append(float(m.get_top()[1]))
  print(f"L{n}")
  for lang in ("zh", "en"):
   print(f"  {lang}: " + " ".join(f"{i}:{t:+.2f}" for i, t in enumerate(tops[lang])))
  print(f"  highest subtitle top = {max(max(tops['zh']), max(tops['en'])):+.3f}"
        f"   -> keep animation elements above about that + 0.1")
