"""advcalc E44 -- chapter 3, section 10, first part (book pp. 161-162): the
maximum and minimum theory of elementary calculus restated for a normed space.
Theorem 10.1 (an interior relative extremum forces the differential to vanish)
and its two-line proof, critical points, what the condition looks like in real
n-space, the box of least surface area for a given volume, the assumption about
the boundary that the argument quietly needs, and the reminder that a vanishing
differential is necessary and not sufficient.  E45 takes the tangent plane from
page 162; pages 163-164 are exercises 10.1 to 10.13.

The box is worked here rather than quoted: the critical point is found, its
gradient is checked to vanish, the surface area there is checked against six
times the volume to the two thirds, and a grid around it is swept to confirm
nothing nearby is smaller.  Three comparison boxes of the same volume are
evaluated so the picture can show that they really are worse.  The saddle of
the last beat has its two directions evaluated as well, since the whole point
is that one is a minimum and the other a maximum.
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

# ── beats 5 to 9: the box of least surface area ────────────────────────
VOL = 8.0


def _area(x, y):
 """Surface area with the third edge eliminated by z = V / (x y)."""
 return 2 * (x * y + VOL / y + VOL / x)


EDGE = VOL ** (1 / 3)
BEST = _area(EDGE, EDGE)
assert abs(EDGE - 2.0) < 1e-12, "the volume was chosen so the edge comes out at two"
assert abs(BEST - 6 * VOL ** (2 / 3)) < 1e-9, "the area is not six times the volume to the two thirds"
assert abs(BEST - 24.0) < 1e-9

_grad = ((_area(EDGE + H, EDGE) - _area(EDGE - H, EDGE)) / (2 * H),
         (_area(EDGE, EDGE + H) - _area(EDGE, EDGE - H)) / (2 * H))
assert max(abs(g) for g in _grad) < 1e-5, "the cube is not a critical point after all"
assert min(_area(EDGE * (1 + dx / 20), EDGE * (1 + dy / 20))
           for dx in range(-8, 9) for dy in range(-8, 9)) >= BEST - 1e-9, \
    "something near the cube has a smaller area, so the picture would be wrong"

# three other boxes of the same volume, for the comparison beat
OTHERS = ((1.0, 2.0), (4.0, 1.0), (2.0, 4.0))
OTHER_AREAS = [2 * (x * y + x * VOL / (x * y) + y * VOL / (x * y)) for x, y in OTHERS]
for (x, y), a in zip(OTHERS, OTHER_AREAS):
 assert abs(x * y * (VOL / (x * y)) - VOL) < 1e-12, "a comparison box has the wrong volume"
 assert a > BEST, "a comparison box beat the cube, which is the opposite of the point"
assert len({round(a, 6) for a in OTHER_AREAS}) == 1, \
    "these three happen to share an area; the beat prints one number for all of them"
OTHER_AREA = OTHER_AREAS[0]

# the boundary really does run away, which is the assumption the argument needs
for _t in (1e-3, 1e-2, 1e3):
 assert _area(_t, 1.0) > 10 * BEST, "the area does not blow up at the boundary"


# ── beat 10: vanishing differential, and neither a maximum nor a minimum
def _saddle(x, y):
 return x * x - y * y


SAD_GRAD = ((_saddle(H, 0.0) - _saddle(-H, 0.0)) / (2 * H),
            (_saddle(0.0, H) - _saddle(0.0, -H)) / (2 * H))
assert max(abs(g) for g in SAD_GRAD) < 1e-9, "the origin should be a critical point"
SAD_UP, SAD_DOWN = _saddle(0.3, 0.0), _saddle(0.0, 0.3)
assert SAD_UP > 0 > SAD_DOWN, "the two directions have to disagree, or the beat says nothing"


class AdvCalcE44Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 44

 MODE_LABEL = {
  0: {"zh": "極值可能出現在哪裡", "en": "where an extreme value can occur"},
  1: {"zh": "定理 10.1：微分必須是零", "en": "Theorem 10.1: the differential vanishes"},
  2: {"zh": "證明：限制到一條直線上", "en": "the proof: restrict to a line"},
  3: {"zh": "臨界點，而且要在內部", "en": "critical points, and interior ones"},
  4: {"zh": "在座標下就是一組方程", "en": "in coordinates it is a system"},
  5: {"zh": "體積固定，表面積最小", "en": "least area for a given volume"},
  6: {"zh": "兩個偏導數設成零", "en": "set both partial derivatives to zero"},
  7: {"zh": "答案是正方體", "en": "the answer is a cube"},
  8: {"zh": "同體積的其他盒子都比較大", "en": "other boxes of the same volume are worse"},
  9: {"zh": "偷偷用掉的那個假設", "en": "the assumption that was slipped in"},
  10: {"zh": "必要，但不充分", "en": "necessary, but not sufficient"},
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

 def _cross(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _box(self, cx, cy, ex, ey, ez, col, sw=2.2):
  """A rectangular box in axonometric projection, drawn as nine edges."""
  EX, EY, EZ = (0.86, -0.30), (0.60, 0.30), (0.0, 0.92)
  P = lambda x, y, z: [cx + EX[0] * x + EY[0] * y + EZ[0] * z,
                       cy + EX[1] * x + EY[1] * y + EZ[1] * z, 0]
  a, b, c = ex, ey, ez
  edges = (((0, 0, 0), (a, 0, 0)), ((0, 0, 0), (0, b, 0)), ((0, 0, 0), (0, 0, c)),
           ((a, 0, 0), (a, b, 0)), ((0, b, 0), (a, b, 0)), ((a, 0, 0), (a, 0, c)),
           ((0, b, 0), (0, b, c)), ((0, 0, c), (a, 0, c)), ((0, 0, c), (0, b, c)),
           ((a, b, 0), (a, b, c)), ((a, 0, c), (a, b, c)), ((0, b, c), (a, b, c)))
  g = VGroup()
  for p, q in edges:
   g.add(Line(P(*p), P(*q), color=col, stroke_width=sw))
  return g

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _where(self):
  cx, cy = -3.85, 0.10
  g = VGroup(self._blob(cx, cy, 1.45, 0.85, 0.16, ACCENT_C))
  for dx, dy, col, r in ((-0.55, 0.22, WARN, 0.075), (0.62, -0.30, ACCENT_B, 0.075)):
   g.add(Dot([cx + dx, cy + dy, 0], radius=r, color=col))
  g.add(Dot([cx + 1.52, cy + 0.06, 0], radius=0.075, color=DIM))
  g.add(self._panel(((0.86, "紅點與藍點在內部，定理管得到",
                      "the red and blue points are interior, so the theorem applies", WARN),
                     (0.20, "灰點在邊界上，定理管不到",
                      "the grey point is on the boundary and is not covered", DIM),
                     (-0.46, "這一整節問的就是「極值能出現在哪」",
                      "the whole section asks where an extreme value can occur", ACCENT_A))))
  return g.add(self._foot("初等微積分的極大極小理論搬過來，幾乎一個字都不用改",
                          "the maximum and minimum theory of elementary calculus carries over almost verbatim",
                          ACCENT_A,
                          "唯一的差別是導數換成微分，而微分是一個線性映射",
                          "the only change is that the derivative becomes a differential, which is a linear map"))

 def _thm101(self):
  ox, oy, sx, sy = -5.35, -0.35, 1.55, 1.05
  X = lambda t: ox + (t + 1.15) * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-1.20), Y(0), 0], [X(1.20), Y(0), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(-1.15 + 2.30 * k / 90), Y(0.85 - 0.62 * (-1.15 + 2.30 * k / 90) ** 2), 0]
                     for k in range(91)], ACCENT_B, sw=3))
  g.add(Dot([X(0.0), Y(0.85), 0], radius=0.07, color=WARN),
        self._dash([X(-0.95), Y(0.85), 0], [X(0.95), Y(0.85), 0], WARN, n=18, sw=2))
  g.add(self._panel(((0.86, "在內部取到相對極大值",
                      "a relative maximum at an interior point", WARN),
                     (0.20, "而且微分在那裡存在",
                      "with the differential existing there", ACCENT_B),
                     (-0.46, "那麼微分就是零映射",
                      "then the differential is the zero map", ACCENT_A))))
  return g.add(self._foot("極小的情形一模一樣，把不等號反過來就好",
                          "a relative minimum is identical with the inequality reversed",
                          ACCENT_A,
                          "紅色那條虛線是切線——它是水平的，這就是結論",
                          "the dashed red line is the tangent, and its being level is the conclusion"))

 def _proof(self):
  cx, cy, s = -4.35, 0.15, 0.85
  g = VGroup(self._cross(cx, cy, 1.35, 0.85))
  for th, col in ((0.0, ACCENT_B), (2.1, ACCENT_C), (4.0, WARN)):
   g.add(self._arr([cx, cy, 0], [cx + s * math.cos(th), cy + s * math.sin(th), 0],
                   col, sw=2.5, tl=0.12))
  g.add(Dot([cx, cy, 0], radius=0.07, color=ACCENT_A))
  g.add(self._sym(0.86, "γ ( t )   =   F ( α + t ξ )", ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.26, "γ ′ ( 0 )   =   0", ACCENT_C, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(-0.34, "dF ₐ ( ξ )   =   D ξ F ( α )   =   0", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "每個方向都零，所以微分是零",
                  "every direction gives zero, so the differential is zero",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("把多變數的問題壓成一變數，再引用一元微積分——E39 的老套路",
                          "squash the many variable question into one and quote elementary calculus, as in E39",
                          ACCENT_A,
                          "這裡用到的只有「方向導數存在而且等於微分」，也就是定理 7.2",
                          "all that is used is Theorem 7.2, that the directional derivative is the differential"))

 def _critical(self):
  cx, cy = -3.85, 0.10
  g = VGroup(self._blob(cx, cy, 1.45, 0.85, 0.16, ACCENT_C))
  for dx, dy, col in ((-0.62, 0.26, WARN), (0.55, -0.34, WARN), (0.05, 0.10, ACCENT_B)):
   g.add(Dot([cx + dx, cy + dy, 0], radius=0.07, color=col))
  g.add(Dot([cx + 1.52, cy + 0.06, 0], radius=0.07, color=DIM))
  g.add(self._curve([[cx + 1.44, cy - 0.06, 0], [cx + 1.60, cy + 0.18, 0]], DIM, sw=2.5),
        self._curve([[cx + 1.60, cy - 0.06, 0], [cx + 1.44, cy + 0.18, 0]], DIM, sw=2.5))
  g.add(self._panel(((0.86, "微分等於零的點，叫臨界點",
                      "a point where the differential vanishes is critical", WARN),
                     (0.20, "內部的極值只能出現在臨界點",
                      "an interior extreme value happens only at one", ACCENT_B),
                     (-0.46, "邊界上的點不受這條定理管",
                      "boundary points are not covered by the theorem", DIM))))
  return g.add(self._foot("所以解題的第一步永遠是「把臨界點找出來」",
                          "so the first step in any such problem is to find the critical points",
                          ACCENT_A,
                          "但邊界要另外處理，後面那個盒子的例子就會碰到",
                          "the boundary needs separate treatment, as the box example will show"))

 def _system(self):
  g = VGroup()
  lines = (("∂ F / ∂ x ₁ ( a )   =   0", ACCENT_B),
           ("∂ F / ∂ x ₂ ( a )   =   0", ACCENT_C),
           ("⋮", DIM),
           ("∂ F / ∂ x ₙ ( a )   =   0", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.82 - k * 0.52, lab, col, FS_TAG + 1, x=-3.55, w=4.60))
  g.add(Line([-5.95, 1.05, 0], [-5.95, -0.90, 0], color=DIM, stroke_width=2),
        Line([-5.95, 1.05, 0], [-5.75, 1.05, 0], color=DIM, stroke_width=2),
        Line([-5.95, -0.90, 0], [-5.75, -0.90, 0], color=DIM, stroke_width=2))
  g.add(self._panel(((0.86, "n 個方程、n 個未知數",
                      "n equations in n unknowns", ACCENT_B),
                     (0.20, "這就是大家實際在解的東西",
                      "this is what anyone actually solves", ACCENT_C),
                     (-0.46, "解出來的只是候選點，還沒分類",
                      "its solutions are only candidates, not yet sorted", WARN))))
  return g.add(self._foot("哪些是極大、哪些是極小、哪些兩者都不是，這條定理不回答",
                          "which are maxima, which minima and which neither, the theorem does not say",
                          ACCENT_A,
                          "要分類得看二階微分，那是第 16 節的事",
                          "sorting them needs the second differential, which is section 16"))

 def _boxsetup(self):
  g = VGroup(self._box(-5.05, -0.55, 1.15, 0.95, 1.30, ACCENT_B))
  g.add(self._sym(0.86, "A   =   2 ( x y  +  x z  +  y z )", ACCENT_B, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._sym(0.26, f"V   =   x y z   =   {VOL:.0f}", WARN, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "體積固定，問表面積最小的形狀",
                  "the volume is fixed; which shape has least area?", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "先用體積把第三個變數消掉",
                  "first use the volume to eliminate the third variable", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("消掉之後只剩兩個自由的變數，就可以用臨界點的條件",
                          "with it eliminated only two free variables remain, and the criterion applies",
                          ACCENT_A,
                          "這是「有約束的極值」最土法的解法：把約束代進去",
                          "this is the crudest way to handle a constraint: substitute it in"))

 def _solve(self):
  g = VGroup()
  lines = (("∂ A / ∂ x   =   0        ⇒        V   =   x ² y", ACCENT_B),
           ("∂ A / ∂ y   =   0        ⇒        V   =   x y ²", ACCENT_C),
           ("x ² y   =   x y ²        ⇒        x   =   y", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.45, w=5.30))
  g.add(self._panel(((0.86, "兩個偏導數各自設成零",
                      "set each partial derivative to zero", ACCENT_B),
                     (0.20, "兩式左邊相同，右邊一比就得到 x 等於 y",
                      "the two left sides agree, so comparing gives x equal to y", ACCENT_C),
                     (-0.46, "對稱性在這裡是算出來的，不是假設的",
                      "the symmetry here is derived, not assumed", WARN))))
  return g.add(self._foot("很多人一開始就假設「答案應該對稱」——這裡不必假設，它自己掉出來",
                          "many would assume the answer is symmetric; here it falls out instead",
                          ACCENT_A,
                          "把 x 等於 y 代回體積，第三邊也跟著相等",
                          "substituting x equal to y back into the volume makes the third edge match"))

 def _cube(self):
  g = VGroup(self._box(-4.85, -0.62, 1.20, 1.20, 1.20, WARN, sw=2.6))
  g.add(self._sym(0.86, f"x  =  y  =  z  =  {EDGE:.0f}", WARN, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._sym(0.20, f"A   =   {BEST:.0f}   =   6 · V ^ ( 2 / 3 )", ACCENT_A,
                  FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._mid(-0.46, "三邊全部相等，所以是正方體",
                  "all three edges agree, so it is a cube", ACCENT_B, FS_TAG,
                  x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("程式驗過這一點的梯度確實是零，而且附近 289 個點沒有更小的",
                          "the gradient here was checked to vanish and 289 nearby points were checked to be worse",
                          ACCENT_A,
                          "體積取八，邊長就是二，表面積是二十四",
                          "with the volume eight the edge is two and the area twenty four"))

 def _compare(self):
  g = VGroup()
  boxes = ((-5.45, 1.20, 1.20, 1.20, WARN, f"{BEST:.0f}"),
           (-2.95, 0.60, 1.20, 2.40, ACCENT_B, f"{OTHER_AREA:.0f}"),
           (-0.45, 2.40, 0.60, 1.20, ACCENT_C, f"{OTHER_AREA:.0f}"))
  for cx, ex, ey, ez, col, lab in boxes:
   g.add(self._box(cx, -0.52, ex * 0.62, ey * 0.62, ez * 0.62, col, sw=2.2),
         self._sym(-0.92, lab, col, FS_TAG + 2, x=cx + 0.45, w=1.20))
  g.add(self._panel(((0.86, "三個盒子體積都是八",
                      "all three boxes have volume eight", ACCENT_A),
                     (0.20, "正方體的表面積是 24",
                      "the cube's area is twenty four", WARN),
                     (-0.46, "拉長的兩個都是 28",
                      "both stretched ones are twenty eight", ACCENT_B)),
                    x=3.90, w=4.60))
  return g.add(self._foot("這不是證明，但它讓結論看得見，也確認方向沒有搞反",
                          "this is not a proof, but it makes the conclusion visible and the direction right",
                          ACCENT_A,
                          "拉得越長，兩個細長的面就越大，表面積跟著往上跑",
                          "the longer it is stretched, the larger the two slender faces and the greater the area"))

 def _boundary(self):
  # A first draft subtracted a constant and clipped the result, which flattened
  # the whole curve into a straight line. Plot the area itself over a window
  # where both ends are already climbing.
  XLO, XHI, BASE = 0.70, 5.20, 20.0
  ox, oy = -5.40, -0.75
  sx, sy = 4.20 / (XHI - XLO), 0.10
  X = lambda x: ox + (x - XLO) * sx
  Y = lambda a: oy + (a - BASE) * sy
  g = VGroup(Line([X(XLO) - 0.16, oy, 0], [X(XHI) + 0.20, oy, 0], color=DIM, stroke_width=1.6),
             Line([X(XLO), oy - 0.14, 0], [X(XLO), Y(36.0), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(XLO + (XHI - XLO) * k / 140),
                      Y(_area(XLO + (XHI - XLO) * k / 140, EDGE)), 0] for k in range(141)],
                    ACCENT_B, sw=3))
  g.add(Dot([X(EDGE), Y(BEST), 0], radius=0.07, color=WARN),
        self._dash([X(XLO), Y(BEST), 0], [X(XHI), Y(BEST), 0], WARN, n=26, sw=1.4))
  for x, ox2 in ((XLO, -0.30), (XHI, 0.30)):
   g.add(self._arr([X(x) + ox2 * 0.2, Y(_area(x, EDGE)), 0],
                   [X(x) + ox2, Y(_area(x, EDGE)) + 0.34, 0], ACCENT_C, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "兩端都往上跑，跑到無窮",
                      "both ends climb, and climb without bound", ACCENT_C),
                     (0.20, "所以極小值不會逃到邊界上",
                      "so the minimum cannot escape to the boundary", WARN),
                     (-0.46, "書上把這一步留成習題，但它是必要的",
                      "the book leaves this as an exercise, and it is needed", ACCENT_A))))
  return g.add(self._foot("沒有這一步，前面只證明了「如果內部有極小值，它在正方體」",
                          "without it, all that was shown is that any interior minimum is the cube",
                          ACCENT_A,
                          "臨界點的條件永遠只給候選，存在性要另外交代",
                          "the critical point condition only ever gives candidates; existence is a separate matter"))

 def _saddlebeat(self):
  ox, oy = -3.95, 0.05
  EX, EY, EZ = (0.90, -0.32), (0.66, 0.30), (0.0, 0.72)
  P = lambda x, y, z: [ox + EX[0] * x + EY[0] * y + EZ[0] * z,
                       oy + EX[1] * x + EY[1] * y + EZ[1] * z, 0]
  g = VGroup()
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([P(u, v / 10.0, 0.62 * _saddle(u, v / 10.0)) for v in range(-10, 11)],
                     ACCENT_C, sw=1.8),
         self._curve([P(v / 10.0, u, 0.62 * _saddle(v / 10.0, u)) for v in range(-10, 11)],
                     ACCENT_C, sw=1.8))
  g.add(self._curve([P(v / 10.0, 0.0, 0.62 * _saddle(v / 10.0, 0.0)) for v in range(-10, 11)],
                    WARN, sw=3),
        self._curve([P(0.0, v / 10.0, 0.62 * _saddle(0.0, v / 10.0)) for v in range(-10, 11)],
                    ACCENT_B, sw=3),
        Dot(P(0, 0, 0), radius=0.07, color=ACCENT_A))
  g.add(self._panel(((0.86, "原點的微分是零，是臨界點",
                      "the differential vanishes at the origin, so it is critical", ACCENT_A),
                     (0.20, "紅色那條上，原點是極小",
                      "along the red curve the origin is a minimum", WARN),
                     (-0.46, "藍色那條上，原點是極大",
                      "along the blue one it is a maximum", ACCENT_B))))
  return g.add(self._foot("同一點在一個方向是谷底、在另一個方向是山頂，所以兩者都不是",
                          "a valley in one direction and a peak in another, so it is neither",
                          ACCENT_A,
                          "充分條件要看二階微分是不是定號的二次型，留到第 16 節",
                          "the sufficient condition asks whether the second differential is a definite form"))

 def stage(self):
  a, b, c = self._where(), self._thm101(), self._proof()
  d, e, f = self._critical(), self._system(), self._boxsetup()
  h, i, j = self._solve(), self._cube(), self._compare()
  k, l = self._boundary(), self._saddlebeat()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE44ZH, AdvCalcE44EN = make(AdvCalcE44Base, "44", prefix="AdvCalcE")
