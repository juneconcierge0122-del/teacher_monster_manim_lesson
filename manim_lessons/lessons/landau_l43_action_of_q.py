"""Lesson 43 — The action as a function of the coordinates (Landau §43).

Three pictures. First a fan of true paths sharing one start and ending at
different points, so the action becomes a function of where you end up. Then
the optical picture that (43.3) really means: level curves of S drawn as
wavefronts, with the momenta as rays standing perpendicular to them. Finally a
q-t diagram for the second half: world lines reaching the same place at
different instants, the action accumulating along one of them, and the two
differentials of (43.6) drawn as a step in t and a step in q.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

SRC = np.array([-4.55, -0.85, 0.0])         # the common starting point
ENDS = [np.array([-0.95, 1.15, 0.0]), np.array([-0.75, 0.35, 0.0]),
        np.array([-0.95, -0.45, 0.0]), np.array([-1.35, -1.15, 0.0])]
WC = np.array([-3.30, -0.20, 0.0])          # centre of the wavefront picture

# ── beats 5-9: the q-t diagram ────────────────────────────────────────
QO = np.array([-4.45, -1.30, 0.0])          # origin of the q, t axes
QX = 2.30                                   # the common final coordinate
TS = (1.10, 1.80, 2.45)                     # the three arrival times
BOW = (-0.42, 0.0, 0.52)                    # how much each world line bows
SRUN = 3.4                                  # seconds for the runner to cross


def _bend(a, b, k):
 """A gently curved path from a to b, so the fan reads as different paths."""
 m = 0.5 * (a + b) + k * np.array([-(b - a)[1], (b - a)[0], 0.0]) / max(
  float(np.linalg.norm(b - a)), 1e-6)
 return [(1 - s) ** 2 * a + 2 * (1 - s) * s * m + s ** 2 * b for s in np.linspace(0, 1, 40)]


def _wpt(s, j):
 """A point at parameter s along world line j of the q-t diagram."""
 b = QO + np.array([QX, TS[j], 0.0])
 m = 0.5 * (QO + b) + np.array([BOW[j], 0.0, 0.0])
 return (1 - s) ** 2 * QO + 2 * (1 - s) * s * m + s ** 2 * b


class ActionOfQBase(CanonicalBase):
 EPISODE = 43
 MODE_LABEL = {0: {"zh": "兩個端點都固定", "en": "both endpoints held fixed"},
               1: {"zh": "改讓終點自由跑", "en": "now let the far end move"},
               2: {"zh": "真實路徑讓積分項消失",
                   "en": "on the true path the integral drops out"},
               3: {"zh": "只剩下邊界項", "en": "only the boundary term survives"},
               4: {"zh": "動量就是作用量的梯度",
                   "en": "momentum is the gradient of the action"},
               5: {"zh": "也讓抵達的時刻變動", "en": "now let the arrival time vary too"},
               6: {"zh": "沿著路徑，dS/dt 就是 L",
                   "en": "along the path, dS/dt is just L"},
               7: {"zh": "另一邊用鏈鎖法則展開",
                   "en": "expand the same derivative by the chain rule"},
               8: {"zh": "兩邊比較", "en": "compare the two"},
               9: {"zh": "作用量的全微分", "en": "the total differential of the action"}}

 def stage(self):
  # ── the fan of true paths ──────────────────────────────────────
  start = VGroup(Dot(SRC, color=ACCENT_A, radius=0.11),
                 self.lab("固定的起點", "fixed start", FS_SMALL, ACCENT_A)
                 .move_to(SRC + np.array([0.30, -0.36, 0])))
  one = self._curve(_bend(SRC, ENDS[1], 0.0), ACCENT_B, sw=4)
  onee = VGroup(Dot(ENDS[1], color=ACCENT_B, radius=0.10),
                self.lab("固定的終點", "fixed end", FS_SMALL, ACCENT_B)
                .move_to(ENDS[1] + np.array([0.42, 0.30, 0])))
  fan = VGroup(*[self._curve(_bend(SRC, e, k), ACCENT_C, sw=3)
                 for e, k in zip(ENDS, (0.55, 0.0, -0.35, -0.75))],
               *[Dot(e, color=ACCENT_C, radius=0.085) for e in ENDS])
  slab = self._mid(1.62, "S 變成終點座標的函數", "S becomes a function of the endpoint",
                   ACCENT_C, FS_SMALL, x=-2.85, w=4.4)

  # ── wavefronts and rays ────────────────────────────────────────
  # Squashed to 0.60 and with the fan kept inside ±0.92: at 0.72 and ±1.05 the
  # outermost ray reached y = 1.55 and struck through wlab. Now the highest ray
  # tip is at y = 1.26, well clear of the labels.
  SQ = 0.60

  def _front(a, r=2.25):
   return WC + r * np.array([np.cos(a), SQ * np.sin(a), 0.0])

  fronts = VGroup(*[self._curve([_front(a, r) for a in np.linspace(-1.15, 1.15, 60)],
                                ACCENT_B, sw=3)
                    for r in (0.75, 1.25, 1.75, 2.25)])
  rays = VGroup()
  for a in np.linspace(-0.92, 0.92, 7):
   d = np.array([np.cos(a), SQ * np.sin(a), 0.0])
   d = d / float(np.linalg.norm(d))
   rays.add(self._arr(_front(a), _front(a) + 0.62 * d, WARN, sw=4, tl=0.15))
  wlab = VGroup(self._mid(1.55, "S = 常數 的等值面", "level curves of S", ACCENT_B, FS_SMALL,
                          x=WC[0] - 1.30, w=2.6),
                self._mid(1.55, "p = ∇S，處處垂直", "p = ∇S, everywhere normal", WARN,
                          FS_SMALL, x=WC[0] + 1.55, w=2.9))

  # ── the q-t diagram ────────────────────────────────────────────
  E = QO + np.array([QX, TS[1], 0.0])        # the arrival event we vary
  qtax = VGroup(self._arr(QO, QO + np.array([3.45, 0, 0]), DIM, sw=3, tl=0.14),
                self._arr(QO, QO + np.array([0, 2.80, 0]), DIM, sw=3, tl=0.14),
                Text("q", font_size=FS_SMALL, color=DIM).move_to(QO + np.array([3.40, 0.28, 0])),
                Text("t", font_size=FS_SMALL, color=DIM).move_to(QO + np.array([-0.26, 2.68, 0])),
                Dot(QO, color=ACCENT_A, radius=0.09))
  qline = self._dash(QO + np.array([QX, -0.10, 0]), QO + np.array([QX, 2.62, 0]), GHOST, n=16)
  worlds = VGroup(*[self._curve([_wpt(s, j) for s in np.linspace(0, 1, 44)],
                                ACCENT_A if j == 1 else ACCENT_C, sw=4 if j == 1 else 2.5)
                    for j in range(3)],
                  *[Dot(QO + np.array([QX, t, 0.0]), color=ACCENT_C, radius=0.085)
                    for t in TS])
  qtlab = self._mid(1.62, "同一個位置，不同的抵達時刻",
                    "the same place, reached at different instants", ACCENT_C, FS_SMALL,
                    x=QO[0] + 1.55, w=4.6)
  # the action piling up along the middle world line: dS/dt = L
  runs = lambda: min(1.0, (self._tau() % (SRUN + 1.2)) / SRUN)
  grow = always_redraw(lambda: self._curve(
   [_wpt(s * runs(), 1) for s in np.linspace(0, 1, 44)], ACCENT_B, sw=7))
  runner = always_redraw(lambda: Dot(_wpt(runs(), 1), color=ACCENT_B, radius=0.10))
  slabel = self.lab("S 沿路累積", "S piles up along the way", FS_SMALL, ACCENT_B) \
   .move_to(QO + np.array([1.15, -0.36, 0]))
  # (43.6): a step in t at fixed q, then a step in q at fixed t.
  # The t-step stops short of the next arrival dot, 0.65 further up.
  dtarr = VGroup(self._arr(E, E + np.array([0, 0.46, 0]), WARN, sw=5, tl=0.16),
                 self.lab("− H dt", "− H dt", FS_SMALL, WARN)
                 .move_to(E + np.array([0.58, 0.34, 0])))
  dqarr = VGroup(self._arr(E, E + np.array([0.85, 0, 0]), ACCENT_B, sw=5, tl=0.16),
                 self.lab("+ p dq", "+ p dq", FS_SMALL, ACCENT_B)
                 .move_to(E + np.array([0.46, -0.30, 0])))

  c0 = VGroup(self._row(0.95, "S = ∫ L dt", "S = ∫ L dt", ACCENT_A, FS_BODY),
              self._row(0.25, "端點的位置與時刻都給定",
                        "both ends fixed in place and time", DIM),
              self._row(-0.45, "真實路徑讓 S 最小", "the true path makes S least", ACCENT_B))
  c1 = VGroup(self._row(0.95, "起點不動", "the start does not move", DIM),
              self._row(0.25, "終點可以跑到別的地方",
                        "the far end may go elsewhere", ACCENT_C),
              self._row(-0.45, "只沿著真實路徑計算",
                        "always along the true path", DIM))
  c2 = VGroup(self._row(0.95, "邊界項 + 積分項", "a boundary term and an integral", DIM),
              self._row(0.25, "拉格朗日方程 ⇒ 積分為零",
                        "Lagrange's equations kill the integral", ACCENT_B))
  c3 = VGroup(self._row(0.95, "δq 在起點是零", "δq vanishes at the start", DIM),
              self._row(0.25, "δS = Σ p δq", "δS = Σ p δq", ACCENT_A, FS_BODY))
  c4 = VGroup(self._row(0.95, "∂S/∂qᵢ = pᵢ", "∂S/∂qᵢ = pᵢ", ACCENT_A, FS_BODY),
              self._row(0.25, "等值面就像波前", "the level surfaces are wavefronts", ACCENT_B),
              self._row(-0.45, "動量就像垂直的光線", "the momenta are the rays", WARN))
  c5 = VGroup(self._row(0.95, "位置固定，時刻不同", "same places, different instants", DIM),
              self._row(0.25, "S 也成了時間的函數", "S is a function of t as well", ACCENT_C))
  c6 = VGroup(self._row(0.95, "按定義", "straight from the definition", DIM),
              self._row(0.25, "dS/dt = L", "dS/dt = L", ACCENT_A, FS_BODY))
  c7 = VGroup(self._row(0.95, "S = S ( q , t )", "S = S ( q , t )", DIM, FS_BODY),
              self._row(0.25, "∂S/∂qᵢ 就是 pᵢ", "and ∂S/∂qᵢ is pᵢ", ACCENT_B))
  c8 = VGroup(self._row(0.95, "L − Σ p q̇ = − H", "L − Σ p q̇ = − H", ACCENT_C, FS_BODY),
              self._row(0.25, "∂S/∂t = − H", "∂S/∂t = − H", ACCENT_A, FS_BODY))
  c9 = VGroup(self._row(0.95, "dS = Σ p dq − H dt", "dS = Σ p dq − H dt", ACCENT_A, FS_BODY),
              self._row(0.25, "對座標的梯度 → 動量", "gradient in q gives momentum", ACCENT_B),
              self._row(-0.45, "對時間的導數 → 負能量",
                        "derivative in t gives minus the energy", WARN),
              self._row(-1.15, "下一步就是漢彌頓－雅可比方程",
                        "next comes the Hamilton-Jacobi equation", DIM))

  return [([start, one, onee, c0], []),
          ([fan, slab, c1], [c0, one, onee]),
          ([c2], [c1]),
          ([c3], [c2]),
          ([fronts, rays, wlab, c4], [c3, fan, slab, start]),
          ([qtax, qline, worlds, qtlab, c5], [c4, fronts, rays, wlab]),
          ([grow, runner, slabel, c6], [c5]),
          ([c7], [c6]),
          ([dtarr, c8], [c7]),
          ([dqarr, c9], [c8])]


LandauL43ZH, LandauL43EN = make(ActionOfQBase, 43)
