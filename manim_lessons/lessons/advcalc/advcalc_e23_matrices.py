"""advcalc E23 -- Chapter 2, section 4, first part (book pp. 88-90): a matrix as
a function on an index set, the space of all m by n matrices, Theorem 4.1 in the
Cartesian case, the row reading, Theorem 4.2 for general V and W, its corollary,
the warning that a matrix is always with respect to chosen bases, and Lemma 4.1.
The section runs to book p. 96; pp. 96-98 are exercises and are not covered.

The section's real content is a change of viewpoint, not a computation, so the
pictures are built to hold two readings of the same array side by side: beat 0
puts the array drawing next to the function drawing, beat 4 puts all three faces
of a matrix in one triangle, and beat 9 draws one single map twice and lets the
two matrices under it disagree. Beat 3 is the one genuinely geometric picture --
the columns as vectors, scaled and added -- because "linear combination map" is
otherwise just a phrase.

Symbols continue E21 and E22: beta for a basis of V, epsilon for a dual basis,
lambda for a functional. The book writes alpha for the basis of V, beta for the
basis of W and mu for the dual basis in W*, but beta has meant "basis vector of
V" for two episodes running, so the new object -- a basis of W -- takes the new
letter gamma rather than stealing one. T prime is the map on Cartesian spaces
that the book writes as T with a bar: a combining macron on a capital renders
faintly, and the book itself uses primes for this role on p. 94.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# One worked example for the whole episode: m = 2, n = 3. It has to be a single
# example because three beats put an array next to a picture of W, and W can only
# be drawn as a plane -- a first draft used a 3 by 4 array beside a 2-dimensional
# W, so beat 10 showed a functional epsilon-k indexing two basis vectors of W
# while the array it wrote into had three rows. Neither bounds.py nor a reading
# of the formula bar can see that; only the two halves of one frame side by side.
M, N = 2, 3
KROW = 1                                     # the row singled out, 0-based
JCOL = 2                                     # the column singled out, 0-based

# One tuple per index range, shared by everything that spells that range out.
# ISUBS runs over the rows of the array and, because they are the same range,
# over the basis of W; JSUBS runs over the columns and the basis of V. E18, E19
# and E21 each shipped a row whose subscripts disagreed with the row above it
# because each row wrote its own index string by hand; bounds.py passes either
# way and so does reading the formula bar alone.
ISUBS = ("₁", "₂")                           # i = 1 … m : rows, and gamma
JSUBS = ("₁", "₂", "₃")                      # j = 1 … n : columns, and beta
SUP = ("¹", "²", "³")                        # the same range, as superscripts

assert len(ISUBS) == M and len(JSUBS) == len(SUP) == N


class AdvCalcE23Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 23

 MODE_LABEL = {
  0: {"zh": "矩陣其實是一個函數", "en": "a matrix is really a function"},
  1: {"zh": "所有矩陣自己構成一個向量空間", "en": "the matrices themselves form a vector space"},
  2: {"zh": "定理 4.1：直行就是骨架", "en": "theorem 4.1: the columns are the skeleton"},
  3: {"zh": "那個映射就是線性組合映射", "en": "the map is the linear combination map"},
  4: {"zh": "矩陣與映射之間是自然同構", "en": "matrices and maps: a natural isomorphism"},
  5: {"zh": "橫列的讀法：m 個線性泛函", "en": "reading the rows: m linear functionals"},
  6: {"zh": "定理 4.2：選定基底之後", "en": "theorem 4.2: once bases are chosen"},
  7: {"zh": "證明：兩個同構接起來", "en": "the proof: two isomorphisms composed"},
  8: {"zh": "推論：座標把方程算出來", "en": "the corollary: coordinates give the equations"},
  9: {"zh": "矩陣永遠是相對於基底的", "en": "a matrix is always with respect to bases"},
  10: {"zh": "怎麼把矩陣元素讀出來", "en": "how to read an entry off the map"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _is_a_function(self):
  """The array drawing and the function drawing, side by side. The point of
  the beat is that they are the same object, so both have to be on screen."""
  arr, _ = self._array(-4.55, 0.55, M, N, dx=0.50, dy=0.40, r=0.05)
  g = VGroup(arr, Text("=", font_size=FS_TAG + 2, color=DIM).move_to([-2.95, 0.55, 0]))
  cells, cpos = self._array(-1.55, 0.55, M, N, dx=0.50, dy=0.40, color=DIM, r=0.04)
  g.add(cells, Dot(cpos(KROW, JCOL), radius=0.075, color=WARN),
        Text("( i , j )", font_size=FS_TAG - 4, color=WARN).move_to([-1.55, -0.28, 0]),
        self._arr([cpos(KROW, JCOL)[0] + 0.90, cpos(KROW, JCOL)[1], 0],
                  [1.70, cpos(KROW, JCOL)[1], 0], ACCENT_A, sw=2, tl=0.10),
        Text("t", font_size=FS_TAG, color=ACCENT_A).move_to([0.80, 0.60, 0]),
        Line([2.15, -0.10, 0], [2.15, 1.20, 0], color=DIM, stroke_width=2.5),
        Text("ℝ", font_size=FS_TAG, color=DIM).move_to([2.52, 1.08, 0]),
        Dot([2.15, cpos(KROW, JCOL)[1], 0], radius=0.07, color=WARN),
        Text("tᵢⱼ", font_size=FS_TAG, color=WARN).move_to([2.72, 0.15, 0]))
  return g.add(self._mid(-0.80, "左邊是畫法，右邊才是矩陣本身",
                         "the left is the drawing, the right is the matrix itself",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.32, "指標集是「列指標配行指標」，就像數列的指標集是自然數",
                         "the index set is row-and-column pairs, as a sequence is indexed by integers",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "第一個指標數橫列，第二個數直行——順序記反了整節都會錯",
                         "the first index counts rows, the second counts columns",
                         ACCENT_C, FS_TAG, w=11.9))

 def _matrix_space(self):
  """Addition place by place, then the same numbers flattened into one index."""
  g = VGroup()
  marks = []
  for cx in (-5.20, -3.10, -1.00):
   a, p = self._array(cx, 0.72, M, N, dx=0.45, dy=0.40, r=0.05)
   g.add(a); marks.append(p(0, 1))
  g.add(Text("+", font_size=FS_TAG + 2, color=DIM).move_to([-4.15, 0.72, 0]),
        Text("=", font_size=FS_TAG + 2, color=DIM).move_to([-2.05, 0.72, 0]))
  for x, y, _ in marks:
   g.add(Dot([x, y, 0], radius=0.085, color=ACCENT_C),
         Line([x, y + 0.20, 0], [x, 1.18, 0], color=ACCENT_C, stroke_width=1.4))
  g.add(self._dash([marks[0][0], 1.18, 0], [marks[2][0], 1.18, 0], ACCENT_C, n=24, sw=1.8),
        self._arr([-0.10, 0.72, 0], [1.05, 0.72, 0], ACCENT_A, sw=2, tl=0.10))
  flat, _ = self._array(2.75, 0.72, 1, M * N, dx=0.45, dy=0.40, r=0.05)
  return g.add(flat,
               self._mid(0.05, "兩個指標攤平成一個", "two indices flattened into one",
                         ACCENT_A, FS_TAG, x=2.75, w=3.10),
               self._mid(-0.85, "加法只在對應的格子之間發生，那就是函數的加法",
                         "addition happens only between matching cells, which is addition of functions",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.32, "所以矩陣的集合不只是一堆陣列，它自己是一個向量空間",
                         "so the set of matrices is not just a pile of arrays, it is a vector space",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.78, "維數是列數乘行數，跟同樣多座標的座標空間沒有分別",
                         "its dimension is rows times columns, no different from a Cartesian space",
                         DIM, FS_TAG, w=11.9))

 def _theorem41(self):
  """The standard basis vector on the left, the column it is sent to on the
  right. Every index in the picture comes from JCOL, so the marked slot of
  delta, the boxed column and the subscripts of the tuple cannot disagree --
  the first draft labelled the tuple t-with-superscript-3 while its entries
  still read t-i-j, which says j = 3 and j at once."""
  dj = self._column(-5.05, 0.40, [("1", WARN) if k == JCOL else "0" for k in range(N)])
  arr, pos = self._array(-2.30, 0.40, M, N, dx=0.60, dy=0.50)
  g = VGroup(dj, Text(f"δ {SUP[JCOL]}", font_size=FS_TAG, color=WARN)
             .move_to([-5.05, -0.62, 0]),
             self._arr([-4.55, 0.40, 0], [-3.65, 0.40, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-4.10, 0.72, 0]),
             arr,
             Rectangle(width=0.50, height=1.20, color=ACCENT_C, stroke_width=2.5)
             .move_to([pos(0, JCOL)[0], 0.40, 0]),
             self._arr([-1.20, 0.40, 0], [-0.20, 0.40, 0], ACCENT_C, sw=2.5, tl=0.12),
             self._column(0.50, 0.40,
                          [(f"t{ISUBS[i]}{JSUBS[JCOL]}", ACCENT_C) for i in range(M)]),
             Text(f"t {SUP[JCOL]}", font_size=FS_TAG, color=ACCENT_C)
             .move_to([0.50, -0.55, 0]))
  return g.add(self._mid(0.40, "第 j 個標準基底向量", "the jth standard basis vector",
                         WARN, FS_TAG, x=3.55, w=4.60),
               self._mid(-0.20, "被送到第 j 直行", "goes to the jth column",
                         ACCENT_C, FS_TAG, x=3.55, w=4.60),
               self._mid(-1.02, "骨架決定整個線性映射，這是第 1 章就有的事",
                         "a skeleton determines the whole linear map, as chapter one showed",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.40, "所以矩陣裡的 n 個直行，恰好就是一個線性映射的骨架",
                         "so the n columns of a matrix are exactly the skeleton of a linear map",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.78, "而且這樣的映射只有一個，不多也不少",
                         "and there is exactly one such map, no more and no fewer",
                         ACCENT_A, FS_TAG, w=11.9))

 def _lincomb(self):
  """The columns as actual vectors, scaled and added. The coefficients are
  applied to the drawn column vectors rather than chosen separately, so the
  arrow head of the sum really is at the corner of the parallelogram."""
  o = (-3.60, 0.00)
  c1, c2, x1, x2 = (1.05, 0.25), (0.20, 0.62), 1.4, 1.0
  at = lambda v: [o[0] + v[0], o[1] + v[1], 0]
  s1, s2 = (c1[0] * x1, c1[1] * x1), (c2[0] * x2, c2[1] * x2)
  tot = (s1[0] + s2[0], s1[1] + s2[1])
  g = VGroup(self._axes(np.array([o[0], o[1], 0]), "", "", w=1.85, h=0.85),
             self._arr(at((0, 0)), at(c1), ACCENT_B, sw=3, tl=0.13),
             self._arr(at((0, 0)), at(c2), ACCENT_C, sw=3, tl=0.13),
             Text(f"t {SUP[0]}", font_size=FS_TAG - 2, color=ACCENT_B).move_to(at((1.25, 0.42))),
             Text(f"t {SUP[1]}", font_size=FS_TAG - 2, color=ACCENT_C).move_to(at((-0.45, 0.72))),
             self._dash(at(s1), at(tot), ACCENT_C, n=9, sw=1.8),
             self._dash(at(s2), at(tot), ACCENT_B, n=9, sw=1.8),
             self._arr(at((0, 0)), at(tot), WARN, sw=3.5, tl=0.15),
             Text("y", font_size=FS_TAG, color=WARN).move_to(at((tot[0] + 0.30, tot[1] + 0.22))))
  arr, pos = self._array(1.45, 0.55, M, N, dx=0.50, dy=0.44)
  g.add(arr, Line([pos(KROW, 0)[0] - 0.22, pos(KROW, 0)[1], 0],
                  [pos(KROW, N - 1)[0] + 0.22, pos(KROW, N - 1)[1], 0],
                  color=ACCENT_B, stroke_width=3),
        self._column(2.95, 0.55, [(f"x{JSUBS[j]}", ACCENT_C) for j in range(N)]),
        Text("=", font_size=FS_TAG + 1, color=DIM).move_to([3.65, 0.55, 0]),
        self._column(4.35, 0.55,
                     [(f"y{ISUBS[i]}", WARN if i == KROW else DIM) for i in range(M)]))
  return g.add(self._mid(-0.92, "把第 j 個座標乘上第 j 直行，再全部加起來",
                         "scale the jth column by the jth coordinate, then add them all up",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.34, "逐個座標寫開，就是熟悉的那組純量方程",
                         "written out coordinate by coordinate, these are the familiar scalar equations",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "第 i 個輸出，由第 i 橫列跟輸入配出來",
                         "the ith output comes from the ith row paired against the input",
                         WARN, FS_TAG, w=11.9))

 def _three_faces(self):
  """One object, three faces. E17 made the same point about matrices in the
  abstract; here the three faces are the ones this section actually uses."""
  a = self._box(0.00, 0.98, "{ tᵢⱼ }", ACCENT_A, w=2.20)
  b = self._box(-3.40, -0.10, "⟨ t ¹ , … , t ⁿ ⟩", ACCENT_B, w=2.90, size=FS_TAG)
  c = self._box(3.40, -0.10, "T ∈ Hom ( ℝⁿ , ℝᵐ )", ACCENT_C, w=3.40, size=FS_TAG)
  g = VGroup(a, b, c)
  for p, q, mx, my in ((-1.10, -3.40, -2.45, 0.58), (1.10, 3.40, 2.45, 0.58)):
   g.add(Line([p, 0.71, 0], [q, 0.24, 0], color=DIM, stroke_width=2),
         Text("≅", font_size=FS_TAG, color=DIM).move_to([mx, my, 0]))
  g.add(Line([-1.92, -0.10, 0], [1.68, -0.10, 0], color=DIM, stroke_width=2),
        Text("≅", font_size=FS_TAG, color=DIM).move_to([-0.12, 0.14, 0]))
  return g.add(self._mid(-0.82, "三個面向之間的對應都不必挑，所以是自然的",
                         "none of these correspondences has to be chosen, which is what natural means",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.30, "把矩陣讀成一串行向量，用的正是其中一個——第 0 章第 10 節的對偶",
                         "reading a matrix as a list of columns is one of them: the duality of chapter zero",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.78, "書上把它當成等號直接用，不再每次交代",
                         "the book treats it as an identity and stops mentioning it",
                         DIM, FS_TAG, w=11.9))

 def _rows(self):
  """Each row leaves as a functional; the m values arriving stack into the
  output tuple. Both the arrow labels and the output cells index themselves
  out of ISUBS, so the two columns of subscripts cannot disagree."""
  arr, pos = self._array(-3.80, 0.30, M, N, dx=0.60, dy=0.55)
  g = VGroup(arr)
  for i in range(M):
   y = pos(i, 0)[1]
   g.add(Line([pos(i, 0)[0] - 0.24, y, 0], [pos(i, N - 1)[0] + 0.24, y, 0],
              color=ACCENT_B, stroke_width=3),
         self._arr([-1.65, y, 0], [0.05, y, 0], DIM, sw=2, tl=0.10),
         Text(f"f{ISUBS[i]}", font_size=FS_TAG - 3, color=ACCENT_B)
         .move_to([-0.80, y + 0.26, 0]))
  return g.add(self._column(0.80, 0.30, [(f"y{ISUBS[i]}", WARN) for i in range(M)], dy=0.55),
               Text("y", font_size=FS_TAG, color=WARN).move_to([0.80, -0.78, 0]),
               self._mid(0.62, "每一條橫列都是 ℝⁿ 上的一個泛函",
                         "each row is a functional on the domain",
                         ACCENT_B, FS_TAG, x=3.95, w=4.20),
               self._mid(-0.10, "m 條橫列湊成一個 m 元組的值",
                         "the m rows together give one m-tuple of values",
                         WARN, FS_TAG, x=3.95, w=4.20),
               self._mid(-1.04, "係數乘座標再加起來，是座標空間上最一般的線性泛函",
                         "coefficients times coordinates summed is the most general functional here",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.41, "所以一個多值的映射，等價於 m 個各自單值的泛函",
                         "so one vector valued map is equivalent to m separate scalar functionals",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "直行看到的是骨架，橫列看到的是方程——同一個陣列",
                         "the columns show the skeleton, the rows show the equations, one array",
                         ACCENT_C, FS_TAG, w=11.9))

 def _theorem42(self):
  """The jth column is drawn as the coefficient list of the image, with the
  image built out of the gamma arrows rather than placed by eye, and every
  index taken from JCOL so the highlighted basis vector, the image label and
  the tuple all name the same column."""
  g = VGroup(Ellipse(width=2.30, height=1.30, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-4.10, 0.45, 0]),
             Text("V", font_size=FS_TAG + 2, color=ACCENT_B).move_to([-4.10, 1.16, 0]))
  for k, y in enumerate((0.80, 0.45, 0.10)):
   hot = k == JCOL
   g.add(Dot([-4.60, y, 0], radius=0.06, color=WARN if hot else ACCENT_B),
         Text(f"β{JSUBS[k]}", font_size=FS_TAG - 4, color=WARN if hot else DIM)
         .move_to([-4.05, y, 0]))
  o, gv = (1.35, -0.05), ((1.05, 0.15), (0.25, 0.75))
  co = (1.1, 1.0)
  at = lambda v: [o[0] + v[0], o[1] + v[1], 0]
  img = (gv[0][0] * co[0] + gv[1][0] * co[1], gv[0][1] * co[0] + gv[1][1] * co[1])
  g.add(self._arr([-2.85, 0.45, 0], [-0.35, 0.45, 0], ACCENT_A, sw=2.5, tl=0.13),
        Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-1.60, 0.74, 0]),
        Ellipse(width=3.00, height=1.60, color=ACCENT_C, stroke_width=2.5,
                fill_color=ACCENT_C, fill_opacity=0.06).move_to([2.40, 0.35, 0]),
        Text("W", font_size=FS_TAG + 2, color=ACCENT_C).move_to([0.42, 1.05, 0]))
  for k, v in enumerate(gv):
   g.add(self._arr(at((0, 0)), at(v), ACCENT_C, sw=2.5, tl=0.11),
         Text(f"γ{ISUBS[k]}", font_size=FS_TAG - 4, color=ACCENT_C)
         .move_to(at((v[0] + 0.18, v[1] - 0.16))))
  g.add(self._dash(at((gv[0][0] * co[0], gv[0][1] * co[0])), at(img), DIM, n=7, sw=1.6),
        self._dash(at((gv[1][0] * co[1], gv[1][1] * co[1])), at(img), DIM, n=7, sw=1.6),
        self._arr(at((0, 0)), at(img), WARN, sw=3, tl=0.13),
        Text(f"T ( β{JSUBS[JCOL]} )", font_size=FS_TAG - 3, color=WARN)
        .move_to(at((img[0] + 0.10, img[1] + 0.28))),
        self._dash(at(img), [4.35, 0.45, 0], DIM, n=8, sw=1.6),
        self._column(4.85, 0.45,
                     [(f"t{ISUBS[i]}{JSUBS[JCOL]}", WARN) for i in range(M)]),
        Text(f"t {SUP[JCOL]}", font_size=FS_TAG - 2, color=WARN).move_to([4.85, -0.35, 0]))
  return g.add(self._mid(-0.92, "先挑好 V 的一組有序基底，跟 W 的一組有序基底",
                         "first fix an ordered basis for V and one for W",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.34, "第 j 個基底向量的像，用 W 的基底展開，係數就是第 j 直行",
                         "expand the image of the jth basis vector in W's basis: the jth column",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "這個對應在矩陣空間與 Hom(V, W) 之間，又是一個同構",
                         "this correspondence is again an isomorphism onto Hom of V and W",
                         ACCENT_A, FS_TAG, w=11.9))

 def _proof(self):
  """Left: the matrix's Cartesian map carried over by the two basis
  isomorphisms. Right: the same construction split into its two steps."""
  g = VGroup(self._box(-4.70, 0.95, "ℝⁿ", DIM, w=1.20),
             self._box(-2.15, 0.95, "ℝᵐ", DIM, w=1.20),
             self._box(-4.70, -0.35, "V", ACCENT_B, w=1.20),
             self._box(-2.15, -0.35, "W", ACCENT_C, w=1.20),
             self._arr([-4.05, 0.95, 0], [-2.80, 0.95, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T ′", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-3.42, 1.22, 0]),
             self._arr([-4.05, -0.35, 0], [-2.80, -0.35, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-3.42, -0.66, 0]),
             self._arr([-4.70, 0.62, 0], [-4.70, -0.02, 0], ACCENT_B, sw=2.5, tl=0.11),
             Text("φ", font_size=FS_TAG - 2, color=ACCENT_B).move_to([-5.12, 0.30, 0]),
             self._arr([-2.15, 0.62, 0], [-2.15, -0.02, 0], ACCENT_C, sw=2.5, tl=0.11),
             Text("ψ", font_size=FS_TAG - 2, color=ACCENT_C).move_to([-1.72, 0.30, 0]),
             Line([-0.75, -0.95, 0], [-0.75, 1.25, 0], color=DIM, stroke_width=1.6))
  chain = ((1.05, "{ tᵢⱼ }", ACCENT_A, 2.00), (0.20, "⟨ τ₁ , … , τₙ ⟩", ACCENT_C, 2.90),
           (-0.65, "T ∈ Hom ( V , W )", ACCENT_B, 3.40))
  for y, s, col, w in chain:
   g.add(self._box(2.60, y, s, col, w=w, h=0.50, size=FS_TAG - 1))
  for y0 in (1.05, 0.20):
   g.add(self._arr([2.60, y0 - 0.27, 0], [2.60, y0 - 0.58, 0], DIM, sw=2, tl=0.09))
  return g.add(self._mid(-1.06, "兩個基底同構把座標空間上的映射搬到 V 與 W 上",
                         "the two basis isomorphisms carry the Cartesian map over to V and W",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.42, "同構合成同構還是同構，證明就結束了",
                         "isomorphisms composed with isomorphisms are isomorphisms, and that is the proof",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "分兩步看也行：每一直行先給 W 裡一個向量，這些向量再給整個映射",
                         "or in two steps: each column gives a vector in W, and those give the map",
                         ACCENT_C, FS_TAG, w=11.9))

 def _corollary(self):
  """The abstract lane on top, the computable lane underneath, joined by the
  coordinate isomorphisms."""
  g = VGroup(Ellipse(width=1.90, height=0.80, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.07).move_to([-3.80, 0.90, 0]),
             Text("V", font_size=FS_TAG, color=ACCENT_B).move_to([-5.15, 0.90, 0]),
             Dot([-3.80, 0.90, 0], radius=0.07, color=WARN),
             Text("ξ", font_size=FS_TAG - 2, color=WARN).move_to([-3.42, 1.12, 0]),
             self._arr([-2.80, 0.90, 0], [-1.30, 0.90, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-2.05, 1.16, 0]),
             Ellipse(width=1.90, height=0.80, color=ACCENT_C, stroke_width=2.5,
                     fill_color=ACCENT_C, fill_opacity=0.07).move_to([-0.30, 0.90, 0]),
             Text("W", font_size=FS_TAG, color=ACCENT_C).move_to([1.05, 0.90, 0]),
             Dot([-0.30, 0.90, 0], radius=0.07, color=WARN),
             Text("η", font_size=FS_TAG - 2, color=WARN).move_to([0.08, 1.12, 0]),
             self._arr([-3.80, 0.44, 0], [-3.80, 0.22, 0], DIM, sw=2, tl=0.09),
             Text("φ ⁻¹", font_size=FS_TAG - 4, color=DIM).move_to([-4.42, 0.33, 0]),
             self._arr([-0.30, 0.44, 0], [-0.30, 0.22, 0], DIM, sw=2, tl=0.09),
             Text("ψ ⁻¹", font_size=FS_TAG - 4, color=DIM).move_to([0.34, 0.33, 0]))
  arr, pos = self._array(-2.05, -0.42, M, N, dx=0.45, dy=0.40, r=0.05)
  return g.add(self._column(-3.80, -0.42,
                            [(f"x{JSUBS[j]}", WARN) for j in range(N)], dy=0.36),
               arr, Line([pos(KROW, 0)[0] - 0.20, pos(KROW, 0)[1], 0],
                         [pos(KROW, N - 1)[0] + 0.20, pos(KROW, N - 1)[1], 0],
                         color=ACCENT_A, stroke_width=3),
               self._column(-0.30, -0.42,
                            [(f"y{ISUBS[i]}", WARN if i == KROW else DIM)
                             for i in range(M)], dy=0.36),
               Text("t", font_size=FS_TAG - 2, color=DIM).move_to([-1.05, -0.42, 0]),
               self._mid(0.90, "抽象的那一層", "the abstract layer",
                         ACCENT_A, FS_TAG, x=3.60, w=4.90),
               self._mid(-0.30, "選好基底之後可以算的那一層", "the layer you can compute in",
                         WARN, FS_TAG, x=3.60, w=4.90),
               self._mid(-1.30, "輸出等於映射作用在輸入上，充要條件就是那組純量方程成立",
                         "the output is the map applied to the input exactly when the equations hold",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "所以抽象的映射被那組方程完全取代，一點資訊也沒少",
                         "so the abstract map is replaced by the equations, losing nothing",
                         DIM, FS_TAG, w=11.9))

 def _basis_dependent(self):
  """One map, drawn once; two basis choices, drawn underneath it; two
  different matrices. The dot patterns differ on purpose -- if both arrays
  looked the same the picture would be arguing against the narration."""
  g = VGroup(self._box(-1.20, 1.00, "V", ACCENT_B, w=1.10, h=0.56),
             self._box(1.20, 1.00, "W", ACCENT_C, w=1.10, h=0.56),
             self._arr([-0.65, 1.00, 0], [0.65, 1.00, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([0.00, 0.70, 0]))
  for sx, lab in ((-1, "( β , γ )"), (1, "( β ′ , γ ′ )")):
   cx = sx * 3.20
   arr, pos = self._array(cx, -0.45, 2, 3, dx=0.50, dy=0.42)
   g.add(Text(lab, font_size=FS_TAG - 2, color=DIM).move_to([cx, 0.30, 0]),
         self._arr([sx * 0.85, 0.73, 0], [cx - sx * 0.55, 0.52, 0], DIM, sw=2, tl=0.10),
         arr)
   # the two arrays disagree in one visible cell, which is the whole claim
   g.add(Dot(pos(0, 1 if sx < 0 else 2), radius=0.085, color=WARN))
  return g.add(Text("≠", font_size=FS_TAG + 3, color=WARN).move_to([0.00, -0.45, 0]),
               self._mid(-1.06, "映射只有一個，矩陣卻有兩個——差別全在基底的選擇",
                         "there is one map but two matrices, and the difference is the basis choice",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.42, "座標空間上矩陣是映射的天然分身，一般空間上不是",
                         "on Cartesian spaces a matrix is a map's natural alter ego; elsewhere it is not",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "所以每次寫下一個矩陣，都要知道自己站在哪一組基底上",
                         "so every matrix written down comes with the bases it was written against",
                         ACCENT_A, FS_TAG, w=11.9))

 def _lemma41(self):
  """The image expanded in the gamma basis, the kth dual basis functional
  reading off one coefficient, and that number landing in cell (k, j).

  W is drawn as a plane, so the array beside it has to have as many rows as
  there are gamma arrows. That is why the whole episode shares one M and one
  N: an earlier draft drew two gammas next to a three-row array, and epsilon
  was then reading a coefficient the array had no room for."""
  o, gv, co = (-4.35, -0.08), ((1.05, 0.15), (0.25, 0.78)), (1.2, 0.9)
  at = lambda v: [o[0] + v[0], o[1] + v[1], 0]
  img = (gv[0][0] * co[0] + gv[1][0] * co[1], gv[0][1] * co[0] + gv[1][1] * co[1])
  g = VGroup()
  for k, v in enumerate(gv):
   g.add(self._arr(at((0, 0)), at(v), ACCENT_C, sw=2.5, tl=0.11),
         Text(f"γ{ISUBS[k]}", font_size=FS_TAG - 4, color=ACCENT_C)
         .move_to(at((v[0] + 0.20, v[1] - 0.18))))
  g.add(self._dash(at((gv[0][0] * co[0], gv[0][1] * co[0])), at(img), DIM, n=7, sw=1.6),
        self._dash(at((gv[1][0] * co[1], gv[1][1] * co[1])), at(img), DIM, n=7, sw=1.6),
        self._arr(at((0, 0)), at(img), WARN, sw=3, tl=0.13),
        Text(f"T ( β{JSUBS[JCOL]} )", font_size=FS_TAG - 3, color=WARN)
        .move_to(at((img[0] + 0.10, img[1] + 0.26))),
        self._arr([-2.30, 0.45, 0], [-0.95, 0.44, 0], ACCENT_A, sw=2.5, tl=0.12),
        Text(f"ε {ISUBS[KROW]}", font_size=FS_TAG - 2, color=ACCENT_A)
        .move_to([-1.62, 0.14, 0]))
  arr, pos = self._array(2.15, 0.40, M, N, dx=0.55, dy=0.45)
  ci, cj = pos(KROW, JCOL)[0], pos(KROW, JCOL)[1]
  return g.add(arr,
               Line([pos(KROW, 0)[0] - 0.22, cj, 0], [pos(KROW, N - 1)[0] + 0.22, cj, 0],
                    color=ACCENT_A, stroke_width=3),
               Line([ci, pos(0, JCOL)[1] + 0.20, 0], [ci, pos(M - 1, JCOL)[1] - 0.20, 0],
                    color=ACCENT_C, stroke_width=3),
               Dot([ci, cj, 0], radius=0.09, color=WARN),
               self._arr([-0.60, 0.48, 0], [0.75, 0.44, 0], WARN, sw=2.5, tl=0.12),
               Text(f"t {ISUBS[KROW]}{JSUBS[JCOL]}", font_size=FS_TAG - 2, color=WARN)
               .move_to([0.08, 0.78, 0]),
               self._mid(-0.82, "對偶基底的作用就是「讀出第 k 個係數」，這裡拿它當量尺",
                         "a dual basis vector reads off one coefficient, and here it is the ruler",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.30, "量到的數就落在第 k 橫列、第 j 直行那一格，隨時可以反推回來",
                         "the number lands in row k and column j, and can be recovered at any time",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "下一集講轉置、秩與矩陣乘法",
                         "next time: the transpose, rank and matrix products",
                         ACCENT_C, FS_TAG, w=11.6))

 def stage(self):
  fn, ms, t41 = self._is_a_function(), self._matrix_space(), self._theorem41()
  lc, tf, rw = self._lincomb(), self._three_faces(), self._rows()
  t42, pf, co = self._theorem42(), self._proof(), self._corollary()
  bd, lm = self._basis_dependent(), self._lemma41()
  return [([fn], []), ([ms], [fn]), ([t41], [ms]), ([lc], [t41]),
          ([tf], [lc]), ([rw], [tf]), ([t42], [rw]), ([pf], [t42]),
          ([co], [pf]), ([bd], [co]), ([lm], [bd])]


AdvCalcE23ZH, AdvCalcE23EN = make(AdvCalcE23Base, "23", prefix="AdvCalcE")
