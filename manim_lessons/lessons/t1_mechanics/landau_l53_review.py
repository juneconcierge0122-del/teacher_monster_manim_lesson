"""Lesson 53 — Mechanics, the whole book (a review episode).

A chain of seven chapter tiles along the bottom lights up one at a time, and
above it a small stage replays the picture that chapter is really about: the
two competing paths of the variational principle, a conserved arrow, an orbit
in an effective potential, a scattering hyperbola, two coupled oscillators, a
spinning body, and a phase-space loop. Every stage is a closed-form curve, so
nothing is integrated and the beats stay cheap.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Rectangle, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

TY = -1.62                                  # chapter tiles: their row
TX0, TDX = -5.92, 0.82                      # first tile centre and pitch
TW, TH = 0.66, 0.46

ST = np.array([-3.45, 0.05, 0.0])           # centre of the little stage above the tiles
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")


class ReviewBase(CanonicalBase):
 EPISODE = 53
 MODE_LABEL = {0: {"zh": "一切從一條原理開始", "en": "it all starts from one principle"},
               1: {"zh": "第一章：運動方程", "en": "chapter I: the equations of motion"},
               2: {"zh": "第二章：守恆定律", "en": "chapter II: conservation laws"},
               3: {"zh": "第三章：把方程積出來",
                   "en": "chapter III: integrating the equations"},
               4: {"zh": "第四章：粒子碰撞", "en": "chapter IV: collisions between particles"},
               5: {"zh": "第五章：小振盪", "en": "chapter V: small oscillations"},
               6: {"zh": "第六章：剛體運動", "en": "chapter VI: motion of a rigid body"},
               7: {"zh": "第七章：正則方程", "en": "chapter VII: the canonical equations"},
               8: {"zh": "第七章：漢彌頓－雅可比",
                   "en": "chapter VII: Hamilton and Jacobi"},
               9: {"zh": "一條原理，一整門力學",
                   "en": "one principle, one whole subject"}}

 def _tau(self):
  return self.t.get_value() - self.ts0

 # ── the seven stages ──────────────────────────────────────────────
 def _s_action(self):
  """Two rival paths between fixed ends; only one makes the action stationary."""
  a = ST + np.array([-1.70, -0.55, 0.0]); b = ST + np.array([1.70, 0.55, 0.0])
  us = np.linspace(0, 1, 60)
  bend = 0.62 * np.sin(1.4 * self._tau())
  true_ = self._curve([a + (b - a) * u + np.array([0, 0.55 * np.sin(PI * u), 0]) for u in us],
                      ACCENT_A, sw=4)
  trial = self._curve([a + (b - a) * u + np.array([0, 0.55 * np.sin(PI * u) + bend
                                                   * np.sin(PI * u), 0]) for u in us],
                      DIM, sw=2.5)
  return VGroup(trial, true_, Dot(a, color=GHOST, radius=0.08), Dot(b, color=GHOST, radius=0.08))

 def _s_lagrange(self):
  """A particle on the stationary path, with its velocity arrow."""
  us = np.linspace(0, 1, 60)
  a = ST + np.array([-1.70, -0.55, 0.0]); b = ST + np.array([1.70, 0.55, 0.0])
  path = self._curve([a + (b - a) * u + np.array([0, 0.55 * np.sin(PI * u), 0]) for u in us],
                     ACCENT_A, sw=4)
  u = 0.5 * (1 + np.sin(0.75 * self._tau() - 0.5 * PI))
  p = a + (b - a) * u + np.array([0, 0.55 * np.sin(PI * u), 0])
  d = (b - a) / 3.4 + np.array([0, 0.55 * PI * np.cos(PI * u) / 3.4, 0])
  return VGroup(path, Dot(p, color=ACCENT_C, radius=0.12),
                self._arr(p, p + 0.75 * d, ACCENT_B, sw=4, tl=0.16))

 def _s_conserve(self):
  """A body turning while its angular momentum arrow stays put."""
  th = 0.9 * self._tau()
  r = 0.95
  arm = VGroup()
  for k in range(3):
   a = th + 2 * PI * k / 3
   arm.add(Line(ST, ST + np.array([r * np.cos(a), 0.62 * r * np.sin(a), 0.0]),
                color=ACCENT_B, stroke_width=4))
   arm.add(Dot(ST + np.array([r * np.cos(a), 0.62 * r * np.sin(a), 0.0]), color=ACCENT_C,
               radius=0.09))
  return VGroup(arm, self._arr(ST, ST + np.array([0, 1.15, 0]), WARN, sw=5, tl=0.18),
                Text("M", font_size=FS_SMALL, color=WARN).move_to(ST + np.array([0.30, 1.10, 0])))

 def _s_orbit(self):
  """A precessing central-field orbit: r oscillating between two turning circles."""
  th = 0.55 * self._tau()
  rr = 1.02 + 0.34 * np.cos(2.6 * th)
  p = ST + np.array([1.45 * rr * np.cos(th) / 1.36, 0.95 * rr * np.sin(th) / 1.36, 0.0])
  us = np.linspace(0, 2 * PI, 90)
  rings = VGroup(self._curve([ST + np.array([1.45 * 1.36 * np.cos(u) / 1.36,
                                             0.95 * 1.36 * np.sin(u) / 1.36, 0.0])
                              for u in us], GHOST, sw=2),
                 self._curve([ST + np.array([1.45 * 0.68 * np.cos(u) / 1.36,
                                             0.95 * 0.68 * np.sin(u) / 1.36, 0.0])
                              for u in us], GHOST, sw=2))
  trail = self._curve([ST + np.array([1.45 * (1.02 + 0.34 * np.cos(2.6 * s)) * np.cos(s) / 1.36,
                                      0.95 * (1.02 + 0.34 * np.cos(2.6 * s)) * np.sin(s) / 1.36,
                                      0.0])
                       for s in np.linspace(max(0.0, th - 7.5), th, 150)], ACCENT_B, sw=3)
  return VGroup(rings, trail, Dot(ST, color=ACCENT_A, radius=0.10),
                Dot(p, color=ACCENT_C, radius=0.10))

 def _s_scatter(self):
  """An elastic collision: one particle in, two out at their fixed angles."""
  o = ST + np.array([-0.15, -0.05, 0.0])
  tc = (0.34 * self._tau()) % 2.0
  if tc < 1.0:
   a = o + np.array([-1.80 * (1.0 - tc), 0.0, 0.0]); b = o
  else:
   u = tc - 1.0
   a = o + u * np.array([1.31, 0.92, 0.0])
   b = o + u * np.array([1.20, -1.20, 0.0])
  return VGroup(self._dash(o + np.array([-1.85, 0, 0]), o + np.array([1.50, 0, 0]), GHOST,
                           n=16),
                Dot(a, color=ACCENT_C, radius=0.15), Dot(b, color=ACCENT_A, radius=0.12),
                Text("θ₁", font_size=FS_SMALL - 2, color=DIM)
                .move_to(o + np.array([0.62, 0.30, 0])),
                Text("θ₂", font_size=FS_SMALL - 2, color=DIM)
                .move_to(o + np.array([0.58, -0.36, 0])))

 def _s_modes(self):
  """Two coupled masses in a normal mode: same frequency, fixed amplitude ratio."""
  y = ST[1] - 0.10
  base = [ST[0] - 0.95, ST[0] + 0.95]
  s = 0.42 * np.sin(2.1 * self._tau())
  xs = [base[0] + s, base[1] - s]
  wall = VGroup(Line([ST[0] - 2.10, y - 0.42, 0], [ST[0] - 2.10, y + 0.42, 0], color=GHOST,
                     stroke_width=4),
                Line([ST[0] + 2.10, y - 0.42, 0], [ST[0] + 2.10, y + 0.42, 0], color=GHOST,
                     stroke_width=4))
  links = VGroup(Line([ST[0] - 2.10, y, 0], [xs[0], y, 0], color=DIM, stroke_width=2),
                 Line([xs[0], y, 0], [xs[1], y, 0], color=ACCENT_A, stroke_width=3),
                 Line([xs[1], y, 0], [ST[0] + 2.10, y, 0], color=DIM, stroke_width=2))
  return VGroup(wall, links, Dot([xs[0], y, 0], color=ACCENT_C, radius=0.15),
                Dot([xs[1], y, 0], color=ACCENT_C, radius=0.15))

 def _s_rigid(self):
  """A body turning about a tilted axis: the axis is fixed, the body is not."""
  th = 1.25 * self._tau()
  ax = np.array([0.42, 1.00, 0.0]); ax = ax / np.linalg.norm(ax)
  per = np.array([-ax[1], ax[0], 0.0])
  g = VGroup(self._arr(ST - 1.05 * ax, ST + 1.15 * ax, WARN, sw=4, tl=0.16))
  for k in range(4):
   a = th + PI * k / 2
   p = ST + 0.92 * np.cos(a) * per + 0.34 * np.sin(a) * ax
   g.add(Line(ST, p, color=ACCENT_B, stroke_width=3))
   g.add(Dot(p, color=ACCENT_C, radius=0.09))
  g.add(Text("Ω", font_size=FS_SMALL, color=WARN).move_to(ST + 1.15 * ax
                                                          + np.array([0.28, 0.06, 0])))
  return g

 def _s_phase(self):
  """A phase-space loop with a cell of states carried round it."""
  th = 0.65 * self._tau()
  us = np.linspace(0, 2 * PI, 90)
  loop = self._curve([ST + np.array([1.55 * np.cos(u), 0.95 * np.sin(u), 0.0]) for u in us],
                     ACCENT_B, sw=3)
  g = VGroup(loop, self._axes(ST, "q", "p", w=1.95, h=1.10))
  for k in range(4):
   a = th + 2 * PI * k / 4
   g.add(Dot(ST + np.array([1.55 * np.cos(a), 0.95 * np.sin(a), 0.0]), color=ACCENT_A,
             radius=0.10))
  return g

 STAGES = ("_s_action", "_s_lagrange", "_s_conserve", "_s_orbit", "_s_scatter", "_s_modes",
           "_s_rigid", "_s_phase")

 def _stage_now(self):
  return getattr(self, self.scene_key)()

 def stage(self):
  self.scene_key = "_s_action"; self.ts0 = 0.0

  def tile(k, color, fill):
   c = np.array([TX0 + k * TDX, TY, 0.0])
   return VGroup(Rectangle(width=TW, height=TH, color=color, stroke_width=2 + fill,
                           fill_opacity=0.22 * fill, fill_color=color).move_to(c),
                 Text(ROMAN[k], font_size=FS_SMALL - 3, color=color).move_to(c))

  # The highlights are built up front, one per chapter, rather than redrawn from
  # the current beat: a redrawn group would change its glyph count as the numeral
  # changes, which is exactly what breaks a FadeIn's family alignment.
  chain = VGroup(*[tile(k, GHOST, 0) for k in range(7)])
  hl = [tile(k, ACCENT_A, 1) for k in range(7)]
  hlall = VGroup(*[tile(k, ACCENT_A, 1) for k in range(7)])
  art = always_redraw(lambda: self._stage_now())

  c0 = VGroup(self._row(0.95, "在所有可能的路徑裡", "among all the possible paths", DIM),
              self._row(0.25, "真實運動讓作用量取極值",
                        "the real motion makes the action stationary", ACCENT_A),
              self._row(-0.45, "S = ∫ L dt", "S = ∫ L dt", WARN, FS_BODY))
  c1 = VGroup(self._row(0.95, "由此得到拉格朗日方程",
                        "this gives Lagrange's equations", ACCENT_A),
              self._row(0.25, "空間均勻、各向同性",
                        "space is homogeneous and isotropic", DIM),
              self._row(-0.45, "時間也均勻", "and time is homogeneous too", DIM),
              self._row(-1.15, "自由粒子的 L 就被定死了",
                        "which fixes L for a free particle", ACCENT_C))
  c2 = VGroup(self._row(0.95, "時間平移 → 能量", "time translation gives energy", ACCENT_A),
              self._row(0.25, "空間平移 → 動量", "space translation gives momentum", ACCENT_B),
              self._row(-0.45, "轉動 → 角動量", "rotation gives angular momentum", ACCENT_C),
              self._row(-1.15, "作用量的形式還決定了縮放",
                        "and the form of S fixes how motions scale", DIM))
  c3 = VGroup(self._row(0.95, "一維運動直接化為求積",
                        "one dimension reduces to quadratures", DIM),
              self._row(0.25, "中心場用有效位能壓成一維",
                        "a central field is squeezed by U_eff", ACCENT_C),
              self._row(-0.45, "克卜勒：橢圓、拋物線、雙曲線",
                        "Kepler: ellipse, parabola, hyperbola", ACCENT_A))
  c4 = VGroup(self._row(0.95, "粒子的衰變", "the disintegration of particles", DIM),
              self._row(0.25, "彈性碰撞的角度關係",
                        "the angles in an elastic collision", ACCENT_B),
              self._row(-0.45, "散射截面與拉塞福公式",
                        "cross-sections and Rutherford's formula", ACCENT_A),
              self._row(-1.15, "只靠守恆律與換參考系",
                        "from conservation laws and a change of frame", DIM))
  c5 = VGroup(self._row(0.95, "位能極小附近都是諧振子",
                        "near a minimum, everything is an oscillator", DIM),
              self._row(0.25, "受迫振盪與共振", "forced motion and resonance", ACCENT_B),
              self._row(-0.45, "多自由度的簡正模態",
                        "normal modes for many degrees of freedom", ACCENT_A),
              self._row(-1.15, "阻尼、參數共振、非線性",
                        "damping, parametric resonance, non-linearity", ACCENT_C))
  c6 = VGroup(self._row(0.95, "角速度與慣性張量",
                        "angular velocity and the inertia tensor", ACCENT_B),
              self._row(0.25, "歐拉方程與歐拉角",
                        "Euler's equations and the Eulerian angles", ACCENT_A),
              self._row(-0.45, "對稱陀螺的進動",
                        "the precession of a symmetrical top", ACCENT_C),
              self._row(-1.15, "非慣性系裡的科氏力與離心力",
                        "Coriolis and centrifugal in a rotating frame", DIM))
  c7 = VGroup(self._row(0.95, "勒讓德變換：速度換成動量",
                        "a Legendre transformation: velocities to momenta", DIM),
              self._row(0.25, "哈密頓方程", "Hamilton's equations", ACCENT_A),
              self._row(-0.45, "帕松括號寫出守恆量的代數",
                        "Poisson brackets: the algebra of the constants", ACCENT_C),
              self._row(-1.15, "相空間體積不變：劉維定理",
                        "phase volume is preserved: Liouville", ACCENT_B))
  c8 = VGroup(self._row(0.95, "作用量當成座標的函數",
                        "the action as a function of the coordinates", DIM),
              self._row(0.25, "漢彌頓－雅可比方程",
                        "gives the Hamilton-Jacobi equation", ACCENT_A),
              self._row(-0.45, "能分離變數就化成一串一維積分",
                        "separation turns it into one-dimensional integrals", ACCENT_C))
  c9 = VGroup(self._row(0.95, "絕熱不變量：面積不變",
                        "adiabatic invariants: the area does not change", ACCENT_B),
              self._row(0.25, "作用變數與角變數",
                        "action variables and angle variables", ACCENT_C),
              self._row(-0.45, "有限運動是條件週期的",
                        "and finite motion is conditionally periodic", ACCENT_A),
              self._row(-1.15, "一條原理，加上時空的對稱",
                        "one principle, plus the symmetries of space and time", WARN))

  def mk(key):
   def go():
    self.scene_key = key; self.ts0 = self.t.get_value()
   return go

  return [([chain, art, c0], [], mk("_s_action")),
          ([hl[0], c1], [c0], mk("_s_lagrange")),
          ([hl[1], c2], [c1, hl[0]], mk("_s_conserve")),
          ([hl[2], c3], [c2, hl[1]], mk("_s_orbit")),
          ([hl[3], c4], [c3, hl[2]], mk("_s_scatter")),
          ([hl[4], c5], [c4, hl[3]], mk("_s_modes")),
          ([hl[5], c6], [c5, hl[4]], mk("_s_rigid")),
          ([hl[6], c7], [c6, hl[5]], mk("_s_phase")),
          ([c8], [c7]),
          ([hlall, c9], [c8, hl[6]])]


LandauL53ZH, LandauL53EN = make(ReviewBase, 53)
