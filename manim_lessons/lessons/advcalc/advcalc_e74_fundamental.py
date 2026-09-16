"""advcalc E74 -- chapter 6, section 1 (book pp. 266-269): the fundamental
theorem of ordinary differential equations, up to Theorem 1.2.

Chapter 6 opens by asking when dalpha/dt = F(t, alpha) has a solution through a
prescribed point, and answers it with the fixed-point theorem of chapter 4.  The
move that makes it work is a change of stage: integrating turns the differential
equation into f(t) = alpha_0 + int F(s, f(s)) ds, an equation that only asks f
to be continuous, and the continuous functions on a closed interval form a
complete space.  The right-hand side defines a map K on a ball of that space,
and a solution is exactly a fixed point of K.

Two estimates make K a contraction of the ball into itself: it moves the centre
by at most delta*m, and it shrinks distances by delta*c, where m bounds F, c is
the Lipschitz constant, and delta is the length of J.  Asking for both at once
is exactly delta < r/(m + cr).  Lemma 1.1 then shows any two solutions through
the same point agree on the intersection of their domains, which lets Theorem
1.2 drop the artificial requirement that the solution stay inside the small
neighbourhood U.

Everything on screen is computed from one example, dx/dt = 1 + x^2 through the
origin, whose solution is tan t.  On the ball of radius one about the origin
m = 2 and c = 2, so the theorem guarantees only |t| < 1/4 -- while the real
solution lives out to pi/2.  That gap, exactly a factor of 2*pi, is the honest
price of an estimate that has to work for every F at once.

The Lipschitz hypothesis is not decoration: dx/dt = 2*sqrt(|x|) is continuous
everywhere and has infinitely many solutions through the origin.
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
PI = math.pi


def simpson(g, a, b, n=800):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


# ── the running example: dx/dt = 1 + x^2 through the origin ───────────
def F(x):
 return 1.0 + x * x


R = 1.0
XS = [-1.0 + 0.001 * k for k in range(2001)]
M_BD = max(abs(F(x)) for x in XS)
assert abs(M_BD - 2.0) < 1e-12, "F is bounded by 2 on the ball of radius one"

# the Lipschitz quotient is |xi + eta|, so its supremum on that ball is 2; no
# sampled pair may exceed it, and the pairs closest together come closest to it
C_SUP = 2.0
QUO = [(a, b, abs(F(a) - F(b)) / abs(a - b))
       for a in (1.0, 0.9, 0.6, 0.2) for b in (0.98, 0.5, -0.4) if a != b]
assert all(q <= C_SUP + 1e-12 for _a, _b, q in QUO), "never above the supremum"
assert max(q for _a, _b, q in QUO) > 1.97, "and the tightest pair all but reaches it"

D_BALL = R / (M_BD + C_SUP * R)
D_CONTR = 1.0 / C_SUP
assert abs(D_BALL - 0.25) < 1e-12 and abs(D_CONTR - 0.5) < 1e-12
assert D_BALL < D_CONTR, "the ball condition bites first, so it is the one in the theorem"
DELTA = 0.2
CONTR = DELTA * C_SUP
assert CONTR < 1.0 and DELTA * M_BD < (1.0 - CONTR) * R, "delta = 0.2 satisfies both"
assert abs(CONTR - 0.4) < 1e-12

BLOW = PI / 2
RATIO = BLOW / D_BALL
assert abs(RATIO - 2 * PI) < 1e-12, "the guaranteed interval is short by exactly 2 pi"
EXIT = PI / 4
assert abs(math.tan(EXIT) - 1.0) < 1e-12, "and the solution leaves the ball at pi/4"

# ── beat 5: the Picard iteration, run for real ────────────────────────
NG, TMAX = 401, 1.0
H = TMAX / (NG - 1)
GRID = [H * k for k in range(NG)]


def picard(prev):
 """f_(n+1)(t) = 0 + int_0^t F(f_n(s)) ds, by the trapezoid rule on GRID."""
 g = [F(v) for v in prev]
 out = [0.0]
 for k in range(1, NG):
  out.append(out[-1] + H * (g[k - 1] + g[k]) / 2.0)
 return out


ITER = [[0.0] * NG]
for _ in range(7):
 ITER.append(picard(ITER[-1]))
TRUE = [math.tan(t) for t in GRID]
ERR = [max(abs(a - b) for a, b in zip(it, TRUE)) for it in ITER]
assert all(ERR[k] > ERR[k + 1] for k in range(len(ERR) - 1)), "every iterate is closer"
assert ERR[-1] < 0.005 and ERR[1] > 0.5, "and they close right in on tan"
assert abs(ITER[1][-1] - 1.0) < 1e-12, "the first iterate is t"
assert abs(ITER[2][-1] - 4.0 / 3.0) < 1e-4, "the second is t + t^3/3"

# ── beat 4: the integral form, checked against the solution ───────────
INT_T = 0.7
INT_A = simpson(lambda s: F(math.tan(s)), 0.0, INT_T)
assert abs(INT_A - math.tan(INT_T)) < 1e-9, \
    "the area under F(s, f(s)) is exactly the height of f: that is the equivalence"

# ── beat 6: how far K moves the centre of the ball ────────────────────
# K applied to the constant zero is t, so its sup norm on J is delta itself
CEN = [(d, d, d * M_BD) for d in (0.05, 0.10, 0.20, 0.25)]
assert all(act <= bnd + 1e-12 for _d, act, bnd in CEN)
assert all(abs(bnd - 2 * act) < 1e-12 for _d, act, bnd in CEN), "the bound is loose by 2"

# ── beat 7: K is a contraction, with the constant nearly attained ─────
PAIRS = ((0.80, 0.30), (0.90, 0.10), (1.00, 0.60), (1.00, 0.98))
CON = []
for _u, _v in PAIRS:
 _d = abs(_u - _v)
 _img = DELTA * abs(F(_u) - F(_v))
 CON.append((_u, _v, _d, _img, _img / _d, CONTR * _d))
assert all(img <= bnd + 1e-12 for _u, _v, _d, img, _q, bnd in CON), "the estimate holds"
assert max(q for _u, _v, _d, _i, q, _b in CON) > 0.39, "and the last pair nearly attains it"
assert max(q for _u, _v, _d, _i, q, _b in CON) < CONTR, "without ever reaching it"

# ── beats 1 and 2: what happens when the Lipschitz condition fails ────
def ROOT(x):
 return 2.0 * math.sqrt(abs(x))


def lift(a):
 """x = 0 up to a, then (t - a)^2 -- a solution through the origin for every a."""
 return lambda t: 0.0 if t <= a else (t - a) ** 2


LIFT_A = (0.0, 0.25, 0.50, 0.75)
for _a in LIFT_A:
 _f = lift(_a)
 for _t in (_a + 0.05, _a + 0.20, _a + 0.35):
  _d = (_f(_t + 1e-6) - _f(_t - 1e-6)) / 2e-6
  assert abs(_d - ROOT(_f(_t))) < 1e-5, "each one really does solve the equation"
 assert _f(0.0) == 0.0, "and every one of them passes through the origin"
BAD = [(x, ROOT(x) / x) for x in (0.1, 0.01, 0.001, 0.0001)]
assert all(abs(q - 2.0 / math.sqrt(x)) < 1e-9 for x, q in BAD)
assert BAD[-1][1] > 30 * BAD[0][1], "no constant b can hold the quotient down"

# ── beat 9: the configuration Lemma 1.1 rules out ─────────────────────
SPLIT = 0.55


def g2(t):
 return math.tan(t) if t <= SPLIT else math.tan(t) + 3.0 * (t - SPLIT) ** 2


G2_T = 0.80
G2_D = (g2(G2_T + 1e-6) - g2(G2_T - 1e-6)) / 2e-6
G2_RES = G2_D - F(g2(G2_T))
assert abs(G2_RES) > 0.8, \
    "the split branch is not a solution, which is exactly why the picture is crossed out"


class AdvCalcE74Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 74

 MODE_LABEL = {
  0: {"zh": "第 6 章開場：要解的是什麼", "en": "chapter 6 opens: what is to be solved"},
  1: {"zh": "真正的假設是 Lipschitz", "en": "the hypothesis that does the work"},
  2: {"zh": "少了它，唯一性就沒了", "en": "without it, uniqueness is gone"},
  3: {"zh": "定理 1.1", "en": "theorem 1.1"},
  4: {"zh": "換舞台：積分方程", "en": "changing the stage"},
  5: {"zh": "解 = K 的不動點", "en": "a solution is a fixed point"},
  6: {"zh": "估計一：球心移動多遠", "en": "first estimate: the centre"},
  7: {"zh": "估計二：K 是壓縮", "en": "second estimate: K contracts"},
  8: {"zh": "兩個條件合成 δ 的上限", "en": "the two conditions, combined"},
  9: {"zh": "引理 1.1", "en": "lemma 1.1"},
  10: {"zh": "定理 1.2，與下一集", "en": "theorem 1.2, and what comes next"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.86, dy=0.34, size=FS_TAG - 2):
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

 def _legend(self, x, rows, y0=1.14, dy=0.27, lw=1.30):
  g = VGroup()
  for k, (col, lab, w) in enumerate(rows):
   y = y0 - k * dy
   g.add(Line([x, y, 0], [x + 0.24, y, 0], color=col, stroke_width=6.0),
         self._sym(y, lab, col, FS_TAG - 3, x=x + 0.36 + w / 2, w=w))
  return g

 # ── beat 0: the equation, and one solution through one point ──────
 def _setup(self):
  ox, oy, sx, sy = -4.05, 0.02, 1.72, 0.68
  g = VGroup(self._arr([ox - 2.00, oy, 0], [ox + 2.04, oy, 0], DIM, sw=3, tl=0.14),
             self._arr([ox, oy - 0.86, 0], [ox, oy + 0.90, 0], DIM, sw=3, tl=0.14),
             self._sym(oy - 0.22, "t", DIM, FS_TAG - 2, x=ox + 2.20, w=0.34),
             self._sym(oy + 1.06, "α", DIM, FS_TAG - 2, x=ox - 0.16, w=0.34))
  for i in range(5):
   tt = -0.8 + 0.4 * i
   for j in range(5):
    x = -0.8 + 0.4 * j
    if abs(tt) < 0.01 and abs(x) < 0.01:
     continue
    dt, dx = 1.0, F(x)
    n = math.hypot(dt * sx, dx * sy)
    ux, uy = 0.15 * dt * sx / n, 0.15 * dx * sy / n
    g.add(Line([ox + sx * tt - ux, oy + sy * x - uy, 0],
               [ox + sx * tt + ux, oy + sy * x + uy, 0], color=DIM, stroke_width=1.8))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_B, t0=-EXIT, t1=EXIT, sw=4.0))
  g.add(Dot([ox, oy, 0], radius=0.070, color=ACCENT_A))
  g.add(self._sym(oy - 0.84, "( t ₀ , α ₀ )", ACCENT_A, FS_TAG - 3, x=ox + 0.62, w=1.20))
  g.add(self._table((("d α / d t   =   F ( t , α )", ACCENT_A),
                     ("f : J → A   ,     J ⊂ I", ACCENT_B),
                     ("f ′ ( t )   =   F ( t , f ( t ) )", ACCENT_B),
                     ("f ( t ₀ )   =   α ₀", ACCENT_C),
                     ("F ( t , α )  =  1 + α ²        f ( t )  =  tan t", DIM)),
                    y0=0.76, dy=0.36))
  g.add(self._cap("藍線是這一集從頭用到尾的那一條解",
                  "the blue curve is the one solution this whole episode follows"))
  return g.add(self._foot("第 6 章從初始值問題開始：給了 ⟨ t ₀ , α ₀ ⟩，方程 d α / d t = F ( t , α ) 有沒有解通過它、唯不唯一",
                          "chapter 6 starts with the initial-value problem: given a point, does the equation have a solution through it, and only one",
                          ACCENT_A,
                          "短線是 F 給出的方向場，藍線是真的解。注意它爬得多快，很快就衝出圖上這一塊——這正是接下來只能保證「局部」的原因",
                          "the short strokes are the direction field F prescribes and the curve is the actual solution; it leaves the box quickly, which is why only a local statement is coming"))

 # ── beat 1: the Lipschitz condition, read off the graph ───────────
 def _lipschitz(self):
  ox, oy, sx, sy = -5.95, -0.60, 1.85, 0.56
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.92, oy, 0], DIM, sw=3, tl=0.14),
             Line([ox + 1.85, oy - 0.10, 0], [ox + 1.85, oy + 1.32, 0],
                  color=DIM, stroke_width=1.3))
  g.add(self._fcurve(ox + 1.85, oy, sx, sy, F, ACCENT_B, t0=-1.0, t1=1.0, sw=2.6))
  xi, eta = 0.85, 0.15
  px, py = ox + 1.85 + sx * xi, oy + sy * F(xi)
  qx, qy = ox + 1.85 + sx * eta, oy + sy * F(eta)
  g.add(Line([qx, qy, 0], [px, py, 0], color=WARN, stroke_width=2.6))
  g.add(Dot([px, py, 0], radius=0.055, color=ACCENT_A), Dot([qx, qy, 0], radius=0.055, color=ACCENT_A))
  g.add(self._dash([qx, oy, 0], [qx, qy, 0], DIM, n=8, sw=1.2),
        self._dash([px, oy, 0], [px, py, 0], DIM, n=10, sw=1.2))
  g.add(self._sym(oy - 0.24, "η", ACCENT_A, FS_TAG - 3, x=qx, w=0.34),
        self._sym(oy - 0.24, "ξ", ACCENT_A, FS_TAG - 3, x=px, w=0.34))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "F ( t , · )", 1.00),
                                 (WARN, "( F ξ − F η ) / ( ξ − η )", 2.10)), y0=1.14))
  g.add(self._table((("        ξ            η          | F ξ − F η | / | ξ − η |", DIM),)
                    + tuple((f"    {a:+.2f}     {b:+.2f}              {q:.4f}", ACCENT_B)
                            for a, b, q in QUO[:5])
                    + ((f"                                      b   =   {C_SUP:.4f}", ACCENT_A),),
                    y0=0.94, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("右欄沒有一列超過最底下那個 b",
                  "no row of the last column is above the b underneath it"))
  return g.add(self._foot("局部一致 Lipschitz：每一點附近有一個常數 b，讓 ‖ F ( t , ξ ) − F ( t , η ) ‖ ≤ b ‖ ξ − η ‖，而且同一個 b 對附近每個 t 都成立",
                          "locally uniformly Lipschitz: near each point one constant b bounds the difference of the values by b times the distance, with the same b for every nearby t",
                          ACCENT_A,
                          "圖上是割線的斜率。這個 F 的割線斜率剛好是 ξ + η，在半徑一的球上不會超過 2——所以 b = 2。F 的二階偏微分連續加上均值定理，一般也給出這個條件",
                          "on the graph it is the slope of a chord; for this F that slope is xi plus eta, never above two on the ball of radius one, so b is two. A continuous second differential gives the condition in general"))

 # ── beat 2: drop the condition and uniqueness goes ────────────────
 def _counter(self):
  ox, oy, sx, sy = -5.95, -0.66, 3.30, 1.20
  g = VGroup(self._frame(ox, oy, 3.52, 1.46, down=0.10))
  for a, col in zip(LIFT_A, (ACCENT_B, ACCENT_C, WARN, ACCENT_A)):
   g.add(self._fcurve(ox, oy, sx, sy, lift(a), col, t0=0.0, t1=1.0, n=160, sw=2.4))
  g.add(Dot([ox, oy, 0], radius=0.065, color=ACCENT_A))
  g.add(self._sym(oy + 1.62, "x ′  =  2 √ | x |   ,   x ( 0 )  =  0", ACCENT_A,
                  FS_TAG - 2, x=ox + 1.76, w=3.40))
  g.add(self._table((("        ξ                  2 √ ξ  /  ξ", DIM),)
                    + tuple((f"     {x:.4f}                {q:10.4f}", WARN)
                            for x, q in BAD)
                    + (("      x  ≡  0    ,     x  =  ( t − a ) ²", ACCENT_B),),
                    y0=0.90, dy=0.28, size=FS_TAG - 3))
  g.add(self._cap("右欄一直往上，沒有 b 攔得住",
                  "the column climbs without limit, so no b can hold it"))
  return g.add(self._foot("這個 F 到處連續，可是過原點的解有無限多條：沿著零軸走任意久，再翹起來成拋物線，每一條都真的滿足方程",
                          "this F is continuous everywhere, yet infinitely many solutions pass through the origin: run along zero as long as you like, then lift off as a parabola",
                          WARN,
                          "垮掉的正是 Lipschitz。商 2 √ ξ 除以 ξ 在原點附近衝上無窮大，所以定理 1.1 的假設不是裝飾，是唯一性唯一的來源",
                          "what fails is exactly the Lipschitz condition: the quotient blows up at the origin, so the hypothesis of Theorem 1.1 is not decoration but the sole source of uniqueness"))

 # ── beat 3: the statement ─────────────────────────────────────────
 def _theorem(self):
  # L is ours to choose, so take it small enough that J is a visible third of it
  ox, oy, sx, sy, LH = -4.05, 0.02, 2.55, 0.66, 0.60
  g = VGroup(self._arr([ox - 2.00, oy, 0], [ox + 2.04, oy, 0], DIM, sw=3, tl=0.14),
             self._arr([ox, oy - 0.88, 0], [ox, oy + 0.92, 0], DIM, sw=3, tl=0.14))
  for s in (1, -1):
   g.add(self._dash([ox - sx * LH, oy + s * sy * 0.95, 0],
                    [ox + sx * LH, oy + s * sy * 0.95, 0], ACCENT_B, n=22, sw=1.5))
   g.add(self._dash([ox + s * sx * LH, oy - sy * 0.95, 0],
                    [ox + s * sx * LH, oy + sy * 0.95, 0], DIM, n=11, sw=1.4))
   g.add(Line([ox + s * sx * DELTA, oy - sy * 0.95, 0],
              [ox + s * sx * DELTA, oy + sy * 0.95, 0], color=ACCENT_C, stroke_width=2.4))
  g.add(self._sym(oy - 0.84, "L", DIM, FS_TAG - 3, x=ox + sx * LH, w=0.36),
        self._sym(oy - 0.84, "J", ACCENT_C, FS_TAG - 3, x=ox + sx * DELTA, w=0.36),
        self._sym(oy + sy * 0.95 + 0.20, "U", ACCENT_B, FS_TAG - 3, x=ox - sx * LH + 0.24, w=0.36))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_A, t0=-DELTA, t1=DELTA, sw=4.2))
  g.add(Dot([ox, oy, 0], radius=0.070, color=ACCENT_A))
  g.add(self._table((("A ⊂ W   ,     I ⊂ ℝ", ACCENT_B),
                     ("F : I × A → W", ACCENT_B),
                     ("‖ F ( t , ξ ) − F ( t , η ) ‖  ≤  b ‖ ξ − η ‖", ACCENT_C),
                     ("⇒     ∃ !   f : J → U", ACCENT_A),
                     ("f ′ = F ( t , f )   ,    f ( t ₀ ) = α ₀", ACCENT_A)),
                    y0=0.78, dy=0.36, size=FS_TAG - 2))
  g.add(self._cap("結論那兩列的重點是驚嘆號", "the point of the last two rows is the exclamation mark"))
  return g.add(self._foot("定理 1.1：A 是 Banach 空間 W 的開集、I 是開區間、F 連續且對第二個變數局部一致 Lipschitz，那麼過每一點恰有一條解",
                          "theorem 1.1: with A open in a Banach space, I an open interval, and F continuous and locally uniformly Lipschitz in its second variable, exactly one solution passes through each point",
                          ACCENT_A,
                          "注意兩個「小」：解只保證活在小區間 J 上，而且只保證落在小鄰域 U 裡。後面那個限制會被引理 1.1 拆掉，前面那個拆不掉",
                          "note the two smallnesses: the solution is promised only on a small interval and only inside a small neighbourhood; Lemma 1.1 will remove the second, and nothing removes the first"))

 # ── beat 4: the change of stage ───────────────────────────────────
 def _integral(self):
  ox, oy, sx, sy = -5.95, -0.66, 3.05, 0.46
  g = VGroup(self._frame(ox, oy, 3.26, 1.48, down=0.10))
  n = 60
  for k in range(n):
   s0 = INT_T * k / n
   g.add(Line([ox + sx * s0, oy, 0], [ox + sx * s0, oy + sy * F(math.tan(s0)), 0],
              color=ACCENT_C, stroke_width=1.6))
  g.add(self._fcurve(ox, oy, sx, sy, lambda s: F(math.tan(s)), ACCENT_B, t0=0.0, t1=0.95, sw=2.6))
  g.add(self._fcurve(ox, oy, sx, sy * 0.62, math.tan, ACCENT_A, t0=0.0, t1=0.95, sw=2.6))
  g.add(self._dash([ox + sx * INT_T, oy, 0], [ox + sx * INT_T, oy + 1.38, 0], DIM, n=11, sw=1.3))
  g.add(self._sym(oy - 0.26, "t", DIM, FS_TAG - 3, x=ox + sx * INT_T, w=0.34))
  hy = oy + sy * 0.62 * math.tan(INT_T)
  g.add(Dot([ox + sx * INT_T, hy, 0], radius=0.062, color=ACCENT_A),
        self._dash([ox, hy, 0], [ox + sx * INT_T, hy, 0], ACCENT_A, n=16, sw=1.3))
  g.add(self._legend(ox + 0.08, ((ACCENT_B, "F ( s , f ( s ) )", 1.40),
                                 (ACCENT_A, "f", 0.40)), y0=1.14))
  g.add(self._table((("f ( t )   =   α ₀  +  ∫ F ( s , f ( s ) ) d s", ACCENT_A),
                     (f"       t                     =    {INT_T:.4f}", DIM),
                     (f"       ∫ F ( s , f ( s ) ) d s     =    {INT_A:.9f}", ACCENT_C),
                     (f"       f ( t )                 =    {math.tan(INT_T):.9f}", ACCENT_A),
                     ("f  ∈  𝒞 ( J , W )", ACCENT_B)),
                    y0=0.84, dy=0.34, size=FS_TAG - 3))
  g.add(self._cap("那兩個 0.842288380 是分開算出來的",
                  "those two numbers were computed separately"))
  return g.add(self._foot("從 t ₀ 積到 t，「f 可微而且滿足方程」就等價於「f 連續而且滿足這條積分式」；反過來由微積分基本定理",
                          "integrating from t zero to t, being a differentiable solution is the same as being a continuous function satisfying the integral equation, and back again by the fundamental theorem",
                          ACCENT_A,
                          "換舞台的好處全在這裡：積分式只要求連續，而有界連續函數的空間是完備的，第 4 章的不動點定理才有地方站",
                          "that is the whole gain: the integral form asks only for continuity, and the bounded continuous functions form a complete space, which is where the fixed-point theorem can stand"))

 # ── beat 5: a solution is a fixed point, and the iteration finds it ─
 def _picard(self):
  ox, oy, sx, sy = -5.95, -0.68, 3.30, 0.82
  g = VGroup(self._frame(ox, oy, 3.52, 1.50, down=0.10))
  for k in range(1, 5):
   g.add(self._curve([[ox + sx * GRID[j], oy + sy * ITER[k][j], 0]
                      for j in range(0, NG, 4)],
                     (WARN, ACCENT_C, ACCENT_B, DIM)[k - 1], sw=2.6))
  g.add(self._curve([[ox + sx * GRID[j], oy + sy * TRUE[j], 0] for j in range(0, NG, 4)],
                    ACCENT_A, sw=3.0))
  g.add(self._dash([ox + sx * D_BALL, oy, 0], [ox + sx * D_BALL, oy + 1.40, 0],
                   ACCENT_A, n=12, sw=1.3))
  g.add(self._sym(oy + 1.62, "δ  <  0.25", ACCENT_A, FS_TAG - 3, x=ox + sx * D_BALL, w=1.30))
  g.add(self._table((("        n         ‖ f ₙ − f ‖ ∞", DIM),)
                    + tuple((f"       {k:2d}            {ERR[k]:.7f}", ACCENT_B)
                            for k in (1, 2, 3, 5, 7))
                    + (("K f  =  f          f ₙ ₊ ₁  =  K f ₙ", ACCENT_A),),
                    y0=0.94, dy=0.26, size=FS_TAG - 3))
  g.add(self._cap("右欄每一列都比上一列小", "each row of the column is below the one above"))
  return g.add(self._foot("定義 K 把 f 送到 α ₀ 加上那個積分，那麼「f 是解」就正好是「K f = f」——問題變成找 K 的不動點",
                          "define K by sending f to alpha zero plus that integral, and being a solution is exactly being a fixed point of K",
                          ACCENT_A,
                          "圖上是從常數零出發的 Picard 迭代：t，然後 t 加三分之一 t 的三次方，一路壓向橘線 tan t。虛線左邊才是定理保證的範圍，圖畫得比它遠是為了看得見",
                          "the picture is the Picard iteration from the constant zero, climbing towards tan; only the part left of the dashed line is what the theorem guarantees, and the plot runs further only to be legible"))

 # ── beat 6: how far K moves the centre ────────────────────────────
 def _centre(self):
  ox, oy, sx, sy = -4.00, -0.30, 5.40, 1.90
  g = VGroup(self._arr([ox - 1.90, oy, 0], [ox + 1.94, oy, 0], DIM, sw=3, tl=0.14),
             self._arr([ox, oy - 0.50, 0], [ox, oy + 0.96, 0], DIM, sw=3, tl=0.14))
  g.add(self._dash([ox - sx * DELTA, oy - 0.44, 0], [ox - sx * DELTA, oy + 0.86, 0],
                   DIM, n=9, sw=1.3),
        self._dash([ox + sx * DELTA, oy - 0.44, 0], [ox + sx * DELTA, oy + 0.86, 0],
                   DIM, n=9, sw=1.3))
  for s in (1, -1):
   g.add(self._dash([ox - sx * DELTA, oy + s * sy * DELTA * M_BD, 0],
                    [ox + sx * DELTA, oy + s * sy * DELTA * M_BD, 0], WARN, n=18, sw=1.4))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: t, ACCENT_B, t0=-DELTA, t1=DELTA, sw=3.0))
  g.add(Dot([ox, oy, 0], radius=0.060, color=ACCENT_A))
  g.add(self._sym(oy + sy * DELTA * M_BD + 0.18, "δ m", WARN, FS_TAG - 3,
                  x=ox - sx * DELTA + 0.44, w=0.70))
  g.add(self._sym(oy - 0.62, "δ", DIM, FS_TAG - 3, x=ox + sx * DELTA, w=0.34))
  g.add(self._table((("        δ        ‖ K ᾱ ₀ − ᾱ ₀ ‖ ∞        δ m", DIM),)
                    + tuple((f"      {d:.2f}            {act:.4f}           {bnd:.4f}",
                             ACCENT_B) for d, act, bnd in CEN)
                    + ((f"      m   =   {M_BD:.4f}", ACCENT_A),),
                    y0=0.86, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("中欄每一列都在右欄底下", "the middle column stays under the right one")) 
  return g.add(self._foot("第一個估計：K 作用在常數函數 α ₀ 上，跑不出 δ m。因為被積的東西不超過 m，而積分的長度只有 δ",
                          "first estimate: K applied to the constant function alpha zero moves it by at most delta times m, because the integrand is bounded by m over an interval of length delta",
                          ACCENT_A,
                          "藍線是 K 作用在常數零上，這裡剛好是 t；紅虛線是 δ m 這條界。要 K 把球打回球內，就要這個位移小到讓壓縮後的球還裝得下",
                          "the blue line is K applied to the constant zero, here just t, and the dashed lines are the bound; for K to map the ball into itself this displacement must leave room for the contracted ball"))

 # ── beat 7: K is a contraction ────────────────────────────────────
 def _contract(self):
  # one vertical scale for both panels, or the shrinking cannot be read off
  ox, oy, sv = -5.90, -0.62, 1.50
  g = VGroup(self._frame(ox, oy, 3.46, 1.50, down=0.10))
  u, v = PAIRS[0]
  for val, col in ((u, ACCENT_B), (v, ACCENT_C)):
   g.add(Line([ox + 0.06, oy + sv * val, 0], [ox + 1.20, oy + sv * val, 0],
              color=col, stroke_width=2.8))
   g.add(self._fcurve(ox + 1.98, oy, 6.40, sv, lambda s, val=val: F(val) * s, col,
                      t0=0.0, t1=DELTA, sw=2.8))
  for x0, a, b, col in ((ox + 1.32, u, v, DIM), (ox + 3.36, F(u) * DELTA, F(v) * DELTA, DIM)):
   g.add(self._arr([x0, oy + sv * a, 0], [x0, oy + sv * b, 0], col, sw=3, tl=0.12),
         self._arr([x0, oy + sv * b, 0], [x0, oy + sv * a, 0], col, sw=3, tl=0.12))
  g.add(self._arr([ox + 1.50, oy + 0.28, 0], [ox + 1.90, oy + 0.28, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._sym(oy + 0.50, "K", ACCENT_A, FS_TAG - 3, x=ox + 1.70, w=0.40))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "f ₁", 0.44), (ACCENT_C, "f ₂", 0.44)), y0=1.14))
  g.add(self._table((("     f ₁      f ₂     ‖ K f ₁ − K f ₂ ‖    ÷ ‖ f ₁ − f ₂ ‖", DIM),)
                    + tuple((f"   {a:.2f}   {b:.2f}        {img:.5f}          {q:.4f}",
                             ACCENT_B) for a, b, _d, img, q, _bd in CON)
                    + ((f"                                        δ c  =  {CONTR:.4f}", ACCENT_A),),
                    y0=0.86, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("左邊那段間距，右邊只剩五分之一不到",
                  "the gap on the left comes back on the right cut to under a fifth"))
  return g.add(self._foot("第二個估計：兩個函數餵進 K，差被 Lipschitz 常數 c 控制，所以 ‖ K f ₁ − K f ₂ ‖ ∞ ≤ δ c ‖ f ₁ − f ₂ ‖ ∞",
                          "second estimate: feeding two functions into K, the Lipschitz constant holds the difference down, so K shrinks distances by delta times c",
                          ACCENT_A,
                          "例子裡 c = 2、δ = 0.2，壓縮常數就是 0.4。表上最後一列兩個常數幾乎相等，商逼到 0.3960——這說明這個估計不是隨手放寬的",
                          "here c is two and delta one fifth, so the constant is two fifths; the last row takes two nearly equal constants and the quotient climbs to 0.3960, so the estimate is not slack"))

 # ── beat 8: the two conditions, and what they cost ────────────────
 def _delta(self):
  ox, oy, sx, sy = -5.90, -0.66, 5.60, 1.10
  g = VGroup(self._frame(ox, oy, 3.48, 1.50, down=0.10))
  assert abs(C_SUP - M_BD) < 1e-12, \
      "in this example the two happen to coincide, so they are drawn as one line"
  g.add(self._fcurve(ox, oy, sx, sy, lambda d: d * C_SUP, ACCENT_B, t0=0.0, t1=0.60, sw=3.0))
  g.add(self._fcurve(ox, oy, sx, sy, lambda d: (1.0 - d * C_SUP) * R, WARN,
                     t0=0.0, t1=0.60, sw=3.0))
  g.add(self._dash([ox, oy + sy * 1.0, 0], [ox + sx * 0.60, oy + sy * 1.0, 0], DIM, n=18, sw=1.2))
  for d, col in ((D_BALL, ACCENT_A), (D_CONTR, DIM)):
   g.add(self._dash([ox + sx * d, oy, 0], [ox + sx * d, oy + 1.20, 0], col, n=10, sw=1.4),
         self._sym(oy - 0.26, f"{d:.2f}", col, FS_TAG - 3, x=ox + sx * d, w=0.56))
  g.add(self._legend(ox + 0.06, ((ACCENT_B, "δ c  =  δ m", 1.10),
                                 (WARN, "( 1 − δ c ) r", 1.30)), y0=1.14))
  g.add(self._table((("δ c  <  1                ⇒     δ  <  0.5000", ACCENT_C),
                     ("δ m  <  ( 1 − δ c ) r      ⇒     δ  <  0.2500", ACCENT_B),
                     (f"δ  <  r / ( m + c r )   =   {D_BALL:.4f}", ACCENT_A),
                     (f"π / 2                     =   {BLOW:.4f}", DIM),
                     (f"( π / 2 )  /  {D_BALL:.2f}          =   {RATIO:.4f}   =   2 π", WARN)),
                    y0=0.82, dy=0.34, size=FS_TAG - 2))
  g.add(self._cap("藍線鑽到紅線底下的那一段，才是可以用的 δ",
                  "the usable deltas are where the blue line runs under the red one"))
  return g.add(self._foot("兩個要求疊起來：δ c 要小於一，δ m 要小於 ( 1 − δ c ) r，合起來正好是 δ < r / ( m + c r )，然後套第 4 章定理 9.1 的推論",
                          "the two demands stack into delta below r over m plus c r, and then a corollary of the chapter 4 fixed-point theorem finishes it",
                          ACCENT_A,
                          "這個例子的 m 與 c 剛好都是 2，所以 δ c 與 δ m 是同一條線，只畫一條。代價也看得見：保證的區間 0.25 對真正的 π / 2，差了整整 2 π 倍",
                          "here m and c both happen to be two, so the first two lines coincide and only one is drawn; the price shows too, a quarter against the true half of pi, short by a factor of two pi"))

 # ── beat 9: the configuration Lemma 1.1 forbids ───────────────────
 def _lemma(self):
  ox, oy, sx, sy = -5.95, -0.60, 2.55, 0.62
  g = VGroup()
  for dx, sp, col, bad in ((0.0, True, WARN, True), (2.95, False, ACCENT_B, False)):
   bx = ox + dx
   g.add(self._frame(bx, oy, 2.66, 1.44, down=0.10))
   g.add(self._fcurve(bx, oy, sx, sy, math.tan, ACCENT_A, t0=0.0, t1=0.95, sw=2.8))
   if sp:
    g.add(self._fcurve(bx, oy, sx, sy, g2, col, t0=0.0, t1=0.95, sw=2.8))
    g.add(self._dash([bx + sx * SPLIT, oy, 0], [bx + sx * SPLIT, oy + 1.34, 0],
                     ACCENT_C, n=11, sw=1.4))
    g.add(self._sym(oy - 0.26, "x", ACCENT_C, FS_TAG - 3, x=bx + sx * SPLIT, w=0.34))
   if bad:
    cx, cy = bx + sx * 0.86, oy + sy * g2(0.86) + 0.26
    g.add(Line([cx - 0.19, cy - 0.19, 0], [cx + 0.19, cy + 0.19, 0], color=WARN, stroke_width=3.6),
          Line([cx - 0.19, cy + 0.19, 0], [cx + 0.19, cy - 0.19, 0], color=WARN, stroke_width=3.6))
  g.add(self._sym(oy + 1.60, "g ₁  ≠  g ₂", WARN, FS_TAG - 3, x=ox + 1.30, w=1.40),
        self._sym(oy + 1.60, "g ₁  =  g ₂", ACCENT_B, FS_TAG - 3, x=ox + 4.25, w=1.40))
  g.add(self._table((("C  =  { t > t ₀  :  g ₁ ( t ) ≠ g ₂ ( t ) }", ACCENT_A),
                     (f"x   =   glb C   =   {SPLIT:.4f}", ACCENT_C),
                     ("x  ∉  C        ⇒        g ₁ ( x )  =  g ₂ ( x )", ACCENT_B),
                     (f"g ₂ ′ − ( 1 + g ₂ ² )   =   {G2_RES:+.4f}", WARN),
                     ("⇒     g ₁  =  g ₂     |     J ₁ ∩ J ₂", ACCENT_A)),
                    y0=0.82, dy=0.34, size=FS_TAG - 3))
  g.add(self._cap("倒數第二列不是零，右邊那張才是真的",
                  "the fourth row is not zero, which is why only the right picture survives"))
  return g.add(self._foot("引理 1.1：過同一點的兩個解，在定義域的交集上一定相等。取 C 為兩者相異的那些 t，令 x 為下確界；C 是開的，所以在 x 兩者相等",
                          "lemma 1.1: two solutions through the same point agree on the intersection of their domains; let x be the greatest lower bound of the set where they differ, which is open, so they agree at x",
                          ACCENT_A,
                          "接著對 ⟨ x , α ⟩ 再用一次定理 1.1：x 右邊一小段上只能有一條解，兩者在那裡就相等，與 x 是下確界矛盾。左圖被打叉，是因為那條分岔根本不滿足方程",
                          "then Theorem 1.1 at that point forces them to agree just to its right, contradicting the bound; the left picture is crossed out because the branching curve does not satisfy the equation at all"))

 # ── beat 10: dropping the restriction on the range ────────────────
 def _global(self):
  ox, oy, sx, sy = -4.05, -0.40, 2.60, 0.72
  g = VGroup(self._arr([ox - 0.16, oy, 0], [ox + 3.10, oy, 0], DIM, sw=3, tl=0.14),
             Line([ox, oy - 0.34, 0], [ox, oy + 1.48, 0], color=DIM, stroke_width=1.3))
  g.add(self._dash([ox, oy + sy * R, 0], [ox + 2.94, oy + sy * R, 0], DIM, n=22, sw=1.4))
  g.add(self._sym(oy + sy * R + 0.20, "U", DIM, FS_TAG - 3, x=ox + 2.62, w=0.36))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_B, t0=0.0, t1=EXIT, sw=3.6))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_A, t0=EXIT, t1=1.00, sw=3.6))
  g.add(self._dash([ox + sx * EXIT, oy, 0], [ox + sx * EXIT, oy + sy * R, 0], DIM, n=9, sw=1.3))
  g.add(self._sym(oy - 0.26, f"{EXIT:.4f}", DIM, FS_TAG - 3, x=ox + sx * EXIT, w=0.80))
  g.add(Dot([ox, oy, 0], radius=0.060, color=ACCENT_A))
  g.add(self._legend(ox + 0.10, ((ACCENT_B, "f : J → U", 1.10),
                                 (ACCENT_A, "f : J → A", 1.10)), y0=1.14))
  g.add(self._table(((f"tan ( π / 4 )   =   {math.tan(EXIT):.4f}   =   r", ACCENT_C),
                     ("f : J → U", ACCENT_C),
                     ("g ₁  =  g ₂     |     J ₁ ∩ J ₂", ACCENT_B),
                     ("∃ !   f : J → A", ACCENT_A),
                     ("J  ⊂  I     ,     f [ J ]  ⊂  A", DIM)),
                    y0=0.80, dy=0.36, size=FS_TAG - 2))
  g.add(self._cap("青線變橘線的地方就是那個限制沒了",
                  "where the curve changes colour is where the restriction goes"))
  return g.add(self._foot("定理 1.2：定理 1.1 只給出從 J 到小鄰域 U 的解，引理 1.1 說任何兩個解都相容，所以「落在 U 裡」不是真的限制",
                          "theorem 1.2: Theorem 1.1 promises a solution only into the small neighbourhood, but Lemma 1.1 says any two solutions are compatible, so landing in U is no real restriction",
                          ACCENT_A,
                          "這個例子在 π / 4 就離開 U，可是解一點事都沒有，照樣往前走。結論是：過每一點，在夠小的 J 上恰有一條從 J 到 A 的解",
                          "this solution leaves U at pi over four and carries on regardless; through each point there is exactly one solution from a small enough J into A"))

 def stage(self):
  a, b, c = self._setup(), self._lipschitz(), self._counter()
  d, e, f_ = self._theorem(), self._integral(), self._picard()
  h, i, j = self._centre(), self._contract(), self._delta()
  k, l = self._lemma(), self._global()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE74ZH, AdvCalcE74EN = make(AdvCalcE74Base, "74", prefix="AdvCalcE")
