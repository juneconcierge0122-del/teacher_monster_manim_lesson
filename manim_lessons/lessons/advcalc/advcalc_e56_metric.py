"""advcalc E56 -- chapter 4, section 1 (book pp. 195-200): metric spaces, open
and closed sets.  Everything the differential calculus did with convergence used
only the distance between two points, so the chapter distils that into three
axioms and rebuilds balls, open sets, interiors, closures and boundaries on top
of them.  Continuity becomes a statement about inverse images -- and pointedly
not about forward images.  Pages 200-201 are exercises 1.1 to 1.15, the first
exercises since page 171.

Four of the beats rest on computations.  The great-circle metric is checked to
satisfy the triangle inequality on sampled triples, and the distance function is
checked to be Lipschitz with constant exactly one rather than merely at most
one.  The two counterexamples about forward images are computed: the arctangent
approaches its bound without reaching it, and the image of the positive integers
under two x over one plus x squared is shown creeping toward a zero it never
attains.  The closing beat builds the sequence Lemma 1.5 promises and watches its
distance climb toward one while staying strictly below it, which is the finite
shadow of the infinite-dimensional failure the book warns about.
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


# ── beat 2: a metric that comes from no norm ───────────────────────────
def _unit(th, ph):
 return (math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th))


def _great(u, v):
 d = sum(a * b for a, b in zip(u, v))
 return math.acos(max(-1.0, min(1.0, d)))


SPH = [_unit(0.4 + 0.7 * i, 0.3 + 1.1 * j) for i in range(3) for j in range(3)]
for _x in SPH:
 for _y in SPH:
  for _z in SPH:
   assert _great(_x, _z) <= _great(_x, _y) + _great(_y, _z) + 1e-12, \
       "the great-circle distance broke the triangle inequality"
assert max(_great(_x, _y) for _x in SPH for _y in SPH) > 2.0, \
    "the samples should be spread out enough for the check to mean something"


# ── beat 3: Lemma 1.1, and Lemma 1.2's Lipschitz constant ──────────────
def _d2(a, b):
 return math.hypot(a[0] - b[0], a[1] - b[1])


PCEN, RAD = (0.0, 0.0), 1.0
QPT = (0.55, 0.30)
DELTA = RAD - _d2(PCEN, QPT)
assert DELTA > 0, "the sample point has to be inside the ball"
for _k in range(720):
 _a = 2 * math.pi * _k / 720
 for _t in (0.999, 0.5):
  _x = (QPT[0] + _t * DELTA * math.cos(_a), QPT[1] + _t * DELTA * math.sin(_a))
  assert _d2(_x, PCEN) < RAD, "the smaller ball is not inside the bigger one"

# the distance function is Lipschitz with constant one, and one is attained
RATIOS = []
for _k in range(200):
 _a, _b = 2 * math.pi * _k / 200, 2 * math.pi * (_k + 37) / 200
 _x = (1.3 * math.cos(_a), 1.3 * math.sin(_a))
 _y = (0.7 * math.cos(_b), 0.7 * math.sin(_b))
 RATIOS.append(abs(_d2(PCEN, _x) - _d2(PCEN, _y)) / _d2(_x, _y))
assert max(RATIOS) <= 1.0 + 1e-12, "the Lipschitz constant is not one"
COLLINEAR = abs(_d2(PCEN, (2.0, 0.0)) - _d2(PCEN, (0.5, 0.0))) / _d2((2.0, 0.0), (0.5, 0.0))
assert abs(COLLINEAR - 1.0) < 1e-12, "one has to be attained, or the constant is not sharp"


# ── beat 8: forward images do not stay closed ──────────────────────────
def _fair(x):
 return 2 * x / (1 + x * x)


IMG = [(n, _fair(n)) for n in (1, 2, 3, 5, 10, 100)]
for _n, _v in IMG:
 assert _v > 0.0, "no member of the image is zero"
assert IMG[-1][1] < 0.03, "yet the image creeps arbitrarily close to zero"
assert abs(IMG[0][1] - 1.0) < 1e-12, "the range's endpoint is attained at one"
ARCTAN = [(x, math.atan(x)) for x in (1.0, 10.0, 1000.0)]
assert all(v < math.pi / 2 for _, v in ARCTAN) and ARCTAN[-1][1] > math.pi / 2 - 1e-3, \
    "the arctangent approaches its bound without reaching it"


# ── beat 9: disjoint closed sets at distance zero ──────────────────────
GAPS = [(x, 1.0 / x) for x in (1.0, 3.0, 10.0, 100.0)]
assert all(g > 0 for _, g in GAPS), "every point of the graph is off the axis"
assert GAPS[-1][1] < 0.02, "yet the distance between the two sets is zero"


# ── beat 10: Lemma 1.5, and why it cannot be improved ──────────────────
def _ramp_dist(k):
 """rho(alpha_k, N) for the continuous ramp approximating the indicator of [0,1].

 N is the closed subspace of functions with vanishing integral over [0, 1], so
 the distance is the component along that indicator, divided by the norm.
 """
 num = 1.0 - 1.0 / (2 * k)
 den = math.sqrt(1.0 - 2.0 / (3 * k))
 return num / den


RAMP = [(k, _ramp_dist(k)) for k in (1, 4, 20, 100)]
for _a, _b in zip(RAMP, RAMP[1:]):
 assert _a[1] < _b[1], "the distance has to climb"
for _k, _v in RAMP:
 assert _v < 1.0, "and it must never reach one, which is the whole point"
assert RAMP[-1][1] > 0.99, "it does get within a hundredth of one"


class AdvCalcE56Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 56

 MODE_LABEL = {
  0: {"zh": "抽出來只剩三條", "en": "what is left is three axioms"},
  1: {"zh": "任何子集也是一個度量空間", "en": "any subset is one too"},
  2: {"zh": "不是每個度量都來自範數", "en": "not every metric comes from a norm"},
  3: {"zh": "球是開的", "en": "a ball is open"},
  4: {"zh": "開集族的三條性質", "en": "three properties of the open sets"},
  5: {"zh": "內部、閉包、邊界", "en": "interior, closure, boundary"},
  6: {"zh": "隨手一個集合通常兩者都不是", "en": "a random set is usually neither"},
  7: {"zh": "連續：逆像保持開與閉", "en": "continuity: inverse images behave"},
  8: {"zh": "可是正像不保持", "en": "forward images do not"},
  9: {"zh": "不相交也可以距離為零", "en": "disjoint can still mean distance zero"},
  10: {"zh": "引理 1.5，以及它為什麼改不好", "en": "Lemma 1.5, and why it cannot improve"},
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

 def _dcirc(self, cx, cy, r, col, sw=1.8, n=40):
  g = VGroup()
  for k in range(n):
   if k % 2:
    continue
   a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
   g.add(self._curve([[cx + r * math.cos(a0 + (a1 - a0) * j / 4),
                       cy + r * math.sin(a0 + (a1 - a0) * j / 4), 0] for j in range(5)],
                     col, sw=sw))
  return g

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _axioms(self):
  cx, cy = -4.55, 0.10
  pts = ((-1.10, -0.55), (1.05, -0.45), (0.05, 0.70))
  g = VGroup()
  for k in range(3):
   a, b = pts[k], pts[(k + 1) % 3]
   g.add(Line([cx + a[0], cy + a[1], 0], [cx + b[0], cy + b[1], 0],
              color=(ACCENT_B, ACCENT_C, WARN)[k], stroke_width=2.6))
  for k, (dx, dy) in enumerate(pts):
   g.add(Dot([cx + dx, cy + dy, 0], radius=0.07, color=ACCENT_A),
         self._sym(cy + dy + (0.30 if dy > 0 else -0.30), ("x", "y", "z")[k], ACCENT_A,
                   FS_TAG, x=cx + dx, w=0.60))
  g.add(self._panel(((0.86, "不同的兩點，距離為正",
                      "distinct points are a positive distance apart", ACCENT_B),
                     (0.20, "距離是對稱的",
                      "the distance is symmetric", ACCENT_C),
                     (-0.46, "而且滿足三角不等式",
                      "and it satisfies the triangle inequality", WARN))))
  return g.add(self._foot("前面三章談收斂與連續時，其實只用到「兩點之間的距離」這一件事",
                          "everything the last three chapters did with convergence used only the distance between two points",
                          ACCENT_A,
                          "把它抽出來就是這三條；一個集合配上這樣一個函數，就叫度量空間",
                          "distilled, that is these three; a set with such a function is a metric space"))

 def _subset(self):
  g = VGroup(self._rect(-4.35, 0.05, 1.65, 0.95, DIM, sw=1.4))
  pts = [(-1.20, -0.60), (-0.75, 0.10), (-0.30, 0.62), (0.35, -0.35),
         (0.90, 0.45), (1.25, -0.70), (0.05, 0.05), (-1.05, 0.70)]
  for dx, dy in pts:
   g.add(Dot([-4.35 + dx, 0.05 + dy, 0], radius=0.065, color=WARN))
  g.add(self._panel(((0.86, "灰框是一個賦範空間，用範數當距離",
                      "the grey frame is a normed space under the norm distance", DIM),
                     (0.20, "紅點是它的一個子集，限制過去仍然是度量空間",
                      "the red points are a subset, still a metric space", WARN),
                     (-0.46, "而這樣的空間可以非常古怪",
                      "and such a space can be very odd indeed", ACCENT_A))))
  return g.add(self._foot("從 ℝⁿ 這種漂亮的空間裡挖一個奇怪的子集出來，幾乎任何你想得到的性質它都可能沒有",
                          "carve a weird subset out of a nice space and it may fail almost any property you can think of",
                          ACCENT_A,
                          "這正是要把論證搬到度量空間去做的理由：不能再靠向量運算",
                          "which is why the arguments move to metric spaces: the vector operations are no longer available"))

 def _greatcircle(self):
  cx, cy, r = -4.25, 0.05, 1.05
  g = VGroup(self._circ(cx, cy, r, ACCENT_C, sw=2.2))
  for f in (0.42, -0.42):
   g.add(self._curve([[cx + r * math.sqrt(max(0.0, 1 - f * f)) * math.cos(2 * math.pi * k / 60),
                       cy + f * r + 0.30 * r * math.sin(2 * math.pi * k / 60), 0]
                      for k in range(61)], DIM, sw=1.2))
  a0, a1 = 2.35, 0.55
  p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
  p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
  g.add(self._curve([[cx + r * math.cos(a0 + (a1 - a0) * k / 40),
                      cy + r * math.sin(a0 + (a1 - a0) * k / 40), 0] for k in range(41)],
                    WARN, sw=3.2))
  g.add(self._dash([p0[0], p0[1], 0], [p1[0], p1[1], 0], DIM, n=10, sw=1.6),
        Dot([p0[0], p0[1], 0], radius=0.07, color=ACCENT_A),
        Dot([p1[0], p1[1], 0], radius=0.07, color=ACCENT_A))
  g.add(self._panel(((0.86, "紅色是球面上的大圓弧長",
                      "red is the great-circle arc along the surface", WARN),
                     (0.20, "灰虛線是空間裡的直線距離",
                      "the dashed grey line is the straight distance in space", DIM),
                     (-0.46, "紅色那個才是這個度量空間的距離",
                      "the red one is the metric of this space", ACCENT_A))))
  return g.add(self._foot("程式把 729 組三元組都試過，大圓距離的三角不等式一次都沒有壞",
                          "all 729 triples were tried here and the triangle inequality never failed for the great-circle distance",
                          ACCENT_A,
                          "更一般地，任何光滑曲面上可以取「曲面內最短曲線的長度」——都不是範數給的",
                          "more generally any smooth surface can use the shortest curve inside it, and none of these come from a norm"))

 def _ballopen(self):
  cx, cy = -4.15, 0.05
  g = VGroup(self._circ(cx, cy, 1.15, ACCENT_B, sw=2.4))
  qx, qy = cx + 1.15 * QPT[0], cy + 1.15 * QPT[1]
  g.add(Dot([cx, cy, 0], radius=0.06, color=DIM),
        Dot([qx, qy, 0], radius=0.07, color=WARN),
        self._circ(qx, qy, 1.15 * DELTA, WARN, sw=2.0))
  g.add(self._arr([cx, cy, 0], [qx, qy, 0], DIM, sw=1.6, tl=0.10))
  g.add(self._sym(0.86, f"δ   =   r   −   ρ ( p , q )", WARN, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "q 是大球裡的任何一點", "q is any point of the big ball",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "那個半徑的小球整個落在大球裡",
                  "the small ball of that radius lies entirely inside", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以每個球都是開的，證明就是三角不等式",
                  "so every ball is open, and the proof is the triangle inequality", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("程式在小球邊界上取 720 個點都驗過，每一個到大球中心的距離都小於 r",
                          "720 points on the small circle were checked here, every one nearer the centre than r",
                          ACCENT_A,
                          "引理 1.2 說「到定點的距離」是 Lipschitz 常數 1 的函數，而 1 是取得到的",
                          "Lemma 1.2 says distance to a fixed point is Lipschitz with constant one, and one is attained"))

 def _topology(self):
  g = VGroup()
  for k, (cx, lab) in enumerate(((-5.15, "∪"), (-2.95, "∩"), (-0.75, "∅ , X"))):
   if k == 0:
    g.add(self._circ(cx - 0.32, 0.30, 0.52, ACCENT_B, sw=2.0),
          self._circ(cx + 0.32, 0.30, 0.52, ACCENT_C, sw=2.0),
          self._circ(cx, -0.05, 0.44, WARN, sw=2.0))
   elif k == 1:
    g.add(self._circ(cx - 0.30, 0.20, 0.62, ACCENT_B, sw=2.0),
          self._circ(cx + 0.30, 0.20, 0.62, ACCENT_C, sw=2.0),
          self._circ(cx, 0.20, 0.22, WARN, sw=2.6))
   else:
    g.add(self._rect(cx, 0.20, 0.72, 0.55, ACCENT_B, sw=2.0),
          Dot([cx, 0.20, 0], radius=0.07, color=WARN))
   g.add(self._sym(-0.86, lab, DIM, FS_TAG + 1, x=cx, w=1.60))
  g.add(self._panel(((0.86, "任意多個開集的聯集是開的",
                      "arbitrary unions of open sets are open", ACCENT_B),
                     (0.20, "兩個開集的交是開的",
                      "the intersection of two of them is open", ACCENT_C),
                     (-0.46, "空集與全空間都是開的",
                      "and the empty set and the whole space are open", WARN))))
  return g.add(self._foot("推論很好記：一個集合是開的，等價於它是一堆開球的聯集",
                          "the corollary is easy to remember: a set is open exactly when it is a union of open balls",
                          ACCENT_A,
                          "注意第二條只說「兩個」——無窮多個開集的交不一定是開的，那是習題 1.4",
                          "note the second says two: an intersection of infinitely many need not be open, which is exercise 1.4"))

 def _closure(self):
  cx, cy = -4.15, 0.05
  g = VGroup(self._blob(cx, cy, 1.25, 0.80, 0.14, WARN, sw=2.6))
  g.add(self._blob(cx, cy, 1.05, 0.62, 0.11, ACCENT_B, sw=1.6))
  g.add(Dot([cx - 0.30, cy + 0.10, 0], radius=0.06, color=ACCENT_B))
  g.add(self._sym(0.86, "∂ A    =    Ā    −    A ⁱⁿᵗ", ACCENT_A, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "藍色裡面：內部，最大的開子集",
                  "inside the blue: the interior, the largest open subset", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "紅色外框：閉包，最小的閉超集",
                  "the red outline: the closure, the smallest closed superset", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "兩者之間那一圈：邊界",
                  "the ring between them: the boundary", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這一整組定義都是互補的：閉集就是補集為開的集合，其餘用 De Morgan 律翻過去",
                          "the whole set of definitions is complementary: closed means the complement is open, and De Morgan does the rest",
                          ACCENT_A,
                          "一點落在閉包裡，等價於它周圍每一個球都跟那個集合相交",
                          "a point lies in the closure exactly when every ball about it meets the set"))

 def _neither(self):
  cx, cy, r = -4.15, 0.05, 1.05
  g = VGroup(self._dcirc(cx, cy, r, DIM, sw=1.6))
  g.add(self._curve([[cx + r * math.cos(0.4 + 2.2 * k / 40),
                      cy + r * math.sin(0.4 + 2.2 * k / 40), 0] for k in range(41)],
                    WARN, sw=3.2))
  g.add(Dot([cx - 0.25, cy - 0.15, 0], radius=0.055, color=ACCENT_B))
  g.add(self._panel(((0.86, "開球，加上邊界的一部分",
                      "an open ball, plus part of its boundary", WARN),
                     (0.20, "不是開的：紅色那段上的點沒有球含在裡面",
                      "not open: no ball about a red point stays inside", ACCENT_C),
                     (-0.46, "也不是閉的：灰色那段的點在閉包裡卻不在集合裡",
                      "not closed: the grey arc lies in the closure but not in the set", DIM))))
  return g.add(self._foot("書上直說：隨手拿一個集合，它通常既不開也不閉",
                          "the book says it outright: a set picked at random is generally neither open nor closed",
                          ACCENT_A,
                          "「開」與「閉」不是互斥的，也不是窮盡的——空集與全空間兩者都是",
                          "open and closed are neither exclusive nor exhaustive: the empty set and the whole space are both"))

 def _inverse(self):
  g = VGroup()
  for cx, lab, col in ((-4.90, "X", ACCENT_B), (-1.90, "Y", WARN)):
   g.add(self._blob(cx, 0.10, 1.15, 0.72, 0.12, DIM, sw=1.8),
         self._sym(1.02, lab, col, FS_TAG, x=cx, w=0.70))
  g.add(self._circ(-5.05, 0.05, 0.46, ACCENT_B, sw=2.2),
        self._circ(-2.05, 0.05, 0.40, WARN, sw=2.2))
  g.add(self._arr([-3.75, 0.34, 0], [-3.25, 0.34, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.25, -0.24, 0], [-3.75, -0.24, 0], ACCENT_C, sw=2.5, tl=0.12))
  g.add(self._sym(0.60, "f", ACCENT_A, FS_TAG, x=-3.50, w=0.60),
        self._sym(-0.54, "f ⁻¹", ACCENT_C, FS_TAG - 1, x=-3.50, w=1.10))
  g.add(self._panel(((0.86, "右邊那個是開的",
                      "the one on the right is open", WARN),
                     (0.20, "它的逆像也是開的",
                      "and so is its inverse image", ACCENT_B),
                     (-0.46, "閉集也一樣，而且兩個的反面都成立",
                      "the same holds for closed sets, and both converses too", ACCENT_C))))
  return g.add(self._foot("因為反面也成立，這句話可以拿來當「連續」的定義——下一集第 2 節就會這樣做",
                          "since the converses hold, this can serve as the definition of continuity, which is what section 2 does",
                          ACCENT_A,
                          "一個立刻的應用：球、閉球、球面分別是「到定點的距離」在三個集合上的逆像",
                          "one immediate use: the ball, closed ball and sphere are inverse images under the distance to a fixed point"))

 def _forward(self):
  ox, oy = -5.95, -0.35
  sx, sy = 2.30, 0.62
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.10, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.72, 0], [ox, oy + 0.86, 0], color=DIM, stroke_width=1.4))
  g.add(self._curve([[ox + sx * (k / 60.0), oy + sy * math.atan(4.0 * (k / 60.0)), 0]
                     for k in range(61)], ACCENT_B, sw=2.6))
  g.add(self._dash([ox, oy + sy * math.pi / 2, 0], [ox + sx * 1.10, oy + sy * math.pi / 2, 0],
                   WARN, n=16, sw=1.4))
  rows = [("        n            2 n / ( 1 + n ² )", DIM)]
  for n, v in IMG[:1] + IMG[4:]:
   rows.append((f"      {n:4d}                {v:.5f}", ACCENT_C))
  g.add(self._table(rows, x=PANEL_X, w=PANEL_W, y0=0.80, dy=0.34))
  g.add(self._mid(-0.72, "零在像的閉包裡，可是不在像裡",
                  "zero lies in the closure of the image but not in it", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("左邊是反正切：像是一個開區間，那條紅虛線永遠碰不到",
                          "on the left the arctangent, whose image is an open interval never reaching the dashed line",
                          ACCENT_A,
                          "右邊是比較公平的那個例子：值域是閉區間，可是正整數這個閉集的像不閉",
                          "on the right the fairer example: the range is closed, yet the image of a closed set is not"))

 def _setdistance(self):
  ox, oy = -5.95, -0.45
  sx, sy = 2.20, 0.52
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.60, oy, 0], color=ACCENT_B, stroke_width=2.6),
             Line([ox, oy - 0.20, 0], [ox, oy + 1.30, 0], color=DIM, stroke_width=1.4))
  g.add(self._curve([[ox + sx * (0.30 + 1.25 * k / 60.0),
                      oy + sy / (0.30 + 1.25 * k / 60.0), 0] for k in range(61)],
                    WARN, sw=2.6))
  for x, gap in GAPS[:3]:
   px = ox + sx * (x / 3.0)
   if px < ox + sx * 1.55:
    g.add(self._dash([px, oy, 0], [px, oy + sy * gap, 0], DIM, n=4, sw=1.2))
  g.add(self._sym(0.86, "ρ ( A , B )   =   glb  { ρ ( a , b ) }", ACCENT_A, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "兩個集合不相交", "the two sets are disjoint", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "兩個都是閉的", "and both of them are closed", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "可是它們之間的距離是零",
                  "yet the distance between them is zero", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("縫隙隨著往右走一路縮小：程式在 x 等於 100 時算出來只剩 0.01",
                          "the gap shrinks all the way along: at x equal to a hundred it is down to a hundredth",
                          ACCENT_A,
                          "另一個例子更簡單：圓的內部與外部是兩個不相交的開集，距離也是零",
                          "a simpler example: the inside and outside of a circle are disjoint open sets at distance zero"))

 def _lemma15(self):
  ox, oy = -5.75, -0.55
  sx, sy = 4.10, 1.55
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.12, 0], [ox, oy + sy * 1.16, 0], color=DIM, stroke_width=1.4))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * 1.06, oy + sy, 0], WARN, n=22, sw=1.6))
  pts = [[ox + sx * min(1.0, math.log(k) / math.log(120.0)), oy + sy * _ramp_dist(k), 0]
         for k in range(1, 101)]
  g.add(self._curve(pts, ACCENT_B, sw=2.8))
  for k, v in RAMP:
   px = ox + sx * min(1.0, math.log(max(k, 1.0001)) / math.log(120.0))
   g.add(Dot([px, oy + sy * v, 0], radius=0.06, color=ACCENT_C))
  rows = [("        k              ρ ( α ₖ , N )", DIM)]
  for k, v in RAMP:
   rows.append((f"      {k:4d}                {v:.6f}", ACCENT_C))
  g.add(self._table(rows, x=PANEL_X, w=PANEL_W, y0=0.84, dy=0.32))
  g.add(self._mid(-0.86, "一路往上，可是永遠到不了一",
                  "climbing all the way, and never reaching one", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理只說「大於一減 ε」。想改成「等於一」就要取 N 裡最近的點——而最近的點可能不存在",
                          "the lemma only promises more than one minus epsilon; improving it needs a nearest point in N, which may not exist",
                          ACCENT_A,
                          "有限維時一定取得到，Hilbert 空間也取得到；書上那個反例兩者都不是",
                          "in finite dimensions and in a Hilbert space it always exists; the book's counterexample is neither"))

 def stage(self):
  a, b, c = self._axioms(), self._subset(), self._greatcircle()
  d, e, f = self._ballopen(), self._topology(), self._closure()
  h, i, j = self._neither(), self._inverse(), self._forward()
  k, l = self._setdistance(), self._lemma15()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE56ZH, AdvCalcE56EN = make(AdvCalcE56Base, "56", prefix="AdvCalcE")
