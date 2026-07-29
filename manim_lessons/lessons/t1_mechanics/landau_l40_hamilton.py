"""Lesson 40 — Hamilton's equations (Landau §40).

Two pictures carry the algebra. The Legendre transform is drawn literally: a
convex L(q-dot), a tangent of slope p, and H read off as minus the intercept,
with p swept so the tangent rolls along the curve. Then phase space, where the
canonical equations are a flow field: arrows (dH/dp, -dH/dq) everywhere, the
constant-energy ellipses they are tangent to, and a point carried around one.
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
PX = 1.55

# ── the Legendre picture: L = ½ m u², so p = m u and H = p² / 2m ──────
LO = np.array([-4.15, -1.25, 0.0])          # origin of the (u, L) axes
LSX = 1.55; LSY = 0.62; LM = 1.0            # axis scales and the mass


def _lpt(u):
 return LO + np.array([LSX * u, LSY * 0.5 * LM * u * u, 0.0])


# ── phase space: H = ½ p² + ½ ω² q² ──────────────────────────────────
PO = np.array([3.15, -0.20, 0.0])           # origin of the (q, p) axes
PSC = 0.98; WOSC = 1.0


class HamiltonBase(LandauBatchBase):
 EPISODE = 40; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "換一組獨立變數", "en": "a different pair of variables"},
               1: {"zh": "勒讓德變換：從 L 的全微分出發",
                   "en": "Legendre: start from the differential of L"},
               2: {"zh": "用動量的定義與拉格朗日方程改寫",
                   "en": "rewrite it with p and Lagrange's equations"},
               3: {"zh": "把速度的微分挪到左邊", "en": "move the velocity differential across"},
               4: {"zh": "哈密頓量：切線的截距",
                   "en": "the Hamiltonian: the intercept of the tangent"},
               5: {"zh": "獨立變數已經換成 q 與 p",
                   "en": "the independent variables are now q and p"},
               6: {"zh": "哈密頓方程，又叫正則方程",
                   "en": "Hamilton's equations, also called canonical"},
               7: {"zh": "在相空間裡就是一個流",
                   "en": "in phase space it is simply a flow"},
               8: {"zh": "中間兩項剛好抵消", "en": "the two middle terms cancel"},
               9: {"zh": "不顯含時間就守恆", "en": "no explicit time, so it is conserved"}}

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
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > 6.30:
   m.scale_to_fit_width(6.30 - x).move_to([x, y, 0], aligned_edge=LEFT)
  return m

 def _lrow(self, y, zh, en, color=DIM, size=FS_SMALL, x=-6.10):
  """A row on the left, used when the picture sits on the right."""
  m = self.lab(zh, en, size, color).move_to([x, y, 0], aligned_edge=LEFT)
  if m.get_right()[0] > 1.10:
   m.scale_to_fit_width(1.10 - x).move_to([x, y, 0], aligned_edge=LEFT)
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

 # ── the two pictures ──────────────────────────────────────────────
 def _u(self):
  """The tangency point, swept back and forth."""
  return 0.62 + 0.52 * np.sin(0.55 * self._tau())

 def _legendre(self):
  u = self._u(); pm = LM * u                      # slope of the tangent = p
  a, b = _lpt(u - 1.05), _lpt(u + 1.05)
  # the tangent line through _lpt(u) with slope p, drawn in screen units
  sl = LSY * pm / LSX
  ta = _lpt(u) + np.array([-1.55, -1.55 * sl, 0.0])
  tb = _lpt(u) + np.array([1.35, 1.35 * sl, 0.0])
  ic = _lpt(u) + np.array([-LSX * u, -LSX * u * sl, 0.0])   # where it meets u = 0
  g = VGroup(Line(ta, tb, color=ACCENT_B, stroke_width=3),
             Dot(_lpt(u), color=WARN, radius=0.09),
             self._dash(LO, ic, GHOST, n=6),
             Dot(ic, color=ACCENT_C, radius=0.085),
             self._arr(LO, ic, ACCENT_C, sw=5) if abs(ic[1] - LO[1]) > 0.12 else VGroup())
  return g

 def _flow(self, q, p):
  """(dq/dt, dp/dt) = (p, -w^2 q) for H = ½p² + ½w²q²."""
  return np.array([p, -WOSC ** 2 * q, 0.0])

 def construct(self):
  self.t = ValueTracker(0.0); self.t0 = 0.0
  F = FORMULAS[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ beats 0-3: the two descriptions, then the algebra ═════════════
  BX = -3.30
  two = VGroup(self.lab("拉格朗日", "Lagrangian", FS_BODY, ACCENT_A)
               .move_to([BX - 1.35, 0.95, 0]),
               self.lab("哈密頓", "Hamiltonian", FS_BODY, ACCENT_B)
               .move_to([BX + 1.35, 0.95, 0]),
               Text("( q , dq/dt )", font_size=FS_BODY, color=ACCENT_A)
               .move_to([BX - 1.35, 0.30, 0]),
               Text("( q , p )", font_size=FS_BODY, color=ACCENT_B)
               .move_to([BX + 1.35, 0.30, 0]),
               Text("s", font_size=FS_BODY, color=DIM).move_to([BX - 1.35, -0.40, 0]),
               Text("2s", font_size=FS_BODY, color=DIM).move_to([BX + 1.35, -0.40, 0]),
               self.lab("二階方程", "2nd order", FS_SMALL, DIM).move_to([BX - 1.35, -0.85, 0]),
               self.lab("一階方程", "1st order", FS_SMALL, DIM).move_to([BX + 1.35, -0.85, 0]),
               self._arr([BX - 0.42, 0.30, 0], [BX + 0.42, 0.30, 0], WARN, sw=5))
  cap0 = VGroup(self._row(0.90, "狀態也可以用座標與動量描述",
                          "the state may be given by q and p", DIM),
                self._row(0.20, "處理一般性問題時更方便",
                          "handier for general questions", ACCENT_B))
  cap1 = VGroup(self._row(0.90, "數學上叫勒讓德變換", "a Legendre transformation", ACCENT_C,
                          FS_BODY),
                self._row(0.20, "先寫下 L 的全微分",
                          "start from the differential of L", DIM))
  cap2 = VGroup(self._row(0.90, "∂L/∂q̇ᵢ 就是動量 pᵢ", "∂L/∂q̇ᵢ is the momentum pᵢ", ACCENT_B),
                self._row(0.20, "∂L/∂qᵢ 就是 ṗᵢ", "∂L/∂qᵢ is ṗᵢ, by Lagrange", ACCENT_B))
  cap3 = VGroup(self._row(0.90, "把 Σ p dq̇ 換成一個全微分",
                          "turn Σ p dq̇ into a total differential", DIM),
                self._row(0.20, "移到左邊，符號反過來",
                          "move it across and flip the signs", ACCENT_C))

  # ══ beat 4: the Legendre picture ══════════════════════════════════
  ax = VGroup(self._arr(LO + np.array([-0.35, 0, 0]), LO + np.array([3.05, 0, 0]), DIM,
                        sw=3, tl=0.15),
              self._arr(LO + np.array([0, -0.35, 0]), LO + np.array([0, 2.75, 0]), DIM,
                        sw=3, tl=0.15),
              Text("dq/dt", font_size=FS_SMALL, color=DIM).move_to(LO + np.array([3.05, -0.26, 0])),
              Text("L", font_size=FS_SMALL, color=DIM).move_to(LO + np.array([-0.26, 2.72, 0])))
  lcur = self._curve([_lpt(u) for u in np.linspace(-0.25, 1.95, 90)], ACCENT_A, sw=4)
  leg = always_redraw(self._legendre)
  lg_lab = VGroup(self.lab("斜率 = p", "slope = p", FS_SMALL, ACCENT_B)
                  .move_to(LO + np.array([2.35, 1.55, 0])),
                  self.lab("截距 = − H", "intercept = − H", FS_SMALL, ACCENT_C)
                  .move_to(LO + np.array([-0.05, -0.62, 0])))
  cap4 = VGroup(self._row(0.90, "H = Σ p q̇ − L", "H = Σ p q̇ − L", ACCENT_A, FS_BODY),
                self._row(0.20, "就是用 q 與 p 寫的能量",
                          "the energy, written in q and p", DIM),
                self._row(-0.50, "把斜率當成新的變數", "the slope becomes the new variable",
                          ACCENT_B),
                self._row(-1.20, "切線的截距就是新的函數",
                          "the intercept is the new function", ACCENT_C))

  # ══ beats 5-7: phase space ════════════════════════════════════════
  pax = VGroup(self._arr(PO + np.array([-2.25, 0, 0]), PO + np.array([2.25, 0, 0]), DIM,
                         sw=3, tl=0.15),
               self._arr(PO + np.array([0, -1.55, 0]), PO + np.array([0, 1.55, 0]), DIM,
                         sw=3, tl=0.15),
               Text("q", font_size=FS_SMALL, color=DIM).move_to(PO + np.array([2.40, -0.20, 0])),
               Text("p", font_size=FS_SMALL, color=DIM).move_to(PO + np.array([-0.22, 1.58, 0])))
  field = VGroup()
  for q in np.linspace(-1.5, 1.5, 7):
   for pp in np.linspace(-1.1, 1.1, 5):
    if abs(q) < 1e-9 and abs(pp) < 1e-9: continue
    d = self._flow(q, pp); d = 0.42 * d / max(float(np.linalg.norm(d)), 1e-6)
    a = PO + PSC * np.array([q, pp, 0.0])
    field.add(self._arr(a, a + d, ACCENT_C, sw=2.5, tl=0.11))
  ell = VGroup(*[self._curve([PO + PSC * r * np.array([np.cos(a), np.sin(a), 0.0])
                              for a in np.linspace(0, 2 * PI, 90)], GHOST, sw=2.5)
                 for r in (0.55, 1.0, 1.45)])
  orb = self._curve([PO + PSC * 1.0 * np.array([np.cos(a), np.sin(a), 0.0])
                     for a in np.linspace(0, 2 * PI, 120)], ACCENT_B, sw=4)
  pdot = always_redraw(lambda: Dot(
   PO + PSC * np.array([np.cos(-WOSC * self._tau()), np.sin(-WOSC * self._tau()), 0.0]),
   color=WARN, radius=0.10))
  cap5 = VGroup(self._lrow(0.90, "dH = − Σ ṗ dq + Σ q̇ dp", "dH = − Σ ṗ dq + Σ q̇ dp",
                           ACCENT_A, FS_BODY),
                self._lrow(0.20, "獨立變數是 q 與 p", "the variables are q and p", DIM),
                self._lrow(-0.50, "直接讀出係數就好", "just read off the coefficients", ACCENT_B))
  cap6 = VGroup(self._lrow(0.90, "q̇ = ∂H/∂p", "q̇ = ∂H/∂p", ACCENT_B, FS_BODY),
                self._lrow(0.25, "ṗ = − ∂H/∂q", "ṗ = − ∂H/∂q", WARN, FS_BODY),
                self._lrow(-0.45, "2s 條一階方程", "2s first-order equations", DIM),
                self._lrow(-1.10, "形式簡潔對稱：正則方程",
                           "simple and symmetric: canonical", ACCENT_C))
  cap7 = VGroup(self._lrow(0.90, "相空間：q 與 p 張成的平面",
                           "phase space: the q, p plane", DIM),
                self._lrow(0.20, "每一點都有一個前進方向",
                           "every point has a direction", ACCENT_C),
                self._lrow(-0.50, "整個演化就是一個流",
                           "the whole evolution is a flow", ACCENT_B))
  cap8 = VGroup(self._lrow(0.90, "dH/dt = ∂H/∂t + Σ (∂H/∂q) q̇ + Σ (∂H/∂p) ṗ",
                           "dH/dt = ∂H/∂t + Σ (∂H/∂q) q̇ + Σ (∂H/∂p) ṗ", DIM),
                self._lrow(0.20, "代入正則方程", "substitute the canonical equations", ACCENT_C),
                self._lrow(-0.50, "後兩項相消", "the last two cancel", WARN, FS_BODY),
                self._lrow(-1.15, "dH/dt = ∂H/∂t", "dH/dt = ∂H/∂t", ACCENT_A, FS_BODY))
  cap9 = VGroup(self._lrow(0.90, "H 不顯含 t  ⟹  H 守恆",
                           "no explicit t, so H is conserved", ACCENT_A, FS_BODY),
                self._lrow(0.20, "這就是能量守恆", "this is conservation of energy", ACCENT_B),
                self._lrow(-0.50, "代表點永遠待在同一條等能量線上",
                           "the point never leaves its energy curve", WARN))

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

  run(0, fin=[two, cap0])
  run(1, fin=[cap1], fout=[cap0])
  run(2, fin=[cap2], fout=[cap1])
  run(3, fin=[cap3], fout=[cap2])
  run(4, fin=[ax, lcur, leg, lg_lab, cap4], fout=[two, cap3])
  run(5, fin=[pax, ell, cap5], fout=[ax, lcur, leg, lg_lab, cap4])
  run(6, fin=[orb, pdot, cap6], fout=[cap5])
  run(7, fin=[field, cap7], fout=[cap6])
  run(8, fin=[cap8], fout=[field, cap7])
  run(9, fin=[cap9], fout=[cap8])
  self.wait(.7)


def _mk(lang):
 return type(f"LandauL40{'ZH' if lang == 'zh' else 'EN'}", (HamiltonBase,), {"LANGUAGE": lang})


LandauL40ZH = _mk("zh")
LandauL40EN = _mk("en")
