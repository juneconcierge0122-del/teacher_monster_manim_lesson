"""advcalc E05 — Chapter 1, section 1, first half (book pp. 21-25): the axioms,
the standard function-space example, and subspaces.

The section moves from pictures to axioms and then back out to function spaces,
so the beats do the same. Beats 1-3 are the book's own three figures (the
parallelogram rule, the scalar multiples along a line, the parallelepiped whose
diagonal proves associativity). Beats 6-7 are the eight axioms, and the trap
there is obvious: the formula bar already lists them, so the pictures show what
each law *does* to an arrow instead of restating it. Beats 8-10 carry the real
payload of the section -- that a space of functions is a vector space, and that
a subset closed under the operations is one too.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# Axonometric screen basis for the three-dimensional beats.
EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE05Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 5

 MODE_LABEL = {
  0: {"zh": "微積分加上向量空間理論", "en": "calculus plus the theory of vector spaces"},
  1: {"zh": "平行四邊形法則", "en": "the parallelogram rule"},
  2: {"zh": "乘上一個數", "en": "multiplication by a number"},
  3: {"zh": "結合律：同一條對角線", "en": "associativity: the same diagonal"},
  4: {"zh": "座標三元組：逐項相加", "en": "coordinate triples: added entry by entry"},
  5: {"zh": "三元組其實是一個函數", "en": "a triple is really a function"},
  6: {"zh": "四條加法公理", "en": "the four axioms for addition"},
  7: {"zh": "四條純量公理", "en": "the four axioms for the scalars"},
  8: {"zh": "A 上的實值函數，逐點相加", "en": "real-valued functions on A, added pointwise"},
  9: {"zh": "子空間：對兩個運算封閉", "en": "a subspace: closed under both operations"},
  10: {"zh": "連續函數是一個函數空間", "en": "the continuous functions form a function space"},
 }

 # ── beat 0: why two chapters go on vector spaces at all ───────────
 def _why(self):
  boxes = ((-4.15, 0.78, "單變數微積分", "calculus of one variable", ACCENT_B),
           (-4.15, -0.42, "向量空間理論", "theory of vector spaces", ACCENT_C))
  g = VGroup()
  for x, y, zh, en, col in boxes:
   g.add(Rectangle(width=3.30, height=0.72, color=col, stroke_width=2.5).move_to([x, y, 0]),
         self._mid(y, zh, en, col, FS_TAG, x=x, w=3.05))
   g.add(self._arr([x + 1.75, y, 0], [-0.85, 0.18, 0], DIM, sw=2.2, tl=0.12))
  g.add(Rectangle(width=3.10, height=0.72, color=ACCENT_A, stroke_width=2.5).move_to([0.85, 0.18, 0]),
        self._mid(0.18, "多變數微積分", "calculus of several variables", ACCENT_A, FS_TAG,
                  x=0.85, w=2.85),
        self._mid(0.78, "第 1 章：一般的 V", "chapter 1: V in general", DIM, FS_TAG, x=4.35, w=3.4),
        self._mid(-0.42, "第 2 章：有限維", "chapter 2: finite-dimensional", DIM, FS_TAG,
                  x=4.35, w=3.4),
        self._arr([2.45, 0.18, 0], [3.05, 0.62, 0], DIM, sw=2, tl=0.10),
        self._arr([2.45, 0.18, 0], [3.05, -0.28, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(-1.45, "處理得好不好，取決於向量空間理論用得夠不夠徹底",
                         "how well it goes depends on how thoroughly that theory is used",
                         DIM, FS_TAG, w=11.6))

 # ── beats 1-3: the book's three figures ───────────────────────────
 O = np.array([-2.60, -0.45, 0.0])
 VA = np.array([1.55, 1.35, 0.0])
 VB = np.array([2.05, -0.28, 0.0])

 def _parallelogram(self):
  """Fig. 1.1. The diagonal from O is the sum."""
  o, a, b = self.O, self.O + self.VA, self.O + self.VB
  p = self.O + self.VA + self.VB
  g = VGroup(self._dash(a, p, GHOST, n=10), self._dash(b, p, GHOST, n=10),
             self._arr(o, a, ACCENT_B, sw=4, tl=0.18),
             self._arr(o, b, ACCENT_C, sw=4, tl=0.18),
             self._arr(o, p, ACCENT_A, sw=5, tl=0.22),
             Dot(o, radius=0.06, color=INK))
  for pt, s, col, off in ((o, "O", INK, (-0.26, -0.20)), (a, "A", ACCENT_B, (-0.24, 0.20)),
                          (b, "B", ACCENT_C, (0.10, -0.30)), (p, "P", ACCENT_A, (0.26, 0.16))):
   g.add(Text(s, font_size=FS_TAG, color=col).move_to(pt + np.array([off[0], off[1], 0.0])))
  return g.add(self._mid(0.85, "以兩個箭頭為鄰邊", "the two arrows as sides",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(0.15, "作出平行四邊形", "build the parallelogram",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(-0.55, "從原點出發的對角線就是和",
                         "the diagonal from the origin is the sum",
                         ACCENT_A, FS_TAG, x=3.20, w=5.4))

 def _scalar(self):
  """Fig. 1.2. Same line, length scaled, side decided by the sign."""
  o = np.array([-0.60, -0.10, 0.0])
  d = np.array([1.35, 0.62, 0.0])
  g = VGroup(Line(o - 1.30 * d, o + 1.90 * d, color=GHOST, stroke_width=2),
             Dot(o, radius=0.06, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.18, -0.28, 0])))
  for k, (f, s, col) in enumerate(((1.0, "A", INK), (1.5, "B", ACCENT_A), (-0.5, "C", ACCENT_C))):
   g.add(self._arr(o, o + f * d, col, sw=4 if k else 3, tl=0.18),
         Text(s, font_size=FS_TAG, color=col)
         .move_to(o + f * d + np.array([0.10, 0.28, 0])))
  return g.add(self._mid(0.95, "同一條直線上", "along the same line", DIM, FS_TAG, x=-4.00, w=4.2),
               self._mid(0.25, "長度乘上 x 的絕對值", "length scaled by the size of x",
                         ACCENT_A, FS_TAG, x=-4.00, w=4.2),
               self._mid(-0.45, "x 為負就換到另一側", "negative x flips to the other side",
                         ACCENT_C, FS_TAG, x=-4.00, w=4.2))

 def _parallelepiped(self):
  """Fig. 1.3: the two bracketings of a sum of three vectors reach the same
  corner of the box, which is the whole of the geometric proof."""
  # The box has to be sized against the projection, not against its own edge
  # lengths: EZ is straight up and EY leans up, so the tallest corner is B+C,
  # not the far corner A+B+C, and it is B+C that decides the clearance.
  org = np.array([-1.80, -0.80, 0.0])
  s = 1.0
  a, b, c = np.array([1.75, 0, 0]), np.array([0, 1.55, 0]), np.array([0, 0, 1.15])
  P = {k: _p(v, org, s) for k, v in
       (("o", 0 * a), ("a", a), ("b", b), ("c", c), ("ab", a + b), ("bc", b + c),
        ("ac", a + c), ("x", a + b + c))}
  edges = (("o", "a"), ("o", "b"), ("o", "c"), ("a", "ab"), ("b", "ab"), ("b", "bc"),
           ("c", "bc"), ("c", "ac"), ("a", "ac"), ("ab", "x"), ("bc", "x"), ("ac", "x"))
  g = VGroup(*[self._dash(P[u], P[v], GHOST, n=8) for u, v in edges])
  g.add(self._arr(P["o"], P["a"], ACCENT_B, sw=3.5, tl=0.16),
        self._arr(P["o"], P["b"], ACCENT_C, sw=3.5, tl=0.16),
        self._arr(P["o"], P["c"], ACCENT_B, sw=3.5, tl=0.16),
        self._arr(P["o"], P["ab"], DIM, sw=2.5, tl=0.13),
        self._arr(P["o"], P["bc"], DIM, sw=2.5, tl=0.13),
        self._arr(P["o"], P["x"], ACCENT_A, sw=5, tl=0.22))
  for k, s2, col, off in (("o", "O", INK, (-0.24, -0.18)), ("a", "A", ACCENT_B, (-0.10, -0.26)),
                          ("b", "B", ACCENT_C, (0.24, -0.10)), ("c", "C", ACCENT_B, (-0.26, 0.14)),
                          ("ab", "P", DIM, (0.06, -0.28)), ("bc", "Q", DIM, (0.26, 0.06)),
                          ("x", "X", ACCENT_A, (0.26, 0.16))):
   g.add(Text(s2, font_size=FS_TAG, color=col).move_to(P[k] + np.array([off[0], off[1], 0.0])))
  return g.add(self._mid(0.95, "先 A 加 B，再加 C", "A plus B first, then C",
                         DIM, FS_TAG, x=3.55, w=5.0),
               self._mid(0.25, "或先 B 加 C，再加 A", "or B plus C first, then A",
                         DIM, FS_TAG, x=3.55, w=5.0),
               self._mid(-0.45, "落在同一個角上 X", "the same corner X either way",
                         ACCENT_A, FS_TAG, x=3.55, w=5.0),
               # Kept out of the full-width bottom slot: vertex A of the box
               # sits at y = -1.33 and its label runs to -1.59, right through it.
               self._mid(-1.15, "但幾何證明說服力有餘，嚴密不足",
                         "such proofs are sketchy, not airtight",
                         WARN, FS_TAG, x=3.55, w=5.0))

 # ── beats 4-5: triples, and triples as functions ──────────────────
 T1 = (2, -1, 3)
 T2 = (1, 4, -2)

 def _triples(self):
  """The two columns added entry by entry, with the arithmetic shown."""
  dy = 0.56
  cols = ((-3.40, self.T1, ACCENT_B), (-1.55, self.T2, ACCENT_C),
          (1.55, tuple(a + b for a, b in zip(self.T1, self.T2)), ACCENT_A))
  g = VGroup(Text("+", font_size=FS_TAG + 6, color=DIM).move_to([-2.48, 0.10, 0]),
             Text("=", font_size=FS_TAG + 6, color=DIM).move_to([-0.20, 0.10, 0]))
  for x, tup, col in cols:
   g.add(Rectangle(width=0.86, height=3 * dy + 0.30, color=col, stroke_width=2.5)
         .move_to([x, 0.10, 0]))
   for k, v in enumerate(tup):
    g.add(Text(str(v), font_size=FS_TAG + 3, color=col).move_to([x, 0.10 + (1 - k) * dy, 0]))
  for k in range(3):
   y = 0.10 + (1 - k) * dy
   if k == 1:                                # the equals sign sits on this row
    g.add(self._dash([-1.05, y, 0], [-0.44, y, 0], GHOST, n=3),
          self._dash([0.04, y, 0], [1.05, y, 0], GHOST, n=5))
   else:
    g.add(self._dash([-1.05, y, 0], [1.05, y, 0], GHOST, n=9))
  return g.add(self._mid(0.75, "逐項相加", "added entry by entry", DIM, FS_TAG, x=4.30, w=3.6),
               self._mid(0.05, "數乘也逐項", "scaling too, entry by entry",
                         DIM, FS_TAG, x=4.30, w=3.6),
               self._mid(-0.65, "幾乎只是形式推演", "almost a formality",
                         ACCENT_A, FS_TAG, x=4.30, w=3.6),
               self._mid(-1.55, "所以向量律對這種對象好證得多",
                         "so the vector laws are much easier to prove here",
                         DIM, FS_TAG, w=11.4))

 def _as_function(self):
  """Domain {1,2,3} on the left, the value at each index on a number line."""
  g = VGroup()
  ox = -4.10
  # The triple runs from -1 to 3, so the number line is scaled and shifted to
  # keep the value 3 clear of the formula bar.
  ysc, yoff = 0.40, -0.20
  def yv(v):
   return yoff + v * ysc
  for k, v in enumerate(self.T1):
   y = 0.72 - k * 0.70
   g.add(Dot([ox, y, 0], radius=0.075, color=ACCENT_B),
         Text(str(k + 1), font_size=FS_TAG, color=ACCENT_B).move_to([ox - 0.40, y, 0]),
         self._arr([ox + 0.22, y, 0], [-0.30, yv(v), 0], ACCENT_A, sw=2.2, tl=0.11))
  ax = 1.90
  g.add(Line([ax, yv(-2.4), 0], [ax, yv(3.4), 0], color=GHOST, stroke_width=2))
  for v in range(-2, 4):
   g.add(Line([ax - 0.10, yv(v), 0], [ax + 0.10, yv(v), 0], color=GHOST, stroke_width=2))
  for v in self.T1:
   g.add(Dot([ax, yv(v), 0], radius=0.07, color=ACCENT_A))
   g.add(self._arr([-0.10, yv(v), 0], [ax - 0.16, yv(v), 0], ACCENT_A, sw=2, tl=0.10))
  g.add(Text("ℝ", font_size=FS_TAG + 2, color=DIM).move_to([ax + 0.42, yv(3.2), 0]))
  return g.add(self._mid(0.55, "定義域是一到三", "the domain is one to three",
                         DIM, FS_TAG, x=4.20, w=3.7),
               self._mid(-0.15, "第 i 項就是在 i 的值", "the ith entry is the value at i",
                         ACCENT_A, FS_TAG, x=4.20, w=3.7),
               self._mid(-1.55, "換一個定義域，就得到一般的函數空間",
                         "change the domain and you have a general function space",
                         ACCENT_B, FS_TAG, w=11.4))

 # ── beats 6-7: what the axioms do, rather than what they say ──────
 def _axioms_add(self):
  """A1-A4 as four small pictures. The formula bar already lists them, so
  each panel shows the move the law licenses."""
  g = VGroup()
  panels = ((-4.65, "A1", "換分組，終點不動", "regroup, the endpoint holds"),
            (-1.55, "A2", "換順序，終點不動", "reorder, the endpoint holds"),
            (1.55, "A3", "加零，什麼都沒變", "add zero, nothing moves"),
            (4.65, "A4", "加上反向的，回到原點", "add the reverse, back to O"))
  for cx, tag, zh, en in panels:
   o = np.array([cx - 0.72, -0.30, 0.0])
   u = np.array([0.78, 0.52, 0.0])
   v = np.array([0.66, -0.30, 0.0])
   g.add(Text(tag, font_size=FS_TAG, color=ACCENT_A).move_to([cx, 1.10, 0]),
         Dot(o, radius=0.05, color=INK))
   if tag == "A3":
    g.add(self._arr(o, o + u, ACCENT_B, sw=3.5, tl=0.15),
          Dot(o + u, radius=0.07, color=ACCENT_A))
   elif tag == "A4":
    g.add(self._arr(o, o + u, ACCENT_B, sw=3.5, tl=0.15),
          self._arr(o + u, o, ACCENT_C, sw=3.5, tl=0.15))
   else:
    g.add(self._arr(o, o + u, ACCENT_B, sw=3, tl=0.14),
          self._arr(o + u, o + u + v, ACCENT_C, sw=3, tl=0.14),
          self._dash(o, o + v, GHOST, n=6), self._dash(o + v, o + u + v, GHOST, n=6),
          Dot(o + u + v, radius=0.07, color=ACCENT_A))
   g.add(self._mid(-1.15, zh, en, DIM, FS_TAG, x=cx, w=2.85))
  return g.add(self._mid(-1.72, "由這四條就能推出零元素唯一、反元素唯一",
                         "these four already give a unique zero and unique negatives",
                         ACCENT_A, FS_TAG, w=11.6))

 def _axioms_scalar(self):
  """S1-S4: scaling twice versus scaling once, and the two distributive laws
  as a pair of similar triangles."""
  o = np.array([-4.30, -0.55, 0.0])
  d = np.array([0.92, 0.44, 0.0])
  g = VGroup(Text("S1", font_size=FS_TAG, color=ACCENT_A).move_to([-3.55, 1.10, 0]),
             self._arr(o, o + d, ACCENT_B, sw=3, tl=0.14),
             self._arr(o, o + 1.6 * d, ACCENT_C, sw=3, tl=0.14),
             self._arr(o, o + 2.4 * d, ACCENT_A, sw=4, tl=0.18),
             self._mid(-1.15, "連乘兩次 = 乘上乘積", "scale twice = scale by the product",
                       DIM, FS_TAG, x=-3.55, w=3.1))
  o2 = np.array([0.05, -0.55, 0.0])
  u = np.array([0.85, 0.62, 0.0])
  v = np.array([0.92, -0.10, 0.0])
  g.add(Text("S2  S3", font_size=FS_TAG, color=ACCENT_A).move_to([1.35, 1.10, 0]),
        self._arr(o2, o2 + u, ACCENT_B, sw=2.5, tl=0.12),
        self._arr(o2 + u, o2 + u + v, ACCENT_C, sw=2.5, tl=0.12),
        self._arr(o2, o2 + u + v, DIM, sw=2, tl=0.11),
        self._arr(o2, o2 + 1.7 * u, ACCENT_B, sw=3.5, tl=0.16),
        self._arr(o2 + 1.7 * u, o2 + 1.7 * (u + v), ACCENT_C, sw=3.5, tl=0.16),
        self._arr(o2, o2 + 1.7 * (u + v), ACCENT_A, sw=4, tl=0.18),
        self._mid(-1.15, "放大整個平行四邊形", "the whole parallelogram scales",
                  DIM, FS_TAG, x=1.35, w=3.4))
  o3 = np.array([4.05, -0.55, 0.0])
  g.add(Text("S4", font_size=FS_TAG, color=ACCENT_A).move_to([4.85, 1.10, 0]),
        self._arr(o3, o3 + 1.55 * d, ACCENT_A, sw=4, tl=0.18),
        self._mid(-1.15, "乘以一，原封不動", "times one, unchanged",
                  DIM, FS_TAG, x=4.85, w=2.6))
  return g.add(self._mid(-1.72, "而且零乘任何向量都得到零向量",
                         "and zero times any vector is the zero vector",
                         ACCENT_A, FS_TAG, w=11.6))

 # ── beats 8-10: function spaces and subspaces ─────────────────────
 def _fn_space(self):
  """Two graphs and their pointwise sum, with the addition shown at one point
  as a stack of two segments."""
  ax, w = -2.60, 4.20                        # pushed left; the right third is captions
  base = -0.95
  xs = np.linspace(-1, 1, 60)
  def curve(fn, col, sw=3):
   return self._curve([[ax + t * w / 2, base + fn(t), 0] for t in xs], col, sw=sw)
  f = lambda t: 0.55 + 0.42 * np.sin(2.6 * t)
  gg = lambda t: 0.30 + 0.34 * t
  g = VGroup(Line([ax - w / 2, base, 0], [ax + w / 2, base, 0], color=GHOST, stroke_width=2),
             curve(f, ACCENT_B), curve(gg, ACCENT_C),
             curve(lambda t: f(t) + gg(t), ACCENT_A, sw=4))
  t0 = 0.35
  x0 = ax + t0 * w / 2
  g.add(self._dash([x0, base, 0], [x0, base + f(t0) + gg(t0), 0], GHOST, n=9),
        Dot([x0, base + f(t0), 0], radius=0.06, color=ACCENT_B),
        Dot([x0, base + gg(t0), 0], radius=0.06, color=ACCENT_C),
        Dot([x0, base + f(t0) + gg(t0), 0], radius=0.075, color=ACCENT_A),
        Text("A", font_size=FS_TAG, color=DIM).move_to([ax + w / 2 + 0.28, base, 0]))
  return g.add(self._mid(0.95, "f 與 g 都是 A 上的實值函數",
                         "f and g are real-valued functions on A",
                         DIM, FS_TAG, x=3.35, w=5.5),
               self._mid(0.25, "在每一點把值加起來", "add the values at each point",
                         ACCENT_A, FS_TAG, x=3.35, w=5.5),
               self._mid(-0.45, "所有這種函數所成的集合就是向量空間",
                         "all such functions form a vector space",
                         ACCENT_B, FS_TAG, x=3.35, w=5.5),
               self._mid(-1.55, "定義域 A 取一到三就回到三元組，取整條實線就是實函數",
                         "taking A to be one to three returns the triples; the line gives functions",
                         DIM, FS_TAG, w=11.6))

 def _subspace(self):
  """A plane through the origin: two arrows in it, and their sum still in it."""
  org = np.array([-2.30, -0.35, 0.0])
  s = 0.95
  quad = [_p(v, org, s) for v in ((-1.7, -1.5, 0), (1.7, -1.5, 0), (1.7, 1.5, 0), (-1.7, 1.5, 0))]
  u, v = np.array([1.15, -0.75, 0]), np.array([0.25, 1.30, 0])
  g = VGroup(Polygon(*quad, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.13),
             self._arr(_p(0 * u, org, s), _p(u, org, s), ACCENT_C, sw=3.5, tl=0.16),
             self._arr(_p(0 * u, org, s), _p(v, org, s), ACCENT_C, sw=3.5, tl=0.16),
             self._arr(_p(0 * u, org, s), _p(u + v, org, s), ACCENT_A, sw=4.5, tl=0.20),
             self._dash(_p(u, org, s), _p(u + v, org, s), GHOST, n=8),
             self._dash(_p(v, org, s), _p(u + v, org, s), GHOST, n=8),
             Dot(_p(0 * u, org, s), radius=0.06, color=INK),
             Text("W", font_size=FS_TAG, color=ACCENT_B).move_to(_p(np.array([-1.35, 1.15, 0]), org, s)))
  return g.add(self._mid(0.95, "取 V 的一個非空子集", "take a nonempty subset of V",
                         DIM, FS_TAG, x=3.35, w=5.3),
               self._mid(0.25, "和留在裡面，數乘也留在裡面",
                         "sums stay inside, and so do scalar multiples",
                         ACCENT_A, FS_TAG, x=3.35, w=5.3),
               self._mid(-0.45, "那它自己就是一個向量空間",
                         "then it is a vector space in its own right",
                         ACCENT_B, FS_TAG, x=3.35, w=5.3),
               self._mid(-1.55, "封閉性保證零元素與反元素也都留在裡面",
                         "closure is what keeps the zero and the negatives inside",
                         DIM, FS_TAG, w=11.6))

 def _examples(self):
  """The two examples the section closes on, side by side."""
  ax, w, base = -3.30, 3.30, -0.70
  xs = np.linspace(-1, 1, 70)
  rng = np.random.default_rng(4)
  jag = rng.uniform(-0.42, 0.42, len(xs))
  g = VGroup(Line([ax - w / 2, base, 0], [ax + w / 2, base, 0], color=GHOST, stroke_width=2),
             self._curve([[ax + t * w / 2, base + 0.85 + 0.40 * np.sin(2.4 * t), 0] for t in xs],
                         ACCENT_A, sw=4),
             self._curve([[ax + t * w / 2, base + 0.30 + j, 0] for t, j in zip(xs, jag)],
                         GHOST, sw=2),
             self._mid(1.05, "連續的", "continuous", ACCENT_A, FS_TAG, x=ax, w=3.2),
             self._mid(-1.20, "連續函數 ⊂ 所有實值函數",
                       "continuous functions inside all real-valued ones",
                       DIM, FS_TAG, x=ax, w=5.0))
  # The axis tip and the caption above it are the classic pair that collide:
  # keep the arrow head below the caption's own bottom edge.
  cx, cy, r = 3.15, -0.10, 0.95
  g.add(self._arr([cx - r, cy, 0], [cx + r, cy, 0], DIM, sw=2.5, tl=0.13),
        self._arr([cx, cy - r, 0], [cx, cy + r, 0], DIM, sw=2.5, tl=0.13),
        Line([cx - 0.80, cy + 0.80, 0], [cx + 0.80, cy - 0.80, 0],
             color=ACCENT_B, stroke_width=4),
        Dot([cx, cy, 0], radius=0.06, color=INK),
        self._mid(1.05, "平面上兩座標相加等於零", "the two coordinates summing to zero",
                  ACCENT_B, FS_TAG, x=cx, w=4.6),
        self._mid(-1.20, "也是一個子空間", "also a subspace", ACCENT_B, FS_TAG, x=cx, w=4.6))
  return g.add(self._mid(-1.72, "書上預設純量是實數，但換成複數或任何一個體都照樣成立",
                         "the book takes the scalars real, but any field would do",
                         DIM, FS_TAG, w=11.6))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  why, par, sca = self._why(), self._parallelogram(), self._scalar()
  box, tri, fn = self._parallelepiped(), self._triples(), self._as_function()
  ax1, ax2 = self._axioms_add(), self._axioms_scalar()
  fs, sub, ex = self._fn_space(), self._subspace(), self._examples()

  return [([why], []),                         # 0  why vector spaces
          ([par], [why]),                      # 1  parallelogram rule
          ([sca], [par]),                      # 2  scalar multiples
          ([box], [sca]),                      # 3  the parallelepiped
          ([tri], [box]),                      # 4  coordinate triples
          ([fn], [tri]),                       # 5  a triple as a function
          ([ax1], [fn]),                       # 6  A1-A4
          ([ax2], [ax1]),                      # 7  S1-S4
          ([fs], [ax2]),                       # 8  the function space
          ([sub], [fs]),                       # 9  subspaces
          ([ex], [sub])]                       # 10 the two examples


AdvCalcE05ZH, AdvCalcE05EN = make(AdvCalcE05Base, "05", prefix="AdvCalcE")
