"""advcalc E63 -- chapter 4, section 9, first part (book pp. 228-230): the
contraction mapping fixed-point theorem.

The book calls the theorem very simple and elegant, and it has three jobs: to
complete the implicit-function theorem here, to give existence and uniqueness
for differential equations in chapter 6, and to be set beside Newton's method.
This episode takes the theorem itself and its four corollaries, ending with
Theorem 9.3, where the implicit-function theorem is finally finished.  E64 picks
up Theorem 9.4, the iterative procedure, the comparison with Newton, and the
worked example in the plane.

Section 9's content runs to book page 234; 234 to 236 are exercises 9.1 to 9.13,
and by section 8 of the playbook they are not worked here.  The OUTLINE lists
the section as 228-236, which counts the exercise pages -- the sixth time that
column has done so.

Every number is computed from one concrete contraction, K(x) = 1 + sin(x)/2 on
the line, whose Lipschitz constant is exactly one half.  Its fixed point is
found by iteration rather than quoted; the Cauchy estimate is checked against
the measured gaps; the ball of Corollary 1 is checked to be carried into itself;
Corollary 3's bound is checked against the measured distance; and the
parametrized family K(s, x) = K(x) + s has its fixed point traced as s moves.
Beats 9 and 10 use a second concrete case, G = eta cubed plus eta minus xi,
where the whole mechanism of Theorem 9.3 can be watched with real numbers.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20

C = 0.5


def K(x):
 return 1.0 + C * math.sin(x)


# the Lipschitz constant is exactly C, since |K'| = C|cos|
_PTS = [k * 6.0 / 400 for k in range(0, 401, 4)]
LIP = max(abs(K(a) - K(b)) / abs(a - b)
          for i, a in enumerate(_PTS) for b in _PTS[i + 1:])
assert 0.4995 < LIP <= C, "a fine enough grid has to find the peak of the derivative"
assert LIP <= C + 1e-9, "the map has to be a contraction with the stated constant"

# the fixed point is iterated to, not quoted
ORBIT = [0.0]
for _ in range(24):
 ORBIT.append(K(ORBIT[-1]))
FIX = ORBIT[-1]
assert abs(K(FIX) - FIX) < 1e-12, "and the last iterate really is fixed"
assert 1.49 < FIX < 1.50, "the fixed point lands just under one and a half"

# beat 3: the measured gaps against C^n delta / (1 - C)
DELTA = abs(ORBIT[1] - ORBIT[0])
GAPS = [(n, abs(ORBIT[n + 1] - ORBIT[n]), C ** n * DELTA) for n in (1, 2, 3, 4)]
for _n, _got, _b in GAPS:
 assert _got > 0.0, "a zero gap would have no logarithm to plot"
for _n, _got, _bound in GAPS:
 assert _got <= _bound + 1e-12, "each gap has to respect C to the n times delta"
TAIL = [(n, abs(FIX - ORBIT[n]), C ** n * DELTA / (1.0 - C)) for n in (1, 2, 3, 4)]
for _n, _got, _bound in TAIL:
 assert _got <= _bound + 1e-12, "and the tail respects the geometric sum"

# beat 4 and 5: the ball is carried into itself
BALL_P, BALL_R = 0.0, 2.5
MOVED = abs(K(BALL_P) - BALL_P)
assert MOVED <= (1.0 - C) * BALL_R, "the center moves less than one minus C times r"
assert all(abs(K(BALL_P + BALL_R * (2 * k / 400.0 - 1))) <= BALL_R + 1e-12
           for k in range(401)), "so every point of the ball is sent back into it"
assert abs(FIX - BALL_P) <= BALL_R, "and the fixed point is inside"

# beat 6: Corollary 3's estimate against the measured distance
COR3_X = 0.0
COR3_D = abs(K(COR3_X) - COR3_X)
COR3_BOUND = COR3_D / (1.0 - C)
assert abs(COR3_X - FIX) <= COR3_BOUND + 1e-12, "x is within d over one minus C"
assert abs(COR3_X - FIX) > 0.7 * COR3_BOUND, "and here the estimate is fairly tight"


# beats 7 and 8: the fixed point as a continuous function of a parameter
def fix_of(s):
 x = 0.0
 for _ in range(60):
  x = K(x) + s
 return x


SVALS = [-0.6 + 1.2 * k / 6 for k in range(7)]
PS = [(s, fix_of(s)) for s in SVALS]
for (_s0, _p0), (_s1, _p1) in zip(PS, PS[1:]):
 assert _p1 > _p0, "the fixed point moves monotonically with the parameter here"
 assert abs(_p1 - _p0) <= abs(_s1 - _s0) / (1.0 - C) + 1e-9, \
     "and it moves by at most the parameter step over one minus C"


# beats 9 and 10: Theorem 9.3 on G(xi, eta) = eta^3 + eta - xi
def G(xi, eta):
 return eta ** 3 + eta - xi


# T = dG^2 at the origin is 1, so K(xi, eta) = eta - G = xi - eta^3
def K2(xi, eta):
 return xi - eta ** 3


def dK2(eta):
 return -3.0 * eta ** 2


assert abs(dK2(0.0)) < 1e-12, "the differential in the second variable dies at the origin"
NBALL = 0.4
assert abs(dK2(NBALL)) <= 0.5, "and stays under one half on the ball the proof picks"
assert abs(dK2(0.42)) > 0.5, "just outside it, the bound is already lost"

IMPL = []
for _xi in (0.1, 0.3, 0.5):
 _e = 0.0
 for _ in range(60):
  _e = K2(_xi, _e)
 IMPL.append((_xi, _e))
 assert abs(G(_xi, _e)) < 1e-12, "the fixed point solves G = 0, which is the point"
for (_a, _fa), (_b, _fb) in zip(IMPL, IMPL[1:]):
 assert _fb > _fa, "and the implicit function is increasing here"


class AdvCalcE63Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 63

 MODE_LABEL = {
  0: {"zh": "壓縮：Lipschitz 常數小於一", "en": "a contraction: Lipschitz constant under one"},
  1: {"zh": "至多一個不動點", "en": "at most one fixed point"},
  2: {"zh": "定理 9.1：反覆作用 K", "en": "Theorem 9.1: apply K over and over"},
  3: {"zh": "為什麼那一列是 Cauchy 的", "en": "why that sequence is Cauchy"},
  4: {"zh": "推論 1：球被送進自己", "en": "Corollary 1: the ball goes into itself"},
  5: {"zh": "C r 加上 ( 1 − C ) r 剛好是 r", "en": "C r plus one minus C times r is exactly r"},
  6: {"zh": "推論 3：離不動點有多遠", "en": "Corollary 3: how far the fixed point is"},
  7: {"zh": "帶參數的壓縮", "en": "a contraction with a parameter"},
  8: {"zh": "推論 4 與定理 9.2", "en": "Corollary 4, and Theorem 9.2"},
  9: {"zh": "定理 9.3：隱函數定理補完", "en": "Theorem 9.3: the implicit-function theorem"},
  10: {"zh": "一階項被消掉，才成為壓縮", "en": "killing the first-order term is what makes it a contraction"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _panel(self, rows, x=PANEL_X, w=PANEL_W):
  g = VGroup()
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=x, w=w))
  return g

 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.34, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plot(self, f, ox, oy, sx, sy, col, sw=2.4, n=240, x0=0.0, x1=1.0):
  return self._curve([[ox + sx * k / n, oy + sy * f(x0 + (x1 - x0) * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _definition(self):
  ox, oy = -5.90, -0.80
  sx, sy = 3.90, 0.86
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 2.42, 0], color=DIM, stroke_width=1.4))
  g.add(self._plot(lambda t: t, ox, oy, sx, sy, DIM, sw=1.6, x0=0.0, x1=2.4),
        self._plot(K, ox, oy, sx, sy, ACCENT_B, sw=2.6, x0=0.0, x1=2.4))
  # the cone of slope +-C about a point of the graph: nothing may leave it
  p = 0.70
  px, py = ox + sx * p / 2.4, oy + sy * K(p)
  for sgn in (1, -1):
   g.add(self._dash([px - 0.85, py - sgn * 0.85 * (sy / (sx / 2.4)) * C, 0],
                    [px + 0.85, py + sgn * 0.85 * (sy / (sx / 2.4)) * C, 0],
                    ACCENT_A, n=10, sw=1.1))
  g.add(Dot([px, py, 0], radius=0.055, color=ACCENT_A))
  g.add(self._table((("     K ( x )   =   1  +  sin ( x ) / 2", DIM),
                     (f"     C   =   {C:.2f}", ACCENT_B),
                     (f"     max  Δ K / Δ x   =   {LIP:.3f}", ACCENT_A)),
                    y0=0.84, dy=0.42))
  g.add(self._mid(-0.60, "灰色那條是 y = x，青色那條是 K",
                  "the grey line is y equal to x, and the teal curve is K", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("壓縮就是 Lipschitz 而且常數嚴格小於一——圖上任何一段割線的斜率都夾在那個楔形裡",
                          "a contraction is Lipschitz with constant strictly under one: every secant of the graph lies inside that wedge",
                          ACCENT_A,
                          "這一集所有的數字都是從這一個 K 算出來的，常數量到 0.500，跟理論值一樣",
                          "every number in this episode comes from this one K, whose constant measures 0.500, exactly the theoretical value"))

 def _unique(self):
  g = VGroup()
  rows = (("K x  =  x   ,   K y  =  y", ACCENT_B),
          ("ρ ( x , y )   =   ρ ( K x , K y )   ≤   C ρ ( x , y )", ACCENT_C),
          ("( 1 − C )  ρ ( x , y )      ≤      0", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.54, lab, col, FS_TAG, x=-3.40, w=5.40))
  g.add(self._dash([-5.90, -0.62, 0], [-0.90, -0.62, 0], DIM, n=24, sw=1.2))
  g.add(self._sym(-0.94, "C  <  1        ⇒        ρ ( x , y )  =  0", ACCENT_A,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._panel(((0.86, "兩個不動點的距離等於它們的像的距離",
                      "two fixed points are as far apart as their images", ACCENT_B),
                     (0.20, "可是像的距離最多只有 C 倍",
                      "but the images are at most C times as far apart", ACCENT_C),
                     (-0.46, "一減 C 是正的，所以距離只能是零",
                      "one minus C is positive, so that distance can only be zero", WARN))))
  return g.add(self._foot("這一段完全沒有用到完備性——唯一性是壓縮這個條件自己給的",
                          "completeness is nowhere in this argument: uniqueness comes from the contraction condition alone",
                          ACCENT_A,
                          "完備性是存在性才需要的，那要等下一拍把點造出來",
                          "completeness is what existence needs, and the next beat is where the point gets built"))

 def _cobweb(self):
  ox, oy = -5.90, -0.90
  sx, sy = 4.00, 0.88
  hi = 2.4
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 2.45, 0], color=DIM, stroke_width=1.4))
  g.add(self._plot(lambda t: t, ox, oy, sx, sy, DIM, sw=1.6, x0=0.0, x1=hi),
        self._plot(K, ox, oy, sx, sy, ACCENT_B, sw=2.4, x0=0.0, x1=hi))
  X = lambda v: ox + sx * v / hi
  Y = lambda v: oy + sy * v
  for i in range(5):
   a, b = ORBIT[i], ORBIT[i + 1]
   g.add(Line([X(a), Y(a), 0], [X(a), Y(b), 0], color=WARN, stroke_width=1.6),
         Line([X(a), Y(b), 0], [X(b), Y(b), 0], color=WARN, stroke_width=1.6))
  g.add(Dot([X(FIX), Y(FIX), 0], radius=0.07, color=ACCENT_A))
  g.add(self._table((("       n          x ₙ", DIM),)
                    + tuple((f"     {n:4d}          {ORBIT[n]:.4f}",
                             ACCENT_C if n < 6 else ACCENT_A)
                            for n in (0, 1, 2, 4, 8)), y0=0.86, dy=0.30))
  g.add(self._mid(-0.92, f"不動點是迭代出來的：{FIX:.4f}",
                  f"the fixed point was iterated to, not quoted: {FIX:.4f}", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("紅色那串階梯就是反覆作用 K：豎直走到曲線上，再水平走回 y = x",
                          "the red staircase is K applied over and over: up to the curve, then across to the line y equal to x",
                          ACCENT_A,
                          "存在性是造出來的，不是找出來的——完備性保證造出來的那一列真的有極限",
                          "existence is constructed rather than found, and completeness is what guarantees the constructed sequence has a limit"))

 def _cauchy(self):
  ox, oy = -5.85, -0.86
  sx, sy = 4.10, 1.90
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  lo = math.log10(GAPS[-1][1]) - 0.7
  hi = math.log10(GAPS[0][2])
  for rows, col, r in ((GAPS, WARN, 1), (GAPS, ACCENT_A, 2)):
   pts = []
   for k, (n, got, bound) in enumerate(rows):
    v = got if r == 1 else bound
    pts.append([ox + sx * k / (len(rows) - 1),
                oy + sy * (math.log10(v) - lo) / (hi - lo), 0])
   g.add(self._curve(pts, col, sw=1.8))
   for pt in pts:
    g.add(Dot(pt, radius=0.055, color=col))
  g.add(self._sym(oy + sy * 1.00, "C ⁿ δ", ACCENT_A, FS_TAG - 1, x=ox + 1.30, w=1.10))
  g.add(self._table((("       n        ρ ( x ₙ ₊ ₁ , x ₙ )        C ⁿ δ", DIM),)
                    + tuple((f"     {n:4d}            {got:.4f}           {bound:.4f}", ACCENT_C)
                            for n, got, bound in GAPS), y0=0.86, dy=0.34))
  g.add(self._mid(-0.86, "橘色是上界，紅色是實際量到的",
                  "orange is the bound and red is what was measured", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("相鄰兩項每走一步就縮小 C 倍，所以第 n 對的距離不超過 C 的 n 次方乘 δ",
                          "each step shrinks the gap by a factor of C, so the n-th gap is at most C to the n times delta",
                          ACCENT_A,
                          "這個上界對每一個 n 都成立，可是很鬆——實際的距離掉得比它快得多，因為這個 K 很平滑",
                          "the bound holds at every n but is generous: for a map this smooth the real gaps fall much faster than it does"))

 def _ball(self):
  ox, oy = -5.60, 0.30
  sx = 4.30
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.0))
  X = lambda v: ox + sx * (v + BALL_R) / (2 * BALL_R)
  g.add(self._dash([X(-BALL_R), oy - 0.30, 0], [X(-BALL_R), oy + 0.30, 0], ACCENT_B, n=6, sw=1.4),
        self._dash([X(BALL_R), oy - 0.30, 0], [X(BALL_R), oy + 0.30, 0], ACCENT_B, n=6, sw=1.4))
  g.add(Dot([X(BALL_P), oy, 0], radius=0.07, color=ACCENT_A),
        self._sym(oy + 0.34, "p", ACCENT_A, FS_TAG - 1, x=X(BALL_P), w=0.60))
  g.add(Dot([X(K(BALL_P)), oy, 0], radius=0.06, color=WARN),
        self._arr([X(BALL_P), oy - 0.22, 0], [X(K(BALL_P)), oy - 0.22, 0], WARN, sw=2.0, tl=0.10),
        self._sym(oy - 0.56, f"d  =  {MOVED:.2f}", WARN, FS_TAG - 1,
                  x=(X(BALL_P) + X(K(BALL_P))) / 2, w=1.40))
  g.add(Dot([X(FIX), oy, 0], radius=0.06, color=ACCENT_C),
        self._sym(oy + 0.34, "a", ACCENT_C, FS_TAG - 1, x=X(FIX), w=0.60))
  g.add(self._table((("     d   ≤   ( 1 − C ) r", DIM),
                     (f"     r   =   {BALL_R:.1f}", ACCENT_B),
                     (f"     ( 1 − C ) r   =   {(1 - C) * BALL_R:.2f}", ACCENT_A),
                     (f"     d   =   {MOVED:.2f}   ≤   {(1 - C) * BALL_R:.2f}", WARN)),
                    y0=0.86, dy=0.38))
  g.add(self._mid(-0.72, "球心移動得夠少，不動點就落在球裡",
                  "the center moves little enough, so the fixed point lands in the ball",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("實際遇到的映射常常只在某一點附近是壓縮，所以要先確認那個鄰域被送進自己",
                          "in practice a map is often a contraction only near a point, so the neighbourhood has to be checked to go into itself",
                          ACCENT_A,
                          "程式在球上取了四百零一個點，每一個的像都還在球裡",
                          "four hundred and one points of the ball were checked here, and every image is still inside it"))

 def _arith(self):
  ox, oy = -5.60, 0.36
  sx = 4.30
  g = VGroup()
  a = sx * C
  g.add(Line([ox, oy, 0], [ox + a, oy, 0], color=ACCENT_B, stroke_width=6),
        Line([ox + a, oy, 0], [ox + sx, oy, 0], color=WARN, stroke_width=6))
  for x0, lab, col, dy in ((ox + a / 2, "C r", ACCENT_B, 0.30),
                           (ox + a + (sx - a) / 2, "( 1 − C ) r", WARN, 0.30)):
   g.add(self._sym(oy + dy, lab, col, FS_TAG - 1, x=x0, w=1.60))
  g.add(self._dash([ox, oy - 0.34, 0], [ox + sx, oy - 0.34, 0], ACCENT_A, n=20, sw=1.4),
        self._sym(oy - 0.68, "r", ACCENT_A, FS_TAG, x=ox + sx / 2, w=0.80))
  g.add(self._panel(((0.86, "像到球心的距離：不超過 C 乘 r",
                      "from the image to the center's image: at most C times r", ACCENT_B),
                     (0.20, "球心自己移動：不超過 ( 1 − C ) r",
                      "and the center itself moves at most one minus C times r", WARN),
                     (-0.46, "兩段加起來剛好是 r，所以還在球裡",
                      "the two add to exactly r, so the image is still in the ball", ACCENT_A))))
  return g.add(self._foot("推論 2 是開球的版本：把「不超過」換成嚴格小於，縮到一個略小的閉球再引用推論 1",
                          "Corollary 2 is the open version: replace at most by strictly less, shrink to a slightly smaller closed ball, and quote Corollary 1",
                          ACCENT_A,
                          "整條推論就是這兩段的加法——沒有別的內容",
                          "the whole corollary is that one addition, and nothing else"))

 def _cor3(self):
  ox, oy = -5.60, 0.30
  sx = 4.30
  lo, hi = -0.4, 2.6
  X = lambda v: ox + sx * (v - lo) / (hi - lo)
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.0))
  g.add(Dot([X(COR3_X), oy, 0], radius=0.07, color=ACCENT_B),
        self._sym(oy + 0.32, "x", ACCENT_B, FS_TAG - 1, x=X(COR3_X), w=0.60),
        Dot([X(K(COR3_X)), oy, 0], radius=0.06, color=WARN),
        self._sym(oy + 0.32, "K x", WARN, FS_TAG - 1, x=X(K(COR3_X)), w=0.90),
        Dot([X(FIX), oy, 0], radius=0.07, color=ACCENT_A),
        self._sym(oy + 0.32, "a", ACCENT_A, FS_TAG - 1, x=X(FIX), w=0.60))
  g.add(self._arr([X(COR3_X), oy - 0.26, 0], [X(K(COR3_X)), oy - 0.26, 0], WARN, sw=2.0, tl=0.10),
        self._arr([X(COR3_X), oy - 0.68, 0], [X(COR3_X + COR3_BOUND), oy - 0.68, 0],
                  ACCENT_A, sw=2.0, tl=0.10))
  g.add(self._sym(oy - 0.50, f"d = {COR3_D:.2f}", WARN, FS_TAG - 2,
                  x=(X(COR3_X) + X(K(COR3_X))) / 2, w=1.30),
        self._sym(oy - 0.92, f"d / ( 1 − C ) = {COR3_BOUND:.2f}", ACCENT_A, FS_TAG - 2,
                  x=(X(COR3_X) + X(COR3_X + COR3_BOUND)) / 2, w=2.30))
  g.add(self._table((("     ρ ( x , a )", DIM),
                     (f"     =   {abs(COR3_X - FIX):.4f}", ACCENT_C),
                     (f"     ≤   {COR3_BOUND:.4f}", ACCENT_A)), y0=0.84, dy=0.40))
  g.add(self._mid(-0.72, "量到 1.4987，上界 2.0000——這一次很緊",
                  "measured 1.4987 against a bound of 2.0000, which is close here", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("推論 3：K 把 x 移動了 d，那麼 x 到不動點的距離不超過 d 除以一減 C",
                          "Corollary 3: if K moves x a distance d, then x is within d over one minus C of the fixed point",
                          ACCENT_A,
                          "做法是取一個以 x 為心、半徑 d 除以一減 C 的閉球，再套推論 1",
                          "the proof takes the closed ball of that radius about x and applies Corollary 1"))

 def _parameter(self):
  ox, oy = -5.85, -0.70
  sx, sy = 4.10, 1.55
  slo, shi = -0.7, 0.7
  plo, phi = 0.6, 2.5
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  pts = []
  for s, p in PS:
   px = ox + sx * (s - slo) / (shi - slo)
   py = oy + sy * (p - plo) / (phi - plo)
   pts.append([px, py, 0])
   g.add(Dot([px, py, 0], radius=0.055, color=ACCENT_C))
  g.add(self._curve(pts, ACCENT_C, sw=2.0))
  g.add(self._sym(oy + sy * 1.00, "s   ↦   p ₛ", ACCENT_A, FS_TAG - 1, x=ox + 1.20, w=1.60))
  g.add(self._table((("        s            p ₛ", DIM),)
                    + tuple((f"     {s:+.2f}         {p:.4f}", ACCENT_C)
                            for s, p in PS[::2]), y0=0.86, dy=0.34))
  g.add(self._mid(-0.86, "參數動，不動點跟著連續地動",
                  "move the parameter and the fixed point moves continuously with it",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("假設 K 對第二個變數是壓縮，而且那個常數對第一個變數的每一個值都通用",
                          "K is assumed to be a contraction in its second variable, with one constant that serves every value of the first",
                          ACCENT_A,
                          "程式驗過：參數走一步，不動點走的距離不超過那一步除以一減 C",
                          "it was checked here that a step in the parameter moves the fixed point by at most that step over one minus C"))

 def _cor4(self):
  g = VGroup()
  g.add(self._sym(0.78, "ρ ( K ( s , p ₜ ) , p ₜ )      ≤      ϵ", ACCENT_B,
                  FS_TAG, x=-3.40, w=5.40))
  g.add(self._arr([-3.40, 0.52, 0], [-3.40, 0.16, 0], ACCENT_A, sw=2.0, tl=0.10))
  g.add(self._sym(-0.06, "ρ ( p ₛ , p ₜ )      ≤      ϵ / ( 1 − C )", WARN,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._mid(-0.62, "所以 s 映到 p ₛ 是連續的", "so the map from s to its fixed point is continuous",
                  ACCENT_A, FS_TAG, x=-3.40, w=5.20))
  g.add(self._panel(((0.86, "參數動一點，K 就把舊的不動點移動一點",
                      "move the parameter a little and K moves the old fixed point a little",
                      ACCENT_B),
                     (0.20, "推論 3 立刻把它換成兩個不動點的距離",
                      "Corollary 3 turns that at once into a distance between fixed points",
                      ACCENT_C),
                     (-0.46, "推論 2 加推論 4 就是定理 9.2",
                      "Corollary 2 together with Corollary 4 is Theorem 9.2", WARN))))
  return g.add(self._foot("定理 9.2 才是後面真正拿來用的形式：球、參數、連續性三件事一次講完",
                          "Theorem 9.2 is the form actually used later: the ball, the parameter, and the continuity all in one statement",
                          ACCENT_A,
                          "第 6 章證常微分方程的存在唯一性時，用的也是這一條",
                          "chapter 6 uses this same statement when it proves existence and uniqueness for differential equations"))

 def _implicit(self):
  ox, oy = -5.85, -0.74
  sx, sy = 4.10, 1.70
  xlo, xhi = 0.0, 0.7
  ylo, yhi = 0.0, 0.55
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  pts = []
  for k in range(121):
   eta = ylo + (yhi - ylo) * k / 120
   xi = eta ** 3 + eta
   if xi > xhi:
    break
   pts.append([ox + sx * (xi - xlo) / (xhi - xlo),
               oy + sy * (eta - ylo) / (yhi - ylo), 0])
  g.add(self._curve(pts, ACCENT_B, sw=2.6))
  for xi, eta in IMPL:
   g.add(Dot([ox + sx * (xi - xlo) / (xhi - xlo),
              oy + sy * (eta - ylo) / (yhi - ylo), 0], radius=0.06, color=WARN))
  g.add(self._sym(oy + sy * 1.00, "G  =  0", ACCENT_B, FS_TAG - 1, x=ox + 1.30, w=1.40))
  g.add(self._table((("        ξ            F ( ξ )", DIM),)
                    + tuple((f"      {xi:.1f}          {eta:.4f}", ACCENT_C)
                            for xi, eta in IMPL), y0=0.86, dy=0.34))
  g.add(self._mid(-0.86, "紅點是迭代出來的，而且驗過 G 真的等於零",
                  "the red points were iterated to, and G was checked to vanish at each",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這裡取 G ( ξ , η ) = η ³ + η − ξ，T 是原點的第二偏微分，等於一",
                          "here G of xi and eta is eta cubed plus eta minus xi, and T, its second partial differential at the origin, is one",
                          ACCENT_A,
                          "於是 K ( ξ , η ) = ξ − η ³，而它的不動點正好就是 G 等於零的解",
                          "so K of xi and eta is xi minus eta cubed, and its fixed points are exactly the solutions of G equal to zero"))

 def _mechanism(self):
  ox, oy = -5.85, -0.20
  sx, sy = 4.10, 1.05
  elo, ehi = -0.5, 0.5
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._plot(lambda e: dK2(e), ox, oy, sx, sy, ACCENT_C, sw=2.4,
                   x0=elo, x1=ehi))
  g.add(self._dash([ox, oy - sy * 0.5, 0], [ox + sx * 1.06, oy - sy * 0.5, 0],
                   WARN, n=20, sw=1.3))
  for e in (-NBALL, NBALL):
   px = ox + sx * (e - elo) / (ehi - elo)
   g.add(self._dash([px, oy - sy * 0.72, 0], [px, oy + 0.16, 0], ACCENT_B, n=6, sw=1.2))
  g.add(Dot([ox + sx * (0.0 - elo) / (ehi - elo), oy, 0], radius=0.07, color=ACCENT_A))
  g.add(self._table((("     d K ²  =  − 3 η ²", DIM),
                     (f"     η  =  0        {abs(dK2(0.0)):.2f}", ACCENT_A),
                     (f"     η  =  {NBALL:.2f}     {dK2(NBALL):.3f}", ACCENT_B),
                     (f"     η  =  0.42     {dK2(0.42):.3f}", WARN)), y0=0.86, dy=0.36))
  g.add(self._mid(-0.86, "紅色虛線是 −1／2：青色那兩條之間才守得住",
                  "the red dashes are minus one half, and the bound holds only between the teal lines",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("K 對第二個變數的微分在原點正好是零——那就是「把一階項消掉」的意思",
                          "the differential of K in its second variable vanishes at the origin, which is what killing the first-order term means",
                          ACCENT_A,
                          "因為它連續，附近就有一個球讓範數不超過二分之一，均值定理再把 K 變成壓縮",
                          "being continuous, it stays under one half on a nearby ball, and the mean value theorem then makes K a contraction"))

 def stage(self):
  a, b, c = self._definition(), self._unique(), self._cobweb()
  d, e, f = self._cauchy(), self._ball(), self._arith()
  h, i, j = self._cor3(), self._parameter(), self._cor4()
  k, l = self._implicit(), self._mechanism()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE63ZH, AdvCalcE63EN = make(AdvCalcE63Base, "63", prefix="AdvCalcE")
