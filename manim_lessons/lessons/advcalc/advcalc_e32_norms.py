"""advcalc E32 -- chapter 3, section 2, first part (book pp. 121-123): the three
properties of the absolute value the proofs actually used, why size is not
unique once there is more than one dimension, the three axioms of a norm, the
notation and the geometric triangle inequality, the usual norms on a Cartesian
space and on a space of continuous functions, which of them are easy and which
wait for chapter 5, Lemma 2.1, and the uniform norm on the bounded functions of
an arbitrary set. E33 takes pp. 123-125, balls and open sets.

The two-norms example is computed rather than asserted. TALL and WIDE are two
piecewise linear functions on [0, 1] of this episode's own making, and the
module evaluates both norms on both of them exactly, in fractions, so beat 2's
claim -- that one is large in the maximum and small in the integral while the
other is the reverse -- is checked before it is drawn, and the bars in the
picture are drawn to the numbers that came out.
"""
import pathlib, sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

# Two functions on [0, 1], each given by its corner points. The spike is tall
# and thin; the plateau is low and broad.
TALL = ((Fraction(0), Fraction(0)), (Fraction(2, 5), Fraction(0)),
        (Fraction(1, 2), Fraction(1)), (Fraction(3, 5), Fraction(0)),
        (Fraction(1), Fraction(0)))
WIDE = ((Fraction(0), Fraction(1, 4)), (Fraction(1), Fraction(1, 4)))


def _peak(pts):
 return max(y for _, y in pts)


def _area(pts):
 """Exact area under a nonnegative piecewise linear graph: trapezoids."""
 return sum((b - a) * (ya + yb) / 2 for (a, ya), (b, yb) in zip(pts, pts[1:]))


PEAKS = (_peak(TALL), _peak(WIDE))
AREAS = (_area(TALL), _area(WIDE))

# ── what beat 2 claims, checked rather than trusted ───────────────────────
assert PEAKS[0] > PEAKS[1], "the spike must be the taller of the two"
assert AREAS[0] < AREAS[1], "and the one with the smaller area, or there is no example"
assert all(y >= 0 for pts in (TALL, WIDE) for _, y in pts), "the picture assumes both are positive"

FMT = lambda v: (str(Fraction(v).numerator) if Fraction(v).denominator == 1
                 else f"{Fraction(v).numerator}/{Fraction(v).denominator}")


class AdvCalcE32Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 32

 MODE_LABEL = {
  0: {"zh": "絕對值只被用到三件事",
      "en": "the absolute value was used for exactly three things"},
  1: {"zh": "「多大」不只一種答案", "en": "how large has more than one answer"},
  2: {"zh": "兩種大小不會一起變小", "en": "the two sizes do not shrink together"},
  3: {"zh": "範數的三條公理", "en": "the three axioms of a norm"},
  4: {"zh": "賦範線性空間與距離", "en": "a normed linear space, and distance"},
  5: {"zh": "座標空間上最常用的三個", "en": "the three in common use on a Cartesian space"},
  6: {"zh": "同樣三個，換成函數空間", "en": "the same three on a space of functions"},
  7: {"zh": "哪個好證，哪個要等第 5 章",
      "en": "which are easy, and which waits for chapter five"},
  8: {"zh": "引理 2.1：把範數搬到別的空間",
      "en": "lemma 2.1: carrying a norm to another space"},
  9: {"zh": "有界函數構成一個向量空間",
      "en": "the bounded functions form a vector space"},
  10: {"zh": "均勻範數：用最小上界定義", "en": "the uniform norm, defined by a least upper bound"},
 }

 # ── drawing ───────────────────────────────────────────────────────
 def _graph(self, ox, oy, pts, col, w=2.30, h=1.10, fill=False):
  """A piecewise linear graph over [0, 1], drawn to the numbers given."""
  X = lambda x: ox + float(x) * w
  Y = lambda y: oy + float(y) * h
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + w + 0.16, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.10, 0], [ox, oy + h + 0.20, 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(x), Y(y), 0] for x, y in pts], col, sw=3))
  if fill:
   for k in range(1, 24):
    x = Fraction(k, 24)
    y = next(ya + (yb - ya) * (x - a) / (b - a)
             for (a, ya), (b, yb) in zip(pts, pts[1:]) if a <= x <= b)
    g.add(Line([X(x), oy, 0], [X(x), Y(y), 0], color=col, stroke_width=1.2))
  return g, X, Y

 # ── beats ─────────────────────────────────────────────────────────
 def _three_things(self):
  rows = (("| x |  >  0        ( x ≠ 0 )", ACCENT_C, "非零的東西量出正數",
           "a nonzero thing measures positive"),
          ("| x y |  =  | x | | y |", WARN, "縮放乘進去",
           "scaling passes through"),
          ("| x + y |  ≤  | x | + | y |", ACCENT_A, "三角不等式",
           "the triangle inequality"))
  g = VGroup()
  for k, (sym, col, zh, en) in enumerate(rows):
   y = 0.86 - k * 0.72
   g.add(self._box(-2.60, y, sym, col, w=5.60, h=0.62, size=FS_TAG),
         self._mid(y, zh, en, col, FS_TAG, x=3.40, w=4.60))
  return g.add(self._mid(-1.20, "上一節的每一個估計，用到的就只有這三條",
                         "every estimate in the last section used only these three",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "既然只用到這三條，就把這三條抽出來當定義",
                         "since only these were used, take them as the definition",
                         ACCENT_B, FS_TAG, w=11.9))

 def _two_answers(self):
  g = VGroup()
  gg, X, Y = self._graph(-4.60, -0.10, TALL, ACCENT_C, fill=False)
  g.add(gg, self._dash([X(0), Y(PEAKS[0]), 0], [X(1), Y(PEAKS[0]), 0], ACCENT_C, n=10, sw=1.4),
        Text("max", font_size=FS_TAG - 4, color=ACCENT_C).move_to([X(1) + 0.44, Y(PEAKS[0]), 0]))
  gg2, X2, Y2 = self._graph(0.90, -0.10, TALL, WARN, fill=True)
  g.add(gg2, Text("∫", font_size=FS_TAG + 2, color=WARN)
        .move_to([X2(1) + 0.44, Y2(0.20), 0]))
  return g.add(self._mid(-0.68, "同一個函數，兩個都合理的「多大」",
                         "one function, two reasonable answers to how large",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.12, "曲線的最高點，還有曲線底下的面積",
                         "the highest point of the curve, and the area beneath it",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.56, "一維時沒有這個問題：絕對值就是唯一的答案",
                         "in one dimension the question does not arise: the absolute value is the answer",
                         ACCENT_C, FS_TAG, w=11.9))

 def _not_together(self):
  g = VGroup()
  for ox, pts, col, zh, en in ((-4.90, TALL, ACCENT_C, "又高又細", "tall and thin"),
                              (0.40, WIDE, WARN, "又低又長", "low and broad")):
   gg, X, Y = self._graph(ox, -0.05, pts, col, fill=True)
   g.add(gg, self._mid(-0.46, zh, en, col, FS_TAG - 1, x=ox + 1.15, w=2.40))
  rows = ((-0.92, f"max  =  {FMT(PEAKS[0])}        ∫  =  {FMT(AREAS[0])}", ACCENT_C, -3.30),
          (-0.92, f"max  =  {FMT(PEAKS[1])}        ∫  =  {FMT(AREAS[1])}", WARN, 2.60))
  for y, s, col, x in rows:
   g.add(self._sym(y, s, col, FS_TAG - 1, x=x, w=4.40))
  return g.add(self._mid(-1.36, "左邊最高點大、面積小；右邊剛好相反",
                         "the left is large in the maximum and small in the integral; the right reverses it",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "兩個數都是照著這兩條折線實際算出來的",
                         "both numbers were computed from the two graphs actually drawn",
                         DIM, FS_TAG, w=11.9))

 def _axioms(self):
  rows = (("n1", "p ( α )  >  0        ( α ≠ 0 )", ACCENT_C, "正性", "positivity"),
          ("n2", "p ( x α )  =  | x |  p ( α )", WARN, "齊次性", "homogeneity"),
          ("n3", "p ( α + β )  ≤  p ( α ) + p ( β )", ACCENT_A, "三角不等式",
           "the triangle inequality"))
  g = VGroup()
  for k, (tag, sym, col, zh, en) in enumerate(rows):
   y = 0.86 - k * 0.72
   g.add(Text(tag, font_size=FS_TAG - 1, color=col).move_to([-5.40, y, 0]),
         self._box(-2.30, y, sym, col, w=5.60, h=0.62, size=FS_TAG),
         self._mid(y, zh, en, col, FS_TAG, x=3.60, w=4.40))
  return g.add(self._mid(-1.20, "跟絕對值那三條一模一樣，只是把數換成向量",
                         "the same three as before, with vectors in place of numbers",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "沒有要求「唯一」，所以同一個空間可以有很多種範數",
                         "nothing asks for uniqueness, so one space can carry many norms",
                         ACCENT_B, FS_TAG, w=11.9))

 def _nls(self):
  g = VGroup(self._box(-3.60, 0.98, "⟨ V , p ⟩", ACCENT_B, w=3.20, h=0.60, size=FS_TAG))
  ox, oy = -3.60, -0.30
  pts = {"ξ": (ox - 1.30, oy + 0.55), "η": (ox + 1.35, oy + 0.72), "ζ": (ox + 0.35, oy - 0.62)}
  for name, (x, y) in pts.items():
   g.add(Text(name, font_size=FS_TAG - 1, color=DIM).move_to([x, y + 0.28, 0]))
  keys = list(pts)
  for a, b, col in ((0, 2, ACCENT_A), (0, 1, ACCENT_C), (1, 2, ACCENT_C)):
   g.add(Line([*pts[keys[a]], 0], [*pts[keys[b]], 0], color=col, stroke_width=2.5))
  rows = ((0.98, "一個向量空間配上一個範數",
           "a vector space together with a norm", ACCENT_B),
          (0.32, "把 α − β 的範數當成距離",
           "read the norm of a difference as a distance", ACCENT_C),
          (-0.34, "第三條就是幾何的三角不等式",
           "and the third axiom is the triangle inequality of geometry", ACCENT_A))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.80, w=5.60))
  return g.add(self._mid(-1.24, "直的一邊不會比繞路長，這句話在任何賦範空間都成立",
                         "the direct side is never longer than the detour, in any normed space",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "範數通常寫成兩條直線包起來",
                         "the norm is usually written between double bars",
                         DIM, FS_TAG, w=11.9))

 def _cartesian(self):
  x = (Fraction(3), Fraction(-4))
  vals = (sum(abs(v) for v in x),
          None,
          max(abs(v) for v in x))
  rows = (("‖ x ‖ ₁", "Σ | x ᵢ |", ACCENT_C, FMT(vals[0])),
          ("‖ x ‖ ₂", "( Σ x ᵢ ² ) ¹ᐟ²", WARN, "5"),
          ("‖ x ‖ ∞", "max | x ᵢ |", ACCENT_A, FMT(vals[2])))
  g = VGroup(self._sym(1.02, f"x  =  ⟨ {FMT(x[0])} , {FMT(x[1])} ⟩", DIM, FS_TAG,
                       x=0.00, w=3.60))
  for k, (name, formula, col, val) in enumerate(rows):
   y = 0.34 - k * 0.62
   g.add(Text(name, font_size=FS_TAG, color=col).move_to([-4.60, y, 0]),
         self._box(-1.60, y, formula, col, w=3.80, h=0.54, size=FS_TAG - 1),
         Text(f"=  {val}", font_size=FS_TAG, color=col).move_to([1.60, y, 0]))
  return g.add(self._mid(0.34, "三個都量得出東西", "all three measure something",
                         DIM, FS_TAG, x=4.30, w=3.20),
               self._mid(-0.28, "量的卻不是同一件事", "but not the same thing",
                         DIM, FS_TAG, x=4.30, w=3.20),
               self._mid(-1.24, "同一個向量，三個範數給三個不同的數",
                         "one vector, three norms, three different numbers",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "下標二那個就是平常說的長度",
                         "the subscript two one is the length of ordinary geometry",
                         ACCENT_B, FS_TAG, w=11.9))

 def _functions(self):
  rows = (("‖ f ‖ ₁", "∫ ₐᵇ | f |", ACCENT_C, "面積", "area"),
          ("‖ f ‖ ₂", "( ∫ ₐᵇ | f | ² ) ¹ᐟ²", WARN, "平方積分", "the square integral"),
          ("‖ f ‖ ∞", "max | f |", ACCENT_A, "最高點", "the highest point"))
  g = VGroup()
  for k, (name, formula, col, zh, en) in enumerate(rows):
   y = 0.82 - k * 0.66
   g.add(Text(name, font_size=FS_TAG, color=col).move_to([-5.00, y, 0]),
         self._box(-2.20, y, formula, col, w=4.40, h=0.56, size=FS_TAG - 1),
         self._mid(y, zh, en, col, FS_TAG, x=2.60, w=3.20))
  g.add(self._arr([-3.90, 0.82, 0], [-3.90, -0.50, 0], DIM, sw=1.8, tl=0.09),
        self._mid(0.16, "求和換成積分", "sums become integrals", DIM, FS_TAG - 2,
                  x=5.00, w=2.20))
  return g.add(self._mid(-1.24, "同一組寫法，換一個向量空間就換一種意思",
                         "the same three recipes mean different things on a different space",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "函數空間是無限維的，這正是需要一般定義的地方",
                         "a function space is infinite dimensional, which is where a general definition earns itself",
                         ACCENT_B, FS_TAG, w=11.9))

 def _difficulty(self):
  rows = (("‖ · ‖ ₁", ACCENT_C, "直接驗就好", "checked directly"),
          ("‖ · ‖ ∞", ACCENT_A, "下一拍", "the next beat"),
          ("‖ · ‖ ₂", WARN, "三角不等式要靠內積，第 5 章",
           "its triangle inequality needs scalar products, chapter five"))
  g = VGroup()
  for k, (name, col, zh, en) in enumerate(rows):
   y = 0.90 - k * 0.62
   g.add(self._box(-3.90, y, name, col, w=2.40, h=0.58, size=FS_TAG),
         self._mid(y, zh, en, col, FS_TAG, x=2.20, w=6.20))
  return g.add(self._mid(-0.86, "實數線上絕對值是唯一的範數，差一個正的常數倍",
                         "on the line the absolute value is the only norm, up to a positive constant",
                         ACCENT_B, FS_TAG, w=11.9),
               self._mid(-1.24, "維度一多，選擇就跟著多——這正是要先講清楚的原因",
                         "more dimensions bring more choices, which is why this has to be settled first",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "後面會證明：有限維時這些選擇其實都等價",
                         "later: in finite dimensions all these choices turn out to be equivalent",
                         DIM, FS_TAG, w=11.9))

 def _lemma(self):
  g = VGroup(self._box(-4.20, 0.72, "V", ACCENT_B, w=1.60, h=0.60, size=FS_TAG),
             self._box(-1.10, 0.72, "W", ACCENT_C, w=1.60, h=0.60, size=FS_TAG),
             self._box(2.00, 0.72, "ℝ", WARN, w=1.60, h=0.60, size=FS_TAG),
             self._arr([-3.35, 0.72, 0], [-1.95, 0.72, 0], ACCENT_A, sw=2.5, tl=0.12),
             self._arr([-0.25, 0.72, 0], [1.15, 0.72, 0], ACCENT_A, sw=2.5, tl=0.12),
             Text("T", font_size=FS_TAG - 2, color=ACCENT_A).move_to([-2.65, 1.02, 0]),
             Text("p", font_size=FS_TAG - 2, color=ACCENT_A).move_to([0.45, 1.02, 0]))
  g.add(self._curve([[-4.20, 0.34, 0], [-4.20, -0.16, 0], [2.00, -0.16, 0], [2.00, 0.34, 0]],
                    DIM, sw=2),
        Text("p ∘ T", font_size=FS_TAG - 1, color=DIM).move_to([-1.10, -0.44, 0]))
  rows = ((-1.00, "T 要是單射，否則非零向量會量出零",
           "T has to be injective, or a nonzero vector would measure zero", WARN),
          (-1.42, "有了它，任何有限維空間都可以借一個範數來用",
           "with it, any finite dimensional space can borrow a norm", ACCENT_C))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, w=11.9))
  return g.add(self._mid(-1.78, "把 ℝⁿ 上現成的三個，經由座標同構搬過去就行了",
                         "carry the three ready-made ones on R-n across a coordinate isomorphism",
                         ACCENT_A, FS_TAG, w=11.9))

 def _bounded(self):
  ox, oy = -3.40, 0.30
  g = VGroup(Line([ox - 0.20, oy, 0], [ox + 3.00, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox, oy - 0.70, 0], [ox, oy + 1.00, 0], color=DIM, stroke_width=1.6))
  wig = [[ox + t * 0.10, oy + 0.42 + 0.26 * ((t % 7) - 3) / 3.0, 0] for t in range(31)]
  g.add(self._curve(wig, ACCENT_C, sw=2.5))
  for s, lab, col in ((0.74, "b", WARN), (-0.10, "− b", WARN)):
   g.add(self._dash([ox, oy + s, 0], [ox + 3.00, oy + s, 0], col, n=12, sw=1.4),
         Text(lab, font_size=FS_TAG - 4, color=col).move_to([ox + 3.28, oy + s, 0]))
  rows = ((0.90, "A 是任意一個非空集合，什麼結構都不必有",
           "A is any nonempty set, with no structure asked of it", ACCENT_A),
          (0.24, "ℬ ( A , ℝ ) 收集 A 上所有有界的函數",
           "B of A and R collects the bounded functions on A", ACCENT_C),
          (-0.42, "兩個有界的線性組合還是有界：界加起來就是新的界",
           "a combination of bounded functions is bounded: the bounds simply add", WARN))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.90, w=5.60))
  return g.add(self._mid(-1.24, "所以它是一個向量空間，接下來可以在上面放範數",
                         "so it is a vector space, and a norm can be put on it",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "注意這裡完全沒有用到 A 的任何性質",
                         "note that nothing about A has been used",
                         DIM, FS_TAG, w=11.9))

 def _uniform(self):
  ox, oy = -4.20, 0.30
  g = VGroup(Line([ox - 0.20, oy, 0], [ox + 3.20, oy, 0], color=DIM, stroke_width=1.6))
  wig = [[ox + t * 0.107, oy + 0.30 + 0.22 * ((t % 5) - 2) / 2.0, 0] for t in range(31)]
  g.add(self._curve(wig, ACCENT_C, sw=2.5))
  top = max(p[1] for p in wig)
  for s, lab, col in ((top + 0.30, "b", DIM), (top, "‖ f ‖ ∞", WARN)):
   g.add(self._dash([ox, s, 0], [ox + 3.20, s, 0], col, n=13, sw=1.4),
         Text(lab, font_size=FS_TAG - 4, color=col).move_to([ox + 3.58, s, 0]))
  rows = ((0.96, "每一個界都在上面", "every bound sits above", DIM),
          (0.34, "最小上界是壓得最低的那一條", "the least upper bound is the lowest of them",
           WARN),
          (-0.28, "所以它比任何界都小或相等",
           "so it is at most any bound at all", ACCENT_A))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=3.10, w=5.20))
  return g.add(self._mid(-1.24, "三角不等式就靠這一句：逐點放大成兩個範數的和，那個和是界",
                         "the triangle inequality is that one line: enlarge pointwise to the sum, which is a bound",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "值域換成任何賦範空間也一樣做。下一集：球與開集",
                         "the same works with any normed space as the target. Next time: balls and open sets",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  tt, ta, nt = self._three_things(), self._two_answers(), self._not_together()
  ax, nl, ca = self._axioms(), self._nls(), self._cartesian()
  fn, df = self._functions(), self._difficulty()
  lm, bd, un = self._lemma(), self._bounded(), self._uniform()
  return [([tt], []), ([ta], [tt]), ([nt], [ta]), ([ax], [nt]),
          ([nl], [ax]), ([ca], [nl]), ([fn], [ca]), ([df], [fn]),
          ([lm], [df]), ([bd], [lm]), ([un], [bd])]


AdvCalcE32ZH, AdvCalcE32EN = make(AdvCalcE32Base, "32", prefix="AdvCalcE")
