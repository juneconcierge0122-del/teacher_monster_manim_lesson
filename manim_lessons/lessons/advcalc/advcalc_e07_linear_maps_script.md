# advcalc E07 — 第 1 章：線性變換與 skeleton

Chapter 1: Linear Transformations and the Skeleton

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 1 節（書頁 29–32）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e07_linear_maps.py`（`AdvCalcE07ZH` / `AdvCalcE07EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[7]` / `FORMULAS_ADVCALC[7]`）
- 配音：`manim_lessons/samples/audio_e07/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.40 分（204 秒）／英文 2.93 分（176 秒）

---

## Beat 0 — 三個運算，還是兩個？ / three operations, or two?
*配音長度：中文 17.3s ／ 英文 14.2s*

**畫面公式**

```
三個運算，還是兩個？   |   three operations, or two?
ℝᴬ  :  f + g  ,  x f  ,  f g          V  :  α + β  ,  x α
```

**旁白（繁中）**

> 先問一個問題。A 上的實值函數，除了相加與數乘之外，其實還可以逐點相乘；連續函數也一樣。既然有三個運算，為什麼還要特地談只有兩個運算的向量空間？

**Narration (EN)**

> Start with a question. Real-valued functions on a set can be multiplied pointwise as well as added and scaled, and so can the continuous ones. With three operations available, why bother with vector spaces, which have only two?

**動畫**

兩個方框：左邊函數空間列出 f+g、xf、fg 三個運算，第三個被劃掉；右邊向量空間只有兩個。

## Beat 1 — 積分保持和，不保持積 / the integral keeps sums, not products
*配音長度：中文 20.7s ／ 英文 16.9s*

**畫面公式**

```
積分保持和，不保持積   |   the integral keeps sums, not products
T ( f ) = ∫ f        T ( f + g ) = T f + T g        T ( f g )  ≠  T f · T g
```

**旁白（繁中）**

> 答案是：最重要的那些映射，保持的正好是這兩個向量運算。書上的例子是積分：閉區間上連續函數的積分，把和送到和、把倍數送到倍數，但它完全不保持乘積，兩個函數乘起來的積分不等於各自積分的乘積。

**Narration (EN)**

> Because the most important mappings are exactly the ones that preserve those two. The book's example is the integral: it sends sums to sums and multiples to multiples, but it does not preserve products at all, since the integral of a product is not the product of the integrals.

**動畫**

四張面積圖：f 與 g 的面積相加正好是 f+g 的面積；右邊 fg 那張打一個大叉，因為它不等於兩個面積相乘。

## Beat 2 — 線性方程組就是這種映射 / a linear system is such a map
*配音長度：中文 20.7s ／ 英文 16.4s*

**畫面公式**

```
線性方程組就是這種映射   |   a linear system is such a map
y₁ = 2x₁ − x₂ + x₃        y₂ = x₁ + 3x₂ − 5x₃
```

**旁白（繁中）**

> 另一個例子是把三元組送到二元組的那種對應，每個分量都是原來三個座標的一次組合。線性方程組能不能解，本質上就是這種映射的理論。所以我們研究向量空間，有一部分正是為了研究保持向量運算的映射。

**Narration (EN)**

> Another is the map sending a triple to a pair, each entry a combination of the three coordinates. Whether a linear system can be solved is essentially the theory of such maps. So we study vector spaces partly to study the maps that preserve their operations.

**動畫**

三個輸入點連到兩個輸出點的網，每個輸出都吃到全部三個輸入。

## Beat 3 — 線性變換的定義 / the definition of a linear transformation
*配音長度：中文 19.1s ／ 英文 18.0s*

**畫面公式**

```
線性變換的定義   |   the definition of a linear transformation
T ( α + β ) = T α + T β    T ( xα ) = x T α        T ( xα + yβ ) = x Tα + y Tβ
```

**旁白（繁中）**

> 定義因此是這樣：從 V 到 W 的一個映射叫線性變換，如果它把和送到和、把純量倍數送到純量倍數。這兩個條件可以併成一條：把「x 倍的 α 加上 y 倍的 β」送到「x 倍的 T α 加上 y 倍的 T β」。

**Narration (EN)**

> The definition follows: a mapping from V to W is a linear transformation if it sends sums to sums and scalar multiples to scalar multiples. The two conditions combine into one: x times alpha plus y times beta goes to x times T alpha plus y times T beta.

**動畫**

左邊 V 裡一個平行四邊形，右邊是它經 T 之後的像。形狀確實變了，但仍然是平行四邊形——結構活下來了。

## Beat 4 — 推廣到任意有限和 / extended to any finite sum
*配音長度：中文 15.4s ／ 英文 14.4s*

**畫面公式**

```
推廣到任意有限和   |   extended to any finite sum
T ( Σ xᵢ αᵢ )  =  Σ xᵢ T ( αᵢ )
```

**旁白（繁中）**

> 用歸納法，這件事馬上推廣到任意有限和：任何線性組合經過 T 之後，還是原來那些像的線性組合，係數一模一樣。積分的性質正是這個式子的特例。

**Narration (EN)**

> By induction this extends at once to any finite sum: a linear combination goes to the linear combination of the images, with exactly the same coefficients. The property of the integral is a special case of this equation.

**動畫**

三支首尾相接的向量與它們的和，在兩邊各畫一次。係數一模一樣，只是每一支都被 T 換過。

## Beat 5 — 以座標空間為定義域 / with coordinate space as domain
*配音長度：中文 17.1s ／ 英文 14.8s*

**畫面公式**

```
以座標空間為定義域   |   with coordinate space as domain
x  ↦  Σ₁³ xᵢ fᵢ        f₁ = sin  ,  f₂ = cos  ,  f₃ = exp
```

**旁白（繁中）**

> 現在來找出所有以 n 維座標空間為定義域的線性映射。先看一個具體的：固定三個函數，把一個三元組送到「以它的三個分量為係數」的那個線性組合。這顯然是線性的。

**Narration (EN)**

> Now to find every linear map whose domain is coordinate n-space. Take a concrete one first: fix three functions and send a triple to the combination having its three entries as coefficients. This is plainly linear.

**動畫**

左邊三條函數曲線，中間一個三元組，右邊是加權和出來的那條新曲線。

## Beat 6 — 餵單位向量，讀回 skeleton / feed the unit vectors, read the skeleton
*配音長度：中文 17.1s ／ 英文 14.8s*

**畫面公式**

```
餵單位向量，讀回 skeleton   |   feed the unit vectors, read the skeleton
T ( δ ʲ )  =  fⱼ        skeleton  =  { T ( δ ⁱ ) }₁ⁿ
```

**旁白（繁中）**

> 有趣的是，從這個映射可以把那三個函數讀回來。把只有第 j 個位置是一的那個向量餵進去，出來的正好是第 j 個函數。這一組像所成的 n 元組，書上叫做 T 的 skeleton。

**Narration (EN)**

> What is interesting is that the three functions can be read back off the map. Feed in the vector with a one in the jth place and zeros elsewhere, and out comes the jth function. That n-tuple of images is what the book calls the skeleton of T.

**動畫**

三列：δ¹、δ²、δ³ 各自經 T 送到 f₁、f₂、f₃；右邊那一整欄用框圈起來，那就是 skeleton。

## Beat 7 — 定理：兩個方向都成立 / the theorem: both directions hold
*配音長度：中文 20.5s ／ 英文 18.3s*

**畫面公式**

```
定理：兩個方向都成立   |   the theorem: both directions hold
Lα ( x )  =  Σ₁ⁿ xᵢ αᵢ        skeleton ( Lα )  =  α        T  =  L β
```

**旁白（繁中）**

> 定理是這樣說的。給定 W 裡任何一個 n 元組，對應的線性組合映射是線性的，而且它的 skeleton 正好就是那個 n 元組。反過來，任何一個從 n 維座標空間出發的線性映射，都等於它自己 skeleton 的線性組合映射。

**Narration (EN)**

> The theorem runs as follows. Given any n-tuple in W, the corresponding linear combination mapping is linear, and its skeleton is exactly that n-tuple. Conversely, every linear map out of coordinate n-space equals the linear combination mapping of its own skeleton.

**動畫**

兩個方框與兩支反方向的箭頭：往右是「做線性組合映射」，往左是「取 skeleton」。來回一圈回到原地，定理的兩半正好就是這兩支箭頭。

## Beat 8 — 只有第 j 項活下來 / only the jth term survives
*配音長度：中文 23.2s ／ 英文 17.2s*

**畫面公式**

```
只有第 j 項活下來   |   only the jth term survives
T ( δ ʲ ) = Σ δ ʲᵢ βᵢ = βⱼ        T ( x ) = T ( Σ xᵢ δ ⁱ ) = Σ xᵢ βᵢ
```

**旁白（繁中）**

> 證明兩半都很短。線性用的是跟前一集那個定理一樣的論證。至於 skeleton，把第 j 個單位向量餵進線性組合映射，只有第 j 項活下來。反過來，任何向量都是單位向量的線性組合，套上 T 再用線性，就回到線性組合映射。

**Narration (EN)**

> Both halves are short. Linearity repeats the previous episode's argument. For the skeleton, feeding in the jth unit vector leaves only the jth term. Conversely any vector is a combination of unit vectors, so applying T and using linearity gets us back.

**動畫**

一排係數方塊，只有第 j 個是一、其餘都是零而且被劃掉，底下只剩 β 的第 j 項掉出來。

## Beat 9 — n 元組與線性映射是一對一的 / n-tuples and linear maps correspond
*配音長度：中文 15.4s ／ 英文 14.3s*

**畫面公式**

```
n 元組與線性映射是一對一的   |   n-tuples and linear maps correspond
α  ↦  Lα  :  Wⁿ  ⟷  { T : ℝⁿ → W }        T  ↦  skeleton ( T )
```

**旁白（繁中）**

> 換個說法：從「W 裡的 n 元組」到「所有從 n 維座標空間到 W 的線性映射」，這個對應是一個雙射，而它的反函數就是取 skeleton。兩邊的資訊量完全一樣。

**Narration (EN)**

> Put another way: the correspondence from n-tuples in W to linear maps from coordinate n-space into W is a bijection, and its inverse is taking the skeleton. The two sides carry exactly the same information.

**動畫**

兩欄點一一對應的雙射圖，兩邊都畫刪節號表示還有更多。

## Beat 10 — 上域是實數線的特例 / the case of the real line
*配音長度：中文 17.6s ／ 英文 16.4s*

**畫面公式**

```
上域是實數線的特例   |   the case of the real line
W = ℝ    ⇒    skeleton  ∈  ℝⁿ
```

**旁白（繁中）**

> 書上說這是一個極其重要的定理，雖然看起來簡單，並且要讀者把它牢牢記住。skeleton 這個詞會一直用到第三章。下一集就從它最簡單的特例開始：上域是實數線的時候。

**Narration (EN)**

> The book calls this a tremendously important theorem, simple though it may seem, and urges the reader to fix it in mind. The word skeleton stays with us for the first three chapters. The next episode starts from its simplest case, when the codomain is the real line.

**動畫**

上排是一般 W 的 skeleton 項，箭頭往下指到上域是實數線的情形——每一項只剩一個數。
