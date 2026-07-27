"""Lesson 38 — Rigid bodies in contact (Landau §38).

Mostly flat pictures: balanced forces, a reaction pair, a normal reaction on an
incline, a sliding block against a rolling wheel whose contact point is
instantaneously at rest. The centrepiece is beat 8, where a sphere is rolled
without slipping around a closed square on the plane by integrating the rolling
constraint itself: it comes home to the same place pointing somewhere else,
which is exactly what makes the constraint non-holonomic.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import numpy as np
from manim import (Arc, Arrow, Circle, Dot, FadeIn, FadeOut, Line, Polygon, Rectangle, Text,
                   VGroup, VMobject, DashedVMobject, ValueTracker, always_redraw, linear,
                   DOWN, LEFT, RIGHT, UP, PI)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.landau_l04_l10 import FORMULAS

FS_TAG = 19
PX = 1.55

# ── beat 8: rolling a sphere without slipping round a closed square ───
BALL_A = 0.484                              # radius, in screen units
# side/radius = 3.71 puts the net rotation at about 91 degrees, which sends the
# marker from the pole all the way to the rim — the clearest possible reading
SQ = 1.794
SQC = np.array([-3.30, -0.20, 0.0])         # centre of the square, on screen


def _loop_path(n=680):
 """The closed square the contact point traces, anticlockwise from a corner."""
 h = SQ / 2.0
 corners = [np.array([-h, -h, 0.0]), np.array([h, -h, 0.0]),
            np.array([h, h, 0.0]), np.array([-h, h, 0.0]), np.array([-h, -h, 0.0])]
 pts = []
 for a, b in zip(corners[:-1], corners[1:]):
  pts.extend(a + (b - a) * s for s in np.linspace(0, 1, n // 4, endpoint=False))
 pts.append(corners[0])
 return np.array(pts)


LOOP = _loop_path()


def _roll(path, a=BALL_A):
 """Integrate the orientation of a sphere rolled without slipping along `path`.

 The constraint V = a Ω × n with n = ẑ gives Ω = (ẑ × V) / a, and the body
 frame obeys dR/dt = [Ω]× R. Nothing here is fitted: this is the constraint.
 """
 R = np.eye(3); out = [R.copy()]
 z = np.array([0.0, 0.0, 1.0])
 for p, q in zip(path[:-1], path[1:]):
  dv = q - p
  om = np.cross(z, dv) / a                          # Ω dt, an infinitesimal rotation
  th = float(np.linalg.norm(om))
  if th > 1e-12:
   k = om / th
   K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
   R = (np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)) @ R
  out.append(R.copy())
 return out


ROLLR = _roll(LOOP)
MARK = np.array([0.0, 0.0, 1.0])            # the body point drawn as a marker


class ContactBase(LandauBatchBase):
 EPISODE = 38; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "平衡：總力與總力矩都為零",
                   "en": "equilibrium: total force and torque both vanish"},
               1: {"zh": "接觸點上的反作用力成對出現",
                   "en": "reactions come in equal and opposite pairs"},
               2: {"zh": "能自由滑動時，反作用力垂直於接觸面",
                   "en": "free to slide: the reaction is normal to it"},
               3: {"zh": "滑動：反作用力垂直，摩擦力沿切線",
                   "en": "sliding: reaction normal, friction tangential"},
               4: {"zh": "純滾動：接觸點瞬間靜止",
                   "en": "pure rolling: the contact point is at rest"},
               5: {"zh": "完全光滑與完全粗糙", "en": "perfectly smooth and perfectly rough"},
               6: {"zh": "接觸會減少自由度", "en": "contact removes degrees of freedom"},
               7: {"zh": "滾動條件是速度之間的關係",
                   "en": "the rolling condition relates the velocities"},
               8: {"zh": "繞一圈回到原處，方向卻變了",
                   "en": "back to the same place, pointing elsewhere"},
               9: {"zh": "拉格朗日乘子，或達朗貝爾原理",
                   "en": "multipliers, or d'Alembert's principle"}}

 # ── helpers ───────────────────────────────────────────────────────
 def lab(self, zh, en, size=FS_SMALL, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def _arr(self, s, t, color, sw=5, tl=0.20):
  if float(np.linalg.norm(np.asarray(t) - np.asarray(s))) < 0.05: return VGroup()
  return Arrow(s, t, buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.34, tip_length=tl)

 def _tag(self, s, follow, off=UP * 0.3, color=INK, size=FS_TAG):
  m = Text(s, font_size=size, color=color)
  m.add_updater(lambda x: x.move_to(follow() + off)); return m

 def _dash(self, a, b, color, n=12, sw=2.5):
  return DashedVMobject(Line(a, b, color=color, stroke_width=sw), num_dashes=n, color=color)

 def _row(self, y, zh, en, color=DIM, size=FS_SMALL, x=PX):
  """A panel row, shrunk if it would run past the safe right edge.

  English labels are roughly twice as wide as the Chinese ones, so a row that
  fits in one language can be silently clipped in the other."""
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > 6.30:
   m.scale_to_fit_width(6.30 - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 def _txt(self, y, s, color=INK, size=FS_BODY, x=PX):
  return Text(s, font_size=size, color=color).move_to([x, y, 0], aligned_edge=LEFT)

 def _rt(self, p, u, v, s=0.16):
  """A right-angle marker at p, between unit directions u and v."""
  return VMobject(color=GHOST, stroke_width=2).set_points_as_corners(
   [p + s * u, p + s * (u + v), p + s * v])

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

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ beat 0: equilibrium ═══════════════════════════════════════════
  BC = np.array([-3.30, -0.15, 0.0])
  blob = Polygon(*[BC + np.array(q) for q in
                   ((-1.05, -0.58, 0), (0.30, -0.86, 0), (1.10, -0.05, 0),
                    (0.80, 0.70, 0), (-0.25, 0.92, 0), (-1.00, 0.40, 0))],
                 color=ACCENT_A, stroke_width=3, fill_opacity=0.10, fill_color=ACCENT_A)
  fpts = [np.array([-0.72, 0.42, 0]), np.array([0.72, 0.30, 0]), np.array([0.02, -0.70, 0])]
  fvec = [np.array([0.62, 0.50, 0]), np.array([0.10, -0.80, 0]), np.array([-0.72, 0.30, 0])]
  eq0 = VGroup(blob, Dot(BC, color=INK, radius=0.07),
               *[self._arr(BC + p, BC + p + v, ACCENT_C, sw=5) for p, v in zip(fpts, fvec)],
               *[Text(f"f{k+1}", font_size=FS_SMALL, color=ACCENT_C)
                 .move_to(BC + p + 1.22 * v) for k, (p, v) in enumerate(zip(fpts, fvec))])
  cap0 = VGroup(self._row(0.95, "總力為零 ⇒ 質心不加速",
                          "total force zero: no acceleration", DIM),
                self._row(0.25, "總力矩為零 ⇒ 不會轉起來",
                          "zero total torque: it does not start turning", DIM),
                self._row(-0.45, "F = 0 時，原點取哪裡都一樣",
                          "with F = 0 the origin does not matter", ACCENT_B))

  # ══ beat 1: a reaction pair ═══════════════════════════════════════
  AX = -3.30
  low = Rectangle(width=2.60, height=0.62, color=ACCENT_A, stroke_width=3,
                  fill_opacity=0.10, fill_color=ACCENT_A).move_to([AX, -0.92, 0])
  up = Rectangle(width=1.55, height=0.62, color=ACCENT_B, stroke_width=3,
                 fill_opacity=0.10, fill_color=ACCENT_B).move_to([AX, -0.25, 0])
  cpt = np.array([AX, -0.61, 0.0])
  pair = VGroup(low, up, Dot(cpt, color=WARN, radius=0.075),
                self._arr(cpt + np.array([0.0, 0.06, 0]), cpt + np.array([0.0, 0.86, 0]),
                          WARN, sw=5),
                self._arr(cpt - np.array([0.0, 0.06, 0]), cpt - np.array([0.0, 0.86, 0]),
                          WARN, sw=5),
                Text("f₁₂", font_size=FS_SMALL, color=WARN).move_to(cpt + np.array([0.42, 0.72, 0])),
                Text("f₂₁", font_size=FS_SMALL, color=WARN).move_to(cpt + np.array([0.42, -0.78, 0])))
  cap1 = VGroup(self._row(0.85, "每個物體各自滿足平衡條件",
                          "each body satisfies both conditions", DIM),
                self._row(0.15, "接觸力 = 反作用力", "contact forces are the reactions", WARN,
                          FS_BODY),
                self._row(-0.55, "大小相等，方向相反", "equal in size, opposite in direction",
                          INK))

  # ══ beats 2-3: the incline, sliding ═══════════════════════════════
  ANG = np.deg2rad(24.0)
  un = np.array([-np.sin(ANG), np.cos(ANG), 0.0])          # surface normal
  ut = np.array([np.cos(ANG), np.sin(ANG), 0.0])           # along the surface
  IA = np.array([-5.20, -1.35, 0.0])
  slope = Line(IA, IA + 4.30 * ut, color=DIM, stroke_width=4)
  ground = Line(IA, IA + np.array([4.30 * np.cos(ANG), 0, 0]), color=GHOST, stroke_width=2)

  def _blk(s):
   c = IA + s * ut + 0.31 * un
   return Rectangle(width=0.86, height=0.62, color=ACCENT_A, stroke_width=3, fill_opacity=0.10,
                    fill_color=ACCENT_A).rotate(ANG).move_to(c), c
  blk2, c2 = _blk(2.55)
  # The slope stays for both beats; the resting block and its normal force are
  # beat 2 only, because beat 3 draws its own moving copy of them.
  inc = VGroup(slope, ground)
  rest = VGroup(blk2,
                self._arr(c2 - 0.31 * un, c2 - 0.31 * un + 1.00 * un, ACCENT_B, sw=5),
                Text("N", font_size=FS_TAG, color=ACCENT_B)
                .move_to(c2 - 0.31 * un + 1.22 * un + np.array([-0.16, 0.04, 0])),
                self._rt(c2 - 0.31 * un, un, ut))
  cap2 = VGroup(self._row(0.85, "可以自由滑動時", "free to slide on each other", DIM),
                self._row(0.15, "反作用力垂直於接觸面",
                          "the reaction is normal to it", ACCENT_B, FS_BODY))
  sl = always_redraw(lambda: VGroup(*[
   m for m in self._slide(IA, ut, un)]))
  cap3 = VGroup(self._row(0.85, "滑動時還有摩擦力", "sliding brings friction too", DIM),
                self._row(0.15, "N 垂直於面", "N is perpendicular to the surface", ACCENT_B),
                self._row(-0.45, "摩擦力沿著切線，方向與運動相反",
                          "friction is tangential, opposing the motion", WARN))

  # ══ beat 4: rolling, the contact point at rest ════════════════════
  WC = np.array([-3.30, -0.35, 0.0]); WR = 0.86
  gnd4 = Line([-6.00, WC[1] - WR, 0], [-0.60, WC[1] - WR, 0], color=DIM, stroke_width=3)

  def _wheel():
   a = 0.75 * self._tau()
   c = WC + np.array([1.15 * np.sin(0.42 * self._tau()), 0.0, 0.0])
   ph = -(c[0] - WC[0]) / WR
   g = VGroup(Circle(radius=WR, color=ACCENT_A, stroke_width=3).move_to(c))
   for k in range(4):
    d = np.array([np.cos(ph + k * PI / 2), np.sin(ph + k * PI / 2), 0.0])
    g.add(Line(c, c + WR * d, color=GHOST, stroke_width=2))
   cp = c + np.array([0.0, -WR, 0.0])
   g.add(Dot(cp, color=WARN, radius=0.09))
   # v = Ω × r about the contact point: zero there, largest at the top
   for f in (0.5, 1.0, 1.5, 2.0):
    q = cp + np.array([0.0, f * WR, 0.0])
    g.add(self._arr(q, q + np.array([0.42 * f, 0.0, 0.0]), ACCENT_C, sw=4, tl=0.14))
   return g
  wheel = always_redraw(_wheel)
  cap4 = VGroup(self._row(0.85, "接觸點的速度是零", "the contact point is at rest",
                          WARN, FS_BODY),
                self._row(0.15, "整個物體像繞著它轉", "the body turns about it", ACCENT_C),
                self._row(-0.55, "反作用力方向不受限制",
                          "the reaction may point any way", DIM),
                self._row(-1.20, "滾動摩擦是一個阻礙滾動的力矩",
                          "rolling friction is an opposing torque", DIM))

  # ══ beat 5: smooth and rough ══════════════════════════════════════
  g5a = Line([-5.90, -1.05, 0], [-1.05, -1.05, 0], color=DIM, stroke_width=3)
  b5 = always_redraw(lambda: Rectangle(width=0.92, height=0.60, color=ACCENT_A, stroke_width=3,
                                       fill_opacity=0.10, fill_color=ACCENT_A)
                     .move_to([-3.50 + 1.30 * np.sin(0.5 * self._tau()), -0.75, 0]))
  g5b = Line([0.75, -1.05, 0], [5.60, -1.05, 0], color=DIM, stroke_width=3)

  def _w5():
   c = np.array([3.20 + 1.30 * np.sin(0.5 * self._tau()), -0.63, 0.0]); r = 0.42
   ph = -(c[0] - 3.20) / r
   g = VGroup(Circle(radius=r, color=ACCENT_B, stroke_width=3).move_to(c))
   for k in range(2):
    d = np.array([np.cos(ph + k * PI / 2), np.sin(ph + k * PI / 2), 0.0])
    g.add(Line(c - r * d, c + r * d, color=GHOST, stroke_width=2))
   return g
  w5 = always_redraw(_w5)
  cap5 = VGroup(self.lab("完全光滑：只滑不摩擦", "perfectly smooth: it just slides",
                         FS_BODY, ACCENT_A).move_to([-3.50, 0.55, 0]),
                self.lab("完全粗糙：只滾不滑", "perfectly rough: it only rolls",
                         FS_BODY, ACCENT_B).move_to([3.20, 0.55, 0]),
                self.lab("兩種情況摩擦力都不必寫進方程",
                         "in both, friction never enters the equations", FS_SMALL, DIM)
                .move_to([0.0, -1.55, 0]))

  # ══ beats 6-7: constraints ════════════════════════════════════════
  rows6 = VGroup(self._txt(0.95, "6", ACCENT_A, FS_BODY, x=-4.60),
                 self.lab("自由剛體", "a free rigid body", FS_BODY, DIM)
                 .move_to([-4.10, 0.95, 0], aligned_edge=LEFT),
                 self._txt(0.20, "5", ACCENT_B, FS_BODY, x=-4.60),
                 self.lab("放到面上", "resting on a surface", FS_BODY, DIM)
                 .move_to([-4.10, 0.20, 0], aligned_edge=LEFT),
                 self._txt(-0.55, "3", WARN, FS_BODY, x=-4.60),
                 self.lab("純滾動的球", "a sphere in pure rolling", FS_BODY, DIM)
                 .move_to([-4.10, -0.55, 0], aligned_edge=LEFT))
  cap6 = VGroup(self._row(0.60, "以前都直接用剛好夠用的座標",
                          "so far we used just enough coordinates", DIM),
                self._row(-0.10, "滾動時可能做不到", "for rolling that may be impossible",
                          WARN, FS_BODY))
  cap7 = VGroup(self._row(0.85, "接觸點速度相等", "the contact points move alike", DIM),
                self._row(0.15, "係數只依賴座標", "the coefficients depend on q only", DIM),
                self._row(-0.55, "左邊若不是全微分，就積不出來",
                          "if not a total derivative, it will not integrate", WARN))

  # ══ beat 8: the sphere round a closed loop ════════════════════════
  loop = self._curve8()
  ball = always_redraw(self._ball8)
  ghost0 = self._ball_at(0, DIM)
  ghostE = self._ball_at(len(ROLLR) - 1, WARN)
  cap8 = VGroup(self._row(0.95, "球沿封閉路徑純滾動一圈",
                          "roll the sphere once round a closed path", DIM),
                self._row(0.25, "回到原來的位置", "back to the same place", ACCENT_B,
                          FS_BODY),
                self._row(-0.45, "但方向不一樣了", "but pointing elsewhere",
                          WARN, FS_BODY),
                self._row(-1.15, "所以約束積不出來：非完整",
                          "the constraint is non-holonomic", INK))

  # ══ beat 9 ════════════════════════════════════════════════════════
  cap9 = VGroup(self._row(0.95, "保留不獨立的座標", "keep the dependent coordinates", DIM),
                self._row(0.25, "用待定乘子加進作用量",
                          "add the constraints with multipliers", ACCENT_B),
                self._row(-0.45, "或者：達朗貝爾原理", "or: d'Alembert's principle", ACCENT_C,
                          FS_BODY),
                self._row(-1.15, "把反作用力明白地寫進方程",
                          "write the reactions in explicitly", DIM))

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

  run(0, fin=[eq0, cap0])
  run(1, fin=[pair, cap1], fout=[eq0, cap0])
  run(2, fin=[inc, rest, cap2], fout=[pair, cap1])
  run(3, fin=[sl, cap3], fout=[cap2, rest])
  run(4, fin=[gnd4, wheel, cap4], fout=[inc, sl, cap3])
  run(5, fin=[g5a, b5, g5b, w5, cap5], fout=[gnd4, wheel, cap4])
  run(6, fin=[rows6, cap6], fout=[g5a, b5, g5b, w5, cap5])
  run(7, fin=[cap7], fout=[rows6, cap6])
  run(8, fin=[loop, ghost0, ball, ghostE, cap8], fout=[cap7])
  run(9, fin=[cap9], fout=[loop, ghost0, ball, ghostE, cap8])
  self.wait(.7)

 # ── beat 3 and 8 pieces ───────────────────────────────────────────
 def _slide(self, IA, ut, un):
  s = 2.55 - 0.95 * np.sin(0.55 * self._tau())
  c = IA + s * ut + 0.31 * un
  foot = c - 0.31 * un
  blk = Rectangle(width=0.86, height=0.62, color=ACCENT_A, stroke_width=3, fill_opacity=0.10,
                  fill_color=ACCENT_A).rotate(np.arctan2(ut[1], ut[0])).move_to(c)
  return [blk, self._arr(foot, foot + 1.00 * un, ACCENT_B, sw=5),
          self._arr(foot, foot + 0.90 * ut, WARN, sw=5),
          Text("N", font_size=FS_SMALL, color=ACCENT_B).move_to(foot + 1.20 * un),
          Text("f", font_size=FS_SMALL, color=WARN).move_to(foot + 1.10 * ut
                                                            + np.array([0.0, -0.18, 0]))]

 def _curve8(self):
  m = VMobject(color=GHOST, stroke_width=3)
  m.set_points_as_corners([SQC + q for q in LOOP[::12]] + [SQC + LOOP[0]])
  return DashedVMobject(m, num_dashes=52, color=GHOST)

 def _ball_at(self, i, color):
  """The sphere drawn at step i: a rim, two body meridians and a marker."""
  c = SQC + LOOP[min(i, len(LOOP) - 1)]; R = ROLLR[min(i, len(ROLLR) - 1)]
  g = VGroup(Circle(radius=BALL_A, color=color, stroke_width=3).move_to(c))
  for e1, e2 in ((np.array([1., 0, 0]), np.array([0, 1., 0])),
                 (np.array([1., 0, 0]), np.array([0, 0, 1.]))):
   u, v = R @ e1, R @ e2
   g.add(VMobject(color=color, stroke_width=2).set_points_as_corners(
    [c + BALL_A * (np.cos(a) * u + np.sin(a) * v) * np.array([1, 1, 0])
     for a in np.linspace(0, 2 * PI, 48)]))
  p = R @ MARK
  g.add(Dot(c + BALL_A * np.array([p[0], p[1], 0.0]), color=color, radius=0.085))
  return g

 def _ball8(self):
  i = int(self._tau() * 190) % len(ROLLR)
  return self._ball_at(i, ACCENT_B)


def _mk(lang):
 return type(f"LandauL38{'ZH' if lang == 'zh' else 'EN'}", (ContactBase,), {"LANGUAGE": lang})


LandauL38ZH = _mk("zh")
LandauL38EN = _mk("en")
