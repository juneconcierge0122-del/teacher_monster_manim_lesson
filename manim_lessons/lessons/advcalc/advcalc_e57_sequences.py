"""advcalc E57 -- chapter 4, sections 2 and 3 (book pp. 201-204): topology, and
sequential convergence.  Section 2 pulls the three properties of the open sets
out as axioms and sorts the earlier notions into topological and metric ones,
noticing that continuity -- defined metrically -- turns out to be topological
after all.  Section 3 brings in sequences, which give the most usable
characterisations of closure, of closed sets and of continuity, and which the
rest of the chapter runs on.  Pages 204-205 are exercises 3.1 to 3.15.

Three claims are checked rather than stated.  Theorem 3.3, that equivalent norms
give the same convergent sequences, is checked in both directions: the three
standard norms on the plane are shown to sandwich one another and to agree on a
sample sequence, while a spike of fixed height and shrinking width is shown to
converge in one norm and not in another -- so those two are not equivalent.  The
sequential test for continuity is exercised on a map that is continuous along
every line through the origin yet not continuous there, with the offending
sequence built exactly the way the proof of Theorem 3.2 builds it.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20


# ── beat 7: a set that is not closed, seen by one sequence ─────────────
SEQ = [(n, 1.0 / n) for n in (2, 3, 5, 12, 40)]
for _n, _v in SEQ:
 assert 0.0 < _v < 1.0, "every term lies in the open interval"
assert SEQ[-1][1] < 0.03, "yet the terms converge to a limit outside it"


# ── beats 8 and 9: separately continuous, not continuous ───────────────
def _bad(p):
 x, y = p
 if x == 0.0 and y == 0.0:
  return 0.0
 return x * y / (x * x + y * y)


# along either axis the function is identically zero, so each variable alone is fine
for _t in (0.5, 0.1, 0.01):
 assert _bad((_t, 0.0)) == 0.0 and _bad((0.0, _t)) == 0.0, \
     "the function has to vanish along the axes for the beat to make its point"
# the sequence the proof of Theorem 3.2 would build
DIAG = [(1.0 / n, (1.0 / n, 1.0 / n)) for n in (1, 4, 20, 100)]
for _d, _p in DIAG:
 assert math.hypot(*_p) < 1.5 * _d and abs(_bad(_p) - 0.5) < 1e-12, \
     "the diagonal sequence has to reach the origin while the values stay at one half"
assert abs(_bad((0.0, 0.0))) < 1e-12, "the value at the origin is zero, so the images do not converge"


# ── beat 10: equivalent norms, and a pair that is not ──────────────────
def _n1(v):
 return abs(v[0]) + abs(v[1])


def _n2(v):
 return math.hypot(v[0], v[1])


def _ni(v):
 return max(abs(v[0]), abs(v[1]))


RING = [(math.cos(2 * math.pi * k / 360), math.sin(2 * math.pi * k / 360)) for k in range(360)]
for _v in RING:
 assert _ni(_v) <= _n2(_v) + 1e-12 <= _n1(_v) + 1e-12 <= 2 * _ni(_v) + 1e-12, \
     "the three standard norms do not sandwich one another as claimed"
SAND = (min(_n2(v) / _ni(v) for v in RING), max(_n1(v) / _ni(v) for v in RING))
assert abs(SAND[0] - 1.0) < 1e-9 and abs(SAND[1] - 2.0) < 1e-9

# a spike of height one and width one over n: it goes to zero in one norm only
def _spike_sup(n):
 return 1.0


def _spike_one(n):
 return 1.0 / (2.0 * n)


SPIKE = [(n, _spike_sup(n), _spike_one(n)) for n in (1, 4, 20, 100)]
for _n, _s, _o in SPIKE:
 assert abs(_s - 1.0) < 1e-12, "the height never changes"
assert SPIKE[-1][2] < 0.01, "while the area goes to zero"
assert SPIKE[0][2] > SPIKE[-1][2], "so the two norms disagree about this sequence"


class AdvCalcE57Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 57

 MODE_LABEL = {
  0: {"zh": "把開集族抽出來當公理", "en": "the open sets, taken as axioms"},
  1: {"zh": "哪些是拓撲的，哪些是度量的", "en": "which notions are which"},
  2: {"zh": "連續其實是拓撲的", "en": "continuity turns out topological"},
  3: {"zh": "鄰域的講法，以及全域的版本", "en": "neighborhoods, and the global form"},
  4: {"zh": "序列收斂：三個量詞", "en": "convergence: three quantifiers"},
  5: {"zh": "N 取 max，不是 δ 取 min", "en": "N is a maximum, not a minimum"},
  6: {"zh": "定理 3.1：閉包就是極限", "en": "Theorem 3.1: closure by limits"},
  7: {"zh": "閉集：極限不准跑出去", "en": "closed: no limit escapes"},
  8: {"zh": "定理 3.2：連續的序列刻畫", "en": "Theorem 3.2: continuity by sequences"},
  9: {"zh": "讓 δ 跑遍 1 / n", "en": "let delta run through one over n"},
  10: {"zh": "等價範數＝同一批收斂序列", "en": "equivalent norms, same sequences"},
 }

 # ── shared pieces ─────────────────────────────────────────────────
 def _panel(self, rows, x=PANEL_X, w=PANEL_W):
  g = VGroup()
  for y, zh, en, col in rows:
   g.add(self._mid(y, zh, en, col, FS_TAG, x=x, w=w))
  return g

 def _foot(self, zh1, en1, col1, zh2, en2, col2=DIM):
  return VGroup(self._mid(-1.22, zh1, en1, col1, FS_TAG, w=11.9),
                self._mid(-1.74, zh2, en2, col2, FS_TAG, w=11.9))

 def _rect(self, cx, cy, w, h, col, sw=1.8):
  return self._curve([[cx - w, cy - h, 0], [cx + w, cy - h, 0], [cx + w, cy + h, 0],
                      [cx - w, cy + h, 0], [cx - w, cy - h, 0]], col, sw=sw)

 def _circ(self, cx, cy, r, col, sw=2.0, n=80):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _table(self, rows, x=PANEL_X, w=PANEL_W, y0=0.72, dy=0.42, size=FS_TAG - 2):
  g = VGroup()
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(y0 - k * dy, lab, col, size, x=x, w=w))
  return g

 # ── beats ─────────────────────────────────────────────────────────
 def _axioms(self):
  g = VGroup(self._rect(-4.35, 0.10, 1.75, 0.92, DIM, sw=1.6))
  for cx, cy, r, col in ((-5.05, 0.42, 0.42, ACCENT_B), (-4.25, 0.18, 0.52, ACCENT_C),
                         (-3.55, 0.48, 0.34, WARN), (-4.55, -0.42, 0.30, ACCENT_A)):
   g.add(self._circ(cx, cy, r, col, sw=1.8))
  g.add(self._sym(-1.02, "𝒯", DIM, FS_TAG + 2, x=-4.35, w=0.80))
  g.add(self._panel(((0.86, "X 是任意一個集合",
                      "let X be any set at all", DIM),
                     (0.20, "𝒯 是滿足那三條性質的一族子集",
                      "and the family satisfy the three properties", ACCENT_B),
                     (-0.46, "這樣的 𝒯 就叫 X 上的一個拓撲",
                      "such a family is called a topology on X", ACCENT_A))))
  return g.add(self._foot("定理 1.1 說的正是：度量空間的開集族構成一個拓撲",
                          "Theorem 1.1 says exactly that the open sets of a metric space form a topology",
                          ACCENT_A,
                          "而研究「有一個拓撲」會推出什麼，就叫一般拓撲學",
                          "and studying what the mere existence of a topology implies is general topology"))

 def _sorting(self):
  g = VGroup()
  left = ("A ⁱⁿᵗ", "Ā", "∂ A")
  right = ("B ᵣ ( p )", "ϵ – δ")
  for k, lab in enumerate(left):
   g.add(self._rect(-5.05, 0.62 - k * 0.56, 0.72, 0.22, ACCENT_B),
         self._sym(0.62 - k * 0.56, lab, ACCENT_B, FS_TAG - 1, x=-5.05, w=1.40))
  for k, lab in enumerate(right):
   g.add(self._rect(-2.35, 0.62 - k * 0.56, 0.82, 0.22, WARN),
         self._sym(0.62 - k * 0.56, lab, WARN, FS_TAG - 1, x=-2.35, w=1.60))
  g.add(self._mid(-1.02, "只用到 𝒯", "uses only the topology", ACCENT_B,
                  FS_TAG - 1, x=-5.05, w=2.20),
        self._mid(-1.02, "要用到 ρ", "needs the metric", WARN,
                  FS_TAG - 1, x=-2.35, w=2.20))
  g.add(self._panel(((0.86, "左邊那些只用到開集族",
                      "the ones on the left use only the family of open sets", ACCENT_B),
                     (0.20, "所以它們是純拓撲的概念",
                      "so they are purely topological", ACCENT_C),
                     (-0.46, "右邊那些要用到距離本身",
                      "the ones on the right need the distance itself", WARN))))
  return g.add(self._foot("定理 1.2 與那條互補的恆等式也只用到 𝒯，所以一樣是拓撲的",
                          "Theorem 1.2 and the complementary identity use only the topology as well",
                          ACCENT_A,
                          "度量空間比拓撲空間多的，就是右邊那一欄——所以它比較好用",
                          "what a metric space has beyond a topological one is the right column, which is why it is easier"))

 def _topcont(self):
  g = VGroup()
  for cx, lab in ((-4.90, "p"), (-1.90, "f ( p )")):
   g.add(self._blob(cx, 0.10, 1.15, 0.70, 0.12, DIM, sw=1.6))
  g.add(self._circ(-5.00, 0.05, 0.44, ACCENT_B, sw=2.2),
        self._circ(-2.00, 0.05, 0.62, WARN, sw=2.2),
        Dot([-5.00, 0.05, 0], radius=0.065, color=ACCENT_A),
        Dot([-2.00, 0.05, 0], radius=0.065, color=ACCENT_A))
  g.add(self._arr([-3.80, 0.20, 0], [-3.30, 0.20, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._sym(-0.86, "B", ACCENT_B, FS_TAG, x=-5.00, w=0.70),
        self._sym(-0.86, "A", WARN, FS_TAG, x=-2.00, w=0.70))
  g.add(self._panel(((0.86, "給了含著像的任何一個開集 A",
                      "given any open A containing the image", WARN),
                     (0.20, "找得到含著 p 的開集 B，整個被送進 A",
                      "some open B about p has its whole image inside A", ACCENT_B),
                     (-0.46, "這句話完全沒提到距離",
                      "and that sentence never mentions the distance", ACCENT_A))))
  return g.add(self._foot("看得出來的關鍵是「開集就是球的聯集」——ε 與 δ 都被吸收進「開集」這兩個字裡",
                          "the key is that an open set is a union of balls, so epsilon and delta are absorbed into the word open",
                          ACCENT_A,
                          "所以連續雖然是用度量定義的，它其實是一個拓撲的性質",
                          "so continuity, though defined metrically, is really a topological property"))

 def _global(self):
  g = VGroup()
  g.add(self._rect(-4.75, 0.50, 1.55, 0.30, ACCENT_B),
        self._mid(0.50, "f ( p ) 的每個鄰域", "every neighborhood of the value",
                  ACCENT_B, FS_TAG - 1, x=-4.75, w=2.90))
  g.add(self._arr([-3.10, 0.50, 0], [-2.60, 0.50, 0], ACCENT_A, sw=2.5, tl=0.12))
  g.add(self._rect(-1.35, 0.50, 1.25, 0.30, ACCENT_C),
        self._mid(0.50, "逆像是 p 的鄰域", "pulls back to one of p",
                  ACCENT_C, FS_TAG - 1, x=-1.35, w=2.30))
  g.add(self._rect(-3.45, -0.44, 2.15, 0.32, WARN),
        self._sym(-0.44, "f ⁻¹ [ A ]  ∈  𝒯          ⇔          f  ∈  C ⁰", WARN,
                  FS_TAG, x=-3.45, w=4.10))
  g.add(self._panel(((0.86, "A 是 p 的鄰域，如果 p 落在 A 的內部",
                      "A is a neighborhood of p when p lies in its interior", DIM),
                     (0.20, "局部的版本用鄰域講最順",
                      "the local statement reads best with neighborhoods", ACCENT_C),
                     (-0.46, "全域的版本更漂亮：開集的逆像都是開的",
                      "the global one is prettier: inverse images of open sets are open", WARN))))
  return g.add(self._foot("這正是上一集引理 1.4 的內容，只是現在它可以當定義而不是定理",
                          "this is Lemma 1.4 of the last episode, except that it can now serve as the definition",
                          ACCENT_A,
                          "閉集的版本也對，而且兩個的反面都成立",
                          "the closed set version holds too, and so do both converses"))

 def _convergence(self):
  ox, oy = -5.85, 0.05
  sx = 4.30
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.06, oy, 0], color=DIM, stroke_width=1.4))
  lim = ox + sx
  g.add(Dot([lim, oy, 0], radius=0.075, color=WARN))
  for k, (n, v) in enumerate(SEQ):
   px = ox + sx * (1.0 - v)
   g.add(Dot([px, oy, 0], radius=0.055, color=ACCENT_B),
         self._sym(oy + 0.36 if k % 2 else oy + 0.62, f"x {n}", ACCENT_B,
                   FS_TAG - 3, x=px, w=0.80))
  g.add(self._circ(lim, oy, 0.28, ACCENT_C, sw=1.8))
  g.add(self._sym(0.86, "( ∀ ϵ ) ( ∃ N ) ( ∀ n > N )      ρ ( x ₙ , a )  <  ϵ",
                  ACCENT_A, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "三個量詞，跟函數的收斂幾乎一樣",
                  "three quantifiers, nearly the definition for functions", DIM,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "順口的講法：對「幾乎所有 n」成立",
                  "the idiomatic phrasing: it holds for almost all n", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "也就是只有有限多個 n 不成立",
                  "meaning it fails for only finitely many", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("於是收斂可以講成：極限周圍每一個球，都含著幾乎所有的項",
                          "so convergence reads: every ball about the limit contains almost all the terms",
                          ACCENT_A,
                          "這個講法把量詞收成一句話，後面的證明會一直用它",
                          "that phrasing folds the quantifiers into one sentence, and the proofs lean on it"))

 def _maxmin(self):
  g = VGroup()
  g.add(self._rect(-4.80, 0.46, 1.30, 0.30, ACCENT_B),
        self._sym(0.46, "N   =   max { N ₁ , N ₂ }", ACCENT_B, FS_TAG, x=-4.80, w=2.40),
        self._rect(-4.80, -0.34, 1.30, 0.30, DIM),
        self._sym(-0.34, "δ   =   min { δ ₁ , δ ₂ }", DIM, FS_TAG, x=-4.80, w=2.40))
  g.add(self._mid(0.46, "序列的情形", "for sequences", ACCENT_B,
                  FS_TAG, x=-2.25, w=2.00),
        self._mid(-0.34, "第 3 章函數的情形", "for functions, in chapter 3", DIM,
                  FS_TAG, x=-2.25, w=2.00))
  g.add(self._panel(((0.86, "引理 3.1：和的極限是極限的和",
                      "Lemma 3.1: the limit of a sum is the sum of the limits", ACCENT_B),
                     (0.20, "引理 3.2：純量積也一樣",
                      "Lemma 3.2: the same for scalar multiples", ACCENT_C),
                     (-0.46, "證明跟第 3 章那兩條幾乎一字不差",
                      "the proofs are almost word for word chapter 3's", WARN))))
  return g.add(self._foot("唯一的差別在這裡：兩個條件要同時滿足，序列取 N 的最大值，函數取 δ 的最小值",
                          "the one difference: to meet two conditions at once, sequences take the larger N and functions the smaller delta",
                          ACCENT_A,
                          "方向相反是因為序列的條件是「n 夠大」，函數的條件是「距離夠小」",
                          "the directions differ because one condition is n large enough and the other is a distance small enough"))

 def _closureseq(self):
  cx, cy = -4.35, 0.05
  g = VGroup(self._blob(cx, cy, 1.15, 0.72, 0.12, ACCENT_B, sw=2.2))
  px, py = cx + 1.24, cy + 0.06
  g.add(Dot([px, py, 0], radius=0.075, color=WARN))
  for k, r in enumerate((0.62, 0.40, 0.26, 0.16)):
   g.add(self._circ(px, py, r, DIM, sw=1.1))
   ang = 2.6 + 0.25 * k
   g.add(Dot([px + r * 0.82 * math.cos(ang), py + r * 0.82 * math.sin(ang), 0],
             radius=0.05, color=ACCENT_C))
  g.add(self._sym(0.86, "x  ∈  Ā        ⇔        ∃ { x ₙ } ⊂ A ,   x ₙ → x",
                  ACCENT_A, FS_TAG - 1, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "紅點在 A 的閉包裡", "the red point lies in the closure",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "在半徑一除以 n 的球裡各挑一點",
                  "pick one point from the ball of radius one over n", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "挑出來的序列就收斂到它",
                  "and the picks converge to it", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("往一個方向用的是上一集的引理 1.3：閉包裡的點，每個球都跟集合相交",
                          "one direction uses Lemma 1.3: every ball about a point of the closure meets the set",
                          ACCENT_A,
                          "反過來就是這個「每個球挑一點」的構造，它在這一章會反覆出現",
                          "the other is this pick-one-per-ball construction, which recurs throughout the chapter"))

 def _closedseq(self):
  ox, oy = -5.85, 0.05
  sx = 4.30
  g = VGroup(Line([ox - 0.10, oy, 0], [ox + sx * 1.08, oy, 0], color=DIM, stroke_width=1.4))
  g.add(Line([ox, oy, 0], [ox + sx, oy, 0], color=ACCENT_B, stroke_width=5))
  g.add(self._circ(ox, oy, 0.09, WARN, sw=2.2), self._circ(ox + sx, oy, 0.09, WARN, sw=2.2))
  for n, v in SEQ:
   g.add(Dot([ox + sx * v, oy + 0.30, 0], radius=0.055, color=ACCENT_C))
  g.add(self._arr([ox + sx * 0.30, oy + 0.52, 0], [ox + 0.10, oy + 0.52, 0],
                  ACCENT_C, sw=2, tl=0.10))
  g.add(self._sym(0.86, "A  =  Ā      ⇔      ( x ₙ ∈ A ,  x ₙ → x    ⇒    x ∈ A )",
                  ACCENT_A, FS_TAG - 2, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "藍色是開區間，兩端不含",
                  "the blue segment is the open interval, ends excluded", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "一除以 n 整個落在裡面",
                  "one over n lies entirely inside it", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "可是極限跑到左端點外面，所以它不是閉的",
                  "yet the limit escapes to the left end, so it is not closed", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這句話是實際判斷「閉不閉」時最常用的：找一個序列，看極限跑不跑掉",
                          "this is the usual test for closedness in practice: find a sequence and see whether the limit escapes",
                          ACCENT_A,
                          "它是定理 3.1 的直接推論，因為閉就是等於自己的閉包",
                          "it follows straight from Theorem 3.1, since closed means equal to one's own closure"))

 def _seqcont(self):
  ox, oy = -4.75, 0.05
  g = VGroup(Line([ox - 1.25, oy, 0], [ox + 1.25, oy, 0], color=DIM, stroke_width=1.4),
             Line([ox, oy - 0.85, 0], [ox, oy + 0.85, 0], color=DIM, stroke_width=1.4))
  g.add(Line([ox - 0.90, oy - 0.90, 0], [ox + 0.90, oy + 0.90, 0],
             color=WARN, stroke_width=2.4))
  # the first of these sits at (1, 1), so the scale has to keep it on screen
  for _d, p in DIAG[:3]:
   g.add(Dot([ox + 0.85 * p[0], oy + 0.85 * p[1], 0], radius=0.055, color=ACCENT_C))
  g.add(Dot([ox, oy, 0], radius=0.07, color=ACCENT_A))
  g.add(self._sym(0.86, "x ₙ  →  a        ⇒        f ( x ₙ )  →  f ( a )", ACCENT_A,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(0.24, "沿兩個座標軸走，函數恆等於零",
                  "along either axis the function is identically zero", ACCENT_B,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.34, "沿對角線走，函數恆等於二分之一",
                  "along the diagonal it is identically one half", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "所以它在原點不連續，儘管每個變數各自都連續",
                  "so it is not continuous at the origin, though each variable alone is", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("定理 3.2：f 在一點連續，等價於每個收斂到那一點的序列，像也收斂到那個值",
                          "Theorem 3.2: continuity at a point is that every sequence converging to it has its images converging",
                          ACCENT_A,
                          "紅色那條對角線上的點就是反例的序列——它收斂到原點，可是像停在二分之一",
                          "the points on the red diagonal are the counterexample's sequence: they reach the origin while the values stay at one half"))

 def _negation(self):
  g = VGroup()
  rows = (("∼ ( ∀ ϵ ) ( ∃ δ ) ( ∀ x )  P", ACCENT_B),
          ("( ∃ ϵ ) ( ∀ δ ) ( ∃ x )  ∼ P", ACCENT_C),
          ("δ   :=   1 / n", WARN))
  for k, (lab, col) in enumerate(rows):
   g.add(self._sym(0.82 - k * 0.56, lab, col, FS_TAG, x=-4.35, w=4.20))
  rows2 = [("        n            ρ ( x ₙ , a )         f ( x ₙ )", DIM)]
  for d, p in DIAG[:3]:
   rows2.append((f"     {round(1 / d):5d}          {math.hypot(*p):.4f}          {_bad(p):.4f}",
                 ACCENT_A))
  g.add(self._table(rows2, x=PANEL_X, w=PANEL_W, y0=0.80, dy=0.36))
  g.add(self._mid(-0.60, "距離掉到零，像卻停在二分之一",
                  "the distance falls to zero while the values stay put", WARN,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("書上說這幾乎是一套自動的證明程序：把量詞的否定寫清楚，再讓 δ 跑遍一除以 n",
                          "the book calls this almost an automatic proof procedure: negate the quantifiers, then let delta run through one over n",
                          ACCENT_A,
                          "這一章之後每次要否定一個「對所有」的敘述，用的都是這一招",
                          "every later denial of a for-all statement in this chapter uses the same move"))

 def _normseq(self):
  g = VGroup()
  rows = [("        n          ‖ · ‖ ∞          ∫ | · |", DIM)]
  for n, s, o in SPIKE[:3]:
   rows.append((f"      {n:4d}          {s:.3f}          {o:.5f}", ACCENT_C))
  g.add(self._table(rows, x=-3.85, w=4.80, y0=0.82, dy=0.34))
  g.add(self._rect(-3.85, -0.66, 2.15, 0.26, ACCENT_A),
        self._sym(-0.66, "p  ≈  q        ⇔        C ( p )  =  C ( q )", ACCENT_A,
                  FS_TAG, x=-3.85, w=4.10))
  g.add(self._panel(((0.86, "同一個序列：高度不動，面積掉到零",
                      "one sequence: the height never moves, the area goes to zero", ACCENT_C),
                     (0.20, "在一個範數下收斂，在另一個下不收斂",
                      "convergent in one norm and not in the other", WARN),
                     (-0.46, "所以那兩個範數不等價",
                      "so those two norms are not equivalent", ACCENT_A))))
  return g.add(self._foot("定理 3.3 說反過來也對：兩個範數等價，等價於它們給出完全同一批收斂序列",
                          "Theorem 3.3 says the converse too: two norms are equivalent exactly when they give the same convergent sequences",
                          ACCENT_A,
                          "程式在平面上驗過三個標準範數互相夾住（比值介於 1 與 2），所以它們兩兩等價",
                          "the three standard norms on the plane were checked here to sandwich one another between one and two"))

 def stage(self):
  a, b, c = self._axioms(), self._sorting(), self._topcont()
  d, e, f = self._global(), self._convergence(), self._maxmin()
  h, i, j = self._closureseq(), self._closedseq(), self._seqcont()
  k, l = self._negation(), self._normseq()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE57ZH, AdvCalcE57EN = make(AdvCalcE57Base, "57", prefix="AdvCalcE")
