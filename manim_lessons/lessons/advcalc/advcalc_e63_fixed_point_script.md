# advcalc E63 — 第 4 章：壓縮映射不動點定理

Chapter 4: The Contraction Mapping Fixed-Point Theorem

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 9 節「壓縮映射不動點定理」的前半（書頁 228–230，定理 9.1、推論 1 到 4、定理 9.2、定理 9.3）。

**§9 的內容收在書頁 234**，234–236 是習題 9.1–9.13，依 PLAYBOOK 第 8 節不做解答。**OUTLINE 把 §9 寫成 228–236，是把習題頁算了進去——那張表的頁碼第六次這樣錯。** E63／E64 因此照內容切，不照 OUTLINE 的頁碼切。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e63_fixed_point.py`（`AdvCalcE63ZH` / `AdvCalcE63EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[63]` / `FORMULAS_ADVCALC[63]`）
- 配音：`manim_lessons/samples/audio_e63/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.82 分（229 秒）／英文 3.27 分（196 秒）

## 一個定理，四條推論，還一筆帳

書上說這條定理「很簡單、很漂亮」，而它要做三件事：**補完隱函數定理**（就在這一節）、
**第 6 章證常微分方程的存在唯一性**、以及**跟 Newton 法比較**（在 E64）。

這一集的骨架是：壓縮的定義 → 唯一性（兩行，完全不需要完備性）→ 存在性（造出來的，
這裡才需要完備性）→ 四條推論把定理搬到「只在局部是壓縮」「帶參數」這兩種實際會遇到的情況 →
定理 9.3 把隱函數定理收掉。

**唯一性與存在性用到的條件不一樣，這件事值得講清楚**：唯一性只靠 C 小於一，
存在性才需要完備。beat 1 的註腳特別點出這一點。

## 所有數字都出自同一個具體的壓縮

用的是 K(x) = 1 + sin(x)／2，Lipschitz 常數理論上是 0.5。

- **beat 0**：程式在細格點上掃過所有割線斜率，量到 **0.4999**，印成 0.500——跟理論值一致。
- **beat 2**：不動點是**迭代出來的**（從 x₀ = 0 開始反覆作用 K），得到 **1.4987**，
  並且驗過 K 作用上去真的不動（誤差小於 1e-12）。
- **beat 3**：相鄰兩項的距離與上界 Cⁿδ 逐項比對：
  0.4207 ≤ 0.5000、0.0736 ≤ 0.2500、0.0042 ≤ 0.1250、0.0002 ≤ 0.0625。
- **beat 4**：取半徑 2.5 的閉球，球心移動 1.00 ≤ (1−C)r = 1.25；
  程式在球上取 401 個點，驗過每一個的像都還在球裡。
- **beat 6**：推論 3 的上界 d／(1−C) = 2.0000，實際距離 1.4987——這一次估計很緊。
- **beat 7**：K(s, x) = K(x) + s，把不動點對參數 s 描出來，並驗過
  「參數走一步，不動點走的距離不超過那一步除以一減 C」。
- **beat 9、10 換另一個具體例子**：G(ξ, η) = η³ + η − ξ，T 是原點的第二偏微分，等於 1，
  於是 K(ξ, η) = ξ − η³。三個 ξ 的隱函數值都是迭代出來的，而且驗過 G 真的等於零。
  dK² = −3η² 在原點是 0，在 η = 0.40 是 −0.480（守得住 1／2），在 η = 0.42 是 −0.529（守不住）。

## 這一輪抓到的錯

**bounds／collide／langscan 三道全過之後，probe 幀沒有再抓到圖畫錯的問題**，
這是這幾集裡第一次。但前面三道抓到的東西裡，有兩個是稿子本身的錯，值得記：

1. **註腳寫「常數量到 0.500，跟理論值一樣」，可是程式量到的是 0.486。**
   原因是取樣格點太粗（步長 0.6），從來沒有靠近 |K′| 的峰值。
   改成步長 0.06 的細格點之後量到 0.4999，註腳才成立。
   **這跟前幾集「畫面說的顏色跟畫出來的不一樣」是同一類錯，只是這次錯在數字上**——
   註腳宣稱了一個數，而那個數是另一段程式算的，兩邊沒有對過。
   現在那個量測加了 `assert 0.4995 < LIP <= C`，格點再變粗就會直接失敗。
2. **兩處草稿殘留的 dead code，而且都夾著中文**：一個 `if False else` 分支、
   一個定義了沒用到的 `rows`。`langscan` 直接抓到，因為它掃的是
   `(字串, 顏色)` 這種 row 樣式，不管那段程式碼有沒有被執行。

另外 `bounds` 抓到座標軸畫過 y = 1.30 的上限（beat 0 與 beat 2），
`collide` 抓到 beat 2 的表格第六列壓到底下的說明、以及 **beat 10 的拋物線在 η = ±0.6
掉到 −1.08，插進註腳的文字裡**——把 η 的範圍收到 ±0.5 就解決了。

---

## Beat 0 — 壓縮：Lipschitz 常數小於一 / a contraction: Lipschitz constant under one
*配音長度：中文 24.8s ／ 英文 16.9s*

**畫面公式**

```
壓縮：Lipschitz 常數小於一   |   a contraction: Lipschitz constant under one
ρ ( K x , K y )    ≤    C  ρ ( x , y )                0  <  C  <  1
```

**旁白（繁中）**

> 第 9 節講壓縮映射不動點定理。書上說它很簡單、很漂亮，而且要做三件事：補完隱函數定理的證明、第 6 章拿來證常微分方程的存在唯一性，還有跟 Newton 法比較。定義是這樣：K 是度量空間到自己的 Lipschitz 映射，而且常數嚴格小於一，就叫壓縮。

**Narration (EN)**

> Section 9 is the contraction mapping fixed-point theorem, which the book calls very simple and elegant. It has three jobs: to complete the implicit-function theorem, to give existence and uniqueness for differential equations in chapter 6, and to be compared with Newton.

**動畫**

灰色的 y = x 與青色的 K；曲線上取一點，畫出斜率 ±C 的楔形——任何一段割線都夾在裡面。
右側列出 K 的式子、C = 0.50，以及**實際量到的** max ΔK/Δx = 0.500。

## Beat 1 — 至多一個不動點 / at most one fixed point
*配音長度：中文 18.9s ／ 英文 18.5s*

**畫面公式**

```
至多一個不動點   |   at most one fixed point
( 1 − C )  ρ ( x , y )      ≤      0            ⇒            x   =   y
```

**旁白（繁中）**

> 壓縮至多只有一個不動點，證明只有兩行：如果 x 與 y 都不動，那麼它們的距離等於它們的像的距離，不超過 C 乘原來的距離；移項就得到一減 C 乘那個距離小於等於零。C 小於一，距離就只能是零。

**Narration (EN)**

> A contraction is a Lipschitz mapping of a metric space into itself whose constant is strictly under one. It has at most one fixed point, in two lines: if x and y are both fixed, the distance between them equals the distance between their images, which is at most C times it.

**動畫**

三列推導加一條虛線與結論。**註腳點出：這一段完全沒有用到完備性**——
唯一性是壓縮這個條件自己給的，完備性是下一拍造點時才需要。

## Beat 2 — 定理 9.1：反覆作用 K / Theorem 9.1: apply K over and over
*配音長度：中文 17.6s ／ 英文 16.0s*

**畫面公式**

```
定理 9.1：反覆作用 K   |   Theorem 9.1: apply K over and over
x ₙ   =   K ⁿ ( x ₀ )                    K ( a )   =   a
```

**旁白（繁中）**

> 定理 9.1：非空的完備度量空間上，壓縮映射有唯一的不動點。存在性是造出來的——隨便取一個起點，反覆作用 K，得到一整列點。要證的就是這一列是 Cauchy 序列。

**Narration (EN)**

> Theorem 9.1: on a nonempty complete metric space a contraction has a unique fixed point. Existence is constructed. Pick any starting point, apply K over and over, and the claim is that the sequence produced this way is Cauchy.

**動畫**

**蛛網圖**：紅色階梯豎直走到曲線上、再水平走回 y = x，一步一步逼近橘點。
右側列出 x₀ 到 x₈ 的實際值，最後停在 1.4987。

## Beat 3 — 為什麼那一列是 Cauchy 的 / why that sequence is Cauchy
*配音長度：中文 22.8s ／ 英文 19.7s*

**畫面公式**

```
為什麼那一列是 Cauchy 的   |   why that sequence is Cauchy
ρ ( x ₘ , x ₙ )   <   C ⁿ δ / ( 1 − C )          δ  =  ρ ( x ₁ , x ₀ )
```

**旁白（繁中）**

> 令 δ 是第一項到起點的距離。每走一步，相鄰兩項的距離就縮小 C 倍，所以第 n 對的距離不超過 C 的 n 次方乘 δ。把中間那些距離加起來，用幾何級數一估：兩個指標都大於 n 時，距離不超過 C 的 n 次方乘 δ 再除以一減 C。

**Narration (EN)**

> Let delta be the distance from the first term to the starting point. Each step shrinks the gap by a factor of C, so the n-th gap is at most C to the n times delta. Summing the gaps between with a geometric series bounds any two terms past n by C to the n delta over one minus C.

**動畫**

對數尺度上兩條折線：橘色是上界 Cⁿδ，紅色是實際量到的距離。
**註腳照實說這個上界很鬆**——這個 K 很平滑，實際距離掉得比上界快得多。

## Beat 4 — 推論 1：球被送進自己 / Corollary 1: the ball goes into itself
*配音長度：中文 22.6s ／ 英文 17.9s*

**畫面公式**

```
推論 1：球被送進自己   |   Corollary 1: the ball goes into itself
ρ ( K p , p )   ≤   ( 1 − C ) r            ⇒            a   ∈   D
```

**旁白（繁中）**

> 實際遇到的映射常常只在某一點附近是壓縮，所以要先確認那個鄰域被送進自己。推論 1：D 是完備空間裡半徑 r 的閉球，K 是壓縮，而且它把球心移動的距離不超過一減 C 乘 r，那麼不動點存在、唯一，而且就落在 D 裡面。

**Narration (EN)**

> In practice a map is often a contraction only near some point, so the neighbourhood has to be carried into itself. Corollary 1: on a closed ball of radius r, if the contraction moves the center at most one minus C times r, the fixed point exists and lies in that ball.

**動畫**

一條數線上標出半徑 2.5 的閉球（兩端青色虛線）、球心 p、球心的像、以及不動點 a。
紅色箭頭標出球心移動的距離 d = 1.00，右側對照 (1−C)r = 1.25。

## Beat 5 — C r 加上 ( 1 − C ) r 剛好是 r / C r plus one minus C times r is exactly r
*配音長度：中文 22.4s ／ 英文 16.9s*

**畫面公式**

```
C r 加上 ( 1 − C ) r 剛好是 r   |   C r plus one minus C times r is exactly r
ρ ( K x , p )    ≤    C r  +  ( 1 − C ) r    =    r
```

**旁白（繁中）**

> 證明只是檢查 K 把 D 送進 D：任取 D 裡的一點，它的像到球心的距離，不超過「它的像到球心的像」加上「球心移動的距離」，也就是 C 乘 r 加上一減 C 乘 r，剛好等於 r。推論 2 是開球的版本，證明是縮到一個略小的閉球再引用推論 1。

**Narration (EN)**

> The proof checks that the ball goes into itself: a point's image is within C times r of the center's image, the center moves at most one minus C times r, and those add to exactly r. Corollary 2 is the open version, proved on a slightly smaller closed ball.

**動畫**

一條線段被切成兩段：青色的 C r 與紅色的 (1−C) r，底下一條虛線標出合計正好是 r。
**整條推論就是這一個加法。**

## Beat 6 — 推論 3：離不動點有多遠 / Corollary 3: how far the fixed point is
*配音長度：中文 18.9s ／ 英文 18.0s*

**畫面公式**

```
推論 3：離不動點有多遠   |   Corollary 3: how far the fixed point is
ρ ( x , a )    ≤    d / ( 1 − C )              d  =  ρ ( K x , x )
```

**旁白（繁中）**

> 推論 3 給的是距離的估計：如果 K 把 x 移動了 d，那麼 x 到不動點的距離不超過 d 除以一減 C。做法是取一個以 x 為心、半徑 d 除以一減 C 的閉球，套推論 1。這一條等一下證連續性時要用。

**Narration (EN)**

> Corollary 3 estimates a distance. If K moves the point x a distance d, then x is within d over one minus C of the fixed point. The proof takes the closed ball of that radius about x and applies Corollary 1. This is what the continuity argument will need.

**動畫**

數線上三點 x、K x、a，兩支箭頭分別標出 d = 1.00 與 d／(1−C) = 2.00。
右側對照實際距離 1.4987 與上界 2.0000——這一次估計很緊。

## Beat 7 — 帶參數的壓縮 / a contraction with a parameter
*配音長度：中文 20.8s ／ 英文 17.8s*

**畫面公式**

```
帶參數的壓縮   |   a contraction with a parameter
ρ ( K ( s , x ) , K ( s , y ) )   ≤   C ρ ( x , y )            ∀ s
```

**旁白（繁中）**

> 接下來讓壓縮帶一個參數。K 變成兩個變數的函數，假設它對第二個變數是壓縮、而且那個常數對第一個變數的每一個值都通用，同時對每個固定的第二變數關於第一個連續。推論 4：那麼不動點是參數的連續函數。

**Narration (EN)**

> Now give the contraction a parameter. K becomes a function of two variables, a contraction in the second with one constant that works for every value of the first, and continuous in the first for each fixed second. Corollary 4: the fixed point is continuous in the parameter.

**動畫**

s 從 −0.60 走到 +0.60，把每一個 s 的不動點畫成一條連續上升的曲線；
右側列出四組 (s, pₛ) 的實際值。

## Beat 8 — 推論 4 與定理 9.2 / Corollary 4, and Theorem 9.2
*配音長度：中文 19.4s ／ 英文 18.6s*

**畫面公式**

```
推論 4 與定理 9.2   |   Corollary 4, and Theorem 9.2
s   ↦   p ₛ                ρ ( p ₛ , p ₜ )   ≤   ϵ / ( 1 − C )
```

**旁白（繁中）**

> 證明就是把推論 3 接上去：參數動一點，K 把原來那個不動點移動不超過 ε，所以新的不動點離它不超過 ε 除以一減 C。推論 2 與推論 4 合起來就是定理 9.2，那才是後面真正拿來用的形式。

**Narration (EN)**

> The proof hooks Corollary 3 on: move the parameter a little and K moves the old fixed point by at most epsilon, so the new fixed point is within epsilon over one minus C of it. Corollaries 2 and 4 combine into Theorem 9.2, which is the form actually used later.

**動畫**

兩列式子，中間一支向下的箭頭代表「套推論 3」，底下一列是連續性的結論。

## Beat 9 — 定理 9.3：隱函數定理補完 / Theorem 9.3: the implicit-function theorem
*配音長度：中文 19.5s ／ 英文 19.1s*

**畫面公式**

```
定理 9.3：隱函數定理補完   |   Theorem 9.3: the implicit-function theorem
K ( ξ , η )  =  η  −  T ⁻ ¹ G ( ξ , η )              T  =  d G ² ₍ α , β ₎
```

**旁白（繁中）**

> 現在可以補完隱函數定理了。定理 9.3：G 在某一點等於零，而且它在那裡的第二個偏微分可逆。令 K 是 η 減去那個偏微分的反元素乘上 G。K 的不動點，正好就是 G 等於零的解。

**Narration (EN)**

> The implicit-function theorem can now be finished. Theorem 9.3: G vanishes at a point where its second partial differential is invertible. Let K be eta minus the inverse of that differential applied to G; its fixed points are exactly the solutions of G equals zero.

**動畫**

G(ξ, η) = η³ + η − ξ 的零集合畫成一條遞增曲線，三個紅點是**迭代出來的**隱函數值，
右側列出 F(0.1)、F(0.3)、F(0.5)，而且每一個都驗過 G 真的等於零。

## Beat 10 — 一階項被消掉，才成為壓縮 / killing the first-order term is what makes it a contraction
*配音長度：中文 20.5s ／ 英文 16.1s*

**畫面公式**

```
一階項被消掉，才成為壓縮   |   killing the first-order term is what makes it a contraction
d K ² ₍ α , β ₎   =   0                    ‖ d K ² ‖    ≤    1 / 2
```

**旁白（繁中）**

> 關鍵在於 K 對第二個變數的微分在那一點正好是零——那就是「把一階項消掉」的意思。因為它連續，附近有一個球讓它的範數不超過二分之一，均值定理就把 K 變成常數二分之一的壓縮，定理 9.2 一套上去就結束了。

**Narration (EN)**

> The key is that the differential of K in its second variable vanishes at that point, which is what killing the first-order term means. Being continuous it stays under one half nearby, so the mean value theorem makes K a contraction with constant one half.

**動畫**

dK² = −3η² 的拋物線，頂點（原點）是橘點；紅色虛線是 −1／2，
青色兩條垂直虛線標出 η = ±0.40。**曲線正好在那兩條線之外才跌破 −1／2**，
右側用三個 η 的值把這件事變成數字。
