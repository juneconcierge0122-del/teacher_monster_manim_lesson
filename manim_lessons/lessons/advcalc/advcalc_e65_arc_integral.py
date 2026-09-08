"""advcalc E65 -- chapter 4, section 10 (book pp. 236-238): the integral of a
parametrized arc.

This is the chapter's last use of completeness.  A very general extension
theorem comes first (10.1: a bounded linear map on a subspace extends uniquely
to its closure, with the same norm), and then the Riemann integral is built by
applying it: the integral is obvious for step functions, that map is bounded by
the length of the interval, the continuous functions lie in the closure of the
step functions (Lemma 10.1, which is where uniform continuity comes back), and
Theorem 10.2 collects the result.  Additivity and the fundamental theorem of
calculus (10.3) follow.  The book is explicit about why this waited until now:
the completeness of W is what proves the integral exists at all.

Section 10's content ends on book page 238; 239 to 240 are exercises 10.1 to
10.15, and section 11 begins on 240.  The OUTLINE lists the section as 236-240,
counting the exercise pages -- the seventh time that column has done so.

One concrete arc runs through the whole episode: f(t) = <cos t, sin t> on the
interval from zero to pi over two, whose integral is exactly <1, 1>.  The
Riemann sums are summed and their errors measured, the bound of beat 6 is
checked against the measured norm, the step-function approximation of beat 7 is
measured against the mesh, additivity is checked as an actual vector addition,
and the difference quotient of beat 10 is evaluated at three step sizes.
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

# ── the one arc the whole episode runs on ──────────────────────────────
A, Bb = 0.0, math.pi / 2


def arc(t):
 return math.cos(t), math.sin(t)


def prim(t):
 """The exact integral from A to t, so the errors below are real errors."""
 return math.sin(t) - math.sin(A), -math.cos(t) + math.cos(A)


EXACT = prim(Bb)
assert abs(EXACT[0] - 1.0) < 1e-15 and abs(EXACT[1] - 1.0) < 1e-15, \
    "the integral of this arc is exactly one and one"


def riemann(n, lo=A, hi=Bb):
 h = (hi - lo) / n
 sx = sy = 0.0
 for k in range(n):
  cx, cy = arc(lo + k * h)
  sx += cx * h
  sy += cy * h
 return sx, sy


SUMS = [(n, riemann(n)) for n in (4, 8, 16, 32)]
SUM_ERR = [(n, math.hypot(s[0] - EXACT[0], s[1] - EXACT[1])) for n, s in SUMS]
for (_n0, _e0), (_n1, _e1) in zip(SUM_ERR, SUM_ERR[1:]):
 assert _e1 < _e0, "refining the partition brings the sum closer"
assert SUM_ERR[-1][1] < 0.06, "and it is visibly converging by the last one"

# ── beat 6: the bound, measured ────────────────────────────────────────
SUP = max(math.hypot(*arc(A + (Bb - A) * k / 2000)) for k in range(2001))
NORM_INT = math.hypot(*EXACT)
LENGTH = Bb - A
assert abs(SUP - 1.0) < 1e-12, "the arc lies on the unit circle, so its sup is one"
assert NORM_INT <= SUP * LENGTH + 1e-12, "which is the bound the theorem gives"
assert NORM_INT > 0.85 * SUP * LENGTH, "and here the bound is not far off"

# ── beats 4 and 5: a step function, and one added point ────────────────
CUTS = (0.0, 0.3, 0.7, 1.0)
VALS = ((1.0, 0.5), (0.0, 2.0), (-1.0, 1.0))


def _clean(v):
 """Round a rounding-error-sized value to a true zero, so it prints as 0.0."""
 return 0.0 if abs(v) < 1e-12 else v


STEP_SUM = (_clean(sum(v[0] * (CUTS[i + 1] - CUTS[i]) for i, v in enumerate(VALS))),
            _clean(sum(v[1] * (CUTS[i + 1] - CUTS[i]) for i, v in enumerate(VALS))))
# the same function described by a finer partition: 0.5 splits the middle piece
FINE_CUTS = (0.0, 0.3, 0.5, 0.7, 1.0)
FINE_VALS = (VALS[0], VALS[1], VALS[1], VALS[2])
FINE_SUM = (_clean(sum(v[0] * (FINE_CUTS[i + 1] - FINE_CUTS[i])
                       for i, v in enumerate(FINE_VALS))),
            _clean(sum(v[1] * (FINE_CUTS[i + 1] - FINE_CUTS[i])
                       for i, v in enumerate(FINE_VALS))))
assert abs(STEP_SUM[0] - FINE_SUM[0]) < 1e-15 and abs(STEP_SUM[1] - FINE_SUM[1]) < 1e-15, \
    "adding a point splits one term into two that add back to it"

# ── beat 7: how close a step function gets, against the mesh ───────────
def step_gap(n):
 """Sup distance from the arc to the step function that samples it left-to-right."""
 h = (Bb - A) / n
 worst = 0.0
 for k in range(n):
  lo = A + k * h
  ax, ay = arc(lo)
  for j in range(41):
   t = lo + h * j / 40
   bx, by = arc(t)
   worst = max(worst, math.hypot(bx - ax, by - ay))
 return h, worst


GAPS = [(n,) + step_gap(n) for n in (4, 8, 16)]
for _n, _h, _g in GAPS:
 # the arc has unit speed, so the sup distance cannot exceed the mesh
 assert _g <= _h + 1e-12, "the mesh bounds the uniform distance, by unit speed"
assert GAPS[-1][2] < 0.10, "so a fine enough partition gets within any epsilon"

# ── beat 9: additivity, as an actual vector addition ───────────────────
CMID = math.pi / 4
LEFT = prim(CMID)
RIGHT = (EXACT[0] - LEFT[0], EXACT[1] - LEFT[1])
assert abs(LEFT[0] + RIGHT[0] - EXACT[0]) < 1e-15, "the two halves add to the whole"
assert abs(LEFT[1] + RIGHT[1] - EXACT[1]) < 1e-15, "in both components"
assert abs(LEFT[0] - 0.7071067811865476) < 1e-12, "the split is at forty five degrees"

# ── beat 10: the difference quotient, at three step sizes ──────────────
XSTAR = 0.6
FSTAR = arc(XSTAR)
QUOT = []
for _h in (0.1, 0.01, 0.001):
 _p1, _p2 = prim(XSTAR + _h), prim(XSTAR)
 _q = ((_p1[0] - _p2[0]) / _h, (_p1[1] - _p2[1]) / _h)
 QUOT.append((_h, math.hypot(_q[0] - FSTAR[0], _q[1] - FSTAR[1])))
for (_h0, _e0), (_h1, _e1) in zip(QUOT, QUOT[1:]):
 assert _e1 < _e0 / 5, "the quotient closes in on the value of f, and fast"
assert QUOT[-1][1] < 1e-3, "so F really is differentiable with derivative f"


class AdvCalcE65Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 65

 MODE_LABEL = {
  0: {"zh": "完備性的最後一個應用", "en": "the last application of completeness"},
  1: {"zh": "定理 10.1：延拓到閉包", "en": "Theorem 10.1: extending to the closure"},
  2: {"zh": "證明：Cauchy 送過去還是 Cauchy", "en": "the proof: Cauchy goes to Cauchy"},
  3: {"zh": "為什麼範數不會變", "en": "why the norm does not change"},
  4: {"zh": "分割與階梯函數", "en": "partitions and step functions"},
  5: {"zh": "跟用哪個分割無關", "en": "independent of the partition used"},
  6: {"zh": "積分是有界線性映射", "en": "integration is a bounded linear map"},
  7: {"zh": "引理 10.1：連續函數在閉包裡", "en": "Lemma 10.1: the continuous ones are in the closure"},
  8: {"zh": "定理 10.2：把前面重述一次", "en": "Theorem 10.2: the recapitulation"},
  9: {"zh": "可加性，就是一個向量加法", "en": "additivity is a vector addition"},
  10: {"zh": "定理 10.3：基本定理還在", "en": "Theorem 10.3: the fundamental theorem survives"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.32, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _arcplot(self, cx, cy, r, col, sw=2.6, lo=A, hi=Bb):
  return self._curve([[cx + r * math.cos(lo + (hi - lo) * k / 90),
                       cy + r * math.sin(lo + (hi - lo) * k / 90), 0]
                      for k in range(91)], col, sw=sw)

 def _staircase(self, ox, oy, sx, sy, cuts, vals, col, sw=2.4, comp=1):
  g = VGroup()
  for i, v in enumerate(vals):
   x0 = ox + sx * cuts[i]
   x1 = ox + sx * cuts[i + 1]
   yy = oy + sy * v[comp]
   g.add(Line([x0, yy, 0], [x1, yy, 0], color=col, stroke_width=sw))
   if i:
    g.add(Line([x0, oy + sy * vals[i - 1][comp], 0], [x0, yy, 0],
               color=col, stroke_width=1.2))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _opening(self):
  cx, cy = -3.95, -0.45
  r = 1.30
  g = VGroup(Line([cx - 0.20, cy, 0], [cx + r * 1.35, cy, 0], color=DIM, stroke_width=1.3),
             Line([cx, cy - 0.20, 0], [cx, cy + r * 1.30, 0], color=DIM, stroke_width=1.3))
  g.add(self._arcplot(cx, cy, r, ACCENT_B))
  g.add(self._arr([cx, cy, 0], [cx + r * 0.72 * EXACT[0], cy + r * 0.72 * EXACT[1], 0],
                  ACCENT_A, sw=3.0, tl=0.16))
  g.add(self._sym(cy + r * 0.72 * EXACT[1] + 0.24,
                  f"⟨ {EXACT[0]:.0f} , {EXACT[1]:.0f} ⟩", ACCENT_A, FS_TAG - 1,
                  x=cx + r * 0.72 * EXACT[0] + 0.30, w=1.60))
  g.add(self._panel(((0.86, "積分對階梯函數是顯然的",
                      "the integral is obvious for a step function", ACCENT_B),
                     (0.20, "要的是把它延拓到連續函數上",
                      "what is wanted is to extend it to the continuous ones", ACCENT_C),
                     (-0.46, "而證明積分存在，非用完備性不可",
                      "and proving the integral exists is what needs completeness", WARN))))
  return g.add(self._foot("書上說得很直白：之所以拖到現在才做積分，就是因為要等完備性",
                          "the book is blunt about it: the integral waited until now precisely because it needs completeness",
                          ACCENT_A,
                          "整集用同一段弧：cos t 與 sin t，從零積到二分之 π，答案剛好是 ⟨ 1 , 1 ⟩",
                          "one arc runs through the whole episode: cosine and sine, integrated from zero to pi over two, and the answer is exactly one and one"))

 def _thm101(self):
  g = VGroup()
  g.add(self._rect(-4.60, 0.56, 1.55, 0.72, DIM, sw=1.6),
        self._sym(1.06, "U ‾", DIM, FS_TAG, x=-4.60, w=1.20))
  g.add(self._rect(-4.60, 0.36, 0.85, 0.30, ACCENT_B, sw=2.0),
        self._sym(0.36, "U", ACCENT_B, FS_TAG, x=-4.60, w=1.00))
  g.add(self._rect(-1.30, 0.46, 0.80, 0.42, WARN, sw=2.0),
        self._sym(0.46, "W", WARN, FS_TAG, x=-1.30, w=1.00))
  g.add(self._arr([-3.70, 0.36, 0], [-2.16, 0.36, 0], ACCENT_B, sw=2.2, tl=0.12),
        self._sym(0.16, "T", ACCENT_B, FS_TAG - 1, x=-2.95, w=0.70))
  g.add(self._arr([-3.02, 0.90, 0], [-2.16, 0.66, 0], ACCENT_A, sw=2.2, tl=0.12),
        self._sym(1.02, "S", ACCENT_A, FS_TAG - 1, x=-2.70, w=0.70))
  g.add(self._panel(((0.86, "T 只定義在子空間 U 上",
                      "T is only defined on the subspace U", ACCENT_B),
                     (0.20, "S 定義在整個閉包上，而且唯一",
                      "S is defined on the whole closure, and is unique", ACCENT_A),
                     (-0.46, "W 完備是延拓存在的理由",
                      "the completeness of W is why the extension exists", WARN))))
  return g.add(self._foot("這條定理本身跟積分無關——它是一條關於「有界線性映射能走多遠」的一般結果",
                          "the theorem has nothing to do with integrals: it is a general result about how far a bounded linear map reaches",
                          ACCENT_A,
                          "而且延拓後範數一模一樣，一點也沒有變大",
                          "and the extension has exactly the same norm, with nothing lost or gained"))

 def _proof(self):
  ox = -5.70
  g = VGroup()
  for oy, lab, col in ((0.72, "ξ ₙ   →   α", ACCENT_B), (-0.10, "T ( ξ ₙ )   →   β", WARN)):
   g.add(Line([ox, oy, 0], [ox + 4.20, oy, 0], color=DIM, stroke_width=1.5))
   for i in range(7):
    px = ox + 4.20 * (0.08 + 0.80 * (1.0 - 1.0 / (i + 1.5)))
    g.add(Dot([px, oy, 0], radius=0.05, color=col))
   g.add(Dot([ox + 4.20 * 0.90, oy, 0], radius=0.075, color=ACCENT_A),
         self._sym(oy + 0.30, lab, col, FS_TAG - 1, x=ox + 1.50, w=2.20))
  g.add(self._arr([ox + 2.10, 0.52, 0], [ox + 2.10, 0.12, 0], ACCENT_C, sw=2.2, tl=0.11),
        self._sym(0.32, "T", ACCENT_C, FS_TAG - 1, x=ox + 2.40, w=0.70))
  g.add(self._mid(-0.62, "上面 Cauchy，下面也 Cauchy",
                  "Cauchy above forces Cauchy below", ACCENT_C,
                  FS_TAG, x=ox + 2.10, w=4.60))
  g.add(self._panel(((0.86, "收斂的序列一定是 Cauchy 的",
                      "a convergent sequence is Cauchy", ACCENT_B),
                     (0.20, "有界線性映射把 Cauchy 送成 Cauchy",
                      "a bounded linear map carries Cauchy to Cauchy", ACCENT_C),
                     (-0.46, "W 完備，所以那個極限真的存在",
                      "W is complete, so that limit really exists", WARN))))
  return g.add(self._foot("換一個收斂到 α 的序列會得到同一個 β——所以這個值只跟 α 有關，不跟序列有關",
                          "a second sequence converging to alpha gives the same beta, so the value depends on alpha alone and not on the sequence",
                          ACCENT_A,
                          "用到的是第 7 節的引理 7.1 與 7.3——這一章前面鋪的每一塊都在這裡派上用場",
                          "what is used is Lemmas 7.1 and 7.3 of section 7: every piece laid earlier in the chapter is spent here"))

 def _norms(self):
  g = VGroup()
  rows = (("‖ S ( α ) ‖    =    lim  ‖ T ( ξ ₙ ) ‖", ACCENT_B),
          ("≤    ‖ T ‖  ·  lim ‖ ξ ₙ ‖    =    ‖ T ‖ ‖ α ‖", ACCENT_C),
          ("⇒          ‖ S ‖    ≤    ‖ T ‖", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.54, lab, col, FS_TAG, x=-3.40, w=5.40))
  g.add(self._dash([-5.90, -0.62, 0], [-0.90, -0.62, 0], DIM, n=24, sw=1.2))
  g.add(self._sym(-0.94, "S   ⊃   T          ⇒          ‖ S ‖   =   ‖ T ‖", ACCENT_A,
                  FS_TAG + 1, x=-3.40, w=5.40))
  g.add(self._panel(((0.86, "一邊：延拓的範數被 T 的範數界住",
                      "one way: T bounds the norm of the extension", ACCENT_B),
                     (0.20, "另一邊：延拓本來就包含 T",
                      "the other way: the extension already contains T", ACCENT_C),
                     (-0.46, "兩邊夾起來，只能相等",
                      "squeezed from both sides, they can only be equal", WARN))))
  return g.add(self._foot("延拓不會讓範數變大，也不會讓它變小——這一點之後量積分的界時就會用到",
                          "extending can neither raise nor lower the norm, which is what the bound on the integral will lean on",
                          ACCENT_A,
                          "書上把這條寫成一般的定理，是因為它跟積分完全無關，值得單獨記住",
                          "the book states it as a general theorem because it has nothing to do with integrals and is worth remembering alone"))

 def _partition(self):
  ox, oy = -5.70, -0.30
  sx, sy = 4.30, 0.42
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._staircase(ox, oy, sx, sy, CUTS, VALS, ACCENT_B, sw=2.6))
  for c in CUTS:
   px = ox + sx * c
   g.add(self._dash([px, oy - 0.52, 0], [px, oy + 0.92, 0], DIM, n=7, sw=1.0),
         Dot([px, oy, 0], radius=0.055, color=WARN))
   g.add(self._sym(oy - 0.72, f"{c:.1f}", DIM, FS_TAG - 3, x=px, w=0.60))
  g.add(self._table((("     A  =  { t ᵢ } ₀ ⁿ", DIM),
                     (f"     α ₁  =  ⟨ {VALS[0][0]:.1f} , {VALS[0][1]:.1f} ⟩", ACCENT_B),
                     (f"     α ₂  =  ⟨ {VALS[1][0]:.1f} , {VALS[1][1]:.1f} ⟩", ACCENT_C),
                     (f"     α ₃  =  ⟨ {VALS[2][0]:.1f} , {VALS[2][1]:.1f} ⟩", WARN)),
                    y0=0.84, dy=0.38))
  g.add(self._mid(-0.78, "畫的是第二個分量；值是 ℝ ² 裡的向量",
                  "the second component is drawn; the values are vectors in the plane",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("分割就是一個含兩端點的有限點集；階梯函數在那些開區間上是常數",
                          "a partition is a finite set of points containing both ends, and a step function is constant on its open intervals",
                          ACCENT_A,
                          "分點本身的值可以是任何東西——那幾個點在積分裡佔的長度是零",
                          "the values at the dividing points may be anything at all: those points carry no length in the integral"))

 def _refine(self):
  ox, oy = -5.70, -0.20
  sx, sy = 4.30, 0.40
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._staircase(ox, oy, sx, sy, CUTS, VALS, ACCENT_B, sw=2.6))
  px = ox + sx * 0.5
  g.add(self._dash([px, oy - 0.30, 0], [px, oy + 1.00, 0], WARN, n=8, sw=1.4),
        Dot([px, oy + sy * VALS[1][1], 0], radius=0.06, color=WARN))
  g.add(self._sym(oy + 1.14, "s", WARN, FS_TAG - 1, x=px, w=0.50))
  g.add(self._table((("     α ( t ᵢ − s )  +  α ( s − t ᵢ ₋ ₁ )", DIM),
                     ("     =      α ( t ᵢ − t ᵢ ₋ ₁ )", ACCENT_A),
                     (f"     Σ  =  ⟨ {STEP_SUM[0]:.2f} , {STEP_SUM[1]:.2f} ⟩", ACCENT_B),
                     (f"     Σ ′  =  ⟨ {FINE_SUM[0]:.2f} , {FINE_SUM[1]:.2f} ⟩", WARN)),
                    y0=0.84, dy=0.38))
  g.add(self._mid(-0.78, "加一個點，和一點也沒變",
                  "one point added, and the sum does not move", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("加一個點會把一項拆成兩項，可是那兩項加回去還是原來那一項",
                          "adding a point splits one term into two, and those two add back to the term they came from",
                          ACCENT_A,
                          "任意兩個分割就透過它們的共同細分來比——一次加一個點走過去",
                          "any two partitions are then compared through their common refinement, one added point at a time"))

 def _bounded(self):
  ox, oy = -5.60, 0.30
  sx = 4.20
  g = VGroup()
  scale = sx / (SUP * LENGTH)
  g.add(Line([ox, oy + 0.34, 0], [ox + scale * NORM_INT, oy + 0.34, 0],
             color=ACCENT_B, stroke_width=7),
        Line([ox, oy - 0.24, 0], [ox + scale * SUP * LENGTH, oy - 0.24, 0],
             color=WARN, stroke_width=7))
  g.add(self._sym(oy + 0.66, f"‖ ∫ f ‖  =  {NORM_INT:.4f}", ACCENT_B, FS_TAG - 1,
                  x=ox + 1.55, w=2.80),
        self._sym(oy - 0.56, f"‖ f ‖ ∞ ( b − a )  =  {SUP * LENGTH:.4f}", WARN,
                  FS_TAG - 1, x=ox + 1.95, w=3.60))
  g.add(self._panel(((0.86, "階梯函數構成向量空間，積分在上面是線性的",
                      "the step functions form a vector space and integration is linear on it",
                      ACCENT_B),
                     (0.20, "而且被區間長度界住",
                      "and it is bounded by the length of the interval", ACCENT_C),
                     (-0.46, "所以定理 10.1 用得上了",
                      "which is exactly what lets Theorem 10.1 be applied", WARN))))
  return g.add(self._foot("這個界就是延拓後的範數上界：積分作為線性映射，範數不超過 b 減 a",
                          "that bound becomes the norm of the extension: as a linear map, integration has norm at most b minus a",
                          ACCENT_A,
                          "畫面上這一段弧的比值是 1.4142 比 1.5708——界是真的，而且不算鬆",
                          "for the arc on screen the two numbers are 1.4142 against 1.5708, so the bound is true and not far off"))

 def _lemma101(self):
  ox, oy = -5.70, -0.62
  sx, sy = 4.20, 1.55
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._curve([[ox + sx * k / 120, oy + sy * arc(A + (Bb - A) * k / 120)[0], 0]
                     for k in range(121)], ACCENT_B, sw=2.6))
  n = 6
  for k in range(n):
   lo = A + (Bb - A) * k / n
   yy = oy + sy * arc(lo)[0]
   g.add(Line([ox + sx * k / n, yy, 0], [ox + sx * (k + 1) / n, yy, 0],
              color=WARN, stroke_width=2.2))
  g.add(self._table((("       n           h            ‖ f − g ‖ ∞", DIM),)
                    + tuple((f"     {nn:4d}       {h:.4f}          {gp:.4f}", ACCENT_C)
                            for nn, h, gp in GAPS), y0=0.86, dy=0.32))
  g.add(self._mid(-0.86, "一致距離永遠不超過網目——因為這段弧的速率是一",
                  "the uniform distance never exceeds the mesh, because this arc has unit speed",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("閉區間上的連續函數均勻連續（定理 5.1），所以分割夠細就壓得到 ε 以內",
                          "a continuous function on a closed interval is uniformly continuous by Theorem 5.1, so a fine enough partition gets under any epsilon",
                          ACCENT_A,
                          "緊緻性在這裡回來了——第 5 節那條定理正是這一步的全部理由",
                          "compactness comes back here: that theorem of section 5 is the entire reason this step works"))

 def _thm102(self):
  ox, oy = -5.85, -0.80
  sx, sy = 4.10, 1.85
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.06, 0], color=DIM, stroke_width=1.4))
  lo = math.log10(SUM_ERR[-1][1]) - 0.5
  hi = math.log10(SUM_ERR[0][1])
  pts = []
  for k, (n, e) in enumerate(SUM_ERR):
   px = ox + sx * k / (len(SUM_ERR) - 1)
   py = oy + sy * (math.log10(e) - lo) / (hi - lo)
   pts.append([px, py, 0])
   g.add(Dot([px, py, 0], radius=0.06, color=ACCENT_C))
  g.add(self._curve(pts, ACCENT_C, sw=2.0))
  g.add(self._sym(oy + sy * 1.00, "‖ Σ ₙ  −  ∫ f ‖", ACCENT_A, FS_TAG - 1,
                  x=ox + 3.10, w=2.20))
  g.add(self._table((("       n          ‖ Σ ₙ  −  ∫ f ‖", DIM),)
                    + tuple((f"     {n:4d}              {e:.4f}", ACCENT_C)
                            for n, e in SUM_ERR), y0=0.86, dy=0.32))
  g.add(self._mid(-0.86, "任何一列收斂到 f 的階梯函數都給同一個極限",
                  "any sequence of step functions converging to f gives the same limit",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 10.2 只是把前面幾步接起來：延拓存在、唯一，而且範數不超過 b 減 a",
                          "Theorem 10.2 just joins the previous steps: the extension exists, is unique, and has norm at most b minus a",
                          ACCENT_A,
                          "畫面上的誤差是真的算出來的：四段、八段、十六段、三十二段的和對上精確值",
                          "the errors on screen are really computed: sums over four, eight, sixteen and thirty-two pieces against the exact value"))

 def _additive(self):
  cx, cy = -3.80, -0.55
  s = 1.55
  g = VGroup(Line([cx - 0.25, cy, 0], [cx + s * 1.35, cy, 0], color=DIM, stroke_width=1.3),
             Line([cx, cy - 0.25, 0], [cx, cy + s * 1.14, 0], color=DIM, stroke_width=1.3))
  g.add(self._arr([cx, cy, 0], [cx + s * LEFT[0], cy + s * LEFT[1], 0],
                  ACCENT_B, sw=2.6, tl=0.14))
  g.add(self._arr([cx + s * LEFT[0], cy + s * LEFT[1], 0],
                  [cx + s * EXACT[0], cy + s * EXACT[1], 0], WARN, sw=2.6, tl=0.14))
  g.add(self._arr([cx, cy, 0], [cx + s * EXACT[0], cy + s * EXACT[1], 0],
                  ACCENT_A, sw=2.0, tl=0.14))
  g.add(self._table((("       ∫ ₐ ᶜ            ∫ ᶜ ᵇ            ∫ ₐ ᵇ", DIM),
                     (f"    {LEFT[0]:.4f}       {RIGHT[0]:.4f}       {EXACT[0]:.4f}", ACCENT_B),
                     (f"    {LEFT[1]:.4f}       {RIGHT[1]:.4f}       {EXACT[1]:.4f}", WARN)),
                    y0=0.84, dy=0.38))
  g.add(self._mid(-0.60, "青色加紅色，剛好是橘色",
                  "the teal one plus the red one is exactly the orange one", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("對階梯函數而言，把和在中間某一點拆開是顯然的；對連續函數就跟著極限傳過去",
                          "for a step function, splitting the sum at an interior point is immediate, and for a continuous one the identity passes to the limit",
                          ACCENT_A,
                          "切點取在四十五度，兩段的分量分別是 0.7071 與 0.2929，加起來是一",
                          "the split is at forty five degrees, where the components are 0.7071 and 0.2929 and add to one"))

 def _ftc(self):
  ox, oy = -5.70, -0.50
  sx, sy = 4.20, 1.20
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._curve([[ox + sx * k / 120, oy + sy * prim(A + (Bb - A) * k / 120)[0], 0]
                     for k in range(121)], ACCENT_B, sw=2.4))
  g.add(self._curve([[ox + sx * k / 120, oy + sy * arc(A + (Bb - A) * k / 120)[0], 0]
                     for k in range(121)], WARN, sw=2.0))
  px = ox + sx * (XSTAR - A) / (Bb - A)
  g.add(self._dash([px, oy, 0], [px, oy + sy * 1.05, 0], DIM, n=8, sw=1.1),
        Dot([px, oy + sy * prim(XSTAR)[0], 0], radius=0.06, color=ACCENT_B),
        Dot([px, oy + sy * arc(XSTAR)[0], 0], radius=0.06, color=WARN))
  g.add(self._table((("       h        ‖ ΔF / h  −  f ‖", DIM),)
                    + tuple((f"     {h:.3f}            {e:.6f}", ACCENT_C)
                            for h, e in QUOT), y0=0.86, dy=0.34))
  g.add(self._mid(-0.80, "青色是 F，紅色是 f——F 的斜率就是 f 的高度",
                  "teal is F and red is f: the slope of F is the height of f", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("證明只有一步：f 在那一點連續，所以差商與 f 的差不超過 ε",
                          "the proof is one step: f is continuous at the point, so the difference quotient differs from it by at most epsilon",
                          ACCENT_A,
                          "第 4 章到此結束——完備性從 Cauchy 序列一路鋪到這裡，最後造出了積分",
                          "that ends chapter 4: completeness ran from Cauchy sequences all the way here, and built the integral at the end"))

 def stage(self):
  a, b, c = self._opening(), self._thm101(), self._proof()
  d, e, f = self._norms(), self._partition(), self._refine()
  h, i, j = self._bounded(), self._lemma101(), self._thm102()
  k, l = self._additive(), self._ftc()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE65ZH, AdvCalcE65EN = make(AdvCalcE65Base, "65", prefix="AdvCalcE")
