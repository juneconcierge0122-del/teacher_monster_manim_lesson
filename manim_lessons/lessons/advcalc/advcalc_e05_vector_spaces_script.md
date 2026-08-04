# advcalc E05 — 第 1 章：向量空間與子空間

Chapter 1: Vector Spaces and Subspaces

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 1 節前半（書頁 21–25）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e05_vector_spaces.py`（`AdvCalcE05ZH` / `AdvCalcE05EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[5]` / `FORMULAS_ADVCALC[5]`）
- 配音：`manim_lessons/samples/audio_e05/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.45 分（207 秒）／英文 3.08 分（185 秒）

---

## Beat 0 — 微積分加上向量空間理論 / calculus plus the theory of vector spaces
*配音長度：中文 22.1s ／ 英文 16.2s*

**畫面公式**

```
微積分加上向量空間理論   |   calculus plus the theory of vector spaces
Ch 1 :  V          Ch 2 :  dim V < ∞
```

**旁白（繁中）**

> 第一章開始講向量空間。多變數的微積分把單變數的微積分與向量空間理論接在一起，而處理得好不好，直接取決於這套理論用得夠不夠徹底。所以書上花前兩章專講向量空間本身：這一章講一般的，下一章講有限維的。

**Narration (EN)**

> Chapter one begins vector spaces. The calculus of several variables unites the calculus of one variable with the theory of vector spaces, and how well it goes depends on how thoroughly that theory is used. So the first two chapters study vector spaces themselves.

**動畫**

「單變數微積分」與「向量空間理論」兩個方框匯流到「多變數微積分」，再分出第 1 章與第 2 章。

## Beat 1 — 平行四邊形法則 / the parallelogram rule
*配音長度：中文 17.9s ／ 英文 15.9s*

**畫面公式**

```
平行四邊形法則   |   the parallelogram rule
OA  +  OB  =  OP
```

**旁白（繁中）**

> 先從讀者大概已經見過的幾何向量開始。它們是從一個選定的原點畫出的箭頭，相加用平行四邊形法則：以兩個箭頭為鄰邊作平行四邊形，從原點出發的那條對角線就是它們的和。

**Narration (EN)**

> We start from the geometric vectors the reader has probably met: arrows drawn from a chosen origin. Two of them are added by the parallelogram rule. Build the parallelogram having the two arrows as sides, and the diagonal from the origin is their sum.

**動畫**

書上的 Fig. 1.1：O、A、B 三點，虛線補成平行四邊形，從 O 出發的對角線 OP 用粗橘線畫出。

## Beat 2 — 乘上一個數 / multiplication by a number
*配音長度：中文 15.9s ／ 英文 17.5s*

**畫面公式**

```
乘上一個數   |   multiplication by a number
x ( OA )  =  OB        | OB |  =  | x | · | OA |
```

**旁白（繁中）**

> 向量也可以乘上一個數。把一個箭頭乘上 x，得到的是同一條直線上的另一個箭頭，長度是原來的 x 倍的絕對值；x 是正的就在原點的同一側，是負的就在另一側。

**Narration (EN)**

> Vectors can also be multiplied by numbers. Multiplying an arrow by x gives another arrow along the same line, whose length is the absolute value of x times the original. It lies on the same side of the origin when x is positive, the opposite side when x is negative.

**動畫**

書上的 Fig. 1.2：同一條直線上的 O、A、B、C。B 是 1.5 倍的 A，C 是 −0.5 倍，示範正負決定落在原點的哪一側。

## Beat 3 — 結合律：同一條對角線 / associativity: the same diagonal
*配音長度：中文 19.1s ／ 英文 17.4s*

**畫面公式**

```
結合律：同一條對角線   |   associativity: the same diagonal
( OA + OB ) + OC  =  OA + ( OB + OC )  =  OX
```

**旁白（繁中）**

> 這兩個運算滿足一些代數律。不過書上提醒，幾何的證明通常比較粗略，說服力有餘而嚴密不足。像加法結合律的標準證明，就是畫一個平行六面體，去看那條從原點出發的對角線。

**Narration (EN)**

> These two operations satisfy certain laws of algebra. The book warns that geometric proofs of them are sketchy, more plausibility argument than airtight logic. The usual proof of the associative law is a picture of a parallelepiped and its diagonal from the origin.

**動畫**

書上的 Fig. 1.3：軸測投影的平行六面體。兩條灰色中繼箭頭 OP 與 OQ 各代表一種分組，最後都落在同一個角 X。

## Beat 4 — 座標三元組：逐項相加 / coordinate triples: added entry by entry
*配音長度：中文 18.2s ／ 英文 16.9s*

**畫面公式**

```
座標三元組：逐項相加   |   coordinate triples: added entry by entry
⟨ x₁ , x₂ , x₃ ⟩ + ⟨ y₁ , y₂ , y₃ ⟩ = ⟨ x₁+y₁ , x₂+y₂ , x₃+y₃ ⟩
```

**旁白（繁中）**

> 另一個大家可能見過的系統是座標三元組。這裡的三維向量是三個數排成的有序組，加法與數乘都是逐項代數地定義的。向量律對這種對象好證得多，因為幾乎只是形式上的推演。

**Narration (EN)**

> Another system the reader may have seen is coordinate triples. Here a three-dimensional vector is an ordered triple of numbers, and both operations are defined algebraically, entry by entry. The vector laws are much easier to prove here, since they are almost formalities.

**動畫**

三個直排的數字方塊：兩個加數與一個和，中間用虛線把同一列連起來，等號放在虛線的缺口上。

## Beat 5 — 三元組其實是一個函數 / a triple is really a function
*配音長度：中文 13.5s ／ 英文 12.1s*

**畫面公式**

```
三元組其實是一個函數   |   a triple is really a function
x  :  { 1 , 2 , 3 } → ℝ        xᵢ  =  x ( i )
```

**旁白（繁中）**

> 如果把三元組看成一個函數，定義域是一到三這三個整數，第 i 項就是函數在 i 的值，那麼這個例子就提示了一個更一般的型別，叫做函數空間。

**Narration (EN)**

> If we think of a triple as a function whose domain is the integers from one to three, with the ith entry the value at i, then this example suggests a much more general type, called a function space.

**動畫**

左邊三個點代表定義域一到三，箭頭連到右邊實數線上的三個值。換一個定義域就變成一般的函數空間。

## Beat 6 — 四條加法公理 / the four axioms for addition
*配音長度：中文 19.2s ／ 英文 16.7s*

**畫面公式**

```
四條加法公理   |   the four axioms for addition
A1 ( α+β )+γ = α+( β+γ )   A2 α+β = β+α   A3 α+0 = α   A4 α+β = 0
```

**旁白（繁中）**

> 現在給定義。設 V 是一個集合，上面給了一個加法與一個數乘。前四條公理只管加法：結合律、交換律、有一個零元素加上去不改變任何向量、而且每個向量都有一個加起來等於零的伙伴。

**Narration (EN)**

> Now the definition. Let V be a set carrying an addition and a multiplication by numbers. The first four axioms concern addition alone: it is associative, it is commutative, there is a zero that changes nothing, and every vector has a partner summing to zero.

**動畫**

A1 到 A4 四個小圖，各自畫出那條律允許你做的動作：換分組、換順序、加零不動、加上反向的回到原點。

## Beat 7 — 四條純量公理 / the four axioms for the scalars
*配音長度：中文 19.5s ／ 英文 18.1s*

**畫面公式**

```
四條純量公理   |   the four axioms for the scalars
S1 ( xy )α = x( yα )   S2 ( x+y )α = xα+yα   S3 x( α+β ) = xα+xβ   S4 1α = α
```

**旁白（繁中）**

> 後四條把數乘接上來：兩個數連續乘等於乘上它們的積、和可以往兩邊分配、乘以一就是原來的向量。從這些公理立刻可以推出零元素唯一、每個向量的反元素唯一，而且零乘任何向量都是零向量。

**Narration (EN)**

> The last four tie in the scalars: multiplying by two numbers in turn is multiplying by their product, sums distribute both ways, and multiplying by one changes nothing. From these, the zero is unique, each negative is unique, and zero times any vector is zero.

**動畫**

S1 是同一方向三段長度遞增的箭頭；S2 與 S3 是整個平行四邊形被等比放大；S4 是原封不動的一支箭頭。

## Beat 8 — A 上的實值函數，逐點相加 / real-valued functions on A, added pointwise
*配音長度：中文 21.6s ／ 英文 19.5s*

**畫面公式**

```
A 上的實值函數，逐點相加   |   real-valued functions on A, added pointwise
ℝᴬ  =  { f : A → ℝ }        ( f + g ) ( a )  =  f ( a ) + g ( a )
```

**旁白（繁中）**

> 書上的標準例子是這樣：取任何一個集合 A，看所有定義在 A 上的實值函數。兩個函數相加就是逐點相加，乘上一個數就是每一點的值都乘上去。A 取一到三就回到三元組，A 取整條實線就是一元實函數的空間。

**Narration (EN)**

> The book's standard example: take any set A and look at all real-valued functions on it. Two are added pointwise, and one is scaled by scaling its value at every point. Taking A to be one to three returns the triples; taking A to be the line gives functions of one real variable.

**動畫**

兩條函數曲線 f 與 g，以及逐點相加得到的粗橘線；在某一點用虛線把三個值疊起來。

## Beat 9 — 子空間：對兩個運算封閉 / a subspace: closed under both operations
*配音長度：中文 20.8s ／ 英文 16.5s*

**畫面公式**

```
子空間：對兩個運算封閉   |   a subspace: closed under both operations
W ⊂ V  ,  W ≠ ∅        α , β ∈ W  ⇒  α + β ∈ W   &   xα ∈ W
```

**旁白（繁中）**

> 接著是子空間。取 V 的一個非空子集，如果它對 V 的兩個運算封閉，那麼它自己就是一個向量空間。理由很短：那些對所有元素都成立的律在小集合裡自動成立，而封閉性保證零元素與反元素也都留在裡面。

**Narration (EN)**

> Now subspaces. Take a nonempty subset of V closed under the two operations; then it is a vector space in its own right. The laws holding for all elements hold automatically in the smaller set, and closure keeps the zero and the negatives inside it.

**動畫**

軸測投影的一片過原點的平面 W，兩支在平面內的向量與它們的和都落在平面上。

## Beat 10 — 連續函數是一個函數空間 / the continuous functions form a function space
*配音長度：中文 19.3s ／ 英文 18.0s*

**畫面公式**

```
連續函數是一個函數空間   |   the continuous functions form a function space
𝒞 [ a , b ]  ⊂  ℝ [ a , b ]        { x : x₁ + x₂ = 0 }  ⊂  ℝ²
```

**旁白（繁中）**

> 所以閉區間上的連續函數，是該區間上所有實值函數的子空間，而這樣的子空間就叫函數空間。書上預設向量空間是實的，但把純量換成複數、甚至換成任何一個體，大部分內容都照樣成立。

**Narration (EN)**

> So the continuous functions on a closed interval form a subspace of all real-valued functions there, and such a subspace is called a function space. The book takes vector spaces to be real, but replacing the scalars by complex numbers, or by any field, leaves most of it standing.

**動畫**

左邊是一條平滑曲線與一條亂跳的灰線（連續函數在所有實值函數裡面）；右邊是平面上 x₁+x₂=0 的那條直線。
