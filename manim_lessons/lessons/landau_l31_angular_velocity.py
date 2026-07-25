"""Lesson 31 — Angular velocity (Landau §31).

Beats 0-5 follow a rigid plate that drifts and spins in the plane: the
rigid-distance condition, the fixed and body-fixed frames, the split of a
displacement into translation plus rotation, the vector triangle
v = V + Omega x r at a point P, the growth of the rotational part with
distance from the axis, and the origin-independence of Omega. Beat 6 switches
to a rolling wheel whose contact point is instantaneously at rest — the
instantaneous axis of rotation.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arc, Arrow, Circle, DashedLine, Dot, FadeIn, FadeOut, Line, Polygon,
                   Text, VGroup, ValueTracker, always_redraw, linear, DOWN, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

SC = 1.117
BODY = [SC * np.array([-0.91, -0.59, 0.0]), SC * np.array([1.00, -0.56, 0.0]),
        SC * np.array([0.59, 0.68, 0.0]), SC * np.array([-0.68, 0.56, 0.0])]
P_B = BODY[1]                              # far point of the plate
O2_B = BODY[3]                             # a second body-fixed origin
FO = np.array([-6.0, -1.95, 0.0])          # origin of the fixed (inertial) frame
FS_TAG = 20                                # size of the on-figure vector labels


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-6 else 1.0)


class AngularVelocityBase(LandauBatchBase):
 EPISODE = 31; LANGUAGE = "zh"
 MODE_LABEL = {1: {"zh": "3 平移 + 3 轉動", "en": "3 translations + 3 rotations"},
               4: {"zh": "離軸越遠，轉動貢獻越大", "en": "farther from the axis, larger contribution"},
               5: {"zh": "角速度與原點的選擇無關", "en": "angular velocity is origin-independent"},
               6: {"zh": "瞬時轉動軸", "en": "instantaneous axis of rotation"}}
 # The centre of mass sweeps left and right at a nearly constant speed (a
 # rounded triangle wave), so V stays clearly visible instead of dying away
 # twice per cycle as it would on a sinusoidal path.
 A = 2.7; W = 0.34; CY = -0.22; KT = 0.97
 SPIN = 0.60; AS = 1.03                    # spin rate, velocity->screen-length scale
 RW = 1.15; GY = -1.62; WAS = 2.2          # rolling wheel radius, ground height, its arrow scale

 # ── geometry of the drifting, spinning plate ──────────────────────
 def _cm(self):
  p = self.W * self.t.get_value()
  return np.array([self.A * (2 / PI) * np.arcsin(self.KT * np.sin(p)), self.CY, 0.0])

 def _V(self):
  p = self.W * self.t.get_value(); s = self.KT * np.sin(p)
  return np.array([self.A * (2 / PI) * self.KT * self.W * np.cos(p)
                   / max(float(np.sqrt(1 - s * s)), 1e-3), 0.0, 0.0])

 def _rot(self, b):
  th = self.SPIN * self.t.get_value(); c, s = np.cos(th), np.sin(th)
  return np.array([c * b[0] - s * b[1], s * b[0] + c * b[1], 0.0])

 def _pt(self, b):
  return self._cm() + self._rot(b)

 def _cross(self, b):                       # Omega x r for a body-fixed point b
  r = self._rot(b)
  return self.SPIN * np.array([-r[1], r[0], 0.0])

 # ── drawing helpers ───────────────────────────────────────────────
 def _tip(self, start, vec, scale=None):
  d = np.asarray(vec, dtype=float) * (self.AS if scale is None else scale)
  n = float(np.linalg.norm(d))
  if n < 0.22: d = d / max(n, 1e-6) * 0.22
  return np.asarray(start, dtype=float) + d

 def _arr(self, start, vec, color, sw=5, scale=None):
  return Arrow(start, self._tip(start, vec, scale), buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.32, tip_length=0.2)

 def _spin_arc(self, centre, radius, color=ACCENT_C):
  a = Arc(radius=radius, start_angle=0.32 * PI, angle=1.16 * PI, color=color,
          stroke_width=4, arc_center=centre)
  a.add_tip(tip_length=0.22)
  return a

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off))
  return m

 def beat(self, i, fin=(), fout=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  r = min(0.5, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate.increment_value(r), run_time=r, rate_func=linear)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate.increment_value(d), run_time=d, rate_func=linear)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * 2.35)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.t = ValueTracker(0.0); self.t6 = 0.0; self.d6 = self.dur(6)
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ── the rigid plate ───────────────────────────────────────────────
  plate = always_redraw(lambda: Polygon(*[self._pt(b) for b in BODY], color=ACCENT_A,
                                        stroke_width=3, fill_opacity=0.10, fill_color=ACCENT_A))
  parts = VGroup(*[always_redraw(lambda b=b: Dot(self._pt(b), color=ACCENT_A, radius=0.075))
                   for b in BODY])
  rods = VGroup(*[always_redraw(lambda a=BODY[i], c=BODY[j]:
                                DashedLine(self._pt(a), self._pt(c), color=GHOST,
                                           stroke_width=2, dash_length=0.09))
                  for i in range(4) for j in range(i + 1, 4)])
  cm = always_redraw(lambda: Dot(self._cm(), color=ACCENT_B, radius=0.085))
  cm_tag = self._tag("O", self._cm, off=np.array([-0.16, -0.32, 0.0]), color=ACCENT_B)

  # ── the two coordinate frames ─────────────────────────────────────
  fx = Arrow(FO, FO + np.array([0.95, 0, 0]), buff=0, color=GHOST, stroke_width=3, tip_length=0.16)
  fy = Arrow(FO, FO + np.array([0, 0.95, 0]), buff=0, color=GHOST, stroke_width=3, tip_length=0.16)
  fxl = Text("X", font_size=FS_SMALL, color=DIM).next_to(fx, DOWN, buff=0.1)
  fyl = Text("Y", font_size=FS_SMALL, color=DIM).next_to(fy, UP, buff=0.1)
  fixed = VGroup(fx, fy, fxl, fyl)
  bx = always_redraw(lambda: Arrow(self._cm(), self._cm() + self._rot(np.array([0.72, 0, 0])),
                                   buff=0, color=ACCENT_B, stroke_width=3, tip_length=0.15))
  by = always_redraw(lambda: Arrow(self._cm(), self._cm() + self._rot(np.array([0, 0.72, 0])),
                                   buff=0, color=ACCENT_B, stroke_width=3, tip_length=0.15))
  body_frame = VGroup(bx, by)

  # ── translation + rotation split ──────────────────────────────────
  Rvec = always_redraw(lambda: Arrow(FO, self._cm(), buff=0, color=DIM, stroke_width=3, tip_length=0.18))
  Rtag = self._tag("R", lambda: 0.55 * FO + 0.45 * self._cm(),
                   off=np.array([-0.1, 0.3, 0.0]), color=DIM)
  arc = always_redraw(lambda: self._spin_arc(self._cm(), 1.42))
  dphi_tag = self._tag("dφ", self._cm, off=np.array([0.0, 1.70, 0.0]), color=ACCENT_C)
  om_tag = self._tag("Ω", self._cm, off=np.array([0.0, 1.70, 0.0]), color=ACCENT_C)

  # ── the vector triangle v = V + Omega x r at the far point P ──────
  Pdot = always_redraw(lambda: Dot(self._pt(P_B), color=WARN, radius=0.085))
  Ptag = self._tag("P", lambda: self._pt(P_B) + 0.36 * _unit(self._rot(P_B)), off=0 * UP, color=WARN)
  rvec = always_redraw(lambda: Line(self._cm(), self._pt(P_B), color=DIM, stroke_width=2.5))
  rtag = self._tag("r", lambda: 0.5 * (self._cm() + self._pt(P_B))
                   - 0.30 * _unit(self._cross(P_B)), off=0 * UP, color=DIM)
  Varr = always_redraw(lambda: self._arr(self._cm(), self._V(), ACCENT_B))
  Vtag = self._tag("V", lambda: self._tip(self._cm(), self._V()), off=UP * 0.32, color=ACCENT_B)
  leg1 = always_redraw(lambda: self._arr(self._pt(P_B), self._V(), ACCENT_B, sw=4))
  leg2 = always_redraw(lambda: self._arr(self._tip(self._pt(P_B), self._V()),
                                         self._cross(P_B), ACCENT_C, sw=4))
  leg2tag = self._tag("Ω × r",
                      lambda: 0.5 * (self._tip(self._pt(P_B), self._V())
                                     + self._tip(self._tip(self._pt(P_B), self._V()), self._cross(P_B)))
                      + 0.42 * _unit(self._rot(P_B)), off=0 * UP, color=ACCENT_C)
  varr = always_redraw(lambda: self._arr(self._pt(P_B), self._V() + self._cross(P_B), WARN, sw=6))
  vtag = self._tag("v", lambda: self._tip(self._pt(P_B), self._V() + self._cross(P_B))
                   + 0.30 * _unit(self._V() + self._cross(P_B)), off=0 * UP, color=WARN)
  triangle = VGroup(leg1, leg2, leg2tag, varr, vtag)

  # ── rotational part grows with distance from the axis ─────────────
  ladder = VGroup()
  for f in (0.34, 0.67, 1.0):
   b = f * P_B
   ladder.add(always_redraw(lambda b=b: Dot(self._pt(b), color=ACCENT_C, radius=0.065)),
              always_redraw(lambda b=b: self._arr(self._pt(b), self._cross(b), ACCENT_C, sw=4)))

  # ── a second body-fixed origin O' ─────────────────────────────────
  O2 = always_redraw(lambda: Dot(self._pt(O2_B), color=WARN, radius=0.085))
  O2tag = self._tag("O′", lambda: self._pt(O2_B) + 0.34 * _unit(self._rot(O2_B)), off=0 * UP, color=WARN)
  avec = always_redraw(lambda: Line(self._cm(), self._pt(O2_B), color=DIM, stroke_width=2.5))
  atag = self._tag("a", lambda: 0.5 * (self._cm() + self._pt(O2_B))
                   - 0.28 * _unit(self._cross(O2_B)), off=0 * UP, color=DIM)
  aleg1 = always_redraw(lambda: self._arr(self._pt(O2_B), self._V(), ACCENT_B, sw=4))
  aleg2 = always_redraw(lambda: self._arr(self._tip(self._pt(O2_B), self._V()),
                                          self._cross(O2_B), ACCENT_C, sw=4))
  aleg2tag = self._tag("Ω × a",
                       lambda: 0.5 * (self._tip(self._pt(O2_B), self._V())
                                      + self._tip(self._tip(self._pt(O2_B), self._V()),
                                                  self._cross(O2_B)))
                       + 0.42 * _unit(self._rot(O2_B)), off=0 * UP, color=ACCENT_C)
  V2arr = always_redraw(lambda: self._arr(self._pt(O2_B), self._V() + self._cross(O2_B),
                                          ACCENT_B, sw=6))
  V2tag = self._tag("V′", lambda: self._tip(self._pt(O2_B), self._V() + self._cross(O2_B))
                    + 0.32 * _unit(self._V() + self._cross(O2_B)), off=0 * UP, color=ACCENT_B)
  at_O2 = VGroup(avec, atag, O2, O2tag, aleg1, aleg2, aleg2tag, V2arr, V2tag)

  stage_a = VGroup(plate, parts, cm, cm_tag, fixed, Rvec, Rtag, arc, om_tag,
                   at_O2, Varr, Vtag)

  # ── beat 6: the rolling wheel ─────────────────────────────────────
  def wc():
   return np.array([-4.2 + 8.4 * (self.t.get_value() - self.t6) / self.d6, self.GY + self.RW, 0.0])

  def wv():
   return np.array([8.4 / self.d6, 0.0, 0.0])

  def spokes():
   c = wc(); th = -c[0] / self.RW
   return VGroup(*[Line(c, c + self.RW * np.array([np.cos(th + k * PI / 2),
                                                   np.sin(th + k * PI / 2), 0.0]),
                        color=DIM, stroke_width=2.5) for k in range(4)])
  ground = Line([-6.6, self.GY, 0], [6.6, self.GY, 0], color=GHOST, stroke_width=4)
  rim = always_redraw(lambda: Circle(radius=self.RW, color=ACCENT_A, stroke_width=4).move_to(wc()))
  spk = always_redraw(spokes)
  wcm = always_redraw(lambda: Dot(wc(), color=ACCENT_B, radius=0.085))
  wV = always_redraw(lambda: self._arr(wc(), wv(), ACCENT_B, scale=self.WAS))
  wVt = self._tag("V", lambda: self._tip(wc(), wv(), self.WAS), off=UP * 0.32, color=ACCENT_B)
  top = always_redraw(lambda: self._arr(wc() + UP * self.RW, 2 * wv(), ACCENT_C, scale=self.WAS))
  topt = self._tag("2V", lambda: self._tip(wc() + UP * self.RW, 2 * wv(), self.WAS),
                   off=UP * 0.32, color=ACCENT_C)
  cdot = always_redraw(lambda: Dot(wc() + DOWN * self.RW, color=WARN, radius=0.12))
  ctag = self._tag("v = 0", lambda: wc() + DOWN * self.RW, off=DOWN * 0.34, color=WARN)
  wheel = VGroup(ground, rim, spk, wcm, wV, wVt, top, topt, cdot, ctag)

  # ── run the beats ─────────────────────────────────────────────────
  active_sub = None; active_f = None
  def run(i, fin=(), fout=()):
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
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  self.add(plate, parts, cm, cm_tag)
  run(0, fin=[rods])                                        # rigid: distances stay constant
  run(1, fin=[fixed, body_frame], fout=[rods])              # two frames, six degrees of freedom
  run(2, fin=[Rvec, Rtag, arc, dphi_tag])                   # dr = dR + dphi x r
  run(3, fin=[Pdot, Ptag, rvec, rtag, Varr, Vtag, triangle],
      fout=[body_frame])                                    # v = V + Omega x r
  run(4, fin=[ladder, om_tag],
      fout=[triangle, dphi_tag, Pdot, Ptag, rvec, rtag])      # Omega = dphi/dt, grows with r
  run(5, fin=[at_O2], fout=[ladder])                          # V' = V + Omega x a, Omega' = Omega
  self.t6 = self.t.get_value()
  self.play(FadeOut(stage_a), FadeIn(wheel), run_time=0.6)
  run(6)                                                    # instantaneous axis of rotation
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL31{'ZH' if lang == 'zh' else 'EN'}", (AngularVelocityBase,), {"LANGUAGE": lang})

LandauL31ZH = _mk("zh")
LandauL31EN = _mk("en")
