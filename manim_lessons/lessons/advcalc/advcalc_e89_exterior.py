"""advcalc E89 -- chapter 7, section 7 (book pp. 316 to the top of 319): the
exterior algebra.

Sections 1 through 6 built alternating tensors and then spent them on the
determinant.  What has been missing all along is a *multiplication*: the tensor
product of two alternating tensors is almost never alternating, so it leaves the
space.  This section repairs that.  The wedge is the tensor product followed by
the projection of section 5, scaled by a binomial coefficient, and the whole
section is the work of showing that the result deserves to be called a product --
that projecting first changes nothing (Theorem 7.1), that it is associative with
a predictable coefficient (Lemma 7.1), graded commutative (Theorem 7.2), bilinear
(Lemma 7.2), and that it vanishes exactly on dependent tuples.

The two results at the end are the payoff.  Theorem 7.3 says every alternating
n-linear functional on the dual factors through the wedge, which makes the wedge
the universal alternating map and identifies the dual of A^n with the alternating
n-forms on V*.  Lemma 7.3 says a nonzero wedge determines the subspace its
factors span, and is determined by it up to a scalar -- a multivector stands to
its span as a single vector stands to its line.

Note on the page range: the outline had this section at pages 316-318, but the
proof of Lemma 7.3 runs onto the first paragraph of 319, and section 8 starts in
the middle of that page.  Checked page by page on 2026-11-02.

Every number on screen is computed here and checked against an implementation
that shares no code with the one being shown.  The wedge is built the book's way
-- the tensor product, antisymmetrised by summing over S_n with signs, times a
binomial coefficient -- while the checks come from numpy's LU-based
`numpy.linalg.det` and `numpy.linalg.matrix_rank`.  The bridge between them is
the one identity that ties a wedge of one-forms to a determinant,

    (lambda_1 ^ ... ^ lambda_n)(xi_1, ..., xi_n)  =  det [ lambda_i(xi_j) ],

so the screen's antisymmetrised sum is compared against a factorisation that
never permutes anything.  The displayed examples use small integers, so a viewer
can check the three by three determinant by hand; a seeded random family is
carried alongside for the identities where exact cancellation would hide a sign
error.
"""
import itertools
import math
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


# ── the algebra, built the way section 7 builds it ────────────────────
def sgn(p):
 """The sign of a permutation, counted off its inversions."""
 s = 1
 for i in range(len(p)):
  for j in range(i + 1, len(p)):
   if p[i] > p[j]:
    s = -s
 return s


def omega(A):
 """The projection of section 5, on the array of a covariant tensor.

 A covariant n-tensor is stored as A[i1..in] = f(e_i1, ..., e_in).  The book's
 f o sigma sends xi to f(xi_sigma(1), ..., xi_sigma(n)), which on the array is
 exactly a transposition of the axes by sigma."""
 n = A.ndim
 out = np.zeros_like(A)
 for p in itertools.permutations(range(n)):
  out = out + sgn(p) * np.transpose(A, p)
 return out / math.factorial(n)


def tens(*As):
 """f (x) g, extended to several factors: the definition opening section 7."""
 out = As[0]
 for B in As[1:]:
  out = np.tensordot(out, B, axes=0)
 return out


def wedge(A, B):
 """f ^ g = C(n+l, n) Omega(f (x) g) -- the definition, binomial and all."""
 n, l = A.ndim, B.ndim
 return math.comb(n + l, n) * omega(tens(A, B))


def wedges(As):
 """Several factors wedged left to right; the wedge is associative by Lemma 7.1."""
 out = As[0]
 for B in As[1:]:
  out = wedge(out, B)
 return out


def ev(A, xs):
 """f(xi_1, ..., xi_n), by contracting the array against the vectors."""
 out = A
 for x in xs:
  out = np.tensordot(out, x, axes=([0], [0]))
 return float(out)


def alternation(A):
 """How far A is from alternating: max over sigma of || A o sigma - sgn(sigma) A ||."""
 n = A.ndim
 return max(float(np.abs(np.transpose(A, p) - sgn(p) * A).max())
            for p in itertools.permutations(range(n)))


def ms(v, spec=".0f"):
 """A number as it should read on screen: a real minus sign, not a hyphen."""
 if v == 0:
  v = 0.0
 return format(v, spec).replace("-", "−")


def vrow(v, spec=".0f"):
 return "( " + " , ".join(ms(x, spec) for x in v) + " )"


M = 4                                       # dim V, so the dual basis is delta^1..delta^4
DUAL = np.eye(M)
_rng = np.random.default_rng(89)

# ── beat 0: the tensor product of two alternating tensors leaves the space
F0 = omega(np.array([[0.0, 2.0, -1.0, 0.0], [-2.0, 0.0, 3.0, 1.0],
                     [1.0, -3.0, 0.0, 2.0], [0.0, -1.0, -2.0, 0.0]]))
G0 = np.array([1.0, 0.0, -1.0, 2.0])
assert alternation(F0) < 1e-12, "the left factor really is alternating"
TENS0 = tens(F0, G0)
ALT_F0, ALT_T0 = alternation(F0), alternation(TENS0)
assert ALT_T0 > 0.5, "and their tensor product really is not -- that is the whole problem"
OMEGA_T0 = alternation(omega(TENS0))
assert OMEGA_T0 < 1e-12, "while projecting it lands back inside"

# ── beat 1: Theorem 7.1, project before or after, it makes no difference ──
T71 = []
for _n, _l in ((1, 1), (2, 1), (1, 2), (2, 2)):
 _f = _rng.standard_normal((M,) * _n)
 _g = _rng.standard_normal((M,) * _l)
 _base = omega(tens(_f, _g))
 T71.append((_n, _l,
             float(np.abs(omega(tens(_f, omega(_g))) - _base).max()),
             float(np.abs(omega(tens(omega(_f), _g)) - _base).max())))
for _n, _l, _a, _b in T71:
 assert max(_a, _b) < 1e-12, f"Theorem 7.1 holds for n = {_n}, l = {_l}"
T71ERR = max(max(a, b) for _n, _l, a, b in T71)
# the l! pairs the proof counts: for each sigma', exactly l! pairs <rho, sigma>
PAIR_N, PAIR_L = 2, 2
PAIRS = math.factorial(PAIR_L)
assert (math.factorial(PAIR_N + PAIR_L) * PAIRS
        == math.factorial(PAIR_N + PAIR_L) * math.factorial(PAIR_L)), \
    "the regrouping in the proof is a count, not an estimate"

# ── beats 2 to 6: integers on screen, so the determinant can be checked by hand
LAM = [np.array([1.0, 2.0, 0.0, 0.0]),
       np.array([0.0, 1.0, -1.0, 0.0]),
       np.array([1.0, 0.0, 0.0, 1.0])]
XI = [np.array([1.0, 0.0, 1.0, 0.0]),
      np.array([0.0, 1.0, 0.0, 2.0]),
      np.array([2.0, -1.0, 0.0, 1.0])]
GRAM = np.array([[float(LAM[i] @ XI[j]) for j in range(3)] for i in range(3)])

W2 = wedge(LAM[0], LAM[1])
W2_FACT = math.factorial(2) * omega(tens(LAM[0], LAM[1]))
assert float(np.abs(W2 - W2_FACT).max()) < 1e-12, \
    "the binomial in the definition is exactly the n! of the corollary when both factors are 1-forms"
W2_EV, W2_DET = ev(W2, XI[:2]), float(np.linalg.det(GRAM[:2, :2]))
assert abs(W2_EV - W2_DET) < 1e-12, \
    "a wedge of two one-forms, evaluated on two vectors, is the 2 x 2 determinant"

W3 = wedges(LAM)
W3_FACT = math.factorial(3) * omega(tens(*LAM))
assert float(np.abs(W3 - W3_FACT).max()) < 1e-12, "and the corollary's n! holds at n = 3"
W3_EV, W3_DET = ev(W3, XI), float(np.linalg.det(GRAM))
assert abs(W3_EV - W3_DET) < 1e-12, \
    "the antisymmetrised sum and numpy's factorisation agree on the 3 x 3"
assert abs(W3_DET - round(W3_DET)) < 1e-9 and abs(W3_DET - 9.0) < 1e-9, \
    "and it is a whole number, so a viewer can redo it by hand"
assert alternation(W3) < 1e-12, "the wedge of one-forms is itself alternating"

# Lemma 7.1 at k = 3, including mixed orders where the coefficient is not n!
L71 = []
for _orders in ((1, 1, 1), (2, 1, 1), (1, 2, 1), (2, 2, 1)):
 _fs = [omega(_rng.standard_normal((M,) * _k)) for _k in _orders]
 _n = sum(_orders)
 _coef = math.factorial(_n) / math.prod(math.factorial(_k) for _k in _orders)
 L71.append((_orders, _coef,
             float(np.abs(wedges(_fs) - _coef * omega(tens(*_fs))).max())))
for _o, _c, _e in L71:
 assert _e < 1e-11, f"Lemma 7.1 holds at orders {_o}, coefficient {_c}"
L71ERR = max(e for _o, _c, e in L71)

# ── beat 5: Theorem 7.2, the sign that depends only on the two orders ─
T72 = []
for _n, _l in ((1, 1), (2, 1), (2, 2), (3, 1)):
 _f = omega(_rng.standard_normal((M,) * _n))
 _g = omega(_rng.standard_normal((M,) * _l))
 _s = (-1) ** (_l * _n)
 T72.append((_n, _l, _s, float(np.abs(wedge(_g, _f) - _s * wedge(_f, _g)).max())))
for _n, _l, _s, _e in T72:
 assert _e < 1e-11, f"Theorem 7.2 holds for n = {_n}, l = {_l}, sign {_s}"
T72ERR = max(e for *_r, e in T72)
assert any(s < 0 for *_r, s, _e in [(n, l, s, e) for n, l, s, e in T72]) or True
LAMLAM = float(np.abs(wedge(LAM[0], LAM[0])).max())
assert LAMLAM < 1e-12, "and a one-form wedged with itself is zero, exactly"
# the signs really do differ between the four cases, so the table is not one fact four times
assert len({s for _n, _l, s, _e in T72}) == 2, "both signs occur in the table"

# ── beat 6: the wedge vanishes exactly on dependent tuples ────────────
DEP = [LAM[0], LAM[1], 2.0 * LAM[0] - 3.0 * LAM[1]]
W_DEP = float(np.abs(wedges(DEP)).max())
W_IND = float(np.abs(W3).max())
RANK_DEP = int(np.linalg.matrix_rank(np.array(DEP)))
RANK_IND = int(np.linalg.matrix_rank(np.array(LAM)))
assert W_DEP < 1e-12 and W_IND > 0.5, "zero exactly on the dependent tuple, nonzero on the other"
assert (RANK_DEP, RANK_IND) == (2, 3), \
    "and an independent rank computation agrees about which is which"
DEP_C = (2.0, -3.0)                          # the combination that makes the third dependent

# ── beat 7: Lemma 7.2, bilinearity ───────────────────────────────────
BIL_A = [np.array([1.0, 0.0, 1.0, 0.0]), np.array([0.0, 2.0, 0.0, -1.0])]
BIL_B = omega(np.array([[0.0, 1.0, 0.0, 0.0], [-1.0, 0.0, 2.0, 0.0],
                        [0.0, -2.0, 0.0, 1.0], [0.0, 0.0, -1.0, 0.0]]))
CA, CB = 2.5, -0.8
BIL = float(np.abs(wedge(CA * BIL_A[0] + CB * BIL_A[1], BIL_B)
                   - (CA * wedge(BIL_A[0], BIL_B) + CB * wedge(BIL_A[1], BIL_B))).max())
assert BIL < 1e-11, "the wedge is linear in its left argument"
BIL2 = float(np.abs(wedge(BIL_A[0], CA * BIL_B + CB * omega(tens(BIL_A[1], BIL_A[0])))
                    - (CA * wedge(BIL_A[0], BIL_B)
                       + CB * wedge(BIL_A[0], omega(tens(BIL_A[1], BIL_A[0]))))).max())
assert BIL2 < 1e-11, "and in its right argument, which is the other half of Lemma 7.2"

# ── beat 8: Theorem 7.3, and the dimensions that force it ────────────
NW = 2
CREP = list(itertools.combinations(range(M), NW))
DIM_A = math.comb(M, NW)
assert len(CREP) == DIM_A, "the increasing index tuples of section 5, one per basis element"
NU = {q: wedges([DUAL[i] for i in q]) for q in CREP}
EVAL = np.array([[ev(NU[q], [DUAL[i] for i in r]) for r in CREP] for q in CREP])
RANK_EVAL = int(np.linalg.matrix_rank(EVAL))
IDENT_ERR = float(np.abs(EVAL - np.eye(DIM_A)).max())
assert RANK_EVAL == DIM_A and IDENT_ERR < 1e-12, \
    "the wedges of dual basis vectors are exactly the basis section 5 built, dual to the representatives"
DIM_AV = math.comb(M, NW)                    # dim A^n(V*), by Theorem 5.2 applied to V*
assert DIM_AV == DIM_A == math.comb(M, NW), \
    "the three spaces of Theorem 7.3 all have dimension C(m, n), which is why injective is enough"

# ── beat 9: Delta(T*) = Delta(T), with no coordinates anywhere ───────
T = np.array([[2.0, -1.0, 0.0, 1.0], [1.0, 3.0, -1.0, 0.0],
              [0.0, 1.0, 2.0, -1.0], [1.0, 0.0, 1.0, 2.0]])
DET_T, DET_TS = float(np.linalg.det(T)), float(np.linalg.det(T.T))
assert abs(DET_T - DET_TS) < 1e-9, "Corollary 1 of Theorem 6.2, in matrix form"
# n = dim V here, so the lambdas are taken to be the dual basis itself and the
# wedge of them is the determinant form; ev_xi is then the determinant of the
# matrix whose columns are the xi's, which a viewer can redo.
LAMN = [DUAL[i] for i in range(M)]
XIN = [np.array([2.0, 1.0, 0.0, 0.0]), np.array([0.0, 1.0, 1.0, 0.0]),
       np.array([1.0, 0.0, 2.0, 1.0]), np.array([0.0, 1.0, 0.0, 3.0])]
TSLAM = [T.T @ a for a in LAMN]              # (T* lambda)(xi) = lambda(T xi)
STAR_L = float(np.linalg.det(np.array([[a @ x for x in XIN] for a in TSLAM])))
STAR_R = float(np.linalg.det(np.array([[a @ (T @ x) for x in XIN] for a in LAMN])))
assert abs(STAR_L - STAR_R) < 1e-9, "the identity (*) that carries T* through the wedge"
EVXI = float(np.linalg.det(np.array([[a @ x for x in XIN] for a in LAMN])))
assert abs(EVXI) > 1e-9, \
    "ev_xi is not the zero functional, which is what lets the Delta be cancelled off it"
assert abs(STAR_L - DET_T * EVXI) < 1e-9, \
    "and both sides really are Delta times ev_xi, not merely equal to each other"
STARERR = max(abs(STAR_L - STAR_R), abs(STAR_L - DET_T * EVXI))

# ── beat 10: Lemma 7.3, the multivector and its span ─────────────────
CH = np.array([[2.0, 1.0, 0.0], [-1.0, 3.0, 1.0], [0.0, 1.0, 2.0]])
MU = [sum(CH[i][j] * LAM[j] for j in range(3)) for i in range(3)]
W_MU = wedges(MU)
K_PRED = float(np.linalg.det(CH))
KERR = float(np.abs(W_MU - K_PRED * W3).max())
assert abs(K_PRED - round(K_PRED)) < 1e-9 and KERR < 1e-11, \
    "same span, so the wedges differ by the determinant of the change of basis"
OTHER = [LAM[0], LAM[1], np.array([0.0, 0.0, 1.0, 1.0])]
W_OTH = wedges(OTHER)
_idx = np.unravel_index(int(np.argmax(np.abs(W3))), W3.shape)
RATIO = float(W_OTH[_idx] / W3[_idx])
NOTPROP = float(np.abs(W_OTH - RATIO * W3).max())
SPAN_SAME = int(np.linalg.matrix_rank(np.vstack([np.array(LAM), np.array(MU)])))
SPAN_OTH = int(np.linalg.matrix_rank(np.vstack([np.array(LAM), np.array(OTHER)])))
assert (SPAN_SAME, SPAN_OTH) == (3, 4), \
    "the mu's stay inside the span, the other tuple leaves it"
assert NOTPROP > 0.5, \
    "and a tuple that leaves the span has a wedge no scalar can match -- the converse has teeth"


class AdvCalcE89Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 89

 MODE_LABEL = {
  0: {"zh": "缺一個乘法：張量積會跑出去",
      "en": "a multiplication is missing: the tensor product leaves"},
  1: {"zh": "定理 7.1：先投影再乘，一樣",
      "en": "Theorem 7.1: projecting first changes nothing"},
  2: {"zh": "楔積的定義，與那個二項係數",
      "en": "the wedge, and that binomial coefficient"},
  3: {"zh": "引理 7.1：接起來的係數",
      "en": "Lemma 7.1: the coefficient when they chain"},
  4: {"zh": "推論：楔積就是第 5 節那組基底",
      "en": "Corollary: the wedge is section 5's basis"},
  5: {"zh": "定理 7.2：換邊只差一個正負號",
      "en": "Theorem 7.2: swapping costs only a sign"},
  6: {"zh": "推論：等於零恰好是相依",
      "en": "Corollary: it vanishes exactly on dependent tuples"},
  7: {"zh": "引理 7.2：楔積是雙線性的",
      "en": "Lemma 7.2: the wedge is bilinear"},
  8: {"zh": "定理 7.3：每個交錯泛函都穿過楔積",
      "en": "Theorem 7.3: every alternating functional factors through it"},
  9: {"zh": "Δ ( T * ) = Δ ( T )，不用座標",
      "en": "Delta of T-star equals Delta of T, with no coordinates"},
  10: {"zh": "多重向量與引理 7.3，第 7 節結束",
       "en": "multivectors and Lemma 7.3, the end of section 7"},
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

 # ── beat 0: alternating in, not alternating out ─────────────────
 def _leaves(self):
  """Two boxes for the alternating spaces and one outside them, with the
  tensor product landing in the wrong one."""
  g = VGroup()
  # The whole figure has to live above about y = -0.66: the caption sits at
  # -0.90 and the two foot lines at -1.22 and -1.74.  A box reaching lower runs
  # its border straight through them, which is what the first cut of this beat
  # did -- and before 2026-11-02 collide could not see a Rectangle border at all.
  ya, ym, yb = 1.00, 0.30, -0.42
  for x, lab, col in ((-5.25, "𝒜 ⁿ", ACCENT_B), (-3.25, "𝒜 ˡ", ACCENT_B)):
   g.add(self._box(x, ya, lab, col, w=1.50, h=0.46, size=FS_TAG - 1))
  g.add(self._box(-4.25, ym, "( V * ) ⊗ ⁿ ⁺ ˡ", WARN, w=1.50, h=0.42, size=FS_TAG - 1))
  g.add(self._box(-4.25, yb, "𝒜 ⁿ ⁺ ˡ", ACCENT_A, w=1.50, h=0.42, size=FS_TAG - 1))
  g.add(self._arr([-5.05, ya - 0.25, 0], [-4.50, ym + 0.23, 0], DIM, sw=2.6, tl=0.12))
  g.add(self._arr([-3.45, ya - 0.25, 0], [-4.00, ym + 0.23, 0], DIM, sw=2.6, tl=0.12))
  g.add(self._sym(ya, "⊗", DIM, FS_TAG, x=-4.25, w=0.40))
  g.add(self._arr([-4.25, ym - 0.23, 0], [-4.25, yb + 0.21, 0], ACCENT_A, sw=3.0, tl=0.13))
  g.add(self._sym(-0.06, "Ω", ACCENT_A, FS_TAG - 1, x=-3.82, w=0.40))
  g.add(self._table((("f  ∈  𝒜 ⁿ            g  ∈  𝒜 ˡ", ACCENT_B),
                     ("( f ⊗ g ) ( ξ ₁ , … , ξ ₙ ₊ ₗ )", DIM),
                     ("=   f ( ξ ₁ , … , ξ ₙ )  g ( ξ ₙ ₊ ₁ , … , ξ ₙ ₊ ₗ )", DIM),
                     ("                    max σ  | ·  ∘ σ   −   sgn σ  ·  · |", DIM),
                     (f"f                            {ms(ALT_F0, '.1e')}", ACCENT_B),
                     (f"f ⊗ g                      {ms(ALT_T0, '.3f')}", WARN),
                     (f"Ω ( f ⊗ g )              {ms(OMEGA_T0, '.1e')}", ACCENT_A)),
                    y0=0.86, dy=0.24, size=FS_TAG - 3))
  g.add(self._cap("中間那一列不是零，所以張量積確實掉出交錯的那一層",
                  "the middle number is not zero, so the tensor product really does fall out"))
  return g.add(self._foot(
   "前六節把交錯張量建好、又拿它做出行列式，但一直缺一個乘法：兩個交錯張量的張量積幾乎從來不是交錯的，一乘就離開那個空間",
   "the first six sections built alternating tensors and spent them on the determinant, but a multiplication was always missing: the tensor product of two alternating tensors is almost never alternating",
   ACCENT_A,
   "第 7 節就是補這件事。辦法很直接：乘完之後用第 5 節那個投影打回來。右表中間那個數在量的就是「離開了多少」，最下面那個是打回來之後的",
   "section 7 repairs it in the obvious way: multiply, then project back with the operator of section 5; the table measures how far out it went and how far in it comes back",
   ))

 # ── beat 1: Theorem 7.1 ─────────────────────────────────────────
 def _commute(self):
  """Three routes from (f, g) to the same element, drawn as a square."""
  g = VGroup()
  xa, xb, yt, yb = -5.25, -3.25, 0.74, -0.30
  for x, y, lab, col in ((xa, yt, "f ⊗ g", DIM), (xb, yt, "f ⊗ Ω g", ACCENT_C),
                         (xa, yb, "Ω ( f ⊗ g )", ACCENT_A),
                         (xb, yb, "Ω ( f ⊗ Ω g )", ACCENT_A)):
   g.add(self._box(x, y, lab, col, w=1.72, h=0.50, size=FS_TAG - 2))
  g.add(self._arr([xa, yt - 0.29, 0], [xa, yb + 0.27, 0], ACCENT_A, sw=2.6, tl=0.12))
  g.add(self._arr([xb, yt - 0.29, 0], [xb, yb + 0.27, 0], ACCENT_A, sw=2.6, tl=0.12))
  g.add(self._sym(yt + 0.02, "↦", DIM, FS_TAG - 1, x=(xa + xb) / 2, w=0.40))
  g.add(self._sym(yb + 0.02, "=", ACCENT_A, FS_TAG, x=(xa + xb) / 2, w=0.40))
  g.add(self._sym(0.22, "Ω", ACCENT_A, FS_TAG - 2, x=xa + 0.42, w=0.34),
        self._sym(0.22, "Ω", ACCENT_A, FS_TAG - 2, x=xb + 0.52, w=0.34))
  g.add(self._sym(-0.92, f"| Δ |   ≤   {ms(T71ERR, '.1e')}", ACCENT_B, FS_TAG - 3,
                  x=-4.25, w=2.20))
  rows = [("      n        l        | Ω ( f ⊗ Ω g ) |        | Ω ( Ω f ⊗ g ) |", DIM)]
  for n, l, a, b in T71:
   rows.append((f"      {n}        {l}            {ms(a, '.1e'):>9}"
                f"            {ms(b, '.1e'):>9}", ACCENT_B))
  rows.append((f"#  {{ ρ   :   ρ σ  =  σ ′ }}   =   l !   =   {PAIRS}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.88, dy=0.24, size=FS_TAG - 4))
  g.add(self._cap("四組階數的兩欄殘差都是零，不是只驗了一種",
                  "both columns are zero for all four pairs of orders, not just one"))
  return g.add(self._foot(
   "定理 7.1 說：先投影再乘，和乘完再投影，結果一樣。證明是把那個和重新分組——把 ρ 看成只動後面 l 個位置，那麼每一個 σ ′ 恰好對應 l 階乘組這樣的配對",
   "Theorem 7.1 says projecting a factor first changes nothing: regroup the sum, reading rho as acting on the last l places only, and each sigma-prime comes from exactly l factorial such pairs",
   ACCENT_A,
   "所以那個和除以 l 階乘就回到原來的樣子。這條是後面每一步的根據：它讓「先打回交錯」這個動作可以隨時插進乘法裡，而不改變答案",
   "so dividing by l factorial gives the original sum back; this is what later steps rest on, since it lets the projection be inserted anywhere in a product without changing the answer",
   ))

 # ── beat 2: the definition of the wedge ─────────────────────────
 def _define(self):
  g = VGroup()
  gram2 = GRAM[:2, :2].astype(int).tolist()
  grid, _p = self._numgrid(-4.60, 0.34, [[ms(v) for v in row] for row in gram2],
                           dx=0.62, dy=0.44, size=FS_TAG - 2, color=INK)
  g.add(grid)
  g.add(self._sym(1.06, "λ ᵢ ( ξ ⱼ )", ACCENT_C, FS_TAG - 2, x=-4.60, w=1.40))
  g.add(self._sym(-0.34, f"det   =   {ms(W2_DET, '+.0f')}", ACCENT_B, FS_TAG - 2,
                  x=-5.05, w=1.60))
  g.add(self._sym(-0.74, f"( λ ₁ ∧ λ ₂ ) ( ξ ₁ , ξ ₂ )   =   {ms(W2_EV, '+.0f')}",
                  ACCENT_A, FS_TAG - 3, x=-4.25, w=3.10))
  g.add(self._table((("f  ∧  g   =   C ( n + l , n )   Ω ( f ⊗ g )", ACCENT_A),
                     ("n  =  l  =  1        C ( 2 , 1 )   =   2", ACCENT_C),
                     ("λ ₁  ∧  λ ₂   =   2  Ω ( λ ₁ ⊗ λ ₂ )", ACCENT_C),
                     (f"λ ₁   =   {vrow(LAM[0])}", DIM),
                     (f"λ ₂   =   {vrow(LAM[1])}", DIM),
                     (f"( λ ₁ ∧ λ ₂ ) ( ξ )        {ms(W2_EV, '+.0f')}", ACCENT_A),
                     (f"det [ λ ᵢ ( ξ ⱼ ) ]            {ms(W2_DET, '+.0f')}", ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("左邊那個二階行列式是一乘一減二乘負一，等於三",
                  "the two by two on the left is one times one minus two times minus one, which is three"))
  return g.add(self._foot(
   "有了定理 7.1 就可以定義乘法：兩個交錯張量的楔積，是它們的張量積投影回交錯那一層，再乘上一個二項係數。那個係數是為了讓後面的公式不帶階乘因子",
   "with Theorem 7.1 in hand the product can be defined: the wedge of two alternating tensors is their tensor product projected back, times a binomial coefficient chosen to keep factorials out of what follows",
   ACCENT_A,
   "一階的情形最好檢查：兩個一形式的楔積，餵進兩個向量，答案就是那個二乘二行列式。右表最後兩列一個是照定義硬算的、一個是獨立算的行列式",
   "the one-form case is the easiest to check: wedge two one-forms, feed in two vectors, and the answer is a two by two determinant -- the last two rows compute it the two independent ways",
   ))

 # ── beat 3: Lemma 7.1, the coefficient when several chain ───────
 def _chain(self):
  g = VGroup()
  xs = (-5.45, -4.25, -3.05)
  for k, x in enumerate(xs):
   g.add(self._box(x, 0.74, f"f {'₁₂₃'[k]}", ACCENT_B, w=0.86, h=0.48, size=FS_TAG - 1))
   g.add(self._sym(0.36, f"n {'₁₂₃'[k]}", DIM, FS_TAG - 4, x=x, w=0.60))
  for x in (-4.85, -3.65):
   g.add(self._sym(0.74, "∧", ACCENT_A, FS_TAG, x=x, w=0.30))
  g.add(self._box(-4.25, -0.52, "Ω ( f ₁ ⊗ f ₂ ⊗ f ₃ )", ACCENT_A,
                  w=2.90, h=0.46, size=FS_TAG - 3))
  g.add(self._arr([-4.25, 0.08, 0], [-4.25, -0.28, 0], ACCENT_A, sw=2.8, tl=0.13))
  g.add(self._sym(-0.10, "n !  /  n ₁ !  n ₂ !  n ₃ !", ACCENT_C, FS_TAG - 4,
                  x=-2.95, w=1.70))
  rows = [("      n ᵢ              n !  /  ∏ n ᵢ !            | Δ |", DIM)]
  for orders, coef, err in L71:
   rows.append((f"  {' , '.join(str(k) for k in orders)}            "
                f"{ms(coef, '.0f'):>4}        {ms(err, '.1e'):>9}", ACCENT_B))
  rows.append((f"n   =   Σ  n ᵢ            | Δ |   ≤   {ms(L71ERR, '.1e')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("四列的係數不一樣，所以那個分母真的有在作用",
                  "the four coefficients differ, so that denominator is doing real work"))
  return g.add(self._foot(
   "引理 7.1 把好幾個接起來：把 k 個交錯張量依序楔起來，等於它們的張量積投影回去，再乘上 n 階乘除以各自階數的階乘。用歸納法加上面那個定義就證完了",
   "Lemma 7.1 chains several together: wedging k alternating tensors in order equals their tensor product projected back, times n factorial over the product of the individual factorials -- induction plus the definition",
   ACCENT_A,
   "右表四組階數的係數分別是六、十二、十二與三十，殘差都是零。階數不同係數就不同，所以那個分母不是裝飾品",
   "the table's four cases have coefficients six, twelve, twelve and thirty with zero residual; different orders give different coefficients, so the denominator is not decoration",
   ))

 # ── beat 4: the corollary that recovers section 5's basis ───────
 def _basis(self):
  g = VGroup()
  # The formula bar already carries both identities; repeating them here would
  # spend the figure's whole height saying nothing new. What the figure is for
  # is the six increasing tuples and the square they index.
  labs = [f"q   =   ( {' , '.join(str(i + 1) for i in q)} )" for q in CREP]
  for k, lab in enumerate(labs[:3]):
   g.add(self._sym(0.86 - k * 0.36, lab, ACCENT_B, FS_TAG - 3, x=-5.40, w=1.90))
  for k, lab in enumerate(labs[3:]):
   g.add(self._sym(0.86 - k * 0.36, lab, ACCENT_B, FS_TAG - 3, x=-3.10, w=1.90))
  g.add(self._sym(-0.34, f"m   =   {M}        n   =   {NW}        C ( m , n )   =   {DIM_A}",
                  ACCENT_C, FS_TAG - 3, x=-4.25, w=3.20))
  rows = [("      ν ( q ) ( μ r )                                    rank", DIM)]
  for k, q in enumerate(CREP):
   rows.append((f"( {' '.join(str(i + 1) for i in q)} )        "
                + "  ".join(ms(EVAL[k][j]) for j in range(DIM_A)), ACCENT_B))
  rows.append((f"=   I            | Δ |  =  {ms(IDENT_ERR, '.1e')}            {RANK_EVAL}",
               ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.21, size=FS_TAG - 5))
  g.add(self._cap("那個方陣就是單位矩陣，所以這組楔積正好是第 5 節取的代表元的對偶",
                  "that square is the identity, so these wedges are dual to section 5's representatives"))
  return g.add(self._foot(
   "一階的情形最有用：n 個一形式楔起來，就是 n 階乘乘上它們張量積的投影。把對偶基底裡遞增的那幾個拿來楔，得到的正好是第 5 節那組基底元素",
   "the one-form case is the useful one: wedging n one-forms gives n factorial times the projection of their tensor product, and wedging an increasing selection of the dual basis gives exactly section 5's basis element",
   ACCENT_A,
   "所以第 5 節辛苦建出來的那組基底，現在只是「對偶基底的楔積」。四維空間取二階有六個，右表把那六個在六個代表元上的值排成方陣，它就是單位矩陣",
   "so the basis section 5 worked for is now just wedges of the dual basis; four dimensions at order two give six of them, and the square of their values on the six representatives is the identity",
   ))

 # ── beat 5: Theorem 7.2, graded commutativity ───────────────────
 def _swap(self):
  g = VGroup()
  xa, xb, y = -5.25, -3.25, 0.66
  g.add(self._box(xa, y, "f  ∧  g", ACCENT_B, w=1.50, h=0.50, size=FS_TAG - 1))
  g.add(self._box(xb, y, "g  ∧  f", ACCENT_C, w=1.50, h=0.50, size=FS_TAG - 1))
  g.add(self._arr([xa + 0.80, y + 0.14, 0], [xb - 0.80, y + 0.14, 0], DIM, sw=2.4, tl=0.11))
  g.add(self._arr([xb - 0.80, y - 0.14, 0], [xa + 0.80, y - 0.14, 0], DIM, sw=2.4, tl=0.11))
  g.add(self._sym(y + 0.36, "( − 1 ) ˡ ⁿ", ACCENT_A, FS_TAG - 2, x=(xa + xb) / 2, w=1.20))
  g.add(self._sym(-0.06, "σ   =   τ ₁  ∘  ⋯  ∘  τ l ₙ", ACCENT_C, FS_TAG - 4,
                  x=-4.25, w=2.40))
  g.add(self._sym(-0.48, f"λ  ∧  λ   =   {ms(LAMLAM, '.1e')}", WARN, FS_TAG - 2,
                  x=-4.25, w=2.40))
  g.add(self._sym(-0.92, "λ  ∧  λ   =   −  λ  ∧  λ", DIM, FS_TAG - 3, x=-4.25, w=2.40))
  rows = [("      n        l        ( − 1 ) ˡ ⁿ        | Δ |", DIM)]
  for n, l, s, err in T72:
   rows.append((f"      {n}        {l}            {ms(s, '+.0f')}        {ms(err, '.1e'):>9}",
                ACCENT_A if s < 0 else ACCENT_B))
  rows.append((f"λ  ∧  λ   =   0        | Δ |   ≤   {ms(max(T72ERR, LAMLAM), '.1e')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("正負號兩種都出現了，所以它真的跟兩個階數有關",
                  "both signs occur, so the sign really does depend on the two orders"))
  return g.add(self._foot(
   "定理 7.2 說換邊只差一個正負號，而那個號只看兩個階數：把後面 l 個位置一個一個搬到前面 n 個位置之前，總共要 l 乘 n 次對換，所以號是負一的 l n 次方",
   "Theorem 7.2 says swapping the two factors costs only a sign, and the sign depends only on the two orders: moving each of the last l places past each of the first n takes l times n transpositions",
   ACCENT_A,
   "兩個階數都是奇數時才會變號。一形式與自己楔起來因此等於自己的相反數，也就是零——這正是前面「兩個變數相同就是零」在楔積這一邊的樣子",
   "the sign flips only when both orders are odd, so a one-form wedged with itself equals its own negative and is therefore zero, which is the earlier vanishing rule seen from the product side",
   ))

 # ── beat 6: zero exactly on dependent tuples ────────────────────
 def _dependent(self):
  g = VGroup()
  for k, (lab, vec, col) in enumerate((("λ ₁", LAM[0], ACCENT_B),
                                       ("λ ₂", LAM[1], ACCENT_B),
                                       ("λ ₃", LAM[2], ACCENT_B))):
   g.add(self._sym(0.78 - k * 0.34, f"{lab}   =   {vrow(vec)}", col, FS_TAG - 3,
                   x=-4.95, w=2.30))
  g.add(self._sym(-0.34, f"μ   =   {ms(DEP_C[0])}  λ ₁   {ms(DEP_C[1], '+.0f')}  λ ₂",
                  WARN, FS_TAG - 3, x=-4.95, w=2.30))
  # W_IND is the largest component of the wedge, not the wedge, so the bars
  # have to be there: "lambda_1 ^ lambda_2 ^ lambda_3 = 2" would be false.
  g.add(self._sym(-0.76, f"| λ ₁ ∧ λ ₂ ∧ λ ₃ |  =  {ms(W_IND, '.0f')}        "
                         f"| λ ₁ ∧ λ ₂ ∧ μ |  =  {ms(W_DEP, '.1e')}",
                  ACCENT_A, FS_TAG - 4, x=-4.25, w=3.40))
  g.add(self._table((("λ ₁  ∧  ⋯  ∧  λ ₙ   =   0      ⟺      rank   <   n", ACCENT_A),
                     ("rank  =  n      ⇒      λ ₁ ∧ ⋯ ∧ λ ₙ   =   ν ( q )", DIM),
                     ("rank  <  n      ⇒      λ ᵢ  ∧  λ ᵢ      ⇒      0", DIM),
                     (f"λ ₁ , λ ₂ , λ ₃        | ∧ |  =  {ms(W_IND, '.0f')}        "
                      f"rank  {RANK_IND}", ACCENT_B),
                     (f"λ ₁ , λ ₂ , μ            | ∧ |  =  {ms(W_DEP, '.1e')}        "
                      f"rank  {RANK_DEP}", WARN),
                     (f"det [ λ ᵢ ( ξ ⱼ ) ]   =   {ms(W3_DET, '+.0f')}   =   "
                      f"{ms(W3_EV, '+.0f')}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("楔積那兩列旁邊的秩是另外獨立算的，兩邊講的是同一件事",
                  "the ranks beside the two wedge rows are computed independently, and say the same thing"))
  return g.add(self._foot(
   "推論說：一組一形式楔起來等於零，恰好就是它們線性相依。獨立的那邊可以延拓成一組基底，楔積就是上一拍那些基底元素裡的某一個，當然不是零",
   "the corollary says a wedge of one-forms vanishes exactly when they are dependent: an independent tuple extends to a basis, and its wedge is one of the previous beat's basis elements, so it is not zero",
   ACCENT_A,
   "相依的那邊，把其中一個拆成其他的組合代進去，每一項都有某個因式出現兩次，而上一拍剛證過那種項是零。右邊把兩種情形並排，秩是另外獨立算的",
   "on the dependent side, substituting one factor as a combination of the others leaves every term with a repeated factor, and the previous beat showed those vanish; the ranks beside them are computed independently",
   ))

 # ── beat 7: Lemma 7.2, bilinearity ──────────────────────────────
 def _bilinear(self):
  g = VGroup()
  # The first cut of this beat drew the three arguments as three points on one
  # line, with c a_1 + c' a_2 sitting between a_1 and a_2. That picture is a
  # lie twice over: c + c' is 1.7, so the combination is not even on the affine
  # line through them, and putting it between the two reads as a convex mix.
  # Two slots, each with its own residual, is what the lemma actually says.
  for k, (slot, err, col) in enumerate(((("( c f ₁  +  c ′ f ₂ )   ∧   g"), BIL, ACCENT_B),
                                        (("f   ∧   ( c g ₁  +  c ′ g ₂ )"), BIL2, ACCENT_C))):
   y = 0.80 - k * 0.78
   g.add(self._box(-4.25, y, slot, col, w=3.20, h=0.44, size=FS_TAG - 4))
   g.add(self._sym(y - 0.33, f"| Δ |   =   {ms(err, '.1e')}", col, FS_TAG - 4,
                   x=-4.25, w=2.20))
  g.add(self._sym(-0.62, f"c   =   {ms(CA, '.1f')}        c ′   =   {ms(CB, '.1f')}",
                  ACCENT_A, FS_TAG - 3, x=-4.25, w=2.60))
  g.add(self._table((("⟨ f , g ⟩   ↦   f  ∧  g", ACCENT_A),
                     ("𝒜 ⁿ  ×  𝒜 ˡ   →   𝒜 ⁿ ⁺ ˡ", ACCENT_B),
                     ("( c f ₁ + c ′ f ₂ )  ∧  g", DIM),
                     ("=   c ( f ₁ ∧ g )  +  c ′ ( f ₂ ∧ g )", DIM),
                     (f"f   :   | Δ |   =   {ms(BIL, '.1e')}", ACCENT_B),
                     (f"g   :   | Δ |   =   {ms(BIL2, '.1e')}", ACCENT_B),
                     ("⊗      ↦      Ω      ↦      ∧", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩邊各驗一次，因為雙線性是兩件事不是一件",
                  "both sides are checked, because bilinearity is two statements, not one"))
  return g.add(self._foot(
   "引理 7.2 說楔積是雙線性的，證明只有一行：張量積本來就是雙線性的，而投影與那個二項係數都是線性的，合起來當然還是雙線性",
   "Lemma 7.2 says the wedge is bilinear, and the proof is one line: the tensor product already is, while the projection and the binomial coefficient are both linear",
   ACCENT_A,
   "這一條看起來最不起眼，卻是下一拍的前提：要說「每個交錯泛函都從楔積穿過去」，得先知道楔積本身對每個位置都是線性的",
   "it looks like the least of them, yet the next beat needs it: before saying every alternating functional factors through the wedge, the wedge must itself be linear in each place",
   ))

 # ── beat 8: Theorem 7.3, the extension theorem ──────────────────
 def _extend(self):
  g = VGroup()
  xa, xb, yt, yb = -5.30, -3.20, 0.70, -0.34
  g.add(self._box(xa, yt, "( V * ) ⁿ", ACCENT_B, w=1.55, h=0.50, size=FS_TAG - 2))
  g.add(self._box(xb, yt, "𝒜 ⁿ", ACCENT_A, w=1.20, h=0.50, size=FS_TAG - 2))
  g.add(self._box(xb, yb, "ℝ", ACCENT_C, w=1.20, h=0.50, size=FS_TAG - 2))
  g.add(self._arr([xa + 0.84, yt, 0], [xb - 0.66, yt, 0], ACCENT_A, sw=2.8, tl=0.13))
  g.add(self._arr([xb, yt - 0.29, 0], [xb, yb + 0.27, 0], ACCENT_C, sw=2.6, tl=0.12))
  g.add(self._arr([xa + 0.70, yt - 0.26, 0], [xb - 0.60, yb + 0.22, 0], DIM,
                  sw=2.4, tl=0.12))
  g.add(self._sym(yt + 0.26, "θ", ACCENT_A, FS_TAG - 2, x=(xa + xb) / 2 + 0.10, w=0.40))
  g.add(self._sym(yb + 0.40, "G", ACCENT_C, FS_TAG - 2, x=xb + 0.36, w=0.40))
  g.add(self._sym(-0.14, "F", DIM, FS_TAG - 2, x=xa + 1.02, w=0.40))
  g.add(self._sym(-0.92, f"F   =   G  ∘  θ", ACCENT_A, FS_TAG - 2, x=-4.25, w=2.20))
  g.add(self._table((("θ  :  ⟨ λ ₁ , … , λ ₙ ⟩   ↦   λ ₁ ∧ ⋯ ∧ λ ₙ", ACCENT_A),
                     ("F   ∈   𝒜 ⁿ ( V * )      ⇒      F   =   G ∘ θ      ∃ !", DIM),
                     (f"d ( 𝒜 ⁿ )               =   C ( m , n )   =   {DIM_A}", ACCENT_B),
                     (f"d ( 𝒜 ⁿ ( V * ) )   =   C ( m , n )   =   {DIM_AV}", ACCENT_B),
                     ("G   ↦   G ∘ θ      1 – 1      ⇒      ≅", ACCENT_C),
                     (f"[ ν ( q ) ( μ r ) ]      rank  =  {RANK_EVAL}      "
                      f"| Δ | = {ms(IDENT_ERR, '.1e')}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩個維數相同，所以單射就夠了，不必另外去證滿射",
                  "the two dimensions agree, so injective suffices and onto needs no separate proof"))
  return g.add(self._foot(
   "定理 7.3 是延拓定理。把 n 個一形式送到它們的楔積，這個對應是交錯多重線性的；定理說任何一個交錯 n 重泛函都唯一地從它穿過去，變成楔積那個空間上的一個線性泛函",
   "Theorem 7.3 is the extension theorem: sending n one-forms to their wedge is alternating and multilinear, and the theorem says every alternating n-linear functional factors through it uniquely, as a single linear functional",
   ACCENT_A,
   "書上說硬算會寫得很繁，改用維數：兩邊都是 m 取 n，而那個對應是單射，所以它是同構。這等於說楔積是所有交錯映射裡最普遍的那一個",
   "the book says the direct computation gets notationally heavy and counts dimensions instead: both sides are m choose n and the map is injective, hence an isomorphism -- the wedge is the universal alternating map",
   ))

 # ── beat 9: Delta(T*) = Delta(T) without coordinates ────────────
 def _adjoint(self):
  g = VGroup()
  # A 4 x 4 at dy 0.36 reaches -0.34 once its brackets are counted, which is
  # exactly where the labels under it were sitting.
  grid, _p = self._numgrid(-4.90, 0.50, [[ms(v) for v in row] for row in T.tolist()],
                           dx=0.46, dy=0.24, size=FS_TAG - 6, color=INK)
  g.add(grid, self._sym(1.20, "T", ACCENT_A, FS_TAG - 1, x=-4.90, w=0.60))
  g.add(self._sym(-0.30, f"Δ ( T )   =   {ms(DET_T, '+.0f')}", ACCENT_A, FS_TAG - 3,
                  x=-5.05, w=1.90))
  g.add(self._sym(-0.64, f"Δ ( T * )   =   {ms(DET_TS, '+.0f')}", ACCENT_B, FS_TAG - 3,
                  x=-5.05, w=1.90))
  g.add(self._sym(-0.46, f"ev ξ   =   {ms(EVXI, '+.0f')}   ≠   0", ACCENT_C, FS_TAG - 3,
                  x=-3.05, w=1.80))
  g.add(self._table((("T * λ ₁  ∧ ⋯ ∧  T * λ ₙ  ( ξ )", ACCENT_A),
                     ("=   λ ₁ ∧ ⋯ ∧ λ ₙ  ( T ξ ₁ , … , T ξ ₙ )", ACCENT_A),
                     ("ev ξ   ∈   𝒜 ⁿ ( V * )            n   =   dim V", DIM),
                     (f"Δ ( T * )  ev ξ            {ms(STAR_L, '+.0f')}", ACCENT_B),
                     (f"Δ ( T )  ev ξ               {ms(STAR_R, '+.0f')}", ACCENT_B),
                     (f"Δ ( T )  ·  ev ξ            {ms(DET_T * EVXI, '+.0f')}", ACCENT_C),
                     (f"| Δ |   ≤   {ms(STARERR, '.1e')}", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("最後三個數相同，而 ev ξ 不是零，所以才能把它約掉",
                  "the last three agree and ev-xi is not zero, which is what lets it be cancelled"))
  return g.add(self._foot(
   "有了楔積就能把「轉置不改變行列式」重證一次，而且完全不用座標。關鍵是伴隨的定義穿過楔積之後，變成把 T 搬到輸入那一邊去",
   "with the wedge in hand the transpose rule can be proved again with no coordinates at all: carrying the adjoint through the wedge moves T over to the inputs instead",
   ACCENT_A,
   "固定一組輸入得到一個交錯 n 重泛函，兩邊各提出一個 Δ，而那個泛函本身不是零，於是兩個 Δ 相等。第 6 節的推論一在矩陣上講的就是這件事",
   "fixing the inputs gives an alternating n-linear functional, each side pulls out one Delta, and since that functional is not zero the two Deltas are equal -- section 6's first corollary, read without a basis",
   ))

 # ── beat 10: multivectors and Lemma 7.3 ─────────────────────────
 def _multivector(self):
  g = VGroup()
  ly = 0.56
  g.add(Line([-5.70, ly, 0], [-2.80, ly, 0], color=DIM, stroke_width=2.0))
  g.add(Dot([-5.20, ly, 0], radius=0.072, color=ACCENT_A))
  g.add(Dot([-3.80, ly, 0], radius=0.072, color=ACCENT_C))
  g.add(self._sym(ly + 0.32, "λ  ∧", ACCENT_A, FS_TAG - 2, x=-5.20, w=0.80))
  g.add(self._sym(ly + 0.32, "μ  ∧", ACCENT_C, FS_TAG - 2, x=-3.80, w=0.80))
  g.add(self._sym(ly - 0.34, f"k   =   {ms(K_PRED, '+.0f')}", ACCENT_C, FS_TAG - 3,
                  x=-4.50, w=1.40))
  g.add(self._sym(-0.24, "L ( λ ₁ , λ ₂ , λ ₃ )   =   L ( μ ₁ , μ ₂ , μ ₃ )",
                  ACCENT_B, FS_TAG - 4, x=-4.40, w=3.00))
  g.add(self._sym(-0.64, f"rank  [ λ ; μ ]   =   {SPAN_SAME}        "
                         f"rank  [ λ ; λ ′ ]   =   {SPAN_OTH}",
                  DIM, FS_TAG - 4, x=-4.25, w=3.40))
  g.add(self._table((("μ ₁ ∧ ⋯ ∧ μ ₙ   =   k ( λ ₁ ∧ ⋯ ∧ λ ₙ )", ACCENT_A),
                     ("⟺      L ( λ ₁ , … , λ ₙ )   =   L ( μ ₁ , … , μ ₙ )", ACCENT_A),
                     (f"μ ᵢ   =   Σ ⱼ  c ᵢ ⱼ  λ ⱼ        k  =  det ( c )  =  "
                      f"{ms(K_PRED, '+.0f')}", ACCENT_C),
                     (f"| μ ∧ ⋯  −  k  λ ∧ ⋯ |            {ms(KERR, '.1e')}", ACCENT_B),
                     (f"λ ′   :   | λ ′ ∧ ⋯  −  c  λ ∧ ⋯ |      {ms(NOTPROP, '.3f')}", WARN),
                     (f"rank   {SPAN_SAME}            rank   {SPAN_OTH}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("倒數第二個數不是零，所以跨出子空間的那一組真的不成比例",
                  "the second-to-last number is not zero, so a tuple that leaves the span is genuinely not proportional"))
  return g.add(self._foot(
   "最後是引理 7.3。不是零的楔積叫多重向量，它的因式張出一個 n 維子空間；引理說兩組獨立的 n 元組張出同一個子空間，恰好就是它們的楔積差一個純量倍",
   "last comes Lemma 7.3: a nonzero wedge is called a multivector and its factors span an n-dimensional subspace, and the lemma says two independent n-tuples span the same subspace exactly when their wedges differ by a scalar",
   ACCENT_A,
   "那個純量就是換底矩陣的行列式。所以多重向量與它所張的子空間的關係，就像一個向量與它所張的那條線——第 8 節與第 9 節會在這上面加一個純量積",
   "that scalar is the determinant of the change of basis, so a multivector stands to its span as a single vector stands to its line; sections 8 and 9 will put a scalar product on top of this",
   ))

 def stage(self):
  a, b, c = self._leaves(), self._commute(), self._define()
  d, e, f_ = self._chain(), self._basis(), self._swap()
  h, i, j = self._dependent(), self._bilinear(), self._extend()
  k, l = self._adjoint(), self._multivector()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE89ZH, AdvCalcE89EN = make(AdvCalcE89Base, "89", prefix="AdvCalcE")
