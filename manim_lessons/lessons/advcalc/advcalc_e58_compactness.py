"""advcalc E58 -- chapter 4, section 4 (book pp. 205-209): sequential
compactness.  Subsequences, the odd-sounding Lemma 4.1, the definition that
"creates convergence out of nothing", and then the chain that ends in Theorem
4.6 -- all norms on real n-space are equivalent -- which fills the one gap
chapter 3 left open when it needed that fact in section 4.  Pages 209-210 are
exercises 4.1 to 4.16.

Four beats are computed.  The peak-term construction of Lemma 4.4 is actually
run on a concrete bounded sequence, and the monotone subsequence it produces is
checked to be monotone; Bolzano-Weierstrass is exercised on a sequence with no
limit at all, by extracting a convergent subsequence from it.  The beat on why
compactness cannot be dropped computes the failure directly: two parameters near
the opposite ends of a half-open interval are shown to have nearly equal images
on the circle while staying far apart themselves.  And Theorem 4.6's two
constants are found by minimising and maximising a deliberately lopsided norm
over the unit sphere of the one-norm, then verified on samples.
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


# ── beats 7 and 8: peak terms, and a monotone subsequence ──────────────
def _seq(n):
 """Bounded, with no limit, and with a few peak terms near the start."""
 return math.sin(1.7 * n) + 1.5 / n


# Being a peak is a statement about the whole infinite tail, so the test runs
# against a long stretch of it; truncating too early would make the last term of
# the window a peak for no reason but the truncation.
LONG = [_seq(n) for n in range(1, 801)]
WINDOW = 40
TERMS = LONG[:WINDOW]
PEAKS = [i for i in range(WINDOW) if all(LONG[i] >= LONG[j] for j in range(i + 1, len(LONG)))]
assert 2 <= len(PEAKS) <= 6, "the beat needs a handful of visible peaks, and finitely many"

MONO_IDX = [PEAKS[-1] + 1]
for _j in range(PEAKS[-1] + 2, WINDOW):
 if LONG[_j] > LONG[MONO_IDX[-1]]:
  MONO_IDX.append(_j)
MONO = [LONG[i] for i in MONO_IDX]
assert len(MONO) >= 4, "the construction has to produce a usable subsequence"
assert all(a < b for a, b in zip(MONO, MONO[1:])), "the subsequence is not increasing"
assert max(abs(t) for t in LONG) < 3.0, "the sequence has to be bounded"
assert max(LONG[-200:]) - min(LONG[-200:]) > 1.5, "and it must not settle down to a limit"


# ── beat 6: dropping compactness breaks Theorem 4.2 ────────────────────
def _wrap(t):
 return (math.cos(t), math.sin(t))


NEAR = [(1e-3, 2 * math.pi - 1e-3), (1e-4, 2 * math.pi - 1e-4)]
GAPS = []
for _a, _b in NEAR:
 _img = math.hypot(_wrap(_a)[0] - _wrap(_b)[0], _wrap(_a)[1] - _wrap(_b)[1])
 GAPS.append((_a, _img, abs(_b - _a)))
for _t, _img, _dom in GAPS:
 assert _img < 1e-2 < 6.0 < _dom, \
     "the images have to be close while the parameters stay far apart"


# ── beat 10: Theorem 4.6's two constants, found on the unit one-sphere ─
def _n1(v):
 return abs(v[0]) + abs(v[1])


def _odd(v):
 """A deliberately lopsided norm, so the two constants are visibly different."""
 return math.sqrt(9.0 * v[0] ** 2 + 0.25 * v[1] ** 2 + 2.0 * v[0] * v[1])


SPHERE = []
for _k in range(4000):
 _t = 4.0 * _k / 4000 - 2.0
 for _s in (1.0, -1.0):
  _x = (_t, _s * (1.0 - abs(_t))) if abs(_t) <= 1.0 else None
  if _x:
   SPHERE.append(_x)
SPHERE = [v for v in SPHERE if abs(_n1(v) - 1.0) < 1e-9]
M_CONST = min(_odd(v) for v in SPHERE)
A_CONST = max(_odd(v) for v in SPHERE)
assert M_CONST > 0.0, "the minimum cannot be zero, since the sphere misses the origin"
assert A_CONST / M_CONST > 3.0, "the two constants should be visibly different"
for _v in ((1.3, -2.1), (0.0, 4.0), (-3.0, 0.5), (2.5, 2.5)):
 assert M_CONST * _n1(_v) <= _odd(_v) + 1e-9 <= A_CONST * _n1(_v) + 1e-9, \
     "the sandwich fails off the sphere, so homogeneity was misused"


class AdvCalcE58Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 58

 MODE_LABEL = {
  0: {"zh": "子序列", "en": "subsequences"},
  1: {"zh": "引理 4.1：一條看起來很怪的話", "en": "Lemma 4.1: an unlikely-sounding one"},
  2: {"zh": "無中生有地造出收斂", "en": "convergence out of nothing"},
  3: {"zh": "引理 4.2：又閉又有界", "en": "Lemma 4.2: closed and bounded"},
  4: {"zh": "最大最小值取得到", "en": "the extremes are attained"},
  5: {"zh": "定理 4.2：反函數也連續", "en": "Theorem 4.2: the inverse is continuous"},
  6: {"zh": "少了緊緻就不成立", "en": "without compactness it fails"},
  7: {"zh": "峰項", "en": "peak terms"},
  8: {"zh": "任何實數列都有單調子序列", "en": "every real sequence has a monotone one"},
  9: {"zh": "推到 ℝⁿ", "en": "lifting it to n dimensions"},
  10: {"zh": "定理 4.6：補上第 3 章的洞", "en": "Theorem 4.6: the gap is filled"},
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

 def _circ(self, cx, cy, r, col, sw=2.0, n=90):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _terms(self, ox, oy, sx, sy, vals, col, r=0.05, hot=(), hotcol=None):
  g = VGroup()
  n = len(vals)
  for i, v in enumerate(vals):
   c = (hotcol or col) if i in hot else col
   g.add(Dot([ox + sx * i / max(1, n - 1), oy + sy * v, 0], radius=r, color=c))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _subsequence(self):
  ox, oy = -5.85, 0.30
  sx = 4.40
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox - 0.10, oy - 0.90, 0], [ox + sx * 1.06, oy - 0.90, 0],
                  color=DIM, stroke_width=1.4))
  keep = (1, 3, 4, 7, 9, 12)
  for i in range(14):
   px = ox + sx * i / 13.0
   g.add(Dot([px, oy, 0], radius=0.06, color=WARN if i in keep else DIM))
  for j, i in enumerate(keep):
   px = ox + sx * i / 13.0
   qx = ox + sx * j / (len(keep) - 1.0)
   g.add(Dot([qx, oy - 0.90, 0], radius=0.06, color=WARN),
         self._arr([px, oy - 0.12, 0], [qx, oy - 0.78, 0], DIM, sw=1.2, tl=0.07))
  g.add(self._panel(((0.86, "從原來的序列裡挑出無窮多項",
                      "pick infinitely many terms out of the sequence", DIM),
                     (0.20, "按原來的順序排好",
                      "and keep them in their original order", WARN),
                     (-0.46, "正式一點就是接上一個嚴格遞增的指標函數",
                      "formally, compose with a strictly increasing index function", ACCENT_A))))
  return g.add(self._foot("書上提了一個好玩的觀察：任何零一序列都是零一零一那個序列的子序列",
                          "the book notes that any sequence of zeros and ones is a subsequence of zero one zero one",
                          ACCENT_A,
                          "如果原序列收斂，每一支子序列都收斂到同一點——這是習題 4.2",
                          "if the sequence converges every subsequence converges to the same point, which is exercise 4.2"))

 def _lemma41(self):
  ox, oy = -5.75, 0.05
  sx = 4.30
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  lim = ox + sx * 0.30
  g.add(Dot([lim, oy, 0], radius=0.075, color=ACCENT_A),
        self._sym(oy - 0.34, "a", ACCENT_A, FS_TAG, x=lim, w=0.60))
  g.add(self._dash([lim - 0.62, oy + 0.44, 0], [lim - 0.62, oy - 0.44, 0], WARN, n=6, sw=1.4),
        self._dash([lim + 0.62, oy + 0.44, 0], [lim + 0.62, oy - 0.44, 0], WARN, n=6, sw=1.4))
  for t in (0.62, 0.74, 0.83, 0.90, 0.95):
   g.add(Dot([ox + sx * t, oy + 0.24, 0], radius=0.055, color=WARN))
  g.add(self._panel(((0.86, "x_n 收斂不到 a",
                      "the terms do not converge to a", DIM),
                     (0.20, "那就挑得出一整支，每一項都離 a 至少 ε 遠",
                      "then a whole subsequence stays at least epsilon away", WARN),
                     (-0.46, "而那一支的任何子序列也收斂不到 a",
                      "and no subsequence of that one converges to a either", ACCENT_C))))
  return g.add(self._foot("反過來寫就是引理 4.1：每一支子序列都還有一支收斂到 a，那麼整個序列就收斂到 a",
                          "turned around that is Lemma 4.1: if every subsequence has a further one converging to a, the sequence does",
                          ACCENT_A,
                          "書上說這條「聽起來很怪」，可是下面證定理 4.2 時正好要用它",
                          "the book calls it wild and unlikely sounding, and then uses it to prove Theorem 4.2"))

 def _definition(self):
  cx, cy = -4.35, 0.05
  g = VGroup(self._blob(cx, cy, 1.25, 0.80, 0.13, ACCENT_B, sw=2.4))
  spots = ((-0.85, 0.35), (0.70, -0.42), (-0.20, 0.55), (0.95, 0.28),
           (-0.60, -0.45), (0.20, -0.10))
  for k, (dx, dy) in enumerate(spots):
   g.add(Dot([cx + dx, cy + dy, 0], radius=0.055, color=DIM))
  tgt = (0.20, -0.10)
  for dx, dy in ((-0.20, 0.55), (0.70, -0.42), (-0.60, -0.45)):
   g.add(self._arr([cx + dx, cy + dy, 0],
                   [cx + tgt[0] - 0.16 * (dx - tgt[0]), cy + tgt[1] - 0.16 * (dy - tgt[1]), 0],
                   WARN, sw=1.4, tl=0.08))
  g.add(Dot([cx + tgt[0], cy + tgt[1], 0], radius=0.075, color=ACCENT_A))
  g.add(self._panel(((0.86, "裡面的每一個序列",
                      "every sequence inside the set", DIM),
                     (0.20, "都有一支子序列收斂",
                      "has a subsequence that converges", WARN),
                     (-0.46, "而且極限也落在裡面",
                      "and the limit lies inside it too", ACCENT_A))))
  return g.add(self._foot("書上的話很傳神：這裡等於是無中生有地造出收斂",
                          "the book puts it well: here, so to speak, we create convergence out of nothing",
                          ACCENT_A,
                          "ℝⁿ 的有界閉集都是這樣的集合；無窮維時就罕見得多，可是一旦有就非常有用",
                          "bounded closed subsets of real n-space all are; in infinite dimensions it is far rarer and far more valuable"))

 def _closedbounded(self):
  g = VGroup()
  for k, (lab, col) in enumerate((("A  =  Ā", ACCENT_B), ("A  ⊂  B ᵣ ( b )", WARN))):
   g.add(self._rect(-2.15, 0.48 - k * 0.84, 1.25, 0.30, col),
         self._sym(0.48 - k * 0.84, lab, col, FS_TAG + 1, x=-2.15, w=2.30))
  g.add(self._rect(-4.95, 0.06, 0.85, 0.30, ACCENT_A),
        self._sym(0.06, "A  ∈  𝒦", ACCENT_A, FS_TAG + 1, x=-4.95, w=1.60))
  for k in range(2):
   g.add(self._arr([-4.00, 0.06, 0], [-3.55, 0.48 - k * 0.84, 0], ACCENT_A, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "閉：收斂序列的極限被子序列抓回集合裡",
                      "closed: a subsequence drags any limit back into the set", ACCENT_B),
                     (0.20, "有界：否則挑得出離某點越來越遠的點",
                      "bounded: else pick points ever further from a fixed one", WARN),
                     (-0.46, "而它的收斂子序列跟這件事矛盾",
                      "and a convergent subsequence of those contradicts it", ACCENT_C))))
  return g.add(self._foot("反過來在 ℝⁿ 上也成立，那是這一節最後要證的定理 4.5；一般的度量空間就不一定",
                          "the converse holds in real n-space, which is Theorem 4.5, but not in a general metric space",
                          ACCENT_A,
                          "𝒦 在這一集裡就是「序列緊緻的集合」的簡寫",
                          "here the script K is shorthand for the sequentially compact sets"))

 def _extremes(self):
  ox, oy = -5.75, -0.30
  sx, sy = 4.20, 0.62
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4))
  f = lambda t: 0.55 * math.sin(3.1 * t + 0.6) + 0.30 * math.cos(1.4 * t) + 0.70
  g.add(self._curve([[ox + sx * (k / 80.0), oy + sy * f(k / 80.0), 0] for k in range(81)],
                    ACCENT_B, sw=2.8))
  vals = [(k / 80.0, f(k / 80.0)) for k in range(81)]
  hi = max(vals, key=lambda p: p[1])
  lo = min(vals, key=lambda p: p[1])
  for t, v, col in ((hi[0], hi[1], WARN), (lo[0], lo[1], ACCENT_C)):
   g.add(Dot([ox + sx * t, oy + sy * v, 0], radius=0.075, color=col),
         self._dash([ox, oy + sy * v, 0], [ox + sx * t, oy + sy * v, 0], col, n=14, sw=1.1))
  g.add(Line([ox, oy - 0.12, 0], [ox, oy - 0.30, 0], color=ACCENT_A, stroke_width=4),
        Line([ox + sx, oy - 0.12, 0], [ox + sx, oy - 0.30, 0], color=ACCENT_A, stroke_width=4),
        Line([ox, oy - 0.21, 0], [ox + sx, oy - 0.21, 0], color=ACCENT_A, stroke_width=4))
  g.add(self._panel(((0.86, "定義域是緊緻的（畫面下方那一段）",
                      "the domain is compact, the segment along the bottom", ACCENT_A),
                     (0.20, "連續映射把緊緻集送成緊緻集",
                      "a continuous map carries compact sets to compact ones", ACCENT_B),
                     (-0.46, "而實數線上的緊緻集含著最大與最小元",
                      "and a compact subset of the line contains its extremes", WARN))))
  return g.add(self._foot("為什麼含著？上確界是集合裡某個序列的極限，而緊緻集是閉的，所以極限留在裡面",
                          "why? the least upper bound is a limit of points of the set, and a compact set is closed",
                          ACCENT_A,
                          "合起來就是那條熟悉的推論：連續函數在緊緻定義域上取得到最大與最小值",
                          "together that is the familiar corollary about a continuous function on a compact domain"))

 def _thm42(self):
  g = VGroup()
  rows = (("y ₙ   →   y", ACCENT_B),
          ("x ₙ ₍ ᵢ ₍ ⱼ ₎ ₎   →   z", ACCENT_C),
          ("f ( z )   =   y            z   =   x", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.80 - k * 0.58, lab, col, FS_TAG + 1, x=-3.55, w=4.60))
  g.add(self._rect(-3.55, -0.86, 2.05, 0.26, ACCENT_A),
        self._sym(-0.86, "f ⁻¹    ∈    C ⁰", ACCENT_A, FS_TAG, x=-3.55, w=3.90))
  g.add(self._panel(((0.86, "要證的是原像序列收斂",
                      "what has to be shown is that the preimages converge", ACCENT_B),
                     (0.20, "任取一支子序列，緊緻性給出再一支收斂的",
                      "take any subsequence and compactness gives a further convergent one", ACCENT_C),
                     (-0.46, "連續性逼出它的極限只能是那一點",
                      "and continuity forces its limit to be the right point", WARN))))
  return g.add(self._foot("到這裡引理 4.1 就登場了：每一支子序列都有一支收斂到同一點，所以整個序列收斂",
                          "and here Lemma 4.1 enters: every subsequence has a further one converging to the same point",
                          ACCENT_A,
                          "那條「聽起來很怪」的引理，唯一的用處就是把這個證明收乾淨",
                          "that unlikely-sounding lemma exists precisely to close this argument"))

 def _needcompact(self):
  ox, oy = -5.75, 0.05
  sx = 2.00
  g = VGroup(Line([ox, oy, 0], [ox + sx, oy, 0], color=ACCENT_B, stroke_width=5))
  g.add(Dot([ox, oy, 0], radius=0.075, color=ACCENT_C),
        self._circ(ox + sx, oy, 0.09, WARN, sw=2.2))
  cx, cy, r = -1.95, 0.05, 0.85
  g.add(self._circ(cx, cy, r, WARN, sw=2.4))
  g.add(Dot([cx + r, cy, 0], radius=0.075, color=ACCENT_A))
  for a, col in ((0.28, ACCENT_C), (-0.28, WARN)):
   g.add(Dot([cx + r * math.cos(a), cy + r * math.sin(a), 0], radius=0.055, color=col))
  g.add(self._arr([ox + sx + 0.30, oy, 0], [cx - r - 0.30, cy, 0], DIM, sw=2, tl=0.10))
  g.add(self._sym(-1.02, "[ 0 , 2 π )", ACCENT_B, FS_TAG - 1, x=ox + sx / 2, w=1.80),
        self._sym(-1.02, "S ¹", WARN, FS_TAG - 1, x=cx, w=1.20))
  g.add(self._panel(((0.86, "左邊少了右端點，所以不是緊緻的",
                      "the left segment misses its right end, so it is not compact", ACCENT_B),
                     (0.20, "映射連續，而且是雙射",
                      "the map is continuous and bijective", DIM),
                     (-0.46, "可是反函數在那一點不連續",
                      "yet the inverse is not continuous there", WARN))))
  return g.add(self._foot(f"程式算過：兩個參數差了 {GAPS[-1][2]:.3f}，可是它們的像只差 {GAPS[-1][1]:.5f}",
                          f"computed here: the two parameters differ by {GAPS[-1][2]:.3f} while their images differ by only {GAPS[-1][1]:.5f}",
                          ACCENT_A,
                          "所以緊緻這個假設不是裝飾品——少了它，定理 4.2 就是錯的",
                          "so compactness is no decoration: without it Theorem 4.2 is simply false"))

 def _peaks(self):
  ox, oy = -5.85, -0.10
  sx, sy = 4.40, 0.38
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  show = TERMS
  pk = set(PEAKS)
  g.add(self._terms(ox, oy, sx, sy, show, DIM, r=0.055, hot=pk, hotcol=WARN))
  for i in sorted(pk):
   px = ox + sx * i / (len(show) - 1.0)
   g.add(self._dash([px, oy + sy * show[i], 0], [px + sx * 0.10, oy + sy * show[i], 0],
                    WARN, n=4, sw=1.1))
  g.add(self._panel(((0.86, "紅色的是峰項",
                      "the red ones are the peak terms", WARN),
                     (0.20, "它大於等於它後面的每一項",
                      "each is at least as large as everything after it", ACCENT_C),
                     (-0.46, "這個序列只有有限多個峰項",
                      "this sequence has only finitely many of them", DIM))))
  return g.add(self._foot(f"程式拿前 {WINDOW} 項對著後面 800 項比，找到 {len(PEAKS)} 個峰項，所以走的是「有限多個」那一支",
                          f"testing the first {WINDOW} terms against eight hundred found {len(PEAKS)} peaks, so the finite branch applies",
                          ACCENT_A,
                          "峰項有無窮多個的話，它們本身就已經是一支遞減的子序列了",
                          "if there were infinitely many they would already form a decreasing subsequence"))

 def _monotone(self):
  ox, oy = -5.85, -0.10
  sx, sy = 4.40, 0.38
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  show = TERMS
  g.add(self._terms(ox, oy, sx, sy, show, DIM, r=0.05))
  pts = [[ox + sx * i / (len(show) - 1.0), oy + sy * show[i], 0] for i in MONO_IDX]
  g.add(self._curve(pts, ACCENT_B, sw=2.4))
  for q in pts:
   g.add(Dot(q, radius=0.062, color=ACCENT_B))
  rows = [("        " + "   ".join(f"{v:+.3f}" for v in MONO[:2]), ACCENT_B),
          ("        " + "   ".join(f"{v:+.3f}" for v in MONO[2:4]), ACCENT_B)]
  g.add(self._table(rows, x=PANEL_X, w=PANEL_W, y0=-0.30, dy=0.38))
  g.add(self._mid(0.60, "最後一個峰項之後，每一項都還有更大的在後面",
                  "past the last peak, every term is topped by a later one", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(0.02, "所以挑得出嚴格遞增的一支",
                  "so a strictly increasing subsequence can be built", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理 4.3 說有界的單調序列一定收斂，用的是上確界；兩條合起來就是定理 4.3",
                          "Lemma 4.3 says a bounded monotone sequence converges, by least upper bound; together they give Theorem 4.3",
                          ACCENT_A,
                          "原來的序列根本沒有極限，可是這一支有——這就是「無中生有」的意思",
                          "the original sequence has no limit at all while this one does, which is what creating convergence means"))

 def _induction(self):
  g = VGroup()
  g.add(self._rect(-4.85, 0.62, 1.45, 0.28, ACCENT_B),
        self._sym(0.62, "ℝ ⁿ  =  ℝ ⁿ ⁻ ¹  ×  ℝ", ACCENT_B, FS_TAG + 1, x=-4.85, w=2.70))
  g.add(self._arr([-4.85, 0.26, 0], [-4.85, 0.10, 0], ACCENT_A, sw=2.5, tl=0.10))
  for k, (lab, col) in enumerate((("{ y ᵐ }   →   y", ACCENT_C), ("{ z ᵐ }   →   z", WARN))):
   g.add(self._rect(-4.85, -0.10 - k * 0.50, 1.25, 0.22, col),
         self._sym(-0.10 - k * 0.50, lab, col, FS_TAG, x=-4.85, w=2.30))
  g.add(self._rect(-1.85, -0.35, 1.35, 0.28, ACCENT_A),
        self._sym(-0.35, "{ x ᵐ }   →   ⟨ y , z ⟩", ACCENT_A, FS_TAG, x=-1.85, w=2.50))
  g.add(self._arr([-3.45, -0.10, 0], [-3.00, -0.28, 0], ACCENT_A, sw=2, tl=0.10),
        self._arr([-3.45, -0.60, 0], [-3.00, -0.42, 0], ACCENT_A, sw=2, tl=0.10))
  g.add(self._panel(((0.86, "先對前 n 減一個座標用歸納假設",
                      "apply the inductive hypothesis to the first block", ACCENT_C),
                     (0.20, "再對剩下那一個座標取一次子序列",
                      "then take a further subsequence in the last coordinate", WARN),
                     (-0.46, "兩個分量都收斂，整個就收斂",
                      "both components converge, so the whole thing does", ACCENT_A))))
  return g.add(self._foot("定理 4.5 隨即得到：ℝⁿ 的有界閉集是序列緊緻的，而且在任何乘積範數下都成立",
                          "Theorem 4.5 follows at once: bounded closed sets in real n-space are compact, in any product norm",
                          ACCENT_A,
                          "「在任何乘積範數下」這句話，要等下一拍那條定理才真的站得住",
                          "the phrase in any product norm only becomes safe with the next beat's theorem"))

 def _thm46(self):
  cx, cy, s = -4.35, 0.10, 1.05
  g = VGroup()
  g.add(self._curve([[cx + s, cy, 0], [cx, cy + s, 0], [cx - s, cy, 0],
                     [cx, cy - s, 0], [cx + s, cy, 0]], ACCENT_B, sw=2.6))
  lo = min(SPHERE, key=_odd)
  hi = max(SPHERE, key=_odd)
  for v, col in ((lo, WARN), (hi, ACCENT_C)):
   g.add(Dot([cx + s * v[0], cy + s * v[1], 0], radius=0.075, color=col))
  g.add(self._sym(0.86, "m ‖ x ‖ ₁      ≤      ‖ x ‖      ≤      a ‖ x ‖ ₁",
                  ACCENT_A, FS_TAG + 1, x=PANEL_X, w=PANEL_W),
        self._sym(0.22, f"m  =  {M_CONST:.4f}          a  =  {A_CONST:.4f}", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.36, "藍色是一範數的單位球面，它是緊緻的",
                  "the blue diamond is the unit sphere of the one-norm, and it is compact",
                  ACCENT_B, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.94, "所以最小值取得到，而且不是零",
                  "so the minimum is attained, and it is not zero", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("兩個點是程式在球面上掃出來的最小值與最大值，再在球面外四個點上驗過那個夾擊",
                          "the two dots are the minimum and maximum found here on the sphere, and the sandwich was checked off it too",
                          ACCENT_A,
                          "這正是第 3 章第 4 節欠下的那個洞：那時用了「有限維上所有範數等價」，證明留到這裡",
                          "this fills the gap section 3.4 left open when it used that all norms on a finite dimensional space are equivalent"))

 def stage(self):
  a, b, c = self._subsequence(), self._lemma41(), self._definition()
  d, e, f = self._closedbounded(), self._extremes(), self._thm42()
  h, i, j = self._needcompact(), self._peaks(), self._monotone()
  k, l = self._induction(), self._thm46()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE58ZH, AdvCalcE58EN = make(AdvCalcE58Base, "58", prefix="AdvCalcE")
