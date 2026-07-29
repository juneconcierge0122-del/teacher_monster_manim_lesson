"""Lesson 50 — Canonical variables (Landau §50).

One picture carries the whole lesson: a lop-sided closed phase path in (q, p),
and, drawn concentric with it, the dashed circle that encloses exactly the same
area. The point on the path runs round unevenly; the hand on the circle -- the
angle variable -- turns at a constant rate, and the two are locked together.
Every claim in the section is then something visible: the shaded strip is the
abbreviated action accumulating, one turn of the hand is the two-pi increment,
and in the last beats the path deforms with a time-dependent parameter while
the circle, the action variable, stays put.

The reparametrisation theta = w + EPS sin w is imposed rather than derived: the
point of the drawing is only that one angle runs uniformly and the other does
not, which is exactly what the transformation buys.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (DashedVMobject, Dot, Line, Polygon, Text, VGroup, VMobject, always_redraw, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

PC = np.array([-3.45, -0.30, 0.0])
SXO, SYO, R0 = 1.30, 0.95, 1.05             # oval: screen scales and mean radius
E2, E4 = 0.22, 0.10                         # the two shape harmonics, at the start
E2B, E4B = 0.02, -0.06                      # and after the slow parameter has moved
EPS = 0.45                                  # how unevenly the point runs: theta = w + EPS sin w
WDOT = 0.62                                 # angle variable, radians per second
TSW, TARC, TMORPH = 13.0, 11.0, 30.0        # sweep, one-turn arc, and shape-morph seconds
RC = R0 * np.sqrt(SXO * SYO)                # circle of equal area, in screen units


class CanonVarBase(CanonicalBase):
 EPISODE = 50
 MODE_LABEL = {0: {"zh": "把 I 當成新的動量", "en": "take I as the new momentum"},
               1: {"zh": "生成函數是簡略作用量",
                   "en": "the generating function is the abbreviated action"},
               2: {"zh": "第一條正則變換公式", "en": "the first transformation formula"},
               3: {"zh": "第二條給出角變數", "en": "the second gives the angle variable"},
               4: {"zh": "新的哈密頓量就是 E ( I )",
                   "en": "the new Hamiltonian is just E of I"},
               5: {"zh": "角變數隨時間線性增加",
                   "en": "the angle variable grows linearly in time"},
               6: {"zh": "繞一圈：S₀ 加 2π I，w 加 2π",
                   "en": "one turn: S₀ by two pi I, w by two pi"},
               7: {"zh": "單值函數是 w 的週期函數",
                   "en": "a one-valued function is periodic in w"},
               8: {"zh": "如果 λ 隨時間變", "en": "if λ does depend on the time"},
               9: {"zh": "正則變數裡的運動方程",
                   "en": "the equations in canonical variables"}}

 # ── the oval, its area kept fixed while the shape morphs ──────────
 def _e(self):
  if not self.morph: return E2, E4
  u = min(1.0, max(0.0, (self.t.get_value() - self.tm0) / TMORPH))
  return E2 + (E2B - E2) * u, E4 + (E4B - E4) * u

 def _r(self, th):
  e2, e4 = self._e()
  # r0 chosen so that the enclosed area, and hence I, is the same for every shape
  r0 = R0 / np.sqrt(1.0 + 0.5 * e2 * e2 + 0.5 * e4 * e4)
  return r0 * (1.0 + e2 * np.cos(2 * th) + e4 * np.cos(4 * th))

 def _pt(self, th):
  r = self._r(th)
  return PC + np.array([SXO * r * np.cos(th), SYO * r * np.sin(th), 0.0])

 def _oval(self):
  return self._curve([self._pt(u) for u in np.linspace(0, 2 * PI, 120)], ACCENT_B, sw=3,
                     maxn=200)

 # ── the two hands ─────────────────────────────────────────────────
 def _w(self):
  return WDOT * (self.t.get_value() - self.tw0)

 def _th(self):
  w = self._w(); return w + EPS * np.sin(w)

 def _qdot(self):
  return Dot(self._pt(self._th()), color=ACCENT_A, radius=0.11)

 def _hand(self):
  w = self._w()
  e = PC + np.array([RC * np.cos(w), RC * np.sin(w), 0.0])
  return VGroup(Line(PC, e, color=ACCENT_C, stroke_width=4), Dot(e, color=ACCENT_C, radius=0.09))

 # ── the abbreviated action accumulating under the upper branch ────
 def _fill(self):
  """The strip between the q axis and the upper branch, swept from the left."""
  u = 1.0 if not self.sweep else min(1.0, max(0.0, (self.t.get_value() - self.ts0) / TSW))
  th1 = PI * (1.0 - u)
  ths = np.linspace(PI, max(th1, 1e-3), 60)
  pts = [self._pt(t) for t in ths]
  pts.append(PC + np.array([pts[-1][0] - PC[0], 0.0, 0.0]))
  pts.append(PC + np.array([pts[0][0] - PC[0], 0.0, 0.0]))
  return Polygon(*pts, color=ACCENT_A, stroke_width=0, fill_opacity=0.24, fill_color=ACCENT_A)

 def _arc(self):
  """One full turn of the hand, drawn as it happens; fixed point count."""
  u = min(1.0, max(0.0, (self.t.get_value() - self.ta0) / TARC))
  a0 = WDOT * (self.ta0 - self.tw0)
  ths = np.linspace(a0, a0 + 2 * PI * u, 60)
  # Well outside the dashed circle: drawn any closer, this ring reads as the
  # circle itself and the action variable's own curve disappears under it.
  r = RC + 0.24
  m = VMobject(color=WARN, stroke_width=4)
  m.set_points_as_corners([PC + np.array([r * np.cos(t), r * np.sin(t), 0.0]) for t in ths])
  return m

 def stage(self):
  self.sweep = False; self.morph = False
  self.tw0 = 0.0; self.ts0 = 0.0; self.ta0 = 0.0; self.tm0 = 0.0

  ax = self._axes(PC, "q", "p", w=2.15, h=1.30)
  ax[3].move_to(PC + np.array([-0.30, 1.15, 0]))
  oval = always_redraw(lambda: self._oval())
  # Dashed, so it reads as a different object from the solid phase path. Safe to
  # dash here because it is static: nothing redraws it, so its dash count is fixed.
  circ = DashedVMobject(self._curve([PC + np.array([RC * np.cos(u), RC * np.sin(u), 0.0])
                                     for u in np.linspace(0, 2 * PI, 100)], ACCENT_C, sw=3),
                        num_dashes=46, color=ACCENT_C)
  qdot = always_redraw(lambda: self._qdot())
  hand = always_redraw(lambda: self._hand())
  fill = always_redraw(lambda: self._fill())
  arc = always_redraw(lambda: self._arc())
  wlab = Text("w", font_size=FS_SMALL, color=ACCENT_C).move_to(PC + np.array([0.55, 0.34, 0]))

  labq = self._mid(1.22, "( q , p )：走得不均勻", "( q , p ): the run is uneven", ACCENT_B,
                   FS_SMALL, x=-4.95, w=2.60)
  labw = self._mid(1.22, "( w , I )：走得均勻", "( w , I ): perfectly even", ACCENT_C,
                   FS_SMALL, x=-1.95, w=2.60)
  ilab = self._mid(-1.88, "同樣的面積：2π I", "the same area: two pi I", WARN, FS_SMALL,
                   x=PC[0], w=4.6)
  mlab = self._mid(-1.88, "λ ( t )：形狀變了，面積沒變",
                   "λ ( t ): the shape moves, the area does not", WARN, FS_SMALL,
                   x=PC[0], w=5.4)

  c0 = VGroup(self._row(0.95, "先把 λ 固定住", "hold λ fixed for now", DIM),
              self._row(0.25, "系統又是封閉的", "so the system is closed again", DIM),
              self._row(-0.45, "把 I 當成新的「動量」",
                        "take I itself as the new momentum", ACCENT_A))
  c1 = VGroup(self._row(0.95, "S₀ = ∫ p dq", "S₀ = ∫ p dq", ACCENT_A, FS_BODY),
              self._row(0.25, "在給定的 E 與 λ 下算",
                        "computed at a given E and λ", DIM))
  c2 = VGroup(self._row(0.95, "封閉系統裡 I 只是 E 的函數",
                        "for a closed system I is a function of E", DIM),
              self._row(0.25, "所以 S₀ 可以寫成 q 和 I 的函數",
                        "so S₀ can be written through q and I", ACCENT_C),
              self._row(-0.45, "固定 E 微分＝固定 I 微分",
                        "and the two derivatives agree", DIM),
              self._row(-1.15, "p = ∂S₀/∂q", "p = ∂S₀/∂q", ACCENT_A, FS_BODY))
  c3 = VGroup(self._row(0.95, "w = ∂S₀/∂I", "w = ∂S₀/∂I", ACCENT_A, FS_BODY),
              self._row(0.25, "I 叫作用變數", "I is the action variable", ACCENT_B),
              self._row(-0.45, "w 叫角變數", "w is the angle variable", ACCENT_C))
  c4 = VGroup(self._row(0.95, "生成函數不顯含時間",
                        "the generating function has no explicit time", DIM),
              self._row(0.25, "所以 H′ 就是 E ( I )", "so H′ is just E of I", ACCENT_C),
              self._row(-0.45, "dI/dt = 0", "dI/dt = 0", ACCENT_A, FS_BODY),
              self._row(-1.15, "dw/dt = dE/dI", "dw/dt = dE/dI", ACCENT_A, FS_BODY))
  c5 = VGroup(self._row(0.95, "I 是常數，本來就該如此",
                        "I is constant, as it had to be", DIM),
              self._row(0.25, "w = ω t + 常數", "w = ω t + constant", ACCENT_C, FS_BODY),
              self._row(-0.45, "它就是振盪的相位", "it is the phase of the oscillation", WARN))
  c6 = VGroup(self._row(0.95, "S₀ 是 q 的多值函數",
                        "S₀ is many-valued in q", DIM),
              self._row(0.25, "每繞一圈增加 2π I", "each turn adds two pi I", ACCENT_A),
              self._row(-0.45, "所以 w 剛好增加 2π", "so w increases by exactly two pi",
                        WARN, FS_BODY))
  c7 = VGroup(self._row(0.95, "任何單值的 F ( q , p )",
                        "any one-valued F of q and p", DIM),
              self._row(0.25, "w 加 2π 就回到原值", "returns when w gains two pi", ACCENT_B),
              self._row(-0.45, "所以是 w 的週期函數",
                        "so it is a periodic function of w", ACCENT_C))
  c8 = VGroup(self._row(0.95, "現在讓 λ 隨時間變", "now let λ depend on the time", WARN),
              self._row(0.25, "生成函數顯含時間了",
                        "the generating function contains t", DIM),
              self._row(-0.45, "H′ = E ( I ; λ ) + Λ ( dλ/dt )",
                        "H′ = E ( I ; λ ) + Λ ( dλ/dt )", ACCENT_A))
  c9 = VGroup(self._row(0.95, "dI/dt = − ( ∂Λ/∂w ) ( dλ/dt )",
                        "dI/dt = − ( ∂Λ/∂w ) ( dλ/dt )", ACCENT_A),
              self._row(0.25, "dw/dt = ω + 一個小修正",
                        "dw/dt = ω plus a small correction", ACCENT_C),
              self._row(-0.45, "諧振子：q ∝ sin w , p ∝ cos w",
                        "the oscillator: q ∝ sin w , p ∝ cos w", DIM),
              self._row(-1.15, "Λ ∝ sin 2w", "Λ ∝ sin 2w", WARN, FS_BODY))

  def start_sweep():
   self.sweep = True; self.ts0 = self.t.get_value()

  def start_hands():
   self.tw0 = self.t.get_value()

  def start_arc():
   self.ta0 = self.t.get_value()

  def start_morph():
   self.morph = True; self.tm0 = self.t.get_value()

  return [([ax, oval, c0], []),
          ([fill, c1], [c0], start_sweep),
          ([c2], [c1]),
          ([circ, hand, wlab, qdot, labq, labw, ilab, c3], [c2, fill], start_hands),
          ([c4], [c3]),
          ([c5], [c4]),
          ([arc, c6], [c5], start_arc),
          ([c7], [c6]),
          ([mlab, c8], [c7, arc, ilab], start_morph),
          ([c9], [c8])]


LandauL50ZH, LandauL50EN = make(CanonVarBase, 50)
