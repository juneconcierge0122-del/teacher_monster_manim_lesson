"""advcalc E60 -- chapter 4, sections 6 and 7 (book pp. 215-218): equicontinuity,
and the first half of completeness.  Section 6 is a page and a half, so it is
merged into this episode the way section 2 was merged into E57.

Equicontinuity is the third use of the same quantifier move.  Uniform continuity
was one delta for many *points*; equicontinuity is one delta for many
*functions*, and uniform equicontinuity is one delta for both at once.  Theorem
6.1 then says total boundedness passes from the domain and the range to the
family itself, by a proof built out of three finite sets.  Section 7 turns to
Cauchy sequences and completeness, and stops at Theorem 7.4 and its second
corollary: every finite-dimensional space, under any norm, is a Banach space.

Section 6 has no exercises at all -- page 216 goes straight on into section 7 --
and section 7's exercises (7.1 to 7.21) sit on pages 221 to 223, past the end of
this episode.

Seven beats carry computations.  The shared delta of beat 0 is checked against
every member of the drawn family; the wedge of beat 1 is drawn at the family's
actual derivative bound, so that its arms reach the corners of the epsilon box
exactly because delta is epsilon over m; the lattice of sampled functions is
counted; the quarters of beat 4 are checked to close at epsilon; the index N of
beat 5 is found by search rather than asserted; the sequence 1/x blows apart is
checked to be Cauchy before the map and not after; and the rationals of beat 8
are built as exact fractions, so "every term is rational and the limit is not"
is a property of the numbers on screen and not a caption.
"""
import math
import pathlib, sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20


# ── beat 0: one delta, four functions ──────────────────────────────────
# f_k(x) = c_k + sin(k x) / k, so |f_k'| = |cos(k x)| <= 1 for every k
FAM_KS = (1, 2, 3, 5)
FAM_C = (0.18, 0.45, 0.72, 0.99)
P0, EPS0, DELTA0 = 0.55, 0.12, 0.12


def _fam(k, x):
 return math.sin(k * x) / k


FAM_SWING = []
for _k in FAM_KS:
 _s = max(abs(_fam(_k, P0 + t * DELTA0 / 200.0) - _fam(_k, P0))
          for t in range(-200, 201))
 FAM_SWING.append((_k, _s))
for _k, _s in FAM_SWING:
 assert _s < EPS0, "the one shared delta has to work for every member"
assert max(_s for _, _s in FAM_SWING) > 0.5 * EPS0, \
    "and it should be tight enough that the boxes are worth drawing"


# ── beat 1: the mean value theorem hands over delta = epsilon / m ──────
EPS1, M1 = 0.30, 3.0
DELTA1 = EPS1 / M1
SLOPES = (1, 3, 10)
MVT = [(m, EPS1 / m) for m in SLOPES]
for _m, _d in MVT:
 # a function with |f'| <= m moves by at most m * delta over a step of delta
 assert abs(_m * _d - EPS1) < 1e-12, "so the bound comes out at exactly epsilon"

# the three curves actually drawn: g_a(x) = c + a sin(3x) / 3, so |g'| = |a cos 3x|
WEDGE = ((3.0, 0.30), (2.0, 0.00), (1.0, -0.30))
XSTAR = 0.35
for _a, _c in WEDGE:
 _d = max(abs(_a * math.cos(3.0 * (-1.0 + 2.0 * k / 400.0))) for k in range(401))
 assert _d <= M1 + 1e-9, "every drawn curve has to respect the bound the wedge shows"
assert abs(M1 * DELTA1 - EPS1) < 1e-12, \
    "so the arms of the wedge land exactly on the corners of the box"


# ── beat 3: a function from D to E is one choice per column ────────────
ND, NE = 4, 3
NG = NE ** ND
assert NG == 81, "the lattice on screen has this many paths through it"
PATHS = ((0, 2, 1, 2), (2, 1, 1, 0))
for _p in PATHS:
 assert len(_p) == ND and all(0 <= _i < NE for _i in _p), "one dot per column"
assert PATHS[0] != PATHS[1], "and the two drawn paths must differ"


# ── beat 4: the quarters that make the diameter come out at epsilon ────
EPS4 = 1.0
CHAIN = (EPS4 / 4, EPS4 / 2, EPS4 / 4)
assert abs(sum(CHAIN) - EPS4) < 1e-12, "the three pieces have to close exactly"


# ── beat 5: the index N is searched for, not asserted ──────────────────
def _seq(n):
 return (-1.0) ** n / n


EPS5 = 0.30
CAU_N = next(N for N in range(1, 400)
             if all(abs(_seq(m) - _seq(n)) < EPS5
                    for m in range(N + 1, N + 60) for n in range(N + 1, N + 60)))
# 1/7 + 1/8 = 0.268 clears the threshold while 1/6 + 1/7 = 0.310 does not
assert CAU_N == 6, f"the search should land on 6, not {CAU_N}"
assert abs(_seq(CAU_N) - _seq(CAU_N + 1)) >= EPS5, \
    "and at the index itself the terms are still a full epsilon apart"


# ── beat 7: 1/x carries a Cauchy sequence to one that is not ───────────
SRC = [(n, 1.0 / n) for n in (20, 40, 80)]
GAP_IN = max(abs(a - b) for _, a in SRC for _, b in SRC)
GAP_OUT = max(abs(m - n) for m, _ in SRC for n, _ in SRC)
assert GAP_IN < 0.05, "the domain points are already huddled together"
assert GAP_OUT >= 50, "while their images have run apart"


# ── beat 8: a Cauchy sequence of rationals whose limit is not one ──────
# (1 + 1/n)^n is an exact rational for every n, and it climbs to e, which is
# not.  Built with Fraction so that "every term is rational" is a property of
# the numbers on screen rather than a claim in the caption.
E_NS = (1, 2, 3, 5, 8, 13, 21, 34)
E_FRACS = [Fraction(n + 1, n) ** n for n in E_NS]
assert all(f.denominator > 1 for f in E_FRACS[1:]), "every term past the first is a true fraction"
E_VALS = [float(f) for f in E_FRACS]
assert all(b > a for a, b in zip(E_VALS, E_VALS[1:])), "the sequence climbs"
assert all(v < math.e for v in E_VALS), "and stays under the limit"
assert math.e - E_VALS[-1] < 0.05, "getting close enough for the gap to read as small"
assert max(abs(a - b) for a in E_VALS[-3:] for b in E_VALS[-3:]) < 0.10, \
    "so the tail is huddled: this really is Cauchy in the rationals"


class AdvCalcE60Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 60

 MODE_LABEL = {
  0: {"zh": "等度連續：一個 δ 對整族", "en": "equicontinuity: one delta for the family"},
  1: {"zh": "均勻等度連續與均值定理", "en": "uniform equicontinuity, via the mean value theorem"},
  2: {"zh": "定理 6.1：全有界傳得下去", "en": "Theorem 6.1: total boundedness passes on"},
  3: {"zh": "證明的骨架：三個有限集", "en": "the proof rests on three finite sets"},
  4: {"zh": "四分之一 ε 拼成直徑 ε", "en": "quarters of epsilon make a diameter of epsilon"},
  5: {"zh": "第 7 節：Cauchy 序列", "en": "Section 7: Cauchy sequences"},
  6: {"zh": "引理 7.1 與 7.2", "en": "Lemmas 7.1 and 7.2"},
  7: {"zh": "Lipschitz 送得過去，連續不夠", "en": "Lipschitz carries it over, continuity does not"},
  8: {"zh": "完備，以及 Banach 空間", "en": "complete, and Banach spaces"},
  9: {"zh": "定理 7.3：完備性搬得動", "en": "Theorem 7.3: completeness travels"},
  10: {"zh": "有限維一定是 Banach 空間", "en": "finite dimensions are always Banach"},
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
 def _shared_delta(self):
  ox, oy = -5.85, -0.72
  sx, sy = 4.30, 1.85
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  cols = (ACCENT_B, ACCENT_C, WARN, ACCENT_A)
  for (k, c0), col in zip(zip(FAM_KS, FAM_C), cols):
   g.add(self._plot(lambda x, k=k, c0=c0: c0 + 0.42 * _fam(k, x),
                    ox, oy, sx, sy, col, sw=1.9))
   cy = oy + sy * (c0 + 0.42 * _fam(k, P0))
   g.add(self._rect(ox + sx * P0, cy, sx * DELTA0, sy * 0.42 * EPS0, col, sw=1.3))
  g.add(self._dash([ox + sx * P0, oy, 0], [ox + sx * P0, oy + sy * 1.05, 0],
                   DIM, n=14, sw=1.0))
  g.add(self._panel(((0.86, "每一個 f 都在那一點連續",
                      "every f in the family is continuous there", ACCENT_B),
                     (0.20, "而且同一個 δ 對整族都行",
                      "and one delta serves the whole family", WARN),
                     (-0.46, "均勻連續是「一個 δ 對很多點」",
                      "uniform continuity was one delta for many points", ACCENT_A))))
  return g.add(self._foot("這一次是「一個 δ 對很多個函數」——同一個量詞把戲，換了一個方向",
                          "this time it is one delta for many functions: the same trick, turned a different way",
                          ACCENT_A,
                          "畫面上四個框寬度一模一樣，那個共同的寬度就是 δ",
                          "the four boxes on screen share one width, and that shared width is delta"))

 def _mvt(self):
  ox, oy = -5.85, 0.05
  sx, sy = 4.10, 0.72
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4))
  cols = (ACCENT_B, ACCENT_C, WARN)
  for (a, c0), col in zip(WEDGE, cols):
   g.add(self._plot(lambda x, a=a, c0=c0: c0 + a * math.sin(3.0 * x) / 3.0,
                    ox, oy, sx, sy, col, sw=1.8, x0=-1.0, x1=1.0))
  # the box sits on the middle curve, and the wedge arms of slope m reach its corners
  a_mid, c_mid = WEDGE[1]
  cx = ox + sx * (XSTAR + 1.0) / 2.0
  cy = oy + sy * (c_mid + a_mid * math.sin(3.0 * XSTAR) / 3.0)
  hw, hh = sx * DELTA1 / 2.0, sy * EPS1
  g.add(self._rect(cx, cy, hw, hh, ACCENT_A, sw=1.6))
  for sx_, sy_ in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
   g.add(Line([cx, cy, 0], [cx + sx_ * hw, cy + sy_ * hh, 0],
              color=ACCENT_A, stroke_width=1.4))
  g.add(Dot([cx, cy, 0], radius=0.05, color=ACCENT_A))
  rows = [("       m            δ  =  ϵ / m", DIM)]
  for mm, dd in MVT:
   rows.append((f"     {mm:4d}              {dd:.3f}", ACCENT_C))
  g.add(self._table(rows, y0=0.80, dy=0.36))
  g.add(self._mid(-0.66, f"ϵ 固定成 {EPS1:.2f}，導數的界越大，δ 就越小",
                  f"with epsilon fixed at {EPS1:.2f}, a larger bound on the derivative buys a smaller delta",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("方框寬 δ、高 ϵ，而斜率 m 的那四條臂剛好走到四個角——這就是 δ = ϵ / m 的意思",
                          "the box is delta wide and epsilon tall, and the four arms of slope m reach exactly its corners: that is what delta equal to epsilon over m means",
                          ACCENT_A,
                          "均值定理把「導數的界」換成「函數值的界」，這一步就是整個例子",
                          "the mean value theorem trades a bound on the derivative for one on the values, and that is the whole example"))

 def _thm61(self):
  ox, sx = -5.60, 3.60
  g = VGroup()
  for oy, n, col, zh, en in ((0.66, 5, ACCENT_B, "定義域 A", "domain A"),
                             (-0.52, 4, ACCENT_C, "值域 B", "range B")):
   g.add(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2.4))
   for i in range(n):
    px = ox + sx * (i + 0.5) / n
    g.add(Dot([px, oy, 0], radius=0.055, color=WARN),
          self._circ(px, oy, sx / (2.0 * n), col, sw=1.1, n=36))
   # the labels sit beside their own line: above it they would land on the
   # other line's balls, and below the lower one they would reach the footnote
   g.add(self._mid(oy, zh, en, col, FS_TAG - 2, x=-0.90, w=2.00))
  g.add(self._panel(((0.86, "A 與 B 都全有界",
                      "both the domain and the range are totally bounded", ACCENT_B),
                     (0.20, "而且那一族均勻等度連續",
                      "and the family is uniformly equicontinuous", ACCENT_C),
                     (-0.46, "那麼那一族在一致度量下也全有界",
                      "then the family too is totally bounded, in the uniform metric", WARN))))
  return g.add(self._foot("也就是說：有限多個一致範數的球，就蓋得住整族函數",
                          "that is, finitely many balls in the uniform norm cover the whole family of functions",
                          ACCENT_A,
                          "上面五個球與下面四個球各自把自己那條線蓋滿，這就是兩邊全有界的意思",
                          "the five balls above and the four below each cover their own line, which is what totally bounded means here"))

 def _lattice(self):
  ox, oy = -5.30, -0.55
  dx, dy = 1.05, 0.62
  g = VGroup()
  for i in range(ND):
   g.add(self._dash([ox + i * dx, oy - 0.20, 0],
                    [ox + i * dx, oy + (NE - 1) * dy + 0.20, 0], DIM, n=8, sw=1.0))
   for j in range(NE):
    g.add(Dot([ox + i * dx, oy + j * dy, 0], radius=0.05, color=DIM))
  for path, col in zip(PATHS, (ACCENT_B, WARN)):
   g.add(self._curve([[ox + i * dx, oy + path[i] * dy, 0] for i in range(ND)],
                     col, sw=2.4))
   for i in range(ND):
    g.add(Dot([ox + i * dx, oy + path[i] * dy, 0], radius=0.07, color=col))
  g.add(self._mid(oy + (NE - 1) * dy + 0.42, "每一條折線就是一個 D → E 的函數",
                  "each polyline is one function from D to E", ACCENT_A,
                  FS_TAG - 1, x=ox + 1.6, w=5.20))
  g.add(self._table(((f"     # D  =  {ND}", ACCENT_B),
                     (f"     # E  =  {NE}", ACCENT_C),
                     (f"     # G  =  {NE} ^ {ND}  =  {NG}", WARN)), y0=0.80, dy=0.44))
  g.add(self._mid(-0.72, "有限，所以之後挑得出有限的 ε 稠密集",
                  "finite, so a finite epsilon-dense set can be picked later", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("D 在 A 裡 δ 稠密，E 在 B 裡 ε 除以四稠密，G 是所有從 D 到 E 的函數",
                          "D is delta-dense in the domain, E is a quarter-epsilon-dense in the range, and G is every function from D to E",
                          ACCENT_A,
                          "畫面上四欄三列，走法一共八十一種——有限這件事就是整個證明的支點",
                          "four columns and three rows give eighty-one paths, and that finiteness is the pivot of the whole proof"))

 def _diameter(self):
  g = VGroup()
  rows = (("ρ ( f p ′ , f p )              ≤   ϵ / 4", ACCENT_B),
          ("ρ ( f p  ,  h p )              ≤   ϵ / 2", ACCENT_C),
          ("ρ ( h p  ,  h p ′ )            ≤   ϵ / 4", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.78 - k * 0.50, lab, col, FS_TAG, x=-3.55, w=5.20))
  g.add(self._dash([-5.60, -0.60, 0], [-1.50, -0.60, 0], DIM, n=22, sw=1.2))
  g.add(self._sym(-0.92, "ρ ( f p ′ , h p ′ )            ≤       ϵ", ACCENT_A,
                  FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "每個 g 收集在 D 上跟它差不到 ε 除以四的 f",
                      "each g collects the f that stay a quarter of epsilon from it on D", ACCENT_B),
                     (0.20, "這些收集蓋得住整族",
                      "these collections cover the whole family", ACCENT_C),
                     (-0.46, "而且每一個的直徑都不超過 ε",
                      "and each of them has diameter at most epsilon", WARN))))
  return g.add(self._foot("兩個四分之一加一個二分之一，剛好湊成一個 ε——三角不等式走三步",
                          "two quarters and a half come to exactly one epsilon, in three steps of the triangle inequality",
                          ACCENT_A,
                          "書上證完之後說：這個論證完全初等，可是很難；「精巧」與「困難」不是同一回事",
                          "the book then says the argument is completely elementary and hard, and that sophisticated and difficult are not the same"))

 def _cauchy(self):
  ox, oy = -5.85, -0.10
  sx, sy = 4.30, 1.50
  nmax = 34
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  for n in range(2, nmax + 1):
   g.add(Dot([ox + sx * n / nmax, oy + sy * _seq(n), 0], radius=0.05,
             color=WARN if n > CAU_N else DIM))
  nx = ox + sx * CAU_N / nmax
  band = sy * EPS5 / 2
  for s in (band, -band):
   g.add(self._dash([nx, oy + s, 0], [ox + sx * 1.06, oy + s, 0], ACCENT_B, n=18, sw=1.2))
  g.add(self._dash([nx, oy - 0.62, 0], [nx, oy + 0.80, 0], ACCENT_A, n=10, sw=1.2),
        self._sym(oy + 0.62, f"N  =  {CAU_N}", ACCENT_A, FS_TAG - 1, x=nx + 0.70, w=1.30))
  g.add(self._panel(((0.86, "定義只提到項與項之間，沒有提到極限",
                      "the definition mentions only the terms, never a limit", ACCENT_B),
                     (0.20, f"ϵ = {EPS5:.2f} 時，這個序列的 N 是 {CAU_N}",
                      f"for epsilon of {EPS5:.2f} this sequence needs an N of {CAU_N}", WARN),
                     (-0.46, "紅色那些項兩兩都靠得比 ε 近，全部落在那條帶子裡",
                      "the red terms are all within epsilon of one another, inside the band", ACCENT_A))))
  return g.add(self._foot(f"這個 N 是程式搜出來的，不是湊的：到 {CAU_N} 為止還差得到 ε，之後就再也不會",
                          f"the N was found by search, not picked: up to {CAU_N} the terms still reach epsilon apart, after it they never do",
                          ACCENT_A,
                          "「項越靠越近的序列應該要收斂」——這一節就是在問這個「應該」何時成立",
                          "a sequence whose terms crowd together ought to converge, and this section asks when that ought holds"))

 def _lemmas(self):
  ox, oy = -5.60, 0.76
  g = VGroup(Line([ox, oy, 0], [ox + 4.30, oy, 0], color=DIM, stroke_width=1.6))
  a = ox + 2.15
  g.add(Dot([a, oy, 0], radius=0.07, color=ACCENT_A),
        self._sym(oy + 0.30, "a", ACCENT_A, FS_TAG - 1, x=a, w=0.60))
  for dxx, lab, col in ((-0.72, "x ₘ", ACCENT_B), (0.58, "x ₙ", WARN)):
   g.add(Dot([a + dxx, oy, 0], radius=0.06, color=col),
         self._sym(oy - 0.36, lab, col, FS_TAG - 1, x=a + dxx, w=0.70))
  g.add(self._sym(oy - 0.80, "ϵ / 2   +   ϵ / 2   =   ϵ", ACCENT_C, FS_TAG, x=a, w=3.20))
  oy2 = -0.92
  g.add(Line([ox, oy2, 0], [ox + 4.30, oy2, 0], color=DIM, stroke_width=1.6))
  for i in range(11):
   px = ox + 4.30 * (0.06 + 0.88 * (1.0 - 1.0 / (i + 1.6)))
   pick = i in (1, 4, 7, 10)
   g.add(Dot([px, oy2, 0], radius=0.075 if pick else 0.045,
             color=WARN if pick else DIM))
  g.add(self._mid(oy2 + 0.40, "紅色那一支收斂，整個序列就跟著收斂",
                  "the red subsequence converges, so the whole sequence does", WARN,
                  FS_TAG - 1, x=ox + 2.15, w=4.60))
  g.add(self._panel(((0.86, "引理 7.1：收斂的一定是 Cauchy 的",
                      "Lemma 7.1: a convergent sequence is Cauchy", ACCENT_B),
                     (0.20, "把三角不等式從極限那裡切成兩半",
                      "split the triangle inequality in half at the limit", ACCENT_C),
                     (-0.46, "引理 7.2：Cauchy 加一支收斂的子序列就夠",
                      "Lemma 7.2: Cauchy plus one convergent subsequence is enough", WARN))))
  return g.add(self._foot("引理 7.2 後面會一直用：只要抓得到一支收斂的，整個序列就被拖過去",
                          "Lemma 7.2 gets used constantly later: catch one convergent subsequence and the whole sequence follows it",
                          ACCENT_A,
                          "兩條合起來說：對 Cauchy 序列而言，「有子序列收斂」與「自己收斂」是同一件事",
                          "together they say that for a Cauchy sequence, having a convergent subsequence and converging are the same thing"))

 def _lipschitz(self):
  ox, sx = -5.85, 4.30
  g = VGroup()
  for oy in (0.80, -0.40):
   g.add(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=1.6))
  cols = (ACCENT_B, ACCENT_C, WARN)
  for (n, v), col in zip(SRC, cols):
   px = ox + sx * v * 6.0
   qx = ox + sx * (n / 100.0)
   g.add(Dot([px, 0.80, 0], radius=0.06, color=col),
         Dot([qx, -0.40, 0], radius=0.06, color=col),
         self._arr([px, 0.68, 0], [qx, -0.28, 0], col, sw=1.6, tl=0.10))
  g.add(self._mid(1.14, "定義域：1／n 擠在一起", "in the domain the terms 1/n huddle",
                  ACCENT_A, FS_TAG - 1, x=ox + 2.15, w=4.60),
        self._mid(-0.78, "像：n 越跑越開", "in the image the terms n run apart",
                  WARN, FS_TAG - 1, x=ox + 2.15, w=4.60))
  g.add(self._table((("       n          1 / n            1 / ( 1 / n )", DIM),)
                    + tuple((f"    {n:4d}        {v:.4f}          {n:6.1f}", ACCENT_C)
                            for n, v in SRC), y0=0.80, dy=0.36))
  g.add(self._mid(-0.66, f"距離從 {GAP_IN:.3f} 變成 {GAP_OUT:.0f}",
                  f"the spread goes from {GAP_IN:.3f} to {GAP_OUT:.0f}", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("Lipschitz 把 Cauchy 送成 Cauchy，有界線性映射是特例；定理 7.1 推廣到均勻連續",
                          "Lipschitz maps carry Cauchy to Cauchy, bounded linear maps being a special case, and Theorem 7.1 extends it to uniformly continuous ones",
                          ACCENT_A,
                          "可是「連續」不夠：一除以 x 在半開區間上連續，卻把上面那一列拆成下面那一列",
                          "continuity alone will not do: one over x is continuous on the half-open interval and still pulls the upper row into the lower one"))

 def _complete(self):
  ox, oy = -5.70, -0.62
  sx, sy = 4.20, 1.55
  lo, hi = 1.90, 2.78
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.10, 0], [ox, oy + sy * 1.02, 0], color=DIM, stroke_width=1.4))
  ey = oy + sy * (math.e - lo) / (hi - lo)
  # the asymptote stops short of the hollow circle, so the circle reads as an
  # open end rather than a bead threaded on the line
  g.add(self._dash([ox, ey, 0], [ox + sx * 1.02 - 0.11, ey, 0], ACCENT_A, n=20, sw=1.2))
  pts = []
  for i, v in enumerate(E_VALS):
   px = ox + sx * (i + 0.5) / len(E_VALS)
   py = oy + sy * (v - lo) / (hi - lo)
   pts.append([px, py, 0])
   g.add(Dot([px, py, 0], radius=0.055, color=ACCENT_C))
  g.add(self._curve(pts, ACCENT_C, sw=1.4))
  g.add(self._circ(ox + sx * 1.02, ey, 0.09, ACCENT_A, sw=2.0),
        self._sym(ey + 0.34, "e   ∉   ℚ", ACCENT_A, FS_TAG, x=ox + sx * 0.86, w=1.80))
  g.add(self._sym(oy + 0.32, "( 1 + 1 / n ) ⁿ", ACCENT_C,
                  FS_TAG - 1, x=ox + 2.30, w=2.10))
  g.add(self._mid(0.24, "每一項都是有理數，可是極限不是",
                  "every term is a rational number, and the limit is not", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "完備：每個 Cauchy 序列都收斂到裡面的一點",
                  "complete: every Cauchy sequence converges to a point inside", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "完備的賦範空間就叫 Banach 空間",
                  "and a complete normed space is called a Banach space", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  g.add(self._sym(0.84, f"{E_FRACS[1]}  ,  {E_FRACS[2]}  ,  {E_FRACS[3]}  ,  …",
                  ACCENT_C, FS_TAG - 2, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 7.2：實數線完備。證明是「Cauchy 序列有界，所以有收斂子序列」，再引用引理 7.2",
                          "Theorem 7.2: the line is complete, because a Cauchy sequence is bounded and so has a convergent subsequence, and then Lemma 7.2 finishes it",
                          ACCENT_A,
                          "空心那個圈就是「該收斂卻無處可去」：在 ℚ 裡這是 Cauchy 序列，極限卻掉在外面",
                          "the hollow circle is a limit with nowhere to go: in the rationals this sequence is Cauchy and its limit falls outside"))

 def _travels(self):
  g = VGroup()
  g.add(self._rect(-4.55, 0.42, 1.05, 0.32, ACCENT_B),
        self._mid(0.42, "A 完備", "A complete", ACCENT_B, FS_TAG, x=-4.55, w=2.00))
  g.add(self._rect(-1.75, 0.42, 1.05, 0.32, WARN),
        self._mid(0.42, "B 完備", "B complete", WARN, FS_TAG, x=-1.75, w=2.00))
  g.add(self._arr([-3.45, 0.62, 0], [-2.85, 0.62, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-2.85, 0.22, 0], [-3.45, 0.22, 0], ACCENT_C, sw=2.5, tl=0.12))
  g.add(self._mid(-0.28, "往右：f 連續、雙射", "rightward: f continuous and bijective",
                  ACCENT_A, FS_TAG - 1, x=-3.15, w=2.90),
        self._mid(-0.78, "往左：f ⁻¹ 是 Lipschitz 的", "leftward: the inverse is Lipschitz",
                  ACCENT_C, FS_TAG - 1, x=-3.15, w=2.90))
  g.add(self._panel(((0.86, "可逆的有界線性映射把 Banach 空間送成 Banach 空間",
                      "an invertible bounded linear map carries a Banach space to one", ACCENT_B),
                     (0.20, "推論：等價的範數要嘛都完備，要嘛都不完備",
                      "corollary: equivalent norms are complete together or not at all", WARN),
                     (-0.46, "所以完備性是範數等價類的性質",
                      "so completeness belongs to the equivalence class, not to one norm", ACCENT_A))))
  return g.add(self._foot("「連續」只保住收斂，「反函數 Lipschitz」才保得住 Cauchy——這就是為什麼兩個條件都要",
                          "continuity alone preserves convergence; it takes a Lipschitz inverse to preserve Cauchy, which is why both hypotheses appear",
                          ACCENT_A,
                          "第 3 章的等價範數到這裡才拿到完備性這一項，補上了那時缺的一塊",
                          "the equivalent norms of chapter 3 only now acquire completeness, filling in a piece that was missing then"))

 def _finite_dim(self):
  g = VGroup()
  boxes = (("ℝ", 0.42, 0.70, ACCENT_B), ("ℝ  ×  ℝ", 0.72, 1.30, ACCENT_C),
           ("ℝ ⁿ", 0.48, 0.85, WARN), ("dim V  <  ∞", 0.92, 1.75, ACCENT_A))
  xs = (-5.05, -3.30, -1.45, 0.65)
  for (lab, hw, tw, col), x in zip(boxes, xs):
   g.add(self._rect(x, 0.46, hw, 0.30, col),
         self._sym(0.46, lab, col, FS_TAG + 1, x=x, w=tw))
  labs = (("定理 7.2", "Theorem 7.2", ACCENT_B),
          ("定理 7.4", "Theorem 7.4", ACCENT_C),
          ("推論 1", "Corollary 1", WARN))
  for (x0, hw0), (x1, hw1), (zh, en, col) in zip(
          [(x, b[1]) for x, b in zip(xs, boxes)],
          [(x, b[1]) for x, b in zip(xs[1:], boxes[1:])], labs):
   g.add(self._arr([x0 + hw0 + 0.06, 0.46, 0], [x1 - hw1 - 0.06, 0.46, 0],
                   ACCENT_A, sw=2.2, tl=0.10),
         self._mid(-0.06, zh, en, col, FS_TAG - 2, x=(x0 + x1) / 2, w=1.80))
  g.add(self._mid(-0.62, "最後一步用第 4 節的定理 4.6：有限維上所有範數等價",
                  "the last step uses Theorem 4.6 of section 4: in finite dimensions all norms are equivalent",
                  ACCENT_A, FS_TAG, w=11.9))
  return g.add(self._foot("所以每一個有限維向量空間，配上任何一個範數，都是 Banach 空間",
                          "so every finite-dimensional vector space, under any norm at all, is a Banach space",
                          ACCENT_A,
                          "實數線完備、乘積保持完備、有限維上範數都等價——三件事扣在一起就是這條推論",
                          "the line is complete, products preserve it, and in finite dimensions all norms agree: those three lock together into the corollary"))

 def stage(self):
  a, b, c = self._shared_delta(), self._mvt(), self._thm61()
  d, e, f = self._lattice(), self._diameter(), self._cauchy()
  h, i, j = self._lemmas(), self._lipschitz(), self._complete()
  k, l = self._travels(), self._finite_dim()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE60ZH, AdvCalcE60EN = make(AdvCalcE60Base, "60", prefix="AdvCalcE")
