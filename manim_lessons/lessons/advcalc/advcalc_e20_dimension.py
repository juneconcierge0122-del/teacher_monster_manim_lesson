"""advcalc E20 — Chapter 2, section 2 (book pp. 77-81): dimension, Theorems
2.1 to 2.5, and the dimensional identities.

Beat 9 is the one that rewards a picture: the identity relating the dimensions
of a sum and an intersection is false if you guess it by adding, and the two
planes meeting in a line show why the intersection has to be subtracted back
out. The counts are computed from the drawn objects rather than asserted.
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


class AdvCalcE20Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 20

 MODE_LABEL = {
  0: {"zh": "兩組基底，個數永遠一樣", "en": "two bases, always the same count"},
  1: {"zh": "同構，若且唯若維數相同", "en": "isomorphic exactly when the dimensions agree"},
  2: {"zh": "有限維上，滿的就是同構", "en": "on a finite-dimensional space, onto means iso"},
  3: {"zh": "假設一組比較少", "en": "suppose one basis were smaller"},
  4: {"zh": "投影不可能是同構", "en": "that projection cannot be an isomorphism"},
  5: {"zh": "座標空間確實是 n 維的", "en": "coordinate n-space really is n-dimensional"},
  6: {"zh": "維數把一切講完了", "en": "the dimension tells the whole story"},
  7: {"zh": "子空間也是有限維", "en": "a subspace is finite-dimensional too"},
  8: {"zh": "所以每個子空間都有補空間", "en": "so every subspace has a complement"},
  9: {"zh": "交集要扣回來", "en": "the intersection has to be subtracted back"},
  10: {"zh": "零空間加值域，等於定義域", "en": "null space plus range is the domain"},
 }

 def _same_count(self):
  g = VGroup()
  for cy, n, col, lab in ((0.72, 4, ACCENT_B, "基底一"), (-0.25, 4, ACCENT_C, "基底二")):
   for k in range(n):
    x = -3.65 + k * 0.86
    g.add(Rectangle(width=0.66, height=0.50, color=col, stroke_width=2).move_to([x, cy, 0]),
          Dot([x, cy, 0], radius=0.05, color=col))
   g.add(Text(str(n), font_size=FS_TAG + 3, color=col).move_to([-0.55, cy, 0]))
  g.add(Text("=", font_size=FS_TAG + 5, color=ACCENT_A).move_to([-0.55, 0.24, 0]))
  return g.add(self._mid(0.72, "同一個空間的一組基底", "one basis for the space",
                         ACCENT_B, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.25, "另一組基底", "and another basis",
                         ACCENT_C, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.15, "元素個數永遠一樣——維數這個概念，靠的就是這件事",
                         "always the same number of elements: dimension rests on that",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "這個共同的個數，就叫 V 的維數",
                         "and that common number is called the dimension",
                         DIM, FS_TAG, w=11.6))

 def _iso_iff(self):
  ax, bx = -2.75, 1.95
  g = VGroup(Ellipse(width=2.20, height=1.75, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.10).move_to([ax, 0.35, 0]),
             Ellipse(width=2.20, height=1.75, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.10).move_to([bx, 0.35, 0]),
             Text("d = n", font_size=FS_TAG, color=ACCENT_B).move_to([ax, 0.35, 0]),
             Text("d = n", font_size=FS_TAG, color=ACCENT_A).move_to([bx, 0.35, 0]),
             self._arr([ax + 1.20, 0.55, 0], [bx - 1.20, 0.55, 0], ACCENT_A, sw=3, tl=0.15),
             self._arr([bx - 1.20, 0.15, 0], [ax + 1.20, 0.15, 0], ACCENT_B, sw=3, tl=0.15),
             Text("≅", font_size=FS_TAG + 4, color=ACCENT_A).move_to([-0.40, 0.88, 0]))
  return g.add(self._mid(-0.95, "有同構，若且唯若維數相同",
                         "an isomorphism exists exactly when the dimensions agree",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.78, "所以維數把 V 的一切都講完了，只差到同構為止",
                         "so the dimension tells all there is to know, to within isomorphism",
                         DIM, FS_TAG, w=11.8))

 def _lemma21(self):
  cx = -2.85
  g = VGroup(Ellipse(width=2.60, height=2.00, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.08).move_to([cx, 0.25, 0]),
             Text("V", font_size=FS_TAG + 1, color=ACCENT_B).move_to([cx, 1.05, 0]))
  for k in range(3):
   y = 0.55 - k * 0.50
   g.add(Dot([cx - 0.60, y, 0], radius=0.07, color=ACCENT_A),
         Dot([cx + 0.60, y, 0], radius=0.07, color=ACCENT_C),
         self._arr([cx - 0.44, y, 0], [cx + 0.44, y, 0], DIM, sw=1.8, tl=0.09))
  return g.add(self._mid(0.95, "取能生成 V 的最少個數", "take the fewest elements that span V",
                         DIM, FS_TAG, x=3.05, w=5.6),
               self._mid(0.05, "那組生成集就是基底", "that spanning set is a basis",
                         ACCENT_B, FS_TAG, x=3.05, w=5.6),
               self._mid(-0.85, "T 是滿的，所以像也生成", "T is onto, so the images span too",
                         ACCENT_C, FS_TAG, x=3.05, w=5.6),
               self._mid(-1.78, "於是像也是基底，T 就是同構",
                         "so the images are a basis as well, and T is an isomorphism",
                         ACCENT_A, FS_TAG, w=11.8))

 def _suppose(self):
  g = VGroup()
  boxes = ((-3.85, "ℝⁿ", ACCENT_B), (-0.35, "V", ACCENT_A), (3.05, "ℝᵐ", ACCENT_C))
  for x, lab, col in boxes:
   g.add(Rectangle(width=1.50, height=0.80, color=col, stroke_width=2.5).move_to([x, 0.55, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([x, 0.55, 0]))
  g.add(self._arr([-3.05, 0.55, 0], [-1.15, 0.55, 0], ACCENT_B, sw=3, tl=0.15),
        Text("θ", font_size=FS_TAG, color=ACCENT_B).move_to([-2.10, 0.90, 0]),
        self._arr([2.25, 0.55, 0], [0.45, 0.55, 0], ACCENT_C, sw=3, tl=0.15),
        Text("φ", font_size=FS_TAG, color=ACCENT_C).move_to([1.35, 0.90, 0]),
        Rectangle(width=3.20, height=0.62, color=WARN, stroke_width=2.5).move_to([-0.35, -0.55, 0]),
        Text("m  <  n", font_size=FS_TAG + 2, color=WARN).move_to([-0.35, -0.55, 0]))
  return g.add(self._mid(-1.30, "假設有一組基底比另一組少",
                         "suppose one basis had fewer elements than another",
                         WARN, FS_TAG, w=11.6),
               self._mid(-1.78, "接著把大的那個座標空間拆成兩塊，造一個往小的那塊的投影",
                         "then split the larger coordinate space and build a projection onto the smaller",
                         DIM, FS_TAG, w=11.9))

 def _contradiction(self):
  g = VGroup()
  ox = -3.55
  for k in range(5):
   on = k < 3
   g.add(Rectangle(width=0.66, height=0.50, color=ACCENT_A if on else GHOST, stroke_width=2)
         .move_to([ox + k * 0.80, 0.72, 0]),
         Text("x" + "₁₂₃₄₅"[k], font_size=FS_TAG - 3, color=ACCENT_A if on else GHOST)
         .move_to([ox + k * 0.80, 0.72, 0]))
  g.add(Rectangle(width=2.30, height=0.66, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 0.80, 0.72, 0]),
        self._arr([ox + 1.60, 0.38, 0], [ox + 1.60, -0.05, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._mid(-0.38, "π 是投影", "π is the projection", ACCENT_A, FS_TAG, x=ox + 1.60, w=3.4),
        Rectangle(width=4.10, height=0.62, color=WARN, stroke_width=2.5).move_to([1.85, -1.15, 0]),
        Text("π ( δ ⁿ )  =  0", font_size=FS_TAG + 1, color=WARN).move_to([1.85, -1.15, 0]))
  return g.add(self._mid(0.72, "π 可以寫成兩個同構的合成", "π is a composition of two isomorphisms",
                         DIM, FS_TAG, x=2.85, w=5.6),
               self._mid(-0.05, "所以 π 自己也是同構", "so π is an isomorphism itself",
                         ACCENT_A, FS_TAG, x=2.85, w=5.6),
               self._mid(-1.78, "可是它把最後一個標準基底向量送到零——矛盾",
                         "but it carries the last standard basis vector to zero, a contradiction",
                         WARN, FS_TAG, w=11.9))

 def _dim_n(self):
  ox = -3.35
  g = VGroup()
  for k in range(4):
   x = ox + k * 1.00
   g.add(Rectangle(width=0.80, height=0.55, color=ACCENT_A, stroke_width=2).move_to([x, 0.55, 0]),
         Text(f"δ{'¹²³ⁿ'[k]}", font_size=FS_TAG - 2, color=ACCENT_A).move_to([x, 0.55, 0]))
   if k == 2:
    g.add(Text("…", font_size=FS_TAG, color=DIM).move_to([x + 0.50, 0.55, 0]))
  g.add(Rectangle(width=4.10, height=0.85, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 1.50, 0.55, 0]),
        Text("n", font_size=FS_TAG + 4, color=ACCENT_A).move_to([ox + 1.50, -0.35, 0]),
        self._arr([ox + 1.50, 0.10, 0], [ox + 1.50, -0.12, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.55, "標準基底有 n 個元素", "the standard basis has n elements",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.35, "所以座標空間是 n 維的", "so coordinate n-space is n-dimensional",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.78, "在這個精確的意義下——每組基底個數相同，所以這個數字有意義",
                         "in this precise sense: every basis has that count, so the number means something",
                         DIM, FS_TAG, w=11.9))

 def _corollary(self):
  g = VGroup()
  for cx, zh, en, col in ((-3.05, "維數相同", "same dimension", ACCENT_B),
                          (3.05, "同構", "isomorphic", ACCENT_A)):
   g.add(Rectangle(width=3.80, height=0.95, color=col, stroke_width=2.5).move_to([cx, 0.45, 0]),
         self._mid(0.45, zh, en, col, FS_TAG + 1, x=cx, w=3.5))
  g.add(self._arr([-1.05, 0.65, 0], [1.05, 0.65, 0], ACCENT_A, sw=3, tl=0.15),
        self._arr([1.05, 0.25, 0], [-1.05, 0.25, 0], ACCENT_B, sw=3, tl=0.15))
  return g.add(self._mid(-0.75, "一邊是因為同構把基底送到基底、個數不變",
                         "one way because an isomorphism carries a basis to one of the same size",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.32, "另一邊是因為兩個都同構於同一個座標空間",
                         "the other because both are isomorphic to the same coordinate space",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.76, "所以維數是有限維空間的完整不變量",
                         "so dimension is a complete invariant for these spaces",
                         ACCENT_A, FS_TAG, w=11.6))

 def _subspace_fd(self):
  cx = -2.75
  g = VGroup(Ellipse(width=4.60, height=2.05, color=DIM, stroke_width=2.5).move_to([cx, 0.15, 0]),
             Ellipse(width=2.60, height=1.35, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.12).move_to([cx - 0.70, 0.15, 0]),
             Text("V", font_size=FS_TAG, color=DIM).move_to([cx + 1.85, 0.95, 0]),
             Text("M", font_size=FS_TAG, color=ACCENT_A).move_to([cx - 0.70, 0.15, 0]))
  for k, x in enumerate((-1.55, -0.85, -0.15)):
   g.add(Dot([cx + x, -0.30, 0], radius=0.06, color=ACCENT_B))
  return g.add(self._mid(0.85, "M 裡的有限獨立子集", "the finite independent subsets of M",
                         ACCENT_B, FS_TAG, x=3.05, w=5.6),
               self._mid(0.00, "每個都能擴充成 V 的基底", "each extends to a basis for V",
                         DIM, FS_TAG, x=3.05, w=5.6),
               self._mid(-0.85, "所以個數有上界", "so their sizes are bounded",
                         ACCENT_A, FS_TAG, x=3.05, w=5.6),
               self._mid(-1.78, "取個數最大的那個，它的線性擴張就是整個 M",
                         "take one of maximum size and its span is the whole of M",
                         DIM, FS_TAG, w=11.8))

 def _complement(self):
  ox = -3.55
  g = VGroup()
  for k in range(5):
   inM = k < 2
   g.add(Rectangle(width=0.72, height=0.52, color=ACCENT_A if inM else ACCENT_C, stroke_width=2)
         .move_to([ox + k * 0.86, 0.62, 0]))
  g.add(Rectangle(width=1.90, height=0.78, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 0.43, 0.62, 0]),
        Rectangle(width=2.72, height=0.78, color=ACCENT_C, stroke_width=2.5)
        .move_to([ox + 3.01, 0.62, 0]),
        self._mid(-0.30, "M 的基底", "a basis for M", ACCENT_A, FS_TAG, x=ox + 0.43, w=1.9),
        self._mid(-0.30, "多出來的那些", "the added vectors", ACCENT_C, FS_TAG, x=ox + 3.01, w=2.7))
  return g.add(self._mid(0.62, "把 M 的基底擴充成 V 的基底",
                         "extend a basis for M to a basis for V",
                         DIM, FS_TAG, x=3.55, w=4.7),
               self._mid(-1.15, "多出來那些的線性擴張，就是一個補空間",
                         "the span of the added vectors is a complement",
                         ACCENT_C, FS_TAG, w=11.6),
               self._mid(-1.78, "所以有限維空間的每一個子空間都有補空間",
                         "so every subspace of a finite-dimensional space has one",
                         ACCENT_A, FS_TAG, w=11.6))

 def _identity(self):
  """Two planes in three-space meeting in a line. The counts are read off the
  drawn objects: two plus two is four, but the sum is only three-dimensional,
  and the line that was counted twice is exactly the difference."""
  org = np.array([-2.75, -0.35, 0.0])
  s = 0.78
  dU, dW = 2, 2
  dSum, dInt = 3, 1
  assert dU + dW == dSum + dInt, "the identity has to balance on the drawn example"
  q1 = [_p(np.array([sx * 1.25, sy * 1.15, 0.0]), org, s)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  q2 = [_p(np.array([sx * 1.25, 0.0, sy * 1.15]), org, s)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  g = VGroup(Polygon(*q1, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.13),
             Polygon(*q2, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.13),
             Line(_p(np.array([-1.25, 0, 0]), org, s), _p(np.array([1.25, 0, 0]), org, s),
                  color=ACCENT_A, stroke_width=4),
             Dot(_p(np.zeros(3), org, s), radius=0.06, color=INK))
  return g.add(self._mid(1.05, f"兩個平面，各 {dU} 維", f"two planes, each of dimension {dU}",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(0.15, f"和是 {dSum} 維，交集是 {dInt} 維",
                         f"the sum is {dSum}-dimensional, the intersection {dInt}",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.75, f"{dU} 加 {dW} 是 {dU + dW}，不是 {dSum}",
                         f"{dU} plus {dW} is {dU + dW}, not {dSum}",
                         WARN, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.78, "交集被算了兩次，所以要扣回來——這就是那條等式",
                         "the intersection was counted twice, and subtracting it back is the identity",
                         ACCENT_A, FS_TAG, w=11.9))

 def _rank_nullity(self):
  g = VGroup(Rectangle(width=4.30, height=0.72, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.15, 0.85, 0]),
             Text("d ( N )  +  d ( R )  =  d ( V )", font_size=FS_TAG + 1, color=ACCENT_A)
             .move_to([-2.15, 0.85, 0]))
  ox = -4.05
  for k in range(5):
   col = ACCENT_B if k < 2 else ACCENT_C
   g.add(Rectangle(width=0.66, height=0.50, color=col, stroke_width=2).move_to([ox + k * 0.80, 0.02, 0]))
  g.add(Rectangle(width=1.75, height=0.74, color=ACCENT_B, stroke_width=2.5).move_to([ox + 0.40, 0.02, 0]),
        Rectangle(width=2.55, height=0.74, color=ACCENT_C, stroke_width=2.5).move_to([ox + 2.80, 0.02, 0]),
        self._mid(-0.62, "零空間", "null space", ACCENT_B, FS_TAG, x=ox + 0.40, w=1.7),
        self._mid(-0.62, "值域", "range", ACCENT_C, FS_TAG, x=ox + 2.80, w=2.5))
  return g.add(self._mid(0.85, "維數等式", "the dimensional identity",
                         ACCENT_A, FS_TAG, x=3.55, w=4.5),
               self._mid(-0.30, "上域維數相同時", "when the codomain matches",
                         DIM, FS_TAG, x=3.55, w=4.5),
               self._mid(-1.30, "嵌射、滿射、雙射三件事完全等價",
                         "injectivity, surjectivity and bijectivity are all equivalent",
                         ACCENT_A, FS_TAG, w=11.8),
               self._mid(-1.76, "最後：所有線性映射所成空間的維數，是兩邊維數的乘積",
                         "last: the space of all linear maps has dimension the product",
                         DIM, FS_TAG, w=11.8))

 def stage(self):
  sc, ii, l21 = self._same_count(), self._iso_iff(), self._lemma21()
  su, co, dn = self._suppose(), self._contradiction(), self._dim_n()
  cr, sf, cp = self._corollary(), self._subspace_fd(), self._complement()
  idt, rn = self._identity(), self._rank_nullity()
  return [([sc], []), ([ii], [sc]), ([l21], [ii]), ([su], [l21]),
          ([co], [su]), ([dn], [co]), ([cr], [dn]), ([sf], [cr]),
          ([cp], [sf]), ([idt], [cp]), ([rn], [idt])]


AdvCalcE20ZH, AdvCalcE20EN = make(AdvCalcE20Base, "20", prefix="AdvCalcE")
