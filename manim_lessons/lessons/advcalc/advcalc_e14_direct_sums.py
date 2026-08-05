"""advcalc E14 — Chapter 1, section 5, first part (book pp. 56-58): direct
sums, the even-odd decomposition, independence and complements.

Two beats carry real content that the symbols do not. Beat 6 draws the
even-odd split of an actual function, because "average it with its own
reflection" is a picture; and beats 9 and 10 draw the book's warning that a
complement is not unique, as one plane with three different lines any of which
completes it -- which is Fig. 1.9 plus the reason the figure is there.
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


class AdvCalcE14Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 14

 MODE_LABEL = {
  0: {"zh": "一族子空間，乘積就是整個空間", "en": "a family of subspaces, product is the whole"},
  1: {"zh": "積空間的等式，在 V 裡的倒影", "en": "the product identities, reflected in V"},
  2: {"zh": "把元組送到它們的和", "en": "sending a tuple to its sum"},
  3: {"zh": "既獨立，又生成", "en": "both independent and spanning"},
  4: {"zh": "存在來自生成，唯一來自獨立", "en": "existence from spanning, uniqueness from independence"},
  5: {"zh": "偶函數與奇函數", "en": "the even and the odd functions"},
  6: {"zh": "跟自己的鏡像平均起來", "en": "average it with its own reflection"},
  7: {"zh": "加起來是零，就每個都是零", "en": "if they sum to zero, each is zero"},
  8: {"zh": "兩個子空間：只交於零", "en": "two subspaces: meeting only at zero"},
  9: {"zh": "補空間不唯一", "en": "a complement is not unique"},
  10: {"zh": "平面配上不在它裡面的直線", "en": "a plane and a line not lying in it"},
 }

 ORG = np.array([-2.65, -0.40, 0.0])
 S = 0.85

 def _plane(self, org=None, s=None, color=ACCENT_B, op=0.13, half=1.35):
  org = self.ORG if org is None else org
  s = self.S if s is None else s
  quad = [np.array([sx * half, sy * half, 0.0]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  return Polygon(*[_p(v, org, s) for v in quad], color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=op)

 def _iso(self):
  g = VGroup(Ellipse(width=2.55, height=1.80, color=ACCENT_A, stroke_width=2.5,
                     fill_color=ACCENT_A, fill_opacity=0.10).move_to([-3.45, 0.30, 0]),
             Text("V", font_size=FS_TAG + 3, color=ACCENT_A).move_to([-3.45, 0.30, 0]))
  for k, y in enumerate((0.95, 0.30, -0.35)):
   g.add(Rectangle(width=1.35, height=0.50, color=(ACCENT_B, ACCENT_C, WARN)[k],
                   stroke_width=2.5).move_to([1.85, y, 0]),
         Text(f"V{k + 1}", font_size=FS_TAG - 2, color=(ACCENT_B, ACCENT_C, WARN)[k])
         .move_to([1.85, y, 0]))
  g.add(Rectangle(width=1.95, height=1.95, color=DIM, stroke_width=2).move_to([1.85, 0.30, 0]),
        self._arr([-2.10, 0.50, 0], [0.75, 0.50, 0], ACCENT_A, sw=3, tl=0.15),
        self._arr([0.75, 0.10, 0], [-2.10, 0.10, 0], ACCENT_A, sw=3, tl=0.15),
        Text("≅", font_size=FS_TAG + 5, color=ACCENT_A).move_to([-0.68, 0.82, 0]))
  return g.add(self._mid(-1.05, "研究某個現象時，冒出一族有限多個子空間",
                         "studying a phenomenon turns up a finite family of subspaces",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.68, "而整個空間自然地同構於它們的乘積",
                         "and the space is naturally isomorphic to their product",
                         ACCENT_A, FS_TAG, w=11.6))

 def _identities(self):
  rows = (("Σ Pᵢ  =  I", ACCENT_A), ("Pⱼ ∘ Pⱼ  =  Pⱼ", ACCENT_B), ("Pᵢ ∘ Pⱼ  =  0", WARN))
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   y = 0.72 - k * 0.72
   g.add(Rectangle(width=3.30, height=0.56, color=col, stroke_width=2.5).move_to([-2.75, y, 0]),
         Text(s, font_size=FS_TAG + 1, color=col).move_to([-2.75, y, 0]))
  return g.add(self._mid(0.72, "全部加起來是恆等", "they sum to the identity",
                         ACCENT_A, FS_TAG, x=2.55, w=5.4),
               self._mid(0.0, "接自己還是自己", "each composed with itself is itself",
                         ACCENT_B, FS_TAG, x=2.55, w=5.4),
               self._mid(-0.72, "不同的兩個相接是零", "different ones compose to zero",
                         WARN, FS_TAG, x=2.55, w=5.4),
               self._mid(-1.62, "這三條是積空間那組投影注入等式，在 V 裡的倒影",
                         "these three are the projection-injection identities, reflected in V",
                         DIM, FS_TAG, w=11.8))

 def _sum_map(self):
  g = VGroup(Rectangle(width=2.05, height=2.00, color=DIM, stroke_width=2)
             .move_to([-3.55, 0.25, 0]))
  cols = (ACCENT_B, ACCENT_C, WARN)
  for k, y in enumerate((0.90, 0.25, -0.40)):
   g.add(Rectangle(width=1.55, height=0.52, color=cols[k], stroke_width=2.5)
         .move_to([-3.55, y, 0]),
         Text(f"α{k + 1}", font_size=FS_TAG - 2, color=cols[k]).move_to([-3.55, y, 0]))
  o = np.array([1.55, -0.55, 0.0])
  vs = (np.array([0.95, 0.42, 0]), np.array([0.30, 0.92, 0]), np.array([0.80, -0.16, 0]))
  p = o
  for k, v in enumerate(vs):
   g.add(self._arr(p, p + v, cols[k], sw=2.5, tl=0.12)); p = p + v
  g.add(self._arr(o, p, ACCENT_A, sw=4, tl=0.18), Dot(o, radius=0.055, color=INK),
        self._arr([-2.35, 0.25, 0], [0.55, 0.25, 0], ACCENT_A, sw=3, tl=0.15),
        Text("π", font_size=FS_TAG + 1, color=ACCENT_A).move_to([-0.90, 0.60, 0]))
  return g.add(self._mid(-1.05, "每個子空間各取一個向量，送到它們的和",
                         "one vector from each subspace, sent to their sum",
                         DIM, FS_TAG, w=11.4),
               self._mid(-1.68, "這是一個從乘積到 V 的線性映射",
                         "that is a linear map from the product into V",
                         ACCENT_A, FS_TAG, w=11.4))

 def _both(self):
  g = VGroup()
  for cx, zh, en, sub_zh, sub_en, col in (
    (-3.15, "嵌射", "injective", "獨立", "independent", ACCENT_B),
    (3.15, "滿射", "surjective", "生成 V", "spanning V", ACCENT_C)):
   g.add(Rectangle(width=4.10, height=1.55, color=col, stroke_width=2.5).move_to([cx, 0.35, 0]),
         self._mid(0.72, zh, en, col, FS_TAG + 1, x=cx, w=3.7),
         self._mid(0.02, sub_zh, sub_en, DIM, FS_TAG, x=cx, w=3.7))
  g.add(Text("+", font_size=FS_TAG + 8, color=DIM).move_to([0.0, 0.35, 0]),
        Rectangle(width=4.60, height=0.68, color=ACCENT_A, stroke_width=2.5)
        .move_to([0.0, -0.95, 0]),
        self._mid(-0.95, "V 是它們的直和", "V is their direct sum", ACCENT_A, FS_TAG, x=0.0, w=4.3),
        self._arr([-3.15, -0.45, 0], [-0.55, -0.65, 0], DIM, sw=2, tl=0.10),
        self._arr([3.15, -0.45, 0], [0.55, -0.65, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(-1.68, "換個說法：每個向量都能唯一地寫成「每個子空間各出一項」的和",
                         "restated: every vector is uniquely a sum with one term from each",
                         DIM, FS_TAG, w=11.9))

 def _unique(self):
  o = np.array([-2.85, -0.55, 0.0])
  u, v = np.array([1.15, 0.32, 0.0]), np.array([0.34, 1.05, 0.0])
  tgt = o + 1.5 * u + 0.9 * v
  g = VGroup(Line(o - 0.55 * u, o + 2.35 * u, color=GHOST, stroke_width=2),
             Line(o - 0.45 * v, o + 1.65 * v, color=GHOST, stroke_width=2),
             self._arr(o, o + 1.5 * u, ACCENT_B, sw=3.5, tl=0.16),
             self._arr(o + 1.5 * u, tgt, ACCENT_C, sw=3.5, tl=0.16),
             self._arr(o, tgt, ACCENT_A, sw=4.5, tl=0.20),
             self._dash(o + 0.9 * v, tgt, GHOST, n=8),
             Dot(o, radius=0.06, color=INK), Dot(tgt, radius=0.085, color=ACCENT_A))
  return g.add(self._mid(1.05, "寫得出來，因為它們生成 V",
                         "an expression exists because they span V",
                         ACCENT_C, FS_TAG, x=3.05, w=5.6),
               self._mid(-0.10, "寫法唯一，因為它們獨立",
                         "it is unique because they are independent",
                         ACCENT_B, FS_TAG, x=3.05, w=5.6),
               self._mid(-1.62, "兩件事都成立，才叫直和",
                         "it takes both to have a direct sum",
                         ACCENT_A, FS_TAG, w=11.4))

 # ── beats 5-6: the even-odd decomposition ────────────────────────
 # amplitude sized so the trough clears the caption below it: the curve
 # reaches BASE - amp * max|f|, and max|f| here is about 1.4
 AX, W, BASE = -1.35, 5.60, -0.10

 def _curve_of(self, fn, col, sw=3, amp=0.46):
  ts = np.linspace(-1, 1, 90)
  return self._curve([[self.AX + t * self.W / 2, self.BASE + amp * fn(2.0 * t), 0]
                      for t in ts], col, sw=sw)

 def _even_odd(self):
  f = lambda z: np.sin(z) + 0.45 * np.cos(1.7 * z)
  g = VGroup(Line([self.AX - self.W / 2, self.BASE, 0], [self.AX + self.W / 2, self.BASE, 0],
                  color=GHOST, stroke_width=2),
             Line([self.AX, self.BASE - 0.95, 0], [self.AX, self.BASE + 0.95, 0],
                  color=GHOST, stroke_width=2),
             self._curve_of(f, ACCENT_A, sw=4),
             self._curve_of(lambda z: f(-z), DIM, sw=2.5))
  return g.add(self._mid(1.05, "一個函數，跟它的鏡像", "a function and its reflection",
                         DIM, FS_TAG, x=3.70, w=4.6),
               self._mid(-1.10, "偶函數所成的子集是子空間，奇函數也是",
                         "the even functions form a subspace, and so do the odd",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.68, "而整個連續函數空間，正好是這兩個的直和",
                         "and the whole space of continuous functions is their direct sum",
                         ACCENT_A, FS_TAG, w=11.6))

 def _split_even_odd(self):
  f = lambda z: np.sin(z) + 0.45 * np.cos(1.7 * z)
  ev = lambda z: (f(z) + f(-z)) / 2
  od = lambda z: (f(z) - f(-z)) / 2
  # the split has to actually reconstitute f, or the picture is decoration
  zs = np.linspace(-2, 2, 40)
  assert max(abs(ev(z) + od(z) - f(z)) for z in zs) < 1e-9
  assert max(abs(ev(z) - ev(-z)) for z in zs) < 1e-9
  assert max(abs(od(z) + od(-z)) for z in zs) < 1e-9
  g = VGroup(Line([self.AX - self.W / 2, self.BASE, 0], [self.AX + self.W / 2, self.BASE, 0],
                  color=GHOST, stroke_width=2),
             Line([self.AX, self.BASE - 0.95, 0], [self.AX, self.BASE + 0.95, 0],
                  color=GHOST, stroke_width=2),
             self._curve_of(f, DIM, sw=2),
             self._curve_of(ev, ACCENT_B, sw=3.5),
             self._curve_of(od, ACCENT_C, sw=3.5))
  return g.add(self._mid(1.05, "平均起來：偶的部分", "the average: the even part",
                         ACCENT_B, FS_TAG, x=3.70, w=4.6),
               self._mid(0.35, "相減除以二：奇的部分", "half the difference: the odd part",
                         ACCENT_C, FS_TAG, x=3.70, w=4.6),
               self._mid(-1.10, "分解唯一，因為同時是偶又是奇的函數只有零",
                         "unique, because the only function both even and odd is zero",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.68, "指數函數的偶奇分量，正好是雙曲餘弦與雙曲正弦",
                         "the even and odd parts of the exponential are cosh and sinh",
                         ACCENT_A, FS_TAG, w=11.6))

 def _restate(self):
  g = VGroup()
  ox = -3.55
  cols = (ACCENT_B, ACCENT_C, WARN)
  for k in range(3):
   x = ox + k * 1.15
   g.add(Rectangle(width=0.86, height=0.52, color=cols[k], stroke_width=2)
         .move_to([x, 0.62, 0]),
         Text(f"α{k + 1}", font_size=FS_TAG - 2, color=cols[k]).move_to([x, 0.62, 0]))
   if k < 2:
    g.add(Text("+", font_size=FS_TAG, color=DIM).move_to([x + 0.58, 0.62, 0]))
  g.add(Text("=", font_size=FS_TAG + 2, color=DIM).move_to([ox + 2.88, 0.62, 0]),
        Text("0", font_size=FS_TAG + 2, color=ACCENT_A).move_to([ox + 3.42, 0.62, 0]),
        self._arr([ox + 1.15, 0.28, 0], [ox + 1.15, -0.28, 0], ACCENT_A, sw=2.5, tl=0.13))
  for k in range(3):
   x = ox + k * 1.15
   g.add(Rectangle(width=0.86, height=0.52, color=DIM, stroke_width=2).move_to([x, -0.62, 0]),
         Text("0", font_size=FS_TAG, color=DIM).move_to([x, -0.62, 0]))
  return g.add(self._mid(0.62, "各取一個，加起來是零", "one from each, summing to zero",
                         DIM, FS_TAG, x=3.05, w=5.4),
               self._mid(-0.62, "那麼每一個都必須是零", "then every one of them is zero",
                         ACCENT_A, FS_TAG, x=3.05, w=5.4),
               self._mid(-1.62, "因為嵌射等價於零空間只有零向量",
                         "since injectivity is the same as having only zero in the null space",
                         DIM, FS_TAG, w=11.6))

 def _two(self):
  g = VGroup()
  for cx, ok in ((-3.05, True), (3.05, False)):
   a = Ellipse(width=2.30, height=1.55, color=ACCENT_B, stroke_width=2.5,
               fill_color=ACCENT_B, fill_opacity=0.10)
   b = Ellipse(width=2.30, height=1.55, color=ACCENT_C, stroke_width=2.5,
               fill_color=ACCENT_C, fill_opacity=0.10)
   if ok:
    a.move_to([cx - 1.02, 0.25, 0]); b.move_to([cx + 1.02, 0.25, 0])
    g.add(a, b, Dot([cx, 0.25, 0], radius=0.09, color=ACCENT_A),
          Text("0", font_size=FS_TAG - 2, color=ACCENT_A).move_to([cx, -0.16, 0]))
   else:
    a.move_to([cx - 0.55, 0.25, 0]); b.move_to([cx + 0.55, 0.25, 0])
    g.add(a, b, Ellipse(width=1.20, height=1.20, color=WARN, stroke_width=2.5,
                        fill_color=WARN, fill_opacity=0.30).move_to([cx, 0.25, 0]))
   g.add(self._mid(-0.95, "只交於零向量：獨立" if ok else "交集不只有零：不獨立",
                   "meeting only at zero: independent" if ok else "a bigger overlap: not independent",
                   ACCENT_A if ok else WARN, FS_TAG, x=cx, w=4.6))
  return g.add(self._mid(-1.68, "所以 V 是兩個子空間的直和，若且唯若 V 是它們的和、而且只交於零",
                         "so V is their direct sum exactly when V is their sum and they meet only at zero",
                         DIM, FS_TAG, w=11.9))

 # ── beats 9-10: complements, and the book's Fig. 1.9 ─────────────
 COMPS = (np.array([0.30, 0.42, 1.15]), np.array([-0.85, 0.20, 1.05]),
          np.array([0.55, -0.75, 1.30]))

 def _not_unique(self):
  """One plane, three different lines each of which completes it. Every one
  is checked to be off the plane, since a line inside it would not be a
  complement at all."""
  g = VGroup(self._plane(), Dot(_p(np.zeros(3), self.ORG, self.S), radius=0.065, color=INK))
  cols = (ACCENT_A, ACCENT_C, WARN)
  for k, d in enumerate(self.COMPS):
   assert abs(float(d[2])) > 0.4, "a complement of the plane must leave it"
   g.add(Line(_p(-0.95 * d, self.ORG, self.S), _p(0.95 * d, self.ORG, self.S),
              color=cols[k], stroke_width=3))
  return g.add(self._mid(1.05, "同一個平面", "one and the same plane",
                         ACCENT_B, FS_TAG, x=3.05, w=5.5),
               self._mid(0.20, "三條不同的直線", "three different lines",
                         DIM, FS_TAG, x=3.05, w=5.5),
               self._mid(-0.65, "每一條都補得起來", "and every one of them completes it",
                         ACCENT_A, FS_TAG, x=3.05, w=5.5),
               self._mid(-1.62, "所以補空間通常不唯一——除非那個子空間是零或全空間",
                         "so a complement is not unique, unless the subspace is trivial or everything",
                         WARN, FS_TAG, w=11.9))

 def _fig19(self):
  """Book Fig. 1.9: a vector split into its part in the plane and its part
  on the line."""
  g = VGroup(self._plane(), Dot(_p(np.zeros(3), self.ORG, self.S), radius=0.065, color=INK))
  d = self.COMPS[0]
  eta = np.array([0.95, -0.70, 0.0])
  lam = 0.72 * d
  o3 = _p(np.zeros(3), self.ORG, self.S)
  g.add(Line(_p(-0.95 * d, self.ORG, self.S), _p(1.15 * d, self.ORG, self.S),
             color=ACCENT_A, stroke_width=3),
        self._arr(o3, _p(eta, self.ORG, self.S), ACCENT_B, sw=3.5, tl=0.16),
        self._arr(_p(eta, self.ORG, self.S), _p(eta + lam, self.ORG, self.S),
                  ACCENT_A, sw=3.5, tl=0.16),
        self._arr(o3, _p(eta + lam, self.ORG, self.S), ACCENT_C, sw=4.5, tl=0.20),
        Text("η", font_size=FS_TAG, color=ACCENT_B)
        .move_to(_p(eta, self.ORG, self.S) + np.array([0.10, -0.28, 0])),
        Text("λ", font_size=FS_TAG, color=ACCENT_A)
        .move_to(_p(eta + lam, self.ORG, self.S) + np.array([0.28, 0.10, 0])),
        Text("N", font_size=FS_TAG, color=ACCENT_B)
        .move_to(_p(np.array([-1.15, 1.15, 0]), self.ORG, self.S)))
  return g.add(self._mid(1.05, "一個平面，加一條不在它裡面的直線",
                         "a plane, and a line not lying in it",
                         DIM, FS_TAG, x=3.05, w=5.5),
               self._mid(0.10, "每個向量唯一地拆成兩份", "every vector splits in exactly one way",
                         ACCENT_C, FS_TAG, x=3.05, w=5.5),
               self._mid(-1.62, "而在三維空間裡，這是唯一一種非平凡的互補配對",
                         "and in three-space those are the only nontrivial complementary pairs",
                         ACCENT_A, FS_TAG, w=11.8))

 def stage(self):
  iso, ide, sm = self._iso(), self._identities(), self._sum_map()
  bo, un = self._both(), self._unique()
  eo, sp, rs = self._even_odd(), self._split_even_odd(), self._restate()
  tw, nu, f19 = self._two(), self._not_unique(), self._fig19()

  return [([iso], []), ([ide], [iso]), ([sm], [ide]), ([bo], [sm]),
          ([un], [bo]), ([eo], [un]), ([sp], [eo]), ([rs], [sp]),
          ([tw], [rs]), ([nu], [tw]), ([f19], [nu])]


AdvCalcE14ZH, AdvCalcE14EN = make(AdvCalcE14Base, "14", prefix="AdvCalcE")
