"""advcalc E34 -- chapter 3, section 3, first part (book pp. 126-128): the
epsilon-delta definition carried over from the real line to normed spaces,
continuity at a point, Lipschitz continuity, Lipschitz functions, bounded
linear mappings, the warning that "bounded" here does not mean the range is a
bounded set, the integral as a bounded linear functional, Theorem 3.1 and
Lemma 3.1.  Book page 129 onward is exercises 3.1 to 3.22; E35 takes the
operator norm from page 128.

Everything the pictures claim is computed here rather than drawn by eye.  The
Lipschitz constant 3 for x squared about 1 is measured on the interval that is
actually drawn and checked to be the smallest one; the deltas it hands back are
checked to work; the square root is checked to escape every cone; the delta of
beat 1 is found by bisection rather than placed by hand.  The linear map's
smallest bound is found by sweeping the unit sphere, which is how the last two
beats can say honestly that the proof of Theorem 3.1 returns 6 where 3 would
have done -- a bound, not the bound.
"""
import math
from fractions import Fraction
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20


# ── beats 1 and 2: a curve with a hole, and the delta that goes with it ──
def _g(u):
 return 0.42 * u + 0.06 * u ** 3


G_ALPHA = 1.2                       # where the hole is
G_BETA = _g(G_ALPHA)                # the limit, which is not the value there
G_EPS = 0.34


def _solve(target, lo, hi):
 """The u where the increasing curve reaches `target`."""
 for _ in range(60):
  mid = (lo + hi) / 2
  lo, hi = (mid, hi) if _g(mid) < target else (lo, mid)
 return (lo + hi) / 2


G_DELTA = min(_solve(G_BETA + G_EPS, G_ALPHA, 3.0) - G_ALPHA,
              G_ALPHA - _solve(G_BETA - G_EPS, -3.0, G_ALPHA))
assert 0.30 < G_DELTA < 0.80, "the delta drawn in beats 1 and 2 is off the picture"
for _k in range(-200, 201):
 _u = G_ALPHA + G_DELTA * _k / 201
 assert abs(_g(_u) - G_BETA) < G_EPS, "the delta band lets the curve out of the epsilon band"


# ── beats 3 and 4: x squared about 1 is Lipschitz with constant 3 ────────
LIP_A, LIP_R, LIP_C = 1.0, 1.0, 3


def _sq(x):
 return x * x


_worst = max(abs(_sq(LIP_A + t) - _sq(LIP_A)) / abs(t)
             for t in (k / 400 for k in range(-399, 400)) if t)
assert _worst <= LIP_C, "x squared is not Lipschitz with constant 3 where the cone is drawn"
assert _worst > LIP_C - 0.01, "3 is not the smallest constant, so the cone would sit loose"

EPSILONS = (Fraction(3, 2), Fraction(1, 2))
DELTAS = [min(Fraction(e, LIP_C), Fraction(LIP_R)) for e in EPSILONS]
for _e, _d in zip(EPSILONS, DELTAS):
 _m = max(abs(_sq(LIP_A + float(_d) * k / 200) - _sq(LIP_A)) for k in range(-199, 200))
 assert _m < _e, "the delta that the Lipschitz constant hands back does not work"


# ── beat 5: the square root escapes every cone at the origin ────────────
SQRT_CS = (1, 2, 4)
for _c in SQRT_CS:
 _x = 1.0 / (2 * _c * _c)
 assert math.sqrt(_x) > _c * _x, "the square root should beat every straight line near zero"
 assert abs(math.sqrt(1.0 / _c ** 2) - _c * (1.0 / _c ** 2)) < 1e-12, \
     "the crossing point drawn for this cone is not where the two meet"


# ── beats 6 to 9: one concrete linear map, both spaces uniformly normed ──
TMAT = ((2, -1), (1, 1))


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


def _T(v):
 return (TMAT[0][0] * v[0] + TMAT[0][1] * v[1],
         TMAT[1][0] * v[0] + TMAT[1][1] * v[1])


def _sphere(n=720):
 """The unit sphere of the uniform norm, one point per direction."""
 for k in range(n):
  c, s = math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)
  m = max(abs(c), abs(s))
  yield (c / m, s / m)


BOUND = max(_ninf(_T(p)) for p in _sphere())
assert abs(BOUND - max(sum(abs(x) for x in r) for r in TMAT)) < 1e-9, \
    "the sup over the unit sphere disagrees with the largest row sum"

RAY = (1, -1)                       # the direction that attains the bound
RAY_XS = (1, 2, 3)
_r0 = _ninf(_T(RAY)) / _ninf(RAY)
assert abs(_r0 - BOUND) < 1e-12, "this ray was picked because it attains the bound"
for _x in RAY_XS:
 _v = (_x * RAY[0], _x * RAY[1])
 assert abs(_ninf(_T(_v)) - _x * _ninf(_T(RAY))) < 1e-12, \
     "the image is supposed to scale exactly with the vector"
 assert abs(_ninf(_T(_v)) / _ninf(_v) - _r0) < 1e-12, \
     "the quotient is supposed to be constant along a ray, which is the whole point"

DELTA_1 = Fraction(1, 3)            # the largest delta that works for epsilon = 1
PROOF_C = 2 / DELTA_1               # what the proof of Theorem 3.1 hands back
assert float(DELTA_1) * BOUND <= 1 + 1e-12, "this delta does not keep the image inside epsilon = 1"
assert float(DELTA_1) * BOUND >= 1 - 1e-12, "a larger delta would have worked, so this is not the largest"
assert PROOF_C > BOUND, "the proof's bound is supposed to be valid but not the smallest"


# ── beat 8: the integral as a bounded linear functional on C([0, 2]) ────
INT_A, INT_B, INT_N = 0.0, 2.0, 6000


def _bump(t):
 return math.sin(math.pi * t / 2) ** 2


INT_SUP = max(_bump(INT_A + (INT_B - INT_A) * k / INT_N) for k in range(INT_N + 1))
INT_VAL = sum(_bump(INT_A + (INT_B - INT_A) * k / INT_N)
              for k in range(INT_N)) * (INT_B - INT_A) / INT_N
assert abs(INT_SUP - 1.0) < 1e-9, "the drawn function should have uniform norm one"
assert abs(INT_VAL - 1.0) < 1e-3, "its integral should come out at one"
assert INT_VAL < (INT_B - INT_A) * INT_SUP, "the bound is supposed to be strict for this f"


# ── beat 10: the norm is Lipschitz with constant one ────────────────────
LEM_A, LEM_B = (2.2, 0.3), (0.5, 0.9)


def _n2(v):
 return math.hypot(v[0], v[1])


LEM_GAP = abs(_n2(LEM_A) - _n2(LEM_B))
LEM_SEG = _n2((LEM_A[0] - LEM_B[0], LEM_A[1] - LEM_B[1]))
assert LEM_GAP < LEM_SEG, "the drawn pair has no visible slack in the reverse triangle inequality"

_norms = (lambda v: abs(v[0]) + abs(v[1]), _n2, _ninf)
for _i in range(-6, 7):
 for _j in range(-6, 7):
  for _p in range(-6, 7):
   for _q in range(-6, 7):
    _a, _b = (_i / 3, _j / 3), (_p / 3, _q / 3)
    _d = (_a[0] - _b[0], _a[1] - _b[1])
    for _n in _norms:
     assert abs(_n(_a) - _n(_b)) <= _n(_d) + 1e-12, "Lemma 3.1 fails on some pair"


class AdvCalcE34Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 34

 MODE_LABEL = {
  0: {"zh": "同一個定義，只換掉一個符號", "en": "the same definition, one symbol changed"},
  1: {"zh": "極限：α 自己被挖掉", "en": "the limit: alpha itself is removed"},
  2: {"zh": "在 α 連續", "en": "continuous at alpha"},
  3: {"zh": "在一點 Lipschitz 連續", "en": "Lipschitz continuous at a point"},
  4: {"zh": "δ 有現成公式，不必再湊", "en": "delta now comes with a formula"},
  5: {"zh": "連續，但不是 Lipschitz", "en": "continuous, but not Lipschitz"},
  6: {"zh": "線性映射：條件塌成一句話", "en": "a linear map: the condition collapses"},
  7: {"zh": "「有界」不是值域有界", "en": "bounded does not mean the range is bounded"},
  8: {"zh": "積分是有界線性泛函", "en": "the integral is a bounded functional"},
  9: {"zh": "定理 3.1：三件事是同一件事", "en": "Theorem 3.1: three conditions, one thing"},
  10: {"zh": "引理 3.1：範數自己是 Lipschitz 的", "en": "Lemma 3.1: the norm is itself Lipschitz"},
 }

 # ── small shared pieces ───────────────────────────────────────────
 def _panel(self, rows, x=PANEL_X, w=PANEL_W):
  g = VGroup()
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=x, w=w))
  return g

 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _square(self, cx, cy, r, col, sw=2.5):
  """The ball of the uniform norm: a square, drawn as one closed path."""
  p = [[cx + r, cy + r, 0], [cx - r, cy + r, 0],
       [cx - r, cy - r, 0], [cx + r, cy - r, 0], [cx + r, cy + r, 0]]
  return self._curve(p, col, sw=sw)

 def _frame(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 # ── beats ─────────────────────────────────────────────────────────
 def _carry(self):
  g = VGroup()
  ax, ay = -3.90, 0.72
  g.add(Line([ax - 1.70, ay, 0], [ax + 1.70, ay, 0], color=DIM, stroke_width=2),
        Dot([ax, ay, 0], radius=0.055, color=WARN))
  for s in (-1, 1):
   g.add(Line([ax + s * 0.90, ay - 0.13, 0], [ax + s * 0.90, ay + 0.13, 0],
              color=ACCENT_C, stroke_width=2))
  g.add(Text("a", font_size=FS_TAG - 3, color=WARN).move_to([ax, ay + 0.26, 0]),
        Text("ℝ", font_size=FS_TAG - 1, color=DIM).move_to([ax - 2.05, ay, 0]))

  bx, by, R = -3.90, -0.42, 0.60
  g.add(self._curve([[bx + R * math.cos(2 * math.pi * k / 72),
                      by + R * math.sin(2 * math.pi * k / 72), 0] for k in range(73)],
                    ACCENT_C, sw=2.5),
        Dot([bx, by, 0], radius=0.055, color=WARN),
        Text("α", font_size=FS_TAG - 3, color=WARN).move_to([bx - 0.24, by + 0.02, 0]),
        Text("V", font_size=FS_TAG - 1, color=DIM).move_to([bx - 2.05, by, 0]),
        self._arr([bx, by, 0], [bx + R * 0.92, by, 0], WARN, sw=2, tl=0.10))
  g.add(self._arr([-2.55, 0.52, 0], [-2.55, -0.22, 0], ACCENT_B, sw=3, tl=0.14))
  g.add(self._panel(((0.86, "定義一個字都不用改，只換符號",
                      "not one word changes, only the symbol", ACCENT_B),
                     (0.20, "定義域放寬成 V 的任意子集",
                      "the domain is relaxed to any subset of V", ACCENT_A),
                     (-0.46, "第 1 節的極限定理照樣成立",
                      "the limit theorems of section 1 carry over", DIM))))
  return g.add(self._foot("實數上的 ε-δ 一整段搬到賦範空間，沒有新東西要學",
                          "the whole of the real epsilon delta story moves across unchanged",
                          ACCENT_A,
                          "出發與到達都是賦範空間，兩邊的範數寫成同一個記號",
                          "both spaces are normed, and both norms are written with the same sign"))

 def _graph(self, punctured):
  ox, oy, sx, sy = -3.50, 0.05, 1.15, 0.68
  X = lambda u: ox + u * sx
  Y = lambda v: oy + v * sy
  g = VGroup(self._frame(ox, oy, 2.30, 0.90))
  eps, dlt = G_EPS * sy, G_DELTA * sx
  bx, byv = X(G_ALPHA), Y(G_BETA)
  for s in (-1, 1):
   g.add(self._dash([X(-1.95), byv + s * eps, 0], [X(1.95), byv + s * eps, 0], ACCENT_A, n=26, sw=1.6),
         self._dash([bx + s * dlt, Y(-1.18), 0], [bx + s * dlt, Y(1.18), 0], ACCENT_C, n=18, sw=1.6))
  lo = [[X(u / 100), Y(_g(u / 100)), 0] for u in range(-195, int(G_ALPHA * 100) - 2)]
  hi = [[X(u / 100), Y(_g(u / 100)), 0] for u in range(int(G_ALPHA * 100) + 3, 196)]
  g.add(self._curve(lo, ACCENT_B, sw=3), self._curve(hi, ACCENT_B, sw=3))
  if punctured:
   g.add(Dot([bx, byv, 0], radius=0.075, color=INK),
         Dot([bx, byv, 0], radius=0.048, color="#0b0e14"),
         Dot([bx, Y(G_BETA + 0.62), 0], radius=0.065, color=WARN))
  else:
   g.add(Dot([bx, byv, 0], radius=0.070, color=WARN))
  g.add(self._dash([X(-1.95), byv, 0], [bx, byv, 0], DIM, n=24, sw=1.2),
        Text("β", font_size=FS_TAG - 3, color=ACCENT_A).move_to([X(-1.95) - 0.24, byv, 0]),
        Text("α", font_size=FS_TAG - 3, color=ACCENT_C).move_to([bx, Y(-1.15), 0]))
  return g, X, Y

 def _limit(self):
  g, X, Y = self._graph(True)
  g.add(self._panel(((0.86, "距離要大於零：α 那一點被挖掉",
                      "the distance must exceed zero: alpha is removed", ACCENT_C),
                     (0.20, "所以 f 在 α 的值是多少都不影響",
                      "so whatever value f takes at alpha does not matter", WARN),
                     (-0.46, "極限問的是靠近時的行為",
                      "a limit asks what happens on the way in", DIM))))
  return g.add(self._foot("紅點是 f 在 α 的值，它高高在上，極限一樣存在",
                          "the red dot is the value at alpha, sitting well away, and the limit survives",
                          WARN,
                          "畫面上的 δ 是解出來的，不是擺上去的",
                          "the delta on screen was solved for, not placed by hand"))

 def _cont(self):
  g, X, Y = self._graph(False)
  g.add(self._panel(((0.86, "極限存在，而且剛好等於 f 在 α 的值",
                      "the limit exists and equals the value at alpha", WARN),
                     (0.20, "「大於零」可以拿掉了",
                      "the greater than zero can now be dropped", ACCENT_B),
                     (-0.46, "ξ 等於 α 時差是零向量，本來就小於 ε",
                      "at xi equal to alpha the difference is zero anyway", DIM))))
  return g.add(self._foot("洞補起來，函數就在這一點連續——差別只在一個點的值",
                          "fill the hole and the function is continuous here: one value is all it took",
                          ACCENT_B,
                          "每一點都連續就叫連續，ξ 跑遍整個定義域",
                          "continuous everywhere is just this at every point of the domain"))

 def _cone(self, with_bands):
  ox, oy, sx, sy = -3.40, 0.05, 1.45, 0.32
  X = lambda x: ox + (x - LIP_A) * sx
  Y = lambda y: oy + (y - _sq(LIP_A)) * sy
  g = VGroup(self._frame(ox, oy, 1.55, 1.00))
  for s in (-1, 1):
   g.add(Line([ox, oy, 0], [X(LIP_A + 1), Y(_sq(LIP_A) + s * LIP_C), 0],
              color=ACCENT_C, stroke_width=2),
         Line([ox, oy, 0], [X(LIP_A - 1), Y(_sq(LIP_A) - s * LIP_C), 0],
              color=ACCENT_C, stroke_width=2))
  g.add(self._curve([[X(x / 100), Y(_sq(x / 100)), 0] for x in range(0, 201)], ACCENT_B, sw=4),
        Dot([ox, oy, 0], radius=0.06, color=WARN),
        Dot([X(2.0), Y(_sq(2.0)), 0], radius=0.06, color=ACCENT_A))
  if with_bands:
   e, d = float(EPSILONS[0]), float(DELTAS[0])
   for s in (-1, 1):
    g.add(self._dash([X(0.02), Y(1 + s * e), 0], [X(1.98), Y(1 + s * e), 0], ACCENT_A, n=22, sw=1.6),
          self._dash([X(LIP_A + s * d), Y(-1.00), 0], [X(LIP_A + s * d), Y(3.05), 0], WARN, n=16, sw=1.6))
  return g, X, Y

 def _lipschitz(self):
  g, X, Y = self._cone(False)
  g.add(self._panel(((0.86, "兩個函數值的距離，被兩個自變數的距離控制住",
                      "the gap in values is controlled by the gap in arguments", ACCENT_C),
                     (0.20, "那個常數就是這個錐形的開口",
                      "the constant is the opening of this cone", ACCENT_B),
                     (-0.46, "曲線只要待在錐形裡就成立",
                      "the condition says only that the curve stays inside", DIM))))
  return g.add(self._foot("錐形的斜率 3 是量出來的，而且是最小的可用值",
                          "the slope three was measured on this interval, and it is the smallest that works",
                          ACCENT_A,
                          "只要求在 α 附近成立，離遠了不管",
                          "it is only required near alpha, and says nothing further out"))

 def _delta(self):
  g, X, Y = self._cone(True)
  rows = ((0.86, "先給 ε，再拿 ε 除以 c 當 δ",
           "hand over epsilon, then take epsilon over c as delta", ACCENT_A),)
  g.add(self._panel(rows))
  for k, (e, d) in enumerate(zip(EPSILONS, DELTAS)):
   g.add(self._sym(0.22 - k * 0.58, f"ε = {e}        →        δ = {d}",
                   WARN if k == 0 else DIM, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("上一集為 x 平方湊了一個 δ，這裡是照公式算出來的",
                          "last time a delta for x squared was hunted for; here it is read off a formula",
                          ACCENT_B,
                          "ε 太大時 δ 會被那個半徑截掉，所以取兩者的小者",
                          "for a large epsilon the radius cuts delta down, hence the smaller of the two"))

 def _sqrt(self):
  ox, oy, sx, sy = -5.15, -0.62, 3.55, 1.32
  X = lambda x: ox + x * sx
  Y = lambda y: oy + y * sy
  g = VGroup(Line([ox - 0.20, oy, 0], [X(1.06), oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.16, 0], [ox, Y(1.08), 0], color=DIM, stroke_width=1.6))
  for c, col in zip(SQRT_CS, (DIM, ACCENT_C, WARN)):
   xe = min(1.0, 1.0 / c)
   g.add(Line([ox, oy, 0], [X(xe), Y(c * xe), 0], color=col, stroke_width=2),
         Dot([X(1.0 / c ** 2), Y(1.0 / c), 0], radius=0.05, color=col),
         Text(f"c = {c}", font_size=FS_TAG - 4, color=col)
         .move_to([X(xe) + 0.30, Y(c * xe), 0]))
  g.add(self._curve([[X(x / 400), Y(math.sqrt(x / 400)), 0] for x in range(0, 401)],
                    ACCENT_B, sw=3))
  g.add(self._panel(((0.86, "每一條直線都會被曲線在原點附近超過",
                      "every straight line is overtaken near the origin", ACCENT_B),
                     (0.20, "比值等於根號 x 分之一，沒有上界",
                      "the quotient is one over the square root, with no ceiling", WARN),
                     (-0.46, "所以在零點連續卻不 Lipschitz",
                      "so it is continuous at zero and not Lipschitz there", ACCENT_C)),
                    x=3.75, w=4.80))
  return g.add(self._foot("Lipschitz 嚴格強於連續，這是最短的反例",
                          "Lipschitz is strictly stronger than continuous, and this is the shortest witness",
                          ACCENT_A,
                          "點是兩者相交的地方，左邊那一段曲線都在直線上方",
                          "the dots mark where the two meet, and left of each the curve is above"))

 def _linear(self):
  cx, cy, s = -3.60, 0.05, 0.32
  g = VGroup(self._frame(cx, cy, 1.20, 1.05))
  g.add(self._square(cx, cy, s, ACCENT_B))
  img = [[cx + s * _T(v)[0], cy + s * _T(v)[1], 0]
         for v in ((1, 1), (1, -1), (-1, -1), (-1, 1), (1, 1))]
  g.add(self._curve(img, WARN, sw=3))
  g.add(self._square(cx, cy, s * BOUND, ACCENT_C, sw=2))
  g.add(Dot([cx + s * BOUND, cy, 0], radius=0.055, color=ACCENT_A),
        Dot([cx - s * BOUND, cy, 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "藍色是單位球，紅色是它的像",
                      "blue is the unit ball, red is its image", WARN),
                     (0.20, "紫色是半徑 c 的球，像整個裝得進去",
                      "purple is the ball of radius c, and the image fits inside", ACCENT_C),
                     (-0.46, "橘點是碰到的地方，所以 c 不能再小",
                      "the orange dots are where they touch, so c cannot shrink", ACCENT_A))))
  return g.add(self._foot("兩點的值相減就是差向量的像，所以只要看一個向量就夠",
                          "the difference of two values is the image of the difference, so one vector suffices",
                          ACCENT_B,
                          "這個 c 就是下一集要定義的算子範數",
                          "this c is the operator norm that the next episode defines"))

 def _unbounded(self):
  dx, dy, ds = -5.15, 0.05, 0.24
  rx, ry, rs = -1.75, 0.05, 0.20
  g = VGroup(self._frame(dx, dy, 0.90, 0.90), self._frame(rx, ry, 2.10, 0.90),
             Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.80, 0.86, 0]),
             Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx - 1.90, 0.86, 0]))
  g.add(self._square(rx, ry, rs * 4.5, DIM, sw=1.6))
  far = (RAY_XS[-1] * RAY[0], RAY_XS[-1] * RAY[1])
  g.add(self._arr([dx, dy, 0], [dx + ds * far[0], dy + ds * far[1], 0], DIM, sw=2, tl=0.10),
        self._arr([rx, ry, 0], [rx + rs * _T(far)[0] + 0.14, ry, 0], DIM, sw=2, tl=0.10))
  for x, col in zip(RAY_XS, (ACCENT_B, ACCENT_C, WARN)):
   v = (x * RAY[0], x * RAY[1])
   w = _T(v)
   g.add(Dot([dx + ds * v[0], dy + ds * v[1], 0], radius=0.06, color=col),
         Dot([rx + rs * w[0], ry + rs * w[1], 0], radius=0.06, color=col),
         Text(f"{x if x > 1 else ''}α", font_size=FS_TAG - 5, color=col)
         .move_to([dx + ds * v[0] - 0.30, dy + ds * v[1] + 0.14, 0]),
         Text(f"{int(_ninf(w))}", font_size=FS_TAG - 5, color=col)
         .move_to([rx + rs * w[0], ry + 0.28, 0]))
  g.add(self._panel(((0.92, "向量放大幾倍，像就放大幾倍",
                      "scale the vector and the image scales the same way", WARN),
                     (0.34, "所以值域跑得出任何一顆球",
                      "so the range escapes every ball you draw", ACCENT_C),
                     (-0.24, "不變的是那個商，一直是 3",
                      "what stays put is the quotient, and it reads three", ACCENT_A)),
                    x=3.90, w=4.60),
        self._sym(-0.82, "3 / 1  =  6 / 2  =  9 / 3  =  3", ACCENT_A, FS_TAG - 1,
                  x=3.90, w=4.60))
  return g.add(self._foot("「有界」講的是商有界，不是值域有界，這是這一節最容易誤會的字",
                          "bounded refers to the quotient, not the range: the most misread word here",
                          ACCENT_A,
                          "灰色那顆球是隨便畫的，第二、第三個像已經在外面",
                          "the grey ball was drawn arbitrarily and the last two images are already outside"))

 def _integral(self):
  ox, oy, sx, sy = -5.30, -0.60, 1.85, 1.20
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.18, oy, 0], [X(2.20), oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.16, 0], [ox, Y(1.30), 0], color=DIM, stroke_width=1.6))
  g.add(self._dash([ox, Y(1.0), 0], [X(2.0), Y(1.0), 0], ACCENT_C, n=26, sw=2),
        self._dash([X(2.0), oy, 0], [X(2.0), Y(1.0), 0], ACCENT_C, n=8, sw=2))
  curve = [[X(t / 200), Y(_bump(t / 200)), 0] for t in range(0, 401)]
  g.add(self._curve(curve, ACCENT_B, sw=3))
  for k in range(1, 40):
   t = 2.0 * k / 40
   g.add(Line([X(t), oy, 0], [X(t), Y(_bump(t)), 0], color=ACCENT_B, stroke_width=1.1))
  g.add(Text("b − a", font_size=FS_TAG - 4, color=ACCENT_C).move_to([X(1.0), Y(1.16), 0]))
  g.add(self._panel(((0.86, "矩形的面積是區間長度乘上一致範數",
                      "the rectangle is the length times the uniform norm", ACCENT_C),
                     (0.20, "陰影的面積是積分本身",
                      "the shading is the integral itself", ACCENT_B),
                     (-0.46, "2 是界，1 是這個 f 的值",
                      "two is the bound and one is this f's value", ACCENT_A)),
                    x=3.90, w=4.60))
  return g.add(self._foot("常數函數 1 會把矩形填滿，所以區間長度是取得到的最小界",
                          "the constant one fills the rectangle, so the length is a bound that is attained",
                          ACCENT_A,
                          "換一個範數，這個界就會變，界永遠是對某一對範數說的",
                          "change either norm and the bound changes: a bound is always relative to a pair"))

 def _theorem(self):
  g = VGroup()
  boxes = ((-4.85, 0.72, "在一點連續", "continuous at a point", ACCENT_B),
           (-1.85, 0.72, "處處連續", "continuous", ACCENT_C),
           (-3.35, -0.50, "有界", "bounded", WARN))
  pts = []
  for x, y, zh, en, col in boxes:
   lab = self._mid(y, zh, en, col, FS_TAG, x=x, w=2.20)
   g.add(lab, self._curve([[x - 1.15, y - 0.28, 0], [x + 1.15, y - 0.28, 0],
                           [x + 1.15, y + 0.28, 0], [x - 1.15, y + 0.28, 0],
                           [x - 1.15, y - 0.28, 0]], col, sw=1.8))
   pts.append((x, y))
  g.add(self._arr([-4.85, 0.42, 0], [-3.90, -0.20, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-2.80, -0.20, 0], [-1.90, 0.42, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.00, 0.72, 0], [-3.68, 0.72, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._sym(-1.00, f"δ = {DELTA_1}        C = 2 / δ = {PROOF_C}", DIM, FS_TAG - 1,
                  x=-3.35, w=3.60))
  g.add(self._panel(((0.86, "三個箭頭繞成一圈，三件事就完全等價",
                      "the three arrows close a circle, so the three agree", ACCENT_A),
                     (0.20, "從一點連續造出界，用的只有線性",
                      "linearity alone turns one point into a bound", ACCENT_B),
                     (-0.46, "最後一步是把 ε 除以 C 當 δ，倒回去",
                      "the last step takes epsilon over C as delta, going back", DIM))))
  return g.add(self._foot("線性映射沒有「只在這裡連續」這種事，一點連續就處處連續",
                          "a linear map cannot be continuous only here: one point forces everywhere",
                          ACCENT_A,
                          "這是線性帶來的剛性，一般的函數完全沒有這種性質",
                          "that rigidity comes from linearity, and ordinary functions have nothing like it"))

 def _lemma(self):
  cx, cy, s = -3.50, 0.05, 0.42
  g = VGroup(self._frame(cx, cy, 1.20, 1.05))
  for v, col in ((LEM_A, ACCENT_C), (LEM_B, WARN)):
   R = _n2(v) * s
   g.add(self._curve([[cx + R * math.cos(2 * math.pi * k / 72),
                       cy + R * math.sin(2 * math.pi * k / 72), 0] for k in range(73)],
                     col, sw=1.6),
         self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=2.5, tl=0.12))
  g.add(Line([cx + s * LEM_A[0], cy + s * LEM_A[1], 0],
             [cx + s * LEM_B[0], cy + s * LEM_B[1], 0], color=ACCENT_B, stroke_width=3))
  g.add(Text("α", font_size=FS_TAG - 4, color=ACCENT_C)
        .move_to([cx + s * LEM_A[0] + 0.22, cy + s * LEM_A[1] + 0.20, 0]),
        Text("β", font_size=FS_TAG - 4, color=WARN)
        .move_to([cx + s * LEM_B[0] + 0.26, cy + s * LEM_B[1] + 0.26, 0]))
  g.add(self._panel(((0.86, "兩圈的半徑差，就是兩個範數的差",
                      "the gap between the two circles is the gap in the norms", ACCENT_C),
                     (0.20, "藍線的長度，是兩個向量的差的範數",
                      "the blue segment is the norm of their difference", ACCENT_B),
                     (-0.46, f"這一對量出來是 {LEM_GAP:.2f} 對 {LEM_SEG:.2f}",
                      f"this pair measures {LEM_GAP:.2f} against {LEM_SEG:.2f}", ACCENT_A))))
  return g.add(self._foot("常數是一，而且已經是最小的：α 與 β 同向時兩邊就相等",
                          "the constant is one and cannot be lowered: the two agree when alpha and beta line up",
                          ACCENT_A,
                          "下一集把「最小的界」正式定義成算子範數",
                          "next time the smallest bound gets a name of its own: the operator norm"))

 def stage(self):
  cr, lm, ct = self._carry(), self._limit(), self._cont()
  lp, dl, sq = self._lipschitz(), self._delta(), self._sqrt()
  ln, ub, ig = self._linear(), self._unbounded(), self._integral()
  th, le = self._theorem(), self._lemma()
  return [([cr], []), ([lm], [cr]), ([ct], [lm]), ([lp], [ct]),
          ([dl], [lp]), ([sq], [dl]), ([ln], [sq]), ([ub], [ln]),
          ([ig], [ub]), ([th], [ig]), ([le], [th])]


AdvCalcE34ZH, AdvCalcE34EN = make(AdvCalcE34Base, "34", prefix="AdvCalcE")
