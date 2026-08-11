"""advcalc E22 — Chapter 2, section 3, second half (book pp. 83-86): annihilator
subspaces, Theorem 3.3 and its corollary, the adjoint of T, Theorems 3.4 and
3.5, rank, dyads with Lemma 3.2, and the commutative square that finally says
what 'natural' means. Book pp. 87-88 are exercises and are not covered.

Two beats carry the weight here. Beat 2 is the proof of the dimension identity,
which is really a picture: lay the extended basis out in a row, cut it where W
stops, and the dual basis vectors past the cut are the annihilator's basis --
the counting is then visible rather than asserted. Beat 10 is the square, and it
is drawn as a square on purpose: 'natural' is a statement about two paths
agreeing, and the two paths have to be traceable on screen for that to land.

Symbols follow E21 rather than the book: beta for a basis of V, epsilon for its
dual basis, lambda for a functional. The book writes the dual basis of Theorem
3.3 as lambda, which would collide with the lambda of the dyad four beats later;
the dyad's vector in W is eta rather than the book's beta for the same reason.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Ellipse, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# One constant for both rows of the basis strip in beat 2. E18, E19 and E21 all
# shipped a row whose subscripts disagreed with the row directly above it,
# because each row spelled its own index string out by hand; the bounds check
# passes (the glyphs are inside the frame) and reading the formula bar alone
# passes too. Sharing the tuple is what makes the two rows unable to disagree.
SUBS = ("₁", "ₘ", "ₘ₊₁", "ₙ")
COLX = (-4.35, -2.95, -0.85, 0.55)
DOTX = (-3.65, -0.15)


class AdvCalcE22Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 22

 MODE_LABEL = {
  0: {"zh": "零化子：對偶版本的正交", "en": "the annihilator: orthogonality in the dual"},
  1: {"zh": "反過來的定義，與五條性質", "en": "the definition the other way, and five properties"},
  2: {"zh": "維數在子空間與零化子之間分完", "en": "the dimensions split between the two"},
  3: {"zh": "零化兩次得到線性擴張", "en": "annihilating twice gives the linear span"},
  4: {"zh": "伴隨算子：把泛函沿著映射拉回來", "en": "the adjoint: pull functionals back along the map"},
  5: {"zh": "這個對應本身就是同構", "en": "the correspondence is itself an isomorphism"},
  6: {"zh": "合成的順序會反過來", "en": "composition reverses the order"},
  7: {"zh": "零空間與值域互換", "en": "null spaces and ranges trade places"},
  8: {"zh": "秩相等", "en": "the ranks are equal"},
  9: {"zh": "值域一維的映射就是 dyad", "en": "a one-dimensional range makes a dyad"},
  10: {"zh": "自然的意思：這張圖可交換", "en": "what natural means: the square commutes"},
 }

 def _sym(self, y, s, color, size=FS_TAG, x=0.0, w=11.0):
  """A language independent line of symbols, scaled to fit like a caption."""
  return self._mid(y, s, s, color, size, x, w)

 def _annihilator(self):
  g = VGroup(Ellipse(width=2.30, height=1.30, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-3.60, 0.30, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-3.60, 1.15, 0]),
             Ellipse(width=1.30, height=0.62, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.16).move_to([-3.60, 0.15, 0]),
             Text("A", font_size=FS_TAG, color=ACCENT_C).move_to([-3.60, 0.72, 0]),
             Line([-0.75, -0.35, 0], [-0.75, 0.95, 0], color=DIM, stroke_width=2.5),
             Text("ℝ", font_size=FS_TAG, color=DIM).move_to([-0.42, 0.90, 0]),
             Dot([-0.75, 0.15, 0], radius=0.07, color=ACCENT_C),
             Text("0", font_size=FS_TAG, color=DIM).move_to([-1.10, 0.15, 0]),
             Ellipse(width=2.30, height=1.30, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.07).move_to([2.70, 0.30, 0]),
             Text("V *", font_size=FS_TAG + 2, color=ACCENT_A).move_to([2.70, 1.15, 0]),
             Ellipse(width=1.45, height=0.62, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.16).move_to([2.70, 0.15, 0]),
             Text("A °", font_size=FS_TAG, color=ACCENT_C).move_to([2.70, 0.15, 0]))
  for y in (0.33, 0.15, -0.03):
   g.add(Dot([-3.75, y, 0], radius=0.055, color=ACCENT_C),
         self._arr([-2.90, y, 0], [-0.92, 0.15, 0], ACCENT_C, sw=2, tl=0.10))
  return g.add(self._mid(-0.78, "A° 收集的是在 A 上整個取零的那些泛函",
                         "A° collects the functionals that vanish on all of A",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.32, "只要有一個向量沒被送到零，那個泛函就不算數",
                         "one vector that is not sent to zero disqualifies a functional",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "正交是在這裡第一次自然出現，但那個詞留到第 5 章",
                         "orthogonality first appears here, but the word waits for chapter five",
                         ACCENT_A, FS_TAG, w=11.9))

 def _both_ways(self):
  rows = ((0.85, "A ⊂ V", ACCENT_B, "A ° ⊂ V *", ACCENT_A,
           "第一個方向", "the first direction"),
          (0.05, "A ⊂ V *", ACCENT_A, "A ° ⊂ V", ACCENT_B,
           "反過來的方向", "the other direction"))
  g = VGroup()
  for y, ls, lc, rs, rc, zh, en in rows:
   g.add(Rectangle(width=2.60, height=0.60, color=lc, stroke_width=2.5).move_to([-4.00, y, 0]),
         Text(ls, font_size=FS_TAG + 1, color=lc).move_to([-4.00, y, 0]),
         self._arr([-2.62, y, 0], [-1.88, y, 0], DIM, sw=2, tl=0.10),
         Text("( · ) °", font_size=FS_TAG - 3, color=DIM).move_to([-2.25, y + 0.30, 0]),
         Rectangle(width=2.80, height=0.60, color=rc, stroke_width=2.5).move_to([-0.40, y, 0]),
         Text(rs, font_size=FS_TAG + 1, color=rc).move_to([-0.40, y, 0]),
         self._mid(y, zh, en, rc, FS_TAG, x=3.60, w=4.80))
  return g.add(self._mid(-0.80, "把 V 跟第二共軛空間認同之後，第二個定義就是第一個的特例",
                         "identify V with its second conjugate and the second is a case of the first",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.32, "五條性質留作習題，其中換成線性擴張零化子不變",
                         "five properties are exercises: passing to the span changes nothing",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "而且任何集合都被包在它的雙重零化子裡——下一拍要用",
                         "and every set sits inside its double annihilator, which the next beat needs",
                         ACCENT_A, FS_TAG, w=11.9))

 def _thm33(self):
  """The proof laid out as a strip. The cut after the mth column is where W
  stops; the dual basis vectors to the right of it are what Theorem 3.3 claims
  is a basis for the annihilator, so the count n = m + (n - m) is on screen
  rather than in the narration only."""
  g = VGroup(Text("V", font_size=FS_TAG, color=ACCENT_B).move_to([-5.55, 0.78, 0]),
             Text("V *", font_size=FS_TAG, color=ACCENT_A).move_to([-5.55, -0.02, 0]))
  for k, (sub, x) in enumerate(zip(SUBS, COLX)):
   past = k >= 2                                # past the cut: these span W°
   w = 1.10 if sub == "ₘ₊₁" else 0.92
   g.add(Rectangle(width=w, height=0.55, color=ACCENT_B, stroke_width=2).move_to([x, 0.78, 0]),
         Text(f"β{sub}", font_size=FS_TAG - 3, color=ACCENT_B).move_to([x, 0.78, 0]),
         Rectangle(width=w, height=0.55, color=ACCENT_C if past else DIM,
                   stroke_width=2.5 if past else 2).move_to([x, -0.02, 0]),
         Text(f"ε{sub}", font_size=FS_TAG - 3,
              color=ACCENT_C if past else DIM).move_to([x, -0.02, 0]))
  for x in DOTX:
   g.add(Text("…", font_size=FS_TAG, color=DIM).move_to([x, 0.78, 0]),
         Text("…", font_size=FS_TAG, color=DIM).move_to([x, -0.02, 0]))
  return g.add(self._dash([-1.90, 1.16, 0], [-1.90, -0.37, 0], DIM, n=9, sw=2),
               Text("W", font_size=FS_TAG, color=ACCENT_B).move_to([-3.65, 1.17, 0]),
               Text("W °", font_size=FS_TAG, color=ACCENT_C).move_to([-0.15, -0.57, 0]),
               self._mid(0.78, "取 W 的基底，延長成 V 的基底",
                         "a basis for W, extended to one for V",
                         ACCENT_B, FS_TAG, x=3.90, w=4.40),
               self._mid(-0.02, "再看它的對偶基底", "then look at its dual basis",
                         ACCENT_A, FS_TAG, x=3.90, w=4.40),
               self._mid(-1.00, "延長出來的那一段所對應的泛函，正好生成零化子",
                         "the functionals matching the added vectors span the annihilator",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.45, "剩下的那一段對 W 不取零，所以進不了零化子",
                         "the ones before the cut do not vanish on W, so they stay out",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "數一數兩段的長度，就是那條維數等式",
                         "counting the two stretches is the dimension identity",
                         ACCENT_A, FS_TAG, w=11.9))

 def _corollary(self):
  g = VGroup(Rectangle(width=1.60, height=0.62, color=DIM, stroke_width=2).move_to([-4.00, 0.78, 0]),
             Text("A", font_size=FS_TAG + 1, color=DIM).move_to([-4.00, 0.78, 0]),
             Text("⊂", font_size=FS_TAG + 1, color=DIM).move_to([-3.00, 0.78, 0]),
             Rectangle(width=2.20, height=0.62, color=ACCENT_B, stroke_width=2.5)
             .move_to([-1.70, 0.78, 0]),
             Text("L ( A )", font_size=FS_TAG + 1, color=ACCENT_B).move_to([-1.70, 0.78, 0]),
             Text("⊂", font_size=FS_TAG + 1, color=DIM).move_to([-0.33, 0.78, 0]),
             Rectangle(width=2.20, height=0.62, color=ACCENT_C, stroke_width=2.5)
             .move_to([1.05, 0.78, 0]),
             Text("A ° °", font_size=FS_TAG + 1, color=ACCENT_C).move_to([1.05, 0.78, 0]),
             self._arr([-1.70, 0.44, 0], [-1.70, 0.08, 0], DIM, sw=2, tl=0.10),
             self._arr([1.05, 0.44, 0], [1.05, 0.08, 0], DIM, sw=2, tl=0.10),
             Rectangle(width=5.60, height=0.62, color=ACCENT_A, stroke_width=2.5)
             .move_to([-0.35, -0.25, 0]),
             self._sym(-0.25, "d ( L ( A ) )  =  d ( A ° ° )", ACCENT_A, FS_TAG + 1,
                       x=-0.35, w=5.35),
             self._arr([-0.35, -0.60, 0], [-0.35, -0.95, 0], WARN, sw=2.5, tl=0.11),
             Rectangle(width=3.40, height=0.62, color=WARN, stroke_width=2.5)
             .move_to([-0.35, -1.28, 0]),
             self._sym(-1.28, "L ( A )  =  A ° °", WARN, FS_TAG + 1, x=-0.35, w=3.15))
  return g.add(self._mid(0.78, "包含關係本來就有", "the inclusion comes for free",
                         DIM, FS_TAG, x=4.20, w=3.80),
               self._mid(-0.25, "維數等式用兩次", "apply the identity twice",
                         ACCENT_A, FS_TAG, x=4.20, w=3.80),
               self._mid(-1.28, "所以兩邊只好一樣", "so the two must coincide",
                         WARN, FS_TAG, x=4.20, w=3.80),
               self._mid(-1.78, "對任何子集都成立，不必先假設它是子空間",
                         "true for any subset at all, no need to assume it is a subspace",
                         ACCENT_C, FS_TAG, w=11.9))

 def _adjoint(self):
  g = VGroup(Rectangle(width=1.40, height=0.62, color=ACCENT_B, stroke_width=2.5)
             .move_to([-3.60, 0.95, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-3.60, 0.95, 0]),
             Rectangle(width=1.40, height=0.62, color=ACCENT_B, stroke_width=2.5)
             .move_to([-0.60, 0.95, 0]),
             Text("W", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-0.60, 0.95, 0]),
             Rectangle(width=1.40, height=0.62, color=DIM, stroke_width=2)
             .move_to([2.30, 0.95, 0]),
             Text("ℝ", font_size=FS_TAG + 2, color=DIM).move_to([2.30, 0.95, 0]),
             self._arr([-2.85, 0.95, 0], [-1.35, 0.95, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-2.10, 1.17, 0]),
             self._arr([0.15, 0.95, 0], [1.55, 0.95, 0], ACCENT_C, sw=2.5, tl=0.12),
             Text("l", font_size=FS_TAG, color=ACCENT_C).move_to([0.85, 1.17, 0]),
             Line([-3.60, 0.63, 0], [-3.60, 0.42, 0], color=DIM, stroke_width=1.6),
             Line([2.30, 0.63, 0], [2.30, 0.42, 0], color=DIM, stroke_width=1.6),
             self._arr([-3.60, 0.42, 0], [2.30, 0.42, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("l ∘ T", font_size=FS_TAG, color=ACCENT_A).move_to([-0.65, 0.14, 0]),
             Rectangle(width=1.80, height=0.60, color=ACCENT_A, stroke_width=2.5)
             .move_to([0.90, -0.60, 0]),
             Text("W *", font_size=FS_TAG + 1, color=ACCENT_A).move_to([0.90, -0.60, 0]),
             Rectangle(width=1.80, height=0.60, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.70, -0.60, 0]),
             Text("V *", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-2.70, -0.60, 0]),
             self._arr([-0.05, -0.60, 0], [-1.75, -0.60, 0], WARN, sw=2.5, tl=0.13),
             Text("T *", font_size=FS_TAG, color=WARN).move_to([-0.90, -0.94, 0]))
  return g.add(self._mid(0.95, "先走 T，再套一個泛函", "go along T, then apply a functional",
                         ACCENT_C, FS_TAG, x=4.30, w=3.60),
               self._mid(-0.60, "得到的對應是線性的", "what results is a linear map",
                         ACCENT_A, FS_TAG, x=4.30, w=3.60),
               self._mid(-1.35, "合成出來的是 V 上的泛函，所以對應落在 V 的對偶空間裡",
                         "the composite is a functional on V, so the map lands in the dual of V",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "注意箭頭反向：V 到 W，但 W 的對偶到 V 的對偶",
                         "the arrow reverses: V to W, but W dual to V dual",
                         WARN, FS_TAG, w=11.9))

 def _thm34(self):
  g = VGroup(Rectangle(width=3.40, height=0.66, color=ACCENT_B, stroke_width=2.5)
             .move_to([-3.50, 0.95, 0]),
             Text("Hom ( V , W )", font_size=FS_TAG, color=ACCENT_B).move_to([-3.50, 0.95, 0]),
             self._arr([-1.75, 0.95, 0], [-0.35, 0.95, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T  ↦  T *", font_size=FS_TAG - 1, color=ACCENT_A).move_to([-1.05, 1.17, 0]),
             Rectangle(width=3.60, height=0.66, color=ACCENT_A, stroke_width=2.5)
             .move_to([1.75, 0.95, 0]),
             Text("Hom ( W * , V * )", font_size=FS_TAG, color=ACCENT_A).move_to([1.75, 0.95, 0]),
             Text("m n", font_size=FS_TAG, color=ACCENT_B).move_to([-3.50, 0.36, 0]),
             Text("=", font_size=FS_TAG, color=DIM).move_to([-0.85, 0.36, 0]),
             Text("m n", font_size=FS_TAG, color=ACCENT_A).move_to([1.75, 0.36, 0]))
  chain = ((-3.40, 2.40, "T  ≠  0", ACCENT_C),
           (-0.35, 2.90, "T ( α )  ≠  0", ACCENT_C),
           (2.85, 2.90, "T * ( l )  ≠  0", WARN))
  for x, w, s, col in chain:
   g.add(Rectangle(width=w, height=0.58, color=col, stroke_width=2.5).move_to([x, -0.42, 0]),
         Text(s, font_size=FS_TAG, color=col).move_to([x, -0.42, 0]))
  return g.add(self._arr([-2.15, -0.42, 0], [-1.85, -0.42, 0], DIM, sw=2, tl=0.09),
               self._arr([1.15, -0.42, 0], [1.35, -0.42, 0], DIM, sw=2, tl=0.09),
               self._mid(-1.10, "不是零的映射，一定找得到不是零的伴隨算子",
                         "a map that is not zero always has an adjoint that is not zero",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.50, "線性來自合成對兩個位置都是線性的",
                         "linearity comes from composition being linear in each slot",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "嵌射加上兩邊維數相同，就是同構",
                         "injective, plus equal dimensions, gives an isomorphism",
                         ACCENT_A, FS_TAG, w=11.9))

 def _reverse(self):
  top = ((-4.20, "U"), (-1.40, "V"), (1.40, "W"))
  bot = ((-4.20, "W *"), (-1.40, "V *"), (1.40, "U *"))
  g = VGroup()
  for x, s in top:
   g.add(Rectangle(width=1.30, height=0.60, color=ACCENT_B, stroke_width=2.5)
         .move_to([x, 0.90, 0]),
         Text(s, font_size=FS_TAG + 2, color=ACCENT_B).move_to([x, 0.90, 0]))
  for x, s in bot:
   g.add(Rectangle(width=1.50, height=0.60, color=ACCENT_A, stroke_width=2.5)
         .move_to([x, -0.30, 0]),
         Text(s, font_size=FS_TAG + 1, color=ACCENT_A).move_to([x, -0.30, 0]))
  g.add(self._arr([-3.50, 0.90, 0], [-2.10, 0.90, 0], ACCENT_B, sw=2.5, tl=0.12),
        Text("S", font_size=FS_TAG, color=ACCENT_B).move_to([-2.80, 1.20, 0]),
        self._arr([-0.70, 0.90, 0], [0.70, 0.90, 0], ACCENT_C, sw=2.5, tl=0.12),
        Text("T", font_size=FS_TAG, color=ACCENT_C).move_to([0.00, 1.20, 0]),
        self._arr([-3.40, -0.30, 0], [-2.20, -0.30, 0], ACCENT_C, sw=2.5, tl=0.12),
        Text("T *", font_size=FS_TAG, color=ACCENT_C).move_to([-2.80, -0.62, 0]),
        self._arr([-0.60, -0.30, 0], [0.60, -0.30, 0], ACCENT_B, sw=2.5, tl=0.12),
        Text("S *", font_size=FS_TAG, color=ACCENT_B).move_to([0.00, -0.62, 0]))
  return g.add(self._mid(0.90, "先 S 再 T", "S first, then T",
                         ACCENT_B, FS_TAG, x=4.30, w=3.60),
               self._mid(-0.30, "先 T* 再 S*", "T star first, then S star",
                         ACCENT_C, FS_TAG, x=4.30, w=3.60),
               self._mid(-1.20, "往回拉的時候，最後施加的那一步最先被遇到",
                         "pulling back, the step applied last is the one met first",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "所以取伴隨算子時，合成的順序整個反過來",
                         "so taking adjoints of a composition reverses the order",
                         ACCENT_A, FS_TAG, w=11.9))

 def _thm35(self):
  g = VGroup(Ellipse(width=2.50, height=1.30, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-3.70, 0.40, 0]),
             Text("W", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-3.70, 1.17, 0]),
             Ellipse(width=1.50, height=0.62, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.16).move_to([-3.70, 0.30, 0]),
             Text("R ( T )", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-3.70, 0.30, 0]),
             Ellipse(width=2.50, height=1.30, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.07).move_to([-0.20, 0.40, 0]),
             Text("W *", font_size=FS_TAG + 2, color=ACCENT_A).move_to([-0.20, 1.17, 0]),
             Ellipse(width=1.70, height=0.62, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.16).move_to([-0.20, 0.30, 0]),
             Text("N ( T * )", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-0.20, 0.30, 0]),
             self._arr([-2.85, 0.30, 0], [-1.15, 0.30, 0], ACCENT_C, sw=2.5, tl=0.12),
             Text("( · ) °", font_size=FS_TAG - 2, color=ACCENT_C).move_to([-2.00, -0.05, 0]),
             Rectangle(width=8.00, height=0.62, color=ACCENT_A, stroke_width=2.5)
             .move_to([-1.40, -0.62, 0]),
             self._sym(-0.62, "T * ( l ) = 0    ⇔    l ∘ T = 0    ⇔    l ( T ( ξ ) ) = 0  ∀ ξ",
                       ACCENT_A, FS_TAG, x=-1.40, w=7.75))
  return g.add(self._mid(0.40, "值域住在 W 裡", "the range lives in W",
                         ACCENT_B, FS_TAG, x=4.55, w=3.10),
               self._mid(-0.62, "每一步只是換句話說", "each step is a restatement",
                         ACCENT_A, FS_TAG, x=4.55, w=3.10),
               self._mid(-1.32, "另一條的證明對稱，書上留給讀者",
                         "the other identity is proved the same way and is left to the reader",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "零空間與值域在兩邊互換了位置",
                         "null spaces and ranges have traded places across the two sides",
                         ACCENT_C, FS_TAG, w=11.9))

 def _rank(self):
  """The array is drawn as dots inside one pair of brackets rather than as a
  grid of cells: E07's matrix drew a box per column, wider than the column
  spacing, and the shared edges turned the array into a table."""
  g = VGroup()
  for i in range(3):
   for j in range(4):
    g.add(Dot([-4.20 + j * 0.55, 0.85 - i * 0.42, 0], radius=0.055, color=INK))
  for x, d in ((-4.55, 0.16), (-2.20, -0.16)):
   g.add(Line([x, 1.05, 0], [x, -0.19, 0], color=DIM, stroke_width=2.5),
         Line([x, 1.05, 0], [x + d, 1.05, 0], color=DIM, stroke_width=2.5),
         Line([x, -0.19, 0], [x + d, -0.19, 0], color=DIM, stroke_width=2.5))
  g.add(Line([-4.42, 0.85, 0], [-2.33, 0.85, 0], color=ACCENT_B, stroke_width=3),
        Line([-4.20, 1.00, 0], [-4.20, -0.14, 0], color=ACCENT_C, stroke_width=3))
  return g.add(self._mid(0.85, "橫列生成的空間", "the space the rows span",
                         ACCENT_B, FS_TAG, x=3.00, w=5.60),
               self._mid(0.25, "直行生成的空間", "the space the columns span",
                         ACCENT_C, FS_TAG, x=3.00, w=5.60),
               Rectangle(width=6.00, height=0.62, color=ACCENT_A, stroke_width=2.5)
               .move_to([-0.60, -0.62, 0]),
               self._sym(-0.62, "d ( R ( T ) )  =  d ( V ) − d ( N ( T ) )  =  d ( R ( T * ) )",
                         ACCENT_A, FS_TAG - 1, x=-0.60, w=5.75),
               self._mid(-1.30, "兩條定理接起來，維數從兩邊被夾成同一個數",
                         "the two theorems squeeze both sides down to the same number",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "這就是後面矩陣的秩，橫列與直行生成的空間一樣大",
                         "this is what rank will mean for a matrix later on",
                         ACCENT_A, FS_TAG, w=11.9))

 def _dyad(self):
  # Every arrow head and the marked vector land on M by construction rather
  # than by hand-placed coordinates: the whole point of the beat is that the
  # range is that one line, and a head sitting just off it would say otherwise.
  p0, d = (-0.05, -0.05), (1.80, 0.80)
  on = lambda t: [p0[0] + t * d[0], p0[1] + t * d[1], 0]
  g = VGroup(Ellipse(width=2.40, height=1.30, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-4.00, 0.35, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-4.00, 1.15, 0]),
             Ellipse(width=2.80, height=1.35, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.07).move_to([0.90, 0.35, 0]),
             Text("W", font_size=FS_TAG + 2, color=ACCENT_A).move_to([0.90, 1.16, 0]),
             Line(on(0.0), on(1.0), color=ACCENT_C, stroke_width=3),
             Text("M", font_size=FS_TAG - 2, color=ACCENT_C).move_to([2.00, 0.60, 0]),
             Dot(on(0.75), radius=0.07, color=ACCENT_C),
             Text("η", font_size=FS_TAG, color=ACCENT_C).move_to([1.48, 0.30, 0]))
  for y, t in ((0.72, 0.20), (0.40, 0.45), (0.08, 0.68)):
   g.add(Dot([-4.35, y, 0], radius=0.055, color=ACCENT_B),
         self._arr([-3.00, y, 0], on(t), DIM, sw=1.8, tl=0.09))
  chain = ((-3.90, "V", ACCENT_B), (-1.60, "ℝ", DIM), (0.70, "M", ACCENT_C))
  for x, s, col in chain:
   g.add(Rectangle(width=1.30, height=0.58, color=col, stroke_width=2.5).move_to([x, -0.68, 0]),
         Text(s, font_size=FS_TAG + 1, color=col).move_to([x, -0.68, 0]))
  return g.add(self._arr([-3.20, -0.68, 0], [-2.30, -0.68, 0], ACCENT_A, sw=2.5, tl=0.11),
               Text("λ", font_size=FS_TAG, color=ACCENT_A).move_to([-2.75, -1.00, 0]),
               self._arr([-0.90, -0.68, 0], [0.00, -0.68, 0], ACCENT_C, sw=2.5, tl=0.11),
               Text("· η", font_size=FS_TAG, color=ACCENT_C).move_to([-0.45, -1.00, 0]),
               self._mid(-0.68, "整個映射拆成兩步", "the whole map factors in two steps",
                         DIM, FS_TAG, x=4.30, w=3.60),
               self._mid(-1.38, "係數對輸入是線性的，所以它就是一個泛函",
                         "the coefficient depends linearly on the input, so it is a functional",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.74, "伴隨算子也是 dyad，泛函與向量兩個角色恰好互換",
                         "the adjoint is a dyad too, with the functional and the vector exchanged",
                         ACCENT_A, FS_TAG, w=11.9))

 def _naturality(self):
  g = VGroup(Rectangle(width=1.50, height=0.60, color=ACCENT_B, stroke_width=2.5)
             .move_to([-2.60, 0.95, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-2.60, 0.95, 0]),
             Rectangle(width=1.50, height=0.60, color=ACCENT_B, stroke_width=2.5)
             .move_to([1.60, 0.95, 0]),
             Text("W", font_size=FS_TAG + 2, color=ACCENT_B).move_to([1.60, 0.95, 0]),
             Rectangle(width=2.00, height=0.60, color=ACCENT_A, stroke_width=2.5)
             .move_to([-2.60, -0.55, 0]),
             Text("V * *", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-2.60, -0.55, 0]),
             Rectangle(width=2.00, height=0.60, color=ACCENT_A, stroke_width=2.5)
             .move_to([1.60, -0.55, 0]),
             Text("W * *", font_size=FS_TAG + 1, color=ACCENT_A).move_to([1.60, -0.55, 0]),
             self._arr([-1.80, 0.95, 0], [0.80, 0.95, 0], ACCENT_B, sw=2.5, tl=0.13),
             Text("T", font_size=FS_TAG, color=ACCENT_B).move_to([-0.50, 1.17, 0]),
             self._arr([-1.55, -0.55, 0], [0.55, -0.55, 0], ACCENT_A, sw=2.5, tl=0.13),
             Text("T * *", font_size=FS_TAG, color=ACCENT_A).move_to([-0.50, -0.90, 0]),
             self._arr([-2.60, 0.62, 0], [-2.60, -0.28, 0], ACCENT_C, sw=2.5, tl=0.12),
             Text("φ", font_size=FS_TAG, color=ACCENT_C).move_to([-3.05, 0.18, 0]),
             self._arr([1.60, 0.62, 0], [1.60, -0.28, 0], ACCENT_C, sw=2.5, tl=0.12),
             Text("ψ", font_size=FS_TAG, color=ACCENT_C).move_to([2.05, 0.18, 0]))
  return g.add(self._mid(0.95, "先走 T，再往下", "along T, then down",
                         ACCENT_B, FS_TAG, x=4.50, w=3.20),
               self._mid(-0.55, "先往下，再走 T**", "down first, then along T star star",
                         ACCENT_A, FS_TAG, x=4.50, w=3.20),
               self._mid(-1.30, "自然的意思是：這個方框對任何 V、W 與 T 都可交換",
                         "natural means this square commutes for every V, W and T",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集進第 4 節，矩陣",
                         "next time: section four, matrices",
                         DIM, FS_TAG, w=11.6))

 def stage(self):
  an, bw, t33 = self._annihilator(), self._both_ways(), self._thm33()
  co, ad, t34 = self._corollary(), self._adjoint(), self._thm34()
  rv, t35, rk = self._reverse(), self._thm35(), self._rank()
  dy, na = self._dyad(), self._naturality()
  return [([an], []), ([bw], [an]), ([t33], [bw]), ([co], [t33]),
          ([ad], [co]), ([t34], [ad]), ([rv], [t34]), ([t35], [rv]),
          ([rk], [t35]), ([dy], [rk]), ([na], [dy])]


AdvCalcE22ZH, AdvCalcE22EN = make(AdvCalcE22Base, "22", prefix="AdvCalcE")
