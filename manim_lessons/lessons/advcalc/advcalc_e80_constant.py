"""advcalc E80 -- chapter 6, section 4 (book pp. 284-287): constant
coefficients, Theorems 4.2 and 4.3, and the starred characterisation.

E79 ended with a method that needs one solution before it can start.  Here the
coefficients are constants, and there is a complete explicit answer, because L
is now a polynomial in the derivative operator: solving the differential
equation becomes factoring p.  The book's route is the detour through section 3
-- psi carries the solution space over, commutes with D, and the two lemmas turn
D into T, so p(D) = 0 on N forces p(T) = 0 on W.  Theorem 3.4 then hands back
t^j e^{bt} times constant vectors, and the first coordinates are the basis.

Real coefficients with complex roots need the complexification of the chapter 4
exercises; the one extra fact is that the real null space is the intersection of
the complex one with the real space, so real solutions are real parts.  That
turns the conjugate pair into e^{bt} cos wt and e^{bt} sin wt, which is Theorem
4.3.  The starred passage then shows the collection of all such solutions is an
algebra, and is exactly the set of continuous functions whose translates span a
finite-dimensional space.

The numbers are computed here, and exactly: a function P(t) e^{lambda t} is
carried as its polynomial and its exponent, so differentiating it is
(P' + lambda P) e^{lambda t} with no finite differences anywhere, and applying
p(D) is arithmetic.  That is what makes the sign check in beat 6 trustworthy --
the theorem's display prints the quadratic's middle term with the opposite sign
to the derivation two paragraphs above it, and the printed version leaves
residuals of order ten instead of 1e-15.
"""
import cmath
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
GRID = (0.0, 0.3, 0.9, 1.7, 2.6, 4.0)       # where "is it zero" is tested


# ── exact arithmetic on  P(t) exp(lambda t)  ──────────────────────────
# A function is a list of (P, lambda) terms with P a list of coefficients,
# lowest power first. Differentiating is (P' + lambda P) exp(lambda t), so no
# finite difference enters anywhere and a residual of 1e-15 means zero.
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


def det(M):
 n = len(M)
 M = [[complex(x) for x in row] for row in M]
 d = 1.0 + 0j
 for i in range(n):
  p = max(range(i, n), key=lambda r: abs(M[r][i]))
  if abs(M[p][i]) < 1e-14:
   return 0.0
  if p != i:
   M[i], M[p] = M[p], M[i]
   d = -d
  d *= M[i][i]
  for r in range(i + 1, n):
   f = M[r][i] / M[i][i]
   for cc in range(i, n):
    M[r][cc] -= f * M[i][cc]
 return d


def nth(terms, k):
 for _ in range(k):
  terms = dall(terms)
 return terms


def wronskian(basis, t=0.0):
 return det([[val(nth(f, k), t) for f in basis] for k in range(len(basis))]).real


def rf(terms):
 """The real-valued function a term list stands for."""
 return lambda t: val(terms, t).real


# ── beats 0 and 2: Theorem 4.2, one repeated root ─────────────────────
B42, N42 = -0.6, 3
P42 = ppow([-B42, 1.0], N42)
BAS42 = [texp(i, B42) for i in range(N42)]
RES42 = [(i, size(applyp(P42, texp(i, B42)))) for i in range(N42 + 1)]
assert all(r < 1e-12 for i, r in RES42[:N42]), "the n functions are in the null space"
assert RES42[N42][1] > 1.0, "and the next power of t is not: there are exactly n of them"
WR42 = wronskian(BAS42)
assert abs(WR42) > 1e-9, "so they are independent, hence a basis"

# ── beat 3: a relatively prime factorization ──────────────────────────
B1, B2 = -0.5, 0.35
P43 = pmul(ppow([-B1, 1.0], 2), [-B2, 1.0])
BAS43 = [texp(0, B1), texp(1, B1), texp(0, B2)]
RES43 = [size(applyp(P43, f)) for f in BAS43]
assert all(r < 1e-12 for r in RES43), "each factor's basis lies in the whole null space"
WR43 = wronskian(BAS43)
assert abs(WR43) > 1e-9, "and the union of the two bases is independent"

# ── beats 5 and 6: Theorem 4.3, and the sign the book prints ──────────
BQ, WQ, MQ = -0.35, 1.8, 2
CQ = BQ * BQ + WQ * WQ
LAMQ = complex(BQ, WQ)
QMINUS = ppow([CQ, -2.0 * BQ, 1.0], MQ)     # (x^2 - 2bx + c)^m, as derived
QPLUS = ppow([CQ, +2.0 * BQ, 1.0], MQ)      # (x^2 + 2bx + c)^m, as displayed
assert abs(LAMQ ** 2 - 2.0 * BQ * LAMQ + CQ) < 1e-12, "lambda is a root of the first one"
assert abs(LAMQ ** 2 + 2.0 * BQ * LAMQ + CQ) > 1.0, "and not of the second"
BAS4R, LAB4R = [], []
for _i in range(MQ):
 BAS4R += [tcos(_i, BQ, WQ), tsin(_i, BQ, WQ)]
 LAB4R += [f"t {'⁰¹²³'[_i]} cos", f"t {'⁰¹²³'[_i]} sin"]
SIGN = [(size(applyp(QMINUS, f)), size(applyp(QPLUS, f))) for f in BAS4R]
assert len(BAS4R) == 2 * MQ, "two m functions, which is the dimension"
assert all(a < 1e-12 for a, _b in SIGN), "the derivation's sign annihilates all of them"
assert all(b > 1.0 for _a, b in SIGN), \
    "the printed sign annihilates none: the theorem's display contradicts its own proof"
WR4R = wronskian(BAS4R)
assert abs(WR4R) > 1e-9, "and the two m of them are independent"

# ── beat 7: D^4 - 1 ───────────────────────────────────────────────────
P4 = [-1.0, 0.0, 0.0, 0.0, 1.0]
ROOTS4 = [complex(1.0, 0.0), complex(-1.0, 0.0), complex(0.0, 1.0), complex(0.0, -1.0)]
assert all(abs(r ** 4 - 1.0) < 1e-15 for r in ROOTS4)
BAS4 = [texp(0, 1.0), texp(0, -1.0), tcos(0, 0.0, 1.0), tsin(0, 0.0, 1.0)]
RES4 = [size(applyp(P4, f)) for f in BAS4]
assert all(r < 1e-12 for r in RES4) and abs(wronskian(BAS4)) > 1e-9
WR4 = wronskian(BAS4)

# ── beat 8: D^3 - 1 ───────────────────────────────────────────────────
P3 = [-1.0, 0.0, 0.0, 1.0]
W3 = math.sqrt(3.0) / 2.0
LAM3 = complex(-0.5, W3)
assert abs(LAM3 ** 3 - 1.0) < 1e-14, "the complex cube roots of one"
BAS3 = [texp(0, 1.0), tcos(0, -0.5, W3), tsin(0, -0.5, W3)]
RES3 = [size(applyp(P3, f)) for f in BAS3]
assert all(r < 1e-12 for r in RES3)
WR3 = wronskian(BAS3)
assert abs(WR3) > 1e-9

# ── beat 9: the algebra, on one product ───────────────────────────────
def fprod(t):
 return math.sin(t) * math.cos(2.0 * t)


def fpieces(t):
 return 0.5 * math.sin(3.0 * t), -0.5 * math.sin(t)


IDENT = max(abs(fprod(t) - sum(fpieces(t))) for t in GRID)
assert IDENT < 1e-14, "2 sin x cos y = sin(x+y) + sin(x-y), which is why products stay inside"
TERMS9 = []
for _w, _c in ((3.0, 0.5), (1.0, -0.5)):
 TERMS9 += [([_c * x for x in P], lam) for P, lam in tsin(0, 0.0, _w)]
PANN = pmul([1.0, 0.0, 1.0], [9.0, 0.0, 1.0])
RES9 = size(applyp(PANN, TERMS9))
RES9ONE = size(applyp([1.0, 0.0, 1.0], TERMS9))
assert RES9 < 1e-12, "the composite of the two operators kills the product"
assert RES9ONE > 1.0, "while either one alone does not: both frequencies have to be caught"
assert max(abs(val(TERMS9, t).real - fprod(t)) for t in GRID) < 1e-14

# ── beat 10: translates ───────────────────────────────────────────────
TT = np.linspace(-3.0, 3.0, 241)
XS = np.linspace(-2.0, 2.0, 8)
SV = {}
for _name, _f in (("cos", np.cos), ("gauss", lambda z: np.exp(-z * z))):
 _M = np.array([_f(TT - x) for x in XS])
 _s = np.linalg.svd(_M, compute_uv=False)
 SV[_name] = (_s, int((_s > 1e-9 * _s[0]).sum()))
assert SV["cos"][1] == 2, "every translate of the cosine lies in a two-dimensional space"
assert SV["gauss"][1] == len(XS), \
    "while eight translates of a Gaussian are eight independent directions"
XSHOW = (-2.0, -1.0, 0.0, 1.0, 2.0)


class AdvCalcE80Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 80

 MODE_LABEL = {
  0: {"zh": "常係數：L 是 D 的多項式", "en": "constant coefficients: a polynomial in D"},
  1: {"zh": "繞道第 3 節", "en": "the detour through section 3"},
  2: {"zh": "定理 4.2 的前半", "en": "theorem 4.2, first half"},
  3: {"zh": "互質分解：基底聯集起來", "en": "relatively prime factors: unite the bases"},
  4: {"zh": "複根：複化", "en": "complex roots: complexification"},
  5: {"zh": "共軛的一對", "en": "the conjugate pair"},
  6: {"zh": "定理 4.3：取實部", "en": "theorem 4.3: take real parts"},
  7: {"zh": "例一", "en": "first example"},
  8: {"zh": "例二", "en": "second example"},
  9: {"zh": "加星號：這些解構成一個代數", "en": "starred: the solutions form an algebra"},
  10: {"zh": "平移張成有限維，第 4 節結束",
       "en": "translates span finitely, and the end of section 4"},
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

  Same helper as E79, and for the same reason: the t range is a parameter, so
  nothing has to be assumed about where t = 0 lands on screen."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 # ── beat 0: L is a polynomial in D ──────────────────────────────
 def _pd(self):
  oy = 0.42
  g = VGroup()
  xs = (-5.55, -4.45, -3.35, -2.25)
  # not "f ‴": that glyph is missing from the font and renders as a double
  # prime, which drew the last two boxes as the same function
  for k, (x0, lab) in enumerate(zip(xs, ("f", "f ′", "f ″", "f ⁽ ³ ⁾"))):
   g.add(self._box(x0, oy, lab, ACCENT_B if k else ACCENT_C, w=0.74, h=0.52, size=FS_TAG))
   g.add(self._sym(oy - 0.52, f"a {'₀₁₂₃'[k]}", ACCENT_A, FS_TAG - 2, x=x0, w=0.60))
  for a, b in zip(xs, xs[1:]):
   g.add(self._arr([a + 0.40, oy, 0], [b - 0.40, oy, 0], DIM, sw=3, tl=0.12))
   g.add(self._sym(oy + 0.42, "D", DIM, FS_TAG - 3, x=(a + b) / 2, w=0.44))
  g.add(self._sym(oy - 1.06, "Σ   a ᵢ  f ⁽ ⁱ ⁾   =   p ( D ) f", ACCENT_A,
                  FS_TAG - 1, x=-4.05, w=3.20))
  g.add(self._table((("L f  =  aₙ f ⁽ ⁿ ⁾  +  ⋯  +  a ₀ f            aₙ  =  1", ACCENT_A),
                     ("D ʲ f  =  f ⁽ ʲ ⁾           L  =  p ( D )", ACCENT_B),
                     ("p ( x )   =   ( x  −  b ) ⁿ            n  =  3", ACCENT_C),
                     (f"b   =   {B42:+.1f}", DIM),
                     ("      a ₀        a ₁        a ₂        a ₃", DIM),
                     ("    " + "    ".join(f"{c:.3f}" for c in P42), ACCENT_B)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("最後一列是那個多項式真正的係數",
                  "the last row holds that polynomial's actual coefficients"))
  return g.add(self._foot("上一集的降階法要先知道一個解才動得了。係數全是常數時有完整的顯式答案，這是整節最有用的一段",
                          "last episode's reduction needed one solution before it could start; with constant coefficients there is a complete explicit answer, the most useful stretch of the section",
                          ACCENT_A,
                          "關鍵是此時 L 就是導數算子的一個多項式：把 D 一次一次作用上去再乘上係數加起來。於是解微分方程變成把 p 分解因式",
                          "the point is that the operator is now a polynomial in the derivative: apply D repeatedly, weight, and add, so solving the equation becomes factoring p"))

 # ── beat 1: the detour through section 3 ────────────────────────
 def _route(self):
  oy = 0.34
  g = VGroup()
  for x0, yy, lab, col in ((-5.20, oy + 0.40, "N", ACCENT_C), (-2.70, oy + 0.40, "𝒩", ACCENT_B),
                           (-2.70, oy - 0.62, "ℝ ⁿ", ACCENT_A)):
   g.add(self._box(x0, yy, lab, col, w=0.84, h=0.54, size=FS_TAG + 2))
  g.add(self._arr([-4.74, oy + 0.40, 0], [-3.16, oy + 0.40, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._arr([-2.70, oy + 0.09, 0], [-2.70, oy - 0.33, 0], ACCENT_A, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.80, "ψ", ACCENT_A, FS_TAG + 1, x=-3.95, w=0.40),
        self._sym(oy - 0.12, "φ ₜ", ACCENT_A, FS_TAG - 2, x=-2.28, w=0.62))
  g.add(self._sym(oy - 0.22, "D  ↾  N", ACCENT_C, FS_TAG - 2, x=-5.20, w=1.10))
  g.add(self._sym(oy - 0.62, "T  ↾  ℝ ⁿ", ACCENT_A, FS_TAG - 2, x=-3.90, w=1.20))
  g.add(self._table((("ψ ( D f )   =   D ψ ( f )", ACCENT_A),
                     ("D [ 𝒩 ]   ⊂   𝒩                § 3  ,  3.1", ACCENT_C),
                     ("T   =   φ ₜ  ∘  D  ∘  φ ₜ ⁻ ¹        § 3  ,  3.2", ACCENT_B),
                     ("p ( D )  ↾  N  =  0      ⇒      p ( T )  =  0", ACCENT_A),
                     ("§ 3  ,  3.4        ⇒        t ʲ  exp ( t λ ᵢ )  β ᵢ ⱼ", DIM)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("兩個箭頭把問題搬到有限維那邊",
                  "the two arrows move the problem into finite dimensions"))
  return g.add(self._foot("書上說最漂亮的走法是繞到第 3 節去。ψ 把解空間搬到一階系統那邊，而且它與微分交換",
                          "the book calls the detour through section 3 the most elegant route: psi carries the solution space over to the system and commutes with differentiation",
                          ACCENT_A,
                          "引理 3.1 說那個空間在 D 底下不變，引理 3.2 說取值同構把 D 換成 T。所以 p 作用在 D 上是零，就推出 p 作用在 T 上是零，而那是有限維的事",
                          "Lemma 3.1 makes that space invariant under D and Lemma 3.2 turns D into T, so the polynomial annihilating D annihilates T, which is a finite-dimensional statement"))

 # ── beat 2: theorem 4.2 ─────────────────────────────────────────
 def _thm42(self):
  ta, tb, oy, sy = 0.0, 6.0, -0.66, 0.52
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14),
             Line([XL, oy - 0.06, 0], [XL, oy + 0.92, 0], color=DIM, stroke_width=1.3))
  cols = (ACCENT_A, ACCENT_B, ACCENT_C)
  for i, col in zip(range(N42), cols):
   g.add(self._plot(lambda t, i=i: t ** i * math.exp(B42 * t), col, ta, tb, oy, sy, sw=2.8))
  g.add(self._legend(XL + 1.18, ((ACCENT_A, "e ᵇ ᵗ", 0.80), (ACCENT_B, "t e ᵇ ᵗ", 1.10),
                                 (ACCENT_C, "t ² e ᵇ ᵗ", 1.20)), y0=1.14, dy=0.25))
  g.add(self._table((("p ( x )  =  ( x − b ) ⁿ        N  =  ⟨ t ⁱ e ᵇ ᵗ ⟩ ᵢ ₌ ₀ ⁿ ⁻ ¹", ACCENT_A),
                     ("        i          ‖ p ( D ) t ⁱ e ᵇ ᵗ ‖", DIM),)
                    + tuple((f"      {i}            {r:.2e}",
                             ACCENT_B if i < N42 else WARN) for i, r in RES42)
                    + ((f"det  ≠  0        {WR42:+.3f}", ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("最後那個 i 是紅的：剛好 n 個，不是 n 加一個",
                  "the last row is red: exactly n of them, not n plus one"))
  return g.add(self._foot("定理 4.2 的前半：p 是 x 減 b 的 n 次方時，解空間的基底是 e 的 b t 次方乘上 t 的零到 n 減一次方",
                          "the first half of Theorem 4.2: when the polynomial is x minus b to the n, the basis is the exponential of b t times the powers of t below n",
                          ACCENT_A,
                          "這正是上一集定理 3.4 那個答案取第一個座標。右表逐個代回去都是零，而 t 的 n 次方那一個不是零，所以剛好 n 個，是一組基底",
                          "that is last episode's Theorem 3.4 in first coordinates; each one substitutes to zero and the nth power does not, so there are exactly n and they form a basis"))

 # ── beat 3: relatively prime factors ────────────────────────────
 def _prime(self):
  ta, tb, oy, sy = 0.0, 2.4, -0.62, 0.38
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14),
             Line([XL, oy - 0.06, 0], [XL, oy + 0.98, 0], color=DIM, stroke_width=1.3))
  for f, col in ((lambda t: math.exp(B1 * t), ACCENT_A),
                 (lambda t: t * math.exp(B1 * t), ACCENT_B),
                 (lambda t: math.exp(B2 * t), ACCENT_C)):
   g.add(self._plot(f, col, ta, tb, oy, sy, sw=2.8))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "e ᵇ ¹ ᵗ", 1.00), (ACCENT_B, "t e ᵇ ¹ ᵗ", 1.30),
                                 (ACCENT_C, "e ᵇ ² ᵗ", 1.00)), y0=1.14, dy=0.25))
  g.add(self._table((("p ( x )  =  ( x − b ₁ ) ²  ( x − b ₂ )", ACCENT_A),
                     (f"b ₁  =  {B1:+.2f}        b ₂  =  {B2:+.2f}", DIM),
                     ("      B ₁  ∪  B ₂            ‖ p ( D ) · ‖", DIM),)
                    + tuple((f"      {lab}          {r:.2e}", ACCENT_B)
                            for lab, r in zip(("e ᵇ ¹ ᵗ    ", "t e ᵇ ¹ ᵗ  ", "e ᵇ ² ᵗ    "),
                                              RES43))
                    + ((f"det        {WR43:+.4f}", ACCENT_C),
                       ("Ch 1  ,  5.5", DIM)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("三條一起獨立，行列式不是零",
                  "the three are independent together, and that determinant is not zero"))
  return g.add(self._foot("後半：把 p 分解成互質的因式，每個因式照前一拍給出一組基底，全部聯集起來就是整個解空間的基底",
                          "the second half: factor the polynomial into relatively prime powers, take the previous beat's basis for each, and the union is a basis for the whole space",
                          ACCENT_A,
                          "理由是第 1 章定理 5.5 那個直和分解，經由同構搬到這裡來。圖上兩個因式各自的基底放在一起，右表的行列式證明它們沒有重複",
                          "the reason is chapter 1's direct sum decomposition carried over by the isomorphism; the two factors' bases are drawn together and the determinant shows none is redundant"))

 # ── beat 4: complexification ────────────────────────────────────
 def _complexify(self):
  oy = 0.56
  g = VGroup()
  g.add(self._box(-4.20, oy, "Z   =   Y   ⊕   i Y", ACCENT_B, w=2.90, h=0.60, size=FS_TAG))
  g.add(self._box(-5.05, oy - 0.96, "Y", ACCENT_A, w=0.86, h=0.52, size=FS_TAG + 1))
  g.add(self._box(-3.35, oy - 0.96, "i Y", DIM, w=0.86, h=0.52, size=FS_TAG + 1))
  g.add(self._arr([-5.05, oy - 0.34, 0], [-5.05, oy - 0.68, 0], DIM, sw=3, tl=0.12))
  g.add(self._arr([-3.35, oy - 0.34, 0], [-3.35, oy - 0.68, 0], DIM, sw=3, tl=0.12))
  g.add(self._sym(oy + 0.54, "S   :   Z   →   Z", ACCENT_B, FS_TAG - 1, x=-4.20, w=2.40))
  g.add(self._sym(oy - 1.44, "T   :   Y   →   Y", ACCENT_A, FS_TAG - 2,
                  x=-5.05, w=1.70))
  g.add(self._table((("Z   =   Y   ⊕   i Y", ACCENT_B),
                     ("N ( T )   =   N ( S )   ∩   Y", ACCENT_A),
                     ("f   =   Re ( f  +  i g )", ACCENT_C),
                     ("Ch 4  ,  § 11", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("第二列就是那個要補上的事實",
                  "the second row is the one extra fact that has to be supplied"))
  return g.add(self._foot("如果 p 的根不全是實數，就要用第 4 章第 11 節習題裡的複化理論。除了最後一步，結果一模一樣",
                          "if the roots are not all real we need the complexification theory from the exercises of chapter 4; except for one last step the results are the same",
                          ACCENT_A,
                          "要補的那個事實是：實算子在實空間上的零化空間，正好是它的複化的零化空間與實空間的交集。所以實的解就是複的解取實部",
                          "the extra fact is that a real operator's null space is the intersection with the real space of the complexified null space, so real solutions are real parts of complex ones"))

 # ── beat 5: the conjugate pair in the plane ─────────────────────
 def _pair(self):
  cx, cy, sx, sy = -4.20, 0.10, 1.30, 0.44
  g = VGroup(self._arr([cx - 1.55, cy, 0], [cx + 1.55, cy, 0], DIM, sw=3, tl=0.13),
             self._arr([cx, cy - 1.00, 0], [cx, cy + 1.00, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(cy - 0.24, "Re", DIM, FS_TAG - 3, x=cx + 1.36, w=0.60),
        self._sym(cy + 0.96, "Im", DIM, FS_TAG - 3, x=cx - 0.44, w=0.60))
  for sgn, lab, col in ((1.0, "λ", ACCENT_A), (-1.0, "λ̄", ACCENT_C)):
   px, py = cx + sx * BQ, cy + sgn * sy * WQ
   g.add(Dot([px, py, 0], radius=0.075, color=col))
   g.add(self._sym(py + sgn * 0.26, lab, col, FS_TAG, x=px - 0.34, w=0.40))
   g.add(self._sym(py + sgn * 0.26, f"m  =  {MQ}", col, FS_TAG - 4, x=px + 0.62, w=1.00))
   g.add(self._dash([cx, py, 0], [px, py, 0], DIM, n=6, sw=1.6))
  g.add(self._dash([cx + sx * BQ, cy, 0], [cx + sx * BQ, cy - sy * WQ, 0], DIM, n=10, sw=1.6))
  g.add(self._sym(cy + 0.20, f"b  =  {BQ:+.2f}", DIM, FS_TAG - 4, x=cx + sx * BQ - 0.52, w=1.10))
  g.add(self._table((("q ( x )   =   ( x ² − 2 b x + c ) ᵐ", ACCENT_A),
                     ("=   ( x − λ ) ᵐ  ( x − λ̄ ) ᵐ", ACCENT_A),
                     ("λ  =  b  +  i ω          ω ²  =  c  −  b ²", ACCENT_C),
                     (f"b  =  {BQ:+.2f}      ω  =  {WQ:.2f}      c  =  {CQ:.4f}", ACCENT_B),
                     (f"m  =  {MQ}          dim  =  {2 * MQ}", ACCENT_A)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("兩個點的實部相同，虛部差一個正負號",
                  "the two points share a real part and differ by the sign of the imaginary one"))
  return g.add(self._foot("設某個二次式在實數上不可約，而 p 的一個因式是它的 m 次方。在複數上它分解成 x 減 λ 與 x 減 λ 共軛，各 m 次方",
                          "let a quadratic be irreducible over the reals and one factor be its mth power: over the complex numbers it splits into x minus lambda and x minus its conjugate, each to the m",
                          ACCENT_A,
                          "其中 λ 的實部是 b、虛部是 ω，而 ω 平方等於常數項減去 b 平方。複的零化空間是 2 m 維的，基底是 t 的幂乘那兩個複指數",
                          "lambda has real part b and imaginary part omega, with omega squared the constant term less b squared; the complex null space has dimension two m, spanned by powers of t times those exponentials"))

 # ── beat 6: theorem 4.3, and the printed sign ───────────────────
 def _thm43(self):
  ta, tb, oy, sy = 0.0, 5.0, -0.30, 0.52
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  cols = (ACCENT_A, ACCENT_B, ACCENT_C, WARN)
  for f, col in zip(BAS4R, cols):
   g.add(self._plot(rf(f), col, ta, tb, oy, sy, sw=2.4))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "cos", 0.66), (ACCENT_B, "sin", 0.66),
                                 (ACCENT_C, "t cos", 1.00), (WARN, "t sin", 1.00)),
                     y0=1.14, dy=0.24))
  g.add(self._table((("{ t ⁱ e ᵇ ᵗ cos ω t }  ∪  { t ⁱ e ᵇ ᵗ sin ω t }", ACCENT_A),
                     ("          − 2 b x            + 2 b x", DIM),)
                    + tuple((f"      {lab}    {a:.1e}        {b:8.3f}", ACCENT_B)
                            for lab, (a, b) in zip(LAB4R, SIGN))
                    + ((f"det        {WR4R:+.3f}          dim  =  {2 * MQ}", ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("左欄是零，右欄不是：符號差一個就不成立",
                  "the left column is zero and the right one is not: one sign decides it"))
  return g.add(self._foot("取實部就得到定理 4.3：e 的 b t 次方乘 cos 與 sin，各再乘上 t 的零到 m 減一次方，一共 2 m 個，是實解空間的基底",
                          "taking real parts gives Theorem 4.3: the exponential of b t times cosine and sine, each with powers of t below m, two m functions, a basis for the real solution space",
                          ACCENT_A,
                          "書上那一行把二次式的中間項印成加號，與它自己上面兩段的推導不一致。右表兩欄就是兩個符號各自的殘差，畫面上用的是一致的那個",
                          "the book's display prints the quadratic's middle term with the opposite sign to its own derivation two paragraphs above; the table gives both residuals and the screen uses the consistent one"))

 # ── beat 7: D^4 - 1 ─────────────────────────────────────────────
 def _quartic(self):
  cx, cy, r = -4.20, 0.14, 0.62
  n = 120
  g = VGroup(self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                           cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                         DIM, sw=1.6))
  g.add(self._arr([cx - 1.05, cy, 0], [cx + 1.05, cy, 0], DIM, sw=3, tl=0.12),
        self._arr([cx, cy - 1.05, 0], [cx, cy + 1.05, 0], DIM, sw=3, tl=0.12))
  labs = (("1", 0.32, 0.26), ("− 1", -0.42, 0.26), ("i", 0.36, 0.26), ("− i", 0.42, -0.26))
  for root, (lab, dx, dy) in zip(ROOTS4, labs):
   px, py = cx + r * root.real, cy + r * root.imag
   g.add(Dot([px, py, 0], radius=0.072, color=ACCENT_A))
   # every root here sits on an axis, so the label has to leave both of them
   g.add(self._sym(py + dy, lab, ACCENT_A, FS_TAG - 2, x=px + dx, w=0.60))
  g.add(self._table((("x ⁴ − 1  =  ( x − 1 ) ( x + 1 ) ( x − i ) ( x + i )", ACCENT_A),
                     ("⟨ e ᵗ , e ⁻ ᵗ , e ⁱ ᵗ , e ⁻ ⁱ ᵗ ⟩", ACCENT_C),
                     ("e ⁱ ᵗ   =   cos t   +   i  sin t", ACCENT_B),
                     ("⟨ e ᵗ , e ⁻ ᵗ , cos t , sin t ⟩", ACCENT_A),
                     ("‖ p ( D ) · ‖   =   " + "  ".join(f"{r:.0e}" for r in RES4), ACCENT_B),
                     (f"det        {WR4:+.3f}", ACCENT_C)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("四個根落在單位圓上，彼此差九十度",
                  "the four roots sit on the unit circle, ninety degrees apart"))
  return g.add(self._foot("第一個例子：D 的四次方減一等於零。多項式分解成四個一次式，複的基底是四個指數",
                          "the first example: the fourth power of D minus one, whose polynomial splits into four linear factors, with four exponentials as the complex basis",
                          ACCENT_A,
                          "因為 e 的 i t 次方是 cos t 加 i sin t，取實部之後實的基底就是 e 的 t 次方、e 的負 t 次方、cos t、sin t，右表代回去都是零",
                          "since the exponential of i t is cosine plus i sine, taking real parts leaves two exponentials, a cosine and a sine, and each substitutes to zero in the table"))

 # ── beat 8: D^3 - 1 ─────────────────────────────────────────────
 def _cubic(self):
  ta, tb, oy, sy = 0.0, 4.2, -0.34, 0.60
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(lambda t: math.exp(-0.5 * t), DIM, ta, tb, oy, sy, sw=1.6))
  g.add(self._plot(lambda t: -math.exp(-0.5 * t), DIM, ta, tb, oy, sy, sw=1.6))
  g.add(self._plot(rf(BAS3[1]), ACCENT_A, ta, tb, oy, sy, sw=2.8))
  g.add(self._plot(rf(BAS3[2]), ACCENT_C, ta, tb, oy, sy, sw=2.8))
  g.add(self._legend(XL + 1.00, ((ACCENT_A, "e ⁻ ᵗ ᐟ ² cos", 1.70),
                                 (ACCENT_C, "e ⁻ ᵗ ᐟ ² sin", 1.70),
                                 (DIM, "±  e ⁻ ᵗ ᐟ ²", 1.30)), y0=1.14, dy=0.24))
  g.add(self._table((("x ³ − 1   =   ( x − 1 ) ( x ² + x + 1 )", ACCENT_A),
                     ("λ   =   − 1 / 2   ±   i √ 3 / 2", ACCENT_C),
                     (f"| λ ³ − 1 |   =   {abs(LAM3 ** 3 - 1.0):.1e}", ACCENT_B),
                     ("⟨ e ᵗ , e ⁻ ᵗ ᐟ ² cos ω t , e ⁻ ᵗ ᐟ ² sin ω t ⟩", ACCENT_A),
                     ("‖ p ( D ) · ‖   =   " + "  ".join(f"{r:.0e}" for r in RES3), ACCENT_B),
                     (f"det        {WR3:+.4f}", ACCENT_C)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("灰線是包絡線，兩條解在它裡面擺盪",
                  "the grey curves are the envelope the two solutions oscillate inside"))
  return g.add(self._foot("第二個例子：D 的三次方減一。分解成 x 減一乘上 x 平方加 x 加一，後面那個不可約，兩個根是負二分之一加減 i 乘根三除以二",
                          "the second example: the third power of D minus one splits into x minus one times an irreducible quadratic, whose roots are minus a half plus and minus i root three over two",
                          ACCENT_A,
                          "所以實的基底是 e 的 t 次方，以及 e 的負 t 除以二次方分別乘上 cos 與 sin。根的實部給了衰減率，虛部給了頻率，圖上兩者都看得到",
                          "so the real basis is the exponential of t together with a decaying exponential times a cosine and a sine: the root's real part sets the decay and its imaginary part the frequency"))

 # ── beat 9: the algebra ─────────────────────────────────────────
 def _algebra(self):
  ta, tb, oy, sy = 0.0, 2.0 * math.pi, -0.32, 0.62
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._plot(lambda t: 0.5 * math.sin(3.0 * t), ACCENT_B, ta, tb, oy, sy, sw=2.0))
  g.add(self._plot(lambda t: -0.5 * math.sin(t), ACCENT_C, ta, tb, oy, sy, sw=2.0))
  g.add(self._plot(fprod, ACCENT_A, ta, tb, oy, sy, sw=3.2))
  g.add(self._legend(XL + 0.06, ((ACCENT_A, "sin t cos 2 t", 1.80),
                                 (ACCENT_B, "sin 3 t / 2", 1.40),
                                 (ACCENT_C, "− sin t / 2", 1.40)), y0=1.14, dy=0.24))
  g.add(self._table((("2 sin x cos y  =  sin ( x + y )  +  sin ( x − y )", ACCENT_A),
                     (f"‖ Δ ‖   =   {IDENT:.1e}", ACCENT_B),
                     ("p ( D )  =  ( D ² + 1 ) ( D ² + 9 )", ACCENT_A),
                     ("      a ₀      a ₁      a ₂      a ₃      a ₄", DIM),
                     ("    " + "    ".join(f"{c:.0f}" for c in PANN), ACCENT_B),
                     (f"‖ p ( D ) f ‖  =  {RES9:.1e}        D ² + 1   :   {RES9ONE:.3f}",
                      ACCENT_C)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("橘線就是藍線加紫線，一格不差",
                  "the orange curve is the blue one plus the purple one, everywhere"))
  return g.add(self._foot("加星號的一段：所有常係數齊次方程的實值解合起來，對加法與乘法都封閉，是 t 的幂、指數、cos 與 sin 生成的代數",
                          "the starred passage: all real solutions of constant coefficient equations, taken together, are closed under addition and multiplication, the algebra generated by powers, exponentials, cosines and sines",
                          ACCENT_A,
                          "加法容易：兩個常係數算子一定交換，複合起來把兩邊的解都殺掉。乘法要靠三角恆等式把乘積寫成和——單獨一個因式殺不掉它，右表最後一列就是證據",
                          "sums are easy, since two such operators commute and the composite kills both; products need the identities that rewrite a product as a sum, and one factor alone does not kill it, as the last row shows"))

 # ── beat 10: translates span a finite-dimensional space ─────────
 def _translate(self):
  ta, tb, oy, sy = -3.0, 3.0, -0.40, 0.50
  g = VGroup(self._arr([XL - 0.14, oy, 0], [XR + 0.30, oy, 0], DIM, sw=3, tl=0.14))
  cols = (DIM, ACCENT_C, ACCENT_A, ACCENT_B, WARN)
  for x0, col in zip(XSHOW, cols):
   g.add(self._plot(lambda t, x0=x0: math.cos(t - x0), col, ta, tb, oy, sy,
                    sw=3.0 if x0 == 0.0 else 2.0))
  g.add(self._legend(XL + 0.06, ((DIM, "K ₋ ₂ f", 1.00), (ACCENT_C, "K ₋ ₁ f", 1.00),
                                 (ACCENT_A, "f", 0.44), (ACCENT_B, "K ₁ f", 0.90),
                                 (WARN, "K ₂ f", 0.90)), y0=1.14, dy=0.22))
  g.add(self._table((("K ₓ f ( t )   =   f ( t  −  x )", ACCENT_A),
                     ("T ∘ K ₓ  =  K ₓ ∘ T      ⇒      K ₓ [ N ]  ⊂  N", ACCENT_A),
                     ("                       σ ₁       σ ₂       σ ₃       σ ₄", DIM),
                     ("      cos             " + "  ".join(f"{v:.0e}" for v in SV["cos"][0][:4]),
                      ACCENT_B),
                     ("      exp ( − t ² )    "
                      + "  ".join(f"{v:.0e}" for v in SV["gauss"][0][:4]), ACCENT_C),
                     (f"dim   =   {SV['cos'][1]}            {SV['gauss'][1]}", ACCENT_A),
                     ("K ₛ ₊ ₜ  =  K ₛ ∘ K ₜ         K ₜ  =  exp ( t S )", DIM)),
                    y0=0.88, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("上面一列第三個數就掉到零，下面一列沒有",
                  "the upper row's third number has already collapsed to zero; the lower one's has not"))
  return g.add(self._foot("最後一件事很漂亮：這些函數恰好是「所有平移張成有限維空間」的那些連續函數。圖上五條都是同一個 cos 的平移",
                          "the last thing is lovely: these are exactly the continuous functions whose translates span a finite-dimensional space, and the five curves are translates of one cosine",
                          ACCENT_A,
                          "因為常係數算子正是與平移交換的線性微分算子，交換就讓零化空間在平移底下不變，而那個空間是有限維的。反過來那一半很細緻，書上沒證。第 4 節到此結束",
                          "constant coefficient operators are precisely those commuting with translation, commuting makes the null space translation invariant, and it is finite-dimensional; the converse is delicate and is left unproved"))

 def stage(self):
  a, b, c = self._pd(), self._route(), self._thm42()
  d, e, f_ = self._prime(), self._complexify(), self._pair()
  h, i, j = self._thm43(), self._quartic(), self._cubic()
  k, l = self._algebra(), self._translate()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE80ZH, AdvCalcE80EN = make(AdvCalcE80Base, "80", prefix="AdvCalcE")
