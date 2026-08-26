"""advcalc E35 -- chapter 3, section 3, second part (book pp. 128-129): the
operator norm as the smallest bound, the integral functional whose norm is
exactly the length of the interval, the two rewritings that remove the
denominator (over the unit sphere, then over the closed unit ball), the
identification of the operator norm with a uniform norm on that ball, maps
bounded below, Hom(V, W) as a normed space (Theorem 3.2) and the product
inequality for composition (Theorem 3.3), and the conjugate space as the
bounded linear functionals.  Book page 129 onward is exercises 3.1 to 3.22 and
E36 opens section 4.

The same linear map as E34 runs through the whole episode so that the numbers
can be checked against each other: its operator norm is found by sweeping the
unit sphere, not read off the matrix, and the largest-row-sum formula is then
asserted to agree.  The three formulations of the definition are computed
separately and asserted equal, which is the content of beats 3 and 4; the
inradius of the image is computed the same way and asserted to be one over the
norm of the inverse, which is beat 6.
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

TMAT = ((2, -1), (1, 1))
SMAT = ((1, 1), (0, 1))
STMAT = tuple(tuple(sum(SMAT[i][k] * TMAT[k][j] for k in range(2)) for j in range(2))
              for i in range(2))
SUMMAT = tuple(tuple(SMAT[i][j] + TMAT[i][j] for j in range(2)) for i in range(2))
TINV = ((1 / 3, 1 / 3), (-1 / 3, 2 / 3))
CORNERS = ((1, 1), (1, -1), (-1, -1), (-1, 1))


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


def _n1(v):
 return abs(v[0]) + abs(v[1])


def _ap(m, v):
 return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


def _sphere(n=1440):
 """The unit sphere of the uniform norm, one point per direction."""
 for k in range(n):
  c, s = math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)
  m = max(abs(c), abs(s))
  yield (c / m, s / m)


def _opnorm(m):
 return max(_ninf(_ap(m, p)) for p in _sphere())


def _rowsum(m):
 return max(sum(abs(x) for x in r) for r in m)


NORM_T, NORM_S = _opnorm(TMAT), _opnorm(SMAT)
NORM_ST, NORM_SUM = _opnorm(STMAT), _opnorm(SUMMAT)
NORM_TINV = _opnorm(TINV)
for _m in (TMAT, SMAT, STMAT, SUMMAT):
 assert abs(_opnorm(_m) - _rowsum(_m)) < 1e-9, \
     "the sup over the sphere disagrees with the largest row sum"
assert abs(NORM_T - 3) < 1e-9 and abs(NORM_S - 2) < 1e-9

# ── beats 3 and 4: three ways of writing the same number ────────────────
LUB_QUOT = max(_ninf(_ap(TMAT, p)) / _ninf(p) for p in _sphere())
LUB_SPHERE = max(_ninf(_ap(TMAT, p)) for p in _sphere())
LUB_BALL = max(_ninf(_ap(TMAT, (x * p[0], x * p[1])))
               for p in _sphere(360) for x in (k / 30 for k in range(1, 31)))
assert abs(LUB_QUOT - LUB_SPHERE) < 1e-9 and abs(LUB_SPHERE - LUB_BALL) < 1e-9, \
    "the three formulations of the operator norm do not agree"

# ── beat 6: bounded below, and the inverse that fixes the constant ──────
_id = tuple(tuple(sum(TMAT[i][k] * TINV[k][j] for k in range(2)) for j in range(2))
            for i in range(2))
assert all(abs(_id[i][j] - (1 if i == j else 0)) < 1e-9 for i in range(2) for j in range(2)), \
    "TINV is not the inverse of TMAT"
LOWER = min(_ninf(_ap(TMAT, p)) for p in _sphere())
assert abs(LOWER - 1 / NORM_TINV) < 1e-6, \
    "the largest lower bound should be one over the norm of the inverse"

# ── beats 8 and 9: the two inequalities, both strict for this pair ──────
assert NORM_SUM < NORM_S + NORM_T and NORM_ST < NORM_S * NORM_T, \
    "both are drawn as inequalities, so a pair attaining equality would mislead"

# ── beat 2: the integral functional on C([0, 2]) ────────────────────────
INT_B = 2.0
INT_FS = (("flat", lambda t: 1.0),
          ("hump", lambda t: math.sin(math.pi * t / 2) ** 2),
          ("spike", lambda t: max(0.0, 1.0 - 4 * abs(t - 1.0))))


def _quot(f, n=4000):
 val = sum(f(INT_B * k / n) for k in range(n)) * INT_B / n
 sup = max(f(INT_B * k / n) for k in range(n + 1))
 return val / sup


INT_Q = [_quot(f) for _, f in INT_FS]
assert abs(INT_Q[0] - INT_B) < 1e-3, "the constant function should attain the bound"
assert all(q < INT_B - 1e-3 for q in INT_Q[1:]), "no other drawn function may reach it"
assert len({round(q, 2) for q in INT_Q}) == 3, "two of the drawn quotients read the same"

# ── beat 7: the right shift is bounded below and still not onto ─────────
SEQ = (0.40, -1.00, 0.70, 0.20, -0.50)
SHIFT = (0.0,) + SEQ[:-1]
assert max(abs(v) for v in SHIFT) == max(abs(v) for v in SEQ), \
    "the shift is supposed to leave the uniform norm alone"
assert SHIFT[0] == 0.0, "the first slot is what the range misses"

# ── beat 10: a functional on the plane, and its norm ────────────────────
AVEC = (2, -1)
NORM_L = max(abs(AVEC[0] * p[0] + AVEC[1] * p[1]) for p in _sphere())
assert abs(NORM_L - _n1(AVEC)) < 1e-9, \
    "the norm of this functional should be the one norm of the vector behind it"


class AdvCalcE35Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 35

 MODE_LABEL = {
  0: {"zh": "最小的那個界值得一個名字", "en": "the smallest bound deserves a name"},
  1: {"zh": "跑得最遠的方向決定它", "en": "the furthest direction fixes it"},
  2: {"zh": "積分：界剛好取得到", "en": "the integral: a bound that is attained"},
  3: {"zh": "齊次性把分母消掉", "en": "homogeneity removes the denominator"},
  4: {"zh": "整顆閉單位球，答案一樣", "en": "the whole closed ball, same answer"},
  5: {"zh": "「有界」回到最原始的意思", "en": "bounded means what it always did"},
  6: {"zh": "有下界：像縮不到多小", "en": "bounded below: the image cannot collapse"},
  7: {"zh": "有下界不保證可逆", "en": "bounded below does not force invertible"},
  8: {"zh": "定理 3.2：Hom 自己是賦範空間", "en": "Theorem 3.2: Hom is itself normed"},
  9: {"zh": "定理 3.3：合成只會變小", "en": "Theorem 3.3: composition only shrinks"},
  10: {"zh": "V 星：有界線性泛函", "en": "V star: the bounded functionals"},
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

 def _square(self, cx, cy, r, col, sw=2.5):
  p = [[cx + r, cy + r, 0], [cx - r, cy + r, 0],
       [cx - r, cy - r, 0], [cx + r, cy - r, 0], [cx + r, cy + r, 0]]
  return self._curve(p, col, sw=sw)

 def _image(self, cx, cy, s, m, col, sw=3):
  p = [[cx + s * _ap(m, v)[0], cy + s * _ap(m, v)[1], 0] for v in CORNERS]
  return self._curve(p + [p[0]], col, sw=sw)

 def _frame(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 # ── beats ─────────────────────────────────────────────────────────
 def _lub(self):
  ox, oy, sx, sy = -5.70, -0.78, 0.700, 0.520
  g = VGroup(Line([ox - 0.16, oy, 0], [ox + 2 * math.pi * sx + 0.30, oy, 0],
                  color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.14, 0], [ox, oy + 3.4 * sy, 0], color=DIM, stroke_width=1.6))
  pts = []
  for k in range(361):
   th = 2 * math.pi * k / 360
   c, s = math.cos(th), math.sin(th)
   u = (c / max(abs(c), abs(s)), s / max(abs(c), abs(s)))
   pts.append([ox + th * sx, oy + _ninf(_ap(TMAT, u)) * sy, 0])
  g.add(self._curve(pts, ACCENT_B, sw=3, maxn=180))
  for val, col, tag in ((NORM_T, WARN, "3"), (LOWER, ACCENT_C, "1")):
   g.add(self._dash([ox, oy + val * sy, 0], [ox + 2 * math.pi * sx, oy + val * sy, 0],
                    col, n=30, sw=1.6),
         Text(tag, font_size=FS_TAG - 4, color=col).move_to([ox - 0.28, oy + val * sy, 0]))
  g.add(self._panel(((0.86, "每個方向都給一個商",
                      "each direction gives one quotient", ACCENT_B),
                     (0.20, "紅線是這些商的最小上界",
                      "the red line is their least upper bound", WARN),
                     (-0.46, "任何比它大的數也是界，所以只記最小的",
                      "anything larger is a bound too, so keep the smallest", DIM))))
  return g.add(self._foot("這條曲線是把方向掃過一圈真的算出來的，不是示意圖",
                          "this curve was computed by sweeping the directions, not sketched",
                          ACCENT_A,
                          "紫線是另一端，那是這一集後半的主角",
                          "the purple line is the other end, and the second half of the episode"))

 def _reach(self):
  cx, cy, s = -3.60, 0.05, 0.32
  g = VGroup(self._frame(cx, cy, 1.25, 1.05))
  g.add(self._square(cx, cy, s, ACCENT_B), self._image(cx, cy, s, TMAT, WARN),
        self._square(cx, cy, s * NORM_T, ACCENT_C, sw=2))
  for sg in (1, -1):
   g.add(Dot([cx + sg * s * NORM_T, cy, 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "藍色單位球，紅色是它的像",
                      "the blue unit ball and its red image", WARN),
                     (0.20, "紫色的半徑就是算子範數",
                      "the radius of the purple one is the operator norm", ACCENT_C),
                     (-0.46, "橘點是碰到的方向，別的方向都構不到",
                      "the orange dots are the directions that reach it", ACCENT_A))))
  return g.add(self._foot("有了名字，那條不等式就有了最省的寫法",
                          "with a name for it, the inequality gets its tightest form",
                          ACCENT_A,
                          "這裡是 3，跟把矩陣每列的絕對值加起來取最大是同一個數",
                          "here it is three, the same number as the largest row of absolute values"))

 def _integral(self):
  g = VGroup()
  for k, ((_, f), q, col) in enumerate(zip(INT_FS, INT_Q, (ACCENT_A, ACCENT_B, ACCENT_C))):
   ox, oy, sx, sy = -5.60 + k * 1.85, -0.42, 0.66, 0.76
   g.add(Line([ox - 0.10, oy, 0], [ox + 2 * sx + 0.10, oy, 0], color=DIM, stroke_width=1.4),
         self._dash([ox, oy + sy, 0], [ox + 2 * sx, oy + sy, 0], DIM, n=16, sw=1.2),
         self._curve([[ox + INT_B * t / 60 * sx, oy + f(INT_B * t / 60) * sy, 0]
                      for t in range(61)], col, sw=3))
   for j in range(1, 24):
    t = INT_B * j / 24
    g.add(Line([ox + t * sx, oy, 0], [ox + t * sx, oy + f(t) * sy, 0],
               color=col, stroke_width=1.0))
   g.add(Text(f"{q:.2f}", font_size=FS_TAG - 3, color=col).move_to([ox + sx, oy - 0.32, 0]))
  g.add(self._panel(((0.88, "三個函數，三個商",
                      "three functions, three quotients", ACCENT_B),
                     (0.28, "只有常數函數把 2 取到",
                      "only the constant reaches two", ACCENT_A),
                     (-0.32, "所以算子範數正好是區間長度",
                      "so the operator norm is exactly the length", ACCENT_C)),
                    x=4.05, w=4.30))
  return g.add(self._foot("最小上界不一定取得到，但這個例子取得到，所以答案是精確的",
                          "a least upper bound need not be attained; this one is, so the answer is exact",
                          ACCENT_A,
                          "虛線是一致範數的高度，商就是陰影面積除以它",
                          "the dashed line is the uniform norm, and the quotient is the area over it"))

 def _homog(self):
  dx, dy, ds = -5.10, 0.05, 0.30
  rx, ry, rs = -1.95, 0.05, 0.16
  long_v, unit_v = (2.0, -2.0), (1.0, -1.0)
  g = VGroup(self._frame(dx, dy, 1.00, 0.95), self._frame(rx, ry, 1.75, 0.95),
             self._square(dx, dy, ds, ACCENT_B, sw=1.8))
  # One arrow per panel, with the unit vector marked on it: the two images lie
  # on the same ray, so drawing both as arrows hides the shorter one entirely.
  g.add(self._arr([dx, dy, 0], [dx + ds * long_v[0], dy + ds * long_v[1], 0],
                  ACCENT_C, sw=2.5, tl=0.12),
        self._arr([rx, ry, 0], [rx + rs * _ap(TMAT, long_v)[0],
                                ry + rs * _ap(TMAT, long_v)[1], 0], ACCENT_C, sw=2.5, tl=0.12),
        Dot([dx + ds * unit_v[0], dy + ds * unit_v[1], 0], radius=0.07, color=ACCENT_A),
        Dot([rx + rs * _ap(TMAT, unit_v)[0], ry + rs * _ap(TMAT, unit_v)[1], 0],
            radius=0.07, color=ACCENT_A))
  g.add(self._panel(((0.92, "長向量除以自己的範數，就落在單位球面上",
                      "divide a vector by its own norm and it lands on the sphere", ACCENT_C),
                     (0.34, "兩個商完全一樣，這就是齊次性",
                      "the two quotients are identical, which is homogeneity", ACCENT_A),
                     (-0.24, "所以分母可以直接消掉",
                      "so the denominator can simply go", ACCENT_B)),
                    x=3.90, w=4.60),
        self._sym(-0.82, "6 / 2   =   3 / 1   =   3", ACCENT_A, FS_TAG - 1,
                  x=3.90, w=4.60))
  return g.add(self._foot("同一條射線上每個向量給的商都一樣，只要挑一個代表",
                          "every vector on one ray gives the same quotient, so pick one representative",
                          ACCENT_A,
                          "代表就挑範數等於一的那個，橘點就是它，剩下的就是在球面上取最小上界",
                          "pick the one of norm one, the orange dot, and what is left is a lub over the sphere"))

 def _closed(self):
  cx, cy, s = -3.60, 0.05, 0.30
  SHRINK = 0.55
  g = VGroup(self._frame(cx, cy, 1.25, 1.05))
  g.add(self._square(cx, cy, s, ACCENT_B, sw=2.5),
        self._square(cx, cy, s * SHRINK, DIM, sw=1.6))
  g.add(self._image(cx, cy, s, TMAT, WARN),
        self._image(cx, cy, s * SHRINK, TMAT, ACCENT_C, sw=2))
  for v in ((1, -1), (-1, 1)):
   g.add(Dot([cx + s * NORM_T * (1 if v[0] > 0 else -1), cy, 0],
             radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "把球縮小，像就照同一個比例縮小",
                      "shrink the ball and the image shrinks by the same factor", ACCENT_C),
                     (0.20, "所以最大的商一定出現在球面上",
                      "so the largest quotient always sits on the sphere", WARN),
                     (-0.46, "在整顆閉球上取最小上界，答案不變",
                      "the lub over the whole closed ball is unchanged", ACCENT_A))))
  return g.add(self._foot("三個版本的定義在程式裡分別算過，三個數字完全相同",
                          "the three versions were each computed separately and came out identical",
                          ACCENT_A,
                          "球面版本比較好證，閉球版本比較好用",
                          "the sphere version is easier to prove and the ball version easier to use"))

 def _uniform(self):
  cx, cy, s = -3.60, 0.05, 0.30
  g = VGroup(self._frame(cx, cy, 1.25, 1.05), self._square(cx, cy, s, ACCENT_B, sw=2))
  g.add(self._image(cx, cy, s, TMAT, WARN))
  for k in range(-9, 10):
   a, b = (k / 9.0, 1.0), (k / 9.0, -1.0)
   g.add(Line([cx + s * _ap(TMAT, a)[0], cy + s * _ap(TMAT, a)[1], 0],
              [cx + s * _ap(TMAT, b)[0], cy + s * _ap(TMAT, b)[1], 0],
              color=WARN, stroke_width=0.9))
  g.add(self._square(cx, cy, s * NORM_T, ACCENT_C, sw=2))
  g.add(self._panel(((0.86, "把定義域限制在閉單位球上",
                      "restrict the domain to the closed unit ball", ACCENT_B),
                     (0.20, "紅色那一整片就是限制後的值域",
                      "the whole red patch is the restricted range", WARN),
                     (-0.46, "它是有界集，最小的框就是算子範數",
                      "it is a bounded set, and the tightest frame is the norm", ACCENT_C))))
  return g.add(self._foot("繞了一圈，「有界」又是最原始的那個意思：值域裝得進一顆球",
                          "the word bounded has come full circle: a range that fits inside a ball",
                          ACCENT_A,
                          "差別只在，要先把定義域切到那顆球上才成立",
                          "the only difference is that the domain has to be cut down first"))

 def _below(self):
  cx, cy, s = -3.60, 0.05, 0.30
  g = VGroup(self._frame(cx, cy, 1.25, 1.05))
  g.add(self._image(cx, cy, s, TMAT, WARN))
  g.add(self._square(cx, cy, s * LOWER, ACCENT_B, sw=2.5),
        self._square(cx, cy, s * NORM_T, ACCENT_C, sw=2))
  for v in ((1, -1), (-1, 1)):
   g.add(Dot([cx + s * v[0], cy + s * v[1], 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "像永遠碰不到裡面那顆藍球的內部",
                      "the image never gets inside the blue ball", ACCENT_B),
                     (0.20, "藍球的半徑就是最大的下界",
                      "the radius of the blue ball is the largest lower bound", ACCENT_A),
                     (-0.46, "它等於反映射的算子範數的倒數",
                      "and it equals one over the norm of the inverse", WARN))))
  return g.add(self._foot("上界看外框，下界看內接的球，同一張圖同時給出 3 與 1",
                          "the upper bound is the outer frame and the lower bound the inscribed ball",
                          ACCENT_A,
                          "橘點是像最靠近原點的地方，那裡剛好貼上藍球",
                          "the orange dots are where the image comes closest, touching the blue ball"))

 def _shift(self):
  ox, dx, sy = -5.30, 0.52, 0.42
  g = VGroup()
  for seq, oyy, col in ((SEQ, 0.46, ACCENT_B), (SHIFT, -0.58, WARN)):
   g.add(Line([ox - 0.16, oyy, 0], [ox + len(seq) * dx, oyy, 0], color=DIM, stroke_width=1.4))
   for k, v in enumerate(seq):
    if abs(v) < 1e-9:
     g.add(Dot([ox + (k + 0.5) * dx, oyy, 0], radius=0.05, color=DIM))
     continue
    g.add(Line([ox + (k + 0.5) * dx, oyy, 0], [ox + (k + 0.5) * dx, oyy + v * sy, 0],
               color=col, stroke_width=6))
  g.add(self._arr([ox + 2.4 * dx, -0.06, 0], [ox + 3.4 * dx, -0.06, 0], DIM, sw=2, tl=0.10))
  g.add(self._panel(((0.92, "把整條數列往右推一格",
                      "push the whole sequence one slot to the right", ACCENT_B),
                     (0.34, "每一項都還在，長度完全沒變",
                      "every entry survives, so the norm does not move", WARN),
                     (-0.24, "但第一格永遠是零，值域漏了一個方向",
                      "but the first slot is always zero, so the range misses one", ACCENT_C)),
                    x=3.90, w=4.60),
        self._sym(-0.82, "( 1 , 0 , 0 , … )   ∉   S [ V ]", ACCENT_A, FS_TAG - 1,
                  x=3.90, w=4.60))
  return g.add(self._foot("下界是一，卻不是滿射，有限維時這種事不可能發生",
                          "the lower bound is one and the map is still not onto, impossible in finite dimensions",
                          ACCENT_A,
                          "維數有限時單射就等於滿射，所以有下界就可逆",
                          "in finite dimensions injective already means onto, so bounded below is invertible"))

 def _hom(self):
  g = VGroup()
  bars = ((NORM_S, "‖ S ‖", ACCENT_B), (NORM_T, "‖ T ‖", ACCENT_C),
          (NORM_SUM, "‖ S + T ‖", WARN), (NORM_S + NORM_T, "‖ S ‖ + ‖ T ‖", ACCENT_A))
  ox, oy, dx, sy = -5.40, -0.62, 1.15, 0.30
  g.add(Line([ox - 0.24, oy, 0], [ox + 4 * dx, oy, 0], color=DIM, stroke_width=1.4))
  for k, (val, tag, col) in enumerate(bars):
   x = ox + (k + 0.5) * dx
   g.add(Line([x, oy, 0], [x, oy + val * sy, 0], color=col, stroke_width=13),
         Text(f"{val:.0f}", font_size=FS_TAG - 3, color=col)
         .move_to([x, oy + val * sy + 0.22, 0]),
         self._sym(oy - 0.30, tag, col, FS_TAG - 4, x=x, w=1.05))
  g.add(self._panel(((0.86, "加法與係數倍都留在裡面",
                      "sums and scalar multiples stay inside", ACCENT_B),
                     (0.20, "而且算子範數滿足三角不等式",
                      "and the operator norm obeys the triangle inequality", WARN),
                     (-0.46, "所以 Hom 自己就是一個賦範線性空間",
                      "so Hom is itself a normed linear space", ACCENT_A))))
  return g.add(self._foot("這一步把「映射」也變成向量，可以再對它談範數與極限",
                          "this turns maps into vectors, so norms and limits apply to them too",
                          ACCENT_A,
                          "第三根比第四根矮，不等式在這裡是嚴格的",
                          "the third bar is shorter than the fourth: the inequality is strict here"))

 def _compose(self):
  g = VGroup()
  s = 0.20
  for cx, m, col in ((-5.30, None, ACCENT_B), (-2.85, TMAT, WARN), (-0.40, STMAT, ACCENT_C)):
   g.add(self._frame(cx, 0.20, 0.95, 0.80))
   g.add(self._square(cx, 0.20, s, col, sw=2.5) if m is None
         else self._image(cx, 0.20, s, m, col, sw=2.5))
  for cx in (-4.20, -1.75):
   g.add(self._arr([cx - 0.24, -0.62, 0], [cx + 0.24, -0.62, 0], DIM, sw=2, tl=0.10))
  g.add(self._sym(-1.00, "‖ S ∘ T ‖  =  3          ‖ S ‖ · ‖ T ‖  =  6", ACCENT_A,
                  FS_TAG - 1, x=-2.85, w=4.40))
  g.add(self._panel(((0.86, "先用 T，再用 S",
                      "T first, then S", WARN),
                     (0.20, "合起來的範數不超過兩個的乘積",
                      "the joined norm is at most the product", ACCENT_C),
                     (-0.46, "常常會比乘積小很多",
                      "and it is often a good deal smaller", ACCENT_A)),
                    x=3.90, w=4.60))
  return g.add(self._foot("兩次放大不會超過兩個放大率相乘，但可能互相抵消",
                          "two stretches never exceed the product of the two factors, and may cancel",
                          ACCENT_A,
                          "「右邊固定接上 T」這件事本身也是一個有界線性變換",
                          "composing on the right by a fixed T is itself a bounded transformation"))

 def _dual(self):
  cx, cy, s = -3.60, 0.05, 0.42
  g = VGroup(self._frame(cx, cy, 1.35, 1.00), self._square(cx, cy, s, ACCENT_B))
  # The level lines of the functional, clipped to the panel: they have slope
  # two, so a segment cut to the panel's width would run right off the top.
  XCAP, YCAP = 2.90, 2.30
  for val, col, sw in ((0.0, DIM, 1.2), (NORM_L, WARN, 2.5), (-NORM_L, WARN, 2.5)):
   xs = [x for x in (val / 2 - YCAP / 2, val / 2 + YCAP / 2)]
   xs = [min(XCAP, max(-XCAP, x)) for x in xs]
   ends = [[cx + s * x, cy + s * (AVEC[0] * x - val) / -AVEC[1], 0] for x in xs]
   g.add(Line(ends[0], ends[1], color=col, stroke_width=sw))
  g.add(self._arr([cx, cy, 0], [cx + s * 1.05 * AVEC[0], cy + s * 1.05 * AVEC[1], 0],
                  ACCENT_C, sw=3, tl=0.12))
  for v in ((1, -1), (-1, 1)):
   g.add(Dot([cx + s * v[0], cy + s * v[1], 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "紫色是那個固定向量",
                      "the purple arrow is the fixed vector", ACCENT_C),
                     (0.20, "紅線是泛函取到最大值的地方",
                      "the red lines are where the functional peaks", WARN),
                     (-0.46, "它們剛好擦過單位球的角",
                      "and they just graze the corners of the unit ball", ACCENT_A))))
  return g.add(self._foot("在一致範數下，這種泛函的算子範數正好是那個向量的一範數",
                          "under the uniform norm such a functional has norm the one norm of its vector",
                          ACCENT_A,
                          "所以對偶空間換了範數也會跟著換，下一集就講這件事",
                          "so the conjugate space changes with the norm, which is the next episode"))

 def stage(self):
  a, b, c = self._lub(), self._reach(), self._integral()
  d, e, f = self._homog(), self._closed(), self._uniform()
  h, i, j = self._below(), self._shift(), self._hom()
  k, l = self._compose(), self._dual()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE35ZH, AdvCalcE35EN = make(AdvCalcE35Base, "35", prefix="AdvCalcE")
