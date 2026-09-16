# advcalc E76 — 第 6 章：對參數的可微相依

Chapter 6: Differentiable Dependence on Parameters

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 2 節「對參數的可微相依」（書頁 274–275），**整節一集講完**。

**這一節整節沒有習題**，275 頁講完直接進 §3——這是這本書裡**第四次**（前三次是第 2 章 *§7、第 4 章 *§12、第 5 章 §5）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e76_parameters.py`（`AdvCalcE76ZH` / `AdvCalcE76EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[76]` / `FORMULAS_ADVCALC[76]`）
- 配音：`manim_lessons/samples/audio_e76/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 207.8 秒（3:27）／英文 201.7 秒（3:21）
- YouTube（私人）：中文 https://youtu.be/Dl0d7Kk_Ha0 ／英文 https://youtu.be/UWsZt_oZLGo

## 這一節在做什麼

§1 問解存不存在、活多遠；**§2 問它怎麼動**。固定 J 與球，初始點就決定一條解：

```
⟨ t ₁ , α ₁ ⟩    ↦    f                J × N   →   V   =   ℬ 𝒞 ( J , W )
```

**定理 2.1**：這個映射連續。**定理 2.2**：若 dF 一致連續，它連續可微。

**兩個證明都不是新工作。** K 只多吃兩個變數，同樣那兩個估計再跑一次，只有一處不同——
N 取半徑 r/2 的球，於是球心那一項變成 r/2 + δm，雙重要求就成了

```
δ   <   r / ( 2 ( m + c r ) )   =   0.125              ( §1 是 0.25 )
```

**正好一半。這就是連續相依的全部代價。**

**接下來全是引用**：第 4 章定理 9.2（帶參數的不動點定理）給連續，定理 9.4 給可微，
前提是 K 自己連續可微。而 K 拆成兩步都已經證過：

```
f   ↦   h  ,  h ( s ) = F ( s , f ( s ) )        Ch 3 , 14.3       𝒞 ¹
h   ↦   k  ,  k ( t ) = ∫ h ( s ) d s            V → W  有界線性     𝒞 ¹
```

**三個偏微分裡兩個算得出來**：dK² = I（增量就是 ξ 本身）、dK¹(h) = −h F(t₁, f(t₁))
（把下限往前挪等於扣掉一小段積分）。三個都連續，第 3 章定理 8.3 接成連續可微。

**推論**：解在任一點的值對初始值可微——α ↦ f 連續可微，而 π ₛ : f ↦ f(s) 有界線性。

## 這一集用的例子

**整章唯一有閉式解映射的初始值問題**，所以連「解對初始值的導數」都能核到真值：

```
x ′  =  t + x       通過 ⟨ t ₁ , α ₁ ⟩      ⟹      f ( t )  =  ( α ₁ + t ₁ + 1 ) e ^( t − t ₁ ) − t − 1
```

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 閉式解真的是解 | 三組 ⟨t₁,α₁⟩ × 三個 t，數值微分 | 誤差 ≤ 1e-5 |
| 它通過該通過的點 | f(t₁) 對 α₁ | 差 < 1e-12 |
| δ 正好砍半 | r/(2(m+cr)) 對 r/(m+cr) | 0.125 ／ 0.25 |
| 雙重要求在該處恰好相等 | r/2 + δm 對 (1−δc)r，δ = 0.125 | 兩邊相等 |
| 在舊上限處被違反 | 同兩式，δ = 0.25 | 左 > 右 |
| dK¹ 的真值 | −F(t₁, f(t₁))，t₁ = 0.5、α₁ = 0.3 | -0.8000 |
| dK¹ 的數值商 | h = 1e-2、1e-3、1e-4 | -0.809030, -0.800900, -0.800090 |
| 解對初始值的導數 | exp(s − t₁)，s = 1、t₁ = 0 | 2.718282 |
| 數值商（映射是仿射，所以精確） | ε = 1e-1 到 1e-4 | 全部 = 2.718282 |

**那一把解張開的倍率就是 2.718282**——不是虛線的長度，是右邊那段對左邊那段的比。
第一版的說明話寫成「虛線的長度就是 2.718282」，是錯的（長度是 3.262），probe 幀抓到。

## 這一輪抓到的錯

- **上下兩排畫得一模一樣。** 第 7 拍要說「假設從 Lipschitz 升級成 dF 一致連續，
  結論就從連續升級成連續可微」，我畫了兩排 F → K → f，同標籤同顏色，
  差別只有小到看不清的 9.2 / 9.4——整拍唯一要說的事被畫成同一件事重複兩次。
  改成上排灰配 𝒞 ⁰、下排橘配 𝒞 ¹，兩排一眼看出不同。
  **這是 E72「兩個矩陣其實是同一個」、E74「δc 與 δm 疊成一條線」的第三次。**
- **說明話指錯東西。** 第 11 拍寫「虛線的長度就是那個 2.718282」，可是虛線長度是 3.262，
  2.718282 是**倍率**。改法不是改話而是補圖：把起點那一段也畫出來，倍率才有東西可比。
- **圓與方框壓到註腳** 三處、**表格跑進說明列** 三處（bounds / collide），
  **表格列裡混中文** 六處加一處 `fix` 混進符號（langscan）。

## 十一拍

### 第 1 拍 — 解怎麼隨初始點變 / how the solution moves with the point

公式列：

```
⟨ t ₁ , α ₁ ⟩    ↦    f                J × N   →   V
```

中文旁白：第 2 節問的是：解怎麼隨初始點變？固定一個區間 J 與函數空間裡的一個球，把初始點送到它決定的那條解，就得到一個從 J 乘 N 到函數空間的映射。這一節要問的就是這個映射連不連續、可不可微。

English: Section 2 asks how the solution varies with the initial point. Fix an interval and a ball in the function space, send the initial point to the solution it determines, and you have a map from that neighbourhood into the function space. Is it continuous, and is it differentiable?

### 第 2 拍 — 定理 2.1 / theorem 2.1

公式列：

```
∃ !   f : J → U                 J × N   →   V
```

中文旁白：定理 2.1：L 乘 U 是初始點的鄰域，F 在上面有界、連續，而且對第二個變數一致 Lipschitz。那麼有一個鄰域 J 乘 N，其中每一點都恰有一條從 J 到 U 的解通過，而且初始點送到解的那個映射是連續的。

English: Theorem 2.1. On a product neighbourhood of the initial point let F be bounded, continuous, and Lipschitz in its second variable uniformly over t. Then some neighbourhood has exactly one solution through each of its points, and the map sending point to solution is continuous.

### 第 3 拍 — K 多吃兩個變數 / K takes two more arguments

公式列：

```
K ( t ₁ , α ₁ , f ) ( t )  =  α ₁ + ∫ F ( s , f ( s ) ) d s      ( s : t ₁ → t )
```

中文旁白：證明就是把上一集的計算重跑一次，只是 K 多吃兩個變數。現在 K 帶著 t 一與 α 一：把 f 送到 α 一加上從 t 一積到 t 的那個積分。對固定的 f，K 顯然對初始點連續。

English: The proof reruns last episode's calculation with K taking two more arguments. K now carries the initial time and value: it sends f to that value plus the integral taken from the initial time out to t. For each fixed f, K is plainly continuous in the initial point.

### 第 4 拍 — N 取半徑的一半 / N is the ball of half the radius

公式列：

```
‖ K ( t ₁ , α ₁ , ᾱ ₀ ) − ᾱ ₀ ‖   ≤   ‖ α ₁ − α ₀ ‖ + δ m   ≤   r / 2 + δ m
```

中文旁白：δ 要減半。N 取半徑是 r 一半的那個球，於是 K 作用在常數函數上，離球心不超過 α 一減 α 零的長度再加 δ m，也就是 r 的一半加 δ m。壓縮那一半的估計完全不動。

English: Delta has to halve. Take N to be the ball of half the radius; then K applied to the constant function sits within the distance from the old centre plus delta times m, that is, half of r plus delta times m. The contraction half of the estimate is untouched.

### 第 5 拍 — 代價：δ 砍半 / the price: delta halves

公式列：

```
δ  <  r / ( 2 ( m + c r ) )   =   0.125            0.25 / 2
```

中文旁白：兩個要求疊起來：r 的一半加 δ m 要小於一減 δ c 再乘 r。算出來是 δ 小於 r 除以二倍的 m 加 c r——正好是上一集那個上限的一半。多要一個連續相依，代價就是區間砍半。

English: Stack the two demands: half of r plus delta times m below one minus delta c, times r. That works out to delta below r over twice m plus c r, exactly half of last episode's ceiling. Asking for continuous dependence as well costs half the interval.

### 第 6 拍 — 套第 4 章定理 9.2 / chapter 4's theorem 9.2

公式列：

```
Ch 4  ,  9.2                ⟨ t ₁ , α ₁ ⟩   ↦   f
```

中文旁白：有了這個 δ，就把第 4 章的定理 9.2 套上去——那是帶參數的不動點定理，它說不動點對參數連續。這裡的參數正是初始點，所以解對初始點連續，定理 2.1 就證完了。

English: With that delta, apply Theorem 9.2 of chapter 4, the fixed-point theorem with a parameter: the fixed point depends continuously on the parameter. Here the parameter is precisely the initial point, so the solution depends continuously on it, and Theorem 2.1 is proved.

### 第 7 拍 — 要可微就要更多 / differentiability asks for more

公式列：

```
Ch 4  ,  9.4                d K     ⇒     d f
```

中文旁白：要可微就要更多。第 4 章的定理 9.4 說不動點對參數連續可微，只要那個映射本身連續可微。於是問題變成 K 連不連續可微，而這只要 F 的微分存在、而且在 L 乘 U 上一致連續。

English: Differentiability asks for more. Theorem 9.4 of chapter 4 says the fixed point is continuously differentiable in the parameter as soon as the map itself is. So the question becomes whether K is, and for that it is enough that the differential of F exist and be uniformly continuous.

### 第 8 拍 — 定理 2.2 / theorem 2.2

公式列：

```
d F      ,      L × U            ⇒         f  ∈  𝒞 ¹
```

中文旁白：定理 2.2：L 乘 U 是初始點的鄰域，F 有界，而且 dF 存在、有界、在 L 乘 U 上一致連續。那麼在定理 2.1 的框架裡，解是初始值的連續可微函數。假設從 Lipschitz 升級成一致連續的微分。

English: Theorem 2.2. On a product neighbourhood of the initial point let F be bounded with its differential existing, bounded, and uniformly continuous there. Then in the setting of Theorem 2.1 the solution is a continuously differentiable function of the initial value.

### 第 9 拍 — 把 K 拆成兩步複合 / K as a composition

公式列：

```
h  ↦  ∫ h ( s ) d s     ( s : t ₁ → t )              Ch 3  ,  14.3
```

中文旁白：證明把 K 拆成兩步複合。從 t 一積到 t 這個動作，是函數空間到自己的有界線性映射，而且對 t 一連續相依；而把 f 送到 s 對應 F 帶入 s 與 f s 那一步，由第 3 章定理 14.3 連續可微。

English: The proof splits K into a composition. Integrating from the initial time out to t is a bounded linear map of the function space into itself, depending continuously on that time; and sending f to F at s and f of s is continuously differentiable by Theorem 14.3 of chapter 3.

### 第 10 拍 — 三個偏微分 / the three partial differentials

公式列：

```
d K ²  =  I            d K ¹ ( h )  =  − h F ( t ₁ , f ( t ₁ ) )
```

中文旁白：接著算三個偏微分。對 f 那一個剛才有了；對 α 一那一個是恆等映射，因為增量就是 ξ 本身；對 t 一那一個是負的 h 乘 F 在 t 一與 f t 一的值。三個都連續，第 3 章定理 8.3 就接成連續可微。

English: Then the three partial differentials. The one in f has just been done; the one in the initial value is the identity, since the increment is the vector itself; the one in the initial time is minus h times F at that time. All three are continuous, and Theorem 8.3 of chapter 3 joins them.

### 第 11 拍 — 推論，與第 2 節的結束 / the corollary, and the end of section 2

公式列：

```
∂ f ( s ) / ∂ α ₁   =   exp ( s − t ₁ )                F ( λ , t , α )
```

中文旁白：推論：解在任一點 s 的值，是初始值的可微函數。因為 α 送到那條解連續可微，而取值那一步是有界線性、自動連續可微，複合起來就是。定理 2.3 把它做成整體的，書上不給證明。第 2 節整節沒有習題。

English: Corollary: the value of a solution at any point is a differentiable function of the initial value, since the map to it is continuously differentiable and evaluation is bounded and linear. Theorem 2.3 makes that global. Section 2 has no exercises at all.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 通過五個不同初始值的解張成一把；左邊一段粗線標出 N，右表把那個映射寫成四列 |
| 2 | L × U 的大框與 J × N 的小框，小框裡三個初始點各配一個顏色——小框比大框小很多 |
| 3 | 三條從不同 ⟨t₁,α₁⟩ 出發的解，各自的起點用虛線接到時間軸：同一個 K，起點從固定變可動 |
| 4 | 兩個同心圓：𝔘 半徑 r、N 半徑 r/2，兩支箭頭比出半徑；右表四列把兩個估計並排 |
| 5 | r/2 + δm 與 (1−δc)r 兩條線在 0.125 交叉，舊的 0.25 也標出來；右表的列在交點處換色 |
| 6 | 同一把解加一條虛線量出它們在右端的散開——初始點動一點，整條解只動一點 |
| 7 | 上排灰（𝒞 ⁰、Lipschitz、9.2）、下排橘（𝒞 ¹、dF、9.4），同一條 F → K → f 升級一次 |
| 8 | 那把解再出現一次，每條的起點加一支箭頭標出初始值的方向——最後一列沿它微分 |
| 9 | f → h → k 三個方塊串成 K = ∫ ∘ F，兩支箭頭各標出它憑什麼是 𝒞 ¹ |
| 10 | f（青）與被積函數 F(s,f(s))（紫）同框，起點下方紅色一小段是 h；右表的商收向 −0.8000 |
| 11 | 那把解最後一次出現，左右各一條虛線量出起點與 s 處的散開，比值就是 e |
