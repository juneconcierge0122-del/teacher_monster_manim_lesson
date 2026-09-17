"""advcalc E78 -- chapter 6, section 3 (book pp. 278-280): the explicit right
inverse, the constant coefficient equation, and Theorem 3.4.

E77 showed that S has a right inverse determined by the complement M_0; this
episode writes it down.  The move is to notice that the left side of
f' - T_t(f) = g is a total derivative in disguise: since K' = T_t . K, the
operator is K' . K^-1, and the product rule turns the whole left side into
K(t) d/dt[K(t)^-1 f(t)].  Integrating gives Theorem 3.3.

Then the constant coefficient case, which the book calls extremely important.
Two small lemmas set it up -- the solution space is invariant under D (3.1), and
evaluation carries D on that space to T on W (3.2) -- and the equation for the
fundamental solution becomes the one elementary calculus answers with an
exponential, so K_t = e^{tT}.  In finite dimensions a polynomial annihilates T,
the space splits into the null spaces of (T - lambda_i)^{m_i}, and on each piece
the infinite series collapses to m terms because T - lambda is nilpotent there.
Theorem 3.4 assembles it: every solution is a finite sum of t^j e^{t lambda_i}
times constant vectors, with as many terms as the degree of the polynomial.

The last beat is the asymptotic criterion, and it is the one place in the
section where the answer is a clean dichotomy: the solution curves are bounded
on the whole of R if and only if every root is pure imaginary with multiplicity
one.  All four cases are computed here -- decay, blow-up, a bounded rotation,
and the pure-imaginary-but-repeated case whose norm grows like t.
"""
import cmath
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
TAU = math.tau


def mv(M, v):
 return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def mm(A, B):
 return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def sm(c, M):
 return [[c * M[i][j] for j in range(2)] for i in range(2)]


def inv(M):
 d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
 return [[M[1][1] / d, -M[0][1] / d], [-M[1][0] / d, M[0][0] / d]]


# ── beats 0 to 3: theorem 3.3, on E77's time-dependent example ────────
J = [[0.0, -1.0], [1.0, 0.0]]


def T_t(t):
 return sm(1.0 + t, J)


def K(t):
 th = t + 0.5 * t * t
 c, s = math.cos(th), math.sin(th)
 return [[c, -s], [s, c]]


def g_src(t):
 return (1.0, 0.4 * math.cos(2.0 * t))


def simpson_vec(fn, a, b, n=240):
 h = (b - a) / n
 out = []
 for i in range(2):
  s = fn(a)[i] + fn(b)[i]
  for k in range(1, n):
   s += (4 if k % 2 else 2) * fn(a + k * h)[i]
  out.append(s * h / 3)
 return tuple(out)


def f33(t):
 """Theorem 3.3's formula, evaluated."""
 if abs(t) < 1e-12:
  return (0.0, 0.0)
 return mv(K(t), simpson_vec(lambda s: mv(inv(K(s)), g_src(s)), 0.0, t))


assert max(abs(f33(0.0)[i]) for i in range(2)) < 1e-12, "it starts at zero, as claimed"
T33 = []
for _t in (0.4, 0.9, 1.4, 1.9):
 _h = 1e-5
 _d = tuple((f33(_t + _h)[i] - f33(_t - _h)[i]) / (2 * _h) for i in range(2))
 _lhs = tuple(_d[i] - mv(T_t(_t), f33(_t))[i] for i in range(2))
 T33.append((_t, _lhs[0], _lhs[1], g_src(_t)[0], g_src(_t)[1]))
assert all(abs(a - c) < 3e-4 and abs(b - d) < 3e-4 for _t, a, b, c, d in T33), \
    "and S applied to it returns g, which is what makes it a right inverse"

# the identity the derivation turns on: K' . K^-1 is T_t
for _t in (0.3, 1.0, 1.7):
 _h = 1e-6
 _dk = [[(K(_t + _h)[i][j] - K(_t - _h)[i][j]) / (2 * _h) for j in range(2)] for i in range(2)]
 _p = mm(_dk, inv(K(_t)))
 assert max(abs(_p[i][j] - T_t(_t)[i][j]) for i in range(2) for j in range(2)) < 1e-6

# ── beats 4 and 5: the two lemmas, on a constant coefficient example ──
TC = [[-0.5, 1.0], [0.0, -0.5]]
LAM, MULT = -0.5, 2
R_NIL = [[TC[i][j] - (LAM if i == j else 0.0) for j in range(2)] for i in range(2)]
assert max(abs(mm(R_NIL, R_NIL)[i][j]) for i in range(2) for j in range(2)) < 1e-15, \
    "R is nilpotent of index 2, so the exponential series stops after two terms"


def expm(M, n=60):
 acc = [[1.0, 0.0], [0.0, 1.0]]
 term = [[1.0, 0.0], [0.0, 1.0]]
 for k in range(1, n):
  term = sm(1.0 / k, mm(term, M))
  acc = [[acc[i][j] + term[i][j] for j in range(2)] for i in range(2)]
 return acc


BETA = (0.0, 1.0)


def f_series(t):
 return mv(expm(sm(t, TC)), BETA)


def f_closed(t):
 """Theorem 3.4's form: e^{t lambda} (beta + t R beta), two terms only."""
 rb = mv(R_NIL, BETA)
 return (math.exp(LAM * t) * (BETA[0] + t * rb[0]),
         math.exp(LAM * t) * (BETA[1] + t * rb[1]))


CLOSED = []
for _t in (0.0, 1.0, 2.5, 5.0, 8.0):
 _a, _b = f_series(_t), f_closed(_t)
 CLOSED.append((_t, _a[0], _b[0], max(abs(_a[i] - _b[i]) for i in range(2))))
assert all(e < 1e-12 for _t, _x, _y, e in CLOSED), \
    "the infinite series and the two-term closed form agree to machine precision"
# and it really solves the equation
for _t in (0.5, 2.0, 4.0):
 _h = 1e-6
 _d = tuple((f_closed(_t + _h)[i] - f_closed(_t - _h)[i]) / (2 * _h) for i in range(2))
 _r = mv(TC, f_closed(_t))
 assert max(abs(_d[i] - _r[i]) for i in range(2)) < 1e-6

# lemma 3.1: the derivative of a solution is again a solution
for _t in (0.4, 1.6, 3.0):
 _h = 1e-5
 _fp = tuple((f_closed(_t + _h)[i] - f_closed(_t - _h)[i]) / (2 * _h) for i in range(2))
 _fpp = tuple((f_closed(_t + _h)[i] - 2 * f_closed(_t)[i] + f_closed(_t - _h)[i]) / (_h * _h)
              for i in range(2))
 _r = mv(TC, _fp)
 assert max(abs(_fpp[i] - _r[i]) for i in range(2)) < 1e-3, \
     "f'' = T f', so the derivative is a solution too"

# ── beat 10: the asymptotic dichotomy, all four cases ─────────────────
OM = 1.4
CASES = []
for lab, root, m in (("a", complex(0.30, 0.0), 1), ("b", complex(-0.50, 0.0), 1),
                     ("c", complex(0.0, OM), 1), ("d", complex(0.0, OM), 2)):
 row = []
 for t in (0.0, 5.0, 10.0, 20.0):
  if m == 1:
   v = cmath.exp(root * t)
  else:
   v = cmath.exp(root * t) * complex(t, 1.0)
  row.append(abs(v))
 CASES.append((lab, root, m, row))
_a, _b, _c, _d = (r for _l, _r, _m, r in CASES)
assert _a[-1] > 100 * _a[0], "positive real part blows up"
assert _b[-1] < 1e-3 * _b[0], "negative real part decays"
assert all(abs(x - 1.0) < 1e-12 for x in _c), "pure imaginary and simple stays bounded"
assert _d[-1] > 15 * _d[0], "pure imaginary but repeated grows like t"
BOUNDED = [lab for lab, root, m, row in CASES if abs(root.real) < 1e-15 and m == 1]
assert BOUNDED == ["c"], "exactly one of the four is bounded on the whole line"


class AdvCalcE78Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 78

 MODE_LABEL = {
  0: {"zh": "回到非齊次方程", "en": "back to the inhomogeneous equation"},
  1: {"zh": "左邊其實是一個全微分", "en": "the left side is a total derivative"},
  2: {"zh": "於是可以直接積分", "en": "so it can be integrated directly"},
  3: {"zh": "定理 3.3：右反元素的公式", "en": "theorem 3.3: the right inverse"},
  4: {"zh": "常係數：引理 3.1", "en": "constant coefficients: lemma 3.1"},
  5: {"zh": "引理 3.2：D 與 T 是同一個算子", "en": "lemma 3.2: D and T are one operator"},
  6: {"zh": "K ₜ  =  exp ( t T )", "en": "the fundamental solution is an exponential"},
  7: {"zh": "有限維：W 拆成零化空間", "en": "finite dimensions: W splits"},
  8: {"zh": "無窮級數變成有限和", "en": "the series becomes a finite sum"},
  9: {"zh": "定理 3.4", "en": "theorem 3.4"},
  10: {"zh": "漸近行為，與第 3 節的結束", "en": "the asymptotics, and the end of section 3"},
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

 def _frame(self, ox, oy, w, h, down=0.30, back=0.12):
  return VGroup(Line([ox - back, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=1.0, sw=2.4, n=140):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _legend(self, x, rows, y0=1.14, dy=0.27):
  g = VGroup()
  for k, (col, lab, w) in enumerate(rows):
   y = y0 - k * dy
   g.add(Line([x, y, 0], [x + 0.24, y, 0], color=col, stroke_width=6.0),
         self._sym(y, lab, col, FS_TAG - 3, x=x + 0.46 + w / 2, w=w))
  return g

 # ── beat 0: what is to be solved, and the identity to use ────────
 def _target(self):
  ox, oy, sx, sy = -5.90, -0.36, 1.58, 0.44
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: g_src(t)[0], ACCENT_B, t0=0.0, t1=2.0, sw=2.8))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: g_src(t)[1], ACCENT_C, t0=0.0, t1=2.0, sw=2.8))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "g ¹", 0.56), (ACCENT_C, "g ²", 0.56)), y0=1.14))
  g.add(self._table((("f ′ ( t )  −  T ₜ ( f ( t ) )   =   g ( t )", ACCENT_A),
                     ("K ′ ( t )   =   T ₜ  ∘  K ( t )", ACCENT_B),
                     ("T ₜ   =   K ′ ( t )  ∘  K ( t ) ⁻ ¹", ACCENT_A),
                     ("f ( 0 )   =   0", ACCENT_C)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("第三列是把第二列解出來，僅此而已",
                  "the third row is the second one solved for the operator, nothing more"))
  return g.add(self._foot("上一集證了右反元素存在，這一集要把它寫出來。要解的是 f ′ 減去 T ₜ 作用在 f 上等於 g，初始值為零",
                          "last episode proved the right inverse exists; this one writes it down, solving the equation with a prescribed g and zero initial value",
                          ACCENT_A,
                          "手上唯一的新工具是基本解自己的方程 K ′ = T ₜ ∘ K。把它解出 T ₜ，代回去之後左邊會變成一個認得出來的東西",
                          "the only new tool is the fundamental solution's own equation; solving it for the operator and substituting turns the left side into something recognisable"))

 # ── beat 1: the left side is a total derivative ──────────────────
 def _total(self):
  oy = 0.26
  g = VGroup()
  for x0, lab, col, w_ in ((-5.30, "f", ACCENT_B, 0.66), (-3.55, "K ⁻ ¹ f", ACCENT_C, 1.30),
                           (-1.60, "d / d t", ACCENT_A, 1.30)):
   g.add(self._box(x0, oy, lab, col, w=w_, h=0.60, size=FS_TAG + 1))
  for a, b in ((-4.97, -4.20), (-2.90, -2.25)):
   g.add(self._arr([a, oy, 0], [b, oy, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.50, "K ⁻ ¹", ACCENT_C, FS_TAG - 3, x=-4.58, w=0.90),
        self._sym(oy + 0.50, "D", ACCENT_A, FS_TAG - 3, x=-2.58, w=0.50))
  g.add(self._arr([-1.60, oy - 0.42, 0], [-1.60, oy - 0.86, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(oy - 1.06, "K ( t )  ·  ( … )", ACCENT_A, FS_TAG - 2, x=-1.60, w=2.00))
  g.add(self._table((("Ch 4  ,  8.12          Ch 3  ,  8.4", DIM),
                     ("f ′ − T ₜ f", ACCENT_B),
                     ("=   K ( t )   d / d t [ K ( t ) ⁻ ¹ ( f ( t ) ) ]", ACCENT_A),
                     ("K ′ K ⁻ ¹  +  K ( K ⁻ ¹ ) ′   =   0", ACCENT_C)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("最後一列是乘法法則，整個等式就靠它",
                  "the last row is the product rule, and the identity rests on it"))
  return g.add(self._foot("由第 4 章習題 8.12 與第 3 章的乘法法則（定理 8.4），f ′ − T ₜ f 正好等於 K ( t ) 乘上 K ( t ) ⁻ ¹ ( f ( t ) ) 對 t 的導數",
                          "by Exercise 8.12 of chapter 4 and chapter 3's product rule, the left side is exactly K at t times the derivative of K inverse applied to f",
                          ACCENT_A,
                          "這就是整個公式的關鍵：一個看起來要解的微分方程，其實左邊已經是某個東西的全微分——只要先用 K ⁻ ¹ 換個座標",
                          "that is the whole formula: what looks like an equation to be solved already has a total derivative on the left, once K inverse is used to change coordinates"))

 # ── beat 2: integrate ────────────────────────────────────────────
 def _integrate(self):
  ox, oy, sx, sy = -5.90, -0.40, 1.58, 0.46
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: mv(inv(K(t)), g_src(t))[0], ACCENT_B,
                     t0=0.0, t1=2.0, sw=2.8))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: mv(inv(K(t)), g_src(t))[1], ACCENT_C,
                     t0=0.0, t1=2.0, sw=2.8))
  n = 44
  for k in range(n):
   s0 = 2.0 * k / n
   g.add(Line([ox + sx * s0, oy, 0],
              [ox + sx * s0, oy + sy * mv(inv(K(s0)), g_src(s0))[0], 0],
              color=ACCENT_B, stroke_width=1.2))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "( K ⁻ ¹ g ) ¹", 1.50),
                                 (ACCENT_C, "( K ⁻ ¹ g ) ²", 1.50)), y0=1.14))
  g.add(self._table((("d / d t [ K ( t ) ⁻ ¹ ( f ( t ) ) ]   =   K ( t ) ⁻ ¹ ( g ( t ) )", ACCENT_A),
                     ("K ( t ) ⁻ ¹ ( f ( t ) )   =   ∫ K ( s ) ⁻ ¹ ( g ( s ) ) d s", ACCENT_B),
                     ("( s  :  0 → t )", DIM),
                     ("f ( t )   =   K ₜ [ ∫ … ]", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("網底就是第二列那個積分",
                  "the hatching is the integral in the second row"))
  return g.add(self._foot("方程於是變成可以直接積分的形式：K ⁻ ¹ f 對 t 的導數等於 K ⁻ ¹ g。兩邊從 0 積到 t，再把 K ₜ 乘回去",
                          "the equation becomes one to integrate directly: the derivative of K inverse applied to f equals K inverse applied to g; integrate from zero to t and multiply K back on",
                          ACCENT_A,
                          "被積的是把 g 先用 K ⁻ ¹ 拉回時刻零那一格再累加。書上說即使覺得推導太技術，也可以把答案直接微分驗一次",
                          "what is integrated is g pulled back to time zero by K inverse; the book adds that even if the derivation feels technical, the answer can simply be differentiated to check"))

 # ── beat 3: theorem 3.3, checked ─────────────────────────────────
 def _thm33(self):
  ox, oy, sx, sy = -5.90, -0.44, 1.58, 0.40
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f33(t)[0], ACCENT_A, t0=0.0, t1=2.0, sw=3.0, n=90))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f33(t)[1], ACCENT_C, t0=0.0, t1=2.0, sw=3.0, n=90))
  g.add(Dot([ox, oy, 0], radius=0.056, color=ACCENT_A))
  g.add(self._legend(ox + 0.06, ((ACCENT_A, "f ¹", 0.56), (ACCENT_C, "f ²", 0.56)), y0=1.14))
  g.add(self._table((("f ( t )  =  K ₜ [ ∫ K ₛ ⁻ ¹ ( g ( s ) ) d s ]", ACCENT_A),
                     ("        t          ( S f ) ( t )              g ( t )", DIM),)
                    + tuple((f"      {t:.1f}     ( {a:+.4f} , {b:+.4f} )   ( {c:+.4f} , {d:+.4f} )",
                             ACCENT_B) for t, a, b, c, d in T33)
                    + (("R   =   S ⁻ ¹  ↾  M ₀", ACCENT_A),),
                    y0=0.92, dy=0.25, size=FS_TAG - 4))
  g.add(self._cap("中間兩欄逐列相同，這就是驗證",
                  "the two middle columns agree row by row, and that is the check"))
  return g.add(self._foot("定理 3.3：f ( t ) = K ₜ 作用在 ∫ K ₛ ⁻ ¹ ( g ( s ) ) d s 上，就是初始值為零的非齊次問題的解",
                          "theorem 3.3: K at t applied to the integral of K inverse applied to g is the solution of the inhomogeneous problem with zero initial value",
                          ACCENT_A,
                          "這正是上一集那個右反元素 R 的顯式公式，由補空間 M ₀ 決定。表上是把答案代回 S 算出來的，與 g 逐列相同",
                          "that is the explicit formula for last episode's right inverse, the one determined by the complement; the table applies S to the answer and gets g back row by row"))

 # ── beat 4: lemma 3.1 ────────────────────────────────────────────
 def _lemma31(self):
  ox, oy, sx, sy = -5.90, -0.30, 0.38, 0.52
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_closed(t)[0], ACCENT_A, t0=0.0, t1=8.4, sw=3.0))
  h = 1e-5
  g.add(self._fcurve(ox, oy, sx, sy,
                     lambda t: (f_closed(t + h)[0] - f_closed(t - h)[0]) / (2 * h),
                     ACCENT_C, t0=0.0, t1=8.4, sw=2.6))
  g.add(self._legend(ox + 0.06, ((ACCENT_A, "f ¹", 0.56), (ACCENT_C, "( f ′ ) ¹", 1.00)), y0=1.14))
  g.add(self._table((("f ′ ( t )   =   T ( f ( t ) )", ACCENT_A),
                     ("f ″ ( t )   =   T ( f ′ ( t ) )", ACCENT_C),
                     ("f  ∈  N       ⇒       f ′  ∈  N", ACCENT_A),
                     ("D [ N ]   ⊂   N", ACCENT_B),
                     ("T   =   [ [ − 0.5 , 1 ] , [ 0 , − 0.5 ] ]", DIM)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("兩條都是解，所以兩條都畫得出來",
                  "both curves are solutions, which is why both can be drawn"))
  return g.add(self._foot("常係數時 T ₜ 是固定的 T。第一個新事實：f 是解則 f ′ 也是解——方程右邊可微，兩邊再微分一次就得到 f ″ = T ( f ′ )",
                          "with constant coefficients the operator is fixed, and the first new fact is that the derivative of a solution is again a solution, since differentiating both sides again gives its equation",
                          ACCENT_A,
                          "這就是引理 3.1：解空間 N 在導數算子 D 底下不變。非常係數時這句話不成立，因為那時右邊還帶著 t",
                          "that is Lemma 3.1: the solution space is invariant under differentiation; it fails for variable coefficients, where the right side still carries a t"))

 # ── beat 5: lemma 3.2 ────────────────────────────────────────────
 def _lemma32(self):
  oy = 0.24
  g = VGroup()
  for x0, yy, lab, col in ((-5.20, oy + 0.42, "N", ACCENT_C), (-2.30, oy + 0.42, "N", ACCENT_C),
                           (-5.20, oy - 0.70, "W", ACCENT_B), (-2.30, oy - 0.70, "W", ACCENT_B)):
   g.add(self._box(x0, yy, lab, col, w=0.72, h=0.56, size=FS_TAG + 3))
  g.add(self._arr([-4.80, oy + 0.42, 0], [-2.72, oy + 0.42, 0], ACCENT_A, sw=3, tl=0.14),
        self._arr([-4.80, oy - 0.70, 0], [-2.72, oy - 0.70, 0], ACCENT_A, sw=3, tl=0.14),
        self._arr([-5.20, oy + 0.10, 0], [-5.20, oy - 0.38, 0], DIM, sw=3, tl=0.13),
        self._arr([-2.30, oy + 0.10, 0], [-2.30, oy - 0.38, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.68, "D", ACCENT_A, FS_TAG, x=-3.76, w=0.50),
        self._sym(oy - 0.46, "T", ACCENT_A, FS_TAG, x=-3.76, w=0.50),
        self._sym(oy - 0.14, "φ ₜ", DIM, FS_TAG - 2, x=-5.62, w=0.60),
        self._sym(oy - 0.14, "φ ₜ", DIM, FS_TAG - 2, x=-1.88, w=0.60))
  g.add(self._table((("π ₜ  ∘  D   =   T  ∘  π ₜ", ACCENT_A),
                     ("φ ₜ   =   π ₜ ↾ N     :     N   ≅   W", ACCENT_C),
                     ("T   =   φ ₜ  ∘  D  ∘  φ ₜ ⁻ ¹", ACCENT_A),
                     ("D  ↾  N          ≅          T", ACCENT_B)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("方塊圖交換，這就是引理 3.2 的全部內容",
                  "the square commutes, and that is all Lemma 3.2 says"))
  return g.add(self._foot("把方程寫成 π ₜ ∘ D = T ∘ π ₜ，而 φ ₜ = π ₜ ↾ N 是同構，就能解出 T = φ ₜ ∘ D ∘ φ ₜ ⁻ ¹",
                          "write the equation as evaluation composed with D equals T composed with evaluation; since evaluation restricted to the solution space is an isomorphism, solve for T",
                          ACCENT_A,
                          "引理 3.2 說的是：微分算子 D 在解空間上的樣子，與 T 在 W 上的樣子，是同一個算子的兩張臉。這解釋了為什麼下一拍指數會出現",
                          "Lemma 3.2 says that differentiation on the solution space and T on W are two faces of one operator, which is why an exponential appears in the next beat"))

 # ── beat 6: the exponential ──────────────────────────────────────
 def _expo(self):
  # a short window on purpose: the two-term sum leaves the frame by t = 4
  ox, oy, sx, sy = -5.90, -0.44, 1.05, 0.40
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  for nterm, col in ((2, DIM), (4, ACCENT_C), (8, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy,
                      lambda t, n=nterm: mv(expm(sm(t, TC), n), BETA)[0], col,
                      t0=0.0, t1=3.0, sw=2.0))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_closed(t)[0], ACCENT_A, t0=0.0, t1=3.0, sw=3.2))
  g.add(self._legend(ox + 0.06, ((DIM, "2", 0.40), (ACCENT_C, "4", 0.40),
                                 (WARN, "8", 0.40)), y0=1.14, dy=0.25))
  g.add(self._table((("d S / d t   =   T  S           S ( 0 )  =  I", ACCENT_B),
                     ("K ₜ   =   exp ( t T )", ACCENT_A),
                     ("exp ( t T ) β   =   Σ ₀  t ʲ  T ʲ ( β )  /  j !", ACCENT_A),
                     ("Σ ₀ ⁶ ⁰   −   exp ( t λ ) [ β + t R β ]", DIM),
                     (f"                    {CLOSED[3][3]:.2e}", ACCENT_B)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("截到 2、4、8 項的曲線一條比一條貼近橘線",
                  "truncating at two, four and eight terms closes in on the orange curve"))
  return g.add(self._foot("基本解的方程現在是 d S / d t = T S、S ( 0 ) = I。在初等微積分裡這正是指數函數的方程，所以 K ₜ = exp ( t T )",
                          "the equation for the fundamental solution is now the one elementary calculus answers with the exponential, so K at t is the exponential of t times T",
                          ACCENT_A,
                          "通過 ⟨ 0 , β ⟩ 的解就是那個級數。圖上灰、紫、紅是截到 2、4、8 項的部分和，橘線是真正的解",
                          "the solution through a vector is that series; the grey, purple and red curves are the partial sums at two, four and eight terms, and the orange one is the solution"))

 # ── beat 7: the space splits ─────────────────────────────────────
 def _splitW(self):
  oy = 0.22
  g = VGroup()
  g.add(self._box(-5.20, oy, "W", ACCENT_A, w=0.86, h=0.62, size=FS_TAG + 3))
  for k, (x0, lab, col) in enumerate(((-3.20, "W ₁", ACCENT_B), (-1.80, "W ₂", ACCENT_C),
                                      (-0.40, "W ₃", WARN))):
   g.add(self._box(x0, oy, lab, col, w=0.80, h=0.62, size=FS_TAG + 2))
   g.add(self._sym(oy - 0.62, f"( T − λ {'₁₂₃'[k]} ) ᵐ", col, FS_TAG - 4, x=x0, w=1.40))
  g.add(self._arr([-4.70, oy, 0], [-3.70, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._sym(oy + 0.52, "⊕", DIM, FS_TAG, x=-2.50, w=0.44),
        self._sym(oy + 0.52, "⊕", DIM, FS_TAG, x=-1.10, w=0.44))
  g.add(self._table((("p ( T )   =   0", ACCENT_A),
                     ("p ( x )   =   ∏ ₁ ᵏ  ( x − λ ᵢ ) ᵐ ⁱ", ACCENT_A),
                     ("W   =   ⊕ ₁ ᵏ  W ᵢ            Ch 1  ,  5.5", ACCENT_B),
                     ("T [ W ᵢ ]   ⊂   W ᵢ", ACCENT_C)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("每一塊在 T 底下不變，所以可以一塊一塊算",
                  "each piece is invariant under T, so they can be handled one at a time"))
  return g.add(self._foot("有限維時 T 一定滿足某個多項式方程。把 p 分解成互質的因式，第 1 章定理 5.5 就把 W 拆成各個零化空間的直和",
                          "in finite dimensions T satisfies a polynomial equation; factoring it into relatively prime powers, chapter 1's Theorem 5.5 splits W into the direct sum of the null spaces",
                          ACCENT_A,
                          "而且每一塊在 T 底下不變，所以指數作用在整個 W 上這件事，可以拆成在每一塊上分別算再加起來",
                          "and each piece is invariant under T, so the exponential acting on all of W can be computed piece by piece and added up"))

 # ── beat 8: the series collapses ─────────────────────────────────
 def _finite(self):
  ox, oy, sx, sy = -5.90, -0.52, 0.38, 0.48
  g = VGroup(self._frame(ox, oy, 3.40, 1.46, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: math.exp(LAM * t), ACCENT_C,
                     t0=0.0, t1=8.4, sw=2.4))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: math.exp(LAM * t) * t, WARN,
                     t0=0.0, t1=8.4, sw=2.4))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: abs(f_closed(t)[0]) + abs(f_closed(t)[1]),
                     ACCENT_A, t0=0.0, t1=8.4, sw=3.0))
  g.add(self._legend(ox + 0.06, ((ACCENT_C, "exp ( t λ )", 1.30),
                                 (WARN, "t  exp ( t λ )", 1.50)), y0=1.14))
  g.add(self._table((("( T − λ ) ᵐ   =   0           R   =   T − λ I", ACCENT_A),
                     ("R ᵐ   =   0                      m  =  2", ACCENT_B),
                     ("exp ( t T )  =  exp ( t λ )  exp ( t R )", ACCENT_A),
                     ("exp ( t R )   =   I  +  t R", ACCENT_C),
                     ("Σ ₀ ⁶ ⁰      ⟶      2", WARN)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("無窮多項的和，在這裡只剩兩項",
                  "an infinite sum, and here only two terms survive"))
  return g.add(self._foot("在一塊 W ᵢ 上 ( T − λ ) ᵐ = 0，所以 T = λ I + R 而 R 冪零。指數分解成 exp ( t λ ) 乘 exp ( t R )，而後者的級數只有 m 項",
                          "on one piece the operator minus lambda is nilpotent, so the exponential factors into the scalar exponential times that of the nilpotent part, whose series has only m terms",
                          ACCENT_A,
                          "無窮級數突然變成有限和，項數正好是那個因式的重數。橘線是這個例子的解的長度，它是 exp ( t λ ) 與 t exp ( t λ ) 兩條的組合",
                          "the infinite series becomes a finite sum with as many terms as the multiplicity; the orange curve is this example's solution size, a combination of the two curves beneath it"))

 # ── beat 9: theorem 3.4, with the two forms agreeing ─────────────
 def _thm34(self):
  ox, oy, sx, sy = -5.90, -0.48, 0.38, 0.46
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_series(t)[0], ACCENT_B,
                     t0=0.0, t1=8.4, sw=5.0))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_closed(t)[0], ACCENT_A,
                     t0=0.0, t1=8.4, sw=2.2))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "Σ ₀ ⁶ ⁰", 1.00),
                                 (ACCENT_A, "exp ( t λ ) [ β + t R β ]", 2.40)), y0=1.14))
  g.add(self._table((("f ( t )   =   Σ ᵢ ⱼ   t ʲ  exp ( t λ ᵢ )  β ᵢ ⱼ", ACCENT_A),
                     ("        t              Σ ₀ ⁶ ⁰                 ‖ Δ ‖", DIM),)
                    + tuple((f"      {t:.1f}        {a:+.8f}        {e:.1e}", ACCENT_B)
                            for t, a, _b, e in CLOSED[1:])
                    + (("λ  =  − 0.5   ,   m  =  2", ACCENT_C),),
                    y0=0.92, dy=0.25, size=FS_TAG - 4))
  g.add(self._cap("細的橘線整條躺在粗的藍線上",
                  "the thin orange curve lies along the thick blue one all the way"))
  return g.add(self._foot("定理 3.4：一般的解是 k 個這種項的和，形狀是 t ʲ exp ( t λ ᵢ ) 乘一個常向量，項數正好是多項式 p 的次數",
                          "theorem 3.4: the general solution is a sum of such terms, each a power of t times an exponential times a constant vector, with as many terms as the degree of the polynomial",
                          ACCENT_A,
                          "右表比對的是截到 60 項的級數與兩項的閉式，差到機器精度。複數情形完全一樣，只是 λ 可以有虛部，外面那個指數就帶一個週期因子",
                          "the table compares the series truncated at sixty terms with the two-term closed form, agreeing to machine precision; the complex case is identical, with a periodic factor when lambda has an imaginary part"))

 # ── beat 10: the asymptotic dichotomy ────────────────────────────
 def _asymptotic(self):
  # a log scale, because the four cases span four orders of magnitude and on a
  # linear axis three of them lie flat along the bottom and cannot be told apart.
  # It also puts the dichotomy on screen: bounded is exactly "on the zero line".
  ox, oy, sx, sy = -5.90, 0.02, 0.330, 0.32
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14),
             Line([ox, oy - 0.76, 0], [ox, oy + 0.54, 0], color=DIM, stroke_width=1.3))
  cols = (WARN, ACCENT_C, ACCENT_B, ACCENT_A)
  for (lab, root, m, _row), col in zip(CASES, cols):
   def lg(t, root=root, m=m):
    return math.log10(abs(cmath.exp(root * t) * (complex(t, 1.0) if m == 2 else 1.0)))
   g.add(self._fcurve(ox, oy, sx, sy, lg, col, t0=0.0, t1=10.0, sw=2.6, n=170))
  g.add(self._sym(oy - 0.94, "10", DIM, FS_TAG - 4, x=ox + 3.30, w=0.50),
        self._sym(oy - 0.94, "t", DIM, FS_TAG - 3, x=ox + 1.70, w=0.34))
  g.add(self._legend(ox + 0.06, ((WARN, "Re λ  >  0", 1.30), (ACCENT_C, "Re λ  <  0", 1.30),
                                 (ACCENT_B, "Re λ = 0 , m = 1", 2.10),
                                 (ACCENT_A, "Re λ = 0 , m = 2", 2.10)), y0=1.14, dy=0.24))
  g.add(self._table((("    t      Re λ > 0    Re λ < 0     m = 1      m = 2", DIM),)
                    + tuple((f"      {int(t):2d}      {r[0]:8.3f}  {r[1]:8.3f}  {r[2]:8.3f}  {r[3]:8.3f}",
                             ACCENT_B) for t, r in
                            ((tt, [CASES[c][3][i] for c in range(4)])
                             for i, tt in enumerate((0.0, 5.0, 10.0, 20.0))))
                    + (("sup ‖ f ‖  <  ∞     ⟺     Re λ = 0  ,  m = 1", ACCENT_A),),
                    y0=0.90, dy=0.27, size=FS_TAG - 4))
  g.add(self._cap("只有青線一直躺在零軸上，右表第三欄也一直是 1",
                  "only the blue curve stays on the zero line, and its column stays at one"))
  return g.add(self._foot("漸近行為完全由根決定：Re λ 大於零指數爆炸、小於零趨近零；Re λ 等於零而重數大於一時像 t ᵐ ⁻ ¹ 那樣長",
                          "the asymptotics are controlled entirely by the roots: positive real part blows up, negative decays, and zero real part with multiplicity above one grows like a power of t",
                          ACCENT_A,
                          "所以解在整條 ℝ 上有界，若且唯若所有根都是純虛數而且重數都是 1。圖的縱軸取了對數——四個案例跨四個數量級，線性軸會把三條壓在底部",
                          "so the solutions are bounded on the whole line exactly when every root is pure imaginary with multiplicity one; the vertical axis is logarithmic, since the four cases span four orders of magnitude"))

 def stage(self):
  a, b, c = self._target(), self._total(), self._integrate()
  d, e, f_ = self._thm33(), self._lemma31(), self._lemma32()
  h, i, j = self._expo(), self._splitW(), self._finite()
  k, l = self._thm34(), self._asymptotic()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE78ZH, AdvCalcE78EN = make(AdvCalcE78Base, "78", prefix="AdvCalcE")
