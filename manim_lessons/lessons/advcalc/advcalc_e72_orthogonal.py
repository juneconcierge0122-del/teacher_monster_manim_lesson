"""advcalc E72 -- chapter 5, section 4 (book pp. 262-263): the adjoint as a map of
V into itself, orthogonal transformations, and the polar decomposition.

Section 2 closed by showing that theta from V into its conjugate space is an
isomorphism exactly when V is complete.  On a Hilbert space, then, the adjoint
need not live in Hom of the conjugate space: conjugating it back by theta gives
a map of V into itself, and that is what Hilbert space theory calls the adjoint.
It is pinned down by (T alpha, beta) = (alpha, T* beta), its matrix is the
transpose, and T is self-adjoint exactly when T = T*.

Then the other important class: T is orthogonal when it preserves the scalar
product, equivalently when T*T = I.  Such a T preserves norms, so it is
injective, and on a finite-dimensional space the condition becomes T* = T^-1.
Written out in Hom R^n it says the columns of the matrix are orthonormal, which
is Theorem 4.1.  Theorem 4.2 is last episode's spectral theorem restated: a
symmetric matrix is conjugated into a diagonal one by an orthogonal matrix.
Theorem 4.3 is the polar decomposition: T*T is self-adjoint with positive
eigenvalues (each one is ||T phi_i||^2), so it has a positive square root S, and
S composed with T inverse turns out to be orthogonal -- five moves across the
product and nothing is left.  Hence T = RS, the analogue of z = r exp(i theta),
and the corollary factors any nonsingular matrix as u d v.

Exercises 4.1 to 4.8 run from 263 to 264, and section 5 (compact
transformations) starts on 264 and has no exercises at all.

Two matrices carry the episode.  T = [[2, 0.6], [-0.4, 1.5]] is invertible and
neither symmetric nor orthogonal, so it has an honest polar decomposition: a
rotation by -15.9453 degrees times the positive matrix whose eigenvalues are the
singular values 2.0893 and 1.5508.  The symmetric matrix of Theorem 4.2 is
E71's [[2, 0.8], [0.8, 1.2]], diagonalised back to the same eigenvalues 2.4944
and 0.7056 it had there.  A rotation, a reflection, and a diagonal matrix whose
columns are orthogonal but not normalised supply the orthogonality tests.
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
TAU = 2.0 * math.pi


def mv(M, v):
 return tuple(sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M)))


def mm(A, B):
 n = len(A)
 return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def tp(M):
 return [[M[j][i] for j in range(len(M))] for i in range(len(M))]


def inv2(M):
 d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
 return [[M[1][1] / d, -M[0][1] / d], [-M[1][0] / d, M[0][0] / d]]


def det2(M):
 return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def dot(a, b):
 return sum(x * y for x, y in zip(a, b))


def nrm(v):
 return math.sqrt(dot(v, v))


def unit(th):
 return (math.cos(th), math.sin(th))


def dev(A, B):
 return max(abs(A[i][j] - B[i][j]) for i in range(len(A)) for j in range(len(A)))


IDM = [[1.0, 0.0], [0.0, 1.0]]

# ── beats 1 to 3: the adjoint as a map of V into itself ───────────────
TG = [[2.0, 0.6], [-0.4, 1.5]]
TS = tp(TG)
AL, BE = (1.0, 0.6), (0.4, 1.3)
ADJ_L, ADJ_R = dot(mv(TG, AL), BE), dot(AL, mv(TS, BE))
assert abs(ADJ_L - ADJ_R) < 1e-12, "the identity that pins the adjoint down"
assert dev(TG, TS) > 0.9, "and this T is nowhere near self-adjoint"

# the direct definition: for a fixed eta the functional is represented by T* eta
BETA_ETA = mv(TS, BE)
REP = [(x, dot(mv(TG, x), BE), dot(x, BETA_ETA))
       for x in ((1.0, 0.0), (0.0, 1.0), AL, (-0.7, 0.5))]
assert all(abs(a - b) < 1e-12 for _x, a, b in REP), \
    "one vector represents the functional, whichever xi it is tested against"
NDIR = 1440
SUPF = max(abs(dot(mv(TG, unit(TAU * k / NDIR)), BE)) for k in range(NDIR))
assert abs(SUPF - nrm(BETA_ETA)) < 1e-4, \
    "and the functional's norm is that vector's norm, which is why it is bounded"

# ── beats 4 to 6: orthogonal ──────────────────────────────────────────
THR = 0.6
RO = [[math.cos(THR), -math.sin(THR)], [math.sin(THR), math.cos(THR)]]
THF = 0.35
RF = [[math.cos(2 * THF), math.sin(2 * THF)], [math.sin(2 * THF), -math.cos(2 * THF)]]
NB = [[1.8, 0.0], [0.0, 0.5]]
BASE = dot(AL, BE)
TESTS = [("rot", RO, dot(mv(RO, AL), mv(RO, BE))),
         ("ref", RF, dot(mv(RF, AL), mv(RF, BE))),
         ("dia", NB, dot(mv(NB, AL), mv(NB, BE)))]
assert abs(TESTS[0][2] - BASE) < 1e-12 and abs(TESTS[1][2] - BASE) < 1e-12, \
    "a rotation and a reflection both preserve the product"
assert abs(TESTS[2][2] - BASE) > 0.10, \
    "while a diagonal matrix with orthogonal but unequal columns does not"
for _n, _M, _v in TESTS[:2]:
 assert dev(mm(tp(_M), _M), IDM) < 1e-15, "which is exactly T*T = I"
assert dev(mm(tp(NB), NB), IDM) > 0.3
assert abs(det2(RO) - 1.0) < 1e-12 and abs(det2(RF) + 1.0) < 1e-12, \
    "the reflection is orthogonal too: orthogonal does not mean rotation"

NORMS = [(x, nrm(x), nrm(mv(RO, x)), nrm(mv(NB, x)))
         for x in ((1.0, 0.0), AL, (-0.7, 0.5))]
assert all(abs(a - b) < 1e-12 for _x, a, b, _c in NORMS), \
    "an orthogonal T preserves every norm, so its null space is zero"
assert any(abs(a - c) > 0.1 for _x, a, _b, c in NORMS)
assert dev(tp(RO), inv2(RO)) < 1e-12, "and once invertible, the adjoint is the inverse"

COLS = []
for _n, _M in (("rot", RO), ("ref", RF), ("dia", NB)):
 c0, c1 = (_M[0][0], _M[1][0]), (_M[0][1], _M[1][1])
 COLS.append((_n, nrm(c0), nrm(c1), dot(c0, c1)))
assert all(abs(a - 1) < 1e-12 and abs(b - 1) < 1e-12 for _n, a, b, _d in COLS[:2])
assert abs(COLS[2][1] - 1.8) < 1e-12 and abs(COLS[2][3]) < 1e-15, \
    "the third one's columns are orthogonal but not of length one, and that is enough to fail"

# ── beat 7: theorem 4.2, on the symmetric matrix of E71 ───────────────
SY = [[2.0, 0.8], [0.8, 1.2]]
SL1 = (3.2 + math.sqrt(3.2)) / 2
SL2 = (3.2 - math.sqrt(3.2)) / 2
_v1 = (SY[0][1], SL1 - SY[0][0])
V1 = (_v1[0] / nrm(_v1), _v1[1] / nrm(_v1))
V2 = (-V1[1], V1[0])
BM = [[V1[0], V2[0]], [V1[1], V2[1]]]
DM = mm(mm(inv2(BM), SY), BM)
assert dev(mm(tp(BM), BM), IDM) < 1e-12, "the eigenvectors as columns make an orthogonal matrix"
assert abs(DM[0][1]) < 1e-12 and abs(DM[1][0]) < 1e-12, "and the conjugate is diagonal"
assert abs(DM[0][0] - SL1) < 1e-12 and abs(DM[1][1] - SL2) < 1e-12, \
    "with E71's own eigenvalues on it"
assert dev(inv2(BM), tp(BM)) < 1e-12, "so the inverse in the theorem is just a transpose"

# ── beats 8 to 10: the polar decomposition ────────────────────────────
TT = mm(TS, TG)
assert dev(TT, tp(TT)) < 1e-15, "T*T is self-adjoint whatever T is"
_t, _d = TT[0][0] + TT[1][1], det2(TT)
R1 = (_t + math.sqrt(_t * _t - 4 * _d)) / 2
R2 = (_t - math.sqrt(_t * _t - 4 * _d)) / 2
_w1 = (TT[0][1], R1 - TT[0][0])
W1 = (_w1[0] / nrm(_w1), _w1[1] / nrm(_w1))
W2 = (-W1[1], W1[0])
assert min(R1, R2) > 0, "and its eigenvalues are positive, because each one is a squared norm"
for _w, _r in ((W1, R1), (W2, R2)):
 assert abs(nrm(mv(TG, _w)) ** 2 - _r) < 1e-12, "that is the identity making them positive"
SG1, SG2 = math.sqrt(R1), math.sqrt(R2)
QM = [[W1[0], W2[0]], [W1[1], W2[1]]]
SM = mm(mm(QM, [[SG1, 0.0], [0.0, SG2]]), tp(QM))
assert dev(mm(SM, SM), TT) < 1e-12 and dev(SM, tp(SM)) < 1e-12, \
    "S is the positive square root of T*T, and self-adjoint"

AM = mm(SM, inv2(TG))
assert dev(mm(tp(AM), AM), IDM) < 1e-12, "and S composed with T inverse is orthogonal"
CHAIN = [dot(mv(AM, AL), mv(AM, BE)),
         dot(mv(inv2(TG), AL), mv(mm(SM, SM), mv(inv2(TG), BE))),
         dot(mv(inv2(TG), AL), mv(TS, BE)),
         dot(AL, BE)]
assert max(abs(c - BASE) for c in CHAIN) < 1e-12, "the five moves of the proof, one number each"
RM = inv2(AM)
assert dev(mm(RM, SM), TG) < 1e-12, "so T factors as an orthogonal times a positive one"
assert dev(mm(tp(RM), RM), IDM) < 1e-12 and abs(det2(RM) - 1.0) < 1e-12
RANG = math.degrees(math.atan2(RM[1][0], RM[0][0]))
assert -20.0 < RANG < -10.0, "the rotation the polar decomposition picks out"
TTS = mm(TG, TS)
assert dev(TTS, tp(TTS)) < 1e-15 and dev(TTS, TT) > 0.4, \
    "the other order starts from T T*, which is a different matrix"

# ── beat 11: t = u d v ────────────────────────────────────────────────
DD = mm(mm(inv2(QM), SM), QM)
UM = mm(RM, QM)
VM = inv2(QM)
assert abs(DD[0][1]) < 1e-12 and abs(DD[1][0]) < 1e-12, "theorem 4.2 diagonalises the symmetric factor"
assert abs(DD[0][0] - SG1) < 1e-9 and abs(DD[1][1] - SG2) < 1e-9
assert dev(mm(mm(UM, DD), VM), TG) < 1e-12, "and the three factors multiply back to the matrix"
for _M in (UM, VM):
 assert dev(mm(tp(_M), _M), IDM) < 1e-12, "with both outer factors orthogonal"


class AdvCalcE72Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 72

 MODE_LABEL = {
  0: {"zh": "把伴隨搬回 V 裡", "en": "bringing the adjoint back into V"},
  1: {"zh": "不繞共軛空間的定義", "en": "the definition without the dual"},
  2: {"zh": "T 星的矩陣是轉置", "en": "the matrix of the adjoint is the transpose"},
  3: {"zh": "正交的定義", "en": "what orthogonal means"},
  4: {"zh": "保長度 ⟹ 單射", "en": "norms preserved, so injective"},
  5: {"zh": "定理 4.1：各欄正交規範", "en": "theorem 4.1: orthonormal columns"},
  6: {"zh": "定理 4.2：對稱可正交對角化", "en": "theorem 4.2: symmetric means diagonalisable"},
  7: {"zh": "T 星 T 的特徵值都是正的", "en": "the eigenvalues of T*T are positive"},
  8: {"zh": "五個等號", "en": "five moves across the product"},
  9: {"zh": "定理 4.3：極分解", "en": "theorem 4.3: the polar decomposition"},
  10: {"zh": "推論：t = u d v", "en": "the corollary"},
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

 def _cross(self, cx, cy, w=1.25, h=1.05):
  return VGroup(Line([cx - w, cy, 0], [cx + w, cy, 0], color=DIM, stroke_width=1.1),
                Line([cx, cy - h, 0], [cx, cy + h, 0], color=DIM, stroke_width=1.1))

 def _vec(self, cx, cy, s, v, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=sw, tl=tl)

 def _pt(self, cx, cy, s, v, col, r=0.065):
  return Dot([cx + s * v[0], cy + s * v[1], 0], radius=r, color=col)

 def _lab(self, cx, cy, s, v, txt, col, dx=0.24, dy=0.24, w=0.90):
  return self._sym(cy + s * v[1] + dy, txt, col, FS_TAG - 1, x=cx + s * v[0] + dx, w=w)

 def _image(self, cx, cy, s, M, col, n=96, sw=2.0):
  """The image of the unit circle under M, which is what a 2x2 matrix looks like."""
  return self._curve([[cx + s * mv(M, unit(TAU * k / n))[0],
                       cy + s * mv(M, unit(TAU * k / n))[1], 0] for k in range(n + 1)],
                     col, sw=sw)

 def _mat(self, cx, cy, M, col, fmt="{:.4f}", dx=0.86, dy=0.46, size=FS_TAG - 2, **kw):
  return self._numgrid(cx, cy, [[fmt.format(v) for v in row] for row in M],
                       dx=dx, dy=dy, size=size, color=col, **kw)

 # ── beats ─────────────────────────────────────────────────────────
 def _adjoint(self):
  x0, x1, y0, y1 = -5.15, -2.45, 0.62, -0.42
  g = VGroup()
  g.add(self._box(x0, y0, "V", ACCENT_B, w=0.80, h=0.52),
        self._box(x1, y0, "V", ACCENT_B, w=0.80, h=0.52),
        self._box(x0, y1, "V *", ACCENT_C, w=0.90, h=0.52),
        self._box(x1, y1, "V *", ACCENT_C, w=0.90, h=0.52))
  g.add(self._arr([x0 + 0.46, y0, 0], [x1 - 0.46, y0, 0], INK, sw=2.4, tl=0.14),
        self._arr([x1 - 0.52, y1, 0], [x0 + 0.52, y1, 0], INK, sw=2.4, tl=0.14),
        self._arr([x0, y0 - 0.30, 0], [x0, y1 + 0.30, 0], ACCENT_A, sw=2.4, tl=0.14),
        self._arr([x1, y1 + 0.30, 0], [x1, y0 - 0.30, 0], WARN, sw=2.4, tl=0.14))
  g.add(self._sym(y0 + 0.34, "θ ⁻ ¹ ∘ T * ∘ θ", ACCENT_A, FS_TAG - 2,
                  x=(x0 + x1) / 2, w=2.40),
        self._sym(y1 - 0.34, "T *", INK, FS_TAG, x=(x0 + x1) / 2, w=0.70),
        self._sym((y0 + y1) / 2, "θ", ACCENT_A, FS_TAG, x=x0 - 0.34, w=0.50),
        self._sym((y0 + y1) / 2, "θ ⁻ ¹", WARN, FS_TAG, x=x1 + 0.48, w=0.90))
  g.add(self._table((("     θ  :   V   ≅   V *", ACCENT_A),
                     (f"     ( T α , β )     =     {ADJ_L:.4f}", ACCENT_B),
                     (f"     ( α , T * β )     =     {ADJ_R:.4f}", ACCENT_B),
                     ("     T  =  T *        ⇔        T  =  θ ⁻ ¹ ∘ T * ∘ θ", DIM)),
                    y0=0.82, dy=0.34))
  g.add(self._cap("上排那個 T 星是搬回 V 裡的版本",
                  "the map along the top is the one brought back into V"))
  return g.add(self._foot("第 2 節收在「θ 是同構的充要條件是 V 完備」。V 是 Hilbert 空間時 θ 可逆，所以可以把 Hom V 星裡的伴隨用 θ 共軛回 Hom V",
                          "section 2 closed on theta being an isomorphism exactly when the space is complete, so on a Hilbert space the adjoint can be conjugated back into maps of V itself",
                          ACCENT_A,
                          "搬回來之後它由 ( T α , β ) = ( α , T * β ) 唯一決定，而 T 自伴的意思就簡化成一行：T 等於 T 星",
                          "once back, it is pinned down uniquely by the identity in the formula bar, and self-adjointness collapses to the one line T equals T star"))

 def _direct(self):
  cx, cy, s = -4.55, -0.14, 0.82
  nb = nrm(BETA_ETA)
  bh = (BETA_ETA[0] / nb, BETA_ETA[1] / nb)
  g = VGroup(self._cross(cx, cy, w=1.32, h=0.95))
  g.add(self._image(cx, cy, s, IDM, DIM, sw=1.3))
  g.add(self._vec(cx, cy, s, bh, ACCENT_B, sw=2.8))
  g.add(self._lab(cx, cy, s, bh, "β", ACCENT_B, dx=0.30, dy=0.16))
  d = s / nb
  foot = [cx + d * bh[0], cy + d * bh[1], 0]
  perp = (-bh[1], bh[0])
  g.add(self._dash([foot[0] - 1.15 * perp[0], foot[1] - 1.15 * perp[1], 0],
                   [foot[0] + 1.15 * perp[0], foot[1] + 1.15 * perp[1], 0],
                   ACCENT_C, n=20, sw=1.8))
  g.add(Dot(foot, radius=0.055, color=ACCENT_C))
  g.add(self._sym(foot[1] + 0.30, "( ξ , β )  =  1", ACCENT_C, FS_TAG - 2,
                  x=cx + 1.62, w=1.60))
  g.add(self._table((("       ξ          ( T ξ , η )       ( ξ , β )", DIM),)
                    + tuple((f"     ⟨ {x[0]:.1f} , {x[1]:.1f} ⟩      {aa:.4f}         {bb:.4f}",
                             ACCENT_B) for x, aa, bb in REP[:3])
                    + ((f"     sup | ( T ξ , η ) |   =   {SUPF:.4f}", ACCENT_C),
                       (f"     ‖ β ‖   =   {nb:.4f}", ACCENT_A)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("最後兩列一樣，所以那個泛函有界",
                  "the last two agree, which is why the functional is bounded"))
  return g.add(self._foot("固定 η 之後，ξ 送到 ( T ξ , η ) 是線性又有界的，所以是 V 星的元素——定理 2.4 說它由唯一一個 β 代表",
                          "with eta fixed, sending xi to that product is linear and bounded, so it is an element of the conjugate space, and theorem 2.4 says one vector represents it",
                          ACCENT_A,
                          f"左圖的虛線是 ( ξ , β ) = 1 那條直線，它離原點 1 / ‖ β ‖ = {1 / nb:.4f}——泛函愈大，那條線就愈靠近原點，而 β 垂直於它",
                          f"the dashed line on the left is where the functional takes the value one; it sits at one over the norm from the origin, perpendicular to that vector"))

 def _transpose(self):
  g = VGroup()
  ga, _p = self._mat(-5.05, 0.24, TG, ACCENT_B, fmt="{:.1f}", dx=0.76)
  gb, _q = self._mat(-2.65, 0.24, TS, ACCENT_C, fmt="{:.1f}", dx=0.76)
  g.add(ga, gb)
  g.add(self._sym(0.96, "t", ACCENT_B, FS_TAG - 1, x=-5.05, w=0.50),
        self._sym(0.96, "t *", ACCENT_C, FS_TAG - 1, x=-2.65, w=0.70),
        self._arr([-4.10, 0.24, 0], [-3.60, 0.24, 0], DIM, sw=2.2, tl=0.12))
  g.add(self._sym(-0.46, f"t ₁₂  =  {TG[0][1]:.1f}", ACCENT_B, FS_TAG - 2, x=-5.05, w=1.70),
        self._sym(-0.46, f"t * ₂₁  =  {TS[1][0]:.1f}", ACCENT_C, FS_TAG - 2, x=-2.65, w=1.70))
  g.add(self._table((("     t * ᵢⱼ   =   ( φ ᵢ , T * φ ⱼ )   =   ( T φ ᵢ , φ ⱼ )   =   t ⱼᵢ",
                      ACCENT_A),
                     (f"     ( T α , β )  =  ( α , T * β )  =  {ADJ_L:.4f}", ACCENT_B),
                     (f"     max | t ᵢⱼ − t ⱼᵢ |   =   {dev(TG, TS):.4f}", WARN),
                     ("     T  ≠  T *", WARN)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("這個 T 的兩個非對角項差一整格，所以不自伴",
                  "this matrix is far from its own transpose, so it is not self-adjoint"))
  return g.add(self._foot("引理 3.1 那段矩陣計算一字不改地推廣：t * ᵢⱼ 就是 t ⱼᵢ，把 T 從內積的一邊搬到另一邊，指標就換位",
                          "the matrix calculation of lemma 3.1 generalises word for word: moving T from one side of the product to the other swaps the two indices",
                          ACCENT_A,
                          "所以 T 自伴 ⇔ T = T * ⇔ 矩陣等於自己的轉置。上一集講的對稱，就是這一句在正交規範基下的樣子",
                          "so self-adjoint means the matrix equals its own transpose, which is exactly last episode's symmetry seen against an orthonormal basis"))

 def _orthogonal(self):
  cx, cy, s = -4.75, -0.16, 0.66
  g = VGroup(self._cross(cx, cy, w=1.20, h=0.92))
  for v, col in ((AL, ACCENT_B), (BE, ACCENT_C)):
   g.add(self._vec(cx, cy, s, v, col, sw=2.2))
   g.add(self._vec(cx, cy, s, mv(RO, v), col, sw=1.4, tl=0.10))
  dx2 = -1.80
  g.add(self._cross(dx2, cy, w=1.20, h=0.92))
  for v, col in ((AL, ACCENT_B), (BE, ACCENT_C)):
   g.add(self._vec(dx2, cy, s, v, col, sw=2.2))
   g.add(self._vec(dx2, cy, s, mv(NB, v), col, sw=1.4, tl=0.10))
  g.add(self._sym(1.04, "R", ACCENT_A, FS_TAG - 2, x=cx, w=0.60),
        self._sym(1.04, "N", WARN, FS_TAG - 2, x=dx2, w=0.60))
  g.add(self._table(((f"     ( α , β )     =     {BASE:.4f}", ACCENT_A),
                     (f"     ( R α , R β )   =   {TESTS[0][2]:.4f}", ACCENT_B),
                     (f"     ( F α , F β )   =   {TESTS[1][2]:.4f}", ACCENT_C),
                     (f"     ( N α , N β )   =   {TESTS[2][2]:.4f}", WARN),
                     (f"     det R  =  {det2(RO):.1f}        det F  =  {det2(RF):.1f}", DIM)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("前三列一樣，第四列差了那麼多",
                  "the first three agree; the fourth does not"))
  return g.add(self._foot("T 叫正交，就是它保純量積。用伴隨恆等式改寫一次：( α , T * T β ) = ( α , β ) 對每一對成立，等價於 T * T = I",
                          "T is orthogonal when it preserves the scalar product, and rewriting once with the adjoint identity turns that into the single equation in the formula bar",
                          ACCENT_A,
                          "轉了 0.6 弧度的 R 與一個鏡射 F 都正交（行列式 + 1 與 − 1），右邊的 N 兩欄正交卻不等長，就不是",
                          "a rotation and a reflection are both orthogonal, with determinants plus and minus one, while the matrix on the right has orthogonal columns of unequal length and is not"))

 def _injective(self):
  cx, cy, s = -4.75, -0.16, 0.62
  g = VGroup(self._cross(cx, cy, w=1.15, h=0.90))
  g.add(self._image(cx, cy, s, IDM, DIM, sw=1.4),
        self._image(cx, cy, s, RO, ACCENT_B, sw=2.4))
  dx2 = -1.80
  g.add(self._cross(dx2, cy, w=1.15, h=0.90))
  g.add(self._image(dx2, cy, s, IDM, DIM, sw=1.4),
        self._image(dx2, cy, s, NB, WARN, sw=2.4))
  g.add(self._sym(1.04, "R", ACCENT_B, FS_TAG - 2, x=cx, w=0.60),
        self._sym(1.04, "N", WARN, FS_TAG - 2, x=dx2, w=0.60))
  g.add(self._table((("       α          ‖ α ‖        ‖ R α ‖       ‖ N α ‖", DIM),)
                    + tuple((f"     ⟨ {x[0]:.1f} , {x[1]:.1f} ⟩    {a:.4f}      {b:.4f}      {c:.4f}",
                             ACCENT_B if abs(a - b) < 1e-9 else WARN)
                            for x, a, b, c in NORMS)
                    + ((f"     max | t * ᵢⱼ − ( t ⁻ ¹ ) ᵢⱼ |   =   {dev(tp(RO), inv2(RO)):.1e}",
                        ACCENT_A),),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("R 把單位圓送回單位圓，N 把它壓成橢圓",
                  "the rotation returns the circle to itself; the other flattens it"))
  return g.add(self._foot("正交的 T 保長度，所以 T α = 0 逼出 α = 0：它單射。V 有限維時單射就可逆",
                          "an orthogonal T preserves norms, so nothing but zero goes to zero and it is injective, which in finite dimensions already means invertible",
                          ACCENT_A,
                          "可逆之後 T * T = I 就寫成 T * = T ⁻ ¹。最後一列驗的正是這件事：轉置與反矩陣逐項相同",
                          "once invertible the condition reads as the adjoint being the inverse, which is what the last row checks entry by entry"))

 def _columns(self):
  cx, cy, s = -4.55, -0.24, 0.78
  g = VGroup(self._cross(cx, cy, w=1.30, h=0.92))
  for v in ((1.0, 0.0), (0.0, 1.0)):
   g.add(self._vec(cx, cy, s, v, DIM, sw=1.6, tl=0.10))
  for j, col in ((0, ACCENT_B), (1, ACCENT_C)):
   c = (RO[0][j], RO[1][j])
   g.add(self._vec(cx, cy, s, c, col, sw=2.8))
   g.add(self._pt(cx, cy, s, c, col, r=0.06))
  g.add(self._image(cx, cy, s, IDM, DIM, sw=1.2))
  g.add(self._lab(cx, cy, s, (RO[0][0], RO[1][0]), "T δ ¹", ACCENT_B, dx=0.42, dy=-0.02,
                  w=1.10),
        self._lab(cx, cy, s, (RO[0][1], RO[1][1]), "T δ ²", ACCENT_C, dx=-0.42, dy=0.24,
                  w=1.10))
  g.add(self._table((("       t          ‖ c ₁ ‖       ‖ c ₂ ‖      ( c ₁ , c ₂ )", DIM),)
                    + tuple((f"     {n}        {a:.4f}      {b:.4f}      {d:+.0e}",
                             ACCENT_B if abs(a - 1) < 1e-9 else WARN)
                            for n, a, b, d in COLS),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("第三列兩欄仍然正交，可是長度不是一",
                  "the third row still has orthogonal columns, of the wrong length"))
  return g.add(self._foot("把 T * T = I 寫成矩陣就是 Σ ₖ t ₖᵢ t ₖⱼ = δ ᵢⱼ：t 的第 i 欄與第 j 欄的內積。這說的正是各欄構成正交規範集",
                          "written out as matrices the condition says that column i dotted with column j is the Kronecker delta, which is to say the columns form an orthonormal set",
                          ACCENT_A,
                          "定理 4.1 因此是：T 正交 ⇔ 標準基的像又是一組正交規範基。注意「正交」不夠——上一集的引理 3.1 也是卡在正規化那半",
                          "so theorem 4.1 reads: T is orthogonal exactly when the standard basis goes to another orthonormal basis, and orthogonal alone is not enough, just as in lemma 3.1"))

 def _diagonalise(self):
  cx, cy, s = -5.30, -0.20, 0.62
  g = VGroup(self._cross(cx, cy, w=0.95, h=0.80))
  g.add(self._image(cx, cy, s, IDM, DIM, sw=1.2))
  for v, col in ((V1, ACCENT_B), (V2, ACCENT_C)):
   g.add(self._vec(cx, cy, s, v, col, sw=2.6))
  g.add(self._sym(1.00, "b", ACCENT_A, FS_TAG - 2, x=cx, w=0.60))
  gg, _p = self._mat(-2.55, 0.22, DM, ACCENT_A, dx=1.10)
  g.add(gg, self._sym(1.00, "b ⁻ ¹  t  b", ACCENT_A, FS_TAG - 2, x=-2.55, w=2.00))
  g.add(self._table(((f"     λ ₁   =   {SL1:.6f}", ACCENT_B),
                     (f"     λ ₂   =   {SL2:.6f}", ACCENT_C),
                     (f"     max | ( b * b ) ᵢⱼ − δ ᵢⱼ |   =   {dev(mm(tp(BM), BM), IDM):.1e}",
                      ACCENT_A),
                     (f"     max | b ⁻ ¹ ᵢⱼ − t * ᵢⱼ |   =   {dev(inv2(BM), tp(BM)):.1e}", DIM),
                     ("     t  =  t *", DIM)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("兩個對角項就是上一集那兩個特徵值",
                  "the two diagonal entries are last episode's eigenvalues"))
  return g.add(self._foot("定理 4.2：對稱的 t 一定有正交的 b 使 b ⁻ ¹ t b 對角。證明就是上一集：t 給的 T 自伴，取正交規範特徵基當 b 的各欄",
                          "theorem 4.2: a symmetric matrix is conjugated into a diagonal one by an orthogonal matrix, and the proof is last episode's spectral theorem with the eigenbasis as the columns",
                          ACCENT_A,
                          "左圖的 b 就是那組特徵向量。這裡故意用回 E71 那個 [[2 , 0.8] , [0.8 , 1.2]]，對角線上出來的正是 2.4944 與 0.7056",
                          "the frame on the left is that eigenbasis, and the matrix is deliberately E71's own, so the diagonal comes out as the two eigenvalues it had there"))

 def _positive(self):
  cx, cy, s = -4.95, -0.18, 0.42
  g = VGroup(self._cross(cx, cy, w=1.30, h=0.92))
  g.add(self._image(cx, cy, s, IDM, DIM, sw=1.4),
        self._image(cx, cy, s, TG, ACCENT_B, sw=2.4))
  for w, sg, col in ((W1, SG1, ACCENT_A), (W2, SG2, WARN)):
   g.add(self._vec(cx, cy, s, mv(TG, w), col, sw=2.4))
  g.add(self._sym(1.02, "T", ACCENT_B, FS_TAG - 2, x=cx, w=0.60))
  gg, _p = self._mat(-2.30, 0.22, TT, ACCENT_C, dx=1.10)
  g.add(gg, self._sym(1.02, "T * T", ACCENT_C, FS_TAG - 2, x=-2.30, w=1.20))
  g.add(self._table(((f"     r ₁  =  {R1:.6f}       ‖ T φ ₁ ‖ ²  =  {nrm(mv(TG, W1)) ** 2:.6f}",
                      ACCENT_A),
                     (f"     r ₂  =  {R2:.6f}       ‖ T φ ₂ ‖ ²  =  {nrm(mv(TG, W2)) ** 2:.6f}",
                      WARN),
                     (f"     √ r ₁  =  {SG1:.4f}        √ r ₂  =  {SG2:.4f}", ACCENT_B),
                     (f"     max | ( S ² ) ᵢⱼ − ( T * T ) ᵢⱼ |  =  {dev(mm(SM, SM), TT):.1e}", DIM)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("每個特徵值都是一個長度平方，所以都是正的",
                  "each eigenvalue is a squared length, which is why none can vanish"))
  return g.add(self._foot("T * T 對任何 T 都自伴，因為 ( T * T ) * = T * T * * = T * T。取它的正交規範特徵基，r ᵢ = ( T * T φ ᵢ , φ ᵢ ) = ‖ T φ ᵢ ‖ ²",
                          "T star T is self-adjoint for every T, and against its orthonormal eigenbasis each eigenvalue equals the squared norm of T applied to that basis vector",
                          ACCENT_A,
                          f"T 可逆時那個長度不是零，所以 r ᵢ 嚴格大於零，正的平方根 S 就定義得出來。左圖的兩支箭頭是橢圓的兩個半軸 {SG1:.4f} 與 {SG2:.4f}",
                          f"with T invertible that length is nonzero, so the positive square root exists, and the two arrows are the ellipse's semi-axes"))

 def _chain(self):
  cy, s = -0.16, 0.40
  g = VGroup()
  for cx, M, col, lab in ((-5.45, IDM, DIM, "‖ ξ ‖  =  1"),
                          (-3.60, inv2(TG), WARN, "T ⁻ ¹"),
                          (-1.75, AM, ACCENT_B, "S T ⁻ ¹")):
   g.add(self._cross(cx, cy, w=0.80, h=0.62))
   g.add(self._image(cx, cy, s, IDM, DIM, sw=1.2))
   if col is not DIM:
    g.add(self._image(cx, cy, s, M, col, sw=2.4))
   g.add(self._sym(0.92, lab, ACCENT_A if col is DIM else col, FS_TAG - 2, x=cx, w=1.60))
  for cx in (-4.52, -2.67):
   g.add(self._arr([cx - 0.22, cy, 0], [cx + 0.22, cy, 0], DIM, sw=2.0, tl=0.11))
  g.add(self._table((("     ( S T ⁻ ¹ α , S T ⁻ ¹ β )", ACCENT_B),
                     (f"     =  ( T ⁻ ¹ α , S ² T ⁻ ¹ β )     =   {CHAIN[1]:.4f}", ACCENT_B),
                     (f"     =  ( T ⁻ ¹ α , T * β )          =   {CHAIN[2]:.4f}", ACCENT_C),
                     (f"     =  ( α , β )                   =   {CHAIN[3]:.4f}", ACCENT_A),
                     (f"     max | ( A * A ) ᵢⱼ − δ ᵢⱼ |  =  {dev(mm(tp(AM), AM), IDM):.1e}",
                      DIM)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("三個圓都是圓，中間那一步的變形被補回來了",
                  "the circle comes back a circle: the middle step is undone"))
  return g.add(self._foot("五個等號：S 搬過去變 S 平方，S 平方就是 T * T，T * 搬過去，T 與 T ⁻ ¹ 消掉，剩下 ( α , β )。所以 A = S T ⁻ ¹ 正交",
                          "five moves: S across becomes S squared, which is T star T, then T star across, then T cancels T inverse, and the product of alpha and beta is what is left",
                          ACCENT_A,
                          "圖上左邊是單位圓，中間是 T ⁻ ¹ 把它拉成的橢圓，右邊是再作用 S 之後——又回到圓，這就是正交",
                          "on the left the unit circle, in the middle the ellipse T inverse stretches it into, and on the right what S does to that: a circle again, which is orthogonality"))

 def _polar(self):
  cy, s = -0.16, 0.40
  g = VGroup()
  for cx, M, col, lab in ((-5.45, IDM, DIM, "‖ ξ ‖  =  1"),
                          (-3.60, SM, ACCENT_C, "S"),
                          (-1.75, TG, ACCENT_B, "R  S   =   T")):
   g.add(self._cross(cx, cy, w=0.80, h=0.62))
   g.add(self._image(cx, cy, s, IDM, DIM, sw=1.2))
   if col is not DIM:
    g.add(self._image(cx, cy, s, M, col, sw=2.4))
   g.add(self._sym(0.92, lab, ACCENT_A if col is DIM else col, FS_TAG - 2, x=cx, w=1.90))
  for cx in (-4.52, -2.67):
   g.add(self._arr([cx - 0.22, cy, 0], [cx + 0.22, cy, 0], DIM, sw=2.0, tl=0.11))
  g.add(self._table((("     T    =    R  S", ACCENT_A),
                     (f"     max | ( R S ) ᵢⱼ − t ᵢⱼ |   =   {dev(mm(RM, SM), TG):.1e}", ACCENT_B),
                     (f"     R   :   {RANG:.4f} °        det R  =  {det2(RM):.1f}", ACCENT_C),
                     (f"     max | S ᵢⱼ − S ⱼᵢ |   =   {dev(SM, tp(SM)):.1e}", DIM),
                     (f"     max | ( T T * ) ᵢⱼ − ( T * T ) ᵢⱼ |  =  {dev(TTS, TT):.4f}", WARN)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap(f"S 先把圓撐成橢圓，R 再把它轉 {RANG:.2f} 度",
                  "S stretches the circle into the ellipse; R then turns it"))
  return g.add(self._foot("定理 4.3：有限維 Hilbert 空間上任何可逆的 T 都寫成 R S，R 正交、S 自伴而且正。R 就是上一拍那個 A 的反元素",
                          "theorem 4.3: any invertible T on a finite-dimensional Hilbert space is an orthogonal map times a positive self-adjoint one, and R is the inverse of the map from the last beat",
                          ACCENT_A,
                          "這個分解唯一；從 T T * 出發會得到另一個順序 T = S ′ R ′。最後一列顯示 T T * 與 T * T 真的不一樣，所以兩個順序的 S 也不同",
                          "the factorisation is unique, and starting from T T star gives the other order; the last row shows those two matrices really differ, so the two positive factors do too"))

 def _svd(self):
  cy, s = -0.16, 0.40
  g = VGroup()
  for cx, M, col, lab in ((-5.45, VM, ACCENT_C, "v"),
                          (-3.60, mm(DD, VM), WARN, "d  v"),
                          (-1.75, TG, ACCENT_B, "u  d  v   =   t")):
   g.add(self._cross(cx, cy, w=0.80, h=0.62))
   g.add(self._image(cx, cy, s, IDM, DIM, sw=1.2))
   g.add(self._image(cx, cy, s, M, col, sw=2.4))
   g.add(self._sym(0.92, lab, col, FS_TAG - 2, x=cx, w=1.90))
  for cx in (-4.52, -2.67):
   g.add(self._arr([cx - 0.22, cy, 0], [cx + 0.22, cy, 0], DIM, sw=2.0, tl=0.11))
  g.add(self._table((("     t    =    u  d  v", ACCENT_A),
                     (f"     d   =   diag ( {DD[0][0]:.4f} , {DD[1][1]:.4f} )", WARN),
                     (f"     max | ( u d v ) ᵢⱼ − t ᵢⱼ |   =   {dev(mm(mm(UM, DD), VM), TG):.1e}",
                      ACCENT_B),
                     (f"     max | ( u * u ) ᵢⱼ − δ ᵢⱼ |   =   {dev(mm(tp(UM), UM), IDM):.1e}",
                      ACCENT_C),
                     (f"     max | ( v * v ) ᵢⱼ − δ ᵢⱼ |   =   {dev(mm(tp(VM), VM), IDM):.1e}",
                      ACCENT_C)),
                    y0=0.86, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("中間那一步是唯一改變形狀的",
                  "the middle step is the only one that changes the shape"))
  return g.add(self._foot("推論：任何非奇異矩陣 t 都寫成 u d v，u 與 v 正交、d 對角。證明是把 t = r s 裡的對稱 s 用定理 4.2 寫成 b d b ⁻ ¹，再併括號",
                          "the corollary: any nonsingular matrix is an orthogonal times a diagonal times an orthogonal, proved by diagonalising the symmetric factor with theorem 4.2 and regrouping",
                          ACCENT_A,
                          f"對角線上那兩個數 {DD[0][0]:.4f} 與 {DD[1][1]:.4f} 就是 T * T 特徵值的平方根，也就是第八拍那個橢圓的兩個半軸長",
                          f"the two numbers on the diagonal are the square roots of the eigenvalues of T star T, which are the semi-axes of the ellipse from the eighth beat"))

 def stage(self):
  a, b, c = self._adjoint(), self._direct(), self._transpose()
  d, e, f_ = self._orthogonal(), self._injective(), self._columns()
  h, i, j = self._diagonalise(), self._positive(), self._chain()
  k, l = self._polar(), self._svd()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE72ZH, AdvCalcE72EN = make(AdvCalcE72Base, "72", prefix="AdvCalcE")
