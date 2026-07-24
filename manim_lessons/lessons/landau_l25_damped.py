"""Lesson 25 — Damped oscillations (animated x(t) graphs).

An x(t) graph is drawn for each regime: the underdamped decaying
oscillation with its exp(-lambda t) envelope, the overdamped aperiodic
return, and the critically-damped return.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Axes, Create, DashedVMobject, FadeIn, FadeOut, Text, VGroup, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class DampedBase(LandauBatchBase):
 EPISODE = 25; LANGUAGE = "zh"
 MODE_LABEL = {
  3: {"zh": "欠阻尼  λ < ω₀", "en": "underdamped,  λ < ω₀"},
  5: {"zh": "過阻尼  λ > ω₀", "en": "overdamped,  λ > ω₀"},
  6: {"zh": "臨界阻尼  λ = ω₀", "en": "critical,  λ = ω₀"},
 }

 def beat(self, i, fin=(), fout=(), draw=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  intro = [FadeIn(m) for m in fin] + [FadeOut(m) for m in fout]
  if intro:
   r = min(0.55, d); self.play(*intro, run_time=r); d -= r
  if draw and d > 0.2:
   dr = max(1.0, d - 0.6); dr = min(dr, d); self.play(*draw, run_time=dr); d -= dr
  if d > 0.05: self.wait(d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * 2.15)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  w0 = 2.0
  lam_u = 0.35; wu = np.sqrt(w0 ** 2 - lam_u ** 2)
  lam_o = 2.6; disc = np.sqrt(lam_o ** 2 - w0 ** 2); r1 = -lam_o + disc; r2 = -lam_o - disc
  F = FORMULAS[self.EPISODE]

  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  ax = Axes(x_range=[0, 9, 1], y_range=[-1.25, 1.25, 1], x_length=10.6, y_length=2.9,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([0, -0.55, 0])
  self.add(heading, ax)

  def curve(fn, color, xr=(0, 9)):
   return ax.plot(fn, x_range=[xr[0], xr[1], 0.02], color=color, stroke_width=4)
  ref = curve(lambda t: np.cos(w0 * t), DIM)
  damped = curve(lambda t: np.exp(-lam_u * t) * np.cos(wu * t), ACCENT_B)
  env_p = curve(lambda t: np.exp(-lam_u * t), WARN); env_n = curve(lambda t: -np.exp(-lam_u * t), WARN)
  env = VGroup(DashedVMobject(env_p, num_dashes=34), DashedVMobject(env_n, num_dashes=34))
  over = curve(lambda t: (r1 * np.exp(r2 * t) - r2 * np.exp(r1 * t)) / (r1 - r2), ACCENT_A)
  crit = curve(lambda t: (1 + w0 * t) * np.exp(-w0 * t), ACCENT_C)

  active_sub = None; active_f = None
  def run(i, fin=(), fout=(), draw=()):
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
   self.beat(i, fin=fin, fout=fout, draw=draw)
   active_sub = s

  run(0, draw=[Create(ref)])            # free (frictionless) oscillation
  run(1)                                # damped-oscillator equation
  run(2)                                # characteristic roots
  run(3, fout=[ref], draw=[Create(damped), Create(env)])  # underdamped + envelope
  run(4)                                # energy decay
  run(5, fout=[damped, env], draw=[Create(over)])         # overdamped
  run(6, fout=[over], draw=[Create(crit)])                # critical
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL25{'ZH' if lang == 'zh' else 'EN'}", (DampedBase,), {"LANGUAGE": lang})

LandauL25ZH = _mk("zh")
LandauL25EN = _mk("en")
