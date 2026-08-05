"""advcalc E17 — Chapter 1, section 6 (book pp. 67-71): bilinear mappings,
Theorems 6.1 and 6.2, and natural isomorphisms.

Beats 2 and 3 are the load-bearing pair: bilinear and linear-on-the-product
are different conditions, and the two counterexamples the book gives are each
one condition holding while the other fails. Drawing them as what actually
happens to a figure -- a line that shifts instead of passing through the
origin, and a sum of pairs whose image misses the sum of the images -- is the
only way to see that they are different conditions rather than two names.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


class AdvCalcE17Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 17

 MODE_LABEL = {
  0: {"zh": "對偶原則的向量空間版本", "en": "duality, in the vector setting"},
  1: {"zh": "固定一個，對另一個是線性的", "en": "hold one fixed, linear in the other"},
  2: {"zh": "線性，但不是雙線性", "en": "linear, but not bilinear"},
  3: {"zh": "雙線性，但不是線性", "en": "bilinear, but not linear"},
  4: {"zh": "一個雙線性，兩個線性", "en": "one bilinear map, two linear ones"},
  5: {"zh": "把第二個變數送到那個映射", "en": "send the second variable to that map"},
  6: {"zh": "合成本身就是雙線性的", "en": "composition is itself bilinear"},
  7: {"zh": "線性組合公式被照亮", "en": "the combination formula, relit"},
  8: {"zh": "純量積給出的同構", "en": "the isomorphism from the scalar product"},
  9: {"zh": "同一個矩陣，兩種讀法", "en": "one matrix, two readings"},
  10: {"zh": "暫時的認同，與永久的", "en": "a transient identification, and a permanent one"},
 }

 def _grid(self, cx, cy, hi_col=None, hi_row=None, n=5, m=4, dx=0.36, dy=0.32):
  g = VGroup()
  for i in range(n):
   for j in range(m):
    on = (hi_col is not None and i == hi_col) or (hi_row is not None and j == hi_row)
    col = ACCENT_A if (hi_col is not None and i == hi_col) else (
      ACCENT_C if (hi_row is not None and j == hi_row) else DIM)
    g.add(Dot([cx + (i - (n - 1) / 2) * dx, cy + (j - (m - 1) / 2) * dy, 0],
              radius=0.07 if on else 0.05, color=col))
  return g

 def _duality(self):
  g = VGroup(Rectangle(width=2.30, height=1.70, color=DIM, stroke_width=2.5)
             .move_to([-3.30, 0.20, 0]),
             self._grid(-3.30, 0.20),
             Text("U × V", font_size=FS_TAG - 2, color=DIM).move_to([-3.30, 1.16, 0]),
             self._arr([-2.05, 0.20, 0], [-0.65, 0.20, 0], ACCENT_A, sw=3, tl=0.15),
             Text("ω", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-1.35, 0.55, 0]),
             Rectangle(width=1.55, height=1.20, color=ACCENT_B, stroke_width=2.5)
             .move_to([0.20, 0.20, 0]),
             Text("W", font_size=FS_TAG + 1, color=ACCENT_B).move_to([0.20, 0.20, 0]))
  return g.add(self._mid(0.85, "第零章的對偶原則", "the duality principle of chapter zero",
                         DIM, FS_TAG, x=3.65, w=4.7),
               self._mid(-0.35, "放進向量空間之後的版本",
                         "in its vector-space setting", ACCENT_A, FS_TAG, x=3.65, w=4.7),
               self._mid(-1.35, "所以它對理解線性代數很重要",
                         "which is why it matters for linear algebra",
                         DIM, FS_TAG, w=11.4))

 def _slices(self):
  g = VGroup()
  for cx, hc, hr, zh, en, col in ((-3.15, 2, None, "固定第一個變數", "hold the first fixed", ACCENT_A),
                                  (3.15, None, 1, "固定第二個變數", "hold the second fixed", ACCENT_C)):
   g.add(Rectangle(width=2.30, height=1.70, color=DIM, stroke_width=2).move_to([cx, 0.30, 0]),
         self._grid(cx, 0.30, hi_col=hc, hi_row=hr),
         self._mid(-0.80, zh, en, col, FS_TAG, x=cx, w=4.4))
   if hc is not None:
    x = cx + (hc - 2) * 0.36
    g.add(Line([x, 0.30 - 0.58, 0], [x, 0.30 + 0.58, 0], color=ACCENT_A, stroke_width=1.8))
   else:
    y = 0.30 + (hr - 1.5) * 0.32
    g.add(Line([cx - 0.80, y, 0], [cx + 0.80, y, 0], color=ACCENT_C, stroke_width=1.8))
  return g.add(self._mid(-1.30, "剩下的那一條，對另一個變數是線性的",
                         "what is left is linear in the other variable",
                         ACCENT_A, FS_TAG, w=11.4),
               self._mid(-1.78, "兩個方向都要成立，才叫雙線性",
                         "both directions must hold for the map to be bilinear",
                         DIM, FS_TAG, w=11.4))

 def _not_bilinear(self):
  """x + y: fix y and the line no longer passes through the origin, so the
  slice is affine rather than linear."""
  o = np.array([-2.85, -0.75, 0.0])
  g = VGroup(self._arr(o - np.array([0.55, 0, 0]), o + np.array([2.55, 0, 0]),
                       DIM, sw=2, tl=0.11),
             self._arr(o - np.array([0, 0.75, 0]), o + np.array([0, 1.35, 0]),
                       DIM, sw=2, tl=0.11),
             Line(o + np.array([-0.45, -0.45, 0]), o + np.array([1.50, 1.50, 0]),
                  color=GHOST, stroke_width=2.5),
             Line(o + np.array([-0.45, 0.30, 0]), o + np.array([1.00, 1.75, 0]),
                  color=WARN, stroke_width=3.5),
             Dot(o, radius=0.06, color=INK),
             Dot(o + np.array([0.0, 0.75, 0]), radius=0.08, color=WARN))
  return g.add(self._mid(1.05, "固定 y 之後的那一條", "the slice after fixing y",
                         DIM, FS_TAG, x=3.10, w=5.4),
               self._mid(0.10, "沒有通過原點", "does not pass through the origin",
                         WARN, FS_TAG, x=3.10, w=5.4),
               self._mid(-0.80, "所以只是仿射，不是線性", "so it is affine, not linear",
                         DIM, FS_TAG, x=3.10, w=5.4),
               self._mid(-1.68, "但把一對數送到它們的和，在乘積空間上確實是線性的",
                         "yet sending a pair to its sum really is linear on the product",
                         DIM, FS_TAG, w=11.9))

 def _not_linear(self):
  """xy: the image of a sum of pairs is checked against the sum of images, and
  the two differ, which is the whole failure of linearity."""
  a, b = (1.0, 2.0), (3.0, 1.0)
  lhs = (a[0] + b[0]) * (a[1] + b[1])
  rhs = a[0] * a[1] + b[0] * b[1]
  assert abs(lhs - rhs) > 1e-9, "the counterexample must actually fail"
  g = VGroup()
  rows = ((0.72, f"( {a[0]:.0f} + {b[0]:.0f} ) ( {a[1]:.0f} + {b[1]:.0f} )  =  {lhs:.0f}", ACCENT_A),
          (-0.02, f"{a[0]:.0f} · {a[1]:.0f}  +  {b[0]:.0f} · {b[1]:.0f}  =  {rhs:.0f}", ACCENT_B))
  for y, s, col in rows:
   g.add(Rectangle(width=5.20, height=0.62, color=col, stroke_width=2.5).move_to([-1.55, y, 0]),
         Text(s, font_size=FS_TAG + 1, color=col).move_to([-1.55, y, 0]))
  g.add(Text("≠", font_size=FS_TAG + 8, color=WARN).move_to([-1.55, -0.72, 0]))
  return g.add(self._mid(0.72, "兩對先相加再取像", "add the pairs, then take the image",
                         ACCENT_A, FS_TAG, x=3.55, w=4.6),
               self._mid(-0.02, "兩個像相加", "or add the two images",
                         ACCENT_B, FS_TAG, x=3.55, w=4.6),
               self._mid(-1.30, "兩邊不相等，所以乘法不是線性的",
                         "the two differ, so multiplication is not linear",
                         WARN, FS_TAG, w=11.4),
               self._mid(-1.78, "但它確實是雙線性的；純量積也一樣",
                         "but it is bilinear, and so is the scalar product",
                         DIM, FS_TAG, w=11.4))

 def _thm61(self):
  g = VGroup(Rectangle(width=2.90, height=0.72, color=ACCENT_A, stroke_width=2.5)
             .move_to([0.0, 0.86, 0]),
             self._mid(0.86, "雙線性的 ω", "a bilinear map", ACCENT_A, FS_TAG, x=0.0, w=2.6))
  for cx, lab, col in ((-3.15, "U  →  Hom ( V , W )", ACCENT_B),
                       (3.15, "V  →  Hom ( U , W )", ACCENT_C)):
   g.add(Rectangle(width=3.90, height=0.80, color=col, stroke_width=2.5).move_to([cx, -0.60, 0]),
         Text(lab, font_size=FS_TAG - 1, color=col).move_to([cx, -0.60, 0]),
         self._arr([np.sign(cx) * 1.35, 0.64, 0], [cx + np.sign(cx) * -1.10, -0.32, 0],
                   DIM, sw=2.2, tl=0.11),
         self._arr([cx + np.sign(cx) * -1.55, -0.32, 0], [np.sign(cx) * 1.05, 0.64, 0],
                   DIM, sw=2.2, tl=0.11))
  return g.add(self._mid(-1.30, "透過對偶，三者互相等價",
                         "by duality the three are equivalent",
                         ACCENT_A, FS_TAG, w=11.4),
               self._mid(-1.78, "這就是雙線性的「線性意義」",
                         "that is the linear meaning of bilinearity",
                         DIM, FS_TAG, w=11.4))

 def _construction(self):
  g = VGroup()
  ys = (0.78, 0.14, -0.50)
  for k, y in enumerate(ys):
   g.add(Dot([-3.85, y, 0], radius=0.075, color=ACCENT_C),
         Text(f"η{k + 1}", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-4.30, y, 0]),
         self._arr([-3.62, y, 0], [-2.20, y, 0], DIM, sw=2, tl=0.10),
         Rectangle(width=2.10, height=0.50, color=ACCENT_A, stroke_width=2)
         .move_to([-1.05, y, 0]),
         Text(f"ω η{k + 1}", font_size=FS_TAG - 3, color=ACCENT_A).move_to([-1.05, y, 0]))
  g.add(Rectangle(width=2.70, height=2.10, color=ACCENT_A, stroke_width=2.5)
        .move_to([-1.05, 0.14, 0]),
        Text("Hom ( U , W )", font_size=FS_TAG - 3, color=ACCENT_A).move_to([-1.05, -1.10, 0]))
  return g.add(self._mid(0.78, "固定第二個變數", "fix the second variable",
                         DIM, FS_TAG, x=3.55, w=4.7),
               self._mid(0.14, "得到一個線性映射", "and a linear map results",
                         ACCENT_A, FS_TAG, x=3.55, w=4.7),
               self._mid(-0.50, "而這個對應本身也線性", "and that correspondence is itself linear",
                         ACCENT_C, FS_TAG, x=3.55, w=4.7),
               self._mid(-1.72, "第二件事，正好就是雙線性的另外一半",
                         "the second fact is exactly the other half of bilinearity",
                         DIM, FS_TAG, w=11.6))

 def _comp_bilinear(self):
  g = VGroup(Rectangle(width=3.10, height=0.72, color=ACCENT_B, stroke_width=2.5)
             .move_to([-3.05, 0.55, 0]),
             Text("⟨ S , T ⟩  ↦  S ∘ T", font_size=FS_TAG, color=ACCENT_B)
             .move_to([-3.05, 0.55, 0]),
             self._arr([-3.05, 0.15, 0], [-3.05, -0.25, 0], DIM, sw=2, tl=0.10),
             Rectangle(width=3.10, height=0.72, color=ACCENT_A, stroke_width=2.5)
             .move_to([-3.05, -0.62, 0]),
             self._mid(-0.62, "雙線性", "bilinear", ACCENT_A, FS_TAG, x=-3.05, w=2.8))
  return g.add(self._mid(0.85, "固定一個就線性，兩邊都是",
                         "fix either one and it is linear",
                         DIM, FS_TAG, x=2.75, w=5.8),
               self._mid(-0.05, "所以「固定 T 從右邊合成是線性」",
                         "so the earlier corollary about composing on the right",
                         DIM, FS_TAG, x=2.75, w=5.8),
               self._mid(-0.95, "其實只是這件事的一半", "was only half of this",
                         ACCENT_A, FS_TAG, x=2.75, w=5.8),
               self._mid(-1.72, "有時這樣重讀給出新洞見，有時反而沒那麼有用",
                         "sometimes the rereading gives insight, sometimes it seems less helpful",
                         DIM, FS_TAG, w=11.8))

 def _thm62(self):
  g = VGroup(Rectangle(width=5.60, height=0.72, color=ACCENT_A, stroke_width=2.5)
             .move_to([-1.75, 0.80, 0]),
             Text("⟨ x , α ⟩  ↦  Σ₁ⁿ xᵢ αᵢ", font_size=FS_TAG + 1, color=ACCENT_A)
             .move_to([-1.75, 0.80, 0]))
  ax, bx = -3.15, 1.05
  for k, y in enumerate((-0.20, -0.80)):
   g.add(Dot([ax, y, 0], radius=0.07, color=ACCENT_B), Dot([bx, y, 0], radius=0.07, color=ACCENT_C),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=1.8, tl=0.09))
  g.add(self._mid(0.25, "Vⁿ", "Vⁿ", ACCENT_B, FS_TAG, x=ax, w=1.6),
        self._mid(0.25, "Hom ( ℝⁿ , V )", "Hom ( ℝⁿ , V )", ACCENT_C, FS_TAG, x=bx, w=3.2))
  return g.add(self._mid(0.80, "這個是雙線性的", "this one is bilinear",
                         ACCENT_A, FS_TAG, x=3.85, w=4.2),
               self._mid(-0.50, "所以右邊那個對應是同構", "so that correspondence is an isomorphism",
                         ACCENT_C, FS_TAG, x=3.85, w=4.2),
               self._mid(-1.72, "第一章那個線性組合的定理，就這樣被重新照亮了",
                         "which is the combination theorem of chapter one, seen again",
                         DIM, FS_TAG, w=11.8))

 def _scalar(self):
  ax, bx = -2.55, 1.85
  ys = (0.72, 0.16, -0.40, -0.96)
  g = VGroup(self._mid(1.15, "ℝⁿ", "ℝⁿ", ACCENT_B, FS_TAG, x=ax, w=2.0),
             self._mid(1.15, "ℝⁿ 上的線性泛函", "the functionals on ℝⁿ",
                       ACCENT_A, FS_TAG, x=bx, w=3.6))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.35, "純量積是雙線性的", "the scalar product is bilinear",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-0.60, "所以這是一個同構", "so this is an isomorphism",
                         ACCENT_A, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.72, "把一個 n 元組送到它的線性泛函，這條對應是自然的",
                         "sending an n-tuple to its functional, and the correspondence is natural",
                         DIM, FS_TAG, w=11.8))

 M = ((2, -1, 0), (1, 4, -2), (0, 2, 5))

 def _two_readings(self):
  dx, dy = 0.72, 0.52
  g = VGroup()
  for cx, mode in ((-3.35, "cells"), (1.65, "cols")):
   for i, row in enumerate(self.M):
    for j, v in enumerate(row):
     g.add(Text(str(v), font_size=FS_TAG + 1, color=INK)
           .move_to([cx + (j - 1) * dx, 0.30 + (1 - i) * dy, 0]))
   if mode == "cells":
    for i in range(3):
     for j in range(3):
      g.add(Rectangle(width=dx - 0.06, height=dy - 0.04, color=GHOST, stroke_width=1.4)
            .move_to([cx + (j - 1) * dx, 0.30 + (1 - i) * dy, 0]))
   else:
    for j in range(3):
     g.add(Rectangle(width=dx - 0.06, height=3 * dy + 0.16,
                     color=(ACCENT_B, ACCENT_C, ACCENT_A)[j], stroke_width=2.5)
           .move_to([cx + (j - 1) * dx, 0.30, 0]))
   g.add(self._mid(-0.85, "兩個指標的函數" if mode == "cells" else "一串行向量",
                   "a function of two indices" if mode == "cells" else "a sequence of columns",
                   DIM if mode == "cells" else ACCENT_A, FS_TAG, x=cx, w=4.4))
  g.add(Text("=", font_size=FS_TAG + 6, color=DIM).move_to([-0.85, 0.30, 0]))
  return g.add(self._mid(-1.72, "這兩個看法之間的對應，就是一個自然同構",
                         "the correspondence between those views is a natural isomorphism",
                         ACCENT_A, FS_TAG, w=11.8))

 def _permanent(self):
  g = VGroup()
  for cx, zh, en, sub_zh, sub_en, col in (
    (-3.05, "一般的同構", "an arbitrary isomorphism", "暫時的認同", "a transient identification", WARN),
    (3.05, "自然同構", "a natural isomorphism", "永久的認同", "a permanent one", ACCENT_A)):
   g.add(Rectangle(width=4.20, height=1.55, color=col, stroke_width=2.5).move_to([cx, 0.35, 0]),
         self._mid(0.72, zh, en, col, FS_TAG + 1, x=cx, w=3.9),
         self._mid(0.00, sub_zh, sub_en, DIM, FS_TAG, x=cx, w=3.9))
  return g.add(self._mid(-1.05, "換一個同構，認同就換一種",
                         "shift to a different isomorphism and the identification changes",
                         WARN, FS_TAG, w=11.8),
               self._mid(-1.72, "而自然同構讓我們直接把矩陣「當成」列、行、或兩個指標的函數",
                         "a natural one lets us think of a matrix as being rows, columns, or a function",
                         ACCENT_A, FS_TAG, w=11.9))

 def stage(self):
  du, sl, nb, nl = self._duality(), self._slices(), self._not_bilinear(), self._not_linear()
  t61, cn, cb = self._thm61(), self._construction(), self._comp_bilinear()
  t62, sc, tr, pm = self._thm62(), self._scalar(), self._two_readings(), self._permanent()
  return [([du], []), ([sl], [du]), ([nb], [sl]), ([nl], [nb]),
          ([t61], [nl]), ([cn], [t61]), ([cb], [cn]), ([t62], [cb]),
          ([sc], [t62]), ([tr], [sc]), ([pm], [tr])]


AdvCalcE17ZH, AdvCalcE17EN = make(AdvCalcE17Base, "17", prefix="AdvCalcE")
