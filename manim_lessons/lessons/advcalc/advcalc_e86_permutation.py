"""advcalc E86 -- chapter 7, sections 3 and 4 (book pp. 308-310): permutations,
and the sign of a permutation.

Sections 3 and 4 are one episode because they are one argument.  Section 3 is
pure group theory on a finite set -- closure, inverses, identity, the count
n factorial, the right translation that will later reindex a sum -- and it ends
by letting a permutation act on a multilinear functional.  Section 4 then takes
that action, applies it to one particular polynomial, and reads off a sign.
Neither half is worth an episode alone; together they are exactly what chapter 7
needs, because "alternating" is defined by that sign and the determinant turns
out to be the only alternating m-fold form.

Two things in the book look like typography and are really the whole content.
The first is the inverse in f(xi o sigma^-1): with sigma itself the composition
rule comes out in the other order, so Lemma 3.1 fails for exactly the pairs that
do not commute -- beat 4 computes both and prints how many fail.  The second is
the word "anti" in Theorem 3.1.  T carries the product in reverse order, and the
only way to put that on screen is to compute the wrong order too: beat 5 shows
both routes ending at different functionals and gives the size of the gap.  To
keep the superscript readable the action is written as a right action, f dot
sigma, which is also the honest reason for the reversal: a right action composed
with left-acting operators reverses.

Everything is enumerated with itertools.permutations -- there is no hard-coded
table anywhere.  The group axioms are checked over all 576 pairs and all 13824
triples of S4; every one of the 24 elements of S4 is factored into
transpositions and rebuilt; all decompositions of length at most 5 are found by
breadth-first search, which is what makes the parity claim a statement about
every factorisation rather than about the one the algorithm happened to
produce.  The action on functionals is carried both as a coefficient array and
as a function on triples of vectors, and the two agree, so the array identities
are identities about the functional.  The sign is the inversion count, and the
polynomial identity E(x o sigma) = sgn(sigma) E(x) is verified on all of S4
rather than asserted from it.
"""
import math
import pathlib, sys
from itertools import permutations, product

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


# ── permutations, as 0-based tuples of images ─────────────────────────
def comp(r, s):
 """(r o s)(i) = r(s(i))."""
 return tuple(r[s[i]] for i in range(len(s)))


def pinv(s):
 out = [0] * len(s)
 for i, v in enumerate(s):
  out[v] = i
 return tuple(out)


def tau(n, i, j):
 return tuple(j if k == i else i if k == j else k for k in range(n))


def inversions(s):
 return sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])


def sgn(s):
 return -1 if inversions(s) % 2 else 1


def show(s):
 """A permutation as the list of its images, one-based."""
 return " , ".join(str(v + 1) for v in s)


def flat(s):
 return " ".join(str(v + 1) for v in s)


S3 = list(permutations(range(3)))
S4 = list(permutations(range(4)))
ID3, ID4 = tuple(range(3)), tuple(range(4))
TR4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]

# ── beat 0: the four group axioms, by enumeration ─────────────────────
SET4 = set(S4)
NCLOSE = sum(1 for a in S4 for b in S4 if comp(a, b) in SET4)
NINVER = sum(1 for s in S4 if comp(s, pinv(s)) == ID4 and comp(pinv(s), s) == ID4)
NASSOC = sum(1 for a in S4 for b in S4 for c in S4
             if comp(comp(a, b), c) == comp(a, comp(b, c)))
assert NCLOSE == len(S4) ** 2, "composition never leaves the set: that is closure"
assert NINVER == len(S4), "every element has a two-sided inverse inside the set"
assert ID4 in SET4, "the identity map is one of the permutations"
assert NASSOC == len(S4) ** 3, "composition is associative on every triple"
SG0 = (1, 2, 3, 0)
SG0I = pinv(SG0)
assert comp(SG0, SG0I) == ID4, "the left figure's two layers really do cancel"

# ── beat 1: transpositions, and the parity of every factorisation ──────
def factor(s):
 """Transpositions t1..tk, as index pairs, with s = t1 o t2 o ... o tk.

 Built by clearing the arrangement one value at a time, so the list is a
 factorisation and not a lucky guess; `rebuild` below is what checks it."""
 n = len(s)
 a = list(s)
 out = []
 for i in range(n):
  if a[i] != i:
   j = a[i]
   out.append((min(i, j), max(i, j)))
   a = [i if v == j else j if v == i else v for v in a]
 return out


def rebuild(pairs, n):
 r = tuple(range(n))
 for i, j in pairs:
  r = comp(r, tau(n, i, j))
 return r


assert all(rebuild(factor(s), 4) == s for s in S4), \
    "every one of the 24 permutations is a product of transpositions"

# every factorisation of length at most five, found by breadth-first search
WIT = {ID4: {0: ()}}
for _L in range(1, 6):
 for _s in [k for k in list(WIT) if _L - 1 in WIT[k]]:
  _base = WIT[_s][_L - 1]
  for _p in TR4:
   WIT.setdefault(comp(_s, tau(4, *_p)), {}).setdefault(_L, _base + (_p,))
assert len(WIT) == len(S4), "transpositions of five or fewer already reach all of S4"
assert all(len({L % 2 for L in w}) == 1 for w in WIT.values()), \
    "a permutation's factorisations may differ in length but never in parity"
assert all(rebuild(w, 4) == s for s, ws in WIT.items() for w in ws.values()), \
    "each witness really does multiply out to the permutation it is filed under"
SG1 = (1, 2, 3, 0)
DEC = {L: WIT[SG1][L] for L in sorted(WIT[SG1])}
assert sorted(DEC) == [3, 5], "this one is a product of three transpositions, or of five"
assert len(set(DEC[5])) == 5, "and the five are five different transpositions, not padding"
assert all(sgn(s) == (1 if min(WIT[s]) % 2 == 0 else -1) for s in S4), \
    "parity of the shortest factorisation is the sign defined later by inversions"
MINLEN = [sum(1 for s in S4 if min(WIT[s]) == k) for k in range(4)]
assert sum(MINLEN) == 24 and MINLEN[0] == 1, "the 24 split by shortest length as printed"
STEPS = [ID4]
for _p in DEC[3]:
 STEPS.append(comp(STEPS[-1], tau(4, *_p)))
assert STEPS[-1] == SG1, "the left figure's last row is the permutation being built"

# ── beat 2: right translation is a bijection ──────────────────────────
RHO2 = (1, 2, 0)
IMG2 = [comp(s, RHO2) for s in S3]
assert sorted(IMG2) == sorted(S3), "right translation lands on all of S3, so it is onto"
assert len(set(IMG2)) == len(S3), "and hits each one once, so it is also one to one"
NRIGHT = sum(1 for r in S4 if sorted(comp(s, r) for s in S4) == sorted(S4))
NLEFT = sum(1 for r in S4 if sorted(comp(r, s) for s in S4) == sorted(S4))
assert NRIGHT == len(S4) and NLEFT == len(S4), \
    "both one-sided translations are bijections, for every fixed element of S4"

# ── beat 3: the count is n factorial ───────────────────────────────────
COUNT = [(n, len(list(permutations(range(n)))), math.factorial(n)) for n in range(1, 7)]
assert all(c == f for _n, c, f in COUNT), \
    "the enumerated number of permutations equals n factorial, n = 1 to 6"

# ── beats 4 to 6: a concrete 3-linear functional and the action ────────
MDIM, NARG = 3, 3
IDX = list(product(range(MDIM), repeat=NARG))
_rs = np.random.default_rng(86)
COEF = {p: round(float(v), 3) for p, v in zip(IDX, _rs.uniform(-2.0, 2.0, len(IDX)))}
VECS = [tuple(tuple(round(float(x), 3) for x in row)
              for row in _rs.uniform(-1.0, 1.0, (NARG, MDIM))) for _ in range(6)]


def fval(C, xs):
 return sum(c * math.prod(xs[k][p[k]] for k in range(NARG)) for p, c in C.items())


def act(C, s, inverse=True):
 """The coefficient array of f dot sigma.

 The book's definition is pointwise, f(xi o sigma^-1); on coefficients that is
 C[q o sigma^-1], which is checked against the pointwise version below."""
 t = pinv(s) if inverse else s
 return {q: C[comp(q, t)] for q in C}


def slots(xs, s, inverse=True):
 t = pinv(s) if inverse else s
 return tuple(xs[t[k]] for k in range(NARG))


def gap(C, D):
 return max(abs(C[p] - D[p]) for p in IDX)


DSAME = max(abs(fval(act(COEF, s), xs) - fval(COEF, slots(xs, s)))
            for s in S3 for xs in VECS)
assert DSAME < 1e-12, \
    "the coefficient action and the pointwise definition are the same functional"

LEM31 = max(gap(act(COEF, comp(a, b)), act(act(COEF, a), b)) for a in S3 for b in S3)
N31 = sum(1 for a in S3 for b in S3
          if gap(act(COEF, comp(a, b)), act(act(COEF, a), b)) > 1e-12)
assert LEM31 == 0.0 and N31 == 0, "Lemma 3.1 holds for all 36 pairs, to the last bit"

WRONG = max(gap(act(COEF, comp(a, b), False), act(act(COEF, a, False), b, False))
            for a in S3 for b in S3)
NWRONG = sum(1 for a in S3 for b in S3
             if gap(act(COEF, comp(a, b), False),
                    act(act(COEF, a, False), b, False)) > 1e-12)
WREV = max(gap(act(COEF, comp(b, a), False), act(act(COEF, a, False), b, False))
           for a in S3 for b in S3)
assert WRONG > 1.0 and NWRONG == 18, \
    "without the inverse Lemma 3.1 fails on exactly the 18 pairs that do not commute"
assert WREV == 0.0, "what it satisfies instead is the same law with the factors swapped"

ANTI = max(gap(act(COEF, comp(r, s)), act(act(COEF, r), s)) for r in S3 for s in S3)
HOMO = max(gap(act(COEF, comp(r, s)), act(act(COEF, s), r)) for r in S3 for s in S3)
NHOMO = sum(1 for r in S3 for s in S3
            if gap(act(COEF, comp(r, s)), act(act(COEF, s), r)) > 1e-12)
NCOMM = sum(1 for r in S3 for s in S3 if comp(r, s) == comp(s, r))
assert ANTI == 0.0, "T of a product is the second operator after the first: an antihomomorphism"
assert HOMO > 1.0 and NHOMO == 18, \
    "the other order fails, which is the evidence for the word anti"
assert NHOMO + NCOMM == len(S3) ** 2, "and it fails on precisely the non-commuting pairs"
INVOK = max(gap(act(act(COEF, s), pinv(s)), COEF) for s in S3)
assert INVOK == 0.0, "T of the inverse undoes T, so each one is invertible"

# ── beat 5: the two routes drawn on the left ───────────────────────────
RHO5, SIG5 = (1, 2, 0), (1, 0, 2)
assert comp(RHO5, SIG5) != comp(SIG5, RHO5), \
    "the two routes end somewhere different only because these two do not commute"
ROUTE = gap(act(act(COEF, RHO5), SIG5), act(act(COEF, SIG5), RHO5))
assert ROUTE > 1.0, "and the gap between the endpoints is not a rounding error"

# ── beat 6: Lemma 3.2, the basis is only rearranged ────────────────────
MB, NB = 2, 3
IDXB = list(product(range(MB), repeat=NB))
SG6 = (1, 2, 0)


def delta(p):
 return {q: (1.0 if q == p else 0.0) for q in IDXB}


NB32 = 0
for _p in IDXB:
 for _s in permutations(range(NB)):
  _got = {q: COEFB for q, COEFB in act(delta(_p), _s).items()}
  if _got == delta(comp(_p, _s)):
   NB32 += 1
assert NB32 == len(IDXB) * math.factorial(NB), \
    "every basis element goes to a basis element, namely the one indexed by p after sigma"
ORBIT = []
_seen = set()
for _p in IDXB:
 if _p in _seen:
  continue
 _cyc, _q = [], _p
 while _q not in _seen:
  _seen.add(_q)
  _cyc.append(_q)
  _q = comp(_q, SG6)
 ORBIT.append(_cyc)
assert sorted(len(c) for c in ORBIT) == [1, 1, 3, 3], \
    "this sigma breaks the eight basis elements into two fixed points and two 3-cycles"
CYC3 = [c for c in ORBIT if len(c) == 3]
FIX3 = [c[0] for c in ORBIT if len(c) == 1]

# ── beat 7: the polynomial E ───────────────────────────────────────────
def epoly(x):
 return math.prod(x[i] - x[j] for i in range(len(x)) for j in range(i + 1, len(x)))


X3 = (0.4, -0.9, 1.6)
SG7 = (2, 0, 1)
PAIRS7 = [(i, j) for i in range(3) for j in range(i + 1, 3)]
FACT7 = [(i, j, SG7[i], SG7[j], X3[i] - X3[j], SG7[i] > SG7[j]) for i, j in PAIRS7]
E7 = epoly(X3)
E7S = epoly(tuple(X3[SG7[i]] for i in range(3)))
NREV7 = sum(1 for *_r, rev in FACT7 if rev)
assert NREV7 == inversions(SG7) == 2, "this sigma reverses two of the three pairs"
assert abs(E7S - sgn(SG7) * E7) < 1e-12 and sgn(SG7) == 1, \
    "two sign flips cancel, so E comes back unchanged even though factors moved"
assert abs(E7) > 1.0, "and E is evaluated away from its zero set, so dividing by it is legal"
assert abs(math.prod(f for *_a, f, _r in FACT7) - E7) < 1e-12, \
    "the three printed factors are the ones E is actually the product of"

# ── beat 8: sgn, as the number of reversals ───────────────────────────
TAB8 = [(s, inversions(s), sgn(s)) for s in S3]
assert [t[1] for t in TAB8] == [0, 1, 1, 2, 2, 3], "the six reversal counts of S3"
XE = (0.3, -1.1, 2.0, 0.7)
assert abs(epoly(XE)) > 1e-3, "E is nonzero here, which the cancellation in beat 9 needs"
DSGN = max(abs(epoly(tuple(XE[s[i]] for i in range(4))) - sgn(s) * epoly(XE)) for s in S4)
NSGN = sum(1 for s in S4
           if abs(epoly(tuple(XE[s[i]] for i in range(4))) - sgn(s) * epoly(XE)) < 1e-9)
assert NSGN == len(S4) and DSGN < 1e-12, \
    "E after sigma is sgn sigma times E, for all 24 elements of S4"
assert all(inversions(s) == inversions(pinv(s)) for s in S4), \
    "sigma and its inverse reverse the same number of pairs, so the sign does not care which"

SG8 = (2, 0, 3, 1)
SG8I = pinv(SG8)
XW = (-5.60, -4.80, -4.00, -3.20)
YTOP, YBOT = 0.86, -0.66


def _cross(a1, b1, a2, b2):
 """Where two straight strands meet, as a fraction of the way down."""
 den = (b1 - a1) - (b2 - a2)
 if abs(den) < 1e-12:
  return None
 u = (a2 - a1) / den
 return u if 1e-9 < u < 1.0 - 1e-9 else None


CROSS = []
for _v in range(4):
 for _w in range(_v + 1, 4):
  _u = _cross(XW[_v], XW[SG8I[_v]], XW[_w], XW[SG8I[_w]])
  if _u is not None:
   CROSS.append((XW[_v] + (XW[SG8I[_v]] - XW[_v]) * _u, YTOP + (YBOT - YTOP) * _u))
assert len(CROSS) == inversions(SG8) == 3, \
    "the strands cross once per reversed pair, so counting crossings counts reversals"

# ── beat 9: sgn is a homomorphism, transpositions are odd ─────────────
NMULT = sum(1 for r in S4 for s in S4 if sgn(comp(r, s)) == sgn(r) * sgn(s))
assert NMULT == len(S4) ** 2, "sgn of a product is the product of the sgns, all 576 pairs"
_rp = np.random.default_rng(409)
SAMPLE = [(S4[int(a)], S4[int(b)]) for a, b in _rp.integers(0, len(S4), (50, 2))]
assert all(sgn(comp(r, s)) == sgn(r) * sgn(s) for r, s in SAMPLE), \
    "the fifty sampled pairs multiply correctly too"
assert all(sgn(tau(4, i, j)) == -1 for i, j in TR4), \
    "all six transpositions of S4 are odd"
EVEN = [s for s in S4 if sgn(s) == 1]
ODD = [s for s in S4 if sgn(s) == -1]
TSW = tau(4, 0, 1)
assert len(EVEN) == len(ODD) == 12, "the 24 split into two halves of twelve"
assert sorted(comp(TSW, s) for s in EVEN) == sorted(ODD), \
    "multiplying by one transposition carries one half onto the other"

# ── beat 10: the alternating projection ───────────────────────────────
def omega(m, n):
 idx = list(product(range(m), repeat=n))
 at = {p: k for k, p in enumerate(idx)}
 out = np.zeros((len(idx), len(idx)))
 for s in permutations(range(n)):
  for p in idx:
   out[at[comp(p, s)], at[p]] += sgn(s) / math.factorial(n)
 return out


RANKS = []
for _m, _n in ((3, 2), (3, 3), (3, 4)):
 _O = omega(_m, _n)
 RANKS.append((_m, _n, int(np.linalg.matrix_rank(_O, tol=1e-9)), math.comb(_m, _n),
               float(np.abs(_O @ _O - _O).max())))
assert all(r == c for _m, _n, r, c, _i in RANKS), \
    "the alternating subspace has the dimension of the m-choose-n subsets"
assert all(i < 1e-12 for *_x, i in RANKS), "and the averaging map really is a projection"
CMAT = np.array([[2.0, -3.0, 1.0], [1.0, 0.0, -2.0], [3.0, 2.0, -1.0]])
AMAT = (CMAT - CMAT.T) / 2.0
assert np.abs(AMAT + AMAT.T).max() < 1e-12, "the projected array is its own negative transposed"
assert np.abs(np.diag(AMAT)).max() < 1e-12, "which forces its diagonal to vanish"
assert np.abs(omega(3, 2) @ CMAT.reshape(-1) - AMAT.reshape(-1)).max() < 1e-12, \
    "and it is what the averaging formula gives, not a separate recipe"


class AdvCalcE86Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 86

 MODE_LABEL = {
  0: {"zh": "置換：在複合之下是一個群", "en": "permutations: a group under composition"},
  1: {"zh": "對換，以及分解的不唯一", "en": "transpositions, and factorisations that differ"},
  2: {"zh": "固定一個元素，右乘是雙射",
      "en": "one element fixed: translation is a bijection"},
  3: {"zh": "個數是 n 階乘", "en": "the count is n factorial"},
  4: {"zh": "作用在泛函上：為什麼是反元素",
      "en": "the action on a functional: why the inverse"},
  5: {"zh": "定理 3.1：反同態", "en": "theorem 3.1: an antihomomorphism"},
  6: {"zh": "引理 3.2：基底只是被重排", "en": "lemma 3.2: the basis is only rearranged"},
  7: {"zh": "多項式 E", "en": "the polynomial E"},
  8: {"zh": "正負號的定義", "en": "the definition of the sign"},
  9: {"zh": "正負號是同態", "en": "the sign is a homomorphism"},
  10: {"zh": "交錯：下一節的子空間", "en": "alternating: the next section's subspace"},
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

 def _nodes(self, xs, y, labels, color, size=FS_TAG - 2, w=0.30):
  """A row of numbered places, each label centred on its own place."""
  return VGroup(*[self._sym(y, s, color, size, x=x, w=w) for x, s in zip(xs, labels)])

 def _link(self, xa, ya, xb, yb, color, pad=0.16, sw=2.2, tl=0.11):
  """An arrow from one place to another, pulled back clear of both labels."""
  dx, dy = xb - xa, yb - ya
  n = math.hypot(dx, dy)
  if n < 2.0 * pad + 0.05:
   return VGroup()
  ux, uy = dx / n, dy / n
  return self._arr([xa + ux * pad, ya + uy * pad, 0],
                   [xb - ux * pad, yb - uy * pad, 0], color, sw=sw, tl=tl)

 def _ring(self, cx, cy, r, labels, color, lpad=0.24, size=FS_TAG - 4):
  """A cycle drawn as a triangle of arrows, labels outside the vertices."""
  ang = [math.pi / 2.0, math.pi * 7.0 / 6.0, math.pi * 11.0 / 6.0]
  vx = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in ang]
  lx = [(cx + (r + lpad) * math.cos(a) * 1.55, cy + (r + lpad) * math.sin(a))
        for a in ang]
  g = VGroup()
  for k in range(3):
   a, b = vx[k], vx[(k + 1) % 3]
   g.add(self._link(a[0], a[1], b[0], b[1], color, pad=0.08, sw=2.0, tl=0.10))
  for (x, y), s in zip(lx, labels):
   g.add(self._sym(y, s, color, size, x=x, w=0.42))
  return g

 # ── beat 0: the four axioms ─────────────────────────────────────
 def _group(self):
  xs = (-5.60, -4.85, -4.10, -3.35)
  ys = (0.86, 0.06, -0.74)
  g = VGroup()
  for y in ys:
   g.add(self._nodes(xs, y, [str(k + 1) for k in range(4)], INK))
  for i in range(4):
   g.add(self._link(xs[i], ys[0], xs[SG0[i]], ys[1], ACCENT_B))
   g.add(self._link(xs[i], ys[1], xs[SG0I[i]], ys[2], ACCENT_C))
  g.add(self._sym(0.46, "σ", ACCENT_B, FS_TAG, x=-2.80, w=0.32),
        self._sym(-0.34, "σ ⁻ ¹", ACCENT_C, FS_TAG - 1, x=-2.72, w=0.72))
  g.add(self._table(((f"σ ∘ ρ   ∈   S ₄            {NCLOSE} / {len(S4) ** 2}", ACCENT_B),
                     (f"σ ∘ σ ⁻ ¹   =   I            {NINVER} / {len(S4)}", ACCENT_C),
                     (f"I   =   ( {show(ID4)} )   ∈   S ₄", ACCENT_A),
                     ("( σ ₁ ∘ σ ₂ ) ∘ σ ₃   =   σ ₁ ∘ ( σ ₂ ∘ σ ₃ )", ACCENT_A),
                     (f"            {NASSOC} / {len(S4) ** 3}", DIM),
                     (f"σ   =   ( {show(SG0)} )", ACCENT_B),
                     (f"σ ⁻ ¹   =   ( {show(SG0I)} )", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("四個分數都是把整個 S₄ 列舉過的結果",
                  "each of those counts comes from enumerating the whole of S four"))
  return g.add(self._foot("集合上的置換就是這個集合到自己的一個一對一又映成的對應。所有置換合起來在複合之下封閉，每個都有反元素，恆等映射也在裡面",
                          "a permutation of a set is a one to one correspondence of that set with itself; the collection of all of them is closed under composition, each has an inverse, and the identity map is one of them",
                          ACCENT_A,
                          "再加上複合本來就滿足結合律，這四件事加起來講的正是一件事：它在複合之下是一個群。左圖上半是一個置換，下半把它還原回去",
                          "together with the associativity that composition always has, those four statements say exactly that it is a group; the figure's upper half is one permutation and the lower half undoes it"))

 # ── beat 1: transpositions ──────────────────────────────────────
 def _transp(self):
  xs = (-5.55, -4.85, -4.15, -3.45)
  ys = (0.92, 0.32, -0.28, -0.88)
  g = VGroup()
  for k, (y, st) in enumerate(zip(ys, STEPS)):
   moved = set(DEC[3][k - 1]) if k else set()
   for x, v, j in zip(xs, st, range(4)):
    g.add(self._sym(y, str(v + 1), WARN if j in moved else INK, FS_TAG - 1, x=x, w=0.30))
   if k:
    i, j = DEC[3][k - 1]
    g.add(self._sym(y, f"( {i + 1}  {j + 1} )", WARN, FS_TAG - 3, x=-2.78, w=0.76))
  g.add(self._table(((f"σ   =   ( {show(SG1)} )", ACCENT_A),
                     ("k   =   3        "
                      + "  ".join(f"( {i + 1}  {j + 1} )" for i, j in DEC[3]), ACCENT_B),
                     ("k   =   5        "
                      + " ".join(f"( {i + 1} {j + 1} )" for i, j in DEC[5]), ACCENT_C),
                     ("( − 1 ) ᵏ        − 1            − 1", ACCENT_A),
                     (f"τ ₁ ∘ ⋯ ∘ τ ₖ   =   σ            {len(S4)} / {len(S4)}", ACCENT_B),
                     (f"k   ≤   5            {len(WIT)} / {len(S4)}", ACCENT_B),
                     ("      k        0      1      2      3", DIM),
                     ("                " + "    ".join(f"{m:<2d}" for m in MINLEN), ACCENT_C)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("兩種寫法長度一個三一個五，奇偶一樣",
                  "the two factorisations have lengths three and five, and the same parity"))
  return g.add(self._foot("最簡單的非恆等置換是把兩個元素互換、其他全部不動，這種叫對換。任何置換都能寫成若干個對換的乘積，而且寫法不只一種",
                          "the simplest permutation other than the identity swaps two elements and leaves the rest alone, and is called a transposition; every permutation is a product of them, in more than one way",
                          ACCENT_A,
                          "左圖從恆等排列出發，每一步交換兩個位置，紅色是剛被動過的那兩個，三步走到目標。右表還給了一個五步的寫法，長度不同但奇偶相同",
                          "the figure starts from the identity arrangement and swaps two places at each step, in red, reaching the target in three; the panel adds a factorisation of length five, a different length of the same parity"))

 # ── beat 2: right translation ───────────────────────────────────
 def _biject(self):
  xa, xb, y0, dy = -5.50, -3.15, 0.88, 0.38
  ys = [y0 - k * dy for k in range(6)]
  at = {s: ys[k] for k, s in enumerate(S3)}
  g = VGroup()
  for k, s in enumerate(S3):
   hot = ACCENT_A if k == 0 else INK
   g.add(self._sym(ys[k], flat(s), hot, FS_TAG - 3, x=xa, w=0.62),
         self._sym(ys[k], flat(s), DIM, FS_TAG - 3, x=xb, w=0.62))
  for k, s in enumerate(S3):
   g.add(self._link(xa + 0.34, ys[k], xb - 0.34, at[comp(s, RHO2)],
                    ACCENT_A if k == 0 else ACCENT_B, pad=0.06, sw=1.8, tl=0.09))
  g.add(self._sym(1.20, "σ", ACCENT_A, FS_TAG, x=xa, w=0.32),
        self._sym(1.20, "σ ∘ ρ", ACCENT_B, FS_TAG - 1, x=xb, w=0.80))
  g.add(self._table((f"ρ   =   ( {show(RHO2)} )", ACCENT_A),
                    ("σ   ↦   σ ∘ ρ", ACCENT_B),
                    ("σ ′   =   ( σ ′ ∘ ρ ⁻ ¹ )  ∘  ρ", ACCENT_B),
                    ("σ ₁ ∘ ρ  =  σ ₂ ∘ ρ      ⇒      σ ₁  =  σ ₂", ACCENT_C),
                    (f"{{ σ ∘ ρ }}   =   S ₃            {len(set(IMG2))} / {len(S3)}", ACCENT_A),
                    (f"{{ σ ∘ ρ }}   =   S ₄            {NRIGHT} / {len(S4)}", ACCENT_B),
                    (f"{{ ρ ∘ σ }}   =   S ₄            {NLEFT} / {len(S4)}", ACCENT_C))
  g.add(self._cap("右欄是同一份名單，箭頭只是把它重新排過",
                  "the right column is the same list, and the arrows only reorder it"))
  return g.add(self._foot("接下來要一個很小但後面一直用得到的事實：把 ρ 固定住，那麼把 σ 送到 σ 複合 ρ 的這個對應，是置換群到自己的雙射",
                          "next comes a small fact that gets used over and over: with one element held fixed, sending each permutation to its composite with that one is a bijection of the group onto itself",
                          ACCENT_A,
                          "映成是因為任何目標都寫得成「它先複合 ρ 的反元素」再複合 ρ；單射是因為右邊一起消去 ρ 就得到兩者相等。以後換和式的指標靠的就是它",
                          "it is onto because any target can be written as itself composed with the inverse first, and one to one because the fixed factor cancels on the right; later it is what reindexes a sum"))

 # ── beat 3: n factorial ─────────────────────────────────────────
 def _count(self):
  xs = [-4.20 + (k - 2.5) * 0.55 for k in range(6)]
  x1 = (-5.30, -4.20, -3.10)
  y0, y1, y2 = 1.02, 0.32, -0.38
  g = VGroup(Dot([-4.20, y0, 0], radius=0.065, color=ACCENT_A))
  for x in x1:
   g.add(Dot([x, y1, 0], radius=0.060, color=ACCENT_B),
         Line([-4.20, y0, 0], [x, y1, 0], color=DIM, stroke_width=1.4))
  for k, x in enumerate(xs):
   g.add(Dot([x, y2, 0], radius=0.055, color=ACCENT_C),
         Line([x1[k // 2], y1, 0], [x, y2, 0], color=DIM, stroke_width=1.4))
   g.add(self._sym(y2 - 0.36, flat(S3[k]), ACCENT_C, FS_TAG - 5, x=x, w=0.50))
  for y, s in ((0.67, "×  3"), (-0.03, "×  2"), (-0.73, "×  1")):
   g.add(self._sym(y, s, DIM, FS_TAG - 3, x=-2.34, w=0.52))
  g.add(self._table((("      n            n !            | S ₙ |", DIM),)
                    + tuple((f"      {n}          {f:<4d}          {c:<4d}",
                             ACCENT_B if n % 2 else ACCENT_C)
                            for n, c, f in COUNT),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("右邊兩欄一欄是階乘，一欄是真的數出來的",
                  "one of the two columns is the factorial and the other is an actual count"))
  return g.add(self._foot("置換的個數是 n 階乘，這是中學就算過的計數。σ 作用在一上有 n 種選法，選定以後作用在二上只剩 n 減一種，再來 n 減二種",
                          "the number of permutations is n factorial, the count from secondary school: the image of one can be chosen in n ways, then the image of two in n minus one, then n minus two",
                          ACCENT_A,
                          "一路乘下去就是 n 階乘。左圖是 n 等於三的選擇樹：第一層三條岔路，第二層各兩條，第三層已經沒得選，六片葉子正好是六個置換",
                          "multiplying all the way down gives n factorial; the tree is the case of three, branching three ways and then two, with nothing left to choose, and its six leaves are the six permutations"))

 # ── beat 4: the action, and the inverse in it ───────────────────
 def _action(self):
  g = VGroup()
  g.add(self._box(-5.50, 0.70, "f", ACCENT_A, w=0.52, h=0.50, size=FS_TAG + 1))
  g.add(self._box(-3.55, 0.70, "f · σ ₁", ACCENT_B, w=1.10, h=0.50, size=FS_TAG))
  g.add(self._box(-3.55, -0.42, "( f · σ ₁ ) · σ ₂", ACCENT_C, w=1.92, h=0.50,
                  size=FS_TAG - 2))
  g.add(self._arr([-5.20, 0.70, 0], [-4.16, 0.70, 0], DIM, sw=3, tl=0.13))
  g.add(self._arr([-3.55, 0.42, 0], [-3.55, -0.14, 0], DIM, sw=3, tl=0.12))
  g.add(self._arr([-5.34, 0.42, 0], [-4.52, -0.26, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(1.00, "σ ₁", ACCENT_B, FS_TAG - 1, x=-4.68, w=0.52),
        self._sym(0.14, "σ ₂", ACCENT_C, FS_TAG - 1, x=-2.42, w=0.52),
        self._sym(-0.14, "σ ₁ σ ₂", ACCENT_A, FS_TAG - 2, x=-5.26, w=0.90))
  g.add(self._sym(-0.98, "f ( ξ ∘ σ )      ⇒      f · ( σ ₁ σ ₂ )   =   ( f · σ ₂ ) · σ ₁",
                  WARN, FS_TAG - 3, x=-4.20, w=3.90))
  g.add(self._table((("f  :  V × V × V  →  ℝ            dim V  =  3", ACCENT_A),
                     ("( f · σ ) ( ξ )   =   f ( ξ ∘ σ ⁻ ¹ )", ACCENT_A),
                     ("f · ( σ ₁ σ ₂ )   =   ( f · σ ₁ ) · σ ₂", ACCENT_B),
                     ("                    ‖ Δ ‖            #", DIM),
                     (f"ξ ∘ σ ⁻ ¹            {LEM31:.0e}            {N31} / 36", ACCENT_B),
                     (f"ξ ∘ σ                {WRONG:.2f}            {NWRONG} / 36", WARN),
                     (f"ξ ∘ σ  ,  σ ₂ σ ₁        {WREV:.0e}            0 / 36", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("右欄是不成立的對數：中間那列有十八對",
                  "the last column counts the pairs that fail, and the middle row has eighteen"))
  return g.add(self._foot("置換也可以作用在多重線性泛函上：把 f 點 σ 定義成先用 σ 的反元素把輸入那串向量重排，再餵給 f。為什麼是反元素而不是 σ 本身",
                          "a permutation can also act on a multilinear functional: rearrange the incoming list of vectors by the inverse first, then feed it in; why the inverse and not the permutation itself",
                          ACCENT_A,
                          "因為這樣才會有引理 3.1：先用 σ 一再用 σ 二，剛好等於直接用兩者的乘積。右表把不用反元素的版本也算了，三十六對裡有十八對不成立",
                          "because only then does Lemma 3.1 hold: acting by one and then the other is acting by the product; the panel computes the version without the inverse, and eighteen of its thirty six pairs fail"))

 # ── beat 5: the antihomomorphism ────────────────────────────────
 def _anti(self):
  g = VGroup()
  for y, (p, q), col, ly in ((0.70, ("ρ", "σ"), ACCENT_B, 1.02),
                             (-0.58, ("σ", "ρ"), ACCENT_C, -0.90)):
   g.add(self._sym(y, "f", ACCENT_A, FS_TAG, x=-5.75, w=0.32))
   g.add(self._sym(y, f"f · {p}", col, FS_TAG - 1, x=-4.55, w=0.84))
   g.add(self._sym(y, f"f · {p} {q}", col, FS_TAG - 1, x=-3.00, w=1.08))
   g.add(self._link(-5.75, y, -4.55, y, DIM, pad=0.26, sw=2.2, tl=0.11))
   g.add(self._link(-4.55, y, -3.00, y, DIM, pad=0.48, sw=2.2, tl=0.11))
   g.add(self._sym(ly, f"T ( {p} )", DIM, FS_TAG - 3, x=-5.18, w=0.82),
         self._sym(ly, f"T ( {q} )", DIM, FS_TAG - 3, x=-3.80, w=0.82))
  g.add(self._dash([-3.00, 0.50, 0], [-3.00, 0.16, 0], WARN, n=4, sw=2.0),
        self._dash([-3.00, -0.04, 0], [-3.00, -0.38, 0], WARN, n=4, sw=2.0),
        self._sym(0.06, "≠", WARN, FS_TAG, x=-3.00, w=0.30))
  g.add(self._table(((f"T ( σ )  f   =   f · σ            ρ  =  ( {show(RHO5)} )", ACCENT_A),
                     (f"T ( ρ σ )   =   T ( σ )  ∘  T ( ρ )        σ  =  ( {show(SIG5)} )",
                      ACCENT_B),
                     ("                        ‖ Δ ‖            #", DIM),
                     (f"T ( σ )  ∘  T ( ρ )        {ANTI:.0e}            0 / 36", ACCENT_B),
                     (f"T ( ρ )  ∘  T ( σ )        {HOMO:.2f}            {NHOMO} / 36", WARN),
                     (f"ρ σ   =   σ ρ                            {NCOMM} / 36", ACCENT_C),
                     (f"T ( σ ⁻ ¹ ) ∘ T ( σ )   =   I            {INVOK:.0e}", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("不成立的十八對，正好就是不可交換的那十八對",
                  "the eighteen pairs that fail are exactly the eighteen that do not commute"))
  return g.add(self._foot("定理 3.1 說，把 f 送到 f 點 σ 的那個算子是線性的，也是可逆的，所以它是個同構。但要很小心它乘起來的順序",
                          "Theorem 3.1 says the operator carrying a functional to its image under one permutation is linear and invertible, hence an isomorphism; but the order in which these operators multiply needs care",
                          ACCENT_A,
                          "ρ 乘 σ 對應的算子，等於先做 ρ 那個再做 σ 那個，順序是顛倒的，所以書上叫它反同態。左圖兩條路的終點不一樣，右表把那個差距算出來了",
                          "the operator of a product is the second one after the first, in reverse order, which is why the book calls it an antihomomorphism; the two routes end apart, and the panel measures the gap"))

 # ── beat 6: lemma 3.2 ───────────────────────────────────────────
 def _basis(self):
  g = VGroup()
  for cy, cyc, col in ((0.62, CYC3[0], ACCENT_B), (-0.52, CYC3[1], ACCENT_C)):
   g.add(self._ring(-4.60, cy, 0.32, [flat(p) for p in cyc], col))
  for cy, p, col in ((0.62, FIX3[0], ACCENT_A), (-0.52, FIX3[1], ACCENT_A)):
   g.add(self._sym(cy, f"{flat(p)}   ↦   {flat(p)}", col, FS_TAG - 4, x=-2.95, w=1.10))
  g.add(self._table((f"m  =  2        n  =  3        m ⁿ  =  {len(IDXB)}", ACCENT_A),
                    ("μ ( p )  ·  σ   =   μ ( p ∘ σ )", ACCENT_A),
                    (f"σ   =   ( {show(SG6)} )", ACCENT_B),
                    ("      p        ↦        p ∘ σ", DIM),
                    ("   ↦   ".join(flat(p) for p in CYC3[0] + [CYC3[0][0]]), ACCENT_B),
                    ("   ↦   ".join(flat(p) for p in CYC3[1] + [CYC3[1][0]]), ACCENT_C),
                    (f"{flat(FIX3[0])}   ↦   {flat(FIX3[0])}"
                     f"            {flat(FIX3[1])}   ↦   {flat(FIX3[1])}", ACCENT_A),
                    (f"S ₃  ×  m ⁿ            {NB32} / {len(IDXB) * 6}", ACCENT_B))
  g.add(self._cap("八個基底元素被分成兩個三元環加兩個不動點",
                  "the eight basis elements fall into two three-cycles and two fixed points"))
  return g.add(self._foot("引理 3.2 說，每一個這樣的算子都把張量積空間的那組基底送回基底自己，只是把它重新排列而已，並沒有產生新的東西",
                          "Lemma 3.2 says each of these operators carries the basis of the tensor product space into itself, merely rearranging it rather than producing anything new",
                          ACCENT_A,
                          "算出來是：指標為 p 的那個基底元素，被 σ 送到指標為 p 複合 σ 的那一個。左圖取二維空間、三重線性，八個基底被一個三循環這樣分",
                          "the computation gives the basis element indexed by p going to the one indexed by p composed with sigma; the figure takes a two-dimensional space and three slots, and one three-cycle splits the eight like this"))

 # ── beat 7: the polynomial E ────────────────────────────────────
 def _poly(self):
  cx, cy, r = -4.42, 0.80, 0.42
  ang = [math.pi / 2.0, math.pi * 7.0 / 6.0, math.pi * 11.0 / 6.0]
  vx = [(cx + r * math.cos(a) * 1.35, cy + r * math.sin(a)) for a in ang]
  g = VGroup()
  for (x, y), k in zip(vx, range(3)):
   g.add(self._sym(y, str(k + 1), INK, FS_TAG, x=x, w=0.28))
  for i, j, si, sj, _f, rev in FACT7:
   a, b = vx[i], vx[j]
   g.add(self._link(a[0], a[1], b[0], b[1], WARN if rev else ACCENT_B,
                    pad=0.17, sw=2.6, tl=0.10))
  for k, (i, j, si, sj, f, rev) in enumerate(FACT7):
   g.add(self._sym(-0.14 - 0.34 * k,
                   f"( x {'₁₂₃'[i]} − x {'₁₂₃'[j]} )   ↦   "
                   f"( x {'₁₂₃'[si]} − x {'₁₂₃'[sj]} )      {-1 if rev else 1:+d}",
                   WARN if rev else ACCENT_B, FS_TAG - 4, x=-4.30, w=3.60))
  g.add(self._sym(0.80, "σ", ACCENT_A, FS_TAG, x=-3.10, w=0.30))
  g.add(self._table(("E ( x )   =   ∏  ( x ᵢ  −  x ₖ )            i  <  k", ACCENT_A),
                    (f"n  =  3            ∏   :   {len(PAIRS7)}", DIM),
                    (f"x   =   ( {' , '.join(f'{v:+.1f}' for v in X3)} )", ACCENT_B),
                    (f"σ   =   ( {show(SG7)} )", ACCENT_A),
                    ("   ·   ".join(f"( {f:+.3f} )" for *_a, f, _r in FACT7), ACCENT_B),
                    (f"E ( x )   =   {E7:+.3f}", ACCENT_B),
                    (f"E ( x ∘ σ )   =   {E7S:+.3f}            {abs(E7S - E7):.0e}", ACCENT_C))
  g.add(self._cap("兩個因式各變一次號，乘起來剛好抵消",
                  "two of the factors change sign once each, and the two flips cancel"))
  return g.add(self._foot("第 4 節先定義一個特別的多項式 E：把所有編號由小到大的配對各取一個差，全部乘起來。n 等於三的時候只有三個因式",
                          "section four starts from one particular polynomial: take the difference across every pair of indices in increasing order and multiply them all together, which for three indices is three factors",
                          ACCENT_A,
                          "用 σ 重排變數之後，每個因式還是某一對的差，配對沒有少也沒有多，只是其中幾對的大小順序被顛倒了，那幾個因式就差一個負號",
                          "after the variables are permuted each factor is still the difference across some pair, with no pair lost or gained, but the order within some pairs is reversed and those factors change sign"))

 # ── beat 8: the definition of the sign ──────────────────────────
 def _sign(self):
  g = VGroup()
  g.add(self._nodes(XW, 1.00, [str(k + 1) for k in range(4)], INK))
  g.add(self._nodes(XW, -0.80, [str(v + 1) for v in SG8], DIM))
  for v in range(4):
   g.add(Line([XW[v], YTOP, 0], [XW[SG8I[v]], YBOT, 0],
              color=ACCENT_B, stroke_width=2.2))
  for x, y in CROSS:
   g.add(Dot([x, y, 0], radius=0.068, color=WARN))
  g.add(self._sym(0.10, f"r  =  {len(CROSS)}", WARN, FS_TAG - 1, x=-2.68, w=0.84))
  g.add(self._sym(-1.06, f"σ   =   ( {show(SG8)} )            sgn σ   =   {sgn(SG8):+d}",
                  ACCENT_A, FS_TAG - 3, x=-4.30, w=3.60))
  g.add(self._table((("      S ₃            r            sgn", DIM),)
                    + tuple((f"   ( {show(s)} )          {r}          {g_:+d}",
                             ACCENT_B if g_ > 0 else ACCENT_C) for s, r, g_ in TAB8)
                    + ((f"E ( x ∘ σ )  =  ( sgn σ ) E ( x )        {NSGN} / {len(S4)}",
                        ACCENT_A),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("中間那欄是顛倒的配對數，右欄是負一的那麼多次方",
                  "the middle column counts reversed pairs and the right one is minus one to that power"))
  return g.add(self._foot("所以 E 被 σ 作用之後只會整體差一個正負號：負一的「順序被顛倒的配對數」次方。這個正負號就叫做 σ 的正負號，記成 sgn",
                          "so permuting the variables changes that polynomial by one overall sign: minus one raised to the number of pairs whose order got reversed, and that sign is what gets called the sign of the permutation",
                          ACCENT_A,
                          "左圖是同一件事的另一種看法：把置換畫成四條線，兩條線交叉一次就代表有一對的順序被顛倒，所以數交點就等於數顛倒，這裡是三個",
                          "the figure is the same thing seen another way: draw the permutation as four strands and each crossing is one reversed pair, so counting crossings counts reversals, and here there are three"))

 # ── beat 9: sgn is a homomorphism ───────────────────────────────
 def _hom(self):
  g = VGroup()
  g.add(self._box(-5.45, 0.60, "sgn  =  + 1", ACCENT_B, w=1.52, h=0.56, size=FS_TAG - 3))
  g.add(self._box(-3.15, 0.60, "sgn  =  − 1", ACCENT_C, w=1.52, h=0.56, size=FS_TAG - 3))
  g.add(self._arr([-4.66, 0.74, 0], [-3.95, 0.74, 0], WARN, sw=3, tl=0.12))
  g.add(self._arr([-3.95, 0.46, 0], [-4.66, 0.46, 0], WARN, sw=3, tl=0.12))
  g.add(self._sym(1.02, "τ", WARN, FS_TAG, x=-4.30, w=0.30),
        self._sym(0.18, "τ", WARN, FS_TAG, x=-4.30, w=0.30))
  g.add(self._sym(0.18, f"{len(EVEN)}", ACCENT_B, FS_TAG - 2, x=-5.45, w=0.42),
        self._sym(0.18, f"{len(ODD)}", ACCENT_C, FS_TAG - 2, x=-3.15, w=0.42))
  g.add(self._sym(-0.42, f"sgn ( ρ σ )   =   ( sgn ρ ) ( sgn σ )        "
                         f"{NMULT} / {len(S4) ** 2}", ACCENT_A, FS_TAG - 3,
                  x=-4.30, w=3.80))
  g.add(self._sym(-0.86, f"τ  ∈  S ₄      ⇒      sgn τ   =   − 1            "
                         f"{len(TR4)} / {len(TR4)}", WARN, FS_TAG - 3, x=-4.30, w=3.80))
  g.add(self._table((("          ρ                σ              sgn", DIM),)
                    + tuple((f"   {flat(r)}        {flat(s)}        "
                             f"{sgn(r):+d} · {sgn(s):+d}  =  {sgn(comp(r, s)):+d}",
                             ACCENT_B if sgn(comp(r, s)) > 0 else ACCENT_C)
                            for r, s in SAMPLE[:5])
                    + ((f"E ( x ) ≠ 0            {epoly(XE):+.3f}", ACCENT_A),),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("最後一列就是證明裡拿來約掉的那個非零值",
                  "the last row is the nonzero value the proof cancels by"))
  return g.add(self._foot("正負號是個同態：兩個置換乘起來的正負號，等於它們各自的正負號相乘。證明是把那個多項式在一個讓它不為零的點上求值，再把它約掉",
                          "the sign is a homomorphism: the sign of a product is the product of the signs, proved by evaluating that polynomial at a point where it does not vanish and cancelling it",
                          ACCENT_A,
                          "另外，對換的正負號一定是負一。所以整個置換群被切成一樣大的兩半，左圖兩個框各十二個，乘上任何一個對換就會跳到另一邊",
                          "a transposition always has sign minus one, so the group splits into two halves of equal size, twelve and twelve in the figure, and multiplying by any transposition jumps from one to the other"))

 # ── beat 10: alternating ────────────────────────────────────────
 def _alt(self):
  g = VGroup()
  ga, _pa = self._numgrid(-5.30, 0.66, [[f"{v:+.0f}" for v in row] for row in CMAT],
                          dx=0.46, dy=0.34, size=FS_TAG - 4, color=DIM)
  gb, _pb = self._numgrid(-3.10, 0.66, [[f"{v:+.1f}" for v in row] for row in AMAT],
                          dx=0.46, dy=0.34, size=FS_TAG - 4, color=ACCENT_C,
                          hotcolor=WARN, hot=tuple((k, k) for k in range(3)))
  g.add(ga, gb, self._sym(0.66, "↦", ACCENT_A, FS_TAG, x=-4.20, w=0.30))
  g.add(self._sym(-0.10, "f", DIM, FS_TAG - 1, x=-5.30, w=0.30),
        self._sym(-0.10, "Ω f", ACCENT_C, FS_TAG - 1, x=-3.10, w=0.60))
  g.add(self._sym(-0.58, "( Ω f ) ᵢ ₖ   =   −  ( Ω f ) ₖ ᵢ", ACCENT_C, FS_TAG - 2,
                  x=-4.20, w=3.20))
  g.add(self._sym(-0.98, "( Ω f ) ᵢ ᵢ   =   0", WARN, FS_TAG - 2, x=-4.20, w=1.70))
  g.add(self._table((("f · σ   =   f", DIM),
                     ("f · σ   =   ( sgn σ )  f", ACCENT_A),
                     ("Ω f   =   ( 1 / n ! )  Σ  ( sgn σ )  f · σ", ACCENT_A),
                     ("      m        n        rank Ω        C ( m , n )", DIM))
                    + tuple((f"      {m}        {n}            {r}              {c}",
                             ACCENT_B if r else ACCENT_C) for m, n, r, c, _i in RANKS)
                    + ((f"Ω ∘ Ω   =   Ω            {max(i for *_x, i in RANKS):.0e}",
                        ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("右邊那個陣列對角線是零，對稱位置互為相反數",
                  "the right-hand array has a zero diagonal and opposite entries across it"))
  return g.add(self._foot("有了正負號就可以把「交錯」講清楚：f 被任何置換作用之後都等於那個置換的正負號乘上 f。對稱則是作用之後完全不變",
                          "with the sign in hand the word alternating can be said precisely: acting by any permutation multiplies the functional by that permutation's sign, while symmetric means acting changes nothing at all",
                          ACCENT_A,
                          "左圖把一個係數陣列投影過去，得到的那個對角線全是零、對稱位置互為相反數。右表那個投影的秩，正好是從 m 個裡取 n 個的組合數。下一集就做這個子空間",
                          "the figure projects one coefficient array and the result has a vanishing diagonal with opposite entries across it; the projection's rank is the number of n-element subsets of m, and the next episode builds that subspace"))

 def stage(self):
  a, b, c = self._group(), self._transp(), self._biject()
  d, e, f_ = self._count(), self._action(), self._anti()
  h, i, j = self._basis(), self._poly(), self._sign()
  k, l = self._hom(), self._alt()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE86ZH, AdvCalcE86EN = make(AdvCalcE86Base, "86", prefix="AdvCalcE")
