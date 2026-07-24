"""Lesson 24 — Vibrations of a linear triatomic molecule (animated).

A linear A–B–A molecule whose normal modes are animated: the symmetric
stretch, the antisymmetric stretch, and the (doubly degenerate) bending
mode. Beat 0 first shows the non-vibrational rigid translation+rotation.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Circle, FadeIn, FadeOut, Line, Text, VGroup, ValueTracker,
                   always_redraw, linear, UP, DOWN)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS


class MoleculeBase(LandauBatchBase):
 EPISODE = 24; LANGUAGE = "zh"
 MODE_LABEL = {
  1: {"zh": "非直線分子   ", "en": "non-linear:   "},
  2: {"zh": "直線分子   ",   "en": "linear:   "},
  4: {"zh": "對稱伸縮   ",   "en": "symmetric stretch   "},
  5: {"zh": "反對稱伸縮   ", "en": "antisymmetric stretch   "},
  6: {"zh": "彎曲模態（簡併 ×2）", "en": "bending  (×2, degenerate)"},
 }

 # ── displacements (dx, dy) of the three atoms per mode ────────────
 def _disp(self, t):
  m = self.mode
  if m == "rigid":
   th = 0.26 * np.sin(0.9 * t); sh = 0.7 * np.sin(0.6 * t); out = []
   for rx, ry in self.rest:
    out.append((rx * np.cos(th) - ry * np.sin(th) + sh - rx,
                rx * np.sin(th) + ry * np.cos(th) - ry))
   return out
  if m == "sym":
   v = 0.42 * np.cos(self.ws * t); return [(-v, 0), (0, 0), (v, 0)]
  if m == "anti":
   v = 0.32 * np.cos(self.wa * t); c = 0.60 * np.cos(self.wa * t)
   return [(v, 0), (-c, 0), (v, 0)]
  if m == "bend":
   o = 0.22 * np.cos(self.wb * t); g = 0.50 * np.cos(self.wb * t)
   return [(0, -o), (0, g), (0, -o)]
  return [(0, 0), (0, 0), (0, 0)]

 def _pos(self, i):
  d = self._disp(self.t.get_value())[i]
  return [self.rest[i][0] + d[0], self.y0 + d[1], 0]

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
  if m.width > 12.3: m.scale_to_fit_width(12.3)
  return m.move_to(UP * 2.1)

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.y0 = -0.55; self.rest = [(-2.1, 0), (0.0, 0), (2.1, 0)]
  self.ws = 2.0; self.wa = 3.0; self.wb = 1.5
  self.mode = "rest"; self.t = ValueTracker(0.0)
  F = FORMULAS[self.EPISODE]

  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  bond1 = always_redraw(lambda: Line(self._pos(0), self._pos(1), color=GHOST, stroke_width=5))
  bond2 = always_redraw(lambda: Line(self._pos(1), self._pos(2), color=GHOST, stroke_width=5))
  cols = [ACCENT_B, ACCENT_C, ACCENT_B]; rads = [0.30, 0.34, 0.30]
  atoms = []
  for i in range(3):
   c = Circle(radius=rads[i], color=cols[i], fill_opacity=1, stroke_width=0)
   c.add_updater(lambda m, i=i: m.move_to(self._pos(i)))
   atoms.append(c)
  names = ["m₁", "m₂", "m₁"]
  labels = []
  for i in range(3):
   lab = Text(names[i], font_size=FS_SMALL, color=DIM)
   lab.add_updater(lambda m, i=i: m.move_to([self._pos(i)[0], self.y0 - 0.66, 0]))
   labels.append(lab)
  self.add(heading, bond1, bond2, *atoms, *labels)

  active_sub = None; active_f = None
  def run(i, mode):
   nonlocal active_sub, active_f
   self.mode = mode
   s = self.sub(self.lines[i]); fin = [s]; fout = []
   if active_sub is not None: fout.append(active_sub)
   lang = "zh" if self.LANGUAGE == "zh" else "en"
   txt = None
   if i in self.MODE_LABEL: txt = self.MODE_LABEL[i][lang]
   if i in F: txt = (txt + F[i]) if txt else F[i]
   if txt is not None:
    f = self.formula(txt); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  run(0, "rigid")    # non-vibrational translation + rotation
  run(1, "rest")     # 3n - 6 counting
  run(2, "rest")     # linear: 3n - 5
  run(3, "rest")     # remove translation + rotation
  run(4, "sym")      # symmetric stretch
  run(5, "anti")     # antisymmetric stretch
  run(6, "bend")     # bending (degenerate)
  self.wait(.6)


def _mk(lang):
 return type(f"LandauL24{'ZH' if lang == 'zh' else 'EN'}", (MoleculeBase,), {"LANGUAGE": lang})

LandauL24ZH = _mk("zh")
LandauL24EN = _mk("en")
