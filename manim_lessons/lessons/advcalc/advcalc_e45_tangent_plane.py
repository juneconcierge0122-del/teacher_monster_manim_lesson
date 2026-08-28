"""advcalc E45 -- chapter 3, section 10, second part (book pp. 162-163): a map
seen as a surface in the product space, the two projections, the tangent plane
as the graph of the differential translated to the point of contact, its
uniqueness as the only affine map approximating to within little oh, and
Theorem 10.2, which says that plane is exactly the union of the tangent lines
to smooth curves lying in the surface.  Pages 163-164 are exercises 10.1 to
10.13; E46 opens section 11.

The worked example is chosen here rather than taken from the book.  Its
Jacobian is computed by central differences and checked against the formula,
the two scalar equations of the tangent plane are evaluated at a test point and
checked, the remainder between the map and its tangent affine map is measured
and asserted to vanish, and a genuinely curved arc on the surface has its
tangent vector in four dimensions checked against the pairing that Theorem 10.2
predicts.
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
H = 1e-6


def _F(x):
 return (x[0] * x[1], x[0] ** 2 - x[1])


APT = (2.0, 1.0)
FA = _F(APT)
JAC = ((APT[1], APT[0]), (2 * APT[0], -1.0))
_num = tuple(tuple((_F((APT[0] + H * (j == 0), APT[1] + H * (j == 1)))[i]
                    - _F((APT[0] - H * (j == 0), APT[1] - H * (j == 1)))[i]) / (2 * H)
                   for j in range(2)) for i in range(2))
assert max(abs(a - b) for r, q in zip(_num, JAC) for a, b in zip(r, q)) < 1e-4, \
    "the Jacobian written down is not the one the difference quotients give"
assert FA == (2.0, 3.0) and JAC == ((1.0, 2.0), (4.0, -1.0)), \
    "the numbers the beats print have moved"


def _G(x):
 """The tangent affine map: the differential translated to the contact point."""
 return (JAC[0][0] * (x[0] - APT[0]) + JAC[0][1] * (x[1] - APT[1]) + FA[0],
         JAC[1][0] * (x[0] - APT[0]) + JAC[1][1] * (x[1] - APT[1]) + FA[1])


# the two scalar equations the beats print, checked away from the contact point
for _p in ((5.0, 7.0), (-1.0, 0.5), (0.0, 0.0)):
 assert abs(_G(_p)[0] - (_p[0] + 2 * _p[1] - 2)) < 1e-9, "the first equation is wrong"
 assert abs(_G(_p)[1] - (4 * _p[0] - _p[1] - 4)) < 1e-9, "the second equation is wrong"


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


SAMPLE = (1e-1, 1e-2, 1e-3)
REM = []
for _t in SAMPLE:
 _xi = (_t, -_t / 2)
 _x = (APT[0] + _xi[0], APT[1] + _xi[1])
 REM.append(_ninf(tuple(a - b for a, b in zip(_F(_x), _G(_x)))) / _ninf(_xi))
assert all(a > b for a, b in zip(REM, REM[1:])) and REM[-1] < 1e-2, \
    "the tangent plane does not approximate to within little oh"


# ── beats 6 and 7: Theorem 10.2, on a genuinely curved arc ─────────────
def _lam(t):
 return (APT[0] + t, APT[1] + t * t)


def _lift(t):
 return (_lam(t)[0], _lam(t)[1], _F(_lam(t))[0], _F(_lam(t))[1])


CURVE_TAN = tuple((a - b) / (2 * H) for a, b in zip(_lift(H), _lift(-H)))
LAM_TAN = tuple((a - b) / (2 * H) for a, b in zip(_lam(H), _lam(-H)))
PRED = (LAM_TAN[0], LAM_TAN[1],
        JAC[0][0] * LAM_TAN[0] + JAC[0][1] * LAM_TAN[1],
        JAC[1][0] * LAM_TAN[0] + JAC[1][1] * LAM_TAN[1])
assert max(abs(a - b) for a, b in zip(CURVE_TAN, PRED)) < 1e-4, \
    "Theorem 10.2 fails on the drawn arc"
assert all(abs(v - round(v)) < 1e-4 for v in PRED), "the beat prints these"
PRED = tuple(round(v) for v in PRED)


class AdvCalcE45Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 45

 MODE_LABEL = {
  0: {"zh": "把映射看成一張曲面", "en": "a map seen as a surface"},
  1: {"zh": "兩個投影", "en": "the two projections"},
  2: {"zh": "切平面：微分的圖形，平移過去", "en": "the tangent plane: the differential, translated"},
  3: {"zh": "切平面的方程式", "en": "the equation of the tangent plane"},
  4: {"zh": "它是唯一貼合得夠好的平面", "en": "the only plane that fits closely enough"},
  5: {"zh": "定理 10.2：所有切線的聯集", "en": "Theorem 10.2: the union of the tangent lines"},
  6: {"zh": "一個方向：沿直線抬上去", "en": "one way: lift a straight line"},
  7: {"zh": "另一個方向：任何曲線都在裡面", "en": "the other: every curve lands inside"},
  8: {"zh": "一個具體的例子", "en": "a concrete example"},
  9: {"zh": "兩條純量方程", "en": "two scalar equations"},
  10: {"zh": "四維裡兩個超平面的交", "en": "two hyperplanes in four dimensions"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── the shared axonometric picture of a surface over a domain ─────
 EX, EY, EZ = (1.05, -0.34), (0.66, 0.34), (0.0, 0.80)

 def _P(self, ox, oy, x, y, z):
  return [ox + self.EX[0] * x + self.EY[0] * y + self.EZ[0] * z,
          oy + self.EX[1] * x + self.EY[1] * y + self.EZ[1] * z, 0]

 def _height(self, x, y):
  """A stand-in surface height, only for the pictures: it has to look curved."""
  return 0.34 * (x * x - 0.6 * y * y) + 0.62

 def _domain(self, ox, oy, col=DIM):
  g = VGroup()
  for u in (-1.0, 0.0, 1.0):
   g.add(Line(self._P(ox, oy, u, -1.0, 0), self._P(ox, oy, u, 1.0, 0), color=col, stroke_width=1.0),
         Line(self._P(ox, oy, -1.0, u, 0), self._P(ox, oy, 1.0, u, 0), color=col, stroke_width=1.0))
  return g

 def _surface(self, ox, oy, col=ACCENT_B, sw=2.0):
  g = VGroup()
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([self._P(ox, oy, u, v / 8.0, self._height(u, v / 8.0))
                      for v in range(-8, 9)], col, sw=sw),
         self._curve([self._P(ox, oy, v / 8.0, u, self._height(v / 8.0, u))
                      for v in range(-8, 9)], col, sw=sw))
  return g

 def _plane(self, ox, oy, px, py, col=WARN, sw=2.0, r=0.62):
  """The tangent plane to the stand-in surface at (px, py), drawn as a patch."""
  h0 = self._height(px, py)
  hx = (self._height(px + H, py) - self._height(px - H, py)) / (2 * H)
  hy = (self._height(px, py + H) - self._height(px, py - H)) / (2 * H)
  corners = [(px - r, py - r), (px + r, py - r), (px + r, py + r), (px - r, py + r)]
  pts = [self._P(ox, oy, x, y, h0 + hx * (x - px) + hy * (y - py)) for x, y in corners]
  return self._curve(pts + [pts[0]], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _asurface(self):
  ox, oy = -3.95, -0.30
  g = VGroup(self._domain(ox, oy), self._surface(ox, oy))
  g.add(self._panel(((0.86, "灰色的格子是定義域",
                      "the grey grid is the domain", DIM),
                     (0.20, "藍色那一張是 F 的圖形",
                      "the blue sheet is the graph of F", ACCENT_B),
                     (-0.46, "它住在 V 乘 W 裡，一張蓋在上面的曲面",
                      "it lives in V times W, a surface lying over the domain", ACCENT_A))))
  return g.add(self._foot("實值函數在平面上的圖形是三維裡的曲面，這裡只是把維數放開",
                          "the graph of a real function of two variables is a surface; here dimensions are free",
                          ACCENT_A,
                          "V 與 W 都可以是任何賦範空間，圖形一樣有意義",
                          "V and W may be any normed spaces and the graph still makes sense"))

 def _projections(self):
  ox, oy = -3.95, -0.30
  g = VGroup(self._domain(ox, oy), self._surface(ox, oy))
  px, py = 0.35, -0.30
  top = self._P(ox, oy, px, py, self._height(px, py))
  bot = self._P(ox, oy, px, py, 0.0)
  g.add(Dot(top, radius=0.065, color=WARN), Dot(bot, radius=0.06, color=ACCENT_C),
        self._arr(top, [bot[0], bot[1] + 0.10, 0], ACCENT_C, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "第一個投影把曲面壓回定義域",
                      "the first projection pushes the surface back down", ACCENT_C),
                     (0.20, "ξ 對應到正上方那一點",
                      "xi corresponds to the point directly above it", WARN),
                     (-0.46, "所以曲面與定義域一一對應",
                      "so the surface and the domain match up one to one", ACCENT_A))))
  return g.add(self._foot("習慣上把 V 想成水平的那一層，值域的方向想成垂直的",
                          "one thinks of V as the horizontal layer and the range direction as vertical",
                          ACCENT_A,
                          "這個想像在 V 與 W 都不是一維時仍然有用",
                          "the picture stays useful even when neither V nor W is one dimensional"))

 def _tangentplane(self):
  ox, oy = -3.95, -0.30
  px, py = 0.35, -0.30
  g = VGroup(self._domain(ox, oy), self._surface(ox, oy, col=ACCENT_B, sw=1.6),
             self._plane(ox, oy, px, py))
  g.add(Dot(self._P(ox, oy, px, py, self._height(px, py)), radius=0.065, color=ACCENT_A))
  g.add(self._panel(((0.86, "微分是線性映射，它的圖形過原點",
                      "the differential is linear, so its graph passes the origin", ACCENT_C),
                     (0.20, "把那個子空間平移到接觸點",
                      "translate that subspace to the point of contact", WARN),
                     (-0.46, "得到的就是切平面",
                      "and what you get is the tangent plane", ACCENT_A))))
  return g.add(self._foot("紅色那一片就是切平面，橘點是接觸點",
                          "the red patch is the tangent plane and the orange dot the point of contact",
                          ACCENT_A,
                          "它是一個仿射子空間，不是線性子空間——除非接觸點是原點",
                          "it is an affine subspace, not a linear one, unless the contact point is the origin"))

 def _equation(self):
  g = VGroup()
  lines = (("η   −   F ( α )     =     dF ₐ ( ξ  −  α )", WARN),
           ("G ( ξ )   =   dF ₐ ( ξ − α )   +   F ( α )", ACCENT_B),
           ("M   =   { ⟨ ξ , G ( ξ ) ⟩ }", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "線性部分是微分",
                      "the linear part is the differential", WARN),
                     (0.20, "常數項是接觸點的值",
                      "the constant term is the value at the contact point", ACCENT_B),
                     (-0.46, "所以切平面是一個仿射映射的圖形",
                      "so the tangent plane is the graph of an affine map", ACCENT_C))))
  return g.add(self._foot("跟一元的點斜式完全一樣，只是斜率換成一個線性映射",
                          "exactly the point slope form of one variable, with the slope now a linear map",
                          ACCENT_A,
                          "維數多少都不影響這條式子的樣子",
                          "the shape of this equation does not depend on any dimension"))

 def _unique(self):
  g = VGroup()
  lines = (("ΔF ₐ ( ζ )   =   T ( ζ )   +   o ( ζ )", ACCENT_B),
           ("Hom  ∩  o   =   { 0 }", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._sym(-0.44, "F ( ξ )  −  G ( ξ )   ∈   o ( ξ − α )", WARN, FS_TAG + 1,
                  x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "微分是唯一的線性部分",
                      "the differential is the only linear part", ACCENT_B),
                     (0.20, "理由是 E37 最後那一條",
                      "the reason is E37's closing result", ACCENT_C),
                     (-0.46, "所以那個仿射映射也是唯一的",
                      "so the affine map is unique as well", WARN))))
  return g.add(self._foot("切平面因此是唯一「貼合到小 o 等級」的平面，這是它的定義性質",
                          "the tangent plane is thus the only one fitting to within little oh, which defines it",
                          ACCENT_A,
                          "「切」在這裡是一個逼近的陳述，不是一個幾何的直覺",
                          "tangency here is a statement about approximation, not a geometric intuition"))

 def _thm102(self):
  ox, oy = -3.95, -0.30
  px, py = 0.35, -0.30
  g = VGroup(self._surface(ox, oy, col=DIM, sw=1.2), self._plane(ox, oy, px, py))
  h0 = self._height(px, py)
  for th, col in ((0.4, ACCENT_B), (1.9, ACCENT_C), (3.5, WARN)):
   dx, dy = 0.55 * math.cos(th), 0.55 * math.sin(th)
   hx = (self._height(px + H, py) - self._height(px - H, py)) / (2 * H)
   hy = (self._height(px, py + H) - self._height(px, py - H)) / (2 * H)
   g.add(self._arr(self._P(ox, oy, px, py, h0),
                   self._P(ox, oy, px + dx, py + dy, h0 + hx * dx + hy * dy),
                   col, sw=2.5, tl=0.12))
  g.add(Dot(self._P(ox, oy, px, py, h0), radius=0.065, color=ACCENT_A))
  g.add(self._panel(((0.86, "平面上的每一個向量",
                      "every vector of the plane", ACCENT_B),
                     (0.20, "都是曲面上某條曲線的切向量",
                      "is the tangent vector of some curve in the surface", ACCENT_C),
                     (-0.46, "反過來也成立，所以兩者剛好相等",
                      "and conversely, so the two coincide exactly", WARN))))
  return g.add(self._foot("這給切平面一個純幾何的說法，完全不提小 o",
                          "this gives the tangent plane a purely geometric reading, with no little oh in it",
                          ACCENT_A,
                          "書上把它寫成「所有切線的聯集」，畫面上是其中三條",
                          "the book calls it the union of the tangent lines; three of them are drawn"))

 def _lift(self):
  ox, oy = -3.95, -0.30
  px, py = 0.35, -0.30
  g = VGroup(self._domain(ox, oy, col=DIM), self._surface(ox, oy, col=DIM, sw=1.0))
  h0 = self._height(px, py)
  dx, dy = 0.62, 0.30
  g.add(Line(self._P(ox, oy, px - dx, py - dy, 0), self._P(ox, oy, px + dx, py + dy, 0),
             color=ACCENT_C, stroke_width=2.5))
  g.add(self._curve([self._P(ox, oy, px + dx * u / 8, py + dy * u / 8,
                             self._height(px + dx * u / 8, py + dy * u / 8))
                     for u in range(-8, 9)], ACCENT_B, sw=3))
  hx = (self._height(px + H, py) - self._height(px - H, py)) / (2 * H)
  hy = (self._height(px, py + H) - self._height(px, py - H)) / (2 * H)
  g.add(self._arr(self._P(ox, oy, px, py, h0),
                  self._P(ox, oy, px + dx, py + dy, h0 + hx * dx + hy * dy),
                  WARN, sw=3, tl=0.14),
        Dot(self._P(ox, oy, px, py, h0), radius=0.065, color=ACCENT_A))
  g.add(self._panel(((0.86, "紫色是定義域裡的一條直線",
                      "purple is a straight line in the domain", ACCENT_C),
                     (0.20, "藍色是把它抬到曲面上",
                      "blue is that line lifted onto the surface", ACCENT_B),
                     (-0.46, "紅色是它的切向量，正好是原來那個向量",
                      "red is its tangent vector, which is the vector we started with", WARN))))
  return g.add(self._foot("用的是引理 8.1（逐分量求導）加上定理 7.2（沿弧走還是光滑）",
                          "this uses Lemma 8.1 componentwise and Theorem 7.2 for the arc",
                          ACCENT_A,
                          "取直線是最省事的選擇，任何通過那點的光滑弧都行",
                          "a straight line is the cheapest choice; any smooth arc through the point would do"))

 def _converse(self):
  ox, oy = -3.95, -0.30
  px, py = 0.35, -0.30
  g = VGroup(self._domain(ox, oy, col=DIM), self._surface(ox, oy, col=DIM, sw=1.0))
  curve = [(px + 0.70 * u / 8, py + 0.55 * (u / 8) ** 2 - 0.10) for u in range(-8, 9)]
  g.add(self._curve([self._P(ox, oy, x, y, 0.0) for x, y in curve], ACCENT_C, sw=2.5),
        self._curve([self._P(ox, oy, x, y, self._height(x, y)) for x, y in curve],
                    ACCENT_B, sw=3))
  h0 = self._height(px, py)
  hx = (self._height(px + H, py) - self._height(px - H, py)) / (2 * H)
  hy = (self._height(px, py + H) - self._height(px, py - H)) / (2 * H)
  dx, dy = 0.62, -0.16
  g.add(self._arr(self._P(ox, oy, px, py, h0),
                  self._P(ox, oy, px + dx, py + dy, h0 + hx * dx + hy * dy),
                  WARN, sw=3, tl=0.14),
        Dot(self._P(ox, oy, px, py, h0), radius=0.065, color=ACCENT_A))
  g.add(self._sym(0.86, "γ ′   =   ⟨ λ ′ , dF ₐ ( λ ′ ) ⟩", WARN, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(0.20, "曲面上任何一條光滑曲線",
                  "any smooth curve lying in the surface", ACCENT_B, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.36, "都是定義域裡一條曲線抬上去的",
                  "is a curve in the domain, lifted", ACCENT_C, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以它的切向量本來就落在平面裡",
                  "so its tangent vector lies in the plane already", ACCENT_A, FS_TAG,
                  x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這次的曲線是真的彎的，不是直線，結論一樣成立",
                          "this curve genuinely bends rather than being straight, and the conclusion still holds",
                          ACCENT_A,
                          "兩個方向都成立，所以「平面」與「切向量的集合」是同一件事",
                          "both directions hold, so the plane and the set of tangent vectors are one thing"))

 def _example(self):
  g = VGroup()
  gr, _ = self._numgrid(-4.55, 0.30, [[f"{x:.0f}" for x in r] for r in JAC],
                        color=WARN, dx=0.85, dy=0.60)
  g.add(gr, self._sym(-0.55, "dF ₐ", WARN, FS_TAG, x=-4.55, w=1.60))
  gr2, _ = self._numgrid(-2.05, 0.30, [[f"{FA[0]:.0f}"], [f"{FA[1]:.0f}"]],
                         color=ACCENT_B, dx=0.55, dy=0.60)
  g.add(gr2, self._sym(-0.55, "F ( a )", ACCENT_B, FS_TAG, x=-2.05, w=1.60))
  g.add(self._panel(((0.86, "一個平面到平面的映射",
                      "a map of the plane to the plane", ACCENT_C),
                     (0.20, "它的圖形住在四維空間裡",
                      "its graph lives in four dimensions", ACCENT_A),
                     (-0.46, "在 2 與 1 那一點，這是雅可比與函數值",
                      "at the point two and one, here are the Jacobian and the value", WARN))))
  return g.add(self._foot("雅可比矩陣是程式用中央差商算的，跟手寫的公式核對過",
                          "the Jacobian was computed here by central differences and checked against the formula",
                          ACCENT_A,
                          "四維畫不出來，但方程式一點都不受影響",
                          "four dimensions cannot be drawn, and the equations do not care"))

 def _equations(self):
  g = VGroup()
  lines = (("y ₁   =   x ₁  +  2 x ₂  −  2", ACCENT_B),
           ("y ₂   =   4 x ₁  −  x ₂  −  4", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._rect(-3.55, 0.55 - k * 0.75, 2.05, 0.30, col),
         self._sym(0.55 - k * 0.75, lab, col, FS_TAG + 1, x=-3.55, w=3.90))
  rows = [("       t         | F − G | / ‖ ξ ‖", DIM)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"{t:8.3f}            {REM[k]:.5f}", (ACCENT_B, ACCENT_C, WARN)[k % 3]))
  g.add(self._table(rows, y0=0.62, dy=0.42))
  return g.add(self._foot("把雅可比與函數值代進上一拍那條方程式，就得到這兩條純量方程",
                          "substituting the Jacobian and the value into the equation gives these two",
                          ACCENT_A,
                          "右邊那一列是餘項的商，掉到零，所以貼合的確是小 o 等級",
                          "the right column is the remainder quotient, and it vanishes, so the fit is little oh"))

 def _hyperplanes(self):
  g = VGroup()
  lines = (("x ₁  +  2 x ₂  −  y ₁   =   2", ACCENT_B),
           ("4 x ₁  −  x ₂  −  y ₂   =   4", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._rect(-3.55, 0.62 - k * 0.70, 2.05, 0.30, col),
         self._sym(0.62 - k * 0.70, lab, col, FS_TAG + 1, x=-3.55, w=3.90))
  g.add(self._sym(-0.62, f"γ ′   =   ⟨ {PRED[0]} , {PRED[1]} , {PRED[2]} , {PRED[3]} ⟩",
                  WARN, FS_TAG + 1, x=-3.55, w=4.20))
  g.add(self._panel(((0.86, "每一條各自是四維裡的一個超平面",
                      "each is a hyperplane in four dimensions", ACCENT_B),
                     (0.20, "切平面就是這兩個超平面的交",
                      "the tangent plane is where the two meet", ACCENT_C),
                     (-0.46, "兩個條件、四個變數，交出來是二維",
                      "two conditions on four variables leave two dimensions", WARN))))
  return g.add(self._foot("紅色那個是曲面上一條真的彎的曲線的切向量，它確實滿足兩條方程",
                          "the red vector is a genuinely curved arc's tangent, and it does satisfy both equations",
                          ACCENT_A,
                          "第 3 章第 10 節到此結束，下一集開始講隱函數定理",
                          "that ends section 10; next time, the implicit function theorem"))

 def stage(self):
  a, b, c = self._asurface(), self._projections(), self._tangentplane()
  d, e, f = self._equation(), self._unique(), self._thm102()
  h, i, j = self._lift(), self._converse(), self._example()
  k, l = self._equations(), self._hyperplanes()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE45ZH, AdvCalcE45EN = make(AdvCalcE45Base, "45", prefix="AdvCalcE")
