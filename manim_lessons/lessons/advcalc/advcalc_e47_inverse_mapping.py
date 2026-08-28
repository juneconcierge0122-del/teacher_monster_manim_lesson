"""advcalc E47 -- chapter 3, section 11, second part (book pp. 166-167): the
existence half that E46 had to leave open.  Theorem 11.2 states it (its proof
waits for chapter 4's fixed point theorem), the local nature of the uniqueness
is shown on an equation with two branches, the reason the implicit function
comes out continuously differentiable is spelled out, and Theorem 11.3, the
inverse mapping theorem, is derived from it in one line, with its usual
corollary.  Pages 169-171 are exercises 11.1 to 11.29; E48 gives the Cartesian
forms.

Both examples are evaluated.  The branch equation has its second partial
differential computed at three points, two where it inverts and gives one
branch each, and one where it vanishes and the branches join.  The map of the
last beat is E43's, so its Jacobian and determinant are already familiar; here
its local inverse is found by Newton iteration and its Jacobian checked against
the inverse of the original's, which is the identity the beat claims.
"""
import math
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from manim import Dot, Line, Text, VGroup
from manim_lessons.lib.design_tokens import (ACCENT_A, ACCENT_B, ACCENT_C, DIM, INK, WARN)
from manim_lessons.lessons.advcalc.arrays import ArrayArt
from manim_lessons.lessons.canonical_base import CanonicalBase, make
from manim_lessons.localization.advcalc import TOPICS_ADVCALC, FORMULAS_ADVCALC

FS_TAG = 17
PANEL_X, PANEL_W = 3.55, 5.20
H = 1e-6


# ── beats 2 and 3: an equation with two branches ───────────────────────
def _Gb(xi, eta):
 return eta * eta - xi


BR_PTS = ((1.0, 1.0), (1.0, -1.0), (0.0, 0.0))
BR_D2 = [(_Gb(x, e + H) - _Gb(x, e - H)) / (2 * H) for x, e in BR_PTS]
for _p, _d in zip(BR_PTS, BR_D2):
 assert abs(_Gb(*_p)) < 1e-12, "a sample point is not on the curve"
assert abs(BR_D2[0]) > 1 and abs(BR_D2[1]) > 1, "the first two points should be invertible"
assert abs(BR_D2[2]) < 1e-9, "the third point is where the theorem must fail"
assert BR_D2[0] * BR_D2[1] < 0, "the two branches should have opposite signs there"


# ── beats 6 to 10: local but not global invertibility ──────────────────
def _Hm(x):
 return (x[0] ** 2 - x[1] ** 2, 2 * x[0] * x[1])


def _jac(f, a):
 cols = []
 for j in range(2):
  p, m = list(a), list(a)
  p[j] += H
  m[j] -= H
  cols.append(tuple((u - v) / (2 * H) for u, v in zip(f(tuple(p)), f(tuple(m)))))
 return tuple(tuple(cols[j][i] for j in range(2)) for i in range(2))


def _det(m):
 return m[0][0] * m[1][1] - m[0][1] * m[1][0]


PPT, QPT = (1.0, 0.5), (-1.0, -0.5)
assert _Hm(PPT) == _Hm(QPT), "these two points were chosen because they share an image"
assert PPT != QPT, "so the map is not injective, which is the point of the beat"
JH = tuple(tuple(round(x) for x in r) for r in _jac(_Hm, PPT))
DETH = _det(JH)
assert abs(DETH - 4 * (PPT[0] ** 2 + PPT[1] ** 2)) < 1e-9 and DETH == 5, \
    "the determinant moved from the value the beat prints"
assert abs(_det(_jac(_Hm, (0.0, 0.0)))) < 1e-9, "the origin is where invertibility fails"
INVH = tuple(tuple(round(x / DETH, 2) for x in r)
             for r in ((JH[1][1], -JH[0][1]), (-JH[1][0], JH[0][0])))

BPT = _Hm(PPT)


def _local_inverse(y, guess=PPT):
 x = list(guess)
 for _ in range(60):
  f = (_Hm(tuple(x))[0] - y[0], _Hm(tuple(x))[1] - y[1])
  j = _jac(_Hm, tuple(x))
  d = _det(j)
  x = [x[0] - (j[1][1] * f[0] - j[0][1] * f[1]) / d,
       x[1] - (-j[1][0] * f[0] + j[0][0] * f[1]) / d]
 return tuple(x)


assert max(abs(a - b) for a, b in zip(_local_inverse(BPT), PPT)) < 1e-9, \
    "the local inverse does not come back to the point it started from"
JINV = _jac(_local_inverse, BPT)
assert max(abs(a - b) for r, q in zip(JINV, INVH) for a, b in zip(r, q)) < 1e-4, \
    "the local inverse's Jacobian is not the inverse of the original's"


class AdvCalcE47Base(ArrayArt, CanonicalBase):
 TOPICS_SRC = TOPICS_ADVCALC
 FORMULAS_SRC = FORMULAS_ADVCALC
 AUDIO_PREFIX = "e"
 EPISODE = 47

 MODE_LABEL = {
  0: {"zh": "上一集留下的缺口", "en": "the gap the last episode left"},
  1: {"zh": "定理 11.2：存在性", "en": "Theorem 11.2: existence"},
  2: {"zh": "「唯一」是局部的", "en": "unique means locally unique"},
  3: {"zh": "兩支黏起來的地方", "en": "where the branches join"},
  4: {"zh": "為什麼微分也連續", "en": "why the differential is continuous too"},
  5: {"zh": "一點可逆，附近都可逆", "en": "invertible at a point, invertible nearby"},
  6: {"zh": "定理 11.3：反映射定理", "en": "Theorem 11.3: the inverse mapping theorem"},
  7: {"zh": "證明只有一行", "en": "the proof takes one line"},
  8: {"zh": "隱函數定理一套就完成", "en": "the implicit function theorem finishes it"},
  9: {"zh": "推論：熟悉的那個說法", "en": "the corollary: the familiar wording"},
  10: {"zh": "局部可逆，不是全域", "en": "locally invertible, not globally"},
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

 def _cross(self, ox, oy, w, h, col=DIM):
  return VGroup(Line([ox - w, oy, 0], [ox + w, oy, 0], color=col, stroke_width=1.6),
                Line([ox, oy - h, 0], [ox, oy + h, 0], color=col, stroke_width=1.6))

 def _circ(self, cx, cy, r, col, sw=2.0, n=72):
  return self._curve([[cx + r * math.cos(2 * math.pi * k / n),
                       cy + r * math.sin(2 * math.pi * k / n), 0] for k in range(n + 1)],
                     col, sw=sw)

 def _blob(self, cx, cy, rx, ry, wob, col, sw=2.5):
  pts = [[cx + rx * math.cos(t / 9.0) + wob * math.cos(3 * t / 9.0),
          cy + ry * math.sin(t / 9.0) - 0.6 * wob * math.sin(2 * t / 9.0), 0]
         for t in range(58)]
  return self._curve(pts + [pts[0]], col, sw=sw)

 def _parabola(self, cx, cy, s, col, lo, hi, sw=3):
  """The sideways parabola eta squared equals xi, over a range of eta."""
  return self._curve([[cx + s * (lo + (hi - lo) * k / 80) ** 2,
                       cy + s * (lo + (hi - lo) * k / 80), 0] for k in range(81)], col, sw=sw)

 # ── beats ─────────────────────────────────────────────────────────
 def _gap(self):
  g = VGroup()
  g.add(self._rect(-4.75, 0.48, 1.55, 0.32, ACCENT_B),
        self._sym(0.48, "dF ₐ   ∃", ACCENT_B, FS_TAG + 1, x=-4.75, w=2.90),
        self._rect(-4.75, -0.44, 1.55, 0.32, WARN),
        self._sym(-0.44, "F   ∃", WARN, FS_TAG + 1, x=-4.75, w=2.90))
  g.add(self._sym(0.48, "E 46", ACCENT_B, FS_TAG, x=-2.05, w=1.30),
        self._sym(-0.44, "E 47", WARN, FS_TAG, x=-2.05, w=1.30))
  for cy, col in ((0.48, ACCENT_B), (-0.44, WARN)):
   g.add(self._arr([-3.05, cy, 0], [-2.60, cy, 0], col, sw=2.5, tl=0.12))
  g.add(self._panel(((0.86, "上一集證的是上面那一條",
                      "the previous episode proved the upper one", ACCENT_B),
                     (0.20, "這一集講下面那一條",
                      "this one states the lower", WARN),
                     (-0.46, "但它的證明還是要等第 4 章",
                      "though its proof still waits for chapter four", DIM))))
  return g.add(self._foot("書上把存在性的證明推遲，是因為它要用不動點定理",
                          "the book postpones the existence proof because it needs the fixed point theorem",
                          ACCENT_A,
                          "陳述本身沒有推遲的理由，而且陳述才是實際會用到的部分",
                          "the statement itself need not wait, and the statement is what gets used"))

 def _thm112(self):
  g = VGroup()
  # the first row carries a word, so it is bilingual; the rest are symbols
  hyps = ((None, ACCENT_B),
          ("G   ∈   C ¹", ACCENT_C),
          ("G ( α , β )  =  0", WARN),
          ("( dG ² ) ⁻¹   ∃", ACCENT_A))
  for k, (lab, col) in enumerate(hyps):
   if k == 0:
    g.add(self._rect(-4.90, 0.80 - k * 0.52, 1.28, 0.22, col),
          self._mid(0.80 - k * 0.52, "空間完備", "the spaces are complete", col,
                    FS_TAG - 1, x=-4.90, w=2.40))
   else:
    g.add(self._rect(-4.90, 0.80 - k * 0.52, 1.28, 0.22, col),
          self._sym(0.80 - k * 0.52, lab, col, FS_TAG - 1, x=-4.90, w=2.40))
  g.add(self._rect(-1.85, -0.10, 1.45, 0.32, WARN),
        self._sym(-0.10, "∃ !  F  :  M → B", WARN, FS_TAG, x=-1.85, w=2.70))
  g.add(self._arr([-3.50, -0.10, 0], [-3.05, -0.10, 0], ACCENT_A, sw=3, tl=0.14))
  g.add(self._panel(((0.86, "四個假設，一個結論",
                      "four hypotheses and one conclusion", ACCENT_B),
                     (0.20, "結論裡的 F 連續可微，而且是唯一的",
                      "the F it returns is continuously differentiable and unique", WARN),
                     (-0.46, "而且它自動滿足 F ( α ) = β",
                      "and it automatically satisfies F of alpha equals beta", ACCENT_A))))
  return g.add(self._foot("有限維一定完備，所以在 ℝⁿ 上這個假設是自動成立的",
                          "finite dimensional spaces are complete, so in real n-space this is automatic",
                          ACCENT_A,
                          "完備性是第 4 章的主題，那裡也會證這條定理",
                          "completeness is chapter four's subject, and this theorem is proved there"))

 def _branches(self):
  cx, cy, s = -4.05, 0.05, 0.82
  g = VGroup(self._cross(cx, cy, 1.45, 1.00))
  g.add(self._parabola(cx, cy, s, ACCENT_C, 0.02, 1.15),
        self._parabola(cx, cy, s, WARN, -1.15, -0.02))
  for (x, e), col in zip(BR_PTS[:2], (ACCENT_C, WARN)):
   g.add(Dot([cx + s * x, cy + s * e, 0], radius=0.07, color=col))
  g.add(self._circ(cx + s * 1.0, cy + s * 1.0, 0.30, ACCENT_C, sw=1.6),
        self._circ(cx + s * 1.0, cy - s * 1.0, 0.30, WARN, sw=1.6))
  g.add(self._panel(((0.86, "同一個 ξ 有兩個解",
                      "the same xi has two solutions", ACCENT_A),
                     (0.20, "指定 β 就選定了一支",
                      "naming beta picks one branch", ACCENT_C),
                     (-0.46, "定理保證那顆小球上只有那一支",
                      "the theorem promises only that branch on the small ball", WARN))))
  return g.add(self._foot("「唯一」是在那顆球上唯一，不是整條曲線上唯一",
                          "unique means unique on that ball, not along the whole curve",
                          ACCENT_A,
                          "兩支各自都連續可微，兩顆球互不相干",
                          "each branch is continuously differentiable on its own, and the balls do not meet"))

 def _joint(self):
  cx, cy, s = -4.05, 0.05, 0.95
  g = VGroup(self._cross(cx, cy, 1.45, 1.00))
  g.add(self._parabola(cx, cy, s, DIM, -1.15, 1.15))
  g.add(Dot([cx, cy, 0], radius=0.08, color=WARN),
        self._circ(cx, cy, 0.40, WARN, sw=2))
  g.add(self._sym(0.86, f"dG ²  =  2 η  =  {BR_D2[2]:.0f}", WARN, FS_TAG + 1,
                  x=PANEL_X, w=PANEL_W),
        self._mid(0.20, "在原點兩支黏在一起", "at the origin the two branches join",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.36, "第二個偏微分等於零，定理不適用",
                  "the second partial differential vanishes, so the theorem is silent",
                  WARN, FS_TAG, x=PANEL_X, w=PANEL_W),
        self._mid(-0.92, "而且那裡確實沒有單值的解",
                  "and there genuinely is no single valued solution there", ACCENT_C,
                  FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("所以「可逆」不是技術性的裝飾，它剛好排除掉分支交會的地方",
                          "invertibility is no decoration: it excludes exactly where branches meet",
                          ACCENT_A,
                          "三個取樣點的第二個偏微分都是程式算的：2、−2、0",
                          "the second partial differential was computed at all three points: two, minus two, zero"))

 def _whyc1(self):
  g = VGroup()
  lines = (("dF   =   − ( dG ² ) ⁻¹  ∘  dG ¹", ACCENT_B),
           ("μ  ↦  dG ⁱ ( μ )                 T  ↦  T ⁻¹", ACCENT_C))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.72 - k * 0.66, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._rect(-3.55, -0.62, 2.05, 0.30, WARN),
        self._sym(-0.62, "dF   ∈   C ⁰", WARN, FS_TAG + 1, x=-3.55, w=3.90))
  g.add(self._panel(((0.86, "公式裡出現的每一樣東西都連續",
                      "everything appearing in the formula is continuous", ACCENT_B),
                     (0.20, "「取反元素」在算子範數下也是連續的",
                      "and taking an inverse is continuous in the operator norm", ACCENT_C),
                     (-0.46, "所以整條公式對點連續",
                      "so the whole formula depends continuously on the point", WARN))))
  return g.add(self._foot("連續可微比可微強，而這裡是白得的——不必另外付代價",
                          "continuously differentiable is stronger than differentiable, and comes free here",
                          ACCENT_A,
                          "後面每次要「連續可微」的假設時，這條就是來源",
                          "every later hypothesis of continuous differentiability traces back to this"))

 def _nearby(self):
  cx, cy = -3.95, 0.05
  g = VGroup(self._blob(cx, cy, 1.45, 0.85, 0.16, DIM))
  g.add(Dot([cx - 0.15, cy + 0.10, 0], radius=0.075, color=WARN),
        self._circ(cx - 0.15, cy + 0.10, 0.62, WARN, sw=2))
  for dx, dy in ((-0.45, 0.28), (0.25, -0.20), (0.05, 0.35)):
   g.add(Dot([cx - 0.15 + dx, cy + 0.10 + dy, 0], radius=0.05, color=ACCENT_C))
  g.add(self._panel(((0.86, "紅點那裡第二個偏微分可逆",
                      "at the red point the second partial differential inverts", WARN),
                     (0.20, "可逆是一個開條件，所以附近整片都可逆",
                      "invertibility is an open condition, so a whole patch does", ACCENT_C),
                     (-0.46, "於是 F 在整個鄰域上可微",
                      "so F is differentiable throughout the neighborhood", ACCENT_A))))
  return g.add(self._foot("「可逆的算子構成開集」是 E35 的算子範數給的",
                          "that the invertible operators form an open set comes from E35's operator norm",
                          ACCENT_A,
                          "所以一點的假設就撐出一整片的結論，這在分析裡很常見",
                          "an assumption at one point buys a conclusion on a whole patch, a common pattern"))

 def _thm113(self):
  dx, rx, cy = -5.05, -1.95, 0.05
  g = VGroup(self._blob(dx, cy, 1.05, 0.72, 0.12, ACCENT_B),
             self._blob(rx, cy, 1.05, 0.72, 0.12, ACCENT_C))
  g.add(Dot([dx - 0.10, cy + 0.05, 0], radius=0.07, color=WARN),
        Dot([rx - 0.10, cy + 0.05, 0], radius=0.07, color=WARN))
  g.add(self._arr([dx + 1.15, cy + 0.26, 0], [rx - 1.15, cy + 0.26, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([rx - 1.15, cy - 0.26, 0], [dx + 1.15, cy - 0.26, 0], WARN, sw=2.5, tl=0.12))
  g.add(self._sym(cy + 0.52, "H", ACCENT_A, FS_TAG, x=(dx + rx) / 2, w=0.80),
        self._sym(cy - 0.54, "F", WARN, FS_TAG, x=(dx + rx) / 2, w=0.80))
  g.add(self._panel(((0.86, "H 連續可微，微分在 β 可逆",
                      "H is continuously differentiable with invertible differential at beta", ACCENT_B),
                     (0.20, "那麼 H 在 β 附近就可逆",
                      "then H is invertible near beta", WARN),
                     (-0.46, "反函數也連續可微",
                      "and the inverse is continuously differentiable too", ACCENT_C))))
  return g.add(self._foot("這是隱函數定理的特例，可是它有自己的名字，因為用得太頻繁",
                          "a special case of the implicit function theorem, named separately because it is used so often",
                          ACCENT_A,
                          "第 4、5 章與後面的流形理論都會反覆引用它",
                          "chapters four and five and the later manifold theory quote it repeatedly"))

 def _oneline(self):
  g = VGroup()
  g.add(self._rect(-3.55, 0.42, 2.35, 0.34, ACCENT_B),
        self._sym(0.42, "G ( ξ , η )    =    ξ   −   H ( η )", ACCENT_B, FS_TAG + 2,
                  x=-3.55, w=4.50))
  g.add(self._sym(-0.42, "dG ²    =    −  dH ᵦ", WARN, FS_TAG + 2, x=-3.55, w=4.50))
  g.add(self._panel(((0.86, "把要證的東西寫成一個隱函數問題",
                      "write the thing to be proved as an implicit function problem", ACCENT_B),
                     (0.20, "這個 G 顯然連續可微",
                      "this G is plainly continuously differentiable", ACCENT_C),
                     (-0.46, "它對第二個變數的偏微分就是負的 dH",
                      "its partial differential in the second variable is minus dH", WARN))))
  return g.add(self._foot("dH 可逆，負的它當然也可逆，所以隱函數定理的假設全部滿足",
                          "dH inverts, so minus it does, and every hypothesis is met",
                          ACCENT_A,
                          "把一個問題改寫成另一個已解決的問題，是這一章反覆用的手法",
                          "rewriting one problem as another already solved is this chapter's recurring move"))

 def _finish(self):
  g = VGroup()
  lines = (("G ( ξ , F ( ξ ) )   =   0", ACCENT_B),
           ("ξ   −   H ( F ( ξ ) )   =   0", ACCENT_C),
           ("H  ∘  F    =    I", WARN))
  for k, (lab, col) in enumerate(lines):
   g.add(self._sym(0.80 - k * 0.62, lab, col, FS_TAG + 1, x=-3.55, w=5.20))
  g.add(self._panel(((0.86, "隱函數定理交出來的 F",
                      "the F the implicit function theorem returns", ACCENT_B),
                     (0.20, "代回 G 的定義",
                      "substituted back into the definition of G", ACCENT_C),
                     (-0.46, "就是「H 接上 F 是恆等映射」",
                      "says exactly that H after F is the identity", WARN))))
  return g.add(self._foot("所以 F 就是 H 的局部反函數，而且它連續可微",
                          "so F is the local inverse of H, and it is continuously differentiable",
                          ACCENT_A,
                          "另一邊的恆等式（F 接上 H）要多做一點功夫，書上留成習題",
                          "the identity the other way round takes a little more work and is left as an exercise"))

 def _corollary(self):
  dx, rx, cy = -4.95, -1.85, 0.05
  g = VGroup(self._blob(dx, cy, 1.08, 0.80, 0.13, DIM),
             self._blob(rx, cy, 1.08, 0.80, 0.13, DIM))
  g.add(self._circ(dx - 0.12, cy + 0.06, 0.46, ACCENT_B, sw=2.5),
        self._blob(rx - 0.05, cy + 0.04, 0.52, 0.36, 0.07, WARN, sw=2.5))
  g.add(Dot([dx - 0.12, cy + 0.06, 0], radius=0.065, color=ACCENT_A),
        Dot([rx - 0.05, cy + 0.04, 0], radius=0.065, color=ACCENT_A))
  g.add(self._arr([dx + 1.22, cy + 0.30, 0], [rx - 1.22, cy + 0.30, 0], ACCENT_A, sw=2.5, tl=0.12),
        self._arr([rx - 1.22, cy - 0.30, 0], [dx + 1.22, cy - 0.30, 0], DIM, sw=2, tl=0.10))
  g.add(self._sym(cy + 0.90, "U", ACCENT_B, FS_TAG, x=dx - 0.12, w=0.70),
        self._sym(cy + 0.90, "N  =  H [ U ]", WARN, FS_TAG, x=rx - 0.05, w=1.90))
  g.add(self._panel(((0.86, "β 有一個開鄰域，H 在上面是單射",
                      "beta has an open neighborhood on which H is injective", ACCENT_B),
                     (0.20, "它的像也是開集",
                      "its image is an open set too", WARN),
                     (-0.46, "而反函數在那個開集上連續可微",
                      "and the inverse is continuously differentiable there", ACCENT_A))))
  return g.add(self._foot("每一句都是局部的：沒有一句話說 H 在整個定義域上可逆",
                          "every clause is local: none of them says H is invertible on its whole domain",
                          ACCENT_A,
                          "「像是開集」這一句在後面談流形時特別重要",
                          "that the image is open matters especially in the later theory of manifolds"))

 def _example(self):
  # A first version set the two coordinate crosses side by side with nothing
  # between them; the probe frame showed one smeared plane with a stray vertical
  # line through it, and no way to tell domain from image. Frame each plane and
  # leave a gap between them for the arrows.
  cy, s, hw, hh = 0.25, 0.58, 0.92, 0.62
  cx, rx = -5.05, -1.65
  g = VGroup()
  for ox in (cx, rx):
   g.add(self._rect(ox, cy, hw + 0.22, hh + 0.18, DIM, sw=1.2),
         self._cross(ox, cy, hw, hh))
  bx, by = rx + s * BPT[0], cy + s * BPT[1]
  for p, col in ((PPT, ACCENT_B), (QPT, ACCENT_C)):
   px, py = cx + s * p[0], cy + s * p[1]
   g.add(Dot([px, py, 0], radius=0.07, color=col),
         self._arr([px + 0.14, py, 0], [bx - 0.14, by, 0], col, sw=1.6, tl=0.10))
  g.add(Dot([bx, by, 0], radius=0.075, color=WARN))
  g.add(self._sym(cy - hh - 0.34, "⟨ x ₁ , x ₂ ⟩", DIM, FS_TAG - 1, x=cx, w=2.20),
        self._sym(cy - hh - 0.34, "H ( x )", WARN, FS_TAG - 1, x=rx, w=2.20))
  gr, _ = self._numgrid(3.10, 0.44, [[f"{x:.0f}" for x in r] for r in JH],
                        color=ACCENT_A, dx=0.66, dy=0.46)
  gr2, _ = self._numgrid(5.30, 0.44, [[f"{x:.2f}" for x in r] for r in INVH],
                         color=WARN, dx=0.86, dy=0.46)
  g.add(gr, gr2, self._sym(0.44, "→", DIM, FS_TAG + 2, x=4.20, w=0.60),
        self._sym(-0.30, "dH ᵦ", ACCENT_A, FS_TAG - 1, x=3.10, w=1.30),
        self._sym(-0.30, "( dH ᵦ ) ⁻¹  =  dF ₐ", WARN, FS_TAG - 1, x=5.30, w=2.20))
  g.add(self._mid(-0.90, "兩個相反的點有同一個像，所以全域不是單射",
                  "two opposite points share an image, so globally it is not injective",
                  ACCENT_A, FS_TAG, x=PANEL_X, w=PANEL_W))
  return g.add(self._foot("這就是 E43 那個映射，行列式是 4 乘長度平方，只在原點是零",
                          "this is E43's map, whose determinant is four times the squared length",
                          ACCENT_A,
                          "所以除了原點以外處處局部可逆，但沒有一處是全域可逆",
                          "so it is locally invertible everywhere but the origin, and globally invertible nowhere"))

 def stage(self):
  a, b, c = self._gap(), self._thm112(), self._branches()
  d, e, f = self._joint(), self._whyc1(), self._nearby()
  h, i, j = self._thm113(), self._oneline(), self._finish()
  k, l = self._corollary(), self._example()
  return [([a], []), ([b], [a]), ([c], [b]), ([d], [c]),
          ([e], [d]), ([f], [e]), ([h], [f]), ([i], [h]),
          ([j], [i]), ([k], [j]), ([l], [k])]


AdvCalcE47ZH, AdvCalcE47EN = make(AdvCalcE47Base, "47", prefix="AdvCalcE")
