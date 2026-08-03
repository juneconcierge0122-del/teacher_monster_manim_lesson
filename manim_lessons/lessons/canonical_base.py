"""Shared scaffolding for the canonical-equations lessons (Landau chapter VII).

Every one of these lessons has the same shape — title, a formula block, a
right-hand panel of short bilingual rows, a picture on the left, and a beat per
narration line — so the plumbing lives here and each lesson file only has to
build its own pictures and captions.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Dot, FadeIn, FadeOut, Line, Text, VGroup, VMobject, DashedVMobject,
                   ValueTracker, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase

FS_TAG = 19
PX = 1.55                                   # left edge of the right-hand panel
RIGHT_EDGE = 6.30                           # nothing may cross this


class CanonicalBase(LandauBatchBase):
 """Subclasses set EPISODE, MODE_LABEL and implement `stage`.

 A lesson outside the Landau series also overrides `TOPICS_SRC`,
 `FORMULAS_SRC` and `AUDIO_PREFIX` (inherited from `LandauBatchBase`) to point
 at its own copy, and passes its own `prefix` to `make`."""
 LANGUAGE = "zh"
 MODE_LABEL = {}

 # ── text ──────────────────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  """A panel row, shrunk if it would run past the safe right edge.

  English labels run about twice as wide as the Chinese ones, so a row that
  fits in one language can be silently clipped in the other."""
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > RIGHT_EDGE:
   m.scale_to_fit_width(RIGHT_EDGE - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 def _mid(self, y, zh, en, color=DIM, size=FS_SMALL, x=0.0, w=12.0):
  m = self.lab(zh, en, size, color).move_to([x, y, 0])
  if m.width > w: m.scale_to_fit_width(w).move_to([x, y, 0])
  return m

 def _txt(self, y, s, color=INK, size=FS_BODY, x=PX):
  m = Text(s, font_size=size, color=color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > RIGHT_EDGE:
   m.scale_to_fit_width(RIGHT_EDGE - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 # ── geometry ──────────────────────────────────────────────────────
 def _arr(self, s, t, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(t) - np.asarray(s))) < 0.05: return VGroup()
  return Arrow(s, t, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _dash(self, a, b, color, n=12, sw=2.5):
  """Fixed dash count: a stretching DashedLine changes its submobject count,
  which breaks FadeIn's one-time family alignment for the whole group."""
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _curve(self, pts, color, sw=3, maxn=180):
  pts = np.asarray(pts, dtype=float)
  if len(pts) > maxn:
   pts = pts[np.linspace(0, len(pts) - 1, maxn).astype(int)]
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(list(pts)); return m

 def _axes(self, o, xl, yl, w=2.25, h=1.45):
  return VGroup(self._arr(o + np.array([-w, 0, 0]), o + np.array([w, 0, 0]), DIM, sw=3, tl=0.14),
                self._arr(o + np.array([0, -h, 0]), o + np.array([0, h, 0]), DIM, sw=3, tl=0.14),
                Text(xl, font_size=FS_SMALL, color=DIM).move_to(o + np.array([w + 0.20, -0.20, 0])),
                Text(yl, font_size=FS_SMALL, color=DIM).move_to(o + np.array([-0.22, h + 0.18, 0])))

 def _tau(self):
  return self.t.get_value() - self.t0

 # ── beat plumbing ─────────────────────────────────────────────────
 def beat(self, i, fin=(), fout=(), extra=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  r = min(0.5, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate(rate_func=linear).increment_value(r), run_time=r)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate(rate_func=linear).increment_value(d), *extra, run_time=d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * (2.35 - 0.22 * max(0, len(s.split(chr(10))) - 2)))

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def stage(self):
  """Return a list of (fin, fout) pairs, one per narration line.

  A third element may be added to any entry: a zero-argument callable run
  just before that beat starts. `stage` is evaluated once, up front, so this
  is the only place a lesson can change something (typically `self.mode`)
  between beats — doing it inline would fire every change immediately.
  """
  raise NotImplementedError

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = self.FORMULAS_SRC[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)
  plan = self.stage()
  active_sub = None; active_f = None
  for i, entry in enumerate(plan):
   fin, fout = entry[0], entry[1]
   if len(entry) > 2 and entry[2] is not None: entry[2]()
   self.t0 = self.t.get_value()
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
  self.wait(.7)


def make(cls, n, prefix="LandauL"):
 """Build the ZH and EN scene classes for lesson n.

 The classes have to claim the lesson's own module. Manim only collects
 scenes whose `__module__` matches the file it was pointed at, and a class
 built by `type()` in here would otherwise carry this module's name, be
 skipped, and leave manim rendering `cls` itself — which silently produces
 one file named after the base class, in the base class's language, for both
 the ZH and the EN run.

 `n` is pasted into the name as given, so a series that wants zero-padded
 scene names passes the string "00" rather than the integer 0. Whatever is
 passed has to match the number handed to `tools/queue.sh`, which builds the
 same name by concatenation (with SCENE_PREFIX set to `prefix`).
 """
 ns = {"__module__": cls.__module__}
 return (type(f"{prefix}{n}ZH", (cls,), dict(ns, LANGUAGE="zh")),
         type(f"{prefix}{n}EN", (cls,), dict(ns, LANGUAGE="en")))
