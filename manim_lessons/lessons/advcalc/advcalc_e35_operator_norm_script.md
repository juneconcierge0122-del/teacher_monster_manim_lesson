# advcalc E35 — 第 3 章：算子範數與 Hom(V, W)

Chapter 3: The Operator Norm and Hom(V, W)

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 3 節的後段（書頁 128–129）。書頁 129 起是習題 3.1–3.22，第 4 節「等價範數」從書頁 132 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e35_operator_norm.py`（`AdvCalcE35ZH` / `AdvCalcE35EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[35]` / `FORMULAS_ADVCALC[35]`）
- 配音：`manim_lessons/samples/audio_e35/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.37 分（202 秒）／英文 3.12 分（187 秒）

## 一個映射貫串整集，所有數字互相對得起來

這一集從頭到尾用 E34 的同一個線性映射（矩陣 `[[2, −1], [1, 1]]`，兩邊都配一致範數），
好處是每個數字都可以拿別的數字來核：

- **算子範數是掃單位球面掃出來的**（1440 個方向），不是從矩陣讀出來的；算完再斷言它跟
  「每列絕對值和取最大」這個公式一致。四個矩陣（T、S、S∘T、S+T）都這樣核過。
- **beats 3 與 4 是「三種寫法同一個數」**，所以程式把三種寫法各算一次——商的最小上界、
  單位球面上的最小上界、閉單位球上的最小上界——再斷言三個浮點數相等。這一句話是這兩拍
  的全部內容，用斷言講比用旁白講可靠。
- **beat 6 的下界是像的內接半徑**，用同一支掃描程式取最小值，再斷言它等於反矩陣算子範數的
  倒數（兩者都是 1）。上界 3 與下界 1 因此可以畫在同一張圖上：外框與內接的球。
- **beat 2 的三個商都是數值積分算的**：常數函數 2.00、隆起 1.00、尖峰 0.25，並斷言只有
  常數把 2 取到、另外兩個嚴格小於 2、而且三個數字彼此不同（初稿的第三個函數用斜坡，
  商也是 1.00，跟第二個一模一樣，畫面上兩個數字重複就白畫了一張圖）。
- **beats 8 與 9 斷言兩個不等式都是嚴格的**——如果隨手挑的 S 剛好取到等號，畫面上寫著
  「≤」卻畫出等號，就會誤導。這一對是 3 ≤ 5 與 3 ≤ 6。

`bounds.py` 第一輪抓到 beat 10 的等高線衝出畫面（斜率 2，照面板寬度截會跑到 y = 2.36），
改成照高度截。`collide.py` 兩輪都是 0。

---

## Beat 0 — 最小的那個界值得一個名字 / the smallest bound deserves a name
*配音長度：中文 17.4s ／ 英文 18.1s*

**畫面公式**

```
最小的那個界值得一個名字   |   the smallest bound deserves a name
‖ T ‖    =    lub { ‖ T ( α ) ‖ / ‖ α ‖    :    α ≠ 0 }
```

**旁白（繁中）**

> 上一集說有界線性映射的界不只一個，任何比它大的數也是界，所以真正該記住的是最小的那一個。把它定義成所有商的最小上界，這個數就叫 T 的算子範數，寫成兩條槓夾著 T。

**Narration (EN)**

> Last time a bounded linear map had many bounds, since anything larger is a bound too, so the one worth remembering is the smallest. Define it as the least upper bound of all those quotients, and the number is called the operator norm of T, written with two bars around T.

**動畫**

橫軸是方向繞一圈，縱軸是那個方向上的商。曲線是掃 360 個方向算出來的（分段線性，所以有折角）。紅色虛線是最小上界 3，紫色虛線是最大下界 1。

## Beat 1 — 跑得最遠的方向決定它 / the furthest direction fixes it
*配音長度：中文 19.4s ／ 英文 17.8s*

**畫面公式**

```
跑得最遠的方向決定它   |   the furthest direction fixes it
‖ T ( α ) ‖  ≤  ‖ T ‖ · ‖ α ‖           ‖ T ‖  =  3
```

**旁白（繁中）**

> 上一集那個例子的算子範數是三。畫面上是單位球的像：跑得最遠的方向決定這個數，其他方向都比較短。有了它，那條不等式就有了最好的寫法：像的範數不超過算子範數乘上向量的範數。

**Narration (EN)**

> For last episode's map that number is three. On screen is the image of the unit ball: the direction that travels furthest fixes the number and every other direction falls short. With it the inequality gets its best form, the image bounded by the operator norm times the vector.

**動畫**

藍色單位球、紅色是它的像、紫色是半徑等於算子範數的球。兩顆橘點是像碰到紫球的方向。

## Beat 2 — 積分：界剛好取得到 / the integral: a bound that is attained
*配音長度：中文 19.5s ／ 英文 15.5s*

**畫面公式**

```
積分：界剛好取得到   |   the integral: a bound that is attained
T ( f )  =  ∫ f           ‖ T ‖  =  b − a  =  2
```

**旁白（繁中）**

> 積分那個例子也算得出來。界是區間長度，而常數函數一剛好把它取到，所以沒有更小的界，算子範數就正好等於區間長度。畫面上另外兩個函數的商都比它小，這就是最小上界的意思。

**Narration (EN)**

> The integral example can be computed too. The bound is the length of the interval, and the constant function one attains it, so no smaller bound exists and the operator norm is that length exactly. The other functions on screen give smaller quotients.

**動畫**

三個小圖並排：常數函數、隆起、尖峰，各自填滿到 x 軸，上方虛線是一致範數的高度。每個圖下面標著它的商：2.00、1.00、0.25。

## Beat 3 — 齊次性把分母消掉 / homogeneity removes the denominator
*配音長度：中文 17.4s ／ 英文 16.7s*

**畫面公式**

```
齊次性把分母消掉   |   homogeneity removes the denominator
‖ T ( α ) ‖ / ‖ α ‖   =   ‖ T ( α / ‖ α ‖ ) ‖           ‖ β ‖ = 1
```

**旁白（繁中）**

> 定義裡的分母其實可以消掉。線性映射是齊次的，把向量先除以自己的範數再送進去，得到的正好是那個商。所以只要在單位球面上取最小上界就夠了，分母不必出現。

**Narration (EN)**

> The denominator can be removed. A linear map is homogeneous, so dividing the vector by its own norm before feeding it in produces exactly that quotient. It is therefore enough to take the least upper bound over the unit sphere, with no denominator in sight.

**動畫**

左邊 V 面板一支長箭頭，箭身上一顆橘點是把它除以自己範數之後的落點；右邊 W 面板是像的箭頭，橘點在對應位置。右邊標著 6 / 2 = 3 / 1 = 3。

## Beat 4 — 整顆閉單位球，答案一樣 / the whole closed ball, same answer
*配音長度：中文 16.3s ／ 英文 14.6s*

**畫面公式**

```
整顆閉單位球，答案一樣   |   the whole closed ball, same answer
‖ T ‖    =    lub { ‖ T ( γ ) ‖    :    ‖ γ ‖ ≤ 1 }
```

**旁白（繁中）**

> 還可以再放寬一點。閉單位球裡的向量都寫得成一個長度不超過一的數乘上單位向量，像的範數只會更小。所以在整顆閉單位球上取最小上界，答案完全一樣。

**Narration (EN)**

> It can be relaxed once more. Every vector in the closed unit ball is a number of size at most one times a unit vector, and its image can only be shorter. So taking the least upper bound over the whole closed ball gives the same answer.

**動畫**

兩顆同心的球（藍色單位球、灰色縮小版）與它們的像（紅色、紫色）。縮小的球給出縮小同樣比例的像，所以最大的商一定在球面上。

## Beat 5 — 「有界」回到最原始的意思 / bounded means what it always did
*配音長度：中文 17.6s ／ 英文 16.6s*

**畫面公式**

```
「有界」回到最原始的意思   |   bounded means what it always did
‖ T ‖    =    ‖ T | B ₁ ‖ ∞
```

**旁白（繁中）**

> 這兩種寫法其實是一致範數：算子範數就是 T 限制在閉單位球上的一致範數。繞了一圈，「有界」又回到最原始的意思，就是值域是有界集，只是要先把定義域限制在那顆球上。

**Narration (EN)**

> Those last two are uniform norms: the operator norm is the uniform norm of T restricted to the closed unit ball. The word bounded has come full circle and means what it always did, that a range is a bounded set, once the domain is cut down to that ball.

**動畫**

藍色單位球、紅色的像整片畫上斜線填滿（那就是限制後的值域）、紫色的框是最小的外接球。

## Beat 6 — 有下界：像縮不到多小 / bounded below: the image cannot collapse
*配音長度：中文 18.8s ／ 英文 16.5s*

**畫面公式**

```
有下界：像縮不到多小   |   bounded below: the image cannot collapse
‖ T ( ξ ) ‖  ≥  b ‖ ξ ‖           b  =  1 / ‖ T ⁻¹ ‖  =  1
```

**旁白（繁中）**

> 反過來也有一個概念。如果像的範數不小於某個正數乘上向量的範數，就說 T 有下界。如果 T 有有界的反映射，下界可以取成反映射的算子範數的倒數。畫面上這個例子算出來是一。

**Narration (EN)**

> There is a notion the other way round. If the image has norm at least some positive number times the vector's norm, T is bounded below. If T has a bounded inverse, that number may be taken to be one over the operator norm of the inverse; on screen it comes out at one.

**動畫**

紅色的像、藍色的內接球（半徑就是最大的下界）、紫色的外接球。兩顆橘點是像最靠近原點的地方。

## Beat 7 — 有下界不保證可逆 / bounded below does not force invertible
*配音長度：中文 18.3s ／ 英文 16.6s*

**畫面公式**

```
有下界不保證可逆   |   bounded below does not force invertible
S ( x ₁ , x ₂ , … )  =  ( 0 , x ₁ , x ₂ , … )           ‖ S ξ ‖  =  ‖ ξ ‖
```

**旁白（繁中）**

> 但有下界不保證可逆，無窮維就會出事。把數列整個往右推一格，長度完全沒變，所以下界是一，可是第一格永遠是零，值域整整漏掉一個方向。有限維才有「有下界就可逆」。

**Narration (EN)**

> But bounded below does not force invertibility, and infinite dimensions break it. Push a sequence one slot to the right: the length is unchanged, so the bound below is one, yet the first slot is always zero and the range misses a whole direction.

**動畫**

上下兩排長條圖：上排是原數列，下排是往右推一格之後的數列，第一格畫成一顆灰點（永遠是零）。右邊標著 (1, 0, 0, …) 不在值域裡。

## Beat 8 — 定理 3.2：Hom 自己是賦範空間 / Theorem 3.2: Hom is itself normed
*配音長度：中文 19.0s ／ 英文 18.2s*

**畫面公式**

```
定理 3.2：Hom 自己是賦範空間   |   Theorem 3.2: Hom is itself normed
‖ S + T ‖  ≤  ‖ S ‖ + ‖ T ‖           3  ≤  2 + 3
```

**旁白（繁中）**

> 把所有有界線性映射收在一起，記成 Hom V W。定理 3.2 說它自己就是一個賦範線性空間，範數就是剛才那個算子範數。三角不等式與齊次性都成立，畫面上是一組真的算過的數字。

**Narration (EN)**

> Collect all the bounded linear maps and call the collection Hom of V and W. Theorem three point two says it is itself a normed linear space under that same operator norm. The triangle inequality and homogeneity both hold, and the numbers on screen were actually computed.

**動畫**

四根長條：‖S‖ = 2、‖T‖ = 3、‖S + T‖ = 3、‖S‖ + ‖T‖ = 5。第三根比第四根矮，不等式是嚴格的。

## Beat 9 — 定理 3.3：合成只會變小 / Theorem 3.3: composition only shrinks
*配音長度：中文 19.4s ／ 英文 18.4s*

**畫面公式**

```
定理 3.3：合成只會變小   |   Theorem 3.3: composition only shrinks
‖ S ∘ T ‖  ≤  ‖ S ‖ · ‖ T ‖           3  ≤  2 · 3
```

**旁白（繁中）**

> 定理 3.3 講合成：兩個映射接起來的算子範數，不超過兩個算子範數的乘積。注意這是不等式不是等式，畫面上這一對是三對六。而且「右邊固定接上 T」這件事本身也是有界線性變換。

**Narration (EN)**

> Theorem three point three is about composition: the operator norm of two maps joined together is at most the product of the two operator norms. It is an inequality and not an equality; the pair on screen reads three against six. Composing on the right by a fixed T is itself bounded.

**動畫**

三個面板串起來：單位球、經過 T 之後的像、再經過 S 之後的像，中間兩支箭頭。下方標著 ‖S∘T‖ = 3 與 ‖S‖·‖T‖ = 6。

## Beat 10 — V 星：有界線性泛函 / V star: the bounded functionals
*配音長度：中文 19.2s ／ 英文 18.0s*

**畫面公式**

```
V 星：有界線性泛函   |   V star: the bounded functionals
V *  =  Hom ( V , ℝ )           ‖ L ₐ ‖  =  ‖ a ‖ ₁  =  3
```

**旁白（繁中）**

> 最後回到對偶空間。V 星現在是所有有界線性泛函的空間。在配上一致範數的平面上，用一個固定向量作內積得到的泛函，算子範數正好等於那個向量的一範數。下一集講等價範數。

**Narration (EN)**

> Finally back to the conjugate space. V star is now the space of bounded linear functionals. On the plane with the uniform norm, the functional given by the inner product with a fixed vector has operator norm exactly the one norm of that vector. Next time, equivalent norms.

**動畫**

單位球加上泛函的三條等高線（中間灰色那條是零），兩條紅線剛好擦過球的兩個角，橘點標出來；紫色箭頭是那個固定向量。

---

## 為什麼「有界」在這一節繞了一圈

第 3 節一開始警告過：線性映射的「有界」不是「值域是有界集」。beat 5 把這件事收回來——
算子範數就是 T **限制在閉單位球上**的一致範數，所以「有界」確實還是最原始的那個意思，
只是定義域要先切到那顆球上。這一拍的圖（限制後的值域是一片有界的區域）就是那句話的圖解。

## 有下界卻不可逆

書上說「有限維時有下界就可逆，一般情況不成立」，但沒有給例子。beat 7 用右移算子補上：
把數列整條往右推一格，一致範數完全不變（所以下界是 1），可是第一格永遠是零，
`(1, 0, 0, …)` 不在值域裡。這是自己選的例子，不是書上的。
