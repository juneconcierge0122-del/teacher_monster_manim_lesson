"""advcalc E02 — Chapter 0, sections 4-6: sets, restricted variables, relations.

Three pictures carry the episode. Beats 0-4 are set diagrams: membership, the
two-way inclusion that is how set identity actually gets proved, and the empty
set. Beats 5-7 are restricted variables, drawn as a domain the variable is
confined to, with the two unfoldings side by side -- the universal one uses
implication and the existential one uses `and`, which is the trap the book
points at. Beats 8-10 build the Cartesian plane: an ordered pair as a point,
then A x B as a grid, then a relation as a scatter of points inside it with its
domain and range projected onto the axes.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Circle, Dot, Ellipse, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# The plane for beats 8-10, kept inside the animation band -1.90 <= y <= 1.30.
# PY0 is set so the `dom R` label under the axis (PY0 - 0.40) clears -1.90, and
# PH so the y-axis tip (PY0 + PH + 0.35) stays under 1.30.
PX0, PY0 = -1.30, -1.35                     # origin of the axes
PW, PH = 3.60, 2.25                         # extent of the drawn quadrant
RIGHT_X, RIGHT_W = 4.40, 3.60               # the caption column beside the plane


class AdvCalcE02Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 2

 MODE_LABEL = {
  0: {"zh": "集合與成員", "en": "sets and membership"},
  1: {"zh": "兩個集合什麼時候是同一個", "en": "when two sets are the same object"},
  2: {"zh": "子集與包含", "en": "subsets and inclusion"},
  3: {"zh": "怎麼指定一個集合", "en": "how a set gets specified"},
  4: {"zh": "空集", "en": "the empty set"},
  5: {"zh": "受限變數與定義域", "en": "restricted variables and the domain"},
  6: {"zh": "受限量詞", "en": "restricted quantifiers"},
  7: {"zh": "展開成無限制變數", "en": "unfolding into unrestricted variables"},
  8: {"zh": "有序對", "en": "ordered pairs"},
  9: {"zh": "關係就是一組有序對", "en": "a relation is simply a set of ordered pairs"},
  10: {"zh": "定義域、值域、笛卡兒積", "en": "domain, range, the Cartesian product"},
 }

 # ── set diagrams ─────────────────────────────────────────────────
 def _blob(self, c, r, color, label):
  return VGroup(Circle(radius=r, color=color, stroke_width=3).move_to(c),
                Text(label, font_size=FS_TAG, color=color).move_to(
                    [c[0], c[1] + r + 0.24, 0]))

 def _members(self):
  pts = [(-3.30, 0.10), (-2.70, 0.42), (-2.60, -0.30), (-3.05, -0.52)]
  g = self._blob([-2.90, 0.0, 0], 1.05, ACCENT_B, "A")
  for p in pts:
   g.add(Dot([p[0], p[1], 0], radius=0.07, color=ACCENT_A))
  g.add(Dot([-0.30, 0.10, 0], radius=0.07, color=DIM),
        Text("x", font_size=FS_SMALL, color=DIM).move_to([-0.30, -0.22, 0]),
        self._mid(-1.45, "元素、成員；屬於的符號", "elements, members; the membership symbol",
                  DIM, FS_TAG, w=10.0))
  return g

 def _equality(self):
  return VGroup(
   self._blob([-2.30, 0.05, 0], 1.00, ACCENT_B, "A"),
   self._blob([2.30, 0.05, 0], 1.00, ACCENT_C, "B"),
   self._mid(-1.35, "成員完全相同，就是同一個對象",
             "exactly the same members means the same object", ACCENT_A, FS_TAG, w=10.4),
   Text("=", font_size=FS_TAG + 6, color=ACCENT_A).move_to([0, 0.05, 0]))

 def _inclusion(self):
  """The two-way inclusion, because that is how equality gets proved."""
  return VGroup(
   Circle(radius=1.18, color=ACCENT_C, stroke_width=3).move_to([-2.40, 0.05, 0]),
   Circle(radius=0.62, color=ACCENT_B, stroke_width=3).move_to([-2.62, -0.05, 0]),
   Text("B", font_size=FS_TAG, color=ACCENT_C).move_to([-2.40, 1.47, 0]),
   Text("A", font_size=FS_TAG, color=ACCENT_B).move_to([-2.62, -0.05, 0]),
   self._mid(0.55, "A 包含於 B，而且 B 包含於 A", "A included in B, and B included in A",
             ACCENT_A, FS_TAG, x=2.30, w=6.4),
   self._mid(-0.30, "就是證明兩個集合相等的辦法", "that is how set identity is established",
             DIM, FS_TAG, x=2.30, w=6.4))

 def _specify(self):
  rows = ("{ 1 , 4 , 7 }", "{ x }", "{ x , y }", "{ x : P ( x ) }")
  g = VGroup(*[Text(s, font_size=FS_TAG, color=ACCENT_A).move_to([-3.40, 0.95 - 0.62 * k, 0])
               for k, s in enumerate(rows)])
  return g.add(self._mid(0.30, "{ x : x² < 9 }  =  ( −3 , 3 )", "{ x : x² < 9 }  =  ( −3 , 3 )",
                         ACCENT_B, FS_TAG + 3, x=2.40, w=6.0),
               self._mid(-0.55, "無限集通常用敘述框架定義",
                         "infinite sets are defined by statement frames", DIM, FS_TAG, x=2.40, w=6.0))

 def _empty(self):
  return VGroup(
   Circle(radius=0.85, color=WARN, stroke_width=3).move_to([-2.60, 0.15, 0]),
   Text("∅", font_size=FS_TAG + 8, color=WARN).move_to([-2.60, 0.15, 0]),
   self._mid(0.55, "就像算術裡需要零一樣", "needed much as arithmetic needs zero",
             DIM, FS_TAG, x=2.20, w=6.6),
   Text("4 = { 0 , 1 , 2 , 3 }", font_size=FS_TAG, color=ACCENT_A).move_to([2.20, -0.10, 0]),
   Text("1 = { 0 }        0 = ∅", font_size=FS_TAG, color=ACCENT_A).move_to([2.20, -0.70, 0]))

 # ── restricted variables ─────────────────────────────────────────
 def _domain(self):
  return VGroup(
   Rectangle(width=3.40, height=1.30, color=ACCENT_C, stroke_width=3).move_to([-2.60, 0.20, 0]),
   Text("ℤ", font_size=FS_TAG + 6, color=ACCENT_C).move_to([-2.60, 0.20, 0]),
   self._mid(0.60, "變數不能拿任意對象當值", "a variable may not take all objects as values",
             DIM, FS_TAG, x=2.40, w=6.4),
   self._mid(-0.15, "它只能取某個集合裡的成員", "only members of a certain set, its domain",
             ACCENT_A, FS_TAG, x=2.40, w=6.4))

 def _restricted(self):
  """The restriction drawn rather than restated: the quantifier reaches only
  into the domain, not into everything. Repeating the two displayed lines
  here would just copy the formula bar above."""
  g = VGroup(
   Ellipse(width=8.60, height=2.60, color=GHOST, stroke_width=2).move_to([-0.60, 0.10, 0]),
   self._mid(1.02, "所有對象", "all objects", DIM, FS_TAG, x=-0.60, w=4.0),
   Rectangle(width=3.10, height=1.32, color=ACCENT_C, stroke_width=3).move_to([-0.60, -0.02, 0]),
   Text("ℤ", font_size=FS_TAG + 8, color=ACCENT_C).move_to([-1.75, -0.02, 0]))
  for k in range(5):
   g.add(Dot([-1.05 + 0.42 * k, -0.02, 0], radius=0.065, color=INK))
  # The caption is short on purpose: anything longer gets shrunk by `_mid` to
  # fit between the ellipse edge (x = 3.70) and the safe right edge.
  return g.add(self._arr([4.55, 0.62, 0], [0.98, 0.06, 0], ACCENT_A, sw=3, tl=0.14),
               self._mid(0.92, "只伸進定義域", "only into the domain",
                         ACCENT_A, FS_TAG, x=4.75, w=3.0),
               self._mid(-1.40, "這裡的屬於符號要讀成介系詞「在」",
                         "the membership symbol is read here as the preposition in",
                         DIM, FS_TAG, w=11.0))

 def _unfold(self):
  """The trap, as the contrast between the two connectives, plus the third
  displayed line on book p. 8 -- the one the formula bar has no room for."""
  # Boxed pairs rather than two bare glyphs: at any font size the arrow and the
  # ampersand carry little visual mass, and the pairing (which quantifier goes
  # with which connective) is the actual content of the beat.
  return VGroup(
   Rectangle(width=4.30, height=1.30, color=ACCENT_B, stroke_width=3).move_to([-2.70, 0.80, 0]),
   Text("∀      ⇒", font_size=FS_TAG + 22, color=ACCENT_B).move_to([-2.70, 0.80, 0]),
   Rectangle(width=4.30, height=1.30, color=ACCENT_C, stroke_width=3).move_to([2.70, 0.80, 0]),
   Text("∃      &", font_size=FS_TAG + 22, color=ACCENT_C).move_to([2.70, 0.80, 0]),
   self._mid(-0.10, "全稱：用蘊涵", "universal: implication", ACCENT_B, FS_TAG, x=-2.70, w=4.4),
   self._mid(-0.10, "存在：用而且", "existential: and", ACCENT_C, FS_TAG, x=2.70, w=4.4),
   Text("{ x ∈ A : P }   =   { x : x ∈ A  &  P }", font_size=FS_TAG + 2, color=ACCENT_A)
   .move_to([0, -0.78, 0]),
   self._mid(-1.45, "受限的集合寫法也一樣展開", "restricted set formation unfolds the same way",
             DIM, FS_TAG, w=11.0))

 # ── the plane ────────────────────────────────────────────────────
 def _axes(self):
  return VGroup(self._arr([PX0 - 0.25, PY0, 0], [PX0 + PW + 0.35, PY0, 0], DIM, sw=3, tl=0.14),
                self._arr([PX0, PY0 - 0.20, 0], [PX0, PY0 + PH + 0.35, 0], DIM, sw=3, tl=0.14))

 def _pair(self):
  x, y = PX0 + 2.10, PY0 + 1.55
  return VGroup(
   self._axes(),
   self._dash([x, PY0, 0], [x, y, 0], GHOST, n=7), self._dash([PX0, y, 0], [x, y, 0], GHOST, n=9),
   Dot([x, y, 0], radius=0.09, color=ACCENT_A),
   Text("⟨ x , y ⟩", font_size=FS_TAG, color=ACCENT_A).move_to([x + 0.95, y + 0.22, 0]),
   self._mid(0.85, "⟨ 1 , 3 ⟩   ≠   ⟨ 3 , 1 ⟩", "⟨ 1 , 3 ⟩   ≠   ⟨ 3 , 1 ⟩",
             WARN, FS_TAG + 3, x=RIGHT_X, w=RIGHT_W),
   self._mid(0.05, "順序是關鍵性質", "the order is crucial",
             DIM, FS_TAG, x=RIGHT_X, w=RIGHT_W))

 def _relation(self):
  """A relation drawn as what it is: a set of points in the plane."""
  pts = [(0.55, 0.50), (0.95, 1.35), (1.60, 0.85), (2.05, 1.95),
         (2.55, 0.40), (2.95, 1.55), (1.25, 2.15)]
  g = VGroup(self._axes())
  for u, v in pts:
   g.add(Dot([PX0 + u, PY0 + v, 0], radius=0.08, color=ACCENT_A))
  return g.add(self._mid(0.85, "關係就是它的圖形", "the relation is its graph",
                         ACCENT_A, FS_TAG, x=RIGHT_X, w=RIGHT_W),
               self._mid(0.05, "一組有序對", "a set of ordered pairs",
                         DIM, FS_TAG, x=RIGHT_X, w=RIGHT_W))

 def _domran(self):
  """Domain and range as the two projections, plus the product as a box."""
  pts = [(0.55, 0.50), (0.95, 1.35), (1.60, 0.85), (2.05, 1.95),
         (2.55, 0.40), (2.95, 1.55), (1.25, 2.15)]
  g = VGroup(self._axes(),
             Rectangle(width=2.75, height=1.95, color=GHOST, stroke_width=2).move_to(
                 [PX0 + 1.75, PY0 + 1.22, 0]))
  for u, v in pts:
   g.add(Dot([PX0 + u, PY0 + v, 0], radius=0.08, color=ACCENT_A))
  g.add(Line([PX0 + 0.55, PY0 - 0.16, 0], [PX0 + 2.95, PY0 - 0.16, 0], color=ACCENT_B, stroke_width=5),
        Line([PX0 - 0.16, PY0 + 0.40, 0], [PX0 - 0.16, PY0 + 1.90, 0], color=ACCENT_C, stroke_width=5),
        Text("dom R", font_size=FS_SMALL, color=ACCENT_B).move_to([PX0 + 1.75, PY0 - 0.40, 0]),
        Text("range R", font_size=FS_SMALL, color=ACCENT_C).move_to([PX0 - 0.80, PY0 + 1.15, 0]))
  # Symbolic on purpose: the English gloss for this one is long enough that
  # `_mid` shrinks it to unreadable inside the column beside the plane.
  return g.add(self._mid(0.85, "A × B", "A × B", ACCENT_A, FS_TAG + 4, x=RIGHT_X, w=RIGHT_W),
               self._mid(0.15, "ℝ² = ℝ × ℝ", "ℝ² = ℝ × ℝ", ACCENT_B, FS_TAG + 2,
                         x=RIGHT_X, w=RIGHT_W),
               self._mid(-0.50, "第一元素在 A，第二元素在 B",
                         "first element in A, second in B", DIM, FS_TAG,
                         x=RIGHT_X, w=RIGHT_W))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  mem, eq, inc = self._members(), self._equality(), self._inclusion()
  spec, emp = self._specify(), self._empty()
  dom, res, unf = self._domain(), self._restricted(), self._unfold()
  pair, rel, dr = self._pair(), self._relation(), self._domran()

  return [([mem], []),                         # 0  sets and membership
          ([eq], [mem]),                       # 1  set equality
          ([inc], [eq]),                       # 2  inclusion, both ways
          ([spec], [inc]),                     # 3  specifying a set
          ([emp], [spec]),                     # 4  the empty set
          ([dom], [emp]),                      # 5  restricted variables
          ([res], [dom]),                      # 6  restricted quantifiers
          ([unf], [res]),                      # 7  the two unfoldings
          ([pair], [unf]),                     # 8  ordered pairs
          ([rel], [pair]),                     # 9  a relation is a set of pairs
          ([dr], [rel])]                       # 10 dom, range, product


AdvCalcE02ZH, AdvCalcE02EN = make(AdvCalcE02Base, "02", prefix="AdvCalcE")
