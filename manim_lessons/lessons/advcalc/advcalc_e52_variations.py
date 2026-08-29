"""advcalc E52 -- chapter 3, section 15 (book pp. 182-185): the calculus of
variations.  A variational problem is a critical-point problem whose domain is
an infinite-dimensional space of arcs; the constraint of fixed endpoints is a
closed plane, so the condition is only that the differential vanish on the
subspace it translates.  Theorem 14.3 of the previous episode makes the
functional differentiable, its differential is the first variation, and the
lemma of Du Bois-Reymond turns the vanishing of that into the Euler equation.
Section 15 has no exercises; section 16 starts on page 186.  Sections 12 to 15
have no exercises at all, which happens nowhere else in this book.

The central formula is checked rather than asserted.  The first variation is
computed two ways at an arc that is deliberately NOT a critical point -- once as
a difference quotient of the functional along h, once as the integral the
theorem gives -- and the two agree to six places while being far from zero, so
the check is not passing for the trivial reason.  The shortest-path example then
has its Euler residual computed along the straight line and along a perturbed
arc, and four perturbed arcs are measured to be longer.
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
H = 1e-6

TA, TB = 0.0, 1.0
YA, YB = 0.0, 2.0


def _simpson(f, n=4000, a=TA, b=TB):
 h = (b - a) / n
 s = f(a) + f(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * f(a + k * h)
 return s * h / 3.0


def _Fint(x, y, t):
 """The integrand of arc length: it does not depend on x or on t."""
 return math.sqrt(1.0 + y * y)


def _dFdx(x, y, t):
 return (_Fint(x + H, y, t) - _Fint(x - H, y, t)) / (2 * H)


def _dFdy(x, y, t):
 return (_Fint(x, y + H, t) - _Fint(x, y - H, t)) / (2 * H)


def _line(t):
 return YA + (YB - YA) * (t - TA) / (TB - TA)


def _bump(eps):
 return lambda t: _line(t) + eps * math.sin(math.pi * t)


def _deriv(f, t):
 return (f(t + H) - f(t - H)) / (2 * H)


def _G(f):
 return _simpson(lambda t: _Fint(f(t), _deriv(f, t), t))


STRAIGHT = math.hypot(TB - TA, YB - YA)
assert abs(_G(_line) - STRAIGHT) < 1e-7, "the straight arc's length is not the distance"

EPS_LIST = (0.30, 0.15, -0.15, -0.30)
LENS = [(e, _G(_bump(e))) for e in EPS_LIST]
for _e, _L in LENS:
 assert _L > STRAIGHT + 1e-4, "a perturbed arc came out no longer than the straight one"


# ── the first variation, computed two ways at a NON-critical arc ───────
def _h(t):
 return math.sin(math.pi * t)


BASE = _bump(0.30)
STEP = 1e-5
VAR_QUOT = (_G(lambda t: BASE(t) + STEP * _h(t))
            - _G(lambda t: BASE(t) - STEP * _h(t))) / (2 * STEP)
VAR_FORM = _simpson(lambda t: (_dFdx(BASE(t), _deriv(BASE, t), t) * _h(t)
                               + _dFdy(BASE(t), _deriv(BASE, t), t) * _deriv(_h, t)))
assert abs(VAR_QUOT - VAR_FORM) < 1e-5, "the first variation formula disagrees with the functional"
assert abs(VAR_QUOT) > 0.1, \
    "the check has to run at an arc that is not critical, or both sides are zero for free"

# and at the straight arc the same two numbers are zero, which is the point
CRIT_QUOT = (_G(lambda t: _line(t) + STEP * _h(t))
             - _G(lambda t: _line(t) - STEP * _h(t))) / (2 * STEP)
assert abs(CRIT_QUOT) < 1e-6, "the straight arc must be a critical point"


# ── Du Bois-Reymond: the partial in y is constant exactly on the solution
def _py(f, t):
 return _dFdy(f(t), _deriv(f, t), t)


TS = [TA + (TB - TA) * k / 200 for k in range(201)]
SPREAD_LINE = max(_py(_line, t) for t in TS) - min(_py(_line, t) for t in TS)
SPREAD_BUMP = max(_py(BASE, t) for t in TS) - min(_py(BASE, t) for t in TS)
PY_CONST = _py(_line, 0.5)
assert SPREAD_LINE < 1e-6 < 0.05 < SPREAD_BUMP, \
    "the partial in y has to be constant on the solution and not on anything else"
assert abs(PY_CONST - (YB - YA) / STRAIGHT) < 1e-6


# ── the Euler residual ─────────────────────────────────────────────────
def _residual(f, t):
 d = (_py(f, t + 1e-4) - _py(f, t - 1e-4)) / 2e-4
 return d - _dFdx(f(t), _deriv(f, t), t)


RES_LINE = max(abs(_residual(_line, t)) for t in TS[20:-20])
RES_BUMP = max(abs(_residual(BASE, t)) for t in TS[20:-20])
assert RES_LINE < 1e-4 < 0.1 < RES_BUMP, \
    "the Euler residual must vanish on the solution and not on the perturbed arc"


class AdvCalcE52Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 52

 MODE_LABEL = {
  0: {"zh": "臨界點問題，只是定義域無窮維", "en": "a critical-point problem, in infinite dimensions"},
  1: {"zh": "約束是一個閉平面", "en": "the constraint is a closed plane"},
  2: {"zh": "弧的空間", "en": "the space of arcs"},
  3: {"zh": "泛函為什麼可微", "en": "why the functional is differentiable"},
  4: {"zh": "第一變分", "en": "the first variation"},
  5: {"zh": "兩端釘住的那些 h", "en": "the h that are pinned at both ends"},
  6: {"zh": "分部積分，端點項消掉", "en": "integrate by parts and the endpoint term goes"},
  7: {"zh": "只受一個限制，所以只能是常數", "en": "one constraint only, so it is constant"},
  8: {"zh": "Euler 方程", "en": "the Euler equation"},
  9: {"zh": "例子：兩點之間最短的路", "en": "an example: the shortest path"},
  10: {"zh": "端點不固定時多兩個條件", "en": "free endpoints add two conditions"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 # a common frame for the arc pictures: t across, the value up
 AX, AY, SX, SY = -5.85, -0.62, 3.90, 0.62

 def _arcaxes(self, col=DIM):
  return VGroup(Line([self.AX - 0.12, self.AY, 0], [self.AX + self.SX + 0.18, self.AY, 0],
                     color=col, stroke_width=1.4),
                Line([self.AX, self.AY - 0.12, 0], [self.AX, self.AY + 2.4 * self.SY, 0],
                     color=col, stroke_width=1.4))

 def _arc(self, f, col, sw=2.4, n=90):
  return self._curve([[self.AX + self.SX * k / n,
                       self.AY + self.SY * f(TA + (TB - TA) * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 def _ends(self, col=WARN):
  return VGroup(Dot([self.AX, self.AY + self.SY * YA, 0], radius=0.07, color=col),
                Dot([self.AX + self.SX, self.AY + self.SY * YB, 0], radius=0.07, color=col))

 # ── beats ─────────────────────────────────────────────────────────
 def _problem(self):
  g = VGroup(self._arcaxes())
  # these arcs are illustrative, so they may be bigger than the ones beat 9
  # actually measures; at the measured size the three read as one thick line
  for e, col in ((0.0, WARN), (0.60, ACCENT_B), (-0.60, ACCENT_C)):
   g.add(self._arc(_bump(e) if e else _line, col, sw=2.4 if e else 3.0))
  g.add(self._ends())
  g.add(self._panel(((0.86, "兩個端點固定，中間的弧任意",
                      "the two endpoints are fixed and the arc between them is free", WARN),
                     (0.20, "要讓那個積分取到極值",
                      "and the integral is to be made extreme", ACCENT_B),
                     (-0.46, "這就是一個臨界點問題，只是定義域是無窮維的",
                      "that is a critical-point problem, in infinite dimensions", ACCENT_A))))
  return g.add(self._foot("書上的說法很直接：變分問題就是臨界點問題，只是用「微分等於零」的方式帶了一個轉折",
                          "the book is blunt: these are critical-point problems, with one twist in how the differential is used",
                          ACCENT_A,
                          "未知的不是一個數，也不是 ℝⁿ 裡的一點，而是一整條弧",
                          "the unknown is neither a number nor a point of real n-space but a whole arc"))

 def _plane(self):
  cx, cy = -4.15, 0.05
  g = VGroup(Line([cx - 1.55, cy - 0.55, 0], [cx + 1.55, cy - 0.05, 0], color=DIM, stroke_width=2),
             Line([cx - 1.55, cy + 0.35, 0], [cx + 1.55, cy + 0.85, 0], color=WARN, stroke_width=2.5))
  g.add(self._arr([cx - 0.35, cy - 0.23, 0], [cx - 0.35, cy + 0.57, 0], ACCENT_A, sw=2.2, tl=0.10),
        self._sym(cy - 0.85, "M", DIM, FS_TAG, x=cx - 1.05, w=0.80),
        self._sym(cy + 1.06, "S  =  M  +  α", WARN, FS_TAG, x=cx + 0.85, w=1.90),
        self._sym(cy + 0.18, "α", ACCENT_A, FS_TAG, x=cx - 0.05, w=0.60))
  g.add(self._panel(((0.86, "約束集合是一個閉平面",
                      "the constraint set is a closed plane", WARN),
                     (0.20, "它是某個子空間平移過去的",
                      "which is a subspace translated", DIM),
                     (-0.46, "所以條件只是「微分在那個子空間上等於零」",
                      "so the condition is just that the differential vanish on it", ACCENT_A))))
  return g.add(self._foot("有約束的極值一般要一個更廣的乘子定理，可是平面這個情形不必——限制上去就是子空間上的函數",
                          "a constrained maximum generally wants a multiplier theorem; for a plane it does not, being a function on the subspace",
                          ACCENT_A,
                          "這就是 E49 那條定理 12.2 在這裡不必登場的原因",
                          "that is why E49's Theorem 12.2 does not have to appear here"))

 def _space(self):
  g = VGroup(self._arcaxes())
  for e, col in ((0.0, DIM), (0.70, ACCENT_B), (-0.50, ACCENT_C), (0.30, WARN)):
   g.add(self._arc(_bump(e) if e else _line, col, sw=2.0))
  g.add(self._ends(ACCENT_A))
  g.add(self._sym(0.86, "V  =  C ¹ ( [ a , b ] , W )", ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.24, "‖ f ‖   =   ‖ f ‖ ∞   +   ‖ f ′ ‖ ∞", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "每一條弧是這個空間裡的一個點",
                  "each arc is one point of this space", ACCENT_C, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "範數把函數與導數都算進去",
                  "the norm counts both the arc and its derivative", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("導數也要算進範數，因為被積函數裡有導數——不然那個泛函根本不連續",
                          "the derivative belongs in the norm because the integrand contains it; otherwise the functional is not even continuous",
                          ACCENT_A,
                          "這個空間是無窮維的，可是前面三章的定理沒有一條用到有限維",
                          "the space is infinite dimensional, and nothing in the last three chapters needed finite dimensions"))

 def _differentiable(self):
  g = VGroup()
  boxes = ((-4.90, "⟨ f , g ⟩  ↦  F ( f , g , · )", ACCENT_B),
           (-1.85, "u  ↦  ∫ ₐ ᵇ  u", WARN))
  for cx, lab, col in boxes:
   g.add(self._rect(cx, 0.52, 1.25, 0.32, col),
         self._sym(0.52, lab, col, FS_TAG, x=cx, w=2.35))
  g.add(self._arr([-3.50, 0.52, 0], [-3.25, 0.52, 0], ACCENT_A, sw=2.5, tl=0.10))
  g.add(self._rect(-3.50, -0.34, 1.85, 0.30, ACCENT_C),
        self._sym(-0.34, "K ( f , g )   =   ∫ ₐ ᵇ  F ( f , g , t )   d t", ACCENT_C,
                  FS_TAG, x=-3.50, w=3.50))
  g.add(self._panel(((0.86, "左邊那個由上一集的定理 14.3 給出可微",
                      "the left one is differentiable by the last episode's Theorem 14.3", ACCENT_B),
                     (0.20, "右邊是有界線性泛函，微分就是它自己",
                      "the right one is a bounded linear functional, its own differential", WARN),
                     (-0.46, "合成規則一套，泛函就可微了",
                      "the composite rule then makes the functional differentiable", ACCENT_C))))
  return g.add(self._foot("先在比較寬的 K 上做，最後再限制到「第二個變數是第一個的導數」那個閉子空間上",
                          "the work is done on the wider K first and then restricted to the closed subspace where g is f prime",
                          ACCENT_A,
                          "那個子空間是閉的要用到第 4 章的積分理論，書上把這一步標了出來",
                          "that the subspace is closed needs the integral theory of chapter 4, and the book flags the step"))

 def _firstvariation(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.48, 2.65, 0.34, ACCENT_A),
        self._sym(0.48, "dG ( h )    =    ∫ ₐ ᵇ  [ dF ¹ ( h )  +  dF ² ( h ′ ) ]   d t",
                  ACCENT_A, FS_TAG + 1, x=-3.45, w=5.10))
  rows = [("        h                  Δ G / Δ            ∫  [ … ]", DIM),
          (f"    sin ( π t )         {VAR_QUOT:.6f}        {VAR_FORM:.6f}", WARN)]
  g.add(self._table(rows, x=-3.45, w=5.30, y0=-0.22, dy=0.42))
  return g.add(self._foot("兩個數字是兩種完全不同的算法：泛函沿 h 的差商，以及定理給的那個積分",
                          "the two numbers come two different ways: a difference quotient of the functional and the integral the theorem gives",
                          ACCENT_A,
                          "而且是在一條「不是解」的弧上算的——在解上兩邊都是零，那樣就驗不出什麼",
                          "and they are computed at an arc that is not a solution; on a solution both are zero and nothing is tested"))

 def _pinned(self):
  g = VGroup(self._arcaxes())
  g.add(self._arc(_line, DIM, sw=1.6))
  for a, col in ((0.55, ACCENT_B), (-0.40, ACCENT_C), (0.25, WARN)):
   g.add(self._curve([[self.AX + self.SX * k / 90,
                       self.AY + self.SY * (_line(k / 90.0) + a * math.sin(math.pi * k / 90.0)), 0]
                      for k in range(91)], col, sw=2.2))
  g.add(self._ends(ACCENT_A))
  g.add(self._panel(((0.86, "灰色那條是候選的弧",
                      "the grey arc is the candidate", DIM),
                     (0.20, "彩色的是它加上一個兩端為零的 h",
                      "the coloured ones are it plus an h vanishing at both ends", ACCENT_B),
                     (-0.46, "臨界點就是：對每一個這樣的 h，第一變分都是零",
                      "critical means the first variation vanishes for every such h", ACCENT_A))))
  return g.add(self._foot("端點固定給出一個閉平面，因為兩個取值映射都是有界線性的",
                          "fixed endpoints give a closed plane because both evaluation maps are bounded and linear",
                          ACCENT_A,
                          "那個平面平移回原點就是 M：兩端都取零的弧構成的子空間",
                          "translating that plane to the origin gives M, the arcs vanishing at both ends"))

 def _byparts(self):
  g = VGroup()
  lines = (("∫ ₐ ᵇ  ( ∂F / ∂x · h   +   ∂F / ∂y · h ′ )    =    0", ACCENT_B),
           ("[ ( ∫ ∂F / ∂x ) · h ] ₐ ᵇ    =    0", DIM),
           ("∫ ₐ ᵇ  ( ∂F / ∂y   −   ∫ ∂F / ∂x )  g    =    0", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.60, lab, col, FS_TAG - 1, x=-3.45, w=5.30))
  g.add(self._curve([[-5.45, 0.08, 0], [-5.15, 0.32, 0]], WARN, sw=2.5),
        self._curve([[-5.15, 0.08, 0], [-5.45, 0.32, 0]], WARN, sw=2.5))
  g.add(self._panel(((0.86, "把第一項分部積分",
                      "integrate the first term by parts", ACCENT_B),
                     (0.20, "端點項因為 h 兩端是零而消掉",
                      "the endpoint term drops because h vanishes at both ends", DIM),
                     (-0.46, "剩下的式子裡只出現 h 的導數",
                      "and only the derivative of h is left in what remains", WARN))))
  return g.add(self._foot("這就是變分法的招牌手法，叫 Du Bois-Reymond 引理",
                          "this is the trademark trick of the subject, the lemma of Du Bois-Reymond",
                          ACCENT_A,
                          "注意分部積分的是第一項，不是第二項——分掉的是 h，留下的是 h 的導數",
                          "note that it is the first term that is integrated by parts, leaving the derivative of h"))

 def _constant(self):
  g = VGroup()
  lines = (("g  =  h ′                  ∫ ₐ ᵇ  g   =   0", ACCENT_B),
           ("∂F / ∂y   −   ∫ ∂F / ∂x      ⊥      N", ACCENT_C),
           ("N ⊥   =   { C }", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.58, lab, col, FS_TAG, x=-3.45, w=5.30))
  g.add(self._rect(-3.45, -0.86, 2.55, 0.26, ACCENT_A),
        self._sym(-0.86, "∂F / ∂y   =   ∫ ₀ ᵗ  ∂F / ∂x   d s   +   C", ACCENT_A,
                  FS_TAG, x=-3.45, w=4.90))
  g.add(self._panel(((0.86, "h 的導數是任意的連續函數",
                      "the derivative of h is an arbitrary continuous function", ACCENT_B),
                     (0.20, "唯一的限制是它的積分為零",
                      "subject only to having integral zero", ACCENT_C),
                     (-0.46, "那個零空間的正交補是一維的常數",
                      "the orthogonal complement of that null space is the constants", WARN))))
  return g.add(self._foot("所以左邊那一整塊只能是常數——這一步把「對所有 h」換成一條方程",
                          "so the whole left side can only be a constant, which turns for all h into one equation",
                          ACCENT_A,
                          "常數是一維的，因為那個泛函的零空間在 C 裡的餘維數是一",
                          "the constants are one dimensional because that functional's null space has codimension one"))

 def _euler(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.58, 2.15, 0.34, ACCENT_A),
        self._sym(0.58, "d / d t    ∂F / ∂y    =    ∂F / ∂x", ACCENT_A, FS_TAG + 2,
                  x=-3.45, w=4.10))
  g.add(self._sym(-0.16, "∂ ² F / ∂y ²  f ″  +  ∂ ² F / ∂y ∂x  f ′  +  ∂ ² F / ∂y ∂t  −  ∂F / ∂x  =  0",
                  ACCENT_C, FS_TAG - 2, x=-3.45, w=5.40))
  # the row labels used to read "f = line" and "f = line + h", which is English
  # in a row that renders the same in both languages
  rows = [(f"    f  =  f ₀                  {RES_LINE:.2e}", ACCENT_B),
          (f"    f  =  f ₀ + h            {RES_BUMP:.4f}", WARN)]
  g.add(self._table(rows, x=-3.45, w=5.20, y0=-0.62, dy=0.34))
  return g.add(self._foot("把常數那條式子再微分一次就得到它；順帶還推出左邊真的可微，這件事本來看不出來",
                          "differentiating the constant identity once more gives it, and shows the left side is differentiable at all",
                          ACCENT_A,
                          "表格是 Euler 方程的殘差：在解上是零，在擾動過的弧上不是",
                          "the table is the Euler residual: zero on the solution and not on the perturbed arc"))

 def _shortest(self):
  g = VGroup(self._arcaxes())
  for (e, _), col in zip(LENS, (ACCENT_B, ACCENT_C, ACCENT_C, ACCENT_B)):
   g.add(self._arc(_bump(e), col, sw=1.8))
  g.add(self._arc(_line, WARN, sw=3.0), self._ends(ACCENT_A))
  rows = ([("       ϵ                L", DIM),
           (f"    {0.0:+.2f}          {STRAIGHT:.6f}", WARN)]
          + [(f"    {e:+.2f}          {L:.6f}", ACCENT_C) for e, L in LENS])
  g.add(self._table(rows, x=PANEL_X, w=PANEL_W, y0=0.80, dy=0.32))
  return g.add(self._foot(f"被積函數不含 x，所以 Euler 方程說對 y 的偏導數是常數（畫面上這條是 {PY_CONST:.4f}），導數也就是常數",
                          f"the integrand has no x, so Euler makes the partial in y constant, here {PY_CONST:.4f}, hence the derivative constant",
                          ACCENT_A,
                          "四條擾動過的弧都量過，每一條都比直線長——這不是證明，可是它確認方向沒有搞反",
                          "all four perturbed arcs were measured and every one is longer, which confirms the direction"))

 def _free(self):
  g = VGroup(self._arcaxes())
  g.add(self._arc(_line, DIM, sw=1.6))
  for a, b, col in ((0.55, 0.35, ACCENT_B), (-0.40, -0.55, ACCENT_C)):
   g.add(self._curve([[self.AX + self.SX * k / 90,
                       self.AY + self.SY * (_line(k / 90.0)
                                            + a * math.sin(math.pi * k / 90.0)
                                            + b * (k / 90.0)), 0]
                      for k in range(91)], col, sw=2.2))
  g.add(self._sym(0.86, "∂F / ∂y  ( a )    =    ∂F / ∂y  ( b )    =    0", WARN,
                  FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "h 不再被釘在兩端", "h is no longer pinned at the ends",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "分部積分留下的端點項不再消失",
                  "so the endpoint term from the integration by parts survives", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "Euler 方程照樣成立，另外多兩個端點條件",
                  "the Euler equation still holds, with two endpoint conditions added", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("端點既不固定也不完全自由的情形要到第 13 章講力學時才處理",
                          "endpoints neither fixed nor wholly free wait until chapter 13, on mechanics",
                          ACCENT_A,
                          "而「什麼時候真的是極大或極小」要看第二變分——那正是下一集第 16 節的主題",
                          "whether it really is a maximum needs the second variation, which is the next section's subject"))

 def stage(self):
  a, b, c = self._problem(), self._plane(), self._space()
  d, e, f = self._differentiable(), self._firstvariation(), self._pinned()
  h, i, j = self._byparts(), self._constant(), self._euler()
  k, l = self._shortest(), self._free()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE52ZH, AdvCalcE52EN = make(AdvCalcE52Base, "52", prefix="AdvCalcE")
