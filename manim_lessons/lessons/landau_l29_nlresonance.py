"""Lesson 29 — Resonance in non-linear oscillations (animated).

The resonance curve transforms from a symmetric peak (linear) to a
leaning peak and finally a folded, multi-valued curve (three amplitudes,
middle branch unstable), giving jumps and hysteresis.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Axes, Create, FadeIn, FadeOut, Text, VGroup, VMobject, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class NLResonanceBase(LandauBatchBase):
 EPISODE = 29; LANGUAGE = "zh"
 MODE_LABEL = {
  4: {"zh": "三個振幅：中間分支不穩定", "en": "three amplitudes: middle branch unstable"},
  5: {"zh": "跳變與遲滯", "en": "jumps and hysteresis"},
 }

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

 def _rescurve(self, ax, A, kappa, lam, color, bmin=0.35, n=260):
  bmax = A / lam
  bs = np.linspace(bmin, bmax, n)
  def eps(b, sign):
   return kappa * b * b + sign * np.sqrt(max(0.0, A * A / (b * b) - lam * lam))
  pts = [ax.c2p(eps(b, -1), b) for b in bs] + [ax.c2p(eps(b, +1), b) for b in bs[::-1]]
  m = VMobject(color=color, stroke_width=4); m.set_points_smoothly(pts)
  return m

 def construct(self):
  A_lin, A_lean, A_fold = 0.40, 0.42, 0.52
  kap, lam = 0.30, 0.20
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  ax = Axes(x_range=[-1.5, 2.5, 1], y_range=[0, 2.6, 1], x_length=9.6, y_length=3.2,
            axis_config={"color": GHOST, "stroke_width": 2, "include_ticks": False})
  ax.move_to([0, -0.55, 0])
  ex = Text("ε", font_size=FS_SMALL, color=DIM).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
  bx = Text("b", font_size=FS_SMALL, color=DIM).next_to(ax.y_axis.get_end(), UP, buff=0.08)
  self.add(heading, ax, ex, bx)

  sym = self._rescurve(ax, A_lin, 0.0, lam, ACCENT_B)
  lean = self._rescurve(ax, A_lean, kap, lam, ACCENT_A)
  fold = self._rescurve(ax, A_fold, kap, lam, WARN)
  # jump arrows on the folded curve
  bs = np.linspace(0.35, A_fold / lam, 400)
  ep_up = kap * bs * bs + np.sqrt(np.maximum(0.0, A_fold ** 2 / bs ** 2 - lam ** 2))
  iC = int(np.argmin(ep_up)); eC, bC = ep_up[iC], bs[iC]
  eD = kap * (A_fold / lam) ** 2
  down = Arrow(ax.c2p(eC, bC - 0.06), ax.c2p(eC, 0.42), color=ACCENT_B, buff=0, stroke_width=5,
               max_tip_length_to_length_ratio=0.28)
  up = Arrow(ax.c2p(eD, 0.5), ax.c2p(eD, A_fold / lam - 0.06), color=ACCENT_C, buff=0, stroke_width=5,
             max_tip_length_to_length_ratio=0.28)

  active_sub = None; active_f = None
  def run(i, fout=(), draw=()):
   nonlocal active_sub, active_f
   s = self.sub(self.lines[i]); fin = [s]; fout = list(fout)
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

  run(0)                                       # non-linear driven oscillator
  run(1, draw=[Create(sym)])                   # symmetric linear peak
  run(2)                                        # amplitude-dependent frequency
  run(3, fout=[sym], draw=[Create(lean)])      # peak leans over
  run(4, fout=[lean], draw=[Create(fold)])     # folded, three roots
  run(5, draw=[FadeIn(down), FadeIn(up)])      # jumps and hysteresis
  run(6)                                        # summary
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL29{'ZH' if lang == 'zh' else 'EN'}", (NLResonanceBase,), {"LANGUAGE": lang})

LandauL29ZH = _mk("zh")
LandauL29EN = _mk("en")
