# advcalc E04 — 第 0 章：對偶、布林運算與等價關係

Chapter 0: Duality, the Boolean Operations and Equivalence Relations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 0 章第 10 到 12 節（書頁 15–21）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e04_duality.py`（`AdvCalcE04ZH` / `AdvCalcE04EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[4]` / `FORMULAS_ADVCALC[4]`）
- 配音：`manim_lessons/samples/audio_e04/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.69 分（221 秒）／英文 3.20 分（192 秒）

---

## Beat 0 — 固定 x，剩下的是只依賴 y 的函數 / hold x fixed, a function of y remains
*配音長度：中文 20.0s ／ 英文 17.4s*

**畫面公式**

```
固定 x，剩下的是只依賴 y 的函數   |   hold x fixed, a function of y remains
F : A × B → C        hˣ ( y )  =  F ( x , y )
```

**旁白（繁中）**

> 先講對偶。設 F 是兩個變數的函數。把 x 固定住，剩下的就是一個只依賴 y 的函數。於是每一個 x 都給出一個函數，而這個對應本身又是一個映射，把 A 送到「所有從 B 到 C 的函數」所成的集合。

**Narration (EN)**

> First, duality. Let F be a function of two variables. Hold x fixed and what remains is a function of y alone. So each x yields a function, and that correspondence is itself a mapping, from A into the set of all functions from B to C.

**動畫**

左邊是 A×B 的點陣，其中一欄被打亮；那一欄在右邊變成一排 B 的點，再各自連到 C。固定 x 之後剩下的就是一個從 B 到 C 的函數。

## Beat 1 — 同一個長方形，兩種讀法 / one rectangle, read two ways
*配音長度：中文 18.9s ／ 英文 16.4s*

**畫面公式**

```
同一個長方形，兩種讀法   |   one rectangle, read two ways
φ : A → Cᴮ        θ : B → Cᴬ        F : A × B → C
```

**旁白（繁中）**

> 反過來也成立：給定一個從 A 到那個函數集合的映射，就能把值回填成兩個變數的函數。所以兩變數的函數、從 A 出發的映射、從 B 出發的映射，是同一件事的三種看法，而最外側那兩個互稱對偶。

**Narration (EN)**

> The converse holds too. Given a mapping from A into that set of functions, we can fill the values back in to get a function of two variables. So the two-variable function and the two mappings are three ways of viewing one phenomenon; the outer two are said to be dual.

**動畫**

同一個點陣畫兩次：左邊沿著欄切，右邊沿著列切，中間擺一個大大的 F，強調兩張圖是同一個 F、只是切法不同。

## Beat 2 — 矩陣：列的元組，或行的元組 / a matrix: a tuple of rows, or of columns
*配音長度：中文 20.1s ／ 英文 17.4s*

**畫面公式**

```
矩陣：列的元組，或行的元組   |   a matrix: a tuple of rows, or of columns
t = { tᵢⱼ }        tᵢ  ↦  ⟨ tᵢ₁ , … , tᵢₙ ⟩        tⱼ  ↦  ⟨ t₁ⱼ , … , tₘⱼ ⟩
```

**旁白（繁中）**

> 第一個應用是矩陣。一個 m 乘 n 的矩陣，就是定義在「列指標與行指標的配對」上的函數。固定列指標就得到一整列，於是矩陣可以讀成若干個列所成的元組；對偶地，也可以讀成若干個行所成的元組。

**Narration (EN)**

> The first application is the matrix. An m by n matrix is a function defined on pairs of a row index and a column index. Fix the row index and you get a whole row, so the matrix can be read as a tuple of rows; dually, it can be read as a tuple of columns.

**動畫**

真的畫一個 3×4 的數字矩陣，中間那一列用橘框、第三行用紫框圈起來，右側三行說明「列的元組」與「行的元組」。

## Beat 3 — n 個函數，或一個取值為 n 元組的函數 / n functions, or one n-tuple-valued function
*配音長度：中文 17.4s ／ 英文 17.5s*

**畫面公式**

```
n 個函數，或一個取值為 n 元組的函數   |   n functions, or one n-tuple-valued function
⟨ f₁ , … , fₙ ⟩        a  ↦  ⟨ f₁ ( a ) , … , fₙ ( a ) ⟩  :  A → Bⁿ
```

**旁白（繁中）**

> 同樣的道理，n 個從 A 到 B 的函數所成的元組，可以看成單一個函數，它的值是 B 裡的 n 元組。稍後還有一個更重要的例子：對偶讓有限維向量空間可以被看成它自己的第二共軛空間。

**Narration (EN)**

> In the same vein, an n-tuple of functions from A to B can be regarded as a single function whose values are n-tuples in B. A more important case comes later: duality is what lets a finite-dimensional vector space be regarded as its own second conjugate space.

**動畫**

左邊一個點 a 射出三條箭頭到 f₁(a)、f₂(a)、f₃(a)；右邊同一個 a 只射出一條箭頭，指向一個 ⟨·,·,·⟩ 的方塊。

## Beat 4 — 線是點的集合，點是線的集合 / a line is a set of points, a point a set of lines
*配音長度：中文 24.3s ／ 英文 18.0s*

**畫面公式**

```
線是點的集合，點是線的集合   |   a line is a set of points, a point a set of lines
F ( p , l ) ∈ { 0 , 1 }        l  ↦  { p : F = 1 }        p  ↦  { l : F = 1 }
```

**旁白（繁中）**

> 幾何裡也有。把點與線看成兩種原始對象，關聯函數在點落在線上時取一、否則取零。固定一條線，就得到線上所有點所成的集合；固定一個點，就得到通過它的所有線。線是點的集合，點也是線的集合，這是投影幾何的基本觀點。

**Narration (EN)**

> Geometry has it too. Take points and lines as two kinds of primitive object, with an incidence function that is one when the point lies on the line. Fix a line and you get the set of points on it; fix a point, the lines through it. This duality is basic to projective geometry.

**動畫**

三個點、三條線的關聯圖，右邊配一張 0/1 的關聯表。橫著讀是線上的點，直著讀是過該點的線。

## Beat 5 — 點記法方便，但讀不回去 / the dot is handy, but cannot be read back
*配音長度：中文 20.5s ／ 英文 17.3s*

**畫面公式**

```
點記法方便，但讀不回去   |   the dot is handy, but cannot be read back
hˣ  =  F ( x , · )        f  =  f ( · )        Dξ F ( · )
```

**旁白（繁中）**

> 固定變數時常用一個點記號：在變動的那個位置擺一個點。這個記法很方便，但有個缺陷——沒辦法一邊代入一邊保留意思，因為看到代入後的值，讀不回原來是哪個函數。書上後面的方向導數就會用到它。

**Narration (EN)**

> When a variable is held fixed there is a convenient device: put a dot in the position of the varying one. The notation is useful but flawed, since we cannot indicate substitution without losing meaning; from the value we cannot read back which function was evaluated.

**動畫**

F(x,·) 經箭頭代入變成 F(x,b)，再有一條紅色箭頭想倒推回去，中間放一個紅色問號——值讀不回原來是哪個函數。

## Beat 6 — 聯集與交集 / union and intersection
*配音長度：中文 22.2s ／ 英文 17.6s*

**畫面公式**

```
聯集與交集   |   union and intersection
⋃ ℱ  =  { x : ( ∃A ∈ ℱ ) ( x ∈ A ) }        x ∈ ⋂ᵢ Aᵢ  ⇔  ( ∀i ) ( x ∈ Aᵢ )
```

**旁白（繁中）**

> 接著是布林運算。固定一個定義域，取它的一族子集。這一族的聯集，是至少屬於其中一個集合的所有元素；交集則是落在每一個集合裡的元素。加上指標之後寫起來更方便，書上說這在技術上與心理上都有好處。

**Narration (EN)**

> Now the Boolean operations. Fix a domain and take a family of its subsets. The union of the family is the set of elements belonging to at least one of them, and the intersection is the set of those lying in every one. Indexing the family makes all of this easier to write.

**動畫**

兩個並排的方框 S：左邊兩個橢圓都填色（聯集），右邊只有中間的透鏡填紅（交集）。

## Beat 7 — 不是每個都在　＝　有時候不在 / not always in  =  sometimes not in
*配音長度：中文 18.5s ／ 英文 16.5s*

**畫面公式**

```
不是每個都在　＝　有時候不在   |   not always in  =  sometimes not in
A′ = { x ∈ S : x ∉ A }        ( ⋂ᵢ Aᵢ )′  =  ⋃ᵢ ( Aᵢ′ )
```

**旁白（繁中）**

> 補集是定義域裡不屬於它的那部分。De Morgan 律說，交集的補集等於補集的聯集——這只是量詞否定規則的直接結果：不是每個都在，就等於有時候不在。各種分配律同樣來自量詞的性質。

**Narration (EN)**

> The complement of a subset is what is left of the domain. De Morgan's law says the complement of an intersection is the union of the complements, and this is an immediate consequence of the rule for negating quantifiers: not always in means the same as sometimes not in.

**動畫**

兩個方框都填色。左邊用布林差挖掉真正的交集透鏡；右邊疊上兩個「各自挖掉一個橢圓」的補集。兩邊沒被蓋到的都只剩中間那一塊。

## Beat 8 — 原像保持三種運算 / the preimage preserves all three
*配音長度：中文 17.0s ／ 英文 17.0s*

**畫面公式**

```
原像保持三種運算   |   the preimage preserves all three
f ⁻¹ [ ⋃ᵢ Bᵢ ] = ⋃ᵢ f ⁻¹ [ Bᵢ ]        f ⁻¹ [ B′ ] = ( f ⁻¹ [ B ] )′
```

**旁白（繁中）**

> 還有一組重要的等式：函數的原像保持聯集、保持交集，也保持補集。注意只有第一條對一般的關係仍然成立，另外兩條會壞掉，因為兩個量詞交換次序之後意思就變了。

**Narration (EN)**

> There are also identities for preimages: a preimage preserves unions, intersections and complements. Only the first survives when the function is replaced by a general relation; the other two fail, because swapping the order of two quantifiers changes the meaning.

**動畫**

A、B 兩個橢圓，B 裡有兩塊子集，A 裡是它們各自的原像，箭頭一一對應。

## Beat 9 — 纖維化與投影 / a fibering and its projection
*配音長度：中文 22.7s ／ 英文 18.4s*

**畫面公式**

```
纖維化與投影   |   a fibering and its projection
⋃ ℱ = A  ,  Aᵢ ∩ Aⱼ = ∅        π : A → ℱ  ,  x ↦ x̄
```

**旁白（繁中）**

> 最後是分割。把一個集合切成互不相交的一族子集，聯集正好是原集合，這就是纖維化，每一塊叫一根纖維。把一個點送到它所在的那根纖維，這個映射叫投影。任何函數都自動把定義域纖維化成它取值不變的那些集合。

**Narration (EN)**

> Finally partitions. Cut a set into a disjoint family of subsets whose union is the whole set: that is a fibering, and each piece is a fiber. Sending a point to its own fiber is the projection. Any function automatically fibers its domain into the sets where it is constant.

**動畫**

一個長方形被切成五條互不相交的橫條，每條各一種顏色，箭頭指到右邊代表 ℱ 的五個點。

## Beat 10 — 每個等價關係都來自某個纖維化 / every equivalence relation comes from a fibering
*配音長度：中文 20.0s ／ 英文 18.7s*

**畫面公式**

```
每個等價關係都來自某個纖維化   |   every equivalence relation comes from a fibering
x ∼ x    x ∼ y ⇒ y ∼ x    x ∼ y & y ∼ z ⇒ x ∼ z        g  =  ḡ ∘ π
```

**旁白（繁中）**

> 等價關係是自反、對稱又遞移的關係。每個纖維化都給出一個等價關係，而這一節的定理是反過來的那半：每一個等價關係，都恰好是某個纖維化的等價關係。有理數與模 p 的整數，都是這樣造出來的。

**Narration (EN)**

> An equivalence relation is reflexive, symmetric and transitive. Every fibering gives one, and the theorem of this section is the converse: every equivalence relation is the equivalence relation of a fibering. The rationals and the integers modulo p are both built this way.

**動畫**

ℤ×(ℤ−{0}) 的整數格點，三條過原點的直線各用一種顏色打亮。同一條線上的點就是同一個有理數。
