"""advcalc E68 -- chapter 5, section 1 (book pp. 247-251): scalar products.

The chapter opens by asking what is behind the two-norms, and the answer is the
scalar product.  Section 1 is the whole apparatus: the three conditions (linear
in the first variable, symmetric, positive definite), the semiscalar product
when the third is weakened, the two examples that explain both two-norms, the
Schwarz inequality and the one-line proof that a quadratic which never changes
sign has no positive discriminant, the corollary that the scalar product norm is
a norm, the pre-Hilbert / Hilbert / Euclidean vocabulary, and then orthogonality:
Lemma 1.1 (orthogonal to a set means orthogonal to the closed span, so every
orthogonal complement is a closed subspace) and Lemma 1.2 (the parallelogram law
and the Pythagorean theorem), closing on the corollary that orthogonal nonzero
vectors are independent.

Section 1's content ends on book page 251, where exercises 1.1 to 1.10 begin;
they run to 252, where section 2 starts.  The chapter intro and the section
heading are both on 247-248, so the episode covers 247-251.  OUTLINE gives the
chapter as 248-266 without a per-section breakdown -- that breakdown is added to
OUTLINE.md with this episode, from the section headings in the book itself.

Two concrete spaces carry every number on screen: the plane under the Euclidean
norm, and C([0,1]) under (f, g) = the integral of f g.  The Schwarz proof's
quadratic is drawn for two pairs, one nearly proportional (ratio 0.9691, the
parabola dipping to 0.0203) and one not (0.5000, dipping to 0.2500), so the
minimum of the parabola is visibly the slack in the inequality.  Beat 0 asks
which norms come from a scalar product and beat 10 answers it: the parallelogram
law holds for the two-norm and fails for the one- and sup-norms, computed on the
same pair of vectors.
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


def simpson(g, a, b, n=2000):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


# ── the two spaces every number lives in ───────────────────────────────
def sp(f, g, a=0.0, b=1.0):
 """The scalar product on C([a, b]): the integral of the product."""
 return simpson(lambda t: f(t) * g(t), a, b)


def nm(f, a=0.0, b=1.0):
 return math.sqrt(sp(f, f, a, b))


def dot(x, y):
 return x[0] * y[0] + x[1] * y[1]


def n2(v):
 return math.sqrt(dot(v, v))


def n1(v):
 return abs(v[0]) + abs(v[1])


def ninf(v):
 return max(abs(v[0]), abs(v[1]))


FT = lambda t: t
FE = math.exp
FM = lambda t: 1.0 - t
FO = lambda t: 1.0
FC = lambda t: math.cos(2.0 * math.pi * t)

# ── beat 1: the three conditions, checked on that product ──────────────
LIN_L = sp(lambda t: 2.0 * FT(t) + 3.0 * FM(t), FE)
LIN_R = 2.0 * sp(FT, FE) + 3.0 * sp(FM, FE)
assert abs(LIN_L - LIN_R) < 1e-12, "linear in the first variable"
SYM = sp(FT, FE) - sp(FE, FT)
assert abs(SYM) < 1e-15, "and symmetric"
POS = sp(FT, FT)
assert POS > 0.3, "and positive definite, which is what the third condition asks"
PROD_AREA = sp(FT, FE)
assert abs(PROD_AREA - 1.0) < 1e-12, "the integral of t times e to the t is exactly one"

# ── beat 2: the two examples ───────────────────────────────────────────
XV, YV = (1.2, 0.3), (0.4, 1.0)
XY = dot(XV, YV)
assert abs(XY - (XV[0] * YV[0] + XV[1] * YV[1])) < 1e-15, "the sum of coordinate products"

# ── beat 3: the quadratic form, and what positive definiteness means ───
QA, QB, QC = 2.0, 0.8, 1.0
assert QB * QB < QA * QC, "the condition of exercise 1.6, and what makes the form definite"


def qform(x, a=QA, b=QB, c=QC):
 return a * x[0] * x[0] + 2.0 * b * x[0] * x[1] + c * x[1] * x[1]


DIRS = [(math.cos(2 * math.pi * k / 720), math.sin(2 * math.pi * k / 720)) for k in range(720)]
Q_MIN = min(qform(d) for d in DIRS)
Q_MAX = max(qform(d) for d in DIRS)
assert Q_MIN > 0.5, "definite: the form is bounded away from zero in every direction"
QB_BAD = 2.0
Q_BAD = min(qform(d, b=QB_BAD) for d in DIRS)
assert QB_BAD ** 2 > QA * QC and Q_BAD < -0.5, \
    "and with that condition broken the form goes negative somewhere"

# ── beats 4 and 5: the quadratic in t whose sign proves Schwarz ────────
PAIRS = ((FT, FE), (FT, FM))
PAR = []
for _f, _g in PAIRS:
 _A, _B, _C = sp(_g, _g), sp(_f, _g), sp(_f, _f)
 PAR.append((_A, _B, _C, _B / _A, _C - _B * _B / _A, 4.0 * _B * _B - 4.0 * _A * _C))
for _A, _B, _C, _t, _m, _d in PAR:
 assert _m > 0 and abs(_d + 4.0 * _A * _m) < 1e-12, \
     "the minimum is the discriminant over minus four a, so one sign settles both"
 assert _d <= 0.0, "and the discriminant is what Schwarz says"
SCHW = [(abs(sp(f, g)), nm(f) * nm(g)) for f, g in PAIRS]
for _l, _r in SCHW:
 assert _l <= _r, "the inequality itself"
assert SCHW[0][0] / SCHW[0][1] > 0.96 and SCHW[1][0] / SCHW[1][1] < 0.51, \
    "one pair nearly proportional, the other far from it: the two parabolas differ by that"


def qt(t, k=0):
 A, B, C = PAR[k][0], PAR[k][1], PAR[k][2]
 return A * t * t - 2.0 * B * t + C


# ── beat 6: the norm, the triangle inequality, homogeneity ─────────────
TRI = [(nm(lambda t: f(t) + g(t)), nm(f) + nm(g)) for f, g in PAIRS]
for _l, _r in TRI:
 assert _l <= _r + 1e-12, "the triangle inequality, which is Schwarz on the middle term"
HOM_C = -2.5
HOM = (nm(lambda t: HOM_C * FE(t)), abs(HOM_C) * nm(FE))
assert abs(HOM[0] - HOM[1]) < 1e-12, "and homogeneity is a direct computation"
# the picture is the plane, where a triangle can actually be drawn
TRI_PL = (n2(XV), n2(YV), n2((XV[0] + YV[0], XV[1] + YV[1])))
assert TRI_PL[2] < TRI_PL[0] + TRI_PL[1], "the drawn triangle satisfies it too"
TRI_PL_R = TRI_PL[2] / (TRI_PL[0] + TRI_PL[1])
assert 0.85 < TRI_PL_R < 0.92, "with a gap wide enough to see in the drawing"

# ── beat 7: C([0, 1]) is not complete in the two-norm (exercise 1.10) ──
NS = (2, 4, 8, 16)


def ramp(n):
 """The continuous ramp of width 1/n across the jump of the step function."""
 h = 0.5 / n

 def f(t):
  if t <= 0.5 - h:
   return 1.0
  if t >= 0.5 + h:
   return 0.0
  return (0.5 + h - t) / (2.0 * h)
 return f


def kstep(t):
 return 1.0 if t < 0.5 else 0.0


# With the kink at the jump, Simpson is the wrong tool; the integral is a pair of
# triangles and comes out in closed form, checked against a fine Riemann sum.
RAMP = []
for _n in NS:
 _h = 0.5 / _n
 _ex = math.sqrt(_h / 6.0)
 _num = math.sqrt(sum((ramp(_n)(k / 60000.0) - kstep(k / 60000.0)) ** 2
                      for k in range(60000)) / 60000.0)
 assert abs(_ex - _num) < 2e-4, "the closed form is the integral"
 RAMP.append((_n, _ex))
for (_, _a), (_, _b) in zip(RAMP, RAMP[1:]):
 assert _b < _a, "and it goes to zero"
assert RAMP[-1][1] < 0.08, "so the sequence converges to a step function in the two-norm"

# ── beat 8: orthogonality, and the angle the scalar product defines ────
ANG = []
for _f, _g in ((FT, FE), (FT, FM), (FO, FC)):
 _c = sp(_f, _g) / (nm(_f) * nm(_g))
 ANG.append((math.degrees(math.acos(max(-1.0, min(1.0, _c)))), _c))
assert abs(ANG[0][0] - 14.29) < 0.05 and abs(ANG[1][0] - 60.0) < 0.05, \
    "the first pair is nearly parallel, the second is sixty degrees apart"
ORTH_IP = abs(sp(FO, FC))
assert abs(ANG[2][1]) < 1e-12 and ORTH_IP < 1e-12, "and the third pair is orthogonal"

# ── beats 9 and 10: the orthogonal family the next chapter expands in ──
SIN = [(k, (lambda k: (lambda t: math.sin(k * t)))(k)) for k in (1, 2, 3, 4)]
GRAM = [[sp(a, b, 0.0, math.pi) for _, b in SIN] for _, a in SIN]
for i in range(4):
 for j in range(4):
  if i == j:
   assert abs(GRAM[i][j] - math.pi / 2) < 1e-9, "each has square norm pi over two"
  else:
   assert abs(GRAM[i][j]) < 1e-9, "and distinct ones are orthogonal"
SPAN = ((1.0, 0.0), (0.0, 1.0), (2.0, -3.0), (-0.7, 1.4))
L11 = [(c1, c2, sp(SIN[3][1],
                   (lambda c1, c2: (lambda t: c1 * SIN[0][1](t) + c2 * SIN[1][1](t)))(c1, c2),
                   0.0, math.pi))
       for c1, c2 in SPAN]
L11_MAX = max(abs(v) for _, _, v in L11)
assert L11_MAX < 1e-9, \
    "orthogonal to the two of them means orthogonal to every combination: lemma 1.1"
XC = (0.5, -1.0, 0.3, 0.8)
SUM_SQ = nm(lambda t: sum(x * s(t) for x, (_, s) in zip(XC, SIN)), 0.0, math.pi) ** 2
DIAG_SQ = sum(x * x * GRAM[i][i] for i, x in enumerate(XC))
assert abs(SUM_SQ - DIAG_SQ) < 1e-9, "the mixed terms drop out, which is lemma 1.2"
assert SUM_SQ > 3.0, "and a nonzero coefficient vector gives a nonzero vector: independence"

# ── beat 10: the parallelogram law, and the norms that fail it ─────────
APL, BPL = XV, YV
SUMV = (APL[0] + BPL[0], APL[1] + BPL[1])
DIFV = (APL[0] - BPL[0], APL[1] - BPL[1])
PARA = []
for _f in (n2, n1, ninf):
 PARA.append((_f(SUMV) ** 2 + _f(DIFV) ** 2, 2.0 * (_f(APL) ** 2 + _f(BPL) ** 2)))
assert abs(PARA[0][0] - PARA[0][1]) < 1e-12, "the two-norm obeys the law"
PARA_GAP = [abs(a - b) for a, b in PARA]
assert PARA_GAP[1] > 2.0 and PARA_GAP[2] > 1.5, \
    "and the one- and sup-norms miss it by a wide margin, which is beat 0's question answered"
PARA_F = (nm(lambda t: FT(t) + FE(t)) ** 2 + nm(lambda t: FT(t) - FE(t)) ** 2,
          2.0 * (nm(FT) ** 2 + nm(FE) ** 2))
assert abs(PARA_F[0] - PARA_F[1]) < 1e-12, "and it holds in the function space too"
PYTH = (nm(lambda t: FO(t) + FC(t)) ** 2, nm(FO) ** 2 + nm(FC) ** 2)
assert abs(PYTH[0] - PYTH[1]) < 1e-9, "the Pythagorean theorem on the orthogonal pair"


class AdvCalcE68Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 68

 MODE_LABEL = {
  0: {"zh": "two-norm 背後是什麼", "en": "what lies behind the two-norms"},
  1: {"zh": "三條定義，與半純量積", "en": "three conditions, and the semiscalar case"},
  2: {"zh": "兩個例子", "en": "the two examples"},
  3: {"zh": "對稱雙線性泛函與它的二次形式", "en": "a symmetric bilinear functional and its form"},
  4: {"zh": "定理 1.1：Schwarz 不等式", "en": "theorem 1.1: the Schwarz inequality"},
  5: {"zh": "同一個二次式的第二種讀法", "en": "the same quadratic, read a second way"},
  6: {"zh": "推論：那個平方根是範數", "en": "the corollary: that square root is a norm"},
  7: {"zh": "pre-Hilbert 與 Hilbert", "en": "pre-Hilbert and Hilbert"},
  8: {"zh": "正交，以及純量積定出的夾角", "en": "orthogonality, and the angle it defines"},
  9: {"zh": "引理 1.1：正交補是閉子空間", "en": "lemma 1.1: the complement is closed"},
  10: {"zh": "引理 1.2 與推論", "en": "lemma 1.2, and the corollary"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.32, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plane(self, cx, cy, s, xspan=1.15, yspan=1.05, back=0.45):
  return VGroup(Line([cx - s * back, cy, 0], [cx + s * xspan, cy, 0],
                     color=DIM, stroke_width=1.3),
                Line([cx, cy - s * back, 0], [cx, cy + s * yspan, 0],
                     color=DIM, stroke_width=1.3))

 def _frame(self, ox, oy, w, h, down=0.30, back=0.12):
  return VGroup(Line([ox - back, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=1.0, sw=2.4, n=72):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _hatch(self, ox, oy, sx, sy, f, col=DIM, t0=0.0, t1=1.0, n=14, sw=1.1):
  g = VGroup()
  for k in range(n + 1):
   t = t0 + k * (t1 - t0) / n
   g.add(Line([ox + sx * t, oy, 0], [ox + sx * t, oy + sy * f(t), 0],
              color=col, stroke_width=sw))
  return g

 def _sphere(self, cx, cy, s, norm, col, sw=2.2, n=144):
  """The unit sphere of a norm, drawn from the norm itself."""
  pts = []
  for k in range(n + 1):
   th = 2.0 * math.pi * k / n
   d = (math.cos(th), math.sin(th))
   r = 1.0 / norm(d)
   pts.append([cx + s * r * d[0], cy + s * r * d[1], 0])
  return self._curve(pts, col, sw=sw)

 def _level(self, cx, cy, s, q, col, sw=2.2, n=144):
  """The level curve q = 1 of a positive definite form, the same way."""
  pts = []
  for k in range(n + 1):
   th = 2.0 * math.pi * k / n
   d = (math.cos(th), math.sin(th))
   r = 1.0 / math.sqrt(q(d))
   pts.append([cx + s * r * d[0], cy + s * r * d[1], 0])
  return self._curve(pts, col, sw=sw)

 def _vec(self, cx, cy, s, v, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=sw, tl=tl)

 # ── beats ─────────────────────────────────────────────────────────
 def _opening(self):
  g = VGroup()
  for cx, norm, lab, col in ((-5.25, n2, "‖ · ‖ ₂", ACCENT_B),
                             (-3.55, n1, "‖ · ‖ ₁", ACCENT_C),
                             (-1.85, ninf, "‖ · ‖ ∞", WARN)):
   g.add(self._sphere(cx, 0.10, 0.56, norm, col))
   g.add(self._sym(-0.76, lab, col, FS_TAG, x=cx, w=1.30))
  g.add(self._sym(0.98, "?", ACCENT_A, FS_TAG + 4, x=-3.55, w=0.60))
  g.add(self._panel(((0.86, "這一章要看的是 two-norm 背後的東西",
                      "the chapter looks at what lies behind the two-norms", ACCENT_B),
                     (0.20, "答案是純量積，而它帶著整套歐氏幾何",
                      "the answer is the scalar product, and it carries Euclidean geometry",
                      ACCENT_C),
                     (-0.46, "夾角、垂直、畢氏定理，全都跟著來",
                      "angles, perpendicularity and the Pythagorean theorem all come with it",
                      WARN))))
  return g.add(self._foot("三條曲線都是某個範數的單位球面，都是從那個範數本身算出來畫的——問題是：哪一個是從純量積來的",
                          "each curve is the unit sphere of one norm, drawn from that norm itself, and the question is which of them comes from a scalar product",
                          ACCENT_A,
                          "無限維時衝擊最大：正交基大量存在，基底展開變成收斂級數，Fourier 級數就是一例；完備的就叫 Hilbert 空間",
                          "the impact is greatest in infinite dimension, where orthogonal bases abound and a basis expansion becomes a convergent series, the Fourier series being one"))

 def _define(self):
  ox, sx = -5.60, 2.40
  oy, sy = 0.26, 0.19
  g = VGroup(self._frame(ox, oy, 2.70, 0.62, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, FT, ACCENT_B),
        self._fcurve(ox, oy, sx, sy, FE, ACCENT_C))
  for f, lab, col in ((FT, "f", ACCENT_B), (FE, "g", ACCENT_C)):
   g.add(self._sym(oy + sy * f(1.0), lab, col, FS_TAG - 1, x=ox + sx + 0.28, w=0.70))
  py, psy = -0.78, 0.30
  g.add(self._frame(ox, py, 2.70, 0.95, down=0.10))
  g.add(self._hatch(ox, py, sx, psy, lambda t: FT(t) * FE(t)))
  g.add(self._fcurve(ox, py, sx, psy, lambda t: FT(t) * FE(t), ACCENT_A))
  g.add(self._sym(py + psy * FT(1.0) * FE(1.0), "f g", ACCENT_A, FS_TAG - 1,
                  x=ox + sx + 0.34, w=0.80))
  g.add(self._sym(py + 0.62, f"{PROD_AREA:.4f}", ACCENT_A, FS_TAG - 2,
                  x=ox + 0.75, w=1.20))
  g.add(self._table((("     ( 2 f  +  3 h , g )         2 ( f , g )  +  3 ( h , g )", DIM),
                     (f"        {LIN_L:.4f}                      {LIN_R:.4f}", ACCENT_B),
                     (f"     ( f , g )  −  ( g , f )    =    {abs(SYM):.1e}", ACCENT_C),
                     (f"     ( f , f )   =   {POS:.4f}   >   0", WARN)), y0=0.86, dy=0.36))
  g.add(self._mid(-0.86, "三條都在同一個例子上驗過",
                  "all three conditions checked on the same example", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"黃色那條是 f 乘 g，它下面那塊的面積就是純量積的值 {PROD_AREA:.4f}",
                          f"the amber curve is f times g, and the area under it is the value of the scalar product, {PROD_AREA:.4f}",
                          ACCENT_A,
                          "把正定換成「對每個向量都大於等於零」這個較弱的條件，就叫半純量積——Schwarz 對它一樣成立",
                          "weakening positive definiteness to mere non-negativity gives a semiscalar product, and Schwarz holds for that too"))

 def _examples(self):
  cx, cy, s = -5.05, -0.42, 0.92
  g = VGroup(self._plane(cx, cy, s, xspan=1.45, yspan=1.30, back=0.25))
  g.add(self._vec(cx, cy, s, XV, ACCENT_B), self._vec(cx, cy, s, YV, ACCENT_C))
  for v, lab, col in ((XV, "x", ACCENT_B), (YV, "y", ACCENT_C)):
   g.add(self._sym(cy + s * v[1] + 0.24, lab, col, FS_TAG - 1,
                   x=cx + s * v[0] + 0.22, w=0.70))
  g.add(self._sym(cy - 0.34, f"( x , y )  =  {XY:.4f}", ACCENT_A, FS_TAG - 1,
                  x=cx + 0.75, w=2.20))
  ox, oy, sx, sy = -2.60, -0.42, 1.35, 0.24
  g.add(self._frame(ox, oy, 1.55, 0.80, down=0.14))
  g.add(self._hatch(ox, oy, sx, sy, lambda t: FT(t) * FE(t), n=10))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: FT(t) * FE(t), ACCENT_A, sw=2.0))
  g.add(self._sym(oy + 0.86, f"( f , g )  =  {PROD_AREA:.4f}", ACCENT_A, FS_TAG - 2,
                  x=ox + 0.80, w=2.10))
  g.add(self._panel(((0.86, "ℝ ⁿ 上是座標乘積之和",
                      "on real n-space it is the sum of coordinate products", ACCENT_B),
                     (0.20, "連續函數上是 f 乘 g 的積分",
                      "on the continuous functions it is the integral of f times g", ACCENT_A),
                     (-0.46, "複空間要改成 Hermitian 對稱，交換時取共軛",
                      "a complex space needs Hermitian symmetry, conjugating on a swap", WARN))))
  return g.add(self._foot(f"左邊是平面上的例子：兩個座標乘積 {XV[0]:.1f}×{YV[0]:.1f} 與 {XV[1]:.1f}×{YV[1]:.1f} 加起來就是 {XY:.4f}",
                          f"on the left the plane example: the two coordinate products add up to {XY:.4f}",
                          ACCENT_A,
                          "這兩個例子等一下就會解釋兩個 two-norm 是從哪裡來的；書上明說這一章只做實數的情形",
                          "these two examples will explain where both two-norms come from, and the book says it studies only the real case"))

 def _form(self):
  cx, cy, s = -4.30, -0.10, 0.82
  g = VGroup(self._plane(cx, cy, s, xspan=1.70, yspan=1.55, back=1.70))
  g.add(self._level(cx, cy, s, qform, ACCENT_B))
  for d, col, lab, off in (((1.0, 0.0), ACCENT_C, "1 / √ a", (0.95, -0.42)),
                           ((0.0, 1.0), WARN, "1 / √ c", (-0.75, 0.30))):
   r = 1.0 / math.sqrt(qform(d))
   g.add(Dot([cx + s * r * d[0], cy + s * r * d[1], 0], radius=0.06, color=col))
   g.add(self._sym(cy + s * r * d[1] + off[1], lab, col, FS_TAG - 2,
                   x=cx + s * r * d[0] + off[0], w=1.10))
  g.add(self._sym(cy + s * 1.10, "q  =  1", ACCENT_B, FS_TAG - 1, x=cx + 1.20, w=1.30))
  g.add(self._table(((f"     q ( x )   =   {QA:.0f} x ₁ ²  +  2 ( {QB:.1f} ) x ₁ x ₂  +  x ₂ ²", DIM),
                     (f"     b ²   =   {QB * QB:.2f}    <    a c   =   {QA * QC:.2f}", ACCENT_B),
                     (f"     min q   =   {Q_MIN:.4f}        max q   =   {Q_MAX:.4f}", ACCENT_C),
                     (f"     b   =   {QB_BAD:.1f}     ⇒     min q   =   {Q_BAD:.4f}", WARN)),
                    y0=0.86, dy=0.36))
  g.add(self._mid(-0.86, "正定就是這條曲線是有界的橢圓",
                  "positive definiteness is what makes this curve a bounded oval", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("那條青綠色的曲線是 q = 1，直接從 q 算出來畫的：每個方向上取 1 除以根號 q",
                          "the teal curve is the level set q equals one, drawn straight from q by taking one over the square root in each direction",
                          ACCENT_A,
                          f"紅色那一列把 b 改成 {QB_BAD:.1f}，條件壞掉，q 在某些方向變成負的（{Q_BAD:.4f}），那條曲線就不再是橢圓",
                          f"the red row breaks the condition: with that b the form goes negative in some directions, {Q_BAD:.4f}, and the curve is no longer an oval"))

 def _schwarz(self):
  ox, oy, sx, sy = -5.45, -0.56, 2.95, 0.78
  g = VGroup(self._frame(ox, oy, sx * 0.95, 1.05, down=0.10, back=sx * 0.20))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: qt(t, 0), ACCENT_B, t0=-0.20, t1=0.90, n=80))
  A, B, C, TS, QM, D = PAR[0]
  g.add(Dot([ox + sx * TS, oy + sy * QM, 0], radius=0.065, color=WARN))
  g.add(self._sym(oy + 0.52, f"{QM:.4f}", WARN, FS_TAG - 2,
                  x=ox + sx * TS + 0.10, w=1.20))
  g.add(self._sym(oy + sy * qt(0.9, 0) + 0.02, "q ( t )", ACCENT_B, FS_TAG - 1,
                  x=ox + sx * 0.90 + 0.40, w=1.10))
  g.add(self._table((("     q ( t )   =   A t ²  −  2 B t  +  C", DIM),
                     (f"     A  =  {A:.4f}    B  =  {B:.4f}    C  =  {C:.4f}", ACCENT_B),
                     (f"     4 B ²  −  4 A C   =   {D:.4f}   ≤   0", WARN),
                     (f"     | ( f , g ) |   =   {SCHW[0][0]:.4f}", ACCENT_C),
                     (f"     √ ( f , f )  ·  √ ( g , g )   =   {SCHW[0][1]:.4f}", ACCENT_C)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "曲線從來不碰到 t 軸，判別式因此不能是正的",
                  "the curve never reaches the axis, so the discriminant cannot be positive",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("那條曲線是 ξ 減 t η 的自內積當成 t 的函數——它是自內積，所以對每個 t 都非負",
                          "the curve is the self-product of the first vector minus t times the second, as a function of t, and being a self-product it is never negative",
                          ACCENT_A,
                          f"不變號的二次式判別式不能是正的（這裡是 {D:.4f}），整理一下就是 Schwarz：{SCHW[0][0]:.4f} ≤ {SCHW[0][1]:.4f}",
                          f"a quadratic that never changes sign has no positive discriminant, {D:.4f} here, and rearranging that is Schwarz: {SCHW[0][0]:.4f} at most {SCHW[0][1]:.4f}"))

 def _second(self):
  ox, oy, sx, sy = -5.45, -0.56, 2.95, 0.78
  g = VGroup(self._frame(ox, oy, sx * 0.95, 1.05, down=0.10, back=sx * 0.20))
  for k, col in ((0, ACCENT_B), (1, ACCENT_C)):
   g.add(self._fcurve(ox, oy, sx, sy, lambda t, k=k: qt(t, k), col, t0=-0.20, t1=0.90, n=80))
   A, B, C, TS, QM, D = PAR[k]
   g.add(Dot([ox + sx * TS, oy + sy * QM, 0], radius=0.065, color=col))
   g.add(self._dash([ox + sx * TS, oy, 0], [ox + sx * TS, oy + sy * QM, 0], col, n=3, sw=1.2))
  g.add(self._table((("       t *      q ( t * )     | ( f , g ) | / ‖ f ‖ ‖ g ‖", DIM),
                     (f"     {PAR[0][3]:.4f}    {PAR[0][4]:.4f}          {SCHW[0][0] / SCHW[0][1]:.4f}",
                      ACCENT_B),
                     (f"     {PAR[1][3]:.4f}    {PAR[1][4]:.4f}          {SCHW[1][0] / SCHW[1][1]:.4f}",
                      ACCENT_C),
                     (f"     q ( t * )   =   ( f , f )  −  ( f , g ) ² / ( g , g )", DIM),
                     (f"     ( g , g )  =  0    ⇒    ( f , g )  =  0", WARN)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "最低點等於零，才是等號成立的時候",
                  "the minimum is zero exactly when equality holds", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"把 t 代成表上第一欄那個 t 星，二次式就化簡成 Schwarz：最低點 ( f , f ) − ( f , g ) ² / ( g , g ) 非負，整理一下就是不等式",
                          f"substituting the value of t in the first column simplifies the quadratic into Schwarz: the minimum is non-negative, and rearranging that is the inequality",
                          ACCENT_A,
                          f"青綠色那一對比值 {SCHW[0][0] / SCHW[0][1]:.4f}、最低點 {PAR[0][4]:.4f}；紫色那一對比值 {SCHW[1][0] / SCHW[1][1]:.4f}、最低點 {PAR[1][4]:.4f}。比值才是跟尺度無關的那一個，最低點還帶著 ( g , g ) 的大小",
                          f"the teal pair has ratio {SCHW[0][0] / SCHW[0][1]:.4f} and minimum {PAR[0][4]:.4f}, the purple one {SCHW[1][0] / SCHW[1][1]:.4f} and {PAR[1][4]:.4f}; the ratio is the scale-free measure, the minimum still carries the size of the second self-product"))

 def _norm(self):
  cx, cy, s = -5.15, -0.62, 1.05
  g = VGroup()
  g.add(self._vec(cx, cy, s, XV, ACCENT_B), self._vec(cx, cy, s, SUMV, ACCENT_A))
  g.add(self._arr([cx + s * XV[0], cy + s * XV[1], 0],
                  [cx + s * SUMV[0], cy + s * SUMV[1], 0], ACCENT_C, sw=2.6, tl=0.13))
  for v, lab, col, dx, dy in ((XV, "ξ", ACCENT_B, -0.02, -0.30),
                              (SUMV, "ξ + η", ACCENT_A, 0.52, 0.26)):
   g.add(self._sym(cy + s * v[1] + dy, lab, col, FS_TAG - 1,
                   x=cx + s * v[0] + dx, w=1.10))
  g.add(self._sym(cy + s * (XV[1] + SUMV[1]) / 2 + 0.02, "η", ACCENT_C, FS_TAG - 1,
                  x=cx + s * (XV[0] + SUMV[0]) / 2 + 0.30, w=0.60))
  g.add(self._table((("     ‖ f + g ‖           ‖ f ‖  +  ‖ g ‖", DIM),
                     (f"      {TRI[0][0]:.4f}              {TRI[0][1]:.4f}", ACCENT_B),
                     (f"      {TRI[1][0]:.4f}              {TRI[1][1]:.4f}", ACCENT_C),
                     (f"     ‖ c g ‖  =  {HOM[0]:.4f}   =   | c | ‖ g ‖", WARN),
                     (f"     | ( f , g ) |  ≤  ‖ f ‖ ‖ g ‖", DIM)), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "三角不等式就是 Schwarz 用在中間那一項",
                  "the triangle inequality is Schwarz applied to the middle term", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"左邊那個三角形畫在平面上（歐氏範數），三邊長算出來是 {TRI_PL[2]:.4f} ≤ {TRI_PL[0]:.4f} + {TRI_PL[1]:.4f}",
                          f"the triangle on the left is drawn in the plane under the Euclidean norm, and its three sides measure {TRI_PL[2]:.4f} at most {TRI_PL[0]:.4f} plus {TRI_PL[1]:.4f}",
                          ACCENT_A,
                          "右邊兩列是同一個不等式在連續函數空間裡的數字——第一對幾乎取到等號，因為它們幾乎成比例",
                          "the two rows on the right are the same inequality in the function space, the first pair nearly attaining equality because those two are nearly proportional"))

 def _hilbert(self):
  ox, oy, sx, sy = -5.70, -0.72, 3.30, 1.15
  g = VGroup(self._frame(ox, oy, 3.55, 1.45, down=0.14))
  for n, col in ((2, WARN), (4, ACCENT_C), (8, ACCENT_A)):
   g.add(self._fcurve(ox, oy, sx, sy, ramp(n), col, n=160, sw=1.8))
  g.add(Line([ox, oy + sy, 0], [ox + sx * 0.5, oy + sy, 0], color=ACCENT_B, stroke_width=3.4),
        Line([ox + sx * 0.5, oy, 0], [ox + sx, oy, 0], color=ACCENT_B, stroke_width=3.4))
  g.add(self._dash([ox + sx * 0.5, oy, 0], [ox + sx * 0.5, oy + sy, 0], ACCENT_B, n=4, sw=1.2))
  g.add(self._sym(oy + sy + 0.26, "k", ACCENT_B, FS_TAG - 1, x=ox + 0.45, w=0.60))
  g.add(self._table((("       n          ‖ f ₙ  −  k ‖ ₂", DIM),)
                    + tuple((f"     {n:3d}              {v:.4f}",
                             WARN if n == 2 else (ACCENT_C if n == 4 else ACCENT_A))
                            for n, v in RAMP), y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "極限在 two-norm 下存在，可是它不連續",
                  "the limit exists in the two-norm, but it is not continuous", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("青綠色那條是階梯函數 k，三條斜線是寬度 1／n 的連續斜坡——離跳躍點遠的地方它們跟 k 完全重合，所以那裡只看得到 k",
                          "the teal one is the step function and the three ramps are continuous, of width one over n; away from the jump they coincide with it exactly, so only the step is visible there",
                          ACCENT_A,
                          "習題 1.10：對任何連續函數 f 都有 ‖ f − k ‖ ₂ > 0，所以這個 Cauchy 列在連續函數裡沒有極限——pre-Hilbert 而非 Hilbert",
                          "exercise 1.10: every continuous function keeps a positive distance from k, so this Cauchy sequence has no limit among the continuous functions"))

 def _orthogonal(self):
  g = VGroup()
  for cx, (deg, cs), lab, col in ((-5.15, ANG[0], "f ,  g", ACCENT_B),
                                  (-3.45, ANG[1], "f ,  h", ACCENT_C),
                                  (-1.75, ANG[2], "u ,  v", WARN)):
   cy, r = -0.30, 0.68
   half = math.radians(deg) / 2.0
   for sgn in (1.0, -1.0):
    g.add(self._arr([cx, cy, 0],
                    [cx + r * math.cos(math.pi / 2 + sgn * half),
                     cy + r * math.sin(math.pi / 2 + sgn * half), 0], col, sw=2.4, tl=0.12))
   g.add(self._curve([[cx + 0.30 * math.cos(math.pi / 2 - half + 2 * half * k / 24),
                       cy + 0.30 * math.sin(math.pi / 2 - half + 2 * half * k / 24), 0]
                      for k in range(25)], DIM, sw=1.3))
   g.add(self._sym(cy + 0.86, f"{deg:.2f} °", col, FS_TAG - 1, x=cx, w=1.40),
         self._sym(cy - 0.30, lab, col, FS_TAG - 1, x=cx, w=1.40))
  g.add(self._panel(((0.86, "內積為零就說兩個向量垂直",
                      "a zero product is what orthogonal means", WARN),
                     (0.20, "餘弦定理給出內積等於兩長度乘夾角餘弦",
                      "the law of cosines gives the product as lengths times a cosine",
                      ACCENT_B),
                     (-0.46, "所以可以定義夾角，不過書上說用不到",
                      "so angles could be defined, though the book has no use for them",
                      ACCENT_C))))
  return g.add(self._foot(f"三個夾角都是從純量積算出來的：{ANG[0][0]:.2f}°、{ANG[1][0]:.2f}°、{ANG[2][0]:.2f}°。箭頭只畫方向，長度沒有照比例",
                          f"the three angles are computed from the scalar product, {ANG[0][0]:.2f}, {ANG[1][0]:.2f} and {ANG[2][0]:.2f} degrees, and the arrows show direction only, not length",
                          ACCENT_A,
                          f"最右邊那一對的內積是 {ORTH_IP:.0e}，也就是垂直；集合的正交與正交補都照這個定義推上去",
                          f"the product of the rightmost pair is {ORTH_IP:.0e}, which is orthogonality, and sets inherit the definition"))

 def _lemma1(self):
  ox, oy, sx, sy = -5.60, -0.15, 0.76, 0.52
  g = VGroup(self._frame(ox, oy, 2.70, 0.72, down=0.68))
  for (k, f), col in zip(SIN, (ACCENT_B, ACCENT_C, DIM, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy, f, col, t0=0.0, t1=math.pi, n=96,
                      sw=2.6 if k == 4 else 1.8))
  g.add(self._sym(oy + sy + 0.24, "s ₄", WARN, FS_TAG - 1, x=ox + 0.50, w=0.70))
  g.add(self._table((("     c ₁              c ₂          ( s ₄ , c ₁ s ₁ + c ₂ s ₂ )", DIM),)
                    + tuple((f"    {c1:5.1f}          {c2:5.1f}              {v:.1e}", ACCENT_C)
                            for c1, c2, v in L11)
                    + ((f"     ( s ᵢ , s ᵢ )   =   {GRAM[0][0]:.4f}", ACCENT_B),),
                    y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "跟兩條的任何組合都正交",
                  "orthogonal to every combination of the two", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"紅色那條是 s ₄，它跟前兩條的任何線性組合的內積最大只有 {L11_MAX:.0e}——這就是引理 1.1 的內容",
                          f"the red curve is the fourth sine, and its product with every linear combination of the first two is at most {L11_MAX:.0e}, which is lemma 1.1",
                          ACCENT_A,
                          "理由是純量積對一個變數既線性又連續，所以「垂直」這個條件在取線性包與取閉包之下都不會壞掉，正交補因此是閉子空間",
                          "the reason is that the scalar product is linear and continuous in one variable, so orthogonality survives spans and limits, and the complement is a closed subspace"))

 def _lemma2(self):
  cx, cy, s = -4.55, -0.46, 0.72
  g = VGroup()
  for a, b, col, sw in ((APL, SUMV, DIM, 1.6), (BPL, SUMV, DIM, 1.6)):
   g.add(Line([cx + s * a[0], cy + s * a[1], 0], [cx + s * b[0], cy + s * b[1], 0],
              color=col, stroke_width=sw))
  g.add(self._vec(cx, cy, s, APL, ACCENT_B), self._vec(cx, cy, s, BPL, ACCENT_C))
  g.add(self._vec(cx, cy, s, SUMV, ACCENT_A, sw=2.4))
  g.add(self._vec(cx, cy, s, DIFV, WARN, sw=2.4))
  for v, lab, col, dx, dy in ((APL, "α", ACCENT_B, 0.24, -0.26), (BPL, "β", ACCENT_C, 0.22, 0.24),
                              (SUMV, "α + β", ACCENT_A, 0.56, 0.24)):
   g.add(self._sym(cy + s * v[1] + dy, lab, col, FS_TAG - 1, x=cx + s * v[0] + dx, w=1.10))
  g.add(self._sym(cy + s * DIFV[1] - 0.02, "α − β", WARN, FS_TAG - 1,
                  x=cx + s * DIFV[0] + 0.78, w=1.10))
  g.add(self._table((("        ‖ α + β ‖ ² + ‖ α − β ‖ ²      2 ( ‖ α ‖ ² + ‖ β ‖ ² )", DIM),
                     (f"  ‖ · ‖ ₂        {PARA[0][0]:.4f}                  {PARA[0][1]:.4f}", ACCENT_B),
                     (f"  ‖ · ‖ ₁        {PARA[1][0]:.4f}                 {PARA[1][1]:.4f}", ACCENT_C),
                     (f"  ‖ · ‖ ∞        {PARA[2][0]:.4f}                  {PARA[2][1]:.4f}", WARN),
                     (f"  ( f , g )      {PARA_F[0]:.4f}                  {PARA_F[1]:.4f}", ACCENT_B),
                     (f"  ‖ Σ x ᵢ s ᵢ ‖ ²  =  {SUM_SQ:.4f}   =   Σ x ᵢ ² ‖ s ᵢ ‖ ²", ACCENT_A)),
                    y0=0.92, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "紅色那支 α − β 從原點畫出，是平移過來的同一個向量",
                  "the red difference is drawn from the origin: the same vector translated",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"這就回答了第一拍那個問題：四種範數裡只有兩範數與函數空間那個純量積兩邊相等——一範數差 {PARA_GAP[1]:.2f}，上界範數差 {PARA_GAP[2]:.2f}",
                          f"that answers the question from the first beat: of the four norms only the two-norm and the function space scalar product balance, the one-norm missing by {PARA_GAP[1]:.2f} and the sup-norm by {PARA_GAP[2]:.2f}",
                          ACCENT_A,
                          f"畢氏定理是同一個展開式：正交的那一對算出 {PYTH[0]:.4f} = {PYTH[1]:.4f}。推論：彼此正交的非零向量必獨立，因為交叉項全消，係數不為零就範數不為零",
                          f"the Pythagorean theorem is the same expansion, {PYTH[0]:.4f} equals {PYTH[1]:.4f} on the orthogonal pair, and the corollary follows: orthogonal nonzero vectors are independent"))

 def stage(self):
  a, b, c = self._opening(), self._define(), self._examples()
  d, e, f_ = self._form(), self._schwarz(), self._second()
  h, i, j = self._norm(), self._hilbert(), self._orthogonal()
  k, l = self._lemma1(), self._lemma2()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE68ZH, AdvCalcE68EN = make(AdvCalcE68Base, "68", prefix="AdvCalcE")
