"""advcalc E55 -- chapter 3, section 17 (book pp. 191-194): higher order
differentials and the Taylor formula.  The differential of the differential of
the differential, and so on without limit; each nth differential is a symmetric
n-linear map, it equals the nested directional derivative, and along a line the
whole thing collapses to the one-variable Taylor formula.  Multi-index notation
compresses the coordinate form, and the section closes with the classes C k and
C infinity.  Section 17 has no exercises, and chapter 3 ends on page 194.

The verification is built on the fact that F restricted to a line is a
polynomial in t whenever F is a polynomial.  Its Taylor coefficients are then
recovered exactly by fitting five sample values, with no truncation error at
all, and from those every claim of the episode becomes checkable: the nested
directional derivatives against the multilinear formula, the symmetry of the
third differential under all six permutations, and -- the sharpest of them --
the mean-value form of the remainder, whose unknown interior point is solved for
and asserted to lie strictly between zero and one.  The book's own example,
the expansion of the sine of x plus y squared, is checked by watching its error
fall by a factor of a hundred and twenty eight when the scale is halved.
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


def _F(v):
 """A quartic, so every restriction to a line is a quartic in t."""
 x, y = v
 return x ** 3 * y + x * y ** 3 - 2 * x * x + 5.0


APT = (0.60, -0.40)
ETA = (0.50, 0.80)


def _solve(a, b):
 """Gaussian elimination with partial pivoting, for the fit below."""
 n = len(b)
 m = [list(row) + [b[i]] for i, row in enumerate(a)]
 for c in range(n):
  piv = max(range(c, n), key=lambda i: abs(m[i][c]))
  m[c], m[piv] = m[piv], m[c]
  for i in range(n):
   if i != c:
    f = m[i][c] / m[c][c]
    m[i] = [u - f * w for u, w in zip(m[i], m[c])]
 return [m[i][n] / m[i][i] for i in range(n)]


def _line_coeffs(a, eta, deg=4):
 """The exact Taylor coefficients of t -> F(a + t eta), which is a polynomial."""
 ts = [-2.0, -1.0, 0.0, 1.0, 2.0][:deg + 1]
 rows = [[t ** j for j in range(deg + 1)] for t in ts]
 vals = [_F(tuple(x + t * d for x, d in zip(a, eta))) for t in ts]
 return _solve(rows, vals)


COEF = _line_coeffs(APT, ETA)
for _t in (0.3, -0.7, 1.4):
 _lam = sum(c * _t ** j for j, c in enumerate(COEF))
 assert abs(_lam - _F(tuple(x + _t * d for x, d in zip(APT, ETA)))) < 1e-9, \
     "the fit is not reproducing the restriction, so it is not a quartic after all"

# lambda^(j)(0) = j! c_j, which is the jth directional derivative along eta
DIRPOW = [math.factorial(j) * COEF[j] for j in range(5)]


# ── beat 2: nested directional derivatives, three different directions ─
XI = ((1.0, 0.0), (0.0, 1.0), (0.7, -0.3))


def _nested(dirs, a, h=1e-2):
 """Apply one central difference per direction, outermost last."""
 def rec(k, p):
  if k == len(dirs):
   return _F(p)
  u = dirs[k]
  hi = tuple(x + h * d for x, d in zip(p, u))
  lo = tuple(x - h * d for x, d in zip(p, u))
  return (rec(k + 1, hi) - rec(k + 1, lo)) / (2 * h)
 return rec(0, a)


def _d3(u, v, w, a=APT):
 """The third differential in closed form, from the partials of this quartic."""
 x, y = a
 t = {(0, 0, 0): 6 * y, (0, 0, 1): 6 * x, (0, 1, 1): 6 * y, (1, 1, 1): 6 * x}
 def coeff(i, j, k):
  return t[tuple(sorted((i, j, k)))]
 return sum(u[i] * v[j] * w[k] * coeff(i, j, k)
            for i in range(2) for j in range(2) for k in range(2))


PERMS = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))
D3_VALS = [_d3(XI[p[0]], XI[p[1]], XI[p[2]]) for p in PERMS]
assert max(D3_VALS) - min(D3_VALS) < 1e-9, "the third differential is not symmetric"
NESTED3 = _nested(XI, APT)
assert abs(NESTED3 - D3_VALS[0]) < 1e-6, \
    "the nested directional derivative is not the third differential"


# ── beats 5 and 6: Taylor, and the interior point of the remainder ─────
M_ORDER = 2
TRUNC = sum(DIRPOW[j] / math.factorial(j) for j in range(M_ORDER + 1))
EXACT = _F(tuple(x + d for x, d in zip(APT, ETA)))
REMAIN = EXACT - TRUNC
# lambda'''(t) = 6 c3 + 24 c4 t, so the remainder fixes k
K_POINT = (REMAIN - COEF[3]) / (4 * COEF[4])
assert 0.0 < K_POINT < 1.0, \
    "the mean value form needs an interior point, and this one is not interior"
_check = sum(DIRPOW[j] / math.factorial(j) for j in range(M_ORDER + 1)) \
    + (6 * COEF[3] + 24 * COEF[4] * K_POINT) / math.factorial(M_ORDER + 1)
assert abs(_check - EXACT) < 1e-9, "the remainder with that k does not close the identity"


# ── beat 8: the multi-index count ──────────────────────────────────────
def _multinomials(n, m):
 """The coefficients of the mth term, summed: they have to come to n to the m."""
 total = 0
 def walk(rest, left, acc):
  nonlocal total
  if rest == 1:
   acc = acc + [left]
   total += math.factorial(m) // math.prod(math.factorial(k) for k in acc)
   return
  for k in range(left + 1):
   walk(rest - 1, left - k, acc + [k])
 walk(n, m, [])
 return total


for _n, _m in ((2, 3), (3, 2), (2, 4)):
 assert _multinomials(_n, _m) == _n ** _m, "the multi-index coefficients do not sum right"
MULTI = [(2, 3, _multinomials(2, 3)), (3, 2, _multinomials(3, 2)), (2, 4, _multinomials(2, 4))]


# ── beat 9: the book's own example ─────────────────────────────────────
def _sinexp(x, y):
 return (x + y * y - x ** 3 / 6 - x * x * y * y / 2
         + (x ** 5 / 120 - x * y ** 4 / 2)
         + (x ** 4 * y * y / 24 - y ** 6 / 6))


ERRS = []
for _s in (0.40, 0.20, 0.10, 0.05):
 _e = abs(math.sin(_s + _s * _s) - _sinexp(_s, _s))
 ERRS.append((_s, _e))
RATIOS = [a[1] / b[1] for a, b in zip(ERRS, ERRS[1:])]
for _r in RATIOS:
 assert 100.0 < _r < 160.0, \
     "halving the scale should divide the error by about 128, since degree seven is the first missing"


class AdvCalcE55Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 55

 MODE_LABEL = {
  0: {"zh": "一直往上疊", "en": "stacking upward"},
  1: {"zh": "n 階微分是對稱的 n 重線性映射", "en": "symmetric n-linear"},
  2: {"zh": "就是連續 n 次方向導數", "en": "the nested directional derivative"},
  3: {"zh": "座標下的多重求和", "en": "the multiple sum in coordinates"},
  4: {"zh": "沿一條直線走", "en": "along one line"},
  5: {"zh": "一般的 Taylor 公式", "en": "the general Taylor formula"},
  6: {"zh": "餘項落在中間某一點", "en": "the remainder sits between"},
  7: {"zh": "m = n = 2 的樣子", "en": "the case m equals n equals two"},
  8: {"zh": "多重指標記號", "en": "multi-index notation"},
  9: {"zh": "實際上不這樣算", "en": "nobody computes it this way"},
  10: {"zh": "C 上標 k 與 C 無窮", "en": "the classes C k and C infinity"},
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

 # ── beats ─────────────────────────────────────────────────────────
 def _stack(self):
  g = VGroup()
  rows = (("F   :   A   →   W", ACCENT_B),
          ("dF   :   A   →   Hom ( V , W )", ACCENT_C),
          ("d ² F   :   A   →   Hom ² ( V , W )", WARN),
          ("d ³ F   :   A   →   Hom ³ ( V , W )", ACCENT_A))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.82 - k * 0.52, lab, col, FS_TAG, x=-3.55, w=5.20))
   if k:
    g.add(self._arr([-5.85, 1.08 - k * 0.52, 0], [-5.85, 0.98 - k * 0.52, 0],
                    DIM, sw=1.6, tl=0.08))
  g.add(self._sym(-1.02, "⋮", DIM, FS_TAG, x=-3.55, w=0.60))
  g.add(self._panel(((0.86, "每一層都是「上一層的微分」",
                      "each row is the differential of the one above", ACCENT_C),
                     (0.20, "值落的空間一層比一層高",
                      "and the space it lands in climbs one level each time", WARN),
                     (-0.46, "這個動作沒有上限",
                      "the move has no ceiling", ACCENT_A))))
  return g.add(self._foot("第 17 節是第 3 章的最後一節，做的就是把上一集那一步一直重複下去",
                          "section 17 closes chapter 3, and all it does is repeat the last episode's step",
                          ACCENT_A,
                          "Hom 的上標就是重數：Hom 二次方是雙線性映射，三次方是三重線性",
                          "the exponent on Hom is the arity: squared means bilinear, cubed means trilinear"))

 def _symmetric(self):
  g = VGroup()
  rows = [("        ( i , j , k )              d ³ F ( ξ ᵢ , ξ ⱼ , ξ ₖ )", DIM)]
  for p, v in zip(PERMS, D3_VALS):
   rows.append((f"        ( {p[0]+1} , {p[1]+1} , {p[2]+1} )                {v:.6f}", ACCENT_C))
  g.add(self._table(rows, x=-3.55, w=5.30, y0=0.86, dy=0.30))
  g.add(self._panel(((0.86, "三個方向的六種排法",
                      "the six orders of three directions", ACCENT_B),
                     (0.20, "六個值完全相同",
                      "all six values agree exactly", ACCENT_C),
                     (-0.46, "n 階微分是對稱的 n 重線性映射",
                      "the nth differential is a symmetric n-linear map", ACCENT_A))))
  return g.add(self._foot("上一集證了二階的對稱，往上是用歸納法推的——書上把那個證明省略了",
                          "the last episode proved symmetry for order two; higher orders go by induction, and the book omits it",
                          ACCENT_A,
                          "表格是程式在一個具體的四次多項式上算的，六個排列逐一算過",
                          "the table was computed here on a concrete quartic, one row per permutation"))

 def _nesteddir(self):
  g = VGroup()
  g.add(self._rect(-3.55, 0.56, 2.55, 0.32, ACCENT_A),
        self._sym(0.56, "D ξ ₁  D ξ ₂  D ξ ₃  F ( α )    =    d ³ F ₐ ( ξ ₁ , ξ ₂ , ξ ₃ )",
                  ACCENT_A, FS_TAG, x=-3.55, w=4.90))
  rows = [(f"    D ξ ₁ D ξ ₂ D ξ ₃ F              {NESTED3:.6f}", ACCENT_B),
          (f"    d ³ F ₐ ( ξ ₁ , ξ ₂ , ξ ₃ )        {D3_VALS[0]:.6f}", ACCENT_C)]
  g.add(self._table(rows, x=-3.55, w=5.30, y0=-0.06, dy=0.40))
  g.add(self._panel(((0.86, "從最左邊那一項出發",
                      "start from the leftmost term", ACCENT_B),
                     (0.20, "反覆用取值映射與合成規則",
                      "and repeat the evaluation map with the composite rule", ACCENT_C),
                     (-0.46, "上一集那條二階的結果就這樣往上推",
                      "that lifts the last episode's second-order result", ACCENT_A))))
  return g.add(self._foot("上面那個數字是三重的中央差商，下面那個是用偏導數寫出來的封閉形式",
                          "the upper number is a threefold central difference and the lower one a closed form in the partials",
                          ACCENT_A,
                          "兩種算法完全不同，六位小數相同",
                          "two entirely different computations, agreeing to six places"))

 def _coords(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.52, 2.65, 0.32, ACCENT_B),
        self._sym(0.52, "d ᵐ F ₐ ( c ¹ , … , c ᵐ )   =   Σ  c ¹ ᵢ … c ᵐ ⱼ  ∂ ᵐ F / ∂x ᵢ … ∂x ⱼ",
                  ACCENT_B, FS_TAG - 2, x=-3.45, w=5.10))
  g.add(self._rect(-4.75, -0.36, 1.35, 0.30, ACCENT_C),
        self._sym(-0.36, "∂ ᵐ F / ∂x ᵢ … ∂x ⱼ   ∈   C ⁰", ACCENT_C, FS_TAG - 2,
                  x=-4.75, w=2.50))
  g.add(self._arr([-3.30, -0.36, 0], [-2.85, -0.36, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._rect(-1.65, -0.36, 1.05, 0.30, WARN),
        self._sym(-0.36, "d ᵐ F   ∈   C ⁰", WARN, FS_TAG - 1, x=-1.65, w=1.90))
  g.add(self._panel(((0.86, "跟第 9 節與上一集同一個模式",
                      "the same pattern as section 9 and the last episode", ACCENT_C),
                     (0.20, "m 階偏導數存在而且連續",
                      "the mth partials exist and are continuous", ACCENT_B),
                     (-0.46, "等價於到 m 階為止的微分都連續",
                      "exactly when the differentials through order m are", WARN))))
  return g.add(self._foot("求和跑遍 m 個指標，每個指標從一跑到 n，所以總共 n 的 m 次方項",
                          "the sum runs over m indices each from one to n, so it has n to the m terms",
                          ACCENT_A,
                          "這也就是為什麼第 8 拍要換一套記號：這些項裡有大量重複的",
                          "which is why beat eight changes notation: a great many of those terms repeat"))

 def _alongline(self):
  ox, oy = -5.75, -0.30
  sx, sy = 4.20, 0.42
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.60, 0], [ox, oy + 1.30, 0], color=DIM, stroke_width=1.4))
  lam = lambda t: sum(c * t ** j for j, c in enumerate(COEF))
  g.add(self._curve([[ox + sx * (k / 60.0), oy + sy * (lam(k / 60.0) - lam(0.0)) + 0.30, 0]
                     for k in range(61)], ACCENT_B, sw=2.8))
  g.add(Dot([ox, oy + 0.30, 0], radius=0.065, color=WARN),
        Dot([ox + sx, oy + sy * (lam(1.0) - lam(0.0)) + 0.30, 0], radius=0.065, color=WARN))
  g.add(self._sym(0.86, "λ ( t )   =   F ( α  +  t η )", ACCENT_B, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._sym(0.24, "d ʲ λ / d t ʲ   =   ( D η ) ʲ F ( α + t η )", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "把多變數的問題壓成一元的",
                  "the many variable question is squashed into one variable", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "j 等於一那一步就是定理 7.2，其餘用歸納",
                  "the case j equal to one is Theorem 7.2 and the rest is induction", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這是這一章從頭到尾最常用的一招：沿一條射線走，把問題交給一元微積分",
                          "this is the chapter's most used move: walk along a ray and hand the problem to one variable calculus",
                          ACCENT_A,
                          "畫面上那條就是這一集用的四次多項式限制到一條直線之後的樣子",
                          "the curve is this episode's quartic restricted to one line"))

 def _taylor(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.60, 2.75, 0.32, ACCENT_A),
        self._sym(0.60, "F ( α + η )  =  F ( α ) + D η F ( α ) + … + ( 1 / m ! ) D η ᵐ F ( α ) + R",
                  ACCENT_A, FS_TAG - 3, x=-3.45, w=5.30))
  rows = [(f"        j            ( 1 / j ! )  D η ʲ F ( α )", DIM)]
  for j in range(3):
   rows.append((f"        {j}                    {DIRPOW[j] / math.factorial(j):+.6f}",
                (ACCENT_B, ACCENT_C, WARN)[j]))
  rows.append((f"        R                    {REMAIN:+.6f}", ACCENT_A))
  g.add(self._table(rows, x=-3.45, w=5.30, y0=0.10, dy=0.26))
  return g.add(self._foot("λ 是一元的實值函數，所以一元的 Taylor 公式直接可用；取 t 等於一再代回去就是這條",
                          "lambda is a real function of one variable, so the ordinary Taylor formula applies; put t equal to one",
                          ACCENT_A,
                          f"表格是 m 等於 {M_ORDER} 的情形，四個數字相加正好是 F 在 α 加 η 的值",
                          f"the table is the case m equal to {M_ORDER}, and the four numbers add to the value at alpha plus eta"))

 def _remainder(self):
  ox, oy = -5.55, -0.20
  sx = 4.00
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=DIM, stroke_width=2))
  for t, lab, col in ((0.0, "0", ACCENT_B), (1.0, "1", ACCENT_C)):
   g.add(Dot([ox + sx * t, oy, 0], radius=0.07, color=col),
         self._sym(oy - 0.34, lab, col, FS_TAG, x=ox + sx * t, w=0.60))
  g.add(Dot([ox + sx * K_POINT, oy, 0], radius=0.08, color=WARN),
        self._sym(oy + 0.34, f"k  =  {K_POINT:.4f}", WARN, FS_TAG, x=ox + sx * K_POINT, w=1.80))
  g.add(self._sym(0.86, "R   =   ( 1 / ( m + 1 ) ! )   d ᵐ ⁺ ¹ F ( η , … , η )",
                  ACCENT_A, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "餘項在 α 與 α 加 η 之間某一點取值",
                  "the remainder is evaluated somewhere between the two ends", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "程式把那個 k 解出來了",
                  "that interior point was solved for here", WARN, FS_TAG,
                  x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "它確實落在零與一之間",
                  "and it does lie strictly between zero and one", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("均值形式只說「存在一個 k」，不說是哪一個；這個例子的 λ 是四次多項式，所以解得出來",
                          "the mean value form only promises some k; here lambda is a quartic, so the k can be solved for",
                          ACCENT_A,
                          "解出來之後把它代回去，等式兩邊到小數點後九位完全相同",
                          "substituting it back closes the identity to nine decimal places"))

 def _twovar(self):
  g = VGroup()
  g.add(self._rect(-3.45, 0.42, 2.75, 0.34, ACCENT_A),
        self._sym(0.42, "( 1 / 2 ! ) D ₛ ² F ( a )  =  ½ [ s ² F ₓₓ  +  2 s t F ₓᵧ  +  t ² F ᵧᵧ ]",
                  ACCENT_A, FS_TAG - 2, x=-3.45, w=5.30))
  g.add(self._sym(-0.34, "( 1 / m ! )  ( Σ ᵢ  y ᵢ  ∂ / ∂x ᵢ ) ᵐ  F ( a )", ACCENT_C,
                  FS_TAG, x=-3.45, w=4.60))
  g.add(self._panel(((0.86, "一般項就是「求和符號的 m 次方」",
                      "the general term is the mth power of a sum of partials", ACCENT_C),
                     (0.20, "m 與 n 都等於二時展開就是上面那一行",
                      "expanding it for m and n both two gives the line above", ACCENT_A),
                     (-0.46, "中間那個 2 是因為混合的兩項相同",
                      "the two in the middle is because the mixed terms coincide", WARN))))
  return g.add(self._foot("那個 2 正是「重複項」的來源：s t 與 t s 給出同一個混合偏導數",
                          "that two is exactly where the repeats come from: s t and t s give one mixed partial",
                          ACCENT_A,
                          "上一集的定理 16.3 保證混合偏導數可交換，所以才能併成一項",
                          "the last episode's Theorem 16.3 is what lets the two be merged into one"))

 def _multiindex(self):
  g = VGroup()
  rows = (("| k |   =   Σ  k ᵢ                x ᵏ   =   x ₁ ᵏ ¹ … x ₙ ᵏ ⁿ", ACCENT_B),
          ("D ᵏ F   =   D ₁ ᵏ ¹ … D ₙ ᵏ ⁿ F              k !   =   k ₁ ! … k ₙ !", ACCENT_C))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.86 - k * 0.46, lab, col, FS_TAG - 2, x=-3.45, w=5.30))
  g.add(self._rect(-3.45, 0.00, 2.35, 0.26, WARN),
        self._sym(0.00, "( 1 / m ! )   Σ | k | = m   ( m ,  k )   D ᵏ F ( a )   x ᵏ",
                  WARN, FS_TAG - 2, x=-3.45, w=4.50))
  # only two of the three checked cases are shown; a fourth row would reach the
  # first footer line
  rows2 = [("      n      m      Σ ( m , k )        n ᵐ", DIM)]
  for n, m, tot in MULTI[:2]:
   rows2.append((f"      {n}      {m}          {tot}            {n ** m}", ACCENT_A))
  g.add(self._table(rows2, x=-3.45, w=5.00, y0=-0.42, dy=0.26))
  return g.add(self._foot("多重指標把整個第 m 項縮成一行——書上說這是「記號上的勝利」",
                          "multi-index notation compresses the whole mth term into one line, which the book calls a notational triumph",
                          ACCENT_A,
                          "表格驗的是那些係數加起來正好是 n 的 m 次方，也就是原來那個展開的項數",
                          "the table checks that the coefficients sum to n to the m, the number of terms in the original expansion"))

 def _practice(self):
  g = VGroup()
  g.add(self._sym(0.80, "sin ( x + y ² )   =   ( x + y ² )  −  ( x + y ² ) ³ / 3 !  +  …",
                  ACCENT_B, FS_TAG - 1, x=-3.45, w=5.30),
        self._sym(0.26, "=   x + y ² − x ³ / 3 ! − x ² y ² / 2 + ( x ⁵ / 5 ! − x y ⁴ / 2 ) + …",
                  ACCENT_C, FS_TAG - 2, x=-3.45, w=5.30))
  # the last column used to be headed "ratio", which is English in a row that
  # renders the same in both languages
  rows = [("        s          | sin − P |          ÷", DIM)]
  for k in range(1, len(ERRS)):
   s_, e_ = ERRS[k]
   rows.append((f"      {s_:.2f}        {e_:.3e}        {RATIOS[k - 1]:.0f}", WARN))
  g.add(self._table(rows, x=-3.45, w=5.30, y0=-0.16, dy=0.28))
  return g.add(self._foot("書上說一般的 Taylor 公式太笨重，主要是理論上的價值；實際的展開是把多項式代進冪級數",
                          "the book calls the general formula too cumbersome to be of much use; real expansions come by substitution",
                          ACCENT_A,
                          "尺度減半，誤差掉 128 倍——也就是 2 的 7 次方，因為第一個沒寫出來的項是七次",
                          "halving the scale divides the error by a hundred and twenty eight, two to the seventh, the first missing degree"))

 def _classes(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("C ᵏ  +  C ᵏ", ACCENT_B), ("C ᵏ  ∘  C ᵏ", ACCENT_C),
                                  ("C ᵏ  ·  C ᵏ", WARN), ("( C ᵏ ) ⁻¹", ACCENT_A))):
   g.add(self._rect(-5.15 + (k % 2) * 1.70, 0.52 - (k // 2) * 0.72, 0.72, 0.26, col),
         self._sym(0.52 - (k // 2) * 0.72, lab, col, FS_TAG - 1,
                   x=-5.15 + (k % 2) * 1.70, w=1.40))
  g.add(self._arr([-2.55, 0.16, 0], [-2.05, 0.16, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._rect(-1.25, 0.16, 0.85, 0.30, ACCENT_A),
        self._sym(0.16, "C ᵏ", ACCENT_A, FS_TAG + 2, x=-1.25, w=1.60))
  g.add(self._mid(-0.66, "對每個 k 都成立就叫 C 無窮",
                  "holding for every k is called C infinity", DIM, FS_TAG, x=-3.45, w=4.20))
  g.add(self._panel(((0.86, "C 上標 k 是一個向量空間",
                      "the class C k is a vector space", ACCENT_B),
                     (0.20, "合成、乘積都保持它",
                      "and composition and products preserve it", ACCENT_C),
                     (-0.46, "下一章會補上「取反元素」也保持",
                      "the next chapter adds that inversion preserves it too", ACCENT_A))))
  return g.add(self._foot("有了取反元素，隱函數定理交出來的那個函數也是同一類——因為它的微分是那些東西合成的",
                          "with inversion, the function the implicit function theorem hands back is of the same class",
                          ACCENT_A,
                          "第 3 章到此結束，書頁 194。下一集開第 4 章：緊緻性與完備性",
                          "that ends chapter 3, on page 194; next comes chapter 4, compactness and completeness"))

 def stage(self):
  a, b, c = self._stack(), self._symmetric(), self._nesteddir()
  d, e, f = self._coords(), self._alongline(), self._taylor()
  h, i, j = self._remainder(), self._twovar(), self._multiindex()
  k, l = self._practice(), self._classes()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE55ZH, AdvCalcE55EN = make(AdvCalcE55Base, "55", prefix="AdvCalcE")
