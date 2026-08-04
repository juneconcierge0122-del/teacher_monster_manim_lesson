"""advcalc E06 — Chapter 1, section 1, second half (book pp. 26-29): unordered
sums, linear combinations, Theorem 1.1 and the linear span.

The section's one real theorem says the linear span is the smallest subspace
including A, so the beats build toward a picture of that nesting (beat 7) and
then justify it. The two places where the picture has to do work the formula
bar cannot: beat 0, where the point is that many different bracketings land on
one endpoint, and beat 2, where the monomials of a two-variable polynomial are
displayed as a staircase precisely because that index set has no natural order.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE06Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 6

 MODE_LABEL = {
  0: {"zh": "十二種算法，同一個終點", "en": "twelve ways, one endpoint"},
  1: {"zh": "只要寫出指標集就沒有歧義", "en": "the index set alone makes it unambiguous"},
  2: {"zh": "有次序的指標，與沒有次序的", "en": "ordered index sets, and unordered ones"},
  3: {"zh": "兩種分法交出四小塊", "en": "two splittings intersect into four pieces"},
  4: {"zh": "線性組合", "en": "a linear combination"},
  5: {"zh": "係數就是那個元組", "en": "the coefficients are the tuple"},
  6: {"zh": "兩個向量的所有線性組合", "en": "all linear combinations of two vectors"},
  7: {"zh": "包含 A 的最小子空間", "en": "the smallest subspace including A"},
  8: {"zh": "相加、數乘，都還在裡面", "en": "closed under adding and under scaling"},
  9: {"zh": "A 無限也不影響", "en": "an infinite A changes nothing"},
  10: {"zh": "生成、有限維", "en": "spanning, and finite dimension"},
 }

 # ── beat 0: the bracketings all land together ─────────────────────
 V3 = (np.array([1.35, 0.72, 0.0]), np.array([1.10, -0.68, 0.0]), np.array([0.95, 0.95, 0.0]))

 def _twelve(self):
  """Three orderings drawn as three staircases from O to the same corner.
  Slightly offset so all three read, but they finish on one dot."""
  o = np.array([-3.55, -0.55, 0.0])
  end = o + sum(self.V3)
  orders = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
  cols = (ACCENT_B, ACCENT_C, ACCENT_A)
  offs = (0.16, 0.0, -0.16)
  g = VGroup()
  for (order, col, dy) in zip(orders, cols, offs):
   p = o + np.array([0.0, dy, 0.0])
   for k in order:
    q = p + self.V3[k]
    g.add(self._arr(p, q, col, sw=2.6, tl=0.13))
    p = q
  g.add(Dot(o, radius=0.075, color=INK), Dot(end, radius=0.10, color=WARN),
        Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.26, -0.22, 0])),
        Text("12", font_size=FS_TAG + 12, color=WARN).move_to([2.55, 0.72, 0]))
  return g.add(self._mid(0.05, "換順序、換分組", "reorder it, regroup it",
                         DIM, FS_TAG, x=2.90, w=4.6),
               self._mid(-0.60, "終點永遠是同一個", "the endpoint never moves",
                         WARN, FS_TAG, x=2.90, w=4.6),
               self._mid(-1.55, "所以有限集合的和，跟怎麼加完全無關",
                         "so the sum of a finite set does not depend on how it is added",
                         DIM, FS_TAG, w=11.6))

 def _bag(self):
  """An unordered heap of vectors with one sum coming out: the notation only
  has to name the index set."""
  cx, cy = -3.35, 0.10
  g = VGroup(Ellipse(width=3.90, height=2.35, color=DIM, stroke_width=2.5).move_to([cx, cy, 0]))
  # Laid out on a jittered ring rather than at random: six arrows drawn from
  # uniform points cluster in the middle and their index labels overlap.
  rng = np.random.default_rng(11)
  for k in range(6):
   a = 2 * np.pi * k / 6 + rng.uniform(-0.26, 0.26)
   base = np.array([cx + 1.05 * np.cos(a), cy + 0.62 * np.sin(a), 0.0])
   d = 0.52 * np.array([np.cos(a + 1.9), np.sin(a + 1.9), 0.0])
   g.add(self._arr(base - 0.5 * d, base + 0.5 * d, ACCENT_B, sw=2.4, tl=0.11),
         Text(f"i{k + 1}", font_size=FS_TAG - 4, color=DIM)
         .move_to(base + np.array([0.0, 0.30, 0])))
  g.add(self._arr([cx + 2.10, cy, 0], [0.55, cy, 0], ACCENT_A, sw=3, tl=0.15),
        Rectangle(width=1.35, height=0.78, color=ACCENT_A, stroke_width=2.5)
        .move_to([1.35, cy, 0]),
        Text("Σ", font_size=FS_TAG + 10, color=ACCENT_A).move_to([1.35, cy, 0]))
  return g.add(self._mid(0.95, "沒有次序也沒關係", "no order needed",
                         DIM, FS_TAG, x=4.35, w=3.5),
               self._mid(0.15, "只要指標集是有限的", "only that the index set is finite",
                         ACCENT_A, FS_TAG, x=4.35, w=3.5),
               self._mid(-1.55, "任何有限的加了指標的向量集合，都唯一決定一個和",
                         "any finite indexed set of vectors determines a unique sum",
                         DIM, FS_TAG, w=11.6))

 def _index_sets(self):
  """Left: a block of integers, in order. Right: the monomials of a
  two-variable polynomial of degree at most five, which is the book's example
  of an index set with no natural order at all."""
  g = VGroup()
  ox = -4.25
  for k in range(5):
   x = ox + k * 0.72
   g.add(Rectangle(width=0.56, height=0.56, color=ACCENT_B, stroke_width=2)
         .move_to([x, 0.55, 0]),
         Text(str(k + 1), font_size=FS_TAG, color=ACCENT_B).move_to([x, 0.55, 0]))
   if k < 4:
    g.add(self._arr([x + 0.30, 0.55, 0], [x + 0.42, 0.55, 0], GHOST, sw=1.8, tl=0.08))
  g.add(self._mid(-0.35, "一到 n：照自然順序", "one to n: the natural order",
                  ACCENT_B, FS_TAG, x=ox + 1.44, w=4.2))
  # No axes on the staircase: drawn to the top of the triangle they overshoot
  # into the formula bar, and the axis labels then collide with the caption.
  # The staircase alone already says the index set has no order.
  bx, by, s = 2.60, -0.85, 0.30
  for i in range(6):
   for j in range(6 - i):
    g.add(Dot([bx + i * s, by + j * s, 0], radius=0.070, color=ACCENT_C))
  g.add(Text("sⁱ tʲ", font_size=FS_TAG - 2, color=DIM).move_to([bx + 3.4 * s, by + 3.0 * s, 0]))
  return g.add(self._mid(1.05, "次數不超過五的單項式", "the monomials of degree at most five",
                         ACCENT_C, FS_TAG, x=3.35, w=4.0),
               self._mid(-1.62, "右邊這個指標集根本沒有自然的次序",
                         "that index set on the right has no natural order at all",
                         ACCENT_C, FS_TAG, w=11.6))

 def _induction(self):
  """The starred proof: each computation's last addition splits I in two, and
  intersecting the two splittings gives the four blocks that regroup."""
  ox, oy, w, h = -2.05, -0.20, 3.20, 1.90
  g = VGroup(Rectangle(width=w, height=h, color=DIM, stroke_width=2.5).move_to([ox, oy, 0]),
             Line([ox, oy - h / 2, 0], [ox, oy + h / 2, 0], color=ACCENT_B, stroke_width=3),
             Line([ox - w / 2, oy, 0], [ox + w / 2, oy, 0], color=ACCENT_C, stroke_width=3))
  names = (("L₁₁", -1, 1), ("L₁₂", 1, 1), ("L₂₁", -1, -1), ("L₂₂", 1, -1))
  for s, sx, sy in names:
   g.add(Text(s, font_size=FS_TAG, color=ACCENT_A)
         .move_to([ox + sx * w / 4, oy + sy * h / 4, 0]))
  g.add(Text("J₁", font_size=FS_TAG - 2, color=ACCENT_B).move_to([ox - w / 4, oy + h / 2 + 0.26, 0]),
        Text("J₂", font_size=FS_TAG - 2, color=ACCENT_B).move_to([ox + w / 4, oy + h / 2 + 0.26, 0]),
        Text("K₁", font_size=FS_TAG - 2, color=ACCENT_C).move_to([ox - w / 2 - 0.34, oy + h / 4, 0]),
        Text("K₂", font_size=FS_TAG - 2, color=ACCENT_C).move_to([ox - w / 2 - 0.34, oy - h / 4, 0]))
  return g.add(self._mid(0.95, "一種算法把 I 切成兩塊", "one computation splits I in two",
                         ACCENT_B, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "另一種算法切成另外兩塊", "the other splits it differently",
                         ACCENT_C, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.45, "交出來的四小塊可以重新結合",
                         "the four blocks can be regrouped", ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.55, "書上把這個形式證明標了星號，只給有興趣的讀者",
                         "the book stars this proof and gives it only for the interested reader",
                         DIM, FS_TAG, w=11.6))

 # ── linear combinations ───────────────────────────────────────────
 def _combination(self):
  """Two vectors, scaled by their coefficients, added tip to tail."""
  o = np.array([-2.85, -1.20, 0.0])
  u, v = np.array([1.25, 0.42, 0.0]), np.array([0.52, 1.05, 0.0])
  xu, xv = 1.7, 1.15
  g = VGroup(self._arr(o, o + u, ACCENT_B, sw=2.5, tl=0.12),
             self._arr(o, o + v, ACCENT_C, sw=2.5, tl=0.12),
             self._arr(o, o + xu * u, ACCENT_B, sw=4, tl=0.18),
             self._arr(o + xu * u, o + xu * u + xv * v, ACCENT_C, sw=4, tl=0.18),
             self._arr(o, o + xu * u + xv * v, ACCENT_A, sw=5, tl=0.22),
             Dot(o, radius=0.06, color=INK),
             Text("α₁", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + u + np.array([0.08, -0.28, 0])),
             Text("α₂", font_size=FS_TAG - 2, color=ACCENT_C)
             .move_to(o + v + np.array([-0.30, 0.10, 0])))
  return g.add(self._mid(0.95, "每個向量先乘上自己的純量",
                         "each vector scaled by its own scalar",
                         DIM, FS_TAG, x=3.10, w=5.6),
               self._mid(0.25, "純量是任意的", "the scalars are arbitrary",
                         DIM, FS_TAG, x=3.10, w=5.6),
               self._mid(-0.45, "加起來就是一個線性組合",
                         "the sum is a linear combination", ACCENT_A, FS_TAG, x=3.10, w=5.6),
               self._mid(-1.55, "只要求是有限個相加",
                         "the only requirement is that the sum be finite",
                         DIM, FS_TAG, w=11.4))

 def _functions(self):
  """The book's own example: sine, cosine and the exponential, and the
  combination whose coefficient triple is three, zero, minus one."""
  ax, w, base = -0.55, 6.60, 0.05
  ts = np.linspace(-1, 1, 90)
  def cur(fn, col, sw=3):
   return self._curve([[ax + t * w / 2, base + 0.26 * fn(2.4 * t), 0] for t in ts], col, sw=sw)
  g = VGroup(Line([ax - w / 2, base, 0], [ax + w / 2, base, 0], color=GHOST, stroke_width=2),
             cur(np.sin, ACCENT_B), cur(np.cos, ACCENT_C),
             cur(lambda z: np.exp(z * 0.55), DIM),
             cur(lambda z: 3 * np.sin(z) - np.exp(z * 0.55), ACCENT_A, sw=4.5))
  # The legend sits over the span of the curves, not off to one side, so each
  # word lands above the curve it names.
  for k, (zh, en, col) in enumerate((("正弦", "sine", ACCENT_B), ("餘弦", "cosine", ACCENT_C),
                                     ("指數", "exponential", DIM))):
   g.add(self._mid(1.10, zh, en, col, FS_TAG - 2, x=-2.60 + k * 2.30, w=2.0))
  return g.add(self._mid(-1.35, "三倍正弦，減掉指數", "three sine, minus the exponential",
                         ACCENT_A, FS_TAG, x=0.0, w=6.0),
               self._mid(-1.72, "照這個順序排，係數三元組就是三、零、負一",
                         "in that listed order the coefficient triple is three, zero, minus one",
                         DIM, FS_TAG, w=11.6))

 def _span(self):
  """The linear span of two vectors in three-space is the plane they lie in,
  and every combination lands back on that plane."""
  org = np.array([-2.10, -0.30, 0.0])
  s = 0.92
  quad = [_p(v, org, s) for v in ((-1.8, -1.5, 0), (1.8, -1.5, 0), (1.8, 1.5, 0), (-1.8, 1.5, 0))]
  u, v = np.array([1.25, -0.85, 0]), np.array([0.30, 1.25, 0])
  o3 = _p(np.zeros(3), org, s)
  g = VGroup(Polygon(*quad, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.13),
             self._arr(o3, _p(u, org, s), ACCENT_C, sw=3.5, tl=0.16),
             self._arr(o3, _p(v, org, s), ACCENT_C, sw=3.5, tl=0.16),
             Dot(o3, radius=0.06, color=INK))
  # Every coefficient pair here is checked against the drawn quad, which spans
  # [-1.8, 1.8] x [-1.5, 1.5] in plane coordinates. A combination rendered
  # outside the plane would contradict the caption underneath it.
  combos = ((0.7, 0.4), (-0.5, 0.6), (0.3, -0.7))
  for (a, b) in combos:
   w = a * u + b * v
   assert abs(w[0]) <= 1.8 and abs(w[1]) <= 1.5, (a, b, w)
   g.add(Dot(_p(w, org, s), radius=0.07, color=ACCENT_A))
  g.add(self._arr(o3, _p(combos[0][0] * u + combos[0][1] * v, org, s), ACCENT_A, sw=4, tl=0.18),
        Text("L", font_size=FS_TAG + 2, color=ACCENT_B)
        .move_to(_p(np.array([-1.45, 1.15, 0]), org, s)))
  return g.add(self._mid(0.95, "所有線性組合所成的集合", "the set of all linear combinations",
                         DIM, FS_TAG, x=3.35, w=5.3),
               self._mid(0.25, "對加法與數乘封閉", "closed under adding and scaling",
                         ACCENT_A, FS_TAG, x=3.35, w=5.3),
               self._mid(-0.45, "所以它是一個子空間", "so it is a subspace",
                         ACCENT_B, FS_TAG, x=3.35, w=5.3),
               self._mid(-1.55, "而且任何含有那兩個向量的子空間，一定也含有它",
                         "and any subspace containing the two vectors must include it",
                         DIM, FS_TAG, w=11.6))

 def _nesting(self):
  """Theorem 1.1 as nested regions -- the one claim the formula bar states but
  cannot show: L(A) is squeezed between A and every subspace containing A."""
  cx, cy = -2.30, 0.0
  g = VGroup(Ellipse(width=5.40, height=2.45, color=DIM, stroke_width=2.5).move_to([cx, cy, 0]),
             Ellipse(width=3.60, height=1.90, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.10).move_to([cx - 0.24, cy, 0]),
             Ellipse(width=2.20, height=1.30, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.12).move_to([cx - 0.52, cy, 0]))
  rng = np.random.default_rng(7)
  for _ in range(7):
   a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0, 0.68)
   g.add(Dot([cx - 0.52 + r * np.cos(a) * 1.00, cy + r * np.sin(a) * 0.56, 0],
             radius=0.055, color=WARN))
  g.add(Text("A", font_size=FS_TAG, color=WARN).move_to([cx - 0.52, cy + 0.80, 0]),
        Text("L ( A )", font_size=FS_TAG, color=ACCENT_B).move_to([cx - 0.30, cy + 1.06, 0]),
        Text("M", font_size=FS_TAG, color=DIM).move_to([cx + 2.10, cy + 0.86, 0]))
  return g.add(self._mid(0.85, "A 的所有線性組合", "all linear combinations of A",
                         ACCENT_B, FS_TAG, x=3.55, w=4.9),
               self._mid(0.15, "是一個子空間", "form a subspace", DIM, FS_TAG, x=3.55, w=4.9),
               self._mid(-0.55, "而且是包含 A 的最小的那個",
                         "and it is the smallest one including A",
                         ACCENT_A, FS_TAG, x=3.55, w=4.9),
               self._mid(-1.55, "任何含有 A 的子空間 M，都得把整個 L ( A ) 裝進去",
                         "any subspace M including A has to contain the whole of L of A",
                         DIM, FS_TAG, w=11.6))

 def _closure(self):
  """The proof's first half, done on the coefficients: add two combinations
  and the like terms merge index by index."""
  ox = -3.05
  rows = ((0.70, ("x₁", "x₂", "x₃"), ACCENT_B), (0.10, ("y₁", "y₂", "y₃"), ACCENT_C))
  g = VGroup()
  for y, coeffs, col in rows:
   for k, c in enumerate(coeffs):
    g.add(Rectangle(width=0.78, height=0.48, color=col, stroke_width=2)
          .move_to([ox + k * 0.92, y, 0]),
          Text(c, font_size=FS_TAG - 2, color=col).move_to([ox + k * 0.92, y, 0]))
  g.add(Text("+", font_size=FS_TAG + 4, color=DIM).move_to([ox - 0.72, 0.40, 0]))
  for k, c in enumerate(("x₁+y₁", "x₂+y₂", "x₃+y₃")):
   g.add(Rectangle(width=1.15, height=0.48, color=ACCENT_A, stroke_width=2.5)
         .move_to([ox + k * 1.28, -0.82, 0]),
         Text(c, font_size=FS_TAG - 4, color=ACCENT_A).move_to([ox + k * 1.28, -0.82, 0]),
         self._dash([ox + k * 0.92, -0.18, 0], [ox + k * 1.28, -0.56, 0], GHOST, n=5))
  return g.add(self._mid(0.75, "兩個線性組合相加", "add two linear combinations",
                         DIM, FS_TAG, x=2.95, w=5.6),
               self._mid(0.05, "按指標合併同類項", "collect terms index by index",
                         ACCENT_A, FS_TAG, x=2.95, w=5.6),
               self._mid(-0.65, "還是一個線性組合", "and it is one again",
                         ACCENT_B, FS_TAG, x=2.95, w=5.6),
               self._mid(-1.55, "乘上一個純量也一樣，用分配律與歸納法",
                         "scaling is the same, by distributivity and induction",
                         DIM, FS_TAG, w=11.4))

 def _infinite(self):
  """An infinite A, with two finite selections whose union is still finite."""
  cx, cy = -2.55, -0.15
  g = VGroup(Ellipse(width=4.80, height=2.10, color=DIM, stroke_width=2.5).move_to([cx, cy, 0]))
  rng = np.random.default_rng(3)
  pts = []
  for _ in range(46):
   a = rng.uniform(0, 2 * np.pi); r = np.sqrt(rng.uniform(0, 1))
   pts.append([cx + r * np.cos(a) * 2.15, cy + r * np.sin(a) * 0.92, 0])
  for q in pts:
   g.add(Dot(q, radius=0.045, color=GHOST))
  for idx, col in ((range(0, 4), ACCENT_B), (range(8, 13), ACCENT_C)):
   for i in idx:
    g.add(Dot(pts[i], radius=0.075, color=col))
  g.add(Text("A", font_size=FS_TAG, color=DIM).move_to([cx, cy + 1.27, 0]),
        Text("…", font_size=FS_TAG + 6, color=GHOST).move_to([cx + 1.55, cy - 0.55, 0]))
  return g.add(self._mid(0.85, "兩個線性組合各自是有限和",
                         "each combination is a finite sum",
                         DIM, FS_TAG, x=3.35, w=5.3),
               self._mid(0.15, "加起來還是有限個", "their sum is still finite",
                         ACCENT_A, FS_TAG, x=3.35, w=5.3),
               self._mid(-0.55, "所以還是線性組合", "so it is again a linear combination",
                         ACCENT_B, FS_TAG, x=3.35, w=5.3),
               self._mid(-1.55, "A 無限也列不完，但論證照樣走得通",
                         "an infinite A cannot be listed, but the argument still runs",
                         DIM, FS_TAG, w=11.6))

 def _spanning(self):
  """Finite dimension on the left, its failure on the right: a tower of powers
  with no finite spanning set."""
  o = np.array([-4.05, -0.55, 0.0])
  e1, e2 = np.array([1.15, 0.0, 0.0]), np.array([0.0, 1.05, 0.0])
  g = VGroup(self._arr(o, o + e1, ACCENT_B, sw=3.5, tl=0.16),
             self._arr(o, o + e2, ACCENT_C, sw=3.5, tl=0.16),
             self._arr(o, o + 1.55 * e1 + 1.25 * e2, ACCENT_A, sw=4.5, tl=0.20),
             self._dash(o + 1.55 * e1, o + 1.55 * e1 + 1.25 * e2, GHOST, n=7),
             self._dash(o + 1.25 * e2, o + 1.55 * e1 + 1.25 * e2, GHOST, n=7),
             Dot(o, radius=0.06, color=INK),
             Text("δ¹", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + e1 + np.array([0.10, -0.26, 0])),
             Text("δ²", font_size=FS_TAG - 2, color=ACCENT_C)
             .move_to(o + e2 + np.array([-0.30, 0.10, 0])),
             self._mid(-1.25, "有限個就生成得出來", "a finite set already spans it",
                       ACCENT_A, FS_TAG, x=-3.35, w=4.4))
  # A bare column with an arrow running off the bottom. Ruling a line through
  # each power turned the group into something that reads as a musical staff.
  bx = 2.35
  for k, s in enumerate(("1", "t", "t²", "t³", "t⁴")):
   g.add(Text(s, font_size=FS_TAG + 1, color=ACCENT_C).move_to([bx, 0.95 - k * 0.42, 0]))
  g.add(self._arr([bx - 0.62, 1.15, 0], [bx - 0.62, -1.15, 0], GHOST, sw=2, tl=0.12),
        Text("…", font_size=FS_TAG + 4, color=GHOST).move_to([bx, -1.02, 0]))
  return g.add(self._mid(-1.25, "這一列停不下來", "this list never stops",
                         WARN, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.78, "閉區間上的連續函數沒有有限生成集 —— 這件事是對的，但並不明顯",
                         "the continuous functions on an interval have no finite spanning set",
                         DIM, FS_TAG, w=11.8))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  twelve, bag, idx = self._twelve(), self._bag(), self._index_sets()
  ind, comb, fns = self._induction(), self._combination(), self._functions()
  spn, nest = self._span(), self._nesting()
  clo, inf, sp2 = self._closure(), self._infinite(), self._spanning()

  return [([twelve], []),                      # 0  twelve ways, one endpoint
          ([bag], [twelve]),                   # 1  the index set suffices
          ([idx], [bag]),                      # 2  ordered and unordered indices
          ([ind], [idx]),                      # 3  the starred induction
          ([comb], [ind]),                     # 4  linear combination
          ([fns], [comb]),                     # 5  sine, cosine, exponential
          ([spn], [fns]),                      # 6  the span of two vectors
          ([nest], [spn]),                     # 7  Theorem 1.1
          ([clo], [nest]),                     # 8  closure, on the coefficients
          ([inf], [clo]),                      # 9  an infinite A
          ([sp2], [inf])]                      # 10 spanning and finite dimension


AdvCalcE06ZH, AdvCalcE06EN = make(AdvCalcE06Base, "06", prefix="AdvCalcE")
