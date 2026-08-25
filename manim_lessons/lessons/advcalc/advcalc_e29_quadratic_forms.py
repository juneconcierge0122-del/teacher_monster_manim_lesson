"""advcalc E29 -- Chapter 2, starred section 7, first part (book pp. 111-113):
a bilinear functional and its matrix, the quadratic form it carries, recovering
a symmetric form from its quadratic form, omega-orthonormal bases, Theorem 7.1
by induction on dimension, Theorem 7.2 and the canonical form, and the fact
that p and n do not depend on the basis. E30 takes pp. 113-115, the practical
algorithm. Section 7 has no exercise set; chapter 3 opens on p. 116.

The example is this episode's own and is built backwards, which is the only
honest way to have one here: E30 is where the algorithm to find a canonical
form appears, so E29 cannot pretend to run it. Instead T is *constructed* as
C-transpose D C from a chosen D = diag(1, 1, -1, 0) and an integer unimodular
C, and then an independent congruence routine re-derives the diagonal from T
alone. The assertions check that the two agree -- that the example really does
have p = 2, n = 1 and a one-dimensional null direction -- along with the
polarization identity and the scaling step, on this same T.
"""
import pathlib, sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Ellipse, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

DIAG = [1, 1, -1, 0]                                  # the shape we want to reach
CMAT = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]
NDIM = len(DIAG)


def _mul(a, b):
 return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
          for j in range(len(b[0]))] for i in range(len(a))]


def _tr(a):
 return [list(r) for r in zip(*a)]


def _congruence(m):
 """Symmetric elimination: the same operation on rows and on columns, which
 is what keeps a symmetric matrix symmetric. Returns the diagonal reached.

 This is E30's algorithm, used here only to check the example: the diagonal
 it finds has to match the one the example was built from."""
 a = [[Fraction(x) for x in r] for r in m]
 n = len(a)
 for k in range(n):
  if a[k][k] == 0:
   j = next((j for j in range(k + 1, n) if a[j][j] != 0), None)
   if j is not None:
    a[k], a[j] = a[j], a[k]
    for r in a:
     r[k], r[j] = r[j], r[k]
   else:
    j = next((j for j in range(k + 1, n) if a[k][j] != 0), None)
    if j is None:
     continue
    for c in range(n):
     a[k][c] += a[j][c]
    for r in a:
     r[k] += r[j]
  for i in range(k + 1, n):
   f = a[i][k] / a[k][k]
   if f:
    for c in range(n):
     a[i][c] -= f * a[k][c]
    for r in a:
     r[i] -= f * r[k]
 return [a[i][i] for i in range(n)]


def _rank(m):
 a = [[Fraction(x) for x in r] for r in m]
 rows, piv = len(a), 0
 for col in range(len(a[0])):
  r = next((i for i in range(piv, rows) if a[i][col] != 0), None)
  if r is None:
   continue
  a[piv], a[r] = a[r], a[piv]
  for i in range(rows):
   if i != piv and a[i][col] != 0:
    f = a[i][col] / a[piv][col]
    a[i] = [p - f * q for p, q in zip(a[i], a[piv])]
  piv += 1
 return piv


T = [[int(x) for x in r] for r in
     _mul(_tr([[Fraction(x) for x in r] for r in CMAT]),
          _mul([[Fraction(int(i == j)) * DIAG[i] for j in range(NDIM)] for i in range(NDIM)],
               [[Fraction(x) for x in r] for r in CMAT]))]

omega = lambda x, y: sum(T[i][j] * x[i] * y[j] for i in range(NDIM) for j in range(NDIM))
q = lambda x: omega(x, x)

FOUND = _congruence(T)
P = sum(1 for v in FOUND if v > 0)
NNEG = sum(1 for v in FOUND if v < 0)
NZERO = sum(1 for v in FOUND if v == 0)

BETA = [2, 0, 0, 0]                      # q = 4, so halving it lands on 1
SCALE = Fraction(1, 2)
ALPHA = [int(SCALE * v) for v in BETA]
XI, ETA = [1, 0, 1, 0], [0, 1, 0, 1]

# ── what the narration claims, checked rather than trusted ────────────────
assert T == _tr(T), "the example is not symmetric"
assert [sum(1 for v in FOUND if v > 0), sum(1 for v in FOUND if v < 0)] == \
       [sum(1 for v in DIAG if v > 0), sum(1 for v in DIAG if v < 0)], \
       "the congruence routine does not recover the signature it was built from"
assert (P, NNEG, NZERO) == (2, 1, 1), "want two plus, one minus and a zero"
assert _rank(T) == P + NNEG == 3, "the rank is not p + n"
assert all(abs(v) <= 2 for r in T for v in r), "the example got too big to read"
# polarization: a symmetric form is recoverable from its quadratic form alone
XI_PLUS = [a + b for a, b in zip(XI, ETA)]
XI_MINUS = [a - b for a, b in zip(XI, ETA)]
assert Fraction(q(XI_PLUS) - q(XI_MINUS), 4) == omega(XI, ETA), "polarization fails"
assert omega(XI, ETA) == omega(ETA, XI), "the example is not symmetric on these two"
# the one-dimensional step: scaling moves the value to exactly one
assert q(BETA) == 4 and q(ALPHA) == 1 and SCALE ** 2 * q(BETA) == q(ALPHA), "scaling is wrong"

FMT = lambda v: str(int(v))
SUB = "₁₂₃₄₅"


def _terms(t, want):
 """The terms of the quadratic form that a symmetric matrix produces.

 `want` picks the diagonal entries or the off-diagonal pairs, because the two
 arrive differently: t-i-i contributes one square, while t-i-j and t-j-i are
 the same number twice and arrive as a doubled cross term. Written out from
 the matrix rather than typed, so it cannot drift from the example."""
 out = []
 for i in range(len(t)):
  for j in range(i, len(t)):
   if (i == j) != (want == "diagonal"):
    continue
   c = t[i][j] * (1 if i == j else 2)
   if not c:
    continue
   term = f"x {SUB[i]}²" if i == j else f"x {SUB[i]} x {SUB[j]}"
   mag = "" if abs(c) == 1 else str(abs(c))
   out.append(("−" if c < 0 else "+", f"{mag} {term}".strip()))
 return out


def _join(out):
 s = "".join(f"  {sign}  {term}" for sign, term in out).strip()
 return s[1:].strip() if s.startswith("+") else s


def _poly(t):
 return _join(_terms(t, "diagonal") + _terms(t, "cross"))


class AdvCalcE29Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 29

 MODE_LABEL = {
  0: {"zh": "一個比較小、但做得成的問題",
      "en": "a smaller problem, and one that can be solved"},
  1: {"zh": "ω 選了基底就有矩陣", "en": "choose a basis and omega has a matrix"},
  2: {"zh": "雙重和與二次型", "en": "the double sum and the quadratic form"},
  3: {"zh": "對稱時，q 反過來決定 ω",
      "en": "when omega is symmetric, q determines it back"},
  4: {"zh": "目標：ω 正交規範基底", "en": "the goal: a basis orthonormal for omega"},
  5: {"zh": "一維：把值調成 ±1",
      "en": "dimension one: scale the value to plus or minus one"},
  6: {"zh": "配 α ₙ 的那個泛函，核空間少一維",
      "en": "pairing against alpha-n: a null space one dimension down"},
  7: {"zh": "歸納：把 N 的基底接上 α ₙ",
      "en": "the induction: N's basis, with alpha-n added"},
  8: {"zh": "定理 7.2：只剩平方項", "en": "theorem 7.2: only square terms are left"},
  9: {"zh": "p 與 n 不依賴基底", "en": "p and n do not depend on the basis"},
  10: {"zh": "符號差與秩", "en": "the signature and the rank"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _two_problems(self):
  """The section's own framing: the hard problem set beside the one it does."""
  g = VGroup()
  for cx, head, col, rows in (
      (-3.30, "T  ∈  Hom ( V , V )", DIM,
       (("挑一組基底讓矩陣簡單", "choose a basis making the matrix simple"),
        ("這是線性代數最難的部分", "this is the hard part of the subject"),
        ("本書只碰到定理 5.5 那一角", "this book only touches theorem 5.5 of it"))),
      (3.30, "T  ∈  Hom ( V , V* )", ACCENT_A,
       (("等價於 V 上的一個雙線性泛函", "equivalent to a bilinear functional on V"),
        ("這一節把它完全解決", "this section settles it completely"),
        ("代價是換了一個目標空間", "the price is a different target space")))):
   g.add(self._box(cx, 0.95, head, col, w=5.20, h=0.62, size=FS_TAG))
   for k, (zh, en) in enumerate(rows):
    g.add(self._mid(0.25 - k * 0.58, zh, en, col if k == 0 else DIM,
                    FS_TAG, x=cx, w=5.00))
  g.add(Line([0.00, -1.05, 0], [0.00, 1.26, 0], color=DIM, stroke_width=1.6))
  return g.add(self._mid(-1.32, "兩個問題只差一個星號：右邊那個是加了星號的第 7 節",
                         "one star between them: the right-hand one is starred section seven",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.78, "做不到的先放著，先把做得到的做乾淨",
                         "leave the one you cannot do; finish the one you can",
                         ACCENT_A, FS_TAG, w=11.9))

 def _matrix_of_omega(self):
  """omega takes two basis vectors and returns the entry they name."""
  g = VGroup(self._box(-4.60, 0.72, "α ᵢ", ACCENT_B, w=1.30, h=0.52),
             self._box(-4.60, -0.12, "α ⱼ", ACCENT_C, w=1.30, h=0.52),
             self._box(-2.60, 0.30, "ω", ACCENT_A, w=1.30, h=0.90, size=FS_TAG + 3),
             self._arr([-3.90, 0.72, 0], [-3.30, 0.48, 0], ACCENT_B, sw=2, tl=0.10),
             self._arr([-3.90, -0.12, 0], [-3.30, 0.12, 0], ACCENT_C, sw=2, tl=0.10),
             self._arr([-1.90, 0.30, 0], [-1.20, 0.30, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("t ᵢⱼ", font_size=FS_TAG + 1, color=WARN).move_to([-0.70, 0.30, 0]))
  cells = [["·"] * NDIM for _ in range(NDIM)]
  cells[1][2] = "t ᵢⱼ"
  grid, pos = self._numgrid(2.90, 0.10, cells, dx=0.72, dy=0.46, size=FS_TAG - 2,
                            hot={(1, 2)}, hotcolor=WARN)
  g.add(grid,
        Text("i", font_size=FS_TAG - 3, color=ACCENT_B)
        .move_to([pos(1, 0)[0] - 0.72, pos(1, 0)[1], 0]),
        Text("j", font_size=FS_TAG - 3, color=ACCENT_C)
        .move_to([pos(0, 2)[0], pos(0, 2)[1] + 0.38, 0]))
  return g.add(self._mid(-1.10, "第 i 列第 j 行那一格，就是 ω 吃這兩個基底向量給出的數",
                         "the entry in row i and column j is what omega returns on those two",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "換一組基底就換一個矩陣，但講的是同一個 ω",
                         "another basis gives another matrix, still describing the same omega",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "這正是第 4 節那本字典，只是這回兩個槽都吃 V 的向量",
                         "the same dictionary as section four, with both slots taking vectors of V",
                         ACCENT_C, FS_TAG, w=11.9))

 def _double_sum(self):
  """The example enters here. The formula bar already carries the double sum
  and the definition of q, so the frame shows the thing the bar cannot: which
  part of this matrix produces which part of this polynomial."""
  grid, _ = self._numgrid(-4.30, 0.40, [[FMT(v) for v in r] for r in T],
                          dx=0.52, dy=0.44, size=FS_TAG - 3, color=ACCENT_C,
                          hot={(i, i) for i in range(NDIM)}, hotcolor=WARN)
  g = VGroup(grid, Text("t", font_size=FS_TAG, color=DIM).move_to([-4.30, -0.62, 0]))
  g.add(self._sym(0.92, "q ( ξ )   =   " + _poly(T), ACCENT_A, FS_TAG, x=1.40, w=8.60),
        self._mid(0.28, "對角線那 4 格各給一個平方項：" + _join(_terms(T, "diagonal")),
                  "each diagonal entry gives one square: " + _join(_terms(T, "diagonal")),
                  WARN, FS_TAG, x=1.40, w=8.60),
        self._mid(-0.34, "非對角線成對出現，所以各帶一個 2：" + _join(_terms(T, "cross")),
                  "off-diagonal entries come in pairs, so each carries a 2: "
                  + _join(_terms(T, "cross")),
                  ACCENT_C, FS_TAG, x=1.40, w=8.60))
  return g.add(self._mid(-1.02, "兩個槽放同一個 ξ，得到的就是座標的齊次二次多項式",
                         "put the same xi in both slots and you get a homogeneous quadratic in the coordinates",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "這三行都是從左邊那個矩陣算出來的，不是手寫的",
                         "all three lines were generated from the matrix on the left, not written out",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "二次型與矩陣是同一件事的兩種寫法",
                         "the form and the matrix are two ways of writing one thing",
                         ACCENT_B, FS_TAG, w=11.9))

 def _polarization(self):
  """Symmetry, and the identity that gets omega back from q -- checked on the
  example rather than asserted at the viewer.

  Symmetry is drawn as the matrix beside its own transpose rather than as a
  line down the diagonal: that line would lie on the diagonal entries and
  cover them, which is what tools/collide.py reports if you try it."""
  g = VGroup()
  hot = {(i, j) for i in range(NDIM) for j in range(NDIM) if i != j and T[i][j]}
  for cx, mat, name in ((-4.30, T, "t"), (-1.10, _tr(T), "t ᵀ")):
   grid, _ = self._numgrid(cx, 0.30, [[FMT(v) for v in r] for r in mat],
                           dx=0.46, dy=0.42, size=FS_TAG - 4, hot=hot, hotcolor=ACCENT_C)
   g.add(grid, Text(name, font_size=FS_TAG - 1, color=DIM).move_to([cx, -0.70, 0]))
  g.add(Text("=", font_size=FS_TAG + 2, color=ACCENT_C).move_to([-2.70, 0.30, 0]))
  xi = "⟨ " + " , ".join(FMT(v) for v in XI) + " ⟩"
  eta = "⟨ " + " , ".join(FMT(v) for v in ETA) + " ⟩"
  rows = ((0.86, f"ξ = {xi}        η = {eta}", DIM),
          (0.30, f"ω ( ξ , η )   =   {FMT(omega(XI, ETA))}", WARN),
          (-0.26, f"[ {FMT(q(XI_PLUS))} − ( {FMT(q(XI_MINUS))} ) ] / 4   =   "
                  f"{FMT(Fraction(q(XI_PLUS) - q(XI_MINUS), 4))}", WARN))
  for y, t, col in rows:
   g.add(self._sym(y, t, col, FS_TAG - 1, x=3.40, w=5.20))
  return g.add(self._mid(-1.40, "對稱就是矩陣等於自己的轉置：高亮的每一對是同一個數",
                         "symmetry is the matrix equalling its own transpose: each highlighted pair is one number",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "所以談二次型跟談對稱雙線性泛函，是同一件事",
                         "so quadratic forms and symmetric bilinear functionals are one subject",
                         ACCENT_A, FS_TAG, w=11.9))

 def _target(self):
  """What we are trying to reach, drawn with this example's own p, n and z."""
  cells = [[FMT(DIAG[i]) if i == j else "0" for j in range(NDIM)] for i in range(NDIM)]
  grid, pos = self._numgrid(-3.40, 0.25, cells, dx=0.66, dy=0.50, size=FS_TAG - 2,
                            hot={(i, i) for i in range(NDIM)}, hotcolor=WARN)
  g = VGroup(grid)
  for i, v in enumerate(DIAG):
   col = ACCENT_C if v > 0 else (WARN if v < 0 else DIM)
   g.add(Dot([pos(i, i)[0] + 0.52, pos(i, i)[1], 0], radius=0.055, color=col))
  rows = ((1.00, "不同的基底向量互相取零", "distinct basis vectors give zero against each other",
           ACCENT_A),
          (0.34, "每個對自己只給 0 、 1 或 − 1", "each gives itself only 0, 1 or minus 1", WARN),
          (-0.32, "這種基底叫 ω 正交規範基底", "such a basis is called orthonormal for omega",
           ACCENT_C))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.70, w=5.80))
  return g.add(self._mid(-1.20, "「正交規範」這個詞是跟內積借來的，內積本身要等到第 5 章",
                         "the word orthonormal is borrowed from scalar products, which wait for chapter five",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "定理 7.1 說這種基底一定存在，證明是對維數作歸納",
                         "theorem 7.1 says such a basis always exists, by induction on dimension",
                         ACCENT_B, FS_TAG, w=11.9))

 def _scale(self):
  """The one-dimensional case, on a vector of the example itself."""
  g = VGroup(self._sym(1.02, "q ( x β )   =   x ²  q ( β )", ACCENT_A, FS_TAG + 1,
                       x=0.00, w=5.40))
  y0 = 0.30
  g.add(Line([-5.00, y0, 0], [3.40, y0, 0], color=DIM, stroke_width=1.6))
  marks = ((-4.20, "β", f"q = {FMT(q(BETA))}", ACCENT_B),
           (-0.40, "α  =  β / 2", f"q = {FMT(q(ALPHA))}", WARN))
  for x, name, val, col in marks:
   g.add(Dot([x, y0, 0], radius=0.075, color=col),
         Text(name, font_size=FS_TAG, color=col).move_to([x, y0 + 0.34, 0]),
         Text(val, font_size=FS_TAG - 2, color=col).move_to([x, y0 - 0.38, 0]))
  g.add(self._arr([-4.20, y0 - 0.72, 0], [-0.40, y0 - 0.72, 0], ACCENT_A, sw=2, tl=0.10),
        self._sym(y0 - 1.06, "x   =   1 / √ | q ( β ) |   =   1 / 2", ACCENT_A, FS_TAG,
                  x=-2.30, w=4.40))
  return g.add(self._mid(-1.00, "縮放不改變方向，只把值乘上 x 的平方",
                         "scaling keeps the direction and multiplies the value by x squared",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.38, "所以只要 q ( β ) 不是零，就能把它調成正一或負一",
                         "so as long as q of beta is not zero, it can be scaled to one or minus one",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.74, "這個例子的 β 與 α 都是實際代進去算過的",
                         "beta and alpha here were both put through the form and evaluated",
                         DIM, FS_TAG, w=11.9))

 def _null_space(self):
  """The functional that pairs against alpha-n, and the space it kills."""
  g = VGroup(Ellipse(width=4.60, height=2.00, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.06).move_to([-3.30, 0.05, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-3.30, 1.18, 0]),
             Line([-5.10, -0.20, 0], [-1.50, -0.20, 0], color=ACCENT_C, stroke_width=3),
             Text("N", font_size=FS_TAG, color=ACCENT_C).move_to([-1.15, -0.20, 0]),
             self._arr([-3.30, -0.20, 0], [-3.30, 0.62, 0], WARN, sw=2.5, tl=0.12),
             Text("α ₙ", font_size=FS_TAG, color=WARN).move_to([-2.90, 0.62, 0]))
  # what f does, rather than the three equations the formula bar already has.
  # The labels sit to the right of the axis and the arrows stop short of it,
  # so nothing is drawn over a number (E22 ran its arrows across the 0).
  ax = 3.90
  g.add(Line([ax, -0.55, 0], [ax, 0.98, 0], color=DIM, stroke_width=2),
        Text("ℝ", font_size=FS_TAG, color=DIM).move_to([ax, 1.18, 0]))
  for y, lab, col, src in ((0.00, "0", ACCENT_C, -0.20), (0.66, "± 1", WARN, 0.62)):
   g.add(Line([ax - 0.12, y, 0], [ax + 0.12, y, 0], color=col, stroke_width=2.5),
         Text(lab, font_size=FS_TAG - 1, color=col).move_to([ax + 0.48, y, 0]),
         self._arr([1.30, src, 0], [ax - 0.22, y, 0], col, sw=2, tl=0.10))
  g.add(self._mid(0.66, "α ₙ 被送到 ± 1", "alpha-n goes to plus or minus one",
                  WARN, FS_TAG, x=0.10, w=2.20),
        self._mid(-0.20, "N 整個被送到 0", "all of N goes to 0",
                  ACCENT_C, FS_TAG, x=0.10, w=2.20))
  return g.add(self._mid(-1.20, "f 不是零泛函，因為 f 作用在 α ₙ 上就等於 ± 1",
                         "f is not the zero functional, since f at alpha-n is plus or minus one",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "非零泛函的核空間剛好少一維——這就是歸納可以往下接的地方",
                         "a nonzero functional has a null space one dimension down, which is where the induction goes",
                         ACCENT_C, FS_TAG, w=11.9))

 def _induction(self):
  g = VGroup(Ellipse(width=4.60, height=2.00, color=DIM, stroke_width=2,
                     fill_opacity=0.0).move_to([-3.30, 0.05, 0]),
             Line([-5.10, -0.15, 0], [-1.50, -0.15, 0], color=ACCENT_C, stroke_width=3),
             Text("N", font_size=FS_TAG, color=ACCENT_C).move_to([-1.15, -0.15, 0]),
             self._arr([-3.30, -0.15, 0], [-3.30, 0.68, 0], WARN, sw=2.5, tl=0.12),
             Text("α ₙ", font_size=FS_TAG, color=WARN).move_to([-2.90, 0.68, 0]))
  for k, x in enumerate((-4.50, -3.90, -2.70)):
   g.add(Dot([x, -0.15, 0], radius=0.06, color=ACCENT_C),
         Text("α " + ("₁" if k == 0 else "₂" if k == 1 else "ₙ₋₁"),
              font_size=FS_TAG - 5, color=ACCENT_C).move_to([x, -0.52, 0]))
  rows = ((1.05, "N 的維數比較小，歸納假設直接給一組正交規範基底",
           "N is smaller, so the inductive hypothesis hands it an orthonormal basis", ACCENT_C),
          (0.35, "N 裡的向量跟 α ₙ 配出來都是零——那就是 N 的定義",
           "vectors of N pair with alpha-n to zero, which is what N means", WARN),
          (-0.35, "接起來就是整個 V 的正交規範基底",
           "put them together and V has one too", ACCENT_A))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.70, w=5.80))
  return g.add(self._mid(-1.20, "n = 1 的情形前一拍已經做完，歸納可以起步",
                         "the case n = 1 was done a beat ago, so the induction has a base",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "這就是定理 7.1：對稱雙線性泛函一定有正交規範基底",
                         "that is theorem 7.1: a symmetric bilinear functional always has one",
                         ACCENT_B, FS_TAG, w=11.9))

 def _canonical(self):
  """The example's canonical form, from the congruence routine, not by hand."""
  cells = [[FMT(FOUND[i]) if i == j else "0" for j in range(NDIM)] for i in range(NDIM)]
  grid, pos = self._numgrid(-3.60, 0.30, cells, dx=0.66, dy=0.50, size=FS_TAG - 2,
                            hot={(i, i) for i in range(NDIM)}, hotcolor=WARN)
  g = VGroup(grid)
  # the three blocks marked under the grid, not over it: a rule drawn across
  # the diagonal would sit on the entries it is naming
  ybar = pos(NDIM - 1, NDIM - 1)[1] - 0.42
  spans = ((ACCENT_C, 0, P), (WARN, P, P + NNEG), (DIM, P + NNEG, NDIM))
  for col, a, b in spans:
   if b > a:
    g.add(Line([pos(a, a)[0] - 0.26, ybar, 0],
               [pos(b - 1, b - 1)[0] + 0.26, ybar, 0], color=col, stroke_width=2.5))
  terms = " + ".join(f"x {SUB[i]}²" for i in range(P))
  if NNEG:
   terms += " − " + " − ".join(f"x {SUB[P + i]}²" for i in range(NNEG))
  g.add(self._sym(0.95, "q ( ξ )   =   " + terms, WARN, FS_TAG + 1, x=2.60, w=5.80),
        self._mid(0.25, f"正的 {P} 個、負的 {NNEG} 個、零的 {NZERO} 個",
                  f"{P} positive, {NNEG} negative, {NZERO} zero",
                  ACCENT_A, FS_TAG, x=2.60, w=5.80),
        self._mid(-0.45, "交叉項全部消失了", "every cross term is gone", ACCENT_C,
                  FS_TAG, x=2.60, w=5.80))
  return g.add(self._mid(-1.20, "這個對角線是程式從左邊那個矩陣重新算出來的，不是抄答案",
                         "that diagonal was recomputed from the matrix, not copied from the answer",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "定理 7.2：在正交規範基底上，二次型只剩帶正負號的平方項",
                         "theorem 7.2: on an orthonormal basis a quadratic form is signed squares only",
                         ACCENT_B, FS_TAG, w=11.9))

 def _independence(self):
  """Why p and n cannot depend on which orthonormal basis you found."""
  g = VGroup()
  blocks = ((-4.00, "V ₁", f"d = {P}", ACCENT_C, "q > 0"),
            (-1.30, "V ₋₁", f"d = {NNEG}", WARN, "q < 0"),
            (1.40, "V ₀", f"d = {NZERO}", DIM, "q = 0"))
  for cx, name, dim, col, cond in blocks:
   g.add(self._box(cx, 0.95, name, col, w=2.10, h=0.58),
         Text(dim, font_size=FS_TAG - 2, color=col).move_to([cx, 0.38, 0]),
         Text(cond, font_size=FS_TAG - 3, color=col).move_to([cx, -0.06, 0]))
  for x in (-2.65, 0.05):
   g.add(Text("⊕", font_size=FS_TAG, color=DIM).move_to([x, 0.95, 0]))
  g.add(self._box(4.30, 0.95, "V", ACCENT_B, w=1.60, h=0.58),
        Text("=", font_size=FS_TAG, color=DIM).move_to([3.05, 0.95, 0]))
  g.add(self._sym(-0.66, "ξ  ∈  V ₁ ∩ ( V ₋₁ ⊕ V ₀ )   ⇒   q ( ξ ) > 0   ∧   q ( ξ ) ≤ 0",
                  ACCENT_A, FS_TAG, x=0.00, w=9.40))
  return g.add(self._mid(-1.20, "所以交集裡只有零向量，兩邊互為補空間，維數只好相等",
                         "so the intersection is only zero, each is a complement of the other, and the dimensions must agree",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "換一組正交規範基底，三塊子空間會換，但三個維數不會",
                         "another orthonormal basis gives different subspaces but the same three dimensions",
                         ACCENT_A, FS_TAG, w=11.9))

 def _signature(self):
  g = VGroup(self._box(-3.60, 0.95, f"σ   =   p − n   =   {P - NNEG}", ACCENT_C,
                       w=4.60, h=0.62, size=FS_TAG),
             self._box(-3.60, 0.15, f"r   =   p + n   =   {P + NNEG}", WARN,
                       w=4.60, h=0.62, size=FS_TAG))
  cells = [[FMT(v) for v in r] for r in T]
  grid, _ = self._numgrid(2.60, 0.40, cells, dx=0.52, dy=0.44, size=FS_TAG - 3,
                          color=ACCENT_B)
  g.add(grid, Text(f"r ( t )  =  {_rank(T)}", font_size=FS_TAG - 1, color=WARN)
        .move_to([2.60, -0.60, 0]))
  return g.add(self._mid(-0.68, "秩就是任何一個表示矩陣的秩，跟基底無關",
                         "the rank is the rank of any matrix representing the form, whichever basis",
                         ACCENT_A, FS_TAG, x=-3.60, w=5.00),
               self._mid(-1.20, "正定與負定是 σ 頂到天花板的那兩種特例，下一集會用到",
                         "positive and negative definite are the two extremes of sigma, and next time uses them",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集：怎麼真的把一個矩陣算成這個形狀，只用加減乘除",
                         "next time: how to compute a matrix into this shape, using only arithmetic",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  tp, mo, ds = self._two_problems(), self._matrix_of_omega(), self._double_sum()
  po, tg, sc = self._polarization(), self._target(), self._scale()
  ns, ind = self._null_space(), self._induction()
  cn, ip, sg = self._canonical(), self._independence(), self._signature()
  return [([tp], []), ([mo], [tp]), ([ds], [mo]), ([po], [ds]),
          ([tg], [po]), ([sc], [tg]), ([ns], [sc]), ([ind], [ns]),
          ([cn], [ind]), ([ip], [cn]), ([sg], [ip])]


AdvCalcE29ZH, AdvCalcE29EN = make(AdvCalcE29Base, "29", prefix="AdvCalcE")
