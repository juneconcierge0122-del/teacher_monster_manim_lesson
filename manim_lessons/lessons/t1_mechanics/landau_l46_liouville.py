"""Lesson 46 — Liouville's theorem (Landau §46).

The last three beats are the point of the lesson, so they get a real
computation: a square of initial conditions is carried by the pendulum flow,
its boundary integrated once by RK4 at import time and looked up per frame.
The blob shears, stretches and draws out into a filament while the shoelace
area printed beside it stays put, which is the theorem itself.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Polygon, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

PC = np.array([-3.45, -0.20, 0.0])          # centre of the phase plane
SX, SY = 1.06, 0.72                         # screen units per phase-space unit
NB = 96                                     # points around the blob boundary
NT, DT = 750, 0.016                         # RK4 steps and step size
SPEED = 0.29                                # replayed so the table lasts beats 7-9

# The old and new cells for beats 2-6, drawn as plain quadrilaterals.
OLDQ = ((-0.62, -0.52), (0.62, -0.52), (0.62, 0.52), (-0.62, 0.52))
NEWQ = ((-0.30, -0.72), (0.86, -0.14), (0.30, 0.72), (-0.86, 0.14))


def _deriv(s):
 """Pendulum: q-dot = p, p-dot = -sin q. Non-linear, so the blob really bends."""
 out = np.empty_like(s)
 out[:, 0] = s[:, 1]
 out[:, 1] = -np.sin(s[:, 0])
 return out


def _blob0():
 """A square of initial conditions, sampled around its boundary."""
 a, b, w, h = -0.55, 1.16, 0.62, 0.40
 side = NB // 4
 xs, ys = [], []
 for u in np.linspace(0, 1, side, endpoint=False):
  xs.append(a - w + 2 * w * u); ys.append(b - h)
 for u in np.linspace(0, 1, side, endpoint=False):
  xs.append(a + w); ys.append(b - h + 2 * h * u)
 for u in np.linspace(0, 1, side, endpoint=False):
  xs.append(a + w - 2 * w * u); ys.append(b + h)
 for u in np.linspace(0, 1, side, endpoint=False):
  xs.append(a - w); ys.append(b + h - 2 * h * u)
 return np.stack([np.asarray(xs), np.asarray(ys)], axis=1)


def _integrate():
 """One RK4 pass at import time; the updater only ever indexes this table."""
 s = _blob0()
 out = np.empty((NT, len(s), 2))
 for k in range(NT):
  out[k] = s
  k1 = _deriv(s); k2 = _deriv(s + 0.5 * DT * k1)
  k3 = _deriv(s + 0.5 * DT * k2); k4 = _deriv(s + DT * k3)
  s = s + (DT / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
 return out


TRACK = _integrate()


def _area(pts):
 x, y = pts[:, 0], pts[:, 1]
 return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


AREA0 = _area(TRACK[0])


class LiouvilleBase(CanonicalBase):
 EPISODE = 46
 MODE_LABEL = {0: {"zh": "相空間：座標與動量張成", "en": "phase space: coordinates and momenta"},
               1: {"zh": "體積元 dΓ", "en": "the volume element dΓ"},
               2: {"zh": "正則變換會改變體積嗎？",
                   "en": "does a canonical transformation change it?"},
               3: {"zh": "只要證明雅可比行列式等於一",
                   "en": "it is enough that the Jacobian be one"},
               4: {"zh": "雅可比可以當分數處理",
                   "en": "Jacobians may be handled like fractions"},
               5: {"zh": "用生成函數寫出矩陣元",
                   "en": "the elements through the generating function"},
               6: {"zh": "只差行與列互換，所以相等",
                   "en": "rows and columns interchanged: equal"},
               7: {"zh": "運動本身就是一串正則變換",
                   "en": "the motion is itself a chain of them"},
               8: {"zh": "形狀改變，體積不變", "en": "the shape changes, the volume does not"},
               9: {"zh": "相流像不可壓縮流體", "en": "the phase flow is incompressible"}}

 def _idx(self):
  """Indexed off the flow's own start, not the beat's: `_tau` restarts at every
  beat, which would snap the blob back to its initial square twice."""
  return min(NT - 1, max(0, int(SPEED * (self.t.get_value() - self.tflow0) / DT)))

 def _blob(self):
  pts = TRACK[self._idx()]
  return Polygon(*[PC + np.array([SX * x, SY * y, 0.0]) for x, y in pts],
                 color=ACCENT_B, stroke_width=3, fill_opacity=0.22, fill_color=ACCENT_B)

 def _areatxt(self):
  a = _area(TRACK[self._idx()]) / AREA0
  # Above and to the right: the blob reaches y = -1.58 below, and directly above
  # the origin sits the p axis label.
  return Text(("面積 = %.3f × 原值" if self.LANGUAGE == "zh" else "area = %.3f of the original")
              % a, font_size=FS_SMALL, color=WARN).move_to(PC + np.array([1.80, 1.66, 0]))

 def stage(self):
  self.tflow0 = 0.0
  ax = self._axes(PC, "q", "p", w=2.20, h=1.30)
  # beats 0-1: one phase path with the representative point on it
  orbit = self._curve([PC + np.array([SX * 1.5 * np.cos(a), SY * 1.5 * np.sin(a), 0.0])
                       for a in np.linspace(0, 2 * PI, 120)], GHOST, sw=2.5)
  pdot = always_redraw(lambda: Dot(
   PC + np.array([SX * 1.5 * np.cos(-0.8 * self._tau()),
                  SY * 1.5 * np.sin(-0.8 * self._tau()), 0.0]), color=ACCENT_A, radius=0.10))
  plab = self._mid(1.42, "代表點畫出相軌跡", "the point traces the phase path", ACCENT_A,
                   FS_SMALL, x=PC[0], w=4.4)
  dgam = Polygon(*[PC + np.array([SX * x, SY * y, 0.0])
                   for x, y in ((0.28, 0.30), (0.62, 0.30), (0.62, 0.62), (0.28, 0.62))],
                 color=WARN, stroke_width=3, fill_opacity=0.25, fill_color=WARN)

  # beats 2-6: the old cell and its image, side by side
  cellA = Polygon(*[PC + np.array([SX * (x - 1.05), SY * y, 0.0]) for x, y in OLDQ],
                  color=ACCENT_B, stroke_width=3, fill_opacity=0.18, fill_color=ACCENT_B)
  cellB = Polygon(*[PC + np.array([SX * (x + 1.15), SY * y, 0.0]) for x, y in NEWQ],
                  color=ACCENT_C, stroke_width=3, fill_opacity=0.18, fill_color=ACCENT_C)
  cellarr = self._arr(PC + np.array([SX * (-0.10), 0, 0]), PC + np.array([SX * 0.28, 0, 0]),
                      WARN, sw=4, tl=0.14)
  celllab = VGroup(self._mid(1.42, "( q , p )", "( q , p )", ACCENT_B, FS_SMALL,
                             x=PC[0] - SX * 1.05, w=2.0),
                   self._mid(1.42, "( Q , P )", "( Q , P )", ACCENT_C, FS_SMALL,
                             x=PC[0] + SX * 1.15, w=2.0),
                   self._mid(-1.62, "兩塊區域的面積相等嗎？", "are the two areas equal?",
                             WARN, FS_SMALL, x=PC[0], w=4.8))

  # beats 7-9: the real flow
  blob = always_redraw(lambda: self._blob())
  atxt = always_redraw(lambda: self._areatxt())
  flab = self._mid(-1.88, "每一點都按運動方程走",
                   "every point moves by the equations of motion", ACCENT_B, FS_SMALL,
                   x=PC[0], w=5.2)

  c0 = VGroup(self._row(0.95, "2s 維的空間", "a space of two s dimensions", DIM),
              self._row(0.25, "每一點是一個狀態", "each point is one state", ACCENT_B),
              self._row(-0.45, "運動畫出相軌跡", "the motion traces a phase path", ACCENT_A))
  c1 = VGroup(self._row(0.95, "dΓ = dq … dp …", "dΓ = dq … dp …", ACCENT_A, FS_BODY),
              self._row(0.25, "∫ dΓ 就是區域的體積",
                        "its integral is the volume of a region", DIM))
  c2 = VGroup(self._row(0.95, "換成 P , Q 之後", "after passing to P and Q", DIM),
              self._row(0.25, "體積會不會變？", "does the volume change?", WARN, FS_BODY))
  c3 = VGroup(self._row(0.95, "換變數要乘雅可比",
                        "changing variables brings the Jacobian", DIM),
              self._row(0.25, "所以要證 D = 1", "so we must show D = 1", ACCENT_A, FS_BODY))
  c4 = VGroup(self._row(0.95, "分子分母同除一項", "divide top and bottom alike", DIM),
              self._row(0.25, "化成兩個 s 階行列式的比",
                        "leaving a ratio of two determinants", ACCENT_C))
  c5 = VGroup(self._row(0.95, "分子：∂Qᵢ/∂qₖ", "numerator: ∂Qᵢ/∂qₖ", ACCENT_B),
              self._row(0.25, "分母：∂pᵢ/∂Pₖ", "denominator: ∂pᵢ/∂Pₖ", ACCENT_C),
              self._row(-0.45, "兩者都是 Φ 的二階偏導數",
                        "both are second derivatives of Φ", DIM))
  c6 = VGroup(self._row(0.95, "行列互換不改變行列式",
                        "transposing leaves a determinant alone", ACCENT_A),
              self._row(0.25, "所以 D = 1", "so D = 1", WARN, FS_BODY))
  c7 = VGroup(self._row(0.95, "上一課末尾證過", "shown at the end of the last lesson", DIM),
              self._row(0.25, "生成函數就是負的作用量",
                        "the generating function is minus the action", ACCENT_C))
  c8 = VGroup(self._row(0.95, "區域被拉長、剪切", "the region is stretched and sheared", DIM),
              self._row(0.25, "纏成很細的形狀", "drawn out into fine filaments", ACCENT_C),
              self._row(-0.45, "但體積始終不變", "yet the volume never changes", WARN,
                        FS_BODY),
              self._row(-1.15, "這就是劉維定理", "this is Liouville's theorem", ACCENT_A))
  c9 = VGroup(self._row(0.95, "相流不可壓縮", "the phase flow is incompressible", ACCENT_B),
              self._row(0.25, "二維、四維的積分也不變",
                        "areas and higher integrals are invariant too", DIM),
              self._row(-0.45, "這些叫龐加萊積分不變量",
                        "these are the Poincare invariants", ACCENT_C))

  return [([ax, orbit, pdot, plab, c0], []),
          ([dgam, c1], [c0]),
          ([cellA, cellB, cellarr, celllab, c2], [c1, orbit, pdot, plab, dgam]),
          ([c3], [c2]),
          ([c4], [c3]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([blob, atxt, flab, c7], [c6, cellA, cellB, cellarr, celllab],
           lambda: setattr(self, "tflow0", self.t.get_value())),
          ([c8], [c7]),
          ([c9], [c8])]


LandauL46ZH, LandauL46EN = make(LiouvilleBase, 46)
