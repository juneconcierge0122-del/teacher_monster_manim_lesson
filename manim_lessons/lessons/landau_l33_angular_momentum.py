"""Lesson 33 — Angular momentum of a rigid body (Landau §33).

Stage A (beats 0-3) is the plane containing the symmetry axis of a prolate
top and the angular velocity: sweeping Omega around shows M following at a
different angle, because each component is stretched by its own principal
moment. Stage B (beats 4-7) switches to an axonometric projection: a spherical
top and a rotator for the simple free rotations, then the symmetrical top whose
axis sweeps a cone about the conserved M — regular precession — while the body
spins about that axis at the rate the two formulas of §33 prescribe.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arc, Arrow, Circle, DashedLine, DashedVMobject, Dot, Ellipse, FadeIn, FadeOut,
                   Line, Polygon, Rectangle, Text, VGroup, VMobject, ValueTracker, always_redraw,
                   linear, DOWN, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

I1 = 1.00                                  # transverse principal moment
I3 = 0.45                                  # moment about the symmetry axis (a prolate top)

# ── stage A: the plane of x3 and Omega ────────────────────────────────
AC = np.array([-3.60, -0.55, 0.0])         # centre of mass of the top
TH3 = np.deg2rad(68.0)                     # screen direction of the symmetry axis
E3 = np.array([np.cos(TH3), np.sin(TH3), 0.0])
E1 = np.array([np.sin(TH3), -np.cos(TH3), 0.0])
OMLEN = 2.05; MSC = 1.15
BETA0 = np.deg2rad(42.0); BETA1 = np.deg2rad(29.0); BETW = 0.46

# ── stage B: axonometric projection ───────────────────────────────────
EX = np.array([1.0, 0.0, 0.0]); EY = np.array([-0.52, -0.30, 0.0]); EZ = np.array([0.0, 1.0, 0.0])
ORG = np.array([0.00, -1.15, 0.0]); PS = 1.24
THETA = np.deg2rad(35.0)
L_AX = 1.75; L_M = 2.05; R_ROT = 0.68
W_PR = 0.50                                # precession rate on screen, M / I1
W_SP = W_PR * (I1 / I3) * np.cos(THETA)    # spin rate, (M / I3) cos(theta)
OS = 1.25                                  # screen length per unit of angular velocity
FS_TAG = 20


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-9 else 1.0)


def _proj(v):
 return ORG + PS * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class AngularMomentumBase(LandauBatchBase):
 EPISODE = 33; LANGUAGE = "zh"
 MODE_LABEL = {3: {"zh": "只有球陀螺才恆平行", "en": "parallel only for a spherical top"},
               4: {"zh": "自由轉動：角動量守恆", "en": "free rotation: M is conserved"},
               5: {"zh": "M、Ω 與對稱軸永遠共面", "en": "M, Ω and the symmetry axis stay coplanar"},
               6: {"zh": "規則進動：對稱軸繞 M 掃出圓錐",
                   "en": "regular precession: the axis sweeps a cone about M"},
               7: {"zh": "自轉與進動的角速度", "en": "the spin rate and the precession rate"}}

 # ── stage A geometry ──────────────────────────────────────────────
 def _beta(self):
  return BETA0 + BETA1 * np.sin(BETW * self.t.get_value())

 def _om(self):
  b = self._beta()
  return OMLEN * (np.cos(b) * E3 + np.sin(b) * E1)

 def _mom(self):
  b = self._beta()
  return MSC * OMLEN * (I3 * np.cos(b) * E3 + I1 * np.sin(b) * E1)

 # ── stage B geometry ──────────────────────────────────────────────
 def _n(self):
  p = self.ps.get_value()
  return np.array([np.sin(THETA) * np.cos(p), np.sin(THETA) * np.sin(p), np.cos(THETA)])

 def _uv(self):
  n = self._n(); u = _unit(np.cross(np.array([0.0, 0.0, 1.0]), n)); return u, np.cross(n, u)

 def _omega3(self):
  return W_PR * np.array([0.0, 0.0, 1.0]) + W_SP * self._n()

 def _ring(self, centre, radius, color, sw=3.5, k=64):
  u, v = self._uv()
  pts = [_proj(centre + radius * (np.cos(a) * u + np.sin(a) * v))
         for a in np.linspace(0, 2 * PI, k)]
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(pts); return m

 def _cone_rim(self):
  r = L_AX * np.sin(THETA); h = L_AX * np.cos(THETA)
  pts = [_proj(np.array([r * np.cos(a), r * np.sin(a), h])) for a in np.linspace(0, 2 * PI, 72)]
  m = VMobject(color=GHOST, stroke_width=3); m.set_points_as_corners(pts)
  return DashedVMobject(m, num_dashes=44, color=GHOST)

 def _theta_arc(self):
  n = self._n(); z = np.array([0.0, 0.0, 1.0])
  pts = [_proj(0.80 * _unit((1 - s) * z + s * n)) for s in np.linspace(0, 1, 24)]
  m = VMobject(color=DIM, stroke_width=2.5); m.set_points_as_corners(pts); return m

 # ── drawing helpers ───────────────────────────────────────────────
 def _arr(self, start, tip, color, sw=5, tl=0.20):
  return Arrow(start, tip, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.32, tip_length=tl)

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off))
  return m

 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _perp(self, p, z):
  """An out-of-page (dot) or into-page (cross) marker sized by |Omega x r|."""
  r = 0.11 + 0.26 * min(abs(z), 2.2) / 2.2
  g = VGroup(Circle(radius=r, color=WARN, stroke_width=3).move_to(p))
  if z >= 0:
   g.add(Dot(p, color=WARN, radius=0.05))
  else:
   d = r * 0.70
   g.add(Line(p + np.array([-d, -d, 0.0]), p + np.array([d, d, 0.0]), color=WARN, stroke_width=2.5),
         Line(p + np.array([-d, d, 0.0]), p + np.array([d, -d, 0.0]), color=WARN, stroke_width=2.5))
  return g

 def _hbar(self, x, y, length, color, h=0.24):
  return Rectangle(width=max(length, 0.02), height=h, color=color, fill_opacity=0.85,
                   stroke_width=0).move_to([x + max(length, 0.02) / 2, y, 0])

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
  self.ps = ValueTracker(0.62)              # precession phase
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ stage A ═══════════════════════════════════════════════════════
  body = Ellipse(width=2 * 0.78, height=2 * 1.60, color=ACCENT_A, stroke_width=3,
                 fill_opacity=0.10, fill_color=ACCENT_A).rotate(TH3 - PI / 2).move_to(AC)
  cm = Dot(AC, color=INK, radius=0.075)
  cm_tag = Text("O", font_size=FS_SMALL, color=DIM).move_to(AC + np.array([-0.26, -0.16, 0.0]))

  # particles with r and v = Omega x r
  part_b = [1.00 * E3 + 0.38 * E1, -0.80 * E3 + 0.46 * E1, 0.44 * E3 - 0.58 * E1]
  particles = VGroup()
  for b in part_b:
   p = AC + b
   particles.add(Line(AC, p, color=GHOST, stroke_width=2))
   particles.add(Dot(p, color=ACCENT_A, radius=0.07))
   particles.add(always_redraw(lambda b=b, p=p: self._perp(
    p, float(np.cross(self._om(), b)[2]))))
  ptag = Text("v = Ω × r", font_size=FS_SMALL, color=WARN).move_to(AC + np.array([1.95, -1.42, 0]))

  om_arr = always_redraw(lambda: self._arr(AC, AC + self._om(), ACCENT_C, sw=5))
  om_tag = self._tag("Ω", lambda: AC + self._om(), off=np.array([0.10, 0.30, 0.0]), color=ACCENT_C)
  m_arr = always_redraw(lambda: self._arr(AC, AC + self._mom(), ACCENT_B, sw=5))
  m_tag = self._tag("M", lambda: AC + self._mom(), off=np.array([0.32, 0.14, 0.0]), color=ACCENT_B)

  ax3 = Line(AC - 0.35 * E3, AC + 2.30 * E3, color=DIM, stroke_width=2)
  ax1 = Line(AC - 0.35 * E1, AC + 2.30 * E1, color=DIM, stroke_width=2)
  ax3t = Text("x₃", font_size=FS_SMALL, color=DIM).move_to(AC + 2.54 * E3)
  ax1t = Text("x₁", font_size=FS_SMALL, color=DIM).move_to(AC + 2.54 * E1)
  axes = VGroup(ax3, ax1, ax3t, ax1t)

  def _drop(vec, e):                        # dashed projection of `vec` onto axis `e`
   return always_redraw(lambda: DashedLine(AC + vec(), AC + float(np.dot(vec(), e)) * e,
                                           color=GHOST, stroke_width=2, dash_length=0.09))
  drops = VGroup(_drop(self._om, E3), _drop(self._om, E1),
                 _drop(self._mom, E3), _drop(self._mom, E1))

  gap = always_redraw(lambda: Arc(radius=1.15, arc_center=AC,
                                  start_angle=float(np.arctan2(*self._om()[1::-1])),
                                  angle=float(np.arctan2(*self._mom()[1::-1])
                                              - np.arctan2(*self._om()[1::-1])),
                                  color=WARN, stroke_width=3))

  # right panel: how each component is stretched
  BX = 2.10; BS = 1.05
  bars = VGroup(
   Text("Ω₃", font_size=FS_SMALL, color=ACCENT_C).move_to([BX - 0.38, 0.98, 0]),
   always_redraw(lambda: self._hbar(BX, 0.98, BS * float(np.dot(self._om(), E3)), ACCENT_C)),
   Text("M₃", font_size=FS_SMALL, color=ACCENT_B).move_to([BX - 0.38, 0.56, 0]),
   always_redraw(lambda: self._hbar(BX, 0.56, BS * float(np.dot(self._mom(), E3)) / MSC,
                                    ACCENT_B)),
   Text("Ω₁", font_size=FS_SMALL, color=ACCENT_C).move_to([BX - 0.38, -0.42, 0]),
   always_redraw(lambda: self._hbar(BX, -0.42, BS * float(np.dot(self._om(), E1)), ACCENT_C)),
   Text("M₁", font_size=FS_SMALL, color=ACCENT_B).move_to([BX - 0.38, -0.84, 0]),
   always_redraw(lambda: self._hbar(BX, -0.84, BS * float(np.dot(self._mom(), E1)) / MSC,
                                    ACCENT_B)),
   Text("× I₃ = 0.45", font_size=FS_SMALL, color=DIM).move_to([BX + 1.05, 0.20, 0]),
   Text("× I₁ = 1.00", font_size=FS_SMALL, color=DIM).move_to([BX + 1.05, -1.20, 0]),
   Line([BX - 0.08, 1.24, 0], [BX - 0.08, -1.10, 0], color=GHOST, stroke_width=2))

  # right panel for beat 3: the spherical top, where M and Omega coincide
  SC = np.array([3.30, -0.30, 0.0])
  sphere = VGroup(Circle(radius=0.95, color=ACCENT_A, stroke_width=3, fill_opacity=0.08,
                         fill_color=ACCENT_A).move_to(SC),
                  Ellipse(width=1.90, height=0.52, color=GHOST, stroke_width=2).move_to(SC),
                  Ellipse(width=0.52, height=1.90, color=GHOST, stroke_width=2).move_to(SC),
                  self._arr(SC, SC + np.array([0.0, 1.75, 0.0]), ACCENT_B, sw=7, tl=0.24),
                  self._arr(SC, SC + np.array([0.0, 1.05, 0.0]), ACCENT_C, sw=5, tl=0.18),
                  Text("M", font_size=FS_TAG, color=ACCENT_B).move_to(SC + np.array([0.34, 1.90, 0])),
                  Text("Ω", font_size=FS_TAG, color=ACCENT_C).move_to(SC + np.array([-0.36, 1.10, 0])),
                  self.lab("球陀螺：M 與 Ω 同方向", "spherical top: M is along Ω",
                           FS_SMALL, DIM).move_to(SC + np.array([0.0, -1.45, 0])))
  stage_a = VGroup(body, cm, cm_tag, axes, drops, om_arr, om_tag, m_arr, m_tag, gap, sphere)

  # ══ stage B ═══════════════════════════════════════════════════════
  # beat 4: the two simple free rotations
  BC1 = np.array([-3.60, -0.28, 0.0])
  ball = VGroup(Circle(radius=1.00, color=ACCENT_A, stroke_width=3, fill_opacity=0.08,
                       fill_color=ACCENT_A).move_to(BC1),
                Ellipse(width=2.00, height=0.56, color=GHOST, stroke_width=2).move_to(BC1),
                Ellipse(width=2.00, height=0.56, color=GHOST, stroke_width=2)
                .move_to(BC1 + np.array([0.0, 0.44, 0.0])),
                self._arr(BC1, BC1 + np.array([0.0, 1.85, 0.0]), ACCENT_B, sw=7, tl=0.24),
                self._arr(BC1, BC1 + np.array([0.0, 1.12, 0.0]), ACCENT_C, sw=5, tl=0.18),
                Text("M", font_size=FS_TAG, color=ACCENT_B).move_to(BC1 + np.array([0.34, 2.00, 0])),
                Text("Ω", font_size=FS_TAG, color=ACCENT_C).move_to(BC1 + np.array([-0.36, 1.18, 0])),
                always_redraw(lambda: Dot(BC1 + np.array([0.95 * np.cos(0.9 * self.t.get_value()),
                                                          0.26 * np.sin(0.9 * self.t.get_value()),
                                                          0.0]), color=WARN, radius=0.08)),
                self.lab("球陀螺：繞空間中固定的軸等速轉動",
                         "spherical top: fixed axis", FS_BODY, INK)
                .move_to(BC1 + np.array([0.0, -1.50, 0])))

  BC2 = np.array([3.30, -0.28, 0.0])
  def _rod():
   a = 0.75 * self.t.get_value(); d = np.array([np.cos(a), np.sin(a), 0.0]) * 1.05
   return VGroup(Line(BC2 - d, BC2 + d, color=ACCENT_A, stroke_width=4),
                 Dot(BC2 + d, color=ACCENT_A, radius=0.13),
                 Dot(BC2 - d, color=ACCENT_A, radius=0.13))
  rotator = VGroup(always_redraw(_rod),
                   Circle(radius=0.16, color=ACCENT_B, stroke_width=3.5).move_to(BC2),
                   Dot(BC2, color=ACCENT_B, radius=0.05),
                   Text("M , Ω", font_size=FS_TAG, color=ACCENT_B)
                   .move_to(BC2 + np.array([0.72, 0.34, 0])),
                   self.lab("轉子：在一個平面內等速旋轉",
                            "rotator: rotation in one plane", FS_BODY, INK)
                   .move_to(BC2 + np.array([0.0, -1.50, 0])))
  simple = VGroup(ball, rotator)

  # beats 5-7: the symmetrical top precessing about M
  O3 = _proj(np.zeros(3))
  Marr = self._arr(O3, _proj(np.array([0.0, 0.0, L_M])), ACCENT_B, sw=6, tl=0.22)
  Mtag = Text("M", font_size=FS_TAG, color=ACCENT_B).move_to(
   _proj(np.array([0.0, 0.0, L_M])) + np.array([0.30, 0.18, 0.0]))
  shaft = always_redraw(lambda: Line(_proj(-0.75 * self._n()), _proj(L_AX * self._n()),
                                     color=ACCENT_A, stroke_width=5))
  rotor = always_redraw(lambda: self._ring(np.zeros(3), R_ROT, ACCENT_A, sw=3.5))
  rotor2 = always_redraw(lambda: self._ring(0.45 * self._n(), 0.62 * R_ROT, ACCENT_A, sw=2.5))
  spin = always_redraw(lambda: Dot(_proj(R_ROT * (
   np.cos((W_SP / W_PR) * self.ps.get_value()) * self._uv()[0]
   + np.sin((W_SP / W_PR) * self.ps.get_value()) * self._uv()[1])), color=WARN, radius=0.085))
  n_tag = self._tag("x₃", lambda: _proj(L_AX * self._n()), off=np.array([0.24, 0.24, 0.0]),
                    color=ACCENT_A, size=FS_SMALL)
  plane = always_redraw(lambda: Polygon(O3, _proj(L_AX * self._n()),
                                        _proj(np.array([0.0, 0.0, L_M])), color=GHOST,
                                        stroke_width=1.5, fill_opacity=0.10, fill_color=INK))
  oarr = always_redraw(lambda: self._arr(O3, _proj(OS * self._omega3()), ACCENT_C, sw=5))
  otag = self._tag("Ω", lambda: _proj(OS * self._omega3()), off=np.array([-0.30, 0.20, 0.0]),
                   color=ACCENT_C)
  thar = always_redraw(self._theta_arc)
  thtag = self._tag("θ", lambda: _proj(0.80 * _unit(np.array([0.0, 0.0, 1.0]) + self._n())),
                    off=np.array([0.10, 0.22, 0.0]), color=DIM, size=FS_SMALL)
  x2 = always_redraw(lambda: self._arr(
   O3, _proj(1.05 * _unit(np.cross(self._n(), np.array([0.0, 0.0, 1.0])))), DIM, sw=3, tl=0.14))
  x2t = self._tag("x₂", lambda: _proj(1.25 * _unit(np.cross(self._n(),
                                                            np.array([0.0, 0.0, 1.0])))),
                  off=np.array([0.16, 0.18, 0.0]), color=DIM, size=FS_SMALL)
  cone = always_redraw(self._cone_rim)

  # beat 7: Omega = Omega_pr (along M) + Omega_3 (along the axis)
  legA = always_redraw(lambda: DashedLine(O3, _proj(OS * W_PR * np.array([0.0, 0.0, 1.0])),
                                          color=ACCENT_C, stroke_width=3, dash_length=0.10))
  legB = always_redraw(lambda: DashedLine(_proj(OS * W_PR * np.array([0.0, 0.0, 1.0])),
                                          _proj(OS * self._omega3()), color=ACCENT_C,
                                          stroke_width=3, dash_length=0.10))
  legAt = self._tag("Ωₚᵣ", lambda: _proj(OS * W_PR * np.array([0.0, 0.0, 1.0])),
                    off=np.array([-0.58, -0.04, 0.0]), color=ACCENT_C, size=FS_SMALL)
  legBt = self._tag("Ω₃", lambda: 0.5 * (_proj(OS * W_PR * np.array([0.0, 0.0, 1.0]))
                                         + _proj(OS * self._omega3())),
                    off=np.array([0.10, 0.26, 0.0]), color=ACCENT_C, size=FS_SMALL)
  decomp = VGroup(legA, legB, legAt, legBt)
  top = VGroup(plane, cone, Marr, Mtag, shaft, rotor, rotor2, spin, n_tag,
               oarr, otag, thar, thtag)

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

  self.add(body, cm, cm_tag)
  run(0, fin=[particles, ptag, om_arr, om_tag])              # M = sum m r x v
  run(1, fin=[m_arr, m_tag], fout=[particles, ptag])         # M_i = I_ik Omega_k
  run(2, fin=[axes, drops, bars])                            # principal axes
  run(3, fin=[gap, sphere], fout=[bars])                     # M is not parallel to Omega
  run(4, fin=[simple], fout=[stage_a])                       # free rotation: M conserved
  run(5, fin=[plane, Marr, Mtag, shaft, rotor, rotor2, spin, n_tag, oarr, otag,
              thar, thtag, x2, x2t], fout=[simple])          # M, Omega, x3 coplanar
  run(6, fin=[cone], fout=[x2, x2t],
      extra=[self.ps.animate(rate_func=linear).increment_value(W_PR * (self.dur(6) - 0.5))])
  run(7, fin=[decomp],
      extra=[self.ps.animate(rate_func=linear).increment_value(W_PR * (self.dur(7) - 0.5))])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL33{'ZH' if lang == 'zh' else 'EN'}", (AngularMomentumBase,),
             {"LANGUAGE": lang})

LandauL33ZH = _mk("zh")
LandauL33EN = _mk("en")
