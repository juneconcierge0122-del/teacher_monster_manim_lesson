"""advcalc E84 -- chapter 6, section 7 (book pp. 301-304): Fourier series, and
the two exercises that are stronger than the section's own theorems.

Section 6 built the whole Sturm-Liouville machine, and section 7 opens by
admitting how little of it is in range: the orthonormal bases that calculations
actually use -- Bessel, Legendre, Hermite, Laguerre -- all come from singular
systems.  The book's own criterion says why, and that criterion is what beat 0
draws: a system is regular when the leading coefficient never vanishes on a
closed bounded interval, and each of those four fails it either at an endpoint
or at infinity.  The famous exception is Fourier series, which is D squared
with two different boundary conditions.

The section is split here as eleven beats because the two boundary conditions
are two separate computations with two separate answers, and the difference
between them is the whole point: type 1 pins one of the two constants and
leaves a one-dimensional eigenspace per eigenvalue, while type 4 is satisfied
by the entire two-dimensional solution space, which is why the periodic case
needs sines and cosines both.  Beats 2 and 5 therefore carry the two linear
systems and their determinants rather than a summary of them.  Beat 5 also
records something the book glosses: it says "again f = c1 x + c0 is ruled out",
but only the x term is ruled out -- the constant survives, and it is exactly
the n = 0 member of the cosine family, which is why the cosines are indexed
from zero and the sines from one.

The last two beats are exercises 7.6 and 7.10.  They are in the main line
because they are the strongest statements in the section -- 7.6 drops Theorem
7.2's hypotheses from "two continuous derivatives and matching derivatives at
the ends" down to "one continuous derivative and matching values", and 7.10 is
the Weierstrass approximation theorem.  Both beats state what the exercise
claims and why it is stronger; neither solves it.

The numbers are computed, and where it is possible they are computed exactly.
The eigenvalue check does not differentiate a sine: a sine is carried as a pair
of complex exponentials, differentiating one is multiplication by lambda, and
applying D squared plus n squared returns a residual that is zero in the
floating point sense rather than small.  The integrating-factor identities of
beat 0 are checked against analytic derivatives of the leading coefficients.
The rounded corner of beat 7 is in closed form as well: because the ramp that
replaces a jump has the same integral as the jump, the primitive leaves the
polygonal line only inside the window, and its deviation there is a parabola
whose extreme value is exactly delta times the jump over four -- which is the
book's own bound, so the assert checks equality and not an inequality.  The
remaining quantities are integrals, and those go through a 400-point
Gauss-Legendre rule, which on products of low-order sines is good to 1e-13.
"""
import cmath
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these
PI = math.pi

_GX, _GW = np.polynomial.legendre.leggauss(400)


def quad(f, a, b):
 """Gauss-Legendre on [a, b]; exact to 1e-13 on everything used here."""
 x = 0.5 * (b - a) * _GX + 0.5 * (a + b)
 return 0.5 * (b - a) * float(np.sum(_GW * np.array([f(t) for t in x])))


# ── exact arithmetic on  P(t) exp(lambda t)  ──────────────────────────
# Carried over from E80. A function is a list of (P, lambda) terms with P a
# list of coefficients, lowest power first; differentiating is
# (P' + lambda P) exp(lambda t). A sine is the pair of complex exponentials, so
# nothing here ever differentiates a sine by quoting the rule for sines.
def dterm(P, lam):
 out = [lam * c for c in P]
 for k in range(1, len(P)):
  out[k - 1] += k * P[k]
 return out


def dall(terms):
 return [(dterm(P, lam), lam) for P, lam in terms]


def applyp(coeffs, terms):
 """Apply a0 + a1 D + ... + an D^n to a function."""
 acc, cur = [], [(list(P), lam) for P, lam in terms]
 for j, a in enumerate(coeffs):
  if j:
   cur = dall(cur)
  if a:
   acc += [([a * c for c in P], lam) for P, lam in cur]
 return acc


def val(terms, t):
 return sum(sum(P[k] * t ** k for k in range(len(P))) * cmath.exp(lam * t)
            for P, lam in terms)


GRID = (0.17, 0.60, 1.10, 1.70, 2.35, 3.00)


def size(terms, ts=GRID):
 return max(abs(val(terms, t)) for t in ts)


def tcos(w):
 return [([0.5], complex(0.0, w)), ([0.5], complex(0.0, -w))]


def tsin(w):
 return [([-0.5j], complex(0.0, w)), ([0.5j], complex(0.0, -w))]


def det2(a, b, c, d):
 return a * d - b * c


# ── beat 0: the four classical bases are singular systems ─────────────
# Each row is (c2, c2', A, B, mu, window, which window ends have c2 = 0).
# The textbook form is A f'' + B f' + C f = 0; multiplying by mu is supposed to
# turn it into (c2 f')' + c0 f = 0, which asks for A mu = c2 and B mu = c2'.
SL = (
 (lambda x: 1.0, lambda x: 0.0,
  lambda x: 1.0, lambda x: 0.0, lambda x: 1.0,
  (0.0, PI), ()),                                     # D squared, on [0, pi]
 (lambda x: x, lambda x: 1.0,
  lambda x: x * x, lambda x: x, lambda x: 1.0 / x,
  (0.0, 1.0), (0,)),                                  # Bessel
 (lambda x: 1.0 - x * x, lambda x: -2.0 * x,
  lambda x: 1.0 - x * x, lambda x: -2.0 * x, lambda x: 1.0,
  (-1.0, 1.0), (0, 1)),                               # Legendre
 (lambda x: math.exp(-x * x), lambda x: -2.0 * x * math.exp(-x * x),
  lambda x: 1.0, lambda x: -2.0 * x, lambda x: math.exp(-x * x),
  (-1.1, 1.1), ()),                                   # Hermite, on the line
 (lambda x: x * math.exp(-x), lambda x: (1.0 - x) * math.exp(-x),
  lambda x: x, lambda x: 1.0 - x, lambda x: math.exp(-x),
  (0.0, 3.5), (0,)),                                  # Laguerre, on [0, inf)
)
SLSAMP = (0.13, 0.31, 0.47, 0.66, 0.83)                # fractions along a window
SLRES = 0.0
for _c2, _c2p, _A, _B, _mu, (_wa, _wb), _z in SL:
 for _u in SLSAMP:
  _x = _wa + (_wb - _wa) * _u
  SLRES = max(SLRES, abs(_A(_x) * _mu(_x) - _c2(_x)), abs(_B(_x) * _mu(_x) - _c2p(_x)))
assert SLRES < 1e-12, \
    "each classical equation really does become ( c2 f' )' + c0 f after its integrating factor"
SLMAX = tuple(max(abs(c2(wa + (wb - wa) * k / 200.0)) for k in range(201))
              for c2, _, _, _, _, (wa, wb), _ in SL)
SLEND = tuple((abs(c2(wa)), abs(c2(wb))) for c2, _, _, _, _, (wa, wb), _ in SL)
assert min(SLEND[0]) > 0.5, "the leading coefficient of D squared is one at both ends: regular"
assert SLEND[1][0] < 1e-15 and SLEND[2][0] < 1e-15 and SLEND[2][1] < 1e-15, \
    "Bessel's vanishes at the left end and Legendre's at both: those systems are singular"
assert SLEND[4][0] < 1e-15, "Laguerre's vanishes at the left end as well"
assert min(SLEND[3]) > 0.25, \
    "Hermite's stays well off zero on the drawn window: what breaks it is the unbounded interval"

# ── beat 1: formal self-adjointness is c1 = c2' ───────────────────────
# T f = c2 f'' + c1 f' + c0 f and the formal adjoint R g = ( c2 g )'' - ( c1 g )'
# + c0 g, both in exact polynomial arithmetic, so a zero residual is really zero.
_P = np.polynomial.Polynomial
GTEST = _P([0.3, -1.2, 0.8, 0.25])


def adjres(c2, c1, c0):
 t = c2 * GTEST.deriv(2) + c1 * GTEST.deriv(1) + c0 * GTEST
 a = (c2 * GTEST).deriv(2) - (c1 * GTEST).deriv(1) + c0 * GTEST
 return float(np.max(np.abs((a - t).coef))) if len((a - t).coef) else 0.0


ADJ_OK = adjres(_P([1.0]), _P([0.0]), _P([0.0]))
ADJ_BAD = adjres(_P([1.0]), _P([1.0]), _P([0.0]))
assert ADJ_OK < 1e-14, "with c2 identically one and c1 zero the operator is its own formal adjoint"
assert ADJ_BAD > 1.0, "and a first order term that is not c2' destroys that: the condition bites"

# ── beat 2: the type 1 problem, three cases ───────────────────────────
R_POS = 1.0
DET_POS = det2(1.0, 1.0, math.exp(R_POS * PI), math.exp(-R_POS * PI))
DET_NIL = det2(0.0, 1.0, PI, 1.0)
R_OK, R_BAD = 2.0, 2.5
DET_OK, DET_BAD = -math.sin(R_OK * PI), -math.sin(R_BAD * PI)
assert abs(DET_POS) > 1.0, \
    "for positive lambda the two endpoint equations are independent, so only f = 0 survives"
assert abs(DET_NIL) > 1.0, "for lambda zero they are independent too, and again only f = 0"
assert abs(DET_OK) < 1e-15, "for negative lambda the determinant vanishes exactly at integer r"
assert abs(DET_BAD) > 0.9, "and at a non-integer r it does not, so there is no eigenfunction there"


def u_pos(x):
 return math.sinh(R_POS * x) / math.sinh(R_POS * PI)


def u_nil(x):
 return x / PI


def u_neg(x):
 return math.sin(R_OK * x)


assert abs(u_pos(PI) - 1.0) < 1e-12 and abs(u_nil(PI) - 1.0) < 1e-12, \
    "the first two curves leave the left zero and never come back to it"
assert abs(u_neg(PI)) < 1e-14, "only the third one is zero at both endpoints"

# ── beats 3 and 4: the eigenfunctions, exactly ────────────────────────
NSHOW = (1, 2, 3)
EIG = tuple((n, size(applyp([float(n * n), 0.0, 1.0], tsin(float(n)))),
             abs(math.sin(n * PI))) for n in NSHOW)
assert all(r < 1e-15 for _n, r, _e in EIG), \
    "D squared sends sin n x to minus n squared times itself: these are the eigenfunctions"
assert all(e < 1e-14 for _n, _r, e in EIG), "and each of them vanishes at both endpoints"
EIG_BAD = abs(math.sin(R_BAD * PI))
assert EIG_BAD > 0.9, "while sin r x with a non-integer r misses the right endpoint entirely"
LAM = tuple(-n * n for n in NSHOW)
assert LAM == (-1, -4, -9), "the eigenvalues are minus the squares of the positive integers"

SS_HALF = tuple(tuple(quad(lambda t, n=n, m=m: math.sin(n * t) * math.sin(m * t), 0.0, PI)
                      for m in NSHOW) for n in NSHOW)
assert all(abs(SS_HALF[i][j]) < 1e-12 for i in range(3) for j in range(3) if i != j), \
    "distinct sines are orthogonal on the half interval"
assert all(abs(SS_HALF[i][i] - PI / 2.0) < 1e-12 for i in range(3)), \
    "and each has square norm pi over two there, not pi"

# ── beat 4: x ( pi - x ) and its partial sums ─────────────────────────
def f71(x):
 return x * (PI - x)


B71 = tuple(quad(lambda t, n=n: f71(t) * math.sin(n * t), 0.0, PI) * 2.0 / PI
            for n in range(1, 10))
assert all(abs(B71[n - 1] - 8.0 / (PI * n ** 3)) < 1e-12 for n in (1, 3, 5, 7, 9)), \
    "the odd coefficients are eight over pi n cubed"
assert all(abs(B71[n - 1]) < 1e-12 for n in (2, 4, 6, 8)), "and the even ones vanish"

NPART = (1, 3, 5, 9)
_XS71 = np.linspace(0.0, PI, 2001)


def s71(N, x):
 return sum(B71[n - 1] * math.sin(n * x) for n in range(1, N + 1))


ERR71 = tuple((N,
               max(abs(f71(float(x)) - s71(N, float(x))) for x in _XS71),
               math.sqrt(quad(lambda t, N=N: (f71(t) - s71(N, t)) ** 2, 0.0, PI)))
              for N in NPART)
assert all(ERR71[k][1] < ERR71[k - 1][1] for k in range(1, len(ERR71))), \
    "the uniform error falls with every extra term, which is what Theorem 7.1 promises"
assert all(ERR71[k][2] < ERR71[k - 1][2] for k in range(1, len(ERR71))), \
    "and so does the two-norm error"
E4SHOW = (1, 3, 5)
_E4 = [[f71(float(x)) - s71(N, float(x)) for x in np.linspace(0.0, PI, 171)] for N in E4SHOW]
E4LO, E4HI = min(min(r) for r in _E4), max(max(r) for r in _E4)
E4SY = 1.30 / (E4HI - E4LO)
E4OY = -0.95 - E4SY * E4LO

# ── beats 5 and 6: the periodic problem ───────────────────────────────
NPER = 2
DETPER_OK = 4.0 * R_OK * math.sin(R_OK * PI) ** 2
DETPER_BAD = 4.0 * R_BAD * math.sin(R_BAD * PI) ** 2
assert abs(DETPER_OK) < 1e-15, \
    "at integer r the periodic system is degenerate: both constants stay free"
assert DETPER_BAD > 1.0, "at a non-integer r it is not, so once again only f = 0"

PERBAS = ((tsin(float(NPER)), lambda x: math.sin(NPER * x),
           lambda x: NPER * math.cos(NPER * x)),
          (tcos(float(NPER)), lambda x: math.cos(NPER * x),
           lambda x: -NPER * math.sin(NPER * x)))
PERRES = tuple((size(applyp([float(NPER * NPER), 0.0, 1.0], tm)),
                abs(f(PI) - f(-PI)),
                abs(d(PI) - d(-PI)))
               for tm, f, d in PERBAS)
assert all(r < 1e-15 for r, _a, _b in PERRES), \
    "both sin n x and cos n x lie in the null space of D squared plus n squared"
assert all(a < 1e-14 and b < 1e-13 for _r, a, b in PERRES), \
    "and both match in value and in slope at the two ends: the whole plane satisfies type 4"
# The Wronskian of the pair, actually evaluated rather than written down: it is
# sin(nx) * (-n sin nx) - (n cos nx) * cos(nx) = -n at every x, and a nonzero
# constant is what makes the pair independent, hence the plane two-dimensional.
WRPER_AT = tuple(math.sin(NPER * x) * (-NPER * math.sin(NPER * x))
                 - (NPER * math.cos(NPER * x)) * math.cos(NPER * x)
                 for x in (-2.7, -1.0, 0.0, 0.8, 2.2))
assert max(abs(w + NPER) for w in WRPER_AT) < 1e-14, \
    "the Wronskian is the constant -n, so the two solutions are independent at every x"
WRPER = WRPER_AT[0]
assert abs(WRPER) > 0.5, "a nonzero Wronskian: that plane really is two-dimensional"
# the lambda = 0 branch: of c1 x + c0, which part survives the periodic condition
CONST_JUMP = tuple((abs(f(PI) - f(-PI)), abs(d(PI) - d(-PI)))
                   for f, d in ((lambda x: 1.0, lambda x: 0.0), (lambda x: x, lambda x: 1.0)))
assert max(CONST_JUMP[0]) < 1e-15, \
    "the constant function meets type 4 in value and in slope, so it is an eigenfunction"
assert CONST_JUMP[1][0] > 1.0, \
    "the x term does not, so only c1 is forced to zero: the survivor is cos 0 x, the n = 0 cosine"

ORTH = {}
for _tag, _fa, _fb, _ra, _rb in (("ss", math.sin, math.sin, (1, 2, 3), (1, 2, 3)),
                                 ("cc", math.cos, math.cos, (0, 1, 2), (0, 1, 2)),
                                 ("sc", math.sin, math.cos, (1, 2, 3), (0, 1, 2))):
 ORTH[_tag] = {(n, m): quad(lambda t, n=n, m=m, a=_fa, b=_fb: a(n * t) * b(m * t), -PI, PI)
               for n in _ra for m in _rb}
OFFMAX = max(abs(v) for (n, m), v in ORTH["ss"].items() if n != m)
OFFMAX = max(OFFMAX, max(abs(v) for (n, m), v in ORTH["cc"].items() if n != m))
SCMAX = max(abs(v) for v in ORTH["sc"].values())
assert OFFMAX < 1e-12, "distinct sines, and distinct cosines, are orthogonal on the full interval"
assert SCMAX < 1e-12, "and every sine is orthogonal to every cosine, which is the one extra fact"
assert all(abs(ORTH["ss"][(n, n)] - PI) < 1e-12 for n in (1, 2, 3)), \
    "on minus pi to pi the square norm is pi, twice what it was on the half interval"
assert all(abs(ORTH["cc"][(n, n)] - PI) < 1e-12 for n in (1, 2)), \
    "and the cosines of positive index agree with them"
assert abs(ORTH["cc"][(0, 0)] - 2.0 * PI) < 1e-11, \
    "but the constant one is the exception: its square norm is two pi"


def prod6(x):
 return math.sin(NPER * x) * math.cos(NPER * x)


def run6(x):
 return (1.0 - math.cos(2.0 * NPER * x)) / (4.0 * NPER)


PRODID = max(abs(prod6(float(x)) - 0.5 * math.sin(2.0 * NPER * float(x)))
             for x in np.linspace(-PI, PI, 801))
assert PRODID < 1e-15, "the integrand is half the sine of twice the angle, hence odd"
RUNCHK = max(abs(run6(float(x)) - quad(prod6, -PI, float(x)))
             for x in np.linspace(-PI, PI, 41))
assert RUNCHK < 1e-13, \
    "the second curve really is the first one's area from the left end, not an unrelated wave"
RUNMIN = min(run6(float(x)) for x in np.linspace(-PI, PI, 801))
assert RUNMIN > -1e-15, "the running area never dips below zero"
assert abs(run6(PI) - run6(-PI)) < 1e-15 and abs(run6(PI)) < 1e-15, \
    "and it comes back to zero at the right end, which is the orthogonality"

# ── beat 7: the density theorem, by hand ──────────────────────────────
def f73(x):
 return math.sin(x) + 0.5 * abs(math.sin(2.0 * x))


def nodes73(n):
 xs = [k * PI / n for k in range(n + 1)]
 return xs, [f73(x) for x in xs]


def slopes73(xs, ys):
 return [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]


def gval(xs, ys, x):
 for i in range(len(xs) - 1):
  if x <= xs[i + 1] + 1e-12:
   return ys[i] + (ys[i + 1] - ys[i]) * (x - xs[i]) / (xs[i + 1] - xs[i])
 return ys[-1]


def gminusH(xs, ss, dl, x):
 """g - H inside a smoothing window, in closed form.

 The ramp has the same integral as the jump it replaces, so H leaves g only
 inside the window, and the deviation there is a parabola with extreme value
 exactly dl times the jump over four."""
 for i in range(1, len(xs) - 1):
  if abs(x - xs[i]) <= dl:
   u, dd = x - (xs[i] - dl), ss[i] - ss[i - 1]
   return -dd * u * u / (4.0 * dl) if u <= dl else dd * (u - dl) - dd * u * u / (4.0 * dl)
 return 0.0


NSUB = (4, 8, 16, 32)
_XS73 = np.linspace(0.0, PI, 2401)
DENS = []
for _n in NSUB:
 _xs, _ys = nodes73(_n)
 _ss = slopes73(_xs, _ys)
 _dl = (PI / _n) / 4.0
 _jump = max(abs(_ss[i] - _ss[i - 1]) for i in range(1, _n))
 _eg = max(abs(f73(float(x)) - gval(_xs, _ys, float(x))) for x in _XS73)
 _eh = max(abs(f73(float(x)) - gval(_xs, _ys, float(x)) + gminusH(_xs, _ss, _dl, float(x)))
           for x in _XS73)
 _gh = max(abs(gminusH(_xs, _ss, _dl, x)) for x in _xs[1:-1])
 DENS.append((_n, _eg, _eh, _dl * _jump / 4.0, _gh))
DENS = tuple(DENS)
assert all(DENS[k][1] < DENS[k - 1][1] for k in range(1, len(DENS))), \
    "refining the subdivision drives the polygonal line uniformly onto f"
assert all(DENS[k][2] < DENS[k - 1][2] for k in range(1, len(DENS))), \
    "and the rounded primitive follows it down, so the twice differentiable ones are dense"
assert all(abs(d[3] - d[4]) < 1e-12 for d in DENS), \
    "the rounding costs exactly delta times the jump over four: the book's bound is attained"
N73 = NSUB[0]
XS73, YS73 = nodes73(N73)
SS73 = slopes73(XS73, YS73)
DL73 = (PI / N73) / 4.0
SMAX73 = max(abs(s) for s in SS73)
H73 = ([(XS73[0], SS73[0])]
       + [p for i in range(1, N73) for p in ((XS73[i] - DL73, SS73[i - 1]),
                                             (XS73[i] + DL73, SS73[i]))]
       + [(XS73[N73], SS73[N73 - 1])])
G73 = ([(XS73[0], SS73[0])]
       + [p for i in range(1, N73) for p in ((XS73[i], SS73[i - 1]), (XS73[i], SS73[i]))]
       + [(XS73[N73], SS73[N73 - 1])])

# ── beat 8: why density is needed, and what it does not buy ───────────
B8 = tuple(quad(lambda t, n=n: math.sin(n * t), 0.0, PI) * 2.0 / PI for n in range(1, 32))
assert all(abs(B8[n - 1] - 4.0 / (PI * n)) < 1e-12 for n in (1, 3, 5, 31)), \
    "the constant one expands with coefficients four over pi n at the odd n"


def s8(N, x):
 return sum(B8[n - 1] * math.sin(n * x) for n in range(1, N + 1))


N8SHOW = (3, 15, 31)
ERR8 = tuple((N,
              max(abs(1.0 - s8(N, float(x))) for x in np.linspace(0.0, PI, 2001)),
              math.sqrt(max(0.0, quad(lambda t, N=N: (1.0 - s8(N, t)) ** 2, 0.0, PI))))
             for N in N8SHOW)
assert all(abs(e[1] - 1.0) < 1e-9 for e in ERR8), \
    "every partial sum is zero at the endpoints, so the uniform error to f = 1 stays at one"
assert all(ERR8[k][2] < ERR8[k - 1][2] for k in range(1, len(ERR8))), \
    "while the two-norm error falls: density buys the two-norm, not the uniform norm"
S8MAX = max(s8(N8SHOW[-1], float(x)) for x in np.linspace(0.0, PI, 2001))
assert S8MAX > 1.0, "the overshoot near the jump does not go away either"

# ── beat 9: exercise 7.6, on a function Theorem 7.2 cannot reach ──────
def f76(x):
 return PI * PI - x * x


A76_0 = quad(f76, -PI, PI) / (2.0 * PI)
A76 = tuple(quad(lambda t, n=n: f76(t) * math.cos(n * t), -PI, PI) / PI for n in range(1, 9))
assert abs(A76_0 - 2.0 * PI * PI / 3.0) < 1e-11, "the mean term is two pi squared over three"
assert all(abs(A76[n - 1] - 4.0 * (-1.0) ** (n + 1) / n ** 2) < 1e-11 for n in range(1, 9)), \
    "and the cosine coefficients alternate as four over n squared"
def d76(x):
 return -2.0 * x


JUMP76 = (abs(f76(-PI) - f76(PI)), abs(d76(-PI) - d76(PI)))
assert JUMP76[0] < 1e-13, "the values do agree at the two ends, which is all exercise 7.6 asks"
assert JUMP76[1] > 1.0, \
    "but the derivatives do not, so Theorem 7.2 says nothing here while 7.6 still applies"


def s76(N, x):
 return A76_0 + sum(A76[n - 1] * math.cos(n * x) for n in range(1, N + 1))


N76 = (1, 2, 4, 8)
ERR76 = tuple(max(abs(f76(float(x)) - s76(N, float(x))) for x in np.linspace(-PI, PI, 2001))
              for N in N76)
assert all(ERR76[k] < ERR76[k - 1] for k in range(1, len(ERR76))), \
    "and the uniform error does fall, which is the conclusion the exercise is after"
E76SHOW = (1, 4)
F76HI = max([f76(0.0)] + [s76(N, 0.0) for N in E76SHOW])

# ── beat 10: exercise 7.10, and the series it leans on ────────────────
def mac(k, x):
 return sum((-1.0) ** j * x ** (2 * j + 1) / math.factorial(2 * j + 1) for j in range(k))


MACD = (3, 5, 7, 9)
MAC = tuple((d,
             max(abs(math.sin(float(x)) - mac((d + 1) // 2, float(x)))
                 for x in np.linspace(0.0, PI, 2001)),
             PI ** (d + 2) / math.factorial(d + 2))
            for d in MACD)
assert all(MAC[k][1] < MAC[k - 1][1] for k in range(1, len(MAC))), \
    "the Maclaurin sections of the sine converge uniformly on the whole of zero to pi"
assert all(e <= b for _d, e, b in MAC), \
    "each error stays under the next term of the series, so the degree needed is finite"
MACSHOW = (3, 5)
M10LO = min(mac((MACSHOW[0] + 1) // 2, float(x)) for x in np.linspace(0.0, PI, 401))
M10HI = max(max(mac((d + 1) // 2, float(x)) for x in np.linspace(0.0, PI, 401))
            for d in MACSHOW)
assert M10LO < -1.5 and M10HI > 0.9, \
    "the cubic section overshoots downward while the quintic does not: the two curves differ"


class AdvCalcE84Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 84

 MODE_LABEL = {
  0: {"zh": "正則的系統不多", "en": "there are not many regular systems"},
  1: {"zh": "T 等於二階導數：形式自伴又正則",
      "en": "T is the second derivative: self-adjoint and regular"},
  2: {"zh": "型 1：三種 λ 都試一遍", "en": "type 1: all three cases of lambda"},
  3: {"zh": "特徵函數與特徵值", "en": "the eigenfunctions and the eigenvalues"},
  4: {"zh": "定理 7.1", "en": "theorem 7.1"},
  5: {"zh": "型 4：週期條件", "en": "type 4: the periodic condition"},
  6: {"zh": "定理 7.2", "en": "theorem 7.2"},
  7: {"zh": "定理 7.3：稠密性", "en": "theorem 7.3: density"},
  8: {"zh": "為什麼需要稠密性", "en": "why density is needed"},
  9: {"zh": "習題 7.6：更強的一致收斂",
      "en": "exercise 7.6: a stronger uniform convergence"},
  10: {"zh": "習題 7.10：Weierstrass 逼近定理，第 6 章結束",
       "en": "exercise 7.10: Weierstrass, and the end of chapter 6"},
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
  """A curve over t in [ta, tb], with ta pinned to the figure's left edge.

  Same helper as E79 and E80, and for the same reason: the t range is a
  parameter, so nothing has to be assumed about where t = 0 lands on screen."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _poly(self, pts, col, ta, tb, oy, sy, sw=2.6, xl=XL, xr=XR):
  """A polygonal line through exact (t, value) pairs -- no resampling, so a
  corner stays a corner instead of being rounded off by the sample spacing."""
  return self._curve([[self._xof(t, ta, tb, xl, xr), oy + sy * v, 0] for t, v in pts],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 def _base(self, oy):
  return self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14)

 # ── beat 0: regular systems are scarce ──────────────────────────
 def _scarce(self):
  oy, sy = -0.72, 1.55
  cols = (ACCENT_A, ACCENT_B, ACCENT_C, WARN, DIM)
  g = VGroup(self._base(oy))
  for (c2, _p, _A, _B, _mu, (wa, wb), _z), mx, col in zip(SL, SLMAX, cols):
   g.add(self._plot(lambda x, c2=c2, mx=mx: c2(x) / mx, col, wa, wb, oy, sy,
                    sw=3.4 if col is ACCENT_A else 2.4))
  # the two places where a leading coefficient really reaches zero
  for x0 in (XL, XR):
   g.add(Dot([x0, oy, 0], radius=0.075, color=WARN))
  # and the two curves whose interval has no right (or left) end at all
  for col, k, xa, xb, end in ((WARN, 3, XL, XL - 0.34, 0), (WARN, 3, XR, XR + 0.34, 1),
                              (DIM, 4, XR, XR + 0.34, 1)):
   yv = SL[k][0](SL[k][5][end]) / SLMAX[k]
   g.add(self._arr([xa, oy + sy * yv, 0], [xb, oy + sy * yv, 0], col, sw=2.5, tl=0.11))
  g.add(self._table((("T f  =  ( c ₂ f ′ ) ′  +  c ₀ f", ACCENT_A),
                     ("c ₂  ≡  1              [ 0 , π ]", ACCENT_A),
                     ("c ₂  =  x              [ 0 , 1 ]            c ₂ ( 0 )  =  0", ACCENT_B),
                     ("c ₂  =  1 − x ²        [ − 1 , 1 ]        c ₂ ( ± 1 )  =  0", ACCENT_C),
                     ("c ₂  =  exp ( − x ² )        ( − ∞ , ∞ )", WARN),
                     ("c ₂  =  x exp ( − x )        [ 0 , ∞ )        c ₂ ( 0 )  =  0", DIM),
                     (f"max  | A μ − c ₂ |  +  | B μ − c ₂ ′ |   =   {SLRES:.1e}", ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("碰底線的是三條；Hermite 不碰，壞的是區間沒有盡頭",
                  "three curves reach the baseline; Hermite does not -- its interval is what has no end"))
  return g.add(self._foot("正則的 Sturm-Liouville 系統不多：最高階係數要在一個有界閉區間上從頭到尾不為零，這一條就刷掉了幾乎所有常用的正交基底",
                          "regular systems are scarce: the leading coefficient has to stay away from zero on a closed bounded interval, and that rules out almost every basis in common use",
                          ACCENT_A,
                          "左圖把五個不同的區間壓成同寬、高度各自歸一，所以長短不能比；右表每一列是那一組寫成自伴形式之後的最高階係數，顏色對應同色的曲線，最後一列是殘差",
                          "the figure squeezes five different intervals to one width and normalises each height, so lengths there mean nothing; each row is one family's leading coefficient in self-adjoint form, coloured to match its curve"))

 # ── beat 1: D squared, and the two boundary conditions ──────────
 def _operator(self):
  x0, xb, xm = -4.20, -2.88, -5.52
  g = VGroup()
  for yy, col, xa in ((0.70, ACCENT_B, x0), (-0.50, ACCENT_C, xm)):
   g.add(Line([xa, yy, 0], [xb, yy, 0], color=col, stroke_width=4.0))
   g.add(Dot([xa, yy, 0], radius=0.075, color=col), Dot([xb, yy, 0], radius=0.075, color=col))
  g.add(Line([x0, -0.58, 0], [x0, -0.42, 0], color=DIM, stroke_width=1.6))
  g.add(self._sym(1.00, "f ( 0 )  =  f ( π )  =  0", ACCENT_B, FS_TAG - 1, x=-4.20, w=2.90))
  g.add(self._sym(0.44, "0", DIM, FS_TAG - 2, x=x0, w=0.34),
        self._sym(0.44, "π", DIM, FS_TAG - 2, x=xb, w=0.34))
  g.add(self._sym(0.06, "f ( − π )  =  f ( π )", ACCENT_C, FS_TAG - 1, x=-4.20, w=2.40))
  g.add(self._sym(-0.20, "f ′ ( − π )  =  f ′ ( π )", ACCENT_C, FS_TAG - 1, x=-4.20, w=2.60))
  g.add(self._sym(-0.76, "− π", DIM, FS_TAG - 2, x=xm, w=0.52),
        self._sym(-0.76, "0", DIM, FS_TAG - 2, x=x0, w=0.34),
        self._sym(-0.76, "π", DIM, FS_TAG - 2, x=xb, w=0.34))
  g.add(self._table((("T f  =  c ₂ f ″  +  c ₁ f ′  +  c ₀ f", ACCENT_A),
                     ("c ₂  ≡  1  ,     c ₁  =  c ₂ ′  =  0  ,     c ₀  ≡  0", ACCENT_A),
                     ("R f  =  ( c ₂ f ) ″  −  ( c ₁ f ) ′  +  c ₀ f            § 6  ,  6.2", DIM),
                     (f"‖ R f  −  T f ‖   =   {ADJ_OK:.1e}", ACCENT_B),
                     (f"c ₁  =  1     ⇒     ‖ R f  −  T f ‖   =   {ADJ_BAD:.3f}", WARN),
                     ("( 1 )        f ( 0 )  =  f ( π )  =  0", ACCENT_B),
                     ("( 4 )        c ₂ ( a )  =  c ₂ ( b )  =  1", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩條線同一個比例尺，下面那個區間剛好是上面的兩倍長",
                  "the two intervals are drawn to one scale, the lower one twice as long"))
  return g.add(self._foot("這一節的算子就是二階導數。最高階係數恆等於一，一階項的係數等於它的導數也就是零，照上一節的引理這正是形式自伴",
                          "the operator of this section is the second derivative: its leading coefficient is one and the first order one is its derivative, namely zero, which is formal self-adjointness",
                          ACCENT_A,
                          "而且最高階係數從頭到尾不為零，所以系統是正則的；兩端的值相等又讓型四那個週期條件用得上。上面是型一的端點，下面是型四",
                          "it never vanishes, so the system is regular, and it takes equal values at the two ends, which is what type 4 needs: type 1 above, type 4 below"))

 # ── beat 2: solving the type 1 problem ──────────────────────────
 def _solve1(self):
  oy, sy = -0.30, 0.72
  g = VGroup(self._base(oy),
             Line([XL, oy - 0.06, 0], [XL, oy + 0.50, 0], color=DIM, stroke_width=1.3))
  for f, col, sw in ((u_pos, ACCENT_B, 2.6), (u_nil, ACCENT_C, 2.6), (u_neg, ACCENT_A, 3.2)):
   g.add(self._plot(f, col, 0.0, PI, oy, sy, sw=sw))
  g.add(Dot([XR, oy + sy, 0], radius=0.075, color=WARN),
        Dot([XR, oy, 0], radius=0.075, color=ACCENT_A),
        Dot([XL, oy, 0], radius=0.065, color=DIM))
  g.add(self._legend(XL + 0.06, ((ACCENT_B, "λ  >  0", 1.00), (ACCENT_C, "λ  =  0", 1.00),
                                 (ACCENT_A, "λ  <  0", 1.00)), y0=1.14, dy=0.24))
  g.add(self._table((("f ″  −  λ f  =  0            f ( 0 )  =  f ( π )  =  0", ACCENT_A),
                     ("λ > 0  :    c ₁ + c ₂ = 0  ,    c ₁ exp ( r π ) + c ₂ exp ( − r π ) = 0",
                      ACCENT_B),
                     (f"λ > 0  :    det   =   {DET_POS:+.3f}            c ₁  =  c ₂  =  0",
                      ACCENT_B),
                     (f"λ = 0  :    f  =  c ₁ x  +  c ₀            det   =   {DET_NIL:+.4f}",
                      ACCENT_C),
                     ("λ < 0  :    c ₂  =  0  ,     c ₁ sin r π  =  0", ACCENT_A),
                     (f"det  =  − sin r π        r = 2  :  {abs(DET_OK):.1e}"
                      f"        r = 2.5  :  {DET_BAD:+.2f}", WARN),
                     ("r  =  n            λ  =  −  n ²", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("三條都從左端的零出發，只有橘色那條回得到右端的零",
                  "all three leave the zero on the left; only the orange one reaches the one on the right"))
  return g.add(self._foot("先解型一。λ 大於零時解空間由兩個指數張成，兩端都為零逼出兩個係數都是零；λ 等於零時解是一次式，同樣只剩零解",
                          "solve type 1 first: for positive lambda two exponentials span the solutions and vanishing at both ends kills both constants, and for lambda zero the linear solution goes the same way",
                          ACCENT_A,
                          "右表把那兩個線性方程組的行列式算出來，都不是零，所以真的只有零解。λ 小於零才有救，左端的零殺掉 cos 那一項，右端的零要求 sin r π 是零",
                          "the table gives the two determinants and neither is zero, so only the trivial solution survives; negative lambda is the only case, and there the right end asks for the sine of r pi to vanish"))

 # ── beat 3: the eigenfunctions and the eigenvalues ──────────────
 def _eigen(self):
  oy, sy = -0.10, 0.58
  g = VGroup(self._base(oy))
  cols = (ACCENT_A, ACCENT_B, ACCENT_C)
  for n, col in zip(NSHOW, cols):
   g.add(self._plot(lambda x, n=n: math.sin(n * x), col, 0.0, PI, oy, sy, sw=2.8))
   for k in range(1, n):
    g.add(Dot([self._xof(k * PI / n, 0.0, PI), oy, 0], radius=0.060, color=col))
  for x0 in (XL, XR):
   g.add(Dot([x0, oy, 0], radius=0.075, color=DIM))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "sin x", 0.90), (ACCENT_B, "sin 2 x", 1.20),
                                 (ACCENT_C, "sin 3 x", 1.20)), y0=1.14, dy=0.24))
  g.add(self._table((("D ² sin n x   =   −  n ² sin n x", ACCENT_A),
                     ("        n          ‖ ( D ² + n ² ) sin n x ‖          | sin n π |", DIM),)
                    + tuple((f"        {n}                {r:.1e}                    {e:.1e}",
                             cols[k]) for k, (n, r, e) in enumerate(EIG))
                    + ((f"λ ₙ   =   {LAM[0]} , {LAM[1]} , {LAM[2]} , …", ACCENT_A),
                       (f"r  =  2.5     ⇒     | sin r π |   =   {EIG_BAD:.3f}", WARN)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("最後一列的 r 不是整數，右端點就不是零了",
                  "the last row's r is not an integer, and its right endpoint is not zero"))
  return g.add(self._foot("所以特徵函數是 sin n x，特徵值是負的 n 平方。左圖畫了前三個，內部節點數一個比一個多，不可能疊成同一條",
                          "so the eigenfunctions are the sines of n x with eigenvalues minus n squared; the figure draws the first three, each with one more interior node than the last",
                          ACCENT_A,
                          "右表把二階導數加上 n 平方再代回去，殘差是機器精度的零——這裡的 sin 是用兩個複指數組起來的，所以微分不是拿 sin 的公式去背",
                          "the table substitutes each back into the second derivative plus n squared; the sine is carried as two complex exponentials, so nothing here differentiates it by quoting the rule"))

 # ── beat 4: Theorem 7.1, and what uniform convergence looks like ─
 def _thm71(self):
  g = VGroup(self._base(E4OY))
  cols = (ACCENT_A, ACCENT_B, ACCENT_C)
  for N, col in zip(E4SHOW, cols):
   g.add(self._plot(lambda x, N=N: f71(x) - s71(N, x), col, 0.0, PI, E4OY, E4SY, sw=2.8))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "f  −  S ₁", 1.20), (ACCENT_B, "f  −  S ₃", 1.20),
                                 (ACCENT_C, "f  −  S ₅", 1.20)), y0=1.14, dy=0.24))
  g.add(self._table((("{ sin n x }   n  ≥  1              𝒞 ⁰ ( [ 0 , π ] )", ACCENT_A),
                     (f"( sin n x , sin m x )  =  0  ,   π / 2  =  {SS_HALF[0][0]:.4f}",
                      ACCENT_A),
                     ("f  =  x ( π − x )            b ₙ   =   8 / ( π n ³ )", ACCENT_B),
                     ("        N          ‖ f − S ‖ ∞          ‖ f − S ‖ ₂", DIM),)
                    + tuple((f"        {N}              {u:.5f}              {w:.5f}",
                             ACCENT_B if N in E4SHOW else DIM)
                            for N, u, w in ERR71),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("三條誤差放大同一個倍率，取愈多項就愈平",
                  "the three errors share one magnification, and more terms means flatter"))
  return g.add(self._foot("定理 7.1：這一族是零到 π 上連續函數空間的正交基底，彼此的內積是零，自己和自己是 π 的一半",
                          "Theorem 7.1: the family is an orthogonal basis for the continuous functions on zero to pi, distinct ones orthogonal and each of square norm half of pi",
                          ACCENT_A,
                          "而且只要 f 有兩階連續導數、兩端的值又都是零，它的 Fourier 級數就一致收斂到 f。右表兩欄的誤差都在往下掉",
                          "and if f has two continuous derivatives and vanishes at both ends its Fourier series converges to it uniformly, as both error columns show"))

 # ── beat 5: the periodic computation ────────────────────────────
 def _period(self):
  oy, sy = -0.15, 0.65
  g = VGroup(self._base(oy),
             Line([self._xof(0.0, -PI, PI), oy - 0.06, 0],
                  [self._xof(0.0, -PI, PI), oy + 0.52, 0], color=DIM, stroke_width=1.3))
  for f, col in ((math.cos, ACCENT_C),
                 (lambda x: math.cos(NPER * x), ACCENT_A),
                 (lambda x: math.sin(NPER * x), ACCENT_B)):
   g.add(self._plot(f, col, -PI, PI, oy, sy, sw=2.8))
   for x0 in (XL, XR):
    g.add(Dot([x0, oy + sy * f(PI if x0 == XR else -PI), 0], radius=0.070, color=col))
  g.add(self._legend(XL + 0.06, ((ACCENT_C, "cos x", 0.90), (ACCENT_A, "cos 2 x", 1.20),
                                 (ACCENT_B, "sin 2 x", 1.20)), y0=1.14, dy=0.24))
  g.add(self._table((("λ > 0  :    c ₁  =  c ₂     ⇒     c ₁  =  −  c ₂     ⇒     f  ≡  0",
                      ACCENT_B),
                     ("λ = 0  :    c ₁  =  0  ,     f  ≡  c ₀   =   cos 0 x", ACCENT_C),
                     ("λ < 0  :    2 c ₁ sin r π  =  0  ,     2 r c ₂ sin r π  =  0", ACCENT_A),
                     (f"det  =  4 r sin ² r π        r = 2  :  {DETPER_OK:.1e}"
                      f"        r = 2.5  :  {DETPER_BAD:.2f}", WARN),
                     ("r  =  n     ⇒     ( D ² + n ² ) f  =  0  ,     dim  =  2", ACCENT_A),
                     (f"Δ f   =   {max(a for _r, a, _b in PERRES):.1e}"
                      f"            Δ f ′   =   {max(b for _r, _a, b in PERRES):.1e}", ACCENT_B),
                     (f"W ( sin n x , cos n x )   =   − n   =   {WRPER:+.1f}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("三條在左右兩端的高度與斜率都對得上",
                  "all three match in height and in slope at the two ends"))
  return g.add(self._foot("換成型四。λ 大於零時兩個條件先逼出兩個係數相等，再逼出它們互為相反數，於是還是只有零解；λ 小於零時仍然得到 r 等於 n",
                          "now type 4: for positive lambda the two conditions force the constants equal and then opposite, so only zero survives, and for negative lambda we again get r equal to n",
                          ACCENT_A,
                          "但這次整個二維解空間都滿足邊界條件，所以每個特徵值都是二重的。λ 等於零時一次項被殺掉、常數項活下來，那個常數就是 cos 零乘 x",
                          "but this time the whole two-dimensional solution space meets the condition, so every eigenvalue is double; for lambda zero the x term dies and the constant lives, and that constant is the cosine of zero x"))

 # ── beat 6: Theorem 7.2 and the one orthogonality left ──────────
 def _thm72(self):
  oy, sy = -0.20, 1.50
  g = VGroup(self._base(oy),
             Line([self._xof(0.0, -PI, PI), oy - 0.06, 0],
                  [self._xof(0.0, -PI, PI), oy + 0.60, 0], color=DIM, stroke_width=1.3))
  g.add(self._plot(prod6, ACCENT_B, -PI, PI, oy, sy, sw=2.8))
  g.add(self._plot(run6, ACCENT_C, -PI, PI, oy, sy, sw=3.0))
  for x0 in (XL, XR):
   g.add(Dot([x0, oy, 0], radius=0.075, color=ACCENT_C))
  g.add(self._legend(XL + 0.06, ((ACCENT_B, "sin 2 x · cos 2 x", 2.00),
                                 (ACCENT_C, "∫ sin 2 t cos 2 t d t", 2.40)), y0=1.14, dy=0.24))
  g.add(self._table((("{ sin n x }   n ≥ 1      ∪      { cos n x }   n ≥ 0", ACCENT_A),
                     ("𝒞 ⁰ ( [ − π , π ] )", ACCENT_A),
                     ("sin n t · cos n t   =   ( 1 / 2 )  sin 2 n t", ACCENT_B),
                     (f"max  | ( sin n x , cos m x ) |   =   {SCMAX:.1e}", ACCENT_B),
                     (f"n ≠ m   :    max  | ( · , · ) |   =   {OFFMAX:.1e}", DIM),
                     (f"( sin n x , sin n x )  =  ( cos n x , cos n x )  =  "
                      f"{ORTH['ss'][(1, 1)]:.4f}", ACCENT_C),
                     (f"( cos 0 x , cos 0 x )   =   {ORTH['cc'][(0, 0)]:.4f}", WARN)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("紫線是藍線的累積面積，跑完正好回到零",
                  "the purple curve is the blue one's running area, and it comes back to zero"))
  return g.add(self._foot("定理 7.2 說 sin 與 cos 兩族合起來是負 π 到 π 上連續函數空間的正交基底。要補證的只有兩族互相正交這一件事",
                          "Theorem 7.2 makes the sines and the cosines together an orthogonal basis for the continuous functions on minus pi to pi, and only one orthogonality is left to check",
                          ACCENT_A,
                          "被積函數是奇函數，在對稱區間上積分必然是零。注意最後兩列：在這個區間上自己和自己是 π，唯獨那個常數是兩倍的 π",
                          "the integrand is odd, so its integral over a symmetric interval has to vanish; note the last two rows, where the square norm is pi except for the constant, which is twice that"))

 # ── beat 7: the density theorem, built by hand ──────────────────
 def _dense(self):
  oyu, syu = 0.22, 0.55
  oyl, syl = -0.62, 0.42 / SMAX73
  g = VGroup(self._plot(f73, ACCENT_A, 0.0, PI, oyu, syu, sw=3.2),
             self._poly(list(zip(XS73, YS73)), ACCENT_B, 0.0, PI, oyu, syu, sw=2.4))
  g.add(self._base(oyl))
  g.add(self._poly(G73, ACCENT_B, 0.0, PI, oyl, syl, sw=2.4))
  g.add(self._poly(H73, ACCENT_C, 0.0, PI, oyl, syl, sw=3.0))
  g.add(self._sym(1.15, "f", ACCENT_A, FS_TAG - 2, x=XL + 0.18, w=0.30),
        self._sym(1.15, "g", ACCENT_B, FS_TAG - 2, x=XL + 0.62, w=0.30))
  g.add(self._sym(0.03, "g ′", ACCENT_B, FS_TAG - 2, x=XL + 0.20, w=0.44),
        self._sym(0.03, "h", ACCENT_C, FS_TAG - 2, x=XL + 0.74, w=0.30))
  g.add(self._table((("f  ∈  𝒞 ( [ a , b ] )     ⇒     ‖ f − H ‖ ∞ < ε  ,    H ∈ 𝒞 ²",
                     ACCENT_A),
                     ("∫ ( h  −  g ′ )   =   0            | g  −  H |   ≤   δ Δ / 4",
                      ACCENT_B),
                     ("        n        ‖ f − g ‖ ∞        ‖ f − H ‖ ∞          δ Δ / 4", DIM),)
                    + tuple((f"      {n:2d}          {eg:.4f}              {eh:.4f}"
                             f"            {bd:.4f}", ACCENT_C)
                            for n, eg, eh, bd, _gh in DENS)
                    + (("‖ · ‖ ₂   ≤   ( b − a ) ¹ ᐟ ²  ‖ · ‖ ∞", ACCENT_A),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("中間兩欄的誤差一起往下掉，最後一欄是磨圓那一步的代價",
                  "the two errors fall together; the last column is the price of the rounding"))
  return g.add(self._foot("定理 7.3 說有兩階連續導數的函數在一致範數下稠密。證法很手工：先用折線逼近 f，上圖橘色是 f、藍色是折線",
                          "Theorem 7.3 says the twice continuously differentiable functions are dense in the uniform norm, proved by hand: first approximate f by a polygonal line, orange and blue above",
                          ACCENT_A,
                          "折線的導數是下圖的階梯函數，再把每個跳躍磨成一小段斜坡，讓磨掉和補上的面積相等。積回去得到的函數只在轉角附近和折線差一點點",
                          "its derivative is the step function below, and each jump is ground into a short ramp of equal area, so the primitive leaves the polygonal line only near the corners"))

 # ── beat 8: what the density is for, and what it is not ─────────
 def _why(self):
  oy, sy = -0.70, 1.05
  g = VGroup(self._base(oy))
  g.add(self._plot(lambda x: 1.0, ACCENT_A, 0.0, PI, oy, sy, sw=3.2))
  for N, col in zip(N8SHOW[:2], (ACCENT_B, ACCENT_C)):
   g.add(self._plot(lambda x, N=N: s8(N, x), col, 0.0, PI, oy, sy, sw=2.4))
  g.add(self._dash([XL + 0.06, oy, 0], [XL + 0.06, oy + sy, 0], WARN, n=7, sw=2.4))
  for x0 in (XL, XR):
   g.add(Dot([x0, oy, 0], radius=0.070, color=DIM))
  g.add(self._legend(XL + 0.52, ((ACCENT_A, "f  ≡  1", 1.00), (ACCENT_B, "S ₃", 0.60),
                                 (ACCENT_C, "S ₁ ₅", 0.80)), y0=1.14, dy=0.24))
  g.add(self._table((("M   ⊂   𝒞 ⁰ ( [ 0 , π ] )            ‖ · ‖ ₂", ACCENT_A),
                     ("M   :    f  ∈  𝒞 ²  ,     f ( 0 )  =  f ( π )  =  0", ACCENT_A),
                     ("§ 7  ,  7.3        Ch 5  ,  2.3", DIM),
                     ("f  ≡  1          f  ∉  M          b ₙ   =   4 / ( π n )", WARN),
                     ("        N          ‖ f − S ‖ ∞          ‖ f − S ‖ ₂", DIM),)
                    + tuple((f"      {N:2d}              {u:.4f}              {w:.4f}",
                             ACCENT_B) for N, u, w in ERR8),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("紅色虛線就是端點上那個永遠不會縮小的誤差",
                  "the red dashes are the endpoint error, and it never shrinks"))
  return g.add(self._foot("為什麼需要稠密性？因為前面證到的只是 M 這個子空間上的展開，而 M 要求兩階可微、端點為零。稠密性把 M 的基底升級成整個空間的基底",
                          "why is density needed? what was proved is an expansion on the subspace M, which asks for two derivatives and zero at the ends; density promotes a basis of M to one of the whole space",
                          ACCENT_A,
                          "但它只給二範數。左圖取 f 恆等於一，二範數誤差確實一直往下掉，一致誤差卻永遠卡在一，因為部分和在端點一定是零",
                          "it buys the two norm only: for f identically one the two-norm error does keep falling while the uniform error stays at one, because every partial sum vanishes at the ends"))

 # ── beat 9: exercise 7.6 ────────────────────────────────────────
 def _ex76(self):
  sy = 1.40 / F76HI
  oy = -0.95
  g = VGroup(self._base(oy),
             Line([self._xof(0.0, -PI, PI), oy - 0.06, 0],
                  [self._xof(0.0, -PI, PI), oy + 0.44, 0], color=DIM, stroke_width=1.3))
  g.add(self._plot(f76, ACCENT_A, -PI, PI, oy, sy, sw=3.2))
  for N, col in zip(E76SHOW, (WARN, ACCENT_C)):
   g.add(self._plot(lambda x, N=N: s76(N, x), col, -PI, PI, oy, sy, sw=2.4))
  for x0 in (XL, XR):
   g.add(Dot([x0, oy, 0], radius=0.070, color=ACCENT_A))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "π ² − x ²", 1.30), (WARN, "S ₁", 0.60),
                                 (ACCENT_C, "S ₄", 0.60)), y0=1.14, dy=0.24))
  g.add(self._table((("f  ∈  𝒞 ¹ ( [ − π , π ] )  ,     f ( − π )  =  f ( π )", ACCENT_A),
                     ("⇒          ‖ f  −  S ‖ ∞     →     0            § 7  ,  7.6", ACCENT_A),
                     ("7.2  :    f ∈ 𝒞 ²  ,   f ( − π ) = f ( π )  ,   f ′ ( − π ) = f ′ ( π )",
                      DIM),
                     (f"f  =  π ² − x ²          f ′ ( − π )  =  {d76(-PI):+.3f}"
                      f"          f ′ ( π )  =  {d76(PI):+.3f}", WARN),
                     (f"a ₀  =  2 π ² / 3  =  {A76_0:.4f}        "
                      f"a ₙ  =  4 ( − 1 ) ⁿ ⁺ ¹ / n ²", ACCENT_B),
                     ("        N   =   " + "        ".join(str(N) for N in N76), DIM),
                     ("‖ f − S ‖ ∞    " + "    ".join(f"{e:.3f}" for e in ERR76), ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩端的值相等，斜率卻差一個正負號",
                  "the two end values agree while the two slopes differ by a sign"))
  return g.add(self._foot("最強的兩個結果其實在習題裡。習題 7.6 要的是：f 只要有連續導數、兩個端點的值相等，Fourier 級數就一致收斂",
                          "the two strongest results are in the exercises: 7.6 asks that if f merely has a continuous derivative and takes equal values at the two endpoints, its Fourier series converges uniformly",
                          ACCENT_A,
                          "只要一階連續可微、而且兩端的值相等就夠，導數不必相等——左圖這個 f 的導數正好不相等，定理 7.2 管不到它。題目給的路線是對導數的級數逐項積分再用 Schwarz 不等式，這裡不做解答",
                          "a continuous first derivative and equal values at the ends is all it asks, and the slopes need not match -- the drawn f is exactly a case Theorem 7.2 cannot reach; the exercise's own route is term-by-term integration and the Schwarz inequality, and it is left at that"))

 # ── beat 10: exercise 7.10, and the end of chapter 6 ────────────
 def _ex710(self):
  oy, sy = -0.08, 1.45 / (M10HI - M10LO)
  g = VGroup(self._base(oy))
  g.add(self._plot(math.sin, ACCENT_A, 0.0, PI, oy, sy, sw=3.2))
  for d, col in zip(MACSHOW, (ACCENT_B, ACCENT_C)):
   g.add(self._plot(lambda x, d=d: mac((d + 1) // 2, x), col, 0.0, PI, oy, sy, sw=2.4))
  g.add(Dot([XR, oy, 0], radius=0.070, color=ACCENT_A))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "sin x", 0.90), (ACCENT_B, "d  =  3", 1.00),
                                 (ACCENT_C, "d  =  5", 1.00)), y0=1.14, dy=0.24))
  g.add(self._table((("‖ f  −  p ‖ ∞   <   ε            p  ∈  ℝ [ x ]", ACCENT_A),
                     ("f  ∈  𝒞 ( [ 0 , π ] )     →     g  ∈  𝒞 ²            § 7  ,  7.3",
                      ACCENT_B),
                     ("g ( t )  −  c t  −  d            0  ,  π     ↦     0", ACCENT_C),
                     ("Σ  b ₙ  sin n t            § 7  ,  7.1", ACCENT_A),
                     ("sin n t   =   Σ  ( − 1 ) ʲ ( n t ) ² ʲ ⁺ ¹ / ( 2 j + 1 ) !", ACCENT_B),
                     ("        d   =   " + "        ".join(str(d) for d, _e, _b in MAC), DIM),
                     ("‖ sin − T ‖ ∞    " + "   ".join(f"{e:.1e}" for _d, e, _b in MAC),
                      ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("左圖是 sin 自己的 Maclaurin 部分和，不是 f 的逼近",
                  "the figure is the sine's own Maclaurin sections, not an approximation of f"))
  return g.add(self._foot("習題 7.10 更漂亮：Weierstrass 逼近定理說，多項式在一致範數下稠密於連續函數空間",
                          "exercise 7.10 is lovelier still: the Weierstrass approximation theorem, that polynomials are dense in the continuous functions in the uniform norm",
                          ACCENT_A,
                          "路線是先用定理 7.3 換成兩階可微的函數，扣掉一條直線讓兩端歸零，再展成 sin 的級數，最後把每個 sin n x 換成它的 Maclaurin 部分和。細節留在習題裡，這裡不做解答",
                          "the route is Theorem 7.3 for a twice differentiable g, a line subtracted so it vanishes at both ends, an expansion in sines, and each sine replaced by a section of its Maclaurin series; the details stay in the exercise"))

 def stage(self):
  a, b, c = self._scarce(), self._operator(), self._solve1()
  d, e, f_ = self._eigen(), self._thm71(), self._period()
  h, i, j = self._thm72(), self._dense(), self._why()
  k, l = self._ex76(), self._ex710()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE84ZH, AdvCalcE84EN = make(AdvCalcE84Base, "84", prefix="AdvCalcE")
