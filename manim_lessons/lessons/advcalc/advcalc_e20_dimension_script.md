# advcalc E20 — 第 2 章：維數

Chapter 2: Dimension

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 2 節（書頁 77–81）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e20_dimension.py`（`AdvCalcE20ZH` / `AdvCalcE20EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[20]` / `FORMULAS_ADVCALC[20]`）
- 配音：`manim_lessons/samples/audio_e20/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.93 分（176 秒）／英文 2.86 分（172 秒）

---

## Beat 0 — 兩組基底，個數永遠一樣 / two bases, always the same count
*配音長度：中文 12.0s ／ 英文 11.5s*

**畫面公式**

```
兩組基底，個數永遠一樣   |   two bases, always the same count
# basis₁  =  # basis₂  =  d ( V )
```

**旁白（繁中）**

> 維數這個概念，靠的是一件事實：同一個空間的兩組基底，元素個數永遠一樣。這個共同的個數，就叫做 V 的維數。

**Narration (EN)**

> The concept of dimension rests on one fact: two different bases for the same space always contain the same number of elements. That common number is called the dimension of the space.

**動畫**

同一個空間畫兩組基底，個數一樣。維數這個概念整個靠這件事。

## Beat 1 — 同構，若且唯若維數相同 / isomorphic exactly when the dimensions agree
*配音長度：中文 16.4s ／ 英文 16.4s*

**畫面公式**

```
同構，若且唯若維數相同   |   isomorphic exactly when the dimensions agree
V ≅ W   ⇔   d ( V ) = d ( W )
```

**旁白（繁中）**

> 它把 V 的一切都講完了，只差到同構為止：兩個空間之間存在同構，若且唯若它們的維數相同。書上只處理有限的維數；不是有限維的時候，維數是一個無限基數。

**Narration (EN)**

> It tells all there is to know about the space to within isomorphism: an isomorphism between two spaces exists exactly when they have the same dimension. The book considers only finite dimensions; otherwise the dimension is an infinite cardinal number.

**動畫**

有同構若且唯若維數相同——所以維數把 V 講完了，只差到同構為止。

## Beat 2 — 有限維上，滿的就是同構 / on a finite-dimensional space, onto means iso
*配音長度：中文 18.5s ／ 英文 17.9s*

**畫面公式**

```
有限維上，滿的就是同構   |   on a finite-dimensional space, onto means iso
dim V < ∞  ,  T ∈ Hom V   onto    ⇒    T   iso
```

**旁白（繁中）**

> 先一個引理：V 是有限維、而一個從 V 到自己的線性映射是滿的，那麼它就是同構。理由是：取能生成 V 的最少個數，那組生成集就是基底；映射是滿的所以像也生成 V，於是像也是基底。

**Narration (EN)**

> A lemma first: if the space is finite-dimensional and a map from it to itself is surjective, it is an isomorphism. Take the smallest number of elements that can span the space; that set is a basis, and since the map is onto, the images span too and are a basis as well.

**動畫**

取能生成 V 的最少個數，那組就是基底；T 是滿的所以像也生成，於是像也是基底。

## Beat 3 — 假設一組比較少 / suppose one basis were smaller
*配音長度：中文 15.6s ／ 英文 15.6s*

**畫面公式**

```
假設一組比較少   |   suppose one basis were smaller
θ : ℝⁿ → V  ,  φ : ℝᵐ → V  ,  m < n
```

**旁白（繁中）**

> 定理：有限維空間的所有基底，元素個數都一樣。證明用反證法：假設一組比另一組少，就可以把大的那個座標空間拆成兩塊，造出一個往小的那塊的投影。

**Narration (EN)**

> The theorem: all bases for a finite-dimensional space have the same number of elements. The proof is by contradiction: suppose one basis is smaller, and split the larger coordinate space in two so as to build a projection onto the smaller piece.

**動畫**

反證法的起手式：假設一組比另一組少，把大的座標空間拆成兩塊，造一個往小塊的投影 π。

## Beat 4 — 投影不可能是同構 / that projection cannot be an isomorphism
*配音長度：中文 14.8s ／ 英文 14.8s*

**畫面公式**

```
投影不可能是同構   |   that projection cannot be an isomorphism
π ( δ ⁿ ) = 0        π = T ⁻¹ ∘ ( T ∘ π )   iso        ⇒⇐
```

**旁白（繁中）**

> 接著那個投影可以寫成兩個同構的合成，所以它自己也是同構——可是它把最後一個標準基底向量送到零，這是矛盾。所以沒有哪一組基底能比另一組少。

**Narration (EN)**

> That projection can then be written as a composition of two isomorphisms, so it is an isomorphism itself. But it carries the last standard basis vector to zero, which is a contradiction. So no basis can be smaller than another.

**動畫**

π 寫成兩個同構的合成，所以自己也是同構；可是它把最後一個標準基底向量送到零——矛盾。

## Beat 5 — 座標空間確實是 n 維的 / coordinate n-space really is n-dimensional
*配音長度：中文 12.9s ／ 英文 12.6s*

**畫面公式**

```
座標空間確實是 n 維的   |   coordinate n-space really is n-dimensional
d ( ℝⁿ )  =  n
```

**旁白（繁中）**

> 每組基底共有的那個整數，就叫 V 的維數。座標空間的標準基底有 n 個元素，所以 n 維座標空間在這個精確的意義下確實是 n 維的。

**Narration (EN)**

> The integer common to every basis is the dimension of the space. The standard basis for coordinate n-space has n elements, so coordinate n-space is n-dimensional in this precise sense.

**動畫**

標準基底有 n 個元素，所以 ℝⁿ 在這個精確的意義下是 n 維的。

## Beat 6 — 維數把一切講完了 / the dimension tells the whole story
*配音長度：中文 15.3s ／ 英文 16.9s*

**畫面公式**

```
維數把一切講完了   |   the dimension tells the whole story
d ( V ) = d ( W )   ⇔   V ≅ W
```

**旁白（繁中）**

> 推論：兩個有限維空間同構，若且唯若維數相同。一個方向是因為同構把基底送到基底、個數不變；另一個方向是因為兩個都同構於同一個座標空間。

**Narration (EN)**

> A corollary: two finite-dimensional spaces are isomorphic exactly when they have the same dimension. One direction holds because an isomorphism carries a basis to a basis of the same size, the other because both are isomorphic to the same coordinate space.

**動畫**

兩個框對比：同構推出維數相同（基底送到基底、個數不變），維數相同推出同構（都同構於同一個座標空間）。

## Beat 7 — 子空間也是有限維 / a subspace is finite-dimensional too
*配音長度：中文 18.4s ／ 英文 17.0s*

**畫面公式**

```
子空間也是有限維   |   a subspace is finite-dimensional too
M ⊂ V  ,  dim V < ∞    ⇒    dim M < ∞
```

**旁白（繁中）**

> 定理：有限維空間的每一個子空間也是有限維的。作法是看子空間裡所有的有限獨立子集，它們都能擴充成 V 的基底，所以個數有上界；取個數最大的那個，它的線性擴張就是整個子空間。

**Narration (EN)**

> The theorem: every subspace of a finite-dimensional space is itself finite-dimensional. Each finite independent subset of it extends to a basis for the whole space, so their sizes are bounded; take one of maximum size and its span is the whole subspace.

**動畫**

M 裡的有限獨立子集每個都能擴充成 V 的基底，所以個數有上界；取最大的那個，擴張就是整個 M。

## Beat 8 — 所以每個子空間都有補空間 / so every subspace has a complement
*配音長度：中文 12.9s ／ 英文 13.1s*

**畫面公式**

```
所以每個子空間都有補空間   |   so every subspace has a complement
basis ( M )  ⊂  basis ( V )        N = L ( added )        V = M ⊕ N
```

**旁白（繁中）**

> 推論：有限維空間的每一個子空間都有補空間。把子空間的基底擴充成 V 的基底，多出來那些向量的線性擴張，就是一個補空間。

**Narration (EN)**

> A corollary: every subspace of a finite-dimensional space has a complement. Extend a basis for the subspace to a basis for the whole space, and the linear span of the added vectors is a complement.

**動畫**

把 M 的基底擴充成 V 的基底，多出來那些的擴張就是補空間。

## Beat 9 — 交集要扣回來 / the intersection has to be subtracted back
*配音長度：中文 16.2s ／ 英文 16.7s*

**畫面公式**

```
交集要扣回來   |   the intersection has to be subtracted back
d ( ⊕₁ⁿ Vᵢ ) = Σ₁ⁿ d ( Vᵢ )        d ( U + W ) + d ( U ∩ W ) = d ( U ) + d ( W )
```

**旁白（繁中）**

> 接著是兩個維數等式。第一個：直和的維數，等於各項維數相加。第二個更有意思：兩個子空間的和的維數，加上它們交集的維數，等於兩個維數相加。

**Narration (EN)**

> Then two dimensional identities. The first: the dimension of a direct sum is the sum of the dimensions. The second is more interesting: the dimension of the sum of two subspaces, plus the dimension of their intersection, equals the sum of the two dimensions.

**動畫**

**這一拍是全集最值得畫的**：三維空間裡兩個平面交於一條線。2 + 2 = 4，但和只有 3 維——交集被算了兩次，所以要扣回來。`assert dU + dW == dSum + dInt` 而且四個數字都是從畫出來的物件數出來的，不是寫死在字串裡。

## Beat 10 — 零空間加值域，等於定義域 / null space plus range is the domain
*配音長度：中文 21.8s ／ 英文 18.6s*

**畫面公式**

```
零空間加值域，等於定義域   |   null space plus range is the domain
d ( V ) = d ( N ) + d ( R )        d ( Hom ( V , W ) ) = m n
```

**旁白（繁中）**

> 還有兩個。零空間的維數加上值域的維數，等於定義域的維數；推論是，上域的維數與定義域相同時，嵌射、滿射、雙射這三件事完全等價。最後一個：所有線性映射所成空間的維數，是兩邊維數的乘積。

**Narration (EN)**

> Two more. The dimension of the null space plus that of the range equals the dimension of the domain; so when the codomain has the same dimension as the domain, injectivity, surjectivity and bijectivity are equivalent. Last: the space of all linear maps has dimension the product.

**動畫**

零空間與值域兩塊拼成定義域；上域維數相同時，嵌射／滿射／雙射三者等價。
