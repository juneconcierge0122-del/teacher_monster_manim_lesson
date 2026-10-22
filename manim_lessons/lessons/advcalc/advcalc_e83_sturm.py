"""advcalc E83 -- chapter 6, section 6, second half (book pp. 297-299): Lemma
6.4, the Sturm-Liouville vocabulary, and Theorems 6.1 and 6.2.

E82 settled what a self-adjoint boundary condition is.  This half spends that
definition on the heaviest result of the chapter: the subspace M the boundary
condition cuts out is a complement of the null space of T - lambda, so T -
lambda has a right inverse S determined by M, and S turns out to be a compact
self-adjoint operator on the pre-Hilbert space of continuous functions.  Once
that word compact is earned, Theorem 5.1 of chapter 5 carries over bodily and
hands back an orthonormal eigenbasis -- and Lemma 6.5 upgrades the convergence
of the expansion from the two-norm to the uniform norm.

The cut is Lemma 6.4 first because everything downstream is that one
inequality seen from a different angle: beat 3 reads it as injectivity on M,
beat 6 divides it by a norm twice, beat 7 feeds the surviving bound into
Schwarz.  The one place the book's own route is reordered is beat 2, which
does the integration by parts before the statement is used rather than after
it is stated, because the endpoint term vanishing is the whole reason the
boundary conditions appear in the hypothesis at all.

Two concrete systems carry the numbers.  Beats 1, 2, 6 and 7 use
T f = ((1 + t^2) f')' - f on [0, 1] with f(0) = f(1) = 0, so c2 runs over
[1, 2] and m = 1 -- beat 3's shooting numbers come from this one too, which is
what its table row now says; beats 8 to 10 use T = D^2 on [0, pi] with the same
Dirichlet condition, which is the example section 6 ends on.  Every integral
on screen is a 240-node Gauss-Legendre quadrature of an analytically
differentiated integrand -- no finite differences anywhere -- so the residual
of an identity that should be exact comes out at 1e-13 and not 1e-5, and the
only differential equation actually integrated (beat 3's null space, which has
no closed form) is run through RK4 at two step sizes that agree to thirteen
digits.

The inequality of Lemma 6.4 is checked honestly rather than comfortably.  With
lambda = 2 it holds for all four test functions with at least 38 percent to
spare, which is margin and not round-off.  With lambda = -5, which violates
lambda >= c0 + 1, it fails for the two low test functions and still holds for
the two with an interior sign change: the hypothesis is what makes the bound
uniform over M, not what makes any single f work.  Beat 1 draws exactly that,
failures and survivors side by side, instead of hiding the survivors.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Rectangle, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these

# ── quadrature ────────────────────────────────────────────────────────
# Everything integrated below has an analytic integrand, so a fixed
# Gauss-Legendre rule is exact to round-off and no step size has to be argued
# about. The integrands are at worst degree-6 polynomials times sines.
_GX, _GW = np.polynomial.legendre.leggauss(240)


def quad(f, a, b):
 x = 0.5 * (b - a) * _GX + 0.5 * (a + b)
 return 0.5 * (b - a) * float(np.dot(_GW, f(x)))


# ── system A:  T f = ((1 + t^2) f')' - f  on [0, 1],  f(0) = f(1) = 0 ──
A, B = 0.0, 1.0
C0 = -1.0
c2 = lambda t: 1.0 + t * t
c2p = lambda t: 2.0 * t
MM = float(min(c2(t) for t in np.linspace(A, B, 4001)))
assert abs(MM - 1.0) < 1e-12, "c2 bottoms out at 1 on [0,1], so m = 1 is the best constant"
assert c2(A) > 0 and c2(B) > 0, "c2 is nowhere zero on the closed interval: the system is regular"
LAM, LBAD = 2.0, -5.0
assert LAM >= C0 + 1.0, "the good lambda satisfies the hypothesis lambda >= c0 + 1"
assert LBAD < C0 + 1.0, "the bad lambda violates it, which is the point of showing it"

TESTF = (
 ("f ₁", lambda t: np.sin(np.pi * t),
  lambda t: np.pi * np.cos(np.pi * t),
  lambda t: -np.pi ** 2 * np.sin(np.pi * t)),
 ("f ₂", lambda t: t * (1.0 - t), lambda t: 1.0 - 2.0 * t, lambda t: -2.0 + 0.0 * t),
 ("f ₃", lambda t: np.sin(2.0 * np.pi * t),
  lambda t: 2.0 * np.pi * np.cos(2.0 * np.pi * t),
  lambda t: -4.0 * np.pi ** 2 * np.sin(2.0 * np.pi * t)),
 ("f ₄", lambda t: t * (1.0 - t) * (1.0 - 2.0 * t),
  lambda t: 1.0 - 6.0 * t + 6.0 * t * t, lambda t: -6.0 + 12.0 * t),
)


def oper(f, fp, fpp):
 """T f = (c2 f')' + c0 f, expanded so nothing is differenced numerically."""
 return lambda t: c2p(t) * fp(t) + c2(t) * fpp(t) + C0 * f(t)


LEM = []            # one row per test function
for _lab, _f, _fp, _fpp in TESTF:
 _T = oper(_f, _fp, _fpp)
 _nf2 = quad(lambda t: _f(t) ** 2, A, B)
 _nfp2 = quad(lambda t: _fp(t) ** 2, A, B)
 _rhs = MM * _nfp2 + _nf2
 _bdry = -(c2(B) * _fp(B) * _f(B) - c2(A) * _fp(A) * _f(A))
 _i1 = quad(lambda t: c2(t) * _fp(t) ** 2, A, B)
 _row = {"lab": _lab, "nf": math.sqrt(_nf2), "nfp": math.sqrt(_nfp2),
         "rhs": _rhs, "bdry": _bdry, "i1": _i1}
 for _tag, _lam in (("ok", LAM), ("bad", LBAD)):
  _direct = quad(lambda t, l=_lam: (_T(t) - l * _f(t)) * _f(t), A, B)
  _i2 = quad(lambda t, l=_lam: (l - C0) * _f(t) ** 2, A, B)
  _row[_tag] = {"lam": _lam, "lhs": abs(_direct), "parts": _bdry + _i1 + _i2,
                "i2": _i2, "ratio": abs(_direct) / _rhs,
                "gap": abs(abs(_direct) - (_bdry + _i1 + _i2))}
 LEM.append(_row)

assert all(abs(r["bdry"]) < 1e-14 for r in LEM), \
    "every test function vanishes at both ends, so the endpoint term of the parts formula is zero"
assert all(r[t]["gap"] < 1e-11 for r in LEM for t in ("ok", "bad")), \
    "the integration by parts identity reproduces the inner product, both lambdas"
assert all(r["ok"]["ratio"] > 1.0 for r in LEM), \
    "Lemma 6.4 holds for every test function once lambda >= c0 + 1"
assert min(r["ok"]["ratio"] for r in LEM) > 1.38, \
    "and holds with real margin, not by a round-off's worth"
assert LEM[0]["bad"]["ratio"] < 1.0 and LEM[1]["bad"]["ratio"] < 1.0, \
    "below the lambda threshold the inequality genuinely fails for the two lowest test functions"
assert LEM[2]["bad"]["ratio"] > 1.0 and LEM[3]["bad"]["ratio"] > 1.0, \
    "while the two with an interior sign change survive: the hypothesis buys uniformity over M"
RMAX = max(r[t]["ratio"] for r in LEM for t in ("ok", "bad"))

# ── beat 2: the two integrands of the parts formula, for f1 ───────────
_lab2, _f2, _fp2, _fpp2 = TESTF[0]
_T2 = oper(_f2, _fp2, _fpp2)
IDIR = lambda t: (LAM * _f2(t) - _T2(t)) * _f2(t)          # ((lambda - T) f, f)
IPAR = lambda t: c2(t) * _fp2(t) ** 2 + (LAM - C0) * _f2(t) ** 2
AREA = quad(IDIR, A, B)
assert abs(quad(IPAR, A, B) - AREA) < 1e-11, \
    "the two integrands differ pointwise but enclose the same area: that is the parts identity"
IMAX = max(float(np.max(IDIR(np.linspace(A, B, 2001)))),
           float(np.max(IPAR(np.linspace(A, B, 2001)))))
assert float(np.max(np.abs(IDIR(np.linspace(A, B, 801)) - IPAR(np.linspace(A, B, 801))))) > 1.0, \
    "and they really are different curves, not the same one drawn twice"

# ── beat 3: the null space of T - lambda misses M ─────────────────────
# ((1 + t^2) u')' - u = lambda u has no closed form, so this one ODE is
# integrated. RK4 at two step sizes agreeing to 13 digits is what licenses
# reading the determinant below as "not zero".
def _rk4(y0, n):
 h = (B - A) / n
 t, y = A, y0
 for _ in range(n):
  def d(tt, yy):
   return (yy[1], ((LAM - C0) * yy[0] - c2p(tt) * yy[1]) / c2(tt))
  k1 = d(t, y)
  k2 = d(t + h / 2, (y[0] + h / 2 * k1[0], y[1] + h / 2 * k1[1]))
  k3 = d(t + h / 2, (y[0] + h / 2 * k2[0], y[1] + h / 2 * k2[1]))
  k4 = d(t + h, (y[0] + h * k3[0], y[1] + h * k3[1]))
  y = (y[0] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
       y[1] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
  t += h
 return y


U1B = _rk4((1.0, 0.0), 4000)[0]
U2B = _rk4((0.0, 1.0), 4000)[0]
assert abs(U2B - _rk4((0.0, 1.0), 1000)[0]) < 1e-11, "the RK4 value has converged in the step size"
DETN = 1.0 * U2B - 0.0 * U1B          # det [[u1(a), u2(a)], [u1(b), u2(b)]]
assert abs(DETN) > 1e-3, \
    "the two boundary functionals are an isomorphism of N(T - lambda) onto the plane"
assert abs(DETN) > 1.0, "so no nonzero solution of (T - lambda) f = 0 lies in M: M and N meet only at 0"

# ── beat 4: regular against singular ──────────────────────────────────
c2sing = lambda t: 1.0 - t * t
assert abs(c2sing(B)) < 1e-15, "the singular example's leading coefficient dies at the right endpoint"
assert min(c2sing(t) for t in np.linspace(A, B - 1e-6, 4001)) > 0.0, \
    "and is positive strictly inside, so it is the endpoint alone that spoils regularity"

# ── beats 6 and 7: the two bounds, and the Holder estimate ────────────
BND = []
for _lab, _f, _fp, _fpp in TESTF:
 _T = oper(_f, _fp, _fpp)
 _g = lambda t, F=_f, O=_T: O(t) - LAM * F(t)
 _ng = math.sqrt(quad(lambda t: _g(t) ** 2, A, B))
 _nf = math.sqrt(quad(lambda t: _f(t) ** 2, A, B))
 _nfp = math.sqrt(quad(lambda t: _fp(t) ** 2, A, B))
 BND.append({"lab": _lab, "ng": _ng, "nf": _nf, "nfp": _nfp,
             "r1": _nf / _ng, "r2": math.sqrt(MM) * _nfp / _ng})
assert all(b["r1"] < 1.0 for b in BND), "Schwarz plus the lemma give the two-norm of f under that of g"
assert all(b["r2"] < 1.0 for b in BND), "and the two-norm of f' under that of g over root m"
assert all(b["r2"] > b["r1"] for b in BND), \
    "the derivative bound is the binding one of the two, which is why compactness needs it"

# Functions scaled to |f'|_2 = 1, the extreme case the unit ball allows: for
# them the Holder bound reads |f(y) - f(x)| <= |y - x|^(1/2) exactly.
_TG = np.linspace(A, B, 801)
HOLD = []
for _k in (0, 2):
 _lab, _f, _fp, _fpp = TESTF[_k]
 _s = 1.0 / math.sqrt(quad(lambda t: _fp(t) ** 2, A, B))
 _v = _s * _f(_TG)
 _d = np.abs(_v[:, None] - _v[None, :])
 _r = np.sqrt(np.abs(_TG[:, None] - _TG[None, :])) + np.eye(len(_TG))
 HOLD.append({"lab": _lab, "s": _s, "peak": float(np.max(np.abs(_v))),
              "worst": float(np.max(_d / _r)),
              "fn": (lambda t, F=_f, S=_s: S * F(t))})
HLIM = 1.0 / math.sqrt(MM)
assert all(h["worst"] < HLIM for h in HOLD), \
    "the Holder estimate holds for both, with the constant the theorem promises"
assert all(h["peak"] <= math.sqrt(B - A) / math.sqrt(MM) + 1e-12 for h in HOLD), \
    "and anchoring at the left endpoint bounds the functions themselves, not just their oscillation"
assert HOLD[0]["peak"] > 1.6 * HOLD[1]["peak"], \
    "the two drawn curves differ by more than their shape: one hump against two, at different heights"
CSUP = 1.0 / math.sqrt(B - A) + math.sqrt(B - A) / math.sqrt(MM)

# ── system B:  T = D^2 on [0, pi],  f(0) = f(pi) = 0 ──────────────────
PI = math.pi
_EX, _EW = np.polynomial.legendre.leggauss(400)
_XX = 0.5 * PI * (_EX + 1.0)
_WW = 0.5 * PI * _EW
NMAX = 6
EIG = []
for _n in range(1, NMAX + 1):
 _mu = -float(_n * _n)
 _r = 1.0 / (_mu - LAM)
 EIG.append({"n": _n, "mu": _mu, "r": _r, "back": (1.0 + LAM * _r) / _r})
assert all(abs(e["back"] - e["mu"]) < 1e-12 for e in EIG), \
    "S phi = r phi translates back to T phi = ((1 + lambda r)/r) phi exactly"
assert all(abs(EIG[k + 1]["r"]) < abs(EIG[k]["r"]) for k in range(NMAX - 1)), \
    "the eigenvalues of the right inverse shrink monotonically"
assert abs(EIG[-1]["r"]) < 0.03, "and pile up at zero, which is how a compact operator looks"
ORTH = [[float(np.dot(_WW, np.sin(_i * _XX) * np.sin(_j * _XX)))
         for _j in range(1, 4)] for _i in range(1, 4)]
assert max(abs(ORTH[i][j]) for i in range(3) for j in range(3) if i != j) < 1e-13, \
    "distinct sines are orthogonal on [0, pi]"
assert all(abs(ORTH[i][i] - PI / 2.0) < 1e-13 for i in range(3)), \
    "and each has squared two-norm pi over two"

# ── beat 9: the Fourier expansion of x(pi - x) ────────────────────────
fx = lambda x: x * (PI - x)
bcl = lambda n: 8.0 / (PI * n ** 3) if n % 2 else 0.0
BNUM = [(n, 2.0 / PI * float(np.dot(_WW, fx(_XX) * np.sin(n * _XX))), bcl(n))
        for n in range(1, 6)]
assert all(abs(num - cl) < 1e-12 for _n, num, cl in BNUM), \
    "the coefficients really are 8 over pi n cubed for odd n and zero for even n"
_FG = np.linspace(0.0, PI, 6001)
_FV = fx(_FG)
FOUR = []
for _N in (1, 3, 5, 7, 9):
 _S = np.zeros_like(_FG)
 for _n in range(1, _N + 1, 2):
  _S += bcl(_n) * np.sin(_n * _FG)
 _e = np.abs(_FV - _S)
 FOUR.append({"N": _N, "sup": float(_e.max()),
              "two": math.sqrt(sum(bcl(n) ** 2 for n in range(_N + 2, 60001, 2)) * PI / 2.0),
              "tail": sum(bcl(n) for n in range(_N + 2, 60001, 2)),
              "err": (_FG.copy(), _FV - _S)})
assert all(FOUR[k + 1]["sup"] < FOUR[k]["sup"] for k in range(len(FOUR) - 1)), \
    "the uniform error falls with every extra term: the series converges uniformly"
assert all(FOUR[k + 1]["two"] < FOUR[k]["two"] for k in range(len(FOUR) - 1)), \
    "and so does the two-norm error, which is the weaker of the two statements"
assert all(d["sup"] <= d["tail"] for d in FOUR), \
    "the uniform error never exceeds the tail of the coefficients, which is why it is uniform"
assert all(d["two"] <= math.sqrt(PI) * d["sup"] + 1e-12 for d in FOUR), \
    "and the two-norm is dominated by the uniform norm, the hypothesis of Lemma 6.5"
assert FOUR[0]["sup"] / FOUR[1]["sup"] > 3.0, \
    "the two drawn error curves differ in size by more than a line width"
E1MAX = max(abs(FOUR[0]["err"][1].max()), abs(FOUR[0]["err"][1].min()))


class AdvCalcE83Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 83

 MODE_LABEL = {
  0: {"zh": "這一集的路線圖", "en": "the route of this episode"},
  1: {"zh": "引理 6.4 的不等式", "en": "the inequality of Lemma 6.4"},
  2: {"zh": "分部積分一次", "en": "one integration by parts"},
  3: {"zh": "M 是零化空間的補", "en": "M is a complement of the null space"},
  4: {"zh": "名詞：Sturm-Liouville 系統", "en": "terminology: a Sturm-Liouville system"},
  5: {"zh": "定理 6.1：緊的自伴右逆",
      "en": "Theorem 6.1: a compact self-adjoint right inverse"},
  6: {"zh": "第一步：兩個界", "en": "first step: the two bounds"},
  7: {"zh": "第二步：等度連續，所以緊", "en": "second step: equicontinuous, hence compact"},
  8: {"zh": "定理 6.2：特徵基底", "en": "Theorem 6.2: the eigenbasis"},
  9: {"zh": "引理 6.5：兩個範數都收斂", "en": "Lemma 6.5: convergence in both norms"},
  10: {"zh": "一個例子，第 6 節結束", "en": "one example, and the end of section 6"},
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
  parameter, so nothing has to be assumed about where t = 0 lands."""
  return self._curve([[xl + (xr - xl) * k / n,
                       oy + sy * f(ta + (tb - ta) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _xof(self, t, ta, tb, xl=XL, xr=XR):
  return xl + (xr - xl) * (t - ta) / (tb - ta)

 def _bar(self, x, y0, h, col, w=0.30):
  return Rectangle(width=w, height=abs(h), color=col, stroke_width=1.6,
                   fill_color=col, fill_opacity=0.5).move_to([x, y0 + h / 2.0, 0])

 # ── beat 0: the route of the proof ──────────────────────────────
 def _route(self):
  g = VGroup()
  ys = (1.10, 0.62, 0.14, -0.34, -0.82)
  steps = (("T  ,  l ₁  ,  l ₂", ACCENT_C, 2.30),
           ("M  =  N ( l ₁ )  ∩  N ( l ₂ )", ACCENT_A, 3.20),
           ("( T − λ ) S   =   I", ACCENT_B, 2.60),
           ("S *  =  S          Ch 4 , 6.1", ACCENT_B, 3.20),
           ("Ch 5 , 5.1      ⇒      { φ ₙ }", ACCENT_A, 3.20))
  for y, (lab, col, w) in zip(ys, steps):
   g.add(self._box(-4.20, y, lab, col, w=w, h=0.30, size=FS_TAG - 3))
  for ya, yb in zip(ys, ys[1:]):
   g.add(self._arr([-4.20, ya - 0.15, 0], [-4.20, yb + 0.15, 0], DIM, sw=3, tl=0.10))
  g.add(self._table((("T f  =  ( c ₂ f ′ ) ′  +  c ₀ f", ACCENT_C),
                     ("( T f , g )  =  ( f , T g )        f , g  ∈  M", ACCENT_A),
                     ("S  =  ( T − λ ) ⁻ ¹  ↾  M", ACCENT_B),
                     ("S *   =   S", DIM),
                     ("T φ ₙ  =  μ ₙ φ ₙ          ( φ ₙ , φ ₘ )  =  δ ₙ ₘ", ACCENT_A)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("下面三格是這一集要掙到的三個字",
                  "the lower three boxes are the three words this episode has to earn"))
  return g.add(self._foot("上一集把自伴邊界條件講清楚了，這一集要用它證出整章最重的那個結果",
                          "last episode pinned down the self-adjoint boundary condition, and this one spends it on the heaviest result of the chapter",
                          ACCENT_A,
                          "邊界條件切出來的子空間是零化空間的補，於是 T 減 λ 有一個右逆；證出這個右逆又緊又自伴，第五章的特徵基底定理就整套搬得過來",
                          "the subspace the condition cuts out complements the null space, so there is a right inverse; show it is compact and self-adjoint and chapter five's eigenbasis theorem transfers wholesale"))

 # ── beat 1: the inequality of Lemma 6.4 ─────────────────────────
 def _lemma(self):
  oy, sy = -0.80, 1.70 / RMAX
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12))
  g.add(self._dash([XL, oy + sy, 0], [XR, oy + sy, 0], DIM, n=22, sw=1.8))
  g.add(self._sym(oy + sy, "1", DIM, FS_TAG - 3, x=-2.22, w=0.26),
        self._sym(oy, "0", DIM, FS_TAG - 3, x=-2.22, w=0.26))
  for k, row in enumerate(LEM):
   cx = XL + 0.425 + 0.85 * k
   g.add(self._bar(cx - 0.18, oy, sy * row["ok"]["ratio"], ACCENT_A))
   g.add(self._bar(cx + 0.18, oy, sy * row["bad"]["ratio"], WARN))
   g.add(self._sym(oy - 0.15, row["lab"], DIM, FS_TAG - 3, x=cx, w=0.46))
  g.add(self._legend(-3.86, ((ACCENT_A, f"λ  =  {LAM:+.0f}", 0.78),
                             (WARN, f"λ  =  {LBAD:+.0f}", 0.78)), y0=1.14, dy=0.24))
  g.add(self._table((("c ₂  =  1 + t ²        c ₀  =  − 1        [ 0 , 1 ]", ACCENT_C),
                     (f"m  =  {MM:.2f}            c ₀ + 1  =  {C0 + 1:.0f}", DIM),
                     ("          | ( ( T − λ ) f , f ) |   /   ( m ‖ f ′ ‖ ₂ ² + ‖ f ‖ ₂ ² )", DIM),)
                    + tuple((f"      {r['lab']}          {r['ok']['ratio']:.3f}"
                             f"          {r['bad']['ratio']:.3f}",
                             WARN if r["bad"]["ratio"] < 1.0 else ACCENT_B)
                            for r in LEM)
                    + (("f ₁ = sin π t      f ₂ = t ( 1 − t )", DIM),
                       ("f ₃ = sin 2 π t      f ₄ = t ( 1 − t ) ( 1 − 2 t )", DIM)),
                    y0=0.90, dy=0.20, size=FS_TAG - 4))
  g.add(self._cap("紅柱掉到虛線以下的那兩列，表上也標成紅的",
                  "the two rows whose red bar falls under the line are red in the table too"))
  return g.add(self._foot("引理 6.4：在那三種邊界條件之下，c 二不小於正的 m、λ 至少比 c 零大一，那麼內積的絕對值不小於 m 乘導數的平方範數加上 f 的平方範數",
                          "Lemma 6.4: under those boundary conditions, with c two at or above a positive m and lambda at least one above c zero, that inner product beats m times the squared norm of the derivative plus the squared norm of f",
                          ACCENT_A,
                          "λ 取得太小的時候，前兩個試驗函數的紅柱就掉到一以下。後兩個照樣撐住——所以那個條件買到的不是某一個 f，是整個子空間上的一致下界",
                          "with lambda too small the first two test functions drop below one while the last two hold up, so what the hypothesis buys is not any single f but one bound uniform over the whole subspace"))

 # ── beat 2: the integration by parts ────────────────────────────
 def _parts(self):
  oy, sy = -0.95, 1.85 / IMAX
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12),
             Line([XL, oy - 0.06, 0], [XL, oy + 1.90, 0], color=DIM, stroke_width=1.3))
  g.add(self._plot(lambda t: float(IDIR(np.array([t]))[0]), ACCENT_A, A, B, oy, sy, sw=3.0))
  g.add(self._plot(lambda t: float(IPAR(np.array([t]))[0]), ACCENT_C, A, B, oy, sy, sw=3.0))
  g.add(self._legend(-5.84, ((ACCENT_A, "( λ f − T f )  f", 1.30),
                             (ACCENT_C, "c ₂ ( f ′ ) ²  +  ( λ − c ₀ ) f ²", 2.20)),
                     y0=1.14, dy=0.24))
  g.add(self._table((("( ( λ − T ) f , f )   =   [ − c ₂ f ′ f ] ₐ ᵇ", ACCENT_A),
                     ("+  ∫ c ₂ ( f ′ ) ² d t  +  ∫ ( λ − c ₀ ) f ² d t", ACCENT_C),
                     (f"[ − c ₂ f ′ f ] ₐ ᵇ   =   {LEM[0]['bdry']:.1e}", ACCENT_B),
                     (f"∫ c ₂ ( f ′ ) ² d t    =    {LEM[0]['i1']:.4f}    ≥    "
                      f"m ‖ f ′ ‖ ₂ ²  =  {MM * LEM[0]['nfp'] ** 2:.4f}", ACCENT_A),
                     (f"∫ ( λ − c ₀ ) f ² d t   =   {LEM[0]['ok']['i2']:.4f}   ≥   "
                      f"‖ f ‖ ₂ ²  =  {LEM[0]['nf'] ** 2:.4f}", ACCENT_C),
                     (f"兩 ∫   =   {AREA:.5f}          Δ   =   {LEM[0]['ok']['gap']:.1e}", DIM)),
                    y0=0.90, dy=0.24, size=FS_TAG - 4))
  g.add(self._cap("兩條曲線形狀完全不同，底下的面積一樣",
                  "the two curves have nothing in common but the area under them"))
  return g.add(self._foot("分部積分一次：λ 減 T 作用在 f 上與 f 的內積，等於一個端點項，加上 c 二乘導數平方的積分，再加上 λ 減 c 零乘 f 平方的積分",
                          "one integration by parts: that inner product is an endpoint term, plus the integral of c two times the derivative squared, plus the integral of lambda minus c zero times f squared",
                          ACCENT_A,
                          "那三種邊界條件剛好讓端點項變成零，剩下的兩個積分一個被 m 乘導數的平方範數界住，一個被 f 的平方範數界住，加起來就是引理",
                          "the listed conditions kill the endpoint term, and the two surviving integrals are bounded below by m times the one squared norm and by the other, which is the lemma"))

 # ── beat 3: M is a complement of the null space ─────────────────
 def _complement(self):
  ox, oy = -4.30, 0.02
  um = np.array([0.977, 0.215, 0.0])
  un = np.array([0.243, 0.970, 0.0])
  o = np.array([ox, oy, 0.0])
  g = VGroup(Line(o - 1.50 * um, o + 1.50 * um, color=ACCENT_A, stroke_width=2.6),
             Line(o - 0.86 * un, o + 0.86 * un, color=ACCENT_C, stroke_width=2.6))
  pm, pn = o + 1.05 * um, o + 0.52 * un
  v = pm + 0.52 * un
  g.add(Dot(v, radius=0.075, color=ACCENT_B), Dot(o, radius=0.055, color=DIM))
  g.add(Dot(pm, radius=0.055, color=ACCENT_A), Dot(pn, radius=0.055, color=ACCENT_C))
  g.add(self._dash(pm, v, DIM, n=7, sw=1.6), self._dash(pn, v, DIM, n=9, sw=1.6))
  # 標籤要貼著它命名的那條線的端點，不是貼著一個沒有畫出來的半長；
  # 而且要放在端點左邊——放右邊會壓到那個 h
  g.add(self._sym(o[1] + 0.86 * un[1] + 0.19, "N ( T − λ )", ACCENT_C, FS_TAG - 2,
                  x=ox + 0.86 * un[0] - 0.80, w=1.34))
  g.add(self._sym(o[1] - 1.50 * um[1] - 0.20, "M", ACCENT_A, FS_TAG - 1, x=ox - 1.52, w=0.34))
  # v 是兩個分量的和，所以它是 f；h 是 N 方向那一個，標在 pn 旁邊
  g.add(self._sym(v[1] + 0.20, "f", ACCENT_B, FS_TAG - 2, x=v[0] + 0.14, w=0.30))
  g.add(self._sym(pn[1] + 0.20, "h", ACCENT_C, FS_TAG - 2, x=pn[0] - 0.20, w=0.30))
  g.add(self._sym(o[1] - 0.24, "0", DIM, FS_TAG - 3, x=ox - 0.16, w=0.26))
  g.add(self._table((("f  ∈  M  ,  ( T − λ ) f  =  0      ⇒      f  =  0", ACCENT_A),
                     ("Ch 6 , 6.3      ⇒      𝒞 ⁰  =  M  ⊕  N ( T − λ )", ACCENT_B),
                     ("dim  N ( T − λ )   =   2", ACCENT_C),
                     ("c ₂  =  1 + t ²  ,  [ 0 , 1 ]  ,  λ  =  2", DIM),)
                    + tuple((f"      {s}", DIM) for s in
                            ("u ₁ ( a )  =  1      u ₂ ( a )  =  0",))
                    + ((f"u ₁ ( b )  =  {U1B:.4f}      u ₂ ( b )  =  {U2B:.4f}", ACCENT_C),
                       (f"det   =   {DETN:.4f}   ≠   0", ACCENT_A)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("那個行列式不是零，所以兩條線只在原點相遇",
                  "that determinant is not zero, so the two lines meet only at the origin"))
  return g.add(self._foot("不等式右邊是正的，所以子空間裡只有零向量會被 T 減 λ 送到零。引理 6.3 說這時候它就是零化空間的補",
                          "the right-hand side is positive, so the only vector of the subspace that T minus lambda kills is zero, and Lemma 6.3 then makes it a complement of the null space",
                          ACCENT_A,
                          "零化空間是二維的，兩個邊界泛函把它等同於平面；表上那個行列式就是這件事的數值版本。於是 T 減 λ 有一個由子空間決定的自伴右逆",
                          "the null space is two dimensional and the two boundary functionals identify it with the plane, which is what the determinant in the table says, so the right inverse exists and is self-adjoint"))

 # ── beat 4: regular against singular ────────────────────────────
 def _regular(self):
  oy, sy = -0.60, 0.70
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12),
             Line([XL, oy - 0.06, 0], [XL, oy + 1.60, 0], color=DIM, stroke_width=1.3))
  g.add(self._plot(lambda t: c2(t), ACCENT_A, A, B, oy, sy, sw=3.0))
  g.add(self._plot(lambda t: c2sing(t), WARN, A, B, oy, sy, sw=3.0))
  g.add(self._dash([XL, oy + sy * MM, 0], [XR, oy + sy * MM, 0], DIM, n=22, sw=1.6))
  g.add(Dot([XR, oy, 0], radius=0.082, color=WARN))
  g.add(self._sym(oy + sy * MM, f"m", DIM, FS_TAG - 3, x=-2.26, w=0.34))
  g.add(self._sym(oy, "0", DIM, FS_TAG - 3, x=XL - 0.22, w=0.26))
  g.add(self._sym(oy + 1.72, "c ₂", DIM, FS_TAG - 3, x=XL + 0.10, w=0.40))
  g.add(self._legend(-4.36, ((ACCENT_A, "1  +  t ²", 0.88), (WARN, "1  −  t ²", 0.88)),
                     y0=1.22, dy=0.24))
  g.add(self._table((("T f  =  ( c ₂ f ′ ) ′  +  c ₀ f          l ₁ ( f ) = l ₂ ( f ) = 0", ACCENT_A),
                     ("c ₂ ( t )  ≠  0        t  ∈  [ a , b ]", ACCENT_B),
                     (f"min  c ₂   =   {MM:.2f}   >   0", ACCENT_B),
                     (f"c ₂ ( b )   =   {c2sing(B):.1f}", WARN),
                     ("[ a , ∞ )", WARN)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("紅點落在軸上，橘線一路離軸一段距離",
                  "the red dot sits on the axis; the orange curve never comes near it"))
  return g.add(self._foot("Sturm-Liouville 系統：一個形式自伴的二階算子，先把導數乘上 c 二再微分，加上 c 零乘 f，配上自伴的邊界條件",
                          "a Sturm-Liouville system is a formally self-adjoint second order operator, the derivative weighted by c two and differentiated again plus c zero times f, with a self-adjoint boundary condition",
                          ACCENT_A,
                          "c 二在閉區間上處處不為零就叫正則；在端點變成零、或者區間變成無窮長，就叫奇異。表上第二、三列是正則，第四、五列各是一種奇異",
                          "it is regular when c two is nowhere zero on the closed interval, and singular when c two dies at an endpoint or the interval runs to infinity, which are the last two rows"))

 # ── beat 5: the statement of Theorem 6.1 ────────────────────────
 def _thm61(self):
  cy = 0.16
  n = 90
  g = VGroup(self._curve([[-5.08 + 0.62 * math.cos(2 * math.pi * k / n),
                           cy + 0.62 * math.sin(2 * math.pi * k / n), 0]
                          for k in range(n + 1)], ACCENT_B, sw=2.4))
  g.add(self._curve([[-3.05 + 0.50 * math.cos(2 * math.pi * k / n),
                      cy + 0.34 * math.sin(2 * math.pi * k / n), 0]
                     for k in range(n + 1)], ACCENT_A, sw=2.4))
  g.add(self._arr([-4.38, cy, 0], [-3.62, cy, 0], ACCENT_C, sw=3, tl=0.13))
  g.add(self._sym(cy + 0.24, "S", ACCENT_C, FS_TAG, x=-4.00, w=0.32))
  g.add(self._sym(cy, "U", ACCENT_B, FS_TAG + 1, x=-5.08, w=0.36))
  g.add(self._sym(cy - 0.86, "‖ g ‖ ₂  ≤  1", ACCENT_B, FS_TAG - 3, x=-5.08, w=1.20))
  g.add(self._sym(cy - 0.66, "S [ U ]", ACCENT_A, FS_TAG - 2, x=-3.05, w=0.80))
  lim = np.array([-3.02, cy + 0.02, 0.0])
  for k in range(6):
   ang = 1.0 + 2.3 * k
   rad = 0.40 * 0.62 ** k
   g.add(Dot([lim[0] + rad * math.cos(ang), lim[1] + 0.68 * rad * math.sin(ang), 0],
             radius=0.044, color=DIM))
  g.add(Dot(lim, radius=0.060, color=ACCENT_C))
  g.add(self._table((("T  :  l ₁ , l ₂            c ₂  >  0", ACCENT_C),
                     ("λ   ≫   0            Ch 6 , 6.4", ACCENT_C),
                     ("S  :  𝒞 ⁰ ( [ a , b ] )  →  𝒞 ⁰ ( [ a , b ] )", ACCENT_A),
                     ("S *  =  S", ACCENT_B),
                     ("cl ( S [ U ] )            Ch 4 , 6.1", ACCENT_B),
                     ("Ch 5 , 5.1      ⇒      { φ ₙ }", ACCENT_A)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("灰點是像裡的一串，紫點是它們收斂到的地方",
                  "the grey dots are a sequence in the image and the purple one is where it lands"))
  return g.add(self._foot("定理 6.1：系統正則、c 二為正、λ 取得夠大時，那個右逆是把連續函數空間映到自己的緊自伴算子",
                          "Theorem 6.1: for a regular system with c two positive and lambda taken large enough, the right inverse is a compact self-adjoint map of the continuous functions into themselves",
                          ACCENT_A,
                          "緊這個字是關鍵，因為第五章的特徵基底定理要的正好就是緊加自伴。證明分兩步，先從引理擠出兩個界，再用那兩個界換到等度連續",
                          "compact is the key word, because compact and self-adjoint is exactly what chapter five's eigenbasis theorem asks for; the proof squeezes two bounds out of the lemma and trades them for equicontinuity"))

 # ── beat 6: the two bounds, on a logarithmic axis ───────────────
 def _bounds(self):
  lo, hi = -2.2, 0.1
  xa, xb = -5.40, -2.60
  xof = lambda u: xa + (u - lo) / (hi - lo) * (xb - xa)
  ys = (0.78, 0.34, -0.10, -0.54)
  g = VGroup(self._arr([xa - 0.14, -0.86, 0], [xb + 0.10, -0.86, 0], DIM, sw=3, tl=0.12))
  g.add(Line([xof(0.0), -0.80, 0], [xof(0.0), 0.94, 0], color=DIM, stroke_width=2.0))
  for u, lab in ((-2.0, "0.01"), (-1.0, "0.1"), (0.0, "1")):
   g.add(self._sym(-1.00, lab, DIM, FS_TAG - 4, x=xof(u), w=0.52))
   g.add(Line([xof(u), -0.86, 0], [xof(u), -0.80, 0], color=DIM, stroke_width=2.0))
  for y, b in zip(ys, BND):
   x1, x2 = xof(math.log10(b["r1"])), xof(math.log10(b["r2"]))
   g.add(Line([x1, y, 0], [x2, y, 0], color=DIM, stroke_width=1.6))
   g.add(Dot([x1, y, 0], radius=0.068, color=ACCENT_A), Dot([x2, y, 0], radius=0.068, color=ACCENT_C))
   g.add(self._sym(y, b["lab"], DIM, FS_TAG - 3, x=-5.72, w=0.46))
  g.add(self._legend(-5.84, ((ACCENT_A, "‖ f ‖ ₂  /  ‖ g ‖ ₂", 1.44),
                             (ACCENT_C, "√ m  ‖ f ′ ‖ ₂  /  ‖ g ‖ ₂", 1.86)),
                     y0=1.20, dy=0.24))
  g.add(self._table((("g   =   ( T − λ ) f", ACCENT_B),
                     ("‖ g ‖ ₂ ‖ f ‖ ₂   ≥   | ( g , f ) |   ≥   m ‖ f ′ ‖ ₂ ² + ‖ f ‖ ₂ ²", ACCENT_A),
                     ("      ‖ g ‖ ₂          ‖ f ‖ ₂          ‖ f ′ ‖ ₂", DIM),)
                    + tuple((f"  {b['lab']}    {b['ng']:8.3f}   {b['nf']:7.4f}   {b['nfp']:7.4f}",
                             ACCENT_B) for b in BND)
                    + ((f"√ m   =   {math.sqrt(MM):.2f}", DIM),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("每一列的紫點都在橘點右邊，兩個都在豎線左邊",
                  "in every row the purple dot is right of the orange one, and both are left of the line"))
  return g.add(self._foot("第一步：令 g 等於 T 減 λ 作用在 f 上。內積不超過兩個二範數相乘，配上引理的下界，先得到 f 的二範數不超過 g 的二範數",
                          "first step: let g be T minus lambda applied to f; the inner product is at most the product of the two norms, and with the lemma's lower bound that puts the two-norm of f under that of g",
                          ACCENT_A,
                          "再代回去一次，就得到導數的二範數不超過 g 的二範數除以根號 m。橫軸是這兩個比值，刻度是十倍一格；離豎線還很遠，但界住整個單位球的就是它",
                          "feeding that back bounds the derivative's two-norm by that of g over root m; the axis carries both ratios a decade per tick, and loose as they look it is this pair that holds the whole unit ball"))

 # ── beat 7: the Holder estimate and the square-root tube ────────
 def _holder(self):
  oy, sy = -0.02, 1.10
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12))
  for sgn in (1.0, -1.0):
   g.add(self._curve([[self._xof(A + 0.5 * k / 60.0, A, B),
                       oy + sgn * sy * math.sqrt(0.5 * k / 60.0) / math.sqrt(MM), 0]
                      for k in range(61)], DIM, sw=1.8))
   g.add(self._curve([[self._xof(A + 0.5 + 0.5 * k / 60.0, A, B),
                       oy + sgn * sy * math.sqrt(max(0.0, 0.5 - 0.5 * k / 60.0)) / math.sqrt(MM), 0]
                      for k in range(61)], DIM, sw=1.8))
  for h, col in zip(HOLD, (ACCENT_A, ACCENT_C)):
   g.add(self._plot(lambda t, F=h["fn"]: float(F(np.array([t]))[0]), col, A, B, oy, sy, sw=3.0))
  g.add(self._legend(-5.84, ((ACCENT_A, "f ₁", 0.40), (ACCENT_C, "f ₃", 0.40)), y0=1.15, dy=0.24))
  g.add(self._table((("| f ( y ) − f ( x ) |   ≤   ∫ | f ′ |   ≤   "
                      "‖ f ′ ‖ ₂ | y − x | ¹ ᐟ ²", ACCENT_A),
                     (f"‖ f ′ ‖ ₂   ≤   ‖ g ‖ ₂ / √ m   =   {HLIM:.2f}", ACCENT_B),
                     ("        max  | Δ f | / | Δ t | ¹ ᐟ ²           max | f |", DIM),)
                    + tuple((f"      {h['lab']}          {h['worst']:.4f}"
                             f"             {h['peak']:.4f}", ACCENT_C) for h in HOLD)
                    + ((f"‖ f ‖ ∞   ≤   C   =   {CSUP:.2f}          Ch 4 , 6.1", ACCENT_A),
                       (f"‖ f ′ ‖ ₂ / ‖ g ‖ ₂   ≤   {max(b['r2'] for b in BND):.3f}", DIM)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("灰線是根號型的套管，兩條曲線整條都關在裡面",
                  "the grey curves are the square-root tube, and both functions are held inside it"))
  return g.add(self._foot("第二步：導數被界住，積分的 Schwarz 不等式就給出 Hölder 型的估計，兩點的函數值之差不超過導數的二範數乘上距離的平方根",
                          "second step: with the derivative bounded, the Schwarz inequality for integrals gives a Holder type estimate, the gap between two values at most the derivative's two-norm times the root of the distance",
                          ACCENT_A,
                          "圖上兩條的導數二範數都剛好是一，也就是單位球容許的極端情形。像集一致等度連續又有界，第四章的定理給出全有界，閉包緊，所以右逆是緊算子",
                          "both curves have derivative two-norm exactly one, the extreme the unit ball allows; the image is uniformly equicontinuous and bounded, chapter four makes it totally bounded, so the inverse is compact"))

 # ── beat 8: the eigenvalues, before and after ───────────────────
 def _eigen(self):
  rlo, rhi = -0.40, 0.05
  # 下限由資料決定：寫死 -28 會把最後一個特徵值映到畫面外
  mlo = min(e["mu"] for e in EIG) - 2.0
  mhi = 3.0
  xr_ = lambda v: XL + (v - rlo) / (rhi - rlo) * (XR - XL)
  xm_ = lambda v: XL + (v - mlo) / (mhi - mlo) * (XR - XL)
  ytop, ybot = 0.62, -0.52
  g = VGroup(self._arr([XL - 0.10, ytop, 0], [XR + 0.10, ytop, 0], DIM, sw=3, tl=0.12),
             self._arr([XL - 0.10, ybot, 0], [XR + 0.10, ybot, 0], DIM, sw=3, tl=0.12))
  for e in EIG:
   g.add(Dot([xr_(e["r"]), ytop, 0], radius=0.062, color=ACCENT_B))
   g.add(Dot([xm_(e["mu"]), ybot, 0], radius=0.062, color=ACCENT_A))
  for e in EIG[:3]:
   g.add(self._sym(ytop + 0.22, f"{e['n']}", ACCENT_B, FS_TAG - 4, x=xr_(e["r"]), w=0.26))
   g.add(self._sym(ybot - 0.22, f"{e['n']}", ACCENT_A, FS_TAG - 4, x=xm_(e["mu"]), w=0.26))
  for e, col in ((EIG[0], ACCENT_C), (EIG[2], DIM)):
   g.add(self._arr([xr_(e["r"]), ytop - 0.10, 0], [xm_(e["mu"]), ybot + 0.10, 0],
                   col, sw=2.4, tl=0.12))
  g.add(self._sym(ytop + 0.44, "r ₙ", ACCENT_B, FS_TAG - 2, x=XL + 0.14, w=0.44))
  g.add(self._sym(ybot - 0.46, "μ ₙ", ACCENT_A, FS_TAG - 2, x=XL + 0.14, w=0.44))
  g.add(self._sym(ytop + 0.22, "0", DIM, FS_TAG - 4, x=xr_(0.0), w=0.26))
  g.add(self._table((("S φ ₙ  =  r ₙ φ ₙ      ⇒      T φ ₙ  =  ( ( 1 + λ r ₙ ) / r ₙ ) φ ₙ", ACCENT_A),
                     (f"T  =  D ²  ,  [ 0 , π ]  ,  λ  =  {LAM:.0f}", DIM),
                     ("      n            r ₙ            ( 1 + λ r ₙ ) / r ₙ", DIM),)
                    + tuple((f"      {e['n']}      {e['r']:+.5f}        {e['back']:+.4f}",
                             ACCENT_B) for e in EIG[:4])
                    + ((f"| r ₆ |   =   {abs(EIG[-1]['r']):.5f}      →      0", ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("上排往右擠成一堆，下排往左散開，順序整個反過來",
                  "the upper row crowds to the right, the lower spreads left, and the order reverses"))
  return g.add(self._foot("定理 6.2：M 有一組完全由 T 的特徵向量構成的正交規範基底。把第五章的定理用在右逆上得到它的特徵基底，再翻譯回 T",
                          "Theorem 6.2: there is an orthonormal basis made entirely of eigenvectors of T, got by applying the chapter five theorem to the right inverse",
                          ACCENT_A,
                          "再把特徵值翻譯回去：右逆把 φ 乘上 r，T 就把 φ 乘上一加 λ r 再除以 r。右逆的特徵值聚集到零，T 的特徵值就跑向負無窮",
                          "then translate the eigenvalues back: if the inverse scales phi by r then T scales it by one plus lambda r over r, so eigenvalues piling up at zero become ones running to minus infinity"))

 # ── beat 9: the two norms of the error ──────────────────────────
 def _uniform(self):
  oy, sy = 0.0, 1.00 / FOUR[0]["tail"]
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12))
  for d, col in ((FOUR[0], ACCENT_A), (FOUR[1], ACCENT_C)):
   for sgn in (1.0, -1.0):
    g.add(self._dash([XL, oy + sgn * sy * d["tail"], 0], [XR, oy + sgn * sy * d["tail"], 0],
                     col, n=24, sw=1.5))
   xs, es = d["err"]
   g.add(self._curve([[self._xof(x, 0.0, PI), oy + sy * e, 0]
                      for x, e in zip(xs[::20], es[::20])], col, sw=3.0))
  g.add(self._legend(-5.84, ((ACCENT_A, "N  =  1", 0.84), (ACCENT_C, "N  =  3", 0.84)),
                     y0=-0.70, dy=0.20))
  g.add(self._table((("f ( x )  =  x ( π − x )        b ₙ  =  8 / ( π n ³ )      ( n  =  1 , 3 , 5 , … )", ACCENT_A),
                     ("      N        ‖ f − S ₙ ‖ ∞        ‖ f − S ₙ ‖ ₂        Σ | b ₙ |", DIM),)
                    + tuple((f"      {d['N']}        {d['sup']:.2e}        {d['two']:.2e}"
                             f"        {d['tail']:.2e}", ACCENT_B) for d in FOUR)
                    + ((f"‖ · ‖ ₂   ≤   √ π  ‖ · ‖ ∞          √ π  =  {math.sqrt(PI):.4f}",
                        ACCENT_C),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("每條誤差曲線都關在它自己那對虛線裡",
                  "each error curve is shut inside its own pair of dashed lines"))
  return g.add(self._foot("引理 6.5：如果算子從一個範數映到另一個壓得住它的範數是緊的，那麼展開式在兩個範數底下都收斂",
                          "Lemma 6.5: if an operator is compact from one norm into a second norm that dominates it, then the expansion converges in both norms",
                          ACCENT_A,
                          "一致範數壓得住二範數，所以子空間裡的 f 的展開式不只是平方平均收斂，它是一致收斂。虛線是係數尾巴，誤差一定關在裡面",
                          "the uniform norm dominates the two-norm, so the expansion of an f in the subspace is not merely a mean square limit but a uniform one; the dashed lines are the coefficient tails that trap it"))

 # ── beat 10: the example section 6 ends on ──────────────────────
 def _example(self):
  oy, sy = -0.10, 0.68
  g = VGroup(self._arr([XL - 0.10, oy, 0], [XR + 0.05, oy, 0], DIM, sw=3, tl=0.12))
  for k, col in zip((1, 2, 3), (ACCENT_A, ACCENT_C, ACCENT_B)):
   g.add(self._plot(lambda x, k=k: math.sin(k * x), col, 0.0, PI, oy, sy, sw=3.0))
  g.add(self._sym(-0.98, "0", DIM, FS_TAG - 3, x=XL, w=0.26),
        self._sym(-0.98, "π", DIM, FS_TAG - 3, x=XR, w=0.26))
  g.add(self._legend(-5.84, ((ACCENT_A, "sin x", 0.72), (ACCENT_C, "sin 2 x", 0.98),
                             (ACCENT_B, "sin 3 x", 0.98)), y0=1.16, dy=0.22))
  g.add(self._table((("T  =  D ²        f ( 0 )  =  f ( π )  =  0", ACCENT_A),
                     ("φ ₙ  =  sin n x          μ ₙ  =  − n ²", ACCENT_B),
                     ("      ( φ ₙ , φ ₘ )      m = 1      m = 2      m = 3", DIM),)
                    + tuple((f"      n = {i + 1}    " + "  ".join(f"{ORTH[i][j]:+.4f}"
                                                                  for j in range(3)), ACCENT_C)
                            for i in range(3))
                    + ((f"π / 2   =   {PI / 2:.4f}            6.1  −  6.12", DIM),),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("對角線上是 π 的一半，其他格子是零",
                  "the diagonal carries half of pi and every other cell is zero"))
  return g.add(self._foot("收個尾。最簡單的例子是二次微分算子配上兩端為零，特徵值是負的 n 平方，特徵函數是正弦，彼此正交",
                          "to close: the simplest example is the second derivative with both ends held at zero, eigenvalues minus n squared and the sines as eigenfunctions, orthogonal to one another",
                          ACCENT_A,
                          "第 6 節到這裡結束，後面接的是十二道習題。下一集就把這個例子從頭到尾完整走一遍",
                          "section 6 ends here and twelve exercises follow; next episode walks this one example through from start to finish"))

 def stage(self):
  a, b, c = self._route(), self._lemma(), self._parts()
  d, e, f_ = self._complement(), self._regular(), self._thm61()
  h, i, j = self._bounds(), self._holder(), self._eigen()
  k, l = self._uniform(), self._example()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE83ZH, AdvCalcE83EN = make(AdvCalcE83Base, "83", prefix="AdvCalcE")
