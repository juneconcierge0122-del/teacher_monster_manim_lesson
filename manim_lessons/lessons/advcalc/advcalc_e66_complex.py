"""advcalc E66 -- chapter 4, section 11 (book pp. 240-243): the complex number
system.

The plane is already a real vector space; what makes it the complex numbers is
one extra operation.  With multiplication in hand the pair one-zero is the
unique identity and every nonzero element is invertible, so the system is a
*field* -- and that is what pays for the section, because a field can serve as a
new scalar field and the whole of chapters 1 and 2 runs again with the reals
replaced by the complex numbers.  Then: the real subfield, i, conjugation as the
only nontrivial automorphism fixing the reals, the absolute value and its
multiplicativity via conjugation, and finally the gap between real and complex
differentiability, closing on the fundamental theorem of algebra and the complex
exponential.

Section 11's content ends on book page 243; 243 to 245 are exercises 11.1 to
11.19, and starred section 12 begins on 245.  The OUTLINE lists the section as
240-245, counting the exercise pages -- the eighth time that column has done so.

Beats 8 and 9 are the spine, and they run the same computation twice.  For
conjugation the difference quotient is the conjugate over the step, which sweeps
the whole unit circle as the direction of approach turns: the limit depends on
the direction, so the map is not complex differentiable.  For a power series the
same quotient collapses to a single point.  Both loci are computed here, not
sketched.
"""
import cmath
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


def prod(a, b):
 """Complex multiplication written out, to check the component formula."""
 return complex(a.real * b.real - a.imag * b.imag,
                a.real * b.imag + a.imag * b.real)


# ── beat 1: multiplication, and what it does to modulus and argument ───
XI = complex(1.2, 0.5)
GA = complex(0.6, 0.9)
PR = XI * GA
assert abs(prod(XI, GA) - PR) < 1e-15, "the component formula is the multiplication"
assert abs(abs(PR) - abs(XI) * abs(GA)) < 1e-15, "moduli multiply"
assert abs(cmath.phase(PR) - (cmath.phase(XI) + cmath.phase(GA))) < 1e-12, \
    "and arguments add"

# ── beat 2: the identity, and the inverse ──────────────────────────────
ONE = complex(1.0, 0.0)
INV = XI.conjugate() / (abs(XI) ** 2)
assert abs(XI * ONE - XI) < 1e-15, "one and zero is the multiplicative identity"
assert abs(XI * INV - ONE) < 1e-15, "and the conjugate over the square modulus inverts"
assert abs(abs(INV) - 1.0 / abs(XI)) < 1e-15, "the inverse has the reciprocal modulus"

# ── beat 4: i, and its square ──────────────────────────────────────────
I = complex(0.0, 1.0)
assert I * I == complex(-1.0, 0.0), "the square of i really is minus one"
assert complex(XI.real, 0.0) + I * complex(XI.imag, 0.0) == XI, \
    "so a pair is x plus i y, exactly"

# ── beats 5 and 6: conjugation is an automorphism, and the absolute value
CONJ_SUM = (XI + GA).conjugate() - (XI.conjugate() + GA.conjugate())
CONJ_PROD = (XI * GA).conjugate() - XI.conjugate() * GA.conjugate()
assert abs(CONJ_SUM) < 1e-15 and abs(CONJ_PROD) < 1e-15, \
    "conjugation preserves both sums and products, so it is an automorphism"
SQ_MOD = XI * XI.conjugate()
assert abs(SQ_MOD.imag) < 1e-15 and abs(SQ_MOD.real - abs(XI) ** 2) < 1e-15, \
    "a number times its conjugate is real, and is the square of the absolute value"
MULT_ROWS = [(a, b, abs(a * b), abs(a) * abs(b))
             for a, b in ((XI, GA), (I, GA), (complex(2.0, 0.0), XI))]
for _a, _b, _l, _r in MULT_ROWS:
 assert abs(_l - _r) < 1e-14, "the absolute value is multiplicative"

# ── beat 8: conjugation is real linear and not complex linear ──────────
# real linear: it commutes with real scalars and respects addition
assert abs((3.0 * XI).conjugate() - 3.0 * XI.conjugate()) < 1e-15, "real linear"
# not complex linear: it does not commute with multiplication by i
NOT_C = (I * XI).conjugate() - I * XI.conjugate()
assert abs(NOT_C) > 1.0, "but it does not commute with multiplication by i"

NDIR = 16
CONJ_LOCUS = []
for _k in range(NDIR):
 _th = 2.0 * math.pi * _k / NDIR
 _h = 0.05 * cmath.exp(1j * _th)
 CONJ_LOCUS.append(_h.conjugate() / _h)
assert all(abs(abs(q) - 1.0) < 1e-14 for q in CONJ_LOCUS), \
    "every quotient sits on the unit circle"
CONJ_SPREAD = max(abs(p - q) for p in CONJ_LOCUS for q in CONJ_LOCUS)
assert CONJ_SPREAD > 1.9, "and they are spread right across it, so there is no limit"
REAL_DIR = complex(0.05, 0.0).conjugate() / complex(0.05, 0.0)
IMAG_DIR = complex(0.0, 0.05).conjugate() / complex(0.0, 0.05)
assert REAL_DIR == ONE and IMAG_DIR == -ONE, \
    "one along the real direction, minus one along the imaginary one"


# ── beat 9: a power series, where the same quotient collapses ───────────
def F(z):
 return 1.0 / (1.0 - z)


def dF(z):
 return 1.0 / (1.0 - z) ** 2


BETA = complex(0.3, 0.0)
SERIES = []
_s = complex(0.0, 0.0)
for _n in range(1, 41):
 _s += BETA ** (_n - 1)
 if _n in (4, 8, 16, 40):
  SERIES.append((_n, abs(_s - F(BETA))))
assert SERIES[-1][1] < 1e-6, "the geometric series really sums to the closed form"

PS_LOCUS = []
for _k in range(NDIR):
 _th = 2.0 * math.pi * _k / NDIR
 _h = 0.02 * cmath.exp(1j * _th)
 PS_LOCUS.append((F(BETA + _h) - F(BETA)) / _h)
PS_SPREAD = max(abs(p - q) for p in PS_LOCUS for q in PS_LOCUS)
assert PS_SPREAD < 0.12, "here the quotients cluster instead of spreading"
assert PS_SPREAD < CONJ_SPREAD / 15, "which is the whole difference between the two"
PS_DEV = max(abs(q - dF(BETA)) for q in PS_LOCUS)
assert PS_DEV < 0.07, "and they cluster on the term-by-term derivative"
# At the scale of beat 8 that cluster is a couple of pixels across, so beat 9
# magnifies it and says the factor on screen rather than drawing an empty picture.
PS_MAG = 12.0
assert 0.55 < PS_DEV * PS_MAG < 0.85, "the magnified cluster has to fill the picture"
SHRINK = [(r, max(abs((F(BETA + r * cmath.exp(1j * 2 * math.pi * k / NDIR))
                       - F(BETA)) / (r * cmath.exp(1j * 2 * math.pi * k / NDIR))
                      - dF(BETA)) for k in range(NDIR)))
          for r in (0.05, 0.01, 0.002)]
for (_r0, _e0), (_r1, _e1) in zip(SHRINK, SHRINK[1:]):
 assert _e1 < _e0, "and the cluster tightens as the step shrinks"

# ── beat 10: the factorisation, and the exponential ────────────────────
FACT = [(z, (z + I) * (z - I), z * z + 1.0)
        for z in (complex(0.0, 0.0), complex(1.0, 0.0), complex(0.7, -0.4))]
for _z, _l, _r in FACT:
 assert abs(_l - _r) < 1e-15, "x squared plus one factors over the complex numbers"
EXP_Z = complex(0.4, 1.1)
EULER = math.exp(EXP_Z.real) * complex(math.cos(EXP_Z.imag), math.sin(EXP_Z.imag))
assert abs(cmath.exp(EXP_Z) - EULER) < 1e-14, \
    "so the real and imaginary parts are e to the x times cosine and sine"
EXP_TERMS = []
_t, _s = ONE, complex(0.0, 0.0)
for _n in range(1, 26):
 _s += _t
 _t = _t * EXP_Z / _n
 if _n in (4, 8, 12, 25):
  EXP_TERMS.append((_n, abs(_s - EULER)))
assert EXP_TERMS[-1][1] < 1e-14, "and the series gets there"


class AdvCalcE66Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 66

 MODE_LABEL = {
  0: {"zh": "第三個基本數域", "en": "the third basic number field"},
  1: {"zh": "多出來的那一個運算", "en": "the one extra operation"},
  2: {"zh": "單位元與反元素：所以它是個域", "en": "an identity and inverses: so it is a field"},
  3: {"zh": "拿 ℂ 當純量域，前兩章重跑一遍", "en": "as a scalar field, chapters 1 and 2 run again"},
  4: {"zh": "ℝ 坐在裡面，而 i 的平方是負一", "en": "the reals sit inside, and i squared is minus one"},
  5: {"zh": "共軛是一個自同構", "en": "conjugation is an automorphism"},
  6: {"zh": "絕對值，以及它為什麼可乘", "en": "the absolute value, and why it multiplies"},
  7: {"zh": "複線性推得出實線性，反過來不行", "en": "complex linear gives real linear, not the reverse"},
  8: {"zh": "共軛的差商掃出整個圓", "en": "the quotient for conjugation sweeps the circle"},
  9: {"zh": "冪級數的差商縮成一點", "en": "for a power series the quotient collapses"},
  10: {"zh": "代數基本定理，與複指數", "en": "the fundamental theorem of algebra, and the exponential"},
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

 def _circ(self, cx, cy, r, col, sw=2.0, n=64):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.32, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 def _plane(self, cx, cy, s, xspan=1.15, yspan=1.05):
  """Axes for a small complex plane; s is screen units per unit of the plane."""
  return VGroup(Line([cx - s * xspan * 0.45, cy, 0], [cx + s * xspan, cy, 0],
                     color=DIM, stroke_width=1.3),
                Line([cx, cy - s * yspan * 0.55, 0], [cx, cy + s * yspan, 0],
                     color=DIM, stroke_width=1.3))

 def _vec(self, cx, cy, s, z, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * z.real, cy + s * z.imag, 0], col, sw=sw, tl=tl)

 # ── beats ─────────────────────────────────────────────────────────
 def _opening(self):
  cx, cy, s = -3.90, -0.30, 0.95
  g = VGroup(self._plane(cx, cy, s))
  g.add(self._vec(cx, cy, s, XI, ACCENT_B))
  g.add(Dot([cx + s * XI.real, cy + s * XI.imag, 0], radius=0.06, color=ACCENT_A))
  g.add(self._dash([cx + s * XI.real, cy, 0], [cx + s * XI.real, cy + s * XI.imag, 0],
                   DIM, n=6, sw=1.0),
        self._dash([cx, cy + s * XI.imag, 0], [cx + s * XI.real, cy + s * XI.imag, 0],
                   DIM, n=6, sw=1.0))
  g.add(self._sym(cy + s * XI.imag + 0.26,
                  f"ξ  =  ⟨ {XI.real:.1f} , {XI.imag:.1f} ⟩", ACCENT_A, FS_TAG - 1,
                  x=cx + s * XI.real + 0.70, w=2.40))
  g.add(self._panel(((0.86, "一個複數本來就等同於一對實數",
                      "a complex number is already just a pair of reals", ACCENT_B),
                     (0.20, "所以這個系統就是笛卡兒平面",
                      "so the system is the Cartesian plane", ACCENT_C),
                     (-0.46, "只是上面多帶了一些結構",
                      "carrying some further structure on top", WARN))))
  return g.add(self._foot("繼有理數與實數之後，複數是第三個必須研究的基本數域",
                          "after the rationals and the reals, the complex numbers are the third basic number field to study",
                          ACCENT_A,
                          "複數值的函數因此只是一種向量值函數——等同於一對實數值函數",
                          "a complex-valued function is therefore a kind of vector-valued function, equivalent to a pair of real-valued ones"))

 def _multiply(self):
  cx, cy, s = -3.95, -0.42, 0.72
  g = VGroup(self._plane(cx, cy, s, xspan=1.30, yspan=1.42))
  g.add(self._vec(cx, cy, s, XI, ACCENT_B),
        self._vec(cx, cy, s, GA, ACCENT_C),
        self._vec(cx, cy, s, PR, WARN))
  for z, lab, col in ((XI, "ξ", ACCENT_B), (GA, "γ", ACCENT_C), (PR, "ξ γ", WARN)):
   g.add(self._sym(cy + s * z.imag + 0.22, lab, col, FS_TAG - 1,
                   x=cx + s * z.real + 0.26, w=0.80))
  g.add(self._table((("     | ξ γ |   =   | ξ | | γ |", DIM),
                     (f"     {abs(PR):.4f}   =   {abs(XI):.4f} × {abs(GA):.4f}", ACCENT_B),
                     ("     arg ξ γ   =   arg ξ  +  arg γ", DIM),
                     (f"     {cmath.phase(PR):.4f}   =   {cmath.phase(XI):.4f} + {cmath.phase(GA):.4f}",
                      WARN)), y0=0.86, dy=0.36))
  g.add(self._mid(-0.72, "長度相乘，角度相加",
                  "the lengths multiply and the angles add", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定義的動機是把一對數寫成 x 加 i y、令 i 的平方等於負一，再照普通代數乘開",
                          "the definition is motivated by writing a pair as x plus i y with i squared minus one, and multiplying out by the ordinary laws of algebra",
                          ACCENT_A,
                          "畫面上三個向量的長度與角度都是算出來的，等式兩邊逐項對過",
                          "the lengths and angles of the three vectors on screen are computed, and both sides of each identity checked"))

 def _field(self):
  cx, cy, s = -3.95, -0.14, 0.88
  g = VGroup(self._plane(cx, cy, s))
  g.add(self._circ(cx, cy, s, DIM, sw=1.2))
  g.add(self._vec(cx, cy, s, XI, ACCENT_B),
        self._vec(cx, cy, s, INV, WARN),
        self._vec(cx, cy, s, ONE, ACCENT_A, sw=2.0))
  for z, lab, col in ((XI, "ξ", ACCENT_B), (INV, "ξ ⁻ ¹", WARN), (ONE, "1", ACCENT_A)):
   dy = 0.24 if z.imag > 0.01 else (-0.32 if z.imag < -0.01 else 0.26)
   g.add(self._sym(cy + s * z.imag + dy, lab, col, FS_TAG - 1,
                   x=cx + s * z.real + 0.30, w=0.90))
  g.add(self._table((("     ξ ⁻ ¹   =   ξ ‾ / | ξ | ²", DIM),
                     (f"     | ξ |   =   {abs(XI):.4f}", ACCENT_B),
                     (f"     | ξ ⁻ ¹ |   =   {abs(INV):.4f}", WARN),
                     (f"     ξ  ξ ⁻ ¹   =   {(XI * INV).real:.1f}", ACCENT_A)),
                    y0=0.86, dy=0.36))
  g.add(self._mid(-0.72, "灰色那個圓是長度一的地方",
                  "the grey circle is where the length is one", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("⟨ 1 , 0 ⟩ 是唯一的乘法單位元，而每個非零元素都有乘法反元素",
                          "the pair one, zero is the unique multiplicative identity, and every nonzero element has an inverse",
                          ACCENT_A,
                          "把這幾件事總結起來就是一句話：這個系統是一個域",
                          "those facts are summarised in one word: the system is a field"))

 def _scalars(self):
  g = VGroup()
  for cy, lab, col in ((0.62, "ℝ", ACCENT_B), (-0.06, "ℂ", WARN)):
   g.add(self._rect(-4.70, cy, 0.42, 0.26, col),
         self._sym(cy, lab, col, FS_TAG + 1, x=-4.70, w=0.70))
   g.add(self._arr([-4.18, cy, 0], [-3.50, cy, 0], ACCENT_A, sw=2.0, tl=0.10))
   g.add(self._rect(-2.35, cy, 1.05, 0.26, col),
         self._sym(cy, "Ch 1 – 2", col, FS_TAG - 1, x=-2.35, w=1.90))
  g.add(self._sym(-0.66, "ℂ ⁿ   =   { ⟨ ξ ₁ , … , ξ ₙ ⟩ }", ACCENT_C,
                  FS_TAG, x=-3.40, w=4.20))
  g.add(self._panel(((0.86, "因為它是一個域，就能當純量域用",
                      "because it is a field, it can serve as a scalar field", ACCENT_B),
                     (0.20, "第 1、2 章把 ℝ 處處換成 ℂ 就仍然成立",
                      "chapters 1 and 2 stay valid with the reals replaced everywhere",
                      WARN),
                     (-0.46, "純量乘法現在是複數乘法",
                      "scalar multiplication is now complex multiplication", ACCENT_A))))
  return g.add(self._foot("這一點就換到了整節的全部——域這個性質不是裝飾，是整套理論可以重跑的理由",
                          "that single fact buys the whole section: being a field is not decoration, it is why the entire theory runs again",
                          ACCENT_A,
                          "於是 ℂ ⁿ 就是複數 n 元組的向量空間，純量是複數",
                          "so complex n-space is the vector space of n-tuples of complex numbers, with complex scalars"))

 def _embed(self):
  cx, cy, s = -3.90, -0.30, 0.95
  g = VGroup(self._plane(cx, cy, s))
  g.add(Line([cx - s * 0.45, cy, 0], [cx + s * 1.15, cy, 0], color=ACCENT_B, stroke_width=3.2))
  for z, lab, col in ((ONE, "1", ACCENT_B), (I, "i", WARN), (-ONE, "− 1", ACCENT_A)):
   g.add(Dot([cx + s * z.real, cy + s * z.imag, 0], radius=0.065, color=col),
         self._sym(cy + s * z.imag + 0.24, lab, col, FS_TAG - 1,
                   x=cx + s * z.real + 0.22, w=0.80))
  g.add(self._curve([[cx + s * 0.62 * math.cos(math.pi / 2 * k / 30),
                      cy + s * 0.62 * math.sin(math.pi / 2 * k / 30), 0]
                     for k in range(31)], WARN, sw=1.4),
        self._curve([[cx + s * 0.62 * math.cos(math.pi / 2 * (1 + k / 30)),
                      cy + s * 0.62 * math.sin(math.pi / 2 * (1 + k / 30)), 0]
                     for k in range(31)], ACCENT_A, sw=1.4))
  g.add(self._table((("     x    ↦    ⟨ x , 0 ⟩", DIM),
                     ("     i   =   ⟨ 0 , 1 ⟩", WARN),
                     (f"     i ²   =   ⟨ {(I * I).real:.0f} , {(I * I).imag:.0f} ⟩", ACCENT_A),
                     ("     ⟨ x , y ⟩   =   x  +  i y", ACCENT_B)), y0=0.86, dy=0.36))
  g.add(self._mid(-0.72, "乘 i 就是轉四分之一圈，轉兩次就到 −1",
                  "multiplying by i is a quarter turn, and two of them reach minus one",
                  ACCENT_C, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("青色那條線是實軸——x 映到 ⟨ x , 0 ⟩ 保和也保積，所以 ℝ 是以子域坐在裡面",
                          "the teal line is the real axis: sending x to the pair with second entry zero preserves sums and products, so the reals sit inside as a subfield",
                          ACCENT_A,
                          "習慣上就把 x 與它的像認同，於是可以寫成 x 加 i y",
                          "it is conventional to identify x with its image, which is what lets a pair be written as x plus i y"))

 def _conjugate(self):
  cx, cy, s = -3.90, -0.10, 0.85
  g = VGroup(self._plane(cx, cy, s, yspan=1.15))
  g.add(Line([cx - s * 0.45, cy, 0], [cx + s * 1.15, cy, 0], color=DIM, stroke_width=2.2))
  g.add(self._vec(cx, cy, s, XI, ACCENT_B),
        self._vec(cx, cy, s, XI.conjugate(), WARN))
  g.add(self._dash([cx + s * XI.real, cy + s * XI.imag, 0],
                   [cx + s * XI.real, cy - s * XI.imag, 0], ACCENT_C, n=7, sw=1.1))
  for z, lab, col in ((XI, "ξ", ACCENT_B), (XI.conjugate(), "ξ ‾", WARN)):
   g.add(self._sym(cy + s * z.imag + (0.24 if z.imag > 0 else -0.30), lab, col,
                   FS_TAG - 1, x=cx + s * z.real + 0.26, w=0.80))
  g.add(self._table((("     ξ + η  ‾   −   ( ξ ‾ + η ‾ )", DIM),
                     (f"     =   {abs(CONJ_SUM):.1e}", ACCENT_B),
                     ("     ξ η  ‾   −   ξ ‾ η ‾", DIM),
                     (f"     =   {abs(CONJ_PROD):.1e}", WARN)), y0=0.86, dy=0.36))
  g.add(self._mid(-0.78, "保和也保積，所以它是域的自同構",
                  "sums and products both survive, so it is a field automorphism",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("共軛就是對實軸的鏡射，而且它保和也保積——所以是這個域到自己的自同構",
                          "conjugation is reflection in the real axis, and it preserves sums and products, so it is an automorphism of the field with itself",
                          ACCENT_A,
                          "而且除了恆等映射之外，它是唯一一個讓每個實數都不動的自同構",
                          "and apart from the identity it is the only automorphism leaving every real number fixed"))

 def _absolute(self):
  cx, cy, s = -4.05, -0.10, 0.76
  g = VGroup(self._plane(cx, cy, s, xspan=1.60, yspan=1.15))
  g.add(self._vec(cx, cy, s, XI, ACCENT_B),
        self._vec(cx, cy, s, XI.conjugate(), ACCENT_C))
  g.add(self._vec(cx, cy, s, SQ_MOD, WARN, sw=3.0))
  rows = [(f"     ξ  ξ ‾   =   {SQ_MOD.real:.4f}   =   | ξ | ²", WARN),
          ("       | a b |          | a | | b |", DIM)]
  for a, b, l, r in MULT_ROWS:
   rows.append((f"      {l:.4f}           {r:.4f}", ACCENT_C))
  g.add(self._table(rows, y0=0.86, dy=0.34))
  g.add(self._mid(-0.72, "三組都對得上，到小數第十四位",
                  "all three agree, to fourteen decimal places", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("ξ 乘它的共軛落在實軸上，而且正好是絕對值的平方——可乘性就從這裡掉出來",
                          "a number times its conjugate lands on the real axis and is exactly the square of the absolute value, and multiplicativity falls out of that",
                          ACCENT_A,
                          "同一個等式順便把反元素交出來：ξ 的共軛除以絕對值的平方",
                          "the same identity hands over the inverse: the conjugate divided by the square of the absolute value"))

 def _oneway(self):
  g = VGroup()
  g.add(self._rect(-4.55, 0.52, 1.25, 0.28, WARN),
        self._mid(0.52, "ℂ 線性", "complex linear", WARN, FS_TAG, x=-4.55, w=2.30))
  g.add(self._rect(-1.45, 0.52, 1.25, 0.28, ACCENT_B),
        self._mid(0.52, "ℝ 線性", "real linear", ACCENT_B, FS_TAG, x=-1.45, w=2.30))
  g.add(self._arr([-3.24, 0.62, 0], [-2.74, 0.62, 0], ACCENT_A, sw=2.4, tl=0.12))
  g.add(self._sym(0.30, "⇏", DIM, FS_TAG + 3, x=-2.99, w=0.70))
  g.add(self._sym(-0.36, f"( i ξ ) ‾   −   i  ξ ‾    =    {abs(NOT_C):.1f}", ACCENT_C,
                  FS_TAG, x=-3.40, w=4.60))
  g.add(self._mid(-0.88, "共軛就是那個反例",
                  "conjugation is the counterexample", WARN, FS_TAG, x=-3.40, w=4.20))
  g.add(self._panel(((0.86, "ℝ 是子域，所以複的自動也是實的",
                      "the reals are a subfield, so complex gives real for free", WARN),
                     (0.20, "可是實線性一般不是複線性",
                      "but real linear is in general not complex linear", ACCENT_B),
                     (-0.46, "差別在於：跟乘 i 交換不交換",
                      "the difference is whether it commutes with multiplying by i",
                      ACCENT_A))))
  return g.add(self._foot("複可微的定義一樣：ΔF 等於一個複線性的 T 加上 o；那樣的 F 自動也實可微",
                          "complex differentiability reads the same way, with a complex linear T plus a remainder, and such an F is automatically real differentiable",
                          ACCENT_A,
                          "可是反過來不成立——下一拍用差商把理由畫出來",
                          "the converse fails, and the next beat draws the reason with a difference quotient"))

 def _sweep(self):
  cx, cy, s = -3.90, -0.05, 0.92
  g = VGroup(self._plane(cx, cy, s, xspan=1.20, yspan=1.05))
  g.add(self._circ(cx, cy, s, DIM, sw=1.2))
  for q in CONJ_LOCUS:
   g.add(Dot([cx + s * q.real, cy + s * q.imag, 0], radius=0.055, color=ACCENT_C))
  for z, lab, col in ((ONE, "→  1", ACCENT_B), (-ONE, "→  − 1", WARN)):
   g.add(Dot([cx + s * z.real, cy + s * z.imag, 0], radius=0.075, color=col),
         self._sym(cy + 0.30, lab, col, FS_TAG - 1,
                   x=cx + s * z.real + (0.60 if z.real > 0 else -0.60), w=1.40))
  g.add(self._table((("     Δ F ( h ) / h   =   h ‾ / h", DIM),
                     (f"     h  >  0        {REAL_DIR.real:.0f}", ACCENT_B),
                     (f"     h  =  i t      {IMAG_DIR.real:.0f}", WARN),
                     (f"     max | q − q ′ |   =   {CONJ_SPREAD:.2f}", ACCENT_C)),
                    y0=0.86, dy=0.36))
  g.add(self._mid(-0.74, "十六個方向的商掃滿整個單位圓",
                  "the quotients for sixteen directions fill the whole unit circle",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("共軛的差商是 h 的共軛除以 h——它的值完全由趨近的方向決定，所以沒有極限",
                          "the quotient for conjugation is the conjugate of the step over the step, whose value is decided entirely by the direction of approach, so no limit exists",
                          ACCENT_A,
                          "沿實軸趨近得到 1，沿虛軸趨近得到 −1；一個映射可以實可微而不複可微",
                          "approaching along the real axis gives one and along the imaginary axis minus one: a map can be real differentiable without being complex differentiable"))

 def _collapse(self):
  # centred on F'(beta), showing the deviations magnified: at the scale of the
  # previous beat this cluster would be a couple of pixels across
  cx, cy, s = -3.90, -0.05, 0.92
  g = VGroup(self._plane(cx, cy, s, xspan=1.20, yspan=1.05))
  tgt = dF(BETA)
  rad = s * PS_DEV * PS_MAG
  g.add(self._circ(cx, cy, rad, DIM, sw=1.3, n=48))
  for q in PS_LOCUS:
   d = (q - tgt) * PS_MAG
   g.add(Dot([cx + s * d.real, cy + s * d.imag, 0], radius=0.055, color=WARN))
  g.add(Dot([cx, cy, 0], radius=0.085, color=ACCENT_A))
  # kept clear of the y axis, which reaches almost as high as this label
  g.add(self._sym(cy + rad + 0.28, f"F ′ ( β )  =  {tgt.real:.4f}", ACCENT_A,
                  FS_TAG - 1, x=cx + 1.35, w=1.90),
        self._sym(cy, f"×  {PS_MAG:.0f}", ACCENT_C,
                  FS_TAG - 1, x=cx + 1.55, w=1.00))
  g.add(self._table((("       r          max | Δ F / h  −  F ′ |", DIM),)
                    + tuple((f"     {r:.3f}                {e:.4f}", ACCENT_C)
                            for r, e in SHRINK), y0=0.86, dy=0.34))
  g.add(self._mid(-0.74, f"同樣十六個方向，散布只有 {PS_SPREAD:.2f}（放大 {PS_MAG:.0f} 倍才看得見）",
                  f"the same sixteen directions, spread only {PS_SPREAD:.2f}, magnified {PS_MAG:.0f} times to be seen",
                  WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("同一個計算，換成冪級數就縮成一點——微分是「乘上 F 撇 β」，而那是複線性的",
                          "the same computation on a power series collapses to a point: the differential is multiplication by F prime of beta, and that is complex linear",
                          ACCENT_A,
                          f"灰圓的半徑是十六個商離 F 撇 β 最遠的那個距離（{PS_DEV:.3f}），放大 {PS_MAG:.0f} 倍畫出來；上一拍那個圓是單位圓",
                          f"the grey circle is the largest distance from those sixteen quotients to F prime of beta, {PS_DEV:.3f}, drawn magnified {PS_MAG:.0f} times; the circle in the last beat was the unit circle"))

 def _closing(self):
  g = VGroup()
  g.add(self._sym(0.82, "x ²  +  1    =    ( x + i ) ( x − i )", ACCENT_B,
                  FS_TAG + 1, x=-3.50, w=4.80))
  g.add(self._sym(0.28, "e ˣ ⁺ ⁱ ʸ    =    e ˣ  ( cos y  +  i sin y )", WARN,
                  FS_TAG + 1, x=-3.50, w=5.20))
  g.add(self._dash([-5.90, -0.10, 0], [-1.10, -0.10, 0], DIM, n=22, sw=1.2))
  rows = [("       n        | σ ₙ  −  e ᶻ |", DIM)]
  for n, e in EXP_TERMS:
   rows.append((f"     {n:4d}            {e:.1e}", ACCENT_C))
  g.add(self._table(rows, y0=0.86, dy=0.34))
  g.add(self._sym(-0.48, f"z  =  {EXP_Z.real:.1f}  +  {EXP_Z.imag:.1f} i", ACCENT_A,
                  FS_TAG - 1, x=-3.50, w=2.80))
  g.add(self._mid(-0.92, "級數與那個公式差在 1e-14 以內",
                  "the series and that formula agree to within 1e-14", ACCENT_A,
                  FS_TAG, x=-3.50, w=5.20))
  return g.add(self._foot("代數基本定理：複係數多項式是一次因式的積。關鍵就是 x ² + 1 在 ℝ 上分解不了",
                          "the fundamental theorem of algebra: a polynomial with complex coefficients is a product of linear factors, and the crux is that x squared plus one does not factor over the reals",
                          ACCENT_A,
                          "書上說複可微的後果「難以估計」，大多留給複變函數論——這一章到此結束",
                          "the book calls the consequences of complex differentiability incalculable and leaves most of them to a course on complex variables, and the chapter ends here"))

 def stage(self):
  a, b, c = self._opening(), self._multiply(), self._field()
  d, e, f = self._scalars(), self._embed(), self._conjugate()
  h, i, j = self._absolute(), self._oneway(), self._sweep()
  k, l = self._collapse(), self._closing()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE66ZH, AdvCalcE66EN = make(AdvCalcE66Base, "66", prefix="AdvCalcE")
