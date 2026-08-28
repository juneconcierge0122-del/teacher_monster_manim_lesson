"""advcalc E43 -- chapter 3, section 9 (book pp. 156-159): the results of the
last two sections carried into real n-space, where a standard basis exists.
Theorem 9.1 lines up the partial derivative, the directional derivative along a
basis vector and the partial differential; Theorem 9.2 makes the n partial
derivatives the skeleton of the differential; Theorem 9.3 is Theorem 8.3
specialised; Theorem 9.4 identifies the Jacobian matrix entry by entry; the
chain rule becomes matrix multiplication; and the Jacobian determinant gets its
name.  Pages 159-160 are exercises 9.1 to 9.11; E44 opens section 10.

One map runs through the whole episode -- the one sending a plane vector to the
squares of its complex square -- because everything about it can be checked:
its Jacobian matrix at the sample point, that each column really is a
directional derivative along a basis vector, that a general directional
derivative is the weighted sum, that the two Jacobians multiply to the
composite's own, and that its determinant is four times the squared length at
every one of four sample points.
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
 return (x[0] ** 2 - x[1] ** 2, 2 * x[0] * x[1])


def _G(y):
 return (y[0] + y[1] ** 2, y[0] - y[1])


def _jac(f, a):
 cols = []
 for j in range(2):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  cols.append(tuple((u - v) / (2 * H) for u, v in zip(f(tuple(p)), f(tuple(m)))))
 return tuple(tuple(cols[j][i] for j in range(2)) for i in range(2))


def _mul(a, b):
 return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
              for i in range(2))


def _det(m):
 return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _round(m):
 return tuple(tuple(round(x) for x in r) for r in m)


APT = (1.0, 0.5)
BPT = _F(APT)
_JF, _JG = _jac(_F, APT), _jac(_G, BPT)
_JC = _jac(lambda x: _G(_F(x)), APT)
for _m in (_JF, _JG, _JC):
 assert all(abs(x - round(x)) < 1e-4 for r in _m for x in r), \
     "the beats print these matrices, so they should be whole numbers here"
JF, JG, JC = _round(_JF), _round(_JG), _round(_JC)
assert _mul(JG, JF) == JC, "the two Jacobians do not multiply to the composite's own"
assert JF != JG and JF != JC, "three identical matrices would make the beat unreadable"

# ── beat 1: each column is a directional derivative along a basis vector
BASIS = ((1.0, 0.0), (0.0, 1.0))
for _j, _d in enumerate(BASIS):
 _dd = tuple((u - v) / (2 * H) for u, v in
             zip(_F((APT[0] + H * _d[0], APT[1] + H * _d[1])),
                 _F((APT[0] - H * _d[0], APT[1] - H * _d[1]))))
 assert max(abs(a - JF[i][_j]) for i, a in enumerate(_dd)) < 1e-4, \
     "a column of the Jacobian is not the directional derivative it is drawn as"

# ── beat 4: a general direction is the weighted sum ────────────────────
YDIR = (2.0, -3.0)
DY = tuple((u - v) / (2 * H) for u, v in
           zip(_F((APT[0] + H * YDIR[0], APT[1] + H * YDIR[1])),
               _F((APT[0] - H * YDIR[0], APT[1] - H * YDIR[1]))))
SUMY = tuple(sum(YDIR[j] * JF[i][j] for j in range(2)) for i in range(2))
assert max(abs(a - b) for a, b in zip(DY, SUMY)) < 1e-4, \
    "the weighted sum of the partial derivatives is not the directional derivative"
assert all(abs(v - round(v)) < 1e-4 for v in SUMY), "the beat prints these"
SUMY = tuple(round(v) for v in SUMY)

# ── beat 10: the Jacobian determinant, at four sample points ───────────
DET_PTS = (APT, (1.0, 0.0), (0.5, -1.5), (2.0, 0.25))
DETS = [_det(_jac(_F, p)) for p in DET_PTS]
for _p, _d in zip(DET_PTS, DETS):
 assert abs(_d - 4 * (_p[0] ** 2 + _p[1] ** 2)) < 1e-4, \
     "the determinant is not four times the squared length after all"
assert len({round(d, 3) for d in DETS}) == 4, "four equal numbers would show nothing"

# the image of a small square really does grow by that factor
SQ_R = 0.10
_img = [_F((APT[0] + SQ_R * v[0], APT[1] + SQ_R * v[1]))
        for v in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
_area = abs(sum(_img[k][0] * _img[(k + 1) % 4][1] - _img[(k + 1) % 4][0] * _img[k][1]
                for k in range(4))) / 2
assert abs(_area / (2 * SQ_R) ** 2 - DETS[0]) < 0.1, \
    "the drawn square's image does not grow by the determinant"


class AdvCalcE43Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 43

 MODE_LABEL = {
  0: {"zh": "搬到實數的 n 維空間", "en": "moving into real n-space"},
  1: {"zh": "定理 9.1：三件事是同一件事", "en": "Theorem 9.1: three names, one thing"},
  2: {"zh": "一維的因子讓偏微分變成一個數", "en": "a one dimensional factor gives a number"},
  3: {"zh": "定理 9.2：偏導數就是骨架", "en": "Theorem 9.2: the partials are the skeleton"},
  4: {"zh": "任意方向：分量乘偏導數再求和", "en": "any direction: a weighted sum"},
  5: {"zh": "古典記號的一點怪處", "en": "a wrinkle in the classical notation"},
  6: {"zh": "定理 9.3：偏導數連續就夠了", "en": "Theorem 9.3: continuous partials suffice"},
  7: {"zh": "雅可比矩陣：每一行一個偏導數", "en": "the Jacobian matrix, a partial per column"},
  8: {"zh": "定理 9.4：矩陣元就是偏導數", "en": "Theorem 9.4: entry by entry"},
  9: {"zh": "鏈鎖規則就是矩陣相乘", "en": "the chain rule is matrix multiplication"},
  10: {"zh": "行列式：F 的雅可比", "en": "the determinant: the Jacobian of F"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _basis(self):
  cx, cy, s = -3.85, 0.05, 1.15
  g = VGroup(self._cross(cx, cy, 1.65, 0.95))
  for d, col, lab, ox, oy in ((BASIS[0], ACCENT_B, "δ ¹", 0.34, -0.26),
                              (BASIS[1], ACCENT_C, "δ ²", 0.36, -0.22)):
   g.add(self._arr([cx, cy, 0], [cx + s * d[0], cy + s * d[1], 0], col, sw=3, tl=0.14),
         self._sym(cy + s * d[1] + oy, lab, col, FS_TAG, x=cx + s * d[0] + ox, w=0.90))
  for k in range(-1, 2):
   for j in range(-1, 2):
    if k or j:
     g.add(Dot([cx + s * 0.5 * k, cy + s * 0.5 * j, 0], radius=0.035, color=DIM))
  g.add(self._panel(((0.86, "前兩節從頭到尾沒有用到座標",
                      "the last two sections never used coordinates", ACCENT_A),
                     (0.20, "這裡開始有標準基底",
                      "here a standard basis appears", ACCENT_B),
                     (-0.46, "於是「偏導數」才第一次真的出現",
                      "and only now does a partial derivative really turn up", ACCENT_C))))
  return g.add(self._foot("整章的定義都不需要座標，這一節是為了跟古典的寫法接上",
                          "the chapter's definitions need no coordinates; this section reconnects to the classical ones",
                          ACCENT_A,
                          "所以這一節沒有新的數學，只有翻譯——但翻譯本身值得做一次",
                          "so there is no new mathematics here, only translation, and it is worth doing once"))

 def _three(self):
  g = VGroup()
  spots = ((-4.95, 0.62, "∂ F / ∂ x ⱼ", ACCENT_B),
           (-1.95, 0.62, "D δ ʲ F", ACCENT_C),
           (-3.45, -0.42, "dF ʲ ₐ", WARN))
  for cx, cy, lab, col in spots:
   g.add(self._rect(cx, cy, 1.05, 0.30, col),
         self._sym(cy, lab, col, FS_TAG + 1, x=cx, w=1.90))
  g.add(self._arr([-3.85, 0.62, 0], [-3.05, 0.62, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.05, 0.50, 0], [-3.05, 0.50, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-4.60, 0.30, 0], [-3.90, -0.10, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.00, -0.10, 0], [-2.30, 0.30, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "老式的偏導數",
                      "the old fashioned partial derivative", ACCENT_B),
                     (0.20, "沿第 j 個基底向量的方向導數",
                      "the directional derivative along the jth basis vector", ACCENT_C),
                     (-0.46, "第 j 個偏微分",
                      "the jth partial differential", WARN))))
  return g.add(self._foot("三個之中只要有一個存在，另外兩個就都存在，而且互相決定",
                          "if any one of the three exists so do the others, and each determines the rest",
                          ACCENT_A,
                          "所以三種說法可以隨時互換，這是定理 9.1 的全部內容",
                          "so the three may be swapped freely, which is all Theorem 9.1 says"))

 def _onedim(self):
  ix, iy = -5.35, 0.05
  g = VGroup(Line([ix - 0.35, iy, 0], [ix + 1.15, iy, 0], color=DIM, stroke_width=2))
  for hh, col in ((0.45, ACCENT_B), (0.90, ACCENT_C)):
   g.add(Dot([ix + hh, iy, 0], radius=0.06, color=col))
  g.add(self._sym(iy - 0.34, "h", DIM, FS_TAG - 1, x=ix + 0.65, w=0.80))
  g.add(self._arr([ix + 1.40, iy, 0], [ix + 2.00, iy, 0], ACCENT_A, sw=2.5, tl=0.12))
  cx, cy, s = -1.85, 0.05, 0.95
  g.add(self._cross(cx, cy, 1.45, 0.90))
  base = (JF[0][0], JF[1][0])
  for hh, col in ((1.0, ACCENT_B), (2.0, ACCENT_C)):
   g.add(self._arr([cx, cy, 0], [cx + s * 0.42 * hh * base[0], cy + s * 0.42 * hh * base[1], 0],
                   col, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "第 j 個因子只有一維",
                      "the jth factor is one dimensional", ACCENT_B),
                     (0.20, "所以偏微分只能是「乘上一個向量」",
                      "so the partial differential can only multiply by a vector", ACCENT_C),
                     (-0.46, "那個向量就是偏導數",
                      "and that vector is the partial derivative", ACCENT_A))))
  return g.add(self._foot("這跟 E39 的定理 7.1 是同一句話：一維定義域讓微分退化成乘法",
                          "this is E39's Theorem 7.1 again: a one dimensional domain collapses a differential",
                          ACCENT_A,
                          "所以在座標下，偏微分與偏導數常常被當成同一個東西",
                          "which is why in coordinates the two are usually treated as one object"))

 def _skeleton(self):
  g = VGroup()
  for k, col in enumerate((ACCENT_B, ACCENT_C)):
   gr, _ = self._numgrid(-5.15 + k * 1.35, 0.30,
                         [[f"{JF[0][k]}"], [f"{JF[1][k]}"]], color=col, dx=0.50, dy=0.46)
   g.add(gr, self._sym(-0.60, f"∂ F / ∂ x {'₁' if k == 0 else '₂'}", col,
                       FS_TAG - 1, x=-5.15 + k * 1.35, w=1.30))
  g.add(self._arr([-3.10, 0.30, 0], [-2.55, 0.30, 0], ACCENT_A, sw=2.5, tl=0.12))
  gr, _ = self._numgrid(-1.65, 0.30, [[f"{x}" for x in r] for r in JF],
                        color=WARN, dx=0.62, dy=0.46)
  g.add(gr, self._sym(-0.60, "dF ₐ", WARN, FS_TAG, x=-1.65, w=1.30))
  g.add(self._panel(((0.86, "兩個偏導數各是一個向量",
                      "each partial derivative is a vector", ACCENT_B),
                     (0.20, "排成一組就是微分的骨架",
                      "gathered into a tuple they are the skeleton", ACCENT_C),
                     (-0.46, "骨架決定線性映射，所以微分就出來了",
                      "a skeleton determines a linear map, so the differential follows", WARN))))
  return g.add(self._foot("這是第 1 章那條「線性映射由基底上的值決定」在這裡的用法",
                          "this is chapter 1's rule that a linear map is fixed by its values on a basis",
                          ACCENT_A,
                          "所以算微分就是算 n 個偏導數，一次一個方向",
                          "so computing a differential means computing n partial derivatives, one direction each"))

 def _weighted(self):
  cx, cy, s = -4.30, 0.05, 0.55
  g = VGroup(self._cross(cx, cy, 1.55, 0.90))
  g.add(self._arr([cx, cy, 0], [cx + s * YDIR[0], cy + s * YDIR[1], 0], ACCENT_A, sw=3, tl=0.12),
        self._arr([cx, cy, 0], [cx + s * YDIR[0], cy, 0], ACCENT_B, sw=2, tl=0.10),
        self._arr([cx + s * YDIR[0], cy, 0], [cx + s * YDIR[0], cy + s * YDIR[1], 0],
                  ACCENT_C, sw=2, tl=0.10))
  g.add(self._sym(0.86, f"y   =   ( {YDIR[0]:.0f} , {YDIR[1]:.0f} )", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.26, f"{YDIR[0]:.0f} · ∂F/∂x ₁   +   ( {YDIR[1]:.0f} ) · ∂F/∂x ₂",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(-0.34, f"D y F ( a )   =   ( {SUMY[0]} , {SUMY[1]} )", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "這正是「梯度點乘方向」的來源",
                  "this is where the gradient dotted with a direction comes from",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("方向拆成兩個分量，各自乘上對應的偏導數再相加",
                          "split the direction into components, scale each by its partial, and add",
                          ACCENT_A,
                          "也因此變化最快的方向就是梯度自己的方向",
                          "and that is why the fastest change is along the gradient's own direction"))

 def _notation(self):
  g = VGroup()
  for cy, lab, col in ((0.55, "dF ₐ ( x )", WARN), (-0.20, "D ⱼ F ( a )", ACCENT_B)):
   g.add(self._rect(-3.75, cy, 1.15, 0.30, col),
         self._sym(cy, lab, col, FS_TAG + 2, x=-3.75, w=2.10))
  g.add(self._curve([[-2.25, 0.38, 0], [-1.85, 0.72, 0]], WARN, sw=3),
        self._curve([[-1.85, 0.38, 0], [-2.25, 0.72, 0]], WARN, sw=3))
  g.add(self._panel(((0.86, "上面那個裡的 x 同時是座標的名字",
                      "in the upper one, x is also the name of the coordinates", WARN),
                     (0.20, "所以讀起來會打架",
                      "so the two readings collide", ACCENT_C),
                     (-0.46, "下面那個把要固定的東西放進下標，精確得多",
                      "the lower one puts what is fixed into the subscript and is precise", ACCENT_B))))
  return g.add(self._foot("這是書上原話：古典的偏導數記號在這裡顯得野蠻",
                          "the book's own word for the classical notation here is barbarism",
                          ACCENT_A,
                          "記號之爭聽起來瑣碎，但寫多變數的鏈鎖規則時差別很大",
                          "a quarrel about notation sounds petty until the multivariable chain rule is written out"))

 def _thm93(self):
  g = VGroup()
  for cy, lab, col in ((0.55, "∂ F / ∂ x ⱼ   ∈   C ( A )", ACCENT_B),
                       (-0.35, "dF   ∈   C ( A )", WARN)):
   g.add(self._rect(-3.75, cy, 1.55, 0.30, col),
         self._sym(cy, lab, col, FS_TAG + 1, x=-3.75, w=2.90))
  g.add(self._arr([-3.75, 0.20, 0], [-3.75, -0.02, 0], ACCENT_A, sw=3, tl=0.12))
  g.add(self._sym(-1.00, "9.3    ⊂    8.3", DIM, FS_TAG, x=-3.75, w=2.40))
  g.add(self._panel(((0.86, "所有偏導數在開集上存在而且連續",
                      "every partial derivative exists and is continuous on the open set", ACCENT_B),
                     (0.20, "就推得出 F 在那裡連續可微",
                      "and F is continuously differentiable there", WARN),
                     (-0.46, "這是上一集定理 8.3 的特例",
                      "this is the previous episode's Theorem 8.3 specialised", ACCENT_A))))
  return g.add(self._foot("實際判斷可微時，用的幾乎都是這一條，不是定義",
                          "in practice this is the test used to decide differentiability, not the definition",
                          ACCENT_A,
                          "因為偏導數算得出來，而定義裡的小 o 不好直接檢查",
                          "because partial derivatives can be computed while a little oh cannot be checked directly"))

 def _jacobian(self):
  g = VGroup()
  gr, pos = self._numgrid(-3.95, 0.20, [[f"{x}" for x in r] for r in JF],
                          color=INK, dx=1.10, dy=0.58)
  g.add(gr)
  for j, col in enumerate((ACCENT_B, ACCENT_C)):
   x = pos(0, j)[0]
   g.add(self._curve([[x - 0.34, 0.60, 0], [x + 0.34, 0.60, 0], [x + 0.34, -0.20, 0],
                      [x - 0.34, -0.20, 0], [x - 0.34, 0.60, 0]], col, sw=2),
         self._sym(-0.62, f"∂ F / ∂ x {'₁' if j == 0 else '₂'}", col, FS_TAG - 2, x=x, w=1.00))
  g.add(self._panel(((0.86, "行對應輸入的變數",
                      "columns answer to the input variables", ACCENT_B),
                     (0.20, "列對應輸出的分量",
                      "rows answer to the output components", ACCENT_C),
                     (-0.46, "第 j 行就是第 j 個偏導數",
                      "the jth column is the jth partial derivative", ACCENT_A))))
  return g.add(self._foot("骨架是「行」不是「列」，這是最常記反的一件事",
                          "the skeleton lives in the columns, not the rows, and that is the easiest thing to get backwards",
                          ACCENT_A,
                          "記法：矩陣乘向量時，向量的第 j 個分量挑的就是第 j 行",
                          "a check: when a matrix meets a vector, the vector's jth entry picks the jth column"))

 def _entries(self):
  g = VGroup()
  gr, pos = self._numgrid(-4.20, 0.30, [[f"{x}" for x in r] for r in JF],
                          color=WARN, dx=0.85, dy=0.62)
  g.add(gr)
  labs = (("∂f ₁ /∂x ₁", "∂f ₁ /∂x ₂"), ("∂f ₂ /∂x ₁", "∂f ₂ /∂x ₂"))
  for i in range(2):
   for j in range(2):
    p = pos(i, j)
    g.add(self._sym(p[1] - 0.30, labs[i][j], DIM, FS_TAG - 5, x=p[0], w=0.90))
  g.add(self._panel(((0.86, "第 i 列第 j 行的元素",
                      "the entry in row i and column j", WARN),
                     (0.20, "就是第 i 個分量對第 j 個變數的偏導數",
                      "is the ith component differentiated by the jth variable", ACCENT_B),
                     (-0.46, f"畫面上這個點的矩陣是 {JF[0][0]} 、 {JF[0][1]} 、 {JF[1][0]} 、 {JF[1][1]}",
                      f"at this point the matrix reads {JF[0][0]}, {JF[0][1]}, {JF[1][0]}, {JF[1][1]}",
                      ACCENT_A))))
  return g.add(self._foot("這一條就是定理 9.4，也是所有實際計算的入口",
                          "that is Theorem 9.4, and it is the door every actual computation goes through",
                          ACCENT_A,
                          "矩陣是程式用中央差商算出來的，跟手算的公式核對過",
                          "the matrix was computed here by central differences and checked against the formula"))

 def _chain(self):
  g = VGroup()
  spots = ((-5.05, JF, ACCENT_B), (-2.95, JG, ACCENT_C), (-0.75, JC, WARN))
  for cx, m, col in spots:
   gr, _ = self._numgrid(cx, 0.36, [[f"{x}" for x in r] for r in m], color=col,
                         dx=0.62, dy=0.48)
   g.add(gr)
  g.add(self._sym(0.36, "·", DIM, FS_TAG + 4, x=-4.00, w=0.50),
        self._sym(0.36, "=", DIM, FS_TAG + 4, x=-1.85, w=0.50))
  g.add(self._sym(-0.52, "J F", ACCENT_B, FS_TAG - 1, x=-5.05, w=1.10),
        self._sym(-0.52, "J G", ACCENT_C, FS_TAG - 1, x=-2.95, w=1.10),
        self._sym(-0.52, "J ( G ∘ F )", WARN, FS_TAG - 1, x=-0.75, w=1.90))
  g.add(self._panel(((0.86, "左邊是兩個雅可比矩陣相乘",
                      "on the left, the two Jacobians multiplied", ACCENT_C),
                     (0.20, "右邊是直接對合成算出來的",
                      "on the right, the composite differentiated directly", WARN),
                     (-0.46, "兩邊一模一樣，這就是那條連鎖公式",
                      "the two agree, and that is the chain rule formula", ACCENT_A))))
  return g.add(self._foot("順序不能反：外函數的雅可比在左邊，內函數的在右邊",
                          "the order matters: the outer map's Jacobian goes on the left",
                          ACCENT_A,
                          "課本裡那條有兩個求和記號的公式，就只是這件事寫成分量",
                          "the textbook formula with its two summation signs is just this, written in components"))

 def _det(self):
  cx, cy, s = -4.60, 0.10, 0.85
  g = VGroup(self._cross(cx, cy, 1.15, 0.85))
  sq = [[cx + s * SQ_R * 4 * v[0], cy + s * SQ_R * 4 * v[1], 0]
        for v in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
  g.add(self._curve(sq + [sq[0]], ACCENT_B, sw=2.5))
  img = [[cx + s * (JF[0][0] * SQ_R * 4 * v[0] + JF[0][1] * SQ_R * 4 * v[1]),
          cy + s * (JF[1][0] * SQ_R * 4 * v[0] + JF[1][1] * SQ_R * 4 * v[1]), 0]
         for v in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
  g.add(self._curve(img + [img[0]], WARN, sw=3))
  rows = [("       x            det J F        4 ‖ x ‖ ²", DIM)]
  for p, d in zip(DET_PTS, DETS):
   rows.append((f"( {p[0]:4.1f} , {p[1]:5.2f} )      {d:7.2f}      {4 * (p[0] ** 2 + p[1] ** 2):7.2f}",
                (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[len(rows) % 4]))
  g.add(self._table(rows, x=3.90, w=4.60, y0=0.70, dy=0.40, size=FS_TAG - 3))
  return g.add(self._foot("藍色小方塊的像是紅色的平行四邊形，面積放大了行列式那麼多倍",
                          "the blue square's image is the red parallelogram, its area grown by the determinant",
                          ACCENT_A,
                          "雅可比不為零，後面會是反函數定理的關鍵。下一集講初等應用",
                          "a nonzero Jacobian is later the key to the inverse function theorem; next, applications"))

 def stage(self):
  a, b, c = self._basis(), self._three(), self._onedim()
  d, e, f = self._skeleton(), self._weighted(), self._notation()
  h, i, j = self._thm93(), self._jacobian(), self._entries()
  k, l = self._chain(), self._det()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE43ZH, AdvCalcE43EN = make(AdvCalcE43Base, "43", prefix="AdvCalcE")
