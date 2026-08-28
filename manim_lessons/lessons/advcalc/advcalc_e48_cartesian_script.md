# advcalc E48 — 第 3 章：隱函數定理的笛卡兒形式

Chapter 3: The Cartesian Forms

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 11 節「隱函數定理」的後段——定理 11.4 與 11.5 的笛卡兒形式（書頁 167–169）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e48_cartesian.py`（`AdvCalcE48ZH` / `AdvCalcE48EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[48]` / `FORMULAS_ADVCALC[48]`）
- 配音：`manim_lessons/samples/audio_e48/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.00 分（180 秒）／英文 2.97 分（178 秒）

## 沒有新的數學，只有翻譯——以及兩個解不出來的例子

定理 11.4 與 11.5 是把前兩集的反映射定理與隱函數定理寫成座標的樣子：
「微分可逆」變成「雅可比行列式不為零」，結論的「唯一的連續可微映射」
變成「唯一的一組實值函數」。這一集的價值不在定理本身，而在兩個例子——
它們都滿足假設，所以解一定存在、唯一而且連續可微，可是誰也寫不出公式。

- **定理 11.4 的例子**：`G(y) = (y₁³ + y₂, y₁ + y₂³)`。斷言在 b = (1, 1) 的雅可比矩陣是
  `[[3, 1], [1, 3]]`、行列式是 8。然後用牛頓法把局部反函數逼出來：
  斷言它從 a = (2, 2) 回到 (1, 1)，斷言在另外兩個取樣點上代回去確實還原，
  並斷言它的雅可比矩陣等於原矩陣的反矩陣。
- **可是寫不出來**：消掉 `y₂` 之後是 `(x₁ − y₁³)³ + y₁ − x₂ = 0`，`y₁` 的九次方程。
  這條式子本身也用斷言驗過（見下面「一次差點溜過去的錯」）。
- **定理 11.5 的例子**：`x₁² + y₁y₂ − 3 = 0`、`x₂ + y₁⁵ − y₂ = 0`，兩個方程、四個變數。
  斷言取樣點上兩式都成立，斷言只對兩個 `y` 取的行列式是 −7，
  再用公式 `dFₐ = −(dG²)⁻¹ ∘ dG¹` 算出微分，
  與數值解出來的隱函數的雅可比逐項比對。消元之後是 `y₁` 的六次方程，一樣寫不出來。

## 一次差點溜過去的錯

第 5 拍那條消元後的方程，第一版把兩個座標寫反了，成了
`(x₂ − y₁³)³ + y₁³ − x₁ = 0`。麻煩的地方是：在畫面用的那個取樣點 (1, 1) 上，
錯的版本剛好也等於零——因為那個映射對兩個座標對稱。
換一個點 (1.1, 0.9) 才露餡（差了 0.78）。現在模組裡有一條斷言，在三個點上檢查那條式子。

同一輪還修掉一句事實錯誤：旁白原本說「第 3 章到此結束」，
但第 3 章還有第 12 到 17 節（子流形與 Lagrange 乘子、函數相依性、均勻連續、
變分法、二階微分、Taylor 公式）。改成「第 11 節到此結束」。

`bounds.py`／`collide.py` 都是零，probe 幀又抓到三處：beat 4 的兩個座標十字並排糊在一起、
連接它們的箭頭因為端點算錯只有 0.1 單位長（畫面上看不見）、
以及表格最後一列與底下的說明擠在一起；beat 7 框住 y 區塊的紅框把最後一行的標籤切掉，
改成在底下畫一個紅色的括弧；beat 8 的矩陣括號頂到上面那個方程的框。

---

## Beat 0 — 翻成座標的語言 / translated into coordinates
*配音長度：中文 17.1s ／ 英文 17.3s*

**畫面公式**

```
翻成座標的語言   |   translated into coordinates
V , W , X                 →                 ℝ ⁿ ,  ℝ ᵐ
```

**旁白（繁中）**

> 前兩集的定理都是用「向量空間加上微分」寫的，乾淨，但實際要用的時候看到的是一堆方程式。這一集把它們翻成座標的語言，也就是大家在多變數微積分課本裡看到的樣子。

**Narration (EN)**

> The last two episodes stated their theorems with vector spaces and differentials, which is clean, but what one meets in practice is a pile of equations. This episode translates them into coordinates, into the form found in any multivariable calculus text.

**動畫**

左邊上下兩個方塊：V, W, X 與 ℝⁿ, ℝᵐ，中間一支往下的箭頭；
右邊對應寫出 dF, dG 與 ∂(…)/∂(…)。右側說明內容一樣，只是換一種寫法。

## Beat 1 — 定理 11.4 的條件 / the condition in Theorem 11.4
*配音長度：中文 14.4s ／ 英文 15.9s*

**畫面公式**

```
定理 11.4 的條件   |   the condition in Theorem 11.4
∂ ( G ₁ , … , G ₙ ) / ∂ ( y ₁ , … , y ₙ ) ( b )      ≠      0
```

**旁白（繁中）**

> 定理 11.4 是反映射定理的笛卡兒形式。給 n 個連續可微的實值函數，變數也是 n 個，唯一的條件是：那個 n 階的雅可比行列式在該點不等於零。

**Narration (EN)**

> Theorem 11.4 is the Cartesian form of the inverse mapping theorem. Given n continuously differentiable real valued functions of n variables, the only condition is that the n by n Jacobian determinant does not vanish at the point.

**動畫**

左邊一個加框的行列式條件，下面是一個 2×2 的偏導數矩陣（符號寫成 ∂G₁/∂y₁ 等）。
右側說明唯一的條件是行列式不為零。

## Beat 2 — 結論：唯一的一組解 / the conclusion: a unique tuple
*配音長度：中文 15.7s ／ 英文 15.4s*

**畫面公式**

```
結論：唯一的一組解   |   the conclusion: a unique tuple
∃ !  F  ∈  C ¹ ( M )                G ( F ( x ) )   =   x
```

**旁白（繁中）**

> 結論是：那一點的像附近有一顆球，球上存在唯一一組連續可微的實值函數，把它們代回去恰好還原成原來的變數。這就是「局部反函數」寫成座標的樣子。

**Narration (EN)**

> The conclusion: near the image of that point there is a ball carrying a unique n-tuple of continuously differentiable real valued functions which, substituted back, return the original variables. That is a local inverse written in coordinates.

**動畫**

左邊三行：∃! F = ⟨F₁, …, Fₙ⟩、F ∈ C¹(M)、G(F(x)) = x。
右側說明唯一仍然是局部的。

## Beat 3 — 例子：行列式是 8 / an example: the determinant is eight
*配音長度：中文 18.1s ／ 英文 18.0s*

**畫面公式**

```
例子：行列式是 8   |   an example: the determinant is eight
G ( y )  =  ⟨ y ₁ ³ + y ₂ ,  y ₁ + y ₂ ³ ⟩                det  =  8
```

**旁白（繁中）**

> 看一個例子。兩個三次的方程，在 1 與 1 那一點，雅可比矩陣是三、一、一、三，行列式是八，不等於零。所以定理適用，那一點的像 2 與 2 附近就有唯一的局部反函數。

**Narration (EN)**

> Here is an example. Two cubic equations; at the point one and one the Jacobian matrix reads three, one, one, three, with determinant eight. Not zero, so the theorem applies and a unique local inverse exists near the image, the point two and two.

**動畫**

左邊印出 G 的定義，下面是雅可比矩陣與 det = 8，旁邊標出 b 與 a。
右側說明兩個三次的方程在那一點行列式不為零。

## Beat 4 — 反函數真的找得出來 / the inverse really can be found
*配音長度：中文 14.8s ／ 英文 14.4s*

**畫面公式**

```
反函數真的找得出來   |   the inverse really can be found
F ( 2 , 2 )  =  ⟨ 1 , 1 ⟩                dF ₐ  =  ( dG ᵦ ) ⁻¹
```

**旁白（繁中）**

> 程式用牛頓法把那個局部反函數真的找出來了，代回去確認確實還原成原來的變數，而且它的雅可比矩陣正好是原矩陣的反矩陣，跟前一集那條式子相符。

**Narration (EN)**

> Newton's method finds that local inverse here, substituting back confirms it returns the original variables, and its Jacobian matrix comes out as the inverse of the original matrix, agreeing with the previous episode's formula.

**動畫**

左右各一個加框的座標平面（分別標 x 與 F(x)），中間一支標著 F 的箭頭；
兩組取樣點用同一個顏色在兩邊各打一點。右側是牛頓法算出來的對照表。

## Beat 5 — 可是寫不出公式 / but no formula can be written
*配音長度：中文 18.3s ／ 英文 16.9s*

**畫面公式**

```
可是寫不出公式   |   but no formula can be written
( x ₁ − y ₁ ³ ) ³   +   y ₁   −   x ₂    =    0
```

**旁白（繁中）**

> 可是如果想把反函數寫成公式，就要消元。消完之後是一個九次方程，一般沒有根式解。這正是定理的價值：它保證解存在而且連續可微，卻完全不告訴你怎麼把它寫出來。

**Narration (EN)**

> But writing the inverse as a formula means eliminating a variable, and what is left is a polynomial of degree nine, with no solution by radicals in general. That is the value of the theorem: it promises a solution exists and is smooth without saying how to write it.

**動畫**

左邊一個加框的消元方程 (x₁ − y₁³)³ + y₁ − x₂ = 0，下面是 y₁⁹ + … = 0。
右側說明消完是九次方程，一般沒有根式解。

## Beat 6 — 定理 11.5：n + m 個變數 / Theorem 11.5: n plus m variables
*配音長度：中文 15.9s ／ 英文 16.1s*

**畫面公式**

```
定理 11.5：n + m 個變數   |   Theorem 11.5: n plus m variables
G ᵢ ( x ₁ , … , x ₙ ,  y ₁ , … , y ₘ )  =  0            i = 1 , … , m
```

**旁白（繁中）**

> 定理 11.5 是隱函數定理的笛卡兒形式。這次有 m 個方程，但變數有 n 加 m 個：n 個是自由的，m 個是要解出來的，而結論是那 m 個可以寫成前面 n 個的函數。

**Narration (EN)**

> Theorem 11.5 is the Cartesian form of the implicit function theorem. Now there are m equations but n plus m variables: n free and m to be solved for, and the conclusion is that those m become functions of the first n.

**動畫**

左邊兩個方塊分開自由變數 x₁…xₙ 與待解變數 y₁…y_m，下面是 Gᵢ(x, y) = 0。
右側說明 m 個方程剛好配 m 個未知數。

## Beat 7 — 行列式只對被解的變數取 / the determinant covers only the solved variables
*配音長度：中文 15.2s ／ 英文 14.5s*

**畫面公式**

```
行列式只對被解的變數取   |   the determinant covers only the solved variables
∂ ( G ₁ , … , G ₘ ) / ∂ ( y ₁ , … , y ₘ ) ( a , b )      ≠      0
```

**旁白（繁中）**

> 關鍵在於行列式只對「要解出來的那 m 個變數」取，取出來的是一個 m 階的方陣。這是最容易記錯的一點——不是對全部變數取，而是只對被解掉的那一組取。

**Narration (EN)**

> The point is that the determinant is taken only over the m variables being solved for, giving an m by m matrix. This is the easiest thing to get wrong: not over all the variables, but only over the ones being eliminated.

**動畫**

左邊一個 2×4 的偏導數矩陣，屬於 y 的那兩行下面畫一個紅色的括弧並標註。
右側說明行列式只取那一塊，這是最容易記錯的一點。

## Beat 8 — 例子：行列式是 −7 / an example: the determinant is minus seven
*配音長度：中文 17.1s ／ 英文 15.6s*

**畫面公式**

```
例子：行列式是 −7   |   an example: the determinant is minus seven
x ₁ ² + y ₁ y ₂ − 3 = 0                x ₂ + y ₁ ⁵ − y ₂ = 0
```

**旁白（繁中）**

> 例子是兩個方程、四個變數，其中兩個是自由變數、兩個要解出來。在指定的那一點，對兩個 y 取的雅可比矩陣是二、一、五、負一，行列式是負七，不等於零。

**Narration (EN)**

> The example is two equations in four variables, two of them free and two to be solved for. At the chosen point the Jacobian matrix in the two y variables reads two, one, five, minus one, with determinant minus seven.

**動畫**

左邊兩條加框的方程，下面是對兩個 y 取的雅可比矩陣與 det = −7。
右側說明兩個方程、四個變數，在指定的點上兩式都成立。

## Beat 9 — 消元之後是六次方程 / eliminating leaves degree six
*配音長度：中文 14.1s ／ 英文 17.4s*

**畫面公式**

```
消元之後是六次方程   |   eliminating leaves degree six
det  =  − 7                y ₁ ⁶  +  x ₂ y ₁  +  x ₁ ² − 3  =  0
```

**旁白（繁中）**

> 想消元的話，第二式解出 y 二代進第一式，得到一個六次方程。六次一般解不出來，可是定理已經保證解存在、唯一，而且連續可微。

**Narration (EN)**

> Eliminating means solving the second equation for the second y and substituting, which leaves a polynomial of degree six. Degree six has no general solution, yet the theorem already promises the solution exists, is unique, and is continuously differentiable.

**動畫**

左邊三行消元：第二式解出 y₂、代進第一式、得到 y₁⁶ + x₂y₁ + x₁² − 3 = 0。
右側說明六次一般解不出來，可是定理已經保證解存在。

## Beat 10 — 微分還是算得出來 / the differential is still computable
*配音長度：中文 19.4s ／ 英文 16.7s*

**畫面公式**

```
微分還是算得出來   |   the differential is still computable
dF ₐ   =   − ( dG ² ) ⁻¹ ∘ dG ¹
```

**旁白（繁中）**

> 而且微分還是算得出來——用上一集那條公式。畫面上那個矩陣是程式算的，跟數值解出來的隱函數的雅可比完全相同。第 3 章第 11 節到此結束，下一集講第 12 節的子流形與 Lagrange 乘子。

**Narration (EN)**

> And the differential can still be computed, by the previous episode's formula. The matrix on screen was computed here and matches the Jacobian of the implicit function solved numerically. That ends section eleven; next come submanifolds and Lagrange multipliers.

**動畫**

左邊三個矩陣：dG¹、dG²，箭頭之後是公式算出來的 dFₐ。
右側說明它跟數值解出來的隱函數的雅可比完全相同。

---

## 兩個例子都是這樣挑的

九次與六次，都在「五次以上一般沒有根式解」的那一邊。這不是巧合：
整節的重點就是定理給的是存在性、唯一性與可微性，而不是公式。
書上自己的例子（`x = ⟨y₁³ + y₂³, y₁² + y₂²⟩`，在 b = ⟨1, 2⟩ 行列式 −12）也是六次，
理由一樣。這一集換了一組數字，好讓每一步都算得出來、驗得起來。

## 第 3 章第 11 節到此結束

下一集進第 12 節：子流形與 Lagrange 乘子（書頁 172 起）。
書頁 169–171 是習題 11.1–11.29，依 PLAYBOOK 第 8 節不做解答。
第 11 節欠的存在性證明要等第 4 章的完備性與不動點定理。
