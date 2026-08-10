# advcalc E21 — 第 2 章：對偶空間

Chapter 2: The Dual Space

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 3 節（書頁 81–83）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e21_dual_space.py`（`AdvCalcE21ZH` / `AdvCalcE21EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[21]` / `FORMULAS_ADVCALC[21]`）
- 配音：`manim_lessons/samples/audio_e21/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.38 分（203 秒）／英文 3.12 分（187 秒）

本節的後半（零化子、伴隨算子、dyad、自然性的交換圖，書頁 83–86）留給 E22。

---

## Beat 0 — 所有線性泛函所成的空間 / the space of all linear functionals
*配音長度：中文 19.6s ／ 英文 18.2s*

**畫面公式**

```
所有線性泛函所成的空間   |   the space of all linear functionals
V *  =  Hom ( V , ℝ )
```

**旁白（繁中）**

> 我們已經遇過不少特別的線性泛函，尤其是座標泛函。把 V 上所有的線性泛函收集起來，得到的空間就叫 V 的對偶空間，也叫共軛空間。這一節全部假設有限維——好處正是沒有連續性那層麻煩。

**Narration (EN)**

> We have already met a good many special linear functionals, the coordinate ones in particular. Collecting all the linear functionals on a space gives the dual, or conjugate, space. This section assumes finite dimensions throughout, and the blessing of that is one fewer complication.

**動畫**

V 畫成橢圓，三個泛函各自沿箭頭把它送到右邊的實數線。重點是「收集起來」這個動作——這些箭頭本身構成一個新的向量空間。

## Beat 1 — 座標泛函構成對偶空間的基底 / the coordinate functionals are a basis for the dual
*配音長度：中文 16.4s ／ 英文 15.7s*

**畫面公式**

```
座標泛函構成對偶空間的基底   |   the coordinate functionals are a basis for the dual
ξ = Σ₁ⁿ xᵢ βᵢ        εⱼ ( ξ )  =  xⱼ
```

**旁白（繁中）**

> 第一個想問的是對偶空間有多大，定理立刻回答了。取 V 的一組有序基底，讓第 j 個座標泛函把向量送到它的第 j 個座標，那麼這些座標泛函就構成對偶空間的一組有序基底。

**Narration (EN)**

> The first thing to ask is how big the dual space is, and a theorem settles it at once. Take an ordered basis and let the jth coordinate functional send a vector to its jth coordinate. Those functionals form an ordered basis for the dual space.

**動畫**

上排是 V 的一組有序基底，下排是對應的座標泛函，一對一往下接。定理說下排就是對偶空間的基底。

## Beat 2 — 作用在第 i 個基底向量上 / evaluate on the ith basis vector
*配音長度：中文 19.3s ／ 英文 18.0s*

**畫面公式**

```
作用在第 i 個基底向量上   |   evaluate on the ith basis vector
Σ cⱼ εⱼ = 0        εⱼ ( βᵢ ) = δ ᵢⱼ        ⇒   cᵢ = 0
```

**旁白（繁中）**

> 先看獨立性。假設它們的某個線性組合是零泛函，那就把它作用在第 i 個基底向量上。那個向量的座標除了第 i 位是一以外全是零，於是整條式子只剩第 i 個係數等於零。每個 i 都成立。

**Narration (EN)**

> Independence first. Suppose some combination of them is the zero functional, and evaluate it on the ith basis vector. That vector has coordinates zero everywhere but a one in the ith place, so the equation collapses to the ith coefficient being zero. That holds for every index.

**動畫**

把零組合作用在第 i 個基底向量上。那一列格子只有第 i 格是一、其餘是零（灰掉），所以整條式子塌成 cᵢ = 0。

## Beat 3 — 任何泛函都是它們的組合 / every functional is a combination of them
*配音長度：中文 20.9s ／ 英文 19.0s*

**畫面公式**

```
任何泛函都是它們的組合   |   every functional is a combination of them
λ ( ξ )  =  Σ λ ( βᵢ ) εᵢ ( ξ )        ⇒   λ = Σ lᵢ εᵢ
```

**旁白（繁中）**

> 再看生成性。基底展開可以改寫成：向量等於各個座標泛函在它身上的值，乘上對應的基底向量。於是任何泛函作用上去，就等於它在基底上的值乘上對應的座標泛函。所以每個泛函都是它們的組合。

**Narration (EN)**

> Spanning next. The basis expansion can be rewritten to say a vector equals the values of the coordinate functionals on it, times the matching basis vectors. So any functional applied to it equals its values on the basis, times those coordinate functionals. Every functional is a combination of them.

**動畫**

三個方框由上往下推導：基底展開改寫、套上泛函、讀出係數，最後得到 λ 是座標泛函的組合。

## Beat 4 — 對偶基底，維數相同 / the dual basis, and the same dimension
*配音長度：中文 10.9s ／ 英文 10.8s*

**畫面公式**

```
對偶基底，維數相同   |   the dual basis, and the same dimension
d ( V * )  =  d ( V )
```

**旁白（繁中）**

> 對偶空間的這組基底，就叫原來那組基底的對偶基底。馬上得到推論：對偶空間的維數等於原空間的維數。

**Narration (EN)**

> This basis for the dual space is called the dual of the original basis. A corollary follows at once: the dual space has the same dimension as the space it came from.

**動畫**

上下兩排格子一對一配好，右邊各標一個 n，於是維數相等。

## Beat 5 — 三條式子的對稱 / the symmetry of the three equations
*配音長度：中文 21.0s ／ 英文 18.7s*

**畫面公式**

```
三條式子的對稱   |   the symmetry of the three equations
ξ = Σ εᵢ ( ξ ) βᵢ        λ = Σ λ ( βᵢ ) εᵢ        λ ( ξ ) = Σ λ ( βᵢ ) εᵢ ( ξ )
```

**旁白（繁中）**

> 有三條式子值得停下來看。前兩條互為鏡像：一條把向量展開成基底的組合，係數是對偶基底作用在它身上的值；另一條把泛函展開成對偶基底的組合，係數是它作用在基底上的值。第三條本身就對稱。

**Narration (EN)**

> Three equations are worth pausing on. The first two mirror each other: one expands a vector in the basis, with coefficients got by applying the dual basis to it; the other expands a functional in the dual basis, with coefficients got by applying it to the basis. The third is symmetric by itself.

**動畫**

三條式子疊成三列，前兩條之間畫一條上下箭頭標出互為鏡像，第三條單獨列出因為它自己就對稱。

## Beat 6 — 同構會隨基底改變 / the isomorphism moves with the basis
*配音長度：中文 16.4s ／ 英文 15.0s*

**畫面公式**

```
同構會隨基底改變   |   the isomorphism moves with the basis
β  ↦  θ ( β ) : V ≅ V *        β′  ↦  θ ( β′ )  ≠  θ ( β )
```

**旁白（繁中）**

> 既然維數相同，兩邊當然同構，而且每一組基底都給出一個同構。可是那個同構會隨著選的基底改變——一般來說，一個空間跟它的對偶空間之間，沒有自然的同構。

**Narration (EN)**

> Since the dimensions agree the two are of course isomorphic, and in fact each basis defines an isomorphism. But that isomorphism varies with the basis chosen, and in general there is no natural isomorphism between a space and its dual.

**動畫**

**這一拍是本集的重點畫面。** 平面上畫一個 α 與兩組基底（青綠是標準基底，紫色是斜的那組），兩個同構各做出一個泛函，拿同一個測試向量去測，得到 1 與 -1。畫面上那兩個數字是程式從基底算出來的，不是寫死的（`_theta` 解座標再乘對偶基底），所以「同構隨基底改變」這句話在畫面上是被驗證的，不是被宣告的。

## Beat 7 — 座標空間有標準同構 / coordinate space has a standard one
*配音長度：中文 17.5s ／ 英文 14.4s*

**畫面公式**

```
座標空間有標準同構   |   coordinate space has a standard one
a  ↦  L a        L a ( x ) = Σ₁ⁿ aᵢ xᵢ        ℝⁿ  ≅  ( ℝⁿ ) *
```

**旁白（繁中）**

> 座標空間是另一回事，因為它本來就有標準基底，所以跟自己的對偶空間之間有一個標準同構：把一個 n 元組送到拿它去跟輸入作內積的那個泛函。於是可以放心把兩邊看成同一個。

**Narration (EN)**

> Coordinate space is another matter, because it comes with a standard basis and so with a standard isomorphism onto its own dual: an n-tuple goes to the functional that pairs it against the input. So the two may freely be identified.

**動畫**

座標空間的標準基底圈起來，往下接到 a ↦ L a。有標準基底，才有標準同構。

## Beat 8 — 到第二共軛空間是自然的 / to the second conjugate space it is natural
*配音長度：中文 19.5s ／ 英文 19.2s*

**畫面公式**

```
到第二共軛空間是自然的   |   to the second conjugate space it is natural
ω ( ξ , f ) = f ( ξ )        ξ ↦ ξ * *   :   V  ≅  V * *
```

**旁白（繁中）**

> 不過一個空間跟第二共軛空間——也就是對偶的對偶——確實是自然同構的。把一個向量跟一個泛函送到那個泛函在那個向量上的值，這個配對是雙線性的，於是由第 1 章的定理，向量送到它對應的映射就是線性的。

**Narration (EN)**

> A space is, however, naturally isomorphic to its second conjugate space, the dual of the dual. Sending a vector and a functional to the value of that functional on that vector is a bilinear pairing, so by a theorem of chapter one, sending a vector to its associated map is linear.

**動畫**

V、V*、V** 三個方框一列排開，下面一條長箭頭直接從 V 拉到 V**，標上 ξ ↦ ξ**——中間不必經過任何選擇。

## Beat 9 — 非零向量上找得到不為零的泛函 / a functional that does not vanish
*配音長度：中文 19.3s ／ 英文 17.7s*

**畫面公式**

```
非零向量上找得到不為零的泛函   |   a functional that does not vanish
α ≠ 0    ⇒    f ( α ) = 1    ⇒    α * * ≠ 0
```

**旁白（繁中）**

> 還剩嵌射要檢查。取一個非零向量，把它當成某組有序基底的第一個向量，再取對偶基底的第一個泛函，那個值就是一。所以它對應過去的元素不是零；兩邊維數相同，於是它同時也是雙射。

**Narration (EN)**

> Injectivity is what remains. Take a nonzero vector, make it the first vector of an ordered basis, and take the first functional of the dual basis: the value is one. So the element it goes to is not zero, and since the dimensions agree the map is bijective as well.

**動畫**

第一格標成 α 並高亮，其餘留白：把 α 排成基底的第一個向量，對偶基底的第一個泛函在它上面就是 1。

## Beat 10 — 兩邊互為對偶 / each is the dual of the other
*配音長度：中文 21.8s ／ 英文 20.4s*

**畫面公式**

```
兩邊互為對偶   |   each is the dual of the other
⟨ ξ , f ⟩ = f ( ξ )        αᵢ * * ( λⱼ ) = λⱼ ( αᵢ ) = δ ᵢⱼ
```

**旁白（繁中）**

> 這樣認同之後，一個空間跟它的對偶空間就對稱地互為對偶。所以在「泛函作用在向量上」這個寫法裡，兩個符號都是變數，常常改寫成一個左右對稱的括號記法。最後一個引理說，對偶基底這件事反過來看也一樣成立。

**Narration (EN)**

> Once that identification is made, a space and its dual are symmetrically related, each the dual of the other. So in the expression for a functional applied to a vector, both symbols are variables, and it is often rewritten with a symmetric bracket. A last lemma says the dual basis relation reads the same way round.

**動畫**

V 與 V* 兩個等寬方框左右對稱擺放，中間雙向箭頭，下面放對稱的括號記法。收在下一集的預告。
