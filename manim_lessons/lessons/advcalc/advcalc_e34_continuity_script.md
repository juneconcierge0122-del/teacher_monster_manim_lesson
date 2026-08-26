# advcalc E34 — 第 3 章：連續、Lipschitz 與有界線性映射

Chapter 3: Continuity, Lipschitz and Bounded Linear Maps

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 3 節的前段（書頁 126–128）。書頁 129 起是習題 3.1–3.22，第 4 節從書頁 132 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e34_continuity.py`（`AdvCalcE34ZH` / `AdvCalcE34EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[34]` / `FORMULAS_ADVCALC[34]`）
- 配音：`manim_lessons/samples/audio_e34/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.24 分（194 秒）／英文 3.25 分（195 秒）

## 這一集的圖都是算出來的，不是畫出來的

第 3 節把第 1 節的 ε-δ 整段搬到賦範空間，內容本身沒有新東西，所以這一集的價值在於
**每一張圖都真的成立**。場景檔在 import 時就把畫面宣稱的事情算一遍：

- **beat 1 的 δ 是解出來的。** 給定 ε，用二分法找出「曲線還留在 ε 帶裡」的最大 δ，
  再取兩側的小者；然後掃 401 個取樣點斷言整個 δ 帶都沒出界。初稿的曲線用 tanh，
  解出來的 δ 剛好讓左邊那條虛線壓在 y 軸上（兩條線幾乎重合），所以換成三次多項式、
  把 α 移到 1.2，兩條虛線才分得開。
- **beat 3 的斜率 3 是量出來的，而且斷言它是最小的。** 在畫出來的區間上掃 799 個點求
  `|x² − 1| / |x − 1|` 的上確界，斷言不超過 3、也不小於 2.99——否則錐形會鬆，
  「c 不能再小」那句話就不成立。
- **beat 4 的兩組 δ 都驗過。** 對 ε = 3/2 與 1/2 各算出 δ，再掃 399 個點確認
  `|f − L| < ε` 真的成立。
- **beat 5 斷言根號 x 逃得出每一條直線**，並且斷言畫出來的交點就是兩者相等的地方。
- **beats 6 到 9 的算子範數是掃單位球面掃出來的**（720 個方向），再斷言它跟
  「矩陣每列絕對值和取最大」這個公式一致。這讓最後一拍可以誠實地說：定理 3.1 的證明
  給出 6，真正的最小界是 3。
- **beat 10 的反向三角不等式在 28561 對向量、三種範數上全掃過**，一次都沒違反。

渲染前 `tools/bounds.py` 與 `tools/collide.py` 都跑到 0。collide 在第一輪抓到三件事：
beat 7 那行比值壓在兩個面板的座標軸上、beat 10 的 α 與 β 標籤各自坐在一條軸線上。

---

## Beat 0 — 同一個定義，只換掉一個符號 / the same definition, one symbol changed
*配音長度：中文 14.7s ／ 英文 17.7s*

**畫面公式**

```
同一個定義，只換掉一個符號   |   the same definition, one symbol changed
f : A → W ,   A ⊂ V           | · |   ⟶   ‖ · ‖
```

**旁白（繁中）**

> 上一節把範數建起來，這一節就把 ε-δ 原封不動搬過來：絕對值換成範數，其他一個字都不用改。定義域也順便放寬，f 定義在 V 的任意一個子集上就行。

**Narration (EN)**

> The last section built norms; this one carries the epsilon delta definition over unchanged. Replace the absolute value sign by the norm sign and no other word moves. The domain is relaxed too: f may live on any subset of V, not the whole space.

**動畫**

上排一條實數線標著 a 與 ±δ 的刻度，下排一顆二維的球標著 α 與半徑箭頭，中間一支向下的箭頭。右邊三行說明定義一字未改、定義域放寬成任意子集、極限定理照抄。

## Beat 1 — 極限：α 自己被挖掉 / the limit: alpha itself is removed
*配音長度：中文 18.1s ／ 英文 17.2s*

**畫面公式**

```
極限：α 自己被挖掉   |   the limit: alpha itself is removed
0 < ‖ ξ − α ‖ < δ      ⇒      ‖ f ( ξ ) − β ‖ < ε
```

**旁白（繁中）**

> 極限的寫法是：對每個 ε 都找得到 δ，使得 ξ 到 α 的距離大於零又小於 δ 時，f 在 ξ 的值到 β 的距離就小於 ε。那個「大於零」是把 α 自己挖掉，因為極限問的是靠近時的行為。

**Narration (EN)**

> The limit reads like this. For every epsilon there is a delta such that whenever the distance from xi to alpha is greater than zero and smaller than delta, the distance from the value at xi to beta is smaller than epsilon. That greater than zero removes alpha itself.

**動畫**

一條有洞的曲線：α 那一點挖成空心圈，f 在 α 的實際值是上方一顆紅點。橘色虛線是 ε 帶，紫色虛線是解出來的 δ 帶，灰色虛線把 β 引到左邊標出來。

## Beat 2 — 在 α 連續 / continuous at alpha
*配音長度：中文 18.0s ／ 英文 18.8s*

**畫面公式**

```
在 α 連續   |   continuous at alpha
‖ ξ − α ‖ < δ      ⇒      ‖ f ( ξ ) − f ( α ) ‖ < ε
```

**旁白（繁中）**

> 如果 α 本來就在定義域裡，而且這個極限剛好等於 f 在 α 的值，就說 f 在 α 連續。這時「大於零」可以丟掉：ξ 等於 α 時兩個值的差是零向量，範數是零，本來就小於 ε。

**Narration (EN)**

> If alpha lies in the domain and this limit is exactly the value at alpha, we say f is continuous at alpha. Now the greater than zero part can go: when xi equals alpha the difference of the two values is the zero vector, whose norm is zero and already smaller than epsilon.

**動畫**

同一張圖，洞補起來變成實心點，紅點消失。差別只在一個點的值。

## Beat 3 — 在一點 Lipschitz 連續 / Lipschitz continuous at a point
*配音長度：中文 16.7s ／ 英文 17.4s*

**畫面公式**

```
在一點 Lipschitz 連續   |   Lipschitz continuous at a point
‖ f ( ξ ) − f ( α ) ‖  ≤  c ‖ ξ − α ‖         ( ‖ ξ − α ‖ < r )
```

**旁白（繁中）**

> 接著是一個比連續更強、也好用得多的性質。如果找得到一個常數 c，使得 ξ 夠靠近 α 時，兩個函數值的距離不超過 c 乘上兩個自變數的距離，就說 f 在 α 是 Lipschitz 連續。

**Narration (EN)**

> Next comes a property stronger than continuity and far easier to use. If there is a constant c such that, for xi close enough to alpha, the distance between the two values is at most c times the distance between the two arguments, we call f Lipschitz continuous at alpha.

**動畫**

x 平方在 1 附近的圖，加上通過 (1, 1)、斜率 ±3 的兩條直線構成的錐形。曲線整段留在錐形裡，右上角一顆橘點是唯一碰到的地方（x = 2）。

## Beat 4 — δ 有現成公式，不必再湊 / delta now comes with a formula
*配音長度：中文 16.4s ／ 英文 16.1s*

**畫面公式**

```
δ 有現成公式，不必再湊   |   delta now comes with a formula
δ  =  min { ε / c ,  r }          f ( x ) = x ² ,  α = 1 ,  c = 3
```

**旁白（繁中）**

> 好處是 δ 不必再湊，有現成的公式：取 ε 除以 c 就成立。上一集我們對 x 平方在一附近湊了半天；現在只要看出 c 可以取三，δ 直接就是 ε 的三分之一。

**Narration (EN)**

> The gain is that delta no longer has to be hunted for: take epsilon over c. Last time we worked to find a delta for x squared near one; here it is enough to notice that c may be taken to be three, and delta is simply a third of epsilon.

**動畫**

同一個錐形，加上 ε = 3/2 的橘色水平帶與 δ = 1/2 的紅色垂直帶。右邊列出兩組 ε 與對應的 δ。

## Beat 5 — 連續，但不是 Lipschitz / continuous, but not Lipschitz
*配音長度：中文 17.6s ／ 英文 18.2s*

**畫面公式**

```
連續，但不是 Lipschitz   |   continuous, but not Lipschitz
( √ x − 0 ) / ( x − 0 )   =   1 / √ x    ⟶    ∞
```

**旁白（繁中）**

> 但不是每個連續函數都做得到。根號 x 在零點連續，可是兩個值的差除以兩個自變數的差等於根號 x 分之一，x 越小這個比值越大，沒有常數撐得住。Lipschitz 嚴格強於連續。

**Narration (EN)**

> But not every continuous function manages this. The square root is continuous at zero, yet the difference of values over the difference of arguments is one over the square root of x, which grows without bound as x shrinks. No constant survives, so Lipschitz is strictly stronger.

**動畫**

第一象限裡的根號曲線，加上斜率 1、2、4 的三條直線；每條線上一顆點標出它跟曲線相交的位置，交點左邊曲線都在直線上方。

## Beat 6 — 線性映射：條件塌成一句話 / a linear map: the condition collapses
*配音長度：中文 18.0s ／ 英文 16.9s*

**畫面公式**

```
線性映射：條件塌成一句話   |   a linear map: the condition collapses
T ( ξ ) − T ( η )  =  T ( ξ − η )          ‖ T ( ζ ) ‖  ≤  c ‖ ζ ‖
```

**旁白（繁中）**

> 如果整個定義域上同一個常數都成立，就說 f 是 Lipschitz 函數。碰到線性映射，條件會塌下來：兩點的值相減就是差向量的像，所以只要檢查每個向量的像的範數不超過 c 乘它自己的範數。

**Narration (EN)**

> If one constant works across the whole domain, f is called a Lipschitz function. For a linear map the condition collapses: the difference of two values is the image of the difference vector, so it is enough that every vector's image has norm at most c times its own norm.

**動畫**

藍色是單位球（一致範數，所以是正方形），紅色是它在 T 底下的像，紫色是半徑 c 的球。兩顆橘點是像碰到紫球的方向，也就是 c 不能再小的理由。

## Beat 7 — 「有界」不是值域有界 / bounded does not mean the range is bounded
*配音長度：中文 18.7s ／ 英文 17.3s*

**畫面公式**

```
「有界」不是值域有界   |   bounded does not mean the range is bounded
‖ T ( x α ) ‖  =  | x | · ‖ T ( α ) ‖          ‖ T ( α ) ‖ / ‖ α ‖  ≤  c
```

**旁白（繁中）**

> 這種線性映射習慣上不叫 Lipschitz，而叫有界，c 叫它的一個界。但這個詞很容易誤會：它不是說值域是有界集。非零的線性映射不可能那樣有界，因為把向量放大幾倍，像就放大幾倍。

**Narration (EN)**

> Such a map is conventionally called bounded rather than Lipschitz, and c is called a bound for it. The word misleads: it does not say the range is a bounded set. No nonzero linear map is bounded that way, since scaling a vector scales its image by the same factor.

**動畫**

左邊 V 面板一條射線，上面三顆點標著 α、2α、3α；右邊 W 面板一條射線，三顆點標著像的長度 3、6、9。灰色方框是隨手畫的一顆球，第二、第三個像已經在框外。右邊列出三個商都等於 3。

## Beat 8 — 積分是有界線性泛函 / the integral is a bounded functional
*配音長度：中文 19.4s ／ 英文 18.1s*

**畫面公式**

```
積分是有界線性泛函   |   the integral is a bounded functional
| ∫ f |  ≤  ( b − a ) ‖ f ‖ ∞           1  ≤  2 · 1
```

**旁白（繁中）**

> 舉個真的例子。連續函數配上一致範數，取定積分就是一個有界線性泛函：積分的絕對值不超過區間長度乘上一致範數。畫面上這個函數的一致範數是一、區間長度是二，積分算出來是一。

**Narration (EN)**

> Here is a real example. Take continuous functions with the uniform norm; the definite integral is a bounded linear functional, since the size of the integral is at most the length of the interval times the uniform norm. On screen the norm is one, the length two, the integral one.

**動畫**

sin 平方的圖填滿到 x 軸（陰影就是積分），上方一條紫色虛線是一致範數的高度、右邊一條垂直虛線圍出面積為 2 的矩形。標著 b − a。

## Beat 9 — 定理 3.1：三件事是同一件事 / Theorem 3.1: three conditions, one thing
*配音長度：中文 19.3s ／ 英文 19.3s*

**畫面公式**

```
定理 3.1：三件事是同一件事   |   Theorem 3.1: three conditions, one thing
ε = 1 :   ‖ ξ ‖ < δ  ⇒  ‖ T ( ξ ) ‖ < 1          C  =  2 / δ
```

**旁白（繁中）**

> 定理 3.1 說，對線性映射而言三件事完全等價：在某一點連續、處處連續、有界。證明從一點連續出發，取 ε 等於一拿到一個 δ，再用線性把它撐成整個空間的界，得到二除以 δ。

**Narration (EN)**

> Theorem three point one says that for a linear map three conditions are one and the same: continuous at a point, continuous everywhere, bounded. The proof starts from one point, takes epsilon equal to one to get a delta, then uses linearity to stretch it into a bound of two over delta.

**動畫**

三個方框排成三角形：在一點連續、處處連續、有界，三支箭頭繞成一圈。下方是這個例子的 δ = 1/3 與證明給出的 C = 2/δ = 6。

## Beat 10 — 引理 3.1：範數自己是 Lipschitz 的 / Lemma 3.1: the norm is itself Lipschitz
*配音長度：中文 17.4s ／ 英文 17.7s*

**畫面公式**

```
引理 3.1：範數自己是 Lipschitz 的   |   Lemma 3.1: the norm is itself Lipschitz
| ‖ α ‖ − ‖ β ‖ |    ≤    ‖ α − β ‖
```

**旁白（繁中）**

> 不過那個界只保證存在，不保證最省：畫面上這個例子真正的最小界是三，證明給出來的是六。最後補一個引理，範數自己就是 Lipschitz 常數為一的函數，範數的差不超過差的範數。

**Narration (EN)**

> That bound is only guaranteed to exist, not to be smallest: for the example on screen the smallest bound is three and the proof hands us six. One last lemma: the norm is itself Lipschitz with constant one, the difference of two norms being at most the norm of the difference.

**動畫**

兩個向量 α、β 從原點畫出，各配一個半徑等於自己範數的圓；藍色線段連兩個端點。兩圈的半徑差 1.19 明顯小於線段長度 1.80。

---

## 為什麼把 x 平方拿來當 Lipschitz 的例子

E31 為了示範 ε-δ，對同一個函數在同一點手工湊了一個 δ（`min{1/2, 2ε/5}`）。這一集刻意
回到同一個例子：Lipschitz 條件一成立，δ 就有公式，不必再湊。兩集放在一起看，
「Lipschitz 比連續好用」這句話才有具體內容。

## 那個「有界」

書上在這裡特別警告一次：線性映射的「有界」不是「值域是有界集」。這是整節最容易誤讀的字，
所以獨立成一拍（beat 7），並且用同一個 T 把「像會跟著放大」與「商不動」畫在兩個面板上。
E35 會把這個商的最小上界正式定義成算子範數。
