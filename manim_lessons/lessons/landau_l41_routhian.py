"""Lesson 41 — The Routhian (Landau §41).

The Routhian is half a Hamiltonian and half a Lagrangian, so the lesson is
built around one split diagram: the q, p pair carried in phase space on the
left, the xi pair carried in configuration space on the right. The payoff is
the cyclic coordinate, shown on the central field the series already knows —
the angle drops out, its momentum freezes into a constant, and what is left is
the one-dimensional radial motion in an effective potential.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Circle, Dot, FadeIn, FadeOut, Line, Rectangle, Text, VGroup, VMobject,
                   DashedVMobject, ValueTracker, always_redraw, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19
PX = 1.55

# ── beats 7-9: a central field, angle cyclic ──────────────────────────
OC = np.array([-3.35, 0.00, 0.0])          # centre of the orbit picture
AA, BB = 1.42, 1.05                         # ellipse semiaxes, in screen units
ORB_W = 0.62                                # how fast the orbit is traced
RC = np.array([2.75, -0.05, 0.0])           # origin of the U_eff picture
RSX, RSY = 0.78, 0.82


def _ueff(r):
 """U + M²/2mr², with the numbers picked so the well sits inside the frame."""
 return -1.55 / max(r, 0.24) + 0.62 / max(r, 0.24) ** 2


class RouthianBase(LandauBatchBase):
 EPISODE = 41; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "只換掉一部分的速度", "en": "replace only some of the velocities"},
               1: {"zh": "一個座標要換，一個保持不變",
                   "en": "one coordinate transformed, one left alone"},
               2: {"zh": "把含速度微分的那一項移過去",
                   "en": "move the velocity differential across"},
               3: {"zh": "勞斯函數", "en": "the Routhian"},
               4: {"zh": "對 q 與 p：哈密頓方程的形式",
                   "en": "for q and p: Hamilton's equations"},
               5: {"zh": "對 ξ：拉格朗日方程的形式",
                   "en": "for xi: Lagrange's equation"},
               6: {"zh": "能量也可以用它寫出來", "en": "the energy, written with it"},
               7: {"zh": "真正的用處：循環座標", "en": "where it earns its keep: cyclic coordinates"},
               8: {"zh": "循環座標的動量是常數",
                   "en": "the momentum of a cyclic coordinate is constant"},
               9: {"zh": "循環座標被完全消掉", "en": "the cyclic coordinate is gone"}}

 # ── helpers ───────────────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _arr(self, s, t, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(t) - np.asarray(s))) < 0.05: return VGroup()
  return Arrow(s, t, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _dash(self, a, b, color, n=12, sw=2.5):
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > 6.30:
   m.scale_to_fit_width(6.30 - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 def _mid(self, y, zh, en, color=DIM, size=FS_SMALL, x=0.0):
  m = self.lab(zh, en, size, color).move_to([x, y, 0])
  if m.width > 12.0: m.scale_to_fit_width(12.0).move_to([x, y, 0])
  return m

 def _curve(self, pts, color, sw=3):
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(list(pts)); return m

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

 def _orbit_pt(self, s):
  return OC + np.array([AA * np.cos(s), BB * np.sin(s), 0.0])

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ beats 0-6: the split diagram ══════════════════════════════════
  LX, RX = -4.75, -1.35
  split = VGroup(
   Line([-3.00, 1.35, 0], [-3.00, -1.30, 0], color=GHOST, stroke_width=2),
   self.lab("換成動量", "traded for p", FS_SMALL, ACCENT_B).move_to([LX + 0.55, 1.15, 0]),
   self.lab("保持速度  v = dξ/dt", "kept: v = dξ/dt", FS_SMALL, ACCENT_A)
   .move_to([RX + 0.60, 1.15, 0]),
   Text("( q , p )", font_size=FS_BODY, color=ACCENT_B).move_to([LX + 0.55, 0.45, 0]),
   Text("( ξ , v )", font_size=FS_BODY, color=ACCENT_A).move_to([RX + 0.60, 0.45, 0]))
  hamil = VGroup(self.lab("像哈密頓量", "acts as a Hamiltonian", FS_SMALL, ACCENT_B)
                 .move_to([LX + 0.55, -0.35, 0]),
                 Text("q̇ = ∂R/∂p", font_size=FS_BODY, color=ACCENT_B)
                 .move_to([LX + 0.55, -0.80, 0]),
                 Text("ṗ = − ∂R/∂q", font_size=FS_BODY, color=ACCENT_B)
                 .move_to([LX + 0.55, -1.25, 0]))
  lagr = VGroup(self.lab("像拉格朗日量", "acts as a Lagrangian", FS_SMALL, ACCENT_A)
                .move_to([RX + 0.60, -0.35, 0]),
                Text("d/dt ( ∂R/∂v ) = ∂R/∂ξ", font_size=FS_BODY, color=ACCENT_A)
                .move_to([RX + 0.60, -0.90, 0]))
  cap0 = VGroup(self._row(0.90, "不必全部換掉", "no need to trade them all", DIM),
                self._row(0.20, "和上一課一樣，只做一半",
                          "the same transformation, half way", ACCENT_C))
  cap1 = VGroup(self._row(0.90, "q 要換，ξ 保持不變", "q is traded, xi stays", DIM),
                self._row(0.20, "全微分共四項", "four terms in the differential", DIM))
  cap2 = VGroup(self._row(0.90, "用 p 與 ṗ 換掉前兩項",
                          "use p and ṗ on the first two", ACCENT_C),
                self._row(0.20, "含 dq̇ 的那一項移過去", "move the dq̇ term across", DIM))
  cap3 = VGroup(self._row(0.90, "R = p q̇ − L", "R = p q̇ − L", ACCENT_A, FS_BODY),
                self._row(0.20, "q̇ 要用 p 表示出來", "with q̇ written in terms of p", DIM))
  cap6 = VGroup(self._row(0.90, "E = R − v ( ∂R/∂v )", "E = R − v ( ∂R/∂v )", ACCENT_C,
                          FS_BODY),
                self._row(0.20, "多個座標時做法完全一樣",
                          "several coordinates work the same way", DIM))

  # ══ beats 7-9: the central field ══════════════════════════════════
  orb = self._curve([self._orbit_pt(s) for s in np.linspace(0, 2 * PI, 140)], GHOST, sw=2.5)
  sun = Dot(OC + np.array([np.sqrt(max(AA ** 2 - BB ** 2, 0.0)), 0.0, 0.0]),
            color=ACCENT_A, radius=0.10)
  pl = always_redraw(lambda: Dot(self._orbit_pt(ORB_W * self._tau()), color=ACCENT_B,
                                 radius=0.10))
  rline = always_redraw(lambda: Line(sun.get_center(), self._orbit_pt(ORB_W * self._tau()),
                                     color=ACCENT_C, stroke_width=3))
  angarc = always_redraw(lambda: self._curve(
   [sun.get_center() + 0.44 * np.array([np.cos(a), np.sin(a), 0.0])
    for a in np.linspace(0.0, float(np.arctan2(
     (self._orbit_pt(ORB_W * self._tau()) - sun.get_center())[1],
     (self._orbit_pt(ORB_W * self._tau()) - sun.get_center())[0])), 24)], WARN, sw=3))
  olab = VGroup(Text("r", font_size=FS_SMALL, color=ACCENT_C)
                .move_to(OC + np.array([-0.30, 0.62, 0])),
                Text("φ", font_size=FS_SMALL, color=WARN)
                .move_to(sun.get_center() + np.array([0.62, 0.20, 0])))
  central = VGroup(orb, sun, rline, angarc, pl, olab)
  cap7 = VGroup(self._row(0.90, "φ 不出現在 L 裡", "φ never appears in L", ACCENT_C, FS_BODY),
                self._row(0.20, "所以也不出現在 R 裡", "so it is absent from R too", DIM),
                self._row(-0.50, "R 只剩 p、r 和 ṙ", "R keeps only p, r and ṙ", ACCENT_B))

  # the effective potential, drawn only from beat 8
  rr = np.linspace(0.30, 3.20, 130)
  uax = VGroup(self._arr(RC + np.array([-0.30, 0, 0]), RC + np.array([2.80, 0, 0]), DIM,
                         sw=3, tl=0.14),
               self._arr(RC + np.array([0, -1.15, 0]), RC + np.array([0, 1.35, 0]), DIM,
                         sw=3, tl=0.14),
               Text("r", font_size=FS_SMALL, color=DIM).move_to(RC + np.array([2.92, -0.20, 0])),
               # beside the axis, not on top of it: ttl8 sits at y = 1.45
               Text("U_eff", font_size=FS_SMALL, color=DIM).move_to(RC + np.array([-0.55, 1.15, 0])))
  ucur = self._curve([RC + np.array([RSX * r, RSY * _ueff(r), 0.0]) for r in rr
                      if abs(RSY * _ueff(r)) < 1.25], ACCENT_A, sw=4)
  rdot = always_redraw(lambda: Dot(
   RC + np.array([RSX * self._rad(), RSY * _ueff(self._rad()), 0.0]), color=ACCENT_B,
   radius=0.09))
  ttl8 = VGroup(self._mid(1.45, "φ 是循環座標，p_φ 守恆", "φ is cyclic, p_φ is conserved",
                          WARN, FS_SMALL, x=OC[0]),
                self._mid(1.45, "只剩一維徑向運動", "one-dimensional radial motion",
                          ACCENT_A, FS_SMALL, x=RC[0]))
  cap8 = self._mid(-1.55, "代進常數值後，剩下的方程只含 r",
                   "with that constant put in, only r is left", ACCENT_B, FS_BODY)
  cap9 = self._mid(-1.55, "解出 r(t)，再積分就得到 φ(t)",
                   "solve for r ( t ), then integrate to get φ ( t )", ACCENT_C, FS_BODY)

  # ── run ───────────────────────────────────────────────────────────
  active_sub = None; active_f = None

  def run(i, fin=(), fout=()):
   nonlocal active_sub, active_f
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

  run(0, fin=[split, cap0])
  run(1, fin=[cap1], fout=[cap0])
  run(2, fin=[cap2], fout=[cap1])
  run(3, fin=[cap3], fout=[cap2])
  run(4, fin=[hamil], fout=[cap3])
  run(5, fin=[lagr])
  run(6, fin=[cap6])
  run(7, fin=[central, cap7], fout=[split, hamil, lagr, cap6])
  run(8, fin=[uax, ucur, rdot, ttl8, cap8], fout=[cap7])
  run(9, fin=[cap9], fout=[cap8])
  self.wait(.7)

 def _rad(self):
  """Distance from the focus, so the dot on U_eff tracks the real orbit."""
  p = self._orbit_pt(ORB_W * self._tau())
  f = OC + np.array([np.sqrt(max(AA ** 2 - BB ** 2, 0.0)), 0.0, 0.0])
  return float(np.clip(np.linalg.norm(p - f), 0.42, 3.10))


def _mk(lang):
 return type(f"LandauL41{'ZH' if lang == 'zh' else 'EN'}", (RouthianBase,), {"LANGUAGE": lang})


LandauL41ZH = _mk("zh")
LandauL41EN = _mk("en")
