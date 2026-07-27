"""Lesson 44 — Maupertuis' principle (Landau §44).

Two pictures. First a bundle of paths between two fixed points, with beads
marking equal time intervals along the true one: beat 1 drops the beads, which
is exactly what the principle drops. Then the payoff of (44.10) — a particle
crossing into a region of lower energy bends like a ray of light, because the
square root of E minus U plays the part of a refractive index.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Line, Polygon, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

A = np.array([-5.05, -0.95, 0.0])           # the fixed start
B = np.array([-1.15, 0.95, 0.0])            # the fixed end
BOWS = (0.72, 0.0, -0.55, -1.05)            # how much each trial path bows
NBEAD = 9                                   # beads marking equal time steps

# beat 9: the refracting boundary
RC = np.array([-3.40, 0.0, 0.0])            # centre of the two-region picture
RW, RH = 2.35, 1.22                         # half width, half height of a slab
# Angles to the normal. The upper slab has the higher U, so the smaller index
# √(E − U); crossing into the lower slab the index rises and the path must bend
# TOWARDS the normal, so the second angle has to be the smaller one.
TH1, TH2 = 0.85, 0.55


def _path(s, k):
 """Point at parameter s along the trial path that bows by k."""
 m = 0.5 * (A + B) + k * np.array([-(B - A)[1], (B - A)[0], 0.0]) / float(
  np.linalg.norm(B - A))
 return (1 - s) ** 2 * A + 2 * (1 - s) * s * m + s ** 2 * B


class MaupertuisBase(CanonicalBase):
 EPISODE = 44
 MODE_LABEL = {0: {"zh": "完整的運動：路徑加上時刻",
                   "en": "the whole motion: the path and the timing"},
               1: {"zh": "只想知道路徑的形狀", "en": "we want only the shape of the path"},
               2: {"zh": "讓抵達的時刻可以變動", "en": "let the final time vary"},
               3: {"zh": "只比較能量相同的運動", "en": "compare only paths of equal energy"},
               4: {"zh": "兩項抵消，只剩簡略作用量",
                   "en": "the terms cancel, leaving the abbreviated action"},
               5: {"zh": "簡略作用量取極小", "en": "the abbreviated action is least"},
               6: {"zh": "把動量用座標與其微分表示",
                   "en": "the momenta through q and dq"},
               7: {"zh": "動能減位能的情形", "en": "for kinetic minus potential energy"},
               8: {"zh": "單個質點：雅可比形式", "en": "one particle: Jacobi's form"},
               9: {"zh": "√(E − U) 就是折射率", "en": "the square root of E minus U is an index"}}

 def _bead(self, j):
  """A bead sliding along the true path, so beat 0 shows the timing too."""
  u = (self._tau() * 0.22 + j / NBEAD) % 1.0
  return Dot(_path(u, 0.0), color=ACCENT_B, radius=0.055)

 def stage(self):
  ends = VGroup(Dot(A, color=ACCENT_A, radius=0.11), Dot(B, color=ACCENT_A, radius=0.11),
                self.lab("起點", "start", FS_SMALL, ACCENT_A)
                .move_to(A + np.array([0.05, -0.36, 0])),
                self.lab("終點", "end", FS_SMALL, ACCENT_A)
                .move_to(B + np.array([0.34, 0.30, 0])))
  trials = VGroup(*[self._curve([_path(s, k) for s in np.linspace(0, 1, 44)], GHOST, sw=2.5)
                    for k in BOWS if k != 0.0])
  true = self._curve([_path(s, 0.0) for s in np.linspace(0, 1, 44)], ACCENT_B, sw=5)
  beads = VGroup(*[always_redraw(lambda j=j: self._bead(j)) for j in range(NBEAD)])
  tlab = self._mid(1.62, "等時間間隔的珠子標出「何時走到哪裡」",
                   "beads at equal time intervals mark the timing", ACCENT_B, FS_SMALL,
                   x=-3.10, w=5.2)
  elab = self._mid(-1.66, "所有比較的路徑能量都等於 E",
                   "every path compared carries the same energy E", WARN, FS_SMALL,
                   x=-3.10, w=5.2)

  # ── beat 9: the refracting boundary ────────────────────────────
  top = Polygon(RC + np.array([-RW, 0, 0]), RC + np.array([RW, 0, 0]),
                RC + np.array([RW, RH, 0]), RC + np.array([-RW, RH, 0]),
                color=GHOST, stroke_width=2, fill_opacity=0.16, fill_color=ACCENT_C)
  bot = Polygon(RC + np.array([-RW, -RH, 0]), RC + np.array([RW, -RH, 0]),
                RC + np.array([RW, 0, 0]), RC + np.array([-RW, 0, 0]),
                color=GHOST, stroke_width=2, fill_opacity=0.05, fill_color=DIM)
  hit = RC + np.array([0.55, 0.0, 0.0])
  # Down and to the right from the upper-left corner of the top slab: the
  # incident ray has to travel through the high-U region to reach the boundary.
  inc = Line(hit + RH / np.cos(TH1) * np.array([-np.sin(TH1), np.cos(TH1), 0]), hit,
             color=ACCENT_B, stroke_width=5)
  out = Line(hit, hit + RH / np.cos(TH2) * np.array([np.sin(TH2), -np.cos(TH2), 0]),
             color=WARN, stroke_width=5)
  norm = self._dash(hit + np.array([0, RH * 0.85, 0]), hit + np.array([0, -RH * 0.85, 0]),
                    GHOST, n=11)
  # Kept to the left of the strike point, and narrow, so neither ray crosses them.
  rlab = VGroup(self._mid(RC[1] + RH * 0.55, "U 較大，折射率較小",
                          "larger U, smaller index", ACCENT_B, FS_SMALL,
                          x=RC[0] - 1.55, w=1.9),
                self._mid(RC[1] - RH * 0.55, "U 較小，折射率較大",
                          "smaller U, larger index", WARN, FS_SMALL,
                          x=RC[0] - 1.55, w=1.9),
                self._mid(1.62, "路徑在交界上折射，就像光線",
                          "the path refracts at the boundary, exactly like light",
                          ACCENT_C, FS_SMALL, x=RC[0], w=5.4))
  refract = VGroup(top, bot, norm, inc, out, rlab)

  c0 = VGroup(self._row(0.95, "解出運動方程", "solve the equations of motion", DIM),
              self._row(0.25, "得到路徑的形狀", "and the shape of the path follows", ACCENT_B),
              self._row(-0.45, "也得到什麼時刻走到哪裡",
                        "and the timing along it as well", ACCENT_C))
  c1 = VGroup(self._row(0.95, "比較簡單的問題", "a more restricted question", DIM),
              self._row(0.25, "只問路徑，不問時間", "the path, with no reference to time",
                        ACCENT_B, FS_BODY))
  c2 = VGroup(self._row(0.95, "L 不顯含時間", "L has no explicit time", DIM),
              self._row(0.25, "所以能量守恆", "so the energy is conserved", ACCENT_A),
              self._row(-0.45, "端點位置固定，時刻可變",
                        "ends fixed in place, free in time", ACCENT_C))
  c3 = VGroup(self._row(0.95, "H 換成常數 E", "replace H by the constant E", DIM),
              self._row(0.25, "δS + E δt = 0", "δS + E δt = 0", ACCENT_A, FS_BODY))
  c4 = VGroup(self._row(0.95, "S = S₀ − E t", "S = S₀ − E t", ACCENT_A, FS_BODY),
              self._row(0.25, "E δt 兩項抵消", "the two E δt terms cancel", DIM),
              self._row(-0.45, "δS₀ = 0", "δS₀ = 0", WARN, FS_BODY))
  c5 = VGroup(self._row(0.95, "S₀ = ∫ Σ p dq", "S₀ = ∫ Σ p dq", ACCENT_A, FS_BODY),
              self._row(0.25, "能量守恆的路徑之中", "among energy-conserving paths", DIM),
              self._row(-0.45, "不論何時抵達終點", "whenever they reach the end", DIM),
              self._row(-1.15, "真實的那一條讓 S₀ 最小",
                        "the true one makes S₀ least", ACCENT_B))
  c6 = VGroup(self._row(0.95, "用動量的定義", "use the definition of momentum", DIM),
              self._row(0.25, "再用能量守恆消掉 dt",
                        "and conservation of energy to remove dt", ACCENT_C))
  c7 = VGroup(self._row(0.95, "L = T − U", "L = T − U", ACCENT_A, FS_BODY),
              self._row(0.25, "E 只是一個參數", "E enters only as a parameter", DIM))
  c8 = VGroup(self._row(0.95, "T = ½ m ( dl/dt )²", "T = ½ m ( dl/dt )²", ACCENT_A, FS_BODY),
              self._row(0.25, "沿著路徑長度積分", "integrated along the path length", DIM),
              self._row(-0.45, "這個形式是雅可比給的", "this form is due to Jacobi", ACCENT_C))
  c9 = VGroup(self._row(0.95, "U = 0：走直線", "U = 0: a straight line", ACCENT_B, FS_BODY),
              self._row(0.25, "有位能時路徑會彎", "with a potential the path bends", WARN),
              self._row(-0.45, "√(E − U) 扮演折射率",
                        "√(E − U) plays the part of an index", ACCENT_A),
              self._row(-1.15, "力學與幾何光學完全平行",
                        "mechanics and ray optics run parallel", DIM))

  return [([ends, true, beads, tlab, c0], []),
          ([trials, c1], [c0, beads, tlab]),
          ([elab, c2], [c1]),
          ([c3], [c2]),
          ([c4], [c3]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([c7], [c6]),
          ([c8], [c7]),
          ([refract, c9], [c8, ends, true, trials, elab])]


LandauL44ZH, LandauL44EN = make(MaupertuisBase, 44)
