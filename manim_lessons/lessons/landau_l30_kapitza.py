"""Lesson 30 — Motion in a rapidly oscillating field: Kapitza's pendulum.

Beats 0-3 show a particle whose motion splits into a slow drift X plus a
small fast jitter. Beats 4-6 show the Kapitza pendulum: a rapidly buzzing
pivot with the bob standing INVERTED (stable), beside the double-well
effective potential whose upper well holds the inverted state.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Axes, Circle, Dot, DashedLine, FadeIn, FadeOut, Line, Text,
                   VGroup, ValueTracker, always_redraw, linear, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class KapitzaBase(LandauBatchBase):
 EPISODE = 30; LANGUAGE = "zh"
 MODE_LABEL = {5: {"zh": "倒立變穩定", "en": "inverted becomes stable"}}

 # ── geometry helpers ──────────────────────────────────────────────
 def _pivot_y(self):
  return self.py0 + self.a_f * np.cos(self.w_f * self.t.get_value())

 def _particle(self):
  t = self.t.get_value()
  return np.array([1.7 * np.sin(0.28 * t), 0.35 + 0.34 * np.cos(self.w_f * t), 0.0])

 def _bob(self):
  th = self.wob * np.sin(self.w_s * self.t.get_value())          # wobble about the top
  return np.array([self.px + self.L * np.sin(th), self._pivot_y() + self.L * np.cos(th), 0.0])

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
  self.px = -3.3; self.py0 = -0.4; self.L = 1.8
  self.a_f = 0.16; self.w_f = 20.0; self.wob = 0.14; self.w_s = 2.6
  self.t = ValueTracker(0.0)
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # beats 0-3: particle = slow drift + fast jitter
  path = Line([-1.7, 0.35, 0], [1.7, 0.35, 0], color=GHOST, stroke_width=2)
  dot = always_redraw(lambda: Dot(self._particle(), color=ACCENT_A, radius=0.13))

  # beats 4-6: Kapitza pendulum (left)
  ceil = Line([self.px - 0.55, self.py0, 0], [self.px + 0.55, self.py0, 0], color=GHOST, stroke_width=5)
  ceil.add_updater(lambda m: m.move_to([self.px, self._pivot_y(), 0]))
  pivot = always_redraw(lambda: Dot([self.px, self._pivot_y(), 0], color=GHOST, radius=0.06))
  rod = always_redraw(lambda: Line([self.px, self._pivot_y(), 0], self._bob(), color=DIM, stroke_width=4))
  bob = always_redraw(lambda: Circle(radius=0.22, color=ACCENT_A, fill_opacity=1, stroke_width=0).move_to(self._bob()))
  pend = VGroup(ceil, pivot, rod, bob)

  # beats 4-6: effective potential double well (right)
  ax = Axes(x_range=[0, 2 * np.pi, np.pi], y_range=[-1.4, 1.7, 1], x_length=4.8, y_length=2.7,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([3.0, -0.35, 0])
  ueff = ax.plot(lambda th: -np.cos(th) + 0.9 * np.sin(th) ** 2, x_range=[0, 2 * np.pi, 0.02],
                 color=ACCENT_B, stroke_width=4)
  well = Dot(ax.c2p(np.pi, 1.0), color=ACCENT_A, radius=0.11)                 # inverted (up) well
  up = Text("↑", font_size=FS_SMALL, color=ACCENT_A).next_to(ax.c2p(np.pi, 1.0), UP, buff=0.08)
  dn = Text("↓", font_size=FS_SMALL, color=DIM).next_to(ax.c2p(0, -1.0), DOWN, buff=0.08)
  plot = VGroup(ax, ueff, up, dn)

  active_sub = None; active_f = None
  def run(i, fin=(), fout=()):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = list(fin) + [s]; fout = list(fout)
   if active_sub is not None: fout.append(active_sub)
   lang = "zh" if self.LANGUAGE == "zh" else "en"
   parts = []
   if i in self.MODE_LABEL: parts.append(self.MODE_LABEL[i][lang])
   if i in F: parts.append(F[i])
   if parts:
    f = self.formula("\n".join(parts)); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  self.add(path, dot)
  run(0)                                     # split: slow X + fast jitter
  run(1)                                     # fast jitter xi = -f/m w^2
  run(2)                                     # averaged: effective potential
  run(3)                                     # U_eff = U + f^2/4 m w^2
  self.remove(dot); self.play(FadeOut(path), FadeIn(pend), FadeIn(plot), run_time=0.6)
  run(4)                                     # Kapitza: pivot vibrates, sin^2 term
  run(5, fin=[well])                         # a^2 w^2 > 2gl -> inverted stable
  run(6)                                     # summary
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL30{'ZH' if lang == 'zh' else 'EN'}", (KapitzaBase,), {"LANGUAGE": lang})

LandauL30ZH = _mk("zh")
LandauL30EN = _mk("en")
