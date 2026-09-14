"""advcalc E71 -- chapter 5, section 3 (book pp. 257-260): self-adjoint
transformations, the spectral theorem, and what is left of it for an arbitrary
transformation.

T is self-adjoint when it can be moved from one side of the scalar product to
the other.  Under the injection of V into its conjugate space that says T
becomes its own adjoint, and against an orthonormal basis it says the matrix is
symmetric (Lemma 3.1).  A self-adjoint T with (T xi, xi) never negative is
called nonnegative, and then (T xi, eta) is a semiscalar product, which is what
lets Schwarz run and give Lemma 3.2: the squared norm of T xi is at most the
norm of T times (T xi, xi).  So (T xi, xi) = 0 forces T xi = 0, and that single
implication is the whole of Theorem 3.1: the maximiser of (T xi, xi) on the unit
sphere is an eigenvector, its orthogonal complement is invariant, and the
induction produces an orthonormal basis of eigenvectors.  Grouping equal
eigenvalues gives the unique orthogonal decomposition of Theorem 3.2, and such a
basis turns every computation with T -- squares, inverses, polynomials -- into
arithmetic on the eigenvalues.  The section closes on what fails without
self-adjointness: the ninety degree rotation of the plane has no eigenvector at
all, since its characteristic polynomial has no real root, and Theorem 3.3
identifies the eigenvalues of any T as the roots of its minimal polynomial.

Exercises 3.1 to 3.14 run from 260 to 261, and section 4 (orthogonal
transformations) starts on 262.

Two matrices carry the episode.  In the plane, S = [[2, 0.8], [0.8, 1.2]] is
self-adjoint with eigenvalues 2.4944 and 0.7056, which is what the unit circle
beats compute with; N = [[2, 0.8], [-0.3, 1.2]] is the same matrix with one
entry moved and fails the definition by 1.166.  In three-space,
A = [[3, 1, 1], [1, 3, 1], [1, 1, 3]] has the repeated eigenvalue 2, so its
eigenvectors are not unique while its eigenspaces are -- the point of Theorem
3.2.  The degenerate semiscalar product is the projection on the diagonal, whose
null direction is an honest nonzero vector of length zero.
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


def dot(a, b):
 return sum(x * y for x, y in zip(a, b))


def nrm(v):
 return math.sqrt(dot(v, v))


def unit(th):
 return (math.cos(th), math.sin(th))


# ── beat 1: the definition, and one matrix that fails it ──────────────
S = [[2.0, 0.8], [0.8, 1.2]]
N = [[2.0, 0.8], [-0.3, 1.2]]
AL, BE = (1.0, 0.6), (0.4, 1.3)
SL, SR = dot(mv(S, AL), BE), dot(AL, mv(S, BE))
NL, NR = dot(mv(N, AL), BE), dot(AL, mv(N, BE))
assert abs(SL - SR) < 1e-12, "T can be moved across the product, which is the definition"
GAP = NR - NL
assert abs(GAP) > 1.1, "and the same matrix with one entry moved fails it outright"
assert abs((NL - NR) - (N[0][1] - N[1][0]) * (AL[1] * BE[0] - AL[0] * BE[1])) < 1e-12, \
    "the failure is exactly the antisymmetric part of the matrix, on that pair"

# ── beat 2: the same statement inside the conjugate space ─────────────
THB = dot(AL, BE)
TSTAR = dot(mv(S, AL), BE)
THTB = dot(AL, mv(S, BE))
assert abs(TSTAR - THTB) < 1e-12, "the two ways round the square give the same functional"

# ── beat 3: the matrix is symmetric only against an orthonormal basis ─
B1, B2 = (1.0, 0.0), (0.0, 2.0)


def coords(v):
 det = B1[0] * B2[1] - B1[1] * B2[0]
 return ((v[0] * B2[1] - v[1] * B2[0]) / det, (B1[0] * v[1] - B1[1] * v[0]) / det)


C1, C2 = coords(mv(S, B1)), coords(mv(S, B2))
SKEW = [[C1[0], C2[0]], [C1[1], C2[1]]]
assert S[0][1] == S[1][0], "against the standard basis the matrix is symmetric"
assert abs(SKEW[0][1] - SKEW[1][0]) > 1.0, \
    "against a basis that is merely independent the same transformation is not"
assert abs(dot(B1, B2)) < 1e-12 and abs(nrm(B2) - 2.0) < 1e-12, \
    "that basis is orthogonal but not normalised, which is already enough to break it"

# ── beats 4 and 5: nonnegative, and the semiscalar product ────────────
P = [[0.5, 0.5], [0.5, 0.5]]
W = (1.0, -1.0)
assert nrm(mv(P, W)) < 1e-15 and dot(mv(P, W), W) < 1e-15 < nrm(W), \
    "a nonzero vector of length zero: this is why the product is only semi"
DIAG = (1.0, 1.0)
PDIAG = dot(mv(P, DIAG), DIAG)
assert PDIAG > 1.9, "off that one direction the product is perfectly ordinary"

L1 = (3.2 + math.sqrt(3.2)) / 2
L2 = (3.2 - math.sqrt(3.2)) / 2
assert abs(L1 * L2 - (S[0][0] * S[1][1] - S[0][1] * S[1][0])) < 1e-12
assert abs(L1 + L2 - (S[0][0] + S[1][1])) < 1e-12
A1 = (S[0][1], L1 - S[0][0])
A1 = (A1[0] / nrm(A1), A1[1] / nrm(A1))
A2 = (-A1[1], A1[0])
assert nrm(tuple(mv(S, A1)[i] - L1 * A1[i] for i in range(2))) < 1e-12
assert nrm(tuple(mv(S, A2)[i] - L2 * A2[i] for i in range(2))) < 1e-12

LEM = []
for _xi in ((1.0, 0.0), (0.6, -0.9), A2, A1):
 LEM.append((_xi, nrm(mv(S, _xi)) ** 2, L1 * dot(mv(S, _xi), _xi)))
assert all(a <= b + 1e-12 for _x, a, b in LEM), "Lemma 3.2 on four vectors"
assert abs(LEM[-1][1] - LEM[-1][2]) < 1e-12, \
    "with equality exactly at the eigenvector whose eigenvalue is the norm"
assert LEM[1][2] - LEM[1][1] > 1.4, "and a wide margin at a direction that is not one"

# ── beat 6: the maximum on the unit circle ────────────────────────────
SAMP = []
for _n in (12, 360, 3600):
 _m = max(dot(mv(S, unit(TAU * k / _n)), unit(TAU * k / _n)) for k in range(_n))
 SAMP.append((_n, _m, L1 - _m))
assert all(g > 0 for _n, _m, g in SAMP), "every sample is below the supremum"
assert SAMP[0][2] > 30 * SAMP[1][2] > 30 * SAMP[2][2], \
    "and the gap closes as the sampling refines, which is what compactness promises"

# ── beat 7: the maximiser is an eigenvector ───────────────────────────
NQ = 3600
QV = [dot(tuple(L1 * unit(TAU * k / NQ)[i] - mv(S, unit(TAU * k / NQ))[i] for i in range(2)),
          unit(TAU * k / NQ)) for k in range(NQ)]
QMIN, QMAX = min(QV), max(QV)
QA1 = dot(tuple(L1 * A1[i] - mv(S, A1)[i] for i in range(2)), A1)
RES = nrm(tuple(mv(S, A1)[i] - L1 * A1[i] for i in range(2)))
assert QMIN > -1e-12, "m minus T is nonnegative, since m was the largest value"
assert abs(QA1) < 1e-14 < QMAX, "it reaches zero at the maximiser and nowhere else"
assert RES < 1e-12, "so Lemma 3.2 turns that zero into T alpha equals m alpha"

# ── beats 8 and 9: three-space, with a repeated eigenvalue ────────────
A = [[3.0, 1.0, 1.0], [1.0, 3.0, 1.0], [1.0, 1.0, 3.0]]
E1 = tuple(1 / math.sqrt(3) for _ in range(3))
U = (1 / math.sqrt(2), -1 / math.sqrt(2), 0.0)
V3 = (1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6))
assert nrm(tuple(mv(A, E1)[i] - 5.0 * E1[i] for i in range(3))) < 1e-12
for _v in (U, V3):
 assert nrm(tuple(mv(A, _v)[i] - 2.0 * _v[i] for i in range(3))) < 1e-12
assert max(abs(dot(E1, U)), abs(dot(E1, V3)), abs(dot(U, V3))) < 1e-12

BEV = (5.0, 3.0, 1.0)
B3 = [[sum(BEV[k] * (E1, U, V3)[k][i] * (E1, U, V3)[k][j] for k in range(3))
       for j in range(3)] for i in range(3)]
for _v, _l in ((E1, 5.0), (U, 3.0), (V3, 1.0)):
 assert nrm(tuple(mv(B3, _v)[i] - _l * _v[i] for i in range(3))) < 1e-12, \
     "built from its own spectrum, so the three eigenvalues are exactly 5, 3 and 1"
assert max(abs(B3[i][j] - B3[j][i]) for i in range(3) for j in range(3)) < 1e-12, \
    "and it is symmetric, so it is self-adjoint"
BXI = (0.35, 0.50)
BIM = (3.0 * BXI[0], 1.0 * BXI[1])
assert abs(BIM[0] / BXI[0] - BIM[1] / BXI[1]) > 1.9, \
    "inside the complement the image points a different way, which is the honest picture"

XI3 = (0.4, -0.9, 0.5)
XP = tuple(XI3[i] - dot(XI3, E1) * E1[i] for i in range(3))
PERP_IN = dot(XP, E1)
PERP_OUT = dot(mv(B3, XP), E1)
assert abs(PERP_IN) < 1e-12 and abs(PERP_OUT) < 1e-12, \
    "the complement of an eigenvector is carried into itself, which is the induction step"

ROT = 0.7
U2 = tuple(math.cos(ROT) * U[i] + math.sin(ROT) * V3[i] for i in range(3))
V2 = tuple(-math.sin(ROT) * U[i] + math.cos(ROT) * V3[i] for i in range(3))
for _v in (U2, V2):
 assert nrm(tuple(mv(A, _v)[i] - 2.0 * _v[i] for i in range(3))) < 1e-12, \
     "a turned pair inside the eigenspace is just as good an orthonormal basis"
assert abs(dot(U2, V2)) < 1e-12 and abs(nrm(U2) - 1.0) < 1e-12
assert abs(dot(U, U2) - math.cos(ROT)) < 1e-12, "and it really is a different pair"

# ── beat 10: an eigenbasis turns everything into arithmetic ───────────
A2M = mm(A, A)
IDM = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
PA = [[A2M[i][j] - 3.0 * A[i][j] + IDM[i][j] for j in range(3)] for i in range(3)]


def pol(t):
 return t * t - 3.0 * t + 1.0


SPEC = [(5.0, 25.0, 1.0 / 5.0, pol(5.0)), (2.0, 4.0, 1.0 / 2.0, pol(2.0))]
assert nrm(tuple(mv(A2M, E1)[i] - 25.0 * E1[i] for i in range(3))) < 1e-9
assert nrm(tuple(mv(PA, E1)[i] - pol(5.0) * E1[i] for i in range(3))) < 1e-9
assert nrm(tuple(mv(PA, U)[i] - pol(2.0) * U[i] for i in range(3))) < 1e-12, \
    "a polynomial in T acts on an eigenvector as that polynomial at its eigenvalue"
PRES = max(nrm(tuple(mv(PA, _v)[i] - pol(_l) * _v[i] for i in range(3)))
           for _v, _l in ((E1, 5.0), (U, 2.0), (V3, 2.0)))
assert PRES < 1e-9

# ── beat 11: the rotation, which has no eigenvector at all ────────────
R = [[0.0, -1.0], [1.0, 0.0]]
NR_ = 1440
RRES = [nrm(tuple(mv(R, unit(TAU * k / NR_))[i]
                  - dot(mv(R, unit(TAU * k / NR_)), unit(TAU * k / NR_)) * unit(TAU * k / NR_)[i]
                  for i in range(2))) for k in range(NR_)]
RMIN = min(RRES)
assert RMIN > 0.999, \
    "no direction is anywhere near being turned into a multiple of itself"
RQ = max(abs(dot(mv(R, unit(TAU * k / NR_)), unit(TAU * k / NR_))) for k in range(NR_))
assert RQ < 1e-15, "the image is perpendicular to the vector, at every single direction"
DISC = 0.0 * 0.0 - 4.0 * 1.0
assert DISC < 0, "the characteristic polynomial has no real root"
ZR = (complex(1, 0), complex(0, -1))
RZ = (-ZR[1], ZR[0])
assert all(abs(RZ[i] - 1j * ZR[i]) < 1e-15 for i in range(2)), \
    "over the complex plane the same matrix does have an eigenvector"


class AdvCalcE71Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 71

 MODE_LABEL = {
  0: {"zh": "自伴的定義", "en": "what self-adjoint means"},
  1: {"zh": "在共軛空間裡的同一句話", "en": "the same sentence inside the dual"},
  2: {"zh": "引理 3.1：矩陣對稱", "en": "lemma 3.1: a symmetric matrix"},
  3: {"zh": "非負與半純量積", "en": "nonnegative, and a semiscalar product"},
  4: {"zh": "引理 3.2", "en": "lemma 3.2"},
  5: {"zh": "特徵值：單位球面上的最大值", "en": "eigenvalues: a maximum on the sphere"},
  6: {"zh": "定理 3.1 的關鍵一步", "en": "the step theorem 3.1 turns on"},
  7: {"zh": "歸納：正交補不變", "en": "the induction: the complement is invariant"},
  8: {"zh": "定理 3.2：分解唯一", "en": "theorem 3.2: the decomposition is unique"},
  9: {"zh": "特徵基底把計算變成算術", "en": "an eigenbasis turns it into arithmetic"},
  10: {"zh": "沒有自伴就可能一個都沒有", "en": "without it there may be none at all"},
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

 def _vec(self, cx, cy, s, v, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=sw, tl=tl)

 def _lab(self, cx, cy, s, v, txt, col, dx=0.24, dy=0.24, w=0.90):
  return self._sym(cy + s * v[1] + dy, txt, col, FS_TAG - 1, x=cx + s * v[0] + dx, w=w)

 def _pt(self, cx, cy, s, v, col, r=0.065):
  return Dot([cx + s * v[0], cy + s * v[1], 0], radius=r, color=col)

 def _cross(self, cx, cy, w=1.25, h=1.05):
  return VGroup(Line([cx - w, cy, 0], [cx + w, cy, 0], color=DIM, stroke_width=1.1),
                Line([cx, cy - h, 0], [cx, cy + h, 0], color=DIM, stroke_width=1.1))

 def _ring(self, cx, cy, s, col, n=96, sw=2.0, r=None):
  rr = r or (lambda th: 1.0)
  return self._curve([[cx + s * rr(TAU * k / n) * math.cos(TAU * k / n),
                       cy + s * rr(TAU * k / n) * math.sin(TAU * k / n), 0]
                      for k in range(n + 1)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _definition(self):
  cx, cy, s = -4.30, -0.42, 0.62
  g = VGroup(self._cross(cx, cy, w=1.10, h=0.55))
  g.add(self._vec(cx, cy, s, AL, ACCENT_B), self._vec(cx, cy, s, BE, ACCENT_C))
  g.add(self._vec(cx, cy, s, mv(S, AL), ACCENT_B, sw=1.8),
        self._vec(cx, cy, s, mv(S, BE), ACCENT_C, sw=1.8))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_B, dx=0.06, dy=-0.26),
        self._lab(cx, cy, s, BE, "β", ACCENT_C, dx=-0.26, dy=0.20),
        self._lab(cx, cy, s, mv(S, AL), "T α", ACCENT_B, dx=0.30, dy=-0.06, w=1.10),
        self._lab(cx, cy, s, mv(S, BE), "T β", ACCENT_C, dx=0.34, dy=0.16, w=1.10))
  g.add(self._table(((f"     ( T α , β )    =    {SL:.4f}", ACCENT_B),
                     (f"     ( α , T β )    =    {SR:.4f}", ACCENT_B),
                     (f"     ( N α , β )    =    {NL:.4f}", WARN),
                     (f"     ( α , N β )    =    {NR:.4f}", WARN),
                     (f"     ( α , N β )  −  ( N α , β )   =   {GAP:.4f}", DIM))))
  g.add(self._cap("上面兩列一模一樣，下面兩列差了那麼多",
                  "the upper two agree to the last digit, the lower two are far apart"))
  return g.add(self._foot("T 自伴的意思是它可以在內積裡從左邊搬到右邊。左圖是 S，把 α 與 β 各送到細箭頭那裡",
                          "self-adjoint means T can be moved from one side of the product to the other; the figure shows what it does to the two vectors",
                          ACCENT_A,
                          "下面兩列用的是同一個矩陣，只把左下角那一項從 0.8 換成 − 0.3。定義立刻失效——自伴是很強的條件",
                          "the lower two rows use the same matrix with one entry changed from 0.8 to minus 0.3, and the definition fails at once"))

 def _adjoint(self):
  x0, x1, y0, y1 = -5.10, -2.40, 0.62, -0.44
  g = VGroup()
  g.add(self._box(x0, y0, "V", ACCENT_B, w=0.80, h=0.52),
        self._box(x1, y0, "V", ACCENT_B, w=0.80, h=0.52),
        self._box(x0, y1, "V *", ACCENT_C, w=0.90, h=0.52),
        self._box(x1, y1, "V *", ACCENT_C, w=0.90, h=0.52))
  g.add(self._arr([x0 + 0.46, y0, 0], [x1 - 0.46, y0, 0], INK, sw=2.4, tl=0.14),
        self._arr([x1 - 0.52, y1, 0], [x0 + 0.52, y1, 0], INK, sw=2.4, tl=0.14),
        self._arr([x0, y0 - 0.30, 0], [x0, y1 + 0.30, 0], ACCENT_A, sw=2.4, tl=0.14),
        self._arr([x1, y0 - 0.30, 0], [x1, y1 + 0.30, 0], ACCENT_A, sw=2.4, tl=0.14))
  g.add(self._sym(y0 + 0.26, "T", INK, FS_TAG, x=(x0 + x1) / 2, w=0.50),
        self._sym(y1 - 0.34, "T *", INK, FS_TAG, x=(x0 + x1) / 2, w=0.70),
        self._sym((y0 + y1) / 2, "θ", ACCENT_A, FS_TAG, x=x0 - 0.34, w=0.50),
        self._sym((y0 + y1) / 2, "θ", ACCENT_A, FS_TAG, x=x1 + 0.34, w=0.50))
  g.add(self._table(((f"     θ ᵦ ( α )   =   ( α , β )   =   {THB:.4f}", ACCENT_C),
                     (f"     ( T * θ ᵦ ) ( α )   =   {TSTAR:.4f}", ACCENT_B),
                     (f"     θ ( T β ) ( α )   =   {THTB:.4f}", ACCENT_B),
                     ("     T * ∘ θ    =    θ ∘ T", ACCENT_A))))
  g.add(self._cap("兩條路徑落在同一個泛函上",
                  "the two ways round the square land on the same functional"))
  return g.add(self._foot("θ 是上一集那個嵌入：θ 把 β 送成「跟 β 取內積」。自伴就是說 T 在這個嵌入底下變成自己的伴隨",
                          "theta is last episode's injection, sending a vector to the functional that takes the product with it, and self-adjointness says T becomes its own adjoint under it",
                          ACCENT_A,
                          "先走 T 再配對、跟先配對再拉回，兩條路徑相等，正是 (T α , β) = (α , T β) 改寫成泛函的樣子",
                          "applying T then pairing, against pairing then pulling back, is the definition rewritten one level up"))

 def _symmetric(self):
  g = VGroup()
  ga, _p = self._numgrid(-5.00, 0.28, [[f"{S[i][j]:.1f}" for j in range(2)] for i in range(2)],
                         dx=0.66, dy=0.46, size=FS_TAG - 2, color=ACCENT_B,
                         hot=((0, 1), (1, 0)), hotcolor=ACCENT_A)
  gb, _q = self._numgrid(-2.60, 0.28, [[f"{SKEW[i][j]:.1f}" for j in range(2)] for i in range(2)],
                         dx=0.66, dy=0.46, size=FS_TAG - 2, color=ACCENT_C,
                         hot=((0, 1), (1, 0)), hotcolor=WARN)
  g.add(ga, gb)
  g.add(self._sym(1.00, "( φ ᵢ , φ ⱼ )  =  δ ᵢⱼ", ACCENT_B, FS_TAG - 2, x=-5.00, w=2.20),
        self._sym(1.00, "‖ b ₂ ‖  =  2", ACCENT_C, FS_TAG - 2, x=-2.60, w=2.20),
        self._sym(-0.42, f"{S[0][1]:.1f}  =  {S[1][0]:.1f}", ACCENT_A, FS_TAG - 2,
                  x=-5.00, w=1.60),
        self._sym(-0.42, f"{SKEW[0][1]:.1f}  ≠  {SKEW[1][0]:.1f}", WARN, FS_TAG - 2,
                  x=-2.60, w=1.60))
  g.add(self._table((("     T b ₁   =   " + f"{C1[0]:.1f} b ₁  +  {C1[1]:.1f} b ₂", ACCENT_C),
                     ("     T b ₂   =   " + f"{C2[0]:.1f} b ₁  +  {C2[1]:.1f} b ₂", ACCENT_C),
                     ("     b ₁  =  ⟨ 1 , 0 ⟩       b ₂  =  ⟨ 0 , 2 ⟩", DIM),
                     ("     ( b ₁ , b ₂ )   =   0", DIM)),
                    y0=0.80, dy=0.36))
  g.add(self._cap("同一個 T，右邊那組基底只是正交、沒有正規化",
                  "the same T; the basis on the right is orthogonal but not normalised"))
  return g.add(self._foot("引理 3.1：對正交規範基而言，T 自伴等價於矩陣對稱。證明是把展開式代進去，條件就變成 t ᵢⱼ 等於 t ⱼᵢ",
                          "lemma 3.1: against an orthonormal basis, self-adjoint is the same as a symmetric matrix, since substituting the expansions turns the condition into that equality of entries",
                          ACCENT_A,
                          "右邊是同一個自伴的 T，只把第二個基向量拉長成兩倍——正規化那半個條件掉了，矩陣就不對稱了",
                          "on the right the same self-adjoint T is written against a basis whose second vector is twice as long, and the symmetry is gone"))

 def _nonnegative(self):
  cx, cy, s = -4.90, -0.14, 0.80
  HW, HH = 1.15, 0.95
  g = VGroup(self._cross(cx, cy, w=HW, h=HH))
  g.add(self._ring(cx, cy, s, ACCENT_B,
                   r=lambda th: 1.0 / math.sqrt(dot(mv(S, unit(th)), unit(th)))))
  dx2 = -1.85
  g.add(self._cross(dx2, cy, w=HW, h=HH))
  for sgn in (1.0, -1.0):
   c = sgn * math.sqrt(2.0) * s * 0.52
   lo = max(-HW, c - HH)
   hi = min(HW, c + HH)
   g.add(self._curve([[dx2 + lo, cy + c - lo, 0], [dx2 + hi, cy + c - hi, 0]],
                     ACCENT_C, sw=2.2))
  g.add(self._vec(dx2, cy, s * 0.52, W, WARN, sw=2.8))
  g.add(self._sym(cy - s * 0.52 - 0.02, "w", WARN, FS_TAG - 1,
                  x=dx2 + s * 0.52 + 0.22, w=0.60))
  g.add(self._sym(1.14, "( S ξ , ξ )  =  1", ACCENT_B, FS_TAG - 2, x=cx, w=2.10),
        self._sym(1.14, "( P ξ , ξ )  =  1", ACCENT_C, FS_TAG - 2, x=dx2, w=2.10))
  g.add(self._table((("     [ ξ , η ]    =    ( T ξ , η )", ACCENT_A),
                     (f"     ( P w , w )   =   {dot(mv(P, W), W):.4f}      ‖ w ‖  =  {nrm(W):.4f}",
                      WARN),
                     (f"     ‖ P w ‖   =   {nrm(mv(P, W)):.4f}", WARN),
                     (f"     ( P ξ , ξ )   =   {PDIAG:.4f}       ξ  =  ⟨ 1 , 1 ⟩", ACCENT_C)),
                    y0=0.82, dy=0.34))
  g.add(self._cap("右邊那條 w 不是零，可是它的長度是零",
                  "the vector on the right is not zero, yet its length is"))
  return g.add(self._foot("T 自伴且 ( T ξ , ξ ) 恆非負時叫非負。這時 [ ξ , η ] = ( T ξ , η ) 是半純量積：對稱來自自伴，非負來自這個條件",
                          "a self-adjoint T is nonnegative when that number is never negative, and then the bracket is a semiscalar product: symmetric because T is self-adjoint",
                          ACCENT_A,
                          "「半」的意思是可能退化。左邊 S 給出的是一個橢圓，右邊那個投影給出兩條平行線，中間整條方向長度都是零",
                          "semi means it may degenerate: on the left the level set is an ellipse, on the right the projection gives two parallel lines and a whole null direction"))

 def _lemma32(self):
  ox, oy = -5.85, -0.62
  g = VGroup(Line([ox - 0.12, oy, 0], [ox + 3.40, oy, 0], color=DIM, stroke_width=1.3))
  sy = 0.235
  for k, (_xi, a, b) in enumerate(LEM):
   x = ox + 0.42 + k * 0.82
   g.add(Line([x - 0.13, oy, 0], [x - 0.13, oy + sy * a, 0], color=ACCENT_B, stroke_width=7.0),
         Line([x + 0.13, oy, 0], [x + 0.13, oy + sy * b, 0], color=ACCENT_C, stroke_width=7.0))
  for x0, col, lab, lw in ((-5.80, ACCENT_B, "‖ T ξ ‖ ²", 1.00),
                           (-4.40, ACCENT_C, "‖ T ‖ ( T ξ , ξ )", 1.80)):
   g.add(Line([x0, 1.06, 0], [x0 + 0.22, 1.06, 0], color=col, stroke_width=6.0),
         self._sym(1.06, lab, col, FS_TAG - 2, x=x0 + 0.32 + lw / 2, w=lw))
  g.add(self._table((("       ξ            ‖ T ξ ‖ ²        ‖ T ‖ ( T ξ , ξ )", DIM),
                     (f"     ⟨ 1 , 0 ⟩       {LEM[0][1]:.4f}        {LEM[0][2]:.4f}", ACCENT_B),
                     (f"     ⟨ 0.6 , − 0.9 ⟩   {LEM[1][1]:.4f}        {LEM[1][2]:.4f}", ACCENT_B),
                     (f"     α ₂            {LEM[2][1]:.4f}        {LEM[2][2]:.4f}", ACCENT_B),
                     (f"     α ₁            {LEM[3][1]:.4f}        {LEM[3][2]:.4f}", ACCENT_A)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("最後一列兩邊一樣，等號真的會發生",
                  "the last row has the two sides equal: the bound is attained"))
  return g.add(self._foot("引理 3.2：把 Schwarz 用在剛才那個半純量積上，取 η = T ξ，就得到 ‖ T ξ ‖ ² ≤ ‖ T ‖ ( T ξ , ξ )",
                          "lemma 3.2 applies Schwarz to that semiscalar product with eta taken to be T xi, which gives the bound in the formula bar",
                          ACCENT_A,
                          "真正要用的是它的推論：( T ξ , ξ ) 一等於零，右邊就是零，左邊被夾死，T ξ 只好是零",
                          "what gets used is the consequence: if that number is zero the right side is zero, so T xi is squeezed to zero as well"))

 def _eigen(self):
  ox, oy, sx, sy = -5.80, -0.74, 3.26 / TAU, 1.46 / L1
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + 3.32, oy, 0], color=DIM, stroke_width=1.3),
             Line([ox, oy - 0.10, 0], [ox, oy + 1.66, 0], color=DIM, stroke_width=1.3))
  for lev, col, lab in ((L1, ACCENT_A, "λ ₁"), (L2, DIM, "λ ₂")):
   g.add(self._dash([ox, oy + sy * lev, 0], [ox + 3.26, oy + sy * lev, 0], col, n=22, sw=1.2),
         self._sym(oy + sy * lev + 0.22, lab, col, FS_TAG - 2, x=ox + 3.02, w=0.70))
  g.add(self._curve([[ox + sx * TAU * k / 240,
                      oy + sy * dot(mv(S, unit(TAU * k / 240)), unit(TAU * k / 240)), 0]
                     for k in range(241)], ACCENT_B, sw=2.4))
  TH1 = math.atan2(A1[1], A1[0])
  for th in (TH1, TH1 + math.pi):
   g.add(Dot([ox + sx * th, oy + sy * L1, 0], radius=0.065, color=ACCENT_A))
  g.add(self._sym(oy + sy * L1 + 0.24, "α ₁", ACCENT_A, FS_TAG - 2, x=ox + sx * TH1, w=0.70))
  g.add(self._sym(oy - 0.26, "0", DIM, FS_TAG - 2, x=ox, w=0.40),
        self._sym(oy - 0.26, "2 π", DIM, FS_TAG - 2, x=ox + 3.26, w=0.70))
  g.add(self._table((("       N              m ( N )          λ ₁  −  m", DIM),)
                    + tuple((f"     {n:5d}         {m:.7f}       {gp:.2e}", ACCENT_B)
                            for n, m, gp in SAMP)
                    + ((f"     λ ₁             {L1:.7f}       0", ACCENT_A),
                       (f"     λ ₂             {L2:.7f}", DIM)),
                    y0=0.88, dy=0.30, size=FS_TAG - 3))
  g.add(self._cap("取樣愈密，最大值就愈貼近 λ ₁",
                  "the finer the sampling, the closer the maximum sits to the top eigenvalue"))
  return g.add(self._foot("α 是特徵向量的意思是 α 不是零、而 T α 是 α 的倍數。球面有界又閉所以緊緻，連續函數一定取到上確界——這是定理 3.1 在分析上唯一的投入",
                          "alpha is an eigenvector when it is nonzero and T alpha is a multiple of it; the sphere is bounded and closed, so a continuous function attains its supremum, which is all the analysis needed",
                          ACCENT_A,
                          "左圖是 ( T ξ , ξ ) 隨方向轉一圈的變化，兩條虛線是 λ ₁ 與 λ ₂ 那兩個高度——它碰到上面那條，只在 ± α ₁ 兩個方向",
                          "the graph on the left is that number as the direction turns once round, between the two dashed eigenvalue levels, and it reaches the upper one in two directions only"))

 def _keystep(self):
  cx, cy, s = -4.40, 0.05, 0.62
  g = VGroup(self._cross(cx, cy, w=1.34, h=1.02))
  g.add(self._ring(cx, cy, s, DIM, sw=1.5))
  for k in range(0, NQ, NQ // 60):
   u = unit(TAU * k / NQ)
   rr = s + 0.44 * QV[k] / QMAX
   g.add(Line([cx + s * u[0], cy + s * u[1], 0], [cx + rr * u[0], cy + rr * u[1], 0],
              color=ACCENT_B, stroke_width=2.2))
  for v in (A1, (-A1[0], -A1[1])):
   g.add(self._pt(cx, cy, s, v, ACCENT_A, r=0.075))
  g.add(self._lab(cx, cy, s, A1, "α ₁", ACCENT_A, dx=0.40, dy=0.34))
  g.add(self._table(((f"     ( ( m − T ) α ₁ , α ₁ )   =   {QA1:.1e}", ACCENT_A),
                     (f"     ‖ T α ₁  −  m α ₁ ‖   =   {RES:.1e}", ACCENT_A),
                     (f"     min ( ( m − T ) ξ , ξ )   =   {QMIN:.1e}", ACCENT_B),
                     (f"     max ( ( m − T ) ξ , ξ )   =   {QMAX:.4f}", WARN),
                     (f"     m   =   λ ₁   =   {L1:.6f}", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("刺只在 ± α ₁ 那兩個點上縮成零",
                  "the spikes shrink to nothing at those two points only"))
  return g.add(self._foot("m 減 T 是非負的自伴變換，而「( T α , α ) 等於 m」寫出來就是「( ( m − T ) α , α ) 等於零」",
                          "m minus T is nonnegative and self-adjoint, and saying the maximum is attained at alpha is saying that number is zero there",
                          ACCENT_A,
                          "圖上每根刺的長度就是那個數：處處非負，而且只在 α ₁ 的方向歸零。引理 3.2 於是把那個零變成 ( m − T ) α = 0",
                          "each spike is that number at one direction: never negative, and zero only along the maximiser, where lemma 3.2 turns it into the vector equation"))

 def _induction(self):
  cx, cy, s = -4.30, -0.30, 0.68
  P1, P2 = (1.00, 0.18), (0.30, 0.50)

  def q(a_, b_):
   return [cx + s * (a_ * P1[0] + b_ * P2[0]), cy + s * (a_ * P1[1] + b_ * P2[1]), 0]

  g = VGroup(self._curve([q(2.1, 1.2), q(2.1, -1.2), q(-2.1, -1.2), q(-2.1, 1.2),
                          q(2.1, 1.2)], ACCENT_B, sw=1.8))
  g.add(self._arr([cx, cy, 0], [cx, cy + 0.82, 0], ACCENT_A, sw=2.8, tl=0.15))
  g.add(self._sym(cy + 1.02, "α ₁", ACCENT_A, FS_TAG - 1, x=cx + 0.24, w=0.70),
        self._sym(cy + s * (-2.1 * P1[1] + 1.2 * P2[1]) + 0.26, "V ₂", ACCENT_B, FS_TAG - 1,
                  x=cx + s * (-2.1 * P1[0] + 1.2 * P2[0]) + 0.24, w=0.80))
  g.add(self._arr([cx, cy, 0], q(*BIM), ACCENT_C, sw=2.0, tl=0.13))
  g.add(self._arr([cx, cy, 0], q(*BXI), WARN, sw=2.8, tl=0.13))
  g.add(self._sym(q(*BXI)[1] + 0.32, "ξ", WARN, FS_TAG - 1, x=q(*BXI)[0] + 0.06, w=0.50),
        self._sym(q(*BIM)[1] - 0.26, "T ξ", ACCENT_C, FS_TAG - 1, x=q(*BIM)[0] + 0.16, w=0.80))
  g.add(self._table(((f"     ( ξ , α ₁ )    =    {PERP_IN:.1e}", WARN),
                     (f"     ( T ξ , α ₁ )    =    {PERP_OUT:.1e}", ACCENT_C),
                     ("     ( T ξ , α ₁ )  =  ( ξ , T α ₁ )  =  m ( ξ , α ₁ )", ACCENT_A),
                     ("     α ₁  =  ⟨ 1 , 1 , 1 ⟩ / √ 3        T α ₁  =  5 α ₁", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("ξ 與 T ξ 指的方向不同，可是都還在那個平面裡",
                  "the image points a different way, and it is still inside the plane"))
  return g.add(self._foot("那一行計算就是全部：把 T 搬過去，碰到 T α ₁ = m α ₁，剩下 m 乘一個已經是零的數",
                          "that one line is the whole argument: move T across, meet the eigenvalue equation, and what is left is m times a number already known to be zero",
                          ACCENT_A,
                          "所以 V ₂ 在 T 底下不變，在 V ₂ 上重做一次就得到 α ₂，維數每次掉一。這一拍畫的 T 特徵值是 5、3、1",
                          "so the complement is invariant, the same argument inside it produces the next eigenvector, and the dimension drops by one; the transformation drawn has eigenvalues five, three and one"))

 def _unique(self):
  cx, cy, s = -4.40, -0.20, 0.76
  g = VGroup(self._ring(cx, cy, s, DIM, sw=1.5))
  for ang, col, sw in ((0.0, ACCENT_B, 2.6), (ROT, WARN, 2.2)):
   for k in (0, 1):
    th = ang + k * math.pi / 2
    g.add(self._vec(cx, cy, s, unit(th), col, sw=sw))
  g.add(self._sym(cy - 0.02, "u", ACCENT_B, FS_TAG - 1, x=cx + s + 0.20, w=0.50),
        self._sym(cy + s + 0.22, "v", ACCENT_B, FS_TAG - 1, x=cx + 0.20, w=0.50),
        self._sym(cy + s * math.sin(ROT) + 0.24, "u ′", WARN, FS_TAG - 1,
                  x=cx + s * math.cos(ROT) + 0.24, w=0.70))
  g.add(self._sym(cy + s * 0.78, "M ₂", ACCENT_A, FS_TAG - 1, x=cx - s - 0.44, w=0.80))
  g.add(self._table(((f"     λ ₁  =  5         dim M ₁  =  1", ACCENT_A),
                     (f"     λ ₂  =  2         dim M ₂  =  2", ACCENT_B),
                     (f"     ‖ T u ′ − 2 u ′ ‖   =   "
                      f"{nrm(tuple(mv(A, U2)[i] - 2 * U2[i] for i in range(3))):.1e}", WARN),
                     (f"     ( u , u ′ )   =   {dot(U, U2):.4f}", WARN),
                     ("     V   =   M ₁  ⊕  M ₂", ACCENT_A)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("轉過的那一對還是特徵向量，還是正交規範",
                  "the turned pair are still eigenvectors, and still orthonormal"))
  return g.add(self._foot("把相同的特徵值歸成一組：M ⱼ 由特徵值等於 λ ⱼ 的基向量張成。引理 3.3 說每個特徵向量都落在某個 M ⱼ 裡",
                          "group the equal eigenvalues, so that each subspace is spanned by the basis vectors sharing an eigenvalue; lemma 3.3 puts every eigenvector inside one of them",
                          ACCENT_A,
                          "所以 M ⱼ 與 λ ⱼ 唯一，基向量本身不唯一。這一拍把上一拍的 3 與 1 併成重根 2，M ₂ 裡任何一組正交規範對都能用",
                          "so the subspaces and the scalars are unique while the basis vectors are not: this transformation repeats an eigenvalue, and any orthonormal pair inside that plane will do"))

 def _arithmetic(self):
  g = VGroup()
  gg, pos = self._numgrid(-4.15, 0.18,
                          [[f"{v:g}" for v in row] for row in
                           ([5, 25, 0.2, pol(5.0)], [2, 4, 0.5, pol(2.0)])],
                          dx=0.86, dy=0.50, size=FS_TAG - 1, color=ACCENT_B,
                          hotcol=0, hotcolor=ACCENT_A)
  g.add(gg)
  for j, lab in enumerate(("T", "T ²", "T ⁻ ¹", "P ( T )")):
   g.add(self._sym(0.78, lab, DIM, FS_TAG - 2, x=pos(0, j)[0], w=0.90))
  g.add(self._sym(-0.56, "P ( t )   =   t ²  −  3 t  +  1", ACCENT_C, FS_TAG - 2,
                  x=-4.15, w=3.20))
  g.add(self._table((("     T β ᵢ  =  r ᵢ β ᵢ         P ( T ) β ᵢ  =  P ( r ᵢ ) β ᵢ", ACCENT_A),
                     (f"     P ( 5 )   =   {pol(5.0):g}        P ( 2 )   =   {pol(2.0):g}", ACCENT_C),
                     (f"     ‖ P ( T ) β ᵢ  −  P ( r ᵢ ) β ᵢ ‖   ≤   {PRES:.1e}", ACCENT_B),
                     ("     x ᵢ   =   ( ξ , β ᵢ )", DIM)),
                    y0=0.84, dy=0.34))
  g.add(self._cap("每一欄都只是把左邊那一欄的數字代進去",
                  "every column is the first one with a function applied to it"))
  return g.add(self._foot("有了特徵向量組成的基，計算全部退化成算術：T 平方的特徵向量一樣、特徵值平方，反元素存在的充要條件是沒有特徵值等於零",
                          "with a basis of eigenvectors the computations collapse into arithmetic: squaring squares the eigenvalues, and the inverse exists exactly when none of them is zero",
                          ACCENT_A,
                          "多項式也一樣：P ( T ) 把 β ᵢ 送成 P ( r ᵢ ) 乘 β ᵢ。正規化再多給一件事——係數直接由內積讀出來",
                          "a polynomial is no different, and an orthonormal basis adds one more convenience: the coefficients of a vector are read off by scalar products"))

 def _rotation(self):
  cx, cy, s = -4.55, -0.14, 0.78
  g = VGroup(self._cross(cx, cy, w=1.28, h=0.95))
  g.add(self._ring(cx, cy, s, DIM, sw=1.4))
  for th, col in ((0.0, ACCENT_B), (1.05, ACCENT_C), (2.30, WARN)):
   v = unit(th)
   g.add(self._vec(cx, cy, s, v, col, sw=2.4),
         self._vec(cx, cy, s, mv(R, v), col, sw=1.4, tl=0.10))
  g.add(self._sym(cy + 0.26, "ξ", ACCENT_B, FS_TAG - 1, x=cx + s + 0.20, w=0.50),
        self._sym(cy + s + 0.24, "R ξ", ACCENT_B, FS_TAG - 1, x=cx + 0.52, w=0.80))
  g.add(self._table((("     λ ²  +  1   =   0            Δ   =   − 4", ACCENT_A),
                     (f"     max | ( R ξ , ξ ) |   =   {RQ:.1e}", ACCENT_B),
                     (f"     min ‖ R ξ − ( R ξ , ξ ) ξ ‖   =   {RMIN:.4f}", WARN),
                     ("     R ⟨ 1 , − i ⟩   =   i ⟨ 1 , − i ⟩", ACCENT_C),
                     ("     p ( t )  =  t ²  +  1", DIM)),
                    y0=0.84, dy=0.32))
  g.add(self._cap("每一個方向都被轉走九十度，一個都沒留下",
                  "every direction is turned through a right angle, so none survives"))
  return g.add(self._foot("這個 R 不自伴，而且連一個特徵向量都沒有：特徵多項式 λ ² + 1 在實數上不可約，判別式是 − 4",
                          "this rotation is not self-adjoint and has no eigenvector at all, since its characteristic polynomial has no real root",
                          ACCENT_A,
                          "換到複二維空間，同一個矩陣的特徵值就成了正負 i。定理 3.3 收尾：特徵值恰好是極小多項式的根",
                          "over complex two-space the same matrix does have eigenvalues, and theorem 3.3 closes the section by identifying them with the roots of the minimal polynomial"))

 def stage(self):
  a, b, c = self._definition(), self._adjoint(), self._symmetric()
  d, e, f_ = self._nonnegative(), self._lemma32(), self._eigen()
  h, i, j = self._keystep(), self._induction(), self._unique()
  k, l = self._arithmetic(), self._rotation()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE71ZH, AdvCalcE71EN = make(AdvCalcE71Base, "71", prefix="AdvCalcE")
