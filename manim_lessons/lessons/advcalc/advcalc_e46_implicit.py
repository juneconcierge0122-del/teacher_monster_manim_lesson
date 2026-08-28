"""advcalc E46 -- chapter 3, section 11, first part (book pp. 164-166): the
observation that the Jacobian chain formula and the differential chain rule are
the same statement with numbers replaced by linear maps, the differential of an
inverse map as a composition inverse, the classical implicit differentiation,
its general form, and Theorem 11.1, which says that an implicit function that
exists and is continuous is differentiable, with a formula matching the
elementary one.  E47 takes the existence theorems from page 166; pages 169-171
are exercises 11.1 to 11.29.

Three examples are computed rather than quoted.  A map with a closed-form
inverse has both Jacobians evaluated and multiplied, to check they give the
identity.  The circle gives the scalar implicit derivative, checked against the
quotient of the two partial derivatives.  And a genuinely vector-valued
implicit equation has its two partial differentials evaluated, the formula of
Theorem 11.1 applied, and the result checked against the Jacobian of the
implicit function solved for explicitly.
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


def _jac(f, a, n=2):
 cols = []
 for j in range(2):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  cols.append(tuple((u - v) / (2 * H) for u, v in zip(f(tuple(p)), f(tuple(m)))))
 return tuple(tuple(cols[j][i] for j in range(2)) for i in range(n))


def _mul(a, b):
 return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
              for i in range(2))


def _round(m):
 return tuple(tuple(round(x, 6) for x in r) for r in m)


# ── beat 2: an inverse map, and the two Jacobians ──────────────────────
def _Fi(x):
 return (x[0] + x[1] ** 2, x[1])


def _Gi(y):
 return (y[0] - y[1] ** 2, y[1])


AI = (1.0, 2.0)
BI = _Fi(AI)
JFI, JGI = _round(_jac(_Fi, AI)), _round(_jac(_Gi, BI))
PROD = _round(_mul(JGI, JFI))
for _p in ((0.7, -1.3), (-2.0, 0.5)):
 assert max(abs(a - b) for a, b in zip(_Gi(_Fi(_p)), _p)) < 1e-12, "these two are not inverse"
assert PROD == ((1.0, 0.0), (0.0, 1.0)), "the two Jacobians do not multiply to the identity"
JFI = tuple(tuple(round(x) for x in r) for r in JFI)
JGI = tuple(tuple(round(x) for x in r) for r in JGI)


# ── beats 3 and 4: the scalar implicit function ────────────────────────
RAD = 5.0


def _g(x, y):
 return x * x + y * y - RAD * RAD


SA, SB = 3.0, 4.0
assert abs(_g(SA, SB)) < 1e-12, "the sample point is not on the circle"
GX = (_g(SA + H, SB) - _g(SA - H, SB)) / (2 * H)
GY = (_g(SA, SB + H) - _g(SA, SB - H)) / (2 * H)
SLOPE = -GX / GY
_f = lambda x: math.sqrt(RAD * RAD - x * x)
assert abs((_f(SA + H) - _f(SA - H)) / (2 * H) - SLOPE) < 1e-5, \
    "the implicit formula disagrees with the explicit derivative"
assert abs(SLOPE + 0.75) < 1e-9, "the beat prints minus three quarters"


# ── beats 5 to 9: the vector implicit function ─────────────────────────
def _G(xi, eta):
 return (eta[0] + xi[0] * eta[1] - 3.0, eta[1] ** 2 + xi[1] - 5.0)


XI, ETA = (1.0, 1.0), (1.0, 2.0)
assert max(abs(v) for v in _G(XI, ETA)) < 1e-12, "the sample point does not satisfy G = 0"

DG1 = _round(tuple(tuple((_G((XI[0] + H * (j == 0), XI[1] + H * (j == 1)), ETA)[i]
                          - _G((XI[0] - H * (j == 0), XI[1] - H * (j == 1)), ETA)[i]) / (2 * H)
                         for j in range(2)) for i in range(2)))
DG2 = _round(tuple(tuple((_G(XI, (ETA[0] + H * (j == 0), ETA[1] + H * (j == 1)))[i]
                          - _G(XI, (ETA[0] - H * (j == 0), ETA[1] - H * (j == 1)))[i]) / (2 * H)
                         for j in range(2)) for i in range(2)))
DET2 = DG2[0][0] * DG2[1][1] - DG2[0][1] * DG2[1][0]
assert abs(DET2) > 1e-9, "the second partial differential has to be invertible"
INV2 = ((DG2[1][1] / DET2, -DG2[0][1] / DET2), (-DG2[1][0] / DET2, DG2[0][0] / DET2))
PRED = tuple(tuple(-sum(INV2[i][k] * DG1[k][j] for k in range(2)) for j in range(2))
             for i in range(2))


def _Fexp(xi):
 """The same implicit function solved for explicitly, as an independent check."""
 r = math.sqrt(5.0 - xi[1])
 return (3.0 - xi[0] * r, r)


assert max(abs(a - b) for a, b in zip(_Fexp(XI), ETA)) < 1e-9, "the explicit solution misses the point"
JEXP = _jac(_Fexp, XI)
assert max(abs(a - b) for r, q in zip(PRED, JEXP) for a, b in zip(r, q)) < 1e-4, \
    "Theorem 11.1's formula disagrees with the explicit implicit function"
DG1 = tuple(tuple(round(x) for x in r) for r in DG1)
DG2 = tuple(tuple(round(x) for x in r) for r in DG2)
PRED = tuple(tuple(round(x, 2) for x in r) for r in PRED)
assert PRED == ((-2.0, 0.25), (-0.0, -0.25)) or PRED == ((-2.0, 0.25), (0.0, -0.25)), PRED
PRED = ((-2.0, 0.25), (0.0, -0.25))


class AdvCalcE46Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 46

 MODE_LABEL = {
  0: {"zh": "兩條公式長得一模一樣", "en": "two formulas, one shape"},
  1: {"zh": "數 → 矩陣 → 線性映射", "en": "number, matrix, linear map"},
  2: {"zh": "反映射：倒數換成合成反元素", "en": "an inverse: reciprocal becomes composition inverse"},
  3: {"zh": "隱函數：把恆等式微分", "en": "implicit: differentiate the identity"},
  4: {"zh": "古典的那條式子", "en": "the classical formula"},
  5: {"zh": "一般情形一字不改", "en": "the general case, word for word"},
  6: {"zh": "解出 dF", "en": "solving for dF"},
  7: {"zh": "定理 11.1", "en": "Theorem 11.1"},
  8: {"zh": "證明：把 η 也當成未知數", "en": "the proof: eta is an unknown too"},
  9: {"zh": "一個向量的例子，核對過", "en": "a vector example, checked"},
  10: {"zh": "存在性還沒證", "en": "existence is still open"},
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

 # ── beats ─────────────────────────────────────────────────────────
 def _twoformulas(self):
  g = VGroup()
  for cy, lab, col in ((0.58, "∂ z ₖ / ∂ x ⱼ   =   Σ  ( ∂ z ₖ / ∂ y ᵢ ) ( ∂ y ᵢ / ∂ x ⱼ )", ACCENT_B),
                       (-0.30, "d ( G ∘ F ) ₐ   =   dG ᵦ  ∘  dF ₐ", ACCENT_C)):
   g.add(self._rect(-3.55, cy, 2.55, 0.32, col),
         self._sym(cy, lab, col, FS_TAG, x=-3.55, w=4.90))
  g.add(self._panel(((0.86, "上面那條：數字相乘、相加",
                      "the upper one multiplies and adds numbers", ACCENT_B),
                     (0.20, "下面那條：線性映射合成、相加",
                      "the lower one composes and adds linear maps", ACCENT_C),
                     (-0.46, "除此之外，兩條完全一樣",
                      "beyond that, the two are the same statement", ACCENT_A))))
  return g.add(self._foot("整個微分學都是這樣走的：把「數」換成「線性映射」，公式原樣成立",
                          "the whole subject goes this way: replace numbers by linear maps and the formulas stand",
                          ACCENT_A,
                          "這一節就是把這個對應用在反函數與隱函數上",
                          "this section applies that correspondence to inverse and implicit functions"))

 def _threelevels(self):
  g = VGroup()
  spots = ((-5.05, "dim V = 1", "· c", ACCENT_B),
           (-2.95, "V = ℝ ⁿ", "[ t ᵢ ⱼ ]", ACCENT_C),
           (-0.85, "V", "∘", WARN))
  for cx, top, bot, col in spots:
   g.add(self._rect(cx, 0.32, 0.92, 0.62, col),
         self._sym(0.56, top, col, FS_TAG - 1, x=cx, w=1.70),
         self._sym(0.06, bot, col, FS_TAG + 2, x=cx, w=1.70))
  for cx in (-4.00, -1.90):
   g.add(self._arr([cx - 0.16, 0.32, 0], [cx + 0.16, 0.32, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "一維：微分就是乘上一個數",
                      "one dimension: multiply by a number", ACCENT_B),
                     (0.20, "座標下：那些數排成矩陣",
                      "in coordinates: those numbers form a matrix", ACCENT_C),
                     (-0.46, "一般情形：乘法換成合成",
                      "in general: multiplication becomes composition", WARN))))
  return g.add(self._foot("三個欄位講的是同一件事，只是把它寫在三種不同的語言裡",
                          "the three columns say one thing in three different languages",
                          ACCENT_A,
                          "所以一元微積分裡的每一條公式，都值得問「一般版本長什麼樣」",
                          "so every formula of one variable calculus is worth asking the general form of"))

 def _inverse(self):
  g = VGroup()
  for cx, m, col, lab in ((-5.05, JFI, ACCENT_B, "dF ₐ"), (-2.95, JGI, ACCENT_C, "dG ᵦ"),
                          (-0.85, ((1, 0), (0, 1)), WARN, "I")):
   gr, _ = self._numgrid(cx, 0.36, [[f"{x:.0f}" for x in r] for r in m], color=col,
                         dx=0.66, dy=0.50)
   g.add(gr, self._sym(-0.52, lab, col, FS_TAG, x=cx, w=1.50))
  g.add(self._sym(0.36, "·", DIM, FS_TAG + 4, x=-4.00, w=0.50),
        self._sym(0.36, "=", DIM, FS_TAG + 4, x=-1.90, w=0.50))
  g.add(self._panel(((0.86, "一元：反函數的導數是導數的倒數",
                      "one variable: the derivative of an inverse is the reciprocal", ACCENT_B),
                     (0.20, "一般：反映射的微分是微分的合成反元素",
                      "in general: the differential of an inverse is the composition inverse", ACCENT_C),
                     (-0.46, "兩個雅可比矩陣乘起來，剛好是單位矩陣",
                      "the two Jacobians multiply to the identity", WARN))))
  return g.add(self._foot("這個映射有封閉形式的反元素，所以兩邊都算得出來核對",
                          "this map has a closed form inverse, so both sides can be evaluated and compared",
                          ACCENT_A,
                          "但「反映射存在」本身還沒證——那是下一集的事",
                          "that an inverse exists at all is not yet proved; that is next time"))

 def _identity(self):
  cx, cy, s = -3.95, -0.05, 0.20
  g = VGroup(self._cross(cx, cy, 1.45, 1.05))
  g.add(self._curve([[cx + s * RAD * math.cos(2 * math.pi * k / 96),
                      cy + s * RAD * math.sin(2 * math.pi * k / 96), 0] for k in range(97)],
                    ACCENT_C, sw=2.5))
  g.add(Dot([cx + s * SA, cy + s * SB, 0], radius=0.07, color=WARN),
        self._dash([cx + s * SA, cy, 0], [cx + s * SA, cy + s * SB, 0], DIM, n=6, sw=1.4),
        self._dash([cx, cy + s * SB, 0], [cx + s * SA, cy + s * SB, 0], DIM, n=6, sw=1.4))
  g.add(self._panel(((0.86, "方程把 y 定成 x 的函數",
                      "the equation defines y as a function of x", ACCENT_C),
                     (0.20, "在那一點附近，上半圓就是那個函數",
                      "near that point the upper semicircle is the function", WARN),
                     (-0.46, "把恆等式對 x 微分，就是古典的做法",
                      "differentiating the identity is the classical move", ACCENT_A))))
  return g.add(self._foot("重點是「不必解出來」——只要知道解存在，就可以對恆等式微分",
                          "the point is that it need not be solved: the identity can be differentiated as it stands",
                          ACCENT_A,
                          "這個例子解得出來，正好可以拿來核對答案",
                          "this example can be solved, which makes it useful for checking the answer"))

 def _classical(self):
  cx, cy, s = -3.95, -0.05, 0.20
  g = VGroup(self._cross(cx, cy, 1.45, 1.05))
  g.add(self._curve([[cx + s * RAD * math.cos(2 * math.pi * k / 96),
                      cy + s * RAD * math.sin(2 * math.pi * k / 96), 0] for k in range(97)],
                    DIM, sw=1.6))
  px, py = cx + s * SA, cy + s * SB
  g.add(Dot([px, py, 0], radius=0.07, color=WARN),
        Line([px - s * 2.6, py - s * 2.6 * SLOPE, 0], [px + s * 2.6, py + s * 2.6 * SLOPE, 0],
             color=ACCENT_A, stroke_width=3))
  g.add(self._sym(0.86, "∂g/∂x   +   ( ∂g/∂y ) · f ′ ( a )   =   0", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.26, f"f ′ ( a )   =   −  {GX:.0f} / {GY:.0f}   =   − 3 / 4", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "解出來的是斜率，不是函數",
                  "what is solved for is the slope, not the function", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.90, "橘色那條切線的斜率就是它",
                  "the orange tangent line has exactly that slope", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("兩個偏導數是程式算的，而顯式解的導數也算過，兩邊相同",
                          "both partial derivatives were computed here, as was the explicit derivative, and they agree",
                          ACCENT_A,
                          "分母不能是零——這就是後面「第二個偏微分要可逆」的一維版本",
                          "the denominator must not vanish, which is the one dimensional form of invertibility"))

 def _general(self):
  g = VGroup()
  lines = (("G ( ξ , F ( ξ ) )   ≡   0", ACCENT_B),
           ("G  ∘  ⟨ I , F ⟩   ≡   0", ACCENT_C),
           ("dG ¹  ∘  I    +    dG ²  ∘  dF ₐ    =    0", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "恆等式寫成一個合成",
                      "write the identity as a composite", ACCENT_C),
                     (0.20, "用上一集那條一般鏈鎖規則微分",
                      "differentiate with the general chain rule", ACCENT_B),
                     (-0.46, "兩個偏微分各配一支內函數",
                      "each partial differential meets one inner map", WARN))))
  return g.add(self._foot("內函數是恆等映射與 F 這一對，所以第一項的微分就是恆等映射",
                          "the inner map is the pair of the identity and F, so the first term keeps the identity",
                          ACCENT_A,
                          "這一步完全是機械的，沒有任何技巧",
                          "this step is entirely mechanical and uses no trick"))

 def _solve(self):
  g = VGroup()
  lines = (("dG ²  ∘  dF ₐ    =    −  dG ¹", ACCENT_B),
           ("dF ₐ    =    −  ( dG ² ) ⁻¹  ∘  dG ¹", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._rect(-3.55, 0.55 - k * 0.80, 2.35, 0.32, col),
         self._sym(0.55 - k * 0.80, lab, col, FS_TAG + 1, x=-3.55, w=4.50))
  # this grey line used to sit at -0.72, close enough to the box above it that
  # the box's lower border read as an underline on the text
  g.add(self._sym(-0.88, "f ′ ( a )   =   −  ( ∂g/∂y ) ⁻¹ ( ∂g/∂x )", DIM,
                  FS_TAG, x=-3.55, w=4.50))
  g.add(self._panel(((0.86, "只要第二個偏微分可逆",
                      "provided the second partial differential is invertible", ACCENT_B),
                     (0.20, "就解得出 dF",
                      "dF can be solved for", WARN),
                     (-0.46, "跟一元那條式子形式完全相同",
                      "the form matches the one variable formula exactly", ACCENT_A))))
  return g.add(self._foot("除法換成合成反元素，順序因此變得要緊：反元素在左邊",
                          "division becomes composition inverse, so order now matters: the inverse goes on the left",
                          ACCENT_A,
                          "灰色那一行是一維的樣子，把它跟上面那行對照著看",
                          "the grey line is the one dimensional shape, worth reading against the one above"))

 def _thm111(self):
  g = VGroup()
  # three hypothesis boxes stacked; the middle one carries a word, so it is
  # bilingual while the other two are symbols
  g.add(self._rect(-4.85, 0.66, 1.45, 0.30, ACCENT_B),
        self._sym(0.66, "G ( ξ , F ( ξ ) )  ≡  0", ACCENT_B, FS_TAG, x=-4.85, w=2.70),
        self._rect(-4.85, -0.06, 1.45, 0.30, ACCENT_C),
        self._mid(-0.06, "F 連續", "F is continuous", ACCENT_C, FS_TAG, x=-4.85, w=2.70),
        self._rect(-4.85, -0.78, 1.45, 0.30, WARN),
        self._sym(-0.78, "( dG ² ) ⁻¹   ∃", WARN, FS_TAG, x=-4.85, w=2.70))
  g.add(self._rect(-1.65, -0.06, 1.35, 0.30, ACCENT_A),
        self._sym(-0.06, "dF ₐ   ∃", ACCENT_A, FS_TAG, x=-1.65, w=2.50))
  g.add(self._arr([-3.30, -0.06, 0], [-2.90, -0.06, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._panel(((0.86, "三個假設：恆等式、連續、第二個偏微分可逆",
                      "three hypotheses: the identity, continuity, invertibility", ACCENT_B),
                     (0.20, "結論：那個隱函數在該點可微",
                      "the conclusion: the implicit function is differentiable there", ACCENT_A),
                     (-0.46, "而且微分就是上一拍那條式子",
                      "and its differential is the formula from the last beat", WARN))))
  return g.add(self._foot("注意「F 存在」是假設而不是結論——這條定理不製造隱函數",
                          "note that F existing is a hypothesis and not a conclusion: this theorem makes nothing",
                          ACCENT_A,
                          "它說的是：如果隱函數存在而且連續，那它一定可微，而且長那個樣子",
                          "it says that if one exists and is continuous, it must be differentiable and look like that"))

 def _proof(self):
  g = VGroup()
  lines = (("0   =   ΔG ( ξ , η )   =   dG ¹ ( ξ )  +  dG ² ( η )  +  o", ACCENT_B),
           ("η   =   O ( ξ )   +   o ( ⟨ ξ , η ⟩ )", ACCENT_C),
           ("η  =  S ( ξ )  +  o ( ξ )              S  ∈  Hom ( V , W )", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG, x=-3.55, w=5.30))
  g.add(self._panel(((0.86, "把 η 當成未知數，先解出來",
                      "treat eta as an unknown and solve for it", ACCENT_B),
                     (0.20, "F 連續，所以 η 是一個無窮小",
                      "F is continuous, so eta is an infinitesimal", ACCENT_C),
                     (-0.46, "引理 5.1 把它升級成大 O，式子就收乾淨了",
                      "Lemma 5.1 upgrades it to big oh and the expression closes", WARN))))
  return g.add(self._foot("這是 E37 那一集唯一一條當時看起來沒用的引理，在這裡派上用場",
                          "this is the one lemma of E37 that looked idle at the time, and here it earns its place",
                          ACCENT_A,
                          "沒有連續性這個假設，就沒辦法起步——所以它是必要的",
                          "without the continuity hypothesis there is no way to start, so it is not decorative"))

 def _example(self):
  g = VGroup()
  for cx, m, col, lab in ((-5.15, DG1, ACCENT_B, "dG ¹"), (-3.15, DG2, ACCENT_C, "dG ²"),
                          (-0.95, PRED, WARN, "dF ₐ")):
   body = [[f"{x:.0f}" if abs(x - round(x)) < 1e-9 else f"{x:.2f}" for x in r] for r in m]
   gr, _ = self._numgrid(cx, 0.36, body, color=col, dx=0.78, dy=0.50)
   g.add(gr, self._sym(-0.48, lab, col, FS_TAG, x=cx, w=1.60))
  g.add(self._sym(0.36, "→", DIM, FS_TAG + 2, x=-2.05, w=0.60))
  g.add(self._panel(((0.86, "兩個偏微分都是程式算的",
                      "both partial differentials were computed here", ACCENT_B),
                     (0.20, "第二個的行列式是 4，可逆",
                      "the second has determinant four, so it inverts", ACCENT_C),
                     (-0.46, "右邊是公式算出來的 dF",
                      "on the right is dF from the formula", WARN))))
  return g.add(self._foot("這個例子解得出顯式解，程式把它的雅可比也算了一次，兩邊完全相同",
                          "this example can be solved explicitly, and its Jacobian was computed too: they agree",
                          ACCENT_A,
                          "所以那條公式不是宣告的，是驗過的",
                          "so the formula is verified here rather than announced"))

 def _existence(self):
  g = VGroup()
  g.add(self._rect(-4.75, 0.42, 1.55, 0.32, ACCENT_B),
        self._sym(0.42, "dF ₐ   ∃", ACCENT_B, FS_TAG + 1, x=-4.75, w=2.90),
        self._rect(-4.75, -0.42, 1.55, 0.32, WARN),
        self._sym(-0.42, "F   ∃", WARN, FS_TAG + 1, x=-4.75, w=2.90))
  # both arrows point from the statement to the chapter that settles it; the
  # lower one is crossed because this chapter does not settle it
  g.add(self._arr([-3.05, 0.42, 0], [-2.35, 0.42, 0], ACCENT_A, sw=3, tl=0.14),
        self._dash([-3.05, -0.42, 0], [-2.35, -0.42, 0], DIM, n=6, sw=2.5),
        self._curve([[-2.82, -0.60, 0], [-2.58, -0.24, 0]], WARN, sw=3),
        self._curve([[-2.58, -0.60, 0], [-2.82, -0.24, 0]], WARN, sw=3))
  g.add(self._sym(0.42, "Ch 3", ACCENT_A, FS_TAG, x=-1.75, w=1.30),
        self._sym(-0.42, "Ch 4", DIM, FS_TAG, x=-1.75, w=1.30))
  g.add(self._panel(((0.86, "這一集證的是上面那個箭頭",
                      "this episode proves the upper arrow", ACCENT_B),
                     (0.20, "存在性是下面那個，還沒證",
                      "existence is the lower one, and is not yet proved", WARN),
                     (-0.46, "它要用第 4 章的不動點定理",
                      "it needs the fixed point theorem of chapter four", DIM))))
  return g.add(self._foot("下一集講定理 11.2 與它的特例——反映射定理",
                          "next time: Theorem 11.2 and its special case, the inverse mapping theorem",
                          ACCENT_A,
                          "書上把存在性的證明推遲到下一章，這裡照樣把界線畫清楚",
                          "the book postpones the existence proof to the next chapter, and the line is drawn here"))

 def stage(self):
  a, b, c = self._twoformulas(), self._threelevels(), self._inverse()
  d, e, f = self._identity(), self._classical(), self._general()
  h, i, j = self._solve(), self._thm111(), self._proof()
  k, l = self._example(), self._existence()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE46ZH, AdvCalcE46EN = make(AdvCalcE46Base, "46", prefix="AdvCalcE")
