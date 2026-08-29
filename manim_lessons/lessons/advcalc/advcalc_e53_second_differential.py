"""advcalc E53 -- chapter 3, section 16, first part (book pp. 186-189): the
second differential.  The differential of F is itself a map into Hom, so it can
be differentiated again; the result eats two vectors and is equivalent to a
bounded bilinear map.  Theorem 16.1 identifies it with the nested directional
derivative, Corollary 1 and Theorem 16.2 tie it to the second partials in
coordinates, and Theorem 16.3 says it is symmetric.  The classification of
critical points that the section is named for is the next episode.

Every claim on screen is computed on one function of two variables.  The second
partials are found by central differences, Theorem 16.1 is checked by taking two
directional derivatives in a row and comparing against the bilinear form, and
the second difference is checked to approach that same form as the increments
shrink.  The closing counterexample matters: its two mixed partials are computed
to be minus one and plus one, so they exist and differ, which is only possible
because no second differential exists there -- without that beat the symmetry
theorem would look like it needed no hypothesis at all.
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


def _F(v):
 x, y = v
 return x ** 3 * y + math.sin(x * y) + x * x * y * y


APT = (0.70, -0.40)
BV, CV = (1.00, 0.50), (-0.30, 1.20)


def _dir(f, a, u, h=1e-5):
 """The directional derivative of a scalar function, by central differences."""
 p = tuple(x + h * d for x, d in zip(a, u))
 m = tuple(x - h * d for x, d in zip(a, u))
 return (f(p) - f(m)) / (2 * h)


def _second(f, a, i, j, h=1e-4):
 e = [(1.0, 0.0), (0.0, 1.0)]
 return _dir(lambda p: _dir(f, p, e[i], h), a, e[j], h)


HESS = [[_second(_F, APT, i, j) for j in range(2)] for i in range(2)]
assert abs(HESS[0][1] - HESS[1][0]) < 1e-5, \
    "the mixed partials disagree, so Theorem 16.3 would be false on this example"
SYM_GAP = abs(HESS[0][1] - HESS[1][0])

# Theorem 16.1: two directional derivatives in a row, against the bilinear form
NESTED = _dir(lambda p: _dir(_F, p, BV), APT, CV)
BILIN = sum(BV[i] * CV[j] * HESS[j][i] for i in range(2) for j in range(2))
assert abs(NESTED - BILIN) < 1e-4, \
    "the nested directional derivative is not the second differential on those two"

# the second difference, which is symmetric by inspection, tends to the same form
def _seconddiff(a, eta, xi):
 p = lambda *vs: tuple(a[k] + sum(v[k] for v in vs) for k in range(2))
 return _F(p(eta, xi)) - _F(p(eta)) - _F(p(xi)) + _F(a)


# the second difference closes in on the bilinear form only like s, not like
# s squared, so the smallest increment has to be genuinely small
DIFFS = []
for _s in (0.20, 0.05, 0.01, 0.002):
 _e = tuple(_s * u for u in BV)
 _x = tuple(_s * u for u in CV)
 _sym = abs(_seconddiff(APT, _e, _x) - _seconddiff(APT, _x, _e))
 assert _sym < 1e-12, "the second difference is symmetric by construction"
 DIFFS.append((_s, _seconddiff(APT, _e, _x) / _s ** 2))
assert all(abs(b[1] - BILIN) < abs(a[1] - BILIN) for a, b in zip(DIFFS, DIFFS[1:])), \
    "the second difference has to close in on the bilinear form"
assert abs(DIFFS[-1][1] - BILIN) < 1e-2


# ── beat 10: mixed partials that exist and differ ──────────────────────
def _bad(v):
 x, y = v
 if x == 0.0 and y == 0.0:
  return 0.0
 return x * y * (x * x - y * y) / (x * x + y * y)


def _bad_x(y, h=1e-9):
 return (_bad((h, y)) - _bad((-h, y))) / (2 * h)


def _bad_y(x, h=1e-9):
 return (_bad((x, h)) - _bad((x, -h))) / (2 * h)


K = 1e-3
MIX_YX = (_bad_x(K) - _bad_x(-K)) / (2 * K)
MIX_XY = (_bad_y(K) - _bad_y(-K)) / (2 * K)
assert abs(MIX_YX + 1.0) < 1e-5 and abs(MIX_XY - 1.0) < 1e-5, \
    "the counterexample's two mixed partials should come out at minus one and plus one"
assert abs(MIX_XY - MIX_YX) > 1.5, "and they have to differ, or the beat says nothing"


class AdvCalcE53Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 53

 MODE_LABEL = {
  0: {"zh": "微分本身也是一個映射", "en": "the differential is itself a map"},
  1: {"zh": "二階微分的定義", "en": "the definition of the second differential"},
  2: {"zh": "它其實是一個雙線性映射", "en": "it is really a bilinear map"},
  3: {"zh": "定理 16.1：就是混合方向導數", "en": "Theorem 16.1: the nested directional derivative"},
  4: {"zh": "證明：在 μ 取值的那個映射", "en": "the proof: evaluation at mu"},
  5: {"zh": "推論：座標下是二階偏導數", "en": "a corollary: the second partials in coordinates"},
  6: {"zh": "定理 16.2：實際會用的判準", "en": "Theorem 16.2: the test actually used"},
  7: {"zh": "逐分量檢查的根據", "en": "what licenses checking componentwise"},
  8: {"zh": "三階以上一模一樣", "en": "third order and beyond, unchanged"},
  9: {"zh": "定理 16.3：對稱", "en": "Theorem 16.3: symmetry"},
  10: {"zh": "二階差分，與一個反例", "en": "the second difference, and a counterexample"},
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

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _dfismap(self):
  g = VGroup(self._blob(-5.05, 0.10, 1.05, 0.72, 0.12, ACCENT_B))
  for dx, dy, col in ((-0.35, 0.22, WARN), (0.42, -0.24, ACCENT_C)):
   g.add(Dot([-5.05 + dx, 0.10 + dy, 0], radius=0.06, color=col))
  for k, (col, m) in enumerate(((WARN, HESS), (ACCENT_C, HESS))):
   gr, _ = self._numgrid(-1.95, 0.62 - k * 1.05,
                         [[f"{v:.2f}" for v in row] for row in m], color=col,
                         dx=0.92, dy=0.44, size=FS_TAG - 3)
   g.add(gr)
  g.add(self._arr([-3.85, 0.24, 0], [-3.05, 0.40, 0], WARN, sw=2, tl=0.10),
        self._arr([-3.85, -0.10, 0], [-3.05, -0.55, 0], ACCENT_C, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "每一點對到一個線性映射",
                      "each point is sent to one linear map", ACCENT_B),
                     (0.20, "所以 dF 本身是一個映射，值落在 Hom 裡",
                      "so dF is itself a map, with values in Hom", WARN),
                     (-0.46, "既然是映射，就可以問它可不可微",
                      "and being a map, it can be asked to be differentiable", ACCENT_A))))
  return g.add(self._foot("這一步是整節的起點，而且它跟第 6 節定義一階微分時的動作一模一樣",
                          "this is where the section starts, and it repeats exactly what section 6 did for the first differential",
                          ACCENT_A,
                          "畫面上那兩個矩陣是同一個函數在兩點的二階資料，用中央差商算的",
                          "the two matrices are that function's second-order data at two points, by central differences"))

 def _definition(self):
  g = VGroup()
  rows = (("F  :  A  →  W", ACCENT_B),
          ("dF  :  A  →  Hom ( V , W )", ACCENT_C),
          ("d ² F ₐ  ∈  Hom ( V ,  Hom ( V , W ) )", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.60, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._sym(-0.90, "d ² F ₐ ( η ) ( ξ )   ∈   W", ACCENT_A, FS_TAG, x=-3.55, w=4.50))
  g.add(self._panel(((0.86, "定義照抄一階的：把 d 作用在 dF 上",
                      "the definition copies the first: apply d to dF", ACCENT_C),
                     (0.20, "所以它吃兩個向量，一次吃一個",
                      "so it eats two vectors, one at a time", WARN),
                     (-0.46, "吃完第一個得到 Hom 裡的元素，再吃第二個才落到 W",
                      "the first gives an element of Hom, the second lands in W", ACCENT_A))))
  return g.add(self._foot("寫成兩層 Hom 看起來嚇人，可是它做的事就是「兩個方向各微一次」",
                          "the nested Hom looks forbidding, yet all it does is differentiate once in each of two directions",
                          ACCENT_A,
                          "同樣的動作可以一直做下去，第 8 拍會看到三階的樣子",
                          "the same move repeats without end, and beat eight shows the third order"))

 def _bilinear(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("η", ACCENT_B), ("ξ", ACCENT_C))):
   g.add(self._rect(-5.35, 0.52 - k * 0.86, 0.44, 0.28, col),
         self._sym(0.52 - k * 0.86, lab, col, FS_TAG + 2, x=-5.35, w=0.90))
   g.add(self._arr([-4.85, 0.52 - k * 0.86, 0], [-4.15, 0.12 + k * 0.06, 0],
                   col, sw=2, tl=0.10))
  g.add(self._rect(-3.65, 0.09, 0.85, 0.34, WARN),
        self._sym(0.09, "ω", WARN, FS_TAG + 3, x=-3.65, w=1.60))
  g.add(self._arr([-2.70, 0.09, 0], [-2.10, 0.09, 0], ACCENT_A, sw=2.5, tl=0.10),
        self._sym(0.09, "W", ACCENT_A, FS_TAG + 2, x=-1.70, w=0.80))
  g.add(self._panel(((0.86, "兩個變數各自線性",
                      "linear in each of the two variables", ACCENT_B),
                     (0.20, "值落在 W 裡，而且有界",
                      "with values in W, and bounded", WARN),
                     (-0.46, "書上說它應該是某種二階導數",
                      "the book says it ought to be a second derivative of some kind", ACCENT_A))))
  return g.add(self._foot("兩層 Hom 與雙線性映射是同一件事，這在第 1 章講積空間時就建立好了",
                          "the nested Hom and the bilinear map are the same thing, settled back in chapter 1",
                          ACCENT_A,
                          "而讀者大概已經猜到，它就是沿 η 與沿 ξ 的混合導數——下一拍證明這件事",
                          "the reader has probably guessed it is the mixed derivative, and the next beat proves it"))

 def _thm161(self):
  g = VGroup()
  g.add(self._rect(-3.55, 0.58, 2.45, 0.32, ACCENT_A),
        self._sym(0.58, "D ᵥ ( D ᵤ F ) ( α )    =    ( d ² F ₐ ( ν ) ) ( μ )", ACCENT_A,
                  FS_TAG + 1, x=-3.55, w=4.70))
  rows = [(f"    μ  =  ⟨ {BV[0]:.1f} , {BV[1]:.1f} ⟩        ν  =  ⟨ {CV[0]:.1f} , {CV[1]:.1f} ⟩", DIM),
          (f"    D ᵥ ( D ᵤ F )              {NESTED:.6f}", ACCENT_B),
          (f"    Σ  μ ᵢ ν ⱼ  ∂ ² F           {BILIN:.6f}", ACCENT_C),
          (f"    Δ ² F  /  s ²              {DIFFS[-1][1]:.6f}", WARN)]
  g.add(self._table(rows, x=-3.55, w=5.30, y0=0.06, dy=0.36))
  g.add(self._panel(((0.86, "先沿 μ 求一次方向導數",
                      "take one directional derivative along mu", ACCENT_B),
                     (0.20, "得到的還是一個點的函數，再沿 ν 求一次",
                      "what comes out is again a function of the point, so do it along nu", ACCENT_C),
                     (-0.46, "結果正好是二階微分吃那兩個向量",
                      "and the result is the second differential on those two vectors", ACCENT_A))))
  return g.add(self._foot("三個數字是三種算法：巢狀的方向導數、二階偏導數的雙重求和、以及第 10 拍那個二階差分",
                          "three numbers, three ways: nested directional derivatives, the double sum over the second partials, and beat ten's second difference",
                          ACCENT_A,
                          "順序要注意：先微的是 μ，後微的是 ν，而下標的位置正好反過來",
                          "the order matters: mu is differentiated first and nu second, while the subscripts read the other way"))

 def _evaluation(self):
  g = VGroup()
  rows = (("ev ᵤ  :  Hom ( V , W )  →  W", ACCENT_B),
          ("ev ᵤ ( T )   =   T ( μ )", ACCENT_C),
          ("D ᵤ F   =   ev ᵤ  ∘  dF", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.84 - k * 0.52, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  # the box used to sit at -0.88, whose lower edge touched the first footer line
  g.add(self._rect(-3.55, -0.78, 2.25, 0.22, ACCENT_A),
        self._sym(-0.78, "d ( ev ᵤ  ∘  dF ) ₐ   =   ev ᵤ  ∘  d ( dF ) ₐ", ACCENT_A,
                  FS_TAG - 1, x=-3.55, w=4.30))
  g.add(self._panel(((0.86, "取值映射是有界線性的",
                      "evaluation is bounded and linear", ACCENT_B),
                     (0.20, "所以它的微分就是它自己",
                      "so it is its own differential", ACCENT_C),
                     (-0.46, "方向導數因此是它接上 dF，合成規則就結束了",
                      "the directional derivative is it after dF, and the composite rule finishes", WARN))))
  return g.add(self._foot("整個證明只有這一行：把「沿 μ 求導」看成「先算 dF，再在 μ 取值」",
                          "the whole proof is that one line: reading the derivative along mu as dF followed by evaluation",
                          ACCENT_A,
                          "這是這一章反覆出現的手法——把一個運算拆成一個可微的映射接上一個線性的",
                          "this is the chapter's recurring move: split an operation into a differentiable map and a linear one"))

 def _coords(self):
  g = VGroup()
  gr, _ = self._numgrid(-4.75, 0.36, [[f"{v:.3f}" for v in row] for row in HESS],
                        color=WARN, dx=1.15, dy=0.50, size=FS_TAG - 2)
  g.add(gr, self._sym(-0.40, "∂ ² F / ∂x ⱼ ∂x ᵢ  ( a )", WARN, FS_TAG - 1, x=-4.75, w=2.60))
  g.add(self._sym(0.36, "d ² F ₐ ( b , c )   =   Σ  b ᵢ c ⱼ  ·", ACCENT_C, FS_TAG,
                  x=-1.85, w=3.20))
  g.add(self._panel(((0.86, "二階微分存在，就推出所有二階偏導數存在",
                      "the second differential existing forces all the second partials to", ACCENT_B),
                     (0.20, "而它吃兩個向量的結果是一個雙重求和",
                      "and its value on two vectors is a double sum", ACCENT_C),
                     (-0.46, "所以那個矩陣就是二階微分在座標下的樣子",
                      "so that matrix is the second differential written in coordinates", WARN))))
  return g.add(self._foot("矩陣是程式算的；下一拍會看到它對稱，而那不是巧合",
                          "the matrix was computed here, and the next beats show its symmetry is no accident",
                          ACCENT_A,
                          "這條推論是單向的：從二階微分推出偏導數，反過來要多一個連續的假設",
                          "the corollary runs one way only; the converse needs continuity as an extra hypothesis"))

 def _thm162(self):
  g = VGroup()
  g.add(self._rect(-4.85, 0.46, 1.25, 0.30, ACCENT_B),
        self._sym(0.46, "∂ ² F / ∂x ᵢ ∂x ⱼ   ∃", ACCENT_B, FS_TAG - 1, x=-4.85, w=2.30),
        self._rect(-4.85, -0.30, 1.25, 0.30, ACCENT_C),
        self._sym(-0.30, "∂ ² F / ∂x ᵢ ∂x ⱼ   ∈   C ⁰", ACCENT_C, FS_TAG - 1, x=-4.85, w=2.30))
  g.add(self._arr([-3.45, 0.08, 0], [-3.00, 0.08, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-1.75, 0.08, 1.25, 0.32, WARN),
        self._sym(0.08, "d ² F   ∈   C ⁰ ( A )", WARN, FS_TAG, x=-1.75, w=2.30))
  g.add(self._panel(((0.86, "所有二階偏導數存在而且連續",
                      "all the second partials exist and are continuous", ACCENT_B),
                     (0.20, "那麼二階微分存在，而且連續",
                      "then the second differential exists and is continuous", WARN),
                     (-0.46, "跟第 9 節那條一階的判準是同一個模式",
                      "the same pattern as section 9's test for the first differential", ACCENT_A))))
  return g.add(self._foot("實際判斷「二階可微」時用的就是這一條，因為偏導數是算得出來的東西",
                          "this is the test actually used, because partial derivatives are things one can compute",
                          ACCENT_A,
                          "證明是把第 9 節的定理 9.3 用在每一個一階偏導數上，再引用下一拍那條引理",
                          "the proof applies Theorem 9.3 to each first partial and then quotes the next beat's lemma"))

 def _lemma(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("S ₁  ∘  F", ACCENT_B), ("S ₂  ∘  F", ACCENT_C),
                                  ("S ₖ  ∘  F", WARN))):
   g.add(self._rect(-5.05, 0.62 - k * 0.62, 0.95, 0.24, col),
         self._sym(0.62 - k * 0.62, lab, col, FS_TAG - 1, x=-5.05, w=1.80))
  g.add(self._sym(0.00, "⋮", DIM, FS_TAG, x=-5.05, w=0.60))
  g.add(self._arr([-3.90, 0.00, 0], [-3.35, 0.00, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-2.15, 0.00, 1.05, 0.30, ACCENT_A),
        self._sym(0.00, "F   ∈   C ¹", ACCENT_A, FS_TAG + 1, x=-2.15, w=2.00))
  g.add(self._panel(((0.86, "一組線性映射併起來可逆",
                      "a collection of linear maps that assembles into an invertible one", ACCENT_B),
                     (0.20, "那麼每個分量都可微，就推出 F 可微",
                      "then every component being differentiable makes F so", ACCENT_A),
                     (-0.46, "反過來也對，因為合成保持可微",
                      "and conversely, since composition preserves differentiability", DIM))))
  return g.add(self._foot("兩行就證完：一個方向用定理 8.1，另一個方向把 S 的反元素接回去",
                          "two lines: one direction by Theorem 8.1, the other by composing with the inverse of S",
                          ACCENT_A,
                          "這條引理是「逐分量檢查」這個習慣的根據，而不是它的藉口",
                          "the lemma is what licenses checking one component at a time, rather than an excuse for it"))

 def _third(self):
  g = VGroup()
  rows = (("( D ᵥ ( D ᵤ F ) ) ( · )    =    Σ  b ᵢ c ⱼ   ∂ ² F / ∂x ⱼ ∂x ᵢ  ( · )", ACCENT_B),
          ("( D ₄ D ᵥ D ᵤ F ) ( a )    =    Σ  b ᵢ c ⱼ d ₖ   ∂ ³ F / ∂x ₖ ∂x ⱼ ∂x ᵢ", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.62 - k * 0.72, lab, col, FS_TAG - 2, x=-3.45, w=5.40))
  g.add(self._panel(((0.86, "三階的公式跟二階長得一模一樣",
                      "the third-order formula has exactly the shape of the second", ACCENT_B),
                     (0.20, "只是多一個指標、多一組分量",
                      "with one more index and one more set of components", WARN),
                     (-0.46, "而且三階偏導數連續，就推出二階微分可微",
                      "and continuous third partials make the second differential differentiable", ACCENT_A))))
  return g.add(self._foot("次數沒有上限：每一階都是把上一階的映射再微一次，公式跟著長一個指標",
                          "there is no ceiling: each order differentiates the last map again and the formula grows one index",
                          ACCENT_A,
                          "第 17 節的 Taylor 公式就是把這一串接起來，那是這一章的最後一節",
                          "section 17's Taylor formula strings these together, and it closes the chapter"))

 def _symmetry(self):
  g = VGroup()
  gr, pos = self._numgrid(-4.85, 0.44, [[f"{v:.3f}" for v in row] for row in HESS],
                          color=DIM, dx=1.15, dy=0.50, size=FS_TAG - 2,
                          hot=((0, 1), (1, 0)), hotcolor=WARN)
  g.add(gr)
  g.add(self._sym(-0.28, f"∂ ² F / ∂x ∂y   −   ∂ ² F / ∂y ∂x    =    {SYM_GAP:.1e}",
                  WARN, FS_TAG - 2, x=-4.20, w=4.00))
  g.add(self._sym(0.44, "( d ² F ₐ ( η ) ) ( ξ )   =   ( d ² F ₐ ( ξ ) ) ( η )", ACCENT_A,
                  FS_TAG - 1, x=-1.55, w=3.20))
  g.add(self._panel(((0.86, "兩個混合偏導數相等",
                      "the two mixed partials agree", WARN),
                     (0.20, "而且這不是這個例子的巧合",
                      "and that is not an accident of this example", ACCENT_C),
                     (-0.46, "定理 16.3：二階微分對兩個變數對稱",
                      "Theorem 16.3: the second differential is symmetric", ACCENT_A))))
  return g.add(self._foot("要注意假設：對稱要的是「二階微分存在」，不是「兩個混合偏導數都存在」",
                          "note the hypothesis: symmetry needs the second differential to exist, not merely both mixed partials",
                          ACCENT_A,
                          "這個差別不是吹毛求疵——下一拍那個反例兩個偏導數都在，卻不相等",
                          "the distinction is not pedantic: the next beat's counterexample has both and they differ"))

 def _difference(self):
  cx, cy, s = -4.65, 0.05, 1.05
  g = VGroup()
  corners = ((0.0, 0.0, "+", ACCENT_A), (1.0, 0.0, "−", ACCENT_B),
             (0.35, 0.95, "−", ACCENT_C), (1.35, 0.95, "+", WARN))
  for ux, uy, sg, col in corners:
   px, py = cx + s * ux, cy + s * uy * 0.70
   g.add(Dot([px, py, 0], radius=0.07, color=col),
         self._sym(py + 0.30, sg, col, FS_TAG + 3, x=px, w=0.50))
  for a, b in ((0, 1), (0, 2), (1, 3), (2, 3)):
   pa, pb = corners[a], corners[b]
   g.add(Line([cx + s * pa[0], cy + s * pa[1] * 0.70, 0],
              [cx + s * pb[0], cy + s * pb[1] * 0.70, 0], color=DIM, stroke_width=1.4))
  rows = [(f"  ∂ ² F / ∂y ∂x  ( 0 )        {MIX_YX:+.4f}", ACCENT_B),
          (f"  ∂ ² F / ∂x ∂y  ( 0 )        {MIX_XY:+.4f}", WARN)]
  g.add(self._table(rows, x=PANEL_X, w=PANEL_W, y0=0.86, dy=0.44))
  g.add(self._mid(-0.20, "兩個都存在，可是不相等",
                  "both exist, and they differ", ACCENT_C, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.78, "所以那一點沒有二階微分",
                  "so there is no second differential at that point", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("左邊是二階差分：四個角上的交錯和。把兩個增量對調，圖形原封不動——對稱是看出來的",
                          "on the left is the second difference, an alternating sum over four corners; swapping the increments leaves it unchanged",
                          ACCENT_A,
                          f"右邊是反例的兩個混合偏導數，程式算出來是 {MIX_YX:+.0f} 與 {MIX_XY:+.0f}",
                          f"on the right are the counterexample's mixed partials, computed here as {MIX_YX:+.0f} and {MIX_XY:+.0f}"))

 def stage(self):
  a, b, c = self._dfismap(), self._definition(), self._bilinear()
  d, e, f = self._thm161(), self._evaluation(), self._coords()
  h, i, j = self._thm162(), self._lemma(), self._third()
  k, l = self._symmetry(), self._difference()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE53ZH, AdvCalcE53EN = make(AdvCalcE53Base, "53", prefix="AdvCalcE")
