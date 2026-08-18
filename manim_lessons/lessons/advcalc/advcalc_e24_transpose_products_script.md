# advcalc E24 — 第 2 章：轉置、秩與矩陣乘法

Chapter 2: The Transpose, Rank and Matrix Products

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 4 節的中段（書頁 90–93）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e24_transpose_products.py`（`AdvCalcE24ZH` / `AdvCalcE24EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[24]` / `FORMULAS_ADVCALC[24]`）
- 配音：`manim_lessons/samples/audio_e24/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.34 分（201 秒）／英文 3.12 分（187 秒）

§4 的剩下部分（行向量看成矩陣、換基底、共變與逆變、Hom 的標準基底 D_kl，書頁 93–96）留給 E25；書頁 96–98 是習題，依 `docs/PLAYBOOK.md` 第 8 節不做解答。

符號沿用 E23：β 是 V 的基底、γ 是 W 的基底、ε 是 γ 的對偶基底。定理 4.3 還需要 V\* 的對偶基底（住在 V\*\* 裡），而依第 21 集那條引理那就是 β\*\*，所以不必再引進新字母。小寫的 t、s、r 是矩陣，大寫的 T、S、R 是它們來自的映射——所以 t\* 是轉置、T\* 是伴隨算子，而定理 4.3 講的正是這兩者的關係。定理 4.5 需要第三個空間，它的基底用 ρ，這個字母整個系列都還沒用過。

陣列的繪圖工具（方括號、點陣、文字行、方框）與 E23 共用 `manim_lessons/lessons/advcalc/arrays.py`。各檔各打一份正是這個系列踩過的坑。

---

## Beat 0 — 轉置：橫列與直行對調 / the transpose: rows and columns exchanged
*配音長度：中文 17.3s ／ 英文 17.0s*

**畫面公式**

```
轉置：橫列與直行對調   |   the transpose: rows and columns exchanged
t * ᵢⱼ  =  t ⱼᵢ        t  :  m × n        t *  :  n × m
```

**旁白（繁中）**

> 上一集把矩陣與線性映射對應起來了。這一集先看轉置：把橫列與直行對調，第 i 列第 j 行那一格，搬到第 j 列第 i 行。原來的橫列變成新的直行，反過來也一樣。

**Narration (EN)**

> The last episode matched matrices with linear maps. This one starts with the transpose: exchange the rows and the columns, so the entry in row i and column j moves to row j and column i. The old rows become the new columns and the other way round.

**動畫**

左右兩個陣列：左邊是 m 列 n 行，右邊是轉置後的 n 列 m 行。左邊的第一條橫列與右邊的第一直行用同一個顏色標出來，說明橫列變成了直行；另外挑一格用同一個記號在兩邊都標出來，兩個標記的位置都由同一組常數算出，所以圖上的指標不可能跟旁邊的標籤說不同的話。

## Beat 1 — 定理 4.3：轉置就是伴隨算子的矩陣 / theorem 4.3: the transpose is the adjoint's matrix
*配音長度：中文 17.3s ／ 英文 17.1s*

**畫面公式**

```
定理 4.3：轉置就是伴隨算子的矩陣   |   theorem 4.3: the transpose is the adjoint's matrix
T : V → W    ↦    t        T * : W * → V *    ↦    t *        ε ᵢ ( γⱼ ) = δ ᵢⱼ
```

**旁白（繁中）**

> 定理四點三說了一件漂亮的事。如果兩邊都用對偶基底來看，伴隨算子的矩陣就是原矩陣的轉置。轉置不是為了方便才定義的運算，它是伴隨算子在矩陣世界裡的長相。

**Narration (EN)**

> Theorem four point three says something rather nice. Read against the dual bases on both sides, the matrix of the adjoint is the transpose of the original matrix. The transpose is not an operation invented for convenience; it is what the adjoint looks like in matrix form.

**動畫**

上排是映射 T 與它的矩陣，下排是伴隨算子與它的矩陣。左邊看到的是箭頭反過來（V 到 W 變成 W 的對偶到 V 的對偶），右邊看到的是形狀反過來（m 列 n 行變成 n 列 m 行）。兩個「取星號」的箭頭把上下接起來，說這兩件事是同一件。

## Beat 2 — 證明：兩條路走到同一個數 / the proof: two routes to one number
*配音長度：中文 19.0s ／ 英文 17.0s*

**畫面公式**

```
證明：兩條路走到同一個數   |   the proof: two routes to one number
s ⱼᵢ  =  β ⱼ * * ( T * ( ε ᵢ ) )  =  ( ε ᵢ ∘ T ) ( βⱼ )  =  ε ᵢ ( T ( βⱼ ) )  =  t ᵢⱼ
```

**旁白（繁中）**

> 證明只是把兩條引理接起來。上一集那條說，矩陣元素等於對偶基底作用在基底向量的像上。把它用在伴隨算子身上，再用第二共軛空間那條把括號拆開，兩個指標就自己互換了。

**Narration (EN)**

> The proof only joins two lemmas. Last episode's says an entry is a dual basis vector applied to the image of a basis vector. Apply it to the adjoint, then use the second conjugate space to unwrap the brackets, and the two indices exchange themselves.

**動畫**

書上的證明是一串四個等號，直接畫出來就等於把公式列再寫一次。改成畫兩條路：上面那條從 V 的基底向量出發，走 T 到 W，再用對偶基底去量；下面那條從 W 的對偶基底出發，走伴隨算子到 V 的對偶空間，再用第二共軛的那組基底去量。兩條箭頭指向同一個被框起來的數。

## Beat 3 — 橫列空間與直行空間 / the row space and the column space
*配音長度：中文 17.8s ／ 英文 16.3s*

**畫面公式**

```
橫列空間與直行空間   |   the row space and the column space
t ʲ  ∈  ℝᵐ   ( j = 1 … n )        t ᵢ  ∈  ℝⁿ   ( i = 1 … m )
```

**旁白（繁中）**

> 接著定義兩個空間。矩陣的 m 條橫列各自是一個 n 元組，它們生成的叫橫列空間；n 個直行各自是一個 m 元組，生成的叫直行空間。兩個空間住在不同的地方，維數卻相同。

**Narration (EN)**

> Now two subspaces. The m rows of a matrix are each an n-tuple, and what they span is the row space. The n columns are each an m-tuple, and what they span is the column space. They live in different spaces and yet have the same dimension.

**動畫**

中間是陣列。橫列被逐條標出來，往左邊離開，落進一個橢圓；直行被逐行標出來，往右邊離開，落進另一個橢圓。兩個橢圓分別標著兩個不同的座標空間——刻意往相反方向離開，就是要說這兩個生成空間不住在同一個地方。

## Beat 4 — 直行空間就是值域 / the column space is the range
*配音長度：中文 16.7s ／ 英文 15.7s*

**畫面公式**

```
直行空間就是值域   |   the column space is the range
T ( δ ʲ )  =  t ʲ        L ( t ¹ , … , t ⁿ )  =  R ( T )
```

**旁白（繁中）**

> 為什麼相同？先看直行空間。第 j 直行正好是標準基底第 j 個向量的像，而基底的像會生成整個值域，所以直行空間根本就是映射的值域，維數就是映射的秩。

**Narration (EN)**

> Why the same? Take the column space first. The jth column is exactly the image of the jth standard basis vector, and the images of a basis span the whole range, so the column space simply is the range of the map, and its dimension is the rank.

**動畫**

左邊橢圓裡是標準基底的 n 個向量，沿著 T 的箭頭過去，右邊橢圓裡是 n 個行向量。右邊那個橢圓本身填了底色，代表它們生成的空間；因為基底的像生成值域，這塊底色就是值域本身。

## Beat 5 — 兩邊被夾成同一個數，這就是秩 / both sides squeeze onto one number: the rank
*配音長度：中文 19.2s ／ 英文 16.3s*

**畫面公式**

```
兩邊被夾成同一個數，這就是秩   |   both sides squeeze onto one number: the rank
d ( L ( t ₁ … t ₘ ) )  =  d ( R ( T * ) )  =  d ( R ( T ) )  =  d ( L ( t ¹ … t ⁿ ) )
```

**旁白（繁中）**

> 另一邊，轉置是伴隨算子的矩陣，所以轉置的直行空間維數就是伴隨算子的秩。但轉置的直行就是原矩陣的橫列。上一集之前證過伴隨算子與原映射同秩，兩邊就被夾成同一個數。

**Narration (EN)**

> On the other side, the transpose is the matrix of the adjoint, so the dimension of its column space is the rank of the adjoint. But the columns of the transpose are the rows of the original. The adjoint has the same rank, so both sides are squeezed onto one number.

**動畫**

四個方框排成一列，中間用等號連起來：最左邊是橫列空間的維數，最右邊是直行空間的維數，中間兩個是伴隨算子與原映射的值域維數。中間那一段用一條線與說明標出來，指明這一步是第 22 集證過的那條定理。兩端就這樣被夾成同一個數。

## Beat 6 — 乘法是從合成算出來的 / multiplication comes out of composition
*配音長度：中文 17.1s ／ 英文 16.4s*

**畫面公式**

```
乘法是從合成算出來的   |   multiplication comes out of composition
y ᵢ = Σ ₕ t ᵢₕ x ₕ        z ₖ = Σ ᵢ s ₖᵢ y ᵢ        z ₖ = Σ ₕ ( Σ ᵢ s ₖᵢ t ᵢₕ ) x ₕ
```

**旁白（繁中）**

> 這個共同的維數就叫矩陣的秩。接下來看乘法。取兩個可以先後合成的線性映射，把各自的純量方程代進去，把和的順序調換再整理，一組新的係數就自己冒出來。

**Narration (EN)**

> That common dimension is the rank of the matrix. Now multiplication. Take two linear maps that compose, substitute one set of scalar equations into the other, swap the order of summation and tidy up, and a new set of coefficients appears on its own.

**動畫**

從左到右是一條鏈：輸入的座標元組、矩陣 t、中間的元組、矩陣 s、輸出的元組。中間那個元組上方有一條虛線與一個向下的箭頭，表示把它代進去。元組的長度全部由 m、n、l 三個常數算出來，所以整條鏈的形狀一定接得起來。

## Beat 7 — 第 k 橫列與第 j 直行交會的地方 / where the kth row and the jth column cross
*配音長度：中文 18.0s ／ 英文 16.6s*

**畫面公式**

```
第 k 橫列與第 j 直行交會的地方   |   where the kth row and the jth column cross
r ₖⱼ  =  Σ ᵢ s ₖᵢ t ᵢⱼ        ( l × m ) · ( m × n )  =  ( l × n )
```

**旁白（繁中）**

> 那組係數就是乘積矩陣。第 k 列第 j 行那一格，是左邊矩陣第 k 橫列跟右邊矩陣第 j 直行的純量積。所以形狀必須對得上：左邊的行數要等於右邊的列數，否則配不起來。

**Narration (EN)**

> Those coefficients are the product matrix. The entry in row k and column j is the scalar product of the kth row of the left factor with the jth column of the right one. So the shapes have to agree: the left factor's columns must match the right factor's rows.

**動畫**

乘積的版面刻意排成 L 型：右邊的因子放在上面，左邊的因子放在旁邊，答案放在右下。左因子的第 k 橫列與答案的第 k 橫列共用同一個 y 座標，右因子的第 j 直行與答案的第 j 直行共用同一個 x 座標，所以標出來的那一列與那一行真的在標出來的那一格交會——那個交會點就是規則本身，不是畫上去的。

## Beat 8 — 代數律是繼承來的，不是驗證來的 / the algebraic laws are inherited, not checked
*配音長度：中文 18.9s ／ 英文 18.3s*

**畫面公式**

```
代數律是繼承來的，不是驗證來的   |   the algebraic laws are inherited, not checked
S ∘ T   ↦   s · t        ( R ∘ S ) ∘ T = R ∘ ( S ∘ T )    ⇒    ( r s ) t = r ( s t )
```

**旁白（繁中）**

> 重點在這裡：矩陣乘法不是先定義再回頭驗證性質，它根本就定義成「合成的那個矩陣」。既然對應保持乘法，合成滿足的代數律就自動被繼承。結合律不必算，它就是合成的結合律。

**Narration (EN)**

> Here is the point. Matrix multiplication is not defined first and then checked. It is defined to be the matrix of the composite. Since the correspondence preserves products, every algebraic law composition obeys is inherited at once. Associativity needs no computation.

**動畫**

左半邊是四個點與三個箭頭的合成鏈，底下兩個括號畫出兩種不同的分組方式，看得出兩種分組走的是同一條路。右半邊上方是合成的結合律，一個箭頭往下把它搬到矩陣的結合律，箭頭旁註明「同構保持乘法」——右邊那條不是驗證出來的，是搬過來的。

## Beat 9 — 定理 4.4：方陣構成一個代數 / theorem 4.4: the square matrices form an algebra
*配音長度：中文 18.9s ／ 英文 18.1s*

**畫面公式**

```
定理 4.4：方陣構成一個代數   |   theorem 4.4: the square matrices form an algebra
M ₙ  ≅  Hom ( ℝⁿ )        e ᵢⱼ  =  δ ᵢⱼ        ∃ t ⁻¹   ⇔   d ( R ( T ) ) = n
```

**旁白（繁中）**

> 定理四點四把這件事說完：所有方陣構成一個代數，自然同構於那個空間上所有線性變換所成的代數。單位映射的矩陣主對角線上是一、其他是零。而方陣可逆，若且唯若秩是滿的。

**Narration (EN)**

> Theorem four point four finishes this. The square matrices form an algebra naturally isomorphic to all linear transformations of the space. The identity gives the matrix with ones down the main diagonal, and a square matrix is invertible exactly when its rank is full.

**動畫**

左上是兩個方框與一個同構符號：所有方陣，與那個空間上所有線性變換。右邊畫出單位矩陣，主對角線上是一、其他是零；那些一是用「兩個指標相等」判出來的，不是逐格打上去的。左下一個方框寫著可逆的充要條件。

## Beat 10 — 定理 4.5 與 4.6：一般空間，與轉置 / theorems 4.5 and 4.6: general spaces, and transposes
*配音長度：中文 20.6s ／ 英文 18.1s*

**畫面公式**

```
定理 4.5 與 4.6：一般空間，與轉置   |   theorems 4.5 and 4.6: general spaces, and transposes
S ∘ T   ↦   s · t        ( s t ) *  =  t * s *
```

**旁白（繁中）**

> 最後兩條把結果推廣。定理四點五說，在一般空間上選好三組基底之後，合成的矩陣仍然是兩個矩陣的乘積。定理四點六說，乘積的轉置等於兩個轉置反過來相乘。下一集講行向量與換基底。

**Narration (EN)**

> Two last theorems generalise. Theorem four point five: with three bases chosen in general spaces, the matrix of a composite is still the product of the two matrices. Theorem four point six: the transpose of a product is the product of the transposes in the opposite order.

**動畫**

左邊三個空間排成一列，兩個箭頭是兩個映射，每個空間底下標著自己選定的基底；底下一條長箭頭是兩者的合成。右邊兩個方框：上面是合成對應到矩陣乘積，下面是乘積的轉置等於兩個轉置反過來相乘。順序反轉這件事，跟第 22 集伴隨算子那條是同一件事。
