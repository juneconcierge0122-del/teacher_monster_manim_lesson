"""advcalc E42 -- chapter 3, section 8, second part (book pp. 154-155): the
answer to the question E41 left open, Theorem 8.2 (continuous partial
differentials do force differentiability) with its two-step proof through E40's
corollary, Theorem 8.3 by induction, Lemma 8.3 (a bounded bilinear map is
everywhere differentiable) and Theorem 8.4, the general product rule.  Pages
155-156 are exercises 8.1 to 8.10; E43 opens section 9.

The counterexample that opens the episode is the standard one: its two partial
derivatives at the origin are both zero while the function itself is one half
all along the diagonal, so it is not even continuous there -- the module
evaluates both facts.  The two-step estimate of Theorem 8.2's proof is carried
out numerically on a concrete map, one step at a time and then together, and
the bilinear map used for Lemma 8.3 and Theorem 8.4 is checked to be bounded
with constant one, differentiated by the lemma's formula, and then run through
the product rule against the composite's own derivative.
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
H = 1e-6
SAMPLE = (1e-1, 1e-2, 1e-3)


# ── beat 0: partials exist, the function is not even continuous ────────
def _bad(v):
 x, y = v
 return 0.0 if (x == 0.0 and y == 0.0) else x * y / (x * x + y * y)


BAD_PX = (_bad((H, 0.0)) - _bad((-H, 0.0))) / (2 * H)
BAD_PY = (_bad((0.0, H)) - _bad((0.0, -H))) / (2 * H)
assert abs(BAD_PX) < 1e-9 and abs(BAD_PY) < 1e-9, "both partials at the origin should be zero"
BAD_DIAG = [_bad((t, t)) for t in SAMPLE]
assert all(abs(v - 0.5) < 1e-12 for v in BAD_DIAG), \
    "the diagonal value is the whole point and it should not move"
assert abs(BAD_DIAG[0] - _bad((0.0, 0.0))) > 0.4, "so the function is not continuous at the origin"


# ── beats 1 to 5: Theorem 8.2, carried out one step at a time ──────────
def _F(a, b):
 return math.sin(a) * b + a * b * b


A0, B0 = 0.6, 0.4
S1 = math.cos(A0) * B0 + B0 * B0          # the first partial differential's slope
S2 = math.sin(A0) + 2 * A0 * B0           # the second's
assert abs(S1 - (_F(A0 + H, B0) - _F(A0 - H, B0)) / (2 * H)) < 1e-6
assert abs(S2 - (_F(A0, B0 + H) - _F(A0, B0 - H)) / (2 * H)) < 1e-6

STEP1, STEP2, TOTAL = [], [], []
for _t in SAMPLE:
 _xi, _eta = _t, -_t / 2
 STEP1.append(abs(_F(A0 + _xi, B0 + _eta) - _F(A0, B0 + _eta) - S1 * _xi) / abs(_xi))
 STEP2.append(abs(_F(A0, B0 + _eta) - _F(A0, B0) - S2 * _eta) / abs(_eta))
 TOTAL.append(abs(_F(A0 + _xi, B0 + _eta) - _F(A0, B0) - (S1 * _xi + S2 * _eta))
              / (abs(_xi) + abs(_eta)))
for _seq in (STEP1, STEP2, TOTAL):
 assert all(a > b for a, b in zip(_seq, _seq[1:])) and _seq[-1] < 1e-2, \
     "one of the three estimates does not fall to zero"


# ── beats 7 to 9: a bounded bilinear map, and the product rule ─────────
def _om(u, v):
 return u[0] * v[1] - u[1] * v[0]


BOUND_B = max(abs(_om((math.cos(a), math.sin(a)), (math.cos(c), math.sin(c))))
              for a in (2 * math.pi * k / 360 for k in range(360))
              for c in (2 * math.pi * k / 360 for k in range(360)))
assert abs(BOUND_B - 1.0) < 1e-9, "this bilinear map should be bounded with constant one"

AVEC, BVEC = (1.0, 2.0), (3.0, -1.0)
REM = []
for _t in SAMPLE:
 _xi, _eta = (_t, -_t / 2), (_t / 3, _t)
 _lhs = _om((AVEC[0] + _xi[0], AVEC[1] + _xi[1]),
            (BVEC[0] + _eta[0], BVEC[1] + _eta[1])) - _om(AVEC, BVEC)
 _rhs = _om(AVEC, _eta) + _om(_xi, BVEC)
 REM.append(abs(_lhs - _rhs) / max(abs(_xi[0]), abs(_xi[1]), abs(_eta[0]), abs(_eta[1])))
assert all(a > b for a, b in zip(REM, REM[1:])) and REM[-1] < 1e-2, \
    "Lemma 8.3's formula is not the differential of the drawn bilinear map"


def _g(t):
 return (t, t * t)


def _h(t):
 return (1.0 + t, 3.0 * t)


CT = 1.0
PROD_DIRECT = (_om(_g(CT + H), _h(CT + H)) - _om(_g(CT - H), _h(CT - H))) / (2 * H)
_dg = tuple((p - q) / (2 * H) for p, q in zip(_g(CT + H), _g(CT - H)))
_dh = tuple((p - q) / (2 * H) for p, q in zip(_h(CT + H), _h(CT - H)))
PROD_1, PROD_2 = _om(_g(CT), _dh), _om(_dg, _h(CT))
assert abs(PROD_DIRECT - (PROD_1 + PROD_2)) < 1e-4, "the general product rule fails here"
for _v in (PROD_1, PROD_2, PROD_DIRECT):
 assert abs(_v - round(_v)) < 1e-4, "the beat prints these, so they should be whole numbers"
PROD_1, PROD_2, PROD_DIRECT = round(PROD_1), round(PROD_2), round(PROD_DIRECT)
assert PROD_2 < 0, "one term is negative here, which is worth showing"


class AdvCalcE42Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 42

 MODE_LABEL = {
  0: {"zh": "偏微分存在，還是可能不可微", "en": "partials can exist with no differential"},
  1: {"zh": "定理 8.2：加上「連續」就夠了", "en": "Theorem 8.2: continuity is enough"},
  2: {"zh": "候選的形式已經被鎖死", "en": "the candidate's form is already pinned"},
  3: {"zh": "工具是上一集那條推論", "en": "the tool is the previous corollary"},
  4: {"zh": "走法：一次只動一個變數", "en": "the route: one variable at a time"},
  5: {"zh": "兩步的誤差加起來還是小", "en": "the two errors still add up small"},
  6: {"zh": "定理 8.3：n 個因子用歸納", "en": "Theorem 8.3: n factors by induction"},
  7: {"zh": "引理 8.3：有界雙線性映射", "en": "Lemma 8.3: bounded bilinear maps"},
  8: {"zh": "固定一邊，剩下的就是線性的", "en": "hold one side and what is left is linear"},
  9: {"zh": "定理 8.4：一般的乘積規則", "en": "Theorem 8.4: the general product rule"},
  10: {"zh": "三條規則到齊，而且不用座標", "en": "three rules, and no coordinates anywhere"},
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

 def _cross(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _counter(self):
  ox, oy, sx, sy = -5.45, 0.05, 0.72, 0.70
  X = lambda th: ox + th * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([X(-0.20), Y(0), 0], [X(2 * math.pi + 0.20), Y(0), 0],
                  color=DIM, stroke_width=1.6),
             Line([ox, Y(-0.75), 0], [ox, Y(0.75), 0], color=DIM, stroke_width=1.6))
  g.add(self._curve([[X(2 * math.pi * k / 240),
                      Y(_bad((math.cos(2 * math.pi * k / 240),
                              math.sin(2 * math.pi * k / 240)))), 0]
                     for k in range(241)], ACCENT_B, sw=3, maxn=200))
  for th, col in ((0.0, ACCENT_A), (math.pi / 2, ACCENT_A), (math.pi / 4, WARN)):
   g.add(Dot([X(th), Y(_bad((math.cos(th), math.sin(th)))), 0], radius=0.06, color=col))
  g.add(self._sym(0.86, "∂ f / ∂ x  =  ∂ f / ∂ y  =  0", ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.26, f"f ( t , t )   =   {BAD_DIAG[0]:.1f}", WARN, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "沿兩個座標軸走過去都是零",
                  "along both coordinate axes it is zero", ACCENT_A, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.90, "沿對角線走過去卻恆等於二分之一",
                  "along the diagonal it never leaves one half", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("藍色是這個函數在單位圓上的值，兩個橘點是座標軸的方向",
                          "blue is the function on the unit circle, the orange dots the axis directions",
                          ACCENT_A,
                          "只看兩個方向就下結論，會漏掉紅點那裡發生的事",
                          "reading only two directions misses entirely what happens at the red one"))

 def _thm82(self):
  g = VGroup()
  for cy, lab, col in ((0.62, "dF ¹ :  A → Hom ( V ₁ , W )", ACCENT_B),
                       (0.02, "dF ² :  A → Hom ( V ₂ , W )", ACCENT_C)):
   g.add(self._rect(-3.75, cy, 1.85, 0.26, col),
         self._sym(cy, lab, col, FS_TAG - 1, x=-3.75, w=3.50))
  g.add(self._rect(-3.75, -0.62, 1.20, 0.26, WARN),
        self._sym(-0.62, "dF ₐ", WARN, FS_TAG, x=-3.75, w=2.20))
  g.add(self._arr([-1.80, 0.32, 0], [-1.35, 0.32, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-1.35, 0.32, 0], [-1.35, -0.62, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-1.35, -0.62, 0], [-2.05, -0.62, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "不只每一點存在，而且對那一點連續",
                      "not merely existing at each point, but continuous in it", ACCENT_B),
                     (0.20, "這樣就推得出整個微分存在",
                      "that already forces the whole differential to exist", WARN),
                     (-0.46, "而且推出來的微分本身也連續",
                      "and the differential it produces is continuous too", ACCENT_A))))
  return g.add(self._foot("上一拍的反例正好卡在這裡：它的偏導數存在，但在原點附近亂跳",
                          "the counterexample fails exactly here: its partials exist but jump about near zero",
                          ACCENT_A,
                          "「連續」這兩個字是整條定理的全部代價",
                          "the single word continuous is the entire price of the theorem"))

 def _pinned(self):
  g = VGroup()
  lines = (("dF ⁱ ₐ    =    dF ₐ ∘ θ ᵢ", ACCENT_B),
           ("Σ  θ ᵢ ∘ π ᵢ    =    I", ACCENT_C),
           ("⇒     dF ₐ    =    Σ  dF ⁱ ₐ ∘ π ᵢ", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.10))
  g.add(self._panel(((0.86, "引理 8.2：偏微分是微分的限制",
                      "Lemma 8.2: a partial is a restriction of the differential", ACCENT_B),
                     (0.20, "嵌入接投影再求和，就是恆等映射",
                      "injections after projections sum to the identity", ACCENT_C),
                     (-0.46, "所以微分若存在，只能長這個樣子",
                      "so if the differential exists it can only look like this", WARN))))
  return g.add(self._foot("先鎖死形式，再證那個形式真的成立——這是很省力的順序",
                          "pin the form down first, then prove it works: a cheap order to argue in",
                          ACCENT_A,
                          "剩下要證的只有「這個候選跟變化量的差落在小 o 裡」",
                          "all that is left is that the candidate differs from the change by a little oh"))

 def _tool(self):
  cx, cy, s = -3.85, 0.10, 1.45
  g = VGroup(self._cross(cx, cy, 1.65, 0.95))
  T = ((0.55, 0.20), (0.10, 0.45))
  corners = ((1, 1), (1, -1), (-1, -1), (-1, 1))
  r = 0.55
  tp = [[cx + s * (T[0][0] * r * v[0] + T[0][1] * r * v[1]),
         cy + s * (T[1][0] * r * v[0] + T[1][1] * r * v[1]), 0] for v in corners]
  fp = [[p[0] + 0.14 * math.cos(2.1 * k), p[1] + 0.14 * math.sin(1.7 * k + 1.0), 0]
        for k, p in enumerate(tp)]
  g.add(self._curve(tp + [tp[0]], ACCENT_C, sw=2.5),
        self._curve(fp + [fp[0]], WARN, sw=3))
  g.add(self._panel(((0.86, "微分跟固定的 T 差不超過 ε",
                      "the differential stays within epsilon of a fixed T", ACCENT_C),
                     (0.20, "變化量跟 T 作用的結果也差不超過 ε 乘位移",
                      "so the change stays within epsilon times the displacement of T", WARN),
                     (-0.46, "這裡的 T 取成中心點的偏微分",
                      "here T is taken to be the partial differential at the centre", ACCENT_A))))
  return g.add(self._foot("這是 E40 定理 7.4 的推論，證明整節就靠它",
                          "this is the corollary to E40's Theorem 7.4, and the whole proof rests on it",
                          ACCENT_A,
                          "它要求的是凸集，而球是凸的，所以在球上可以用",
                          "it needs a convex set, and a ball is convex, so it applies on the ball"))

 def _twostep(self):
  cx, cy, s = -4.20, 0.05, 1.55
  g = VGroup(self._cross(cx, cy, 1.65, 0.90))
  a, b = (0.0, 0.0), (0.62, 0.42)
  mid = (0.0, b[1])
  P = lambda v: [cx + s * v[0], cy + s * v[1], 0]
  g.add(Dot(P(a), radius=0.065, color=WARN), Dot(P(mid), radius=0.055, color=ACCENT_C),
        Dot(P(b), radius=0.065, color=ACCENT_B))
  g.add(self._arr(P(a), P(mid), ACCENT_C, sw=2.5, tl=0.12),
        self._arr(P(mid), P(b), ACCENT_B, sw=2.5, tl=0.12),
        self._dash(P(a), P(b), DIM, n=10, sw=1.6))
  g.add(self._sym(cy - 0.95, "η", ACCENT_C, FS_TAG - 1, x=cx - 0.24, w=0.60),
        self._sym(cy + s * b[1] + 0.26, "ξ", ACCENT_B, FS_TAG - 1,
                  x=cx + s * b[0] / 2, w=0.60))
  g.add(self._panel(((0.86, "第二步：只動第二個變數",
                      "second step: move only the second variable", ACCENT_C),
                     (0.20, "第一步：只動第一個變數",
                      "first step: move only the first variable", ACCENT_B),
                     (-0.46, "每一步都只剩一個變數在動",
                      "each step leaves exactly one variable in motion", ACCENT_A))))
  return g.add(self._foot("灰色虛線是真正要估的那一段，橘色兩段是實際走的路",
                          "the grey dashes are the displacement to be estimated; the two arrows are the route",
                          ACCENT_A,
                          "沿著座標方向走，是為了讓一變數的工具用得上",
                          "moving along the coordinate directions is what makes the one variable tool apply"))

 def _errors(self):
  g = VGroup()
  rows = [("      t          step 1        step 2         total", DIM)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"{t:7.3f}      {STEP1[k]:8.5f}     {STEP2[k]:8.5f}     {TOTAL[k]:8.5f}",
                (ACCENT_B, ACCENT_C, WARN)[k % 3]))
  g.add(self._table(rows, x=-3.30, w=6.00, y0=0.62, dy=0.40, size=FS_TAG - 1))
  g.add(self._sym(-1.00, "ε ‖ ξ ‖   +   ε ‖ η ‖   =   ε ( ‖ ξ ‖ + ‖ η ‖ )", ACCENT_A,
                  FS_TAG, x=-3.30, w=5.60))
  g.add(self._panel(((0.86, "兩步各自的誤差都掉到零",
                      "both steps' errors fall to zero", ACCENT_B),
                     (0.20, "加起來還是 ε 乘上整個位移",
                      "their sum is still epsilon times the whole displacement", WARN),
                     (-0.46, "用的是相加的乘積範數，所以剛好相配",
                      "the sum product norm is used, which is what makes it match", ACCENT_A))))
  return g.add(self._foot("三個數字都是在一個具體的例子上算出來的，不是估的",
                          "all three columns were computed on a concrete example rather than estimated",
                          ACCENT_A,
                          "ε 可以取到任意小，所以差落在小 o 裡，候選就是微分",
                          "epsilon may be made as small as one likes, so the difference is little oh"))

 def _induction(self):
  g = VGroup()
  for cx, lab, col in ((-5.05, "V ₁", ACCENT_B), (-3.55, "V ₂", ACCENT_C), (-2.05, "V ₃", WARN)):
   g.add(self._rect(cx, 0.62, 0.42, 0.26, col),
         self._sym(0.62, lab, col, FS_TAG, x=cx, w=0.80))
  g.add(self._rect(-4.30, -0.10, 1.30, 0.26, ACCENT_A),
        self._sym(-0.10, "V ₁ × V ₂", ACCENT_A, FS_TAG, x=-4.30, w=2.40))
  g.add(self._rect(-3.30, -0.82, 2.10, 0.26, ACCENT_A),
        self._sym(-0.82, "( V ₁ × V ₂ ) × V ₃", ACCENT_A, FS_TAG, x=-3.30, w=4.00))
  g.add(self._arr([-4.90, 0.32, 0], [-4.55, 0.20, 0], DIM, sw=2, tl=0.10),
        self._arr([-3.70, 0.32, 0], [-4.05, 0.20, 0], DIM, sw=2, tl=0.10),
        self._arr([-4.30, -0.40, 0], [-3.90, -0.52, 0], DIM, sw=2, tl=0.10),
        self._arr([-2.05, 0.32, 0], [-2.35, -0.52, 0], DIM, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "先把前兩個因子併成一個",
                      "merge the first two factors into one", ACCENT_A),
                     (0.20, "再把第三個當成第二個因子加進去",
                      "then add the third as the second factor", WARN),
                     (-0.46, "每一步都是兩個因子的情形",
                      "every step is the two factor case again", ACCENT_B))))
  return g.add(self._foot("連續性讓每一步接得上，所以歸納推得下去",
                          "continuity is what lets each step attach, so the induction goes through",
                          ACCENT_A,
                          "書上把這件事寫成一句「以下類推」，這裡把它畫出來",
                          "the book compresses this into and so on; here it is drawn"))

 def _bilinear(self):
  cx, cy, s = -4.30, 0.05, 0.50
  g = VGroup(self._cross(cx, cy, 1.55, 0.90))
  g.add(self._arr([cx, cy, 0], [cx + s * AVEC[0], cy + s * AVEC[1], 0], ACCENT_B, sw=2.5, tl=0.12),
        self._arr([cx, cy, 0], [cx + s * BVEC[0], cy + s * BVEC[1], 0], ACCENT_C, sw=2.5, tl=0.12))
  para = [[cx, cy, 0],
          [cx + s * AVEC[0], cy + s * AVEC[1], 0],
          [cx + s * (AVEC[0] + BVEC[0]), cy + s * (AVEC[1] + BVEC[1]), 0],
          [cx + s * BVEC[0], cy + s * BVEC[1], 0], [cx, cy, 0]]
  g.add(self._curve(para, WARN, sw=1.6))
  g.add(self._sym(0.86, f"ω ( α , β )   =   {_om(AVEC, BVEC):.0f}", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._sym(0.26, "d ω ( ξ , η )  =  ω ( α , η ) + ω ( ξ , β )", ACCENT_A, FS_TAG,
                  x=PANEL_X, w=PANEL_W))
  rows = [("       t         | rem | / ‖ · ‖", DIM)]
  for k, t in enumerate(SAMPLE):
   rows.append((f"{t:8.3f}            {REM[k]:.6f}", (ACCENT_B, ACCENT_C, WARN)[k % 3]))
  g.add(self._table(rows, y0=-0.30, dy=0.36, size=FS_TAG - 3))
  return g.add(self._foot("這個雙線性映射就是平行四邊形的有向面積，界剛好是一",
                          "this bilinear map is the signed area of the parallelogram, with bound exactly one",
                          ACCENT_A,
                          "餘項是 ω 作用在兩個增量上，所以它是小 o，這就是引理 8.3",
                          "the remainder is omega of the two increments, hence little oh: that is Lemma 8.3"))

 def _hold(self):
  g = VGroup()
  # symbols only: every word in this beat lives in the bilingual panel below
  lines = (("ω ( · , β )     ∈     Hom ( X , W )", ACCENT_B),
           ("d ω ¹     =     ω ( · , β )", ACCENT_C),
           ("β  ↦  ω ( · , β )     ∈     Hom ( Y , Hom ( X , W ) )", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "固定一邊，剩下的就是線性的",
                      "hold one side and what is left is linear", ACCENT_B),
                     (0.20, "所以那個偏微分就是它自己",
                      "so that partial differential is the map itself", ACCENT_C),
                     (-0.46, "而它對點又是線性的，所以連續",
                      "and it depends linearly on the point, hence continuously", WARN))))
  return g.add(self._foot("兩個偏微分都連續，定理 8.2 一套就得到處處可微",
                          "both partials are continuous, so Theorem 8.2 hands back differentiability everywhere",
                          ACCENT_A,
                          "這就是為什麼上半場那條定理要先講：它在這裡立刻用上",
                          "which is why the first half's theorem came first: it is used immediately"))

 def _product(self):
  g = VGroup()
  for cx, lab, col in ((-5.15, "A", ACCENT_B), (-3.05, "X × Y", ACCENT_C), (-0.95, "W", WARN)):
   half = 0.42 if len(lab) < 3 else 0.85
   g.add(self._rect(cx, 0.58, half, 0.28, col),
         self._sym(0.58, lab, col, FS_TAG + 1, x=cx, w=1.70))
  g.add(self._arr([-4.60, 0.58, 0], [-4.00, 0.58, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-2.10, 0.58, 0], [-1.45, 0.58, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(0.94, "⟨ g , h ⟩", ACCENT_A, FS_TAG - 1, x=-4.30, w=1.30),
        self._sym(0.94, "ω", ACCENT_A, FS_TAG - 1, x=-1.78, w=0.60))
  rows = ((f"ω ( g , dh )   =   {PROD_1}", ACCENT_B),
          (f"ω ( dg , h )   =   {PROD_2}", ACCENT_C),
          (f"{PROD_1} + ( {PROD_2} )   =   {PROD_DIRECT}", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(-0.06 - k * 0.40, lab, col, FS_TAG, x=-3.05, w=4.20))
  g.add(self._panel(((0.86, "定理 8.1 給 ⟨g, h⟩ 可微",
                      "Theorem 8.1 makes the pair differentiable", ACCENT_B),
                     (0.20, "引理 8.3 給 ω 可微",
                      "Lemma 8.3 makes omega differentiable", ACCENT_C),
                     (-0.46, "鏈鎖規則把兩件事接起來",
                      "and the chain rule joins the two", WARN))))
  return g.add(self._foot("一項是負的，所以這不是「兩個正數相加」那種乘積規則",
                          "one term is negative, so this is not a rule about adding two positive things",
                          ACCENT_A,
                          "直接對合成微分，答案也是同一個數",
                          "differentiating the composite directly returns the same number"))

 def _summary(self):
  g = VGroup()
  rows = (("d ( F + G ) ₐ   =   dF ₐ + dG ₐ", ACCENT_B),
          ("d ( G ∘ F ) ₐ   =   dG ᵦ ∘ dF ₐ", ACCENT_C),
          ("d ω ( g , h )   =   ω ( g , dh ) + ω ( dg , h )", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._rect(-3.55, 0.72 - k * 0.66, 2.55, 0.26, col),
         self._sym(0.72 - k * 0.66, lab, col, FS_TAG, x=-3.55, w=4.90))
  g.add(self._panel(((0.86, "加法、合成、乘積，三條都有了",
                      "sums, composites and products: all three are in", ACCENT_B),
                     (0.20, "而且從頭到尾沒有用到座標",
                      "and no coordinates were used anywhere", ACCENT_C),
                     (-0.46, "下一集才把它們搬到實數的 n 維空間",
                      "only next time do they move to real n-space", WARN))))
  return g.add(self._foot("第 3 章第 8 節到此結束，這一節是整章最技術的一段",
                          "that ends section 8, the most technical stretch of the chapter",
                          ACCENT_A,
                          "下一集：偏導數、雅可比矩陣，以及矩陣形式的鏈鎖規則",
                          "next time: partial derivatives, the Jacobian matrix, and the chain rule as matrices"))

 def stage(self):
  a, b, c = self._counter(), self._thm82(), self._pinned()
  d, e, f = self._tool(), self._twostep(), self._errors()
  h, i, j = self._induction(), self._bilinear(), self._hold()
  k, l = self._product(), self._summary()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE42ZH, AdvCalcE42EN = make(AdvCalcE42Base, "42", prefix="AdvCalcE")
