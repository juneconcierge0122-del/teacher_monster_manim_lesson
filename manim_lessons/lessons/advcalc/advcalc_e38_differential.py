"""advcalc E38 -- chapter 3, section 6 (book pp. 140-144): the tangent line
rewritten as a linear functional once the point of tangency is translated to
the origin, the same move in two variables, the definition of differentiability
(the change is a bounded linear map plus little oh), the uniqueness that comes
straight out of E37's last result, Theorem 6.1 (change in big oh, sums,
products, constants, and linear maps being their own differentials) and
Theorem 6.2, the chain rule.  Book pages 145-146 are exercises 6.1 to 6.18;
E39 opens section 7.

Every remainder on screen is evaluated, not asserted by hand: the tables show
the actual quotient falling, and the chain rule beat multiplies two Jacobians
and then checks the product against the composite's own change, so the picture
cannot claim a rule the arithmetic does not support.  The examples are chosen
here rather than taken from the book's exercises.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
SAMPLE = [10 ** (-k) for k in range(0, 4)]


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


def _ap(m, v):
 return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


def _mul(a, b):
 return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
              for i in range(2))


# ── beats 0 and 1: one variable, f(x) = x squared about a = 1 ──────────
A1, SLOPE = 1.0, 2.0


def _f1(x):
 return x * x


REM1 = [abs((_f1(A1 + t) - _f1(A1)) - SLOPE * t) / abs(t) for t in SAMPLE]
assert all(a > b for a, b in zip(REM1, REM1[1:])), "the remainder quotient should be falling"
assert REM1[-1] < 1e-2, "and it should already be small at the last sample"
for _t, _r in zip(SAMPLE, REM1):
 assert abs(_r - abs(_t)) < 1e-12, "for x squared the quotient is exactly the increment"

# ── beat 2: two variables, f(x, y) = x squared plus x y about (1, 1) ───
def _f2(x, y):
 return x * x + x * y


SKEL = (3.0, 1.0)                                     # the two partial derivatives
REM2 = []
for _t in SAMPLE:
 _xi = (_t, _t / 2)
 _d = _f2(1 + _xi[0], 1 + _xi[1]) - _f2(1.0, 1.0)
 REM2.append(abs(_d - (SKEL[0] * _xi[0] + SKEL[1] * _xi[1])) / _ninf(_xi))
assert all(a > b for a, b in zip(REM2, REM2[1:])) and REM2[-1] < 1e-2, \
    "the two variable remainder should fall to zero as well"
assert abs(_f2(1 + 1e-6, 1) - _f2(1, 1)) / 1e-6 - SKEL[0] < 1e-4, \
    "the first partial derivative on screen is not the one the function has"
assert abs(_f2(1, 1 + 1e-6) - _f2(1, 1)) / 1e-6 - SKEL[1] < 1e-4, \
    "the second partial derivative on screen is not the one the function has"

# ── beat 4: two candidates differ by something Hom and little oh share ─
CAND = ((2.0, 0.0), (2.0, 0.4))                       # two proposed slopes
DIFF = [abs((CAND[1][0] - CAND[0][0]) * t + (CAND[1][1] - CAND[0][1]) * t) / abs(t)
        for t in SAMPLE]
assert all(abs(d - DIFF[0]) < 1e-12 for d in DIFF), \
    "the difference of two linear candidates keeps a constant quotient, which is the point"
assert DIFF[0] > 0, "the two candidates have to actually differ"

# ── beat 8: the product rule on a concrete pair ────────────────────────
PROD_D = 1.0 * 3.0 + 2.0 * 1.0                        # F(a) dG + dF G(a) at a = 1
REM8 = [abs(((1 + t) ** 5 - 1) - PROD_D * t) / abs(t) for t in SAMPLE]
assert abs(PROD_D - 5.0) < 1e-12, "x squared times x cubed should differentiate to five"
assert REM8[-1] < REM8[0] and REM8[-1] < 0.02, "the product remainder should vanish too"

# ── beat 9: the chain rule, two Jacobians against the composite ────────
def _F(v):
 return (v[0] ** 2 + v[1], v[0] * v[1])


def _G(v):
 return (v[0] + v[1] ** 2, v[0] - v[1])


ALPHA = (1.0, 1.0)
BETA = _F(ALPHA)
JF = ((2 * ALPHA[0], 1.0), (ALPHA[1], ALPHA[0]))
JG = ((1.0, 2 * BETA[1]), (1.0, -1.0))
JC = _mul(JG, JF)
assert JC == ((4.0, 3.0), (1.0, 0.0)), "the product of the two Jacobians moved"
REM9 = []
for _t in SAMPLE:
 _xi = (_t, -_t / 2)
 _d = tuple(a - b for a, b in
            zip(_G(_F((ALPHA[0] + _xi[0], ALPHA[1] + _xi[1]))), _G(_F(ALPHA))))
 REM9.append(_ninf(tuple(a - b for a, b in zip(_d, _ap(JC, _xi)))) / _ninf(_xi))
assert all(a > b for a, b in zip(REM9, REM9[1:])) and REM9[-1] < 1e-2, \
    "the composite's remainder should vanish, or the chain rule is not what is drawn"


class AdvCalcE38Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 38

 MODE_LABEL = {
  0: {"zh": "把切點搬到原點", "en": "move the point of tangency to the origin"},
  1: {"zh": "切線是最貼近變化量的直線", "en": "the tangent hugs the change"},
  2: {"zh": "兩個變數：切平面", "en": "two variables: a tangent plane"},
  3: {"zh": "定義：線性部分加一個小 o", "en": "the definition: a linear part plus little oh"},
  4: {"zh": "為什麼只有一種寫法", "en": "why there is only one such T"},
  5: {"zh": "微分是一個映射，不是一個數", "en": "a differential is a map, not a number"},
  6: {"zh": "定理 6.1：三條容易的", "en": "Theorem 6.1: three easy parts"},
  7: {"zh": "加法規則", "en": "the sum rule"},
  8: {"zh": "乘積規則，第二項是並矢", "en": "the product rule, with a dyad"},
  9: {"zh": "定理 6.2：鏈鎖規則", "en": "Theorem 6.2: the chain rule"},
  10: {"zh": "證明就是把上一集用一遍", "en": "the proof is last episode, applied"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 def _cross(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 # ── beats ─────────────────────────────────────────────────────────
 def _tangent(self):
  ox, oy, sx, sy = -5.40, -0.55, 1.05, 0.42
  X = lambda x: ox + x * sx
  Y = lambda y: oy + y * sy
  g = VGroup(Line([X(0), Y(0), 0], [X(2.1), Y(0), 0], color=DIM, stroke_width=1.6),
             Line([X(0), Y(0), 0], [X(0), Y(3.2), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(x / 50), Y(_f1(x / 50)), 0] for x in range(0, 91)], ACCENT_B, sw=3),
        Line([X(0.2), Y(SLOPE * 0.2 - 1), 0], [X(1.8), Y(SLOPE * 1.8 - 1), 0],
             color=ACCENT_C, stroke_width=2.5),
        Dot([X(A1), Y(_f1(A1)), 0], radius=0.06, color=WARN))
  # the same picture again, with the point of tangency at its own origin
  px, py, ps = -1.55, 0.10, 0.62
  g.add(self._cross(px, py, 1.15, 0.95))
  g.add(self._curve([[px + ps * t, py + ps * (SLOPE * t + t * t), 0]
                     for t in (k / 100 - 0.65 for k in range(0, 131))], ACCENT_B, sw=3),
        Line([px - ps * 0.65, py - ps * SLOPE * 0.65, 0],
             [px + ps * 0.65, py + ps * SLOPE * 0.65, 0], color=ACCENT_C, stroke_width=2.5),
        Dot([px, py, 0], radius=0.06, color=WARN))
  g.add(self._panel(((0.86, "左邊是原來的圖，右邊把切點搬到原點",
                      "the left is as drawn; on the right the point sits at the origin", WARN),
                     (0.20, "切線就變成過原點的直線",
                      "the tangent becomes a line through the origin", ACCENT_C),
                     (-0.46, "也就是一個線性泛函的圖形",
                      "which is to say, the graph of a linear functional", ACCENT_B))))
  return g.add(self._foot("這個換座標的動作，是整節唯一的技巧",
                          "that change of coordinates is the only trick in the section",
                          ACCENT_A,
                          "斜率沒變，變的是「切線現在是一個映射」這個看法",
                          "the slope did not move; what moved is seeing the tangent as a map"))

 def _hug(self):
  px, py, ps = -3.90, -0.10, 1.05
  g = VGroup(self._cross(px, py, 1.70, 1.05))
  g.add(self._curve([[px + ps * t, py + ps * (SLOPE * t + t * t) * 0.55, 0]
                     for t in (k / 80 - 0.75 for k in range(0, 121))], ACCENT_B, sw=3),
        Line([px - ps * 0.75, py - ps * SLOPE * 0.75 * 0.55, 0],
             [px + ps * 0.75, py + ps * SLOPE * 0.75 * 0.55, 0],
             color=ACCENT_C, stroke_width=2.5))
  for t in (0.42, 0.66):
   g.add(self._dash([px + ps * t, py + ps * SLOPE * t * 0.55, 0],
                    [px + ps * t, py + ps * (SLOPE * t + t * t) * 0.55, 0], WARN, n=5, sw=2))
  rows = [("      t          | Δf − l | / | t |", DIM)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"{t:8.4f}            {REM1[k]:.5f}",
                (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[k % 4]))
  g.add(self._table(rows))
  return g.add(self._foot("紅色那一段是差，它比 t 更快趨於零，所以落在小 o 裡",
                          "the red gap is the difference; it vanishes faster than t, so it is little oh",
                          ACCENT_A,
                          "數字是算出來的：對 x 平方而言，那個商就正好等於 t",
                          "the numbers are computed: for x squared the quotient is exactly the increment"))

 def _plane(self):
  ox, oy = -4.00, 0.10
  EX, EY, EZ = (0.86, -0.30), (0.72, 0.34), (0.0, 0.78)
  P = lambda x, y, z: [ox + EX[0] * x + EY[0] * y + EZ[0] * z,
                       oy + EX[1] * x + EY[1] * y + EZ[1] * z, 0]
  g = VGroup()
  # The tangent plane is drawn sparsely and the surface densely, so that the
  # two are told apart at a glance; a first draft drew a five by five grid for
  # each and the surface disappeared into it.
  for u in (-1.0, 0.0, 1.0):
   g.add(self._curve([P(u, v / 10.0, 0.16 * (SKEL[0] * u + SKEL[1] * v / 10.0))
                      for v in range(-10, 11)], ACCENT_C, sw=1.8),
         self._curve([P(v / 10.0, u, 0.16 * (SKEL[0] * v / 10.0 + SKEL[1] * u))
                      for v in range(-10, 11)], ACCENT_C, sw=1.8))
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([P(u, v / 10.0, 0.16 * (SKEL[0] * u + SKEL[1] * v / 10.0
                                             + u * u + u * v / 10.0))
                      for v in range(-10, 11)], ACCENT_B, sw=2.4))
  # the gap between the two at two corners, which is the little oh
  for u, v in ((1.0, 1.0), (-1.0, -1.0)):
   lin = 0.16 * (SKEL[0] * u + SKEL[1] * v)
   g.add(self._dash(P(u, v, lin), P(u, v, lin + 0.16 * (u * u + u * v)), WARN, n=4, sw=2))
  g.add(Dot(P(0, 0, 0), radius=0.06, color=WARN))
  g.add(self._panel(((0.86, "紫色是切平面，青色是實際的曲面",
                      "purple is the tangent plane, teal the actual surface", ACCENT_C),
                     (0.20, "線性泛函的骨架就是兩個偏導數",
                      "the skeleton of the linear functional is the two partials", ACCENT_B),
                     (-0.46, f"這個例子是 {SKEL[0]:.0f} 與 {SKEL[1]:.0f}",
                      f"for this example they are {SKEL[0]:.0f} and {SKEL[1]:.0f}", ACCENT_A))))
  return g.add(self._foot("兩個變數只是把「一條直線」換成「一個平面」，說法完全一樣",
                          "two variables only swap a line for a plane; the wording is unchanged",
                          ACCENT_A,
                          "所以定義根本不必提維數，下一拍就直接寫出來",
                          "so the definition need not mention dimension at all, as the next beat shows"))

 def _defn(self):
  g = VGroup()
  boxes = ((-5.05, "ΔF ₐ ( ξ )", ACCENT_B), (-2.85, "T ( ξ )", ACCENT_C), (-0.75, "o ( ξ )", WARN))
  for cx, lab, col in boxes:
   g.add(self._curve([[cx - 0.85, 0.42, 0], [cx + 0.85, 0.42, 0],
                      [cx + 0.85, -0.22, 0], [cx - 0.85, -0.22, 0], [cx - 0.85, 0.42, 0]],
                     col, sw=2),
         self._sym(0.10, lab, col, FS_TAG + 1, x=cx, w=1.60))
  for cx, sign in ((-3.95, "="), (-1.80, "+")):
   g.add(self._sym(0.10, sign, DIM, FS_TAG + 2, x=cx, w=0.50))
  g.add(self._panel(((0.86, "變化量 = 線性部分 + 一個小 o",
                      "the change is a linear part plus a little oh", ACCENT_A),
                     (0.20, "沒有極限、沒有分母",
                      "no limit and no denominator anywhere", ACCENT_C),
                     (-0.46, "也不必假設有限維",
                      "and no assumption of finite dimension", DIM))))
  return g.add(self._foot("T 必須是有界線性映射，這一點是定義的一部分，不是附帶條件",
                          "T is required to be a bounded linear map: part of the definition, not a rider",
                          ACCENT_A,
                          "整個一元微積分的導數，就是這一句在維數等於一時的樣子",
                          "the ordinary derivative is this same sentence with the dimension set to one"))

 def _unique(self):
  ox, oy, sx, sy = -5.20, -0.58, 3.00, 1.30
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.14, oy, 0], [ox + sx + 0.24, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.14, 0], [ox, oy + sy + 0.24, 0], color=DIM, stroke_width=1.6))
  g.add(self._dash([X(0), Y(DIFF[0]), 0], [X(1.0), Y(DIFF[0]), 0], WARN, n=24, sw=2.5),
        self._curve([[X(t / 200), Y(max(t, 1) / 200.0), 0] for t in range(1, 201)],
                    ACCENT_B, sw=3))
  g.add(Text(f"{DIFF[0]:.1f}", font_size=FS_TAG - 4, color=WARN)
        .move_to([ox - 0.30, Y(DIFF[0]), 0]))
  g.add(self._panel(((0.86, "假設有兩個候選的線性部分",
                      "suppose two linear parts were both to work", ACCENT_C),
                     (0.20, "它們的差同時在 Hom 與小 o 裡",
                      "their difference lies in Hom and in little oh at once", WARN),
                     (-0.46, "而那兩個只交於零映射",
                      "and those two meet only at the zero map", ACCENT_A))))
  return g.add(self._foot("紅線就是那個差的比值，它不動，所以不可能是小 o",
                          "the red line is that difference's quotient: it never moves, so it is not little oh",
                          ACCENT_A,
                          "唯一性完全來自上一集最後那一條，不必再證一次",
                          "uniqueness comes entirely from last episode's closing result"))

 def _isamap(self):
  dx, rx, cy, s = -5.05, -2.00, 0.05, 0.40
  g = VGroup(self._cross(dx, cy, 0.90, 0.90), self._cross(rx, cy, 0.90, 0.90),
             Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx, cy + 1.02, 0]),
             Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx, cy + 1.02, 0]))
  for v, col in (((1.0, 0.4), ACCENT_B), ((-0.4, 1.0), ACCENT_C)):
   w = _ap(JF, v)
   g.add(self._arr([dx, cy, 0], [dx + s * v[0], cy + s * v[1], 0], col, sw=2.5, tl=0.12),
         self._arr([rx, cy, 0], [rx + s * 0.42 * w[0], cy + s * 0.42 * w[1], 0],
                   col, sw=2.5, tl=0.12))
  g.add(self._arr([dx + 1.05, cy - 0.62, 0], [rx - 1.05, cy - 0.62, 0], ACCENT_A, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "微分吃一個向量，吐一個向量",
                      "a differential eats a vector and returns a vector", ACCENT_B),
                     (0.20, "維數等於一時它才退化成一個數",
                      "only in dimension one does it collapse to a number", ACCENT_C),
                     (-0.46, "無窮維時習慣叫它第一變分",
                      "in infinite dimensions it is called the first variation", ACCENT_A))))
  return g.add(self._foot("變分法的人比微分學的人更早看到它，只是沒發現是同一件事",
                          "the calculus of variations met it first without realising it was the same object",
                          ACCENT_A,
                          "把它當成映射，後面的規則才寫得出來——尤其是鏈鎖規則",
                          "treating it as a map is what makes the rules expressible, the chain rule above all"))

 def _easy(self):
  g = VGroup()
  rows = ((0.86, "可微  ⇒  ΔF ₐ  ∈  O", ACCENT_B),
          (0.16, "F ≡ c   ⇒   dF ₐ  =  0", ACCENT_C),
          (-0.54, "F ∈ Hom   ⇒   dF ₐ  =  F", WARN))
  for y, lab, col in rows:
   g.add(self._curve([[-6.10, y + 0.30, 0], [-1.05, y + 0.30, 0],
                      [-1.05, y - 0.30, 0], [-6.10, y - 0.30, 0], [-6.10, y + 0.30, 0]],
                     col, sw=1.8),
         self._sym(y, lab, col, FS_TAG + 1, x=-3.58, w=4.60))
  g.add(self._panel(((0.86, "可微一定推得出變化量在大 O 裡",
                      "differentiable forces the change into big oh", ACCENT_B),
                     (0.20, "常數函數的微分是零映射",
                      "a constant function has the zero map as its differential", ACCENT_C),
                     (-0.46, "線性映射的微分就是它自己",
                      "a linear map is its own differential", WARN))))
  return g.add(self._foot("第三條的理由最短：線性映射的變化量本來就等於它自己",
                          "the third is the shortest: a linear map's change already equals the map",
                          ACCENT_A,
                          "所以線性映射處處可微，而且每一點的微分都一樣",
                          "so a linear map is differentiable everywhere with the same differential"))

 def _sum(self):
  g = VGroup()
  lines = (("Δ ( F + G ) ₐ   =   ΔF ₐ  +  ΔG ₐ", ACCENT_B),
           ("=   ( dF ₐ + o )  +  ( dG ₐ + o )", ACCENT_C),
           ("=   ( dF ₐ + dG ₐ )   +   o", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.10))
  g.add(self._panel(((0.86, "把兩個「線性加小 o」相加",
                      "add two copies of linear part plus little oh", ACCENT_C),
                     (0.20, "小 o 對加法封閉，所以還是小 o",
                      "little oh is closed under addition, so it stays little oh", WARN),
                     (-0.46, "而兩個線性部分的和還是線性的",
                      "and the sum of two linear parts is still linear", ACCENT_B))))
  return g.add(self._foot("整個推導不到兩行，靠的全是上一集那條定理的第一項",
                          "the derivation is under two lines and rests entirely on part one of last episode",
                          ACCENT_A,
                          "唯一性再保證這就是和的微分，沒有別的可能",
                          "uniqueness then guarantees this is the differential of the sum"))

 def _product(self):
  ox, oy, sx, sy = -5.30, -0.58, 3.00, 1.20
  TMAX = 0.12                        # past this the quotient leaves the frame
  X = lambda t: ox + (t / TMAX) * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.14, oy, 0], [ox + sx + 0.24, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.14, 0], [ox, oy + 1.55 * sy, 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(TMAX * t / 200.0),
                      Y(abs(((1 + TMAX * t / 200.0) ** 5 - 1) - PROD_D * (TMAX * t / 200.0))
                        / (TMAX * t / 200.0)), 0]
                     for t in range(1, 201)], ACCENT_B, sw=3))
  rows = [("d ( F G ) ₐ  =  F ( α ) dG ₐ  +  dF ₐ G ( α )", ACCENT_A),
          (f"=   1 · 3   +   2 · 1   =   {PROD_D:.0f}", WARN)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"t = {t:7.4f}          {REM8[k]:.5f}",
                (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[k % 4]))
  g.add(self._table(rows, y0=0.88, dy=0.36, size=FS_TAG - 3))
  return g.add(self._foot("第二項是一個並矢：一個線性泛函配上一個固定的向量",
                          "the second term is a dyad: a linear functional paired with a fixed vector",
                          ACCENT_A,
                          "所以乘積規則在向量值的情形也照樣成立，順序不能亂調",
                          "so the product rule survives for vector values, provided the order is kept"))

 def _chain(self):
  g = VGroup()
  for cx, lab, col in ((-5.30, "V", ACCENT_B), (-3.20, "W", ACCENT_C), (-1.10, "X", WARN)):
   g.add(self._cross(cx, 0.62, 0.62, 0.38),
         Dot([cx, 0.62, 0], radius=0.055, color=col),
         Text(lab, font_size=FS_TAG - 2, color=DIM).move_to([cx, 1.16, 0]))
  for cx in (-4.25, -2.15):
   g.add(self._arr([cx - 0.34, 0.62, 0], [cx + 0.34, 0.62, 0], ACCENT_A, sw=2.5, tl=0.12))
  gr, _ = self._numgrid(-5.30, -0.44, [[f"{x:.0f}" for x in r] for r in JF], color=ACCENT_B)
  gg, _ = self._numgrid(-3.20, -0.44, [[f"{x:.0f}" for x in r] for r in JG], color=ACCENT_C)
  gc, _ = self._numgrid(-1.10, -0.44, [[f"{x:.0f}" for x in r] for r in JC], color=WARN)
  g.add(gr, gg, gc)
  g.add(self._sym(-1.00, "dG ᵦ  ∘  dF ₐ", DIM, FS_TAG - 2, x=-1.10, w=2.20))
  rows = [("       t         | rem | / ‖ ξ ‖", DIM)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"{t:8.4f}            {REM9[k]:.5f}",
                (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[k % 4]))
  g.add(self._table(rows, y0=0.72, dy=0.40))
  return g.add(self._foot("兩個雅可比矩陣乘出來的，跟直接算合成的變化量完全一致",
                          "the product of the two Jacobians agrees with the composite's own change",
                          ACCENT_A,
                          "這一拍的數字是程式算的，右邊那一列就是餘項的商",
                          "the numbers were computed here, and the right column is the remainder's quotient"))

 def _proof(self):
  g = VGroup()
  lines = (("Δ ( G ∘ F ) ₐ   =   ΔG ᵦ ( ΔF ₐ )", ACCENT_B),
           ("=   dG ᵦ ( dF ₐ + o )   +   o ( O )", ACCENT_C),
           ("=   dG ᵦ ∘ dF ₐ   +   o", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.82 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.10))
  g.add(self._panel(((0.86, "小 o 接大 O 還是小 o",
                      "little oh after big oh is little oh", ACCENT_C),
                     (0.20, "大 O 接小 o 也是小 o",
                      "big oh after little oh is little oh as well", WARN),
                     (-0.46, "剩下的就只有兩個線性部分的合成",
                      "what survives is the composite of the two linear parts", ACCENT_B))))
  return g.add(self._foot("上一集那條定理的每一項，在這裡剛好都用上一次",
                          "every part of last episode's theorem gets used exactly once here",
                          ACCENT_A,
                          "第 3 章的核心到此結束，下一集講方向導數與均值定理",
                          "that is the core of chapter three; next time, directional derivatives"))

 def stage(self):
  a, b, c = self._tangent(), self._hug(), self._plane()
  d, e, f = self._defn(), self._unique(), self._isamap()
  h, i, j = self._easy(), self._sum(), self._product()
  k, l = self._chain(), self._proof()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE38ZH, AdvCalcE38EN = make(AdvCalcE38Base, "38", prefix="AdvCalcE")
