# advcalc E75 — 第 6 章：整體解與 n 階方程

Chapter 6: Global Solutions and the nth-Order Equation

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 1 節「基本定理」的**後半**（書頁 269–272），接 E74 的定理 1.2。**第 1 節到此結束**，習題 1.1–1.13 在 272–273（依 PLAYBOOK 第 8 節不做解答）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e75_global.py`（`AdvCalcE75ZH` / `AdvCalcE75EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[75]` / `FORMULAS_ADVCALC[75]`）
- 配音：`manim_lessons/samples/audio_e75/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 207.6 秒（3:27）／英文 200.6 秒（3:20）
- YouTube（私人）：中文 https://youtu.be/4w53FSmGBns ／英文 https://youtu.be/deHfmDoGPrE

## 這半節在做什麼

**局部解可以拼。** 跑到一條局部解的尾端附近再取一個新的局部解，引理 1.1 保證兩者在交集上相等，
而新的那條伸得更遠。把「一直拼下去」講精確就是取聯集：

```
𝔉  =  { g  :  g ′ = F ( t , g )  ,  g ( t ₀ ) = α ₀ }              f   =   ∪ 𝔉
```

**函數是有序對的集合**，所以聯集有意義；而引理 1.1 正好保證它還是個函數。
聯集自己是解（任一點附近都與某個 g 相同），而且包含每一條解——**定理 1.3**：極大解存在且唯一。

**極大解一般撞上 A 的邊界**，所以 J ⊊ I。E74 的例子正是如此：I = ℝ 而 J = ( −π/2 , π/2 )。

**定理 1.4** 給出 J = I 的條件：**A = W**，而且有連續的 c 使

```
‖ F ( t , α ₁ ) − F ( t , α ₂ ) ‖    ≤    c ( t ) ‖ α ₁ − α ₂ ‖       ∀ α ₁ , α ₂ ∈ W
```

**重點在「任兩點」**——要對 W 裡所有點成立，不是只在附近。

**證明的關鍵一步**是把定理 1.1 的半徑上限改寫：

```
r / ( m + r c )    =    1 / ( c + m / r )       ⟶       1 / c
```

分母裡只有第二項跟 r 有關，而 **A = W 讓 r 沒有上限**，所以上限爬向 1/c。
這是整個證明唯一用到 A = W 的地方。接著挑 t₁ 使 b − t₁ < 1/c，就能讓 t₁ + δ 超過 b，與極大性矛盾。

**n 階方程**用 ψ : f ↦ ⟨ f , f ′ , … , f ⁽ⁿ⁻¹⁾ ⟩ 化成一階系統，前面每條都是
「這個座標的導數等於下一個座標」，只有最後一條帶 G。**定理 1.5** 因此直接從 1.1、1.2 落下來。

## 這一集用的例子

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 兩個解都對 | 數值微分比對方程 | 誤差 ≤ 1e-5 |
| 拼接的右端點 | 定理 1.1 自己的 δ，連六步 | 0.2500, 0.4385, 0.5959, 0.7297, 0.8443, 0.9426 |
| 拼接永遠過不了 π/2 | 每一步的右端點 | 全部 < 1.5708 |
| 每段一段比一段短 | δ ₖ | 0.2500, 0.1985, 0.1653, 0.1404 |
| t + x 的 Lipschitz 商 | 四組點 | 全部 = 1.0000 |
| 1 + x² 的 Lipschitz 商 | 同四組點 | 1.5, 5.0, 19.0, 199.0 |
| 半徑上限爬向 1/c | r = 1 到 10⁴ | 0.126758, 0.592099, 0.935549, 0.993158, 0.999312 |
| 兩種寫法相同 | r/(m+rc) 對 1/(c+m/r) | 差 < 1e-12 |
| 矛盾的數字 | b − t₁ = 0.60 < 1/c，t₁+δ = 3.20 | 超出 0.20 |
| 旋轉場的解是單位圓 | sin² + cos² | = 1 |
| 旋轉場保距，所以 c = 1 | 三組點的商 | 全部 = 1.0000 |

**那個 1/c 是這一集的樞紐。** 定理 1.4 的證明看起來技術，其實只有一件事：
把上限寫成 1/(c + m/r) 之後，A = W 就把 m/r 壓成零。

## 這一輪抓到的錯

- **`if False else` 寫進場景檔。** 第 8 拍的表格一時寫成兩段再用 `if False else` 挑一段——
  這正是那條 grep 在抓的東西，而且是我自己加的。寫完就 grep 到，改成單一呼叫。
  同一輪還清掉圓那一行的死算式（`0.02 * k * math.tau / 1.0 * 0 +`）。
- **ox 被當成面板左緣，可是資料跑負的。** 第 1、2 拍的定義域與曲線都從負的 t 開始，
  ox 卻當成左緣用，於是 x 掉到 −9.14。改成「ox 就是 t = 0」並在註解裡寫明。
- **tan 直接畫到 y = ±5。** 第 3、5 拍照 t 的範圍畫 tan，沒算過值域。**按 t 裁、不要按值裁**——
  把值 clamp 住會變成平台加懸崖（PLAYBOOK 第 5 節那條）。
- **拋物線根本沒鑽出灰錐。** 第 4 拍要說「斜率有界的線罩得住、拋物線罩不住」，
  可是 x² 只在 |x| > c 之後才超過 c|x|，而我原本的視窗只到 1.05、錐的斜率卻取 3.4——
  畫出來兩條都乖乖待在錐裡，正好把要說的反例畫成了正例。視窗改到 ±3.2、錐斜率改成 2，才看得到它鑽出去。
- **相平面上的初始點標錯位置。** 第 9 拍的初始條件是 x(0) = 0、x′(0) = 1，
  所以相點 ⟨ α ₁ , α ₂ ⟩ = ⟨ x , x ′ ⟩ 在圓的**頂端** (0, 1)；我標在右側 (1, 0)，
  與同一張圖的表格自相矛盾。probe 幀抓到。
- **表格列裡混中文** 三處（langscan），**圖例與邊框壓到註腳**若干處（bounds / collide）。

## 十一拍

### 第 1 拍 — 把局部解拼起來 / patching local solutions

公式列：

```
g ₁  =  g ₂     |     J ₁ ∩ J ₂                  J ₁ ∪ J ₂
```

中文旁白：上一集的定理 1.1 只給出局部解。可是跑到一條局部解的尾端附近，再取一個新的局部解，引理 1.1 保證兩者在定義域的交集上相等，而新的那條往前伸得更遠。兩段就拼成一條活得更久的解，一直拼下去。

English: Theorem 1.1 last episode gave only local solutions. But run to near the end of one, take a fresh local solution there, and Lemma 1.1 guarantees the two agree on the overlap while the new one reaches further. The two patch into a longer solution, and so on.

### 第 2 拍 — 精確的做法：取聯集 / made precise: a union

公式列：

```
𝔉  =  { g  :  g ′ = F ( t , g )  ,  g ( t ₀ ) = α ₀ }          f  =  ∪ 𝔉
```

中文旁白：要把「一直拼下去」講精確，就取聯集。設 𝔉 是所有通過那一點的解。函數本來就是有序對的集合，所以聯集有意義；而引理 1.1 正好保證這個聯集還是個函數——同一個 t 不會被配到兩個不同的值。

English: To make patching precise, take a union. Let the family be all solutions through the point. A function is a set of ordered pairs, so the union means something, and Lemma 1.1 is exactly what guarantees the union is still a function: no t gets two values.

### 第 3 拍 — 定理 1.3：極大解 / theorem 1.3: the maximal solution

公式列：

```
f ′ ( t )  =  F ( t , f ( t ) )               g  ⊂  f       ∀ g ∈ 𝔉
```

中文旁白：這個聯集自己就是解：定義域裡任一點附近，它都與 𝔉 裡某一條相同，所以可微而且滿足方程。而每一條解都被它包含。定理 1.3：過 I 乘 A 裡的每一點，都有唯一一條決定好的極大解。

English: That union is itself a solution: near any point of its domain it agrees with one member of the family, so it is differentiable and satisfies the equation. And it contains every solution. Theorem 1.3: through each point there is a unique maximal solution.

### 第 4 拍 — 極大解一般撞上 A 的邊界 / it generally runs into the boundary

公式列：

```
J  ⊊  I                J  =  ( − π / 2 ,  π / 2 )
```

中文旁白：極大解一般會撞上 A 的邊界，所以定義域 J 真包含在 I 裡。上一集那個例子正是如此：I 是整條實數線，而解 tan t 只活在正負 π 的一半之間，兩邊都被漸近線卡住。

English: A maximal solution generally runs into the boundary of A, so its domain sits properly inside I. Last episode's example is exactly that: I is the whole real line while the solution tan t lives only between minus and plus half of pi, walled in by asymptotes.

### 第 5 拍 — 定理 1.4 / theorem 1.4

公式列：

```
‖ F ( t , α ₁ ) − F ( t , α ₂ ) ‖  ≤  c ( t ) ‖ α ₁ − α ₂ ‖       ⇒     J  =  I
```

中文旁白：定理 1.4 給出 J 等於 I 的條件：A 是整個 W，F 連續，而且存在連續函數 c，使 F 在任兩點的差的長度不超過 c t 乘上兩點的距離——注意這裡要對 W 裡所有的點成立，不只是附近。

English: Theorem 1.4 says when the domain is all of I: A is the whole of W, F is continuous, and some continuous function c bounds the difference of the values of F by c of t times the distance. This must hold for every pair of points in W, not just nearby ones.

### 第 6 拍 — 兩個例子只差這一條 / two examples, one difference

公式列：

```
c ( t )  ≡  1                  | ξ + η |   →   ∞
```

中文旁白：兩個例子的差別只在這一條。x 的導數等於 t 加 x，商恆等於一，c 可以取常數一；x 的導數等於一加 x 平方，商是 ξ 加 η 的絕對值，沒有任何 c 攔得住。前者活在整條實數線上，後者在 π 的一半就沒了。

English: The two examples differ in exactly that. For the derivative of x equal to t plus x the quotient is always one, so c is constant. For one plus x squared it is the absolute value of xi plus eta, and no c holds it down. The first lives on the whole line, the second dies at half of pi.

### 第 7 拍 — 證明（一）：取緊的閉包 / proof, one: a compact closure

公式列：

```
b  <  sup I           L ‾  ⊂  I           c  =  max { c ( t )  :  t ∈ L ‾ }
```

中文旁白：證明用反證。設極大解 g 的右端點 b 還在 I 裡面。取一個有限開區間 L 包含 b，而且它的閉包落在 I 裡。閉包是緊的，所以連續的 c 在上面有最大值，把那個最大值叫做 c。

English: The proof is by contradiction. Suppose the maximal solution has right endpoint b still inside I. Choose a finite open interval containing b whose closure lies in I. That closure is compact, so the continuous c attains a maximum on it; call it c.

### 第 8 拍 — 證明（二）：r 沒有上限 / proof, two: no ceiling on r

公式列：

```
r / ( m + r c )   =   1 / ( c + m / r )       ⟶       1 / c
```

中文旁白：關鍵在 A 是整個 W。定理 1.1 給的區間半徑上限是 r 除以 m 加 r c，也就是一除以 c 加 m 除以 r。因為球可以取多大都行，r 沒有上限，這個上限就一路爬向一除以 c。

English: The point is that A is the whole of W. The radius bound from Theorem 1.1 is r over m plus r c, which is one over c plus m over r. Since the ball may be taken as large as we like, r has no ceiling and the bound climbs all the way to one over c.

### 第 9 拍 — 證明（三）：矛盾 / proof, three: the contradiction

公式列：

```
b − t ₁  <  1 / c            t ₁ + δ  >  b            t ₁ + δ  ≤  b
```

中文旁白：於是挑 t 一使 b 減 t 一小於一除以 c，就能取到 δ 讓 t 一加 δ 超過 b。可是通過那一點的極大解包含 g，所以必須 t 一加 δ 不超過 b。矛盾，所以 b 不可能在 I 裡面。

English: So pick a point with b minus it below one over c, and delta can be chosen to carry past b. But the maximal solution through that point contains the original, so the reach must be at most b. That is a contradiction, so b cannot lie inside I.

### 第 10 拍 — n 階方程化成一階系統 / the nth-order equation as a system

公式列：

```
d α ᵢ / d t  =  α ᵢ ₊ ₁                d α ₙ / d t  =  G ( t , α )
```

中文旁白：最後是 n 階方程。用 ψ 把 f 送到 f 與它的前 n 減一階導數，方程就寫成 f 的 n 階導數等於 G 帶入 t 與 ψ f。化成一階系統的辦法很老：前面幾條是每個 α 的導數等於下一個 α，最後一條才是 G。

English: Last, the nth-order equation. Send f to itself together with its first n minus one derivatives, and the equation reads: the nth derivative of f is G at t and that tuple. The reduction to a first-order system is ancient: each derivative is the next coordinate.

### 第 11 拍 — 定理 1.5，與第 1 節的結束 / theorem 1.5, and the end of section 1

公式列：

```
∃ !  f : J → W                 ψ f ( t ₀ )  =  β
```

中文旁白：這樣得到的 F 顯然局部一致 Lipschitz，所以定理 1.1 與 1.2 直接給出 n 階方程的存在唯一，這就是定理 1.5。極大解由定理 1.3 給；若 G 的 Lipschitz 界連續而且 A 是 W 的 n 次冪，定理 1.4 就給出整個 I。

English: The F this produces is plainly locally uniformly Lipschitz, so Theorems 1.1 and 1.2 hand over existence and uniqueness for the nth-order equation, which is Theorem 1.5. Theorem 1.3 gives the maximal solution, and Theorem 1.4 gives all of I when the bound is continuous.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | tan t 加四段彩色的局部解，每段下方一個括號標出它的定義域；右表列出 t ₖ、δ ₖ 與右端點，δ 一段比一段短而右端點一路往右 |
| 2 | 𝔉 裡四個定義域疊成四條橫線，全都含 t ₀，最底下橘線是它們的聯集 |
| 3 | 極大解畫粗，兩條 𝔉 裡的解畫更粗疊在上面——沒有一條伸出橘線之外 |
| 4 | tan t 與 ±π/2 兩道紅牆；下面橘線是 J、灰線是 I，橘線明顯短 |
| 5 | 左右兩塊：t + x 的斜線待在灰錐裡，1 + x ² 的拋物線鑽出去（打叉）。錐的兩條邊是 ± c 乘 x 的絕對值 |
| 6 | e ᵗ − t − 1 與 tan t 同框；紅線在 π/2 的虛線前陡起來，藍線一路往右 |
| 7 | I、J、L ‾ 三條線與 b 的位置，上面一條 c ( t ) 的曲線——緊性把它換成一個數 |
| 8 | 半徑上限對 r 的曲線（r 取對數刻度）爬向 1/c 的虛線，永遠碰不到 |
| 9 | J 的右端點 b 與青色那段 t ₁ 到 t ₁+δ，青段伸過 b 並被打叉 |
| 10 | 單位圓加八支切向的場箭頭；初始點標在圓頂 (0, 1)，因為 ⟨ α ₁ , α ₂ ⟩ = ⟨ x , x ′ ⟩ |
| 11 | sin t 一路畫到右邊界再加一支箭頭（沒有牆）；右表把 1.1、1.2、1.3、1.4 各給出什麼列成四列 |
