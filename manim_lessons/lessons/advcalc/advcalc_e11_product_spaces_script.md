# advcalc E11 — 第 1 章：積空間與 Hom(V, W)

Chapter 1: Product Spaces and Hom(V, W)

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 3 節（書頁 43–46）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e11_product_spaces.py`（`AdvCalcE11ZH` / `AdvCalcE11EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[11]` / `FORMULAS_ADVCALC[11]`）
- 配音：`manim_lessons/samples/audio_e11/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.03 分（182 秒）／英文 2.76 分（165 秒）

---

## Beat 0 — 每個指標都落進同一個 W / every index lands in the same W
*配音長度：中文 18.4s ／ 英文 18.3s*

**畫面公式**

```
每個指標都落進同一個 W   |   every index lands in the same W
Wᴬ  =  { f : A → W }        ( f + g ) ( a )  =  f ( a ) + g ( a )
```

**旁白（繁中）**

> 前面看過：W 是向量空間、A 是任意集合時，所有從 A 到 W 的函數所成的空間，跟實值函數空間一樣是向量空間。加法逐點做，數乘也逐點做，向量律成立的理由一模一樣。

**Narration (EN)**

> We have seen that when W is a vector space and A is any set, the space of all functions from A into W is a vector space in the same way the real-valued ones are. Addition is pointwise, and so is multiplication by scalars, for exactly the same reasons.

**動畫**

左邊 I 的四個指標點，四支箭頭全部射進同一個 W 的橢圓。

## Beat 1 — 但沒有理由要同一個 / but there is no reason it must be
*配音長度：中文 15.2s ／ 英文 15.2s*

**畫面公式**

```
但沒有理由要同一個   |   but there is no reason it must be
∏ᵢ Wᵢ  =  { f  :  dom f = I  ,  f ( i ) ∈ Wᵢ }
```

**旁白（繁中）**

> 但沒有理由每個指標都要用同一個 W。給一族用 I 編號的向量空間，它們的笛卡兒積定義成：所有定義域是 I、而且在每個 i 取的值都落在第 i 個空間裡的函數。

**Narration (EN)**

> But there is no reason to use the same W at every index. Given a collection of vector spaces indexed by I, their Cartesian product is defined as all functions with domain I whose value at each i lies in the ith space.

**動畫**

同一張圖再畫一次，這次四支箭頭各自射進屬於自己的空間——兩張圖的差別，就是積空間的定義。

## Beat 2 — 球面上的向量場 / a vector field on the sphere
*配音長度：中文 20.5s ／ 英文 17.4s*

**畫面公式**

```
球面上的向量場   |   a vector field on the sphere
S = { x : Σ₁³ xᵢ² = 1 }        Wₓ  ⊂  ℝ³        ∏ₓ ∈ S Wₓ
```

**旁白（繁中）**

> 書上舉了一個很具體的例子。單位球面上，每一點的切平面平移到原點就是一個子空間。那麼所有這些子空間的乘積裡的一個元素，就是在球面每一點指定一個平行於該點切平面的向量——也就是球面上的一個向量場。

**Narration (EN)**

> The book gives a concrete example. On the unit sphere, the tangent plane at each point, translated to the origin, is a subspace. An element of the product of all of those assigns to each point of the sphere a vector parallel to the tangent plane there: a vector field.

**動畫**

書上的 Fig. 1.8：軸測投影的球面網格，三個點上各自畫出切平面與一支切向量。

## Beat 3 — 座標投影，不是座標泛函 / a projection, not a functional
*配音長度：中文 14.8s ／ 英文 13.0s*

**畫面公式**

```
座標投影，不是座標泛函   |   a projection, not a functional
πⱼ ( f )  =  f ( j )   ∈   Wⱼ
```

**旁白（繁中）**

> 積空間上的第 j 個座標投影，還是在 j 取值。只是這時取到的值落在一個向量空間裡，而不是落在實數裡，所以叫它座標投影，而不是座標泛函。

**Narration (EN)**

> The jth coordinate projection on a product space is still evaluation at j. Here its values lie in a vector space rather than in the reals, so it is called a coordinate projection rather than a coordinate functional.

**動畫**

左邊一個裝著 f 的橢圓，箭頭經 πⱼ 指到右邊的 Wⱼ，裡面掉出來的是一支向量，不是一個數。

## Beat 4 — 運算被「投影要線性」逼出來 / linearity of the projections forces it
*配音長度：中文 17.1s ／ 英文 16.2s*

**畫面公式**

```
運算被「投影要線性」逼出來   |   linearity of the projections forces it
πⱼ ( f + g )  =  πⱼ ( f ) + πⱼ ( g )        πⱼ ( x f )  =  x πⱼ ( f )
```

**旁白（繁中）**

> 關鍵的一句是：積空間上的向量運算，被「所有座標投影都要是線性的」這個要求唯一決定。兩個元素的和，必須是那個在每個 j 的值等於兩者在 j 的值相加的元素；數乘也一樣。

**Narration (EN)**

> The key point is that the vector operations on a product space are uniquely determined by requiring that all the coordinate projections be linear. The sum of two elements must be the one whose value at each j is the sum of their values there, and likewise for scalars.

**動畫**

f、g、f+g 三個橢圓各自經 πⱼ 讀出值，右邊用平行四邊形畫出兩支向量相加。

## Beat 5 — 恰好只有一種辦法 / in exactly one way
*配音長度：中文 20.2s ／ 英文 17.3s*

**畫面公式**

```
恰好只有一種辦法   |   in exactly one way
∏ᵢ Wᵢ   :   unique
```

**旁白（繁中）**

> 所以定理是：一族向量空間的笛卡兒積，恰好只有一種辦法做成向量空間，使得所有座標投影都線性。證明就是把之前那些公理檢查原封不動再走一遍——那些論證從來沒要求被加的函數值都落在同一個空間。

**Narration (EN)**

> So the theorem: the Cartesian product of a collection of vector spaces can be made into a vector space in exactly one way so that the coordinate projections are all linear. The proof is the earlier axiom check verbatim, which never asked that the values lie in one space.

**動畫**

上方一個「所有投影都線性」的方框，往下連到三個候選運算，只有第一個活下來，其餘兩個被劃掉。

## Beat 6 — 把線性的那些挑出來 / singling out the linear ones
*配音長度：中文 12.6s ／ 英文 12.6s*

**畫面公式**

```
把線性的那些挑出來   |   singling out the linear ones
Hom ( V , W )   ⊂   Wⱽ
```

**旁白（繁中）**

> 接著是 Hom。當定義域本身是一個向量空間的時候，我們特別把所有線性映射從函數空間裡挑出來，這個子集就寫成 Hom V W。

**Narration (EN)**

> Now Hom. When the domain is itself a vector space, we single out from the function space the subset consisting of all the linear mappings, and that subset is written Hom of V and W.

**動畫**

巢狀的橢圓：外圈是所有映射，內圈打亮的是線性的那些。

## Beat 7 — Hom 是一個子空間 / Hom is a subspace
*配音長度：中文 15.3s ／ 英文 14.1s*

**畫面公式**

```
Hom 是一個子空間   |   Hom is a subspace
( S + T ) ( xα + yβ )  =  x ( S + T ) ( α )  +  y ( S + T ) ( β )
```

**旁白（繁中）**

> 第一個定理是形式上的：Hom 是所有映射所成空間的一個子空間。兩個線性映射相加還是線性、乘上純量還是線性，而且零變換在裡面，所以非空。

**Narration (EN)**

> The first theorem is a formality: Hom is a subspace of the space of all mappings. The sum of two linear maps is linear, so is a scalar multiple, and the zero transformation is in there, so it is nonempty.

**動畫**

S 與 T 各自把同一個平行四邊形送成不同形狀，S+T 是第三個——三個都還是平行四邊形。

## Beat 8 — 合成還是線性 / composition stays linear
*配音長度：中文 17.3s ／ 英文 15.8s*

**畫面公式**

```
合成還是線性   |   composition stays linear
T ∈ Hom ( V , W )  ,  S ∈ Hom ( W , X )   ⇒   S ∘ T ∈ Hom ( V , X )
```

**旁白（繁中）**

> 接下來是合成。兩個線性映射合起來還是線性的。這句話很基本，但它需要定義域與上域對得上；這一節的敘述都是這樣，論證簡單，可是被討論的對象會越來越複雜。

**Narration (EN)**

> Next, composition. The composition of two linear maps is linear. The statement is elementary but it needs the obvious hypotheses on domains and codomains, which is the pattern here: simple arguments, but objects of growing complexity.

**動畫**

V、W、X 三個橢圓與兩支箭頭，底下一支 S∘T 的長箭頭把頭尾接起來。

## Beat 9 — 分配律，兩邊都成立 / distributive on both sides
*配音長度：中文 11.1s ／ 英文 10.0s*

**畫面公式**

```
分配律，兩邊都成立   |   distributive on both sides
( S₁ + S₂ ) ∘ T = S₁∘T + S₂∘T        c ( S ∘ T ) = ( cS ) ∘ T = S ∘ ( cT )
```

**旁白（繁中）**

> 同一個定理還說了兩件事：合成對加法有分配律，而且兩邊都成立；另外，合成與純量乘法可以交換次序。

**Narration (EN)**

> The same theorem adds two more things: composition distributes over addition, on both sides, and composition commutes with multiplication by scalars.

**動畫**

T 分岔到 S₁ 與 S₂，再匯回一個 Σ 方塊，示範分配律。

## Beat 10 — 固定 T 從右邊合成 / composing with a fixed T
*配音長度：中文 19.5s ／ 英文 15.6s*

**畫面公式**

```
固定 T 從右邊合成   |   composing with a fixed T
S  ↦  S ∘ T   :   Hom ( W , X )  →  Hom ( V , X )
```

**旁白（繁中）**

> 最後一個推論。把某個固定的 T 從右邊合成上去，這件事本身就是一個線性變換，從一個 Hom 空間到另一個 Hom 空間。而且如果 T 是同構，這個變換也是同構——因為拿 T 的反函數去合成就能還原。

**Narration (EN)**

> A last corollary. Composing with a fixed T on the right is itself a linear transformation from one Hom space to another. And if T is an isomorphism then so is that transformation, since composing with the inverse of T undoes it.

**動畫**

兩欄點一一對應：Hom(W, X) 與 Hom(V, X)，中間標著「∘ T」。
