"""Lesson 35 — Eulerian angles (Landau §35).

Everything happens in one axonometric picture of two frames sharing an origin.
Beats 0-2 build it up: the fixed axes, the body axes, the two planes and the
line of nodes where they meet, then the three angles as arcs. Beat 3 runs the
defining sequence — phi about Z, theta about the line of nodes, psi about the
body axis — on a loop. Beats 4-5 hang the three angular-velocity contributions
on their own axes and read their projections off a stacked bar chart. Beats 6-9
dress the body as a symmetrical top, drop psi onto the line of nodes, and
recover the regular precession of §33 from the components of M.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (Arrow, Dot, FadeIn, FadeOut, Line, Polygon, Rectangle, Text, VGroup, VMobject,
                   DashedVMobject, ValueTracker, always_redraw, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19

# ── axonometric projection ────────────────────────────────────────────
EX = np.array([0.80, -0.42, 0.0])           # fixed X, to the lower right
EY = np.array([-0.66, -0.34, 0.0])          # fixed Y, to the lower left
EZ = np.array([0.0, 1.0, 0.0])              # fixed Z, straight up
ORG = np.array([-2.25, -0.65, 0.0]); PS = 1.05
# Kept short enough that the Z and x3 labels clear the bottom of a three-line
# formula (beats 5 and 8) while the X label stays above the subtitle.
L = 1.50                                    # axis length
LT = 1.12                                   # label radius, in units of L
RP = 1.35                                   # radius of the two plane rings

PHI0 = np.deg2rad(52.0); TH0 = np.deg2rad(48.0); PSI0 = np.deg2rad(44.0)
SEQ_T = 8.0                                 # loop period of the beat-3 sequence
WPHI = 0.40; WPSI = 0.55                    # steady rates used in beats 4-6
THA = 0.42; THW = 0.85                      # nutation amplitude and rate
OSC = 1.90                                  # screen length per unit of angular velocity

I1 = 1.00; I3 = 0.45                        # principal moments of the symmetrical top
TH9 = np.deg2rad(42.0)                      # fixed tilt during the beat-9 precession
W_PR = 0.46                                 # M / I1 on screen
W_SP = W_PR * (I1 / I3) * np.cos(TH9)       # (M / I3) cos(theta)

PX = 1.45                                   # left edge of the right-hand panel


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-9 else 1.0)


def _p(v):
 return ORG + PS * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


def _frame(phi, th, psi):
 """The line of nodes and the three body axes, in fixed coordinates."""
 cp, sp, ct, st, cs, ss = (np.cos(phi), np.sin(phi), np.cos(th),
                           np.sin(th), np.cos(psi), np.sin(psi))
 N = np.array([cp, sp, 0.0])
 x3 = np.array([sp * st, -cp * st, ct])
 x1 = np.array([cp * cs - sp * ss * ct, sp * cs + cp * ss * ct, ss * st])
 return N, x1, np.cross(x3, x1), x3


def _smooth(x):
 x = float(np.clip(x, 0.0, 1.0)); return x * x * (3.0 - 2.0 * x)


class EulerAnglesBase(LandauBatchBase):
 EPISODE = 35; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "兩個座標系，共同原點", "en": "two frames, one shared origin"},
               1: {"zh": "節線：兩個平面的交線", "en": "the line of nodes: where the planes meet"},
               2: {"zh": "三個歐拉角", "en": "the three Eulerian angles"},
               3: {"zh": "三次接續的轉動", "en": "three successive rotations"},
               4: {"zh": "角速度拆成三份，軸並不互相垂直",
                   "en": "three parts on three axes that are not perpendicular"},
               6: {"zh": "對稱陀螺的轉動動能", "en": "the rotational energy of a symmetrical top"},
               7: {"zh": "把 x₁ 取在節線上", "en": "putting x₁ on the line of nodes"},
               8: {"zh": "取 Z 沿著守恆的角動量", "en": "Z taken along the conserved M"},
               9: {"zh": "規則進動，與第 33 課一致", "en": "regular precession, as in lesson 33"}}

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

 def _dash(self, a, b, color, n=12, sw=2.5):
  """Fixed dash count: a stretching DashedLine changes its submobject count,
  which knocks out FadeIn's one-time family alignment for the whole group."""
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _ax(self, v, color, sw=4, k=1.0):
  return self._arr(_p(np.zeros(3)), _p(k * L * np.asarray(v)), color, sw=sw, tl=0.18)

 def _ring(self, e1, e2, r, color, sw=2.5, k=72):
  pts = [_p(r * (np.cos(a) * np.asarray(e1) + np.sin(a) * np.asarray(e2)))
         for a in np.linspace(0, 2 * PI, k)]
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(pts); return m

 def _arc(self, u, v, r, color, sw=3.5, k=26):
  pts = [_p(r * _unit((1 - s) * np.asarray(u) + s * np.asarray(v)))
         for s in np.linspace(0, 1, k)]
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(pts); return m

 def _amid(self, u, v, r):
  return _p(r * _unit(np.asarray(u) + np.asarray(v)))

 def _sq(self, u, v, s=0.18, color=GHOST):
  """A small right-angle marker in the plane of two perpendicular unit vectors."""
  o = np.zeros(3)
  return Polygon(_p(s * np.asarray(u)), _p(s * (np.asarray(u) + np.asarray(v))),
                 _p(s * np.asarray(v)), _p(o), color=color, stroke_width=2)

 def _seg(self, x0, y, a, b, color, h=0.22):
  """One segment of a stacked signed bar, running from a to a+b."""
  w = max(abs(b), 0.02)
  return Rectangle(width=w, height=h, color=color, fill_opacity=0.85,
                   stroke_width=0).move_to([x0 + a + b / 2, y, 0])

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  return self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)

 # ── the Euler angles, per stage ───────────────────────────────────
 def _tau(self):
  return self.t.get_value() - self.t0

 def _ang(self):
  m, tau = self.mode, self._tau()
  if m <= 2:                                # a slow drift, to read as 3D
   return PHI0 + 0.20 * np.sin(0.38 * tau), TH0 + 0.14 * np.sin(0.29 * tau), PSI0
  if m == 3:                                # phi, then theta, then psi
   u = (tau / SEQ_T) % 1.0
   return (PHI0 * _smooth((u - 0.02) / 0.26), TH0 * _smooth((u - 0.32) / 0.26),
           PSI0 * _smooth((u - 0.62) / 0.26))
  if m <= 6:                                # steady precession and spin, nutating
   return (PHI0 + WPHI * tau, TH0 + THA * np.sin(THW * tau), PSI0 + WPSI * tau)
  if m <= 8:                                # x1 on the line of nodes
   return PHI0 + WPHI * tau, TH0 + THA * np.sin(THW * tau), 0.0
  return PHI0 + W_PR * tau, TH9, W_SP * tau  # regular precession

 def _rates(self):
  m, tau = self.mode, self._tau()
  if m <= 6:
   return THA * THW * np.cos(THW * tau), WPHI, WPSI
  if m <= 8:
   return THA * THW * np.cos(THW * tau), WPHI, 0.0
  return 0.0, W_PR, W_SP

 def _om(self):
  """The angular velocity, as the sum of its three Eulerian pieces."""
  N, _, _, x3 = _frame(*self._ang())
  dth, dph, dps = self._rates()
  return dth * N + dph * np.array([0.0, 0.0, 1.0]) + dps * x3

 def _comp(self):
  """Each body-axis component of Omega, split into its theta and phi parts."""
  _, th, psi = self._ang(); dth, dph, dps = self._rates()
  return ((dph * np.sin(th) * np.sin(psi), dth * np.cos(psi)),
          (dph * np.sin(th) * np.cos(psi), -dth * np.sin(psi)),
          (dph * np.cos(th), dps))

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
  self.t = ValueTracker(0.0); self.t0 = 0.0; self.mode = 0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)
  O3 = _p(np.zeros(3)); ZV = np.array([0.0, 0.0, 1.0])

  # ══ the fixed frame ═══════════════════════════════════════════════
  fixed = VGroup(self._ax([1, 0, 0], DIM), self._ax([0, 1, 0], DIM), self._ax(ZV, DIM),
                 Text("X", font_size=FS_TAG, color=DIM)
                 .move_to(_p(LT * L * np.array([1.0, 0, 0])) + np.array([0.12, -0.10, 0])),
                 Text("Y", font_size=FS_TAG, color=DIM)
                 .move_to(_p(LT * L * np.array([0, 1.0, 0])) + np.array([-0.14, -0.10, 0])),
                 Text("Z", font_size=FS_TAG, color=DIM)
                 .move_to(_p(LT * L * ZV) + np.array([-0.02, 0.20, 0])),
                 Dot(O3, color=INK, radius=0.07))

  # ══ the body frame ════════════════════════════════════════════════
  def _bx(i, color=ACCENT_A, sw=5):
   return always_redraw(lambda: self._ax(_frame(*self._ang())[i], color, sw=sw))
  body = VGroup(_bx(1), _bx(2), _bx(3),
                self._tag("x₁", lambda: _p(LT * L * _frame(*self._ang())[1]),
                          off=np.array([0.14, -0.14, 0]), color=ACCENT_A, size=FS_SMALL),
                self._tag("x₂", lambda: _p(LT * L * _frame(*self._ang())[2]),
                          off=np.array([0.14, -0.14, 0]), color=ACCENT_A, size=FS_SMALL),
                self._tag("x₃", lambda: _p(LT * L * _frame(*self._ang())[3]),
                          off=np.array([0.18, 0.14, 0]), color=ACCENT_A, size=FS_SMALL))

  legend = VGroup(self._row(0.95, "固定座標系　X , Y , Z", "the fixed frame  X , Y , Z", DIM),
                  self._row(0.30, "隨物體轉　x₁ , x₂ , x₃", "the body frame  x₁ , x₂ , x₃",
                            ACCENT_A),
                  self._row(-0.45, "兩者共用一個原點", "both share a single origin", INK))

  # ══ beat 1: the two planes and the line of nodes ══════════════════
  planeXY = self._ring([1, 0, 0], [0, 1, 0], RP, GHOST, sw=2.5)
  plane12 = always_redraw(lambda: self._ring(_frame(*self._ang())[1], _frame(*self._ang())[2],
                                             1.20, ACCENT_A, sw=2))
  node = always_redraw(lambda: Line(_p(-1.15 * RP * _frame(*self._ang())[0]),
                                    _p(1.15 * RP * _frame(*self._ang())[0]),
                                    color=WARN, stroke_width=4))
  nodet = self._tag("ON", lambda: _p(1.30 * RP * _frame(*self._ang())[0]),
                    off=np.array([0.20, -0.14, 0]), color=WARN, size=FS_SMALL)
  perp1 = always_redraw(lambda: self._sq(_frame(*self._ang())[0], ZV))
  perp2 = always_redraw(lambda: self._sq(_frame(*self._ang())[0], _frame(*self._ang())[3]))
  cap1 = VGroup(self._row(0.80, "水平面 XY　與　物體平面 x₁x₂",
                          "the XY plane and the x₁x₂ plane", DIM),
                self._row(0.15, "交線就是節線 ON", "they meet along the line of nodes", WARN),
                self._row(-0.55, "ON 同時垂直於 Z 與 x₃",
                          "ON is perpendicular to Z and to x₃", INK))
  planes = VGroup(planeXY, plane12)
  nodeg = VGroup(node, nodet)

  # ══ beat 2: the three angles ══════════════════════════════════════
  arcT = always_redraw(lambda: self._arc(ZV, _frame(*self._ang())[3], 0.62, ACCENT_B))
  arcP = always_redraw(lambda: self._arc([1, 0, 0], _frame(*self._ang())[0], 0.92, ACCENT_C))
  arcS = always_redraw(lambda: self._arc(_frame(*self._ang())[0], _frame(*self._ang())[1],
                                         0.92, ACCENT_A))
  tagT = self._tag("θ", lambda: self._amid(ZV, _frame(*self._ang())[3], 0.62),
                   off=np.array([0.20, 0.10, 0]), color=ACCENT_B, size=FS_SMALL)
  tagP = self._tag("φ", lambda: self._amid([1, 0, 0], _frame(*self._ang())[0], 0.92),
                   off=np.array([0.06, -0.24, 0]), color=ACCENT_C, size=FS_SMALL)
  tagS = self._tag("ψ", lambda: self._amid(_frame(*self._ang())[0], _frame(*self._ang())[1],
                                           0.92), off=np.array([0.20, 0.14, 0]),
                   color=ACCENT_A, size=FS_SMALL)
  arcs = VGroup(arcT, arcP, arcS, tagT, tagP, tagS)
  cap2 = VGroup(self._row(0.85, "θ：Z 與 x₃ 的夾角", "θ: between Z and x₃", ACCENT_B),
                self._row(0.20, "φ：從 X 量到節線", "φ: from X to the line of nodes", ACCENT_C),
                self._row(-0.45, "ψ：從節線量到 x₁", "ψ: from the line of nodes to x₁",
                          ACCENT_A))

  # ══ beat 3: the defining sequence ═════════════════════════════════
  steps = VGroup(Text("① φ ⟳ Z", font_size=FS_BODY, color=ACCENT_C)
                 .move_to([PX + 0.30, 0.85, 0], aligned_edge=LEFT),
                 Text("② θ ⟳ ON", font_size=FS_BODY, color=ACCENT_B)
                 .move_to([PX + 0.30, 0.20, 0], aligned_edge=LEFT),
                 Text("③ ψ ⟳ x₃", font_size=FS_BODY, color=ACCENT_A)
                 .move_to([PX + 0.30, -0.45, 0], aligned_edge=LEFT))

  def _now():
   u = (self._tau() / SEQ_T) % 1.0
   return 0 if u < 0.32 else (1 if u < 0.62 else 2)
  mark = always_redraw(lambda: Dot([PX, 0.85 - 0.65 * _now(), 0], color=INK, radius=0.08))
  cap3 = self._row(-1.20, "回到重合的位置後重複", "then it repeats from the aligned start", DIM)

  # ══ beats 4-5: the angular velocity ═══════════════════════════════
  def _rate_arr(vec, rate, color):
   return always_redraw(lambda: self._arr(O3, _p(OSC * rate() * np.asarray(vec())), color,
                                          sw=5, tl=0.18))
  vth = _rate_arr(lambda: _frame(*self._ang())[0], lambda: self._rates()[0], WARN)
  vph = _rate_arr(lambda: ZV, lambda: self._rates()[1], ACCENT_B)
  vps = _rate_arr(lambda: _frame(*self._ang())[3], lambda: self._rates()[2], ACCENT_C)
  vom = always_redraw(lambda: self._arr(O3, _p(OSC * self._om()), INK, sw=7, tl=0.24))
  vomt = self._tag("Ω", lambda: _p(OSC * self._om()), off=np.array([0.24, 0.16, 0]), color=INK)
  rates = VGroup(vth, vph, vps, vom, vomt)
  cap4 = VGroup(self._row(0.95, "dθ/dt　沿節線 ON", "dθ/dt  along ON", WARN),
                self._row(0.30, "dφ/dt　沿固定的 Z", "dφ/dt  along the fixed Z", ACCENT_B),
                self._row(-0.35, "dψ/dt　沿物體的 x₃", "dψ/dt  along the body's x₃", ACCENT_C),
                self._row(-1.15, "三者相加就是 Ω", "their sum is Ω", INK))

  BX = 3.95; BSC = 1.55
  zero = Line([BX, 1.30, 0], [BX, -0.95, 0], color=GHOST, stroke_width=2)
  bars = VGroup(zero)
  for k, (y, name) in enumerate(((1.00, "Ω₁"), (0.25, "Ω₂"), (-0.50, "Ω₃"))):
   bars.add(Text(name, font_size=FS_SMALL, color=INK).move_to([BX - 0.02, y + 0.30, 0]))
   bars.add(always_redraw(lambda y=y, k=k: self._seg(BX, y, 0.0, BSC * self._comp()[k][0],
                                                     ACCENT_B)))
   bars.add(always_redraw(lambda y=y, k=k: self._seg(
    BX, y, BSC * self._comp()[k][0], BSC * self._comp()[k][1],
    ACCENT_C if k == 2 else WARN)))
  cap5 = VGroup(self._row(-1.25, "青：dφ/dt 的貢獻", "cyan: from dφ/dt", ACCENT_B, x=1.55),
                self._row(-1.25, "紅：dθ/dt", "red: dθ/dt", WARN, x=4.35))

  # ══ beats 6-9: the symmetrical top ════════════════════════════════
  rotor = VGroup(always_redraw(lambda: self._ring(_frame(*self._ang())[1],
                                                  _frame(*self._ang())[2], 0.78, ACCENT_A, sw=4)),
                 always_redraw(lambda: self._ring(_frame(*self._ang())[1],
                                                  _frame(*self._ang())[2], 0.46, ACCENT_A, sw=2)))
  EX6 = 3.85; ESC = 6.00
  ezero = Line([EX6 - 1.90, -0.30, 0], [EX6 - 1.90, 0.95, 0], color=GHOST, stroke_width=2)

  def _energy():
   _, th, _ = self._ang(); dth, dph, dps = self._rates()
   return (0.5 * I1 * (dth ** 2 + (dph * np.sin(th)) ** 2),
           0.5 * I3 * (dph * np.cos(th) + dps) ** 2)
  ebars = VGroup(ezero,
                 Text("½ I₁ [ ... ]", font_size=FS_SMALL, color=ACCENT_B)
                 .move_to([EX6 - 1.60, 1.10, 0], aligned_edge=LEFT),
                 always_redraw(lambda: self._seg(EX6 - 1.90, 0.75, 0.0, ESC * _energy()[0],
                                                 ACCENT_B, h=0.26)),
                 Text("½ I₃ [ ... ]", font_size=FS_SMALL, color=ACCENT_C)
                 .move_to([EX6 - 1.60, 0.32, 0], aligned_edge=LEFT),
                 always_redraw(lambda: self._seg(EX6 - 1.90, -0.05, 0.0, ESC * _energy()[1],
                                                 ACCENT_C, h=0.26)))
  cap6 = VGroup(self._row(-0.75, "I₁ = I₂ ≠ I₃", "I₁ = I₂ ≠ I₃", INK, FS_BODY, x=EX6 - 1.90),
                self._row(-1.30, "垂直於 x₃ 的兩根主軸可任選",
                          "the two axes across x₃ are free", DIM, x=EX6 - 1.90))

  cap7 = VGroup(self._row(0.85, "x₁ 取在節線上 ⟹ ψ = 0",
                          "put x₁ on ON, so ψ = 0", WARN, FS_BODY),
                self._row(0.10, "Ω₁ = dθ/dt", "Ω₁ = dθ/dt", WARN),
                self._row(-0.40, "Ω₂ = (dφ/dt) sinθ", "Ω₂ = (dφ/dt) sinθ", ACCENT_B),
                self._row(-0.90, "Ω₃ = (dφ/dt) cosθ + dψ/dt",
                          "Ω₃ = (dφ/dt) cosθ + dψ/dt", ACCENT_C))

  # beat 8: M along Z, and its components on the body axes
  MLEN = 1.42
  Marr = self._arr(O3, _p(MLEN * ZV), ACCENT_B, sw=7, tl=0.24)
  Mtag = Text("M", font_size=FS_TAG, color=ACCENT_B).move_to(
   _p(MLEN * ZV) + np.array([0.36, 0.02, 0]))
  M3 = always_redraw(lambda: self._arr(
   O3, _p(MLEN * np.cos(self._ang()[1]) * _frame(*self._ang())[3]), ACCENT_C, sw=5, tl=0.18))
  M2 = always_redraw(lambda: self._arr(
   O3, _p(MLEN * np.sin(self._ang()[1]) * _frame(*self._ang())[2]), WARN, sw=5, tl=0.18))
  Mdash = always_redraw(lambda: self._dash(
   _p(MLEN * np.cos(self._ang()[1]) * _frame(*self._ang())[3]), _p(MLEN * ZV), GHOST, n=10))
  mom = VGroup(Marr, Mtag, M3, M2, Mdash)
  # a flat right-triangle restatement of the same decomposition
  TA = np.array([2.05, -0.75, 0.0]); TH_ = np.deg2rad(48.0)
  TB = TA + np.array([0.0, 2.05, 0.0])
  TC = TA + 2.05 * np.array([np.sin(TH_), np.cos(TH_), 0.0])
  tri = VGroup(Line(TA, TB, color=ACCENT_C, stroke_width=4),
               Line(TA, TC, color=ACCENT_B, stroke_width=5),
               Line(TB, TC, color=WARN, stroke_width=4),
               Text("M", font_size=FS_SMALL, color=ACCENT_B)
               .move_to(0.5 * (TA + TC) + np.array([0.30, -0.10, 0])),
               Text("M cosθ", font_size=FS_SMALL, color=ACCENT_C)
               .move_to(0.5 * (TA + TB) + np.array([-0.52, 0.0, 0])),
               Text("M sinθ", font_size=FS_SMALL, color=WARN)
               .move_to(0.5 * (TB + TC) + np.array([0.42, 0.16, 0])),
               Text("θ", font_size=FS_SMALL, color=DIM).move_to(TA + np.array([0.16, 0.44, 0])))
  cap8 = VGroup(self._row(-1.20, "x₁ ⊥ M　⟹　M₁ = 0", "x₁ ⊥ M, so M₁ = 0", INK, FS_BODY,
                          x=1.90))

  # beat 9: the cone swept by the body axis
  cone = DashedVMobject(self._ring([1, 0, 0], [0, 1, 0], L * np.sin(TH9), GHOST, sw=3)
                        .shift(_p(L * np.cos(TH9) * ZV) - _p(np.zeros(3))),
                        num_dashes=44, color=GHOST)
  cap9 = VGroup(self._row(0.90, "dθ/dt = 0　⟹　θ 固定", "dθ/dt = 0, so θ is fixed", WARN,
                          FS_BODY),
                self._row(0.15, "dφ/dt = M / I₁", "dφ/dt = M / I₁", ACCENT_B, FS_BODY),
                self._row(-0.60, "Ω₃ = ( M / I₃ ) cosθ", "Ω₃ = ( M / I₃ ) cosθ", ACCENT_C,
                          FS_BODY),
                self._row(-1.30, "就是第 33 課的規則進動",
                          "the regular precession of lesson 33", DIM))

  # ── run the beats ─────────────────────────────────────────────────
  active_sub = None; active_f = None

  def run(i, mode, fin=(), fout=()):
   nonlocal active_sub, active_f
   self.mode = mode; self.t0 = self.t.get_value()
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
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  self.add(fixed)
  run(0, 0, fin=[body, legend])
  run(1, 1, fin=[planes, nodeg, perp1, perp2, cap1], fout=[legend])
  run(2, 2, fin=[arcs, cap2], fout=[cap1, perp1, perp2])
  run(3, 3, fin=[steps, mark, cap3], fout=[cap2])
  # The planes have done their job; from here they only crowd the vectors.
  run(4, 4, fin=[rates, cap4], fout=[steps, mark, cap3, arcs, planes])
  run(5, 5, fin=[bars, cap5], fout=[cap4])
  run(6, 6, fin=[rotor, ebars, cap6], fout=[bars, cap5, rates])
  run(7, 7, fin=[cap7], fout=[ebars, cap6])
  run(8, 8, fin=[mom, tri, cap8], fout=[cap7, nodeg])
  run(9, 9, fin=[cone, cap9], fout=[tri, cap8, M2, Mdash])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL35{'ZH' if lang == 'zh' else 'EN'}", (EulerAnglesBase,), {"LANGUAGE": lang})


LandauL35ZH = _mk("zh")
LandauL35EN = _mk("en")
