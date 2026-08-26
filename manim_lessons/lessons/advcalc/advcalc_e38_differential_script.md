# advcalc E38 — 第 3 章：微分

Chapter 3: The Differential

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 6 節（書頁 140–144）。書頁 145–146 是習題 6.1–6.18，第 7 節「方向導數與均值定理」從書頁 146 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e38_differential.py`（`AdvCalcE38ZH` / `AdvCalcE38EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[38]` / `FORMULAS_ADVCALC[38]`）
- 配音：`manim_lessons/samples/audio_e38/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.12 分（187 秒）／英文 3.02 分（181 秒）

## 餘項一律算出來擺在畫面上

這一集的每一條規則都是「某個東西是線性部分，剩下的落在小 o 裡」，所以場景檔一律把餘項的商
算出來放進表格，並且斷言它真的往下掉：

- **beat 1**：`x²` 在 1 附近，餘項的商斷言**正好等於** t（不是「趨近」，是每個取樣點都相等）。
- **beat 2**：`x² + xy` 在 (1, 1)，骨架是兩個偏導數 3 與 1。除了斷言餘項的商往下掉，
  還用差商反查一次那兩個偏導數，確認畫面上寫的 3 與 1 就是這個函數真的有的。
- **beat 4**：兩個候選的線性部分，斷言它們的差的商是**常數**——不動，所以不是小 o，
  所以線性部分唯一。這一拍完全靠 E37 最後那一條。
- **beat 8**：乘積規則在 `x² · x³` 上，`F(α)dG + dF·G(α) = 1·3 + 2·1 = 5`，
  斷言等於 5，並列出餘項的商。
- **beat 9 是最實在的一拍**：兩個平面到平面的映射，把兩個雅可比矩陣乘起來得到
  `[[4, 3], [1, 0]]`（斷言它就是這個矩陣），再拿它去減合成的實際變化量，斷言餘項的商
  單調下降到 0.0015。也就是說，鏈鎖規則在畫面上這個例子是**驗過的**，不是宣告的。

例子都是自己挑的，不是書上的習題（習題 6.10 有一個類似的映射，刻意避開）。

`bounds.py` 第一輪抓到三處：beat 0 兩個面板的曲線都衝出上緣（拋物線畫太遠）、
beat 2 的曲面爬到 y = 1.54、beat 9 的三個空間標籤頂到 1.32。`collide.py` 接著抓到
那三個標籤壓在座標軸上。probe 幀又抓到兩件工具看不到的事：beat 2 的切平面畫成 5×5 網格時
把曲面吃掉了（改成平面稀疏、曲面密集，並加上兩處紅色虛線標出差距），以及 beat 8 的曲線
被上限截斷成一個平台加懸崖（改成只畫 t 小於 0.12 的那一段）。

---

## Beat 0 — 把切點搬到原點 / move the point of tangency to the origin
*配音長度：中文 21.4s ／ 英文 16.9s*

**畫面公式**

```
把切點搬到原點   |   move the point of tangency to the origin
l ( t )  =  f ′ ( a ) · t              y − f ( a )  =  f ′ ( a ) ( x − a )
```

**旁白（繁中）**

> 先回到最普通的一元微積分。函數在一點的導數是切線的斜率。把切點平移到原點之後，切線就變成一條過原點的直線，也就是一個線性泛函的圖形：t 對應到導數乘上 t。這個換座標的動作是整節的關鍵。

**Narration (EN)**

> Start from ordinary one variable calculus. The derivative at a point is the slope of the tangent line. Translate the point of tangency to the origin and the tangent becomes a line through the origin, the graph of a linear functional sending t to the derivative times t.

**動畫**

左邊是原來的拋物線與切線，右邊是把切點搬到原點之後的同一張圖——切線變成過原點的直線。

## Beat 1 — 切線是最貼近變化量的直線 / the tangent hugs the change
*配音長度：中文 18.1s ／ 英文 17.1s*

**畫面公式**

```
切線是最貼近變化量的直線   |   the tangent hugs the change
Δf ₐ ( t )  =  f ( a + t ) − f ( a )              Δf ₐ − l   ∈   o
```

**旁白（繁中）**

> 平移之後，曲線變成變化量：Δf 在 t 的值，是 a 加 t 的函數值減掉 a 的函數值。切線是那條最貼近它的直線，兩者的差落在小 o 裡。畫面上那個差除以 t，確實一路掉到零。

**Narration (EN)**

> After the translation the curve becomes the change: delta f at t is the value at a plus t minus the value at a. The tangent is the line that hugs it most closely, and the gap between them lies in little oh. On screen that gap over t falls steadily to zero.

**動畫**

變化量與它的切線，兩條紅色虛線標出兩處的差。右邊是餘項的商的表：1、0.1、0.01、0.001。

## Beat 2 — 兩個變數：切平面 / two variables: a tangent plane
*配音長度：中文 18.0s ／ 英文 17.2s*

**畫面公式**

```
兩個變數：切平面   |   two variables: a tangent plane
l ( s , t )  =  s f ₁ ( a , b )  +  t f ₂ ( a , b )              ⟨ 3 , 1 ⟩
```

**旁白（繁中）**

> 兩個變數也一樣，只是切線換成切平面。線性泛函是 s 乘第一個偏導數，加上 t 乘第二個偏導數，它的骨架就是兩個偏導數排成的一列。畫面上那個例子的骨架是三與一。

**Narration (EN)**

> Two variables work the same way, with a tangent plane instead of a line. The linear functional is s times the first partial derivative plus t times the second, and its skeleton is those two partials in a row. For the example on screen the skeleton is three and one.

**動畫**

軸測投影的切平面（紫色，稀疏網格）與實際曲面（青色，密集曲線），兩處紅色虛線標出差距。

## Beat 3 — 定義：線性部分加一個小 o / the definition: a linear part plus little oh
*配音長度：中文 15.5s ／ 英文 16.6s*

**畫面公式**

```
定義：線性部分加一個小 o   |   the definition: a linear part plus little oh
ΔF ₐ ( ξ )    =    T ( ξ )   +   o ( ξ )              T ∈ Hom ( V , W )
```

**旁白（繁中）**

> 定義就這樣寫出來：F 在 α 可微，如果存在一個有界線性映射 T，使得變化量等於 T 加上一個小 o。就這一句，沒有極限、沒有分母，也不必假設有限維。

**Narration (EN)**

> The definition now writes itself. F is differentiable at alpha if there is a bounded linear map T with the change equal to T plus a little oh. That is the whole sentence: no limit, no denominator, and no assumption of finite dimension.

**動畫**

三個方框排成一列：變化量 = 線性部分 + 小 o，中間是等號與加號。

## Beat 4 — 為什麼只有一種寫法 / why there is only one such T
*配音長度：中文 14.8s ／ 英文 15.1s*

**畫面公式**

```
為什麼只有一種寫法   |   why there is only one such T
T ₁ − T ₂    ∈    Hom  ∩  o    =    { 0 }
```

**旁白（繁中）**

> 這個 T 是唯一的，理由就是上一集最後那一條：兩個候選的差同時屬於 Hom 與小 o，而這兩個只交於零映射。所以「線性部分」不可能有第二種寫法。

**Narration (EN)**

> That T is unique, and the reason is the last result of the previous episode: the difference of two candidates lies in Hom and in little oh at once, and those meet only at the zero map. So the linear part admits no second version.

**動畫**

紅色水平虛線是兩個候選之差的比值（永遠不動），青色是一個真的小 o 的比值（收到零）。

## Beat 5 — 微分是一個映射，不是一個數 / a differential is a map, not a number
*配音長度：中文 17.9s ／ 英文 16.6s*

**畫面公式**

```
微分是一個映射，不是一個數   |   a differential is a map, not a number
ΔF ₐ     =     dF ₐ     +     o
```

**旁白（繁中）**

> 這個唯一的 T 就叫 F 在 α 的微分。它是一個映射，不是一個數。定義域是無窮維時，習慣叫它第一變分。變分法的人比微分學的人更早看到它，只是沒發現是同一件事。

**Narration (EN)**

> This unique T is called the differential of F at alpha. It is a map, not a number. When the domain is infinite dimensional it is traditionally called the first variation; the calculus of variations saw it first without realising it was the same object.

**動畫**

左右兩個面板，同一個向量在 V 裡與它的像在 W 裡，中間一支箭頭：微分吃向量、吐向量。

## Beat 6 — 定理 6.1：三條容易的 / Theorem 6.1: three easy parts
*配音長度：中文 17.0s ／ 英文 18.1s*

**畫面公式**

```
定理 6.1：三條容易的   |   Theorem 6.1: three easy parts
F ≡ c   ⇒   dF ₐ = 0              F ∈ Hom   ⇒   dF ₐ = F
```

**旁白（繁中）**

> 定理 6.1 先收三條容易的。可微一定推得出變化量落在大 O 裡；常數函數的微分是零映射；而有界線性映射處處可微，微分就是它自己，因為它的變化量本來就等於它。

**Narration (EN)**

> Theorem six point one clears three easy parts. Differentiable forces the change into big oh; a constant function has the zero map as differential; and a bounded linear map is differentiable everywhere with itself as differential, since its change already equals it.

**動畫**

三個方框，各寫一條容易的結論：可微推得出大 O、常數的微分是零、線性映射的微分是自己。

## Beat 7 — 加法規則 / the sum rule
*配音長度：中文 15.1s ／ 英文 16.3s*

**畫面公式**

```
加法規則   |   the sum rule
d ( F + G ) ₐ    =    dF ₐ   +   dG ₐ
```

**旁白（繁中）**

> 加法規則：和的微分就是兩個微分的和。證明只是把兩個「線性部分加小 o」相加，再用上一集那條「小 o 對加法封閉」。整個推導不到兩行。

**Narration (EN)**

> The sum rule: the differential of a sum is the sum of the differentials. The proof just adds two copies of linear part plus little oh and leans on little oh being closed under addition, which the previous episode established. It takes barely two lines.

**動畫**

三行推導：變化量相加、各自展開成「線性加小 o」、再併回去。

## Beat 8 — 乘積規則，第二項是並矢 / the product rule, with a dyad
*配音長度：中文 16.0s ／ 英文 14.9s*

**畫面公式**

```
乘積規則，第二項是並矢   |   the product rule, with a dyad
d ( F G ) ₐ    =    F ( α ) dG ₐ   +   dF ₐ G ( α )
```

**旁白（繁中）**

> 乘積規則：一個實值函數乘上一個向量值函數，微分是「函數值乘微分」加上「微分乘函數值」。第二項是一個並矢，因為那是一個線性泛函配上一個固定的向量。

**Narration (EN)**

> The product rule: a real valued function times a vector valued one has differential the value times the differential plus the differential times the value. That second term is a dyad, being a linear functional paired with a fixed vector.

**動畫**

餘項的商的曲線（只畫 t 小於 0.12 的那一段），右邊是乘積規則的算式與四個取樣點。

## Beat 9 — 定理 6.2：鏈鎖規則 / Theorem 6.2: the chain rule
*配音長度：中文 15.9s ／ 英文 15.7s*

**畫面公式**

```
定理 6.2：鏈鎖規則   |   Theorem 6.2: the chain rule
d ( G ∘ F ) ₐ   =   dG ᵦ ∘ dF ₐ              β = F ( α )
```

**旁白（繁中）**

> 定理 6.2 是鏈鎖規則：合成的微分等於兩個微分的合成。畫面上是兩個平面到平面的映射，兩個雅可比矩陣乘出來的那個，跟直接算合成的變化量完全一致。

**Narration (EN)**

> Theorem six point two is the chain rule: the differential of a composite is the composite of the differentials. On screen, two maps of the plane to itself, where the product of the two Jacobians agrees exactly with the change computed directly.

**動畫**

V、W、X 三個空間排成一列，底下是三個矩陣：兩個雅可比與它們的乘積。右邊是餘項的商的表。

## Beat 10 — 證明就是把上一集用一遍 / the proof is last episode, applied
*配音長度：中文 17.4s ／ 英文 16.8s*

**畫面公式**

```
證明就是把上一集用一遍   |   the proof is last episode, applied
o ∘ O   ⊂   o              O ∘ o   ⊂   o
```

**旁白（繁中）**

> 證明就是把上一集那條定理逐條用一遍：小 o 接大 O 是小 o、大 O 接小 o 也是小 o，最後只剩下兩個線性部分的合成。第 3 章的核心到這裡講完，下一集講方向導數與均值定理。

**Narration (EN)**

> The proof applies the previous episode's theorem line by line: little oh after big oh is little oh, big oh after little oh is little oh, and what survives is the composite of the two linear parts. Next time, directional derivatives and the mean value theorem.

**動畫**

三行推導：把合成拆開、用 E37 的合成規則吃掉兩個小 o、剩下兩個線性部分的合成。

---

## 定義裡沒有「極限」

這一節最值得注意的是定義的形狀：`ΔFα = T + o`。沒有極限符號、沒有分母、也沒有假設維數有限。
一元微積分的導數是它在維數等於一時的樣子，而無窮維時它叫第一變分。整章前面四節
（範數、連續、算子範數、等價範數、無窮小）鋪的全部工具，就是為了讓這一句話寫得出來。

## 鏈鎖規則的證明就是 E37 的定理逐條用一遍

`小 o 接大 O 是小 o`、`大 O 接小 o 也是小 o`——這兩條剛好把展開之後多出來的項全部吃掉，
剩下的只有兩個線性部分的合成。收尾那一拍就是這件事，所以 E37 與 E38 是同一段論證的兩半。
