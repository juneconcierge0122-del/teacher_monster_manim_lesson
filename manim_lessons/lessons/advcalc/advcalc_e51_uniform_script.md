# advcalc E51 — 第 3 章：均勻連續與函數值的映射

Chapter 3: Uniform Continuity and Function-Valued Mappings

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 14 節「均勻連續與函數值的映射」（書頁 179–182）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e51_uniform.py`（`AdvCalcE51ZH` / `AdvCalcE51EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[51]` / `FORMULAS_ADVCALC[51]`）
- 配音：`manim_lessons/samples/audio_e51/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.28 分（197 秒）／英文 3.24 分（194 秒）

## 升級：把點的映射變成函數的映射

這一節的模式是把一個點到點的映射升級成一個函數值的映射，然後證明點映射的性質會傳過去。
最直接的應用是積分號下微分，而定理 14.3 是後面第 15 節與第 6 章真正會引用的那一條。

畫面上的數字都是算出來的：

- **均勻與不均勻的對比是量出來的**：對 `1/x` 固定 ε = 0.5，程式算出在 0.70 可以取 δ = 0.181，
  在 0.13 只剩 0.0079（差 23 倍），在 0.01 更是差了 3648 倍。
  對照組是單位正方形上的乘積函數：一個 δ = 0.05 在 41 乘 41 個格點上都驗過，處處有效。
- **積分號下微分用三種算法算過**：取 `F(x,y) = x²y³ + sin(xy)`，在 y = 0.8 那一點，
  積分的差商、偏導數的積分、以及手推的封閉形式，三個數字到小數點後八位完全相同（1.06279935）。
  定理保證的是前兩者相等；第三個是拿來確認前兩者沒有一起算錯。
- **定理 14.3 在一組具體的 g、f、h 上驗過**：g 是平方、f 是正弦、h 是三倍角的餘弦，
  斷言餘項除以增量隨著增量縮小而單調下降，最後落到 10⁻² 以下；並斷言 dg 的界確實是 2。

probe 幀抓到三處曲線間距的問題：beat 2 的三條曲線只差 0.24 個單位、
beat 3 的兩條只差 0.07、beat 5 的三條只差 0.16，在畫面上都糊成一條。三處都拉開了。
langscan 抓到 beat 8 表格最後一列的標籤是英文的 `closed form`，改成符號 `I ′ ( y )`。

---

## Beat 0 — δ 可不可以跟位置無關 / may delta ignore where you stand
*配音長度：中文 19.2s ／ 英文 17.8s*

**畫面公式**

```
δ 可不可以跟位置無關   |   may delta ignore where you stand
‖ ξ − η ‖  <  δ            ⇒            ‖ F ( ξ ) − F ( η ) ‖   <   ϵ
```

**旁白（繁中）**

> 第 14 節先把均勻連續說清楚。普通的連續是：給了 ε，δ 可以隨著你站的那一點變。均勻連續要求 δ 只跟 ε 有關，跟站在哪裡無關。差別看起來小，可是整節都靠它。

**Narration (EN)**

> Section 14 begins with uniform continuity. Ordinary continuity lets delta depend on the anchor point at which continuity is asserted. Uniform continuity asks that delta depend on epsilon alone. The difference looks small, and the whole section rests on it.

**動畫**

左邊 1/x 的曲線，兩個錨點各打一點、拉一條灰色虛線到橫軸、並在軸下畫出各自的 δ 長條。
右側說明均勻連續要求 δ 跟位置無關。

## Beat 1 — 這一節的模式：升級 / the pattern: escalation
*配音長度：中文 17.5s ／ 英文 16.8s*

**畫面公式**

```
這一節的模式：升級   |   the pattern: escalation
F  :  M × N  →  X                    φ  :  N  →  Y
```

**旁白（繁中）**

> 這一節的模式是升級：把一個點到點的映射，升級成一個函數到函數的映射，然後證明點映射的性質會傳給函數值的映射。第 15 節與第 6 章都會用到，最直接的應用是積分號下微分。

**Narration (EN)**

> The pattern is escalation: a point-to-point map is raised to a function-valued map, and properties of the first are shown to pass to the second. Section 15 and chapter 6 both use it, and the immediate application is differentiation under the integral sign.

**動畫**

左邊兩個加框的式子（點到點的 F、函數值的 φ），中間一支往下的箭頭。
右側說明點映射的性質會傳給升級後的映射。

## Beat 2 — 一族函數，一個一致範數 / a family of functions, one uniform norm
*配音長度：中文 19.3s ／ 英文 18.3s*

**畫面公式**

```
一族函數，一個一致範數   |   a family of functions, one uniform norm
Y  =  ℬ𝒞 ( M , X )                ‖ f ‖  =  lub  { ‖ f ( ξ ) ‖ }
```

**旁白（繁中）**

> 設定是這樣。F 是乘積開集上的有界連續映射。把第二個變數固定住，剩下的就是 M 上一個有界連續函數，也就是那個函數空間的一個元素。那個空間帶的是一致範數：逐點取上確界。

**Narration (EN)**

> Here is the setup. F is a bounded continuous map on a product open set. Hold the second variable fixed and what remains is a bounded continuous function on M, an element of the space of all of them. That space carries the uniform norm, the least upper bound taken pointwise.

**動畫**

左邊一族三條曲線，中間一支雙向箭頭標出最大的那個間隙。
右側說明一致範數取的是上確界，不是平均。

## Beat 3 — 定理 14.1：連續性傳得過去 / Theorem 14.1: continuity carries across
*配音長度：中文 17.4s ／ 英文 19.4s*

**畫面公式**

```
定理 14.1：連續性傳得過去   |   Theorem 14.1: continuity carries across
F  ∈  C ᵘ            ⇒            η  ↦  F ( · , η )    ∈    C ᵘ
```

**旁白（繁中）**

> 定理 14.1：如果 F 均勻連續，那麼把 η 送到那個函數的映射連續，而且是均勻連續的。左邊是有限維裡的一點，右邊是一個無窮維空間裡的一點，可是連續性照樣傳過去。

**Narration (EN)**

> Theorem 14.1: if F is uniformly continuous, then the map sending eta to that function is continuous, in fact uniformly continuous. The left side is a point of a finite-dimensional space and the right side a point of an infinite-dimensional one, and continuity passes across.

**動畫**

左邊兩條靠近的曲線，上下兩條灰色虛線構成一個 ε 帶。
右側說明兩個參數值夠近時，兩條曲線整條落在同一個帶裡。

## Beat 4 — 證明只有兩行 / the proof is two lines
*配音長度：中文 18.5s ／ 英文 16.5s*

**畫面公式**

```
證明只有兩行   |   the proof is two lines
‖ η − ν ‖ < δ      ⇒      ‖ F ( ξ , η ) − F ( ξ , ν ) ‖ < ϵ        ∀ ξ
```

**旁白（繁中）**

> 證明只有兩行，完全靠均勻連續。給了 ε 取到 δ，再把第一個變數取成同一個，就得到：兩個 η 夠近時，兩個函數在每一點都夠近。而每一點都近，就是一致範數下近。

**Narration (EN)**

> The proof is two lines and rests entirely on uniformity. Choose delta for epsilon, then take the first variable to be the same on both sides, and two nearby etas give two functions close at every point. Close at every point is close in the uniform norm.

**動畫**

左邊三行證明的式子，下面一個加框的結論。
右側說明第一個變數兩邊取成同一個。

## Beat 5 — 推論：積分對參數連續 / a corollary: the integral is continuous in y
*配音長度：中文 16.0s ／ 英文 16.6s*

**畫面公式**

```
推論：積分對參數連續   |   a corollary: the integral is continuous in y
y    ↦    ∫ ₀ ¹  F ( x , y )  d x            ∈    C ⁰
```

**旁白（繁中）**

> 推論是一個熟悉的事實：單位正方形上均勻連續的 F，對 x 積分之後是 y 的連續函數。理由是那個映射就是「積分」這個有界線性泛函，接上剛才那個連續映射。

**Narration (EN)**

> The corollary is a familiar fact: for F uniformly continuous on the unit square, integrating over x leaves a continuous function of y. The reason is that this map is the bounded linear functional of integration composed with the continuous map just built.

**動畫**

左邊三條被積函數的曲線（三個 y 值），右邊一張 y 與積分值的表。
註腳說明理由不是計算而是合成。

## Beat 6 — 定理 14.2：可微也傳得過去 / Theorem 14.2: so does differentiability
*配音長度：中文 16.1s ／ 英文 17.8s*

**畫面公式**

```
定理 14.2：可微也傳得過去   |   Theorem 14.2: so does differentiability
[ dφ ᵦ ( η ) ] ( ξ )    =    dF ² ⟨ ξ , β ⟩ ( η )
```

**旁白（繁中）**

> 定理 14.2 把連續換成可微。如果對第二個變數的偏微分存在，而且它是有界的、均勻連續的，那麼那個函數值的映射可微，而且它的微分逐點就是那個偏微分。

**Narration (EN)**

> Theorem 14.2 upgrades continuity to differentiability. If the partial differential in the second variable exists and is a bounded, uniformly continuous function of the point, then the function-valued map is differentiable and its differential is that partial taken pointwise.

**動畫**

左邊兩個方塊（假設、結論）與一個加框的逐點公式。
右側說明微分逐點就是那個偏微分。

## Beat 7 — 關鍵是換一個讀法 / the key is a change of reading
*配音長度：中文 16.8s ／ 英文 16.2s*

**畫面公式**

```
關鍵是換一個讀法   |   the key is a change of reading
Δ F ² ⟨ ξ , β ⟩ ( η )    =    [ Δ φ ᵦ ( η ) ] ( ξ )
```

**旁白（繁中）**

> 證明的關鍵是一個換讀法：F 對第二個變數的增量，逐點看就是那個函數值映射的增量。左邊是 X 裡的一個向量，右邊是函數空間裡的一個函數，可是它們是同一件事寫兩次。

**Narration (EN)**

> The proof turns on a change of reading: the increment of F in the second variable, read pointwise, is the increment of the function-valued map. One side is a vector in X and the other a function in the big space, yet they are the same thing written twice.

**動畫**

左邊三行式子，把 F 對第二個變數的增量與函數值映射的增量對在一起。
右側說明左邊是 X 裡的向量、右邊是函數空間裡的函數。

## Beat 8 — 積分號下微分 / differentiating under the integral
*配音長度：中文 18.2s ／ 英文 17.4s*

**畫面公式**

```
積分號下微分   |   differentiating under the integral
d / d y   ∫ ₀ ¹  F  d x        =        ∫ ₀ ¹  ∂F / ∂y   d x
```

**旁白（繁中）**

> 於是得到積分號下微分：正方形上 F 連續、對 y 的偏導數存在而且均勻連續，那麼對 x 積分之後是 y 的可微函數，導數就是把偏導數放進積分號裡。程式在一個例子上把兩邊都算過。

**Narration (EN)**

> That gives differentiation under the integral sign: with F continuous on the square and its partial in y uniformly continuous, integrating over x leaves a differentiable function of y whose derivative is the partial taken inside. Both sides are computed here on an example.

**動畫**

左邊一個加框的積分號下微分公式，下面一張表列出三種算法的數值。
三個數字到小數點後八位相同。

## Beat 9 — 定理 14.3：把「接上 g」當成映射 / Theorem 14.3: composition as a map
*配音長度：中文 19.4s ／ 英文 20.5s*

**畫面公式**

```
定理 14.3：把「接上 g」當成映射   |   Theorem 14.3: composition as a map
G ( f )  =  g ∘ f            [ dG ( h ) ] ( s )  =  dg ( f ( s ) ;  h ( s ) )
```

**旁白（繁中）**

> 定理 14.3 是後面真正用到的那一條。把「接上 g」本身當成一個映射：f 送到 g 接上 f。如果 g 處處可微而且微分有界均勻連續，那麼這個映射可微，微分在每一點就是 g 在那一點的微分。

**Narration (EN)**

> Theorem 14.3 is the one actually used later. Make composition by g into a map of its own: f goes to g after f. If g is differentiable with a bounded uniformly continuous differential, that map is differentiable, and its differential at each point is the differential of g there.

**動畫**

左邊兩個方塊（f 與 g 接上 f）與一個加框的逐點公式。
右側說明分號左邊是取微分的那一點、右邊是微分作用的向量。

## Beat 10 — T 真的是有界線性映射 / T really is a bounded linear map
*配音長度：中文 18.5s ／ 英文 17.2s*

**畫面公式**

```
T 真的是有界線性映射   |   T really is a bounded linear map
‖ T ‖  ≤  b            [ dG ( h ) ] ( t )  =  dg ¹ ( h ₁ ) + dg ² ( h ₂ )
```

**旁白（繁中）**

> 最後要驗的是那個 T 真的落在 Hom 裡：加法與齊次都逐點驗，範數不超過 dg 的界。還有一個乘積版本：定義域拆成兩個因子時，微分是兩個偏微分各配一支——這正是下一集算第一變分的式子。

**Narration (EN)**

> What is left is checking that T really lies in Hom: additivity and homogeneity hold pointwise, and its norm is at most the bound on dg. There is a product version too: split the domain in two and each factor gets its own partial, which is what the next episode needs.

**動畫**

左邊兩行 Hom 的驗證式子，下面一張 t 與餘項比值的表。
右側說明那一欄掉下去，所以餘項真的是小 o。

---

## 為什麼要三種算法

積分號下微分那一拍如果只算兩個數字，兩者相等只證明「程式的兩段程式碼一致」。
加上手推的封閉形式之後，三個數字相同才排除掉「兩邊一起算錯」的可能。
這一集的被積函數是 `x²y³ + sin(xy)`，它對 x 的積分有封閉形式
`y³/3 + (1 − cos y)/y`，微分之後就是第三個數字。

## 這一節唯一會被引用的定理

書上自己說了：這一節的東西後面只有定理 14.3 真的會用到。
它把「接上 g」當成一個映射，而下一集算第一變分時用的正是它的乘積版本——
定義域拆成兩個因子時，微分是兩個偏微分各配一支。
