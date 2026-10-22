"""advcalc E81 -- chapter 6, section 5 (book pp. 288-292): solving the
inhomogeneous equation, undetermined coefficients, variation of parameters,
Theorem 5.1, and the spring that is also a circuit.

The section has two halves and they disagree with each other, which is why the
eleven beats are cut where they are.  The first half is undetermined
coefficients: if g happens to lie in the null space of a constant coefficient S
then f lies in the null space of S composed with L, a space E80 described
completely, so one guesses a general element of it and matches coefficients.
Four beats cover it because the three cases -- plain exponential, trigonometric
right side, and a factor shared between L and S -- are three different guesses,
and the third is where the extra power of t comes from.  Then a whole beat is
spent on the book's own complaint, that this is not a linear right inverse at
all but a different trick for every g, because that complaint is the reason the
rest of the section exists.

The second half is variation of parameters, and it is section 3's first-order
formula pushed through psi.  Three beats carry it: the matrix w of the basis
and its derivatives, the cancellation of the middle w(0) -- which is the one
step that needs an argument, since integration commutes with a constant matrix
-- and then Theorem 5.1, which is what is left once g is the n-tuple with g
only in the last slot.  The worked example is y'' + y = 1/cos x, chosen by the
book precisely because 1/cos x solves no constant coefficient equation, so the
first half cannot touch it.

Every number is computed, and nearly all of it exactly.  Functions of the form
P(t) exp(lambda t) are carried as a polynomial and an exponent, as in E80, so
differentiating is (P' + lambda P) exp(lambda t) and applying a polynomial in D
is arithmetic: a residual of 1e-15 there really is zero.  The sec example falls
outside that family, so its second derivative is written out in closed form
rather than differenced, and the residual it leaves is 1e-16 instead of the
1e-4 a finite difference would have left.  The matrix facts (det w = -1 for the
sine-cosine basis, K' = T K, K(0) = I, and the middle factor cancelling) are
checked numerically over a grid of t and s.

Two pictures had to be designed around the warning that two curves must earn
their difference.  In beat 2 the particular solution really is the right side
times 0.909, so drawing only those two would have drawn one curve twice; a
third member of the affine family, f minus the homogeneous solution, is drawn
with them and it crosses the axis, and the caption says outright that the first
two are proportional.  In beat 10 the undamped and the lightly damped motion
would have had nearly the same frequency at the obvious choice of k, so k is
1.2 rather than 2: the damped frequency is 1.908 against 2, but the decaying
envelope and the monotone over-damped curve are what separate the three, and
the module pins that the over-damped one never changes sign while the other two
do.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import cmath
import numpy as np
from manim import Line, Rectangle, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC


FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these
GRID = (0.0, 0.3, 0.9, 1.7, 2.6, 4.0)       # where "is it zero" is tested


# ── exact arithmetic on  P(t) exp(lambda t)  ──────────────────────────
# Same representation as E80: a function is a list of (P, lambda) terms with P
# a list of coefficients, lowest power first. Differentiating a term is
# (P' + lambda P) exp(lambda t), so no finite difference enters anywhere and a
# residual of 1e-15 is a proof of zero rather than an estimate of it.
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


def tscale(terms, s):
 return [([s * c for c in P], lam) for P, lam in terms]


def tsub(A, B):
 return list(A) + tscale(B, -1.0)


def val(terms, t):
 return sum(sum(P[k] * t ** k for k in range(len(P))) * cmath.exp(lam * t)
            for P, lam in terms)


def size(terms, ts=GRID):
 return max(abs(val(terms, t)) for t in ts)


def pmul(A, B):
 out = [0.0] * (len(A) + len(B) - 1)
 for i, a in enumerate(A):
  for j, b in enumerate(B):
   out[i + j] += a * b
 return out


def ppow(A, n):
 out = [1.0]
 for _ in range(n):
  out = pmul(out, A)
 return out


def texp(i, lam):
 return [([0.0] * i + [1.0], complex(lam))]


def tcos(i, b, w):
 lam = complex(b, w)
 return [([0.0] * i + [0.5], lam), ([0.0] * i + [0.5], lam.conjugate())]


def tsin(i, b, w):
 lam = complex(b, w)
 return [([0.0] * i + [-0.5j], lam), ([0.0] * i + [0.5j], lam.conjugate())]


def rf(terms):
 """The real-valued function a term list stands for."""
 return lambda t: val(terms, t).real


# ── beat 2: y' - a y = exp(b t) ───────────────────────────────────────
A2, B2 = -0.4, 0.7
C2 = 1.0 / (B2 - A2)
L2 = [-A2, 1.0]                             # the operator D - a
G2 = texp(0, B2)
F2 = tscale(G2, C2)                         # the particular solution
H2 = tsub(F2, texp(0, A2))                  # another member of v + N
N2 = texp(0, A2)                            # a member of N, not of v + N
R2F = size(tsub(applyp(L2, F2), G2))
R2H = size(tsub(applyp(L2, H2), G2))
R2N = size(tsub(applyp(L2, N2), G2))
assert abs((B2 - A2) * C2 - 1.0) < 1e-15, "matching coefficients gives (b - a) c = 1"
assert R2F < 1e-13, "c exp(b t) really does solve y' - a y = exp(b t)"
assert R2H < 1e-13, "and so does every f + (member of N): the solutions are an affine set"
assert R2N > 1.0, "while a member of N alone solves the homogeneous equation, not this one"
# the two drawn curves f and g differ only by the factor c, and the caption says
# so; the third curve is what makes the picture about the affine family
RAT2 = max(abs(val(F2, t).real / val(G2, t).real - C2) for t in GRID)
assert RAT2 < 1e-14, "f is g times c exactly, which is why those two curves stay parallel"
T2A, T2B = -1.2, 2.0
assert min(val(H2, T2A + (T2B - T2A) * k / 200).real for k in range(201)) < -0.5 \
    and max(val(H2, T2A + (T2B - T2A) * k / 200).real for k in range(201)) > 0.5, \
    "the third curve changes sign in the window, so it cannot be mistaken for the other two"

# ── beat 3: y' - a y = cos b t ────────────────────────────────────────
SQ3 = A2 * A2 + B2 * B2
C31, C32 = B2 / SQ3, -A2 / SQ3
G3 = tcos(0, 0.0, B2)
F3 = tscale(tsin(0, 0.0, B2), C31) + tscale(tcos(0, 0.0, B2), C32)
S3 = [B2 * B2, 0.0, 1.0]                    # the annihilator D^2 + b^2
R3 = size(tsub(applyp(L2, F3), G3))
R3S = size(applyp(S3, G3))
R3SL = size(applyp(pmul(S3, L2), F3))
assert R3 < 1e-13, "b sin - a cos over a^2 + b^2 solves y' - a y = cos b t"
assert R3S < 1e-13, "the right side is annihilated by D^2 + b^2, which is why that S was chosen"
assert R3SL < 1e-13, "so the solution lies in the null space of S composed with L"
T3A, T3B = 0.0, 12.0
D3 = max(abs(val(tsub(F3, G3), T3A + (T3B - T3A) * k / 400).real) for k in range(401))
assert D3 > 0.9, "f and g are far apart somewhere in the window: not one curve drawn twice"
AMP3 = math.hypot(C31, C32)
PH3 = math.atan2(C32, C31)
assert abs(AMP3 - 1.0 / math.sqrt(SQ3)) < 1e-14, "the amplitude is the reciprocal root of a^2+b^2"
assert abs(math.pi / 2 - PH3) > 0.8, "and the phase differs from the cosine's by most of a radian"

# ── beat 4: a shared factor forces an extra power of t ────────────────
R4 = -0.6
L4 = ppow([-R4, 1.0], 2)                    # (D - r)^2
RR4 = [size(applyp(L4, texp(i, R4))) for i in range(3)]
assert RR4[0] < 1e-13 and RR4[1] < 1e-13, \
    "exp(r t) and t exp(r t) are killed outright, so no multiple of them can equal exp(r t)"
assert RR4[2] > 1.0, "only t^2 exp(r t) survives (D - r)^2, which is why the guess needs t^2"
C4 = 0.5
R4A = size(tsub(applyp(L4, tscale(texp(2, R4), C4)), texp(0, R4)))
assert R4A < 1e-13, "and with c = 1/2 it lands exactly on exp(r t)"
SL4 = ppow([-R4, 1.0], 3)
assert size(applyp(SL4, tscale(texp(2, R4), C4))) < 1e-13, "S composed with L is (D - r)^3"
# the same obstruction in first order: when b = a there is no c at all
R4Z = size(applyp([-A2, 1.0], texp(0, A2)))
assert R4Z < 1e-13 and size(texp(0, A2)) > 0.1, \
    "with b = a the guess c exp(a t) is annihilated, so (b - a) c = 1 has no solution"
# the drawn example: (D^2 + 1) f = sin t
P41 = [1.0, 0.0, 1.0]
F41 = tscale(tcos(1, 0.0, 1.0), -0.5)       # -t cos t / 2
R4B = size(tsub(applyp(P41, F41), tsin(0, 0.0, 1.0)))
assert R4B < 1e-13, "-t cos t / 2 solves (D^2 + 1) f = sin t"
T4A, T4B = 0.0, 10.0
ENV4 = max(abs(val(F41, T4A + (T4B - T4A) * k / 400).real) for k in range(401))
assert ENV4 > 4.0, "its amplitude has grown past four while the right side never leaves [-1, 1]"

# ── beats 6 to 9: the matrix w for the basis {sin, cos} ───────────────
TSYS = np.array([[0.0, 1.0], [-1.0, 0.0]])  # the first-order system for y'' + y = 0
IDN = np.eye(2)


def wmat(t):
 return np.array([[math.sin(t), math.cos(t)], [math.cos(t), -math.sin(t)]])


def wdot(t):
 return np.array([[math.cos(t), -math.sin(t)], [-math.sin(t), -math.cos(t)]])


TS6 = tuple(-1.2 + 0.3 * k for k in range(9))
W0 = wmat(0.0)
W0I = np.linalg.inv(W0)
T6 = 0.6
W6 = wmat(T6)
DW6 = float(np.linalg.det(W6))
K6 = W6 @ W0I
assert max(abs(float(np.linalg.det(wmat(t))) + 1.0) for t in TS6) < 1e-14, \
    "the determinant of w for the sine-cosine basis is identically minus one"
R6 = max(float(np.abs(wdot(t) @ W0I - TSYS @ (wmat(t) @ W0I)).max()) for t in TS6)
R6I = float(np.abs(wmat(0.0) @ W0I - IDN).max())
assert R6 < 1e-13, "so K(t) = w(t) w(0) inverse satisfies the transport equation K' = T K"
assert R6I < 1e-15, "and starts at the identity, which is what makes it the right inverse"
R7 = max(float(np.abs((wmat(t) @ W0I) @ (W0 @ np.linalg.inv(wmat(s)))
                      - wmat(t) @ np.linalg.inv(wmat(s))).max())
         for t in TS6 for s in TS6)
assert R7 < 1e-13, "the two middle w(0) factors really do cancel, for every t and s"

# ── beat 9: y'' + y = 1 / cos x on (-pi/2, pi/2) ──────────────────────
# v'' is written out in closed form rather than differenced, so the residual
# below is floating point noise and not a truncation error.
def v9(x):
 return x * math.sin(x) + math.cos(x) * math.log(math.cos(x))


def v9pp(x):
 return (math.cos(x) - x * math.sin(x) - math.cos(x) * math.log(math.cos(x))
         + math.sin(x) ** 2 / math.cos(x))


X9 = (-1.2, -0.6, -0.1, 0.0, 0.4, 1.0, 1.2)
R9 = max(abs(v9pp(x) + v9(x) - 1.0 / math.cos(x)) for x in X9)
assert R9 < 1e-13, "x sin x + cos x log cos x really solves y'' + y = 1 / cos x"
CP9 = [np.linalg.solve(wmat(x), np.array([0.0, 1.0 / math.cos(x)])) for x in X9]
assert max(abs(c[0] - 1.0) for c in CP9) < 1e-13, \
    "Theorem 5.1's system gives the first coefficient's derivative as one"
assert max(abs(c[1] + math.tan(x)) for c, x in zip(CP9, X9)) < 1e-13, \
    "and the second's as minus the tangent, which integrates to log cos x"
X9A, X9B = -1.52, 1.52                      # the drawn range, inside the interval
XAX, XBX = -1.70, 1.70                      # the axis range, so +-pi/2 is on screen
assert X9B < math.pi / 2 < XBX, "the endpoints of the interval are drawn, and are outside the curve"
V9MAX = max(v9(X9A + (X9B - X9A) * k / 300) for k in range(301))
# the window stops short of pi/2, so the solution tops out near 1.37 rather than
# at pi/2; what this pins is only that it is not a flat line in the window
assert V9MAX > 1.2, \
    "the particular solution climbs to over 1.2 at the ends: it is not flat in the window"

# ── beat 10: the spring, three dampings, and the circuit ──────────────
M10, C10 = 1.0, 4.0
OM = math.sqrt(C10 / M10)
FR = OM / (2.0 * math.pi)
KU, KO = 1.2, 5.0
assert abs(M10 * OM * OM - C10) < 1e-15, "Omega is the square root of c over m"
assert KU * KU < 4.0 * M10 * C10 < KO * KO, \
    "one damping is below the oscillating threshold and the other above it"
DEC = KU / (2.0 * M10)
WD = math.sqrt(4.0 * M10 * C10 - KU * KU) / (2.0 * M10)
RO = sorted(((-KO + s * math.sqrt(KO * KO - 4.0 * M10 * C10)) / (2.0 * M10)
             for s in (1.0, -1.0)), reverse=True)
AO = -RO[1] / (RO[0] - RO[1])
BO = RO[0] / (RO[0] - RO[1])
X_UN = tcos(0, 0.0, OM)
X_UD = list(tcos(0, -DEC, WD)) + tscale(tsin(0, -DEC, WD), DEC / WD)
X_OD = tscale(texp(0, RO[0]), AO) + tscale(texp(0, RO[1]), BO)
RES10 = [size(applyp([C10, k, M10], X)) for k, X in ((0.0, X_UN), (KU, X_UD), (KO, X_OD))]
assert all(r < 1e-12 for r in RES10), \
    "each drawn motion solves its own equation m x'' + k x' + c x = 0"
assert all(abs(val(X, 0.0).real - 1.0) < 1e-14 and abs(val(dall(X), 0.0).real) < 1e-13
           for X in (X_UN, X_UD, X_OD)), \
    "all three start released from rest at the same displacement, so only the damping differs"
T10A, T10B = 0.0, 6.0
SAMP = [T10A + (T10B - T10A) * k / 400 for k in range(401)]
MIN_OD = min(val(X_OD, t).real for t in SAMP)
assert MIN_OD > 0.0, "the over-damped curve never crosses the axis: it does not vibrate"
assert min(val(X_UD, t).real for t in SAMP) < -0.1, \
    "the under-damped one does, so the two damped curves are not the same shape"
AMP_UD = math.sqrt(1.0 + (DEC / WD) ** 2)      # the true amplitude of X_UD
assert abs(WD - OM) / OM < 0.06 and DEC > 0.5, \
    "the two frequencies are within six percent, so it is the envelope and not the frequency " \
    "that tells the damped curve from the undamped one"
assert AMP_UD > 1.03, \
    "and the envelope is that amplitude times the exponential, not the bare exponential: " \
    "the cosine and the sine part add in quadrature"


class AdvCalcE81Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 81

 MODE_LABEL = {
  0: {"zh": "要解的是什麼，兩條路", "en": "what is to be solved, and two routes"},
  1: {"zh": "待定係數的想法", "en": "the idea behind undetermined coefficients"},
  2: {"zh": "最簡單的例子", "en": "the simplest example"},
  3: {"zh": "三角函數的例子", "en": "the trigonometric example"},
  4: {"zh": "有公因式：多帶一個 t 的幂", "en": "a shared factor: one more power of t"},
  5: {"zh": "書上為什麼不滿意", "en": "why the book is not satisfied"},
  6: {"zh": "參數變異：那個矩陣", "en": "variation of parameters: that matrix"},
  7: {"zh": "中間那兩個抵消掉", "en": "the two middle factors cancel"},
  8: {"zh": "定理 5.1", "en": "theorem 5.1"},
  9: {"zh": "書上的例子", "en": "the book's worked example"},
  10: {"zh": "彈簧與電路，第 5 節結束",
       "en": "the spring and the circuit, and the end of section 5"},
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

  The same helper E79 and E80 use, and for the same reason: the t range is a
  parameter, so nothing has to be assumed about where t = 0 lands on screen."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 # ── beat 0: L f = g, and the affine set of solutions ────────────────
 def _setup(self):
  g = VGroup(self._box(-4.20, 0.95, "L ( f )   =   g", ACCENT_A, w=2.10, h=0.48,
                       size=FS_TAG))
  for x0, lab, col in ((-5.15, "S  ∘  L", WARN), (-3.25, "w ( t )", ACCENT_B)):
   g.add(self._arr([-4.20, 0.69, 0], [x0 + (0.35 if x0 < -4.2 else -0.35), 0.38, 0],
                   DIM, sw=3, tl=0.12))
   g.add(self._box(x0, 0.12, lab, col, w=1.40, h=0.48, size=FS_TAG))
  g.add(self._mid(-0.32, "只對某些 g", "only some g", WARN, FS_TAG - 3, x=-5.15, w=1.70))
  g.add(self._mid(-0.32, "對所有 g", "every g", ACCENT_B, FS_TAG - 3, x=-3.25, w=1.70))
  g.add(self._sym(-0.66, "f   =   v   +   Σ ᵢ  c ᵢ  u ᵢ", ACCENT_A, FS_TAG - 1,
                  x=-4.20, w=3.10))
  g.add(self._table((("L ( f )   =   g            L  :  𝒞 ⁿ ( I )  →  𝒞 ⁰ ( I )", ACCENT_A),
                     ("L ( v )   =   g            L ( u ᵢ )   =   0", ACCENT_B),
                     ("M   =   v   +   N            dim N   =   n", ACCENT_A),
                     ("f   =   v   +   Σ ᵢ  c ᵢ  u ᵢ", ACCENT_C),
                     ("S  ∘  L                    w ( t )  ∫  w ⁻ ¹", DIM),
                     ("§ 5 . 1   –   5 . 22", DIM)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("第三列就是那個仿射子空間",
                  "the third row is that affine subspace"))
  return g.add(self._foot("這一節要解的是非齊次方程。只要手上有任何一個特解 v，全部的解就是 v 加上齊次解空間，是一個仿射子空間",
                          "this section solves the inhomogeneous equation: given any one particular solution v, all of them are v plus the null space, an affine subspace",
                          ACCENT_A,
                          "書上給兩條路：待定係數法容易算，但只對某些右邊管用；參數變異法比較費事，卻對每一個右邊都成立。習題 5.1 到 5.22 在下一頁",
                          "the book gives two routes: undetermined coefficients is easy but only handles some right sides, variation of parameters is heavier and handles them all"))

 # ── beat 1: g in N(S) forces f into N(S o L) ───────────────────────
 def _idea(self):
  g = VGroup()
  g.add(Rectangle(width=1.95, height=1.52, color=ACCENT_B,
                  stroke_width=2.5).move_to([-4.85, 0.45, 0]))
  g.add(self._sym(0.93, "N ( S ∘ L )", ACCENT_B, FS_TAG - 2, x=-4.85, w=1.60))
  g.add(self._box(-4.85, 0.12, "N ( L )", ACCENT_A, w=1.45, h=0.46, size=FS_TAG - 2))
  g.add(self._box(-2.95, 0.45, "N ( S )", ACCENT_C, w=1.20, h=0.50, size=FS_TAG - 2))
  g.add(self._arr([-3.84, 0.45, 0], [-3.58, 0.45, 0], DIM, sw=3, tl=0.11))
  g.add(self._sym(0.74, "L", DIM, FS_TAG - 3, x=-3.71, w=0.26))
  g.add(self._sym(-0.48, "f   ∈   N ( S ∘ L )", ACCENT_A, FS_TAG - 1, x=-4.60, w=2.30))
  g.add(self._table((("S ( g )   =   0            S   =   p ( D )", ACCENT_A),
                     ("L ( f )  =  g      ⇒      ( S ∘ L ) ( f )  =  S ( g )  =  0", ACCENT_A),
                     ("N ( L )   ⊂   N ( S ∘ L )", ACCENT_B),
                     ("L [ N ( S ∘ L ) ]   ⊂   N ( S )", ACCENT_C),
                     ("dim N ( S ∘ L )  =  dim N ( L )  +  dim N ( S )", ACCENT_B),
                     ("§ 4", DIM)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("箭頭指的是 L 把大空間送進 N ( S )",
                  "the arrow is L carrying the big space into the null space of S"))
  return g.add(self._foot("如果 g 自己落在某個常係數算子 S 的零化空間裡，把 S 接在 L 後面複合起來，這個複合算子就把 f 殺掉了",
                          "if g itself lies in the null space of a constant coefficient S, then S composed after L annihilates f",
                          ACCENT_A,
                          "而常係數算子的零化空間上一集已經完全算清楚，是有限維的。所以答案一定在那個空間裡面，剩下的事只是把係數定出來",
                          "last episode described those null spaces completely and they are finite dimensional, so the answer sits inside one and only the coefficients are left to find"))

 # ── beat 2: y' - a y = exp(b t) ────────────────────────────────────
 def _expcase(self):
  oy, sy = -0.19, 0.28
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(rf(G2), ACCENT_A, T2A, T2B, oy, sy, sw=3.2))
  g.add(self._plot(rf(F2), ACCENT_B, T2A, T2B, oy, sy, sw=2.4))
  g.add(self._plot(rf(H2), ACCENT_C, T2A, T2B, oy, sy, sw=2.4))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "g  =  e ᵇ ᵗ", 1.20),
                                 (ACCENT_B, "f  =  c e ᵇ ᵗ", 1.40),
                                 (ACCENT_C, "f  −  e ᵃ ᵗ", 1.30)), y0=1.14, dy=0.24))
  g.add(self._table((("y ′  −  a y  =  e ᵇ ᵗ            f  =  c e ᵇ ᵗ", ACCENT_A),
                     ("( b − a ) c   =   1            c   =   1 / ( b − a )", ACCENT_A),
                     (f"a  =  {A2:+.2f}        b  =  {B2:+.2f}        c  =  {C2:.6f}", ACCENT_B),
                     ("                              ‖ ( D − a ) ·  −  g ‖", DIM),
                     (f"      c e ᵇ ᵗ                    {R2F:.2e}", ACCENT_B),
                     (f"      c e ᵇ ᵗ  −  e ᵃ ᵗ            {R2H:.2e}", ACCENT_C),
                     (f"      e ᵃ ᵗ                      {R2N:.3f}", WARN)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("藍線就是橘線乘上 c，紫線是另一個解",
                  "the blue curve is the orange one times c; the purple one is another solution"))
  return g.add(self._foot("最簡單的例子：右邊被 D 減 b 殺掉，所以拿常數乘同一個指數去試，代進去得到 b 減 a 再乘那個常數等於一",
                          "the simplest example: the right side is killed by D minus b, so try a constant times that exponential and get b minus a times the constant equal to one",
                          ACCENT_A,
                          "所以常數是 b 減 a 的倒數，約零點九零九——所以藍線是橘線的零點九零九倍，左半段兩條幾乎疊在一起。紫線減掉了一個齊次解，它會穿過軸，三條合起來才是那個仿射集合",
                          "the constant is the reciprocal of b minus a, about 0.909, which is why those two run parallel; subtracting a homogeneous solution gives the purple one, which crosses the axis"))

 # ── beat 3: y' - a y = cos b t ─────────────────────────────────────
 def _trigcase(self):
  oy, sy = 0.02, 0.42
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(rf(G3), ACCENT_A, T3A, T3B, oy, sy, sw=3.2))
  g.add(self._plot(rf(F3), ACCENT_B, T3A, T3B, oy, sy, sw=2.6))
  g.add(self._legend(XL + 1.34, ((ACCENT_A, "g  =  cos b t", 1.50),
                                 (ACCENT_B, "f", 0.30)), y0=1.14, dy=0.24))
  g.add(self._table((("y ′  −  a y  =  cos b t          S  =  D ²  +  b ²", ACCENT_A),
                     ("N ( S )   =   ⟨ sin b t  ,  cos b t ⟩", ACCENT_C),
                     ("f   =   c ₁ sin b t   +   c ₂ cos b t", ACCENT_A),
                     (f"c ₁  =  b / ( a ² + b ² )  =  {C31:.6f}", ACCENT_B),
                     (f"c ₂  =  − a / ( a ² + b ² )  =  {C32:.6f}", ACCENT_B),
                     (f"‖ ( D − a ) f − g ‖  =  {R3:.1e}      ‖ S ( g ) ‖  =  {R3S:.1e}",
                      ACCENT_B),
                     (f"max | f − g |   =   {D3:.4f}        ‖ ( S ∘ L ) f ‖  =  {R3SL:.1e}",
                      ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩條的振幅與相位都不同，不是同一條",
                  "the two differ in both amplitude and phase: they are not one curve"))
  return g.add(self._foot("右邊換成 cos b t 也一樣。它被 D 平方加 b 平方殺掉，那個零化空間的基底是 sin b t 與 cos b t",
                          "the same works for a cosine on the right: it is killed by D squared plus b squared, whose null space is spanned by the sine and the cosine",
                          ACCENT_A,
                          "所以拿這兩個的線性組合去試，比對係數解一個二元一次方程組，答案是 b 乘 sin 減掉 a 乘 cos，再除以 a 平方加 b 平方",
                          "so try a combination of those two, match coefficients and solve a two by two system: the answer is b times the sine less a times the cosine, over a squared plus b squared"))

 # ── beat 4: a shared factor, and the growing amplitude ─────────────
 def _resonance(self):
  oy, sy = 0.07, 0.19
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  for s in (1.0, -1.0):
   g.add(self._plot(lambda t, s=s: s * t / 2.0, DIM, T4A, T4B, oy, sy, sw=1.5))
  g.add(self._plot(math.sin, ACCENT_C, T4A, T4B, oy, sy, sw=2.0))
  g.add(self._plot(rf(F41), ACCENT_A, T4A, T4B, oy, sy, sw=3.0))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "f  =  − t cos t / 2", 2.00),
                                 (ACCENT_C, "g  =  sin t", 1.20),
                                 (DIM, "±  t / 2", 0.90)), y0=1.14, dy=0.24))
  g.add(self._table((("( D − r ) ² f  =  e ʳ ᵗ          S ∘ L  =  ( D − r ) ³", ACCENT_A),
                     ("            i                ‖ ( D − r ) ² ( t ⁱ e ʳ ᵗ ) ‖", DIM),
                     (f"            0                {RR4[0]:.2e}", WARN),
                     (f"            1                {RR4[1]:.2e}", WARN),
                     (f"            2                {RR4[2]:.4f}", ACCENT_B),
                     (f"f  =  t ² e ʳ ᵗ / 2          ‖ ( D − r ) ² f − e ʳ ᵗ ‖  =  {R4A:.1e}",
                      ACCENT_A),
                     (f"( D ² + 1 ) ( − t cos t / 2 )  −  sin t      {R4B:.1e}", ACCENT_C)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("紫線始終在正負一之間，橘線沒有上界",
                  "the purple curve stays inside plus and minus one; the orange one has no bound"))
  return g.add(self._foot("如果 L 與 S 有公因式就要多帶一個 t 的幂。前兩列是零，表示指數與 t 乘指數都被殺光，怎麼乘常數都湊不出右邊",
                          "a factor shared by L and S forces an extra power of t: the first two rows are zero, so no multiple of those can ever equal the right side",
                          ACCENT_A,
                          "第三列才不是零，所以要試 t 平方乘指數，係數是二分之一。圖上畫的是書上第二個例子，振幅隨 t 線性長大，這就是共振的雛形",
                          "only the third row survives, so the guess needs t squared and the constant is one half; the picture is the book's second example, whose amplitude grows linearly"))

 # ── beat 5: a trick per g, against one process for all ─────────────
 def _complaint(self):
  g = VGroup()
  ys = (1.08, 0.78, 0.48)
  gs = ("e ᵇ ᵗ", "cos b t", "1 / cos t")
  tries = (("c e ᵇ ᵗ", ACCENT_B), ("c ₁ sin + c ₂ cos", ACCENT_B), ("?", WARN))
  for y, lab, (tr, col) in zip(ys, gs, tries):
   g.add(self._sym(y, lab, ACCENT_A, FS_TAG - 3, x=-5.56, w=0.92))
   g.add(self._arr([-5.02, y, 0], [-4.62, y, 0], DIM, sw=2.5, tl=0.10))
   g.add(self._sym(y, tr, col, FS_TAG - 3, x=-3.64, w=1.80))
  g.add(self._dash([XL, 0.26, 0], [XR, 0.26, 0], DIM, n=18, sw=1.4))
  g.add(self._box(-3.30, -0.26, "w ( t ) ∫ w ⁻ ¹", ACCENT_A, w=1.90, h=0.50,
                  size=FS_TAG - 3))
  for k, y in enumerate((0.04, -0.26, -0.56)):
   g.add(self._sym(y, gs[k], ACCENT_A, FS_TAG - 3, x=-5.56, w=0.92))
   g.add(self._arr([-5.02, y, 0], [-4.32, -0.26 + (y + 0.26) * 0.35, 0],
                   DIM, sw=2.5, tl=0.10))
  g.add(self._table((("L ( f )  =  g        ⇒        f  =  R ( g )", ACCENT_A),
                     ("L  ∘  R   =   I", ACCENT_A),
                     ("R ( g ₁ + g ₂ )   =   R ( g ₁ )   +   R ( g ₂ )", ACCENT_B),
                     ("g ₁  ↦  S ₁        g ₂  ↦  S ₂        g ₃  ↦  ?", WARN),
                     ("g ᵢ   ↦   R            R   ≠   R ( g )", ACCENT_A),
                     ("§ 5", DIM)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("上半每個 g 換一次招，下半只有一個流程",
                  "above, each g needs its own trick; below, one process takes them all"))
  return g.add(self._foot("書上對待定係數法並不滿意。它違反了整章的哲學：解方程應該是一個線性的右反元素，一個固定的流程把任何 g 送回對應的 f",
                          "the book is not satisfied: this violates the chapter's philosophy that solving should be a linear right inverse, one fixed process sending any g back to an f",
                          ACCENT_A,
                          "可是待定係數法隨著 g 換算子、換試探的形式，遇到不是常係數方程的解的 g 就完全用不上。它只是好算而已",
                          "undetermined coefficients changes its operator and its guessed form with every g, and has nothing at all to offer when g solves no constant coefficient equation"))

 # ── beat 6: the matrix w, and the transport map ────────────────────
 def _wmatrix(self):
  gw, _ = self._numgrid(-5.10, 0.48, [[f"{v:+.4f}" for v in row] for row in W6],
                        dx=0.78, dy=0.40, size=FS_TAG - 5, color=ACCENT_B)
  gk, _ = self._numgrid(-3.26, 0.48, [[f"{v:+.4f}" for v in row] for row in K6],
                        dx=0.78, dy=0.40, size=FS_TAG - 5, color=ACCENT_C)
  g = VGroup(gw, gk)
  g.add(self._arr([-4.28, 0.48, 0], [-3.96, 0.48, 0], DIM, sw=2.5, tl=0.10))
  g.add(self._sym(1.06, "·   w ( 0 ) ⁻ ¹", DIM, FS_TAG - 4, x=-4.12, w=1.10))
  g.add(self._sym(-0.12, f"w ( t )   ,   t  =  {T6:.2f}", ACCENT_B, FS_TAG - 3,
                  x=-5.10, w=1.70))
  g.add(self._sym(-0.12, "K ₜ", ACCENT_C, FS_TAG - 3, x=-3.26, w=0.44))
  g.add(self._sym(-0.52, "w ᵢ ⱼ ( t )   =   u ⱼ ⁽ ⁱ ⁻ ¹ ⁾ ( t )", ACCENT_A, FS_TAG - 2,
                  x=-4.20, w=3.20))
  g.add(self._table((("u ₁  =  sin t            u ₂  =  cos t", ACCENT_B),
                     ("w ᵢ ⱼ ( t )   =   u ⱼ ⁽ ⁱ ⁻ ¹ ⁾ ( t )", ACCENT_A),
                     (f"det w ( t )   =   {DW6:+.6f}", ACCENT_C),
                     ("K ₜ   =   w ( t ) · w ( 0 ) ⁻ ¹            K ₀   =   I", ACCENT_A),
                     (f"‖ K ′ − T ∘ K ‖  =  {R6:.1e}        ‖ K ₀ − I ‖  =  {R6I:.1e}",
                      ACCENT_B),
                     ("§ 3  ,  3.3", DIM)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("行列式不隨 t 變，所以每個 t 都可逆",
                  "the determinant does not move with t, so w is invertible at every t"))
  return g.add(self._foot("第二條路叫參數變異，它真的是一個右反元素，對每個 g 都管用，連變係數的 L 都反得了",
                          "the second route, variation of parameters, really is a right inverse: it works for every g and even inverts a variable coefficient L",
                          ACCENT_A,
                          "把已知的 n 個獨立解與它們各階導數排成矩陣 w，它的行就是一階系統解空間的基底。乘上 w 在零的反矩陣就得到第 3 節那個轉移映射",
                          "stack the known solutions and their derivatives into a matrix w whose columns are a basis for the first order system; times the inverse of w at zero it is section three's transport map"))

 # ── beat 7: the middle factor cancels ──────────────────────────────
 def _cancel(self):
  g = VGroup(self._sym(1.10, "f ( t )   =   K ₜ  ∫  ( K ₛ ) ⁻ ¹ ( g ( s ) ) d s",
                       ACCENT_A, FS_TAG - 2, x=-4.20, w=3.30))
  xs = (-5.50, -4.64, -3.78, -2.92)
  labs = (("w ( t )", ACCENT_B), ("w ( 0 ) ⁻ ¹", WARN),
          ("w ( 0 )", WARN), ("w ( s ) ⁻ ¹", ACCENT_C))
  for x0, (lab, col) in zip(xs, labs):
   g.add(self._box(x0, 0.68, lab, col, w=0.80, h=0.46, size=FS_TAG - 5))
  g.add(Line([-5.03, 0.26, 0], [-3.39, 0.26, 0], color=WARN, stroke_width=2.0),
        Line([-5.03, 0.26, 0], [-5.03, 0.40, 0], color=WARN, stroke_width=2.0),
        Line([-3.39, 0.26, 0], [-3.39, 0.40, 0], color=WARN, stroke_width=2.0))
  g.add(self._sym(0.06, "=   I", WARN, FS_TAG - 3, x=-4.21, w=0.70))
  g.add(self._arr([-4.21, -0.14, 0], [-4.21, -0.36, 0], DIM, sw=2.5, tl=0.10))
  g.add(self._sym(-0.60, "f ( t )   =   w ( t )  ∫  w ( s ) ⁻ ¹ · g ( s ) d s",
                  ACCENT_A, FS_TAG - 2, x=-4.20, w=3.30))
  g.add(self._table((("f ( t )   =   K ₜ  ∫  ( K ₛ ) ⁻ ¹ ( g ( s ) ) d s", ACCENT_A),
                     ("K ₜ  =  w ( t ) · w ( 0 ) ⁻ ¹        ( K ₛ ) ⁻ ¹  =  w ( 0 ) · w ( s ) ⁻ ¹",
                      ACCENT_B),
                     ("∫ ( A · h )   =   A · ∫ h            A ′   =   0", ACCENT_C),
                     ("f ( t )   =   w ( t )  ∫  w ( s ) ⁻ ¹ · g ( s ) d s", ACCENT_A),
                     (f"‖ w ( t ) w ( 0 ) ⁻ ¹ w ( 0 ) w ( s ) ⁻ ¹  −  w ( t ) w ( s ) ⁻ ¹ ‖  =  {R7:.1e}",
                      ACCENT_B),
                     ("k ( s )  =  w ( s ) ⁻ ¹ · g ( s )        w ( s ) · k ( s )  =  g ( s )",
                      ACCENT_A)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("紅色那兩個相鄰，乘起來是單位矩陣",
                  "the two red factors stand next to each other and multiply to the identity"))
  return g.add(self._foot("把矩陣代進第 3 節那條解公式，會出現 w 在 t 乘上 w 在零的反矩陣，再乘上一個本身含有 w 在零的積分",
                          "substituting the matrix into section three's formula gives w at t times the inverse of w at zero, times an integral that itself carries w at zero",
                          ACCENT_A,
                          "因為積分與常矩陣相乘可以交換，那個常矩陣可以搬進積分裡，中間兩個就相鄰而抵消，剩下的就是真正要用的公式",
                          "integration commutes with multiplication by a constant matrix, so that factor moves inside, the two meet and cancel, and what is left is the formula actually used"))

 # ── beat 8: theorem 5.1 ────────────────────────────────────────────
 def _thm51(self):
  gw, _ = self._numgrid(-5.20, 0.48,
                        [[f"w {a} {b}" for b in ("₁", "₂", "₃")]
                         for a in ("₁", "₂", "₃")],
                        dx=0.40, dy=0.38, size=FS_TAG - 5, color=ACCENT_B, hotrow=2,
                        hotcolor=ACCENT_C)
  g = VGroup(gw)
  g.add(self._sym(0.48, "·", DIM, FS_TAG - 2, x=-4.40, w=0.16))
  g.add(self._column(-3.95, 0.48, [("k ₁", ACCENT_A), ("k ₂", ACCENT_A), ("k ₃", ACCENT_A)],
                     dy=0.38, size=FS_TAG - 5))
  g.add(self._sym(0.48, "=", DIM, FS_TAG - 2, x=-3.50, w=0.20))
  g.add(self._column(-3.05, 0.48, [("0", DIM), ("0", DIM), ("g", ACCENT_C)],
                     dy=0.38, size=FS_TAG - 5))
  g.add(self._sym(-0.34, "Σ ᵢ  c ᵢ ′  u ᵢ ⁽ ʲ ⁾   =   0        j  ≤  n − 2",
                  ACCENT_A, FS_TAG - 3, x=-4.20, w=3.30))
  g.add(self._sym(-0.64, "Σ ᵢ  c ᵢ ′  u ᵢ ⁽ ⁿ ⁻ ¹ ⁾   =   g        f  =  Σ ᵢ  c ᵢ  u ᵢ",
                  ACCENT_A, FS_TAG - 3, x=-4.20, w=3.30))
  g.add(self._table((("g   =   ⟨ 0 , … , 0 , g ⟩", ACCENT_A),
                     ("Σ ⱼ  w ᵢ ⱼ ( s )  k ⱼ ( s )   =   0            i   <   n", ACCENT_B),
                     ("Σ ⱼ  w ₙ ⱼ ( s )  k ⱼ ( s )   =   g ( s )", ACCENT_C),
                     ("f ( t )  =  Σ ⱼ  w ₁ ⱼ ∫ k ⱼ ( s ) d s  =  Σ ⱼ  u ⱼ ( t ) c ⱼ ( t )",
                      ACCENT_A),
                     ("c ᵢ ′   =   k ᵢ                        5 . 1", ACCENT_A),
                     (f"det w   ≠   0            {DW6:+.4f}", ACCENT_B)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("右邊只有最後一格不是零，紫色那一列",
                  "only the last slot of the right side is nonzero, the purple row"))
  return g.add(self._foot("現在把右邊取成前面全是零、只有最後一項是 g 的向量，矩陣方程就塌成一組很乾淨的條件",
                          "now take the right side to be the vector that is zero everywhere except for g in the last slot, and the matrix equation collapses into a clean system",
                          ACCENT_A,
                          "各階導數的加權和前 n 減一條全是零，最後一條等於 g，未知數是那些係數的導數。這就是定理 5.1，解出導數再積回去，f 就是係數乘基底的和",
                          "the first n minus one weighted sums vanish and the top one equals g; that is Theorem 5.1, and integrating the derivatives back gives f as the coefficients times the basis"))

 # ── beat 9: y'' + y = 1 / cos x ────────────────────────────────────
 def _secant(self):
  # the curves are even, so they rise at both ends; the vertical scale keeps
  # their tops below the legend rather than threading the legend between them
  oy, sy = -0.30, 0.52
  xa, xb = self._xof(X9A, XAX, XBX), self._xof(X9B, XAX, XBX)
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  for xx in (-math.pi / 2, math.pi / 2):
   px = self._xof(xx, XAX, XBX)
   g.add(self._dash([px, oy - 0.26, 0], [px, oy + 0.95, 0], WARN, n=9, sw=1.5))
  g.add(self._plot(lambda x: x * math.sin(x), ACCENT_B, X9A, X9B, oy, sy, sw=2.2,
                   xl=xa, xr=xb))
  g.add(self._plot(lambda x: math.cos(x) * math.log(math.cos(x)), ACCENT_C,
                   X9A, X9B, oy, sy, sw=2.2, xl=xa, xr=xb))
  g.add(self._plot(v9, ACCENT_A, X9A, X9B, oy, sy, sw=3.2, xl=xa, xr=xb))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "v", 0.30), (ACCENT_B, "x sin x", 1.10),
                                 (ACCENT_C, "( log cos x ) cos x", 2.10)),
                     y0=1.14, dy=0.24))
  g.add(self._table((("y ″  +  y   =   1 / cos x", ACCENT_A),
                     ("u ₁ = sin x      u ₂ = cos x      I = ( − π / 2 , π / 2 )", ACCENT_B),
                     ("c ₁ ′ sin x  +  c ₂ ′ cos x   =   0", ACCENT_A),
                     ("c ₁ ′ cos x  −  c ₂ ′ sin x   =   1 / cos x", ACCENT_A),
                     ("c ₁ ′  =  1        c ₂ ′  =  − tan x", ACCENT_C),
                     ("c ₁  =  x        c ₂  =  log cos x", ACCENT_C),
                     (f"‖ v ″ + v − 1 / cos x ‖   =   {R9:.1e}", ACCENT_B)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("橘線是藍線加紫線，紅虛線是區間的兩端",
                  "the orange curve is the blue plus the purple; the red dashes are the endpoints"))
  return g.add(self._foot("書上的例子是 y 兩撇加 y 等於 cos x 的倒數。齊次解的基底是 sin x 與 cos x，但右邊不是任何常係數方程的解",
                          "the book's example is y double prime plus y equal to one over the cosine; the homogeneous basis is the sine and the cosine, but that right side solves no constant coefficient equation",
                          ACCENT_A,
                          "所以待定係數法用不上，只能用定理。解出兩個係數的導數分別是一與負的正切，積回去就得到畫面上那條橘線。區間必須限在正負二分之π之間",
                          "so only the theorem applies: the two derivatives come out as one and minus the tangent, and integrating gives the orange curve, on an interval that has to stop at plus and minus half pi"))

 # ── beat 10: the spring, the damping, and the circuit ──────────────
 def _spring(self):
  oy, sy = 0.22, 0.62
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  for s in (1.0, -1.0):
   # the amplitude factor matters: the solution is cos + (delta/omega) sin, whose
   # peak is sqrt(1 + (delta/omega)^2) times the bare exponential, so the bare one
   # would be crossed by the very first peak
   g.add(self._plot(lambda t, s=s: s * AMP_UD * math.exp(-DEC * t), DIM,
                    T10A, T10B, oy, sy, sw=1.5))
  g.add(self._plot(rf(X_UN), ACCENT_A, T10A, T10B, oy, sy, sw=2.8))
  g.add(self._plot(rf(X_UD), ACCENT_B, T10A, T10B, oy, sy, sw=2.8))
  g.add(self._plot(rf(X_OD), ACCENT_C, T10A, T10B, oy, sy, sw=2.8))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "k  =  0", 1.00),
                                 (ACCENT_B, "k ²  <  4 m c", 1.60),
                                 (ACCENT_C, "k ²  >  4 m c", 1.60),
                                 (DIM, "±  A e ⁻ ᵏ ᵗ ᐟ ² ᵐ", 1.80)), y0=1.14, dy=0.22))
  g.add(self._table((("m d ² x / d t ²  +  c x  =  0            x  =  a cos Ω t", ACCENT_A),
                     (f"m = {M10:.1f}    c = {C10:.1f}    Ω = {OM:.4f}    Ω / 2 π = {FR:.4f}",
                      ACCENT_B),
                     ("m d ² x / d t ²  +  k d x / d t  +  c x  =  0", ACCENT_A),
                     (f"k = {KU:.1f}    k ² < 4 m c    ω = {WD:.4f}    k / 2 m = {DEC:.1f}",
                      ACCENT_B),
                     (f"k = {KO:.1f}      k ² > 4 m c      {RO[0]:+.1f}  ,  {RO[1]:+.1f}",
                      ACCENT_C),
                     ("‖ m x ″ + k x ′ + c x ‖   =   "
                      + "  ".join(f"{r:.0e}" for r in RES10), ACCENT_B),
                     ("L d ² x / d t ²  +  R d x / d t  +  x / C  =  a sin ω t", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("三條的起點相同，只有阻尼不同",
                  "the three start from the same release; only the damping differs"))
  return g.add(self._foot("最後是彈簧。質量乘加速度加上彈性係數乘位移等於零，解是角頻率等於根號 c 除以 m 的正弦波，每單位時間振盪 Ω 除以二π 次",
                          "the section ends with a spring: mass times acceleration plus stiffness times displacement is zero, a sine of angular frequency the root of c over m",
                          ACCENT_A,
                          "加上摩擦後阻尼小的仍然永遠振盪，只是振幅照灰色包絡線衰減；阻尼夠大就根本不振動。同一個方程也治理電路，外加週期電壓時就出現相位與共振",
                          "with friction, light damping still oscillates inside the grey envelope while heavy damping does not vibrate at all; the same equation governs a circuit, where a driving voltage brings phase and resonance"))

 def stage(self):
  a, b, c = self._setup(), self._idea(), self._expcase()
  d, e, f_ = self._trigcase(), self._resonance(), self._complaint()
  h, i, j = self._wmatrix(), self._cancel(), self._thm51()
  k, l = self._secant(), self._spring()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE81ZH, AdvCalcE81EN = make(AdvCalcE81Base, "81", prefix="AdvCalcE")
