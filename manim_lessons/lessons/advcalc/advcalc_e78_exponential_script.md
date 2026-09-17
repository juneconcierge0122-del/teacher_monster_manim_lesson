# advcalc E78 — 第 6 章：常係數與矩陣指數

Chapter 6: Constant Coefficients and the Exponential

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 3 節「線性方程」的**後半**（書頁 278–280），接 E77 的定理 3.2。**§3 到此結束**，習題 3.1–3.9 在 280–281。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e78_exponential.py`（`AdvCalcE78ZH` / `AdvCalcE78EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[78]` / `FORMULAS_ADVCALC[78]`）
- 配音：`manim_lessons/samples/audio_e78/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 232.4 秒（3:52）／英文 208.2 秒（3:28）
- YouTube（私人）：中文 https://youtu.be/1sy5NxxkAKk ／英文 https://youtu.be/IDcSGXuLci4

## 這半節在做什麼

**左邊其實是一個全微分。** 手上唯一的新工具是基本解自己的方程 K ′ = T ₜ ∘ K，
把它解出 T ₜ = K ′ K ⁻ ¹ 代回去，由第 4 章習題 8.12 與第 3 章定理 8.4：

```
f ′ − T ₜ f    =    K ( t )  d / d t [ K ( t ) ⁻ ¹ ( f ( t ) ) ]
```

一個看起來要解的微分方程，**左邊已經是某個東西的全微分**——只要先用 K ⁻ ¹ 換個座標。
於是直接積分，得到 **定理 3.3**：

```
f ( t )   =   K ₜ [ ∫ K ₛ ⁻ ¹ ( g ( s ) ) d s ]        ( s : 0 → t )
```

這就是 E77 那個右反元素 R 的顯式公式。

**常係數：兩個小引理。** 引理 3.1 說解空間在 D 底下不變（右邊可微，再微分一次）；
**引理 3.2 說得更多**：

```
π ₜ ∘ D  =  T ∘ π ₜ           ⇒           T  =  φ ₜ ∘ D ∘ φ ₜ ⁻ ¹
```

**微分算子在解空間上的樣子，與 T 在 W 上的樣子，是同一個算子的兩張臉。**
這解釋了為什麼指數會出現：d S / d t = T S 就是指數函數的方程，所以 K ₜ = exp ( t T )。

**有限維時級數會塌成有限和。** p ( T ) = 0，W = ⊕ W ᵢ，在一塊上 T = λ I + R 而 R ᵐ = 0：

```
exp ( t T ) α   =   exp ( t λ ) [ α + t R α + ⋯ + t ᵐ ⁻ ¹ R ᵐ ⁻ ¹ α / ( m − 1 ) ! ]
```

**項數正好是那個因式的重數。** 定理 3.4 把一般情形寫成 Σ t ʲ exp ( t λ ᵢ ) β ᵢ ⱼ，
項數是 p 的次數。

## 這一集用的例子

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| K ′ K ⁻ ¹ 真的是 T ₜ | 三個 t 的數值微分 | 差 < 1e-6 |
| 定理 3.3 的公式對 | 代回 S 與 g 逐列比對 | 差 < 3e-4 |
| 它從零出發 | f ( 0 ) | < 1e-12 |
| R 冪零 | R ² | 全部 0（< 1e-15）|
| 60 項級數 = 2 項閉式 | 五個 t | 0e+00, 1e-16, 1e-16, 1e-15, 7e-15 |
| 閉式真的是解 | 三個 t 的數值微分 | 差 < 1e-6 |
| 引理 3.1（f ′ 也是解）| f ″ 對 T f ′ | 差 < 1e-3 |
| 漸近的四種情形 | ‖ f ( t ) ‖ 在 t = 0 / 5 / 10 / 20 | 見下表 |

| 情形 | λ | m | t = 0 | t = 5 | t = 10 | t = 20 |
|---|---|---|---|---|---|---|
| Re λ > 0 | 0.3 | 1 | 1.000 | 4.482 | 20.086 | 403.429 |
| Re λ < 0 | −0.5 | 1 | 1.000 | 0.082 | 0.007 | 0.000 |
| 純虛、單根 | 1.4 i | 1 | 1.000 | 1.000 | 1.000 | 1.000 |
| 純虛、重根 | 1.4 i | 2 | 1.000 | 5.099 | 10.050 | 20.025 |

**只有第三列一直是 1。** 這就是那個二分：

```
sup ‖ f ( t ) ‖  <  ∞         ⟺         Re λ ₙ = 0    ,    m ₙ = 1
```

場景檔用 `assert BOUNDED == ["c"]` 把「四個裡只有一個有界」釘住。

## 這一輪抓到的錯

- **表頭寫的欄位和表裡的資料不一樣。** 第 11 拍的表頭原本寫「log ‖ f ( t ) ‖ ↑ ／ ‖ f ( t ) ‖」，
  可是那四欄其實是**四個案例的 ‖ f ( t ) ‖**，沒有一欄是 log。改成直接標四個案例。
  這跟 E76「說明話指著長度卻講倍率」是同一類：**畫面上的字要指著畫面上真的有的東西**。
- **線性軸把三條壓在底部。** 第 11 拍四個案例跨四個數量級（0.0002 到 403），
  線性軸上只看得到爆炸那一條，其餘三條都貼在軸上分不出來。
  **改成對數軸**——順帶讓「有界 ⟺ 落在零線上」變成字面上看得見的事。
  第一版還試過把值 clamp 在 22，那會畫出 PLAYBOOK 第 5 節警告的「平台加懸崖」，放棄。
- **截斷級數飛出畫面。** 第 7 拍畫截到 2、4、8 項的部分和，原本沿用其他拍的 t ∈ [0, 8.4]；
  兩項的部分和在 t = 4 就離開畫面（y 到 +23）。視窗縮到 [0, 3]，那裡三條部分和一條比一條貼近。
- **`vs` 混進符號列**（langscan，2 個拉丁字母），改成 ⟶。
  另外把 `Re`、`Im`、`ker` 加進 langscan 白名單——它們是算子名，不是單字。

## 十一拍

### 第 1 拍 — 回到非齊次方程 / back to the inhomogeneous equation

公式列：

```
f ′ ( t ) − T ₜ ( f ( t ) )  =  g ( t )          T ₜ  =  K ′ ( t ) ∘ K ( t ) ⁻ ¹
```

中文旁白：上一集把解空間的結構弄清楚了，這一集要把右反元素真的寫出來。要解的是 f 一撇減去 T t 作用在 f 上等於 g。已知基本解滿足 K 一撇等於 T t 複合 K，所以 T t 等於 K 一撇複合 K 的反元素。

English: Last episode settled the structure of the solution space; this one writes the right inverse down. We want f with its derivative minus the operator applied to f equal to g. The fundamental solution satisfies its own equation, so the operator is K prime composed with K inverse.

### 第 2 拍 — 左邊其實是一個全微分 / the left side is a total derivative

公式列：

```
f ′ − T ₜ f    =    K ( t )  d / d t [ K ( t ) ⁻ ¹ ( f ( t ) ) ]
```

中文旁白：把這個代回去，左邊其實是一個全微分。由第 4 章習題 8.12 與第 3 章的乘法法則，f 一撇減去 T t f 正好等於 K t 乘上「K t 的反元素作用在 f 上」對 t 的導數。這一步是整個公式的關鍵。

English: Substituting that, the left side is really a total derivative. By Exercise 8.12 of chapter 4 and the product rule of chapter 3, it equals K at t times the derivative of the inverse of K applied to f. That step is the whole formula.

### 第 3 拍 — 於是可以直接積分 / so it can be integrated directly

公式列：

```
d / d t [ K ( t ) ⁻ ¹ ( f ( t ) ) ]    =    K ( t ) ⁻ ¹ ( g ( t ) )
```

中文旁白：於是方程變成可以直接積分的形式：K t 的反元素作用在 f 上，它對 t 的導數等於 K t 的反元素作用在 g 上。兩邊從零積到 t，再把 K t 乘回去就得到答案。書上說即使覺得推導太技術，也可以直接微分驗證。

English: So the equation becomes one to integrate directly: the derivative of K inverse applied to f equals K inverse applied to g. Integrate from zero to t and multiply K back on. The book notes that even if the derivation feels technical, the answer can be checked by differentiating.

### 第 4 拍 — 定理 3.3：右反元素的公式 / theorem 3.3: the right inverse

公式列：

```
f ( t )  =  K ₜ [ ∫ K ₛ ⁻ ¹ ( g ( s ) ) d s ]      ( s : 0 → t )         f ( 0 ) = 0
```

中文旁白：定理 3.3：f t 等於 K t 作用在「K s 的反元素作用在 g s 上，從零積到 t」這個積分上，就是初始值為零的非齊次問題的解。這正是上一集那個右反元素 R 的顯式公式，由 M 零這個補決定。

English: Theorem 3.3. The function K at t applied to the integral from zero to t of the inverse of K applied to g is the solution of the inhomogeneous problem with zero initial value. That is the explicit formula for last episode's right inverse, the one determined by that complement.

### 第 5 拍 — 常係數：引理 3.1 / constant coefficients: lemma 3.1

公式列：

```
f ′ ( t )  =  T ( f ( t ) )       ⇒       f ″ ( t )  =  T ( f ′ ( t ) )
```

中文旁白：接下來是常係數的情形，T t 是固定的 T，這一段極其重要。第一個新事實：如果 f 是解，那麼 f 一撇也是解。因為方程右邊可微，兩邊再微分一次就得到 f 兩撇等於 T 作用在 f 一撇上。這就是引理 3.1：解空間在導數算子底下不變。

English: Now constant coefficients, where the operator is a fixed T. The first new fact: if f solves the equation then so does its derivative, since the right side is differentiable and differentiating again gives its equation. That is Lemma 3.1: the solution space is invariant under D.

### 第 6 拍 — 引理 3.2：D 與 T 是同一個算子 / lemma 3.2: D and T are one operator

公式列：

```
π ₜ ∘ D  =  T ∘ π ₜ                T  =  φ ₜ ∘ D ∘ φ ₜ ⁻ ¹
```

中文旁白：而且導數算子在解空間上其實就是複合 T。把方程寫成 π t 複合 D 等於 T 複合 π t，再用 φ t 是同構，就解得出 T 等於 φ t 複合 D 再複合 φ t 的反元素。這是引理 3.2：同一個算子，在兩個空間裡的兩張臉。

English: Moreover differentiation on that space is just composition with T. Write the equation as evaluation composed with D equals T composed with evaluation, and since evaluation there is an isomorphism, solve for T. That is Lemma 3.2: one operator with two faces in two spaces.

### 第 7 拍 — K ₜ  =  exp ( t T ) / the fundamental solution is an exponential

公式列：

```
K ₜ  =  exp ( t T )            exp ( t T ) β  =  Σ ₀ ᶠ  t ʲ  T ʲ ( β ) / j !
```

中文旁白：基本解的方程現在是 S 一撇等於 T S。在初等微積分裡這就是指數函數的方程，所以可以預期而且立刻驗證 K t 等於 e 的 t T 次方。通過零與 β 的解就是那個級數：t 的 j 次方乘 T 的 j 次方作用在 β 上，除以 j 階乘，全部加起來。

English: The equation for the fundamental solution is now the one elementary calculus solves with the exponential, so K at t is the exponential of t times T. The solution through a vector is that series: t to the j times the jth power of T applied to it, over j factorial.

### 第 8 拍 — 有限維：W 拆成零化空間 / finite dimensions: W splits

公式列：

```
p ( x )  =  ∏ ₁ ᵏ ( x − λ ᵢ ) ᵐ ⁱ              W  =  ⊕ ₁ ᵏ  W ᵢ
```

中文旁白：有限維時可以走得更遠。T 滿足某個多項式方程，把它分解成互質的因式，W 就是各個零化空間的直和，而每一塊在 T 底下不變。於是只要看 α 落在其中一塊上的情形就夠了。

English: In finite dimensions we can go further. T satisfies a polynomial equation; factor it into relatively prime powers and W is the direct sum of the null spaces, each invariant under T. So it is enough to see what happens when the vector lies in one of those pieces.

### 第 9 拍 — 無窮級數變成有限和 / the series becomes a finite sum

公式列：

```
exp ( t T ) α  =  exp ( t λ ) [ α + t R α + ⋯ + t ᵐ ⁻ ¹ R ᵐ ⁻ ¹ α / ( m − 1 ) ! ]
```

中文旁白：在那一塊上 T 減 λ 的 m 次方是零，所以 T 等於 λ 加上一個冪零的 R。指數分解成 e 的 t λ 次方乘 e 的 t R 次方，而後者的級數只有 m 項——無窮級數突然變成有限和，項數正好是那個因式的重數。

English: On such a piece T minus lambda to the m is zero, so T is lambda plus a nilpotent R. The exponential factors into the scalar one times the exponential of t R, whose series has only m terms. The infinite series becomes a finite sum, with as many terms as the multiplicity.

### 第 10 拍 — 定理 3.4 / theorem 3.4

公式列：

```
f ( t )   =   Σ ᵢ ⱼ    t ʲ   exp ( t λ ᵢ )   β ᵢ ⱼ
```

中文旁白：定理 3.4 把這些合起來：一般的解是 k 個這種項的和，形狀是 t 的 j 次方乘 e 的 t λ i 次方再乘一個常向量，項數正好是多項式的次數。複數的情形完全一樣，只是 λ 可以有虛部，於是外面那個指數帶一個週期因子。

English: Theorem 3.4 collects this: the general solution is a sum of such terms, each t to the j times the exponential of t lambda times a constant vector, with as many terms as the degree of the polynomial. The complex case is identical, except lambda may have an imaginary part.

### 第 11 拍 — 漸近行為，與第 3 節的結束 / the asymptotics, and the end of section 3

公式列：

```
sup ‖ f ( t ) ‖  <  ∞        ⟺        Re λ ₙ = 0    ,    m ₙ = 1
```

中文旁白：最後看漸近行為，它完全由那些根決定。實部大於零就指數爆炸，小於零就趨近零；實部是零而重數大於一時像 t 的 m 減一次方那樣長。所以解在整條實數線上有界，若且唯若所有根都是純虛數而且重數都是一。第 3 節到此結束。

English: Finally the asymptotics, controlled entirely by those roots. Positive real part means blow-up, negative means decay, zero real part with multiplicity above one grows like a power of t. So solutions are bounded on the whole line exactly when every root is pure imaginary and simple.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | g 的兩個座標各一條曲線；右表三列：要解的方程、K 自己的方程、把它解出 T ₜ |
| 2 | f → K ⁻ ¹ f → d / d t 三個方塊串起來，再往下接 K ( t ) · ( … )；右表最後一列是乘法法則 |
| 3 | 被積函數 K ⁻ ¹ g 的兩個座標與第一個座標下方的網底——網底就是那個積分 |
| 4 | 定理 3.3 算出來的解，兩個座標各一條；右表把 S f 與 g 逐列並排 |
| 5 | f 與 f ′ 兩條曲線（都是解，所以都畫得出來）；右表列出引理 3.1 的三步 |
| 6 | N → N、W → W 的方塊圖，上排 D、下排 T，兩邊 φ ₜ 接起來——交換方塊 |
| 7 | 截到 2、4、8 項的部分和一條比一條貼近橘色的真解；視窗只到 t = 3 |
| 8 | W 拆成 W ₁ ⊕ W ₂ ⊕ W ₃，每塊底下標出它是哪個 ( T − λ ᵢ ) ᵐ 的零化空間 |
| 9 | exp ( t λ ) 與 t exp ( t λ ) 兩條，加上橘線是這個例子的解的長度——無窮級數只剩兩項 |
| 10 | 粗藍線是 60 項級數、細橘線是兩項閉式，整條躺在一起；右表的差是 1e-15 量級 |
| 11 | 四個案例的 log ‖ f ( t ) ‖：紅升、橘緩升、青平躺在零軸、紫下降。縱軸取對數 |
