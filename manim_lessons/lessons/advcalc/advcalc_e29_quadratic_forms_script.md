# advcalc E29 — 第 2 章：二次型與慣性定理

Chapter 2: Quadratic Forms and the Law of Inertia

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 7 節的前段（書頁 111–113）。第 7 節帶星號，整節沒有習題。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e29_quadratic_forms.py`（`AdvCalcE29ZH` / `AdvCalcE29EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[29]` / `FORMULAS_ADVCALC[29]`）
- 配音：`manim_lessons/samples/audio_e29/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.17 分（190 秒）／英文 3.31 分（199 秒）

## 這一集的例子是倒著造的

E30 才會講「怎麼把一個矩陣算成對角形」，所以 E29 不能假裝跑那個算法。作法是反過來：先挑定
對角線 `( 1 , 1 , − 1 , 0 )`，用一個整數的么模矩陣 C 做合同變換 `T = Cᵀ D C`，得到一個看起來
普通的對稱矩陣；再用一個**獨立寫的**合同對角化程序，只從 T 出發把對角線算回來，然後斷言兩者
的正負個數相符。

場景檔頂端還驗了：T 確實對稱、p 與 n 是 2 與 1、秩等於 p + n、極化公式在具體的 ξ 與 η 上成立、
以及縮放那一步真的把 q 從 4 調到 1。**改動 D 或 C 會讓這一集 import 失敗**，而不是安靜地畫出一個
不再說明那些性質的例子。

---

## Beat 0 — 一個比較小、但做得成的問題 / a smaller problem, and one that can be solved
*配音長度：中文 20.2s ／ 英文 17.6s*

**畫面公式**

```
一個比較小、但做得成的問題   |   a smaller problem, and one that can be solved
T  ∈  Hom ( V , V* )        ω : V × V → ℝ        ω ( ξ , η )  =  [ T ( ξ ) ] ( η )
```

**旁白（繁中）**

> 第 7 節帶星號，處理一個比較小、但做得成的問題。線性代數真正想做的是挑一組基底，讓一個變換的矩陣變簡單。那件事很難。這一節換個目標：讓 Hom ( V , V* ) 裡的變換變簡單。

**Narration (EN)**

> Section seven is starred, and settles a smaller problem than the one linear algebra really wants. The real problem is the structure of a transformation in Hom V: a basis making its matrix simple. That is hard. Here the target is a transformation from V to V star.

**動畫**

左右兩個方框並排：左邊是線性代數真正想解決的問題（Hom ( V , V ) 裡的變換），三行說明它有多難；右邊是這一節換的目標（Hom ( V , V* ) 裡的變換），三行說明它做得到。中間一條分隔線。

## Beat 1 — ω 選了基底就有矩陣 / choose a basis and omega has a matrix
*配音長度：中文 15.2s ／ 英文 16.2s*

**畫面公式**

```
ω 選了基底就有矩陣   |   choose a basis and omega has a matrix
t ᵢⱼ  =  ω ( α ᵢ , α ⱼ )
```

**旁白（繁中）**

> 這種變換等價於 V 上的一個雙線性泛函 ω。選一組基底之後，ω 就決定一個矩陣：第 i 列第 j 行那一格，是 ω 作用在第 i 個與第 j 個基底向量上的值。

**Narration (EN)**

> Such a transformation is equivalent to a bilinear functional omega on V. Once a basis is chosen, omega determines a matrix: the entry in row i and column j is the value of omega on the ith and jth basis vectors.

**動畫**

左邊 ω 是一台有兩個輸入槽的機器，吃 α ᵢ 與 α ⱼ，吐出 t ᵢⱼ；右邊一個 4×4 的格子陣，第 i 列第 j 行那一格高亮並標著 t ᵢⱼ，列與行的索引標在格子外面。

## Beat 2 — 雙重和與二次型 / the double sum and the quadratic form
*配音長度：中文 16.2s ／ 英文 19.1s*

**畫面公式**

```
雙重和與二次型   |   the double sum and the quadratic form
ω ( ξ , η )  =  Σ ᵢ , ⱼ  t ᵢⱼ x ᵢ y ⱼ        q ( ξ )  =  ω ( ξ , ξ )
```

**旁白（繁中）**

> 把 ξ 與 η 用座標展開，雙線性讓 ω 拆成雙重和：t ᵢⱼ 乘 x ᵢ 乘 y ⱼ 全部加起來。兩個變數都取同一個 ξ，得到的 q 就是座標的齊次二次多項式，叫二次型。

**Narration (EN)**

> Expand xi and eta in coordinates and bilinearity splits omega into a double sum: omega is the sum of t-i-j times x-i times y-j. Setting both arguments to the same xi gives q, a homogeneous quadratic polynomial in the coordinates, called a quadratic form.

**動畫**

左邊是例子的矩陣，對角線高亮。右邊三行：完整的二次型多項式、對角線那四格各給的平方項、以及非對角線成對出現所以各帶一個 2 的交叉項。三行都是從矩陣算出來的。

## Beat 3 — 對稱時，q 反過來決定 ω / when omega is symmetric, q determines it back
*配音長度：中文 18.6s ／ 英文 20.7s*

**畫面公式**

```
對稱時，q 反過來決定 ω   |   when omega is symmetric, q determines it back
t ᵢⱼ  =  t ⱼᵢ        ω ( ξ , η )  =  [ q ( ξ + η ) − q ( ξ − η ) ] / 4
```

**旁白（繁中）**

> 接下來假設 ω 對稱，兩個變數對調不改變值。這時 q 反過來也決定 ω：ξ 加 η 的 q 減掉 ξ 減 η 的 q，再除以四就是 ω。所以談二次型跟談對稱雙線性泛函是同一件事。

**Narration (EN)**

> From here we assume omega is symmetric, meaning that swapping its two arguments changes nothing. Then q determines omega in return: take q of xi plus eta, subtract q of xi minus eta, and divide by four. So quadratic forms and symmetric bilinear functionals are the same subject.

**動畫**

矩陣與它自己的轉置並排，中間一個等號，鏡射的那幾對格子高亮——對稱畫成「等於自己的轉置」，而不是沿對角線畫一條線（那條線會壓在對角線的數字上，`tools/collide.py` 會報）。右邊用具體的 ξ 與 η 把極化公式兩邊各算一次。

## Beat 4 — 目標：ω 正交規範基底 / the goal: a basis orthonormal for omega
*配音長度：中文 14.9s ／ 英文 16.8s*

**畫面公式**

```
目標：ω 正交規範基底   |   the goal: a basis orthonormal for omega
ω ( α ᵢ , α ⱼ ) = 0   ( i ≠ j )        ω ( α ᵢ , α ᵢ )  ∈  { 0 , 1 , − 1 }
```

**旁白（繁中）**

> 目標是找一組基底，讓不同的基底向量互相取零，而每個基底向量對自己的值只會是一、負一或零。這種基底借用內積的講法，叫 ω 正交規範基底。

**Narration (EN)**

> The goal is a basis on which distinct basis vectors give zero against each other, and each one gives itself one of only three values: one, minus one, or zero. Borrowing the language of scalar products, such a basis is called orthonormal for omega.

**動畫**

目標矩陣：對角線是 1、1、−1、0，其餘全是零；每個對角元右邊放一個小點，顏色分正、負、零三種。右邊三行說明什麼叫 ω 正交規範基底。

## Beat 5 — 一維：把值調成 ±1 / dimension one: scale the value to plus or minus one
*配音長度：中文 16.2s ／ 英文 17.5s*

**畫面公式**

```
一維：把值調成 ±1   |   dimension one: scale the value to plus or minus one
α  =  x β        x  =  1 / √ | ω ( β , β ) |        ω ( α , α )  =  ± 1
```

**旁白（繁中）**

> 存在性用維數作歸納。一維時：如果 ω 不是零，取一個 q 不為零的 β，乘上一個適當的倍數就能把值調成正負一，那個倍數是 β 自己的值取絕對值再開根號的倒數。

**Narration (EN)**

> Existence is an induction on dimension. In dimension one: if omega is not zero, take a beta whose q is nonzero and scale it, and the value becomes plus or minus one. The scale factor is one over the square root of the absolute value of that number.

**動畫**

一條數線上兩個點：β 標著 q = 4，α = β / 2 標著 q = 1，底下一個箭頭從 β 指到 α，並寫出 x = 1 / √|q(β)| = 1/2。兩個值都是把向量代進這一集的例子實際算出來的。

## Beat 6 — 配 α ₙ 的那個泛函，核空間少一維 / pairing against alpha-n: a null space one dimension down
*配音長度：中文 19.2s ／ 英文 18.6s*

**畫面公式**

```
配 α ₙ 的那個泛函，核空間少一維   |   pairing against alpha-n: a null space one dimension down
f ( ξ )  =  ω ( ξ , α ₙ )        N  =  f ⁻¹ ( 0 )        d ( N )  =  n − 1
```

**旁白（繁中）**

> 一般情形：ω 不是零函數，所以存在 β 使得 ω 對 β 與 β 不為零。調好當成最後一個基底向量 α ₙ。接著看「拿 ξ 去配 α ₙ」這個泛函，它不是零泛函，核空間 N 的維數是 n 減一。

**Narration (EN)**

> In general omega is not the zero functional, so some beta has omega of beta with beta nonzero. Scale it and make it the last basis vector alpha-n. Now the functional that pairs xi against alpha-n is not the zero functional, so its null space N has dimension n minus one.

**動畫**

左邊 V 是一個橢圓，裡面一條水平線是核空間 N，α ₙ 是一支從 N 指向上方的箭頭。右邊一條垂直的實數線，兩支箭頭分別從 N 與 α ₙ 指過去，落在 0 與 ± 1；標籤放在線的右側、箭頭停在線的左側，所以沒有任何東西畫在數字上。

## Beat 7 — 歸納：把 N 的基底接上 α ₙ / the induction: N's basis, with alpha-n added
*配音長度：中文 18.6s ／ 英文 19.2s*

**畫面公式**

```
歸納：把 N 的基底接上 α ₙ   |   the induction: N's basis, with alpha-n added
{ α ᵢ } ₁ⁿ⁻¹  ⊂  N        ω ( α ᵢ , α ₙ )  =  0   ( i < n )
```

**旁白（繁中）**

> 把 ω 限制在 N 上，歸納假設給出 N 的一組正交規範基底。而 N 裡每一個向量跟 α ₙ 配出來都是零——這正是核空間的定義。湊在一起就是整個 V 的正交規範基底。這是定理 7.1。

**Narration (EN)**

> Restrict omega to N and the inductive hypothesis gives N an orthonormal basis. Every vector of N pairs with alpha-n to zero, which is exactly what belonging to that null space means. Put them together and you have an orthonormal basis for the whole of V. That is Theorem 7.1.

**動畫**

同一張橢圓與核空間的圖，N 上多了 α ₁、α ₂ 到 α ₙ₋₁ 三個點。右邊三行說明歸納怎麼接：N 比較小所以歸納假設給得出基底、N 裡的向量跟 α ₙ 配出零、接起來就是整個 V 的基底。

## Beat 8 — 定理 7.2：只剩平方項 / theorem 7.2: only square terms are left
*配音長度：中文 17.1s ／ 英文 17.3s*

**畫面公式**

```
定理 7.2：只剩平方項   |   theorem 7.2: only square terms are left
q ( ξ )  =  x ₁² + … + x ₚ²  −  x ₚ₊₁² − … − x ₚ₊ₙ²
```

**旁白（繁中）**

> 有了這種基底，q 就只剩平方項：正的那些排前面、負的接著、零的最後。所以 q 等於前 p 個座標的平方和，減掉接下來 n 個座標的平方和。這是定理 7.2。

**Narration (EN)**

> On such a basis q keeps only its square terms: the positive ones first, the negative ones next, the zeros last. So q is the sum of the first p coordinates squared, minus the sum of the next n coordinates squared. That is Theorem 7.2.

**動畫**

例子的正交規範形式：對角線 1、1、−1、0，格子下方三條色棒分別框出正的兩格、負的一格、零的一格。右邊寫出只剩平方項的 q，以及正負零各幾個。這個對角線是程式從原矩陣重新算出來的。

## Beat 9 — p 與 n 不依賴基底 / p and n do not depend on the basis
*配音長度：中文 18.1s ／ 英文 18.5s*

**畫面公式**

```
p 與 n 不依賴基底   |   p and n do not depend on the basis
V  =  V ₁ ⊕ V ₋₁ ⊕ V ₀        V ₁ ∩ ( V ₋₁ ⊕ V ₀ )  =  { 0 }
```

**旁白（繁中）**

> 關鍵是 p 與 n 不依賴基底。理由：值為正的那塊 V ₁ 跟另外兩塊的直和只交於零，因為交集裡的非零向量會同時滿足 q 大於零與 q 小於等於零。互相是補空間，維數只好相等。

**Narration (EN)**

> What matters is that p and n do not depend on the basis. The part where q is positive meets the sum of the other two only at zero: a nonzero vector in that intersection would have q positive and q at most zero at once. Each is a complement of the other, so the dimensions agree.

**動畫**

V ₁、V ₋₁、V ₀ 三個方框用 ⊕ 連起來等於 V，每個方框下面標著維數與 q 的正負號。底下一行寫出交集裡的非零向量會同時滿足 q > 0 與 q ≤ 0。

## Beat 10 — 符號差與秩 / the signature and the rank
*配音長度：中文 15.9s ／ 英文 17.1s*

**畫面公式**

```
符號差與秩   |   the signature and the rank
σ  =  p − n        r  =  p + n
```

**旁白（繁中）**

> p 減 n 叫這個二次型的符號差，p 加 n 叫它的秩，而秩就是任何一個表示矩陣的秩。下一集講怎麼真的把一個矩陣算成這個形狀——只用加減乘除，不必解多項式方程。

**Narration (EN)**

> The number p minus n is the signature of the form and p plus n is its rank, which is the rank of any matrix representing it. Next time: how to actually compute a matrix into this shape, using nothing but arithmetic, with no polynomial equations to solve.

**動畫**

左邊兩個方框寫出 σ = p − n = 1 與 r = p + n = 3；右邊是例子的原矩陣，底下標著它的秩，也是算出來的。

---

## 抽幀時發現、但沒有重渲的一件事

英文版 beat 6 的兩個窄欄位字幕（`x=0.10, w=2.20`）被 `_mid` 壓縮之後，跟旁邊核空間那條線的
`N` 標籤擠在一起，讀起來像同一句。`collide.py` 沒有報，因為兩個邊界框只是相鄰、沒有重疊。

**英文大約是中文的兩倍寬**，所以窄欄位裡的雙語字幕在英文版會出問題。後面的集數改用符號
（`α ₙ ↦ ± 1`）放窄欄位。這一格影響不大，而且 YouTube 的 token 不能刪片、重上會留下一支要手動
清掉的舊片，所以留著。
