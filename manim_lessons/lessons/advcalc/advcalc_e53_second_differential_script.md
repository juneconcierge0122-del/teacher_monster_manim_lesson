# advcalc E53 — 第 3 章：二階微分

Chapter 3: The Second Differential

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 16 節「二階微分與臨界點的分類」的前半（書頁 186–189）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e53_second_differential.py`（`AdvCalcE53ZH` / `AdvCalcE53EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[53]` / `FORMULAS_ADVCALC[53]`）
- 配音：`manim_lessons/samples/audio_e53/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.14 分（189 秒）／英文 3.02 分（181 秒）

## 同一個數字，三種算法

二階微分就是「把 dF 再微一次」。這一集把它跟熟悉的東西對起來，而每一步都在同一個函數
`F(x, y) = x³y + sin(xy) + x²y²` 上算過：

- **定理 16.1**：先沿 μ 求一次方向導數、再沿 ν 求一次，得到 **2.359343**；
  二階偏導數配上兩組分量的雙重求和，也是 **2.359343**；
  第 10 拍那個二階差分除以增量的平方，在增量取到 0.002 時是 2.367454。
  三種完全不同的算法，同一個數字。
- **定理 16.3**：那個 2×2 的二階偏導數矩陣，兩個混合元的差是 **0.0**（浮點意義下完全相同）。
- **而那個對稱不是白來的**：收尾用的是經典的反例 `xy(x²−y²)/(x²+y²)`。
  程式算出它在原點的兩個混合偏導數是 **−1** 與 **+1**：兩個都存在、卻不相等。
  所以那一點沒有二階微分——**少了這一拍，定理 16.3 看起來像是不需要假設的**。
- **二階差分本身對稱**：程式在三個尺度上都斷言了交換兩個增量之後值完全相同（差是 0）。

probe 幀抓到兩處：beat 0 原本畫了兩個矩陣代表「兩點各對到一個線性映射」，
可是兩個矩陣是同一個——改成兩點各自的 dF，並斷言兩者差得夠遠；
beat 7 的省略號跟中間那個方塊畫在同一個高度，直接印在字上面。

---

## Beat 0 — 微分本身也是一個映射 / the differential is itself a map
*配音長度：中文 16.5s ／ 英文 16.5s*

**畫面公式**

```
微分本身也是一個映射   |   the differential is itself a map
dF  :  A  →  Hom ( V , W )                    γ   ↦   dF ᵧ
```

**旁白（繁中）**

> 第 16 節講二階微分。F 的微分本身是一個映射：把一點送到 dF 在那一點的值，落在 Hom 裡。既然它是一個映射，就可以問它可不可微——這一問就得到二階微分。

**Narration (EN)**

> Section 16 is about the second differential. The differential of F is itself a map: it sends a point to the differential of F there, an element of Hom. Being a map, it can be asked whether it is differentiable, and that question produces the second differential.

**動畫**

左邊一團定義域上兩個不同顏色的點，兩支箭頭指向右邊各自的 dF（一列兩個數字）。
右側說明 dF 本身是一個映射，值落在 Hom 裡。

## Beat 1 — 二階微分的定義 / the definition of the second differential
*配音長度：中文 17.0s ／ 英文 15.9s*

**畫面公式**

```
二階微分的定義   |   the definition of the second differential
d ² F ₐ    =    d ( dF ) ₐ    ∈    Hom ( V ,  Hom ( V , W ) )
```

**旁白（繁中）**

> 定義照抄一階的：把 d 作用在 dF 上，得到的是從 V 到 Hom(V, W) 的有界線性映射。所以二階微分吃兩個向量：先吃一個得到 Hom 裡的元素，再吃一個得到 W 裡的向量。

**Narration (EN)**

> The definition copies the first: apply d to dF and get a bounded linear map from V into Hom of V and W. So the second differential eats two vectors, the first giving an element of Hom and the second a vector in W.

**動畫**

左邊三行式子（F、dF、d²F 各自的型別），下面一行 d²F 吃兩個向量之後落在 W 裡。
右側說明它一次吃一個。

## Beat 2 — 它其實是一個雙線性映射 / it is really a bilinear map
*配音長度：中文 17.6s ／ 英文 16.2s*

**畫面公式**

```
它其實是一個雙線性映射   |   it is really a bilinear map
ω  :  V × V  →  W                ω ( η , ξ )  =  d ² F ₐ ( η ) ( ξ )
```

**旁白（繁中）**

> 換個說法：它等價於一個有界的雙線性映射，兩個變數各自線性，值落在 W 裡。書上說這個東西應該是某種二階導數，而且讀者可能已經猜到，它就是兩個方向的混合導數。

**Narration (EN)**

> Put another way, it is equivalent to a bounded bilinear map: linear in each of two variables with values in W. The book says this ought to be some kind of second derivative, and the reader might well guess it is the mixed derivative in the two directions.

**動畫**

左邊兩個方塊 η、ξ 各一支箭頭進入 ω，再一支箭頭出到 W。
右側說明兩個變數各自線性、值有界。

## Beat 3 — 定理 16.1：就是混合方向導數 / Theorem 16.1: the nested directional derivative
*配音長度：中文 16.9s ／ 英文 17.2s*

**畫面公式**

```
定理 16.1：就是混合方向導數   |   Theorem 16.1: the nested directional derivative
D ᵥ ( D ᵤ F ) ( α )        =        ( d ² F ₐ ( ν ) ) ( μ )
```

**旁白（繁中）**

> 定理 16.1 就是把這個猜測證出來：F 連續可微而且二階微分存在，那麼固定一個方向的方向導數作為點的函數在該點可微，而它沿另一個方向的導數，就是二階微分吃那兩個向量。

**Narration (EN)**

> Theorem 16.1 proves that guess: if F is continuously differentiable and the second differential exists, then the directional derivative in a fixed direction is differentiable in the point, and its derivative along a second direction is the second differential on the two.

**動畫**

左邊一個加框的定理 16.1，下面一張表列出三種算法的數值。
右側說明先沿 μ、再沿 ν。

## Beat 4 — 證明：在 μ 取值的那個映射 / the proof: evaluation at mu
*配音長度：中文 15.8s ／ 英文 15.8s*

**畫面公式**

```
證明：在 μ 取值的那個映射   |   the proof: evaluation at mu
D ᵤ F   =   ev ᵤ  ∘  dF                  ev ᵤ ( T )   =   T ( μ )
```

**旁白（繁中）**

> 證明用一個叫「在 μ 取值」的映射：它把 Hom 裡的 T 送到 T 作用在 μ 上，是有界線性的。於是沿 μ 的方向導數就是這個取值映射接上 dF，合成規則直接給出結論。

**Narration (EN)**

> The proof uses evaluation at mu, the map sending T in Hom to T applied to mu, which is bounded and linear. The directional derivative along mu is then that evaluation composed with dF, and the composite rule hands over the conclusion.

**動畫**

左邊三行 ev 的式子，下面一個加框的合成。
右側說明取值映射是有界線性的，微分就是它自己。

## Beat 5 — 推論：座標下是二階偏導數 / a corollary: the second partials in coordinates
*配音長度：中文 14.9s ／ 英文 15.8s*

**畫面公式**

```
推論：座標下是二階偏導數   |   a corollary: the second partials in coordinates
d ² F ₐ ( b , c )    =    Σ  b ᵢ c ⱼ   ∂ ² F / ∂x ⱼ ∂x ᵢ  ( a )
```

**旁白（繁中）**

> 推論一：定義域是實數的 n 維空間時，二階微分存在就推出所有二階偏導數存在，而且它吃兩個向量的結果，就是那些偏導數配上兩組分量的雙重求和。

**Narration (EN)**

> Corollary one: when the domain is real n-space, the existence of the second differential forces all the second partial derivatives to exist, and its value on two vectors is the double sum of those partials weighted by the two sets of components.

**動畫**

左邊二階偏導數的矩陣與它的標籤，右邊是雙重求和的式子。
右側說明那個矩陣就是二階微分在座標下的樣子。

## Beat 6 — 定理 16.2：實際會用的判準 / Theorem 16.2: the test actually used
*配音長度：中文 18.0s ／ 英文 17.1s*

**畫面公式**

```
定理 16.2：實際會用的判準   |   Theorem 16.2: the test actually used
∂ ² F / ∂x ᵢ ∂x ⱼ   ∈   C ⁰ ( A )        ⇒        d ² F   ∈   C ⁰ ( A )
```

**旁白（繁中）**

> 定理 16.2 是反過來的、實際會用到的判準：所有二階偏導數在開集上存在而且連續，那麼二階微分就存在而且連續。這跟第 9 節那條「偏導數連續推出可微」是同一個模式。

**Narration (EN)**

> Theorem 16.2 is the converse, and the test actually used: if all the second partial derivatives exist and are continuous on an open set, then the second differential exists and is continuous there. It is the same pattern as section 9's test for the first.

**動畫**

左邊兩個假設方塊（存在、連續）經一支箭頭指向結論方塊。
右側說明這跟第 9 節那條一階的判準同一個模式。

## Beat 7 — 逐分量檢查的根據 / what licenses checking componentwise
*配音長度：中文 17.3s ／ 英文 16.7s*

**畫面公式**

```
逐分量檢查的根據   |   what licenses checking componentwise
S  =  ⟨ S ₁ , … , S ₖ ⟩ ,   S ⁻¹  ∃        ⇒        ( F  ⇔  S ᵢ ∘ F )
```

**旁白（繁中）**

> 證明要一條分量法的引理：如果一組線性映射併起來是可逆的，那麼 F 可微，等價於每一個分量接上 F 都可微。這條引理兩行就證完，可是它是「逐分量檢查」這件事的根據。

**Narration (EN)**

> The proof needs a componentwise lemma: if a finite collection of linear maps assembles into an invertible one, then F is differentiable exactly when each component composed with F is. It takes two lines and is what licenses checking one component at a time.

**動畫**

左邊三個分量方塊（中間放一個省略號）經一支箭頭指向 F ∈ C¹。
右側說明反過來也對。

## Beat 8 — 三階以上一模一樣 / third order and beyond, unchanged
*配音長度：中文 16.5s ／ 英文 16.7s*

**畫面公式**

```
三階以上一模一樣   |   third order and beyond, unchanged
( D ₄ D ᵥ D ᵤ F ) ( a )    =    Σ  b ᵢ c ⱼ d ₖ   ∂ ³ F / ∂x ₖ ∂x ⱼ ∂x ᵢ
```

**旁白（繁中）**

> 同樣的做法可以一直往下推。三階的公式長得一模一樣，只是多一個指標、多一組分量；而三階偏導數存在且連續，就推出二階微分可微。次數沒有上限。

**Narration (EN)**

> The same construction repeats indefinitely. The third-order formula has exactly the same shape with one more index and one more set of components, and third partials existing and continuous make the second differential differentiable. There is no ceiling on the order.

**動畫**

左邊兩行公式：二階的與三階的，形狀一模一樣只是多一個指標。
右側說明次數沒有上限。

## Beat 9 — 定理 16.3：對稱 / Theorem 16.3: symmetry
*配音長度：中文 16.8s ／ 英文 17.4s*

**畫面公式**

```
定理 16.3：對稱   |   Theorem 16.3: symmetry
( d ² F ₐ ( η ) ) ( ξ )        =        ( d ² F ₐ ( ξ ) ) ( η )
```

**旁白（繁中）**

> 定理 16.3 是這一節最要緊的一條：二階微分對它的兩個變數是對稱的。也就是混合偏導數可以交換次序——可是要注意，前提是二階微分存在，不是只有偏導數存在。

**Narration (EN)**

> Theorem 16.3 is the one that matters most here: the second differential is symmetric in its two arguments. That is, mixed partials may be taken in either order, but note the hypothesis is that the second differential exists, not merely that the partials do.

**動畫**

左邊二階偏導數矩陣，兩個非對角元標成紅色，下面印出兩者的差。
右邊是對稱的式子。

## Beat 10 — 二階差分，與一個反例 / the second difference, and a counterexample
*配音長度：中文 21.2s ／ 英文 16.2s*

**畫面公式**

```
二階差分，與一個反例   |   the second difference, and a counterexample
Δ ² F ₐ ( η , ξ )  =  F ( α + η + ξ ) − F ( α + η ) − F ( α + ξ ) + F ( α )
```

**旁白（繁中）**

> 證明的關鍵是二階差分：F 在四個點上的交錯和。它一眼就看得出對稱，因為兩個增量地位相同；而估計說它跟二階微分只差一個小量。經典的反例裡兩個混合偏導數存在卻不相等，那裡二階微分就不存在。

**Narration (EN)**

> The proof turns on the second difference, an alternating sum of F at four points. It is visibly symmetric, since the two increments enter alike, and an estimate says it is close to the second differential. In the classic counterexample the mixed partials differ.

**動畫**

左邊一個平行四邊形，四個角各打一點並標上 + − − + 的符號。
右邊是反例的兩個混合偏導數：−1 與 +1。

---

## 假設是「二階微分存在」，不是「偏導數存在」

這是這一集最容易滑過去的一句話。定理 16.3 要的是二階微分存在，
而不是兩個混合偏導數各自存在。差別不是吹毛求疵：最後一拍那個反例的兩個混合偏導數
在原點都存在，一個是 −1、一個是 +1，正好差了 2。它們不相等，
所以那一點沒有二階微分——反過來說，只要二階微分存在，對稱就是白得的。

## 下一集

第 16 節的後半是這一節名字裡的另一半：臨界點的分類。
用第 2 章的定理 7.1 取一組 ω 正交的基，二次型化成標準形，
而「−1 的個數」就決定了那個臨界點是極大、極小、還是鞍點——
以及鞍點上「往下」的那個子空間有幾維。
