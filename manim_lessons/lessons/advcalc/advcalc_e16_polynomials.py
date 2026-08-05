"""advcalc E16 — Chapter 1, section 5, last part (book pp. 61-67): solving a
linear equation, and polynomials in T.

The section's own framing is that "solving" means producing a right inverse,
so beat 3 draws what that buys: a whole line of targets going back to a whole
line of solutions, which is the content of "the solution varies linearly" and
is invisible in the equation. Beats 5 to 7 are about a correspondence that
preserves three operations at once, so the three are drawn side by side rather
than named.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Ellipse, Line, Polygon, Rectangle, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

EX = np.array([0.92, -0.30, 0.0])
EY = np.array([0.66, 0.40, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def _p(v, org, s=1.0):
 return org + s * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AdvCalcE16Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 16

 MODE_LABEL = {
  0: {"zh": "有解，就是目標落在值域裡", "en": "solvable means the target is in the range"},
  1: {"zh": "把值域當成新的上域", "en": "make the range the new codomain"},
  2: {"zh": "求解程序就是一個右逆", "en": "a solution process is a right inverse"},
  3: {"zh": "解要隨目標線性地變化", "en": "the solution must vary linearly"},
  4: {"zh": "補空間與右逆一一對應", "en": "complements match right inverses"},
  5: {"zh": "把變數換成 T", "en": "substitute T for the variable"},
  6: {"zh": "多項式相乘，對應算子合成", "en": "multiplying polynomials is composing"},
  7: {"zh": "三個運算同時被保持", "en": "all three operations preserved"},
  8: {"zh": "互質，就湊得出一", "en": "relatively prime: the combination is one"},
  9: {"zh": "不變：T 把它送進自己", "en": "invariant: T carries it into itself"},
  10: {"zh": "零空間裂成直和", "en": "the null space splits into a direct sum"},
 }

 def _blob(self, cx, cy, rx, ry, col, op=0.0, sw=2.5):
  return Ellipse(width=2 * rx, height=2 * ry, color=col, stroke_width=sw,
                 fill_color=col, fill_opacity=op).move_to([cx, cy, 0])

 def _solvable(self):
  ax, bx, cy = -3.10, 1.75, 0.05
  g = VGroup(self._blob(ax, cy, 1.15, 1.05, DIM),
             self._blob(bx, cy, 1.15, 1.05, DIM),
             self._blob(bx, cy - 0.22, 0.78, 0.62, ACCENT_A, 0.16),
             Text("V", font_size=FS_TAG, color=DIM).move_to([ax, cy + 1.12, 0]),
             Text("W", font_size=FS_TAG, color=DIM).move_to([bx, cy + 1.12, 0]),
             Text("R ( T )", font_size=FS_TAG - 3, color=ACCENT_A)
             .move_to([bx, cy - 0.22, 0]),
             self._arr([ax + 1.28, cy, 0], [bx - 1.28, cy, 0], ACCENT_A, sw=3, tl=0.15),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-0.70, cy + 0.32, 0]),
             Dot([bx + 0.30, cy - 0.42, 0], radius=0.085, color=ACCENT_B),
             Dot([bx - 0.10, cy + 0.72, 0], radius=0.085, color=WARN))
  return g.add(self._mid(-1.25, "落在值域裡的目標，有解；落在外面的，無解",
                         "a target inside the range is solvable, one outside is not",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.75, "所以第一個問題永遠是：值域到底是什麼",
                         "so the first question is always what the range actually is",
                         ACCENT_A, FS_TAG, w=11.6))

 def _onto(self):
  ax, bx, cy = -3.10, 1.75, 0.05
  g = VGroup(self._blob(ax, cy, 1.15, 1.05, DIM),
             self._blob(bx, cy, 0.86, 0.78, ACCENT_A, 0.16),
             Text("V", font_size=FS_TAG, color=DIM).move_to([ax, cy + 1.12, 0]),
             Text("W", font_size=FS_TAG, color=ACCENT_A).move_to([bx, cy + 0.98, 0]),
             self._arr([ax + 1.28, cy, 0], [bx - 0.99, cy, 0], ACCENT_A, sw=3, tl=0.15),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-0.55, cy + 0.32, 0]))
  return g.add(self._mid(-1.25, "認得值域，就把它當成新的上域",
                         "once the range is known, make it the codomain",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.75, "於是可以假設 T 是滿的；剩下的問題是「解出來」是什麼意思",
                         "so we may assume T is onto; what remains is what solving means",
                         ACCENT_A, FS_TAG, w=11.8))

 def _right_inverse(self):
  ax, bx, cy = -2.85, 1.95, 0.15
  g = VGroup(self._blob(ax, cy, 1.05, 0.95, DIM), self._blob(bx, cy, 1.05, 0.95, DIM),
             Text("V", font_size=FS_TAG, color=DIM).move_to([ax, cy + 1.02, 0]),
             Text("W", font_size=FS_TAG, color=DIM).move_to([bx, cy + 1.02, 0]),
             self._arr([ax + 1.18, cy + 0.26, 0], [bx - 1.18, cy + 0.26, 0],
                       ACCENT_A, sw=3, tl=0.15),
             Text("T", font_size=FS_TAG, color=ACCENT_A).move_to([-0.45, cy + 0.58, 0]),
             self._arr([bx - 1.18, cy - 0.26, 0], [ax + 1.18, cy - 0.26, 0],
                       ACCENT_B, sw=3, tl=0.15),
             Text("S", font_size=FS_TAG, color=ACCENT_B).move_to([-0.45, cy - 0.58, 0]))
  return g.add(self._mid(-1.25, "S 把目標送回去，跟 T 合起來剛好是恆等",
                         "S sends the target back, and composing with T gives the identity",
                         ACCENT_B, FS_TAG, w=11.6),
               self._mid(-1.75, "所有重要的求解程序，本質上都是在算這個右逆",
                         "every important solution process is computing that right inverse",
                         ACCENT_A, FS_TAG, w=11.8))

 def _linear_choice(self):
  """A line of targets going back to a line of solutions: that the choice is
  linear is the content, and a single pair of dots would not show it."""
  o1 = np.array([-3.20, -0.15, 0.0])
  o2 = np.array([2.00, -0.15, 0.0])
  d1 = np.array([0.55, 1.05, 0.0])
  d2 = np.array([0.85, 0.62, 0.0])
  g = VGroup(Line(o1 - 0.85 * d1, o1 + 0.95 * d1, color=ACCENT_B, stroke_width=3.5),
             Line(o2 - 0.85 * d2, o2 + 0.95 * d2, color=ACCENT_A, stroke_width=3.5),
             Text("V", font_size=FS_TAG, color=DIM).move_to([o1[0] - 1.05, 1.05, 0]),
             Text("W", font_size=FS_TAG, color=DIM).move_to([o2[0] + 1.15, 1.05, 0]))
  for f in (-0.6, 0.0, 0.7):
   g.add(Dot(o2 + f * d2, radius=0.075, color=ACCENT_A),
         Dot(o1 + f * d1, radius=0.075, color=ACCENT_B),
         self._arr(o2 + f * d2 - np.array([0.22, 0, 0]),
                   o1 + f * d1 + np.array([0.22, 0, 0]), DIM, sw=1.8, tl=0.09))
  return g.add(self._mid(-1.25, "目標沿著一條線走，解也沿著一條線走",
                         "as the target runs along a line, so does the solution",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.75, "把這個當成「解出來」的意思，說法就乾淨了",
                         "taking that as the meaning of solving gives a clean statement",
                         DIM, FS_TAG, w=11.6))

 ORG = np.array([-2.95, -0.30, 0.0])
 S = 0.82

 def _plane(self, color=ACCENT_B, op=0.14, half=1.30):
  quad = [np.array([sx * half, sy * half, 0.0]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  return Polygon(*[_p(v, self.ORG, self.S) for v in quad], color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=op)

 MDIR = np.array([0.35, 0.45, 1.20])

 def _thm53(self):
  o3 = _p(np.zeros(3), self.ORG, self.S)
  assert abs(float(self.MDIR[2])) > 0.4, "the complement must leave the null space plane"
  g = VGroup(self._plane(), Dot(o3, radius=0.06, color=INK),
             Line(_p(-0.95 * self.MDIR, self.ORG, self.S),
                  _p(1.15 * self.MDIR, self.ORG, self.S), color=ACCENT_A, stroke_width=3.5),
             Text("N", font_size=FS_TAG, color=ACCENT_B)
             .move_to(_p(np.array([-1.10, 1.10, 0]), self.ORG, self.S)),
             Text("M", font_size=FS_TAG, color=ACCENT_A)
             .move_to(_p(1.15 * self.MDIR, self.ORG, self.S) + np.array([0.28, 0.10, 0])))
  return g.add(self._mid(1.05, "N 是零空間", "N is the null space",
                         ACCENT_B, FS_TAG, x=3.30, w=5.2),
               self._mid(0.20, "M 是它的補空間", "M is a complement of it",
                         ACCENT_A, FS_TAG, x=3.30, w=5.2),
               self._mid(-0.65, "若且唯若 T 限制在 M 上是同構",
                         "exactly when T restricted to M is an isomorphism",
                         DIM, FS_TAG, x=3.30, w=5.2),
               self._mid(-1.68, "而「取那個限制的反函數」，是補空間與右逆之間的雙射",
                         "and inverting that restriction is a bijection onto the right inverses",
                         ACCENT_A, FS_TAG, w=11.9))

 def _substitute(self):
  g = VGroup()
  for k, (lab, col, y) in enumerate((("q ( t )  =  c₀ + c₁ t + c₂ t ²", ACCENT_B, 0.70),
                                     ("q ( T )  =  c₀ I + c₁ T + c₂ T ∘ T", ACCENT_A, -0.30))):
   g.add(Rectangle(width=5.60, height=0.72, color=col, stroke_width=2.5).move_to([-1.85, y, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([-1.85, y, 0]))
  g.add(self._arr([-1.85, 0.30, 0], [-1.85, -0.06, 0], ACCENT_A, sw=2.5, tl=0.12),
        Text("t  ↦  T", font_size=FS_TAG, color=ACCENT_A).move_to([-0.10, 0.14, 0]))
  return g.add(self._mid(0.70, "一個多項式", "a polynomial", DIM, FS_TAG, x=3.60, w=4.0),
               self._mid(-0.30, "變成一個算子", "becomes an operator",
                         ACCENT_A, FS_TAG, x=3.60, w=4.0),
               self._mid(-1.25, "算子的次方，就是它跟自己合成那麼多次",
                         "a power of the operator means composing it with itself",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.75, "固定同一個 T，所以整組多項式共用一個算子",
                         "the same T throughout, so all the polynomials share one operator",
                         DIM, FS_TAG, w=11.6))

 def _commute(self):
  g = VGroup()
  rows = ((0.62, ("p₁ ( T )", "p₂ ( T )"), ACCENT_B), (-0.28, ("p₂ ( T )", "p₁ ( T )"), ACCENT_C))
  for y, (a, b), col in rows:
   for j, lab in enumerate((a, b)):
    g.add(Rectangle(width=1.55, height=0.52, color=col, stroke_width=2)
          .move_to([-3.35 + j * 1.85, y, 0]),
          Text(lab, font_size=FS_TAG - 2, color=col).move_to([-3.35 + j * 1.85, y, 0]))
   g.add(self._arr([-2.50, y, 0], [-2.35, y, 0], DIM, sw=1.8, tl=0.08),
         self._arr([-0.62, y, 0], [0.35, y, 0], col, sw=2.2, tl=0.11))
  g.add(Rectangle(width=1.85, height=1.30, color=ACCENT_A, stroke_width=2.5)
        .move_to([1.35, 0.17, 0]),
        Text("p ( T )", font_size=FS_TAG, color=ACCENT_A).move_to([1.35, 0.17, 0]))
  return g.add(self._mid(-1.05, "兩個次序，同一個算子——所以它們可交換",
                         "either order, the same operator: so they commute",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.68, "這來自合成的雙線性；加法那邊更直接",
                         "this comes from the bilinearity of composition; addition is more direct",
                         DIM, FS_TAG, w=11.6))

 def _homomorphism(self):
  g = VGroup()
  for cx, zh, en, col in ((-3.05, "多項式的代數", "the algebra of polynomials", ACCENT_B),
                          (3.05, "算子的代數", "the algebra of operators", ACCENT_A)):
   g.add(Rectangle(width=4.20, height=2.20, color=col, stroke_width=2.5).move_to([cx, 0.15, 0]),
         self._mid(1.00, zh, en, col, FS_TAG, x=cx, w=3.9))
  for k, (a, b) in enumerate((("p + q", "P + Q"), ("p · q", "P ∘ Q"), ("c p", "c P"))):
   y = 0.30 - k * 0.55
   g.add(Text(a, font_size=FS_TAG - 1, color=ACCENT_B).move_to([-3.05, y, 0]),
         Text(b, font_size=FS_TAG - 1, color=ACCENT_A).move_to([3.05, y, 0]),
         self._arr([-1.55, y, 0], [1.55, y, 0], DIM, sw=1.8, tl=0.09))
  return g.add(self._mid(-1.30, "三個運算同時被保持，這就叫代數同態",
                         "all three operations preserved: that is an algebra homomorphism",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.78, "同態是通用的詞——向量空間之間的同態就是線性變換",
                         "the word is general: a homomorphism of vector spaces is a linear map",
                         DIM, FS_TAG, w=11.8))

 def _coprime(self):
  g = VGroup(Rectangle(width=6.60, height=0.80, color=ACCENT_A, stroke_width=2.5)
             .move_to([-1.35, 0.45, 0]),
             Text("a₁ ( t ) p₁ ( t )  +  a₂ ( t ) p₂ ( t )  =  1", font_size=FS_TAG + 2,
                  color=ACCENT_A).move_to([-1.35, 0.45, 0]),
             self._mid(-0.45, "p₁ 與 p₂ 互質：除了常數以外沒有公因式",
                       "relatively prime: no common factor but constants",
                       DIM, FS_TAG, x=-1.35, w=6.4))
  return g.add(self._mid(0.45, "一定湊得出這樣一對", "such a pair always exists",
                         ACCENT_A, FS_TAG, x=4.10, w=3.6),
               self._mid(-1.30, "書上直接假設這件事，證明留給代數課",
                         "the book assumes this and leaves the proof to algebra",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.78, "下一拍就靠它把零空間拆開",
                         "the next beat uses it to split a null space",
                         DIM, FS_TAG, w=11.4))

 def _invariant(self):
  o3 = _p(np.zeros(3), self.ORG, self.S)
  u, v = np.array([0.95, -0.55, 0.0]), np.array([0.25, 1.00, 0.0])
  g = VGroup(self._plane(color=ACCENT_B, op=0.14),
             Dot(o3, radius=0.06, color=INK),
             self._arr(o3, _p(u, self.ORG, self.S), ACCENT_C, sw=3, tl=0.14),
             self._arr(o3, _p(0.55 * u + 0.62 * v, self.ORG, self.S), ACCENT_A, sw=3.5, tl=0.16),
             self._dash(_p(u, self.ORG, self.S), _p(0.55 * u + 0.62 * v, self.ORG, self.S),
                        GHOST, n=8),
             Text("M", font_size=FS_TAG, color=ACCENT_B)
             .move_to(_p(np.array([-1.05, 1.05, 0]), self.ORG, self.S)))
  return g.add(self._mid(1.05, "T 把 M 送進 M 自己裡面", "T carries M into M itself",
                         ACCENT_A, FS_TAG, x=3.20, w=5.4),
               self._mid(0.10, "就說 M 在 T 之下不變", "then M is invariant under T",
                         DIM, FS_TAG, x=3.20, w=5.4),
               self._mid(-1.30, "定理：任何 T 的多項式，它的零空間都是不變的",
                         "the theorem: the null space of any polynomial in T is invariant",
                         ACCENT_A, FS_TAG, w=11.6),
               self._mid(-1.74, "因為 T 與 q ( T ) 可交換", "because T and q of T commute",
                         DIM, FS_TAG, w=11.6))

 def _split(self):
  g = VGroup(Rectangle(width=2.35, height=0.66, color=ACCENT_A, stroke_width=2.5)
             .move_to([-3.35, 0.85, 0]),
             Text("q  =  q₁ q₂", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-3.35, 0.85, 0]))
  o3 = _p(np.zeros(3), np.array([-2.55, -0.55, 0.0]), 0.72)
  quad = [_p(np.array([sx * 1.15, sy * 1.15, 0.0]), np.array([-2.55, -0.55, 0.0]), 0.72)
          for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  d = np.array([0.30, 0.40, 1.10])
  g.add(Polygon(*quad, color=ACCENT_B, stroke_width=2.5,
                fill_color=ACCENT_B, fill_opacity=0.14),
        Line(_p(-0.85 * d, np.array([-2.55, -0.55, 0.0]), 0.72),
             _p(1.05 * d, np.array([-2.55, -0.55, 0.0]), 0.72), color=ACCENT_C, stroke_width=3.5),
        Dot(o3, radius=0.06, color=INK),
        Text("N₁", font_size=FS_TAG - 2, color=ACCENT_B)
        .move_to(_p(np.array([-0.95, 0.95, 0]), np.array([-2.55, -0.55, 0.0]), 0.72)),
        Text("N₂", font_size=FS_TAG - 2, color=ACCENT_C)
        .move_to(_p(1.05 * d, np.array([-2.55, -0.55, 0.0]), 0.72) + np.array([0.28, 0.08, 0])))
  return g.add(self._mid(0.85, "互質的兩個因子", "two relatively prime factors",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(0.00, "零空間就裂成兩塊的直和",
                         "and the null space splits as a direct sum",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.85, "兩塊在 T 之下都不變", "both pieces invariant under T",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.68, "推論用歸納推到任意多個互質因子——後面解微分方程要用",
                         "a corollary extends it to any number of factors, used later on",
                         DIM, FS_TAG, w=11.9))

 def stage(self):
  sv, on, ri, lc = self._solvable(), self._onto(), self._right_inverse(), self._linear_choice()
  t53, sub, cm = self._thm53(), self._substitute(), self._commute()
  hom, cp, inv, sp = self._homomorphism(), self._coprime(), self._invariant(), self._split()
  return [([sv], []), ([on], [sv]), ([ri], [on]), ([lc], [ri]),
          ([t53], [lc]), ([sub], [t53]), ([cm], [sub]), ([hom], [cm]),
          ([cp], [hom]), ([inv], [cp]), ([sp], [inv])]


AdvCalcE16ZH, AdvCalcE16EN = make(AdvCalcE16Base, "16", prefix="AdvCalcE")
