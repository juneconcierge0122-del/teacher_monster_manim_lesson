"""advcalc E28 -- Chapter 2, section 6, second part (book pp. 105-109): every
elementary row operation as premultiplication by an elementary matrix, the
three elementary matrices, their inverses, b = u^p ... u^1 and r = b . a, why a
nonsingular square matrix reduces to e so that b is its inverse, the augmented
a | e device, and determinants by semireduction. Page 109 onward is exercises,
and *section 7 (the diagonalization of a quadratic form) begins on p. 111.

Everything numeric here is computed, not typed. `_elem` builds an elementary
matrix the way the narration says to build it -- by performing the operation on
the identity -- and the assertions below check the claim the whole episode rests
on, that premultiplying by it does the same operation to any matrix. The two
worked examples are this episode's own, per the copyright note in
docs/PLAYBOOK.md section 8, and each is chosen to show something the obvious
choice would not: the inverse example stays in whole numbers from start to
finish, and the determinant example has a first row of order two, so the
modified interchange (1') is actually forced rather than merely mentioned.
"""
import pathlib, sys
from fractions import Fraction
from functools import reduce
from itertools import permutations
from operator import mul as _times

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

INV_START = [[1, 2], [3, 5]]                       # the inverse example
DET_START = [[0, 1, 2], [1, 1, 1], [2, 0, 3]]      # nonsingular, needs an interchange
SING_START = [[0, 1, 2], [1, 1, 1], [1, 0, -1]]    # same two top rows, singular

N_FIG = 4        # size of the schematic identity in beats 1-3
I0, J0 = 1, 3    # the two rows those beats operate on, zero based
CVAL, XVAL = Fraction(3), Fraction(-2)


def _e(n):
 return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def _mul(a, b):
 return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
          for j in range(len(b[0]))] for i in range(len(a))]


def _apply(m, op):
 """One elementary row operation. ('swap', i, j), ('scale', i, c) or
 ('add', i, j, x) meaning row i becomes row i plus x times row j."""
 a = [r[:] for r in m]
 if op[0] == "swap":
  a[op[1]], a[op[2]] = a[op[2]], a[op[1]]
 elif op[0] == "scale":
  a[op[1]] = [op[2] * v for v in a[op[1]]]
 else:
  a[op[1]] = [p + op[3] * q for p, q in zip(a[op[1]], a[op[2]])]
 return a


def _elem(n, op):
 """The elementary matrix of an operation, found the way beat 1 says to find
 it: by performing the operation on the identity."""
 return _apply(_e(n), op)


def _undo(op):
 return {"swap": lambda: op,
         "scale": lambda: ("scale", op[1], 1 / op[2]),
         "add": lambda: ("add", op[1], op[2], -op[3])}[op[0]]()


def _det(m):
 n, s = len(m), Fraction(0)
 for p in permutations(range(n)):
  sg, t = 1, Fraction(1)
  for i in range(n):
   for j in range(i + 1, n):
    if p[i] > p[j]:
     sg = -sg
  for i in range(n):
   t *= m[i][p[i]]
  s += sg * t
 return s


def _semireduce(m):
 """The book's determinant procedure: (1') interchange two rows and change the
 sign of the one moved down, and (3) subtract multiples -- but no scaling, so
 the determinant survives every step. Returns the chain with its labels."""
 a = [[Fraction(x) for x in r] for r in m]
 out, piv = [([r[:] for r in a], None)], 0
 for col in range(len(a[0])):
  r = next((i for i in range(piv, len(a)) if a[i][col] != 0), None)
  if r is None:
   continue
  if r != piv:
   a[piv], a[r] = a[r], a[piv]
   a[r] = [-x for x in a[r]]
   out.append(([q[:] for q in a], "1′"))
  if any(a[i][col] != 0 for i in range(len(a)) if i != piv):
   for i in range(len(a)):
    if i != piv and a[i][col] != 0:
     f = a[i][col] / a[piv][col]
     a[i] = [p - f * q for p, q in zip(a[i], a[piv])]
   out.append(([q[:] for q in a], "3"))
  piv += 1
 return out


# ── the inverse example, run rather than written out ───────────────────────
INV_OPS = [("add", 1, 0, Fraction(-3)), ("scale", 1, Fraction(-1)),
           ("add", 0, 1, Fraction(-2))]
INV_US = [_elem(2, op) for op in INV_OPS]
INV_CHAIN = [[[Fraction(x) for x in r] for r in INV_START]]
for _u in INV_US:
 INV_CHAIN.append(_mul(_u, INV_CHAIN[-1]))
B = INV_US[2]
for _u in reversed(INV_US[:2]):
 B = _mul(B, _u)

AUG = [[Fraction(x) for x in r] + list(e) for r, e in zip(INV_START, _e(2))]
AUG_CHAIN = [AUG]
for _op in INV_OPS:
 AUG_CHAIN.append(_apply(AUG_CHAIN[-1], _op))

DET_CHAIN = _semireduce(DET_START)
DET_S = DET_CHAIN[-1][0]
SING_CHAIN = _semireduce(SING_START)
SING_S = SING_CHAIN[-1][0]
_diag = lambda s: [s[i][i] for i in range(len(s))]
_prod = lambda v: reduce(_times, v, Fraction(1))

# ── what the narration claims, checked here rather than trusted ────────────
# The claim the whole episode rests on: the matrix you get by doing the
# operation to e does that same operation to anything you premultiply.
_probe = [[Fraction(i * 7 + j * 3 - 5) for j in range(N_FIG)] for i in range(N_FIG)]
for _op in (("swap", I0, J0), ("scale", I0, CVAL), ("add", I0, J0, XVAL)):
 assert _mul(_elem(N_FIG, _op), _probe) == _apply(_probe, _op), "u . a is not the operation"
 assert _mul(_elem(N_FIG, _op), _elem(N_FIG, _undo(_op))) == _e(N_FIG), "not inverse to each other"

assert INV_CHAIN[-1] == _e(2), "the inverse example does not reduce to e"
assert _mul(B, [[Fraction(x) for x in r] for r in INV_START]) == _e(2), "b is not the inverse"
assert all(x.denominator == 1 for m in INV_CHAIN for r in m for x in r), "fractions appeared"
assert all(x.denominator == 1 for r in B for x in r), "the inverse is not integral"
assert len(INV_CHAIN) == 4 and len(AUG_CHAIN) == 4, "four matrices are drawn"
assert [r[:2] for r in AUG_CHAIN[-1]] == _e(2), "the left half did not become e"
assert [r[2:] for r in AUG_CHAIN[-1]] == B, "the right half is not b"

assert len(DET_CHAIN) == 5 and DET_CHAIN[1][1] == "1′", "want five steps, starting with (1')"
assert _prod(_diag(DET_S)) == _det(DET_START) != 0, "the diagonal product is not the determinant"
assert all(x.denominator == 1 for m, _ in DET_CHAIN for r in m for x in r), "fractions appeared"
assert _prod(_diag(SING_S)) == _det(SING_START) == 0, "the singular example is not singular"
assert not any(SING_S[-1]), "the singular example has no zero row"
assert DET_START[:2] == SING_START[:2], "the two examples should differ in one row only"


def FMT(v):
 v = Fraction(v)
 return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


class AdvCalcE28Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 28

 MODE_LABEL = {
  0: {"zh": "元組當直行看，變換就是左乘",
      "en": "tuples as columns, transformations as multiplication"},
  1: {"zh": "把運算施在 e 上，就得到 u", "en": "do the operation to e and out comes u"},
  2: {"zh": "三種初等矩陣", "en": "the three elementary matrices"},
  3: {"zh": "它們的反矩陣還是同一型", "en": "each inverse is elementary of the same kind"},
  4: {"zh": "一串運算就是一串左乘", "en": "a sequence of operations is a sequence of products"},
  5: {"zh": "方陣非奇異時，化簡的終點是 e",
      "en": "for a nonsingular square matrix the reduction ends at e"},
  6: {"zh": "一個例子：三步走到 e", "en": "one example: three steps to e"},
  7: {"zh": "把 e 貼在右邊，一起化簡", "en": "put e alongside and reduce them together"},
  8: {"zh": "算行列式只用兩種運算", "en": "determinants use only two operations"},
  9: {"zh": "半簡化形與對角線的乘積",
      "en": "the semireduced form and the product down its diagonal"},
  10: {"zh": "可逆，當且僅當行列式不是零",
       "en": "invertible if and only if the determinant is not zero"},
 }

 # ── beats ─────────────────────────────────────────────────────────

 def _column_picture(self):
  """The n-tuple as an n by 1 column, so that A is multiplication by a."""
  g = VGroup()
  a, _ = self._array(-4.30, 0.45, 3, 4, dx=0.50, dy=0.42, color=ACCENT_B)
  g.add(a, Text("·", font_size=FS_TAG + 4, color=DIM).move_to([-2.90, 0.45, 0]))
  g.add(self._column(-2.20, 0.45, ["x ₁", "x ₂", "x ₃", "x ₄"], color=ACCENT_C, dy=0.36),
        Text("=", font_size=FS_TAG + 2, color=DIM).move_to([-1.40, 0.45, 0]),
        self._column(-0.70, 0.45, ["y ₁", "y ₂", "y ₃"], color=WARN, dy=0.36))
  for x, y, s, col in ((-4.30, -0.55, "a", ACCENT_B), (-2.20, -0.55, "x", ACCENT_C),
                       (-0.70, -0.55, "y", WARN)):
   g.add(Text(s, font_size=FS_TAG, color=col).move_to([x, y, 0]))
  lines = ((0.95, "元組直著寫，就是一條 n 乘 1 的矩陣",
            "written downward, a tuple is an n by 1 matrix", ACCENT_C),
           (0.25, "於是線性變換就是左乘 a",
            "so a linear transformation is multiplication by a", WARN),
           (-0.45, "y 等於 a 乘 x", "y equals a times x", ACCENT_A))
  for y, zh, en, col in lines:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=3.50, w=5.40))
  return g.add(self._mid(-1.32, "上一集解決了基底與維數，還剩行列式與反矩陣",
                         "last time settled a basis and a dimension; two problems are left",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "問題是：列運算在這個看法下，究竟是什麼？",
                         "the question: what is a row operation in this picture?",
                         ACCENT_A, FS_TAG, w=11.9))

 def _find_u(self):
  """u . a = (u . e) . a, so the operation performed on e is u itself."""
  op = ("add", I0, J0, XVAL)
  u = _elem(N_FIG, op)
  g = VGroup(self._box(-2.75, 1.00, "α ᵢ₀   →   α ᵢ₀  +  x α ⱼ₀", ACCENT_C,
                       w=5.00, h=0.58, size=FS_TAG))
  eg, _ = self._numgrid(-4.30, -0.18, [[FMT(v) for v in r] for r in _e(N_FIG)],
                        dx=0.44, dy=0.38, size=FS_TAG - 4)
  ug, upos = self._numgrid(-1.20, -0.18, [[FMT(v) for v in r] for r in u],
                           dx=0.44, dy=0.38, size=FS_TAG - 4,
                           hot={(I0, J0)}, hotcolor=WARN)
  g.add(eg, ug,
        self._arr([-3.20, -0.18, 0], [-2.30, -0.18, 0], ACCENT_C, sw=2.5, tl=0.12),
        Text("( 3 )", font_size=FS_TAG - 5, color=ACCENT_C).move_to([-2.75, 0.12, 0]),
        Text("e", font_size=FS_TAG, color=DIM).move_to([-4.30, -1.05, 0]),
        Text("u", font_size=FS_TAG, color=WARN).move_to([-1.20, -1.05, 0]),
        # from outside the bracket, not from under the cell: an arrow rising
        # through the column crosses the entries below it (see STATUS's note
        # on E27's marker lines).
        self._arr([upos(I0, J0)[0] + 0.86, upos(I0, J0)[1], 0],
                  [upos(I0, J0)[0] + 0.44, upos(I0, J0)[1], 0], WARN, sw=2, tl=0.10))
  lines = ((0.35, "把運算施在單位矩陣 e 上", "perform the operation on the identity e",
            ACCENT_C),
           (-0.30, "跑出來的那個矩陣就是 u", "and the matrix that comes out is u", WARN))
  for y, zh, en, col in lines:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=3.60, w=4.80))
  return g.add(self._mid(-1.32, "因為 u 乘 a 等於 u 乘 e 之後再乘 a，兩邊講的是同一件事",
                         "since u times a is u times e, times a, the two sides say the same thing",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "這個等式不是巧合，是 e 的定義直接給的",
                         "that identity is not a coincidence; it is what e means",
                         DIM, FS_TAG, w=11.9))

 def _three_matrices(self):
  """This episode's own version of the book's schematic figure: the entries
  are the numbers themselves, each grid built by running the operation on e,
  so what is on screen is what the definition produces."""
  ops = (("swap", I0, J0), ("scale", I0, CVAL), ("add", I0, J0, XVAL))
  hots = ({(I0, J0), (J0, I0), (I0, I0), (J0, J0)}, {(I0, I0)}, {(I0, J0)})
  glosses = (("對調第 i₀ 列與第 j₀ 列", "interchange rows i-0 and j-0"),
             ("第 i₀ 列乘上 c", "multiply row i-0 by c"),
             ("第 j₀ 列的 x 倍加到第 i₀ 列", "add x times row j-0 to row i-0"))
  g = VGroup()
  for cx, op, hot, (zh, en) in zip((-4.05, 0.00, 4.05), ops, hots, glosses):
   u = _elem(N_FIG, op)
   cells = [[FMT(v) for v in r] for r in u]
   if op[0] == "scale":
    cells[I0][I0] = "c"
   if op[0] == "add":
    cells[I0][J0] = "x"
   grid, pos = self._numgrid(cx, 0.30, cells, dx=0.40, dy=0.34,
                             size=FS_TAG - 5, hot=hot, hotcolor=WARN)
   g.add(grid,
         Text("i ₀", font_size=FS_TAG - 7, color=ACCENT_C)
         .move_to([pos(I0, 0)[0] - 0.52, pos(I0, 0)[1], 0]),
         Text("j ₀", font_size=FS_TAG - 7, color=ACCENT_C)
         .move_to([pos(0, J0)[0], pos(0, J0)[1] + 0.42, 0]),
         self._mid(-0.70, zh, en, WARN, FS_TAG - 1, x=cx, w=3.80))
  return g.add(self._mid(-1.32, "三個矩陣都是把運算施在 e 上算出來的，其餘位置跟 e 一樣",
                         "each was computed by running the operation on e; elsewhere they match e",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "對角線上原本都是 1，只有被動到的那幾格不一樣",
                         "the diagonal is ones; only the places touched come out different",
                         DIM, FS_TAG, w=11.9))

 def _inverse_pairs(self):
  """Each inverse is elementary of the same kind. One pair is multiplied out
  on screen; the module checks all three, which is what the caption says."""
  rows = ((0.95, "( 1 )   對調   ↔   再對調一次", "( 1 )   interchange, then interchange again",
           ACCENT_B),
          (0.25, "( 2 )   乘上 c   ↔   乘上 c 分之一", "( 2 )   times c, then times one over c",
           ACCENT_C),
          (-0.45, "( 3 )   加 x 倍   ↔   加 負 x 倍", "( 3 )   plus x times, then minus x times",
           WARN))
  g = VGroup()
  for y, zh, en, col in rows:
   g.add(self._box(-3.55, y, "", col, w=5.20, h=0.62),
         self._mid(y, zh, en, col, FS_TAG - 1, x=-3.55, w=4.90))
  op = ("add", I0, J0, XVAL)
  mats = (_elem(N_FIG, op), _elem(N_FIG, _undo(op)), _e(N_FIG))
  hots = ({(I0, J0)}, {(I0, J0)}, set())
  for cx, m, hot in zip((1.30, 3.35, 5.40), mats, hots):
   grid, _ = self._numgrid(cx, 0.50, [[FMT(v) for v in r] for r in m], dx=0.34, dy=0.30,
                           size=FS_TAG - 6, hot=hot, hotcolor=WARN)
   g.add(grid)
  for x, s in ((2.33, "·"), (4.38, "=")):
   g.add(Text(s, font_size=FS_TAG, color=DIM).move_to([x, 0.50, 0]))
  return g.add(self._mid(-0.35, "第三種那一對是真的乘出來的",
                         "the third pair really was multiplied out",
                         ACCENT_A, FS_TAG, x=3.35, w=4.80),
               self._mid(-0.80, "另外兩對也一樣驗過", "the other two were checked the same way",
                         DIM, FS_TAG, x=3.35, w=4.80),
               self._mid(-1.32, "所以每一個初等矩陣都是非奇異的，而且反矩陣也是初等矩陣",
                         "so every elementary matrix is nonsingular, with an elementary inverse",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "( 2 ) 要求 c 不是零，否則那一列就被抹掉，做不回去",
                         "( 2 ) needs c nonzero; otherwise the row is wiped out and cannot return",
                         DIM, FS_TAG, w=11.9))

 def _chain(self):
  """The order reverses: the operation done first stands rightmost in the
  product, because it is the one that touches a. Each factor keeps the colour
  of the arrow it came from, so the mirrored colour order carries the point --
  a first draft drew connecting lines instead and they read as scribble."""
  xs = (-5.00, -2.50, 0.00, 2.50, 5.00)
  labs = ("a", "u ¹ · a", "u ² u ¹ · a", "…", "r")
  cols = (ACCENT_B, DIM, DIM, DIM, ACCENT_C)
  hues = (ACCENT_B, ACCENT_C, WARN, ACCENT_A)
  done = ("u ¹", "u ²", "u ³", "u ᵖ")           # in the order they are performed
  g = VGroup()
  for x, s, col in zip(xs, labs, cols):
   g.add(self._box(x, 0.92, s, col, w=2.00, h=0.60, size=FS_TAG - 1))
  mids = [(xs[k] + xs[k + 1]) / 2 for k in range(len(xs) - 1)]
  for k, x in enumerate(xs[:-1]):
   g.add(self._arr([x + 1.05, 0.92, 0], [xs[k + 1] - 1.05, 0.92, 0], DIM, sw=2, tl=0.10),
         Text(done[k], font_size=FS_TAG - 4, color=hues[k]).move_to([mids[k], 1.18, 0]))
  for k in range(len(mids)):                     # same colours, mirrored order
   g.add(Text(done[k], font_size=FS_TAG - 2, color=hues[k])
         .move_to([mids[-1 - k], 0.18, 0]))
  for k in range(len(mids) - 1):
   g.add(Text("·", font_size=FS_TAG, color=DIM)
         .move_to([(mids[k] + mids[k + 1]) / 2, 0.18, 0]))
  g.add(Text("b   =", font_size=FS_TAG - 1, color=DIM).move_to([-5.35, 0.18, 0]),
        Text("r   =   b · a", font_size=FS_TAG - 1, color=ACCENT_C).move_to([5.25, 0.18, 0]),
        self._arr([mids[-1] + 0.45, -0.22, 0], [mids[0] - 0.45, -0.22, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(-0.62, "乘積要從右往左讀：先做的那一個排在最右邊，因為它先碰到 a",
                         "read the product right to left: the one done first stands nearest a",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.20, "上下兩排的顏色順序是反過來的，這就是那個顛倒",
                         "the colours run the other way in the two rows, and that is the reversal",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "如果這串運算把 a 化成列簡化階梯形，那 r 就等於 b 乘 a",
                         "if the sequence row reduces a, then r equals b times a",
                         ACCENT_C, FS_TAG, w=11.9))

 def _square_case(self):
  """Why the reduction of a nonsingular square matrix can only end at e:
  m orders, strictly increasing, all inside 1 to m, leaves one possibility."""
  m = 5
  g = VGroup(self._box(-3.60, 1.00, "d ( V )   =   m", ACCENT_B, w=3.20, h=0.58,
                       size=FS_TAG - 1))
  for k in range(m):
   x = -5.10 + k * 0.75
   g.add(Text(f"{k + 1}", font_size=FS_TAG - 5, color=DIM).move_to([x, 0.30, 0]),
         Text(f"n {'₁₂₃₄₅'[k]}", font_size=FS_TAG - 5, color=WARN).move_to([x, -0.20, 0]),
         self._arr([x, 0.13, 0], [x, -0.03, 0], WARN, sw=1.8, tl=0.08))
  g.add(Line([-5.45, 0.05, 0], [-5.10 + (m - 1) * 0.75 + 0.35, 0.05, 0],
             color=DIM, stroke_width=1.6))
  eg, _ = self._numgrid(2.60, 0.30, [[FMT(v) for v in r] for r in _e(m)],
                        dx=0.38, dy=0.32, size=FS_TAG - 6,
                        hot={(i, i) for i in range(m)}, hotcolor=WARN)
  g.add(eg, Text("r  =  e", font_size=FS_TAG, color=ACCENT_C).move_to([2.60, -0.75, 0]),
        self._arr([-0.90, 0.30, 0], [0.60, 0.30, 0], ACCENT_A, sw=2.5, tl=0.12))
  return g.add(self._mid(-0.75, "m 個階嚴格遞增，又都在 1 到 m 之間",
                         "m orders, strictly increasing, all between one and m",
                         ACCENT_A, FS_TAG, x=-3.30, w=5.20),
               self._mid(-1.20, "排法只有一種：第 i 個階就是 i。於是每個樞紐直行都是標準基底向量",
                         "only one arrangement is possible: the ith order is i, so every pivot column is a standard basis vector",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.62, "化簡的終點只能是單位矩陣，不會是別的形狀",
                         "the reduction can only end at the identity, no other shape",
                         WARN, FS_TAG, w=11.9))

 def _inverse_example(self):
  """Chosen so that no fraction appears anywhere, unlike the first matrix one
  would reach for. The chain and the three elementary matrices below it were
  computed by the module; the product of the three is b."""
  xs = (-4.50, -1.50, 1.50, 4.50)
  g = VGroup()
  for cx, mat in zip(xs, INV_CHAIN):
   grid, _ = self._numgrid(cx, 0.85, [[FMT(v) for v in r] for r in mat],
                           dx=0.55, dy=0.42, size=FS_TAG - 3)
   g.add(grid)
  for k in range(3):
   mid = (xs[k] + xs[k + 1]) / 2
   g.add(self._arr([xs[k] + 0.72, 0.85, 0], [xs[k + 1] - 0.72, 0.85, 0], DIM, sw=2, tl=0.10),
         self._dash([mid, 0.78, 0], [mid, 0.44, 0], DIM, n=4, sw=1.4))
   u, _ = self._numgrid(mid, 0.02, [[FMT(v) for v in r] for r in INV_US[k]],
                        dx=0.42, dy=0.34, size=FS_TAG - 6, color=ACCENT_C)
   g.add(u, Text(f"u {'¹²³'[k]}", font_size=FS_TAG - 6, color=ACCENT_C)
         .move_to([mid, -0.50, 0]))
  bg, _ = self._numgrid(0.95, -1.05, [[FMT(v) for v in r] for r in B],
                        dx=0.55, dy=0.40, size=FS_TAG - 3, color=WARN)
  g.add(bg, Text("b   =   u ³ · u ² · u ¹   =", font_size=FS_TAG - 1, color=WARN)
        .move_to([-1.90, -1.05, 0]),
        Text("=   a ⁻¹", font_size=FS_TAG - 1, color=ACCENT_A).move_to([2.45, -1.05, 0]))
  return g.add(self._mid(-1.66, "三步就把 a 化成 e，全程沒有分數；b 乘 a 等於 e 是程式乘出來檢查過的",
                         "three steps take a to e with no fraction anywhere, and b times a was multiplied out and checked",
                         ACCENT_C, FS_TAG, w=11.9))

 def _augmented(self):
  """a | e reduced together: the same operations, one bookkeeping device."""
  xs = (-4.80, -1.60, 1.60, 4.80)
  g = VGroup()
  for k, (cx, mat) in enumerate(zip(xs, AUG_CHAIN)):
   last = k == len(xs) - 1
   hot = {(i, j) for i in range(2) for j in (2, 3)} if last else set()
   grid, pos = self._numgrid(cx, 0.72, [[FMT(v) for v in r] for r in mat],
                             dx=0.46, dy=0.42, size=FS_TAG - 3,
                             hot=hot, hotcolor=WARN)
   g.add(grid, self._dash([cx, pos(0, 0)[1] + 0.16, 0], [cx, pos(1, 0)[1] - 0.16, 0],
                          DIM, n=5, sw=1.8))
   if k:
    g.add(self._arr([xs[k - 1] + 1.10, 0.72, 0], [cx - 1.10, 0.72, 0], DIM, sw=2, tl=0.10))
  g.add(Text("a  |  e", font_size=FS_TAG - 1, color=ACCENT_B).move_to([-4.80, -0.25, 0]),
        Text("e  |  b", font_size=FS_TAG - 1, color=WARN).move_to([4.80, -0.25, 0]))
  return g.add(self._mid(-0.85, "同樣那三步，只是右半邊跟著一起做",
                         "the same three steps, with the right half carried along",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.28, "因為 b 乘 e 就是 b：右半邊記錄的正是那一串運算的乘積",
                         "because b times e is b: the right half records the product of the operations",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "左半邊變成 e 的時候，右半邊就是反矩陣，直接讀出來",
                         "when the left half is e, the right half is the inverse, ready to read off",
                         WARN, FS_TAG, w=11.9))

 def _two_ops(self):
  rows = ((0.95, "( 1′ )   α ᵢ  ↔  α ⱼ  ,  α ⱼ  →  − α ⱼ", ACCENT_B,
           "對調，並把搬下去的那一列變號", "interchange, and flip the sign of the one moved down"),
          (0.20, "( 3 )   α ᵢ  →  α ᵢ  −  x α ⱼ", WARN,
           "減去別列的倍數", "subtract a multiple of another row"))
  g = VGroup()
  for y, s, col, zh, en in rows:
   g.add(self._box(-2.60, y, s, col, w=6.00, h=0.62, size=FS_TAG - 1),
         self._mid(y, zh, en, col, FS_TAG - 1, x=3.60, w=4.80))
  g.add(self._box(-2.60, -0.60, "( 2 )   α ᵢ  →  c α ᵢ", DIM, w=6.00, h=0.62, size=FS_TAG - 1),
        self._mid(-0.60, "這一種不用：它會把行列式乘上 c",
                  "not this one: it multiplies the determinant by c",
                  DIM, FS_TAG - 1, x=3.60, w=4.80))
  return g.add(self._mid(-1.32, "前兩種都不改變行列式，所以整個過程算出來的還是原來那個數",
                         "the first two leave the determinant alone, so the number never changes",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "代價是首項不除成 1，最後停在一個「半簡化」的形狀",
                         "the price is not dividing by leading entries; we stop at a semireduced shape",
                         ACCENT_C, FS_TAG, w=11.9))

 def _semireduced(self):
  """The chain the module computed, with the interchange genuinely needed:
  the first row of this example has order two, so (1') comes first."""
  xs = (-4.84, -2.42, 0.00, 2.42, 4.84)
  g = VGroup()
  for k, ((mat, op), cx) in enumerate(zip(DET_CHAIN, xs)):
   last = k == len(xs) - 1
   grid, _ = self._numgrid(cx, 0.72, [[FMT(v) for v in r] for r in mat],
                           dx=0.42, dy=0.36, size=FS_TAG - 5,
                           hot={(i, i) for i in range(len(mat))} if last else set(),
                           hotcolor=WARN)
   g.add(grid)
   if k:
    g.add(self._arr([xs[k - 1] + 0.78, 0.72, 0], [cx - 0.78, 0.72, 0], DIM, sw=2, tl=0.09),
          Text(f"( {op} )", font_size=FS_TAG - 7, color=ACCENT_A)
          .move_to([(xs[k - 1] + cx) / 2, 1.00, 0]))
  prod = "  ·  ".join(FMT(v) for v in _diag(DET_S))
  g.add(self._box(0.00, -0.30, f"Δ ( a )   =   {prod}   =   {FMT(_det(DET_START))}",
                  WARN, w=6.60, h=0.62, size=FS_TAG - 1))
  return g.add(self._mid(-1.02, "第一列的階是 2，所以第一步真的必須對調，而且被搬下去的那一列變了號",
                         "the first row has order two, so the first step really is an interchange, with a sign change",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.42, "每個樞紐直行最後只剩自己那一個首項係數，這就是半簡化形",
                         "each pivot column ends up with only its own leading coefficient: that is semireduced",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "對角線相乘等於行列式，這個等式是程式核對過的",
                         "the diagonal product equals the determinant, and that was checked by computation",
                         DIM, FS_TAG, w=11.9))

 def _conclusion(self):
  """Two examples differing in one row: one nonsingular, one not. Both were
  semireduced by the same code, and both determinants were checked against a
  direct computation."""
  g = VGroup()
  sides = ((-3.40, DET_START, DET_S, ACCENT_C, "化得到 e", "reduces all the way to e"),
           (2.40, SING_START, SING_S, WARN, "化不到 e", "cannot reach e"))
  for cx, start, s, col, zh, en in sides:
   a, _ = self._numgrid(cx - 1.10, 0.68, [[FMT(v) for v in r] for r in start],
                        dx=0.42, dy=0.36, size=FS_TAG - 5,
                        hot={(2, j) for j in range(3)}, hotcolor=col)
   b, _ = self._numgrid(cx + 1.10, 0.68, [[FMT(v) for v in r] for r in s],
                        dx=0.42, dy=0.36, size=FS_TAG - 5,
                        hot={(i, i) for i in range(3)}, hotcolor=col)
   g.add(a, b, self._arr([cx - 0.34, 0.68, 0], [cx + 0.34, 0.68, 0], DIM, sw=2, tl=0.09),
         Text(f"Δ   =   {FMT(_det(start))}", font_size=FS_TAG - 1, color=col)
         .move_to([cx, -0.08, 0]),
         self._mid(-0.58, zh, en, col, FS_TAG, x=cx, w=4.60))
  g.add(self._box(0.00, -1.18, "d ( V ) = m      ⇔      Δ ( a ) ≠ 0      ⇔      ∃ a ⁻¹",
                  ACCENT_A, w=8.00, h=0.62, size=FS_TAG - 1))
  return g.add(self._mid(-1.78, "第 6 節到此結束。下一集進第 7 節：二次型的對角化",
                         "that finishes section six; next time, the diagonalization of a quadratic form",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  cp, fu, tm = self._column_picture(), self._find_u(), self._three_matrices()
  ip, ch, sc = self._inverse_pairs(), self._chain(), self._square_case()
  ie, ag, to = self._inverse_example(), self._augmented(), self._two_ops()
  sr, cc = self._semireduced(), self._conclusion()
  return [([cp], []), ([fu], [cp]), ([tm], [fu]), ([ip], [tm]),
          ([ch], [ip]), ([sc], [ch]), ([ie], [sc]), ([ag], [ie]),
          ([to], [ag]), ([sr], [to]), ([cc], [sr])]


AdvCalcE28ZH, AdvCalcE28EN = make(AdvCalcE28Base, "28", prefix="AdvCalcE")
