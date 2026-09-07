"""advcalc E64 -- chapter 4, section 9, second part (book pp. 231-234): Theorem
9.4, the iterative procedure, the comparison with Newton's method, and the
worked example in the plane.

E63 took the fixed-point theorem itself.  Here the theorem is pushed the other
way (Theorem 9.4: a differentiable contraction defines a differentiable implicit
function), and then the book makes the point that is easy to miss -- the proof
of the fixed-point theorem is not only an existence argument, it is an
*algorithm*.  Written out, the iteration subtracts one fixed inverse at every
step; Newton's method replaces that fixed inverse with the local one, converges
far faster, and pays for it by needing the inverses of infinitely many linear
transformations.  The section closes with the simplest possible inverse mapping
in the plane, where the iterates turn out to be computing Taylor expansions.

Section 9's content ends on book page 234; 234 to 236 are exercises 9.1 to 9.13,
and by section 8 of the playbook they are not worked here.

The book's Figures 4.4 and 4.5 sketch the two iterations.  Beats 3 and 4 draw
that idea from scratch: a single root-finding picture with its own curve,
staircase, labels and numbers, rather than the book's parametrized pair.

Everything numerical comes from one concrete case, G(y) = e^y - 1.3, whose root
is a logarithm.  Both iterations are run from the same start, so the tables are
the two methods on the same problem: the fixed-slope errors fall by a roughly
constant factor while Newton's square at every step.  The quadratic bound of
beat 7 is checked against the measured steps, and the plane example of beats 9
and 10 is iterated and then compared against the Taylor truncations the book
prints.
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

# ── the one concrete problem both methods are run on ───────────────────
# G has to be visibly curved over the plotted range, or the fixed-slope lines
# and the tangents draw the same picture and beats 3 and 4 say nothing.
START = 1.5


def G(y):
 return y * y + y - 0.6


def dG(y):
 return 2.0 * y + 1.0


D2G = 2.0
ROOT = (-1.0 + math.sqrt(1.0 + 2.4)) / 2.0
assert abs(G(ROOT)) < 1e-15, "the root is exact, so the errors below are too"

T0 = dG(START)  # the one inverse the first procedure computes and then reuses

FIXED = [START]
for _ in range(7):
 FIXED.append(FIXED[-1] - G(FIXED[-1]) / T0)
NEWTON = [START]
for _ in range(7):
 NEWTON.append(NEWTON[-1] - G(NEWTON[-1]) / dG(NEWTON[-1]))

FIX_ERR = [abs(v - ROOT) for v in FIXED]
NEW_ERR = [abs(v - ROOT) for v in NEWTON]
assert abs(FIXED[1] - NEWTON[1]) < 1e-15, "both methods take the same first step"
# the fixed-slope errors fall by a roughly constant factor
RATIOS = [FIX_ERR[i + 1] / FIX_ERR[i] for i in range(1, 5)]
assert max(RATIOS) - min(RATIOS) < 0.08, "so its convergence is geometric"
assert 0.40 < min(RATIOS) < 0.60, "with a ratio set by the derivative mismatch"
# Newton's square instead
for i in range(1, 5):
 assert NEW_ERR[i + 1] < NEW_ERR[i] ** 2 * 2.0, "Newton squares the error each step"
assert NEW_ERR[5] < 1e-13 < FIX_ERR[5], "which is a different kind of fast"

# ── beat 7: the quadratic bound, with a K that actually bounds both ─────
LO, HI = 0.25, 1.65
KBOUND = max(max(1.0 / dG(LO + (HI - LO) * k / 400), D2G) for k in range(401))
STEPS = [abs(NEWTON[i + 1] - NEWTON[i]) for i in range(4)]
for i in range(1, 4):
 assert STEPS[i] <= KBOUND ** 2 * STEPS[i - 1] ** 2 + 1e-15, \
     "each Newton step is bounded by K squared times the square of the last"

# ── beat 8: the book's clean choice, tau = 3/2 ─────────────────────────
TAU = 1.5
K8 = 2.0
C8 = (8.0 / 3.0) * math.log(K8)  # from K^2 = e^{3c/4}
assert abs(K8 ** 2 - math.exp(3 * C8 / 4)) < 1e-12, "that is what fixes c"
assert K8 >= 2 ** 0.75, "the book needs K at least two to the three quarters"
assert math.exp(C8) >= 4.0, "which is what makes e to the c at least four"
TAIL8 = math.exp(-C8 * (TAU - 1)) / (1 - math.exp(-C8 * (TAU - 1)))
assert TAIL8 <= 1.0, "so the sum of the steps stays inside the unit ball"
START8 = K8 ** -5
assert abs(START8 - 0.03125) < 1e-12, "and the requirement collapses to K to the minus five"


# ── beats 9 and 10: the inverse mapping in the plane ───────────────────
def Hmap(u, v):
 return u + v * v, u ** 3 + v


def Jdiff(u, v):
 """H(u) - u, which carries only the higher-order terms."""
 return v * v, u ** 3


PX, PY = 0.10, 0.08
UV = [(0.0, 0.0)]
for _ in range(30):
 _ju, _jv = Jdiff(*UV[-1])
 UV.append((PX - _ju, PY - _jv))
UEND, VEND = UV[-1]
_hx, _hy = Hmap(UEND, VEND)
assert abs(_hx - PX) < 1e-14 and abs(_hy - PY) < 1e-14, \
    "the iteration really does invert H at this point"

# the truncations the book prints, checked against the iterated answer
# The book prints u = x - y^2 - 2yx^3 + ..., but its own u3 = x - (y - x^3)^2
# expands to x - y^2 + 2yx^3 - x^6, so the sign there is a plus.  The numbers
# below settle it mechanically rather than by reading the page again.
TAY_U = PX - PY ** 2 + 2 * PY * PX ** 3
TAY_U_AS_PRINTED = PX - PY ** 2 - 2 * PY * PX ** 3
TAY_V = PY - PX ** 3 + 3 * PX ** 2 * PY ** 2
assert abs(TAY_U - UEND) < abs(TAY_U_AS_PRINTED - UEND) / 5, \
    "the plus sign matches the iteration, and by a wide margin"
assert abs(TAY_U - UEND) < 5e-5 and abs(TAY_V - VEND) < 5e-5, \
    "both truncations agree with the iterate to the order they are carried to"
ITER_ROWS = [(n, UV[n][0], UV[n][1]) for n in (1, 2, 3, 4)]


class AdvCalcE64Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 64

 MODE_LABEL = {
  0: {"zh": "定理 9.4：反過來的方向", "en": "Theorem 9.4: the other direction"},
  1: {"zh": "證明：材料都備好了", "en": "the proof: the pieces are already in place"},
  2: {"zh": "不動點定理其實是一個演算法", "en": "the fixed-point theorem is an algorithm"},
  3: {"zh": "固定斜率的那一道階梯", "en": "the staircase of one fixed slope"},
  4: {"zh": "Newton 法：改用當地的斜率", "en": "Newton: use the local slope instead"},
  5: {"zh": "快，可是要付代價", "en": "faster, but it has to be paid for"},
  6: {"zh": "快多少：e 的負 c τ ⁿ", "en": "how much faster: e to the minus c tau to the n"},
  7: {"zh": "每一步把誤差平方一次", "en": "each step squares the error"},
  8: {"zh": "取 τ 等於二分之三", "en": "taking tau to be three halves"},
  9: {"zh": "平面上最簡單的反映射", "en": "the simplest inverse mapping in the plane"},
  10: {"zh": "迭代算出來的正是 Taylor 展開", "en": "the iterates are computing Taylor expansions"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.32, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plot(self, f, ox, oy, sx, sy, col, sw=2.4, n=240, x0=0.0, x1=1.0):
  return self._curve([[ox + sx * k / n, oy + sy * f(x0 + (x1 - x0) * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 def _iter_picture(self, seq, slope_at_center, col):
  """One root-finding staircase, drawn from scratch.

  From the current point go up to the curve, then follow a line of the given
  slope back down to the axis; where it lands is the next point.  A fixed slope
  gives the first procedure, the local slope gives Newton.
  """
  ox, oy = -5.90, -0.86
  sx, sy = 4.00, 0.50
  X = lambda v: ox + sx * (v - LO) / (HI - LO)
  Y = lambda v: oy + sy * v
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._plot(G, ox, oy, sx, sy, ACCENT_B, sw=2.4, x0=LO, x1=HI))
  for i in range(3):
   a = seq[i]
   ga = G(a)
   m = slope_at_center if slope_at_center is not None else dG(a)
   b = a - ga / m
   g.add(Line([X(a), Y(0.0), 0], [X(a), Y(ga), 0], color=col, stroke_width=1.5),
         Line([X(a), Y(ga), 0], [X(b), Y(0.0), 0], color=col, stroke_width=1.8))
  g.add(Dot([X(ROOT), oy, 0], radius=0.065, color=ACCENT_A))
  return g, X, Y

 # ── beats ─────────────────────────────────────────────────────────
 def _thm94(self):
  g = VGroup()
  g.add(self._rect(-4.45, 0.52, 1.15, 0.30, ACCENT_B),
        self._mid(0.52, "K 可微", "K differentiable", ACCENT_B, FS_TAG, x=-4.45, w=2.10))
  g.add(self._rect(-1.35, 0.52, 1.15, 0.30, WARN),
        self._mid(0.52, "F 可微", "F differentiable", WARN, FS_TAG, x=-1.35, w=2.10))
  g.add(self._arr([-3.24, 0.52, 0], [-2.56, 0.52, 0], ACCENT_A, sw=2.4, tl=0.12))
  g.add(self._mid(-0.02, "定理 9.4", "Theorem 9.4", ACCENT_A, FS_TAG - 1, x=-2.90, w=1.80))
  g.add(self._mid(-0.56, "連續可微也一樣傳得下去（推論）",
                  "continuous differentiability is inherited too, by the corollary",
                  ACCENT_C, FS_TAG - 1, x=-2.90, w=5.60))
  g.add(self._panel(((0.86, "定理 9.2 給的是存在、唯一、連續",
                      "Theorem 9.2 gave existence, uniqueness and continuity", ACCENT_B),
                     (0.20, "9.4 再往上加一層：可微",
                      "9.4 adds one more floor: differentiability", WARN),
                     (-0.46, "假設是 K 自己可微，不是 F",
                      "what is assumed differentiable is K itself, not F", ACCENT_A))))
  return g.add(self._foot("上一集是「壓縮造出一個函數」，這一集問那個函數有多好——答案是跟 K 一樣好",
                          "the last episode built a function out of a contraction; this one asks how good it is, and the answer is as good as K",
                          ACCENT_A,
                          "定理 8.2 與 9.3 湊齊了隱函數定理的材料，9.4 則是把它升級成可微的版本",
                          "Theorems 8.2 and 9.3 completed the ingredients of the implicit-function theorem, and 9.4 upgrades it to the differentiable form"))

 def _proof(self):
  g = VGroup()
  rows = (("‖ K ( ξ , η ′ ) − K ( ξ , η ″ ) ‖   ≤   C ‖ η ′ − η ″ ‖", ACCENT_B),
          ("⇔          ‖ d K ² ‖    ≤    C", ACCENT_C),
          ("G ( ξ , η )  =  η  −  K ( ξ , η )        d G ²  =  I  −  d K ²", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.52, lab, col, FS_TAG, x=-3.40, w=5.40))
  g.add(self._dash([-5.90, -0.58, 0], [-0.90, -0.58, 0], DIM, n=24, sw=1.2))
  g.add(self._sym(-0.90, "‖ d K ² ‖ < 1        ⇒        ∃ ( d G ² ) ⁻ ¹", ACCENT_A,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._panel(((0.86, "Lipschitz 條件就是微分有界，兩者等價",
                      "the Lipschitz condition is a bound on the differential", ACCENT_B),
                     (0.20, "定理 8.1 讓 I − dK² 可逆",
                      "Theorem 8.1 makes the identity minus it invertible", ACCENT_C),
                     (-0.46, "再引第 3 章的定理 11.1 就結束",
                      "and Theorem 11.1 of chapter 3 finishes the argument", WARN))))
  return g.add(self._foot("這是第 8 節那條幾何級數的第二次回收：C 小於一，所以 I − dK² 可逆",
                          "this is the second use of section 8's geometric series: C is under one, so the identity minus it is invertible",
                          ACCENT_A,
                          "整個第 4 章到這裡扣成一串——完備、Banach 代數、不動點，三件事互相支撐",
                          "the whole of chapter 4 locks together here: completeness, the Banach algebra, and the fixed point all hold each other up"))

 def _algorithm(self):
  g = VGroup()
  g.add(self._sym(0.76, "η ᵢ ₊ ₁    =    K ( ξ , η ᵢ )", ACCENT_B,
                  FS_TAG + 1, x=-3.40, w=4.60))
  g.add(self._arr([-3.40, 0.48, 0], [-3.40, 0.12, 0], ACCENT_A, sw=2.0, tl=0.10))
  g.add(self._sym(-0.10, "η ᵢ ₊ ₁  −  η ᵢ    =    −  T ⁻ ¹ G ( ξ , η ᵢ )", WARN,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._mid(-0.72, "T 只算一次，之後每一步重複用",
                  "T is computed once and reused at every step afterwards",
                  ACCENT_C, FS_TAG, x=-3.40, w=5.40))
  g.add(self._panel(((0.86, "不動點定理不只是隱函數定理的推論",
                      "the fixed-point theorem is not only a route to the implicit-function theorem",
                      ACCENT_B),
                     (0.20, "它的證明本身就是一個演算法",
                      "its proof is itself an algorithm", WARN),
                     (-0.46, "只要中心那一點的反元素算得出來",
                      "provided the one inverse at the center point can be computed",
                      ACCENT_A))))
  return g.add(self._foot("存在性的證明是「反覆作用 K」，而那句話本身就是可以拿去跑的程式",
                          "the existence proof says to apply K over and over, and that sentence is already a program",
                          ACCENT_A,
                          "書上用星號標了這一段，因為這是整節最容易被讀過去的一句話",
                          "the book stars this passage, because it is the sentence in the section most easily read past"))

 def _fixed_slope(self):
  g, X, Y = self._iter_picture(FIXED, T0, WARN)
  g.add(self._mid(0.92, "斜率固定為 T", "slope fixed at T", ACCENT_A,
                  FS_TAG - 1, x=-4.20, w=2.30))
  g.add(self._table((("       i          y ᵢ          | y ᵢ − y * |", DIM),)
                    + tuple((f"     {i:4d}       {FIXED[i]:.5f}        {FIX_ERR[i]:.2e}",
                             ACCENT_C) for i in (1, 2, 3, 4)), y0=0.86, dy=0.32))
  g.add(self._mid(-0.62, f"誤差每一步大約乘上 {sum(RATIOS) / len(RATIOS):.2f}",
                  f"the error is multiplied by about {sum(RATIOS) / len(RATIOS):.2f} at every step",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("從當前點往上走到曲線，再沿一條固定斜率的直線走回橫軸——落點就是下一個點",
                          "from the current point go up to the curve, then follow a line of one fixed slope back to the axis, and where it lands is the next point",
                          ACCENT_A,
                          "書上把這件事畫成一張圖；這裡的曲線、階梯與標號都是自己重新設計的",
                          "the book sketches this; the curve, the staircase and the labels here are our own design"))

 def _newton(self):
  g, X, Y = self._iter_picture(NEWTON, None, ACCENT_C)
  g.add(self._mid(0.92, "斜率取當地的 d G", "slope is the local d G", ACCENT_A,
                  FS_TAG - 1, x=-4.05, w=2.60))
  g.add(self._table((("       i          y ᵢ          | y ᵢ − y * |", DIM),)
                    + tuple((f"     {i:4d}       {NEWTON[i]:.5f}        {NEW_ERR[i]:.2e}",
                             ACCENT_C) for i in (1, 2, 3, 4)), y0=0.86, dy=0.32))
  g.add(self._mid(-0.62, "同樣的起點，同樣的第一步，之後完全不同",
                  "the same start and the same first step, and nothing alike after that",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("Newton 法把那條直線的斜率換成當前點的微分——也就是切線",
                          "Newton replaces the slope of that line with the differential at the current point, that is, the tangent",
                          ACCENT_A,
                          f"第四步的誤差：固定斜率還是 {FIX_ERR[4]:.1e}，Newton 已經到 {NEW_ERR[4]:.1e}",
                          f"at the fourth step the fixed-slope error is still {FIX_ERR[4]:.1e} while Newton is already at {NEW_ERR[4]:.1e}"))

 def _trade(self):
  g = VGroup()
  for cy, zh, en, col, cnt in ((0.62, "固定斜率", "one fixed slope", WARN, "×  1"),
                               (-0.06, "Newton", "Newton", ACCENT_C, "×  ∞")):
   g.add(self._rect(-4.30, cy, 1.30, 0.26, col),
         self._mid(cy, zh, en, col, FS_TAG - 1, x=-4.30, w=2.40),
         self._sym(cy, cnt, ACCENT_A, FS_TAG, x=-2.10, w=1.20))
  g.add(self._mid(-0.72, "要算幾個反元素",
                  "how many inverses have to be computed",
                  ACCENT_A, FS_TAG - 1, x=-3.20, w=4.60))
  g.add(self._table((("       i          T ⁻ ¹            S ᵢ ⁻ ¹", DIM),)
                    + tuple((f"     {i:4d}       {FIX_ERR[i]:.1e}        {NEW_ERR[i]:.1e}",
                             ACCENT_C) for i in (1, 2, 3, 4)), y0=0.86, dy=0.32))
  g.add(self._mid(-0.62, "同一個問題，同一個起點",
                  "the same problem, from the same starting point", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("書上的說法是：Newton 快得多，可是它的缺點是要能算出無窮多個線性變換的反元素",
                          "the book says Newton converges much more rapidly, but suffers the disadvantage that the inverses of an infinite number of linear transformations must be computable",
                          ACCENT_A,
                          "前面那個程序只算一次反元素，之後一直重複用——便宜，但慢",
                          "the first procedure inverts once and reuses it: cheap, and slow"))

 def _claim(self):
  g = VGroup()
  rows = (("‖ ( d G ₓ ) ⁻ ¹ ‖    ≤    K", ACCENT_B),
          ("‖ d ² G ₓ ‖    ≤    K", ACCENT_C),
          ("1  <  τ  <  2", ACCENT_A))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.50, lab, col, FS_TAG, x=-3.90, w=4.20))
  g.add(self._dash([-5.90, -0.54, 0], [-1.40, -0.54, 0], DIM, n=22, sw=1.2))
  g.add(self._sym(-0.88, "‖ x ₙ  −  x ₙ ₋ ₁ ‖      ≤      exp ( − c τ ⁿ )", WARN,
                  FS_TAG + 1, x=-3.65, w=4.80))
  g.add(self._panel(((0.86, "兩個界都放在同一個常數 K 上",
                      "both bounds are put on the same constant K", ACCENT_B),
                     (0.20, "指數裡還有一個指數",
                      "there is an exponent inside the exponent", ACCENT_C),
                     (-0.46, "τ 大於一，所以 τ ⁿ 自己就爆炸",
                      "tau is over one, so tau to the n blows up on its own", WARN))))
  return g.add(self._foot("這不是幾何收斂——幾何收斂是 e 的負 c n，這裡的指數是 τ 的 n 次方",
                          "this is not geometric convergence: geometric would be e to the minus c n, and here the exponent is tau to the n",
                          ACCENT_A,
                          "書上要證的就是這個形狀，而證明的關鍵在下一拍",
                          "that shape is what the book sets out to prove, and the key step is in the next beat"))

 def _squaring(self):
  ox, oy = -5.85, -0.80
  sx, sy = 4.10, 1.85
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  lo = math.log10(NEW_ERR[4]) - 1.0
  hi = math.log10(FIX_ERR[1])
  for errs, col in ((FIX_ERR, WARN), (NEW_ERR, ACCENT_C)):
   pts = []
   for i in range(1, 5):
    pts.append([ox + sx * (i - 1) / 3,
                oy + sy * (math.log10(errs[i]) - lo) / (hi - lo), 0])
   g.add(self._curve(pts, col, sw=2.0))
   for pt in pts:
    g.add(Dot(pt, radius=0.055, color=col))
  # the curves start high on the left and fall, so the label goes top right
  g.add(self._sym(oy + sy * 1.00, "log  | y ᵢ − y * |", ACCENT_A, FS_TAG - 1,
                  x=ox + 3.15, w=2.40))
  g.add(self._table((("     K   =   %.3f" % KBOUND, DIM),
                     ("       i         Δ ᵢ            K ² Δ ᵢ ₋ ₁ ²", DIM))
                    + tuple((f"     {i:4d}      {STEPS[i]:.2e}        "
                             f"{KBOUND ** 2 * STEPS[i - 1] ** 2:.2e}", ACCENT_C)
                            for i in (1, 2, 3)), y0=0.86, dy=0.32))
  g.add(self._mid(-0.72, "紅色是固定斜率，紫色是 Newton",
                  "red is the fixed slope and purple is Newton", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("歸納的關鍵是 Taylor 定理：一階項剛好消掉，剩下 K 平方乘上前一步的平方",
                          "the induction turns on Taylor's theorem: the first-order term cancels exactly, leaving K squared times the square of the previous step",
                          ACCENT_A,
                          "每走一步就把誤差平方一次——紫色那條在對數圖上是往下折的，不是直的",
                          "squaring the error at every step is why the purple line bends downward on a log plot instead of running straight"))

 def _constants(self):
  g = VGroup()
  rows = ((f"τ   =   3 / 2", ACCENT_B),
          (f"K   =   {K8:.0f}            K ²   =   e ³ ᶜ ᐟ ⁴", ACCENT_C),
          (f"c   =   {C8:.4f}            e ᶜ   =   {math.exp(C8):.2f}   ≥   4", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.52, lab, col, FS_TAG, x=-3.60, w=4.80))
  g.add(self._dash([-5.90, -0.60, 0], [-1.30, -0.60, 0], DIM, n=22, sw=1.2))
  g.add(self._sym(-0.92, f"‖ G ( 0 ) ‖    ≤    K ⁻ ⁵    =    {START8:.5f}", ACCENT_A,
                  FS_TAG + 1, x=-3.60, w=4.80))
  g.add(self._panel(((0.86, "τ 小於二，所以 c 取大就撐得住歸納",
                      "tau is under two, so a large enough c carries the induction", ACCENT_B),
                     (0.20, f"尾巴的和是 {TAIL8:.3f}，不超過一",
                      f"the sum of the tail is {TAIL8:.3f}, which is at most one", ACCENT_C),
                     (-0.46, "所有條件最後收成對起始值的一個要求",
                      "and every condition collapses into one requirement on the start", WARN))))
  return g.add(self._foot("書上挑 τ 等於二分之三，讓那個不等式剛好成立，其他常數就都被決定了",
                          "the book takes tau to be three halves so that the inequality just holds, and every other constant is then determined",
                          ACCENT_A,
                          "畫面上的 c 與那個 K 的負五次方都是照書上的關係式算出來的",
                          "the c on screen and that K to the minus five are both computed from the book's own relations"))

 def _plane(self):
  g = VGroup()
  g.add(self._sym(0.80, "x   =   u  +  v ²                    y   =   u ³  +  v", ACCENT_B,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._sym(0.16, "d H ₀    =    I", ACCENT_A, FS_TAG + 1, x=-3.40, w=2.40))
  g.add(self._sym(-0.42, "H ( u )  −  u    =    J ( u )    =    ⟨ v ² ,  u ³ ⟩", WARN,
                  FS_TAG, x=-3.40, w=5.40))
  g.add(self._mid(-0.94, "一階項在這裡被消掉了",
                  "the first-order terms have cancelled here", ACCENT_C,
                  FS_TAG, x=-3.40, w=5.20))
  g.add(self._panel(((0.86, "Jacobian 在原點正好是單位矩陣",
                      "the Jacobian is exactly the identity at the origin", ACCENT_B),
                     (0.20, "所以差只剩高階項",
                      "so the difference carries only higher-order terms", WARN),
                     (-0.46, "這就是 d K ² = 0 的實際樣貌",
                      "and that is the practical face of the differential vanishing", ACCENT_A))))
  return g.add(self._foot("書上說這是「盡可能簡單」的例子：反映射定理最素的一個情形",
                          "the book calls this as simple as possible: the barest case of the inverse mapping theorem",
                          ACCENT_A,
                          "迭代是 u ₙ = x − J ( u ₙ ₋ ₁ )，從零出發，每一項都是多項式",
                          "the iteration is x minus J of the previous point, started from zero, and every term is a polynomial"))

 def _taylor(self):
  g = VGroup()
  g.add(self._sym(0.86, "u   =   x  −  y ²  +  2 y x ³  +  …", ACCENT_B,
                  FS_TAG, x=-3.50, w=5.20),
        self._sym(0.38, "v   =   y  −  x ³  +  3 x ² y ²  +  …", ACCENT_C,
                  FS_TAG, x=-3.50, w=5.20))
  g.add(self._dash([-5.90, 0.02, 0], [-1.10, 0.02, 0], DIM, n=22, sw=1.2))
  g.add(self._sym(-0.28, f"x  =  {PX:.2f}  ,  y  =  {PY:.2f}", ACCENT_A,
                  FS_TAG - 1, x=-3.50, w=3.40))
  g.add(self._mid(-0.66, f"迭代到收斂　{UEND:.7f}", f"iterated      {UEND:.7f}",
                  WARN, FS_TAG - 1, x=-3.50, w=4.40),
        self._mid(-0.98, f"加號版的截斷式　{TAY_U:.7f}",
                  f"truncation, plus sign   {TAY_U:.7f}",
                  ACCENT_A, FS_TAG - 1, x=-3.50, w=4.40))
  g.add(self._table((("       n          u ₙ            v ₙ", DIM),)
                    + tuple((f"     {n:4d}      {u:.6f}      {v:.6f}", ACCENT_C)
                            for n, u, v in ITER_ROWS), y0=0.86, dy=0.32))
  g.add(self._mid(-0.62, "H 作用回去，誤差小於 1e-14",
                  "applying H to the answer returns the point to within 1e-14", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("那兩列多項式算出來的，正是兩個反函數的 Taylor 展開——書上把前幾項印出來",
                          "those two sequences of polynomials are computing the Taylor expansions of the two inverse functions, whose leading terms the book prints",
                          ACCENT_A,
                          "書上第三項印的是減 2 y x ³，可是它自己上面那行的 u ₃ 展開出來是加——數值也站在加號這邊",
                          "the book prints minus 2 y x cubed there, but its own u3 expands to a plus, and the numbers agree with the plus"))

 def stage(self):
  a, b, c = self._thm94(), self._proof(), self._algorithm()
  d, e, f = self._fixed_slope(), self._newton(), self._trade()
  h, i, j = self._claim(), self._squaring(), self._constants()
  k, l = self._plane(), self._taylor()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE64ZH, AdvCalcE64EN = make(AdvCalcE64Base, "64", prefix="AdvCalcE")
