"""advcalc E10 — Chapter 1, section 2, second half (book pp. 39-43): the
equation of a plane, dropping the scalar product for a linear functional,
parallel translation, affine subspaces and hyperplanes.

The section has one real turn in it, and beats 2 and 3 exist to carry it: the
plane's equation is derived with the scalar product and then the scalar product
is deliberately thrown away, because a general vector space has none. So beat 2
is the only beat in the episode whose picture is a comparison rather than a
construction, and beat 3 redraws the same plane with the new description over
it, to make the point that nothing about the plane changed.

Beat 10 pays off the whole run: a hyperplane is a plane in three-space and a
line in the plane, which is a claim about two pictures side by side.
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


class AdvCalcE10Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 10

 MODE_LABEL = {
  0: {"zh": "垂直於一個方向的平面", "en": "the plane perpendicular to a direction"},
  1: {"zh": "展開成係數乘座標", "en": "expanded into coefficients times coordinates"},
  2: {"zh": "但一般空間沒有純量積", "en": "but a general space has no scalar product"},
  3: {"zh": "改用線性泛函描述同一個平面",
      "en": "the same plane, described by a functional"},
  4: {"zh": "係數隨時讀得回來", "en": "the coefficients read back off f"},
  5: {"zh": "每條有向線段滑到等價的線段",
      "en": "every directed segment slides to an equivalent one"},
  6: {"zh": "座標之間差一個固定向量", "en": "the coordinates differ by one fixed vector"},
  7: {"zh": "平行移動就是加上常向量", "en": "a translation is adding a constant vector"},
  8: {"zh": "平移後還是一個平面", "en": "the translate is again a plane"},
  9: {"zh": "平面與直線都是子空間的平移",
      "en": "planes and lines are translates of subspaces"},
  10: {"zh": "超平面", "en": "the hyperplane"},
 }

 # The quad corners pick up EY as well as EZ, so the top corner of a raised
 # plane sits far higher than its offset suggests; sized against that corner.
 ORG = np.array([-2.55, -0.55, 0.0])
 S = 0.85
 AV = np.array([0.0, 0.0, 1.30])                # the normal direction OA
 BV = np.array([0.55, 0.45, 0.55])              # the base point B

 def _plane(self, offset, org=None, s=None, color=ACCENT_B, op=0.14, half=1.25):
  """A quad perpendicular to AV, at the given height along it."""
  org = self.ORG if org is None else org
  s = self.S if s is None else s
  c = offset * np.array([0.0, 0.0, 1.0])
  corners = [c + np.array([sx * half, sy * half, 0.0])
             for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  return Polygon(*[_p(v, org, s) for v in corners], color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=op)

 def _frame(self, show_b=True):
  o = _p(np.zeros(3), self.ORG, self.S)
  g = VGroup(self._arr(o, _p(self.AV, self.ORG, self.S), ACCENT_A, sw=3.5, tl=0.16),
             Dot(o, radius=0.06, color=INK),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.18, 0])),
             Text("A", font_size=FS_TAG, color=ACCENT_A)
             .move_to(_p(self.AV, self.ORG, self.S) + np.array([-0.26, 0.16, 0])))
  if show_b:
   b = _p(self.BV, self.ORG, self.S)
   g.add(Dot(b, radius=0.075, color=ACCENT_C),
         Text("B", font_size=FS_TAG, color=ACCENT_C).move_to(b + np.array([0.24, -0.12, 0])))
  return g

 # ── beats 0-4 ─────────────────────────────────────────────────────
 def _perp_plane(self):
  g = VGroup(self._plane(self.BV[2]), self._frame())
  X = self.BV + np.array([0.95, -0.70, 0.0])
  xp, bp = _p(X, self.ORG, self.S), _p(self.BV, self.ORG, self.S)
  g.add(Line(bp, xp, color=WARN, stroke_width=3), Dot(xp, radius=0.075, color=WARN),
        Text("X", font_size=FS_TAG, color=WARN).move_to(xp + np.array([0.22, -0.16, 0])))
  return g.add(self._mid(1.05, "平面包含 X", "the plane contains X",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "若且唯若 BX 垂直於 OA 的方向",
                         "exactly when BX is perpendicular to the direction OA",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "翻成座標，就是一個純量積等於零",
                         "in coordinates, one scalar product is zero",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "用的是上一集的第二與第四件事",
                         "using the second and fourth facts of the last episode",
                         DIM, FS_TAG, w=11.4))

 def _expand(self):
  g = VGroup(self._plane(self.BV[2]), self._frame())
  return g.add(self._mid(1.05, "純量積對第一個變數是線性的",
                         "the scalar product is linear in its first variable",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "把定值那一項記成一個數", "name the constant term",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "方程就變成係數乘座標再加起來",
                         "and the equation is coefficients times coordinates, summed",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "反過來只要方向不是零，滿足這個方程的點集就是一個平面",
                         "conversely, if the direction is nonzero, that locus is a plane",
                         DIM, FS_TAG, w=11.6))

 def _no_product(self):
  """The one comparison beat: three-space has a scalar product, a general
  vector space has nothing in that slot."""
  g = VGroup()
  for cx, zh, en, col, has in ((-3.15, "座標三維空間", "coordinate three-space", ACCENT_B, True),
                               (3.15, "一般的向量空間", "a general vector space", WARN, False)):
   g.add(Rectangle(width=4.30, height=2.15, color=col, stroke_width=2.5).move_to([cx, 0.10, 0]),
         self._mid(0.95, zh, en, col, FS_TAG, x=cx, w=3.9))
   if has:
    g.add(Text("( x , y )  =  Σ xᵢ yᵢ", font_size=FS_TAG + 2, color=ACCENT_B)
          .move_to([cx, 0.10, 0]),
          self._mid(-0.62, "有自然的純量積", "has a natural scalar product",
                    ACCENT_B, FS_TAG, x=cx, w=3.9))
   else:
    g.add(Line([cx - 0.70, -0.20, 0], [cx + 0.70, 0.40, 0], color=WARN, stroke_width=4),
          Line([cx - 0.70, 0.40, 0], [cx + 0.70, -0.20, 0], color=WARN, stroke_width=4),
          self._mid(-0.62, "沒有", "has none at all", WARN, FS_TAG, x=cx, w=3.9))
  return g.add(self._mid(-1.55, "所以書上刻意在早期的向量理論裡完全不用它，第五章才回來",
                         "so the book deliberately neglects it until chapter five",
                         DIM, FS_TAG, w=11.8))

 def _functional(self):
  """The very same plane, relabelled. Nothing in the picture moves."""
  g = VGroup(self._plane(self.BV[2], color=ACCENT_A, op=0.16), self._frame(show_b=False))
  return g.add(self._mid(1.05, "同一個平面，一模一樣", "the very same plane, unchanged",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "係數乘座標就是最一般的線性泛函",
                         "coefficients times coordinates is the general functional",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "所以方程可以完全不提純量積",
                         "so the equation need not mention the scalar product",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "反過來，任何非零泛函與任何一個數，決定的都是一個平面",
                         "conversely any nonzero functional and any number give a plane",
                         DIM, FS_TAG, w=11.6))

 def _read_back(self):
  ox = -3.30
  g = VGroup()
  for k in range(3):
   x = ox + k * 1.15
   g.add(Rectangle(width=0.86, height=0.52, color=ACCENT_B, stroke_width=2)
         .move_to([x, 0.68, 0]),
         Text(f"δ{'¹²³'[k]}", font_size=FS_TAG - 2, color=ACCENT_B).move_to([x, 0.68, 0]),
         self._arr([x, 0.34, 0], [x, -0.14, 0], DIM, sw=2, tl=0.10),
         Text("f", font_size=FS_TAG - 3, color=ACCENT_A).move_to([x + 0.24, 0.10, 0]),
         Rectangle(width=0.86, height=0.52, color=ACCENT_A, stroke_width=2)
         .move_to([x, -0.46, 0]),
         Text(f"a{'₁₂₃'[k]}", font_size=FS_TAG - 2, color=ACCENT_A).move_to([x, -0.46, 0]))
  return g.add(self._mid(1.15, "把三個單位向量餵進泛函", "feed the three unit vectors into f",
                         DIM, FS_TAG, x=2.95, w=5.6),
               self._mid(0.20, "出來的就是三個係數", "and out come the three coefficients",
                         ACCENT_A, FS_TAG, x=2.95, w=5.6),
               self._mid(-0.65, "所以兩個描述隨時互換", "so the two descriptions interchange freely",
                         DIM, FS_TAG, x=2.95, w=5.6),
               self._mid(-1.55, "泛函與係數三元組，本來就是同一份資料",
                         "the functional and its coefficient triple are the same data",
                         DIM, FS_TAG, w=11.4))

 # ── beats 5-8: translation ────────────────────────────────────────
 TRI = (np.array([0.0, 0.0, 0.0]), np.array([1.25, 0.20, 0.0]), np.array([0.55, 1.05, 0.0]))
 SHIFT = np.array([1.65, -0.85, 0.0])

 def _slide(self):
  """A figure and its slide, with the matching directed segments drawn."""
  # A longer shift than the later beats use: at the shared SHIFT the two copies
  # overlapped and the slide could not be read off the picture.
  o = np.array([-3.05, 0.05, 0.0])
  sh = 1.45 * self.SHIFT
  g = VGroup()
  for off, col, op in ((np.zeros(3), ACCENT_B, 0.14), (sh, ACCENT_A, 0.14)):
   pts = [o + off + v for v in self.TRI]
   g.add(Polygon(*pts, color=col, stroke_width=2.5, fill_color=col, fill_opacity=op))
  for v, col in zip(self.TRI, (WARN, ACCENT_C, DIM)):
   g.add(self._arr(o + v, o + v + sh, col, sw=2.2, tl=0.11))
  return g.add(self._mid(1.05, "把圖形沿著平面滑動", "slide the figure along the plane",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "所有直線都保持平行", "every line stays parallel to where it was",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "每條有向線段都滑到與它等價的線段",
                         "each directed segment slides to an equivalent one",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "三支箭頭一模一樣 —— 這正是等價的條件",
                         "the three arrows are identical, which is the equivalence condition",
                         DIM, FS_TAG, w=11.6))

 def _difference(self):
  o = np.array([-2.10, -0.30, 0.0])
  x = o + np.array([1.05, 1.15, 0.0])
  y = x + self.SHIFT
  b = o + self.SHIFT
  g = VGroup(self._arr(o, x, ACCENT_B, sw=3, tl=0.14),
             self._arr(b, y, ACCENT_C, sw=3, tl=0.14),
             self._arr(o, b, ACCENT_A, sw=3.5, tl=0.16),
             self._arr(x, y, ACCENT_A, sw=3.5, tl=0.16),
             Dot(o, radius=0.065, color=INK), Dot(b, radius=0.07, color=ACCENT_A),
             Text("O", font_size=FS_TAG, color=INK).move_to(o + np.array([-0.24, -0.16, 0])),
             Text("B", font_size=FS_TAG, color=ACCENT_A).move_to(b + np.array([0.06, -0.30, 0])),
             Text("X", font_size=FS_TAG, color=ACCENT_B).move_to(x + np.array([-0.22, 0.22, 0])),
             Text("Y", font_size=FS_TAG, color=ACCENT_C).move_to(y + np.array([0.24, 0.14, 0])))
  return g.add(self._mid(1.05, "X 滑到 Y，原點滑到 B", "X slides to Y, the origin to B",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(0.20, "所以 OX 與 BY 等價", "so OX and BY are equivalent",
                         DIM, FS_TAG, x=3.35, w=5.2),
               self._mid(-0.65, "座標之間差的就是同一個固定向量",
                         "the coordinates differ by one and the same fixed vector",
                         ACCENT_A, FS_TAG, x=3.35, w=5.2))

 def _add_const(self):
  """A grid of points, each pushed by the same vector."""
  g = VGroup()
  ox, oy, s = -3.55, -0.35, 0.60
  for i in range(4):
   for j in range(3):
    p0 = np.array([ox + i * s, oy + j * s, 0.0])
    g.add(Dot(p0, radius=0.055, color=GHOST),
          self._arr(p0, p0 + self.SHIFT * 0.62, ACCENT_A, sw=1.8, tl=0.09),
          Dot(p0 + self.SHIFT * 0.62, radius=0.055, color=ACCENT_A))
  return g.add(self._mid(1.10, "每一點都被推同一段", "every point is pushed the same way",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(0.25, "所以座標形式就是加上一個常向量",
                         "so in coordinates it is adding a constant vector",
                         ACCENT_A, FS_TAG, x=3.20, w=5.4),
               self._mid(-0.60, "反過來任何常向量都給出一個平行移動",
                         "and any constant vector gives a translation",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.62, "平面與空間都一樣成立", "this holds for the plane and for space alike",
                         DIM, FS_TAG, w=11.4))

 def _translate_plane(self):
  """Two parallel planes: the same functional, a shifted constant."""
  g = VGroup(self._plane(0.15, color=ACCENT_B, op=0.14),
             self._plane(0.95, color=ACCENT_A, op=0.14),
             self._frame(show_b=False))
  p0 = _p(np.array([0.0, 0.0, 0.15]), self.ORG, self.S)
  p1 = _p(np.array([0.0, 0.0, 0.95]), self.ORG, self.S)
  g.add(self._arr(p0, p1, ACCENT_A, sw=3, tl=0.14),
        Text("b", font_size=FS_TAG, color=ACCENT_A)
        .move_to(0.5 * (p0 + p1) + np.array([0.26, 0.0, 0])))
  return g.add(self._mid(1.05, "同一個泛函", "the same functional",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(0.25, "常數加上泛函在位移向量的值",
                         "the constant plus the functional at the shift",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.55, "所以平移之後還是一個平面",
                         "so the translate is again a plane",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.62, "幾何上很明顯，現在也有了純代數的證明",
                         "geometrically clear, and now proved algebraically",
                         DIM, FS_TAG, w=11.4))

 # ── beats 9-10 ────────────────────────────────────────────────────
 def _through_origin(self):
  """The plane through the origin is the null space; every other plane is
  that one, shifted."""
  g = VGroup(self._plane(0.0, color=ACCENT_B, op=0.18),
             self._plane(0.95, color=DIM, op=0.08),
             self._frame(show_b=False))
  p0 = _p(np.zeros(3), self.ORG, self.S)
  p1 = _p(np.array([0.0, 0.0, 0.95]), self.ORG, self.S)
  g.add(self._arr(p0, p1, DIM, sw=2.5, tl=0.13))
  return g.add(self._mid(1.05, "常數是零時，平面通過原點",
                         "when the constant is zero the plane passes through the origin",
                         ACCENT_B, FS_TAG, x=3.25, w=5.4),
               self._mid(0.25, "這時它就是泛函的零空間，是子空間",
                         "and then it is the null space of f, a subspace",
                         ACCENT_A, FS_TAG, x=3.25, w=5.4),
               self._mid(-0.55, "其他的平面都是它的平移", "every other plane is a translate of it",
                         DIM, FS_TAG, x=3.25, w=5.4),
               self._mid(-1.62, "直線也一樣 —— 座標空間裡的平面與直線，都是子空間的平移",
                         "lines too: planes and lines are translates of subspaces",
                         ACCENT_A, FS_TAG, w=11.8))

 def _hyperplane(self):
  """The payoff, as two pictures: a hyperplane is a plane in three-space and
  a line in the plane."""
  g = VGroup()
  org3 = np.array([-3.55, -0.30, 0.0])
  g.add(self._plane(0.0, org=org3, s=0.72, color=ACCENT_B, op=0.18, half=1.60),
        Dot(_p(np.zeros(3), org3, 0.72), radius=0.06, color=INK),
        self._mid(1.10, "在三維空間裡：一個平面", "in three-space: a plane",
                  ACCENT_B, FS_TAG, x=-3.55, w=4.4),
        self._mid(-1.20, "維數是 3 減 1", "dimension three minus one",
                  DIM, FS_TAG, x=-3.55, w=4.4))
  cx, cy, r = 3.05, -0.20, 1.05
  g.add(self._arr([cx - r, cy, 0], [cx + r, cy, 0], DIM, sw=2.5, tl=0.13),
        self._arr([cx, cy - r, 0], [cx, cy + r, 0], DIM, sw=2.5, tl=0.13),
        Line([cx - 0.92, cy + 0.78, 0], [cx + 0.92, cy - 0.78, 0],
             color=ACCENT_A, stroke_width=4),
        Dot([cx, cy, 0], radius=0.06, color=INK),
        self._mid(1.10, "在平面裡：一條直線", "in the plane: a line",
                  ACCENT_A, FS_TAG, x=cx, w=4.4),
        self._mid(-1.20, "維數是 2 減 1", "dimension two minus one",
                  DIM, FS_TAG, x=cx, w=4.4))
  return g.add(self._mid(-1.72, "非零泛函的零空間永遠是 n 減一維的，這種東西叫超平面",
                         "the null space of a nonzero functional always has dimension n minus one",
                         ACCENT_A, FS_TAG, w=11.8))

 # ── the eleven beats ─────────────────────────────────────────────
 def stage(self):
  pp, ex = self._perp_plane(), self._expand()
  npd, fnl, rb = self._no_product(), self._functional(), self._read_back()
  sl, df, ac = self._slide(), self._difference(), self._add_const()
  tp, to, hp = self._translate_plane(), self._through_origin(), self._hyperplane()

  return [([pp], []),                          # 0  the perpendicular plane
          ([ex], [pp]),                        # 1  expanded
          ([npd], [ex]),                       # 2  no scalar product in general
          ([fnl], [npd]),                      # 3  the same plane, via f
          ([rb], [fnl]),                       # 4  reading the coefficients back
          ([sl], [rb]),                        # 5  sliding
          ([df], [sl]),                        # 6  the fixed difference
          ([ac], [df]),                        # 7  adding a constant vector
          ([tp], [ac]),                        # 8  the translate is a plane
          ([to], [tp]),                        # 9  translates of subspaces
          ([hp], [to])]                        # 10 hyperplanes


AdvCalcE10ZH, AdvCalcE10EN = make(AdvCalcE10Base, "10", prefix="AdvCalcE")
