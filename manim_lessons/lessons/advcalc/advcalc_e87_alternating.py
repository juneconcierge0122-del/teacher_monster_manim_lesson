"""advcalc E87 -- chapter 7, section 5 (book pp. 310-312): the subspace of
alternating tensors, the projection Omega, and dim A^n = C(m, n).

This is the hinge of the chapter.  Section 2 gave the covariant tensors of
order n a basis indexed by all n-tuples of indices, so the dimension there is
m^n.  Section 5 asks for the ones that pick up the sign of a permutation when
their arguments are permuted, and the answer collapses from m^n to the binomial
coefficient: a coefficient attached to a tuple with a repeat has to be its own
negative, so only the injective tuples survive, and injective tuples with the
same range differ by a permutation, so each range set is counted n! times.  The
case n = m leaves a single representative, hence dimension one, and that is the
whole basis of the next episode -- up to a constant there is only one
alternating m-form, and the book's last display on p. 312 already prints the
determinant's formula without naming it.

Everything on screen is computed here from one representation: a covariant
tensor of order n over R^m is the array c(p) = f(a_p1, ..., a_pn), and the
permuted tensor is a transposition of that array, verified against the
pointwise definition f^s(xi) = f(xi o s^-1) rather than assumed.  So "Omega f
is alternating" is checked by actually permuting the projected array for all
six elements of S_3 and reading off the residual, and the dimension is obtained
three independent ways -- by enumerating representatives, by the binomial
formula, and by the rank of the linear system that says c(p) = sgn(s) c(p o s).
The nullity uses adjacent transpositions, which generate S_n; that shortcut is
pinned against the full group on two cases.

The example in beats 3 and 4 is a tensor of order 3 over R^4 on purpose.  Order
3 over R^3 would also be neither symmetric nor alternating, but its alternating
subspace is one-dimensional, so Omega would land in a line and "projection"
would look like "collapse"; over R^4 the target is four-dimensional and the
picture is honest.  The residuals are Frobenius norms, not sup norms: with
small integer coefficients the sup norm saturates and prints the same number
for five different permutations, which reads like a bug rather than a proof.
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


# ── permutations, and the action on a coefficient array ───────────────
def perms(n):
 return list(itertools.permutations(range(n)))


def sgn(s):
 k = 1
 for i in range(len(s)):
  for j in range(i + 1, len(s)):
   if s[i] > s[j]:
    k = -k
 return k


def invp(s):
 out = [0] * len(s)
 for i, v in enumerate(s):
  out[v] = i
 return tuple(out)


def ev(C, X):
 """f(xi_1, ..., xi_n), with row i of X the coordinates of xi_i."""
 n, m = C.ndim, C.shape[0]
 tot = 0.0
 for p in itertools.product(range(m), repeat=n):
  t = C[p]
  if t:
   for i in range(n):
    t *= X[i, p[i]]
   tot += t
 return float(tot)


def act(C, s):
 """The coefficients of f^s, where f^s(xi) = f(xi o s inverse)."""
 m, n = C.shape[0], C.ndim
 q = invp(s)
 D = np.zeros_like(C, dtype=float)
 for p in itertools.product(range(m), repeat=n):
  D[p] = C[tuple(p[q[i]] for i in range(n))]
 return D


def omega(C):
 P = perms(C.ndim)
 out = np.zeros_like(C, dtype=float)
 for s in P:
  out += sgn(s) * act(C, s)
 return out / len(P)


def nrm(A):
 return float(np.linalg.norm(np.asarray(A, dtype=float).ravel()))


def altres(C, s):
 """How far f falls short of f^s = (sgn s) f."""
 return nrm(act(C, s) - sgn(s) * C)


def is_alt(C, tol=1e-12):
 return all(altres(C, s) < tol for s in perms(C.ndim))


def is_sym(C, tol=1e-12):
 return all(nrm(act(C, s) - C) < tol for s in perms(C.ndim))


def nu(m, n, q):
 """The alternating tensor built from the representative q."""
 C = np.zeros((m,) * n)
 for s in perms(n):
  C[tuple(q[s[i]] for i in range(n))] += sgn(s)
 return C


def reps(m, n):
 """C: the injective tuples whose entries increase."""
 return list(itertools.combinations(range(m), n))


def injective(m, n):
 return [p for p in itertools.product(range(m), repeat=n) if len(set(p)) == n]


def falling(m, n):
 """m (m - 1) ... (m - n + 1): zero as soon as n exceeds m, as it should be."""
 out = 1
 for k in range(n):
  out *= m - k
 return out


def nullity(m, n, full=False):
 """dim of the solution space of c(p) = sgn(s) c(p o s), by rank.

 Adjacent transpositions generate S_n and the condition is multiplicative in
 s, so imposing it on them is the whole condition; `full` runs the entire
 group instead, which is what pins that claim below."""
 idx = list(itertools.product(range(m), repeat=n))
 pos = {p: k for k, p in enumerate(idx)}
 if full:
  gens = perms(n)
 else:
  gens = [tuple(range(k)) + (k + 1, k) + tuple(range(k + 2, n)) for k in range(n - 1)]
 rows = []
 for p in idx:
  for s in gens:
   r = np.zeros(len(idx))
   r[pos[p]] += 1.0
   r[pos[tuple(p[s[i]] for i in range(n))]] -= sgn(s)
   rows.append(r)
 if not rows:
  return len(idx)
 return len(idx) - int(np.linalg.matrix_rank(np.array(rows), tol=1e-9))


# ── the representation itself, before anything is read off it ─────────
# `act` permutes the axes of the coefficient array; the definition permutes the
# arguments. Everything below rests on those being the same thing, so it is
# checked rather than asserted in a comment.
_CHK = np.arange(1.0, 28.0).reshape(3, 3, 3) % 7.0 - 3.0
_X = np.array([[2.0, -1.0, 3.0], [1.0, 4.0, -2.0], [-3.0, 2.0, 1.0]])
assert all(abs(ev(act(_CHK, _s), _X) - ev(_CHK, _X[list(invp(_s))])) < 1e-12
           for _s in perms(3)), \
    "permuting the array's axes is the same map as permuting the functional's arguments"
assert all(sgn(_s) * sgn(_r) == sgn(tuple(_s[_r[i]] for i in range(3)))
           for _s in perms(3) for _r in perms(3)), \
    "sgn is multiplicative, which is what both proofs in this section turn on"

# ── beat 0: the two definitions, in the bilinear case ─────────────────
SYM2 = np.array([[2.0, 3.0], [3.0, -1.0]])
ALT2 = np.array([[0.0, 2.0], [-2.0, 0.0]])
XI2, ET2 = np.array([1.0, 2.0]), np.array([3.0, -1.0])
SV = (ev(SYM2, np.array([XI2, ET2])), ev(SYM2, np.array([ET2, XI2])))
AV = (ev(ALT2, np.array([XI2, ET2])), ev(ALT2, np.array([ET2, XI2])))
assert is_sym(SYM2) and not is_alt(SYM2), "the left example is symmetric and nothing else"
assert is_alt(ALT2) and not is_sym(ALT2), "the right example is alternating and nothing else"
assert all(ALT2[i, i] == 0.0 for i in range(2)), "an alternating matrix has a zero diagonal"
assert SV[0] == SV[1] and SV[0] != 0.0, "swapping the arguments leaves the symmetric value alone"
assert AV[0] == -AV[1] and AV[0] != 0.0, "and flips the sign of the alternating one"

# ── beat 1: a repeated argument kills an alternating functional ───────
VEC3 = np.array([[2.0, -1.0, 3.0], [1.0, 4.0, -2.0], [-3.0, 2.0, 1.0]])
ALT3 = nu(3, 3, (0, 1, 2))
assert is_alt(ALT3), "the tensor used in beats 1 and 10 really is alternating"
REPEAT = [(a, b, c, ev(ALT3, VEC3[[a, b, c]]))
          for a, b, c in ((0, 0, 1), (1, 0, 0), (0, 1, 0), (2, 2, 0))]
FULL3 = ev(ALT3, VEC3)
assert all(abs(v) < 1e-12 for _a, _b, _c, v in REPEAT), \
    "every tuple with a repeated vector is sent to zero"
assert abs(FULL3) > 1.0, "while three independent vectors are not: f is not the zero functional"

# ── beat 2: the operator ──────────────────────────────────────────────
FACT = [math.factorial(k) for k in range(1, 6)]
PERM3 = perms(3)
assert FACT == [1, 2, 6, 24, 120] and len(PERM3) == FACT[2], \
    "the sum defining Omega runs over n! permutations"
assert sum(1 for s in PERM3 if sgn(s) > 0) == sum(1 for s in PERM3 if sgn(s) < 0), \
    "half the terms of that sum enter with a plus and half with a minus"

# ── beats 3 and 4: Omega is a projection, and lemma 5.1 ───────────────
FEX = np.zeros((4, 4, 4))
for _idx, _v in {(0, 1, 2): 3.0, (1, 0, 2): 1.0, (0, 2, 3): -2.0, (3, 1, 0): 2.0,
                 (1, 1, 2): 1.0, (2, 0, 1): -1.0, (2, 3, 0): 2.0, (0, 0, 0): 1.0}.items():
 FEX[_idx] = _v
FEX = FEX + nu(4, 3, (0, 1, 3))
OFEX = omega(FEX)
NF, NOF = nrm(FEX), nrm(OFEX)
PROJ = [(s, sgn(s), altres(FEX, s), altres(OFEX, s)) for s in PERM3]
IDEM = nrm(omega(OFEX) - OFEX)
assert not is_sym(FEX) and not is_alt(FEX), \
    "the test tensor is neither symmetric nor alternating, so there is something to project"
assert all(r < 1e-12 for _s, _g, _a, r in PROJ), \
    "Omega f passes the alternating test for every one of the six permutations"
assert any(a > 1.0 for _s, _g, a, _r in PROJ), "which f itself does not"
assert IDEM < 1e-12, "and projecting twice changes nothing: Omega is idempotent"
assert NOF > 0.5, "Omega f is not the zero tensor, so the projection has a non-trivial image"
assert nrm(OFEX - FEX) > 1.0, "but it is not f either, so the projection is not the identity"
LEMMA = [(r, sgn(r), nrm(omega(act(FEX, r)) - sgn(r) * OFEX),
          nrm(omega(act(FEX, r)) - OFEX)) for r in PERM3]
assert all(g < 1e-12 for _r, _s, g, _b in LEMMA), \
    "lemma 5.1 holds for every rho: permuting first costs exactly the sign of rho"
assert all(b > 1.0 for _r, s, _g, b in LEMMA if s < 0), \
    "and dropping that sign breaks it on every odd rho, so the sign is not decoration"

# ── beat 5: the condition on the coefficients ─────────────────────────
C12, C13, C23 = 2.0, -3.0, 5.0
COEF32 = np.array([[0.0, C12, C13], [-C12, 0.0, C23], [-C13, -C23, 0.0]])
assert is_alt(COEF32), "the nine coefficients drawn on the left come from an alternating tensor"
assert max(abs(COEF32[p] - sgn(s) * COEF32[tuple(p[s[i]] for i in range(2))])
           for p in itertools.product(range(3), repeat=2) for s in perms(2)) < 1e-12, \
    "c(p) = sgn(s) c(p o s) holds for all nine p and both permutations"
assert all(COEF32[i, i] == 0.0 for i in range(3)), "so the diagonal coefficients vanish"

# ── beats 6 and 9: the dimension counts ───────────────────────────────
DIM3 = [(n, falling(3, n), len(reps(3, n)), nullity(3, n)) for n in range(1, 6)]
DIM4 = [(n, falling(4, n), len(reps(4, n)), nullity(4, n)) for n in range(0, 5)]
assert [d for _n, _f, _c, d in DIM3] == [3, 3, 1, 0, 0], \
    "over a three-dimensional V the dimensions are 3, 3, 1, 0, 0 as n runs from 1 to 5"
assert [d for _n, _f, _c, d in DIM4] == [1, 4, 6, 4, 1], \
    "and over a four-dimensional one they are the fourth row of Pascal's triangle"
assert all(c == d == math.comb(m, n) for m, tab in ((3, DIM3), (4, DIM4))
           for n, _f, c, d in tab), \
    "enumerating representatives, the binomial formula and the rank all agree"
assert all(len(reps(m, n)) == math.comb(m, n)
           for m in range(2, 6) for n in range(0, m + 1)), \
    "theorem 5.2 verified by enumeration for every m from 2 to 5 and every n up to m"
assert all(len(reps(m, n)) == 0 and len(injective(m, n)) == 0
           for m in range(2, 6) for n in range(m + 1, m + 3)), \
    "and past n = m there is no injective tuple at all, so the space is zero"
assert nullity(3, 3, full=True) == nullity(3, 3) == 1, \
    "the adjacent-transposition shortcut gives the same rank as the whole group"
assert nullity(4, 2, full=True) == nullity(4, 2) == 6, "the same on a second case"
assert sum(math.comb(4, n) for n in range(5)) == 2 ** 4, \
    "the row of binomial coefficients sums to 2^m, which is what Pascal's triangle says"
PASCAL = [[math.comb(r, k) for k in range(r + 1)] for r in range(6)]
assert PASCAL[4] == [c for _n, _f, c, _d in DIM4], \
    "and the highlighted row is the one the right-hand table is counting"

# ── beats 7 and 8: representatives and the basis ──────────────────────
M7, N7 = 4, 2
REP7 = reps(M7, N7)
ORD7 = [(q, [tuple(q[s[i]] for i in range(N7)) for s in perms(N7)]) for q in REP7]
INJ7 = injective(M7, N7)
assert len(INJ7) == falling(M7, N7) == len(REP7) * math.factorial(N7), \
    "the injective tuples split into |C| classes of n! each"
assert sorted(p for _q, ps in ORD7 for p in ps) == sorted(INJ7), \
    "and those classes between them are exactly the injective tuples, each once"
NU7 = {q: nu(M7, N7, q) for q in REP7}
assert all(is_alt(v) for v in NU7.values()), "every nu(q) is alternating"
for _q in REP7:
 _mu = np.zeros((M7,) * N7)
 _mu[_q] = 1.0
 assert nrm(NU7[_q] - math.factorial(N7) * omega(_mu)) < 1e-12, \
     "nu(q) is n! times the projection of mu(q), which is why it is alternating"
EVAL7 = np.array([[NU7[q][p] for p in REP7] for q in REP7])
assert np.array_equal(EVAL7, np.eye(len(REP7))), \
    "nu(q) is 1 on its own representative and 0 on the others, so the family is independent"
RNDA = np.zeros((M7,) * N7)
for _k, _q in enumerate(REP7):
 RNDA += (_k - 2) * NU7[_q]
EXPRES = nrm(sum(RNDA[q] * NU7[q] for q in REP7) - RNDA)
assert is_alt(RNDA) and EXPRES < 1e-12, \
    "and an alternating tensor is recovered from its coefficients at the representatives"
assert np.linalg.matrix_rank(EVAL7) == len(REP7) == nullity(M7, N7), \
    "so the family spans as well as being independent: it is a basis"

# ── beat 10: n = m, and the determinant hiding in the expansion ───────
assert len(reps(3, 3)) == 1 and nullity(3, 3) == 1, \
    "when n = m there is one representative, so the alternating space is a line"
assert ALT3[0, 1, 2] == 1.0, "normalising its generator to 1 on the standard basis"
TERMS = []
for _s in PERM3:
 _pr = 1.0
 for _i in range(3):
  _pr *= VEC3[_i, _s[_i]]
 TERMS.append((_s, sgn(_s), _pr))
LEIB = sum(g * pr for _s, g, pr in TERMS)
NPDET = float(np.linalg.det(VEC3))
DETERR = abs(LEIB - NPDET)
assert DETERR < 1e-12, \
    "the signed sum of the last display on p. 312 is numpy's determinant: next episode's premise"
assert abs(ev(ALT3, VEC3) - NPDET) < 1e-12, \
    "and the alternating tensor evaluates to the same number, so they are the same functional"
assert len({pr for _s, _g, pr in TERMS}) == len(TERMS), \
    "the six products drawn on screen are six different numbers, not a repeated one"
HOT = PERM3[4]
assert sgn(HOT) > 0 and tuple(i + 1 for i in HOT) == (3, 1, 2), \
    "the term picked out in the left figure is the one printed in orange on the right"
RANK7 = int(np.linalg.matrix_rank(EVAL7))
DIMB7 = DIM4[N7][3]
assert RANK7 == DIMB7 == math.comb(M7, N7), \
    "the rank of the evaluation matrix, the rank of the linear system and C(4, 2) are one number"


def pstr(s):
 return " ".join(str(i + 1) for i in s)


def ival(v):
 return str(int(round(v))).replace("-", "\u2212")


def sval(v):
 return "0" if abs(v) < 1e-12 else f"{v:+.0f}".replace("-", "\u2212")


class AdvCalcE87Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 87

 MODE_LABEL = {
  0: {"zh": "兩個定義：對稱與交錯",
      "en": "two definitions: symmetric and alternating"},
  1: {"zh": "交錯：變數有重複就是零",
      "en": "alternating: a repeated argument gives zero"},
  2: {"zh": "投影算子 Ω",
      "en": "the projection operator"},
  3: {"zh": "定理 5.1：它真的是投影",
      "en": "theorem 5.1: it really is a projection"},
  4: {"zh": "引理 5.1：先重排再投影",
      "en": "lemma 5.1: permute first, then project"},
  5: {"zh": "把交錯翻譯成係數的條件",
      "en": "alternating, as a condition on the coefficients"},
  6: {"zh": "兩個後果：重複為零，n 大於 m 時全零",
      "en": "two consequences: repeats vanish, and nothing survives past m"},
  7: {"zh": "n 不超過 m 時怎麼數",
      "en": "counting when n does not exceed m"},
  8: {"zh": "代表元造出來的那組基底",
      "en": "the basis the representatives build"},
  9: {"zh": "定理 5.2：維數就是組合數",
      "en": "theorem 5.2: the dimension is the binomial coefficient"},
  10: {"zh": "n = m：維數是 1，而那就是行列式",
       "en": "n equal to m: dimension one, and that is the determinant"},
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

 def _between(self, p, q, color, inset=0.19, n=5, sw=1.6, bow=0.0):
  """A dashed connector between two grid cells, pulled back from both centres.

  Drawing straight from one cell centre to another puts the line through the
  digits in those cells, which is what collide reports as `Line through '0'`.
  The two ends are inset so the connector lives in the gap between cells."""
  import numpy as _np
  a_, b_ = _np.asarray(p, dtype=float), _np.asarray(q, dtype=float)
  d = b_ - a_
  L = float(_np.linalg.norm(d))
  if L <= 2.2 * inset:
   return VGroup()
  u = d / L
  if not bow:
   return self._dash(a_ + inset * u, b_ - inset * u, color, n=n, sw=sw)
  # A straight run between two cells two apart passes through the cell in
  # between -- on the anti-diagonal that is the zero on the main diagonal. Bow
  # the connector around it instead of through it.
  perp = _np.array([-u[1], u[0], 0.0])
  mid = 0.5 * (a_ + b_) + bow * perp
  return VGroup(self._dash(a_ + inset * u, mid, color, n=max(3, n // 2), sw=sw),
                self._dash(mid, b_ - inset * u, color, n=max(3, n // 2), sw=sw))

 def _loop(self, cx, cy, r, color, sw=2.2, n=56):
  """A self-arrow: a circle hanging below the point at its top, with a head.

  Clearing `_arr`'s 0.05 chord threshold is not enough. manim also clamps the
  head by `max_tip_length_to_length_ratio=0.34`, so a 0.068 chord gets a head of
  0.023 -- about three pixels at 1080p, which is no head at all. The head is cut
  from the last forty-five degrees, giving a chord near 0.2 and a head near 0.07."""
  a0, a1 = math.radians(96.0), math.radians(96.0 + 348.0)
  pt = lambda a: [cx + r * math.cos(a), cy + r * math.sin(a), 0]
  g = VGroup(self._curve([pt(a0 + (a1 - a0) * k / n) for k in range(n + 1)], color, sw=sw))
  return g.add(self._arr(pt(a1 - math.radians(45.0)), pt(a1), color, sw=sw + 1, tl=0.11))

 # ── beat 0: symmetric and alternating, side by side ─────────────
 def _defs(self):
  g = VGroup()
  for cx, mat, col, head in ((-5.05, SYM2, ACCENT_B, "t ᵢ ⱼ   =   t ⱼ ᵢ"),
                             (-3.35, ALT2, ACCENT_A, "t ᵢ ⱼ   =   − t ⱼ ᵢ")):
   grid, pos = self._numgrid(cx, 0.44, [[ival(v) for v in row] for row in mat],
                             dx=0.50, dy=0.40, size=FS_TAG - 2, color=col)
   g.add(grid)
   # the mirror the condition is about: both grids get it, but one is
   # unchanged across it and the other changes sign, which is the whole point
   g.add(self._between(pos(0, 0), pos(1, 1), DIM, n=5, sw=1.4))
   g.add(self._sym(1.08, head, col, FS_TAG - 2, x=cx, w=1.56))
  for k, (col, vals) in enumerate(((ACCENT_B, SV), (ACCENT_A, AV))):
   cx = -5.05 + 1.70 * k
   g.add(self._sym(-0.28, f"f ( ξ , η )  =  {ival(vals[0])}", col, FS_TAG - 4, x=cx, w=1.60),
         self._sym(-0.58, f"f ( η , ξ )  =  {ival(vals[1])}", col, FS_TAG - 4, x=cx, w=1.60))
  g.add(self._table((("f ( ξ ∘ σ ⁻ ¹ )   =   f ( ξ )", ACCENT_B),
                     ("f ( ξ ∘ σ ⁻ ¹ )   =   ( sgn σ )  f ( ξ )", ACCENT_A),
                     ("n  =  2        f ( ξ , η )   =   Σ t ᵢ ⱼ  x ᵢ  y ⱼ", DIM),
                     ("ξ  =  ⟨ 1 , 2 ⟩            η  =  ⟨ 3 , − 1 ⟩", DIM),
                     (f"t ᵢ ⱼ  =  t ⱼ ᵢ          {ival(SV[0])}          {ival(SV[1])}",
                      ACCENT_B),
                     (f"t ᵢ ⱼ  =  − t ⱼ ᵢ        {ival(AV[0])}        {ival(AV[1])}",
                      ACCENT_A)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("左邊翻過虛線不變，右邊變號",
                  "the left grid survives the dashed mirror; the right one flips sign"))
  return g.add(self._foot("這一節只做兩件事：寫清楚對稱與交錯，然後算出交錯那個子空間的維數",
                          "the section does two things: it says what symmetric and alternating mean, then computes the dimension of the alternating subspace",
                          ACCENT_A,
                          "對稱是把變數照任何一個置換重排值都不變，交錯是值會乘上那個置換的正負號。雙線性的情形就是交換兩個變數之後值不變、或者變號",
                          "symmetric means the value survives any permutation of the arguments and alternating means it picks up that permutation's sign; for two arguments it is simply whether swapping them keeps the value or flips it"))

 # ── beat 1: a repeat sends the value to zero ────────────────────
 def _repeat(self):
  oy = 0.50
  g = VGroup()
  for x0, lab, col in ((-5.25, "ξ", ACCENT_A), (-4.20, "ξ", ACCENT_A), (-3.15, "η", ACCENT_B)):
   g.add(self._box(x0, oy, lab, col, w=0.76, h=0.52, size=FS_TAG + 2))
  g.add(self._arr([-5.25, 1.14, 0], [-4.20, 1.14, 0], WARN, sw=3, tl=0.12),
        self._arr([-4.20, 0.96, 0], [-5.25, 0.96, 0], WARN, sw=3, tl=0.12))
  g.add(self._sym(1.05, "τ", WARN, FS_TAG - 2, x=-5.72, w=0.32))
  for y, s in ((0.04, "f ( ξ , ξ , η )   =   − f ( ξ , ξ , η )"),
               (-0.30, "2  f ( ξ , ξ , η )   =   0"),
               (-0.64, "f ( ξ , ξ , η )   =   0")):
   g.add(self._sym(y, s, ACCENT_A if y < -0.1 else INK, FS_TAG - 2, x=-4.20, w=3.30))
  g.add(self._table((("n  =  3        m  =  3        c ( p )  =  sgn p", ACCENT_A),
                     ("ξ  =  ⟨ 2 , − 1 , 3 ⟩", DIM),
                     ("η  =  ⟨ 1 , 4 , − 2 ⟩", DIM),
                     ("ζ  =  ⟨ − 3 , 2 , 1 ⟩", DIM),
                     (f"f ( ξ , ξ , η )  =  {ival(REPEAT[0][3])}"
                      f"        f ( η , ξ , ξ )  =  {ival(REPEAT[1][3])}", ACCENT_B),
                     (f"f ( ξ , η , ξ )  =  {ival(REPEAT[2][3])}"
                      f"        f ( ζ , ζ , ξ )  =  {ival(REPEAT[3][3])}", ACCENT_B),
                     (f"f ( ξ , η , ζ )   =   {ival(FULL3)}", WARN)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("最後一列不是零，這個泛函不是零",
                  "the last row is not zero, so this functional is not either"))
  return g.add(self._foot("交錯有一個立刻看得出來的後果：只要兩個變數相同，值一定是零",
                          "alternating has one consequence you see at once: if two arguments are equal the value is zero",
                          ACCENT_A,
                          "把那兩個相同的變數對換，一方面什麼都沒動、值不變，另一方面按定義要乘上負一。於是那個值等於它自己的相反數，只能是零",
                          "swap the two equal arguments: nothing has moved so the value is unchanged, yet the definition demands a change of sign, so the value is its own negative and must vanish"))

 # ── beat 2: the operator and its n! terms ───────────────────────
 def _oper(self):
  oy = 0.74
  g = VGroup(self._box(-5.00, oy, "( V * ) ⊗ ⁿ", ACCENT_C, w=1.64, h=0.56, size=FS_TAG),
             self._box(-3.10, oy, "𝒜 ⁿ", ACCENT_A, w=0.94, h=0.56, size=FS_TAG + 1))
  g.add(self._arr([-4.12, oy, 0], [-3.63, oy, 0], ACCENT_B, sw=3, tl=0.12))
  g.add(self._sym(oy + 0.32, "Ω", ACCENT_B, FS_TAG, x=-3.88, w=0.34))
  g.add(self._sym(0.30, f"n  =  3        n !  =  {FACT[2]}", DIM, FS_TAG - 3, x=-4.20, w=2.00))
  for k, s in enumerate(PERM3):
   col = ACCENT_B if sgn(s) > 0 else WARN
   g.add(self._sym(-0.06 - 0.32 * (k % 3), f"{'+' if sgn(s) > 0 else '−'}   ( {pstr(s)} )",
                   col, FS_TAG - 3, x=-5.10 + 1.74 * (k // 3), w=1.40))
  g.add(self._table((("( Ω f ) ( ξ )   =   ( 1 / n ! )  Σ  ( sgn σ )  f ( ξ ∘ σ ⁻ ¹ )", ACCENT_A),
                     ("σ  ∈  S ₙ                | S ₙ |   =   n !", DIM),
                     ("        n       " + "".join(f"{v:>7}" for v in range(1, 6)), DIM),
                     ("      n !       " + "".join(f"{v:>7}" for v in FACT), ACCENT_B),
                     ("Ω  :  ( V * ) ⊗ ⁿ    →    𝒜 ⁿ", ACCENT_C),
                     (f"n  =  3        m  =  4        ‖ f ‖  =  {NF:.3f}", DIM)),
                    y0=0.90, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("六個置換三個加號、三個減號",
                  "three of the six permutations enter with a plus, three with a minus"))
  return g.add(self._foot("對稱的全體與交錯的全體都是子空間，而交錯那一個是後面整章要用的",
                          "the symmetric tensors and the alternating ones are both subspaces, and the alternating one is what the rest of the chapter needs",
                          ACCENT_A,
                          "更好的是有一個線性算子可以把任意一個共變張量壓成交錯的：把它在每一個置換底下的樣子乘上那個置換的正負號，全部加起來，再除以 n 階乘",
                          "better still, one linear operator flattens any covariant tensor into an alternating one: weight each permuted copy by the sign of its permutation, add them, and divide by n factorial"))

 # ── beat 3: theorem 5.1, drawn as a projection ──────────────────
 def _proj(self):
  ly, fx, fy = -0.27, -4.90, 0.78
  g = VGroup(Line([-5.72, ly, 0], [-2.68, ly, 0], color=ACCENT_A, stroke_width=2.2))
  g.add(Dot([fx, fy, 0], radius=0.075, color=ACCENT_C),
        Dot([fx, ly, 0], radius=0.075, color=ACCENT_A))
  g.add(self._arr([fx, fy - 0.09, 0], [fx, ly + 0.09, 0], ACCENT_B, sw=3, tl=0.13))
  g.add(self._sym(fy, "f", ACCENT_C, FS_TAG, x=fx - 0.30, w=0.26),
        self._sym(0.28, "Ω", ACCENT_B, FS_TAG - 1, x=fx + 0.30, w=0.30),
        self._sym(ly + 0.15, "Ω f", ACCENT_A, FS_TAG - 2, x=fx + 0.52, w=0.72),
        self._sym(ly - 0.52, "𝒜 ⁿ", ACCENT_A, FS_TAG - 2, x=-2.95, w=0.60))
  g.add(self._loop(fx, ly - 0.26, 0.26, ACCENT_B))
  g.add(self._sym(ly - 0.26, "Ω", ACCENT_B, FS_TAG - 3, x=fx, w=0.26))
  g.add(self._sym(fy, f"‖ f ‖   =   {NF:.3f}", ACCENT_C, FS_TAG - 3, x=-3.84, w=1.58))
  # 原本 x=-3.45，左緣正好貼著上一個 "Ω f" 的右緣，兩個標籤讀起來連成一串
  g.add(self._sym(ly + 0.15, f"‖ Ω f ‖   =   {NOF:.3f}", ACCENT_A, FS_TAG - 3,
                  x=-3.15, w=1.56))
  g.add(self._sym(-0.98, f"Ω ( Ω f )   −   Ω f   =   {IDEM:.1e}", ACCENT_B,
                  FS_TAG - 3, x=-4.60, w=2.60))
  g.add(self._sym(1.12, "f   ∉   𝒜 ⁿ", ACCENT_C, FS_TAG - 2, x=-4.20, w=1.40))
  # two header lines, not one long one: a single row naming both residuals in
  # full would be wider than the panel, and `_sym` shrinks each row on its own,
  # so a shrunk heading no longer sits over the columns it names
  g.add(self._table((("‖ g ( · ∘ σ )   −   ( sgn σ )  g ‖", DIM),
                     ("      σ        sgn σ        g = f        g = Ω f", DIM))
                    + tuple((f"    {pstr(s)}        {gg:+d}        {a:8.3f}      {r:.1e}",
                             DIM if k == 0 else ACCENT_B)
                            for k, (s, gg, a, r) in enumerate(PROJ)),
                    y0=0.90, dy=0.21, size=FS_TAG - 5))
  g.add(self._cap("表頭下第一列是恆等置換，兩欄都是零",
                  "the first row under the heading is the identity, zero in both columns"))
  return g.add(self._foot("定理 5.1 說這個算子真的是投影。第一件事：它的像一定是交錯的",
                          "theorem 5.1 says the operator really is a projection; first, its image is always alternating",
                          ACCENT_A,
                          "證明用正負號的乘法性，加上固定一個置換之後複合是雙射這個小事實。第二件事：本來就交錯的東西原封不動送回來，因為那時每一項都等於原來那個泛函",
                          "that needs the sign to be multiplicative and composition with a fixed permutation to be a bijection; second, an already alternating tensor comes back untouched, because then every one of the terms is the original"))

 # ── beat 4: lemma 5.1, as a square ──────────────────────────────
 def _lemma(self):
  ty, by = 0.72, -0.28
  g = VGroup(self._box(-5.20, ty, "f", ACCENT_C, w=0.92, h=0.52, size=FS_TAG + 2),
             self._box(-3.30, ty, "g", ACCENT_B, w=0.92, h=0.52, size=FS_TAG + 2),
             self._box(-5.20, by, "Ω f", ACCENT_A, w=1.08, h=0.52, size=FS_TAG + 1),
             self._box(-3.30, by, "Ω g", ACCENT_A, w=1.08, h=0.52, size=FS_TAG + 1))
  g.add(self._arr([-4.68, ty, 0], [-3.82, ty, 0], DIM, sw=3, tl=0.12),
        self._arr([-4.60, by, 0], [-3.90, by, 0], WARN, sw=3, tl=0.12),
        self._arr([-5.20, ty - 0.30, 0], [-5.20, by + 0.30, 0], ACCENT_B, sw=3, tl=0.12),
        self._arr([-3.30, ty - 0.30, 0], [-3.30, by + 0.30, 0], ACCENT_B, sw=3, tl=0.12))
  g.add(self._sym(ty + 0.32, "·  ∘  ρ", DIM, FS_TAG - 2, x=-4.25, w=0.92),
        self._sym(by - 0.34, "×  ( sgn ρ )", WARN, FS_TAG - 2, x=-4.25, w=1.26),
        self._sym(0.22, "Ω", ACCENT_B, FS_TAG - 2, x=-5.52, w=0.30),
        self._sym(0.22, "Ω", ACCENT_B, FS_TAG - 2, x=-2.98, w=0.30))
  g.add(self._sym(-0.94, "g ( ξ )   =   f ( ξ ∘ ρ )", ACCENT_B, FS_TAG - 2, x=-4.20, w=2.40))
  g.add(self._table((("  ρ    sgn ρ    ‖ Ω g − ( sgn ρ ) Ω f ‖    ‖ Ω g − Ω f ‖", DIM),)
                    + tuple((f"  {pstr(r)}      {gg:+d}            {good:.1e}"
                             f"               {bad:8.3f}",
                             ACCENT_B if gg > 0 else ACCENT_C)
                            for r, gg, good, bad in LEMMA)
                    + (("sgn ρ  =  + 1      ⇒      Ω g   =   Ω f", ACCENT_A),),
                    y0=0.90, dy=0.23, size=FS_TAG - 5))
  g.add(self._cap("右欄三個奇置換不是零，正負號不能省",
                  "the right column is nonzero on the three odd rows: the sign cannot be dropped"))
  return g.add(self._foot("引理 5.1 是同一個計算的小變形：先用一個置換重排變數再投影，等於先投影再乘上那個置換的正負號",
                          "lemma 5.1 is a small variant of the same computation: permuting the arguments and then projecting equals projecting and then multiplying by that permutation's sign",
                          ACCENT_A,
                          "證明與上面那一段一字不差，只要把和式裡的指標換個名字。這一條在下一拍把係數的條件推出來的時候就會用到",
                          "the proof is word for word the one above with the summation index renamed, and the next beat needs it to turn the definition into a condition on the coefficients"))

 # ── beat 5: the nine coefficients ───────────────────────────────
 def _coef(self):
  grid, pos = self._numgrid(-4.65, 0.40, [[sval(v) for v in row] for row in COEF32],
                            dx=0.58, dy=0.42, size=FS_TAG - 2, color=INK,
                            hot=((0, 0), (1, 1), (2, 2)), hotcolor=WARN)
  g = VGroup(grid)
  for j in range(3):
   g.add(self._sym(pos(0, j)[1] + 0.34, str(j + 1), DIM, FS_TAG - 5, x=pos(0, j)[0], w=0.26))
   g.add(self._sym(pos(j, 0)[1], str(j + 1), DIM, FS_TAG - 5, x=pos(j, 0)[0] - 0.54, w=0.26))
  for (a, b), col in ((((0, 1), (1, 0)), ACCENT_B), (((0, 2), (2, 0)), ACCENT_C),
                      (((1, 2), (2, 1)), ACCENT_A)):
   # the anti-diagonal pair has the centre cell in its way, so it gets bowed
   bow = 0.26 if (a, b) == ((0, 2), (2, 0)) else 0.0
   g.add(self._between(pos(*a), pos(*b), col, n=5, sw=1.8, bow=bow))
  g.add(self._sym(-0.44, "c ( i , j )   =   f ( α ᵢ , α ⱼ )", INK, FS_TAG - 2, x=-4.65, w=2.80))
  g.add(self._sym(-0.78, "c ( 1 , 1 )  =  c ( 2 , 2 )  =  c ( 3 , 3 )  =  0", WARN,
                  FS_TAG - 3, x=-4.65, w=3.20))
  g.add(self._table((("f  ∈  𝒜 ⁿ      ⟺      c ( p )  =  ( sgn σ )  c ( p ∘ σ )", ACCENT_A),
                     ("m  =  3        n  =  2        m ⁿ  =  9", DIM),
                     ("c ( i , j )   =   − c ( j , i )", DIM),
                     (f"c ( 1 , 2 )  =  {sval(C12)}        c ( 2 , 1 )  =  {sval(-C12)}",
                      ACCENT_B),
                     (f"c ( 1 , 3 )  =  {sval(C13)}        c ( 3 , 1 )  =  {sval(-C13)}",
                      ACCENT_C),
                     (f"c ( 2 , 3 )  =  {sval(C23)}        c ( 3 , 2 )  =  {sval(-C23)}",
                      ACCENT_A),
                     (f"dim 𝒜 ⁿ  =  {DIM3[1][3]}        C ( 3 , 2 )  =  {math.comb(3, 2)}",
                      ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("對角線上紅的三格是零，虛線各連一對",
                  "the three red diagonal cells vanish; each dashed line joins one pair"))
  return g.add(self._foot("把交錯翻譯成係數的語言：共變張量由它在基底組合上的係數完全決定",
                          "translate alternating into the language of coefficients: a covariant tensor is fixed by its values on tuples of basis vectors",
                          ACCENT_A,
                          "交錯這個條件就等價於把指標依任何一個置換重排，係數就乘上那個置換的正負號。對角線上那三個必須是零，其餘六個兩兩差一個負號",
                          "alternating is exactly the condition that permuting the indices multiplies the coefficient by the sign, so the three on the diagonal have to vanish and the other six pair off"))

 # ── beat 6: the two things that die ─────────────────────────────
 def _vanish(self):
  g = VGroup()
  # the two notes sit clear of the fourth source dot at x = -3.60: the lower
  # one is deliberately the shorter of the pair, because the slanted arrow
  # below it runs out to x = -3.60 at the height the text would occupy
  for sy, ty, src, tgt, pmap, note, nw in ((1.02, 0.50, 3, 3, (0, 1, 1),
                                            "p  =  ⟨ 1 , 2 , 2 ⟩", 1.40),
                                           (-0.20, -0.72, 4, 3, (0, 1, 2, 1),
                                            "4  >  3", 0.78)):
   xs = [-5.40 + 0.60 * k for k in range(src)]
   xt = [-5.40 + 0.60 * k for k in range(tgt)]
   seen = {}
   for i, j in enumerate(pmap):
    seen.setdefault(j, []).append(i)
   for i, j in enumerate(pmap):
    col = WARN if len(seen[j]) > 1 else DIM
    g.add(self._arr([xs[i], sy - 0.08, 0], [xt[j], ty + 0.08, 0], col, sw=3, tl=0.11))
   for x in xs:
    g.add(Dot([x, sy, 0], radius=0.062, color=ACCENT_A))
   for k, x in enumerate(xt):
    col = WARN if len(seen.get(k, [])) > 1 else ACCENT_B
    g.add(Dot([x, ty, 0], radius=0.062, color=col))
    g.add(self._sym(ty - 0.24, str(k + 1), col, FS_TAG - 5, x=x, w=0.24))
   g.add(self._sym((sy + ty) / 2, note, WARN, FS_TAG - 4, x=-2.95, w=nw))
  g.add(self._table((("p ᵢ  =  p ⱼ   ,   i ≠ j      ⇒      c ( p )   =   0", ACCENT_A),
                     ("n  >  m        ⇒        𝒜 ⁿ   =   { 0 }", WARN),
                     ("m  =  3            n   " + "".join(f"{n:>5}" for n, *_ in DIM3), DIM),
                     ("m ⋯ ( m − n + 1 )      "
                      + "".join(f"{f:>5}" for _n, f, _c, _d in DIM3), ACCENT_B),
                     ("            | C |      "
                      + "".join(f"{c:>5}" for _n, _f, c, _d in DIM3), ACCENT_C),
                     ("        dim 𝒜 ⁿ      "
                      + "".join(f"{d:>5}" for _n, _f, _c, d in DIM3), ACCENT_A),
                     ("n  =  4 , 5        ⇒        | C |   =   0", DIM)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("上面是自己撞的，下面四個塞三個，一定撞",
                  "the upper map collides by choice; the lower one, four into three, cannot avoid it"))
  return g.add(self._foot("第一個後果：指標有重複時，拿對換那兩個位置的置換去套，係數等於它自己的相反數，所以是零",
                          "the first consequence: if an index repeats, apply the transposition swapping those two places and the coefficient is its own negative, hence zero",
                          ACCENT_A,
                          "第二個後果：n 比 m 大的時候根本不存在沒有重複的指標組，所以每一個係數都是零，那個子空間只剩下零",
                          "the second: once n exceeds m no tuple avoids a repeat at all, so every coefficient vanishes and the subspace is reduced to zero"))

 # ── beat 7: the injective tuples, sorted by range ───────────────
 def _count(self):
  g = VGroup()
  ys = [0.90 - 0.22 * k for k in range(M7)]
  for k, y in enumerate(ys):
   g.add(self._sym(y, str(k + 1), DIM, FS_TAG - 6, x=-5.84, w=0.22))
  for c, (q, ps) in enumerate(ORD7):
   x = -5.40 + 0.56 * c
   for k, y in enumerate(ys):
    if k in q:
     g.add(Dot([x, y, 0], radius=0.078, color=ACCENT_A))
    else:
     g.add(Dot([x, y, 0], radius=0.042, color=DIM))
   for r, p in enumerate(ps):
    g.add(self._sym(-0.02 - 0.24 * r, " ".join(str(i + 1) for i in p),
                    ACCENT_B, FS_TAG - 7, x=x, w=0.50))
  g.add(self._sym(1.16, f"| C |   =   {len(REP7)}", ACCENT_A, FS_TAG - 3, x=-4.00, w=1.20))
  g.add(self._sym(-0.58, f"n !   =   {math.factorial(N7)}", ACCENT_B, FS_TAG - 3,
                  x=-4.70, w=1.00),
        self._sym(-0.58, f"{len(REP7)}  ×  {math.factorial(N7)}   =   {len(INJ7)}",
                  ACCENT_C, FS_TAG - 3, x=-3.20, w=1.60))
  g.add(self._table((("n  ≤  m          p   =   q ∘ σ          σ  ∈  S ₙ", ACCENT_A),
                     ("q ₁  <  q ₂  <  ⋯  <  q ₙ", ACCENT_B),
                     ("m  =  4            n  =  2", DIM),
                     (f"m ( m − 1 ) ⋯ ( m − n + 1 )   =   {falling(M7, N7)}", ACCENT_C),
                     (f"| C |  ·  n !   =   {len(REP7)}  ·  {math.factorial(N7)}"
                      f"   =   {len(INJ7)}", ACCENT_B),
                     (f"| C |   =   {len(INJ7)}  /  {math.factorial(N7)}   =   {len(REP7)}",
                      ACCENT_A),
                     ("q   ⊂   { 1 , 2 , 3 , 4 }          | q |   =   2", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("六欄各兩個排法，一共十二個單射",
                  "each of the six columns carries two orderings: twelve injective tuples"))
  return g.add(self._foot("剩下 n 不超過 m 的情形。把所有單射的指標組按值域分類，值域相同的那一群彼此只差一個置換，每群恰好 n 階乘個",
                          "that leaves n at most m: sort the injective tuples by their range, and tuples with the same range differ by a permutation, so each class holds exactly n factorial of them",
                          ACCENT_A,
                          "每一群裡挑出把值域由小排到大的那一個當代表。於是代表元的集合，與從 m 個元素裡取 n 個的子集一一對應",
                          "take as representative the one whose range is listed in increasing order, and the representatives correspond one to one with the n element subsets"))

 # ── beat 8: the basis the representatives build ─────────────────
 def _basis(self):
  grid, _pos = self._numgrid(-4.20, 0.26, [[ival(v) for v in row] for row in EVAL7],
                             dx=0.42, dy=0.28, size=FS_TAG - 6, color=DIM,
                             hot=tuple((k, k) for k in range(len(REP7))), hotcolor=ACCENT_A)
  g = VGroup(grid)
  g.add(self._sym(-0.92, "[  ν ( q ) ( α ᵢ , α ⱼ )  ]          ⟨ i , j ⟩  ∈  C",
                  INK, FS_TAG - 3, x=-4.20, w=3.30))
  g.add(self._table((("ν ( q )   =   Σ  ( sgn σ )  μ ( q ∘ σ )        ( σ ∈ S ₙ )", ACCENT_A),
                     ("ν ( q )   =   n !  Ω ( μ ( q ) )        ⇒        ν ( q )  ∈  𝒜 ⁿ",
                      ACCENT_C),
                     ("m  =  4      n  =  2      ν ₁ ₂  =  μ ₁ ₂  −  μ ₂ ₁", ACCENT_B),
                     ("f   =   Σ  c ( q )  ν ( q )            ( q ∈ C )", ACCENT_A),
                     (f"‖ f  −  Σ c ( q ) ν ( q ) ‖   =   {EXPRES:.1e}", ACCENT_B),
                     (f"rank   =   {RANK7}            | C |   =   {len(REP7)}", ACCENT_C),
                     (f"dim 𝒜 ⁿ   =   {DIMB7}            C ( 4 , 2 )   =   "
                      f"{math.comb(4, 2)}", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("對角線是 1、其餘是 0，所以彼此獨立",
                  "the diagonal is one and the rest zero, so the six are independent"))
  return g.add(self._foot("對每個代表元造一個張量：把它在所有置換底下的基底元素乘上正負號加起來，那正好是 n 階乘倍的投影",
                          "each representative builds a tensor: add up its basis elements over all permutations weighted by the sign, which is n factorial times the projection",
                          ACCENT_A,
                          "所以它一定是交錯的。而任何一個交錯張量都能唯一寫成它們的線性組合，係數就是原來那些代表位置上的係數，所以這一族就是一組基底",
                          "so it is alternating, and every alternating tensor is uniquely a combination of them with the coefficients read straight off the representatives, which makes the family a basis"))

 # ── beat 9: theorem 5.2 ─────────────────────────────────────────
 def _dim(self):
  g = VGroup()
  for r, row in enumerate(PASCAL):
   y = 1.10 - 0.26 * r
   col = ACCENT_A if r == 4 else DIM
   g.add(self._sym(y, str(r), col, FS_TAG - 6, x=-5.70, w=0.24))
   for k, v in enumerate(row):
    g.add(self._sym(y, str(v), col, FS_TAG - 5, x=-4.20 + 0.42 * (k - r / 2.0), w=0.38))
  g.add(self._sym(-0.62, "C ( 4 , n )   =   " + " , ".join(str(v) for v in PASCAL[4]),
                  ACCENT_A, FS_TAG - 3, x=-4.20, w=3.20))
  g.add(self._sym(-0.94, f"Σ  C ( 4 , n )   =   {sum(PASCAL[4])}   =   2 ⁴",
                  DIM, FS_TAG - 3, x=-4.20, w=2.60))
  g.add(self._table((("dim 𝒜 ⁿ   =   C ( m , n )   =   m ! / ( n ! ( m − n ) ! )", ACCENT_A),
                     ("m  =  4            n   " + "".join(f"{n:>5}" for n, *_ in DIM4), DIM),
                     ("m ⋯ ( m − n + 1 )      "
                      + "".join(f"{f:>5}" for _n, f, _c, _d in DIM4), ACCENT_B),
                     ("            | C |      "
                      + "".join(f"{c:>5}" for _n, _f, c, _d in DIM4), ACCENT_C),
                     ("        dim 𝒜 ⁿ      "
                      + "".join(f"{d:>5}" for _n, _f, _c, d in DIM4), ACCENT_A),
                     (f"Σ  C ( 4 , n )   =   {sum(PASCAL[4])}   =   2 ⁴", DIM),
                     ("m  =  2 , 3 , 4 , 5      ⇒      | C |   =   C ( m , n )", DIM)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("上面那列數單射，下面兩列除以 n 階乘",
                  "the upper row counts injective tuples; the two below divide it by n factorial"))
  return g.add(self._foot("定理 5.2：交錯張量子空間的維數，就是從 m 個裡取 n 個的組合數",
                          "theorem 5.2: the dimension of the alternating subspace is the number of ways of choosing n things out of m",
                          ACCENT_A,
                          "算法是先數單射的個數，從 m 開始連乘 n 個遞減的因子，再除以每一群裡的 n 階乘。右表下面兩列用兩種完全不同的算法，得到同一組數字",
                          "count the injective tuples first, a product of n decreasing factors starting at m, then divide by the n factorial inside each class; the last two rows reach the same numbers two different ways"))

 # ── beat 10: n = m, and the determinant ─────────────────────────
 def _det(self):
  grid, pos = self._numgrid(-4.60, 0.40, [[ival(v) for v in row] for row in VEC3],
                            dx=0.60, dy=0.44, size=FS_TAG - 2, color=DIM,
                            hot=tuple((i, HOT[i]) for i in range(3)), hotcolor=ACCENT_A)
  g = VGroup(grid)
  for i in range(2):
   g.add(self._between(pos(i, HOT[i]), pos(i + 1, HOT[i + 1]), ACCENT_A, n=5, sw=1.8))
  g.add(self._sym(1.20, f"m  =  n  =  3          | C |  =  {len(reps(3, 3))}",
                  ACCENT_C, FS_TAG - 4, x=-4.20, w=2.60))
  g.add(self._sym(-0.56, "σ  =  ⟨ " + " , ".join(str(i + 1) for i in HOT) + " ⟩"
                         f"          sgn σ  =  {sgn(HOT):+d}",
                  ACCENT_A, FS_TAG - 3, x=-4.60, w=2.90))
  # the product is spelled out from HOT, so the cells highlighted above and the
  # factors named here cannot drift apart
  g.add(self._sym(-0.88, "  ".join(f"x ( {i + 1} , {HOT[i] + 1} )" for i in range(3))
                         + f"   =   {ival(dict((s, pr) for s, _g, pr in TERMS)[HOT])}",
                  ACCENT_A, FS_TAG - 3, x=-4.60, w=3.10))
  g.add(self._table((("      σ        sgn σ        ∏  x ( i , σ ( i ) )"
                      "        sgn  ·  ∏", DIM),)
                    + tuple((f"    {pstr(s)}        {gg:+d}"
                             f"            {ival(pr):>5}"
                             f"            {ival(gg * pr):>5}",
                             ACCENT_A if s == HOT else ACCENT_B)
                            for s, gg, pr in TERMS)
                    + ((f"Σ  =  {ival(LEIB)}        det  =  {NPDET:.6f}"
                        f"        Δ  =  {DETERR:.1e}", ACCENT_C),),
                    y0=0.90, dy=0.21, size=FS_TAG - 5))
  g.add(self._cap("橘色那三格就是右表橘色那一項",
                  "the three orange cells are the term printed in orange on the right"))
  return g.add(self._foot("最後是 n 等於 m 這個特例：代表元只剩一個，維數就是一",
                          "last comes the case n equal to m, where a single representative is left and the dimension is one",
                          ACCENT_A,
                          "把係數調成一，展開式就是對所有置換求和，每一項是正負號乘上一串座標的乘積，每個變數各出一個、行與列都不重複。書上說這本質上就是行列式的公式，下一集就把它認出來",
                          "set the coefficient to one and the expansion is a sum over all permutations of a sign times a product of coordinates, one from every row and every column; the book calls this essentially the formula for the determinant, which is next episode's starting point"))

 def stage(self):
  a, b, c = self._defs(), self._repeat(), self._oper()
  d, e, f_ = self._proj(), self._lemma(), self._coef()
  h, i, j = self._vanish(), self._count(), self._basis()
  k, l = self._dim(), self._det()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE87ZH, AdvCalcE87EN = make(AdvCalcE87Base, "87", prefix="AdvCalcE")
