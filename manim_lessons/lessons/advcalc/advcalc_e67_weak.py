"""advcalc E67 -- chapter 4, starred section *12 (book pp. 245-247): weak methods.

All norms on a finite-dimensional space are equivalent and every linear map with
a finite-dimensional domain is bounded, which suggests the limit theory of such
spaces can be had without norms at all.  The device is to replace a vector-valued
map F by the whole family of real-valued maps {l o F : l in V*}.  Theorem 12.1
says that in finite dimension this loses nothing: convergence under every
functional is convergence in norm.  Integration and differentiation of
parametrized arcs are then *defined* by commuting with functionals, the
fundamental theorem becomes one line, and the one thing that does not come for
free is the norm inequality, which needs Theorem 12.2 -- and the book states that
one without proof.

Section 12's content ends a third of the way down book page 247, where chapter 5
begins, and the section has **no exercises at all** -- the second time in this
book (starred section 7 of chapter 2 was the first).  The OUTLINE lists 245-248,
so this time its page column overshoots into the next chapter rather than into
exercises; either way it is wrong for the ninth section running.

Everything on screen is computed in one concrete case: V is the plane under the
one-norm, so V* carries the sup norm and its unit sphere is a square; the arc is
the quarter circle f(t) = (cos t, sin t) on [0, pi/2], whose integral is the
vector (1, 1).  The weak definitions are checked against Simpson quadrature and
central differences rather than asserted, and beat 9's norming functional, its
tangent line and the whole edge that line touches are all found by search.
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


# V is the plane under the one-norm, so the dual norm is the sup norm.  Picking
# the one-norm is not cosmetic: it is the norm Theorem 12.1's proof uses, and its
# unit sphere is the diamond whose corners beat 9 needs.
def n1(v):
 return abs(v[0]) + abs(v[1])


def dn(l):
 return max(abs(l[0]), abs(l[1]))


def ap(l, v):
 return l[0] * v[0] + l[1] * v[1]


def simpson(g, a, b, n=2000):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


# ── the arc, and the five functionals every table is built from ─────────
TA, TB = 0.0, math.pi / 2


def f(t):
 return (math.cos(t), math.sin(t))


def fp(t):
 return (-math.sin(t), math.cos(t))


def Fx(x):
 """The integral of f from the left endpoint to x, in closed form."""
 return (math.sin(x), 1.0 - math.cos(x))


INT = (1.0, 1.0)
LAMS = [(1.0, 0.5), (-0.4, 1.0), (1.0, 1.0), (0.25, -1.0), (-1.0, -0.75)]
assert all(abs(dn(l) - 1.0) < 1e-15 for l in LAMS), \
    "every functional in the tables has dual norm one, so the numbers compare"

# ── beat 5: the weak integral, checked against quadrature ──────────────
INT_ROWS = [(l, simpson(lambda t: ap(l, f(t)), TA, TB), ap(l, INT)) for l in LAMS]
INT_ERR = max(abs(q - v) for _l, q, v in INT_ROWS)
assert INT_ERR < 1e-12, "the quadrature and the vector (1, 1) agree for every functional"
AREA = INT_ROWS[0][1]
assert min(ap(LAMS[0], f(TA + k * (TB - TA) / 200)) for k in range(201)) > 0.4, \
    "the first composite stays positive, so the shaded area is the integral itself"

# ── beat 6: that correspondence is linear, hence lies in the second dual
L1, L2 = LAMS[0], LAMS[1]
LC = (2 * L1[0] - 3 * L2[0], 2 * L1[1] - 3 * L2[1])
LIN_L = simpson(lambda t: ap(LC, f(t)), TA, TB)
LIN_R = 2 * INT_ROWS[0][1] - 3 * INT_ROWS[1][1]
assert abs(LIN_L - LIN_R) < 1e-12, "so the map is linear in the functional"

# ── beats 1 and 2: a sequence, its shadows, and the one-norm ───────────
XI = (1.0, -0.5)
NS = (1, 2, 4, 8, 16)


def seq(n):
 r, th = 0.9 / n, n * math.pi / 3
 return (XI[0] + r * math.cos(th), XI[1] + r * math.sin(th))


SEQ_ROWS = []
for _n in NS:
 _d = (seq(_n)[0] - XI[0], seq(_n)[1] - XI[1])
 SEQ_ROWS.append((_n, abs(_d[0]), abs(_d[1]), n1(_d), abs(ap(L1, _d))))
for (_, _, _, _s0, _), (_, _, _, _s1, _) in zip(SEQ_ROWS, SEQ_ROWS[1:]):
 assert abs(_s1 - _s0 / 2) < 1e-12, \
     "the directions were chosen so the one-norm halves exactly down the column"
assert all(_q <= _s + 1e-12 for _, _, _, _s, _q in SEQ_ROWS), \
    "and each shadow is under the bound"
# The shadow is not monotone -- the direction of approach turns as n grows -- and
# the caption says so, so it has to be true of these particular rows.
assert any(SEQ_ROWS[k][4] > SEQ_ROWS[k - 1][4] for k in range(1, len(SEQ_ROWS))), \
    "one functional's values need not decrease, they are only squeezed"
SEQ_DRAW = [seq(n) for n in range(1, 13)]

# ── beat 3: drop one functional and a runaway sequence passes ──────────
RUN = [(n, 0.0, float(n), n1((0.0, float(n)))) for n in NS]
assert all(e1 == 0.0 and nn == float(n) for n, e1, _e2, nn in RUN), \
    "the first coordinate is zero throughout while the norm is n"

# ── beat 7: the weak derivative, by central differences ────────────────
X0 = 0.7
HS = (0.1, 0.01, 0.001)
DER_L = L2
DER_ROWS = [(h, (ap(DER_L, f(X0 + h)) - ap(DER_L, f(X0 - h))) / (2 * h)) for h in HS]
DER_TRUE = ap(DER_L, fp(X0))
# the composite drawn in beat 7 has to rise across the frame, not sit flat in it
DER_SPAN = (max(ap(DER_L, f(TA + k * (TB - TA) / 200)) for k in range(201))
            - min(ap(DER_L, f(TA + k * (TB - TA) / 200)) for k in range(201)))
assert DER_SPAN > 1.3, "the second functional's composite sweeps the whole frame"

DER_ERR = [abs(cd - DER_TRUE) for _h, cd in DER_ROWS]
assert DER_ERR[1] < DER_ERR[0] / 50 and DER_ERR[2] < DER_ERR[1] / 50, \
    "a central difference falls off like h squared, and these do"
DER_MAX = max(abs((ap(l, f(X0 + 1e-5)) - ap(l, f(X0 - 1e-5))) / 2e-5 - ap(l, fp(X0)))
              for l in LAMS)
assert DER_MAX < 1e-9, "and the same vector works for every functional in the table"

# ── beat 8: the fundamental theorem, weakly ────────────────────────────
FTC_ROWS = [(h, (ap(L1, Fx(X0 + h)) - ap(L1, Fx(X0 - h))) / (2 * h)) for h in HS]
FTC_TRUE = ap(L1, f(X0))
FTC_ERR = [abs(cd - FTC_TRUE) for _h, cd in FTC_ROWS]
assert FTC_ERR[2] < FTC_ERR[0] / 1000, "the difference quotient for F converges to f"
FTC_MAX = max(abs((ap(l, Fx(X0 + 1e-5)) - ap(l, Fx(X0 - 1e-5))) / 2e-5 - ap(l, f(X0)))
              for l in LAMS)
assert FTC_MAX < 1e-9, "for every functional at once, which is what F prime equals f means"

# ── beat 9: Theorem 12.2, by search over the dual unit sphere ──────────
KD = 64


def dual_sphere(k, K=KD):
 """The kth of K points on the sup-norm unit sphere of V*, a square."""
 s = 4.0 * k / K
 if s < 1:
  return (1.0, -1.0 + 2 * s)
 if s < 2:
  return (1.0 - 2 * (s - 1), 1.0)
 if s < 3:
  return (-1.0, 1.0 - 2 * (s - 2))
 return (-1.0 + 2 * (s - 3), -1.0)


DUAL = [dual_sphere(k) for k in range(KD)]
assert all(abs(dn(l) - 1.0) < 1e-12 for l in DUAL), "the square really is the unit sphere"
SUP = max(abs(ap(l, INT)) for l in DUAL)
assert abs(SUP - n1(INT)) < 1e-12, "the supremum is the one-norm of the vector: Theorem 12.2"
NORMING = [l for l in DUAL if abs(abs(ap(l, INT)) - SUP) < 1e-12]
assert NORMING == [(1.0, 1.0), (-1.0, -1.0)], \
    "and exactly two sample points attain it, one the negative of the other"
SECOND = max(abs(ap(l, INT)) for l in DUAL if l not in NORMING)
assert SECOND < SUP - 0.1, "every other sampled functional is strictly, visibly short"
# The tangent line is where the norming functional takes the value ||a||.  It
# never enters the ball, but it touches the sphere along a whole edge rather than
# at the single point a, and beat 9 says so.
def prim_sphere(k, K=256):
 """The kth of K points on the one-norm sphere of radius two in V."""
 s = 4.0 * k / K
 if s < 1:
  return (2.0 - 2 * s, 2 * s)
 if s < 2:
  return (-2 * (s - 1), 2.0 - 2 * (s - 1))
 if s < 3:
  return (-2.0 + 2 * (s - 2), -2 * (s - 2))
 return (2 * (s - 3), -2.0 + 2 * (s - 3))


PRIM = [prim_sphere(k) for k in range(256)]
assert all(abs(n1(v) - 2.0) < 1e-12 for v in PRIM), "radius two under the one-norm"
assert all(ap(NORMING[0], v) <= 2.0 + 1e-12 for v in PRIM), \
    "the sphere lies on one side of the tangent line, which is the point of it"
EDGE = [v for v in PRIM if abs(ap(NORMING[0], v) - 2.0) < 1e-9]
TOUCH = len(EDGE)
assert TOUCH > 60, "and the line touches it along a whole edge, not at one point"
assert EDGE == PRIM[:TOUCH], "the contact set is one unbroken run of the sampled sphere"

# ── beat 10: the inequality the chain finally gives ────────────────────
FINF = max(n1(f(TA + k * (TB - TA) / 4000)) for k in range(4001))
assert abs(FINF - math.sqrt(2.0)) < 1e-6, "the uniform norm of the arc is root two"
BOUND = (TB - TA) * FINF
NRM = n1(INT)
assert NRM <= BOUND, "and the inequality holds"
RATIO = NRM / BOUND
assert 0.89 < RATIO < 0.91, "with a real gap of about a tenth, not an equality in disguise"
# Beat 10 draws the two numbers as bars; one unit of them is this many screen
# units, and the caption says the factor rather than leaving it to be guessed.
BAR = 1.15
assert BAR * BOUND < 3.0, "both bars have to fit in the left half of the frame"


class AdvCalcE67Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 67

 MODE_LABEL = {
  0: {"zh": "也許根本不需要範數", "en": "perhaps no norms are needed at all"},
  1: {"zh": "定理 12.1，容易的那一半", "en": "theorem 12.1, the easy half"},
  2: {"zh": "反過來：對偶基那 n 個座標泛函", "en": "the converse: the n coordinate functionals"},
  3: {"zh": "少一個泛函就測不出來", "en": "one functional short and the test fails"},
  4: {"zh": "弱收斂，以及有限維的等價", "en": "weak convergence, and the finite-dimensional equivalence"},
  5: {"zh": "積分的弱定義", "en": "the weak definition of the integral"},
  6: {"zh": "為什麼那個向量唯一", "en": "why that vector is unique"},
  7: {"zh": "微分照抄同一句話", "en": "differentiation reads the same way"},
  8: {"zh": "微積分基本定理變成一行", "en": "the fundamental theorem in one line"},
  9: {"zh": "弱方法拿不到的那一個", "en": "the one weak methods do not reach"},
  10: {"zh": "最後那一串不等式", "en": "the chain that finishes it"},
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

 def _plane(self, cx, cy, s, xspan=1.15, yspan=1.05, back=0.45):
  """Axes for a small copy of V; s is screen units per unit of the plane."""
  return VGroup(Line([cx - s * back, cy, 0], [cx + s * xspan, cy, 0],
                     color=DIM, stroke_width=1.3),
                Line([cx, cy - s * back, 0], [cx, cy + s * yspan, 0],
                     color=DIM, stroke_width=1.3))

 def _frame(self, ox, oy, w, h, down=0.30):
  """Axes for a graph of a real function of a real variable."""
  return VGroup(Line([ox - 0.12, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _arc(self, cx, cy, s, g, col, sw=2.6, n=48, t0=TA, t1=TB):
  return self._curve([[cx + s * g(t0 + k * (t1 - t0) / n)[0],
                       cy + s * g(t0 + k * (t1 - t0) / n)[1], 0] for k in range(n + 1)],
                     col, sw=sw)

 def _graph(self, ox, oy, sx, sy, l, col, sw=2.4, n=64, t0=TA, t1=TB):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * ap(l, f(t0 + k * (t1 - t0) / n)), 0]
                      for k in range(n + 1)], col, sw=sw)

 def _pt(self, cx, cy, s, v, col, r=0.055):
  return Dot([cx + s * v[0], cy + s * v[1], 0], radius=r, color=col)

 # ── beats ─────────────────────────────────────────────────────────
 def _opening(self):
  cx, cy, s = -5.20, -0.40, 1.05
  g = VGroup(self._plane(cx, cy, s, xspan=1.20, yspan=1.20, back=0.30))
  g.add(self._arc(cx, cy, s, f, ACCENT_B))
  for t, col in ((0.0, ACCENT_A), (0.75, ACCENT_C), (TB, WARN)):
   g.add(self._arr([cx, cy, 0], [cx + s * f(t)[0], cy + s * f(t)[1], 0], col,
                   sw=2.2, tl=0.11))
  g.add(self._sym(cy + s * 1.20 + 0.02, "f", ACCENT_B, FS_TAG, x=cx + 0.95, w=0.60))
  ox, oy, sx, sy = -2.95, -0.32, 0.99, 0.56
  g.add(self._frame(ox, oy, 1.72, 0.78, down=0.34))
  g.add(self._graph(ox, oy, sx, sy, L1, ACCENT_A),
        self._graph(ox, oy, sx, sy, L2, ACCENT_C))
  g.add(self._sym(oy + sy * ap(L1, f(0.0)) + 0.20, "λ ₁ ∘ f", ACCENT_A, FS_TAG - 2,
                  x=ox + 1.28, w=1.10),
        self._sym(oy + sy * ap(L2, f(0.0)) - 0.20, "λ ₂ ∘ f", ACCENT_C, FS_TAG - 2,
                  x=ox + 1.28, w=1.10))
  g.add(self._arr([cx + 1.35, cy + 0.28, 0], [ox - 0.30, cy + 0.28, 0], DIM,
                  sw=1.8, tl=0.10))
  g.add(self._panel(((0.86, "有限維空間上所有範數都等價",
                      "all norms on a finite-dimensional space are equivalent", ACCENT_B),
                     (0.20, "有限維定義域的線性映射自動有界",
                      "a linear map with such a domain is automatically bounded", ACCENT_C),
                     (-0.46, "於是：極限理論也許不需要範數",
                      "so the limit theory may need no norms at all", WARN))))
  return g.add(self._foot("左邊那條青綠色的弧是 f，右邊兩條曲線是拿兩個泛函複合出來的實值函數",
                          "the teal arc on the left is f, and the two curves on the right are the real-valued functions got by composing with two functionals",
                          ACCENT_A,
                          "這一節的做法就是：要研究向量值的 F，改去研究 λ 複合 F 的全體，λ 跑遍對偶空間",
                          "the method of the section is to study a vector-valued F through the whole family of composites, as the functional runs over the dual space"))

 def _forward(self):
  cx, cy, s = -5.35, 0.30, 0.95
  g = VGroup(self._plane(cx, cy, s, xspan=1.45, yspan=0.85, back=0.30))
  for k, v in enumerate(SEQ_DRAW):
   g.add(self._pt(cx, cy, s, v, ACCENT_C, r=0.048 if k else 0.058))
  g.add(self._pt(cx, cy, s, XI, ACCENT_A, r=0.075))
  g.add(self._sym(cy + s * XI[1] - 0.28, "ξ", ACCENT_A, FS_TAG - 1,
                  x=cx + s * XI[0] + 0.26, w=0.60))
  ox, oy = -2.70, -0.10
  g.add(Line([ox, oy, 0], [ox + 2.30, oy, 0], color=DIM, stroke_width=1.3))
  lv = ap(L1, XI)
  for k, v in enumerate(SEQ_DRAW):
   g.add(Dot([ox + 1.15 + 0.68 * (ap(L1, v) - lv), oy, 0],
             radius=0.048, color=ACCENT_C))
  g.add(Dot([ox + 1.15, oy, 0], radius=0.072, color=ACCENT_A))
  g.add(self._sym(oy + 0.30, "λ ₁ ( ξ )", ACCENT_A, FS_TAG - 2, x=ox + 1.15, w=1.20))
  g.add(self._table(((" n     | λ ₁ ( ξ ₙ − ξ ) |      ‖ λ ₁ ‖ ‖ ξ ₙ − ξ ‖", DIM),)
                    + tuple((f"{n:3d}            {q:.4f}                    {t:.4f}",
                             ACCENT_C if q < t else WARN)
                            for n, _e1, _e2, t, q in SEQ_ROWS), y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "左邊的點收斂，右邊的影子就跟著收斂",
                  "the points converge on the left, and the shadows follow on the right",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("必要的那一半沒有內容：泛函自動連續，差的絕對值被它的範數乘上向量的範數壓著",
                          "the necessary half has no content: a functional is automatically continuous, so the difference is bounded by its norm times the norm of the vector",
                          ACCENT_A,
                          "表上左欄不是單調下降的——趨近的方向在轉——可是每一列都被右欄壓著，所以還是收斂",
                          "the left column does not decrease monotonically, because the direction of approach turns, but every row is squeezed by the right one"))

 def _converse(self):
  cx, cy, s = -5.30, 0.35, 1.15
  g = VGroup(self._plane(cx, cy, s, xspan=1.30, yspan=0.70, back=0.25))
  g.add(self._pt(cx, cy, s, XI, ACCENT_A, r=0.070))
  for n, col in ((1, WARN), (2, ACCENT_B)):
   v = seq(n)
   g.add(self._pt(cx, cy, s, v, col, r=0.055))
   g.add(self._dash([cx + s * XI[0], cy + s * XI[1], 0],
                    [cx + s * v[0], cy + s * XI[1], 0], col, n=5, sw=1.4),
         self._dash([cx + s * v[0], cy + s * XI[1], 0],
                    [cx + s * v[0], cy + s * v[1], 0], col, n=5, sw=1.4))
  g.add(self._sym(cy + s * XI[1] - 0.30, "ξ", ACCENT_A, FS_TAG - 1,
                  x=cx + s * XI[0] - 0.22, w=0.60))
  g.add(self._table((("  n      | E ₁ |       | E ₂ |       ‖ · ‖ ₁", DIM),)
                    + tuple((f"{n:3d}      {e1:.4f}      {e2:.4f}      {t:.4f}",
                             WARN if n == 1 else (ACCENT_B if n == 2 else ACCENT_C))
                            for n, e1, e2, t, _q in SEQ_ROWS), y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "兩段虛線的長度加起來就是那一列的一範數",
                  "the two dashed legs add up to the one-norm in that row",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("紅色那一組是 n 等於 1，青綠色那一組是 n 等於 2；虛線走的是先橫再直的路",
                          "the red pair is n equals one and the teal pair is n equals two, and the dashes go across and then up",
                          ACCENT_A,
                          "假設每個泛函都收斂，座標泛函也就收斂，而一範數是那 n 個座標差的絕對值之和",
                          "if every functional converges then the coordinate functionals do, and the one-norm is the sum of the absolute values of the n coordinate differences"))

 def _dropone(self):
  cx, cy, s = -4.60, -0.72, 0.30
  g = VGroup(self._plane(cx, cy, s, xspan=2.00, yspan=5.80, back=1.20))
  for n in range(1, 6):
   g.add(self._pt(cx, cy, s, (0.0, float(n)), WARN, r=0.058))
  g.add(self._arr([cx, cy + s * 5.40, 0], [cx, cy + s * 6.10, 0], WARN, sw=2.0, tl=0.11))
  g.add(Dot([cx, cy, 0], radius=0.095, color=ACCENT_B))
  g.add(self._sym(cy, "E ₁  =  0", ACCENT_B, FS_TAG - 1, x=cx + 1.55, w=1.30))
  g.add(self._sym(cy + s * 3.00, "η ₙ", WARN, FS_TAG - 1, x=cx + 0.44, w=0.70))
  g.add(self._table((("  n      E ₁ ( η ₙ )      E ₂ ( η ₙ )      ‖ η ₙ ‖ ₁", DIM),)
                    + tuple((f"{n:3d}          {e1:.1f}              {e2:.1f}             {nn:.1f}",
                             WARN) for n, e1, e2, nn in RUN), y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "青綠色那個點是 E ₁ 看到的全部",
                  "the teal dot is everything the first functional sees", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("紅色那串點的第一個座標永遠是零，只用 E ₁ 去測就看起來收斂——可是範數是 n，跑到無限大",
                          "the red points have first coordinate zero throughout, so the first functional alone reports convergence, while the norm is n and runs to infinity",
                          ACCENT_A,
                          "所以對偶基那 n 個泛函一個都不能少：漏掉哪一個，那個泛函的核就是測不到的方向",
                          "so not one of the n dual basis functionals can be dropped: whichever is left out, its null space is the direction the test cannot see"))

 def _weakdef(self):
  g = VGroup()
  g.add(self._rect(-4.90, 0.52, 1.15, 0.28, ACCENT_B),
        self._mid(0.52, "範數收斂", "norm convergence", ACCENT_B, FS_TAG, x=-4.90, w=2.10))
  g.add(self._rect(-1.90, 0.52, 1.15, 0.28, ACCENT_C),
        self._mid(0.52, "弱收斂", "weak convergence", ACCENT_C, FS_TAG, x=-1.90, w=2.10))
  g.add(self._arr([-3.68, 0.66, 0], [-3.12, 0.66, 0], ACCENT_A, sw=2.4, tl=0.12),
        self._arr([-3.12, 0.34, 0], [-3.68, 0.34, 0], WARN, sw=2.4, tl=0.12))
  g.add(self._mid(1.04, "任何賦範空間", "in any normed space", ACCENT_A,
                  FS_TAG - 2, x=-3.40, w=1.90),
        self._mid(0.06, "有限維才有", "only in finite dimension", WARN,
                  FS_TAG - 2, x=-3.40, w=1.90))
  g.add(self._sym(-0.52, "V *   =   Hom ( V , ℝ )", ACCENT_B, FS_TAG, x=-3.40, w=3.40))
  g.add(self._panel(((0.86, "對偶空間是有界線性泛函的集合",
                      "the dual is the set of bounded linear functionals", ACCENT_B),
                     (0.20, "每個泛函作用上去都收斂，就叫弱收斂",
                      "convergence under every one of them is called weak convergence",
                      ACCENT_C),
                     (-0.46, "定理 12.1：有限維時兩者是同一件事",
                      "theorem 12.1: in finite dimension the two coincide", WARN))))
  return g.add(self._foot("向右那個黃色箭頭在任何賦範空間都成立，理由就是前面那一行估計",
                          "the amber arrow to the right holds in any normed space, for the reason given by the estimate made earlier",
                          ACCENT_A,
                          "向左那個紅色箭頭是定理 12.1 的內容，而它的證明要用到「維數有限」這件事",
                          "the red arrow back is the content of theorem 12.1, and its proof is where finite dimension is used"))

 def _integral(self):
  cx, cy, s = -5.35, -0.42, 0.92
  g = VGroup(self._plane(cx, cy, s, xspan=1.20, yspan=1.20, back=0.28))
  g.add(self._arc(cx, cy, s, f, ACCENT_B))
  g.add(self._arr([cx, cy, 0], [cx + s * INT[0], cy + s * INT[1], 0], ACCENT_A,
                  sw=2.8, tl=0.13))
  g.add(self._sym(cy + s * INT[1] + 0.22, f"∫ f  =  ⟨ {INT[0]:.0f} , {INT[1]:.0f} ⟩",
                  ACCENT_A, FS_TAG - 2, x=cx + s + 0.62, w=1.90))
  ox, oy, sx, sy = -2.95, -0.42, 0.99, 0.62
  g.add(self._frame(ox, oy, 1.74, 0.86, down=0.18))
  for k in range(15):
   t = TA + k * (TB - TA) / 14
   g.add(Line([ox + sx * t, oy, 0], [ox + sx * t, oy + sy * ap(L1, f(t)), 0],
              color=DIM, stroke_width=1.1))
  g.add(self._graph(ox, oy, sx, sy, L1, ACCENT_A))
  g.add(self._sym(oy + 0.86, f"{AREA:.4f}", ACCENT_A, FS_TAG - 2, x=ox + 1.20, w=1.10))
  g.add(self._table((("      λ            ∫ λ ∘ f        λ ( ∫ f )", DIM),)
                    + tuple((f"⟨ {l[0]:.2f} , {l[1]:.2f} ⟩      {q:.4f}        {v:.4f}",
                             ACCENT_A if l == L1 else ACCENT_C)
                            for l, q, v in INT_ROWS), y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, f"五個泛函都對得上，最大誤差 {INT_ERR:.0e}",
                  f"all five functionals agree, largest error {INT_ERR:.0e}", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"右邊那塊陰影是第一個泛函複合後的積分，{AREA:.4f}，正好是黃色箭頭那個向量在它下面的值",
                          f"the shaded area on the right is the integral of the first composite, {AREA:.4f}, which is exactly the value the amber vector takes under it",
                          ACCENT_A,
                          "積分的弱定義就是這樣：∫f 是那個唯一的向量，使每個泛函在它上面的值等於複合的積分",
                          "that is the weak definition: the integral is the unique vector on which every functional takes the value of the integral of the composite"))

 def _secondual(self):
  g = VGroup()
  for cx, lab, col in ((-5.05, "V *", ACCENT_B), (-2.35, "ℝ", ACCENT_C)):
   g.add(self._rect(cx, 0.72, 0.58, 0.26, col),
         self._sym(0.72, lab, col, FS_TAG + 1, x=cx, w=0.95))
  g.add(self._arr([-4.42, 0.72, 0], [-2.98, 0.72, 0], ACCENT_A, sw=2.2, tl=0.11))
  g.add(self._sym(1.04, "λ  ↦  ∫ λ ∘ f", ACCENT_A, FS_TAG - 1, x=-3.70, w=2.60))
  for cx, lab, col in ((-5.05, "V * *", ACCENT_C), (-2.35, "V", ACCENT_B)):
   g.add(self._rect(cx, -0.02, 0.58, 0.26, col),
         self._sym(-0.02, lab, col, FS_TAG + 1, x=cx, w=0.95))
  g.add(self._sym(-0.02, "≅", ACCENT_A, FS_TAG + 2, x=-3.70, w=0.70))
  g.add(self._dash([-5.05, 0.44, 0], [-5.05, 0.26, 0], DIM, n=3, sw=1.4))
  g.add(self._sym(-0.52, f"λ  =  2 λ ₁  −  3 λ ₂        {LIN_L:.4f}   =   {LIN_R:.4f}",
                  ACCENT_C, FS_TAG - 1, x=-3.70, w=4.60))
  g.add(self._panel(((0.86, "那個對應對泛函是線性的",
                      "that correspondence is linear in the functional", ACCENT_A),
                     (0.20, "所以它是二次對偶空間裡的一個元素",
                      "so it is an element of the second dual", ACCENT_C),
                     (-0.46, "第 2 章定理 3.2：那裡每個元素都由唯一一個向量給出",
                      "chapter 2 theorem 3.2: each element there comes from one vector",
                      ACCENT_B))))
  return g.add(self._foot("紫色那一行是線性的檢查：把 λ 換成 2 λ ₁ 減 3 λ ₂，積分照著同樣的組合走",
                          "the purple line checks linearity: replacing the functional by that combination sends the integral to the same combination",
                          ACCENT_A,
                          "有了唯一性，「定義成那個向量」才合法；而這個定義天生就讓積分跟泛函交換",
                          "uniqueness is what makes the definition legitimate, and the definition makes integration commute with functionals by construction"))

 def _derivative(self):
  ox, oy, sx, sy = -5.45, -0.28, 1.95, 0.72
  g = VGroup(self._frame(ox, oy, 3.30, 0.95, down=0.42))
  g.add(self._graph(ox, oy, sx, sy, DER_L, ACCENT_B, n=80))
  px, py = ox + sx * X0, oy + sy * ap(DER_L, f(X0))
  m = sy * DER_TRUE / sx
  g.add(Line([px - 0.95, py - 0.95 * m, 0], [px + 0.95, py + 0.95 * m, 0],
             color=WARN, stroke_width=2.6))
  g.add(Dot([px, py, 0], radius=0.062, color=ACCENT_A))
  g.add(self._dash([px, oy, 0], [px, py, 0], DIM, n=4, sw=1.2))
  g.add(self._sym(oy - 0.26, f"x ₀  =  {X0:.1f}", DIM, FS_TAG - 2, x=px, w=1.10))
  g.add(self._sym(py + 0.40, "λ ₂ ∘ f", ACCENT_B, FS_TAG - 2, x=px - 0.86, w=1.10))
  g.add(self._table((("     h        Δ λ ₂ ∘ f / 2 h         | · − λ ₂ ( f ′ ) |", DIM),)
                    + tuple((f"  {h:.3f}         {cd:.6f}              {er:.1e}", ACCENT_C)
                            for (h, cd), er in zip(DER_ROWS, DER_ERR))
                    + ((f"                 λ ₂ ( f ′ ( x ₀ ) )  =  {DER_TRUE:.6f}", ACCENT_A),),
                    y0=0.80, dy=0.32))
  g.add(self._mid(-0.86, "步長縮十倍，誤差縮一百倍",
                  "ten times the step, a hundred times the error", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("紅色那條直線畫的就是那個導數，青綠色是複合出來的實值函數，切點在 x ₀",
                          "the red line is that derivative, the teal curve is the composite, and they touch at the marked point",
                          ACCENT_A,
                          "把泛函映到它在 x ₀ 的導數也是線性的，所以同樣有唯一的向量對每個泛函成立——那就是 f 撇",
                          "sending a functional to that derivative is linear too, so again one vector satisfies the identity for every functional, and that vector is the derivative"))

 def _ftc(self):
  cx, cy, s = -5.20, -0.62, 1.32
  g = VGroup(self._plane(cx, cy, s, xspan=1.30, yspan=1.40, back=0.22))
  g.add(self._arc(cx, cy, s, f, ACCENT_B))
  g.add(self._arc(cx, cy, s, Fx, ACCENT_C))
  g.add(self._arr([cx, cy, 0], [cx + s * f(X0)[0], cy + s * f(X0)[1], 0], ACCENT_B,
                  sw=2.4, tl=0.12))
  fx, fy = cx + s * Fx(X0)[0], cy + s * Fx(X0)[1]
  g.add(Dot([fx, fy, 0], radius=0.062, color=ACCENT_A))
  g.add(self._arr([fx, fy, 0], [fx + s * f(X0)[0], fy + s * f(X0)[1], 0], WARN,
                  sw=2.4, tl=0.12))
  g.add(self._sym(cy + s * 0.30, "f", ACCENT_B, FS_TAG - 1, x=cx + s * 1.15, w=0.55),
        self._sym(cy + s * 0.42, "F", ACCENT_C, FS_TAG - 1, x=cx + s * 0.20, w=0.55))
  g.add(self._table((("     h      Δ λ ₁ ∘ F / 2 h        | · − λ ₁ ( f ( x ₀ ) ) |", DIM),)
                    + tuple((f"  {h:.3f}        {cd:.6f}             {er:.1e}", ACCENT_C)
                            for (h, cd), er in zip(FTC_ROWS, FTC_ERR))
                    + ((f"                λ ₁ ( f ( x ₀ ) )  =  {FTC_TRUE:.6f}", ACCENT_A),),
                    y0=0.80, dy=0.32))
  g.add(self._mid(-0.86, f"五個泛函一起看，誤差 {FTC_MAX:.0e}",
                  f"taking all five functionals at once, error {FTC_MAX:.0e}", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("紫色那條是 F，它在 x ₀ 的紅色切向量跟青綠色那個位置向量一樣——這就是 F 撇 等於 f",
                          "the purple curve is F, and the red tangent vector at the marked point equals the teal position vector, which is what the theorem says",
                          ACCENT_A,
                          "弱定義給出複合等於複合的積分，標準的基本定理把它微分掉，再翻回來就得到 F 可微",
                          "the weak definition turns the composite into an integral, the standard theorem differentiates it, and the weak definition of the derivative turns the answer back"))

 def _tangent(self):
  cx, cy, s = -5.05, -0.15, 0.46
  g = VGroup(self._plane(cx, cy, s, xspan=2.30, yspan=2.30, back=2.30))
  g.add(self._curve([[cx + s * v[0], cy + s * v[1], 0] for v in PRIM]
                    + [[cx + s * PRIM[0][0], cy + s * PRIM[0][1], 0]], ACCENT_B, sw=2.0))
  g.add(self._curve([[cx + s * v[0], cy + s * v[1], 0] for v in EDGE], WARN, sw=3.2))
  for u0, u1 in ((2.0, 2.55), (0.0, -0.55)):
   g.add(self._dash([cx + s * u0, cy + s * (2.0 - u0), 0],
                    [cx + s * u1, cy + s * (2.0 - u1), 0], WARN, n=4, sw=1.8))
  g.add(self._pt(cx, cy, s, INT, ACCENT_A, r=0.070))
  g.add(self._sym(cy + s * INT[1] + 0.26, "α", ACCENT_A, FS_TAG - 1,
                  x=cx + s * INT[0] + 0.24, w=0.60))
  ox, oy, sx, sy = -2.80, -0.62, 0.46, 0.55
  g.add(self._frame(ox, oy, 2.00, 1.30, down=0.14))
  g.add(self._curve([[ox + sx * 4.0 * k / 256, oy + sy * abs(ap(dual_sphere(k, 256), INT)), 0]
                     for k in range(257)], ACCENT_C, sw=2.0))
  g.add(self._dash([ox, oy + sy * SUP, 0], [ox + 2.00, oy + sy * SUP, 0], ACCENT_A,
                   n=14, sw=1.4))
  g.add(self._sym(oy + sy * SUP + 0.24, f"{SUP:.4f}", ACCENT_A, FS_TAG - 2,
                  x=ox + 0.60, w=1.20))
  g.add(self._sym(oy - 0.22, "| λ ( α ) |  ,   ‖ λ ‖  =  1", ACCENT_C, FS_TAG - 2,
                  x=ox + 1.00, w=2.30))
  g.add(self._table(((f"‖ α ‖ ₁   =   {NRM:.4f}", ACCENT_B),
                     (f"sup | λ ( α ) | / ‖ λ ‖   =   {SUP:.4f}", ACCENT_A),
                     (f"λ   =   ⟨ {NORMING[0][0]:.0f} , {NORMING[0][1]:.0f} ⟩", ACCENT_A),
                     (f"{SUP:.4f}   >   {SECOND:.4f}      ( λ ≠ ± ⟨ 1 , 1 ⟩ )", ACCENT_C),
                     (f"{TOUCH:d} / {len(PRIM):d}", WARN)), y0=0.80, dy=0.34))
  g.add(self._mid(-0.90, "紅色那一整條邊就是切線碰到菱形的地方",
                  "the whole red edge is where the tangent line meets the diamond", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"定理 12.2 要的是一個範數一的泛函把 ‖ α ‖ 取到：取樣 {KD:d} 個裡只有 ⟨ 1 , 1 ⟩ 與它的負號取到 {SUP:.4f}",
                          f"theorem 12.2 asks for a functional of norm one attaining the norm: of {KD:d} sampled, only that pair and its negative reach {SUP:.4f}",
                          ACCENT_A,
                          f"幾何上就是在 α 那裡的切超平面，而在一範數下它含著菱形整條邊（取樣 {len(PRIM):d} 點裡有 {TOUCH:d} 點），書上說這種平面顯然存在但不證",
                          f"geometrically a hyperplane tangent there, which under the one-norm contains a whole edge, {TOUCH:d} of {len(PRIM):d} sampled points, and the book states this without proof"))

 def _closing(self):
  g = VGroup()
  y1, y2, x0 = 0.62, 0.10, -5.70
  for y, val, col in ((y1, NRM, ACCENT_B), (y2, BOUND, WARN)):
   g.add(Line([x0, y, 0], [x0 + BAR * val, y, 0], color=col, stroke_width=7.0))
   g.add(self._sym(y, f"{val:.4f}", col, FS_TAG - 1, x=x0 + BAR * val + 0.50, w=1.30))
  g.add(self._dash([x0 + BAR * NRM, y1 - 0.16, 0], [x0 + BAR * NRM, y2 + 0.16, 0],
                   DIM, n=3, sw=1.2))
  g.add(self._sym(-0.34, f"‖ ∫ f ‖ ₁   /   ( b − a ) ‖ f ‖ ∞   =   {RATIO:.4f}", ACCENT_A,
                  FS_TAG - 1, x=-3.90, w=4.40))
  g.add(self._sym(-0.86, f"‖ f ‖ ∞  =  {FINF:.4f}        b − a  =  {TB - TA:.4f}", ACCENT_C,
                  FS_TAG - 1, x=-3.90, w=4.40))
  g.add(self._panel(((0.90, "假設了定理 12.2，剩下就是一串不等式",
                      "granting theorem 12.2, the rest is a chain", ACCENT_A),
                     (0.24, "值 ≤ 長度 × 複合的最大值 ≤ 長度 × ‖ λ ‖ × 上界範數",
                      "value ≤ length × max of the composite ≤ length × ‖ λ ‖ × uniform norm",
                      ACCENT_C),
                     (-0.42, "第 4 章到此結束，下一章是純量積空間",
                      "chapter 4 ends here, and scalar product spaces come next", WARN))))
  return g.add(self._foot(f"兩條橫線是同一把尺畫的：每一單位 {BAR:.2f} 個螢幕單位。青綠色是 ‖ ∫ f ‖ ₁，紅色是區間長度乘上上界範數",
                          f"the two bars share one scale, {BAR:.2f} screen units per unit: teal is the norm of the integral, red is the length times the uniform norm",
                          ACCENT_A,
                          f"不等式成立而且有實在的差距——比值 {RATIO:.4f}，不是偽裝的等式；這是弱方法唯一拿不到的那一步",
                          f"the inequality holds with a real gap, ratio {RATIO:.4f}, not an equality in disguise, and it is the one step weak methods do not reach"))

 def stage(self):
  a, b, c = self._opening(), self._forward(), self._converse()
  d, e, f_ = self._dropone(), self._weakdef(), self._integral()
  h, i, j = self._secondual(), self._derivative(), self._ftc()
  k, l = self._tangent(), self._closing()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE67ZH, AdvCalcE67EN = make(AdvCalcE67Base, "67", prefix="AdvCalcE")
