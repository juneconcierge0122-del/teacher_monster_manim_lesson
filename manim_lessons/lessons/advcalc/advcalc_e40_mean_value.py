"""advcalc E40 -- chapter 3, section 7, second part (book pp. 148-150): why the
one-variable mean value theorem has no exact analogue for vector values,
Theorem 7.3 (the inequality that replaces it) with the least-upper-bound proof,
Theorem 7.4 and the observation that only convexity was used, the corollary
that subtracts a fixed linear map, and the notation section -- the swap of
fixed variable between the directional derivative and the differential, the J
notation, and the second differential as a bilinear map.  Pages 151-152 are
exercises 7.1 to 7.15; E41 opens section 8.

The arc that carries the first three beats was picked so the failure of the
exact theorem is visible rather than argued: it has speed exactly one, so every
candidate mean value vector has length 2.2 while the chord it would have to
equal has length 1.78.  The module measures both and asserts the gap, and it
measures the sup of the differential's operator norm on a ball against the
worst actual change, which is Theorem 7.4's content.
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


# ── beats 0 to 4: an arc of speed exactly one ──────────────────────────
T0, T1 = 0.0, 2.2


def _f(t):
 return (math.sin(t), 1.0 - math.cos(t))


def _fp(t):
 return (math.cos(t), math.sin(t))


def _n2(v):
 return math.hypot(v[0], v[1])


SPEED = max(_n2(_fp(T0 + (T1 - T0) * k / 2000)) for k in range(2001))
assert abs(SPEED - 1.0) < 1e-12, "this arc was chosen because its speed is exactly one"
CHORD = _n2(tuple(a - b for a, b in zip(_f(T1), _f(T0))))
BOUND = SPEED * (T1 - T0)
assert CHORD < BOUND, "Theorem 7.3 fails on the drawn arc"
assert BOUND - CHORD > 0.3, "the gap has to be wide enough to see"

# every candidate mean value vector has length 2.2, so none of them is the chord
MISS = min(max(abs((_f(T1)[i] - _f(T0)[i]) - (T1 - T0) * _fp(c)[i]) for i in (0, 1))
           for c in (T0 + (T1 - T0) * k / 4000 for k in range(4001)))
assert MISS > 0.25, "an exact mean value point nearly exists, which would spoil the beat"
for _c in (T0 + (T1 - T0) * k / 200 for k in range(201)):
 assert abs(_n2(((T1 - T0) * _fp(_c)[0], (T1 - T0) * _fp(_c)[1])) - BOUND) < 1e-12, \
     "the candidates should all have the same length, which is why none of them fits"

# beat 3: the set A of the proof, for one concrete epsilon
EPS3 = 0.15


def _dist(x):
 return _n2(tuple(a - b for a, b in zip(_f(x), _f(T0))))


def _line3(x):
 return (SPEED + EPS3) * (x - T0) + EPS3


for _k in range(401):
 _x = T0 + (T1 - T0) * _k / 400
 assert _dist(_x) <= _line3(_x), "the whole interval should already lie in A for this epsilon"


# ── beats 5 to 8: Theorem 7.4 on a concrete map ────────────────────────
def _F(v):
 return (0.30 * v[0] * v[0] + 0.20 * v[1], 0.15 * v[0] * v[1])


def _J(v):
 return ((0.60 * v[0], 0.20), (0.15 * v[1], 0.15 * v[0]))


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


def _opn(m):
 return max(abs(m[0][0]) + abs(m[0][1]), abs(m[1][0]) + abs(m[1][1]))


BALL_R = 0.8
EPS4 = max(_opn(_J((BALL_R * math.cos(2 * math.pi * k / 720) * u,
                    BALL_R * math.sin(2 * math.pi * k / 720) * u)))
           for k in range(720) for u in (0.25, 0.5, 0.75, 1.0))
WORST = 0.0
for _k in range(180):
 _th = 2 * math.pi * _k / 180
 for _u in (0.2, 0.5, 0.8):
  _b = (0.35 * math.cos(_th) * _u, 0.35 * math.sin(_th) * _u)
  for _j in range(72):
   _ph = 2 * math.pi * _j / 72
   _xi = (0.30 * math.cos(_ph), 0.30 * math.sin(_ph))
   if _ninf((_b[0] + _xi[0], _b[1] + _xi[1])) > BALL_R:
    continue
   _d = tuple(p - q for p, q in zip(_F((_b[0] + _xi[0], _b[1] + _xi[1])), _F(_b)))
   WORST = max(WORST, _ninf(_d) / _ninf(_xi))
assert WORST <= EPS4 + 1e-9, "Theorem 7.4 fails on the drawn map, so the picture would lie"
assert WORST > 0.2 * EPS4, "the bound should not be so loose that the beat says nothing"

# beat 5: the pair that comes closest to the bound, so the picture is not slack.
# A first draft used a pair reaching only a quarter of the allowed circle, which
# read as though the theorem were saying almost nothing.
BETA = (-0.42, 0.0)
XI = (-0.26, 0.26)
SEG_D = tuple(p - q for p, q in zip(_F((BETA[0] + XI[0], BETA[1] + XI[1])), _F(BETA)))
assert _ninf((BETA[0] + XI[0], BETA[1] + XI[1])) <= BALL_R, "the far end left the ball"
assert _ninf(SEG_D) <= EPS4 * _ninf(XI) + 1e-12, "the drawn pair breaks the inequality"
assert _ninf(SEG_D) > 0.7 * EPS4 * _ninf(XI), "the drawn arrow should nearly fill the circle"


class AdvCalcE40Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 40

 MODE_LABEL = {
  0: {"zh": "精確的均值定理在這裡是錯的", "en": "the exact theorem is false here"},
  1: {"zh": "定理 7.3：改成一個不等式", "en": "Theorem 7.3: an inequality instead"},
  2: {"zh": "速率乘時間，蓋得住直線距離", "en": "speed times time covers the straight gap"},
  3: {"zh": "證明：先造一個集合", "en": "the proof: build a set first"},
  4: {"zh": "它的上界只能是右端點", "en": "its bound can only be the right endpoint"},
  5: {"zh": "定理 7.4：多變數的說法", "en": "Theorem 7.4: the many variable form"},
  6: {"zh": "證明就是把上一集接上來", "en": "the proof attaches the previous episode"},
  7: {"zh": "用到的只有凸性", "en": "only convexity was used"},
  8: {"zh": "推論：把一個固定的 T 減掉", "en": "the corollary: subtract a fixed T"},
  9: {"zh": "記號：固定住的變數對調", "en": "notation: which variable is pinned"},
  10: {"zh": "dF 自己也可以再微分一次", "en": "dF can be differentiated again"},
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

 def _circ(self, cx, cy, r, col, sw=2.5, n=96):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _arcpath(self, cx, cy, s, col, sw=3):
  base = _f(T0)
  return self._curve([[cx + s * (_f(T0 + (T1 - T0) * k / 90)[0] - base[0]),
                       cy + s * (_f(T0 + (T1 - T0) * k / 90)[1] - base[1]), 0]
                      for k in range(91)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _nopoint(self):
  cx, cy, s = -3.85, 0.12, 0.45
  g = VGroup(self._cross(cx, cy, 1.55, 1.00))
  base, end = _f(T0), _f(T1)
  ex, ey = cx + s * (end[0] - base[0]), cy + s * (end[1] - base[1])
  g.add(self._circ(cx, cy, s * BOUND, DIM, sw=1.6))
  for k in range(8):
   c = T0 + (T1 - T0) * k / 7
   v = ((T1 - T0) * _fp(c)[0], (T1 - T0) * _fp(c)[1])
   g.add(Line([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], color=ACCENT_C, stroke_width=1.4))
  g.add(self._arcpath(cx, cy, s, ACCENT_B))
  g.add(self._arr([cx, cy, 0], [ex, ey, 0], WARN, sw=3, tl=0.12),
        Dot([cx, cy, 0], radius=0.06, color=ACCENT_A), Dot([ex, ey, 0], radius=0.06, color=WARN))
  g.add(self._panel(((0.86, "紫色是所有候選：長度全部一樣",
                      "purple is every candidate, and they all have one length", ACCENT_C),
                     (0.20, "紅色是真正要湊出來的那一段",
                      "red is the vector they would have to reproduce", WARN),
                     (-0.46, "長度就對不上，所以那個點不存在",
                      "the lengths disagree, so no such point exists", ACCENT_A)),
                    x=3.75, w=4.90),
        self._sym(-1.00, f"{BOUND:.1f}    ≠    {CHORD:.2f}", ACCENT_A, FS_TAG - 1,
                  x=3.75, w=4.90))
  return g.add(self._foot("這條弧的速率恆等於一，所以每個候選向量的長度都是 2.2",
                          "this arc has speed exactly one, so every candidate vector has length 2.2",
                          ACCENT_A,
                          "而兩端的直線距離只有 1.78，最接近的候選還差 0.31",
                          "the straight gap is only 1.78, and the closest candidate still misses by 0.31"))

 def _thm73(self):
  cx, cy, s = -3.85, 0.12, 0.45
  g = VGroup(self._cross(cx, cy, 1.55, 1.00))
  base, end = _f(T0), _f(T1)
  ex, ey = cx + s * (end[0] - base[0]), cy + s * (end[1] - base[1])
  g.add(self._circ(cx, cy, s * BOUND, ACCENT_C, sw=2.5),
        self._arcpath(cx, cy, s, ACCENT_B),
        self._arr([cx, cy, 0], [ex, ey, 0], WARN, sw=3, tl=0.12),
        Dot([cx, cy, 0], radius=0.06, color=ACCENT_A), Dot([ex, ey, 0], radius=0.06, color=WARN))
  g.add(self._panel(((0.86, "紫色的球半徑是 m 乘上區間長度",
                      "the purple ball has radius m times the length", ACCENT_C),
                     (0.20, "定理說終點一定落在裡面",
                      "the theorem says the endpoint lands inside", WARN),
                     (-0.46, "不等式活下來了，等式沒有",
                      "the inequality survives where the equation did not", ACCENT_A)),
                    x=3.75, w=4.90))
  return g.add(self._foot("條件只要求「導數的範數處處不超過 m」，不必連續、不必有界變差",
                          "only the norm of the derivative is bounded; nothing else is required",
                          ACCENT_A,
                          "結論是一個球的包含關係，這是後面每一次估計的出發點",
                          "the conclusion is a containment, and every later estimate starts from it"))

 def _speed(self):
  ox, oy, sx, sy = -5.55, -0.55, 1.15, 0.62
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-0.15), Y(0), 0], [X(2.55), Y(0), 0], color=DIM, stroke_width=1.6),
             Line([ox, Y(-0.20), 0], [ox, Y(2.60), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(T1 * k / 120), Y(_dist(T1 * k / 120)), 0] for k in range(121)],
                    ACCENT_B, sw=3),
        Line([X(0), Y(0), 0], [X(T1), Y(BOUND), 0], color=ACCENT_C, stroke_width=2.5))
  g.add(Dot([X(T1), Y(CHORD), 0], radius=0.06, color=WARN),
        Dot([X(T1), Y(BOUND), 0], radius=0.06, color=ACCENT_C),
        self._dash([X(T1), Y(CHORD), 0], [X(T1), Y(BOUND), 0], ACCENT_A, n=5, sw=2))
  g.add(self._panel(((0.86, "青色是走到 x 為止的直線距離",
                      "teal is the straight distance travelled by x", ACCENT_B),
                     (0.20, "紫色是速率上限乘上時間",
                      "purple is the speed limit times the time", ACCENT_C),
                     (-0.46, "青色永遠壓在紫色下面",
                      "teal never rises above purple", WARN)),
                    x=3.90, w=4.60),
        self._sym(-0.94, f"{CHORD:.2f}    ≤    {BOUND:.1f}", ACCENT_A, FS_TAG - 1,
                  x=3.90, w=4.60))
  return g.add(self._foot("兩條線只在起點碰到，之後就分開——弧比直線長是一般情形",
                          "the two meet only at the start; an arc being longer than its chord is the rule",
                          ACCENT_A,
                          "相等只在弧本身是直線、而且速率跑滿上限時才發生",
                          "equality needs the arc to be straight and to run at the limit throughout"))

 def _setA(self):
  ox, oy, sx, sy = -5.55, -0.55, 1.15, 0.55
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-0.15), Y(0), 0], [X(2.55), Y(0), 0], color=DIM, stroke_width=1.6),
             Line([ox, Y(-0.20), 0], [ox, Y(3.10), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(T1 * k / 120), Y(_dist(T1 * k / 120)), 0] for k in range(121)],
                    ACCENT_B, sw=3),
        Line([X(0), Y(_line3(0)), 0], [X(T1), Y(_line3(T1)), 0], color=WARN, stroke_width=2.5))
  g.add(Line([X(0), Y(-0.16), 0], [X(T1), Y(-0.16), 0], color=ACCENT_A, stroke_width=6),
        Dot([X(0), Y(-0.16), 0], radius=0.055, color=ACCENT_A),
        Dot([X(T1), Y(-0.16), 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "紅線是放寬過的上界，比 m 多一個 ε",
                      "red is the relaxed bound: m with an epsilon added", WARN),
                     (0.20, "青色留在紅線下面的那些 x，就是集合 A",
                      "the x where teal stays under red make up the set A", ACCENT_B),
                     (-0.46, "橘色那一段就是 A，起點附近一定有一小段",
                      "orange is A, and a piece of it near the start always exists", ACCENT_A))))
  return g.add(self._foot("多出來的那個 ε 是為了讓 A 一開始就非空，最後再讓它趨於零",
                          "the extra epsilon is what makes A nonempty to begin with; it goes to zero at the end",
                          ACCENT_A,
                          "這是實分析裡「用最小上界逼到底」的標準寫法，值得看熟",
                          "this is the standard least upper bound argument, and it is worth knowing by sight"))

 def _lub(self):
  ox, oy, sx, sy = -5.55, -0.30, 1.15, 0.55
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-0.15), Y(0), 0], [X(2.55), Y(0), 0], color=DIM, stroke_width=1.6))
  L = 1.35
  g.add(self._curve([[X(T1 * k / 120), Y(_dist(T1 * k / 120)), 0] for k in range(121)],
                    ACCENT_B, sw=3),
        Line([X(0), Y(_line3(0)), 0], [X(T1), Y(_line3(T1)), 0], color=WARN, stroke_width=2.5))
  g.add(self._dash([X(L), Y(-0.18), 0], [X(L), Y(_line3(L) + 0.25), 0], ACCENT_C, n=8, sw=2),
        Dot([X(L), Y(_dist(L)), 0], radius=0.06, color=ACCENT_C),
        Text("l", font_size=FS_TAG - 4, color=ACCENT_C).move_to([X(L), Y(-0.42), 0]))
  g.add(self._arr([X(L), Y(_dist(L)) - 0.30, 0], [X(L + 0.45), Y(_dist(L)) - 0.30, 0],
                  ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "假設上界 l 落在右端點左邊",
                      "suppose the bound l lies left of the right endpoint", ACCENT_C),
                     (0.20, "導數在 l 還在，斜率還是小於 m 加 ε",
                      "the derivative still exists at l, with slope under m plus epsilon", ACCENT_B),
                     (-0.46, "所以還能往右推一小段，仍然留在紅線下面",
                      "so one can push right a little and stay under the red line", ACCENT_A))))
  return g.add(self._foot("推出來的點也在 A 裡，這跟「l 是上界」矛盾，所以 l 只能是右端點",
                          "that point is in A too, contradicting l being an upper bound, so l is the right end",
                          ACCENT_A,
                          "在右端點得到帶 ε 的不等式，最後讓 ε 趨於零就是定理",
                          "at the right end the inequality holds with epsilon, and letting it vanish is the theorem"))

 def _thm74(self):
  dx, dy, ds = -5.15, 0.05, 1.15
  rx, ry, rs = -1.90, 0.05, 2.30
  g = VGroup(self._cross(dx, dy, 1.05, 0.95), self._cross(rx, ry, 1.55, 0.95),
             Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx - 0.95, 0.90, 0]),
             Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx - 1.45, 0.90, 0]))
  g.add(self._circ(dx, dy, ds * BALL_R, ACCENT_C, sw=2))
  bx, by = dx + ds * BETA[0], dy + ds * BETA[1]
  ex, ey = dx + ds * (BETA[0] + XI[0]), dy + ds * (BETA[1] + XI[1])
  g.add(Line([bx, by, 0], [ex, ey, 0], color=ACCENT_A, stroke_width=3),
        Dot([bx, by, 0], radius=0.06, color=WARN), Dot([ex, ey, 0], radius=0.06, color=ACCENT_B))
  fb, fe = _F(BETA), _F((BETA[0] + XI[0], BETA[1] + XI[1]))
  g.add(self._circ(rx, ry, rs * EPS4 * _ninf(XI), ACCENT_C, sw=2),
        self._arr([rx, ry, 0], [rx + rs * (fe[0] - fb[0]), ry + rs * (fe[1] - fb[1]), 0],
                  WARN, sw=3, tl=0.12),
        Dot([rx, ry, 0], radius=0.06, color=WARN))
  g.add(self._arr([dx + 1.20, dy - 0.68, 0], [rx - 1.70, ry - 0.68, 0], DIM, sw=2, tl=0.10))
  g.add(self._panel(((0.92, "左邊：球裡取兩點，連成線段",
                      "left: two points of the ball and the segment between them", ACCENT_A),
                     (0.34, "右邊：兩個像的差",
                      "right: the difference of the two images", WARN),
                     (-0.24, "紫圈半徑就是 ε 乘上位移的範數",
                      "the purple radius is epsilon times the displacement's norm", ACCENT_C)),
                    x=3.90, w=4.60),
        self._sym(-0.82, f"{_ninf(SEG_D):.3f}    ≤    {EPS4 * _ninf(XI):.3f}", ACCENT_A,
                  FS_TAG - 1, x=3.90, w=4.60))
  return g.add(self._foot("紅色箭頭留在紫圈裡，這就是定理 7.4 說的事",
                          "the red arrow stays inside the purple circle, which is what Theorem 7.4 says",
                          ACCENT_A,
                          "兩個數字都是程式掃出來的，ε 取的是球上微分算子範數的上確界",
                          "both numbers were swept out here, epsilon being the sup of the operator norm"))

 def _proof74(self):
  ox, oy = -3.90, 0.30
  g = VGroup()
  lines = (("λ ( t )  =  β + t ξ          t ∈ [ 0 , 1 ]", ACCENT_C),
           ("γ ( t )  =  F ( λ ( t ) )          γ ′ ( t )  =  dF ( ξ )", ACCENT_B),
           ("‖ γ ′ ( t ) ‖  ≤  ε ‖ ξ ‖          ⇒          ‖ γ ( 1 ) − γ ( 0 ) ‖  ≤  ε ‖ ξ ‖", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.82 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "線段本身就是一條參數化弧",
                      "the segment is itself a parametrized arc", ACCENT_C),
                     (0.20, "定理 7.2 給出它的切向量",
                      "Theorem 7.2 supplies its tangent vector", ACCENT_B),
                     (-0.46, "再套定理 7.3 就結束了",
                      "then Theorem 7.3 closes it", WARN))))
  return g.add(self._foot("多變數的估計，最後都化成沿一條線段的一變數估計",
                          "a many variable estimate always ends up a one variable estimate along a segment",
                          ACCENT_A,
                          "這就是為什麼上一集要先把弧與方向導數講清楚",
                          "which is why arcs and directional derivatives had to come first"))

 def _convex(self):
  g = VGroup()
  cx1, cy1 = -4.95, 0.10
  g.add(self._blob(cx1, cy1, 1.05, 0.72, 0.10, ACCENT_B))
  p1, p2 = (cx1 - 0.72, cy1 + 0.30), (cx1 + 0.78, cy1 - 0.28)
  g.add(Line([p1[0], p1[1], 0], [p2[0], p2[1], 0], color=ACCENT_A, stroke_width=3),
        Dot([p1[0], p1[1], 0], radius=0.055, color=ACCENT_A),
        Dot([p2[0], p2[1], 0], radius=0.055, color=ACCENT_A))
  cx2, cy2 = -1.75, 0.10
  moon = []
  for k in range(73):
   th = -1.25 + 2.50 * k / 72
   moon.append([cx2 + 1.05 * math.cos(th), cy2 + 0.90 * math.sin(th), 0])
  for k in range(73):
   th = 1.25 - 2.50 * k / 72
   moon.append([cx2 + 0.40 + 0.72 * math.cos(th), cy2 + 0.62 * math.sin(th), 0])
  g.add(self._curve(moon + [moon[0]], WARN, sw=2.5, maxn=200))
  q1, q2 = (cx2 + 0.28, cy2 + 0.82), (cx2 + 0.28, cy2 - 0.82)
  g.add(Line([q1[0], q1[1], 0], [q2[0], q2[1], 0], color=ACCENT_A, stroke_width=3),
        Dot([q1[0], q1[1], 0], radius=0.055, color=ACCENT_A),
        Dot([q2[0], q2[1], 0], radius=0.055, color=ACCENT_A))
  g.add(self._panel(((0.86, "左邊：任兩點的線段都在裡面",
                      "left: every segment between two points stays inside", ACCENT_B),
                     (0.20, "右邊：這一條就跑出去了",
                      "right: this one leaves the set", WARN),
                     (-0.46, "定理只需要左邊那個性質，不必是球",
                      "the theorem needs only the left property, never a ball", ACCENT_A))))
  return g.add(self._foot("證明裡球只被用到一次，就是「線段整條都在裡面」",
                          "the ball was used exactly once in the proof, to keep the segment inside",
                          ACCENT_A,
                          "所以把「球」換成「凸集」，同一句話原封不動成立",
                          "so replacing ball by convex set leaves the statement untouched"))

 def _corollary(self):
  cx, cy, s = -3.85, 0.10, 1.45
  g = VGroup(self._cross(cx, cy, 1.65, 0.95))
  # the image of a small square under F, against the image under a fixed linear T
  T = _J((0.0, 0.0))
  corners = ((1, 1), (1, -1), (-1, -1), (-1, 1))
  r = 0.45
  fp = [[cx + s * (_F((r * v[0], r * v[1]))[0] - _F((0.0, 0.0))[0]),
         cy + s * (_F((r * v[0], r * v[1]))[1] - _F((0.0, 0.0))[1]), 0] for v in corners]
  tp = [[cx + s * (T[0][0] * r * v[0] + T[0][1] * r * v[1]),
         cy + s * (T[1][0] * r * v[0] + T[1][1] * r * v[1]), 0] for v in corners]
  g.add(self._curve(tp + [tp[0]], ACCENT_C, sw=2.5),
        self._curve(fp + [fp[0]], WARN, sw=3))
  g.add(self._panel(((0.86, "紫色是固定的線性映射 T 的像",
                      "purple is the image under the fixed linear map T", ACCENT_C),
                     (0.20, "紅色是真正的變化量",
                      "red is the actual change", WARN),
                     (-0.46, "微分跟 T 差多少，兩者就差多少",
                      "they differ by as much as the differential differs from T", ACCENT_A))))
  return g.add(self._foot("證明只有一行：令 F 等於 G 減 T，再用定理 7.4",
                          "the proof is one line: set F to G minus T and apply Theorem 7.4",
                          ACCENT_A,
                          "下一節證「連續偏微分推出可微」時，用的就是這一條推論",
                          "the next section's proof that continuous partials give differentiability uses exactly this"))

 def _notation(self):
  cx, cy, w, h = -3.70, 0.10, 1.55, 0.80
  g = VGroup(self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                          [cx - w, cy + h, 0], [cx - w, cy - h, 0]], DIM, sw=1.8))
  g.add(Line([cx - w, cy + 0.34, 0], [cx + w, cy + 0.34, 0], color=ACCENT_B, stroke_width=3),
        Line([cx - 0.62, cy - h, 0], [cx - 0.62, cy + h, 0], color=WARN, stroke_width=3))
  g.add(Dot([cx - 0.62, cy + 0.34, 0], radius=0.075, color=ACCENT_A),
        Text("α", font_size=FS_TAG - 3, color=DIM).move_to([cx, cy - h - 0.30, 0]),
        Text("ξ", font_size=FS_TAG - 3, color=DIM).move_to([cx - w - 0.28, cy, 0]))
  g.add(self._panel(((0.92, "藍色：把 α 固定，得到 dF 下標 α",
                      "blue: pin alpha down and get dF sub alpha", ACCENT_B),
                     (0.34, "紅色：把 ξ 固定，得到 D 下標 ξ 的 F",
                      "red: pin xi down and get D sub xi of F", WARN),
                     (-0.24, "同一張表，兩種切法，交點是同一個值",
                      "one table, two ways of slicing, the same value where they cross", ACCENT_A))))
  return g.add(self._foot("這就是為什麼書上特別提「兩個記號裡下標的位置剛好對調」",
                          "this is why the book points out that the subscripts swap positions",
                          ACCENT_A,
                          "第三種寫法把函數本身放進下標，寫成 J 下標 F，把 F 挪出視線",
                          "a third notation puts the function itself in the subscript, as J sub F"))

 def _second(self):
  g = VGroup()
  boxes = ((-5.05, "V", ACCENT_B), (-2.85, "Hom ( V , W )", ACCENT_C), (-0.35, "ω ( ξ , η )", WARN))
  for cx, lab, col in boxes:
   half = 0.55 if lab == "V" else 1.05
   g.add(self._curve([[cx - half, 0.62, 0], [cx + half, 0.62, 0], [cx + half, 0.06, 0],
                      [cx - half, 0.06, 0], [cx - half, 0.62, 0]], col, sw=1.8),
         self._sym(0.34, lab, col, FS_TAG + 1, x=cx, w=2.00))
  g.add(self._arr([-4.35, 0.34, 0], [-3.95, 0.34, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-1.75, 0.34, 0], [-1.45, 0.34, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._sym(-0.46, "dF : A → Hom ( V , W )          d ² F ₐ  =  d ( dF ) ₐ",
                  DIM, FS_TAG - 1, x=-2.75, w=5.10))
  g.add(self._panel(((0.86, "dF 本身是一個映射，所以可以再問一次可微",
                      "dF is a map, so the question can be asked again", ACCENT_B),
                     (0.20, "它的微分落在 Hom 的 Hom 裡",
                      "its differential lands in a Hom of a Hom", ACCENT_C),
                     (-0.46, "照對偶來看，那就是一個雙線性映射",
                      "by duality that is exactly a bilinear map", WARN))))
  return g.add(self._foot("二階微分在這本書後面會用來寫 Taylor 展開與極值的判別",
                          "the second differential later carries Taylor expansions and the tests for extrema",
                          ACCENT_A,
                          "第 3 章第 7 節到此結束，下一集講微分與乘積空間",
                          "that ends section 7; next time, the differential and product spaces"))

 def stage(self):
  a, b, c = self._nopoint(), self._thm73(), self._speed()
  d, e, f = self._setA(), self._lub(), self._thm74()
  h, i, j = self._proof74(), self._convex(), self._corollary()
  k, l = self._notation(), self._second()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE40ZH, AdvCalcE40EN = make(AdvCalcE40Base, "40", prefix="AdvCalcE")
