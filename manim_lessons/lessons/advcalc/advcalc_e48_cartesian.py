"""advcalc E48 -- chapter 3, section 11, third part (book pp. 167-169): the
Cartesian forms of the two theorems.  Theorem 11.4 states the inverse mapping
theorem in terms of an n by n Jacobian determinant, Theorem 11.5 states the
implicit function theorem with the determinant taken only over the variables
being solved for, and both are shown on examples whose explicit solution would
need a polynomial of degree nine and degree six respectively.  That ends
chapter 3; pages 169-171 are exercises 11.1 to 11.29.

Both examples are chosen here rather than taken from the book, and both are
solved numerically as an independent check: the local inverse is found by
Newton iteration and its Jacobian compared with the inverse of the original's,
and the implicit function is solved the same way and its Jacobian compared with
the formula of Theorem 11.1.  The point of both beats is that a solution
provably exists while no formula for it does, so the numerical solution is the
only honest way to put one on screen.
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


def _jac(f, a):
 cols = []
 for j in range(2):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  cols.append(tuple((u - v) / (2 * H) for u, v in zip(f(tuple(p)), f(tuple(m)))))
 return tuple(tuple(cols[j][i] for j in range(2)) for i in range(2))


def _det(m):
 return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _inv(m):
 d = _det(m)
 return ((m[1][1] / d, -m[0][1] / d), (-m[1][0] / d, m[0][0] / d))


# ── beats 3 to 5: Theorem 11.4 on a map with no usable inverse formula ──
def _Gn(y):
 return (y[0] ** 3 + y[1], y[0] + y[1] ** 3)


BPT = (1.0, 1.0)
APT = _Gn(BPT)
JG = tuple(tuple(round(x) for x in r) for r in _jac(_Gn, BPT))
DETG = _det(JG)
assert APT == (2.0, 2.0) and JG == ((3, 1), (1, 3)) and DETG == 8, \
    "the numbers the beats print have moved"


def _newton(target, guess=BPT):
 x = list(guess)
 for _ in range(80):
  f = (_Gn(tuple(x))[0] - target[0], _Gn(tuple(x))[1] - target[1])
  j = _jac(_Gn, tuple(x))
  d = _det(j)
  x = [x[0] - (j[1][1] * f[0] - j[0][1] * f[1]) / d,
       x[1] - (-j[1][0] * f[0] + j[0][0] * f[1]) / d]
 return tuple(x)


assert max(abs(a - b) for a, b in zip(_newton(APT), BPT)) < 1e-9, \
    "the local inverse does not return the point it started from"
SAMPLES = ((2.10, 1.95), (1.85, 2.15))
for _t in SAMPLES:
 _y = _newton(_t)
 assert max(abs(a - b) for a, b in zip(_Gn(_y), _t)) < 1e-9, \
     "the local inverse does not actually invert"
JINV = tuple(tuple(round(x, 3) for x in r) for r in _inv(JG))
_JF = _jac(_newton, APT)
assert max(abs(a - b) for r, q in zip(_JF, JINV) for a, b in zip(r, q)) < 1e-4, \
    "the local inverse's Jacobian is not the inverse of the original's"


# Beat 5 prints the equation left after eliminating y2, and a first draft of it
# had the two coordinates crossed over. That version happens to vanish at the
# sample point as well, so only a second point catches it: check three.
def _eliminated(x, y1):
 """(x1 - y1^3)^3 + y1 - x2, the beat-5 equation, as written on the screen."""
 return (x[0] - y1 ** 3) ** 3 + y1 - x[1]


for _b in ((1.0, 1.0), (1.1, 0.9), (0.7, 1.3)):
 assert abs(_eliminated(_Gn(_b), _b[0])) < 1e-9, "the printed elimination is not the right one"


# ── beats 8 to 10: Theorem 11.5 on two equations in four variables ─────
def _G1(x, y):
 return x[0] ** 2 + y[0] * y[1] - 3.0


def _G2(x, y):
 return x[1] + y[0] ** 5 - y[1]


X0, Y0 = (1.0, 1.0), (1.0, 2.0)
assert abs(_G1(X0, Y0)) < 1e-12 and abs(_G2(X0, Y0)) < 1e-12, \
    "the sample point does not satisfy the two equations"

DGY = tuple(tuple(round((g(X0, (Y0[0] + H * (j == 0), Y0[1] + H * (j == 1)))
                         - g(X0, (Y0[0] - H * (j == 0), Y0[1] - H * (j == 1)))) / (2 * H))
                  for j in range(2)) for g in (_G1, _G2))
DGX = tuple(tuple(round((g((X0[0] + H * (j == 0), X0[1] + H * (j == 1)), Y0)
                         - g((X0[0] - H * (j == 0), X0[1] - H * (j == 1)), Y0)) / (2 * H))
                  for j in range(2)) for g in (_G1, _G2))
DETY = _det(DGY)
assert DGY == ((2, 1), (5, -1)) and DETY == -7, "the printed determinant has moved"
_iy = _inv(DGY)
DFI = tuple(tuple(-sum(_iy[i][k] * DGX[k][j] for k in range(2)) for j in range(2))
            for i in range(2))


def _solve_y(x, guess=Y0):
 y = list(guess)
 for _ in range(120):
  f = (_G1(x, tuple(y)), _G2(x, tuple(y)))
  j = tuple(tuple((g(x, (y[0] + H * (k == 0), y[1] + H * (k == 1)))
                   - g(x, (y[0] - H * (k == 0), y[1] - H * (k == 1)))) / (2 * H)
                  for k in range(2)) for g in (_G1, _G2))
  d = _det(j)
  y = [y[0] - (j[1][1] * f[0] - j[0][1] * f[1]) / d,
       y[1] - (-j[1][0] * f[0] + j[0][0] * f[1]) / d]
 return tuple(y)


assert max(abs(a - b) for a, b in zip(_solve_y(X0), Y0)) < 1e-9, \
    "the numerical implicit function misses the point it should pass through"
_JN = _jac(_solve_y, X0)
assert max(abs(a - b) for r, q in zip(_JN, DFI) for a, b in zip(r, q)) < 1e-4, \
    "Theorem 11.1's formula disagrees with the implicit function solved numerically"


class AdvCalcE48Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 48

 MODE_LABEL = {
  0: {"zh": "翻成座標的語言", "en": "translated into coordinates"},
  1: {"zh": "定理 11.4 的條件", "en": "the condition in Theorem 11.4"},
  2: {"zh": "結論：唯一的一組解", "en": "the conclusion: a unique tuple"},
  3: {"zh": "例子：行列式是 8", "en": "an example: the determinant is eight"},
  4: {"zh": "反函數真的找得出來", "en": "the inverse really can be found"},
  5: {"zh": "可是寫不出公式", "en": "but no formula can be written"},
  6: {"zh": "定理 11.5：n + m 個變數", "en": "Theorem 11.5: n plus m variables"},
  7: {"zh": "行列式只對被解的變數取", "en": "the determinant covers only the solved variables"},
  8: {"zh": "例子：行列式是 −7", "en": "an example: the determinant is minus seven"},
  9: {"zh": "消元之後是六次方程", "en": "eliminating leaves degree six"},
  10: {"zh": "微分還是算得出來", "en": "the differential is still computable"},
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

 def _cross(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _translate(self):
  g = VGroup()
  for cy, lab, col in ((0.52, "V ,  W ,  X", ACCENT_B), (-0.36, "ℝ ⁿ ,  ℝ ᵐ", WARN)):
   g.add(self._rect(-4.55, cy, 1.25, 0.32, col),
         self._sym(cy, lab, col, FS_TAG + 2, x=-4.55, w=2.30))
  g.add(self._arr([-4.55, 0.16, 0], [-4.55, -0.02, 0], ACCENT_A, sw=3, tl=0.12))
  g.add(self._sym(0.52, "dF ,  dG", ACCENT_B, FS_TAG, x=-1.85, w=2.20),
        self._sym(-0.36, "∂ ( … ) / ∂ ( … )", WARN, FS_TAG, x=-1.85, w=2.60))
  g.add(self._panel(((0.86, "上面是前兩集的說法，乾淨",
                      "the upper row is the last two episodes: clean", ACCENT_B),
                     (0.20, "下面是實際會看到的樣子",
                      "the lower row is what one actually meets", WARN),
                     (-0.46, "內容一樣，只是換一種寫法",
                      "the content is identical; only the notation changes", ACCENT_A))))
  return g.add(self._foot("這一集沒有新的數學，是把兩條定理翻成座標的語言",
                          "there is no new mathematics here; the two theorems are put into coordinates",
                          ACCENT_A,
                          "多變數微積分課本裡看到的就是下面那一列",
                          "the lower row is the version any multivariable calculus text prints"))

 def _condition(self):
  g = VGroup()
  g.add(self._rect(-3.55, 0.42, 2.65, 0.34, WARN),
        self._sym(0.42, "∂ ( G ₁ , … , G ₙ ) / ∂ ( y ₁ , … , y ₙ )  ≠  0",
                  WARN, FS_TAG, x=-3.55, w=5.10))
  gr, _ = self._numgrid(-3.55, -0.52, [["∂G ₁ /∂y ₁", "∂G ₁ /∂y ₂"],
                                       ["∂G ₂ /∂y ₁", "∂G ₂ /∂y ₂"]],
                        color=ACCENT_B, dx=1.55, dy=0.48, size=FS_TAG - 5)
  g.add(gr)
  g.add(self._panel(((0.86, "n 個函數、n 個變數",
                      "n functions of n variables", ACCENT_B),
                     (0.20, "全部連續可微",
                      "all continuously differentiable", ACCENT_C),
                     (-0.46, "唯一的條件是行列式不為零",
                      "the only condition is that the determinant does not vanish", WARN))))
  return g.add(self._foot("行列式不為零，等價於那個雅可比矩陣可逆，也就是微分可逆",
                          "a nonvanishing determinant is the Jacobian matrix inverting, hence the differential",
                          ACCENT_A,
                          "所以這只是上一集那個假設換成座標的說法",
                          "so this is the previous episode's hypothesis restated in coordinates"))

 def _conclusion(self):
  g = VGroup()
  lines = (("∃ !   F   =   ⟨ F ₁ , … , F ₙ ⟩", ACCENT_B),
           ("F   ∈   C ¹ ( M )", ACCENT_C),
           ("G ( F ( x ) )   =   x                x ∈ M", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "唯一一組實值函數",
                      "a unique tuple of real valued functions", ACCENT_B),
                     (0.20, "每一個都連續可微",
                      "each of them continuously differentiable", ACCENT_C),
                     (-0.46, "代回去恰好還原成原來的變數",
                      "substituting back returns the original variables", WARN))))
  return g.add(self._foot("「唯一」仍然是局部的：只在那顆球 M 上唯一",
                          "unique is still local: unique on the ball M and nowhere claimed beyond it",
                          ACCENT_A,
                          "而 F ( a ) = b 這一條是自動附帶的，不必另外要求",
                          "and F of a equalling b comes along automatically, without being asked for"))

 def _det8(self):
  g = VGroup()
  g.add(self._sym(0.86, "G ( y )  =  ⟨ y ₁ ³ + y ₂ ,   y ₁ + y ₂ ³ ⟩", ACCENT_B,
                  FS_TAG + 1, x=-3.55, w=5.20))
  gr, _ = self._numgrid(-4.35, 0.02, [[f"{x}" for x in r] for r in JG],
                        color=ACCENT_C, dx=0.68, dy=0.50)
  g.add(gr, self._sym(-0.62, "dG ᵦ", ACCENT_C, FS_TAG, x=-4.35, w=1.40))
  g.add(self._sym(0.02, f"det   =   {DETG}", WARN, FS_TAG + 2, x=-2.15, w=2.20),
        self._sym(-0.62, f"b  =  ⟨ 1 , 1 ⟩       a  =  ⟨ {APT[0]:.0f} , {APT[1]:.0f} ⟩",
                  ACCENT_A, FS_TAG - 1, x=-2.05, w=2.80))
  g.add(self._panel(((0.86, "兩個三次的方程",
                      "two cubic equations", ACCENT_B),
                     (0.20, "在 1 與 1 那一點的雅可比矩陣",
                      "the Jacobian matrix at the point one and one", ACCENT_C),
                     (-0.46, "行列式是 8，不等於零",
                      "its determinant is eight, which is not zero", WARN))))
  return g.add(self._foot("所以定理適用：像 2 與 2 附近有唯一的局部反函數",
                          "so the theorem applies: a unique local inverse exists near the image",
                          ACCENT_A,
                          "矩陣是程式用中央差商算的，行列式也是",
                          "the matrix was computed here by central differences, and so was the determinant"))

 def _found(self):
  # The first version set the two coordinate crosses side by side with nothing
  # between them -- one smeared plane on the probe frame -- and computed the
  # connecting arrow from the wrong pair of centres, so it came out a tenth of a
  # unit long and vanished. Frame each plane and drive the arrow off the frames.
  cy, s, hw, hh = 0.30, 1.05, 0.80, 0.58
  ax, bx = -5.15, -1.95
  g = VGroup()
  for ox in (ax, bx):
   g.add(self._rect(ox, cy, hw + 0.20, hh + 0.18, DIM, sw=1.2),
         self._cross(ox, cy, hw, hh))
  for t, col in zip(SAMPLES, (ACCENT_B, ACCENT_C)):
   y = _newton(t)
   g.add(Dot([ax + s * (t[0] - APT[0]) * 3, cy + s * (t[1] - APT[1]) * 3, 0],
             radius=0.065, color=col),
         Dot([bx + s * (y[0] - BPT[0]) * 3, cy + s * (y[1] - BPT[1]) * 3, 0],
             radius=0.065, color=col))
  g.add(Dot([ax, cy, 0], radius=0.055, color=WARN), Dot([bx, cy, 0], radius=0.055, color=WARN))
  g.add(self._arr([ax + hw + 0.32, cy, 0], [bx - hw - 0.32, cy, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(cy + 0.34, "F", ACCENT_A, FS_TAG, x=(ax + bx) / 2, w=0.70))
  g.add(self._sym(cy - hh - 0.34, "x", DIM, FS_TAG - 1, x=ax, w=1.20),
        self._sym(cy - hh - 0.34, "F ( x )", WARN, FS_TAG - 1, x=bx, w=1.60))
  rows = [("       x                    F ( x )", DIM)]
  for t in SAMPLES:
   y = _newton(t)
   rows.append((f"( {t[0]:.2f} , {t[1]:.2f} )      ( {y[0]:.4f} , {y[1]:.4f} )", ACCENT_B))
  g.add(self._table(rows, y0=0.72, dy=0.44))
  g.add(self._mid(-0.74, "代回去確實還原成 x", "substituting back really does return x",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("局部反函數是用牛頓法一步一步逼出來的，不是解出來的",
                          "the local inverse was iterated to by Newton's method, not solved for",
                          ACCENT_A,
                          "而它的雅可比矩陣算出來正好是原矩陣的反矩陣",
                          "and its Jacobian matrix comes out as the inverse of the original's"))

 def _noformula(self):
  g = VGroup()
  g.add(self._rect(-3.55, 0.48, 2.65, 0.34, WARN),
        self._sym(0.48, "( x ₁ − y ₁ ³ ) ³   +   y ₁   −   x ₂   =   0",
                  WARN, FS_TAG + 1, x=-3.55, w=5.10))
  g.add(self._sym(-0.30, "y ₁ ⁹   +   …   =   0", ACCENT_C, FS_TAG + 2, x=-3.55, w=4.20))
  g.add(self._panel(((0.86, "想寫成公式，就得消元",
                      "writing a formula means eliminating a variable", ACCENT_B),
                     (0.20, "消完是一個九次方程",
                      "what is left has degree nine", ACCENT_C),
                     (-0.46, "一般沒有根式解",
                      "with no solution by radicals in general", WARN))))
  return g.add(self._foot("這正是定理的價值：它保證解存在而且連續可微",
                          "this is exactly the value of the theorem: it promises a smooth solution exists",
                          ACCENT_A,
                          "卻完全不告訴你怎麼把它寫出來——第 4 章會給逼近的辦法",
                          "without saying how to write it; chapter four supplies a way to approximate it"))

 def _thm115(self):
  g = VGroup()
  g.add(self._rect(-4.55, 0.42, 1.15, 0.32, ACCENT_B),
        self._sym(0.42, "x ₁ , … , x ₙ", ACCENT_B, FS_TAG, x=-4.55, w=2.10),
        self._rect(-1.95, 0.42, 1.15, 0.32, WARN),
        self._sym(0.42, "y ₁ , … , y ₘ", WARN, FS_TAG, x=-1.95, w=2.10))
  g.add(self._sym(-0.36, "G ᵢ ( x , y )  =  0            i = 1 , … , m", ACCENT_C,
                  FS_TAG + 1, x=-3.25, w=5.00))
  g.add(self._panel(((0.86, "藍色那些是自由變數",
                      "the blue ones are the free variables", ACCENT_B),
                     (0.20, "紅色那些是要解出來的",
                      "the red ones are to be solved for", WARN),
                     (-0.46, "m 個方程，剛好配 m 個未知數",
                      "m equations matching m unknowns", ACCENT_C))))
  return g.add(self._foot("結論是那 m 個變數可以寫成前面 n 個的連續可微函數",
                          "the conclusion is that those m become continuously differentiable functions of the n",
                          ACCENT_A,
                          "方程的個數必須等於要解出來的變數個數，否則行列式不是方陣",
                          "the counts must match, or the determinant would not be of a square matrix"))

 def _whichvars(self):
  g = VGroup()
  gr, pos = self._numgrid(-4.05, 0.28,
                          [["∂G ₁ /∂x ₁", "∂G ₁ /∂x ₂", "∂G ₁ /∂y ₁", "∂G ₁ /∂y ₂"],
                           ["∂G ₂ /∂x ₁", "∂G ₂ /∂x ₂", "∂G ₂ /∂y ₁", "∂G ₂ /∂y ₂"]],
                          color=DIM, dx=1.10, dy=0.52, size=FS_TAG - 7)
  g.add(gr)
  # A red box around the y block clipped the last column's labels, which are
  # wider than the column spacing, and its right edge landed on the matrix's own
  # closing bracket. An underbrace marks the same two columns and cannot clip.
  x0, x1 = pos(0, 2)[0], pos(0, 3)[0]
  ux0, ux1, uy = x0 - 0.48, x1 + 0.46, -0.34
  g.add(self._curve([[ux0, uy + 0.12, 0], [ux0, uy, 0], [ux1, uy, 0], [ux1, uy + 0.12, 0]],
                    WARN, sw=2.5))
  g.add(self._sym(-0.52, "只 對 y 取", WARN, FS_TAG, x=(x0 + x1) / 2, w=2.20)
        if False else self._mid(-0.52, "只對 y 那一組取", "taken over the y block only",
                                WARN, FS_TAG, x=(x0 + x1) / 2, w=2.40))
  g.add(self._panel(((0.86, "整個雅可比矩陣有 n 加 m 行",
                      "the full Jacobian has n plus m columns", DIM),
                     (0.20, "行列式只取紅線標住的那兩行",
                      "the determinant is taken over the marked columns only", WARN),
                     (-0.46, "這是最容易記錯的一點",
                      "this is the easiest thing to get wrong", ACCENT_A))))
  return g.add(self._foot("取全部變數的話矩陣根本不是方陣，行列式無從談起",
                          "over all the variables the matrix is not square and has no determinant at all",
                          ACCENT_A,
                          "紅線標住的是 m 乘 m 的，剛好對應 m 個要解出來的變數",
                          "the marked block is m by m, matching the m variables being solved for"))

 def _example115(self):
  g = VGroup()
  for k, lab in enumerate(("x ₁ ²  +  y ₁ y ₂  −  3   =   0",
                           "x ₂  +  y ₁ ⁵  −  y ₂   =   0")):
   g.add(self._rect(-3.85, 0.80 - k * 0.56, 2.15, 0.26, (ACCENT_B, ACCENT_C)[k]),
         self._sym(0.80 - k * 0.56, lab, (ACCENT_B, ACCENT_C)[k], FS_TAG, x=-3.85, w=4.10))
  # the matrix used to sit high enough that its bracket ran into the lower box
  gr, _ = self._numgrid(-4.75, -0.58, [[f"{x}" for x in r] for r in DGY],
                        color=WARN, dx=0.68, dy=0.46)
  g.add(gr, self._sym(-0.58, f"det   =   {DETY}".replace("-", "−"), WARN, FS_TAG + 1, x=-2.55, w=2.40))
  g.add(self._panel(((0.86, "兩個方程、四個變數",
                      "two equations in four variables", ACCENT_B),
                     (0.20, "在指定的那一點兩式都成立",
                      "both hold at the chosen point", ACCENT_C),
                     (-0.46, "對兩個 y 取的行列式是 −7",
                      "the determinant over the two y variables is minus seven", WARN))))
  return g.add(self._foot("兩個矩陣元都是程式用中央差商算的，行列式也是",
                          "both matrix entries were computed here by central differences, as was the determinant",
                          ACCENT_A,
                          "不等於零，所以定理適用：y 可以寫成 x 的函數",
                          "it does not vanish, so the theorem applies and y becomes a function of x"))

 def _degree6(self):
  g = VGroup()
  lines = (("y ₂   =   x ₂  +  y ₁ ⁵", ACCENT_C),
           ("x ₁ ²  +  y ₁ ( x ₂ + y ₁ ⁵ )  −  3   =   0", ACCENT_B),
           ("y ₁ ⁶   +   x ₂ y ₁   +   x ₁ ²  −  3   =   0", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "第二式解出 y 二",
                      "solve the second equation for the second y", ACCENT_C),
                     (0.20, "代進第一式",
                      "substitute into the first", ACCENT_B),
                     (-0.46, "得到一個六次方程",
                      "and a polynomial of degree six is left", WARN))))
  return g.add(self._foot("六次一般解不出來，可是定理已經保證解存在、唯一，而且連續可微",
                          "degree six has no general solution, yet the theorem already promises a smooth unique one",
                          ACCENT_A,
                          "這一集兩個例子都是這樣挑的：存在性有保證，公式沒有",
                          "both examples were chosen this way: existence guaranteed, formula unavailable"))

 def _differential(self):
  g = VGroup()
  for cx, m, col, lab in ((-5.15, DGX, ACCENT_B, "dG ¹"), (-3.15, DGY, ACCENT_C, "dG ²")):
   gr, _ = self._numgrid(cx, 0.40, [[f"{x}" for x in r] for r in m], color=col,
                         dx=0.68, dy=0.46)
   g.add(gr, self._sym(-0.36, lab, col, FS_TAG, x=cx, w=1.40))
  body = [[f"{x:.3f}" for x in r] for r in DFI]
  gr, _ = self._numgrid(-0.75, 0.40, body, color=WARN, dx=1.05, dy=0.46)
  g.add(gr, self._sym(-0.36, "dF ₐ", WARN, FS_TAG, x=-0.75, w=1.40))
  g.add(self._sym(0.40, "→", DIM, FS_TAG + 2, x=-2.00, w=0.60))
  g.add(self._panel(((0.86, "用上一集那條公式算出來",
                      "computed by the previous episode's formula", ACCENT_B),
                     (0.20, "跟數值解出來的隱函數的雅可比完全相同",
                      "identical to the Jacobian of the numerically solved implicit function", WARN),
                     (-0.46, "所以公式寫不出來，微分還是算得出來",
                      "so no formula exists and the differential is still computable", ACCENT_A))))
  return g.add(self._foot("這就是整節的重點：存在性、唯一性、可微性，全部不必解出來就有",
                          "that is the section's point: existence, uniqueness and differentiability without solving",
                          ACCENT_A,
                          "第 3 章第 11 節到此結束，下一集講第 12 節的子流形與 Lagrange 乘子",
                          "that ends section eleven; next come submanifolds and Lagrange multipliers"))

 def stage(self):
  a, b, c = self._translate(), self._condition(), self._conclusion()
  d, e, f = self._det8(), self._found(), self._noformula()
  h, i, j = self._thm115(), self._whichvars(), self._example115()
  k, l = self._degree6(), self._differential()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE48ZH, AdvCalcE48EN = make(AdvCalcE48Base, "48", prefix="AdvCalcE")
