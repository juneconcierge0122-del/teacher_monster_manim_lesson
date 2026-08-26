"""advcalc E37 -- chapter 3, section 5 (book pp. 136-139): neighborhoods and
deleted neighborhoods, the three classes of functions vanishing at the origin
(the infinitesimals S, the Lipschitz class big oh, and little oh), the three
short examples that separate them, Theorem 5.1 in full (nesting and closure,
composition, products, Hom inside big oh, and Hom meeting little oh only at
zero), and the remark that all of it survives a change to an equivalent norm.
Book page 140 is exercises 5.1 to 5.11; E38 opens section 6, the differential.

The book writes the three classes with script letters.  They are written here
with plain S, O and o, which is the notation everyone reads anyway and which
the render font is certain to carry.

Every quotient the episode puts on screen is evaluated rather than sketched,
including the one that carries the punch line: a nonzero linear map's quotient
is a constant along a ray no matter how far in you go, which is why Hom and
little oh meet only at the zero map, and therefore why a differential is
unique.  The last beat evaluates the same quotient under two different norms
to check that the classification really does not move.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20

FUNCS = (("√|x|", lambda x: math.sqrt(abs(x)), WARN),
         ("x", lambda x: x, ACCENT_C),
         ("x²", lambda x: x * x, ACCENT_B))
SAMPLE = [10 ** (-k) for k in range(0, 4)]          # 1, 0.1, 0.01, 0.001


def _ratio(f, x):
 return abs(f(x)) / abs(x)


# ── beat 5: the three examples really do sit in different classes ───────
RATIOS = [[_ratio(f, x) for x in SAMPLE] for _, f, _ in FUNCS]
assert RATIOS[0][0] < RATIOS[0][-1], "the square root's quotient should be climbing"
assert RATIOS[0][-1] > 30, "it should already be large at the last sample"
assert all(abs(r - 1) < 1e-12 for r in RATIOS[1]), "the identity's quotient is one throughout"
assert RATIOS[2][-1] < 1e-2 and RATIOS[2][-1] < RATIOS[2][0], "x squared's quotient should vanish"
# and the Lipschitz condition itself: big oh holds for x and x squared, not for the root
for _k, (_, _f, _) in enumerate(FUNCS):
 _sup = max(_ratio(_f, 10 ** (-t / 4.0)) for t in range(0, 41))
 assert (_sup > 30) == (_k == 0), "only the square root should escape every Lipschitz constant"

# ── beat 7: composition ────────────────────────────────────────────────
_sq = lambda x: x * x
COMPOSE = [_ratio(lambda x: _sq(_sq(x)), x) for x in SAMPLE]
assert COMPOSE[-1] < 1e-8 and all(a > b for a, b in zip(COMPOSE, COMPOSE[1:])), \
    "the composite should fall to zero faster than either factor"

# ── beat 8: a big oh times an infinitesimal ────────────────────────────
PRODUCT = [_ratio(lambda x: x * math.sqrt(abs(x)), x) for x in SAMPLE]
for _x, _p in zip(SAMPLE, PRODUCT):
 assert abs(_p - math.sqrt(abs(_x))) < 1e-12, "the product's quotient should be the square root"
assert PRODUCT[-1] < 0.05, "and it should be visibly on its way to zero"

# ── beat 9: a nonzero linear map cannot be little oh ───────────────────
TMAT = ((2, -1), (1, 1))


def _ninf(v):
 return max(abs(v[0]), abs(v[1]))


def _n1(v):
 return abs(v[0]) + abs(v[1])


def _ap(m, v):
 return (m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1])


RAY = (1, -1)
LIN = [_ninf(_ap(TMAT, (t * RAY[0], t * RAY[1]))) / _ninf((t * RAY[0], t * RAY[1]))
       for t in SAMPLE]
assert all(abs(r - LIN[0]) < 1e-12 for r in LIN), \
    "the whole point is that this quotient does not move as the vector shrinks"
assert LIN[0] > 0, "a nonzero linear map has a nonzero quotient somewhere"

# ── beat 10: an equivalent norm does not move the classification ───────
NORM_PAIR = (("∞", _ninf), ("₁", _n1))
SQ_RATIOS = {}
for _name, _n in NORM_PAIR:
 SQ_RATIOS[_name] = [_n((t * t, (t / 2) ** 2)) / _n((t, t / 2)) for t in SAMPLE]
 assert SQ_RATIOS[_name][-1] < 1e-2, "squaring should be little oh under either norm"
assert SQ_RATIOS["∞"] != SQ_RATIOS["₁"], "the two norms should give different numbers"
for _a, _b in zip(SQ_RATIOS["∞"], SQ_RATIOS["₁"]):
 assert 0.5 < _a / _b < 2.0, "but only by a bounded factor, which is why the class is the same"


class AdvCalcE37Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 37

 MODE_LABEL = {
  0: {"zh": "鄰域，與去心鄰域", "en": "neighborhoods, and deleted ones"},
  1: {"zh": "重點是趨於零的速度", "en": "what matters is the rate"},
  2: {"zh": "無窮小 S：會趨於零就好", "en": "the infinitesimals S: it just has to vanish"},
  3: {"zh": "大 O：被一個楔形壓住", "en": "big oh: held inside a wedge"},
  4: {"zh": "小 o：比自變數更快", "en": "little oh: faster than its argument"},
  5: {"zh": "三個例子把三個類分開", "en": "three examples, three classes"},
  6: {"zh": "定理 5.1：三個都是向量空間", "en": "Theorem 5.1: all three are vector spaces"},
  7: {"zh": "合成：有一個是小 o 就夠", "en": "composition: one little oh is enough"},
  8: {"zh": "乘積：大 O 乘無窮小落進小 o", "en": "product: big oh times an infinitesimal"},
  9: {"zh": "Hom 與小 o 只交於零映射", "en": "Hom meets little oh only at zero"},
  10: {"zh": "換等價範數，三個類不動", "en": "an equivalent norm changes nothing"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _panel(self, rows, x=PANEL_X, w=PANEL_W):
  g = VGroup()
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=x, w=w))
  return g

 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _blob(self, cx, cy, rx, ry, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + 0.16 * rx * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.14 * ry * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _circle(self, cx, cy, r, col, sw=2.5):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / 72),
                       cy + r * math.sin(2 * math.pi * k / 72), 0] for k in range(73)],
                     col, sw=sw)

 def _plot(self, ox, oy, sx, sy, w=2.60, h=1.05):
  """Bare axes for a quotient picture, with the origin at the left."""
  return VGroup(Line([ox - 0.14, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.6),
                Line([ox, oy - 0.14, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.6))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.62, dy=0.44, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _nbhd(self):
  g = VGroup()
  for cx, hole in ((-4.85, False), (-1.80, True)):
   g.add(self._blob(cx, 0.10, 1.15, 0.78, ACCENT_C),
         self._circle(cx + 0.18, 0.14, 0.46, ACCENT_B, sw=2),
         Dot([cx + 0.18, 0.14, 0], radius=0.06, color=WARN if not hole else DIM))
   if hole:
    g.add(Dot([cx + 0.18, 0.14, 0], radius=0.075, color=WARN),
          Dot([cx + 0.18, 0.14, 0], radius=0.048, color="#0b0e14"))
   g.add(Text("α", font_size=FS_TAG - 3, color=WARN)
         .move_to([cx + 0.18, 0.14 - 0.30, 0]))
  g.add(self._panel(((0.86, "包含以 α 為心的一顆開球",
                      "it contains an open ball about alpha", ACCENT_B),
                     (0.20, "這樣的集合就叫 α 的鄰域",
                      "such a set is called a neighborhood of alpha", ACCENT_C),
                     (-0.46, "把 α 本身挖掉，就是去心鄰域",
                      "remove alpha itself and it is a deleted one", WARN))))
  return g.add(self._foot("形狀可以很不規則，重點只有「α 周圍有一整圈的空間」",
                          "the shape may be irregular; all that matters is room all round alpha",
                          ACCENT_A,
                          "接下來三個類的函數都定義在零的某個鄰域上，不必是整個空間",
                          "the three classes below all live on some neighborhood of zero"))

 def _why(self):
  ox, oy, sx, sy = -5.10, -0.62, 2.90, 0.95
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.30, h=1.85))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g.add(self._curve([[X(t / 100), Y((t / 100) + 0.9 * (t / 100) ** 2), 0]
                     for t in range(0, 101)], ACCENT_B, sw=3),
        Line([X(0), Y(0), 0], [X(1.0), Y(1.0), 0], color=ACCENT_C, stroke_width=2.5))
  for t in (0.55, 1.0):
   g.add(self._dash([X(t), Y(t), 0], [X(t), Y(t + 0.9 * t * t), 0], WARN, n=6, sw=2),
         Dot([X(t), Y(t + 0.9 * t * t), 0], radius=0.05, color=ACCENT_B),
         Dot([X(t), Y(t), 0], radius=0.05, color=ACCENT_C))
  g.add(self._panel(((0.86, "青色是實際的變化量",
                      "the teal curve is the actual change", ACCENT_B),
                     (0.20, "紫色是它的線性部分",
                      "the purple line is its linear part", ACCENT_C),
                     (-0.46, "紅色那一段就是差，它要比 t 更快趨於零",
                      "the red gap is the difference, and it must vanish faster than t", WARN))))
  return g.add(self._foot("整個微分學就是在研究「趨於零的速度」，所以速度需要一套詞",
                          "the whole differential calculus studies rates of vanishing, so rates need names",
                          ACCENT_A,
                          "接下來三個類，就是把「多快」分成三個等級",
                          "the three classes below sort how fast into three grades"))

 def _class_s(self):
  ox, oy, sx, sy = -5.10, -0.55, 3.10, 1.35
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.35))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  for name, f, col in FUNCS:
   g.add(self._curve([[X(t / 100), Y(abs(f(t / 100))), 0] for t in range(0, 101)], col, sw=3))
  g.add(Dot([X(0), Y(0), 0], radius=0.06, color=ACCENT_A))
  g.add(self._panel(((0.86, "三條線在零都收到零",
                      "all three curves come down to zero at zero", ACCENT_A),
                     (0.20, "值是零、而且連續，就在 S 裡",
                      "value zero and continuous there is all S asks", ACCENT_C),
                     (-0.46, "它完全沒有要求「趨得多快」",
                      "it says nothing at all about how fast", DIM))))
  return g.add(self._foot("這一類最寬鬆，光靠它分不出三條線的差別",
                          "this is the loosest class and cannot tell the three curves apart",
                          ACCENT_A,
                          "所以下面兩拍要換一個看法：不看函數，看比值",
                          "so the next two beats stop watching the function and watch the quotient"))

 def _class_o(self):
  ox, oy, sx, sy = -5.10, -0.55, 3.10, 1.35
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.35))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  c = 1.15
  g.add(Line([X(0), Y(0), 0], [X(1.0), Y(c), 0], color=ACCENT_A, stroke_width=2))
  for name, f, col in FUNCS:
   g.add(self._curve([[X(t / 100), Y(abs(f(t / 100))), 0] for t in range(0, 101)], col, sw=3))
  g.add(self._panel(((0.86, "橘線的斜率就是那個常數 c",
                      "the slope of the orange line is the constant c", ACCENT_A),
                     (0.20, "青色與紫色都壓在它下面",
                      "the teal and purple curves stay underneath it", ACCENT_C),
                     (-0.46, "紅色那條無論 c 多大都會鑽出去",
                      "the red one escapes however large c is made", WARN))))
  return g.add(self._foot("大 O 就是「在零附近被某個線性的東西壓住」，也就是在零 Lipschitz",
                          "big oh means held down by something linear near zero: Lipschitz at zero",
                          ACCENT_A,
                          "常數多大不重要，重要的是存在一個常數",
                          "the size of the constant does not matter, only that one exists"))

 def _class_oo(self):
  ox, oy, sx, sy = -5.10, -0.55, 3.10, 1.35
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.35))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  for c, col in ((1.15, DIM), (0.55, DIM), (0.22, ACCENT_A)):
   g.add(Line([X(0), Y(0), 0], [X(min(1.0, 1.30 / c)), Y(min(c, 1.30)), 0],
              color=col, stroke_width=1.6))
  for name, f, col in FUNCS[1:]:
   g.add(self._curve([[X(t / 100), Y(abs(f(t / 100))), 0] for t in range(0, 101)], col, sw=3))
  g.add(self._panel(((0.86, "把楔形越關越窄",
                      "narrow the wedge as far as you like", ACCENT_A),
                     (0.20, "青色最後總是關得住",
                      "the teal curve is caught in the end every time", ACCENT_B),
                     (-0.46, "紫色是直線，關到某個角度就關不住了",
                      "the purple line is straight, and past some angle it never is", ACCENT_C))))
  return g.add(self._foot("小 o 要求對每一個 c 都成立，所以比大 O 強得多",
                          "little oh asks this for every c, which is far stronger than big oh",
                          ACCENT_A,
                          "換句話說，比值必須真的趨於零，不能只是被壓住",
                          "put differently, the quotient must actually vanish, not merely stay bounded"))

 def _examples(self):
  ox, oy, sx, sy = -5.30, -0.62, 3.00, 0.42
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.30, h=1.55))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + min(v, 3.6) * sy
  for name, f, col in FUNCS:
   g.add(self._curve([[X(t / 200), Y(_ratio(f, max(t, 1) / 200.0)), 0]
                      for t in range(1, 201)], col, sw=3))
  g.add(self._dash([X(0), Y(1.0), 0], [X(1.0), Y(1.0), 0], DIM, n=22, sw=1.2),
        Text("1", font_size=FS_TAG - 5, color=DIM).move_to([ox - 0.24, Y(1.0), 0]))
  rows = [("       x          √|x|        x         x ²", DIM)]
  for k, x in enumerate(SAMPLE):
   rows.append((f"{x:8.3f}   {RATIOS[0][k]:8.2f}   {RATIOS[1][k]:6.2f}   {RATIOS[2][k]:7.3f}",
                (ACCENT_A, ACCENT_C, ACCENT_B, WARN)[k % 4]))
  g.add(self._table(rows, y0=0.80, dy=0.40))
  return g.add(self._foot("三個比值：一個爆炸、一個永遠是一、一個趨於零",
                          "three quotients: one explodes, one sits at one, one goes to zero",
                          ACCENT_A,
                          "S 分不出它們，大 O 分掉第一個，小 o 分掉第二個",
                          "S cannot tell them apart; big oh cuts the first, little oh the second"))

 def _nesting(self):
  cx, cy = -3.55, 0.10
  g = VGroup()
  for rx, ry, col in ((1.85, 0.95, ACCENT_C), (1.30, 0.68, ACCENT_B), (0.72, 0.38, ACCENT_A)):
   g.add(self._circle(cx, cy, 0.0, col) if rx == 0 else
         self._curve([[cx + rx * math.cos(2 * math.pi * k / 96),
                       cy + ry * math.sin(2 * math.pi * k / 96), 0] for k in range(97)],
                     col, sw=2.5))
  for lab, dx, dy, col in (("S", -1.60, 0.72, ACCENT_C), ("O", -1.05, 0.44, ACCENT_B),
                           ("o", -0.48, 0.14, ACCENT_A)):
   g.add(Text(lab, font_size=FS_TAG + 1, color=col).move_to([cx + dx, cy + dy, 0]))
  for lab, dx, dy, up, col in (("√|x|", 1.28, 0.22, 0.26, WARN),
                               ("x", 0.92, -0.20, -0.26, ACCENT_B),
                               ("x²", 0.16, 0.10, -0.28, ACCENT_A)):
   g.add(Dot([cx + dx, cy + dy, 0], radius=0.055, color=col),
         Text(lab, font_size=FS_TAG - 3, color=col).move_to([cx + dx, cy + dy + up, 0]))
  g.add(self._panel(((0.86, "三個類一個套一個",
                      "the three classes nest", ACCENT_C),
                     (0.20, "而且各自對加法與係數倍封閉",
                      "and each is closed under sums and scalar multiples", ACCENT_B),
                     (-0.46, "所以三個都是向量空間",
                      "so all three are vector spaces", ACCENT_A))))
  return g.add(self._foot("能像向量一樣加來加去，是後面推導微分規則的前提",
                          "being able to add them like vectors is what the rules of differentiation need",
                          ACCENT_A,
                          "三個點就是上一拍那三個例子，各自落在該落的環裡",
                          "the three dots are the previous examples, each in the ring it belongs to"))

 def _compose(self):
  g = VGroup()
  for cx, lab, col in ((-5.30, "V", ACCENT_B), (-3.20, "W", ACCENT_C), (-1.10, "X", WARN)):
   g.add(self._circle(cx, 0.42, 0.42, col, sw=2),
         Dot([cx, 0.42, 0], radius=0.055, color=col),
         Text(lab, font_size=FS_TAG - 2, color=DIM).move_to([cx, 1.10, 0]))
  for cx in (-4.25, -2.15):
   g.add(self._arr([cx - 0.32, 0.42, 0], [cx + 0.32, 0.42, 0], ACCENT_A, sw=2.5, tl=0.12))
  rows = [("       x          x ² ∘ x ²", DIM)]
  for k, x in enumerate(SAMPLE):
   rows.append((f"{x:8.3f}        {COMPOSE[k]:.2e}", (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[k % 4]))
  g.add(self._table(rows, y0=0.80, dy=0.40))
  return g.add(self._foot("大 O 接大 O 還是大 O：兩個常數乘起來就是新的常數",
                          "big oh after big oh is big oh: the two constants multiply into a new one",
                          ACCENT_A,
                          "只要有一個是小 o，合成就掉進小 o，這裡是 x 的三次方",
                          "one little oh anywhere drags the composite in; here the quotient is x cubed"))

 def _product(self):
  ox, oy, sx, sy = -5.30, -0.58, 3.10, 1.40
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.45))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g.add(self._curve([[X(t / 200), Y(math.sqrt(t / 200.0)), 0] for t in range(0, 201)],
                    ACCENT_A, sw=3))
  for k, x in enumerate(SAMPLE):
   if x > 0.02:
    g.add(Dot([X(x), Y(math.sqrt(x)), 0], radius=0.05, color=WARN))
  rows = [("       x        x · √|x|   /   x", DIM)]
  for k, x in enumerate(SAMPLE):
   rows.append((f"{x:8.3f}            {PRODUCT[k]:.4f}",
                (ACCENT_B, ACCENT_C, WARN, ACCENT_A)[k % 4]))
  g.add(self._table(rows, y0=0.80, dy=0.40))
  return g.add(self._foot("大 O 乘上一個無窮小，結果一定落在小 o 裡",
                          "a big oh times an infinitesimal always lands in little oh",
                          ACCENT_A,
                          "這一條在後面算微分的乘法規則時會一直用到",
                          "the product rule for differentials will lean on this constantly"))

 def _hom(self):
  ox, oy, sx, sy = -5.30, -0.58, 3.10, 0.40
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.55))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g.add(self._dash([X(0), Y(LIN[0]), 0], [X(1.0), Y(LIN[0]), 0], WARN, n=24, sw=2.5),
        self._curve([[X(t / 200), Y(_ratio(_sq, max(t, 1) / 200.0)), 0]
                     for t in range(1, 201)], ACCENT_B, sw=3))
  g.add(Text(f"{LIN[0]:.0f}", font_size=FS_TAG - 4, color=WARN)
        .move_to([ox - 0.26, Y(LIN[0]), 0]))
  g.add(self._panel(((0.86, "紅線是一個線性映射的比值",
                      "the red line is a linear map's quotient", WARN),
                     (0.20, "不管走多近，它都不動",
                      "however far in you go, it does not move", ACCENT_A),
                     (-0.46, "青色那條才是小 o 該有的樣子",
                      "the teal curve is what little oh looks like", ACCENT_B))))
  return g.add(self._foot("所以 Hom 跟小 o 只交於零映射——非零的線性映射永遠出不了大 O",
                          "so Hom meets little oh only at the zero map; a nonzero one never gets in",
                          ACCENT_A,
                          "證明只用到齊次性，所以一次齊次的函數裡除了零沒有小 o",
                          "the proof uses only homogeneity, so no degree one homogeneous map but zero is in"))

 def _norms(self):
  ox, oy, sx, sy = -5.30, -0.58, 3.10, 1.45
  g = VGroup(self._plot(ox, oy, sx, sy, w=3.40, h=1.45))
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  for (name, n), col in zip(NORM_PAIR, (WARN, ACCENT_B)):
   g.add(self._curve([[X(t / 200), Y(n(((t / 200.0) ** 2, ((t / 200.0) / 2) ** 2))
                                     / max(n((t / 200.0, (t / 200.0) / 2)), 1e-9)), 0]
                      for t in range(1, 201)], col, sw=3))
  rows = [("       t         ‖ · ‖ ∞        ‖ · ‖ ₁", DIM)]
  for k, x in enumerate(SAMPLE):
   rows.append((f"{x:8.3f}      {SQ_RATIOS['∞'][k]:8.5f}   {SQ_RATIOS['₁'][k]:8.5f}",
                (ACCENT_A, ACCENT_C, WARN, ACCENT_B)[k % 4]))
  g.add(self._table(rows, y0=0.80, dy=0.40))
  return g.add(self._foot("兩個範數給的數字不同，但都趨於零，所以分類完全一樣",
                          "two norms, different numbers, both vanishing: the classification is identical",
                          ACCENT_A,
                          "這就是微分唯一的理由，下一集正式定義微分",
                          "and that is why a differential is unique; next time it gets its definition"))

 def stage(self):
  a, b, c = self._nbhd(), self._why(), self._class_s()
  d, e, f = self._class_o(), self._class_oo(), self._examples()
  h, i, j = self._nesting(), self._compose(), self._product()
  k, l = self._hom(), self._norms()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE37ZH, AdvCalcE37EN = make(AdvCalcE37Base, "37", prefix="AdvCalcE")
