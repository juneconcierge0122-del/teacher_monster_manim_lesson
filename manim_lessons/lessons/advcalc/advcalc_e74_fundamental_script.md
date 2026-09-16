# advcalc E74 — 第 6 章：基本定理

Chapter 6: The Fundamental Theorem

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 1 節「基本定理」的**前半**（書頁 266–269，收在定理 1.2），也是第 6 章的第一集。後半（整體解、極大解、n 階方程，269–272）留給 E75。

**第 6 章的細目表是這一輪自己核出來的**，原本 `OUTLINE.md` 只有章層級的一列。核出來的結果：§1 內容 266–272、習題 1.1–1.13 在 272–273；**§2「對參數的可微相依」只有 274–275 兩頁，而且整節沒有習題**（這是全書第四次，前三次是第 2 章 *§7、第 4 章 *§12、第 5 章 §5）；§3 276–280；§4 281–287；§5 288–292；§6 294–299；§7 301–303，第 6 章收在書頁 304。**章層級那一列寫 266–305 是把第 7 章的第一頁也算了進去。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e74_fundamental.py`（`AdvCalcE74ZH` / `AdvCalcE74EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[74]` / `FORMULAS_ADVCALC[74]`）
- 配音：`manim_lessons/samples/audio_e74/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 233.0 秒（3:53）／英文 211.9 秒（3:32），配音 232.2 ／ 211.1 秒
- YouTube（私人）：中文 https://youtu.be/Y1CUxFIijIQ ／英文 https://youtu.be/GhzTYxFC9Q4

## 這一節在做什麼

**問題是初始值問題。** W 是 Banach 空間、A ⊂ W 開、I ⊂ ℝ 開、F : I × A → W 連續，
問 d α / d t = F ( t , α ) 有沒有解通過 ⟨ t ₀ , α ₀ ⟩，唯不唯一。

**答案靠的是 Lipschitz，不是連續。** 局部一致 Lipschitz：每一點附近有一個 b，使
‖ F ( t , ξ ) − F ( t , η ) ‖ ≤ b ‖ ξ − η ‖，而且同一個 b 對那一段的每個 t 都成立。
書上指出 dF ² 連續加均值定理就給得出它。

**這個假設不是裝飾。** x ′ = 2 √ | x | 到處連續，可是過原點的解有無限多條：

```
x ( t )   =   0        ( t ≤ a )                x ( t )   =   ( t − a ) ²       ( t > a )
```

每個 a ≥ 0 都給一條，而 Lipschitz 商 2 √ ξ / ξ 在原點附近衝上無窮大。

**證明的關鍵一步是換舞台。** 從 t ₀ 積到 t：

```
f ′ = F ( t , f )  ,  f ( t ₀ ) = α ₀        ⟺        f ( t )  =  α ₀ + ∫ F ( s , f ( s ) ) d s
```

右邊只要求 f **連續**，而有界連續函數的空間是**完備**的——第 4 章的不動點定理才有地方站。
於是 K : f ↦ α ₀ + ∫ F ( s , f ( s ) ) d s，**解就正好是 K 的不動點**。

**兩個估計把 K 變成球的壓縮自映射：**

```
‖ K ( ᾱ ₀ ) − ᾱ ₀ ‖ ∞    ≤    δ m                      ( 球心移動 )
‖ K f ₁ − K f ₂ ‖ ∞      ≤    δ c ‖ f ₁ − f ₂ ‖ ∞         ( 壓縮 )
```

要 δ c < 1 又要 δ m < ( 1 − δ c ) r，兩者合起來正好是 **δ < r / ( m + c r )**。

**引理 1.1** 說過同一點的兩個解在定義域交集上必相等（取相異集合的下確界，它是開集，
所以下確界本身兩者相等，再用一次定理 1.1 得到矛盾）。有了它，**定理 1.2** 就能把
「解必須落在小鄰域 U 裡」這個人為限制拿掉。

## 這一集用的例子

**整集只用一個例子**，每個畫面上的數字都在場景檔裡算出來並 assert：

```
d x / d t   =   1  +  x ²          x ( 0 )  =  0                f ( t )  =  tan t
```

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| F 的界 m | 1 + x ² 的絕對值在半徑一的球上取最大 | 2.0000 |
| Lipschitz 常數 c | 割線斜率是 ξ + η，取上確界 | 2.0000 |
| δ 的上限 | r / ( m + c r ) | 0.2500 |
| 壓縮條件單獨給的上限 | 1 / c | 0.5000 |
| 真正的解活多遠 | tan t 的極點 | 1.5708 |
| 保守多少倍 | ( π / 2 ) ÷ 0.25 | 6.283185  =  2 π |
| 解離開 U 的時刻 | tan t = 1 | 0.7854 |
| Picard 迭代收不收斂 | ‖ f ₙ − tan ‖ ∞ ，n = 1…7 | 0.5574 → 0.0001367 |
| 積分式對不對 | ∫ F ( s , f ( s ) ) d s 對 tan ( 0.7 ) | 0.842288380 ／ 0.842288380 |

**那個 2 π 是這一集的重點之一。** 定理保證的區間只有 0.25，真正的解活到 π / 2，
差了整整 2 π 倍——一個要對**所有** F 都成立的估計，本來就得這麼保守。

## 這一輪抓到的錯

- **表格列裡混了中文。** 第 3、4、9、10 拍的 `_table` 寫了「開」「連續」「定理 1.1 ⇒ …」，
  而 `_table` 走的是 `_sym`，兩個語言渲染成同一個樣子。langscan 一次抓到 9 處，
  全部改成純符號，說明話搬到 `_cap` 與 `_foot`。這是這個錯第六次出現。
- **圖例貼到公式列。** 四張圖的圖例 y ₀ 放在 1.20–1.24，實測頂端到 1.30–1.32，
  bounds 抓到 26 處。圖例統一降到 1.14。
- **三張表跑進說明列。** 第 1、2、5 拍的表格列數比預想多一列（表頭與結語各一），
  最後一列壓到 −0.74 ~ −0.94，撞上 −0.90 的 `_cap`。y ₀ 與 dy 一起收緊。
- **第 0 拍的點標籤壓在方向場上。** ( t ₀ , α ₀ ) 原本放在原點右上 0.30 處，
  那一整塊都是方向場的短線。移到方向場上緣之外（oy + 0.96）。
- **第 8 拍的門檻虛線穿過圖例。** 兩條標 0.25 與 0.50 的虛線畫到 y = 0.74，
  正好穿過圖例第三列的字。虛線縮到 1.20（曲線在那裡早就交會了，不需要畫那麼高）。
- **第 8 拍的兩條線其實是同一條。** δ c 與 δ m 一條畫紫、一條畫青，可是這個例子的
  m 與 c 剛好都是 2，兩條線完全重合，圖例列了三項而畫面上只有兩條線。
  改成只畫一條、標成 δ c = δ m，並在註腳說明為什麼；場景檔加一條
  `assert abs(C_SUP - M_BD) < 1e-12` 把「它們相等」這件事釘住，
  哪天換了例子而忘了改圖，assert 會先失敗。這是 E72「兩個矩陣其實是同一個」的同類。
- **第 7 拍看不出壓縮。** 兩個像畫在寬度只有 0.28 的範圍裡，兩條線幾乎疊成一筆，
  而「距離被壓小」正是這一拍唯一要說的事。重畫成左右兩塊**共用同一個縱向尺度**
  （這是關鍵——兩邊各自縮放就看不出比例），並在兩邊各畫一支雙箭頭標出間距：
  左邊 0.5，右邊 0.11，比例 0.22，剛好在 δ c = 0.4 底下。
- **第 0 拍的方向場糊成一片斜線。** 短線半長 0.28、格點間距 0.486，線比格子長，
  相鄰的線互相接續，整塊讀起來像網底而不是方向場。格點改成 5 × 5、半長改成 0.15，
  並跳過原點那一根（它被 ⟨ t ₀ , α ₀ ⟩ 的點蓋住）。
- **第 3 拍的 J 小到看不見。** L 取 ±1.15、J 取 ±0.2，比例 1 比 6，J 的兩條線緊貼縱軸，
  看起來像軸的一部分。**L 是我們自己選的**，所以改取 ±0.6，J 就成了 L 的三分之一，
  再把 L × U 畫成一個明確的方框、J 畫成方框裡的一條窄帶。
- **第 9 拍的分岔看不出來。** 假的那一支寫成 tan t 加 0.9 ( t − x ) ²，
  在 t = 0.95 只離真解 0.089，兩條線黏在一起，而「分岔」是這一拍要否證的東西。
  係數改成 3.0（殘差同時從 +0.3310 變成 +1.0787，assert 門檻一起提高），
  打叉的位置也從分岔點移到那一支上面——畫在分岔點會讓人以為是那個點有問題。
- **第 10 拍兩段同色。** J → U 那一段用 ACCENT_C（紫），與 ACCENT_A（橘）在 480p 下
  幾乎同色，整條曲線讀起來是一條；註腳還寫「青線變橘線」，顏色根本對不上。
  改用 ACCENT_B（青），圖例同時改掉。
- **第 4 拍加的 f ( t ) 標籤壓在網底上。** 為了讓「面積 = f ( t ) 的高度」有著落，
  加了一個點、一條虛線與一個標籤，結果標籤正好落在積分的網底裡，collide 抓到 20 處。
  標籤拿掉，點與虛線留著——右表那兩個 0.842288380 已經把話說完了。

## 十一拍

### 第 1 拍 — 第 6 章開場：要解的是什麼 / chapter 6 opens: what is to be solved

公式列：

```
d α / d t   =   F ( t , α )              f ′ ( t )   =   F ( t , f ( t ) )
```

中文旁白：第 6 章講微分方程。設 W 是 Banach 空間，A 是其中的開集，I 是開區間，F 從 I 乘 A 連續映到 W。要解的方程是 α 對 t 的導數等於 F t α；解是定義在子區間上的函數 f，它在每一點的導數都等於 F 帶入 t 與 f t 的值。

English: Chapter 6 opens on differential equations. Let W be a Banach space, A an open subset of it, I an open interval, and F a continuous map from I times A into W. A solution is a function f on a subinterval whose derivative at each point equals F of t and f of t.

### 第 2 拍 — 真正的假設是 Lipschitz / the hypothesis that does the work

公式列：

```
‖ F ( t , ξ ) − F ( t , η ) ‖    ≤    b ‖ ξ − η ‖
```

中文旁白：撐住整個定理的假設不是連續，而是 Lipschitz。局部一致 Lipschitz 是說：每一點附近都找得到一個常數 b，讓 F 在 ξ 與在 η 的值相差的長度，不超過 b 乘上 ξ 減 η 的長度，而且同一個 b 對附近每個 t 都管用。

English: The hypothesis that carries the theorem is not continuity but a Lipschitz condition. Locally uniformly Lipschitz means that near each point one constant b makes the length of F at xi minus F at eta at most b times the length of xi minus eta, with the same b for every nearby t.

### 第 3 拍 — 少了它，唯一性就沒了 / without it, uniqueness is gone

公式列：

```
x ′  =  2 √ | x |          x ≡ 0  ,  x = ( t − a ) ²          2 / ( √ ξ + √ η )  →  ∞
```

中文旁白：少了它，唯一性立刻垮掉。看 x 的導數等於二倍根號 x 的絕對值：過原點的解有無限多條，先沿著零軸走任意久，再翹起來變成拋物線。它在原點附近的 Lipschitz 商是二除以兩個根號的和，會衝上無窮大。

English: Without it uniqueness collapses at once. Take the derivative of x equal to twice the square root of the absolute value of x. Infinitely many solutions pass through the origin: run along zero as long as you like, then lift off as a parabola. The quotient blows up there.

### 第 4 拍 — 定理 1.1 / theorem 1.1

公式列：

```
∃ !  f : J → U               f ′ = F ( t , f )  ,   f ( t ₀ ) = α ₀
```

中文旁白：定理 1.1：A 是 Banach 空間 W 的開集，I 是開區間，F 從 I 乘 A 連續映到 W，並且對第二個變數局部一致 Lipschitz。那麼過 I 乘 A 裡的每一點，在 α 零的某個鄰域與夠小的區間 J 上，恰好存在一條解。

English: Theorem 1.1. Let A be open in a Banach space W, let I be an open interval, and let F from I times A to W be continuous and locally uniformly Lipschitz in its second variable. Then through each point there is exactly one solution, on a small enough interval J.

### 第 5 拍 — 換舞台：積分方程 / changing the stage

公式列：

```
f ( t )   =   α ₀   +   ∫ F ( s , f ( s ) ) d s          ( s : t ₀ → t )
```

中文旁白：證明的第一步是換舞台。從 t 零積到 t，f 是解就等價於 f t 等於 α 零加上 F 在 s 與 f s 的積分；反過來由微積分基本定理也成立。好處是積分式只要求 f 連續，而連續函數的空間是完備的。

English: The proof starts by changing the stage. Integrating from t zero to t, being a solution is the same as satisfying f of t equals alpha zero plus the integral of F at s and f of s. The integral form only asks that f be continuous, and such functions form a complete space.

### 第 6 拍 — 解 = K 的不動點 / a solution is a fixed point

公式列：

```
K :  f  ↦  α ₀ + ∫ F ( s , f ( s ) ) d s                  K f  =  f
```

中文旁白：於是定義 K，把 f 送到 α 零加上那個積分，解就正好是 K 的不動點。畫面上是 Picard 迭代：從常數零出發一次次代回去，得到 t、再得到 t 加三分之一 t 的三次方，一路逼近真正的解。剩下要證的是 K 會壓縮。

English: So define K, sending f to alpha zero plus that integral. A solution is exactly a fixed point of K. On screen is the Picard iteration: start from the constant zero, feed it back in, and watch t, then t plus a third of t cubed, close in on the true solution.

### 第 7 拍 — 估計一：球心移動多遠 / first estimate: the centre

公式列：

```
‖ K ( ᾱ ₀ ) − ᾱ ₀ ‖ ∞    ≤    δ m                 m  =  2
```

中文旁白：第一個估計：K 把球心移動多遠。設 F 在 L 乘 U 上的界是 m，J 的長度是 δ，那麼 K 作用在常數函數 α 零上，離 α 零不超過 δ 乘 m。例子裡 F 是一加 x 平方，在半徑一的球上 m 等於二。

English: First estimate: how far K moves the centre of the ball. If F is bounded by m on L times U and J has length delta, then K applied to the constant function alpha zero sits within delta times m of it. In the example F is one plus x squared, so m is two on the unit ball.

### 第 8 拍 — 估計二：K 是壓縮 / second estimate: K contracts

公式列：

```
‖ K f ₁ − K f ₂ ‖ ∞   ≤   δ c ‖ f ₁ − f ₂ ‖ ∞            δ c  =  0.4
```

中文旁白：第二個估計：K 是壓縮。餵進兩個函數，積分的差被 Lipschitz 常數 c 控制，所以 K f 一減 K f 二的上確界範數，不超過 δ 乘 c 乘原來的距離。例子裡 c 也是二，取 δ 等於零點二，壓縮常數就是零點四。

English: Second estimate: K contracts. Feed in two functions; the difference of the integrals is held down by the Lipschitz constant c, so the sup norm of K f one minus K f two is at most delta times c times the original distance. Here c is two and delta a fifth, giving two fifths.

### 第 9 拍 — 兩個條件合成 δ 的上限 / the two conditions, combined

公式列：

```
δ  <  r / ( m + c r )  =  0.25                 ( π / 2 )  /  0.25  =  2 π
```

中文旁白：兩個要求疊起來：δ 乘 c 要小於一，δ 乘 m 要小於一減壓縮常數再乘 r。合起來就是 δ 小於 r 除以 m 加 c r，例子裡上限是零點二五。而真正的解活到 π 的一半，保證的區間短了二π 倍。書上的推論說，F 的二階偏微分連續就夠。

English: The two demands stack: delta times c below one, and delta times m below one minus the contraction constant, times r. Together that is delta below r over m plus c r, here a quarter. The true solution lives out to half of pi, short of that by a factor of two pi.

### 第 10 拍 — 引理 1.1 / lemma 1.1

公式列：

```
C  =  { t > t ₀  :  g ₁ ( t ) ≠ g ₂ ( t ) }              x  =  glb C
```

中文旁白：引理 1.1：通過同一點的兩個解，在定義域的交集上一定相等。取 C 為交集裡 t 大於 t 零而兩者不相等的那些點，令 x 是它的下確界。C 是開的，所以 x 不在 C 裡，兩個解在 x 相等；再對 x 用一次定理 1.1，就得到矛盾。

English: Lemma 1.1. Two solutions through the same point agree on the intersection of their domains. Let C be the set of t above t zero where they differ, and x its greatest lower bound. C is open, so x is not in it and the two agree at x; Theorem 1.1 at x then contradicts the bound.

### 第 11 拍 — 定理 1.2，與下一集 / theorem 1.2, and what comes next

公式列：

```
∃ !  f : J → A                     f ( t ₀ )  =  α ₀
```

中文旁白：定理 1.2 把值域的限制拿掉。定理 1.1 只給出從 J 到小鄰域 U 的解，而引理 1.1 說任何兩個解都相容，所以落在 U 裡不是真的限制。結論是：過每一點，在夠小的 J 上存在唯一一條從 J 到 A 的解。下一集接整體解。

English: Theorem 1.2 drops the restriction on the range. Theorem 1.1 gives a solution only from J into the small neighbourhood U, but Lemma 1.1 says any two solutions are compatible, so landing in U is no real restriction. Through each point there is one solution from J into A.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 方向場（7 × 5 根短線，斜率 1 + x ²）加上通過原點的 tan t；解很快就離開方框，預告「只能是局部的」 |
| 2 | F ( t , · ) 的圖與一條割線，割線斜率就是 Lipschitz 商；右表列出幾組 ξ、η 與商，沒有一列超過 b = 2 |
| 3 | 過原點的四條解（a = 0、0.25、0.50、0.75）像扇子一樣散開；右表的商一路衝到 200 |
| 4 | 定理 1.1 的幾何：L 與 J 兩組垂直虛線、U 的兩條水平虛線、J 上唯一那條解 |
| 5 | 被積函數 F ( s , f ( s ) ) 的圖與它下方的面積，面積的高度正好是 f ( t )；右表兩列到小數第九位相同 |
| 6 | Picard 迭代 f ₁ 到 f ₄ 一層層壓向 tan t；虛線標出定理真正保證的 δ < 0.25，圖畫得比它遠只是為了看得見 |
| 7 | K 作用在常數零上得到 t，與 ± δ m 兩條紅虛線；右表四列的實際位移都在界底下，而且剛好差兩倍 |
| 8 | 兩個常數函數（水平線）經過 K 之後變成兩條斜率不同的直線；右表最後一列的商逼到 0.3960，說明 δ c = 0.4 不是隨手放寬的 |
| 9 | δ c、δ m、( 1 − δ c ) r 三條線與兩個門檻 0.25、0.50；藍線鑽到紅線底下的那一段才是可用的 δ |
| 10 | 左右兩張圖：左邊是引理 1.1 禁止的分岔（打叉，因為那條分岔根本不滿足方程，殘差 +0.3310），右邊是唯一的那條 |
| 11 | U 的上緣與 tan t：青色那一段是定理 1.1 保證的 f : J → U，過了 π / 4 變成橘色，那正是定理 1.2 拿掉的限制 |
