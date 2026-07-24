"""Lesson 27 — Parametric resonance (animated pumped swing).

A pendulum whose length is modulated at twice the swing frequency (2 w0),
so its amplitude grows exponentially: the classic "pumping a swing" image
of parametric resonance. The swing amplitude grows within every beat.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Circle, Dot, FadeIn, FadeOut, Line, Text, ValueTracker,
                   always_redraw, linear, UP, DOWN, LEFT, RIGHT)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, DIM, GHOST, INK,
                                             FS_BODY, FS_H1, FS_H2, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class ParametricBase(LandauBatchBase):
 EPISODE = 27; LANGUAGE = "zh"

 def _state(self, t):
  A = min(self.thmax, self.th0 * np.exp(self.s * t))
  theta = A * np.sin(self.w0 * t)
  L = self.L0 * (1 - 0.11 * np.cos(2 * self.w0 * t))   # length pumped at 2 w0
  return theta, L

 def _bob(self):
  th, L = self._state(self.t.get_value())
  return self.pivot + np.array([L * np.sin(th), -L * np.cos(th), 0.0])

 def beat(self, i, fin=(), fout=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  self.t.set_value(0); r = min(0.45, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate.set_value(r), run_time=r, rate_func=linear)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate.set_value(r + d), run_time=d, rate_func=linear)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * 2.2)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.pivot = np.array([0.0, 1.35, 0.0]); self.L0 = 2.45
  self.w0 = 2.0; self.s = 0.24; self.th0 = 0.10; self.thmax = 0.80
  self.t = ValueTracker(0.0)
  F = FORMULAS[self.EPISODE]

  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  ceiling = Line(self.pivot + LEFT * 0.7, self.pivot + RIGHT * 0.7, color=GHOST, stroke_width=5)
  pivot_dot = Dot(self.pivot, color=GHOST, radius=0.06)
  rod = always_redraw(lambda: Line(self.pivot, self._bob(), color=DIM, stroke_width=4))
  bob = always_redraw(lambda: Circle(radius=0.24, color=ACCENT_A, fill_opacity=1,
                                     stroke_width=0).move_to(self._bob()))
  self.add(heading, ceiling, pivot_dot, rod, bob)

  active_sub = None; active_f = None
  def run(i):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = [s]; fout = []
   if active_sub is not None: fout.append(active_sub)
   if i in F:
    f = self.formula(F[i]); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  for i in range(7):
   run(i)
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL27{'ZH' if lang == 'zh' else 'EN'}", (ParametricBase,), {"LANGUAGE": lang})

LandauL27ZH = _mk("zh")
LandauL27EN = _mk("en")
