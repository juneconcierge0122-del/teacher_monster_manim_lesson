"""advcalc E88 -- chapter 7, section 6 (book pp. 312-315): the determinant.

The previous episode worked out that the space of alternating m-forms on an
m-dimensional space has dimension one.  This episode spends that one.  Up to a
scalar multiple there is only one alternating m-linear functional on R^m, so
fixing its value on the standard basis at 1 determines it outright, and the
functional so determined is the determinant.  Everything else in the section is
that single sentence being cashed in: the explicit sum over permutations,
invariance under transpose, the basis-free determinant of a transformation, its
multiplicativity, the equivalence with singularity, the reduction lemmas, the
expansion by minors, the cofactor matrix, and Cramer's rule.

The eleven beats follow the book's own order because each result is used by the
next one: Corollary 2 is Corollary 1 applied to Lemma 6.1, Theorem 6.2's three
corollaries all run through Theorem 6.1, and Theorem 6.3's own corollary is the
expansion theorem read on a matrix with two equal columns.  Two beats are spent
on the pair 6.2 and 6.3 because the reduction lemma is what makes the expansion
theorem a theorem rather than a definition.

Every number on screen is computed here, and every one of them is checked
against an implementation that shares no code with the one being shown.  The
displayed values come from `dexp`, the literal sum over the m! permutations with
`sgn` counting inversions; the checks come from numpy's LU-based
`numpy.linalg.det` and `numpy.linalg.solve`.  That is the point of the asserts
below: a sum over permutations agreeing with itself proves nothing, so the
expansion down column 1 is compared with the expansions down columns 2 and 3,
with the permutation sum, and with numpy, and Cramer's three quotients are
compared coordinate by coordinate with the linear solver.  Integer matrices are
used on screen so a viewer can check a row by hand; a seeded pair of random
matrices is carried alongside so the formula is also tested where cancellation
is not conveniently exact.
"""
import itertools
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Rectangle, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these


# ── the determinant, written out the way Lemma 6.1 writes it ──────────
def sgn(p):
 """The sign of a permutation, counted off its inversions."""
 s = 1
 for i in range(len(p)):
  for j in range(i + 1, len(p)):
   if p[i] > p[j]:
    s = -s
 return s


def dexp(M):
 """Lemma 6.1 literally: sum over S_m of sgn(sigma) times one entry per column.

 Nothing here is shared with numpy's factorisation, which is what makes the
 comparisons below a test rather than a tautology."""
 m = len(M)
 return float(sum(sgn(p) * math.prod(M[p[j]][j] for j in range(m))
                  for p in itertools.permutations(range(m))))


def minor(M, i, r):
 """The submatrix with row i and column r deleted -- the book's (t)^{ir}."""
 return [[M[a][b] for b in range(len(M)) if b != r] for a in range(len(M)) if a != i]


def ms(v, spec=".0f"):
 """A number as it should read on screen: a real minus sign, not a hyphen.

 Zero is normalised first, or an entry that came out of the arithmetic as
 negative zero would be printed with a minus sign in front of it."""
 if v == 0:
  v = 0.0
 return format(v, spec).replace("-", "−")


def mrow(M, spec=".0f"):
 return "[ " + " ;  ".join("  ".join(ms(v, spec) for v in row) for row in M) + " ]"


# ── beat 0: the normalisation that picks one form out of the line ─────
M_DIM = 3
DIM_ALT = math.comb(M_DIM, M_DIM)
IDENT = np.eye(M_DIM)
D_IDENT = dexp(IDENT.tolist())
assert DIM_ALT == 1, "the space of alternating m-forms on an m-dimensional space is a line"
assert abs(D_IDENT - 1.0) < 1e-12, \
    "and the determinant is the point of that line taking the value 1 on the standard basis"
CMULT = (-1.0, 0.5, 1.0, 2.0, 2.8)          # where the sample forms sit on the line

# ── beats 1, 2, 3, 10: one asymmetric 3 x 3 ───────────────────────────
T3 = np.array([[2.0, -1.0, 3.0], [1.0, 4.0, -2.0], [-1.0, 5.0, 1.0]])
D_T3 = dexp(T3.tolist())
assert abs(D_T3 - np.linalg.det(T3)) < 1e-12, \
    "the permutation sum and numpy's factorisation give the same determinant"
PERM3 = [(p, sgn(p), [T3[p[j]][j] for j in range(3)]) for p in itertools.permutations(range(3))]
TERM3 = [s * math.prod(f) for _p, s, f in PERM3]
assert abs(sum(TERM3) - D_T3) < 1e-12, "the six listed terms are the whole sum, nothing dropped"
SHOW3 = 4                                   # the permutation highlighted in the grid, (3 1 2)
assert PERM3[SHOW3][0] == (2, 0, 1), "the highlighted cells are the ones that row of the table uses"

# ── beat 2: transpose ─────────────────────────────────────────────────
D_T3T = dexp(T3.T.tolist())
assert abs(D_T3T - D_T3) < 1e-12, "Corollary 1: transposing does not change the determinant"
assert np.abs(T3 - T3.T).max() > 1.0, \
    "and the two grids on screen really are different matrices, so the equality says something"

# ── beat 3: alternating and multilinear in the rows ───────────────────
ROW_C, ROW_K = 2.5, 3.0
_SWAP = T3[[1, 0, 2]]
_SCALE = T3.astype(float).copy(); _SCALE[1] *= ROW_C
_SHEAR = T3.astype(float).copy(); _SHEAR[2] += ROW_K * _SHEAR[0]
ROWOPS = [("swap", _SWAP, -D_T3), ("scale", _SCALE, ROW_C * D_T3), ("shear", _SHEAR, D_T3)]
for _n, _M, _want in ROWOPS:
 assert abs(dexp(_M.tolist()) - _want) < 1e-12, \
     f"row operation {_n}: alternating multilinearity in the rows predicts the new determinant"
 assert abs(np.linalg.det(_M) - _want) < 1e-10, \
     f"row operation {_n}: and numpy agrees with that prediction too"
D_SWAP, D_SCALE, D_SHEAR = (dexp(M.tolist()) for _n, M, _w in ROWOPS)
ROWERR = max(abs(dexp(M.tolist()) - w) for _n, M, w in ROWOPS)

# ── beat 4: k_T does not depend on which form we start from ───────────
TD = np.array([[1.0, 1.0, 0.0], [0.0, 2.0, 1.0], [0.0, 0.0, 1.0]])
XI = np.array([[1.0, 0.0, 2.0], [2.0, 1.0, 0.0], [0.0, 3.0, 1.0]])
D_TD, D_XI = dexp(TD.tolist()), dexp(XI.tolist())
assert abs(D_XI) > 1e-9, "the test m-tuple is independent, so f does not vanish on it"
FORMC = (2.5, -0.8)
FVAL = [(c, c * D_XI, c * dexp((TD @ XI).tolist())) for c in FORMC]
for _c, _f, _ft in FVAL:
 assert abs(_ft / _f - D_TD) < 1e-12, \
     "f_T / f is the determinant of T whichever nonzero multiple of D we call f"
assert abs(FVAL[0][2] / FVAL[0][1] - FVAL[1][2] / FVAL[1][1]) < 1e-12, \
    "so the two sample forms yield the very same constant: k_T is independent of f"
KERR = max(abs(ft / f - np.linalg.det(TD)) for _c, f, ft in FVAL)

# ── beat 5: Theorem 6.1, multiplicativity ─────────────────────────────
S3 = np.array([[1.0, 2.0, 0.0], [0.0, 1.0, 3.0], [2.0, 0.0, 1.0]])
ST3 = S3 @ T3
D_S3, D_ST3 = dexp(S3.tolist()), dexp(ST3.tolist())
assert abs(D_ST3 - D_S3 * D_T3) < 1e-12, "Theorem 6.1: the composite's determinant is the product"
assert abs(D_ST3 - np.linalg.det(ST3)) < 1e-10, "and numpy's determinant of the product agrees"
MULERR = abs(D_ST3 - D_S3 * D_T3)

# ── beat 6: similarity, and singular if and only if zero ──────────────
THETA = np.array([[1.0, 1.0, 0.0], [0.0, 2.0, 1.0], [1.0, 0.0, 1.0]])
assert abs(dexp(THETA.tolist())) > 1e-9, "theta has to be an isomorphism for the conjugate to exist"
SIM = THETA @ T3 @ np.linalg.inv(THETA)
D_SIM = dexp(SIM.tolist())
assert abs(D_SIM - D_T3) < 1e-10, "Theorem 6.2: a similar transformation has the same determinant"
SING = np.array([[1.0, 2.0, -1.0], [3.0, 0.0, 2.0], [7.0, 2.0, 3.0]])
assert np.abs(SING[2] - (SING[0] + 2.0 * SING[1])).max() < 1e-12, \
    "the third row of this matrix really is the first plus twice the second"
D_SING = dexp(SING.tolist())
RANK_SING = int(np.linalg.matrix_rank(SING))
RANK_T3 = int(np.linalg.matrix_rank(T3))
assert abs(D_SING) < 1e-12 and RANK_SING == 2, \
    "Corollary 3 one way: a dependent row makes the determinant vanish, and the rank drop"
assert abs(D_T3) > 1.0 and RANK_T3 == 3, \
    "Corollary 3 the other way: full rank goes with a determinant that is not zero"

# ── beat 7: Lemma 6.2, the reduction ──────────────────────────────────
RED = np.array([[2.0, -1.0, 3.0, 0.0], [1.0, 4.0, -2.0, 0.0],
                [-1.0, 5.0, 1.0, 0.0], [5.0, -2.0, 3.0, 1.0]])
assert np.abs(RED[:, 3] - np.eye(4)[:, 3]).max() < 1e-12, "the last column is the vector delta^m"
SUB = RED[:3, :3]
D_RED, D_SUB = dexp(RED.tolist()), dexp(SUB.tolist())
assert abs(D_RED - D_SUB) < 1e-12, \
    "Lemma 6.2: deleting the last row and column leaves the determinant alone"
RED2 = RED.copy(); RED2[3, :3] = [-4.0, 6.0, -9.0]
D_RED2 = dexp(RED2.tolist())
assert abs(D_RED2 - D_RED) < 1e-12, \
    "and the rest of that last row cannot matter: D depends only on the deleted submatrix"
assert abs(D_RED - np.linalg.det(RED)) < 1e-10, "numpy agrees with both of those"

# ── beats 8 and 9: Theorem 6.3 on a 4 x 4 ─────────────────────────────
T4 = np.array([[2.0, 1.0, -1.0, 3.0], [0.0, 3.0, 2.0, -2.0],
               [1.0, -1.0, 4.0, 1.0], [3.0, 2.0, 0.0, -1.0]])
D_T4 = dexp(T4.tolist())
assert abs(D_T4 - np.linalg.det(T4)) < 1e-10, "the 4 x 4 permutation sum matches numpy as well"


def expand(M, r):
 """Theorem 6.3 down column r, as the list of its m signed terms."""
 return [(-1.0) ** (i + r) * M[i][r] * dexp(minor(M, i, r)) for i in range(len(M))]


COLS = [0, 1, 2]
EXPAND = {r: expand(T4.tolist(), r) for r in COLS}
for _r in COLS:
 assert abs(sum(EXPAND[_r]) - D_T4) < 1e-12, \
     f"expanding down column {_r + 1} reproduces the determinant, not just its own arithmetic"
assert max(abs(sum(EXPAND[a]) - sum(EXPAND[b])) for a in COLS for b in COLS) < 1e-12, \
    "and the three different columns agree with each other, which a sign slip would break"
EXERR = max(abs(sum(EXPAND[r]) - np.linalg.det(T4)) for r in COLS)
RSHOW = 1                                   # the column whose four terms are listed on screen
MINORS = [minor(T4.tolist(), i, RSHOW) for i in range(4)]
MDET = [dexp(m) for m in MINORS]
assert all(abs(d - np.linalg.det(np.array(m))) < 1e-10 for m, d in zip(MINORS, MDET)), \
    "each 3 x 3 minor drawn on screen carries the determinant the table credits it with"

# ── beat 9: Corollary 1, the cofactor matrix, and the inverse ─────────
OFFD = [(0, 1), (1, 2)]
CROSS = [(r, s, sum((-1.0) ** (i + r) * T4[i][s] * dexp(minor(T4.tolist(), i, r))
                    for i in range(4))) for r, s in OFFD]
for _r, _s, _v in CROSS:
 assert abs(_v) < 1e-12, \
     "Corollary 1: entries of one column against another column's minors sum to zero"
COF = np.array([[(-1.0) ** (i + j) * dexp(minor(T4.tolist(), i, j)) for j in range(4)]
                for i in range(4)])
COFT = COF.T @ T4
assert np.abs(COFT - D_T4 * np.eye(4)).max() < 1e-10, \
    "the two results together: the transposed cofactor matrix times t is D(t) on the diagonal"
COFERR = float(np.abs(COFT - D_T4 * np.eye(4)).max())
INVERR = float(np.abs(COF.T / D_T4 - np.linalg.inv(T4)).max())
assert INVERR < 1e-12, "so cofactors over D(t) really are the entries of the inverse matrix"

# ── beat 10: Cramer's rule against an independent solver ───────────────
XWANT = np.array([1.0, -1.0, 2.0])
YVEC = T3 @ XWANT
DJ = []
for _j in range(3):
 _M = T3.copy(); _M[:, _j] = YVEC
 DJ.append(dexp(_M.tolist()))
XCRAMER = [d / D_T3 for d in DJ]
XSOLVE = np.linalg.solve(T3, YVEC)
assert max(abs(a - b) for a, b in zip(XCRAMER, XSOLVE)) < 1e-12, \
    "Cramer's quotients agree coordinate by coordinate with a linear solver that never forms a minor"
assert max(abs(a - b) for a, b in zip(XCRAMER, XWANT)) < 1e-12, \
    "and both recover the vector the right-hand side was built from"
CRERR = max(abs(a - b) for a, b in zip(XCRAMER, XSOLVE))

# ── the formula where cancellation is not conveniently exact ──────────
_rng = np.random.default_rng(88)
RAND = []
for _m in (3, 4):
 _R = _rng.standard_normal((_m, _m))
 RAND.append((_m, abs(dexp(_R.tolist()) - np.linalg.det(_R)),
              abs(dexp(_R.T.tolist()) - np.linalg.det(_R))))
for _m, _e, _et in RAND:
 assert _e < 1e-12, f"the explicit {_m} x {_m} formula matches numpy on a matrix with no round numbers"
 assert _et < 1e-12, f"and so does its transpose, on the same {_m} x {_m} matrix"
RANDERR = max(max(e, et) for _m, e, et in RAND)


class AdvCalcE88Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 88

 MODE_LABEL = {
  0: {"zh": "唯一性：差一個純量只有一個", "en": "uniqueness: only one, up to a scalar"},
  1: {"zh": "引理 6.1：顯式公式", "en": "Lemma 6.1: the explicit formula"},
  2: {"zh": "推論 1：轉置不改變它", "en": "Corollary 1: the transpose has the same value"},
  3: {"zh": "推論 2：對橫列也是交錯的", "en": "Corollary 2: alternating in the rows as well"},
  4: {"zh": "Δ ( T )：不依賴任何基底", "en": "Delta of T: defined with no basis at all"},
  5: {"zh": "定理 6.1：合成變成相乘", "en": "Theorem 6.1: composition becomes multiplication"},
  6: {"zh": "定理 6.2 與三個推論", "en": "Theorem 6.2 and its three corollaries"},
  7: {"zh": "引理 6.2 與 6.3：降一階", "en": "Lemmas 6.2 and 6.3: dropping one dimension"},
  8: {"zh": "定理 6.3：餘因子展開", "en": "Theorem 6.3: the expansion by minors"},
  9: {"zh": "推論 1 與餘因子矩陣", "en": "Corollary 1 and the cofactor matrix"},
  10: {"zh": "Cramer 法則，第 6 節結束", "en": "Cramer's rule, and the end of section 6"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.90, dy=0.30, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _cap(self, zh, en):
  return self._mid(-0.90, zh, en, ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W)

 # ── beat 0: one line, one marked point ──────────────────────────
 def _unique(self):
  x0, sx, ly = -4.80, 0.75, 0.62
  g = VGroup(Line([XL + 0.05, ly, 0], [XR + 0.05, ly, 0], color=DIM, stroke_width=2.0),
             Line([x0, ly - 0.14, 0], [x0, ly + 0.14, 0], color=DIM, stroke_width=1.6))
  for c in CMULT:
   hot = abs(c - 1.0) < 1e-9
   g.add(Dot([x0 + sx * c, ly, 0], radius=0.085 if hot else 0.055,
             color=ACCENT_A if hot else DIM))
  g.add(self._sym(ly + 0.28, "D", ACCENT_A, FS_TAG, x=x0 + sx, w=0.40),
        self._sym(ly + 0.28, "c  ·  D", DIM, FS_TAG - 3, x=x0 + sx * 2.0, w=0.90),
        self._sym(ly + 0.40, "𝒜 ᵐ", ACCENT_B, FS_TAG - 1, x=XL + 0.35, w=0.80))
  grid, _p = self._numgrid(-4.60, -0.48, IDENT.astype(int).tolist(),
                           dx=0.42, dy=0.32, size=FS_TAG - 5, color=DIM,
                           hot=((0, 0), (1, 1), (2, 2)), hotcolor=ACCENT_A)
  g.add(grid)
  g.add(self._sym(0.22, "δ ¹      δ ²      δ ³", ACCENT_A, FS_TAG - 4, x=-4.60, w=1.60))
  g.add(self._sym(-0.48, f"D   =   {ms(D_IDENT, '.6f')}", ACCENT_A, FS_TAG - 3, x=-2.95, w=1.50))
  g.add(self._table(((f"dim 𝒜 ᵐ   =   {DIM_ALT}", ACCENT_B),
                     ("f  ,  g   ∈   𝒜 ᵐ            g   =   c  ·  f", DIM),
                     ("D ( δ ¹ , … , δ ᵐ )   =   1", ACCENT_A),
                     ("D ( x ¹ , … , x ᵐ )   =   D ( x )", ACCENT_A),
                     (f"m   =   {M_DIM}            det ( I )   =   {ms(D_IDENT, '.6f')}", ACCENT_C),
                     ("§ 5        ⇒        § 6", DIM)),
                    y0=0.88, dy=0.32, size=FS_TAG - 3))
  g.add(self._cap("線上每一點都是交錯形式，只有一點在標準基底上取值 1",
                  "every point of the line is an alternating form; one of them takes the value 1"))
  return g.add(self._foot("上一集算出交錯 m 重形式那個空間是一維的。這一集就靠那個一：差一個純量倍，這種形式只有一個",
                          "last episode found that the space of alternating m-forms is one-dimensional, and this episode lives off that one: up to a scalar multiple there is only one such form",
                          ACCENT_A,
                          "所以只要再要求它在標準基底上取值等於一，就把它完全定死了。那個唯一確定的形式就是行列式，它在一個矩陣的各直行上的值就是那個矩陣的行列式",
                          "so asking it to take the value one on the standard basis pins it down outright, and its value on the columns of a matrix is that matrix's determinant"))

 # ── beat 1: the six terms of a 3 x 3 ────────────────────────────
 def _lemma(self):
  p3, s3, f3 = PERM3[SHOW3]
  grid, pos = self._numgrid(-4.20, 0.30, [[ms(v) for v in row] for row in T3.tolist()],
                            dx=0.52, dy=0.42, size=FS_TAG - 3, color=INK,
                            hot=tuple((p3[j], j) for j in range(3)), hotcolor=ACCENT_A)
  g = VGroup(grid)
  for j in range(3):
   g.add(self._sym(1.06, str(j + 1), DIM, FS_TAG - 5, x=pos(0, j)[0], w=0.30))
   g.add(self._sym(pos(j, 0)[1], str(j + 1), DIM, FS_TAG - 5, x=-5.20, w=0.30))
  g.add(self._sym(-0.62, "σ   =   (  " + "  ".join(str(k + 1) for k in p3) + "  )",
                  ACCENT_A, FS_TAG - 2, x=-4.20, w=1.80))
  g.add(self._sym(-0.98, f"ε ( σ )   =   {ms(s3, '+.0f')}", ACCENT_A, FS_TAG - 3,
                  x=-4.20, w=1.50))
  rows = [("      σ            ε                ∏            ε  ∏", DIM)]
  for k, ((p, s, f), term) in enumerate(zip(PERM3, TERM3)):
   rows.append((f"( {' '.join(str(q + 1) for q in p)} )     {ms(s, '+.0f')}     "
                + "  ".join(ms(v) for v in f) + f"      {ms(term, '+.0f')}",
                ACCENT_A if k == SHOW3 else ACCENT_B))
  rows.append((f"Σ   =   {ms(sum(TERM3), '+.0f')}          det   =   "
               f"{ms(float(np.linalg.det(T3)), '.6f')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 5))
  g.add(self._cap("橘色那一列用的就是圖上三個橘色的格子",
                  "the orange row of the table uses the three orange cells of the grid"))
  return g.add(self._foot("引理 6.1 把它寫成顯式公式。對每一種把一到 m 重排的方式，從每一條直行各取一個元素，彼此落在不同橫列，乘起來",
                          "Lemma 6.1 writes it out explicitly: for each way of rearranging one through m, take one entry from every column, no two of them in the same row, and multiply",
                          ACCENT_A,
                          "再按照那個重排的奇偶配上正負號，最後全部加總。三階就是六項，右表逐項列出來，最後一列的總和與獨立算出來的行列式一樣",
                          "then attach a sign from the parity of that rearrangement and add; three by three gives six terms, and their total matches a determinant computed independently"))

 # ── beat 2: the transpose ───────────────────────────────────────
 def _transpose(self):
  g = VGroup()
  for cx, M, lab, col in ((-5.15, T3, "t", ACCENT_A), (-3.25, T3.T, "t ᵀ", ACCENT_B)):
   grid, _p = self._numgrid(cx, 0.36, [[ms(v) for v in row] for row in M.tolist()],
                            dx=0.44, dy=0.36, size=FS_TAG - 4, color=INK)
   g.add(grid, self._sym(1.14, lab, col, FS_TAG, x=cx, w=0.70))
   g.add(self._sym(-0.62, f"D   =   {ms(dexp(M.tolist()), '+.0f')}", col, FS_TAG - 3,
                   x=cx, w=1.40))
  g.add(self._table((("D ( t ᵀ )   =   D ( t )", ACCENT_A),
                     ("t σ ( 1 ) , 1  ⋯  t σ ( m ) , m   =   t 1 , ρ ( 1 )  ⋯  t m , ρ ( m )", DIM),
                     ("ρ   =   σ ⁻ ¹            σ   ↦   σ ⁻ ¹   :   S ₘ   →   S ₘ", ACCENT_C),
                     ("ε ( σ ⁻ ¹ )   =   ε ( σ )", ACCENT_C),
                     (f"D ( t )   =   {ms(D_T3, '+.0f')}        D ( t ᵀ )   =   "
                      f"{ms(D_T3T, '+.0f')}", ACCENT_B),
                     (f"| Δ |   ≤   {ms(abs(D_T3T - D_T3), '.1e')}", ACCENT_B),
                     (f"max | t  −  t ᵀ |   =   {ms(float(np.abs(T3 - T3.T).max()), '.0f')}",
                      ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("兩個陣列確實不同，最後一列就是它們差多少",
                  "the two grids really do differ, and the last row says by how much"))
  return g.add(self._foot("推論一說轉置不改變行列式。證明只要把乘積裡的因子依照橫列指標重新排序，乘積就變成依橫列取的同一個樣子",
                          "the first corollary says transposing changes nothing: reorder the factors of each product by their row index and it becomes the same thing read along the rows",
                          ACCENT_A,
                          "用的重排是原來那個的反排列。因為取反排列是一對一的對應，奇偶性又不變，整個和就原封不動。右邊兩個行列式相同，但兩個陣列本身不同",
                          "the rearrangement used is the inverse of the original, and since inverting is one to one and keeps the parity, the whole sum is untouched"))

 # ── beat 3: alternating in the rows ─────────────────────────────
 def _rows(self):
  cols = (ACCENT_A, ACCENT_B, DIM)
  left = [(f"t {'₁₂₃'[k]}", cols[k]) for k in range(3)]
  right = [left[1], left[0], left[2]]
  g = VGroup(self._column(-5.30, 0.30, left, dy=0.42, size=FS_TAG - 3),
             self._column(-3.30, 0.30, right, dy=0.42, size=FS_TAG - 3))
  g.add(self._arr([-4.90, 0.30, 0], [-3.70, 0.30, 0], DIM, sw=3, tl=0.13))
  g.add(self._sym(0.56, "t ₁   ↔   t ₂", ACCENT_A, FS_TAG - 4, x=-4.30, w=1.20),
        self._sym(0.04, "D   ↦   −  D", ACCENT_B, FS_TAG - 4, x=-4.30, w=1.20))
  g.add(self._sym(-0.62, f"D   =   {ms(D_T3, '+.0f')}", ACCENT_A, FS_TAG - 3, x=-5.30, w=1.40),
        self._sym(-0.62, f"D   =   {ms(D_SWAP, '+.0f')}", ACCENT_B, FS_TAG - 3, x=-3.30, w=1.40))
  g.add(self._table((("D ( t ᵀ )  =  D ( t )        ⇒        D ( t ₁ , … , t ₘ )", ACCENT_A),
                     (f"D ( t )                           {ms(D_T3, '+.0f')}", ACCENT_B),
                     (f"t ₁   ↔   t ₂                       {ms(D_SWAP, '+.0f')}", ACCENT_B),
                     (f"c  ·  t ₂        c  =  {ms(ROW_C, '.1f')}      {ms(D_SCALE, '+.1f')}",
                      ACCENT_C),
                     (f"t ₃  +  k  ·  t ₁    k  =  {ms(ROW_K, '.0f')}      {ms(D_SHEAR, '+.0f')}",
                      ACCENT_C),
                     (f"c  ·  D ( t )   =   {ms(ROW_C * D_T3, '+.1f')}", DIM),
                     (f"| Δ |   ≤   {ms(ROWERR, '.1e')}", ACCENT_A)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("右邊那一疊只有前兩條互換，第三條沒動",
                  "the right-hand stack has only its first two swapped; the third is where it was"))
  return g.add(self._foot("推論二立刻跟著來。既然轉置不改變行列式，而它對直行是交錯多重線性的，對橫列當然也是",
                          "the second corollary follows at once: the determinant is alternating and multilinear in the columns, and transposing makes it so in the rows too",
                          ACCENT_A,
                          "所以對調兩條橫列會變號，某一條乘上常數就整個乘上那個常數，某一條加上另一條的倍數則完全不變。右表三種操作各算一次，都對得上",
                          "so swapping two rows flips the sign, scaling one scales the whole thing, and adding a multiple of another changes nothing: the table runs all three"))

 # ── beat 4: k_T is the same for every f ─────────────────────────
 def _delta(self):
  g = VGroup()
  for yy, a, b, col in ((0.55, "f", "f ₜ", ACCENT_A), (-0.45, "g", "g ₜ", ACCENT_C)):
   g.add(self._box(-5.30, yy, a, col, w=0.80, h=0.52, size=FS_TAG))
   g.add(self._box(-3.20, yy, b, col, w=0.80, h=0.52, size=FS_TAG))
   g.add(self._arr([-4.90, yy, 0], [-3.60, yy, 0], ACCENT_B, sw=3, tl=0.13))
   g.add(self._sym(yy + 0.25, "×   Δ ( T )", ACCENT_B, FS_TAG - 4, x=-4.25, w=1.20))
  for cx in (-5.30, -3.20):
   g.add(self._arr([cx, 0.29, 0], [cx, -0.19, 0], DIM, sw=3, tl=0.11))
  g.add(self._sym(0.05, "×  c", DIM, FS_TAG - 4, x=-5.72, w=0.60),
        self._sym(0.05, "×  c", DIM, FS_TAG - 4, x=-2.78, w=0.60))
  rows = [("f ₜ ( ξ )   =   f ( T ξ ₁ , … , T ξ ₘ )   =   k ₜ  ·  f ( ξ )", ACCENT_A),
          (f"Δ ( T )   =   det ( t )   =   {ms(D_TD, '+.0f')}", ACCENT_B),
          ("        c            f ( ξ )        f ₜ ( ξ )        f ₜ  /  f", DIM)]
  for c, f, ft in FVAL:
   rows.append((f"    {ms(c, '+.1f')}        {ms(f, '+.1f')}      {ms(ft, '+.1f')}"
                f"      {ms(ft / f, '.6f')}", ACCENT_C))
  rows.append((f"| Δ |   ≤   {ms(KERR, '.1e')}", ACCENT_A))
  g.add(self._table(tuple(rows), y0=0.88, dy=0.28, size=FS_TAG - 4))
  g.add(self._cap("最後一欄兩個數字相同：那個倍率與選哪個形式無關",
                  "the last column repeats itself: that factor does not depend on the form chosen"))
  return g.add(self._foot("接著定義不依賴基底的行列式。取任何一個不是零的交錯 m 形式，把 T 先作用在每個輸入上再餵給它，得到的還是一個交錯 m 形式",
                          "next comes a determinant that needs no basis: take any nonzero alternating m-form and apply T to each input before feeding it in, and the result is again such a form",
                          ACCENT_A,
                          "所以是原來那個的常數倍。因為那個空間一維，那個常數與選哪個形式無關，就叫做 T 的 Δ。圖上兩個形式差一個 c，倍率卻是同一個",
                          "so it is a constant multiple of the original, and because the space is one-dimensional that constant is the same whichever form we start from"))

 # ── beat 5: Theorem 6.1 ─────────────────────────────────────────
 def _mult(self):
  g = VGroup()
  for cx in (-5.70, -4.20, -2.70):
   g.add(self._box(cx, 0.55, "ℝ ᵐ", ACCENT_A, w=0.86, h=0.52, size=FS_TAG))
  for xa, xb, lab, val in ((-5.27, -4.63, "T", D_T3), (-3.77, -3.13, "S", D_S3)):
   g.add(self._arr([xa, 0.55, 0], [xb, 0.55, 0], ACCENT_B, sw=3, tl=0.12))
   g.add(self._sym(0.86, lab, ACCENT_B, FS_TAG, x=(xa + xb) / 2, w=0.40))
   g.add(self._sym(0.14, f"Δ   =   {ms(val, '+.0f')}", ACCENT_C, FS_TAG - 4,
                   x=(xa + xb) / 2, w=1.10))
  g.add(self._arr([-5.70, -0.40, 0], [-2.70, -0.40, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._sym(-0.16, "S   ∘   T", ACCENT_A, FS_TAG - 2, x=-4.20, w=1.20))
  g.add(self._sym(-0.72, f"{ms(D_S3)}   ·   {ms(D_T3)}   =   {ms(D_ST3)}",
                  ACCENT_A, FS_TAG - 2, x=-4.20, w=2.20))
  g.add(self._table((("Δ ( S  ∘  T )   =   Δ ( S )   ·   Δ ( T )", ACCENT_A),
                     ("s   =   " + mrow(S3.astype(int).tolist()), DIM),
                     ("t   =   " + mrow(T3.astype(int).tolist()), DIM),
                     (f"Δ ( S )   =   {ms(D_S3, '+.0f')}", ACCENT_B),
                     (f"Δ ( T )   =   {ms(D_T3, '+.0f')}", ACCENT_B),
                     (f"Δ ( S )  ·  Δ ( T )   =   {ms(D_S3 * D_T3, '+.0f')}", ACCENT_C),
                     (f"Δ ( S  ∘  T )   =   {ms(D_ST3, '+.0f')}", ACCENT_C),
                     (f"| Δ |   ≤   {ms(MULERR, '.1e')}", ACCENT_A)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("最後兩個數相同，所以倒數第二列與最後一列對得起來",
                  "the last two numbers coincide, which is the whole content of the theorem"))
  return g.add(self._foot("定理 6.1 說 Δ 把合成變成相乘。證明只有兩行：把 S 合成 T 作用在一組輸入上，先把 S 提出一個 Δ S，再把 T 提出一個 Δ T",
                          "Theorem 6.1 says this turns composition into multiplication, and the proof is two lines: feed a composite in, pull out one factor for the outer map and one for the inner",
                          ACCENT_A,
                          "然後把形式本身約掉。右表拿兩個具體的三階矩陣核對，兩個行列式相乘與合成的行列式一樣，差距落在最後一列那個數量級",
                          "then cancel the form itself; the table checks it on two concrete three by three matrices, and the residual is the last row"))

 # ── beat 6: similarity, and singular if and only if zero ────────
 def _singular(self):
  g = VGroup()
  for yy, lab in ((0.60, "V"), (-0.40, "W")):
   for cx in (-5.40, -3.20):
    g.add(self._box(cx, yy, lab, ACCENT_A, w=0.80, h=0.52, size=FS_TAG + 1))
  for yy, lab, col in ((0.60, "T", ACCENT_B), (-0.40, "S", ACCENT_C)):
   g.add(self._arr([-5.00, yy, 0], [-3.60, yy, 0], col, sw=3, tl=0.13))
   g.add(self._sym(yy + 0.26, lab, col, FS_TAG, x=-4.30, w=0.40))
  for cx, lx in ((-5.40, -5.80), (-3.20, -2.80)):
   g.add(self._arr([cx, 0.34, 0], [cx, -0.14, 0], DIM, sw=3, tl=0.11))
   g.add(self._sym(0.10, "θ", DIM, FS_TAG, x=lx, w=0.40))
  g.add(self._sym(-0.92, f"Δ ( S )   =   Δ ( T )   =   {ms(D_T3, '+.0f')}",
                  ACCENT_A, FS_TAG - 2, x=-4.30, w=2.60))
  g.add(self._table((("S  =  θ ∘ T ∘ θ ⁻ ¹        ⇒        Δ ( S )  =  Δ ( T )", ACCENT_A),
                     (f"Δ ( T )  =  {ms(D_T3, '+.0f')}        Δ ( S )  =  "
                      f"{ms(D_SIM, '.6f')}", ACCENT_B),
                     ("D ( t )  =  Δ ( T )        D ( s · t )  =  D ( s ) D ( t )", ACCENT_A),
                     ("D ( t )   =   0        ⟺        ker ( t )   ≠   0", ACCENT_A),
                     ("u   =   " + mrow(SING.astype(int).tolist()), DIM),
                     ("u ₃   =   u ₁   +   2  ·  u ₂", ACCENT_C),
                     (f"D ( u )  =  {ms(D_SING, '.1e')}        rank  =  {RANK_SING}", WARN),
                     (f"D ( t )  =  {ms(D_T3, '+.0f')}        rank  =  {RANK_T3}", ACCENT_B)),
                    y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("紅的那一列行列式是零，秩也少了一",
                  "the red row has determinant zero, and one less than full rank to match"))
  return g.add(self._foot("定理 6.2 說相似變換的 Δ 相同，於是三個推論一起落地：矩陣的行列式等於它代表的那個變換的 Δ、矩陣乘積的行列式等於兩個行列式相乘",
                          "Theorem 6.2 says similar transformations share the same value, so three corollaries land together: a matrix has the determinant of the transformation it stands for, and products multiply",
                          ACCENT_A,
                          "還有最有用的一條，行列式等於零恰好等價於矩陣奇異。右表那個矩陣的第三橫列是第一橫列加兩倍的第二橫列，行列式就真的是零",
                          "and most usefully, the determinant vanishes exactly when the matrix is singular: the table's third row is the first plus twice the second, and its determinant really is zero"))

 # ── beat 7: Lemma 6.2, the reduction ────────────────────────────
 def _reduce(self):
  grid, pos = self._numgrid(-4.20, 0.10, [[ms(v) for v in row] for row in RED.tolist()],
                            dx=0.58, dy=0.44, size=FS_TAG - 4, color=INK,
                            hotcol=3, hotcolor=ACCENT_A)
  g = VGroup(grid)
  xc, yr = pos(0, 3)[0], pos(3, 0)[1]
  g.add(Line([-5.37, yr, 0], [-3.03, yr, 0], color=WARN, stroke_width=2.4))
  g.add(Line([xc, 0.96, 0], [xc, -0.76, 0], color=WARN, stroke_width=2.4))
  g.add(Rectangle(width=1.68, height=1.28, color=ACCENT_B,
                  stroke_width=2.4).move_to([-4.49, 0.32, 0]))
  g.add(self._sym(0.32, "s", ACCENT_B, FS_TAG + 1, x=-2.74, w=0.40),
        self._sym(1.16, "δ ᵐ", ACCENT_A, FS_TAG - 2, x=xc, w=0.70))
  g.add(self._table((("t ᵐ   =   δ ᵐ            s   =   ( t ) ᵐ ᵐ", ACCENT_A),
                     (f"D ( t )   =   {ms(D_RED, '.6f')}", ACCENT_B),
                     (f"D ( s )   =   {ms(D_SUB, '.6f')}", ACCENT_B),
                     ("  " + mrow(RED[3, :3].astype(int).tolist()) + "   →   "
                      + mrow(RED2[3, :3].astype(int).tolist()), DIM),
                     (f"D ( t )   =   {ms(D_RED2, '.6f')}", ACCENT_C),
                     ("T  ↾  X   =   id        ⇒        Δ ( T )   =   Δ ( T  ↾  Y )", ACCENT_A),
                     (f"m   =   4            dim Y   =   3", DIM)),
                    y0=0.90, dy=0.26, size=FS_TAG - 4))
  g.add(self._cap("劃掉的那一橫列換掉三個數，行列式還是一樣",
                  "the struck-out row gets three new entries and the determinant does not move"))
  return g.add(self._foot("引理 6.2 處理降階。當最後一條直行剛好是標準基底的最後一個向量時，行列式等於劃掉最後一橫列與最後一直行之後那個小矩陣的行列式",
                          "Lemma 6.2 drops a dimension: when the last column is the last standard basis vector, the determinant equals that of the matrix left after deleting the last row and column",
                          ACCENT_A,
                          "推廣到變換上就是引理 6.3：T 在補空間上是恆等時，Δ 可以只在剩下的子空間裡算。右表第四列換掉了被劃掉那一橫列的三個數，行列式紋風不動",
                          "Lemma 6.3 carries this to transformations: if T is the identity on a complement, the value may be computed inside the rest, which is the last two rows of the table"))

 # ── beat 8: Theorem 6.3, four minors ────────────────────────────
 def _expand(self):
  g = VGroup()
  spots = ((-5.20, 0.58), (-3.10, 0.58), (-5.20, -0.58), (-3.10, -0.58))
  for i, ((cx, cy), M) in enumerate(zip(spots, MINORS)):
   sign = (-1.0) ** (i + RSHOW)
   grid, _p = self._numgrid(cx, cy, [[ms(v) for v in row] for row in M],
                            dx=0.36, dy=0.24, size=FS_TAG - 6, color=INK)
   g.add(grid)
   ent = ms(T4[i][RSHOW])
   if T4[i][RSHOW] < 0:
    ent = "(  " + ent + "  )"
   g.add(self._sym(cy + 0.58, f"{ms(sign, '+.0f')[0]}   {ent}",
                   ACCENT_A if sign > 0 else ACCENT_C, FS_TAG - 4, x=cx, w=1.10))
  rows = [(f"r   =   {RSHOW + 1}            i          t ᵢ ᵣ          "
           f"D ( ( t ) ⁱ ʳ )", DIM)]
  for i, term in enumerate(EXPAND[RSHOW]):
   rows.append((f"        {i + 1}        {ms(T4[i][RSHOW], '+.0f')}        "
                f"{ms(MDET[i], '+.0f')}        {ms(term, '+.0f')}", ACCENT_B))
  rows.append((f"Σ   =   {ms(sum(EXPAND[RSHOW]), '+.0f')}        det   =   "
               f"{ms(float(np.linalg.det(T4)), '.4f')}", ACCENT_A))
  rows.append(("r  =  1 , 2 , 3        Σ   =   "
               + " , ".join(ms(sum(EXPAND[r]), '+.0f') for r in COLS), ACCENT_C))
  rows.append((f"| Δ |   ≤   {ms(EXERR, '.1e')}", ACCENT_A))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 5))
  g.add(self._cap("四個小陣列是四個不同的小矩陣，上面的符號正負交錯",
                  "the four grids are four different submatrices, and the signs above them alternate"))
  return g.add(self._foot("定理 6.3 就是餘因子展開。沿著第 r 條直行走下去，每個元素乘上劃掉它所在那一橫列與那一直行之後的小行列式，再配上正負交錯的符號",
                          "Theorem 6.3 is the expansion by minors: go down column r, multiply each entry by the smaller determinant left after deleting its own row and column, and attach alternating signs",
                          ACCENT_A,
                          "加起來就是原來的行列式。右表沿第二直行展開，四項逐項列出；倒數第二列是沿三條不同直行各展開一次的總和，三個數一模一樣",
                          "adding them gives the determinant; the table expands down the second column, and the row below it runs the same expansion down three different columns, to the same number"))

 # ── beat 9: Corollary 1 and the cofactor matrix ─────────────────
 def _cofactor(self):
  grid, _p = self._numgrid(-4.20, 0.14, [[ms(v) for v in row] for row in COFT.tolist()],
                           dx=0.70, dy=0.44, size=FS_TAG - 4, color=DIM,
                           hot=tuple((k, k) for k in range(4)), hotcolor=ACCENT_A)
  g = VGroup(grid)
  g.add(self._sym(1.18, "c ᵀ   ·   t", ACCENT_B, FS_TAG, x=-4.20, w=1.40))
  g.add(self._sym(-0.92, f"=   {ms(D_T4, '+.0f')}   ·   I", ACCENT_A, FS_TAG - 2,
                  x=-4.20, w=1.80))
  rows = [("c ᵢ ⱼ   =   ( − 1 ) ⁱ ⁺ ʲ   D ( ( t ) ⁱ ʲ )", ACCENT_A),
          ("Σ ᵢ   c ᵢ ᵣ   t ᵢ ₛ   =   δ ᵣ ₛ   ·   D ( t )", ACCENT_A)]
  for r, s, v in CROSS:
   rows.append((f"( r , s )  =  ( {r + 1} , {s + 1} )            Σ   =   {ms(v, '.1e')}",
                ACCENT_C))
  rows.append((f"D ( t )   =   {ms(D_T4, '+.0f')}", ACCENT_B))
  rows.append((f"| c ᵀ · t   −   D ( t ) · I |   ≤   {ms(COFERR, '.1e')}", ACCENT_B))
  rows.append(("s ᵣ ᵢ   =   c ᵢ ᵣ   /   D ( t )", ACCENT_A))
  rows.append((f"| s   −   t ⁻ ¹ |   ≤   {ms(INVERR, '.1e')}", ACCENT_A))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("對角線上四格相同，其餘十二格都是零",
                  "the four diagonal cells all read alike and the other twelve are zero"))
  return g.add(self._foot("如果把展開式裡的元素換成另一條直行上的，那個和就是零，因為它等於一個有兩條直行相同的矩陣的行列式",
                          "replace those entries by the ones from a different column and the sum is zero, since it is the determinant of a matrix with two equal columns",
                          ACCENT_A,
                          "兩件事合起來寫成一條：餘因子矩陣轉置後乘上原矩陣，剛好是行列式乘上單位矩陣，所以反矩陣就是餘因子除以行列式，最後一列與直接求逆比對過",
                          "both facts fit one line: the transposed cofactor matrix times the original is the determinant times the identity, so the inverse is cofactors over the determinant"))

 # ── beat 10: Cramer's rule ──────────────────────────────────────
 def _cramer(self):
  grid, _p = self._numgrid(-5.46, 0.30, [[ms(v) for v in row] for row in T3.tolist()],
                           dx=0.44, dy=0.36, size=FS_TAG - 4, color=INK)
  g = VGroup(grid)
  g.add(self._column(-4.26, 0.30, [(f"x {'₁₂₃'[k]}", ACCENT_A) for k in range(3)],
                     dy=0.38, size=FS_TAG - 3))
  g.add(self._sym(0.30, "=", DIM, FS_TAG, x=-3.58, w=0.30))
  g.add(self._column(-2.90, 0.30, [(ms(v), ACCENT_B) for v in YVEC.tolist()],
                     dy=0.38, size=FS_TAG - 3))
  g.add(self._sym(-0.72, f"D ( t )   =   {ms(D_T3, '+.0f')}", ACCENT_C, FS_TAG - 2,
                  x=-4.40, w=2.00))
  rows = [("t   ·   x   =   y", ACCENT_A),
          ("y   =   " + mrow([YVEC.tolist()]), ACCENT_B),
          (f"D ( t )   =   {ms(D_T3, '+.0f')}", ACCENT_C),
          ("        j            d ⱼ              x ⱼ", DIM)]
  for j in range(3):
   rows.append((f"        {j + 1}          {ms(DJ[j], '+.0f')}          "
                f"{ms(XCRAMER[j], '+.6f')}", ACCENT_A))
  rows.append((f"| Δ |   ≤   {ms(CRERR, '.1e')}", ACCENT_B))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 4))
  g.add(self._cap("三個商都是整數除以 54，與獨立解出來的那組逐項相同",
                  "the three quotients match, entry by entry, a solution found independently"))
  return g.add(self._foot("最後是 Cramer 法則。把第 j 條直行換成右手邊那個向量，算出來的行列式除以原本的行列式，就是解的第 j 個座標",
                          "last comes Cramer's rule: replace the jth column by the right-hand side, and that determinant over the original determinant is the jth coordinate of the solution",
                          ACCENT_A,
                          "右表三個座標與獨立的數值解法逐項相同。第 7 章還剩外代數、外冪與星算子這三節，整節的行列式性質到此全部兌現",
                          "the table's three coordinates agree entry by entry with an independent solver; three sections of chapter 7 remain, on exterior algebra, exterior powers and the star operator"))

 def stage(self):
  a, b, c = self._unique(), self._lemma(), self._transpose()
  d, e, f_ = self._rows(), self._delta(), self._mult()
  h, i, j = self._singular(), self._reduce(), self._expand()
  k, l = self._cofactor(), self._cramer()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE88ZH, AdvCalcE88EN = make(AdvCalcE88Base, "88", prefix="AdvCalcE")
