"""Lesson 32 — The inertia tensor (Landau §32).

A five-particle planar body drifts and spins on the left of the stage while a
live 3x3 matrix panel on the right shows its inertia tensor: each cell holds a
square whose area is proportional to |I_ik|, so the products of inertia visibly
grow and shrink as the body-fixed axes are turned, and collapse to nothing at
the principal axes. Beats 0-1 split the kinetic energy into translation plus
rotation (with live energy bars), 2-5 build the tensor and diagonalise it,
6 classifies the tops, 7 shows the coplanar and collinear special cases, and 8
shifts the origin away from the centre of mass.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (Arc, Arrow, Circle, DashedLine, Dot, FadeIn, FadeOut, Line, Polygon,
                   Rectangle, RegularPolygon, Square, Text, VGroup, ValueTracker,
                   always_redraw, linear, smooth, DOWN, LEFT, RIGHT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

# ── the body: five point masses in a plane, centre of mass at the origin ──
MASS = np.array([1.0, 1.4, 0.8, 1.2, 1.0])
_RAW = np.array([[-1.5, 0.7], [1.3, 0.9], [1.6, -0.6], [-0.4, -1.1], [-1.1, -0.2]])
BODY = _RAW - (MASS[:, None] * _RAW).sum(0) / MASS.sum()
HULL = [1, 0, 4, 3, 2]                     # convex order of the five particles
MU = float(MASS.sum())

BS = 0.78                                  # screen units per body unit
BC = np.array([-3.55, -0.30, 0.0])         # home of the body on the stage
MC = np.array([3.30, -0.30, 0.0])          # centre of the matrix panel
CW = 0.94                                  # matrix cell pitch
ALPHA_STAR = 0.11953                       # axis angle that diagonalises I
I_PRIN = (3.335, 8.134, 11.469)            # the principal moments of this body
I_MAX = I_PRIN[2]
FS_TAG = 20


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-6 else 1.0)


def _inertia(al):
 """The 2x2 in-plane block of I for body axes turned through `al`."""
 c, s = np.cos(al), np.sin(al)
 x = BODY[:, 0] * c + BODY[:, 1] * s
 y = -BODY[:, 0] * s + BODY[:, 1] * c
 return (float((MASS * y * y).sum()), float((MASS * x * x).sum()),
         float(-(MASS * x * y).sum()))


class InertiaTensorBase(LandauBatchBase):
 EPISODE = 32; LANGUAGE = "zh"
 MODE_LABEL = {2: {"zh": "慣性張量", "en": "the inertia tensor"},
               4: {"zh": "座標軸一轉，九個分量就跟著變",
                   "en": "turn the axes and all nine components change"},
               5: {"zh": "慣性主軸與主慣量", "en": "principal axes and principal moments"},
               6: {"zh": "非對稱陀螺 ／ 對稱陀螺 ／ 球陀螺",
                   "en": "asymmetrical / symmetrical / spherical top"},
               7: {"zh": "共面系統 ／ 共線系統（轉子）",
                   "en": "coplanar system / collinear system (rotator)"},
               8: {"zh": "換一個原點來算", "en": "computing about another origin"}}
 SPIN = 0.42                               # angular velocity of the body
 DA = 0.90; DW = 0.55                      # drift amplitude and rate of the centre of mass
 AS = 1.55                                 # velocity arrow scale
 AXL = 1.62                                # length of the drawn body axes

 # ── kinematics of the drifting, spinning body ─────────────────────
 def _drift(self):
  return np.array([self.DA * np.sin(self.DW * self.t.get_value()) * self.dv.get_value(), 0.0, 0.0])

 def _C(self):
  return BC + self._drift()

 def _V(self):
  return np.array([self.DA * self.DW * np.cos(self.DW * self.t.get_value())
                   * self.dv.get_value(), 0.0, 0.0])

 def _r(self, j):
  th = self.SPIN * self.t.get_value(); c, s = np.cos(th), np.sin(th); b = BODY[j] * BS
  return np.array([c * b[0] - s * b[1], s * b[0] + c * b[1], 0.0])

 def _p(self, j):
  return self._C() + self._r(j)

 def _w(self, j):                          # the rotational part Omega x r
  r = self._r(j)
  return self.SPIN * np.array([-r[1], r[0], 0.0])

 def _e(self, k):                          # unit vector of body axis k (0 or 1)
  a = self.SPIN * self.t.get_value() + self.al.get_value() + k * PI / 2
  return np.array([np.cos(a), np.sin(a), 0.0])

 # ── small drawing helpers ─────────────────────────────────────────
 def _tip(self, start, vec, scale=None, minlen=0.20):
  d = np.asarray(vec, dtype=float) * (self.AS if scale is None else scale)
  n = float(np.linalg.norm(d))
  if n < minlen: d = d / max(n, 1e-6) * minlen
  return np.asarray(start, dtype=float) + d

 def _arr(self, start, vec, color, sw=4, scale=None, minlen=0.20):
  return Arrow(start, self._tip(start, vec, scale, minlen), buff=0, color=color,
               stroke_width=sw, max_tip_length_to_length_ratio=0.34, tip_length=0.18)

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off))
  return m

 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def bars(self, vals, colors, base, scale=0.13, w=0.26, gap=0.42, names=("I₁", "I₂", "I₃")):
  """Three vertical bars growing upward from `base`, with labels underneath."""
  g = VGroup()
  for k, (v, c) in enumerate(zip(vals, colors)):
   x = base[0] + k * (w + gap)
   h = max(v * scale, 0.012)
   g.add(Rectangle(width=w, height=h, color=c, fill_opacity=0.85, stroke_width=0)
         .move_to([x, base[1] + h / 2, 0.0]))
   g.add(Text(names[k], font_size=FS_SMALL, color=DIM).move_to([x, base[1] - 0.26, 0.0]))
  g.add(Line([base[0] - 0.28, base[1], 0], [base[0] + 2 * (w + gap) + 0.28, base[1], 0],
             color=GHOST, stroke_width=2))
  return g

 # ── the matrix panel ──────────────────────────────────────────────
 def _cell(self, r, c):
  return MC + np.array([(c - 1) * CW, (1 - r) * CW, 0.0])

 def _block(self, r, c):
  """A square whose area tracks |I_rc| for the in-plane 2x2 block."""
  def make():
   I11, I22, I12 = _inertia(self.al.get_value())
   v = (I11, I12, I12, I22)[2 * r + c]
   side = 0.70 * float(np.sqrt(abs(v) / I_MAX))
   col = ACCENT_A if r == c else (WARN if v < 0 else ACCENT_B)
   return Square(side_length=max(side, 0.008), color=col, fill_opacity=0.9,
                 stroke_width=0).move_to(self._cell(r, c))
  return always_redraw(make)

 def matrix_panel(self):
  g = VGroup()
  for r in range(3):
   for c in range(3):
    g.add(Square(side_length=0.78, color=GHOST, stroke_width=1.6).move_to(self._cell(r, c)))
  for r, c in ((0, 2), (1, 2), (2, 0), (2, 1)):
   g.add(Text("0", font_size=FS_SMALL, color=GHOST).move_to(self._cell(r, c)))
  s3 = 0.70 * float(np.sqrt(I_PRIN[2] / I_MAX))
  g.add(Square(side_length=s3, color=ACCENT_A, fill_opacity=0.9,
               stroke_width=0).move_to(self._cell(2, 2)))
  for k in range(3):
   g.add(Text("123"[k], font_size=FS_SMALL, color=DIM)
         .move_to(self._cell(0, k) + UP * 0.72))
   g.add(Text("123"[k], font_size=FS_SMALL, color=DIM)
         .move_to(self._cell(k, 0) + LEFT * 1.12))
  h = 1.5 * CW
  for sgn in (-1, 1):
   x = MC[0] + sgn * 1.62
   g.add(Line([x, MC[1] - h, 0], [x, MC[1] + h, 0], color=DIM, stroke_width=2.5))
   for e in (-1, 1):
    g.add(Line([x, MC[1] + e * h, 0], [x - sgn * 0.18, MC[1] + e * h, 0],
               color=DIM, stroke_width=2.5))
  return g

 # ── beat plumbing ─────────────────────────────────────────────────
 def beat(self, i, fin=(), fout=(), extra=()):
  # NOTE: rate_func is set per animation, never as a play() keyword — a play-level
  # rate_func overrides the ones the `extra` trackers carry.
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
  return m.move_to(UP * 2.35)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.t = ValueTracker(0.0)
  self.al = ValueTracker(0.0)               # angle of the body axes within the body
  self.dv = ValueTracker(1.0)               # how much the centre of mass still drifts
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ── the body ──────────────────────────────────────────────────────
  plate = always_redraw(lambda: Polygon(*[self._p(j) for j in HULL], color=ACCENT_A,
                                        stroke_width=2.5, fill_opacity=0.09, fill_color=ACCENT_A))
  dots = VGroup(*[always_redraw(lambda j=j: Dot(self._p(j), color=ACCENT_A,
                                                radius=0.055 + 0.035 * MASS[j]))
                  for j in range(5)])
  cm = always_redraw(lambda: Dot(self._C(), color=ACCENT_B, radius=0.085))
  cm_tag = self._tag("O", self._C, off=np.array([-0.28, -0.10, 0.0]), color=ACCENT_B)
  arc = always_redraw(lambda: Arc(radius=1.55, start_angle=0.34 * PI, angle=1.12 * PI,
                                  color=ACCENT_C, stroke_width=3.5,
                                  arc_center=self._C()).add_tip(tip_length=0.20))
  om_tag = self._tag("Ω", self._C, off=UP * 1.80, color=ACCENT_C)

  # ── beat 0: the total velocity of every particle ──────────────────
  vtot = VGroup(*[always_redraw(lambda j=j: self._arr(self._p(j), self._V() + self._w(j),
                                                      WARN, sw=4.5)) for j in range(5)])
  vtag = self._tag("v", lambda: self._tip(self._p(1), self._V() + self._w(1)),
                   off=np.array([0.0, 0.30, 0.0]), color=WARN)

  # ── beat 1: the same velocities split into V and Omega x r ────────
  split = VGroup()
  for j in range(5):
   split.add(always_redraw(lambda j=j: self._arr(self._p(j), self._V(), ACCENT_B, sw=3.5)))
   split.add(always_redraw(lambda j=j: self._arr(self._tip(self._p(j), self._V()),
                                                 self._w(j), ACCENT_C, sw=3.5)))
  # both tags are pushed radially outward so they never sit on top of the centre of mass
  Vtag = self._tag("V", lambda: self._tip(self._p(1), self._V())
                   + 0.34 * _unit(self._r(1)), off=UP * 0.10, color=ACCENT_B)
  wtag = self._tag("Ω × r", lambda: self._tip(self._tip(self._p(2), self._V()), self._w(2))
                   + 0.52 * _unit(self._r(2)), off=UP * 0.10, color=ACCENT_C)

  # energy bars: translation pulses with V, rotation stays constant
  ES = 3.0; EX = 1.55
  Trot = 0.5 * self.SPIN ** 2 * I_PRIN[2] * BS ** 2
  ebars = VGroup(
   self.lab("平移動能  ½ μ V²", "translational  ½ μ V²").move_to([EX + 1.0, 0.66, 0]),
   always_redraw(lambda: Rectangle(width=max(ES * 0.5 * MU * float(np.dot(self._V(), self._V())),
                                             0.02), height=0.30, color=ACCENT_B,
                                   fill_opacity=0.85, stroke_width=0)
                 .move_to([EX + max(ES * 0.5 * MU * float(np.dot(self._V(), self._V())), 0.02) / 2,
                           0.24, 0])),
   self.lab("轉動動能  Tᵣₒₜ", "rotational  Tᵣₒₜ").move_to([EX + 1.0, -0.60, 0]),
   Rectangle(width=ES * Trot, height=0.30, color=ACCENT_C, fill_opacity=0.85,
             stroke_width=0).move_to([EX + ES * Trot / 2, -1.02, 0]),
   Line([EX, 0.55, 0], [EX, -1.25, 0], color=GHOST, stroke_width=2))

  # ── beats 2-5: the body axes and the matrix ───────────────────────
  ax1 = always_redraw(lambda: Arrow(self._C(), self._C() + self.AXL * self._e(0), buff=0,
                                    color=ACCENT_B, stroke_width=3, tip_length=0.16))
  ax2 = always_redraw(lambda: Arrow(self._C(), self._C() + self.AXL * self._e(1), buff=0,
                                    color=ACCENT_B, stroke_width=3, tip_length=0.16))
  ax1t = self._tag("x₁", lambda: self._C() + (self.AXL + 0.26) * self._e(0), off=0 * UP,
                   color=ACCENT_B, size=FS_SMALL)
  ax2t = self._tag("x₂", lambda: self._C() + (self.AXL + 0.26) * self._e(1), off=0 * UP,
                   color=ACCENT_B, size=FS_SMALL)
  ax3 = always_redraw(lambda: VGroup(Circle(radius=0.13, color=ACCENT_B, stroke_width=3)
                                     .move_to(self._C()),
                                     Dot(self._C(), color=ACCENT_B, radius=0.04)))
  axes = VGroup(ax1, ax2, ax1t, ax2t, ax3)
  mat = self.matrix_panel()
  blocks = VGroup(*[self._block(r, c) for r in range(2) for c in range(2)])

  # ── beat 3: the perpendicular distance that builds I₁₁ ────────────
  def foot():
   e = self._e(0)
   return self._C() + float(np.dot(self._p(1) - self._C(), e)) * e
  perp = always_redraw(lambda: DashedLine(self._p(1), foot(), color=WARN, stroke_width=3,
                                          dash_length=0.10))
  perp_tag = self._tag("x₂", lambda: 0.5 * (self._p(1) + foot()), off=np.array([0.30, 0.0, 0.0]),
                       color=WARN, size=FS_SMALL)
  hot = always_redraw(lambda: Dot(self._p(1), color=WARN, radius=0.10))
  cell11 = Square(side_length=0.78, color=WARN, stroke_width=3).move_to(self._cell(0, 0))
  diag3 = VGroup(perp, perp_tag, hot, cell11)

  # ── beat 4: the products of inertia are the ones that move ────────
  offhi = VGroup(*[Square(side_length=0.78, color=WARN, stroke_width=2.5)
                   .move_to(self._cell(r, c)) for r, c in ((0, 1), (1, 0))])

  # ── beat 5: the principal moments ─────────────────────────────────
  prin = VGroup(*[Text(f"I{'₁₂₃'[k]} = {I_PRIN[k]:.1f}", font_size=FS_SMALL, color=ACCENT_A)
                  .move_to([MC[0] + 2.45, self._cell(k, k)[1], 0.0]) for k in range(3)])

  stage_a = VGroup(plate, dots, cm, cm_tag, arc, om_tag, axes, mat, blocks, prin)

  # ── beat 6: the three kinds of top ────────────────────────────────
  def top_panel(cx, icon, vals, name_zh, name_en):
   g = VGroup(icon.move_to([cx - 1.10, -0.18, 0.0]))
   g.add(self.bars(vals, (ACCENT_A, ACCENT_B, ACCENT_C), [cx + 0.30, -1.35, 0.0],
                   scale=0.115))
   g.add(self.lab(name_zh, name_en, FS_BODY, INK).move_to([cx, 0.92, 0.0]))
   return g

  ico_a = Polygon(*[np.array([BODY[j][0], BODY[j][1], 0.0]) * 0.44 for j in HULL],
                  color=ACCENT_A, stroke_width=2.5, fill_opacity=0.10, fill_color=ACCENT_A)
  ico_b = VGroup(RegularPolygon(n=6, radius=0.62, color=ACCENT_A, stroke_width=2.5,
                                fill_opacity=0.10, fill_color=ACCENT_A),
                 DashedLine([0, -0.85, 0], [0, 0.85, 0], color=ACCENT_C, stroke_width=2.5,
                            dash_length=0.10))
  ico_c = VGroup(Circle(radius=0.60, color=ACCENT_A, stroke_width=2.5, fill_opacity=0.10,
                        fill_color=ACCENT_A),
                 Line([-0.72, 0, 0], [0.72, 0, 0], color=ACCENT_C, stroke_width=2),
                 Line([0, -0.72, 0], [0, 0.72, 0], color=ACCENT_C, stroke_width=2),
                 Line([-0.50, -0.50, 0], [0.50, 0.50, 0], color=ACCENT_C, stroke_width=2))
  tops = VGroup(top_panel(-4.60, ico_a, I_PRIN, "非對稱陀螺", "asymmetrical top"),
                top_panel(0.00, ico_b, (5.0, 5.0, 10.0), "對稱陀螺", "symmetrical top"),
                top_panel(4.60, ico_c, (8.0, 8.0, 8.0), "球陀螺", "spherical top"))

  # ── beat 7: coplanar and collinear systems ────────────────────────
  flat = VGroup(Polygon([-1.30, -0.22, 0], [0.55, -0.62, 0], [1.30, 0.22, 0], [-0.55, 0.62, 0],
                        color=GHOST, stroke_width=2, fill_opacity=0.08, fill_color=INK),
                *[Dot([BODY[j][0] * 0.52, BODY[j][1] * 0.34, 0.0], color=ACCENT_A, radius=0.075)
                  for j in range(5)],
                Arrow([0, 0, 0], [0, 1.15, 0], buff=0, color=ACCENT_C, stroke_width=3,
                      tip_length=0.16),
                Text("x₃", font_size=FS_SMALL, color=ACCENT_C).move_to([0.30, 1.22, 0]))
  flat.scale(0.74).move_to([-4.85, -0.18, 0.0])
  flat_bars = self.bars(I_PRIN, (ACCENT_A, ACCENT_B, ACCENT_C), [-2.75, -1.35, 0.0], scale=0.115)
  brace = VGroup(Text("+", font_size=FS_BODY, color=INK).move_to([-2.41, -0.86, 0]),
                 Text("=", font_size=FS_BODY, color=INK).move_to([-1.73, -0.86, 0]))
  coplanar = VGroup(flat, flat_bars, brace,
                    self.lab("共面", "coplanar", FS_BODY, INK).move_to([-3.55, 1.05, 0]))

  line_pts = [-1.35, -0.55, 0.35, 1.25]
  rod = VGroup(Line([-1.55, 0, 0], [1.55, 0, 0], color=ACCENT_C, stroke_width=3),
               *[Dot([x, 0, 0], color=ACCENT_A, radius=0.085) for x in line_pts],
               Text("x₃", font_size=FS_SMALL, color=ACCENT_C).move_to([1.78, 0.24, 0]),
               Arrow([0, 0, 0], [0, 1.05, 0], buff=0, color=ACCENT_B, stroke_width=3,
                     tip_length=0.16),
               Text("x₂", font_size=FS_SMALL, color=ACCENT_B).move_to([0.30, 1.12, 0]))
  rod.scale(0.74).move_to([2.35, -0.18, 0.0])
  rod_bars = self.bars((9.0, 9.0, 0.0), (ACCENT_A, ACCENT_B, ACCENT_C), [4.55, -1.35, 0.0],
                       scale=0.115)
  collinear = VGroup(rod, rod_bars,
                     self.lab("共線（轉子）", "collinear (rotator)", FS_BODY, INK)
                     .move_to([3.55, 1.05, 0]))
  special = VGroup(coplanar, collinear,
                   Line([0.0, 1.35, 0], [0.0, -1.72, 0], color=GHOST, stroke_width=2))

  # ── beat 8: moving the origin away from the centre of mass ────────
  a_b = np.array([1.05, 0.62])              # the displacement, fixed in the body
  def a_vec():
   th = self.SPIN * self.t.get_value(); c, s = np.cos(th), np.sin(th)
   return np.array([c * a_b[0] - s * a_b[1], s * a_b[0] + c * a_b[1], 0.0]) * BS
  Oprime = always_redraw(lambda: Dot(self._C() + a_vec(), color=WARN, radius=0.09))
  avec = always_redraw(lambda: Arrow(self._C(), self._C() + a_vec(), buff=0, color=WARN,
                                     stroke_width=3.5, tip_length=0.18))
  atag = self._tag("a", lambda: self._C() + 0.55 * a_vec(), off=np.array([0.10, 0.28, 0.0]),
                   color=WARN)
  Optag = self._tag("O′", lambda: self._C() + 1.16 * a_vec(), off=np.array([0.14, 0.20, 0.0]), color=WARN)
  a2 = float(np.dot(a_b, a_b))              # in body units, matching I_PRIN
  SB = 0.235; BX = 1.30
  shift = VGroup(
   avec, atag, Oprime, Optag,
   Text("I₃", font_size=FS_SMALL, color=ACCENT_A).move_to([BX - 0.40, 0.30, 0]),
   Rectangle(width=SB * I_PRIN[2], height=0.34, color=ACCENT_A, fill_opacity=0.85,
             stroke_width=0).move_to([BX + SB * I_PRIN[2] / 2, 0.30, 0]),
   Text("I′₃", font_size=FS_SMALL, color=WARN).move_to([BX - 0.40, -0.60, 0]),
   Rectangle(width=SB * I_PRIN[2], height=0.34, color=ACCENT_A, fill_opacity=0.85,
             stroke_width=0).move_to([BX + SB * I_PRIN[2] / 2, -0.60, 0]),
   Rectangle(width=SB * MU * a2, height=0.34, color=WARN, fill_opacity=0.85,
             stroke_width=0).move_to([BX + SB * (I_PRIN[2] + MU * a2 / 2), -0.60, 0]),
   Text("μ a²", font_size=FS_SMALL, color=WARN)
   .move_to([BX + SB * (I_PRIN[2] + MU * a2 / 2), -1.06, 0]),
   Line([BX, 0.62, 0], [BX, -0.92, 0], color=GHOST, stroke_width=2))

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

  self.add(plate, dots, cm, cm_tag)
  run(0, fin=[vtot, vtag, arc, om_tag])
  run(1, fin=[split, Vtag, wtag, ebars], fout=[vtot, vtag])
  run(2, fin=[axes, mat, blocks], fout=[split, Vtag, wtag, ebars],
      extra=[self.dv.animate(rate_func=lambda x: smooth(min(1.0, x / 0.35))).set_value(0.0)])
  run(3, fin=[diag3])
  run(4, fin=[offhi], fout=[diag3],
      extra=[self.al.animate(rate_func=linear).set_value(2.55)])
  run(5, fin=[prin], fout=[offhi],
      extra=[self.al.animate(rate_func=lambda x: smooth(min(1.0, x / 0.45)))
             .set_value(PI + ALPHA_STAR)])
  run(6, fin=[tops], fout=[stage_a])
  run(7, fin=[special], fout=[tops])
  run(8, fin=[plate, dots, cm, cm_tag, shift], fout=[special])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL32{'ZH' if lang == 'zh' else 'EN'}", (InertiaTensorBase,), {"LANGUAGE": lang})

LandauL32ZH = _mk("zh")
LandauL32EN = _mk("en")
