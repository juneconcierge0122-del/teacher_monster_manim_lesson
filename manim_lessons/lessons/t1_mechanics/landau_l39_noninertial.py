"""Lesson 39 — Motion in a non-inertial frame (Landau §39).

Two demonstrations carry the lesson. A pendulum in an accelerating carriage
hangs along the effective gravity g minus W, which is the whole content of
(39.5). Then a puck is launched across a turntable: the same motion is drawn
twice, straight in the inertial frame and curved in the rotating one, with the
curve produced by transforming the straight path rather than by any fudge.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (Arrow, Circle, Dot, FadeIn, FadeOut, Line, Rectangle, Text, VGroup, VMobject,
                   DashedVMobject, ValueTracker, always_redraw, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19
PX = 1.55

# ── beats 8-9: the turntable ──────────────────────────────────────────
TL = np.array([-3.55, -0.25, 0.0])          # inertial view centre
TR = np.array([2.95, -0.25, 0.0])           # rotating view centre
TRAD = 1.35                                 # disc radius
WSPIN = 0.55                                # angular velocity of the disc
TFLY = 4.6                                  # time for the puck to cross
P0 = np.array([0.0, -1.28, 0.0])            # launch point, in disc coordinates
PV = np.array([0.0, 2.0 * 1.28 / 4.6, 0.0])  # straight-line velocity, crosses in TFLY


def _rot2(v, a):
 c, s = np.cos(a), np.sin(a)
 return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


class NonInertialBase(LandauBatchBase):
 EPISODE = 39; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "到目前為止都在慣性系裡", "en": "so far, always an inertial frame"},
               1: {"zh": "最小作用量原理不在乎座標系",
                   "en": "least action does not care about the frame"},
               2: {"zh": "第一步：平移的參考系", "en": "step one: a translating frame"},
               3: {"zh": "全微分可以直接丟掉", "en": "total derivatives may simply be dropped"},
               4: {"zh": "加速度等效於一個均勻力場",
                   "en": "acceleration acts like a uniform force field"},
               5: {"zh": "第二步：轉動的參考系", "en": "step two: a rotating frame"},
               6: {"zh": "多出一項與速度成一次的項",
                   "en": "a term linear in the velocity appears"},
               7: {"zh": "三個慣性力", "en": "three inertia forces"},
               8: {"zh": "科氏力：直線看起來會彎",
                   "en": "Coriolis: a straight line looks curved"},
               9: {"zh": "離心力：背離轉軸", "en": "centrifugal: straight away from the axis"}}

 # ── helpers ───────────────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _arr(self, s, t, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(t) - np.asarray(s))) < 0.05: return VGroup()
  return Arrow(s, t, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _dash(self, a, b, color, n=12, sw=2.5):
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  """A panel row, shrunk if it would run past the safe right edge."""
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > 6.30:
   m.scale_to_fit_width(6.30 - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 def _mid(self, y, zh, en, color=DIM, size=FS_SMALL, x=0.0):
  m = self.lab(zh, en, size, color).move_to([x, y, 0])
  if m.width > 12.0: m.scale_to_fit_width(12.0).move_to([x, y, 0])
  return m

 def _curve(self, pts, color, sw=3):
  m = VMobject(color=color, stroke_width=sw); m.set_points_as_corners(list(pts)); return m

 def _tau(self):
  return self.t.get_value() - self.t0

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

 # ── the turntable ─────────────────────────────────────────────────
 def _fly(self):
  """Puck position in disc coordinates, and the disc angle, at this instant."""
  s = self._tau() % (TFLY + 1.1)
  s = min(s, TFLY)
  return P0 + PV * s, WSPIN * self._tau()

 def _disc(self, centre, ang, color=DIM):
  g = VGroup(Circle(radius=TRAD, color=color, stroke_width=3).move_to(centre))
  for k in range(6):
   d = _rot2(np.array([1.0, 0.0, 0.0]), ang + k * PI / 3)
   g.add(Line(centre, centre + TRAD * d, color=GHOST, stroke_width=2))
  g.add(Dot(centre, color=color, radius=0.055))
  return g

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ beats 0-1: the inertial frame ═════════════════════════════════
  IC = np.array([-3.40, -0.20, 0.0])
  frame0 = VGroup(self._arr(IC, IC + np.array([1.50, 0, 0]), DIM, sw=4, tl=0.16),
                  self._arr(IC, IC + np.array([0, 1.30, 0]), DIM, sw=4, tl=0.16),
                  Text("K₀", font_size=FS_TAG, color=DIM).move_to(IC + np.array([-0.34, 1.24, 0])),
                  Dot(IC, color=INK, radius=0.06))
  pdot = always_redraw(lambda: Dot(IC + np.array([0.30 + 0.42 * self._tau() % 1.6, 0.70, 0]),
                                   color=ACCENT_A, radius=0.10))
  parr = always_redraw(lambda: self._arr(
   IC + np.array([0.30 + 0.42 * self._tau() % 1.6, 0.70, 0]),
   IC + np.array([0.30 + 0.42 * self._tau() % 1.6, 0.70, 0]) + np.array([0.80, 0, 0]),
   ACCENT_C, sw=4, tl=0.16))
  cap0 = VGroup(self._row(0.90, "慣性系 K₀ 裡的拉格朗日量", "in an inertial frame K₀", DIM),
                self._row(0.20, "L₀ = ½ m v₀² − U", "L₀ = ½ m v₀² − U", ACCENT_A, FS_BODY),
                self._row(-0.50, "運動方程只在這裡成立",
                          "the equation of motion holds only here", WARN))
  cap1 = VGroup(self._row(0.90, "最小作用量原理與座標系無關",
                          "least action is frame-independent", ACCENT_B, FS_BODY),
                self._row(0.20, "拉格朗日方程照樣成立",
                          "Lagrange's equations still hold", DIM),
                self._row(-0.50, "只有 L 本身要改寫", "only L itself must be rewritten", WARN,
                          FS_BODY))

  # ══ beats 2-4: the accelerating carriage ══════════════════════════
  CC = np.array([-3.20, -0.30, 0.0])
  car = Rectangle(width=2.90, height=1.85, color=DIM, stroke_width=3).move_to(CC)
  wheels = VGroup(*[Circle(radius=0.20, color=GHOST, stroke_width=3)
                    .move_to(CC + np.array([dx, -1.12, 0])) for dx in (-0.85, 0.85)])
  piv = CC + np.array([0.0, 0.80, 0.0])
  WACC = 0.62                                       # frame acceleration, in units of g
  tilt = np.arctan(WACC)
  # the carriage accelerates to the +x side, so g − W tilts back to −x
  bobd = np.array([-np.sin(tilt), -np.cos(tilt), 0.0])
  rod = Line(piv, piv + 1.15 * bobd, color=ACCENT_A, stroke_width=4)
  bob = Dot(piv + 1.15 * bobd, color=ACCENT_A, radius=0.14)
  vert = self._dash(piv, piv + np.array([0.0, -1.15, 0.0]), GHOST, n=8)
  bp = piv + 1.15 * bobd
  eff = VGroup(self._arr(bp, bp + np.array([0.0, -0.85, 0]), ACCENT_B, sw=5),
               Text("g", font_size=FS_SMALL, color=ACCENT_B)
               .move_to(bp + np.array([-0.24, -0.92, 0])),
               self._arr(bp, bp + np.array([-0.85 * WACC, 0.0, 0]), WARN, sw=5),
               Text("− W", font_size=FS_SMALL, color=WARN)
               .move_to(bp + np.array([-0.85 * WACC - 0.32, 0.20, 0])),
               self._dash(bp + np.array([0.0, -0.85, 0]),
                          bp + np.array([-0.85 * WACC, -0.85, 0]), GHOST, n=6),
               self._dash(bp + np.array([-0.85 * WACC, 0.0, 0]),
                          bp + np.array([-0.85 * WACC, -0.85, 0]), GHOST, n=6))
  wacc = VGroup(self._arr(CC + np.array([-0.20, 1.28, 0]), CC + np.array([1.10, 1.28, 0]),
                          ACCENT_C, sw=6),
                Text("W", font_size=FS_TAG, color=ACCENT_C).move_to(CC + np.array([1.34, 1.28, 0])))
  carriage = VGroup(car, wheels, wacc, vert, rod, bob)
  cap2 = VGroup(self._row(0.90, "K′ 相對 K₀ 以 V(t) 平移",
                          "K′ translates with V(t)", DIM, FS_BODY),
                self._row(0.20, "速度差一個 V", "the velocities differ by V", DIM),
                self._row(-0.50, "代進去就多出兩項", "substituting adds two terms", ACCENT_C))
  cap3 = VGroup(self._row(0.90, "½ m V² 只依賴時間", "½ m V² depends on time only", DIM),
                self._row(0.20, "m V · v′ 拆成全微分 + 加速度項",
                          "m V · v′ splits into a derivative plus W", DIM),
                self._row(-0.50, "全微分不改變運動方程",
                          "total derivatives change nothing", ACCENT_B))
  cap4 = VGroup(self._row(0.90, "等效於一個均勻力場", "equivalent to a uniform field", WARN,
                          FS_BODY),
                self._row(0.20, "大小 m W，方向相反", "of size m W, pointing the other way",
                          WARN),
                self._row(-0.50, "擺就沿著 g − W 的方向掛著",
                          "the pendulum hangs along g − W", ACCENT_A))

  # ══ beats 5-7: the rotating frame ═════════════════════════════════
  RC = np.array([-3.30, -0.25, 0.0])
  # beat 5 carries a three-line formula, whose block reaches down to y = 1.40,
  # so the spin arrow and its label have to stay below that.
  rot5 = VGroup(Circle(radius=1.30, color=GHOST, stroke_width=2).move_to(RC),
                Dot(RC, color=INK, radius=0.06),
                self._arr(RC, RC + np.array([0.0, 1.35, 0]), ACCENT_C, sw=5),
                Text("Ω", font_size=FS_TAG, color=ACCENT_C).move_to(RC + np.array([0.30, 1.28, 0])))
  rvec = always_redraw(lambda: self._arr(
   RC, RC + 1.15 * _rot2(np.array([1.0, 0.0, 0.0]), 0.45 * self._tau()), ACCENT_A, sw=5))
  rtag = always_redraw(lambda: Text("r", font_size=FS_SMALL, color=ACCENT_A).move_to(
   RC + 1.38 * _rot2(np.array([1.0, 0.0, 0.0]), 0.45 * self._tau())))
  rcross = always_redraw(lambda: self._arr(
   RC + 1.15 * _rot2(np.array([1.0, 0.0, 0.0]), 0.45 * self._tau()),
   RC + 1.15 * _rot2(np.array([1.0, 0.0, 0.0]), 0.45 * self._tau())
   + 0.72 * _rot2(np.array([0.0, 1.0, 0.0]), 0.45 * self._tau()), WARN, sw=4, tl=0.16))
  ctag = self.lab("Ω × r", "Ω × r", FS_SMALL, WARN).move_to(RC + np.array([1.05, -1.55, 0]))
  cap5 = VGroup(self._row(0.90, "K 與 K′ 同原點，以 Ω 轉動",
                          "K shares the origin and turns with Ω", DIM),
                self._row(0.20, "v′ = v + Ω × r", "v′ = v + Ω × r", ACCENT_B, FS_BODY),
                self._row(-0.50, "得到任意參考系的 L",
                          "giving L for any frame at all", ACCENT_A))
  cap6 = VGroup(self._row(0.90, "m v · ( Ω × r )", "m v · ( Ω × r )", WARN, FS_BODY),
                self._row(0.20, "與速度成一次的項", "linear in the velocity", WARN),
                self._row(-0.50, "以前的 L 從來沒有這種項",
                          "no earlier Lagrangian had one", DIM))
  cap7 = VGroup(self._row(0.90, "m r × dΩ/dt：轉動不均勻才有",
                          "m r × dΩ/dt: only if Ω changes", ACCENT_C),
                self._row(0.20, "2 m v × Ω：科氏力", "2 m v × Ω: the Coriolis force", WARN,
                          FS_BODY),
                self._row(-0.50, "m Ω × ( r × Ω )：離心力",
                          "m Ω × ( r × Ω ): centrifugal", ACCENT_B, FS_BODY),
                self._row(-1.20, "後兩個即使等速轉動也存在",
                          "the last two survive a steady rotation", DIM))

  # ══ beat 8: the turntable, both views ═════════════════════════════
  discL = always_redraw(lambda: self._disc(TL, self._fly()[1]))
  discR = self._disc(TR, 0.0)
  trailL = self._curve([TL + P0 + PV * s for s in np.linspace(0, TFLY, 40)], ACCENT_B, sw=3)
  trailR = self._curve([TR + _rot2(P0 + PV * s, -WSPIN * s)
                        for s in np.linspace(0, TFLY, 90)], WARN, sw=3)
  puckL = always_redraw(lambda: Dot(TL + self._fly()[0], color=ACCENT_B, radius=0.10))
  puckR = always_redraw(lambda: Dot(TR + _rot2(self._fly()[0], -self._fly()[1]),
                                    color=WARN, radius=0.10))
  lab8 = VGroup(self.lab("慣性系：直線", "inertial frame: a straight line", FS_BODY, ACCENT_B)
                .move_to(TL + np.array([0.0, 1.72, 0])),
                self.lab("轉動系：彎曲", "rotating frame: it curves", FS_BODY, WARN)
                .move_to(TR + np.array([0.0, 1.72, 0])),
                self._mid(-1.62, "同一個運動，兩種座標系", "one motion, two frames", DIM))
  turn = VGroup(discL, discR, trailL, trailR, puckL, puckR, lab8)

  # ══ beat 9: centrifugal ═══════════════════════════════════════════
  CF = np.array([-3.30, -0.25, 0.0])
  axl = Line(CF + np.array([0, -1.45, 0]), CF + np.array([0, 1.55, 0]), color=ACCENT_C,
             stroke_width=4)
  pp = CF + np.array([1.05, 0.45, 0.0])
  cent = VGroup(axl, Text("Ω", font_size=FS_TAG, color=ACCENT_C)
                .move_to(CF + np.array([-0.28, 1.48, 0])),
                self._arr(CF, pp, ACCENT_A, sw=4),
                Text("r", font_size=FS_SMALL, color=ACCENT_A).move_to(CF + np.array([0.44, 0.42, 0])),
                Dot(pp, color=ACCENT_A, radius=0.10),
                self._dash(CF + np.array([0.0, 0.45, 0]), pp, GHOST, n=7),
                Text("ρ", font_size=FS_SMALL, color=DIM).move_to(CF + np.array([0.52, 0.66, 0])),
                self._arr(pp, pp + np.array([1.15, 0.0, 0]), WARN, sw=6),
                Text("m ρ Ω²", font_size=FS_SMALL, color=WARN)
                .move_to(pp + np.array([1.30, 0.28, 0])))
  cap9 = VGroup(self._row(0.90, "位於 r 與 Ω 張成的平面內",
                          "in the plane of r and Ω", DIM),
                self._row(0.20, "垂直於轉軸，方向背離它",
                          "perpendicular to the axis, pointing out", ACCENT_B),
                self._row(-0.50, "大小 = m ρ Ω²", "magnitude m ρ Ω²", WARN, FS_BODY))

  # ── run ───────────────────────────────────────────────────────────
  active_sub = None; active_f = None

  def run(i, fin=(), fout=()):
   nonlocal active_sub, active_f
   self.t0 = self.t.get_value()
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

  run(0, fin=[frame0, pdot, parr, cap0])
  run(1, fin=[cap1], fout=[cap0])
  run(2, fin=[carriage, cap2], fout=[frame0, pdot, parr, cap1])
  run(3, fin=[cap3], fout=[cap2])
  run(4, fin=[eff, cap4], fout=[cap3])
  run(5, fin=[rot5, rvec, rtag, rcross, ctag, cap5], fout=[carriage, eff, cap4])
  run(6, fin=[cap6], fout=[cap5])
  run(7, fin=[cap7], fout=[cap6])
  run(8, fin=[turn], fout=[rot5, rvec, rtag, rcross, ctag, cap7])
  run(9, fin=[cent, cap9], fout=[turn])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL39{'ZH' if lang == 'zh' else 'EN'}", (NonInertialBase,),
             {"LANGUAGE": lang})


LandauL39ZH = _mk("zh")
LandauL39EN = _mk("en")
