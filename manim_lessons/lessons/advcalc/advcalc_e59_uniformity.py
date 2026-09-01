"""advcalc E59 -- chapter 4, section 5 (book pp. 210-214): compactness and
uniformity.  The word "uniform" is a reversal of quantifiers, and the section's
subject is how often a compact domain upgrades a pointwise property into a
uniform one.  It ends with two results that identify sequential compactness with
the Heine-Borel property on a metric space, and with the corollary that separates
finite from infinite dimensions: a normed space is finite-dimensional exactly
when its closed unit ball is sequentially compact.  Pages 214-215 are exercises
5.1 to 5.14.

Five beats carry computations.  The three standard failures -- x to the n, one
over x, and the sine of one over x -- are each exhibited with the numbers that
make them fail, and the third is the interesting one: it is bounded as well as
continuous, so boundedness is not what is missing.  The tent functions are
checked to converge pointwise while every supremum stays at one, the book's
family of non-overlapping peaks is checked to have all mutual uniform distances
equal to one, and the closing beat computes an actual Lebesgue number for a
concrete covering and then computes a radius that is too large.
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


# ── beat 2: pointwise but not uniformly ────────────────────────────────
POW = [(n, 0.5 ** n, 0.99 ** n) for n in (2, 10, 50)]
for _n, _mid, _hi in POW:
 assert _hi > 0.5, "near one the values stay high, so the supremum is one"
assert POW[-1][1] < 1e-14, "while at any fixed point the values fall to zero"


# ── beat 3: continuous and bounded, still not uniformly continuous ─────
def _wiggle(x):
 return math.sin(1.0 / x)


PAIRS = []
for _k in (2, 8, 32):
 _a = 1.0 / (2 * math.pi * _k + math.pi / 2)
 _b = 1.0 / (2 * math.pi * _k + 3 * math.pi / 2)
 PAIRS.append((_a - _b, abs(_wiggle(_a) - _wiggle(_b))))
for _gap, _jump in PAIRS:
 assert _gap > 0 and abs(_jump - 2.0) < 1e-9, \
     "the two points must straddle a full swing of the sine"
assert PAIRS[-1][0] < 1e-3, "and they have to get arbitrarily close together"
assert all(abs(_wiggle(1.0 / (10 + k))) <= 1.0 for k in range(50)), "it is bounded"


# ── beat 5: tents on a compact domain ──────────────────────────────────
def _tent(n, x):
 lo, hi = 1.0 / n, 2.0 / n
 if not (lo < x < hi):
  return 0.0
 mid = 1.5 / n
 return (x - lo) / (mid - lo) if x <= mid else (hi - x) / (hi - mid)


TENTS = []
for _n in (2, 6, 20):
 _sup = max(_tent(_n, k / 4000.0) for k in range(4001))
 TENTS.append((_n, _sup, _tent(_n, 0.70)))
for _n, _sup, _at in TENTS:
 assert abs(_sup - 1.0) < 1e-6, "every tent still has height one"
assert TENTS[0][2] > 0.5 and TENTS[-1][2] == 0.0, \
    "at a fixed point the values start high and then vanish for good"


# ── beat 6: one compact set makes the distance positive ────────────────
CIRC_LINE = 1.0
_probe = min(math.hypot(math.cos(2 * math.pi * k / 720) - 0.0,
                        math.sin(2 * math.pi * k / 720) - 2.0) for k in range(720))
assert abs(_probe - CIRC_LINE) < 1e-6, "the circle and the line y = 2 are one apart"


# ── beats 7 and 8: totally bounded, and a ball that is not ─────────────
DENSE_N = 8
GRID = [i / DENSE_N for i in range(1, DENSE_N)]
for _k in range(1, 4000):
 _x = _k / 4000.0
 assert min(abs(_x - g) for g in GRID) < 1.0 / DENSE_N, \
     "the grid is not r-dense in the interval after all"


def _peak(n, x):
 """The book's peak: base from 1/(2n+2) to 1/(2n), apex at 1/(2n+1)."""
 lo, mid, hi = 1.0 / (2 * n + 2), 1.0 / (2 * n + 1), 1.0 / (2 * n)
 if not (lo < x < hi):
  return 0.0
 return (x - lo) / (mid - lo) if x <= mid else (hi - x) / (hi - mid)


PEAK_NS = (1, 2, 3, 5)
# the apexes sit at 1/(2n+1) and would fall between grid points, so a uniform
# grid alone reports a supremum a little under one
SAMP = sorted([k / 20000.0 for k in range(20001)]
              + [1.0 / (2 * n + 1) for n in PEAK_NS])
for _i in PEAK_NS:
 assert abs(max(_peak(_i, x) for x in SAMP) - 1.0) < 1e-3, "each peak has height one"
 for _j in PEAK_NS:
  if _i == _j:
   continue
  assert max(_peak(_i, x) * _peak(_j, x) for x in SAMP) == 0.0, "the peaks must not overlap"
  _sep = max(abs(_peak(_i, x) - _peak(_j, x)) for x in SAMP)
  assert abs(_sep - 1.0) < 1e-3, "so their uniform distance is one"
PEAK_GAP = 1.0


# ── beat 10: an actual Lebesgue number, and one that is too large ──────
COVER = ((0.0, 0.60), (0.40, 1.0))
GOOD_R, BAD_R = 0.09, 0.11


def _fits(p, r):
 lo, hi = p - r, p + r
 return any(a <= max(lo, 0.0) and min(hi, 1.0) <= b for a, b in COVER)


assert all(_fits(k / 2000.0, GOOD_R) for k in range(2001)), \
    "the smaller radius should be a Lebesgue number for this covering"
assert not _fits(0.5, BAD_R), "and the larger one should fail in the middle"


class AdvCalcE59Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 59

 MODE_LABEL = {
  0: {"zh": "「均勻」就是把量詞反過來", "en": "uniform means reversing quantifiers"},
  1: {"zh": "逐點收斂與均勻收斂", "en": "pointwise and uniform convergence"},
  2: {"zh": "逐點推不出均勻", "en": "pointwise does not give uniform"},
  3: {"zh": "連續、有界，仍然不均勻", "en": "continuous, bounded, still not uniform"},
  4: {"zh": "定理 5.1：緊緻就補得起來", "en": "Theorem 5.1: compactness repairs it"},
  5: {"zh": "可是收斂補不起來", "en": "but it does not repair convergence"},
  6: {"zh": "定理 5.2：距離變成正的", "en": "Theorem 5.2: the distance turns positive"},
  7: {"zh": "r 稠密與全有界", "en": "r-dense, and totally bounded"},
  8: {"zh": "無窮維的單位球蓋不住", "en": "the infinite-dimensional ball resists"},
  9: {"zh": "有限維的分界線", "en": "where finite dimensions end"},
  10: {"zh": "Lebesgue 數，兩種緊緻接起來", "en": "a Lebesgue number joins the two"},
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

 def _circ(self, cx, cy, r, col, sw=2.0, n=80):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plot(self, f, ox, oy, sx, sy, col, sw=2.4, n=200, x0=0.0, x1=1.0, clip=None):
  pts = []
  for k in range(n + 1):
   x = x0 + (x1 - x0) * k / n
   v = f(x)
   if clip is not None:
    v = min(v, clip)
   pts.append([ox + sx * (x - x0) / (x1 - x0), oy + sy * v, 0])
  return self._curve(pts, col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _quantifiers(self):
  g = VGroup()
  rows = (("( ∀ y ∈ A ) ( ∀ c ) ( ∃ d )   Q", DIM),
          ("( ∀ c ) ( ∃ d ) ( ∀ y ∈ A )   Q", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._rect(-3.55, 0.52 - k * 0.86, 2.35, 0.30, col),
         self._sym(0.52 - k * 0.86, lab, col, FS_TAG + 1, x=-3.55, w=4.50))
  g.add(self._arr([-3.55, 0.10, 0], [-3.55, -0.12, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "上面那一行：d 可以隨著 y 變",
                      "the upper line lets d change with y", DIM),
                     (0.20, "下面那一行：一個 d 對所有 y 都行",
                      "the lower one asks one d to serve every y", WARN),
                     (-0.46, "差別只在兩個量詞的順序",
                      "the whole difference is the order of two quantifiers", ACCENT_A))))
  return g.add(self._foot("均勻連續就是這樣來的：δ 只依賴 ε，不依賴那個「主張連續的點」",
                          "uniform continuity is exactly this: delta depends on epsilon and not on the point",
                          ACCENT_A,
                          "第 3 章第 14 節已經看過，這個順序一換，那個性質就強得多",
                          "section 3.14 already showed how much stronger the property becomes once reversed"))

 def _convergence(self):
  ox, oy = -5.85, -0.55
  sx, sy = 4.30, 1.40
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.10, 0], color=DIM, stroke_width=1.4))
  base = lambda x: 0.55 * math.sin(2.6 * x) + 0.20
  g.add(self._plot(base, ox, oy, sx, sy, ACCENT_A, sw=2.6))
  for e, col in ((0.30, ACCENT_B), (0.16, ACCENT_C), (0.07, WARN)):
   g.add(self._plot(lambda x, e=e: base(x) + e * (1 + 0.8 * math.sin(9 * x)),
                    ox, oy, sx, sy, col, sw=1.8))
  g.add(self._panel(((0.86, "逐點收斂：每個點各有各的 N",
                      "pointwise: each point gets its own N", DIM),
                     (0.20, "均勻收斂：一個 N 對所有點都行",
                      "uniform: one N serves every point at once", WARN),
                     (-0.46, "等價於一致範數下的距離掉到零",
                      "which is the distance in the uniform norm falling to zero", ACCENT_A))))
  return g.add(self._foot("這就是那個上確界範數叫「一致範數」的原因——它量的正好是「處處都靠近」",
                          "that is why the least upper bound norm is called the uniform norm: it measures closeness everywhere at once",
                          ACCENT_A,
                          "畫面上三條彩色的曲線一條比一條貼近底下那條橘色的，可是貼近的方式才是重點",
                          "the three curves close in on the orange one, and how they close in is the point"))

 def _powers(self):
  ox, oy = -5.85, -0.60
  sx, sy = 4.30, 1.60
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.12, 0], color=DIM, stroke_width=1.4))
  for n, col in ((2, ACCENT_B), (10, ACCENT_C), (50, WARN)):
   g.add(self._plot(lambda x, n=n: x ** n, ox, oy, sx, sy, col, sw=2.4))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * 1.06, oy + sy, 0], DIM, n=20, sw=1.2))
  rows = [("        n            x = 0.5          x = 0.99", DIM)]
  for n, mid, hi in POW:
   rows.append((f"      {n:4d}          {mid:.2e}          {hi:.4f}", ACCENT_C))
  g.add(self._table(rows, y0=0.80, dy=0.36))
  g.add(self._mid(-0.66, "每一點都掉到零，可是上確界永遠是一",
                  "every point falls to zero while the supremum stays at one", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("固定一個點，值掉得飛快；可是把點往一挪，值又爬回來——所以沒有一個 N 對所有點都行",
                          "fix a point and the values crash, but move the point toward one and they climb back, so no single N serves everywhere",
                          ACCENT_A,
                          "定義域是開區間零到一，它不是緊緻的；可是下一拍會看到，緊緻也救不了收斂這件事",
                          "the domain here is the open unit interval, which is not compact; the next beat shows that compactness would not help anyway"))

 def _wiggly(self):
  ox, oy = -5.85, 0.05
  sx, sy = 4.30, 0.70
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  g.add(self._plot(lambda x: math.sin(1.0 / max(x, 1e-4)), ox, oy, sx, sy, ACCENT_C,
                   sw=2.0, n=3000, x0=0.010, x1=1.0))
  for f, col in ((1.0, WARN), (-1.0, WARN)):
   g.add(self._dash([ox, oy + sy * f, 0], [ox + sx * 1.06, oy + sy * f, 0], col, n=20, sw=1.0))
  rows = [("        k            x − y              | Δ f |", DIM)]
  for k, (gap, jump) in zip((2, 8, 32), PAIRS):
   rows.append((f"      {k:4d}         {gap:.5f}            {jump:.1f}", WARN))
  g.add(self._table(rows, y0=0.80, dy=0.36))
  g.add(self._mid(-0.66, "兩點越靠越近，函數值卻始終差 2",
                  "the two points close in while the values stay two apart", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這個例子有意思的地方是：它連續，而且有界——所以缺的不是有界",
                          "what makes this example interesting is that it is continuous and bounded, so boundedness is not what is missing",
                          ACCENT_A,
                          "缺的是緊緻：定義域開在零那一端，函數就有無窮多次來回的空間",
                          "what is missing is compactness: the domain is open at zero, leaving room for infinitely many swings"))

 def _thm51(self):
  g = VGroup()
  rows = (("∼ ( f ∈ C ᵘ )      ⇒      ∃ ϵ   ∀ δ   ∃ x , y", ACCENT_B),
          ("δ  :=  1 / n              ρ ( x ₙ , y ₙ )  <  1 / n", ACCENT_C),
          ("x ₙ ₍ ᵢ ₎  →  x          y ₙ ₍ ᵢ ₎  →  x", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.56, lab, col, FS_TAG - 1, x=-3.55, w=5.20))
  g.add(self._rect(-3.55, -0.82, 2.25, 0.26, ACCENT_A),
        self._sym(-0.82, "ρ ( f ( x ₙ ₍ ᵢ ₎ ) , f ( y ₙ ₍ ᵢ ₎ ) )   →   0", ACCENT_A,
                  FS_TAG - 1, x=-3.55, w=4.30))
  g.add(self._panel(((0.86, "否定均勻連續，得到 ε 與兩列點",
                      "deny uniformity and two sequences appear", ACCENT_B),
                     (0.20, "緊緻性抽出收斂的子序列",
                      "compactness extracts a convergent subsequence", ACCENT_C),
                     (-0.46, "連續性逼出矛盾：像的距離掉到零",
                      "and continuity forces the images together", WARN))))
  return g.add(self._foot("這正是上一集那套「讓 δ 跑遍一除以 n」的自動證明程序，第二次登場",
                          "this is the automatic procedure of the last episode, letting delta run through one over n, used again",
                          ACCENT_A,
                          "兩列點靠得越來越近，可是像始終差 ε——緊緻性把這件事變成不可能",
                          "the two sequences close in while their images stay apart, and compactness makes that impossible"))

 def _tents(self):
  ox, oy = -5.85, -0.55
  sx, sy = 4.30, 1.40
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.12, 0], color=DIM, stroke_width=1.4))
  for n, col in ((2, ACCENT_B), (6, ACCENT_C), (20, WARN)):
   g.add(self._plot(lambda x, n=n: _tent(n, x), ox, oy, sx, sy, col, sw=2.2, n=1600))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * 1.06, oy + sy, 0], DIM, n=20, sw=1.2))
  g.add(Line([ox, oy - 0.24, 0], [ox + sx, oy - 0.24, 0], color=ACCENT_A, stroke_width=4))
  rows = [("        n          ‖ f ₙ ‖ ∞          f ₙ ( 0.7 )", DIM)]
  for n, sup, at in TENTS:
   rows.append((f"      {n:4d}          {sup:.3f}            {at:.3f}", ACCENT_C))
  g.add(self._table(rows, y0=0.80, dy=0.36))
  g.add(self._mid(-0.66, "定義域緊緻，逐點收斂，可是不均勻",
                  "compact domain, pointwise convergence, still not uniform", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("帳篷越來越窄、越來越靠左，可是高度始終是一——所以一致範數下的距離不掉",
                          "the tents narrow and slide left while the height never changes, so the uniform distance does not fall",
                          ACCENT_A,
                          "定理 5.1 補得起連續，補不起收斂；這一點很容易記錯",
                          "Theorem 5.1 repairs continuity but not convergence, which is easy to misremember"))

 def _positive(self):
  cx, cy = -4.15, -0.15
  g = VGroup(self._circ(cx, cy, 0.78, ACCENT_B, sw=2.6))
  g.add(Line([cx - 1.55, cy + 1.35, 0], [cx + 1.55, cy + 1.35, 0], color=WARN, stroke_width=3))
  g.add(self._arr([cx, cy + 0.78, 0], [cx, cy + 1.35, 0], ACCENT_A, sw=2, tl=0.10),
        self._sym(cy + 1.08, f"{CIRC_LINE:.0f}", ACCENT_A, FS_TAG, x=cx + 0.34, w=0.70))
  g.add(self._panel(((0.86, "青色那個圓是緊緻的",
                      "the teal circle is compact", ACCENT_B),
                     (0.20, "紅色那條線是閉的，兩者不相交",
                      "the red line is closed, and the two are disjoint", WARN),
                     (-0.46, "所以它們的距離一定是正的",
                      "so the distance between them must be positive", ACCENT_A))))
  return g.add(self._foot("上一集看過兩個不相交的閉集距離為零——差別就在那裡兩個都不緊緻",
                          "the last episode showed disjoint closed sets at distance zero, and there neither was compact",
                          ACCENT_A,
                          "書上把這條的證明留給讀者，用的還是那套自動的反證",
                          "the book leaves this proof to the reader, and it is the same automatic contradiction again"))

 def _dense(self):
  ox, oy = -5.85, 0.30
  sx = 4.30
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.6))
  for gpt in GRID:
   px = ox + sx * gpt
   g.add(Dot([px, oy, 0], radius=0.06, color=WARN),
         self._circ(px, oy, sx / DENSE_N, ACCENT_C, sw=1.1, n=40))
  g.add(self._sym(0.86, "B ᵣ [ A ]   =   ∪ { B ᵣ ( a )  :  a ∈ A }", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "每一點都離某個紅點不到 r", "every point is within r of a red one",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "對每個 r 都找得到這樣一個有限集",
                  "and such a finite set exists for every r", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "這就叫全有界",
                  "that is what totally bounded means", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"畫面上是 {DENSE_N - 1} 個點，程式驗過它們在整個區間上是 1／{DENSE_N} 稠密的",
                          f"the {DENSE_N - 1} points on screen were checked here to be one over {DENSE_N} dense in the whole interval",
                          ACCENT_A,
                          "全有界比有界強得多——下一拍那個例子有界卻不全有界",
                          "total boundedness is much stronger than boundedness, as the next beat's example shows"))

 def _peaks(self):
  ox, oy = -5.85, -0.50
  sx, sy = 4.30, 1.30
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.14, 0], color=DIM, stroke_width=1.4))
  for n, col in zip(PEAK_NS, (ACCENT_B, ACCENT_C, WARN, ACCENT_A)):
   g.add(self._plot(lambda x, n=n: _peak(n, x), ox, oy, sx, sy, col, sw=2.2, n=3000))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * 1.06, oy + sy, 0], DIM, n=20, sw=1.1))
  g.add(self._sym(0.86, f"‖ f ₙ  −  f ₘ ‖ ∞    =    {PEAK_GAP:.0f}", WARN,
                  FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "四個尖峰互不重疊，高度都是一",
                  "four peaks that never overlap, each of height one", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "所以任何兩個的一致距離都是一",
                  "so any two of them are one apart in the uniform norm", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "半徑二分之一的球最多只裝得下一個",
                  "no ball of radius one half holds more than one", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("所以那個閉單位球用有限多個球蓋不住——它有界，可是不全有界",
                          "so the closed unit ball cannot be covered by finitely many: it is bounded but not totally bounded",
                          ACCENT_A,
                          "引理 5.1 的一般版本用的是引理 1.5，也就是上一集那個逼近 1 的構造",
                          "the general form of Lemma 5.1 uses Lemma 1.5, the construction that crept toward one two episodes ago"))

 def _riesz(self):
  g = VGroup()
  g.add(self._rect(-4.75, 0.46, 1.35, 0.30, ACCENT_B),
        self._sym(0.46, "dim V   <   ∞", ACCENT_B, FS_TAG + 1, x=-4.75, w=2.50))
  g.add(self._arr([-3.30, 0.60, 0], [-2.65, 0.60, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-2.65, 0.32, 0], [-3.30, 0.32, 0], ACCENT_C, sw=2.5, tl=0.12))
  g.add(self._rect(-1.55, 0.46, 1.15, 0.30, WARN),
        self._sym(0.46, "B ₁ ‾   ∈   𝒦", WARN, FS_TAG + 1, x=-1.55, w=2.10))
  g.add(self._mid(-0.30, "往右：定理 4.4", "rightward: Theorem 4.4",
                  ACCENT_A, FS_TAG - 1, x=-3.35, w=2.40),
        self._mid(-0.80, "往左：引理 5.1 與 5.2", "leftward: Lemmas 5.1 and 5.2",
                  ACCENT_C, FS_TAG - 1, x=-3.35, w=2.40))
  g.add(self._panel(((0.86, "有限維：閉單位球序列緊緻",
                      "finite dimensional: the closed unit ball is compact", ACCENT_B),
                     (0.20, "無窮維：它連全有界都不是",
                      "infinite dimensional: it is not even totally bounded", WARN),
                     (-0.46, "所以這條等價就是兩者的分界線",
                      "so this equivalence is the line between the two", ACCENT_A))))
  return g.add(self._foot("往右那個箭頭是定理 4.4（有界閉集緊緻），往左是這一節的兩條引理",
                          "the rightward arrow is Theorem 4.4, that bounded closed sets are compact; the leftward one is this section's two lemmas",
                          ACCENT_A,
                          "一句話：緊緻的單位球是有限維獨有的奢侈品",
                          "in one line: a compact unit ball is a luxury only finite dimensions can afford"))

 def _lebesgue(self):
  ox, oy = -5.85, 0.35
  sx = 4.30
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.0))
  for (a, b), col, dy in zip(COVER, (ACCENT_B, ACCENT_C), (0.34, -0.34)):
   g.add(Line([ox + sx * a, oy + dy, 0], [ox + sx * b, oy + dy, 0], color=col, stroke_width=5))
  g.add(Line([ox + sx * (0.5 - GOOD_R), oy - 0.86, 0], [ox + sx * (0.5 + GOOD_R), oy - 0.86, 0],
             color=WARN, stroke_width=5),
        Dot([ox + sx * 0.5, oy - 0.86, 0], radius=0.055, color=ACCENT_A))
  g.add(self._sym(0.86, "∀ p ∈ A      ∃ j      B ᵣ ( p )   ⊂   E ⱼ", ACCENT_A,
                  FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, f"r = {GOOD_R:.2f} 對每一點都成立",
                  f"r equal to {GOOD_R:.2f} works at every point", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, f"r = {BAD_R:.2f} 在中間那一點就失敗",
                  f"r equal to {BAD_R:.2f} already fails in the middle", DIM,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "有了這個 r，有限子覆蓋就跟著出來",
                  "with that r in hand the finite subcover follows", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("兩條彩色的線段是一個開覆蓋，紅色那一段是中間那點的 r 球，它整個落在上面那一段裡",
                          "the two coloured segments are an open covering, and the red one is the ball about the midpoint, sitting inside the upper set",
                          ACCENT_A,
                          "定理 5.3 與 5.4 於是說：在度量空間上，序列緊緻與有限子覆蓋是同一件事",
                          "Theorems 5.3 and 5.4 then say that on a metric space, sequential compactness and finite subcovers are one thing"))

 def stage(self):
  a, b, c = self._quantifiers(), self._convergence(), self._powers()
  d, e, f = self._wiggly(), self._thm51(), self._tents()
  h, i, j = self._positive(), self._dense(), self._peaks()
  k, l = self._riesz(), self._lebesgue()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE59ZH, AdvCalcE59EN = make(AdvCalcE59Base, "59", prefix="AdvCalcE")
