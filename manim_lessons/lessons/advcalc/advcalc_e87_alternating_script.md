# advcalc E87 — 第 7 章：交錯張量與它的維數

Chapter 7: Alternating Tensors and Their Dimension

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 7 章第 5 節「The subspace 𝒜 ⁿ of alternating tensors」（書頁 310 下半到 312 上半），從兩個定義起，收在 n = m 那個特例。**第 7 章整章沒有習題。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e87_alternating.py`（`AdvCalcE87ZH` / `AdvCalcE87EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[87]` / `FORMULAS_ADVCALC[87]`）
- 配音：`manim_lessons/samples/audio_e87/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 263.1 秒（4:23）／英文 205.8 秒（3:25）
- YouTube（私人）：中文 https://youtu.be/ss8slBY4XOk ／英文 https://youtu.be/u0jHipfKPPQ

## 這半節在做什麼

**這一集是整章的軸心。** 第 2 節給了 n 階共變張量一組以「所有 n 元指標組」為索引的基底，
所以那裡的維數是 m ⁿ。第 5 節問的是其中哪些在變數被置換時只差一個正負號，
答案從 m ⁿ 塌縮成一個組合數。

兩個定義（書頁 310）：

```
f ( ξ ∘ σ )   =   f ( ξ )                        對稱
f ( ξ ∘ σ )   =   ( sgn σ )  f ( ξ )             交錯
```

**記號說明**：書上把置換作用寫成 f 的 σ 次方，但 Unicode 沒有上標的 σ
（最接近的修飾字母是 δ，那會在畫面上印出錯的字母），所以畫面一律照書上的定義式寫成
`f ( ξ ∘ σ )`。同理，索引本身是指標組時一律用括號帶，`c ( p )`、`ν ( q )`——Unicode 也沒有下標 q。

交錯的第一個後果立刻就看得出來：**兩個變數相同就是零**。把那兩個對換，值沒動，
可是按定義要變號，所以它等於自己的相反數。

**投影算子**（定理 5.1）：

```
( Ω f ) ( ξ )   =   ( 1 / n ! )  Σ  ( sgn σ )  f ( ξ ∘ σ )        ( σ ∈ S ₙ )
Ω  :  ( V * ) ⊗ ⁿ   →   𝒜 ⁿ                Ω ∘ Ω   =   Ω
```

證明兩件事：像一定交錯（用 sgn 的乘法性，加上 σ ↦ σ ∘ ρ 是雙射），
而本來就交錯的原封不動送回來（那時 n ! 項每一項都是原來的 f）。
**引理 5.1** 是同一個計算換個指標名字：

```
g ( ξ )  =  f ( ξ ∘ ρ )          ⇒          Ω g   =   ( sgn ρ )  Ω f
```

**係數的刻畫**（書頁 311 的核心）：

```
f  ∈  𝒜 ⁿ          ⟺          c ( p )   =   ( sgn σ )  c ( p ∘ σ )
```

於是兩個後果：p 有重複時拿那個對換去套，得到 c ( p ) = − c ( p )，所以是零；
而 **n > m 時根本沒有單射的 p**，所以 𝒜 ⁿ = { 0 }。

n ≤ m 時，單射的 p 按值域分類，同一類彼此只差一個置換，每類 n ! 個。
取值域遞增的那一個當代表（記作 C），於是

```
ν ( q )  =  Σ ( sgn σ ) μ ( q ∘ σ )  =  n ! Ω ( μ ( q ) )        f  =  Σ  c ( q )  ν ( q )
```

**定理 5.2**：

```
dim 𝒜 ⁿ   =   C ( m , n )   =   m !  /  ( n !  ( m − n ) ! )
```

**n = m 這個特例就是下一集的全部根據。** C 只剩恆等置換一個元素，所以 dim 𝒜 ᵐ = 1，而

```
f ( ξ ₁ , … , ξ ₘ )  =  c  Σ  ( sgn σ )  x ( 1 , σ ( 1 ) ) ⋯ x ( m , σ ( m ) )
```

書上說「這本質上就是行列式的公式」。E88 就把它認出來。

## 這一集用的例子

一個 m 維空間上的 n 階共變張量，在這裡就是陣列 c ( p ) = f ( α_p₁ , … , α_pₙ )。
置換作用實作成陣列的軸置換，而且**與逐點定義 f ^ σ ( ξ ) = f ( ξ ∘ σ ⁻ ¹ ) 對驗過**，
不是假設相等。所有殘差都是 Frobenius 範數——小整數係數下 sup 範數會飽和，
五個不同的置換會印出同一個數字，看起來像 bug 而不像證明。

| 要驗的事 | 結果 |
|---|---|
| 2 × 2 的對稱例子 `[[2,3],[3,-1]]` 真的對稱、且**不**交錯 | f ( ξ , η ) = 23，f ( η , ξ ) = 23 |
| 2 × 2 的交錯例子 `[[0,2],[-2,0]]` 真的交錯、且**不**對稱，對角線是零 | f ( ξ , η ) = −14，f ( η , ξ ) = +14 |
| n = m = 3 的交錯 f，三種重複方式都是零 | f ( ξ , ξ , η ) = f ( η , ξ , ξ ) = f ( ξ , η , ξ ) = f ( ζ , ζ , ξ ) = 0 |
| **但它不是零泛函** | f ( ξ , η , ζ ) = 53 |
| 取一個既不對稱也不交錯的 f（m = 4、n = 3） | ‖ f ‖ = 5.196，‖ Ω f ‖ = 1.683，‖ Ω f − f ‖ = 4.916 |
| **Ω f 對 S ₃ 全部六個 σ 都交錯** | 殘差全部 0.0e+00，而 f 自己是 0、7.211、8.124、7.874、7.874、6.928 |
| **Ω ( Ω f ) = Ω f** | 0.0e+00 |
| 引理 5.1 對全部六個 ρ 成立 | 全部 0.0e+00 |
| **把 sgn ρ 拿掉就不成立** | 三個奇置換全部 3.367 |
| m = 3、n = 2 的交錯係數 c ( p ) = sgn σ · c ( p ∘ σ ) | 九個 p 與兩個置換全部通過，對角線三個是零 |
| **n > m 時只有零**：m = 3，n = 4 與 5 | 單射的 p 有 0 個，dim 𝒜 ⁿ = 0 |
| m = 3，n = 1…5 的維數 | 單射 3、6、6、0、0 → \| C \| 與 dim 都是 3、3、1、0、0 |
| m = 4，n = 0…4 的維數 | 單射 1、4、12、24、24 → \| C \| 與 dim 都是 1、4、6、4、1 |
| **m = 2…5、n = 0…m 全部驗** `len(C) == comb(m, n)` | 全部通過 |
| 用線性方程組的秩獨立算一次維數 | 與 \| C \| 逐格相同（相鄰對換那個捷徑另外對全群驗過兩次） |
| m = 4、n = 2 的 ν ( q ) 全部交錯，且 = n ! Ω ( μ ( q ) ) | 殘差 < 1e-12 |
| 六個 ν ( q ) 在六個代表元上的取值矩陣 | **就是 6 × 6 單位矩陣**，rank = 6 |
| 任一交錯 f 由代表元上的係數還原 | 殘差 0.0e+00 |
| **n = m 時維數是 1** | m = 3 的 C 只有一個元素，生成元在標準基底上的值調成 1 |
| **第 11 拍的展開式 = numpy 的行列式** | Σ = 53，`numpy.linalg.det` = 53.000000，差 7.1e-15 |
| 那六項彼此不同（不是同一個數字印六次） | 8、−8、−1、−6、6、−36 |

最後一列是下一集的伏筆：**那個和式已經是行列式了**，只差一個名字。

## 這一輪抓到的錯

- **上標的 σ 根本不存在。** 原本照計畫把置換作用寫成 `f ᵟ`，但 U+1D5F 是**修飾字母小寫 delta**，
  畫面上會印出 f 的 δ 次方——字元畫得出來（DejaVu Sans 有），**但它說的是另一件事**。
  Unicode 沒有上標 σ。改成照書上的定義式寫 `f ( ξ ∘ σ )`，整集一致。
  **這是「字元查得到不等於字元是對的」**：E80 那次 `‴` 是缺字，這次是有字但是錯字。
- **下標 q 也不存在**（Unicode 的拉丁下標沒有 q）。`μ_q`、`ν_q`、`c_p` 一律改成括號帶索引。
- **八列的表最後一列會壓到 `_cap`。** 第 4、5、11 拍各八列，照 PLAYBOOK 用 `dy = 0.23`
  （落在 −0.71，`_cap` 在 −0.90）。
- **第 4 拍原本要塞九列。** 六個 σ、一列表頭、一列 Ω ( Ω f ) 的殘差，再加一列定義欄位，
  九列無論 `dy` 怎麼調都壓到說明話。改成**表頭兩列**（一列寫出殘差的式子、一列寫欄名），
  把 Ω ( Ω f ) − Ω f 那個數字移到左圖的自迴圈旁邊。
  起因是**一行就寫完的表頭會超過面板寬度**，而 `_sym` 是逐列各自縮放的，
  縮過的表頭就不再對準它所標示的欄。規則：**表頭不能縮，要縮就拆兩列。**
- **投影的例子原本取 m = 3、n = 3。** 那也確實既不對稱也不交錯，可是 m = 3 時 dim 𝒜 ³ = 1，
  Ω 會把它打到一條線上，「投影」看起來像「塌掉」。改成 m = 4、n = 3，
  目標空間是四維的，圖才誠實。
- **殘差原本用 sup 範數，五個置換印出同一個數字。** 小整數係數下 max 會飽和
  （六列裡有五列是 4.000），看起來像複製貼上的 bug。改成 Frobenius 範數之後
  是 7.211、8.124、7.874、7.874、6.928——其中兩個相同是因為那兩個是互為反元素的三輪換，
  不是巧合。
- **第 7 拍下面那個註記會被斜箭頭穿過。** 四個源點排到 x = −3.60，
  而 4 → 2 那支斜箭頭在註記上緣的高度上剛好還在 x = −3.93 附近。
  把下面那個註記從 `n = 4 > 3 = m` 縮成 `4 > 3`（它指的就是畫面上四個點對三個點），
  並把兩個註記都右移到 x = −2.95。
- **「畫成同一條」的風險點，這一集全部正面處理過**：
  對稱與交錯那兩個矩陣刻意取不同的非對角值（3 與 2），交錯的對角線是零；
  不同 n 的維數**不畫成曲線**，改成巴斯卡三角形加表格，
  因為 C ( 3 , n ) 與 C ( 4 , n ) 在 n = 0 處同值、畫成兩條線會在左端重合。
  第 4 拍的自迴圈是唯一一處刻意畫「回到原地」，它靠的是一個真的圈，不是兩個相同的方塊。

## 十一拍

### 第 1 拍 — 兩個定義：對稱與交錯 / two definitions: symmetric and alternating

公式列：

```
f ( ξ ∘ σ )   =   f ( ξ )              f ( ξ ∘ σ )   =   ( sgn σ )  f ( ξ )
```

中文旁白：這一節只做兩件事：先把對稱與交錯這兩個條件寫清楚，再算出交錯張量那個子空間的維數。對稱是說把變數依任何一個置換重排，值都不變；交錯是說值會乘上那個置換的正負號。雙線性的情形最好記：對稱就是交換兩個變數值不變，交錯就是交換之後變號。

English: This section does two things: it writes down what symmetric and alternating mean, and then it computes the dimension of the alternating subspace. Symmetric means the value survives any permutation of the arguments; alternating means it picks up the sign of that permutation.

### 第 2 拍 — 交錯：變數有重複就是零 / alternating: a repeated argument gives zero

公式列：

```
ξ ᵢ  =  ξ ⱼ   ,   i  ≠  j          ⇒          f ( ξ ₁ , … , ξ ₙ )   =   0
```

中文旁白：交錯有一個立刻就看得出來的後果：只要有兩個變數相同，值一定是零。理由是把那兩個相同的變數對換，一方面值完全沒變，另一方面按定義要乘上負一，於是那個值等於它自己的相反數，只能是零。右表最後一列不是零，所以這個泛函本身並不是零。

English: Alternating has one consequence you see at once: if two arguments are equal the value is zero. Swap those two. The value cannot change, yet by definition it must change sign, so it equals its own negative. The last row on the right is not zero, so this functional itself is not.

### 第 3 拍 — 投影算子 Ω / the projection operator

公式列：

```
( Ω f ) ( ξ )   =   ( 1 / n ! )  Σ  ( sgn σ )  f ( ξ ∘ σ )        ( σ ∈ S ₙ )
```

中文旁白：對稱的全體與交錯的全體都是子空間，而交錯那一個是後面整章要用的。更好的是，有一個線性算子可以把任意一個共變張量壓成交錯的：把它在每一個置換底下的樣子乘上那個置換的正負號，全部加起來，再除以 n 階乘。

English: The symmetric tensors and the alternating ones are both subspaces, and the alternating one is what this chapter needs. One linear operator flattens any covariant tensor into an alternating one: weight each permuted copy by its sign, add, and divide by n factorial.

### 第 4 拍 — 定理 5.1：它真的是投影 / theorem 5.1: it really is a projection

公式列：

```
Ω  :  ( V * ) ⊗ ⁿ   →   𝒜 ⁿ                Ω ∘ Ω   =   Ω
```

中文旁白：定理 5.1 說這個算子真的是一個投影，要驗的有兩件事。第一，它的像一定是交錯的，證明用正負號的乘法性，加上固定一個置換之後複合是雙射這個小事實。第二，本來就交錯的東西它原封不動送回來，因為那時每一項都等於原來那個泛函，一共 n 階乘項。

English: Theorem 5.1 says that operator really is a projection, and there are two things to check. Its image is always alternating, which needs the sign to be multiplicative and composition with a fixed permutation to be a bijection. And it returns an already alternating tensor untouched.

### 第 5 拍 — 引理 5.1：先重排再投影 / lemma 5.1: permute first, then project

公式列：

```
g ( ξ )  =  f ( ξ ∘ ρ )          ⇒          Ω g   =   ( sgn ρ )  Ω f
```

中文旁白：引理 5.1 是同一個計算的一個小變形：先用一個置換重排變數再投影，等於先投影再乘上那個置換的正負號。證明與上面那一段一字不差，只要把和式裡的指標換個名字。這一條在下一拍把係數的條件推出來的時候就會用到。

English: Lemma 5.1 is a small variant of the same computation: permuting the arguments and then projecting is the same as projecting and then multiplying by that permutation sign. The proof is word for word the one above, with the summation index renamed. The next beat needs it.

### 第 6 拍 — 把交錯翻譯成係數的條件 / alternating, as a condition on the coefficients

公式列：

```
f  ∈  𝒜 ⁿ          ⟺          c ( p )   =   ( sgn σ )  c ( p ∘ σ )
```

中文旁白：接下來把交錯翻譯成係數的語言。一個共變張量由它在基底組合上的那些係數完全決定，而交錯這個條件就等價於：把指標依任何一個置換重排，係數就乘上那個置換的正負號。左圖把九個係數排成格子，對角線上的三個必須是零，其餘六個兩兩差一個負號。

English: Now translate alternating into coefficients. A covariant tensor is fixed by its values on tuples of basis vectors, and alternating is exactly the condition that permuting the indices multiplies the coefficient by the sign. On the left the diagonal vanishes and the rest pair off.

### 第 7 拍 — 兩個後果：重複為零，n 大於 m 時全零 / two consequences: repeats vanish, and nothing survives past m

公式列：

```
p ᵢ  =  p ⱼ   ⇒   c ( p )  =  0              n  >  m   ⇒   𝒜 ⁿ  =  { 0 }
```

中文旁白：這個條件馬上給出兩個後果。第一，如果指標有重複，就拿對換那兩個位置的置換去套，得到係數等於它自己的相反數，所以是零。第二，當 n 比 m 大的時候，根本不存在沒有重複的指標組，所以每一個係數都是零——那個子空間只剩下零。

English: Two consequences follow at once. If an index repeats, apply the transposition swapping those two places and the coefficient equals its own negative, hence zero. And once n exceeds m no tuple avoids a repeat, so every coefficient vanishes and the subspace collapses to zero.

### 第 8 拍 — n 不超過 m 時怎麼數 / counting when n does not exceed m

公式列：

```
p   =   q ∘ σ              q ₁  <  q ₂  <  ⋯  <  q ₙ              σ  ∈  S ₙ
```

中文旁白：剩下 n 不超過 m 的情形。把所有單射的指標組按值域分類：值域相同的那一群彼此只差一個置換，每一群恰好 n 階乘個。每一群裡挑出把值域由小排到大的那一個當代表，於是代表元的集合與從 m 個元素裡取 n 個的子集一一對應。

English: That leaves n at most m. Sort the injective tuples by their range: those with the same range differ by a permutation, so each class holds exactly n factorial of them. Take the one whose range is listed in increasing order, and the representatives match the n element subsets.

### 第 9 拍 — 代表元造出來的那組基底 / the basis the representatives build

公式列：

```
ν ( q )  =  Σ ( sgn σ ) μ ( q ∘ σ )  =  n ! Ω ( μ ( q ) )      ( σ ∈ S ₙ )
```

中文旁白：對每個代表元造一個張量：把它在所有置換底下的基底元素乘上正負號加起來，那正好是 n 階乘倍的投影，所以一定是交錯的。而任何一個交錯張量都能唯一寫成它們的線性組合，係數就是原來那些代表位置上的係數。所以這一族就是一組基底。

English: Each representative builds a tensor: add up its basis elements over all permutations, weighted by the sign, which is n factorial times the projection, so it is alternating. Every alternating tensor is uniquely a combination of these, with coefficients read off the representatives.

### 第 10 拍 — 定理 5.2：維數就是組合數 / theorem 5.2: the dimension is the binomial coefficient

公式列：

```
dim 𝒜 ⁿ   =   C ( m , n )   =   m !  /  ( n !  ( m − n ) ! )
```

中文旁白：於是定理 5.2：交錯張量子空間的維數，就是從 m 個裡取 n 個的組合數。算法是先數單射的個數，從 m 開始連乘 n 個遞減的因子，再除以每一群裡的 n 階乘。右表下面兩列用兩種完全不同的算法，得到同一組數字。

English: Hence Theorem 5.2: the alternating subspace has dimension the number of ways of choosing n things out of m. Count the injective tuples first, a product of n decreasing factors starting at m, then divide by the n factorial in each class. The last two rows agree by two routes.

### 第 11 拍 — n = m：維數是 1，而那就是行列式 / n equal to m: dimension one, and that is the determinant

公式列：

```
f ( ξ ₁ , … , ξ ₘ )  =  c  Σ  ( sgn σ )  x ( 1 , σ ( 1 ) ) ⋯ x ( m , σ ( m ) )
```

中文旁白：最後是 n 等於 m 這個特例。這時候代表元只剩一個，維數就是一。把係數調成一，展開式就是對所有置換求和，每一項是正負號乘上一串座標的乘積，每個變數各出一個，而且行與列都不重複。書上說這本質上就是行列式的公式，下一集就把它認出來。

English: Last comes n equal to m. A single representative is left, so the dimension is one. Set the coefficient to one and the expansion is a sum over all permutations of a sign times a product of coordinates, one from every row and column. The book calls this essentially the determinant.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 左右兩個 2 × 2 數值格子（對稱／反對稱），各畫一條對角虛鏡；右表最後兩列是 f ( ξ , η ) 與 f ( η , ξ ) 的實際值，上面一列相同、下面一列差正負號 |
| 2 | ⟨ ξ , ξ , η ⟩ 三個方塊，前兩個同色（它們真的是同一個向量），上面一對反向箭頭表示對換；底下三行把 f = − f 推到 f = 0 |
| 3 | ( V * ) ⊗ ⁿ → 𝒜 ⁿ 兩個方塊，Ω 標在箭頭上；底下把 S ₃ 的六個置換列成兩欄，加號青色、減號紅色 |
| 4 | 𝒜 ⁿ 畫成一條橫線，f 在線外、Ω f 在線上，一支垂直箭頭是投影；**Ω f 底下掛一個自迴圈**表示再投影一次停在原地。右表兩欄是 f 與 Ω f 各自的交錯誤差 |
| 5 | f / g / Ω f / Ω g 四個方塊圍成一個方塊圖，上面標 · ∘ ρ、下面標 × ( sgn ρ )、兩側標 Ω。右表右欄只有三個奇置換不是零 |
| 6 | m = 3、n = 2 的九個係數排成格子，對角線三格紅色（都是零），三條不同顏色的虛線各連一對差負號的；顏色與右表三列對應 |
| 7 | 上下兩個箭頭圖：上面 3 個位置送進 3 個指標但刻意撞在一起，下面 4 個位置送進 3 個指標、非撞不可。撞到的箭頭與靶點都是紅的 |
| 8 | m = 4、n = 2 的六個子集排成六欄（實心點表示選中），每欄底下掛它的 2 個排法；底下 6 × 2 = 12 |
| 9 | 六個 ν ( q ) 在六個代表元上的 6 × 6 取值矩陣，對角線橘色的 1、其餘灰色的 0 |
| 10 | 巴斯卡三角形第 0 到第 5 列，**第 4 列整列橘色**（就是右表在數的那一列）；底下附 C ( 4 , n ) 與它們的和 2 ⁴ |
| 11 | 3 × 3 的數值矩陣，σ = ⟨ 3 , 1 , 2 ⟩ 選到的三格橘色、用虛線串起來（每行每列各一個）；右表四欄是 σ、sgn σ、乘積、帶號的那一項（**Σ 加的是最後那一欄**），那一項印成橘色，最後一列把 Σ 與 numpy 的行列式並排 |
