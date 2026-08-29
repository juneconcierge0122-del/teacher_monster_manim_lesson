"""advcalc E51 -- chapter 3, section 14 (book pp. 179-182): uniform continuity
and function-valued mappings.  The pattern of the section is escalation: a
point-to-point map F on a product is turned into a map from one factor into a
space of functions on the other, and uniform continuity of F is exactly what
makes the escalated map continuous (Theorem 14.1) or differentiable (Theorem
14.2).  Theorem 14.3, on composition by g, is the one used later, in section 15
and in chapter 6.  Section 14 has no exercises; section 15 starts partway down
page 182.

The beats are checked numerically.  The opening contrast is made concrete: for
one over x on the half-open unit interval the largest delta that works for a
fixed epsilon is computed at two anchors and shown to collapse by a factor of
more than a hundred, while for the product on the unit square one delta is shown
by sampling to work everywhere.  Differentiation under the integral sign is
checked three ways at one point -- a difference quotient of the integral, the
integral of the partial derivative, and the closed form -- and Theorem 14.3 is
checked by watching the remainder of the composition map fall faster than the
increment on a concrete f, h and g.
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


# ── beat 0: continuity that is not uniform, and continuity that is ─────
EPS0 = 0.5


def _delta_recip(a, eps=EPS0):
 """The largest delta that works for 1/x at the anchor a: the left side binds."""
 return a - 1.0 / (1.0 / a + eps)


# Both anchors have to sit on the part of the curve that fits on screen, which
# caps how big the ratio between their deltas can be. FAR is the same
# computation at an anchor far off the left of the picture, so the footer can
# say that the collapse keeps going.
ANCHORS = (0.70, 0.13)
DELTAS = tuple(_delta_recip(a) for a in ANCHORS)
RATIO = DELTAS[0] / DELTAS[1]
FAR = 0.01
FAR_RATIO = DELTAS[0] / _delta_recip(FAR)
assert RATIO > 15, "the two drawn anchors have to differ enough to be worth drawing"
assert FAR_RATIO > 1000, "and the collapse has to keep going off the left of the picture"
for _a, _d in zip(ANCHORS, DELTAS):
 assert abs(1.0 / (_a - _d * 0.999) - 1.0 / _a) < EPS0 + 1e-9, "the delta claimed is too big"

EPS_SQ, DEL_SQ = 0.10, 0.05
_grid = [(i / 40.0, j / 40.0) for i in range(41) for j in range(41)]
for _p in _grid:
 for _dx, _dy in ((DEL_SQ, 0.0), (0.0, DEL_SQ), (DEL_SQ, DEL_SQ), (-DEL_SQ, DEL_SQ)):
  _q = (min(max(_p[0] + _dx, 0.0), 1.0), min(max(_p[1] + _dy, 0.0), 1.0))
  assert abs(_p[0] * _p[1] - _q[0] * _q[1]) <= EPS_SQ + 1e-12, \
      "one delta does not work everywhere on the square after all"


# ── beats 5 and 8: the integral, and differentiating under it ──────────
def _Fxy(x, y):
 return x * x * y ** 3 + math.sin(x * y)


def _simpson(f, n=2000):
 h = 1.0 / n
 s = f(0.0) + f(1.0)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * f(k * h)
 return s * h / 3.0


def _integral(y):
 return _simpson(lambda x: _Fxy(x, y))


Y0 = 0.80
STEP_Y = 1e-4
LHS = (_integral(Y0 + STEP_Y) - _integral(Y0 - STEP_Y)) / (2 * STEP_Y)
RHS = _simpson(lambda x: (_Fxy(x, Y0 + H) - _Fxy(x, Y0 - H)) / (2 * H))
EXACT = Y0 ** 2 + (math.sin(Y0) * Y0 - (1.0 - math.cos(Y0))) / Y0 ** 2
assert abs(LHS - RHS) < 1e-6 and abs(LHS - EXACT) < 1e-6, \
    "the three ways of getting the derivative do not agree"
# and the integral itself moves continuously with y
CONT = [(y, _integral(y)) for y in (0.60, 0.70, 0.80)]
assert all(abs(b[1] - a[1]) < 0.6 for a, b in zip(CONT, CONT[1:]))


# ── beats 9 and 10: Theorem 14.3 on a concrete composition ─────────────
def _g(a):
 return a * a


def _f(s):
 return math.sin(s)


def _h(s):
 return math.cos(3 * s)


SS = [math.pi * k / 240.0 for k in range(241)]
BND = 2.0
assert max(abs(2 * _f(s)) for s in SS) <= BND + 1e-9, "two is a bound for dg on the range of f"


def _remainder(t):
 """sup over s of the error in dG, divided by the size of the increment."""
 return max(abs((_g(_f(s) + t * _h(s)) - _g(_f(s))) - t * 2 * _f(s) * _h(s))
            for s in SS) / (t * max(abs(_h(s)) for s in SS))


REM = [(t, _remainder(t)) for t in (1e-1, 1e-2, 1e-3)]
assert all(a[1] > b[1] for a, b in zip(REM, REM[1:])), "the remainder has to shrink"
assert REM[-1][1] < 1e-2, "and it has to be small, or dG is not the differential"


class AdvCalcE51Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 51

 MODE_LABEL = {
  0: {"zh": "δ 可不可以跟位置無關", "en": "may delta ignore where you stand"},
  1: {"zh": "這一節的模式：升級", "en": "the pattern: escalation"},
  2: {"zh": "一族函數，一個一致範數", "en": "a family of functions, one uniform norm"},
  3: {"zh": "定理 14.1：連續性傳得過去", "en": "Theorem 14.1: continuity carries across"},
  4: {"zh": "證明只有兩行", "en": "the proof is two lines"},
  5: {"zh": "推論：積分對參數連續", "en": "a corollary: the integral is continuous in y"},
  6: {"zh": "定理 14.2：可微也傳得過去", "en": "Theorem 14.2: so does differentiability"},
  7: {"zh": "關鍵是換一個讀法", "en": "the key is a change of reading"},
  8: {"zh": "積分號下微分", "en": "differentiating under the integral"},
  9: {"zh": "定理 14.3：把「接上 g」當成映射", "en": "Theorem 14.3: composition as a map"},
  10: {"zh": "T 真的是有界線性映射", "en": "T really is a bounded linear map"},
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

 # ── beats ─────────────────────────────────────────────────────────
 def _notuniform(self):
  ox, oy = -6.05, -0.75
  sx, sy = 5.10, 0.17
  X = lambda x: ox + x * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.10, oy, 0], [X(1.02), oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, Y(9.0), 0], color=DIM, stroke_width=1.4))
  g.add(self._curve([[X(0.12 + 0.88 * k / 180), Y(1.0 / (0.12 + 0.88 * k / 180)), 0]
                     for k in range(181)], ACCENT_C, sw=2.6))
  for a, d, col in zip(ANCHORS, DELTAS, (ACCENT_B, WARN)):
   g.add(Dot([X(a), Y(1.0 / a), 0], radius=0.06, color=col),
         Line([X(a - d), oy - 0.14, 0], [X(a + d), oy - 0.14, 0], color=col, stroke_width=5),
         self._dash([X(a), oy, 0], [X(a), Y(1.0 / a), 0], col, n=8, sw=1.2))
  g.add(self._panel(((0.86, "同一個 ε，站在不同的地方",
                      "one epsilon, two places to stand", DIM),
                     (0.20, "站得越靠近左邊，δ 要取得越小",
                      "the further left you stand, the smaller delta must be", WARN),
                     (-0.46, "均勻連續就是要求 δ 跟位置無關",
                      "uniform continuity asks that delta not depend on where", ACCENT_A))))
  return g.add(self._foot(f"程式算過：ε 取 {EPS0:.1f} 時，在 {ANCHORS[0]:.2f} 可以取 δ = {DELTAS[0]:.3f}，"
                          f"在 {ANCHORS[1]:.2f} 只剩 {DELTAS[1]:.4f}",
                          f"computed here: for epsilon {EPS0:.1f}, delta is {DELTAS[0]:.3f} at "
                          f"{ANCHORS[0]:.2f} and only {DELTAS[1]:.4f} at {ANCHORS[1]:.2f}",
                          ACCENT_A,
                          f"相差 {RATIO:.0f} 倍；在 {FAR:.2f} 那裡更是差了 {FAR_RATIO:.0f} 倍，所以這個函數不是均勻連續的",
                          f"a factor of {RATIO:.0f}, and {FAR_RATIO:.0f} at {FAR:.2f}, so it is not uniformly continuous"))

 def _escalate(self):
  g = VGroup()
  g.add(self._rect(-4.55, 0.56, 1.55, 0.30, ACCENT_B),
        self._sym(0.56, "F  :  M × N   →   X", ACCENT_B, FS_TAG, x=-4.55, w=2.90))
  g.add(self._arr([-4.55, 0.16, 0], [-4.55, -0.06, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._rect(-4.55, -0.40, 1.55, 0.30, WARN),
        self._sym(-0.40, "φ  :  N   →   Y", WARN, FS_TAG, x=-4.55, w=2.90))
  g.add(self._mid(0.56, "點到點的映射", "a point-to-point map", DIM,
                  FS_TAG, x=-1.85, w=2.40),
        self._mid(-0.40, "函數值的映射", "a function-valued map", ACCENT_C,
                  FS_TAG, x=-1.85, w=2.40))
  g.add(self._panel(((0.86, "把第二個變數當成參數",
                      "treat the second variable as a parameter", ACCENT_B),
                     (0.20, "每個參數值給出 M 上的一個函數",
                      "each value of it gives one function on M", WARN),
                     (-0.46, "點映射的性質會傳給升級後的映射",
                      "properties of the point map pass to the escalated one", ACCENT_A))))
  return g.add(self._foot("這個模式在第 15 節的變分法與第 6 章的微分方程裡都會用到",
                          "the pattern is used in section 15 on variations and in chapter 6 on differential equations",
                          ACCENT_A,
                          "最直接的應用是「積分號下微分」，這一集第 8 拍就會算到",
                          "the immediate application is differentiating under the integral, reached in beat eight"))

 def _family(self):
  ox, oy = -5.85, -0.10
  sx, sy = 4.60, 0.62
  X = lambda x: ox + x * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.10, oy, 0], [X(1.04), oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.62, 0], [ox, oy + 1.02, 0], color=DIM, stroke_width=1.4))
  for e, col in ((0.35, ACCENT_B), (0.75, ACCENT_C), (1.15, WARN)):
   g.add(self._curve([[X(k / 60.0), Y(0.55 * math.sin(2.6 * k / 60.0 + e) + 0.30 * e), 0]
                      for k in range(61)], col, sw=2.4))
  # the uniform norm is the widest vertical gap, not the average one
  xs = 0.42
  g.add(self._arr([X(xs), Y(0.55 * math.sin(2.6 * xs + 0.35) + 0.105), 0],
                  [X(xs), Y(0.55 * math.sin(2.6 * xs + 1.15) + 0.345), 0],
                  ACCENT_A, sw=2.5, tl=0.10))
  g.add(self._panel(((0.86, "每個參數值給出一條曲線",
                      "each value of the parameter gives one curve", ACCENT_B),
                     (0.20, "它們住在同一個函數空間裡",
                      "and they all live in one space of functions", ACCENT_C),
                     (-0.46, "兩條曲線的距離取最大的那個間隙",
                      "the distance between two of them is the widest gap", ACCENT_A))))
  return g.add(self._foot("一致範數取的是上確界，不是平均——所以「靠近」是「處處靠近」",
                          "the uniform norm is a least upper bound, not an average, so close means close everywhere",
                          ACCENT_A,
                          "那個空間是無窮維的，可是它仍然是一個賦範空間，前面的定理照樣適用",
                          "that space is infinite dimensional, yet still normed, so the earlier theorems still apply"))

 def _thm141(self):
  ox, oy = -5.85, 0.00
  sx, sy = 4.60, 0.55
  X = lambda x: ox + x * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.10, oy, 0], [X(1.04), oy, 0], color=DIM, stroke_width=1.4))
  base = lambda x: 0.60 * math.sin(2.6 * x + 0.6) + 0.20
  g.add(self._curve([[X(k / 60.0), Y(base(k / 60.0)), 0] for k in range(61)], ACCENT_B, sw=2.6),
        self._curve([[X(k / 60.0), Y(base(k / 60.0) + 0.12), 0] for k in range(61)], WARN, sw=2.2))
  for sgn in (1, -1):
   g.add(self._dash([X(0), Y(base(0) + 0.06 + sgn * 0.20), 0],
                    [X(1.0), Y(base(1.0) + 0.06 + sgn * 0.20), 0], DIM, n=26, sw=1.0))
  g.add(self._panel(((0.86, "兩個參數值靠得夠近",
                      "two values of the parameter close enough together", ACCENT_B),
                     (0.20, "兩條曲線就整條落在同一個 ε 帶裡",
                      "and the two curves stay inside one epsilon band throughout", WARN),
                     (-0.46, "所以升級後的映射是均勻連續的",
                      "so the escalated map is uniformly continuous", ACCENT_A))))
  return g.add(self._foot("關鍵是 δ 對每一個 ξ 都一樣——這正是均勻連續給的東西",
                          "the point is that one delta serves every xi, which is exactly what uniformity gives",
                          ACCENT_A,
                          "如果 F 只是連續而不均勻，δ 會隨 ξ 變，取不到一個對整條曲線都成立的",
                          "if F were merely continuous the delta would vary with xi and no single one would serve"))

 def _proof141(self):
  g = VGroup()
  lines = (("‖ ⟨ ξ , η ⟩ − ⟨ μ , ν ⟩ ‖ < δ    ⇒    ‖ F ( ξ , η ) − F ( μ , ν ) ‖ < ϵ", ACCENT_B),
           ("μ   :=   ξ", ACCENT_C),
           ("‖ η − ν ‖ < δ    ⇒    ‖ F ( ξ , η ) − F ( ξ , ν ) ‖ < ϵ        ∀ ξ", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.58, lab, col, FS_TAG - 2, x=-3.55, w=5.30))
  g.add(self._rect(-3.55, -0.86, 2.15, 0.26, ACCENT_A),
        self._sym(-0.86, "‖ φ ( η ) − φ ( ν ) ‖   ≤   ϵ", ACCENT_A, FS_TAG, x=-3.55, w=4.10))
  g.add(self._panel(((0.86, "均勻連續給的 δ",
                      "the delta that uniformity provides", ACCENT_B),
                     (0.20, "第一個變數兩邊取成同一個",
                      "take the first variable to be the same on both sides", ACCENT_C),
                     (-0.46, "每一點都近，就是一致範數下近",
                      "close at every point is close in the uniform norm", WARN))))
  return g.add(self._foot("最後那個小於等於是因為上確界：逐點的嚴格不等式取上確界之後只保得住不等於",
                          "the final inequality is not strict because a least upper bound of strict ones need not be",
                          ACCENT_A,
                          "整個證明沒有用到任何有限維的東西，所以在無窮維上一樣成立",
                          "nothing in the proof uses finite dimensionality, so it holds in infinite dimensions too"))

 def _integralcont(self):
  ox, oy = -5.85, -0.55
  sx, sy = 4.40, 0.36
  X = lambda x: ox + x * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.10, oy, 0], [X(1.06), oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, Y(2.5), 0], color=DIM, stroke_width=1.4))
  for (y, _), col in zip(CONT, (ACCENT_B, ACCENT_C, WARN)):
   g.add(self._curve([[X(k / 60.0), Y(_Fxy(k / 60.0, y) + 0.9), 0] for k in range(61)],
                     col, sw=2.4))
  rows = [("        y            ∫ ₀ ¹ F  d x", DIM)]
  for y, v in CONT:
   rows.append((f"    {y:.2f}            {v:.5f}", ACCENT_C))
  g.add(self._table(rows, y0=0.60, dy=0.44))
  return g.add(self._foot("三條曲線是三個 y 值的被積函數，右邊是它們的積分，隨 y 平滑地移動",
                          "the three curves are the integrands at three values of y, and the integrals move smoothly",
                          ACCENT_A,
                          "理由不是計算，是合成：積分是一個有界線性泛函，接上剛才那個連續映射",
                          "the reason is not computation but composition: integration is a bounded linear functional"))

 def _thm142(self):
  g = VGroup()
  g.add(self._rect(-4.85, 0.52, 1.45, 0.30, ACCENT_B),
        self._mid(0.52, "第二個偏微分有界、均勻連續",
                  "the second partial differential is bounded and uniform",
                  ACCENT_B, FS_TAG - 1, x=-4.85, w=2.70))
  g.add(self._arr([-3.30, 0.52, 0], [-2.85, 0.52, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._rect(-1.55, 0.52, 1.15, 0.30, WARN),
        self._mid(0.52, "φ 可微", "phi is differentiable", WARN, FS_TAG - 1, x=-1.55, w=2.10))
  g.add(self._rect(-3.35, -0.42, 2.45, 0.32, ACCENT_C),
        self._sym(-0.42, "[ dφ ᵦ ( η ) ] ( ξ )    =    dF ² ⟨ ξ , β ⟩ ( η )", ACCENT_C,
                  FS_TAG + 1, x=-3.35, w=4.70))
  g.add(self._panel(((0.86, "假設從連續換成可微",
                      "the hypothesis moves from continuous to differentiable", ACCENT_B),
                     (0.20, "結論也跟著換",
                      "and so does the conclusion", WARN),
                     (-0.46, "微分逐點就是那個偏微分",
                      "the differential is that partial, taken pointwise", ACCENT_C))))
  return g.add(self._foot("注意結論裡的微分是一個「函數到函數」的線性映射，可是它的公式逐點就寫完了",
                          "the differential in the conclusion is a map of functions, yet its formula is pointwise",
                          ACCENT_A,
                          "書上說 φ 其實是連續可微的，把同樣的論證再走一次就得到",
                          "the book notes that phi is in fact continuously differentiable, by the same argument again"))

 def _reading(self):
  g = VGroup()
  lines = (("Δ F ² ⟨ ξ , β ⟩ ( η )    =    F ( ξ , β + η )  −  F ( ξ , β )", ACCENT_B),
           ("=    [ φ ( β + η )  −  φ ( β ) ] ( ξ )", ACCENT_C),
           ("=    [ Δ φ ᵦ ( η ) ] ( ξ )", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.78 - k * 0.60, lab, col, FS_TAG - 1, x=-3.45, w=5.40))
  g.add(self._panel(((0.86, "左邊是 X 裡的一個向量",
                      "the left side is a vector in X", ACCENT_B),
                     (0.20, "右邊是函數空間裡的一個函數，在 ξ 取值",
                      "the right side is a function in the big space, evaluated at xi", ACCENT_C),
                     (-0.46, "同一件事寫兩次，證明就是靠這個",
                      "the same thing written twice, and the proof runs on it", WARN))))
  return g.add(self._foot("剩下的只是把逐點的估計取上確界，再驗那個 T 落在 Hom 裡",
                          "what remains is taking a least upper bound of the pointwise estimate and checking T is in Hom",
                          ACCENT_A,
                          "逐點的估計本身來自定理 7.4 的推論，也就是均值定理那一集的結果",
                          "the pointwise estimate itself is the corollary to Theorem 7.4, from the mean value episode"))

 def _underintegral(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.62, 2.55, 0.32, ACCENT_A),
        self._sym(0.62, "d / d y   ∫ ₀ ¹  F  d x        =        ∫ ₀ ¹  ∂F / ∂y   d x",
                  ACCENT_A, FS_TAG + 1, x=-3.45, w=4.90))
  # the last row used to be labelled in English, which would have shown up in
  # the Chinese render; every label here is a symbol
  rows = [(f"F ( x , y )   =   x ² y ³  +  sin ( x y )        y  =  {Y0:.1f}", DIM),
          (f"Δ  /  Δ y                {LHS:.8f}", ACCENT_B),
          (f"∫  ∂F / ∂y              {RHS:.8f}", ACCENT_C),
          (f"I ′ ( y )                  {EXACT:.8f}", WARN)]
  g.add(self._table(rows, x=-3.45, w=5.40, y0=0.08, dy=0.34))
  return g.add(self._foot("三個數字是三種完全不同的算法：積分的差商、偏導數的積分、以及手推的封閉形式",
                          "the three numbers come three different ways: a quotient of integrals, an integral of partials, and a closed form",
                          ACCENT_A,
                          "定理保證的正是前兩者相等；第三個只是拿來確認前兩者沒有一起算錯",
                          "the theorem is exactly that the first two agree; the third is there in case both went wrong together"))

 def _thm143(self):
  g = VGroup()
  for cx, lab, col in ((-5.05, "f  :  S  →  A", ACCENT_B),
                       (-2.35, "g ∘ f  :  S  →  W", WARN)):
   g.add(self._rect(cx, 0.52, 1.20, 0.30, col),
         self._sym(0.52, lab, col, FS_TAG, x=cx, w=2.20))
  g.add(self._arr([-3.90, 0.52, 0], [-3.60, 0.52, 0], ACCENT_A, sw=2.5, tl=0.10))
  g.add(self._sym(0.86, "G", ACCENT_A, FS_TAG, x=-3.75, w=0.60))
  g.add(self._rect(-3.75, -0.34, 2.55, 0.32, ACCENT_C),
        self._sym(-0.34, "[ dG ( h ) ] ( s )    =    dg ( f ( s ) ;  h ( s ) )", ACCENT_C,
                  FS_TAG + 1, x=-3.75, w=4.90))
  g.add(self._panel(((0.86, "把「接上 g」本身當成一個映射",
                      "make composition by g into a map of its own", ACCENT_B),
                     (0.20, "g 可微、微分有界均勻連續",
                      "with g differentiable and its differential bounded and uniform", WARN),
                     (-0.46, "那麼這個映射可微，微分逐點就是 g 的微分",
                      "then it is differentiable, and its differential is g's, pointwise", ACCENT_C))))
  return g.add(self._foot("分號左邊是取微分的那一點，右邊是微分作用的向量——兩個都跟著 s 走",
                          "left of the semicolon is where the differential is taken, right of it the vector it acts on",
                          ACCENT_A,
                          "這是這一節裡後面唯一真的會被引用的定理，第 15 節與第 6 章都靠它",
                          "this is the one theorem of the section actually quoted later, in section 15 and chapter 6"))

 def _hom(self):
  g = VGroup()
  lines = (("T ( h ₁ + h ₂ )  =  T ( h ₁ )  +  T ( h ₂ )", ACCENT_B),
           (f"‖ T ‖   ≤   b   =   {BND:.0f}", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.86 - k * 0.46, lab, col, FS_TAG, x=-4.45, w=3.40))
  rows = [("        t          ‖ Δ G − T ‖  /  ‖ h ‖", DIM)]
  for t, r in REM:
   rows.append((f"    {t:.3f}                  {r:.6f}", WARN))
  g.add(self._table(rows, x=-4.35, w=4.60, y0=-0.06, dy=0.30))
  g.add(self._panel(((0.86, "加法與齊次都是逐點驗的",
                      "additivity and homogeneity are checked pointwise", ACCENT_B),
                     (0.20, "範數不超過 dg 在值域上的界",
                      "the norm is at most the bound on dg over the range", ACCENT_C),
                     (-0.46, "右邊那一欄掉下去，所以餘項真的是小 o",
                      "the column falls away, so the remainder really is little oh", WARN))))
  return g.add(self._foot("表格是程式在一個具體的 g、f、h 上算的：g 是平方，f 是正弦，h 是三倍角的餘弦",
                          "the table was computed on a concrete g, f and h here: squaring, a sine and a cosine",
                          ACCENT_A,
                          "第 14 節到此結束，這一節整節沒有習題。下一集講第 15 節的變分法",
                          "that ends section 14, which has no exercises; next is section 15 on the calculus of variations"))

 def stage(self):
  a, b, c = self._notuniform(), self._escalate(), self._family()
  d, e, f = self._thm141(), self._proof141(), self._integralcont()
  h, i, j = self._thm142(), self._reading(), self._underintegral()
  k, l = self._thm143(), self._hom()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE51ZH, AdvCalcE51EN = make(AdvCalcE51Base, "51", prefix="AdvCalcE")
