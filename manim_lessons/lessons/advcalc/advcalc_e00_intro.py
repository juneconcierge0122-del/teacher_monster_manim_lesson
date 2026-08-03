"""advcalc E00 — what Loomis & Sternberg's *Advanced Calculus* actually is.

The picture that carries the whole episode is the chapter band: fourteen cells
along the bottom, one per chapter, which stays on screen for all eleven beats
while a highlight walks across it. Chapters 0-11 are one logical unit (each
depending on the ones before) and 12-13 hang off the side as applications, so
beat 2 draws that split as two spans above the band and everything after it is
just the highlight moving.

Beat 3 is the exception: the band drops to a supporting role and the tangent
picture from the book's Fig. 3.8 (p. 141) comes up in the middle, because the
one idea worth showing before any of the content is that the differential is a
linear map approximating the change, with an error of smaller order.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Line, Rectangle, Text, VGroup, LEFT
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_CELL = 15                                # chapter numbers inside the band
FS_TAG = 17                                 # labels above the band

# ── the chapter band ──────────────────────────────────────────────────
# 14 cells, pitch 0.86, so the row spans x = -6.02 .. 6.02 (inside the 6.30
# safe edge). y is chosen so the band bottom sits at -1.78: the playbook's
# measured floor for animation is -1.90, below which a four-line subtitle hits.
NCH = 14
CW, CH, PITCH = 0.80, 0.46, 0.86
BY = -1.55
CX = [-5.59 + PITCH * i for i in range(NCH)]
SPAN_Y = BY + CH / 2 + 0.16                 # the bracket bar, -1.16
LABEL_Y = -0.72                             # group captions; 0.44 clear of the bar

# ── beat 3: the tangent picture (book Fig. 3.8, p. 141) ───────────────
OX, OY = -2.30, -0.60                       # picture origin on screen
UA, UT = 1.30, 2.90                         # the abscissas a and a+t
USPAN = 3.80
UTAN = (0.70, 3.05)                         # the tangent is cut short of the curve
                                            # so its far end stays under y = 1.28


def _f(u):
 """Concave and exaggerated on purpose: with a gentler curve the o(t) gap is
 a couple of hundredths of a screen unit and reads as a drawing error."""
 return 1.55 * (1.0 - np.exp(-0.80 * np.asarray(u, dtype=float)))


def _fp(u):
 return 1.24 * float(np.exp(-0.80 * u))


class AdvCalcE00Base(CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 0

 MODE_LABEL = {
  0: {"zh": "哈佛榮譽班的講義", "en": "notes from an honors course at Harvard"},
  1: {"zh": "先修條件", "en": "the prerequisites"},
  2: {"zh": "前半：賦範向量空間　　後半：流形", "en": "first half: normed vector spaces / second half: manifolds"},
  3: {"zh": "微分是最接近的那個線性逼近", "en": "the differential is the closest linear approximation"},
  4: {"zh": "代數的準備", "en": "algebraic preparation"},
  5: {"zh": "微分學本身", "en": "the differential calculus itself"},
  6: {"zh": "分析的地基，與第一批應用", "en": "analytic groundwork, and the first applications"},
  7: {"zh": "多重線性代數與積分", "en": "multilinear algebra and integration"},
  8: {"zh": "流形上的微積分", "en": "calculus on manifolds"},
  9: {"zh": "兩章互相獨立的應用", "en": "two independent applications"},
  10: {"zh": "這個系列的計畫", "en": "the plan for this series"},
 }

 # ── pieces ───────────────────────────────────────────────────────
 def _band(self):
  """One cell per chapter, numbered 0 to 13."""
  g = VGroup()
  for i in range(NCH):
   g.add(Rectangle(width=CW, height=CH, color=GHOST, stroke_width=2).move_to([CX[i], BY, 0]),
         Text(str(i), font_size=FS_CELL, color=DIM).move_to([CX[i], BY, 0]))
  return g

 def _hl(self, i0, i1, color=ACCENT_B):
  """A box around cells i0..i1. Height 0.58 keeps the bottom at -1.84."""
  x0, x1 = CX[i0] - CW / 2, CX[i1] + CW / 2
  return Rectangle(width=(x1 - x0) + 0.14, height=0.58, color=color,
                   stroke_width=4).move_to([(x0 + x1) / 2, BY, 0])

 def _span(self, i0, i1, color):
  """A bracket over cells i0..i1, drawn above the band."""
  x0, x1 = CX[i0] - CW / 2, CX[i1] + CW / 2
  bar = self._dash([x0, SPAN_Y, 0], [x1, SPAN_Y, 0], color, n=max(6, int((x1 - x0) * 3)))
  tick = VGroup(*[self._dash([x, SPAN_Y, 0], [x, SPAN_Y - 0.12, 0], color, n=2)
                  for x in (x0, x1)])
  return VGroup(bar, tick)

 def _cap(self, i0, i1, zh, en, color=ACCENT_B):
  x0, x1 = CX[i0] - CW / 2, CX[i1] + CW / 2
  return self._mid(LABEL_Y, zh, en, color=color, size=FS_TAG,
                   x=(x0 + x1) / 2, w=(x1 - x0) + 1.6)

 def _topics(self, rows):
  """What a chapter group actually contains, as a centred column.

  Beats 4-9 are pure highlight-walking, and without this the whole middle of
  the frame is empty for six consecutive beats — the failure the playbook
  warns about. Top row tops out at 1.11, bottom row bottoms at -0.46, so the
  column clears both the two-line formula and the group caption."""
  return VGroup(*[self._mid(y, zh, en, INK, FS_TAG, w=10.0)
                  for y, (zh, en) in zip((1.00, 0.55, 0.10, -0.35), rows)])

 def _book(self):
  """The title card that stands in for the book itself, beats 0-2.

  Deliberately not repeating the authors and dates: those are already on the
  formula line for beat 0, and the card outlives that beat."""
  return VGroup(
   Rectangle(width=3.90, height=1.50, color=GHOST, stroke_width=2).move_to([0, 0.30, 0]),
   Text("ADVANCED CALCULUS", font_size=FS_TAG, color=ACCENT_A).move_to([0, 0.72, 0]),
   Text("revised edition", font_size=FS_SMALL, color=DIM).move_to([0, 0.34, 0]),
   Text("592 pp.  ·  ch. 0 – 13", font_size=FS_SMALL, color=INK).move_to([0, -0.06, 0]))

 def _prereq(self):
  """Two chips feeding the book card, beat 1.

  The chips stop at x = -2.65 and the card starts at -1.95, which is the whole
  reason the card shrank: `_arr` returns an empty VGroup below length 0.05, so
  an arrow into a card that a wide English label already touches draws
  nothing at all and fails silently."""
  a = self._mid(0.72, "嚴格的單變數微積分", "rigorous one variable calculus",
                ACCENT_C, FS_TAG, x=-4.30, w=3.30)
  b = self._mid(0.10, "線性代數", "linear algebra", ACCENT_C, FS_TAG, x=-4.30, w=3.30)
  return VGroup(a, b,
                self._arr([-2.55, 0.72, 0], [-2.05, 0.52, 0], ACCENT_C, sw=3, tl=0.14),
                self._arr([-2.55, 0.10, 0], [-2.05, 0.24, 0], ACCENT_C, sw=3, tl=0.14))

 def _legend(self):
  """Curve / tangent / gap named in a column on the empty right half.

  The three names started out next to the lines they label, but at this scale
  df, Δf and 𝒪(t) all want the same corner above the point a+t and overlap
  each other whatever order they are placed in. Out here they cannot collide,
  and the colours carry the correspondence."""
  g = VGroup()
  for y, color, s in ((0.95, ACCENT_A, "Δf"), (0.50, ACCENT_C, "df"), (0.05, WARN, "𝒪 ( t )")):
   g.add(Line([3.20, y, 0], [3.65, y, 0], color=color, stroke_width=4),
         Text(s, font_size=FS_TAG, color=color).move_to([3.82, y, 0], aligned_edge=LEFT))
  return g

 def _tangent(self):
  """Book Fig. 3.8: the change, its linear approximation, and the gap."""
  us = np.linspace(0.0, USPAN, 160)
  curve = self._curve([[OX + u, OY + v, 0] for u, v in zip(us, _f(us))], ACCENT_A, sw=4)

  fa, m = float(_f(UA)), _fp(UA)
  tan = self._curve([[OX + u, OY + fa + m * (u - UA), 0] for u in UTAN], ACCENT_C, sw=3)

  ya, yc = OY + fa, OY + float(_f(UT))      # the curve at a and at a+t
  yt = OY + fa + m * (UT - UA)              # the tangent at a+t
  axes = VGroup(self._arr([OX - 0.30, OY, 0], [OX + USPAN + 0.30, OY, 0], DIM, sw=3, tl=0.14),
                self._arr([OX, OY - 0.22, 0], [OX, OY + 1.75, 0], DIM, sw=3, tl=0.14))
  guides = VGroup(self._dash([OX + UA, OY, 0], [OX + UA, ya, 0], GHOST, n=5),
                  self._dash([OX + UT, OY, 0], [OX + UT, yt, 0], GHOST, n=9))
  gap = self._arr([OX + UT, yc, 0], [OX + UT, yt, 0], WARN, sw=4, tl=0.12)
  return VGroup(axes, guides, curve, tan, gap, self._legend(),
                Text("a", font_size=FS_SMALL, color=DIM).move_to([OX + UA, OY - 0.26, 0]),
                Text("a + t", font_size=FS_SMALL, color=DIM).move_to([OX + UT + 0.16, OY - 0.26, 0]))

 def _close(self):
  return VGroup(
   self._mid(0.72, "155 集　·　一集約兩到四個書頁", "155 episodes  ·  two to four pages each", ACCENT_A, FS_TAG, w=9.0),
   self._mid(0.18, "加星號的進階節也不跳過", "the starred advanced sections are not skipped", INK, FS_TAG, w=9.0),
   self._mid(-0.40, "下一集：第 0 章第 1 到 3 節，邏輯與量詞",
             "next: chapter 0, sections 1 to 3, logic and quantifiers", ACCENT_B, FS_TAG, w=9.0))

 # ── the ten beats ────────────────────────────────────────────────
 def stage(self):
  band, book, pre = self._band(), self._book(), self._prereq()
  spans = VGroup(self._span(0, 11, ACCENT_B), self._span(12, 13, ACCENT_C))
  caps = VGroup(self._cap(0, 11, "第 0 到 11 章：一個邏輯上的整體",
                          "chapters 0 to 11: one logical unit", ACCENT_B),
                self._cap(12, 13, "獨立", "independent", ACCENT_C))
  tan = self._tangent()
  close = self._close()

  groups = [
   (0, 2, "第 0 到 2 章", "chapters 0 to 2",
    [("邏輯、量詞、集合", "logic, quantifiers, sets"),
     ("向量空間、子空間、商空間", "vector spaces, subspaces, quotients"),
     ("基底、維數、對偶空間", "bases, dimension, the dual space"),
     ("矩陣、跡、行列式", "matrices, trace, determinant")]),
   (3, 3, "第 3 章", "chapter 3",
    [("範數與連續性", "norms and continuity"),
     ("無窮小的三個類", "the three classes of infinitesimal"),
     ("微分、方向導數、均值定理", "the differential, directional derivatives"),
     ("隱函數定理、拉格朗日乘子", "the implicit-function theorem, multipliers")]),
   (4, 6, "第 4 到 6 章", "chapters 4 to 6",
    [("度量空間、緊緻性、完備性", "metric spaces, compactness, completeness"),
     ("壓縮映射不動點定理", "the contraction mapping fixed-point theorem"),
     ("純量積、正交投影、自伴", "scalar products, projection, self-adjointness"),
     ("微分方程與傅立葉級數", "differential equations and Fourier series")]),
   (7, 8, "第 7 到 8 章", "chapters 7 to 8",
    [("雙線性與多重線性泛函", "bilinear and multilinear functionals"),
     ("交錯張量與外代數", "alternating tensors and the exterior algebra"),
     ("行列式的代數來源", "where the determinant comes from"),
     ("黎曼積分與變數變換公式", "Riemann integration, change of variables")]),
   (9, 11, "第 9 到 11 章", "chapters 9 to 11",
    [("座標卡與可微流形", "atlases and differentiable manifolds"),
     ("切空間、向量場、李導數", "tangent spaces, vector fields, Lie derivatives"),
     ("單位分割、密度、散度定理", "partitions of unity, densities, divergence"),
     ("外微分形式與斯托克斯定理", "exterior forms and Stokes' theorem")]),
   (12, 13, "第 12 到 13 章", "chapters 12 to 13",
    [("格林公式與卜瓦松積分", "Green's formulas and the Poisson integral"),
     ("狄利克雷問題與次調和函數", "Dirichlet's problem, subharmonic functions"),
     ("餘切叢上的辛形式", "the symplectic form on the cotangent bundle"),
     ("剛體、小振盪、正則變換", "rigid bodies, small oscillations, canonical maps")]),
  ]
  marks = [(self._hl(a, b), self._cap(a, b, zh, en), self._topics(rows))
           for a, b, zh, en, rows in groups]

  plan = [([band, book], []),                      # 0  the book
          ([pre], []),                             # 1  prerequisites
          ([spans, caps], [pre]),                  # 2  the two halves
          ([tan], [book, spans, caps]),            # 3  what a differential is
          ]
  for k, mark in enumerate(marks):                 # 4-9  the highlight walks
   out = [tan] if k == 0 else list(marks[k - 1])
   plan.append((list(mark), out))
  plan.append(([close], list(marks[-1])))          # 10  the plan for the series
  return plan


AdvCalcE00ZH, AdvCalcE00EN = make(AdvCalcE00Base, "00", prefix="AdvCalcE")
