"""advcalc E75 -- chapter 6, section 1 (book pp. 269-272): global solutions,
the maximal solution, Theorem 1.4, and the nth-order equation.

E74 stopped at Theorem 1.2, which promises a solution only on some small enough
interval.  This half of the section asks how far that solution really goes.  The
answer comes in two steps.  First a construction: run to near the end of a local
solution, take a fresh local solution there, and Lemma 1.1 makes the two agree
on the overlap while the new one reaches further.  Made precise, this is a union
-- a function being a set of ordered pairs, the union of the whole family of
solutions through a point is again a function exactly because of Lemma 1.1, and
it is the unique maximal solution (Theorem 1.3).

Second, when is the maximal solution defined on all of I?  Theorem 1.4: when A
is the whole of W and F is Lipschitz in its second variable with a bound c(t)
continuous in t -- globally in alpha, not just locally.  The proof turns on one
observation: Theorem 1.1's radius bound r/(m + rc) equals 1/(c + m/r), and with
A = W there is no ceiling on r, so that bound climbs to 1/c.  Any right endpoint
b strictly inside I can then be overshot, which contradicts maximality.

The two examples that carry the episode differ in exactly that hypothesis, and
in nothing else -- both have A = W = R.  For F = t + x the Lipschitz quotient is
identically 1, so c is constant and the solution e^t - t - 1 lives on the whole
line.  For F = 1 + x^2 the quotient is |xi + eta|, which no c(t) can hold down,
and tan t dies at pi/2.  That is the whole content of Theorem 1.4 in one pair.

The section closes by reducing the nth-order equation to a first-order system,
where every derivative becomes the next coordinate and only the last equation
carries G.  Here that is x'' = -x turning into the rotation field on the plane,
whose solution curve is the unit circle.
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
PI = math.pi
BLOW = PI / 2


# ── the two equations, differing only in Theorem 1.4's hypothesis ─────
def FA(t, x):
 """dies at pi/2: the Lipschitz quotient |xi + eta| has no bound over R."""
 return 1.0 + x * x


def FB(t, x):
 """lives on all of R: the quotient is identically one."""
 return t + x


def gB(t):
 return math.exp(t) - t - 1.0


for _t in (-1.0, 0.0, 0.7, 2.0, 3.5):
 _d = (math.tan(_t + 1e-6) - math.tan(_t - 1e-6)) / 2e-6 if abs(_t) < BLOW else None
 if _d is not None:
  assert abs(_d - FA(_t, math.tan(_t))) < 1e-4, "tan solves the first equation"
 _e = (gB(_t + 1e-6) - gB(_t - 1e-6)) / 2e-6
 assert abs(_e - FB(_t, gB(_t))) < 1e-5, "and this one solves the second"
assert abs(gB(0.0)) < 1e-15 and abs(math.tan(0.0)) < 1e-15, "both through the origin"

# the quotients, which is the only place the two differ
QA = [(a, b, abs(FA(0.0, a) - FA(0.0, b)) / abs(a - b)) for a, b in
      ((1.0, 0.5), (3.0, 2.0), (10.0, 9.0), (100.0, 99.0))]
QB = [(a, b, abs(FB(0.0, a) - FB(0.0, b)) / abs(a - b)) for a, b in
      ((1.0, 0.5), (3.0, 2.0), (10.0, 9.0), (100.0, 99.0))]
assert all(abs(q - 1.0) < 1e-12 for _a, _b, q in QB), "identically one, so c is constant"
assert all(abs(q - (a + b)) < 1e-9 for a, b, q in QA)
assert QA[-1][2] > 100 * QA[0][2], "and unbounded, so no c(t) exists"
C_B = 1.0

# ── beat 0: patching local solutions, with Theorem 1.1's own delta ────
R_BALL = 1.0
PATCH = []
_tk = 0.0
for _ in range(6):
 _ak = math.tan(_tk)
 _lo, _hi = _ak - R_BALL, _ak + R_BALL
 _m = 1.0 + max(_lo * _lo, _hi * _hi)          # sup of 1 + x^2 on the ball
 _c = 2.0 * max(abs(_lo), abs(_hi))            # sup of |2x| on the ball
 _d = R_BALL / (_m + _c * R_BALL)
 PATCH.append((_tk, _ak, _m, _c, _d, _tk + _d))
 _tk += 0.96 * _d
assert all(PATCH[i][5] < PATCH[i + 1][5] for i in range(len(PATCH) - 1)), \
    "each patch reaches further right than the one before"
assert all(PATCH[i + 1][0] < PATCH[i][5] for i in range(len(PATCH) - 1)), \
    "and starts inside it, so the two overlap and Lemma 1.1 applies"
assert all(PATCH[i][4] > PATCH[i + 1][4] for i in range(len(PATCH) - 1)), \
    "the patches shrink, because the ball round a larger value has a larger m and c"
assert all(p[5] < BLOW for p in PATCH), "and none of them ever passes pi/2"

# ── beat 7: with A = W there is no ceiling on r, so the bound climbs ──
T1, LBAR = 2.0, (1.5, 2.5)
A1 = gB(T1)
M_B = max(abs(FB(t, A1)) for t in LBAR)
RAD = [(r, r / (M_B + r * C_B)) for r in (1.0, 10.0, 100.0, 1.0e3, 1.0e4)]
assert all(RAD[i][1] < RAD[i + 1][1] for i in range(len(RAD) - 1)), "monotone in r"
assert all(abs(b - 1.0 / (C_B + M_B / r)) < 1e-12 for r, b in RAD), "the two forms agree"
assert RAD[-1][1] < 1.0 / C_B, "never reaching the limit"
assert 1.0 / C_B - RAD[-1][1] < 1.0e-3, "but getting arbitrarily close to it"

# ── beat 8: the contradiction, with numbers ───────────────────────────
B_HYP, T1H, DELTA_H = 3.00, 2.40, 0.80
assert B_HYP - T1H < 1.0 / C_B, "t1 is chosen closer to b than 1/c"
assert T1H + DELTA_H > B_HYP, "so the local solution there reaches past b"
assert DELTA_H < 1.0 / C_B, "while delta still respects the bound of the last beat"
OVER = T1H + DELTA_H - B_HYP

# ── beats 9 and 10: the second-order equation as a first-order system ─
def FC(a1, a2):
 """x'' = -x becomes the rotation field on the plane."""
 return (a2, -a1)


for _t in (0.0, 0.6, 1.9, 4.2):
 _p = (math.sin(_t), math.cos(_t))
 _d = ((math.sin(_t + 1e-6) - math.sin(_t - 1e-6)) / 2e-6,
       (math.cos(_t + 1e-6) - math.cos(_t - 1e-6)) / 2e-6)
 _f = FC(*_p)
 assert abs(_d[0] - _f[0]) < 1e-6 and abs(_d[1] - _f[1]) < 1e-6, \
     "sine and cosine together solve the system"
 assert abs(_p[0] ** 2 + _p[1] ** 2 - 1.0) < 1e-12, "so the solution curve is the unit circle"
C_C = 1.0
QC = []
for _p, _q in (((1.0, 0.0), (0.0, 1.0)), ((0.5, 0.5), (-0.5, 0.2)), ((3.0, 1.0), (3.0, 4.0))):
 _fp, _fq = FC(*_p), FC(*_q)
 _num = math.hypot(_fp[0] - _fq[0], _fp[1] - _fq[1])
 _den = math.hypot(_p[0] - _q[0], _p[1] - _q[1])
 QC.append((_num, _den, _num / _den))
assert all(abs(q - C_C) < 1e-12 for _n, _d, q in QC), \
    "the field is a rotation, so it preserves distances: c is 1 and theorem 1.4 applies"


class AdvCalcE75Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 75

 MODE_LABEL = {
  0: {"zh": "把局部解拼起來", "en": "patching local solutions"},
  1: {"zh": "精確的做法：取聯集", "en": "made precise: a union"},
  2: {"zh": "定理 1.3：極大解", "en": "theorem 1.3: the maximal solution"},
  3: {"zh": "極大解一般撞上 A 的邊界", "en": "it generally runs into the boundary"},
  4: {"zh": "定理 1.4", "en": "theorem 1.4"},
  5: {"zh": "兩個例子只差這一條", "en": "two examples, one difference"},
  6: {"zh": "證明（一）：取緊的閉包", "en": "proof, one: a compact closure"},
  7: {"zh": "證明（二）：r 沒有上限", "en": "proof, two: no ceiling on r"},
  8: {"zh": "證明（三）：矛盾", "en": "proof, three: the contradiction"},
  9: {"zh": "n 階方程化成一階系統", "en": "the nth-order equation as a system"},
  10: {"zh": "定理 1.5，與第 1 節的結束", "en": "theorem 1.5, and the end of section 1"},
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

 # ── beat 0: the patches, drawn with their own deltas ──────────────
 def _patch(self):
  ox, oy, sx, sy = -6.00, -0.36, 3.30, 0.42
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.70, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, DIM, t0=0.0, t1=1.05, sw=2.0))
  cols = (ACCENT_B, ACCENT_C, WARN, ACCENT_A)
  for k, (tk, ak, _m, _c, d, rt) in enumerate(PATCH[:4]):
   lo = max(0.0, tk - d)
   g.add(self._fcurve(ox, oy, sx, sy, math.tan, cols[k], t0=lo, t1=rt, sw=3.0))
   y = oy - 0.22 - 0.17 * k
   g.add(Line([ox + sx * lo, y, 0], [ox + sx * rt, y, 0], color=cols[k], stroke_width=3.0),
         Line([ox + sx * lo, y - 0.05, 0], [ox + sx * lo, y + 0.05, 0],
              color=cols[k], stroke_width=3.0),
         Line([ox + sx * rt, y - 0.05, 0], [ox + sx * rt, y + 0.05, 0],
              color=cols[k], stroke_width=3.0))
  g.add(self._table((("       t ₖ         δ ₖ        t ₖ + δ ₖ", DIM),)
                    + tuple((f"    {tk:.4f}    {d:.4f}      {rt:.4f}", ACCENT_B)
                            for tk, _a, _m, _c, d, rt in PATCH[:5])
                    + ((f"    π / 2   =   {BLOW:.4f}", ACCENT_A),),
                    y0=0.92, dy=0.27, size=FS_TAG - 3))
  g.add(self._cap("中欄越來越小，右欄越來越大", "the middle column shrinks, the right one grows"))
  return g.add(self._foot("跑到一條局部解的尾端附近，再取一個新的局部解：引理 1.1 保證兩者在交集上相等，而新的那條伸得更遠，於是拼成一條活得更久的解",
                          "run to near the end of one local solution and take a fresh one there: Lemma 1.1 makes them agree on the overlap while the new one reaches further",
                          ACCENT_A,
                          "每一段的長度都是定理 1.1 自己算出來的 δ。注意它一段比一段短——球心的值越大，m 與 c 都越大——所以這樣拼下去永遠過不了 π / 2",
                          "each patch is as long as Theorem 1.1's own delta allows, and each is shorter than the last, since a ball round a larger value has a larger m and c, so the patching never passes pi over two"))

 # ── beat 1: the family, and why the union is a function ───────────
 def _union(self):
  ox, oy, sx = -4.10, 0.46, 2.20          # ox is t = 0, so the bars run both ways
  g = VGroup()
  doms = ((-0.30, 0.34), (-0.52, 0.55), (-0.18, 0.78), (-0.66, 0.42))
  cols = (ACCENT_B, ACCENT_C, WARN, DIM)
  for k, ((lo, hi), col) in enumerate(zip(doms, cols)):
   y = oy - 0.20 * k
   g.add(Line([ox + sx * lo, y, 0], [ox + sx * hi, y, 0], color=col, stroke_width=3.4))
  uy = oy - 0.20 * len(doms) - 0.16
  g.add(Line([ox + sx * min(d[0] for d in doms), uy, 0],
             [ox + sx * max(d[1] for d in doms), uy, 0], color=ACCENT_A, stroke_width=5.0))
  g.add(self._dash([ox, uy - 0.18, 0], [ox, oy + 0.20, 0], ACCENT_A, n=9, sw=1.3))
  g.add(Dot([ox, uy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._sym(uy - 0.34, "t ₀", ACCENT_A, FS_TAG - 3, x=ox, w=0.44))
  g.add(self._legend(ox - 2.00, ((DIM, "g  ∈  𝔉", 0.94), (ACCENT_A, "∪ 𝔉", 0.70)), y0=1.14))
  g.add(self._table((("𝔉  =  { g  :  g ′ = F ( t , g )  ,  g ( t ₀ ) = α ₀ }", ACCENT_B),
                     ("g ₁ ( t ) = α ₁  ,  g ₂ ( t ) = α ₂     ⇒     α ₁ = α ₂", ACCENT_C),
                     ("f   =   ∪ 𝔉", ACCENT_A),
                     ("t ₀  ∈  J  ⊂  I        ∀ g ∈ 𝔉", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("第二列就是引理 1.1，聯集靠它才是函數",
                  "the second row is Lemma 1.1, and it is what makes the union a function"))
  return g.add(self._foot("𝔉 是所有通過 ⟨ t ₀ , α ₀ ⟩ 的解。函數是有序對的集合，所以聯集有意義；而引理 1.1 說同一個 t 不會被配到兩個不同的值",
                          "the family is every solution through the point; a function is a set of ordered pairs so the union makes sense, and Lemma 1.1 says no t is given two values",
                          ACCENT_A,
                          "上面四條是 𝔉 裡的四個定義域，全都含 t ₀；最底下那條橘線是它們的聯集。這一步把「一直拼下去」從描述變成一個確切的東西",
                          "the four bars above are four domains in the family, all containing the initial time, and the orange bar below is their union: that is what turns the patching picture into a definite object"))

 # ── beat 2: the union is a solution, and it is maximal ────────────
 def _maximal(self):
  ox, oy, sx, sy, TC = -4.05, -0.08, 1.15, 0.34, 1.20   # ox is t = 0
  g = VGroup(self._arr([ox - 2.10, oy, 0], [ox + 2.14, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_A, t0=-TC, t1=TC, sw=3.6))
  for lo, hi, col in ((-0.34, 0.40, ACCENT_B), (-0.72, 0.86, ACCENT_C)):
   g.add(self._fcurve(ox, oy, sx, sy, math.tan, col, t0=lo, t1=hi, sw=6.5))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_A, t0=-TC, t1=TC, sw=2.2))
  g.add(Dot([ox, oy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._legend(ox - 2.00, ((ACCENT_C, "g  ∈  𝔉", 0.94),
                                 (ACCENT_A, "f  =  ∪ 𝔉", 1.18)), y0=1.14))
  g.add(self._table((("f ′ ( t )   =   F ( t , f ( t ) )", ACCENT_A),
                     ("g   ⊂   f            ∀ g ∈ 𝔉", ACCENT_C),
                     ("f  :  J → A       J  =  ∪ { J ₉  :  g ∈ 𝔉 }", ACCENT_B),
                     ("∃ !   f", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("每一條粗線都躺在橘線上，沒有一條伸出去",
                  "every thick arc lies along the orange one, and none of them reaches past it"))
  return g.add(self._foot("聯集自己就是解：定義域裡任一點附近，它都與 𝔉 裡某一條相同，所以在那裡可微而且滿足方程",
                          "the union is itself a solution, because near any point of its domain it coincides with one member of the family and so is differentiable and satisfies the equation there",
                          ACCENT_A,
                          "而每一條解都被它包含，所以它是唯一的極大解——這就是定理 1.3：過 I 乘 A 裡的每一點，都有唯一一條決定好的極大解",
                          "and it contains every solution, so it is the unique maximal one: that is Theorem 1.3, a uniquely determined maximal solution through each point of the domain"))

 # ── beat 3: the maximal domain is properly inside I ───────────────
 def _proper(self):
  # clipped by t, not by value: a clamped tan reads as a plateau plus a cliff
  ox, oy, sx, sy, TC = -4.05, -0.02, 1.15, 0.34, 1.2036
  g = VGroup(self._arr([ox - 2.10, oy, 0], [ox + 2.14, oy, 0], DIM, sw=3, tl=0.14))
  for s in (1, -1):
   g.add(self._dash([ox + s * sx * BLOW, oy - 0.34, 0],
                    [ox + s * sx * BLOW, oy + 1.00, 0], WARN, n=10, sw=1.6))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, ACCENT_A, t0=-TC, t1=TC, sw=3.4))
  g.add(Line([ox - sx * BLOW, oy - 0.56, 0], [ox + sx * BLOW, oy - 0.56, 0],
             color=ACCENT_A, stroke_width=4.0))
  g.add(Line([ox - 2.06, oy - 0.80, 0], [ox + 2.06, oy - 0.80, 0],
             color=DIM, stroke_width=3.0))
  g.add(self._sym(oy - 0.56, "J", ACCENT_A, FS_TAG - 3, x=ox + sx * BLOW + 0.28, w=0.40),
        self._sym(oy - 0.80, "I", DIM, FS_TAG - 3, x=ox + 2.30, w=0.40))
  g.add(Dot([ox, oy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._table((("J   ⊊   I", ACCENT_A),
                     (f"J   =   ( − {BLOW:.4f} ,  {BLOW:.4f} )", WARN),
                     ("I   =   ℝ", DIM),
                     ("x ′  =  1 + x ²        x ( 0 )  =  0", ACCENT_B),
                     ("f ( t )   =   tan t", ACCENT_B)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("橘線比灰線短，而且兩端都停在紅虛線上",
                  "the orange bar is shorter than the grey one, stopped at both dashed walls"))
  return g.add(self._foot("極大解一般會撞上 A 的邊界，所以它的定義域 J 真包含在 I 裡——上一集那個例子正是如此",
                          "a maximal solution generally runs into the boundary of A, so its domain sits properly inside I, and last episode's example is exactly that",
                          ACCENT_A,
                          "這裡 I 是整條實數線，而解只活在正負 π / 2 之間。F 到處連續、到處光滑，什麼病都沒有——會停下來的原因不在 F，在解自己跑掉了",
                          "here I is the whole line while the solution lives only between the two walls; F is continuous and smooth everywhere, so what stops it is not F but the solution running away"))

 # ── beat 4: the hypothesis of theorem 1.4, drawn as a cone ────────
 def _thm14(self):
  # the window has to reach past |x| = c or the parabola never leaves the cone:
  # x^2 exceeds c*x only beyond x = c, so with c = 2 the picture needs |x| > 2
  oy, sx, sy, XW, CC = -0.10, 0.33, 0.075, 3.20, 2.00
  g = VGroup()
  for cx, f, col, lab, lw, ok in ((-5.02, FB, ACCENT_B, "t + x", 1.00, True),
                                  (-2.18, FA, WARN, "1 + x ²", 1.30, False)):
   g.add(self._arr([cx - 1.24, oy, 0], [cx + 1.28, oy, 0], DIM, sw=3, tl=0.12),
         Line([cx, oy - 0.54, 0], [cx, oy + 0.92, 0], color=DIM, stroke_width=1.3))
   for s in (1, -1):
    g.add(self._dash([cx - sx * XW, oy - s * sy * CC * XW, 0],
                     [cx + sx * XW, oy + s * sy * CC * XW, 0], DIM, n=13, sw=1.2))
   g.add(self._fcurve(cx, oy, sx, sy, lambda x, f=f: f(0.4, x) - f(0.4, 0.0), col,
                      t0=-XW, t1=XW, sw=3.0))
   g.add(self._sym(oy + 1.06, lab, col, FS_TAG - 3, x=cx, w=lw))
   if not ok:
    ex = cx + sx * 2.70
    ey = oy + sy * 2.70 ** 2 + 0.26
    g.add(Line([ex - 0.17, ey - 0.17, 0], [ex + 0.17, ey + 0.17, 0],
               color=WARN, stroke_width=3.4),
          Line([ex - 0.17, ey + 0.17, 0], [ex + 0.17, ey - 0.17, 0],
               color=WARN, stroke_width=3.4))
   g.add(self._sym(oy - 0.72, "± c | x |", DIM, FS_TAG - 4, x=cx, w=1.10))
  g.add(self._table((("A   =   W", ACCENT_A),
                     ("‖ F ( t , α ₁ ) − F ( t , α ₂ ) ‖  ≤  c ( t ) ‖ α ₁ − α ₂ ‖", ACCENT_C),
                     ("∀  α ₁ , α ₂  ∈  W", WARN),
                     ("c  :  I → ℝ", ACCENT_B),
                     ("⇒        J   =   I", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("左邊那條走不出灰錐，右邊那條一定走得出去",
                  "the left curve stays inside the grey cone; the right one must leave it"))
  return g.add(self._foot("定理 1.4：A 是整個 W、F 連續，而且有連續的 c 使 F 在任兩點的差被 c ( t ) 乘距離控制住，那麼每條極大解的定義域就是整個 I",
                          "theorem 1.4: if A is the whole of W and some continuous c bounds the difference of F's values by c of t times the distance, every maximal solution is defined on all of I",
                          ACCENT_A,
                          "重點在那個「任兩點」：灰錐要罩住整條曲線，不是只罩住原點附近一段。斜率有界的線罩得住，拋物線不管錐開多大都會鑽出去",
                          "the force is in for every pair: the cone has to cover the whole curve, not just a stretch near the centre, and a parabola escapes any cone however wide"))

 # ── beat 5: the two solutions, side by side ───────────────────────
 def _pair(self):
  ox, oy, sx, sy = -5.95, -0.68, 1.95, 0.40
  g = VGroup(self._frame(ox, oy, 3.60, 1.52, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, gB, ACCENT_B, t0=0.0, t1=1.80, sw=3.0))
  g.add(self._fcurve(ox, oy, sx, sy, math.tan, WARN, t0=0.0, t1=1.28, sw=3.0))
  g.add(self._dash([ox + sx * BLOW, oy, 0], [ox + sx * BLOW, oy + 1.44, 0], WARN, n=12, sw=1.5))
  g.add(self._sym(oy + 1.66, f"π / 2  =  {BLOW:.4f}", WARN, FS_TAG - 3,
                  x=ox + sx * BLOW, w=1.80))
  g.add(self._legend(ox + 0.10, ((ACCENT_B, "e ᵗ − t − 1", 1.30),
                                 (WARN, "tan t", 0.80)), y0=1.14))
  g.add(self._table((("        ξ          η       | F ξ − F η | / | ξ − η |", DIM),)
                    + tuple((f"    {a:6.1f}   {b:6.1f}         {qb:.4f}          {qa:8.1f}",
                             ACCENT_B)
                            for (a, b, qa), (_c, _d, qb) in zip(QA, QB))
                    + (("                              t + x          1 + x ²", DIM),),
                    y0=0.90, dy=0.28, size=FS_TAG - 4))
  g.add(self._cap("左欄一直是 1，右欄一路衝上去",
                  "one column stays at one, the other runs away"))
  return g.add(self._foot("兩個例子的 A 都是整個 ℝ，差別只在 Lipschitz 那一條：t + x 的商恆等於 1，所以 c 取常數 1 就夠；1 + x ² 的商是 | ξ + η | ，沒有任何 c 攔得住",
                          "both examples have A equal to all of R, and differ only in the Lipschitz hypothesis: one quotient is identically one, the other is the absolute value of the sum and no c holds it down",
                          ACCENT_A,
                          "結果就分成兩邊：藍線活在整條實數線上，紅線在 π / 2 停住。定理 1.4 的內容全在這一對例子裡",
                          "and the outcome splits accordingly: the blue solution lives on the whole line and the red one stops, which is the whole content of Theorem 1.4 in one pair"))

 # ── beat 6: the compact closure that gives c a maximum ────────────
 def _compact(self):
  ox, oy, sx = -5.90, 0.10, 0.92
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.70, oy, 0], DIM, sw=3, tl=0.14))
  ib = (0.20, 3.80)
  g.add(Line([ox + sx * ib[0], oy + 0.52, 0], [ox + sx * ib[1], oy + 0.52, 0],
             color=DIM, stroke_width=3.0))
  g.add(Line([ox + sx * ib[0], oy + 0.28, 0], [ox + sx * B_HYP, oy + 0.28, 0],
             color=ACCENT_A, stroke_width=4.0))
  g.add(Line([ox + sx * 2.10, oy - 0.26, 0], [ox + sx * 3.50, oy - 0.26, 0],
             color=ACCENT_B, stroke_width=4.0))
  for xx, col, lab, lw, yy in ((ib[1], DIM, "I", 0.36, 0.52),
                               (B_HYP, ACCENT_A, "J", 0.36, 0.28),
                               (3.50, ACCENT_B, "L ‾", 0.44, -0.26)):
   g.add(self._sym(oy + yy, lab, col, FS_TAG - 3, x=ox + sx * xx + 0.26, w=lw))
  g.add(self._dash([ox + sx * B_HYP, oy - 0.42, 0], [ox + sx * B_HYP, oy + 0.42, 0],
                   ACCENT_A, n=7, sw=1.4))
  g.add(self._sym(oy - 0.58, "b", ACCENT_A, FS_TAG - 3, x=ox + sx * B_HYP, w=0.34))
  g.add(self._fcurve(ox, oy + 0.72, sx, 0.10, lambda t: 1.0 + 0.9 * math.sin(1.7 * t),
                     ACCENT_C, t0=0.20, t1=3.80, sw=2.4))
  g.add(self._sym(oy + 1.10, "c ( t )", ACCENT_C, FS_TAG - 3, x=ox + 0.44, w=0.90))
  g.add(self._table((("b   <   sup I", ACCENT_A),
                     ("b  ∈  L      ,      L ‾   ⊂   I", ACCENT_B),
                     ("c   =   max { c ( t )  :  t ∈ L ‾ }", ACCENT_C),
                     (f"c   =   {C_B:.4f}", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("b 在灰線裡面，這是要推翻的那個假設",
                  "b sits inside the grey bar, and that is the assumption to be broken"))
  return g.add(self._foot("反證法。設極大解的右端點 b 還在 I 裡面，取有限開區間 L 含 b 且 L ‾ ⊂ I。L ‾ 是緊的，所以連續的 c 在上面取到最大值",
                          "by contradiction: suppose the right endpoint b still lies inside I, and choose a finite open interval containing b whose closure lies in I; that closure is compact, so c attains a maximum",
                          ACCENT_A,
                          "「緊」在這裡只做一件事：把一個連續函數換成一個數。有了那個數 c，下一拍的估計才有東西可以算",
                          "compactness does exactly one job here: it turns a continuous function into a single number, and the next beat's estimate needs a number to work with"))

 # ── beat 7: the radius bound climbing to 1/c ──────────────────────
 def _radius(self):
  ox, oy, sx, sy = -5.90, -0.62, 0.78, 1.28
  g = VGroup(self._frame(ox, oy, 3.52, 1.52, down=0.10))
  g.add(self._fcurve(ox, oy, sx, sy, lambda u: (10.0 ** u) / (M_B + (10.0 ** u) * C_B),
                     ACCENT_B, t0=0.0, t1=4.30, sw=3.0, n=180))
  g.add(self._dash([ox, oy + sy / C_B, 0], [ox + 3.42, oy + sy / C_B, 0], ACCENT_A, n=24, sw=1.5))
  g.add(self._sym(oy + sy / C_B + 0.22, "1 / c", ACCENT_A, FS_TAG - 3, x=ox + 2.90, w=0.80))
  for u in (0, 1, 2, 3, 4):
   g.add(self._sym(oy - 0.26, f"10{'⁰¹²³⁴'[u]}", DIM, FS_TAG - 4, x=ox + sx * u, w=0.52))
  g.add(self._sym(oy - 0.26, "r", DIM, FS_TAG - 3, x=ox + 3.60, w=0.34))
  g.add(self._table((("       r          r / ( m + r c )", DIM),)
                    + tuple((f"    {r:8.0f}         {b:.6f}", ACCENT_B) for r, b in RAD)
                    + ((f"    1 / c   =   {1.0 / C_B:.6f}", ACCENT_A),),
                    y0=0.92, dy=0.27, size=FS_TAG - 3))
  g.add(self._cap("右欄一路爬向橘線，卻永遠碰不到",
                  "the column climbs to the orange line without ever touching it"))
  return g.add(self._foot("定理 1.1 給的半徑上限是 r / ( m + r c )，把它改寫成 1 / ( c + m / r )：分母裡只有第二項跟 r 有關",
                          "the radius bound from Theorem 1.1 is r over m plus r c, which is one over c plus m over r, and only the second term in that denominator involves r",
                          ACCENT_A,
                          "關鍵在 A 是整個 W：球要多大有多大，r 沒有上限，所以 m / r 可以壓到任意小，上限就爬向 1 / c。這是整個證明唯一用到 A = W 的地方",
                          "the point is that A is the whole of W: the ball may be as large as we like, so m over r can be made as small as we please and the bound climbs to one over c, which is the only place A = W is used"))

 # ── beat 8: the overshoot ─────────────────────────────────────────
 def _clash(self):
  ox, oy, sx = -5.60, -0.16, 1.05
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.90, oy, 0], DIM, sw=3, tl=0.14))
  g.add(Line([ox, oy + 0.30, 0], [ox + sx * B_HYP, oy + 0.30, 0],
             color=ACCENT_A, stroke_width=4.0))
  g.add(self._sym(oy + 0.30, "J", ACCENT_A, FS_TAG - 3, x=ox + sx * B_HYP + 0.28, w=0.36))
  g.add(self._dash([ox + sx * B_HYP, oy - 0.50, 0], [ox + sx * B_HYP, oy + 0.52, 0],
                   ACCENT_A, n=8, sw=1.5))
  g.add(Line([ox + sx * T1H, oy - 0.26, 0], [ox + sx * (T1H + DELTA_H), oy - 0.26, 0],
             color=ACCENT_B, stroke_width=4.0))
  for xx, col, lab, w_, yy in ((B_HYP, ACCENT_A, "b", 0.34, -0.72),
                               (T1H, ACCENT_B, "t ₁", 0.46, -0.50),
                               (T1H + DELTA_H, ACCENT_B, "t ₁ + δ", 1.00, -0.50)):
   g.add(self._sym(oy + yy, lab, col, FS_TAG - 3, x=ox + sx * xx, w=w_))
  cx = ox + sx * (B_HYP + OVER / 2)
  g.add(Line([cx - 0.17, oy + 0.66, 0], [cx + 0.17, oy + 1.00, 0], color=WARN, stroke_width=3.4),
        Line([cx - 0.17, oy + 1.00, 0], [cx + 0.17, oy + 0.66, 0], color=WARN, stroke_width=3.4))
  g.add(self._table(((f"b − t ₁   =   {B_HYP - T1H:.2f}   <   1 / c   =   {1.0 / C_B:.2f}", ACCENT_B),
                     (f"δ   =   {DELTA_H:.2f}      ⇒      t ₁ + δ   =   {T1H + DELTA_H:.2f}", ACCENT_C),
                     (f"t ₁ + δ   >   b   =   {B_HYP:.2f}", WARN),
                     ("t ₁ + δ   ≤   b", ACCENT_A),
                     (f"{T1H + DELTA_H:.2f}   >   {B_HYP:.2f}     ⇒     b  ∉  I", WARN)),
                    y0=0.86, dy=0.34))
  g.add(self._cap("青線伸過橘虛線，而它不該伸過去",
                  "the blue bar reaches past the dashed line, which it must not do"))
  return g.add(self._foot("挑 t ₁ 使 b − t ₁ 小於 1 / c，上一拍就給得出 δ 讓 t ₁ + δ 超過 b。可是通過 ⟨ t ₁ , g ( t ₁ ) ⟩ 的極大解包含 g，所以必須 t ₁ + δ ≤ b",
                          "pick a point closer to b than one over c, and the previous beat supplies a delta carrying past b; but the maximal solution through that point contains the original, so it must not",
                          ACCENT_A,
                          "兩件事同時成立，矛盾，所以 b 不可能在 I 裡面——每條極大解的定義域只能是整個 I。這一拍是定理 1.4 的收口",
                          "both cannot hold, so b cannot lie inside I and every maximal solution has all of I for its domain, which closes Theorem 1.4"))

 # ── beat 9: the second-order equation as a rotation field ─────────
 def _system(self):
  cx, cy, s = -4.00, 0.06, 0.64
  g = VGroup(self._arr([cx - 1.42, cy, 0], [cx + 1.42, cy, 0], DIM, sw=3, tl=0.12),
             self._arr([cx, cy - 0.92, 0], [cx, cy + 1.02, 0], DIM, sw=3, tl=0.12))
  g.add(self._curve([[cx + s * math.cos(math.tau * k / 96),
                      cy + s * math.sin(math.tau * k / 96), 0] for k in range(97)],
                    ACCENT_A, sw=3.4))
  for k in range(8):
   th = math.tau * k / 8
   px, py = math.cos(th), math.sin(th)
   fx, fy = FC(px, py)
   n = math.hypot(fx, fy)
   g.add(self._arr([cx + s * px, cy + s * py, 0],
                   [cx + s * px + 0.34 * fx / n, cy + s * py + 0.34 * fy / n, 0],
                   ACCENT_B, sw=3, tl=0.11))
  # x(0) = 0 and x'(0) = 1, so the phase point starts at the TOP of the circle,
  # not the right: <alpha_1, alpha_2> is <x, x'>
  g.add(Dot([cx, cy + s, 0], radius=0.058, color=WARN))
  g.add(self._sym(cy + s + 0.24, "( 0 , 1 )", WARN, FS_TAG - 4, x=cx + 0.72, w=0.94))
  g.add(self._sym(cy - 0.24, "α ₁", DIM, FS_TAG - 3, x=cx + 1.60, w=0.48),
        self._sym(cy + 1.12, "α ₂", DIM, FS_TAG - 3, x=cx - 0.02, w=0.48))
  g.add(self._table((("d ⁿ α / d t ⁿ   =   G ( t , α , … , d ⁿ ⁻ ¹ α / d t ⁿ ⁻ ¹ )", ACCENT_A),
                     ("ψ f   =   ⟨ f , f ′ , … , f ⁽ ⁿ ⁻ ¹ ⁾ ⟩", ACCENT_C),
                     ("d α ᵢ / d t  =  α ᵢ ₊ ₁          d α ₙ / d t  =  G ( t , α )", ACCENT_B),
                     ("x ″  =  − x         x ( 0 ) = 0  ,  x ′ ( 0 ) = 1", ACCENT_B),
                     ("f ( t )  =  sin t          sin ² + cos ²  =  1", ACCENT_A)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("箭頭處處與圓相切，所以解就沿著圓跑",
                  "the arrows are tangent to the circle everywhere, so the solution runs round it"))
  return g.add(self._foot("n 階方程用 ψ 把 f 送到 f 與它的前 n − 1 階導數，方程就成了 f 的 n 階導數等於 G 帶入 t 與 ψ f；初始條件是 n 個值",
                          "the nth-order equation sends f to itself together with its first n minus one derivatives, so the equation reads: the nth derivative is G at t and that tuple, with n initial values",
                          ACCENT_A,
                          "化成一階系統的辦法很老：前面每一條都是「這個 α 的導數等於下一個 α」，只有最後一條帶 G。這裡 x ″ = − x 就變成平面上的旋轉場，解曲線正是單位圓",
                          "the reduction is ancient: each equation but the last says one coordinate's derivative is the next, and here the second-order equation becomes the rotation field whose solution curve is the unit circle"))

 # ── beat 10: theorem 1.5, and what the four theorems give ─────────
 def _close(self):
  ox, oy, sx, sy = -5.95, -0.30, 0.62, 0.52
  g = VGroup(self._arr([ox - 0.14, oy, 0], [ox + 3.76, oy, 0], DIM, sw=3, tl=0.14))
  g.add(self._fcurve(ox, oy, sx, sy, math.sin, ACCENT_A, t0=0.0, t1=5.90, sw=3.2, n=200))
  g.add(self._arr([ox + 3.50, oy + 0.30, 0], [ox + 3.76, oy + 0.30, 0], ACCENT_A, sw=3, tl=0.12))
  g.add(Dot([ox, oy, 0], radius=0.058, color=ACCENT_A))
  g.add(self._sym(oy + 0.84, "f ( t )  =  sin t", ACCENT_A, FS_TAG - 3, x=ox + 1.20, w=1.70))
  g.add(self._table((("1.1  ,  1.2      ⇒      1.5", ACCENT_B),
                     ("1.3              ⇒      ∃ !   f  =  ∪ 𝔉", ACCENT_C),
                     (f"c   ≡   {C_C:.4f}       ,      A  =  W ⁿ", ACCENT_B),
                     ("1.4              ⇒      J   =   I   =   ℝ", ACCENT_A)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("這一條沒有牆，一路走到底",
                  "this one meets no wall and runs the whole way"))
  return g.add(self._foot("化出來的 F 顯然局部一致 Lipschitz，所以定理 1.1 與 1.2 直接給出 n 階方程的存在唯一——這就是定理 1.5，證明只是把記號換掉",
                          "the F that comes out is plainly locally uniformly Lipschitz, so Theorems 1.1 and 1.2 hand over existence and uniqueness for the nth-order equation, which is Theorem 1.5",
                          ACCENT_A,
                          "接著定理 1.3 給極大解，而旋轉場的 c 恆等於 1、A 是整個平面，定理 1.4 就給出整條實數線。第 1 節到此結束，下一集是 §2「對參數的可微相依」",
                          "then Theorem 1.3 gives the maximal solution, and since the rotation field has c identically one with A the whole plane, Theorem 1.4 gives the whole real line; section 1 ends here"))

 def stage(self):
  a, b, c = self._patch(), self._union(), self._maximal()
  d, e, f_ = self._proper(), self._thm14(), self._pair()
  h, i, j = self._compact(), self._radius(), self._clash()
  k, l = self._system(), self._close()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE75ZH, AdvCalcE75EN = make(AdvCalcE75Base, "75", prefix="AdvCalcE")
