# advcalc E77 — 第 6 章：線性方程的解空間

Chapter 6: The Solution Space of the Linear Equation

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 3 節「線性方程」的**前半**（書頁 276–277，收在定理 3.2）。

**§3 從 1 集改成 2 集**（2026-09-17 動工時改的）。原本細目表估 1 集，可是它有定理 3.1 到 3.4 加引理 3.1、3.2，內容橫跨 276–280，而且前半（解空間的結構）與後半（e ᵗᵀ 與 Jordan 型展開）是兩件不同的事。切在定理 3.2 之後。**OUTLINE 的五個地方一起改過**，總集數 170 → 171。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e77_linear.py`（`AdvCalcE77ZH` / `AdvCalcE77EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[77]` / `FORMULAS_ADVCALC[77]`）
- 配音：`manim_lessons/samples/audio_e77/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 231.8 秒（3:51）／英文 197.4 秒（3:17）
- YouTube（私人）：中文 https://youtu.be/EDl3HI8v154 ／英文 https://youtu.be/S6aB3QBeY0Y

## 這半節在做什麼

**線性把定理 1.4 的假設免費送上來。** F ( t , α ) = T ₜ ( α ) 時，

```
F ( t , ξ ) − F ( t , η )   =   T ₜ ( ξ − η )       ⇒       ‖ · ‖  ≤  c ( t ) ‖ ξ − η ‖
```

Lipschitz 條件退化成「T ₜ 有界」，而且**自動對 W 裡所有點成立**——正是定理 1.4 要的那種。
所以這一節的解一律活在整個 I 上。

**於是整個問題變成線性代數**，而且一個不等式都用不到：

```
S : X ₁ → X ₀            ( S f ) ( t )  =  f ′ ( t ) − F ( t , f ( t ) )
```

**定理 3.1** 說了四件事，書上指出它們彼此等價，而最簡潔的說法是一個同構：

```
⟨ S , π ₜ ₀ ⟩   :   X ₁   ≅   X ₀ × W
        N = ker S   ↔   { 0 } × W                M = ker π ₜ ₀   ↔   X ₀ × { 0 }
```

**左邊的分解只是右邊那個明顯的直和分解拉回來。** 證明也只有一句話：對固定的 g 設 G = F + g，
那就是第 1 節的方程，定理 1.3、1.4 給出唯一的整體解。

**M 是 N 的補**，這件事把初始值問題拆成兩個獨立的子問題：h 解非齊次而初始值歸零、
k 解齊次而帶著初始值，f = h + k。

**基本解** K ₜ = φ ₜ ∘ φ ₀ ⁻ ¹ 是 W 到自己的一族線性同構，K ₀ = I，而 K ₜ ( β ) 就是
通過 ⟨ 0 , β ⟩ 那條解在 t 的值——**一個算子把所有初始值的解一次全帶著走**。

**d K ₜ / d t = T ₜ ∘ K ₜ 目前只是逐點的意思。** 假設裡只說 ‖ T ₜ ‖ 被 c ( t ) 壓住，
沒說 t ↦ T ₜ 連續，所以導數不一定以 Hom W 的範數極限存在。**定理 3.2** 補上這一點。

## 這一集用的例子

**一個真的隨時間變、但基本解仍寫得出來的線性方程**：

```
T ₜ   =   ( 1 + t )  J                    K ₜ   =   exp ( Θ ( t )  J )  ,   Θ ( t ) = t + t ² / 2
```

所有 T ₜ 互相交換，所以指數可以直接積起來。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| K ₀ 是恆等 | 逐元比對 | 差 < 1e-15 |
| ‖ T ₜ ‖ 就是那個 c ( t ) | 單位圓上取 720 點 | 1.0000, 1.5000, 2.0000, 2.5000, 3.0000 |
| K 滿足自己的方程 | 四個 t 的數值微分對 T ₜ K ₜ | 差 < 1e-6 |
| K ₜ ( β ) 真的是解 | 三個 β × 三個 t | 差 < 1e-6 |
| 兩條基底解永遠是基 | det [ f ₁ ( t ) f ₂ ( t ) ] | 全部 = 1.00000000 |
| S 是滿射 | 對 g = ( 1 , 0 ) 建解再代回 S | (1.0000, -0.0000), (1.0000, +0.0000), (1.0000, +0.0000) |
| M ⊕ N 的分解 | h ( t ₀ ) 與 S h 對 S f | h ( t ₀ ) < 1e-12，S h = S f，S k = 0 |

**那個行列式是同構的全部內容**：兩條解在任何一個時刻取的值都還是線性獨立，從來不會塌下去。
這是線性方程獨有的——非線性時解會互相撞上（E74 的反例正是如此）。

## 這一輪抓到的錯

- **兩條軌道其實是同一個圓。** 第 5 拍原本把兩條基底解各畫一條軌道，一紫一青；
  可是兩條都是單位向量，而 K ₜ 是旋轉，**兩條軌道完全重合**——「兩條解」畫成了一條。
  改成：灰圈畫一次（那是共同的軌道），再畫兩組箭頭在 t = 0 與 t = 0.8，
  每組兩支永遠垂直、虛線接起斜邊，剛體般轉動。
  **這是「畫成兩個其實是同一個」的第四次**（E72 兩個矩陣、E74 δ c 與 δ m、E76 上下兩排）。
  bounds 與 collide 都看不到這一類：重合的線不算碰撞。
- **三條軌道也全是單位圓。** 第 9 拍用了三個 β：( 1 , 0 )、( 0 , 1 )、( − 0.7 , 0.7 )，
  長度全是 1 或 0.99，三條軌道又疊成一個圓。改成 1.0 / 0.62 / 0.34 三個不同長度。
- **圖例的色塊與標籤互相疊。** `_legend` 把標籤置中在 `x + 0.36 + w / 2`，
  w 給小了的時候標籤左緣會壓到色塊上。間距改成 0.46，並把窄標籤的 w 放寬。
- **t ² 畫到框外**（第 6 拍，y 到 +1.76）、**圖例掉到畫面外**（第 8 拍，x 到 −6.95）、
  **表格跑進說明列**（第 4 拍）——bounds / collide 各自抓到。

## 十一拍

### 第 1 拍 — 線性讓定理 1.4 免費送 / linearity hands over theorem 1.4

公式列：

```
F ( t , α )  =  T ₜ ( α )            ‖ T ₜ ‖   ≤   c ( t )
```

中文旁白：第 3 節假設 F 對第二個變數是線性的：F t α 等於 T t 作用在 α 上，而 T t 的範數被一個連續函數 c t 控制住。這一句話就把定理 1.4 的強 Lipschitz 假設免費送給我們，所以這一節的解一律活在整個 I 上。

English: Section 3 assumes F is linear in its second variable: F at t and alpha is an operator applied to alpha, with its norm bounded by a continuous function of t. That hands us the strong Lipschitz hypothesis of Theorem 1.4 for free, so every solution lives on all of I.

### 第 2 拍 — 兩個函數空間與 S / two function spaces and S

公式列：

```
S : X ₁ → X ₀            ( S f ) ( t )  =  f ′ ( t ) − F ( t , f ( t ) )
```

中文旁白：於是可以只談整體解，而整個問題變成線性代數。設 X 零是 I 到 W 的連續函數空間，X 一是其中有連續一階導數的那些。定義 S 把 f 送到 f 一撇減去 F 帶入 t 與 f t。範數在接下來的定理裡完全不起作用。

English: So we may speak only of global solutions, and the problem becomes linear algebra. Let one space be the continuous functions from I to W and the other those with a continuous derivative. Define S by sending f to its derivative minus F at t and f of t.

### 第 3 拍 — 定理 3.1 / theorem 3.1

公式列：

```
N  =  ker S           π ₜ ₀ ↾ N  :  N  ≅  W           X ₁  ≅  X ₀ × W
```

中文旁白：定理 3.1：S 是從 X 一到 X 零的滿射線性映射；方程的整體解全體 N 正是 S 的核，所以是向量空間；對每個 t 零，在 t 零取值這個映射限制到 N 上是 N 到 W 的同構；它的核 M 因此是 N 的補，並決定 S 的一個右反元素。

English: Theorem 3.1. S is a surjective linear map; the global solutions are exactly its null space, hence a vector space; evaluation at any initial time restricted to that null space is an isomorphism onto W; and the null space of evaluation is a complement of it.

### 第 4 拍 — 證明只有一句話 / the proof is one sentence

公式列：

```
G ( t , α )  =  F ( t , α ) + g ( t )         ⟨ S , π ₜ ₀ ⟩  :  X ₁  →  X ₀ × W
```

中文旁白：證明只有一句話。對固定的 g 設 G 等於 F 加 g，那是第 1 節那個方程，由定理 1.3 與 1.4 它有唯一的整體解通過任一初始點，定義域是整個 I。所以把 f 送到 S f 與 f t 零這個映射是雙射，而且顯然線性。

English: The proof is one sentence. For fixed g set G to be F plus g, which is section 1's equation, so it has a unique global solution through any initial point. Hence sending f to the pair of S f and its value at the initial time is a bijection, and plainly linear.

### 第 5 拍 — N 與 W 同構 / the solution space is a copy of W

公式列：

```
dim N   =   dim W   =   2                  f   ↦   f ( t ₀ )
```

中文旁白：第一個結果是 N 與 W 同構，所以維度相同。畫面上是兩條基底解：一條在時間零通過第一個基向量，一條通過第二個。在任何一個時刻取值，它們給出的仍然是 W 的一組基——同構就是這個意思。

English: The first consequence is that the solution space is isomorphic to W, so they have the same dimension. On screen are two basis solutions, one through each basis vector at time zero. Evaluated at any moment they still give a basis of W, and that is the isomorphism.

### 第 6 拍 — M 是 N 的補 / M is a complement of N

公式列：

```
M  =  ker π ₜ ₀                  X ₁   =   M  ⊕  N
```

中文旁白：第二個結果是 M 與 N 互為補。M 是在 t 零取值為零的那些函數，而 X 一等於 M 直和 N。任何一個 X 一裡的函數，都唯一地拆成「在 t 零歸零的那一半」加上「一條解」。

English: The second consequence is that the two spaces are complementary. One is the functions vanishing at the initial time, and the whole space is their direct sum. Every function with a continuous derivative splits uniquely into a part that vanishes at the initial time plus a solution.

### 第 7 拍 — 初始值問題拆成兩半 / the problem splits in two

公式列：

```
f  =  h  +  k         S h = g , h ( t ₀ ) = 0         S k = 0 , k ( t ₀ ) = α ₀
```

中文旁白：這個分解把初始值問題拆成兩個獨立的子問題。h 解非齊次方程但初始值是零；k 解齊次方程但初始值是 α 零。答案就是 h 加 k。書上說這是「非齊次方程配齊次初始資料」與「齊次方程配非齊次初始資料」的直和。

English: That splitting breaks the initial-value problem into two independent subproblems. One solves the inhomogeneous equation with zero initial value; the other the homogeneous equation with the given initial value. The answer is their sum.

### 第 8 拍 — 基本解 K ₜ / the fundamental solution

公式列：

```
K ₜ  =  φ ₜ ∘ φ ₀ ⁻ ¹          f ᵦ ( t )  =  K ₜ ( β )          K ₀  =  I
```

中文旁白：接下來只看齊次方程。φ t 是在時刻 t 取值那個 N 到 W 的同構。取 t 零等於零，定義 K t 等於 φ t 複合 φ 零的反元素。那麼 K t 是 W 到自己的一族線性同構，而 K t 作用在 β 上就是通過零與 β 的那條解。書上叫它基本解。

English: Now only the homogeneous equation. Evaluation at time t is an isomorphism from the solution space onto W. With the initial time zero, define K at t as that isomorphism composed with the inverse of the one at zero. K at t applied to a vector is the solution through it.

### 第 9 拍 — 導數只是逐點的意思 / the derivative is only pointwise

公式列：

```
d K ₜ / d t  =  T ₜ ∘ K ₜ                ( β )
```

中文旁白：既然每條解都滿足方程，K t 對 t 的導數等於 T t 複合 K t——可是這句話目前只是逐點的意思，對每個 β 成立。導數不一定以 Hom W 的範數極限存在，因為假設裡沒有說 t 送到 T t 是連續的。

English: Since every solution satisfies the equation, the derivative of K is the operator composed with K. But that is so far only pointwise, true at each vector. The derivative need not exist as a norm limit, because nothing says t goes continuously to the operator.

### 第 10 拍 — 定理 3.2 / theorem 3.2

公式列：

```
d A / d t  =  T ₜ ∘ A   ,   A ₀  =  I               A ₜ   =   K ₜ
```

中文旁白：定理 3.2 補上這一點：只要 t 送到 T t 連續，初始值問題 A 一撇等於 T t 複合 A、A 零是恆等，在有連續導數的那個空間裡就有唯一解。而在 β 取值是有界線性，所以那個解作用在 β 上滿足同一個方程，兩者因此相等。

English: Theorem 3.2 supplies that. If t does go continuously to the operator, the initial-value problem for A with A at zero the identity has a unique solution with a continuous derivative. Evaluation at a vector is bounded and linear, so that solution agrees with K.

### 第 11 拍 — 這一集的例子，與下一集 / the example, and what comes next

公式列：

```
T ₜ  =  ( 1 + t ) J           K ₜ  =  exp ( Θ ( t ) J )  ,  Θ ( t ) = t + t ² / 2
```

中文旁白：這一集的例子是 T t 等於一加 t 再乘旋轉生成元。它的基本解算得出來：轉 t 加二分之一 t 平方那麼多角度的旋轉。K 零是恆等、導數也對得上。下一集接定理 3.3 的顯式公式，以及常係數時的 e 的 t T 次方。

English: The example here is the rotation generator scaled by one plus t. Its fundamental solution can be written down: rotation through t plus half t squared. Next episode takes up the explicit formula of Theorem 3.3 and the constant coefficient case.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | ‖ T ₜ ‖ = 1 + t 的直線與五個取樣點；右表把「線性 ⇒ Lipschitz ⇒ J = I」三步列出來 |
| 2 | X ₁ → X ₀ 兩個方塊與 S 的箭頭，下面標出兩個空間各是什麼、f 被送成什麼；最後一列的範數是灰的 |
| 3 | X ₁ ≅ X ₀ × W 的對照圖：左邊 N 與 M，右邊 { 0 } × W 與 X ₀ × { 0 }，逐列對應 |
| 4 | g = ( 1 , 0 ) 那條解的兩個座標各一條曲線；右表把 S f 算回來，逐列都是 g 自己 |
| 5 | 一個灰圈加兩組垂直的箭頭（t = 0 與 t = 0.8），虛線接起斜邊；右表的行列式永遠是 1 |
| 6 | 隨手取的 f = ⟨ t ² , sin t ⟩ 拆成 h 加 k，紅線恰在 t ₀ 穿過零點 |
| 7 | f 分出 h 與 k 兩個方塊，各自帶一半的資料；右表寫出 R 與 ( π ₜ ₀ ↾ N ) ⁻ ¹ |
| 8 | 一條軌道加三支箭頭（β、K ₀ ․ ₇ β、K ₁ ․ ₅ β），三支同長因為 K ₜ 是旋轉 |
| 9 | 三個長度不同的 β 各一條軌道，每條在 t = 1.1 加一支切向箭頭——逐點驗出來的意思 |
| 10 | K ₜ 兩個矩陣元對 t 的曲線，光滑；右表把定理 3.2 的四步列出來 |
| 11 | 一條軌道加四個等時間間隔的點，間隔越來越大因為 ‖ T ₜ ‖ 一直在長 |
