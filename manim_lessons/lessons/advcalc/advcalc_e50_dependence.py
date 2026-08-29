"""advcalc E50 -- chapter 3, section 13 (book pp. 175-179): functional
dependence.  When is one of a collection of functions a function of the rest?
That is nearly, but not quite, the question of whether the range of the combined
mapping is a submanifold, and both directions of "nearly" fail in an instructive
way.  The tools are Theorem 13.1 (rank is lower semicontinuous) and Theorem 13.2
(a map of constant rank r has r-dimensional patches as local images), and the
corollary is the precise form of functional dependence.  Section 13 has no
exercises; section 14 starts partway down page 179.

Everything the beats claim is computed here.  Ranks are found by elimination,
not asserted by hand.  The lower-semicontinuity beat checks both halves of the
one-sidedness -- that arbitrarily small perturbations of a rank-deficient map
raise the rank, and that no perturbation within the theorem's epsilon lowers the
rank of an invertible one -- because showing only one half would make the
theorem look like plain continuity.  The corollary's example is checked to have
constant rank two and to satisfy its dependence exactly, and the closing
counterexample is checked to admit no monotone projection near the origin, which
is what stops its neighborhood there from being a patch.
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
H = 1e-6


def _rank(rows, tol=1e-9):
 """Rank by elimination, so no beat prints a rank that was assumed."""
 m = [list(map(float, r)) for r in rows]
 nr, nc = len(m), len(m[0])
 r = 0
 for c in range(nc):
  if r >= nr:
   break
  piv = max(range(r, nr), key=lambda i: abs(m[i][c]))
  if abs(m[piv][c]) < tol:
   continue
  m[r], m[piv] = m[piv], m[r]
  for i in range(nr):
   if i != r:
    f = m[i][c] / m[r][c]
    m[i] = [a - f * b for a, b in zip(m[i], m[r])]
  r += 1
 return r


def _jac(f, a, nout):
 """The Jacobian as a list of rows, by central differences."""
 cols = []
 for j in range(len(a)):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  cols.append([(u - v) / (2 * H) for u, v in zip(f(tuple(p)), f(tuple(m)))])
 return [[cols[j][i] for j in range(len(a))] for i in range(nout)]


# ── beat 2: dependent, yet the range is only a curve ───────────────────
def _twisted(t):
 return (t[0], t[0] ** 2, t[0] ** 3)


for _t in ((0.4,), (-0.7,), (1.3,)):
 assert _rank(_jac(_twisted, _t, 3)) == 1, \
     "the second and third depend on the first, so the range is a curve, not a surface"


# ── beat 3: the range is a surface, yet there is no global dependence ──
def _sph(u):
 s, t = u
 return (math.cos(s) * math.cos(t), math.sin(s) * math.cos(t), math.sin(t))


UP, DOWN = (0.7, 0.4), (0.7, -0.4)
assert max(abs(a - b) for a, b in zip(_sph(UP)[:2], _sph(DOWN)[:2])) < 1e-12, \
    "the two parameter points must agree in the first two functions"
assert abs(_sph(UP)[2] - _sph(DOWN)[2]) > 0.7, \
    "and disagree in the third, or there would be no obstruction to dependence"
for _u in (UP, DOWN, (2.1, 0.9)):
 assert _rank(_jac(_sph, _u, 3)) == 2, "the sphere's parametrisation has rank two"


# ── beat 4: rank three puts a whole ball inside the range ──────────────
def _full(x):
 return (x[0], x[1], x[2] + x[0] * x[1])


assert _rank(_jac(_full, (0.3, -0.2, 0.5), 3)) == 3, \
    "this one is onto a neighborhood, so its range lies on no surface"


# ── beats 5 and 6: rank is lower semicontinuous, and only that way ─────
def _norm(m):
 return max(sum(abs(v) for v in row) for row in m)


DEFICIENT = ((1.0, 0.0), (0.0, 0.0))
INVERTIBLE = ((1.0, 0.0), (0.0, 1.0))
assert _rank(DEFICIENT) == 1 and _rank(INVERTIBLE) == 2

# the rank of a deficient map jumps UP arbitrarily close to it
JUMPED = ((1.0, 0.0), (0.0, 1e-9))
assert _norm([[a - b for a, b in zip(r, q)] for r, q in zip(JUMPED, DEFICIENT)]) < 1e-8
assert _rank(JUMPED) == 2, "rank has to be able to jump up, or the theorem is plain continuity"

# but within the epsilon of the proof it never falls
STEP = 0.2
M_BOUND = 1.0
EPS = M_BOUND / 2
_perturb = [(a, b, c, d) for a in (-STEP, 0.0, STEP) for b in (-STEP, 0.0, STEP)
            for c in (-STEP, 0.0, STEP) for d in (-STEP, 0.0, STEP)]
for _q in _perturb:
 _d = ((_q[0], _q[1]), (_q[2], _q[3]))
 if _norm(_d) >= EPS:
  continue
 for _T in (DEFICIENT, INVERTIBLE):
  _S = tuple(tuple(a + b for a, b in zip(r, q)) for r, q in zip(_T, _d))
  assert _rank(_S) >= _rank(_T), "rank fell inside the epsilon, which Theorem 13.1 forbids"
# and the bound is not vacuous: at distance one the rank of either does fall
assert _rank(((0.0, 0.0), (0.0, 0.0))) == 0 and _norm(DEFICIENT) == 1.0 > EPS


# ── beats 7 to 9: constant rank, and the corollary's example ───────────
def _dep(v):
 x, y = v
 return (x + y, x - y, x * x - y * y)


DEP_PTS = ((1.0, 0.4), (-0.6, 2.0), (0.0, 0.0), (1.5, -1.5))
for _v in DEP_PTS:
 assert _rank(_jac(_dep, _v, 3)) == 2, "the example must have constant rank two"
 _f = _dep(_v)
 assert abs(_f[2] - _f[0] * _f[1]) < 1e-12, "the third is exactly the product of the first two"
DEP_ROWS = [(v, _dep(v)) for v in DEP_PTS[:3]]


# ── beat 10: constant rank does not make the whole range a submanifold ─
SPIN = 1.0


def _spiral(t):
 return (t * math.cos(SPIN / t), t * math.sin(SPIN / t))


_ts = [0.020 + (0.100 - 0.020) * k / 4000 for k in range(4001)]
TURNS = []
for _k in range(8):
 _u = (math.cos(math.pi * _k / 8), math.sin(math.pi * _k / 8))
 _v = [_spiral(t)[0] * _u[0] + _spiral(t)[1] * _u[1] for t in _ts]
 _d = [b - a for a, b in zip(_v, _v[1:])]
 TURNS.append(sum(1 for a, b in zip(_d, _d[1:]) if a * b < 0))
assert min(TURNS) >= 10, \
    "some direction projects the spiral monotonically, and then it would be a patch after all"


class AdvCalcE50Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 50

 MODE_LABEL = {
  0: {"zh": "誰是誰的函數", "en": "which is a function of which"},
  1: {"zh": "換個問法：像是不是曲面", "en": "restated: is the range a surface"},
  2: {"zh": "例外一：相依，可是像只是一條曲線", "en": "first exception: dependent, but only a curve"},
  3: {"zh": "例外二：像是曲面，卻只有局部相依", "en": "second: a surface, yet only locally dependent"},
  4: {"zh": "秩是三就裝不進曲面", "en": "rank three fits on no surface"},
  5: {"zh": "定理 13.1：秩跳得上去，掉不下來", "en": "Theorem 13.1: rank rises, never falls"},
  6: {"zh": "證明：在補空間上有下界", "en": "the proof: bounded below on a complement"},
  7: {"zh": "定理 13.2：常秩就有一塊", "en": "Theorem 13.2: constant rank gives a patch"},
  8: {"zh": "證明的骨架", "en": "the skeleton of the proof"},
  9: {"zh": "推論：這才是「函數相依」", "en": "the corollary: dependence, made precise"},
  10: {"zh": "那個小麻煩", "en": "the small difficulty"},
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

 EX, EY, EZ = (0.98, -0.32), (0.62, 0.32), (0.0, 0.80)

 def _P(self, ox, oy, x, y, z):
  return [ox + self.EX[0] * x + self.EY[0] * y + self.EZ[0] * z,
          oy + self.EX[1] * x + self.EY[1] * y + self.EZ[1] * z, 0]

 def _axes3(self, ox, oy, s=1.0, col=DIM):
  return VGroup(self._arr(self._P(ox, oy, 0, 0, 0), self._P(ox, oy, 1.25 * s, 0, 0), col, sw=1.4, tl=0.10),
                self._arr(self._P(ox, oy, 0, 0, 0), self._P(ox, oy, 0, 1.25 * s, 0), col, sw=1.4, tl=0.10),
                self._arr(self._P(ox, oy, 0, 0, 0), self._P(ox, oy, 0, 0, 1.25 * s), col, sw=1.4, tl=0.10))

 # ── beats ─────────────────────────────────────────────────────────
 def _question(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("f ¹", ACCENT_B), ("f ²", ACCENT_C), ("f ³", WARN))):
   g.add(self._rect(-5.35 + k * 1.20, 0.52, 0.44, 0.30, col),
         self._sym(0.52, lab, col, FS_TAG + 2, x=-5.35 + k * 1.20, w=0.90))
  g.add(self._arr([-4.15, 0.10, 0], [-4.15, -0.16, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._rect(-4.15, -0.52, 1.95, 0.32, ACCENT_A),
        self._sym(-0.52, "f ³   =   g ( f ¹ , f ² )      ?", ACCENT_A, FS_TAG + 1,
                  x=-4.15, w=3.70))
  g.add(self._panel(((0.86, "一組定義在同一個開集上的連續函數",
                      "a collection of continuous functions on one open set", DIM),
                     (0.20, "其中某一個是不是其他幾個的函數",
                      "is one of them a function of the rest?", ACCENT_B),
                     (-0.46, "這一節就是把這個問題問清楚",
                      "this section is about making that question precise", ACCENT_A))))
  return g.add(self._foot("要求的是一個兩變數的 g，在整個公共定義域上都對，不是只在某一點附近",
                          "what is asked for is a g of two variables holding on the whole common domain",
                          ACCENT_A,
                          "「相依」這個詞在線性代數裡有另一個意思，這裡講的是函數的相依",
                          "dependence means something else in linear algebra; here it is dependence of functions"))

 def _restate(self):
  ox, oy = -4.15, -0.35
  g = VGroup(self._axes3(ox, oy, 1.15))
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([self._P(ox, oy, 0.45 + 0.42 * u, 0.30 + 0.42 * v / 6.0,
                              0.55 + 0.22 * u * u - 0.16 * (v / 6.0) ** 2)
                      for v in range(-6, 7)], ACCENT_B, sw=2.0),
         self._curve([self._P(ox, oy, 0.45 + 0.42 * v / 6.0, 0.30 + 0.42 * u,
                              0.55 + 0.22 * (v / 6.0) ** 2 - 0.16 * u * u)
                      for v in range(-6, 7)], ACCENT_B, sw=2.0))
  g.add(self._panel(((0.86, "把三個函數併成一個映射",
                      "put the three together into one mapping", ACCENT_B),
                     (0.20, "問它的像是不是一個二維子流形",
                      "and ask whether its range is a two-dimensional submanifold", ACCENT_A),
                     (-0.46, "兩個問題幾乎一樣，可是兩邊各有一個例外",
                      "the two questions nearly agree, with one exception each way", WARN))))
  return g.add(self._foot("如果第三個真的是前兩個的函數，像就落在那個函數的圖形上，而圖形是二維的",
                          "if the third is a function of the first two, the range lies on that function's graph",
                          ACCENT_A,
                          "接下來兩拍就是那兩個例外，它們說明「幾乎」兩個字要放在哪裡",
                          "the next two beats are the exceptions, and they say where the word nearly belongs"))

 def _collapse(self):
  ox, oy = -4.35, -0.35
  g = VGroup(self._axes3(ox, oy, 1.15))
  g.add(self._curve([self._P(ox, oy, 0.60 * (k / 12.0) + 0.30,
                             0.60 * (k / 12.0) ** 2 + 0.10,
                             0.75 * (k / 12.0) ** 3 + 0.05) for k in range(0, 13)],
                    WARN, sw=3))
  g.add(self._sym(0.86, "f ²  =  g ∘ f ¹              f ³  =  h ∘ f ¹", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "第三個確實是前兩個的函數",
                  "the third really is a function of the first two", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "可是像縮成一條曲線，只有一維",
                  "yet the range collapses to a curve, only one-dimensional", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以「相依」推不出「像是二維的」",
                  "so dependence does not force the range to be two-dimensional", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("畫面上那條是 t 送到 t、t 平方、t 立方，程式驗過它的微分的秩處處是一",
                          "the curve is t to t, t squared, t cubed, and its differential is checked to have rank one",
                          ACCENT_A,
                          "像落在一個二維子流形「上面」，可是它自己不是一個二維子流形",
                          "the range lies on a two-dimensional submanifold without being one"))

 def _local(self):
  cx, cy, r = -4.35, 0.05, 1.00
  g = VGroup(self._circ(cx, cy, r, ACCENT_C, sw=2.2))
  for f in (0.42, -0.42):
   g.add(self._curve([[cx + r * math.sqrt(max(0.0, 1 - f * f)) * math.cos(2 * math.pi * k / 60),
                       cy + f * r + 0.30 * r * math.sin(2 * math.pi * k / 60), 0]
                      for k in range(61)], DIM, sw=1.3))
  ux = cx + r * 0.62
  g.add(Dot([ux, cy + 0.52, 0], radius=0.07, color=ACCENT_B),
        Dot([ux, cy - 0.52, 0], radius=0.07, color=WARN),
        self._dash([ux, cy - 0.52, 0], [ux, cy + 0.52, 0], DIM, n=6, sw=1.4))
  g.add(self._panel(((0.86, "像真的是一個二維子流形",
                      "the range genuinely is a two-dimensional submanifold", ACCENT_C),
                     (0.20, "可是這兩點的前兩個座標相同，第三個不同",
                      "yet these two points share the first two and differ in the third", WARN),
                     (-0.46, "所以整體上寫不成一個函數，只能局部",
                      "so no global function exists, only local ones", ACCENT_A))))
  return g.add(self._foot("能說的只有：每一點附近三個裡總有一個是另外兩個的函數",
                          "all one can say is that near each point one of the three is a function of the others",
                          ACCENT_A,
                          "走到球面的另一邊，要解出來的可能換成另外一個",
                          "on the far side of the sphere it may be a different one that has to be solved for"))

 def _rank3(self):
  ox, oy = -4.15, -0.30
  g = VGroup(self._axes3(ox, oy, 1.15))
  g.add(self._circ(ox + 0.95, oy + 0.62, 0.52, WARN, sw=2.5))
  for k in range(1, 4):
   g.add(self._circ(ox + 0.95, oy + 0.62, 0.52 * k / 4.0, DIM, sw=1.1))
  g.add(Dot([ox + 0.95, oy + 0.62, 0], radius=0.065, color=ACCENT_A))
  g.add(self._sym(0.86, "rank  dF ₐ   =   3", WARN, FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "隱函數定理說像裡含一整顆球",
                  "the implicit function theorem puts a whole ball in the range", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "一顆球裝不進任何二維的東西",
                  "and no ball fits inside anything two-dimensional", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以秩必須處處小於三",
                  "so the rank must everywhere be less than three", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這是必要條件；而秩處處等於二時，像基本上就是一個二維流形",
                          "that is necessary; and where the rank is everywhere two, the range essentially is a surface",
                          ACCENT_A,
                          "「基本上」這三個字要等到最後一拍才交代清楚",
                          "the word essentially is not settled until the last beat"))

 def _semicont(self):
  """Both halves of the one-sidedness, each in its own frame.

  A first version put all four matrices in one row with the arrows between
  them; at the default grid size the digits were tiny and the four bracket
  pairs read as one row of brackets. Frame each half and give the numbers the
  size of the rest of the beat.
  """
  g = VGroup()
  cols = ((-4.70, DEFICIENT, JUMPED, 1, 2, ACCENT_B),
          (-1.40, INVERTIBLE, INVERTIBLE, 2, 2, WARN))
  for gx, T, S, rt, rs, col in cols:
   g.add(self._rect(gx, 0.42, 1.55, 0.62, DIM, sw=1.2))
   a, _ = self._numgrid(gx - 0.82, 0.42, [[f"{v:.0f}" for v in row] for row in T],
                        color=DIM, dx=0.55, dy=0.52, size=FS_TAG)
   b, _ = self._numgrid(gx + 0.82, 0.42,
                        [[("ϵ" if 0 < abs(v) < 1e-3 else f"{v:.0f}") for v in row]
                         for row in S], color=col, dx=0.55, dy=0.52, size=FS_TAG)
   g.add(a, b, self._arr([gx - 0.20, 0.42, 0], [gx + 0.20, 0.42, 0], ACCENT_A,
                         sw=2.5, tl=0.10),
         self._sym(-0.50, f"rank   {rt}    →    {rs}", col, FS_TAG, x=gx, w=2.60))
  g.add(self._panel(((0.86, "左邊：秩 1 的旁邊有秩 2，任意近",
                      "left: rank two sits arbitrarily close to rank one", ACCENT_B),
                     (0.20, "右邊：秩 2 的旁邊全是秩 2",
                      "right: everything near rank two has rank two", WARN),
                     (-0.46, "所以秩跳得上去，掉不下來",
                      "so rank can jump up and cannot fall", ACCENT_A))))
  return g.add(self._foot(f"程式把 {len(_perturb)} 個擾動都試過，只要範數小於 {EPS:.1f}，秩就沒有掉下來過",
                          f"all {len(_perturb)} perturbations were tried here, and within norm {EPS:.1f} the rank never fell",
                          ACCENT_A,
                          "如果只演右邊那一半，看起來就只是連續性；左邊那一半才是「下半」兩個字的內容",
                          "showing only the right half would look like continuity; the left half is what lower means"))

 def _bound(self):
  """The one inequality the proof of Theorem 13.1 turns on, drawn as bars."""
  # The labels used to sit below their bars, which put each one closer to the
  # next bar than to its own and made the picture read off by one. Put each
  # label level with its bar, off to the right where all three line up.
  ox, oy, s = -6.05, 0.30, 3.10
  g = VGroup(Line([ox, oy - 0.90, 0], [ox, oy + 0.90, 0], color=DIM, stroke_width=1.4))
  bars = ((0.56, M_BOUND, WARN, "‖ T ( α ) ‖   ≥   m ‖ α ‖"),
          (0.02, EPS, ACCENT_C, "‖ ( S − T ) ( α ) ‖   ≤   ( m / 2 ) ‖ α ‖"),
          (-0.52, EPS, ACCENT_B, "‖ S ( α ) ‖   ≥   ( m / 2 ) ‖ α ‖"))
  for y, length, col, lab in bars:
   g.add(Line([ox, oy + y, 0], [ox + s * length, oy + y, 0], color=col, stroke_width=6),
         self._sym(oy + y, lab, col, FS_TAG - 2, x=-1.05, w=3.10))
  g.add(self._panel(((0.86, "T 在補空間 X 上有正的下界 m",
                      "T is bounded below on the complement X by a positive m", WARN),
                     (0.20, "S 與 T 的距離小於 m 的一半",
                      "S is within m over two of T", ACCENT_C),
                     (-0.46, "所以 S 在 X 上還是有下界，還是單射",
                      "so S is still bounded below on X, and still injective", ACCENT_B))))
  return g.add(self._foot("單射就表示 S 的像至少和 X 一樣大，而 X 的維數就是 T 的秩",
                          "injective means the range of S is at least as big as X, whose dimension is T's rank",
                          ACCENT_A,
                          "下界 m 的存在來自第 4 章的定理 4.2：有限維上的同構，反元素有界",
                          "the bound m comes from Theorem 4.2: an isomorphism in finite dimensions has a bounded inverse"))

 def _thm132(self):
  g = VGroup()
  g.add(self._rect(-5.05, 0.46, 1.15, 0.30, ACCENT_B),
        self._sym(0.46, "rank  dF ᵧ  ≡  r", ACCENT_B, FS_TAG, x=-5.05, w=2.10),
        self._rect(-5.05, -0.30, 1.15, 0.30, ACCENT_C),
        self._sym(-0.30, "r  <  dim W", ACCENT_C, FS_TAG, x=-5.05, w=2.10))
  g.add(self._arr([-3.70, 0.08, 0], [-3.20, 0.08, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-1.85, 0.08, 1.35, 0.32, WARN),
        self._sym(0.08, "F [ U ]   ≅   L  ⊂  ℝ ʳ", WARN, FS_TAG + 1, x=-1.85, w=2.50))
  g.add(self._panel(((0.86, "秩在整個定義域上是同一個 r",
                      "the rank is the same r throughout the domain", ACCENT_B),
                     (0.20, "每一點都有一個鄰域",
                      "then every point has a neighborhood", ACCENT_C),
                     (-0.46, "它的像是 W 裡一塊 r 維的塊",
                      "whose image is an r-dimensional patch in W", WARN))))
  return g.add(self._foot("常秩是關鍵：秩只要在定義域裡變一下，結論就沒了",
                          "constant rank is the point: let it vary anywhere and the conclusion goes",
                          ACCENT_A,
                          "而定理 13.1 保證秩不會突然掉下去，所以「常秩」這個假設檢查得動",
                          "and Theorem 13.1 keeps the rank from falling, which makes that hypothesis checkable"))

 def _skeleton(self):
  g = VGroup()
  lines = (("W   =   W ₁  ⊕  W ₂                W   =   W ₂  ⊕  dF [ V ]", ACCENT_B),
           ("P  :  W  ↠  W ₁                P ↾ dF [ V ]    ≅", ACCENT_C),
           ("ζ   =   P ∘ F ( ξ , G ( ζ , ξ ) )", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.82 - k * 0.56, lab, col, FS_TAG - 1, x=-3.55, w=5.20))
  g.add(self._rect(-3.55, -0.82, 2.15, 0.26, ACCENT_A),
        self._sym(-0.82, "F   =   K  ∘  P  ∘  F", ACCENT_A, FS_TAG + 1, x=-3.55, w=4.10))
  g.add(self._panel(((0.86, "把 W 拆成微分的像與一個補空間",
                      "split W into the range of the differential and a complement", ACCENT_B),
                     (0.20, "投影 P 在附近每一點都是同構",
                      "the projection P is an isomorphism at every nearby point", ACCENT_C),
                     (-0.46, "隱函數定理把它反解出來，式子就收乾淨",
                      "the implicit function theorem inverts it and the identity closes", WARN))))
  return g.add(self._foot("「附近每一點都是同構」這一步用的正是定理 13.1，這是它在這一節唯一的用處",
                          "the step about nearby points is exactly Theorem 13.1, its only use in the section",
                          ACCENT_A,
                          "最後一行寫成分量就是「第二組是第一組的函數」，也就是要證的東西",
                          "written in components the last line says the second block is a function of the first"))

 def _corollary(self):
  g = VGroup()
  g.add(self._sym(0.86, "f ¹  =  x + y        f ²  =  x − y        f ³  =  x ² − y ²",
                  ACCENT_B, FS_TAG, x=-3.35, w=5.60))
  rows = [("       x  ,  y                 f ¹ · f ²             f ³", DIM)]
  for v, f in DEP_ROWS:
   rows.append((f"( {v[0]:.1f} , {v[1]:.1f} )        {f[0] * f[1]:8.2f}      {f[2]:8.2f}",
                ACCENT_C))
  g.add(self._table(rows, x=-3.35, w=5.60, y0=0.28, dy=0.40))
  g.add(self._panel(((0.86, "三個函數，微分的秩處處是二",
                      "three functions whose differential has rank two everywhere", ACCENT_B),
                     (0.20, "所以三減二，也就是一個，是其餘的函數",
                      "so three minus two, that is one of them, is a function of the rest", ACCENT_C),
                     (-0.46, "這裡就是第三個等於前兩個的乘積",
                      "here the third is the product of the first two", WARN))))
  return g.add(self._foot("表格右邊兩欄是程式各自算的，四個取樣點上都相同，秩也都是二",
                          "the last two columns were computed separately here and agree at four sample points",
                          ACCENT_A,
                          "推論只保證局部；這個例子剛好整體都成立，那是這個例子特別好",
                          "the corollary only promises this locally; that it holds globally here is luck"))

 def _difficulty(self):
  ox, oy = -4.05, -0.20
  g = VGroup(self._axes3(ox, oy, 1.10))
  g.add(self._curve([self._P(ox, oy, 0.0, 0.0, 1.05 - 0.55 * k / 8.0) for k in range(9)],
                    ACCENT_B, sw=2.6))
  g.add(self._curve([self._P(ox, oy, 0.34 * math.sin(1.35 * k / 8.0),
                             0.0, 0.50 - 0.50 * (k / 8.0) ** 2) for k in range(9)],
                    ACCENT_B, sw=2.6))
  # A first version drew eight turns inside a radius of under one unit and the
  # spiral came out a solid blob. Three turns read as a spiral; that it keeps
  # turning is what the footer's assertion is for.
  pts = []
  for k in range(400):
   t = 0.045 + (0.32 - 0.045) * (1.0 - k / 399.0)
   x, y = _spiral(t)
   pts.append(self._P(ox, oy, x * 3.4, y * 3.4, 0.0))
  g.add(self._curve(pts, WARN, sw=2.2))
  g.add(Dot(self._P(ox, oy, 0, 0, 0), radius=0.07, color=ACCENT_A))
  g.add(self._circ(*self._P(ox, oy, 0, 0, 0)[:2], 0.46, ACCENT_A, sw=1.6))
  g.add(self._panel(((0.86, "曲線沿 z 軸下來，轉個彎後在平面上螺旋內縮",
                      "the curve comes down the axis, turns over, then spirals in", ACCENT_B),
                     (0.20, "它是一個區間的連續可微單射的像",
                      "it is the injective image of an interval", DIM),
                     (-0.46, "可是原點附近怎麼取鄰域，交出來都不是一塊",
                      "yet no neighborhood of the origin meets it in a patch", WARN))))
  return g.add(self._foot(f"程式對八個方向都算過：在原點附近，投影至少來回 {min(TURNS)} 次，所以沒有一個方向是單調的",
                          f"checked in eight directions: near the origin every projection turns at least {min(TURNS)} times",
                          ACCENT_A,
                          "沒有單調的投影就沒有一塊，所以它不是 ℝ³ 的一維子流形——問題出在嵌入方式",
                          "no monotone projection means no patch, so it is not a submanifold; the imbedding is at fault"))

 def stage(self):
  a, b, c = self._question(), self._restate(), self._collapse()
  d, e, f = self._local(), self._rank3(), self._semicont()
  h, i, j = self._bound(), self._thm132(), self._skeleton()
  k, l = self._corollary(), self._difficulty()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE50ZH, AdvCalcE50EN = make(AdvCalcE50Base, "50", prefix="AdvCalcE")
