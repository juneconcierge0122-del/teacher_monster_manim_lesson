"""Report two labels that do not overlap but sit on top of each other anyway.

    python tools/crowd.py lessons/advcalc/advcalc_e85_tensor.py AdvCalcE85

`collide.py` asks whether two text boxes *intersect*, and ignores anything
under PAD. Two lines that merely abut therefore come back as zero collisions --
which is exactly what the reader sees as one run-on line. Three of those
shipped past collide in one round:

  E87 beat 4   'Ω f' and '‖ Ω f ‖ = 1.683' placed at the same height, edges
               touching, reading as 'Ω f‖Ω f‖'.
  E85 beat 9   the table's eighth row landed 0.007 units above the caption --
               one pixel at 1080p.
  E88 beat 1   a '§ 5 ⇒ § 6' row sitting on the caption's glyphs.

So this asks the opposite question: x ranges overlap, and the vertical gap is
positive but small. The threshold is below a table's own row pitch (rows set
0.26 apart leave about 0.07), so ordinary spacing is not reported and what is
left is a label that has drifted into the line below it.

Anything under about 0.03 is touching and has to be fixed. Between 0.03 and
GAP it is tight but legible, and the series is full of it; read the report
rather than chasing the number to zero.
"""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim import ValueTracker

from manim_lessons.tools.collide import box, leaves

GAP = 0.048       # a table's own row pitch leaves 0.068-0.072, so stay under it
XOVER = 0.10      # and the two must really share this much width


def main(path, scene):
 mod = importlib.import_module(
     "manim_lessons." + str(pathlib.Path(path).with_suffix("")).replace("/", "."))
 bad = 0
 for lang in ("ZH", "EN"):
  cls = getattr(mod, scene + lang)
  sc = cls.__new__(cls)
  sc.t = ValueTracker(0)
  sc.title, sc.lines = sc.TOPICS_SRC[sc.EPISODE][sc.LANGUAGE]
  for i, (fin, _) in enumerate(sc.stage()):
   texts = []
   for m in fin:
    leaves(m, texts, [])
   for a in range(len(texts)):
    for b in range(a + 1, len(texts)):
     la, ra, ba, ta = box(texts[a])
     lb, rb, bb, tb = box(texts[b])
     ox = min(ra, rb) - max(la, lb)
     gap = max(ba, bb) - min(ta, tb)
     if ox > XOVER and 0.0 <= gap < GAP:
      bad += 1
      print(f"  {scene}{lang} beat {i:2d} gap {gap:.3f}  "
            f"{texts[a].text[:22]!r} / {texts[b].text[:22]!r}")
 print(f"{scene}: {bad} crowded pairs")
 return bad


if __name__ == "__main__":
 sys.exit(1 if main(sys.argv[1], sys.argv[2]) else 0)
