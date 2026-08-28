"""advcalc E41 -- chapter 3, section 8, first part (book pp. 152-153): an
m-tuple of functions and a single m-tuple-valued function are the same object,
Theorem 8.1 and its two-line proof through the injections and projections,
Lemma 8.1 for arcs, why a product *domain* is harder, the partial differentials
as restrictions of the differential, the formula expressing the differential as
their sum, the general chain rule, the direct characterisation of a partial
differential by freezing the other variables, and Lemma 8.2.  E42 takes
Theorem 8.2 from page 154; pages 155-156 are exercises 8.1 to 8.10.

The two running examples are a map of the plane whose components are handled
separately (so the assembled Jacobian can be checked against a remainder test)
and the inner product, which is the smallest honest function of two vector
variables.  Its two partial differentials are written down, their sum is
checked against the actual change, and the general chain rule is evaluated on a
concrete pair of inner functions and checked against the composite's own
derivative -- four plus one against five.
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


def _ninf(v):
 return max(abs(x) for x in v)


# ── beats 0 to 2: the range is a product ───────────────────────────────
def _F1(v):
 return v[0] ** 2 + v[1]


def _F2(v):
 return v[0] * v[1]


ALPHA = (1.0, 1.0)


def _grad(f, a):
 return ((f((a[0] + H, a[1])) - f((a[0] - H, a[1]))) / (2 * H),
         (f((a[0], a[1] + H)) - f((a[0], a[1] - H))) / (2 * H))


JAC = (_grad(_F1, ALPHA), _grad(_F2, ALPHA))
assert all(abs(x - round(x)) < 1e-4 for r in JAC for x in r), \
    "the assembled matrix should come out at whole numbers for this point"
JAC = tuple(tuple(round(x) for x in r) for r in JAC)

REM1 = []
for _t in (1e-1, 1e-2, 1e-3):
 _xi = (_t, -_t / 2)
 _d = (_F1((ALPHA[0] + _xi[0], ALPHA[1] + _xi[1])) - _F1(ALPHA),
       _F2((ALPHA[0] + _xi[0], ALPHA[1] + _xi[1])) - _F2(ALPHA))
 _lin = (JAC[0][0] * _xi[0] + JAC[0][1] * _xi[1], JAC[1][0] * _xi[0] + JAC[1][1] * _xi[1])
 REM1.append(_ninf(tuple(a - b for a, b in zip(_d, _lin))) / _ninf(_xi))
assert all(a > b for a, b in zip(REM1, REM1[1:])) and REM1[-1] < 1e-2, \
    "the assembled differential does not actually differentiate the pair"


# ── beat 3: an arc in three dimensions, checked componentwise ──────────
def _arc(t):
 return (math.cos(t), math.sin(t), t / 2)


ARC_T = 0.7
ARC_TAN = tuple((a - b) / (2 * H) for a, b in zip(_arc(ARC_T + H), _arc(ARC_T - H)))
_exact = (-math.sin(ARC_T), math.cos(ARC_T), 0.5)
assert max(abs(a - b) for a, b in zip(ARC_TAN, _exact)) < 1e-5, \
    "the tangent vector is not the componentwise derivative it is drawn as"


# ── beats 4 to 8: the domain is a product; the inner product ───────────
def _dot(u, v):
 return u[0] * v[0] + u[1] * v[1]


AVEC, BVEC = (1.0, 2.0), (3.0, -1.0)
DOT0 = _dot(AVEC, BVEC)


def _p1(xi):
 return _dot(xi, BVEC)          # the first partial differential at (a, b)


def _p2(eta):
 return _dot(AVEC, eta)         # the second


REM2 = []
for _t in (1e-1, 1e-2, 1e-3):
 _xi, _eta = (_t, -_t / 2), (_t / 3, _t)
 _lhs = _dot((AVEC[0] + _xi[0], AVEC[1] + _xi[1]),
             (BVEC[0] + _eta[0], BVEC[1] + _eta[1])) - DOT0
 REM2.append(abs(_lhs - (_p1(_xi) + _p2(_eta))) / max(_ninf(_xi), _ninf(_eta)))
assert all(a > b for a, b in zip(REM2, REM2[1:])) and REM2[-1] < 1e-3, \
    "the two partial differentials do not add up to the differential"

# freezing the other variable gives the same partial differential
for _xi in ((1.0, 0.0), (0.0, 1.0), (1.0, -1.0)):
 _froz = (_dot((AVEC[0] + H * _xi[0], AVEC[1] + H * _xi[1]), BVEC)
          - _dot((AVEC[0] - H * _xi[0], AVEC[1] - H * _xi[1]), BVEC)) / (2 * H)
 assert abs(_froz - _p1(_xi)) < 1e-6, \
     "freezing the second variable should reproduce the first partial differential"


# ── beat 7: the general chain rule on a concrete pair ──────────────────
def _g1(t):
 return (t, t * t)


def _g2(t):
 return (1.0 - t, 2.0 * t)


CT = 1.0
DIRECT = (_dot(_g1(CT + H), _g2(CT + H)) - _dot(_g1(CT - H), _g2(CT - H))) / (2 * H)
D1 = tuple((a - b) / (2 * H) for a, b in zip(_g1(CT + H), _g1(CT - H)))
D2 = tuple((a - b) / (2 * H) for a, b in zip(_g2(CT + H), _g2(CT - H)))
TERM1, TERM2 = _dot(D1, _g2(CT)), _dot(_g1(CT), D2)
assert abs(DIRECT - (TERM1 + TERM2)) < 1e-4, "the general chain rule fails on the drawn example"
assert abs(TERM1 - round(TERM1)) < 1e-4 and abs(TERM2 - round(TERM2)) < 1e-4, \
    "the two terms should be whole numbers, since the beat prints them"
TERM1, TERM2, DIRECT = round(TERM1), round(TERM2), round(DIRECT)
assert TERM1 != TERM2, "two equal terms would hide which is which"


class AdvCalcE41Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 41

 MODE_LABEL = {
  0: {"zh": "m 個函數，就是一個 m 元組值的函數", "en": "m functions are one tuple-valued function"},
  1: {"zh": "定理 8.1：分量可微就整體可微", "en": "Theorem 8.1: componentwise is enough"},
  2: {"zh": "證明靠嵌入與投影都是線性的", "en": "the proof: injections and projections are linear"},
  3: {"zh": "引理 8.1：弧的切向量逐分量算", "en": "Lemma 8.1: a tangent vector, component by component"},
  4: {"zh": "定義域是乘積就沒這麼好", "en": "a product domain is harder"},
  5: {"zh": "偏微分：把微分限制到一個因子", "en": "a partial differential is a restriction"},
  6: {"zh": "微分等於各偏微分之和", "en": "the differential is the sum of the partials"},
  7: {"zh": "一般鏈鎖規則", "en": "the general chain rule"},
  8: {"zh": "把其他變數固定住，也得到同一個東西", "en": "freezing the others gives the same object"},
  9: {"zh": "實務上先遇到的是偏微分", "en": "in practice the partials come first"},
  10: {"zh": "引理 8.2：只有一個方向成立", "en": "Lemma 8.2: only one direction holds"},
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

 def _circ(self, cx, cy, r, col, sw=2.5, n=72):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.40, size=FS_TAG - 2):
  g = VGroup()
  for k, (s, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, s, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _same(self):
  g = VGroup()
  ax, ay = -5.35, 0.05
  g.add(self._circ(ax, ay, 0.42, ACCENT_A, sw=2), Dot([ax, ay, 0], radius=0.055, color=ACCENT_A))
  for dy, col, lab in ((0.55, ACCENT_B, "W ₁"), (-0.55, ACCENT_C, "W ₂")):
   g.add(self._circ(-3.55, ay + dy, 0.30, col, sw=2),
         self._arr([ax + 0.52, ay + 0.18 * (1 if dy > 0 else -1), 0],
                   [-3.95, ay + dy, 0], col, sw=2, tl=0.10),
         self._sym(ay + dy, lab, col, FS_TAG - 2, x=-3.55, w=0.90))
  g.add(self._rect(-1.45, ay, 0.52, 0.72, WARN),
        self._sym(ay + 0.34, "W ₁", ACCENT_B, FS_TAG - 2, x=-1.45, w=0.90),
        self._sym(ay - 0.34, "W ₂", ACCENT_C, FS_TAG - 2, x=-1.45, w=0.90),
        self._arr([-3.15, ay, 0], [-2.10, ay, 0], WARN, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "左邊：兩個函數，各自到一個空間",
                      "left: two functions, each into its own space", ACCENT_B),
                     (0.20, "右邊：一個函數，到乘積空間",
                      "right: one function, into the product", WARN),
                     (-0.46, "這兩件事本來就是同一件事",
                      "these were already the same thing", ACCENT_A))))
  return g.add(self._foot("這一半容易，因為乘積的結構全都在值域那邊",
                          "this half is easy because the product structure sits on the range side",
                          ACCENT_A,
                          "後半段把乘積搬到定義域，情況立刻變得不一樣",
                          "the second half moves the product to the domain, and everything changes"))

 def _thm81(self):
  g = VGroup()
  cx = -3.85
  g.add(self._sym(0.86, f"dF ¹ ₐ   =   ( {JAC[0][0]} , {JAC[0][1]} )", ACCENT_B,
                  FS_TAG + 1, x=cx, w=4.20),
        self._sym(0.24, f"dF ² ₐ   =   ( {JAC[1][0]} , {JAC[1][1]} )", ACCENT_C,
                  FS_TAG + 1, x=cx, w=4.20))
  gr, _ = self._numgrid(cx, -0.58, [[f"{x}" for x in r] for r in JAC], color=WARN, dx=0.62, dy=0.46)
  g.add(gr)
  rows = [("       t         | rem | / ‖ ξ ‖", DIM)]
  for t, r in zip((1e-1, 1e-2, 1e-3), REM1):
   rows.append((f"{t:8.3f}            {r:.5f}", (ACCENT_B, ACCENT_C, WARN)[len(rows) % 3]))
  g.add(self._table(rows, y0=0.62, dy=0.42))
  return g.add(self._foot("兩個分量各自的微分疊起來，就是整個 F 的微分",
                          "stack the two components' differentials and the whole differential appears",
                          ACCENT_A,
                          "右邊那一列是餘項的商，程式算的，它確實掉到零",
                          "the right column is the remainder quotient, computed here, and it does vanish"))

 def _proof81(self):
  g = VGroup()
  boxes = ((-5.05, 0.62, "A", ACCENT_A), (-2.35, 0.62, "W ⱼ", ACCENT_B),
           (-2.35, -0.52, "W", WARN))
  for cx, cy, lab, col in boxes:
   g.add(self._rect(cx, cy, 0.52, 0.28, col),
         self._sym(cy, lab, col, FS_TAG + 1, x=cx, w=0.90))
  g.add(self._arr([-4.45, 0.62, 0], [-2.95, 0.62, 0], ACCENT_B, sw=2.5, tl=0.12),
        self._arr([-2.35, 0.30, 0], [-2.35, -0.20, 0], ACCENT_C, sw=2.5, tl=0.12),
        self._arr([-4.45, 0.42, 0], [-2.95, -0.48, 0], WARN, sw=2.5, tl=0.12))
  g.add(self._sym(0.86, "F ʲ", ACCENT_B, FS_TAG - 1, x=-3.70, w=1.00),
        self._sym(0.05, "θ ⱼ", ACCENT_C, FS_TAG - 1, x=-2.00, w=0.80),
        self._sym(-0.86, "Σ  θ ⱼ ∘ F ʲ   =   F", WARN, FS_TAG - 1, x=-3.70, w=3.20))
  g.add(self._panel(((0.86, "嵌入 θ 與投影 π 都是線性映射",
                      "the injections and projections are linear maps", ACCENT_C),
                     (0.20, "線性映射的微分就是它自己",
                      "and a linear map is its own differential", ACCENT_B),
                     (-0.46, "所以合成與求和都直接過關",
                      "so composing and summing both go through untouched", WARN))))
  return g.add(self._foot("這是 E38 那五條規則第一次真的派上用場",
                          "this is the first place E38's five rules genuinely earn their keep",
                          ACCENT_A,
                          "反方向把分量寫成 π 接上 F，理由一模一樣",
                          "the other direction writes a component as a projection after F, for the same reason"))

 def _arc3(self):
  ox, oy = -3.90, 0.00
  EX, EY, EZ = (0.92, -0.32), (0.62, 0.30), (0.0, 0.62)
  P = lambda x, y, z: [ox + EX[0] * x + EY[0] * y + EZ[0] * z,
                       oy + EX[1] * x + EY[1] * y + EZ[1] * z, 0]
  g = VGroup()
  for a, b in (((-1.25, 0, 0), (1.25, 0, 0)), ((0, -1.25, 0), (0, 1.25, 0)),
               ((0, 0, -0.55), (0, 0, 1.15))):
   g.add(Line(P(*a), P(*b), color=DIM, stroke_width=1.4))
  g.add(self._curve([P(*_arc(2.4 * k / 90 - 0.4)) for k in range(91)], ACCENT_B, sw=3))
  p = _arc(ARC_T)
  g.add(Dot(P(*p), radius=0.065, color=WARN),
        self._arr(P(*p), P(p[0] + 0.85 * ARC_TAN[0], p[1] + 0.85 * ARC_TAN[1],
                           p[2] + 0.85 * ARC_TAN[2]), ACCENT_A, sw=3, tl=0.14))
  rows = [("f ′ ( x )", DIM),
          (f"( {ARC_TAN[0]:.2f} ,  {ARC_TAN[1]:.2f} ,  {ARC_TAN[2]:.2f} )", ACCENT_A)]
  g.add(self._table(rows, y0=0.62, dy=0.48, size=FS_TAG))
  g.add(self._mid(-0.34, "三個分量各自微分，再排成一組",
                  "differentiate each component and gather them up", ACCENT_B, FS_TAG,
                  x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("在座標下算切向量的人做的就是這件事，引理 8.1 只是把它說清楚",
                          "computing a tangent vector in coordinates is exactly this; Lemma 8.1 just says so",
                          ACCENT_A,
                          "它是定理 8.1 在定義域只有一維時的特例",
                          "it is Theorem 8.1 with the domain cut down to one dimension"))

 def _harder(self):
  g = VGroup()
  g.add(self._rect(-4.95, 0.05, 0.95, 0.72, ACCENT_C),
        Line([-4.95, -0.67, 0], [-4.95, 0.77, 0], color=ACCENT_C, stroke_width=1.6),
        self._sym(0.05, "V ₁", ACCENT_B, FS_TAG, x=-5.45, w=0.80),
        self._sym(0.05, "V ₂", WARN, FS_TAG, x=-4.45, w=0.80))
  g.add(self._circ(-1.85, 0.05, 0.46, ACCENT_A, sw=2),
        self._sym(0.05, "W", ACCENT_A, FS_TAG, x=-1.85, w=0.80),
        self._arr([-3.90, 0.05, 0], [-2.45, 0.05, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(0.34, "F", ACCENT_A, FS_TAG - 1, x=-3.18, w=0.70))
  g.add(self._panel(((0.86, "輸入被切成兩塊，函數還是只有一個",
                      "the input is cut in two and the function stays single", ACCENT_C),
                     (0.20, "兩個變數的函數帶的資訊，多於兩個一變數函數",
                      "a function of two variables carries more than two of one", WARN),
                     (-0.46, "所以定義域這一側沒有定理 8.1",
                      "so there is no Theorem 8.1 on the domain side", ACCENT_A))))
  return g.add(self._foot("值域可以拆，是因為「到乘積去」等於「分別到每個因子去」",
                          "the range splits because landing in a product is landing in each factor",
                          ACCENT_A,
                          "定義域不行，因為「從乘積出發」不等於「分別從每個因子出發」",
                          "the domain does not, because starting from a product is not starting from each"))

 def _partial(self):
  g = VGroup()
  cx, cy, w, h = -4.55, 0.05, 1.05, 0.72
  g.add(self._rect(cx, cy, w, h, DIM))
  g.add(Line([cx - 0.30, cy - h, 0], [cx - 0.30, cy + h, 0], color=ACCENT_B, stroke_width=4),
        Dot([cx - 0.30, cy, 0], radius=0.06, color=WARN))
  g.add(self._sym(cy - h - 0.30, "V ₁ × V ₂", DIM, FS_TAG - 1, x=cx, w=2.20))
  g.add(self._circ(-1.60, cy, 0.46, ACCENT_A, sw=2),
        self._arr([cx + w + 0.18, cy, 0], [-2.20, cy, 0], ACCENT_B, sw=2.5, tl=0.12),
        self._sym(cy + 0.32, "dF ² ₐ", ACCENT_B, FS_TAG - 1, x=-2.85, w=1.20))
  g.add(self._panel(((0.86, "把整個微分限制到一個因子上",
                      "restrict the whole differential to one factor", ACCENT_B),
                     (0.20, "得到的就是那個因子的偏微分",
                      "what comes back is that factor's partial differential", ACCENT_A),
                     (-0.46, "它住在「因子到值域」的 Hom 裡",
                      "it lives in the Hom from that factor to the range", WARN))))
  return g.add(self._foot("藍色那一條就是第二個因子，其他座標全部按住不動",
                          "the blue line is the second factor, with every other coordinate pinned",
                          ACCENT_A,
                          "偏微分是映射，不是數——一個因子可以是任何維數的空間",
                          "a partial differential is a map, not a number: a factor may have any dimension"))

 def _sum(self):
  cx, cy, s = -4.45, 0.05, 1.05
  g = VGroup(self._cross(cx, cy, 1.35, 0.85))
  xi, eta = (0.85, 0.0), (0.0, 0.62)
  g.add(self._arr([cx, cy, 0], [cx + s * xi[0], cy + s * xi[1], 0], ACCENT_B, sw=2.5, tl=0.12),
        self._arr([cx + s * xi[0], cy + s * xi[1], 0],
                  [cx + s * (xi[0] + eta[0]), cy + s * (xi[1] + eta[1]), 0],
                  WARN, sw=2.5, tl=0.12),
        self._arr([cx, cy, 0], [cx + s * (xi[0] + eta[0]), cy + s * (xi[1] + eta[1]), 0],
                  ACCENT_A, sw=3, tl=0.12))
  g.add(self._sym(0.86, "ξ    =    θ ₁ ( ξ ₁ )   +   θ ₂ ( ξ ₂ )", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._sym(0.24, "dF ₐ ( ξ )    =    dF ¹ ₐ ( ξ ₁ )   +   dF ² ₐ ( ξ ₂ )", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  rows = [("       t         | rem | / ‖ · ‖", DIM)]
  for t, r in zip((1e-1, 1e-2, 1e-3), REM2):
   rows.append((f"{t:8.3f}            {r:.6f}", (ACCENT_B, ACCENT_C, WARN)[len(rows) % 3]))
  g.add(self._table(rows, y0=-0.16, dy=0.30, size=FS_TAG - 3))
  return g.add(self._foot("向量拆成兩塊，微分是線性的，於是它也跟著拆成兩項",
                          "split the vector in two; the differential is linear, so it splits in two as well",
                          ACCENT_A,
                          "右邊那一列是內積例子的餘項，確實掉到零",
                          "the right column is the inner product example's remainder, and it does vanish"))

 def _chain(self):
  g = VGroup()
  for cx, lab, col in ((-5.10, "ℝ", ACCENT_B), (-2.95, "V ₁ × V ₂", ACCENT_C), (-0.75, "ℝ", WARN)):
   half = 0.42 if lab == "ℝ" else 0.95
   g.add(self._rect(cx, 0.55, half, 0.28, col),
         self._sym(0.55, lab, col, FS_TAG + 1, x=cx, w=1.80))
  g.add(self._arr([-4.55, 0.55, 0], [-4.00, 0.55, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-1.90, 0.55, 0], [-1.25, 0.55, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._sym(0.90, "G", ACCENT_A, FS_TAG - 1, x=-4.28, w=0.60),
        self._sym(0.90, "F", ACCENT_A, FS_TAG - 1, x=-1.58, w=0.60))
  rows = [(f"dF ¹ ( g ¹ ′ )   =   {TERM1}", ACCENT_B),
          (f"dF ² ( g ² ′ )   =   {TERM2}", ACCENT_C),
          (f"{TERM1} + {TERM2}   =   {DIRECT}", WARN)]
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(-0.08 - k * 0.40, lab, col, FS_TAG, x=-2.95, w=4.20))
  g.add(self._panel(((0.86, "外函數吃兩個變數，內函數有兩支",
                      "the outer map takes two variables and the inner has two arms", ACCENT_C),
                     (0.20, "每支各配一個偏微分，再加起來",
                      "each arm gets its own partial differential, then they add", ACCENT_A),
                     (-0.46, "直接對合成微分，答案一樣",
                      "differentiating the composite directly gives the same", WARN))))
  return g.add(self._foot("這就是一般的鏈鎖規則，也是課本裡那條偏導數連鎖公式的來源",
                          "this is the general chain rule, and the source of the usual partial derivative formula",
                          ACCENT_A,
                          "畫面上的三個數字都是程式算的，加起來確實對得上",
                          "the three numbers on screen were computed here, and they do add up"))

 def _freeze(self):
  cx, cy, w, h = -4.30, 0.05, 1.35, 0.80
  g = VGroup(self._rect(cx, cy, w, h, DIM))
  for k in range(-3, 4):
   g.add(Line([cx - w, cy + h * k / 4, 0], [cx + w, cy + h * k / 4, 0],
              color=DIM, stroke_width=0.8))
  g.add(Line([cx - w, cy + h * 0.25, 0], [cx + w, cy + h * 0.25, 0], color=WARN, stroke_width=4),
        Dot([cx - 0.35, cy + h * 0.25, 0], radius=0.06, color=ACCENT_A))
  g.add(self._sym(cy - h - 0.18, "ξ ₂  =  α ₂", WARN, FS_TAG - 1, x=cx, w=2.20))
  g.add(self._panel(((0.86, "把第二個變數釘在 α₂，只留第一個能動",
                      "pin the second variable at alpha two and let only the first move", WARN),
                     (0.20, "剩下的是一個一變數的函數",
                      "what is left is a function of one variable", ACCENT_B),
                     (-0.46, "它的微分就是第一個偏微分",
                      "its differential is the first partial differential", ACCENT_A))))
  return g.add(self._foot("兩個定義是同一個東西：限制整個微分，或者先固定再微分",
                          "the two definitions agree: restrict the differential, or freeze first and then differentiate",
                          ACCENT_A,
                          "程式在內積那個例子上把兩條路各走一次，結果相同",
                          "both routes were walked on the inner product example here and came out the same"))

 def _practice(self):
  g = VGroup()
  for cy, lab, col in ((0.52, "dF ¹ ₐ", ACCENT_B), (-0.32, "dF ² ₐ", ACCENT_C)):
   g.add(self._rect(-4.85, cy, 0.85, 0.26, col),
         self._sym(cy, lab, col, FS_TAG, x=-4.85, w=1.50))
  g.add(self._rect(-1.95, 0.10, 0.85, 0.26, WARN),
        self._sym(0.10, "dF ₐ", WARN, FS_TAG, x=-1.95, w=1.50))
  g.add(self._arr([-3.90, 0.44, 0], [-2.90, 0.20, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([-3.90, -0.24, 0], [-2.90, 0.00, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "先算得出來的是左邊那兩個",
                      "the two on the left are what can be computed first", ACCENT_B),
                     (0.20, "右邊那個是後來拼出來的",
                      "the one on the right is assembled afterwards", WARN),
                     (-0.46, "跟定義的順序剛好相反",
                      "the reverse of the order the definitions came in", ACCENT_A))))
  return g.add(self._foot("定義從整個微分往下切，計算從偏微分往上拼",
                          "the definition cuts downward from the whole; computing builds upward from the parts",
                          ACCENT_A,
                          "所以「偏微分存在能不能推出可微」是一個真的問題，下一集回答",
                          "so whether the partials force differentiability is a real question, answered next time"))

 def _lemma82(self):
  g = VGroup()
  for cx, lab, col in ((-4.95, "dF ₐ   ∃", WARN), (-1.85, "dF ⁱ ₐ   ∃", ACCENT_B)):
   g.add(self._rect(cx, 0.32, 1.05, 0.30, col),
         self._sym(0.32, lab, col, FS_TAG + 1, x=cx, w=1.90))
  g.add(self._arr([-3.80, 0.44, 0], [-3.00, 0.44, 0], ACCENT_A, sw=3, tl=0.14),
        self._arr([-3.00, 0.10, 0], [-3.80, 0.10, 0], DIM, sw=2, tl=0.10),
        self._curve([[-3.55, -0.02, 0], [-3.25, 0.22, 0]], WARN, sw=3),
        self._curve([[-3.25, -0.02, 0], [-3.55, 0.22, 0]], WARN, sw=3))
  g.add(self._sym(-0.60, "dF ⁱ ₐ    =    dF ₐ ∘ θ ᵢ", ACCENT_A, FS_TAG + 1, x=-3.40, w=3.80))
  g.add(self._panel(((0.86, "往右成立：可微就有全部偏微分",
                      "rightward holds: differentiable gives every partial", ACCENT_A),
                     (0.20, "而且它們就等於那些限制",
                      "and they are exactly those restrictions", ACCENT_B),
                     (-0.46, "往左一般不成立，下一集補條件",
                      "leftward generally fails; next time supplies the condition", WARN))))
  return g.add(self._foot("這一集只證了容易的那個方向，難的那個方向要用均值定理",
                          "only the easy direction is proved here; the hard one needs the mean value theorem",
                          ACCENT_A,
                          "下一集：連續的偏微分推得出可微，還有一般的乘積規則",
                          "next time: continuous partials do give differentiability, and the general product rule"))

 def stage(self):
  a, b, c = self._same(), self._thm81(), self._proof81()
  d, e, f = self._arc3(), self._harder(), self._partial()
  h, i, j = self._sum(), self._chain(), self._freeze()
  k, l = self._practice(), self._lemma82()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE41ZH, AdvCalcE41EN = make(AdvCalcE41Base, "41", prefix="AdvCalcE")
