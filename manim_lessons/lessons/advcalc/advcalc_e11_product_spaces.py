"""advcalc E11 — Chapter 1, section 3, first half (book pp. 43-46): product
spaces, Theorem 3.1, Hom(V, W) and composition.

The one idea a picture can carry here that the formula bar cannot is that a
product space lets the target differ from index to index. So beats 0 and 1 are
deliberately the same diagram twice, once with every arrow landing in one copy
of W and once with each landing somewhere different -- the change between the
two frames is the definition.

Beat 2 is the book's own Fig. 1.8, and it is the payoff: an element of a
product over the sphere is a vector field, which is a thing worth seeing rather
than reading.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Circle, Dot, Ellipse, Line, PI, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE11Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 11

 MODE_LABEL = {
  0: {"zh": "每個指標都落進同一個 W", "en": "every index lands in the same W"},
  1: {"zh": "但沒有理由要同一個", "en": "but there is no reason it must be"},
  2: {"zh": "球面上的向量場", "en": "a vector field on the sphere"},
  3: {"zh": "座標投影，不是座標泛函", "en": "a projection, not a functional"},
  4: {"zh": "運算被「投影要線性」逼出來", "en": "linearity of the projections forces it"},
  5: {"zh": "恰好只有一種辦法", "en": "in exactly one way"},
  6: {"zh": "把線性的那些挑出來", "en": "singling out the linear ones"},
  7: {"zh": "Hom 是一個子空間", "en": "Hom is a subspace"},
  8: {"zh": "合成還是線性", "en": "composition stays linear"},
  9: {"zh": "分配律，兩邊都成立", "en": "distributive on both sides"},
  10: {"zh": "固定 T 從右邊合成", "en": "composing with a fixed T"},
 }

 IDX = (0.85, 0.20, -0.45, -1.10)

 def _fan(self, same):
  """Index dots on the left, each with an arrow into a target region. With
  `same` all four arrows end in one copy of W; otherwise each ends in its own
  space, which is the entire difference between the two definitions."""
  ax = -4.05
  g = VGroup(Text("I", font_size=FS_TAG, color=DIM).move_to([ax, 1.20, 0]))
  cols = (ACCENT_B, ACCENT_C, ACCENT_A, WARN)
  for k, y in enumerate(self.IDX):
   g.add(Dot([ax, y, 0], radius=0.075, color=DIM),
         Text(f"i{k + 1}", font_size=FS_TAG - 4, color=DIM).move_to([ax - 0.44, y, 0]))
   if same:
    g.add(self._arr([ax + 0.18, y, 0], [0.45, -0.10, 0], ACCENT_B, sw=2, tl=0.10))
   else:
    g.add(self._arr([ax + 0.18, y, 0], [0.45, y, 0], cols[k], sw=2, tl=0.10))
  if same:
   g.add(Ellipse(width=2.30, height=2.05, color=ACCENT_B, stroke_width=2.5,
                 fill_color=ACCENT_B, fill_opacity=0.10).move_to([1.65, -0.10, 0]),
         Text("W", font_size=FS_TAG + 1, color=ACCENT_B).move_to([1.65, -0.10, 0]))
  else:
   for k, y in enumerate(self.IDX):
    g.add(Ellipse(width=1.55, height=0.52, color=cols[k], stroke_width=2.5,
                  fill_color=cols[k], fill_opacity=0.10).move_to([1.35, y, 0]),
          Text(f"W{k + 1}", font_size=FS_TAG - 3, color=cols[k]).move_to([1.35, y, 0]))
  return g

 def _same_w(self):
  return self._fan(True).add(
   self._mid(0.95, "定義域是任意集合", "the domain is any set at all",
             DIM, FS_TAG, x=4.55, w=3.2),
   self._mid(0.15, "值都落在同一個 W", "all the values in one W", ACCENT_B, FS_TAG, x=4.55, w=3.2),
   self._mid(-1.55, "加法逐點做，數乘也逐點做，理由跟實值函數空間一模一樣",
             "addition and scaling are pointwise, for exactly the same reasons as before",
             DIM, FS_TAG, w=11.8))

 def _diff_w(self):
  return self._fan(False).add(
   self._mid(0.95, "每個指標配自己的空間", "each index gets its own space",
             ACCENT_A, FS_TAG, x=4.55, w=3.2),
   self._mid(0.15, "這就是笛卡兒積", "and that is the Cartesian product",
             DIM, FS_TAG, x=4.55, w=3.2),
   self._mid(-1.55, "元素是定義域為 I 的函數，在每個 i 的值落在第 i 個空間裡",
             "an element is a function on I whose value at each i lies in the ith space",
             DIM, FS_TAG, w=11.8))

 # ── beat 2: the book's Fig. 1.8 ──────────────────────────────────
 def _sphere(self):
  """A sphere with a tangent plane and a vector at three of its points: one
  element of the product over all points of the sphere.

  Drawn as the flat idiom -- outline circle, one equator ellipse, one meridian
  ellipse -- rather than as a projected mesh of the octant. The mesh version
  came out as a crumpled fan, because the axonometric basis is not orthonormal
  on screen and the octant folds over itself."""
  c = np.array([-3.30, -0.20, 0.0])
  R = 1.30
  g = VGroup(Circle(radius=R, color=GHOST, stroke_width=2.5).move_to(c),
             Ellipse(width=2 * R, height=0.66 * R, color=GHOST, stroke_width=2).move_to(c),
             Ellipse(width=0.66 * R, height=2 * R, color=GHOST, stroke_width=2).move_to(c))
  for (ang, rr), col in (((0.95, 0.74), ACCENT_A), ((2.35, 0.66), ACCENT_C),
                         ((-0.75, 0.80), ACCENT_B)):
   n = np.array([np.cos(ang), np.sin(ang), 0.0])
   tg = np.array([-n[1], n[0], 0.0])
   pt = c + rr * R * n
   g.add(Ellipse(width=0.92, height=0.30, color=col, stroke_width=2,
                 fill_color=col, fill_opacity=0.20)
         .move_to(pt).rotate(ang + PI / 2, about_point=pt),
         Dot(pt, radius=0.055, color=INK),
         self._arr(pt, pt + 0.74 * tg, col, sw=3, tl=0.14))
  return g.add(self._mid(0.95, "每一點的切平面是一個子空間",
                         "the tangent plane at each point is a subspace",
                         DIM, FS_TAG, x=3.15, w=5.6),
               self._mid(0.15, "乘積裡的一個元素", "one element of the product",
                         DIM, FS_TAG, x=3.15, w=5.6),
               self._mid(-0.65, "就是在每一點指定一個切向量",
                         "assigns a tangent vector at every point",
                         ACCENT_A, FS_TAG, x=3.15, w=5.6),
               self._mid(-1.55, "也就是球面上的一個向量場",
                         "that is, a vector field on the sphere",
                         ACCENT_A, FS_TAG, w=11.4))

 def _projection(self):
  """Evaluation at j, with the answer being a vector rather than a number --
  which is the whole reason for the change of name."""
  g = VGroup(Ellipse(width=3.30, height=2.15, color=DIM, stroke_width=2.5)
             .move_to([-3.35, 0.05, 0]),
             Text("f", font_size=FS_TAG + 4, color=ACCENT_A).move_to([-3.35, 0.05, 0]),
             self._arr([-1.60, 0.05, 0], [-0.20, 0.05, 0], ACCENT_A, sw=3, tl=0.15),
             Text("πⱼ", font_size=FS_TAG, color=ACCENT_A).move_to([-0.90, 0.42, 0]))
  o = np.array([1.85, -0.35, 0.0])
  g.add(Ellipse(width=2.60, height=1.75, color=ACCENT_B, stroke_width=2.5,
                fill_color=ACCENT_B, fill_opacity=0.10).move_to([1.85, 0.05, 0]),
        self._arr(o, o + np.array([0.85, 0.62, 0]), ACCENT_A, sw=3.5, tl=0.16),
        Dot(o, radius=0.055, color=INK),
        Text("Wⱼ", font_size=FS_TAG - 2, color=ACCENT_B).move_to([1.85, 0.82, 0]))
  return g.add(self._mid(0.95, "還是在 j 取值", "still evaluation at j",
                         DIM, FS_TAG, x=4.55, w=3.2),
               self._mid(-0.70, "但取到的是向量", "but the value is a vector",
                         ACCENT_A, FS_TAG, x=4.55, w=3.2),
               self._mid(-1.55, "所以叫座標投影，不叫座標泛函",
                         "hence a coordinate projection, not a functional",
                         DIM, FS_TAG, w=11.4))

 def _forced(self):
  """Two elements added at one index: the value there has to be the sum."""
  g = VGroup()
  for k, (lab, col, dy) in enumerate((("f", ACCENT_B, 0.75), ("g", ACCENT_C, 0.05),
                                      ("f + g", ACCENT_A, -0.75))):
   g.add(Ellipse(width=2.05, height=0.56, color=col, stroke_width=2.5).move_to([-3.55, dy, 0]),
         Text(lab, font_size=FS_TAG, color=col).move_to([-3.55, dy, 0]),
         self._arr([-2.45, dy, 0], [-1.30, dy, 0], DIM, sw=2, tl=0.10),
         Text("πⱼ", font_size=FS_TAG - 4, color=DIM).move_to([-1.88, dy + 0.24, 0]))
  o = np.array([-0.35, 0.0, 0.0])
  u, v = np.array([1.00, 0.42, 0.0]), np.array([0.42, -0.80, 0.0])
  g.add(self._arr(o, o + u, ACCENT_B, sw=3, tl=0.14),
        self._arr(o, o + v, ACCENT_C, sw=3, tl=0.14),
        self._arr(o, o + u + v, ACCENT_A, sw=4, tl=0.18),
        self._dash(o + u, o + u + v, GHOST, n=7),
        self._dash(o + v, o + u + v, GHOST, n=7),
        Dot(o, radius=0.055, color=INK),
        Text("Wⱼ", font_size=FS_TAG - 2, color=DIM).move_to([-0.35, 1.05, 0]))
  return g.add(self._mid(0.95, "要讓每個投影都線性",
                         "for every projection to come out linear",
                         DIM, FS_TAG, x=3.95, w=4.3),
               self._mid(-0.70, "和在 j 的值就只能是這個",
                         "the value at j has only one possible choice",
                         ACCENT_A, FS_TAG, x=3.95, w=4.3),
               self._mid(-1.55, "數乘也一樣，整組運算就被逼出來了",
                         "the same for scalars, so the whole operation is forced",
                         DIM, FS_TAG, w=11.4))

 def _unique(self):
  """One admissible operation, several rejected: the theorem is a uniqueness
  claim and the picture says so."""
  g = VGroup(Rectangle(width=3.10, height=0.80, color=DIM, stroke_width=2.5)
             .move_to([-3.45, 0.90, 0]),
             self._mid(0.90, "所有投影都線性", "all projections linear",
                       DIM, FS_TAG, x=-3.45, w=2.85))
  for k, (dy, ok) in enumerate(((0.15, True), (-0.55, False), (-1.25, False))):
   col = ACCENT_A if ok else WARN
   g.add(self._arr([-3.45, 0.46, 0], [-0.95, dy + 0.10, 0], DIM, sw=1.8, tl=0.09)
         if k == 0 else VGroup(),
         Rectangle(width=2.70, height=0.54, color=col, stroke_width=2.5).move_to([0.55, dy, 0]),
         self._mid(dy, "一組運算", "an operation", col, FS_TAG, x=0.55, w=2.45))
   if not ok:
    g.add(Line([-0.85, dy - 0.24, 0], [1.95, dy + 0.24, 0], color=WARN, stroke_width=3))
  return g.add(self._mid(0.90, "只有一組活下來", "only one survives",
                         ACCENT_A, FS_TAG, x=3.85, w=4.1),
               self._mid(0.10, "其他的都不滿足要求", "the rest fail the requirement",
                         WARN, FS_TAG, x=3.85, w=4.1),
               self._mid(-1.72, "證明就是把之前的公理檢查原封不動再走一遍",
                         "the proof is the earlier axiom check, verbatim",
                         DIM, FS_TAG, w=11.4))

 # ── beats 6-10: Hom ──────────────────────────────────────────────
 def _hom(self):
  cx, cy = -2.70, 0.05
  g = VGroup(Ellipse(width=5.20, height=2.35, color=DIM, stroke_width=2.5).move_to([cx, cy, 0]),
             Ellipse(width=2.90, height=1.45, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.13).move_to([cx - 0.55, cy, 0]))
  rng = np.random.default_rng(5)
  for _ in range(9):
   a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0.25, 0.95)
   g.add(Dot([cx - 0.55 + r * np.cos(a) * 1.15, cy + r * np.sin(a) * 0.55, 0],
             radius=0.055, color=ACCENT_A))
  for _ in range(7):
   a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0.55, 1.0)
   x = cx + r * np.cos(a) * 2.35
   if abs(x - (cx - 0.55)) < 1.55: x += 1.95
   g.add(Dot([min(x, cx + 2.35), cy + r * np.sin(a) * 1.05, 0], radius=0.05, color=DIM))
  g.add(Text("Wⱽ", font_size=FS_TAG, color=DIM).move_to([cx + 2.05, cy + 0.92, 0]),
        Text("Hom", font_size=FS_TAG, color=ACCENT_A).move_to([cx - 0.55, cy + 0.92, 0]))
  return g.add(self._mid(0.85, "所有從 V 到 W 的映射", "all mappings from V to W",
                         DIM, FS_TAG, x=3.55, w=4.9),
               self._mid(0.05, "裡面線性的那些", "the linear ones among them",
                         ACCENT_A, FS_TAG, x=3.55, w=4.9),
               self._mid(-0.75, "就寫成 Hom", "are what we call Hom",
                         DIM, FS_TAG, x=3.55, w=4.9),
               self._mid(-1.55, "定義域本身是向量空間時，才值得這樣挑出來",
                         "worth singling out only when the domain is itself a vector space",
                         DIM, FS_TAG, w=11.6))

 def _subspace(self):
  """Two linear maps added: the sum sends the parallelogram to a
  parallelogram too, which is what closure means here."""
  u, v = np.array([0.92, 0.26, 0.0]), np.array([0.26, 0.86, 0.0])
  MS = np.array([[0.80, 0.36, 0], [-0.28, 0.72, 0], [0, 0, 1]])
  MT = np.array([[0.42, -0.52, 0], [0.60, 0.34, 0], [0, 0, 1]])
  g = VGroup()
  for ox, M, lab, col in ((-4.30, MS, "S", ACCENT_B), (-1.35, MT, "T", ACCENT_C),
                          (2.35, MS + MT, "S + T", ACCENT_A)):
   o = np.array([ox, -0.55, 0.0])
   a, b = M @ u, M @ v
   g.add(self._arr(o, o + a, col, sw=2.5, tl=0.12),
         self._arr(o, o + b, col, sw=2.5, tl=0.12),
         self._arr(o, o + a + b, col, sw=3.5, tl=0.16),
         self._dash(o + a, o + a + b, GHOST, n=6),
         self._dash(o + b, o + a + b, GHOST, n=6),
         Dot(o, radius=0.05, color=INK),
         self._mid(1.05, lab, lab, col, FS_TAG, x=ox + 0.55, w=1.8))
  g.add(Text("+", font_size=FS_TAG + 6, color=DIM).move_to([-0.10, -0.10, 0]),
        Text("=", font_size=FS_TAG + 6, color=DIM).move_to([1.30, -0.10, 0]))
  return g.add(self._mid(-1.55, "兩個線性映射相加還是線性，數乘也是，而且零變換在裡面",
                         "the sum of two linear maps is linear, so is a multiple, and zero is in",
                         DIM, FS_TAG, w=11.8))

 def _compose(self):
  xs = (-4.10, -0.90, 2.30)
  labs = ("V", "W", "X")
  cols = (ACCENT_B, ACCENT_C, ACCENT_A)
  g = VGroup()
  for x, lab, col in zip(xs, labs, cols):
   g.add(Ellipse(width=1.85, height=1.90, color=col, stroke_width=2.5,
                 fill_color=col, fill_opacity=0.08).move_to([x, 0.15, 0]),
         Text(lab, font_size=FS_TAG + 2, color=col).move_to([x, 1.16, 0]))
  for k, (a, b, lab) in enumerate(((0, 1, "T"), (1, 2, "S"))):
   g.add(self._arr([xs[a] + 1.00, 0.15, 0], [xs[b] - 1.00, 0.15, 0],
                   ACCENT_A, sw=3, tl=0.15),
         Text(lab, font_size=FS_TAG, color=ACCENT_A)
         .move_to([(xs[a] + xs[b]) / 2, 0.50, 0]))
  g.add(self._arr([xs[0], -1.38, 0], [xs[2], -1.38, 0], ACCENT_C, sw=3.5, tl=0.17),
        Text("S ∘ T", font_size=FS_TAG, color=ACCENT_C).move_to([xs[1], -1.12, 0]))
  return g.add(self._mid(-1.78, "很基本，但需要定義域與上域對得上",
                         "elementary, but it needs the domains and codomains to match",
                         DIM, FS_TAG, w=11.6))

 def _distrib(self):
  """Two parallel routes reaching the same place: composition distributes."""
  g = VGroup()
  ox = -3.85
  for dy, lab, col in ((0.62, "S₁", ACCENT_B), (-0.62, "S₂", ACCENT_C)):
   g.add(Rectangle(width=0.95, height=0.52, color=col, stroke_width=2).move_to([ox + 2.15, dy, 0]),
         Text(lab, font_size=FS_TAG - 2, color=col).move_to([ox + 2.15, dy, 0]),
         self._arr([ox + 0.60, 0.0, 0], [ox + 1.62, dy, 0], DIM, sw=2, tl=0.10),
         self._arr([ox + 2.68, dy, 0], [ox + 3.70, 0.0, 0], DIM, sw=2, tl=0.10))
  g.add(Rectangle(width=0.95, height=0.52, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox, 0.0, 0]),
        Text("T", font_size=FS_TAG - 1, color=ACCENT_A).move_to([ox, 0.0, 0]),
        Rectangle(width=1.35, height=0.52, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 4.45, 0.0, 0]),
        Text("Σ", font_size=FS_TAG + 3, color=ACCENT_A).move_to([ox + 4.45, 0.0, 0]))
  return g.add(self._mid(0.95, "先分開合成再加起來", "compose separately, then add",
                         DIM, FS_TAG, x=3.55, w=4.6),
               self._mid(0.05, "跟先加起來再合成一樣", "is the same as adding first",
                         ACCENT_A, FS_TAG, x=3.55, w=4.6),
               self._mid(-1.55, "另一邊也成立，而且合成與純量乘法可以交換次序",
                         "it holds on the other side too, and commutes with scalars",
                         DIM, FS_TAG, w=11.6))

 def _corollary(self):
  ax, bx = -2.45, 1.75
  ys = (0.72, 0.16, -0.40, -0.96)
  g = VGroup(self._mid(1.10, "Hom ( W , X )", "Hom ( W , X )", ACCENT_B, FS_TAG, x=ax, w=3.2),
             self._mid(1.10, "Hom ( V , X )", "Hom ( V , X )", ACCENT_A, FS_TAG, x=bx, w=3.2))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  g.add(Text("∘ T", font_size=FS_TAG, color=DIM).move_to([(ax + bx) / 2, 1.10, 0]))
  return g.add(self._mid(0.60, "這個對應本身是線性的", "the correspondence is itself linear",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-0.45, "T 是同構時它也是", "and an isomorphism when T is",
                         ACCENT_A, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.55, "因為拿 T 的反函數去合成就能還原",
                         "because composing with the inverse of T undoes it",
                         DIM, FS_TAG, w=11.6))

 def stage(self):
  sw, dw, sp = self._same_w(), self._diff_w(), self._sphere()
  pr, fo, un = self._projection(), self._forced(), self._unique()
  hm, su = self._hom(), self._subspace()
  cp, di, co = self._compose(), self._distrib(), self._corollary()

  return [([sw], []), ([dw], [sw]), ([sp], [dw]), ([pr], [sp]),
          ([fo], [pr]), ([un], [fo]), ([hm], [un]), ([su], [hm]),
          ([cp], [su]), ([di], [cp]), ([co], [di])]


AdvCalcE11ZH, AdvCalcE11EN = make(AdvCalcE11Base, "11", prefix="AdvCalcE")
