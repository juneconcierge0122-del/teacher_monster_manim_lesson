"""advcalc E30 -- Chapter 2, starred section 7, second part (book pp. 113-115):
the practical algorithm for reaching an orthogonal basis, the repair when the
diagonal is all zeros, clearing the first row and column, the recursion on what
is left, the worked example, why this is row *and* column reduction, and the
parity of a form with the two-dimensional shortcut it gives. Section 7 has no
exercises; chapter 3 opens on p. 116 and E31 starts there.

The algorithm is run here, not described. `_reduce` performs it in exact
arithmetic and returns every intermediate matrix together with the elementary
matrix that produced it, so the chain on screen is the chain the code walked.
The example is this episode's own, chosen by search rather than by hand against
four conditions the narration relies on: the diagonal starts all zero, so the
gamma-one repair is forced; the recursion on the trailing block actually fires;
every intermediate entry stays a whole number; and the result has both signs on
its diagonal. The assertions below pin each of those, along with the congruence
itself -- C-transpose T C really is the final diagonal -- and the determinant,
which is the same at every step and is what beat 10 is about.
"""
import pathlib, sys
from fractions import Fraction
from itertools import permutations
from math import isqrt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

START = [[0, 2, 1], [2, 0, -1], [1, -1, 0]]
NDIM = len(START)
SUB = "₁₂₃₄"


def _mul(a, b):
 return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
          for j in range(len(b[0]))] for i in range(len(a))]


def _tr(a):
 return [list(r) for r in zip(*a)]


def _fr(m):
 return [[Fraction(x) for x in r] for r in m]


def _eye(n):
 return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def _det(m):
 n, s = len(m), Fraction(0)
 for p in permutations(range(n)):
  sg = 1
  for i in range(n):
   for j in range(i + 1, n):
    if p[i] > p[j]:
     sg = -sg
  t = Fraction(sg)
  for i in range(n):
   t *= m[i][p[i]]
  s += t
 return s


def _reduce(t):
 """The section's procedure. Each step changes the basis by an elementary
 matrix e, and the matrix of the form changes by e-transpose . a . e --
 the same operation on the rows and on the columns, which is what keeps it
 symmetric. Returns [(matrix, e, label)], the first entry being the start."""
 n = len(t)
 a, out = _fr(t), None
 out = [(_fr(t), _eye(n), None)]
 for k in range(n):
  if a[k][k] == 0:
   j = next((j for j in range(k + 1, n) if a[k][j] != 0), None)
   if j is None:
    continue
   e = _eye(n)
   e[j][k] = Fraction(1)                        # gamma_k becomes gamma_k + gamma_j
   a = _mul(_tr(e), _mul(a, e))
   out.append(([r[:] for r in a], e, ("add", k, j)))
  if a[k][k] != 0 and any(a[k][j] != 0 for j in range(k + 1, n)):
   e = _eye(n)
   for j in range(k + 1, n):
    if a[k][j] != 0:
     e[k][j] = -a[k][j] / a[k][k]                # gamma_j becomes gamma_j + c gamma_k
   a = _mul(_tr(e), _mul(a, e))
   out.append(([r[:] for r in a], e, ("clear", k, None)))
 return out


CHAIN = _reduce(START)
FINAL = CHAIN[-1][0]
BASIS = _eye(NDIM)
for _m, _e, _op in CHAIN[1:]:
 BASIS = _mul(BASIS, _e)
DIAGONAL = [FINAL[i][i] for i in range(NDIM)]
P = sum(1 for v in DIAGONAL if v > 0)
NNEG = sum(1 for v in DIAGONAL if v < 0)
DET = _det(_fr(START))
NORM = isqrt(int(abs(DIAGONAL[0])))              # what normalizing divides beta-1 by
CORNER = CHAIN[1][0][0][0]                       # what the repair puts in the corner

# ── what the narration claims, checked rather than trusted ────────────────
assert START == _tr(START), "the example is not symmetric"
assert all(START[i][i] == 0 for i in range(NDIM)), \
    "the diagonal must start at zero, or the repair step is never forced"
assert len(CHAIN) == 4 and CHAIN[1][2][0] == "add", "want the repair, then two clearings"
assert CHAIN[2][2] == ("clear", 0, None) and CHAIN[3][2] == ("clear", 1, None), \
    "the recursion on the trailing block has to actually fire"
assert all(x.denominator == 1 for m, _, _ in CHAIN for r in m for x in r), \
    "an intermediate matrix left the whole numbers"
assert all(m == _tr(m) for m, _, _ in CHAIN), "a step broke the symmetry"
assert all(FINAL[i][j] == 0 for i in range(NDIM) for j in range(NDIM) if i != j), \
    "the end of the chain is not diagonal"
assert _mul(_tr(BASIS), _mul(_fr(START), BASIS)) == FINAL, \
    "the chain is not a congruence of the matrix it started from"
assert CORNER == 2 * START[0][1] != 0, "the repair did not put 2 t12 in the corner"
assert (P, NNEG) == (2, 1), "the narration says p is two and n is one"
assert all(_det(m) == DET for m, _, _ in CHAIN), "a step changed the determinant"
assert _det(_fr([r[:2] for r in START[:2]])) < 0, \
    "the two by two shortcut wants a negative determinant here"
assert NORM * NORM == abs(DIAGONAL[0]), "the normalizing divisor is not a whole number"

FMT = lambda v: str(v.numerator) if Fraction(v).denominator == 1 else \
    f"{Fraction(v).numerator}/{Fraction(v).denominator}"


def _vecs():
 """The basis the algorithm ended on, written in the basis it started from.

 This is what the procedure actually hands you, and it is the one thing the
 chain of matrices does not show: the columns of the accumulated change of
 basis, read off rather than retyped."""
 out = []
 for j in range(NDIM):
  terms = []
  for i in range(NDIM):
   c = BASIS[i][j]
   if not c:
    continue
   mag = "" if abs(c) == 1 else FMT(abs(c))
   terms.append(("−" if c < 0 else "+", f"{mag} α {SUB[i]}".strip()))
  t = "".join(f"  {sg}  {term}" for sg, term in terms).strip()
  out.append(f"β {SUB[j]}   =   {t[1:].strip() if t.startswith('+') else t}")
 return out


class AdvCalcE30Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 30

 MODE_LABEL = {
  0: {"zh": "歸納證明不告訴你怎麼算",
      "en": "an existence proof does not tell you how to compute"},
  1: {"zh": "先求正交，正規化留到最後", "en": "orthogonal first, normalize at the end"},
  2: {"zh": "先找一個對自己不取零的向量",
      "en": "first find a vector that does not vanish on itself"},
  3: {"zh": "對角線全是零時的補救", "en": "the repair when the diagonal is all zeros"},
  4: {"zh": "左上角那一格變成 2 t ₁₂", "en": "the corner becomes twice t-1-2"},
  5: {"zh": "把其餘向量推進核空間", "en": "push the other vectors into the null space"},
  6: {"zh": "第一列與第一行清乾淨", "en": "the first row and column, cleared"},
  7: {"zh": "對剩下那塊重複", "en": "repeat on what is left"},
  8: {"zh": "例子走到底", "en": "the example, run to the end"},
  9: {"zh": "列與行一起做", "en": "rows and columns at the same time"},
  10: {"zh": "奇偶性與二維的捷徑", "en": "parity, and the shortcut in two dimensions"},
 }

 def _grid(self, cx, cy, mat, **kw):
  return self._numgrid(cx, cy, [[FMT(v) for v in r] for r in mat],
                       dx=kw.pop("dx", 0.56), dy=kw.pop("dy", 0.46),
                       size=kw.pop("size", FS_TAG - 3), **kw)

 # ── beats ─────────────────────────────────────────────────────────
 def _why(self):
  g = VGroup(self._box(-3.40, 0.95, "∃  { β ᵢ }", DIM, w=4.40, h=0.62, size=FS_TAG),
             self._box(3.40, 0.95, "{ t ᵢⱼ }   →   { β ᵢ }", ACCENT_A,
                       w=4.40, h=0.62, size=FS_TAG))
  rows = ((0.20, "上一集：對維數作歸納", "last time: an induction on dimension",
           "這一集：一個真的能跑的程序", "this time: a procedure you can actually run"),
          (-0.36, "證明它一定在那裡", "it proves the basis is there",
           "把它算出來", "it produces the basis"),
          (-0.92, "但沒說怎麼找", "but not how to find it",
           "只用加減乘除", "using only add, subtract, multiply, divide"))
  for y, lzh, len_, rzh, ren in rows:
   g.add(self._mid(y, lzh, len_, DIM, FS_TAG, x=-3.40, w=4.20),
         self._mid(y, rzh, ren, ACCENT_C if y > -0.5 else WARN, FS_TAG, x=3.40, w=4.20))
  g.add(Line([0.00, -1.05, 0], [0.00, 1.26, 0], color=DIM, stroke_width=1.6))
  return g.add(self._mid(-1.40, "最後一步的開根號是唯一的例外，而且只在正規化時出現",
                         "the square root at the very end is the one exception, and only for normalizing",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "不必解多項式方程，這正是這個方法的價值",
                         "no polynomial equation ever has to be solved, and that is the point",
                         ACCENT_B, FS_TAG, w=11.9))

 def _two_stages(self):
  """Orthogonal first, normalized second, on the example's own numbers."""
  mid = [[FMT(v) if i == j else "0" for j, v in enumerate(r)] for i, r in enumerate(FINAL)]
  norm = [["1" if i == j and DIAGONAL[i] > 0 else "-1" if i == j else "0"
           for j in range(NDIM)] for i in range(NDIM)]
  g = VGroup()
  for cx, cells, col, zh, en in ((-3.30, mid, ACCENT_C, "正交：非對角線全是零",
                                  "orthogonal: every off-diagonal entry is zero"),
                                 (2.40, norm, WARN, "正規化：對角線只剩 ± 1",
                                  "normalized: the diagonal is only plus and minus one")):
   grid, _ = self._numgrid(cx, 0.42, cells, dx=0.62, dy=0.48, size=FS_TAG - 2,
                           hot={(i, i) for i in range(NDIM)}, hotcolor=col)
   g.add(grid, self._mid(-0.52, zh, en, col, FS_TAG, x=cx, w=4.60))
  g.add(self._arr([-1.20, 0.42, 0], [0.30, 0.42, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(0.78, "β ᵢ  /  √ | ω ( β ᵢ , β ᵢ ) |", ACCENT_A, FS_TAG - 1,
                  x=-0.45, w=2.20))
  return g.add(self._mid(-1.16, "第二步很簡單，難的全在第一步，所以先只求正交",
                         "the second step is easy and all the work is in the first, so aim for orthogonal",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "值是零的那些方向不必動，開根號也碰不到它們",
                         "directions where the value is zero are left alone; no square root touches them",
                         DIM, FS_TAG, w=11.9))

 def _find_pivot(self):
  grid, pos = self._grid(-3.60, 0.35, START, dx=0.66, dy=0.50, size=FS_TAG - 2,
                         hot={(i, i) for i in range(NDIM)}, hotcolor=WARN)
  g = VGroup(grid)
  for i in range(NDIM):
   g.add(Text(f"q ( α {SUB[i]} ) = 0", font_size=FS_TAG - 5, color=WARN)
         .move_to([pos(i, NDIM - 1)[0] + 1.20, pos(i, i)[1], 0]))
  return g.add(self._mid(1.00, "對角線上的 t ᵢᵢ 就是 q ( α ᵢ )",
                         "the diagonal entry t-i-i is exactly q of alpha-i",
                         ACCENT_A, FS_TAG, x=2.90, w=5.40),
               self._mid(-0.55, "有一格不是零，那個基底向量就能用",
                         "if one of them is not zero, that basis vector will do",
                         ACCENT_C, FS_TAG, x=2.90, w=5.40),
               self._mid(-1.16, "但這個例子三格都是零，一個現成的都沒有",
                         "but this example has three zeros and offers none",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "例子是挑過的，挑的就是這個最麻煩的情形",
                         "the example was chosen to be exactly this awkward case",
                         DIM, FS_TAG, w=11.9))

 def _repair(self):
  e = CHAIN[1][1]
  grid, _ = self._grid(-4.40, 0.30, e, dx=0.56, dy=0.46, hot={(1, 0)}, hotcolor=WARN)
  g = VGroup(grid, Text("e", font_size=FS_TAG, color=DIM).move_to([-4.40, -0.58, 0]))
  # the repair, drawn: two directions that pair with each other, added
  ox, oy = -0.80, -0.35
  g.add(self._arr([ox, oy, 0], [ox + 1.30, oy, 0], ACCENT_B, sw=2.5, tl=0.12),
        self._arr([ox, oy, 0], [ox, oy + 1.00, 0], ACCENT_C, sw=2.5, tl=0.12),
        self._arr([ox, oy, 0], [ox + 1.30, oy + 1.00, 0], WARN, sw=2.5, tl=0.12),
        self._dash([ox + 1.30, oy, 0], [ox + 1.30, oy + 1.00, 0], DIM, n=5, sw=1.4),
        self._dash([ox, oy + 1.00, 0], [ox + 1.30, oy + 1.00, 0], DIM, n=6, sw=1.4),
        Text("α ₁", font_size=FS_TAG - 3, color=ACCENT_B).move_to([ox + 0.65, oy - 0.28, 0]),
        Text("α ₂", font_size=FS_TAG - 3, color=ACCENT_C).move_to([ox - 0.34, oy + 0.55, 0]),
        Text("γ ₁", font_size=FS_TAG - 3, color=WARN).move_to([ox + 1.58, oy + 1.02, 0]))
  rows = ((0.62, "換基底的矩陣只動了一格", "the change of basis touches one entry", ACCENT_C),
          (0.00, "所以做得回去，還是一組基底",
           "so it can be undone and the list is still a basis", DIM),
          (-0.62, "q ( γ ₁ ) 不是零，即使 q ( α ₁ ) 與 q ( α ₂ ) 都是零",
           "q of gamma one is nonzero even though q of alpha one and alpha two are not",
           WARN))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=3.60, w=4.80))
  return g.add(self._mid(-1.16, "只要 ω 不是零形式，非對角線一定有一格不是零，這一步就走得下去",
                         "as long as omega is not the zero form some off-diagonal entry is nonzero, and this step goes through",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "把兩個互相配不出零的方向加在一起，讓它跟自己配得出東西",
                         "add two directions that pair with each other, and the sum pairs with itself",
                         ACCENT_B, FS_TAG, w=11.9))

 def _corner(self):
  a, b = CHAIN[0][0], CHAIN[1][0]
  g = VGroup()
  for cx, mat, col, hot in ((-3.90, a, ACCENT_B, {(0, 1), (1, 0), (0, 0), (1, 1)}),
                            (-0.30, b, WARN, {(0, 0)})):
   grid, _ = self._grid(cx, 0.42, mat, hot=hot, hotcolor=col)
   g.add(grid)
  g.add(self._arr([-2.30, 0.42, 0], [-1.60, 0.42, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(-0.48, f"s ₁₁  =  {FMT(a[0][0])} + 2 · {FMT(a[0][1])} + {FMT(a[1][1])}"
                         f"  =  {FMT(b[0][0])}", WARN, FS_TAG, x=-2.10, w=5.40))
  return g.add(self._mid(0.85, "對角線是零時，前後兩項都消失",
                         "with a zero diagonal the two outer terms vanish",
                         DIM, FS_TAG, x=3.40, w=4.80),
               self._mid(0.20, "只剩中間的兩倍 t ₁₂", "only twice t-1-2 is left",
                         ACCENT_C, FS_TAG, x=3.40, w=4.80),
               self._mid(-1.16, "這個數保證不是零，接下來才有東西可以拿來除",
                         "that number is guaranteed nonzero, which is what the next step divides by",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "左邊那個矩陣的四格是自己乘出來的，不是抄的",
                         "the four entries on the left were multiplied out, not copied",
                         DIM, FS_TAG, w=11.9))

 def _push(self):
  g = VGroup(self._sym(1.02, "ω ( γ ⱼ + c γ ₁ , γ ₁ )   =   s ₁ⱼ  +  c  s ₁₁   =   0",
                       ACCENT_A, FS_TAG, x=0.00, w=8.60))
  s = CHAIN[1][0]
  rows = [(0.34, f"j = 2 :   c  =  −  {FMT(s[0][1])} / {FMT(s[0][0])}"
                 f"  =  {FMT(-Fraction(s[0][1], s[0][0]))}", WARN)]
  if s[0][2]:
   rows.append((-0.24, f"j = 3 :   c  =  −  {FMT(s[0][2])} / {FMT(s[0][0])}"
                       f"  =  {FMT(-Fraction(s[0][2], s[0][0]))}", WARN))
  else:
   rows.append((-0.24, "j = 3 :   s ₁₃ = 0   ,   c = 0", DIM))
  for y, t, col in rows:
   g.add(self._sym(y, t, col, FS_TAG, x=0.00, w=7.40))
  return g.add(self._mid(-0.86, "要 γ ⱼ 跟 γ ₁ 配出零，c 就只有一個選擇",
                         "asking gamma j to pair with gamma one to zero leaves one choice of c",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.32, "分母就是上一步弄出來的那個非零數",
                         "the denominator is the nonzero number the previous step produced",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "s ₁₃ 本來就是零的話，那一個方向不必動",
                         "where s-1-3 is already zero that direction needs no change",
                         DIM, FS_TAG, w=11.9))

 def _cleared(self):
  a, b = CHAIN[1][0], CHAIN[2][0]
  g = VGroup()
  hot = {(0, j) for j in range(1, NDIM)} | {(i, 0) for i in range(1, NDIM)}
  for cx, mat, col in ((-3.90, a, ACCENT_B), (-0.30, b, ACCENT_C)):
   grid, _ = self._grid(cx, 0.40, mat, hot=hot, hotcolor=col)
   g.add(grid)
  g.add(self._arr([-2.30, 0.40, 0], [-1.60, 0.40, 0], ACCENT_A, sw=2.5, tl=0.12))
  return g.add(self._mid(0.80, "第一列與第一行清乾淨", "the first row and column are cleared",
                         ACCENT_C, FS_TAG, x=3.40, w=4.80),
               self._mid(0.15, "左上角那一格留著不動", "the corner entry stays where it is",
                         DIM, FS_TAG, x=3.40, w=4.80),
               self._mid(-0.50, "對稱一路都在", "symmetry survives every step",
                         WARN, FS_TAG, x=3.40, w=4.80),
               self._mid(-1.16, "第一個基底向量已經跟其他每一個都配出零了",
                         "the first basis vector now pairs to zero with every other one",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "它這輩子不會再被動到",
                         "it is finished and will not be touched again",
                         DIM, FS_TAG, w=11.9))

 def _recurse(self):
  b = CHAIN[2][0]
  grid, pos = self._grid(-3.30, 0.35, b, dx=0.66, dy=0.50, size=FS_TAG - 2,
                         hot={(i, j) for i in range(1, NDIM) for j in range(1, NDIM)},
                         hotcolor=WARN)
  g = VGroup(grid)
  x0, x1 = pos(1, 1)[0] - 0.34, pos(NDIM - 1, NDIM - 1)[0] + 0.34
  y0, y1 = pos(NDIM - 1, NDIM - 1)[1] - 0.30, pos(1, 1)[1] + 0.30
  g.add(self._brackets(x0, x1, y0, y1, color=WARN, d=0.12, sw=2))
  rows = ((0.92, "剩下的是一個少一維的同樣問題",
           "what is left is the same problem, one dimension down", ACCENT_A),
          (0.26, "對這一塊重複第 2 到第 6 拍",
           "run beats two through six again on this block", ACCENT_C),
          (-0.40, "一直做到沒有非對角線的格子",
           "keep going until no off-diagonal entry is left", WARN))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.70, w=5.60))
  return g.add(self._mid(-1.16, "這個例子的那一塊還不是對角的，所以遞迴真的會跑一次",
                         "this example's block is not diagonal yet, so the recursion really does run",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "過程有點長，但每一步都只是加減乘除",
                         "the process is long, but every step is plain arithmetic",
                         DIM, FS_TAG, w=11.9))

 def _example(self):
  xs = (-4.86, -1.62, 1.62, 4.86)
  g = VGroup()
  for k, ((mat, _e, op), cx) in enumerate(zip(CHAIN, xs)):
   last = k == len(CHAIN) - 1
   grid, _ = self._grid(cx, 0.62, mat, dx=0.46, dy=0.40, size=FS_TAG - 5,
                        hot={(i, i) for i in range(NDIM)} if last else set(),
                        hotcolor=WARN)
   g.add(grid)
   if k:
    zh = "γ ₁ + γ ₂" if op[0] == "add" else f"清第 {op[1] + 1} 列"
    en = "γ ₁ + γ ₂" if op[0] == "add" else f"clear {op[1] + 1}"
    g.add(self._arr([xs[k - 1] + 0.92, 0.62, 0], [cx - 0.92, 0.62, 0], DIM, sw=2, tl=0.09))
    g.add(self._mid(0.94, zh, en, ACCENT_A, FS_TAG - 5,
                    x=(xs[k - 1] + cx) / 2, w=1.60))
  # the formula bar already has the diagonal and the three numbers, so the
  # frame shows the basis those matrices were quietly accumulating instead
  for k, line in enumerate(_vecs()):
   g.add(self._sym(-0.24 - k * 0.40, line, WARN if k == 0 else ACCENT_C,
                   FS_TAG - 1, x=0.00, w=7.00))
  return g.add(self._mid(-1.44, f"要正規化只剩一件事：第一個基底向量除以 {NORM}",
                         f"one thing remains for normalizing: divide the first basis vector by {NORM}",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "這四個矩陣是程式跑出來的，而且驗過它們確實是同一個形式",
                         "these four matrices were computed, and checked to be the same form throughout",
                         DIM, FS_TAG, w=11.9))

 def _rows_and_columns(self):
  """Why this is not row reduction: both bases move, so both sides multiply."""
  e = CHAIN[2][1]
  g = VGroup()
  parts = ((-4.60, _tr(e), "e ᵀ", ACCENT_C), (-1.55, CHAIN[1][0], "a", ACCENT_B),
           (1.50, e, "e", ACCENT_C))
  for cx, mat, name, col in parts:
   grid, _ = self._grid(cx, 0.45, mat, dx=0.50, dy=0.42, size=FS_TAG - 5, color=col)
   g.add(grid, Text(name, font_size=FS_TAG - 1, color=col).move_to([cx, -0.40, 0]))
  for x in (-3.05, 0.00):
   g.add(Text("·", font_size=FS_TAG + 2, color=DIM).move_to([x, 0.45, 0]))
  g.add(Text("=", font_size=FS_TAG + 2, color=DIM).move_to([2.95, 0.45, 0]))
  grid, _ = self._grid(4.50, 0.45, CHAIN[2][0], dx=0.50, dy=0.42, size=FS_TAG - 5,
                       color=WARN)
  g.add(grid, Text("a ′", font_size=FS_TAG - 1, color=WARN).move_to([4.50, -0.40, 0]))
  return g.add(self._mid(-0.94, "左邊那個做列運算，右邊那個做行運算，而且是同一個 e",
                         "the left factor works on rows, the right on columns, and it is the same e",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.38, "因為 T 從 V 到 V*，定義域與值域的基底同時在換",
                         "because T runs from V to V star, both bases change together",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "要讓對稱矩陣做完還是對稱，本來也只能這樣做",
                         "and it is the only way a symmetric matrix comes out symmetric",
                         WARN, FS_TAG, w=11.9))

 def _parity(self):
  g = VGroup()
  for k, ((mat, _e, _op), cx) in enumerate(zip(CHAIN, (-5.00, -1.90, 1.20, 4.30))):
   grid, _ = self._grid(cx, 0.72, mat, dx=0.38, dy=0.34, size=FS_TAG - 7, color=DIM)
   g.add(grid, Text(f"Δ = {FMT(_det(mat))}", font_size=FS_TAG - 4, color=WARN)
         .move_to([cx, -0.02, 0]))
  two = [r[:2] for r in START[:2]]
  g.add(self._sym(-0.62, f"t ₁₁ t ₂₂ − t ₁₂²   =   {FMT(_det(_fr(two)))}   <   0"
                         "        ⇒        σ = 0", ACCENT_A, FS_TAG, x=0.00, w=8.60))
  return g.add(self._mid(-1.16, "換基底只把行列式乘上一個平方數，所以正負號永遠不變",
                         "changing basis multiplies the determinant by a square, so its sign never moves",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.50, "二維時這就夠了：行列式是負的，符號差一定是零",
                         "in two dimensions that is enough: a negative determinant forces signature zero",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集離開線性代數，進第 3 章的極限與範數",
                         "next time we leave linear algebra for chapter three, limits and norms",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  wh, ts, fp = self._why(), self._two_stages(), self._find_pivot()
  rp, cn, pu = self._repair(), self._corner(), self._push()
  cl, rc, ex = self._cleared(), self._recurse(), self._example()
  rw, pa = self._rows_and_columns(), self._parity()
  return [([wh], []), ([ts], [wh]), ([fp], [ts]), ([rp], [fp]),
          ([cn], [rp]), ([pu], [cn]), ([cl], [pu]), ([rc], [cl]),
          ([ex], [rc]), ([rw], [ex]), ([pa], [rw])]


AdvCalcE30ZH, AdvCalcE30EN = make(AdvCalcE30Base, "30", prefix="AdvCalcE")
