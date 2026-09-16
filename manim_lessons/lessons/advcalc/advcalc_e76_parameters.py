"""advcalc E76 -- chapter 6, section 2 (book pp. 274-275): differentiable
dependence on parameters.  The whole section in one episode, and it has no
exercises at all.

Sections 1 asked whether a solution exists and how far it runs.  This one asks
how it *moves* when the initial point moves.  Fix J and the ball in the function
space, and the initial point determines a solution, so there is a map from a
neighbourhood of the initial point into the function space.  Theorem 2.1 says it
is continuous; Theorem 2.2 says that if dF is uniformly continuous it is
continuously differentiable.

Neither proof is new work.  K just takes two more arguments -- the initial time
and value -- and the same two estimates run again, except that taking N to be
the ball of half the radius eats half the room: the double requirement becomes
delta < r/(2(m + cr)), exactly half of section 1's ceiling.  That is the whole
price of continuous dependence.  Then chapter 4's fixed-point theorem with a
parameter (9.2) gives continuity and its differentiable version (9.4) gives
differentiability, provided K itself is continuously differentiable, which comes
from chapter 3's Theorems 14.3 and 8.3 once the three partial differentials of K
are in hand -- and two of the three are computed outright: dK^2 is the identity
and dK^1(h) is -h F(t_1, f(t_1)).

Everything is checked on the one initial-value problem in this chapter whose
solution map has a closed form:

    x' = t + x  through  <t_1, a_1>   gives   f(t) = (a_1 + t_1 + 1) e^(t-t_1) - t - 1

so the corollary's derivative of f(s) with respect to the initial value is
exp(s - t_1) on the nose, and the fan of solutions spreads at exactly that rate.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20


def simpson(g, a, b, n=400):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


# ── the one problem in this chapter with a closed-form solution map ───
def F(t, x):
 return t + x


def sol(t1, a1):
 """the solution through <t1, a1>, in closed form."""
 return lambda t: (a1 + t1 + 1.0) * math.exp(t - t1) - t - 1.0


for _t1, _a1 in ((0.0, 0.0), (0.5, 0.3), (-0.4, 1.2)):
 _f = sol(_t1, _a1)
 assert abs(_f(_t1) - _a1) < 1e-12, "it passes through the point it should"
 for _t in (_t1 - 0.3, _t1 + 0.2, _t1 + 0.9):
  _d = (_f(_t + 1e-6) - _f(_t - 1e-6)) / 2e-6
  assert abs(_d - F(_t, _f(_t))) < 1e-5, "and it solves the equation"

# ── beats 3 and 4: the delta that continuous dependence costs ─────────
# the same ball as E74 and E75: F = 1 + x^2 about the origin with r = 1
R, M_BD, C_SUP = 1.0, 2.0, 2.0
D_ONE = R / (M_BD + C_SUP * R)
D_TWO = R / (2.0 * (M_BD + C_SUP * R))
assert abs(D_ONE - 0.25) < 1e-12 and abs(D_TWO - 0.125) < 1e-12
assert abs(D_TWO - D_ONE / 2.0) < 1e-15, "exactly half, which is the point of the beat"
# and it is what the double requirement r/2 + delta*m < (1 - delta*c) r gives
_lhs = lambda d: R / 2.0 + d * M_BD
_rhs = lambda d: (1.0 - d * C_SUP) * R
assert _lhs(D_TWO) == _rhs(D_TWO), "the two sides meet exactly at the new ceiling"
assert _lhs(D_TWO * 0.9) < _rhs(D_TWO * 0.9) and _lhs(D_ONE) > _rhs(D_ONE), \
    "satisfied below it and violated at the old one"
STEP = [(d, _lhs(d), _rhs(d)) for d in (0.02, 0.06, 0.10, 0.125, 0.20, 0.25)]

# ── beat 9: the partial differential in the initial time ──────────────
T1P, A1P = 0.5, 0.3
FP = sol(T1P, A1P)
DK1 = -F(T1P, FP(T1P))
assert abs(DK1 + 0.8) < 1e-12, "minus F at the initial point, which here is -0.8"
DK1_NUM = []
for _h in (1e-2, 1e-3, 1e-4):
 _inc = -simpson(lambda s: F(s, FP(s)), T1P, T1P + _h, 20)
 DK1_NUM.append((_h, _inc / _h))
assert all(abs(q - DK1) < 1e-2 for _h, q in DK1_NUM), "the quotient is that number"
assert abs(DK1_NUM[-1][1] - DK1) < abs(DK1_NUM[0][1] - DK1), "and closes in as h shrinks"

# ── beats 10 and 0: the solution fan, spreading at exp(s - t1) ────────
S_EVAL = 1.0
FAN = (-0.6, -0.3, 0.0, 0.3, 0.6)
DFDA = math.exp(S_EVAL - 0.0)
SPREAD = []
for _e in (1e-1, 1e-2, 1e-3, 1e-4):
 _q = (sol(0.0, _e)(S_EVAL) - sol(0.0, 0.0)(S_EVAL)) / _e
 SPREAD.append((_e, _q))
assert all(abs(q - DFDA) < 1e-9 for _e, q in SPREAD), \
    "the map is affine in the initial value, so the quotient is exp(s) exactly"
assert abs(DFDA - math.e) < 1e-12, "and at s = 1 it is e"
GROW = [(s, math.exp(s)) for s in (0.0, 0.5, 1.0, 1.5)]
assert GROW[0][1] < GROW[-1][1], "the fan opens as s grows"


class AdvCalcE76Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 76

 MODE_LABEL = {
  0: {"zh": "解怎麼隨初始點變", "en": "how the solution moves with the point"},
  1: {"zh": "定理 2.1", "en": "theorem 2.1"},
  2: {"zh": "K 多吃兩個變數", "en": "K takes two more arguments"},
  3: {"zh": "N 取半徑的一半", "en": "N is the ball of half the radius"},
  4: {"zh": "代價：δ 砍半", "en": "the price: delta halves"},
  5: {"zh": "套第 4 章定理 9.2", "en": "chapter 4's theorem 9.2"},
  6: {"zh": "要可微就要更多", "en": "differentiability asks for more"},
  7: {"zh": "定理 2.2", "en": "theorem 2.2"},
  8: {"zh": "把 K 拆成兩步複合", "en": "K as a composition"},
  9: {"zh": "三個偏微分", "en": "the three partial differentials"},
  10: {"zh": "推論，與第 2 節的結束", "en": "the corollary, and the end of section 2"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.90, dy=0.30, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _cap(self, zh, en):
  return self._mid(-0.90, zh, en, ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W)

 def _frame(self, ox, oy, w, h, down=0.30, back=0.12):
  return VGroup(Line([ox - back, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=1.0, sw=2.4, n=140):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _legend(self, x, rows, y0=1.14, dy=0.27):
  g = VGroup()
  for k, (col, lab, w) in enumerate(rows):
   y = y0 - k * dy
   g.add(Line([x, y, 0], [x + 0.24, y, 0], color=col, stroke_width=6.0),
         self._sym(y, lab, col, FS_TAG - 3, x=x + 0.36 + w / 2, w=w))
  return g

 def _fan(self, ox, oy, sx, sy, t1=1.55, sw=2.6):
  """the solutions through <0, a> for a spread of a: the object of the section."""
  g = VGroup()
  for a, col in zip(FAN, (DIM, ACCENT_C, ACCENT_A, ACCENT_B, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy, sol(0.0, a), col, t0=0.0, t1=t1, sw=sw))
   g.add(Dot([ox, oy + sy * a, 0], radius=0.050, color=col))
  return g

 # ── beat 0: the map whose continuity is the question ──────────────
 def _question(self):
  ox, oy, sx, sy = -5.95, -0.24, 1.90, 0.30
  g = VGroup(self._arr([ox - 0.14, oy - sy * 0.9, 0], [ox + 3.42, oy - sy * 0.9, 0],
                       DIM, sw=3, tl=0.14),
             Line([ox, oy - sy * 1.1, 0], [ox, oy + 1.18, 0], color=DIM, stroke_width=1.3))
  g.add(self._fan(ox, oy, sx, sy))
  g.add(self._dash([ox, oy + sy * FAN[0], 0], [ox, oy + sy * FAN[-1], 0], INK, n=6, sw=2.6))
  g.add(self._sym(oy + sy * FAN[-1] + 0.26, "N", INK, FS_TAG - 3, x=ox + 0.30, w=0.40))
  g.add(self._table((("⟨ t ₁ , α ₁ ⟩      ↦      f", ACCENT_A),
                     ("J × N     →     V", ACCENT_B),
                     ("V   =   ℬ 𝒞 ( J , W )", ACCENT_C),
                     ("𝔘   =   B ᵣ ( ᾱ ₀ )   ⊂   V", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("整節問的就是第一列那個箭頭有多好",
                  "the whole section is about how good that first arrow is"))
  return g.add(self._foot("第 1 節問解存不存在、活多遠；第 2 節問它怎麼動。把初始點送到它決定的那條解，就得到一個從 J 乘 N 到函數空間 V 的映射",
                          "section 1 asked whether a solution exists and how far it runs; this one asks how it moves, through the map sending an initial point to the solution it determines",
                          ACCENT_A,
                          "畫面上五條就是通過五個不同初始值的解。它們看起來很乖，可是「初始點動一點、整條解只動一點」這件事要證，而且能證到可微",
                          "the five curves are the solutions through five initial values; they look tame, but that a small move in the point makes only a small move in the whole solution has to be proved, and can be proved differentiable"))

 # ── beat 1: theorem 2.1 ───────────────────────────────────────────
 def _thm21(self):
  cx, cy, s = -4.05, 0.06, 0.62
  g = VGroup()
  for w_, h_, col, lab, lw in ((1.60, 1.00, DIM, "L × U", 1.30),
                               (0.78, 0.48, ACCENT_B, "J × N", 1.30)):
   g.add(Line([cx - w_, cy - h_, 0], [cx + w_, cy - h_, 0], color=col, stroke_width=2.0),
         Line([cx - w_, cy + h_, 0], [cx + w_, cy + h_, 0], color=col, stroke_width=2.0),
         Line([cx - w_, cy - h_, 0], [cx - w_, cy + h_, 0], color=col, stroke_width=2.0),
         Line([cx + w_, cy - h_, 0], [cx + w_, cy + h_, 0], color=col, stroke_width=2.0))
   g.add(self._sym(cy + h_ + 0.14, lab, col, FS_TAG - 4, x=cx + w_ - 0.42, w=lw))
  for a, col in zip((-0.30, 0.0, 0.30), (ACCENT_C, ACCENT_A, WARN)):
   g.add(Dot([cx + 0.22, cy + s * a, 0], radius=0.052, color=col))
  g.add(Dot([cx, cy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._table((("F   :   L × U → W        ‖ F ‖  ≤  m", ACCENT_B),
                     ("‖ F ( t , ξ ) − F ( t , η ) ‖  ≤  c ‖ ξ − η ‖", ACCENT_C),
                     ("⟨ t ₁ , α ₁ ⟩  ∈  J × N     ⇒     ∃ !  f : J → U", ACCENT_A),
                     ("⟨ t ₁ , α ₁ ⟩   ↦   f          J × N → V", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("小框裡的每一點都配到一條解，而配法連續",
                  "every point of the inner box gets a solution, and the assignment is continuous"))
  return g.add(self._foot("定理 2.1：F 在 L × U 上有界、連續、對第二個變數一致 Lipschitz，那麼有個較小的鄰域 J × N，其中每一點恰有一條從 J 到 U 的解通過",
                          "theorem 2.1: with F bounded, continuous and uniformly Lipschitz in its second variable on the outer box, some smaller neighbourhood has exactly one solution through each of its points",
                          ACCENT_A,
                          "而且那個「初始點 ↦ 解」的映射從 J × N 到 V 是連續的。注意小框比大框小很多——下面幾拍會看到它為什麼非小不可",
                          "and the map from initial point to solution is continuous; note how much smaller the inner box is, and the next beats show why it has to be"))

 # ── beat 2: K with two more arguments ─────────────────────────────
 def _kmap(self):
  ox, oy, sx, sy = -5.90, -0.30, 1.85, 0.30
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.46, oy, 0], DIM, sw=3, tl=0.14))
  for t1, a1, col in ((0.0, 0.0, ACCENT_B), (0.45, 0.28, ACCENT_C), (0.90, -0.20, WARN)):
   f = sol(t1, a1)
   g.add(self._fcurve(ox, oy, sx, sy, f, col, t0=t1, t1=t1 + 0.85, sw=2.8))
   g.add(Dot([ox + sx * t1, oy + sy * a1, 0], radius=0.055, color=col))
   g.add(self._dash([ox + sx * t1, oy, 0], [ox + sx * t1, oy + sy * a1, 0], col, n=4, sw=1.2))
  g.add(self._legend(ox + 0.08, ((ACCENT_B, "⟨ t ₁ , α ₁ ⟩", 1.40),), y0=1.14))
  g.add(self._table((("K ( t ₁ , α ₁ , f ) ( t )   =   α ₁  +  ∫ F ( s , f ( s ) ) d s", ACCENT_A),
                     ("( s  :  t ₁ → t )", DIM),
                     ("g  =  K ( t ₁ , α ₁ , f )       ⟺       g ′ = F ( t , g )", ACCENT_B),
                     ("f     ↦     K ( t ₁ , α ₁ , f )", ACCENT_C)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("同一個 K，只是起點從固定變成可動",
                  "the same K, with its starting point free instead of fixed"))
  return g.add(self._foot("證明就是把上一集的計算重跑一次，只是 K 多吃兩個變數：現在它帶著 t ₁ 與 α ₁，把 f 送到 α ₁ 加上從 t ₁ 積到 t 的積分",
                          "the proof reruns the calculation with K taking two more arguments: it now carries the initial time and value, sending f to that value plus the integral from that time out to t",
                          ACCENT_A,
                          "對固定的 f，K 顯然對 ⟨ t ₁ , α ₁ ⟩ 連續——積分的下限與加進去的常數都連續地依賴它們。真正要重算的是那兩個估計",
                          "for each fixed f, K is plainly continuous in the initial point, since both the lower limit and the added constant depend on it continuously; what needs recomputing is the two estimates"))

 # ── beat 3: N is the ball of half the radius ──────────────────────
 def _halfball(self):
  cx, cy = -4.05, 0.04
  g = VGroup()
  for rad, col, lab, lw, dx in ((0.94, ACCENT_B, "𝔘  =  B ᵣ ( ᾱ ₀ )", 1.90, -1.46),
                                (0.47, WARN, "N  =  B ᵣ ⁄ ₂ ( α ₀ )", 2.00, 1.46)):
   g.add(self._curve([[cx + rad * math.cos(math.tau * k / 80),
                       cy + rad * math.sin(math.tau * k / 80), 0] for k in range(81)],
                     col, sw=2.6))
   g.add(self._sym(cy + rad + 0.20, lab, col, FS_TAG - 4, x=cx + dx, w=lw))
  g.add(Dot([cx, cy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._arr([cx, cy, 0], [cx + 0.47, cy, 0], WARN, sw=3, tl=0.12))
  g.add(self._arr([cx, cy - 0.16, 0], [cx + 0.94, cy - 0.16, 0], ACCENT_B, sw=3, tl=0.12))
  g.add(self._table((("α ₁  ∈  N       ⇒       ‖ α ₁ − α ₀ ‖  ≤  r / 2", WARN),
                     ("‖ K ( t ₁ , α ₁ , ᾱ ₀ ) − ᾱ ₀ ‖   ≤   r / 2  +  δ m", ACCENT_A),
                     ("‖ K f ₁ − K f ₂ ‖ ∞   ≤   δ c ‖ f ₁ − f ₂ ‖ ∞", ACCENT_C),
                     ("r / 2  +  δ m    <    ( 1 − δ c ) r", ACCENT_B)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("紅圈吃掉一半，剩下的才是 δ 能用的",
                  "the red circle eats half the room, and delta gets what is left"))
  return g.add(self._foot("N 取半徑是 r 一半的球。於是 K 作用在常數函數上，離球心不超過 ‖ α ₁ − α ₀ ‖ 加 δ m，也就是 r / 2 加 δ m",
                          "take N to be the ball of half the radius; then K applied to the constant function sits within the distance from the old centre plus delta times m, that is half of r plus delta times m",
                          ACCENT_A,
                          "壓縮那一半的估計完全不動——它跟起點無關。動的只有球心那一項，而它從 δ m 變成 r / 2 加 δ m",
                          "the contraction half of the estimate is untouched, since it never involved the starting point; only the displacement term changes, from delta times m to half of r plus that"))

 # ── beat 4: the ceiling halves ────────────────────────────────────
 def _halfdelta(self):
  ox, oy, sx, sy = -5.90, -0.60, 11.20, 1.10
  g = VGroup(self._frame(ox, oy, 3.48, 1.50, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, lambda d: R / 2.0 + d * M_BD, ACCENT_B,
                     t0=0.0, t1=0.30, sw=3.0))
  g.add(self._fcurve(ox, oy, sx, sy, lambda d: (1.0 - d * C_SUP) * R, WARN,
                     t0=0.0, t1=0.30, sw=3.0))
  for d, col in ((D_TWO, ACCENT_A), (D_ONE, DIM)):
   g.add(self._dash([ox + sx * d, oy, 0], [ox + sx * d, oy + 1.16, 0], col, n=10, sw=1.4),
         self._sym(oy - 0.26, f"{d:.3f}", col, FS_TAG - 3, x=ox + sx * d, w=0.66))
  g.add(self._legend(ox + 0.08, ((ACCENT_B, "r / 2 + δ m", 1.30),
                                 (WARN, "( 1 − δ c ) r", 1.30)), y0=1.14))
  g.add(self._table((("        δ        r / 2 + δ m      ( 1 − δ c ) r", DIM),)
                    + tuple((f"    {d:.3f}        {a:.3f}           {b:.3f}",
                             ACCENT_B if a < b else WARN) for d, a, b in STEP)
                    + ((f"    δ  <  {D_TWO:.3f}   =   {D_ONE:.2f} / 2", ACCENT_A),),
                    y0=0.94, dy=0.235, size=FS_TAG - 3),)
  g.add(self._cap("兩欄在 0.125 交換大小，那就是新的上限",
                  "the two columns swap order at 0.125, and that is the new ceiling"))
  return g.add(self._foot("兩個要求疊起來：r / 2 + δ m 要小於 ( 1 − δ c ) r，算出來是 δ < r / ( 2 ( m + c r ) ) = 0.125——正好是上一集那個 0.25 的一半",
                          "stacking the two demands gives delta below r over twice m plus c r, which is 0.125 here, exactly half of the 0.25 that section 1 allowed",
                          ACCENT_A,
                          "這就是連續相依的全部代價：同一個 F、同一個球，區間砍一半。定理 2.1 的小框之所以非小不可，原因就在這裡",
                          "that is the entire price of continuous dependence: the same F and the same ball, with half the interval, and it is why the inner box of Theorem 2.1 has to be small"))

 # ── beat 5: the fixed point moves continuously with the parameter ─
 def _cont(self):
  ox, oy, sx, sy = -5.90, -0.28, 1.85, 0.30
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.46, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fan(ox, oy, sx, sy, t1=1.40, sw=2.8))
  g.add(self._dash([ox + sx * 1.40, oy + sy * sol(0.0, FAN[0])(1.40), 0],
                   [ox + sx * 1.40, oy + sy * sol(0.0, FAN[-1])(1.40), 0], INK, n=9, sw=1.6))
  g.add(self._table((("Ch 4  ,  9.2", ACCENT_C),
                     ("‖ K ( p , f ₁ ) − K ( p , f ₂ ) ‖   ≤   C ‖ f ₁ − f ₂ ‖", DIM),
                     ("⇒          p     ↦     f ( p )", ACCENT_A),
                     ("p   =   ⟨ t ₁ , α ₁ ⟩", ACCENT_B)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("左邊的點動一點，右邊那一整條就只動一點",
                  "move the dots a little and the whole curves move only a little"))
  return g.add(self._foot("有了那個 δ，就把第 4 章的定理 9.2 套上去：那是帶參數的不動點定理，它說壓縮映射的不動點對參數連續",
                          "with that delta in hand, apply chapter 4's Theorem 9.2, the fixed-point theorem with a parameter: the fixed point of a contraction depends continuously on the parameter",
                          ACCENT_A,
                          "這裡的參數正是初始點，不動點正是解，所以定理 2.1 就證完了。整個第 2 節沒有新的分析，只是把舊定理擺在對的位置上",
                          "here the parameter is the initial point and the fixed point is the solution, so Theorem 2.1 is proved; the section adds no new analysis, it puts old theorems in the right place"))

 # ── beat 6: what differentiability needs ──────────────────────────
 def _needs(self):
  ox, oy = -5.85, 0.30
  g = VGroup()
  # the two rows must differ on screen, or the beat's only point -- that
  # upgrading the hypothesis upgrades the conclusion -- is drawn twice as one
  for yy, col, tag, hyp, thm in ((oy + 0.34, DIM, "𝒞 ⁰", "Lipschitz", "9.2"),
                                 (oy - 0.66, ACCENT_A, "𝒞 ¹", "d F", "9.4")):
   for k, (x0, lab) in enumerate(((-5.00, "F"), (-3.40, "K"), (-1.80, "f"))):
    g.add(self._box(x0, yy, lab, col, w=0.70, h=0.52, size=FS_TAG + 2))
    if k < 2:
     g.add(self._arr([x0 + 0.42, yy, 0], [x0 + 1.18, yy, 0], col, sw=3, tl=0.12))
   g.add(self._sym(yy + 0.36, thm, col, FS_TAG - 3, x=-4.20, w=0.70),
         self._sym(yy, tag, col, FS_TAG, x=-6.00, w=0.80),
         self._sym(yy + 0.36, hyp, col, FS_TAG - 3, x=-5.00, w=1.40))
  g.add(self._table((("Ch 4  ,  9.4", ACCENT_C),
                     ("K  ∈  𝒞 ¹        ⇒        f  ∈  𝒞 ¹", ACCENT_A),
                     ("d F        L × U", ACCENT_B),
                     ("⇒        K  ∈  𝒞 ¹", ACCENT_C)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("上排是連續那一條，下排把每一格升級一次",
                  "the top row is the continuous chain; the bottom upgrades every box"))
  return g.add(self._foot("第 4 章的定理 9.4 說：不動點對參數連續可微，只要那個映射本身連續可微。所以問題就變成 K 連不連續可微",
                          "chapter 4's Theorem 9.4 says the fixed point is continuously differentiable in the parameter as soon as the map itself is, so the question becomes whether K is",
                          ACCENT_A,
                          "而那只要 F 的微分存在、而且在 L × U 上一致連續。假設從「Lipschitz」升級成「dF 一致連續」，結論就從「連續」升級成「連續可微」",
                          "and for that it is enough that dF exist and be uniformly continuous on the outer box: upgrade the hypothesis from Lipschitz to a uniformly continuous differential and the conclusion upgrades too"))

 # ── beat 7: theorem 2.2 ───────────────────────────────────────────
 def _thm22(self):
  ox, oy, sx, sy = -5.90, -0.28, 1.85, 0.30
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.46, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fan(ox, oy, sx, sy, t1=1.40, sw=2.4))
  for a, col in zip(FAN, (DIM, ACCENT_C, ACCENT_A, ACCENT_B, WARN)):
   g.add(self._arr([ox - 0.02, oy + sy * a, 0], [ox + 0.34, oy + sy * a, 0], col, sw=3, tl=0.11))
  g.add(self._table((("F     L × U → W          ‖ F ‖   ≤   m", ACCENT_B),
                     ("d F        L × U           ‖ d F ‖   ≤   M", ACCENT_C),
                     ("⇒     ⟨ t ₁ , α ₁ ⟩ ↦ f      ∈     𝒞 ¹", ACCENT_A),
                     ("∂ f / ∂ α ₁       ∃", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("箭頭是初始值的方向，最後一列說它推得出整條解的變化",
                  "the arrows are the direction of the initial value, and the last row differentiates along it"))
  return g.add(self._foot("定理 2.2：L × U 是初始點的鄰域，F 有界，而且 dF 存在、有界、在 L × U 上一致連續。那麼在定理 2.1 的框架裡，解是初始值的連續可微函數",
                          "theorem 2.2: on that neighbourhood let F be bounded with dF existing, bounded and uniformly continuous; then in the setting of Theorem 2.1 the solution is continuously differentiable in the initial value",
                          ACCENT_A,
                          "注意「一致」連續：在 L × U 上一致，不是每一點各自連續。這個條件比 Lipschitz 強，而它換來的是可以對初始值微分",
                          "note the uniformity: uniformly continuous on the whole box, not continuous at each point separately, and that stronger hypothesis is what buys differentiation in the initial value"))

 # ── beat 8: K as a composition of two known maps ──────────────────
 def _compose(self):
  oy = 0.20
  g = VGroup()
  xs = (-5.40, -3.60, -1.80)
  labs = (("f", ACCENT_B, 0.60), ("h", ACCENT_C, 0.60), ("k", ACCENT_A, 0.60))
  for x0, (lab, col, w_) in zip(xs, labs):
   g.add(self._box(x0, oy, lab, col, w=w_, h=0.56, size=FS_TAG + 3))
  for k, x0 in enumerate(xs[:-1]):
   g.add(self._arr([x0 + 0.38, oy, 0], [xs[k + 1] - 0.38, oy, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(oy + 0.34, "F ( s , f ( s ) )", ACCENT_C, FS_TAG - 3, x=-4.50, w=1.80),
        self._sym(oy + 0.34, "∫ h ( s ) d s", ACCENT_A, FS_TAG - 3, x=-2.70, w=1.60))
  g.add(self._sym(oy - 0.40, "Ch 3  ,  14.3", DIM, FS_TAG - 4, x=-4.50, w=1.50),
        self._sym(oy - 0.40, "( s  :  t ₁ → t )", DIM, FS_TAG - 4, x=-2.70, w=1.60))
  g.add(self._sym(oy - 0.86, "K   =   ∫  ∘  F", ACCENT_A, FS_TAG - 1, x=-3.60, w=2.20))
  g.add(self._table((("f    ↦    h  ,   h ( s )  =  F ( s , f ( s ) )", ACCENT_C),
                     ("Ch 3  ,  14.3      ⇒      𝒞 ¹", ACCENT_C),
                     ("h    ↦    k  ,   k ( t )  =  ∫ h ( s ) d s", ACCENT_A),
                     ("h   ↦   k        :        V  →  V", ACCENT_A),
                     ("⇒          d K ³", ACCENT_B)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("兩格都是已經證過的東西，K 只是把它們串起來",
                  "both arrows are already-proved maps, and K only strings them together"))
  return g.add(self._foot("把 K 拆成兩步：先把 f 送到 s ↦ F ( s , f ( s ) )，這一步由第 3 章定理 14.3 連續可微；再從 t ₁ 積到 t，這一步是 V 到 V 的有界線性映射",
                          "split K in two: first send f to the function F at s and f of s, continuously differentiable by chapter 3's Theorem 14.3; then integrate from the initial time out to t, a bounded linear map of V into itself",
                          ACCENT_A,
                          "有界線性映射自動連續可微，所以複合起來，K 對第三個變數的偏微分存在而且連續。剩下兩個偏微分下一拍算",
                          "a bounded linear map is automatically continuously differentiable, so the composition gives K a continuous partial differential in its third argument; the other two come next"))

 # ── beat 9: the three partial differentials, two of them computed ─
 def _partials(self):
  ox, oy, sx, sy = -5.90, -0.44, 2.05, 0.46
  g = VGroup(self._frame(ox, oy, 3.50, 1.44, down=0.10))
  f = sol(T1P, A1P)
  g.add(self._fcurve(ox, oy, sx, sy, f, ACCENT_B, t0=T1P, t1=T1P + 0.70, sw=3.0))
  g.add(Dot([ox + sx * T1P, oy + sy * A1P, 0], radius=0.058, color=ACCENT_A))
  hh = 0.34
  g.add(Line([ox + sx * T1P, oy - 0.26, 0], [ox + sx * (T1P + hh), oy - 0.26, 0],
             color=WARN, stroke_width=4.0))
  g.add(self._sym(oy - 0.52, "h", WARN, FS_TAG - 3, x=ox + sx * (T1P + hh / 2), w=0.34))
  g.add(self._fcurve(ox, oy, sx, sy, lambda t: F(t, f(t)), ACCENT_C,
                     t0=T1P, t1=T1P + 0.70, sw=2.4))
  g.add(self._legend(ox + 0.08, ((ACCENT_B, "f", 0.40),
                                 (ACCENT_C, "F ( s , f ( s ) )", 1.60)), y0=1.14))
  g.add(self._table((("d K ²   =   I", ACCENT_A),
                     ("Δ K ¹ ( h )  =  − ∫ F ( s , f ( s ) ) d s      ( s : t ₁ → t ₁ + h )", ACCENT_C),
                     (f"d K ¹ ( h )  =  − h F ( t ₁ , f ( t ₁ ) )  =  − {abs(DK1):.4f} h", ACCENT_A),)
                    + tuple((f"      h  =  {h:.0e}          Δ K ¹ / h  =  {q:+.6f}", ACCENT_B)
                            for h, q in DK1_NUM)
                    + (("Ch 3  ,  8.3      ⇒      K  ∈  𝒞 ¹", ACCENT_B),),
                    y0=0.92, dy=0.24, size=FS_TAG - 4))
  g.add(self._cap("商收向 −0.8000，絕對值正是紫線起點的高度",
                  "the quotient closes on minus the height of the purple curve at the start"))
  return g.add(self._foot("三個偏微分：對 f 那一個上一拍有了；對 α ₁ 那一個是恆等映射，因為增量就是 ξ 本身；對 t ₁ 那一個是 − h F ( t ₁ , f ( t ₁ ) )",
                          "the three partial differentials: the one in f was done last beat; the one in the initial value is the identity, since the increment is the vector itself; the one in the initial time is minus h times F there",
                          ACCENT_A,
                          "第三個的道理是：把下限從 t ₁ 挪到 t ₁ + h，等於扣掉那一小段的積分，而那一小段約等於 h 乘被積函數在起點的值。三個都連續，第 3 章定理 8.3 就接成連續可微",
                          "the third holds because moving the lower limit subtracts a short integral, which is about h times the integrand at the start; all three being continuous, chapter 3's Theorem 8.3 joins them into continuous differentiability"))

 # ── beat 10: the corollary, with the derivative computed ──────────
 def _corollary(self):
  ox, oy, sx, sy = -5.90, -0.30, 1.85, 0.30
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.46, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fan(ox, oy, sx, sy, t1=1.55, sw=2.6))
  # draw the spread at the start as well, or "2.718282" has nothing to be
  # 2.718282 times: it is the ratio of the two segments, not the length of one
  g.add(self._dash([ox + sx * S_EVAL, oy + sy * sol(0.0, FAN[0])(S_EVAL), 0],
                   [ox + sx * S_EVAL, oy + sy * sol(0.0, FAN[-1])(S_EVAL), 0],
                   INK, n=8, sw=1.8))
  g.add(self._dash([ox - 0.16, oy + sy * FAN[0], 0], [ox - 0.16, oy + sy * FAN[-1], 0],
                   INK, n=4, sw=1.8))
  g.add(self._sym(oy - 0.34, "s", INK, FS_TAG - 3, x=ox + sx * S_EVAL, w=0.34),
        self._sym(oy - 0.34, "t ₁", INK, FS_TAG - 3, x=ox - 0.16, w=0.44))
  g.add(self._table((("α     ↦     f ( s )", ACCENT_A),
                     ("π ₛ   :   f   ↦   f ( s )", ACCENT_C),
                     (f"∂ f ( s ) / ∂ α ₁   =   exp ( s − t ₁ )   =   {DFDA:.6f}", ACCENT_A),)
                    + tuple((f"      ε  =  {e:.0e}         Δ f ( s ) / ε  =  {q:.6f}", ACCENT_B)
                            for e, q in SPREAD[:3])
                    + (("Ch 6  ,  2.3", DIM),),
                    y0=0.92, dy=0.24, size=FS_TAG - 4),)
  g.add(self._cap("右邊那一段是左邊那一段的 2.718282 倍",
                  "the right segment is that many times the left one"))
  return g.add(self._foot("推論：解在任一點 s 的值，是初始值的可微函數。因為 α ↦ f 連續可微，而取值 π ₛ 是有界線性、自動連續可微，複合起來就是",
                          "corollary: the value of a solution at any point is a differentiable function of the initial value, since the map to the solution is continuously differentiable and evaluation is bounded and linear",
                          ACCENT_A,
                          "這個例子的解映射有閉式，所以那個導數算得出真值 exp ( s − t ₁ )，在 s = 1 就是 e。定理 2.3 把整件事做成整體的，書上不給證明。第 2 節整節沒有習題",
                          "this example's solution map has a closed form, so the derivative is exactly the exponential and at s = 1 it is e; Theorem 2.3 makes the whole thing global, unproved in the book, and section 2 has no exercises at all"))

 def stage(self):
  a, b, c = self._question(), self._thm21(), self._kmap()
  d, e, f_ = self._halfball(), self._halfdelta(), self._cont()
  h, i, j = self._needs(), self._thm22(), self._compose()
  k, l = self._partials(), self._corollary()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE76ZH, AdvCalcE76EN = make(AdvCalcE76Base, "76", prefix="AdvCalcE")
