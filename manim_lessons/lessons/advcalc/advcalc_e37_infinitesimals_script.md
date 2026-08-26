# advcalc E37 — 第 3 章：無窮小、大 O 與小 o

Chapter 3: Infinitesimals, Big Oh and Little Oh

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 5 節（書頁 136–139）。書頁 140 是習題 5.1–5.11，第 6 節「微分」從書頁 140 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e37_infinitesimals.py`（`AdvCalcE37ZH` / `AdvCalcE37EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[37]` / `FORMULAS_ADVCALC[37]`）
- 配音：`manim_lessons/samples/audio_e37/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.53 分（212 秒）／英文 3.38 分（203 秒）

## 花體字母改成 S、O、o

書上把三個類寫成花體的 script S、script O 與 script o。渲染用的字型雖然吃得下那三個碼位，
但無法確定顯示出來的字形長什麼樣，而且花體 O 跟花體 o 在 17pt 底下幾乎分不出大小寫——
這一集整集都在講「大 O 與小 o 的差別」，字形分不出來就毀了。所以畫面一律用 `S`、`O`、`o`，
這也是大家平常讀的寫法。

## 每一個比值都是算出來的

三個類的差別完全在「比值的行為」上，所以場景檔把比值算出來擺在畫面上，並且斷言它們的行為：

- `√|x|` 的比值在 x = 0.001 時已經是 31.6，斷言它大於 30（爆炸）。
- `x` 的比值斷言恆等於 1（不是「趨近 1」，是每一個取樣點都等於 1）。
- `x²` 的比值斷言在最後一點小於 0.01，而且比第一點小。
- 另外掃 41 個取樣點，斷言**只有**根號那一個逃得出所有 Lipschitz 常數——
  這一條防的是「換了例子卻忘了改旁白」。
- beat 7 的合成（x² 接 x²）斷言比值單調下降而且最後小於 1e-8。
- beat 8 的乘積斷言比值**正好等於** `√|x|`（誤差 1e-12），因為旁白就是這樣說的。
- **beat 9 是這一集的重點**：斷言線性映射的比值在四個取樣點上完全相同（差 1e-12 以內）。
  它不動，所以不可能趨於零，所以 Hom 與小 o 只交於零映射。
- beat 10 用兩個不同的範數算同一個比值，斷言兩個都趨於零、而且彼此只差有限倍（0.5 到 2 之間）。

`bounds.py` 第一輪抓到 beat 1 的曲線衝到 y = 2.21（縱向比例沒縮），以及 beat 0 的不規則形狀
凸出畫面左緣。`collide.py` 抓到 beat 6 最內圈的橢圓穿過 `x²` 這個標籤。

---

## Beat 0 — 鄰域，與去心鄰域 / neighborhoods, and deleted ones
*配音長度：中文 22.0s ／ 英文 19.2s*

**畫面公式**

```
鄰域，與去心鄰域   |   neighborhoods, and deleted ones
A   ⊃   B ᵣ ( α )             A ∖ { α }
```

**旁白（繁中）**

> 這一節要把「無窮小」講清楚。早期的書把它講得像邏輯上的胡話，很多現代教科書乾脆避開，但想法本身很有用。先定好兩個詞：包含以某點為心的一顆開球的集合，叫那一點的鄰域；去心鄰域就是鄰域挖掉那一點。

**Narration (EN)**

> This section makes the word infinitesimal respectable. Early treatments amounted to logical nonsense and many modern books avoid it, yet the idea is useful. Two words first: a set containing an open ball about a point is a neighborhood of it; delete the point and it is a deleted one.

**動畫**

兩團不規則的形狀，各自包著一顆以 α 為心的球。左邊那顆 α 是實心點，右邊挖成空心圈——那就是去心鄰域。

## Beat 1 — 重點是趨於零的速度 / what matters is the rate
*配音長度：中文 21.9s ／ 英文 17.0s*

**畫面公式**

```
重點是趨於零的速度   |   what matters is the rate
Δf ( t )  −  l ( t )   ∈   o             l ( t )  =  f ′ ( a ) · t
```

**旁白（繁中）**

> 為什麼要它？導數的定義裡，分子的變化量與分母的增量都趨於零，真正有內容的是「差商減掉導數之後還是趨於零」。把它乘回增量，就得到一個比增量更快趨於零的函數。整個微分學就是在研究趨於零的速度。

**Narration (EN)**

> Why bother? In the definition of a derivative both the change on top and the increment underneath go to zero; what carries content is that the difference quotient minus the derivative still goes to zero. Multiplied back by the increment, that vanishes faster than the increment.

**動畫**

青色是實際的變化量、紫色是它的線性部分，兩條紅色虛線標出兩處的差。

## Beat 2 — 無窮小 S：會趨於零就好 / the infinitesimals S: it just has to vanish
*配音長度：中文 18.4s ／ 英文 18.9s*

**畫面公式**

```
無窮小 S：會趨於零就好   |   the infinitesimals S: it just has to vanish
S :    f ( 0 ) = 0  ,    f ( ξ )  ⟶  0        ( ξ → 0 )
```

**旁白（繁中）**

> 底下三個類的函數都從零的一個鄰域映到另一個賦範空間。第一個寫成 S：在零的值是零，而且在零連續。書上把這一類叫做無窮小，它只要求「會趨於零」，沒有要求趨得多快。

**Narration (EN)**

> The three classes below all consist of maps from a neighborhood of zero into another normed space. The first is written S: the value at zero is zero and the map is continuous there. The book calls these the infinitesimals; they must approach zero, with no demand on how fast.

**動畫**

三條曲線（根號、直線、拋物線）在原點都收到零。S 只要求這件事，分不出三者的差別。

## Beat 3 — 大 O：被一個楔形壓住 / big oh: held inside a wedge
*配音長度：中文 18.6s ／ 英文 17.6s*

**畫面公式**

```
大 O：被一個楔形壓住   |   big oh: held inside a wedge
O :    ‖ f ( ξ ) ‖   ≤   c ‖ ξ ‖             ( ‖ ξ ‖ < r )
```

**旁白（繁中）**

> 第二個叫大 O：在零的值是零，而且在零是 Lipschitz 連續。也就是說，存在正的半徑與常數，使得在那顆球裡，像的範數不超過常數乘上向量的範數。畫面上那個楔形就是這個條件。

**Narration (EN)**

> The second is called big oh: the value at zero is zero and the map is Lipschitz continuous there. That is, there are a positive radius and a constant such that inside that ball the image has norm at most the constant times the vector's norm. The wedge on screen is that condition.

**動畫**

同樣三條曲線，加上一條橘色的直線代表楔形的邊。青色與紫色壓在下面，紅色鑽了出去。

## Beat 4 — 小 o：比自變數更快 / little oh: faster than its argument
*配音長度：中文 17.8s ／ 英文 17.5s*

**畫面公式**

```
小 o：比自變數更快   |   little oh: faster than its argument
o :    ‖ f ( ξ ) ‖ / ‖ ξ ‖   ⟶   0          ( ξ → 0 )
```

**旁白（繁中）**

> 第三個叫小 o：在零的值是零，而且像的範數除以向量的範數趨於零。這比大 O 強，它要求「不只被常數壓住，而且比向量本身更快趨於零」，楔形不管開多小，最後都關得住它。

**Narration (EN)**

> The third is little oh: the value at zero is zero and the image's norm divided by the vector's norm goes to zero. This is stronger: not merely held down by a constant, but vanishing faster than the vector itself, so however narrow the wedge it is caught in the end.

**動畫**

楔形越關越窄（三條斜率遞減的線）。青色的拋物線最後總是關得住，紫色的直線關到某個角度就不行了。

## Beat 5 — 三個例子把三個類分開 / three examples, three classes
*配音長度：中文 18.0s ／ 英文 20.0s*

**畫面公式**

```
三個例子把三個類分開   |   three examples, three classes
√ | x |  ∈  S ∖ O           x  ∈  O ∖ o           x ²  ∈  o
```

**旁白（繁中）**

> 三個很短的例子就把三個類分開。根號絕對值 x 在 S 裡但不在大 O 裡，比值會爆炸；x 自己在大 O 裡但不在小 o 裡，比值永遠是一；x 平方三個都在。表上是算出來的數字。

**Narration (EN)**

> Three very short examples separate the three classes. The square root of the size of x is in S but not in big oh, since its quotient explodes. x itself is in big oh but not little oh, its quotient being one forever. x squared is in all three. The table holds the computed numbers.

**動畫**

三個比值畫在同一張圖上：紅色往左爆炸、紫色是水平線、青色往左收到零。右邊是四個取樣點的數字表。

## Beat 6 — 定理 5.1：三個都是向量空間 / Theorem 5.1: all three are vector spaces
*配音長度：中文 17.6s ／ 英文 18.6s*

**畫面公式**

```
定理 5.1：三個都是向量空間   |   Theorem 5.1: all three are vector spaces
o    ⊂    O    ⊂    S
```

**旁白（繁中）**

> 定理 5.1 第一條：小 o 包含在大 O 裡，大 O 包含在 S 裡，而且三個類對加法與係數倍都封閉。所以它們都是向量空間，可以像向量一樣加來加去，這正是後面推導微分規則要用的。

**Narration (EN)**

> Theorem five point one, first part: little oh sits inside big oh, which sits inside S, and all three are closed under addition and scalar multiples. So each is a vector space and they can be added like vectors, which is exactly what deriving the rules of differentiation needs.

**動畫**

三個同心的橢圓標著 S、O、o，三個例子各放一顆點在該落的環裡：根號在最外環、x 在中環、x 平方在最內環。

## Beat 7 — 合成：有一個是小 o 就夠 / composition: one little oh is enough
*配音長度：中文 18.7s ／ 英文 18.6s*

**畫面公式**

```
合成：有一個是小 o 就夠   |   composition: one little oh is enough
g ∘ f  ∈  O            ( f ∈ o  ∨  g ∈ o )   ⇒   g ∘ f  ∈  o
```

**旁白（繁中）**

> 第二、三條講合成。大 O 接大 O 還是大 O，因為兩個常數乘起來就是新的常數。而只要兩個裡面有一個是小 o，合成就掉進小 o——畫面上是 x 平方接 x 平方，比值變成 x 的三次方。

**Narration (EN)**

> Parts two and three are about composition. Big oh after big oh is big oh, since the two constants multiply into a new one. And if either one is little oh the composite falls into little oh: on screen, x squared after x squared, whose quotient becomes x cubed.

**動畫**

三個圓排成一列，中間兩支箭頭，代表 V 到 W 到 X 的合成。右邊是 x² 接 x² 的比值表。

## Beat 8 — 乘積：大 O 乘無窮小落進小 o / product: big oh times an infinitesimal
*配音長度：中文 20.0s ／ 英文 17.7s*

**畫面公式**

```
乘積：大 O 乘無窮小落進小 o   |   product: big oh times an infinitesimal
f ∈ O ,   g ∈ S              ⇒              f g   ∈   o
```

**旁白（繁中）**

> 第四、五條講乘積。一個大 O 乘上一個無窮小，結果落在小 o 裡。畫面上是 x 乘根號絕對值 x，比值就等於根號絕對值 x，確實趨於零。後面算微分的乘法規則時，會一直用到這一條。

**Narration (EN)**

> Parts four and five are about products. A big oh times an infinitesimal lands in little oh. On screen that is x times the square root of the size of x, whose quotient is the square root itself and does go to zero. The product rule for differentials leans on this constantly.

**動畫**

根號曲線（那就是 x 乘根號絕對值 x 的比值），加上四個取樣點的數字表。

## Beat 9 — Hom 與小 o 只交於零映射 / Hom meets little oh only at zero
*配音長度：中文 20.0s ／ 英文 19.0s*

**畫面公式**

```
Hom 與小 o 只交於零映射   |   Hom meets little oh only at zero
Hom ( V , W )  ⊂  O ( V , W )             Hom  ∩  o  =  { 0 }
```

**旁白（繁中）**

> 第六、七條最關鍵。每個有界線性映射都在大 O 裡，這只是把定義抄一遍。可是 Hom 跟小 o 只交於零映射：非零的線性映射沿著一條射線走，比值是固定的常數，畫面上永遠是三，不可能趨於零。

**Narration (EN)**

> Parts six and seven matter most. Every bounded linear map is in big oh, which is the definition copied out. But Hom meets little oh only at the zero map: walk a nonzero linear map along a ray and the quotient is a fixed constant, three on screen, which cannot go to zero.

**動畫**

紅色虛線是線性映射的比值，一條水平線（永遠是 3）；青色是 x 平方的比值，往左收到零。

## Beat 10 — 換等價範數，三個類不動 / an equivalent norm changes nothing
*配音長度：中文 18.7s ／ 英文 18.8s*

**畫面公式**

```
換等價範數，三個類不動   |   an equivalent norm changes nothing
Δf   =   l   +   o             l ₁  =  l ₂
```

**旁白（繁中）**

> 這一條就是「微分唯一」的理由——一個變化量最多只有一種寫成「線性部分加小 o」的方式。最後補一句，三個類換成等價範數完全不變，因為常數只差有限的倍數。下一集開始講微分。

**Narration (EN)**

> That is exactly why a differential is unique: a change can be written as a linear part plus little oh in at most one way. One remark to close: the three classes survive a change to an equivalent norm, since the constants differ only by a bounded factor. Next time, the differential.

**動畫**

同一個平方映射在兩種範數底下的比值，兩條曲線都收到零，只是數字不同。右邊是對照表。

---

## 為什麼 beat 9 值得單獨一拍

`Hom ∩ o = {0}` 看起來只是定理 5.1 的第七項，但整個微分學的「唯一性」全靠它：
一個變化量寫成「線性部分加小 o」的方式只有一種，正是因為兩個候選的差同時落在
Hom 與小 o 裡，而那裡只有零映射。E38 定義微分時會直接引用這一句，所以這裡把它
畫成一張圖：**線性映射的比值是一條水平線，永遠不動。**

書上還加了一句 remark：證明只用到齊次性，沒用到可加性。所以更強的結論是——
一次齊次的函數裡，除了零以外沒有小 o。這句話也放進收尾字幕。
