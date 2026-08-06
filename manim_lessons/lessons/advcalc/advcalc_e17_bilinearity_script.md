# advcalc E17 — 第 1 章：雙線性與自然同構

Chapter 1: Bilinearity and Natural Isomorphisms

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 6 節（書頁 67–71）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e17_bilinearity.py`（`AdvCalcE17ZH` / `AdvCalcE17EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[17]` / `FORMULAS_ADVCALC[17]`）
- 配音：`manim_lessons/samples/audio_e17/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.90 分（174 秒）／英文 2.75 分（165 秒）

---

## Beat 0 — 對偶原則的向量空間版本 / duality, in the vector setting
*配音長度：中文 9.7s ／ 英文 9.2s*

**畫面公式**

```
對偶原則的向量空間版本   |   duality, in the vector setting
ω  :  U × V  →  W
```

**旁白（繁中）**

> 雙線性映射對理解線性代數很重要，因為它正是第零章那個對偶原則，放進向量空間之後的版本。

**Narration (EN)**

> Bilinear mappings matter for understanding linear algebra, because bilinearity is the vector-space setting for the duality principle of chapter zero.

**動畫**

U × V 的方框經 ω 送到 W。第零章的對偶原則放進向量空間之後的樣子。

## Beat 1 — 固定一個，對另一個是線性的 / hold one fixed, linear in the other
*配音長度：中文 12.1s ／ 英文 10.1s*

**畫面公式**

```
固定一個，對另一個是線性的   |   hold one fixed, linear in the other
ω ( ξ , · )   linear        ω ( · , η )   linear
```

**旁白（繁中）**

> 定義是這樣：從兩個空間的乘積到第三個空間的一個映射叫做雙線性，如果把其中一個變數固定住之後，它對另一個變數是線性的。

**Narration (EN)**

> The definition: a mapping from the product of two spaces into a third is bilinear if it is linear in each variable when the other variable is held fixed.

**動畫**

同一個方格區域切兩次：固定一個變數是一組直的切線，固定另一個是一組橫的切線。兩個方向都要線性，才叫雙線性。

## Beat 2 — 線性，但不是雙線性 / linear, but not bilinear
*配音長度：中文 18.5s ／ 英文 17.1s*

**畫面公式**

```
線性，但不是雙線性   |   linear, but not bilinear
⟨ x , y ⟩ ↦ x + y   :   linear ,  not bilinear
```

**旁白（繁中）**

> 要特別注意，這跟「在乘積空間上是線性的」完全不是同一件事。把一對數送到它們的和，在乘積空間上確實是線性映射，但它不是雙線性的——固定一個之後只是仿射，除非固定的那個是零。

**Narration (EN)**

> This is emphatically not the same notion as linearity on the product space. Sending a pair of numbers to their sum really is a linear map on the product, but it is not bilinear: hold one fixed and it is affine, not linear, unless the one held fixed is zero.

**動畫**

**反例一**：座標軸上畫兩條斜線，固定 y 之後的那一條明顯**不通過原點**（原點另標 INK 小點對照）。所以它是仿射不是線性——把一對數送到和，在乘積上是線性的，卻不是雙線性的。

## Beat 3 — 雙線性，但不是線性 / bilinear, but not linear
*配音長度：中文 15.2s ／ 英文 15.6s*

**畫面公式**

```
雙線性，但不是線性   |   bilinear, but not linear
⟨ x , y ⟩ ↦ x y   :   bilinear ,  not linear
```

**旁白（繁中）**

> 反過來，把一對數送到它們的乘積是雙線性的，卻不是線性的：兩個有序對先相加再取像，不等於兩個像相加。純量積也一樣，是雙線性而不是線性。

**Narration (EN)**

> The other way round, sending a pair of numbers to their product is bilinear but not linear: adding two ordered pairs first and then taking the image does not give the sum of the images. The scalar product is the same, bilinear but not linear.

**動畫**

**反例二**：兩個框，上面是「先加再取像」、下面是「兩個像相加」，中間一個大大的 ≠。`assert abs(lhs - rhs) > 1e-9` 先算過，確定這個反例真的不相等，不是嘴巴說。

## Beat 4 — 一個雙線性，兩個線性 / one bilinear map, two linear ones
*配音長度：中文 15.1s ／ 英文 14.8s*

**畫面公式**

```
一個雙線性，兩個線性   |   one bilinear map, two linear ones
ω  ⟷  U → Hom ( V , W )   ⟷   V → Hom ( U , W )
```

**旁白（繁中）**

> 定理六點一把雙線性的線性意義講清楚：一個雙線性映射，透過對偶，等價於一個從第一個空間到「所有線性映射」的線性映射，也等價於一個從第二個空間出發的。

**Narration (EN)**

> Theorem six point one explains the linear meaning of bilinearity: by duality a bilinear map is equivalent to a linear map from the first space into the space of all linear maps, and equally to one from the second space.

**動畫**

中間一個 ω 框，往左右兩邊各拉出雙向箭頭到兩個 Hom 框：三者透過對偶互相等價。

## Beat 5 — 把第二個變數送到那個映射 / send the second variable to that map
*配音長度：中文 15.0s ／ 英文 13.3s*

**畫面公式**

```
把第二個變數送到那個映射   |   send the second variable to that map
ω η ( ξ ) = ω ( ξ , η )        ω c η + d ζ  =  c ω η  +  d ω ζ
```

**旁白（繁中）**

> 作法就是固定一個變數。固定第二個變數，得到的是一個線性映射；而「把第二個變數送到那個線性映射」本身又是線性的——這正好就是雙線性的另外一半。

**Narration (EN)**

> The construction is to hold a variable fixed. Holding the second fixed gives a linear map; and sending the second variable to that linear map is itself linear, which is exactly the other half of bilinearity.

**動畫**

左邊一排 η 點各自送到右邊 Hom(U,W) 框裡的一個元素：固定第二個變數得到線性映射，而這個對應本身又是線性的——那正好是雙線性的另一半。

## Beat 6 — 合成本身就是雙線性的 / composition is itself bilinear
*配音長度：中文 17.3s ／ 英文 16.1s*

**畫面公式**

```
合成本身就是雙線性的   |   composition is itself bilinear
⟨ S , T ⟩  ↦  S ∘ T   :   bilinear
```

**旁白（繁中）**

> 這個重新解讀有時給出新的洞見，有時反而沒那麼有用。合成本身就是雙線性的，而前面那條「固定一個 T 從右邊合成是線性的」推論，其實只是把雙線性的一半明講出來而已。

**Narration (EN)**

> The reinterpretation sometimes gives new insight and sometimes seems less helpful. Composition is itself bilinear, and the earlier corollary about composing on the right by a fixed map is really just half of that bilinearity, stated explicitly.

**動畫**

⟨S,T⟩ ↦ S∘T 的框往下標一個「雙線性」：先前那條「固定 T 從右邊合成是線性」只是它的一半。

## Beat 7 — 線性組合公式被照亮 / the combination formula, relit
*配音長度：中文 19.7s ／ 英文 17.0s*

**畫面公式**

```
線性組合公式被照亮   |   the combination formula, relit
ω ( x , α )  =  Σ₁ⁿ xᵢ αᵢ        α ↦ ω α  :  Vⁿ  ≅  Hom ( ℝⁿ , V )
```

**旁白（繁中）**

> 但線性組合的公式與第一章那個定理，確實因此被照亮。定理六點二說：把一個係數元組與一個向量元組送到它們的線性組合，這是雙線性的；於是「把向量元組送到對應的線性組合映射」是一個同構。

**Narration (EN)**

> But the linear combination formula and the theorem from chapter one do receive new light. Theorem six point two: sending a tuple of coefficients and a tuple of vectors to their combination is bilinear, so sending a tuple of vectors to its combination map is an isomorphism.

**動畫**

純量積的框，下面 Vⁿ 與 Hom(ℝⁿ,V) 兩排點用箭頭一一對上：雙線性推出那個對應是同構。

## Beat 8 — 純量積給出的同構 / the isomorphism from the scalar product
*配音長度：中文 12.4s ／ 英文 11.9s*

**畫面公式**

```
純量積給出的同構   |   the isomorphism from the scalar product
( x , a ) = Σ₁ⁿ xᵢ aᵢ        a  ↦  L a   :   ℝⁿ  ≅  Hom ( ℝⁿ , ℝ )
```

**旁白（繁中）**

> 一個特例：純量積是雙線性的，所以「把一個 n 元組送到對應的線性泛函」，是從座標空間到它上面所有線性泛函所成空間的同構。

**Narration (EN)**

> A special case: the scalar product is bilinear, so sending an n-tuple to its linear functional is an isomorphism from coordinate n-space onto the space of all linear functionals on it.

**動畫**

ℝⁿ 與「ℝⁿ 上的線性泛函」兩排點一一對應，這條對應是自然的。

## Beat 9 — 同一個矩陣，兩種讀法 / one matrix, two readings
*配音長度：中文 17.5s ／ 英文 18.7s*

**畫面公式**

```
同一個矩陣，兩種讀法   |   one matrix, two readings
{ tᵢⱼ }  ∈  ℝ ᵐ ˣ ⁿ        { tᵢⱼ }  ∈  ( ℝᵐ ) ⁿ
```

**旁白（繁中）**

> 接著是自然同構。有時候兩個空間關係密切到會挑出一個特定的同構。一個矩陣可以看成兩個整數指標的函數，也可以看成一串行向量——這兩個看法之間的對應，就是自然的。

**Narration (EN)**

> Now natural isomorphisms. Sometimes two spaces are related so closely that one particular isomorphism between them is singled out. A matrix can be viewed as a function of two integer indices, or as a sequence of column vectors, and the correspondence between those views is natural.

**動畫**

同一個 5×4 數字陣列畫兩次：左邊用細框標成一格一格（兩個指標的函數），右邊改用直長框圈起每一行（一串行向量），中間一個大等號。同一個對象的兩種讀法。

## Beat 10 — 暫時的認同，與永久的 / a transient identification, and a permanent one
*配音長度：中文 20.7s ／ 英文 20.2s*

**畫面公式**

```
暫時的認同，與永久的   |   a transient identification, and a permanent one
arbitrary  :  transient        natural  :  permanent
```

**旁白（繁中）**

> 一般的同構只是暫時把兩個空間認同起來；換一個同構，就換一種認同。自然同構造成的是永久的認同：我們會直接把矩陣「當成」列的序列、行的序列、或者兩個指標的函數，覺得那是同一個對象的三個面向。

**Narration (EN)**

> An arbitrary isomorphism identifies two spaces only transiently; shift to a different one and the identification changes. A natural isomorphism makes it permanent: we think of a matrix as being a sequence of rows, of columns, or a function of two indices, three aspects of one object.

**動畫**

兩個並排的框，各寫一種認同方式：一般同構是暫時的，自然同構是永久的。
