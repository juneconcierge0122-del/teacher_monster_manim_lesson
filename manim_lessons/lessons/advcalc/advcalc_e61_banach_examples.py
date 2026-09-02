"""advcalc E61 -- chapter 4, section 7 second half (book pp. 218-221): the list of
Banach spaces, the epsilon-over-three argument, and infinite series.

E60 stopped at Theorem 7.4 and its second corollary.  This episode takes the
rest of the section: the bounded functions and the bounded linear maps are
Banach spaces (7.5, 7.6); a closed subset of a complete space is complete and a
complete subset of anything is closed, which is the same as saying a complete
space is absolutely closed (7.7); the continuous ones form a closed subspace by
the "up, over, and down" argument (7.8), so a uniform limit of continuous
functions is continuous; sequential compactness gives completeness (7.9), total
boundedness gives Cauchy subsequences (7.4), and together compactness is exactly
total boundedness plus completeness (7.10).  It ends with series: absolute
convergence implies convergence in a Banach space (7.11), and the Weierstrass
comparison test.

Section 7's content stops at page 221; 221 to 223 are exercises 7.1 to 7.21, and
by section 8 of the playbook they are not worked here.  Figure 4.3 in the book
sketches the epsilon-over-three argument; beat 4 draws that idea from scratch,
with its own staircase, numbers, and labels.

Seven beats carry computations: the uniform-norm gaps of beat 0 and the slopes
of beat 1 are measured off the curves actually drawn, the escaping Cauchy
sequence of beat 2 is checked to leave the half-open interval, the three steps
of beat 4 are each checked to sit under a third of epsilon and to sum under it,
the pointwise limit of beat 5 is checked to be discontinuous while each member
is continuous, the nested radii of beat 7 are checked to force the Cauchy
bound, and the two series of beats 9 and 10 are summed.
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


# ── beat 0: a Cauchy sequence in the uniform norm ──────────────────────
def _limit(x):
 return 0.30 * math.sin(2.4 * x) + 0.10


def _wig(x):
 return math.sin(7.0 * x)


UNIF_NS = (2, 4, 8)
UNIF = []
for _n in UNIF_NS:
 _g = max(abs(_wig(k / 4000.0) / _n) for k in range(4001))
 UNIF.append((_n, _g))
for _n, _g in UNIF:
 # the wiggle peaks at one inside the interval, so the sup is one over n up to
 # how finely the peak is sampled
 assert abs(_g - 1.0 / _n) < 1e-5, "the uniform gap is one over n"
assert UNIF[-1][1] < 0.13 and UNIF[0][1] > 0.45, "and it really does shrink on screen"


# ── beat 1: linear is what has to survive the limit ────────────────────
SLOPES = (1.60, 1.35, 1.22, 1.15)
SLOPE_LIM = 1.10
for _a, _b in zip(SLOPES, SLOPES[1:]):
 assert _a > _b > SLOPE_LIM, "the slopes close in on the limit from above"
assert SLOPES[-1] - SLOPE_LIM < 0.06, "and get close enough to read as converging"


# ── beat 2: the sequence that escapes the half-open interval ───────────
ESC = [(n, 1.0 / n) for n in (2, 4, 10, 40)]
assert all(0.0 < v <= 1.0 for _, v in ESC), "every term is inside the interval"
assert min(v for _, v in ESC) < 0.03, "while the terms march down to the missing end"
assert max(abs(a - b) for _, a in ESC[2:] for _, b in ESC[2:]) < 0.08, "so it is Cauchy"


# ── beat 4: up, over, and down ─────────────────────────────────────────
EPS4 = 0.90
STEP = EPS4 / 3.0
UP_OVER_DOWN = (0.27, 0.24, 0.26)
for _s in UP_OVER_DOWN:
 assert _s < STEP, "each of the three steps has to sit under a third of epsilon"
assert sum(UP_OVER_DOWN) < EPS4, "so the three of them together stay under epsilon"


# ── beat 5: continuous members, a discontinuous pointwise limit ────────
def _arct(n, x):
 return math.atan(n * x) * 2.0 / math.pi


ARC_NS = (2, 8, 40)
for _n in ARC_NS:
 assert abs(_arct(_n, 0.0)) < 1e-12, "every member sends zero to zero"
ARC_AT = [(n, _arct(n, 0.25)) for n in ARC_NS]
assert ARC_AT[0][1] < 0.35 and ARC_AT[-1][1] > 0.93, \
    "at a fixed positive point the values climb toward one"
assert abs(_arct(4000, 0.25) - 1.0) < 1e-3, \
    "so the pointwise limit is one on the right, zero at the origin: a jump"


# ── beat 7: the nested balls, and the bound they force ─────────────────
NEST_RS = (1.0, 1.0 / 2, 1.0 / 3, 1.0 / 4)
for _k, _r in enumerate(NEST_RS, start=1):
 assert abs(_r - 1.0 / _k) < 1e-12, "the radii run through one over k"
# two points inside the same ball of radius 1/n are within 2/n of each other
NEST_BOUND = 2.0 * NEST_RS[-1]
assert NEST_BOUND == 0.5, "which is the bound the diagonal subsequence inherits"


# ── beats 9 and 10: two series that are actually summed ────────────────
GEO = [2.0 ** -i for i in range(1, 9)]
GEO_PARTIAL = [sum(GEO[:k]) for k in range(1, len(GEO) + 1)]
assert abs(GEO_PARTIAL[-1] - 1.0) < 0.005, "the partial sums climb to one"
assert all(b > a for a, b in zip(GEO_PARTIAL, GEO_PARTIAL[1:])), "and climb monotonically"

WEIER_NS = (1, 2, 3, 4, 5, 6)
WEIER_M = [1.0 / n ** 2 for n in WEIER_NS]
WEIER_TAIL = sum(1.0 / n ** 2 for n in range(len(WEIER_NS) + 1, 4000))
assert abs(sum(WEIER_M) + WEIER_TAIL - math.pi ** 2 / 6) < 1e-3, \
    "the constants sum to pi squared over six"
assert WEIER_TAIL < 0.16, "so the tail past the terms drawn is already small"


def _weier(x, upto):
 return sum(math.sin(n * x) / n ** 2 for n in WEIER_NS[:upto])


WEIER_GAP = max(abs(_weier(k / 2000.0 * 6.0, 6) - _weier(k / 2000.0 * 6.0, 4))
                for k in range(2001))
WEIER_BOUND = WEIER_M[4] + WEIER_M[5]
assert WEIER_GAP <= WEIER_BOUND + 1e-9, \
    "the gap between two partial sums is bounded by the constants, not by x"
assert WEIER_GAP < 0.07, "and it is small enough that the curves overlap on screen"



class AdvCalcE61Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 61

 MODE_LABEL = {
  0: {"zh": "定理 7.5：有界函數的空間", "en": "Theorem 7.5: the bounded functions"},
  1: {"zh": "定理 7.6：極限還得是線性的", "en": "Theorem 7.6: the limit must stay linear"},
  2: {"zh": "定理 7.7：閉與完備互相換", "en": "Theorem 7.7: closed and complete trade places"},
  3: {"zh": "完備化，與「絕對閉」", "en": "completion, and absolutely closed"},
  4: {"zh": "定理 7.8：上去、過去、下來", "en": "Theorem 7.8: up, over, and down"},
  5: {"zh": "均勻收斂保得住連續", "en": "uniform convergence keeps continuity"},
  6: {"zh": "定理 7.9：緊緻推得出完備", "en": "Theorem 7.9: compact gives complete"},
  7: {"zh": "引理 7.4：一層一層套下去", "en": "Lemma 7.4: the nested construction"},
  8: {"zh": "定理 7.10：緊緻拆成兩件事", "en": "Theorem 7.10: compactness splits in two"},
  9: {"zh": "級數與絕對收斂", "en": "series, and absolute convergence"},
  10: {"zh": "Weierstrass 判別法", "en": "the Weierstrass comparison test"},
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

 def _circ(self, cx, cy, r, col, sw=2.0, n=48):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plot(self, f, ox, oy, sx, sy, col, sw=2.4, n=220, x0=0.0, x1=1.0):
  return self._curve([[ox + sx * k / n, oy + sy * f(x0 + (x1 - x0) * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _uniform_norm(self):
  ox, oy = -5.85, -0.10
  sx, sy = 4.30, 0.95
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  for (n, gap), col in zip(UNIF, (ACCENT_C, ACCENT_B, WARN)):
   g.add(self._plot(lambda x, n=n: _limit(x) + _wig(x) / n, ox, oy, sx, sy, col, sw=1.7))
  # the tube is the last gap, drawn dashed so it cannot be mistaken for a member
  for s in (UNIF[-1][1], -UNIF[-1][1]):
   g.add(self._curve([[ox + sx * k / 60, oy + sy * (_limit(k / 60.0) + s), 0]
                      for k in range(61)], DIM, sw=1.0))
  g.add(self._plot(_limit, ox, oy, sx, sy, ACCENT_A, sw=3.0))
  rows = [("       n          ‖ f ₙ  −  g ‖ ∞", DIM)]
  for n, gap in UNIF:
   rows.append((f"     {n:4d}                {gap:.3f}", ACCENT_C))
  g.add(self._table(rows, y0=0.86, dy=0.32))
  g.add(self._mid(-0.92, "橘色那條粗的是極限，灰色細的兩條是最後一個 n 的管子",
                  "the thick curve is the limit and the thin grey pair is the last tube", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("一致範數量的是「處處都靠近」，所以逐點的極限一得到，有界與一致收斂就跟著出來",
                          "the uniform norm measures closeness everywhere at once, so once the pointwise limit exists, boundedness and uniform convergence follow",
                          ACCENT_A,
                          "A 可以是任何一個集合——這裡完全沒有用到定義域的結構",
                          "A may be any set at all: nothing about the structure of the domain is used here"))

 def _linear_limit(self):
  ox, oy = -5.60, -0.55
  sx, sy = 3.90, 1.55
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.10, 0], color=DIM, stroke_width=1.4))
  for a, col in zip(SLOPES, (DIM, ACCENT_C, ACCENT_B, WARN)):
   g.add(Line([ox, oy, 0], [ox + sx, oy + sy * a / 1.75, 0], color=col, stroke_width=1.8))
  g.add(Line([ox, oy, 0], [ox + sx, oy + sy * SLOPE_LIM / 1.75, 0],
             color=ACCENT_A, stroke_width=3.0))
  rows = [("       n          ‖ T ₙ ‖", DIM)]
  for k, a in enumerate(SLOPES, start=1):
   rows.append((f"     {k:4d}              {a:.2f}", ACCENT_C))
  rows.append((f"      ∞               {SLOPE_LIM:.2f}", ACCENT_A))
  g.add(self._table(rows, y0=0.86, dy=0.30))
  g.add(self._mid(-0.94, "每一條都過原點而且是直的——極限也必須是",
                  "each one is straight and through the origin, and the limit must be too",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 7.5 的證明照抄一遍就好，只多一件事：要檢查極限那個映射還是線性的",
                          "the proof of Theorem 7.5 is copied over, with one thing added: the limit map has to be checked to be linear",
                          ACCENT_A,
                          "書上把這一條留成習題；第 8 節的 Banach 代數整節都建在它上面",
                          "the book leaves this one as an exercise, and section 8 on Banach algebras is built entirely on it"))

 def _closed_complete(self):
  ox, oy = -5.70, 0.36
  sx = 4.20
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.2))
  g.add(Dot([ox + sx, oy, 0], radius=0.07, color=ACCENT_B),
        self._circ(ox, oy, 0.09, WARN, sw=2.2))
  for (n, v), col in zip(ESC, (DIM, DIM, ACCENT_C, WARN)):
   g.add(Dot([ox + sx * v, oy, 0], radius=0.055, color=col))
  g.add(self._sym(oy + 0.40, "(  0  ,  1  ]", ACCENT_B, FS_TAG, x=ox + sx * 0.5, w=2.40))
  g.add(self._mid(oy - 0.42, "1／n 是 Cauchy 的，可是極限 0 不在裡面",
                  "the terms 1/n are Cauchy, and the limit zero is not in the set", WARN,
                  FS_TAG - 1, x=ox + sx * 0.5, w=4.60))
  g.add(self._panel(((0.86, "完備空間裡的閉子集，是完備的",
                      "a closed subset of a complete space is complete", ACCENT_B),
                     (0.20, "任何度量空間裡的完備子集，是閉的",
                      "a complete subset of any metric space is closed", ACCENT_C),
                     (-0.46, "空心那一端沒補上，兩件事就一起壞掉",
                      "leave the hollow end out and both properties fail together", WARN))))
  return g.add(self._foot("第二半的說法是：完備的空間是「絕對閉」的——放進多大的空間裡，它都還是閉集",
                          "the second half says a complete space is absolutely closed: it stays closed inside however large a space you put it in",
                          ACCENT_A,
                          "半開區間兩件事都不成立，補上 0 之後兩件事同時成立——這不是巧合",
                          "the half-open interval fails both, and adding the zero repairs both at once, which is not a coincidence"))

 def _completion(self):
  g = VGroup()
  g.add(self._rect(-3.65, 0.16, 2.30, 0.72, ACCENT_B, sw=2.0),
        self._mid(1.06, "ℝ：完備", "the reals: complete", ACCENT_B,
                  FS_TAG - 1, x=-3.65, w=2.60))
  g.add(self._curve([[-3.65 + 1.55 * math.cos(2 * math.pi * k / 60),
                      0.16 + 0.46 * math.sin(2 * math.pi * k / 60), 0]
                     for k in range(61)], ACCENT_C, sw=1.6))
  g.add(self._mid(0.16, "ℚ", "the rationals", ACCENT_C, FS_TAG, x=-3.65, w=1.60))
  g.add(self._panel(((0.86, "ℚ 的閉包是 ℝ，跟 ℚ 自己不一樣",
                      "the closure of the rationals is the reals, not the rationals", ACCENT_C),
                     (0.20, "所以 ℚ 在 ℝ 裡不是閉的",
                      "so the rationals are not closed inside the reals", WARN),
                     (-0.46, "不完備的空間，永遠找得到一個地方讓它不閉",
                      "an incomplete space can always be put somewhere it fails to be closed",
                      ACCENT_A))))
  return g.add(self._foot("完備化：任何度量空間都造得出一個包含它的完備空間，習題 7.21 到 7.23 給了做法",
                          "completion: any metric space can be embedded in a complete one, and exercises 7.21 to 7.23 give the construction",
                          ACCENT_A,
                          "所以「絕對閉」與「完備」是同一件事，而 ℚ 配上 ℝ 就是這件事的樣板",
                          "so absolutely closed and complete are the same property, and the rationals inside the reals are the picture to keep"))

 def _up_over_down(self):
  ox, oy = -5.85, -0.62
  sx, sy = 4.10, 1.55
  g = VGroup()
  gg = lambda x: 0.30 * math.sin(2.6 * x) + 0.40
  fn = lambda x: gg(x) + 0.30
  g.add(self._plot(gg, ox, oy, sx, sy, ACCENT_A, sw=2.6),
        self._plot(fn, ox, oy, sx, sy, ACCENT_B, sw=2.2))
  ax, xx = 0.22, 0.70
  pax, pxx = ox + sx * ax, ox + sx * xx
  ga, gx = oy + sy * gg(ax), oy + sy * gg(xx)
  fa, fx = oy + sy * fn(ax), oy + sy * fn(xx)
  g.add(self._arr([pxx, gx, 0], [pxx, fx, 0], WARN, sw=2.0, tl=0.10),
        self._arr([pxx, fx, 0], [pax, fa, 0], ACCENT_C, sw=2.0, tl=0.10),
        self._arr([pax, fa, 0], [pax, ga, 0], WARN, sw=2.0, tl=0.10))
  for px, lab in ((pax, "a"), (pxx, "x")):
   g.add(self._dash([px, oy, 0], [px, oy + sy * 0.42, 0], DIM, n=6, sw=1.0),
         self._sym(oy - 0.22, lab, DIM, FS_TAG - 1, x=px, w=0.60))
  g.add(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4))
  rows = [("                      <   ϵ / 3", DIM)]
  for lab, s, col in zip(("↑", "→", "↓"), UP_OVER_DOWN, (WARN, ACCENT_C, WARN)):
   rows.append((f"      {lab}            {s:.2f}", col))
  rows.append((f"      Σ            {sum(UP_OVER_DOWN):.2f}   <   {EPS4:.2f}", WARN))
  g.add(self._table(rows, y0=0.84, dy=0.36))
  return g.add(self._foot("上去：g 與 f ₙ 差不到 ε 除以三。過去：f ₙ 自己連續。下來：再回到 g",
                          "up: g and the n-th function differ by under a third of epsilon; over: that function is itself continuous; down: back to g again",
                          ACCENT_A,
                          "三段各壓在 ε 除以三以內，加起來剛好是 ε——書上把這一招畫成一張圖，這裡自己重畫",
                          "three steps each under a third of epsilon add to epsilon; the book sketches this, and the drawing here is our own"))

 def _keeps_continuity(self):
  ox, oy = -5.85, -0.06
  sx, sy = 4.20, 0.80
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             self._dash([ox + sx * 0.5, oy - sy * 1.10, 0], [ox + sx * 0.5, oy + sy * 1.10, 0],
                        DIM, n=12, sw=1.0))
  for n, col in zip(ARC_NS, (ACCENT_B, ACCENT_C, WARN)):
   g.add(self._plot(lambda x, n=n: _arct(n, x), ox, oy, sx, sy, col,
                    sw=1.9, n=400, x0=-1.0, x1=1.0))
  for y0, y1, x0, x1 in ((1.0, 1.0, 0.5, 1.06), (-1.0, -1.0, -0.06, 0.5)):
   g.add(self._dash([ox + sx * x1 if x1 > 0.5 else ox + sx * x0, oy + sy * y0, 0],
                    [ox + sx * x0 if x1 > 0.5 else ox + sx * x1, oy + sy * y1, 0],
                    ACCENT_A, n=14, sw=1.4))
  g.add(Dot([ox + sx * 0.5, oy, 0], radius=0.06, color=ACCENT_A))
  rows = [("       n          f ₙ ( 0.25 )", DIM)]
  for n, v in ARC_AT:
   rows.append((f"     {n:4d}              {v:.3f}", ACCENT_C))
  g.add(self._table(rows, y0=0.80, dy=0.36))
  g.add(self._mid(-0.70, "逐點的極限是一個跳躍——每一個成員卻都連續",
                  "the pointwise limit has a jump, though every member is continuous", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這一列不是均勻收斂的，所以定理 7.8 管不到它——極限也就沒有義務連續",
                          "this sequence does not converge uniformly, so Theorem 7.8 says nothing about it, and the limit is under no obligation to be continuous",
                          ACCENT_A,
                          "反過來說，均勻收斂的連續函數列，極限一定連續；書上還提醒證明其實給得更多",
                          "the other way round, a uniform limit of continuous functions is continuous, and the book notes the proof gave more than that"))

 def _compact_complete(self):
  cx, cy = -3.85, 0.18
  g = VGroup(self._curve([[cx + 1.55 * math.cos(2 * math.pi * k / 80),
                           cy + 0.78 * math.sin(2 * math.pi * k / 80), 0]
                          for k in range(81)], ACCENT_B, sw=2.2))
  pts = []
  for i in range(12):
   r = 1.20 * (0.90 ** i)
   th = 0.9 * i
   pts.append([cx + r * math.cos(th) * 0.95, cy + r * math.sin(th) * 0.48, 0])
  g.add(self._curve(pts, DIM, sw=1.2))
  for i, p in enumerate(pts):
   pick = i in (2, 5, 8, 11)
   g.add(Dot(p, radius=0.07 if pick else 0.045, color=WARN if pick else DIM))
  g.add(Dot([cx, cy, 0], radius=0.075, color=ACCENT_A))
  g.add(self._panel(((0.86, "Cauchy 序列在序列緊緻的集合裡",
                      "a Cauchy sequence inside a sequentially compact set", ACCENT_B),
                     (0.20, "抽得出一支收斂的子序列",
                      "has a convergent subsequence to extract", WARN),
                     (-0.46, "引理 7.2 一引用，整個序列就收斂",
                      "and Lemma 7.2 then makes the whole sequence converge", ACCENT_A))))
  return g.add(self._foot("證明只有兩行，因為要用的兩件事上一集與這一集都已經備好了",
                          "the proof is two lines, because both of the things it needs were put in place already",
                          ACCENT_A,
                          "反過來不成立：實數線完備，可是一點也不緊緻——它連有界都不是",
                          "the converse fails: the line is complete and not compact at all, not even bounded"))

 def _nested(self):
  g = VGroup()
  cx, cy = -4.15, 0.15
  for k, (r, col) in enumerate(zip(NEST_RS, (DIM, ACCENT_B, ACCENT_C, WARN))):
   g.add(self._circ(cx, cy, 1.00 * r, col, sw=1.8))
   g.add(self._sym(0.88 - k * 0.36, f"r  =  1 / {k + 1}", col, FS_TAG - 2,
                   x=-1.35, w=1.90))
  for i in range(6):
   g.add(Dot([cx + 0.15 * math.cos(2.1 * i), cy + 0.15 * math.sin(2.1 * i), 0],
             radius=0.038, color=DIM))
  g.add(self._panel(((0.86, "每一個球裡都還有無窮多項",
                      "each ball still holds infinitely many terms", ACCENT_B),
                     (0.20, "半徑一路換成 1、二分之一、三分之一…",
                      "the radii run through one, a half, a third, and on", ACCENT_C),
                     (-0.46, f"同一個球裡兩點相距不到 {NEST_BOUND:.1f}，沿對角線挑就是 Cauchy",
                      f"two points in one ball are within {NEST_BOUND:.1f}, so the diagonal choice is Cauchy",
                      WARN))))
  return g.add(self._foot("全有界給的是「有限多個球」，所以一定有一個球裝了無窮多項——鴿籠原理",
                          "total boundedness supplies finitely many balls, so one of them must hold infinitely many terms: the pigeonhole",
                          ACCENT_A,
                          "一層一層套下去之後沿著對角線挑，挑出來的那一支就是 Cauchy 的",
                          "nest that construction and then pick along the diagonal, and the subsequence that comes out is Cauchy"))

 def _splits(self):
  g = VGroup()
  g.add(self._rect(-4.60, 0.52, 1.00, 0.30, ACCENT_B),
        self._sym(0.52, "𝒦", ACCENT_B, FS_TAG + 2, x=-4.60, w=1.60))
  g.add(self._rect(-1.55, 0.90, 1.30, 0.28, ACCENT_C),
        self._mid(0.90, "全有界", "totally bounded", ACCENT_C, FS_TAG - 1, x=-1.55, w=2.40))
  g.add(self._rect(-1.55, 0.14, 1.30, 0.28, WARN),
        self._mid(0.14, "完備", "complete", WARN, FS_TAG - 1, x=-1.55, w=2.40))
  g.add(self._arr([-3.54, 0.62, 0], [-2.90, 0.84, 0], ACCENT_A, sw=2.2, tl=0.10),
        self._arr([-2.90, 0.84, 0], [-3.54, 0.62, 0], ACCENT_A, sw=2.2, tl=0.10),
        self._arr([-3.54, 0.42, 0], [-2.90, 0.20, 0], ACCENT_A, sw=2.2, tl=0.10),
        self._arr([-2.90, 0.20, 0], [-3.54, 0.42, 0], ACCENT_A, sw=2.2, tl=0.10))
  g.add(self._mid(-0.42, "往右上：第 5 節　往右下：定理 7.9",
                  "up to the right: section 5.  down to the right: Theorem 7.9",
                  ACCENT_A, FS_TAG - 1, x=-3.10, w=5.60),
        self._mid(-0.90, "往左：引理 7.4 加上完備性",
                  "back to the left: Lemma 7.4 together with completeness",
                  ACCENT_C, FS_TAG - 1, x=-3.10, w=5.60))
  g.add(self._panel(((0.86, "序列緊緻，等價於全有界而且完備",
                      "sequentially compact is the same as totally bounded and complete",
                      ACCENT_B),
                     (0.20, "兩個條件互相獨立，缺一不可",
                      "the two conditions are independent, and neither can be dropped", WARN),
                     (-0.46, "開區間全有界卻不完備；實數線完備卻不全有界",
                      "the open interval is totally bounded and not complete; the line is complete and not totally bounded",
                      ACCENT_A))))
  return g.add(self._foot("緊緻這件事到這裡被拆成兩個獨立的條件，第 5 節與第 7 節各出一半",
                          "compactness is finally split into two independent conditions, one supplied by section 5 and one by section 7",
                          ACCENT_A,
                          "第 5 節那條 Lebesgue 數的結論則是把序列緊緻接到有限子覆蓋上",
                          "and section 5's Lebesgue number was what joined sequential compactness to finite subcovers"))

 def _series(self):
  ox, oy = -5.85, -0.66
  sx, sy = 4.10, 1.60
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.10, 0], color=DIM, stroke_width=1.4))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * 1.08, oy + sy, 0], ACCENT_A, n=20, sw=1.2))
  step = sx / (len(GEO_PARTIAL) + 0.5)
  prev = oy
  for k, s in enumerate(GEO_PARTIAL):
   x0, x1 = ox + step * (k + 0.25), ox + step * (k + 1.25)
   y = oy + sy * s
   g.add(Line([x0, prev, 0], [x0, y, 0], color=ACCENT_C, stroke_width=1.6),
         Line([x0, y, 0], [x1, y, 0], color=ACCENT_B, stroke_width=2.0))
   prev = y
  g.add(self._sym(oy + sy + 0.26, "Σ  =  1", ACCENT_A, FS_TAG, x=ox + sx * 0.80, w=1.80))
  g.add(self._table((("      σ ₙ   =   Σ ₁ ⁿ  2 ⁻ ⁱ", DIM),
                     (f"      σ ₃   =   {GEO_PARTIAL[2]:.3f}", ACCENT_C),
                     (f"      σ ₆   =   {GEO_PARTIAL[5]:.3f}", ACCENT_B),
                     (f"      σ ₈   =   {GEO_PARTIAL[7]:.3f}", WARN)), y0=0.84, dy=0.38))
  g.add(self._mid(-0.86, "級數收斂＝部分和的序列收斂",
                  "a series converges when its sequence of partial sums does", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("絕對收斂是說「那些範數的級數」在實數上收斂——那是一個關於實數的條件",
                          "absolute convergence asks that the series of norms converge in the reals, which is a condition about real numbers",
                          ACCENT_A,
                          "定理 7.11：在 Banach 空間裡它就夠了，因為部分和自己是 Cauchy 的",
                          "Theorem 7.11: in a Banach space that is enough, because the partial sums are then Cauchy themselves"))

 def _weierstrass(self):
  ox, oy = -5.85, 0.00
  sx, sy = 4.10, 1.00
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  for upto, col in ((2, ACCENT_B), (4, ACCENT_C), (6, WARN)):
   g.add(self._plot(lambda x, upto=upto: _weier(x, upto), ox, oy, sx, sy, col,
                    sw=1.9, n=300, x0=0.0, x1=6.0))
  rows = [("       n          M ₙ  =  1 / n ²", DIM)]
  for n, m in list(zip(WEIER_NS, WEIER_M))[:2]:
   rows.append((f"     {n:4d}                {m:.4f}", ACCENT_C))
  rows.append((f"      Σ                {math.pi ** 2 / 6:.4f}", ACCENT_A))
  rows.append((f"  ‖ σ ₆ − σ ₄ ‖ ∞   =   {WEIER_GAP:.4f}", ACCENT_B))
  rows.append((f"  M ₅ + M ₆         =   {WEIER_BOUND:.4f}", WARN))
  g.add(self._table(rows, y0=0.86, dy=0.30))
  g.add(self._mid(-0.94, "常數蓋得住，級數就均勻收斂",
                  "the constants dominate, so the series converges uniformly", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("三條曲線幾乎疊在一起——均勻收斂看起來就是這樣；它們的差被那兩個常數蓋住，跟 x 無關",
                          "the three curves nearly coincide, which is what uniform convergence looks like, and their gap is held down by the two constants, not by x",
                          ACCENT_A,
                          "書上還留了一條反過來的習題：每個絕對收斂的級數都收斂，就刻畫了完備性",
                          "the book also leaves the converse as an exercise: every absolutely convergent series converging is itself a characterisation of completeness"))

 def stage(self):
  a, b, c = self._uniform_norm(), self._linear_limit(), self._closed_complete()
  d, e, f = self._completion(), self._up_over_down(), self._keeps_continuity()
  h, i, j = self._compact_complete(), self._nested(), self._splits()
  k, l = self._series(), self._weierstrass()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE61ZH, AdvCalcE61EN = make(AdvCalcE61Base, "61", prefix="AdvCalcE")
