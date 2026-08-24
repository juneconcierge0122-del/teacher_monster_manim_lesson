# advcalc E28 — 第 2 章：初等矩陣、反矩陣與行列式

Chapter 2: Elementary Matrices, Inverses and Determinants

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 6 節的後段（書頁 105–109）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e28_elementary_matrices.py`（`AdvCalcE28ZH` / `AdvCalcE28EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[28]` / `FORMULAS_ADVCALC[28]`）
- 配音：`manim_lessons/samples/audio_e28/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.16 分（189 秒）／英文 3.25 分（195 秒）

§6 的內容收在書頁 109 上半，書頁 109 起是習題 6.1–6.20（一路排到 111），依 `docs/PLAYBOOK.md` 第 8 節不做解答。第 7 節「二次型的對角化」從書頁 111 起，是 E29。

## 這一集的兩個範例都是自己的，而且都是算出來的

書上第 106–108 頁用同一個 2×2 矩陣示範反矩陣與行列式，並在第 106 頁畫了 Fig 2.5。依第 8 節，三者都自己重做，而且各自要**多做一件事**。

**反矩陣的例子**改成 `[[1, 2], [3, 5]]`：三步化到 e，而且從頭到尾不出現分數（書上那個例子的第二個初等矩陣是 [[1, 0], [0, −1/2]]，反矩陣裡也有 3/2 與 −1/2），所以觀眾的注意力可以留在「哪一步對應哪一個初等矩陣」上。三個初等矩陣、它們的乘積 b、以及 a | e 的增廣鏈，全部是模組載入時算出來的。

**行列式的例子**改成 `[[0, 1, 2], [1, 1, 1], [2, 0, 3]]`：第一列的階是 2，所以那個帶變號的對調 ( 1′ ) **是真的必須用上**，不是講講而已；整條鏈仍然全是整數。最後一拍的奇異例子 `[[0, 1, 2], [1, 1, 1], [1, 0, -1]]` 與它只差最後一列，半簡化形的最後一列歸零、對角線出現 0，行列式因此是 0。

**Fig 2.5** 的示意畫法（一條對角線加幾個記號）改成把三個矩陣的數字整個畫出來，因為這一拍要看的正是「其餘位置跟 e 一模一樣」。

場景檔頂端把旁白宣稱的事寫成 `assert`，其中最要緊的一條是這一集的立論本身：

```python
for _op in (("swap", I0, J0), ("scale", I0, CVAL), ("add", I0, J0, XVAL)):
 assert _mul(_elem(N_FIG, _op), _probe) == _apply(_probe, _op)
 assert _mul(_elem(N_FIG, _op), _elem(N_FIG, _undo(_op))) == _e(N_FIG)
```

也就是「把運算施在 e 上得到的矩陣，左乘任何矩陣都會做出同一個運算」與「三對初等矩陣互為反矩陣」這兩件事，是驗過的而不是寫上去的。
另外還驗了：反矩陣的例子確實化到 e、b 乘 a 等於 e、全程不出現分數、a | e 的右半邊確實等於 b、半簡化形的對角線乘積等於用定義算出的行列式。

---

## Beat 0 — 元組當直行看，變換就是左乘 / tuples as columns, transformations as multiplication
*配音長度：中文 17.2s ／ 英文 17.3s*

**畫面公式**

```
元組當直行看，變換就是左乘   |   tuples as columns, transformations as multiplication
y  =  a · x        A  ∈  Hom ( ℝⁿ , ℝᵐ )        y ᵢ  =  Σ ⱼ a ᵢⱼ x ⱼ
```

**旁白（繁中）**

> 上一集用消去法解決了基底與維數，還剩行列式與反矩陣。這一節先換個看法：把元組寫成一條直行，線性變換就是左乘矩陣。那麼列運算在這個看法下是什麼？

**Narration (EN)**

> Last time elimination settled a basis and a dimension; determinants and inverses are still open. This section changes the picture first: write a tuple as a column and a linear transformation is multiplication by a matrix. So what is a row operation in that picture?

**動畫**

左邊一個 3×4 的點陣是 a，乘上一條 4 格的直行 x，等於一條 3 格的直行 y。右邊三行說明把元組直著寫之後，線性變換就只是左乘一個矩陣。這是接下來整節的看法。

## Beat 1 — 把運算施在 e 上，就得到 u / do the operation to e and out comes u
*配音長度：中文 15.5s ／ 英文 16.7s*

**畫面公式**

```
把運算施在 e 上，就得到 u   |   do the operation to e and out comes u
u · a  =  ( u · e ) · a        ⇒        u  =  u · e
```

**旁白（繁中）**

> 答案是：每一個初等列運算都等於左乘一個初等矩陣 u。怎麼找出 u？因為 u 乘 a 等於 u 乘 e 再乘 a，只要把那個運算施在單位矩陣 e 上，跑出來的就是 u。

**Narration (EN)**

> The answer: every elementary row operation is premultiplication by an elementary matrix u. How do you find u? Since u times a is u times e, times a, you can simply perform the operation on the identity matrix e, and what comes out is u itself.

**動畫**

左邊 e，一個標了 ( 3 ) 的箭頭指到右邊的 u：兩個矩陣只差 i₀ 列 j₀ 行那一格，那一格被箭頭指著。上方的方框寫出正在做的那一個運算，公式列則是 u · a = ( u · e ) · a。

## Beat 2 — 三種初等矩陣 / the three elementary matrices
*配音長度：中文 15.8s ／ 英文 18.6s*

**畫面公式**

```
三種初等矩陣   |   the three elementary matrices
u ᵢ₀ⱼ₀ = u ⱼ₀ᵢ₀ = 1        u ᵢ₀ᵢ₀ = c        u ᵢ₀ⱼ₀ = x
```

**旁白（繁中）**

> 三種運算給出三種初等矩陣。對調兩列，就是把 e 的那兩列對調；某一列乘上 c，就是把對角線上那個一換成 c；加上第 j 列的 x 倍，就是在 i 列 j 行填進 x。

**Narration (EN)**

> Three operations, three elementary matrices. Interchanging two rows interchanges those rows of e; multiplying a row by c replaces that one on the diagonal by c; adding x times row j to row i puts x into the i, j place. Everywhere else they agree with e.

**動畫**

三個 4×4 的矩陣並排，分別是把三種運算施在 e 上算出來的結果：對調型的兩個 1 換了位置、伸縮型的對角線上換成 c、加倍型的 i₀ 列 j₀ 行填進 x。每個矩陣左邊標 i₀、上方標 j₀。書上 Fig 2.5 是用一條對角線加幾個記號的示意圖，這裡改成把數字本身畫出來，因為要看的就是「其餘位置跟 e 一樣」這件事。

## Beat 3 — 它們的反矩陣還是同一型 / each inverse is elementary of the same kind
*配音長度：中文 18.1s ／ 英文 17.6s*

**畫面公式**

```
它們的反矩陣還是同一型   |   each inverse is elementary of the same kind
( 1 ) ⁻¹ = ( 1 )        c  ↔  1 / c        x  ↔  − x
```

**旁白（繁中）**

> 這些初等矩陣都是非奇異的，反矩陣還是同一型。對調自己就是自己的反；乘上 c 的反是乘上 c 分之一；加 x 倍的反是加負 x 倍。影片乘出其中一對，三對程式都驗過。

**Narration (EN)**

> These elementary matrices are all nonsingular, and each inverse is elementary of the same kind. An interchange is its own inverse; multiplying by c is undone by multiplying by one over c; adding x times a row is undone by adding minus x times it.

**動畫**

左邊三個方框把三種運算與它的反運算配成對。右邊實際乘出第三型的那一對：u 乘 u⁻¹ 等於 e，兩個被動到的格子用高亮標出來。另外兩對在模組的 assert 裡驗過。

## Beat 4 — 一串運算就是一串左乘 / a sequence of operations is a sequence of products
*配音長度：中文 15.8s ／ 英文 17.0s*

**畫面公式**

```
一串運算就是一串左乘   |   a sequence of operations is a sequence of products
b  =  u ᵖ · u ᵖ⁻¹ · … · u ¹        r  =  b · a
```

**旁白（繁中）**

> 一整串運算就對應一整串左乘。把這些初等矩陣按順序乘起來寫成 b，b 乘 a 就是整串運算做在 a 上的結果；若這串運算把 a 化成階梯形 r，那 r 就等於 b 乘 a。

**Narration (EN)**

> A sequence of operations corresponds to a sequence of premultiplications. Multiply those elementary matrices in order and call the product b; then b times a is the whole sequence done to a. If the sequence row reduces a, then r equals b times a.

**動畫**

上排是 a 經過 u¹ 到 uᵖ 一路變成 r 的鏈，每個箭頭上標著當時做的那一個初等矩陣。下排是乘積 b，順序反過來寫：uᵖ 在最左、u¹ 在最右。中間的虛線把上排的每一個 u 連到它在乘積裡的位置，四條線交叉在一起——這個交叉就是「先做的排在最右邊」。

## Beat 5 — 方陣非奇異時，化簡的終點是 e / for a nonsingular square matrix the reduction ends at e
*配音長度：中文 17.0s ／ 英文 18.8s*

**畫面公式**

```
方陣非奇異時，化簡的終點是 e   |   for a nonsingular square matrix the reduction ends at e
d ( V ) = m        1 ≤ n ₁ < … < n ₘ ≤ m        ⇒   n ᵢ = i
```

**旁白（繁中）**

> 現在讓 a 是方陣而且非奇異。列空間的維數是 m，於是有 m 個階，嚴格遞增又落在一到 m 之間，只能排成一二三到 m。每個樞紐直行都是標準基底，所以 r 就是 e。

**Narration (EN)**

> Now let a be square and nonsingular. Its row space has dimension m, so there are m orders, increasing and all between one and m, which leaves only one, two, three up to m. Every pivot column is a standard basis vector, so r is the identity matrix e.

**動畫**

左邊一條刻著 1 到 m 的線，每個位置底下標著 nᵢ：m 個階、嚴格遞增、又都落在這 m 個位置裡，排法只有一種。箭頭指到右邊的 5×5 單位矩陣，對角線高亮。

## Beat 6 — 一個例子：三步走到 e / one example: three steps to e
*配音長度：中文 17.3s ／ 英文 18.8s*

**畫面公式**

```
一個例子：三步走到 e   |   one example: three steps to e
b · a  =  e        b  =  a ⁻¹
```

**旁白（繁中）**

> 既然 b 乘 a 等於 e，b 就是 a 的反矩陣。消去法把 a 化成 e 的同時，也把反矩陣造了出來。影片用一個自己挑的二乘二例子：三步化到 e，三個初等矩陣乘起來就是它。

**Narration (EN)**

> Since b times a is e, b is the inverse of a. In reducing a to e, elimination has built the inverse along the way. The video runs a two by two example of its own: three steps down to e, and the three elementary matrices multiplied together are exactly the inverse.

**動畫**

上排是 [[1,2],[3,5]] 三步化成 e 的鏈；每個箭頭底下用虛線接著當時那一個初等矩陣（也是算出來的）。最下面把三個乘起來得到 b，正好是 a 的反矩陣。這個例子是自己挑的，挑的條件是全程不出現分數。

## Beat 7 — 把 e 貼在右邊，一起化簡 / put e alongside and reduce them together
*配音長度：中文 15.5s ／ 英文 18.0s*

**畫面公式**

```
把 e 貼在右邊，一起化簡   |   put e alongside and reduce them together
a | e        →        e | b
```

**旁白（繁中）**

> 不過真要算有更省事的做法：因為 b 乘 e 就是 b，把同一串運算施在 e 上就直接得到 b。把 e 貼在 a 右邊一路化簡，左半邊變成 e 時，右半邊就是反矩陣。

**Narration (EN)**

> For actual work there is a tidier way. Since b times e is b, performing the same sequence on e alone already delivers b. Put e to the right of a as one matrix and row reduce; by the time the left half is e, the right half is the inverse, ready to read off.

**動畫**

同樣三步，但矩陣是 2×4 的 a | e，中間一條虛線分隔左右半邊。最後一個矩陣左半邊是 e、右半邊高亮，就是反矩陣。與上一拍對照：同一串運算，右半邊自動記錄了它們的乘積。

## Beat 8 — 算行列式只用兩種運算 / determinants use only two operations
*配音長度：中文 20.1s ／ 英文 17.3s*

**畫面公式**

```
算行列式只用兩種運算   |   determinants use only two operations
( 1′ )  α ᵢ ↔ α ⱼ  ,  α ⱼ → − α ⱼ            ( 3 )  α ᵢ → α ᵢ − x α ⱼ
```

**旁白（繁中）**

> 最後是行列式。這裡改用兩種運算：對調兩列、同時把搬下去的那一列變號；以及減去別列的倍數。這兩種都不改變行列式。注意這回不把首項除成一，那個運算會把行列式乘上一個數。

**Narration (EN)**

> Finally determinants. Here we use two operations: interchange two rows and at the same time change the sign of the one moved down; and, as before, subtract a multiple of another row. Neither changes the determinant. We do not divide by leading entries now.

**動畫**

( 1′ ) 與 ( 3 ) 兩個方框亮著，( 2 ) 那個是暗的，旁邊寫明為什麼不用它——它會把行列式乘上 c。

## Beat 9 — 半簡化形與對角線的乘積 / the semireduced form and the product down its diagonal
*配音長度：中文 18.7s ／ 英文 16.2s*

**畫面公式**

```
半簡化形與對角線的乘積   |   the semireduced form and the product down its diagonal
Δ ( a )  =  Δ ( s )  =  Π ᵢ₌₁ᵐ  s ᵢᵢ
```

**旁白（繁中）**

> 做到底得到的矩陣叫半簡化形：每個樞紐直行只剩自己那個首項係數。它的行列式跟原來一樣，而它幾乎是對角的，行列式就是對角線上那些數相乘。影片的例子真的用上了一次對調。

**Narration (EN)**

> Carried through, that leaves a matrix called semireduced: each pivot column keeps only its own leading coefficient. Its determinant is the one we started with, and being nearly diagonal, that determinant is the product of the numbers down the diagonal.

**動畫**

五個 3×3 矩陣的鏈，箭頭上標著 ( 1′ ) 或 ( 3 )。第一步真的是對調，因為這個例子第一列的階是 2；被搬下去的那一列整列變號。最後一個矩陣的對角線高亮，底下的方框寫出對角線相乘等於行列式。整條鏈與那個等號都是模組用 Fraction 算出來、並與行列式的定義核對過的。

## Beat 10 — 可逆，當且僅當行列式不是零 / invertible if and only if the determinant is not zero
*配音長度：中文 18.3s ／ 英文 18.8s*

**畫面公式**

```
可逆，當且僅當行列式不是零   |   invertible if and only if the determinant is not zero
a · a ⁻¹  =  e        ⇔        Δ ( a )  ≠  0
```

**旁白（繁中）**

> 如果 a 是奇異的，維數小於 m，半簡化形最後一列全是零，對角線上出現零，乘積是零。合起來就是這一節的結論：方陣可逆，當且僅當行列式不是零。下一集進第 7 節。

**Narration (EN)**

> If a is singular the dimension is less than m, the last row of the semireduced matrix is zero, a zero appears on the diagonal and the product vanishes. So: a square matrix is invertible if and only if its determinant is not zero. Next time, section seven.

**動畫**

左右兩組：各自是原矩陣與它的半簡化形，原矩陣的最後一列高亮（兩個例子只差這一列），半簡化形的對角線高亮。左邊行列式是 −5、右邊是 0。底下一個方框把三件事寫成等價：維數等於 m、行列式不為零、反矩陣存在。

**這一拍有一段書上的論證沒有放進來。** 非奇異的情形，書上是用第 5 節列的行列式性質 (c)(d) 說明 Δ 等於那些首項係數的乘積；奇異的情形則需要多一步——對半簡化形再做幾次**行**運算（等於右乘型 (2) 的初等矩陣，同樣不改變行列式）把最後一直行清成零，才由性質 (c) 得到 Δ = 0。三分鐘的導讀只講結論：對角線乘積就是行列式，奇異時是零。旁白沒有宣稱那是顯然的。
