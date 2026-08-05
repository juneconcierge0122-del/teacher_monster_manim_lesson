"""advcalc E18 — Chapter 2, section 1, first half (book pp. 71-74): bases, the
coordinate isomorphism, Lemma 1.2 and Theorems 1.1 and 1.2.

Beat 9 is the one worth drawing: the informal way to find a basis is to walk a
spanning set and keep the members that enlarge the span, and that is a picture
of a chain of nested subspaces growing by one dimension at a time. The book
declines to formalize it, so the episode shows the idea and then states the
theorem it is replaced by.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


class AdvCalcE18Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 18

 MODE_LABEL = {
  0: {"zh": "第 2 章：有限維空間", "en": "chapter 2: the finite-dimensional spaces"},
  1: {"zh": "搬到座標空間，就取得矩陣", "en": "transferred to coordinates, it becomes a matrix"},
  2: {"zh": "嵌射是獨立，同構是基底", "en": "injective is independent, iso is a basis"},
  3: {"zh": "每個向量唯一一組係數", "en": "one set of coefficients per vector"},
  4: {"zh": "驗一個具體的例子", "en": "checking a concrete one"},
  5: {"zh": "比較常見的那個定義", "en": "the more usual definition"},
  6: {"zh": "基底同構與座標同構", "en": "the basis and coordinate isomorphisms"},
  7: {"zh": "兩件小事", "en": "two small remarks"},
  8: {"zh": "擴張外面的向量，加進去還獨立", "en": "a vector outside the span keeps it independent"},
  9: {"zh": "留下讓擴張變大的那些", "en": "keep the ones that enlarge the span"},
  10: {"zh": "極小的生成集就是基底", "en": "a minimal spanning set is a basis"},
 }

 def _chapter(self):
  g = VGroup(Ellipse(width=5.20, height=2.20, color=DIM, stroke_width=2.5)
             .move_to([-2.35, 0.05, 0]),
             Text("V", font_size=FS_TAG, color=DIM).move_to([-2.35, 1.15, 0]),
             Ellipse(width=3.00, height=1.55, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.12).move_to([-3.05, 0.05, 0]),
             self._mid(0.05, "有限維", "finite-dimensional", ACCENT_A, FS_TAG, x=-3.05, w=2.7))
  return g.add(self._mid(0.85, "每個有限維空間配一個整數", "each such space gets one integer",
                         DIM, FS_TAG, x=3.35, w=5.0),
               self._mid(0.00, "叫做維數", "called its dimension", ACCENT_A, FS_TAG, x=3.35, w=5.0),
               self._mid(-0.85, "後面深入探討的主要工具", "the principal tool for what follows",
                         DIM, FS_TAG, x=3.35, w=5.0),
               self._mid(-1.72, "它符合我們對「維度」的直覺，而且證得出來",
                         "it matches our intuition about dimensionality, and can be proved to",
                         DIM, FS_TAG, w=11.6))

 def _transfer(self):
  g = VGroup()
  for cx, lab, col in ((-3.75, "V", ACCENT_B), (-0.35, "ℝⁿ", ACCENT_A)):
   g.add(Ellipse(width=1.70, height=1.30, color=col, stroke_width=2.5,
                 fill_color=col, fill_opacity=0.10).move_to([cx, 0.45, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([cx, 0.45, 0]))
  g.add(self._arr([-2.85, 0.45, 0], [-1.30, 0.45, 0], ACCENT_A, sw=3, tl=0.15),
        Text("≅", font_size=FS_TAG + 3, color=ACCENT_A).move_to([-2.05, 0.82, 0]),
        self._arr([0.55, 0.45, 0], [1.90, 0.45, 0], ACCENT_C, sw=3, tl=0.15),
        Rectangle(width=1.85, height=1.30, color=ACCENT_C, stroke_width=2.5)
        .move_to([2.90, 0.45, 0]),
        Text("t", font_size=FS_TAG + 3, color=ACCENT_C).move_to([2.90, 0.45, 0]))
  return g.add(self._mid(-0.75, "一個算子被搬到座標空間，在那裡取得一個矩陣",
                         "an operator transferred to coordinates acquires a matrix there",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.72, "所以有限維空間上的線性變換理論，完全被矩陣映照出來",
                         "so linear transformations on such spaces are mirrored completely by matrices",
                         ACCENT_A, FS_TAG, w=11.9))

 def _defs(self):
  g = VGroup()
  for cx, cond, zh, en, col in ((-3.05, "inj", "獨立", "independent", ACCENT_B),
                                (3.05, "iso", "基底", "a basis", ACCENT_A)):
   g.add(Rectangle(width=4.20, height=1.75, color=col, stroke_width=2.5).move_to([cx, 0.35, 0]),
         Text(f"L α   {cond}", font_size=FS_TAG + 2, color=col).move_to([cx, 0.72, 0]),
         self._arr([cx, 0.42, 0], [cx, 0.10, 0], DIM, sw=2, tl=0.10),
         self._mid(-0.12, zh, en, col, FS_TAG + 1, x=cx, w=3.8))
  return g.add(self._mid(-1.05, "同一個線性組合映射，兩個條件，兩個名字",
                         "one combination map, two conditions, two names",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.72, "指標集是一到 n 時，就叫有序基底，或者框架",
                         "when the index set is one to n it is an ordered basis, or a frame",
                         DIM, FS_TAG, w=11.8))

 def _unique(self):
  o = np.array([-2.95, -0.55, 0.0])
  u, v = np.array([1.20, 0.28, 0.0]), np.array([0.32, 1.05, 0.0])
  tgt = o + 1.55 * u + 0.92 * v
  g = VGroup(Line(o - 0.50 * u, o + 2.40 * u, color=GHOST, stroke_width=2),
             Line(o - 0.40 * v, o + 1.60 * v, color=GHOST, stroke_width=2),
             self._arr(o, o + 1.55 * u, ACCENT_B, sw=3, tl=0.14),
             self._arr(o + 1.55 * u, tgt, ACCENT_C, sw=3, tl=0.14),
             self._arr(o, tgt, ACCENT_A, sw=4.5, tl=0.20),
             self._dash(o + 0.92 * v, tgt, GHOST, n=8),
             Dot(o, radius=0.06, color=INK))
  return g.add(self._mid(1.05, "存在，因為它們生成 V", "they exist because the vectors span V",
                         ACCENT_C, FS_TAG, x=3.20, w=5.4),
               self._mid(-0.10, "唯一，因為它們獨立", "they are unique because it is independent",
                         ACCENT_B, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.72, "所以是基底，若且唯若每個向量都有唯一一組係數",
                         "so it is a basis exactly when every vector has one set of coefficients",
                         ACCENT_A, FS_TAG, w=11.8))

 B1, B2 = (2.0, 1.0), (1.0, -3.0)

 def _concrete(self):
  """The book's own example, with the elimination actually carried out so the
  claim that the solution is unique is not merely asserted."""
  det = self.B1[0] * self.B2[1] - self.B1[1] * self.B2[0]
  assert abs(det) > 1e-9, "a basis needs a nonzero determinant here"
  o = np.array([-3.05, -0.45, 0.0])
  s = 0.42
  g = VGroup(self._arr(o - np.array([1.20, 0, 0]), o + np.array([1.75, 0, 0]),
                       GHOST, sw=2, tl=0.10),
             self._arr(o - np.array([0, 0.95, 0]), o + np.array([0, 1.30, 0]),
                       GHOST, sw=2, tl=0.10),
             Dot(o, radius=0.06, color=INK))
  for (b, col, lab) in ((self.B1, ACCENT_B, "b¹"), (self.B2, ACCENT_C, "b²")):
   tip = o + s * np.array([b[0], b[1], 0.0])
   g.add(self._arr(o, tip, col, sw=3.5, tl=0.16),
         Text(lab, font_size=FS_TAG - 2, color=col).move_to(tip + np.array([0.22, 0.16, 0])))
  g.add(Text(f"det  =  {det:.0f}  ≠  0", font_size=FS_TAG + 1, color=ACCENT_A)
        .move_to([2.85, 0.75, 0]))
  return g.add(self._mid(-0.10, "所以每個目標都有唯一解",
                         "so every target has exactly one solution",
                         ACCENT_A, FS_TAG, x=2.85, w=5.6),
               self._mid(-0.95, "拆成兩條純量方程，消去法解出來",
                         "split into two scalar equations and eliminate",
                         DIM, FS_TAG, x=2.85, w=5.6),
               self._mid(-1.72, "驗一組向量是不是基底，就是驗這件事",
                         "checking a set is a basis is checking exactly that",
                         DIM, FS_TAG, w=11.6))

 def _corollary(self):
  ox = -3.35
  g = VGroup()
  for k in range(3):
   x = ox + k * 1.20
   g.add(Rectangle(width=0.90, height=0.52, color=ACCENT_B, stroke_width=2).move_to([x, 0.62, 0]),
         Text(f"x{k + 1}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, 0.62, 0]))
   if k < 2:
    g.add(Text("+", font_size=FS_TAG, color=DIM).move_to([x + 0.60, 0.62, 0]))
  g.add(Text("=", font_size=FS_TAG + 2, color=DIM).move_to([ox + 3.00, 0.62, 0]),
        Text("0", font_size=FS_TAG + 2, color=ACCENT_A).move_to([ox + 3.50, 0.62, 0]),
        self._arr([ox + 1.20, 0.28, 0], [ox + 1.20, -0.24, 0], ACCENT_A, sw=2.5, tl=0.12))
  for k in range(3):
   x = ox + k * 1.20
   g.add(Rectangle(width=0.90, height=0.52, color=DIM, stroke_width=2).move_to([x, -0.58, 0]),
         Text("0", font_size=FS_TAG, color=DIM).move_to([x, -0.58, 0]))
  return g.add(self._mid(0.62, "係數乘向量加起來是零", "coefficients times vectors summing to zero",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.58, "就每個係數都是零", "forces every coefficient to be zero",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.72, "因為那正好是說零空間只有零向量",
                         "because that says precisely that the null space is only zero",
                         DIM, FS_TAG, w=11.8))

 def _isos(self):
  g = VGroup()
  for cx, lab, col in ((-3.55, "V", ACCENT_B), (0.35, "ℝⁿ", ACCENT_A)):
   g.add(Ellipse(width=1.60, height=1.20, color=col, stroke_width=2.5,
                 fill_color=col, fill_opacity=0.10).move_to([cx, 0.50, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([cx, 0.50, 0]))
  g.add(self._arr([0.35 - 0.90, 0.72, 0], [-3.55 + 0.90, 0.72, 0], ACCENT_C, sw=3, tl=0.15),
        Text("L α", font_size=FS_TAG - 1, color=ACCENT_C).move_to([-1.60, 1.06, 0]),
        self._arr([-3.55 + 0.90, 0.28, 0], [0.35 - 0.90, 0.28, 0], ACCENT_A, sw=3, tl=0.15),
        Text("L α ⁻¹", font_size=FS_TAG - 1, color=ACCENT_A).move_to([-1.60, -0.06, 0]),
        self._arr([1.20, 0.50, 0], [2.35, 0.50, 0], DIM, sw=2.5, tl=0.13),
        Text("xⱼ", font_size=FS_TAG, color=DIM).move_to([2.80, 0.50, 0]))
  return g.add(self._mid(-0.80, "基底同構，與它的反函數座標同構",
                         "the basis isomorphism, and its inverse the coordinate isomorphism",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.72, "再取第 j 個座標，就是第 j 個座標泛函",
                         "and taking the jth coordinate is the jth coordinate functional",
                         ACCENT_A, FS_TAG, w=11.6))

 def _remarks(self):
  g = VGroup()
  ox = -3.55
  for k, (lab, col) in enumerate((("α₁", ACCENT_B), ("α₂", ACCENT_B), ("α₁", WARN))):
   g.add(Rectangle(width=0.90, height=0.52, color=col, stroke_width=2).move_to([ox + k * 1.05, 0.72, 0]),
         Text(lab, font_size=FS_TAG - 2, color=col).move_to([ox + k * 1.05, 0.72, 0]))
  g.add(Line([ox + 1.65, 0.42, 0], [ox + 2.45, 1.02, 0], color=WARN, stroke_width=3),
        self._mid(0.72, "指標重複，就一定不獨立", "a repeated index is never independent",
                  WARN, FS_TAG, x=2.85, w=5.6))
  for k in range(4):
   g.add(Rectangle(width=0.72, height=0.48, color=ACCENT_A if k < 2 else GHOST, stroke_width=2)
         .move_to([ox + k * 0.90, -0.55, 0]))
  g.add(Rectangle(width=1.75, height=0.72, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 0.45, -0.55, 0]),
        self._mid(-0.55, "獨立集合的子集也獨立", "a subset of an independent set is independent",
                  ACCENT_A, FS_TAG, x=2.85, w=5.6))
  return g.add(self._mid(-1.72, "這兩件小事，等一下挑基底的時候會用到",
                         "both small remarks get used in picking a basis below",
                         DIM, FS_TAG, w=11.6))

 def _lemma(self):
  o = np.array([-2.95, -0.45, 0.0])
  u = np.array([1.35, 0.32, 0.0])
  beta = o + 0.95 * u + np.array([0.15, 1.05, 0.0])
  g = VGroup(Line(o - 0.60 * u, o + 2.15 * u, color=ACCENT_B, stroke_width=3.5),
             Dot(o, radius=0.06, color=INK),
             self._arr(o, o + 1.30 * u, ACCENT_B, sw=3, tl=0.14),
             self._arr(o, beta, ACCENT_A, sw=3.5, tl=0.16),
             Dot(beta, radius=0.085, color=ACCENT_A),
             Text("L ( B )", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + 2.15 * u + np.array([0.20, -0.28, 0])),
             Text("β", font_size=FS_TAG, color=ACCENT_A)
             .move_to(beta + np.array([0.24, 0.14, 0])))
  return g.add(self._mid(1.05, "β 不在 B 的線性擴張裡", "beta is not in the span of B",
                         ACCENT_A, FS_TAG, x=3.20, w=5.4),
               self._mid(0.05, "把它加進去，還是獨立的", "adjoin it and the set stays independent",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.30, "若有非零組合等於零，β 的係數不能是零",
                         "if a nontrivial combination vanished, beta's coefficient could not be zero",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.74, "那就解得出 β 落在擴張裡——矛盾",
                         "and then beta could be solved for, putting it in the span",
                         WARN, FS_TAG, w=11.6))

 def _grow(self):
  """The chain of spans, each step adding one dimension. Drawn as nested
  regions because that is what "enlarges the span" means."""
  g = VGroup()
  for k, (w, h, col) in enumerate(((1.55, 0.75, ACCENT_B), (2.85, 1.30, ACCENT_C),
                                   (4.35, 1.95, ACCENT_A))):
   g.add(Ellipse(width=w, height=h, color=col, stroke_width=2.5,
                 fill_color=col, fill_opacity=0.08).move_to([-2.45, 0.10, 0]))
  for k, x in enumerate((-3.05, -2.05, -0.95)):
   g.add(Dot([x, 0.10, 0], radius=0.075, color=(ACCENT_B, ACCENT_C, ACCENT_A)[k]),
         Text(f"α{k + 1}", font_size=FS_TAG - 4, color=(ACCENT_B, ACCENT_C, ACCENT_A)[k])
         .move_to([x, 0.44, 0]))
  return g.add(self._mid(0.95, "一個一個看過去", "run through the spanning set",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.05, "留下讓擴張真的變大的", "keeping the ones that enlarge the span",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.85, "最後剩下的就是基底", "and what is left is a basis",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.72, "很直觀，但要嚴格寫下來相當麻煩，所以書上換了個作法",
                         "intuitive, but messy to set up rigorously, so the book proceeds differently",
                         DIM, FS_TAG, w=11.9))

 def _thm11(self):
  g = VGroup(Rectangle(width=4.60, height=0.72, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.55, 0.85, 0]),
             self._mid(0.85, "極小的有限生成集", "a minimal finite spanning set",
                       ACCENT_A, FS_TAG, x=-2.55, w=4.3),
             self._arr([-2.55, 0.45, 0], [-2.55, 0.10, 0], DIM, sw=2, tl=0.10),
             Rectangle(width=4.60, height=0.72, color=ACCENT_B, stroke_width=2.5)
             .move_to([-2.55, -0.28, 0]),
             self._mid(-0.28, "就是一組基底", "is a basis", ACCENT_B, FS_TAG, x=-2.55, w=4.3))
  ox = 2.75
  for k in range(4):
   g.add(Rectangle(width=0.62, height=0.48, color=ACCENT_A if k < 4 else GHOST, stroke_width=2)
         .move_to([ox + (k - 1.5) * 0.72, 0.85, 0]),
         Text("1", font_size=FS_TAG - 3, color=ACCENT_A if k == 1 else GHOST)
         .move_to([ox + (k - 1.5) * 0.72, 0.85, 0]))
  g.add(self._mid(-0.28, "Kronecker 的 delta 函數", "the Kronecker delta functions",
                  ACCENT_A, FS_TAG, x=ox, w=4.4),
        self._mid(0.30, "座標空間的標準基底", "the standard basis for coordinate space",
                  DIM, FS_TAG, x=ox, w=4.4))
  return g.add(self._mid(-1.05, "所以任何有限維空間都有基底，任何有限獨立子集都能擴充成基底",
                         "so every finite-dimensional space has a basis, and independent sets extend",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.72, "而標準基底特別在於：它的基底同構正好是恆等",
                         "the standard basis is singled out because its basis isomorphism is the identity",
                         ACCENT_A, FS_TAG, w=11.9))

 def stage(self):
  ch, tf, df, un = self._chapter(), self._transfer(), self._defs(), self._unique()
  cc, co, iso = self._concrete(), self._corollary(), self._isos()
  rm, lm, gr, t11 = self._remarks(), self._lemma(), self._grow(), self._thm11()
  return [([ch], []), ([tf], [ch]), ([df], [tf]), ([un], [df]),
          ([cc], [un]), ([co], [cc]), ([iso], [co]), ([rm], [iso]),
          ([lm], [rm]), ([gr], [lm]), ([t11], [gr])]


AdvCalcE18ZH, AdvCalcE18EN = make(AdvCalcE18Base, "18", prefix="AdvCalcE")
