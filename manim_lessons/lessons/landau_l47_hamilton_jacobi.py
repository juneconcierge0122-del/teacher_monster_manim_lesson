"""Lesson 47 — The Hamilton-Jacobi equation (Landau §47).

The middle of the lesson gets the picture it deserves: two panels side by side,
the ordinary phase plane on the left with the representative point running
along its orbit, and the (alpha, beta) plane on the right where the very same
motion is a point that does not move at all. That is the whole content of the
method — a canonical transformation onto constants. The last beat returns to
the optical picture, with the level surfaces of S advancing as wavefronts.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

PL = np.array([-5.15, -0.10, 0.0])          # the ordinary phase plane
PR = np.array([-1.40, -0.10, 0.0])          # the plane of the new constants
RX, RY = 0.95, 0.80                         # orbit semiaxes on screen
WSP = 0.62                                  # how fast the point runs

WC = np.array([-3.30, -0.15, 0.0])          # centre of the wavefront picture
SQ = 0.55                                   # squashed so the outermost front clears
                                            # the subtitle at the bottom of the frame


class HamiltonJacobiBase(CanonicalBase):
 EPISODE = 47
 MODE_LABEL = {0: {"zh": "上一課的兩個結果", "en": "two results from the last lesson"},
               1: {"zh": "把動量換成 S 的導數", "en": "replace each momentum by a derivative of S"},
               2: {"zh": "一整套積分方法的出發點",
                   "en": "the basis of a general method"},
               3: {"zh": "要的是完全積分", "en": "what we want is a complete integral"},
               4: {"zh": "把它當成生成函數", "en": "take it as a generating function"},
               5: {"zh": "新的哈密頓量等於零", "en": "the new Hamiltonian vanishes"},
               6: {"zh": "所有新變數都是常數", "en": "so every new variable is a constant"},
               7: {"zh": "解出座標隨時間的變化", "en": "solve for the coordinates in time"},
               # beat 8's formula is already two lines
               9: {"zh": "等值面是波前，動量是光線",
                   "en": "level surfaces are wavefronts, momenta are rays"}}

 def _orb(self, o, moving):
  a = WSP * (self.t.get_value() - self.tflow0) if moving else 0.0
  return o + np.array([RX * np.cos(a), RY * np.sin(a), 0.0])

 def stage(self):
  self.tflow0 = 0.0
  # h kept low so the p and β axis labels stay clear of `heads` at y = 1.30
  axL = self._axes(PL, "q", "p", w=1.35, h=0.95)
  axR = self._axes(PR, "α", "β", w=1.35, h=0.95)
  orbit = self._curve([PL + np.array([RX * np.cos(a), RY * np.sin(a), 0.0])
                       for a in np.linspace(0, 2 * PI, 120)], GHOST, sw=2.5)
  runner = always_redraw(lambda: Dot(self._orb(PL, True), color=ACCENT_A, radius=0.11))
  frozen = Dot(PR + np.array([RX * 0.55, RY * 0.45, 0.0]), color=WARN, radius=0.11)
  # Below the planes: at centre height this would sit on the q axis and its label,
  # and the gap between the two planes there is only about one unit wide.
  arrow = self._arr(PL + np.array([1.55, -0.95, 0]), PR + np.array([-1.55, -0.95, 0]),
                    ACCENT_C, sw=4, tl=0.16)
  heads = VGroup(self._mid(1.30, "點一直在動", "the point keeps moving", ACCENT_A, FS_SMALL,
                           x=PL[0], w=2.9),
                 self._mid(1.30, "點完全不動", "the point does not move", WARN, FS_SMALL,
                           x=PR[0], w=2.9))
  glab = self._mid(-1.86, "生成函數就是漢彌頓－雅可比方程的完全積分",
                   "the generating function is the complete integral", ACCENT_C, FS_SMALL,
                   x=-3.25, w=5.8)

  # ── beat 9: wavefronts and rays ────────────────────────────────
  def _front(a, r):
   return WC + r * np.array([np.cos(a), SQ * np.sin(a), 0.0])

  fronts = always_redraw(lambda: VGroup(*[
   self._curve([_front(a, r) for a in np.linspace(-1.12, 1.12, 56)], ACCENT_B, sw=3)
   for r in 0.70 + 0.50 * np.arange(4) + 0.50 * ((0.42 * self._tau()) % 1.0)]))
  rays = VGroup(*[self._arr(_front(a, 2.32), _front(a, 2.32) + 0.55 * _unit(a),
                            WARN, sw=4, tl=0.15)
                  for a in np.linspace(-0.90, 0.90, 7)])
  wlab = VGroup(self._mid(1.52, "S = 常數：波前", "S = const: wavefronts", ACCENT_B, FS_SMALL,
                          x=WC[0] - 1.35, w=2.7),
                self._mid(1.52, "p = ∇S：光線", "p = ∇S: the rays", WARN, FS_SMALL,
                          x=WC[0] + 1.55, w=2.7))

  c0 = VGroup(self._row(0.95, "∂S/∂t + H = 0", "∂S/∂t + H = 0", ACCENT_A, FS_BODY),
              self._row(0.25, "∂S/∂qᵢ = pᵢ", "∂S/∂qᵢ = pᵢ", ACCENT_B, FS_BODY))
  c1 = VGroup(self._row(0.95, "一階偏微分方程", "a first-order partial equation", DIM),
              self._row(0.25, "只含 S 一個未知函數",
                        "in the single unknown S", ACCENT_C),
              self._row(-0.45, "漢彌頓－雅可比方程",
                        "the Hamilton-Jacobi equation", ACCENT_A, FS_BODY))
  c2 = VGroup(self._row(0.95, "和拉格朗日方程並列",
                        "alongside Lagrange's equations", DIM),
              self._row(0.25, "和正則方程並列", "and the canonical equations", DIM),
              self._row(-0.45, "都是積分運動方程的方法",
                        "each a way of integrating the motion", ACCENT_B))
  c3 = VGroup(self._row(0.95, "通解含任意函數", "the general integral has a function", DIM),
              self._row(0.25, "完全積分含 s + 1 個常數",
                        "a complete integral has s + 1 constants", ACCENT_A),
              self._row(-0.45, "其中一個是相加常數",
                        "one of which is merely additive", DIM))
  c4 = VGroup(self._row(0.95, "f ( t , q ; α ) 當生成函數",
                        "f ( t , q ; α ) generates", ACCENT_C),
              self._row(0.25, "α 當新的動量", "with the α as the new momenta", ACCENT_B),
              self._row(-0.45, "β 當新的座標", "and the β as the new coordinates", ACCENT_A))
  c5 = VGroup(self._row(0.95, "H′ = H + ∂f/∂t", "H′ = H + ∂f/∂t", ACCENT_A, FS_BODY),
              self._row(0.25, "但 f 滿足那條方程",
                        "but f satisfies the equation", DIM),
              self._row(-0.45, "所以 H′ = 0", "so H′ = 0", WARN, FS_BODY))
  c6 = VGroup(self._row(0.95, "H′ = 0 ⟹ 導數全為零",
                        "H′ = 0 kills every derivative", DIM),
              self._row(0.25, "α 是常數，β 也是常數",
                        "the α are constants, and so are the β", ACCENT_B))
  c7 = VGroup(self._row(0.95, "∂f/∂αᵢ = βᵢ", "∂f/∂αᵢ = βᵢ", ACCENT_A, FS_BODY),
              self._row(0.25, "s 條代數方程", "s algebraic equations", DIM),
              self._row(-0.45, "解出 q ( t )", "give q as a function of t", ACCENT_C),
              self._row(-1.15, "再由 p = ∂S/∂q 得到動量",
                        "and p = ∂S/∂q gives the momenta", DIM))
  c8 = VGroup(self._row(0.95, "保守系統：S = S₀ − E t",
                        "conservative: S = S₀ − E t", ACCENT_A, FS_BODY),
              self._row(0.25, "只剩座標的方程",
                        "leaving an equation in q alone", ACCENT_B))
  c9 = VGroup(self._row(0.95, "S 的等值面就是波前",
                        "the level surfaces of S are wavefronts", ACCENT_B),
              self._row(0.25, "動量處處垂直於它們",
                        "the momenta stand normal to them", WARN),
              self._row(-0.45, "運動就是波前的傳播",
                        "the motion is their advance", ACCENT_C),
              self._row(-1.15, "力學與光學合而為一",
                        "mechanics and optics become one", ACCENT_A))

  return [([axL, orbit, runner, c0], [],
           lambda: setattr(self, "tflow0", self.t.get_value())),
          ([c1], [c0]),
          ([c2], [c1]),
          ([c3], [c2]),
          ([axR, frozen, arrow, heads, glab, c4], [c3]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([c7], [c6]),
          ([c8], [c7]),
          ([fronts, rays, wlab, c9],
           [c8, axL, axR, orbit, runner, frozen, arrow, heads, glab])]


def _unit(a):
 d = np.array([np.cos(a), SQ * np.sin(a), 0.0])
 return d / float(np.linalg.norm(d))


LandauL47ZH, LandauL47EN = make(HamiltonJacobiBase, 47)
