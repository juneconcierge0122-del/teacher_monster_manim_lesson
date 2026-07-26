"""Lesson 34 — The equations of motion of a rigid body (Landau §34).

Stage A (beats 0-2) is translation: a tumbling body whose centre of mass flies
along a parabola under a constant total force, with the internal force pairs
drawn cancelling, then the same body inside a potential well where F is minus
the gradient of U. Stage B (beats 3-5) is torque: a force through the centre of
mass beside the same force off centre, then a live bar readout of
K = K' + a x F while the origin slides, and the couple whose vanishing F
flattens that readout. Stage C (beats 6-9) closes with K = -dU/dphi for a
needle in a field, the line of action along which one equivalent force may be
slid, and the uniform field whose weighted average point is the centre of mass.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arc, Arrow, Circle, DashedVMobject, Dot, FadeIn, FadeOut, Line,
                   Polygon, Rectangle, Text, VGroup, VMobject, ValueTracker, always_redraw,
                   linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 20
BS = 0.78                                   # body scale


def _b(x, y):
 return np.array([BS * x, BS * y, 0.0])


BV = [_b(-1.10, -0.60), _b(0.32, -0.92), _b(1.16, -0.06),
      _b(0.86, 0.74), _b(-0.26, 0.98), _b(-1.06, 0.42)]
# The four x-coordinates are kept well apart so the beat-9 balance beam, which
# only sees x, never draws two loads on top of each other.
PARTS = [_b(-0.72, -0.30), _b(0.20, -0.60), _b(0.66, 0.30), _b(-0.30, 0.62)]
MASSES = [0.55, 1.10, 0.80, 0.45]           # beat 8-9: the coefficients e_i

# ── beat 1: the parabolic flight of the centre of mass ────────────────
P0 = np.array([-4.55, -0.95, 0.0]); V0 = np.array([1.30, 0.85, 0.0])
ACC = np.array([0.0, -0.235, 0.0]); SMAX = 7.0
FEXT = [np.array([0.34, -0.58, 0.0]), np.array([-0.34, -0.42, 0.0])]  # they sum to -1 in y
FSC = 0.80                                  # screen length per unit of force

# ── beat 2: the potential well ────────────────────────────────────────
WC = np.array([0.0, -0.15, 0.0]); WA = 3.50; WB = 1.42

# ── beats 4-5: torque about a shifted origin ──────────────────────────
BC4 = np.array([-3.55, 0.15, 0.0])
PA1 = _b(-0.55, 0.62); PA2 = _b(0.70, 0.30)  # PA2 sits above the track O′ slides along
FV = 1.20 * np.array([-0.744, -0.668, 0.0])  # perpendicular to PA1, so r x f is large
AMAX = 2.70
BAR_X0 = 2.90; BAR_SC = 0.72

# ── beat 6: a needle in a uniform field ───────────────────────────────
LC6 = np.array([-3.60, 0.10, 0.0]); UC = np.array([3.30, 0.10, 0.0])
UAMP = 0.85; UPHI = 4.80 / (2 * PI)          # screen length per radian of phi

# ── beat 7: the line of action ────────────────────────────────────────
C7 = np.array([-1.60, 0.10, 0.0])
P7 = [_b(-0.65, 0.50), _b(0.58, 0.45), _b(0.10, -0.70)]
F7 = [np.array([0.30, 0.55, 0.0]), np.array([0.42, -0.20, 0.0]),
      np.array([0.35, 0.30, 0.0])]

# ── beats 8-9: the uniform field ──────────────────────────────────────
C8 = np.array([-2.90, 0.10, 0.0]); PIV = np.array([-2.50, 1.45, 0.0]); PIVB = _b(0.13, 1.35)
BEAM_X = 3.40; BEAM_SC = 2.60


def _rot(v, ph):
 c, s = np.cos(ph), np.sin(ph)
 return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


def _place(v, R, ph):
 return R + _rot(v, ph)


def _crossz(a, b):
 return float(a[0] * b[1] - a[1] * b[0])


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-9 else 1.0)


class RigidEOMBase(LandauBatchBase):
 EPISODE = 34; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "六個自由度 ⇒ 六條方程", "en": "six degrees of freedom, six equations"},
               1: {"zh": "內力成對抵消，只剩外力", "en": "internal forces cancel in pairs"},
               2: {"zh": "勢能對質心座標的梯度", "en": "the gradient of U in the coordinates of R"},
               3: {"zh": "力矩 = 位置 × 力", "en": "torque = position × force"},
               4: {"zh": "力矩與原點的選擇有關", "en": "the torque depends on the origin"},
               5: {"zh": "力偶：不推質心，只轉物體", "en": "a couple: no push, only turning"},
               6: {"zh": "力矩是勢能對轉角的負斜率", "en": "torque is minus the slope of U in φ"},
               7: {"zh": "化成沿一條直線作用的單一個力", "en": "one force along a single line"},
               8: {"zh": "均勻場：每個質點受同方向的力", "en": "uniform field: parallel forces everywhere"},
               9: {"zh": "重力的效果集中在質心", "en": "gravity acts at the centre of mass"}}

 # ── drawing helpers ───────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _arr(self, start, tip, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(tip) - np.asarray(start))) < 0.05:
   return VGroup()
  return Arrow(start, tip, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off))
  return m

 def _body(self, R, ph, color=ACCENT_A, op=0.10, sw=3):
  return Polygon(*[_place(v, R, ph) for v in BV], color=color, stroke_width=sw,
                 fill_opacity=op, fill_color=color)

 def _spin_arrow(self, centre, radius, color, start=-0.55, ang=2.5, sw=4):
  a = Arc(radius=radius, arc_center=centre, start_angle=start, angle=ang,
          color=color, stroke_width=sw)
  a.add_tip(tip_length=0.20)
  return a

 def _dash(self, a, b, color, n=14, sw=2.5):
  """A dashed segment whose submobject count never changes.

  DashedLine derives its number of dashes from its length, so a stretching one
  inside an always_redraw keeps changing its family size. FadeIn aligns the
  families of a whole VGroup once, and a member that changes shape underneath
  it knocks the alignment out — glyphs of neighbouring Text then silently stop
  being drawn. A fixed dash count keeps the family stable.
  """
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _sbar(self, x0, y, val, color, h=0.22):
  w = max(abs(val), 0.02)
  return Rectangle(width=w, height=h, color=color, fill_opacity=0.85,
                   stroke_width=0).move_to([x0 + val / 2, y, 0])

 def _field(self, xs, y0, y1, horiz=False, color=DIM, sw=1.5):
  """A uniform field drawn as parallel lines, each carrying one small head."""
  g = VGroup()
  for x in xs:
   if horiz:
    g.add(Line([y0, x, 0], [y1, x, 0], color=color, stroke_width=sw))
    g.add(self._arr([(y0 + y1) / 2, x, 0], [(y0 + y1) / 2 + 0.24, x, 0], color, sw=sw, tl=0.13))
   else:
    g.add(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=sw))
    g.add(self._arr([x, (y0 + y1) / 2, 0], [x, (y0 + y1) / 2 - 0.24, 0], color, sw=sw, tl=0.13))
  return g

 # ── geometry that the updaters read ───────────────────────────────
 def _flightR(self):
  s = SMAX * self.pa.get_value()
  return P0 + V0 * s + 0.5 * ACC * s * s

 def _wellR(self):
  th = np.deg2rad(150.0 + 8.0 * np.sin(0.35 * self.t.get_value()))
  u = 1.0 - 0.14 * (0.5 + 0.5 * np.sin(0.50 * self.t.get_value()))
  return WC + u * np.array([WA * np.cos(th), WB * np.sin(th), 0.0])

 def _wellF(self):
  d = self._wellR() - WC
  return -1.15 * _unit(np.array([d[0] / WA ** 2, d[1] / WB ** 2, 0.0]))

 def _forces(self):
  """Beats 4-5: the applied forces, the second one blended in by `cp`."""
  cp = self.cp.get_value()
  return [(PA1, FV), (PA2, -cp * FV)]

 def _KKa(self):
  """Beats 4-5: the torque about O, the torque about O', and a x F."""
  a = np.array([AMAX * (0.5 + 0.5 * np.sin(0.50 * self.t.get_value())), 0.0, 0.0])
  F = sum((f for _, f in self._forces()), np.zeros(3))
  K = sum(_crossz(p, f) for p, f in self._forces())
  return K, K - _crossz(a, F), _crossz(a, F), a

 def _phi6(self):
  return 1.05 * np.sin(0.45 * self.t.get_value())

 def _upt(self, phi):
  return UC + np.array([UPHI * phi, -UAMP * np.cos(phi), 0.0])

 def _line7(self):
  F = sum(F7, np.zeros(3)); K = sum(_crossz(p, f) for p, f in zip(P7, F7))
  q0 = K * np.array([F[1], -F[0], 0.0]) / float(np.dot(F[:2], F[:2]))
  return C7 + q0, _unit(F), F

 def _tail7(self):
  q0, u, _ = self._line7()
  return q0 + u * (-1.10 + 1.70 * np.sin(0.45 * self.t.get_value()))

 def _r0(self):
  return sum(m * p for m, p in zip(MASSES, PARTS)) / sum(MASSES)

 def _phi9(self):
  return 0.50 * np.sin(0.55 * self.t.get_value())

 def _R9(self):
  return PIV - _rot(PIVB, self._phi9())

 # ── beat plumbing ─────────────────────────────────────────────────
 def beat(self, i, fin=(), fout=(), extra=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  r = min(0.5, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate(rate_func=linear).increment_value(r), run_time=r)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate(rate_func=linear).increment_value(d), *extra, run_time=d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * (2.35 - 0.22 * max(0, len(s.split(chr(10))) - 2)))

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.t = ValueTracker(0.0)
  self.pa = ValueTracker(0.0)               # progress along the parabola
  self.sp = ValueTracker(0.0)               # local clock for the spin-up
  self.cp = ValueTracker(0.0)               # how much of the couple is switched on
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ beat 0: two vector equations ══════════════════════════════════
  A0 = np.array([-3.55, 0.05, 0.0])
  body0 = always_redraw(lambda: self._body(A0, 0.30 * self.t.get_value()))
  parts0 = always_redraw(lambda: VGroup(*[
   Dot(_place(p, A0, 0.30 * self.t.get_value()), color=ACCENT_A, radius=0.065) for p in PARTS]))
  cm0 = Dot(A0, color=INK, radius=0.075)
  cm0t = Text("O", font_size=FS_SMALL, color=DIM).move_to(A0 + np.array([-0.24, -0.20, 0.0]))
  pu = _unit(np.array([0.80, 0.45, 0.0]))
  parr = self._arr(A0, A0 + 1.30 * pu, ACCENT_B, sw=5)
  ptag = Text("P", font_size=FS_TAG, color=ACCENT_B).move_to(A0 + 1.30 * pu
                                                             + np.array([0.24, 0.16, 0.0]))
  marc = self._spin_arrow(A0, 1.42, ACCENT_C)
  mtag = Text("M", font_size=FS_TAG, color=ACCENT_C).move_to(A0 + np.array([-1.02, -1.12, 0.0]))
  rows0 = VGroup(
   self._arr([1.45, 0.80, 0], [2.15, 0.80, 0], ACCENT_B, sw=4, tl=0.16),
   self.lab("3 個平移自由度", "3 translations", FS_BODY, INK)
   .move_to([2.35, 0.80, 0], aligned_edge=LEFT),
   self._spin_arrow([1.80, -0.10, 0], 0.34, ACCENT_C, sw=3.5),
   self.lab("3 個轉動自由度", "3 rotations", FS_BODY, INK)
   .move_to([2.35, -0.10, 0], aligned_edge=LEFT),
   self.lab("六條運動方程", "six equations of motion", FS_BODY, ACCENT_A)
   .move_to([1.45, -1.05, 0], aligned_edge=LEFT))
  stage0 = VGroup(parr, ptag, marc, mtag, rows0)

  # ══ beat 1: the flight of the centre of mass ══════════════════════
  path = VMobject(color=GHOST, stroke_width=3)
  path.set_points_as_corners([P0 + V0 * s + 0.5 * ACC * s * s
                              for s in np.linspace(0, SMAX, 80)])
  path = DashedVMobject(path, num_dashes=52, color=GHOST)
  ph1 = lambda: 0.30 * self.t.get_value()
  body1 = always_redraw(lambda: self._body(self._flightR(), ph1()))
  parts1 = always_redraw(lambda: VGroup(*[
   Dot(_place(p, self._flightR(), ph1()), color=ACCENT_A, radius=0.065) for p in PARTS]))
  cm1 = always_redraw(lambda: Dot(self._flightR(), color=INK, radius=0.075))
  farr = always_redraw(lambda: self._arr(self._flightR(),
                                         self._flightR() + FSC * np.array([0.0, -1.0, 0.0]),
                                         ACCENT_B, sw=6, tl=0.22))
  ftag = self._tag("F", lambda: self._flightR() + FSC * np.array([0.0, -1.0, 0.0]),
                   off=np.array([0.28, -0.10, 0.0]), color=ACCENT_B)
  ext = always_redraw(lambda: VGroup(*[
   self._arr(_place(p, self._flightR(), ph1()),
             _place(p, self._flightR(), ph1()) + FSC * f, ACCENT_C, sw=4, tl=0.16)
   for p, f in zip((PARTS[0], PARTS[2]), FEXT)]))

  def _pairs():
   R, ph = self._flightR(), ph1()
   g = VGroup()
   for i, k in ((0, 1), (1, 2), (2, 3), (3, 0)):
    p, q = _place(PARTS[i], R, ph), _place(PARTS[k], R, ph)
    u = _unit(q - p)
    g.add(Line(p, q, color=GHOST, stroke_width=1.5))
    g.add(self._arr(p + 0.26 * (q - p), p + 0.26 * (q - p) + 0.28 * u, WARN, sw=3.5, tl=0.13))
    g.add(self._arr(q - 0.26 * (q - p), q - 0.26 * (q - p) - 0.28 * u, WARN, sw=3.5, tl=0.13))
   return g
  pairs = always_redraw(_pairs)
  stage1 = VGroup(path, body1, parts1, cm1, farr, ftag, ext, pairs)

  # ══ beat 2: the body in a potential well ══════════════════════════
  cont = VGroup(*[VMobject(color=GHOST, stroke_width=2.5).set_points_as_corners(
   [WC + np.array([k * WA * np.cos(a), k * WB * np.sin(a), 0.0])
    for a in np.linspace(0, 2 * PI, 96)]) for k in (0.42, 0.71, 1.0)])
  wmin = Dot(WC, color=ACCENT_B, radius=0.075)
  wmint = self.lab("U 最小", "U is least", FS_SMALL, DIM).move_to(WC + np.array([0.0, -0.34, 0]))
  body2 = always_redraw(lambda: self._body(self._wellR(), 0.24 * self.t.get_value()))
  cm2 = always_redraw(lambda: Dot(self._wellR(), color=INK, radius=0.075))
  f2 = always_redraw(lambda: self._arr(self._wellR(), self._wellR() + self._wellF(),
                                       ACCENT_B, sw=6, tl=0.22))
  f2t = self._tag("F", lambda: self._wellR() + self._wellF(),
                  off=np.array([0.26, -0.16, 0.0]), color=ACCENT_B)
  dr = always_redraw(lambda: self._dash(self._wellR(), self._wellR() + 0.55 * self._wellF(),
                                        WARN, n=5, sw=4))
  drt = self._tag("δR", lambda: self._wellR() + 0.55 * self._wellF(),
                  off=np.array([-0.38, 0.06, 0.0]), color=WARN, size=FS_SMALL)
  cont_t = self.lab("等勢面", "curves of constant U", FS_SMALL, DIM).move_to([4.55, 0.95, 0])
  stage2 = VGroup(cont, wmin, wmint, body2, cm2, f2, f2t, dr, drt, cont_t)

  # ══ beat 3: with and without a torque ═════════════════════════════
  LC, RC = np.array([-3.45, 0.05, 0.0]), np.array([2.45, 0.05, 0.0])
  uf = _unit(np.array([np.cos(0.44), np.sin(0.44), 0.0]))
  lbody = VGroup(self._body(LC, 0.0),
                 *[Dot(_place(p, LC, 0.0), color=ACCENT_A, radius=0.065) for p in PARTS],
                 Dot(LC, color=INK, radius=0.075),
                 self._arr(LC - 1.25 * uf, LC, ACCENT_C, sw=5),
                 Text("f", font_size=FS_TAG, color=ACCENT_C)
                 .move_to(LC - 1.25 * uf + np.array([-0.10, -0.28, 0.0])),
                 Text("O", font_size=FS_SMALL, color=DIM).move_to(LC + np.array([0.26, -0.22, 0])),
                 self.lab("力通過質心：沒有力矩", "force through O: no torque", FS_SMALL, DIM)
                 .move_to(LC + np.array([0.0, -1.45, 0.0])))
  ph3 = lambda: 0.16 * self.sp.get_value() + 0.010 * self.sp.get_value() ** 2
  papp = lambda: _place(_b(0.62, 0.55), RC, ph3())
  # A tangential grip: the torque it exerts is constant, which is what spins the
  # body up, and the arrow never points back across the centre of mass.
  uf3 = lambda: _unit(_rot(papp() - RC, PI / 2))
  rbody = VGroup(
   always_redraw(lambda: self._body(RC, ph3())),
   always_redraw(lambda: VGroup(*[Dot(_place(p, RC, ph3()), color=ACCENT_A, radius=0.065)
                                  for p in PARTS])),
   Dot(RC, color=INK, radius=0.075),
   always_redraw(lambda: self._dash(RC, papp(), GHOST, n=7)),
   always_redraw(lambda: self._arr(papp(), papp() + 1.20 * uf3(), ACCENT_C, sw=5)),
   self._tag("f", lambda: papp() + 1.20 * uf3(), off=np.array([0.16, 0.24, 0.0]),
             color=ACCENT_C),
   self._tag("r", lambda: 0.5 * (RC + papp()), off=np.array([-0.24, 0.14, 0.0]),
             color=DIM, size=FS_SMALL),
   VGroup(Circle(radius=0.26, color=WARN, stroke_width=3).move_to(RC),
          Dot(RC, color=WARN, radius=0.055)),
   Text("r × f", font_size=FS_SMALL, color=WARN).move_to(RC + np.array([0.98, -0.50, 0.0])),
   self.lab("力偏離質心：產生力矩", "force off O: a torque appears", FS_SMALL, DIM)
   .move_to(RC + np.array([0.0, -1.45, 0.0])))
  stage3 = VGroup(lbody, rbody)

  # ══ beats 4-5: the torque about a shifted origin ══════════════════
  body4 = VGroup(self._body(BC4, 0.0),
                 *[Dot(_place(p, BC4, 0.0), color=ACCENT_A, radius=0.065) for p in PARTS])
  o4 = Dot(BC4, color=INK, radius=0.075)
  o4t = Text("O", font_size=FS_SMALL, color=DIM).move_to(BC4 + np.array([-0.26, -0.22, 0.0]))
  op = always_redraw(lambda: Dot(BC4 + self._KKa()[3], color=ACCENT_B, radius=0.075))
  opt = self._tag("O′", lambda: BC4 + self._KKa()[3], off=np.array([0.14, -0.32, 0.0]),
                  color=ACCENT_B, size=FS_SMALL)
  aarr = always_redraw(lambda: self._arr(BC4, BC4 + self._KKa()[3], DIM, sw=3, tl=0.16))
  aart = self._tag("a", lambda: BC4 + 0.5 * self._KKa()[3], off=np.array([0.0, -0.30, 0.0]),
                   color=DIM, size=FS_SMALL)
  f4 = always_redraw(lambda: VGroup(*[
   self._arr(BC4 + p, BC4 + p + f, ACCENT_C, sw=5) for p, f in self._forces()]))
  f4t = Text("f", font_size=FS_TAG, color=ACCENT_C).move_to(BC4 + PA1 + FV
                                                            + np.array([-0.06, -0.30, 0.0]))
  f4t2 = self._tag("− f", lambda: BC4 + PA2 - self.cp.get_value() * FV,
                   off=np.array([0.34, 0.16, 0.0]), color=ACCENT_C, size=FS_SMALL)
  r4 = always_redraw(lambda: self._dash(BC4, BC4 + PA1, ACCENT_A, n=6))
  r4p = always_redraw(lambda: self._dash(BC4 + self._KKa()[3], BC4 + PA1, ACCENT_B, n=12))
  zero = Line([BAR_X0, 1.52, 0], [BAR_X0, -0.98, 0], color=GHOST, stroke_width=2)
  bars = VGroup(
   Text("K", font_size=FS_SMALL, color=ACCENT_A).move_to([BAR_X0 - 0.02, 1.45, 0]),
   always_redraw(lambda: self._sbar(BAR_X0, 1.15, BAR_SC * self._KKa()[0], ACCENT_A)),
   Text("K′", font_size=FS_SMALL, color=ACCENT_B).move_to([BAR_X0 + 0.02, 0.55, 0]),
   always_redraw(lambda: self._sbar(BAR_X0, 0.25, BAR_SC * self._KKa()[1], ACCENT_B)),
   Text("a × F", font_size=FS_SMALL, color=ACCENT_C).move_to([BAR_X0 + 0.24, -0.35, 0]),
   always_redraw(lambda: self._sbar(BAR_X0, -0.65, BAR_SC * self._KKa()[2], ACCENT_C)))
  cap4 = self.lab("原點移動時，K′ 跟著改變", "K′ changes as the origin moves", FS_SMALL, DIM
                  ).move_to([BAR_X0, -1.35, 0])
  cap5 = self.lab("力偶：F = 0，K′ 不再改變", "a couple: F = 0, so K′ stops changing",
                  FS_SMALL, WARN).move_to([BAR_X0, -1.35, 0])
  stage4 = VGroup(body4, o4, o4t, op, opt, aarr, aart, f4, f4t, r4, r4p, zero, bars)

  # ══ beat 6: torque as minus the slope of U ════════════════════════
  fld6 = self._field([LC6[1] + k * 0.62 for k in (-2, -1, 0, 1, 2)], -5.55, -1.65, horiz=True)
  fld6t = Text("E", font_size=FS_SMALL, color=DIM).move_to([-1.40, LC6[1] + 1.24, 0])
  ndl = always_redraw(lambda: VGroup(
   Line(LC6 - 1.00 * _rot(np.array([1.0, 0, 0]), self._phi6()),
        LC6 + 1.00 * _rot(np.array([1.0, 0, 0]), self._phi6()), color=ACCENT_A, stroke_width=6),
   Dot(LC6 + 1.00 * _rot(np.array([1.0, 0, 0]), self._phi6()), color=WARN, radius=0.13),
   Dot(LC6 - 1.00 * _rot(np.array([1.0, 0, 0]), self._phi6()), color=ACCENT_B, radius=0.13)))
  ndlk = always_redraw(lambda: self._spin_arrow(
   LC6, 1.36, ACCENT_C, start=-0.55 if self._phi6() < 0 else 2.60,
   ang=2.2 if self._phi6() < 0 else -2.2, sw=3.5))
  ndlkt = Text("K", font_size=FS_TAG, color=ACCENT_C).move_to(LC6 + np.array([0.0, -1.62, 0.0]))
  phit = always_redraw(lambda: Text("φ", font_size=FS_SMALL, color=DIM).move_to(
   LC6 + 0.52 * _rot(np.array([1.0, 0, 0]), 0.5 * self._phi6()) + np.array([0.0, 0.24, 0.0])))
  ucur = VMobject(color=ACCENT_A, stroke_width=4)
  ucur.set_points_as_corners([self._upt(p) for p in np.linspace(-PI, PI, 120)])
  uax = Line(UC + np.array([-UPHI * PI, 0, 0]), UC + np.array([UPHI * PI, 0, 0]),
             color=GHOST, stroke_width=2)
  uaxt = Text("φ", font_size=FS_SMALL, color=DIM).move_to(UC + np.array([UPHI * PI + 0.26, 0, 0]))
  ucurt = Text("U(φ)", font_size=FS_SMALL, color=ACCENT_A).move_to(UC + np.array([-1.95, 1.12, 0]))
  udot = always_redraw(lambda: Dot(self._upt(self._phi6()), color=WARN, radius=0.09))
  utan = always_redraw(lambda: Line(
   self._upt(self._phi6()) - np.array([0.55, 0.55 * UAMP * np.sin(self._phi6()) / UPHI, 0]),
   self._upt(self._phi6()) + np.array([0.55, 0.55 * UAMP * np.sin(self._phi6()) / UPHI, 0]),
   color=ACCENT_C, stroke_width=3.5))
  ukar = always_redraw(lambda: self._arr(
   self._upt(self._phi6()), self._upt(self._phi6())
   + np.array([-0.90 * np.sign(np.sin(self._phi6()) + 1e-9) * min(1.0, abs(np.sin(self._phi6()))
                                                                  * 1.6 + 0.25), 0, 0]),
   ACCENT_C, sw=4, tl=0.16))
  cap6 = self.lab("斜率越陡，力矩越大", "the steeper the slope, the larger K", FS_SMALL, DIM
                  ).move_to(UC + np.array([0.0, -1.45, 0.0]))
  stage6 = VGroup(fld6, fld6t, ndl, ndlk, ndlkt, phit, uax, uaxt, ucur, ucurt, udot, utan,
                  ukar, cap6)

  # ══ beat 7: the line of action ════════════════════════════════════
  q0, u7, FS7 = self._line7()
  body7 = VGroup(self._body(C7, 0.0),
                 *[Dot(_place(p, C7, 0.0), color=ACCENT_A, radius=0.065) for p in PARTS],
                 Dot(C7, color=INK, radius=0.075),
                 Text("O", font_size=FS_SMALL, color=DIM).move_to(C7 + np.array([-0.26, -0.24, 0])))
  small7 = VGroup(*[self._arr(C7 + p, C7 + p + 1.05 * f, ACCENT_C, sw=3.5, tl=0.15)
                    for p, f in zip(P7, F7)])
  line7 = DashedVMobject(Line(q0 - 3.30 * u7, q0 + 2.05 * u7, color=WARN, stroke_width=2.5),
                         num_dashes=40, color=WARN)
  big7 = always_redraw(lambda: self._arr(self._tail7(), self._tail7() + 1.05 * FS7,
                                         ACCENT_B, sw=6, tl=0.22))
  big7t = self._tag("F", lambda: self._tail7() + 1.05 * FS7, off=np.array([0.28, 0.14, 0.0]),
                    color=ACCENT_B)
  a7 = always_redraw(lambda: self._dash(C7, self._tail7(), DIM, n=14))
  a7t = self._tag("a", lambda: 0.5 * (C7 + self._tail7()), off=np.array([-0.02, -0.28, 0.0]),
                  color=DIM, size=FS_SMALL)
  cap7 = self.lab("在這條作用線上，力矩都一樣", "same torque anywhere on this line",
                  FS_SMALL, WARN).move_to([-2.10, -1.58, 0])
  # The right half builds the same resultant tip to tail, so it is clear where the
  # single equivalent force came from.
  chain = VGroup(); tip = np.array([2.00, -0.75, 0.0])
  for f in F7:
   chain.add(self._arr(tip, tip + 2.20 * f, ACCENT_C, sw=4, tl=0.16)); tip = tip + 2.20 * f
  chain.add(self._arr([2.00, -0.75, 0], tip, ACCENT_B, sw=6, tl=0.22))
  chain.add(Text("Σ f = F", font_size=FS_SMALL, color=ACCENT_B).move_to([2.20, 0.95, 0]))
  cap7b = self.lab("三個力的合力", "the resultant of the three forces", FS_SMALL, DIM
                   ).move_to([3.20, -1.45, 0])
  stage7 = VGroup(body7, small7, line7, big7, big7t, a7, a7t, cap7, chain, cap7b)

  # ══ beat 8: the uniform field ═════════════════════════════════════
  fld8 = self._field([-5.9 + 1.15 * k for k in range(6)], 1.55, -1.55)
  fld8t = Text("E", font_size=FS_SMALL, color=DIM).move_to([-5.9, 1.80, 0])
  ph8 = lambda: 0.22 * self.t.get_value()
  body8 = always_redraw(lambda: self._body(C8, ph8()))
  parts8 = always_redraw(lambda: VGroup(*[
   Dot(_place(p, C8, ph8()), color=ACCENT_A, radius=0.055 + 0.055 * m)
   for p, m in zip(PARTS, MASSES)]))
  wts8 = always_redraw(lambda: VGroup(*[
   self._arr(_place(p, C8, ph8()), _place(p, C8, ph8()) + np.array([0.0, -0.55 * m, 0.0]),
             WARN, sw=4, tl=0.15) for p, m in zip(PARTS, MASSES)]))
  r0dot = always_redraw(lambda: Dot(_place(self._r0(), C8, ph8()), color=ACCENT_B, radius=0.095))
  r0t = self._tag("r₀", lambda: _place(self._r0(), C8, ph8()), off=np.array([0.30, 0.20, 0.0]),
                  color=ACCENT_B, size=FS_SMALL)
  col = VGroup(); yy = 1.15
  for m in MASSES:
   col.add(self._arr([3.20, yy, 0], [3.20, yy - 0.55 * m, 0], WARN, sw=4, tl=0.15))
   yy -= 0.55 * m + 0.06
  col.add(self._arr([4.30, 1.15, 0], [4.30, 1.15 - 0.55 * sum(MASSES), 0], ACCENT_B,
                    sw=6, tl=0.22))
  col.add(Text("Σ f = F", font_size=FS_SMALL, color=ACCENT_B).move_to([3.80, -0.95, 0]))
  stage8 = VGroup(fld8, fld8t, body8, parts8, wts8, r0dot, r0t, col)

  # ══ beat 9: the weight acts at the centre of mass ═════════════════
  rod = always_redraw(lambda: Line(PIV, _place(self._r0(), self._R9(), self._phi9()),
                                   color=DIM, stroke_width=3))
  piv = VGroup(Dot(PIV, color=INK, radius=0.085),
               Line(PIV + np.array([-0.30, 0.14, 0]), PIV + np.array([0.30, 0.14, 0]),
                    color=GHOST, stroke_width=4))
  body9 = always_redraw(lambda: self._body(self._R9(), self._phi9()))
  parts9 = always_redraw(lambda: VGroup(*[
   Dot(_place(p, self._R9(), self._phi9()), color=ACCENT_A, radius=0.055 + 0.055 * m)
   for p, m in zip(PARTS, MASSES)]))
  cm9 = always_redraw(lambda: Dot(_place(self._r0(), self._R9(), self._phi9()),
                                  color=ACCENT_B, radius=0.095))
  w9 = always_redraw(lambda: self._arr(
   _place(self._r0(), self._R9(), self._phi9()),
   _place(self._r0(), self._R9(), self._phi9()) + np.array([0.0, -1.15, 0.0]),
   ACCENT_B, sw=6, tl=0.22))
  w9t = self._tag("F", lambda: _place(self._r0(), self._R9(), self._phi9())
                  + np.array([0.0, -1.15, 0.0]), off=np.array([0.28, -0.06, 0.0]),
                  color=ACCENT_B)
  cap9 = self.lab("重力等效成質心上的一支箭頭", "gravity becomes one arrow at the centre of mass",
                  FS_SMALL, DIM).move_to([-2.60, -1.45, 0])
  beam = Line([BEAM_X - 2.10, -0.20, 0], [BEAM_X + 2.10, -0.20, 0], color=ACCENT_A, stroke_width=4)
  loads = VGroup()
  for p, m in zip(PARTS, MASSES):
   r = 0.13 + 0.13 * m
   loads.add(Circle(radius=r, color=WARN, stroke_width=3, fill_opacity=0.20, fill_color=WARN)
             .move_to([BEAM_X + BEAM_SC * p[0], -0.20 + r, 0]))
  fx = BEAM_X + BEAM_SC * self._r0()[0]
  ful = VGroup(Polygon([fx, -0.24, 0], [fx - 0.24, -0.66, 0], [fx + 0.24, -0.66, 0],
                       color=ACCENT_B, stroke_width=3, fill_opacity=0.25, fill_color=ACCENT_B),
               Text("r₀", font_size=FS_SMALL, color=ACCENT_B).move_to([fx, -0.92, 0]))
  cap9b = self.lab("加權平均：恰好平衡", "the weighted average balances", FS_SMALL, DIM
                   ).move_to([BEAM_X, -1.45, 0])
  stage9 = VGroup(rod, piv, body9, parts9, cm9, w9, w9t, cap9, beam, loads, ful, cap9b)

  # ── run the beats ─────────────────────────────────────────────────
  active_sub = None; active_f = None

  def run(i, fin=(), fout=(), extra=()):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = list(fin) + [s]; fout = list(fout)
   if active_sub is not None: fout.append(active_sub)
   lang = "zh" if self.LANGUAGE == "zh" else "en"
   bits = []
   if i in self.MODE_LABEL: bits.append(self.MODE_LABEL[i][lang])
   if i in F: bits.append(F[i])
   if bits:
    f = self.formula("\n".join(bits)); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout, extra=extra)
   active_sub = s

  self.add(body0, parts0, cm0, cm0t)
  run(0, fin=[stage0])
  run(1, fin=[stage1], fout=[stage0, body0, parts0, cm0, cm0t],
      extra=[self.pa.animate(rate_func=linear).set_value(1.0)])
  run(2, fin=[stage2], fout=[stage1])
  run(3, fin=[stage3], fout=[stage2],
      extra=[self.sp.animate(rate_func=linear).increment_value(self.dur(3) - 0.5)])
  run(4, fin=[stage4, cap4], fout=[stage3])
  # The couple is switched on over the first third of the beat, so most of it is
  # spent watching O′ slide with the bars already flat.
  run(5, fin=[cap5], fout=[cap4],
      extra=[self.cp.animate(rate_func=lambda x: min(1.0, 3.2 * x)).set_value(1.0)])
  run(6, fin=[stage6], fout=[stage4, cap5])
  run(7, fin=[stage7], fout=[stage6])
  run(8, fin=[stage8], fout=[stage7])
  run(9, fin=[stage9], fout=[stage8])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL34{'ZH' if lang == 'zh' else 'EN'}", (RigidEOMBase,), {"LANGUAGE": lang})


LandauL34ZH = _mk("zh")
LandauL34EN = _mk("en")
