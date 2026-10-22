# advcalc E84 — 第 6 章：Fourier 級數

Chapter 6: Fourier Series

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 7 節「Fourier 級數」**全節**，**第 6 章到此結束**（書頁 301–303）。習題 7.1–7.10 在 304。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e84_fourier.py`（`AdvCalcE84ZH` / `AdvCalcE84EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[84]` / `FORMULAS_ADVCALC[84]`）
- 配音：`manim_lessons/samples/audio_e84/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 280.9 秒（4:41）／英文 206.5 秒（3:27）
- YouTube（私人）：中文 https://youtu.be/74PqP-j7cKQ ／英文 https://youtu.be/oA8ZepMDHmM

## 這一節在做什麼

書上開頭就說：**正則的 Sturm-Liouville 系統其實不多。** Bessel、Legendre、Hermite、Laguerre
全來自奇異的系統——不是最高階係數在端點歸零，就是區間根本無界。最有名的那個例外正是 Fourier 級數。

它就是 T = D ² 配兩種邊界條件。**型 1**（f ( 0 ) = f ( π ) = 0）：λ > 0 與 λ = 0 都只剩零解，
λ < 0 才有救，條件是 sin r π = 0 ⇒ r = n。特徵函數 { sin n x }、特徵值 { − n ² }，這就是**定理 7.1**。

**型 4**（週期）：同樣逼出整數，但這次**整個二維解空間都滿足邊界條件**，所以每個特徵值都是二重的。
畫面上也點出書上寫得鬆散的一處：書說一次式「同樣被排除」，**但其實只排除了 x 那一項**——
常數函數的值與斜率在兩端都相等，它活下來就是 n = 0 的那個 cos，這正是**定理 7.2** 裡
cos 從 0 編號、sin 從 1 編號的理由。

**定理 7.3** 是稠密性，證法很手工：先用折線逼近，再把每個轉角磨成一小段斜坡，讓磨掉與補上的面積相等。
它的作用是把「M 的基底」升級成「整個 𝒞 ⁰ 的基底」。

最後兩拍是習題裡那兩個更強的結果：**習題 7.6**（只要一階連續可微、兩端值相等就一致收斂）與
**習題 7.10**（Weierstrass 逼近定理）。**只講它們說什麼、為什麼比正文強，不做解答。**

## 這一集用的例子

| 要驗的事 | 結果 |
|---|---|
| 五組古典方程乘上積分因子後變成自伴形式 | 殘差 1.1e-16 |
| λ > 0 與 λ = 0 只有零解 | det = −23.097、−3.1416，**都不是零** |
| λ < 0 時 det = − sin r π | r = 2：2.4e-16；**r = 2.5：−1.00** |
| ( D ² + n ² ) sin n x | 0（用複指數組起來，不是背微分公式）|
| 正交性 | [ 0 , π ] 上自己和自己是 π / 2；[ −π , π ] 上是 π；**唯獨常數是 2π** |
| 週期情形的二重性 | **Wronskian = − n = −2.0**（五個點真的算過）|
| 一致收斂（x ( π − x )）| 0.10500 → 0.02923 → 0.01331 → 0.00485 |
| 磨圓的代價 | **恰好等於 δΔ/4**（不是小於，是相等到 1e-12）|
| f ≡ 1 的一致誤差 | **永遠是 1.0000**，而二範數誤差在掉——稠密性買到的是二範數 |
| 習題 7.6 的例子 | f ( −π ) = f ( π )，但 f ′ 差一個正負號 → 定理 7.2 管不到它 |

## 這一輪抓到的錯

- **說明話與模組自己的 assert 打臉。** `_cap` 說「只有橘色那條不碰底線」，可是模組裡就寫著
  `min(SLEND[3]) > 0.25, "Hermite's stays well off zero..."`——畫面上有**兩條**不碰底線，
  而那正是 Hermite 的重點（壞的是無界區間，不是係數歸零）。改成把兩種奇異分開講。
- **`det ⟨ sin n x , cos n x ⟩ = −2` 是手打的**，assert `abs(WRPER) > 0.5` 等於在驗 `2 > 0.5`；
  而且同一張表裡 `( , )` 是內積，那個寫法很容易被讀成「sin 與 cos 的內積是 −2」（真值是 0）。
  改成**真的算 Wronskian**（五個點全是 −2.0），標籤改 `W ( sin n x , cos n x ) = − n`。
- 作圖約定一度被我改丟：五條曲線屬於五個不同區間、壓成同寬，**長短不能比**——
  這句話補回註腳，中英都補。
- Bessel 那列寫 `( 0 , 1 ]` 卻同時說 `c ₂ ( 0 ) = 0`，區間不含 0 就不該這樣寫 → 改 `[ 0 , 1 ]`。
- 旁白說習題 7.6 的好處含「不必兩階可微」，但畫的 `π² − x²` 是 𝒞 ^∞，
  畫面實際支持的只有「導數不必在端點相等」那一半 → 旁白改成只講那一半。
- `_cap` 說「前兩欄的誤差一起往下掉」，可是第一欄是細分數 n，兩個誤差在第二、三欄 → 改「中間兩欄」。

### 我自己複核時撤回的兩條

- 「上圖的折線太細、看不出是折線」→ **撤回**。`N73 = 4`，放大四倍後四段折線的轉角清清楚楚，
  是 480p 整張看造成的誤判。**判斷線條細節之前要先放大。**
- 「第 11 拍的說明話沒講那幾條是什麼」→ **撤回**。檔案裡早就是
  「左圖是 sin 自己的 Maclaurin 部分和，不是 f 的逼近」——**我看的是過期的幀**：
  那個 agent 在我開始渲 probe 之後還在改檔案。

## 十一拍

### 第 1 拍 — 正則的系統不多 / there are not many regular systems

公式列：

```
T f  =  ( c ₂ f ′ ) ′  +  c ₀ f            c ₂ ( t )  ≠  0  ,    a  ≤  t  ≤  b
```

中文旁白：正則的 Sturm-Liouville 系統其實不多。計算裡常用的那幾組正交基底，像 Bessel、Legendre、Hermite、Laguerre，全來自奇異的系統：不是最高階係數在端點變成零，就是區間根本無界。最有名的那個例外，正是 Fourier 級數。

English: There are not many regular Sturm-Liouville systems. The bases calculations use, those of Bessel, Legendre, Hermite and Laguerre, come from singular ones: the leading coefficient dies at an endpoint, or the interval is unbounded. The famous exception is Fourier series.

### 第 2 拍 — T 等於二階導數：形式自伴又正則 / T is the second derivative: self-adjoint and regular

公式列：

```
T f  =  D ² f          c ₂  ≡  1  ,    c ₁  =  c ₂ ′  =  0  ,    c ₀  ≡  0
```

中文旁白：這一節的算子就是 T 作用在 f 上等於 f 的二階導數。最高階係數恆等於一，所以一階項的係數等於它的導數，也就是零，照上一節的引理這正是形式自伴；而最高階係數從頭到尾不為零，系統是正則的。邊界條件取兩種：型一要兩個端點的值都是零，型四要週期。

English: The operator here is T f equals the second derivative of f. Its leading coefficient is one, so the first order one is zero, which makes T formally self-adjoint, and it never vanishes, so the system is regular. Type one asks for zero at both ends, type four for periodicity.

### 第 3 拍 — 型 1：三種 λ 都試一遍 / type 1: all three cases of lambda

公式列：

```
f ″  −  λ f  =  0            f ( 0 )  =  f ( π )  =  0            sin r π  =  0
```

中文旁白：先解型一。方程是 f 的二階導數減去 λ 乘 f 等於零。λ 大於零時解空間由兩個指數張成，兩端都為零會逼出兩個係數都是零；λ 等於零時解是一次式，同樣只剩零解。右表把這兩個線性方程組的行列式算出來，都不是零。λ 小於零才有救，條件是 sin r π 等於零。

English: Solve type one first. For positive lambda the solution space is spanned by two exponentials, and vanishing at both ends forces both constants to zero. For lambda zero the solution is linear, and again only zero survives. The table gives those two determinants, neither of them zero.

### 第 4 拍 — 特徵函數與特徵值 / the eigenfunctions and the eigenvalues

公式列：

```
D ² sin n x   =   −  n ² sin n x            λ ₙ   =   −  n ²
```

中文旁白：所以特徵函數是 sin n x，特徵值是負的 n 平方，n 跑遍正整數。左圖畫了前三個，節點數一個比一個多，不可能疊成同一條。右表把二階導數加上 n 平方再代回去，殘差是機器精度的零，兩個端點的值也是零；換成不是整數的 r，右端點馬上就離開零了。

English: Only negative lambda works, and the condition is that the sine of r pi vanishes. So the eigenfunctions are the sines of n x, with eigenvalues minus n squared. The figure draws the first three, each with one more node. A non-integer r leaves the right endpoint.

### 第 5 拍 — 定理 7.1 / theorem 7.1

公式列：

```
{ sin n x }   n  ≥  1          ( sin n x , sin m x )  =  0          n  ≠  m
```

中文旁白：定理 7.1 說，這一族是零到 π 上連續函數空間的正交基底：彼此的內積是零，自己和自己是 π 的一半。而且只要 f 有兩階連續導數、兩端的值又都是零，它的 Fourier 級數就一致收斂到 f。左圖畫的是誤差本身，三條放大同一個倍率，取愈多項就愈平。

English: Theorem 7.1: this family is an orthogonal basis for the continuous functions on zero to pi. Distinct ones are orthogonal, each has square norm half of pi. If f has two continuous derivatives and vanishes at both ends, its series converges uniformly.

### 第 6 拍 — 型 4：週期條件 / type 4: the periodic condition

公式列：

```
2 c ₁ sin r π  =  0  ,    2 r c ₂ sin r π  =  0          r  =  n  ,    dim  =  2
```

中文旁白：換成型四的週期條件。λ 大於零那一支，兩個條件先逼出兩個係數相等，再逼出它們互為相反數，於是還是只有零解；λ 等於零時一次項被殺掉，但常數項活了下來，那就是 cos 零乘 x。λ 小於零時仍然得到 r 等於 n，但這次整個二維解空間都滿足邊界條件。

English: Now the periodic condition. For positive lambda the two conditions force the constants equal and then opposite, so only zero survives. For lambda zero the linear term dies but the constant lives, and that constant is the cosine of zero x. Negative lambda again gives r equal to n.

### 第 7 拍 — 定理 7.2 / theorem 7.2

公式列：

```
{ sin n x }  ∪  { cos n x }            ∫ sin n t cos n t d t   =   0
```

中文旁白：所以週期情形的每個特徵值都是二重的，sin 與 cos 兩族都要。定理 7.2 說它們合起來是負 π 到 π 上連續函數空間的正交基底。要補證的只有兩族互相正交：被積函數是奇函數，在對稱區間上積分必然是零，左圖那條累積面積的曲線跑完正好回到零。

English: This time the whole two dimensional solution space meets the condition, so every eigenvalue is double and both families are needed. Theorem 7.2 makes the sines and cosines together an orthogonal basis. A sine against a cosine is odd, so the running area returns to zero.

### 第 8 拍 — 定理 7.3：稠密性 / theorem 7.3: density

公式列：

```
f  ∈  𝒞 ( [ a , b ] )          ‖ f  −  H ‖ ∞  <  ε          H  ∈  𝒞 ² ( [ a , b ] )
```

中文旁白：定理 7.3 說，有兩階連續導數的函數在一致範數下稠密，端點附近為零的那一族在二範數下稠密。證法很手工：先用折線逼近 f，折線的導數是階梯函數，再把每個跳躍磨成一小段斜坡，讓磨掉和補上的面積相等。積回去得到的函數只在轉角附近和折線差一點點。

English: Theorem 7.3: functions with two continuous derivatives are dense in the uniform norm, and those vanishing near the ends are dense in the two norm. The proof is by hand. Approximate f by a polygonal line, then grind each jump of its step derivative into a ramp of equal area.

### 第 9 拍 — 為什麼需要稠密性 / why density is needed

公式列：

```
M   ⊂   𝒞 ⁰ ( [ 0 , π ] )            ‖ · ‖ ₂            Ch 5  ,  2.3
```

中文旁白：為什麼需要這一步？因為前面證到的只是 M 這個子空間上的展開，而 M 要求兩階可微、端點為零。稠密性把 M 的基底升級成整個連續函數空間的基底。左圖是個反例：取 f 恆等於一，二範數誤差確實一直往下掉，但一致誤差永遠卡在一，因為部分和在端點一定是零。

English: Why is that needed? What was proved before is an expansion on the subspace M, which asks for two derivatives and zero at the ends. Density promotes a basis of M to a basis of the whole space. For f identically one the two norm error falls, the uniform error does not.

### 第 10 拍 — 習題 7.6：更強的一致收斂 / exercise 7.6: a stronger uniform convergence

公式列：

```
f  ∈  𝒞 ¹  ,    f ( − π )  =  f ( π )          ⇒          ‖ f  −  S ‖ ∞   →   0
```

中文旁白：正文的定理其實不是最強的，最強的兩個結果藏在習題裡。習題 7.6 要的是：f 只要有連續導數、而且兩個端點的值相等，Fourier 級數就一致收斂，不必要求兩階可微，也不必要求導數在端點相等。題目給的路線是把導數的級數逐項積分，再用 Schwarz 不等式收尾。

English: The strongest results here are not the theorems but two of the exercises. Exercise 7.6 asks for this: if f merely has a continuous derivative and takes equal values at the two endpoints, its Fourier series converges uniformly. No second derivative is needed.

### 第 11 拍 — 習題 7.10：Weierstrass 逼近定理，第 6 章結束 / exercise 7.10: Weierstrass, and the end of chapter 6

公式列：

```
‖ f  −  p ‖ ∞   <   ε            p  ∈  ℝ [ x ]            § 7  ,  7.10
```

中文旁白：習題 7.10 更漂亮：Weierstrass 逼近定理說，多項式在一致範數下稠密於連續函數空間。先用定理 7.3 換成兩階可微的 g，扣掉一條直線讓兩端歸零，再展成 sin 的級數，把每個 sin n x 換成 Maclaurin 部分和。第 6 章到此結束。

English: Exercise 7.10 is lovelier still: the Weierstrass theorem, that polynomials are dense in the continuous functions in the uniform norm. Replace f by a twice differentiable g, subtract a line so it vanishes at both ends, expand in sines, and truncate each Maclaurin series.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 五組古典系統的 c ₂ 畫在同一條底線上（區間壓成同寬、高度各自歸一） |
| 2 | 兩種邊界條件的區間對照，下面那個剛好是上面的兩倍長 |
| 3 | 三種 λ 的解：只有 λ < 0 那條回得到右端的零 |
| 4 | 前三個 sin n x，節點數各不相同；最後一列的 r 不是整數 |
| 5 | f − S ₁、f − S ₃、f − S ₅ 三條誤差曲線，同一個倍率放大 |
| 6 | 週期條件：三條在兩端的高度與斜率都對得上 |
| 7 | sin 2 x · cos 2 x 與它的累積面積，跑完正好回到零 |
| 8 | f、折線 g、磨圓後的 H；下圖是 g ′ 的階梯與 h 的斜坡 |
| 9 | f ≡ 1 的部分和在端點永遠是零，紅虛線就是那個不會縮小的誤差 |
| 10 | π ² − x ² 的兩端值相等、斜率差一個正負號 |
| 11 | sin 自己的 Maclaurin 部分和：三次那條衝過頭、五次的沒有 |
