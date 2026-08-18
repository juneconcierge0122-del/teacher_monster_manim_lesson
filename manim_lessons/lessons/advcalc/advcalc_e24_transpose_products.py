"""advcalc E24 -- Chapter 2, section 4, middle part (book pp. 90-93): the
transpose, Theorem 4.3 identifying it as the adjoint's matrix, the row and
column spaces, the corollary that their dimensions agree and the resulting
notion of the rank of a matrix, matrix products, Theorem 4.4 making the square
matrices an algebra, and Theorems 4.5 and 4.6.

Two beats do the real work. Beat 2 draws the proof of Theorem 4.3 as two routes
that arrive at one number, because that is what the chain of four equalities in
the book actually is, and a chain of equalities on screen is just the formula
bar again. Beat 7 lays the product out with the left factor beside the answer
and the right factor above it, so the marked row and the marked column really do
cross at the marked entry -- that geometry is the rule. The book's own Fig. 2.1
puts three rectangles in a row instead; this composition is deliberately not it.

Symbols continue E23: beta for a basis of V, gamma for a basis of W, epsilon for
the dual basis of gamma. Theorem 4.3 also needs the dual basis of V* sitting
inside V**, and by the lemma of E21 that is just beta**, so no new letter is
needed there. Lower case t, s, r are matrices and upper case T, S, R the maps
they came from, so t* is the transpose while T* is the adjoint -- which is
exactly the pairing Theorem 4.3 is about. Theorem 4.5 needs a third space, and
its basis takes rho, which the series has not used anywhere.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Ellipse, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# t is m by n, carried over unchanged from E23 so the two episodes show the same
# matrix. s is the left factor of the product, so it is l by m -- its column
# count has to be t's row count, which is the constraint beat 7 is about, and
# writing it as L, M rather than as two literals is what keeps that true.
M, N = 2, 3
L = 3
KROW, JCOL = 1, 2                            # the entry singled out, 0-based

# One tuple per index range. ISUBS and JSUBS index t; KSUBS indexes the rows of
# s and of the product, which is a different range that happens to be the same
# length as JSUBS -- it gets its own name so that changing L cannot silently
# leave a row of subscripts behind.
ISUBS = ("₁", "₂")                           # i = 1 … m : rows of t, and gamma
JSUBS = ("₁", "₂", "₃")                      # j = 1 … n : columns of t, and beta
KSUBS = ("₁", "₂", "₃")                      # k = 1 … l : rows of s and of r
SUP = ("¹", "²", "³")                        # j again, as superscripts

assert len(ISUBS) == M and len(JSUBS) == len(SUP) == N and len(KSUBS) == L


class AdvCalcE24Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 24

 MODE_LABEL = {
  0: {"zh": "轉置：橫列與直行對調", "en": "the transpose: rows and columns exchanged"},
  1: {"zh": "定理 4.3：轉置就是伴隨算子的矩陣",
      "en": "theorem 4.3: the transpose is the adjoint's matrix"},
  2: {"zh": "證明：兩條路走到同一個數", "en": "the proof: two routes to one number"},
  3: {"zh": "橫列空間與直行空間", "en": "the row space and the column space"},
  4: {"zh": "直行空間就是值域", "en": "the column space is the range"},
  5: {"zh": "兩邊被夾成同一個數，這就是秩",
      "en": "both sides squeeze onto one number: the rank"},
  6: {"zh": "乘法是從合成算出來的", "en": "multiplication comes out of composition"},
  7: {"zh": "第 k 橫列與第 j 直行交會的地方",
      "en": "where the kth row and the jth column cross"},
  8: {"zh": "代數律是繼承來的，不是驗證來的",
      "en": "the algebraic laws are inherited, not checked"},
  9: {"zh": "定理 4.4：方陣構成一個代數",
      "en": "theorem 4.4: the square matrices form an algebra"},
  10: {"zh": "定理 4.5 與 4.6：一般空間，與轉置",
       "en": "theorems 4.5 and 4.6: general spaces, and transposes"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _transpose(self):
  """The same entry marked in both arrays, and one row of t marked as the
  matching column of t*. Both marks come from KROW and JCOL, so the picture
  cannot claim one pair of indices while the labels claim another."""
  a, pa = self._array(-4.30, 0.55, M, N, dx=0.55, dy=0.50)
  b, pb = self._array(-0.60, 0.55, N, M, dx=0.55, dy=0.50)
  g = VGroup(a, b,
             Line([pa(0, 0)[0] - 0.22, pa(0, 0)[1], 0],
                  [pa(0, N - 1)[0] + 0.22, pa(0, 0)[1], 0], color=ACCENT_B, stroke_width=3),
             Line([pb(0, 0)[0], pb(0, 0)[1] + 0.20, 0],
                  [pb(0, 0)[0], pb(N - 1, 0)[1] - 0.20, 0], color=ACCENT_B, stroke_width=3),
             Dot(pa(KROW, JCOL), radius=0.09, color=WARN),
             Dot(pb(JCOL, KROW), radius=0.09, color=WARN),
             self._arr([-2.90, 0.55, 0], [-1.55, 0.55, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("( · ) *", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-2.22, 0.84, 0]),
             Text("t", font_size=FS_TAG, color=DIM).move_to([-4.30, -0.28, 0]),
             Text("t *", font_size=FS_TAG, color=DIM).move_to([-0.60, -0.55, 0]),
             Text(f"t {ISUBS[KROW]}{JSUBS[JCOL]}", font_size=FS_TAG - 4, color=WARN)
             .move_to([-3.05, -0.10, 0]),
             Text(f"t * {JSUBS[JCOL]}{ISUBS[KROW]}", font_size=FS_TAG - 4, color=WARN)
             .move_to([0.62, 0.10, 0]))
  return g.add(self._mid(0.75, "第一條橫列變成第一直行", "the first row becomes the first column",
                         ACCENT_B, FS_TAG, x=3.60, w=5.00),
               self._mid(0.15, "兩個指標對調就是全部", "swapping the two indices is the whole story",
                         WARN, FS_TAG, x=3.60, w=5.00),
               self._mid(-1.00, "形狀也跟著轉過來：m 列 n 行的矩陣，轉置後是 n 列 m 行",
                         "the shape turns with it: an m by n matrix transposes to an n by m one",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.40, "看起來只是把陣列翻過來，但下一拍會看到它其實有來歷",
                         "it looks like nothing but flipping the array, but it has a source",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "轉置不是為了方便才定義的",
                         "the transpose was not invented for convenience",
                         ACCENT_A, FS_TAG, w=11.9))

 def _thm43(self):
  """The map and its adjoint on the left, their matrices on the right. The
  arrow reverses and the shape flips, and Theorem 4.3 says those are the same
  fact seen twice."""
  t, _ = self._array(0.60, 0.85, M, N, dx=0.50, dy=0.45)
  ts, _ = self._array(0.60, -0.35, N, M, dx=0.50, dy=0.45)
  g = VGroup(self._box(-3.40, 0.85, "T  :  V  →  W", ACCENT_B, w=3.20, size=FS_TAG),
             Text("↦", font_size=FS_TAG + 2, color=DIM).move_to([-1.15, 0.85, 0]),
             t,
             self._box(-3.40, -0.35, "T *  :  W *  →  V *", ACCENT_A, w=3.20, size=FS_TAG),
             Text("↦", font_size=FS_TAG + 2, color=DIM).move_to([-1.15, -0.35, 0]),
             ts,
             self._arr([-3.40, 0.52, 0], [-3.40, -0.02, 0], ACCENT_C, sw=2.5, tl=0.11),
             Text("( · ) *", font_size=FS_TAG - 4, color=ACCENT_C).move_to([-4.10, 0.25, 0]),
             self._dash([1.75, 0.85, 0], [1.75, -0.35, 0], ACCENT_C, n=8, sw=2),
             Text("( · ) *", font_size=FS_TAG - 4, color=ACCENT_C).move_to([2.35, 0.25, 0]))
  return g.add(self._mid(0.85, "箭頭反過來", "the arrow reverses",
                         ACCENT_B, FS_TAG, x=4.35, w=3.50),
               self._mid(-0.35, "形狀也反過來", "the shape reverses too",
                         ACCENT_A, FS_TAG, x=4.35, w=3.50),
               self._mid(-1.42, "取伴隨算子與取轉置，是同一件事在兩邊的說法",
                         "taking the adjoint and taking the transpose are one act described twice",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "前提是兩邊都用對偶基底來讀，換基底就不成立",
                         "provided both sides are read against the dual bases",
                         DIM, FS_TAG, w=11.9))

 def _proof43(self):
  """The book's chain of four equalities, drawn as what it is: two ways of
  getting at one number. Written out as a chain it would only repeat the
  formula bar underneath it."""
  g = VGroup(self._box(-4.55, 0.85, "βⱼ  ∈  V", ACCENT_B, w=2.00, size=FS_TAG - 1),
             self._arr([-3.50, 0.85, 0], [-2.85, 0.85, 0], DIM, sw=2, tl=0.10),
             Text("T", font_size=FS_TAG - 4, color=DIM).move_to([-3.18, 1.10, 0]),
             self._box(-1.55, 0.85, "T ( βⱼ )  ∈  W", ACCENT_B, w=2.60, size=FS_TAG - 1),
             self._box(-4.55, -0.35, "ε ᵢ  ∈  W *", ACCENT_A, w=2.00, size=FS_TAG - 1),
             self._arr([-3.50, -0.35, 0], [-2.95, -0.35, 0], DIM, sw=2, tl=0.10),
             Text("T *", font_size=FS_TAG - 4, color=DIM).move_to([-3.22, -0.10, 0]),
             self._box(-1.45, -0.35, "T * ( ε ᵢ )  ∈  V *", ACCENT_A, w=2.80, size=FS_TAG - 1),
             self._arr([-0.15, 0.85, 0], [1.80, 0.42, 0], ACCENT_B, sw=2.5, tl=0.12),
             Text("ε ᵢ", font_size=FS_TAG - 3, color=ACCENT_B).move_to([0.72, 0.86, 0]),
             self._arr([-0.02, -0.35, 0], [1.80, 0.10, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("β ⱼ * *", font_size=FS_TAG - 3, color=ACCENT_A).move_to([0.86, -0.42, 0]),
             self._box(2.65, 0.26, f"t {ISUBS[KROW]}{JSUBS[JCOL]}", WARN, w=1.50, h=0.66))
  return g.add(self._mid(0.85, "上一集的引理", "last episode's lemma",
                         ACCENT_B, FS_TAG, x=4.85, w=2.60),
               self._mid(-0.35, "同一條，用在 T* 上", "the same one, applied to the adjoint",
                         ACCENT_A, FS_TAG, x=4.85, w=2.60),
               self._mid(-1.04, "中間那一步是把合成的括號拆開：泛函先走 T 再取值",
                         "the middle step just unwraps the composite: apply T, then evaluate",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.42, "而「對偶基底的對偶基底」就是原來的向量，這是第 21 集那條",
                         "and the dual of the dual basis is the original vector, from episode 21",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "兩條路走到同一個數，指標卻恰好互換——這就是轉置",
                         "two routes, one number, and the indices come out swapped",
                         WARN, FS_TAG, w=11.9))

 def _two_spaces(self):
  """The rows leave to the left into one Cartesian space, the columns to the
  right into another. Drawing them leaving in opposite directions is the
  point: the two spans are not subspaces of the same space."""
  arr, pos = self._array(-0.30, 0.62, M, N, dx=0.60, dy=0.50)
  g = VGroup(arr,
             Ellipse(width=2.60, height=1.30, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-4.20, 0.62, 0]),
             Text("ℝⁿ", font_size=FS_TAG, color=ACCENT_B).move_to([-4.20, 1.20, 0]),
             Ellipse(width=2.60, height=1.30, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.07).move_to([3.60, 0.62, 0]),
             Text("ℝᵐ", font_size=FS_TAG, color=ACCENT_C).move_to([3.60, 1.20, 0]),
             self._arr([-1.60, 0.62, 0], [-2.75, 0.62, 0], ACCENT_B, sw=2.5, tl=0.12),
             self._arr([1.00, 0.62, 0], [2.15, 0.62, 0], ACCENT_C, sw=2.5, tl=0.12))
  for i in range(M):
   g.add(Line([pos(i, 0)[0] - 0.22, pos(i, 0)[1], 0],
              [pos(i, N - 1)[0] + 0.22, pos(i, 0)[1], 0], color=ACCENT_B, stroke_width=3),
         self._arr([-4.85, 0.42 - i * 0.34, 0], [-3.70, 0.62 - i * 0.34, 0],
                   ACCENT_B, sw=2, tl=0.10))
  for j in range(N):
   g.add(Line([pos(0, j)[0], pos(0, j)[1] + 0.20, 0],
              [pos(M - 1, j)[0], pos(M - 1, j)[1] - 0.20, 0], color=ACCENT_C, stroke_width=3),
         self._arr([3.05, 0.30, 0], [3.85 - j * 0.30, 1.02 - j * 0.14, 0],
                   ACCENT_C, sw=2, tl=0.10))
  return g.add(self._mid(0.10, "m 條橫列", "the m rows", ACCENT_B, FS_TAG, x=-2.20, w=1.70),
               self._mid(0.10, "n 個直行", "the n columns", ACCENT_C, FS_TAG, x=1.60, w=1.70),
               self._mid(-0.95, "橫列各自是 n 元組，直行各自是 m 元組，住在不同的空間裡",
                         "rows are n-tuples and columns are m-tuples, living in different spaces",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.38, "所以「維數相同」不是因為它們是同一個空間——它們不是",
                         "so equal dimension is not because they are the same space, they are not",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "它們生成的兩個子空間，維數卻總是一樣",
                         "yet the two subspaces they span always have the same dimension",
                         WARN, FS_TAG, w=11.9))

 def _colspace(self):
  """The columns are the images of the standard basis, so their span is the
  range. The span is drawn behind the arrows rather than asserted beside
  them."""
  o = (2.35, 0.30)
  cols = ((1.15, 0.30), (-0.35, 0.62), (0.70, -0.55))
  at = lambda v: [o[0] + v[0], o[1] + v[1], 0]
  g = VGroup(Ellipse(width=2.40, height=1.40, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-4.20, 0.45, 0]),
             Text("ℝⁿ", font_size=FS_TAG, color=ACCENT_B).move_to([-4.20, 1.18, 0]),
             Ellipse(width=3.60, height=1.90, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.10).move_to([2.35, 0.30, 0]),
             Text("ℝᵐ", font_size=FS_TAG, color=ACCENT_C).move_to([4.45, 1.05, 0]),
             self._arr([-2.90, 0.45, 0], [0.35, 0.45, 0], ACCENT_A, sw=2.5, tl=0.13),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-1.30, 0.74, 0]))
  for j in range(N):
   g.add(Dot([-4.70, 0.80 - j * 0.35, 0], radius=0.06, color=ACCENT_B),
         Text(f"δ {SUP[j]}", font_size=FS_TAG - 5, color=DIM)
         .move_to([-4.15, 0.80 - j * 0.35, 0]),
         self._arr(at((0, 0)), at(cols[j]), WARN, sw=2.5, tl=0.11),
         Text(f"t {SUP[j]}", font_size=FS_TAG - 5, color=WARN)
         .move_to(at((cols[j][0] * 1.22, cols[j][1] * 1.28))))
  return g.add(self._mid(-0.95, "第 j 直行就是第 j 個標準基底向量的像",
                         "the jth column is the image of the jth standard basis vector",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.38, "而基底的像會生成整個值域，所以直行空間就是值域本身",
                         "and the images of a basis span the range, so the column space is the range",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "於是直行空間的維數，就是這個映射的秩",
                         "so the dimension of the column space is the rank of the map",
                         ACCENT_A, FS_TAG, w=11.9))

 def _rank(self):
  """The four equal dimensions as a chain, with the two ends labelled as the
  two claims and the middle step marked as the one that came from E22."""
  chain = ((-4.55, "d ( L ( t ₁ , t ₂ ) )", ACCENT_B, 2.70),
           (-1.55, "d ( R ( T * ) )", ACCENT_A, 2.30),
           (1.45, "d ( R ( T ) )", ACCENT_A, 2.20),
           (4.40, "d ( L ( t ¹ … t ⁿ ) )", ACCENT_C, 2.80))
  g = VGroup()
  for x, s, col, w in chain:
   g.add(self._box(x, 0.72, s, col, w=w, h=0.62, size=FS_TAG - 2))
  for x in (-3.05, -0.05, 2.95):
   g.add(Text("=", font_size=FS_TAG + 1, color=DIM).move_to([x, 0.72, 0]))
  return g.add(self._dash([-1.55, 0.41, 0], [-1.55, 0.05, 0], WARN, n=4, sw=2),
               self._dash([1.45, 0.41, 0], [1.45, 0.05, 0], WARN, n=4, sw=2),
               Line([-1.55, 0.05, 0], [1.45, 0.05, 0], color=WARN, stroke_width=2.5),
               self._mid(-0.22, "這一步是第 22 集那條：伴隨算子與原映射同秩",
                         "this step is from episode 22: the adjoint has the same rank",
                         WARN, FS_TAG, w=11.9),
               self._mid(-0.75, "左端是橫列空間（因為轉置的直行就是原來的橫列）",
                         "the left end is the row space, since the transpose's columns are the rows",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.18, "右端是直行空間，也就是上一拍那個值域",
                         "the right end is the column space, the range from the previous beat",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.58, "兩端被夾成同一個數，這個共同的維數就叫矩陣的秩",
                         "both ends are squeezed onto one number, and that number is the rank",
                         ACCENT_A, FS_TAG, w=11.9))

 def _compose(self):
  """Where the product comes from: substitute one set of scalar equations
  into the other. The tuple lengths are read off M, N and L, so the chain of
  shapes across the picture is forced to be composable."""
  g = VGroup(self._column(-5.00, 0.60, [(f"x{JSUBS[j]}", ACCENT_B) for j in range(N)], dy=0.40),
             Text("x", font_size=FS_TAG - 3, color=ACCENT_B).move_to([-5.00, -0.32, 0]))
  t, _ = self._array(-3.35, 0.60, M, N, dx=0.45, dy=0.42, r=0.05)
  s, _ = self._array(-0.10, 0.60, L, M, dx=0.45, dy=0.42, r=0.05)
  g.add(t, Text("t", font_size=FS_TAG - 3, color=DIM).move_to([-3.35, -0.32, 0]),
        self._arr([-2.45, 0.60, 0], [-1.95, 0.60, 0], DIM, sw=2, tl=0.09),
        self._column(-1.35, 0.60, [(f"y{ISUBS[i]}", ACCENT_C) for i in range(M)], dy=0.40),
        Text("y", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-1.35, -0.32, 0]),
        self._arr([-0.85, 0.60, 0], [-0.60, 0.60, 0], DIM, sw=2, tl=0.09),
        s, Text("s", font_size=FS_TAG - 3, color=DIM).move_to([-0.10, -0.32, 0]),
        self._arr([0.60, 0.60, 0], [1.10, 0.60, 0], DIM, sw=2, tl=0.09),
        self._column(1.70, 0.60, [(f"z{KSUBS[k]}", WARN) for k in range(L)], dy=0.40),
        Text("z", font_size=FS_TAG - 3, color=WARN).move_to([1.70, -0.42, 0]),
        self._dash([-1.35, 1.12, 0], [-0.10, 1.12, 0], ACCENT_C, n=10, sw=2),
        self._arr([-0.10, 1.12, 0], [-0.10, 0.92, 0], ACCENT_C, sw=2, tl=0.09))
  return g.add(self._mid(1.12, "把 y 代進去", "substitute y",
                         ACCENT_C, FS_TAG, x=3.95, w=4.10),
               self._mid(0.30, "剩下的只有 x 與一組新係數", "what is left is x and new coefficients",
                         WARN, FS_TAG, x=3.95, w=4.10),
               self._mid(-0.95, "中間那個 y 只是過路，代進去之後就消失了",
                         "the y in the middle is only in transit, and substituting removes it",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.38, "把兩個和的順序對調，係數就自己聚成一組",
                         "swap the order of the two sums and the coefficients gather themselves",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "那一組係數，就是我們要的乘積矩陣",
                         "that gathered set of coefficients is the product matrix",
                         WARN, FS_TAG, w=11.9))

 def _product(self):
  """Left factor beside the answer, right factor above it, so the marked row
  and the marked column actually cross at the marked entry. The rows of s and
  of r share their y coordinates and the columns of t and of r share their x
  coordinates by construction, which is what makes the crossing true rather
  than merely drawn."""
  t, pt = self._array(1.40, 0.85, M, N, dx=0.55, dy=0.45)
  r, pr = self._array(1.40, -0.55, L, N, dx=0.55, dy=0.45)
  s, ps = self._array(-1.00, -0.55, L, M, dx=0.55, dy=0.45)
  cx, cy = pr(KROW, JCOL)[0], pr(KROW, JCOL)[1]
  g = VGroup(t, r, s,
             Text("t", font_size=FS_TAG, color=DIM).move_to([2.75, 0.85, 0]),
             Text("s", font_size=FS_TAG, color=DIM).move_to([-2.15, -0.55, 0]),
             Text("r", font_size=FS_TAG, color=WARN).move_to([2.75, -0.55, 0]),
             Line([ps(KROW, 0)[0] - 0.22, cy, 0], [ps(KROW, M - 1)[0] + 0.22, cy, 0],
                  color=ACCENT_B, stroke_width=3),
             Line([cx, pt(0, JCOL)[1] + 0.20, 0], [cx, pt(M - 1, JCOL)[1] - 0.20, 0],
                  color=ACCENT_C, stroke_width=3),
             self._dash([ps(KROW, M - 1)[0] + 0.30, cy, 0], [cx - 0.14, cy, 0],
                        ACCENT_B, n=14, sw=1.8),
             self._dash([cx, pt(M - 1, JCOL)[1] - 0.30, 0], [cx, cy + 0.14, 0],
                        ACCENT_C, n=7, sw=1.8),
             Dot([cx, cy, 0], radius=0.10, color=WARN))
  return g.add(self._mid(0.85, "右邊的因子放上面", "the right factor goes above",
                         ACCENT_C, FS_TAG, x=4.60, w=3.00),
               self._mid(-0.55, "左邊的因子放旁邊", "the left factor goes beside",
                         ACCENT_B, FS_TAG, x=4.60, w=3.00),
               self._mid(-1.40, "那一格就是第 k 橫列與第 j 直行的純量積，交會的地方",
                         "that entry is the scalar product of the kth row and the jth column",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "所以形狀必須對得上：左邊的行數要等於右邊的列數",
                         "so the shapes must agree: the left factor's columns are the right's rows",
                         DIM, FS_TAG, w=11.9))

 def _inherited(self):
  """Associativity is not verified on the right; it is carried across."""
  g = VGroup()
  xs = (-5.10, -3.90, -2.70, -1.50)
  for x in xs:
   g.add(Dot([x, 0.95, 0], radius=0.07, color=ACCENT_B))
  for a, b, lab in ((xs[0], xs[1], "T"), (xs[1], xs[2], "S"), (xs[2], xs[3], "R")):
   g.add(self._arr([a + 0.14, 0.95, 0], [b - 0.14, 0.95, 0], DIM, sw=2, tl=0.09),
         Text(lab, font_size=FS_TAG - 4, color=DIM).move_to([(a + b) / 2, 1.18, 0]))
  for y, lo, hi, col in ((0.72, xs[0], xs[2], ACCENT_C), (0.36, xs[1], xs[3], ACCENT_A)):
   g.add(Line([lo, y, 0], [hi, y, 0], color=col, stroke_width=2.5),
         Line([lo, y, 0], [lo, y + 0.12, 0], color=col, stroke_width=2.5),
         Line([hi, y, 0], [hi, y + 0.12, 0], color=col, stroke_width=2.5))
  return g.add(Line([-0.55, -0.75, 0], [-0.55, 1.20, 0], color=DIM, stroke_width=1.6),
               self._sym(0.90, "( R ∘ S ) ∘ T   =   R ∘ ( S ∘ T )", ACCENT_B, FS_TAG, x=3.00, w=5.60),
               self._arr([3.00, 0.55, 0], [3.00, 0.10, 0], WARN, sw=2.5, tl=0.12),
               self._mid(0.33, "同構保持乘法", "the isomorphism preserves products",
                         WARN, FS_TAG, x=4.90, w=2.60),
               self._box(3.00, -0.28, "( r s ) t   =   r ( s t )", WARN, w=4.20, h=0.66,
                         size=FS_TAG),
               self._mid(-1.05, "矩陣乘法不是先定義好再回頭驗證性質",
                         "matrix multiplication is not defined first and checked afterwards",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.40, "它根本就定義成「合成的那個矩陣」",
                         "it is defined to be the matrix of the composite",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "所以結合律不必計算，它就是合成的結合律",
                         "so associativity needs no computation: it is composition's own",
                         WARN, FS_TAG, w=11.9))

 def _algebra(self):
  """The identity matrix is built from a Kronecker test rather than typed
  out, so the ones land on the diagonal by definition."""
  g = VGroup(self._box(-4.60, 0.95, "M ₙ", ACCENT_B, w=1.40),
             Text("≅", font_size=FS_TAG + 1, color=DIM).move_to([-3.45, 0.95, 0]),
             self._box(-1.95, 0.95, "Hom ( ℝⁿ )", ACCENT_C, w=2.60, size=FS_TAG))
  y0 = 0.62 + 0.45
  for i in range(N):
   for j in range(N):
    hot = i == j
    g.add(Text("1" if hot else "0", font_size=FS_TAG - 4, color=WARN if hot else DIM)
          .move_to([2.05 + j * 0.55, y0 - i * 0.45, 0]))
  return g.add(self._brackets(1.73, 3.47, y0 - (N - 1) * 0.45 - 0.20, y0 + 0.20),
               Text("e", font_size=FS_TAG, color=WARN).move_to([2.60, -0.32, 0]),
               self._box(-2.60, -0.35, "∃ t ⁻¹    ⇔    d ( R ( T ) )  =  n", ACCENT_A,
                         w=5.20, h=0.66, size=FS_TAG),
               self._mid(-1.05, "加法、純量乘法與乘法都被保持，所以那是代數的同構",
                         "sums, scalar multiples and products are all preserved: an algebra isomorphism",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.40, "單位映射對應的矩陣，主對角線上是一、其他地方是零",
                         "the identity map corresponds to ones down the diagonal and zeros elsewhere",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "而方陣可逆，若且唯若它的秩是滿的",
                         "and a square matrix is invertible exactly when its rank is full",
                         ACCENT_A, FS_TAG, w=11.9))

 def _thm4546(self):
  g = VGroup()
  spots = ((-5.00, "U", "β"), (-3.10, "V", "γ"), (-1.20, "W", "ρ"))
  for x, s, b in spots:
   g.add(self._box(x, 0.95, s, ACCENT_B, w=1.10, h=0.56),
         Text(b, font_size=FS_TAG - 3, color=ACCENT_C).move_to([x, 0.48, 0]))
  for a, b, lab in ((-5.00, -3.10, "T"), (-3.10, -1.20, "S")):
   g.add(self._arr([a + 0.60, 0.95, 0], [b - 0.60, 0.95, 0], ACCENT_A, sw=2.5, tl=0.12),
         Text(lab, font_size=FS_TAG - 3, color=ACCENT_A).move_to([(a + b) / 2, 1.22, 0]))
  g.add(self._arr([-5.00, 0.12, 0], [-1.20, 0.12, 0], DIM, sw=2, tl=0.11),
        Line([-5.00, 0.12, 0], [-5.00, 0.30, 0], color=DIM, stroke_width=1.6),
        Text("S ∘ T", font_size=FS_TAG - 3, color=DIM).move_to([-3.10, -0.16, 0]))
  return g.add(Line([-0.25, -0.55, 0], [-0.25, 1.25, 0], color=DIM, stroke_width=1.6),
               self._box(3.00, 0.92, "S ∘ T    ↦    s · t", ACCENT_A, w=4.00, h=0.66,
                         size=FS_TAG),
               self._box(3.00, 0.02, "( s t ) *   =   t * s *", WARN, w=4.00, h=0.66,
                         size=FS_TAG),
               self._mid(-0.62, "順序又反了一次", "the order reverses once again",
                         WARN, FS_TAG, x=3.00, w=3.80),
               self._mid(-1.10, "選定三組基底之後，合成的矩陣還是兩個矩陣的乘積",
                         "with three bases chosen, a composite's matrix is still the product",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.42, "而轉置反轉順序，跟伴隨算子那條是同一件事——第 22 集就看過",
                         "and transposing reverses the order, the same fact as for adjoints in E22",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集講行向量、換基底與 Hom 的標準基底",
                         "next time: column vectors, change of basis, and a basis for Hom",
                         ACCENT_C, FS_TAG, w=11.6))

 def stage(self):
  tr, t43, pf = self._transpose(), self._thm43(), self._proof43()
  ts, cs, rk = self._two_spaces(), self._colspace(), self._rank()
  cp, pd, ih = self._compose(), self._product(), self._inherited()
  al, gn = self._algebra(), self._thm4546()
  return [([tr], []), ([t43], [tr]), ([pf], [t43]), ([ts], [pf]),
          ([cs], [ts]), ([rk], [cs]), ([cp], [rk]), ([pd], [cp]),
          ([ih], [pd]), ([al], [ih]), ([gn], [al])]


AdvCalcE24ZH, AdvCalcE24EN = make(AdvCalcE24Base, "24", prefix="AdvCalcE")
