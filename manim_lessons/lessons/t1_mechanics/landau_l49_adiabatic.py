"""Lesson 49 — Adiabatic invariants (Landau §49).

Two pictures, in the order the argument needs them. First a pendulum whose
string is slowly pulled in: the parameter changes over many periods, so the
energy drifts without being conserved. Then the phase plane, where the same
slow change stretches the ellipse tall and thin while the area it encloses --
the adiabatic invariant -- is printed on screen and does not move.

The pendulum phase is integrated in closed form rather than per frame: with a
linear length ramp, the integral of one over the square root of the length is
elementary, so the swing is reproducible between the -ql preview and -qh.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Polygon, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

PIV = np.array([-3.45, 1.15, 0.0])          # pendulum pivot
L0, L1, TLAM = 1.85, 1.30, 29.0             # string length before, after, ramp seconds
A0 = 0.55                                   # angular amplitude at L0
KP = 5.30                                   # pendulum frequency scale: omega = KP / sqrt(l)

PC = np.array([-3.45, -0.50, 0.0])          # phase-plane origin
AE, BE = 1.62, 0.78                         # ellipse semi-axes on screen at s = 1
SMAX, TRAMP = 0.80, 30.0                    # omega grows to 1 + SMAX over TRAMP seconds
WDOT = 2.05                                 # phase-point angular rate at s = 1
QS = 0.75                                   # where the dq strip sits, as a fraction of AE


class AdiabaticBase(CanonicalBase):
 EPISODE = 49
 MODE_LABEL = {0: {"zh": "慢慢改變的參數 λ", "en": "a slowly varying parameter λ"},
               1: {"zh": "λ 固定就是封閉系統", "en": "with λ fixed the system is closed"},
               2: {"zh": "對一個週期取平均", "en": "average over one period"},
               3: {"zh": "哪一個量保持不變？", "en": "which quantity stays constant?"},
               4: {"zh": "能量的變化率", "en": "the rate of change of the energy"},
               5: {"zh": "把時間積分換成座標積分",
                   "en": "trade the time integral for the coordinate"},
               6: {"zh": "沿著 λ 固定的那條軌道", "en": "along the path at fixed λ"},
               7: {"zh": "環積分除以 2π", "en": "the loop integral over two pi"},
               8: {"zh": "相軌跡圍出來的面積", "en": "the area enclosed by the phase path"},
               9: {"zh": "諧振子：I = E / ω", "en": "the oscillator: I = E over ω"}}

 # ── the slow parameter ────────────────────────────────────────────
 def _x(self, t0):
  return max(0.0, self.t.get_value() - t0)

 def _len(self):
  if not self.lam: return L0
  return L0 - (L0 - L1) * min(1.0, self._x(self.tlam0) / TLAM)

 def _pphase(self):
  """KP times the integral of one over sqrt(l) dt, in closed form."""
  t = self.t.get_value()
  if not self.lam: return KP * (t - self.tpend0) / np.sqrt(L0)
  a = (self.tlam0 - self.tpend0) / np.sqrt(L0)
  x = self._x(self.tlam0); c = (L0 - L1) / TLAM
  xr = min(x, TLAM)
  a += (2.0 / c) * (np.sqrt(L0) - np.sqrt(L0 - c * xr))
  if x > TLAM: a += (x - TLAM) / np.sqrt(L1)
  return KP * a

 def _pend(self):
  l = self._len()
  th = A0 * (L0 / l) ** 0.75 * np.cos(self._pphase())
  b = PIV + np.array([l * np.sin(th), -l * np.cos(th), 0.0])
  return VGroup(Line(PIV, b, color=DIM, stroke_width=3),
                Dot(b, color=ACCENT_A, radius=0.13))

 def _lbar(self):
  x = PIV[0] + 1.55
  return Line([x, PIV[1], 0], [x, PIV[1] - self._len(), 0], color=ACCENT_C, stroke_width=6)

 # ── the phase ellipse ─────────────────────────────────────────────
 def _s(self):
  if not self.ramp: return 1.0
  return 1.0 + SMAX * min(1.0, self._x(self.tr0) / TRAMP)

 def _ab(self):
  s = self._s(); return AE / np.sqrt(s), BE * np.sqrt(s)

 def _phi(self):
  """Angle on the ellipse: WDOT times the integral of s dt, in closed form."""
  if not self.ramp: return WDOT * (self.t.get_value() - self.tdot0)
  a = self.tr0 - self.tdot0
  x = self._x(self.tr0)
  a += x + SMAX * min(x, TRAMP) ** 2 / (2.0 * TRAMP)
  if x > TRAMP: a += SMAX * (x - TRAMP)
  return WDOT * a

 def _pts(self, n=90):
  a, b = self._ab()
  return [PC + np.array([a * np.cos(u), b * np.sin(u), 0.0])
          for u in np.linspace(0, 2 * PI, n)]

 def _ell(self):
  return self._curve(self._pts(), ACCENT_B, sw=3, maxn=200)

 def _fill(self):
  return Polygon(*self._pts(), color=ACCENT_B, stroke_width=0,
                 fill_opacity=0.20, fill_color=ACCENT_B)

 def _pdot(self):
  a, b = self._ab(); u = self._phi()
  return Dot(PC + np.array([a * np.cos(u), b * np.sin(u), 0.0]), color=ACCENT_A, radius=0.10)

 # ── live read-outs, above the picture ─────────────────────────────
 def _area(self):
  a, b = self._ab()
  s = ("面積 / 2π = %.3f（始終不變）" if self.LANGUAGE == "zh"
       else "area / 2π = %.3f (never changes)") % (0.5 * a * b)
  return Text(s, font_size=FS_SMALL, color=WARN).move_to([PC[0], 0.88, 0])

 def _eom(self):
  s = self._s()
  txt = ("ω = %.2f ω₀        E = %.2f E₀" if self.LANGUAGE == "zh"
         else "ω = %.2f ω₀        E = %.2f E₀") % (s, s)
  return Text(txt, font_size=FS_SMALL, color=ACCENT_C).move_to([PC[0], 1.24, 0])

 def stage(self):
  self.lam = False; self.ramp = False
  self.tpend0 = 0.0; self.tlam0 = 0.0; self.tdot0 = 0.0; self.tr0 = 0.0

  pend = always_redraw(lambda: self._pend())
  pivot = Dot(PIV, color=GHOST, radius=0.07)
  plab = self._mid(-1.32, "一個週期 T 很短，λ 幾乎沒動",
                   "one period T is short, and λ hardly moves in it", ACCENT_A, FS_SMALL,
                   x=PIV[0], w=4.6)
  lbar = always_redraw(lambda: self._lbar())
  # The bar shrinks upwards, so its label sits below the longest it ever is.
  llab = Text("λ", font_size=FS_SMALL, color=ACCENT_C).move_to([PIV[0] + 1.55, -0.98, 0])

  ax = self._axes(PC, "q", "p", w=2.15, h=1.15)
  ax[3].move_to(PC + np.array([-0.30, 0.92, 0]))      # p label, clear of the read-outs
  ell = always_redraw(lambda: self._ell())
  fill = always_redraw(lambda: self._fill())
  pdot = always_redraw(lambda: self._pdot())
  # Above the picture: a 4-line English subtitle reaches up to about y = -1.55.
  elab = self._mid(1.24, "相軌跡：λ 固定時是封閉曲線",
                   "the phase path: a closed curve at fixed λ", ACCENT_B, FS_SMALL,
                   x=PC[0], w=5.5)

  xq = PC[0] + QS * AE; hq = BE * np.sqrt(1.0 - QS * QS)
  strip = VGroup(Line([xq, PC[1] - hq, 0], [xq, PC[1] + hq, 0], color=WARN, stroke_width=3),
                 Line([xq + 0.15, PC[1] - hq, 0], [xq + 0.15, PC[1] + hq, 0],
                      color=WARN, stroke_width=3),
                 Text("dq", font_size=FS_SMALL - 2, color=WARN)
                 .move_to([xq + 0.08, PC[1] - hq - 0.24, 0]))
  parr = VGroup(self._arr([xq, PC[1], 0], [xq, PC[1] + hq, 0], ACCENT_A, sw=4, tl=0.14),
                Text("p", font_size=FS_SMALL, color=ACCENT_A)
                .move_to([xq + 0.34, PC[1] + 0.5 * hq, 0]))
  area = always_redraw(lambda: self._area())
  eom = always_redraw(lambda: self._eom())

  c0 = VGroup(self._row(0.95, "一維的有限運動", "a finite motion in one dimension", DIM),
              self._row(0.25, "系統帶著一個參數 λ", "the system carries a parameter λ",
                        ACCENT_C),
              self._row(-0.45, "一個週期裡 λ 只變一點點",
                        "λ barely changes in one period", ACCENT_A))
  c1 = VGroup(self._row(0.95, "λ 固定 → 封閉系統", "λ fixed: a closed system", ACCENT_B),
              self._row(0.25, "能量守恆，運動嚴格週期",
                        "energy conserved, motion strictly periodic", DIM),
              self._row(-0.45, "λ 會變 → 能量不再守恆",
                        "λ varying: the energy is not conserved", WARN))
  c2 = VGroup(self._row(0.95, "但能量變得也很慢", "but the energy changes slowly too", DIM),
              self._row(0.25, "對一個週期取平均", "average over one period", ACCENT_B),
              self._row(-0.45, "抹掉快速的抖動", "smoothing out the fast wobble", DIM),
              self._row(-1.15, "剩下穩定的緩慢漂移", "leaving a steady slow drift", ACCENT_A))
  c3 = VGroup(self._row(0.95, "平均的 E 成了 λ 的函數",
                        "the averaged E is a function of λ", ACCENT_C),
              self._row(0.25, "寫成某個量保持不變",
                        "written as one quantity staying fixed", DIM),
              self._row(-0.45, "這就叫絕熱不變量", "this is the adiabatic invariant", WARN,
                        FS_BODY))
  c4 = VGroup(self._row(0.95, "H 裡顯含 λ", "H contains λ explicitly", ACCENT_C),
              self._row(0.25, "右邊還帶著快變的 q , p",
                        "the fast q and p are still on the right", DIM),
              self._row(-0.45, "所以要對週期平均", "so we average over the period", ACCENT_A))
  c5 = VGroup(self._row(0.95, "dt = dq / ( ∂H/∂p )", "dt = dq / ( ∂H/∂p )", ACCENT_A, FS_BODY),
              self._row(0.25, "時間積分換成座標積分",
                        "the time integral becomes one over q", ACCENT_B),
              self._row(-0.45, "週期就是同一個積分繞一圈",
                        "and the period is that integral once round", DIM))
  c6 = VGroup(self._row(0.95, "沿著軌道 H = E", "along the path H = E", DIM),
              self._row(0.25, "p = p ( q ; E , λ )", "p = p ( q ; E , λ )", ACCENT_A, FS_BODY),
              self._row(-0.45, "對 λ 微分換掉被平均的量",
                        "differentiate by λ to replace it", ACCENT_C))
  c7 = VGroup(self._row(0.95, "分子變成 − ∂p/∂λ", "the numerator becomes − ∂p/∂λ", ACCENT_C),
              self._row(0.25, "分母就是 ∂p/∂E", "the denominator is ∂p/∂E", ACCENT_B),
              self._row(-0.45, "兩者合成一條全微分",
                        "the two make up one total differential", DIM),
              self._row(-1.15, "所以 dI/dt = 0", "so dI/dt = 0", WARN, FS_BODY))
  c8 = VGroup(self._row(0.95, "相空間就是 q , p 的平面",
                        "phase space is the plane of q and p", DIM),
              self._row(0.25, "週期運動畫出封閉曲線",
                        "a periodic motion draws a closed curve", ACCENT_B),
              self._row(-0.45, "I = 圍出的面積 / 2π", "I = the area inside, over two pi",
                        ACCENT_A, FS_BODY),
              self._row(-1.15, "2π ( ∂I/∂E ) = T", "2π ( ∂I/∂E ) = T", WARN))
  c9 = VGroup(self._row(0.95, "反過來 ∂E/∂I = ω", "inversely ∂E/∂I = ω", ACCENT_C, FS_BODY),
              self._row(0.25, "諧振子的相軌跡是橢圓",
                        "the oscillator's phase path is an ellipse", DIM),
              self._row(-0.45, "面積 / 2π = E / ω", "the area over two pi is E / ω", ACCENT_A,
                        FS_BODY),
              self._row(-1.15, "所以 E 和 ω 成正比地變",
                        "so E stays proportional to ω", WARN))

  def start_lam():
   self.lam = True; self.tlam0 = self.t.get_value()

  def start_dot():
   self.tdot0 = self.t.get_value()

  def start_ramp():
   self.ramp = True; self.tr0 = self.t.get_value()

  return [([pivot, pend, plab, c0], []),
          ([c1], [c0]),
          ([lbar, llab, c2], [c1], start_lam),
          ([c3], [c2]),
          ([ax, ell, pdot, elab, c4], [c3, pivot, pend, plab, lbar, llab], start_dot),
          ([strip, parr, c5], [c4]),
          ([c6], [c5]),
          ([fill, c7], [c6, strip, parr]),
          ([area, c8], [c7], start_ramp),
          ([eom, c9], [c8, elab])]


LandauL49ZH, LandauL49EN = make(AdiabaticBase, 49)
