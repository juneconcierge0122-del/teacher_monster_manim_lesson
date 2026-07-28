"""Lesson 51 — Accuracy of conservation of the adiabatic invariant (Landau §51).

Four pictures, one per stage of the argument. First Λ as a periodic function of
the angle variable, with the two ends of a period pinned at the same height --
which is the whole reason the mean of its derivative vanishes. Then the ramp of
the parameter, with the action variable wobbling under it and coming back to
almost, but not exactly, the same level. Then the complex angle plane of
Fig. 56: the contour lifted off the real axis and caught in loops round the
singularities, with the imaginary part of the nearest one measured. Finally the
size of the drift for three different ramp speeds, which is the answer.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Line, Rectangle, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

AO = np.array([-3.45, -0.30, 0.0])          # Lambda(w) plot origin
AW, AH = 2.30, 0.95                         # its half width and height
WSPAN = 4.4 * PI                            # how much of w is on screen: just over two periods
LDOT = 1.05                                 # w per second for the dot on that curve

BO1 = np.array([-3.45, 0.62, 0.0])          # lambda(t) plot origin
BO2 = np.array([-3.45, -1.05, 0.0])         # I(t) plot origin
BW, BH = 2.10, 0.42
TB = 26.0                                   # seconds for the ramp to play out

CO = np.array([-3.45, -0.55, 0.0])          # complex w-plane origin
CW, CH = 2.30, 1.45
POLES = ((-0.55, 0.62), (0.95, 0.40), (1.95, 1.05))   # in plot units; second is nearest

DO = np.array([-3.45, -1.35, 0.0])          # bar chart baseline
RATIOS = (2.0, 5.0, 9.0)


def _lam(w):
 return 0.62 * np.cos(w) + 0.22 * np.cos(2 * w)


class AccuracyBase(CanonicalBase):
 EPISODE = 51
 MODE_LABEL = {0: {"zh": "同一條方程的另一個用法",
                   "en": "the same equation used again"},
               1: {"zh": "Λ 是單值的，所以是週期的",
                   "en": "Λ is single-valued, hence periodic"},
               2: {"zh": "週期函數導數的平均是零",
                   "en": "a periodic derivative averages to zero"},
               3: {"zh": "整段過程總共變了多少？",
                   "en": "how much does it change in all?"},
               4: {"zh": "展成傅立葉級數", "en": "expand it in a Fourier series"},
               5: {"zh": "把積分變數換成 w", "en": "change the variable to w"},
               6: {"zh": "把 w 當成複變數", "en": "treat w as a complex variable"},
               7: {"zh": "離實軸最近的那個奇點",
                   "en": "the singularity nearest the real axis"},
               8: {"zh": "這個指數非常大", "en": "and that exponent is large"},
               9: {"zh": "越慢，漂移越指數式地小",
                   "en": "slower means exponentially smaller"}}

 # ── picture A: Lambda as a function of the angle variable ─────────
 def _acurve(self):
  ws = np.linspace(-0.5 * WSPAN, 0.5 * WSPAN, 160)
  return self._curve([AO + np.array([AW * w / (0.5 * WSPAN), AH * _lam(w), 0.0]) for w in ws],
                     ACCENT_B, sw=3)

 def _apt(self, w):
  return AO + np.array([AW * w / (0.5 * WSPAN), AH * _lam(w), 0.0])

 def _adot(self):
  w = -0.5 * WSPAN + (LDOT * (self.t.get_value() - self.ta0)) % WSPAN
  return Dot(self._apt(w), color=ACCENT_A, radius=0.10)

 # ── picture B: the ramp, and the action variable under it ─────────
 def _u(self):
  return min(1.0, max(0.0, (self.t.get_value() - self.tb0) / TB))

 def _bx(self, s):
  return BW * (2.0 * s - 1.0)

 def _lamt(self, s):
  return np.tanh(3.4 * (2.0 * s - 1.0))

 def _it(self, s):
  """Wobbling all the way, and left a hair higher than it started."""
  return 0.16 * np.sin(19.0 * s) * (1.0 - self._lamt(s) ** 2) + 0.30 * (self._lamt(s) + 1.0) / 2

 def _bramp(self, o, f, color, sw=3):
  u = self._u()
  n = max(2, int(4 + 150 * u))
  ss = np.linspace(0.0, u, n)
  return self._curve([o + np.array([self._bx(s), BH * f(s), 0.0]) for s in ss], color, sw=sw)

 # ── picture C: the contour in the complex angle plane ─────────────
 def _cpt(self, x, y):
  return CO + np.array([CW * x / 2.4, CH * y / 1.7, 0.0])

 def _contour(self):
  """The real axis pushed up so that it just clears each singularity."""
  xs = np.linspace(-2.35, 2.35, 200)
  ys = np.zeros_like(xs)
  for px, py in POLES:
   ys += (py + 0.16) * np.exp(-((xs - px) / 0.42) ** 2)
  return self._curve([self._cpt(x, y) for x, y in zip(xs, ys)], ACCENT_A, sw=4)

 def _loop(self, px, py, r=0.26):
  return self._curve([self._cpt(px + r * np.cos(a), py + r * np.sin(a))
                      for a in np.linspace(0, 2 * PI, 60)], ACCENT_A, sw=3)

 def _cross(self, px, py, color=WARN, s=0.11):
  c = self._cpt(px, py)
  return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=4),
                Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=4))

 def stage(self):
  self.ta0 = 0.0; self.tb0 = 0.0

  # A
  aax = self._axes(AO, "w", "Λ", w=AW + 0.20, h=AH + 0.30)
  acur = self._acurve()
  adot = always_redraw(lambda: self._adot())
  per = VGroup(self._dash(self._apt(-PI) + np.array([0, -0.55, 0]),
                          self._apt(-PI) + np.array([0, 0.30, 0]), DIM, n=6),
               self._dash(self._apt(PI) + np.array([0, -0.55, 0]),
                          self._apt(PI) + np.array([0, 0.30, 0]), DIM, n=6),
               Dot(self._apt(-PI), color=WARN, radius=0.09),
               Dot(self._apt(PI), color=WARN, radius=0.09),
               self._arr(self._apt(-PI) + np.array([0, -0.50, 0]),
                         self._apt(PI) + np.array([0, -0.50, 0]), WARN, sw=3, tl=0.13))
  alab = self._mid(-1.80, "一個週期的兩端等高，所以總變化是零",
                   "the two ends of a period sit level, so the total change is zero",
                   WARN, FS_SMALL, x=AO[0], w=5.6)

  # B
  bax1 = self._axes(BO1, "t", "λ", w=BW + 0.20, h=BH + 0.24)
  bax2 = self._axes(BO2, "t", "I", w=BW + 0.20, h=BH + 0.24)
  bl = always_redraw(lambda: self._bramp(BO1, self._lamt, ACCENT_C))
  bi = always_redraw(lambda: self._bramp(BO2, self._it, ACCENT_B))
  bends = VGroup(self._dash(BO1 + np.array([-BW, -BH, 0]), BO1 + np.array([BW, -BH, 0]),
                            GHOST, n=16),
                 self._dash(BO1 + np.array([-BW, BH, 0]), BO1 + np.array([BW, BH, 0]),
                            GHOST, n=16),
                 self._mid(BO1[1] - BH - 0.24, "λ₋", "λ₋", DIM, FS_SMALL - 2,
                           x=BO1[0] - BW - 0.05, w=0.9),
                 self._mid(BO1[1] + BH + 0.24, "λ₊", "λ₊", DIM, FS_SMALL - 2,
                           x=BO1[0] + BW + 0.05, w=0.9))
  # The step the I curve ends on, called out where it actually happens.
  i0 = BO2 + np.array([0, BH * self._it(0.0), 0])
  i1 = BO2 + np.array([0, BH * self._it(1.0), 0])
  distep = VGroup(self._dash(i0 + np.array([-BW, 0, 0]), i0 + np.array([BW + 0.30, 0, 0]),
                             GHOST, n=18),
                  self._arr([BO2[0] + BW + 0.14, i0[1], 0], [BO2[0] + BW + 0.14, i1[1], 0],
                            WARN, sw=4, tl=0.12),
                  Text("ΔI", font_size=FS_SMALL - 2, color=WARN)
                  .move_to([BO2[0] + BW + 0.52, i1[1] + 0.24, 0]))
  dilab = self._mid(-1.80, "ΔI 小得不成比例", "ΔI comes out disproportionately small",
                    WARN, FS_SMALL, x=BO2[0], w=5.2)

  # C
  cax = VGroup(self._arr(CO + np.array([-CW - 0.15, 0, 0]), CO + np.array([CW + 0.15, 0, 0]),
                         DIM, sw=3, tl=0.14),
               self._arr(CO, CO + np.array([0, CH + 0.15, 0]), DIM, sw=3, tl=0.14),
               Text("re w", font_size=FS_SMALL - 2, color=DIM)
               .move_to(CO + np.array([CW + 0.05, -0.26, 0])),
               Text("im w", font_size=FS_SMALL - 2, color=DIM)
               .move_to(CO + np.array([-0.52, CH + 0.10, 0])))
  cont = self._contour()
  loops = VGroup(*[self._loop(px, py) for px, py in POLES])
  near = POLES[1]
  # Only the nearest singularity is picked out in the warning colour, so the
  # w₀ label beside it cannot be read as belonging to one of the others.
  crosses = VGroup(*[self._cross(px, py, WARN if (px, py) == near else DIM)
                     for px, py in POLES])
  imarr = VGroup(self._arr(self._cpt(near[0] + 0.62, 0.0),
                           self._cpt(near[0] + 0.62, near[1]), WARN, sw=4, tl=0.15),
                 self._dash(self._cpt(*near), self._cpt(near[0] + 0.62, near[1]), WARN, n=5),
                 Text("im w₀", font_size=FS_SMALL - 2, color=WARN)
                 .move_to(self._cpt(near[0] + 1.32, 0.5 * near[1])))
  w0lab = Text("w₀", font_size=FS_SMALL, color=WARN).move_to(
   self._cpt(near[0] - 0.60, near[1] + 0.26))

  # D
  bars = VGroup()
  for k, rt in enumerate(RATIOS):
   h = 1.75 * np.exp(-rt / 3.0)
   x = DO[0] - 1.55 + 1.55 * k
   bars.add(Rectangle(width=0.62, height=max(h, 0.03), color=ACCENT_A, stroke_width=2,
                      fill_opacity=0.35, fill_color=ACCENT_A)
            .move_to([x, DO[1] + 0.5 * max(h, 0.03), 0]))
   bars.add(Text("τ / T = %d" % int(rt), font_size=FS_SMALL - 3, color=DIM)
            .move_to([x, DO[1] - 0.26, 0]))
  bline = Line(DO + np.array([-2.30, 0, 0]), DO + np.array([2.30, 0, 0]), color=GHOST,
               stroke_width=2)
  dlab = VGroup(self._mid(1.10, "ΔI 隨 τ / T 指數式地縮小",
                          "ΔI shrinks exponentially with τ / T", ACCENT_A, FS_SMALL,
                          x=DO[0], w=5.2))

  c0 = VGroup(self._row(0.95, "上一課最後那條方程",
                        "the last equation of the previous lesson", DIM),
              self._row(0.25, "可以再證一次絕熱不變性",
                        "proves the invariance a second time", ACCENT_A),
              self._row(-0.45, "順便告訴我們它有多準",
                        "and tells us how accurate it is", ACCENT_C))
  c1 = VGroup(self._row(0.95, "S₀ 對 q 不是單值的", "S₀ is not single-valued in q", DIM),
              self._row(0.25, "但 Λ 是：微分在固定 I 下做",
                        "but Λ is: the derivative is at fixed I", ACCENT_C),
              self._row(-0.45, "多值的增量剛好消掉",
                        "and the many-valued increments cancel", DIM),
              self._row(-1.15, "所以 Λ 是 w 的週期函數",
                        "so Λ is periodic in w", ACCENT_B))
  c2 = VGroup(self._row(0.95, "週期函數的導數", "the derivative of a periodic function", DIM),
              self._row(0.25, "對一個週期平均一定是零",
                        "averages to zero over a period", ACCENT_A),
              self._row(-0.45, "所以 ⟨ dI/dt ⟩ = 0", "so the mean of dI/dt is zero", WARN,
                        FS_BODY))
  c3 = VGroup(self._row(0.95, "設 λ 兩端都趨於定值",
                        "let λ tend to constants at both ends", DIM),
              self._row(0.25, "給定一開始的 I₋", "with I₋ given at the start", ACCENT_C),
              self._row(-0.45, "問最後總共差了多少",
                        "ask what the total difference is", ACCENT_A))
  c4 = VGroup(self._row(0.95, "ΔI 是對全部時間的積分",
                        "ΔI is an integral over all time", DIM),
              self._row(0.25, "Λ 在 w 上是週期的", "Λ is periodic in w", ACCENT_B),
              self._row(-0.45, "所以先展成傅立葉級數",
                        "so expand it in a Fourier series first", ACCENT_C))
  c5 = VGroup(self._row(0.95, "λ 變得夠慢時", "when λ varies slowly enough", DIM),
              self._row(0.25, "w 隨時間單調增加",
                        "w increases monotonically with t", ACCENT_A),
              self._row(-0.45, "積分變數可以換成 w",
                        "so the variable may be changed to w", ACCENT_C),
              self._row(-1.15, "上下限不變", "and the limits are unaltered", DIM))
  c6 = VGroup(self._row(0.95, "假設實軸上沒有奇點",
                        "assume no singularity on the real axis", DIM),
              self._row(0.25, "把路徑推到上半平面",
                        "push the contour into the upper half-plane", ACCENT_A),
              self._row(-0.45, "路徑被奇點勾住成一個個圈",
                        "and it is caught in loops round them", ACCENT_C))
  c7 = VGroup(self._row(0.95, "主要貢獻來自最近的那個",
                        "the nearest one gives the main term", DIM),
              self._row(0.25, "每一項都帶指數因子",
                        "every term carries an exponential factor", ACCENT_C),
              self._row(-0.45, "只留衰減最慢的一項",
                        "keep only the slowest-decaying one", DIM),
              self._row(-1.15, "ΔI ~ exp ( − im w₀ )", "ΔI ~ exp ( − im w₀ )", WARN, FS_BODY))
  c8 = VGroup(self._row(0.95, "t₀ 的量級就是特徵時間 τ",
                        "t₀ is of the order of the time τ", DIM),
              self._row(0.25, "im w₀ ~ ω τ ~ τ / T", "im w₀ ~ ω τ ~ τ / T", ACCENT_A, FS_BODY),
              self._row(-0.45, "而 τ 遠大於週期 T", "and τ is far longer than T", ACCENT_C))
  c9 = VGroup(self._row(0.95, "參數變得越慢", "the more slowly the parameter moves", DIM),
              self._row(0.25, "ΔI 就指數式地變小",
                        "the more exponentially small ΔI is", WARN, FS_BODY),
              self._row(-0.45, "最低階：dw/dt = ω ( I , λ )",
                        "to leading order: dw/dt = ω ( I , λ )", ACCENT_A),
              self._row(-1.15, "奇點來自 Λ ( t ) 與 1/ω ( t )",
                        "the singularities come from Λ and 1/ω", ACCENT_C))

  def start_a():
   self.ta0 = self.t.get_value()

  def start_b():
   self.tb0 = self.t.get_value()

  A = VGroup(aax, acur, adot, per, alab)
  B = VGroup(bax1, bax2, bl, bi, bends, dilab)
  C = VGroup(cax, cont, loops, crosses)

  return [([aax, acur, adot, c0], [], start_a),
          ([per, c1], [c0]),
          ([alab, c2], [c1]),
          ([bax1, bax2, bl, bi, bends, c3],
           [c2, aax, acur, adot, per, alab], start_b),
          ([c4], [c3]),
          ([distep, dilab, c5], [c4]),
          ([cax, cont, loops, crosses, c6],
           [c5, bax1, bax2, bl, bi, bends, distep, dilab]),
          ([w0lab, imarr, c7], [c6]),
          ([c8], [c7]),
          ([bline, bars, dlab, c9], [c8, cax, cont, loops, crosses, w0lab, imarr])]


LandauL51ZH, LandauL51EN = make(AccuracyBase, 51)
