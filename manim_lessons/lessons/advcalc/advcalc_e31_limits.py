"""advcalc E31 -- the opening of chapter 3 (book p. 116) and section 1, the
review in R (pp. 117-120): what the differential calculus is about, why a norm
has to come first, the route through the chapter, the two theorems at the end
of it, the epsilon-delta definition, the punctured point, the order of the
three quantifiers, how delta follows epsilon, the two worked estimates, and the
least upper bound property. Page 120 onward is exercises 1.1 to 1.16, and E32
starts section 2 on p. 121.

The epsilon-delta pictures are drawn from a delta this module computes. For
f(x) = x squared at a = 1 the bound |x^2 - 1| = |x - 1||x + 1| gives a delta,
and `_delta` returns it; the assertions then sample the interval and check that
the band really does contain the graph, and that it would not for any larger
delta by much. So the two bands in beats 7 and 8 are a true picture of this
definition rather than two rectangles drawn to look convincing. The book's
Fig. 3.1 shows an abstract increasing graph; this is a concrete one of the
episode's own, per the copyright note in docs/PLAYBOOK.md section 8.
"""
import pathlib, sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17

A, L = Fraction(1), Fraction(1)                  # f(x) = x^2 at a = 1
f = lambda x: x * x
EPS = (Fraction(3, 10), Fraction(1, 10))         # the two bands beats 7 and 8 draw


def _delta(eps):
 """A delta that works, chosen the way the section chooses one: |x^2 - 1| is
 |x - 1| |x + 1|, so keeping |x - 1| under a half keeps |x + 1| under 5/2, and
 then |x - 1| < 2 eps / 5 does it. Kept as an exact fraction."""
 return min(Fraction(1, 2), Fraction(2, 5) * eps)


DELTAS = [_delta(e) for e in EPS]

# ── what the pictures claim, checked rather than trusted ──────────────────
for _e, _d in zip(EPS, DELTAS):
 _worst = max(abs(f(A + _d * Fraction(k, 40)) - L) for k in range(-40, 41))
 assert _worst < _e, "the delta band does not stay inside the epsilon band"
 assert abs(f(A + _d * 2) - L) > _e, "the delta is far looser than it needs to be"
assert EPS[1] < EPS[0] and DELTAS[1] < DELTAS[0], \
    "beat 8 says a narrower epsilon forces a narrower delta"

FMT = lambda v: (str(Fraction(v).numerator) if Fraction(v).denominator == 1
                 else f"{Fraction(v).numerator}/{Fraction(v).denominator}")


class AdvCalcE31Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 31

 MODE_LABEL = {
  0: {"zh": "微分學：用線性映射逼近非線性映射",
      "en": "the calculus: linear approximations to nonlinear mappings"},
  1: {"zh": "所以要先會量長度", "en": "so length has to be measured first"},
  2: {"zh": "這一章的路線", "en": "the route through this chapter"},
  3: {"zh": "章末的兩個大定理", "en": "the two large theorems at the end"},
  4: {"zh": "ε-δ 的定義", "en": "the epsilon-delta definition"},
  5: {"zh": "為什麼要挖掉 x = a 那一點",
      "en": "why the point x = a is left out"},
  6: {"zh": "三個量詞的順序不能動", "en": "the order of the three quantifiers is fixed"},
  7: {"zh": "ε 變窄，δ 跟著窄", "en": "narrower epsilon, narrower delta"},
  8: {"zh": "用法一：兩個一半", "en": "first use: two halves"},
  9: {"zh": "用法二：先把分母壓住", "en": "second use: pin the denominator first"},
  10: {"zh": "最小上界性質", "en": "the least upper bound property"},
 }

 # ── the picture the definition is about ───────────────────────────
 def _axes31(self, ox, oy, sx, sy, half=Fraction(45, 100)):
  """Axes with the graph of f, returned with the mapping into scene space.

  The curve is clipped to the drawn box rather than trusted to stay in it:
  x squared leaves the frame quickly, and bounds.py finds that out the moment
  the scale changes."""
  X = lambda x: ox + float(x - A) * sx
  Y = lambda y: oy + float(y - L) * sy
  g = VGroup(Line([ox - 1.85, oy - 1.05, 0], [ox + 1.85, oy - 1.05, 0],
                  color=DIM, stroke_width=1.6),
             Line([ox - 1.60, oy - 1.15, 0], [ox - 1.60, oy + 1.05, 0],
                  color=DIM, stroke_width=1.6))
  pts = []
  for k in range(-30, 31):
   x = A + Fraction(k, 30) * half
   y = Y(f(x))
   if abs(y - oy) <= 1.00 and abs(X(x) - ox) <= 1.72:
    pts.append([X(x), y, 0])
  g.add(self._curve(pts, ACCENT_B, sw=2.5))
  return g, X, Y

 def _band(self, ox, oy, sx, sy, eps, delta, X, Y, ecol, dcol):
  """The two bands the definition names, plus the point they meet at."""
  g = VGroup()
  for dy, col in ((eps, ecol), (-eps, ecol)):
   g.add(self._dash([ox - 1.60, Y(L + dy), 0], [ox + 1.60, Y(L + dy), 0],
                    col, n=14, sw=1.4))
  for dx, col in ((delta, dcol), (-delta, dcol)):
   g.add(self._dash([X(A + dx), oy - 1.05, 0], [X(A + dx), oy + 1.00, 0],
                    col, n=12, sw=1.4))
  return g.add(Dot([X(A), Y(L), 0], radius=0.06, color=WARN))

 # ── beats ─────────────────────────────────────────────────────────
 def _what(self):
  ox, oy, sx, sy = -3.30, 0.10, 1.90, 1.05
  g, X, Y = self._axes31(ox, oy, sx, sy)
  # the real tangent: f'(1) = 2, so the line rises twice as fast as x moves
  g.add(Line([X(A - Fraction(1, 2)), Y(L - Fraction(1, 1)), 0],
             [X(A + Fraction(1, 2)), Y(L + Fraction(1, 1)), 0],
             color=WARN, stroke_width=2.5),
        Dot([X(A), Y(L), 0], radius=0.06, color=WARN),
        Text("F", font_size=FS_TAG - 2, color=ACCENT_B).move_to([X(A) + 1.05, Y(L) + 0.75, 0]),
        Text("d F", font_size=FS_TAG - 2, color=WARN).move_to([X(A) + 1.15, Y(L) + 0.18, 0]))
  rows = ((0.92, "非線性的東西，在一點附近長得像線性的",
           "near a point a nonlinear map looks like a linear one", ACCENT_A),
          (0.28, "那個線性映射就叫這一點的微分",
           "that linear map is the differential there", WARN),
          (-0.36, "差多少，是這一章要精確說明的事",
           "how much they differ is what this chapter makes precise", ACCENT_C))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.80, w=5.60))
  return g.add(self._mid(-1.20, "前兩章已經把線性映射弄清楚了，剩下的是「逼近」這個詞",
                         "the first two chapters settled linear maps; what is left is the word approximation",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "整章的目標就是把這句話變成可以計算的東西",
                         "the whole chapter is about turning that sentence into something computable",
                         DIM, FS_TAG, w=11.9))

 def _why_norm(self):
  ox, oy = -3.20, 0.20
  g = VGroup(Line([ox - 1.90, oy - 0.90, 0], [ox + 1.90, oy - 0.90, 0],
                  color=DIM, stroke_width=1.6))
  pts = [[ox + t * 0.19, oy - 0.90 + 0.62 * (t * 0.19) - 0.10 * (t * 0.19) ** 3, 0]
         for t in range(-10, 11)]
  g.add(self._curve(pts, ACCENT_B, sw=2.5),
        Line([ox - 1.90, oy - 0.90 - 0.62 * 1.90, 0],
             [ox + 1.90, oy - 0.90 + 0.62 * 1.90, 0], color=WARN, stroke_width=2))
  x1 = ox + 1.45
  y_curve = oy - 0.90 + 0.62 * 1.45 - 0.10 * 1.45 ** 3
  y_line = oy - 0.90 + 0.62 * 1.45
  g.add(self._arr([x1, y_line, 0], [x1, y_curve, 0], ACCENT_C, sw=2, tl=0.09),
        Text("‖ · ‖", font_size=FS_TAG - 3, color=ACCENT_C).move_to([x1 + 0.52, (y_line + y_curve) / 2, 0]))
  rows = ((0.86, "誤差是一個向量，不是一個數",
           "the error is a vector, not a number", ACCENT_C),
          (0.22, "要說它小，就得先能量它的長度",
           "to call it small you must first measure its length", WARN),
          (-0.42, "向量空間上量長度的東西叫範數",
           "what measures length on a vector space is a norm", ACCENT_A))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.90, w=5.40))
  return g.add(self._mid(-1.20, "所以這一章從範數開始，而不是從微分開始",
                         "so the chapter opens with norms rather than with differentials",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "一維時範數就是絕對值，這也是第 1 節要複習的東西",
                         "in one dimension the norm is the absolute value, which section one reviews",
                         DIM, FS_TAG, w=11.9))

 def _route(self):
  stops = (("‖ · ‖", ACCENT_C, "範數", "norms"),
           ("lim", ACCENT_C, "連續", "continuity"),
           ("𝒪 , ϵ , o", DIM, "無窮小", "infinitesimals"),
           ("d F", WARN, "微分", "the differential"),
           ("∂ f / ∂ x", WARN, "偏導數", "partial derivatives"),
           ("[ ∂ f ᵢ / ∂ x ⱼ ]", ACCENT_A, "Jacobian 矩陣", "the Jacobian matrix"))
  g = VGroup()
  xs = [-5.05 + k * 2.02 for k in range(len(stops))]
  for x, (sym, col, zh, en) in zip(xs, stops):
   g.add(self._box(x, 0.62, sym, col, w=1.76, h=0.58, size=FS_TAG - 2),
         self._mid(0.02, zh, en, col, FS_TAG - 2, x=x, w=1.90))
  for x, nxt in zip(xs, xs[1:]):
   g.add(self._arr([x + 0.90, 0.62, 0], [nxt - 0.90, 0.62, 0], DIM, sw=1.8, tl=0.08))
  return g.add(self._mid(-0.72, "每一步都要用到前一步，順序不能跳",
                         "each step needs the one before it, so the order is not optional",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.20, "在座標空間裡，微分最後就是一個偏導數排成的矩陣",
                         "in a Cartesian space the differential ends up as a matrix of partial derivatives",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "於是微分法的規則就變成矩陣運算",
                         "and the rules of the calculus become matrix operations",
                         DIM, FS_TAG, w=11.9))

 def _theorems(self):
  g = VGroup()
  for cx, head, col, rows in (
      (-3.30, "d F ( α )   可逆", ACCENT_C,
       (("那麼 F 在 α 附近可逆", "then F itself is invertible near alpha"),
        ("線性的性質傳回非線性的映射", "a linear property carried back to the map"))),
      (3.30, "G ( x , y ) = 0", WARN,
       (("那麼 y 在附近被 x 唯一決定", "then y is determined by x nearby"),
        ("這就是隱函數定理", "that is the implicit-function theorem")))):
   g.add(self._box(cx, 0.92, head, col, w=5.00, h=0.62, size=FS_TAG))
   for k, (zh, en) in enumerate(rows):
    g.add(self._mid(0.24 - k * 0.56, zh, en, col if k == 0 else DIM,
                    FS_TAG, x=cx, w=4.90))
  g.add(Line([0.00, -0.60, 0], [0.00, 1.24, 0], color=DIM, stroke_width=1.6))
  return g.add(self._mid(-1.06, "兩個定理都要用到實數的完備性，那是第 4 章的事",
                         "both theorems lean on the completeness of the reals, which is chapter four",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "所以這一章會先把能做的做完，把完備性欠著",
                         "so this chapter does what it can and leaves completeness owing",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "第 1 節先回到實數上，把 ε-δ 練熟",
                         "section one goes back to the real line to get fluent with epsilon and delta",
                         ACCENT_B, FS_TAG, w=11.9))

 def _definition(self):
  ox, oy, sx, sy = -3.10, 0.15, 2.60, 1.00
  g, X, Y = self._axes31(ox, oy, sx, sy)
  e, d = EPS[0], DELTAS[0]
  g.add(self._band(ox, oy, sx, sy, e, d, X, Y, ACCENT_C, WARN))
  g.add(Text("a", font_size=FS_TAG - 3, color=DIM).move_to([X(A) + 0.20, oy - 1.22, 0]),
        Text("l", font_size=FS_TAG - 3, color=DIM).move_to([ox - 1.80, Y(L), 0]),
        Text("ϵ", font_size=FS_TAG - 3, color=ACCENT_C).move_to([ox + 1.78, Y(L + e), 0]),
        Text("δ", font_size=FS_TAG - 3, color=WARN).move_to([X(A + d) + 0.16, oy + 0.92, 0]))
  rows = ((0.86, "先給一條 ϵ 帶，", "first a band of width epsilon is given,", ACCENT_C),
          (0.22, "才回答得出一條 δ 帶", "and only then can a delta be named", WARN),
          (-0.42, "δ 內的圖形整段落在 ϵ 帶裡",
           "the graph over the delta band lands inside the epsilon band", ACCENT_A))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=2.90, w=5.40))
  return g.add(self._mid(-1.38, f"畫的是 f ( x ) = x ² 在 a = 1，ϵ = {FMT(e)} 時 δ = {FMT(d)}",
                         f"drawn for f of x = x squared at a = 1: epsilon {FMT(e)} gives delta {FMT(d)}",
                         DIM, FS_TAG, w=11.9),
               self._mid(-1.78, "這個 δ 是算出來的，而且驗過整段圖形真的沒有跑出帶子",
                         "that delta was computed, and the graph over it was checked to stay inside",
                         ACCENT_B, FS_TAG, w=11.9))

 def _puncture(self):
  ox, oy = -2.60, 0.42
  g = VGroup(Line([ox - 2.40, oy, 0], [ox + 2.40, oy, 0], color=DIM, stroke_width=1.6),
             Dot([ox, oy, 0], radius=0.075, color=DIM, fill_opacity=0.0),
             Text("a", font_size=FS_TAG - 2, color=DIM).move_to([ox, oy - 0.36, 0]))
  for s in (-1, 1):
   g.add(Line([ox + s * 0.16, oy + 0.13, 0], [ox + s * 1.30, oy + 0.13, 0],
              color=ACCENT_C, stroke_width=4),
         Text("δ", font_size=FS_TAG - 3, color=WARN)
         .move_to([ox + s * 1.30, oy + 0.42, 0]))
  rows = ((-0.42, "0 < | x − a | 這半邊，就是把 a 自己挖掉",
           "the strictly positive half of the inequality is what removes a itself", ACCENT_A),
          (-0.90, "微積分的差商在 a 根本沒定義，卻正是要看的東西",
           "the difference quotients of calculus are undefined at a, and are exactly what we watch", WARN))
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, w=11.9))
  return g.add(self._mid(-1.40, "所以極限講的是「附近」，不是「在那一點」",
                         "so a limit is about the neighbourhood, not about the point",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "f 在 a 有沒有定義、定義成多少，都跟這個極限無關",
                         "whether f is even defined at a, and as what, does not enter",
                         DIM, FS_TAG, w=11.9))

 def _quantifiers(self):
  g = VGroup()
  order = (("∀ ϵ > 0", ACCENT_C), ("∃ δ > 0", WARN), ("∀ x", ACCENT_B))
  swapped = (("∀ ϵ > 0", ACCENT_C), ("∀ x", ACCENT_B), ("∃ δ > 0", WARN))
  for y, row, mark, col in ((0.80, order, "✓", ACCENT_A), (-0.10, swapped, "✗", DIM)):
   for k, (s, c) in enumerate(row):
    g.add(self._box(-3.60 + k * 2.00, y, s, c, w=1.80, h=0.56, size=FS_TAG - 1))
   g.add(Text(mark, font_size=FS_TAG + 2, color=col).move_to([-0.90, y, 0]))
  g.add(self._mid(0.80, "δ 只能靠 ϵ 決定", "delta may depend on epsilon only",
                  ACCENT_A, FS_TAG, x=2.90, w=5.20),
        self._mid(-0.10, "這樣寫等於允許 δ 隨 x 改", "this lets delta change with x",
                  DIM, FS_TAG, x=2.90, w=5.20))
  return g.add(self._mid(-0.92, "同樣三個量詞，順序一動，講的就是另一件事",
                         "the same three quantifiers in another order state something else",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.36, "第二種寫法幾乎對每個函數都成立，所以什麼也沒說",
                         "the second version holds for almost any function, so it says nothing",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "這種句子念起來不像人話，但那正是它精確的原因",
                         "such sentences read badly as prose, and that is exactly why they are exact",
                         DIM, FS_TAG, w=11.9))

 def _narrower(self):
  g = VGroup()
  for cx, e, d, ecol in ((-3.20, EPS[0], DELTAS[0], ACCENT_C),
                         (2.40, EPS[1], DELTAS[1], WARN)):
   ox, oy, sx, sy = cx, 0.20, 2.30, 0.85
   ax, X, Y = self._axes31(ox, oy, sx, sy)
   g.add(ax, self._band(ox, oy, sx, sy, e, d, X, Y, ecol, ecol))
   g.add(self._sym(-1.02, f"ϵ = {FMT(e)}        δ = {FMT(d)}", ecol, FS_TAG - 1,
                   x=cx, w=4.20))
  return g.add(self._mid(-1.44, "ϵ 縮成三分之一，δ 也跟著縮成三分之一",
                         "epsilon down to a third takes delta down to a third with it",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.78, "兩個 δ 都是同一條公式算出來的，圖也是照著畫的",
                         "both deltas come from the same formula, and both pictures are drawn from them",
                         DIM, FS_TAG, w=11.9))

 def _sum(self):
  g = VGroup(self._sym(1.00, "h  =  f  +  g        w  =  u  +  v", ACCENT_A,
                       FS_TAG, x=0.00, w=6.40))
  # the two pieces are drawn end to end and exactly half the total each, so
  # the picture is the argument rather than an illustration of it
  bar, half = 4.60, 2.30
  for k, (lab, col) in enumerate((("| f − u |", ACCENT_C), ("| g − v |", WARN))):
   x0 = -bar / 2 + k * half
   g.add(Line([x0, 0.30, 0], [x0 + half, 0.30, 0], color=col, stroke_width=6),
         Text(lab, font_size=FS_TAG - 3, color=col)
         .move_to([x0 + half / 2, 0.62, 0]),
         Text("< ϵ / 2", font_size=FS_TAG - 4, color=col)
         .move_to([x0 + half / 2, -0.02, 0]))
  g.add(Line([-bar / 2, -0.42, 0], [bar / 2, -0.42, 0], color=ACCENT_A, stroke_width=6),
        Text("| h − w |   <   ϵ", font_size=FS_TAG - 2, color=ACCENT_A)
        .move_to([0.00, -0.74, 0]))
  return g.add(self._mid(-1.16, "兩個一半加起來剛好是一個 ϵ，這就是為什麼要切一半",
                         "two halves add to one epsilon, which is the whole reason for halving",
                         ACCENT_A, FS_TAG, w=11.9),
               self._mid(-1.44, "兩個 δ 取小的那一個，兩邊的不等式才會同時成立",
                         "take the smaller of the two deltas so both inequalities hold at once",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.78, "引理 1.1 的證明，寫下來就只有選 δ 這一步",
                         "written out, the proof of Lemma 1.1 is just that choice of delta",
                         DIM, FS_TAG, w=11.9))

 def _reciprocal(self):
  g = VGroup(self._sym(1.02, "h  =  1 / f        w  =  1 / u        u  ≠  0",
                       ACCENT_A, FS_TAG, x=0.00, w=6.60),
             self._sym(0.40, "h − w   =   ( u − f ) / ( f u )", WARN, FS_TAG,
                       x=0.00, w=6.60))
  ox, oy = 0.00, -0.36
  g.add(Line([ox - 2.60, oy, 0], [ox + 2.60, oy, 0], color=DIM, stroke_width=1.6),
        Dot([ox - 2.20, oy, 0], radius=0.06, color=DIM),
        Text("0", font_size=FS_TAG - 3, color=DIM).move_to([ox - 2.20, oy - 0.32, 0]),
        Dot([ox + 1.10, oy, 0], radius=0.07, color=ACCENT_C),
        Text("u", font_size=FS_TAG - 3, color=ACCENT_C).move_to([ox + 1.10, oy + 0.30, 0]),
        Line([ox - 0.55, oy + 0.14, 0], [ox - 0.55, oy - 0.14, 0], color=WARN,
             stroke_width=2.5),
        Text("| u | / 2", font_size=FS_TAG - 4, color=WARN)
        .move_to([ox - 0.55, oy - 0.42, 0]),
        Line([ox - 0.55, oy + 0.06, 0], [ox + 2.40, oy + 0.06, 0], color=WARN,
             stroke_width=5))
  return g.add(self._mid(-1.16, "先花掉一個 δ 把 f 逼到 u 的一半以外，分母就有了下界",
                         "spend one delta keeping f beyond half of u, and the denominator has a floor",
                         WARN, FS_TAG, w=11.9),
               self._mid(-1.44, "剩下的就跟前一拍一樣：再取一個 δ 把分子壓小",
                         "the rest is like the last beat: take another delta to make the numerator small",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "會動的分母是這裡唯一的難處，其餘都是照抄",
                         "the moving denominator is the only difficulty; the rest is routine",
                         DIM, FS_TAG, w=11.9))

 def _lub(self):
  ox, oy = -0.40, 0.72
  g = VGroup(Line([ox - 4.60, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.6),
             Line([ox - 4.20, oy, 0], [ox - 0.60, oy, 0], color=ACCENT_C, stroke_width=6),
             Text("A", font_size=FS_TAG - 1, color=ACCENT_C)
             .move_to([ox - 2.40, oy + 0.34, 0]))
  for k, x in enumerate((-0.60, 0.70, 2.10)):
   col = WARN if k == 0 else DIM
   g.add(Dot([ox + x, oy, 0], radius=0.07 if k == 0 else 0.055, color=col))
  g.add(self._mid(oy - 0.44, "最小的那一個上界", "the smallest of the upper bounds",
                  WARN, FS_TAG - 1, x=ox - 0.60, w=2.60),
        self._mid(oy - 0.44, "其他上界", "other upper bounds", DIM, FS_TAG - 1,
                  x=ox + 1.90, w=2.20))
  rows = ((-0.44, "lub ( 0 , 1 )  =  1        lub [ 0 , 1 ]  =  1", DIM),
          (-0.96, "glb { 1 / n }  =  0        lub { x : x ² < 2 }  =  √ 2", ACCENT_A))
  for y, s, col in rows:
   g.add(self._sym(y, s, col, FS_TAG, x=0.00, w=8.40))
  return g.add(self._mid(-1.44, "最小上界可以在集合裡，也可以不在——這一點正是重點",
                         "the least upper bound may or may not belong to the set, and that is the point",
                         ACCENT_C, FS_TAG, w=11.9),
               self._mid(-1.78, "有理數就沒有這個性質，這是實數與它們的分水嶺",
                         "the rationals do not have this property, and that is what separates them",
                         ACCENT_B, FS_TAG, w=11.9))

 def stage(self):
  wt, wn, rt = self._what(), self._why_norm(), self._route()
  th, df, pu = self._theorems(), self._definition(), self._puncture()
  qu, nr = self._quantifiers(), self._narrower()
  sm, rc, lb = self._sum(), self._reciprocal(), self._lub()
  return [([wt], []), ([wn], [wt]), ([rt], [wn]), ([th], [rt]),
          ([df], [th]), ([pu], [df]), ([qu], [pu]), ([nr], [qu]),
          ([sm], [nr]), ([rc], [sm]), ([lb], [rc])]


AdvCalcE31ZH, AdvCalcE31EN = make(AdvCalcE31Base, "31", prefix="AdvCalcE")
