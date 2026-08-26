# advcalc E36 — 第 3 章：等價範數與乘積範數

Chapter 3: Equivalent Norms and Product Norms

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 4 節（書頁 132–134）。書頁 135–136 是習題 4.1–4.18，第 5 節「無窮小」從書頁 136 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e36_equivalent_norms.py`（`AdvCalcE36ZH` / `AdvCalcE36EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[36]` / `FORMULAS_ADVCALC[36]`）
- 配音：`manim_lessons/samples/audio_e36/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.22 分（193 秒）／英文 3.04 分（182 秒）

## 常數一律取最緊的，而且是掃出來的

這一節整節都在講「兩個範數差不了多少」，所以每個常數都必須是最緊的那一個，
不然畫面上的球就會鬆一圈，而旁白說的又是「這是最緊的」。場景檔的做法是掃過整個圓，
對每一對範數求 `f / g` 的上確界：

- 平面上量出來是 `‖x‖₁ ≤ √2 ‖x‖₂`、`‖x‖₂ ≤ √2 ‖x‖∞`、`‖x‖₁ ≤ 2 ‖x‖∞`，
  而反方向三個常數全是 1（斷言檢查過）。畫面上的三個數字就是掃描的結果，不是查表抄的。
- **beat 4 的反例是數值積分算的**：`t` 的 n 次方在 0 到 1 上的一範數，算出來跟 `1/(n+1)`
  對得起來（斷言誤差小於 1e-4）。比值 2、5、17 一路爬，這就是「無窮維不等價」的具體樣子。
- **beat 6 斷言定理 4.2 的證明在這個矩陣上剛好是緊的**：`max |tᵢⱼ| = 3`，而
  `sup ‖Tx‖∞ / ‖x‖₁` 掃出來也是 3。所以那句「這裡是 3，而且剛好是最緊的」不是猜的。
- **beat 10 斷言加法的算子範數正好是 1**（在 240 × 240 組方向上掃過），
  因為那句話跟三角不等式是同一件事。

`bounds.py` 第一輪抓到 beat 8 的左面板擠出畫面左緣（−6.35），而且那一版的兩個面板
其實是重疊的，投影箭頭直接穿過中間那個面板。改成 V 與 W 上下疊在左邊、V × W 放右邊。
`collide.py` 抓到三拍的符號列壓在面板座標軸上（beats 1、2、10），以及 beat 4 最下面
那一列數字撞到收尾字幕。

---

## Beat 0 — 範數同構：兩邊都有界 / norm isomorphic: bounded both ways
*配音長度：中文 19.9s ／ 英文 16.5s*

**畫面公式**

```
範數同構：兩邊都有界   |   norm isomorphic: bounded both ways
T ∈ Hom ( V , W )   ,   T ⁻¹ ∈ Hom ( W , V )
```

**旁白（繁中）**

> 兩個賦範空間如果有一個線性雙射，而且它跟它的反映射都有界，就說這兩個空間範數同構。跟以前一樣，同構的空間就當成同一個。同一個空間上的兩個範數要怎麼算「一樣」，就從這裡引出來。

**Narration (EN)**

> Two normed spaces are norm isomorphic if there is a linear bijection between them with both the map and its inverse bounded. As always, isomorphic spaces are treated as the same. What it should mean for two norms on one space to be the same grows out of this.

**動畫**

左右兩個面板各一顆單位球（形狀不同，因為範數不同），上面一支橘色箭頭是 T、下面一支紫色箭頭是反映射，兩個方向都要有界。

## Beat 1 — 兩個範數等價的定義 / when two norms are equivalent
*配音長度：中文 15.2s ／ 英文 13.9s*

**畫面公式**

```
兩個範數等價的定義   |   when two norms are equivalent
p   ≤   a q            q   ≤   b p
```

**旁白（繁中）**

> 定義是這樣：兩個範數 p 與 q 等價，如果找得到常數 a 與 b，使得 p 不超過 a 倍的 q，而且 q 也不超過 b 倍的 p。兩個方向都要成立，只有一邊不算數。

**Narration (EN)**

> Here is the definition. Two norms p and q are equivalent if there are constants a and b with p at most a times q, and q at most b times p. Both directions are required; one of them alone is not enough.

**動畫**

同心的兩顆球：紅色是一個範數的、藍色是另一個的。下方是那兩條不等式。

## Beat 2 — 互相夾住，就是恆等映射有界 / each brackets the other
*配音長度：中文 16.6s ／ 英文 15.3s*

**畫面公式**

```
互相夾住，就是恆等映射有界   |   each brackets the other
( 1 / b ) q    ≤    p    ≤    a q
```

**旁白（繁中）**

> 把兩式合起來，就是 q 除以 b 不超過 p、p 不超過 a 倍的 q：任何一個都被另一個的兩個倍數夾住。換句話說，恆等映射從一個範數看到另一個範數，兩個方向都是有界的。

**Narration (EN)**

> Put the two together and q over b is at most p, which is at most a times q: either one is bracketed by two multiples of the other. Equivalently, the identity map read from one norm to the other is bounded in both directions.

**動畫**

紅色那顆球夾在兩顆灰色的球中間——這就是「被另一個的兩個倍數夾住」。

## Beat 3 — 幾何上：單位球互相包 / geometrically, the balls nest
*配音長度：中文 19.7s ／ 英文 15.9s*

**畫面公式**

```
幾何上：單位球互相包   |   geometrically, the balls nest
‖ x ‖ ∞  ≤  ‖ x ‖ ₂  ≤  ‖ x ‖ ₁  ≤  2 ‖ x ‖ ∞            ‖ x ‖ ₁  ≤  √2 ‖ x ‖ ₂
```

**旁白（繁中）**

> 幾何上就是單位球互相包住。平面上一範數的球是斜正方形、二範數是圓、無窮範數是正方形。畫面上量出來的最緊常數是：一範數不超過二範數的根號二倍，也不超過無窮範數的兩倍。

**Narration (EN)**

> Geometrically the unit balls contain one another. On the plane the one norm ball is a tilted square, the two norm ball is round, and the uniform one is an upright square. The tightest constants measured on screen are root two, and a factor of two.

**動畫**

平面上三顆單位球疊在一起：斜正方形、圓、正方形。右邊三行是掃出來的最緊常數。

## Beat 4 — 無窮維會壞掉 / infinite dimensions break it
*配音長度：中文 16.9s ／ 英文 18.0s*

**畫面公式**

```
無窮維會壞掉   |   infinite dimensions break it
f ₙ ( t )  =  t ⁿ           ‖ f ₙ ‖ ∞ = 1  ,   ‖ f ₙ ‖ ₁ = 1 / ( n + 1 )
```

**旁白（繁中）**

> 但無窮維會壞掉。取閉區間上的連續函數，t 的 n 次方的一致範數永遠是一，一範數卻是 n 加一分之一。比值就是 n 加一，要多大有多大，所以這兩個範數不等價。

**Narration (EN)**

> Infinite dimensions break this. Take continuous functions on an interval: t to the n has uniform norm one forever, while its one norm is one over n plus one. The ratio is n plus one, which grows without ceiling, so those two norms are not equivalent.

**動畫**

t 的一次、四次、十六次方畫在同一張圖上，全都在右端碰到高度為 1 的虛線（一致範數）。右邊列出三個一範數與對應的比值 2.0、5.0、17.0。

## Beat 5 — 定理 4.1：有限維上全部等價 / Theorem 4.1: in finite dimensions, all of them
*配音長度：中文 15.4s ／ 英文 15.4s*

**畫面公式**

```
定理 4.1：有限維上全部等價   |   Theorem 4.1: in finite dimensions, all of them
dim V  <  ∞            ⇒            p  ∼  q
```

**旁白（繁中）**

> 定理 4.1 說：有限維向量空間上所有範數都等價。這條要到第 4 章才證得動，但它是後面很多地方可以安心換範數的根據，也是這一節真正想講的結論。

**Narration (EN)**

> Theorem four point one says that on a finite dimensional vector space all norms are equivalent. It cannot be proved until chapter four, but it is what lets later chapters swap norms without a second thought, and it is the real point of the section.

**動畫**

三顆單位球，外加兩顆同心的灰色圓球把它們夾在中間——「任何單位球都夾得進兩顆圓球之間」。

## Beat 6 — 定理 4.2：有限維之間一定有界 / Theorem 4.2: always bounded
*配音長度：中文 16.9s ／ 英文 18.9s*

**畫面公式**

```
定理 4.2：有限維之間一定有界   |   Theorem 4.2: always bounded
‖ T x ‖ ∞   ≤   ( max | t ᵢ ⱼ | ) · ‖ x ‖ ₁            b  =  3
```

**旁白（繁中）**

> 定理 4.2 是它的直接後果：有限維之間的線性映射一定有界。挑一組座標把映射寫成矩陣，像的每個分量都是一列係數乘上座標，取矩陣元絕對值的最大值當常數就成了。

**Narration (EN)**

> Theorem four point two follows at once: a linear map between finite dimensional spaces is always bounded. Pick coordinates, write it as a matrix, and each component of the image is a row of coefficients against the coordinates; the largest entry in size serves as the constant.

**動畫**

藍色是一範數的球、紅色是它在矩陣底下的像、紫色是半徑 3 的無窮範數球，像整個裝得進去。

## Beat 7 — 定理 4.3：Hom 不受影響 / Theorem 4.3: Hom does not notice
*配音長度：中文 16.2s ／ 英文 15.7s*

**畫面公式**

```
定理 4.3：Hom 不受影響   |   Theorem 4.3: Hom does not notice
p ∼ p′  ,   q ∼ q′            ⇒            ‖ T ‖  ∼  ‖ T ‖ ′
```

**旁白（繁中）**

> 定理 4.3 說換成等價範數，Hom 這個集合完全不變，而且兩種範數在 Hom 上誘導出來的算子範數也彼此等價。所以在有限維裡，「用哪個範數」從來不會影響結論。

**Narration (EN)**

> Theorem four point three says that replacing a norm by an equivalent one leaves the set Hom untouched, and the two operator norms it induces on Hom are themselves equivalent. In finite dimensions, which norm you picked never changes the conclusion.

**動畫**

兩個面板畫著同一組球的兩種範數版本，中間一支箭頭；下方一行寫著 Hom(V, W) = Hom(V, W)。

## Beat 8 — 乘積空間該配什麼範數 / what norm belongs on a product
*配音長度：中文 17.5s ／ 英文 16.4s*

**畫面公式**

```
乘積空間該配什麼範數   |   what norm belongs on a product
‖ ⟨ α , ξ ⟩ ‖    ∼    ‖ α ‖ + ‖ ξ ‖
```

**旁白（繁中）**

> 接著問乘積空間該配什麼範數。要求很自然：兩個投影與兩個嵌入都要連續。光是這個要求，就把乘積範數決定到等價為止，它一定跟「兩邊的範數相加」那一個等價。

**Narration (EN)**

> Then, what norm belongs on a product space? The requirement is natural: both projections and both injections should be continuous. That alone pins the product norm down to within equivalence, and it must be equivalent to adding the two norms.

**動畫**

左邊上下疊著 V 與 W 兩顆球，右邊是 V × W 的球，橘色箭頭是嵌入、灰色箭頭是投影。

## Beat 9 — 定理 4.4：三種乘積範數等價 / Theorem 4.4: three product norms, all equivalent
*配音長度：中文 18.2s ／ 英文 16.9s*

**畫面公式**

```
定理 4.4：三種乘積範數等價   |   Theorem 4.4: three product norms, all equivalent
‖ · ‖ ₁   ∼   ‖ · ‖ ₂   ∼   ‖ · ‖ ∞            ( V × W )
```

**旁白（繁中）**

> 定理 4.4 說常用的三種乘積範數，相加的、歐氏的、取最大的，彼此等價，而且都符合上面那個要求。平面上這三個就是剛才畫過的一、二、無窮範數，所以是同一張圖。

**Narration (EN)**

> Theorem four point four says the three usual product norms, the sum, the Euclidean and the maximum, are equivalent to one another and each meets that requirement. On the plane those three are the one, two and uniform norms drawn earlier, so it is the same picture.

**動畫**

三顆單位球（跟 beat 3 同一張圖），右邊列出三種乘積範數的公式。

## Beat 10 — 加法有界，直和看投影 / addition is bounded; direct sums watch the projections
*配音長度：中文 20.5s ／ 英文 19.6s*

**畫面公式**

```
加法有界，直和看投影   |   addition is bounded; direct sums watch the projections
‖ α + β ‖  ≤  ‖ α ‖ + ‖ β ‖            ‖ + ‖  =  1
```

**旁白（繁中）**

> 最後兩件事。引理 4.1：加法是從 V 乘 V 到 V 的有界線性映射，用相加的乘積範數時，界正好是一，因為那就是三角不等式本身。定理 4.5：一個空間是範數直和，當且僅當所有投影都有界。

**Narration (EN)**

> Two last things. Lemma four point one: addition is a bounded linear map from V times V to V, with bound exactly one under the sum norm, since that is the triangle inequality itself. Theorem four point five: a space is a norm direct sum exactly when its projections are bounded.

**動畫**

一個向量三角形：藍色加紫色接成紅色，紅色不會比兩段的和長。下方寫著加法的算子範數是 1。

---

## 為什麼三種乘積範數的圖跟 beat 3 是同一張

在平面上，把 ℝ × ℝ 的三種乘積範數（相加、歐氏、取最大）寫出來，就正好是 `‖·‖₁`、
`‖·‖₂`、`‖·‖∞`。所以 beat 9 直接重用 beat 3 那張圖，並在旁白裡點명這件事——
這不是偷懶，是這一節的內容本身：乘積範數不是新東西。

## 定理 4.1 沒有證

書上明說這條要到第 4 章（用緊緻性）才證得動，這裡照樣不證，只把它的**用途**講清楚：
後面很多章可以隨手換範數，靠的就是它。畫面上那兩顆灰色的圓球是它的圖像化說法——
「任何單位球都夾得進兩顆同心的圓球之間」。
