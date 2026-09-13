"""advcalc E69 -- chapter 5, section 2, first half (book pp. 252-254): orthogonal
projection.

Dropping a perpendicular from a point to a line or a plane is one of the oldest
devices in geometry, and section 2 is that device in a pre-Hilbert space.  The
foot of the perpendicular from a vector to a subspace M is the vector in M whose
difference is orthogonal to M, and having a foot for every vector is exactly the
direct sum decomposition V = M + M-perp.  Lemma 2.1 identifies the foot with the
best approximation; Lemma 2.2 shows a minimising sequence is Cauchy (by the
parallelogram law of the last episode); Theorem 2.1 then gets the decomposition
out of completeness.  The rest is the projection itself: Lemma 2.3 (projections
on orthogonal subspaces add) and Lemma 2.4 (the projection on a line), which is
where the Fourier coefficient comes from.

Section 2 runs from book page 252 to 256 and takes two episodes.  This one stops
at the top of 254, where the Fourier coefficient has just been named; E70 picks
up with orthonormal sets, Bessel's inequality, bases, Gram-Schmidt and the
theorem that V is a Hilbert space exactly when V* is its own mirror.

Two examples carry the numbers.  In the plane, M is the line through a fixed
vector, and every claim about feet and distances is computed there -- including
beat 4, where a point of M that is *not* the foot makes the quadratic of the
proof dip below zero.  In C([0, pi]) the target is built as a combination of
four sines, three of which span M, so the Fourier coefficients come back exactly
as the numbers it was built from and the residual is the fourth sine alone.
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


# ── the plane: M is the line through ETA ───────────────────────────────
def dot(a, b):
 return a[0] * b[0] + a[1] * b[1]


def n2(v):
 return math.sqrt(dot(v, v))


def sub(a, b):
 return (a[0] - b[0], a[1] - b[1])


ETA = (1.0, 0.45)
AL = (0.6, 1.5)
XC = dot(AL, ETA) / dot(ETA, ETA)
MU = (XC * ETA[0], XC * ETA[1])
RES = sub(AL, MU)
RHO = n2(RES)
assert abs(dot(RES, ETA)) < 1e-12, "the foot is where the difference is orthogonal to M"

# ── beats 2 and 3: every other point of M is farther, by Pythagoras ────
OTHER = []
for _s in (0.8, -0.6):
 _xi = (MU[0] + _s * ETA[0], MU[1] + _s * ETA[1])
 _d, _leg = n2(sub(AL, _xi)), abs(_s) * n2(ETA)
 assert abs(_d ** 2 - (RHO ** 2 + _leg ** 2)) < 1e-12, "a right triangle at the foot"
 OTHER.append((_s, _xi, _d, _leg))
assert all(d > RHO for _s, _xi, d, _leg in OTHER), "so the foot is the unique closest point"

# ── beat 4: what goes wrong at a point of M that is not the foot ───────
MUP = (MU[0] + 0.8 * ETA[0], MU[1] + 0.8 * ETA[1])
QB = dot(sub(AL, MUP), ETA)
QA = dot(ETA, ETA)
assert abs(QB) > 0.9, "at the wrong point the product does not vanish"
T_MIN = -QB / QA
Q_MIN = -QB * QB / QA
assert Q_MIN < -0.7, "and then the quadratic dips below zero: moving that way gets closer"


def qwrong(t):
 return 2.0 * t * QB + t * t * QA


def qright(t):
 return t * t * QA


assert qwrong(T_MIN) < 0 < qright(T_MIN), \
    "the same quadratic at the foot never goes below zero, which is the whole proof"

# ── beats 5 and 6: a minimising sequence, and why it is Cauchy ─────────
NS = (1, 2, 4, 8, 16)


def mu_n(n):
 s = (-1) ** n / n
 return (MU[0] + s * ETA[0], MU[1] + s * ETA[1])


MSEQ = [(n, mu_n(n), n2(sub(AL, mu_n(n)))) for n in NS]
for (_, _, _a), (_, _, _b) in zip(MSEQ, MSEQ[1:]):
 assert _b < _a, "the distances decrease to the distance from the vector to M"
assert MSEQ[-1][2] - RHO < 0.003, "and they get there"
NP, MP = 1, 3
MID = ((mu_n(NP)[0] + mu_n(MP)[0]) / 2, (mu_n(NP)[1] + mu_n(MP)[1]) / 2)
PAR_L = n2(sub(mu_n(NP), mu_n(MP))) ** 2
PAR_R = 2.0 * (n2(sub(AL, mu_n(NP))) ** 2 + n2(sub(AL, mu_n(MP))) ** 2) \
    - 4.0 * n2(sub(AL, MID)) ** 2
assert abs(PAR_L - PAR_R) < 1e-12, "the parallelogram law, written for the two terms"
MID_D = n2(sub(AL, MID))
assert MID_D >= RHO, "and the midpoint is in M too, so its distance is at least rho"

# ── C([0, pi]): the target is built out of four sines ──────────────────
COEF = (1.0, 0.6, 0.35)
TAIL_K, TAIL_C = 5, 0.5


def alpha(t):
 return (sum(c * math.sin((i + 1) * t) for i, c in enumerate(COEF))
         + TAIL_C * math.sin(TAIL_K * t))


SIN = [(k, (lambda k: (lambda t: math.sin(k * t)))(k)) for k in (1, 2, 3)]
SQ = PI / 2


def fsp(f, g):
 return simpson(lambda t: f(t) * g(t), 0.0, PI)


def fnm(f):
 return math.sqrt(fsp(f, f))


FC = [fsp(alpha, f) / SQ for _k, f in SIN]
for _c, _built in zip(FC, COEF):
 assert abs(_c - _built) < 1e-9, \
     "the Fourier coefficients come back as the numbers the target was built from"


def proj(n):
 return lambda t: sum(FC[i] * SIN[i][1](t) for i in range(n))


PD = [(n, fnm(lambda t, n=n: alpha(t) - proj(n)(t))) for n in (1, 2, 3)]
for (_, _a), (_, _b) in zip(PD, PD[1:]):
 assert _b < _a, "each extra basis vector can only bring the projection closer"
FRHO = PD[-1][1]
assert abs(FRHO - TAIL_C * math.sqrt(SQ)) < 1e-9, \
    "and what is left is exactly the one sine that M does not contain"
ORTH = [(k, fsp(lambda t: alpha(t) - proj(3)(t), f)) for k, f in SIN]
assert all(abs(v) < 1e-9 for _k, v in ORTH), "the residual is orthogonal to all of M"
PERT = []
for _p in ((0.15, 0.0, 0.0), (0.0, -0.2, 0.0), (0.1, 0.1, 0.1)):
 _q = lambda t, _p=_p: sum((FC[i] + _p[i]) * SIN[i][1](t) for i in range(3))
 PERT.append((_p, fnm(lambda t, _q=_q: alpha(t) - _q(t))))
assert all(d > FRHO for _p, d in PERT), "and every other point of M really is farther"
L23 = fnm(lambda t: proj(3)(t) - sum(FC[i] * SIN[i][1](t) for i in range(3)))
assert L23 < 1e-12, "the three one-dimensional projections add up to the projection"


class AdvCalcE69Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 69

 MODE_LABEL = {
  0: {"zh": "作垂線，取垂足", "en": "dropping a perpendicular"},
  1: {"zh": "有垂足 ⇔ 直和分解", "en": "a foot for every vector is the decomposition"},
  2: {"zh": "引理 2.1：垂足就是最佳近似", "en": "lemma 2.1: the foot is the best approximation"},
  3: {"zh": "一個方向：畢氏定理", "en": "one direction: the Pythagorean theorem"},
  4: {"zh": "反過來：那個二次式不能變號", "en": "the converse: that quadratic cannot change sign"},
  5: {"zh": "取極小化序列，關鍵在完備性", "en": "a minimising sequence, and where completeness enters"},
  6: {"zh": "引理 2.2：它一定是 Cauchy", "en": "lemma 2.2: such a sequence is Cauchy"},
  7: {"zh": "定理 2.1：V = M ⊕ M ⊥", "en": "theorem 2.1: the decomposition"},
  8: {"zh": "正交投影就是那個被挑出來的", "en": "the orthogonal projection is the distinguished one"},
  9: {"zh": "引理 2.3：投影可以加起來", "en": "lemma 2.3: projections add"},
  10: {"zh": "引理 2.4 與 Fourier 係數", "en": "lemma 2.4, and the Fourier coefficient"},
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

 def _fcurve(self, ox, oy, sx, sy, f, col, t0=0.0, t1=PI, sw=2.4, n=96):
  return self._curve([[ox + sx * (t0 + k * (t1 - t0) / n),
                       oy + sy * f(t0 + k * (t1 - t0) / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 # the plane, drawn with the line M through the origin
 def _stage(self, cx, cy, s, lo=-1.25, hi=2.25, axes=True):
  g = VGroup()
  if axes:
   g.add(Line([cx - s * 0.85, cy, 0], [cx + s * 2.30, cy, 0], color=DIM, stroke_width=1.1),
         Line([cx, cy - s * 0.65, 0], [cx, cy + s * 1.95, 0], color=DIM, stroke_width=1.1))
  g.add(Line([cx + s * lo * ETA[0], cy + s * lo * ETA[1], 0],
             [cx + s * hi * ETA[0], cy + s * hi * ETA[1], 0],
             color=ACCENT_B, stroke_width=2.6))
  return g

 def _pt(self, cx, cy, s, v, col, r=0.065):
  return Dot([cx + s * v[0], cy + s * v[1], 0], radius=r, color=col)

 def _seg(self, cx, cy, s, a, b, col, n=6, sw=1.4):
  return self._dash([cx + s * a[0], cy + s * a[1], 0],
                    [cx + s * b[0], cy + s * b[1], 0], col, n=n, sw=sw)

 def _vec(self, cx, cy, s, v, col, sw=2.6, tl=0.13):
  return self._arr([cx, cy, 0], [cx + s * v[0], cy + s * v[1], 0], col, sw=sw, tl=tl)

 def _lab(self, cx, cy, s, v, txt, col, dx=0.24, dy=0.24, w=0.90):
  return self._sym(cy + s * v[1] + dy, txt, col, FS_TAG - 1, x=cx + s * v[0] + dx, w=w)

 # ── beats ─────────────────────────────────────────────────────────
 def _opening(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  g.add(self._pt(cx, cy, s, AL, ACCENT_A), self._pt(cx, cy, s, MU, WARN))
  g.add(self._seg(cx, cy, s, AL, MU, WARN, n=7, sw=1.6))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_A, dx=0.02, dy=0.28),
        self._lab(cx, cy, s, MU, "μ", WARN, dx=0.26, dy=-0.28),
        self._sym(cy + s * 2.05 * ETA[1], "M", ACCENT_B, FS_TAG - 1,
                  x=cx + s * 2.05 * ETA[0] + 0.26, w=0.70))
  g.add(self._panel(((0.86, "從一點往一條線或一個平面作垂線",
                      "dropping a perpendicular from a point to a line or a plane",
                      ACCENT_B),
                     (0.20, "再用直角三角形論證",
                      "and then arguing with right triangles", ACCENT_C),
                     (-0.46, "這一招在 pre-Hilbert 空間裡一樣重要",
                      "the device matters just as much in a pre-Hilbert space", WARN))))
  return g.add(self._foot("青綠色那條線是子空間 M，紅色那個點是垂足 μ——M 裡使 α 減 μ 垂直 M 的那一點",
                          "the teal line is the subspace M and the red dot is the foot, the point of M whose difference from the given vector is orthogonal to M",
                          ACCENT_A,
                          f"這裡 M 是平面上一條過原點的直線，垂足與距離都是算出來的：ρ = {RHO:.4f}，而內積 ( α − μ , η ) = {dot(RES, ETA):.0e}",
                          f"here M is a line through the origin, and the foot and the distance are computed: rho is {RHO:.4f} and the product of the difference with the direction is {dot(RES, ETA):.0e}"))

 def _decomp(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  # M-perp, drawn from the direction the computation produced
  pe = (-ETA[1], ETA[0])
  g.add(Line([cx - s * 0.40 * pe[0], cy - s * 0.40 * pe[1], 0],
             [cx + s * 1.35 * pe[0], cy + s * 1.35 * pe[1], 0],
             color=ACCENT_C, stroke_width=2.0))
  g.add(self._vec(cx, cy, s, AL, ACCENT_A), self._vec(cx, cy, s, MU, WARN))
  g.add(self._arr([cx + s * MU[0], cy + s * MU[1], 0],
                  [cx + s * AL[0], cy + s * AL[1], 0], ACCENT_C, sw=2.4, tl=0.12))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_A, dx=0.02, dy=0.28),
        self._lab(cx, cy, s, MU, "μ", WARN, dx=0.26, dy=-0.28),
        self._sym(cy - s * 0.40 * pe[1] - 0.10, "M ⊥", ACCENT_C, FS_TAG - 1,
                  x=cx - s * 0.40 * pe[0] + 0.62, w=1.00))
  g.add(self._table(((f"     α   =   μ   +   ( α − μ )", DIM),
                     (f"     μ   =   ⟨ {MU[0]:.4f} , {MU[1]:.4f} ⟩", WARN),
                     (f"     α − μ   =   ⟨ {RES[0]:.4f} , {RES[1]:.4f} ⟩", ACCENT_C),
                     (f"     ( α − μ , η )   =   {dot(RES, ETA):.0e}", ACCENT_B)),
                    y0=0.80, dy=0.36))
  g.add(self._mid(-0.86, "一個在 M 裡，一個垂直 M",
                  "one term in M, the other orthogonal to it", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("把 α 寫成 μ 加上 α 減 μ：每個 α 都有垂足，等價於 V 分解成 M 與它的正交補的直和",
                          "writing the vector as the foot plus the difference: having a foot for every vector is the same as the direct sum decomposition",
                          ACCENT_A,
                          "而這個分解正是完備性保證的——接下來三拍就是在把它證出來",
                          "and that decomposition is exactly what completeness guarantees, which the next three beats prove"))

 def _lemma21(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  g.add(self._pt(cx, cy, s, AL, ACCENT_A), self._pt(cx, cy, s, MU, WARN))
  g.add(self._seg(cx, cy, s, AL, MU, WARN, n=7, sw=1.6))
  for (_s, xi, d, _leg), col in zip(OTHER, (ACCENT_C, DIM)):
   g.add(self._pt(cx, cy, s, xi, col, r=0.055), self._seg(cx, cy, s, AL, xi, col, n=7, sw=1.2))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_A, dx=0.02, dy=0.28),
        self._lab(cx, cy, s, MU, "μ", WARN, dx=0.10, dy=-0.30),
        self._lab(cx, cy, s, OTHER[0][1], "ξ", ACCENT_C, dx=0.20, dy=-0.28))
  g.add(self._table((("        ‖ α − · ‖", DIM),
                     (f"     μ          {RHO:.4f}", WARN),
                     (f"     ξ          {OTHER[0][2]:.4f}", ACCENT_C),
                     (f"     ξ ′         {OTHER[1][2]:.4f}", DIM)), y0=0.80, dy=0.36))
  g.add(self._mid(-0.86, "垂足是唯一最近的那一點",
                  "the foot is the unique closest point", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理 2.1：μ 在 M 裡時，α 減 μ 垂直 M 的充要條件，就是 μ 是 M 裡離 α 最近的唯一一點",
                          "lemma 2.1: for a vector in M, the difference being orthogonal to M is equivalent to its being the unique closest point of M",
                          ACCENT_A,
                          "也就是說「垂足」與「最佳近似」是同一件事——右邊三個距離都是算出來的，垂足那一個最小",
                          "so the foot and the best approximation are the same thing, and the three distances on the right are computed, with the foot's the smallest"))

 def _pythagoras(self):
  cx, cy, s = -4.35, -0.52, 0.84
  _s, XI, D, LEG = OTHER[0]
  g = self._stage(cx, cy, s, lo=-0.35, hi=2.25)
  g.add(Line([cx + s * AL[0], cy + s * AL[1], 0], [cx + s * MU[0], cy + s * MU[1], 0],
             color=WARN, stroke_width=2.2),
        Line([cx + s * AL[0], cy + s * AL[1], 0], [cx + s * XI[0], cy + s * XI[1], 0],
             color=ACCENT_C, stroke_width=2.2))
  # the right-angle mark, built from the two directions it sits between
  u = (RES[0] / RHO, RES[1] / RHO)
  v = (ETA[0] / n2(ETA), ETA[1] / n2(ETA))
  c0 = [cx + s * MU[0], cy + s * MU[1], 0]
  g.add(self._curve([[c0[0] + 0.16 * u[0], c0[1] + 0.16 * u[1], 0],
                     [c0[0] + 0.16 * (u[0] + v[0]), c0[1] + 0.16 * (u[1] + v[1]), 0],
                     [c0[0] + 0.16 * v[0], c0[1] + 0.16 * v[1], 0]], DIM, sw=1.6))
  g.add(self._pt(cx, cy, s, AL, ACCENT_A), self._pt(cx, cy, s, MU, WARN),
        self._pt(cx, cy, s, XI, ACCENT_C, r=0.055))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_A, dx=0.02, dy=0.28),
        self._lab(cx, cy, s, MU, "μ", WARN, dx=0.06, dy=-0.30),
        self._lab(cx, cy, s, XI, "ξ", ACCENT_C, dx=0.22, dy=-0.28))
  g.add(self._table((("     ‖ α − ξ ‖ ²      ‖ α − μ ‖ ²  +  ‖ μ − ξ ‖ ²", DIM),
                     (f"      {D ** 2:.4f}             {RHO ** 2:.4f}  +  {LEG ** 2:.4f}",
                      ACCENT_C),
                     (f"      {D ** 2:.4f}                    {RHO ** 2 + LEG ** 2:.4f}",
                      ACCENT_A),
                     (f"     ‖ α − ξ ‖  =  {D:.4f}   >   {RHO:.4f}", WARN)),
                    y0=0.80, dy=0.36))
  g.add(self._mid(-0.86, "直角就在垂足那裡",
                  "the right angle sits at the foot", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("一個方向直接用畢氏定理：α 減 ξ 的平方，等於 α 減 μ 的平方加上 μ 減 ξ 的平方",
                          "one direction is the Pythagorean theorem: the square of the distance to any other point splits into the two squares",
                          ACCENT_A,
                          "第二項只有在 ξ 就是 μ 的時候才是零，所以最近的點只有一個——這也順便把唯一性證掉了",
                          "the second term vanishes only when that point is the foot, so the closest point is unique, which the same line proves"))

 def _converse(self):
  ox, oy, sx, sy = -5.20, -0.38, 2.30, 0.62
  g = VGroup(self._frame(ox, oy, sx * 1.30, 1.05, down=0.72, back=sx * 0.28))
  g.add(self._fcurve(ox, oy, sx, sy, qwrong, WARN, t0=-0.25, t1=1.20, n=80),
        self._fcurve(ox, oy, sx, sy, qright, ACCENT_B, t0=-0.25, t1=1.20, n=80))
  g.add(Dot([ox + sx * T_MIN, oy + sy * Q_MIN, 0], radius=0.065, color=WARN))
  g.add(self._sym(oy + sy * Q_MIN + 0.24, f"{Q_MIN:.4f}", WARN, FS_TAG - 2,
                  x=ox + sx * T_MIN, w=1.00))
  g.add(self._sym(oy + sy * qright(1.15) + 0.22, "μ", ACCENT_B, FS_TAG - 1,
                  x=ox + sx * 1.15 + 0.26, w=0.70),
        self._sym(oy + sy * qwrong(1.15) + 0.24, "μ ′", WARN, FS_TAG - 1,
                  x=ox + sx * 1.15 + 0.28, w=0.80))
  g.add(self._table((("     q ( t )   =   2 t ( α − · , ξ )  +  t ² ‖ ξ ‖ ²", DIM),
                     (f"     μ ′ :   ( α − μ ′ , ξ )   =   {QB:.4f}", WARN),
                     (f"     t  =  {T_MIN:.4f}      q  =  {Q_MIN:.4f}   <   0", WARN),
                     (f"     μ :   ( α − μ , ξ )   =   {dot(RES, ETA):.0e}", ACCENT_B),
                     (f"     q ( t )  =  {QA:.4f} t ²   ≥   0", ACCENT_B)),
                    y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "紅色那條掉到零以下，就表示可以走得更近",
                  "the red curve dips below zero, so one can get closer", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("反過來的證明：如果 μ 最近，那 0 ≤ 2t ( α − μ , ξ ) + t ² ‖ ξ ‖ ² 對每個實數 t 都要成立",
                          "the converse: if the point is closest, that quadratic must be non-negative for every real t",
                          ACCENT_A,
                          f"內積不是零的話，取跟它反號的 t 就會讓式子變負（紅色那條在 t = {T_MIN:.2f} 掉到 {Q_MIN:.4f}）——所以內積只能是零",
                          f"if the product were nonzero, a t of the opposite sign makes it negative, as the red curve does at {T_MIN:.2f}, so the product must vanish"))

 def _sequence(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  g.add(self._pt(cx, cy, s, AL, ACCENT_A))
  for (n, v, d), col in zip(MSEQ, (DIM, DIM, ACCENT_C, ACCENT_C, WARN)):
   g.add(self._pt(cx, cy, s, v, col, r=0.05), self._seg(cx, cy, s, AL, v, col, n=6, sw=1.0))
  g.add(self._pt(cx, cy, s, MU, WARN, r=0.07))
  g.add(self._lab(cx, cy, s, AL, "α", ACCENT_A, dx=0.02, dy=0.28),
        self._lab(cx, cy, s, MU, "μ", WARN, dx=0.10, dy=-0.30))
  g.add(self._table((("       n        ‖ α − μ ₙ ‖", DIM),)
                    + tuple((f"     {n:3d}          {d:.4f}", ACCENT_C)
                            for n, _v, d in MSEQ)
                    + ((f"     ρ            {RHO:.4f}", WARN),), y0=0.90, dy=0.25,
                    size=FS_TAG - 3))
  g.add(self._mid(-0.86, "距離往 ρ 掉，點往垂足靠",
                  "the distances fall to rho and the points close in on the foot",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("找垂足的辦法：取 M 裡一列 μ ₙ，讓它們到 α 的距離趨近 M 到 α 的距離 ρ，再把 μ 定義成極限",
                          "how to look for the foot: take a sequence in M whose distances tend to the distance from the vector to M, and define the foot as its limit",
                          ACCENT_A,
                          "關鍵就在這裡：這種序列一定是 Cauchy 的（下一拍），可是 M 不完備的時候，那個極限可能不存在",
                          "and here is the crux: such a sequence is always Cauchy, as the next beat shows, but its limit need not exist when M is not complete"))

 def _cauchy(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  a, b = mu_n(NP), mu_n(MP)
  g.add(self._pt(cx, cy, s, AL, ACCENT_A))
  for v, col, lab, off in ((a, ACCENT_C, "μ ₙ", (0.26, -0.32)),
                           (b, WARN, "μ ₘ", (0.80, -0.02)), (MID, INK, "", None)):
   g.add(self._pt(cx, cy, s, v, col, r=0.06), self._seg(cx, cy, s, AL, v, col, n=6, sw=1.2))
   if lab:
    g.add(self._lab(cx, cy, s, v, lab, col, dx=off[0], dy=off[1], w=1.00))
  g.add(self._table((("     ‖ μ ₙ − μ ₘ ‖ ²          2 ( … )  −  ‖ 2 α − ( μ ₙ + μ ₘ ) ‖ ²", DIM),
                     (f"        {PAR_L:.6f}                        {PAR_R:.6f}", ACCENT_C),
                     (f"     ‖ α − ( μ ₙ + μ ₘ ) / 2 ‖   =   {MID_D:.4f}", ACCENT_B),
                     (f"     ρ   =   {RHO:.4f}", WARN)), y0=0.80, dy=0.36))
  g.add(self._mid(-0.86, "白色那個中點也在 M 裡，所以它的距離至少是 ρ",
                  "the white midpoint lies in M too, so its distance is at least rho", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理 2.2 的證明就是平行四邊形法則，寫在 α 減 μ ₙ 與 α 減 μ ₘ 這兩個向量上",
                          "the proof of lemma 2.2 is the parallelogram law, written for those two difference vectors",
                          ACCENT_A,
                          "前面那項趨近 4ρ ²，後面那項永遠至少 4ρ ²，兩邊一夾，μ ₙ 減 μ ₘ 就趨近零——序列是 Cauchy 的",
                          "the first term tends to four rho squared and the second is always at least that, so the difference of the two terms goes to zero"))

 def _theorem21(self):
  ox, oy, sx, sy = -5.70, -0.25, 0.95, 0.52
  g = VGroup(self._frame(ox, oy, 3.10, 1.05, down=0.34))
  g.add(self._fcurve(ox, oy, sx, sy, alpha, ACCENT_A),
        self._fcurve(ox, oy, sx, sy, proj(3), WARN),
        self._fcurve(ox, oy, sx, sy, lambda t: alpha(t) - proj(3)(t), ACCENT_C, sw=2.0))
  g.add(self._sym(oy + sy * alpha(0.88) + 0.40, "α", ACCENT_A, FS_TAG - 1,
                  x=ox + sx * 0.88, w=0.70),
        self._sym(oy - sy * 1.05, "α − P α", ACCENT_C, FS_TAG - 2,
                  x=ox + sx * 1.55, w=1.40))
  g.add(self._table((("     ( α − P α ,  sin k t )", DIM),)
                    + tuple((f"     k  =  {k}          {v:.0e}", ACCENT_C)
                            for k, v in ORTH)
                    + ((f"     ‖ α − P α ‖   =   {FRHO:.4f}", ACCENT_A),), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "剩下來那一條跟 M 裡每一個都垂直",
                  "what is left is orthogonal to everything in M", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 2.1：M 完備時 V 就分解成 M 與它的正交補的直和。這裡 M 是 sin t、sin 2t、sin 3t 張成的三維子空間",
                          "theorem 2.1: when M is complete the space splits as that direct sum, and here M is the three-dimensional span of the first three sines",
                          ACCENT_A,
                          "有限維子空間一定完備，所以這個分解一定成立——紫色那條就是 α 減掉投影之後剩下的部分",
                          "a finite-dimensional subspace is always complete, so the decomposition always holds, and the purple curve is what is left after subtracting the projection"))

 def _projection(self):
  cx, cy, s = -4.35, -0.52, 0.84
  g = self._stage(cx, cy, s)
  TWO = (AL, (1.55, 1.05))
  for v, col in zip(TWO, (ACCENT_A, ACCENT_C)):
   x = dot(v, ETA) / dot(ETA, ETA)
   f = (x * ETA[0], x * ETA[1])
   g.add(self._pt(cx, cy, s, v, col), self._pt(cx, cy, s, f, WARN, r=0.055),
         self._seg(cx, cy, s, v, f, col, n=6, sw=1.2))
  g.add(self._lab(cx, cy, s, TWO[0], "ξ ₁", ACCENT_A, dx=0.04, dy=0.28, w=1.00),
        self._lab(cx, cy, s, TWO[1], "ξ ₂", ACCENT_C, dx=0.26, dy=0.24, w=1.00))
  g.add(self._panel(((0.86, "沿正交補到 M 的那個投影",
                      "the projection on M along the orthogonal complement", ACCENT_B),
                     (0.20, "在各種補空間給出的投影裡是被挑出來的",
                      "among the projections on M it is the distinguished one", ACCENT_C),
                     (-0.46, "因為它同時是垂足與最佳近似",
                      "because it is at once the foot and the best approximation", WARN))))
  return g.add(self._foot("紅色那兩個點是同一個投影 P 作用在兩個向量上的像——P 把整個空間壓到 M 上，而且壓兩次跟壓一次一樣",
                          "the two red dots are the images of one and the same projection, which takes the whole space onto M and does nothing more when applied twice",
                          ACCENT_A,
                          "「投影」這個字就是從垂足來的：P(ξ) 是從 ξ 落到 M 的垂足，也是 M 裡離 ξ 最近的那一點",
                          "the word projection comes from the foot of the perpendicular: the image is the foot, and also the closest point of M"))

 def _lemma23(self):
  ox, oy, sx, sy = -5.70, -0.25, 0.95, 0.52
  g = VGroup(self._frame(ox, oy, 3.10, 1.05, down=0.34))
  for i, col in zip(range(3), (ACCENT_B, ACCENT_C, DIM)):
   g.add(self._fcurve(ox, oy, sx, sy, lambda t, i=i: FC[i] * SIN[i][1](t), col, sw=1.8))
  g.add(self._fcurve(ox, oy, sx, sy, proj(3), WARN, sw=2.6))
  g.add(self._table((("     P ᵢ α   =   ( α , φ ᵢ ) / ‖ φ ᵢ ‖ ²  ·  φ ᵢ", DIM),
                     (f"     ‖ P α  −  Σ ᵢ P ᵢ α ‖   =   {L23:.0e}", ACCENT_A),
                     (f"     ( α − P α , φ ᵢ )   ≤   {max(abs(v) for _k, v in ORTH):.0e}",
                      ACCENT_C),
                     ("     M ᵢ  ⊥  M ⱼ        i  ≠  j", ACCENT_B)), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "三條加起來就是那條粗的",
                  "the three thin curves add up to the thick one", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("引理 2.3：有限多個完備、兩兩正交的子空間，把 α 在每一個上面的投影加起來，就是 α 在直和上的投影",
                          "lemma 2.3: for finitely many complete, pairwise orthogonal subspaces, the projections on each add up to the projection on the direct sum",
                          ACCENT_A,
                          "證明只要對每一個子空間分別驗證垂直，而交叉項因為兩兩正交全都是零",
                          "the proof only checks orthogonality against each subspace separately, and the cross terms vanish because the subspaces are orthogonal"))

 def _fourier(self):
  ox, oy, sx, sy = -5.70, -0.25, 0.95, 0.52
  g = VGroup(self._frame(ox, oy, 3.10, 1.05, down=0.34))
  g.add(self._fcurve(ox, oy, sx, sy, alpha, ACCENT_A))
  for n, col in zip((1, 2, 3), (DIM, ACCENT_C, WARN)):
   g.add(self._fcurve(ox, oy, sx, sy, proj(n), col, sw=1.8 if n < 3 else 2.4))
  g.add(self._sym(oy + sy * alpha(0.88) + 0.40, "α", ACCENT_A, FS_TAG - 1,
                  x=ox + sx * 0.88, w=0.70))
  g.add(self._table((("       i        x ᵢ            ‖ α − P ᵢ α ‖", DIM),)
                    + tuple((f"      {i + 1}      {FC[i]:.4f}          {PD[i][1]:.4f}",
                             (DIM, ACCENT_C, WARN)[i]) for i in range(3))
                    + ((f"     ( ξ , η ) / ‖ η ‖ ²   ·   η", ACCENT_A),), y0=0.86, dy=0.34))
  g.add(self._mid(-0.90, "多一個基向量，就只會更近",
                  "one more basis vector can only bring it closer", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot(f"引理 2.4：到 η 張成的一維子空間的投影是 ( ξ , η ) / ‖ η ‖ ² 乘 η，那個係數就叫 Fourier 係數",
                          f"lemma 2.4: the projection on the span of a single vector is that quotient times the vector, and the number is the Fourier coefficient",
                          ACCENT_A,
                          f"這裡的 α 是拿四個正弦組出來的，而積分把前三個係數原封不動還回來（{FC[0]:.4f}、{FC[1]:.4f}、{FC[2]:.4f}）；剩下那一個正弦不在 M 裡，就是 ρ = {FRHO:.4f}",
                          f"the target here was built from four sines, and the integral returns the first three coefficients unchanged; the fourth is not in M, and it is exactly the residual, {FRHO:.4f}"))

 def stage(self):
  a, b, c = self._opening(), self._decomp(), self._lemma21()
  d, e, f_ = self._pythagoras(), self._converse(), self._sequence()
  h, i, j = self._cauchy(), self._theorem21(), self._projection()
  k, l = self._lemma23(), self._fourier()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f_], [e]), ([h], [f_]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE69ZH, AdvCalcE69EN = make(AdvCalcE69Base, "69", prefix="AdvCalcE")
