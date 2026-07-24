"""Lesson 28 — Anharmonic oscillations (animated x(t) graphs).

Shows the two qualitative effects of non-linearity: the waveform is no
longer a pure sine (overtones), and the frequency depends on amplitude,
so two oscillators of different amplitude drift out of step.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Axes, Create, FadeIn, FadeOut, Text, VGroup, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class AnharmonicBase(LandauBatchBase):
 EPISODE = 28; LANGUAGE = "zh"

 def beat(self, i, fin=(), fout=(), draw=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  intro = [FadeIn(m) for m in fin] + [FadeOut(m) for m in fout]
  if intro:
   r = min(0.55, d); self.play(*intro, run_time=r); d -= r
  if draw and d > 0.2:
   dr = min(d, max(1.2, d - 0.6)); self.play(*draw, run_time=dr); d -= dr
  if d > 0.05: self.wait(d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * 2.2)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  ax = Axes(x_range=[0, 9, 1], y_range=[-1.4, 1.4, 1], x_length=10.6, y_length=2.8,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([0, -0.6, 0])
  self.add(heading, ax)

  def cv(fn, color):
   return ax.plot(fn, x_range=[0, 9, 0.02], color=color, stroke_width=4)
  ref = cv(lambda t: 0.9 * np.cos(2.0 * t), ACCENT_B)                       # pure sine
  anh = cv(lambda t: 0.9 * np.cos(2.0 * t) + 0.25 * np.cos(4.0 * t) - 0.18, ACCENT_A)  # distorted
  small = cv(lambda t: 0.4 * np.cos(2.0 * t), ACCENT_B)                     # small amplitude
  large = cv(lambda t: 1.05 * np.cos(1.6 * t), WARN)                        # large amplitude, lower w

  active_sub = None; active_f = None
  def run(i, fout=(), draw=()):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = [s]; fout = list(fout)
   if active_sub is not None: fout.append(active_sub)
   if i in F:
    f = self.formula(F[i]); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout, draw=draw)
   active_sub = s

  run(0, draw=[Create(ref)])                                # harmonic = pure sine
  run(1)                                                    # Lagrangian with anharmonic terms
  run(2)                                                    # non-linear equation
  run(3)                                                    # successive approximation
  run(4, draw=[Create(anh)])                                # overtones -> distorted waveform
  run(5, fout=[ref, anh], draw=[Create(small), Create(large)])  # amplitude-dependent frequency
  run(6)                                                    # summary
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL28{'ZH' if lang == 'zh' else 'EN'}", (AnharmonicBase,), {"LANGUAGE": lang})

LandauL28ZH = _mk("zh")
LandauL28EN = _mk("en")
