"""advcalc E19 — Chapter 2, section 1, second half (book pp. 74-77): Theorems
1.3 to 1.6, and infinite bases.

Beat 7 carries the proof of the existence theorem, which is a round trip:
translate the vector into coordinates against the old basis, then rebuild it
against the new tuple. Drawn as a path through coordinate space, because that
detour is the whole argument and the formula bar shows only its endpoints.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE19Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 19

 MODE_LABEL = {
  0: {"zh": "同構把基底送到基底", "en": "an isomorphism carries a basis to a basis"},
  1: {"zh": "像就是它的 skeleton", "en": "the images are its skeleton"},
  2: {"zh": "反過來也對", "en": "and the converse holds"},
  3: {"zh": "互補子空間的基底，聯集起來", "en": "bases of complements, taken together"},
  4: {"zh": "拆成兩邊，兩邊都得是零", "en": "split it in two, and both halves vanish"},
  5: {"zh": "直和也一樣", "en": "and the same for a direct sum"},
  6: {"zh": "指定基底的像，映射就唯一", "en": "name the images of a basis, and the map is unique"},
  7: {"zh": "先翻成座標，再照新的組回去", "en": "into coordinates, then rebuilt"},
  8: {"zh": "那個映射怎麼隨元組變化？", "en": "how does that map vary with the tuple?"},
  9: {"zh": "線性地，而且是同構地", "en": "linearly, and isomorphically"},
  10: {"zh": "無限基底", "en": "infinite bases"},
 }

 def _carry(self):
  ax, bx = -3.20, 1.85
  ys = (0.72, 0.16, -0.40)
  g = VGroup(Ellipse(width=2.10, height=2.05, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.08).move_to([ax, 0.16, 0]),
             Ellipse(width=2.10, height=2.05, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.08).move_to([bx, 0.16, 0]),
             Text("V", font_size=FS_TAG, color=ACCENT_B).move_to([ax, 1.18, 0]),
             Text("W", font_size=FS_TAG, color=ACCENT_A).move_to([bx, 1.18, 0]))
  for y in ys:
   g.add(Dot([ax - 0.30, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx - 0.30, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.20, y, 0], [bx - 0.80, y, 0], DIM, sw=1.8, tl=0.09))
  g.add(Text("T", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-0.68, 0.55, 0]))
  return g.add(self._mid(-1.25, "T 是同構時，基底的像還是基底",
                         "when T is an isomorphism, the images of a basis are a basis",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.75, "這是後面幾條結論的起點",
                         "which is where the next few conclusions start",
                         DIM, FS_TAG, w=11.6))

 def _skeleton(self):
  g = VGroup()
  boxes = ((-4.00, "ℝⁿ", ACCENT_C), (-0.65, "V", ACCENT_B), (2.70, "W", ACCENT_A))
  for x, lab, col in boxes:
   g.add(Rectangle(width=1.50, height=0.80, color=col, stroke_width=2.5).move_to([x, 0.45, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([x, 0.45, 0]))
  g.add(self._arr([-3.20, 0.45, 0], [-1.45, 0.45, 0], ACCENT_B, sw=3, tl=0.15),
        Text("L α", font_size=FS_TAG - 1, color=ACCENT_B).move_to([-2.32, 0.82, 0]),
        self._arr([0.15, 0.45, 0], [1.90, 0.45, 0], ACCENT_A, sw=3, tl=0.15),
        Text("T", font_size=FS_TAG - 1, color=ACCENT_A).move_to([1.02, 0.82, 0]),
        self._arr([-4.00, -0.05, 0], [2.70, -0.05, 0], ACCENT_C, sw=3.5, tl=0.17),
        Text("T ∘ L α", font_size=FS_TAG, color=ACCENT_C).move_to([-0.65, -0.42, 0]))
  return g.add(self._mid(-1.25, "兩個同構接起來，還是同構",
                         "an isomorphism after an isomorphism is again one",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.75, "而它的 skeleton 正好就是那些像",
                         "and its skeleton is exactly the family of images",
                         ACCENT_C, FS_TAG, w=11.6))

 def _converse(self):
  ox = -3.75
  g = VGroup()
  for k in range(3):
   x = ox + k * 1.05
   g.add(Rectangle(width=0.86, height=0.52, color=ACCENT_C, stroke_width=2)
         .move_to([x, 0.62, 0]),
         Text(f"δ{'¹²³'[k]}", font_size=FS_TAG - 2, color=ACCENT_C).move_to([x, 0.62, 0]),
         self._arr([x, 0.28, 0], [x, -0.20, 0], DIM, sw=2, tl=0.10),
         Rectangle(width=0.86, height=0.52, color=ACCENT_B, stroke_width=2)
         .move_to([x, -0.52, 0]),
         Text(f"α{k + 1}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, -0.52, 0]))
  g.add(Text("θ", font_size=FS_TAG, color=ACCENT_A).move_to([ox - 0.55, 0.05, 0]))
  return g.add(self._mid(0.62, "任何一個從座標空間來的同構",
                         "any isomorphism out of coordinate space",
                         DIM, FS_TAG, x=2.85, w=5.6),
               self._mid(-0.52, "作用在標準基底上，就得到一組基底",
                         "applied to the standard basis gives a basis",
                         ACCENT_B, FS_TAG, x=2.85, w=5.6),
               self._mid(-1.72, "所以基底與「從座標空間來的同構」是同一件事",
                         "so a basis and an isomorphism out of coordinate space are the same thing",
                         ACCENT_A, FS_TAG, w=11.9))

 ORG = np.array([-2.85, -0.35, 0.0])
 S = 0.80
 LDIR = np.array([0.32, 0.42, 1.15])

 def _plane(self, color=ACCENT_B, op=0.13, half=1.25):
  quad = [np.array([sx * half, sy * half, 0.0]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  return Polygon(*[_p(v, self.ORG, self.S) for v in quad], color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=op)

 def _union(self):
  assert abs(float(self.LDIR[2])) > 0.4, "the complement must leave the plane"
  o3 = _p(np.zeros(3), self.ORG, self.S)
  g = VGroup(self._plane(), Dot(o3, radius=0.06, color=INK),
             Line(_p(-0.85 * self.LDIR, self.ORG, self.S),
                  _p(1.05 * self.LDIR, self.ORG, self.S), color=ACCENT_A, stroke_width=3.5))
  for v, col in ((np.array([0.95, -0.55, 0.0]), ACCENT_B),
                 (np.array([0.22, 0.95, 0.0]), ACCENT_B),
                 (0.78 * self.LDIR, ACCENT_A)):
   g.add(self._arr(o3, _p(v, self.ORG, self.S), col, sw=3, tl=0.14))
  g.add(Text("X", font_size=FS_TAG, color=ACCENT_B)
        .move_to(_p(np.array([-1.05, 1.05, 0]), self.ORG, self.S)),
        Text("Y", font_size=FS_TAG, color=ACCENT_A)
        .move_to(_p(1.05 * self.LDIR, self.ORG, self.S) + np.array([0.26, 0.10, 0])))
  return g.add(self._mid(1.05, "X 的基底，加上 Y 的基底", "a basis for X and a basis for Y",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(0.10, "聯集起來就是 V 的基底", "together are a basis for V",
                         ACCENT_A, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.72, "反過來，把一組基底分成兩份，兩份的擴張就互補",
                         "conversely, partition a basis and the two spans are complementary",
                         DIM, FS_TAG, w=11.8))

 def _split_proof(self):
  g = VGroup()
  ox = -3.15
  for k, (lab, col) in enumerate((("Σ𝘑 xᵢ αᵢ", ACCENT_B), ("Σ𝘒 xᵢ αᵢ", ACCENT_A))):
   g.add(Rectangle(width=2.30, height=0.60, color=col, stroke_width=2.5)
         .move_to([ox + k * 2.60, 0.72, 0]),
         Text(lab, font_size=FS_TAG - 1, color=col).move_to([ox + k * 2.60, 0.72, 0]),
         self._arr([ox + k * 2.60, 0.36, 0], [ox + k * 2.60, -0.10, 0], DIM, sw=2, tl=0.10),
         Rectangle(width=1.10, height=0.56, color=col, stroke_width=2.5)
         .move_to([ox + k * 2.60, -0.42, 0]),
         Text("0", font_size=FS_TAG + 1, color=col).move_to([ox + k * 2.60, -0.42, 0]))
  g.add(Text("+", font_size=FS_TAG + 4, color=DIM).move_to([ox + 1.30, 0.72, 0]),
        Text("=  0", font_size=FS_TAG + 2, color=DIM).move_to([ox + 5.05, 0.72, 0]))
  return g.add(self._mid(-1.05, "一半落在 X、一半落在 Y，而 X 與 Y 只交於零",
                         "one half lies in X and one in Y, and they meet only at zero",
                         DIM, FS_TAG, w=11.8),
               self._mid(-1.72, "所以兩邊都是零，於是每個係數都是零",
                         "so both are zero, and then every coefficient is zero",
                         ACCENT_A, FS_TAG, w=11.6))

 def _direct_sum(self):
  g = VGroup()
  for k, (x, col) in enumerate(((-3.55, ACCENT_B), (-1.85, ACCENT_C), (-0.15, WARN))):
   g.add(Rectangle(width=1.45, height=1.05, color=col, stroke_width=2.5).move_to([x, 0.45, 0]),
         Text(f"B{k + 1}", font_size=FS_TAG - 2, color=col).move_to([x, 0.45, 0]))
   if k < 2:
    g.add(Text("∪", font_size=FS_TAG + 2, color=DIM).move_to([x + 0.85, 0.45, 0]))
  g.add(self._arr([0.70, 0.45, 0], [1.85, 0.45, 0], ACCENT_A, sw=3, tl=0.15),
        Rectangle(width=1.85, height=1.05, color=ACCENT_A, stroke_width=2.5)
        .move_to([2.85, 0.45, 0]),
        self._mid(0.45, "V 的基底", "a basis for V", ACCENT_A, FS_TAG, x=2.85, w=1.7))
  return g.add(self._mid(-0.75, "V 是一族子空間的直和時",
                         "when V is the direct sum of a family",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.72, "各個子空間的基底聯集起來，就是 V 的基底（用歸納推上去）",
                         "the union of their bases is a basis for V, by induction",
                         ACCENT_A, FS_TAG, w=11.9))

 def _exists(self):
  g = VGroup()
  ox = -3.65
  for k in range(3):
   y = 0.72 - k * 0.62
   g.add(Rectangle(width=0.92, height=0.50, color=ACCENT_B, stroke_width=2).move_to([ox, y, 0]),
         Text(f"β{k + 1}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([ox, y, 0]),
         self._arr([ox + 0.55, y, 0], [ox + 1.75, y, 0], ACCENT_A, sw=2, tl=0.10),
         Rectangle(width=0.92, height=0.50, color=ACCENT_C, stroke_width=2)
         .move_to([ox + 2.30, y, 0]),
         Text(f"α{k + 1}", font_size=FS_TAG - 2, color=ACCENT_C).move_to([ox + 2.30, y, 0]))
  g.add(Text("S", font_size=FS_TAG, color=ACCENT_A).move_to([ox + 1.15, 1.06, 0]))
  return g.add(self._mid(0.72, "給一組有序基底", "give an ordered basis",
                         ACCENT_B, FS_TAG, x=2.95, w=5.6),
               self._mid(0.10, "與 W 裡任意一個同長度的元組", "and any tuple of the same length in W",
                         ACCENT_C, FS_TAG, x=2.95, w=5.6),
               self._mid(-0.52, "就恰好有一個線性映射對上", "and exactly one linear map matches",
                         ACCENT_A, FS_TAG, x=2.95, w=5.6),
               self._mid(-1.72, "重點是「恰好一個」——存在與唯一都有",
                         "the point is exactly one: both existence and uniqueness",
                         DIM, FS_TAG, w=11.6))

 def _detour(self):
  g = VGroup()
  boxes = ((-3.55, "V", ACCENT_B), (-0.05, "ℝⁿ", ACCENT_C), (3.45, "W", ACCENT_A))
  for x, lab, col in boxes:
   g.add(Rectangle(width=1.50, height=0.80, color=col, stroke_width=2.5).move_to([x, 0.55, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([x, 0.55, 0]))
  g.add(self._arr([-2.75, 0.55, 0], [-0.85, 0.55, 0], ACCENT_C, sw=3, tl=0.15),
        Text("( L β ) ⁻¹", font_size=FS_TAG - 2, color=ACCENT_C).move_to([-1.80, 0.92, 0]),
        self._arr([0.75, 0.55, 0], [2.65, 0.55, 0], ACCENT_A, sw=3, tl=0.15),
        Text("L α", font_size=FS_TAG - 2, color=ACCENT_A).move_to([1.70, 0.92, 0]),
        self._arr([-3.55, -0.05, 0], [3.45, -0.05, 0], ACCENT_B, sw=3.5, tl=0.17),
        Text("S", font_size=FS_TAG + 1, color=ACCENT_B).move_to([-0.05, -0.42, 0]))
  return g.add(self._mid(-1.05, "先把向量翻成座標，再照新的元組組回去",
                         "translate the vector into coordinates, then rebuild against the new tuple",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.72, "會成立的關鍵，是基底同構可逆",
                         "what makes it work is that the basis isomorphism is invertible",
                         ACCENT_C, FS_TAG, w=11.6))

 def _varies(self):
  ax, bx = -2.75, 1.85
  ys = (0.72, 0.16, -0.40, -0.96)
  g = VGroup(self._mid(1.15, "Wⁿ 裡的元組", "tuples in Wⁿ", ACCENT_C, FS_TAG, x=ax, w=3.2),
             self._mid(1.15, "對應的那個 S", "the matching map S", ACCENT_A, FS_TAG, x=bx, w=3.2))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_C),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.35, "元組動，映射跟著動", "move the tuple, the map moves with it",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-0.60, "怎麼動？", "but how?", ACCENT_A, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.72, "答案是：線性地，而且是同構地",
                         "the answer is linearly, and in fact isomorphically",
                         ACCENT_A, FS_TAG, w=11.6))

 def _thm16(self):
  g = VGroup(Rectangle(width=2.60, height=0.80, color=ACCENT_C, stroke_width=2.5)
             .move_to([-3.05, 0.55, 0]),
             Text("Wⁿ", font_size=FS_TAG + 2, color=ACCENT_C).move_to([-3.05, 0.55, 0]),
             Rectangle(width=3.60, height=0.80, color=ACCENT_A, stroke_width=2.5)
             .move_to([2.35, 0.55, 0]),
             Text("Hom ( V , W )", font_size=FS_TAG, color=ACCENT_A).move_to([2.35, 0.55, 0]),
             self._arr([-1.65, 0.75, 0], [0.45, 0.75, 0], ACCENT_A, sw=3, tl=0.15),
             self._arr([0.45, 0.35, 0], [-1.65, 0.35, 0], ACCENT_C, sw=3, tl=0.15),
             Text("≅", font_size=FS_TAG + 5, color=ACCENT_A).move_to([-0.60, 1.05, 0]))
  return g.add(self._mid(-0.55, "固定 V 的一組有序基底之後",
                         "with an ordered basis for V held fixed",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.15, "這是一個同構", "this is an isomorphism",
                         ACCENT_A, FS_TAG, w=11.4),
               self._mid(-1.75, "證明就是把第一章那兩個同構合起來",
                         "the proof composes the two isomorphisms from chapter one",
                         DIM, FS_TAG, w=11.6))

 def _infinite(self):
  g = VGroup(Ellipse(width=5.00, height=2.00, color=DIM, stroke_width=2.5)
             .move_to([-2.35, 0.05, 0]),
             Ellipse(width=3.10, height=1.35, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.12).move_to([-3.00, 0.05, 0]),
             Text("ℝᴵ", font_size=FS_TAG, color=DIM).move_to([-0.55, 0.80, 0]),
             self._mid(0.05, "除了有限多個位置以外都是零",
                       "zero except at finitely many places",
                       ACCENT_A, FS_TAG, x=-3.00, w=2.9))
  return g.add(self._mid(0.85, "Kronecker 函數的定義照舊", "the Kronecker functions as before",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.75, "但它們只生成裡面那一塊", "but they span only the inner part",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.30, "用選擇公理可以證明每個向量空間都有基底",
                         "the axiom of choice gives every vector space a basis",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.78, "但這種無限基底在分析上不太好用，所以先專注在有限維",
                         "but such bases are of little use in analysis, so finite dimensions come first",
                         DIM, FS_TAG, w=11.9))

 def stage(self):
  ca, sk, cv = self._carry(), self._skeleton(), self._converse()
  un, sp, ds = self._union(), self._split_proof(), self._direct_sum()
  ex, dt, va, t16, inf = (self._exists(), self._detour(), self._varies(),
                          self._thm16(), self._infinite())
  return [([ca], []), ([sk], [ca]), ([cv], [sk]), ([un], [cv]),
          ([sp], [un]), ([ds], [sp]), ([ex], [ds]), ([dt], [ex]),
          ([va], [dt]), ([t16], [va]), ([inf], [t16])]


AdvCalcE19ZH, AdvCalcE19EN = make(AdvCalcE19Base, "19", prefix="AdvCalcE")
