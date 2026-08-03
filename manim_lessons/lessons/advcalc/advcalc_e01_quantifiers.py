"""advcalc E01 — Chapter 0, sections 1-3: logic, quantifiers, the connectives.

The book calls chapter 0 reference material, with one exception it is emphatic
about: the order of mixed quantifiers ("his whole mathematical future is at
stake"). So the episode spends its middle on exactly that, with the book's own
example on a number line -- for every x there is a y (the y slides along, one
per x) versus there is a y for every x (one fixed y that must beat them all,
and visibly fails at y+1).

Beats 0-2 set up frames and the two quantifiers, 3-5 are the order, 6 is the
three-quantifier definition of convergence, 7-9 are the connectives with their
truth tables, and 10 is the negation rule sweeping across a quantifier string.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
FS_CELL = 16

# The two number lines for beats 4-5. Both live in the animation band
# (-1.90 <= y <= 1.30); the upper one is the true statement, the lower the false.
NLX0, NLX1 = -4.30, 3.10
NY_T, NY_F = 0.75, -0.85
XS = (-3.30, -1.70, -0.10, 1.50)            # the sample values of x


class AdvCalcE01Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 1

 MODE_LABEL = {
  0: {"zh": "敘述與敘述框架", "en": "statements and statement frames"},
  1: {"zh": "全稱量詞", "en": "the universal quantifier"},
  2: {"zh": "存在量詞；束縛變數與自由變數", "en": "the existential quantifier; bound and free"},
  3: {"zh": "兩種量詞混用時，順序會改變意思", "en": "with both kinds, the order changes the meaning"},
  4: {"zh": "書上的例子", "en": "the book's own example"},
  5: {"zh": "第二句強得多", "en": "the second is by far the stronger statement"},
  6: {"zh": "同種量詞可交換；收斂的定義", "en": "same kind commutes; the definition of convergence"},
  7: {"zh": "而且、或", "en": "and, or"},
  8: {"zh": "最麻煩的「如果就」", "en": "the troublesome if-then"},
  9: {"zh": "恆真式與三條常用等價", "en": "tautologies and three useful equivalences"},
  10: {"zh": "量詞的否定", "en": "negating a string of quantifiers"},
 }

 # ── pieces ───────────────────────────────────────────────────────
 def _panel(self, x, w, zh, en, tcolor, rows):
  """A titled box whose rows are centred vertically, so a two-row panel and a
  three-row one sit level rather than both hanging from the top."""
  g = VGroup(Rectangle(width=w, height=2.30, color=GHOST, stroke_width=2).move_to([x, 0.05, 0]),
             self._mid(1.42, zh, en, tcolor, FS_TAG, x=x, w=w))
  y0 = 0.05 + 0.31 * (len(rows) - 1)
  for k, s in enumerate(rows):
   g.add(Text(s, font_size=FS_TAG, color=INK).move_to([x, y0 - 0.62 * k, 0]))
  return g

 def _stmt_vs_frame(self):
  """The book's own examples on both sides (p. 1)."""
  return VGroup(
   self._panel(-3.30, 4.90, "敘述", "statement", ACCENT_B,
               ["1 < 2          T", "4 + 3 = 5          F"]),
   self._panel(3.30, 4.90, "敘述框架", "statement frame", ACCENT_C,
               ["x < 4", "x < y", "3x² + y² = 10"]),
   self._mid(-1.55, "左邊當下就能判斷真假；右邊要給了值才能判斷",
             "the left is true or false as it stands; the right needs values first",
             DIM, FS_TAG, w=11.6))

 def _branch_all(self):
  """One frame, and the two ways out of it."""
  return VGroup(
   Rectangle(width=2.90, height=0.66, color=ACCENT_A, stroke_width=2).move_to([0, 1.05, 0]),
   Text("P ( x ) :  x < 4", font_size=FS_TAG, color=ACCENT_A).move_to([0, 1.05, 0]),
   self._mid(0.05, "給 x 一個值", "give x a value", ACCENT_B, FS_TAG, x=-3.40, w=3.8),
   Text("P ( 5 ) :  5 < 4", font_size=FS_TAG, color=DIM).move_to([-3.40, -0.55, 0]),
   self._mid(0.05, "宣告它永遠為真", "assert it is always true", ACCENT_C, FS_TAG, x=3.40, w=3.8),
   Text("( ∀x ) ( x < 4 )", font_size=FS_TAG, color=DIM).move_to([3.40, -0.55, 0]),
   self._arr([-0.85, 0.86, 0], [-2.90, 0.30, 0], ACCENT_B, sw=3, tl=0.14),
   self._arr([0.85, 0.86, 0], [2.90, 0.30, 0], ACCENT_C, sw=3, tl=0.14))

 def _branch_exists(self):
  """The third way out, and what quantifying did to x.

  The free/bound pair goes on the left as its own two-line column, mirroring
  the right one. Hanging `x free` under the substitution branch reads as if
  P(5) were the free case, which is backwards -- x is free in the frame, and
  it is the quantifier that binds it."""
  return VGroup(
   self._mid(-1.05, "宣告它有時為真", "assert it is sometimes true", ACCENT_C, FS_TAG, x=3.40, w=3.8),
   Text("( ∃x ) ( x < 4 )", font_size=FS_TAG, color=DIM).move_to([3.40, -1.58, 0]),
   self._mid(-1.05, "框架裡的 x 是自由的", "x is free in the frame", ACCENT_B, FS_TAG,
             x=-3.40, w=3.9),
   self._mid(-1.58, "加了量詞，x 就變束縛", "quantifying binds it", WARN, FS_TAG,
             x=-3.40, w=3.9))

 def _line(self, y, color):
  return VGroup(self._arr([NLX0 - 0.20, y, 0], [NLX1 + 0.60, y, 0], DIM, sw=3, tl=0.14),
                Text("x", font_size=FS_SMALL, color=color).move_to([NLX0 - 0.45, y, 0]))

 def _order_true(self):
  """For every x there is a y: the witness slides, one per x."""
  g = VGroup(self._line(NY_T, DIM),
             self._mid(NY_T + 0.62, "對每個 x，都找得到一個 y", "for every x, a y can be found",
                       ACCENT_B, FS_TAG, x=-1.10, w=6.2),
             Text("T", font_size=FS_TAG, color=ACCENT_B).move_to([NLX1 + 1.05, NY_T + 0.62, 0]))
  for x in XS:                              # each x gets its own witness y = x+1
   g.add(self._dot(x, NY_T, ACCENT_A), self._dot(x + 1.10, NY_T, ACCENT_B),
         self._arr([x + 0.10, NY_T + 0.26, 0], [x + 1.00, NY_T + 0.26, 0], ACCENT_B, sw=2.5, tl=0.10))
  return g

 def _order_false(self):
  """There is a y for every x: one fixed y, beaten by y+1."""
  y0 = 1.90
  g = VGroup(self._line(NY_F, DIM),
             self._mid(NY_F - 0.66, "同一個 y 要對所有 x 都成立", "one single y must work for every x",
                       WARN, FS_TAG, x=-1.10, w=6.2),
             Text("F", font_size=FS_TAG, color=WARN).move_to([NLX1 + 1.05, NY_F - 0.66, 0]),
             self._dot(y0, NY_F, ACCENT_C), self._dot(y0 + 0.85, NY_F, WARN),
             Text("y₀", font_size=FS_SMALL, color=ACCENT_C).move_to([y0, NY_F + 0.30, 0]),
             Text("y₀ + 1", font_size=FS_SMALL, color=WARN).move_to([y0 + 0.95, NY_F + 0.30, 0]))
  for x in XS:
   g.add(self._dot(x, NY_F, ACCENT_A))
  return g

 def _dot(self, x, y, color):
  return Line([x, y - 0.10, 0], [x, y + 0.10, 0], color=color, stroke_width=5)

 def _convergence(self):
  """The three-quantifier definition drawn instead of restated.

  The formula bar already has the string of quantifiers, so the picture shows
  what it means: an epsilon band, and the N that the band forces. Which is
  also the point of the previous four beats -- N depends on epsilon, so the
  order (for every epsilon, there exists an N) is the one that works."""
  import math
  LIM, EPS, AY = 0.15, 0.45, -1.15
  X0, DX, NPT = -4.30, 0.52, 14
  vals = [LIM + 1.60 * math.exp(-0.28 * n) * math.cos(1.1 * n) for n in range(1, NPT + 1)]
  nx = X0 + DX * 2.5                        # the last term outside the band is n = 3
  g = VGroup(
   self._arr([X0 - 0.45, AY, 0], [X0 + DX * NPT + 0.35, AY, 0], DIM, sw=3, tl=0.14),
   Line([X0 - 0.40, LIM, 0], [X0 + DX * NPT + 0.10, LIM, 0], color=DIM, stroke_width=2),
   self._dash([X0 - 0.40, LIM + EPS, 0], [X0 + DX * NPT + 0.10, LIM + EPS, 0], ACCENT_C, n=26),
   self._dash([X0 - 0.40, LIM - EPS, 0], [X0 + DX * NPT + 0.10, LIM - EPS, 0], ACCENT_C, n=26),
   self._dash([nx, AY, 0], [nx, LIM + 0.95, 0], WARN, n=8),
   Text("N", font_size=FS_SMALL, color=WARN).move_to([nx, AY - 0.28, 0]),
   Text("x", font_size=FS_SMALL, color=DIM).move_to([X0 + DX * NPT + 0.42, LIM, 0]),
   Text("+ε", font_size=FS_SMALL, color=ACCENT_C).move_to([X0 + DX * NPT + 0.45, LIM + EPS, 0]),
   Text("−ε", font_size=FS_SMALL, color=ACCENT_C).move_to([X0 + DX * NPT + 0.45, LIM - EPS, 0]))
  for k, v in enumerate(vals):
   inside = abs(v - LIM) <= EPS
   g.add(Dot([X0 + DX * k, v, 0], radius=0.065, color=ACCENT_B if inside else WARN))
  return g.add(self._mid(-1.70, "先給 ε，才找得到 N —— 所以量詞的順序是這一個",
                         "epsilon first, then an N can be found: that is why the order is this one",
                         ACCENT_A, FS_TAG, w=11.6))

 def _table(self, x, head, rows, color):
  """A little truth table. Four rows of T/F, as in the book."""
  g = VGroup(Text(head, font_size=FS_TAG, color=color).move_to([x, 1.05, 0]))
  for k, r in enumerate(rows):
   g.add(Text(r, font_size=FS_CELL, color=INK).move_to([x, 0.55 - 0.36 * k, 0]))
  return g

 def _connectives(self):
  return VGroup(self._table(-3.70, "P & Q", ("T T   T", "T F   F", "F T   F", "F F   F"), ACCENT_B),
                self._table(0.00, "P or Q", ("T T   T", "T F   T", "F T   T", "F F   T"), ACCENT_C),
                self._mid(-1.15, "數學裡的「或」永遠是相容的", "in mathematics, or is always inclusive",
                          ACCENT_C, FS_TAG, x=0.0, w=6.4))

 def _implies(self):
  """The table, plus the instantiations that force the two odd rows (p. 4)."""
  ex = ("2 < 3  ⇒  2 < 5      T", "4 < 3  ⇒  4 < 5      T", "6 < 3  ⇒  6 < 5      T")
  g = VGroup(self._table(-3.70, "P ⇒ Q", ("T T   T", "T F   F", "F T   T", "F F   T"), ACCENT_A),
             self._mid(0.72, "「若 x 小於三則 x 小於五」對每個 x 都成立",
                       "if x is under three then x is under five holds for every x",
                       DIM, FS_TAG, x=1.85, w=6.5))
  for k, s in enumerate(ex):
   g.add(Text(s, font_size=FS_CELL, color=INK if k == 0 else ACCENT_C)
         .move_to([1.85, 0.16 - 0.46 * k, 0]))
  return g.add(self._mid(-1.45, "所以只有前提真、結論假的時候才是假的",
                         "so it is false only when a true premise gives a false conclusion",
                         WARN, FS_TAG, w=11.4))

 def _equivs(self):
  """A tautology shown as an all-T column, beside the equivalence the
  formula line does not have room for."""
  g = VGroup(self._table(-3.90, "P or (∼P)", ("T      T", "F      T"), ACCENT_B),
             self._mid(-0.55, "真值表全部為真", "the whole column is T", ACCENT_B, FS_TAG,
                       x=-3.90, w=3.6),
             Text("( P ⇒ Q )    ⇔    Q or (∼P)", font_size=FS_TAG + 3, color=ACCENT_A)
             .move_to([1.90, 0.60, 0]),
             self._mid(-0.10, "第三條等價，這一條最常被用到",
                       "the third equivalence, the one used most often", DIM, FS_TAG,
                       x=1.90, w=6.4))
  return g.add(self._mid(-1.45, "不涉及量詞的有效推理，都要用恆真式表達",
                         "valid reasoning without quantifiers is expressed by tautologies",
                         DIM, FS_TAG, w=11.4))

 def _negation(self):
  """The rule as the mechanism, not as the equation.

  The formula bar already carries the whole identity, so restating it here
  would just be the same two lines twice. What the picture adds is the moving
  parts: each quantifier flipping in place, and the negation sign taking its
  own route from the front of the string to the back."""
  QX = (-3.40, -1.90, -0.40)
  TOP, BOT = 0.85, -0.35
  g = VGroup(Text("P", font_size=FS_TAG + 3, color=DIM).move_to([1.00, TOP, 0]),
             Text("P", font_size=FS_TAG + 3, color=ACCENT_A).move_to([2.20, BOT, 0]))
  for x, up, dn in zip(QX, ("( ∀x )", "( ∃y )", "( ∀z )"), ("( ∃x )", "( ∀y )", "( ∃z )")):
   g.add(Text(up, font_size=FS_TAG + 3, color=DIM).move_to([x, TOP, 0]),
         Text(dn, font_size=FS_TAG + 3, color=ACCENT_A).move_to([x, BOT, 0]),
         self._arr([x, TOP - 0.28, 0], [x, BOT + 0.28, 0], ACCENT_B, sw=2.5, tl=0.12))
  # the negation sign, and the path it takes to the end of the string
  for x, y, c in ((-4.60, TOP, WARN), (1.00, BOT, WARN)):
   g.add(Rectangle(width=0.62, height=0.56, color=c, stroke_width=2).move_to([x, y, 0]),
         Text("∼", font_size=FS_TAG + 5, color=c).move_to([x, y, 0]))
  g.add(self._dash([-4.60, TOP - 0.34, 0], [-4.60, -1.00, 0], WARN, n=6),
        self._dash([-4.60, -1.00, 0], [1.00, -1.00, 0], WARN, n=22),
        self._arr([1.00, -1.00, 0], [1.00, BOT - 0.32, 0], WARN, sw=2.5, tl=0.12))
  return g.add(self._mid(-1.55, "每個量詞換成相反的那種，否定號移到整串的最後",
                         "flip every quantifier, move the sign to the end of the string",
                         ACCENT_B, FS_TAG, w=11.4))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  card, ways, bf = self._stmt_vs_frame(), self._branch_all(), self._branch_exists()
  ot, of = self._order_true(), self._order_false()
  conv = self._convergence()
  conn, impl, eq, neg = self._connectives(), self._implies(), self._equivs(), self._negation()

  return [([card], []),                        # 0  statement vs frame
          ([ways], [card]),                    # 1  the universal quantifier
          ([bf], []),                          # 2  the existential; bound and free
          ([ot], [ways, bf]),                  # 3  order matters
          ([of], []),                          # 4  the book's example, both lines
          ([], []),                            # 5  the second is stronger
          ([conv], [ot, of]),                  # 6  same kind commutes; convergence
          ([conn], [conv]),                    # 7  and, or
          ([impl], [conn]),                    # 8  if-then
          ([eq], [impl]),                      # 9  tautologies and equivalences
          ([neg], [eq])]                       # 10 negating quantifiers


AdvCalcE01ZH, AdvCalcE01EN = make(AdvCalcE01Base, "01", prefix="AdvCalcE")
