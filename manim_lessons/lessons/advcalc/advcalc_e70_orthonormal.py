"""advcalc E70 -- chapter 5, section 2, second half (book pp. 254-256): orthonormal
sequences, Bessel, bases, Gram-Schmidt, and the Riesz theorem.

Everything here comes out of one identity.  If the first n terms of the Fourier
series are summed, that partial sum is the projection on the span of those n
vectors (E69's Lemmas 2.3 and 2.4), so the difference is orthogonal to it and
Pythagoras gives ||xi - sigma_n||^2 = ||xi||^2 - sum of the squares of the first
n coefficients.  Read one way that is Bessel's inequality; read the other way it
is Parseval's condition, which is exactly when the Fourier series converges to
the vector.  A sequence whose Fourier series always converges is a basis
(Theorem 2.3: iff its span is dense; corollary: in a Hilbert space, iff nothing
but zero is orthogonal to all of it), orthogonal bases are singled out because
the coefficient at one basis vector does not depend on the others, Lemma 2.5
orthogonalises any independent sequence, and Theorem 2.4 closes the section: the
map sending a vector to the functional "take the product with me" is an
isomorphism exactly when the space is complete.

This finishes section 2; exercises 2.1 to 2.11 run from 256 to 257 and section 3
(self-adjoint transformations) starts on 257.

The numbers are computed in C([0, pi]) with the normalised sines, against the
constant function -- whose Fourier sine series converges slowly enough to see,
overshooting near both ends.  The counterexample family is the even sines alone,
where the constant's coefficients are all zero, Bessel is satisfied with room to
spare and Parseval fails completely.  Gram-Schmidt is run on 1, x, x^2 over the
unit interval and reproduces the book's own answer.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
PI = math.pi


def simpson(g, a, b, n=2000):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


def sp(f, g, a=0.0, b=PI):
 return simpson(lambda t: f(t) * g(t), a, b)


def nm(f, a=0.0, b=PI):
 return math.sqrt(sp(f, f, a, b))


# ── the orthonormal sines, and the constant function to expand ─────────
def phi(k):
 return lambda t: math.sqrt(2.0 / PI) * math.sin(k * t)


for _k in (1, 2, 3):
 assert abs(nm(phi(_k)) - 1.0) < 1e-9, "normalised: each has length one"
assert abs(sp(phi(1), phi(2))) < 1e-12 and abs(sp(phi(1), phi(3))) < 1e-12, \
    "and they are orthogonal, so the collection is orthonormal"


def XI(t):
 return 1.0


NX2 = sp(XI, XI)
assert abs(NX2 - PI) < 1e-9, "the constant function has square norm pi on this interval"
NCO = 7
X = [sp(XI, phi(k)) for k in range(1, NCO + 1)]
assert abs(X[0] - math.sqrt(2.0 / PI) * 2.0) < 1e-9, "the odd coefficients are two over n"
assert all(abs(X[k]) < 1e-12 for k in (1, 3, 5)), "and the even ones vanish"


def sigma(n):
 return lambda t: sum(X[i] * phi(i + 1)(t) for i in range(n))


# ── beats 1 to 3: the identity, Bessel, Parseval ───────────────────────
ROWS = []
_run = 0.0
for _n in range(1, NCO + 1):
 _run += X[_n - 1] ** 2
 _d2 = nm(lambda t, _n=_n: XI(t) - sigma(_n)(t)) ** 2
 assert abs(_run + _d2 - NX2) < 1e-7, \
     "the whole section rests on this: the two pieces always add to the squared norm"
 ROWS.append((_n, _run, _d2))
assert all(r <= NX2 + 1e-9 for _n, r, _d2 in ROWS), "which is Bessel's inequality"
assert ROWS[-1][1] > 0.94 * NX2 and ROWS[-1][2] > 0.02, \
    "the series is on its way to Parseval but visibly has not arrived at n = 7"
SN = math.sqrt(ROWS[2][1])
RN = math.sqrt(ROWS[2][2])
assert abs(SN ** 2 + RN ** 2 - NX2) < 1e-7, "the right triangle beat 1 draws"

# ── beats 5 and 6: the best approximation, and a family that is no basis
D3 = nm(lambda t: XI(t) - sigma(3)(t))
WORSE = []
for _f in (0.8, 1.25):
 _q = lambda t, _f=_f: sum(_f * X[i] * phi(i + 1)(t) for i in range(3))
 WORSE.append((_f, nm(lambda t, _q=_q: XI(t) - _q(t))))
assert all(d > D3 for _f, d in WORSE), "any other combination is farther: E69's lemma 2.1"
EVEN = [(2 * k, sp(XI, phi(2 * k))) for k in (1, 2, 3, 4)]
EVEN_SUM = sum(v * v for _k, v in EVEN)
assert EVEN_SUM < 1e-20 < NX2, \
    "against the even sines alone the constant has no Fourier series at all"
EVEN_PERP = [sp(phi(1), phi(2 * k)) for k in (1, 2, 3)]
assert all(abs(v) < 1e-12 for v in EVEN_PERP), \
    "and the first sine is orthogonal to every one of them, so the complement is not zero"

# ── beat 7: with a skew basis the coefficient moves ────────────────────
# v = e1 + e2.  Against the orthogonal basis its first coefficient is 1; against
# {e1, e1 + e2} the same vector is 0*e1 + 1*(e1 + e2).
VCO = (1.0, 1.0)
ORTH_C = VCO[0]
SKEW_C = VCO[0] - VCO[1]
assert ORTH_C != SKEW_C, "the same vector, the same first basis vector, two coefficients"

# ── beat 8: Gram-Schmidt in the plane, and beat 9 in C([0, 1]) ─────────
A1, A2 = (1.0, 0.35), (0.55, 1.25)


def dot(a, b):
 return a[0] * b[0] + a[1] * b[1]


def n2(v):
 return math.sqrt(dot(v, v))


GS_X = dot(A2, A1) / dot(A1, A1)
GS_MU = (GS_X * A1[0], GS_X * A1[1])
GS_F2 = (A2[0] - GS_MU[0], A2[1] - GS_MU[1])
assert abs(dot(GS_F2, A1)) < 1e-12, "what is left is orthogonal to the first vector"


def poly(c):
 return lambda t: sum(ci * t ** i for i, ci in enumerate(c))


MONO = [[1.0], [0.0, 1.0], [0.0, 0.0, 1.0]]
GS = []
GS_C = []
for _n in range(3):
 _c = list(MONO[_n]) + [0.0] * (3 - len(MONO[_n]))
 for _p in GS:
  _f = sp(poly(MONO[_n]), poly(_p), 0.0, 1.0) / sp(poly(_p), poly(_p), 0.0, 1.0)
  GS_C.append((_n + 1, len(GS_C), _f))
  _c = [ci - _f * pi for ci, pi in zip(_c, _p)]
 GS.append(_c)
assert abs(GS[1][0] + 0.5) < 1e-9 and abs(GS[1][1] - 1.0) < 1e-9, "the book's x minus a half"
assert abs(GS[2][0] - 1.0 / 6) < 1e-9 and abs(GS[2][1] + 1.0) < 1e-9, \
    "and the book's x squared minus x plus a sixth"
GS_ORTH = [(i, j, sp(poly(GS[i]), poly(GS[j]), 0.0, 1.0))
           for i, j in ((0, 1), (0, 2), (1, 2))]
assert all(abs(v) < 1e-9 for _i, _j, v in GS_ORTH), "the three are mutually orthogonal"
GS_NM = [nm(poly(c), 0.0, 1.0) for c in GS]

# ── beat 10: the map into the dual is an isometry ──────────────────────
BETA = (1.2, 0.5)
NDIR = 1440
DIRS = [(math.cos(2 * PI * k / NDIR), math.sin(2 * PI * k / NDIR)) for k in range(NDIR)]
SUPV = max(abs(dot(u, BETA)) for u in DIRS)
assert abs(SUPV - n2(BETA)) < 1e-4, \
    "the norm of the functional is the norm of the vector, so the map is an isometry"
BHAT = (BETA[0] / n2(BETA), BETA[1] / n2(BETA))
assert abs(abs(dot(BHAT, BETA)) - n2(BETA)) < 1e-12, "and the supremum is attained, at the vector itself"


class AdvCalcE70Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 70

 MODE_LABEL = {
  0: {"zh": "正交規範", "en": "orthonormal"},
  1: {"zh": "定理 2.2 的那一行計算", "en": "the one line theorem 2.2 turns on"},
  2: {"zh": "Bessel 不等式", "en": "Bessel's inequality"},
  3: {"zh": "Parseval：級數什麼時候收斂到 ξ", "en": "Parseval: when the series gets there"},
  4: {"zh": "基底的定義", "en": "what a basis means here"},
  5: {"zh": "定理 2.3：線性包稠密就夠了", "en": "theorem 2.3: a dense span is enough"},
  6: {"zh": "推論：正交補只有零", "en": "the corollary: nothing but zero is orthogonal"},
  7: {"zh": "正交基為什麼被偏愛", "en": "why orthogonal bases are favoured"},
  8: {"zh": "引理 2.5：正交化", "en": "lemma 2.5: orthogonalising"},
  9: {"zh": "書上的例子：1、x、x ²", "en": "the book's example"},
  10: {"zh": "定理 2.4：同構 ⇔ 完備", "en": "theorem 2.4: an isomorphism exactly when complete"},
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

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.86, dy=0.34, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _frame(self, ox, oy, w, h, down=0.30, back=0.12):
  return VGroup(Line([ox - back, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=PI, sw=2.4, n=140):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _pt(self, cx, cy, s, v, col, r=0.065):
  return Dot([cx + s * v[0], cy + s * v[1], 0], radius=r, color=col)

 def _vec(self, cx, cy, s, v, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=sw, tl=tl)

 def _lab(self, cx, cy, s, v, txt, col, dx=0.24, dy=0.24, w=0.90):
  return self._sym(cy + s * v[1] + dy, txt, col, FS_TAG - 1, x=cx + s * v[0] + dx, w=w)

 # ── beats ─────────────────────────────────────────────────────────
 def _orthonormal(self):
  ox, oy, sx, sy = -5.70, -0.18, 0.95, 0.62
  g = VGroup(self._frame(ox, oy, 3.10, 0.72, down=0.66))
  for k, col in ((1, ACCENT_B), (2, ACCENT_C), (3, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy, phi(k), col, sw=2.2))
  g.add(self._sym(oy + sy * phi(1)(PI / 2) + 0.26, "φ ₁", ACCENT_B, FS_TAG - 1,
                  x=ox + sx * PI / 2, w=0.80))
  g.add(self._table(((f"     ‖ φ ₁ ‖   =   {nm(phi(1)):.6f}", ACCENT_B),
                     (f"     ‖ φ ₂ ‖   =   {nm(phi(2)):.6f}", ACCENT_C),
                     (f"     ( φ ₁ , φ ₂ )   =   {sp(phi(1), phi(2)):.0e}", DIM),
                     (f"     ( φ ₁ , φ ₃ )   =   {sp(phi(1), phi(3)):.0e}", DIM)),
                    y0=0.80, dy=0.36))
  g.add(self._mid(-0.86, "正交，而且每一個長度都是一",
                  "orthogonal, and each of length one", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這一集的計算大半在這組上做：[ 0 , π ] 上的 sin k t 各乘上 √ ( 2 / π )，長度就正好是一",
                          "most of this episode computes with these: the sines on the interval scaled by the square root of two over pi, which makes each of length one",
                          ACCENT_A,
                          "要展開的向量取常數函數 1，它的 Fourier 正弦級數收斂得夠慢，慢到畫得出來",
                          "the vector to be expanded is the constant function one, whose Fourier sine series converges slowly enough to be drawn"))

 def _identity(self):
  cx, cy, s = -4.55, -0.62, 1.05
  g = VGroup()
  o = [cx, cy, 0]
  a = [cx + s * SN, cy, 0]
  b = [cx + s * SN, cy + s * RN, 0]
  g.add(Line(o, a, color=ACCENT_B, stroke_width=2.8),
        Line(a, b, color=ACCENT_C, stroke_width=2.8),
        Line(o, b, color=ACCENT_A, stroke_width=2.8))
  g.add(self._curve([[a[0] - 0.16, a[1], 0], [a[0] - 0.16, a[1] + 0.16, 0],
                     [a[0], a[1] + 0.16, 0]], DIM, sw=1.6))
  g.add(self._sym(cy - 0.30, f"‖ σ ₃ ‖  =  {SN:.4f}", ACCENT_B, FS_TAG - 2,
                  x=cx + s * SN / 2, w=1.90),
        self._sym(cy + s * RN / 2, f"{RN:.4f}", ACCENT_C, FS_TAG - 2,
                  x=cx + s * SN + 0.60, w=1.20),
        self._sym(cy + s * RN / 2 + 0.30, f"‖ ξ ‖  =  {math.sqrt(NX2):.4f}", ACCENT_A,
                  FS_TAG - 2, x=cx + s * SN / 2 - 0.70, w=1.90))
  g.add(self._table((("       n      Σ ₁ ⁿ x ᵢ ²      ‖ ξ − σ ₙ ‖ ²        +", DIM),)
                    + tuple((f"     {n:3d}      {a_:.4f}        {b_:.4f}      {a_ + b_:.4f}",
                             ACCENT_C if n % 2 else DIM)
                            for n, a_, b_ in ROWS[:5]), y0=0.90, dy=0.28, size=FS_TAG - 3))
  g.add(self._mid(-0.86, "最後一欄永遠是 ‖ ξ ‖ ²",
                  "the last column is always the squared norm", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("部分和是 ξ 在前 n 個向量張成的空間上的投影，所以 ξ 減部分和垂直於它——畢氏定理直接給出那個等式",
                          "the partial sum is the projection on the span of the first n, so the difference is orthogonal to it and the Pythagorean theorem gives the identity at once",
                          ACCENT_A,
                          f"左邊那個直角三角形畫的就是 n = 3 的情形：兩股 {SN:.4f} 與 {RN:.4f}，斜邊 {math.sqrt(NX2):.4f}",
                          f"the right triangle on the left is the case n equals three: legs {SN:.4f} and {RN:.4f}, hypotenuse {math.sqrt(NX2):.4f}"))

 def _bessel(self):
  ox, oy, sx, sy = -5.40, -0.72, 0.42, 0.52
  g = VGroup(self._frame(ox, oy, 3.20, 1.55, down=0.12))
  g.add(self._dash([ox, oy + sy * NX2, 0], [ox + 3.10, oy + sy * NX2, 0], ACCENT_A,
                   n=18, sw=1.6))
  g.add(self._sym(oy + sy * NX2 + 0.24, f"‖ ξ ‖ ²  =  {NX2:.4f}", ACCENT_A, FS_TAG - 2,
                  x=ox + 1.30, w=2.20))
  for n, run, _d2 in ROWS:
   g.add(Line([ox + sx * n, oy, 0], [ox + sx * n, oy + sy * run, 0],
              color=ACCENT_B, stroke_width=5.0))
   g.add(Dot([ox + sx * n, oy + sy * run, 0], radius=0.05, color=ACCENT_C))
  g.add(self._sym(oy - 0.26, "n", DIM, FS_TAG - 2, x=ox + sx * 4, w=0.60))
  g.add(self._table((("       n         Σ ₁ ⁿ x ᵢ ²", DIM),)
                    + tuple((f"     {n:3d}          {run:.6f}", ACCENT_B)
                            for n, run, _d2 in ROWS[:5])
                    + ((f"     ‖ ξ ‖ ²      {NX2:.6f}", ACCENT_A),), y0=0.90, dy=0.26,
                    size=FS_TAG - 3))
  g.add(self._mid(-0.90, "每一根都停在那條虛線底下",
                  "every bar stops below the dashed line", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("Bessel 不等式就是上一拍那個等式的左邊非負：前 n 個係數的平方和，對每個 n 都不超過 ‖ ξ ‖ ²",
                          "Bessel's inequality is just the left side of that identity being non-negative: the sum of the first n squared coefficients never exceeds the squared norm",
                          ACCENT_A,
                          "偶數項的係數是零，所以柱子每隔一根才長高一次——級數因此收斂，而且和不超過 ‖ ξ ‖ ²",
                          "the even coefficients vanish, so the bars only rise every other step, and the series converges with sum at most the squared norm"))

 def _parseval(self):
  ox, oy, sx, sy = -5.40, -0.72, 0.42, 0.52
  g = VGroup(self._frame(ox, oy, 3.20, 1.55, down=0.12))
  g.add(self._dash([ox, oy + sy * NX2, 0], [ox + 3.10, oy + sy * NX2, 0], ACCENT_A,
                   n=18, sw=1.6))
  for n, run, d2 in ROWS:
   g.add(Dot([ox + sx * n, oy + sy * run, 0], radius=0.055, color=ACCENT_B))
   g.add(Dot([ox + sx * n, oy + sy * d2, 0], radius=0.055, color=WARN))
  g.add(self._sym(oy + sy * NX2 + 0.24, f"{NX2:.4f}", ACCENT_A, FS_TAG - 2,
                  x=ox + 1.10, w=1.30))
  g.add(self._sym(oy + sy * ROWS[-1][1] - 0.28, "Σ x ᵢ ²", ACCENT_B, FS_TAG - 2,
                  x=ox + sx * 7 + 0.44, w=1.20),
        self._sym(oy + sy * ROWS[-1][2] + 0.26, "‖ ξ − σ ₙ ‖ ²", WARN, FS_TAG - 2,
                  x=ox + sx * 7 + 0.64, w=1.60))
  g.add(self._table((("       n      Σ ₁ ⁿ x ᵢ ²      ‖ ξ − σ ₙ ‖ ²", DIM),)
                    + tuple((f"     {n:3d}      {run:.4f}        {d2:.4f}", ACCENT_C)
                            for n, run, d2 in (ROWS[0], ROWS[2], ROWS[4], ROWS[6]))
                    + ((f"     Σ ₁ ⁿ x ᵢ ²  +  ‖ ξ − σ ₙ ‖ ²   =   {NX2:.4f}",
                        ACCENT_A),), y0=0.90, dy=0.28,
                    size=FS_TAG - 3))
  g.add(self._mid(-0.90, "一個往上、一個往下，加起來不動",
                  "one rises, the other falls, and the sum never moves", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("Parseval 就是同一個等式反過來讀：部分和收斂到 ξ，等價於係數平方和收斂到 ‖ ξ ‖ ²",
                          "Parseval is the same identity read the other way: the partial sums converge to the vector exactly when the squared coefficients sum to the squared norm",
                          ACCENT_A,
                          f"這個例子還沒到——n = 7 時青綠色那些點才到 {ROWS[-1][1]:.4f}，紅色那些點還有 {ROWS[-1][2]:.4f}",
                          f"this example has not arrived: at n equals seven the rising points reach {ROWS[-1][1]:.4f} and the falling ones still stand at {ROWS[-1][2]:.4f}"))

 def _basis(self):
  ox, oy, sx, sy = -5.70, -0.42, 0.95, 0.62
  g = VGroup(self._frame(ox, oy, 3.10, 1.05, down=0.30))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * PI, oy + sy, 0], ACCENT_A, n=20, sw=1.6))
  for n, col, sw in ((1, DIM, 1.8), (3, ACCENT_C, 1.8), (7, WARN, 2.4)):
   g.add(self._fcurve(ox, oy, sx, sy, sigma(n), col, sw=sw))
  g.add(self._sym(oy + sy + 0.26, "ξ  =  1", ACCENT_A, FS_TAG - 2,
                  x=ox + sx * 0.55, w=1.40))
  g.add(self._table((("       n        ‖ ξ − σ ₙ ‖", DIM),)
                    + tuple((f"     {n:3d}          {math.sqrt(d2):.4f}",
                             (DIM, ACCENT_C, WARN)[i])
                            for i, (n, _r, d2) in enumerate((ROWS[0], ROWS[2], ROWS[6])))
                    + (("     ξ   =   Σ ᵢ x ᵢ φ ᵢ", ACCENT_A),), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "基底的意思是這個級數真的收斂到 ξ",
                  "a basis means that series really converges to the vector", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("黃色虛線是常數函數 ξ，三條曲線是 n = 1、3、7 的部分和——兩端翹起來的地方就是它們還沒追上的部分",
                          "the amber dashed line is the constant function and the three curves are the partial sums for one, three and seven terms, overshooting at both ends where they have not caught up",
                          ACCENT_A,
                          "「基底」在這裡不是有限展開的意思，而是「每個元素都是自己 Fourier 級數的和」",
                          "a basis here does not mean a finite expansion: it means every element is the sum of its own Fourier series"))

 def _dense(self):
  ox, oy, sx, sy = -5.70, -0.42, 0.95, 0.62
  g = VGroup(self._frame(ox, oy, 3.10, 1.05, down=0.30))
  g.add(self._dash([ox, oy + sy, 0], [ox + sx * PI, oy + sy, 0], ACCENT_A, n=20, sw=1.6))
  g.add(self._fcurve(ox, oy, sx, sy, sigma(3), ACCENT_B, sw=2.6))
  for (f, _d), col in zip(WORSE, (ACCENT_C, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy,
                      lambda t, f=f: sum(f * X[i] * phi(i + 1)(t) for i in range(3)),
                      col, sw=1.8))
  g.add(self._table((("       M  =  L ( φ ₁ , φ ₂ , φ ₃ )", DIM),
                     (f"     σ ₃              {D3:.4f}", ACCENT_B),)
                    + tuple((f"     {f:.2f}  ·  σ ₃        {d:.4f}",
                             (ACCENT_C, WARN)[i]) for i, (f, d) in enumerate(WORSE))
                    + ((f"     min   =   {D3:.4f}", ACCENT_A),), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "同一個空間裡，Fourier 那一組最近",
                  "inside that span the Fourier combination is the closest", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 2.3 的證明就靠這件事：稠密給出一個 ε 以內的有限組合，而同樣長度的 Fourier 部分和只會更近",
                          "that is what the proof of theorem 2.3 uses: density supplies a finite combination within epsilon, and the Fourier partial sum of the same length can only be closer",
                          ACCENT_A,
                          f"青綠色那條是 Fourier 的，兩條細的是把係數乘上 {WORSE[0][0]:.2f} 與 {WORSE[1][0]:.2f} 之後的樣子，距離都變大",
                          f"the teal curve is the Fourier one and the two thin curves scale its coefficients, both ending up farther away"))

 def _corollary(self):
  ox, oy, sx, sy = -5.70, -0.18, 0.95, 0.62
  g = VGroup(self._frame(ox, oy, 3.10, 0.72, down=0.66))
  for k, col, sw in ((2, ACCENT_C, 1.8), (4, DIM, 1.8), (1, WARN, 2.6)):
   g.add(self._fcurve(ox, oy, sx, sy, phi(k), col, sw=sw))
  g.add(self._sym(oy + sy * phi(1)(PI / 2) + 0.26, "φ ₁", WARN, FS_TAG - 1,
                  x=ox + sx * PI / 2, w=0.80))
  g.add(self._table((("     { φ ₂ , φ ₄ , φ ₆ , … }", DIM),)
                    + tuple((f"     ( ξ , φ {k} )   =   {v:.0e}", ACCENT_C)
                            for k, v in EVEN[:3])
                    + ((f"     Σ x ᵢ ²  =  {EVEN_SUM:.0e}    <    {NX2:.4f}", ACCENT_A),
                       (f"     ( φ ₁ , φ ₂ ᵏ )   =   {max(abs(v) for v in EVEN_PERP):.0e}",
                        WARN)), y0=0.88, dy=0.30))
  g.add(self._mid(-0.90, "紅色那條垂直於整組偶數正弦",
                  "the red curve is orthogonal to every even sine", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("只取偶數的那一組是正交規範的，Bessel 也成立——可是常數函數在它上面的係數全是零，Parseval 差了整個 ‖ ξ ‖ ²",
                          "the even sines alone are orthonormal and Bessel holds, but the constant function has every coefficient zero against them, so Parseval fails by the whole squared norm",
                          ACCENT_A,
                          "推論說的就是這個：Hilbert 空間裡，基底的充要條件是正交補只有零——這裡 φ ₁ 就不是零",
                          "that is what the corollary says: in a Hilbert space a sequence is a basis exactly when nothing but zero is orthogonal to all of it, and here the first sine is not zero"))

 def _favoured(self):
  cx, cy, s = -4.30, -0.55, 0.95
  g = VGroup(Line([cx - s * 0.30, cy, 0], [cx + s * 1.70, cy, 0], color=DIM, stroke_width=1.1),
             Line([cx, cy - s * 0.30, 0], [cx, cy + s * 1.55, 0], color=DIM, stroke_width=1.1))
  g.add(self._vec(cx, cy, s, (1.0, 0.0), ACCENT_B, sw=2.4),
        self._vec(cx, cy, s, (0.0, 1.0), ACCENT_B, sw=2.4),
        self._vec(cx, cy, s, (1.0, 1.0), ACCENT_C, sw=2.4))
  g.add(self._vec(cx, cy, s, VCO, ACCENT_A, sw=3.0))
  g.add(self._lab(cx, cy, s, (1.0, 0.0), "e ₁", ACCENT_B, dx=0.10, dy=-0.28),
        self._lab(cx, cy, s, (0.0, 1.0), "e ₂", ACCENT_B, dx=-0.32, dy=0.26),
        self._lab(cx, cy, s, (1.0, 1.0), "e ₁ + e ₂", ACCENT_C, dx=0.70, dy=-0.02, w=1.60),
        self._lab(cx, cy, s, VCO, "ξ", ACCENT_A, dx=0.04, dy=0.30))
  g.add(self._table((("     ξ   =   x ₁ e ₁  +  x ₂ e ₂", DIM),
                     (f"     x ₁   =   {ORTH_C:.1f}", ACCENT_B),
                     ("     ξ   =   y ₁ e ₁  +  y ₂ ( e ₁ + e ₂ )", DIM),
                     (f"     y ₁   =   {SKEW_C:.1f}", ACCENT_C),
                     ("     x ᵦ   =   ( ξ , β ) / ‖ β ‖ ²", ACCENT_A)), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "同一個 ξ、同一個 e ₁，係數卻不一樣",
                  "the same vector and the same first basis vector, two different coefficients",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("換掉第二個基向量，ξ 在 e ₁ 上的係數就從 1 變成 0——一般的基底，係數跟其餘基向量有關",
                          "replacing the second basis vector changes the coefficient at the first from one to zero: for an arbitrary basis the coefficient depends on the rest",
                          ACCENT_A,
                          "用正交基就不會：係數永遠是 Fourier 係數 ( ξ , β ) / ‖ β ‖ ²，只由 β 決定。這就是正交基被偏愛的理由",
                          "with an orthogonal basis it cannot: the coefficient is always the Fourier coefficient and depends on that basis vector alone, which is why such bases are favoured"))

 def _gramschmidt(self):
  cx, cy, s = -4.30, -0.62, 1.05
  g = VGroup(Line([cx - s * 0.30, cy, 0], [cx + s * 1.60, cy, 0], color=DIM, stroke_width=1.1),
             Line([cx, cy - s * 0.30, 0], [cx, cy + s * 1.45, 0], color=DIM, stroke_width=1.1))
  g.add(Line([cx - s * 0.30 * A1[0], cy - s * 0.30 * A1[1], 0],
             [cx + s * 1.55 * A1[0], cy + s * 1.55 * A1[1], 0],
             color=ACCENT_B, stroke_width=2.0))
  g.add(self._vec(cx, cy, s, A1, ACCENT_B), self._vec(cx, cy, s, A2, ACCENT_C))
  g.add(self._vec(cx, cy, s, GS_MU, WARN, sw=2.2))
  g.add(self._arr([cx + s * GS_MU[0], cy + s * GS_MU[1], 0],
                  [cx + s * A2[0], cy + s * A2[1], 0], ACCENT_A, sw=2.6, tl=0.12))
  g.add(self._lab(cx, cy, s, A1, "α ₁", ACCENT_B, dx=0.24, dy=-0.26),
        self._lab(cx, cy, s, A2, "α ₂", ACCENT_C, dx=0.04, dy=0.30),
        self._lab(cx, cy, s, GS_MU, "μ", WARN, dx=0.16, dy=-0.46),
        self._sym(cy + s * (GS_MU[1] + A2[1]) / 2, "φ ₂", ACCENT_A, FS_TAG - 1,
                  x=cx + s * (GS_MU[0] + A2[0]) / 2 + 0.42, w=0.90))
  g.add(self._table((("     φ ₙ   =   α ₙ  −  P ( α ₙ )", DIM),
                     (f"     μ   =   ⟨ {GS_MU[0]:.4f} , {GS_MU[1]:.4f} ⟩", WARN),
                     (f"     φ ₂   =   ⟨ {GS_F2[0]:.4f} , {GS_F2[1]:.4f} ⟩", ACCENT_A),
                     (f"     ( φ ₂ , α ₁ )   =   {dot(GS_F2, A1):.0e}", ACCENT_B)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "減掉投影，剩下的就垂直",
                  "subtract the projection and what is left is orthogonal", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理 2.5 的作法就是上一集那個投影：φ ₂ 是 α ₂ 減掉它在 α ₁ 上的投影，而兩者張成的子空間完全一樣",
                          "lemma 2.5 uses last episode's projection: the second vector minus its projection on the first, and the two pairs span the same subspace",
                          ACCENT_A,
                          "遞迴算下去的時候，投影的係數就是前面那些已經正交化的向量的 Fourier 係數",
                          "carried on recursively, the multipliers in the projection are the Fourier coefficients with respect to the vectors already orthogonalised"))

 def _example(self):
  ox, oy, sx, sy = -5.20, -0.30, 2.60, 0.95
  g = VGroup(self._frame(ox, oy, 2.95, 1.05, down=0.42))
  for c, col, sw in ((GS[0], ACCENT_B, 2.2), (GS[1], ACCENT_C, 2.2), (GS[2], WARN, 2.6)):
   g.add(self._fcurve(ox, oy, sx, sy, poly(c), col, t0=0.0, t1=1.0, sw=sw))
  g.add(self._sym(oy + sy * 1.0 + 0.24, "1", ACCENT_B, FS_TAG - 1,
                  x=ox + sx * 0.5, w=0.60))
  g.add(self._table((("     φ ₁  =  1", ACCENT_B),
                     (f"     φ ₂  =  x  −  {abs(GS[1][0]):.4f}", ACCENT_C),
                     (f"     φ ₃  =  x ²  −  x  +  {GS[2][0]:.4f}", WARN),
                     (f"     ( φ ₁ , φ ₂ )  =  {GS_ORTH[0][2]:.0e}    ( φ ₂ , φ ₃ )  =  {GS_ORTH[2][2]:.0e}",
                      DIM),
                     (f"     ‖ φ ₂ ‖  =  {GS_NM[1]:.4f}      ‖ φ ₃ ‖  =  {GS_NM[2]:.4f}", ACCENT_A)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, f"六分之一 = {GS[2][0]:.4f}，跟書上一樣",
                  f"a sixth is {GS[2][0]:.4f}, exactly the book's answer", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("書上的例子：C ( [ 0 , 1 ] ) 上的 1、x、x ²，正交化之後是 1、x − 1 / 2、x ² − x + 1 / 6",
                          "the book's example: one, x and x squared on the unit interval, orthogonalised into one, x minus a half, and x squared minus x plus a sixth",
                          ACCENT_A,
                          "這裡的三條都是程式照遞迴算出來的，係數 1 / 2、1 / 3、1 三個也都對得上；書上說這個過程完全初等，可是再算幾項就很煩",
                          "all three are produced by the recursion in code, and the three multipliers match as well; the book calls the process elementary but burdensome after a few terms"))

 def _riesz(self):
  cx, cy, s = -4.30, -0.12, 0.85
  g = VGroup(Line([cx - s * 1.45, cy, 0], [cx + s * 1.45, cy, 0], color=DIM, stroke_width=1.1),
             Line([cx, cy - s * 1.05, 0], [cx, cy + s * 1.25, 0], color=DIM, stroke_width=1.1))
  g.add(self._curve([[cx + s * u[0], cy + s * u[1], 0] for u in DIRS[::20]]
                    + [[cx + s * DIRS[0][0], cy + s * DIRS[0][1], 0]], ACCENT_B, sw=2.0))
  g.add(self._vec(cx, cy, s, BETA, ACCENT_A, sw=2.8))
  g.add(self._pt(cx, cy, s, BHAT, WARN, r=0.07),
        self._pt(cx, cy, s, (-BHAT[0], -BHAT[1]), WARN, r=0.07))
  g.add(self._lab(cx, cy, s, BETA, "β", ACCENT_A, dx=0.20, dy=0.24),
        self._lab(cx, cy, s, BHAT, "ξ", WARN, dx=0.38, dy=-0.54))
  g.add(self._table((("     θ ᵦ ( ξ )   =   ( ξ , β )", DIM),
                     (f"     sup | ( ξ , β ) |   =   {SUPV:.4f}", ACCENT_B),
                     (f"     ‖ β ‖   =   {n2(BETA):.4f}", ACCENT_A),
                     ("     ‖ θ ᵦ ‖   =   ‖ β ‖", WARN),
                     ("     θ  ≅       ⇔       V  = Hilbert", ACCENT_C)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "上界在 β 自己的方向上取到",
                  "the supremum is attained in the direction of that very vector",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"θ 把 β 送成「跟 β 取內積」這個泛函。它是線性、單射，而且等距：在單位圓上取樣 {NDIR} 個方向，上界 {SUPV:.4f} 就是 ‖ β ‖ = {n2(BETA):.4f}",
                          f"the map sends a vector to the functional that takes the product with it; it is linear, injective and an isometry, and sampling {NDIR} directions on the unit circle gives the supremum as the norm itself",
                          ACCENT_A,
                          "定理 2.4：它是同構的充要條件就是 V 為 Hilbert 空間。第 4 章的定理 12.2 要靠切超平面才有的東西，純量積這裡直接就有了",
                          "theorem 2.4: it is an isomorphism exactly when the space is a Hilbert space, and what chapter 4 needed a tangent hyperplane for comes free here"))

 def stage(self):
  a, b, c = self._orthonormal(), self._identity(), self._bessel()
  d, e, f_ = self._parseval(), self._basis(), self._dense()
  h, i, j = self._corollary(), self._favoured(), self._gramschmidt()
  k, l = self._example(), self._riesz()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE70ZH, AdvCalcE70EN = make(AdvCalcE70Base, "70", prefix="AdvCalcE")
