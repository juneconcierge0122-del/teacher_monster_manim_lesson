"""advcalc E54 -- chapter 3, section 16, second part (book pp. 189-191): the
classification of critical points.  With the differential vanishing and the
second differential nonsingular, an omega-orthonormal basis turns the quadratic
form into a signed sum of squares; the number p of plus signs classifies the
point, and Theorem 16.4 handles p equal to n.  The proof squeezes the increment
between two very close quadratic surfaces of the same type, which is stronger
than the bare statement.  Section 16 has no exercises.

The classification is checked twice over on three examples, once by the
determinant rule and once by brute force.  Each example's Hessian is computed by
central differences, the determinant rule is applied to it, and separately the
function is sampled on a ring around the critical point to see whether it rises
everywhere, falls everywhere, or does both; the two verdicts are asserted to
agree.  The paraboloid sandwich of Theorem 16.4's proof is checked as an
inequality at many points rather than quoted, and the omega-orthonormal basis of
beat 1 is actually constructed and its pairings verified.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
H = 1e-4


def _grad(f, a):
 out = []
 for j in range(2):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  out.append((f(tuple(p)) - f(tuple(m))) / (2 * H))
 return tuple(out)


def _hess(f, a):
 e = ((1.0, 0.0), (0.0, 1.0))
 row = lambda i: [( _dirdir(f, a, e[i], e[j]) ) for j in range(2)]
 return [row(0), row(1)]


def _dirdir(f, a, u, v, h=1e-3):
 """A second directional derivative, by a symmetric four-point difference."""
 p = lambda su, sv: f(tuple(x + su * h * du + sv * h * dv
                           for x, du, dv in zip(a, u, v)))
 return (p(1, 1) - p(1, -1) - p(-1, 1) + p(-1, -1)) / (4 * h * h)


# ── beat 1: an omega-orthonormal basis, actually constructed ───────────
OMEGA = ((1.0, 2.0), (2.0, 1.0))


def _om(u, v, m=OMEGA):
 return sum(u[i] * m[i][j] * v[j] for i in range(2) for j in range(2))


def _orthonormalise(m):
 """Gram-Schmidt with signs: the diagonal comes out at plus or minus one."""
 basis = []
 for e in ((1.0, 0.0), (0.0, 1.0)):
  v = list(e)
  for b in basis:
   c = _om(tuple(v), b, m) / _om(b, b, m)
   v = [x - c * y for x, y in zip(v, b)]
  basis.append(tuple(v))
 out = []
 for b in basis:
  s = _om(b, b, m)
  out.append(tuple(x / math.sqrt(abs(s)) for x in b))
 return out


BASIS = _orthonormalise(OMEGA)
PAIR = [[_om(BASIS[i], BASIS[j]) for j in range(2)] for i in range(2)]
assert abs(PAIR[0][1]) < 1e-9 and abs(PAIR[1][0]) < 1e-9, "the basis is not omega-orthogonal"
assert abs(PAIR[0][0] - 1.0) < 1e-9 and abs(PAIR[1][1] + 1.0) < 1e-9, \
    "the diagonal should come out at plus one and minus one"
P_INDEX = sum(1 for i in range(2) if PAIR[i][i] > 0)
assert P_INDEX == 1, "this form is indefinite, so p is one and the point would be a saddle"


# ── beats 3, 8 and 9: three critical points, classified two ways ───────
def _fmin(v):
 return v[0] ** 2 + 3 * v[1] ** 2 + v[0] ** 3


def _fmax(v):
 return -2 * v[0] ** 2 - v[1] ** 2 + v[0] * v[1] ** 2


def _fsad(v):
 return v[0] ** 2 - v[1] ** 2 + v[0] ** 3 * v[1]


def _by_determinant(f):
 hh = _hess(f, (0.0, 0.0))
 det = hh[0][0] * hh[1][1] - hh[0][1] * hh[1][0]
 if det < 0:
  return "saddle", hh, det
 return ("min" if hh[0][0] > 0 else "max"), hh, det


def _by_sampling(f, r=0.05, n=360):
 vals = [f((r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)))
         for k in range(n)]
 lo, hi = min(vals), max(vals)
 if lo > 0:
  return "min"
 if hi < 0:
  return "max"
 return "saddle"


CASES = []
for _f, _name in ((_fmin, "min"), (_fsad, "saddle"), (_fmax, "max")):
 assert max(abs(g) for g in _grad(_f, (0.0, 0.0))) < 1e-6, "the origin is not critical"
 _verdict, _hh, _det = _by_determinant(_f)
 assert _verdict == _by_sampling(_f) == _name, \
     "the determinant rule and brute-force sampling disagree"
 CASES.append((_name, _hh, _det))
assert len({c[0] for c in CASES}) == 3, "the three cases have to be different"


# ── beats 5 to 7: the sandwich of Theorem 16.4's proof ─────────────────
def _fq(v):
 """A function whose second differential at the origin is the identity."""
 return (v[0] ** 2 + v[1] ** 2) / 2 + v[0] ** 3


DELTA = 0.05
EPS = 0.11
RING = [(r * math.cos(a), r * math.sin(a))
        for r in (DELTA, DELTA / 2, DELTA / 5)
        for a in (2 * math.pi * k / 72 for k in range(72))]
for _x in RING:
 _n2 = _x[0] ** 2 + _x[1] ** 2
 assert (1 - EPS) * _n2 / 2 <= _fq(_x) <= (1 + EPS) * _n2 / 2, \
     "the increment escaped the two paraboloids"
# and the bound is not slack: at the edge it very nearly touches
_edge = max(abs(2 * _fq(_x) / (_x[0] ** 2 + _x[1] ** 2) - 1.0) for _x in RING)
assert _edge > 0.5 * EPS, "the epsilon chosen is far larger than it needs to be"


class AdvCalcE54Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 54

 MODE_LABEL = {
  0: {"zh": "兩個假設", "en": "two hypotheses"},
  1: {"zh": "ω 正交基：化成有正負號的平方和", "en": "an omega-orthonormal basis"},
  2: {"zh": "對角線上不能有零", "en": "no zero on the diagonal"},
  3: {"zh": "p 從 0 到 n，共 n + 1 種", "en": "p from zero to n: n plus one cases"},
  4: {"zh": "定理 16.4：正定就是極小", "en": "Theorem 16.4: positive definite means minimum"},
  5: {"zh": "證明：把導數夾起來", "en": "the proof: squeeze the derivative"},
  6: {"zh": "積分之後：夾在兩個拋物面之間", "en": "integrate: between two paraboloids"},
  7: {"zh": "一般的 p：夾在兩個同型的曲面之間", "en": "general p: two surfaces of one type"},
  8: {"zh": "鞍點：往下那一片有幾維", "en": "a saddle: how many dimensions go down"},
  9: {"zh": "兩個變數的捷徑", "en": "the shortcut for two variables"},
  10: {"zh": "換到完備空間上照樣成立", "en": "it survives on a complete space"},
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

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 EX, EY, EZ = (0.90, -0.30), (0.62, 0.30), (0.0, 0.74)

 def _P(self, ox, oy, x, y, z):
  return [ox + self.EX[0] * x + self.EY[0] * y + self.EZ[0] * z,
          oy + self.EX[1] * x + self.EY[1] * y + self.EZ[1] * z, 0]

 def _quadric(self, ox, oy, sp, sm, col, sw=1.9, scale=0.62, ext=1.0):
  """The surface z = sp x^2 + sm y^2, drawn as a mesh in the shared frame.

  `ext` is the half-width in domain units. At ext = 1 the mesh reaches about
  1.5 units either side of ox, which is too wide to put three of them in a row.
  """
  g = VGroup()
  q = lambda a, b: scale * (sp * a * a + sm * b * b)
  for u in (-1.0, -0.5, 0.0, 0.5, 1.0):
   uu = ext * u
   g.add(self._curve([self._P(ox, oy, uu, ext * v / 8.0, q(uu, ext * v / 8.0))
                      for v in range(-8, 9)], col, sw=sw),
         self._curve([self._P(ox, oy, ext * v / 8.0, uu, q(ext * v / 8.0, uu))
                      for v in range(-8, 9)], col, sw=sw))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _hypotheses(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("df ₐ   =   0", ACCENT_B),
                                  ("( d ² f ₐ ) ⁻¹    ∃", WARN))):
   g.add(self._rect(-4.55, 0.48 - k * 0.84, 1.35, 0.30, col),
         self._sym(0.48 - k * 0.84, lab, col, FS_TAG + 1, x=-4.55, w=2.50))
  g.add(self._arr([-3.05, 0.06, 0], [-2.55, 0.06, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-1.45, 0.06, 1.00, 0.30, ACCENT_A),
        self._sym(0.06, "p   ∈   { 0 , … , n }", ACCENT_A, FS_TAG, x=-1.45, w=1.90))
  g.add(self._panel(((0.86, "第一個假設：那一點是臨界點",
                      "first: the point is critical", ACCENT_B),
                     (0.20, "第二個：二階微分存在，而且非奇異",
                      "second: the second differential exists and is nonsingular", WARN),
                     (-0.46, "有了這兩個，那一點就落進 n 加一類的其中一類",
                      "with both, the point falls into one of n plus one classes", ACCENT_A))))
  return g.add(self._foot("非奇異的意思是：它對應的那個雙線性形式，在任何一組基底下的矩陣都可逆",
                          "nonsingular means the bilinear form it corresponds to has an invertible matrix in any basis",
                          ACCENT_A,
                          "少了第二個假設就什麼都說不出來——那正是 E44 最後那個馬鞍面之外的情況",
                          "without the second hypothesis nothing can be said, which is the case E44's saddle left open"))

 def _orthobasis(self):
  g = VGroup()
  gr, _ = self._numgrid(-5.00, 0.46, [[f"{v:.0f}" for v in row] for row in OMEGA],
                        color=DIM, dx=0.62, dy=0.50, size=FS_TAG)
  g.add(gr, self._sym(-0.18, "ω", DIM, FS_TAG, x=-5.00, w=1.20))
  g.add(self._arr([-4.05, 0.46, 0], [-3.55, 0.46, 0], ACCENT_A, sw=2.5, tl=0.12))
  gr2, _ = self._numgrid(-2.60, 0.46, [[f"{v:.0f}" for v in row] for row in PAIR],
                         color=WARN, dx=0.62, dy=0.50, size=FS_TAG)
  g.add(gr2, self._sym(-0.18, "ω ( α ᵢ , α ⱼ )", WARN, FS_TAG - 1, x=-2.60, w=2.10))
  g.add(self._sym(-0.80, f"α ₁  =  ⟨ {BASIS[0][0]:.2f} , {BASIS[0][1]:.2f} ⟩       "
                         f"α ₂  =  ⟨ {BASIS[1][0]:.2f} , {BASIS[1][1]:.2f} ⟩",
                  ACCENT_C, FS_TAG - 2, x=-3.55, w=4.60))
  g.add(self._panel(((0.86, "第 2 章定理 7.1：對稱雙線性形式有 ω 正交基",
                      "Theorem 7.1 of chapter 2 gives an omega-orthonormal basis", ACCENT_B),
                     (0.20, "不同的兩個基向量配出來是零",
                      "two different basis vectors pair to zero", ACCENT_C),
                     (-0.46, "同一個配自己是正一或負一",
                      "and each pairs with itself to plus or minus one", WARN))))
  return g.add(self._foot("畫面上那組基底是程式用帶正負號的 Gram–Schmidt 真的算出來的，配對的結果驗過",
                          "the basis on screen was actually constructed here by a signed Gram-Schmidt and its pairings checked",
                          ACCENT_A,
                          "這個 ω 的行列式是負三，所以正負各一個——換句話說 p 等於一",
                          "this form has determinant minus three, so one plus and one minus, that is p equal to one"))

 def _nozero(self):
  g = VGroup()
  gr, pos = self._numgrid(-4.35, 0.42, [["1", "0", "0"], ["0", "0", "0"], ["0", "0", "− 1"]],
                          color=DIM, dx=0.72, dy=0.52, size=FS_TAG,
                          hot=((1, 1),), hotcolor=WARN)
  g.add(gr)
  x1 = pos(0, 1)[0]
  g.add(self._rect(x1, 0.42, 0.30, 0.80, WARN, sw=2.0))
  g.add(self._sym(-0.62, "det   =   0", WARN, FS_TAG + 1, x=-4.35, w=2.40))
  g.add(self._panel(((0.86, "如果對角線上有一個零",
                      "if one zero sat on the diagonal", WARN),
                     (0.20, "那一整欄就都是零",
                      "that whole column would vanish", ACCENT_C),
                     (-0.46, "矩陣就奇異了，跟假設矛盾",
                      "the matrix would be singular, against the hypothesis", ACCENT_A))))
  return g.add(self._foot("因為 ω 正交，第 i 欄除了對角線那一格以外本來就全是零",
                          "omega-orthogonality already makes every entry of the ith column zero except the diagonal one",
                          ACCENT_A,
                          "所以「非奇異」這個假設，正好是「對角線上只有正一與負一」的保證",
                          "so nonsingularity is exactly what guarantees the diagonal carries only plus and minus ones"))

 def _cases(self):
  g = VGroup()
  for k, (ox, sp, sm, col) in enumerate(((-4.95, 1.0, 1.0, ACCENT_B),
                                         (-2.75, 1.0, -1.0, WARN),
                                         (-0.55, -1.0, -1.0, ACCENT_C))):
   g.add(self._quadric(ox, 0.02, sp, sm, col, sw=1.6, scale=0.40, ext=0.70))
   g.add(self._sym(-0.95, f"p  =  {2 - k}", col, FS_TAG - 1, x=ox, w=1.30))
  g.add(self._sym(0.86, "q ( x )   =   Σ ₁ ᵖ  x ᵢ ²   −   Σ ᵖ ⁺ ¹ ⁿ  x ᵢ ²",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "混合的二階偏導數全是零", "all the mixed second partials vanish",
                  DIM, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "對角線上前 p 個是正一、其餘是負一",
                  "the diagonal is plus one p times and minus one after", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以一共有 n 加一種可能",
                  "so there are n plus one possibilities in all", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("兩個變數的時候就是三種：極小、鞍點、極大，畫面上由左到右",
                          "for two variables that is three, left to right: minimum, saddle, maximum",
                          ACCENT_A,
                          "n 維時中間的鞍點還細分成 n 減一種，差別在「往下」那一片有幾維",
                          "in n dimensions the saddle splits into n minus one kinds by how many directions go down"))

 def _thm164(self):
  g = VGroup(self._quadric(-4.35, -0.30, 1.0, 1.0, ACCENT_B, sw=2.0, scale=0.58))
  g.add(Dot(self._P(-4.35, -0.30, 0, 0, 0), radius=0.075, color=WARN))
  g.add(self._rect(PANEL_X, 0.60, 2.10, 0.30, ACCENT_A),
        self._sym(0.60, "q   ≻   0        ⇒        Δ f ₐ   ≥   0", ACCENT_A,
                  FS_TAG + 1, x=PANEL_X, w=4.00))
  g.add(self._mid(0.00, "正定就是 p 等於 n", "positive definite means p equals n",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.58, "也就是那個二次型對每一個非零向量都是正的",
                  "that is, the form is positive on every nonzero vector", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("結論是相對極小；證明給的其實比這句話更強，下兩拍會看到",
                          "the conclusion is a relative minimum, and the proof gives more than that, as the next two beats show",
                          ACCENT_A,
                          "負定的情形把 f 換成負 f 就好，不必另外證",
                          "the negative definite case follows by replacing f with minus f"))

 def _squeeze(self):
  ox, oy = -5.65, -0.55
  sx, sy = 4.30, 1.30
  X = lambda t: ox + t * sx
  Y = lambda v: oy + v * sy
  g = VGroup(Line([ox - 0.12, oy, 0], [X(1.06), oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.12, 0], [ox, Y(1.30), 0], color=DIM, stroke_width=1.4))
  for c, col, sw in ((1 + EPS, ACCENT_C, 1.8), (1.0, DIM, 1.4), (1 - EPS, ACCENT_B, 1.8)):
   g.add(self._curve([[X(k / 40.0), Y(c * k / 40.0), 0] for k in range(41)], col, sw=sw))
  g.add(self._curve([[X(k / 40.0), Y((k / 40.0) * (1 + 0.7 * EPS * math.sin(5 * k / 40.0))), 0]
                     for k in range(41)], WARN, sw=2.8))
  g.add(self._panel(((0.86, "紅色是 h 的導數，沿著射線走",
                      "red is the derivative of h along the ray", WARN),
                     (0.20, "它被夾在兩條斜率差 ε 的直線之間",
                      "squeezed between two lines whose slopes differ by epsilon", ACCENT_C),
                     (-0.46, "夾擊來自二階微分的定義，加上微分是零",
                      "the squeeze comes from the definition, plus the differential vanishing", ACCENT_A))))
  return g.add(self._foot("h 是把 f 限制到一條射線上得到的一元函數，它的導數就是 df 作用在方向上",
                          "h is f restricted to a ray, and its derivative is df applied to the direction",
                          ACCENT_A,
                          "整個證明就是一維的手法：把多變數的估計壓到一條射線上再積分",
                          "the whole proof is a one variable manoeuvre: push the estimate onto a ray and integrate"))

 def _sandwich(self):
  # The sandwich only holds for norms up to delta, so it has to be plotted over
  # that range; a first version drew it out to one and the curve left the frame
  # by more than a unit, which is exactly what the theorem does not claim.
  ox, oy = -5.65, -0.70
  sx, sy = 4.30, 1.50
  VMAX = (1 + EPS) * DELTA ** 2 / 2
  X = lambda t: ox + t / DELTA * sx
  Y = lambda v: oy + v / VMAX * sy
  g = VGroup(Line([ox - 0.12, oy, 0], [X(DELTA * 1.06), oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.12, 0], [ox, Y(VMAX * 1.12), 0], color=DIM, stroke_width=1.4))
  for c, col, sw in (((1 + EPS) / 2, ACCENT_C, 1.8), ((1 - EPS) / 2, ACCENT_B, 1.8)):
   g.add(self._curve([[X(DELTA * k / 40.0), Y(c * (DELTA * k / 40.0) ** 2), 0]
                      for k in range(41)], col, sw=sw))
  g.add(self._curve([[X(DELTA * k / 40.0), Y(_fq((DELTA * k / 40.0, 0.0))), 0]
                     for k in range(41)], WARN, sw=2.8))
  g.add(self._sym(0.86, "( 1 − ϵ ) ‖ x ‖ ² / 2    ≤    Δ f ₐ    ≤    ( 1 + ϵ ) ‖ x ‖ ² / 2",
                  ACCENT_A, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.20, "不只是「有極小」", "not merely that there is a minimum",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.38, "增量夾在兩個非常接近的拋物面之間",
                  "the increment lies between two very close paraboloids", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.96, f"程式在 216 個點上驗過這個夾擊（ϵ = {EPS:.2f}）",
                  f"the squeeze was checked here at 216 points, with epsilon {EPS:.2f}", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("夾擊是把上一拍那條不等式對 t 從零積到一得到的，左邊剛好是函數的增量",
                          "the sandwich is the last beat's inequality integrated from zero to one, whose left side is the increment",
                          ACCENT_A,
                          "而且那個 ε 不是隨便取寬的：在邊界上實際的偏差已經用掉它的一半以上",
                          "and the epsilon is not slack: at the edge the actual deviation already uses more than half of it"))

 def _generalp(self):
  g = VGroup()
  g.add(self._quadric(-4.55, -0.15, 1.0, -(1 - EPS), ACCENT_B, sw=1.5, scale=0.50, ext=0.72),
        self._quadric(-1.85, -0.15, 1.0, -(1 + EPS), ACCENT_C, sw=1.5, scale=0.50, ext=0.72))
  g.add(self._sym(0.86, "( q ( x ) − ϵ ‖ x ‖ ² ) / 2   ≤   Δ f ₐ   ≤   ( q ( x ) + ϵ ‖ x ‖ ² ) / 2",
                  ACCENT_A, FS_TAG - 2, x=PANEL_X, w=PANEL_W),
        self._mid(0.20, "把長度平方換成那個二次型",
                  "replace the squared length by the quadratic form", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.38, "增量夾在兩個同型的二次曲面之間",
                  "the increment lies between two quadric surfaces of one type", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.96, "前 p 個座標的係數是一減 ε 與一加 ε，後面那些反過來",
                  "the first p coefficients are one minus and one plus epsilon, the rest reversed",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("畫面上兩張是同一個鞍面被 ε 撐開的上下界，形狀相同、只差一點點",
                          "the two sheets are the upper and lower bounds on one saddle, the same shape a little apart",
                          ACCENT_A,
                          "「同型」是關鍵：夾住它的兩個曲面跟它自己是同一種二次曲面",
                          "same type is the point: the two surfaces bounding it are quadrics of its own kind"))

 def _saddle(self):
  ox, oy = -4.15, -0.15
  g = VGroup(self._quadric(ox, oy, 1.0, -1.0, DIM, sw=1.3, scale=0.55))
  g.add(self._curve([self._P(ox, oy, v / 8.0, 0.0, 0.55 * (v / 8.0) ** 2)
                     for v in range(-8, 9)], ACCENT_B, sw=3),
        self._curve([self._P(ox, oy, 0.0, v / 8.0, -0.55 * (v / 8.0) ** 2)
                     for v in range(-8, 9)], WARN, sw=3),
        Dot(self._P(ox, oy, 0, 0, 0), radius=0.07, color=ACCENT_A))
  g.add(self._sym(0.86, "V ₁  =  L ( δ ¹ , … , δ ᵖ )        V ₂  =  L ( δ ᵖ ⁺ ¹ , … , δ ⁿ )",
                  ACCENT_A, FS_TAG - 2, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "藍色那一片：在 V₁ 上是相對極小",
                  "blue: a relative minimum on the first subspace", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "紅色那一片：在 V₂ 上是相對極大",
                  "red: a relative maximum on the complementary one", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "往下那一片的維數就是 n 減 p",
                  "the downward subspace has dimension n minus p", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("所以鞍點不是一種，而是 n 減一種——差別在往下那一片有幾維",
                          "so a saddle is not one thing but n minus one things, told apart by that dimension",
                          ACCENT_A,
                          "兩個變數時只有一種鞍點，所以這個細分在平面上看不出來",
                          "with two variables there is only one kind, so the distinction is invisible in the plane"))

 def _shortcut(self):
  g = VGroup()
  for k, (name, hh, det) in enumerate(CASES):
   cx = -5.20 + k * 2.25
   gr, _ = self._numgrid(cx, 0.50, [[f"{v:.0f}" for v in row] for row in hh],
                         color=(ACCENT_B, WARN, ACCENT_C)[k], dx=0.62, dy=0.48, size=FS_TAG - 1)
   g.add(gr, self._sym(-0.22, f"det  =  {det:.0f}", (ACCENT_B, WARN, ACCENT_C)[k],
                       FS_TAG - 1, x=cx, w=1.90),
         self._sym(-0.74, f"f ₓₓ  =  {hh[0][0]:.0f}", DIM, FS_TAG - 2, x=cx, w=1.90))
  g.add(self._panel(((0.86, "行列式是正的：極大或極小",
                      "a positive determinant: a maximum or a minimum", ACCENT_B),
                     (0.20, "沿一條直線走一下就知道是哪一個",
                      "and following one line says which of the two", ACCENT_C),
                     (-0.46, "行列式是負的：鞍點",
                      "a negative determinant: a saddle", WARN))))
  return g.add(self._foot("三個矩陣都是程式用差商算的，而且每一個都用兩種方法分類過：行列式的規則，以及在一圈上取樣",
                          "all three matrices were computed here, and each was classified two ways: by the determinant rule and by sampling a ring",
                          ACCENT_A,
                          "兩種方法在三個例子上結論都相同，所以那條規則不是背下來的，是驗過的",
                          "the two verdicts agree on all three, so the rule is checked here rather than recited"))

 def _banach(self):
  g = VGroup()
  rows = (("q   ≻   0", ACCENT_B),
          ("q ¹ ᐟ ²    ≈    ‖ · ‖", ACCENT_C))
  for k, (lab, col) in enumerate(rows):
   g.add(self._rect(-4.55, 0.50 - k * 0.80, 1.25, 0.30, col),
         self._sym(0.50 - k * 0.80, lab, col, FS_TAG + 1, x=-4.55, w=2.30))
  g.add(self._arr([-3.15, 0.10, 0], [-2.65, 0.10, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-1.55, 0.10, 1.15, 0.30, WARN),
        self._mid(0.10, "仍然是極小", "still a minimum", WARN, FS_TAG, x=-1.55, w=2.10))
  g.add(self._panel(((0.86, "定義域換成無窮維的完備空間",
                      "let the domain be an infinite dimensional complete space", ACCENT_B),
                     (0.20, "假設改成二次型正定，而且它的範數與原範數等價",
                      "assume the form positive definite and its norm equivalent to the given one", ACCENT_C),
                     (-0.46, "證明幾乎一個字都不用改",
                      "and the proof is virtually unchanged", WARN))))
  return g.add(self._foot("這一句是給變分法用的：E52 那個弧的空間就是無窮維的，二階微分叫第二變分",
                          "this is for the calculus of variations: E52's space of arcs is infinite dimensional, and the second differential is the second variation",
                          ACCENT_A,
                          "第 3 章第 16 節到此結束，下一集講第 17 節的 Taylor 公式，也是這一章最後一節",
                          "that ends section 16; next is section 17 on the Taylor formula, the last of the chapter"))

 def stage(self):
  a, b, c = self._hypotheses(), self._orthobasis(), self._nozero()
  d, e, f = self._cases(), self._thm164(), self._squeeze()
  h, i, j = self._sandwich(), self._generalp(), self._saddle()
  k, l = self._shortcut(), self._banach()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE54ZH, AdvCalcE54EN = make(AdvCalcE54Base, "54", prefix="AdvCalcE")
