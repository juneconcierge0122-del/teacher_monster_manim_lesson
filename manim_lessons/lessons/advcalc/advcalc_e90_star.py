"""advcalc E90 -- chapter 7, sections 8 and 9 (book pp. 319-320): exterior
powers of a scalar product space, and the star operator.

Two sections of a page and a bit each, and they are one idea.  Section 8 puts a
scalar product on the exterior powers: given a nondegenerate symmetric form on V
-- the book calls it a scalar product even where it is not positive definite --
the determinant of the matrix of pairwise products turns the q-th power into a
scalar product space of its own.  What makes that definition legal is Theorem
7.3 from the previous episode: the right-hand side is alternating and multilinear
in each half, so it extends from wedges of vectors to the whole power.

Section 9 spends it.  The top power is one-dimensional, so its induced product
has a constant sign and exactly two of its elements are unit; choosing one is
choosing an orientation.  With an orientation fixed, wedging a q-vector against
an (n-q)-vector lands in that one-dimensional space and so is a number, which by
nondegeneracy is a scalar product against a unique (n-q)-vector.  That vector is
the star, and the three identities that close the chapter -- what star does on
the basis, that star twice is plus or minus the identity, and that star
preserves the product up to a sign -- all read off the signs of the basis.

The signature is taken as three plus signs and one minus, so the number the
book calls # is 1 and none of the signs in (9.4) or (9.5) collapse to a vacuous
+1.  With an all-positive signature every one of those identities would come out
as "equals itself", and a sign error would be invisible; that is the reason for
the choice.

Every number on screen is computed here and checked against an implementation
that shares no code with the one being shown.  The star is built twice: once by
solving its defining identity (9.2) against each basis element of the
complementary power, and once by reading the sign off epsilon and the basis
signs as (9.3) prescribes, with nothing solved.  The scalar product on the power
is likewise computed twice, once as the determinant of the matrix of pairwise
products by numpy's factorisation and once as the diagonal form that (8.3) says
it must take in this basis.
"""
import itertools
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
XL, XR = -5.90, -2.50                       # the left figure lives between these


def sgn_seq(seq):
 """The sign of the permutation that sorts seq into increasing order.

 This is the book's epsilon_k, counted off inversions rather than looked up."""
 s, a = 1, list(seq)
 for i in range(len(a)):
  for j in range(i + 1, len(a)):
   if a[i] > a[j]:
    s = -s
 return s


def ms(v, spec=".0f"):
 """A number as it should read on screen: a real minus sign, not a hyphen."""
 if v == 0:
  v = 0.0
 return format(v, spec).replace("-", "−")


N = 4
SIG = (1.0, 1.0, 1.0, -1.0)                 # (u_i, u_j) = +- delta_ij, the basis of (8.2)
HASH = sum(1 for g in SIG if g < 0)         # the # of (8.3), (8.4), (9.1) and (9.5)
Q = 2
assert HASH > 0, \
    "an all-positive signature would make every sign below a vacuous +1, hiding any error"


def idx(q):
 """The increasing q-tuples: one per basis element of the q-th power."""
 return list(itertools.combinations(range(N), q))


def gram_diag(q):
 """(8.3) read as a formula: (u_i, u_i) is the product of the signs it uses."""
 return np.array([math.prod(SIG[r] for r in i) for i in idx(q)])


def gram_full(q, xs, ys):
 """(8.1) from the definition: the determinant of the matrix of pairwise products.

 This is the half that goes through numpy's factorisation, so comparing it
 against `gram_diag` is a test rather than a restatement."""
 return float(np.linalg.det(np.array([[sum(SIG[k] * x[k] * y[k] for k in range(N))
                                       for y in ys] for x in xs])))


def sp(q, a, b):
 """The scalar product on the q-th power, in the basis {u_i}."""
 return float(np.sum(gram_diag(q) * np.asarray(a) * np.asarray(b)))


def wedge_top(q, a, b):
 """The coefficient of u_1 ^ ... ^ u_n in (sum a_i u_i) ^ (sum b_j u_j).

 Every term with a repeated index drops out, which is the vanishing rule of the
 previous episode; what survives carries the sign of the shuffle."""
 I, J = idx(q), idx(N - q)
 tot = 0.0
 for p, i in enumerate(I):
  for r, j in enumerate(J):
   if set(i) & set(j):
    continue
   tot += a[p] * b[r] * sgn_seq(list(i) + list(j))
 return float(tot)


def star_solve(q, a):
 """(9.2) solved: the unique element with (y, *v) = f_v(y) for every basis y."""
 J, gj = idx(N - q), gram_diag(N - q)
 eye = np.eye(len(J))
 return np.array([wedge_top(q, a, eye[r]) / gj[r] for r in range(len(J))])


def star_formula(q, a):
 """(9.3) instead: the sign read off epsilon and the basis signs, nothing solved."""
 I, J = idx(q), idx(N - q)
 out = np.zeros(len(J))
 for p, i in enumerate(I):
  if a[p] == 0:
   continue
  j = tuple(sorted(set(range(N)) - set(i)))
  out[J.index(j)] += a[p] * sgn_seq(list(i) + list(j)) * math.prod(SIG[k] for k in j)
 return out


_rng = np.random.default_rng(90)
EYE = np.eye(N)
DIMS = [len(idx(q)) for q in range(N + 1)]
assert DIMS == [math.comb(N, q) for q in range(N + 1)], \
    "the powers have the dimensions Theorem 5.2 gave them"

# ── beat 0: the form, and the isomorphism it induces ─────────────────
G_V = np.diag(SIG)
assert float(np.abs(G_V - G_V.T).max()) == 0.0, "symmetric"
assert abs(float(np.linalg.det(G_V))) > 1e-12, "and nondegenerate, which is all 'scalar product' means here"
DET_GV = float(np.linalg.det(G_V))
# y |-> ybar is an isomorphism exactly because the form is nondegenerate
RANK_GV = int(np.linalg.matrix_rank(G_V))
assert RANK_GV == N, "so the map of V onto its dual really is onto"
NEG_IDX = [k + 1 for k, g in enumerate(SIG) if g < 0]

# ── beat 1: (8.1) is symmetric, and agrees with the diagonal form ────
US = [_rng.standard_normal(N) for _ in range(Q)]
VS = [_rng.standard_normal(N) for _ in range(Q)]
SYM_ERR = abs(gram_full(Q, US, VS) - gram_full(Q, VS, US))
assert SYM_ERR < 1e-12, "(8.1) is symmetric in u and v, as the determinant makes plain"
SP_UV = gram_full(Q, US, VS)
# the 2 x 2 of pairwise products, as the screen will show it
PAIR = np.array([[sum(SIG[k] * US[i][k] * VS[j][k] for k in range(N))
                  for j in range(Q)] for i in range(Q)])
assert abs(float(np.linalg.det(PAIR)) - SP_UV) < 1e-12, "and it is that determinant"

# ── beats 2 and 3: (8.2) and (8.3) ──────────────────────────────────
I2 = idx(Q)
G2 = np.array([[gram_full(Q, [EYE[r] for r in i], [EYE[s] for s in j]) for j in I2]
               for i in I2])
OFF = float(np.abs(G2 - np.diag(np.diag(G2))).max())
DIAG2 = np.diag(G2)
assert OFF < 1e-12, \
    "distinct index tuples are orthogonal: one index is missing from the other, so a whole row vanishes"
assert all(abs(abs(d) - 1.0) < 1e-12 for d in DIAG2), "and each basis element is unit"
assert float(np.abs(DIAG2 - gram_diag(Q)).max()) < 1e-12, \
    "the determinant and the product-of-signs formula agree entry by entry"
HASH_Q = int(sum(1 for d in DIAG2 if d < 0))
assert 0 < HASH_Q < len(DIAG2), "both signs occur in the power, so the table is not one fact six times"
# the row that vanishes when the tuples differ, shown concretely
MISS_I, MISS_J = I2[0], I2[3]      # (1 2) against (2 3): one shared index, one dead row
MISS_ROW = [[sum(SIG[k] * EYE[r][k] * EYE[s][k] for k in range(N)) for s in MISS_J]
            for r in MISS_I]
assert any(all(abs(v) < 1e-12 for v in row) for row in MISS_ROW), \
    "and there it is: a whole row of zeros"

# ── beat 4: (8.4) ───────────────────────────────────────────────────
TOP = gram_full(N, [EYE[r] for r in range(N)], [EYE[r] for r in range(N)])
TOP_PRED = (-1.0) ** HASH
assert abs(TOP - TOP_PRED) < 1e-12, "(8.4): the top power's self product is minus one to the #"

# ── beat 5: (9.1), the orientation ──────────────────────────────────
GTOP = float(gram_diag(N)[0])
assert abs(abs(GTOP) - 1.0) < 1e-12, "the top power is one-dimensional and its product is nondegenerate"
UNITS = 2                                    # +u and -u, and nothing else
assert abs(GTOP - TOP_PRED) < 1e-12, "and that sign is the one (8.4) predicted"

# ── beats 6 to 8: the star, built two independent ways ──────────────
STAR_ERR, DEF_ERR = 0.0, 0.0
for _ in range(40):
 _a = _rng.standard_normal(len(I2))
 STAR_ERR = max(STAR_ERR, float(np.abs(star_solve(Q, _a) - star_formula(Q, _a)).max()))
assert STAR_ERR < 1e-12, \
    "solving (9.2) and reading off (9.3) give the same operator -- the one real check in this episode"
_J = idx(N - Q)
for _p in range(len(I2)):
 _a = np.eye(len(I2))[_p]
 _sa = star_solve(Q, _a)
 for _r in range(len(_J)):
  _b = np.eye(len(_J))[_r]
  DEF_ERR = max(DEF_ERR, abs(sp(N - Q, _b, _sa) - wedge_top(Q, _a, _b)))
assert DEF_ERR < 1e-12, "and the defining identity holds on every pair of basis elements"
# the table of *u_i, as (9.3) writes it
STARTAB = []
for _p, _i in enumerate(I2):
 _j = tuple(sorted(set(range(N)) - set(_i)))
 _c = star_solve(Q, np.eye(len(I2))[_p])
 STARTAB.append((_i, _j, sgn_seq(list(_i) + list(_j)), float(_c[_J.index(_j)])))
assert len({c for _i, _j, _e, c in STARTAB}) > 1, "the coefficients are not all the same number"
# the wedges that vanish: a repeated index
VANISH = sum(1 for _i in I2 for _j in _J if set(_i) & set(_j))
TOTAL = len(I2) * len(_J)
assert 0 < VANISH < TOTAL, "some pairs vanish and some do not"

# ── beat 9: (9.4) ───────────────────────────────────────────────────
DD_K = Q * (N - Q) + HASH
DD_PRED = (-1.0) ** DD_K
DD_ERR = 0.0
for _ in range(40):
 _a = _rng.standard_normal(len(I2))
 DD_ERR = max(DD_ERR, float(np.abs(star_solve(N - Q, star_solve(Q, _a)) - DD_PRED * _a).max()))
assert DD_ERR < 1e-12, "(9.4): star twice is plus or minus the identity, with that exponent"
assert DD_PRED < 0, "and here it is minus, so the identity is not a tautology"
# the same exponent across every q, so the table is not one case
DDQ = []
for _q in range(N + 1):
 _k = _q * (N - _q) + HASH
 _e = 0.0
 for _ in range(12):
  _a = _rng.standard_normal(len(idx(_q)))
  _e = max(_e, float(np.abs(star_solve(N - _q, star_solve(_q, _a))
                            - (-1.0) ** _k * _a).max()))
 DDQ.append((_q, _k, (-1) ** _k, _e))
 assert _e < 1e-12, f"(9.4) holds at q = {_q}"
DDERR = max(e for *_r, e in DDQ)
assert len({s for _q, _k, s, _e in DDQ}) == 2, "both signs occur across the five powers"

# ── beat 10: (9.5) ──────────────────────────────────────────────────
FIVE_ERR, FIVE_PAIRS = 0.0, []
for _ in range(40):
 _a, _b = _rng.standard_normal(len(I2)), _rng.standard_normal(len(I2))
 FIVE_ERR = max(FIVE_ERR, abs(sp(N - Q, star_solve(Q, _a), star_solve(Q, _b))
                              - (-1.0) ** HASH * sp(Q, _a, _b)))
assert FIVE_ERR < 1e-11, "(9.5): star preserves the product up to minus one to the #"
for _p in (0, 2, 5):
 _a = np.eye(len(I2))[_p]
 FIVE_PAIRS.append((I2[_p], sp(Q, _a, _a),
                    sp(N - Q, star_solve(Q, _a), star_solve(Q, _a))))
assert any(abs(v - w) > 0.5 for _i, v, w in FIVE_PAIRS), \
    "and the two columns really do differ, since # is odd"


class AdvCalcE90Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 90

 MODE_LABEL = {
  0: {"zh": "純量積：對稱、非退化，不必正定",
      "en": "a scalar product: symmetric, nondegenerate, not necessarily definite"},
  1: {"zh": "( 8.1 )：外冪上的純量積",
      "en": "(8.1): a scalar product on the exterior power"},
  2: {"zh": "( 8.2 )：取一組 ± 1 的基底",
      "en": "(8.2): a basis whose products are plus or minus one"},
  3: {"zh": "( 8.3 )：外冪的基底也是正交的",
      "en": "(8.3): the power's basis is orthogonal too"},
  4: {"zh": "( 8.4 )：最高次冪的自乘",
      "en": "(8.4): the top power's self product"},
  5: {"zh": "( 9.1 )：兩個單位元素，選一個就是定向",
      "en": "(9.1): two unit elements, and choosing one is an orientation"},
  6: {"zh": "( 9.2 )：星算子的定義",
      "en": "(9.2): the star operator defined"},
  7: {"zh": "基底上的星：重複的指標全是零",
      "en": "the star on the basis: repeated indices give zero"},
  8: {"zh": "( 9.3 )：兩種算法對照",
      "en": "(9.3): the two computations compared"},
  9: {"zh": "( 9.4 )：星兩次等於正負恆等",
      "en": "(9.4): star twice is plus or minus the identity"},
  10: {"zh": "( 9.5 )：第 7 章結束",
       "en": "(9.5), and the end of chapter 7"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.90, dy=0.26, size=FS_TAG - 4):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _cap(self, zh, en):
  return self._mid(-0.90, zh, en, ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W)

 def _signs(self, cx, cy, vals, dx=0.52, size=FS_TAG - 3):
  """A row of plus and minus ones, the negative ones picked out in red."""
  g = VGroup()
  x0 = cx - (len(vals) - 1) * dx / 2
  for k, v in enumerate(vals):
   g.add(self._sym(cy, ms(v, "+.0f"), WARN if v < 0 else ACCENT_B, size,
                   x=x0 + k * dx, w=dx - 0.04))
  return g

 # ── beat 0: the form on V, carried to the dual ──────────────────
 def _form(self):
  g = VGroup()
  grid, _p = self._numgrid(-4.90, 0.52, [[ms(v) for v in row] for row in G_V.tolist()],
                           dx=0.44, dy=0.26, size=FS_TAG - 6, color=INK,
                           hot=((3, 3),), hotcolor=WARN)
  g.add(grid, self._sym(1.16, "(  u ᵢ  ,  u ⱼ  )", ACCENT_A, FS_TAG - 2, x=-4.90, w=1.90))
  g.add(self._sym(-0.26, f"det   =   {ms(DET_GV, '+.0f')}        rank   =   {RANK_GV}",
                  ACCENT_C, FS_TAG - 3, x=-4.40, w=2.40))
  g.add(self._sym(-0.60, "y   ↦   ȳ        :        V   →   V *", ACCENT_A,
                  FS_TAG - 3, x=-4.40, w=2.80))
  g.add(self._table((("(  ,  )   :   V  ×  V   →   ℝ", ACCENT_A),
                     ("(  x  ,  y  )   =   (  y  ,  x  )", ACCENT_B),
                     (f"det  (  u ᵢ  ,  u ⱼ  )   =   {ms(DET_GV, '+.0f')}   ≠   0", ACCENT_B),
                     ("ȳ ( x )   =   (  x  ,  y  )            ȳ   ∈   V *", DIM),
                     ("(  ū  ,  v̄  )   =   (  u  ,  v  )", ACCENT_C),
                     (f"n   =   {N}        #   =   {HASH}        "
                      f"σ   =   ( + , + , + , − )", ACCENT_C)),
                    y0=0.88, dy=0.25))
  g.add(self._cap("第四個對角元是負的，所以這個純量積不是正定的",
                  "the fourth diagonal entry is negative, so this scalar product is not definite"))
  return g.add(self._foot(
   "第 8 節與第 9 節各只有一頁多，但它們是同一件事。先在 V 上給一個非退化的對稱雙線性形式——書上把它叫純量積，即使它不是正定的也照叫",
   "sections 8 and 9 are a page and a bit each, and they are one idea: start with a nondegenerate symmetric bilinear form on V, which the book calls a scalar product even where it is not positive definite",
   ACCENT_A,
   "非退化讓每個向量對應到對偶空間裡一個泛函，而且是個同構，於是對偶空間上也有一個純量積。這一集把負號個數取成一，否則後面每一條等式的正負號都會塌成加一，錯了也看不出來",
   "nondegeneracy sends each vector to a functional on the dual, isomorphically, so the dual carries a scalar product too; the signature here has one minus, or every sign below would collapse to plus one and hide an error",
   ))

 # ── beat 1: (8.1) ───────────────────────────────────────────────
 def _power(self):
  g = VGroup()
  grid, pos = self._numgrid(-4.40, 0.46, [[ms(v, "+.3f") for v in row]
                                          for row in PAIR.tolist()],
                            dx=1.30, dy=0.42, size=FS_TAG - 4, color=INK)
  g.add(grid, self._sym(1.12, "(  ū ᵢ  ,  v̄ ⱼ  )", ACCENT_A, FS_TAG - 2, x=-4.40, w=2.20))
  g.add(self._sym(-0.18, f"det   =   {ms(SP_UV, '+.4f')}", ACCENT_B, FS_TAG - 2,
                  x=-4.40, w=2.40))
  g.add(self._sym(-0.58, f"( ū ₁ ∧ ū ₂ ,  v̄ ₁ ∧ v̄ ₂ )   =   {ms(SP_UV, '+.4f')}",
                  ACCENT_A, FS_TAG - 4, x=-4.40, w=3.10))
  g.add(self._table((("( ū ₁ ∧ ⋯ ∧ ū q ,  v̄ ₁ ∧ ⋯ ∧ v̄ q )", ACCENT_A),
                     ("=   det  (  ū ᵢ  ,  v̄ ⱼ  )", ACCENT_A),
                     ("ū        ⇒        v̄   ↦   det   ∈   𝒜 q ( V * )", DIM),
                     ("7.3        ⇒        𝒜 q   →   ℝ", ACCENT_C),
                     ("v̄        ⇒        ū   ↦   det", DIM),
                     (f"(  u  ,  v  )  −  (  v  ,  u  )        {ms(SYM_ERR, '.1e')}",
                      ACCENT_B)),
                    y0=0.90, dy=0.26))
  g.add(self._cap("左邊那個二乘二行列式就是右邊那個純量積，兩者是同一個數",
                  "the two by two determinant on the left is the scalar product on the right"))
  return g.add(self._foot(
   "第 8 節把純量積搬到外冪上。公式 8.1 說：兩個楔積的純量積，就是那個兩兩相乘排成的矩陣的行列式。這個定義看起來理所當然，其實要靠上一集的定理 7.3 才站得住",
   "section 8 carries the scalar product to the exterior powers: formula 8.1 says the product of two wedges is the determinant of the matrix of pairwise products -- obvious looking, but it needs Theorem 7.3 to stand up",
   ACCENT_A,
   "固定一半，右邊對另一半是交錯多重線性的，所以由定理 7.3 唯一地延拓成那個外冪上的線性函數；兩邊都做一次就得到雙線性。對稱則從行列式本身看得出來",
   "fix one half and the right-hand side is alternating and multilinear in the other, so Theorem 7.3 extends it uniquely to a linear function on the power; doing both halves gives bilinearity, and symmetry is plain from the determinant",
   ))

 # ── beat 2: (8.2) ───────────────────────────────────────────────
 def _basis(self):
  g = VGroup()
  g.add(self._sym(0.96, "(  u ᵢ  ,  u ⱼ  )   =   ±  δ ᵢ ⱼ", ACCENT_A, FS_TAG - 1,
                  x=-4.25, w=3.00))
  g.add(self._signs(-4.25, 0.50, list(SIG), dx=0.66, size=FS_TAG))
  for k in range(N):
   g.add(self._sym(0.14, f"u {'₁₂₃₄'[k]}", DIM, FS_TAG - 4,
                   x=-4.25 - (N - 1) * 0.33 + k * 0.66, w=0.60))
  g.add(self._sym(-0.28, f"(  u ᵢ  ,  u ᵢ  )        i   =   1 , … , {N}",
                  DIM, FS_TAG - 4, x=-4.25, w=3.00))
  g.add(self._sym(-0.68, f"#   =   {HASH}        n  −  #   =   {N - HASH}",
                  ACCENT_C, FS_TAG - 3, x=-4.25, w=2.60))
  g.add(self._sym(-0.98, "(  u ᵢ  ,  u ⱼ  )   =   0        i   ≠   j",
                  ACCENT_B, FS_TAG - 4, x=-4.25, w=3.00))
  g.add(self._table(((" 2 , 7.1        ⇒        ∃   { u ᵢ }", ACCENT_C),
                     ("(  u ᵢ  ,  u ⱼ  )   =   ±  δ ᵢ ⱼ", ACCENT_A),
                     (f"n   =   {N}", ACCENT_B),
                     (f"#  { '{' } + 1 { '}' }   =   {N - HASH}", ACCENT_B),
                     (f"#  { '{' } − 1 { '}' }   =   #   =   {HASH}", WARN),
                     (f"i   :   {' , '.join(str(k) for k in NEG_IDX)}", WARN)),
                    y0=0.88, dy=0.26))
  g.add(self._cap("紅色那一個就是整集所有正負號的來源",
                  "the red one is where every sign in this episode comes from"))
  return g.add(self._foot(
   "要證那個純量積非退化，得先挑一組好的基底。第 2 章的定理 7.1 保證：在任何非退化對稱形式之下，都找得到一組基底，使得兩兩相乘不是正一就是負一，不同的兩個則是零",
   "showing the product is nondegenerate needs a good basis first, and Theorem 7.1 of chapter 2 provides one: under any nondegenerate symmetric form there is a basis whose vectors pair to plus or minus one, and to zero with each other",
   ACCENT_A,
   "負號的個數就是書上那個井字號。它不依賴選了哪一組這樣的基底，而後面第 9 節每一條等式的正負號都是它決定的",
   "the number of minus signs is the book's hash mark; it does not depend on which such basis was chosen, and it fixes the sign in every identity of section 9",
   ))

 # ── beat 3: (8.3) ───────────────────────────────────────────────
 def _orthogonal(self):
  g = VGroup()
  grid, _p = self._numgrid(-4.60, 0.40, [[ms(v) for v in row] for row in MISS_ROW],
                           dx=0.70, dy=0.44, size=FS_TAG - 3, color=INK,
                           hotrow=0, hotcolor=WARN)
  g.add(grid)
  g.add(self._sym(1.10, f"i   =   ( {' '.join(str(r + 1) for r in MISS_I)} )        "
                        f"j   =   ( {' '.join(str(s + 1) for s in MISS_J)} )",
                  ACCENT_A, FS_TAG - 3, x=-4.60, w=2.80))
  g.add(self._sym(-0.20, "det   =   0", WARN, FS_TAG - 2, x=-4.60, w=1.80))
  g.add(self._signs(-4.25, -0.62, list(DIAG2), dx=0.50, size=FS_TAG - 2))
  g.add(self._sym(-0.96, "(  ū ᵢ  ,  ū ᵢ  )", DIM, FS_TAG - 4, x=-4.25, w=1.80))
  rows = [("      i            j            (  ū ᵢ  ,  ū ⱼ  )", DIM)]
  for k, i in enumerate(I2):
   rows.append((f"  ( {' '.join(str(r + 1) for r in i)} )        "
                f"( {' '.join(str(r + 1) for r in i)} )            "
                f"{ms(DIAG2[k], '+.0f')}",
                WARN if DIAG2[k] < 0 else ACCENT_B))
  rows.append((f"i  ≠  j   ⇒   0        | Δ |  ≤  {ms(OFF, '.1e')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.21, size=FS_TAG - 5))
  g.add(self._cap("上面那一列整列是零，因為第一個指標不在右邊那一組裡",
                  "the upper row is all zeros, because its index is missing from the other tuple"))
  return g.add(self._foot(
   "公式 8.3 說外冪上那組基底也是正交的，而且每個元素自乘是正一或負一。不同的兩個指標組，一定有某個指標只出現在其中一邊，那個矩陣就整條橫列是零，行列式當然是零",
   "formula 8.3 says the power's basis is orthogonal too, each element pairing with itself to plus or minus one: two different index tuples always leave one index out of the other, which makes a whole row of the matrix vanish",
   ACCENT_A,
   "相同的指標組，那個矩陣對角線是正負一、其餘是零，行列式就是對角元的乘積。四維取二階有六個基底元素，右表那六個自乘的值裡有三個是負的",
   "for equal tuples the matrix has plus or minus one down the diagonal and zeros elsewhere, so the determinant is the product of those; four dimensions at order two give six basis elements, three of them with a negative self product",
   ))

 # ── beat 4: (8.4) ───────────────────────────────────────────────
 def _top(self):
  g = VGroup()
  g.add(self._sym(0.92, "u ₁  ∧  u ₂  ∧  u ₃  ∧  u ₄", ACCENT_A, FS_TAG - 1,
                  x=-4.25, w=3.00))
  g.add(self._signs(-4.25, 0.52, list(SIG), dx=0.66, size=FS_TAG))
  g.add(self._sym(0.08, f"∏ ᵢ  (  u ᵢ  ,  u ᵢ  )   =   {ms(TOP, '+.0f')}   =   "
                        f"( − 1 ) ^ #", ACCENT_A, FS_TAG - 3, x=-4.25, w=3.10))
  g.add(self._sym(-0.28, f"#   =   {HASH}", WARN, FS_TAG - 2, x=-4.25, w=1.60))
  g.add(self._sym(-0.62, f"dim 𝒜 ⁿ   =   {DIMS[N]}", ACCENT_C, FS_TAG - 3,
                  x=-4.25, w=2.20))
  rows = [("      q        dim 𝒜 q        (  ū ᵢ  ,  ū ᵢ  )", DIM)]
  for q in range(N + 1):
   d = gram_diag(q)
   rows.append((f"      {q}            {DIMS[q]}            "
                + "  ".join(ms(v, "+.0f") for v in d),
                ACCENT_A if q == N else ACCENT_B))
  rows.append((f"( u ₁ ∧ ⋯ ∧ u ₙ ,  u ₁ ∧ ⋯ ∧ u ₙ )   =   {ms(TOP, '+.0f')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.22, size=FS_TAG - 5))
  g.add(self._cap("最後一列只有一個數，因為最高次冪是一維的",
                  "the last row carries one number only, because the top power is a line"))
  return g.add(self._foot(
   "公式 8.4 把最高次冪算出來：把整組基底楔起來，那個元素自乘就是全部對角元的乘積，也就是負一的井字號次方。這一集取的是三正一負，所以答案是負一",
   "formula 8.4 computes the top power: wedge the whole basis together and that element's self product is the product of all the diagonal entries, minus one to the hash; with three pluses and one minus it comes out minus one",
   ACCENT_A,
   "右表把五個外冪的維數與自乘值都列出來，一到四那幾列負號的個數各不相同。最高次冪只有一個基底元素，這件事是下一拍的全部根據",
   "the table lists the dimension and the self products for all five powers, and the number of minus signs differs from row to row; the top power has a single basis element, which is what the next beat rests on",
   ))

 # ── beat 5: (9.1), the orientation ──────────────────────────────
 def _orient(self):
  g = VGroup()
  ly = 0.54
  g.add(Line([-5.70, ly, 0], [-2.80, ly, 0], color=DIM, stroke_width=2.0))
  g.add(self._sym(ly + 0.44, "𝒜 ⁿ", ACCENT_C, FS_TAG - 1, x=-5.55, w=0.80))
  for x, col, lab in ((-5.00, ACCENT_A, "ū"), (-3.60, DIM, "−  ū")):
   g.add(Dot([x, ly, 0], radius=0.082, color=col))
   g.add(self._sym(ly + 0.30, lab, col, FS_TAG - 2, x=x, w=0.80))
  g.add(Line([-4.30, ly - 0.13, 0], [-4.30, ly + 0.13, 0], color=DIM, stroke_width=1.6))
  g.add(self._sym(-0.04, f"(  ū  ,  ū  )   =   {ms(GTOP, '+.0f')}   =   ( − 1 ) ^ #",
                  ACCENT_A, FS_TAG - 3, x=-4.30, w=3.00))
  g.add(self._sym(-0.44, f"#  { '{' } ū  :  ( ū , ū ) = ± 1 { '}' }   =   {UNITS}",
                  ACCENT_B, FS_TAG - 3, x=-4.30, w=2.80))
  g.add(self._sym(-0.86, "ū        ⇄        −  ū", ACCENT_C, FS_TAG - 3,
                  x=-4.30, w=2.60))
  g.add(self._table((("dim 𝒜 ⁿ   =   1            n   =   dim V", ACCENT_A),
                     ("sgn  (  ū  ,  ū  )        ∀  ū  ≠  0", ACCENT_B),
                     (f"#  { '{' } ū  :  ( ū , ū ) = ± 1 { '}' }   =   {UNITS}", ACCENT_B),
                     (f"(  ū  ,  ū  )   =   ( − 1 ) ^ #   =   {ms(GTOP, '+.0f')}", ACCENT_A),
                     ("ū        :        (  ū  ,  ū  )   =   ( − 1 ) ^ #", ACCENT_C),
                     ("ū   ↦   −  ū        ⇒        ∗   ↦   −  ∗", DIM)),
                    y0=0.88, dy=0.26))
  g.add(self._cap("線上只有這兩點是單位的，其餘都不是",
                  "only those two points of the line are unit; none of the others are"))
  return g.add(self._foot(
   "第 9 節從一件小事開始。最高次冪是一維的，而導出的純量積非退化，所以每個不是零的元素自乘都同號；於是恰好有兩個元素自乘等於正一或負一，彼此差一個負號",
   "section 9 starts from something small: the top power is a line and its induced product is nondegenerate, so every nonzero element has the same sign, and exactly two of them are unit -- each the negative of the other",
   ACCENT_A,
   "選定其中一個並固定住，幾何上就是替 V 選了一個定向。整節接下來的定義都依賴這個選擇：換成另一個，星算子就整個差一個負號",
   "choosing one of them and holding it fixed is geometrically a choice of orientation for V, and everything defined in the rest of the section depends on it: take the other and the star changes sign throughout",
   ))

 # ── beat 6: (9.2), the definition of the star ───────────────────
 def _define(self):
  g = VGroup()
  xa, xb, yt, yb = -5.30, -3.25, 0.70, -0.30
  g.add(self._box(xa, yt, "𝒜 q", ACCENT_B, w=1.10, h=0.46, size=FS_TAG - 1))
  g.add(self._box(xb, yt, "𝒜 ⁿ ⁻ q", ACCENT_C, w=1.40, h=0.46, size=FS_TAG - 1))
  g.add(self._box((xa + xb) / 2, yb, "𝒜 ⁿ   ≅   ℝ", ACCENT_A,
                  w=1.80, h=0.46, size=FS_TAG - 1))
  g.add(self._arr([xa + 0.20, yt - 0.27, 0], [(xa + xb) / 2 - 0.50, yb + 0.25, 0],
                  DIM, sw=2.4, tl=0.12))
  g.add(self._arr([xb - 0.30, yt - 0.27, 0], [(xa + xb) / 2 + 0.50, yb + 0.25, 0],
                  DIM, sw=2.4, tl=0.12))
  g.add(self._sym(yt + 0.02, "∧", ACCENT_A, FS_TAG, x=(xa + xb) / 2, w=0.34))
  g.add(self._sym(-0.74, "v̄  ∧  ȳ   =   f v̄ ( ȳ )  ·  ū", ACCENT_A, FS_TAG - 2,
                  x=-4.25, w=3.00))
  g.add(self._table((("v̄  ∈  𝒜 q        ȳ  ∈  𝒜 ⁿ ⁻ q", ACCENT_B),
                     ("v̄  ∧  ȳ   ∈   𝒜 ⁿ        dim   =   1", ACCENT_A),
                     ("v̄  ∧  ȳ   =   f v̄ ( ȳ )  ū        f v̄   ∈   ( 𝒜 ⁿ ⁻ q ) *", DIM),
                     ("det  (  ,  )   ≠   0        :        𝒜 ⁿ ⁻ q", ACCENT_C),
                     ("⇒   ∃ !   ∗ v̄        (  ȳ  ,  ∗ v̄  )   =   f v̄ ( ȳ )", ACCENT_A),
                     (f"(  ȳ  ,  ∗ v̄  )  ū   =   v̄  ∧  ȳ        | Δ |  ≤  "
                      f"{ms(DEF_ERR, '.1e')}", ACCENT_B)),
                    y0=0.90, dy=0.26))
  g.add(self._cap("最後一列是把定義式在每一對基底元素上都驗過一次",
                  "the last row checks the defining identity on every pair of basis elements"))
  return g.add(self._foot(
   "有了定向就能定義星算子。拿一個 q 次的元素去楔一個 n 減 q 次的，結果落在那個一維空間裡，所以它就是一個數乘上選定的那個基準元素，而且對後者是線性的",
   "with an orientation fixed the star can be defined: wedging a q-vector against an (n minus q)-vector lands in that one-dimensional space, so it is a number times the chosen element, and linearly so",
   ACCENT_A,
   "而 n 減 q 次那一層上的純量積是非退化的，所以那個線性泛函一定是「與某個唯一元素作內積」。那個唯一的元素就定義成 v 的星。整句話就是公式 9.2",
   "and the product on the complementary power is nondegenerate, so that linear functional has to be the product against one unique element -- that element is defined to be the star of v, which is all formula 9.2 says",
   ))

 # ── beat 7: the star on the basis ───────────────────────────────
 def _vanish(self):
  g = VGroup()
  g.add(self._sym(0.94, "ū ᵢ   ∧   ū ⱼ", ACCENT_A, FS_TAG - 1, x=-4.25, w=2.20))
  i0, j0 = I2[0], I2[3]        # (1 2) and (2 3): exactly one index in common
  g.add(self._sym(0.52, f"i   =   ( {' '.join(str(r + 1) for r in i0)} )        "
                        f"j   =   ( {' '.join(str(r + 1) for r in j0)} )",
                  WARN, FS_TAG - 3, x=-4.25, w=3.00))
  g.add(self._sym(0.14, "i  ∩  j   ≠   ∅        ⇒        0", WARN, FS_TAG - 3,
                  x=-4.25, w=3.00))
  i1 = I2[0]
  j1 = tuple(sorted(set(range(N)) - set(i1)))
  g.add(self._sym(-0.26, f"i   =   ( {' '.join(str(r + 1) for r in i1)} )        "
                         f"j   =   ( {' '.join(str(r + 1) for r in j1)} )",
                  ACCENT_B, FS_TAG - 3, x=-4.25, w=3.00))
  g.add(self._sym(-0.64, f"ū ᵢ  ∧  ū ⱼ   =   ε  ū        ε   =   "
                         f"{ms(sgn_seq(list(i1) + list(j1)), '+.0f')}",
                  ACCENT_A, FS_TAG - 3, x=-4.25, w=3.00))
  g.add(self._table((("ū ᵢ  ∧  ū ⱼ   =   0        ⟺        i  ∩  j   ≠   ∅", ACCENT_A),
                     ("i  ∩  j   =   ∅   ⇒   ū ᵢ ∧ ū ⱼ   =   ε k  ū", ACCENT_A),
                     ("ε k   =   sgn  k            k   =   (  i  ,  j  )", ACCENT_C),
                     (f"q   =   {Q}        n  −  q   =   {N - Q}", DIM),
                     (f"#  ( i , j )                        {TOTAL}", ACCENT_B),
                     (f"ū ᵢ ∧ ū ⱼ  =  0                {VANISH}", WARN),
                     (f"ū ᵢ ∧ ū ⱼ  ≠  0                {TOTAL - VANISH}", ACCENT_B)),
                    y0=0.90, dy=0.24))
  g.add(self._cap("三十六對裡只有六對不是零，就是互補的那六對",
                  "of the thirty-six pairs only six are nonzero: the complementary ones"))
  return g.add(self._foot(
   "要把星算出來，先看它在基底上的樣子。兩個指標組只要有一個共同的指標，楔起來就是零——那是上一集「因式重複就是零」的直接後果",
   "working the star out starts on the basis: if two index tuples share even one index their wedge is zero, which is last episode's repeated-factor rule applied directly",
   ACCENT_A,
   "沒有共同指標就表示它們剛好互補，楔起來等於那個基準元素乘上把兩串接起來之後排序所需的正負號。所以每個基底元素的星，只會落在互補的那一個基底元素上",
   "no shared index means they are exactly complementary, and the wedge is the chosen element times the sign of the shuffle that sorts the two tuples concatenated, so each basis element's star sits on the complementary one alone",
   ))

 # ── beat 8: (9.3), two computations compared ────────────────────
 def _compare(self):
  g = VGroup()
  g.add(self._sym(0.96, "∗  ū ᵢ   =   ±  ε  ū ⱼ", ACCENT_A, FS_TAG - 1, x=-4.25, w=2.60))
  for k, (i, j, eps, c) in enumerate(STARTAB[:4]):
   g.add(self._sym(0.52 - k * 0.34,
                   f"( {' '.join(str(r + 1) for r in i)} )   →   "
                   f"( {' '.join(str(r + 1) for r in j)} )        "
                   f"{ms(c, '+.0f')}",
                   WARN if c < 0 else ACCENT_B, FS_TAG - 3, x=-4.40, w=3.00))
  g.add(self._sym(-0.92, f"| Δ |   ≤   {ms(STAR_ERR, '.1e')}", ACCENT_A,
                  FS_TAG - 3, x=-4.40, w=3.00))
  rows = [("      i            j            ε            ∗  ū ᵢ", DIM)]
  for i, j, eps, c in STARTAB:
   rows.append((f"  ( {' '.join(str(r + 1) for r in i)} )        "
                f"( {' '.join(str(r + 1) for r in j)} )        "
                f"{ms(eps, '+.0f')}        {ms(c, '+.0f')}",
                WARN if c < 0 else ACCENT_B))
  rows.append((f"( 9.2 )   vs   ( 9.3 )            {ms(STAR_ERR, '.1e')}", ACCENT_C))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.21, size=FS_TAG - 5))
  g.add(self._cap("第三欄與第四欄不是同一串數字，差的就是 8.3 那一列的正負號",
                  "the third and fourth columns are not the same numbers: they differ by the signs of 8.3"))
  return g.add(self._foot(
   "公式 9.3 把星在基底上寫死：送到互補的那個基底元素，係數是接起來排序的正負號，再配上 8.3 裡那個元素的正負號。右表第三欄是前者、第四欄是兩者的乘積",
   "formula 9.3 pins the star down on the basis: it goes to the complementary element, with the shuffle sign times the sign that element carries in 8.3 -- the table's third column is the first of those and the fourth is the product",
   ACCENT_A,
   "這一拍是整集唯一真正的保證：螢幕上的星是用公式 9.2 去解那個定義式解出來的，而對照用的是照公式 9.3 把正負號讀出來、完全不解方程的另一支實作，兩者逐格相同",
   "this beat is the episode's one real guarantee: the star on screen is obtained by solving the defining identity of 9.2, while the comparison reads the signs off 9.3 and solves nothing, and the two agree entry by entry",
   ))

 # ── beat 9: (9.4) ───────────────────────────────────────────────
 def _twice(self):
  g = VGroup()
  xa, xb, xc = -5.50, -4.25, -3.00
  for x, lab, col in ((xa, "𝒜 q", ACCENT_B), (xb, "𝒜 ⁿ ⁻ q", ACCENT_C),
                      (xc, "𝒜 q", ACCENT_B)):
   g.add(self._box(x, 0.66, lab, col, w=1.10, h=0.46, size=FS_TAG - 2))
  g.add(self._arr([xa + 0.58, 0.66, 0], [xb - 0.58, 0.66, 0], ACCENT_A, sw=2.6, tl=0.12))
  g.add(self._arr([xb + 0.58, 0.66, 0], [xc - 0.58, 0.66, 0], ACCENT_A, sw=2.6, tl=0.12))
  g.add(self._sym(1.10, "∗", ACCENT_A, FS_TAG - 1, x=(xa + xb) / 2, w=0.34),
        self._sym(1.10, "∗", ACCENT_A, FS_TAG - 1, x=(xb + xc) / 2, w=0.34))
  g.add(self._sym(0.16, f"q ( n − q )  +  #   =   {Q} · {N - Q}  +  {HASH}   =   {DD_K}",
                  ACCENT_C, FS_TAG - 4, x=-4.25, w=3.20))
  g.add(self._sym(-0.24, f"∗  ∗  v̄   =   {ms(DD_PRED, '+.0f')}  v̄", ACCENT_A,
                  FS_TAG - 2, x=-4.25, w=2.80))
  g.add(self._sym(-0.64, f"| Δ |   ≤   {ms(DDERR, '.1e')}", ACCENT_B, FS_TAG - 3,
                  x=-4.25, w=2.80))
  g.add(self._sym(-0.98, "ū   ↦   −  ū        ⇒        ∗   ↦   −  ∗", DIM,
                  FS_TAG - 4, x=-4.25, w=3.20))
  rows = [("      q        q ( n − q )  +  #        ∗ ∗        | Δ |", DIM)]
  for q, k, s, e in DDQ:
   rows.append((f"      {q}                    {k}                "
                f"{ms(s, '+.0f')}        {ms(e, '.1e'):>9}",
                ACCENT_A if q == Q else (WARN if s < 0 else ACCENT_B)))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.23, size=FS_TAG - 5))
  g.add(self._cap("那一欄兩種正負號都出現，所以指數裡每一項都有在作用",
                  "both signs appear in that column, so every term of the exponent is doing work"))
  return g.add(self._foot(
   "公式 9.4 說星做兩次等於正負恆等，而那個號是負一的「q 乘 n 減 q，再加上井字號」次方。把 9.3 套兩次就看得出來：第一次把指標組換成補集、第二次換回來",
   "formula 9.4 says the star applied twice is plus or minus the identity, with exponent q times n minus q, plus the hash; applying 9.3 twice shows it, the first pass swapping the tuple for its complement and the second swapping back",
   ACCENT_A,
   "右表把五個 q 都驗過，正負兩種都出現，所以指數裡那兩項都不是裝飾。注意這整個算子依賴先前選的那個定向：換成另一個基準元素，星就整個變號，而做兩次的結果不變",
   "the table checks all five values of q and both signs occur, so neither term of the exponent is decoration; the whole operator depends on the orientation chosen earlier, and swapping it flips the star throughout while leaving star-twice alone",
   ))

 # ── beat 10: (9.5), and the end of the chapter ──────────────────
 def _preserve(self):
  g = VGroup()

  rows = [("        ū ᵢ                  (  v  ,  v  )        (  ∗ v  ,  ∗ v  )", DIM)]
  for i, a, b in FIVE_PAIRS:
   rows.append((f"  ( {' '.join(str(r + 1) for r in i)} )                "
                f"{ms(a, '+.0f')}                    {ms(b, '+.0f')}",
                WARN if a * b < 0 else ACCENT_B))
  rows.append((f"#   =   {HASH}        ( − 1 ) ^ #   =   {ms((-1.0) ** HASH, '+.0f')}",
               ACCENT_C))
  rows.append((f"| Δ |   ≤   {ms(FIVE_ERR, '.1e')}", ACCENT_A))
  rows.append(("§ 7.9      ⇒      § 8.1", DIM))
  g.add(self._table(tuple(rows), y0=0.90, dy=0.24, size=FS_TAG - 5))
  for k, (i, a, b) in enumerate(FIVE_PAIRS):
   y = 0.46 - k * 0.40
   g.add(self._sym(y, f"( {' '.join(str(r + 1) for r in i)} )", ACCENT_B,
                   FS_TAG - 3, x=-5.55, w=0.90))
   g.add(self._sym(y, ms(a, "+.0f"), WARN if a < 0 else ACCENT_B, FS_TAG - 2,
                   x=-4.60, w=0.60))
   g.add(self._arr([-4.30, y, 0], [-3.80, y, 0], DIM, sw=2.2, tl=0.11))
   g.add(self._sym(y, ms(b, "+.0f"), WARN if b < 0 else ACCENT_B, FS_TAG - 2,
                   x=-3.45, w=0.60))
  g.add(self._sym(-0.78, f"( − 1 ) ^ #   =   {ms((-1.0) ** HASH, '+.0f')}", ACCENT_A,
                  FS_TAG - 3, x=-4.40, w=2.40))
  g.add(self._cap("左邊三對的兩個數都差一個負號，因為井字號是奇數",
                  "all three pairs on the left differ by a sign, because the hash is odd"))
  return g.add(self._foot(
   "最後一條是公式 9.5：星保持純量積，只差負一的井字號次方。推法是把 9.2 用兩次再配上 9.4，左右各換一次邊，兩個負號湊起來剛好只剩井字號那一個",
   "the last identity is formula 9.5: the star preserves the scalar product up to minus one to the hash, which follows from using 9.2 twice and then 9.4, the two signs combining to leave only the hash behind",
   ACCENT_A,
   "這一集取的井字號是奇數，所以左邊三對的兩個數都真的差一個負號，不是巧合地相等。第 7 章到此結束，整章一題習題也沒有；下一章是積分",
   "the hash here is odd, so all three pairs really do differ by a sign rather than coincidentally agreeing; chapter 7 ends here, with no exercises anywhere in it, and the next chapter is integration",
   ))

 def stage(self):
  a, b, c = self._form(), self._power(), self._basis()
  d, e, f_ = self._orthogonal(), self._top(), self._orient()
  h, i, j = self._define(), self._vanish(), self._compare()
  k, l = self._twice(), self._preserve()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE90ZH, AdvCalcE90EN = make(AdvCalcE90Base, "90", prefix="AdvCalcE")
