"""Array drawing shared by the advcalc episodes that put matrices on screen.

Section 4 of chapter 2 spends three episodes drawing the same few objects -- a
bracketed grid of dots, a bracketed column of labelled cells, a labelled box --
so they live here rather than in each lesson. Keeping one copy is not only
tidiness: E23's own notes record that a row of subscripts spelled out twice
drifts apart silently, and the same is true of a helper copied between files.

`_array` hands back the position function it drew with, so a beat that wants to
mark a row, a column or one entry asks for the coordinates the dots actually
went to instead of recomputing them from the same constants by hand.
"""
from manim import Dot, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import DIM, INK

FS_TAG = 17


class ArrayArt:
 """Mixin for CanonicalBase subclasses. Needs `_mid` from the base."""

 def _sym(self, y, s, color, size=FS_TAG, x=0.0, w=11.0):
  """A language independent line of symbols, scaled to fit like a caption."""
  return self._mid(y, s, s, color, size, x, w)

 def _brackets(self, x0, x1, y0, y1, color=DIM, d=0.16, sw=2.5):
  """The two square brackets around an array, drawn as three strokes each."""
  g = VGroup()
  for x, s in ((x0, d), (x1, -d)):
   g.add(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=sw),
         Line([x, y0, 0], [x + s, y0, 0], color=color, stroke_width=sw),
         Line([x, y1, 0], [x + s, y1, 0], color=color, stroke_width=sw))
  return g

 def _array(self, cx, cy, rows, cols, dx=0.55, dy=0.45, color=INK, r=0.055):
  """A dot array centred on (cx, cy), plus the brackets around it.

  Returns (group, pos) where pos(i, j) is the centre of the (i, j) dot."""
  x0 = cx - (cols - 1) * dx / 2
  y0 = cy + (rows - 1) * dy / 2
  pos = lambda i, j: [x0 + j * dx, y0 - i * dy, 0]
  g = VGroup(*[Dot(pos(i, j), radius=r, color=color)
               for i in range(rows) for j in range(cols)])
  g.add(self._brackets(x0 - 0.32, x0 + (cols - 1) * dx + 0.32,
                       y0 - (rows - 1) * dy - 0.22, y0 + 0.22))
  return g, pos

 def _column(self, cx, cy, entries, color=INK, dy=0.42, size=FS_TAG - 3):
  """A bracketed column of text cells, top entry first."""
  y0 = cy + (len(entries) - 1) * dy / 2
  g = VGroup(*[Text(s, font_size=size, color=c).move_to([cx, y0 - k * dy, 0])
               for k, (s, c) in enumerate((e if isinstance(e, tuple) else (e, color))
                                          for e in entries)])
  return g.add(self._brackets(cx - 0.34, cx + 0.34,
                              y0 - (len(entries) - 1) * dy - 0.20, y0 + 0.20))

 def _box(self, x, y, s, color, w=1.40, h=0.60, size=FS_TAG + 1):
  return VGroup(Rectangle(width=w, height=h, color=color, stroke_width=2.5).move_to([x, y, 0]),
                Text(s, font_size=size, color=color).move_to([x, y, 0]))
