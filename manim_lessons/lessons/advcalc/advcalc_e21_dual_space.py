"""advcalc E21 — Chapter 2, section 3 (book pp. 81-83): the dual space, dual
bases, Theorem 3.1, and the second conjugate space.

Beat 6 is the one that rewards a picture. That a space and its dual are
isomorphic but not naturally so is easy to state and easy to nod along to
without seeing anything. So the two isomorphisms are actually carried out on
one concrete vector in the plane, with two different bases, and the two
resulting functionals are evaluated on a test vector: they disagree. The
numbers on screen are computed from the bases rather than asserted.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Arrow, Dot, Ellipse, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


def _coords(alpha, basis):
 """Coordinates of a plane vector against an ordered basis, as a 2-tuple."""
 return tuple(np.linalg.solve(np.array(basis, dtype=float).T, np.array(alpha, dtype=float)))


def _theta(alpha, basis):
 """The functional that the basis-dependent isomorphism V -> V* attaches to
 alpha: expand alpha in the basis, then read those coordinates as coefficients
 against the dual basis. Returned as the row vector acting on standard
 coordinates, so that two bases can be compared on the same test vector."""
 c = np.array(_coords(alpha, basis), dtype=float)
 return c @ np.linalg.inv(np.array(basis, dtype=float).T)


class AdvCalcE21Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 21

 MODE_LABEL = {
  0: {"zh": "所有線性泛函所成的空間", "en": "the space of all linear functionals"},
  1: {"zh": "座標泛函構成對偶空間的基底", "en": "the coordinate functionals are a basis for the dual"},
  2: {"zh": "作用在第 i 個基底向量上", "en": "evaluate on the ith basis vector"},
  3: {"zh": "任何泛函都是它們的組合", "en": "every functional is a combination of them"},
  4: {"zh": "對偶基底，維數相同", "en": "the dual basis, and the same dimension"},
  5: {"zh": "三條式子的對稱", "en": "the symmetry of the three equations"},
  6: {"zh": "同構會隨基底改變", "en": "the isomorphism moves with the basis"},
  7: {"zh": "座標空間有標準同構", "en": "coordinate space has a standard one"},
  8: {"zh": "到第二共軛空間是自然的", "en": "to the second conjugate space it is natural"},
  9: {"zh": "非零向量上找得到不為零的泛函", "en": "a functional that does not vanish"},
  10: {"zh": "兩邊互為對偶", "en": "each is the dual of the other"},
 }

 def _dual_def(self):
  cx = -3.05
  g = VGroup(Ellipse(width=2.70, height=1.55, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.10).move_to([cx, 0.10, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([cx, 1.10, 0]),
             Line([0.35, -0.55, 0], [0.35, 0.95, 0], color=DIM, stroke_width=2.5),
             Text("ℝ", font_size=FS_TAG + 1, color=DIM).move_to([0.72, 0.90, 0]))
  for k, y in enumerate((0.48, 0.10, -0.28)):
   col = (ACCENT_A, ACCENT_C, ACCENT_B)[k]
   g.add(Dot([cx - 0.55, y, 0], radius=0.06, color=col),
         self._arr([cx + 1.45, y, 0], [0.20, 0.72 - k * 0.44, 0], col, sw=2, tl=0.10))
  return g.add(self._mid(0.75, "每一個線性泛函都把 V 送到實數",
                         "each linear functional carries V to the reals",
                         DIM, FS_TAG, x=3.55, w=4.7),
               self._mid(-0.15, "把它們全部收集起來", "collect all of them together",
                         ACCENT_A, FS_TAG, x=3.55, w=4.7),
               self._mid(-1.15, "得到的向量空間就是 V 的對偶空間，也叫共軛空間",
                         "the vector space that results is the dual, or conjugate, space",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "這一節全部假設有限維——好處正是沒有連續性那層麻煩",
                         "this section assumes finite dimensions: the blessing is one fewer complication",
                         DIM, FS_TAG, w=11.9))

 def _thm31(self):
  ox = -3.75
  g = VGroup()
  for k in range(4):
   x = ox + k * 1.05
   g.add(Rectangle(width=0.86, height=0.56, color=ACCENT_B, stroke_width=2).move_to([x, 0.80, 0]),
         Text(f"β{'₁₂₃ₙ'[k]}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, 0.80, 0]),
         Rectangle(width=0.86, height=0.56, color=ACCENT_A, stroke_width=2).move_to([x, -0.30, 0]),
         Text(f"ε{'₁₂₃ₙ'[k]}", font_size=FS_TAG - 2, color=ACCENT_A).move_to([x, -0.30, 0]),
         self._arr([x, 0.48, 0], [x, -0.00, 0], DIM, sw=1.8, tl=0.09))
  return g.add(self._mid(0.80, "V 的一組有序基底", "an ordered basis for V",
                         ACCENT_B, FS_TAG, x=2.95, w=5.6),
               self._mid(-0.30, "第 j 個座標泛函", "the jth coordinate functional",
                         ACCENT_A, FS_TAG, x=2.95, w=5.6),
               self._mid(-1.15, "它把一個向量送到它的第 j 個座標",
                         "it sends a vector to its jth coordinate",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.78, "定理：這些座標泛函構成對偶空間的一組有序基底",
                         "the theorem: those functionals are an ordered basis for the dual space",
                         ACCENT_A, FS_TAG, w=11.9))

 def _independence(self):
  ox = -3.85
  g = VGroup(Text("Σ cⱼ εⱼ  =  0", font_size=FS_TAG + 2, color=WARN).move_to([-2.35, 1.08, 0]))
  for k in range(4):
   x = ox + k * 0.82
   hit = k == 1
   g.add(Rectangle(width=0.70, height=0.52, color=ACCENT_A if hit else GHOST,
                   stroke_width=2.5 if hit else 2).move_to([x, 0.35, 0]),
         Text("1" if hit else "0", font_size=FS_TAG - 2,
              color=ACCENT_A if hit else GHOST).move_to([x, 0.35, 0]))
  g.add(Text("βᵢ", font_size=FS_TAG, color=ACCENT_B).move_to([ox - 0.78, 0.35, 0]),
        Rectangle(width=3.35, height=0.72, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 1.23, 0.35, 0]),
        self._arr([ox + 1.23, -0.05, 0], [ox + 1.23, -0.52, 0], ACCENT_A, sw=2.5, tl=0.12),
        Rectangle(width=2.40, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 1.23, -0.85, 0]),
        Text("cᵢ  =  0", font_size=FS_TAG + 1, color=ACCENT_A).move_to([ox + 1.23, -0.85, 0]))
  return g.add(self._mid(0.95, "作用在第 i 個基底向量上",
                         "evaluate it on the ith basis vector",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(0.05, "座標組只有第 i 位是一", "its coordinates are one in the ith place only",
                         ACCENT_B, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.85, "整條式子只剩一項", "the whole equation collapses to one term",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.78, "每個 i 都成立，所以這些座標泛函獨立",
                         "that holds for every index, so the functionals are independent",
                         ACCENT_A, FS_TAG, w=11.8))

 def _spanning(self):
  g = VGroup(Rectangle(width=5.30, height=0.68, color=ACCENT_B, stroke_width=2.5)
             .move_to([-2.55, 0.92, 0]),
             Text("ξ  =  Σ εᵢ ( ξ ) βᵢ", font_size=FS_TAG + 1, color=ACCENT_B)
             .move_to([-2.55, 0.92, 0]),
             Rectangle(width=5.30, height=0.68, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.55, 0.08, 0]),
             Text("λ ( ξ )  =  Σ λ ( βᵢ ) εᵢ ( ξ )", font_size=FS_TAG + 1, color=ACCENT_A)
             .move_to([-2.55, 0.08, 0]),
             self._arr([-2.55, 0.55, 0], [-2.55, 0.45, 0], DIM, sw=2, tl=0.08),
             self._arr([-2.55, -0.28, 0], [-2.55, -0.50, 0], DIM, sw=2, tl=0.10),
             Rectangle(width=3.10, height=0.62, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.55, -0.85, 0]),
             Text("λ  =  Σ lᵢ εᵢ", font_size=FS_TAG + 1, color=ACCENT_A)
             .move_to([-2.55, -0.85, 0]))
  return g.add(self._mid(0.92, "基底展開改寫一下", "rewrite the basis expansion",
                         ACCENT_B, FS_TAG, x=3.35, w=4.9),
               self._mid(0.08, "套上任何一個線性泛函", "apply any linear functional",
                         ACCENT_A, FS_TAG, x=3.35, w=4.9),
               self._mid(-0.85, "係數是它在基底上的值", "the coefficients are its values on the basis",
                         DIM, FS_TAG, x=3.35, w=4.9),
               self._mid(-1.78, "所以每個泛函都是這些座標泛函的線性組合——它們生成對偶空間",
                         "so every functional is a combination of them: they span the dual space",
                         ACCENT_A, FS_TAG, w=11.9))

 def _dual_basis(self):
  ox = -3.55
  g = VGroup()
  for k in range(4):
   x = ox + k * 0.94
   sub = "₁₂₃ₙ"[k]
   g.add(Rectangle(width=0.78, height=0.52, color=ACCENT_B, stroke_width=2).move_to([x, 0.85, 0]),
         Text(f"β{sub}", font_size=FS_TAG - 3, color=ACCENT_B).move_to([x, 0.85, 0]),
         Rectangle(width=0.78, height=0.52, color=ACCENT_A, stroke_width=2).move_to([x, 0.10, 0]),
         Text(f"ε{sub}", font_size=FS_TAG - 3, color=ACCENT_A).move_to([x, 0.10, 0]),
         Line([x, 0.59, 0], [x, 0.36, 0], color=DIM, stroke_width=1.6))
  g.add(Text("n", font_size=FS_TAG + 3, color=ACCENT_B).move_to([ox + 3.42, 0.85, 0]),
        Text("n", font_size=FS_TAG + 3, color=ACCENT_A).move_to([ox + 3.42, 0.10, 0]),
        Rectangle(width=3.90, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([-1.55, -0.75, 0]),
        Text("d ( V * )  =  d ( V )", font_size=FS_TAG + 1, color=ACCENT_A)
        .move_to([-1.55, -0.75, 0]))
  return g.add(self._mid(0.85, "V 的基底", "a basis for V", ACCENT_B, FS_TAG, x=3.35, w=4.9),
               self._mid(0.10, "它的對偶基底", "and its dual basis", ACCENT_A, FS_TAG, x=3.35, w=4.9),
               self._mid(-1.35, "一對一配好，個數自然相同",
                         "paired off one to one, so the counts match",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.78, "推論：對偶空間的維數等於原空間的維數",
                         "the corollary: the dual has the same dimension as the space",
                         ACCENT_A, FS_TAG, w=11.9))

 def _three_eqs(self):
  rows = (("ξ  =  Σ εᵢ ( ξ ) βᵢ", ACCENT_B, 0.92),
          ("λ  =  Σ λ ( βᵢ ) εᵢ", ACCENT_A, 0.14),
          ("λ ( ξ )  =  Σ λ ( βᵢ ) εᵢ ( ξ )", ACCENT_C, -0.64))
  g = VGroup()
  for s, col, y in rows:
   g.add(Rectangle(width=5.40, height=0.66, color=col, stroke_width=2.5).move_to([-2.50, y, 0]),
         Text(s, font_size=FS_TAG + 1, color=col).move_to([-2.50, y, 0]))
  g.add(Line([0.35, 0.92, 0], [0.35, 0.14, 0], color=DIM, stroke_width=2),
        Text("↕", font_size=FS_TAG + 2, color=DIM).move_to([0.35, 0.53, 0]))
  return g.add(self._mid(0.92, "向量展開成基底", "a vector expanded in the basis",
                         ACCENT_B, FS_TAG, x=3.85, w=4.2),
               self._mid(0.14, "泛函展開成對偶基底", "a functional in the dual basis",
                         ACCENT_A, FS_TAG, x=3.85, w=4.2),
               self._mid(-0.64, "這一條本身就對稱", "this one is symmetric by itself",
                         ACCENT_C, FS_TAG, x=3.85, w=4.2),
               self._mid(-1.78, "前兩條互為鏡像：係數都是拿對面那組基底去作用得到的",
                         "the first two mirror each other: each coefficient comes from the other basis",
                         DIM, FS_TAG, w=11.9))

 def _no_natural(self):
  """Two bases for the plane, one vector, two isomorphisms V -> V*. The
  functionals that come out are evaluated on one test vector and disagree,
  which is what 'the isomorphism depends on the basis' actually means. All
  four numbers below are computed, not written in by hand."""
  alpha = (2.0, 1.0)
  b1 = ((1.0, 0.0), (0.0, 1.0))
  b2 = ((1.0, 1.0), (0.0, 1.0))
  test = (0.0, 1.0)
  f1, f2 = _theta(alpha, b1), _theta(alpha, b2)
  v1, v2 = float(f1 @ np.array(test)), float(f2 @ np.array(test))
  assert abs(v1 - v2) > 1e-9, "the two bases must actually disagree for this beat to mean anything"
  assert alpha not in b1 and alpha not in b2, "alpha drawn over a basis vector would hide it"
  org = np.array([-3.55, 0.05, 0.0])
  s = 0.58
  g = VGroup(Line(org + [-1.2 * s, 0, 0], org + [2.6 * s, 0, 0], color=GHOST, stroke_width=1.6),
             Line(org + [0, -1.4 * s, 0], org + [0, 1.7 * s, 0], color=GHOST, stroke_width=1.6))
  for (bx, by), col in ((b1[0], ACCENT_B), (b1[1], ACCENT_B), (b2[0], ACCENT_C), (b2[1], ACCENT_C)):
   g.add(Arrow(org, org + s * np.array([bx, by, 0.0]), color=col, stroke_width=2.2,
               buff=0, max_tip_length_to_length_ratio=0.22))
  g.add(Arrow(org, org + s * np.array([alpha[0], alpha[1], 0.0]), color=INK,
              stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.16),
        Text("α", font_size=FS_TAG, color=INK).move_to(org + s * np.array([2.30, 1.25, 0.0])))
  for y, col, lab, val in ((0.72, ACCENT_B, "θ ( β )", v1), (-0.10, ACCENT_C, "θ ( β′ )", v2)):
   g.add(Rectangle(width=4.30, height=0.62, color=col, stroke_width=2.5).move_to([0.95, y, 0]),
         Text(f"{lab} ( α )  ↦  {val:.0f}", font_size=FS_TAG + 1, color=col).move_to([0.95, y, 0]))
  g.add(Rectangle(width=2.15, height=0.58, color=WARN, stroke_width=2.5).move_to([4.60, 0.31, 0]),
        Text(f"{v1:.0f}  ≠  {v2:.0f}", font_size=FS_TAG + 1, color=WARN).move_to([4.60, 0.31, 0]))
  return g.add(self._mid(-0.90, "同一個 α，兩組基底，做出來的泛函不一樣",
                         "one vector, two bases, and the functionals come out different",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.40, "拿同一個向量去測就分得出來",
                         "testing both on the same vector tells them apart",
                         WARN, FS_TAG, w=11.6),
               self._mid(-1.78, "所以同構有，但沒有哪一個是自然的——它隨基底跑",
                         "so isomorphisms exist, but none is natural: it moves with the basis",
                         ACCENT_A, FS_TAG, w=11.9))

 def _rn_standard(self):
  ox = -3.75
  g = VGroup()
  for k in range(3):
   x = ox + k * 1.15
   g.add(Rectangle(width=0.76, height=0.52, color=ACCENT_B, stroke_width=2).move_to([x, 0.90, 0]),
         Text(f"δ{'¹²ⁿ'[k]}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, 0.90, 0]))
  g.add(Text("…", font_size=FS_TAG, color=DIM).move_to([ox + 1.72, 0.90, 0]),
        Rectangle(width=3.30, height=0.76, color=ACCENT_B, stroke_width=2.5)
        .move_to([ox + 1.15, 0.90, 0]),
        self._arr([ox + 1.15, 0.46, 0], [ox + 1.15, 0.10, 0], ACCENT_A, sw=2.5, tl=0.12),
        Rectangle(width=4.60, height=0.66, color=ACCENT_A, stroke_width=2.5)
        .move_to([-1.95, -0.25, 0]),
        Text("a  ↦  L a  ,  L a ( x ) = Σ aᵢ xᵢ", font_size=FS_TAG, color=ACCENT_A)
        .move_to([-1.95, -0.25, 0]))
  return g.add(self._mid(0.90, "座標空間本來就有標準基底",
                         "coordinate space comes with a standard basis",
                         ACCENT_B, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.25, "所以有一個標準的同構", "so there is a standard isomorphism",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.30, "把 n 元組送到「拿它去跟輸入作內積」的那個泛函",
                         "an n-tuple goes to the functional that pairs it against the input",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "所以可以放心把座標空間跟它的對偶空間看成同一個",
                         "so coordinate space may freely be identified with its dual",
                         ACCENT_A, FS_TAG, w=11.9))

 def _second_dual(self):
  boxes = ((-3.75, "V", ACCENT_B), (-0.35, "V *", ACCENT_A), (3.05, "V * *", ACCENT_C))
  g = VGroup()
  for x, lab, col in boxes:
   g.add(Rectangle(width=1.55, height=0.80, color=col, stroke_width=2.5).move_to([x, 0.82, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([x, 0.82, 0]))
  g.add(self._arr([-2.95, 0.82, 0], [-1.15, 0.82, 0], DIM, sw=2.5, tl=0.13),
        self._arr([0.45, 0.82, 0], [2.25, 0.82, 0], DIM, sw=2.5, tl=0.13),
        self._arr([-3.75, 0.36, 0], [3.05, 0.36, 0], ACCENT_C, sw=3, tl=0.15),
        Text("ξ  ↦  ξ * *", font_size=FS_TAG + 1, color=ACCENT_C).move_to([-0.35, 0.02, 0]),
        Rectangle(width=4.30, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([-1.65, -0.55, 0]),
        Text("ω ( ξ , f )  =  f ( ξ )", font_size=FS_TAG + 1, color=ACCENT_A)
        .move_to([-1.65, -0.55, 0]))
  return g.add(self._mid(-0.55, "這個配對是雙線性的", "the pairing is bilinear",
                         DIM, FS_TAG, x=3.35, w=4.7),
               self._mid(-1.30, "於是由第 1 章的定理，向量送到它對應的那個映射就是線性的",
                         "so by a theorem of chapter one, sending a vector to its map is linear",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "而這一個，是自然的同構",
                         "and this one is a natural isomorphism",
                         ACCENT_C, FS_TAG, w=11.6))

 def _injective(self):
  ox = -3.75
  g = VGroup()
  for k in range(4):
   x = ox + k * 0.94
   first = k == 0
   g.add(Rectangle(width=0.78, height=0.54, color=ACCENT_A if first else GHOST,
                   stroke_width=2.5 if first else 2).move_to([x, 0.95, 0]))
  g.add(Text("α", font_size=FS_TAG - 1, color=ACCENT_A).move_to([ox, 0.95, 0]),
        self._mid(0.42, "把 α 當成第一個基底向量", "make α the first basis vector",
                  ACCENT_A, FS_TAG, x=ox + 1.41, w=3.8),
        self._arr([ox + 1.41, 0.12, 0], [ox + 1.41, -0.22, 0], DIM, sw=2, tl=0.10),
        Rectangle(width=3.05, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 1.41, -0.55, 0]),
        Text("f ( α )  =  1", font_size=FS_TAG + 1, color=ACCENT_A)
        .move_to([ox + 1.41, -0.55, 0]))
  return g.add(self._mid(0.95, "取一個非零向量", "take a nonzero vector",
                         DIM, FS_TAG, x=3.15, w=5.2),
               self._mid(-0.05, "取對偶基底的第一個泛函", "take the first functional of the dual basis",
                         ACCENT_A, FS_TAG, x=3.15, w=5.2),
               self._mid(-1.30, "所以它對應過去的元素不是零——映射是嵌射",
                         "so the element it goes to is not zero, and the map is injective",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "兩邊維數相同，於是它同時也是雙射",
                         "the dimensions agree, so it is bijective as well",
                         DIM, FS_TAG, w=11.6))

 def _symmetry(self):
  g = VGroup(Rectangle(width=3.90, height=0.70, color=ACCENT_B, stroke_width=2.5)
             .move_to([-2.85, 0.88, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-2.85, 0.88, 0]),
             Rectangle(width=3.90, height=0.70, color=ACCENT_A, stroke_width=2.5)
             .move_to([1.75, 0.88, 0]),
             Text("V *", font_size=FS_TAG + 2, color=ACCENT_A).move_to([1.75, 0.88, 0]),
             self._arr([-0.85, 1.06, 0], [-0.25, 1.06, 0], ACCENT_A, sw=2.5, tl=0.12),
             self._arr([-0.25, 0.70, 0], [-0.85, 0.70, 0], ACCENT_B, sw=2.5, tl=0.12),
             Rectangle(width=4.20, height=0.64, color=ACCENT_C, stroke_width=2.5)
             .move_to([-1.55, 0.15, 0]),
             Text("⟨ ξ , f ⟩  =  f ( ξ )", font_size=FS_TAG + 1, color=ACCENT_C)
             .move_to([-1.55, 0.15, 0]))
  return g.add(self._mid(0.15, "兩個符號都是變數", "both symbols are variables",
                         ACCENT_C, FS_TAG, x=3.35, w=4.7),
               self._mid(-0.70, "每一個都是另一個的對偶", "each one is the dual of the other",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.32, "引理：一組泛函是某組基底的對偶基底，反過來看也一樣成立",
                         "the lemma: if functionals are dual to a basis, that basis is dual to them",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集接零化子與伴隨算子",
                         "next time: annihilators and the adjoint",
                         DIM, FS_TAG, w=11.6))

 def stage(self):
  dd, t31, ind = self._dual_def(), self._thm31(), self._independence()
  sp, db, te = self._spanning(), self._dual_basis(), self._three_eqs()
  nn, rs, sd = self._no_natural(), self._rn_standard(), self._second_dual()
  inj, sy = self._injective(), self._symmetry()
  return [([dd], []), ([t31], [dd]), ([ind], [t31]), ([sp], [ind]),
          ([db], [sp]), ([te], [db]), ([nn], [te]), ([rs], [nn]),
          ([sd], [rs]), ([inj], [sd]), ([sy], [inj])]


AdvCalcE21ZH, AdvCalcE21EN = make(AdvCalcE21Base, "21", prefix="AdvCalcE")
