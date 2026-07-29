"""Special S01 — Verbalizable representations as a global workspace.

Based on Gurnee et al., "Verbalizable Representations Form a Global Workspace
in Language Models" (Anthropic, 2026), transformer-circuits.pub/2026/workspace.

Stage A (beats 0-2) is the layer tower: a cloud of internal representations of
which only a few are ever spoken, then the Jacobian lens tapping one middle
layer and replacing everything above it, then the sparse J-space decomposition.
Stage B (beats 3-7) is a prompt -> lens -> output flow on which each of the five
functional properties is demonstrated by swapping the top lens coordinate mid
beat and watching the output follow (or, for selectivity, not follow).
Stage C (beats 8-9) is the structural board: the depth profile of the workspace,
its capacity, the ablation contrast, the broadcast hub and the ignition curves.
Beat 10 closes on the five properties around the workspace itself.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import numpy as np
from manim import (Arrow, Circle, DashedLine, Dot, FadeIn, FadeOut, Line, Rectangle,
                   RoundedRectangle, Text, Transform, VGroup, VMobject, ValueTracker,
                   always_redraw, linear, DOWN, UP)
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, GHOST, INK, WARN,
                                             FS_BODY, FS_H1, FS_H2, FS_SMALL, apply_global_config)
from manim_lessons.lessons.landau_l04_l10 import LandauBatchBase
from manim_lessons.localization.special_topics import TOPICS_SPECIAL, FORMULAS_SPECIAL

FS_TAG = 16                                # in-figure labels
FS_TOK = 17                                # vocabulary tokens
FS_MICRO = 14                              # axis numbers, table cells

# ── stage A: the layer tower ──────────────────────────────────────────
TWX = -5.05; TWW = 1.15                    # tower centre and width
TWB, TWT = -1.55, 1.72                     # bottom and top of the tower
NBLK = 15
TAP = 0.60                                 # the layer the lens is taken at, as a fraction

# ── stage B: prompt -> lens -> output ─────────────────────────────────
P1X, P1W = -4.45, 3.80                     # prompt card
P2X, P2W = 0.10, 3.60                      # lens panel
P3X, P3W = 4.60, 3.60                      # output card
CARDY, CARDH = 0.55, 2.20
LENSY, LENSH = 0.20, 3.14
ROW0, RGAP = 1.02, 0.50                    # first readout row, row pitch
TOKX = P2X - 1.62; BARX = P2X + 0.14; BARW = 1.60

# ── stage C: the structural board ─────────────────────────────────────
PX0, PX1 = -6.20, -1.00                    # depth profile, layer 0 -> 100
PYB, PYH = -1.42, 2.05
BAND = (38.0, 92.0)


def _lx(layer):
 return PX0 + (PX1 - PX0) * layer / 100.0


def _profile(layer):
 """How strongly the workspace is loaded at a given depth (schematic)."""
 return float(np.exp(-(((layer - 66.0) / 21.0) ** 2)) * (1.0 - np.exp(-((layer / 26.0) ** 3))))


class WorkspaceBase(LandauBatchBase):
 EPISODE = 1; LANGUAGE = "zh"
 MODE_LABEL = {0: {"zh": "內部表徵很多，說得出口的很少",
                   "en": "many representations, few of them spoken"},
               1: {"zh": "雅可比透鏡：直接把中層讀成詞彙",
                   "en": "the Jacobian lens: read a middle layer as vocabulary"},
               2: {"zh": "工作空間座標：稀疏、非負、佔比很小",
                   "en": "workspace coordinates: sparse, non-negative, small"},
               3: {"zh": "性質一　口語報告", "en": "property 1 — verbal report"},
               4: {"zh": "性質二　指向性調控", "en": "property 2 — directed modulation"},
               5: {"zh": "性質三　內部推理", "en": "property 3 — internal reasoning"},
               6: {"zh": "性質四　彈性泛化", "en": "property 4 — flexible generalization"},
               7: {"zh": "性質五　選擇性", "en": "property 5 — selectivity"},
               8: {"zh": "結構：深度、容量、消融", "en": "structure: depth, capacity, ablation"},
               9: {"zh": "廣播樞紐與點火動態", "en": "a broadcast hub, and ignition"},
               10: {"zh": "功能上的工作空間", "en": "a workspace in the functional sense"}}

 def setup(self):
  apply_global_config()
  self.title, self.lines = TOPICS_SPECIAL[self.EPISODE][self.LANGUAGE]
  self.clock = ValueTracker(0)
  self.audio_dir = (pathlib.Path(__file__).resolve().parents[2] / "samples"
                    / f"audio_s{self.EPISODE:02d}" / ("zh-TW" if self.LANGUAGE == "zh" else "en"))

 # ── small helpers ─────────────────────────────────────────────────
 def lab(self, zh, en, size=FS_TAG, color=DIM):
  return Text(zh if self.LANGUAGE == "zh" else en, font_size=size, color=color)

 def pick(self, zh, en):
  return zh if self.LANGUAGE == "zh" else en

 def card(self, cx, cy, w, h, color=GHOST):
  return RoundedRectangle(width=w, height=h, corner_radius=0.14, color=color, stroke_width=2,
                          fill_opacity=0.05, fill_color=INK).move_to([cx, cy, 0])

 def rows_at(self, left, top, texts, size=FS_TAG, color=INK, gap=0.34):
  g = VGroup()
  for k, s in enumerate(texts):
   m = Text(s, font_size=size, color=color)
   m.move_to([left + m.width / 2, top - k * gap, 0])
   g.add(m)
  return g

 def tok(self, s, y, on):
  m = Text(s, font_size=FS_TOK, color=ACCENT_A if on else INK)
  return m.move_to([TOKX + m.width / 2, y, 0])

 def bar(self, val, y, on):
  w = max(val * BARW, 0.04)
  return Rectangle(width=w, height=0.15, stroke_width=0, fill_opacity=0.9,
                   fill_color=ACCENT_C if on else DIM).move_to([BARX + w / 2, y, 0])

 def readout(self, items):
  """A J-lens readout panel; row 0 is the one the swaps act on."""
  toks, bars = [], []
  for k, (s, v) in enumerate(items):
   y = ROW0 - k * RGAP
   toks.append(self.tok(s, y, k == 0)); bars.append(self.bar(v, y, k == 0))
  return VGroup(*toks, *bars), toks, bars

 def big(self, s, cx, cy, color=ACCENT_A, size=26):
  return Text(s, font_size=size, color=color).move_to([cx, cy, 0])

 # ── beat plumbing (a swap can land part-way through a beat) ────────
 def beat(self, i, fin=(), fout=(), mid=(), at=0.55, extra=()):
  d = self.dur(i); self.add_sound(str(self.audio_dir / f"{i:02d}.mp3"))
  r = min(0.5, d)
  self.play(*[FadeIn(m) for m in fin], *[FadeOut(m) for m in fout],
            self.t.animate(rate_func=linear).increment_value(r), run_time=r)
  d -= r
  if mid and d > 1.2:
   h = max(0.05, (d - 0.9) * at)
   self.play(self.t.animate(rate_func=linear).increment_value(h), run_time=h); d -= h
   s = min(0.9, d)
   self.play(*mid, self.t.animate(rate_func=linear).increment_value(s), run_time=s); d -= s
  if d > 1e-3:
   self.play(self.t.animate(rate_func=linear).increment_value(d), *extra, run_time=d)

 def formula(self, s):
  m = Text(s, font_size=FS_H2, color=ACCENT_A, line_spacing=1.15)
  if m.width > 12.4: m.scale_to_fit_width(12.4)
  return m.move_to(UP * (2.35 - 0.22 * max(0, len(s.split(chr(10))) - 2)))

 def sub(self, line):
  return self.text(line, FS_BODY, INK).to_edge(DOWN, buff=.5)

 # ══════════════════════════════════════════════════════════════════
 def construct(self):
  self.t = ValueTracker(0.0)
  F = FORMULAS_SPECIAL[self.EPISODE]
  heading = self.text(self.title, FS_H1, ACCENT_A).to_edge(UP, buff=.45)
  self.add(heading)

  # ══ stage A ══════════════════════════════════════════════════════
  bh = (TWT - TWB) / NBLK
  blocks = VGroup(*[Rectangle(width=TWW, height=bh * 0.86, color=GHOST, stroke_width=1.6,
                              fill_opacity=0.10, fill_color=INK)
                    .move_to([TWX, TWB + (k + 0.5) * bh, 0]) for k in range(NBLK)])
  tw_lo = Text("0", font_size=FS_MICRO, color=DIM).move_to([TWX - 1.00, TWB + 0.10, 0])
  tw_hi = Text("100", font_size=FS_MICRO, color=DIM).move_to([TWX - 1.00, TWT - 0.10, 0])
  tw_cap = self.lab("層", "layer", FS_MICRO, DIM).move_to([TWX - 1.00, 0.0, 0])
  tower = VGroup(blocks, tw_lo, tw_hi, tw_cap)

  # the cloud: many representations, a handful of them verbalizable
  rng = np.random.default_rng(7)
  cpos = []
  while len(cpos) < 84:
   p = np.array([rng.uniform(-2.05, 2.05), rng.uniform(-1.35, 1.35), 0.0])
   if (p[0] / 2.05) ** 2 + (p[1] / 1.35) ** 2 <= 1.0: cpos.append(p + np.array([-1.25, 0.05, 0.0]))
  vocal = sorted(rng.choice(len(cpos), 7, replace=False))
  cloud = VGroup(*[Dot(cpos[k], radius=0.048, color=(ACCENT_C if k in vocal else GHOST))
                   for k in range(len(cpos))])
  cloud_tag = self.lab("內部表徵", "internal representations", FS_TAG, DIM
                       ).move_to([-1.25, -1.62, 0])
  spoke_box = self.card(4.75, 0.05, 2.90, 1.30, ACCENT_A)
  spoke_tag = self.lab("說得出口的", "verbalizable", FS_TAG, ACCENT_A).move_to([4.75, 0.42, 0])
  spoke_dots = VGroup(*[Dot([4.75 + (k - 3) * 0.30, -0.22, 0], radius=0.055, color=ACCENT_C)
                        for k in range(7)])
  bridge = Arrow([0.95, 0.05, 0], [3.22, 0.05, 0], buff=0, color=ACCENT_C, stroke_width=4,
                 tip_length=0.18)
  intro = VGroup(cloud, cloud_tag, bridge, spoke_box, spoke_tag, spoke_dots)

  # the lens: tap one middle layer, replace everything above it
  tapy = TWB + TAP * (TWT - TWB)
  tapblk = Rectangle(width=TWW, height=bh * 0.86, color=ACCENT_C, stroke_width=3,
                     fill_opacity=0.28, fill_color=ACCENT_C).move_to([TWX, tapy, 0])
  above = VGroup(*[Rectangle(width=TWW, height=bh * 0.86, color=GHOST, stroke_width=1.4,
                             fill_opacity=0.03, fill_color=GHOST)
                   .move_to([TWX, TWB + (k + 0.5) * bh, 0])
                   for k in range(NBLK) if TWB + (k + 0.5) * bh > tapy + 0.05])
  skip = DashedLine([TWX + 0.72, tapy + 0.18, 0], [TWX + 0.72, TWT + 0.02, 0], color=WARN,
                    stroke_width=3, dash_length=0.10)
  skip_tag = self.lab("上面的層被 J 取代", "layers above replaced by J", FS_MICRO, WARN
                      ).move_to([TWX + 2.05, TWT - 0.16, 0])
  beam = Line([TWX + 0.60, tapy, 0], [P2X - 1.86, tapy, 0], color=ACCENT_C, stroke_width=3)
  beam_tag = Text("J", font_size=FS_H2, color=ACCENT_C).move_to([-2.60, tapy + 0.34, 0])
  pulse = always_redraw(lambda: Dot(
   [TWX + 0.60 + ((P2X - 1.86) - (TWX + 0.60)) * ((0.55 * self.t.get_value()) % 1.0), tapy, 0],
   radius=0.075, color=ACCENT_C))
  lens_tap = VGroup(tapblk, above, skip, skip_tag)
  lens_beam = VGroup(beam, beam_tag, pulse)

  lens_box = self.card(P2X, LENSY, P2W, LENSH)
  lens_hdr = Text("J-lens readout", font_size=FS_MICRO, color=DIM).move_to([P2X, 1.52, 0])
  demo_rows, _, _ = self.readout([("Paris", 1.00), ("France", 0.72), ("capital", 0.55),
                                  ("city", 0.40), ("Lyon", 0.24)])
  demo_panel = VGroup(lens_box, lens_hdr, demo_rows)

  # J-space: a sparse non-negative combination, and how little variance it is
  VCX = -2.95
  var_col = VGroup(
   Rectangle(width=0.62, height=2.52, stroke_width=0, fill_opacity=0.55, fill_color=GHOST)
   .move_to([VCX, 0.06, 0]),
   Rectangle(width=0.62, height=0.28, stroke_width=0, fill_opacity=0.95, fill_color=ACCENT_C)
   .move_to([VCX, 1.18, 0]),
   Text("J-space  <  10 %", font_size=FS_MICRO, color=ACCENT_C)
   .move_to([VCX + 1.32, 1.18, 0]),
   self.lab("其餘變異", "the rest", FS_MICRO, DIM).move_to([VCX + 1.00, 0.30, 0]),
   self.lab("一個活化的變異", "variance of one activation", FS_MICRO, DIM)
   .move_to([VCX, -1.52, 0]))
  coef = VGroup()
  for k, (nm, v) in enumerate([("j₁", 0.92), ("j₂", 0.74), ("j₃", 0.61), ("j₄", 0.45),
                               ("j₂₅", 0.21)]):
   y = 1.10 - k * 0.46
   coef.add(Text(nm, font_size=FS_TAG, color=ACCENT_B).move_to([0.75, y, 0]))
   w = v * 2.30
   coef.add(Rectangle(width=w, height=0.17, stroke_width=0, fill_opacity=0.9,
                      fill_color=ACCENT_B).move_to([1.25 + w / 2, y, 0]))
  coef.add(Text("⋮", font_size=FS_TAG, color=DIM).move_to([0.75, -0.51, 0]))
  coef.add(self.lab("k ≈ 25 個非負係數", "k ≈ 25 non-negative coefficients", FS_MICRO, DIM)
           .move_to([2.05, -1.52, 0]))
  jspace = VGroup(var_col, coef)

  # ══ stage B ══════════════════════════════════════════════════════
  p1 = self.card(P1X, CARDY, P1W, CARDH)
  p3 = self.card(P3X, CARDY, P3W, CARDH)
  a12 = Arrow([P1X + P1W / 2 + 0.06, CARDY, 0], [P2X - P2W / 2 - 0.08, CARDY, 0], buff=0,
              color=DIM, stroke_width=4, tip_length=0.16)
  a23 = Arrow([P2X + P2W / 2 + 0.08, CARDY, 0], [P3X - P3W / 2 - 0.06, CARDY, 0], buff=0,
              color=DIM, stroke_width=4, tip_length=0.16)
  p1_hdr = self.lab("提示", "prompt", FS_MICRO, DIM).move_to([P1X, CARDY + 0.92, 0])
  p3_hdr = self.lab("模型輸出", "the model says", FS_MICRO, DIM).move_to([P3X, CARDY + 0.92, 0])
  frame = VGroup(p1, p3, a12, a23, p1_hdr, p3_hdr, lens_box, lens_hdr)

  def swap(toks, bars, new):
   """Replace the top lens coordinate and flash the bar."""
   nt = self.tok(new, ROW0, True).set_color(WARN)
   nb = self.bar(0.98, ROW0, True).set_fill(WARN)
   return [Transform(toks[0], nt), Transform(bars[0], nb)]

  # beat 3 — verbal report
  b3p = self.rows_at(P1X - 1.62, CARDY + 0.42,
                     self.pick(["請在心裡想一個運動，", "先不要說出來。"],
                               ["Think of a sport.", "Do not say it yet."]))
  b3r, b3t, b3b = self.readout([("soccer", 1.00), ("basketball", 0.64), ("tennis", 0.47),
                                ("sport", 0.35), ("game", 0.22)])
  b3o = self.big("Soccer", P3X, CARDY - 0.10)
  b3 = VGroup(b3p, b3r, b3o)

  # beat 4 — directed modulation
  b4p = self.rows_at(P1X - 1.62, CARDY + 0.62,
                     self.pick(["逐字抄寫這句話：", "「牆上那幅舊畫掛歪了。」", "同時在心裡想著柑橘類水果。"],
                               ["Copy this out word by word:", "\"The old painting hung",
                                "crookedly on the wall.\"", "While holding citrus in mind."]),
                     size=FS_MICRO)
  b4r, b4t, b4b = self.readout([("orange", 1.00), ("lemon", 0.80), ("citrus", 0.62),
                                ("fruit", 0.45), ("lime", 0.30)])
  b4o = VGroup(self.lab("抄寫結果完全不變", "the copy comes out unchanged", FS_TAG, INK)
               .move_to([P3X, CARDY + 0.18, 0]),
               self.lab("柑橘一個字也沒出現", "no citrus word ever appears", FS_TAG, DIM)
               .move_to([P3X, CARDY - 0.34, 0]))
  b4note = self.lab("改叫它「不要去想」", "now told: do not think of it", FS_MICRO, WARN
                    ).move_to([P2X, -1.62, 0])
  b4 = VGroup(b4p, b4r, b4o)

  # beat 5 — internal reasoning
  b5p = self.rows_at(P1X - 1.62, CARDY + 0.42,
                     self.pick(["會結網的那種動物，", "有幾條腿？"],
                               ["The number of legs on", "the animal that spins", "webs is ___"]))
  b5r, b5t, b5b = self.readout([("spider", 1.00), ("web", 0.71), ("eight", 0.56),
                                ("arachnid", 0.40), ("insect", 0.26)])
  b5o = self.big("8", P3X, CARDY - 0.10, size=34)
  b5note = self.lab("蜘蛛從沒出現在題目或答案裡", "spider is never written down", FS_MICRO, DIM
                    ).move_to([P2X, -1.62, 0])
  b5 = VGroup(b5p, b5r, b5o)

  # beat 6 — flexible generalization
  b6p = self.rows_at(P1X - 1.68, CARDY + 0.55,
                     self.pick(["法國的首都是…", "法國人說的語言是…", "法國位於哪一洲…"],
                               ["the capital of France is", "people in France speak",
                                "France is on the continent"]), size=FS_MICRO, gap=0.52)
  b6r, b6t, b6b = self.readout([("France", 1.00), ("Paris", 0.58), ("Europe", 0.45),
                                ("French", 0.37), ("Lyon", 0.24)])
  b6o = VGroup(*[Text(s, font_size=FS_TOK, color=ACCENT_A).move_to([P3X, CARDY + 0.55 - k * 0.52, 0])
                 for k, s in enumerate(["Paris", "French", "Europe"])])
  b6n = ["Beijing", "Chinese", "Asia"]
  b6 = VGroup(b6p, b6r, b6o)

  # beat 7 — selectivity
  p3b = self.card(P3X, 0.20, P3W + 0.30, 3.05)
  b7p = self.rows_at(P1X - 1.62, CARDY + 0.42,
                     self.pick(["一段西班牙文：", "「El sol se pone", "sobre el mar.」"],
                               ["a Spanish passage:", "\"El sol se pone", "sobre el mar.\""]))
  b7r, b7t, b7b = self.readout([("Spanish", 1.00), ("Spain", 0.63), ("español", 0.50),
                                ("romance", 0.38), ("Latin", 0.25)])
  b7tasks = [(("續寫下一句", "continue the text"), ("不變", "unchanged"), ACCENT_B),
             (("偵測夾雜的外語", "spot a foreign word"), ("不變", "unchanged"), ACCENT_B),
             (("說出這是什麼語言", "name the language"), ("跟著換", "follows"), WARN),
             (("舉一位這語言的作家", "name an author"), ("跟著換", "follows"), WARN)]
  b7tab = VGroup(Text("task", font_size=FS_MICRO, color=DIM).move_to([P3X - 1.20, 1.40, 0]),
                 self.lab("結果", "result", FS_MICRO, DIM).move_to([P3X + 1.15, 1.40, 0]),
                 Line([P3X - 1.75, 1.18, 0], [P3X + 1.75, 1.18, 0], color=GHOST, stroke_width=1.6))
  for k, (nm, res, col) in enumerate(b7tasks):
   y = 0.80 - k * 0.56
   a = self.lab(*nm, FS_MICRO, INK); a.move_to([P3X - 1.72 + a.width / 2, y, 0])
   b = self.lab(*res, FS_MICRO, col); b.move_to([P3X + 0.95 + b.width / 2, y, 0])
   b7tab.add(a, b, Dot([P3X + 0.72, y, 0], radius=0.055, color=col))
  b7 = VGroup(b7p, b7r, b7tab)

  # ══ stage C ══════════════════════════════════════════════════════
  axis = Line([PX0, PYB, 0], [PX1, PYB, 0], color=GHOST, stroke_width=2)
  band = Rectangle(width=_lx(BAND[1]) - _lx(BAND[0]), height=PYH, stroke_width=0,
                   fill_opacity=0.16, fill_color=ACCENT_C).move_to(
   [(_lx(BAND[0]) + _lx(BAND[1])) / 2, PYB + PYH / 2, 0])
  curve = VMobject(color=ACCENT_C, stroke_width=4)
  curve.set_points_as_corners([[_lx(l), PYB + PYH * 0.92 * _profile(l), 0]
                               for l in np.linspace(0, 100, 160)])
  ticks = VGroup()
  for l in (0, 38, 92, 100):
   ticks.add(Line([_lx(l), PYB, 0], [_lx(l), PYB - 0.12, 0], color=DIM, stroke_width=2),
             Text(str(l), font_size=FS_MICRO, color=DIM).move_to([_lx(l), PYB - 0.32, 0]))
  prof_tag = self.lab("工作空間只活在中間層", "the workspace lives in the middle layers",
                      FS_TAG, INK).move_to([(PX0 + PX1) / 2, 1.55, 0])
  profile = VGroup(band, axis, curve, ticks, prof_tag)

  cap_dots = VGroup(*[Dot([0.55 + (k % 5) * 0.26, 1.34 - (k // 5) * 0.26, 0], radius=0.065,
                          color=ACCENT_B) for k in range(25)])
  cap_tag = self.lab("同時只有約 10–25 個概念", "only about 10–25 concepts at once", FS_TAG, DIM)
  cap_tag.move_to([2.05 + cap_tag.width / 2, 1.02, 0])
  capacity = VGroup(cap_dots, cap_tag)

  abl_base = -1.42
  abl = VGroup(Line([0.30, abl_base, 0], [6.10, abl_base, 0], color=GHOST, stroke_width=2))
  for k, (x, h, col) in enumerate([(0.75, 0.96, ACCENT_B), (1.35, 0.92, ACCENT_B),
                                   (1.95, 0.89, ACCENT_B), (4.05, 0.08, WARN),
                                   (4.65, 0.05, WARN), (5.25, 0.11, WARN)]):
   abl.add(Rectangle(width=0.42, height=1.28, color=GHOST, stroke_width=1.6, fill_opacity=0)
           .move_to([x, abl_base + 0.64, 0]),
           Rectangle(width=0.42, height=max(h * 1.28, 0.03), stroke_width=0, fill_opacity=0.9,
                     fill_color=col).move_to([x, abl_base + max(h * 1.28, 0.03) / 2, 0]))
  abl.add(self.lab("淺層任務", "shallow tasks", FS_MICRO, ACCENT_B).move_to([1.35, abl_base - 0.28, 0]),
          self.lab("多跳推理", "multi-hop reasoning", FS_MICRO, WARN).move_to([4.65, abl_base - 0.28, 0]),
          self.lab("壓制工作空間後的正確率", "accuracy after suppressing the workspace",
                   FS_MICRO, DIM).move_to([3.00, 0.28, 0]))
  board = VGroup(profile, capacity, abl)

  # beat 9 — broadcast hub and ignition
  HC = np.array([-4.30, 0.05, 0.0])
  hub = VGroup(Circle(radius=0.52, color=ACCENT_C, stroke_width=3, fill_opacity=0.20,
                      fill_color=ACCENT_C).move_to(HC),
               Text("J", font_size=FS_H2, color=ACCENT_C).move_to(HC))
  for k in range(12):
   a = 2 * np.pi * k / 12 + 0.13
   d = np.array([np.cos(a), np.sin(a) * 0.78, 0.0])
   hub.add(Line(HC + 0.56 * d, HC + 1.42 * d, color=ACCENT_C, stroke_width=2.2),
           Rectangle(width=0.22, height=0.16, stroke_width=0, fill_opacity=0.8,
                     fill_color=DIM).move_to(HC + 1.58 * d))
  OC = np.array([-1.55, 0.05, 0.0])
  other = VGroup(Circle(radius=0.34, color=GHOST, stroke_width=2.5).move_to(OC))
  for k in range(2):
   d = np.array([np.cos(0.5 + k * 1.1), np.sin(0.5 + k * 1.1) * 0.78, 0.0])
   other.add(Line(OC + 0.38 * d, OC + 0.95 * d, color=GHOST, stroke_width=2.2),
             Rectangle(width=0.20, height=0.15, stroke_width=0, fill_opacity=0.7,
                       fill_color=GHOST).move_to(OC + 1.08 * d))
  hub_tag = self.lab("工作空間方向接得比較廣", "workspace directions compose more broadly",
                     FS_MICRO, DIM).move_to([-3.05, -1.55, 0])

  IX0, IX1, IYB, IYH = 0.55, 5.00, -1.20, 2.10
  def _ix(l): return IX0 + (IX1 - IX0) * l / 100.0
  ign_ax = Line([IX0, IYB, 0], [IX1, IYB, 0], color=GHOST, stroke_width=2)
  ign_on = DashedLine([_ix(38), IYB, 0], [_ix(38), IYB + IYH, 0], color=WARN, stroke_width=2.5,
                      dash_length=0.10)
  def _sig(l, up):
   s = 1.0 / (1.0 + np.exp(-(l - 44.0) / 3.4))
   return 0.5 + (0.46 * s if up else -0.46 * s)
  ign_a = VMobject(color=ACCENT_A, stroke_width=4)
  ign_a.set_points_as_corners([[_ix(l), IYB + IYH * _sig(l, True), 0]
                               for l in np.linspace(0, 100, 140)])
  ign_b = VMobject(color=ACCENT_B, stroke_width=4)
  ign_b.set_points_as_corners([[_ix(l), IYB + IYH * _sig(l, False), 0]
                               for l in np.linspace(0, 100, 140)])
  lab_a = self.lab("解讀 A", "reading A", FS_MICRO, ACCENT_A)
  lab_a.move_to([IX1 + 0.18 + lab_a.width / 2, IYB + IYH * 0.96, 0])
  lab_b = self.lab("解讀 B", "reading B", FS_MICRO, ACCENT_B)
  lab_b.move_to([IX1 + 0.18 + lab_b.width / 2, IYB + IYH * 0.04, 0])
  ign = VGroup(ign_ax, ign_on, ign_a, ign_b, lab_a, lab_b,
               Text("38", font_size=FS_MICRO, color=WARN).move_to([_ix(38) - 0.24, IYB - 0.24, 0]),
               self.lab("歧義輸入在工作空間起點突然收斂",
                        "an ambiguous input commits where the workspace begins",
                        FS_MICRO, DIM).move_to([(IX0 + IX1) / 2 + 0.35, -1.72, 0]))
  ign_scan = always_redraw(lambda: Line(
   [_ix(min(100.0, (28.0 * self.t.get_value()) % 118.0)), IYB, 0],
   [_ix(min(100.0, (28.0 * self.t.get_value()) % 118.0)), IYB + IYH, 0],
   color=GHOST, stroke_width=2))
  hubign = VGroup(hub, other, hub_tag, ign, ign_scan)

  # ══ beat 10 — the five properties around the workspace ═══════════
  CC = np.array([0.0, 0.10, 0.0])
  core = VGroup(Circle(radius=0.96, color=ACCENT_C, stroke_width=3, fill_opacity=0.16,
                       fill_color=ACCENT_C).move_to(CC),
                self.lab("全域\n工作空間", "global\nworkspace", FS_TAG, INK).move_to(CC))
  props = [("口語報告", "verbal report"), ("指向性調控", "directed modulation"),
           ("內部推理", "internal reasoning"), ("彈性泛化", "flexible generalization"),
           ("選擇性", "selectivity")]
  spokes = VGroup()
  for k, (zh, en) in enumerate(props):
   a = np.pi / 2 + 2 * np.pi * k / 5
   d = np.array([np.cos(a), np.sin(a), 0.0])
   spokes.add(Line(CC + 1.02 * d, CC + np.array([2.55 * np.cos(a), 1.15 * np.sin(a), 0.0]),
                   color=ACCENT_C, stroke_width=2.2))
   m = self.lab(zh, en, FS_TAG, ACCENT_B)
   m.move_to(CC + np.array([(2.95 + 0.5 * m.width) * np.cos(a) * 0.92, 1.42 * np.sin(a), 0.0]))
   spokes.add(m)
  closing = VGroup(core, spokes)

  # ── run the beats ─────────────────────────────────────────────────
  active_sub = None; active_f = None
  def run(i, fin=(), fout=(), mid=(), at=0.55, extra=()):
   nonlocal active_sub, active_f
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
   self.beat(i, fin=fin, fout=fout, mid=mid, at=at, extra=extra)
   active_sub = s

  self.add(tower)
  run(0, fin=[intro])
  run(1, fin=[lens_tap, lens_beam, demo_panel], fout=[intro])
  run(2, fin=[jspace], fout=[demo_rows, lens_hdr, lens_box, lens_beam])
  run(3, fin=[frame, b3], fout=[jspace, tower, lens_tap],
      mid=swap(b3t, b3b, "rugby") + [Transform(b3o, self.big("Rugby", P3X, CARDY - 0.10))])
  run(4, fin=[b4], fout=[b3], mid=[FadeIn(b4note)]
      + [b.animate.stretch_to_fit_width(max(b.width * 0.42, 0.04), about_edge=np.array([-1, 0, 0]))
         .set_fill(DIM) for b in b4b])
  run(5, fin=[b5, b5note], fout=[b4, b4note],
      mid=swap(b5t, b5b, "ant") + [Transform(b5o, self.big("6", P3X, CARDY - 0.10, size=34))])
  run(6, fin=[b6], fout=[b5, b5note],
      mid=swap(b6t, b6b, "China")
      + [Transform(b6o[k], Text(b6n[k], font_size=FS_TOK, color=WARN)
                   .move_to([P3X, CARDY + 0.55 - k * 0.52, 0])) for k in range(3)])
  run(7, fin=[p3b, b7], fout=[b6, p3, p3_hdr, a23],
      mid=swap(b7t, b7b, "French"))
  run(8, fin=[board], fout=[frame, p3b, b7])
  run(9, fin=[hubign], fout=[board])
  run(10, fin=[closing], fout=[hubign])
  self.wait(.8)


def _mk(lang):
 return type(f"SpecialS01{'ZH' if lang == 'zh' else 'EN'}", (WorkspaceBase,), {"LANGUAGE": lang})

SpecialS01ZH = _mk("zh")
SpecialS01EN = _mk("en")
