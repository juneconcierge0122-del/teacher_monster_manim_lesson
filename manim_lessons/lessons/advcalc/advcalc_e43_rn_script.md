# advcalc E43 — 第 3 章：微分與 ℝⁿ

Chapter 3: The Differential and Real n-Space

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 9 節（書頁 156–159）。書頁 159–160 是習題 9.1–9.11，第 10 節「初等應用」從書頁 161 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e43_rn.py`（`AdvCalcE43ZH` / `AdvCalcE43EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[43]` / `FORMULAS_ADVCALC[43]`）
- 配音：`manim_lessons/samples/audio_e43/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.06 分（183 秒）／英文 2.95 分（177 秒）

## 一個映射，把整節的每一句話都驗過

這一集從頭到尾用同一個映射：把平面向量送到它「複數平方」的那一個，
`F(x₁, x₂) = (x₁² − x₂², 2x₁x₂)`。好處是它的每一件事都算得出來，而且互相核得起來：

- **雅可比矩陣**用中央差商算出來（不是手推），斷言它的元素都是整數，
  在取樣點 (1, 0.5) 得到 2、−1、1、2。
- **每一行都是一個方向導數**：斷言沿 δ¹ 與 δ² 的方向導數分別等於第一行與第二行。
- **任意方向是加權和**：方向取 (2, −3)，斷言中央差商算出來的 (7, −4) 等於
  兩個偏導數的加權和。
- **鏈鎖規則就是矩陣相乘**：另取一個 G，斷言 `J_G · J_F` 逐項等於直接對合成算出來的雅可比，
  並斷言三個矩陣互不相同（否則畫面分不出誰是誰）。
- **行列式**在四個取樣點上都算過，斷言等於 `4‖x‖²`，並斷言四個數字互不相同。
- **面積放大**也驗了：把一個邊長 0.2 的小方塊送過去，斷言像的面積除以原面積等於行列式。

`bounds.py` 抓到 beat 0 的基底標籤與 beat 10 的像跑出上緣。probe 幀抓到 beat 7：
為了讓兩個欄標籤不重疊而把矩陣的行距拉到 1.30，結果一個矩陣看起來變成兩個並排的行向量，
改回 1.10 並縮小標籤才對。

---

## Beat 0 — 搬到實數的 n 維空間 / moving into real n-space
*配音長度：中文 14.4s ／ 英文 14.9s*

**畫面公式**

```
搬到實數的 n 維空間   |   moving into real n-space
ℝ ⁿ               δ ¹ ,  δ ² ,  … ,  δ ⁿ
```

**旁白（繁中）**

> 前兩節的結果從頭到尾沒有用到座標。這一節把它們搬到實數的 n 維空間，那裡有標準基底，於是「偏導數」這個古典的東西才第一次真的出現。

**Narration (EN)**

> Nothing in the last two sections used coordinates. This section moves the results into real n-space, where a standard basis exists, and so the classical object called a partial derivative finally makes its first real appearance.

**動畫**

平面上的標準基底兩支箭頭，加上一圈格點。

## Beat 1 — 定理 9.1：三件事是同一件事 / Theorem 9.1: three names, one thing
*配音長度：中文 15.7s ／ 英文 15.4s*

**畫面公式**

```
定理 9.1：三件事是同一件事   |   Theorem 9.1: three names, one thing
∂ F / ∂ x ⱼ ( a )    =    D δ ʲ F ( a )    =    dF ʲ ₐ ( 1 )
```

**旁白（繁中）**

> 定理 9.1 把三件事對在一起：老式的偏導數、沿第 j 個基底向量的方向導數、第 j 個偏微分。三個只要有一個存在，另外兩個就都存在，而且互相決定。

**Narration (EN)**

> Theorem 9.1 lines three things up: the old fashioned partial derivative, the directional derivative along the jth basis vector, and the jth partial differential. If any one of them exists the other two do, and each determines the others.

**動畫**

三個方框排成三角形：偏導數、沿基底向量的方向導數、偏微分，箭頭繞成一圈。

## Beat 2 — 一維的因子讓偏微分變成一個數 / a one dimensional factor gives a number
*配音長度：中文 14.1s ／ 英文 14.4s*

**畫面公式**

```
一維的因子讓偏微分變成一個數   |   a one dimensional factor gives a number
dF ʲ ₐ ( h )     =     h · ( ∂ F / ∂ x ⱼ ) ( a )
```

**旁白（繁中）**

> 第 j 個偏微分特別簡單，因為第 j 個因子只有一維：它做的事就只是「乘上那個偏導數」。所以在實數的 n 維空間上，偏微分退化成一個數。

**Narration (EN)**

> The jth partial differential is especially simple, because the jth factor is one dimensional: all it does is multiply by that partial derivative. So in real n-space a partial differential collapses into a single number.

**動畫**

左邊一條 h 的實數線，右邊是它的像：同一個偏導數向量的一倍與兩倍。

## Beat 3 — 定理 9.2：偏導數就是骨架 / Theorem 9.2: the partials are the skeleton
*配音長度：中文 15.4s ／ 英文 15.2s*

**畫面公式**

```
定理 9.2：偏導數就是骨架   |   Theorem 9.2: the partials are the skeleton
dF ₐ    ←    { ( ∂ F / ∂ x ⱼ ) ( a ) }        ( j = 1 … n )
```

**旁白（繁中）**

> 定理 9.2：如果 F 在 a 可微，那麼 n 個偏導數全都存在，而且它們排成的那一組就是微分的骨架。這就是「用基底方向把微分讀出來」在座標下的樣子。

**Narration (EN)**

> Theorem 9.2: if F is differentiable at a then all n partial derivatives exist, and the tuple they form is the skeleton of the differential. That is what reading a differential off the basis directions looks like in coordinates.

**動畫**

兩個單行的列向量（兩個偏導數），一支箭頭指向右邊由它們組成的矩陣。

## Beat 4 — 任意方向：分量乘偏導數再求和 / any direction: a weighted sum
*配音長度：中文 19.6s ／ 英文 16.6s*

**畫面公式**

```
任意方向：分量乘偏導數再求和   |   any direction: a weighted sum
D y F ( a )   =   Σ  y ⱼ ( ∂ F / ∂ x ⱼ ) ( a )              ( 7 , − 4 )
```

**旁白（繁中）**

> 於是任意方向的導數，就是把那個方向的各個分量乘上對應的偏導數再加起來。這正是大家熟悉的「梯度點乘方向」，也是為什麼梯度方向的變化最快。畫面上方向取二與負三，算出來是七與負四。

**Narration (EN)**

> The derivative in any direction is the direction's components multiplied by the matching partial derivatives and added. That is the familiar gradient dotted with the direction, and why the gradient's own direction gives the fastest change. On screen, seven and minus four.

**動畫**

一支方向箭頭拆成水平與垂直兩個分量，右邊是加權和算出來的 (7, −4)。

## Beat 5 — 古典記號的一點怪處 / a wrinkle in the classical notation
*配音長度：中文 14.7s ／ 英文 13.4s*

**畫面公式**

```
古典記號的一點怪處   |   a wrinkle in the classical notation
dF ₐ ( x )                    D ⱼ F ( a )
```

**旁白（繁中）**

> 書上在這裡吐槽了古典記號一句：把微分寫成 dF 下標 a 作用在 x 上，讀起來很怪，因為 x 同時是座標的名字。D 下標 j 的 F 這種寫法精確得多。

**Narration (EN)**

> The book takes a swipe at the classical notation here: writing the differential at a applied to x reads badly, since x is also the name of the coordinates. Writing D sub j of F is a good deal more precise.

**動畫**

兩個記號的方框，上面那個被打叉——因為它的 x 同時是座標的名字。

## Beat 6 — 定理 9.3：偏導數連續就夠了 / Theorem 9.3: continuous partials suffice
*配音長度：中文 14.8s ／ 英文 17.0s*

**畫面公式**

```
定理 9.3：偏導數連續就夠了   |   Theorem 9.3: continuous partials suffice
∂ F / ∂ x ⱼ  ∈  C ( A )         ⇒         dF  ∈  C ( A )
```

**旁白（繁中）**

> 定理 9.3 是上一集定理 8.3 的特例：只要所有偏導數在一個開集上存在而且連續，F 就在那裡連續可微。這是實際判斷可微時真正在用的判準。

**Narration (EN)**

> Theorem 9.3 is the previous episode's Theorem 8.3 as a special case: if every partial derivative exists and is continuous on an open set, F is continuously differentiable there. This is the test actually used to decide differentiability.

**動畫**

兩個方框上下排列，一支箭頭往下：偏導數連續推出連續可微。

## Beat 7 — 雅可比矩陣：每一行一個偏導數 / the Jacobian matrix, a partial per column
*配音長度：中文 18.3s ／ 英文 18.1s*

**畫面公式**

```
雅可比矩陣：每一行一個偏導數   |   the Jacobian matrix, a partial per column
t    =    [  ∂ F / ∂ x ₁    …    ∂ F / ∂ x ₙ  ]
```

**旁白（繁中）**

> 如果值域也是實數的 m 維空間，微分就是一個線性映射，它的矩陣就叫雅可比矩陣。要記的是：矩陣的第 j 行，是第 j 個偏導數排成的那個 m 元組——行對應輸入變數，列對應輸出分量。

**Narration (EN)**

> If the range is real m-space as well, the differential is a linear map and its matrix is called the Jacobian matrix. What to remember is that its jth column is the m-tuple of jth partial derivatives: columns answer to input variables, rows to output components.

**動畫**

雅可比矩陣，兩行各自框起來，底下標著它們是哪一個偏導數。

## Beat 8 — 定理 9.4：矩陣元就是偏導數 / Theorem 9.4: entry by entry
*配音長度：中文 14.1s ／ 英文 15.5s*

**畫面公式**

```
定理 9.4：矩陣元就是偏導數   |   Theorem 9.4: entry by entry
t ᵢ ⱼ     =     ( ∂ f ᵢ / ∂ x ⱼ ) ( a )     =     ∂ y ᵢ / ∂ x ⱼ
```

**旁白（繁中）**

> 定理 9.4 把它寫死：第 i 列第 j 行的元素，就是第 i 個分量對第 j 個變數的偏導數。畫面上那個映射在該點的矩陣是二、負一、一、二。

**Narration (EN)**

> Theorem 9.4 nails it down: the entry in row i and column j is the partial derivative of the ith component with respect to the jth variable. For the map on screen, at that point the matrix is two, minus one, one, two.

**動畫**

同一個矩陣，四個元素底下各標著它是哪一個偏導數。

## Beat 9 — 鏈鎖規則就是矩陣相乘 / the chain rule is matrix multiplication
*配音長度：中文 19.8s ／ 英文 18.1s*

**畫面公式**

```
鏈鎖規則就是矩陣相乘   |   the chain rule is matrix multiplication
∂ z ₖ / ∂ x ⱼ     =     Σ ᵢ  ( ∂ z ₖ / ∂ y ᵢ ) ( ∂ y ᵢ / ∂ x ⱼ )
```

**旁白（繁中）**

> 鏈鎖規則寫成矩陣，就是大家背過的那條連鎖公式。它其實只是「線性映射的合成等於矩陣相乘」，記號一換就什麼都不必背了。畫面上兩個雅可比矩陣乘出來的，跟直接對合成算的完全一樣。

**Narration (EN)**

> Written as matrices the chain rule becomes the formula everyone memorised. It is only the statement that composing linear maps is multiplying matrices, so with the right notation nothing is left to memorise. On screen the two Jacobians multiply to the composite's own.

**動畫**

三個矩陣：J_F、J_G、以及它們的乘積，中間是點與等號。

## Beat 10 — 行列式：F 的雅可比 / the determinant: the Jacobian of F
*配音長度：中文 22.5s ／ 英文 18.0s*

**畫面公式**

```
行列式：F 的雅可比   |   the determinant: the Jacobian of F
det J F ( a )     =     4 ( ‖ x ‖ ₂ ) ²
```

**旁白（繁中）**

> 最後，如果 F 從 n 維空間映到自己，雅可比矩陣的行列式就叫 F 的雅可比。畫面上那個映射的雅可比是四乘上向量長度的平方，四個取樣點全部對得上。雅可比不為零，後面會是反函數定理的關鍵。下一集講初等應用。

**Narration (EN)**

> Finally, if F maps n-space to itself, the determinant of the Jacobian matrix is called the Jacobian of F. For the map on screen it is four times the squared length of the vector, and all four samples agree. A nonzero Jacobian is later the key to the inverse function theorem.

**動畫**

藍色的小方塊與它的像（紅色的平行四邊形），右邊是四個取樣點的行列式對照表。

---

## 這一節沒有新的數學

第 7、8 兩節的定理全都不需要座標。這一節做的事是翻譯：把它們寫成偏導數與雅可比矩陣的語言，
好跟古典的多變數微積分接上。所以每一條定理都是前面某一條的特例——
定理 9.3 是定理 8.3、定理 9.1 的第三項是 E39 的定理 7.1。

## 書上對古典記號的評語

原文用了 barbarism 這個字形容 `∂F/∂xⱼ` 這套寫法在這裡造成的混亂：
把微分寫成「dF 下標 a 作用在 x 上」時，`x` 同時是座標的名字，兩個讀法會打架。
`D_j F` 這種寫法把要固定的東西放進下標，精確得多。這一拍就在畫這件事。
