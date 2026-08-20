"""advcalc E26 -- Chapter 2, section 5 (book pp. 99-101): the trace functional
and Theorem 5.1 that characterises it, the determinant's geometric meaning, the
five properties the book assumes of it, Theorem 5.2 in two dimensions, and
Theorems 5.3 to 5.5 including Cramer's rule. The section's content ends on
p. 101; pp. 101-102 are exercises 5.1-5.12 and are not covered.

Two things about this section need care. The determinant's *existence* is not
proved here -- the book defers it to chapter 7 and simply assumes a function
with five properties -- so the beats say "assumed" where the book says assumed;
claiming otherwise would misrepresent what has been established. And the five
properties are stated for a Delta that is not yet known to exist, which is a
different logical status from the trace, whose existence beat 2 actually
constructs.

Beat 2 draws the swapping property as one grid of products read two ways rather
than as a chain of sigmas, because the content is that both sums range over the
same set of products. Beat 7 redesigns the book's Fig. 2.3: rather than a
rectangle beside its sheared image, the space is drawn as a stack of layers that
slide without deforming, which is why the volume survives -- the picture then
carries the reason and not only the fact. Beat 4 deliberately echoes E23's "one
map, two matrices" composition, since the trace's basis independence is exactly
a statement about that pair of matrices.

Symbols continue E23 to E25: β for a basis of V, t and s for matrices, T and S
for maps. λ is the trace functional, the letter E21 and E22 used for a
functional generally, here for the one this section singles out; Δ is the
determinant and c the coefficient matrix of the uniqueness argument.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Polygon, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# The trace beats need a square matrix, so this episode's worked example is
# n by n with n = 3. Beat 9 draws a genuine 2 by 2 instead, because Theorem 5.2
# is the two-dimensional case and nothing else -- that is not a second example
# contradicting the first.
NSQ = 3
IDX = ("₁", "₂", "₃")

assert len(IDX) == NSQ


class AdvCalcE26Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 26

 MODE_LABEL = {
  0: {"zh": "兩個特別的實數值函數", "en": "two special real-valued functions"},
  1: {"zh": "定理 5.1：這三個條件只留下一個泛函",
      "en": "theorem 5.1: three conditions leave one functional"},
  2: {"zh": "存在性：同一堆乘積，兩種讀法",
      "en": "existence: one set of products, read two ways"},
  3: {"zh": "唯一性：條件把係數逼成單位矩陣",
      "en": "uniqueness: the conditions force the coefficients"},
  4: {"zh": "同一個變換，兩組基底，同一個跡",
      "en": "one map, two bases, one trace"},
  5: {"zh": "行列式的絕對值是體積的倍率",
      "en": "the determinant's size is the volume factor"},
  6: {"zh": "正負號記錄定向", "en": "the sign records orientation"},
  7: {"zh": "書上假設的五條性質：乘法性與剪切",
      "en": "five assumed properties: products and shearings"},
  8: {"zh": "直和、一維、二維互換", "en": "direct sums, one dimension, a swap"},
  9: {"zh": "定理 5.2：二維的公式", "en": "theorem 5.2: the two-dimensional formula"},
  10: {"zh": "轉置、可逆，與 Cramer 法則",
       "en": "transposes, invertibility, and Cramer's rule"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _two_functions(self):
  g = VGroup(self._box(-4.30, 0.55, "Hom ( V )", ACCENT_B, w=2.60, h=0.62, size=FS_TAG),
             self._arr([-3.00, 0.75, 0], [-1.05, 1.00, 0], ACCENT_A, sw=2.5, tl=0.12),
             self._arr([-3.00, 0.35, 0], [-1.05, 0.10, 0], ACCENT_C, sw=2.5, tl=0.12),
             self._box(-0.30, 1.00, "λ", ACCENT_A, w=1.10, h=0.54),
             self._box(-0.30, 0.10, "Δ", ACCENT_C, w=1.10, h=0.54),
             Line([1.60, -0.35, 0], [1.60, 1.30, 0], color=DIM, stroke_width=2.5),
             Text("ℝ", font_size=FS_TAG, color=DIM).move_to([2.00, 1.20, 0]),
             Dot([1.60, 1.00, 0], radius=0.07, color=ACCENT_A),
             Dot([1.60, 0.10, 0], radius=0.07, color=ACCENT_C),
             self._arr([0.30, 1.00, 0], [1.42, 1.00, 0], DIM, sw=2, tl=0.10),
             self._arr([0.30, 0.10, 0], [1.42, 0.10, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(1.00, "跡", "the trace", ACCENT_A, FS_TAG, x=3.60, w=3.00),
               self._mid(0.10, "行列式", "the determinant", ACCENT_C, FS_TAG, x=3.60, w=3.00),
               self._mid(-0.85, "兩個都把一個線性變換送到一個數",
                         "both send a linear transformation to a number",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.32, "兩個都與基底的選擇無關，雖然定義的時候都要先選一組基底",
                         "both are independent of the basis, though defining them needs one",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "但兩者的處境不同：跡這一節就造得出來，行列式的存在性留到第 7 章",
                         "their standing differs: the trace is built here, the determinant is not",
                         WARN, FS_TAG, w=11.9))

 def _thm51(self):
  """The three conditions on the left, the one surviving functional and its
  formula on the right. The highlighted cells are the diagonal by
  construction, not by hand-placed coordinates."""
  conds = ((0.95, "λ  ∈  ( Hom V ) *", ACCENT_B),
           (0.25, "λ ( S ∘ T )  =  λ ( T ∘ S )", ACCENT_A),
           (-0.45, "λ ( I )  =  n", ACCENT_C))
  g = VGroup()
  for y, s, col in conds:
   g.add(self._box(-4.00, y, s, col, w=4.20, h=0.58, size=FS_TAG - 1))
  arr, pos = self._array(1.90, 0.25, NSQ, NSQ, dx=0.55, dy=0.50)
  g.add(self._arr([-1.75, 0.25, 0], [-0.70, 0.25, 0], WARN, sw=2.5, tl=0.12),
        Text("∃ !", font_size=FS_TAG - 2, color=WARN).move_to([-1.22, 0.55, 0]),
        arr)
  for k in range(NSQ):
   g.add(Dot(pos(k, k), radius=0.09, color=WARN))
  return g.add(Text("t", font_size=FS_TAG - 3, color=DIM).move_to([1.90, -0.62, 0]),
               self._mid(0.25, "主對角線的和", "the sum down the diagonal",
                         WARN, FS_TAG, x=4.60, w=3.20),
               self._mid(-1.06, "三個條件放在一起，只剩下一個泛函符合",
                         "put the three conditions together and only one functional survives",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.42, "而它在任何基底下，都等於矩陣主對角線上元素的和",
                         "and in any basis it is the sum of the entries down the main diagonal",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "第二個條件才是關鍵：它是這個泛函與眾不同的地方",
                         "the second condition is the one that singles this functional out",
                         DIM, FS_TAG, w=11.9))

 def _existence(self):
  """One grid of products, read along rows and along columns. The two sums
  of the theorem range over the same cells, which is the whole argument, and
  a chain of sigmas on screen would just be the formula bar again."""
  g = VGroup()
  for i in range(NSQ):
   for j in range(NSQ):
    g.add(Text(f"s{IDX[i]}{IDX[j]}  t{IDX[j]}{IDX[i]}", font_size=FS_TAG - 7, color=DIM)
          .move_to([-3.05 + j * 1.55, 0.85 - i * 0.55, 0]))
  g.add(self._brackets(-4.10, 1.90, -0.50, 1.07))
  for i in range(NSQ):
   g.add(self._arr([-4.45, 0.85 - i * 0.55, 0], [-4.05, 0.85 - i * 0.55, 0],
                   ACCENT_A, sw=2, tl=0.09))
  for j in range(NSQ):
   g.add(self._arr([-3.05 + j * 1.55, 1.30, 0], [-3.05 + j * 1.55, 1.12, 0],
                   ACCENT_C, sw=2, tl=0.09))
  return g.add(self._mid(-0.95, "先沿橫列加，得到的是合成一個順序的跡",
                         "add along the rows and you get the trace of one composite",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.34, "先沿直行加，得到的是另一個順序的跡",
                         "add along the columns and you get the trace of the other",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "同一堆乘積，只是加的順序不同——所以兩邊當然相等",
                         "the same products either way, so the two are equal of course",
                         WARN, FS_TAG, w=11.9))

 def _uniqueness(self):
  chain = ((1.00, "μ  ∈  ( Hom V ) *", ACCENT_B, 3.40),
           (0.25, "ν  =  μ ∘ θ   on   ℝ ⁿˣⁿ", ACCENT_A, 4.20),
           (-0.50, "ν ( t )  =  Σ c ᵢⱼ t ᵢⱼ", ACCENT_C, 3.60))
  g = VGroup()
  for y, s, col, w in chain:
   g.add(self._box(-3.20, y, s, col, w=w, h=0.58, size=FS_TAG - 1))
  for y in (1.00, 0.25):
   g.add(self._arr([-3.20, y - 0.31, 0], [-3.20, y - 0.46, 0], DIM, sw=2, tl=0.08))
  arr, pos = self._array(2.60, 0.25, NSQ, NSQ, dx=0.55, dy=0.50, color=DIM, r=0.05)
  g.add(arr)
  for k in range(NSQ):
   g.add(Dot(pos(k, k), radius=0.09, color=WARN))
  return g.add(Text("c", font_size=FS_TAG - 3, color=WARN).move_to([2.60, -0.62, 0]),
               self._mid(-1.05, "把交換的條件代進去，對角線外的係數被逼成零",
                         "feed in the swapping condition and the off-diagonal coefficients vanish",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "對角線上的則被逼成彼此相等，再用單位變換那條定住大小",
                         "the diagonal ones are forced equal, and the identity condition fixes them",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "剩下的正是主對角線的和。細節書上留作習題",
                         "what is left is the diagonal sum; the book leaves the details as exercises",
                         DIM, FS_TAG, w=11.9))

 def _basis_free(self):
  """E23 drew one map with two different matrices under it; the trace is the
  statement that one number under those two matrices agrees."""
  g = VGroup(self._box(0.00, 1.02, "T", ACCENT_A, w=1.20, h=0.54))
  for sx, lab in ((-1, "β"), (1, "β ′")):
   cx = sx * 3.10
   arr, pos = self._array(cx, 0.10, NSQ, NSQ, dx=0.50, dy=0.45, color=DIM, r=0.05)
   g.add(Text(lab, font_size=FS_TAG - 2, color=DIM).move_to([cx, 0.90, 0]),
         self._arr([sx * 0.45, 0.78, 0], [cx - sx * 0.55, 0.62, 0], DIM, sw=2, tl=0.10),
         arr)
   for k in range(NSQ):
    g.add(Dot(pos(k, k), radius=0.085, color=WARN))
   g.add(self._arr([cx, -0.65, 0], [cx, -0.90, 0], WARN, sw=2, tl=0.09))
  return g.add(self._box(0.00, -1.12, "tr ( T )", WARN, w=2.00, h=0.56, size=FS_TAG),
               self._arr([-2.10, -1.12, 0], [-1.05, -1.12, 0], WARN, sw=2, tl=0.10),
               self._arr([2.10, -1.12, 0], [1.05, -1.12, 0], WARN, sw=2, tl=0.10),
               self._mid(-1.62, "兩個矩陣不一樣，主對角線的和卻一樣——這就是跡與基底無關",
                         "the two matrices differ and their diagonal sums do not: that is the trace",
                         ACCENT_A, FS_TAG, w=11.9))

 def _volume(self):
  """Two figures and their images, with the images computed by applying one
  matrix to the source points rather than drawn by eye. Two figures because
  the claim is about every figure, and a computed image because a picture
  that draws its own T inconsistently would be asserting something false."""
  TM = ((1.15, 0.55), (0.30, 1.00))            # the map both figures go through
  ap = lambda p: (TM[0][0] * p[0] + TM[0][1] * p[1], TM[1][0] * p[0] + TM[1][1] * p[1])
  SQ = ((0, 0), (1.00, 0), (1.00, 1.00), (0, 1.00))
  TRI = ((0, 0), (0.80, 0), (0.35, 0.65))
  put = lambda pts, ox, oy: [[ox + q[0], oy + q[1], 0] for q in pts]
  g = VGroup(
   Polygon(*put(SQ, -5.05, -0.10), color=ACCENT_B, stroke_width=2.5,
           fill_color=ACCENT_B, fill_opacity=0.12),
   Polygon(*put(TRI, -3.55, -0.10), color=ACCENT_C, stroke_width=2.5,
           fill_color=ACCENT_C, fill_opacity=0.12),
   Polygon(*put([ap(q) for q in SQ], -0.60, -0.10), color=ACCENT_B, stroke_width=2.5,
           fill_color=ACCENT_B, fill_opacity=0.12),
   Polygon(*put([ap(q) for q in TRI], 2.35, -0.10), color=ACCENT_C, stroke_width=2.5,
           fill_color=ACCENT_C, fill_opacity=0.12),
   self._arr([-2.35, 0.40, 0], [-1.05, 0.40, 0], ACCENT_A, sw=2.5, tl=0.13),
   Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-1.70, 0.69, 0]))
  return g.add(self._mid(-0.95, "同一個倍率對每一個圖形都成立，不只對正方形",
                         "the same factor works for every figure, not only for the square",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.34, "那個倍率就是行列式的絕對值",
                         "that factor is the absolute value of the determinant",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "體積要先選基底才定義得出來，但倍率不依賴那個選擇",
                         "volume needs a basis to define, but the factor does not depend on it",
                         DIM, FS_TAG, w=11.9))

 def _orientation(self):
  """Two frames, one keeping the turn and one reversing it. The second frame
  is chosen so its determinant really is negative and the sign is asserted,
  because a first draft drew a second vector up and to the left -- which
  leaves the determinant positive while the label underneath said otherwise.
  Nothing but computing the number catches that."""
  V1 = (1.05, 0.10)
  RIGHT = (0.30, -0.90)                        # the orientation-reversing partner
  LEFT = (0.35, 0.95)
  det = lambda u, v: u[0] * v[1] - u[1] * v[0]
  assert det(V1, LEFT) > 0 > det(V1, RIGHT), "the frames do not have the signs claimed"
  g = VGroup()
  for cx, second, col, lab in ((-3.40, LEFT, ACCENT_B, "Δ  >  0"),
                               (2.60, RIGHT, WARN, "Δ  <  0")):
   o = (cx, 0.10)
   at = lambda v: [o[0] + v[0], o[1] + v[1], 0]
   g.add(self._arr(at((0, 0)), at(V1), col, sw=2.5, tl=0.12),
         self._arr(at((0, 0)), at(second), col, sw=2.5, tl=0.12),
         Text("1", font_size=FS_TAG - 5, color=col).move_to(at((V1[0] + 0.20, V1[1] - 0.16))),
         Text("2", font_size=FS_TAG - 5, color=col)
         .move_to(at((second[0] + (0.22 if second[1] > 0 else 0.30),
                       second[1] + (0.14 if second[1] > 0 else 0.16)))))
   sweep = [at((V1[0] * 0.66 * (1 - k / 10) + second[0] * 0.66 * (k / 10),
                V1[1] * 0.66 * (1 - k / 10) + second[1] * 0.66 * (k / 10)))
            for k in range(11)]
   g.add(self._curve(sweep, col, sw=2.5),
         self._box(cx, -1.16, lab, col, w=2.00, h=0.52, size=FS_TAG))
  return g.add(Line([-0.40, -1.44, 0], [-0.40, 1.20, 0], color=DIM, stroke_width=1.6),
               self._mid(1.05, "第一個到第二個的轉向沒變",
                         "the turn from the first to the second is unchanged",
                         ACCENT_B, FS_TAG, x=-3.40, w=4.40),
               self._mid(1.05, "轉向被反過來了", "the turn has been reversed",
                         WARN, FS_TAG, x=2.60, w=4.40),
               self._mid(-1.74, "定向本身要留到後面才講清楚，這裡先當成有沒有把左右手對調",
                         "orientation is explained later; for now, whether left and right swapped",
                         DIM, FS_TAG, w=11.9))

 def _props_ab(self):
  """The book's Fig. 2.3 shows a rectangle beside its sheared image. Drawing
  the space as layers that slide instead shows why the volume survives: no
  layer changes length, they only move."""
  g = VGroup(self._box(-4.05, 0.98, "Δ ( S ∘ T )  =  Δ ( S ) Δ ( T )", ACCENT_A,
                       w=4.00, h=0.58, size=FS_TAG - 1),
             Line([-1.70, -1.35, 0], [-1.70, 1.25, 0], color=DIM, stroke_width=1.6))
  base, k = (-4.20, -0.75), 0.52
  for i in range(5):
   y = base[1] + i * 0.30
   sh = i * k * 0.30
   g.add(Line([base[0] + sh, y, 0], [base[0] + 1.30 + sh, y, 0],
              color=ACCENT_B, stroke_width=3))
  g.add(Line([base[0] - 0.45, base[1], 0], [base[0] + 2.30, base[1], 0],
             color=WARN, stroke_width=2.5),
        Text("N", font_size=FS_TAG - 4, color=WARN).move_to([base[0] + 2.55, base[1], 0]))
  o = (0.30, -0.60)
  src = [[o[0], o[1], 0], [o[0] + 1.30, o[1], 0],
         [o[0] + 1.30, o[1] + 1.20, 0], [o[0], o[1] + 1.20, 0]]
  img = [[o[0] + 2.70, o[1], 0], [o[0] + 4.00, o[1], 0],
         [o[0] + 4.00 + 0.62, o[1] + 1.20, 0], [o[0] + 2.70 + 0.62, o[1] + 1.20, 0]]
  g.add(Polygon(*src, color=DIM, stroke_width=2.5),
        Polygon(*img, color=ACCENT_B, stroke_width=2.5,
                fill_color=ACCENT_B, fill_opacity=0.12),
        self._arr([o[0] + 1.55, o[1] + 0.60, 0], [o[0] + 2.45, o[1] + 0.60, 0],
                  ACCENT_A, sw=2.5, tl=0.12))
  return g.add(self._mid(0.98, "面積完全沒有變", "the area does not change at all",
                         ACCENT_B, FS_TAG, x=2.90, w=5.40),
               self._mid(-1.10, "每一層自己不變形，只是滑動",
                         "no layer deforms; they only slide",
                         ACCENT_B, FS_TAG, x=-3.20, w=5.00),
               self._mid(-1.42, "所以剪切完全不改變體積，行列式是一",
                         "so a shearing does not change volume at all, and its determinant is one",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "書上把它描述成「在 N 的不變子空間與商空間上都是恆等」",
                         "the book states it as being the identity on N and on the quotient",
                         DIM, FS_TAG, w=11.9))

 def _props_cde(self):
  g = VGroup()
  rows = ((0.95, "V  =  M ⊕ N    ⇒    Δ  =  Δ ᴹ  ·  Δ ᴺ", ACCENT_B, 5.60),
          (0.15, "d ( V ) = 1    ⇒    Δ ( T )  =  c ᴛ", ACCENT_C, 4.80),
          (-0.65, "d ( V ) = 2  ,   β₁ ↔ β₂    ⇒    Δ  =  − 1", WARN, 5.20))
  for y, s, col, w in rows:
   g.add(self._box(-2.40, y, s, col, w=w, h=0.60, size=FS_TAG - 1))
  o = (2.90, -0.65)
  g.add(self._arr([o[0] - 0.55, o[1] - 0.30, 0], [o[0] + 0.55, o[1] + 0.45, 0],
                  WARN, sw=2.5, tl=0.11),
        self._arr([o[0] + 0.55, o[1] + 0.45, 0], [o[0] - 0.55, o[1] - 0.30, 0],
                  WARN, sw=2.5, tl=0.11))
  return g.add(self._mid(0.95, "拆開就相乘", "split, and they multiply",
                         ACCENT_B, FS_TAG, x=3.30, w=3.20),
               self._mid(0.15, "一維就是那個常數", "in one dimension, the constant",
                         ACCENT_C, FS_TAG, x=3.30, w=3.20),
               self._mid(-1.28, "第五條是純粹的定向性質：互換一對獨立向量，把轉向反過來",
                         "the fifth is pure orientation: swapping two independent vectors reverses it",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "這五條是書上假設的，不是這一節證出來的——存在性在第 7 章",
                         "these five are assumed here, not proved: existence waits for chapter seven",
                         ACCENT_A, FS_TAG, w=11.9))

 def _thm52(self):
  """The two products drawn as the two diagonals of a genuine 2 by 2, which
  is what Theorem 5.2 is about; the rest of the episode's arrays are n by n."""
  cell = lambda i, j: [-3.60 + j * 1.10, 0.75 - i * 0.60, 0]
  g = VGroup()
  for i in range(2):
   for j in range(2):
    g.add(Text(f"t{IDX[i]}{IDX[j]}", font_size=FS_TAG - 4, color=DIM).move_to(cell(i, j)))
  g.add(self._brackets(-4.05, -1.95, 0.05, 0.99),
        Line(cell(0, 0), cell(1, 1), color=ACCENT_B, stroke_width=3),
        Line(cell(1, 0), cell(0, 1), color=WARN, stroke_width=3),
        self._box(1.35, 0.45, "t ₁₁ t ₂₂   −   t ₁₂ t ₂₁", ACCENT_A, w=4.40, h=0.62,
                  size=FS_TAG),
        self._arr([-1.55, 0.45, 0], [-1.00, 0.45, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(-0.30, "往下的那一條相乘", "the product going down",
                         ACCENT_B, FS_TAG, x=1.35, w=4.40),
               self._mid(-0.72, "減去往上的那一條", "minus the one going up",
                         WARN, FS_TAG, x=1.35, w=4.40),
               self._mid(-1.32, "這是一般公式的特例。一般的公式有 n 階乘項，每項是 n 個數的乘積",
                         "a special case of a general formula: n factorial terms of n entries each",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "n 大的時候不實用，但 n 等於三還算好用",
                         "impractical for large n, but fine for n equal to three",
                         ACCENT_A, FS_TAG, w=11.9))

 def _last_three(self):
  g = VGroup(self._box(-3.30, 1.02, "Δ ( T * )  =  Δ ( T )", ACCENT_B, w=3.60, h=0.56,
                       size=FS_TAG - 1),
             self._box(-3.30, 0.32, "Δ ( θ ∘ T ∘ θ ⁻¹ )  =  Δ ( T )", ACCENT_B, w=4.60,
                       h=0.56, size=FS_TAG - 1),
             self._box(-3.30, -0.38, "Δ ( T ) ≠ 0    ⇔    ∃ T ⁻¹", ACCENT_C, w=4.20,
                       h=0.56, size=FS_TAG - 1),
             Line([-0.75, -1.05, 0], [-0.75, 1.25, 0], color=DIM, stroke_width=1.6))
  arr, pos = self._array(2.30, 0.35, NSQ, NSQ, dx=0.55, dy=0.50, color=DIM, r=0.05)
  g.add(arr)
  jx = pos(0, 1)[0]
  for i in range(NSQ):
   g.add(Dot([jx, pos(i, 1)[1], 0], radius=0.085, color=WARN))
  return g.add(Line([jx, pos(0, 1)[1] + 0.22, 0], [jx, pos(NSQ - 1, 1)[1] - 0.22, 0],
                    color=WARN, stroke_width=2.5),
               Text("y", font_size=FS_TAG - 3, color=WARN).move_to([jx, -0.60, 0]),
               self._mid(1.02, "把第 j 直行換成等號右邊那個向量",
                         "replace the jth column by the right hand side",
                         WARN, FS_TAG, x=2.30, w=4.40),
               self._mid(-0.98, "兩個行列式的比，就是解的第 j 個座標",
                         "the ratio of the two determinants is the jth coordinate",
                         ACCENT_A, FS_TAG, x=2.30, w=4.40),
               self._mid(-1.32, "Cramer 法則在 n 大的時候不實用，但理論上重要",
                         "Cramer's rule is impractical for large n and theoretically important",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "第 2 章第 5 節到此結束，下一集講矩陣計算",
                         "that ends section five; next time, matrix computations",
                         ACCENT_C, FS_TAG, w=11.6))

 def stage(self):
  tf, t51, ex = self._two_functions(), self._thm51(), self._existence()
  un, bf, vo = self._uniqueness(), self._basis_free(), self._volume()
  orr, ab, cde = self._orientation(), self._props_ab(), self._props_cde()
  t52, lt = self._thm52(), self._last_three()
  return [([tf], []), ([t51], [tf]), ([ex], [t51]), ([un], [ex]),
          ([bf], [un]), ([vo], [bf]), ([orr], [vo]), ([ab], [orr]),
          ([cde], [ab]), ([t52], [cde]), ([lt], [t52])]


AdvCalcE26ZH, AdvCalcE26EN = make(AdvCalcE26Base, "26", prefix="AdvCalcE")
