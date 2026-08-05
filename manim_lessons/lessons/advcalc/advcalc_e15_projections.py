"""advcalc E15 — Chapter 1, section 5, second part (book pp. 58-61): the
projection operators, Theorems 5.1 and 5.2, and idempotence.

The result the section is built toward is that being idempotent and being a
projection are the same thing, so beat 7 draws idempotence as what it actually
is -- applying the map a second time moves nothing -- rather than restating the
equation sitting in the formula bar. Beat 4 exists because the book itself
stops to warn that the word "projection" now has three unrelated-looking
meanings in play, and three small pictures settle that faster than a sentence.
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


class AdvCalcE15Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 15

 MODE_LABEL = {
  0: {"zh": "獨立可以疊起來", "en": "independence stacks"},
  1: {"zh": "直和可以一層一層拆", "en": "direct sums come apart in layers"},
  2: {"zh": "同構有反函數，接上投影", "en": "invert the isomorphism, then project"},
  3: {"zh": "送到它在第 j 個子空間的那一份", "en": "to its own share in the jth subspace"},
  4: {"zh": "「投影」在這本書有三個意思", "en": "three things called projection"},
  5: {"zh": "值域、相接為零、加起來是恆等", "en": "ranges, zero composites, summing to I"},
  6: {"zh": "反過來也成立", "en": "and the converse holds"},
  7: {"zh": "冪等：再做一次什麼也沒動", "en": "idempotent: doing it twice moves nothing"},
  8: {"zh": "冪等，就是投影", "en": "idempotent is the same as projection"},
  9: {"zh": "設 Q 是恆等減去 P", "en": "set Q to be the identity minus P"},
  10: {"zh": "一對互補投影", "en": "a pair of complementary projections"},
 }

 ORG = np.array([-2.75, -0.35, 0.0])
 S = 0.85
 KDIR = np.array([0.30, 0.42, 1.15])

 def _plane(self, org=None, s=None, color=ACCENT_B, op=0.13, half=1.35):
  org = self.ORG if org is None else org
  s = self.S if s is None else s
  quad = [np.array([sx * half, sy * half, 0.0]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
  return Polygon(*[_p(v, org, s) for v in quad], color=color, stroke_width=2.5,
                 fill_color=color, fill_opacity=op)

 # ── beats 0-1: layered independence ──────────────────────────────
 def _layered(self):
  # the outer label sits above the outer ellipse, so the ellipse has to clear
  # the band by its own label height, not just by its own edge
  g = VGroup(Ellipse(width=5.40, height=2.05, color=DIM, stroke_width=2.5)
             .move_to([-2.35, -0.05, 0]),
             Text("V", font_size=FS_TAG, color=DIM).move_to([-2.35, 1.12, 0]),
             Ellipse(width=1.70, height=1.35, color=ACCENT_B, stroke_width=2.5,
                     fill_color=ACCENT_B, fill_opacity=0.12).move_to([-4.05, -0.05, 0]),
             Text("V₁", font_size=FS_TAG - 2, color=ACCENT_B).move_to([-4.05, -0.05, 0]),
             Ellipse(width=3.10, height=1.58, color=ACCENT_A, stroke_width=2.5)
             .move_to([-1.55, -0.05, 0]),
             Text("V₀", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-1.55, 0.78, 0]))
  for k, x in enumerate((-2.45, -1.55, -0.65)):
   g.add(Ellipse(width=0.80, height=0.86, color=ACCENT_C, stroke_width=2)
         .move_to([x, -0.15, 0]),
         Text(f"V{k + 2}", font_size=FS_TAG - 5, color=ACCENT_C).move_to([x, -0.15, 0]))
  return g.add(self._mid(0.85, "V₁ 與 V₀ 獨立", "the two are independent",
                         ACCENT_B, FS_TAG, x=3.55, w=4.9),
               self._mid(0.05, "V₀ 又分解成獨立的一族", "and the second splits independently",
                         ACCENT_C, FS_TAG, x=3.55, w=4.9),
               self._mid(-0.75, "那麼合起來也獨立", "then all of them together are independent",
                         ACCENT_A, FS_TAG, x=3.55, w=4.9),
               self._mid(-1.62, "這條引理技術性，但等一下的定理要靠它",
                         "a technical lemma, but the theorems below lean on it",
                         DIM, FS_TAG, w=11.6))

 def _peel(self):
  g = VGroup()
  ox = -3.85
  for k, (lab, col) in enumerate((("V", ACCENT_A), ("V₁ ⊕ V₀", ACCENT_B),
                                  ("V₁ ⊕ V₂ ⊕ …", ACCENT_C))):
   y = 0.72 - k * 0.78
   g.add(Rectangle(width=3.60, height=0.60, color=col, stroke_width=2.5).move_to([ox, y, 0]),
         Text(lab, font_size=FS_TAG, color=col).move_to([ox, y, 0]))
   if k < 2:
    g.add(self._arr([ox, y - 0.34, 0], [ox, y - 0.46, 0], DIM, sw=2, tl=0.10))
  return g.add(self._mid(0.72, "先拆成兩塊", "split it in two first",
                         DIM, FS_TAG, x=2.55, w=5.4),
               self._mid(-0.06, "再把其中一塊拆下去", "then split one of them further",
                         DIM, FS_TAG, x=2.55, w=5.4),
               self._mid(-0.84, "結果還是一個直和", "and the result is still a direct sum",
                         ACCENT_A, FS_TAG, x=2.55, w=5.4),
               self._mid(-1.62, "所以直和可以一層一層拆下去",
                         "so direct sums can be taken apart a layer at a time",
                         DIM, FS_TAG, w=11.6))

 # ── beats 2-3: what a projection is ──────────────────────────────
 def _build(self):
  g = VGroup()
  boxes = ((-4.05, "V", ACCENT_A), (-0.65, "∏ Vᵢ", DIM), (2.75, "Vⱼ", ACCENT_B))
  for x, lab, col in boxes:
   g.add(Rectangle(width=1.60, height=0.80, color=col, stroke_width=2.5).move_to([x, 0.35, 0]),
         Text(lab, font_size=FS_TAG + 1, color=col).move_to([x, 0.35, 0]))
  g.add(self._arr([-3.20, 0.35, 0], [-1.50, 0.35, 0], ACCENT_A, sw=3, tl=0.15),
        Text("π ⁻¹", font_size=FS_TAG - 1, color=ACCENT_A).move_to([-2.35, 0.72, 0]),
        self._arr([0.20, 0.35, 0], [1.90, 0.35, 0], ACCENT_B, sw=3, tl=0.15),
        Text("πⱼ", font_size=FS_TAG - 1, color=ACCENT_B).move_to([1.05, 0.72, 0]),
        self._arr([-4.05, -0.15, 0], [2.75, -0.15, 0], ACCENT_C, sw=3.5, tl=0.17),
        Text("Pⱼ", font_size=FS_TAG + 1, color=ACCENT_C).move_to([-0.65, -0.52, 0]))
  return g.add(self._mid(-1.10, "V 是直和時，那個映射是同構，所以有反函數",
                         "when V is the direct sum, that map is an isomorphism, so it inverts",
                         DIM, FS_TAG, w=11.6),
               self._mid(-1.70, "反函數接上第 j 個座標投影，就得到 V 到 Vⱼ 的映射",
                         "and composing the jth coordinate projection after it lands in the jth subspace",
                         ACCENT_C, FS_TAG, w=11.9))

 def _component(self):
  o = np.array([-2.95, -0.60, 0.0])
  u, v = np.array([1.25, 0.30, 0.0]), np.array([0.32, 1.05, 0.0])
  a, b = 1.45 * u, 0.95 * v
  g = VGroup(Line(o - 0.50 * u, o + 2.35 * u, color=GHOST, stroke_width=2),
             Line(o - 0.40 * v, o + 1.60 * v, color=GHOST, stroke_width=2),
             self._arr(o, o + a + b, ACCENT_A, sw=4.5, tl=0.20),
             self._arr(o, o + a, ACCENT_B, sw=3.5, tl=0.16),
             self._dash(o + a, o + a + b, GHOST, n=7),
             Dot(o, radius=0.06, color=INK),
             Text("α", font_size=FS_TAG, color=ACCENT_A)
             .move_to(o + a + b + np.array([0.24, 0.16, 0])),
             Text("Pⱼ ( α )", font_size=FS_TAG - 1, color=ACCENT_B)
             .move_to(o + a + np.array([0.20, -0.32, 0])),
             Text("Vⱼ", font_size=FS_TAG - 2, color=DIM)
             .move_to(o + 2.35 * u + np.array([0.22, -0.18, 0])))
  return g.add(self._mid(1.05, "每個向量唯一地拆成各子空間各一項",
                         "every vector splits uniquely, one term per subspace",
                         DIM, FS_TAG, x=3.15, w=5.5),
               self._mid(-0.15, "投影就送出第 j 個那一項", "the projection returns the jth term",
                         ACCENT_B, FS_TAG, x=3.15, w=5.5),
               self._mid(-1.62, "書上把它叫做 α 的第 j 個分量",
                         "the book calls that the jth component of alpha",
                         DIM, FS_TAG, w=11.4))

 def _three_meanings(self):
  """The book stops to flag the collision, so the episode does too."""
  g = VGroup()
  ox = -4.05
  # 1: coordinate projection on a product
  g.add(Rectangle(width=0.95, height=1.35, color=DIM, stroke_width=2).move_to([ox, 0.30, 0]))
  for k, y in enumerate((0.72, 0.30, -0.12)):
   g.add(Rectangle(width=0.70, height=0.34, color=ACCENT_B if k == 1 else GHOST,
                   stroke_width=1.8).move_to([ox, y, 0]))
  g.add(self._arr([ox + 0.55, 0.30, 0], [ox + 1.05, 0.30, 0], ACCENT_B, sw=2, tl=0.10))
  # 2: projection onto a quotient
  cx = -0.75
  for k in (-1, 0, 1):
   g.add(Line([cx - 0.72, 0.30 + k * 0.34, 0], [cx + 0.42, 0.30 + k * 0.34, 0],
              color=ACCENT_C, stroke_width=2))
  g.add(self._arr([cx + 0.62, 0.30, 0], [cx + 1.10, 0.30, 0], ACCENT_C, sw=2, tl=0.10),
        Dot([cx + 1.30, 0.30, 0], radius=0.06, color=ACCENT_C))
  # 3: projection along a complement
  ox3 = 3.10
  o = np.array([ox3 - 0.85, -0.10, 0.0])
  u, v = np.array([1.30, 0.0, 0.0]), np.array([0.30, 0.85, 0.0])
  g.add(Line(o, o + 1.55 * u, color=GHOST, stroke_width=2),
        self._arr(o, o + u + v, ACCENT_A, sw=3, tl=0.14),
        self._arr(o, o + u, WARN, sw=3, tl=0.14),
        self._dash(o + u, o + u + v, GHOST, n=6))
  for cx2, zh, en, col in ((ox + 0.20, "積空間", "on a product", ACCENT_B),
                           (cx + 0.25, "商空間", "onto a quotient", ACCENT_C),
                           (ox3, "沿補空間", "along a complement", WARN)):
   g.add(self._mid(-1.05, zh, en, col, FS_TAG, x=cx2, w=3.3))
  return g.add(self._mid(-1.70, "三個都叫投影，互相有關但確實不同，靠上下文分辨",
                         "all three are called projection: related, but distinct, and context settles it",
                         DIM, FS_TAG, w=11.9))

 # ── beats 5-6: the two theorems ──────────────────────────────────
 def _thm(self, forward):
  left = (("R ( Pᵢ )  =  Vᵢ", ACCENT_B), ("Pᵢ ∘ Pⱼ  =  0", WARN), ("Σ Pᵢ  =  I", ACCENT_A))
  g = VGroup()
  for k, (s, col) in enumerate(left):
   y = 0.72 - k * 0.70
   g.add(Rectangle(width=3.10, height=0.54, color=col, stroke_width=2.5).move_to([-3.15, y, 0]),
         Text(s, font_size=FS_TAG, color=col).move_to([-3.15, y, 0]))
  g.add(Rectangle(width=3.00, height=0.72, color=ACCENT_A, stroke_width=2.5)
        .move_to([2.55, 0.02, 0]),
        Text("V  =  ⊕ Vᵢ", font_size=FS_TAG + 1, color=ACCENT_A).move_to([2.55, 0.02, 0]))
  if forward:
   g.add(self._arr([0.85, 0.02, 0], [-1.45, 0.02, 0], ACCENT_A, sw=3, tl=0.15))
  else:
   g.add(self._arr([-1.45, 0.02, 0], [0.85, 0.02, 0], ACCENT_A, sw=3, tl=0.15))
  return g

 def _forward(self):
  return self._thm(True).add(
   self._mid(-1.25, "直和給出的那些投影，滿足這三條",
             "the projections coming from a direct sum satisfy all three",
             DIM, FS_TAG, w=11.6),
   self._mid(-1.68, "正是積空間那組等式在 V 裡的倒影",
             "which is the product-space identities reflected in V",
             ACCENT_A, FS_TAG, w=11.6))

 def _converse(self):
  return self._thm(False).add(
   self._mid(-1.25, "反過來：只要滿足後兩條，把值域取出來",
             "conversely: assume the last two, and take the ranges",
             DIM, FS_TAG, w=11.6),
   self._mid(-1.68, "V 就是這些值域的直和，而它們正好是對應的投影",
             "V is their direct sum and the maps are the corresponding projections",
             ACCENT_A, FS_TAG, w=11.6))

 # ── beats 7-10: idempotence ──────────────────────────────────────
 def _idempotent(self):
  """Applying P a second time moves nothing: the second arrow has to land on
  the first arrow's tip, so the picture is drawn from that identity."""
  o = np.array([-3.15, -0.65, 0.0])
  u, v = np.array([1.30, 0.0, 0.0]), np.array([0.34, 1.05, 0.0])
  a = o + 1.45 * u + 0.95 * v
  Pa = o + 1.45 * u
  PPa = Pa                                       # P is the identity on its range
  assert float(np.linalg.norm(PPa - Pa)) < 1e-12
  g = VGroup(Line(o - 0.45 * u, o + 2.45 * u, color=ACCENT_B, stroke_width=3),
             self._arr(o, a, ACCENT_A, sw=3.5, tl=0.16),
             self._dash(a, Pa, GHOST, n=7),
             self._arr(o, Pa, WARN, sw=4.5, tl=0.20),
             Dot(o, radius=0.06, color=INK), Dot(Pa, radius=0.10, color=WARN),
             Text("α", font_size=FS_TAG, color=ACCENT_A)
             .move_to(a + np.array([0.24, 0.14, 0])),
             Text("P α", font_size=FS_TAG - 1, color=WARN)
             .move_to(Pa + np.array([0.16, -0.32, 0])),
             Text("R ( P )", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + 2.45 * u + np.array([0.36, 0.20, 0])))
  return g.add(self._mid(1.05, "再做一次 P", "apply P a second time",
                         DIM, FS_TAG, x=3.35, w=5.1),
               self._mid(0.10, "點完全沒有動", "and the point does not move",
                         WARN, FS_TAG, x=3.35, w=5.1),
               self._mid(-0.80, "因為它在值域上就是恆等", "since it is the identity on its range",
                         ACCENT_B, FS_TAG, x=3.35, w=5.1),
               self._mid(-1.62, "而它的零空間，正好是其他那些子空間的和",
                         "and its null space is the sum of all the other subspaces",
                         DIM, FS_TAG, w=11.6))

 def _same_thing(self):
  g = VGroup()
  for cx, zh, en, col in ((-2.85, "冪等", "idempotent", ACCENT_B),
                          (2.85, "是一個投影", "is a projection", ACCENT_A)):
   g.add(Rectangle(width=3.60, height=0.95, color=col, stroke_width=2.5).move_to([cx, 0.45, 0]),
         self._mid(0.45, zh, en, col, FS_TAG + 1, x=cx, w=3.3))
  g.add(self._arr([-0.95, 0.65, 0], [0.95, 0.65, 0], ACCENT_A, sw=3, tl=0.15),
        self._arr([0.95, 0.25, 0], [-0.95, 0.25, 0], ACCENT_B, sw=3, tl=0.15),
        Rectangle(width=5.20, height=0.62, color=ACCENT_C, stroke_width=2.5)
        .move_to([0.0, -0.70, 0]),
        self._mid(-0.70, "V  =  值域  ⊕  零空間", "V  =  range  ⊕  null space",
                  ACCENT_C, FS_TAG, x=0.0, w=4.9))
  return g.add(self._mid(-1.68, "所以「冪等」與「是一個投影」，講的是同一件事",
                         "so being idempotent and being a projection are one and the same",
                         ACCENT_A, FS_TAG, w=11.8))

 def _proof(self):
  rows = (("Q  =  I  −  P", ACCENT_C), ("P ∘ Q  =  P − P ∘ P", DIM),
          ("=  0", ACCENT_A), ("R ( Q )  =  N ( P )", ACCENT_B))
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   y = 0.85 - k * 0.62
   g.add(Rectangle(width=4.00, height=0.50, color=col, stroke_width=2 if k else 2.5)
         .move_to([-2.55, y, 0]),
         Text(s, font_size=FS_TAG, color=col).move_to([-2.55, y, 0]))
  return g.add(self._mid(0.85, "設 Q 是恆等減去 P", "set Q to be the identity minus P",
                         ACCENT_C, FS_TAG, x=2.95, w=5.4),
               self._mid(-0.15, "兩個相接就是零", "their composite is zero",
                         ACCENT_A, FS_TAG, x=2.95, w=5.4),
               self._mid(-1.01, "於是套用前一個定理", "so the previous theorem applies",
                         DIM, FS_TAG, x=2.95, w=5.4),
               self._mid(-1.68, "而 Q 的值域，正好就是 P 的零空間",
                         "and the range of Q is exactly the null space of P",
                         ACCENT_B, FS_TAG, w=11.6))

 def _complementary(self):
  o = np.array([-2.95, -0.45, 0.0])
  u, v = np.array([1.35, 0.0, 0.0]), np.array([0.32, 1.05, 0.0])
  a = o + 1.45 * u + 0.95 * v
  g = VGroup(Line(o - 0.40 * u, o + 2.35 * u, color=ACCENT_B, stroke_width=3),
             Line(o - 0.35 * v, o + 1.55 * v, color=ACCENT_C, stroke_width=3),
             self._arr(o, a, ACCENT_A, sw=4, tl=0.18),
             self._arr(o, o + 1.45 * u, ACCENT_B, sw=3.5, tl=0.16),
             self._arr(o, o + 0.95 * v, ACCENT_C, sw=3.5, tl=0.16),
             self._dash(o + 1.45 * u, a, GHOST, n=7),
             self._dash(o + 0.95 * v, a, GHOST, n=7),
             Dot(o, radius=0.06, color=INK),
             Text("P α", font_size=FS_TAG - 2, color=ACCENT_B)
             .move_to(o + 1.45 * u + np.array([0.14, -0.30, 0])),
             Text("Q α", font_size=FS_TAG - 2, color=ACCENT_C)
             .move_to(o + 0.95 * v + np.array([-0.36, 0.14, 0])))
  return g.add(self._mid(1.05, "相加是恆等", "they sum to the identity",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(0.10, "兩邊相接都是零", "and compose to zero both ways",
                         DIM, FS_TAG, x=3.15, w=5.4),
               self._mid(-0.80, "這樣一對叫互補投影", "such a pair is called complementary",
                         ACCENT_A, FS_TAG, x=3.15, w=5.4),
               self._mid(-1.68, "最後書上補了個細節：嚴格說要引進一個恆等注入，上域才對得上",
                         "the book closes on a fine point: an identity injection is needed for the codomains to match",
                         DIM, FS_TAG, w=11.9))

 def stage(self):
  la, pe = self._layered(), self._peel()
  bu, co, tm = self._build(), self._component(), self._three_meanings()
  fw, cv = self._forward(), self._converse()
  idm, st, pf, cm = self._idempotent(), self._same_thing(), self._proof(), self._complementary()

  return [([la], []), ([pe], [la]), ([bu], [pe]), ([co], [bu]),
          ([tm], [co]), ([fw], [tm]), ([cv], [fw]), ([idm], [cv]),
          ([st], [idm]), ([pf], [st]), ([cm], [pf])]


AdvCalcE15ZH, AdvCalcE15EN = make(AdvCalcE15Base, "15", prefix="AdvCalcE")
