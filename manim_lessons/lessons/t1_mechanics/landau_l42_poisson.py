"""Lesson 42 — Poisson brackets (Landau §42).

The picture that carries the lesson is phase space with the Hamiltonian flow
drawn on it. A conserved quantity has level curves lying along that flow, so
the bracket with H vanishes; a quantity that is not conserved has level curves
cutting across it, and the dot visibly crosses from one level to the next.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import Dot, Line, Text, VGroup, always_redraw, PI
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_SMALL)
from manim_lessons.lessons.canonical_base import CanonicalBase, make, PX

PO = np.array([-3.35, -0.15, 0.0])          # phase-space origin
PSC = 1.05
WOSC = 0.85                                 # how fast the dot goes round


class PoissonBase(CanonicalBase):
 EPISODE = 42
 MODE_LABEL = {0: {"zh": "任何一個相空間上的函數", "en": "any function on phase space"},
               1: {"zh": "代入哈密頓方程，帕松括號就出現了",
                   "en": "put in Hamilton's equations and the bracket appears"},
               2: {"zh": "運動積分的條件", "en": "the condition for an integral of the motion"},
               3: {"zh": "等值線沿著流：所以它不變",
                   "en": "level curves along the flow, so it cannot change"},
               4: {"zh": "任意兩個量的帕松括號", "en": "the bracket of any two quantities"},
               5: {"zh": "反對稱，而且對常數為零",
                   "en": "antisymmetric, and zero against a constant"},
               6: {"zh": "座標與動量之間的基本括號",
                   "en": "the fundamental brackets among q and p"},
               7: {"zh": "雅可比恆等式", "en": "Jacobi's identity"},
               8: {"zh": "帕松定理", "en": "Poisson's theorem"},
               9: {"zh": "已知的守恆量能生出新的",
                   "en": "known integrals can breed new ones"}}

 def _flow(self, q, p):
  return np.array([p, -q, 0.0])

 def _dotpos(self):
  a = -WOSC * self._tau()
  return PO + PSC * np.array([np.cos(a), np.sin(a), 0.0])

 def stage(self):
  # Beat 1 carries a three-line formula reaching down to y = 1.40, and the
  # beat-3 labels sit at y = 1.62, so the p axis and its label have to keep
  # clear of both: h = 1.20 puts the label at y = 1.23.
  ax = self._axes(PO, "q", "p", w=2.15, h=1.20)
  field = VGroup()
  for q in np.linspace(-1.5, 1.5, 7):
   for pp in np.linspace(-1.15, 1.15, 5):
    if abs(q) < 1e-9 and abs(pp) < 1e-9: continue
    d = self._flow(q, pp); d = 0.40 * d / max(float(np.linalg.norm(d)), 1e-6)
    a = PO + PSC * np.array([q, pp, 0.0])
    field.add(self._arr(a, a + d, ACCENT_C, sw=2.5, tl=0.11))
  # level curves of a conserved f: circles, lying along the flow
  good = VGroup(*[self._curve([PO + PSC * r * np.array([np.cos(a), np.sin(a), 0.0])
                               for a in np.linspace(0, 2 * PI, 90)], ACCENT_B, sw=3)
                  for r in (0.55, 0.92, 1.25)])
  # level curves of something not conserved: verticals, cutting across it
  bad = VGroup(*[self._curve([PO + np.array([PSC * c, PSC * y, 0.0])
                              for y in np.linspace(-1.25, 1.25, 30)], WARN, sw=3)
                 for c in (-1.1, -0.55, 0.0, 0.55, 1.1)])
  pdot = always_redraw(lambda: Dot(self._dotpos(), color=ACCENT_A, radius=0.10))
  gl = self._mid(1.62, "f 的等值線：沿著流", "f: along the flow", ACCENT_B, FS_SMALL,
                 x=PO[0] - 1.15, w=2.2)
  bl = self._mid(1.62, "g 的等值線：橫切", "g: across it", WARN, FS_SMALL,
                 x=PO[0] + 1.30, w=2.2)

  c0 = VGroup(self._row(0.95, "f ( p , q , t )", "f ( p , q , t )", ACCENT_A, FS_BODY),
              self._row(0.25, "先寫下它的全導數", "write its total derivative", DIM))
  c1 = VGroup(self._row(0.95, "q̇ 與 ṗ 換成 H 的偏導數",
                        "q̇ and ṗ become derivatives of H", DIM),
              self._row(0.25, "剩下的組合就是帕松括號",
                        "what is left is the Poisson bracket", ACCENT_C, FS_BODY))
  c2 = VGroup(self._row(0.95, "df/dt = 0", "df/dt = 0", ACCENT_A, FS_BODY),
              self._row(0.25, "就是運動積分", "an integral of the motion", DIM))
  c3 = VGroup(self._row(0.95, "不顯含時間時", "with no explicit time", DIM),
              self._row(0.25, "[ H , f ] = 0", "[ H , f ] = 0", ACCENT_B, FS_BODY),
              self._row(-0.45, "等值線與流向重合", "its level curves follow the flow", ACCENT_B),
              self._row(-1.15, "g 的等值線橫著切過去，就會變",
                        "g cuts across the flow, so it changes", WARN))
  c4 = VGroup(self._row(0.95, "對每一對 q 與 p", "for each q and p pair", DIM),
              self._row(0.25, "交叉的偏導數相減", "subtract the crossed derivatives", ACCENT_C))
  c5 = VGroup(self._row(0.95, "對調兩個函數就變號", "swapping them changes the sign", ACCENT_C),
              self._row(0.25, "對常數的括號是零", "the bracket with a constant is zero", DIM),
              self._row(-0.45, "而且對每個變數都是線性的", "and it is linear in each", DIM))
  c6 = VGroup(self._row(0.95, "兩個座標：零", "two coordinates: zero", DIM),
              self._row(0.25, "兩個動量：零", "two momenta: zero", DIM),
              self._row(-0.45, "動量與自己的座標：一",
                        "a momentum with its own coordinate: one", ACCENT_B))
  c7 = VGroup(self._row(0.95, "三個函數依序輪換", "the three functions in cyclic order", DIM),
              self._row(0.25, "三項加起來恆等於零", "the three terms add up to zero", ACCENT_C))
  c8 = VGroup(self._row(0.95, "f 與 g 都守恆", "f and g are both integrals", DIM),
              self._row(0.25, "那麼 [ f , g ] 也守恆", "then [ f , g ] is one too", ACCENT_A,
                        FS_BODY))
  c9 = VGroup(self._row(0.95, "在雅可比恆等式裡取 h = H",
                        "put h = H in Jacobi's identity", DIM),
              self._row(0.25, "前兩項各自為零", "the first two terms vanish", DIM),
              self._row(-0.45, "所以第三項也必須為零",
                        "so the third must vanish as well", ACCENT_C),
              self._row(-1.15, "守恆量可以互相生成", "integrals generate integrals", WARN,
                        FS_BODY))

  return [([ax, c0], []),
          ([field, c1], [c0]),
          ([c2], [c1]),
          ([good, bad, gl, bl, pdot, c3], [c2]),
          ([c4], [c3, good, bad, gl, bl]),
          ([c5], [c4]),
          ([c6], [c5]),
          ([c7], [c6]),
          ([c8], [c7]),
          ([c9], [c8])]


LandauL42ZH, LandauL42EN = make(PoissonBase, 42)
