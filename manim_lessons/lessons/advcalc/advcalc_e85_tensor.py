"""advcalc E85 -- chapter 7, sections 1 and 2 (book pp. 305-308): bilinear
functionals, the tensor product of dual spaces, and covariant tensors.

Chapter 7 opens by saying it is principally for reference and that the reader
is not expected to study its proofs; its goal is the machinery of alternating
multilinear functionals, with the determinant as one of the rewards.  Sections
1 and 2 are the same statement told twice, once for two slots and once for n of
them -- the space of bilinear functionals, its three natural descriptions, the
elementary tensors, and the basis of dimension m to the n -- so they are one
episode rather than two.  The chapter has no exercises anywhere, which beat 0
says once and nothing afterwards pretends otherwise.

The whole episode runs on one worked example: V is three-dimensional, W is
two-dimensional, and f is the bilinear functional with the integer matrix T.
Everything on screen is then arithmetic on that matrix, and the two routes to
every number are computed separately so that agreeing means something.  A
bilinear functional is carried as a Python function of two coordinate vectors,
never as its matrix; `gram` recovers the matrix by evaluating the function on
the basis pairs, exactly as the book's t_ij = f(alpha_i, beta_j) does.  So the
linearity of f -> (alpha -> f_alpha) in beat 2 is checked by building the sum
and the scalar multiple as functions and taking the matrix of each afterwards,
and the expansion in beat 4 is checked by evaluating the mn elementary tensors
against the functional over a 243-point grid of integer pairs rather than at
one lucky point.  The counts in beats 6, 8 and 9 come from itertools.product,
not from a power -- the point of those beats is that the formula m to the n is
a count of tuples, and a count that is computed by the formula would prove
nothing.

Two layout facts worth recording.  Beat 1 draws two straight lines, which is
exactly the configuration that has silently drawn one line twice in this
series, so the two slopes f(xi', eta) and f(xi, eta') are asserted distinct at
module level; the first vectors tried gave them both the value one.  And the
second tuple index is written r, not the book's q: Unicode has a subscript r
and no subscript q, and the alternative was a literal underscore in every row
of beats 7 to 9.
"""
import itertools
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these

# ── the one worked example: dim V = m = 3, dim W = 2 ──────────────────
M, NDUAL = 3, 2
MN = M * NDUAL
T = np.array([[2.0, -1.0], [0.0, 3.0], [1.0, 2.0]])
S2 = np.array([[1.0, 0.0], [-2.0, 1.0], [0.0, 4.0]])
EV, EW = np.eye(M), np.eye(NDUAL)


def bil(Tm):
 """The bilinear functional with matrix Tm, as a function of coordinates."""
 return lambda x, y: float(np.asarray(x) @ Tm @ np.asarray(y))


def gram(h):
 """Recover t_ij = h(alpha_i, beta_j) by evaluating h on the basis pairs."""
 return np.array([[h(EV[i], EW[j]) for j in range(NDUAL)] for i in range(M)])


def gram_rev(h):
 """The same table read the other way round, for the Hom(V, W*) picture."""
 return np.array([[h(EV[i], EW[j]) for i in range(M)] for j in range(NDUAL)])


F = bil(T)
G = bil(S2)
assert np.abs(gram(F) - T).max() == 0.0, \
    "evaluating f on the basis pairs returns the matrix it was built from"

# the grid every pointwise claim is tested on, not one lucky point
GRIDPTS = [(np.array([a, b, c], float), np.array([d, e], float))
           for a, b, c in itertools.product((-1.0, 0.0, 2.0), repeat=3)
           for d, e in itertools.product((-1.0, 1.0, 3.0), repeat=2)]

# ── beat 1: linear in each slot, not in both ──────────────────────────
XI, XIP = np.array([1.0, 0.0, 1.0]), np.array([1.0, 1.0, 0.0])
ETA, ETAP = np.array([1.0, 0.0]), np.array([0.0, 1.0])
C0 = F(XI, ETA)
SLA, SLB = F(XIP, ETA), F(XI, ETAP)
CQ = F(XIP, ETAP)
SS = np.linspace(-1.0, 1.0, 201)
assert max(abs(F(XI + s * XIP, ETA) - (C0 + SLA * s)) for s in SS) < 1e-12, \
    "fixing the second slot leaves a straight line in the parameter"
assert max(abs(F(XI, ETA + s * ETAP) - (C0 + SLB * s)) for s in SS) < 1e-12, \
    "and so does fixing the first one"
assert SLA != SLB, \
    "the two lines have different slopes, so they are two lines and not one drawn twice"
assert max(abs(F(XI + s * XIP, ETA + s * ETAP)
               - (C0 + (SLA + SLB) * s + CQ * s * s)) for s in SS) < 1e-12, \
    "moving both slots at once is quadratic, with the cross value as leading coefficient"
assert CQ != 0.0, "that quadratic really bends: bilinear is not linear jointly"
CURV = [lambda s: C0 + SLA * s, lambda s: C0 + SLB * s,
        lambda s: F(XI + s * XIP, ETA + s * ETAP)]
V1LO = min(min(f(s) for s in SS) for f in CURV)
V1HI = max(max(f(s) for s in SS) for f in CURV)
SY1 = 1.00 / (V1HI - V1LO)
OY1 = -0.15 - SY1 * (V1LO + V1HI) / 2.0
assert SY1 * (min(f(1.0) for f in CURV) - min(f(-1.0) for f in CURV)) != 0.0

# ── beat 2: f -> (alpha -> f_alpha) is linear, and invertible ─────────
CSC = -1.5
LIN_ADD = float(np.abs(gram(lambda x, y: F(x, y) + G(x, y)) - (gram(F) + gram(G))).max())
LIN_SC = float(np.abs(gram(lambda x, y: CSC * F(x, y)) - CSC * gram(F)).max())
REVR = float(np.abs(gram_rev(F) - gram(F).T).max())
INVR = max(abs(sum(gram(F)[i, j] * x[i] * y[j] for i in range(M) for j in range(NDUAL))
               - F(x, y)) for x, y in GRIDPTS)
assert LIN_ADD == 0.0 and LIN_SC == 0.0, \
    "the correspondence respects sums and scalars, which is all Theorem 1.1 adds"
assert REVR == 0.0, "reversing the roles of the variables transposes the table"
assert INVR == 0.0, "and rebuilding f from its table gives f back, so the map is a bijection"

# ── beat 3: elementary iff dyad ───────────────────────────────────────
GAM = np.array([1.0, -2.0, 3.0])
LAM = np.array([2.0, 1.0])
DYAD = np.outer(GAM, LAM)
assert np.abs(gram(lambda x, y: float(GAM @ x) * float(LAM @ y)) - DYAD).max() == 0.0, \
    "the elementary tensor's table is the outer product of the two functionals"
RK1, RK2 = int(np.linalg.matrix_rank(DYAD)), int(np.linalg.matrix_rank(T))
SV1 = float(np.linalg.svd(DYAD, compute_uv=False)[1])
SV2 = float(np.linalg.svd(T, compute_uv=False)[1])
assert RK1 == 1 and SV1 < 1e-12, "an elementary functional corresponds to a rank one map"
assert RK2 == 2 and SV2 > 1.0, "and the worked example is not elementary: its rank is two"

# ── beat 4: Theorem 1.2, the mn elementary functionals are a basis ────
EXPAND = max(abs(F(x, y) - sum(T[i, j] * x[i] * y[j]
                               for i in range(M) for j in range(NDUAL)))
             for x, y in GRIDPTS)
assert EXPAND == 0.0, \
    "f agrees with the sum of its mn elementary pieces at every one of the test pairs"
_rng = np.random.default_rng(0)
BPAIRS = []
while len(BPAIRS) < MN:
 _x = _rng.integers(-2, 3, M).astype(float)
 _y = _rng.integers(-2, 3, NDUAL).astype(float)
 if np.abs(_x).sum() > 0 and np.abs(_y).sum() > 0:
  BPAIRS.append((_x, _y))
EVAL6 = np.array([[x[i] * y[j] for i in range(M) for j in range(NDUAL)] for x, y in BPAIRS])
DET6 = float(np.linalg.det(EVAL6))
assert abs(DET6) > 1.0, \
    "the mn elementary functionals are independent, so with mn of them they are a basis"

# ── beats 5: trilinear, one slot at a time ────────────────────────────
LV = (np.array([1.0, -1.0, 2.0]), np.array([2.0, 1.0, 0.0]), np.array([-1.0, 0.0, 1.0]))
UV = (np.array([1.0, 1.0, -1.0]), np.array([0.0, 2.0, 1.0]), np.array([2.0, -1.0, 1.0]))
WV = np.array([1.0, 0.0, 2.0])


def tri(a, b, c):
 return float((LV[0] @ a) * (LV[1] @ b) * (LV[2] @ c))


SLOPE3, SEC3 = [], 0.0
for _k in range(3):
 _arg = list(UV)
 _f0 = tri(*_arg)
 _vals = []
 for _s in (1.0, 2.0, 3.0):
  _arg[_k] = UV[_k] + _s * WV
  _vals.append(tri(*_arg))
 SLOPE3.append(_vals[0] - _f0)
 SEC3 = max(SEC3, max(abs(_vals[_j] - _f0 - (_j + 1) * (_vals[0] - _f0)) for _j in range(3)))
assert SEC3 == 0.0, "an elementary trilinear functional is linear in each slot on its own"
assert len(set(SLOPE3)) == 3, \
    "and the three slopes differ, so the three slots are genuinely three different maps"

# ── beats 6 to 9: the tuple set m-bar-to-the-n ────────────────────────
TUPS = {n: list(itertools.product(range(1, M + 1), repeat=n)) for n in (1, 2, 3)}
CNT = {n: len(TUPS[n]) for n in (1, 2, 3)}
assert all(CNT[n] == M ** n for n in (1, 2, 3)), \
    "counting the tuples one by one gives the same answer as the power m to the n"

C33 = np.array([[2.0, -1.0, 0.0], [3.0, 1.0, -2.0], [0.0, 4.0, 1.0]])
Z1, Z2 = np.array([1.0, -2.0, 3.0]), np.array([2.0, 1.0, -1.0])
V6 = float(Z1 @ C33 @ Z2)
V6S = sum(Z1[p - 1] * Z2[q - 1] * C33[p - 1, q - 1] for p, q in TUPS[2])
D6 = abs(V6 - V6S)
assert D6 == 0.0, \
    "the expansion over all n-tuples reproduces the value of the bilinear functional"


def muval(r, p):
 """mu_r evaluated at the basis vectors indexed by p: one when r = p, else zero."""
 return float(np.prod([1.0 if r[i] == p[i] else 0.0 for i in range(len(r))]))


KRON = np.array([[muval(r, p) for p in TUPS[2]] for r in TUPS[2]])
OFFV = float(max(abs(KRON[a, b]) for a in range(CNT[2]) for b in range(CNT[2]) if a != b))
ONV = float(min(KRON[a, a] for a in range(CNT[2])))
DETK = float(np.linalg.det(KRON))
assert OFFV == 0.0, "mu_r vanishes on every tuple of basis vectors except its own"
assert ONV == 1.0, "and takes the value one on that one"
assert abs(DETK - 1.0) < 1e-12, \
    "so the table is the identity and the elementary functionals are independent"
COEF = [float(sum(KRON[a, b] * C33[TUPS[2][b][0] - 1, TUPS[2][b][1] - 1]
                  for b in range(CNT[2]))) for a in range(CNT[2])]
assert all(abs(COEF[a] - C33[TUPS[2][a][0] - 1, TUPS[2][a][1] - 1]) == 0.0
           for a in range(CNT[2])), \
    "which is why the coordinate c_r is just the value of f on the rth tuple"

_rng2 = np.random.default_rng(11)
A27 = {t: float(_rng2.integers(-5, 6)) for t in TUPS[3]}
DBL = sum(sum(A27[p + (j,)] for j in range(1, M + 1)) for p in TUPS[2])
SGL = sum(A27[r] for r in TUPS[3])
assert abs(DBL - SGL) == 0.0, \
    "the double sum over a tuple and one more index is the single sum one length up"
assert sorted(p + (j,) for p in TUPS[2] for j in range(1, M + 1)) == sorted(TUPS[3]), \
    "because that pairing is a bijection, which is the whole content of the inductive step"

# ── beat 10: order two splits into symmetric and skew ─────────────────
SYM = (C33 + C33.T) / 2.0
SKW = (C33 - C33.T) / 2.0
RSYM = float(np.abs(SYM.T - SYM).max())
RSKW = float(np.abs(SKW.T + SKW).max())
RSPL = float(np.abs(SYM + SKW - C33).max())
DSYM, DSKW = M * (M + 1) // 2, M * (M - 1) // 2
assert RSPL == 0.0 and RSYM == 0.0 and RSKW == 0.0, \
    "every order two tensor is a symmetric part plus a skew part, uniquely"
assert DSYM + DSKW == M ** 2, \
    "and the two dimensions add up to m squared, which is the dimension of the whole space"


class AdvCalcE85Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 85

 MODE_LABEL = {
  0: {"zh": "第 7 章：備查章節，整章沒有習題",
      "en": "chapter 7: a reference chapter, and no exercises in it"},
  1: {"zh": "雙線性泛函自成一個向量空間",
      "en": "the bilinear functionals form a vector space"},
  2: {"zh": "定理 1.1：三個空間自然同構",
      "en": "theorem 1.1: three spaces, naturally isomorphic"},
  3: {"zh": "初等張量：秩一", "en": "elementary tensors: rank one"},
  4: {"zh": "定理 1.2：維數是 m 乘 n", "en": "theorem 1.2: the dimension is m times n"},
  5: {"zh": "推廣到 n 重線性", "en": "on to n slots"},
  6: {"zh": "都取同一個 V：n 階共變張量",
      "en": "all slots the same V: covariant tensors of order n"},
  7: {"zh": "初等多重線性泛函", "en": "the elementary multilinear functionals"},
  8: {"zh": "定理 2.1 與推論：維數是 m 的 n 次方",
      "en": "theorem 2.1 and its corollary: the dimension is m to the n"},
  9: {"zh": "歸納那一步：雙重和寫成單一和",
      "en": "the inductive step: a double sum as a single one"},
  10: {"zh": "收尾：對稱與交錯，下一集從置換開始",
       "en": "closing: symmetry and alternation, and permutations next"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.90, dy=0.30, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _cap(self, zh, en):
  return self._mid(-0.90, zh, en, ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W)

 def _legend(self, x, rows, y0=1.14, dy=0.27):
  g = VGroup()
  for k, (col, lab, w) in enumerate(rows):
   y = y0 - k * dy
   g.add(Line([x, y, 0], [x + 0.24, y, 0], color=col, stroke_width=6.0),
         self._sym(y, lab, col, FS_TAG - 3, x=x + 0.46 + w / 2, w=w))
  return g

 def _plot(self, f, col, ta, tb, oy, sy, sw=2.6, n=170, xl=XL, xr=XR):
  """A curve over the parameter in [ta, tb], pinned to the figure's edges.

  Same helper as E79 and E80: the range is a parameter, so nothing has to be
  assumed about where the parameter's zero lands on screen."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 # ── beat 0: the map of the chapter ──────────────────────────────
 def _chapter(self):
  g = VGroup()
  xs = (-5.30, -4.20, -3.10)
  ys = (0.72, 0.08, -0.56)
  for k in range(9):
   col = ACCENT_A if k < 2 else DIM
   g.add(self._box(xs[k % 3], ys[k // 3], f"§ {k + 1}", col,
                   w=0.86, h=0.44, size=FS_TAG - 1))
  g.add(Line([-5.73, 0.42, 0], [-3.77, 0.42, 0], color=ACCENT_A, stroke_width=4.0))
  g.add(self._table((("§ 1          V * ⊗ W *", ACCENT_A),
                     ("§ 2          ( V * ) ⊗ ⁿ", ACCENT_A),
                     ("§ 3  ,  § 4          S ₙ   ,   ±  1", DIM),
                     ("§ 5          𝒜 ⁿ   ⊂   ( V * ) ⊗ ⁿ", DIM),
                     ("§ 6          det", DIM),
                     ("§ 7  ,  § 8          ∧", DIM),
                     ("§ 9          ∗", DIM),
                     (f"dim ( V * ) ⊗ ⁿ   =   m ⁿ            {M} ³   =   {M ** 3}",
                      ACCENT_B)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("右表每一列是那一節最後做出來的東西",
                  "each row names what that section ends up building"))
  return g.add(self._foot("第 7 章一開頭就說自己主要是備查用的，證明大多寫了出來，但不期待讀者細讀。目標是交錯多重線性泛函那一整套工具",
                          "chapter 7 says at the outset that it is principally for reference: most proofs are included but the reader is not expected to study them, and the goal is the machinery of alternating multilinear functionals",
                          ACCENT_A,
                          "左圖九個方塊是這一章的九節，橘色那兩節是這一集。行列式是第 6 節的收穫。整章從頭到尾一題習題也沒有，所以這一集不會示範任何習題",
                          "the nine boxes are the nine sections and the orange pair is this episode; the determinant is section 6's reward, and since the chapter sets no exercises at all none is worked here"))

 # ── beat 1: linear in each slot, not in both ────────────────────
 def _slots(self):
  ta, tb = -1.0, 1.0
  g = VGroup(self._arr([XL - 0.14, -0.72, 0], [XR + 0.30, -0.72, 0], DIM, sw=3, tl=0.14))
  for col, f in zip((ACCENT_A, ACCENT_B, ACCENT_C), CURV):
   g.add(self._plot(f, col, ta, tb, OY1, SY1, sw=2.8))
  for s, lab in ((-1.0, "−  1"), (0.0, "0"), (1.0, "+  1")):
   x = self._xof(s, ta, tb)
   g.add(Line([x, -0.76, 0], [x, -0.68, 0], color=DIM, stroke_width=1.6))
   g.add(self._sym(-0.90, lab, DIM, FS_TAG - 4, x=x, w=0.44))
  g.add(self._sym(-0.56, "s", DIM, FS_TAG - 3, x=XR + 0.30, w=0.30))
  x0 = self._xof(0.0, ta, tb)
  g.add(self._dash([x0, -0.68, 0], [x0, 0.40, 0], DIM, n=9, sw=1.6))
  g.add(Dot([x0, OY1 + SY1 * C0, 0], radius=0.075, color=INK))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "f ( ξ + s ξ ′ , η )", 2.10),
                                 (ACCENT_B, "f ( ξ , η + s η ′ )", 2.10),
                                 (ACCENT_C, "f ( ξ + s ξ ′ , η + s η ′ )", 2.90)),
                     y0=1.14, dy=0.26))
  g.add(self._table((("f ( ξ + s ξ ′ , η )   =   f ( ξ , η )  +  s  f ( ξ ′ , η )", ACCENT_A),
                     ("f ( ξ , η + s η ′ )   =   f ( ξ , η )  +  s  f ( ξ , η ′ )", ACCENT_B),
                     ("f ( ξ + s ξ ′ , η + s η ′ )   =   c ₀  +  c ₁ s  +  c ₂ s ²",
                      ACCENT_C),
                     (f"f ( ξ ′ , η )   =   {SLA:+.0f}            f ( ξ , η ′ )   =   {SLB:+.0f}",
                      ACCENT_A),
                     (f"c ₀   =   {C0:+.0f}        c ₁   =   {SLA + SLB:+.0f}"
                      f"        c ₂   =   {CQ:+.0f}", DIM),
                     ("V * ⊗ W *   =   { f }            dim   =   m n", ACCENT_A),
                     (f"m   =   {M}        n   =   {NDUAL}        m n   =   {MN}", ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("三條線在 s 等於零那裡交會，值都是 f 本身",
                  "the three meet where s is zero, and all three equal f itself there"))
  return g.add(self._foot("先看雙線性的情形。V 與 W 有限維時，兩者乘積上的雙線性泛函全體很顯然是個向量空間，書上記作 V 星與 W 星的張量積",
                          "start with the bilinear case: for finite dimensional V and W the bilinear functionals on their product pretty clearly form a vector space, written as the tensor product of the two dual spaces",
                          ACCENT_A,
                          "橘線與青線是固定一個變數時的樣子，兩條都是直線，而且斜率不同；紫線是兩個變數一起動，它是拋物線。雙線性不等於對整體線性",
                          "the orange and the cyan curve each fix one slot and are straight lines of different slopes, while the purple one moves both and is a parabola: bilinear is not jointly linear"))

 # ── beat 2: Theorem 1.1 ─────────────────────────────────────────
 def _iso(self):
  g = VGroup(self._sym(0.88, "V * ⊗ W *", ACCENT_A, FS_TAG, x=-4.20, w=1.80),
             self._sym(-0.52, "Hom ( V , W * )", ACCENT_B, FS_TAG - 2, x=-5.20, w=1.95),
             self._sym(-0.52, "Hom ( W , V * )", ACCENT_C, FS_TAG - 2, x=-3.15, w=1.95))
  g.add(self._arr([-4.72, 0.66, 0], [-5.02, -0.30, 0], ACCENT_A, sw=3, tl=0.13),
        self._arr([-3.68, 0.66, 0], [-3.38, -0.30, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(0.18, "≅", ACCENT_A, FS_TAG, x=-4.46, w=0.30),
        self._sym(0.18, "≅", ACCENT_A, FS_TAG, x=-3.94, w=0.30))
  g.add(self._dash([-5.20, -0.68, 0], [-5.20, -0.92, 0], DIM, n=4, sw=1.6),
        self._dash([-3.15, -0.68, 0], [-3.15, -0.92, 0], DIM, n=4, sw=1.6))
  g.add(self._arr([-4.52, -0.92, 0], [-5.14, -0.92, 0], ACCENT_A, sw=3, tl=0.13),
        self._arr([-3.82, -0.92, 0], [-3.21, -0.92, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(-0.92, "≅", ACCENT_A, FS_TAG, x=-4.17, w=0.30))
  g.add(self._table((("V * ⊗ W *   ≅   Hom ( V , W * )   ≅   Hom ( W , V * )", ACCENT_A),
                     ("Φ f   =   ( α   ↦   f ( ·  ,  α ) )            Ch 1  ,  6.1",
                      ACCENT_C),
                     (f"Φ ( f + g )  −  Φ f  −  Φ g              {LIN_ADD:.1e}", ACCENT_B),
                     (f"Φ ( c f )  −  c  Φ f        c  =  {CSC:+.1f}        {LIN_SC:.1e}",
                      ACCENT_B),
                     ("Φ ⁻ ¹ ( t ᵢ ⱼ )   =   Σ   t ᵢ ⱼ  ( μ ᵢ ⊗ ν ⱼ )", ACCENT_A),
                     (f"Φ ⁻ ¹ Φ f   −   f              {INVR:.1e}", ACCENT_B),
                     (f"Ψ f   −   ( Φ f ) ᵗ              {REVR:.1e}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("三個殘差都是零：那個對應真的是線性的雙射",
                  "all three residuals vanish: the correspondence really is a linear bijection"))
  return g.add(self._foot("定理 1.1 說這三個空間自然同構。每個雙線性泛函都決定一個對應，而那個對應把第二個變數送到一個線性泛函上",
                          "Theorem 1.1 makes the three spaces naturally isomorphic: each bilinear functional determines a correspondence sending the second variable to a linear functional",
                          ACCENT_A,
                          "第 1 章定理 6.1 已經做掉一半，說那個對應是雙射；這一章補的只是它本身也是線性的。角色對調就得到另一個同構，右表最後一列是轉置",
                          "chapter 1's Theorem 6.1 did half of it by making the correspondence bijective, and all that is added here is that it is itself linear; reversing the roles transposes the table, which is the last row"))

 # ── beat 3: elementary iff rank one ─────────────────────────────
 def _elem(self):
  g = VGroup()
  for cx, Mx, lab, col, rk in ((-5.10, DYAD, "γ ⊗ λ", ACCENT_B, RK1),
                               (-3.35, T, "f", ACCENT_C, RK2)):
   grid, _pos = self._numgrid(cx, 0.26, [[f"{int(v):+d}" for v in row] for row in Mx],
                              dx=0.52, dy=0.42, size=FS_TAG - 4, color=col)
   g.add(grid)
   g.add(self._sym(1.12, lab, col, FS_TAG, x=cx, w=1.00))
   g.add(self._sym(-0.62, f"rank   =   {rk}", col, FS_TAG - 3, x=cx, w=1.30))
  g.add(self._table((("( γ ⊗ λ ) ( ξ , η )   =   γ ( ξ )  ·  λ ( η )", ACCENT_A),
                     (f"γ ( α ᵢ )   :   {' , '.join(f'{int(v):+d}' for v in GAM)}"
                      f"            λ ( β ⱼ )   :   "
                      f"{' , '.join(f'{int(v):+d}' for v in LAM)}", ACCENT_C),
                     ("t ᵢ ⱼ   =   γ ᵢ  λ ⱼ            ⇔            rank   =   1",
                      ACCENT_A),
                     (f"rank ( γ ⊗ λ )   =   {RK1}            σ ₂   =   {SV1:.1e}",
                      ACCENT_B),
                     (f"rank ( f )   =   {RK2}            σ ₂   =   {SV2:.3f}", ACCENT_C),
                     ("Hom ( V , W * )            Ch 2  ,  § 4", DIM)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("左邊那個的第二個奇異值是零，右邊那個不是",
                  "the left one's second singular value is zero and the right one's is not"))
  return g.add(self._foot("γ 張量 λ 在一對向量上的值，就是 γ 作用在第一個上面乘以 λ 作用在第二個上面。書上把長這個樣子的雙線性泛函叫做初等的",
                          "the value of gamma tensor lambda on a pair of vectors is gamma on the first times lambda on the second, and the book calls any bilinear functional of that shape elementary",
                          ACCENT_A,
                          "一個雙線性泛函是初等的，若且唯若它對應的線性映射的秩是一。左邊那個矩陣的每一列都是同一列的倍數，右邊那個不是，兩者的秩真的算出來了",
                          "a bilinear functional is elementary exactly when the corresponding linear map has rank one: every row of the left table is a multiple of one row and the right one is not, and both ranks are actually computed"))

 # ── beat 4: Theorem 1.2, the coefficient table ──────────────────
 def _basis2(self):
  grid, pos = self._numgrid(-4.05, 0.10, [[f"{int(v):+d}" for v in row] for row in T],
                            dx=0.74, dy=0.50, size=FS_TAG - 3, color=ACCENT_A)
  g = VGroup(grid)
  for i in range(M):
   g.add(self._sym(pos(i, 0)[1], f"μ {'₁₂₃'[i]}", ACCENT_B, FS_TAG - 3, x=-5.15, w=0.60))
  for j in range(NDUAL):
   g.add(self._sym(0.98, f"ν {'₁₂'[j]}", ACCENT_C, FS_TAG - 3, x=pos(0, j)[0], w=0.60))
  g.add(self._sym(-0.84, "t ᵢ ⱼ   =   f ( α ᵢ , β ⱼ )", ACCENT_A, FS_TAG - 3,
                  x=-4.05, w=2.60))
  g.add(self._table((("f   =   Σ ᵢ ⱼ   t ᵢ ⱼ   ( μ ᵢ ⊗ ν ⱼ )", ACCENT_A),
                     ("( μ ᵢ ⊗ ν ⱼ ) ( ξ , η )   =   x ᵢ  y ⱼ", ACCENT_C),
                     (f"m   =   {M}            n   =   {NDUAL}            m n   =   {MN}",
                      ACCENT_B),
                     (f"max | Δ |   =   {EXPAND:.1e}", ACCENT_B),
                     (f"det   =   {DET6:+.0f}            ⇒            dim   =   {MN}",
                      ACCENT_A),
                     ("Ch 2  ,  § 4", DIM)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("左圖橫列的指標是 μ，直行的指標是 ν",
                  "the figure's rows are indexed by mu and its columns by nu"))
  return g.add(self._foot("定理 1.2：取 V 與 W 的基底和它們的對偶基底，那 m 乘 n 個初等泛函就構成張量積的一組基底，所以維數是 m 乘 n",
                          "Theorem 1.2: take bases of V and W and their dual bases, and the m times n elementary functionals form a basis of the tensor product, so its dimension is m times n",
                          ACCENT_A,
                          "左圖每一格就是 f 在那一對基底向量上的值。那個最大差是把展開式與 f 在兩百多對整數向量上逐點比出來的，而那個行列式說六個基底元素彼此獨立",
                          "each cell is f's value on that pair of basis vectors; the largest difference compares the expansion with f at over two hundred integer pairs, and the determinant says the six are independent"))

 # ── beat 5: n slots ─────────────────────────────────────────────
 def _multi(self):
  g = VGroup()
  xs = (-5.55, -4.55, -3.55, -2.60)
  labs = ("V ₁", "V ₂", "⋯", "V ₙ")
  for x, lab, k in zip(xs, labs, range(4)):
   g.add(self._box(x, 0.62, lab, ACCENT_A if k == 1 else DIM,
                   w=0.72, h=0.46, size=FS_TAG - 1))
  for a, b in zip(xs, xs[1:]):
   g.add(self._sym(0.62, "×", DIM, FS_TAG - 3, x=(a + b) / 2, w=0.22))
  g.add(self._sym(0.22, "α ⱼ", ACCENT_A, FS_TAG - 2, x=-4.55, w=0.46))
  for x in (-5.55, -2.60):
   g.add(self._sym(0.22, "α ᵢ", DIM, FS_TAG - 2, x=x, w=0.46))
  g.add(self._box(-4.05, -0.52, "ℝ", ACCENT_B, w=0.72, h=0.46, size=FS_TAG + 1))
  g.add(self._arr([-4.55, 0.06, 0], [-4.28, -0.28, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(-0.14, "f", ACCENT_A, FS_TAG, x=-4.86, w=0.34))
  g.add(self._table((("f   :   V ₁  ×  ⋯  ×  V ₙ   →   ℝ", ACCENT_A),
                     ("α ⱼ   ↦   f ( α ₁ , … , α ₙ )            i   ≠   j", ACCENT_C),
                     ("( λ ₁ ⊗ ⋯ ⊗ λ ₙ ) ( ξ )   =   λ ₁ ( ξ ₁ ) ⋯ λ ₙ ( ξ ₙ )",
                      ACCENT_B),
                     (f"Δ ⱼ   =   {SLOPE3[0]:+.0f}  ,  {SLOPE3[1]:+.0f}  ,  "
                      f"{SLOPE3[2]:+.0f}", ACCENT_C),
                     (f"| Δ ² |   =   {SEC3:.1e}", ACCENT_B),
                     ("V ₁ *  ⊗  ⋯  ⊗  V ₙ *", ACCENT_A),
                     ("V ₁ * ⊗ ⋯ ⊗ V ₙ *   ≅   Hom ( V ₁ , V ₂ * ⊗ ⋯ ⊗ V ₙ * )", DIM)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("只有點亮的那一格在動，其餘都先凍結住",
                  "only the lit slot is moving and the rest are frozen"))
  return g.add(self._foot("以上整套都推廣到多重線性。f 從 n 個空間的乘積映到實數，要求是固定其他變數的時候，對每一個變數都線性",
                          "all of that generalises to multilinear functionals: f runs from a product of n spaces to the reals and is required to be linear in each variable when the others are held fixed",
                          ACCENT_A,
                          "全體一樣是個向量空間，記作那 n 個對偶空間的張量積。右表那三個增量是同一個初等三重線性泛函在三個位置上的斜率，三個都不一樣",
                          "they form a vector space again, written as the tensor product of the n dual spaces; the three increments are one elementary trilinear functional's slopes in its three slots, and all three differ"))

 # ── beat 6: all slots the same V ────────────────────────────────
 def _covariant(self):
  grid, _pos = self._numgrid(-4.20, 0.14,
                             [[f"⟨ {i} , {j} ⟩" for j in range(1, M + 1)]
                              for i in range(1, M + 1)],
                             dx=0.80, dy=0.46, size=FS_TAG - 4, color=ACCENT_B)
  g = VGroup(grid)
  g.add(self._sym(1.02, f"m̄ ²            m   =   {M}", ACCENT_A, FS_TAG - 2,
                  x=-4.20, w=2.20))
  g.add(self._sym(-0.78, f"| m̄ ² |   =   {CNT[2]}", ACCENT_B, FS_TAG - 2,
                  x=-4.20, w=1.80))
  g.add(self._table((("V ₁  =  ⋯  =  V ₙ  =  V            ( V * ) ⊗ ⁿ", ACCENT_A),
                     ("ξ ᵢ   =   Σ ⱼ   x ⁱ ⱼ   α ⱼ", ACCENT_C),
                     ("f ( ξ ₁ , … , ξ ₙ )   =   Σ ₚ   x ¹ ₚ ₁ ⋯ x ⁿ ₚ ₙ   "
                      "f ( α ₚ ₁ , … , α ₚ ₙ )", ACCENT_A),
                     ("p   ∈   m̄ ⁿ            1   ≤   p ᵢ   ≤   m", ACCENT_B),
                     (f"m   =   {M}        n   =   2        m ⁿ   =   {CNT[2]}",
                      ACCENT_C),
                     (f"f ( ξ ₁ , ξ ₂ )   =   {V6:+.0f}            Σ ₚ   =   {V6S:+.0f}",
                      ACCENT_A),
                     (f"| Δ |   =   {D6:.1e}", DIM)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("左圖那九格就是 n 等於二時所有的 p",
                  "those nine cells are every p there is when n is two"))
  return g.add(self._foot("為了讓記號簡單，也因為這才是最有用的情形，以下讓這 n 個空間全都是同一個 V。這時候記作 V 星的 n 次張量冪，叫做 n 階共變張量空間",
                          "to keep the notation simple, and because it is the case of most interest, let all n spaces be one and the same V: the space is then a tensor power of the dual, the covariant tensors of order n",
                          ACCENT_A,
                          "把每個變數照基底展開，再逐個變數用線性，就得到一個跑遍所有 n 元組的和式。右表那兩個值一個是直接算的、一個是把九項加起來的",
                          "expanding each variable and using linearity one slot at a time gives a sum over all tuples of length n; of the two values below, one is computed directly and the other by adding those nine terms"))

 # ── beat 7: the elementary multilinear functionals ──────────────
 def _mu(self):
  grid, _pos = self._numgrid(-4.20, 0.16, [[int(v) for v in row] for row in KRON],
                             dx=0.33, dy=0.21, size=FS_TAG - 6, color=DIM,
                             hot=tuple((a, a) for a in range(CNT[2])),
                             hotcolor=ACCENT_A)
  g = VGroup(grid)
  g.add(self._table((("μ ᵣ   =   μ ᵣ ₁  ⊗  ⋯  ⊗  μ ᵣ ₙ", ACCENT_A),
                     ("μ ᵣ ( α ₚ ₁ , … , α ₚ ₙ )   =   Π ᵢ   μ ᵣ ᵢ ( α ₚ ᵢ )", ACCENT_C),
                     ("=   0    ( p  ≠  r )            =   1    ( p  =  r )", ACCENT_B),
                     ("μ ᵣ ( ξ ₁ , … , ξ ₙ )   =   x ¹ ᵣ ₁ ⋯ x ⁿ ᵣ ₙ", ACCENT_A),
                     ("c ᵣ   =   f ( α ᵣ ₁ , … , α ᵣ ₙ )", ACCENT_A),
                     (f"p  ≠  r   :   {OFFV:.0e}            p  =  r   :   {ONV:.0f}",
                      ACCENT_B),
                     (f"det   =   {DETK:+.0f}            m ⁿ   =   {CNT[2]}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("橫的是 r、直的是 p，只有對角線上是一",
                  "rows are r and columns are p, and only the diagonal is one"))
  return g.add(self._foot("用對偶基底做出的初等多重線性泛函，在基底的 n 元組上只有兩個指標完全一樣時才是一，其他全是零。左圖那個九乘九的表就是單位矩陣",
                          "the elementary multilinear functionals built from the dual basis are worth one on a tuple of basis vectors only when the two index tuples agree, and zero otherwise, so that nine by nine table is the identity",
                          ACCENT_A,
                          "這正是為什麼係數可以一眼讀出來：把展開式代到第 r 組基底向量上，除了第 r 項以外每一項都被殺掉，剩下的就是 f 在那一組上的值",
                          "that is exactly why the coordinates can be read off: substituting the rth tuple of basis vectors into the expansion kills every term but the rth, leaving f's value on that tuple"))

 # ── beat 8: Theorem 2.1 and the corollary ───────────────────────
 def _dim(self):
  g = VGroup()
  levels = ((0.86, 1, 0.0, 0.055), (0.34, M, 1.08, 0.055),
            (-0.18, M ** 2, 0.36, 0.045), (-0.70, M ** 3, 0.12, 0.032))
  pts = []
  for y, cnt, step, r in levels:
   row = [-4.20 + (k - (cnt - 1) / 2.0) * step for k in range(cnt)]
   pts.append((y, row, r))
  for (ya, ra, _r0), (yb, rb, _r1) in zip(pts, pts[1:]):
   for k, xb in enumerate(rb):
    g.add(Line([ra[k * len(ra) // len(rb)] if False else ra[k // M], ya, 0],
               [xb, yb, 0], color=DIM, stroke_width=1.2))
  for y, row, r in pts:
   for x in row:
    g.add(Dot([x, y, 0], radius=r, color=ACCENT_B if y < 0.80 else DIM))
  for (y, _row, _r), n in zip(pts[1:], (1, 2, 3)):
   g.add(self._sym(y, str(M ** n), ACCENT_B, FS_TAG - 3, x=-2.25, w=0.32))
  g.add(self._table((("{ μ ₚ   :   p  ∈  m̄ ⁿ }            ( V * ) ⊗ ⁿ", ACCENT_A),
                     ("f   =   Σ ₚ   c ₚ  μ ₚ            c ₚ   =   f ( α ₚ ₁ , … , α ₚ ₙ )",
                      ACCENT_C),
                     ("        n            m ⁿ            | m̄ ⁿ |", DIM))
                    + tuple((f"        {n}            {M ** n}            {CNT[n]}",
                             ACCENT_B) for n in (1, 2, 3))
                    + ((f"dim ( V * ) ⊗ ⁿ   =   m ⁿ            m   =   {M}", ACCENT_A),
                       (f"det   =   {DETK:+.0f}", ACCENT_C)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("中間一欄是公式，右邊一欄是真的數出來的",
                  "the middle column is the formula and the right one an actual count"))
  return g.add(self._foot("定理 2.1：這些初等泛函構成 n 階共變張量空間的一組基底，而座標就是 f 在對應的那組基底向量上的值。推論是維數等於 m 的 n 次方",
                          "Theorem 2.1: those elementary functionals are a basis of the covariant tensors of order n, with coordinates the values of f on the matching tuples, and the corollary is that the dimension is m to the n",
                          ACCENT_A,
                          "左圖那棵樹每多一個位置就分三叉：m 等於三的時候三層剛好是三個、九個、二十七個。右表那兩欄一欄是幂、一欄是把元組一個一個數出來的",
                          "the tree branches three ways for each extra slot, so with m three the levels hold three, nine and twenty-seven; one column is the power and the other counts the tuples one by one"))

 # ── beat 9: the inductive step ──────────────────────────────────
 def _induct(self):
  g = VGroup()
  ly = [0.60, 0.00, -0.60]
  ry = [0.90 - k * 0.225 for k in range(CNT[2])]
  for k, y in enumerate(ly):
   g.add(self._sym(y, f"⟨ {k + 1} ⟩", ACCENT_A, FS_TAG - 3, x=-5.60, w=0.62))
  for k, y in enumerate(ry):
   p, j = TUPS[2][k]
   g.add(self._sym(y, f"⟨ {p} , {j} ⟩", ACCENT_B, FS_TAG - 5, x=-2.95, w=0.80))
   g.add(Line([-5.22, ly[p - 1], 0], [-3.42, y, 0], color=DIM, stroke_width=1.3))
  g.add(self._sym(1.14, "m̄ ¹   ×   m̄", ACCENT_A, FS_TAG - 3, x=-5.60, w=1.30))
  g.add(self._sym(1.14, "m̄ ²", ACCENT_B, FS_TAG - 3, x=-2.95, w=0.70))
  g.add(self._table((("m̄ ⁿ  ×  m̄            ↔            m̄ ⁿ ⁺ ¹", ACCENT_A),
                     ("⟨ p , j ⟩   ↦   r            r ᵢ  =  p ᵢ   ,   r ₙ ₊ ₁  =  j",
                      ACCENT_C),
                     ("Σ ₚ ∈ m̄ ⁿ   Σ ⱼ ∈ m̄            =            Σ ᵣ ∈ m̄ ⁿ ⁺ ¹",
                      ACCENT_A),
                     (f"{CNT[1]}  ×  {M}  =  {CNT[2]}            "
                      f"{CNT[2]}  ×  {M}  =  {CNT[3]}", ACCENT_B),
                     (f"Σ Σ   =   {DBL:+.0f}            Σ   =   {SGL:+.0f}", ACCENT_C),
                     (f"| Δ |   =   {abs(DBL - SGL):.1e}", ACCENT_B)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("左邊三個各長出三條，右邊剛好九個",
                  "each of the three on the left grows three, and the right holds nine"))
  return g.add(self._foot("為什麼要堆這麼多記號？因為嚴格的證明要對 n 做歸納，而歸納那一步得把一個雙重和寫成單一和",
                          "why pile up so much notation? a strict proof needs an induction on n, and the inductive step has to rewrite a double sum as a single one",
                          ACCENT_A,
                          "用到的事實是：一個 n 元組再配上一個指標，和一個 n 加一元組一一對應。左圖畫的是 n 等於一那一步，右表下面兩列是 n 等於二那一步真的加出來的",
                          "the fact it uses is that a tuple together with one more index is the same thing as a tuple one longer; the figure draws the step from one slot to two, and the last rows add up the step from two to three"))

 # ── beat 10: symmetry and alternation ───────────────────────────
 def _split(self):
  g = VGroup()
  for cx, Mx, lab, col, rel in ((-5.15, SYM, "S", ACCENT_B, "S ᵗ   =   S"),
                                (-3.35, SKW, "A", ACCENT_C, "A ᵗ   =   −  A")):
   grid, _pos = self._numgrid(cx, 0.24, [[f"{v:+.1f}" for v in row] for row in Mx],
                              dx=0.46, dy=0.36, size=FS_TAG - 5, color=col)
   g.add(grid)
   g.add(self._sym(1.08, lab, col, FS_TAG + 1, x=cx, w=0.40))
   g.add(self._sym(-0.56, rel, col, FS_TAG - 3, x=cx, w=1.40))
  g.add(self._sym(0.24, "+", ACCENT_A, FS_TAG, x=-4.25, w=0.24))
  g.add(self._sym(-0.88, f"{DSYM}   +   {DSKW}   =   {M ** 2}   =   m ²",
                  ACCENT_A, FS_TAG - 2, x=-4.25, w=2.40))
  g.add(self._table((("C   =   S   +   A", ACCENT_A),
                     ("S   =   ( C + C ᵗ ) / 2            A   =   ( C − C ᵗ ) / 2",
                      ACCENT_C),
                     (f"| S ᵗ − S |   =   {RSYM:.0e}            "
                      f"| A ᵗ + A |   =   {RSKW:.0e}", ACCENT_B),
                     (f"| S + A − C |   =   {RSPL:.0e}", ACCENT_B),
                     (f"𝒜 ⁿ   ⊂   ( V * ) ⊗ ⁿ            C ( {M} , 2 )   =   {DSKW}",
                      ACCENT_C),
                     ("S ₙ   ,   ±  1            § 3  ,  § 4", DIM)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("兩個矩陣相加就是原來那個係數矩陣",
                  "the two matrices add back up to the original coefficient matrix"))
  return g.add(self._foot("有了基底就可以談對稱與交錯了。二階的時候，任何一個係數矩陣都能唯一地拆成對稱的一半加上反對稱的一半，維數六加三剛好是九",
                          "with a basis in hand one can speak of symmetry and alternation: in order two every coefficient matrix splits uniquely into a symmetric half and a skew half, and six plus three is nine",
                          ACCENT_A,
                          "階數再高就不是這麼乾淨地分成兩塊了，第 5 節要處理的是交錯的那一塊。而交錯是用置換的正負號定義的，所以下一集得先從置換群講起",
                          "at higher orders it no longer splits that cleanly into two pieces, and section 5 goes after the alternating piece alone; alternating is defined by the sign of a permutation, so the next episode starts with those"))

 def stage(self):
  a, b, c = self._chapter(), self._slots(), self._iso()
  d, e, f_ = self._elem(), self._basis2(), self._multi()
  h, i, j = self._covariant(), self._mu(), self._dim()
  k, l = self._induct(), self._split()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE85ZH, AdvCalcE85EN = make(AdvCalcE85Base, "85", prefix="AdvCalcE")
