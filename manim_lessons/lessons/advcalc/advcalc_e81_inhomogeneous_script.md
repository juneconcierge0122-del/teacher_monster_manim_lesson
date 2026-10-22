# advcalc E81 — 第 6 章：解非齊次方程

Chapter 6: Solving the Inhomogeneous Equation

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 5 節「解非齊次方程」**全節**（書頁 288–292）。習題 5.1–5.22 在 293–294。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e81_inhomogeneous.py`（`AdvCalcE81ZH` / `AdvCalcE81EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[81]` / `FORMULAS_ADVCALC[81]`）
- 配音：`manim_lessons/samples/audio_e81/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 258.1 秒（4:18）／英文 205.2 秒（3:25）
- YouTube（私人）：中文 https://youtu.be/Hf-Ie7uqduo ／英文 https://youtu.be/JBPh7KjmBTA

## 這一節在做什麼

書上給兩條路，並且明說它對第一條不滿意。

**待定係數法**容易算，但只對某些 g 管用：g 自己落在某個常係數算子 S 的零化空間裡時，
解就落在 S ∘ L 的零化空間裡，而那個空間上一集已經完全知道。

```
S ( g )  =  0        ⇒        ( S ∘ L ) ( f )   =   S ( g )   =   0
```

**L 與 S 有公因式時要多帶一個 t 的幂**，次數正好是公因式重複的次數。
( D ² + 1 ) f = sin t 的解是 − t cos t / 2——振幅隨 t 線性長大，那就是共振的雛形。

**書上為什麼不滿意**：待定係數法**不是一個線性右反元素**，不是「一個流程對付所有 g」，
而是隨 g 換招。**參數變異法**才是真正的右反元素，對每個 g 都成立，連變係數的 L 都能反：

```
w ᵢ ⱼ ( t )  =  u ⱼ ⁽ ⁱ ⁻ ¹ ⁾ ( t )          K ₜ  =  w ( t ) · w ( 0 ) ⁻ ¹
f ( t )  =  w ( t ) · ∫ w ( s ) ⁻ ¹ · g ( s ) d s
```

中間那個常矩陣 w ( 0 ) 消掉，是因為積分與常矩陣相乘可交換。**定理 5.1** 把它寫成
只含 c ᵢ ′ 的線性方程組。最後用彈簧與 LRC 電路收尾——同一個方程治理兩件事。

## 這一集用的例子

| 要驗的事 | 結果 |
|---|---|
| y ′ − a y = e ᵇ ᵗ 的 c = 1 / ( b − a ) | a = −0.40、b = +0.70 ⇒ c = 0.909091，殘差 4.4e-16 |
| 三角那組的兩個係數 | 殘差 3.6e-15 |
| ( D − r ) ² ( t ² e ʳ ᵗ / 2 ) − e ʳ ᵗ | 0 |
| **不帶 t 的試驗函數被殺光** | i = 0、1 殘差 0；**i = 2 是 2.0000** |
| ( D ² + 1 ) ( − t cos t / 2 ) − sin t | 1.1e-16，振幅在視窗內長到 4 以上 |
| w 的行列式不隨 t 變 | 恆為 −1 |
| v ″ + v − 1 / cos x | 2.2e-16（在 ( −π/2 , π/2 ) 內） |
| 三種阻尼各自滿足自己的方程 | 殘差 ≤ 2e-15 |
| **兩個頻率只差 4.6%** | Ω = 2.0000、ω_d = 1.9079——所以分辨靠包絡線 |
| 欠阻尼的真實振幅因子 | A = 1.0483（不是裸指數）|

## 這一輪抓到的錯

- **assert 的訊息與它驗的事相反。** 原本驗 `|ω_d − Ω| > 0.08`，訊息卻說「分開這兩條的是
  包絡線、不是頻率」——要釘後者該驗兩個頻率有多**接近**。改成驗相對差 < 6%，並補一條驗振幅因子。
- **包絡線畫得比真實振幅低 4.8%。** 解是 cos + ( δ / ω ) sin 乘上指數，真實振幅是裸指數的
  √( 1 + ( δ / ω ) ² ) = 1.0483 倍，第一個峰會跑到灰線外。改畫 A e ⁻ ᵟ ᵗ。
- **「幾乎平行」講錯了。** 同指數、差常數倍是**成比例**，垂直距離一路變大。改成
  「藍線是橘線的零點九零九倍，左半段兩條幾乎疊在一起」。
- `V9MAX` 算了沒用——補上它本來該做的檢查（曲線在視窗裡不是一條平線），**門檻由實測值決定**
  （1.3667，所以釘 > 1.2），不是用猜的。

## 十一拍

### 第 1 拍 — 要解的是什麼，兩條路 / what is to be solved, and two routes

公式列：

```
L ( f )  =  g            f   ∈   v  +  N            dim N   =   n
```

中文旁白：這一節要解的是非齊次方程：算子 L 作用在 f 上等於給定的 g。只要找到任何一個特解 v，全部的解就是 v 加上齊次解空間 N，是一個仿射子空間。書上給兩條路：一條容易算但只對某些 g 管用，另一條比較費事，卻對每一個 g 都成立。

English: This section solves the inhomogeneous equation: L applied to f equals a given g. Once we hold one particular solution v, every solution is v plus the null space N, an affine subspace. The book gives two routes: one easy but good only for some g, one harder but valid for all.

### 第 2 拍 — 待定係數的想法 / the idea behind undetermined coefficients

公式列：

```
S ( g )  =  0        ⇒        ( S ∘ L ) ( f )   =   S ( g )   =   0
```

中文旁白：第一條路的想法很簡單。如果 g 自己落在某個常係數算子 S 的零化空間裡，那麼把 S 接在 L 後面複合起來，這個複合算子就把 f 殺掉了。而常係數算子的零化空間我們上一集已經完全知道，所以答案一定在那個有限維的空間裡面。

English: The first route is simple. If g itself lies in the null space of some constant coefficient operator S, then S composed after L annihilates f. We already know those null spaces completely, so the answer sits inside that finite dimensional space.

### 第 3 拍 — 最簡單的例子 / the simplest example

公式列：

```
y ′  −  a y  =  e ᵇ ᵗ            f  =  c e ᵇ ᵗ            ( b − a ) c  =  1
```

中文旁白：最簡單的例子是 y 一撇減去 a 乘 y 等於 e 的 b t 次方。右邊被 D 減 b 殺掉，所以拿常數乘上同一個指數去試，代進去得到 b 減 a 再乘那個常數等於一，常數就是 b 減 a 的倒數。取 a 等於負零點四、b 等於零點七，常數約是零點九零九。

English: The simplest example is y prime minus a y equals the exponential of b t. The right side is killed by D minus b, so we try a constant times that exponential and find that b minus a times the constant is one. The constant is the reciprocal of b minus a, here zero point nine one.

### 第 4 拍 — 三角函數的例子 / the trigonometric example

公式列：

```
y ′  −  a y  =  cos b t          S  =  D ² + b ²          f  =  c ₁ sin b t + c ₂ cos b t
```

中文旁白：換成右邊是 cos b t 也一樣。它被 D 平方加 b 平方殺掉，那個零化空間的基底是 sin b t 與 cos b t，所以拿這兩個的線性組合去試，比對係數解一個二元一次方程組，答案是 b 乘 sin 減掉 a 乘 cos，再除以 a 平方加 b 平方。

English: The same works when the right side is the cosine of b t. It is killed by D squared plus b squared, whose null space is spanned by the sine and the cosine, so we try a combination of those and match coefficients. The answer carries b and minus a over a squared plus b squared.

### 第 5 拍 — 有公因式：多帶一個 t 的幂 / a shared factor: one more power of t

公式列：

```
( D − r ) ² f  =  e ʳ ᵗ          ( D ² + 1 ) f  =  sin t          f  =  − t cos t / 2
```

中文旁白：如果 L 與 S 有公因式，就要多帶一個 t 的幂，次數就是公因式重複的次數。畫面上畫的是書上第二個例子：D 平方加一作用在 f 上等於 sin t，解是負二分之一乘 t 再乘 cos t。它的振幅隨 t 線性長大，而右邊始終在正負一之間，這就是共振的雛形。

English: When L and S share a common factor an extra power of t is needed. The picture shows the second example: D squared plus one applied to f equals the sine of t, solved by minus one half t times the cosine. Its amplitude grows while the right side stays bounded.

### 第 6 拍 — 書上為什麼不滿意 / why the book is not satisfied

公式列：

```
L  ∘  R   =   I            R ( λ g )   =   λ R ( g )            R   ≠   R ( g )
```

中文旁白：書上對這個方法並不滿意。它違反了整章的哲學：解方程應該是一個線性的右反元素，一個固定的流程把任何 g 送回對應的 f。可是待定係數法隨著 g 換算子、換試探的形式，遇到不是常係數方程的解的 g 就完全用不上。它只是好算而已。

English: The book is not satisfied. This method violates the philosophy that solving should be a linear right inverse, one fixed process sending any g back to a matching f. Undetermined coefficients changes its operator and its guess with every g, and fails on most of them.

### 第 7 拍 — 參數變異：那個矩陣 / variation of parameters: that matrix

公式列：

```
w ᵢ ⱼ ( t )  =  u ⱼ ⁽ ⁱ ⁻ ¹ ⁾ ( t )              K ₜ  =  w ( t ) · w ( 0 ) ⁻ ¹
```

中文旁白：第二條路叫參數變異，它真的是一個右反元素，對每個 g 都管用，連變係數的 L 都反得了。做法是把第 3 節一階系統的公式翻譯過來：把已知的 n 個獨立解與它們各階導數排成一個矩陣 w，它的行就是一階系統解空間的基底。

English: The second route, variation of parameters, really is a right inverse: it works for every g and even inverts a variable coefficient L. Arrange the n known solutions and their derivatives into a matrix w, whose columns are a basis for the solution space of the first order system.

### 第 8 拍 — 中間那兩個抵消掉 / the two middle factors cancel

公式列：

```
f ( t )  =  w ( t ) · ∫ w ( s ) ⁻ ¹ · g ( s ) d s            ( s  :  0 → t )
```

中文旁白：把這個矩陣代進第 3 節那條解公式，會出現 w 在 t 乘上 w 在零的反矩陣，再乘上一個本身含有 w 在零的積分。因為積分與常矩陣相乘可以交換，中間那兩個就互相抵消，剩下 f 在 t 等於 w 在 t 乘上 w 在 s 的反矩陣作用在 g 上的積分。

English: Substituting that matrix into the section three formula produces w at t times the inverse of w at zero, times an integral carrying w at zero. Integration commutes with a constant matrix, so the middle factors cancel and leave w at t times the integral of w inverse on g.

### 第 9 拍 — 定理 5.1 / theorem 5.1

公式列：

```
Σ ᵢ c ᵢ ′ u ᵢ ⁽ ʲ ⁾  =  0    ( j ≤ n − 2 )        Σ ᵢ c ᵢ ′ u ᵢ ⁽ ⁿ ⁻ ¹ ⁾  =  g
```

中文旁白：現在把右邊取成前面全是零、只有最後一項是 g 的向量，矩陣方程就塌成一組很乾淨的條件：各階導數的加權和前 n 減一條全是零，最後一條等於 g，未知數是那些係數的導數。這就是定理 5.1，解出導數再積回去，f 就是係數乘基底的和。

English: Now take the right side to be the vector that is zero except for g in the last slot. The matrix equation collapses into a clean system in the derivatives of the coefficients: the first n minus one weighted sums vanish and the top one equals g. That is Theorem five point one.

### 第 10 拍 — 書上的例子 / the book's worked example

公式列：

```
y ″  +  y  =  1 / cos x            v  =  x sin x  +  ( log cos x ) cos x
```

中文旁白：書上的例子是 y 兩撇加 y 等於 cos x 的倒數。齊次解的基底是 sin x 與 cos x，但右邊不是常係數方程的解，待定係數法用不上。定理解出兩個係數的導數分別是一與負的正切，積回去就得到 x 乘 sin x，加上 cos x 的對數再乘 cos x。

English: The book example is y double prime plus y equals one over the cosine, which solves no constant coefficient equation. With sine and cosine as the basis, the theorem gives the two derivatives as one and minus the tangent, so the answer is x sine x plus log cosine x times cosine x.

### 第 11 拍 — 彈簧與電路，第 5 節結束 / the spring and the circuit, and the end of section 5

公式列：

```
m d ² x / d t ²  +  k d x / d t  +  c x  =  a sin ω t          Ω  =  √ ( c / m )
```

中文旁白：最後是彈簧。質量乘加速度加上彈性係數乘位移等於零，解是角頻率等於根號 c 除以 m 的正弦波。加上摩擦以後，阻尼小的仍然永遠振盪，只是振幅照指數衰減；阻尼夠大就根本不振動。同一個方程也治理電路，外加週期電壓時就出現相位與共振。

English: The section ends with a spring: mass times acceleration plus stiffness times displacement is zero, a sine whose frequency is the square root of c over m. Light damping still oscillates inside a decaying envelope, heavy damping does not vibrate. A circuit obeys the same equation.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | L ( f ) = g 分成兩條分支：紅的「只對某些 g」、青的「對所有 g」 |
| 2 | N ( S )、N ( L )、N ( S ∘ L ) 的包含關係，箭頭標出 L 把大空間送進 N ( S ) |
| 3 | g = e ᵇ ᵗ 與 f = c e ᵇ ᵗ 兩條成比例的曲線，加上減掉齊次解的第三條 |
| 4 | y ′ − a y = cos b t 的 g 與 f，兩條相位與振幅都不同 |
| 5 | − t cos t / 2 的振幅隨 t 線性長大，± t / 2 是它的包絡線 |
| 6 | 待定係數與參數變異的兩欄對照（適用範圍／是不是單一流程） |
| 7 | w ( t ) 的行列式隨 t 畫出來，恆為 −1 所以每個 t 都可逆 |
| 8 | K ₜ = w ( t ) w ( 0 ) ⁻ ¹ 三個因子，中間那兩個紅的相乘是單位矩陣 |
| 9 | g = ⟨ 0 , … , 0 , g ⟩ 只有最後一格不是零 |
| 10 | v = x sin x + ( log cos x ) cos x 與它的兩個組成，紅虛線標出 ±π/2 |
| 11 | 三種阻尼：不衰減的正弦、指數包絡裡的振盪、完全不振動；灰線是 ± A e ⁻ ᵟ ᵗ |
