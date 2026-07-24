"""Lesson 23 — Normal modes of a coupled two-mass system (animated).

Two masses joined by three springs between fixed walls. The two normal
modes (in-phase and out-of-phase) are animated, then their superposition.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, FadeIn, FadeOut, Line, ParametricFunction, Square, Text,
                   VGroup, ValueTracker, always_redraw, linear, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class NormalBase(LandauBatchBase):
 EPISODE = 23; LANGUAGE = "zh"
 # language-specific captions for the two normal-mode beats
 MODE_LABEL = {4: {"zh": "同相 ", "en": "in-phase :  "},
               5: {"zh": "反相 ", "en": "out-of-phase :  "}}

 # ── displacements of the two masses ───────────────────────────────
 def _d(self, t):
  m = self.mode
  if m == "sym":   v = self.A * np.cos(self.w1 * t); return v, v
  if m == "anti":  v = self.A * np.cos(self.w2 * t); return v, -v
  if m == "super":
   a = self.As * np.cos(self.w1 * t); b = self.Aa * np.cos(self.w2 * t)
   return a + b, a - b
  return 0.0, 0.0

 def spring(self, x1, x2, coils=6, amp=0.16):
  y = self.y0
  def f(s):
   x = x1 + (x2 - x1) * s
   yy = y + (amp * np.sin(2 * np.pi * coils * s) if 0.07 < s < 0.93 else 0.0)
   return np.array([x, yy, 0.0])
  return ParametricFunction(f, t_range=[0, 1, 0.01], color=DIM, stroke_width=2.5)

 def _arrows(self):
  if self.mode not in ("sym", "anti", "super"): return VGroup()
  d1, d2 = self._d(self.t.get_value()); g = VGroup()
  for X, d, c in ((self.X1, d1, ACCENT_A), (self.X2, d2, ACCENT_C)):
   if abs(d) > 0.08:
    cx = X + d; y = self.y0 + 0.75
    g.add(Arrow([cx, y, 0], [cx + 1.1 * d, y, 0], color=c, buff=0,
                stroke_width=5, max_tip_length_to_length_ratio=0.5))
  return g

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

 def construct(self):
  self.wall_l = -5.2; self.wall_r = 5.2; self.y0 = -0.5
  self.X1 = -1.4; self.X2 = 1.4; self.hw = 0.3
  self.w1 = 1.6; self.w2 = 2.77; self.A = 0.7; self.As = 0.5; self.Aa = 0.42
  self.mode = "rest"; self.t = ValueTracker(0.0)
  F = FORMULAS[self.EPISODE]

  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  wl = Line([self.wall_l, self.y0 - 0.7, 0], [self.wall_l, self.y0 + 0.7, 0], color=GHOST, stroke_width=6)
  wr = Line([self.wall_r, self.y0 - 0.7, 0], [self.wall_r, self.y0 + 0.7, 0], color=GHOST, stroke_width=6)
  ground = Line([self.wall_l, self.y0 - 0.7, 0], [self.wall_r, self.y0 - 0.7, 0], color=GHOST, stroke_width=2)
  m1 = Square(side_length=0.6, color=ACCENT_B, fill_opacity=1, stroke_width=0)
  m2 = Square(side_length=0.6, color=ACCENT_C, fill_opacity=1, stroke_width=0)
  m1.add_updater(lambda m: m.move_to([self.X1 + self._d(self.t.get_value())[0], self.y0, 0]))
  m2.add_updater(lambda m: m.move_to([self.X2 + self._d(self.t.get_value())[1], self.y0, 0]))
  sL = always_redraw(lambda: self.spring(self.wall_l, self.X1 + self._d(self.t.get_value())[0] - self.hw))
  sM = always_redraw(lambda: self.spring(self.X1 + self._d(self.t.get_value())[0] + self.hw,
                                         self.X2 + self._d(self.t.get_value())[1] - self.hw, coils=5))
  sR = always_redraw(lambda: self.spring(self.X2 + self._d(self.t.get_value())[1] + self.hw, self.wall_r))
  arrows = always_redraw(self._arrows)
  self.add(heading, wl, wr, ground, sL, sM, sR, m1, m2, arrows)

  active_sub = None; active_f = None
  def run(i, mode):
   nonlocal active_sub, active_f
   self.mode = mode
   s = self.sub(self.lines[i]); fin = [s]; fout = []
   if active_sub is not None: fout.append(active_sub)
   if i in F:
    txt = F[i]
    if i in self.MODE_LABEL:
     txt = self.MODE_LABEL[i]["zh" if self.LANGUAGE == "zh" else "en"] + txt
    f = self.formula(txt); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  run(0, "rest")     # coupled system at rest
  run(1, "rest")     # quadratic Lagrangian
  run(2, "rest")     # assume common frequency
  run(3, "rest")     # characteristic equation → eigenfrequencies
  run(4, "sym")      # normal mode 1: in-phase
  run(5, "anti")     # normal mode 2: out-of-phase
  run(6, "super")    # general motion = superposition
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL23{'ZH' if lang == 'zh' else 'EN'}", (NormalBase,), {"LANGUAGE": lang})

LandauL23ZH = _mk("zh")
LandauL23EN = _mk("en")
