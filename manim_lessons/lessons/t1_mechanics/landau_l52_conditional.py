"""Lesson 52 — Conditionally periodic motion (Landau §52).

The section's one hard claim is that the motion never repeats yet passes
arbitrarily close to every state, and that is a claim about a picture: the
square of the two angle variables, wrapped at two pi on both sides. A straight
line of irrational slope is drawn on it, beat after beat, and slowly blackens
the whole square without ever closing. Switching the frequency ratio to a ratio
of small integers closes it immediately, which is degeneracy; the last beats
give degeneracy its physical example, the closed Kepler ellipse and the extra
one-valued vector that goes with it.

The trajectory is a table built at import: a line on a torus is exact, so there
is nothing to integrate, but it must be cut into separate strokes wherever it
wraps or the wrap segments draw straight across the square.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Rectangle, Text, VGroup, VMobject, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

SQ = np.array([-3.60, -0.10, 0.0])          # centre of the (w₁, w₂) square
HS = 1.30                                   # its half side
RATE = 1.75                                 # w₁ per second
GOLD = 0.5 * (1.0 + np.sqrt(5.0))           # an irrational slope, as far from rational as any
DEG = 2.0 / 3.0                             # the commensurable ratio for the degenerate beat
WMAX = 200.0                                # precomputed past the longest the beats can run,
                                            # so the point never freezes at the end
TAU = 2 * PI

PL1 = np.array([-5.05, 0.15, 0.0])          # the two little phase loops of beats 0-1
PL2 = np.array([-1.95, 0.15, 0.0])

KC = np.array([-3.45, -0.35, 0.0])          # Kepler ellipse centre
KA, KB = 1.70, 1.05                         # its semi-axes on screen


def _strokes(slope):
 """The line w₂ = slope · w₁ on the torus, as one straight stroke per wrap.

 Between two wraps the line is exactly straight, so each stroke needs only its
 two endpoints -- a few dozen points for the whole figure instead of thousands
 of samples redrawn every frame."""
 cuts = {0.0, WMAX}
 k = 1
 while TAU * k <= WMAX: cuts.add(TAU * k); k += 1
 k = 1
 while TAU * k / slope <= WMAX: cuts.add(TAU * k / slope); k += 1
 ts = sorted(cuts)
 out = []
 for a, b in zip(ts[:-1], ts[1:]):
  if b - a < 1e-6: continue
  m = 0.5 * (a + b)
  ox = TAU * np.floor(m / TAU); oy = TAU * np.floor(slope * m / TAU)
  out.append((a, b, (a - ox) / TAU, (slope * a - oy) / TAU,
              (b - ox) / TAU, (slope * b - oy) / TAU))
 return out


TRACKS = {"irr": _strokes(GOLD), "deg": _strokes(DEG)}


class ConditionalBase(CanonicalBase):
 EPISODE = 52
 MODE_LABEL = {0: {"zh": "變數完全分離", "en": "the variables separate completely"},
               1: {"zh": "每個座標一個作用變數",
                   "en": "one action variable per coordinate"},
               2: {"zh": "作用變數與角變數",
                   "en": "action variables and angle variables"},
               3: {"zh": "來回一趟只加 2π", "en": "there and back adds just two pi"},
               4: {"zh": "多重傅立葉級數", "en": "a multiple Fourier series"},
               5: {"zh": "頻率一般不可公度",
                   "en": "the frequencies are incommensurable"},
               6: {"zh": "永遠不回來，卻無限接近",
                   "en": "never returning, yet passing arbitrarily close"},
               7: {"zh": "可公度就是簡併", "en": "commensurable means degenerate"},
               8: {"zh": "簡併帶來更多單值積分",
                   "en": "degeneracy brings more one-valued integrals"},
               9: {"zh": "庫侖場：完全簡併", "en": "the Coulomb field: completely degenerate"}}

 # ── the square of angle variables ─────────────────────────────────
 def _wnow(self):
  return min(WMAX, max(0.0, RATE * (self.t.get_value() - self.tw0)))

 def _sqpt(self, x, y):
  return SQ + np.array([HS * (2 * x - 1), HS * (2 * y - 1), 0.0])

 def _line(self):
  """Every stroke drawn so far; each wrap of the square is a pen lift."""
  w = self._wnow()
  m = VMobject(color=ACCENT_B, stroke_width=2.2)
  drew = False
  for a, b, x0, y0, x1, y1 in TRACKS[self.track]:
   if a >= w: break
   f = 1.0 if b <= w else (w - a) / (b - a)
   m.start_new_path(self._sqpt(x0, y0))
   m.add_points_as_corners([self._sqpt(x0 + f * (x1 - x0), y0 + f * (y1 - y0))])
   drew = True
  if not drew:
   m.start_new_path(self._sqpt(0.0, 0.0))
   m.add_points_as_corners([self._sqpt(0.0, 0.0)])
  return m

 def _runner(self):
  w = self._wnow()
  for a, b, x0, y0, x1, y1 in TRACKS[self.track]:
   if w <= b:
    f = 0.0 if b <= a else (w - a) / (b - a)
    return Dot(self._sqpt(x0 + f * (x1 - x0), y0 + f * (y1 - y0)),
               color=ACCENT_A, radius=0.09)
  return Dot(self._sqpt(x1, y1), color=ACCENT_A, radius=0.09)

 # ── the two little phase loops of the opening beats ───────────────
 def _loop(self, o, a, b, color):
  us = np.linspace(0, 2 * PI, 80)
  return VGroup(self._curve([o + np.array([a * np.cos(u), b * np.sin(u), 0.0]) for u in us],
                            color, sw=3),
                Dot(o, color=GHOST, radius=0.04))

 # ── the closed Kepler orbit and the vector peculiar to it ─────────
 def _kfocus(self):
  return KC + np.array([-KA * np.sqrt(1.0 - (KB / KA) ** 2), 0.0, 0.0])

 def _korbit(self):
  """Static: the closed path, the attracting centre, and the extra integral."""
  f = self._kfocus()
  return VGroup(self._curve([KC + np.array([KA * np.cos(u), KB * np.sin(u), 0.0])
                             for u in np.linspace(0, 2 * PI, 140)], ACCENT_B, sw=3),
                Dot(f, color=ACCENT_A, radius=0.10),
                self._arr(f, f + np.array([-1.15, 0.0, 0.0]), WARN, sw=5, tl=0.18),
                # Just the symbol: any wording long enough to explain it runs off
                # the left edge, and the panel row beside it already says what it is.
                Text("A", font_size=FS_SMALL, color=WARN)
                .move_to(f + np.array([-1.10, 0.30, 0])))

 def _kmover(self):
  f = self._kfocus()
  th = 1.15 * (self.t.get_value() - self.tk0)
  p = KC + np.array([KA * np.cos(th), KB * np.sin(th), 0.0])
  return VGroup(Line(f, p, color=DIM, stroke_width=2), Dot(p, color=ACCENT_C, radius=0.10))

 def stage(self):
  self.track = "irr"
  self.tw0 = 0.0; self.tk0 = 0.0

  l1 = self._loop(PL1, 0.85, 0.62, ACCENT_B)
  l2 = self._loop(PL2, 0.55, 0.88, ACCENT_C)
  ll1 = self._mid(-1.05, "( q₁ , p₁ )", "( q₁ , p₁ )", ACCENT_B, FS_SMALL, x=PL1[0], w=2.2)
  ll2 = self._mid(-1.05, "( q₂ , p₂ )", "( q₂ , p₂ )", ACCENT_C, FS_SMALL, x=PL2[0], w=2.2)
  il1 = self._mid(1.24, "I₁ = 面積 / 2π", "I₁ = area / two pi", ACCENT_B, FS_SMALL,
                  x=PL1[0], w=2.7)
  il2 = self._mid(1.24, "I₂ = 面積 / 2π", "I₂ = area / two pi", ACCENT_C, FS_SMALL,
                  x=PL2[0], w=2.7)

  box = Rectangle(width=2 * HS, height=2 * HS, color=DIM, stroke_width=2.5).move_to(SQ)
  bx = Text("w₁", font_size=FS_SMALL, color=DIM).move_to(SQ + np.array([HS + 0.32, -HS + 0.02,
                                                                       0]))
  by = Text("w₂", font_size=FS_SMALL, color=DIM).move_to(SQ + np.array([-HS - 0.32, HS - 0.02,
                                                                       0]))
  tick = VGroup(Text("0", font_size=FS_SMALL - 4, color=GHOST)
                .move_to(SQ + np.array([-HS - 0.24, -HS - 0.26, 0])),
                Text("2π", font_size=FS_SMALL - 4, color=GHOST)
                .move_to(SQ + np.array([HS - 0.02, -HS - 0.26, 0])))
  line = always_redraw(lambda: self._line())
  runner = always_redraw(lambda: self._runner())
  wlab = self._mid(-1.95, "邊界是接起來的：走出去就從另一邊回來",
                   "the edges are joined: leaving one side re-enters at the other",
                   DIM, FS_SMALL, x=SQ[0], w=5.6)
  dlab = self._mid(-1.95, "頻率變成 3 比 2：立刻閉合",
                   "the ratio is now three to two, and it closes at once",
                   WARN, FS_SMALL, x=SQ[0], w=5.6)
  korb = self._korbit()
  kmov = always_redraw(lambda: self._kmover())
  klab = self._mid(-1.85, "克卜勒運動：兩個頻率相同，軌道閉合",
                   "Kepler motion: the two frequencies coincide and the path closes",
                   WARN, FS_SMALL, x=KC[0], w=5.8)

  c0 = VGroup(self._row(0.95, "任意多個自由度", "any number of degrees of freedom", DIM),
              self._row(0.25, "每個座標上運動都有限",
                        "the motion is finite in every coordinate", ACCENT_C),
              self._row(-0.45, "S₀ = Σ Sᵢ ( qᵢ )", "S₀ = Σ Sᵢ ( qᵢ )", ACCENT_A, FS_BODY))
  c1 = VGroup(self._row(0.95, "每一項都是多值的", "each piece is many-valued", DIM),
              self._row(0.25, "座標來回一趟", "the coordinate runs there and back",
                        ACCENT_B),
              self._row(-0.45, "作用量就增加 2π Iᵢ", "and the action gains two pi Iᵢ",
                        ACCENT_A),
              self._row(-1.15, "每個自由度一個作用變數",
                        "one action variable per degree of freedom", WARN))
  c2 = VGroup(self._row(0.95, "和單自由度時一樣的變換",
                        "the same transformation as before", DIM),
              self._row(0.25, "Iᵢ 全是常數", "every Iᵢ is constant", ACCENT_B),
              self._row(-0.45, "wᵢ = ωᵢ t + 常數", "wᵢ = ωᵢ t + constant", ACCENT_A, FS_BODY))
  c3 = VGroup(self._row(0.95, "第 i 個座標來回一趟",
                        "one coordinate there and back", DIM),
              self._row(0.25, "只讓第 i 個角變數加 2π",
                        "raises only its own angle, by two pi", ACCENT_C),
              self._row(-0.45, "所以單值函數在每個 wᵢ 上都是週期的",
                        "so one-valued functions are periodic in each", ACCENT_B))
  c4 = VGroup(self._row(0.95, "展成多重傅立葉級數",
                        "expand in a multiple Fourier series", DIM),
              self._row(0.25, "代入 wᵢ = ωᵢ t + 常數",
                        "and put in wᵢ = ωᵢ t + constant", ACCENT_C),
              self._row(-0.45, "頻率是基本頻率的整數倍相加",
                        "frequencies are integer sums of the basic ones", ACCENT_A),
              self._row(-1.15, "ωₖ = ∂E / ∂Iₖ", "ωₖ = ∂E / ∂Iₖ", WARN, FS_BODY))
  c5 = VGroup(self._row(0.95, "這些頻率一般不可公度",
                        "these are generally incommensurable", ACCENT_C),
              self._row(0.25, "所以整個和不是週期的",
                        "so the sum is not a periodic function", DIM),
              self._row(-0.45, "座標與動量也都不是",
                        "and neither are the coordinates or momenta", WARN))
  c6 = VGroup(self._row(0.95, "經過某個狀態之後", "having passed through a state", DIM),
              self._row(0.25, "有限時間內不會再回來",
                        "it never returns in any finite time", WARN),
              self._row(-0.45, "但時間夠久就任意接近",
                        "yet in time it passes arbitrarily close", ACCENT_B),
              self._row(-1.15, "這叫條件週期運動",
                        "this is conditionally periodic motion", ACCENT_A, FS_BODY))
  c7 = VGroup(self._row(0.95, "幾個頻率可公度就叫簡併",
                        "commensurable frequencies mean degeneracy", ACCENT_C),
              self._row(0.25, "全部可公度就是完全簡併",
                        "all of them: completely degenerate", DIM),
              self._row(-0.45, "這時軌道閉合", "and then every path closes", WARN),
              self._row(-1.15, "能量依賴的獨立變數也變少",
                        "the energy also depends on fewer of them", DIM))
  c8 = VGroup(self._row(0.95, "沒有簡併時只有 s 個單值積分",
                        "without degeneracy only s are one-valued", DIM),
              self._row(0.25, "其餘是角變數除以頻率的差",
                        "the rest are differences of w over ω", ACCENT_C),
              self._row(-0.45, "有簡併時某個組合只差 2π 的整數倍",
                        "with it, one combination is fixed up to two pi", ACCENT_B),
              self._row(-1.15, "取三角函數就又是一個",
                        "so its cosine is one more one-valued integral", WARN))
  c9 = VGroup(self._row(0.95, "U = − α / r 就是例子",
                        "the field U = − α / r is the example", ACCENT_A),
              self._row(0.25, "多出來的是專屬它的那個向量",
                        "the extra integral is the vector peculiar to it", WARN),
              self._row(-0.45, "球座標與拋物線座標都能分離",
                        "and it separates in two coordinate systems", ACCENT_C),
              self._row(-1.15, "每個 Iᵢ 同樣是絕熱不變量",
                        "every Iᵢ is again an adiabatic invariant", DIM))

  def start_w():
   self.tw0 = self.t.get_value()

  def go_degenerate():
   self.track = "deg"; self.tw0 = self.t.get_value()

  def start_kep():
   self.tk0 = self.t.get_value()

  return [([l1, l2, ll1, ll2, c0], []),
          ([il1, il2, c1], [c0]),
          ([box, bx, by, tick, line, runner, wlab, c2],
           [c1, l1, l2, ll1, ll2, il1, il2], start_w),
          ([c3], [c2]),
          ([c4], [c3]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([dlab, c7], [c6, wlab], go_degenerate),
          ([c8], [c7]),
          ([korb, kmov, klab, c9], [c8, box, bx, by, tick, line, runner, dlab], start_kep)]


LandauL52ZH, LandauL52EN = make(ConditionalBase, 52)
