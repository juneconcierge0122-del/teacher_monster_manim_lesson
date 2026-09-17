# advcalc E80 — 第 6 章：常係數方程的顯式解

Chapter 6: Constant Coefficients, Solved Explicitly

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 4 節「n 階線性方程」的**後半**（書頁 284 下半到 287），從「We now turn to an important tractable case」起。**§4 到此結束**，習題 4.1–4.19 在 287。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e80_constant.py`（`AdvCalcE80ZH` / `AdvCalcE80EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[80]` / `FORMULAS_ADVCALC[80]`）
- 配音：`manim_lessons/samples/audio_e80/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 250.0 秒（4:10）／英文 206.9 秒（3:27）
- YouTube（私人）：中文 https://youtu.be/T1BVZndPncM ／英文 https://youtu.be/4EPuV_RaySg

## 這半節在做什麼

**係數全是常數時，L 是 D 的一個多項式**，於是解微分方程變成分解因式：

```
L   =   p ( D )            p ( x )   =   Σ ₀ ⁿ  a ᵢ  x ⁱ
```

書上說最漂亮的走法是**繞到第 3 節去**。ψ 與微分交換、引理 3.1 給 D 不變性、
引理 3.2 把 D 換成 T，所以：

```
p ( D )  ↾  N   =   0            ⇒            p ( T )   =   0
```

而那是**有限維**的事，第 3 節的定理 3.4 已經解完了。取第一個座標就是答案。

**定理 4.2**（單一重根與互質分解）：

```
p ( x )  =  ( x − b ) ⁿ        N  =  ⟨ e ᵇ ᵗ , t e ᵇ ᵗ , … , t ⁿ ⁻ ¹ e ᵇ ᵗ ⟩
p ( x )  =  ∏ ₁ ᵏ  p ᵢ ( x )              B   =   ∪ ₁ ᵏ  B ᵢ
```

**複根要用第 4 章第 11 節習題裡的複化。** 要補的那一個事實是

```
Z  =  Y  ⊕  i Y              N ( T )   =   N ( S )  ∩  Y
```

所以實的解就是複的解取實部。於是不可約的二次因式交出共軛的一對，**定理 4.3**：

```
{ t ⁱ e ᵇ ᵗ cos ω t }  ∪  { t ⁱ e ᵇ ᵗ sin ω t }        i  =  0 , … , m − 1
```

**加星號的一段**：這些解構成一個代數（對加法與乘法封閉），
而且恰好是「所有平移張成有限維空間」的那些連續函數，因為常係數算子**正是**與平移交換的
線性微分算子。反過來那一半很細緻，書上沒證（它靠 K ₛ ₊ ₜ = K ₛ ∘ K ₜ 且 K ₜ → I 推出 K ₜ = exp ( t S )）。

## 書上定理 4.3 那一行的符號印錯了

**推導與定理的陳述不一致。** 書頁 285 的推導用的是

```
q ( x )   =   ( x ² − 2 b x + c ) ᵐ        λ  =  b + i ω        ω ²  =  c − b ²
```

根是 b ± i ω，所以基底裡的指數是 **e 的正 b t 次方**。可是兩段之後的定理 4.3 把二次式印成
`( t ² + 2 b t + c ) ᵐ`，而基底照樣寫 e ᵇ ᵗ。**兩者不可能同時對**：
t ² + 2 b t + c 的根是 −b ± i ω，基底該是 e 的負 b t 次方。

場景檔把兩個版本都算出來（b = −0.35、ω = 1.8、c = b ² + ω ² = 3.3625，m = 2）：

| 基底函數 | ( x ² − 2 b x + c ) ² 的殘差 | ( x ² + 2 b x + c ) ² 的殘差 |
|---|---|---|
| e ᵇ ᵗ cos ω t | 4.4e-15 | **6.110** |
| e ᵇ ᵗ sin ω t | 3.6e-15 | **4.735** |
| t e ᵇ ᵗ cos ω t | 5.0e-15 | **16.772** |
| t e ᵇ ᵗ sin ω t | 7.1e-15 | **14.516** |

畫面與旁白用的是**推導那個版本**（減號），並在註腳明說書上印的是加號。
`assert all(b > 1.0 for _a, b in SIGN)` 把這件事釘住——
哪天有人「照書修正」成加號，assert 會直接失敗。

這是這本書第二個這樣釘住的印刷錯誤（第一個是書頁 234 的 u 展開式符號，見 E64）。

## 數值是怎麼算的：精確，不是有限差分

這一集所有的殘差都是**精確算的**。一個函數以 `P(t) exp(λt)` 的項列表示（P 是係數串、λ 是複數），
微分就是

```
d / d t [ P ( t ) e ^ ( λ t ) ]   =   ( P ′ + λ P )  e ^ ( λ t )
```

純粹的多項式運算，**沒有任何有限差分**。所以 `p ( D )` 作用上去只是算術，
1e-15 這個數字才可以當成「就是零」來讀——這是符號那一項可以拿來下判斷的前提。

| 要驗的事 | 結果 |
|---|---|
| ( x − b ) ³ 殺掉 e ᵇ ᵗ、t e ᵇ ᵗ、t ² e ᵇ ᵗ | 1.4e-16、4.4e-16、4.4e-16 |
| **但殺不掉 t ³ e ᵇ ᵗ** | **6.0** — 所以剛好 n 個，不是 n + 1 個 |
| 那三個獨立 | Wronskian = +2 |
| ( x − b ₁ ) ² ( x − b ₂ ) 殺掉聯集的三個 | ≤ 1.1e-16，Wronskian = +0.7225 |
| 定理 4.3 的 2 m 個基底 | 見上表，Wronskian = +41.990 |
| x ⁴ − 1 殺掉 e ᵗ、e ⁻ ᵗ、cos t、sin t | 全部 0，Wronskian = −8 |
| x ³ − 1 的複根 | \| λ ³ − 1 \| = 2.5e-16 |
| x ³ − 1 殺掉那三個實基底 | ≤ 2.2e-16，Wronskian = +2.5981 |
| sin t cos 2 t = ( sin 3 t − sin t ) / 2 | 差 5.6e-17 |
| ( D ² + 1 ) ( D ² + 9 ) 殺掉它 | 4.6e-15 |
| **單獨 ( D ² + 1 ) 殺不掉** | **3.994** — 兩個頻率都要抓 |
| cos 的八個平移 | 奇異值 2.5e+01、1.9e+01、6.8e-15、… → **rank 2** |
| exp ( − t ² ) 的八個平移 | 1.4e+01 … 1.1e-01，八個都不是零 → **rank 8** |

最後那兩列是第 11 拍的重點：**平移的維數是判準本身**，而它是一個可以算的數。

## 這一輪抓到的錯

- **三張表的最後一列壓到說明話**，與 E79 同一類（八列用 `dy = 0.26` 會落在 −0.92，`_cap` 在 −0.90）。
  收成 `dy = 0.23`。
- **四個根的標籤壓在座標軸上。** 第 8 拍那四個根全部落在軸上（±1、±i），
  而標籤原本只沿著一個方向偏移（實軸上的往左右、虛軸上的往上下），
  結果每一個都貼在某一條軸的箭頭上，collide 報四次 `stroke/text Arrow through '−1'` 之類。
  改成**四個標籤各給一組斜的偏移**，兩條軸都離開。
  規則：**點在軸上時，標籤不能只沿軸偏移**。
- 順手清掉兩個沒有替換欄位的 f-string，和一個把標籤「先放高再 shift 下來」的寫法。
- **三撇字元缺字，把兩個方塊畫成同一個函數（只有 1080p 看得出來）。**
  第 1 拍那條導數鏈原本寫 f → f ′ → f ″ → f ‴，可是 **U+2034 ‴ 這個字元字型裡沒有，
  被畫成兩撇**，於是第三、第四個方塊變成同一個函數，而底下掛的 a ₂、a ₃ 還是不同的。
  改用 `f ⁽ ³ ⁾`。**這是「畫成兩個其實是同一個」的第五次，前四次都是幾何造成的，這次是排版**——
  bounds 與 collide 都看不到（字元在框內、沒疊到東西），480p 下兩撇三撇本來就分不清。
  **為此重渲了一次。** 同一輪順手放大核過 `λ̄` 與 `ᐟ`，兩個都畫得出來。
  規則：**畫面用到罕用字元，就在 1080p 下放大看一次。**
- 表格那四列的列標原本寫 `t ^ 0 cos`，旁邊整片都是真正的上下標，只有這裡是程式碼式的插入符號。改成 `t ⁰ cos`。

## 十一拍

### 第 1 拍 — 常係數：L 是 D 的多項式 / constant coefficients: a polynomial in D

公式列：

```
L  =  p ( D )          p ( x )  =  Σ ₀ ⁿ  a ᵢ  x ⁱ          D f  =  f ′
```

中文旁白：上一集的降階法要先知道一個解才動得了。這一集是整節裡最有用的一段：係數全是常數的情形，有完整的顯式答案。關鍵是此時 L 就是導數算子的一個多項式，記作 p 作用在 D 上，於是解微分方程變成把 p 分解因式。

English: Last episode's reduction needed one solution before it could start. This episode is the most useful stretch of the section: with constant coefficients there is a complete explicit answer, because the operator is now a polynomial in D, and solving becomes factoring.

### 第 2 拍 — 繞道第 3 節 / the detour through section 3

公式列：

```
p ( D )  ↾  N   =   0            ⇒            p ( T )   =   0
```

中文旁白：書上說最漂亮的走法是繞到第 3 節去。ψ 把解空間同構地搬到一階系統那邊，而且它與微分交換；引理 3.1 說那個空間在 D 底下不變，引理 3.2 說取值同構把 D 換成 T。所以 p 作用在 D 上是零，就推出 p 作用在 T 上是零。

English: The book calls the most elegant route the detour through section 3. Psi carries the solution space over to the system and commutes with differentiation; Lemma 3.1 makes that space invariant under D, and Lemma 3.2 turns D into T. So the polynomial annihilating D annihilates T.

### 第 3 拍 — 定理 4.2 的前半 / theorem 4.2, first half

公式列：

```
p ( x )  =  ( x − b ) ⁿ        N  =  ⟨ e ᵇ ᵗ , t e ᵇ ᵗ , … , t ⁿ ⁻ ¹ e ᵇ ᵗ ⟩
```

中文旁白：定理 4.2 的前半：如果 p 是 x 減 b 的 n 次方，那麼解空間有基底 e 的 b t 次方、t 乘它、一直到 t 的 n 減一次方乘它。這正是上一集定理 3.4 那個答案取第一個座標，而且剛好 n 個，所以是一組基底。

English: The first half of Theorem 4.2: if the polynomial is x minus b to the n, the solution space has the basis given by the exponential of b t, t times it, up to t to the n minus one times it. That is last episode's Theorem 3.4 in first coordinates, and there are exactly n of them.

### 第 4 拍 — 互質分解：基底聯集起來 / relatively prime factors: unite the bases

公式列：

```
p ( x )  =  ∏ ₁ ᵏ  p ᵢ ( x )              B   =   ∪ ₁ ᵏ  B ᵢ
```

中文旁白：後半：把 p 分解成互質的因式的乘積，每個因式照前一拍給出一組基底，全部聯集起來就是整個解空間的基底。理由是第 1 章定理 5.5 那個直和分解，經由同構搬到這裡來。

English: The second half: factor the polynomial into relatively prime powers, take the basis of the previous beat for each factor, and the union is a basis for the whole solution space. The reason is chapter 1's Theorem 5.5, the direct sum decomposition, carried over by the isomorphism.

### 第 5 拍 — 複根：複化 / complex roots: complexification

公式列：

```
Z  =  Y  ⊕  i Y              N ( T )   =   N ( S )  ∩  Y
```

中文旁白：如果 p 的根不全是實數，就要用第 4 章第 11 節習題裡的複化理論。除了最後一步，結果一模一樣。要補的那個事實是：實算子在實空間上的零化空間，正好是它的複化的零化空間與實空間的交集。所以實的解就是複的解取實部。

English: If the roots are not all real we need the complexification theory from chapter 4's exercises. The extra fact is that the null space of a real operator is the intersection with the real space of the complexified one, so the real solutions are real parts of complex ones.

### 第 6 拍 — 共軛的一對 / the conjugate pair

公式列：

```
q ( x ) = ( x ² − 2 b x + c ) ᵐ = ( x − λ ) ᵐ ( x − λ̄ ) ᵐ      λ = b + i ω
```

中文旁白：具體來說，設某個二次式在實數上不可約，而 p 的一個因式是它的 m 次方。在複數上它分解成 x 減 λ 的 m 次方乘 x 減 λ 共軛的 m 次方，其中 λ 的實部是 b、虛部是 ω，而 ω 平方等於常數項減去 b 平方。複的零化空間是 2 m 維的。

English: Concretely, let a quadratic be irreducible over the reals and one factor be its mth power. Over the complex numbers it splits into x minus lambda and x minus its conjugate, each to the m, with lambda of real part b and imaginary part omega. That null space has dimension two m.

### 第 7 拍 — 定理 4.3：取實部 / theorem 4.3: take real parts

公式列：

```
{ t ⁱ e ᵇ ᵗ cos ω t }  ∪  { t ⁱ e ᵇ ᵗ sin ω t }        i  =  0 , … , m − 1
```

中文旁白：取實部就得到定理 4.3：e 的 b t 次方乘 cos ω t、乘 sin ω t，各再乘上 t 的零到 m 減一次方，一共 2 m 個，所以是實解空間的基底。順帶一提，書上那一行把二次式的中間項印成加號，與它自己上面兩段的推導不一致，畫面上用的是一致的那個。

English: Taking real parts gives Theorem 4.3: the exponential of b t times cosine and sine of omega t, each times powers of t up to m minus one, two m functions in all. Note that the book's display prints the quadratic's middle sign against its own derivation; the screen is consistent.

### 第 8 拍 — 例一 / first example

公式列：

```
x ⁴ − 1 = ( x − 1 ) ( x + 1 ) ( x − i ) ( x + i )      N = ⟨ e ᵗ , e ⁻ ᵗ , cos t , sin t ⟩
```

中文旁白：看兩個例子。D 的四次方減一等於零：多項式分解成 x 減一、x 加一、x 減 i、x 加 i 四個一次式，複的基底是四個指數。因為 e 的 i t 次方是 cos t 加 i sin t，實的基底就是 e 的 t 次方、e 的負 t 次方、cos t、sin t。

English: Two examples. For the fourth power of D minus one the polynomial splits into four linear factors, and the complex basis is four exponentials. Since the exponential of i t is cosine plus i sine, the real basis is two exponentials, a cosine and a sine.

### 第 9 拍 — 例二 / second example

公式列：

```
x ³ − 1  =  ( x − 1 ) ( x ² + x + 1 )          λ  =  − 1 / 2  ±  i √ 3 / 2
```

中文旁白：D 的三次方減一等於零：分解成 x 減一乘上 x 平方加 x 加一，後面那個不可約，兩個根是負二分之一加減 i 乘根三除以二。所以實的基底是 e 的 t 次方，以及 e 的負 t 除以二次方分別乘上 cos 與 sin 根三 t 除以二。

English: For the third power of D minus one the polynomial splits into x minus one times an irreducible quadratic. Its roots are minus a half plus and minus i root three over two, so the real basis is the exponential of t and a decaying one times a cosine and a sine.

### 第 10 拍 — 加星號：這些解構成一個代數 / starred: the solutions form an algebra

公式列：

```
𝒜  ·  𝒜   ⊂   𝒜          2 sin x cos y  =  sin ( x + y )  +  sin ( x − y )
```

中文旁白：接下來是加星號的一段。所有常係數齊次線性方程的實值解合起來，這個集合對加法與乘法都封閉，它就是 t 的幂、指數、cos 與 sin 生成的代數。加法容易：兩個常係數算子一定交換，複合起來就把兩邊的解都殺掉。乘法要靠三角恆等式把乘積寫成和。

English: The starred passage: all real solutions of constant coefficient equations form a set closed under addition and multiplication, the algebra generated by powers of t, exponentials, cosines and sines. Sums are easy: two such operators commute, so the composite kills both.

### 第 11 拍 — 平移張成有限維，第 4 節結束 / translates span finitely, and the end of section 4

公式列：

```
K ₓ f ( t )  =  f ( t − x )            dim ⟨ K ₓ f  :  x ∈ ℝ ⟩   <   ∞
```

中文旁白：最後一件事很漂亮：這些函數恰好是「所有平移張成有限維空間」的那些連續函數。因為常係數算子正是與平移交換的線性微分算子，而算子交換就讓零化空間在平移底下不變，那個空間又是有限維的。反過來那一半很細緻，書上沒證。第 4 節到此結束。

English: The last thing is lovely: these are exactly the continuous functions whose translates span a finite-dimensional space. Constant coefficient operators are precisely those commuting with translation, which makes the null space translation invariant, and it is finite-dimensional.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | f → f ′ → f ″ → f ‴ 四個方塊由 D 串起來，每個底下掛一個係數，最後併成 Σ a ᵢ f ⁽ ⁱ ⁾ = p ( D ) f |
| 2 | N → 𝒩 → ℝ ⁿ 三個方塊（ψ 與 φ ₜ 兩支箭頭），D 標在左上、T 標在右下 |
| 3 | e ᵇ ᵗ、t e ᵇ ᵗ、t ² e ᵇ ᵗ 三條；右表最後一列是紅的 t ³ e ᵇ ᵗ，殘差 6.0 |
| 4 | 兩個因式的三個基底畫在一起（兩條衰減、一條成長）；右表附 Wronskian |
| 5 | Z = Y ⊕ i Y 一個大方塊拆成 Y 與 i Y，S 在上、T 在 Y 那一側 |
| 6 | 複平面上共軛的一對，各標 m = 2，虛線標出 b 與 ± ω |
| 7 | 定理 4.3 的四個實基底一起畫（兩個包絡、兩個相位）；右表兩欄是兩個符號的殘差 |
| 8 | x ⁴ = 1 的四個根落在單位圓上，彼此差九十度。**標籤斜著放，兩條軸都不壓** |
| 9 | e ⁻ ᵗ ᐟ ² cos 與 sin 兩條，加上 ± e ⁻ ᵗ ᐟ ² 的灰色包絡線——根的實部是衰減、虛部是頻率 |
| 10 | sin t cos 2 t 一條粗線，加上 sin 3 t / 2 與 − sin t / 2 兩條細線：粗線正是兩條細線的和 |
| 11 | 同一個 cos 的五個平移；右表兩列奇異值：cos 第三個就掉到 1e-15，Gaussian 八個都在 |
