"""advcalc E79 -- chapter 6, section 4 (book pp. 281-284, first half): the
nth-order linear equation, Theorem 4.1, and reduction of order.

Section 4 opens by doing to the nth-order equation what section 1 did to the
first-order one: line f up with its first n-1 derivatives and the equation
becomes a first-order system on W^n.  Everything section 3 proved then carries
over -- psi is an isomorphism of solution spaces, evaluation at any one instant
is an isomorphism onto W^n, and the complement of the solution space is the
functions vanishing to order n-1 there.  Theorem 4.1 is that list written out
for the scalar case, where the equation is the null space of one operator L.

After that the section turns practical, and is honest about the limits: there is
no general method for finding a basis of the null space.  Three things do work.
The first-order equation integrates outright.  Constant coefficients have a
complete answer (that is E80).  And in between, if one solution u is already
known, v = c u reduces the problem by one order, because the terms of L(v) with
no derivative of c add up to c L(u) = 0 and the rest is an operator of order
n-1 applied to c'.  For n = 2 that finishes the job, since order one integrates.

Everything on screen is computed here.  The worked example is the book's
y'' - 2y/t^2 = 0, whose second solution comes out as 1/t; the reduction is
verified against a test c (not only against the answer), the two solutions'
Wronskian is pinned at -3, and the singular example t y'' + y' = 0 is carried
along to show what the regular hypothesis is buying.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these


def d1(f, t, h=1e-5):
 return (f(t + h) - f(t - h)) / (2 * h)


def d2(f, t, h=1e-4):
 return (f(t + h) - 2 * f(t) + f(t - h)) / (h * h)


# ── the example carried through the episode: y'' - 2 y / t^2 = 0 ──────
def L2(f, t):
 """The book's operator, applied numerically."""
 return d2(f, t) - 2.0 * f(t) / (t * t)


def u(t):
 return t * t


def v(t):
 return 1.0 / t


for _t in (0.6, 1.0, 1.7, 2.4):
 assert abs(L2(u, _t)) < 1e-6, "t^2 solves it, which is the solution found by inspection"
 assert abs(L2(v, _t)) < 1e-6, "and 1/t is the one reduction of order hands back"

# the Wronskian is a nonzero constant, so the two are independent: -3 exactly
WR = [(t, u(t) * d1(v, t) - d1(u, t) * v(t)) for t in (0.6, 1.0, 1.7, 2.4)]
assert all(abs(w + 3.0) < 1e-6 for _t, w in WR), "u v' - u' v = -3 at every t"

# they take the same value at t = 1 and differ only in the derivative there,
# which is the point of beat 10: the isomorphism is of pairs, not of values
PAIRS = [("u", u(1.0), d1(u, 1.0)), ("v", v(1.0), d1(v, 1.0))]
assert abs(PAIRS[0][1] - PAIRS[1][1]) < 1e-6, "same value at t = 1"
assert abs(PAIRS[0][2] - PAIRS[1][2]) > 2.9, "different derivative there"
DET1 = PAIRS[0][1] * PAIRS[1][2] - PAIRS[0][2] * PAIRS[1][1]
assert abs(DET1 + 3.0) < 1e-6, "and the 2 by 2 evaluation matrix has determinant -3"


# ── beat 2: n initial values, one solution ────────────────────────────
def sol(A, B):
 return lambda t: A * t * t + B / t


# three solutions sharing the value 1 at t = 1 and differing in the slope there
INIT = []
for _s in (2.0, -1.0, 0.5):
 _A = (1.0 + _s) / 3.0
 INIT.append((_s, _A, 1.0 - _A))
for _s, _A, _B in INIT:
 _f = sol(_A, _B)
 assert abs(_f(1.0) - 1.0) < 1e-12 and abs(d1(_f, 1.0) - _s) < 1e-6
 assert abs(L2(_f, 1.4)) < 1e-6, "each one is a solution"
assert len({round(A, 6) for _s, A, _B in INIT}) == 3, "and the three are genuinely different"


# ── beat 3: the coefficients of the example, as an operator L ─────────
def a0(t):
 return -2.0 / (t * t)


COEF = [(t, 1.0, 0.0, a0(t)) for t in (0.7, 1.0, 1.5, 2.2)]


# ── beat 4: the singular example  t y'' + y' = 0 ──────────────────────
def Lsing(f, t):
 return t * d2(f, t) + d1(f, t)


def ylog(t):
 return math.log(t)


def yone(t):
 return 1.0


for _t in (0.3, 0.8, 1.6, 2.3):
 assert abs(Lsing(ylog, _t)) < 1e-4, "log t solves the singular equation away from 0"
 assert abs(Lsing(yone, _t)) < 1e-9, "and so does every constant"
# t y' = k is the first integral, so y' = k/t: unbounded at 0 unless k = 0.
# That is the whole collapse: on an interval around 0 only the constants survive.
SING = [(t, ylog(t), d1(ylog, t)) for t in (0.5, 0.2, 0.05, 0.01)]
assert all(abs(dy - 1.0 / t) < 1e-3 * max(1.0, 1.0 / t) for t, _y, dy in SING)
assert SING[-1][2] > 50.0, "the derivative blows up as the origin is approached"
DIM_AWAY, DIM_ACROSS = 2, 1


# ── beats 5 and 6: Theorem 4.1's right inverse, computed ──────────────
# L(f) = 1 has the particular solution t^2 log t / 3; correcting it by the
# element of N that matches its value and derivative at t = 1 gives the one the
# complement M_1 picks out, the image of 1 under the right inverse.
def vpart(t):
 return t * t * math.log(t) / 3.0


A_COR, B_COR = 1.0 / 9.0, -1.0 / 9.0


def rinv(t):
 return vpart(t) - (A_COR * t * t + B_COR / t)


for _t in (0.7, 1.0, 1.6, 2.1):
 assert abs(L2(vpart, _t) - 1.0) < 1e-4, "t^2 log t / 3 is a particular solution"
 assert abs(L2(rinv, _t) - 1.0) < 1e-4, "so is the corrected one"
assert abs(rinv(1.0)) < 1e-12 and abs(d1(rinv, 1.0)) < 1e-6, \
    "and the corrected one vanishes to order n - 1 at t = 1, so it lies in M_1"
RINV = [(t, vpart(t), rinv(t)) for t in (0.7, 1.0, 1.6, 2.1)]
AFFINE = [(0.0, 0.0), (0.12, 0.0), (0.0, 0.25), (-0.10, 0.18)]
for _A, _B in AFFINE:
 assert abs(L2(lambda t, A=_A, B=_B: rinv(t) + A * t * t + B / t, 1.3) - 1.0) < 1e-4, \
     "every member of the affine family solves the same inhomogeneous equation"

# ── beat 7: the first-order equation, solved outright ─────────────────
FIRST = []
for _name, _a, _y in (("1", lambda t: 1.0 / t, lambda t: 1.0 / t),
                      ("2", lambda t: 2.0 * t, lambda t: math.exp(-t * t))):
 _rows = [(t, _y(t), d1(_y, t) + _a(t) * _y(t)) for t in (0.6, 1.2, 1.8, 2.4)]
 assert all(abs(r) < 1e-6 for _t, _yy, r in _rows), \
     "the exponential of minus the integral of a really does solve y' + a y = 0"
 FIRST.append((_name, _rows))


# ── beats 8 and 9: the reduction, verified against a test c ───────────
def S1(w, t):
 """The order n-1 operator L(c u) = S(c') leaves behind, for this example."""
 return t * t * d1(w, t) + 4.0 * t * w(t)


def ctest(t):
 return math.sin(t)


def vtest(t):
 return t * t * ctest(t)


RED = []
for _t in (0.6, 1.1, 1.7, 2.3):
 _lhs = L2(vtest, _t)
 _rhs = S1(lambda s: d1(ctest, s), _t)
 RED.append((_t, _lhs, _rhs))
assert all(abs(a - b) < 2e-3 for _t, a, b in RED), \
    "L(c u) = S(c'), with the c L(u) term gone, for a c that is not the answer"


# and the reduced equation, solved: w' + (4/t) w = 0 gives w = t^-4, c = t^-3
def wred(t):
 return t ** -4.0


for _t in (0.6, 1.2, 2.0):
 assert abs(S1(wred, _t)) < 1e-6, "t^-4 spans the null space of S"
C_SCALE = -1.0 / 3.0                        # the integral of t^-4 is -1/(3 t^3)
for _t in (0.7, 1.4, 2.2):
 assert abs(C_SCALE * _t ** -3.0 * u(_t) - C_SCALE * v(_t)) < 1e-12, \
     "so c u is 1/t up to the scalar, which is all a basis needs"
ORD_L, ORD_S = 2, 1


class AdvCalcE79Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 79

 MODE_LABEL = {
  0: {"zh": "第 4 節：n 階線性方程", "en": "section 4: the nth-order equation"},
  1: {"zh": "ψ 把兩個解空間接起來", "en": "psi joins the two solution spaces"},
  2: {"zh": "n 個初始值決定唯一一個解", "en": "n initial values, exactly one solution"},
  3: {"zh": "取 W 是實數線：一個算子 L", "en": "taking W real: a single operator"},
  4: {"zh": "正則與奇異", "en": "regular and singular"},
  5: {"zh": "定理 4.1", "en": "theorem 4.1"},
  6: {"zh": "實務上分成兩件事", "en": "the problem splits in two"},
  7: {"zh": "一階：直接積出來", "en": "order one: integrated outright"},
  8: {"zh": "降階法", "en": "reduction of order"},
  9: {"zh": "為什麼低一階就夠了", "en": "why one order less suffices"},
  10: {"zh": "二階：找到一個解就全解完了", "en": "order two: one solution finishes it"},
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

 def _plot(self, f, col, ta, tb, oy, sy, sw=2.6, n=150, xl=XL, xr=XR):
  """A curve over t in [ta, tb], with ta pinned to the figure's left edge.

  The t range is a parameter and the mapping is written out here on purpose:
  E75 had one helper where `ox` meant "t = 0" and another where it meant "the
  left edge", and two beats ran off the panel where the data went negative.
  Here nothing has to be assumed about where t = 0 sits."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 def _hline(self, y, col=DIM, sw=1.3, xl=XL, xr=XR):
  return Line([xl, y, 0], [xr, y, 0], color=col, stroke_width=sw)

 # ── beat 0: the equation, and the tuple that flattens it ─────────
 def _setup(self):
  oy = 0.30
  g = VGroup(self._box(-5.50, oy, "f", ACCENT_B, w=0.72, h=0.58, size=FS_TAG + 3))
  ents = (("f", ACCENT_B), ("f ′", ACCENT_C), ("⋮", DIM), ("f ⁽ ⁿ ⁻ ¹ ⁾", ACCENT_A))
  cx, dy = -4.20, 0.34
  ytop = oy + (len(ents) - 1) * dy / 2
  for k, (lab, col) in enumerate(ents):
   g.add(self._sym(ytop - k * dy, lab, col, FS_TAG - 4, x=cx, w=0.90))
  g.add(self._brackets(cx - 0.50, cx + 0.50,
                       ytop - (len(ents) - 1) * dy - 0.18, ytop + 0.18))
  g.add(self._box(-2.72, oy, "W ⁿ", DIM, w=0.86, h=0.52, size=FS_TAG))
  g.add(self._arr([-5.19, oy, 0], [-4.80, oy, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.54, "ψ", ACCENT_A, FS_TAG + 1, x=-5.00, w=0.40))
  g.add(self._arr([-3.64, oy, 0], [-3.20, oy, 0], DIM, sw=3, tl=0.12))
  g.add(self._sym(oy + 0.22, "∈", DIM, FS_TAG - 2, x=-3.42, w=0.40))
  g.add(self._table((("d ⁿ α / d t ⁿ   =   G ( t , α , … , d ⁿ ⁻ ¹ α / d t ⁿ ⁻ ¹ )", ACCENT_A),
                     ("d α / d t   =   F ( t , α )   =   T ₜ ( α )", ACCENT_B),
                     ("ψ f   =   ⟨ f , f ′ , … , f ⁽ ⁿ ⁻ ¹ ⁾ ⟩", ACCENT_C),
                     ("n   =   1       ⇒       § 1", DIM)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("第二列的 T ₜ 對第二個變數是線性的",
                  "the operator in the second row is linear in its second variable"))
  return g.add(self._foot("第 4 節要解的是 α 的 n 階導數等於 G，而 G 對 α 與它的各階導數是線性的。老辦法照樣管用",
                          "section 4 solves the equation whose nth derivative side is linear in the function and its lower derivatives, and the old device still works",
                          ACCENT_A,
                          "把 f 和它的前 n 減一階導數排成一個 n 元組，n 階方程就變成第 3 節那種一階系統，只是空間換成 W 的 n 次冪",
                          "lining f up with its first n minus one derivatives turns the nth-order equation into a first-order system, on the n-fold product instead"))

 # ── beat 1: psi is an isomorphism of solution spaces ─────────────
 def _psi(self):
  oy = 0.30
  g = VGroup()
  for x0, lab, col in ((-5.10, "N", ACCENT_C), (-3.00, "𝒩", ACCENT_B)):
   g.add(self._box(x0, oy, lab, col, w=0.80, h=0.60, size=FS_TAG + 3))
  g.add(self._arr([-4.58, oy + 0.14, 0], [-3.48, oy + 0.14, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._arr([-3.52, oy - 0.14, 0], [-4.62, oy - 0.14, 0], DIM, sw=3, tl=0.14))
  g.add(self._sym(oy + 0.52, "ψ", ACCENT_A, FS_TAG + 1, x=-4.05, w=0.40),
        self._sym(oy - 0.52, "π ¹", DIM, FS_TAG - 2, x=-4.05, w=0.60))
  g.add(self._sym(oy - 0.92, "N  ⊂  𝒞 ⁿ ( I , W )            𝒩  ⊂  𝒞 ¹ ( I , W ⁿ )",
                  DIM, FS_TAG - 3, x=-4.05, w=3.40))
  g.add(self._table((("f  ∈  N        ⟺        ψ f  ∈  𝒩", ACCENT_A),
                     ("ψ  :  N    ≅    𝒩", ACCENT_C),
                     ("π ¹  ∘  ψ   =   id", ACCENT_B),
                     ("§ 1  ,  1.5", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("上下兩個箭頭互為反元素，這就是同構",
                  "the two arrows invert one another, which is what the isomorphism says"))
  return g.add(self._foot("第 1 節定理 1.5 的證明其實已經說完了：f 是 n 階方程的解，若且唯若那個 n 元組是一階系統的解",
                          "the proof of Theorem 1.5 already said it: f solves the nth-order equation exactly when that n-tuple solves the first-order system",
                          ACCENT_A,
                          "而排導數這個動作本身是線性的，回頭只要取第一個座標，所以 ψ 是兩個解空間之間的同構，不只是雙射",
                          "lining up derivatives is itself linear and the way back is taking the first coordinate, so psi is an isomorphism of the two solution spaces"))

 # ── beat 2: n initial values fix the solution ────────────────────
 def _initial(self):
  ta, tb, oy, sy = 0.55, 1.75, -0.62, 0.36
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  cols = (ACCENT_A, ACCENT_B, ACCENT_C)
  for (s, A, B), col in zip(INIT, cols):
   g.add(self._plot(sol(A, B), col, ta, tb, oy, sy, sw=2.8))
  x1 = self._xof(1.0, ta, tb)
  g.add(Dot([x1, oy + sy * 1.0, 0], radius=0.058, color=INK))
  g.add(self._sym(oy + sy * 1.0 + 0.26, "t ₀", DIM, FS_TAG - 3, x=x1, w=0.44))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "f ′ ( t ₀ )  =  2", 1.60),
                                 (ACCENT_B, "f ′ ( t ₀ )  =  − 1", 1.70),
                                 (ACCENT_C, "f ′ ( t ₀ )  =  0.5", 1.70)), y0=1.14, dy=0.25))
  g.add(self._table((("π ₜ ∘ ψ  :  f  ↦  ⟨ f ( t ) , … , f ⁽ ⁿ ⁻ ¹ ⁾ ( t ) ⟩", ACCENT_A),
                     ("N     ≅     W ⁿ", ACCENT_C),
                     ("f ( t ₀ )   =   1     ,     n   =   2", DIM),)
                    + tuple((f"      f ′ ( t ₀ )  =  {s:+.1f}        A  =  {A:+.4f}   B  =  {B:+.4f}",
                             ACCENT_B) for s, A, B in INIT),
                    y0=0.88, dy=0.28, size=FS_TAG - 4))
  g.add(self._cap("三條在 t ₀ 同值，只有斜率不同",
                  "the three agree at that instant and differ only in slope"))
  return g.add(self._foot("第 3 節說一階系統的解由它在某一個時刻的值唯一決定。兩件事合起來，取值映射是解空間到 W 的 n 次冪的同構",
                          "section 3 fixed a solution of the system by its value at one instant, and together the two make evaluation an isomorphism onto the n-fold product",
                          ACCENT_A,
                          "也就是「n 個初始值決定唯一一個解」。圖上三條都是本集那個例子的解，在 t ₀ 的值都是 1，是斜率把它們分開的",
                          "that is: n initial values, exactly one solution; the three curves all solve this episode's example and share their value, so only the slope separates them"))

 # ── beat 3: W real, and the operator L ──────────────────────────
 def _operator(self):
  ta, tb, oy, sy = 0.75, 2.4, 0.42, 0.30
  g = VGroup(self._hline(oy), self._plot(a0, ACCENT_C, ta, tb, oy, sy, sw=2.8))
  g.add(self._hline(oy + sy * 1.0, ACCENT_B, sw=2.8))
  g.add(self._legend(XL + 0.06, ((ACCENT_B, "a ₂", 0.56), (ACCENT_C, "a ₀", 0.56)), y0=1.14))
  # one tick per line, each at its own height: the first version put the zero
  # at the height of the a2 = 1 line and so labelled that line zero
  g.add(self._sym(oy - 0.22, "0", DIM, FS_TAG - 3, x=XR + 0.30, w=0.34),
        self._sym(oy + sy, "1", ACCENT_B, FS_TAG - 3, x=XR + 0.30, w=0.34))
  g.add(self._table((("G ( t , x ₁ , … , x ₙ )   =   Σ ₁ ⁿ  k ᵢ ( t ) x ᵢ", ACCENT_A),
                     ("( L f ) ( t )  =  aₙ ( t ) f ⁽ ⁿ ⁾ ( t )  +  ⋯  +  a ₀ ( t ) f ( t )",
                      ACCENT_A),
                     ("N   =   L ⁻ ¹ ( 0 )", ACCENT_C),
                     ("        t            a ₂        a ₁         a ₀", DIM),)
                    + tuple((f"      {t:.1f}        {c2:.2f}     {c1:.2f}     {c0:+.4f}", ACCENT_B)
                            for t, c2, c1, c0 in COEF),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("a ₁ 恆為零，就是那條軸，所以沒有畫",
                  "the middle coefficient is zero, which is the axis itself, so it is not drawn"))
  return g.add(self._foot("取 W 是實數線。G 在每個 t 是線性函數，係數是 n 個連續函數，於是解空間正好是一個線性變換的零化空間",
                          "take W to be the real line: G is linear at each t with n continuous coefficients, so the solution space is exactly one transformation's null space",
                          ACCENT_A,
                          "把指標挪一挪對齊導數的階數，L 就寫成係數乘各階導數的和。圖上是本集例子的係數，a ₀ 在原點附近不連續，所以區間不能含零",
                          "shifting indices to match the orders writes L as coefficients times derivatives; the example's lowest coefficient is discontinuous at the origin, so the interval must avoid it"))

 # ── beat 4: regular and singular ────────────────────────────────
 def _singular(self):
  ta, tb, oy, sy = 0.22, 2.4, 0.02, 0.42
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14),
             Line([XL, oy - 0.68, 0], [XL, oy + 0.52, 0], color=DIM, stroke_width=1.3))
  g.add(self._plot(ylog, ACCENT_C, ta, tb, oy, sy, sw=2.8))
  g.add(self._hline(oy + sy * 1.0, ACCENT_B, sw=2.8))
  g.add(self._legend(XL + 1.40, ((ACCENT_B, "y  =  1", 0.96),
                                 (ACCENT_C, "y  =  log t", 1.50)), y0=1.14))
  g.add(self._table((("t  y ″   +   y ′   =   0            a ₂ ( t )  =  t", ACCENT_A),
                     ("( t  y ′ ) ′   =   0         ⇒         y ′   =   k / t", ACCENT_C),
                     ("        t              y              y ′", DIM),)
                    + tuple((f"      {t:.2f}      {y:+.4f}      {dy:8.2f}", ACCENT_B)
                            for t, y, dy in SING)
                    + ((f"dim N   =   {DIM_AWAY}      →      {DIM_ACROSS}", ACCENT_A),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("右欄一路衝上去，那就是崩掉的地方",
                  "the last column runs away, and that is where the dimension is lost"))
  return g.add(self._foot("最高階的係數處處不為零就可以除掉，這叫正則；某個 t 讓它變成零的奇異情形要另外的理論，這本書不碰",
                          "if the top coefficient never vanishes we divide it out, the regular case; the singular case needs further study and the book leaves it alone",
                          ACCENT_A,
                          "左邊這個奇異例子的第一積分是 t y ′ 等於常數，所以除了常數解以外 y ′ 在原點附近爆掉：不含原點時解空間是二維，一含進來就掉成一維",
                          "this singular example integrates to t times the derivative being constant, so apart from the constants the derivative blows up at the origin: two dimensions away from it, one across it"))

 # ── beat 5: theorem 4.1 ─────────────────────────────────────────
 def _thm41(self):
  oy = 0.34
  g = VGroup()
  g.add(self._box(-5.05, oy, "𝒞 ⁿ ( I )", ACCENT_A, w=1.50, h=0.56, size=FS_TAG))
  g.add(self._box(-2.95, oy, "𝒞 ⁰ ( I )", ACCENT_B, w=1.50, h=0.56, size=FS_TAG))
  g.add(self._arr([-4.26, oy + 0.14, 0], [-3.72, oy + 0.14, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._arr([-3.72, oy - 0.14, 0], [-4.26, oy - 0.14, 0], ACCENT_C, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.46, "L", ACCENT_A, FS_TAG, x=-3.99, w=0.40),
        self._sym(oy - 0.46, "R", ACCENT_C, FS_TAG, x=-3.99, w=0.40))
  for x0, lab, col in ((-5.66, "N", ACCENT_C), (-4.44, "M ₜ ₀", ACCENT_B)):
   g.add(self._box(x0, oy - 1.02, lab, col, w=0.96, h=0.48, size=FS_TAG - 1))
  g.add(self._sym(oy - 1.02, "⊕", DIM, FS_TAG, x=-5.05, w=0.40))
  g.add(self._arr([-5.05, oy - 0.34, 0], [-5.05, oy - 0.74, 0], DIM, sw=3, tl=0.12))
  g.add(self._table((("L [ 𝒞 ⁿ ( I ) ]   =   𝒞 ⁰ ( I )", ACCENT_A),
                     ("dim N   =   n            N   =   L ⁻ ¹ ( 0 )", ACCENT_C),
                     ("φ ₜ ₀ ∘ ψ   :   N    ≅    ℝ ⁿ", ACCENT_A),
                     ("M ₜ ₀  =  { f  :  f ( t ₀ ) = ⋯ = f ⁽ ⁿ ⁻ ¹ ⁾ ( t ₀ ) = 0 }", ACCENT_B),
                     ("L  ∘  R   =   id", ACCENT_A)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("下面那一列是把左上那個空間拆成兩半",
                  "the row below splits the space on the left into two halves"))
  return g.add(self._foot("定理 4.1 把一般理論在這裡的樣子收攏起來：L 是滿射，零化空間就是解空間而維數是 n，在任一時刻取值都是它到 n 維空間的同構",
                          "theorem 4.1 gathers the general theory here: the operator is onto, its null space is the solution space of dimension n, and evaluation anywhere is an isomorphism onto n-space",
                          ACCENT_A,
                          "而在那個時刻連同前 n 減一階導數全為零的函數構成一個補，於是決定了 L 的一個線性右反元素 R",
                          "and the functions vanishing there to order n minus one form a complement, which determines a linear right inverse of the operator"))

 # ── beat 6: the two-part practical problem ──────────────────────
 def _program(self):
  ta, tb, oy, sy = 0.6, 1.9, -0.50, 0.95
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  for A, B in AFFINE[1:]:
   g.add(self._plot(lambda t, A=A, B=B: rinv(t) + A * t * t + B / t, DIM,
                    ta, tb, oy, sy, sw=2.0))
  g.add(self._plot(rinv, ACCENT_A, ta, tb, oy, sy, sw=3.2))
  x1 = self._xof(1.0, ta, tb)
  g.add(Dot([x1, oy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "R g", 0.80), (DIM, "R g  +  N", 1.50)), y0=1.14))
  g.add(self._table((("L ( f )   =   g", ACCENT_A),
                     ("f     ∈     v   +   N            L ( v )  =  g", ACCENT_A),
                     ("        t          v ( t )        ( R g ) ( t )", DIM),)
                    + tuple((f"      {t:.1f}      {a:+.5f}      {b:+.5f}", ACCENT_B)
                            for t, a, b in RINV)
                    + (("( R g ) ( t ₀ )  =  ( R g ) ′ ( t ₀ )  =  0", ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("灰線與橘線只差一個齊次解",
                  "the grey curves differ from the orange one by a homogeneous solution"))
  return g.add(self._foot("實務上分成兩件事：一是找出解空間的一組基底，也就是解齊次方程；二是找出一個右反元素，也就是替每個 g 挑一個解",
                          "in practice the problem splits in two: find a basis for the solution space, the homogeneous problem, and find a right inverse, which picks one solution per right-hand side",
                          ACCENT_A,
                          "有了一個特解，全部的解就是解空間平移過去的仿射子空間。橘線是定理 4.1 那個補挑出來的那一個：它在 t ₀ 的值與斜率都是零",
                          "with one particular solution all of them form an affine subspace; the orange curve is the one that complement picks, vanishing in value and slope at the chosen instant"))

 # ── beat 7: order one, integrated ───────────────────────────────
 def _firstorder(self):
  ta, tb, oy, sy = 0.5, 2.5, -0.62, 0.50
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(lambda t: 1.0 / t, ACCENT_A, ta, tb, oy, sy, sw=3.0))
  g.add(self._plot(lambda t: math.exp(-t * t), ACCENT_C, ta, tb, oy, sy, sw=3.0))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "a  =  1 / t", 1.30),
                                 (ACCENT_C, "a  =  2 t", 1.10)), y0=1.14))
  rows = [("y ′  +  a ( t )  y   =   0        y  =  exp ( − ∫ a )", ACCENT_A),
          ("        t            y            y ′ + a y", DIM)]
  for name, rs in FIRST:
   col = ACCENT_A if name == "1" else ACCENT_C
   rows += [(f"      {t:.1f}      {y:+.5f}      {r:+.1e}", col) for t, y, r in rs[:2]]
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("右欄是代回去的殘差，到機器精度",
                  "the last column is the residual after substituting, at machine precision"))
  return g.add(self._foot("很遺憾找基底沒有一般的方法，只能部分成功。一階的情形可以直接解：y 一撇除以 y 就是 log y 的導數",
                          "unhappily there is no general method for a basis, only partial success; order one goes through directly, since the derivative over the function is the derivative of its logarithm",
                          ACCENT_A,
                          "所以 y 等於 e 的「負 a 的積分」次方。上面兩條就是兩個 a 各自的解，右表把它們代回原方程，殘差是零",
                          "so the solution is the exponential of minus the integral of the coefficient; the two curves are the solutions for two coefficients, with zero residual in the table"))

 # ── beat 8: reduction of order ──────────────────────────────────
 def _reduce(self):
  oy = 0.26
  g = VGroup()
  g.add(self._box(-5.35, oy, "L ( c u )", ACCENT_A, w=1.30, h=0.56, size=FS_TAG + 1))
  g.add(self._box(-3.30, oy + 0.44, "c  L ( u )   =   0", WARN, w=2.10, h=0.48, size=FS_TAG))
  g.add(self._box(-3.30, oy - 0.44, "S ( c ′ )", ACCENT_C, w=2.10, h=0.48, size=FS_TAG))
  g.add(self._arr([-4.66, oy + 0.10, 0], [-4.42, oy + 0.34, 0], DIM, sw=3, tl=0.12))
  g.add(self._arr([-4.66, oy - 0.10, 0], [-4.42, oy - 0.34, 0], ACCENT_C, sw=3, tl=0.12))
  g.add(self._sym(oy + 0.88, "u   ∈   N", DIM, FS_TAG - 3, x=-3.30, w=1.30))
  g.add(self._sym(oy - 0.92, "n   −   1", ACCENT_C, FS_TAG - 2, x=-3.30, w=1.10))
  g.add(self._table((("v   =   c  u        v ⁽ ʲ ⁾  =  Σ ᵢ  C ( j , i )  c ⁽ ⁱ ⁾ u ⁽ ʲ ⁻ ⁱ ⁾",
                      ACCENT_A),
                     ("L ( v )   =   c L ( u )   +   S ( c ′ )   =   S ( c ′ )", ACCENT_A),
                     ("        t          L ( c u )         S ( c ′ )", DIM),)
                    + tuple((f"      {t:.1f}      {a:+.5f}      {b:+.5f}", ACCENT_B)
                            for t, a, b in RED)
                    + (("c ( t )   =   sin t", ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("中間兩欄逐列相同，而這個 c 不是答案",
                  "the two middle columns agree row by row, and this c is not the answer"))
  return g.add(self._foot("假設已經知道一個解 u，就找 c 乘 u 這種形式的第二個解。用 Leibniz 公式展開代進 L，不帶 c 的導數的那些項合起來是 c 乘 L ( u )",
                          "suppose one solution is known and look for a second of the form c times it: expanding by Leibniz, the terms with no derivative of c add up to c times the operator applied to it",
                          ACCENT_A,
                          "那一塊正好是零，剩下的可以寫成一個 n 減一階的算子作用在 c 一撇上。右表用一個隨便取的 c 驗這件事，不是用答案驗",
                          "that block is zero, and the rest is an operator of order n minus one applied to the derivative of c; the table checks this with an arbitrary c, not with the answer"))

 # ── beat 9: why the reduced equation suffices, and the caveat ───
 def _why(self):
  oy = 0.40
  g = VGroup()
  g.add(self._box(-5.10, oy + 0.50, f"L    :    {ORD_L}", ACCENT_A, w=1.34, h=0.52, size=FS_TAG))
  g.add(self._box(-5.10, oy - 0.60, f"S    :    {ORD_S}", ACCENT_C, w=1.34, h=0.52, size=FS_TAG))
  # two lanes, not one: with both arrows on the same line the cross sat on the
  # downward one too, and the picture said neither direction works
  g.add(self._arr([-5.52, oy + 0.24, 0], [-5.52, oy - 0.34, 0], ACCENT_C, sw=3, tl=0.13))
  g.add(self._arr([-4.68, oy - 0.34, 0], [-4.68, oy + 0.24, 0], DIM, sw=3, tl=0.13))
  cx, cy = -4.68, oy - 0.05
  g.add(Line([cx - 0.17, cy - 0.17, 0], [cx + 0.17, cy + 0.17, 0], color=WARN, stroke_width=4.0),
        Line([cx - 0.17, cy + 0.17, 0], [cx + 0.17, cy - 0.17, 0], color=WARN, stroke_width=4.0))
  g.add(self._sym(oy - 1.06, "N ( S )   ⊂   N ( L )   ?", WARN, FS_TAG - 2, x=-4.40, w=2.60))
  g.add(self._table((("{ g ᵢ } ₁ ⁿ ⁻ ¹   :   S ( g ᵢ )  =  0", ACCENT_A),
                     ("c ᵢ ( t )   =   ∫ g ᵢ ( s ) d s", ACCENT_C),
                     ("L ( c ᵢ u )   =   S ( c ᵢ ′ )   =   S ( g ᵢ )   =   0", ACCENT_A),
                     ("u , c ₁ u , … , c ₙ ₋ ₁ u        :        ≅        ℝ ⁿ", ACCENT_B),
                     ("S ( t ⁻ ⁴ )  =  0            c   ∝   t ⁻ ³", ACCENT_C)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("紅叉是那個走不回去的方向",
                  "the red cross marks the direction that does not go back"))
  return g.add(self._foot("解 S f 等於零這個低一階的方程就夠了：取它零化空間的一組基底各自積分，L 作用在係數乘 u 上就等於 S 作用在基底上，是零",
                          "solving that lower-order equation suffices: take a basis of its null space and integrate each one, and the operator applied to coefficient times solution equals the operator on the basis, zero",
                          ACCENT_A,
                          "而且這些新解與 u 一起是獨立的。但這個手法不能一層層疊上去——它是從上面削，不是從下面長，要疊得先有 N ( S ) 落在 N ( L ) 裡面的一階算子",
                          "and the new solutions are independent of the old; but this does not stack up, working off the top and not the bottom, since building up would need a first-order operator inside this one"))

 # ── beat 10: the second-order example, finished ─────────────────
 def _example(self):
  ta, tb, oy, sy = 0.55, 1.50, -0.72, 0.50
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(u, ACCENT_B, ta, tb, oy, sy, sw=3.0))
  g.add(self._plot(v, ACCENT_C, ta, tb, oy, sy, sw=3.0))
  x1, y1 = self._xof(1.0, ta, tb), oy + sy * 1.0
  sx = (XR - XL) / (tb - ta)
  g.add(Dot([x1, y1, 0], radius=0.060, color=INK))
  for slope, col in ((2.0, ACCENT_B), (-1.0, ACCENT_C)):
   dx = 1.30
   g.add(self._arr([x1, y1, 0], [x1 + dx, y1 + dx * sy * slope / sx, 0], col, sw=4, tl=0.16))
  g.add(self._legend(XL + 0.06, ((ACCENT_B, "u  =  t ²", 1.00),
                                 (ACCENT_C, "v  =  1 / t", 1.30)), y0=1.14))
  g.add(self._table((("y ″   −   2 y / t ²   =   0          N  =  ⟨ t ²  ,  1 / t ⟩", ACCENT_A),
                     ("        t          u v ′ − u ′ v", DIM),)
                    + tuple((f"      {t:.1f}          {w:+.4f}", ACCENT_B) for t, w in WR)
                    + ((f"u ( t ₀ )  =  v ( t ₀ )  =  {PAIRS[0][1]:.0f}", ACCENT_C),
                       (f"u ′ ( t ₀ )  =  {PAIRS[0][2]:+.0f}        v ′ ( t ₀ )  =  {PAIRS[1][2]:+.0f}",
                        ACCENT_A)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("值相同，兩個箭頭卻朝不同的方向",
                  "the values agree, yet the two arrows point different ways"))
  return g.add(self._foot("二階只要找到一個解就全部解完，因為剩下的是一階方程。書上的例子一眼看出 t ² 是解，代進去之後第二個解是 t 的倒數",
                          "order two is finished by one solution, since what remains is order one: the example's first solution is visible by inspection and substituting gives one over t as the second",
                          ACCENT_A,
                          "兩條在 t ₀ 的值相同也不礙事：定理 4.1 的同構配的是「值與導數」這一對，右表那個行列式一直是 − 3，從來不是零",
                          "their sharing a value there does not matter: Theorem 4.1's isomorphism pairs value with derivative, and that determinant stays at minus three, never zero"))

 def stage(self):
  a, b, c = self._setup(), self._psi(), self._initial()
  d, e, f_ = self._operator(), self._singular(), self._thm41()
  h, i, j = self._program(), self._firstorder(), self._reduce()
  k, l = self._why(), self._example()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE79ZH, AdvCalcE79EN = make(AdvCalcE79Base, "79", prefix="AdvCalcE")
