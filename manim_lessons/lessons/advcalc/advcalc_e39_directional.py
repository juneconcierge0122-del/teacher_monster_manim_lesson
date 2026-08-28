"""advcalc E39 -- chapter 3, section 7, first part (book pp. 146-148): a
parametrized arc and its tangent vector, Theorem 7.1 (the tangent vector is the
skeleton of the arc's differential), the restriction of a map to a straight
line, the directional derivative, the warning that "direction" is a misuse of
the word, Theorem 7.2 (differentiable implies every directional derivative
exists and equals the differential applied to xi), and the homogeneous
counterexample showing the converse fails.  E40 takes the mean-value theorem
from page 148; pages 151-152 are exercises 7.1 to 7.15.

The two maps that carry the episode are the same one E38 used for its chain
rule, so its Jacobian is already familiar, and the book's own smallest
counterexample.  Every directional derivative shown is evaluated by a central
difference and asserted against the Jacobian, and the counterexample's three
properties -- homogeneous, continuous at the origin, every directional
derivative present -- are each checked, as is the one property it lacks, since
the whole beat rests on it failing to be additive.
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


# ── beats 0 to 2: one parametrized arc in the plane ────────────────────
def _arc(t):
 return (t, 0.55 * t * t + 0.25 * t)


ARC_X = 0.55
ARC_TAN = (1.0, 2 * 0.55 * ARC_X + 0.25)
_h = 1e-6
_num = tuple((a - b) / (2 * _h) for a, b in zip(_arc(ARC_X + _h), _arc(ARC_X - _h)))
assert max(abs(a - b) for a, b in zip(_num, ARC_TAN)) < 1e-6, \
    "the tangent vector drawn is not the one the difference quotient gives"


# ── beats 3 to 7: a differentiable map, and its Jacobian ───────────────
def _F(v):
 return (v[0] ** 2 + v[1], v[0] * v[1])


ALPHA = (1.0, 1.0)
JAC = ((2 * ALPHA[0], 1.0), (ALPHA[1], ALPHA[0]))


def _ap(m, v):
 return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


def _dd(f, a, xi, h=1e-6):
 """The directional derivative, by a central difference."""
 p, m = f((a[0] + h * xi[0], a[1] + h * xi[1])), f((a[0] - h * xi[0], a[1] - h * xi[1]))
 return ((p[0] - m[0]) / (2 * h), (p[1] - m[1]) / (2 * h))


DIRS = ((1.0, 0.0), (0.0, 1.0), (1.0, -1.0))
for _xi in DIRS:
 assert max(abs(a - b) for a, b in zip(_dd(_F, ALPHA, _xi), _ap(JAC, _xi))) < 1e-4, \
     "a directional derivative disagrees with the differential applied to the same vector"

# beat 5: the same direction, three different derivatives
RAY = (1.0, 0.0)
SCALES = (1.0, 2.0, 3.0)
RAY_D = [_dd(_F, ALPHA, (c * RAY[0], c * RAY[1])) for c in SCALES]
for _c, _d in zip(SCALES, RAY_D):
 assert max(abs(a - _c * b) for a, b in zip(_d, RAY_D[0])) < 1e-4, \
     "scaling xi should scale the directional derivative by the same factor"
assert RAY_D[0] != RAY_D[1], "the whole point is that these three differ"

# beat 6: a curved arc through alpha, not a straight line
def _lam(t):
 return (ALPHA[0] + t, ALPHA[1] + t * t)


LAM_TAN = tuple((a - b) / (2 * _h) for a, b in zip(_lam(_h), _lam(-_h)))
GAM_TAN = tuple((a - b) / (2 * _h) for a, b in zip(_F(_lam(_h)), _F(_lam(-_h))))
assert max(abs(a - b) for a, b in zip(GAM_TAN, _ap(JAC, LAM_TAN))) < 1e-4, \
    "Theorem 7.2 fails on the drawn arc, so the picture would be claiming something false"


# ── beats 8 to 10: the book's smallest counterexample ──────────────────
def _H(v):
 x, y = v
 return 0.0 if (x == 0.0 and y == 0.0) else x ** 3 / (x * x + y * y)


HOM_DIRS = ((1.0, 0.0), (1.0, 1.0), (2.0, -1.0))
HOM_VALS = [_H(v) for v in HOM_DIRS]
for _t in (0.5, 2.0, -3.0):
 for _v in HOM_DIRS + ((0.0, 1.0),):
  assert abs(_H((_t * _v[0], _t * _v[1])) - _t * _H(_v)) < 1e-12, "this function is not homogeneous"
for _v, _val in zip(HOM_DIRS, HOM_VALS):
 _d = (_H((1e-7 * _v[0], 1e-7 * _v[1])) - _H((0.0, 0.0))) / 1e-7
 assert abs(_d - _val) < 1e-6, "the directional derivative at the origin should be the value at xi"
assert len({round(v, 3) for v in HOM_VALS}) == 3, "the three slopes drawn should be visibly different"

# continuous at the origin: the value on a circle of radius r never exceeds r
for _r in (1.0, 0.1, 0.01):
 assert max(abs(_H((_r * math.cos(2 * math.pi * k / 360), _r * math.sin(2 * math.pi * k / 360))))
            for k in range(360)) <= _r + 1e-12, "this function is not continuous at the origin"

# and the one thing it is not: additive
ADD_A, ADD_B = (1.0, 0.0), (0.0, 1.0)
ADD_SUM = (ADD_A[0] + ADD_B[0], ADD_A[1] + ADD_B[1])
assert abs((_H(ADD_A) + _H(ADD_B)) - _H(ADD_SUM)) > 0.4, \
    "the counterexample only works because this fails, and it should fail visibly"

# The only linear map that could be its differential is the one reading off the two
# basis directions. Beat 10 draws it and shows where it parts company.
LIN_A, LIN_B = _H((1.0, 0.0)), _H((0.0, 1.0))


def _lin(th):
 return LIN_A * math.cos(th) + LIN_B * math.sin(th)


for _k in (0, 90, 180, 270):
 _th = 2 * math.pi * _k / 360
 assert abs(_H((math.cos(_th), math.sin(_th))) - _lin(_th)) < 1e-12, \
     "the linear candidate should agree with the function on the axes"
GAP = max(abs(_H((math.cos(2 * math.pi * k / 720), math.sin(2 * math.pi * k / 720))) - _lin(2 * math.pi * k / 720))
          for k in range(720))
assert GAP > 0.3, "the two curves have to part company visibly, or the beat shows nothing"


class AdvCalcE39Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 39

 MODE_LABEL = {
  0: {"zh": "從區間到賦範空間的函數", "en": "a function from an interval into a normed space"},
  1: {"zh": "參數化弧與它的切向量", "en": "a parametrized arc, and its tangent vector"},
  2: {"zh": "定理 7.1：切向量就是骨架", "en": "Theorem 7.1: the tangent vector is the skeleton"},
  3: {"zh": "一次只看一條直線", "en": "one straight line at a time"},
  4: {"zh": "方向導數的定義", "en": "the directional derivative"},
  5: {"zh": "「方向」其實用錯了字", "en": "direction is the wrong word"},
  6: {"zh": "定理 7.2：沿光滑弧走還是光滑", "en": "Theorem 7.2: smooth arcs stay smooth"},
  7: {"zh": "微分可以一個方向一個方向讀", "en": "the differential, one direction at a time"},
  8: {"zh": "齊次函數：限制到直線就是直線", "en": "homogeneous: a line restricts to a line"},
  9: {"zh": "可微的齊次函數只能是線性的", "en": "a differentiable homogeneous map must be linear"},
  10: {"zh": "所以非線性的齊次函數就是反例", "en": "so any nonlinear one is a counterexample"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 def _arcpath(self, cx, cy, s, col, lo=-1.05, hi=1.15, sw=3):
  pts = [[cx + s * _arc(lo + (hi - lo) * k / 90)[0],
          cy + s * _arc(lo + (hi - lo) * k / 90)[1], 0] for k in range(91)]
  return self._curve(pts, col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _interval(self):
  ix, iy = -5.30, 0.05
  g = VGroup(Line([ix - 0.85, iy, 0], [ix + 0.85, iy, 0], color=DIM, stroke_width=2.5))
  for x, lab, col in ((ix - 0.20, "x", WARN), (ix + 0.42, "x + t", ACCENT_C)):
   g.add(Dot([x, iy, 0], radius=0.06, color=col),
         Text(lab, font_size=FS_TAG - 4, color=col).move_to([x, iy - 0.30, 0]))
  g.add(self._arr([ix + 1.05, iy, 0], [ix + 1.70, iy, 0], ACCENT_A, sw=2.5, tl=0.12),
        Text("f", font_size=FS_TAG - 3, color=ACCENT_A).move_to([ix + 1.38, iy + 0.26, 0]))
  cx, cy, s = -1.85, -0.05, 1.05
  g.add(self._cross(cx, cy, 1.35, 0.95), self._arcpath(cx, cy, s, ACCENT_B))
  p0, p1 = _arc(ARC_X - 0.55), _arc(ARC_X + 0.42)
  g.add(Dot([cx + s * p0[0], cy + s * p0[1], 0], radius=0.06, color=WARN),
        Dot([cx + s * p1[0], cy + s * p1[1], 0], radius=0.06, color=ACCENT_C),
        Line([cx + s * p0[0], cy + s * p0[1], 0], [cx + s * p1[0], cy + s * p1[1], 0],
             color=ACCENT_A, stroke_width=2.5))
  g.add(self._panel(((0.86, "分子是兩個向量的差",
                      "the numerator is a difference of vectors", ACCENT_C),
                     (0.20, "分母還是一個實數",
                      "the denominator is still a real number", ACCENT_B),
                     (-0.46, "所以商是向量，定義一字不改",
                      "so the quotient is a vector and the definition stands", ACCENT_A))))
  return g.add(self._foot("橘色那條割線，就是差商在還沒取極限時的樣子",
                          "the orange chord is the difference quotient before the limit is taken",
                          ACCENT_A,
                          "值域是賦範空間，維數多少都行，這一節從頭到尾不需要座標",
                          "the range is any normed space; no coordinates are needed anywhere here"))

 def _tangent(self):
  cx, cy, s = -3.55, 0.00, 1.15
  g = VGroup(self._cross(cx, cy, 1.75, 0.95), self._arcpath(cx, cy, s, ACCENT_B))
  p = _arc(ARC_X)
  px, py = cx + s * p[0], cy + s * p[1]
  g.add(Dot([px, py, 0], radius=0.065, color=WARN),
        self._arr([px, py, 0], [px + s * 0.62 * ARC_TAN[0], py + s * 0.62 * ARC_TAN[1], 0],
                  ACCENT_A, sw=3, tl=0.14))
  for u in (-0.75, -0.15, 1.00):
   q = _arc(u)
   g.add(Dot([cx + s * q[0], cy + s * q[1], 0], radius=0.05, color=DIM))
  g.add(self._panel(((0.86, "值域是一條曲線，叫參數化弧",
                      "the range is a curve, called a parametrized arc", ACCENT_B),
                     (0.20, "導數就叫那一點的切向量",
                      "the derivative is called the tangent vector there", ACCENT_A),
                     (-0.46, "每一點都有，就說整條弧光滑",
                      "one at every point makes the whole arc smooth", DIM))))
  return g.add(self._foot("弧是函數，不是它的值域——同一條曲線可以有很多種走法",
                          "an arc is the function, not its range: one curve admits many parametrizations",
                          ACCENT_A,
                          "走法不同，切向量的長度就不同，方向才是共有的",
                          "different parametrizations give different lengths, and only the direction is shared"))

 def _skeleton(self):
  ix, iy = -5.30, 0.05
  g = VGroup(Line([ix - 0.30, iy, 0], [ix + 1.05, iy, 0], color=DIM, stroke_width=2))
  for h, col in ((0.42, ACCENT_B), (0.84, ACCENT_C)):
   g.add(Dot([ix + h, iy, 0], radius=0.06, color=col))
  g.add(Text("h", font_size=FS_TAG - 4, color=DIM).move_to([ix + 0.60, iy - 0.30, 0]))
  g.add(self._arr([ix + 1.30, iy, 0], [ix + 1.95, iy, 0], ACCENT_A, sw=2.5, tl=0.12))
  cx, cy, s = -1.85, -0.05, 0.72
  g.add(self._cross(cx, cy, 1.35, 0.95))
  for h, col in ((1.0, ACCENT_B), (2.0, ACCENT_C)):
   g.add(self._arr([cx, cy, 0], [cx + s * h * ARC_TAN[0], cy + s * h * ARC_TAN[1], 0],
                   col, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "微分吃一個實數，吐一個向量",
                      "the differential eats a number and returns a vector", ACCENT_B),
                     (0.20, "它做的事只有「乘上切向量」",
                      "all it does is multiply by the tangent vector", ACCENT_A),
                     (-0.46, "所以切向量就是它的骨架",
                      "so the tangent vector is its skeleton", ACCENT_C))))
  return g.add(self._foot("定義域只有一維，Hom 就只剩下「乘一個固定向量」這一種映射",
                          "with a one dimensional domain, Hom holds nothing but multiplication by a vector",
                          ACCENT_A,
                          "可微與切向量存在因此是同一件事，這就是定理 7.1",
                          "differentiable and having a tangent vector are therefore the same, which is Theorem 7.1"))

 def _restrict(self):
  dx, dy, ds = -5.15, 0.05, 0.62
  rx, ry, rs = -1.90, 0.05, 0.42
  g = VGroup(self._cross(dx, dy, 0.95, 0.90), self._cross(rx, ry, 1.60, 0.90),
             Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.86, 0.86, 0]),
             Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx - 1.50, 0.86, 0]))
  ax, ay = dx + ds * (ALPHA[0] - 1.0), dy + ds * (ALPHA[1] - 1.0)
  xi = DIRS[2]
  g.add(Line([ax - ds * 1.15 * xi[0], ay - ds * 1.15 * xi[1], 0],
             [ax + ds * 1.15 * xi[0], ay + ds * 1.15 * xi[1], 0], color=ACCENT_C, stroke_width=2.5),
        Dot([ax, ay, 0], radius=0.065, color=WARN),
        Text("α", font_size=FS_TAG - 4, color=WARN).move_to([ax - 0.26, ay + 0.20, 0]))
  base = _F(ALPHA)
  pts = []
  for k in range(61):
   t = -1.15 + 2.30 * k / 60
   q = _F((ALPHA[0] + t * xi[0], ALPHA[1] + t * xi[1]))
   pts.append([rx + rs * (q[0] - base[0]), ry + rs * (q[1] - base[1]), 0])
  g.add(self._curve(pts, ACCENT_B, sw=3), Dot([rx, ry, 0], radius=0.065, color=WARN))
  g.add(self._arr([dx + 1.10, dy - 0.62, 0], [rx - 1.75, ry - 0.62, 0], ACCENT_A, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "紫色那條直線是定義域裡挑的",
                      "the purple line is chosen in the domain", ACCENT_C),
                     (0.20, "把 F 限制上去，就得到一條弧",
                      "restricting F to it produces an arc", ACCENT_B),
                     (-0.46, "一條弧只有一個變數，好處理得多",
                      "an arc has one variable, which is far easier", ACCENT_A))))
  return g.add(self._foot("這是把多變數的問題暫時壓成一變數的標準手法",
                          "this is the standard move: squash a many variable question into one variable",
                          ACCENT_A,
                          "代價是每個方向都要問一次，而方向有無窮多個",
                          "the price is one question per direction, and there are infinitely many"))

 def _defn(self):
  cx, cy, s = -4.30, 0.32, 1.05
  g = VGroup(self._cross(cx, cy, 1.92, 0.72))
  xi = DIRS[2]
  base = _F(ALPHA)
  pts = []
  for k in range(61):
   t = -0.95 + 1.90 * k / 60
   q = _F((ALPHA[0] + t * xi[0], ALPHA[1] + t * xi[1]))
   pts.append([cx + s * (q[0] - base[0]), cy + s * (q[1] - base[1]), 0])
  g.add(self._curve(pts, ACCENT_B, sw=3), Dot([cx, cy, 0], radius=0.065, color=WARN))
  for t, col in ((0.85, DIM), (0.45, ACCENT_C)):
   q = _F((ALPHA[0] + t * xi[0], ALPHA[1] + t * xi[1]))
   g.add(Dot([cx + s * (q[0] - base[0]), cy + s * (q[1] - base[1]), 0], radius=0.055, color=col),
         Line([cx, cy, 0], [cx + s * (q[0] - base[0]), cy + s * (q[1] - base[1]), 0],
              color=col, stroke_width=2))
  d = _ap(JAC, xi)
  g.add(self._arr([cx, cy, 0], [cx + s * 1.15 * d[0], cy + s * 1.15 * d[1], 0],
                  ACCENT_A, sw=3, tl=0.14))
  g.add(self._panel(((0.86, "灰色與紫色是還沒取極限的割線",
                      "grey and purple are chords, before the limit", ACCENT_C),
                     (0.20, "t 越小，割線越靠近橘色那支",
                      "the smaller t is, the closer they come to the orange one", ACCENT_A),
                     (-0.46, "橘色就是 F 在 α 沿 ξ 的方向導數",
                      "orange is the derivative of F at alpha in the direction xi", WARN))))
  return g.add(self._foot("這個定義沒有用到微分，它自己就站得住",
                          "this definition never mentions the differential; it stands on its own",
                          ACCENT_A,
                          "所以方向導數可能全部存在，而微分卻不存在——最後三拍就在講這件事",
                          "so they can all exist while no differential does, which the last three beats are about"))

 def _misuse(self):
  dx, dy, ds = -5.15, 0.05, 0.52
  rx, ry, rs = -2.05, 0.05, 0.26
  g = VGroup(self._cross(dx, dy, 0.92, 0.90), self._cross(rx, ry, 1.95, 0.90),
             Text("ξ", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.82, 0.86, 0]),
             Text("D ξ F", font_size=FS_TAG - 2, color=DIM).move_to([rx - 1.55, 0.86, 0]))
  far = (SCALES[-1] * RAY[0], SCALES[-1] * RAY[1])
  g.add(self._arr([dx, dy, 0], [dx + ds * far[0], dy + ds * far[1], 0], DIM, sw=2, tl=0.10),
        self._arr([rx, ry, 0], [rx + rs * RAY_D[-1][0] + 0.10, ry + rs * RAY_D[-1][1], 0],
                  DIM, sw=2, tl=0.10))
  for c, d, col in zip(SCALES, RAY_D, (ACCENT_B, ACCENT_C, WARN)):
   g.add(Dot([dx + ds * c * RAY[0], dy + ds * c * RAY[1], 0], radius=0.06, color=col),
         Dot([rx + rs * d[0], ry + rs * d[1], 0], radius=0.06, color=col),
         Text(f"{c:.0f} ξ" if c > 1 else "ξ", font_size=FS_TAG - 5, color=col)
         .move_to([dx + ds * c * RAY[0], dy + ds * c * RAY[1] + 0.28, 0]),
         Text(f"{c:.0f} ×", font_size=FS_TAG - 5, color=col)
         .move_to([rx + rs * d[0], ry + rs * d[1] + 0.28, 0]))
  g.add(self._panel(((0.92, "三個 ξ 指的是同一個方向",
                      "the three vectors all point the same way", ACCENT_B),
                     (0.34, "可是三個導數差一個倍數",
                      "yet the three derivatives differ by a factor", WARN),
                     (-0.24, "所以真正成立的是「對 ξ 線性」",
                      "what actually holds is linearity in xi", ACCENT_A)),
                    x=3.90, w=4.60))
  return g.add(self._foot("書上特別點出這個字用得不精確，值得記一下",
                          "the book flags the imprecision of the word, and it is worth remembering",
                          ACCENT_A,
                          "習慣上還是照講「方向導數」，只要知道它依賴的是向量不是方向",
                          "the name is kept anyway; just remember it depends on the vector, not the direction"))

 def _thm72(self):
  dx, dy, ds = -5.15, 0.05, 0.70
  rx, ry, rs = -1.95, 0.05, 0.40
  g = VGroup(self._cross(dx, dy, 0.95, 0.90), self._cross(rx, ry, 1.55, 0.90),
             Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.86, 0.86, 0]),
             Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx - 1.45, 0.86, 0]))
  lam0 = _lam(0.0)
  g.add(self._curve([[dx + ds * (_lam(-0.9 + 1.8 * k / 60)[0] - lam0[0]),
                      dy + ds * (_lam(-0.9 + 1.8 * k / 60)[1] - lam0[1]), 0] for k in range(61)],
                    ACCENT_C, sw=3),
        Dot([dx, dy, 0], radius=0.065, color=WARN),
        self._arr([dx, dy, 0], [dx + ds * 0.85 * LAM_TAN[0], dy + ds * 0.85 * LAM_TAN[1], 0],
                  ACCENT_A, sw=2.5, tl=0.12))
  g0 = _F(lam0)
  g.add(self._curve([[rx + rs * (_F(_lam(-0.9 + 1.8 * k / 60))[0] - g0[0]),
                      ry + rs * (_F(_lam(-0.9 + 1.8 * k / 60))[1] - g0[1]), 0] for k in range(61)],
                    ACCENT_C, sw=3),
        Dot([rx, ry, 0], radius=0.065, color=WARN),
        self._arr([rx, ry, 0], [rx + rs * 0.85 * GAM_TAN[0], ry + rs * 0.85 * GAM_TAN[1], 0],
                  ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._arr([dx + 1.10, dy - 0.62, 0], [rx - 1.70, ry - 0.62, 0], ACCENT_B, sw=2, tl=0.10))
  g.add(self._panel(((0.92, "紫色是 V 裡一條彎的光滑弧",
                      "purple is a curved smooth arc in V", ACCENT_C),
                     (0.34, "它的像還是光滑弧",
                      "its image is a smooth arc again", ACCENT_B),
                     (-0.24, "而且切向量就是原來的切向量丟進微分",
                      "and its tangent vector is the original one fed into the differential", ACCENT_A)),
                    x=3.90, w=4.60),
        self._sym(-0.82, f"dF ₐ ( {LAM_TAN[0]:.0f} , {LAM_TAN[1]:.0f} )  =  "
                         f"( {GAM_TAN[0]:.0f} , {GAM_TAN[1]:.0f} )", ACCENT_A, FS_TAG - 1,
                  x=3.90, w=4.60))
  return g.add(self._foot("這只是鏈鎖規則換一個說法：合成的微分是微分的合成",
                          "this is the chain rule in different clothing: the composite's differential is the composite",
                          ACCENT_A,
                          "所以「沿弧走」與「沿直線走」得到的是同一套資訊",
                          "so travelling along an arc and along a line carry exactly the same information"))

 def _readoff(self):
  dx, dy, ds = -5.30, 0.05, 0.46
  rx, ry, rs = -2.30, 0.05, 0.34
  g = VGroup(self._cross(dx, dy, 0.85, 0.85), self._cross(rx, ry, 1.05, 0.85),
             Text("ξ", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.78, 0.82, 0]),
             Text("dF ₐ ( ξ )", font_size=FS_TAG - 2, color=DIM).move_to([rx - 0.60, 0.82, 0]))
  for xi, col in zip(DIRS, (ACCENT_B, ACCENT_C, WARN)):
   d = _ap(JAC, xi)
   g.add(self._arr([dx, dy, 0], [dx + ds * xi[0], dy + ds * xi[1], 0], col, sw=2.5, tl=0.12),
         self._arr([rx, ry, 0], [rx + rs * d[0], ry + rs * d[1], 0], col, sw=2.5, tl=0.12))
  gr, _ = self._numgrid(-0.60, 0.05, [[f"{x:.0f}" for x in r] for r in JAC], color=ACCENT_A)
  g.add(gr)
  g.add(self._panel(((0.86, "三個方向，三個方向導數",
                      "three directions, three directional derivatives", ACCENT_B),
                     (0.20, "每一個都等於微分作用在那個向量上",
                      "each equals the differential applied to that vector", ACCENT_A),
                     (-0.46, "把基底方向問一遍，矩陣就出來了",
                      "ask the basis directions and the matrix falls out", WARN))))
  return g.add(self._foot("實際計算微分時做的就是這件事：一個方向一個方向問",
                          "computing a differential in practice is exactly this: one direction at a time",
                          ACCENT_A,
                          "橘色那個矩陣的兩行，就是兩個基底方向的方向導數",
                          "the two columns of the orange matrix are the two basis directional derivatives"))

 def _homog(self):
  dx, dy, ds = -5.30, 0.05, 0.62
  ox, oy, sx, sy = -2.80, -0.42, 1.25, 0.42
  g = VGroup(self._cross(dx, dy, 0.90, 0.85))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g.add(Line([X(-0.15), Y(0), 0], [X(2.10), Y(0), 0], color=DIM, stroke_width=1.6),
        Line([X(0), Y(-1.00), 0], [X(0), Y(3.30), 0], color=DIM, stroke_width=1.6))
  for xi, val, col in zip(HOM_DIRS, HOM_VALS, (WARN, ACCENT_B, ACCENT_C)):
   n = max(abs(xi[0]), abs(xi[1]))
   g.add(self._arr([dx, dy, 0], [dx + ds * xi[0] / n, dy + ds * xi[1] / n, 0], col, sw=2.5, tl=0.12),
         Line([X(0), Y(0), 0], [X(1.9), Y(1.9 * val), 0], color=col, stroke_width=2.5))
  g.add(Dot([dx, dy, 0], radius=0.055, color=WARN))
  rows = [("  ξ            F ( ξ )", DIM)]
  for xi, val, col in zip(HOM_DIRS, HOM_VALS, (WARN, ACCENT_B, ACCENT_C)):
   rows.append((f"( {xi[0]:.0f} , {xi[1]:.0f} )          {val:.2f}", col))
  g.add(self._table(rows, x=4.05, w=4.30, y0=0.72, dy=0.42))
  return g.add(self._foot("把齊次函數限制到一條過原點的直線，得到的就是一條直線",
                          "restrict a homogeneous function to a line through the origin and a line comes back",
                          ACCENT_A,
                          "所以每個方向導數都存在，而且斜率正好是函數在 ξ 的值",
                          "so every directional derivative exists, its slope being the value at xi"))

 def _mustbelinear(self):
  g = VGroup()
  lines = (("D ξ F ( 0 )   =   F ( ξ )", ACCENT_B),
           ("D ξ F ( 0 )   =   dF ₀ ( ξ )", ACCENT_C),
           ("⇒     F   =   dF ₀     ∈   Hom ( V , W )", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.10))
  g.add(self._panel(((0.86, "上一拍：齊次就有每個方向導數",
                      "the last beat: homogeneous gives every directional derivative", ACCENT_B),
                     (0.20, "定理 7.2：可微就讓它等於微分",
                      "Theorem 7.2: differentiable makes it the differential", ACCENT_C),
                     (-0.46, "兩式一比，函數自己就是那個線性映射",
                      "compare the two and the function is that linear map", WARN))))
  return g.add(self._foot("所以「可微的齊次函數」這件事，其實就是「線性映射」",
                          "so a differentiable homogeneous function is nothing but a linear map",
                          ACCENT_A,
                          "反過來說，只要找一個非線性的齊次函數，就有反例",
                          "turn it around and any nonlinear homogeneous function is a counterexample"))

 def _counter(self):
  ox, oy, sx, sy = -5.55, 0.05, 0.72, 0.72
  X = lambda th: ox + th * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-0.20), Y(0), 0], [X(2 * math.pi + 0.20), Y(0), 0],
                  color=DIM, stroke_width=1.6),
             Line([ox, Y(-1.20), 0], [ox, Y(1.20), 0], color=DIM, stroke_width=1.6))
  # what the function does on the unit circle, against what a linear map would do
  g.add(self._curve([[X(2 * math.pi * k / 240),
                      Y(_H((math.cos(2 * math.pi * k / 240), math.sin(2 * math.pi * k / 240)))), 0]
                     for k in range(241)], ACCENT_B, sw=3, maxn=200),
        self._curve([[X(2 * math.pi * k / 240), Y(LIN_A * math.cos(2 * math.pi * k / 240)
                                                  + LIN_B * math.sin(2 * math.pi * k / 240)), 0]
                     for k in range(241)], WARN, sw=2.5, maxn=200))
  for th in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
   g.add(Dot([X(th), Y(_H((math.cos(th), math.sin(th)))), 0], radius=0.055, color=ACCENT_A))
  g.add(Dot([X(math.pi / 4), Y(_H((math.cos(math.pi / 4), math.sin(math.pi / 4)))), 0],
            radius=0.055, color=ACCENT_B),
        Dot([X(math.pi / 4), Y(LIN_A * math.cos(math.pi / 4) + LIN_B * math.sin(math.pi / 4)), 0],
            radius=0.055, color=WARN),
        self._dash([X(math.pi / 4), Y(_H((math.cos(math.pi / 4), math.sin(math.pi / 4)))), 0],
                   [X(math.pi / 4), Y(LIN_A * math.cos(math.pi / 4)
                                      + LIN_B * math.sin(math.pi / 4)), 0], ACCENT_C, n=4, sw=2))
  g.add(self._sym(0.86, f"F ( 1 , 0 )  +  F ( 0 , 1 )   =   {_H(ADD_A) + _H(ADD_B):.1f}",
                  WARN, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._sym(0.26, f"F ( 1 , 1 )   =   {_H(ADD_SUM):.1f}", ACCENT_B, FS_TAG - 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "紅色是「如果它線性」該長的樣子",
                  "red is what it would look like if it were linear", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.90, "四個橘點對得上，中間就對不上了",
                  "the four orange points agree and everything between does not", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("藍色是這個函數在單位圓上的值，紅色是同時通過那四點的線性函數",
                          "blue is the function on the unit circle, red the linear map through those four points",
                          ACCENT_A,
                          "有限維時只要方向導數對 α 連續就真的可微，但那要用均值定理，下一集講",
                          "continuity of the directional derivatives does rescue it, but that needs next time's theorem"))

 def stage(self):
  a, b, c = self._interval(), self._tangent(), self._skeleton()
  d, e, f = self._restrict(), self._defn(), self._misuse()
  h, i, j = self._thm72(), self._readoff(), self._homog()
  k, l = self._mustbelinear(), self._counter()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE39ZH, AdvCalcE39EN = make(AdvCalcE39Base, "39", prefix="AdvCalcE")
