"""advcalc E73 -- chapter 5, section 5 (book pp. 264-265): compact transformations
and the one infinite-dimensional case where the eigenbasis theorem survives.

Theorem 3.1 breaks down in infinite dimensions: a bounded self-adjoint operator
need not have a single eigenvector, and a continuous spectrum has to be handled
alongside the discrete one.  Multiplication by x on the unit interval is the
standard witness -- every point of [0, 1] is in its spectrum and none of them is
an eigenvalue.  But one class survives: T is compact when the closure of the
image of the unit ball is sequentially compact, and Theorem 5.1 says a compact
self-adjoint T has an orthonormal basis of eigenvectors for its range, with
eigenvalues tending to zero.

The proof is Theorem 3.1's with a different opening.  Take m = ||T|| and a
sequence of unit vectors whose images approach that norm; then
((m^2 - T^2) xi_n, xi_n) = m^2 - ||T xi_n||^2 tends to zero, and E71's Lemma 3.2
-- nonnegative self-adjoint, so the number controls the vector -- turns that
into (m^2 - T^2)(xi_n) -> 0.  Compactness then makes T xi_n converge, which
drags xi_n along with it and produces a nonzero beta with T^2 beta = m^2 beta.
Factoring m^2 - T^2 as (m - T)(m + T) hands over an eigenvector with |r| = m,
and the induction of Theorem 3.1 runs from there.  Compactness bites a second
time in showing |r_n| goes to zero: if the eigenvalues stayed above b, the
images of the orthonormal eigenvectors would remain 2b^2 apart in square norm
and no subsequence could converge.

This section has no exercises at all -- page 265 finishes and chapter 6 begins
on 266.  It is the third time in the book (after chapter 2's *7 and chapter 4's
*12), and it closes chapter 5.

Everything is computed with the Green's operator of the Dirichlet problem on the
unit interval, K(x, y) = min(x, y)(1 - max(x, y)), which is exactly the
"startling application in the next chapter" the book is pointing at: it is
symmetric, hence self-adjoint, compact, and its eigenvectors are the normalised
sines with eigenvalues 1/(n pi)^2 falling to zero.
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


def simpson(g, a, b, n=800):
 h = (b - a) / n
 s = g(a) + g(b)
 for k in range(1, n):
  s += (4 if k % 2 else 2) * g(a + k * h)
 return s * h / 3


def sp(f, g, a=0.0, b=1.0):
 return simpson(lambda t: f(t) * g(t), a, b)


def nm(f, a=0.0, b=1.0):
 return math.sqrt(sp(f, f, a, b))


# ── the operator: the Green's function of -u'' with Dirichlet ends ────
def K(x, y):
 return x * (1.0 - y) if x <= y else y * (1.0 - x)


def T(f):
 return lambda x: simpson(lambda y: K(x, y) * f(y), 0.0, 1.0, 200)


def phi(n):
 return lambda x: math.sqrt(2.0) * math.sin(n * PI * x)


def r(n):
 return 1.0 / (n * PI) ** 2


assert max(abs(K(0.05 * i, 0.05 * j) - K(0.05 * j, 0.05 * i))
           for i in range(21) for j in range(21)) == 0.0, \
    "the kernel is symmetric, which is what makes the operator self-adjoint"
_f = lambda x: x * (1.0 - x) + 0.3
_g = lambda x: math.sin(3.0 * x) + 0.2
assert abs(sp(T(_f), _g) - sp(_f, T(_g))) < 1e-8, "and here it is, checked on a pair"
for _k in (1, 2, 3):
 assert abs(nm(phi(_k)) - 1.0) < 1e-9
assert abs(sp(phi(1), phi(2))) < 1e-12, "the sines are orthonormal"
EIG = []
for _n in (1, 2, 3, 4):
 _e = max(abs(T(phi(_n))(0.1 * _k) - r(_n) * phi(_n)(0.1 * _k)) for _k in range(11))
 assert _e < 1e-8, "each normalised sine is an eigenvector, with eigenvalue one over n pi squared"
 EIG.append((_n, r(_n), _e))
M = r(1)
assert all(EIG[i][1] > EIG[i + 1][1] for i in range(3)) and EIG[-1][1] < 0.01 * 1.0, \
    "the eigenvalues fall away, which is the whole point of the theorem"

# ── beat 1: a self-adjoint operator with no eigenvector at all ────────
LAM = 0.5


def bump(c0, h):
 return lambda x: math.cos(PI * (x - c0) / (2 * h)) ** 2 if abs(x - c0) < h else 0.0


MUL = []
for _h in (0.25, 0.125, 0.0625, 0.03125):
 _w = bump(LAM, _h)
 _c = 1.0 / math.sqrt(simpson(lambda t: _w(t) ** 2, LAM - _h, LAM + _h, 600))
 _d = math.sqrt(simpson(lambda t: ((t - LAM) * _c * _w(t)) ** 2, LAM - _h, LAM + _h, 600))
 MUL.append((_h, _c * math.sqrt(simpson(lambda t: _w(t) ** 2, LAM - _h, LAM + _h, 600)), _d))
assert all(abs(u - 1.0) < 1e-9 for _h, u, _d in MUL), "every one of them is a unit vector"
assert MUL[0][2] > 4 * MUL[-1][2] and MUL[-1][2] < 0.01, \
    "yet the image can be made as small as we like: 0.5 is in the spectrum"
assert all(d > 0 for _h, _u, d in MUL), \
    "and never zero, because (x - lambda) f = 0 forces f = 0: it is not an eigenvalue"
MUL_RATIO = MUL[0][2] / MUL[1][2]
assert 1.9 < MUL_RATIO < 2.1, "halving the width halves it, so the infimum is zero"

# ── beat 2: what compactness rules out ────────────────────────────────
SEP = nm(lambda x: phi(1)(x) - phi(2)(x)) ** 2
assert abs(SEP - 2.0) < 1e-9, \
    "an orthonormal sequence is always this far apart, so the identity is not compact"
PAIRS = []
for _i, _j in ((1, 2), (2, 3), (3, 4), (5, 6)):
 _d2 = nm(lambda x, _i=_i, _j=_j: T(phi(_i))(x) - T(phi(_j))(x)) ** 2
 PAIRS.append((_i, _j, _d2, r(_i) ** 2 + r(_j) ** 2))
assert all(abs(a - b) < 1e-8 for _i, _j, a, b in PAIRS), \
    "beat 9's identity, checked: the squared distance is the sum of the squared eigenvalues"
assert PAIRS[0][2] > 400 * PAIRS[-1][2], "and under T the images do crowd together"

# ── beats 4 to 6: the maximising sequence ─────────────────────────────
SEQ = []
for _n in (1, 2, 4, 8):
 _c = 1.0 / _n
 _t2 = (r(1) ** 2 + _c * _c * r(2) ** 2) / (1 + _c * _c)
 SEQ.append((_n, math.sqrt(_t2), M * M - _t2,
             _c * (M * M - r(2) ** 2) / math.sqrt(1 + _c * _c)))
assert all(SEQ[i][1] < SEQ[i + 1][1] < M for i in range(3)), "the norms climb towards ||T||"
assert SEQ[0][2] > 30 * SEQ[-1][2] and SEQ[0][3] > 5 * SEQ[-1][3], \
    "and both the number and the vector of lemma 3.2 fall away together"
for _n, _tn, _q, _v in SEQ:
 assert abs(_q - (M * M - _tn ** 2)) < 1e-12, "the identity the proof opens with"

# the two branches of the factoring, on T and on its negative
BR_PLUS = (M, "gamma")
BR_MINUS = (-M, "alpha")
assert abs(r(1) - M) < 1e-12, \
    "for this operator every eigenvalue is positive, so it is always the second branch"
assert abs((-T(phi(1))(0.3)) + M * phi(1)(0.3)) < 1e-8, \
    "flip the sign of T and the first branch is the one that fires"

# ── beats 9 and 10: the range has the eigenvectors as a basis ─────────
ONE = lambda x: 1.0
NCO = 8
A_CO = [sp(ONE, phi(n)) for n in range(1, NCO + 1)]
B_CO = [sp(T(ONE), phi(n)) for n in range(1, NCO + 1)]
for _n in range(1, NCO + 1):
 assert abs(B_CO[_n - 1] - r(_n) * A_CO[_n - 1]) < 1e-8, \
     "the coefficients of the image are the coefficients of the source, scaled"
NA = nm(ONE)
NB = nm(T(ONE))
TAIL = []
for _n in range(1, 6):
 _res = math.sqrt(max(0.0, NB ** 2 - sum(B_CO[k] ** 2 for k in range(_n))))
 TAIL.append((_n, _res, r(_n + 1) * NA))
assert all(res <= bnd + 1e-9 for _n, res, bnd in TAIL), \
    "the estimate of the last beat, never violated"
assert TAIL[0][1] > 10 * TAIL[-1][1], "and the tail really does fall away"
assert abs(NA - 1.0) < 1e-9


class AdvCalcE73Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 73

 MODE_LABEL = {
  0: {"zh": "無窮維時定理 3.1 失效", "en": "in infinite dimensions theorem 3.1 fails"},
  1: {"zh": "緊的定義", "en": "what compact means"},
  2: {"zh": "定理 5.1", "en": "theorem 5.1"},
  3: {"zh": "證明的起手", "en": "how the proof opens"},
  4: {"zh": "引理 3.2 第二次付現", "en": "lemma 3.2 pays off again"},
  5: {"zh": "緊性第一次用上", "en": "compactness, first use"},
  6: {"zh": "把 m ² − T ² 分解掉", "en": "factoring the difference"},
  7: {"zh": "歸納", "en": "the induction"},
  8: {"zh": "為什麼 | r ₙ | 必須趨近零", "en": "why the eigenvalues must die away"},
  9: {"zh": "係數的關係", "en": "how the coefficients relate"},
  10: {"zh": "尾巴的估計，與第 5 章的結束", "en": "the tail estimate, and the end of chapter 5"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.86, dy=0.34, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _cap(self, zh, en):
  return self._mid(-0.90, zh, en, ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W)

 def _frame(self, ox, oy, w, h, down=0.30, back=0.12):
  return VGroup(Line([ox - back, oy, 0], [ox + w, oy, 0], color=DIM, stroke_width=1.3),
                Line([ox, oy - down, 0], [ox, oy + h, 0], color=DIM, stroke_width=1.3))

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=1.0, sw=2.4, n=140):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _bars(self, ox, oy, vals, sy, dx=0.40, sw=7.0, cols=None):
  g = VGroup()
  for k, v in enumerate(vals):
   c = (cols[k] if cols else ACCENT_B)
   g.add(Line([ox + dx * (k + 1), oy, 0], [ox + dx * (k + 1), oy + sy * v, 0],
              color=c, stroke_width=sw))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _nospectrum(self):
  ox, oy, sx, sy = -6.00, -0.62, 3.40, 0.62
  g = VGroup(self._frame(ox, oy, 3.52, 1.42, down=0.10))
  for (h, _u, _d), col in zip(MUL, (DIM, ACCENT_C, ACCENT_B, WARN)):
   w = bump(LAM, h)
   c = 1.0 / math.sqrt(simpson(lambda t: w(t) ** 2, LAM - h, LAM + h, 400))
   g.add(self._fcurve(ox, oy, sx, sy, lambda t, w=w, c=c: 0.42 * c * w(t), col,
                      t0=0.0, t1=1.0, n=200, sw=2.0))
  g.add(self._dash([ox + sx * LAM, oy, 0], [ox + sx * LAM, oy + 1.32, 0], ACCENT_A,
                   n=14, sw=1.4))
  g.add(self._sym(oy + 1.42, "λ  =  0.5", ACCENT_A, FS_TAG - 2, x=ox + sx * LAM, w=1.30))
  g.add(self._table((("       h          ‖ f ‖        ‖ ( M − λ ) f ‖", DIM),)
                    + tuple((f"     {h:.5f}     {u:.4f}        {d:.6f}", ACCENT_B)
                            for h, u, d in MUL)
                    + ((f"     ( x − λ ) f ( x )  ≡  0     ⇒     f  =  0", ACCENT_A),),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("中間那一欄永遠是一，右邊那一欄卻要多小有多小",
                  "every one of them is a unit vector, yet the image shrinks without limit"))
  return g.add(self._foot("無窮維時定理 3.1 失效：這個 M 把 f ( x ) 送成 x f ( x )，有界、自伴，可是連一個特徵向量都沒有",
                          "in infinite dimensions theorem 3.1 fails; multiplication by x is bounded and self-adjoint yet has no eigenvector at all",
                          ACCENT_A,
                          "把 f 擠在 λ 附近，‖ ( M − λ ) f ‖ 就要多小有多小——λ 在譜裡；可是它永遠不是零，所以不是特徵值。這就是「連續譜」",
                          "squeezing the bump towards that point makes the image as small as we like, so the point is in the spectrum, but it is never zero, so it is not an eigenvalue"))

 def _compact(self):
  ox, oy = -5.90, -0.74
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.56, 0], color=DIM, stroke_width=1.3))
  g.add(self._dash([ox, oy + 1.30, 0], [ox + 3.30, oy + 1.30, 0], WARN, n=22, sw=1.3))
  g.add(self._sym(oy + 1.50, "‖ φ ₙ ‖  =  1", WARN, FS_TAG - 3, x=ox + 2.70, w=1.60))
  g.add(self._bars(ox, oy, [1.0] * 6, 1.30, dx=0.24, sw=5.0, cols=[WARN] * 6))
  g.add(self._bars(ox + 1.80, oy, [r(n) / M for n in range(1, 7)], 1.30, dx=0.24, sw=5.0,
                   cols=[ACCENT_B] * 6))
  g.add(self._sym(oy - 0.28, "φ ₙ", WARN, FS_TAG - 2, x=ox + 0.84, w=0.70),
        self._sym(oy - 0.28, "T φ ₙ", ACCENT_B, FS_TAG - 2, x=ox + 2.64, w=1.00))
  g.add(self._table((("     S   =   { ξ  :  ‖ ξ ‖  ≤  1 }", DIM),
                     (f"     ‖ φ ᵢ − φ ⱼ ‖ ²   =   {SEP:.4f}", WARN),
                     (f"     ‖ T φ ₁ − T φ ₂ ‖ ²   =   {PAIRS[0][2]:.6f}", ACCENT_B),
                     (f"     ‖ T φ ₅ − T φ ₆ ‖ ²   =   {PAIRS[-1][2]:.6f}", ACCENT_B),
                     (f"     r ₁  =  {r(1):.6f}        r ₆  =  {r(6):.6f}", ACCENT_A)),
                    y0=0.84, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("左邊那排永遠一樣高，右邊那排掉下去",
                  "the bars on the left never move; the ones on the right fall away"))
  return g.add(self._foot("定義：S 是單位球，T 緊的意思是 T [ S ] 的閉包序列緊緻。恆等映射在無窮維不緊——正交規範序列兩兩距離都是 √ 2，抽不出收斂子列",
                          "definition: T is compact when the closure of the image of the unit ball is sequentially compact; the identity is not, since an orthonormal sequence keeps a fixed distance apart",
                          ACCENT_A,
                          "這一集的 T 是 Dirichlet 問題的 Green 算子，K ( x , y ) = min ( x , y ) ( 1 − max ( x , y ) )。它的像擠成一團，所以緊",
                          "the operator throughout is the Green's function of the Dirichlet problem, whose images crowd together, which is what compactness asks for"))

 def _theorem(self):
  ox, oy, sx, sy = -5.90, -0.30, 3.30, 0.52
  g = VGroup(self._frame(ox, oy, 3.42, 0.78, down=0.72))
  for n, col in ((1, ACCENT_B), (2, ACCENT_C), (3, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy, phi(n), col, sw=2.0, n=160))
  g.add(self._sym(oy + sy * math.sqrt(2.0) + 0.24, "φ ₁", ACCENT_B, FS_TAG - 2,
                  x=ox + sx * 0.5, w=0.70))
  g.add(self._table((("       n          r ₙ           ‖ T φ ₙ − r ₙ φ ₙ ‖", DIM),)
                    + tuple((f"     {n:3d}       {rv:.8f}         {e:.1e}", ACCENT_B)
                            for n, rv, e in EIG)
                    + ((f"     m  =  ‖ T ‖  =  r ₁  =  {M:.8f}", ACCENT_A),),
                    y0=0.86, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("特徵值一路掉向零，這正是定理保證的",
                  "the eigenvalues fall towards zero, which is what the theorem promises"))
  return g.add(self._foot("定理 5.1：T 自伴而且緊時，T 的像有一組完全由特徵向量構成的正交規範基，而特徵值序列收斂到零（或只有有限個）",
                          "theorem 5.1: for a compact self-adjoint T the range has an orthonormal basis of eigenvectors, and the eigenvalues converge to zero or are finite in number",
                          ACCENT_A,
                          "這個 Green 算子的特徵向量正是正規化的正弦，特徵值是 1 / ( n π ) ²——下一章要用的 Fourier 級數就是從這裡出來的",
                          "for this operator the eigenvectors are the normalised sines and the eigenvalues are one over n pi squared, which is where the next chapter's Fourier series comes from"))

 def _opening(self):
  ox, oy = -5.85, -0.66
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.52, 0], color=DIM, stroke_width=1.3))
  sy = 1.24 / M
  g.add(self._dash([ox, oy + sy * M, 0], [ox + 3.30, oy + sy * M, 0], ACCENT_A, n=22, sw=1.3))
  g.add(self._sym(oy + sy * M + 0.24, f"m  =  ‖ T ‖  =  {M:.6f}", ACCENT_A, FS_TAG - 3,
                  x=ox + 1.70, w=2.60))
  for k, (n, tn, _q, _v) in enumerate(SEQ):
   x = ox + 0.62 + k * 0.72
   g.add(Line([x, oy, 0], [x, oy + sy * tn, 0], color=ACCENT_B, stroke_width=7.0),
         Dot([x, oy + sy * tn, 0], radius=0.05, color=ACCENT_C))
   g.add(self._sym(oy - 0.26, f"{n}", DIM, FS_TAG - 3, x=x, w=0.40))
  g.add(self._table((("       n        ‖ T ξ ₙ ‖         m ² − ‖ T ξ ₙ ‖ ²", DIM),)
                    + tuple((f"     {n:3d}      {tn:.8f}        {q:.3e}", ACCENT_B)
                            for n, tn, q, _v in SEQ),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("長條爬向虛線，右邊那一欄就掉向零",
                  "the bars climb to the dashed line and the last column falls to zero"))
  return g.add(self._foot("證明的起手：m 取 ‖ T ‖，挑一列長度都是一的 ξ ₙ 使 ‖ T ξ ₙ ‖ 趨近 m。那個內積展開就是 m ² 減 ‖ T ξ ₙ ‖ ²",
                          "the proof opens by taking m to be the norm of T and a sequence of unit vectors whose images approach it; expanding the product gives m squared minus those squared norms",
                          ACCENT_A,
                          "這裡取 ξ ₙ = ( φ ₁ + φ ₂ / n ) 正規化之後的樣子，是最容易寫下來的一列；定理 3.1 那時候是在球面上取最大值，這裡改成取上確界的序列",
                          "the sequence drawn is the first eigenvector perturbed by the second over n, the easiest one to write down; theorem 3.1 took a maximum, this takes a maximising sequence"))

 def _lemma(self):
  ox, oy = -5.85, -0.70
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.50, 0], color=DIM, stroke_width=1.3))
  qs = max(q for _n, _t, q, _v in SEQ)
  vs = max(v for _n, _t, _q, v in SEQ)
  for k, (n, _t, q, v) in enumerate(SEQ):
   x = ox + 0.52 + k * 0.72
   g.add(Line([x - 0.13, oy, 0], [x - 0.13, oy + 1.24 * q / qs, 0],
              color=ACCENT_B, stroke_width=7.0),
         Line([x + 0.13, oy, 0], [x + 0.13, oy + 1.24 * v / vs, 0],
              color=ACCENT_C, stroke_width=7.0))
   g.add(self._sym(oy - 0.26, f"{n}", DIM, FS_TAG - 3, x=x, w=0.40))
  g.add(Line([ox + 0.10, 1.20, 0], [ox + 0.32, 1.20, 0], color=ACCENT_B, stroke_width=6.0),
        self._sym(1.20, "( ( m ² − T ² ) ξ ₙ , ξ ₙ )", ACCENT_B, FS_TAG - 3,
                  x=ox + 1.50, w=2.20))
  g.add(Line([ox + 0.10, 0.92, 0], [ox + 0.32, 0.92, 0], color=ACCENT_C, stroke_width=6.0),
        self._sym(0.92, "‖ ( m ² − T ² ) ξ ₙ ‖", ACCENT_C, FS_TAG - 3,
                  x=ox + 1.36, w=1.90))
  g.add(self._table((("       n        ( ( m ² − T ² ) ξ ₙ , ξ ₙ )      ‖ ( m ² − T ² ) ξ ₙ ‖",
                      DIM),)
                    + tuple((f"     {n:3d}          {q:.3e}              {v:.3e}", ACCENT_B)
                            for n, _t, q, v in SEQ)
                    + (("     m ²  −  T ²   ≥   0", ACCENT_A),),
                    y0=0.80, dy=0.28, size=FS_TAG - 3))
  g.add(self._cap("兩排一起掉下去，這就是引理 3.2 說的",
                  "both columns fall together, which is exactly what lemma 3.2 says"))
  return g.add(self._foot("m ² 減 T ² 非負而且自伴，所以引理 3.2 可以用——上一集那個推論在這裡第二次付現：那個數趨近零，向量就被逼著趨近零",
                          "m squared minus T squared is nonnegative and self-adjoint, so lemma 3.2 applies and last episode's consequence pays off a second time",
                          ACCENT_A,
                          "左邊藍色是那個數、右邊青色是那個向量的長度。沒有引理 3.2 的話，只知道數趨近零是推不出向量趨近零的",
                          "the blue bars are the number and the teal ones the length of the vector; without that lemma the first falling to zero would say nothing about the second"))

 def _compactness(self):
  oy = -0.12
  g = VGroup()

  def xi(n):
   c = 1.0 / n
   return lambda x: (phi(1)(x) + c * phi(2)(x)) / math.sqrt(1 + c * c)

  for ox, sx, sy, fam, lim, hd, ld in ((-6.00, 2.55, 0.30, xi, phi(1), "ξ ₙ", "φ ₁"),
                                       (-3.15, 2.55, 3.00,
                                        lambda n: (lambda x, n=n: T(xi(n))(x)),
                                        lambda x: M * phi(1)(x), "T ξ ₙ", "β")):
   g.add(self._frame(ox, oy, 2.66, 0.66, down=0.62))
   g.add(self._fcurve(ox, oy, sx, sy, lim, ACCENT_A, sw=3.2, n=120))
   for n, col in ((1, WARN), (2, ACCENT_C), (4, ACCENT_B), (8, DIM)):
    g.add(self._fcurve(ox, oy, sx, sy, fam(n), col, sw=1.6, n=120))
   g.add(self._sym(1.02, hd, INK, FS_TAG - 2, x=ox + sx / 2, w=1.20))
   g.add(self._sym(oy + sy * lim(0.5) + 0.24, ld, ACCENT_A, FS_TAG - 2,
                   x=ox + sx * 0.5, w=0.70))
  g.add(self._table((("     T ξ ₙ    ⟶    β", ACCENT_B),
                     ("     T ² ξ ₙ    ⟶    T β                m ² ξ ₙ    ⟶    T β", ACCENT_C),
                     (f"     ‖ β ‖  =  lim ‖ T ξ ₙ ‖  =  m  =  {M:.6f}", WARN),
                     ("     T ² ( β )    =    m ² β", ACCENT_A)),
                    y0=0.80, dy=0.32))
  g.add(self._cap("兩邊都收斂，可是先確定的是右邊那一張",
                  "both converge, but it is the right-hand one that is known first"))
  return g.add(self._foot("緊性第一次用上：T 緊，所以必要時取子列可以假設 T ξ ₙ 收斂到 β。於是 T ² ξ ₙ 趨近 T β，而上一拍說 m ² ξ ₙ 也趨近 T β",
                          "compactness is used here for the first time: the images converge along a subsequence, so T squared applied to them tends to T beta, and by the last beat so does m squared times them",
                          ACCENT_A,
                          f"因為 m 不是零，ξ ₙ 自己就等於 T ² ξ ₙ / m ²，於是也收斂。‖ β ‖ = m = {M:.6f} 不是零——手上於是有一個非零的 β 滿足 T ² β = m ² β。兩張圖的縱向尺度不同",
                          f"since m is not zero the vectors equal their own images under T squared over m squared, so they converge too, and the limit has norm m; the two panels use different vertical scales"))

 def _factor(self):
  cx, cy = -4.10, -0.24
  g = VGroup()
  g.add(self._box(cx, cy + 0.62, "( m − T ) ( m + T ) α   =   0", ACCENT_A,
                  w=3.60, h=0.52, size=FS_TAG - 1))
  for dx, col, lab in ((-1.20, ACCENT_B, "( m + T ) α  =  0"),
                       (1.20, ACCENT_C, "γ  =  ( m + T ) α  ≠  0")):
   g.add(self._arr([cx + 0.30 * (1 if dx > 0 else -1), cy + 0.34, 0],
                   [cx + dx, cy - 0.06, 0], DIM, sw=2.0, tl=0.12))
   g.add(self._sym(cy - 0.26, lab, col, FS_TAG - 3, x=cx + dx, w=2.10))
  g.add(self._sym(cy - 0.66, "T α  =  − m α", ACCENT_B, FS_TAG - 2, x=cx - 1.20, w=1.90),
        self._sym(cy - 0.66, "T γ  =  m γ", ACCENT_C, FS_TAG - 2, x=cx + 1.20, w=1.90))
  g.add(self._table(((f"     | r ₁ |   =   m   =   {M:.8f}", ACCENT_A),
                     (f"     T φ ₁   =   {r(1):.8f}  φ ₁", ACCENT_C),
                     (f"     ( − T ) φ ₁   =   − {r(1):.8f}  φ ₁", ACCENT_B),
                     ("     m ²  −  T ²   =   ( m − T ) ( m + T )", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("兩個分支都交出一個 | r | = m 的特徵向量",
                  "either branch hands over an eigenvector whose eigenvalue has size m"))
  return g.add(self._foot("β 除以自己的長度得到單位向量 α，而 0 = ( m ² − T ² ) α，把它分解成 ( m − T ) ( m + T ) α",
                          "normalising that vector gives a unit vector annihilated by the difference, and the difference factors as shown",
                          ACCENT_A,
                          "這一集的 Green 算子每個特徵值都是正的，所以走的永遠是右邊那一支；把 T 換成 − T，走的就是左邊那一支",
                          "for this operator every eigenvalue is positive so it is always the right-hand branch; flipping the sign of the operator fires the left-hand one"))

 def _induction(self):
  ox, oy, sx, sy = -5.90, -0.34, 3.30, 0.46
  g = VGroup(self._frame(ox, oy, 3.42, 0.70, down=0.66))
  for n, col in ((1, DIM), (2, ACCENT_C), (3, ACCENT_B)):
   g.add(self._fcurve(ox, oy, sx, sy, phi(n), col, sw=2.4 if n > 1 else 1.4, n=160))
  g.add(self._sym(oy + sy * math.sqrt(2.0) + 0.22, "φ ₁", DIM, FS_TAG - 2,
                  x=ox + sx * 0.5, w=0.70),
        self._sym(oy + sy * math.sqrt(2.0) + 0.22, "φ ₂", ACCENT_C, FS_TAG - 2,
                  x=ox + sx * 0.25, w=0.70))
  g.add(self._table((("     V ₂   =   { φ ₁ } ⊥            T [ V ₂ ]  ⊂  V ₂", ACCENT_A),
                     (f"     ( φ ₁ , φ ₂ )   =   {sp(phi(1), phi(2)):+.0e}", DIM),
                     (f"     | r ₂ |  =  ‖ T ↾ V ₂ ‖  =  {r(2):.8f}", ACCENT_C),
                     (f"     | r ₃ |  =  ‖ T ↾ V ₃ ‖  =  {r(3):.8f}", ACCENT_B),
                     (f"     | r ₄ |   =   {r(4):.8f}", DIM)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("每一步都在更小的空間上取範數，所以遞減",
                  "each step takes the norm on a smaller space, so the numbers decrease"))
  return g.add(self._foot("接下來跟定理 3.1 一樣：V ₂ 取 φ ₁ 的正交補，它在 T 底下不變，而 T 限制在上面仍然緊、仍然自伴，所以又生出 φ ₂",
                          "from here the induction is theorem 3.1's: the orthogonal complement of the first eigenvector is invariant, and the restriction is still compact and still self-adjoint",
                          ACCENT_A,
                          "| r ₙ | 就是 T 限制在 V ₙ 上的範數，而 V ₙ 一層層變小，所以 | r ₙ | 本來就遞減——可是「遞減」還不等於「趨近零」",
                          "each eigenvalue in absolute value is the norm of the restriction, and those spaces shrink, so the numbers decrease; but decreasing is not yet tending to zero"))

 def _decay(self):
  ox, oy = -5.85, -0.70
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.52, 0], color=DIM, stroke_width=1.3))
  g.add(self._dash([ox, oy + 0.42, 0], [ox + 3.30, oy + 0.42, 0], WARN, n=22, sw=1.3))
  g.add(self._sym(oy + 0.62, "2 b ²", WARN, FS_TAG - 3, x=ox + 2.90, w=0.90))
  top = PAIRS[0][2]
  for k, (i, j, d2, _s) in enumerate(PAIRS):
   x = ox + 0.62 + k * 0.72
   g.add(Line([x, oy, 0], [x, oy + 1.26 * d2 / top, 0], color=ACCENT_B, stroke_width=7.0))
   g.add(self._sym(oy - 0.28, f"{i} , {j}", DIM, FS_TAG - 3, x=x, w=0.70))
  g.add(self._table((("       i , j       ‖ T φ ᵢ − T φ ⱼ ‖ ²        r ᵢ ² + r ⱼ ²", DIM),)
                    + tuple((f"     {i} , {j}         {d2:.8f}          {s:.8f}", ACCENT_B)
                            for i, j, d2, s in PAIRS)
                    + ((f"     ‖ φ ᵢ − φ ⱼ ‖ ²   =   {SEP:.4f}", WARN),),
                    y0=0.86, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("長條掉下去，就是子列收斂得起來的意思",
                  "the bars falling is what lets a subsequence converge at all"))
  return g.add(self._foot("| r ₙ | 若不趨近零，就有 b 大於零使每個 | r ₙ | 不小於 b。可是兩個像的距離平方正好是 r ᵢ ² + r ⱼ ²，於是永遠不小於 2 b ²",
                          "if the eigenvalues did not tend to zero there would be a positive lower bound, but the squared distance between two images is exactly the sum of their squares",
                          ACCENT_A,
                          "那樣 { T φ ᵢ } 就抽不出收斂子列，與 T 緊矛盾——所以 | r ₙ | 必須趨近零。最後一列是原本的 φ ᵢ，它們永遠差 2，這正是恆等映射不緊的原因",
                          "then no subsequence of the images could converge, contradicting compactness, so the eigenvalues must die away; the last row is the same distance for the eigenvectors themselves"))

 def _coefficients(self):
  ox, oy = -5.85, -0.66
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.50, 0], color=DIM, stroke_width=1.3))
  sa = 1.24 / max(abs(v) for v in A_CO[:6])
  sb = 1.24 / max(abs(v) for v in B_CO[:6])
  for k in range(6):
   x = ox + 0.46 + k * 0.50
   g.add(Line([x - 0.11, oy, 0], [x - 0.11, oy + sa * abs(A_CO[k]), 0],
              color=ACCENT_B, stroke_width=6.0),
         Line([x + 0.11, oy, 0], [x + 0.11, oy + sb * abs(B_CO[k]), 0],
              color=ACCENT_C, stroke_width=6.0))
   g.add(self._sym(oy - 0.26, f"{k + 1}", DIM, FS_TAG - 3, x=x, w=0.40))
  for y0_, col, lab, lw in ((1.20, ACCENT_B, "a ₙ", 0.70), (0.92, ACCENT_C, "b ₙ", 0.70)):
   g.add(Line([ox + 0.10, y0_, 0], [ox + 0.32, y0_, 0], color=col, stroke_width=6.0),
         self._sym(y0_, lab, col, FS_TAG - 3, x=ox + 0.58, w=lw))
  g.add(self._table((("       n          a ₙ            b ₙ            r ₙ a ₙ", DIM),)
                    + tuple((f"     {n:3d}     {A_CO[n - 1]:+.8f}   {B_CO[n - 1]:+.8f}   "
                             f"{r(n) * A_CO[n - 1]:+.8f}", ACCENT_B)
                            for n in (1, 2, 3, 5)),
                    y0=0.86, dy=0.32, size=FS_TAG - 4))
  g.add(self._cap("後兩欄逐列相同，這一拍全靠它",
                  "the last two columns agree row by row: the whole beat is that"))
  return g.add(self._foot("設 β = T α，兩者的 Fourier 係數滿足 b ₙ = r ₙ a ₙ。證明就一行：把 T 從內積的一邊搬到另一邊，碰到 T φ ₙ = r ₙ φ ₙ",
                          "if beta is the image of alpha their Fourier coefficients differ by the eigenvalue, proved in one line by moving T across the product onto the eigenvector",
                          ACCENT_A,
                          "這裡 α 取常數函數 1，所以偶數項的係數是零。兩排長條各自正規化過，才看得出 b ₙ 掉得比 a ₙ 快很多——那個比例就是 r ₙ",
                          "here the source is the constant function, so the even coefficients vanish; the two rows of bars are separately scaled, which is how the much faster decay shows up"))

 def _tail(self):
  ox, oy = -5.85, -0.70
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.50, 0], color=DIM, stroke_width=1.3))
  top = max(b for _n, _r, b in TAIL)
  for k, (n, res, bnd) in enumerate(TAIL):
   x = ox + 0.56 + k * 0.62
   g.add(Line([x + 0.12, oy, 0], [x + 0.12, oy + 1.24 * bnd / top, 0],
              color=WARN, stroke_width=7.0),
         Line([x - 0.12, oy, 0], [x - 0.12, oy + 1.24 * res / top, 0],
              color=ACCENT_B, stroke_width=7.0))
   g.add(self._sym(oy - 0.26, f"{n}", DIM, FS_TAG - 3, x=x, w=0.40))
  for y0_, col, lab, lw in ((1.20, ACCENT_B, "‖ β − Σ ₁ ⁿ b ᵢ φ ᵢ ‖", 1.90),
                            (0.92, WARN, "| r ₙ ₊ ₁ |  ‖ α ‖", 1.60)):
   g.add(Line([ox + 0.10, y0_, 0], [ox + 0.32, y0_, 0], color=col, stroke_width=6.0),
         self._sym(y0_, lab, col, FS_TAG - 3, x=ox + 0.42 + lw / 2, w=lw))
  g.add(self._table((("       n        ‖ β − Σ ₁ ⁿ b ᵢ φ ᵢ ‖         | r ₙ ₊ ₁ | ‖ α ‖", DIM),)
                    + tuple((f"     {n:3d}          {res:.3e}               {bnd:.3e}",
                             ACCENT_B) for n, res, bnd in TAIL)
                    + (("     N ( T )   =   R ( T ) ⊥", ACCENT_A),),
                    y0=0.80, dy=0.24, size=FS_TAG - 3))
  g.add(self._cap("藍色永遠在紅色底下，而兩排一起掉向零",
                  "the estimate holds at every n, and both fall to zero"))
  return g.add(self._foot("β 減掉前 n 項等於 T 作用在 α 減掉前 n 項上，後者落在 V ₙ ₊ ₁ 裡、長度不超過 ‖ α ‖，所以尾巴不超過 | r ₙ ₊ ₁ | ‖ α ‖",
                          "the tail of beta is T applied to the tail of alpha, which lies in the next complement and is no longer than alpha, so the tail is bounded by the next eigenvalue",
                          ACCENT_A,
                          "第 5 章到此結束（這一節整節沒有習題）。下一章會認出某個微分算子的右反元素是緊而自伴的——Fourier 級數就是這個定理的推論",
                          "chapter 5 ends here, with no exercises in this section at all; the next chapter recognises a right inverse of a differential operator as compact and self-adjoint, and Fourier series follow"))

 def stage(self):
  a, b, c = self._nospectrum(), self._compact(), self._theorem()
  d, e, f_ = self._opening(), self._lemma(), self._compactness()
  h, i, j = self._factor(), self._induction(), self._decay()
  k, l = self._coefficients(), self._tail()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE73ZH, AdvCalcE73EN = make(AdvCalcE73Base, "73", prefix="AdvCalcE")
