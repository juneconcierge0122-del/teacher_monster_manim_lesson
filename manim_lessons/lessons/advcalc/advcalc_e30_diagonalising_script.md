# advcalc E30 — 第 2 章：把二次型算成對角形

Chapter 2: Computing a Quadratic Form into Diagonal Shape

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 7 節的後段（書頁 113–115）。第 7 節整節沒有習題，第 3 章從書頁 116 開始。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e30_diagonalising.py`（`AdvCalcE30ZH` / `AdvCalcE30EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[30]` / `FORMULAS_ADVCALC[30]`）
- 配音：`manim_lessons/samples/audio_e30/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.04 分（183 秒）／英文 3.22 分（193 秒）

## 這一集的例子是搜出來的

範例 `[[0, 2, 1], [2, 0, −1], [1, −1, 0]]` 不是隨手挑的，是按四個條件搜出來的，每一個條件都對應
旁白裡的一句話：

1. **對角線一開始全是零**，所以 `γ ₁ = α ₁ + α ₂` 那個補救步驟是真的必須用上，不是講講而已；
2. **清完第一列之後右下角那塊還不是對角的**，所以「對剩下那塊重複」真的會跑一次；
3. **過程全程都是整數**，觀眾的注意力不會被分數吃掉；
4. **結果的對角線有正有負**（4、−1、1），符號差不是退化的。

場景檔把這四條全部寫成 `assert`，另外還驗了：每一步都保持對稱、最後確實是對角的、
`Cᵀ T C` 等於那個對角矩陣（也就是整條鏈真的是同一個二次型的合同變換）、以及**每一步的行列式
都沒變**——最後一拍的奇偶性就是靠這一條。

---

## Beat 0 — 歸納證明不告訴你怎麼算 / an existence proof does not tell you how to compute
*配音長度：中文 18.0s ／ 英文 17.2s*

**畫面公式**

```
歸納證明不告訴你怎麼算   |   an existence proof does not tell you how to compute
{ t ᵢⱼ }   →   { β ᵢ }        ω ( β ᵢ , β ⱼ )  =  0   ( i ≠ j )
```

**旁白（繁中）**

> 上一集證明了正交規範基底一定存在，但那是歸納證明，不告訴你怎麼找。這一集給實際的算法，它有個好性質：在最後正規化之前，全程只用加減乘除，不必解任何多項式方程。

**Narration (EN)**

> Last time proved an orthonormal basis exists, but the proof was an induction and does not tell you how to find one. This episode gives the algorithm, and it has a pleasant property: until the final normalization it uses only arithmetic, with no polynomial equations to solve.

**動畫**

左右兩欄：左邊是上一集的存在性證明（一個 ∃ 的方框，三行說明它證得出來但不告訴你怎麼找），右邊是這一集的算法（三行說明它跑得出來、只用加減乘除）。中間一條分隔線。

## Beat 1 — 先求正交，正規化留到最後 / orthogonal first, normalize at the end
*配音長度：中文 15.9s ／ 英文 16.8s*

**畫面公式**

```
先求正交，正規化留到最後   |   orthogonal first, normalize at the end
β ᵢ   →   β ᵢ  /  √ | ω ( β ᵢ , β ᵢ ) |
```

**旁白（繁中）**

> 先把目標降一級：只要正交就好，不同的基底向量互相取零，值是多少先不管。等拿到正交基底，再把每一個除以自己那個值的絕對值開根號，正規化就完成了。

**Narration (EN)**

> First lower the target: settle for an orthogonal basis, distinct basis vectors giving zero against each other, never mind what values they give themselves. Once that is in hand, divide each by the square root of the size of its own value and normalization is done.

**動畫**

左邊是例子做完的對角矩陣（4、−1、1），一個箭頭指到右邊正規化後的 ± 1 對角矩陣，箭頭上寫著除以自己值的平方根。兩張圖用的都是這一集實際算出來的對角線。

## Beat 2 — 先找一個對自己不取零的向量 / first find a vector that does not vanish on itself
*配音長度：中文 18.1s ／ 英文 18.1s*

**畫面公式**

```
先找一個對自己不取零的向量   |   first find a vector that does not vanish on itself
t ᵢᵢ  =  ω ( α ᵢ , α ᵢ )  =  q ( α ᵢ )
```

**旁白（繁中）**

> 第一步是找一個 β，使得 ω 對 β 與 β 不為零。如果矩陣對角線上有一格不是零，那個基底向量直接可以用，因為對角線上的 t ᵢᵢ 就是 q ( α ᵢ )。麻煩的是對角線全是零的情形。

**Narration (EN)**

> The first step is to find a beta with omega of beta and beta nonzero. If some entry on the diagonal is not zero, that basis vector will do, since the diagonal entry t-i-i is just q of alpha-i. The awkward case is a matrix whose diagonal is entirely zeros.

**動畫**

例子的原矩陣，對角線三格高亮，右邊各標著 q ( α ᵢ ) = 0——三格都是零，一個現成的都沒有，這正是挑這個例子的原因。

## Beat 3 — 對角線全是零時的補救 / the repair when the diagonal is all zeros
*配音長度：中文 16.0s ／ 英文 16.7s*

**畫面公式**

```
對角線全是零時的補救   |   the repair when the diagonal is all zeros
t ₁₂ ≠ 0        γ ₁ = α ₁ + α ₂        γ ᵢ = α ᵢ   ( i > 1 )
```

**旁白（繁中）**

> 這時只要 ω 不是零形式，就有某個非對角線的格子不是零，假設是第一列第二行。取 γ ₁ 等於 α ₁ 加 α ₂，其餘不動；這樣還是一組基底，因為這個換法做得回去。

**Narration (EN)**

> There, as long as omega is not the zero form, some off-diagonal entry is nonzero, say the one in row one, column two. Take gamma one to be alpha one plus alpha two and leave the others alone. That is still a basis, because the swap can be undone.

**動畫**

左邊是那一步的換基底矩陣 e，只有一格被動到。右邊畫出為什麼有效：α ₁ 與 α ₂ 兩支箭頭加上對角線的 γ ₁，配一句「即使 q ( α ₁ ) 與 q ( α ₂ ) 都是零，q ( γ ₁ ) 也不是零」。

## Beat 4 — 左上角那一格變成 2 t ₁₂ / the corner becomes twice t-1-2
*配音長度：中文 16.2s ／ 英文 21.9s*

**畫面公式**

```
左上角那一格變成 2 t ₁₂   |   the corner becomes twice t-1-2
s ₁₁  =  t ₁₁ + 2 t ₁₂ + t ₂₂  =  2 t ₁₂  ≠  0
```

**旁白（繁中）**

> 新矩陣左上角那一格是 t ₁₁ 加兩倍 t ₁₂ 再加 t ₂₂；對角線全零時它就等於兩倍 t ₁₂，不是零。影片的例子正好是這種矩陣，所以這一步真的必須用上，做完左上角變成四。

**Narration (EN)**

> The new top-left entry is t-1-1 plus twice t-1-2 plus t-2-2, which on an all-zero diagonal is just twice t-1-2, and not zero. The example here is a matrix of exactly that kind, so the step is forced rather than described, and it leaves four in the corner.

**動畫**

兩個矩陣並排：左邊原矩陣的四格高亮（t ₁₁、t ₁₂、t ₂₁、t ₂₂），右邊做完之後左上角變成 4。底下寫出 s ₁₁ = 0 + 2·2 + 0 = 4 這個算式，數字全是從矩陣讀出來的。

## Beat 5 — 把其餘向量推進核空間 / push the other vectors into the null space
*配音長度：中文 15.2s ／ 英文 16.8s*

**畫面公式**

```
把其餘向量推進核空間   |   push the other vectors into the null space
γ ⱼ  →  γ ⱼ + c γ ₁        ω ( γ ⱼ + c γ ₁ , γ ₁ )  =  0
```

**旁白（繁中）**

> 第二步：把其餘的基底向量推進「拿 ξ 去配 γ ₁」這個泛函的核空間。把 γ ⱼ 換成 γ ⱼ 加 c 倍的 γ ₁，要求它跟 γ ₁ 配出來是零，這樣它就落在那個核空間裡。

**Narration (EN)**

> Second step: push the other basis vectors into the null space of the functional that pairs xi against gamma one. Replace gamma j by gamma j plus c times gamma one, and ask for it to pair with gamma one to zero, which puts it in that null space.

**動畫**

上方是 ω ( γ ⱼ + c γ ₁ , γ ₁ ) = s ₁ⱼ + c s ₁₁ = 0，底下兩行把例子的 j = 2 與 j = 3 各解一次，c 的值是算出來的。

## Beat 6 — 第一列與第一行清乾淨 / the first row and column, cleared
*配音長度：中文 14.7s ／ 英文 17.7s*

**畫面公式**

```
第一列與第一行清乾淨   |   the first row and column, cleared
c  =  −  s ₁ⱼ / s ₁₁        r ₁ⱼ  =  r ⱼ₁  =  0   ( j > 1 )
```

**旁白（繁中）**

> 解出來 c 就是負的 s ₁ⱼ 除以 s ₁₁——剛才那一步就是為了讓這個除法合法。換完之後還是基底，而新矩陣的第一列與第一行，除了左上角那格全變成零。

**Narration (EN)**

> Solving gives c as minus s-1-j over s-1-1, and the first step is what made that division legal. The list still spans the same space, so it is still a basis, and the first row and column of the new matrix are zero apart from the corner.

**動畫**

兩個矩陣並排，第一列與第一行（左上角除外）在右邊那個變成零，這些格子高亮。

## Beat 7 — 對剩下那塊重複 / repeat on what is left
*配音長度：中文 14.9s ／ 英文 13.2s*

**畫面公式**

```
對剩下那塊重複   |   repeat on what is left
{ r ᵢⱼ  :  2 ≤ i , j ≤ n }
```

**旁白（繁中）**

> 剩下的是一個少一維的問題：對右下角那塊子矩陣重複同一件事，一直做到底。過程有點長，但每一步都只是加減乘除，這正是這個方法真正的價值。

**Narration (EN)**

> What is left is the same problem one dimension smaller: repeat on the block in the bottom right, and keep going. The process is long, but every step is a rational operation, and that is the real value of the method.

**動畫**

做完第一輪的矩陣，右下角那塊 2×2 用一組額外的括號框起來並高亮：剩下的是同一個問題，少一維。這個例子的那一塊還不是對角的，所以遞迴真的會跑一次。

## Beat 8 — 例子走到底 / the example, run to the end
*配音長度：中文 17.2s ／ 英文 16.7s*

**畫面公式**

```
例子走到底   |   the example, run to the end
( 4 , − 1 , 1 )        p = 2  ,  n = 1  ,  σ = 1
```

**旁白（繁中）**

> 把例子走到底，得到一個對角矩陣，對角線是四、負一、一，所以 p 是二、n 是一，符號差是一。要正規化的話，把第一個基底向量除以二就好，因為四開根號是二。

**Narration (EN)**

> Run the example to the end and a diagonal matrix comes out: four, minus one, one. So p is two, n is one and the signature is one. To normalize, divide the first basis vector by two, the square root of four, and that is all.

**動畫**

四個矩陣的鏈，箭頭上標著每一步做了什麼。底下三行是算法真正交出來的東西：三個 β 用原本的 α 表示，由累積的換基底矩陣讀出來。

## Beat 9 — 列與行一起做 / rows and columns at the same time
*配音長度：中文 18.8s ／ 英文 18.5s*

**畫面公式**

```
列與行一起做   |   rows and columns at the same time
s  =  ( a* ) ⁻¹ · t · a ⁻¹        s  =  eᵀ · t · e
```

**旁白（繁中）**

> 這些步驟看起來很像列運算，但有個差別：因為 T 是從 V 到 V*，定義域與值域的基底同時在換，每一步等於同時左乘與右乘一個初等矩陣——列與行一起做。要維持對稱，本來也只能這樣。

**Narration (EN)**

> These steps look like row reduction with one difference. Since T runs from V to V star, the bases of domain and range change together, so each step multiplies by an elementary matrix on both sides: rows and columns at once, which is the only way a symmetric matrix stays symmetric.

**動畫**

eᵀ · a · e = a′ 四個矩陣並排乘出來，左邊那個做列運算、右邊那個做行運算，而且是同一個 e。

## Beat 10 — 奇偶性與二維的捷徑 / parity, and the shortcut in two dimensions
*配音長度：中文 17.6s ／ 英文 19.9s*

**畫面公式**

```
奇偶性與二維的捷徑   |   parity, and the shortcut in two dimensions
Δ ( s )  =  [ Δ ( e ) ] ²  Δ ( t )        t ₁₁ t ₂₂ − t ₁₂²
```

**旁白（繁中）**

> 最後一件事：換基底時新矩陣的行列式等於舊的乘上一個平方數，所以正負號不會變，二次型有奇偶性。二維時這讓你不必正交化就讀出符號差——只要看 t ₁₁ t ₂₂ 減 t ₁₂ 平方的正負。

**Narration (EN)**

> One last thing. Changing basis multiplies the determinant by a square, so its sign never changes and a quadratic form has a parity. In two dimensions that lets you read the signature without orthonormalizing: look at the sign of t-1-1 t-2-2 minus t-1-2 squared.

**動畫**

四個矩陣的鏈重畫一次，每一個底下標著自己的行列式——四個都是 −4，奇偶性直接看得見。底下寫出二維的捷徑：t ₁₁ t ₂₂ − t ₁₂² = −4 < 0，所以符號差是 0。
