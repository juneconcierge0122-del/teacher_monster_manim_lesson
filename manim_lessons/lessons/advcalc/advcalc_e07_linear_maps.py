"""advcalc E07 — Chapter 1, section 1, third part (book pp. 29-32): linear
transformations, Theorem 1.2 and the skeleton.

The section's argument is a loop: a linear map out of coordinate n-space is
built from an n-tuple, and the n-tuple is read back off the map by feeding it
the unit vectors. Beats 6 to 9 draw that loop, because it is the one thing the
formula bar states but cannot show -- both directions of a bijection.

Beat 1 is the other place a picture earns its keep: that the integral respects
sums but not products is an area fact, so it is drawn as areas rather than
asserted again in symbols.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17


class AdvCalcE07Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 7

 MODE_LABEL = {
  0: {"zh": "三個運算，還是兩個？", "en": "three operations, or two?"},
  1: {"zh": "積分保持和，不保持積", "en": "the integral keeps sums, not products"},
  2: {"zh": "線性方程組就是這種映射", "en": "a linear system is such a map"},
  3: {"zh": "線性變換的定義", "en": "the definition of a linear transformation"},
  4: {"zh": "推廣到任意有限和", "en": "extended to any finite sum"},
  5: {"zh": "以座標空間為定義域", "en": "with coordinate space as domain"},
  6: {"zh": "餵單位向量，讀回 skeleton", "en": "feed the unit vectors, read the skeleton"},
  7: {"zh": "定理：兩個方向都成立", "en": "the theorem: both directions hold"},
  8: {"zh": "只有第 j 項活下來", "en": "only the jth term survives"},
  9: {"zh": "n 元組與線性映射是一對一的", "en": "n-tuples and linear maps correspond"},
  10: {"zh": "上域是實數線的特例", "en": "the case of the real line"},
 }

 # ── beat 0: which operations survive ─────────────────────────────
 def _ops(self):
  g = VGroup()
  panels = ((-3.15, "函數空間", "a function space", ACCENT_B,
             (("f + g", True), ("x f", True), ("f g", False))),
            (3.15, "向量空間", "a vector space", ACCENT_A,
             (("α + β", True), ("x α", True), (None, None))))
  for cx, zh, en, col, rows in panels:
   g.add(Rectangle(width=4.10, height=2.35, color=col, stroke_width=2.5).move_to([cx, 0.05, 0]),
         self._mid(1.05, zh, en, col, FS_TAG, x=cx, w=3.8))
   for k, (s, keep) in enumerate(rows):
    if s is None:
     continue
    y = 0.68 - k * 0.62
    g.add(Text(s, font_size=FS_TAG + 3, color=INK if keep else WARN).move_to([cx - 0.85, y, 0]))
    if not keep:
     g.add(Line([cx - 1.35, y - 0.20, 0], [cx - 0.35, y + 0.20, 0], color=WARN, stroke_width=3),
           self._mid(y, "被丟掉", "dropped", WARN, FS_TAG, x=cx + 0.95, w=2.0))
  return g.add(self._mid(-1.55, "為什麼不研究三個運算都有的結構？",
                         "why not study the structure with all three operations?",
                         DIM, FS_TAG, w=11.4))

 # ── beat 1: the integral, as areas ───────────────────────────────
 def _integral(self):
  """f and g shaded under their graphs, then the sum; the product beside it
  with a cross, because its area is not the product of the two areas."""
  g = VGroup()
  ts = np.linspace(0, 1, 60)
  def panel(cx, fn, col, lab_zh, lab_en):
   base, w, h = -0.95, 2.10, 1.45
   pts = [[cx - w / 2 + t * w, base + h * fn(t), 0] for t in ts]
   poly = Polygon(*([[cx - w / 2, base, 0]] + pts + [[cx + w / 2, base, 0]]),
                  color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.25)
   return VGroup(poly, Line([cx - w / 2, base, 0], [cx + w / 2, base, 0],
                            color=GHOST, stroke_width=2),
                 self._mid(0.95, lab_zh, lab_en, col, FS_TAG, x=cx, w=2.2))
  f = lambda t: 0.30 + 0.55 * np.sin(np.pi * t)
  gg = lambda t: 0.22 + 0.42 * t
  g.add(panel(-4.55, f, ACCENT_B, "f", "f"),
        Text("+", font_size=FS_TAG + 6, color=DIM).move_to([-3.30, -0.30, 0]),
        panel(-2.05, gg, ACCENT_C, "g", "g"),
        Text("=", font_size=FS_TAG + 6, color=DIM).move_to([-0.80, -0.30, 0]),
        panel(0.45, lambda t: f(t) + gg(t), ACCENT_A, "f + g", "f + g"))
  g.add(panel(3.75, lambda t: f(t) * gg(t) * 1.9, WARN, "f g", "f g"),
        Line([2.55, -1.05, 0], [4.95, 0.75, 0], color=WARN, stroke_width=4))
  return g.add(self._mid(-1.55, "左邊的面積加得起來，右邊的乘不起來",
                         "the areas on the left add; the one on the right does not multiply",
                         DIM, FS_TAG, w=11.4))

 def _system(self):
  """Three inputs feeding two outputs, which is all a linear system is."""
  ax, bx = -2.30, 1.50
  ys_in = (0.72, 0.02, -0.68)
  ys_out = (0.42, -0.38)
  g = VGroup()
  for k, y in enumerate(ys_in):
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Text(f"x{k + 1}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([ax - 0.52, y, 0]))
  for k, y in enumerate(ys_out):
   g.add(Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         Text(f"y{k + 1}", font_size=FS_TAG - 2, color=ACCENT_A).move_to([bx + 0.52, y, 0]))
  for yi in ys_in:
   for yo in ys_out:
    g.add(Line([ax + 0.14, yi, 0], [bx - 0.14, yo, 0], color=DIM, stroke_width=1.6))
  return g.add(self._mid(0.95, "每個輸出是輸入的一次組合",
                         "each output a first-degree combination of the inputs",
                         DIM, FS_TAG, x=4.05, w=4.2),
               self._mid(-0.05, "所以線性方程組能不能解", "so whether a system can be solved",
                         DIM, FS_TAG, x=4.05, w=4.2),
               self._mid(-0.75, "就是這種映射的理論", "is the theory of such maps",
                         ACCENT_A, FS_TAG, x=4.05, w=4.2),
               self._mid(-1.55, "研究向量空間，有一部分是為了研究保持運算的映射",
                         "we study vector spaces partly to study the maps preserving them",
                         DIM, FS_TAG, w=11.4))

 # ── beat 3: linearity as a parallelogram carried across ──────────
 UV = (np.array([1.05, 0.30, 0.0]), np.array([0.32, 1.00, 0.0]))

 def _pgram(self, o, u, v, cols, sw=3):
  g = VGroup(self._arr(o, o + u, cols[0], sw=sw, tl=0.14),
             self._arr(o, o + v, cols[1], sw=sw, tl=0.14),
             self._arr(o, o + u + v, cols[2], sw=sw + 1, tl=0.18),
             self._dash(o + u, o + u + v, GHOST, n=7),
             self._dash(o + v, o + u + v, GHOST, n=7),
             Dot(o, radius=0.055, color=INK))
  return g

 def _linear_def(self):
  """The same parallelogram on both sides: T carries the whole figure."""
  u, v = self.UV
  o1, o2 = np.array([-4.55, -0.75, 0.0]), np.array([1.35, -0.75, 0.0])
  # the image parallelogram is a genuinely different shape, so that the point
  # reads as "the structure survives", not "nothing happened"
  M = np.array([[0.86, 0.46, 0], [-0.34, 0.78, 0], [0, 0, 1]])
  g = VGroup(self._pgram(o1, u, v, (ACCENT_B, ACCENT_C, ACCENT_A)),
             self._pgram(o2, M @ u, M @ v, (ACCENT_B, ACCENT_C, ACCENT_A)),
             self._arr([-1.85, -0.10, 0], [0.55, -0.10, 0], ACCENT_A, sw=3, tl=0.16),
             Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([-0.65, 0.20, 0]),
             self._mid(1.05, "V", "V", DIM, FS_TAG, x=-3.60, w=1.2),
             self._mid(1.05, "W", "W", DIM, FS_TAG, x=2.30, w=1.2))
  return g.add(self._mid(-1.55, "和送到和、倍數送到倍數 —— 整個平行四邊形被搬過去",
                         "sums to sums and multiples to multiples: the whole figure carries over",
                         ACCENT_A, FS_TAG, w=11.6))

 def _finite_sum(self):
  """Four scaled vectors and their sum, each arrow matched on the far side."""
  o1, o2 = np.array([-4.45, -0.55, 0.0]), np.array([1.15, -0.55, 0.0])
  vs = (np.array([0.78, 0.52, 0]), np.array([0.90, -0.16, 0]), np.array([0.42, 0.86, 0]))
  M = np.array([[0.80, 0.40, 0], [-0.30, 0.84, 0], [0, 0, 1]])
  g = VGroup()
  for o, mat in ((o1, np.eye(3)), (o2, M)):
   p = o
   for k, v in enumerate(vs):
    q = p + mat @ v
    g.add(self._arr(p, q, (ACCENT_B, ACCENT_C, DIM)[k], sw=2.5, tl=0.12))
    p = q
   g.add(self._arr(o, p, ACCENT_A, sw=4, tl=0.18), Dot(o, radius=0.055, color=INK))
  g.add(self._arr([-1.75, -0.10, 0], [0.35, -0.10, 0], ACCENT_A, sw=3, tl=0.16),
        Text("T", font_size=FS_TAG + 3, color=ACCENT_A).move_to([-0.70, 0.20, 0]))
  return g.add(self._mid(1.05, "係數一模一樣", "the coefficients are unchanged",
                         ACCENT_A, FS_TAG, w=11.0),
               self._mid(-1.55, "積分的那個性質，正是這個式子的特例",
                         "the property of the integral is a special case of this",
                         DIM, FS_TAG, w=11.4))

 # ── beats 5-9: the skeleton loop ─────────────────────────────────
 def _curves(self, cx, base, w, h, weights=None):
  ts = np.linspace(-1, 1, 70)
  fns = (np.sin, np.cos, lambda z: np.exp(0.5 * z) - 1.0)
  cols = (ACCENT_B, ACCENT_C, DIM)
  g = VGroup(Line([cx - w / 2, base, 0], [cx + w / 2, base, 0], color=GHOST, stroke_width=2))
  if weights is None:
   for fn, col in zip(fns, cols):
    g.add(self._curve([[cx + t * w / 2, base + h * fn(2.0 * t), 0] for t in ts], col, sw=2.5))
  else:
   f = lambda z: sum(c * fn(z) for c, fn in zip(weights, fns))
   g.add(self._curve([[cx + t * w / 2, base + h * 0.55 * f(2.0 * t), 0] for t in ts],
                     ACCENT_A, sw=4))
  return g

 def _example(self):
  g = VGroup(self._curves(-3.55, -0.30, 3.10, 0.62),
             self._mid(1.05, "固定三個函數", "fix three functions", DIM, FS_TAG, x=-3.55, w=3.2),
             self._arr([-1.75, -0.30, 0], [-0.15, -0.30, 0], ACCENT_A, sw=3, tl=0.15),
             Text("⟨ x₁ , x₂ , x₃ ⟩", font_size=FS_TAG, color=ACCENT_A)
             .move_to([-0.95, 0.10, 0]),
             self._curves(2.35, -0.30, 3.10, 0.62, weights=(1.4, -0.6, 1.1)),
             self._mid(1.05, "加權和是一條新曲線", "the weighted sum is a new function",
                       ACCENT_A, FS_TAG, x=2.35, w=3.6))
  return g.add(self._mid(-1.55, "這個從三元組到函數的對應，顯然是線性的",
                         "this map from triples to functions is plainly linear",
                         DIM, FS_TAG, w=11.4))

 def _skeleton(self):
  """Feed each unit vector in and the corresponding function drops out."""
  g = VGroup()
  ox = -4.35
  names = ("δ¹", "δ²", "δ³")
  outs = ("f₁", "f₂", "f₃")
  cols = (ACCENT_B, ACCENT_C, DIM)
  for k in range(3):
   y = 0.80 - k * 0.72
   g.add(Rectangle(width=1.05, height=0.50, color=cols[k], stroke_width=2)
         .move_to([ox, y, 0]),
         Text(names[k], font_size=FS_TAG, color=cols[k]).move_to([ox, y, 0]),
         self._arr([ox + 0.62, y, 0], [ox + 1.85, y, 0], DIM, sw=2.2, tl=0.11),
         Text("T", font_size=FS_TAG - 2, color=ACCENT_A).move_to([ox + 1.24, y + 0.26, 0]),
         Rectangle(width=1.05, height=0.50, color=cols[k], stroke_width=2)
         .move_to([ox + 2.45, y, 0]),
         Text(outs[k], font_size=FS_TAG, color=cols[k]).move_to([ox + 2.45, y, 0]))
  # the enclosing box only has to reach the three inner boxes (y = 0.80 down to
  # -0.64, half-height 0.25), and at 2.50 tall it ran into the formula bar
  g.add(Rectangle(width=1.55, height=2.20, color=ACCENT_A, stroke_width=2.5)
        .move_to([ox + 2.45, 0.08, 0]))
  return g.add(self._mid(0.85, "把只有一個位置是一的向量餵進去",
                         "feed in the vector with a single one",
                         DIM, FS_TAG, x=2.55, w=5.0),
               self._mid(0.10, "出來的就是第 j 個函數", "and the jth function comes out",
                         DIM, FS_TAG, x=2.55, w=5.0),
               self._mid(-0.65, "這一組像叫做 T 的 skeleton", "that n-tuple is the skeleton of T",
                         ACCENT_A, FS_TAG, x=2.55, w=5.0),
               self._mid(-1.55, "映射造出來之後，材料還讀得回來",
                         "the map is built from the tuple, and gives it back",
                         DIM, FS_TAG, w=11.4))

 def _theorem(self):
  """The loop drawn as a loop: a tuple builds a map, the map returns the
  tuple. Two arrows, not one, because the theorem has two halves."""
  lx, rx, cy = -2.55, 2.55, 0.20
  g = VGroup(Rectangle(width=2.90, height=1.05, color=ACCENT_B, stroke_width=2.5)
             .move_to([lx, cy, 0]),
             self._mid(cy, "W 裡的 n 元組", "an n-tuple in W", ACCENT_B, FS_TAG, x=lx, w=2.6),
             Rectangle(width=2.90, height=1.05, color=ACCENT_A, stroke_width=2.5)
             .move_to([rx, cy, 0]),
             self._mid(cy, "一個線性映射", "a linear map", ACCENT_A, FS_TAG, x=rx, w=2.6),
             self._arr([lx + 1.50, cy + 0.30, 0], [rx - 1.50, cy + 0.30, 0],
                       ACCENT_A, sw=3, tl=0.15),
             self._arr([rx - 1.50, cy - 0.30, 0], [lx + 1.50, cy - 0.30, 0],
                       ACCENT_B, sw=3, tl=0.15),
             self._mid(cy + 0.68, "做線性組合映射", "form the combination map",
                       ACCENT_A, FS_TAG, w=4.4),
             self._mid(cy - 0.68, "取 skeleton", "take the skeleton", ACCENT_B, FS_TAG, w=4.4))
  return g.add(self._mid(-1.20, "來回一圈就回到原地 —— 兩個方向都要證",
                         "the round trip returns where it began: both halves need proving",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.72, "定理的兩半，正好就是這兩支箭頭",
                         "the two halves of the theorem are these two arrows",
                         DIM, FS_TAG, w=11.4))

 def _only_jth(self):
  """The coefficient row of the jth unit vector, with everything but one
  entry annihilated."""
  ox = -3.05
  g = VGroup()
  for k in range(4):
   x = ox + k * 1.15
   on = k == 1
   # the struck-out entries stay legible: GHOST is for background rules, and
   # at that value the zeros simply vanished
   g.add(Rectangle(width=0.72, height=0.50, color=ACCENT_A if on else DIM, stroke_width=2)
         .move_to([x, 0.72, 0]),
         Text("1" if on else "0", font_size=FS_TAG, color=ACCENT_A if on else DIM)
         .move_to([x, 0.72, 0]),
         Text("×", font_size=FS_TAG - 3, color=DIM).move_to([x, 0.28, 0]),
         Rectangle(width=0.72, height=0.50, color=ACCENT_B if on else DIM, stroke_width=2)
         .move_to([x, -0.16, 0]),
         Text(f"β{k + 1}", font_size=FS_TAG - 3, color=ACCENT_B if on else DIM)
         .move_to([x, -0.16, 0]))
   if not on:
    g.add(Line([x - 0.42, -0.42, 0], [x + 0.42, 0.10, 0], color=WARN, stroke_width=2.5))
  g.add(self._arr([ox + 1.15, -0.52, 0], [ox + 1.15, -1.00, 0], ACCENT_A, sw=2.5, tl=0.13),
        Text("β₂", font_size=FS_TAG + 2, color=ACCENT_A).move_to([ox + 1.15, -1.28, 0]))
  return g.add(self._mid(0.85, "餵進第 j 個單位向量", "feed in the jth unit vector",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.15, "其他項的係數都是零", "every other coefficient is zero",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "只有第 j 項活下來", "so only the jth term survives",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "反過來：任何向量都是單位向量的組合，套上 T 再用線性就回去了",
                         "conversely any vector is a combination of unit vectors; apply T and use linearity",
                         DIM, FS_TAG, w=11.8))

 def _bijection(self):
  """Two columns of dots joined one-to-one, the picture of a bijection."""
  ax, bx = -2.45, 1.65
  ys = (0.85, 0.30, -0.25, -0.80)
  g = VGroup(self._mid(1.10, "Wⁿ", "Wⁿ", ACCENT_B, FS_TAG, x=ax, w=2.0),
             self._mid(1.10, "所有線性映射", "all the linear maps", ACCENT_A, FS_TAG, x=bx, w=3.0))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  g.add(Text("⋮", font_size=FS_TAG + 4, color=GHOST).move_to([ax, -1.25, 0]),
        Text("⋮", font_size=FS_TAG + 4, color=GHOST).move_to([bx, -1.25, 0]))
  return g.add(self._mid(0.75, "一個 n 元組配一個映射", "one tuple, one map",
                         DIM, FS_TAG, x=4.35, w=3.5),
               self._mid(0.05, "沒有多的，也沒有少的", "none left over on either side",
                         DIM, FS_TAG, x=4.35, w=3.5),
               self._mid(-0.65, "兩邊的資訊量一樣", "the same information twice",
                         ACCENT_A, FS_TAG, x=4.35, w=3.5),
               self._mid(-1.62, "書上說這個定理極其重要，要讀者牢牢記住",
                         "the book calls this tremendously important and asks the reader to fix it in mind",
                         ACCENT_A, FS_TAG, w=11.8))

 def _real_case(self):
  """W collapses to the line, so each skeleton entry is one number."""
  g = VGroup()
  ox = -3.20
  for k in range(4):
   x = ox + k * 1.00
   g.add(Rectangle(width=0.70, height=0.50, color=ACCENT_B, stroke_width=2)
         .move_to([x, 0.62, 0]),
         Text(f"β{k + 1}", font_size=FS_TAG - 3, color=ACCENT_B).move_to([x, 0.62, 0]),
         self._arr([x, 0.30, 0], [x, -0.18, 0], DIM, sw=2, tl=0.10),
         Rectangle(width=0.70, height=0.50, color=ACCENT_A, stroke_width=2)
         .move_to([x, -0.46, 0]),
         Text(f"b{k + 1}", font_size=FS_TAG - 3, color=ACCENT_A).move_to([x, -0.46, 0]))
  g.add(self._mid(1.08, "W 是一般的向量空間", "W a general vector space",
                  ACCENT_B, FS_TAG, x=ox + 1.50, w=4.2),
        self._mid(-1.00, "W 是實數線：每一項只是一個數",
                  "W the real line: each entry is one number",
                  ACCENT_A, FS_TAG, x=ox + 1.50, w=4.6))
  return g.add(self._mid(0.55, "skeleton 變成一個數字 n 元組",
                         "the skeleton becomes an n-tuple of numbers",
                         ACCENT_A, FS_TAG, x=3.55, w=5.0),
               self._mid(-0.25, "這就是線性泛函", "and that is a linear functional",
                         DIM, FS_TAG, x=3.55, w=5.0),
               self._mid(-1.62, "下一集從這裡開始，一路做到矩陣",
                         "the next episode starts here and runs on to matrices",
                         DIM, FS_TAG, w=11.4))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  ops, itg, sys_ = self._ops(), self._integral(), self._system()
  ld, fs = self._linear_def(), self._finite_sum()
  ex, sk = self._example(), self._skeleton()
  th, oj = self._theorem(), self._only_jth()
  bi, rc = self._bijection(), self._real_case()

  return [([ops], []),                         # 0  two operations, not three
          ([itg], [ops]),                      # 1  the integral
          ([sys_], [itg]),                     # 2  a linear system
          ([ld], [sys_]),                      # 3  the definition
          ([fs], [ld]),                        # 4  any finite sum
          ([ex], [fs]),                        # 5  the concrete example
          ([sk], [ex]),                        # 6  the skeleton
          ([th], [sk]),                        # 7  Theorem 1.2 as a loop
          ([oj], [th]),                        # 8  only the jth term
          ([bi], [oj]),                        # 9  the bijection
          ([rc], [bi])]                        # 10 the real-line case


AdvCalcE07ZH, AdvCalcE07EN = make(AdvCalcE07Base, "07", prefix="AdvCalcE")
