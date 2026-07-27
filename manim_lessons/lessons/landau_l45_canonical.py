"""Lesson 45 — Canonical transformations (Landau §45).

One picture carries the whole lesson: two phase planes side by side, with a
marked cell in the old one and its image in the new one. A point transformation
moves the cell horizontally only, because it touches q alone; a canonical
transformation tilts and slides it, because it mixes q with p; and the last
beat rotates it by a right angle, which is the transformation that simply
renames the momentum a coordinate.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Polygon, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

OL = np.array([-5.20, -0.10, 0.0])          # centre of the old phase plane
NW = np.array([-1.35, -0.10, 0.0])          # centre of the new phase plane
SC = 0.62                                   # units per phase-space unit
CELL = ((-0.7, -0.7), (0.7, -0.7), (0.7, 0.7), (-0.7, 0.7))


def _pt(o, x, y):
 return o + SC * np.array([x, y, 0.0])


class CanonicalBase45(CanonicalBase):
 EPISODE = 45
 MODE_LABEL = {0: {"zh": "只換座標：點變換", "en": "coordinates only: a point transformation"},
               1: {"zh": "動量和座標地位平等", "en": "momenta and coordinates rank equally"},
               2: {"zh": "把全部 2s 個變數一起換",
                   "en": "transform all two s variables together"},
               3: {"zh": "要求新變數也滿足哈密頓方程",
                   "en": "demand Hamilton's equations in the new variables"},
               4: {"zh": "被積函數只能差一個全微分",
                   "en": "the integrands may differ only by a total differential"},
               5: {"zh": "生成函數 F ( q , Q , t )", "en": "the generating function F ( q , Q , t )"},
               # no label on beat 6: its formula is already two lines, and a third
               # would drop the block's bottom edge to y = 1.40, onto the picture.
               7: {"zh": "生成函數不含時間時", "en": "when it carries no time"},
               8: {"zh": "座標與動量只差一個名字",
                   "en": "coordinate and momentum differ only in name"},
               9: {"zh": "用帕松括號寫出正則的條件",
                   "en": "the canonical condition in Poisson brackets"}}

 # ── the moving cell ───────────────────────────────────────────────
 def _map(self, x, y):
  """Where the old cell corner (x, y) lands, for the current beat's mode."""
  if self.mode == "point":                  # Q = Q(q): p is dragged along
   return 0.72 * x + 0.30, y / 0.72
  if self.mode == "swap":                   # Q = p, P = -q: a right angle
   a = 0.5 * PI * min(1.0, self._tau() / 2.4)
   c, s = np.cos(a), np.sin(a)
   return c * x - s * y, s * x + c * y
  return 0.86 * x + 0.42 * y, (y - 0.34 * x) / 0.86   # a shear: area preserved

 def _cell(self, o, mapped):
  pts = [_pt(o, *(self._map(x, y) if mapped else (x, y))) for x, y in CELL]
  return Polygon(*pts, color=ACCENT_C if mapped else ACCENT_B, stroke_width=4,
                 fill_opacity=0.16, fill_color=ACCENT_C if mapped else ACCENT_B)

 def stage(self):
  self.mode = "point"
  axL = self._axes(OL, "q", "p", w=1.38, h=1.05)
  axR = self._axes(NW, "Q", "P", w=1.38, h=1.05)
  cellL = self._cell(OL, False)
  cellR = always_redraw(lambda: self._cell(NW, True))
  # Below the planes: at centre height the arrow would sit on the q axis and its
  # label, and the two planes leave only a 1.1-unit gap there anyway.
  arrow = VGroup(self._arr(OL + np.array([1.62, -1.02, 0]), NW + np.array([-1.62, -1.02, 0]),
                           WARN, sw=4, tl=0.16),
                 self._mid(OL[1] - 1.38, "正則變換", "canonical", WARN, FS_SMALL,
                           x=0.5 * (OL[0] + NW[0]), w=2.2))
  heads = VGroup(self._mid(1.42, "舊變數", "old variables", ACCENT_B, FS_SMALL, x=OL[0], w=2.6),
                 self._mid(1.42, "新變數", "new variables", ACCENT_C, FS_SMALL, x=NW[0], w=2.6))
  arealab = self._mid(-1.62, "面積不變：這正是下一課的劉維定理",
                      "the area is unchanged, which is the next lesson", DIM, FS_SMALL,
                      x=-3.25, w=5.6)

  c0 = VGroup(self._row(0.95, "座標怎麼選都可以", "any coordinates will do", DIM),
              self._row(0.25, "拉格朗日方程形式不變",
                        "Lagrange's equations keep their form", ACCENT_B),
              self._row(-0.45, "這叫點變換", "this is a point transformation", ACCENT_C))
  c1 = VGroup(self._row(0.95, "哈密頓方程也不變",
                        "Hamilton's equations are unchanged too", DIM),
              self._row(0.25, "但它允許更廣的變換",
                        "but they allow far more than that", ACCENT_C))
  c2 = VGroup(self._row(0.95, "Q 和 P 都可以依賴 q 與 p",
                        "Q and P may both depend on q and p", ACCENT_A),
              self._row(0.25, "這是哈密頓寫法的一大好處",
                        "an important advantage of the treatment", DIM))
  c3 = VGroup(self._row(0.95, "不是每個變換都保持正則",
                        "not every transformation stays canonical", WARN),
              self._row(0.25, "條件是什麼？", "what is the condition?", DIM))
  c4 = VGroup(self._row(0.95, "差別只是端點上的常數",
                        "the difference is a constant at the ends", DIM),
              self._row(0.25, "不影響變分", "which cannot affect the variation", ACCENT_B),
              self._row(-0.45, "F 就是生成函數", "F is the generating function", ACCENT_A))
  c5 = VGroup(self._row(0.95, "p = ∂F/∂q", "p = ∂F/∂q", ACCENT_A, FS_BODY),
              self._row(0.25, "P = − ∂F/∂Q", "P = − ∂F/∂Q", ACCENT_B, FS_BODY),
              self._row(-0.45, "H′ = H + ∂F/∂t", "H′ = H + ∂F/∂t", ACCENT_C, FS_BODY))
  c6 = VGroup(self._row(0.95, "做一次勒讓德變換", "one Legendre transformation", DIM),
              self._row(0.25, "p = ∂Φ/∂q  ,  Q = ∂Φ/∂P", "p = ∂Φ/∂q  ,  Q = ∂Φ/∂P",
                        ACCENT_A, FS_BODY))
  c7 = VGroup(self._row(0.95, "H′ − H = ∂F/∂t", "H′ − H = ∂F/∂t", ACCENT_C, FS_BODY),
              self._row(0.25, "不含時間就直接代換",
                        "with no time, just substitute", DIM))
  c8 = VGroup(self._row(0.95, "Q = p , P = − q", "Q = p , P = − q", WARN, FS_BODY),
              self._row(0.25, "只是把兩者對調", "simply interchanges the two", DIM),
              self._row(-0.45, "所以叫正則共軛量",
                        "hence: canonically conjugate", ACCENT_A))
  c9 = VGroup(self._row(0.95, "帕松括號在正則變換下不變",
                        "brackets are invariant under them", ACCENT_B),
              self._row(0.25, "[ Q , Q ] = 0 , [ P , P ] = 0",
                        "[ Q , Q ] = 0 , [ P , P ] = 0", DIM),
              self._row(-0.45, "[ P , Q ] = δ", "[ P , Q ] = δ", ACCENT_A, FS_BODY),
              self._row(-1.15, "運動本身也是一串正則變換",
                        "the motion is itself a chain of them", ACCENT_C))

  def mode(m):
   return lambda: setattr(self, "mode", m)

  return [([axL, axR, cellL, cellR, arrow, heads, c0], []),
          ([c1], [c0]),
          ([c2], [c1], mode("shear")),
          ([c3], [c2]),
          ([c4], [c3]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([c7], [c6]),
          ([c8], [c7], mode("swap")),
          ([arealab, c9], [c8])]


LandauL45ZH, LandauL45EN = make(CanonicalBase45, 45)
