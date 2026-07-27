"""Lesson 48 — Separation of the variables (Landau §48).

The picture is the bookkeeping made visible: the Hamilton-Jacobi equation as
one wide box holding all the variables, from which one tile at a time detaches,
carries off its own constant, and becomes a one-dimensional integral. By the
end the wide box is empty and the row of little integrals is the complete
integral — which is exactly what "reduced to quadratures" means.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import Dot, Rectangle, Text, VGroup, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make

BOXY = 0.72                                 # centre height of the big box
ROWY = -0.86                                # where the separated integrals sit
X0, DXT = -5.35, 1.05                       # first tile centre, tile pitch
TW, TH = 0.86, 0.62                         # tile size
NAMES = ("q₁", "q₂", "q₃", "t")


class SeparationBase(CanonicalBase):
 EPISODE = 48
 MODE_LABEL = {0: {"zh": "完全積分怎麼求？", "en": "how is a complete integral found?"},
               1: {"zh": "某個座標只以一個組合出現",
                   "en": "one coordinate appears only in one combination"},
               2: {"zh": "把 S 拆成兩部分", "en": "split S into two pieces"},
               3: {"zh": "那個組合必須是常數", "en": "the combination must be a constant"},
               4: {"zh": "一條常微分方程", "en": "an ordinary differential equation"},
               5: {"zh": "剩下的方程少一個變數",
                   "en": "one independent variable fewer remains"},
               6: {"zh": "保守系統的完全積分", "en": "the complete integral, conservative case"},
               7: {"zh": "循環座標是最簡單的特例",
                   "en": "a cyclic coordinate is the simplest case"},
               8: {"zh": "時間也是一個「循環變數」",
                   "en": "the time separates as a cyclic variable too"},
               9: {"zh": "球座標、拋物線座標……",
                   "en": "spherical, parabolic, and more"}}

 def _tile(self, j, y, color, tag=None):
  c = np.array([X0 + j * DXT, y, 0.0])
  box = Rectangle(width=TW, height=TH, color=color, stroke_width=3,
                  fill_opacity=0.16, fill_color=color).move_to(c)
  g = VGroup(box, Text(NAMES[j], font_size=FS_SMALL, color=color).move_to(c))
  if tag is not None:
   g.add(Text(tag, font_size=FS_SMALL - 2, color=WARN)
         .move_to(c + np.array([0.0, -0.56, 0])))
  return g

 def _bigbox(self, n):
  """The equation still holding n variables, shrinking as tiles peel away."""
  if n <= 0: return VGroup()
  w = n * DXT + 0.34
  c = np.array([X0 - 0.5 * TW + 0.5 * w - 0.17 + (4 - n) * DXT, BOXY, 0.0])
  return Rectangle(width=w, height=TH + 0.46, color=ACCENT_C, stroke_width=3).move_to(c)

 def stage(self):
  eqlab = self._mid(1.52, "漢彌頓－雅可比方程", "the Hamilton-Jacobi equation", ACCENT_C,
                    FS_SMALL, x=-3.30, w=4.6)
  # Below the α tags, which hang at y = -1.42 under each dropped tile.
  rowlab = self._mid(-1.80, "每一項只含一個變數，各自積分",
                     "each piece holds one variable and integrates on its own",
                     ACCENT_B, FS_SMALL, x=-3.30, w=5.8)

  full = VGroup(self._bigbox(4), *[self._tile(j, BOXY, ACCENT_A) for j in range(4)])
  # the equation losing one variable at a time, and the integrals it leaves behind
  boxes = [self._bigbox(3), self._bigbox(2), self._bigbox(1), VGroup()]
  peeled = [VGroup(*[self._tile(k, BOXY, ACCENT_A) for k in range(j + 1, 4)])
            for j in range(4)]
  drops = [self._tile(j, ROWY, ACCENT_B, tag=f"α{'₁₂₃'[j]}" if j < 3 else "− E t")
           for j in range(4)]
  cyc = self._tile(0, ROWY, WARN, tag="α₁ = p₁")

  c0 = VGroup(self._row(0.95, "許多重要情形都做得到",
                        "it can be done in many important cases", DIM),
              self._row(0.25, "方法叫做分離變數",
                        "the method is separating the variables", ACCENT_A))
  c1 = VGroup(self._row(0.95, "組合 φ ( q₁ , ∂S/∂q₁ )", "the combination φ ( q₁ , ∂S/∂q₁ )",
                        ACCENT_A),
              self._row(0.25, "不含其他座標", "with no other coordinate in it", DIM),
              self._row(-0.45, "也不含時間與其他導數",
                        "and no time or other derivative", DIM))
  c2 = VGroup(self._row(0.95, "S = S′ + S₁ ( q₁ )", "S = S′ + S₁ ( q₁ )", ACCENT_A, FS_BODY),
              self._row(0.25, "一部分只依賴 q₁", "one piece depends on q₁ alone", ACCENT_B))
  c3 = VGroup(self._row(0.95, "方程對任何 q₁ 都成立",
                        "the equation holds for every q₁", DIM),
              self._row(0.25, "q₁ 一變只有 φ 會變",
                        "and only φ changes when q₁ does", ACCENT_C),
              self._row(-0.45, "所以 φ 必須是常數",
                        "so φ has to be a constant", WARN, FS_BODY))
  c4 = VGroup(self._row(0.95, "φ = α₁", "φ = α₁", ACCENT_A, FS_BODY),
              self._row(0.25, "直接積分就得到 S₁",
                        "simple integration gives S₁", ACCENT_B))
  c5 = VGroup(self._row(0.95, "剩下的還是偏微分方程",
                        "what is left is still a partial equation", DIM),
              self._row(0.25, "但獨立變數少一個",
                        "but with one variable fewer", ACCENT_C),
              self._row(-0.45, "一個一個分離下去",
                        "separate them one after another", ACCENT_A))
  c6 = VGroup(self._row(0.95, "S = Σ Sₖ ( qₖ ) − E t", "S = Σ Sₖ ( qₖ ) − E t", ACCENT_A,
                        FS_BODY),
              self._row(0.25, "化成一串一維積分",
                        "a chain of one-dimensional integrals", ACCENT_B),
              self._row(-0.45, "這就叫化為求積", "this is what quadratures means", DIM))
  c7 = VGroup(self._row(0.95, "循環座標不出現在 H 裡",
                        "a cyclic coordinate is absent from H", DIM),
              self._row(0.25, "φ 就退化成 ∂S/∂q₁",
                        "so φ reduces to ∂S/∂q₁ alone", ACCENT_C),
              self._row(-0.45, "S₁ = α₁ q₁", "S₁ = α₁ q₁", ACCENT_A, FS_BODY),
              self._row(-1.15, "α₁ 就是那個守恆的動量",
                        "and α₁ is its conserved momentum", WARN))
  c8 = VGroup(self._row(0.95, "− E t 這一項", "the term with minus E t", DIM),
              self._row(0.25, "正是把時間分離出來",
                        "is the time separated in just that way", ACCENT_B))
  c9 = VGroup(self._row(0.95, "循環座標的簡化全包含在內",
                        "every cyclic simplification is contained here", DIM),
              self._row(0.25, "還有不循環卻可分離的情形",
                        "and cases that separate without being cyclic", ACCENT_C),
              self._row(-0.45, "球座標、拋物線座標",
                        "spherical and parabolic coordinates", ACCENT_A),
              self._row(-1.15, "最有力的求通解方法",
                        "the most powerful route to the general integral", WARN))

  return [([full, eqlab, c0], []),
          ([c1], [c0]),
          ([c2], [c1]),
          ([c3], [c2]),
          ([boxes[0], peeled[0], drops[0], rowlab, c4], [c3, full]),
          ([boxes[1], peeled[1], drops[1], c5], [c4, boxes[0], peeled[0]]),
          # beat 6 separates both q₃ and t, so the equation is emptied out here:
          # no box and no tiles left in it, or `t` would show twice.
          ([drops[2], drops[3], c6], [c5, boxes[1], peeled[1], eqlab]),
          ([cyc, c7], [c6, drops[0]]),
          ([c8], [c7]),
          ([c9], [c8])]


LandauL48ZH, LandauL48EN = make(SeparationBase, 48)
