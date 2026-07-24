"""Lesson 22 — Forced oscillations & resonance (animated).

Reuses the timing helpers of LandauBatchBase but replaces the static
formula stage with a live spring-mass oscillator, a driving-force arrow,
a resonance curve, and the linear amplitude growth at resonance.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Axes, DashedLine, FadeIn, FadeOut, Line, ParametricFunction,
                   Square, Text, VGroup, ValueTracker, always_redraw, linear, UP, DOWN, RIGHT)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class ForcedBase(LandauBatchBase):
 EPISODE = 22; LANGUAGE = "zh"

 # ── physics of the on-screen mass ─────────────────────────────────
 def _disp(self, t):
  m = self.mode
  if m == "driven": return self.amp * np.cos(self.gamma * t)
  if m == "grow":   return min(self.cap, self.rate * t) * np.sin(self.omega * t)
  if m == "free":   return 0.8 * np.cos(self.omega * t)
  return 0.0

 def spring(self, x2):
  x1, y = self.wall_x, self.y0
  def f(s):
   x = x1 + (x2 - x1) * s
   yy = y + (0.18 * np.sin(2 * np.pi * 7 * s) if 0.06 < s < 0.94 else 0.0)
   return np.array([x, yy, 0.0])
  return ParametricFunction(f, t_range=[0, 1, 0.01], color=DIM, stroke_width=2.5)

 def _arrow(self):
  t = self.t.get_value()
  if self.mode not in ("driven", "grow"): return VGroup()
  val = np.cos(self.gamma * t) if self.mode == "driven" else np.cos(self.omega * t)
  if abs(val) < 0.06: return VGroup()
  cx = self.x0 + self._disp(t); y = self.y0 + 0.8
  return Arrow([cx, y, 0], [cx + 0.9 * val, y, 0], color=WARN, buff=0,
               stroke_width=5, max_tip_length_to_length_ratio=0.45)

 # ── beat playback: audio + fades while the mass keeps moving ───────
 def beat(self, i, fin=(), fout=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  self.t.set_value(0); r = min(0.45, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate.set_value(r), run_time=r, rate_func=linear)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate.set_value(r + d), run_time=d, rate_func=linear)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.1)
  if m.width > 12.3: m.scale_to_fit_width(12.3)
  return m.move_to(UP * 2.15)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def _resonance_curve(self):
  ax = Axes(x_range=[0, 3.4, 1], y_range=[0, 3, 1], x_length=4.4, y_length=2.8,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([4.15, self.y0 + 0.1, 0])
  fn = lambda g: min(2.85, 0.55 / abs(self.omega ** 2 - g ** 2))
  left = ax.plot(fn, x_range=[0.05, self.omega - 0.13, 0.01], color=ACCENT_B, stroke_width=4)
  right = ax.plot(fn, x_range=[self.omega + 0.13, 3.35, 0.01], color=ACCENT_B, stroke_width=4)
  asymp = DashedLine(ax.c2p(self.omega, 0), ax.c2p(self.omega, 3), color=WARN, stroke_width=3)
  gx = Text("γ", font_size=FS_SMALL, color=DIM).next_to(ax.x_axis.get_end(), DOWN, buff=0.12)
  wl = Text("ω", font_size=FS_SMALL, color=WARN).next_to(ax.c2p(self.omega, 0), DOWN, buff=0.12)
  ay = Text("a", font_size=FS_SMALL, color=DIM).next_to(ax.y_axis.get_end(), UP, buff=0.08)
  return VGroup(ax, left, right, asymp, gx, wl, ay)

 def construct(self):
  self.wall_x = -5.0; self.x0 = -1.6; self.y0 = -0.5
  self.omega = 2.2; self.gamma = 1.3; self.amp = 1.05; self.rate = 0.24; self.cap = 2.2
  self.mode = "rest"; self.t = ValueTracker(0.0)
  F = FORMULAS[self.EPISODE]

  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  wall = Line([self.wall_x, self.y0 - 0.7, 0], [self.wall_x, self.y0 + 0.7, 0], color=GHOST, stroke_width=6)
  ground = Line([self.wall_x, self.y0 - 0.7, 0], [1.4, self.y0 - 0.7, 0], color=GHOST, stroke_width=2)
  mass = Square(side_length=0.6, color=ACCENT_B, fill_opacity=1, stroke_width=0)
  mass.add_updater(lambda m: m.move_to([self.x0 + self._disp(self.t.get_value()), self.y0, 0]))
  spring = always_redraw(lambda: self.spring(self.x0 + self._disp(self.t.get_value()) - 0.3))
  arrow = always_redraw(self._arrow)
  self.add(heading, wall, ground, spring, mass, arrow)

  active_sub = None; active_f = None; curve = None
  def run(i, mode, gamma=None, extra_in=(), extra_out=()):
   nonlocal active_sub, active_f
   self.mode = mode
   if gamma is not None: self.gamma = gamma
   s = self.sub(self.lines[i])
   fin = list(extra_in) + [s]; fout = list(extra_out)
   if active_sub is not None: fout.append(active_sub)
   if i in F:
    f = self.formula(F[i]); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  run(0, "rest")                       # oscillator at rest
  run(1, "driven", gamma=1.3)          # add the force  → mass driven
  run(2, "driven", gamma=1.3)          # periodic force
  run(3, "driven", gamma=1.3)          # steady-state amplitude
  curve = self._resonance_curve()
  run(4, "rest", extra_in=[curve])     # resonance curve appears
  run(5, "grow", gamma=self.omega, extra_out=[curve])   # amplitude grows at resonance
  # summary: calm free oscillation, drop the last formula
  self.mode = "free"
  s = self.sub(self.lines[6])
  self.beat(6, fin=[s], fout=[active_sub] + ([active_f] if active_f else []))
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL22{'ZH' if lang == 'zh' else 'EN'}", (ForcedBase,), {"LANGUAGE": lang})

LandauL22ZH = _mk("zh")
LandauL22EN = _mk("en")
