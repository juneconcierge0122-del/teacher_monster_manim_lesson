# advcalc E83 — 第 6 章：Sturm-Liouville 系統與特徵基底

Chapter 6: Sturm-Liouville Systems and the Eigenbasis

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 6 節的**後半**，**§6 到此結束**（書頁 297 下半–299）。習題 6.1–6.12 在 300–301。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e83_sturm.py`（`AdvCalcE83ZH` / `AdvCalcE83EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[83]` / `FORMULAS_ADVCALC[83]`）
- 配音：`manim_lessons/samples/audio_e83/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 259.3 秒（4:19）／英文 201.3 秒（3:21）
- YouTube（私人）：中文 https://youtu.be/pElyyNI3DkY ／英文 https://youtu.be/1YOX60sK4_o

## 這半節在做什麼

上一集把「自伴」弄清楚，這一集用它證出整章最重的結果。引擎是 **引理 6.4** 的不等式：

```
| ( ( T − λ ) f , f ) |   ≥   m ‖ f ′ ‖ ₂ ²   +   ‖ f ‖ ₂ ²          f ∈ M
```

證明是分部積分一次：端點項被邊界條件殺掉，剩下兩個積分分別被那兩個範數由下界住。
**那個條件買到的不是某一個 f，是整個子空間上的一致下界。**

**定理 6.1**：正則 Sturm-Liouville 系統的右逆是 𝒞 ⁰ 到自己的**緊自伴**映射。兩步：
Schwarz 加引理給出 ‖ f ‖ ₂ ≤ ‖ g ‖ ₂ 與 ‖ f ′ ‖ ₂ ≤ ‖ g ‖ ₂ / √m；那個界翻成
| f ( y ) − f ( x ) | ≤ ‖ f ′ ‖ ₂ | y − x | ^ ( 1 / 2 )，於是一致等度連續、全有界、閉包緊。

**定理 6.2** 給出 M 的一組完全由特徵向量構成的正交規範基底，再把特徵值翻譯回去：

```
S φ ₙ  =  r ₙ φ ₙ        ⇒        T φ ₙ  =  ( ( 1 + λ r ₙ ) / r ₙ ) φ ₙ
```

右逆的特徵值聚集到零、T 的特徵值就跑向負無窮。**引理 6.5** 處理兩個範數，
結論是展開式在**兩個範數底下都收斂**——所以是一致收斂，不只平方平均。

## 這一集用的例子

兩個系統：c ₂ = 1 + t ²、c ₀ = −1 在 [ 0 , 1 ]（拍 2、3、7、8）；T = D ² 在 [ 0 , π ]（拍 9–11）。

| 要驗的事 | 結果 |
|---|---|
| 引理 6.4，λ = +2 | 四個試驗函數的比值 1.533／1.545／1.387／1.419，**全部 ≥ 1** |
| λ = −5（太小）| 0.889／0.909 **掉到 1 以下**，後兩個仍撐住 |
| 端點項被邊界條件殺掉 | ≤ 1e-13 |
| 引理 6.3 的行列式 | 1.1199 ≠ 0 |
| sin n x 滿足 f ″ = − n ² f | 殘差 0 |
| 正交性 | n ≠ m 為零；自己和自己是 π / 2 |
| 一致收斂（f = x ( π − x )）| ‖ f − S ‖ ∞：1.05e-01 → 2.92e-02 → 1.33e-02 → 4.85e-03 |

## 這一輪抓到的錯

- **表頭指著另一個算子（最嚴重）。** 表上寫 `T = D ² , [ 0 , π ] , λ = 2`，底下三個數
  （2.2527／1.1199／1.1199）卻是 `( ( 1 + t ² ) u ′ ) ′ − u` 在 **[ 0 , 1 ]** 上積出來的。
  **用封閉解核過**：D ² 在 [ 0 , π ]、λ = 2 應為 cosh ( √2 π ) = 42.5157、sinh ( √2 π ) / √2 = 30.0548。
  三道自動關卡都看不到這種錯。改標成真正算的那個系統，docstring 也一起改。
- **同一個顏色在同一張畫面裡代表兩件事**：圖裡橘色是 λ = +2 的柱，表裡橘色是「這一列失格」。
  失格的列改用紅色，與紅柱同義。
- **說明話講斜率，套管管的是函數值。** 灰色套管 min ( √t , √(1−t) ) / √m 界的是 | f |；
  端點處 √ 的切線是垂直的，對斜率什麼都沒說。
- **圖例兩條的文字一模一樣**（都寫 ‖ f ′ ‖ ₂ = 1），看圖的人分不出哪條是哪條 → 改標 f ₁／f ₃。
- **一個標籤按「半長 1.46」擺，可是線只畫到 0.86**——飄在它所指的線上方 0.6 之外，還頂出畫面到 1.70。
- 那個點標成 `h`，但它是**兩個分量的和** → 改標 `f`，`h` 移到 N 方向的分量上。
- 字元：`⌣` 不是任何緊算子記號（換掉）、`両` 是日文字形（改 `兩`）、`S [ U ] ‾` 的上槓不會蓋在上面（改 `cl ( S [ U ] )`，並把 `cl` 加進 langscan 白名單）。
- 中文旁白數錯列（英文版是對的）：「第二列是正則」→「第二、三列是正則，第四、五列各是一種奇異」。

## 十一拍

### 第 1 拍 — 這一集的路線圖 / the route of this episode

公式列：

```
( T − λ ) S  =  I          S *  =  S          Ch 5 , 5.1   ⇒   { φ ₙ }
```

中文旁白：上一集把自伴邊界條件講清楚了，這一集要用它證出整章最重的那個結果。路線是這樣：邊界條件切出來的子空間是零化空間的補，於是 T 減 λ 有一個右逆；接著證這個右逆又緊又自伴；然後第五章的特徵基底定理就整套搬得過來。

English: Last episode pinned down the self-adjoint boundary condition; now it earns the chapter's heaviest result. The subspace it cuts out complements the null space, so T minus lambda has a right inverse. That inverse is compact and self-adjoint, and chapter five then applies.

### 第 2 拍 — 引理 6.4 的不等式 / the inequality of Lemma 6.4

公式列：

```
| ( ( T − λ ) f , f ) |   ≥   m ‖ f ′ ‖ ₂ ²  +  ‖ f ‖ ₂ ²          f  ∈  M
```

中文旁白：引理 6.4 是引擎。假設邊界條件是前面列出的第一、第二或第四種，c 二在閉區間上不小於某個正的 m，而且 λ 至少比 c 零大一。那麼對子空間裡的每一個 f，T 減 λ 作用在 f 上與 f 做內積，絕對值不小於 m 乘導數的平方範數加上 f 的平方範數。

English: Lemma 6.4 is the engine. Take the first, second or fourth condition, c two at or above a positive m, lambda at least one above c zero. Then for f in the subspace, the inner product of f with T minus lambda of f beats m times the squared norm of f prime plus that of f.

### 第 3 拍 — 分部積分一次 / one integration by parts

公式列：

```
∫ c ₂ ( f ′ ) ² d t  +  ∫ ( λ − c ₀ ) f ² d t   =   ( ( λ − T ) f , f )
```

中文旁白：怎麼來的？分部積分一次。λ 減 T 作用在 f 上與 f 的內積，等於一個端點項，加上 c 二乘導數平方的積分，再加上 λ 減 c 零乘 f 平方的積分。那三種邊界條件剛好讓端點項變成零，剩下的兩個積分就分別被那兩個平方範數由下面界住。

English: One integration by parts does it. The inner product of f with lambda minus T applied to f is an endpoint term, plus the integral of c two times f prime squared, plus the integral of lambda minus c zero times f squared. The listed conditions kill the endpoint term.

### 第 4 拍 — M 是零化空間的補 / M is a complement of the null space

公式列：

```
M  ∩  N ( T − λ )  =  { 0 }            𝒞 ⁰  =  M  ⊕  N ( T − λ )
```

中文旁白：不等式右邊是正的，所以子空間裡只有零向量會被 T 減 λ 送到零。引理 6.3 說這時候子空間就是零化空間的補；而零化空間是二維的，兩個邊界泛函把它等同於平面。於是 T 減 λ 有一個由這個子空間決定的自伴右逆。

English: The right side is positive, so the only vector of the subspace killed by T minus lambda is zero. Lemma 6.3 then makes the subspace a complement of the null space, which is two dimensional and identified with the plane by the two boundary functionals.

### 第 5 拍 — 名詞：Sturm-Liouville 系統 / terminology: a Sturm-Liouville system

公式列：

```
T f  =  ( c ₂ f ′ ) ′  +  c ₀ f            l ₁ ( f )  =  l ₂ ( f )  =  0
```

中文旁白：名詞時間。所謂 Sturm-Liouville 系統，是一個形式自伴的二階算子，先把導數乘上 c 二再微分，加上 c 零乘 f，配上一個自伴的邊界條件。如果 c 二在閉區間上處處不為零，就叫正則；如果它在端點變成零，或者區間變成無窮長，就叫奇異。

English: A Sturm-Liouville system is a formally self-adjoint second order operator, f prime weighted by c two then differentiated, plus c zero times f, with a self-adjoint boundary condition. It is regular if c two is nowhere zero, singular if c two vanishes at an end.

### 第 6 拍 — 定理 6.1：緊的自伴右逆 / Theorem 6.1: a compact self-adjoint right inverse

公式列：

```
S  :  𝒞 ⁰ ( [ a , b ] )   →   𝒞 ⁰ ( [ a , b ] )            S *  =  S
```

中文旁白：定理 6.1：正則、c 二為正、λ 取得夠大的時候，那個右逆是把連續函數空間映到自己的緊自伴算子。緊這個字是關鍵，因為第五章的特徵基底定理要的正好就是緊加自伴。證明分兩步，先從引理擠出兩個界，再用那兩個界換到等度連續。

English: Theorem 6.1: for a regular system with c two positive and lambda large enough, the right inverse is a compact self-adjoint map of the continuous functions into themselves. Compact is the key word, since that is just what chapter five asks for.

### 第 7 拍 — 第一步：兩個界 / first step: the two bounds

公式列：

```
‖ f ‖ ₂   ≤   ‖ g ‖ ₂              ‖ f ′ ‖ ₂   ≤   ‖ g ‖ ₂  /  √ m
```

中文旁白：第一步。令 g 等於 T 減 λ 作用在 f 上。內積的絕對值不超過兩個二範數相乘，配上引理給的下界，先得到 f 的二範數不超過 g 的二範數；再代回去一次，得到導數的二範數不超過 g 的二範數除以根號 m。所以右逆把單位球送進函數與導數都被界住的集合。

English: First step. Let g be T minus lambda applied to f. The inner product is at most the product of the two norms, and with the lemma's lower bound that gives the two-norm of f at most that of g. Feeding it back bounds the two-norm of f prime by that of g over root m.

### 第 8 拍 — 第二步：等度連續，所以緊 / second step: equicontinuous, hence compact

公式列：

```
| f ( y ) − f ( x ) |   ≤   ‖ f ′ ‖ ₂  | y − x | ¹ ᐟ ²   ≤   | y − x | ¹ ᐟ ²  /  √ m
```

中文旁白：第二步。導數被界住，積分的 Schwarz 不等式就給出一個 Hölder 型的估計：兩點的函數值之差，不超過導數的二範數乘上兩點距離的平方根。於是像集一致等度連續，值域也有界，第四章的定理給出全有界，閉包是緊的，所以右逆是緊算子。

English: Second step. With f prime bounded, the Schwarz inequality gives a Holder type estimate: the gap between two values of f is at most the two-norm of f prime times the square root of the distance. So the image is uniformly equicontinuous and totally bounded.

### 第 9 拍 — 定理 6.2：特徵基底 / Theorem 6.2: the eigenbasis

公式列：

```
S φ ₙ  =  r ₙ φ ₙ        ⇒        T φ ₙ  =  ( ( 1 + λ r ₙ ) / r ₙ ) φ ₙ
```

中文旁白：定理 6.2：存在一組完全由 T 的特徵向量組成的正交規範基底。把第五章的定理用在右逆上得到它的特徵基底，再把特徵值翻譯回去：右逆把 φ 乘上 r，那麼 T 就把 φ 乘上一加 λ r 再除以 r。右逆的特徵值聚集到零，T 的特徵值就跑向負無窮。

English: Theorem 6.2: there is an orthonormal basis made entirely of eigenvectors of T. Apply chapter five to the right inverse, then translate its eigenvalues back: if the inverse scales phi by r, then T scales phi by one plus lambda r, over r. Those r pile up at zero.

### 第 10 拍 — 引理 6.5：兩個範數都收斂 / Lemma 6.5: convergence in both norms

公式列：

```
f  =  Σ b ₙ φ ₙ        ‖ f − S ₙ ‖ ∞  →  0        ‖ f − S ₙ ‖ ₂  →  0
```

中文旁白：最後一塊是一致收斂。引理 6.5 說：如果算子從一個範數映到另一個壓得住它的範數是緊的，那麼展開式在兩個範數底下都收斂。一致範數壓得住二範數，所以子空間裡的 f 的展開式不只是平方平均收斂，它是一致收斂。

English: The last piece is uniform convergence. Lemma 6.5: if an operator is compact from one norm into a second that dominates it, the expansion converges in both. The uniform norm dominates the two-norm, so an f in the subspace is a uniform limit of its series.

### 第 11 拍 — 一個例子，第 6 節結束 / one example, and the end of section 6

公式列：

```
T  =  D ²      f ( 0 ) = f ( π ) = 0      φ ₙ = sin n x      μ ₙ = − n ²
```

中文旁白：收個尾。最簡單的例子是二次微分算子配上兩端為零，特徵值是負的 n 平方，特徵函數是 sin n x，彼此正交。第 6 節到這裡結束，後面接的是十二道習題。下一集就把這個例子從頭到尾完整走一遍。

English: To close. The simplest example is the second derivative with both ends held at zero: eigenvalues minus n squared, eigenfunctions the sines of n x, mutually orthogonal. Section 6 ends here, followed by twelve exercises, and next episode walks this example from start to finish.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | T → M → S → 緊自伴 → 特徵基底 這條推理鏈的方塊圖 |
| 2 | 四個試驗函數的柱狀圖，橘柱（λ = +2）全在虛線上、紅柱（λ = −5）有兩根掉下去 |
| 3 | 分部積分之後兩條形狀完全不同的曲線，底下的面積相同 |
| 4 | M 與 N ( T − λ ) 兩條線只在原點相遇，f 是兩個分量的和 |
| 5 | 正則與奇異的 c ₂ 對照：一條離開軸、一條在端點碰到零 |
| 6 | S [ U ] 裡的一串灰點收斂到紫點 |
| 7 | 每一列的紫點都在橘點右邊、兩個都在豎線左邊（兩個界） |
| 8 | 根號型的套管，兩條函數整條都關在裡面 |
| 9 | r ₙ 往右擠成一堆、μ ₙ 往左散開，順序整個反過來 |
| 10 | N = 1 與 N = 3 的誤差曲線，各自關在自己那對虛線裡 |
| 11 | sin n x 的正交性矩陣：對角線是 π / 2，其他格子是零 |
