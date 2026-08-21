"""advcalc E27 -- Chapter 2, section 6, first part (book pp. 102-105): the
elimination process and the four problems it settles, Lemma 6.1 on elementary
operations preserving the span, the order of a tuple, the reduction algorithm,
the structure of the matrix it produces, and row-reduced echelon form with its
canonical basis. Section 6 runs to p. 109 and E28 takes pp. 105-109; p. 109
onward is exercises.

The worked example is this episode's own rather than the book's, per the
copyright note in docs/PLAYBOOK.md section 8, and it is chosen to do more work
than the book's does: it is 3 by 4 of rank 2 with orders 1 and 3, so all three
structural properties -- rising orders, a leftover zero row, and delta in each
pivot column -- are visible in a single run, and the row that turns to zeros is
genuinely a combination of the other two, which beat 9 can then point at.

The reduction is *run* here, not typed out. REDUCTION below is produced by
`_reduce` in exact integer arithmetic and checked against the properties the
narration claims, so the matrices on screen cannot drift from the algorithm
being described. The book's own example admits to being arranged so that no
fractions appear; this one is arranged the same way, but by search rather than
by hand, and the search is what the assertions preserve.
"""
import pathlib, sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

START = [[1, -1, 2, 1], [-1, 1, -3, -2], [0, 0, 2, 2]]


def _reduce(m):
 """Row reduce, returning every intermediate matrix and the operation used.

 Operations are numbered as the narration numbers them: (1) interchange,
 (2) scale, (3) subtract a multiple."""
 a = [[Fraction(x) for x in row] for row in m]
 out, piv = [([r[:] for r in a], None)], 0
 for col in range(len(a[0])):
  r = next((i for i in range(piv, len(a)) if a[i][col] != 0), None)
  if r is None:
   continue
  if r != piv:
   a[piv], a[r] = a[r], a[piv]
   out.append(([q[:] for q in a], 1))
  if a[piv][col] != 1:
   c = a[piv][col]
   a[piv] = [x / c for x in a[piv]]
   out.append(([q[:] for q in a], 2))
  if any(a[i][col] != 0 for i in range(len(a)) if i != piv):
   for i in range(len(a)):
    if i != piv and a[i][col] != 0:
     f = a[i][col]
     a[i] = [p - f * q for p, q in zip(a[i], a[piv])]
   out.append(([q[:] for q in a], 3))
  piv += 1
 return out


def _order(row):
 """The book's `order`: the index of the first nonzero entry, 1-based."""
 return next((j + 1 for j, x in enumerate(row) if x != 0), None)


REDUCTION = _reduce(START)
FINAL = REDUCTION[-1][0]
ORDERS = [_order(r) for r in FINAL]
RANK = sum(1 for r in FINAL if any(x != 0 for x in r))

# Everything the narration claims about this example, checked here rather than
# trusted. If a future edit changes START, the episode fails to import instead
# of quietly drawing a matrix that no longer illustrates the point.
assert all(x.denominator == 1 for a, _ in REDUCTION for r in a for x in r), "fractions appeared"
assert len(REDUCTION) == 4, "the chain is drawn as four matrices"
assert ORDERS[:RANK] == [1, 3] and ORDERS[RANK:] == [None], "orders 1 and 3, then a zero row"
assert RANK == 2 < len(START), "want a leftover zero row"
for j in range(RANK):                        # pivot columns are the standard basis
 col = [FINAL[i][ORDERS[j] - 1] for i in range(len(FINAL))]
 assert col == [1 if i == j else 0 for i in range(len(FINAL))], "pivot column is not delta"
# the row that vanishes really is a combination of the two that survive
assert [-2 * p - 2 * q for p, q in zip(START[0], START[1])] == START[2], "row 3 is not that combination"

FMT = lambda v: str(int(v))


class AdvCalcE27Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 27

 MODE_LABEL = {
  0: {"zh": "一個程序，四個問題", "en": "one procedure, four problems"},
  1: {"zh": "引理 6.1：三種運算不改變線性擴張",
      "en": "lemma 6.1: three operations that preserve the span"},
  2: {"zh": "理由是每一種都做得回去", "en": "because every one of them can be undone"},
  3: {"zh": "階：第一個非零座標的位置", "en": "order: where the first nonzero entry sits"},
  4: {"zh": "演算法的一步", "en": "one step of the algorithm"},
  5: {"zh": "一個例子，從頭走到尾", "en": "one example, start to finish"},
  6: {"zh": "做完之後的三個性質", "en": "three properties of what you end with"},
  7: {"zh": "為什麼那些橫列是獨立的", "en": "why those rows are independent"},
  8: {"zh": "四個問題裡的前兩個解決了",
      "en": "the first two of the four problems, settled"},
  9: {"zh": "那條看不出來的相依列", "en": "the dependent row you could not see"},
  10: {"zh": "列簡化階梯形與典範基底",
       "en": "row-reduced echelon form and the canonical basis"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _four_problems(self):
  g = VGroup(self._box(-4.30, 0.55, "α₁ , … , α ₘ", ACCENT_B, w=2.80, h=0.62, size=FS_TAG),
             self._arr([-2.85, 0.55, 0], [-1.85, 0.55, 0], ACCENT_A, sw=2.5, tl=0.12))
  outs = ((0.98, "α ₁ , … , α ₖ   ⊂   L ( α₁ , … , α ₘ )", ACCENT_C),
          (0.30, "d ( V )", ACCENT_C),
          (-0.38, "Δ ( a )", WARN),
          (-1.06, "a ⁻¹", WARN))
  for y, s, col in outs:
   g.add(self._box(0.60, y, s, col, w=4.40, h=0.56, size=FS_TAG - 1))
  g.add(Line([-1.70, outs[-1][0], 0], [-1.70, outs[0][0], 0], color=DIM, stroke_width=1.6))
  for y, _, _ in outs:
   g.add(self._arr([-1.70, y, 0], [-1.55, y, 0], DIM, sw=1.8, tl=0.09))
  return g.add(self._mid(-1.78, "同一個中學就學過的消去程序，一次解決這四件事",
                         "one elimination procedure from school settles all four",
                         ACCENT_A, FS_TAG, w=11.9))

 def _three_ops(self):
  rows = ((0.95, "α ᵢ   ↔   α ⱼ", ACCENT_B),
          (0.20, "α ᵢ   →   x α ᵢ      ( x ≠ 0 )", ACCENT_C),
          (-0.55, "α ᵢ   →   α ᵢ  −  x α ⱼ      ( j ≠ i )", WARN))
  g = VGroup()
  for k, (y, s, col) in enumerate(rows):
   g.add(self._box(-2.20, y, s, col, w=5.60, h=0.60, size=FS_TAG - 1),
         Text(f"( {k + 1} )", font_size=FS_TAG - 2, color=col).move_to([-5.50, y, 0]))
  return g.add(self._mid(0.95, "對調", "interchange", ACCENT_B, FS_TAG, x=3.55, w=3.60),
               self._mid(0.20, "乘上非零的數", "scale by a nonzero number",
                         ACCENT_C, FS_TAG, x=3.55, w=3.60),
               self._mid(-0.55, "減去另一個的倍數", "subtract a multiple of another",
                         WARN, FS_TAG, x=3.55, w=3.60),
               self._mid(-1.30, "第三條要求 j 不等於 i：減自己的倍數會把向量弄掉",
                         "the third needs j different from i; subtracting itself would destroy it",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "三種都不改變這串向量生成的空間",
                         "none of the three changes the space the list spans",
                         ACCENT_A, FS_TAG, w=11.9))

 def _undo(self):
  """Each operation is its own way back, so the two lists sit inside each
  other's span. Drawing the containment both ways is the proof."""
  g = VGroup(self._box(-3.80, 0.88, "{ α ᵢ }", ACCENT_B, w=1.80, h=0.56),
             self._box(-0.40, 0.88, "{ β ᵢ }", ACCENT_C, w=1.80, h=0.56),
             self._arr([-2.85, 1.02, 0], [-1.35, 1.02, 0], ACCENT_A, sw=2.5, tl=0.12),
             self._arr([-1.35, 0.74, 0], [-2.85, 0.74, 0], WARN, sw=2.5, tl=0.12),
             Text("( 1 ) ( 2 ) ( 3 )", font_size=FS_TAG - 6, color=ACCENT_A)
             .move_to([-2.10, 1.22, 0]))
  pairs = ((0.10, "( 1 )", "↔  ( 1 )"), (-0.50, "( 2 )   × x", "↔  ( 2 )   ÷ x"),
           (-1.10, "( 3 )   − x α ⱼ", "↔  ( 3 )   + x α ⱼ"))
  for y, a, b in pairs:
   g.add(Text(a, font_size=FS_TAG - 4, color=DIM).move_to([-3.90, y, 0]),
         Text(b, font_size=FS_TAG - 4, color=DIM).move_to([-1.30, y, 0]))
  return g.add(self._box(3.30, 0.88, "L ( { β ᵢ } )  =  L ( { α ᵢ } )", ACCENT_A,
                         w=4.60, h=0.58, size=FS_TAG - 1),
               self._mid(0.10, "每一種運算都有反過來的那一種",
                         "each operation has its own way back",
                         DIM, FS_TAG, x=3.30, w=4.60),
               self._mid(-0.70, "所以兩串向量互相落在對方的線性擴張裡",
                         "so each list lies inside the other's span",
                         ACCENT_C, FS_TAG, x=3.30, w=4.60),
               self._mid(-1.78, "互相包含，生成的空間就只好一樣",
                         "each contains the other, so the two spans coincide",
                         ACCENT_A, FS_TAG, w=11.9))

 def _order_def(self):
  ex = [0, 0, 0, 2, -1, 0]
  n = _order(ex)
  g = VGroup()
  for j, v in enumerate(ex):
   hot = j == n - 1
   g.add(Text(FMT(v), font_size=FS_TAG - 1, color=WARN if hot else DIM)
         .move_to([-2.80 + j * 0.80, 0.75, 0]),
         Text(f"{j + 1}", font_size=FS_TAG - 6, color=DIM)
         .move_to([-2.80 + j * 0.80, 1.15, 0]))
  g.add(self._brackets(-3.15, -2.80 + (len(ex) - 1) * 0.80 + 0.35, 0.51, 0.99))
  return g.add(self._arr([-2.80 + (n - 1) * 0.80, 0.25, 0],
                         [-2.80 + (n - 1) * 0.80, 0.48, 0], WARN, sw=2.5, tl=0.11),
               Text(f"n ( x )  =  {n}", font_size=FS_TAG, color=WARN)
               .move_to([-2.80 + (n - 1) * 0.80, -0.10, 0]),
               self._mid(-0.85, "階就是第一個不是零的座標排在第幾個",
                         "the order is the place of the first entry that is not zero",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.32, "階越小，代表這個元組左邊的零越少",
                         "a smaller order means fewer zeros on the left",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "零元組沒有階，這個定義只對非零的元組講",
                         "the zero tuple has no order; the definition is for nonzero ones",
                         ACCENT_C, FS_TAG, w=11.9))

 def _one_step(self):
  """The first step, on the real starting matrix rather than a schematic."""
  hot = {(0, j) for j in range(4)} | {(i, 0) for i in range(len(START))}
  a, pos = self._numgrid(-3.20, 0.35, [[FMT(v) for v in r] for r in START],
                         dx=0.62, dy=0.46, size=FS_TAG - 2, hot=hot, hotcolor=WARN)
  bot = pos(len(START) - 1, 0)[1] - 0.42
  g = VGroup(a,
             self._arr([pos(0, 0)[0] - 0.90, pos(0, 0)[1], 0],
                       [pos(0, 0)[0] - 0.62, pos(0, 0)[1], 0], WARN, sw=2, tl=0.10),
             self._arr([pos(0, 0)[0], bot - 0.26, 0], [pos(0, 0)[0], bot - 0.04, 0],
                       ACCENT_C, sw=2, tl=0.10))
  steps = ((1.00, "階最小的搬到最上面", "least order to the top", WARN),
           (0.30, "首項除成 1", "divide by the leading entry", ACCENT_A),
           (-0.40, "其他列減掉它的倍數", "subtract multiples from the rest", ACCENT_C))
  for y, zh, en, col in steps:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.90, w=5.60))
  return g.add(self._mid(-1.20, "做完這一步，那一直行只剩最上面一個 1，底下全是零",
                         "after this step the column has the leading one and nothing else",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.60, "這個例子第一列的階本來就最小，所以不必對調",
                         "here the first row already has least order, so no interchange is needed",
                         DIM, FS_TAG, w=11.9))

 def _run(self):
  """The chain the module actually computed. Nothing here is typed out."""
  g = VGroup()
  xs = [-3.69, -1.23, 1.23, 3.69]
  for k, ((mat, op), cx) in enumerate(zip(REDUCTION, xs)):
   grid, _ = self._numgrid(cx, 0.62, [[FMT(v) for v in r] for r in mat],
                           dx=0.44, dy=0.38, size=FS_TAG - 5)
   g.add(grid)
   if k:
    g.add(self._arr([cx - 1.23, 0.62, 0], [cx - 0.85, 0.62, 0], DIM, sw=2, tl=0.09),
          Text(f"( {op} )", font_size=FS_TAG - 6, color=ACCENT_A)
          .move_to([cx - 1.04, 0.90, 0]))
  return g.add(self._mid(-0.35, "每一步都只是前面那三種運算之一",
                         "every step is one of the three operations",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-0.90, "先清掉第 1 直行，再把第 2 列的首項除成 1，最後清掉第 3 直行",
                         "clear column one, scale row two to a leading one, clear column three",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.42, "第三列在最後一步變成一整列的零",
                         "the third row becomes a row of zeros at the last step",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "這四個矩陣是程式跑出來的，不是手寫上去的",
                         "these four matrices were computed, not written out by hand",
                         ACCENT_C, FS_TAG, w=11.9))

 def _structure(self):
  """The three claims, marked on the computed final matrix."""
  # Mark the pivot columns and the zero row by colouring their own cells and
  # putting the markers outside the brackets. A first draft drew lines through
  # the columns, which simply covered the numbers up.
  hot = {(i, ORDERS[j] - 1) for j in range(RANK) for i in range(len(FINAL))}
  hot |= {(len(FINAL) - 1, j) for j in range(len(FINAL[0]))}
  a, pos = self._numgrid(-3.30, 0.10, [[FMT(v) for v in r] for r in FINAL],
                         dx=0.62, dy=0.46, size=FS_TAG - 2, hot=hot, hotcolor=WARN)
  g = VGroup(a)
  for j in range(RANK):
   c = ORDERS[j] - 1
   g.add(self._arr([pos(0, c)[0], pos(0, c)[1] + 0.46, 0],
                   [pos(0, c)[0], pos(0, c)[1] + 0.28, 0], WARN, sw=2, tl=0.09),
         Text(f"n {'₁₂₃'[j]}", font_size=FS_TAG - 6, color=WARN)
         .move_to([pos(0, c)[0], pos(0, c)[1] + 0.64, 0]))
  zr = len(FINAL) - 1
  g.add(self._arr([pos(zr, 0)[0] - 0.72, pos(zr, 0)[1], 0],
                  [pos(zr, 0)[0] - 0.46, pos(zr, 0)[1], 0], ACCENT_C, sw=2, tl=0.10))
  props = ((1.00, "前 k 列的階遞增", "the first k orders rise", ACCENT_B),
           (0.30, "其餘的列全是零", "the rest are zero rows", ACCENT_C),
           (-0.40, "第 nⱼ 直行是 δ ʲ", "the n-j-th column is delta", WARN))
  for y, zh, en, col in props:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.70, w=5.80))
  return g.add(self._mid(-1.20, f"這個例子的階是 {ORDERS[0]} 與 {ORDERS[1]}，中間跳過了一個",
                         "here the orders are one and three, with one skipped between",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.62, "階不必連號，跳過的那些直行就是自由的方向",
                         "orders need not be consecutive; the skipped columns are the free ones",
                         DIM, FS_TAG, w=11.9))

 def _independent(self):
  """The argument is positional, so the picture is positional: one column,
  one coefficient, nowhere for it to hide."""
  g = VGroup(self._box(-2.60, 1.00, "c ₁ α ₁  +  c ₂ α ₂  =  0", ACCENT_B,
                       w=4.60, h=0.60, size=FS_TAG - 1))
  hot = {(j, ORDERS[j] - 1) for j in range(RANK)}
  a, pos = self._numgrid(-3.30, 0.05, [[FMT(v) for v in r] for r in FINAL[:RANK]],
                         dx=0.62, dy=0.46, size=FS_TAG - 2, hot=hot, hotcolor=WARN)
  g.add(a)
  bot = pos(RANK - 1, 0)[1] - 0.42
  for j in range(RANK):
   c = ORDERS[j] - 1
   g.add(self._arr([pos(j, c)[0], bot - 0.30, 0], [pos(j, c)[0], bot - 0.06, 0],
                   WARN, sw=2, tl=0.09),
         Text(f"c {'₁₂'[j]}", font_size=FS_TAG - 3, color=WARN)
         .move_to([pos(j, c)[0], bot - 0.52, 0]))
  return g.add(self._mid(0.55, "第 nⱼ 直行只有第 j 列是 1", "that column has a one only in row j",
                         WARN, FS_TAG, x=2.90, w=5.60),
               self._mid(-0.15, "所以組合在那個位置就等於 cⱼ",
                         "so the combination equals c-j exactly there",
                         ACCENT_A, FS_TAG, x=2.90, w=5.60),
               self._mid(-1.32, "要整個組合是零，每一個係數就只好是零",
                         "for the whole combination to vanish, every coefficient must be zero",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "沒有別的橫列能補上那一格——這就是獨立",
                         "no other row can fill that place, and that is independence",
                         ACCENT_A, FS_TAG, w=11.9))

 def _settled(self):
  g = VGroup(self._box(-3.30, 0.95, "α ₁ , … , α ₖ   ⊂   L ( α₁ , … , α ₘ )", ACCENT_C,
                       w=5.20, h=0.60, size=FS_TAG - 1),
             self._box(-3.30, 0.20, "d ( V )", ACCENT_C, w=5.20, h=0.60, size=FS_TAG - 1),
             self._box(-3.30, -0.55, "Δ ( a )", DIM, w=5.20, h=0.60, size=FS_TAG - 1),
             self._box(-3.30, -1.30, "a ⁻¹", DIM, w=5.20, h=0.60, size=FS_TAG - 1))
  for y in (0.95, 0.20):
   g.add(Text("✓", font_size=FS_TAG + 2, color=WARN).move_to([-0.10, y, 0]))
  for y in (-0.55, -1.30):
   g.add(Text("→", font_size=FS_TAG, color=DIM).move_to([-0.10, y, 0]))
  return g.add(self._mid(0.95, "非零的那 k 條橫列直接讀出來",
                         "the k nonzero rows read straight off",
                         ACCENT_C, FS_TAG, x=3.40, w=4.60),
               self._mid(0.20, "維數就是 k", "the dimension is k",
                         ACCENT_C, FS_TAG, x=3.40, w=4.60),
               self._mid(-0.55, "留給下一集", "left for the next episode",
                         DIM, FS_TAG, x=3.40, w=4.60),
               self._mid(-1.30, "也留給下一集", "also for the next episode",
                         DIM, FS_TAG, x=3.40, w=4.60))

 def _hidden(self):
  """The example's third row really is the combination shown; the module
  asserts it, so the caption is not a claim taken on trust."""
  a, _ = self._numgrid(-3.60, 0.62, [[FMT(v) for v in r] for r in START],
                       dx=0.62, dy=0.46, size=FS_TAG - 2, hotrow=2, hotcolor=WARN)
  b, _ = self._numgrid(1.90, 0.62, [[FMT(v) for v in r] for r in FINAL],
                       dx=0.62, dy=0.46, size=FS_TAG - 2, hotrow=2, hotcolor=WARN)
  return VGroup(a, b,
                self._arr([-1.60, 0.62, 0], [-0.10, 0.62, 0], ACCENT_A, sw=2.5, tl=0.12),
                self._box(0.15, -0.55, "α ₃   =   − 2 α ₁  −  2 α ₂", WARN, w=4.40,
                          h=0.60, size=FS_TAG - 1),
                self._mid(-1.16, "第三列本來就是另外兩列的組合，只是看不出來",
                          "the third row was a combination of the other two all along",
                          WARN, FS_TAG, w=11.9),
                self._mid(-1.48, "消去把這件事變成看得見的：它退成一整列的零",
                          "elimination makes that visible by collapsing it to zeros",
                          ACCENT_A, FS_TAG, w=11.9),
                self._mid(-1.78, "所以這個列空間的維數是 2，不是 3",
                          "so the row space has dimension two, not three",
                          ACCENT_C, FS_TAG, w=11.9))

 def _echelon(self):
  """A schematic echelon matrix, drawn from a staircase of pivot columns so
  the zeros below the stairs land where the algorithm would put them. The
  book's Fig. 2.4 is an 8 by 11 with its own pattern; this is a smaller one
  of this episode's own choosing."""
  piv = (0, 2, 3, 5)
  rows, cols = 6, 7
  cell = lambda i, j: [-4.60 + j * 0.66, 0.92 - i * 0.36, 0]
  g = VGroup()
  for i in range(rows):
   for j in range(cols):
    if i < len(piv):
     if j < piv[i]:
      s, col = "0", DIM
     elif j == piv[i]:
      s, col = "1", WARN
     elif j in piv:
      s, col = "0", DIM
     else:
      s, col = "–", DIM
    else:
     s, col = "0", DIM
    g.add(Text(s, font_size=FS_TAG - 4, color=col).move_to(cell(i, j)))
  g.add(self._brackets(-4.90, -4.60 + (cols - 1) * 0.66 + 0.30,
                       0.92 - (rows - 1) * 0.36 - 0.20, 1.12))
  stair = []
  for i, p in enumerate(piv):
   stair += [[cell(i, p)[0] - 0.33, cell(i, p)[1] + 0.18, 0],
             [cell(i, p)[0] - 0.33, cell(i, p)[1] - 0.18, 0]]
  stair.append([cell(len(piv) - 1, cols - 1)[0] + 0.33,
                cell(len(piv) - 1, piv[-1])[1] - 0.18, 0])
  g.add(self._curve(stair, ACCENT_C, sw=2.5))
  return g.add(self._mid(0.90, "每一列的第一個 1 都比上一列更右邊",
                         "each leading one sits further right than the last",
                         WARN, FS_TAG, x=2.70, w=5.60),
               self._mid(0.20, "階梯線底下全是零", "everything below the stairs is zero",
                         ACCENT_C, FS_TAG, x=2.70, w=5.60),
               self._mid(-0.50, "每個 1 所在的直行，其他位置也都是零",
                         "each pivot column is zero everywhere else",
                         DIM, FS_TAG, x=2.70, w=5.60),
               self._mid(-1.32, "這個形狀完全由列空間決定，跟從哪個矩陣開始無關",
                         "the shape is fixed by the row space, whatever matrix you began with",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "所以它的橫列叫做這個空間的典範基底。下一集：初等矩陣",
                         "so its rows are the canonical basis; next time, elementary matrices",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  fp, to, un = self._four_problems(), self._three_ops(), self._undo()
  od, os, rn = self._order_def(), self._one_step(), self._run()
  st, ip, se = self._structure(), self._independent(), self._settled()
  hd, ec = self._hidden(), self._echelon()
  return [([fp], []), ([to], [fp]), ([un], [to]), ([od], [un]),
          ([os], [od]), ([rn], [os]), ([st], [rn]), ([ip], [st]),
          ([se], [ip]), ([hd], [se]), ([ec], [hd])]


AdvCalcE27ZH, AdvCalcE27EN = make(AdvCalcE27Base, "27", prefix="AdvCalcE")
