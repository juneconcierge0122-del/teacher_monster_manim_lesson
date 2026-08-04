"""advcalc E08 — Chapter 1, section 1, last part (book pp. 32-36): matrices,
Theorems 1.3 and 1.4, the kernel, isomorphism and eigenvectors.

The matrix beats have an easy failure mode: a grid of symbols on screen under a
grid of symbols in the formula bar. So the array here is always drawn with its
columns boxed and traced back to the skeleton entries they came from, which is
the fact the array alone does not show.

Beats 7 to 9 are about what a linear map does to whole subspaces, so they are
drawn as a plane collapsing onto a line -- the kernel is the direction that
collapses, and that is also why injectivity is a statement about one subspace
rather than about pairs of vectors.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE08Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 8

 MODE_LABEL = {
  0: {"zh": "線性泛函：skeleton 是一組數", "en": "a functional: the skeleton is numbers"},
  1: {"zh": "泛函與座標空間自然對應", "en": "functionals correspond to the space itself"},
  2: {"zh": "每一項是一個 m 元組", "en": "each entry is an m-tuple"},
  3: {"zh": "矩陣的行就是 skeleton", "en": "the columns of the matrix are the skeleton"},
  4: {"zh": "攤開成 m 個純量方程", "en": "written out as m scalar equations"},
  5: {"zh": "矩陣與線性映射一一對應", "en": "matrices and linear maps correspond"},
  6: {"zh": "座標泛函", "en": "the coordinate functionals"},
  7: {"zh": "子空間的像還是子空間", "en": "the image of a subspace is a subspace"},
  8: {"zh": "核：被壓成零的那些向量", "en": "the kernel: what collapses to zero"},
  9: {"zh": "同構：同一個空間的兩種寫法", "en": "isomorphism: one space, two notations"},
  10: {"zh": "特徵向量與特徵值", "en": "eigenvectors and eigenvalues"},
 }

 # ── beats 0-1: the functional ────────────────────────────────────
 B = (3, -1, 2, 4)

 def _functional(self):
  ox = -3.35
  g = VGroup()
  for k, b in enumerate(self.B):
   x = ox + k * 1.02
   g.add(Rectangle(width=0.72, height=0.50, color=ACCENT_B, stroke_width=2)
         .move_to([x, 0.74, 0]),
         Text(f"δ{'¹²³⁴'[k]}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, 0.74, 0]),
         self._arr([x, 0.42, 0], [x, -0.06, 0], DIM, sw=2, tl=0.10),
         Text(str(b), font_size=FS_TAG + 3, color=ACCENT_A).move_to([x, -0.36, 0]))
  g.add(Rectangle(width=4.20, height=0.62, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 1.53, -0.36, 0]),
        Text("F", font_size=FS_TAG + 2, color=ACCENT_A).move_to([ox - 0.95, 0.74, 0]))
  return g.add(self._mid(0.85, "把每個單位向量餵進去", "feed in each unit vector",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.15, "得到的都只是一個數", "and each answer is just a number",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "整個 skeleton 是一組係數", "so the skeleton is a row of coefficients",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.55, "泛函的值，就是係數乘座標再加起來",
                         "the functional's value is coefficients times coordinates, summed",
                         DIM, FS_TAG, w=11.4))

 def _natural(self):
  ax, bx = -2.35, 1.75
  ys = (0.80, 0.24, -0.32, -0.88)
  g = VGroup(self._mid(1.10, "所有線性泛函", "all the linear functionals",
                       ACCENT_A, FS_TAG, x=ax, w=3.4),
             self._mid(1.10, "座標空間自己", "the coordinate space itself",
                       ACCENT_B, FS_TAG, x=bx, w=3.4))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_A),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_B),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.75, "由泛函取值得到係數", "evaluate to get the coefficients",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-0.05, "由係數做加權和得到泛函", "weight and sum to get the functional",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.55, "所以這兩邊是自然的一一對應",
                         "so the two sides correspond naturally, one to one",
                         ACCENT_A, FS_TAG, w=11.4))

 # ── beats 2-5: the matrix ────────────────────────────────────────
 M = ((2, -1, 0), (1, 4, -2), (0, 2, 5))

 def _columns(self):
  """The skeleton entries standing up as columns before they are a matrix."""
  dy, dx = 0.50, 1.30
  ox, oy = -2.60, 0.10
  g = VGroup()
  for j in range(3):
   x = ox + j * dx
   g.add(Rectangle(width=0.86, height=3 * dy + 0.28, color=(ACCENT_B, ACCENT_C, ACCENT_A)[j],
                   stroke_width=2.5).move_to([x, oy, 0]),
         Text(f"T ( δ{'¹²³'[j]} )", font_size=FS_TAG - 3,
              color=(ACCENT_B, ACCENT_C, ACCENT_A)[j]).move_to([x, oy + 1.10, 0]))
   for i in range(3):
    g.add(Text(str(self.M[i][j]), font_size=FS_TAG + 2, color=INK)
          .move_to([x, oy + (1 - i) * dy, 0]))
  return g.add(self._mid(-1.05, "每一項都是一個 m 元組，畫成一直行",
                         "each entry is an m-tuple, drawn as a column",
                         DIM, FS_TAG, x=ox + dx, w=6.0),
               self._mid(0.75, "n 個這樣的行並排", "n such columns side by side",
                         DIM, FS_TAG, x=3.85, w=4.2),
               self._mid(-0.05, "就成了一個長方形陣列", "make a rectangular array",
                         ACCENT_A, FS_TAG, x=3.85, w=4.2),
               self._mid(-1.62, "這個帶兩個指標的數組，就叫 T 的矩陣",
                         "that doubly indexed array is the matrix of T",
                         DIM, FS_TAG, w=11.4))

 def _matrix_cols(self):
  """The array with its columns boxed and labelled back to the skeleton."""
  dy, dx = 0.50, 0.72
  ox, oy = -2.85, 0.05
  g = VGroup()
  for i in range(3):
   for j in range(3):
    g.add(Text(str(self.M[i][j]), font_size=FS_TAG + 2, color=INK)
          .move_to([ox + (j - 1) * dx, oy + (1 - i) * dy, 0]))
  for j in range(3):
   # the box has to be narrower than the column pitch, or adjacent boxes
   # share a border and the array reads as a grid of cells
   g.add(Rectangle(width=dx - 0.06, height=3 * dy + 0.24,
                   color=(ACCENT_B, ACCENT_C, ACCENT_A)[j], stroke_width=2.5)
         .move_to([ox + (j - 1) * dx, oy, 0]),
         Text(f"δ{'¹²³'[j]}", font_size=FS_TAG - 4, color=(ACCENT_B, ACCENT_C, ACCENT_A)[j])
         .move_to([ox + (j - 1) * dx, oy - 1.10, 0]))
  return g.add(self._mid(0.95, "第 j 行就是 T 在第 j 個單位向量的值",
                         "the jth column is T at the jth unit vector",
                         ACCENT_A, FS_TAG, x=2.85, w=6.2),
               self._mid(0.15, "所以矩陣唯一決定 T", "so the matrix determines T uniquely",
                         DIM, FS_TAG, x=2.85, w=6.2),
               self._mid(-0.65, "因為它的各行正好是 skeleton",
                         "because its columns are exactly the skeleton",
                         DIM, FS_TAG, x=2.85, w=6.2),
               self._mid(-1.62, "矩陣不是新東西，是 skeleton 換一個排法",
                         "the matrix is not new: it is the skeleton, laid out",
                         DIM, FS_TAG, w=11.4))

 def _rows(self):
  """The ith output traced across the ith row and down the input column."""
  dy, dx = 0.50, 0.72
  ox, oy = -3.15, 0.15
  g = VGroup()
  for i in range(3):
   for j in range(3):
    on = i == 1
    g.add(Text(str(self.M[i][j]), font_size=FS_TAG + 2, color=ACCENT_A if on else DIM)
          .move_to([ox + (j - 1) * dx, oy + (1 - i) * dy, 0]))
  g.add(Rectangle(width=3 * dx + 0.28, height=dy + 0.14, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox, oy, 0]))
  bx = ox + 1.75
  for j in range(3):
   g.add(Text(f"x{j + 1}", font_size=FS_TAG, color=ACCENT_B)
         .move_to([bx, oy + (1 - j) * dy, 0]))
  g.add(Rectangle(width=0.78, height=3 * dy + 0.24, color=ACCENT_B, stroke_width=2.5)
        .move_to([bx, oy, 0]),
        Text("=", font_size=FS_TAG + 5, color=DIM).move_to([bx + 0.78, oy, 0]),
        Text("y₂", font_size=FS_TAG + 1, color=ACCENT_A).move_to([bx + 1.50, oy, 0]))
  return g.add(self._mid(0.95, "第 i 列的係數", "the coefficients in the ith row",
                         ACCENT_A, FS_TAG, x=3.60, w=4.9),
               self._mid(0.20, "乘上對應的輸入座標", "times the matching input coordinates",
                         ACCENT_B, FS_TAG, x=3.60, w=4.9),
               self._mid(-0.55, "加起來就是第 i 個輸出", "summed, give the ith output",
                         DIM, FS_TAG, x=3.60, w=4.9),
               self._mid(-1.62, "一般的線性方程組就是這樣來的",
                         "this is where a general system of linear equations comes from",
                         DIM, FS_TAG, w=11.4))

 def _corr(self):
  ax, bx = -2.45, 1.75
  ys = (0.78, 0.22, -0.34)
  g = VGroup(self._mid(1.10, "m 乘 n 的矩陣", "m by n matrices", ACCENT_B, FS_TAG, x=ax, w=3.2),
             self._mid(1.10, "線性映射", "linear maps", ACCENT_A, FS_TAG, x=bx, w=3.2))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  g.add(Text("⋮", font_size=FS_TAG + 4, color=GHOST).move_to([ax, -0.80, 0]),
        Text("⋮", font_size=FS_TAG + 4, color=GHOST).move_to([bx, -0.80, 0]),
        Rectangle(width=2.30, height=0.44, color=WARN, stroke_width=2.5).move_to([ax, -1.42, 0]),
        self._mid(-1.42, "只有一列", "a single row", WARN, FS_TAG, x=ax, w=2.1),
        self._mid(-1.42, "線性泛函", "a linear functional", WARN, FS_TAG, x=bx, w=2.6))
  return g.add(self._mid(0.75, "每個矩陣給一個映射", "each matrix gives a map",
                         DIM, FS_TAG, x=4.35, w=3.4),
               self._mid(-0.05, "每個映射給一個矩陣", "each map gives a matrix",
                         ACCENT_A, FS_TAG, x=4.35, w=3.4))

 def _coord_fn(self):
  """Evaluation at one index, pulled out of a function."""
  ax, w, base = -2.75, 3.60, -0.35
  ts = np.linspace(-1, 1, 70)
  g = VGroup(Line([ax - w / 2, base, 0], [ax + w / 2, base, 0], color=GHOST, stroke_width=2),
             self._curve([[ax + t * w / 2, base + 0.62 + 0.42 * np.sin(2.3 * t), 0] for t in ts],
                         ACCENT_B, sw=3))
  x0 = ax + 0.30
  y0 = base + 0.62 + 0.42 * np.sin(2.3 * (x0 - ax) / (w / 2))
  g.add(self._dash([x0, base, 0], [x0, y0, 0], GHOST, n=6),
        Dot([x0, y0, 0], radius=0.08, color=ACCENT_A),
        Text("i", font_size=FS_TAG - 2, color=DIM).move_to([x0, base - 0.28, 0]),
        self._arr([x0 + 0.20, y0, 0], [1.55, y0, 0], ACCENT_A, sw=2.5, tl=0.13),
        Text("f ( i )", font_size=FS_TAG, color=ACCENT_A).move_to([2.10, y0, 0]))
  return g.add(self._mid(0.95, "在指標集上的函數空間裡", "on a function space over an index set",
                         DIM, FS_TAG, x=3.70, w=4.9),
               self._mid(-0.45, "取第 i 個位置的值", "take the value at the ith place",
                         ACCENT_A, FS_TAG, x=3.70, w=4.9),
               self._mid(-1.55, "函數上的向量運算，當初就是為了讓這些取值變成線性的",
                         "the vector operations on functions were defined to make these linear",
                         DIM, FS_TAG, w=11.6))

 # ── beats 7-8: subspaces, the kernel ─────────────────────────────
 def _collapse(self):
  """A plane through the origin carried onto a line: still a subspace, and
  the collapsed direction is the kernel of the next beat."""
  org1 = np.array([-3.35, -0.20, 0.0])
  s = 0.80
  quad = [_p(v, org1, s) for v in ((-1.6, -1.4, 0), (1.6, -1.4, 0), (1.6, 1.4, 0), (-1.6, 1.4, 0))]
  o1 = _p(np.zeros(3), org1, s)
  g = VGroup(Polygon(*quad, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.13),
             self._arr(o1, _p(np.array([1.2, -0.7, 0]), org1, s), ACCENT_C, sw=3, tl=0.14),
             self._arr(o1, _p(np.array([0.2, 1.2, 0]), org1, s), ACCENT_C, sw=3, tl=0.14),
             Dot(o1, radius=0.06, color=INK),
             self._mid(1.05, "一個子空間", "a subspace", ACCENT_B, FS_TAG, x=-3.35, w=3.0))
  o2 = np.array([2.95, -0.20, 0.0])
  d = np.array([1.05, 0.42, 0.0])
  g.add(Line(o2 - 1.5 * d, o2 + 1.5 * d, color=ACCENT_A, stroke_width=4),
        Dot(o2, radius=0.06, color=INK),
        self._arr(o2, o2 + 0.95 * d, ACCENT_C, sw=3, tl=0.14),
        self._mid(1.05, "像還是子空間", "the image is again a subspace",
                  ACCENT_A, FS_TAG, x=2.95, w=4.2),
        self._arr([-0.75, -0.20, 0], [0.85, -0.20, 0], ACCENT_A, sw=3, tl=0.16),
        Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([0.05, 0.10, 0]))
  return g.add(self._mid(-1.55, "線性把線性擴張送到像的線性擴張，原像也一樣是子空間",
                         "a linear map carries spans onto spans, and preimages are subspaces too",
                         DIM, FS_TAG, w=11.8))

 def _kernel(self):
  """The direction that collapses, drawn inside the domain."""
  org1 = np.array([-3.35, -0.20, 0.0])
  s = 0.80
  quad = [_p(v, org1, s) for v in ((-1.6, -1.4, 0), (1.6, -1.4, 0), (1.6, 1.4, 0), (-1.6, 1.4, 0))]
  o1 = _p(np.zeros(3), org1, s)
  kdir = np.array([0.9, 1.1, 0])
  g = VGroup(Polygon(*quad, color=DIM, stroke_width=2, fill_color=DIM, fill_opacity=0.07),
             Line(_p(-1.15 * kdir, org1, s), _p(1.15 * kdir, org1, s),
                  color=WARN, stroke_width=4),
             Dot(o1, radius=0.06, color=INK),
             Text("N ( T )", font_size=FS_TAG, color=WARN)
             .move_to(_p(1.15 * kdir, org1, s) + np.array([0.16, 0.26, 0])),
             self._mid(1.10, "被壓成零的方向", "the direction that collapses",
                       WARN, FS_TAG, x=-3.35, w=3.6))
  o2 = np.array([2.95, -0.20, 0.0])
  d = np.array([1.05, 0.42, 0.0])
  g.add(Line(o2 - 1.5 * d, o2 + 1.5 * d, color=ACCENT_A, stroke_width=4),
        Dot(o2, radius=0.10, color=WARN),
        Text("0", font_size=FS_TAG, color=WARN).move_to(o2 + np.array([0.0, -0.36, 0])),
        self._mid(1.10, "值域", "the range", ACCENT_A, FS_TAG, x=2.95, w=3.0),
        self._arr([-0.75, -0.20, 0], [0.85, -0.20, 0], ACCENT_A, sw=3, tl=0.16),
        Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([0.05, 0.10, 0]))
  return g.add(self._mid(-1.55, "核只有零向量時，就沒有東西被壓在一起 —— 這就是嵌射",
                         "when the kernel is only zero nothing is collapsed together: that is injectivity",
                         ACCENT_A, FS_TAG, w=11.8))

 def _isomorphism(self):
  """The book's own example: a triple and a polynomial, entry by entry."""
  ox, dy = -3.25, 0.62
  coeffs = ("c₁", "c₂", "c₃")
  terms = ("c₁ · 1", "c₂ · x", "c₃ · x²")
  g = VGroup()
  for k in range(3):
   y = 0.66 - k * dy
   g.add(Rectangle(width=0.80, height=0.48, color=ACCENT_B, stroke_width=2).move_to([ox, y, 0]),
         Text(coeffs[k], font_size=FS_TAG - 2, color=ACCENT_B).move_to([ox, y, 0]),
         self._arr([ox + 0.48, y, 0], [ox + 1.55, y, 0], DIM, sw=2, tl=0.10),
         Text(terms[k], font_size=FS_TAG, color=ACCENT_A).move_to([ox + 2.30, y, 0]))
  g.add(Rectangle(width=1.10, height=3 * dy + 0.20, color=ACCENT_B, stroke_width=2.5)
        .move_to([ox, -0.02, 0]),
        self._mid(1.15, "ℝ³", "ℝ³", ACCENT_B, FS_TAG, x=ox, w=1.0),
        self._mid(1.15, "次數小於 3 的多項式", "polynomials of degree less than 3",
                  ACCENT_A, FS_TAG, x=ox + 2.70, w=3.4))
  return g.add(self._mid(0.55, "既線性又雙射", "both linear and bijective",
                         DIM, FS_TAG, x=3.85, w=4.2),
               self._mid(-0.25, "所以是同構", "so it is an isomorphism",
                         ACCENT_A, FS_TAG, x=3.85, w=4.2),
               self._mid(-1.55, "同構的兩個空間，作為抽象向量空間根本就是同一個",
                         "isomorphic spaces simply are the same abstract vector space",
                         DIM, FS_TAG, w=11.6))

 def _eigen(self):
  """One vector kept on its own line, one turned off it."""
  o = np.array([-2.15, -0.45, 0.0])
  u = np.array([1.35, 0.72, 0.0])
  v = np.array([1.05, -0.52, 0.0])
  Mv = np.array([0.30, 1.10, 0.0])
  g = VGroup(Line(o - 0.55 * u, o + 2.15 * u, color=GHOST, stroke_width=2),
             self._arr(o, o + u, ACCENT_B, sw=3, tl=0.14),
             self._arr(o, o + 1.75 * u, ACCENT_A, sw=4.5, tl=0.20),
             self._arr(o, o + v, ACCENT_C, sw=3, tl=0.14),
             self._arr(o, o + Mv, WARN, sw=3, tl=0.14),
             self._dash(o + v, o + Mv, GHOST, n=7),
             Dot(o, radius=0.06, color=INK),
             Text("α", font_size=FS_TAG, color=ACCENT_B)
             .move_to(o + u + np.array([-0.10, -0.28, 0])),
             Text("T α", font_size=FS_TAG, color=ACCENT_A)
             .move_to(o + 1.75 * u + np.array([0.30, 0.16, 0])))
  return g.add(self._mid(1.05, "留在同一條線上：特徵向量",
                         "kept on its own line: an eigenvector",
                         ACCENT_A, FS_TAG, x=2.95, w=5.4),
               self._mid(0.20, "倍數就是特徵值", "and the multiple is the eigenvalue",
                         DIM, FS_TAG, x=2.95, w=5.4),
               self._mid(-0.60, "轉離了原來的方向：不是", "turned off its line: not one",
                         WARN, FS_TAG, x=2.95, w=5.4),
               self._mid(-1.55, "這條線索到第二章與第五章會再展開",
                         "this thread is picked up again in chapters two and five",
                         DIM, FS_TAG, w=11.4))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  fn, nat = self._functional(), self._natural()
  cols, mc, rows = self._columns(), self._matrix_cols(), self._rows()
  corr, cf = self._corr(), self._coord_fn()
  col2, ker = self._collapse(), self._kernel()
  iso, eig = self._isomorphism(), self._eigen()

  return [([fn], []),                          # 0  the functional's skeleton
          ([nat], [fn]),                       # 1  the natural correspondence
          ([cols], [nat]),                     # 2  entries as columns
          ([mc], [cols]),                      # 3  columns are the skeleton
          ([rows], [mc]),                      # 4  the m scalar equations
          ([corr], [rows]),                    # 5  matrices and maps
          ([cf], [corr]),                      # 6  coordinate functionals
          ([col2], [cf]),                      # 7  subspaces carry over
          ([ker], [col2]),                     # 8  the kernel
          ([iso], [ker]),                      # 9  isomorphism
          ([eig], [iso])]                      # 10 eigenvectors


AdvCalcE08ZH, AdvCalcE08EN = make(AdvCalcE08Base, "08", prefix="AdvCalcE")
