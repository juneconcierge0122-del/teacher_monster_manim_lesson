# advcalc E23 — 第 2 章：矩陣與線性變換的字典

Chapter 2: Matrices and Linear Transformations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 4 節的前段（書頁 88–90）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e23_matrices.py`（`AdvCalcE23ZH` / `AdvCalcE23EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[23]` / `FORMULAS_ADVCALC[23]`）
- 配音：`manim_lessons/samples/audio_e23/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.15 分（189 秒）／英文 3.13 分（188 秒）

第 4 節到書頁 96 為止，書頁 96–98 是習題 4.1–4.26，依 `docs/PLAYBOOK.md` 第 8 節不做解答；書頁 99 起是第 5 節「跡與行列式」。本節其餘內容（轉置、秩、矩陣乘法、換基底、Hom 的標準基底）留給 E24 與 E25。

符號沿用 E21 與 E22：β 是 V 的基底、ε 是對偶基底、λ 是泛函。書上寫 α 是 V 的基底、β 是 W 的基底、μ 是 W* 的對偶基底，但 β 在前兩集已經是 V 的基底，所以新出現的物件（W 的基底）改用新字母 γ，而不是把 β 的意思換掉。書上的 T̄ 改寫成 T′：大寫字母加組合長音符會渲染得很淡，而書自己在書頁 94 就是用撇號表示同一種角色。

全集共用一組具體例子：m = 2、n = 3。這件事是必要的而不是隨手選的——有三拍把陣列畫在 W 的圖旁邊，而 W 只能畫成平面，初稿用了 3×4 的陣列配兩個 γ 箭頭，於是第 10 拍的 ε_k 讀的係數在陣列裡沒有位置。`bounds.py` 與單讀公式列都看不到這件事，只有把一張幀的兩半擺在一起才看得出來。

---

## Beat 0 — 矩陣其實是一個函數 / a matrix is really a function
*配音長度：中文 18.0s ／ 英文 15.3s*

**畫面公式**

```
矩陣其實是一個函數   |   a matrix is really a function
t : { 1 … m } × { 1 … n }  →  ℝ        t ( i , j )  =  tᵢⱼ        t  =  { tᵢⱼ }
```

**旁白（繁中）**

> 矩陣給人的印象是一個長方形數字陣列，但陣列只是畫法。矩陣其實是函數，定義在列指標配行指標的指標集上，就像數列也是函數。第一個指標數橫列，第二個數直行。

**Narration (EN)**

> A matrix is usually pictured as a rectangular array of numbers, but that picture is inexact. The array is only a way of drawing it. A matrix is really a function on the index set of row and column pairs, just as a sequence is a function.

**動畫**

左右並排兩張圖：左邊是熟悉的方括號陣列，右邊把同一個東西畫成指標集上的函數——每一格是一個 ⟨i, j⟩ 對，其中一格反白，箭頭從它出發指到一條實數線上的一點。中間一個等號說這兩張圖是同一個對象。

## Beat 1 — 所有矩陣自己構成一個向量空間 / the matrices themselves form a vector space
*配音長度：中文 18.0s ／ 英文 16.5s*

**畫面公式**

```
所有矩陣自己構成一個向量空間   |   the matrices themselves form a vector space
( s + t )ᵢⱼ = sᵢⱼ + tᵢⱼ        ( c t )ᵢⱼ = c tᵢⱼ        d ( ℝ ᵐˣⁿ ) = m n
```

**旁白（繁中）**

> 既然是函數，矩陣的加法就是函數的加法，逐格相加，純量乘法也一樣。所以所有矩陣自己構成一個向量空間，維數是列數乘行數，就是一個座標空間，只是指標集花俏一點。

**Narration (EN)**

> Being a function, matrices add place by place, which is just the addition of functions, and scalar multiplication works the same way. So all matrices of one shape form a vector space, a Cartesian space with a rather fancy finite index set.

**動畫**

三個同形狀的陣列排成加法算式，對應的那一格都反白成同一個顏色，並用短豎線接到上方一條虛線，說明加法只在對應格之間發生。右邊一個箭頭把陣列攤平成一列六個點，也就是同樣多座標的座標空間。

## Beat 2 — 定理 4.1：直行就是骨架 / theorem 4.1: the columns are the skeleton
*配音長度：中文 15.4s ／ 英文 16.6s*

**畫面公式**

```
定理 4.1：直行就是骨架   |   theorem 4.1: the columns are the skeleton
t ʲ  =  ⟨ t₁ⱼ , … , tₘⱼ ⟩  ∈  ℝᵐ        T ( δ ʲ )  =  t ʲ        skeleton T = { t ʲ }
```

**旁白（繁中）**

> 定理四點一先處理座標空間。把矩陣的第 j 行看成一個 m 元組，那麼恰好有一個線性映射的骨架就是這串行向量，也就是把標準基底的第 j 個向量送到第 j 行。

**Narration (EN)**

> Theorem four point one handles the Cartesian case. Read the jth column of the matrix as an m-tuple. Then there is exactly one linear map whose skeleton is that list of columns, that is, one that sends the jth standard basis vector to the jth column.

**動畫**

左邊是標準基底向量，第三格是 1、其餘是 0；中間的陣列把第三直行框起來；右邊是被框起來那一行抽出來的二元組。畫面上每一個具體的指標都由同一個常數決定，所以 δ³、框住的行、與 t₁₃ / t₂₃ 三者不可能指到不同的行。

## Beat 3 — 那個映射就是線性組合映射 / the map is the linear combination map
*配音長度：中文 16.7s ／ 英文 16.0s*

**畫面公式**

```
那個映射就是線性組合映射   |   the map is the linear combination map
T ( x )  =  Σ₁ⁿ xⱼ t ʲ        yᵢ  =  Σ₁ⁿ tᵢⱼ xⱼ    ( i = 1 , … , m )
```

**旁白（繁中）**

> 這個映射就是線性組合映射：輸入的第 j 個座標乘上第 j 行，全部加起來。逐個座標寫開，就是大家最熟悉的那組純量方程，第 i 個輸出由第 i 橫列跟輸入配出來。

**Narration (EN)**

> What is that map? It is the linear combination map: multiply the jth coordinate of the input by the jth column and add. Written out coordinate by coordinate, this gives the familiar scalar equations, each output being a row paired against the input.

**動畫**

左邊是真的幾何圖：兩個行向量畫成箭頭，各自乘上係數（虛線是縮放後的長度），用平行四邊形加起來得到輸出。和的箭頭端點是由係數乘上畫出來的向量算出來的，不是手動擺的。右邊是同一件事的純量方程版本：陣列的第二橫列與輸入元組配出輸出的第二格。

## Beat 4 — 矩陣與映射之間是自然同構 / matrices and maps: a natural isomorphism
*配音長度：中文 17.6s ／ 英文 16.6s*

**畫面公式**

```
矩陣與映射之間是自然同構   |   matrices and maps: a natural isomorphism
{ tᵢⱼ }  ↦  T   :   ℝ ᵐˣⁿ  ≅  Hom ( ℝⁿ , ℝᵐ )        ℝ ᵐˣⁿ  ≅  ( ℝᵐ ) ⁿ
```

**旁白（繁中）**

> 反過來每個線性映射都這樣出現，所以矩陣與映射之間是自然同構。這裡還偷用了另一個：把矩陣看成一串行向量，是把兩個指標的函數，跟 m 元組的 n 元組當成同一件東西。

**Narration (EN)**

> Every linear map arises this way, so matrices and maps correspond by a natural isomorphism. A second one is being used quietly here: reading a matrix as a list of columns identifies a function of two indices with an n-tuple of m-tuples.

**動畫**

一個三角形，三個頂點是同一個對象的三個面向：兩個指標的函數、一串行向量、一個線性映射。三條邊都標著同構符號，強調這些對應都不必挑。

## Beat 5 — 橫列的讀法：m 個線性泛函 / reading the rows: m linear functionals
*配音長度：中文 17.5s ／ 英文 16.8s*

**畫面公式**

```
橫列的讀法：m 個線性泛函   |   reading the rows: m linear functionals
fᵢ ( x )  =  Σ₁ⁿ tᵢⱼ xⱼ  ∈  ( ℝⁿ ) *        T  ⟷  ⟨ f₁ , … , fₘ ⟩
```

**旁白（繁中）**

> 橫列有另一種讀法。第 i 條純量方程本身就是一個線性泛函，而係數乘座標加起來，正是座標空間上最一般的泛函。所以 m 條橫列，就是與那個多值映射等價的 m 個泛函。

**Narration (EN)**

> The rows admit another reading. The ith scalar equation is itself a linear functional, and coefficients times coordinates summed is the most general functional on a Cartesian space. So the m rows are the m functionals equivalent to the one vector valued map.

**動畫**

陣列的每一條橫列被一條橫桿標出來，各自沿一個箭頭離開，箭頭上標著 f₁、f₂；抵達的值疊成右邊的輸出元組。與前幾拍的直行讀法對照：同一個陣列，兩種讀法。

## Beat 6 — 定理 4.2：選定基底之後 / theorem 4.2: once bases are chosen
*配音長度：中文 17.6s ／ 英文 18.0s*

**畫面公式**

```
定理 4.2：選定基底之後   |   theorem 4.2: once bases are chosen
T ( βⱼ )  =  Σ₁ᵐ tᵢⱼ γᵢ        { tᵢⱼ }  ↦  T   :   ℝ ᵐˣⁿ  ≅  Hom ( V , W )
```

**旁白（繁中）**

> 離開座標空間。一般的空間沒有現成座標，要先選定有序基底。定理四點二說：兩邊基底選好之後，每個矩陣對應唯一一個映射，把第 j 個基底向量送到第 j 行給的組合。

**Narration (EN)**

> Now leave the Cartesian spaces. A general space has no ready made coordinates, so ordered bases must be chosen. Theorem four point two: with a basis fixed on each side, every matrix gives a unique map sending the jth basis vector to the jth column combination.

**動畫**

左邊 V 畫成橢圓，裡面三個基底向量，第三個反白。箭頭 T 指到右邊的 W，W 裡畫出兩個 γ 箭頭，被反白的基底向量的像用平行四邊形由這兩個 γ 組出來。像的位置是算出來的，所以它一定真的落在 γ 張出來的位置上。虛線把它接到右邊的係數行 t₁₃ / t₂₃。

## Beat 7 — 證明：兩個同構接起來 / the proof: two isomorphisms composed
*配音長度：中文 17.0s ／ 英文 18.7s*

**畫面公式**

```
證明：兩個同構接起來   |   the proof: two isomorphisms composed
T  =  ψ ∘ T ′ ∘ φ ⁻¹        τⱼ  =  Σ₁ᵐ tᵢⱼ γᵢ        T ( βⱼ )  =  τⱼ
```

**旁白（繁中）**

> 證明只是把兩個同構接起來：矩陣先給出座標空間之間的映射，基底同構再把它搬到 V 與 W 上。也可以分兩步看，每一行先決定 W 裡一個向量，這些向量再決定整個映射。

**Narration (EN)**

> The proof only composes two isomorphisms. The matrix first gives a map between Cartesian spaces, and the two basis isomorphisms carry it over to V and W. Another view splits it in two: each column fixes a vector in W, and those n vectors fix the map.

**動畫**

左邊是一個矩形交換圖：上排兩個座標空間、下排 V 與 W，兩側是基底同構 φ 與 ψ。右邊用一條垂直鏈畫同一件事的兩步版本：矩陣先給出 W 裡的 n 個向量，這些向量再給出整個映射。中間一條細線把兩種說法分開。

## Beat 8 — 推論：座標把方程算出來 / the corollary: coordinates give the equations
*配音長度：中文 18.0s ／ 英文 17.5s*

**畫面公式**

```
推論：座標把方程算出來   |   the corollary: coordinates give the equations
η  =  T ( ξ )      ⇔      yᵢ  =  Σ₁ⁿ tᵢⱼ xⱼ    ( i = 1 , … , m )
```

**旁白（繁中）**

> 推論把話講到底。設 x 是輸入的座標元組、y 是輸出的座標元組，那麼輸出等於映射作用在輸入上，充要條件就是那組純量方程成立。抽象的映射被那組方程完全取代。

**Narration (EN)**

> The corollary finishes the point. Let x be the coordinate tuple of the input and y that of the output. Then the output equals the map applied to the input exactly when those scalar equations hold. With bases chosen, the abstract map is replaced by the equations.

**動畫**

上下兩層。上層是抽象的：ξ 在 V 裡、沿 T 到 W 裡的 η。下層是可以算的：輸入的座標元組、陣列、輸出的座標元組，第二橫列被標出來對應到輸出的第二格。兩層之間用座標同構的向下箭頭接起來。

## Beat 9 — 矩陣永遠是相對於基底的 / a matrix is always with respect to bases
*配音長度：中文 16.8s ／ 英文 17.9s*

**畫面公式**

```
矩陣永遠是相對於基底的   |   a matrix is always with respect to bases
( T , β , γ )  ↦  { tᵢⱼ }        ( T , β ′ , γ ′ )  ↦  { t ′ᵢⱼ }  ≠  { tᵢⱼ }
```

**旁白（繁中）**

> 但有件事一定要記住：矩陣永遠是相對於選定的基底。座標空間上矩陣是映射的天然分身，一般空間上的映射自己沒有矩陣，是選了基底才有；換一組基底就換一個矩陣。

**Narration (EN)**

> But one thing has to be remembered: a matrix is always with respect to chosen bases. On Cartesian spaces a matrix is the natural alter ego of a map, but a map on a general space has no matrix of its own. Change the bases and the same map gets a different matrix.

**動畫**

最上面畫一次映射 T：V 到 W。底下兩個面板各自標著一組基底選擇，各自長出一個陣列，兩個陣列反白的格子位置不同，中間一個不等號。整張圖只有一個映射，卻有兩個矩陣。

## Beat 10 — 怎麼把矩陣元素讀出來 / how to read an entry off the map
*配音長度：中文 16.6s ／ 英文 18.0s*

**畫面公式**

```
怎麼把矩陣元素讀出來   |   how to read an entry off the map
t ₖⱼ  =  ε ₖ ( T ( βⱼ ) )        ε ₖ ( γᵢ )  =  δ ᵢₖ
```

**旁白（繁中）**

> 最後一條引理說怎麼把元素讀出來：用 W 的對偶基底去量，第 k 個對偶基底作用在第 j 個基底向量的像上，得到的就是第 k 列第 j 行那格。下一集講轉置、秩與乘法。

**Narration (EN)**

> A last lemma says how to read an entry off the map. Measure with the dual basis of W: apply the kth dual basis functional to the image of the jth basis vector, and the number you get is the entry in row k, column j. Next time: the transpose, rank and products.

**動畫**

左邊把像用 γ 基底展開；中間的箭頭是對偶基底 ε₂，它的作用就是讀出第二個係數；右邊那個數落進陣列裡第二橫列、第三直行的那一格，橫桿與豎桿在該格交叉。
