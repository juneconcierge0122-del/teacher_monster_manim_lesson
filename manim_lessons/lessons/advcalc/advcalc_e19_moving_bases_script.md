# advcalc E19 — 第 2 章：基底之間的搬移

Chapter 2: Moving Between Bases

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 1 節（書頁 74–77）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e19_moving_bases.py`（`AdvCalcE19ZH` / `AdvCalcE19EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[19]` / `FORMULAS_ADVCALC[19]`）
- 配音：`manim_lessons/samples/audio_e19/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.73 分（164 秒）／英文 2.58 分（155 秒）

---

## Beat 0 — 同構把基底送到基底 / an isomorphism carries a basis to a basis
*配音長度：中文 9.6s ／ 英文 9.7s*

**畫面公式**

```
同構把基底送到基底   |   an isomorphism carries a basis to a basis
α   basis for  V  ,  T   iso    ⇒    { T ( αᵢ ) }   basis for  W
```

**旁白（繁中）**

> 從基底存在這件事，可以推出幾個簡單但常用的結論。第一個是：同構把基底送到基底。

**Narration (EN)**

> From the existence of bases follow a few elementary but much-used conclusions. The first: an isomorphism carries a basis to a basis.

**動畫**

基底經一個同構送過去，像仍然是一組基底。

## Beat 1 — 像就是它的 skeleton / the images are its skeleton
*配音長度：中文 15.3s ／ 英文 16.3s*

**畫面公式**

```
像就是它的 skeleton   |   the images are its skeleton
T ∘ L α   iso        skeleton  =  { T ( αᵢ ) }
```

**旁白（繁中）**

> 證明很短：基底同構後面接上那個同構，還是一個同構，而它的 skeleton 正好就是那些像。所以任何一組基底，都可以看成標準基底在某個基底同構之下的像。

**Narration (EN)**

> The proof is short. A basis isomorphism followed by the isomorphism is again an isomorphism, and its skeleton is exactly the family of images. So any basis can be seen as the image of the standard basis under some basis isomorphism.

**動畫**

兩個同構接起來還是同構，而它的 skeleton 正好是那些像。

## Beat 2 — 反過來也對 / and the converse holds
*配音長度：中文 12.5s ／ 英文 12.3s*

**畫面公式**

```
反過來也對   |   and the converse holds
θ  :  ℝᴵ → V   iso    ⇒    αⱼ  =  θ ( δ ʲ )
```

**旁白（繁中）**

> 反過來也對：任何一個從座標空間到 V 的同構，都會變成某一組基底的基底同構——只要把它作用在標準基底上，得到的那組向量就是。

**Narration (EN)**

> The converse holds too: any isomorphism from coordinate space onto V becomes the basis isomorphism of some basis, namely the family obtained by applying it to the standard basis.

**動畫**

反過來：任何從座標空間來的同構，作用在標準基底上就得到一組基底。所以兩者是同一件事。

## Beat 3 — 互補子空間的基底，聯集起來 / bases of complements, taken together
*配音長度：中文 17.9s ／ 英文 17.1s*

**畫面公式**

```
互補子空間的基底，聯集起來   |   bases of complements, taken together
V  =  X ⊕ Y    ⇒    basis ( X )  ∪  basis ( Y )  =  basis ( V )
```

**旁白（繁中）**

> 接著是一個關於互補子空間的定理：X 與 Y 互補時，X 的一組基底與 Y 的一組基底聯集起來，就是 V 的基底。反過來，把 V 的一組基底分成兩份，那兩份的線性擴張就是互補的子空間。

**Narration (EN)**

> Next a theorem about complements. If two subspaces are complementary, then a basis for one together with a basis for the other is a basis for V. Conversely, partition a basis for V into two sets and their linear spans are complementary subspaces.

**動畫**

軸測圖：X 是平面、Y 是穿出平面的線，兩者互補。`assert LDIR[2] > 0.4` 確保 Y 真的離開了 X 的平面。兩邊的基底聯集起來就是 V 的基底。

## Beat 4 — 拆成兩邊，兩邊都得是零 / split it in two, and both halves vanish
*配音長度：中文 17.0s ／ 英文 17.0s*

**畫面公式**

```
拆成兩邊，兩邊都得是零   |   split it in two, and both halves vanish
Σ𝘑∪𝘒 xᵢ αᵢ = 0    ⇒    ξ = η = 0    ⇒    xᵢ = 0
```

**旁白（繁中）**

> 證明分兩半。聯集生成 V，因為它的線性擴張同時包含 X 與 Y；而如果有一個零組合，把它拆成落在 X 的那部分與落在 Y 的那部分，兩邊都必須是零，於是每個係數都是零。

**Narration (EN)**

> The proof has two halves. The union spans V because its span contains both subspaces. And if some combination vanishes, split it into the part lying in one subspace and the part lying in the other; both must be zero, and then every coefficient is zero.

**動畫**

把一個零組合拆成落在 X 的那半與落在 Y 的那半；X 與 Y 只交於零，所以兩邊都得是零。

## Beat 5 — 直和也一樣 / and the same for a direct sum
*配音長度：中文 9.5s ／ 英文 10.4s*

**畫面公式**

```
直和也一樣   |   and the same for a direct sum
V = ⊕₁ⁿ Vᵢ    ⇒    B = ⋃₁ⁿ Bᵢ   basis
```

**旁白（繁中）**

> 推論用歸納推上去：V 是一族子空間的直和時，各個子空間的基底聯集起來，就是 V 的一組基底。

**Narration (EN)**

> A corollary carries this up by induction: when V is the direct sum of a family of subspaces, the union of bases for those subspaces is a basis for V.

**動畫**

V 是一族子空間的直和時，各基底的聯集就是 V 的基底（歸納）。

## Beat 6 — 指定基底的像，映射就唯一 / name the images of a basis, and the map is unique
*配音長度：中文 15.4s ／ 英文 13.7s*

**畫面公式**

```
指定基底的像，映射就唯一   |   name the images of a basis, and the map is unique
β   basis  ,  α ∈ Wⁿ    ⇒    ∃ ! S ,   S ( βᵢ ) = αᵢ
```

**旁白（繁中）**

> 再來是一個存在性定理。給定 V 的一組有序基底，以及 W 裡任意一個同樣長度的向量元組，那麼恰好有一個線性映射，把基底的第 i 個向量送到那個元組的第 i 項。

**Narration (EN)**

> Then an existence theorem. Given an ordered basis for V and any tuple of vectors of the same length in W, there is exactly one linear map sending the ith basis vector to the ith entry of that tuple.

**動畫**

一組有序基底、一個 W 裡等長的元組，中間恰好一個線性映射對上。重點在「恰好一個」。

## Beat 7 — 先翻成座標，再照新的組回去 / into coordinates, then rebuilt
*配音長度：中文 13.5s ／ 英文 13.5s*

**畫面公式**

```
先翻成座標，再照新的組回去   |   into coordinates, then rebuilt
S  =  L α  ∘  ( L β ) ⁻¹
```

**旁白（繁中）**

> 證明就是把座標同構接上線性組合映射。這件事之所以成立，關鍵是基底同構可逆——先把向量翻成座標，再照新的元組組回去。

**Narration (EN)**

> The proof is the coordinate isomorphism followed by a combination map. What makes it work is that the basis isomorphism is invertible: translate the vector into coordinates, then rebuild it against the new tuple.

**動畫**

存在性定理的證明畫成一趟**繞路**：向量先翻成座標，再照新元組組回去。那段繞路就是整個論證，公式列只看得到起點與終點。

## Beat 8 — 那個映射怎麼隨元組變化？ / how does that map vary with the tuple?
*配音長度：中文 10.7s ／ 英文 8.5s*

**畫面公式**

```
那個映射怎麼隨元組變化？   |   how does that map vary with the tuple?
α  ↦  S α
```

**旁白（繁中）**

> 自然要問：那個唯一的映射，會怎麼隨著 W 裡的那個元組變化？答案是「線性地，而且是同構地」。

**Narration (EN)**

> It is natural to ask how that unique map varies with the tuple chosen in W. The answer is linearly, and in fact isomorphically.

**動畫**

左邊 Wⁿ 的元組、右邊對應的 S，元組動則映射跟著動——問題是怎麼動。

## Beat 9 — 線性地，而且是同構地 / linearly, and isomorphically
*配音長度：中文 15.9s ／ 英文 16.0s*

**畫面公式**

```
線性地，而且是同構地   |   linearly, and isomorphically
α  ↦  S α   :   Wⁿ  ≅  Hom ( V , W )
```

**旁白（繁中）**

> 定理：固定 V 的一組有序基底，把 W 裡的元組送到對應的那個唯一映射，這是從 W 的 n 次冪到所有線性映射所成空間的同構。證明就是把第一章那兩個同構合起來。

**Narration (EN)**

> The theorem: fix an ordered basis for V, and send each tuple in W to its unique map. That is an isomorphism from the nth power of W onto the space of all linear maps. The proof composes the two isomorphisms from chapter one.

**動畫**

答案：固定有序基底之後，Wⁿ → Hom(V,W) 是一個同構，由第一章那兩個同構合成。

## Beat 10 — 無限基底 / infinite bases
*配音長度：中文 25.6s ／ 英文 19.2s*

**畫面公式**

```
無限基底   |   infinite bases
ℝ𝘐  =  L ( { δ ⁱ : i ∈ I } )   ⊂   ℝᴵ
```

**旁白（繁中）**

> 最後書上補了無限基底，那一段標了星號。Kronecker 函數的定義照舊，但它們不再生成整個函數空間，只生成「除了有限多個位置以外都是零」的那個子空間。用選擇公理可以證明每個向量空間都有基底，不過無限基底在分析上不太好用，所以現在先專注在有限維。

**Narration (EN)**

> The book closes with infinite bases, in a starred passage. The Kronecker functions no longer span the whole function space, only the functions that are zero except at finitely many places. The axiom of choice gives every space a basis, but such bases are of little use in analysis.

**動畫**

兩個同心的區域：外圈是整個函數空間，內圈是「除了有限多個位置以外都是零」的那一塊。Kronecker 函數只生成內圈。
