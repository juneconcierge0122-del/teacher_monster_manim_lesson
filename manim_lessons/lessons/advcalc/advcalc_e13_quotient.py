"""advcalc E13 — Chapter 1, section 4 (book pp. 52-56): affine subspaces, the
quotient space, and Theorems 4.1 through 4.4.

The claim the section turns on is that a family of parallel lines is itself a
vector space, which sounds absurd until the set sum of two of them is drawn and
lands on a third line of the same family. Beats 6 and 7 do exactly that, and
beat 7 checks the arithmetic rather than asserting it: the sum line's offset is
computed from the two summands and compared against the family.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


class AdvCalcE13Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 13

 MODE_LABEL = {
  0: {"zh": "向量空間裡的「平面」", "en": "the planes in a vector space"},
  1: {"zh": "子空間平移過去，就是陪集", "en": "a subspace shifted: a coset"},
  2: {"zh": "要嘛相同，要嘛不交", "en": "identical or disjoint, never in between"},
  3: {"zh": "交集與集合和", "en": "intersections and set sums"},
  4: {"zh": "被線性映射送過去", "en": "carried by a linear map"},
  5: {"zh": "平移不是線性的", "en": "translation is not linear"},
  6: {"zh": "一族平行的直線", "en": "a family of parallel lines"},
  7: {"zh": "兩條相加，還是這一族裡的一條", "en": "two of them add to a third"},
  8: {"zh": "把向量送到它所在的那條", "en": "sending a vector to its own line"},
  9: {"zh": "有滿射就夠了", "en": "a surjection is enough"},
  10: {"zh": "穿過商空間分解", "en": "factoring through the quotient"},
 }

 # The direction and the step between cosets are sized against the whole
 # family: five lines have to fit the band, so the vertical cost is
 # 2 * half * D_y for one line plus 4 * OFF_y for the stack.
 D = np.array([1.70, 0.28, 0.0])
 OFF = np.array([-0.12, 0.55, 0.0])              # one step between parallel lines

 def _line(self, o, k, color, sw=3, half=1.10, dashed=False):
  a, b = o + k * self.OFF - half * self.D, o + k * self.OFF + half * self.D
  return self._dash(a, b, color, n=13) if dashed else Line(a, b, color=color, stroke_width=sw)

 def _planes(self):
  o = np.array([-2.05, -0.20, 0.0])
  g = VGroup()
  for k, col in ((0, ACCENT_B), (1, DIM), (-1, DIM)):
   g.add(self._line(o, k, col, sw=3.5 if k == 0 else 2.5))
  g.add(Dot(o, radius=0.065, color=INK),
        Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.26, -0.18, 0])),
        self._mid(1.10, "過原點的那一條是子空間", "the one through the origin is a subspace",
                  ACCENT_B, FS_TAG, x=2.55, w=5.8))
  return g.add(self._mid(0.20, "其他的都不是", "the others are not",
                         DIM, FS_TAG, x=2.55, w=5.8),
               self._mid(-0.60, "但它們都是「平面」", "but all of them are planes",
                         ACCENT_A, FS_TAG, x=2.55, w=5.8),
               self._mid(-1.62, "這一節問：平移、相交、被映射送過去之後會怎麼樣",
                         "the section asks what translation, intersection and images do to them",
                         DIM, FS_TAG, w=11.8))

 def _coset(self):
  o = np.array([-2.35, -0.45, 0.0])
  g = VGroup(self._line(o, 0, ACCENT_B, sw=3.5),
             self._line(o, 1, ACCENT_A, sw=3.5),
             Dot(o, radius=0.065, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.26, -0.18, 0])),
             Text("N", font_size=FS_TAG, color=ACCENT_B)
             .move_to(o - 1.05 * self.D + np.array([-0.10, -0.28, 0])),
             Dot(o + self.OFF, radius=0.075, color=ACCENT_A),
             Text("α", font_size=FS_TAG, color=ACCENT_A)
             .move_to(o + self.OFF + np.array([-0.28, 0.12, 0])),
             self._arr(o, o + self.OFF, ACCENT_A, sw=3, tl=0.14))
  return g.add(self._mid(1.10, "N 的每個元素都加上 α", "shift everything in N by alpha",
                         DIM, FS_TAG, x=2.85, w=5.6),
               self._mid(0.25, "得到含 α 的陪集", "and get the coset containing alpha",
                         ACCENT_A, FS_TAG, x=2.85, w=5.6),
               self._mid(-0.60, "也就是過 α 且平行於 N 的仿射子空間",
                         "the affine subspace through alpha parallel to N",
                         DIM, FS_TAG, x=2.85, w=5.6),
               self._mid(-1.62, "第二節說的「平面」，指的就是這種東西",
                         "these are what section two wanted to call planes",
                         DIM, FS_TAG, w=11.6))

 def _disjoint(self):
  """Two points on one line share a coset; a point on another has a coset
  that misses it entirely. There is no third possibility."""
  o = np.array([-2.35, -0.35, 0.0])
  g = VGroup()
  for k, col in ((0, DIM), (1, ACCENT_A), (2, ACCENT_C)):
   g.add(self._line(o, k, col, sw=3 if k else 2.5))
  for f, k, lab, col in ((-0.55, 1, "α", ACCENT_A), (0.62, 1, "γ", ACCENT_A),
                         (0.10, 2, "β", ACCENT_C)):
   p = o + k * self.OFF + f * self.D
   g.add(Dot(p, radius=0.08, color=col),
         Text(lab, font_size=FS_TAG, color=col).move_to(p + np.array([-0.06, 0.30, 0])))
  return g.add(self._mid(1.10, "α 與 γ 在同一條上", "alpha and gamma on one line",
                         ACCENT_A, FS_TAG, x=3.05, w=5.4),
               self._mid(0.25, "所以它們的陪集是同一個", "so their cosets are the same one",
                         DIM, FS_TAG, x=3.05, w=5.4),
               self._mid(-0.60, "β 的那一條完全碰不到", "beta's misses theirs entirely",
                         ACCENT_C, FS_TAG, x=3.05, w=5.4),
               self._mid(-1.62, "這正是第零章那個等價關係：差落在 N 裡就等價",
                         "this is chapter zero's equivalence relation: equivalent when the difference lies in N",
                         DIM, FS_TAG, w=11.8))

 def _ops(self):
  """Two affine subspaces meeting in a smaller affine subspace, beside two
  adding to a bigger one."""
  g = VGroup()
  o1 = np.array([-3.35, -0.30, 0.0])
  d2 = np.array([1.05, -0.95, 0.0])
  g.add(Line(o1 - 1.15 * self.D, o1 + 1.15 * self.D, color=ACCENT_B, stroke_width=3),
        Line(o1 - 1.05 * d2, o1 + 1.05 * d2, color=ACCENT_C, stroke_width=3),
        Dot(o1, radius=0.09, color=ACCENT_A),
        self._mid(1.10, "交集：空的，或還是仿射", "the intersection: empty, or affine again",
                  DIM, FS_TAG, x=-3.35, w=4.6))
  o2 = np.array([2.55, -0.30, 0.0])
  quad = [o2 + sx * 1.25 * self.D / 2 + sy * 0.95 * d2 / 2
          for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  g.add(Polygon(*quad, color=ACCENT_A, stroke_width=2.5,
                fill_color=ACCENT_A, fill_opacity=0.13),
        Line(o2 - 0.62 * self.D, o2 + 0.62 * self.D, color=ACCENT_B, stroke_width=3),
        Line(o2 - 0.55 * d2, o2 + 0.55 * d2, color=ACCENT_C, stroke_width=3),
        self._mid(1.10, "集合和：還是仿射", "the set sum: affine again",
                  DIM, FS_TAG, x=2.55, w=4.6))
  return g.add(self._mid(-1.62, "任意多個的交集也一樣：要嘛是空的，要嘛還是仿射子空間",
                         "any family intersects to the empty set or to an affine subspace",
                         DIM, FS_TAG, w=11.8))

 def _under_T(self):
  g = VGroup()
  o1 = np.array([-3.85, -0.20, 0.0])
  g.add(Ellipse(width=3.05, height=2.30, color=DIM, stroke_width=2).move_to([-3.85, -0.05, 0]),
        Line(o1 - 0.75 * self.D, o1 + 0.75 * self.D, color=ACCENT_A, stroke_width=3.5),
        Text("V", font_size=FS_TAG, color=DIM).move_to([-3.85, 1.15, 0]))
  o2 = np.array([2.35, -0.20, 0.0])
  d = np.array([1.30, -0.20, 0.0])
  g.add(Ellipse(width=3.05, height=2.30, color=DIM, stroke_width=2).move_to([2.35, -0.05, 0]),
        Line(o2 - 0.72 * d, o2 + 0.72 * d, color=ACCENT_A, stroke_width=3.5),
        Text("W", font_size=FS_TAG, color=DIM).move_to([2.35, 1.15, 0]),
        self._arr([-2.15, -0.05, 0], [0.65, -0.05, 0], ACCENT_A, sw=3, tl=0.16),
        Text("T", font_size=FS_TAG + 2, color=ACCENT_A).move_to([-0.75, 0.28, 0]))
  return g.add(self._mid(-1.05, "線性映射把仿射子空間送到仿射子空間",
                         "a linear map carries an affine subspace to an affine subspace",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.68, "反過來，原像要嘛是空的，要嘛還是仿射子空間",
                         "and a preimage is either empty or an affine subspace",
                         DIM, FS_TAG, w=11.6))

 def _not_linear(self):
  o = np.array([-2.55, -0.55, 0.0])
  sh = np.array([1.05, 1.15, 0.0])
  g = VGroup(Dot(o, radius=0.075, color=INK),
             Text("0", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.26, -0.20, 0])),
             self._arr(o, o + sh, ACCENT_A, sw=3.5, tl=0.16),
             Dot(o + sh, radius=0.085, color=ACCENT_A),
             Text("α", font_size=FS_TAG, color=ACCENT_A)
             .move_to(o + sh + np.array([0.26, 0.14, 0])),
             Text("Sα ( 0 )  =  α  ≠  0", font_size=FS_TAG + 1, color=WARN)
             .move_to([1.75, 0.35, 0]))
  return g.add(self._mid(-0.45, "零沒有被送到零", "zero is not carried to zero",
                         WARN, FS_TAG, x=1.75, w=5.2),
               self._mid(-1.05, "所以平移不是線性的", "so translation is not linear",
                         DIM, FS_TAG, x=1.75, w=5.2),
               self._mid(-1.68, "但它確實把仿射子空間送到仿射子空間；線性映射後面接一個平移，就叫仿射變換",
                         "it does carry affine subspaces to affine subspaces; linear then translated is an affine transformation",
                         DIM, FS_TAG, w=11.9))

 # ── beats 6-8: the family of parallel lines is a vector space ────
 FAM = (-2, -1, 0, 1, 2)

 def _family(self):
  o = np.array([-2.15, -0.30, 0.0])
  g = VGroup()
  for k in self.FAM:
   g.add(self._line(o, k, ACCENT_B if k == 0 else DIM, sw=3.5 if k == 0 else 2.5, half=1.15))
  g.add(Dot(o, radius=0.065, color=INK),
        Text("N", font_size=FS_TAG, color=ACCENT_B)
        .move_to(o - 0.95 * self.D + np.array([-0.14, -0.26, 0])))
  return g.add(self._mid(1.10, "固定一個子空間", "fix one subspace",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(0.25, "看它所有的平移", "and look at all its translates",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.60, "得到一族平行的直線", "you get a family of parallel lines",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.62, "這些平移把整個空間纖維化",
                         "these translates fiber the whole space",
                         DIM, FS_TAG, w=11.6))

 def _sum_of_lines(self):
  """The set sum of the coset at level 1 and the coset at level -2 is the
  coset at level -1. The level is computed, not assumed."""
  ka, kb = 1, -2
  ks = ka + kb
  assert ks in self.FAM, "the sum must land on a line that is actually drawn"
  o = np.array([-2.15, -0.30, 0.0])
  g = VGroup()
  for k in self.FAM:
   col = {ka: ACCENT_B, kb: ACCENT_C, ks: ACCENT_A}.get(k, GHOST)
   g.add(self._line(o, k, col, sw=3.5 if k in (ka, kb, ks) else 1.8, half=1.15))
  pa = o + ka * self.OFF - 0.35 * self.D
  pb = o + kb * self.OFF + 0.15 * self.D
  ps = pa + (pb - o)
  g.add(Dot(pa, radius=0.08, color=ACCENT_B), Dot(pb, radius=0.08, color=ACCENT_C),
        Dot(ps, radius=0.09, color=ACCENT_A),
        self._dash(pa, ps, GHOST, n=7), self._dash(pb, ps, GHOST, n=7))
  return g.add(self._mid(1.10, "從兩條各取一個點", "take one point from each line",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(0.25, "相加", "and add them", DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.60, "落點永遠在同一條上", "the result always lands on one line",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.62, "所以這一族平行直線，自己就構成一個向量空間",
                         "so this family of parallel lines is itself a vector space",
                         ACCENT_A, FS_TAG, w=11.8))

 def _projection(self):
  o = np.array([-3.30, -0.30, 0.0])
  g = VGroup()
  cols = (ACCENT_C, ACCENT_A, ACCENT_B, WARN, ACCENT_C)
  for j, k in enumerate(self.FAM):
   g.add(self._line(o, k, cols[j], sw=3, half=0.95),
         Dot([1.85, o[1] + k * 0.40, 0], radius=0.075, color=cols[j]),
         self._arr([o[0] + 0.95 * self.D[0] + k * self.OFF[0] + 0.16,
                    o[1] + 0.95 * self.D[1] + k * self.OFF[1], 0],
                   [1.65, o[1] + k * 0.40, 0], cols[j], sw=1.8, tl=0.09))
  g.add(Text("V", font_size=FS_TAG, color=DIM).move_to([-3.60, 1.08, 0]),
        Text("V / N", font_size=FS_TAG, color=DIM).move_to([1.85, 1.08, 0]))
  return g.add(self._mid(0.35, "每個向量送到它所在的那條線",
                         "each vector goes to the line it lies on",
                         DIM, FS_TAG, x=4.15, w=3.7),
               self._mid(-0.60, "這個映射保持加法與數乘",
                         "and this map preserves both operations",
                         ACCENT_A, FS_TAG, x=4.15, w=3.7),
               self._mid(-1.62, "只有乘以零那一種要另外規定成 N 本身",
                         "only multiplication by zero needs a separate stipulation",
                         DIM, FS_TAG, w=11.6))

 def _thm41(self):
  g = VGroup(Ellipse(width=2.60, height=1.85, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.10).move_to([-3.35, 0.10, 0]),
             self._mid(0.10, "向量空間", "a vector space", ACCENT_B, FS_TAG, x=-3.35, w=2.3),
             self._arr([-1.95, 0.10, 0], [-0.35, 0.10, 0], ACCENT_A, sw=3, tl=0.15),
             self._mid(0.55, "滿射，而且保持運算", "onto, and preserving the operations",
                       ACCENT_A, FS_TAG, x=-1.15, w=3.4),
             Ellipse(width=2.60, height=1.85, color=DIM, stroke_width=2.5)
             .move_to([1.05, 0.10, 0]),
             self._mid(0.10, "兩個像運算的運算", "two vectorlike operations",
                       DIM, FS_TAG, x=1.05, w=2.4),
             self._arr([2.45, 0.10, 0], [3.35, 0.10, 0], ACCENT_A, sw=2.5, tl=0.13),
             self._mid(0.10, "也是向量空間", "also a vector space",
                       ACCENT_A, FS_TAG, x=4.65, w=2.6))
  return g.add(self._mid(-1.05, "省下逐條檢查八條公理的工夫",
                         "which saves checking all eight axioms by hand",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.68, "所以商空間是向量空間，而投影是滿的線性映射",
                         "so the quotient is a vector space and the projection is a surjective linear map",
                         ACCENT_A, FS_TAG, w=11.8))

 def _factor(self):
  g = VGroup(Rectangle(width=1.30, height=0.68, color=ACCENT_B, stroke_width=2.5)
             .move_to([-3.55, 0.70, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-3.55, 0.70, 0]),
             Rectangle(width=1.30, height=0.68, color=ACCENT_A, stroke_width=2.5)
             .move_to([1.35, 0.70, 0]),
             Text("W", font_size=FS_TAG + 2, color=ACCENT_A).move_to([1.35, 0.70, 0]),
             Rectangle(width=1.75, height=0.68, color=ACCENT_C, stroke_width=2.5)
             .move_to([-1.10, -0.70, 0]),
             Text("V / M", font_size=FS_TAG + 1, color=ACCENT_C).move_to([-1.10, -0.70, 0]),
             self._arr([-2.85, 0.70, 0], [0.65, 0.70, 0], ACCENT_A, sw=3, tl=0.15),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-1.10, 1.02, 0]),
             self._arr([-3.40, 0.32, 0], [-1.60, -0.42, 0], ACCENT_C, sw=2.5, tl=0.13),
             Text("π", font_size=FS_TAG, color=ACCENT_C).move_to([-2.75, -0.20, 0]),
             self._arr([-0.45, -0.48, 0], [1.15, 0.30, 0], ACCENT_C, sw=2.5, tl=0.13),
             Text("S", font_size=FS_TAG, color=ACCENT_C).move_to([0.62, -0.24, 0]))
  return g.add(self._mid(0.70, "零空間包含 M 時", "when the null space includes M",
                         DIM, FS_TAG, x=4.15, w=3.6),
               self._mid(-0.70, "就能唯一地繞這一圈", "the detour is unique",
                         ACCENT_C, FS_TAG, x=4.15, w=3.6),
               self._mid(-1.62, "另外，子空間被 T 送進自己時，商空間上也有唯一一個相容的映射",
                         "and if a subspace is carried into itself, a unique matching map exists on the quotient",
                         DIM, FS_TAG, w=11.9))

 def stage(self):
  pl, cs, dj = self._planes(), self._coset(), self._disjoint()
  op, ut, nl = self._ops(), self._under_T(), self._not_linear()
  fm, sl, pj = self._family(), self._sum_of_lines(), self._projection()
  t41, fc = self._thm41(), self._factor()

  return [([pl], []), ([cs], [pl]), ([dj], [cs]), ([op], [dj]),
          ([ut], [op]), ([nl], [ut]), ([fm], [nl]), ([sl], [fm]),
          ([pj], [sl]), ([t41], [pj]), ([fc], [t41])]


AdvCalcE13ZH, AdvCalcE13EN = make(AdvCalcE13Base, "13", prefix="AdvCalcE")
