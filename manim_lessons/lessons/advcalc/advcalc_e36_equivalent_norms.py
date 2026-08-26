"""advcalc E36 -- chapter 3, section 4 (book pp. 132-134): norm isomorphism,
equivalent norms and the two-sided inequality that defines them, the failure of
equivalence in infinite dimensions, Theorem 4.1 (all norms on a finite
dimensional space are equivalent, proved only in chapter 4), Theorem 4.2 (a
linear map between finite dimensional spaces is bounded), Theorem 4.3 (Hom is
unchanged under equivalent norms), product norms and what pins them down,
Theorem 4.4, Lemma 4.1 (addition is bounded by one) and Theorem 4.5.  Book
pages 135-136 are exercises 4.1 to 4.18; E37 opens section 5.

Every constant the episode shows is the sharpest one, found by sweeping the
circle rather than quoted: the factors between the one, two and uniform norms,
the bound that Theorem 4.2's proof produces for a concrete matrix, and the
operator norm of addition, which comes out at exactly one because that
statement is the triangle inequality.  Beat 4's counterexample is integrated
numerically and checked against the closed form one over n plus one, so the
picture and the narration cannot drift apart.
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
STEPS = 96


def _n1(v):
 return abs(v[0]) + abs(v[1])


def _n2(v):
 return math.hypot(v[0], v[1])


def _nif(v):
 return max(abs(v[0]), abs(v[1]))


NORMS = (("₁", _n1), ("₂", _n2), ("∞", _nif))


def _circle(n=2880):
 for k in range(n):
  yield (math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))


def _sharp(f, g):
 """The smallest constant c with f <= c g, found rather than quoted."""
 return max(f(v) / g(v) for v in _circle())


# ── beat 3: the six constants between the three norms ──────────────────
CONST = {(a, b): _sharp(f, g) for a, f in NORMS for b, g in NORMS if a != b}
assert abs(CONST[("₁", "∞")] - 2) < 1e-6, "the sharp factor from uniform to one norm should be two"
assert abs(CONST[("₁", "₂")] - math.sqrt(2)) < 1e-6
assert abs(CONST[("₂", "∞")] - math.sqrt(2)) < 1e-6
for a, b in (("∞", "₁"), ("∞", "₂"), ("₂", "₁")):
 assert abs(CONST[(a, b)] - 1) < 1e-9, "this direction of the chain should need no factor at all"


def _reach(norm, th):
 c, s = math.cos(th), math.sin(th)
 return 1.0 / norm((c, s))


def _unit(norm, cx, cy, scale):
 pts = []
 for k in range(STEPS + 1):
  th = 2 * math.pi * k / STEPS
  r = _reach(norm, th) * scale
  pts.append([cx + r * math.cos(th), cy + r * math.sin(th), 0])
 return pts


# ── beat 4: t to the n, where the two norms come apart ─────────────────
POWERS = (1, 4, 16)
INT_N = 40000
ONE_NORMS = [sum((k / INT_N) ** n for k in range(INT_N)) / INT_N for n in POWERS]
for _n, _v in zip(POWERS, ONE_NORMS):
 assert abs(_v - 1.0 / (_n + 1)) < 1e-4, "the numerical one norm disagrees with one over n plus one"
RATIOS = [1.0 / v for v in ONE_NORMS]
assert RATIOS[0] < RATIOS[1] < RATIOS[2], "the ratio is supposed to be climbing"
assert RATIOS[-1] > 16, "the last ratio should already be large enough to make the point"

# ── beat 6: the bound Theorem 4.2's proof hands back ───────────────────
TMAT = ((2, -1), (1, 3))


def _ap(m, v):
 return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


ENTRY_MAX = max(abs(x) for r in TMAT for x in r)
PROOF_SHARP = max(_nif(_ap(TMAT, v)) / _n1(v) for v in _circle())
assert PROOF_SHARP <= ENTRY_MAX + 1e-9, "the proof's bound does not actually bound the map"
assert abs(PROOF_SHARP - ENTRY_MAX) < 1e-6, \
    "for this matrix the proof's bound is sharp, which is what the caption says"

# ── beat 10: addition, bounded by exactly one under the sum norm ───────
ADD_NORM = 0.0
for _i in range(240):
 for _j in range(240):
  _a = (math.cos(2 * math.pi * _i / 240), math.sin(2 * math.pi * _i / 240))
  _b = (math.cos(2 * math.pi * _j / 240), math.sin(2 * math.pi * _j / 240))
  ADD_NORM = max(ADD_NORM, _n2((_a[0] + _b[0], _a[1] + _b[1])) / (_n2(_a) + _n2(_b)))
assert abs(ADD_NORM - 1.0) < 1e-9, "addition should have operator norm exactly one"


class AdvCalcE36Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 36

 MODE_LABEL = {
  0: {"zh": "範數同構：兩邊都有界", "en": "norm isomorphic: bounded both ways"},
  1: {"zh": "兩個範數等價的定義", "en": "when two norms are equivalent"},
  2: {"zh": "互相夾住，就是恆等映射有界", "en": "each brackets the other"},
  3: {"zh": "幾何上：單位球互相包", "en": "geometrically, the balls nest"},
  4: {"zh": "無窮維會壞掉", "en": "infinite dimensions break it"},
  5: {"zh": "定理 4.1：有限維上全部等價", "en": "Theorem 4.1: in finite dimensions, all of them"},
  6: {"zh": "定理 4.2：有限維之間一定有界", "en": "Theorem 4.2: always bounded"},
  7: {"zh": "定理 4.3：Hom 不受影響", "en": "Theorem 4.3: Hom does not notice"},
  8: {"zh": "乘積空間該配什麼範數", "en": "what norm belongs on a product"},
  9: {"zh": "定理 4.4：三種乘積範數等價", "en": "Theorem 4.4: three product norms, all equivalent"},
  10: {"zh": "加法有界，直和看投影", "en": "addition is bounded; direct sums watch the projections"},
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

 def _ball(self, norm, cx, cy, scale, col, sw=2.5):
  return self._curve(_unit(norm, cx, cy, scale), col, sw=sw)

 def _frame(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 # ── beats ─────────────────────────────────────────────────────────
 def _iso(self):
  dx, rx, cy, s = -5.10, -1.95, 0.05, 0.34
  g = VGroup(self._frame(dx, cy, 0.95, 0.90), self._frame(rx, cy, 0.95, 0.90),
             self._ball(_n2, dx, cy, s, ACCENT_B),
             self._ball(_n1, rx, cy, s * 1.35, WARN))
  g.add(self._arr([dx + 1.15, cy + 0.30, 0], [rx - 1.15, cy + 0.30, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([rx - 1.15, cy - 0.30, 0], [dx + 1.15, cy - 0.30, 0], ACCENT_C, sw=2.5, tl=0.12),
        Text("V", font_size=FS_TAG - 2, color=DIM).move_to([dx, cy + 1.02, 0]),
        Text("W", font_size=FS_TAG - 2, color=DIM).move_to([rx, cy + 1.02, 0]))
  g.add(self._panel(((0.86, "一個線性雙射，去跟回都有界",
                      "one linear bijection, bounded going and coming back", ACCENT_A),
                     (0.20, "這種空間就當成同一個",
                      "such spaces are treated as the same one", ACCENT_C),
                     (-0.46, "只有一個方向有界不算",
                      "one direction alone does not count", DIM))))
  return g.add(self._foot("同一個空間上的兩個範數要怎麼算「一樣」，就從這裡引出來",
                          "what it means for two norms on one space to agree grows out of this",
                          ACCENT_A,
                          "把那個雙射取成恆等映射，就得到下一拍的定義",
                          "take the bijection to be the identity and the next definition appears"))

 def _defn(self):
  cx, cy, s = -3.55, 0.05, 0.62
  g = VGroup(self._frame(cx, cy, 1.35, 0.72))
  g.add(self._ball(_n1, cx, cy, s, WARN), self._ball(_n2, cx, cy, s, ACCENT_B))
  g.add(self._sym(-0.86, "p  ≤  a q          q  ≤  b p", ACCENT_A, FS_TAG - 1,
                  x=cx, w=3.40))
  g.add(self._panel(((0.86, "p 不超過 a 倍的 q",
                      "p is at most a times q", WARN),
                     (0.20, "而且 q 不超過 b 倍的 p",
                      "and q is at most b times p", ACCENT_B),
                     (-0.46, "兩個方向都要，缺一個就不是等價",
                      "both are needed; one alone is not equivalence", ACCENT_A))))
  return g.add(self._foot("這正是「恆等映射兩個方向都有界」，只是換個說法",
                          "this is the identity map being bounded both ways, said differently",
                          ACCENT_A,
                          "等價是一個等價關係，所以把範數分成一類一類的",
                          "equivalence really is an equivalence relation, so norms fall into classes"))

 def _bracket(self):
  cx, cy, s = -3.55, 0.05, 0.55
  g = VGroup(self._frame(cx, cy, 1.55, 0.72))
  g.add(self._ball(_n2, cx, cy, s * 0.72, DIM, sw=1.6),
        self._ball(_n1, cx, cy, s, WARN),
        self._ball(_n2, cx, cy, s * 1.45, DIM, sw=1.6))
  g.add(self._sym(-0.90, "( 1 / b ) q   ≤   p   ≤   a q", ACCENT_A, FS_TAG - 1,
                  x=cx, w=3.40))
  g.add(self._panel(((0.86, "把兩式合起來，就是被夾住",
                      "put the two together and it is bracketed", ACCENT_A),
                     (0.20, "紅色那顆球夾在兩顆灰球中間",
                      "the red ball sits between the two grey ones", WARN),
                     (-0.46, "任何一個都被另一個的兩個倍數夾住",
                      "either one is caught between two multiples of the other", DIM))))
  return g.add(self._foot("常數多大不重要，重要的是它們存在而且跟向量無關",
                          "the size of the constants does not matter; that they exist and are uniform does",
                          ACCENT_A,
                          "所以「哪個範數」不影響收斂、極限、連續這些概念",
                          "so convergence, limits and continuity cannot tell the two norms apart"))

 def _three(self):
  cx, cy, s = -3.55, 0.05, 0.72
  g = VGroup(self._frame(cx, cy, 1.55, 1.05))
  for (name, norm), col in zip(NORMS, (WARN, ACCENT_B, ACCENT_C)):
   g.add(self._ball(norm, cx, cy, s, col))
  rows = ((0.92, "斜正方形、圓、正方形", "a tilted square, a circle, an upright square", DIM),)
  g.add(self._panel(rows, x=PANEL_X, w=PANEL_W))
  for k, (a, b) in enumerate((("₁", "₂"), ("₂", "∞"), ("₁", "∞"))):
   g.add(self._sym(0.28 - k * 0.56,
                   f"‖ x ‖ {a}   ≤   {CONST[(a, b)]:.3f}  ‖ x ‖ {b}",
                   (WARN, ACCENT_B, ACCENT_C)[k], FS_TAG - 1, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這三個常數是掃過整個圓量出來的，而且都是最緊的",
                          "the three constants were measured round the whole circle and each is the tightest",
                          ACCENT_A,
                          "反方向都不必乘任何東西，所以三個範數兩兩等價",
                          "the other direction needs no factor at all, so the three are pairwise equivalent"))

 def _breaks(self):
  ox, oy, sx, sy = -5.40, -0.62, 3.10, 1.30
  g = VGroup(Line([ox - 0.16, oy, 0], [ox + sx + 0.24, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.14, 0], [ox, oy + sy + 0.20, 0], color=DIM, stroke_width=1.6),
             self._dash([ox, oy + sy, 0], [ox + sx, oy + sy, 0], DIM, n=24, sw=1.2))
  for n, col in zip(POWERS, (ACCENT_B, ACCENT_C, WARN)):
   g.add(self._curve([[ox + (t / 80) * sx, oy + (t / 80) ** n * sy, 0] for t in range(81)],
                     col, sw=3))
  g.add(Text("1", font_size=FS_TAG - 4, color=DIM).move_to([ox - 0.24, oy + sy, 0]))
  g.add(self._panel(((0.92, "一致範數永遠是 1，圖都碰到那條虛線",
                      "the uniform norm stays at one: every curve touches the line", ACCENT_A),
                     (0.34, "一範數是曲線底下的面積，越來越小",
                      "the one norm is the area underneath, and it shrinks", ACCENT_B)),
                    x=3.90, w=4.60))
  for k, (n, v) in enumerate(zip(POWERS, ONE_NORMS)):
   g.add(self._sym(-0.16 - k * 0.36, f"n = {n:2d}        {v:.4f}        {1 / v:5.1f}",
                   (ACCENT_B, ACCENT_C, WARN)[k], FS_TAG - 2, x=3.90, w=4.60))
  return g.add(self._foot("比值就是 n 加一，要多大有多大，所以這兩個範數不等價",
                          "the ratio is n plus one and grows without ceiling, so the two are not equivalent",
                          ACCENT_A,
                          "面積是數值積分算的，跟 n 加一分之一核對過",
                          "the areas were integrated numerically and checked against one over n plus one"))

 def _finite(self):
  cx, cy, s = -3.55, 0.05, 0.62
  g = VGroup(self._frame(cx, cy, 1.55, 1.05))
  for (name, norm), col in zip(NORMS, (WARN, ACCENT_B, ACCENT_C)):
   g.add(self._ball(norm, cx, cy, s, col, sw=1.8))
  g.add(self._ball(_n2, cx, cy, s * math.sqrt(2), DIM, sw=1.4),
        self._ball(_n2, cx, cy, s / math.sqrt(2), DIM, sw=1.4))
  g.add(self._panel(((0.86, "不管想出多奇怪的範數",
                      "however strange a norm you invent", ACCENT_B),
                     (0.20, "只要維數有限，它一定跟這些等價",
                      "in finite dimensions it is equivalent to these", ACCENT_A),
                     (-0.46, "證明要用到緊緻性，留到第 4 章",
                      "the proof needs compactness and waits for chapter 4", DIM))))
  return g.add(self._foot("這一條是後面很多章可以隨手換範數的根據",
                          "this is what lets later chapters swap norms without a second thought",
                          ACCENT_A,
                          "兩顆灰球說的是：任何單位球都夾得進兩顆同心的圓球之間",
                          "the grey circles say any unit ball can be caught between two round ones"))

 def _bounded(self):
  cx, cy, s = -3.55, 0.05, 0.30
  g = VGroup(self._frame(cx, cy, 1.35, 1.05))
  g.add(self._ball(_n1, cx, cy, s, ACCENT_B))
  img = [[cx + s * _ap(TMAT, v)[0], cy + s * _ap(TMAT, v)[1], 0]
         for v in ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 0))]
  g.add(self._curve(img, WARN, sw=3))
  g.add(self._ball(_nif, cx, cy, s * ENTRY_MAX, ACCENT_C, sw=2))
  g.add(self._panel(((0.86, "座標一取，映射就是一個矩陣",
                      "pick coordinates and the map becomes a matrix", ACCENT_B),
                     (0.20, "取矩陣元絕對值的最大值當常數",
                      "take the largest entry in size as the constant", ACCENT_C),
                     (-0.46, "這裡是 3，而且剛好是最緊的",
                      "here that is three, and it happens to be sharp", WARN))))
  return g.add(self._foot("有限維之間根本沒有不連續的線性映射，這在無窮維完全不成立",
                          "between finite dimensional spaces no linear map is discontinuous; not so beyond",
                          ACCENT_A,
                          "藍色是一範數的球、紫色是無窮範數的球，兩邊用的範數本來就可以不同",
                          "blue is a one norm ball and purple a uniform one: the two norms need not match"))

 def _homsame(self):
  g = VGroup()
  cols = ((-4.90, WARN, ACCENT_B), (-2.20, ACCENT_C, ACCENT_A))
  for cx, ca, cb in cols:
   g.add(self._frame(cx, 0.20, 0.95, 0.80),
         self._ball(_n1, cx, 0.20, 0.34, ca, sw=2),
         self._ball(_n2, cx, 0.20, 0.34 * 1.24, cb, sw=2))
  g.add(self._arr([-3.65, 0.20, 0], [-3.15, 0.20, 0], DIM, sw=2, tl=0.10))
  g.add(self._sym(-0.86, "Hom ( V , W )      =      Hom ( V , W )", ACCENT_A,
                  FS_TAG - 1, x=-3.55, w=4.20))
  g.add(self._panel(((0.86, "把範數換成等價的",
                      "replace a norm by an equivalent one", ACCENT_C),
                     (0.20, "有界的還是那一批映射，一個不多一個不少",
                      "exactly the same maps are bounded, no more and no fewer", ACCENT_A),
                     (-0.46, "誘導出來的兩個算子範數也彼此等價",
                      "and the two induced operator norms are equivalent too", ACCENT_B))))
  return g.add(self._foot("所以在有限維裡，「用哪個範數」從來不會影響結論",
                          "so in finite dimensions the choice of norm never changes the conclusion",
                          ACCENT_A,
                          "會影響的是常數的大小，不是哪些映射有界",
                          "what it changes is the size of the constants, not which maps are bounded"))

 def _product(self):
  lx, mx, s = -5.20, -2.40, 0.34
  g = VGroup()
  for cy, col, lab in ((0.62, ACCENT_B, "V"), (-0.52, ACCENT_C, "W")):
   g.add(self._frame(lx, cy, 0.55, 0.48), self._ball(_n2, lx, cy, s, col, sw=2),
         Text(lab, font_size=FS_TAG - 2, color=DIM).move_to([lx - 0.92, cy, 0]))
  g.add(self._frame(mx, 0.05, 0.95, 0.80), self._ball(_n1, mx, 0.05, s * 1.55, WARN, sw=2),
        Text("V × W", font_size=FS_TAG - 2, color=DIM).move_to([mx, 1.08, 0]))
  g.add(self._arr([-4.50, 0.44, 0], [-3.50, 0.20, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.50, -0.20, 0], [-4.50, -0.44, 0], DIM, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "要求只有一條：投影與嵌入都要連續",
                      "one requirement only: projections and injections continuous", ACCENT_A),
                     (0.20, "光是這條就把乘積範數定到等價為止",
                      "that alone pins the product norm down to equivalence", WARN),
                     (-0.46, "它一定跟「兩邊相加」那個等價",
                      "it must be equivalent to adding the two norms", ACCENT_C))))
  return g.add(self._foot("橘色是嵌入、灰色是投影，兩個方向都要有界",
                          "orange is an injection and grey a projection, and both must be bounded",
                          ACCENT_A,
                          "這是一個很典型的做法：用「要保住什麼」反過來決定結構",
                          "a typical move: let what must be preserved decide the structure"))

 def _three_product(self):
  cx, cy, s = -3.55, 0.05, 0.72
  g = VGroup(self._frame(cx, cy, 1.55, 1.05))
  for (name, norm), col in zip(NORMS, (WARN, ACCENT_B, ACCENT_C)):
   g.add(self._ball(norm, cx, cy, s, col))
  for k, (name, lab) in enumerate((("₁", "‖ α ‖ + ‖ ξ ‖"),
                                   ("₂", "( ‖ α ‖ ² + ‖ ξ ‖ ² ) ^ ½"),
                                   ("∞", "max { ‖ α ‖ , ‖ ξ ‖ }"))):
   g.add(self._sym(0.86 - k * 0.60, f"‖ · ‖ {name}      {lab}",
                   (WARN, ACCENT_B, ACCENT_C)[k], FS_TAG - 1, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("平面上這三個就是剛才那三顆球，所以是同一張圖",
                          "on the plane these three are the balls from before, so it is the same picture",
                          ACCENT_A,
                          "三個都是乘積範數，而且互相等價，用哪個都行",
                          "all three are product norms and all three are equivalent, so any will do"))

 def _add(self):
  cx, cy, s = -3.90, 0.05, 0.85
  g = VGroup(self._frame(cx, cy, 1.60, 0.70))
  a, b = (0.95, 0.45), (-0.25, 0.90)
  tip = (a[0] + b[0], a[1] + b[1])
  g.add(self._arr([cx, cy, 0], [cx + s * a[0], cy + s * a[1], 0], ACCENT_B, sw=2.5, tl=0.12),
        self._arr([cx + s * a[0], cy + s * a[1], 0], [cx + s * tip[0], cy + s * tip[1], 0],
                  ACCENT_C, sw=2.5, tl=0.12),
        self._arr([cx, cy, 0], [cx + s * tip[0], cy + s * tip[1], 0], WARN, sw=3, tl=0.12))
  g.add(self._sym(-0.86, f"‖ + ‖   =   {ADD_NORM:.0f}", ACCENT_A, FS_TAG - 1, x=cx, w=2.60))
  g.add(self._panel(((0.86, "紅色不會比藍加紫長",
                      "the red one is never longer than blue plus purple", WARN),
                     (0.20, "那就是三角不等式，所以界正好是 1",
                      "that is the triangle inequality, so the bound is exactly one", ACCENT_A),
                     (-0.46, "定理 4.5：是直和，恰好等於投影都有界",
                      "Theorem 4.5: a direct sum is exactly bounded projections", ACCENT_C))))
  return g.add(self._foot("加法是有界線性映射這件事，跟三角不等式是同一句話的兩種說法",
                          "addition being bounded and the triangle inequality are one statement twice",
                          ACCENT_A,
                          "第 3 章的工具到此齊了，下一集開始講無窮小",
                          "the machinery of chapter three is complete; next time, infinitesimals"))

 def stage(self):
  a, b, c = self._iso(), self._defn(), self._bracket()
  d, e, f = self._three(), self._breaks(), self._finite()
  h, i, j = self._bounded(), self._homsame(), self._product()
  k, l = self._three_product(), self._add()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE36ZH, AdvCalcE36EN = make(AdvCalcE36Base, "36", prefix="AdvCalcE")
