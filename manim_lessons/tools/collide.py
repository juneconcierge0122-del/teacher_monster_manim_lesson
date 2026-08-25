"""Report elements that sit inside the frame but on top of each other.

    python tools/collide.py lessons/advcalc/advcalc_e28_elementary_matrices.py AdvCalcE28

`bounds.py` finds things that run off the edge. This finds the other half of
the layout bugs, the ones that have twice cost a re-render:

  E27  marker lines drawn through a matrix to pick out a column and a row
       covered the numbers they were pointing at.
  E28  an arrow rising at one cell to point at it ran its shaft straight
       through the entry in the row below.

Both were invisible to bounds.py (everything was inside the frame) and to a
480p probe frame (a stroke crossing a digit is a few pixels there). Both were
obvious in the finished 1080p render, which is the expensive place to find out.

Two checks:

  text/text     two labels whose boxes overlap. Captions are centred and get
                scaled to fit, so this mostly catches a label placed under a
                figure drifting into the caption row beneath it.
  stroke/text   a line, arrow, dash or curve whose path passes through a
                label's box. Tested segment against box, not box against box,
                so a diagonal connector running past a label is not reported
                merely because their bounding boxes share a corner.

Closed shapes are skipped -- `_box` draws a rectangle around its own label
and the region blobs are ellipses with their names written on the rim -- as is
any stroke whose own box swallows the label's, which is the same situation
drawn a different way. What is left still needs a person's eye now and then: a
label deliberately placed on a line, an arrow that ends on its own target, will
be reported. The point is to make those the only things worth looking at.
Text boxes are inset before the stroke test, so an arrow tip that stops just
short of a label, which is what a pointer is supposed to do, does not count.
Both language scenes are built and checked, since the two lay out differently.

Aim for zero on a new episode. The episodes written before this existed do
report hits, and they were left alone: E22's three arrows really do cross the
`0` they converge on, and E25 and E26 trace paths that run past the labels
between their endpoints on purpose. Reading the report is part of the job.
"""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim import Arc, Circle, Dot, Ellipse, Rectangle, Text, ValueTracker

CONTAINERS = (Rectangle, Ellipse, Circle, Arc, Dot)

PAD = 0.03        # ignore text/text overlaps smaller than this
INSET = 0.16      # shrink a text box by this fraction before the stroke test


def leaves(m, texts, strokes):
 """Split a beat's mobject tree into labels and the strokes drawn around them."""
 if isinstance(m, Text):
  texts.append(m)
  return texts, strokes
 if not isinstance(m, CONTAINERS) and getattr(m, "points", None) is not None and len(m.points):
  strokes.append(m)
 for s in m.submobjects:
  leaves(s, texts, strokes)
 return texts, strokes


def box(m, inset=0.0):
 l, r = m.get_left()[0], m.get_right()[0]
 b, t = m.get_bottom()[1], m.get_top()[1]
 dx, dy = (r - l) * inset, (t - b) * inset
 return l + dx, r - dx, b + dy, t - dy


def hits_box(p, q, bx):
 """Does the segment p->q meet the box? Liang-Barsky, which is exact and
 cheap, and unlike a box test says no for a diagonal that misses."""
 l, r, b, t = bx
 x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
 dx, dy = x1 - x0, y1 - y0
 lo, hi = 0.0, 1.0
 for num, den in ((l - x0, dx), (x0 - r, -dx), (b - y0, dy), (y0 - t, -dy)):
  if den == 0:
   if num > 0:
    return False
   continue
  s = num / den
  if den > 0:
   lo = max(lo, s)
  else:
   hi = min(hi, s)
  if lo > hi:
   return False
 return True


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
   texts, strokes = [], []
   for m in fin:
    leaves(m, texts, strokes)
   for a in range(len(texts)):
    for b in range(a + 1, len(texts)):
     la, ra, ba, ta = box(texts[a])
     lb, rb, bb, tb = box(texts[b])
     ox, oy = min(ra, rb) - max(la, lb), min(ta, tb) - max(ba, bb)
     if ox > PAD and oy > PAD:
      bad += 1
      print(f"  {scene}{lang} beat {i:2d} text/text  "
            f"{texts[a].text[:16]!r} + {texts[b].text[:16]!r}  ({ox:.2f} x {oy:.2f})")
   for s in strokes:
    pts = s.get_anchors()
    sbx = box(s)
    for t in texts:
     tbx = box(t)
     if (sbx[0] <= tbx[0] and sbx[1] >= tbx[1]
         and sbx[2] <= tbx[2] and sbx[3] >= tbx[3]):
      continue                       # a container drawn around the label
     bx = box(t, INSET)
     if any(hits_box(pts[k], pts[k + 1], bx) for k in range(len(pts) - 1)):
      bad += 1
      print(f"  {scene}{lang} beat {i:2d} stroke/text "
            f"{type(s).__name__} through {t.text[:20]!r}")
      break
 print(f"{scene}: {bad} collisions")
 return bad


if __name__ == "__main__":
 sys.exit(1 if main(sys.argv[1], sys.argv[2]) else 0)
