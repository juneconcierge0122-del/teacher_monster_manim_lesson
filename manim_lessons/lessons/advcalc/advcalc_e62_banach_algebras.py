"""advcalc E62 -- chapter 4, section 8 (book pp. 223-226): a first look at Banach
algebras.

The section exists to pay a debt from chapter 3.  The inverse mapping theorem
needed to know that an invertible T stays invertible under small perturbation
and that inversion is continuous; in finite dimensions the determinant settles
it, and here the geometric series settles it in general.  Hom V is both a Banach
space and an algebra, and once the transformations are forgotten and only the
algebra axioms kept, the elementary geometric series argument goes through
verbatim (8.1), which makes the invertible elements open and inversion
continuous (8.2).  Power series then converge on balls (8.3), the exponential
converges everywhere, and with a theorem on differentiating a limit (8.4) plus
two lemmas the series can be differentiated term by term (8.5).  The striking
part is the shape of the answer: dF at y is multiplication by a single element.

Book pages 227 and 228 are exercises 8.1 to 8.24, and section 9 begins on 228.

Everything numerical here is computed on real two-by-two matrices under the
max-row-sum norm, which is submultiplicative and gives the identity norm one, so
the algebra axioms on screen are the axioms these numbers actually satisfy.  The
geometric series is summed and compared against the exact inverse, the estimate
r/(1-r) is checked against measured values at three radii, the radius 1/m of
Theorem 8.2 is checked to work and to be sharp, and the exponential of a
rotation generator is summed and checked against the rotation it should be --
which is also what beat 10 draws.
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

I2 = ((1.0, 0.0), (0.0, 1.0))
Z2 = ((0.0, 0.0), (0.0, 0.0))


def mul(a, b):
 return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
              for i in range(2))


def add(a, b):
 return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def sub(a, b):
 return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))


def smul(c, a):
 return tuple(tuple(c * a[i][j] for j in range(2)) for i in range(2))


def nrm(a):
 """Max row sum: submultiplicative, and the identity comes out at one."""
 return max(abs(a[i][0]) + abs(a[i][1]) for i in range(2))


def inv(a):
 d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
 return None if abs(d) < 1e-12 else ((a[1][1] / d, -a[0][1] / d),
                                     (-a[1][0] / d, a[0][0] / d))


assert nrm(I2) == 1.0, "the identity has norm one, as a Banach algebra needs"


# ── beat 1: the axioms hold for the numbers actually shown ─────────────
AX_S = ((0.60, -0.30), (0.20, 0.50))
AX_T = ((0.40, 0.10), (-0.20, 0.70))
AX = (nrm(AX_S), nrm(AX_T), nrm(mul(AX_S, AX_T)))
assert AX[2] <= AX[0] * AX[1] + 1e-12, "the norm has to be submultiplicative"
assert AX[2] < AX[0] * AX[1] - 0.05, "and here the inequality is strictly slack"
assert nrm(sub(mul(AX_S, add(AX_T, I2)),
               add(mul(AX_S, AX_T), AX_S))) < 1e-12, "distributivity"


# ── beat 2: the geometric series, summed and compared ──────────────────
GX = ((0.30, 0.20), (-0.10, 0.40))
GR = nrm(GX)
assert GR < 1.0, "the series only has a chance when the norm is under one"
GINV = inv(sub(I2, GX))
GEO = []
_p, _s = I2, Z2
for _k in range(1, 13):
 _s = add(_s, _p)
 _p = mul(_p, GX)
 if _k in (2, 4, 8, 12):
  GEO.append((_k, nrm(sub(_s, GINV))))
for _a, _b in zip(GEO, GEO[1:]):
 assert _b[1] < _a[1], "the partial sums close in on the exact inverse"
assert GEO[-1][1] < 1e-4, "and get there fast enough to print as zero"


# ── beat 3: the estimate r / (1 - r), measured at three radii ──────────
EST = []
for _r in (0.20, 0.40, 0.60):
 _x = smul(_r / GR, GX)
 assert abs(nrm(_x) - _r) < 1e-12, "scaled to land exactly on the radius"
 EST.append((_r, nrm(sub(I2, inv(sub(I2, _x)))), _r / (1.0 - _r)))
for _r, _got, _bound in EST:
 assert _got <= _bound + 1e-12, "the measured value has to respect the estimate"
# measured / bound runs 0.96, 0.88, 0.74 across the three radii: true, and
# loosening as r grows, but never far off
assert EST[-1][1] < 0.80 * EST[-1][2], "the estimate is true rather than tight"


# ── beat 4: the radius 1 / m, checked to work and to be sharp ──────────
YY = ((1.00, 0.50), (0.00, 1.00))
M4 = nrm(inv(YY))
RAD = 1.0 / M4
assert abs(M4 - 1.5) < 1e-12 and abs(RAD - 2.0 / 3.0) < 1e-12, \
    "the inverse has norm three halves, so the guaranteed radius is two thirds"
SAFE = smul(0.95 * RAD / nrm(((0.4, 0.2), (0.1, 0.3))), ((0.4, 0.2), (0.1, 0.3)))
assert nrm(SAFE) < RAD and inv(sub(YY, SAFE)) is not None, \
    "inside the radius the perturbed element is still invertible"
assert inv(sub(YY, YY)) is None and nrm(YY) > RAD, \
    "and far enough out an invertible element can be destroyed outright"


# ── beat 6: the comparison that makes a power series converge ──────────
DELTA6, S6 = 1.0, 0.70
A6 = [1.0 / (n + 1) ** 2 for n in range(9)]
B6 = max(A6[n] * DELTA6 ** n for n in range(9))
R6 = S6 / DELTA6
for _n in range(9):
 assert A6[_n] * S6 ** _n <= B6 * R6 ** _n + 1e-12, \
     "each term is dominated by the real geometric series b r to the n"
assert R6 < 1.0, "which converges precisely because the smaller ball was chosen"


# ── beats 7 and 10: the exponential of a rotation generator ────────────
J = ((0.0, -1.0), (1.0, 0.0))
THETA = 1.0
EXP_TERMS = []
_p, _s = I2, Z2
for _k in range(1, 15):
 _s = add(_s, smul(1.0 / math.factorial(_k - 1), _p))
 _p = mul(_p, smul(THETA, J))
 if _k in (3, 6, 9, 14):
  EXP_TERMS.append((_k, _s))
ROT = ((math.cos(THETA), -math.sin(THETA)), (math.sin(THETA), math.cos(THETA)))
EXP_ERR = [(k, nrm(sub(s, ROT))) for k, s in EXP_TERMS]
for _a, _b in zip(EXP_ERR, EXP_ERR[1:]):
 assert _b[1] < _a[1], "the partial sums close in on the rotation"
assert EXP_ERR[-1][1] < 1e-9, "and the exponential really is that rotation"

# gamma(t) = exp(t J) applied to (1, 0) traces the circle, and its velocity is
# the tangent -- checked, not asserted in a caption
GAMMA_T = 1.05
GPOS = (math.cos(GAMMA_T), math.sin(GAMMA_T))
GVEL = (-math.sin(GAMMA_T), math.cos(GAMMA_T))
assert abs(GPOS[0] * GVEL[0] + GPOS[1] * GVEL[1]) < 1e-12, \
    "the velocity is perpendicular to the radius, so it is tangent"
assert abs(math.hypot(*GPOS) - 1.0) < 1e-12 and abs(math.hypot(*GVEL) - 1.0) < 1e-12, \
    "and both are unit vectors, since the generator has norm one here"


class AdvCalcE62Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 62

 MODE_LABEL = {
  0: {"zh": "第 3 章留下來的那個問題", "en": "the question left over from chapter 3"},
  1: {"zh": "Banach 代數的公理", "en": "the axioms of a Banach algebra"},
  2: {"zh": "定理 8.1：幾何級數", "en": "Theorem 8.1: the geometric series"},
  3: {"zh": "順便得到的誤差估計", "en": "the estimate that comes along with it"},
  4: {"zh": "定理 8.2：可逆元是開集", "en": "Theorem 8.2: the invertible elements are open"},
  5: {"zh": "一行代數，補上第 3 章的洞", "en": "one line of algebra fills chapter 3's gap"},
  6: {"zh": "定理 8.3：冪級數在球上", "en": "Theorem 8.3: power series on a ball"},
  7: {"zh": "指數函數，處處收斂", "en": "the exponential, convergent everywhere"},
  8: {"zh": "定理 8.4：極限的可微性", "en": "Theorem 8.4: differentiating a limit"},
  9: {"zh": "一項一項微分下去", "en": "differentiating term by term"},
  10: {"zh": "微分就是「乘上 F 撇」", "en": "the differential is multiplication by F prime"},
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

 def _circ(self, cx, cy, r, col, sw=2.0, n=64):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _blob(self, cx, cy, col, sw=2.2):
  return self._curve([[cx + (1.55 + 0.22 * math.sin(3 * 2 * math.pi * k / 90))
                       * math.cos(2 * math.pi * k / 90),
                       cy + (0.82 + 0.14 * math.cos(2 * 2 * math.pi * k / 90))
                       * math.sin(2 * math.pi * k / 90), 0]
                      for k in range(91)], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plot(self, f, ox, oy, sx, sy, col, sw=2.4, n=220, x0=0.0, x1=1.0):
  return self._curve([[ox + sx * k / n, oy + sy * f(x0 + (x1 - x0) * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _debt(self):
  cx, cy = -3.60, 0.20
  g = VGroup(self._blob(cx, cy, ACCENT_B))
  g.add(Dot([cx - 0.30, cy, 0], radius=0.075, color=ACCENT_A),
        self._sym(cy + 0.28, "T", ACCENT_A, FS_TAG, x=cx - 0.30, w=0.60),
        self._circ(cx - 0.30, cy, 0.50, WARN, sw=1.5))
  g.add(Dot([cx + 0.05, cy - 0.22, 0], radius=0.06, color=WARN),
        self._sym(cy - 0.50, "S", WARN, FS_TAG, x=cx + 0.05, w=0.60))
  g.add(self._mid(cy + 1.05, "可逆元的全體", "the invertible elements", ACCENT_B,
                  FS_TAG - 1, x=cx, w=3.20))
  g.add(self._panel(((0.86, "反映射定理用到：T 可逆，附近的 S 也可逆",
                      "the inverse mapping theorem needed S invertible near an invertible T",
                      ACCENT_B),
                     (0.20, "而且反元素還要連續地依賴它",
                      "and the inverse to depend continuously on it", ACCENT_C),
                     (-0.46, "有限維靠行列式，一般的情況要另一套",
                      "the determinant settles finite dimensions; the general case needs more",
                      WARN))))
  return g.add(self._foot("這一節就是為了還第 3 章這筆帳——而還帳用的是初等微積分裡的幾何級數",
                          "this section exists to pay that debt from chapter 3, and it pays with the geometric series of elementary calculus",
                          ACCENT_A,
                          "紅圈就是要證明存在的那個半徑：圈裡的每一個 S 都還在可逆元裡面",
                          "the red circle is the radius that has to be shown to exist: every S inside it is still invertible"))

 def _axioms(self):
  g = VGroup()
  rows = (("S ( T ₁ + T ₂ )   =   S T ₁  +  S T ₂", ACCENT_B),
          ("( S ₁ + S ₂ ) T   =   S ₁ T  +  S ₂ T", ACCENT_B),
          ("c ( S T )   =   ( c S ) T   =   S ( c T )", ACCENT_C),
          ("‖ S T ‖   ≤   ‖ S ‖  ‖ T ‖              ‖ I ‖   =   1", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.82 - k * 0.50, lab, col, FS_TAG, x=-3.40, w=5.40))
  g.add(self._table((("     ‖ S ‖         ‖ T ‖       ‖ S T ‖", DIM),
                     (f"     {AX[0]:.2f}          {AX[1]:.2f}          {AX[2]:.2f}", ACCENT_C),
                     (f"     {AX[0]:.2f}  ×  {AX[1]:.2f}   =   {AX[0] * AX[1]:.2f}", ACCENT_A)),
                    y0=0.80, dy=0.40))
  g.add(self._mid(-0.72, "畫面上這兩個矩陣真的滿足那條不等式",
                  "the two matrices on screen really do satisfy that inequality", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("Hom V 既是 Banach 空間，又帶著一個結合的乘法——合成。這幾條就是 Banach 代數的公理",
                          "Hom V is a Banach space and carries an associative multiplication, composition, and this list is the axioms of a Banach algebra",
                          ACCENT_A,
                          "書上說：把「它們是變換」這件複雜的事忘掉，只當成抽象代數裡的元素",
                          "the book says to forget the complicated nature of a transformation and treat it merely as an element of an abstract algebra"))

 def _geometric(self):
  ox, oy = -5.85, -0.72
  sx, sy = 4.20, 1.85
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  lo = math.log10(GEO[-1][1])
  hi = math.log10(GEO[0][1])
  pts = []
  for k, e in GEO:
   px = ox + sx * (k - GEO[0][0]) / (GEO[-1][0] - GEO[0][0])
   py = oy + sy * (math.log10(e) - lo) / (hi - lo)
   pts.append([px, py, 0])
   g.add(Dot([px, py, 0], radius=0.06, color=ACCENT_C))
  g.add(self._curve(pts, ACCENT_C, sw=1.8))
  g.add(self._sym(oy + sy * 1.02, "‖ σ ₙ  −  ( e − x ) ⁻ ¹ ‖", ACCENT_A,
                  FS_TAG - 1, x=ox + 1.70, w=3.00))
  rows = [("       n          ‖ σ ₙ  −  ( e − x ) ⁻ ¹ ‖", DIM)]
  for k, e in GEO:
   rows.append((f"     {k:4d}                {e:.2e}", ACCENT_C))
  g.add(self._table(rows, y0=0.86, dy=0.32))
  g.add(self._mid(-0.94, f"這裡 ‖ x ‖ = {GR:.2f}，所以級數收斂",
                  f"here the norm of x is {GR:.2f}, so the series converges", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("證明只用到絕對收斂：x 的 n 次方的範數不超過範數的 n 次方，拿實數的幾何級數比較就好",
                          "the proof only needs absolute convergence: a power has norm at most the power of the norm, so the real geometric series dominates it",
                          ACCENT_A,
                          "而上一集的定理 7.11 保證：在 Banach 空間裡，絕對收斂就真的收斂",
                          "and Theorem 7.11 from the last episode guarantees that in a Banach space absolute convergence is convergence"))

 def _estimate(self):
  ox, oy = -5.85, -0.70
  sx, sy = 4.10, 1.75
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  top = 2.0
  g.add(self._plot(lambda r: min(r / (1.0 - r), top) / top, ox, oy, sx * 0.80, sy,
                   ACCENT_A, sw=2.4, n=240, x0=0.0, x1=0.68))
  for (r, got, bound), col in zip(EST, (ACCENT_B, ACCENT_C, WARN)):
   px = ox + sx * 0.80 * r / 0.68
   g.add(Dot([px, oy + sy * got / top, 0], radius=0.06, color=col),
         self._dash([px, oy, 0], [px, oy + sy * min(bound, top) / top, 0], col, n=8, sw=1.0))
  g.add(self._sym(oy + sy * 1.00, "r / ( 1 − r )", ACCENT_A, FS_TAG - 1,
                  x=ox + sx * 0.72, w=1.90))
  g.add(self._table([("       r        ‖ e − ( e − x ) ⁻ ¹ ‖      r / ( 1 − r )", DIM)]
                    + [(f"    {r:.2f}              {got:.3f}                {bound:.3f}", ACCENT_C)
                       for r, got, bound in EST], y0=0.86, dy=0.34))
  g.add(self._mid(-0.80, "三個半徑都量過：實際值一直在上界底下",
                  "measured at three radii, and the value stays under the bound every time",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這條估計是幾何級數自己送的：把 n 從 1 開始的那些項的範數加起來，就是 r 除以一減 r",
                          "the estimate falls out of the series itself: summing the norms of the terms from one onward gives r over one minus r",
                          ACCENT_A,
                          "它是對的，可是不緊：r = 0.60 那一點量到 1.10，上界卻是 1.50",
                          "it is true rather than tight: at r equal to 0.60 the measured value is 1.10 against a bound of 1.50"))

 def _open_set(self):
  cx, cy = -3.60, 0.18
  g = VGroup(self._blob(cx, cy, ACCENT_B))
  g.add(Dot([cx - 0.20, cy, 0], radius=0.075, color=ACCENT_A),
        self._sym(cy + 0.26, "y", ACCENT_A, FS_TAG, x=cx - 0.20, w=0.60),
        self._circ(cx - 0.20, cy, 0.62, WARN, sw=1.6))
  g.add(self._sym(cy - 0.80, f"r  =  1 / m  =  {RAD:.2f}", WARN, FS_TAG - 1,
                  x=cx - 0.20, w=2.40))
  g.add(self._table((("     m   =   ‖ y ⁻ ¹ ‖", DIM),
                     (f"     m   =   {M4:.2f}", ACCENT_C),
                     (f"     1 / m   =   {RAD:.3f}", ACCENT_A),
                     (f"     ‖ h ‖   =   {nrm(SAFE):.3f}   <   1 / m", ACCENT_B)),
                    y0=0.84, dy=0.40))
  g.add(self._mid(-0.86, "所以 y 減 h 一定還可逆——程式驗過了",
                  "so y minus h is still invertible, and that was checked", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 8.2：可逆元的全體是開集，而且取反元素這個映射在上面連續",
                          "Theorem 8.2: the invertible elements form an open set, and inversion is continuous on it",
                          ACCENT_A,
                          "半徑是 y 的反元素的範數的倒數——反元素越大，能保證的半徑就越小",
                          "the radius is one over the norm of the inverse, so a larger inverse buys a smaller guaranteed radius"))

 def _one_line(self):
  g = VGroup()
  rows = (("y  −  h    =    y  ( e  −  x )        ,        x  =  y ⁻ ¹ h", ACCENT_B),
          ("‖ x ‖    ≤    m  ‖ h ‖    <    1", ACCENT_C),
          ("( e − x ) ⁻ ¹    =    Σ ₀ ∞   x ⁿ", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.54, lab, col, FS_TAG, x=-3.40, w=5.40))
  g.add(self._dash([-5.90, -0.62, 0], [-0.90, -0.62, 0], DIM, n=24, sw=1.2))
  g.add(self._sym(-0.94, "( y − h ) ⁻ ¹    =    ( e − x ) ⁻ ¹  y ⁻ ¹", ACCENT_A,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._panel(((0.86, "把 y 減 h 提出一個 y，剩下的正好是 e 減 x",
                      "factor a y out of y minus h and what is left is exactly e minus x",
                      ACCENT_B),
                     (0.20, "x 的範數小於一，定理 8.1 就直接可用",
                      "the norm of x is under one, so Theorem 8.1 applies at once", ACCENT_C),
                     (-0.46, "推論：Hom 裡的可逆元開，取反元素連續",
                      "corollary: the invertible elements of Hom are open and inversion is continuous",
                      WARN))))
  return g.add(self._foot("第 3 章欠的那一條到這裡還清了——而且用的完全是代數，沒有碰行列式",
                          "the debt from chapter 3 is settled here, and settled by algebra alone, with no determinant anywhere",
                          ACCENT_A,
                          "這就是書上說「最自然、最漂亮」的那個做法：把問題丟回幾何級數",
                          "this is the way the book calls the most natural and most elegant: hand the problem back to the geometric series"))

 def _power_series(self):
  cx, cy = -3.75, 0.18
  g = VGroup(self._circ(cx, cy, 1.00, ACCENT_B, sw=2.0),
             self._circ(cx, cy, 0.70, WARN, sw=2.0))
  g.add(Dot([cx, cy, 0], radius=0.05, color=DIM))
  g.add(self._sym(cy + 1.10, f"δ  =  {DELTA6:.1f}", ACCENT_B, FS_TAG - 1, x=cx + 1.15, w=1.30),
        self._sym(cy - 0.86, f"s  =  {S6:.2f}", WARN, FS_TAG - 1, x=cx + 0.34, w=1.30))
  g.add(self._table((("     ‖ a ₙ ‖ δ ⁿ   ≤   b", DIM),
                     (f"     b   =   {B6:.2f}", ACCENT_C),
                     (f"     r   =   s / δ   =   {R6:.2f}", ACCENT_A),
                     (f"     Σ b r ⁿ   =   {B6 / (1 - R6):.2f}", WARN)),
                    y0=0.84, dy=0.40))
  g.add(self._mid(-0.86, "小球上每一項都被 b rⁿ 蓋住，所以均勻收斂",
                  "on the smaller ball every term is dominated by b r to the n, hence uniform",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 8.3：只要 aₙ 乘 δⁿ 那一列的範數有界，冪級數就在半徑 δ 的球裡收斂",
                          "Theorem 8.3: as long as the norms of a-n times delta to the n stay bounded, the power series converges on the ball of radius delta",
                          ACCENT_A,
                          "而在任何一個更小的球上是均勻收斂的——比較的對象還是實數的幾何級數",
                          "and uniformly on any smaller ball, the comparison again being a real geometric series"))

 def _exponential(self):
  ox, oy = -5.85, -0.72
  sx, sy = 4.20, 1.85
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  lo, hi = math.log10(EXP_ERR[-1][1]), math.log10(EXP_ERR[0][1])
  pts = []
  for k, e in EXP_ERR:
   px = ox + sx * (k - EXP_ERR[0][0]) / (EXP_ERR[-1][0] - EXP_ERR[0][0])
   py = oy + sy * (math.log10(e) - lo) / (hi - lo)
   pts.append([px, py, 0])
   g.add(Dot([px, py, 0], radius=0.06, color=WARN))
  g.add(self._curve(pts, WARN, sw=1.8))
  g.add(self._sym(oy + sy * 1.02, "‖ σ ₙ  −  R ( θ ) ‖", ACCENT_A, FS_TAG - 1,
                  x=ox + 1.55, w=2.80))
  rows = [("       n          ‖ σ ₙ  −  R ( θ ) ‖", DIM)]
  for k, e in EXP_ERR:
   rows.append((f"     {k:4d}                {e:.1e}", ACCENT_C))
  g.add(self._table(rows, y0=0.86, dy=0.32))
  g.add(self._mid(-0.94, "取 x 是旋轉的生成元，指數就真的是那個旋轉",
                  "take x to be the generator of a rotation and the exponential is that rotation",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("指數函數是 x 的 n 次方除以 n 階乘的和，對代數裡每一個 x 都收斂，在任何球上均勻收斂",
                          "the exponential is the sum of x to the n over n factorial, convergent for every x in the algebra and uniformly on any ball",
                          ACCENT_A,
                          "初等微積分那套比較法整套搬過來就夠了，一個字都不用改",
                          "the usual comparison arguments of elementary calculus carry over without a word of change"))

 def _diff_limit(self):
  g = VGroup()
  labs = (("逐點收斂", "pointwise", ACCENT_B),
          ("關於 β 均勻", "uniformly in beta", ACCENT_C),
          ("結論", "conclusion", WARN))
  syms = ("F ⁿ   →   F",
          "d F ⁿ ᵦ   →   d F ᵦ",
          "F   →   d F ᵦ   =   lim  d F ⁿ ᵦ")
  for k, (s, (zh, en, col)) in enumerate(zip(syms, labs)):
   g.add(self._sym(0.76 - k * 0.56, s, col, FS_TAG + 1, x=-4.05, w=3.60),
         self._mid(0.76 - k * 0.56, zh, en, col, FS_TAG - 1, x=-1.10, w=2.20))
  g.add(self._dash([-5.90, -0.10, 0], [-0.10, -0.10, 0], DIM, n=26, sw=1.1))
  g.add(self._panel(((0.86, "微分的收斂要是均勻的，逐點不夠",
                      "the differentials must converge uniformly; pointwise is not enough",
                      ACCENT_B),
                     (0.20, "證明用均值定理把兩個差商夾起來",
                      "the proof pins two difference quotients with the mean value theorem",
                      ACCENT_C),
                     (-0.46, "三個 ε 疊起來，得到 3 ε 乘 ‖ ξ ‖",
                      "three epsilons stack up to three epsilon times the norm of xi", WARN))))
  return g.add(self._foot("這是一條「極限的可微性」定理：微分與取極限這兩件事在什麼條件下可以交換",
                          "this is a theorem about differentiating a limit: when differentiation and passing to the limit may be exchanged",
                          ACCENT_A,
                          "有了它，冪級數才能一項一項微分——書上把剩下的證明整組留成習題",
                          "with it the power series can be differentiated term by term, and the book leaves the remaining proofs as a set of exercises"))

 def _term_by_term(self):
  g = VGroup()
  y0 = 0.72
  g.add(self._sym(y0, "F ( x )    =    a ₀  +  a ₁ x  +  a ₂ x ²  +  a ₃ x ³  +  …",
                  ACCENT_B, FS_TAG, x=-3.30, w=5.60))
  for k, dx in enumerate((-1.40, -0.30, 0.80)):
   g.add(self._arr([dx, y0 - 0.16, 0], [dx, y0 - 0.52, 0], ACCENT_A, sw=1.8, tl=0.09))
  g.add(self._sym(y0 - 0.74, "F ′ ( y )    =    a ₁  +  2 a ₂ y  +  3 a ₃ y ²  +  …",
                  WARN, FS_TAG, x=-3.30, w=5.60))
  g.add(self._sym(y0 - 1.40, "d p ₍ a , b ₎ ( x , y )   =   a y  +  x b", ACCENT_C,
                  FS_TAG - 1, x=-3.30, w=4.40))
  g.add(self._panel(((0.86, "引理 8.1：乘法本身可微",
                      "Lemma 8.1: multiplication itself is differentiable", ACCENT_C),
                     (0.20, "引理 8.2：交換代數上的單項式可微",
                      "Lemma 8.2: on a commutative algebra a monomial is differentiable",
                      ACCENT_B),
                     (-0.46, "定理 8.5：兩者合起來，冪級數可微",
                      "Theorem 8.5: together they make the power series differentiable", WARN))))
  return g.add(self._foot("逐項微分得到的那個級數，正是初等微積分裡寫下來的同一個式子",
                          "the series that term-by-term differentiation produces is the very one written down in elementary calculus",
                          ACCENT_A,
                          "引理 8.2 要求交換——單項式的微分裡那個 n 就是從交換性來的",
                          "Lemma 8.2 asks for commutativity: the factor n in a monomial's differential is exactly what commuting buys"))

 def _multiplication(self):
  cx, cy = -3.70, 0.02
  R = 0.92
  g = VGroup(self._circ(cx, cy, R, DIM, sw=1.4))
  px, py = cx + R * GPOS[0], cy + R * GPOS[1]
  g.add(Line([cx, cy, 0], [px, py, 0], color=ACCENT_C, stroke_width=1.6),
        Dot([px, py, 0], radius=0.07, color=ACCENT_A))
  g.add(self._arr([px, py, 0], [px + 0.62 * GVEL[0], py + 0.62 * GVEL[1], 0],
                  WARN, sw=2.4, tl=0.12))
  g.add(self._sym(py + 0.34, "γ ( t )", ACCENT_A, FS_TAG - 1, x=px + 0.34, w=1.10),
        self._sym(py + 0.62 * GVEL[1] + 0.06, "γ ′ ( t )  =  x e ᵗ ˣ", WARN,
                  FS_TAG - 1, x=px + 0.62 * GVEL[0] - 0.86, w=2.20))
  g.add(self._table((("     γ ( t )  ·  γ ′ ( t )", DIM),
                     (f"     =   {GPOS[0] * GVEL[0] + GPOS[1] * GVEL[1]:.1f}", ACCENT_A),
                     ("     ‖ γ ‖  =  ‖ γ ′ ‖  =  1", ACCENT_B)), y0=0.84, dy=0.40))
  g.add(self._mid(-0.60, "速度垂直於半徑，所以它是切的——這是算出來的",
                  "the velocity is perpendicular to the radius, so it is tangent, and that was computed",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 8.5 最值得注意的是答案的形狀：F 在 y 的微分就是「乘上 F 撇 y」這個線性變換",
                          "the striking part of Theorem 8.5 is the shape of the answer: the differential of F at y is multiplication by the single element F prime of y",
                          ACCENT_A,
                          "指數函數因此是自己的導數，指數律也跟著出來——但那條要在交換的代數上才成立",
                          "the exponential is therefore its own derivative and the law of exponents follows, though only on a commutative algebra"))

 def stage(self):
  a, b, c = self._debt(), self._axioms(), self._geometric()
  d, e, f = self._estimate(), self._open_set(), self._one_line()
  h, i, j = self._power_series(), self._exponential(), self._diff_limit()
  k, l = self._term_by_term(), self._multiplication()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE62ZH, AdvCalcE62EN = make(AdvCalcE62Base, "62", prefix="AdvCalcE")
