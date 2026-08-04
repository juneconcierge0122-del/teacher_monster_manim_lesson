"""advcalc E04 — Chapter 0, sections 10-12: duality, Boolean operations,
partitions and equivalence relations.

This is the episode chapter 0 was missing: E03 stopped at section 9 on book
page 15, and the chapter runs to page 21.

The three sections want three different pictures, so the beats fall into three
runs. Duality (beats 0-5) is carried by one rectangular grid of dots read two
ways -- down its columns and along its rows -- which is the whole content of
the section and the one thing the formula bar cannot show. The Boolean run
(6-8) is shaded regions inside a fixed box. The partition run (9-10) is a
rectangle cut into strips, then the integer lattice whose lines through the
origin are exactly the rational numbers.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Difference, Dot, Ellipse, Intersection, Line, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK,
                                             WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# The A x B grid. A runs along x (NA columns), B runs up y (NB rows).
NA, NB = 5, 4
GDX, GDY = 0.40, 0.36


class AdvCalcE04Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 4

 MODE_LABEL = {
  0: {"zh": "固定 x，剩下的是只依賴 y 的函數", "en": "hold x fixed, a function of y remains"},
  1: {"zh": "同一個長方形，兩種讀法", "en": "one rectangle, read two ways"},
  2: {"zh": "矩陣：列的元組，或行的元組", "en": "a matrix: a tuple of rows, or of columns"},
  3: {"zh": "n 個函數，或一個取值為 n 元組的函數",
      "en": "n functions, or one n-tuple-valued function"},
  4: {"zh": "線是點的集合，點是線的集合", "en": "a line is a set of points, a point a set of lines"},
  5: {"zh": "點記法方便，但讀不回去", "en": "the dot is handy, but cannot be read back"},
  6: {"zh": "聯集與交集", "en": "union and intersection"},
  7: {"zh": "不是每個都在　＝　有時候不在", "en": "not always in  =  sometimes not in"},
  8: {"zh": "原像保持三種運算", "en": "the preimage preserves all three"},
  9: {"zh": "纖維化與投影", "en": "a fibering and its projection"},
  10: {"zh": "每個等價關係都來自某個纖維化",
       "en": "every equivalence relation comes from a fibering"},
 }

 # ── the A x B grid, the picture the whole duality section runs on ──
 def _grid(self, cx, cy, hi_col=None, hi_row=None, dim=GHOST):
  """Dots at every (i, j). A highlighted column is one fixed x, a highlighted
  row one fixed y -- the two slicings the section is about."""
  g = VGroup()
  for i in range(NA):
   for j in range(NB):
    on_col = hi_col is not None and i == hi_col
    on_row = hi_row is not None and j == hi_row
    c = ACCENT_A if on_col else (ACCENT_C if on_row else dim)
    g.add(Dot([cx + (i - (NA - 1) / 2) * GDX, cy + (j - (NB - 1) / 2) * GDY, 0],
              radius=0.075 if (on_col or on_row) else 0.055, color=c))
  return g

 def _gridbox(self, cx, cy, color=DIM):
  return Rectangle(width=NA * GDX + 0.30, height=NB * GDY + 0.30,
                   color=color, stroke_width=2).move_to([cx, cy, 0])

 def _axlab(self, cx, cy):
  return VGroup(Text("A", font_size=FS_TAG, color=DIM)
                .move_to([cx, cy - NB * GDY / 2 - 0.38, 0]),
                Text("B", font_size=FS_TAG, color=DIM)
                .move_to([cx - NA * GDX / 2 - 0.40, cy, 0]))

 def _fix_x(self):
  """One column of the grid becomes a single function from B to C."""
  cx, cy = -3.60, 0.05
  col = VGroup(*[Dot([0.95, cy + (j - (NB - 1) / 2) * GDY, 0], radius=0.075, color=ACCENT_A)
                 for j in range(NB)])
  tgt = VGroup(*[Dot([3.15, cy + (j - (NB - 1) / 2) * GDY * 0.7, 0], radius=0.06, color=ACCENT_B)
                 for j in range(NB)])
  g = VGroup(self._gridbox(cx, cy), self._grid(cx, cy, hi_col=2), self._axlab(cx, cy),
             self._arr([cx + NA * GDX / 2 + 0.30, cy, 0], [0.55, cy, 0], ACCENT_A, sw=2.5, tl=0.12),
             col, tgt,
             Text("B", font_size=FS_TAG, color=ACCENT_A).move_to([0.95, cy + 0.95, 0]),
             Text("C", font_size=FS_TAG, color=ACCENT_B).move_to([3.15, cy + 0.95, 0]))
  for j in range(NB):
   g.add(self._arr([1.20, cy + (j - (NB - 1) / 2) * GDY, 0],
                   [2.90, cy + (j - (NB - 1) / 2) * GDY * 0.7, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(-1.55, "一個 x 給出一個函數，這個對應本身又是映射",
                         "each x yields a function, and that correspondence is a mapping",
                         ACCENT_A, FS_TAG, w=11.6))

 def _two_ways(self):
  """The same grid sliced down its columns and along its rows."""
  g = VGroup()
  for cx, hi, lab_zh, lab_en, col in ((-3.10, "col", "一欄一欄讀", "read down the columns", ACCENT_A),
                                      (3.10, "row", "一列一列讀", "read along the rows", ACCENT_C)):
   cy = 0.30
   g.add(self._gridbox(cx, cy),
         self._grid(cx, cy, hi_col=2 if hi == "col" else None,
                    hi_row=None if hi == "col" else 1),
         self._mid(-0.85, lab_zh, lab_en, col, FS_TAG, x=cx, w=4.6))
   for k in range(NA if hi == "col" else NB):
    if hi == "col":
     x = cx + (k - (NA - 1) / 2) * GDX
     g.add(Line([x, cy - NB * GDY / 2 - 0.06, 0], [x, cy + NB * GDY / 2 + 0.06, 0],
                color=ACCENT_A, stroke_width=1.6))
    else:
     y = cy + (k - (NB - 1) / 2) * GDY
     g.add(Line([cx - NA * GDX / 2 - 0.06, y, 0], [cx + NA * GDX / 2 + 0.06, y, 0],
                color=ACCENT_C, stroke_width=1.6))
  return g.add(Text("F", font_size=FS_TAG + 5, color=INK).move_to([0, 0.30, 0]),
               self._mid(-1.55, "兩張圖是同一個 F，只是切法不同",
                         "both pictures are the same F, only sliced differently",
                         DIM, FS_TAG, w=11.6))

 # ── the matrix ────────────────────────────────────────────────────
 M = ((2, -1, 0, 3), (1, 4, -2, 1), (0, 2, 5, -3))

 def _matrix(self):
  """A real 3 x 4 array with one row and one column picked out. The two
  brackets on the right are the point: the same array is a tuple of rows and,
  dually, a tuple of columns."""
  dx, dy = 0.62, 0.52
  ox, oy = -3.30, 0.25
  g = VGroup()
  for i, row in enumerate(self.M):
   for j, v in enumerate(row):
    x, y = ox + (j - 1.5) * dx, oy + (1 - i) * dy
    on_r, on_c = i == 1, j == 2
    c = ACCENT_A if on_r else (ACCENT_C if on_c else INK)
    g.add(Text(str(v), font_size=FS_TAG + 2, color=c).move_to([x, y, 0]))
  g.add(Rectangle(width=4 * dx + 0.34, height=dy + 0.16, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox, oy, 0]),
        Rectangle(width=dx + 0.24, height=3 * dy + 0.30, color=ACCENT_C, stroke_width=2.5)
        .move_to([ox + 0.5 * dx, oy, 0]))
  return g.add(self._mid(0.95, "固定列指標，得到一整列", "fix the row index, get a whole row",
                         ACCENT_A, FS_TAG, x=2.90, w=6.0),
               self._mid(0.25, "固定行指標，得到一整行", "fix the column index, get a column",
                         ACCENT_C, FS_TAG, x=2.90, w=6.0),
               self._mid(-0.45, "同一個矩陣，兩種讀法", "one matrix, two readings",
                         DIM, FS_TAG, x=2.90, w=6.0),
               self._mid(-1.55, "這正是對偶：把兩個指標之一固定住",
                         "this is duality: hold one of the two indices fixed",
                         DIM, FS_TAG, w=11.4))

 def _tuple_fn(self):
  """Three functions out of one point, or one function into a triple."""
  ax, bx = -4.55, -2.30
  ys = (0.72, 0.02, -0.68)
  g = VGroup(Dot([ax, 0.02, 0], radius=0.085, color=ACCENT_B),
             Text("a", font_size=FS_TAG, color=ACCENT_B).move_to([ax, 0.42, 0]))
  for k, y in enumerate(ys):
   g.add(self._arr([ax + 0.20, 0.02, 0], [bx - 0.22, y, 0], ACCENT_A, sw=2.2, tl=0.11),
         Dot([bx, y, 0], radius=0.07, color=ACCENT_A),
         Text(f"f{k + 1} ( a )", font_size=FS_TAG - 2, color=ACCENT_A)
         .move_to([bx + 0.62, y, 0]))
  g.add(Text("B", font_size=FS_TAG, color=DIM).move_to([bx + 0.30, 1.15, 0]))
  cx, dx2 = 1.70, 4.20
  g.add(Dot([cx, 0.02, 0], radius=0.085, color=ACCENT_B),
        Text("a", font_size=FS_TAG, color=ACCENT_B).move_to([cx, 0.42, 0]),
        self._arr([cx + 0.20, 0.02, 0], [dx2 - 1.05, 0.02, 0], ACCENT_C, sw=2.6, tl=0.13),
        Rectangle(width=2.30, height=0.62, color=ACCENT_C, stroke_width=2.5)
        .move_to([dx2, 0.02, 0]),
        Text("⟨ · , · , · ⟩", font_size=FS_TAG, color=ACCENT_C).move_to([dx2, 0.02, 0]),
        Text("B³", font_size=FS_TAG, color=DIM).move_to([dx2, 0.72, 0]))
  return g.add(self._mid(-1.35, "左邊三個函數，右邊一個函數 —— 同一份資料",
                         "three functions on the left, one on the right, the same data",
                         DIM, FS_TAG, w=11.4))

 # ── incidence: points and lines ───────────────────────────────────
 PTS = ((-4.60, -0.95), (-3.05, 0.55), (-1.55, -0.95))
 LNS = ((0, 1), (1, 2), (0, 2))

 def _incidence(self):
  """Three points, three lines, and the 0/1 table that records which is on
  which. Reading the table by rows gives the points on a line; by columns, the
  lines through a point."""
  g = VGroup()
  for a, b in self.LNS:
   pa, pb = np.array(self.PTS[a]), np.array(self.PTS[b])
   d = (pb - pa) / float(np.linalg.norm(pb - pa))
   s, t = pa - 0.42 * d, pb + 0.42 * d
   g.add(Line([s[0], s[1], 0], [t[0], t[1], 0], color=ACCENT_C, stroke_width=2.5))
  for k, (x, y) in enumerate(self.PTS):
   g.add(Dot([x, y, 0], radius=0.085, color=ACCENT_A),
         Text(f"p{k + 1}", font_size=FS_TAG - 2, color=ACCENT_A).move_to([x - 0.02, y + 0.36, 0]))
  dx, dy = 0.66, 0.44
  ox, oy = 3.10, 0.05
  for j in range(3):
   g.add(Text(f"p{j + 1}", font_size=FS_TAG - 3, color=ACCENT_A)
         .move_to([ox + (j - 1) * dx, oy + 1.5 * dy, 0]),
         Text(f"l{j + 1}", font_size=FS_TAG - 3, color=ACCENT_C)
         .move_to([ox - 2.0 * dx, oy + (1 - j) * dy, 0]))
  for i, (a, b) in enumerate(self.LNS):
   for j in range(3):
    v = 1 if j in (a, b) else 0
    g.add(Text(str(v), font_size=FS_TAG, color=INK if v else GHOST)
          .move_to([ox + (j - 1) * dx, oy + (1 - i) * dy, 0]))
  return g.add(self._mid(-1.45, "橫著讀是線上的點，直著讀是過該點的線",
                         "read across for the points on a line, down for the lines through a point",
                         DIM, FS_TAG, w=11.6))

 def _dotnote(self):
  """The dot notation and the flaw: the evaluated value does not remember
  which function produced it."""
  g = VGroup(
   Text("F ( x , · )", font_size=FS_TAG + 5, color=ACCENT_A).move_to([-3.90, 0.72, 0]),
   self._mid(0.10, "在變動的位置擺一個點", "a dot in the position of the varying one",
             DIM, FS_TAG, x=-3.90, w=4.4),
   self._arr([-2.15, 0.72, 0], [-0.55, 0.72, 0], DIM, sw=2.5, tl=0.13),
   Text("F ( x , b )", font_size=FS_TAG + 5, color=ACCENT_B).move_to([0.95, 0.72, 0]),
   self._mid(0.10, "代進去，剩下一個值", "substitute, and a value is left",
             DIM, FS_TAG, x=0.95, w=4.0),
   self._arr([0.95, -0.40, 0], [-3.90, -0.40, 0], WARN, sw=2.5, tl=0.14),
   Text("?", font_size=FS_TAG + 8, color=WARN).move_to([-1.50, -0.78, 0]))
  return g.add(self._mid(-1.35, "從值讀不回原來是哪個函數，所以才要那個累贅的記號",
                         "the value cannot say which function was evaluated, hence the clumsy notation",
                         WARN, FS_TAG, w=11.6))

 # ── Boolean operations ───────────────────────────────────────────
 def _blob(self, cx, cy, rx, ry, color, fill=0.0):
  return Ellipse(width=2 * rx, height=2 * ry, color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=fill).move_to([cx, cy, 0])

 PANEL_H = 2.10
 PANEL_CY = 0.05

 def _panel(self, cx, cy, w=4.30, h=None):
  return Rectangle(width=w, height=h or self.PANEL_H, color=DIM,
                   stroke_width=2).move_to([cx, cy, 0])

 def _boolean(self):
  """Union and intersection of the same two sets, shaded, side by side."""
  g = VGroup()
  for cx, which, zh, en in ((-3.05, "u", "聯集：至少在一個裡面", "union: in at least one"),
                            (3.05, "i", "交集：每一個裡面都在", "intersection: in every one")):
   cy = self.PANEL_CY
   g.add(self._panel(cx, cy),
         Text("S", font_size=FS_TAG - 2, color=DIM).move_to([cx - 1.90, cy + 0.80, 0]))
   for dx, col in ((-0.44, ACCENT_A), (0.44, ACCENT_B)):
    g.add(self._blob(cx + dx, cy, 0.95, 0.66, col, 0.30 if which == "u" else 0.10))
   if which == "i":
    g.add(self._blob(cx, cy, 0.51, 0.55, WARN, 0.55))
   g.add(self._mid(-1.20, zh, en, ACCENT_A if which == "u" else WARN, FS_TAG, x=cx, w=4.6))
  return g.add(self._mid(-1.72, "加上指標之後，這兩個運算對任意多個集合都寫得出來",
                         "with an index set, both operations are written for any family at all",
                         DIM, FS_TAG, w=11.6))

 def _demorgan(self):
  """The complement of the intersection, and the union of the two complements.

  Punching both discs out of the right panel would draw the complement of the
  *union*, which is a different set -- the mistake the law is there to warn
  against. The right panel is therefore built as two overlapping complements,
  each covering everything outside its own disc, so their union visibly leaves
  only the lens uncovered, exactly as on the left."""
  g = VGroup()
  for cx, side in ((-3.05, "L"), (3.05, "R")):
   cy = self.PANEL_CY
   base = Rectangle(width=4.30, height=self.PANEL_H).move_to([cx, cy, 0])
   ea = self._blob(cx - 0.44, cy, 0.95, 0.66, ACCENT_A)
   eb = self._blob(cx + 0.44, cy, 0.95, 0.66, ACCENT_B)
   g.add(self._panel(cx, cy))
   if side == "L":
    g.add(Difference(base, Intersection(ea, eb), stroke_width=0,
                     fill_color=WARN, fill_opacity=0.34))
   else:
    g.add(Difference(base, ea, stroke_width=0, fill_color=ACCENT_A, fill_opacity=0.24),
          Difference(base, eb, stroke_width=0, fill_color=ACCENT_B, fill_opacity=0.24))
   g.add(self._blob(cx - 0.44, cy, 0.95, 0.66, ACCENT_A, 0.0),
         self._blob(cx + 0.44, cy, 0.95, 0.66, ACCENT_B, 0.0))
  return g.add(self._mid(-1.20, "左：交集的補集　　右：兩個補集疊起來",
                         "left: complement of the intersection    right: the two complements laid over each other",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.75, "蓋不到的都只剩中間那一塊 —— 這就是量詞否定規則",
                         "both leave only the lens uncovered: this is the rule for negating quantifiers",
                         WARN, FS_TAG, w=11.6))

 def _preimage(self):
  """Two subsets of B and their preimages in A, so the union on the right
  matches the union on the left piece for piece."""
  ax, bx = -2.40, 1.60
  cy = -0.05
  g = VGroup(self._blob(ax, cy, 1.05, 1.05, DIM, 0.0),
             self._blob(bx, cy, 1.05, 1.05, DIM, 0.0),
             Text("A", font_size=FS_TAG, color=DIM).move_to([ax, cy + 1.19, 0]),
             Text("B", font_size=FS_TAG, color=DIM).move_to([bx, cy + 1.19, 0]))
  for dy, col in ((0.45, ACCENT_A), (-0.45, ACCENT_C)):
   g.add(self._blob(bx, cy + dy, 0.62, 0.38, col, 0.30),
         self._blob(ax, cy + dy, 0.66, 0.40, col, 0.30),
         self._arr([ax + 1.15, cy + dy, 0], [bx - 1.15, cy + dy, 0], col, sw=2.2, tl=0.11))
  return g.add(self._mid(-1.45, "右邊取聯集、交集或補集，左邊的原像照著一起變",
                         "take a union, an intersection or a complement on the right and the preimage follows",
                         DIM, FS_TAG, w=11.6))

 # ── partitions ────────────────────────────────────────────────────
 NSTRIP = 5

 def _fibering(self):
  """A rectangle cut into disjoint strips, each strip sent to one dot."""
  cols = (ACCENT_A, ACCENT_B, ACCENT_C, WARN, ACCENT_A)
  ox, oy, w, h = -3.30, -0.10, 3.20, 1.85
  sh = h / self.NSTRIP
  g = VGroup(Text("A", font_size=FS_TAG, color=DIM).move_to([ox, oy + h / 2 + 0.32, 0]))
  for k in range(self.NSTRIP):
   y = oy + h / 2 - (k + 0.5) * sh
   g.add(Rectangle(width=w, height=sh, color=cols[k], stroke_width=2,
                   fill_color=cols[k], fill_opacity=0.20).move_to([ox, y, 0]),
         Dot([2.60, y, 0], radius=0.08, color=cols[k]),
         self._arr([ox + w / 2 + 0.16, y, 0], [2.40, y, 0], cols[k], sw=2, tl=0.10))
  return g.add(Text("ℱ", font_size=FS_TAG + 3, color=DIM).move_to([2.60, oy + h / 2 + 0.38, 0]),
               self._mid(-1.45, "每一塊是一根纖維，把點送到它那根纖維就是投影",
                         "each strip is a fiber; sending a point to its fiber is the projection",
                         DIM, FS_TAG, w=11.6))

 LAT = 3

 def _rationals(self):
  """The book's own example. Integer pairs with second entry nonzero; two of
  them are equivalent exactly when they lie on one line through the origin,
  and each such line is one rational number."""
  s = 0.42
  ox, oy = -2.05, -0.10
  g = VGroup()
  for m in range(-self.LAT, self.LAT + 1):
   for n in range(-self.LAT, self.LAT + 1):
    if n == 0:
     continue
    g.add(Dot([ox + m * s, oy + n * s, 0], radius=0.045, color=GHOST))
  for (m, n), col in (((1, 2), ACCENT_A), ((1, 1), ACCENT_B), ((3, 1), ACCENT_C)):
   k = max(abs(v) for v in (m, n))
   f = self.LAT / k
   g.add(Line([ox - f * m * s, oy - f * n * s, 0], [ox + f * m * s, oy + f * n * s, 0],
              color=col, stroke_width=2.5))
   for j in (1, -1):
    for t in range(1, int(f) + 1):
     g.add(Dot([ox + j * t * m * s, oy + j * t * n * s, 0], radius=0.065, color=col))
  g.add(self._mid(0.95, "同一條過原點的線 = 同一個有理數",
                  "one line through the origin = one rational number",
                  ACCENT_A, FS_TAG, x=2.85, w=6.2),
        self._mid(0.25, "自反、對稱、遞移", "reflexive, symmetric, transitive",
                  DIM, FS_TAG, x=2.85, w=6.2),
        self._mid(-0.45, "所以等價類就是纖維", "so the classes are exactly the fibers",
                  ACCENT_B, FS_TAG, x=2.85, w=6.2))
  return g.add(self._mid(-1.60, "模 p 的整數也一樣造出來：餘數相同的算成一個",
                         "the integers modulo p are built the same way, by common remainder",
                         DIM, FS_TAG, w=11.6))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  fx, tw = self._fix_x(), self._two_ways()
  mat, tup = self._matrix(), self._tuple_fn()
  inc, dn = self._incidence(), self._dotnote()
  boo, dm, pre = self._boolean(), self._demorgan(), self._preimage()
  fib, rat = self._fibering(), self._rationals()

  return [([fx], []),                          # 0  hold x fixed
          ([tw], [fx]),                        # 1  one rectangle, two slicings
          ([mat], [tw]),                       # 2  the matrix
          ([tup], [mat]),                      # 3  n functions vs one
          ([inc], [tup]),                      # 4  points and lines
          ([dn], [inc]),                       # 5  the dot notation
          ([boo], [dn]),                       # 6  union and intersection
          ([dm], [boo]),                       # 7  De Morgan
          ([pre], [dm]),                       # 8  preimages
          ([fib], [pre]),                      # 9  fibering
          ([rat], [fib])]                      # 10 equivalence relations


AdvCalcE04ZH, AdvCalcE04EN = make(AdvCalcE04Base, "04", prefix="AdvCalcE")
