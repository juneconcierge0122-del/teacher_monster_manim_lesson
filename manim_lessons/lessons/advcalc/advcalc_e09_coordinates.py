"""advcalc E09 — Chapter 1, section 2, first half (book pp. 36-39): the
coordinate correspondence, the four assumed geometric theorems, the scalar
product, and the equation of a line.

This is the first section of the book with real pictures in it, and the beats
follow its own figures: the axis box of Fig. 1.4, the two right triangles of
Fig. 1.5, the parallelogram of Fig. 1.6. Beats 5 to 8 are the four facts the
book declines to prove, so each is drawn as the geometric statement it is
rather than restated as the algebra already sitting in the formula bar.
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


class AdvCalcE09Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 9

 MODE_LABEL = {
  0: {"zh": "把座標系接回向量空間", "en": "coordinates, back onto vector spaces"},
  1: {"zh": "直線上的座標對應", "en": "the correspondence on a line"},
  2: {"zh": "原點與三個單位點", "en": "an origin and three unit points"},
  3: {"zh": "每個點決定一個三元組", "en": "each point determines a triple"},
  4: {"zh": "單位點對到單位向量", "en": "unit points go to unit vectors"},
  5: {"zh": "假設一：這是個雙射", "en": "assumption one: it is a bijection"},
  6: {"zh": "假設二：等價的有向線段", "en": "assumption two: equivalent directed segments"},
  7: {"zh": "假設三：同一條線上就是純量倍數",
      "en": "assumption three: on one line means a multiple"},
  8: {"zh": "假設四：畢氏定理給出長度", "en": "assumption four: Pythagoras gives the length"},
  9: {"zh": "垂直，就是純量積為零", "en": "perpendicular means the scalar product is zero"},
  10: {"zh": "直線的方程", "en": "the equation of a line"},
 }

 # ── beat 0 ────────────────────────────────────────────────────────
 def _bridge(self):
  g = VGroup()
  for cx, zh, en, col in ((-2.85, "幾何空間", "geometric space", ACCENT_B),
                          (2.85, "座標空間", "coordinate space", ACCENT_A)):
   g.add(Rectangle(width=3.60, height=1.15, color=col, stroke_width=2.5).move_to([cx, 0.45, 0]),
         self._mid(0.45, zh, en, col, FS_TAG, x=cx, w=3.3))
  g.add(self._arr([-1.00, 0.62, 0], [1.00, 0.62, 0], ACCENT_A, sw=3, tl=0.15),
        self._arr([1.00, 0.28, 0], [-1.00, 0.28, 0], ACCENT_B, sw=3, tl=0.15),
        self._mid(-0.60, "座標讓我們用向量的語言談直線與平面",
                  "coordinates let us treat lines and planes in vector terms",
                  DIM, FS_TAG, w=11.0),
        self._mid(-1.20, "而幾何直觀反過來幫我們理解向量空間",
                  "and the geometry repays us in intuition about vector spaces",
                  DIM, FS_TAG, w=11.0))
  return g.add(self._mid(-1.75, "所以先複習座標對應是怎麼建立的",
                         "so we begin by reviewing how the correspondence is set up",
                         ACCENT_A, FS_TAG, w=11.0))

 def _line_coord(self):
  """A zero point, a unit point, and the numbers that follow."""
  o = np.array([-2.60, -0.10, 0.0])
  d = np.array([1.42, 0.30, 0.0])
  g = VGroup(Line(o - 1.05 * d, o + 2.45 * d, color=GHOST, stroke_width=2.5))
  for f, s, col in ((0.0, "O", INK), (1.0, "Q", ACCENT_B),
                    (2.0, "2", ACCENT_A), (-0.7, "−0.7", WARN)):
   pt = o + f * d
   g.add(Dot(pt, radius=0.075, color=col),
         Text(s, font_size=FS_TAG, color=col).move_to(pt + np.array([0.0, 0.32, 0])))
  g.add(self._arr(o + np.array([0, -0.34, 0]), o + d + np.array([0, -0.34, 0]),
                  ACCENT_B, sw=2.2, tl=0.11),
        self._mid(-0.85, "這一段當作單位", "this segment is the unit",
                  ACCENT_B, FS_TAG, x=-1.90, w=3.4))
  return g.add(self._mid(0.95, "大小是到零點的距離", "size is the distance from the zero point",
                         DIM, FS_TAG, x=3.55, w=5.0),
               self._mid(0.15, "正負看在零點的哪一側", "sign says which side it lies on",
                         DIM, FS_TAG, x=3.55, w=5.0),
               self._mid(-1.62, "三維的作法完全一樣，只是要三條這樣的線",
                         "three dimensions go the same way, with three such lines",
                         DIM, FS_TAG, w=11.4))

 # ── the axis system ───────────────────────────────────────────────
 # Sized against the projection: EZ is straight up, so the third axis arrow
 # plus its label is what decides the clearance, not the box as a whole.
 ORG = np.array([-2.15, -0.90, 0.0])
 S = 0.95
 AXV = (np.array([1.55, 0, 0]), np.array([0, 1.55, 0]), np.array([0, 0, 1.30]))

 def _axes3(self, with_units=True):
  o = _p(np.zeros(3), self.ORG, self.S)
  g = VGroup(Dot(o, radius=0.065, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.20, 0])))
  cols = (ACCENT_B, ACCENT_C, ACCENT_A)
  for k, v in enumerate(self.AXV):
   tip = _p(1.30 * v, self.ORG, self.S)
   g.add(self._arr(o, tip, cols[k], sw=2.5, tl=0.13),
         Text(f"L{k + 1}", font_size=FS_TAG - 3, color=cols[k])
         .move_to(tip + np.array([0.22, 0.16, 0])))
   if with_units:
    q = _p(v, self.ORG, self.S)
    g.add(Dot(q, radius=0.075, color=cols[k]),
          Text(f"Q{k + 1}", font_size=FS_TAG - 3, color=cols[k])
          .move_to(q + np.array([-0.06, 0.28, 0])))
  return g

 def _axis_system(self):
  return self._axes3().add(
   self._mid(1.05, "任選一個原點", "choose an origin", DIM, FS_TAG, x=3.30, w=5.2),
   self._mid(0.30, "與三個單位點，四點不共面",
             "and three unit points, the four not in a plane", DIM, FS_TAG, x=3.30, w=5.2),
   self._mid(-0.45, "三條線就是座標軸", "the three lines are the coordinate axes",
             ACCENT_A, FS_TAG, x=3.30, w=5.2),
   self._mid(-1.62, "每條軸上都已經有了剛才那種座標對應",
             "each axis already carries a correspondence of the kind just described",
             DIM, FS_TAG, w=11.4))

 XP = np.array([0.95, 1.05, 0.85])

 def _triple(self):
  """Book Fig. 1.4: X projected onto each axis by the plane parallel to the
  other two."""
  g = self._axes3(with_units=False)
  X = _p(self.XP, self.ORG, self.S)
  g.add(Dot(X, radius=0.085, color=WARN),
        Text("X", font_size=FS_TAG, color=WARN).move_to(X + np.array([0.24, 0.18, 0])))
  for k in range(3):
   e = np.zeros(3); e[k] = self.XP[k]
   foot = _p(e, self.ORG, self.S)
   g.add(Dot(foot, radius=0.07, color=(ACCENT_B, ACCENT_C, ACCENT_A)[k]),
         Text(f"x{k + 1}", font_size=FS_TAG - 3, color=(ACCENT_B, ACCENT_C, ACCENT_A)[k])
         .move_to(foot + np.array([0.02, -0.30, 0]) if k != 2
                  else foot + np.array([-0.30, 0.06, 0])),
         self._dash(foot, X, GHOST, n=9))
  return g.add(self._mid(1.05, "過 X 平行於另外兩軸的平面",
                         "the plane through X parallel to the other two axes",
                         DIM, FS_TAG, x=3.50, w=5.0),
               self._mid(0.30, "交這一軸於一點", "meets this axis in a point",
                         DIM, FS_TAG, x=3.50, w=5.0),
               self._mid(-0.45, "三個座標一起組成一個三元組",
                         "the three coordinates make a triple",
                         ACCENT_A, FS_TAG, x=3.50, w=5.0),
               self._mid(-1.62, "這個對應就叫這組軸系定義的座標對應",
                         "that is the correspondence defined by the axis system",
                         DIM, FS_TAG, w=11.4))

 def _units(self):
  g = self._axes3()
  cols = (ACCENT_B, ACCENT_C, ACCENT_A)
  # The triples are listed in a column on the right, not set beside their own
  # axis tips: placed there they ran into the Q and L labels already sitting on
  # each tip, and into each other where two tips project close together.
  for k in range(3):
   tup = ["0", "0", "0"]; tup[k] = "1"
   y = 0.80 - k * 0.62
   g.add(Text(f"Q{k + 1}", font_size=FS_TAG - 1, color=cols[k]).move_to([1.95, y, 0]),
         self._arr([2.28, y, 0], [2.88, y, 0], DIM, sw=2, tl=0.10),
         Text("⟨ " + " , ".join(tup) + " ⟩", font_size=FS_TAG - 1, color=cols[k])
         .move_to([3.75, y, 0]))
  return g.add(self._mid(-0.95, "三個單位點的座標三元組，正好是那三個單位向量",
                         "the triples of the unit points are exactly the unit vectors",
                         ACCENT_A, FS_TAG, x=2.85, w=5.8),
               self._mid(-1.62, "這一點等一下會反覆用到",
                         "that fact gets used again and again shortly",
                         DIM, FS_TAG, w=11.4))

 # ── the four assumptions ──────────────────────────────────────────
 def _assume1(self):
  ax, bx = -2.35, 1.75
  ys = (0.80, 0.24, -0.32, -0.88)
  g = VGroup(self._mid(1.12, "幾何空間的點", "the points of space", ACCENT_B, FS_TAG, x=ax, w=3.4),
             self._mid(1.12, "三元組", "the triples", ACCENT_A, FS_TAG, x=bx, w=3.4))
  for y in ys:
   g.add(Dot([ax, y, 0], radius=0.075, color=ACCENT_B),
         Dot([bx, y, 0], radius=0.075, color=ACCENT_A),
         self._arr([ax + 0.16, y, 0], [bx - 0.16, y, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.65, "一個點配一個三元組", "one point, one triple",
                         DIM, FS_TAG, x=4.45, w=3.3),
               self._mid(-0.35, "兩邊都不多不少", "nothing left over either side",
                         ACCENT_A, FS_TAG, x=4.45, w=3.3),
               self._mid(-1.62, "嚴格說這要當幾何定理證，但書上說那些證明相當棘手，直接假設",
                         "strictly this needs proof, but the book calls it tricky and assumes it",
                         DIM, FS_TAG, w=11.8))

 def _assume2(self):
  """Two directed segments that are equal in length, parallel and similarly
  directed, with the coordinate differences drawn as the same arrow."""
  d = np.array([1.45, 0.62, 0.0])
  g = VGroup()
  for base, la, lb, col in ((np.array([-3.85, 0.30, 0.0]), "A", "B", ACCENT_B),
                            (np.array([-0.95, -0.95, 0.0]), "X", "Y", ACCENT_C)):
   g.add(self._arr(base, base + d, col, sw=3.5, tl=0.16),
         Dot(base, radius=0.065, color=col), Dot(base + d, radius=0.065, color=col),
         Text(la, font_size=FS_TAG, color=col).move_to(base + np.array([-0.10, -0.30, 0])),
         Text(lb, font_size=FS_TAG, color=col).move_to(base + d + np.array([0.18, 0.22, 0])))
  g.add(self._mid(-1.62, "等長、平行、方向相同 —— 就說這兩條有向線段等價",
                  "equal in length, parallel, similarly directed: the two are equivalent",
                  ACCENT_A, FS_TAG, w=11.6))
  return g.add(self._mid(1.05, "終點座標減起點座標", "endpoint minus starting coordinates",
                         DIM, FS_TAG, x=3.55, w=4.9),
               self._mid(0.10, "兩條算出來一樣", "comes out the same for both",
                         ACCENT_A, FS_TAG, x=3.55, w=4.9))

 def _assume3(self):
  o = np.array([-2.40, -0.55, 0.0])
  d = np.array([1.30, 0.72, 0.0])
  g = VGroup(Line(o - 0.75 * d, o + 2.35 * d, color=GHOST, stroke_width=2),
             Dot(o, radius=0.065, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.18, 0])))
  for f, s, col in ((1.0, "X", ACCENT_B), (1.9, "Y", ACCENT_A), (-0.55, "Z", WARN)):
   pt = o + f * d
   g.add(self._arr(o, pt, col, sw=3, tl=0.14), Dot(pt, radius=0.075, color=col),
         Text(s, font_size=FS_TAG, color=col).move_to(pt + np.array([0.20, 0.22, 0])))
  return g.add(self._mid(1.05, "Y 在過 O 與 X 的線上", "Y lies on the line through O and X",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(0.25, "若且唯若它的座標是 X 的倍數",
                         "exactly when its coordinates are a multiple of X's",
                         ACCENT_A, FS_TAG, x=3.35, w=5.2),
               self._mid(-0.55, "而那個倍數就是 Y 的座標", "and that multiple is Y's coordinate",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(-1.62, "這時是把 X 當作這條線上的單位點",
                         "taking X as the unit point on that line",
                         DIM, FS_TAG, w=11.4))

 def _pythagoras(self):
  """Book Fig. 1.5, left: the two right triangles that give the norm."""
  o = np.array([-2.90, -1.25, 0.0])
  a = np.array([1.75, 0.0, 0.0])
  b = np.array([0.48, 0.80, 0.0])
  c = np.array([0.0, 1.30, 0.0])
  Y = o + a + b
  X = Y + c
  g = VGroup(self._arr(o, o + a * 1.25, DIM, sw=2, tl=0.11),
             self._arr(o, o + b * 1.7, DIM, sw=2, tl=0.11),
             self._arr(o, o + c * 1.15, DIM, sw=2, tl=0.11),
             Polygon(o, o + a, Y, color=ACCENT_B, stroke_width=2,
                     fill_color=ACCENT_B, fill_opacity=0.16),
             Line(o, Y, color=ACCENT_B, stroke_width=3),
             Line(Y, X, color=ACCENT_C, stroke_width=3),
             self._arr(o, X, ACCENT_A, sw=4, tl=0.18),
             Dot(o, radius=0.06, color=INK), Dot(X, radius=0.075, color=WARN),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.18, 0])),
             Text("X", font_size=FS_TAG, color=WARN).move_to(X + np.array([0.22, 0.16, 0])),
             Text("s", font_size=FS_TAG - 3, color=ACCENT_B)
             .move_to(o + 0.55 * (a + b) + np.array([0.10, -0.24, 0])),
             Text("r", font_size=FS_TAG - 3, color=ACCENT_A)
             .move_to(o + 0.55 * (a + b + c) + np.array([-0.28, 0.06, 0])))
  return g.add(self._mid(1.05, "先在底面用一次畢氏定理", "Pythagoras once in the base plane",
                         ACCENT_B, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "再在直立的三角形用一次", "and once in the upright triangle",
                         ACCENT_C, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "長度就是各座標平方和開根號",
                         "the length is the root of the sum of squares",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.68, "這一條要求三軸互相垂直、共用同一個長度單位",
                         "this one asks that the axes be perpendicular with a common unit",
                         DIM, FS_TAG, w=11.6))

 def _perp(self):
  """Book Fig. 1.5, right: Pythagoras on triangle OXY."""
  o = np.array([-3.05, -0.35, 0.0])
  x = o + np.array([1.35, 1.20, 0.0])
  y = o + np.array([1.75, -0.95, 0.0])
  n1 = (x - o) / float(np.linalg.norm(x - o))
  n2 = (y - o) / float(np.linalg.norm(y - o))
  g = VGroup(Line(o, x, color=ACCENT_B, stroke_width=3),
             Line(o, y, color=ACCENT_C, stroke_width=3),
             Line(x, y, color=ACCENT_A, stroke_width=3),
             Polygon(o, o + 0.34 * n1, o + 0.34 * (n1 + n2), o + 0.34 * n2,
                     color=WARN, stroke_width=2),
             Dot(o, radius=0.06, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.26, -0.14, 0])),
             Text("X", font_size=FS_TAG, color=ACCENT_B).move_to(x + np.array([0.06, 0.28, 0])),
             Text("Y", font_size=FS_TAG, color=ACCENT_C).move_to(y + np.array([0.24, -0.16, 0])))
  return g.add(self._mid(1.05, "把畢氏定理再用一次到這個三角形",
                         "apply Pythagoras once more to this triangle",
                         DIM, FS_TAG, x=3.05, w=5.6),
               self._mid(0.20, "就得到：這個角是直角",
                         "and out comes: this angle is a right angle",
                         WARN, FS_TAG, x=3.05, w=5.6),
               self._mid(-0.65, "若且唯若純量積等於零", "exactly when the scalar product is zero",
                         ACCENT_A, FS_TAG, x=3.05, w=5.6),
               self._mid(-1.62, "純量積就是對應座標相乘再加起來",
                         "the scalar product is corresponding coordinates multiplied and summed",
                         DIM, FS_TAG, w=11.6))

 def _line_eq(self):
  """Book Fig. 1.6: the line through B parallel to OA."""
  o = np.array([-2.95, -0.75, 0.0])
  a = np.array([1.05, 1.30, 0.0])
  b = np.array([1.95, -0.10, 0.0])
  g = VGroup(Line(o + b - 0.75 * a, o + b + 1.55 * a, color=ACCENT_A, stroke_width=3),
             self._arr(o, o + a, ACCENT_B, sw=3.5, tl=0.16),
             self._arr(o, o + b, ACCENT_C, sw=3.5, tl=0.16),
             self._arr(o + b, o + b + 0.95 * a, ACCENT_B, sw=2.5, tl=0.13),
             Dot(o, radius=0.06, color=INK),
             Dot(o + b, radius=0.075, color=ACCENT_C),
             Dot(o + b + 0.95 * a, radius=0.075, color=WARN),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.18, 0])),
             Text("A", font_size=FS_TAG, color=ACCENT_B)
             .move_to(o + a + np.array([-0.24, 0.18, 0])),
             Text("B", font_size=FS_TAG, color=ACCENT_C)
             .move_to(o + b + np.array([0.10, -0.30, 0])),
             Text("X", font_size=FS_TAG, color=WARN)
             .move_to(o + b + 0.95 * a + np.array([0.26, 0.14, 0])))
  return g.add(self._mid(1.05, "過 B 且平行於 OA 的直線", "the line through B parallel to OA",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(0.25, "包含 X，若且唯若座標差是 OA 的倍數",
                         "contains X exactly when the difference is a multiple of OA",
                         ACCENT_A, FS_TAG, x=3.35, w=5.2),
               self._mid(-0.55, "所以方程是參數乘方向再加位移",
                         "so the equation is parameter times direction plus offset",
                         ACCENT_B, FS_TAG, x=3.35, w=5.2),
               self._mid(-1.62, "拆成座標就是三條參數方程", "in coordinates, three parametric equations",
                         DIM, FS_TAG, w=11.4))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  br, lc = self._bridge(), self._line_coord()
  ax, tr, un = self._axis_system(), self._triple(), self._units()
  a1, a2, a3 = self._assume1(), self._assume2(), self._assume3()
  py, pe, le = self._pythagoras(), self._perp(), self._line_eq()

  return [([br], []),                          # 0  why this section exists
          ([lc], [br]),                        # 1  coordinates on a line
          ([ax], [lc]),                        # 2  the axis system
          ([tr], [ax]),                        # 3  Fig. 1.4
          ([un], [tr]),                        # 4  unit points to unit vectors
          ([a1], [un]),                        # 5  assumption one
          ([a2], [a1]),                        # 6  assumption two
          ([a3], [a2]),                        # 7  assumption three
          ([py], [a3]),                        # 8  assumption four
          ([pe], [py]),                        # 9  perpendicularity
          ([le], [pe])]                        # 10 the line


AdvCalcE09ZH, AdvCalcE09EN = make(AdvCalcE09Base, "09", prefix="AdvCalcE")
