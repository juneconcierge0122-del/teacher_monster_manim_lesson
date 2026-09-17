"""advcalc E77 -- chapter 6, section 3 (book pp. 276-277): the linear equation,
the structure of its solution space, and the fundamental solution.

The moment F is linear in its second variable -- F(t, alpha) = T_t(alpha) with
||T_t|| <= c(t) and c continuous -- Theorem 1.4's strong Lipschitz hypothesis
comes free, so every solution is global and the whole section can be done in
linear algebra.  Norms play no part in Theorem 3.1.

Theorem 3.1 says that S: f |-> f' - F(t, f) is a surjective linear map from the
continuously differentiable functions onto the continuous ones; that its null
space N is the space of global solutions; that evaluation at any t_0 restricted
to N is an isomorphism onto W; and that the null space M of that evaluation is
therefore a complement of N, which determines a right inverse of S.  The proof
is section 1 in one sentence: for fixed g the equation with F + g has a unique
global solution through any initial point, so <S, pi_t0> is a bijection.

That complement is what splits the initial-value problem into two independent
halves: inhomogeneous equation with zero initial data, plus homogeneous equation
with the given initial data.  The homogeneous half is then carried by the
fundamental solution K_t = phi_t . phi_0^-1, a one-parameter family of
isomorphisms of W with K_0 = I, and dK_t/dt = T_t . K_t -- pointwise at each
beta.  Theorem 3.2 upgrades that to a genuine norm-limit derivative as soon as
t |-> T_t is continuous, which the hypotheses so far do not give.

Everything is checked on a linear equation that is genuinely time-dependent yet
still has a closed-form fundamental solution: T_t = (1 + t) J with J the
rotation generator, whose operators all commute, so K_t is rotation through
Theta(t) = t + t^2/2.
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
TAU = math.tau


# ── 2x2 helpers ──────────────────────────────────────────────────────
def mv(M, v):
 return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def mm(A, B):
 return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def sm(c, M):
 return [[c * M[i][j] for j in range(2)] for i in range(2)]


def inv(M):
 d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
 return [[M[1][1] / d, -M[0][1] / d], [-M[1][0] / d, M[0][0] / d]]


def opnorm(M):
 """the operator norm of a 2x2, by sampling the unit circle finely enough."""
 return max(math.hypot(*mv(M, (math.cos(TAU * k / 720), math.sin(TAU * k / 720))))
            for k in range(720))


# ── the example: a genuinely time-dependent linear equation ──────────
J = [[0.0, -1.0], [1.0, 0.0]]


def T(t):
 return sm(1.0 + t, J)


def theta(t):
 return t + 0.5 * t * t


def K(t):
 c, s = math.cos(theta(t)), math.sin(theta(t))
 return [[c, -s], [s, c]]


assert all(abs(K(0.0)[i][j] - (1.0 if i == j else 0.0)) < 1e-15
           for i in range(2) for j in range(2)), "K is the identity at zero"
NORMS = [(t, opnorm(T(t)), 1.0 + t) for t in (0.0, 0.5, 1.0, 1.5, 2.0)]
assert all(abs(n - c) < 1e-6 for _t, n, c in NORMS), \
    "the operator norm is exactly 1 + t, which is the continuous c(t) of the hypothesis"

# dK/dt = T_t . K_t, checked as a matrix
for _t in (0.2, 0.7, 1.3, 2.0):
 _h = 1e-6
 _d = [[(K(_t + _h)[i][j] - K(_t - _h)[i][j]) / (2 * _h) for j in range(2)] for i in range(2)]
 _p = mm(T(_t), K(_t))
 assert max(abs(_d[i][j] - _p[i][j]) for i in range(2) for j in range(2)) < 1e-6, \
     "the fundamental solution satisfies its own differential equation"

# and K_t(beta) really is the solution through <0, beta>
for _b in ((1.0, 0.0), (0.0, 1.0), (0.6, -0.8)):
 for _t in (0.3, 1.1, 1.9):
  _h = 1e-6
  _d = tuple((mv(K(_t + _h), _b)[i] - mv(K(_t - _h), _b)[i]) / (2 * _h) for i in range(2))
  _f = mv(T(_t), mv(K(_t), _b))
  assert max(abs(_d[i] - _f[i]) for i in range(2)) < 1e-6

# ── beat 4: the two basis solutions stay a basis at every moment ──────
E1, E2 = (1.0, 0.0), (0.0, 1.0)
T0 = 0.8
BASIS = []
for _t in (0.0, 0.4, T0, 1.4, 2.0):
 _a, _b = mv(K(_t), E1), mv(K(_t), E2)
 BASIS.append((_t, _a, _b, _a[0] * _b[1] - _a[1] * _b[0]))
assert all(abs(d - 1.0) < 1e-9 for _t, _a, _b, d in BASIS), \
    "the determinant stays 1, so the pair is a basis at every moment: that is the isomorphism"
DIM_N = 2

# ── beats 5 and 6: the splitting, done on one concrete f ──────────────
def f_any(t):
 """some function in X_1, chosen with no regard for the equation."""
 return (t * t, math.sin(t))


def Sf(f, t):
 h = 1e-6
 d = tuple((f(t + h)[i] - f(t - h)[i]) / (2 * h) for i in range(2))
 Tf = mv(T(t), f(t))
 return (d[0] - Tf[0], d[1] - Tf[1])


A_AT_T0 = f_any(T0)
KI = inv(K(T0))


def k_part(t):
 """the solution through <T0, f(T0)>: the N half of the splitting."""
 return mv(K(t), mv(KI, A_AT_T0))


def h_part(t):
 return (f_any(t)[0] - k_part(t)[0], f_any(t)[1] - k_part(t)[1])


assert max(abs(h_part(T0)[i]) for i in range(2)) < 1e-12, \
    "the M half vanishes at t_0, which is what defines M"
SPLIT = []
for _t in (0.2, 0.8, 1.4, 2.0):
 _sf, _sh, _sk = Sf(f_any, _t), Sf(h_part, _t), Sf(k_part, _t)
 SPLIT.append((_t, math.hypot(*_sf), math.hypot(*_sh), math.hypot(*_sk)))
assert all(abs(a - b) < 1e-5 for _t, a, b, _c in SPLIT), \
    "S h equals S f, because the other half is a solution"
assert all(c < 1e-5 for _t, _a, _b, c in SPLIT), "and S k is zero"

# ── beat 3: surjectivity, checked by building a solution for one g ────
def g_test(t):
 return (1.0, 0.0)


def simpson_vec(fn, a, b, n=200):
 h = (b - a) / n
 acc = [0.0, 0.0]
 for i in range(2):
  s = fn(a)[i] + fn(b)[i]
  for kk in range(1, n):
   s += (4 if kk % 2 else 2) * fn(a + kk * h)[i]
  acc[i] = s * h / 3
 return tuple(acc)


def f_inhom(t):
 """Theorem 3.3's formula, used here only to witness that S is onto."""
 if abs(t) < 1e-12:
  return (0.0, 0.0)
 return mv(K(t), simpson_vec(lambda s: mv(inv(K(s)), g_test(s)), 0.0, t))


ONTO = []
for _t in (0.4, 0.9, 1.5, 2.0):
 _r = Sf(f_inhom, _t)
 ONTO.append((_t, _r[0], _r[1]))
assert all(abs(a - 1.0) < 2e-4 and abs(b) < 2e-4 for _t, a, b in ONTO), \
    "S applied to it gives back g, so that g is in the image"
assert max(abs(f_inhom(0.0)[i]) for i in range(2)) < 1e-12


class AdvCalcE77Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 77

 MODE_LABEL = {
  0: {"zh": "線性讓定理 1.4 免費送", "en": "linearity hands over theorem 1.4"},
  1: {"zh": "兩個函數空間與 S", "en": "two function spaces and S"},
  2: {"zh": "定理 3.1", "en": "theorem 3.1"},
  3: {"zh": "證明只有一句話", "en": "the proof is one sentence"},
  4: {"zh": "N 與 W 同構", "en": "the solution space is a copy of W"},
  5: {"zh": "M 是 N 的補", "en": "M is a complement of N"},
  6: {"zh": "初始值問題拆成兩半", "en": "the problem splits in two"},
  7: {"zh": "基本解 K ₜ", "en": "the fundamental solution"},
  8: {"zh": "導數只是逐點的意思", "en": "the derivative is only pointwise"},
  9: {"zh": "定理 3.2", "en": "theorem 3.2"},
  10: {"zh": "這一集的例子，與下一集", "en": "the example, and what comes next"},
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

 def _orbit(self, cx, cy, s, beta, col, t1=2.0, sw=2.6, n=160):
  return self._curve([[cx + s * mv(K(t1 * k / n), beta)[0],
                       cy + s * mv(K(t1 * k / n), beta)[1], 0] for k in range(n + 1)],
                     col, sw=sw)

 # ── beat 0: linearity gives the hypothesis of theorem 1.4 ─────────
 def _free(self):
  ox, oy, sx, sy = -5.90, -0.56, 1.32, 0.42
  g = VGroup(self._frame(ox, oy, 3.40, 1.46, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: 1.0 + t, ACCENT_B, t0=0.0, t1=2.4, sw=3.0))
  for t in (0.0, 0.6, 1.2, 1.8, 2.4):
   g.add(Dot([ox + sx * t, oy + sy * (1.0 + t), 0], radius=0.052, color=ACCENT_A))
  g.add(self._sym(oy + 1.62, "‖ T ₜ ‖  =  1 + t", ACCENT_B, FS_TAG - 3, x=ox + 1.70, w=2.20))
  g.add(self._sym(oy - 0.26, "t", DIM, FS_TAG - 3, x=ox + 3.28, w=0.34))
  g.add(self._table((("F ( t , α )   =   T ₜ ( α )", ACCENT_A),
                     ("‖ T ₜ ( ξ ) − T ₜ ( η ) ‖  =  ‖ T ₜ ( ξ − η ) ‖  ≤  c ( t ) ‖ ξ − η ‖",
                      ACCENT_C),
                     ("⇒     1.4          ⇒     J   =   I", ACCENT_A),)
                    + tuple((f"      t = {t:.1f}       ‖ T ₜ ‖ = {n:.6f}", ACCENT_B)
                            for t, n, _c in NORMS[:3]),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("線性讓那個不等式變成一行代數",
                  "linearity turns that inequality into one line of algebra"))
  return g.add(self._foot("F 對第二個變數線性時，F ( t , ξ ) − F ( t , η ) 就是 T ₜ ( ξ − η )，所以 Lipschitz 條件退化成「T ₜ 有界」——而且是對 W 裡所有點成立的那種",
                          "when F is linear in its second variable the difference of its values is the operator applied to the difference, so the Lipschitz condition collapses into boundedness of the operator, globally in alpha",
                          ACCENT_A,
                          "那正是定理 1.4 要的強假設，所以這一節的解一律活在整個 I 上。第 3 節因此可以只談整體解，而問題整個變成線性代數",
                          "that is exactly the strong hypothesis Theorem 1.4 wants, so every solution here is global, and the section can work entirely in linear algebra"))

 # ── beat 1: the two spaces and S ──────────────────────────────────
 def _spaces(self):
  oy = 0.16
  g = VGroup()
  for x0, lab, col, w_ in ((-5.10, "X ₁", ACCENT_B, 1.10), (-2.20, "X ₀", ACCENT_C, 1.10)):
   g.add(self._box(x0, oy, lab, col, w=w_, h=0.72, size=FS_TAG + 4))
  g.add(self._arr([-4.50, oy + 0.14, 0], [-2.80, oy + 0.14, 0], ACCENT_A, sw=4, tl=0.16))
  g.add(self._sym(oy + 0.46, "S", ACCENT_A, FS_TAG + 1, x=-3.65, w=0.50))
  g.add(self._sym(oy - 0.62, "𝒞 ¹ ( I , W )", ACCENT_B, FS_TAG - 3, x=-5.10, w=1.70),
        self._sym(oy - 0.62, "𝒞 ( I , W )", ACCENT_C, FS_TAG - 3, x=-2.20, w=1.70))
  g.add(self._sym(oy - 1.02, "f", ACCENT_B, FS_TAG - 2, x=-5.10, w=0.50),
        self._sym(oy - 1.02, "f ′ − F ( t , f )", ACCENT_C, FS_TAG - 3, x=-2.20, w=1.90))
  g.add(self._table((("X ₀   =   𝒞 ( I , W )", ACCENT_C),
                     ("X ₁   =   𝒞 ¹ ( I , W )   ⊂   X ₀", ACCENT_B),
                     ("( S f ) ( t )   =   f ′ ( t )  −  F ( t , f ( t ) )", ACCENT_A),
                     ("‖ · ‖", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("最後一列是灰的，因為範數在這裡不起作用",
                  "the last row is grey because norms play no part here"))
  return g.add(self._foot("設 X ₀ 是 I 到 W 的連續函數、X ₁ 是其中有連續一階導數的那些，S 把 f 送到 f ′ 減去 F 帶入 t 與 f ( t )",
                          "let the first space be the continuous functions from I to W and the second those with a continuous derivative, and let S send f to its derivative minus F at t and f of t",
                          ACCENT_A,
                          "注意這兩個空間都沒有指定範數。定理 3.1 是純粹的線性代數：滿射、核、補、右反元素——一個不等式都用不到",
                          "note that neither space is given a norm: Theorem 3.1 is pure linear algebra about surjectivity, null spaces, complements and right inverses, with no inequality anywhere"))

 # ── beat 2: the statement ─────────────────────────────────────────
 def _thm31(self):
  oy = 0.24
  g = VGroup()
  for x0, lab, col, w_ in ((-5.30, "X ₁", ACCENT_B, 1.00), (-2.10, "X ₀ × W", ACCENT_A, 1.90)):
   g.add(self._box(x0, oy, lab, col, w=w_, h=0.70, size=FS_TAG + 3))
  g.add(self._arr([-4.75, oy + 0.12, 0], [-3.10, oy + 0.12, 0], ACCENT_A, sw=4, tl=0.16))
  g.add(self._sym(oy + 0.44, "⟨ S , π ₜ ₀ ⟩", ACCENT_A, FS_TAG - 2, x=-3.92, w=1.50))
  g.add(self._sym(oy - 0.10, "≅", ACCENT_A, FS_TAG + 2, x=-3.92, w=0.50))
  g.add(self._sym(oy - 0.72, "N  =  ker S", ACCENT_C, FS_TAG - 3, x=-5.30, w=1.70),
        self._sym(oy - 0.72, "{ 0 } × W", ACCENT_C, FS_TAG - 3, x=-2.10, w=1.40))
  g.add(self._sym(oy - 1.08, "M  =  ker π ₜ ₀", WARN, FS_TAG - 3, x=-5.30, w=1.90),
        self._sym(oy - 1.08, "X ₀ × { 0 }", WARN, FS_TAG - 3, x=-2.10, w=1.50))
  g.add(self._table((("S     X ₁ → X ₀", ACCENT_B),
                     ("N   =   ker S", ACCENT_C),
                     ("π ₜ ₀ ↾ N   :   N   ≅   W", ACCENT_A),
                     ("X ₁   =   M   ⊕   N", WARN),
                     ("S ∘ R   =   I", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("左右兩欄逐列對應，整個定理就是這張對照表",
                  "the two columns correspond row by row, and that is the whole theorem"))
  return g.add(self._foot("定理 3.1：S 是滿射；整體解全體 N 是 S 的核，所以是向量空間；在 t ₀ 取值限制到 N 上是 N 到 W 的同構；它的核 M 因此是 N 的補，並決定一個右反元素",
                          "theorem 3.1: S is surjective; the global solutions are its null space and so a vector space; evaluation at the initial time restricted there is an isomorphism onto W; and its null space is a complement determining a right inverse",
                          ACCENT_A,
                          "書上說最後那一句「⟨ S , π ₜ ₀ ⟩ 是 X ₁ 到 X ₀ × W 的同構」與前面每一句等價——左邊的分解只是右邊那個明顯的直和分解拉回來而已",
                          "the book notes that the single statement that the pair map is an isomorphism is equivalent to all the rest: the decomposition on the left is just the obvious one on the right pulled back"))

 # ── beat 3: the proof, and surjectivity witnessed ─────────────────
 def _proof(self):
  ox, oy, sx, sy = -5.90, -0.30, 1.42, 0.52
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_inhom(t)[0], ACCENT_B, t0=0.0, t1=2.2, sw=3.0))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_inhom(t)[1], ACCENT_C, t0=0.0, t1=2.2, sw=3.0))
  g.add(Dot([ox, oy, 0], radius=0.056, color=ACCENT_A))
  g.add(self._legend(ox + 0.08, ((ACCENT_B, "f ¹", 0.50), (ACCENT_C, "f ²", 0.50)), y0=1.14))
  g.add(self._table((("G ( t , α )   =   F ( t , α )  +  g ( t )", ACCENT_A),
                     ("1.3  ,  1.4     ⇒     ∃ !   f  ,   J = I", ACCENT_B),
                     ("        t            ( S f ) ( t )", DIM),)
                    + tuple((f"      {t:.1f}        ( {a:.4f} , {b:+.4f} )", ACCENT_B)
                            for t, a, b in ONTO[:3])
                    + (("g ( t )   =   ( 1 , 0 )", ACCENT_A),),
                    y0=0.92, dy=0.25, size=FS_TAG - 3))
  g.add(self._cap("右欄每一列都是 g 自己，所以那個 g 在像裡",
                  "every row of the right column is g itself, so that g is in the image"))
  return g.add(self._foot("證明只有一句話：對固定的 g 設 G = F + g，那就是第 1 節的方程，由定理 1.3 與 1.4 它有唯一的整體解通過任一初始點",
                          "the proof is one sentence: for fixed g set G to be F plus g, which is section 1's equation, so it has a unique global solution through any initial point",
                          ACCENT_A,
                          "所以把 f 送到 ⟨ S f , f ( t ₀ ) ⟩ 是雙射，而且顯然線性——同構。畫面上是 g = ( 1 , 0 ) 的那條解，兩個座標各一條曲線",
                          "so sending f to the pair of S f and its initial value is a bijection and plainly linear, hence an isomorphism; on screen is the solution for a constant g, one curve per coordinate"))

 # ── beat 4: the solution space is a copy of W ─────────────────────
 def _iso(self):
  cx, cy, s = -4.05, -0.14, 0.58
  g = VGroup(self._arr([cx - 1.40, cy, 0], [cx + 1.40, cy, 0], DIM, sw=3, tl=0.12),
             self._arr([cx, cy - 0.94, 0], [cx, cy + 1.00, 0], DIM, sw=3, tl=0.12))
  # one circle, drawn once: K_t is a rotation, so every unit beta has the same
  # orbit and two coloured orbits would be the same curve twice
  g.add(self._curve([[cx + s * math.cos(TAU * k / 96), cy + s * math.sin(TAU * k / 96), 0]
                     for k in range(97)], DIM, sw=1.8))
  for t, col in ((0.0, ACCENT_B), (T0, WARN)):
   a, b = mv(K(t), E1), mv(K(t), E2)
   g.add(self._arr([cx, cy, 0], [cx + s * a[0], cy + s * a[1], 0], col, sw=4, tl=0.14),
         self._arr([cx, cy, 0], [cx + s * b[0], cy + s * b[1], 0], col, sw=4, tl=0.14),
         self._dash([cx + s * a[0], cy + s * a[1], 0], [cx + s * b[0], cy + s * b[1], 0],
                    col, n=7, sw=1.3))
  g.add(self._legend(cx - 2.20, ((ACCENT_B, "t  =  0", 0.90),
                                 (WARN, f"t  =  {T0}", 0.90)), y0=1.14))
  g.add(self._table((("        t          det [ f ₁ ( t )   f ₂ ( t ) ]", DIM),)
                    + tuple((f"      {t:.1f}                {d:.8f}", ACCENT_B)
                            for t, _a, _b, d in BASIS)
                    + ((f"dim N   =   dim W   =   {DIM_N}", ACCENT_A),),
                    y0=0.92, dy=0.27, size=FS_TAG - 3))
  g.add(self._cap("行列式永遠是 1，所以任何時刻取值都還是一組基",
                  "the determinant is always one, so evaluating at any moment still gives a basis"))
  return g.add(self._foot("在 t ₀ 取值把 N 同構地送到 W，所以 dim N = dim W。灰圈是共同的軌道（K ₜ 是旋轉），兩組箭頭是兩條基底解在 t = 0 與 t = 0.8 的值",
                          "evaluation at the initial time carries the solution space isomorphically onto W, so the dimensions agree; the grey circle is the common orbit, and the two pairs of arrows are the basis solutions at two different moments",
                          ACCENT_A,
                          "同構的內容全在那個行列式：兩條解在任何一個時刻取的值都還是線性獨立，從來不會塌下去。虛線是它們的斜邊，兩組一樣長，因為這個例子的 K ₜ 只是旋轉",
                          "the content of the isomorphism is that determinant: the values stay independent at every moment and never collapse, which is special to the linear case"))

 # ── beat 5: M and N are complementary ────────────────────────────
 def _complement(self):
  ox, oy, sx, sy = -5.90, -0.34, 1.86, 0.34
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.40, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: f_any(t)[0], ACCENT_A, t0=0.0, t1=1.70, sw=3.2))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: k_part(t)[0], ACCENT_C, t0=0.0, t1=1.70, sw=2.4))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: h_part(t)[0], WARN, t0=0.0, t1=1.70, sw=2.4))
  g.add(self._dash([ox + sx * T0, oy - 0.22, 0], [ox + sx * T0, oy + 1.06, 0], DIM, n=9, sw=1.3))
  g.add(Dot([ox + sx * T0, oy, 0], radius=0.055, color=WARN))
  g.add(self._sym(oy - 0.40, "t ₀", DIM, FS_TAG - 3, x=ox + sx * T0, w=0.44))
  g.add(self._legend(ox + 0.08, ((ACCENT_A, "f", 0.50), (ACCENT_C, "k  ∈  N", 1.10),
                                 (WARN, "h  ∈  M", 1.10)), y0=1.14, dy=0.25))
  g.add(self._table((("M   =   ker π ₜ ₀", WARN),
                     ("X ₁   =   M   ⊕   N", ACCENT_A),
                     (f"h ( t ₀ )   =   ( 0 , 0 )        t ₀ = {T0}", WARN),
                     ("k   =   K ₜ  K ₜ ₀ ⁻ ¹  f ( t ₀ )", ACCENT_C),
                     ("f   =   h   +   k", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("紅線在虛線上穿過零點，那就是 M 的定義",
                  "the red curve crosses zero exactly at the dashed line, which is what defines M"))
  return g.add(self._foot("M 是在 t ₀ 取值為零的那些函數。任何一個 X ₁ 裡的 f 都唯一地拆成 h 加 k：k 是通過 ⟨ t ₀ , f ( t ₀ ) ⟩ 的那條解，h 是剩下的",
                          "M is the functions vanishing at the initial time, and every f splits uniquely as h plus k, where k is the solution through its own initial value and h is what remains",
                          ACCENT_A,
                          "畫面上的 f 是隨手取的 ⟨ t ² , sin t ⟩，跟方程一點關係都沒有——重點正是這樣的 f 也照拆不誤。圖上畫的是第一個座標",
                          "the f on screen is an arbitrary pair chosen with no regard for the equation, which is the point: it splits all the same; the plot shows the first coordinate"))

 # ── beat 6: the two independent subproblems ──────────────────────
 def _split(self):
  oy = 0.30
  g = VGroup()
  g.add(self._box(-5.30, oy, "f", ACCENT_A, w=0.70, h=0.56, size=FS_TAG + 3))
  g.add(self._box(-3.00, oy + 0.50, "h", WARN, w=0.70, h=0.56, size=FS_TAG + 3))
  g.add(self._box(-3.00, oy - 0.62, "k", ACCENT_C, w=0.70, h=0.56, size=FS_TAG + 3))
  g.add(self._arr([-4.90, oy + 0.10, 0], [-3.42, oy + 0.46, 0], DIM, sw=3, tl=0.14),
        self._arr([-4.90, oy - 0.10, 0], [-3.42, oy - 0.58, 0], DIM, sw=3, tl=0.14))
  g.add(self._sym(oy + 0.84, "S h = g  ,  h ( t ₀ ) = 0", WARN, FS_TAG - 3, x=-1.70, w=2.60),
        self._sym(oy - 0.98, "S k = 0  ,  k ( t ₀ ) = α ₀", ACCENT_C, FS_TAG - 3, x=-1.70, w=2.60))
  g.add(self._table((("S f  =  g    ,    f ( t ₀ )  =  α ₀", ACCENT_A),
                     ("f   =   h   +   k", ACCENT_A),
                     ("h   =   R ( g )        R   :   X ₀ → M", WARN),
                     ("k   =   ( π ₜ ₀ ↾ N ) ⁻ ¹ ( α ₀ )", ACCENT_C),
                     ("M   ∩   N   =   { 0 }", DIM)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("兩個子問題各自只帶一半的資料",
                  "each subproblem carries only half of the data"))
  return g.add(self._foot("M 是 N 的補，這件事把初始值問題拆成兩個獨立的子問題：h 解非齊次方程但初始值歸零，k 解齊次方程但帶著初始值",
                          "the complement splits the initial-value problem into two independent subproblems: one solves the inhomogeneous equation with zero initial data, the other the homogeneous equation with the given data",
                          ACCENT_A,
                          "書上說初始值問題在某種意義下是這兩個獨立問題的「直和」。下一集的定理 3.3 會給出上面那個 R 的顯式公式",
                          "the book calls the initial-value problem the direct sum of these two independent ones; next episode's Theorem 3.3 gives an explicit formula for that right inverse"))

 # ── beat 7: the fundamental solution ─────────────────────────────
 def _fundamental(self):
  cx, cy, s = -4.05, -0.14, 0.56
  g = VGroup(self._arr([cx - 1.42, cy, 0], [cx + 1.42, cy, 0], DIM, sw=3, tl=0.12),
             self._arr([cx, cy - 0.92, 0], [cx, cy + 0.98, 0], DIM, sw=3, tl=0.12))
  BET = (0.9, 0.35)
  g.add(self._orbit(cx, cy, s, BET, ACCENT_A, t1=2.0, sw=3.0))
  g.add(self._arr([cx, cy, 0], [cx + s * BET[0], cy + s * BET[1], 0], ACCENT_B, sw=4, tl=0.14))
  for t, col in ((0.7, ACCENT_C), (1.5, WARN)):
   v = mv(K(t), BET)
   g.add(self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=4, tl=0.14))
  g.add(self._legend(cx - 2.20, ((ACCENT_B, "β", 0.40), (ACCENT_C, "K ₀ ․ ₇ β", 1.20),
                                 (WARN, "K ₁ ․ ₅ β", 1.20)), y0=1.14, dy=0.25))
  g.add(self._table((("φ ₜ   =   π ₜ ↾ N     :     N   ≅   W", ACCENT_C),
                     ("K ₜ   =   φ ₜ  ∘  φ ₀ ⁻ ¹", ACCENT_A),
                     ("K ₀   =   I", ACCENT_B),
                     ("f ᵦ ( t )   =   K ₜ ( β )", ACCENT_A),
                     (f"Θ ( t )  =  t + t ² / 2      Θ ( 1.5 ) = {theta(1.5):.4f}", DIM)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("三支箭頭同長，因為 K ₜ 在這個例子裡是旋轉",
                  "the three arrows have equal length, because here K is a rotation"))
  return g.add(self._foot("φ ₜ 是在時刻 t 取值那個 N 到 W 的同構。取 t ₀ = 0，定義 K ₜ = φ ₜ ∘ φ ₀ ⁻ ¹——它是 W 到自己的一族線性同構，書上叫基本解",
                          "evaluation at time t is an isomorphism from the solution space onto W; with the initial time zero, K at t is that isomorphism composed with the inverse of the one at zero, a family of isomorphisms the book calls a fundamental solution",
                          ACCENT_A,
                          "K ₜ 作用在 β 上，就是通過 ⟨ 0 , β ⟩ 的那條解在時刻 t 的值。一個算子就把所有初始值的解一次全帶著走",
                          "K at t applied to a vector is the value at time t of the solution through it, so one operator carries the solutions for every initial value at once"))

 # ── beat 8: the derivative is only pointwise so far ──────────────
 def _pointwise(self):
  cx, cy, s = -4.05, -0.14, 0.56
  g = VGroup(self._arr([cx - 1.42, cy, 0], [cx + 1.42, cy, 0], DIM, sw=3, tl=0.12),
             self._arr([cx, cy - 0.92, 0], [cx, cy + 0.98, 0], DIM, sw=3, tl=0.12))
  # three different norms on purpose, or the three orbits are one circle
  for beta, col in (((1.0, 0.0), ACCENT_B), ((0.0, 0.62), ACCENT_C),
                    ((-0.24, 0.24), WARN)):
   g.add(self._orbit(cx, cy, s, beta, col, t1=2.0, sw=2.0))
   t = 1.1
   v, w = mv(K(t), beta), mv(T(t), mv(K(t), beta))
   n = math.hypot(*w)
   g.add(Dot([cx + s * v[0], cy + s * v[1], 0], radius=0.050, color=col),
         self._arr([cx + s * v[0], cy + s * v[1], 0],
                   [cx + s * v[0] + 0.34 * w[0] / n, cy + s * v[1] + 0.34 * w[1] / n, 0],
                   col, sw=3, tl=0.11))
  g.add(self._table((("d K ₜ / d t   =   T ₜ  ∘  K ₜ", ACCENT_A),
                     ("( β )          ∀ β ∈ W", WARN),
                     ("t   ↦   T ₜ          Hom W", DIM),
                     ("‖ · ‖", DIM),
                     ("⇒     3.2", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("箭頭是逐點驗出來的，每個 β 一支",
                  "the arrows are checked one vector at a time, one per beta"))
  return g.add(self._foot("既然每條解都滿足方程，d K ₜ / d t = T ₜ ∘ K ₜ——可是這句話目前只是逐點的意思：對每個 β 分別成立",
                          "since every solution satisfies the equation, the derivative of K is the operator composed with K, but so far only pointwise: separately at each vector",
                          ACCENT_A,
                          "導數不一定以 Hom W 的範數極限存在，因為假設裡從頭到尾沒有說 t ↦ T ₜ 是連續的——只說了 ‖ T ₜ ‖ 被 c ( t ) 壓住",
                          "the derivative need not exist as a norm limit in the space of operators, because nothing in the hypotheses says the operator depends continuously on t, only that its norm is bounded"))

 # ── beat 9: theorem 3.2 ──────────────────────────────────────────
 def _thm32(self):
  ox, oy, sx, sy = -5.90, -0.50, 1.32, 0.46
  g = VGroup(self._frame(ox, oy, 3.40, 1.44, down=0.10))
  for i, j, col, lab, lw in ((0, 0, ACCENT_B, "K ¹ ¹", 1.00), (1, 0, ACCENT_C, "K ² ¹", 1.00)):
   g.add(self._fcurve(ox, oy + 0.62, sx, sy, lambda t, i=i, j=j: K(t)[i][j], col,
                      t0=0.0, t1=2.4, sw=2.8))
  g.add(self._dash([ox, oy + 0.62, 0], [ox + 3.28, oy + 0.62, 0], DIM, n=22, sw=1.1))
  g.add(Dot([ox, oy + 0.62 + sy, 0], radius=0.055, color=ACCENT_B))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "K ¹ ¹", 0.94), (ACCENT_C, "K ² ¹", 0.94)), y0=1.14))
  g.add(self._table((("t   ↦   T ₜ          ⟹        ⟨ t , A ⟩  ↦  T ₜ ∘ A", ACCENT_C),
                     ("d A / d t   =   T ₜ  ∘  A    ,    A ₀  =  I", ACCENT_A),
                     ("∃ !   A   ∈   𝒞 ¹ ( I , Hom W )", ACCENT_B),
                     ("d A ₜ ( β ) / d t   =   T ₜ ( A ₜ ( β ) )", ACCENT_C),
                     ("A ₜ   =   K ₜ", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("兩條曲線是 K ₜ 的兩個矩陣元，對 t 光滑",
                  "the curves are two matrix entries of K, smooth in t"))
  return g.add(self._foot("定理 3.2：只要 t ↦ T ₜ 連續，初始值問題 d A / d t = T ₜ ∘ A、A ₀ = I 在 𝒞 ¹ ( I , Hom W ) 裡就有唯一解",
                          "theorem 3.2: as soon as the operator depends continuously on t, the initial-value problem for A with A at zero the identity has a unique solution with a continuous derivative",
                          ACCENT_A,
                          "而在 β 取值是有界線性映射，所以 A ₜ ( β ) 對 t 可微並滿足同一個方程，兩者因此相等——基本解升級成 Hom W 裡一條真正可微的參數曲線",
                          "and evaluation at a vector is a bounded linear map, so that solution satisfies the same equation and the two agree: the fundamental solution becomes a genuinely differentiable arc in the space of operators"))

 # ── beat 10: the example, and what comes next ────────────────────
 def _example(self):
  cx, cy, s = -4.05, -0.10, 0.56
  g = VGroup(self._arr([cx - 1.42, cy, 0], [cx + 1.42, cy, 0], DIM, sw=3, tl=0.12),
             self._arr([cx, cy - 0.88, 0], [cx, cy + 0.96, 0], DIM, sw=3, tl=0.12))
  BET = (1.0, 0.0)
  g.add(self._orbit(cx, cy, s, BET, ACCENT_A, t1=2.4, sw=2.8, n=200))
  for t, col in ((0.0, ACCENT_B), (0.8, ACCENT_C), (1.6, WARN), (2.4, DIM)):
   v = mv(K(t), BET)
   g.add(Dot([cx + s * v[0], cy + s * v[1], 0], radius=0.058, color=col))
  g.add(self._table((("T ₜ   =   ( 1 + t )  J", ACCENT_B),
                     ("Θ ( t )   =   t  +  t ² / 2", ACCENT_C),
                     ("K ₜ   =   exp ( Θ ( t )  J )", ACCENT_A),)
                    + tuple((f"      t = {t:.1f}      Θ = {theta(t):.4f}", DIM)
                            for t in (0.8, 1.6, 2.4)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("四個點的間隔越來越大，因為 ‖ T ₜ ‖ 一直在長",
                  "the four dots spread apart because the operator norm keeps growing"))
  return g.add(self._foot("這一集的例子是 T ₜ = ( 1 + t ) J，J 是旋轉生成元。所有 T ₜ 互相交換，所以基本解寫得出來：轉 Θ ( t ) = t + t ² / 2 那麼多的旋轉",
                          "the example is the rotation generator scaled by one plus t; those operators all commute, so the fundamental solution can be written down as rotation through t plus half t squared",
                          ACCENT_A,
                          "K ₀ = I、d K / d t = T ₜ ∘ K ₜ 都在場景檔裡驗過。下一集：定理 3.3 的顯式右反元素，然後是常係數與 e ᵗᵀ",
                          "that it is the identity at zero and satisfies its own equation are both checked in the scene file; next episode: the explicit right inverse of Theorem 3.3, then constant coefficients and the exponential"))

 def stage(self):
  a, b, c = self._free(), self._spaces(), self._thm31()
  d, e, f_ = self._proof(), self._iso(), self._complement()
  h, i, j = self._split(), self._fundamental(), self._pointwise()
  k, l = self._thm32(), self._example()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE77ZH, AdvCalcE77EN = make(AdvCalcE77Base, "77", prefix="AdvCalcE")
