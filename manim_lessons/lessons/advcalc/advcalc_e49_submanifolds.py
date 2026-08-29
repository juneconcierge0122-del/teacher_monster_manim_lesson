"""advcalc E49 -- chapter 3, section 12 (book pp. 172-175): submanifolds and
Lagrange multipliers.  A graph is an n-dimensional patch; a submanifold is a set
that is a patch near each of its points, which is what the sphere is and a graph
is not.  Theorem 12.1 makes a zero set a submanifold whenever the differential
is surjective on it, and Theorem 12.2 replaces "dF vanishes" by "dF is l after
dG" for a maximum constrained to lie on one.  Section 12 has no exercises;
section 13 starts halfway down page 175.

Every number on screen is computed here.  The sphere's gradient is checked to be
nonzero at four of its points (so dG is onto and Theorem 12.1 applies) and zero
at the origin (which is not on it).  For Theorem 12.2 the two gradients are
checked to be parallel at the north pole with multiplier one half, and checked
NOT to be parallel at a nearby point of the sphere -- without that second check
the beat would show a condition that holds everywhere and says nothing.  The
closing example is E44's box again, solved by a multiplier instead of by
substitution: the multiplier comes out at exactly 2 and the area at 24, which is
the number E44 arrived at the other way.
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


def _grad(f, a, n=3):
 """Central differences, so the arrows drawn are not the ones written down."""
 out = []
 for j in range(n):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  out.append((f(tuple(p)) - f(tuple(m))) / (2 * H))
 return tuple(out)


# ── beats 1 to 5: the sphere as a submanifold ──────────────────────────
def _g(x):
 return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 1.0


SPHERE_PTS = ((0.0, 1.0, 0.0), (0.6, 0.8, 0.0), (0.0, 0.6, 0.8), (0.6, 0.0, 0.8))
for _p in SPHERE_PTS:
 assert abs(_g(_p)) < 1e-12, "a sample point is not on the sphere"
 assert max(abs(v) for v in _grad(_g, _p)) > 1.0, \
     "dG must be onto at every point of the zero set, or Theorem 12.1 does not apply"
assert max(abs(v) for v in _grad(_g, (0.0, 0.0, 0.0))) < 1e-6, \
    "the one point where it fails is the origin, which is not on the sphere"

# the null space of dG is two dimensional there, which is why S is a surface
NULL_DIM = 3 - 1
assert NULL_DIM == 2, "the tangent space of a surface in three-space is two dimensional"


# ── beats 6 to 8 and 10: the constrained maximum on the sphere ─────────
def _F(x):
 return x[1]


def _on_sphere(n=90):
 for i in range(n + 1):
  th = math.pi * i / n
  for j in range(2 * n):
   ph = 2 * math.pi * j / (2 * n)
   yield (math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph))


NP = (0.0, 1.0, 0.0)
BEST = max(_F(p) for p in _on_sphere())
assert abs(BEST - _F(NP)) < 1e-9, "the maximum is at the north pole"

LMULT = _grad(_F, NP)[1] / _grad(_g, NP)[1]
assert abs(LMULT - 0.5) < 1e-6, "the beat prints one half"
assert max(abs(a - LMULT * b) for a, b in zip(_grad(_F, NP), _grad(_g, NP))) < 1e-6, \
    "dF is not l after dG at the maximum, so Theorem 12.2 would be false here"

# and the condition has to fail somewhere, or the beat says nothing
QPT = (0.6, 0.8, 0.0)
_a, _b = _grad(_F, QPT), _grad(_g, QPT)
CROSS = _a[0] * _b[1] - _a[1] * _b[0]
assert abs(CROSS) > 0.5, "the two gradients must not be parallel away from the maximum"


# ── beat 10: E44's box again, this time with a multiplier ──────────────
VOL = 8.0


def _A(v):
 return 2 * (v[0] * v[1] + v[1] * v[2] + v[2] * v[0])


def _Vc(v):
 return v[0] * v[1] * v[2] - VOL


EDGE = VOL ** (1 / 3)
CUBE = (EDGE, EDGE, EDGE)
assert abs(_Vc(CUBE)) < 1e-9, "the cube does not have the right volume"
_gA, _gV = _grad(_A, CUBE), _grad(_Vc, CUBE)
LAM = _gA[0] / _gV[0]
assert max(abs(a - LAM * b) for a, b in zip(_gA, _gV)) < 1e-4, \
    "the cube is not a Lagrange critical point of the area under the volume constraint"
assert abs(LAM - 2.0) < 1e-4, "the beat prints two"
assert abs(_A(CUBE) - 24.0) < 1e-9, "E44 got twenty four the other way; this must agree"
assert abs(EDGE - 2.0) < 1e-12


class AdvCalcE49Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 49

 MODE_LABEL = {
  0: {"zh": "一張圖形就是一塊", "en": "a graph is a patch"},
  1: {"zh": "球面不是一張圖形", "en": "the sphere is not a graph"},
  2: {"zh": "子流形：每一點附近都是一塊", "en": "a submanifold: a patch near each point"},
  3: {"zh": "定理 12.1：零集合什麼時候是子流形", "en": "Theorem 12.1: when a zero set is one"},
  4: {"zh": "證明：零空間就是那個 V", "en": "the proof: the null space is the V"},
  5: {"zh": "切向量：曲線的等價類", "en": "a tangent vector: a class of curves"},
  6: {"zh": "有約束時 dF 不會是零", "en": "constrained, dF does not vanish"},
  7: {"zh": "定理 12.2：換成 dF 等於 l 接上 dG", "en": "Theorem 12.2: dF becomes l after dG"},
  8: {"zh": "證明：還是隱函數定理", "en": "the proof: the implicit function theorem again"},
  9: {"zh": "座標下就是乘子法", "en": "in coordinates: the multiplier rule"},
  10: {"zh": "兩個例子，其中一個是 E44", "en": "two examples, one of them E44's"},
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

 def _ellipse(self, cx, cy, rx, ry, col, sw=1.6, n=80, a0=0.0, a1=2 * math.pi):
  return self._curve([[cx + rx * math.cos(a0 + (a1 - a0) * k / n),
                       cy + ry * math.sin(a0 + (a1 - a0) * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _ball(self, cx, cy, r, col=ACCENT_C, sw=2.2):
  """A sphere drawn as an outline plus two latitudes and one meridian."""
  g = VGroup(self._circ(cx, cy, r, col, sw=sw))
  for f in (0.45, -0.45):
   g.add(self._ellipse(cx, cy + f * r, r * math.sqrt(1 - f * f), 0.30 * r, DIM, sw=1.3))
  g.add(self._ellipse(cx, cy, 0.36 * r, r, DIM, sw=1.3))
  return g

 # the axonometric frame the first beat's patch is drawn in
 EX, EY, EZ = (1.02, -0.33), (0.64, 0.33), (0.0, 0.78)

 def _P(self, ox, oy, x, y, z):
  return [ox + self.EX[0] * x + self.EY[0] * y + self.EZ[0] * z,
          oy + self.EX[1] * x + self.EY[1] * y + self.EZ[1] * z, 0]

 def _height(self, x, y):
  return 0.30 * (x * x - 0.6 * y * y) + 0.60

 def _domain(self, ox, oy, col=DIM):
  g = VGroup()
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([self._P(ox, oy, u, v / 4.0, 0.0) for v in range(-4, 5)], col, sw=1.1),
         self._curve([self._P(ox, oy, v / 4.0, u, 0.0) for v in range(-4, 5)], col, sw=1.1))
  return g

 def _sheet(self, ox, oy, col=ACCENT_B, sw=2.0):
  g = VGroup()
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(self._curve([self._P(ox, oy, u, v / 8.0, self._height(u, v / 8.0))
                      for v in range(-8, 9)], col, sw=sw),
         self._curve([self._P(ox, oy, v / 8.0, u, self._height(v / 8.0, u))
                      for v in range(-8, 9)], col, sw=sw))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _patch(self):
  ox, oy = -3.95, -0.30
  g = VGroup(self._domain(ox, oy), self._sheet(ox, oy))
  g.add(self._panel(((0.86, "灰色的格子是 V 裡的一個開集",
                      "the grey grid is an open set in V", DIM),
                     (0.20, "藍色那一張是 F 的圖形",
                      "the blue sheet is the graph of F", ACCENT_B),
                     (-0.46, "書上把這樣的 F 叫做一塊，n 維的塊",
                      "the book calls such an F an n-dimensional patch", ACCENT_A))))
  return g.add(self._foot("第 12 節開始講流形，而流形是用「一塊一塊」拼出來的",
                          "section 12 begins manifolds, and manifolds are built out of patches",
                          ACCENT_A,
                          "n 是定義域那一側的維數，m 是值域那一側的",
                          "n is the dimension on the domain side and m the one on the range side"))

 def _notagraph(self):
  cx, cy, r = -4.15, 0.05, 1.05
  g = VGroup(self._ball(cx, cy, r))
  for th, col in ((0.9, WARN), (3.5, ACCENT_B)):
   px, py = cx + r * math.cos(th), cy + r * math.sin(th)
   g.add(Dot([px, py, 0], radius=0.065, color=col), self._circ(px, py, 0.42, col, sw=2))
  g.add(self._panel(((0.86, "整顆球面寫不成一張圖形",
                      "the whole sphere is not the graph of anything", ACCENT_C),
                     (0.20, "不管怎麼把三維空間拆成直和都不行",
                      "no way of splitting three-space as a direct sum helps", DIM),
                     (-0.46, "可是每一小塊都是一張圖形",
                      "yet each small piece of it is a graph", WARN))))
  return g.add(self._foot("兩個圈是兩塊，它們重疊的地方兩張圖形都成立",
                          "the two circles are two patches, and both graphs hold where they overlap",
                          ACCENT_A,
                          "每一塊各自挑自己的 V 與 W——挑切平面與它的法線最省事",
                          "each patch picks its own V and W; the tangent plane and its normal are easiest"))

 def _submanifold(self):
  cx, cy, r = -4.15, 0.05, 1.05
  g = VGroup(self._ball(cx, cy, r))
  # a first draft put this at th = 1.15, where the marker circle and its label
  # ran off the top of the frame; keep the whole circle inside
  th = 0.65
  px, py = cx + r * math.cos(th), cy + r * math.sin(th)
  g.add(Dot([px, py, 0], radius=0.07, color=WARN), self._circ(px, py, 0.52, WARN, sw=2.2))
  g.add(self._sym(py, "N", WARN, FS_TAG, x=px + 0.82, w=0.70))
  g.add(self._panel(((0.86, "S 上每一點都有一個鄰域 N",
                      "every point of S has a neighborhood N", WARN),
                     (0.20, "N 與 S 交出來是一塊 n 維的塊",
                      "whose intersection with S is an n-dimensional patch", ACCENT_B),
                     (-0.46, "這句話就是子流形的定義",
                      "that sentence is the definition of a submanifold", ACCENT_A))))
  return g.add(self._foot("如果每一塊對應的那個函數都連續可微，就說 S 是光滑的",
                          "if the function of every patch is continuously differentiable, S is smooth",
                          ACCENT_A,
                          "球面就是三維空間裡一個二維的光滑子流形",
                          "the sphere is a two dimensional smooth submanifold of three-space"))

 def _thm121(self):
  cx, cy, r = -4.75, 0.05, 0.92
  g = VGroup(self._ball(cx, cy, r))
  for th in (0.6, 2.3, 4.2, 5.4):
   px, py = cx + r * math.cos(th), cy + r * math.sin(th)
   g.add(Dot([px, py, 0], radius=0.055, color=WARN),
         self._arr([px, py, 0], [cx + 1.42 * r * math.cos(th), cy + 1.42 * r * math.sin(th), 0],
                   WARN, sw=2, tl=0.10))
  g.add(self._sym(0.86, "G  ∈  C ¹ ( U )        U  ⊂  X        dim X  =  n + m",
                  ACCENT_B, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "零集合上每一點的微分都是滿射",
                  "the differential is onto at every point of the zero set", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "那麼零集合是 n 維子流形",
                  "then the zero set is an n-dimensional submanifold", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "球面上梯度處處不為零，所以定理適用",
                  "on the sphere the gradient never vanishes, so it applies", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("四個取樣點的梯度都是程式算的，長度都大於一；唯一為零的是原點，而原點不在球面上",
                          "the gradient was computed at four of its points and is never small; only the origin gives zero",
                          ACCENT_A,
                          "「滿射」在這裡就是「梯度不是零向量」，因為值域是一維的",
                          "onto here just means the gradient is not the zero vector, the range being one dimensional"))

 def _proof121(self):
  g = VGroup()
  lines = (("dG ᵧ  :  X  ↠  Y", ACCENT_B),
           ("dim  N ( dG ᵧ )   =   ( n + m )  −  m   =   n", ACCENT_C),
           ("X   =   V  ×  W                ( dG ² ) ⁻¹   ∃", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "滿射，所以零空間的維數剛好是 n",
                      "onto, so the null space has dimension exactly n", ACCENT_B),
                     (0.20, "把零空間當 V，隨便取一個補空間當 W",
                      "take the null space as V and any complement as W", ACCENT_C),
                     (-0.46, "限制在 W 上是同構，隱函數定理就套得上",
                      "restricted to W it is an isomorphism, so the theorem applies", WARN))))
  return g.add(self._foot("維數那一步用的是第 2 章的定理 2.4，可逆那一步用的是 E47 的定理 11.2",
                          "the dimension step is Theorem 2.4 of chapter 2, the invertibility step E47's Theorem 11.2",
                          ACCENT_A,
                          "交出來的就是一塊圖形，於是零集合在那一點附近是一塊",
                          "what comes back is a graph, so the zero set is a patch near that point"))

 def _tangent(self):
  """Two different arcs with one tangent vector.

  A first version drew both arcs on the sphere itself. At that radius the two
  differ by about four hundredths of a unit, so the probe frame showed one
  smear at the top of the ball and the whole point of the beat was invisible.
  Draw the sphere for context and put the two arcs in a blow-up beside it,
  where the difference between them is the size of the picture.
  """
  cx, cy, r = -5.15, 0.15, 0.80
  th = 0.95
  px, py = cx + r * math.cos(th), cy + r * math.sin(th)
  g = VGroup(self._ball(cx, cy, r))
  g.add(Dot([px, py, 0], radius=0.06, color=WARN), self._circ(px, py, 0.26, WARN, sw=1.6))

  zx, zy, hw, hh = -2.30, 0.15, 1.32, 0.82
  g.add(self._rect(zx, zy, hw, hh, DIM, sw=1.2))
  g.add(self._arr([px + 0.34, py - 0.10, 0], [zx - hw - 0.14, zy + 0.34, 0], DIM, sw=1.4, tl=0.10))

  # the surface patch, drawn as a slanted grid so the arcs read as lying in it
  ex, ey = (0.92, 0.17), (0.30, 0.62)
  Q = lambda u, v: [zx + ex[0] * u + ey[0] * v, zy + ex[1] * u + ey[1] * v, 0]
  for w in (-1.0, -0.5, 0.0, 0.5, 1.0):
   g.add(Line(Q(-1.0, w), Q(1.0, w), color=DIM, stroke_width=1.0),
         Line(Q(w, -1.0), Q(w, 1.0), color=DIM, stroke_width=1.0))
  # both arcs run along ex at u = 0 and differ only in how they bend
  for bend, col in ((0.85, ACCENT_B), (-0.62, ACCENT_A)):
   g.add(self._curve([Q(k / 10.0, bend * (k / 10.0) ** 2) for k in range(-10, 11)],
                     col, sw=2.6))
  g.add(self._arr(Q(0, 0), Q(0.86, 0), WARN, sw=3, tl=0.14),
        Dot(Q(0, 0), radius=0.07, color=WARN))
  g.add(self._panel(((0.86, "藍色與橘色是曲面上兩條不同的曲線",
                      "the blue and orange arcs are two different curves in the surface", ACCENT_B),
                     (0.20, "在那一點卻有同一個切向量",
                      "with the same tangent vector at that point", ACCENT_A),
                     (-0.46, "所以切向量是曲線的一個等價類",
                      "so a tangent vector is an equivalence class of curves", WARN))))
  return g.add(self._foot("這是定理 10.2 的說法：切空間的元素恰好是 S 上曲線的切向量",
                          "this is Theorem 10.2: the tangent space is exactly the tangent vectors of arcs in S",
                          ACCENT_A,
                          "後面談抽象流形時沒有外面的空間可用，這個等價類就直接當成定義",
                          "for an abstract manifold there is no ambient space, and the class becomes the definition"))

 def _nozero(self):
  cx, cy, r = -4.35, 0.05, 1.05
  g = VGroup(self._ball(cx, cy, r))
  for f in (0.75, 0.35, -0.05, -0.45):
   g.add(self._dash([cx - 1.32, cy + f * r, 0], [cx + 1.32, cy + f * r, 0], DIM, n=16, sw=1.2))
  g.add(Dot([cx, cy + r, 0], radius=0.075, color=WARN),
        self._arr([cx + 1.05, cy - 0.30, 0], [cx + 1.05, cy + 0.30, 0], ACCENT_B, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "虛線是 F 的等高面",
                      "the dashed lines are the level sets of F", DIM),
                     (0.20, "最大值 1 在最上面那一點取到",
                      "the maximum, one, is at the topmost point", WARN),
                     (-0.46, "可是 F 線性，dF 就是 F，永遠不是零",
                      "yet F is linear, so dF is F and never vanishes", ACCENT_B))))
  return g.add(self._foot("所以「令微分等於零」在有約束的時候完全用不上——這正是需要另一條定理的理由",
                          "so setting the differential to zero is useless under a constraint, which is why another theorem is needed",
                          ACCENT_A,
                          "最大值是程式在球面上取樣掃出來的，確實落在那一點",
                          "the maximum was found here by sampling the sphere, and it does sit at that point"))

 def _thm122(self):
  # Two framed pictures: at the maximum the two gradients line up, and at a
  # nearby point of the same sphere they do not. Without the second frame the
  # beat would show a condition that holds everywhere and says nothing.
  cy, r, hw, hh = 0.12, 0.55, 1.05, 0.72
  g = VGroup()
  for ox, p in ((-5.00, NP), (-1.85, QPT)):
   g.add(self._rect(ox, cy, hw, hh, DIM, sw=1.2), self._circ(ox, cy, r, ACCENT_C, sw=1.8))
   px, py = ox + r * p[0], cy + r * p[1]
   gf, gg = _grad(_F, p), _grad(_g, p)
   nf = math.hypot(gf[0], gf[1])
   ng = math.hypot(gg[0], gg[1])
   g.add(self._arr([px, py, 0], [px + 0.44 * gg[0] / ng, py + 0.44 * gg[1] / ng, 0],
                   WARN, sw=2.5, tl=0.12),
         self._arr([px + 0.07, py - 0.07, 0],
                   [px + 0.07 + 0.29 * gf[0] / nf, py - 0.07 + 0.29 * gf[1] / nf, 0],
                   ACCENT_B, sw=2.5, tl=0.10),
         Dot([px, py, 0], radius=0.06, color=ACCENT_A))
  g.add(self._sym(cy - hh - 0.30, "dF   =   l  ∘  dG", ACCENT_A, FS_TAG - 1, x=-5.00, w=2.20),
        self._sym(cy - hh - 0.30, "dF   ≠   l  ∘  dG", DIM, FS_TAG - 1, x=-1.85, w=2.20))
  g.add(self._panel(((0.86, "紅色是 dG，藍色是 dF",
                      "red is dG and blue is dF", WARN),
                     (0.20, "左邊在最大值那一點，兩者平行",
                      "on the left, at the maximum, they are parallel", ACCENT_B),
                     (-0.46, "右邊換一個點，兩者就不平行了",
                      "on the right, at another point, they are not", DIM))))
  return g.add(self._foot("所以那個條件有內容：它在球面上大部分的點都不成立",
                          "so the condition has content: it fails at most points of the sphere",
                          ACCENT_A,
                          f"程式算出兩個梯度在最大值那裡的比值是 {LMULT:.1f}，在右邊那點的叉積是 {abs(CROSS):.2f}",
                          f"the ratio at the maximum comes out at {LMULT:.1f} and the cross product on the right at {abs(CROSS):.2f}"))

 def _proof122(self):
  g = VGroup()
  lines = (("K ( ξ )   =   F ( ξ , H ( ξ ) )                dK ₐ   =   0", ACCENT_B),
           ("0   =   dF ¹   +   dF ²  ∘  dH ₐ", ACCENT_C),
           ("0   =   dG ¹   +   dG ²  ∘  dH ₐ", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.82 - k * 0.56, lab, col, FS_TAG, x=-3.55, w=5.20))
  # the box used to sit at -0.66, whose upper edge cut the row above it
  g.add(self._rect(-3.55, -0.82, 2.35, 0.26, ACCENT_A),
        self._sym(-0.82, "l   =   dF ²  ∘  ( dG ² ) ⁻¹", ACCENT_A, FS_TAG, x=-3.55, w=4.50))
  g.add(self._panel(((0.86, "把 S 局部寫成圖形，限制上去得到 K",
                      "write S locally as a graph and restrict F to get K", ACCENT_B),
                     (0.20, "α 是 K 的臨界點，所以 dK 是零",
                      "alpha is a critical point of K, so dK vanishes", ACCENT_C),
                     (-0.46, "兩式解掉 dH，剩下的就是那個 l",
                      "eliminating dH between the two leaves that l", WARN))))
  return g.add(self._foot("第二個偏微分可逆是子流形那個假設給的，所以 dH 解得出來",
                          "the second partial differential inverts because S is a submanifold, so dH can be solved for",
                          ACCENT_A,
                          "把兩個分量各自接上投影再相加，就得到 dF 等於 l 接上 dG",
                          "composing each component with a projection and adding gives dF equal to l after dG"))

 def _cartesian(self):
  g = VGroup()
  g.add(self._sym(0.72, "∂F / ∂x ⱼ    −    Σ  c ᵢ  ∂g ⁱ / ∂x ⱼ    =    0",
                  ACCENT_B, FS_TAG + 1, x=-3.55, w=5.20),
        self._sym(0.10, "g ⁱ ( x )   =   0                i = 1 , … , m", WARN,
                  FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._rect(-3.55, -0.56, 2.35, 0.30, ACCENT_A),
        self._mid(-0.56, "n 加 m 個方程，n 加 m 個未知數",
                  "n plus m equations, n plus m unknowns", ACCENT_A, FS_TAG, x=-3.55, w=4.50))
  g.add(self._panel(((0.86, "上面那 n 條來自定理 12.2",
                      "the n equations above come from Theorem 12.2", ACCENT_B),
                     (0.20, "下面那 m 條是約束本身",
                      "the m below are the constraints themselves", WARN),
                     (-0.46, "未知數是 n 個座標加上 m 個乘子",
                      "the unknowns are n coordinates and m multipliers", ACCENT_A))))
  return g.add(self._foot("那些 c 就是對偶空間裡的泛函寫成座標的樣子——這就是「Lagrange 乘子」這個名字的來源",
                          "the coefficients are the functional on the dual written in coordinates, which is where the name comes from",
                          ACCENT_A,
                          "乘子不是要求的答案，可是不把它當未知數，方程就配不平",
                          "the multipliers are not what is wanted, yet without them as unknowns the count does not balance"))

 def _examples(self):
  g = VGroup()
  # The answers used to be a fifth row inside each column. The left one is far
  # too long for a 2.30-wide column and shrank to something unreadable, so both
  # answers now share one wide row underneath the two systems.
  left = (("0  −  2 c x ₁   =   0", ACCENT_B),
          ("1  −  2 c x ₂   =   0", ACCENT_B),
          ("0  −  2 c x ₃   =   0", ACCENT_B),
          ("Σ  x ᵢ ²   =   1", DIM))
  right = (("2 ( y + z )  −  λ y z   =   0", ACCENT_C),
           ("2 ( x + z )  −  λ x z   =   0", ACCENT_C),
           ("2 ( x + y )  −  λ x y   =   0", ACCENT_C),
           ("x y z   =   V", DIM))
  for k, (lab, col) in enumerate(left):
   g.add(self._sym(0.84 - k * 0.44, lab, col, FS_TAG - 2, x=-5.05, w=2.30))
  for k, (lab, col) in enumerate(right):
   g.add(self._sym(0.84 - k * 0.44, lab, col, FS_TAG - 2, x=-1.95, w=2.70))
  # one wide row for both answers shrank the text to half the size of the
  # equations above it; give each answer the width of its own column instead
  g.add(self._sym(-0.92, "⟨ 0 , ± 1 , 0 ⟩ ,   c  =  ± 1 / 2", WARN,
                  FS_TAG - 2, x=-5.00, w=2.55),
        self._sym(-0.92, f"x = y = z = {EDGE:.0f} ,   λ = {LAM:.0f}", WARN,
                  FS_TAG - 2, x=-1.95, w=2.70))
  g.add(self._panel(((0.86, "左邊：球面上第二個座標的極值",
                      "left: the second coordinate on the sphere", ACCENT_B),
                     (0.20, "右邊：E44 那個盒子，這次用乘子",
                      "right: E44's box, by a multiplier this time", ACCENT_C),
                     (-0.46, "前三式逼出三邊相等，約束再給出邊長",
                      "the first three force the edges equal and the constraint fixes them", WARN))))
  return g.add(self._foot(f"程式驗過：正方體那一點兩個梯度的比值正好是 {LAM:.0f}，表面積是 {_A(CUBE):.0f}，跟 E44 用代入法得到的一樣",
                          f"checked here: at the cube the two gradients differ by exactly {LAM:.0f}, and the area is {_A(CUBE):.0f}, as E44 got by substituting",
                          ACCENT_A,
                          "第 12 節到此結束，這一節整節沒有習題。下一集講第 13 節的函數相依性",
                          "that ends section 12, which has no exercises at all; next is section 13 on functional dependence"))

 def stage(self):
  a, b, c = self._patch(), self._notagraph(), self._submanifold()
  d, e, f = self._thm121(), self._proof121(), self._tangent()
  h, i, j = self._nozero(), self._thm122(), self._proof122()
  k, l = self._cartesian(), self._examples()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE49ZH, AdvCalcE49EN = make(AdvCalcE49Base, "49", prefix="AdvCalcE")
