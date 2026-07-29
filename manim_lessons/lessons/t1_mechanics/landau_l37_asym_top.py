"""Lesson 37 — The asymmetrical top (Landau §37).

The whole lesson lives on one picture: the energy ellipsoid in M-space, the
sphere of constant |M|, and the family of curves they cut out — Landau's
Fig. 51. Every curve is obtained by integrating the torque-free equation
dM/dt = M x Omega once at import time, so the polhodes, the separatrix through
the middle axis and the diverging path that demonstrates its instability are
all the real trajectories. Beats 6-9 read the same integration as the Jacobian
functions cn, sn and dn, and watch them degenerate to cos, sin and 1.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (Arrow, Dot, FadeIn, FadeOut, Line, Text, VGroup, VMobject, DashedVMobject,
                   ValueTracker, always_redraw, linear, DOWN, LEFT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19
EX = np.array([0.80, -0.42, 0.0]); EY = np.array([-0.66, -0.34, 0.0]); EZ = np.array([0.0, 1.0, 0.0])
ORG = np.array([-2.35, -0.62, 0.0]); PS = 1.10; MS = 0.95   # M-space -> 3D units

II = np.array([1.00, 1.60, 2.50])           # I1 < I2 < I3
E2 = 1.0                                    # 2E
SEMI = np.sqrt(E2 * II)                     # ellipsoid semiaxes in M-space
# the meridian angle at which |M|^2 crosses 2E*I2, i.e. the separatrix
TH_SEP = float(np.arcsin(np.sqrt((SEMI[2] ** 2 - SEMI[1] ** 2) /
                                 (SEMI[2] ** 2 - SEMI[0] ** 2))))
FAMILY = [0.26, 0.52, 0.78, 1.02, 1.24, 1.42]               # polar angles, radians
PX = 1.50
SPD = 1.8                                   # playback speed along a trajectory

# At M² = 2E I₂ the two quadrics reduce to M₁²(1/a₁² − 1/a₂²) = M₃²(1/a₂² − 1/a₃²),
# so the separatrix is two great circles of the sphere, in the planes M₃ = ±c M₁.
_CSEP = float(np.sqrt((1 / SEMI[0] ** 2 - 1 / SEMI[1] ** 2) /
                      (1 / SEMI[1] ** 2 - 1 / SEMI[2] ** 2)))


def _unit(v):
 n = float(np.linalg.norm(v))
 return np.asarray(v, dtype=float) / (n if n > 1e-9 else 1.0)


def _p(v):
 v = MS * np.asarray(v, dtype=float)
 return ORG + PS * (float(v[0]) * EX + float(v[1]) * EY + float(v[2]) * EZ)


def _dM(m):
 """Torque-free motion in the body frame: dM/dt = M x Omega, Omega_i = M_i / I_i."""
 w = m / II
 return np.cross(m, w)


def _track(m0, n, dt):
 out = np.empty((n, 3)); m = np.asarray(m0, dtype=float).copy()
 for i in range(n):
  out[i] = m
  k1 = _dM(m); k2 = _dM(m + 0.5 * dt * k1); k3 = _dM(m + 0.5 * dt * k2); k4 = _dM(m + dt * k3)
  m = m + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
 return out


def _closed(th, dt=0.006, nmax=9000):
 """One full closed polhode starting from the M2 = 0 meridian at polar angle th."""
 m0 = np.array([SEMI[0] * np.sin(th), 0.0, SEMI[2] * np.cos(th)])
 tr = _track(m0, nmax, dt)
 d = np.linalg.norm(tr - tr[0], axis=1); r0 = float(np.linalg.norm(tr[0]))
 idx = np.nonzero(d > 0.25 * r0)[0]
 if len(idx) == 0: return tr, nmax * dt
 far = int(idx[0]) + 200                              # leave the start well behind
 if far >= nmax: return tr, nmax * dt
 back = int(np.argmin(d[far:])) + far
 if d[back] > 0.05 * r0: return tr, nmax * dt         # never came back
 return tr[:back + 1], (back + 1) * dt


def _sep():
 """The separatrix: two great circles of the sphere |M| = √(2E I₂)."""
 out = []
 for sgn in (1.0, -1.0):
  u = _unit(np.array([1.0, 0.0, sgn * _CSEP])); v = np.array([0.0, 1.0, 0.0])
  out.append([SEMI[1] * (np.cos(a) * u + np.sin(a) * v) for a in np.linspace(0, 2 * PI, 96)])
 return out


CURVES = [_closed(t)[0] for t in FAMILY]
SEP = _sep()
# Must be a loop about x3, i.e. M^2 > 2E*I2. Landau's (37.10) assume that; on a
# loop about x1 the roles of the suffixes 1 and 3 swap and Omega_1, not Omega_3,
# is the one that never changes sign.
SHOW = 1                                    # the curve followed in beats 2, 4, 6-9
TRACK, TPER = _closed(FAMILY[SHOW])         # its period, for the waveform panel
# beat 5: a path that starts a hair off the middle axis and wanders far
NEAR2 = _track(np.array([0.045, SEMI[1] * 0.9988, 0.045]), 5200, 0.006)
NEAR1 = _track(np.array([SEMI[0] * 0.995, 0.075, 0.055]), 5200, 0.006)


class AsymTopBase(LandauBatchBase):
 EPISODE = 37; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "三個主慣量都不同，而且沒有外力矩",
                   "en": "three different moments, and no torque"},
               1: {"zh": "能量給橢球面，角動量給球面",
                   "en": "energy gives an ellipsoid, M gives a sphere"},
               2: {"zh": "M 的尖端走在兩個面的交線上",
                   "en": "the tip of M runs along their intersection"},
               3: {"zh": "固定能量、改變 M：一整族路徑",
                   "en": "fixed energy, varying M: a family of paths"},
               4: {"zh": "路徑封閉 ⇒ 相對於物體是週期運動",
                   "en": "closed paths, so the motion is periodic"},
               5: {"zh": "中間那根軸不穩定", "en": "the middle axis is unstable"},
               6: {"zh": "用兩個守恆律消掉兩個分量",
                   "en": "two conservation laws remove two components"},
               7: {"zh": "積出來是橢圓積分", "en": "the integral is an elliptic one"},
               8: {"zh": "三個雅可比橢圓函數", "en": "three Jacobian elliptic functions"},
               9: {"zh": "兩個主慣量相等時退化回對稱陀螺",
                   "en": "equal moments bring back the symmetrical top"}}

 # ── helpers ───────────────────────────────────────────────────────
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

 def _curve(self, pts, color, sw=3, maxn=170):
  """Draw a trajectory, thinned first: the integrations run to several thousand
  steps, and handing that many corners to a VMobject makes rendering crawl."""
  pts = np.asarray(pts, dtype=float)
  if len(pts) > maxn:
   pts = pts[np.linspace(0, len(pts) - 1, maxn).astype(int)]
  m = VMobject(color=color, stroke_width=sw)
  m.set_points_as_corners([_p(q) for q in pts]); return m

 def _both(self, pts, color, sw=3):
  """A polhode and its antipodal twin — the two loops of Landau's Fig. 51."""
  return VGroup(self._curve(pts, color, sw), self._curve(-np.asarray(pts), color, sw))

 def _ell_wire(self, color=GHOST, sw=2):
  g = VGroup()
  for th in np.linspace(0.001, PI - 0.001, 5):                      # latitudes
   g.add(self._curve([SEMI * np.array([np.sin(th) * np.cos(a), np.sin(th) * np.sin(a),
                                       np.cos(th)]) for a in np.linspace(0, 2 * PI, 56)],
                     color, sw))
  for ph in np.linspace(0, PI, 4, endpoint=False):                  # meridians
   g.add(self._curve([SEMI * np.array([np.sin(t) * np.cos(ph), np.sin(t) * np.sin(ph),
                                       np.cos(t)]) for t in np.linspace(0, 2 * PI, 56)],
                     color, sw))
  return g

 def _sphere(self, r, color=ACCENT_B, sw=2.5):
  g = VGroup()
  for th in (0.62, PI / 2, PI - 0.62):
   g.add(self._curve([r * np.array([np.sin(th) * np.cos(a), np.sin(th) * np.sin(a),
                                    np.cos(th)]) for a in np.linspace(0, 2 * PI, 56)],
                     color, sw))
  g.add(self._curve([r * np.array([np.cos(a), 0.0, np.sin(a)])
                     for a in np.linspace(0, 2 * PI, 56)], color, sw))
  return g

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  return self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)

 def _txt(self, y, s, color=INK, size=FS_BODY, x=PX):
  return Text(s, font_size=size, color=color).move_to([x, y, 0], aligned_edge=LEFT)

 def _tau(self):
  return self.t.get_value() - self.t0

 def _at(self, tr, speed=SPD):
  i = int(self._tau() * speed / 0.006) % len(tr)
  return tr[i]

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
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)
  O3 = _p(np.zeros(3))

  axes = VGroup(
   *[self._arr(O3, _p(1.12 * SEMI[k] * e), ACCENT_A, sw=4, tl=0.16)
     for k, e in enumerate((np.array([1., 0, 0]), np.array([0, 1., 0]), np.array([0, 0, 1.])))],
   Text("x₁", font_size=FS_SMALL, color=ACCENT_A)
   .move_to(_p(1.22 * SEMI[0] * np.array([1., 0, 0])) + np.array([0.18, -0.14, 0])),
   Text("x₂", font_size=FS_SMALL, color=ACCENT_A)
   .move_to(_p(1.22 * SEMI[1] * np.array([0, 1., 0])) + np.array([-0.20, -0.14, 0])),
   Text("x₃", font_size=FS_SMALL, color=ACCENT_A)
   .move_to(_p(1.12 * SEMI[2] * np.array([0, 0, 1.])) + np.array([0.26, 0.02, 0])),
   Dot(O3, color=INK, radius=0.06))

  # ══ beats 0-2: the two surfaces ═══════════════════════════════════
  cap0 = VGroup(self._row(0.95, "I₃ > I₂ > I₁", "I₃ > I₂ > I₁", INK, FS_BODY),
                self._row(0.25, "能量守恆", "energy is conserved", ACCENT_A),
                self._row(-0.35, "角動量的大小守恆", "the magnitude of M is conserved", ACCENT_B),
                self._row(-1.10, "兩個守恆律，三個未知數",
                          "two integrals, three unknowns", DIM))
  ell = self._ell_wire()
  RAD = float(np.linalg.norm(CURVES[SHOW][0]))
  sph = self._sphere(RAD)
  cap1 = VGroup(self._row(0.95, "橢球：半軸 √( 2E Iᵢ )", "ellipsoid: semiaxes √( 2E Iᵢ )",
                          DIM, FS_BODY),
                self._row(0.25, "球面：半徑 M", "sphere: radius M", ACCENT_B, FS_BODY))
  inter = self._both(CURVES[SHOW], WARN, sw=4)
  mdot = always_redraw(lambda: Dot(_p(self._at(TRACK)), color=WARN, radius=0.085))
  marr = always_redraw(lambda: self._arr(O3, _p(self._at(TRACK)), ACCENT_B, sw=5, tl=0.18))
  mtag = self._tag("M", lambda: _p(self._at(TRACK)), off=np.array([0.24, 0.16, 0]),
                   color=ACCENT_B)
  cap2 = VGroup(self._row(-0.45, "交線就是 M 的路徑", "their intersection: the path of M",
                          WARN, FS_BODY),
                self._row(-1.15, "√( 2E I₁ )  <  M  <  √( 2E I₃ )",
                          "√( 2E I₁ )  <  M  <  √( 2E I₃ )", DIM))

  # ══ beat 3: the whole family ══════════════════════════════════════
  fam = VGroup(*[self._both(c, ACCENT_C, sw=2.5) for c in CURVES],
               *[self._curve(c, WARN, sw=4) for c in SEP])
  cap3 = VGroup(self._row(0.95, "M 小：繞 x₁ 的小圈", "small M: little loops about x₁",
                          ACCENT_C),
                self._row(0.25, "M² = 2E I₂：兩條平面曲線",
                          "M² = 2E I₂: two plane curves", WARN, FS_BODY),
                self._row(-0.45, "M 大：繞 x₃ 的小圈", "large M: little loops about x₃",
                          ACCENT_C),
                self._row(-1.15, "這些就叫 polhode", "these curves are the polhodes", DIM))

  # ══ beat 4: closed, hence periodic ════════════════════════════════
  fan = always_redraw(lambda: VGroup(*[
   Line(O3, _p(TRACK[int((self._tau() * SPD / 0.006 - j * 40) % len(TRACK))]),
        color=ACCENT_C, stroke_width=1.6) for j in range(14)]))
  cap4 = VGroup(self._row(0.95, "走完一圈回到原處", "one circuit and it is back", INK, FS_BODY),
                self._row(0.25, "掃出一個錐面", "sweeping out a cone", ACCENT_C),
                self._row(-0.45, "M ( t + T ) = M ( t )", "M ( t + T ) = M ( t )", WARN,
                          FS_BODY))

  # ══ beat 5: stability ═════════════════════════════════════════════
  p1 = self._curve(NEAR1, ACCENT_B, sw=3)
  p2 = self._curve(NEAR2, WARN, sw=3)
  d1 = always_redraw(lambda: Dot(_p(self._at(NEAR1)), color=ACCENT_B, radius=0.08))
  d2 = always_redraw(lambda: Dot(_p(self._at(NEAR2)), color=WARN, radius=0.08))
  cap5 = VGroup(self._row(0.95, "從 x₁ 附近出發：一直待在附近",
                          "started near x₁: it stays near", ACCENT_B),
                self._row(0.25, "從 x₂ 附近出發：跑得很遠",
                          "started near x₂: it runs far away", WARN),
                self._row(-0.45, "x₁ 與 x₃ 穩定", "x₁ and x₃ are stable", ACCENT_B, FS_BODY),
                self._row(-1.15, "x₂ 不穩定", "x₂ is unstable", WARN, FS_BODY))

  # ══ beats 6-9: the elliptic functions ═════════════════════════════
  WC = np.array([3.95, 0.10, 0.0]); WW = 2.20; WH = 0.62
  SC = np.abs(TRACK / II).max()

  def _wave(k, color):
   pts = [WC + np.array([WW * (2 * s - 1), WH * TRACK[int(s * (len(TRACK) - 1))][k] / II[k] / SC,
                         0.0]) for s in np.linspace(0, 1, 150)]
   m = VMobject(color=color, stroke_width=4); m.set_points_as_corners(pts); return m

  def _wdot(k, color):
   def _q():
    s = (self._tau() * SPD / TPER) % 1.0
    return WC + np.array([WW * (2 * s - 1),
                          WH * TRACK[int(s * (len(TRACK) - 1))][k] / II[k] / SC, 0.0])
   return always_redraw(lambda: Dot(_q(), color=color, radius=0.075))
  waves = VGroup(Line(WC + np.array([-WW, 0, 0]), WC + np.array([WW, 0, 0]),
                      color=GHOST, stroke_width=2),
                 _wave(0, ACCENT_A), _wave(1, ACCENT_B), _wave(2, ACCENT_C),
                 _wdot(0, ACCENT_A), _wdot(1, ACCENT_B), _wdot(2, ACCENT_C),
                 Text("Ω₁ ∝ cn τ", font_size=FS_SMALL, color=ACCENT_A)
                 .move_to(WC + np.array([-1.35, 1.20, 0])),
                 Text("Ω₂ ∝ sn τ", font_size=FS_SMALL, color=ACCENT_B)
                 .move_to(WC + np.array([0.10, 1.20, 0])),
                 Text("Ω₃ ∝ dn τ", font_size=FS_SMALL, color=ACCENT_C)
                 .move_to(WC + np.array([1.50, 1.20, 0])))
  cap6 = VGroup(self._row(-1.35, "只剩一條含 Ω₂ 的一階方程",
                          "one first-order equation in Ω₂ alone", DIM, x=2.20))
  cap7 = VGroup(self._row(-1.35, "反解得到雅可比函數 sn",
                          "inverting it gives the function sn", DIM, x=2.20))
  cap8 = VGroup(self._row(-1.35, "週期由完全橢圓積分 K 決定",
                          "the period is fixed by K", DIM, x=2.20))
  cap9 = VGroup(self._row(-1.35, "k² → 0 就回到 cos、sin 與常數",
                          "at k² → 0 they become cos, sin and 1", WARN, x=2.20))

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

  self.add(axes)
  run(0, fin=[cap0])
  run(1, fin=[ell, sph, cap1], fout=[cap0])
  run(2, fin=[inter, mdot, marr, mtag, cap2], fout=[cap1])
  run(3, fin=[fam, cap3], fout=[cap2, sph, inter, mdot, marr, mtag])
  run(4, fin=[inter, mdot, marr, mtag, fan, cap4], fout=[fam, cap3])
  run(5, fin=[p1, p2, d1, d2, cap5], fout=[inter, mdot, marr, mtag, fan, cap4])
  run(6, fin=[inter, mdot, cap6], fout=[p1, p2, d1, d2, cap5, ell])
  run(7, fin=[cap7], fout=[cap6])
  run(8, fin=[waves], fout=[cap7])
  run(9, fin=[cap9], fout=[])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL37{'ZH' if lang == 'zh' else 'EN'}", (AsymTopBase,), {"LANGUAGE": lang})


LandauL37ZH = _mk("zh")
LandauL37EN = _mk("en")
