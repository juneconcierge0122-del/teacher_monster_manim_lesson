"""advcalc E03 — Chapter 0, sections 7-9: functions, mappings, composition.

Everything here is arrows between two columns of dots, which is the one picture
that makes the whole section legible: a function is the relation whose arrows
never fork, and injective / surjective / bijective are three ways for that
arrow pattern to be special. Beat 3 reuses the book's own counterexample (Fig.
0.3): squaring is a function, and reversing its arrows forks at 4, so the
inverse is not. Beat 10 chains two of these panels into A -> B -> C.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN,
                                             FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# One column of dots is an ellipse with points down its middle. Everything sits
# in the animation band -1.90 <= y <= 1.30, so the columns are 2.0 tall.
COL_RX, COL_RY = 0.52, 1.02
CY = -0.28                                  # centre height of every column


class AdvCalcE03Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 3

 MODE_LABEL = {
  0: {"zh": "函數是一種特別的關係", "en": "a function is a special kind of relation"},
  1: {"zh": "主動的函數，被動的關係", "en": "the function active, the relation passive"},
  2: {"zh": "帶尾巴的箭頭記法", "en": "the stopped arrow notation"},
  3: {"zh": "反關係通常不是函數", "en": "the inverse is usually not a function"},
  4: {"zh": "從 A 到 B 的函數，隱含三件事", "en": "f from A to B implies three things"},
  5: {"zh": "嵌射、滿射、雙射", "en": "injective, surjective, bijective"},
  6: {"zh": "所有這種對象所成的集合", "en": "the set of all such objects"},
  7: {"zh": "有序三元組", "en": "the ordered triple"},
  8: {"zh": "為精確付出的代價；指標集合", "en": "the price of precision; indexed sets"},
  9: {"zh": "一般的笛卡兒積", "en": "the general Cartesian product"},
  10: {"zh": "合成、恆等、反映射", "en": "composition, the identity, the inverse"},
 }

 # ── the two-column picture ───────────────────────────────────────
 def _col(self, x, n, label, color):
  """An ellipse with n dots evenly down it. Returns (group, dot positions)."""
  ys = [CY + COL_RY * 0.62 * (1 - 2 * k / (n - 1)) for k in range(n)]
  g = VGroup(Ellipse(width=2 * COL_RX, height=2 * COL_RY, color=color, stroke_width=3)
             .move_to([x, CY, 0]),
             Text(label, font_size=FS_TAG, color=color).move_to([x, CY + COL_RY + 0.26, 0]))
  for y in ys:
   g.add(Dot([x, y, 0], radius=0.065, color=INK))
  return g, [[x, y, 0] for y in ys]

 def _map(self, xa, xb, na, nb, pairs, la="A", lb="B", ca=ACCENT_B, cb=ACCENT_C, arrow=ACCENT_A):
  """Two columns joined by the given (i, j) arrows."""
  ga, pa = self._col(xa, na, la, ca)
  gb, pb = self._col(xb, nb, lb, cb)
  g = VGroup(ga, gb)
  for i, j in pairs:
   g.add(self._arr([pa[i][0] + COL_RX * 0.55, pa[i][1], 0],
                   [pb[j][0] - COL_RX * 0.65, pb[j][1], 0], arrow, sw=2.5, tl=0.12))
  return g

 def _defn(self):
  """A function: arrows never fork. Beside it, a relation that does."""
  ok = self._map(-4.15, -1.95, 4, 4, [(0, 0), (1, 1), (2, 1), (3, 3)])
  bad = self._map(1.95, 4.15, 4, 4, [(0, 0), (1, 1), (1, 2), (3, 3)], arrow=WARN)
  return VGroup(ok, bad,
                self._mid(-1.62, "左：每個 x 恰好一個 y　　右：分岔，不是函數",
                          "left: exactly one y for each x    right: it forks, not a function",
                          DIM, FS_TAG, w=11.6))

 def _active(self):
  return VGroup(
   self._map(-3.90, -1.70, 4, 4, [(0, 0), (1, 1), (2, 1), (3, 3)]),
   self._mid(0.75, "函數作用在 x 上，給出一個值", "a function acts on x to give a value",
             ACCENT_A, FS_TAG, x=2.60, w=6.2),
   self._mid(0.05, "所以也常被叫做算子", "so it is often called an operator",
             DIM, FS_TAG, x=2.60, w=6.2),
   self._mid(-0.65, "一般的關係，配對比較被動", "a plain relation pairs more passively",
             DIM, FS_TAG, x=2.60, w=6.2))

 def _stopped(self):
  """Concrete pairings under the stopped arrow, chosen so that 2 and -2 both
  land on 4 -- which is exactly what makes the inverse fork in the next beat."""
  rows = ("1   ↦   1", "2   ↦   4", "3   ↦   9", "−2   ↦   4")
  g = VGroup(*[Text(s, font_size=FS_TAG + 2, color=WARN if k == 3 else ACCENT_A)
               .move_to([-2.70, 0.80 - 0.52 * k, 0]) for k, s in enumerate(rows)])
  return g.add(self._mid(0.60, "把每個數配上它的平方", "each number paired with its square",
                         DIM, FS_TAG, x=2.60, w=6.2),
               self._mid(-0.10, "定義域必須是清楚的", "the domain must be understood",
                         ACCENT_B, FS_TAG, x=2.60, w=6.2),
               self._mid(-1.55, "注意 2 與 −2 都對到 4", "note that 2 and −2 both land on 4",
                         WARN, FS_TAG, w=11.0))

 # Book Fig. 0.3, laid out by hand. The sideways parabola on the right is the
 # one that bites: it is symmetric about its own horizontal axis, so its axis
 # has to sit near the middle of the band or the lower branch runs straight
 # through the caption and into the subtitle.
 LP = (-3.30, -1.10, 0.95, 1.05)            # x0, y0, sx, sy for y = x^2
 RP = (1.15, -0.10, 0.75, 0.95)             # x0, y0, sy_up, sx_right for x = y^2
 TMAX = 1.30

 def _inverse(self):
  """Squaring, and its inverse forking at 4."""
  ts = np.linspace(-self.TMAX, self.TMAX, 90)
  lx, ly, lsx, lsy = self.LP
  rx, ry, rsy, rsx = self.RP
  left = self._curve([[lx + lsx * t, ly + lsy * t * t, 0] for t in ts], ACCENT_A, sw=3)
  right = self._curve([[rx + rsx * t * t, ry + rsy * t, 0] for t in ts], ACCENT_A, sw=3)
  xe, ye = rx + rsx * self.TMAX ** 2, rsy * self.TMAX
  return VGroup(
   self._arr([lx - 1.55, ly, 0], [lx + 1.55, ly, 0], DIM, sw=2.5, tl=0.12),
   self._arr([lx, ly - 0.25, 0], [lx, ly + 2.05, 0], DIM, sw=2.5, tl=0.12),
   left, Text("x ↦ x²", font_size=FS_TAG, color=ACCENT_A).move_to([lx, 1.14, 0]),
   self._arr([rx - 0.30, ry, 0], [rx + 2.45, ry, 0], DIM, sw=2.5, tl=0.12),
   self._arr([rx, ry - 1.20, 0], [rx, ry + 1.20, 0], DIM, sw=2.5, tl=0.12),
   right, Text("f ⁻¹", font_size=FS_TAG, color=WARN).move_to([rx + 2.90, ry + ye, 0]),
   Dot([xe, ry + ye, 0], radius=0.075, color=WARN),
   Dot([xe, ry - ye, 0], radius=0.075, color=WARN),
   self._mid(-1.62, "同一個 4 配上兩個值，所以反關係不是函數",
             "one 4 paired with two values, so the inverse is not a function",
             WARN, FS_TAG, w=11.6))

 def _triple(self):
  return VGroup(
   self._map(-3.60, -1.40, 4, 5, [(0, 0), (1, 1), (2, 2), (3, 3)]),
   self._mid(0.85, "f 是函數", "f is a function", DIM, FS_TAG, x=2.80, w=6.0),
   self._mid(0.25, "定義域正好是 A", "its domain is exactly A", DIM, FS_TAG, x=2.80, w=6.0),
   self._mid(-0.35, "值域包含於 B，B 叫上域", "its range lies in B, the codomain",
             ACCENT_A, FS_TAG, x=2.80, w=6.0))

 def _three(self):
  """Injective, surjective, bijective side by side.

  Each caption is placed under its own pair of columns rather than spaced
  inside one string: the padding that lines three Chinese words up leaves the
  three English words sitting between the panels instead of under them."""
  inj = self._map(-5.30, -3.60, 3, 5, [(0, 0), (1, 2), (2, 4)])
  sur = self._map(-0.85, 0.85, 4, 3, [(0, 0), (1, 1), (2, 1), (3, 2)])
  bij = self._map(3.60, 5.30, 4, 4, [(0, 0), (1, 1), (2, 2), (3, 3)])
  caps = [(-4.45, "嵌射", "injective"), (0.0, "滿射", "surjective"), (4.45, "雙射", "bijective")]
  return VGroup(inj, sur, bij,
                *[self._mid(-1.62, zh, en, ACCENT_A, FS_TAG, x=x, w=3.4)
                  for x, zh, en in caps])

 def _allsuch(self):
  return VGroup(
   Text("{ f  :  A → S }", font_size=FS_TAG + 4, color=ACCENT_A).move_to([0, 0.80, 0]),
   self._mid(0.10, "新對象一出現，就去看所有這種對象所成的集合",
             "once a new object appears, look at the set of all such objects",
             DIM, FS_TAG, w=11.0),
   Text("χ  :  S → { 0 , 1 }", font_size=FS_TAG + 2, color=ACCENT_B).move_to([0, -0.62, 0]),
   self._mid(-1.30, "子集對應到特徵函數，取值只有零與一",
             "subsets correspond to characteristic functions, values zero and one",
             ACCENT_B, FS_TAG, w=11.0))

 def _triples(self):
  """The two models for a triple, side by side (book p. 12).

  Restating the two displayed equations here would only copy the formula bar,
  so the picture carries what the bar has no room for: the nesting on the
  left, and the competing sequence reading on the right."""
  return VGroup(
   Rectangle(width=3.60, height=1.10, color=ACCENT_A, stroke_width=3).move_to([-3.20, 0.50, 0]),
   Rectangle(width=2.10, height=0.58, color=ACCENT_B, stroke_width=2).move_to([-3.72, 0.50, 0]),
   Text("⟨ x , y ⟩", font_size=FS_TAG, color=ACCENT_B).move_to([-3.72, 0.50, 0]),
   Text("z", font_size=FS_TAG, color=INK).move_to([-2.10, 0.50, 0]),
   self._mid(-0.35, "先配成對，再與第三個配對", "the first two paired, then paired with z",
             DIM, FS_TAG, x=-3.20, w=4.6),
   Text("{ ⟨1,x⟩ , ⟨2,y⟩ , ⟨3,z⟩ }", font_size=FS_TAG, color=ACCENT_C).move_to([3.10, 0.50, 0]),
   self._mid(-0.35, "或讀成長度 3 的序列", "or read as a sequence of length three",
             DIM, FS_TAG, x=3.10, w=4.6),
   self._mid(-1.20, "兩個模型一樣好用，但其實是不同的對象",
             "the two models serve equally well, yet are different objects",
             WARN, FS_TAG, w=11.4))

 def _indexed(self):
  g = VGroup(self._mid(0.90, "把其實不同的兩個對象視為同一，是為了精確付出的代價",
                       "identifying distinct objects is the price paid for precision",
                       DIM, FS_TAG, w=11.4))
  xs = [-3.30, -1.65, 0.0, 1.65, 3.30]
  for k, x in enumerate(xs):
   g.add(Dot([x, 0.15, 0], radius=0.07, color=ACCENT_C),
         Dot([x, -0.95, 0], radius=0.07, color=ACCENT_A),
         self._arr([x, 0.02, 0], [x, -0.82, 0], DIM, sw=2, tl=0.10),
         Text(f"i{k + 1}", font_size=FS_SMALL, color=ACCENT_C).move_to([x, 0.48, 0]))
  return g.add(self._mid(-1.50, "加了指標的集合，其實就是那個指標函數",
                         "an indexed set is really just the indexing function",
                         ACCENT_A, FS_TAG, w=11.4))

 def _product(self):
  return VGroup(
   Text("∏ Sᵢ   =   { f  :  dom f = I ,  f ( i ) ∈ Sᵢ }", font_size=FS_TAG + 3, color=ACCENT_A)
   .move_to([0, 0.55, 0]),
   self._mid(-0.30, "定義域是指標集 I", "the domain is the index set I", DIM, FS_TAG, w=10.0),
   self._mid(-1.05, "在每個 i 上取的值，落在對應的那個集合裡",
             "the value at each i lies in the corresponding set", ACCENT_B, FS_TAG, w=11.0))

 def _compose(self):
  """A -> B -> C, with the composite arrow underneath.

  Built as three columns rather than two overlapping `_map` calls: chaining
  those draws the middle column twice, so its ellipse doubles up and its label
  is rendered on top of itself. The columns are also shorter than elsewhere,
  to leave room for the composite arrow and the caption under it."""
  ry, cy = 0.85, -0.05
  xs = (-4.30, -0.60, 3.10)
  labels = ("A", "B", "C")
  colors = (ACCENT_B, ACCENT_C, ACCENT_B)
  g, pts = VGroup(), []
  for x, lab, col in zip(xs, labels, colors):
   ys = [cy + ry * 0.62 * (1 - 2 * k / 3) for k in range(4)]
   g.add(Ellipse(width=2 * COL_RX, height=2 * ry, color=col, stroke_width=3).move_to([x, cy, 0]),
         Text(lab, font_size=FS_TAG, color=col).move_to([x, cy + ry + 0.24, 0]))
   for y in ys:
    g.add(Dot([x, y, 0], radius=0.065, color=INK))
   pts.append([[x, y, 0] for y in ys])
  for (src, dst, pairs, col) in ((0, 1, [(0, 0), (1, 1), (2, 2), (3, 3)], ACCENT_A),
                                 (1, 2, [(0, 1), (1, 1), (2, 3), (3, 0)], ACCENT_C)):
   for i, j in pairs:
    g.add(self._arr([pts[src][i][0] + COL_RX * 0.55, pts[src][i][1], 0],
                    [pts[dst][j][0] - COL_RX * 0.65, pts[dst][j][1], 0], col, sw=2.5, tl=0.12))
  return g.add(self._arr([xs[0], -1.30, 0], [xs[2], -1.30, 0], ACCENT_A, sw=3, tl=0.16),
               Text("g ∘ f", font_size=FS_TAG, color=ACCENT_A).move_to([xs[1], -1.08, 0]),
               self._mid(-1.72, "有反映射，若且唯若是雙射",
                         "it has an inverse exactly when it is bijective",
                         ACCENT_A, FS_TAG, x=0.0, w=11.0))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  defn, act, stop, inv = self._defn(), self._active(), self._stopped(), self._inverse()
  tri, three = self._triple(), self._three()
  alls, trs, idx = self._allsuch(), self._triples(), self._indexed()
  prod, comp = self._product(), self._compose()

  return [([defn], []),                        # 0  what a function is
          ([act], [defn]),                     # 1  active vs passive
          ([stop], [act]),                     # 2  the stopped arrow
          ([inv], [stop]),                     # 3  the inverse forks
          ([tri], [inv]),                      # 4  f from A to B
          ([three], [tri]),                    # 5  inj, surj, bij
          ([alls], [three]),                   # 6  the set of all such
          ([trs], [alls]),                     # 7  ordered triples
          ([idx], [trs]),                      # 8  indexed sets
          ([prod], [idx]),                     # 9  the general product
          ([comp], [prod])]                    # 10 composition


AdvCalcE03ZH, AdvCalcE03EN = make(AdvCalcE03Base, "03", prefix="AdvCalcE")
