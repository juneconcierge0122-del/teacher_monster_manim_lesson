"""advcalc E12 — Chapter 1, section 3, second half (book pp. 46-52): Theorem
3.4, Hom(V) as an algebra, the injections, and Theorems 3.6 and 3.7.

The section is about taking a linear map apart and putting it back together,
so beats 5 to 8 are one continuous picture: a product space with labelled
slots, the two round trips that define the projection-injection identities,
and then the book's own two-by-three example coming apart into rows and being
reassembled. Drawing the reassembly is the point -- the identity that does it
is a sum of maps, which reads as nothing at all in symbols.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


class AdvCalcE12Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 12

 MODE_LABEL = {
  0: {"zh": "拆成一堆各自獨立的問題", "en": "split into independent questions"},
  1: {"zh": "第 i 個投影接上去，就是第 i 列", "en": "the ith projection gives the ith row"},
  2: {"zh": "一條向量方程換成 m 條純量方程", "en": "one vector equation, m scalar ones"},
  3: {"zh": "向量空間，再加上一個乘法", "en": "a vector space with a multiplication"},
  4: {"zh": "但這個乘法不可交換", "en": "but this multiplication does not commute"},
  5: {"zh": "注入：放進第 j 格，其他放零", "en": "an injection: into slot j, zeros elsewhere"},
  6: {"zh": "投影與注入的三條等式", "en": "three identities relating them"},
  7: {"zh": "把 T 拆成兩個線性泛函", "en": "T comes apart into two functionals"},
  8: {"zh": "再用同一條等式裝回去", "en": "and the same identity puts it back"},
  9: {"zh": "一族映射，恰好裝成一個", "en": "a family of maps, one assembly"},
  10: {"zh": "定義域是積空間時的對稱說法", "en": "the symmetric statement on the domain"},
 }

 SLOTS = (0.78, 0.06, -0.66)

 def _product_box(self, cx, hi=None, labels=("W₁", "W₂", "W₃")):
  """A product space drawn as labelled slots, so an injection has somewhere
  visible to put its vector."""
  g = VGroup(Rectangle(width=1.85, height=2.35, color=DIM, stroke_width=2.5)
             .move_to([cx, 0.06, 0]))
  cols = (ACCENT_B, ACCENT_C, ACCENT_A)
  for k, y in enumerate(self.SLOTS):
   on = hi is not None and k == hi
   g.add(Rectangle(width=1.45, height=0.56,
                   color=cols[k] if on else GHOST, stroke_width=2.5 if on else 1.8)
         .move_to([cx, y, 0]),
         Text(labels[k], font_size=FS_TAG - 3, color=cols[k] if on else DIM)
         .move_to([cx, y, 0]))
  return g

 def _split(self):
  """One arrow into a product, then read out slot by slot."""
  g = VGroup(Ellipse(width=1.60, height=1.70, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.08).move_to([-4.35, 0.06, 0]),
             Text("V", font_size=FS_TAG + 1, color=ACCENT_B).move_to([-4.35, 0.06, 0]),
             self._arr([-3.50, 0.06, 0], [-2.35, 0.06, 0], ACCENT_A, sw=3, tl=0.15),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-2.92, 0.40, 0]),
             self._product_box(-1.35))
  for k, y in enumerate(self.SLOTS):
   g.add(self._arr([-0.35, y, 0], [0.75, y, 0], (ACCENT_B, ACCENT_C, ACCENT_A)[k],
                   sw=2, tl=0.10),
         Text(f"π{k + 1} ∘ T", font_size=FS_TAG - 3,
              color=(ACCENT_B, ACCENT_C, ACCENT_A)[k]).move_to([1.45, y, 0]))
  return g.add(self._mid(0.78, "整體是線性的", "the whole thing is linear",
                         DIM, FS_TAG, x=4.30, w=3.5),
               self._mid(-0.66, "若且唯若每一條都是", "exactly when each of these is",
                         ACCENT_A, FS_TAG, x=4.30, w=3.5),
               self._mid(-1.62, "所以「往積空間裡送」可以拆成一堆各自獨立的問題",
                         "so mapping into a product splits into independent questions",
                         DIM, FS_TAG, w=11.6))

 M = ((2, -1, 1), (1, 1, 4))

 def _matrix(self, cx, cy, hi_row=None, dx=0.72, dy=0.52):
  g = VGroup()
  for i, row in enumerate(self.M):
   for j, v in enumerate(row):
    on = hi_row is not None and i == hi_row
    g.add(Text(str(v), font_size=FS_TAG + 2, color=ACCENT_A if on else DIM)
          .move_to([cx + (j - 1) * dx, cy + (0.5 - i) * dy, 0]))
  if hi_row is not None:
   g.add(Rectangle(width=3 * dx + 0.26, height=dy + 0.10, color=ACCENT_A, stroke_width=2.5)
         .move_to([cx, cy + (0.5 - hi_row) * dy, 0]))
  return g

 def _row(self):
  g = VGroup(self._matrix(-3.35, 0.15, hi_row=0),
             self._arr([-1.75, 0.15, 0], [-0.45, 0.15, 0], ACCENT_A, sw=2.5, tl=0.13),
             Text("π₁ ∘ T", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-1.10, 0.50, 0]),
             Rectangle(width=2.60, height=0.56, color=ACCENT_A, stroke_width=2.5)
             .move_to([0.95, 0.15, 0]),
             Text("⟨ 2 , −1 , 1 ⟩", font_size=FS_TAG - 1, color=ACCENT_A)
             .move_to([0.95, 0.15, 0]))
  return g.add(self._mid(-0.85, "這個線性泛函的 skeleton", "the skeleton of that functional",
                         DIM, FS_TAG, x=0.95, w=5.0),
               self._mid(0.60, "正好就是矩陣的第 i 列", "is exactly the ith row of the matrix",
                         ACCENT_A, FS_TAG, x=4.15, w=3.6),
               self._mid(-1.62, "這把積空間的語言接回了上一節的矩陣",
                         "which ties the product language back to last section's matrix",
                         DIM, FS_TAG, w=11.6))

 def _scalar_eqs(self):
  g = VGroup(Rectangle(width=3.00, height=0.66, color=ACCENT_B, stroke_width=2.5)
             .move_to([-3.35, 0.72, 0]),
             Text("y  =  T ( x )", font_size=FS_TAG + 1, color=ACCENT_B)
             .move_to([-3.35, 0.72, 0]))
  for k, s in enumerate(("y₁  =  2x₁ − x₂ + x₃", "y₂  =  x₁ + x₂ + 4x₃")):
   g.add(Rectangle(width=3.85, height=0.56, color=ACCENT_A, stroke_width=2)
         .move_to([1.35, 0.42 - k * 0.72, 0]),
         Text(s, font_size=FS_TAG - 1, color=ACCENT_A).move_to([1.35, 0.42 - k * 0.72, 0]))
  g.add(self._arr([-1.80, 0.72, 0], [-0.65, 0.42, 0], DIM, sw=2, tl=0.10),
        self._arr([-1.80, 0.72, 0], [-0.65, -0.30, 0], DIM, sw=2, tl=0.10),
        self._mid(-1.05, "讀出第 i 個座標，就是接上第 i 個投影",
                  "reading off the ith coordinate is composing the ith projection",
                  DIM, FS_TAG, w=11.4))
  return g.add(self._mid(-1.62, "用代數的話說：把一個線性映射換成一組線性映射",
                         "algebraically: one linear map replaced by a set of them",
                         ACCENT_A, FS_TAG, w=11.6))

 def _algebra(self):
  g = VGroup(Rectangle(width=4.60, height=2.35, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.55, 0.05, 0]),
             self._mid(0.95, "Hom ( V )", "Hom ( V )", ACCENT_A, FS_TAG, x=-2.55, w=4.2))
  for k, (zh, en, col) in enumerate(((" S + T ", "S + T", ACCENT_B),
                                     (" c S ", "c S", ACCENT_B),
                                     (" S ∘ T ", "S ∘ T", WARN))):
   g.add(Rectangle(width=1.35, height=0.50, color=col, stroke_width=2)
         .move_to([-3.75 + k * 1.20, 0.10, 0]),
         Text(en, font_size=FS_TAG - 2, color=col).move_to([-3.75 + k * 1.20, 0.10, 0]))
  g.add(self._mid(-0.70, "前兩個是向量運算，第三個是新的",
                  "the first two are the vector operations, the third is new",
                  DIM, FS_TAG, x=-2.55, w=4.4))
  return g.add(self._mid(0.85, "合成永遠滿足結合律", "composition is always associative",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(0.05, "加上分配律與純量的相容", "with distributivity and the scalars",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(-0.75, "這種結構就叫代數", "that structure is called an algebra",
                         ACCENT_A, FS_TAG, x=3.35, w=5.2),
               self._mid(-1.62, "之前的實值函數空間也是代數",
                         "the real-valued function spaces are algebras too",
                         DIM, FS_TAG, w=11.4))

 def _noncomm(self):
  """Two orders, two different endpoints. The claim is an inequality, so the
  two results are drawn as visibly different vectors."""
  # S rotates, so S(T(alpha)) reaches much higher than either factor suggests;
  # the origin is set from that composite, not from the input vector.
  o = np.array([-2.35, -0.85, 0.0])
  u = np.array([1.15, 0.30, 0.0])
  S = np.array([[0.30, -0.95, 0], [0.95, 0.30, 0], [0, 0, 1]])
  T = np.array([[1.35, 0.0, 0], [0.0, 0.55, 0], [0, 0, 1]])
  a, b = S @ (T @ u), T @ (S @ u)
  assert float(np.linalg.norm(a - b)) > 0.35, "the two orders must land visibly apart"
  g = VGroup(self._arr(o, o + u, DIM, sw=2.5, tl=0.12),
             self._arr(o, o + a, ACCENT_B, sw=4, tl=0.18),
             self._arr(o, o + b, WARN, sw=4, tl=0.18),
             Dot(o, radius=0.055, color=INK),
             Text("α", font_size=FS_TAG - 2, color=DIM)
             .move_to(o + u + np.array([0.14, -0.22, 0])),
             Text("S ∘ T", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + a + np.array([-0.34, 0.22, 0])),
             Text("T ∘ S", font_size=FS_TAG - 2, color=WARN)
             .move_to(o + b + np.array([0.38, 0.10, 0])))
  return g.add(self._mid(0.85, "換個次序，終點就不一樣", "swap the order, the endpoint moves",
                         WARN, FS_TAG, x=3.20, w=5.4),
               self._mid(-0.65, "所以這個乘法不可交換", "so this multiplication does not commute",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.62, "除非 V 是零空間，或者跟實數線同構",
                         "unless V is trivial or is isomorphic to the real line",
                         DIM, FS_TAG, w=11.4))

 def _injection(self):
  g = VGroup(Ellipse(width=1.60, height=0.70, color=ACCENT_C, stroke_width=2.5)
             .move_to([-4.15, 0.06, 0]),
             Text("W₂", font_size=FS_TAG - 2, color=ACCENT_C).move_to([-4.15, 0.06, 0]),
             self._arr([-3.30, 0.06, 0], [-2.20, 0.06, 0], ACCENT_C, sw=3, tl=0.14),
             Text("θ₂", font_size=FS_TAG, color=ACCENT_C).move_to([-2.75, 0.42, 0]),
             self._product_box(-1.20, hi=1))
  for k, y in enumerate(self.SLOTS):
   if k != 1:
    g.add(Text("0", font_size=FS_TAG, color=DIM).move_to([-1.20, y, 0]))
  return g.add(self._mid(0.85, "把向量放進第 j 格", "put the vector into slot j",
                         ACCENT_C, FS_TAG, x=3.30, w=5.2),
               self._mid(0.05, "其他格全部放零", "and zero into every other slot",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.75, "這就是第 j 個注入", "that is the jth injection",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "投影是往外讀，注入是往裡放",
                         "projections read out; injections put in",
                         DIM, FS_TAG, w=11.4))

 def _identities(self):
  """The three identities as three separate small round trips, kept apart so
  that the one that gives zero is visibly a different journey."""
  g = VGroup()
  rows = ((0.82, "θⱼ", "πⱼ", "Iⱼ", ACCENT_A), (-0.06, "θᵢ", "πⱼ", "0", WARN))
  for y, first, second, out, col in rows:
   ox = -4.15
   for k, (lab, c) in enumerate(((first, ACCENT_C), (second, ACCENT_B))):
    g.add(Rectangle(width=0.86, height=0.50, color=c, stroke_width=2)
          .move_to([ox + k * 1.35, y, 0]),
          Text(lab, font_size=FS_TAG - 2, color=c).move_to([ox + k * 1.35, y, 0]))
    if k == 0:
     g.add(self._arr([ox + 0.48, y, 0], [ox + 0.88, y, 0], DIM, sw=1.8, tl=0.09))
   g.add(self._arr([ox + 1.83, y, 0], [ox + 2.35, y, 0], col, sw=2.2, tl=0.11),
         Rectangle(width=0.86, height=0.50, color=col, stroke_width=2.5)
         .move_to([ox + 2.85, y, 0]),
         Text(out, font_size=FS_TAG - 1, color=col).move_to([ox + 2.85, y, 0]))
  g.add(self._mid(-1.05, "而指標有限時，把每個「注入接投影」加起來就是恆等",
                  "and for a finite index set, summing injection-after-projection is the identity",
                  ACCENT_A, FS_TAG, w=11.8))
  return g.add(self._mid(0.82, "接自己的投影：恆等", "with its own projection: the identity",
                         DIM, FS_TAG, x=3.10, w=5.6),
               self._mid(-0.06, "接別人的投影：零", "with any other: zero",
                         WARN, FS_TAG, x=3.10, w=5.6))

 def _take_apart(self):
  g = VGroup(self._matrix(-3.55, 0.55, hi_row=0, dy=0.56),
             self._matrix(-3.55, -0.95, hi_row=1, dy=0.56))
  for k, (y, lab, col) in enumerate(((0.55, "l₁ = π₁ ∘ T", ACCENT_A),
                                     (-0.95, "l₂ = π₂ ∘ T", ACCENT_A))):
   g.add(self._arr([-1.95, y, 0], [-0.75, y, 0], col, sw=2.2, tl=0.11),
         Rectangle(width=2.85, height=0.52, color=col, stroke_width=2.5).move_to([0.75, y, 0]),
         Text(lab, font_size=FS_TAG - 2, color=col).move_to([0.75, y, 0]))
  return g.add(self._mid(0.55, "第一列給第一個泛函", "the first row gives the first functional",
                         DIM, FS_TAG, x=4.15, w=3.7),
               self._mid(-0.95, "第二列給第二個", "the second row the second",
                         DIM, FS_TAG, x=4.15, w=3.7),
               self._mid(-1.72, "一個到二維的映射，就這樣拆成兩個線性泛函",
                         "so a map into the plane comes apart into two linear functionals",
                         ACCENT_A, FS_TAG, w=11.6))

 def _put_back(self):
  g = VGroup()
  for k, (y, lab, col) in enumerate(((0.72, "l₁", ACCENT_B), (-0.12, "l₂", ACCENT_C))):
   g.add(Rectangle(width=0.92, height=0.50, color=col, stroke_width=2.5)
         .move_to([-4.10, y, 0]),
         Text(lab, font_size=FS_TAG - 1, color=col).move_to([-4.10, y, 0]),
         self._arr([-3.55, y, 0], [-2.60, y, 0], DIM, sw=2, tl=0.10),
         Rectangle(width=0.92, height=0.50, color=col, stroke_width=2)
         .move_to([-2.05, y, 0]),
         Text(f"θ{k + 1}", font_size=FS_TAG - 2, color=col).move_to([-2.05, y, 0]),
         self._arr([-1.50, y, 0], [-0.55, 0.30, 0], DIM, sw=2, tl=0.10))
  g.add(Rectangle(width=1.15, height=0.72, color=ACCENT_A, stroke_width=2.5)
        .move_to([0.05, 0.30, 0]),
        Text("Σ", font_size=FS_TAG + 5, color=ACCENT_A).move_to([0.05, 0.30, 0]),
        self._arr([0.68, 0.30, 0], [1.75, 0.30, 0], ACCENT_A, sw=3, tl=0.15),
        Rectangle(width=1.35, height=0.72, color=ACCENT_A, stroke_width=2.5)
        .move_to([2.50, 0.30, 0]),
        Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([2.50, 0.30, 0]))
  return g.add(self._mid(-1.05, "用的正好是「注入接投影加起來等於恆等」那一條",
                         "using exactly the identity that these sum to the identity map",
                         ACCENT_A, FS_TAG, w=11.8),
               self._mid(-1.65, "拆開與裝回，是同一條等式的兩個方向",
                         "taking apart and putting back are one identity, read two ways",
                         DIM, FS_TAG, w=11.8))

 def _assemble(self):
  ax, bx = -2.75, 1.85
  ys = (0.72, 0.06, -0.60)
  g = VGroup(self._mid(1.15, "一族 Tᵢ", "a family of maps", ACCENT_B, FS_TAG, x=ax, w=3.2),
             self._mid(1.15, "唯一一個 T", "exactly one map", ACCENT_A, FS_TAG, x=bx, w=3.2))
  for y in ys:
   g.add(Rectangle(width=0.92, height=0.48, color=ACCENT_B, stroke_width=2).move_to([ax, y, 0]),
         self._arr([ax + 0.55, y, 0], [bx - 0.62, 0.06, 0], DIM, sw=2, tl=0.10))
  g.add(Rectangle(width=1.15, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([bx, 0.06, 0]),
        Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([bx, 0.06, 0]))
  return g.add(self._mid(-1.15, "從共同定義域出發、分別到各個因子",
                         "out of one common domain, into the separate factors",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.72, "就恰好裝出一個到積空間的線性映射",
                         "assemble into exactly one linear map into the product",
                         ACCENT_A, FS_TAG, w=11.4))

 def _dual(self):
  g = VGroup()
  for cy, zh, en, col, left in ((0.62, "上域是積空間", "the codomain is the product", ACCENT_A, False),
                                (-0.62, "定義域是積空間", "the domain is the product", ACCENT_B, True)):
   ox = -4.05
   g.add(Ellipse(width=1.20, height=0.62, color=DIM, stroke_width=2).move_to([ox, cy, 0]),
         Rectangle(width=1.20, height=0.86, color=col, stroke_width=2.5)
         .move_to([ox + 2.55, cy, 0]) if not left else
         Rectangle(width=1.20, height=0.86, color=col, stroke_width=2.5).move_to([ox, cy, 0]),
         self._arr([ox + 0.72, cy, 0], [ox + 1.90, cy, 0], col, sw=2.2, tl=0.11),
         self._mid(cy, zh, en, col, FS_TAG, x=2.35, w=5.8))
   if left:
    g.add(Ellipse(width=1.20, height=0.62, color=DIM, stroke_width=2).move_to([ox + 2.55, cy, 0]))
  return g.add(self._mid(-1.62, "這個定理對任意積空間都成立，而且其實刻畫了積空間",
                         "the theorem holds for all product spaces and in fact characterizes them",
                         DIM, FS_TAG, w=11.8))

 def stage(self):
  sp, rw, se = self._split(), self._row(), self._scalar_eqs()
  al, nc = self._algebra(), self._noncomm()
  inj, ids = self._injection(), self._identities()
  ta, pb, asm, du = self._take_apart(), self._put_back(), self._assemble(), self._dual()

  return [([sp], []), ([rw], [sp]), ([se], [rw]), ([al], [se]),
          ([nc], [al]), ([inj], [nc]), ([ids], [inj]), ([ta], [ids]),
          ([pb], [ta]), ([asm], [pb]), ([du], [asm])]


AdvCalcE12ZH, AdvCalcE12EN = make(AdvCalcE12Base, "12", prefix="AdvCalcE")
