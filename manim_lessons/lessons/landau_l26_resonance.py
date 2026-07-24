"""Lesson 26 — Forced oscillations under friction (animated resonance curves).

Builds the amplitude-vs-driving-frequency plot and then draws a family of
resonance curves for decreasing damping, so the peak visibly grows taller
and sharper (smaller lambda -> larger quality factor).
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Axes, Create, DashedLine, FadeIn, FadeOut, Text, VGroup, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class ResonanceBase(LandauBatchBase):
 EPISODE = 26; LANGUAGE = "zh"

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
  return m.move_to(UP * 2.15)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  w0 = 1.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, 6, 1], x_length=8.8, y_length=3.3,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([0, -0.5, 0])
  gl = Text("γ", font_size=FS_SMALL, color=DIM).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
  bl = Text("b", font_size=FS_SMALL, color=DIM).next_to(ax.y_axis.get_end(), UP, buff=0.08)
  axg = VGroup(ax, gl, bl)

  def bc(lam, color):
   return ax.plot(lambda g: 1.0 / np.sqrt((w0 ** 2 - g ** 2) ** 2 + 4 * lam ** 2 * g ** 2),
                  x_range=[0.02, 2.2, 0.008], color=color, stroke_width=4)
  c0 = bc(0.45, DIM); c1 = bc(0.28, ACCENT_B); c2 = bc(0.16, ACCENT_A); c3 = bc(0.09, WARN)
  wline = DashedLine(ax.c2p(w0, 0), ax.c2p(w0, 6), color=DIM, stroke_width=2)
  wlab = Text("ω₀", font_size=FS_SMALL, color=DIM).next_to(ax.c2p(w0, 0), DOWN, buff=0.15)

  active_sub = None; active_f = None
  def run(i, fin=(), fout=(), draw=()):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = list(fin) + [s]; fout = list(fout)
   if active_sub is not None: fout.append(active_sub)
   if i in F:
    f = self.formula(F[i]); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout, draw=draw)
   active_sub = s

  run(0)                                       # driven damped equation
  run(1)                                       # steady state after transient
  run(2, fin=[axg], draw=[Create(c0)])         # amplitude curve (broad, large damping)
  run(3, fin=[wline, wlab])                    # finite peak near omega_0
  run(4, draw=[Create(c1), Create(c2), Create(c3)])  # family: smaller damping -> sharper
  run(5)                                        # quality factor Q
  run(6)                                        # phase lag
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL26{'ZH' if lang == 'zh' else 'EN'}", (ResonanceBase,), {"LANGUAGE": lang})

LandauL26ZH = _mk("zh")
LandauL26EN = _mk("en")
