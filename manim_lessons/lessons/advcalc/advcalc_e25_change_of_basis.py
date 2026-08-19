"""advcalc E25 -- Chapter 2, section 4, last part (book pp. 93-96): Cartesian
vectors read as column and row matrices, a linear map as left multiplication, a
functional as a row vector and the adjoint as right multiplication, the change
of coordinates isomorphism, the two-storey diagram and the identity it can be
read off, the similarity form, covariant and contravariant, and the standard
basis D_kl of Hom(V, W). Section 4 ends at p. 96; pp. 96-98 are exercises and
are not covered, and p. 99 begins section 5.

Beat 5 is the episode's hinge and is drawn as three stacked rows -- two storeys
of Cartesian spaces with the abstract pair between them -- so that beat 6 can
trace one path around it against the direct arrow. The book's Fig. 2.2 draws the
same nine maps as a prism; this composition is deliberately not that one.

Beat 8 makes the covariant/contravariant pair concrete rather than verbal: one
change matrix drives both rules, and the two rules use matrices inverse to each
other, which is the whole content of the two words.

Symbols continue E23 and E24: beta and beta-prime are the two bases of V, gamma
and gamma-prime the two of W, epsilon the dual basis. phi and psi are the basis
isomorphisms of E23, now numbered for the two choices; a and b are the change of
coordinate matrices and t-prime and t-double-prime the matrices of T against the
two pairs of bases. T-prime is again the Cartesian transcription of T, the same
role the prime played in E23.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# The same worked example as E23 and E24: t is m by n with m = 2, n = 3.
M, N = 2, 3
KROW, JCOL = 1, 2                            # the k and l of D_kl, 0-based

ISUBS = ("₁", "₂")                           # i = 1 … m : rows of t, and gamma
JSUBS = ("₁", "₂", "₃")                      # j = 1 … n : columns of t, and beta

assert len(ISUBS) == M and len(JSUBS) == N


class AdvCalcE25Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 25

 MODE_LABEL = {
  0: {"zh": "一個 n 元組的兩種讀法", "en": "two ways to read an n-tuple"},
  1: {"zh": "映射就是左乘一個矩陣", "en": "a map is left multiplication by a matrix"},
  2: {"zh": "泛函就是列向量", "en": "a functional is a row vector"},
  3: {"zh": "伴隨算子變成右乘", "en": "the adjoint becomes right multiplication"},
  4: {"zh": "換座標，不是空間上的映射",
      "en": "a change of coordinates, not a map on the space"},
  5: {"zh": "兩層的圖：九個映射", "en": "the two-storey diagram: nine maps"},
  6: {"zh": "兩條路一樣，等式就讀出來了",
      "en": "two paths agree, and the identity falls out"},
  7: {"zh": "同一個空間，與實數那一側", "en": "one space, and the real line side"},
  8: {"zh": "共變與逆變：同一個換基底，兩條反向的規則",
      "en": "covariant and contravariant: one change, two inverse rules"},
  9: {"zh": "Hom(V, W) 的標準基底", "en": "the standard basis of Hom(V, W)"},
  10: {"zh": "矩陣元素就是這組基底下的座標",
       "en": "the entries were the coordinates all along"},
 }

 # ── beats ─────────────────────────────────────────────────────────
 def _two_readings(self):
  """One tuple, two shapes. Both readings are built from the same JSUBS, so
  the column and the row cannot end up listing different entries."""
  ent = [f"x{JSUBS[j]}" for j in range(N)]
  g = VGroup(Text("⟨  " + "  ,  ".join(ent) + "  ⟩", font_size=FS_TAG + 1, color=DIM)
             .move_to([0.00, 1.05, 0]),
             self._column(-2.80, -0.15, [(e, ACCENT_B) for e in ent], dy=0.44),
             self._arr([-0.80, 0.80, 0], [-2.40, 0.30, 0], ACCENT_B, sw=2.5, tl=0.12),
             self._arr([0.80, 0.80, 0], [2.00, 0.30, 0], ACCENT_C, sw=2.5, tl=0.12))
  y0 = -0.15
  for j, e in enumerate(ent):
   g.add(Text(e, font_size=FS_TAG - 3, color=ACCENT_C).move_to([2.55 + j * 0.75, y0, 0]))
  return g.add(self._brackets(2.55 - 0.34, 2.55 + (N - 1) * 0.75 + 0.34, y0 - 0.24, y0 + 0.24),
               Text("n × 1", font_size=FS_TAG - 3, color=ACCENT_B).move_to([-2.80, -0.95, 0]),
               Text("1 × n", font_size=FS_TAG - 3, color=ACCENT_C).move_to([3.30, -0.78, 0]),
               self._mid(-1.32, "兩種讀法都是自然同構，不必挑，所以可以直接當成同一個東西",
                         "both readings are natural isomorphisms, so they are simply identified",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "書上把行向量定為標準的那一個，列向量寫成它的轉置",
                         "the book fixes the column vector as standard; the row is its transpose",
                         ACCENT_A, FS_TAG, w=11.9))

 def _left_mult(self):
  """The scalar equations of E24, now read as one matrix product."""
  t, pos = self._array(-3.20, 0.55, M, N, dx=0.50, dy=0.46)
  g = VGroup(t, Text("t", font_size=FS_TAG - 3, color=DIM).move_to([-3.20, -0.30, 0]),
             self._column(-1.85, 0.55, [(f"x{JSUBS[j]}", ACCENT_B) for j in range(N)], dy=0.42),
             Text("x", font_size=FS_TAG - 3, color=ACCENT_B).move_to([-1.85, -0.42, 0]),
             Text("=", font_size=FS_TAG + 1, color=DIM).move_to([-1.05, 0.55, 0]),
             self._column(-0.25, 0.55,
                          [(f"y{ISUBS[i]}", WARN if i == KROW else DIM) for i in range(M)],
                          dy=0.42),
             Text("y", font_size=FS_TAG - 3, color=WARN).move_to([-0.25, -0.30, 0]),
             Line([pos(KROW, 0)[0] - 0.22, pos(KROW, 0)[1], 0],
                  [pos(KROW, N - 1)[0] + 0.22, pos(KROW, 0)[1], 0],
                  color=WARN, stroke_width=3))
  return g.add(self._box(3.05, 0.55, "T   :   x  ↦  t x", ACCENT_A, w=3.60, h=0.66,
                         size=FS_TAG),
               self._mid(-0.30, "映射與乘法合而為一", "map and product coincide",
                         ACCENT_A, FS_TAG, x=3.05, w=3.40),
               self._mid(-1.05, "把座標空間看成行向量的空間之後，線性映射就只是「左乘一個固定矩陣」",
                         "viewing a Cartesian space as columns, a linear map is left multiplication",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "上一集那組純量方程，其實一直就是這條乘法",
                         "last episode's scalar equations were this product all along",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "而輸出的第 i 格，還是第 i 橫列配上整個輸入",
                         "and the ith output is still the ith row against the whole input",
                         WARN, FS_TAG, w=11.9))

 def _functional_row(self):
  """A row times a column is a one by one matrix, which is a number. The
  shapes are spelled out because that is the entire point of the beat."""
  ent = [f"a{JSUBS[j]}" for j in range(N)]
  g = VGroup()
  for j, e in enumerate(ent):
   g.add(Text(e, font_size=FS_TAG - 3, color=ACCENT_C).move_to([-4.30 + j * 0.75, 0.55, 0]))
  g.add(self._brackets(-4.64, -4.30 + (N - 1) * 0.75 + 0.34, 0.31, 0.79),
        Text("a *", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-3.55, -0.10, 0]),
        Text("·", font_size=FS_TAG + 2, color=DIM).move_to([-1.55, 0.55, 0]),
        self._column(-0.70, 0.55, [(f"x{JSUBS[j]}", ACCENT_B) for j in range(N)], dy=0.42),
        Text("x", font_size=FS_TAG - 3, color=ACCENT_B).move_to([-0.70, -0.42, 0]),
        Text("=", font_size=FS_TAG + 1, color=DIM).move_to([0.35, 0.55, 0]),
        self._box(1.55, 0.55, "Σ aᵢ xᵢ", WARN, w=1.70, h=0.62, size=FS_TAG - 1),
        Text("1 × n", font_size=FS_TAG - 4, color=ACCENT_C).move_to([-3.55, 1.05, 0]),
        Text("n × 1", font_size=FS_TAG - 4, color=ACCENT_B).move_to([-0.70, 1.15, 0]),
        Text("1 × 1", font_size=FS_TAG - 4, color=WARN).move_to([1.55, 1.05, 0]))
  return g.add(self._mid(-0.35, "一乘一的矩陣，就是一個數",
                         "a one by one matrix is a number",
                         WARN, FS_TAG, x=3.60, w=4.60),
               self._mid(-1.05, "泛函的矩陣是一列 n 行，所以泛函就是列向量",
                         "the matrix of a functional is 1 by n, so a functional is a row vector",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.44, "第 21 集那個 a 對應到 L a 的自然同構，現在有了矩陣的說法",
                         "the natural isomorphism of episode 21 now has a matrix reading",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "純量積就是列向量乘行向量——形狀自己把它逼出來",
                         "the scalar product is a row times a column, forced by the shapes alone",
                         ACCENT_A, FS_TAG, w=11.9))

 def _adjoint_right(self):
  """Left multiplication acts on the input; right multiplication acts on the
  functional. The two sit on opposite sides of the same t on purpose."""
  g = VGroup(self._box(-3.30, 0.95, "L a ( T ( x ) )   =   a * t x", ACCENT_B, w=4.60,
                       h=0.66, size=FS_TAG),
             self._arr([-3.30, 0.58, 0], [-3.30, 0.16, 0], DIM, sw=2, tl=0.10),
             self._box(-3.30, -0.20, "T * ( L a )   =   a * t", WARN, w=4.20, h=0.66,
                       size=FS_TAG),
             Line([0.35, -0.95, 0], [0.35, 1.25, 0], color=DIM, stroke_width=1.6),
             self._box(3.20, 0.95, "a *  ·  t", WARN, w=2.60, h=0.62, size=FS_TAG),
             self._box(3.20, -0.20, "t *  ·  a", ACCENT_C, w=2.60, h=0.62, size=FS_TAG))
  return g.add(self._mid(0.95, "列向量：右乘", "as a row: multiply on the right",
                         WARN, FS_TAG, x=5.30, w=1.90),
               self._mid(-0.20, "行向量：左乘", "as a column: on the left",
                         ACCENT_C, FS_TAG, x=5.30, w=1.90),
               self._mid(-1.05, "泛函寫成列向量時，伴隨算子是從右邊乘上去的",
                         "with functionals written as rows, the adjoint multiplies from the right",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.44, "取轉置把它換回行向量，右乘就變成左乘轉置矩陣",
                         "transpose back to columns and right becomes left, by the transpose",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "所以這是「伴隨算子的矩陣是轉置」的第二個證明",
                         "so this is a second proof that the adjoint's matrix is the transpose",
                         ACCENT_A, FS_TAG, w=11.9))

 def _change_coords(self):
  """Two maps that look alike and are not. Drawing them as different shapes
  of diagram -- one a triangle through the space, one an arrow inside it --
  is the distinction the book warns about."""
  g = VGroup(self._box(-5.00, 1.00, "ℝⁿ", DIM, w=1.10, h=0.54),
             self._box(-5.00, -0.30, "ℝⁿ", DIM, w=1.10, h=0.54),
             self._box(-2.70, 0.35, "V", ACCENT_B, w=1.10, h=0.54),
             self._arr([-4.42, 1.00, 0], [-3.20, 0.60, 0], ACCENT_B, sw=2.5, tl=0.12),
             Text("φ", font_size=FS_TAG - 3, color=ACCENT_B).move_to([-3.75, 0.98, 0]),
             self._arr([-3.20, 0.10, 0], [-4.42, -0.30, 0], ACCENT_C, sw=2.5, tl=0.12),
             Text("θ ⁻¹", font_size=FS_TAG - 3, color=ACCENT_C).move_to([-3.70, -0.34, 0]),
             self._arr([-5.00, 0.71, 0], [-5.00, -0.01, 0], WARN, sw=2.5, tl=0.11),
             Text("A", font_size=FS_TAG - 3, color=WARN).move_to([-5.45, 0.35, 0]),
             Line([-1.30, -0.95, 0], [-1.30, 1.25, 0], color=DIM, stroke_width=1.6),
             self._box(1.60, 0.35, "V", ACCENT_B, w=1.10, h=0.54),
             self._box(4.30, 0.35, "V", ACCENT_B, w=1.10, h=0.54),
             self._arr([2.20, 0.35, 0], [3.70, 0.35, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG - 3, color=ACCENT_A).move_to([2.95, 0.64, 0]),
             self._mid(-0.15, "把 βᵢ 送到 βᵢ ′", "sends each basis vector to the new one",
                       ACCENT_A, FS_TAG, x=2.95, w=3.40))
  return g.add(self._mid(-0.98, "左邊那個把座標換成座標，住在座標空間上",
                         "the left one turns coordinates into coordinates, on the Cartesian space",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.40, "右邊那個把向量送到向量，住在 V 上——兩者長得很像，不是同一個",
                         "the right one sends vectors to vectors, on V; they look alike and differ",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "書上特地提醒不要搞混，因為兩者都寫成兩個基底同構的合成",
                         "the book warns about this: both are composites of two basis isomorphisms",
                         DIM, FS_TAG, w=11.9))

 def _diagram(self, paths=False):
  """The nine maps of the section, as three rows rather than the book's
  prism. `paths` marks the way around against the direct arrow, which is
  what beat 6 reads the identity off."""
  LX, RX = -3.60, 1.40
  YT, YM, YB = 0.94, 0.12, -0.70
  g = VGroup(self._box(LX, YT, "ℝⁿ", DIM, w=1.05, h=0.48, size=FS_TAG),
             self._box(RX, YT, "ℝᵐ", DIM, w=1.05, h=0.48, size=FS_TAG),
             self._box(LX, YM, "V", ACCENT_B, w=1.05, h=0.48, size=FS_TAG),
             self._box(RX, YM, "W", ACCENT_C, w=1.05, h=0.48, size=FS_TAG),
             self._box(LX, YB, "ℝⁿ", DIM, w=1.05, h=0.48, size=FS_TAG),
             self._box(RX, YB, "ℝᵐ", DIM, w=1.05, h=0.48, size=FS_TAG))
  rows = ((YT, "T ′", WARN if paths else ACCENT_A),
          (YM, "T", ACCENT_A),
          (YB, "T ″", ACCENT_B if paths else ACCENT_A))
  for y, lab, col in rows:
   g.add(self._arr([LX + 0.60, y, 0], [RX - 0.60, y, 0], col, sw=2.5, tl=0.12),
         Text(lab, font_size=FS_TAG - 3, color=col).move_to([(LX + RX) / 2, y + 0.24, 0]))
  for x, up, dn, lab in ((LX, "φ₁", "φ₂", "V"), (RX, "ψ₁", "ψ₂", "W")):
   g.add(self._arr([x, YT - 0.26, 0], [x, YM + 0.26, 0], ACCENT_B, sw=2, tl=0.10),
         Text(up, font_size=FS_TAG - 5, color=ACCENT_B).move_to([x + 0.42, YT - 0.42, 0]),
         self._arr([x, YB + 0.26, 0], [x, YM - 0.26, 0], ACCENT_C, sw=2, tl=0.10),
         Text(dn, font_size=FS_TAG - 5, color=ACCENT_C).move_to([x + 0.42, YB + 0.42, 0]))
  for x, off, lab, col in ((LX, -1.05, "A", WARN), (RX, 1.05, "B", WARN)):
   sx = x + off
   g.add(Line([x, YT, 0], [sx, YT, 0], color=col, stroke_width=2),
         self._arr([sx, YT, 0], [sx, YB, 0], col, sw=2, tl=0.11) if not paths
         else self._arr([sx, YB, 0], [sx, YT, 0], col, sw=2, tl=0.11),
         Line([sx, YB, 0], [x, YB, 0], color=col, stroke_width=2),
         Text(lab + (" ⁻¹" if paths and off < 0 else ""), font_size=FS_TAG - 4, color=col)
         .move_to([sx + (-0.42 if off < 0 else 0.42), (YT + YB) / 2, 0]))
  return g

 def _fig(self):
  return self._diagram().add(
   self._mid(0.94, "第一組基底", "the first pair of bases", DIM, FS_TAG, x=4.35, w=3.20),
   self._mid(-0.70, "第二組基底", "the second pair", DIM, FS_TAG, x=4.35, w=3.20),
   self._mid(-1.42, "上下兩層是座標空間，中間夾著抽象的 V 與 W，四個基底同構把它們接起來",
             "two storeys of Cartesian spaces, the abstract pair between, joined by four isos",
             ACCENT_B, FS_TAG, w=11.9),
   self._mid(-1.78, "兩側是換座標的映射。九個映射，彼此牽制",
             "the changes of coordinates stand at the sides: nine maps, all constraining each other",
             WARN, FS_TAG, w=11.9))

 def _read_off(self):
  return self._diagram(paths=True).add(
   self._mid(0.94, "繞這一圈", "the way around", WARN, FS_TAG, x=4.35, w=3.20),
   self._mid(-0.70, "與直接走這一條", "against the direct one", ACCENT_B, FS_TAG, x=4.35, w=3.20),
   self._box(0.00, -1.28, "t ″   =   b  t ′  a ⁻¹", WARN, w=4.20, h=0.52, size=FS_TAG),
   self._mid(-1.76, "照定義硬推也會得到它，但中間有一堆走過又折回的步驟",
             "the definitions give it too, with retraced steps the diagram removes",
             DIM, FS_TAG, w=11.9))

 def _two_cases(self):
  g = VGroup(self._box(-3.30, 1.00, "W  =  V", ACCENT_B, w=2.20, h=0.58, size=FS_TAG),
             self._arr([-3.30, 0.63, 0], [-3.30, 0.22, 0], DIM, sw=2, tl=0.10),
             self._box(-3.30, -0.15, "t ″   =   a  t ′  a ⁻¹", ACCENT_B, w=4.00, h=0.62,
                       size=FS_TAG),
             Line([0.30, -0.95, 0], [0.30, 1.25, 0], color=DIM, stroke_width=1.6),
             self._box(3.30, 1.00, "W  =  ℝ    ⇒    b  =  e", ACCENT_C, w=4.20, h=0.58,
                       size=FS_TAG - 1),
             self._arr([3.30, 0.63, 0], [3.30, 0.22, 0], DIM, sw=2, tl=0.10),
             self._box(3.30, -0.15, "f ″   =   ( a ⁻¹ ) *  f ′", ACCENT_C, w=4.00, h=0.62,
                       size=FS_TAG))
  return g.add(self._mid(-0.75, "只有一組基底要換，就是相似變換",
                         "one basis change only: a similarity",
                         ACCENT_B, FS_TAG, x=-3.30, w=4.60),
               self._mid(-0.75, "實數那一側沒有基底要換", "nothing changes on the real line",
                         ACCENT_C, FS_TAG, x=3.30, w=4.60),
               self._mid(-1.30, "所以泛函的座標乘的是換座標矩陣的反矩陣的轉置",
                         "so a functional's coordinates get the transpose of the inverse",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "而向量的座標乘的是那個矩陣本身——下一拍看這件事的名字",
                         "while a vector's coordinates get the matrix itself: next beat names this",
                         ACCENT_A, FS_TAG, w=11.9))

 def _co_contra(self):
  """One change matrix, two rules, and the rules use inverse matrices. That
  is the whole content of the two words, so it is drawn as one source
  branching into two rather than as two unrelated formulas."""
  g = VGroup(self._box(0.00, 0.98, "a", WARN, w=1.20, h=0.56),
             self._mid(0.98, "換基底", "one change of basis", WARN, FS_TAG, x=2.30, w=2.60),
             self._arr([-0.45, 0.71, 0], [-2.60, 0.30, 0], ACCENT_B, sw=2.5, tl=0.12),
             self._arr([0.45, 0.71, 0], [2.60, 0.30, 0], ACCENT_C, sw=2.5, tl=0.12),
             self._box(-3.30, 0.00, "x ″   =   a  x ′", ACCENT_B, w=3.00, h=0.62, size=FS_TAG),
             self._box(3.30, 0.00, "f ″   =   ( a ⁻¹ ) *  f ′", ACCENT_C, w=3.60, h=0.62,
                       size=FS_TAG),
             self._dash([-1.80, -0.32, 0], [1.50, -0.32, 0], DIM, n=16, sw=1.8),
             Text("( · ) ⁻¹", font_size=FS_TAG - 4, color=DIM).move_to([-0.15, -0.56, 0]))
  return g.add(self._mid(-0.90, "同一個換基底，兩條規則，用的矩陣互為反矩陣（還加一個轉置）",
                         "one change, two rules, and their matrices are inverse to each other",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.32, "V 裡的向量叫逆變，V 的對偶空間裡的泛函叫共變",
                         "vectors in V are called contravariant, functionals in its dual covariant",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "這兩個詞來自古典張量分析，在微分幾何裡會一直出現",
                         "the words come from classical tensor analysis and recur in geometry",
                         WARN, FS_TAG, w=11.9))

 def _dkl(self):
  """D_kl drawn by what it does: everything to zero except one basis vector,
  which goes to one basis vector. The indices come from KROW and JCOL, and
  the single 1 in the matrix is placed from the same pair."""
  g = VGroup(Text("V", font_size=FS_TAG, color=ACCENT_B).move_to([-5.15, 1.05, 0]),
             Text("W", font_size=FS_TAG, color=ACCENT_C).move_to([-1.05, 1.05, 0]))
  for j in range(N):
   y = 0.70 - j * 0.52
   hot = j == JCOL
   g.add(Dot([-5.15, y, 0], radius=0.06, color=WARN if hot else ACCENT_B),
         Text(f"β{JSUBS[j]}", font_size=FS_TAG - 4, color=WARN if hot else DIM)
         .move_to([-4.65, y, 0]))
  for i in range(M):
   y = 0.55 - i * 0.52
   hot = i == KROW
   g.add(Dot([-1.05, y, 0], radius=0.06, color=WARN if hot else ACCENT_C),
         Text(f"γ{ISUBS[i]}", font_size=FS_TAG - 4, color=WARN if hot else DIM)
         .move_to([-0.55, y, 0]))
  g.add(self._arr([-4.20, 0.70 - JCOL * 0.52, 0], [-1.55, 0.55 - KROW * 0.52, 0],
                  WARN, sw=2.5, tl=0.12))
  for j in range(N):
   if j == JCOL:
    continue
   g.add(Text("↦  0", font_size=FS_TAG - 4, color=DIM)
         .move_to([-3.70, 0.70 - j * 0.52, 0]))
  cell = lambda i, j: [2.60 + j * 0.55, 0.55 - i * 0.50, 0]
  for i in range(M):
   for j in range(N):
    hot = (i, j) == (KROW, JCOL)
    g.add(Text("1" if hot else "0", font_size=FS_TAG - 4, color=WARN if hot else DIM)
          .move_to(cell(i, j)))
  return g.add(self._brackets(2.60 - 0.34, 2.60 + (N - 1) * 0.55 + 0.34,
                              0.55 - (M - 1) * 0.50 - 0.22, 0.77),
               Text(f"δ {'ᵏˡ'}", font_size=FS_TAG - 2, color=WARN).move_to([3.15, -0.55, 0]),
               self._mid(-1.05, "第 k l 個基底：把第 l 個基底向量送到第 k 個，其餘全送到零",
                         "the k l th one sends the l th basis vector to the k th and the rest to zero",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.44, "對應的矩陣只有一格是一，其他全是零——那正是矩陣空間的標準基底",
                         "its matrix has a single 1: exactly the standard basis of the matrix space",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "同構把矩陣的標準基底搬成 Hom 的標準基底",
                         "the isomorphism carries one standard basis onto the other",
                         DIM, FS_TAG, w=11.9))

 def _expansion(self):
  g = VGroup(self._box(-3.10, 0.96, "T ( ξ )  =  Σ ᵢⱼ t ᵢⱼ D ᵢⱼ ( ξ )", ACCENT_A,
                       w=5.20, h=0.62, size=FS_TAG),
             self._arr([-3.10, 0.59, 0], [-3.10, 0.22, 0], DIM, sw=2, tl=0.10),
             self._box(-3.10, -0.15, "T   =   Σ ᵢⱼ t ᵢⱼ D ᵢⱼ", WARN, w=4.20, h=0.62,
                       size=FS_TAG),
             Line([0.40, -0.95, 0], [0.40, 1.25, 0], color=DIM, stroke_width=1.6),
             self._box(3.40, 0.96, "W  =  ℝ", ACCENT_C, w=2.00, h=0.56, size=FS_TAG),
             self._arr([3.40, 0.62, 0], [3.40, 0.22, 0], DIM, sw=2, tl=0.10),
             self._box(3.40, -0.15, "D ₗ   =   ε ₗ", ACCENT_C, w=2.60, h=0.62, size=FS_TAG))
  return g.add(self._mid(-0.72, "係數自己跑出來，就是矩陣元素",
                         "the coefficients come out as the matrix entries",
                         WARN, FS_TAG, x=-3.10, w=5.20),
               self._mid(-0.72, "對偶基底是特例", "the dual basis is a special case",
                         ACCENT_C, FS_TAG, x=3.40, w=3.20),
               self._mid(-1.32, "所以矩陣元素從頭到尾都是「T 在這組基底下的座標」",
                         "so the entries were the coordinates of T in this basis all along",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "第 2 章第 4 節到此結束，下一集講跡與行列式",
                         "that ends section four; next time, trace and determinant",
                         DIM, FS_TAG, w=11.6))

 def stage(self):
  tr, lm, fr = self._two_readings(), self._left_mult(), self._functional_row()
  ar, cc, fg = self._adjoint_right(), self._change_coords(), self._fig()
  ro, tc, co = self._read_off(), self._two_cases(), self._co_contra()
  dk, ex = self._dkl(), self._expansion()
  return [([tr], []), ([lm], [tr]), ([fr], [lm]), ([ar], [fr]),
          ([cc], [ar]), ([fg], [cc]), ([ro], [fg]), ([tc], [ro]),
          ([co], [tc]), ([dk], [co]), ([ex], [dk])]


AdvCalcE25ZH, AdvCalcE25EN = make(AdvCalcE25Base, "25", prefix="AdvCalcE")
