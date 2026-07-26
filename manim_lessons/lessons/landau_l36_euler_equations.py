"""Lesson 36 — Euler's equations (Landau §36).

Beats 0-2 are the transformation rule: a vector pinned to a turning body sweeps
a cone, its tip moving at exactly Omega x A, and the general case adds the
vector's own rate in the moving frame. Beats 3-4 read the cyclic 1-2-3 pattern
of the resulting component equations straight off a cycling highlight, with the
product terms shown to be the components of Omega x M. Beats 5-9 drop the
torque: an asymmetric top traces a real polhode, integrated from Euler's
equations, and a symmetrical one collapses to Omega turning uniformly on a cone
about the body's own axis — the regular precession of §33 seen from the body.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arrow, Dot, FadeIn, FadeOut, Line, Rectangle, Text, VGroup, VMobject,
                   DashedVMobject, ValueTracker, always_redraw, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19

# ── axonometric projection, with x3 up ────────────────────────────────
EX = np.array([0.80, -0.42, 0.0]); EY = np.array([-0.66, -0.34, 0.0]); EZ = np.array([0.0, 1.0, 0.0])
ORG = np.array([-2.45, -0.55, 0.0]); PS = 1.15
L = 1.32                                    # axis length
LT = 1.16                                   # label radius, in units of L
OS = 1.30                                   # screen length per unit of angular velocity

ALF = np.deg2rad(42.0)                      # half-angle of the beat-1 cone
WA = 0.62                                   # rate at which A goes round it

# ── the asymmetric top of beat 5 ──────────────────────────────────────
IA = np.array([1.00, 1.70, 2.60])
# Comfortably inside the separatrix, so the polhode is a tidy closed loop about
# x3 (the largest moment) rather than a near-separatrix sweep across the sphere.
OM0 = np.array([0.55, 0.30, 0.80])          # period ≈ 8.8 s
POL_DT = 0.004; POL_N = 12000               # 48 s of trajectory, plenty for one beat


def _deriv(w):
 return np.array([-(IA[2] - IA[1]) * w[1] * w[2] / IA[0],
                  -(IA[0] - IA[2]) * w[2] * w[0] / IA[1],
                  -(IA[1] - IA[0]) * w[0] * w[1] / IA[2]])


def _polhode():
 """Integrate the torque-free Euler equations once, at import time."""
 out = np.empty((POL_N, 3)); w = OM0.copy()
 for i in range(POL_N):
  out[i] = w
  k1 = _deriv(w); k2 = _deriv(w + 0.5 * POL_DT * k1); k3 = _deriv(w + 0.5 * POL_DT * k2)
  k4 = _deriv(w + POL_DT * k3)
  w = w + (POL_DT / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
 return out


POL = _polhode()

# ── the symmetrical top of beats 6-9 ──────────────────────────────────
I1S = 1.00; I3S = 2.20
OM3 = 0.62; AMP = 0.72
WOM = OM3 * (I3S - I1S) / I1S               # the rate omega of (36.6)

PX = 1.50                                   # left edge of the right-hand panel


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-9 else 1.0)


def _p(v):
 return ORG + PS * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


class EulerEqBase(LandauBatchBase):
 EPISODE = 36; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "只有在慣性主軸上才這麼簡單",
                   "en": "this simple only in the principal axes"},
               1: {"zh": "固定在物體上的向量，只會被轉動帶著走",
                   "en": "a vector pinned to the body is only carried round"},
               2: {"zh": "把規則用到 P 與 M 上", "en": "the rule applied to P and to M"},
               3: {"zh": "三條方程只是指標的輪換", "en": "the same equation, cycled 1-2-3"},
               4: {"zh": "乘積項就是 Ω × M 的分量",
                   "en": "the product terms are the components of Ω × M"},
               5: {"zh": "非對稱陀螺：Ω 在物體上畫出一條閉曲線",
                   "en": "an asymmetric top: Ω traces a closed curve"},
               6: {"zh": "對稱陀螺：沿軸的分量是常數",
                   "en": "a symmetrical top: the axial component is constant"},
               7: {"zh": "兩個橫向分量互相驅動", "en": "the two transverse components drive each other"},
               8: {"zh": "橫向部分大小固定，等速旋轉",
                   "en": "the transverse part turns at constant magnitude"},
               9: {"zh": "從物體上看到的規則進動",
                   "en": "the regular precession, seen from the body"}}

 # ── drawing helpers ───────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _arr(self, start, tip, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(tip) - np.asarray(start))) < 0.05:
   return VGroup()
  return Arrow(start, tip, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off))
  return m

 def _dash(self, a, b, color, n=12, sw=2.5):
  """Fixed dash count, so a stretching segment never changes its family size."""
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _ax(self, v, color, sw=4, k=1.0):
  return self._arr(_p(np.zeros(3)), _p(k * L * np.asarray(v)), color, sw=sw, tl=0.18)

 def _ring(self, e1, e2, r, color, sw=2.5, k=72, at=None):
  c = np.zeros(3) if at is None else np.asarray(at)
  pts = [_p(c + r * (np.cos(a) * np.asarray(e1) + np.sin(a) * np.asarray(e2)))
         for a in np.linspace(0, 2 * PI, k)]
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(pts); return m

 def _curve(self, pts, color, sw=3):
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners([_p(q) for q in pts])
  return m

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  return self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)

 def _txt(self, y, s, color=INK, size=FS_BODY, x=PX):
  return Text(s, font_size=size, color=color).move_to([x, y, 0], aligned_edge=LEFT)

 # ── the moving parts, per stage ───────────────────────────────────
 def _tau(self):
  return self.t.get_value() - self.t0

 def _A(self):
  """Beats 1-2: a vector pinned to the body, going round the cone."""
  a = WA * self._tau()
  return np.array([np.sin(ALF) * np.cos(a), np.sin(ALF) * np.sin(a), np.cos(ALF)])

 def _pol(self):
  i = int(self._tau() / POL_DT) % POL_N
  return POL[i]

 def _oms(self):
  a = WOM * self._tau()
  return np.array([AMP * np.cos(a), AMP * np.sin(a), OM3])

 def _om(self):
  return self._pol() if self.mode == 5 else self._oms()

 # ── beat plumbing ─────────────────────────────────────────────────
 def beat(self, i, fin=(), fout=(), extra=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  r = min(0.5, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate(rate_func=linear).increment_value(r), run_time=r)
  d -= r
  if d > 1e-3:
   self.play(self.t.animate(rate_func=linear).increment_value(d), *extra, run_time=d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * (2.35 - 0.22 * max(0, len(s.split(chr(10))) - 2)))

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0; self.mode = 0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)
  O3 = _p(np.zeros(3))
  E1 = np.array([1.0, 0, 0]); E2 = np.array([0, 1.0, 0]); E3 = np.array([0, 0, 1.0])

  # ══ beat 0: why the moving frame ══════════════════════════════════
  axes = VGroup(self._ax(E1, ACCENT_A), self._ax(E2, ACCENT_A), self._ax(E3, ACCENT_A),
                Text("x₁", font_size=FS_SMALL, color=ACCENT_A)
                .move_to(_p(LT * L * E1) + np.array([0.14, -0.12, 0])),
                Text("x₂", font_size=FS_SMALL, color=ACCENT_A)
                .move_to(_p(LT * L * E2) + np.array([-0.16, -0.12, 0])),
                # beside the tip, not above it: beat 4 carries a three-line formula
                Text("x₃", font_size=FS_SMALL, color=ACCENT_A)
                .move_to(_p(LT * L * E3) + np.array([0.26, 0.02, 0])),
                Dot(O3, color=INK, radius=0.07))
  om0 = _unit(np.array([0.46, 0.30, 1.0]))
  m0 = _unit(np.array([0.46 / 1.0, 0.30 / 1.7, 1.0 / 2.6]))     # M_i = I_i Omega_i
  pair0 = VGroup(self._arr(O3, _p(1.35 * om0), ACCENT_C, sw=6, tl=0.22),
                 Text("Ω", font_size=FS_TAG, color=ACCENT_C)
                 .move_to(_p(1.35 * om0) + np.array([-0.26, 0.16, 0])),
                 self._arr(O3, _p(1.35 * m0), ACCENT_B, sw=6, tl=0.22),
                 Text("M", font_size=FS_TAG, color=ACCENT_B)
                 .move_to(_p(1.35 * m0) + np.array([0.28, 0.14, 0])))
  cap0 = VGroup(self._row(0.95, "固定座標系：dM/dt = K", "in the fixed frame: dM/dt = K", DIM,
                          FS_BODY),
                self._row(0.25, "但 M 與 Ω 一般不平行", "but M and Ω are not parallel", WARN),
                self._row(-0.40, "主軸座標系：Mᵢ = Iᵢ Ωᵢ", "principal axes: Mᵢ = Iᵢ Ωᵢ",
                          ACCENT_B, FS_BODY),
                self._row(-1.10, "所以先把方程換到動座標系",
                          "so move the equations to that frame", INK))

  # ══ beats 1-2: the transformation rule ════════════════════════════
  omv = VGroup(self._arr(O3, _p(1.55 * E3), ACCENT_C, sw=6, tl=0.22),
               Text("Ω", font_size=FS_TAG, color=ACCENT_C)
               .move_to(_p(1.55 * E3) + np.array([0.28, 0.10, 0])))
  AL = 1.50                                 # the length A is drawn at
  rim = DashedVMobject(self._ring(E1, E2, AL * np.sin(ALF), GHOST, sw=3,
                                  at=AL * np.cos(ALF) * E3), num_dashes=40, color=GHOST)
  side = self._dash(O3, _p(AL * np.cos(ALF) * E3), GHOST, n=8)
  avec = always_redraw(lambda: self._arr(O3, _p(AL * self._A()), ACCENT_A, sw=6, tl=0.22))
  atag = self._tag("A", lambda: _p(AL * self._A()), off=np.array([-0.26, 0.18, 0]),
                   color=ACCENT_A)
  cross = always_redraw(lambda: self._arr(
   _p(AL * self._A()), _p(AL * self._A() + 0.95 * _unit(np.cross(E3, self._A()))),
   WARN, sw=5, tl=0.18))
  ctag = self._tag("Ω × A", lambda: _p(AL * self._A()
                                       + 0.95 * _unit(np.cross(E3, self._A()))),
                   off=np.array([0.40, -0.16, 0]), color=WARN, size=FS_SMALL)
  cone = VGroup(omv, rim, side, avec, atag, cross, ctag)
  cap1 = VGroup(self._row(1.00, "A 固定在物體上時", "when A is pinned to the body", DIM),
                self._txt(0.45, "dA/dt  =  Ω × A", ACCENT_A),
                self._row(-0.30, "一般情況再加上它自己的變化",
                          "in general, add its own change", DIM),
                self._txt(-0.85, "dA/dt  =  d′A/dt  +  Ω × A", INK))
  # the vector triangle for the general case
  TO = np.array([2.30, -1.45, 0.0])
  t_own = np.array([1.15, 0.30, 0.0]); t_rot = np.array([0.45, 0.95, 0.0])
  tri = VGroup(self._arr(TO, TO + t_own, ACCENT_B, sw=5),
               self._arr(TO + t_own, TO + t_own + t_rot, WARN, sw=5),
               self._arr(TO, TO + t_own + t_rot, INK, sw=6, tl=0.22),
               Text("d′A/dt", font_size=FS_SMALL, color=ACCENT_B)
               .move_to(TO + 0.5 * t_own + np.array([0.10, -0.28, 0])),
               Text("Ω × A", font_size=FS_SMALL, color=WARN)
               .move_to(TO + t_own + 0.5 * t_rot + np.array([0.52, 0.0, 0])),
               Text("dA/dt", font_size=FS_SMALL, color=INK)
               .move_to(TO + 0.55 * (t_own + t_rot) + np.array([-0.42, 0.22, 0])))
  cap2 = VGroup(self._txt(1.05, "d′P/dt + Ω × P = F", ACCENT_B),
                self._txt(0.45, "d′M/dt + Ω × M = K", ACCENT_C))

  # ══ beats 3-4: the cyclic component equations ═════════════════════
  def _cyc(rows, colors, y0=0.95, dy=0.72):
   g = VGroup()
   for k, (s, c) in enumerate(zip(rows, colors)):
    g.add(Text(s, font_size=FS_BODY, color=c).move_to([PX + 0.42, y0 - dy * k, 0],
                                                      aligned_edge=LEFT))
   return g

  def _mark(y0=0.95, dy=0.72, period=2.4):
   return always_redraw(lambda: Dot(
    [PX, y0 - dy * (int(self._tau() / period) % 3), 0], color=INK, radius=0.085))
  rows3 = _cyc(["1 :   Ω₂ V₃ − Ω₃ V₂", "2 :   Ω₃ V₁ − Ω₁ V₃", "3 :   Ω₁ V₂ − Ω₂ V₁"],
               [ACCENT_A, ACCENT_B, ACCENT_C])
  mark3 = _mark()
  cap3 = self._row(-1.25, "指標 1 → 2 → 3 → 1 輪換", "the indices cycle 1 → 2 → 3 → 1", DIM)
  rows4 = _cyc(["( I₃ − I₂ ) Ω₂ Ω₃", "( I₁ − I₃ ) Ω₃ Ω₁", "( I₂ − I₁ ) Ω₁ Ω₂"],
               [ACCENT_A, ACCENT_B, ACCENT_C])
  mark4 = _mark()
  cap4 = VGroup(self._row(-1.25, "這三個就是 ( Ω × M )ᵢ",
                          "these three are ( Ω × M )ᵢ", WARN, FS_BODY))
  mxm = always_redraw(lambda: self._arr(
   O3, _p(0.90 * _unit(np.cross(om0, m0))), WARN, sw=5, tl=0.18))
  mxmt = Text("Ω × M", font_size=FS_SMALL, color=WARN).move_to(
   _p(0.90 * _unit(np.cross(om0, m0))) + np.array([0.20, -0.30, 0]))

  # ══ beats 5-9: free rotation ══════════════════════════════════════
  polc = self._curve([OS * q for q in POL[:6000]], GHOST, sw=2.5)
  omv5 = always_redraw(lambda: self._arr(O3, _p(OS * self._om()), ACCENT_C, sw=6, tl=0.22))
  omt5 = self._tag("Ω", lambda: _p(OS * self._om()), off=np.array([0.24, 0.16, 0]),
                   color=ACCENT_C)
  tip5 = always_redraw(lambda: Dot(_p(OS * self._om()), color=WARN, radius=0.075))
  cap5 = VGroup(self._row(0.95, "I₁ ≠ I₂ ≠ I₃", "I₁ ≠ I₂ ≠ I₃", INK, FS_BODY),
                self._row(0.25, "Ω 的軌跡是一條閉曲線", "Ω traces a closed curve", DIM),
                self._row(-0.45, "三個分量彼此耦合", "the three components are coupled", DIM))

  rim6 = DashedVMobject(self._ring(E1, E2, OS * AMP, GHOST, sw=3, at=OS * OM3 * E3),
                        num_dashes=40, color=GHOST)
  om3v = self._arr(O3, _p(OS * OM3 * E3), ACCENT_B, sw=5, tl=0.18)
  om3t = Text("Ω₃", font_size=FS_SMALL, color=ACCENT_B).move_to(
   _p(OS * OM3 * E3) + np.array([-0.30, 0.06, 0]))
  perp6 = always_redraw(lambda: self._dash(_p(OS * OM3 * E3), _p(OS * self._om()),
                                           ACCENT_A, n=8))
  cap6 = VGroup(self._row(0.95, "I₁ = I₂", "I₁ = I₂", INK, FS_BODY),
                self._row(0.25, "第三條方程的乘積項消失",
                          "the product term in the third drops out", DIM),
                self._row(-0.45, "Ω₃ 是常數", "Ω₃ is constant", ACCENT_B, FS_BODY))

  # the (Omega_1, Omega_2) plane
  QC = np.array([4.15, 0.05, 0.0]); QS = 1.15
  quad = VGroup(Line(QC + np.array([-1.5, 0, 0]), QC + np.array([1.5, 0, 0]),
                     color=GHOST, stroke_width=2),
                Line(QC + np.array([0, -1.5, 0]), QC + np.array([0, 1.5, 0]),
                     color=GHOST, stroke_width=2),
                Text("Ω₁", font_size=FS_SMALL, color=DIM).move_to(QC + np.array([1.68, -0.16, 0])),
                Text("Ω₂", font_size=FS_SMALL, color=DIM).move_to(QC + np.array([-0.20, 1.62, 0])),
                DashedVMobject(VMobject(color=GHOST, stroke_width=2.5).set_points_as_corners(
                 [QC + QS * AMP * np.array([np.cos(a), np.sin(a), 0])
                  for a in np.linspace(0, 2 * PI, 80)]), num_dashes=48, color=GHOST),
                always_redraw(lambda: self._arr(
                 QC, QC + QS * np.array([self._oms()[0], self._oms()[1], 0.0]), ACCENT_A, sw=5)),
                always_redraw(lambda: Dot(
                 QC + QS * np.array([self._oms()[0], self._oms()[1], 0.0]),
                 color=WARN, radius=0.08)))
  # No caption above the plane: the Ω₂ axis label already sits at y ≈ 1.67.
  cap7 = VGroup(self._row(-1.45, "A = √( Ω₁² + Ω₂² ) 固定", "A = √( Ω₁² + Ω₂² ) is fixed",
                          WARN, x=2.70))

  # the two sinusoids
  WC8 = np.array([3.95, -0.05, 0.0]); WW = 2.15; WH = 0.62; WT = 2 * PI / WOM

  def _wave(fn, color):
   pts = [WC8 + np.array([WW * (2 * s - 1), WH * fn(2 * PI * s), 0])
          for s in np.linspace(0, 1, 140)]
   m = VMobject(color=color, stroke_width=4); m.set_points_as_corners(pts); return m

  def _wdot(fn, color):
   def _q():
    s = (self._tau() % WT) / WT
    return WC8 + np.array([WW * (2 * s - 1), WH * fn(2 * PI * s), 0])
   return always_redraw(lambda: Dot(_q(), color=color, radius=0.08))
  waves = VGroup(Line(WC8 + np.array([-WW, 0, 0]), WC8 + np.array([WW, 0, 0]),
                      color=GHOST, stroke_width=2),
                 _wave(np.cos, ACCENT_A), _wave(np.sin, ACCENT_B),
                 _wdot(np.cos, ACCENT_A), _wdot(np.sin, ACCENT_B),
                 Text("Ω₁ = A cos ωt", font_size=FS_SMALL, color=ACCENT_A)
                 .move_to(WC8 + np.array([-0.55, 1.15, 0])),
                 Text("Ω₂ = A sin ωt", font_size=FS_SMALL, color=ACCENT_B)
                 .move_to(WC8 + np.array([-0.55, -1.15, 0])))

  trail = always_redraw(lambda: self._curve(
   [np.array([OS * AMP * np.cos(WOM * s), OS * AMP * np.sin(WOM * s), OS * OM3])
    for s in np.linspace(max(0.0, self._tau() - WT), self._tau() + 1e-3, 48)], ACCENT_C, sw=3))
  cap9 = VGroup(self._row(0.95, "在物體座標系裡：Ω 繞 x₃ 轉",
                          "body frame: Ω turns about x₃", ACCENT_C, FS_BODY),
                self._row(0.25, "M 因為 Mᵢ = Iᵢ Ωᵢ，做同樣的運動",
                          "M does the same, since Mᵢ = Iᵢ Ωᵢ", ACCENT_B),
                self._row(-0.45, "在固定座標系裡（第 33 課）：x₃ 繞 M 轉",
                          "fixed frame, lesson 33: x₃ about M", DIM),
                self._row(-1.15, "同一個運動的兩種看法",
                          "two views of one motion", INK, FS_BODY))

  # ── run the beats ─────────────────────────────────────────────────
  active_sub = None; active_f = None

  def run(i, mode, fin=(), fout=()):
   nonlocal active_sub, active_f
   self.mode = mode; self.t0 = self.t.get_value()
   s = self.sub(self.lines[i]); fin = list(fin) + [s]; fout = list(fout)
   if active_sub is not None: fout.append(active_sub)
   lang = "zh" if self.LANGUAGE == "zh" else "en"
   bits = []
   if i in self.MODE_LABEL: bits.append(self.MODE_LABEL[i][lang])
   if i in F: bits.append(F[i])
   if bits:
    f = self.formula("\n".join(bits)); fin.append(f)
    if active_f is not None: fout.append(active_f)
    active_f = f
   self.beat(i, fin=fin, fout=fout)
   active_sub = s

  self.add(axes)
  run(0, 0, fin=[pair0, cap0])
  run(1, 1, fin=[cone, cap1], fout=[pair0, cap0, axes])
  run(2, 2, fin=[tri, cap2], fout=[cap1])
  run(3, 3, fin=[axes, rows3, mark3, cap3], fout=[cone, tri, cap2])
  run(4, 4, fin=[pair0, mxm, mxmt, rows4, mark4, cap4], fout=[rows3, mark3, cap3])
  run(5, 5, fin=[polc, omv5, omt5, tip5, cap5],
      fout=[pair0, mxm, mxmt, rows4, mark4, cap4])
  run(6, 6, fin=[rim6, om3v, om3t, perp6, cap6], fout=[polc, cap5])
  run(7, 7, fin=[quad, cap7], fout=[cap6, om3t, perp6])
  run(8, 8, fin=[waves], fout=[quad, cap7])
  run(9, 9, fin=[trail, cap9], fout=[waves, om3v])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL36{'ZH' if lang == 'zh' else 'EN'}", (EulerEqBase,), {"LANGUAGE": lang})


LandauL36ZH = _mk("zh")
LandauL36EN = _mk("en")
