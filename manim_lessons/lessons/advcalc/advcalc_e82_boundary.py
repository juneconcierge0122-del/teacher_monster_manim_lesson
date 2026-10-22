"""advcalc E82 -- chapter 6, section 6 (book pp. 294-297), as far as Lemma 6.3.

This half-section changes tools.  A boundary-value problem looks like an
initial-value problem -- the same equation, the same operator -- but the data
sits somewhere else: the initial-value problem pins f and f' at one point, the
boundary-value problem pins one value of f at each end of [a, b].  The book is
blunt about what that costs: the reader has no clue how to attack it from the
initial-value development, and wholly new tools have to be devised.  The tools
are the scalar product and self-adjointness, and this episode is about what
self-adjointness means for a differential operator.

The cut falls after Lemma 6.3 because that is where the section stops talking
about the operator and starts estimating: Lemma 6.4 needs c2 bounded below and
lambda large, which is E83's business.  So the eleven beats run from the
contrast between the two kinds of data, through integration by parts, the
formal adjoint R, the parity of n, the second-order formulas, Lemma 6.2,
Lemma 6.1, the four self-adjoint boundary conditions, Lemma 6.3, and the
closing remark about T - lambda.

Every number on screen is computed here.  The interval is [-1, 1], chosen so
that a 220-point Gauss-Legendre rule is exact to machine precision on these
integrands with no change of variable, and so that c2 = 1 + t^2 takes the same
value at both ends -- which is exactly what the periodic boundary condition (4)
requires.  Derivatives are supplied analytically, never by finite differences,
so a residual of 1e-15 really is zero and the identity checks are not
approximate; the only differences taken anywhere are the two at the top that
check the hand-written derivatives against the functions they came from.

One deliberate drawing decision, beat 6.  Lemma 6.2 says T is formally
self-adjoint exactly when c1 = c2', and the obvious picture is to plot c1 and
c2' for a self-adjoint example and a non-self-adjoint one.  But in the
self-adjoint example those two are literally the same function, so that picture
draws one curve twice and nobody watching can tell whether the coincidence is
the theorem or a bug in the lesson.  The screen plots the difference c1 - c2'
instead: one example is the constant zero and the other is the line 1 - 2t,
genuinely two curves.  The coincidence that matters is carried by numbers --
the table prints c2' and the two c1 side by side at four sample points -- rather
than by two strokes landing on each other.
"""
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

A, B = -1.0, 1.0                            # the interval, and the Gauss rule's own
NODES, WTS = np.polynomial.legendre.leggauss(220)


def ip(u, v):
 """The scalar product (u, v) = int_a^b u v dt that the section is built on."""
 return float(np.dot(WTS, np.asarray(u(NODES)) * np.asarray(v(NODES))))


def sup(f, n=801):
 ts = np.linspace(A, B, n)
 return float(np.max(np.abs(np.asarray(f(ts), dtype=float))))


def poly(p, k=0):
 """t -> the kth derivative of the polynomial with coefficients p, lowest first."""
 c = list(map(float, p))
 for _ in range(k):
  c = [i * c[i] for i in range(1, len(c))]
 if not c:
  return lambda t: 0.0 * np.asarray(t, dtype=float)
 return lambda t: sum(c[i] * np.asarray(t, dtype=float) ** i for i in range(len(c)))


# ── the two test functions, with their derivatives written out ────────
# Nothing below is differenced numerically: every derivative is the exact one,
# so a residual of 1e-15 in the identity checks means the identity holds.
FD = [lambda t: np.sin(1.3 * t) + 0.4 * np.asarray(t, float) ** 2,
      lambda t: 1.3 * np.cos(1.3 * t) + 0.8 * np.asarray(t, float),
      lambda t: -1.69 * np.sin(1.3 * t) + 0.8 + 0.0 * np.asarray(t, float),
      lambda t: -2.197 * np.cos(1.3 * t),
      lambda t: 2.8561 * np.sin(1.3 * t)]
GD = [lambda t: np.cos(1.7 * t) + 0.3 * np.asarray(t, float),
      lambda t: -1.7 * np.sin(1.7 * t) + 0.3 + 0.0 * np.asarray(t, float),
      lambda t: -2.89 * np.cos(1.7 * t),
      lambda t: 4.913 * np.sin(1.7 * t),
      lambda t: 8.3521 * np.cos(1.7 * t)]
_H = 1e-5
assert max(abs(float(FD[k](t + _H) - FD[k](t - _H)) / (2 * _H) - float(FD[k + 1](t)))
           for k in range(4) for t in (-0.7, 0.2, 0.9)) < 1e-7, \
    "each hand-written derivative of f really is the derivative of the one above it"
assert max(abs(float(GD[k](t + _H) - GD[k](t - _H)) / (2 * _H) - float(GD[k + 1](t)))
           for k in range(4) for t in (-0.7, 0.2, 0.9)) < 1e-7, \
    "and the same for g, so everything below rests on exact derivatives"

# ── beats 3 and 4: n integrations by parts, and the leading sign ──────
# int f^(n) g  -  (-1)^n int f g^(n)  =  sum_j (-1)^j f^(n-1-j) g^(j) |_a^b
PARTS = []
for _n in (1, 2, 3, 4):
 _lhs = ip(FD[_n], GD[0]) - (-1.0) ** _n * ip(FD[0], GD[_n])
 _bdy = sum((-1.0) ** j * (float(FD[_n - 1 - j](B)) * float(GD[j](B))
                           - float(FD[_n - 1 - j](A)) * float(GD[j](A)))
            for j in range(_n))
 # R and T are built as functions and subtracted pointwise, not filled in by
 # parity: for the leading term alone, T g = g^(n) and R g = (-1)^n g^(n), so
 # the sup of their difference is what decides whether R can equal T at all.
 _Tg = (lambda x, k=_n: np.asarray(GD[k](x), float))
 _Rg = (lambda x, k=_n: (-1.0) ** k * np.asarray(GD[k](x), float))
 PARTS.append((_n, _lhs, _bdy, abs(_lhs - _bdy),
               sup(lambda x, R=_Rg, T=_Tg: R(x) - T(x))))
assert all(d < 1e-12 for _n, _l, _b, d, _s in PARTS), \
    "repeating integration by parts moves every derivative across and leaves exactly the endpoint sum"
assert all(s < 1e-15 for n, _l, _b, _d, s in PARTS if n % 2 == 0), \
    "at even order R and T agree as functions, so formal self-adjointness is not ruled out"
assert all(s > 1.0 for n, _l, _b, _d, s in PARTS if n % 2 == 1), \
    "at odd order they differ by twice the derivative, so no odd-order operator is formally self-adjoint"
LEAD1 = sup(GD[1])
assert LEAD1 > 0.5, \
    "at order one the formal adjoint is minus the derivative, a genuinely different operator"

# ── beats 5 and 6: the second-order operator ──────────────────────────
C2 = [lambda t: 1.0 + np.asarray(t, float) ** 2,
      lambda t: 2.0 * np.asarray(t, float),
      lambda t: 2.0 + 0.0 * np.asarray(t, float)]
C0 = -1.0
SA = [lambda t: 2.0 * np.asarray(t, float),                   # c1 = c2', self-adjoint
      lambda t: 2.0 + 0.0 * np.asarray(t, float)]
NS = [lambda t: 1.0 + 0.0 * np.asarray(t, float),             # c1 = 1, not self-adjoint
      lambda t: 0.0 * np.asarray(t, float)]


def top(c1, d, c0=C0):
 """T d = c2 d'' + c1 d' + c0 d, for d a list of a function and its derivatives."""
 return lambda t: C2[0](t) * d[2](t) + c1[0](t) * d[1](t) + c0 * d[0](t)


def rop(c1, d, c0=C0):
 """R d = (c2 d)'' - (c1 d)' + c0 d, with the Leibniz expansion carried out."""
 return lambda t: (C2[0](t) * d[2](t) + (2.0 * C2[1](t) - c1[0](t)) * d[1](t)
                   + (C2[2](t) - c1[1](t) + c0) * d[0](t))


def bform(c1, f, g):
 """B(f, g) = c2 (f' g - g' f) + (c1 - c2') f g, as a function of t."""
 return lambda t: (C2[0](t) * (f[1](t) * g[0](t) - g[1](t) * f[0](t))
                   + (c1[0](t) - C2[1](t)) * f[0](t) * g[0](t))


def bjump(c1, f, g):
 b = bform(c1, f, g)
 return float(b(B)) - float(b(A))


SA_GAP = sup(lambda t: rop(SA, GD)(t) - top(SA, GD)(t))
NS_GAP = sup(lambda t: rop(NS, GD)(t) - top(NS, GD)(t))
NS_SHAPE = sup(lambda t: rop(NS, GD)(t) - top(NS, GD)(t)
               - ((4.0 * np.asarray(t, float) - 2.0) * GD[1](t) + 2.0 * GD[0](t)))
assert SA_GAP < 1e-13, "with c1 = c2' the formal adjoint R is the operator T itself"
assert NS_GAP > 1.0, "with c1 = 1 it is not: R and T disagree by a visible amount"
assert NS_SHAPE < 1e-13, \
    "and they disagree by (2c2' - 2c1) g' + (c2'' - c1') g, which for these coefficients is (4t - 2) g' + 2 g"

IDS = []
for _nm, _c1 in (("sa", SA), ("ns", NS)):
 _l = ip(top(_c1, FD), GD[0]) - ip(FD[0], rop(_c1, GD))
 _r = bjump(_c1, FD, GD)
 IDS.append((_nm, _l, _r, abs(_l - _r)))
assert all(d < 1e-12 for _nm, _l, _r, d in IDS), \
    "(Tf, g) - (f, Rg) is the jump of B across the two ends, whether or not T is self-adjoint"
assert min(abs(v) for _nm, v, _r, _d in IDS) > 0.1, \
    "and neither side is accidentally zero for these f and g, so the check has content"

TSHOW = (-1.0, -0.4, 0.3, 1.0)
COEF = [(t, float(C2[1](t)), float(SA[0](t)), float(NS[0](t))) for t in TSHOW]
DSA = sup(lambda t: SA[0](t) - C2[1](t))
DNS = sup(lambda t: NS[0](t) - C2[1](t))
assert DSA < 1e-15, "c1 - c2' vanishes identically for the self-adjoint example"
assert DNS > 2.0, \
    "and is the line 1 - 2t for the other one, so the two plotted differences are not the same curve"

# ── beat 8: the four self-adjoint boundary conditions ─────────────────
K3, KB3 = 0.5, -1.2                         # f'(a) = k f(a),  f'(b) = c f(b)
_M3 = np.array([[-K3, 1.0 + K3, -2.0 - K3, 3.0 + K3],
                [-KB3, 1.0 - KB3, 2.0 - KB3, 3.0 - KB3]])
_u3, _s3, _v3 = np.linalg.svd(_M3)
assert _s3[1] > 1e-6, "the two endpoint conditions of case (3) are independent"
CUB = [[poly(_v3[2], k) for k in range(3)], [poly(_v3[3], k) for k in range(3)]]

PAIRS = [
 ("1", [lambda t: 1.0 - np.asarray(t, float) ** 2,
        lambda t: -2.0 * np.asarray(t, float),
        lambda t: -2.0 + 0.0 * np.asarray(t, float)],
       [lambda t: np.asarray(t, float) - np.asarray(t, float) ** 3,
        lambda t: 1.0 - 3.0 * np.asarray(t, float) ** 2,
        lambda t: -6.0 * np.asarray(t, float)]),
 ("2", [lambda t: np.asarray(t, float) ** 3 - 3.0 * np.asarray(t, float),
        lambda t: 3.0 * np.asarray(t, float) ** 2 - 3.0,
        lambda t: 6.0 * np.asarray(t, float)],
       [lambda t: np.cos(math.pi * np.asarray(t, float)),
        lambda t: -math.pi * np.sin(math.pi * np.asarray(t, float)),
        lambda t: -math.pi ** 2 * np.cos(math.pi * np.asarray(t, float))]),
 ("3", CUB[0], CUB[1]),
 ("4", [lambda t: np.cos(math.pi * np.asarray(t, float)),
        lambda t: -math.pi * np.sin(math.pi * np.asarray(t, float)),
        lambda t: -math.pi ** 2 * np.cos(math.pi * np.asarray(t, float))],
       [lambda t: np.sin(math.pi * np.asarray(t, float)),
        lambda t: math.pi * np.cos(math.pi * np.asarray(t, float)),
        lambda t: -math.pi ** 2 * np.sin(math.pi * np.asarray(t, float))]),
]
OUT = ([lambda t: 1.0 + np.asarray(t, float),
        lambda t: 1.0 + 0.0 * np.asarray(t, float),
        lambda t: 0.0 * np.asarray(t, float)],
       [lambda t: np.exp(np.asarray(t, float))] * 3)

assert max(abs(float(h(x))) for h in (PAIRS[0][1][0], PAIRS[0][2][0]) for x in (A, B)) < 1e-13, \
    "case (1): both functions of the pair vanish at a and at b"
assert max(abs(float(h(x))) for h in (PAIRS[1][1][1], PAIRS[1][2][1]) for x in (A, B)) < 1e-13, \
    "case (2): both derivatives of the pair vanish at a and at b"
assert max(abs(float(h[1](A)) - K3 * float(h[0](A))) for h in CUB) < 1e-12 \
   and max(abs(float(h[1](B)) - KB3 * float(h[0](B))) for h in CUB) < 1e-12, \
    "case (3): each function's slope at an end is the prescribed multiple of its value there"
assert abs(float(C2[0](A)) - float(C2[0](B))) < 1e-15, \
    "case (4) needs c2 to agree at the two ends, which is why 1 + t^2 is used on [-1, 1]"
assert max(abs(float(h[k](A)) - float(h[k](B)))
           for h in (PAIRS[3][1], PAIRS[3][2]) for k in (0, 1)) < 1e-13, \
    "case (4): value and slope match periodically for both functions of the pair"

BJ = [(nm, bjump(SA, f, g)) for nm, f, g in PAIRS]
BJOUT = bjump(SA, OUT[0], OUT[1])
assert all(abs(v) < 1e-12 for _nm, v in BJ), \
    "all four conditions make B vanish across the ends, which is what makes them self-adjoint"
assert abs(BJOUT) > 1.0, \
    "while a pair satisfying none of them leaves B nonzero, so the four conditions are doing work"
SELF = [(ip(top(SA, f), g[0]), ip(f[0], top(SA, g))) for _nm, f, g in PAIRS]
assert all(abs(x - y) < 1e-12 for x, y in SELF), \
    "so on each of those M the operator moves across the scalar product unchanged"
GEN = (ip(top(SA, FD), GD[0]), ip(FD[0], top(SA, GD)))
assert abs(GEN[0] - GEN[1] - bjump(SA, FD, GD)) < 1e-12, \
    "while for a pair outside M the two sides differ by exactly that jump of B"
NORM = [sup(f[0]) for _nm, f, _g in PAIRS]
assert min(NORM) > 0.2, \
    "every drawn representative is a nonzero function, so scaling it to the row height is safe"

# ── beat 9: Lemma 6.3, the map f -> <l1 f, l2 f> restricted to N ──────
# T f = f'' - f is formally self-adjoint (c2 = 1, c1 = 0 = c2', c0 = -1) and its
# null space is spanned by the two exponentials, so the map is a 2 x 2 matrix.
NBAS = [[lambda t: np.exp(np.asarray(t, float))] * 3,
        [lambda t: np.exp(-np.asarray(t, float)),
         lambda t: -np.exp(-np.asarray(t, float)),
         lambda t: np.exp(-np.asarray(t, float))]]
assert max(sup(lambda t, h=h: h[2](t) - h[0](t)) for h in NBAS) < 1e-12, \
    "both basis functions really do solve f'' - f = 0"
LFUN = (("1", lambda h: float(h[0](A)), lambda h: float(h[0](B))),
        ("2", lambda h: float(h[1](A)), lambda h: float(h[1](B))),
        ("4", lambda h: float(h[0](A)) - float(h[0](B)),
              lambda h: float(h[1](A)) - float(h[1](B))))
DET = [(nm, float(np.linalg.det(np.array([[l1(h) for h in NBAS], [l2(h) for h in NBAS]]))))
       for nm, l1, l2 in LFUN]
assert all(abs(d) > 1e-6 for _nm, d in DET), \
    "for each condition the map from the two-dimensional N to R^2 is injective, hence onto"

# ── beat 10: T - lambda, and the lambda that are not allowed ──────────
def shoot(lam):
 """f(b) for the solution of f'' - f - lam f = 0 with f(a) = 0, f'(a) = 1.

 T - lam is injective on the case-(1) M exactly when this does not vanish."""
 s = 1.0 + lam
 if s > 1e-9:
  mu = math.sqrt(s)
  return math.sinh(2.0 * mu) / mu
 if s < -1e-9:
  nu = math.sqrt(-s)
  return math.sin(2.0 * nu) / nu
 return 2.0


LBAD = [-1.0 - (k * math.pi / 2.0) ** 2 for k in (1, 2, 3)]
LGOOD = (0.0, 1.0, 4.0)
LA, LB = -12.0, 1.0
LMARK = [l for l in LBAD if LA <= l <= LB]
assert all(abs(shoot(l)) < 1e-12 for l in LBAD), \
    "the shooting function vanishes exactly at lambda = -1 - (k pi / 2)^2"
assert all(abs(shoot(l)) > 1.0 for l in LGOOD), \
    "and not at the lambda the next lemma will want, so T - lambda stays injective on M there"
assert shoot(LBAD[0] + 0.3) * shoot(LBAD[0] - 0.3) < 0.0, \
    "it changes sign there, so the exceptional lambda are isolated points, not an interval"
assert len(LMARK) == 2, "two of those points fall inside the plotted range of lambda"
LSPAN = max(abs(shoot(LA + (LB - LA) * k / 400.0)) for k in range(401))
assert LSPAN > 3.0, "and the plotted range of the shooting function is tall enough to read"


class AdvCalcE82Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 82

 MODE_LABEL = {
  0: {"zh": "邊界值問題：資料換了位置", "en": "the boundary-value problem: the data moves"},
  1: {"zh": "同樣想拆成兩個子問題", "en": "the same split into two subproblems"},
  2: {"zh": "換個觀點：純量積與自伴", "en": "a new viewpoint: scalar products and self-adjointness"},
  3: {"zh": "分部積分把導數搬過去", "en": "integration by parts moves the derivatives across"},
  4: {"zh": "形式伴隨，以及 n 的奇偶", "en": "the formal adjoint, and the parity of n"},
  5: {"zh": "二階的情形算出來", "en": "the second-order case, computed"},
  6: {"zh": "引理 6.2：形式自伴的判準", "en": "Lemma 6.2: the test for formal self-adjointness"},
  7: {"zh": "引理 6.1：換成邊界條件", "en": "Lemma 6.1: trade it for a boundary condition"},
  8: {"zh": "四組自伴邊界條件", "en": "four self-adjoint boundary conditions"},
  9: {"zh": "引理 6.3：補空間換成單射", "en": "Lemma 6.3: complement becomes injective"},
  10: {"zh": "收尾：把 T 換成 T 減 λ", "en": "closing: replacing T by T minus lambda"},
 }

 # ── shared pieces, the same ones E79 and E80 use ──────────────────
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
  """A curve over t in [ta, tb], with ta pinned to the figure's left edge."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * float(f(ta + (tb - ta) * k / n)), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 def _ends(self, oy, h=0.10, xl=XL, xr=XR, col=DIM, lab=False, dy=0.30):
  """Tick marks for the two ends of the interval, and optionally their names.

  The names sit outside [xl, xr], where no plotted curve can reach, so they
  never land on the stroke they are describing."""
  g = VGroup(Line([xl, oy - h, 0], [xl, oy + h, 0], color=col, stroke_width=2.0),
             Line([xr, oy - h, 0], [xr, oy + h, 0], color=col, stroke_width=2.0))
  if lab:
   g.add(self._sym(oy - dy, "a", col, FS_TAG - 3, x=xl - 0.20, w=0.30),
         self._sym(oy - dy, "b", col, FS_TAG - 3, x=xr + 0.26, w=0.30))
  return g

 # ── beat 0: where the data sits ─────────────────────────────────
 def _data(self):
  oy = -0.30
  g = VGroup()
  # left panel: one point, a value and a slope
  xa, xb = -5.78, -4.42
  g.add(self._arr([xa - 0.12, oy, 0], [xb + 0.22, oy, 0], DIM, sw=3, tl=0.12))
  g.add(self._plot(lambda t: 0.30 + 0.34 * math.sin(1.9 * t + 0.4), ACCENT_B,
                   A, B, oy, 1.0, sw=2.8, xl=xa, xr=xb))
  tm = (xa + xb) / 2
  ym = oy + 0.30 + 0.34 * math.sin(0.4)
  sl = 0.34 * 1.9 * math.cos(0.4) / ((xb - xa) / 2.0)
  g.add(Line([tm - 0.34, ym - 0.34 * sl, 0], [tm + 0.34, ym + 0.34 * sl, 0],
             color=ACCENT_A, stroke_width=3.0))
  g.add(Dot([tm, ym, 0], radius=0.072, color=ACCENT_A))
  g.add(self._sym(oy - 0.32, "t ₀", DIM, FS_TAG - 2, x=tm, w=0.44))
  g.add(self._sym(1.08, "f ( t ₀ )  ,  f ′ ( t ₀ )", ACCENT_A, FS_TAG - 2,
                  x=tm, w=1.44))
  # right panel: two points, one value at each end
  xc, xd = -3.86, -2.50
  g.add(self._arr([xc - 0.12, oy, 0], [xd + 0.22, oy, 0], DIM, sw=3, tl=0.12))
  g.add(self._plot(lambda t: 0.10 + 0.40 * math.cos(0.5 * math.pi * t) + 0.30 * t,
                   ACCENT_C, A, B, oy, 1.0, sw=2.8, xl=xc, xr=xd))
  for x0, v in ((xc, -0.20), (xd, 0.40)):
   g.add(self._dash([x0, oy, 0], [x0, oy + v, 0], DIM, n=4, sw=1.4))
   g.add(Dot([x0, oy + v, 0], radius=0.072, color=ACCENT_A))
  g.add(self._sym(oy - 0.38, "a", DIM, FS_TAG - 2, x=xc, w=0.34),
        self._sym(oy - 0.38, "b", DIM, FS_TAG - 2, x=xd, w=0.34))
  g.add(self._sym(1.08, "f ( a )  ,  f ( b )", ACCENT_A, FS_TAG - 2,
                  x=(xc + xd) / 2, w=1.40))
  g.add(self._sym(0.62, "↔", DIM, FS_TAG + 2, x=-4.14, w=0.44))
  g.add(self._table((("T ( f )   =   g            T   :   𝒞 ²   →   𝒞 ⁰", ACCENT_A),
                     ("I   =   [ a , b ]            ∂ I   =   { a , b }", ACCENT_C),
                     ("f ( t ₀ )  ,  f ′ ( t ₀ )          ⇒        § 2  –  § 5", ACCENT_B),
                     ("f ( a )  ,  f ( b )                  ⇒        § 6", ACCENT_A),
                     (f"a   =   {A:+.0f}              b   =   {B:+.0f}", DIM)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("左邊一個點上給兩個數，右邊兩個點上各給一個",
                  "two numbers at one point on the left, one at each of two points on the right"))
  return g.add(self._foot("要解的還是 T 作用在 f 上等於 g，但給定的條件換了位置：初值問題在同一個點上給值與斜率，邊值問題在區間兩端各給一個值",
                          "the equation is still T of f equals g, but the data moves: the initial-value problem gives a value and a slope at one point, the boundary-value problem one value at each end",
                          ACCENT_A,
                          "物理裡最重要的那些問題幾乎都是後面這一種。書上說它看起來很像前面那種，性格卻完全不同",
                          "most of the important problems in physics are of the second kind, and the book says it looks like the first while being of a wholly different character"))

 # ── beat 1: the same split, and why it is not available ─────────
 def _split(self):
  g = VGroup()
  g.add(self._box(-4.20, 0.86, "𝒞 ² [ a , b ]", ACCENT_B, w=2.30, h=0.52, size=FS_TAG))
  g.add(self._box(-5.14, -0.10, "N ( T )", ACCENT_C, w=1.32, h=0.50, size=FS_TAG))
  g.add(self._box(-3.26, -0.10, "M", ACCENT_A, w=1.32, h=0.50, size=FS_TAG))
  g.add(self._sym(-0.10, "⊕", DIM, FS_TAG + 1, x=-4.20, w=0.40))
  g.add(self._arr([-4.62, 0.56, 0], [-5.14, 0.18, 0], DIM, sw=3, tl=0.12))
  g.add(self._arr([-3.78, 0.56, 0], [-3.26, 0.18, 0], DIM, sw=3, tl=0.12))
  g.add(self._sym(-0.64, "?", WARN, FS_TAG + 4, x=-4.20, w=0.34))
  g.add(self._sym(-1.02, "M   =   { f  :  f ( a )  =  f ( b )  =  0 }", ACCENT_A,
                  FS_TAG - 2, x=-4.20, w=3.30))
  g.add(self._table((("T f  =  g            T f ₀  =  g  ,  f ₀ ∈ M", ACCENT_A),
                     ("f   =   f ₀   +   h            h  ∈  N ( T )", ACCENT_B),
                     ("M   ⊕   N ( T )   =   𝒞 ² [ a , b ]   ?", WARN),
                     ("dim N ( T )   =   2", ACCENT_C),
                     ("§ 2  –  § 5            ⇒            ?", DIM)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("紅色那一列就是沒有辦法回答的那一句",
                  "the red row is the one question the old theory cannot answer"))
  return g.add(self._foot("看起來也能像初值問題那樣拆成兩個子問題：只要那個在兩端都歸零的集合 M 恰好是零化空間的補空間就行",
                          "it looks as though this splits into two subproblems the same way, provided the set of functions vanishing at both ends is a complement of the null space",
                          ACCENT_A,
                          "可是書上提醒，從初值那一套理論完全看不出該怎麼判斷它是不是補空間，得另外造一套工具",
                          "but the book warns that the initial-value development gives no clue how to decide that, and that wholly new tools have to be devised"))

 # ── beat 2: the route through the scalar product ────────────────
 def _route(self):
  g = VGroup()
  xa, xb, ya, yb = -5.14, -3.26, 0.60, -0.38
  g.add(self._box(xa, ya, "( f , g )", ACCENT_B, w=1.52, h=0.50, size=FS_TAG))
  g.add(self._box(xb, ya, "R   =   T", ACCENT_A, w=1.52, h=0.50, size=FS_TAG))
  g.add(self._box(xb, yb, "S   =   S *", ACCENT_C, w=1.52, h=0.50, size=FS_TAG))
  g.add(self._box(xa, yb, "Ch 5  ,  5.1", DIM, w=1.52, h=0.50, size=FS_TAG - 2))
  g.add(self._arr([xa + 0.80, ya, 0], [xb - 0.80, ya, 0], DIM, sw=3, tl=0.11))
  g.add(self._arr([xb, ya - 0.29, 0], [xb, yb + 0.29, 0], DIM, sw=3, tl=0.12))
  g.add(self._arr([xb - 0.80, yb, 0], [xa + 0.80, yb, 0], DIM, sw=3, tl=0.11))
  g.add(self._sym((ya + yb) / 2, "M", DIM, FS_TAG - 2, x=xb + 0.36, w=0.36))
  g.add(self._sym(1.12, "( f , g )   =   ∫ ᵃ ᵇ  f g  d t", ACCENT_B, FS_TAG - 2,
                  x=-4.20, w=2.80))
  g.add(self._sym(-0.96, "T  ∘  S   =   I            S  :  𝒞 ⁰  →  M", ACCENT_A,
                  FS_TAG - 2, x=-4.20, w=3.30))
  g.add(self._table((("( f , g )   =   ∫ ᵃ ᵇ  f g  d t", ACCENT_B),
                     ("R   =   T              ⇒          ∃  M", ACCENT_A),
                     ("S   :   𝒞 ⁰   →   M            T ∘ S   =   I", ACCENT_C),
                     ("S   =   S *", ACCENT_A),
                     ("T f  −  r f  =  0  ,  f ∈ M            Ch 5  ,  5.1", DIM)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("第四列是關鍵：右逆同時是自伴的與緊的",
                  "the fourth row is the point: the right inverse is both self-adjoint and compact"))
  return g.add(self._foot("新工具是純量積與自伴算子。把兩個函數的乘積從 a 積到 b，當成它們的內積",
                          "the new tools are the scalar product and the theory of self-adjoint operators: integrate the product of two functions from a to b",
                          ACCENT_A,
                          "如果 T 在這個內積下自伴，適當選的 M 會讓右逆同時是自伴而且緊的，第 5 章定理 5.1 就能原封不動地搬過來用",
                          "if T is self-adjoint for that product, a suitable M makes the right inverse self-adjoint and compact, and Theorem 5.1 of chapter 5 applies unchanged"))

 # ── beat 3: integration by parts, one derivative at a time ──────
 def _parts(self):
  xi, xe = -5.10, -2.95
  g = VGroup(self._sym(1.14, "∫ ᵃ ᵇ", DIM, FS_TAG - 2, x=xi, w=0.66),
             self._sym(1.14, "[  ·  ] ᵃ ᵇ", DIM, FS_TAG - 2, x=xe, w=0.90))
  rows = (("c ₂ f ″ g", "", ACCENT_A),
          ("−  f ′ ( c ₂ g ) ′", "+  c ₂ f ′ g", ACCENT_B),
          ("+  f ( c ₂ g ) ″", "−  f ( c ₂ g ) ′", ACCENT_C))
  ys = (0.68, 0.06, -0.56)
  for y, (li, ri, col) in zip(ys, rows):
   g.add(self._sym(y, li, col, FS_TAG - 2, x=xi, w=1.50))
   if ri:
    g.add(self._sym(y, ri, col, FS_TAG - 2, x=xe, w=1.50))
  for ya, yb in zip(ys, ys[1:]):
   g.add(self._arr([-6.05, ya - 0.10, 0], [-6.05, yb + 0.10, 0], DIM, sw=3, tl=0.11))
  g.add(self._sym(-1.00, "( T f , g )   =   ( f , R g )   +   B | ᵃ ᵇ", ACCENT_A,
                  FS_TAG - 2, x=-4.10, w=3.40))
  g.add(self._table((("∫ ᵃ ᵇ  f ′ g   =   f g | ᵃ ᵇ   −   ∫ ᵃ ᵇ  f g ′", ACCENT_A),
                     ("    n        ∫ f ⁽ ⁿ ⁾ g  −  ( − 1 ) ⁿ ∫ f g ⁽ ⁿ ⁾            [  ·  ] ᵃ ᵇ",
                      DIM),)
                    + tuple((f"    {n}              {l:+9.5f}                {b:+9.5f}", ACCENT_B)
                            for n, l, b, _d, _s in PARTS)
                    + ((f"max | Δ |        {max(d for _n, _l, _b, d, _s in PARTS):.1e}", ACCENT_C),
                       ("B ( f , g ) | ᵃ ᵇ   =   Σ  k ᵢ ⱼ  f ⁽ ⁱ ⁾ g ⁽ ʲ ⁾ | ᵃ ᵇ", ACCENT_A)),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("中間一欄與右邊一欄逐列相等，第三列的數值最大",
                  "the middle and right columns agree row by row, and the third row carries the largest value"))
  return g.add(self._foot("用分部積分，把 f 身上的導數一次搬一個到 g 身上。搬完以後 f 不帶導數，g 被某個 n 階算子 R 作用著",
                          "integration by parts shifts the derivatives off f onto g one at a time; at the end f carries none and g is acted on by an operator R of order n",
                          ACCENT_A,
                          "每一步在端點留下的值累積成一個 B。於是 T f 與 g 的內積，等於 f 與 R g 的內積加上 B 在兩端的差",
                          "the endpoint evaluations accumulate into a quantity B, so the product of T f with g is the product of f with R g plus the jump of B across the ends"))

 # ── beat 4: the formal adjoint and the parity of n ──────────────
 def _parity(self):
  oy, sy = -0.10, 0.30
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._ends(oy, lab=True))
  g.add(self._plot(lambda t: float(GD[1](t)), ACCENT_A, A, B, oy, sy, sw=3.0))
  g.add(self._plot(lambda t: -float(GD[1](t)), ACCENT_C, A, B, oy, sy, sw=3.0))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "T g   =   g ′", 1.20),
                                 (ACCENT_C, "R g   =   −  g ′", 1.50)), y0=1.14, dy=0.25))
  g.add(self._table((("T f  =  Σ ᵢ  a ᵢ f ⁽ ⁱ ⁾        R g  =  Σ ᵢ ( − 1 ) ⁱ ( a ᵢ g ) ⁽ ⁱ ⁾",
                      ACCENT_A),
                     ("    n            ( − 1 ) ⁿ              ‖ R g  −  T g ‖", DIM),)
                    + tuple((f"    {n}              {-1 if n % 2 else 1:+d}                "
                             f"{s:.3f}", WARN if n % 2 else ACCENT_B)
                            for n, _l, _b, _d, s in PARTS)
                    + ((f"n  =  2 k + 1          ‖ g ′ ‖   =   {LEAD1:.4f}", ACCENT_C),
                       ("R   =   T            ⇒            n   =   2 k", ACCENT_A)),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("紅的兩列是奇數階，最後一欄不是零",
                  "the two red rows are the odd orders, where the last column is not zero"))
  return g.add(self._foot("R 叫做 T 的形式伴隨；如果 R 剛好就是 T，就說 T 是形式自伴的。每做一次分部積分都帶一個負號",
                          "R is called the formal adjoint of T, and if R is T itself we say T is formally self-adjoint; every integration by parts introduces one sign change",
                          ACCENT_A,
                          "所以 R 的首項係數是負一的 n 次方乘上 T 的。要讓兩個算子連最高階那一項都對得起來，n 就必須是偶數。圖上是一階的情形",
                          "so the leading coefficient of R is minus one to the n times that of T, and for the two to share even their first terms n has to be even; the figure is the case of order one"))

 # ── beat 5: the second-order formulas, checked ──────────────────
 def _second(self):
  oy, sy = -0.14, 0.52
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._ends(oy, lab=True))
  g.add(self._plot(lambda t: float(FD[0](t)), ACCENT_A, A, B, oy, sy, sw=3.0))
  g.add(self._plot(lambda t: float(GD[0](t)), ACCENT_C, A, B, oy, sy, sw=3.0))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "f", 0.36), (ACCENT_C, "g", 0.36)),
                     y0=1.14, dy=0.25))
  g.add(self._table((("R g   =   ( c ₂ g ) ″  −  ( c ₁ g ) ′  +  c ₀ g", ACCENT_A),
                     ("B   =   c ₂ ( f ′ g − g ′ f )  +  ( c ₁ − c ₂ ′ ) f g", ACCENT_A),
                     ("c ₂   =   1 + t ²            c ₀   =   − 1", ACCENT_C),
                     ("    c ₁            ( T f , g ) − ( f , R g )            B | ᵃ ᵇ", DIM),)
                    + tuple((f"    {lab}          {l:+9.5f}              {r:+9.5f}", col)
                            for (lab, col), (_nm, l, r, _d)
                            in zip((("2 t", ACCENT_B), ("1  ", WARN)), IDS))
                    + ((f"max | Δ |          {max(d for _n, _l, _r, d in IDS):.1e}", ACCENT_C),
                       (f"‖ R g − T g ‖        {SA_GAP:.1e}          {NS_GAP:.4f}", ACCENT_A)),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("兩組 c 一都讓那個等式成立，但只有上面那組 R 等於 T",
                  "both choices of c one satisfy the identity; only the upper one has R equal to T"))
  return g.add(self._foot("以下只看二階。T f 是 c 二乘 f 兩撇加 c 一乘 f 一撇加 c 零乘 f；分部積分兩次後就得到 R 與 B 的公式",
                          "from here on only the second-order case: T f is c two f double prime plus c one f prime plus c zero f, and two integrations by parts give the formulas for R and B",
                          ACCENT_A,
                          "圖上兩條就是右表那兩欄數字所用的 f 與 g。端點項整理起來是 c 二乘 f 一撇 g 減 g 一撇 f，再加 c 一減 c 二一撇乘 f g",
                          "the two curves are the f and g the table's numbers were computed from; the endpoint part is c two times f prime g minus g prime f, plus c one less c two prime times f g"))

 # ── beat 6: Lemma 6.2, drawn as the difference ──────────────────
 def _lemma62(self):
  oy, sy = -0.10, 0.28
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=1.6, tl=0.12))
  g.add(self._ends(oy, h=0.08, lab=True))
  # The self-adjoint example's difference is identically zero, so it lies along
  # the axis: drawn thick, in colour, with its own sample dots, so that nobody
  # has to guess whether a curve is there at all.
  for c1, col, sw in ((SA, ACCENT_A, 5.0), (NS, ACCENT_C, 3.0)):
   g.add(self._plot(lambda t, c1=c1: float(c1[0](t)) - float(C2[1](t)),
                    col, A, B, oy, sy, sw=sw))
   for t0 in TSHOW:
    g.add(Dot([self._xof(t0, A, B),
               oy + sy * (float(c1[0](t0)) - float(C2[1](t0))), 0],
              radius=0.062, color=col))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "c ₁ − c ₂ ′   =   0", 1.70),
                                 (ACCENT_C, "c ₁ − c ₂ ′   =   1 − 2 t", 2.20)),
                     y0=1.14, dy=0.25))
  g.add(self._table((("R  =  T    ⟺    c ₁  =  c ₂ ′          T f  =  ( c ₂ f ′ ) ′ + c ₀ f",
                      ACCENT_A),
                     ("    t              c ₂ ′            c ₁ : 2 t            c ₁ : 1", DIM),)
                    + tuple((f"  {t:+.1f}            {d:+.2f}            {s:+.2f}"
                             f"            {n:+.2f}", ACCENT_B) for t, d, s, n in COEF)
                    + ((f"‖ c ₁ − c ₂ ′ ‖          {DSA:.1e}          {DNS:.3f}", ACCENT_C),
                       ("c ᵢ ′  =  0      ⇒      R  =  T   ⟺   c ₁  =  0", ACCENT_A)),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("第三欄與第二欄逐列相同，第四欄不同",
                  "the third column repeats the second row by row; the fourth does not"))
  return g.add(self._foot("引理 6.2：二階算子形式自伴，若且唯若 c 一等於 c 二一撇。這時 T f 可以寫成 c 二 f 一撇的導數再加 c 零 f",
                          "Lemma 6.2: a second-order operator is formally self-adjoint exactly when c one is the derivative of c two, and then T f is the derivative of c two f prime plus c zero f",
                          ACCENT_A,
                          "畫的是兩個例子各自的 c 一減 c 二一撇：自伴那組恆為零，另一組是一條斜線。原來那兩條曲線疊起來會分不出有幾條，所以改畫這個差",
                          "the screen plots c one less c two prime for the two examples: identically zero for one, a sloping line for the other, because the two original curves would coincide and could not be told from one"))

 # ── beat 7: Lemma 6.1 ───────────────────────────────────────────
 def _lemma61(self):
  g = VGroup()
  xa, xb, yy = -5.14, -3.26, 0.76
  g.add(self._box(xa, yy, "u  ,  v", ACCENT_B, w=1.40, h=0.50, size=FS_TAG))
  g.add(self._box(xb, yy, "f  ,  g", ACCENT_A, w=1.40, h=0.50, size=FS_TAG))
  g.add(self._arr([xa + 0.74, yy, 0], [xb - 0.74, yy, 0], DIM, sw=3, tl=0.11))
  g.add(self._sym(yy + 0.30, "S", DIM, FS_TAG - 2, x=(xa + xb) / 2, w=0.34))
  g.add(self._sym(yy - 0.46, "𝒞 ⁰", DIM, FS_TAG - 3, x=xa, w=0.56),
        self._sym(yy - 0.46, "M", DIM, FS_TAG - 3, x=xb, w=0.40))
  for y, s, col in ((-0.10, "( u , S v )   =   ( T f , g )", ACCENT_B),
                    (-0.52, "=   ( f , T g )   +   B | ᵃ ᵇ", ACCENT_A),
                    (-0.94, "=   ( S u , v )   +   B | ᵃ ᵇ", ACCENT_C)):
   g.add(self._sym(y, s, col, FS_TAG - 2, x=-4.05, w=3.20))
  g.add(self._table((("T f  =  u        T g  =  v        R  =  T", ACCENT_A),
                     ("S  =  S *      ⟺      B ( f , g ) | ᵃ ᵇ   =   0", ACCENT_A),
                     ("                ( T f , g )              ( f , T g )", DIM),)
                    + tuple((f"    ( {nm} )          {x:+9.5f}            {y:+9.5f}", ACCENT_B)
                            for (nm, _v), (x, y) in zip(BJ, SELF))
                    + ((f"    f , g          {GEN[0]:+9.5f}            {GEN[1]:+9.5f}", WARN),),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("前四列兩欄相等，紅的那一列差了一個不為零的 B",
                  "the two columns agree on the first four rows; on the red one they differ by a B that is not zero"))
  return g.add(self._foot("引理 6.1 把算子的性質換成邊界條件的性質。設 T 形式自伴，M 是零化空間的補空間",
                          "Lemma 6.1 trades a property of the operator for a property of the boundary condition: let T be formally self-adjoint and M a complement of the null space",
                          ACCENT_A,
                          "那麼 M 決定的右逆是自伴算子，若且唯若 M 裡任意兩個函數的 B 在兩端的差都是零。推導只有一行，自伴那一項自動相消",
                          "then the right inverse determined by M is self-adjoint exactly when B vanishes across the ends for every pair in M; expanding both products cancels the self-adjoint term"))

 # ── beat 8: the four conditions, as four interval sketches ──────
 def _four(self):
  xl, xr = -5.52, -2.50
  g = VGroup()
  ys = (0.94, 0.30, -0.34, -0.92)
  tags = ("( 1 )", "( 2 )", "( 3 )", "( 4 )")
  cols = (ACCENT_A, ACCENT_B, ACCENT_C, WARN)
  for y, tag, col, (_nm, f, _g), nn in zip(ys, tags, cols, PAIRS, NORM):
   g.add(Line([xl, y, 0], [xr, y, 0], color=DIM, stroke_width=1.2))
   g.add(self._ends(y, h=0.07, xl=xl, xr=xr))
   g.add(self._plot(lambda t, f=f, nn=nn: float(f[0](t)) / nn, col, A, B, y, 0.18,
                    sw=2.6, xl=xl, xr=xr))
   g.add(self._sym(y, tag, col, FS_TAG - 3, x=-6.00, w=0.56))
   for x0 in (xl, xr):
    g.add(Dot([x0, y, 0], radius=0.045, color=DIM))
  g.add(self._sym(1.22, "a", DIM, FS_TAG - 3, x=xl, w=0.30),
        self._sym(1.22, "b", DIM, FS_TAG - 3, x=xr, w=0.30))
  g.add(self._table((("( 1 )   f ( a ) = f ( b ) = 0          ( 2 )   f ′ ( a ) = f ′ ( b ) = 0",
                      ACCENT_A),
                     (f"( 3 )   f ′ ( a ) = k f ( a )  ,  f ′ ( b ) = c f ( b )        "
                      f"k = {K3:+.2f}  ,  c = {KB3:+.2f}", ACCENT_A),
                     ("( 4 )   c ₂ ( a ) = c ₂ ( b )  ,  f ( a ) = f ( b )  ,  f ′ ( a ) = f ′ ( b )",
                      ACCENT_A),)
                    + tuple((f"      ( {nm} )              B | ᵃ ᵇ   =   {v:+.1e}", ACCENT_B)
                            for nm, v in BJ)
                    + ((f"      ( −  )              B | ᵃ ᵇ   =   {BJOUT:+.4f}", WARN),),
                    y0=0.90, dy=0.22, size=FS_TAG - 4))
  g.add(self._cap("每一列畫的是那一組裡的第一個函數；最後一列哪一組都不滿足",
                  "each row draws the first function of that pair, and the last table row satisfies none of them"))
  return g.add(self._foot("於是可以直接寫下好幾組自伴的邊界條件：兩端函數值為零、兩端斜率為零、斜率各自正比於同一端的函數值",
                          "several self-adjoint boundary conditions can now be written down: the function vanishes at both ends, the slope vanishes at both ends, or each slope is proportional to the value at its own end",
                          ACCENT_A,
                          "第四組要 c 二在兩端相等，條件是函數值與斜率都週期性地相等。右表逐組算出來全是零，哪一組都不滿足的那一對就不是",
                          "the fourth asks c two to agree at the ends and the value and slope to match periodically; the table makes all four vanish, and the pair in none of them does not"))

 # ── beat 9: Lemma 6.3 ───────────────────────────────────────────
 def _lemma63(self):
  g = VGroup()
  cx, cy, dx = -5.20, 0.52, -3.10
  corners = ((-0.62, -0.30), (0.22, -0.30), (0.62, 0.30), (-0.22, 0.30))
  for s, t in zip(corners, corners[1:] + corners[:1]):
   g.add(Line([cx + s[0], cy + s[1], 0], [cx + t[0], cy + t[1], 0],
              color=ACCENT_C, stroke_width=2.0))
  g.add(self._arr([dx - 0.45, cy, 0], [dx + 0.45, cy, 0], DIM, sw=2.5, tl=0.11),
        self._arr([dx, cy - 0.45, 0], [dx, cy + 0.45, 0], DIM, sw=2.5, tl=0.11))
  g.add(self._sym(1.12, "N", ACCENT_C, FS_TAG, x=cx, w=0.40),
        self._sym(1.12, "ℝ ²", ACCENT_A, FS_TAG, x=dx, w=0.50))
  g.add(self._arr([-4.40, cy, 0], [-3.70, cy, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(cy + 0.28, "⟨ l ₁ , l ₂ ⟩", ACCENT_A, FS_TAG - 3, x=-4.02, w=1.00))
  g.add(self._sym(-0.32, "N   ∩   M   =   { 0 }", ACCENT_B, FS_TAG - 2, x=-4.15, w=2.40))
  g.add(self._sym(-0.70, "dim N   =   2            N   ≅   ℝ ²", ACCENT_C,
                  FS_TAG - 2, x=-4.15, w=3.10))
  g.add(self._sym(-1.02, "l ( f )  =  k ₁ f ( a ) + k ₂ f ′ ( a ) + k ₃ f ( b ) + k ₄ f ′ ( b )",
                  DIM, FS_TAG - 3, x=-4.15, w=3.50))
  g.add(self._table((("( a )   M ⊕ N = 𝒞 ²        ⟷        ( a ′ )   N ( T ↾ M ) = { 0 }",
                      ACCENT_A),
                     ("T f   =   f ″  −  f              N   =   ⟨ e ᵗ , e ⁻ ᵗ ⟩", ACCENT_C),
                     ("                          det  ⟨ l ₁ , l ₂ ⟩ ↾ N", DIM),)
                    + tuple((f"        ( {nm} )                      {d:+9.4f}", ACCENT_B)
                            for nm, d in DET)
                    + (("Ch 2  ,  2.4                Ch 1  ,  5.3", DIM),),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("三個行列式都不是零，所以那個映射是同構",
                  "none of the three determinants is zero, so each of those maps is an isomorphism"))
  return g.add(self._foot("引理 6.3 說，條件 a「M 是零化空間的補」可以換成 a 一撇「T 限制在 M 上是單射」",
                          "Lemma 6.3 says condition a, that M is a complement of the null space, may be replaced by a prime, that T restricted to M is injective",
                          ACCENT_A,
                          "單射表示 M 與零化空間只交於零，於是把 f 送到兩個泛函值的映射在零化空間上也是單射；而它是二維的，單射就等於到平面的同構",
                          "injectivity makes M meet the null space only at zero, so the map sending f to its two functional values is injective there, and on a two-dimensional space that is an isomorphism onto the plane"))

 # ── beat 10: the lambda that are not allowed ────────────────────
 def _shift(self):
  oy, sy = -0.30, 0.18
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=2.2, tl=0.13))
  g.add(self._plot(shoot, ACCENT_B, LA, LB, oy, sy, sw=2.8))
  # 不允許的只是那幾個離散的零點，所以長條要畫滿整條軸、在紅點處斷開——
  # 原本從 λ₁（它自己就是不允許的那一點）畫到右端，等於把左邊合法的 λ 排除掉了
  _gap = 0.10
  _cuts = sorted(self._xof(lam, LA, LB) for lam in LMARK)
  _edges = [XL - 0.14] + [c for x in _cuts for c in (x - _gap, x + _gap)] + [XR + 0.30]
  for _i in range(0, len(_edges), 2):
   _x0, _x1 = _edges[_i], _edges[_i + 1]
   if _x1 - _x0 > 0.05:
    g.add(Line([_x0, oy - 0.16, 0], [_x1, oy - 0.16, 0], color=ACCENT_A, stroke_width=5.0))
  for k, lam in enumerate(LMARK):
   px = self._xof(lam, LA, LB)
   g.add(Dot([px, oy, 0], radius=0.068, color=WARN))
   g.add(self._sym(oy - 0.34, f"λ {'₁₂₃'[k]}", WARN, FS_TAG - 3, x=px, w=0.46))
  g.add(self._sym(oy + 0.24, "λ", DIM, FS_TAG - 2, x=XR + 0.18, w=0.30))
  g.add(self._legend(XL + 0.06, ((ACCENT_B, "λ   ↦   f ( b )", 1.30),
                                 (ACCENT_A, "( a ′ )", 0.70)), y0=1.14, dy=0.25))
  g.add(self._table((("( 1 )  ,  ( 2 )  ,  ( 4 )            T   →   T  −  λ            ( a ′ )",
                      ACCENT_A),
                     ("λ ₖ   =   − 1   −   ( k π / 2 ) ²", WARN),
                     ("              λ                    f ( b )", DIM),)
                    + tuple((f"      λ {'₁₂₃'[k]}      {lam:+9.4f}          {shoot(lam):+.1e}",
                             WARN) for k, lam in enumerate(LBAD))
                    + tuple((f"             {lam:+9.4f}          {shoot(lam):+9.4f}", ACCENT_B)
                            for lam in LGOOD[:2])
                    + ((f"c ₂  ≥  m  >  0        λ  ≥  c ₀ + 1          Ch 6  ,  6.4", ACCENT_C),),
                    y0=0.90, dy=0.20, size=FS_TAG - 4))
  g.add(self._cap("橘色那幾段都是允許的 λ，只在紅點處斷開",
                  "the orange runs the whole axis and breaks only at the red dots"))
  return g.add(self._foot("前面四組條件裡，第一、第二、第四組在 T 換成 T 減 λ 之後單射仍然成立；第三組也成立，但證明較難，書上略過",
                          "of those four conditions the first, second and fourth keep injectivity when T is replaced by T minus lambda, and so does the third, by a harder argument the book omits",
                          ACCENT_A,
                          "畫的是條件一的打靶函數：從左端出發、值為零斜率為一的解，到右端的值。零點就是少數不能用的 λ。下一集用這些條件證出右逆是緊的自伴算子",
                          "the curve is the shooting function for condition one, the value at b of the solution leaving a with value zero and slope one; its zeros are the few disallowed lambda, and next time these conditions give a compact self-adjoint right inverse"))

 def stage(self):
  a, b, c = self._data(), self._split(), self._route()
  d, e, f_ = self._parts(), self._parity(), self._second()
  h, i, j = self._lemma62(), self._lemma61(), self._four()
  k, l = self._lemma63(), self._shift()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE82ZH, AdvCalcE82EN = make(AdvCalcE82Base, "82", prefix="AdvCalcE")
