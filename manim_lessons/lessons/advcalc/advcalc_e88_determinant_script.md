# advcalc E88 — 第 7 章：行列式

Chapter 7: The Determinant

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 7 章第 6 節「行列式」（書頁 312–315），從 §6 的開頭到 Cramer 法則那一行為止。**第 7 章整章沒有習題**，所以這一節收在 Cramer 法則，後面直接接 §7。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e88_determinant.py`（`AdvCalcE88ZH` / `AdvCalcE88EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[88]` / `FORMULAS_ADVCALC[88]`）
- 配音：`manim_lessons/samples/audio_e88/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 238.0 秒（3:58）／英文 195.9 秒（3:15）
- YouTube（私人）：中文 https://youtu.be/63uYiZdExMU ／英文 https://youtu.be/kokcmYr2efU

## 這一節在做什麼

**整節只靠上一集的一個數字。** §5 算出交錯 m 重形式那個空間的維數是 m 取 m，也就是一：

```
dim 𝒜 ᵐ   =   1            D ( δ ¹ , … , δ ᵐ )   =   1
```

所以 ℝ ᵐ 上的交錯 m 重線性泛函差一個純量倍只有一個，再要求它在標準基底上取值等於一，就把它完全定死。那個唯一確定的形式就是**行列式** D；一個矩陣的行列式，就是 D 在它那 m 條直行上的值。剩下的整節，是第 2 章列過的每一條行列式性質一條一條被兌現。

**引理 6.1** 把它寫成顯式公式——從每一條直行各取一個元素、彼此落在不同橫列，乘起來再配上重排的奇偶號，全部加總：

```
D ( t )  =  Σ  ε ( σ )  t σ ( 1 ) , 1  ⋯  t σ ( m ) , m            σ  ∈  S ₘ
```

**推論 1** 說轉置不改變它：把乘積的因子依橫列指標重排，用的是原排列的反排列，而取反排列是 S ₘ 上的一對一對應、奇偶性又不變，所以整個和原封不動。**推論 2** 立刻跟著來——既然轉置無關，對直行交錯多重線性就等於對橫列也交錯多重線性。

接著是**不依賴基底**的那個行列式。取任何一個不是零的交錯 m 形式 f，把 T 先作用在每個輸入上：

```
f ₜ ( ξ ₁ , … , ξ ₘ )  =  f ( T ξ ₁ , … , T ξ ₘ )  =  Δ ( T )  ·  f ( ξ ₁ , … , ξ ₘ )
```

出來的還是一個交錯 m 形式，所以是 f 的常數倍；而因為那個空間一維，那個常數**與選哪個 f 無關**，它就是 Δ ( T )。**定理 6.1** 的證明只有兩行：

```
Δ ( S  ∘  T )   =   Δ ( S )   ·   Δ ( T )
```

**定理 6.2** 說相似變換的 Δ 相同，三個推論一起落地：矩陣的 D 等於它代表的變換的 Δ、矩陣乘積的 D 等於兩個 D 相乘，以及最有用的一條：

```
D ( t )   =   0        ⟺        t   奇異
```

要把第 2 章剩下的性質補齊，靠的是兩個**降階**引理。**引理 6.2**：最後一條直行是 δ ᵐ 時，行列式等於劃掉最後一橫列與最後一直行之後那個小矩陣的行列式——注意前提只要求**直行**，被劃掉那一橫列的其他元素根本進不了答案。**引理 6.3** 把它翻成變換的話：T 在補空間 X 上是恆等時，Δ 可以只在 Y 裡面算。

降階引理一到手，**定理 6.3**（餘因子展開）就是把第 r 條直行寫成 δ ⁱ 的組合再逐項套用引理：

```
D ( t )   =   Σ ᵢ  ( − 1 ) ⁱ ⁺ ʳ  t ᵢ ᵣ  D ( ( t ) ⁱ ʳ )
```

把其中的元素換成**另一條**直行上的，那個和是零——因為它等於一個有兩條直行相同的矩陣的行列式。兩件事合成一條，就是餘因子矩陣與反矩陣：

```
Σ ᵢ  c ᵢ ᵣ  t ᵢ ₛ   =   δ ᵣ ₛ  ·  D ( t )            s ᵣ ᵢ   =   c ᵢ ᵣ  /  D ( t )
```

最後是 **Cramer 法則**：把第 j 條直行換成右手邊那個向量，

```
x ⱼ   =   d ⱼ  /  D ( t )            t  ·  x   =   y
```

算出來的行列式除以原行列式，就是解的第 j 個座標。書上說這在第 2 章第 5 節用別的記號講過了。

## 這一集用的例子

畫面上每一個數字都由模組層算出來並 `assert` 釘住，而**顯示用的值與檢查用的值不共用任何程式碼**：螢幕上的數來自 `dexp`（照引理 6.1 對 m! 個排列硬加，`sgn` 數逆序對），檢查用的來自 `numpy.linalg.det` 與 `numpy.linalg.solve`（LU 分解，不經過任何餘子式）。「公式自己算出來的數等於自己」什麼也證不了，所以下表凡是標**獨立對照**的那幾列，才是這一集真正的保證。

| 要驗的事 | 結果 |
|---|---|
| 3 × 3 的六項顯式和 | +8 , +20 , +1 , +15 , −2 , +12 → Σ = +54 |
| **獨立對照**：同一個 3 × 3 的 `numpy.linalg.det` | 54.00000000000001 |
| **獨立對照**：隨機 3 × 3、4 × 4（seed 88）顯式公式 vs `det` | 5.6e−17 , 1.1e−16 |
| **獨立對照**：同兩個隨機矩陣的轉置 vs `det` | 8.3e−17 , 2.5e−16 |
| 轉置不變（整數例） | D ( t ) = +54，D ( t ᵀ ) = +54，而 max \| t − t ᵀ \| = 7 |
| 交錯性：對調兩條橫列 | −54（= − D） |
| 交錯性：某一橫列乘 c = 2.5 | +135.0（= c · D） |
| 交錯性：某一橫列加 k = 3 倍的另一條 | +54（不變） |
| k ᵀ 與 f 無關（c = +2.5 與 −0.8） | f ₜ / f = 2.000000 與 2.000000，都等於 Δ ( T ) = +2 |
| Δ ( S ∘ T ) = Δ ( S ) Δ ( T ) | +13 · +54 = +702，而 Δ ( S ∘ T ) = +702 |
| 相似不變 Δ ( θ ∘ T ∘ θ ⁻ ¹ ) | 54.000000 |
| **奇異 ⟺ D = 0**：第三橫列 = 第一橫列 + 2 × 第二橫列 | D = 0.0e+00，rank = 2 |
| 對照的可逆矩陣 | D = +54，rank = 3 |
| 引理 6.2 的降階（4 × 4 最後一直行是 δ ⁴） | D ( t ) = 54.000000，左上 3 × 3 的 D ( s ) = 54.000000 |
| **被劃掉那一橫列的其他元素不影響** | [ 5  −2  3 ] → [ −4  6  −9 ]，D 仍是 54.000000 |
| 餘因子展開：沿第 1 直行 | +12 , +0 , −13 , −159 → Σ = −160 |
| 餘因子展開：沿第 2 直行 | −32 , −144 , −16 , +32 → Σ = −160 |
| 餘因子展開：沿第 3 直行 | −2 , −34 , −124 , +0 → Σ = −160 |
| 餘因子展開：沿第 4 直行 | −138 , +18 , −7 , −33 → Σ = −160 |
| **四條直行的展開彼此相同，且獨立對照 `det`** | 四個都是 −160，\| Δ \| ≤ 5.7e−14 |
| **推論 1**：( r , s ) = ( 1 , 2 )，s ≠ r 時的和 | 0.0e+00 |
| **推論 1**：( r , s ) = ( 2 , 3 )，s ≠ r 時的和 | 0.0e+00 |
| 餘因子矩陣：c ᵀ · t 與 D ( t ) · I 逐格比對 | \| Δ \| ≤ 0.0e+00 （對角線四格都是 −160） |
| **獨立對照**：c ᵀ / D ( t ) vs `numpy.linalg.inv` | \| Δ \| ≤ 5.6e−17 |
| Cramer 的三個 d ⱼ | +54 , −54 , +108（y = [ 9  −7  −4 ]） |
| **獨立對照**：Cramer 的解 vs `numpy.linalg.solve` | x = +1 , −1 , +2，逐項差 ≤ 0.0e+00 |

整數矩陣是故意的：讀者可以把右表任何一列用手算核一次。但整數會讓很多抵消「剛好」是零，所以另外帶了一對 seed 88 的隨機矩陣，讓顯式公式在沒有漂亮數字的地方也與 `numpy.linalg.det` 對一次。

## 這一輪抓到的錯

- **`sgn` 不在 `langscan` 的白名單裡，而正負號非寫不可。** `_sym` 與 `FORMULAS` 必須語言無關，任何兩個以上的連續拉丁字母都會被擋下來。所以畫面上的符號函數一律寫成 `ε ( σ )`，「sgn」只活在旁白的白話裡。同一條規則也咬到另外兩處：`Cramer` 只能放進雙語的 `MODE_LABEL`，「singular」改寫成 `ker ( t ) ≠ 0`（`ker` 在白名單裡），意思一樣而且更精確。
- **拍序計畫把餘因子展開寫成「沿某一列展開」，與它自己的 assert 清單（「沿第 1、2、3 行」）相反。**書上定理 6.3 是沿**直行**往下走：i 跑的是橫列、r 固定一條直行。整集一律改用「直行／橫列」這組不會被兩岸慣例弄反的講法，和 localization 裡既有的用字也一致。
- **引理 6.2 的前提被計畫寫鬆了。** 計畫寫「最後一行一列是 δ ᵐ」，書上只要求**最後一條直行**是 δ ᵐ；被劃掉那一橫列的其他元素根本進不了行列式。這不是細節——那張「劃掉一橫列一直行」的圖很容易讓人以為那一橫列必須是零。所以多釘了一條 assert：把那三個數換成完全不同的值再算一次（`D_RED2`），D 仍是 54.000000，而且畫面把換數字這件事畫出來、`_cap` 明說。
- **負零。** `c ᵀ · t` 的離對角格子是算出來的，其中幾格是 `-0.0`，直接 `format` 會在畫面上印成「−0」。`ms()` 先把等於零的值正規化成 `0.0` 才格式化。
- **`ˢ`（U+02E2）整個 advcalc 目錄從來沒用過，所以不敢用。** 需要上標 s 的地方全部改成下標（`t ᵢ ₛ`、`δ ᵣ ₛ`），那兩個字元前面幾集用過。`‴` 沒碰。用到的每一個罕用字元都先用 `fc-list :charset=` 對照過系統字型，再挑既有集數已經出現過的那些。
- **英文旁白第一稿有八句超過四行**（最長 312 字元），逐句壓到 272 字元以內重驗。
- **第 3 拍差點畫成兩疊一樣的符號。** 左右兩疊只有前兩條互換、第三條原地不動，所以 `_cap` 直接說「第三條沒動」，而不是只說「對調了」。

## 十一拍

### 第 1 拍 — 唯一性：差一個純量只有一個 / uniqueness: only one, up to a scalar

公式列：

```
dim 𝒜 ᵐ   =   1            D ( δ ¹ , … , δ ᵐ )   =   1
```

中文旁白：上一集算出交錯 m 重形式那個空間是一維的。這一集就靠那個一：差一個純量倍，這種形式只有一個，所以只要再要求它在標準基底上取值等於一，就把它完全定死了。那個唯一確定的形式就是行列式。

English: Last episode found that the space of alternating m-forms is one-dimensional. This episode lives off that one. Up to a scalar multiple there is only one such form, so asking it to take the value one on the standard basis pins it down completely. That form is the determinant.

### 第 2 拍 — 引理 6.1：顯式公式 / Lemma 6.1: the explicit formula

公式列：

```
D ( t )  =  Σ  ε ( σ )  t σ ( 1 ) , 1  ⋯  t σ ( m ) , m            σ  ∈  S ₘ
```

中文旁白：引理 6.1 把它寫成顯式公式。對每一種把一到 m 重排的方式，從每一條直行各取一個元素，彼此落在不同橫列，乘起來，再按照那個重排的奇偶配上正負號，最後全部加總。三階就是六項，右表逐項列出來。

English: Lemma 6.1 writes it out explicitly. For each way of rearranging one through m, take one entry from every column, no two in the same row, multiply them, attach a sign from the parity of that rearrangement, and add. Three by three gives six terms.

### 第 3 拍 — 推論 1：轉置不改變它 / Corollary 1: the transpose has the same value

公式列：

```
D ( t ᵀ )   =   D ( t )            ρ  =  σ ⁻ ¹            ε ( ρ )  =  ε ( σ )
```

中文旁白：推論一說轉置不改變行列式。證明只要把乘積裡的因子依照橫列指標重新排序，乘積就變成依橫列取的同一個樣子，用的重排是原來那個的反排列。因為取反排列是一對一的對應，奇偶性又不變，整個和就原封不動。

English: The first corollary says transposing changes nothing. Reorder each product by row index and it becomes the same thing read along the rows, with the inverse rearrangement. Inverting is one to one and keeps the parity, so the sum is untouched.

### 第 4 拍 — 推論 2：對橫列也是交錯的 / Corollary 2: alternating in the rows as well

公式列：

```
D ( … , t ᵢ , … , t ⱼ , … )   =   −  D ( … , t ⱼ , … , t ᵢ , … )
```

中文旁白：推論二立刻跟著來。既然轉置不改變行列式，而它對直行是交錯多重線性的，對橫列當然也是。所以對調兩條橫列會變號，某一條乘上常數就整個乘上那個常數，某一條加上另一條的倍數則完全不變。

English: The second corollary follows at once. The determinant is alternating and multilinear in the columns, so transposing makes it so in the rows too. Swapping two rows flips the sign, scaling one scales the whole thing, adding a multiple of another changes nothing.

### 第 5 拍 — Δ ( T )：不依賴任何基底 / Delta of T: defined with no basis at all

公式列：

```
f ₜ ( ξ ₁ , … , ξ ₘ )  =  f ( T ξ ₁ , … , T ξ ₘ )  =  Δ ( T )  ·  f ( ξ ₁ , … , ξ ₘ )
```

中文旁白：接著定義不依賴基底的行列式。取任何一個不是零的交錯 m 形式，把 T 先作用在每個輸入上再餵給它，得到的還是一個交錯 m 形式，所以是原來那個的常數倍。因為那個空間一維，那個常數與選哪個形式無關，就叫做 T 的 Δ。

English: Next comes a determinant that needs no basis. Take any nonzero alternating m-form and apply T to each input before feeding it in: what comes out is again such a form, so it is a constant multiple. The space is one-dimensional, so that constant does not depend on the form.

### 第 6 拍 — 定理 6.1：合成變成相乘 / Theorem 6.1: composition becomes multiplication

公式列：

```
Δ ( S  ∘  T )   =   Δ ( S )   ·   Δ ( T )
```

中文旁白：定理 6.1 說 Δ 把合成變成相乘。證明只有兩行：把 S 合成 T 作用在一組輸入上，先把 S 提出一個 Δ S，再把 T 提出一個 Δ T，然後把形式本身約掉。右表拿兩個具體的三階矩陣核對，乘積與合成的行列式一樣。

English: Theorem 6.1 says this turns composition into multiplication. The proof is two lines: feed a composite into the form, pull out one factor for the outer map and one for the inner, then cancel the form itself. The table checks it on two concrete three by three matrices.

### 第 7 拍 — 定理 6.2 與三個推論 / Theorem 6.2 and its three corollaries

公式列：

```
S  =  θ ∘ T ∘ θ ⁻ ¹   ⇒   Δ ( S )  =  Δ ( T )          D ( t )  =  0  ⟺  ker ( t )  ≠  0
```

中文旁白：定理 6.2 說相似變換的 Δ 相同，於是三個推論一起落地：矩陣的行列式等於它代表的那個變換的 Δ、矩陣乘積的行列式等於兩個行列式相乘，還有最有用的一條，行列式等於零恰好等價於矩陣奇異。

English: Theorem 6.2 says similar transformations share the same value, and three corollaries land together. A matrix has the determinant of the transformation it stands for, a product has the product of determinants, and the determinant vanishes exactly when the matrix is singular.

### 第 8 拍 — 引理 6.2 與 6.3：降一階 / Lemmas 6.2 and 6.3: dropping one dimension

公式列：

```
t ᵐ   =   δ ᵐ            s   =   ( t ) ᵐ ᵐ            D ( s )   =   D ( t )
```

中文旁白：引理 6.2 處理降階。當最後一條直行剛好是標準基底的最後一個向量時，行列式等於劃掉最後一橫列與最後一直行之後那個小矩陣的行列式。推廣到變換上就是引理 6.3：T 在補空間上是恆等時，Δ 可以只在剩下的子空間裡算。

English: Lemma 6.2 drops a dimension. When the last column is the last standard basis vector, the determinant equals that of the matrix left after deleting the last row and column. Lemma 6.3 carries this over: if T is the identity on a complement, work inside the rest.

### 第 9 拍 — 定理 6.3：餘因子展開 / Theorem 6.3: the expansion by minors

公式列：

```
D ( t )   =   Σ ᵢ  ( − 1 ) ⁱ ⁺ ʳ  t ᵢ ᵣ  D ( ( t ) ⁱ ʳ )
```

中文旁白：定理 6.3 就是餘因子展開。沿著第 r 條直行走下去，每個元素乘上劃掉它所在那一橫列與那一直行之後的小行列式，再配上正負交錯的符號，加起來就是原來的行列式。右表沿第二直行展開，四項逐項列出。

English: Theorem 6.3 is the expansion by minors. Go down one column, multiply each entry by the smaller determinant left after deleting its own row and its own column, attach alternating signs, and add: the result is the determinant. The table expands down the second column, all four terms.

### 第 10 拍 — 推論 1 與餘因子矩陣 / Corollary 1 and the cofactor matrix

公式列：

```
Σ ᵢ  c ᵢ ᵣ  t ᵢ ₛ   =   δ ᵣ ₛ  ·  D ( t )            s ᵣ ᵢ   =   c ᵢ ᵣ  /  D ( t )
```

中文旁白：如果把展開式裡的元素換成另一條直行上的，那個和就是零，因為它等於一個有兩條直行相同的矩陣的行列式。兩件事合起來寫成一條：餘因子矩陣轉置後乘上原矩陣，剛好是行列式乘上單位矩陣，所以反矩陣就是餘因子除以行列式。

English: Replace those entries by the ones from a different column and the sum is zero, since it is the determinant of a matrix with two equal columns. Both facts fit one line: the transposed cofactor matrix times the original is the determinant times the identity.

### 第 11 拍 — Cramer 法則，第 6 節結束 / Cramer's rule, and the end of section 6

公式列：

```
x ⱼ   =   d ⱼ  /  D ( t )            t  ·  x   =   y
```

中文旁白：最後是 Cramer 法則。把第 j 條直行換成右手邊那個向量，算出來的行列式除以原本的行列式，就是解的第 j 個座標。右表三個座標與獨立的數值解法逐項相同。第 7 章還剩外代數、外冪與星算子這三節。

English: Last comes Cramer's rule. Replace the jth column by the right-hand side; the determinant of that over the original determinant is the jth coordinate of the solution. The three coordinates agree entry by entry with an independent solver. Three sections remain.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 一條代表 𝒜 ᵐ 的直線上擺五個點（都是 c · D），只有 c = 1 那一點是橘的；下面是 3 × 3 單位矩陣，旁邊標 D = 1.000000 |
| 2 | T3 的 3 × 3 數字陣列，σ = ( 3 1 2 ) 用到的三格染橘（每條直行一格、每條橫列一格）；直行與橫列各標 1 2 3；右表六項逐列，橘的那一列就是圖上那三格 |
| 3 | T3 與 T3 的轉置兩個數字陣列並排，各自標上自己的 D；右表最後一列印出兩個陣列的最大差 6，證明它們真的不是同一個矩陣 |
| 4 | 兩疊括起來的橫列符號：左邊 t ₁ t ₂ t ₃、右邊 t ₂ t ₁ t ₃（**只有前兩條互換，第三條沒動**），中間一支箭頭標 t ₁ ↔ t ₂ 與 D ↦ − D，兩疊下面各標自己的 D |
| 5 | 一個交換方塊：f → f ₜ 與 g → g ₜ 兩支水平箭頭各標 × Δ ( T )，f → g 與 f ₜ → g ₜ 兩支垂直箭頭各標 × c；右表最後一欄兩個 2.000000 |
| 6 | ℝ ᵐ → ℝ ᵐ → ℝ ᵐ 三個方塊，兩支箭頭標 T 與 S，底下各掛 Δ = +54、Δ = +13；下方一支長箭頭標 S ∘ T，再下面是 13 · 54 = 702 |
| 7 | V → V 與 W → W 兩層的相似方塊（上 T、下 S、兩側 θ），底下標 Δ ( S ) = Δ ( T ) = +54；右表奇異那一列是紅的 |
| 8 | 4 × 4 數字陣列，最後一直行（0 0 0 1）染橘並標 δ ᵐ，最後一橫列與最後一直行各用紅色方框圈起來（刪除線會劃過它指的那些數字，所以改成框），左上 3 × 3 用青色方框圈起來標 s |
| 9 | 四個 3 × 3 的小數字陣列（第 2 直行的四個餘子式，**四個真的是不同的矩陣**），每個上面標它的 ( − 1 ) ⁱ ⁺ ʳ 與 t ᵢ ₂，符號 − + − + 交錯 |
| 10 | c ᵀ · t 的 4 × 4 數字陣列：對角線四格都是 −160（橘），其餘十二格是 0（灰），下面標 = −160 · I |
| 11 | t 的 3 × 3 陣列、x 的符號直行、等號、y 的數字直行排成 t · x = y，下方標 D ( t ) = +54；右表三個 d ⱼ 與三個 x ⱼ |
