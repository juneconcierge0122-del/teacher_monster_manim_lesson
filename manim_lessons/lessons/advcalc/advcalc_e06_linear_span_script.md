# advcalc E06 — 第 1 章：線性組合與線性擴張

Chapter 1: Linear Combinations and Linear Span

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 1 節後半（書頁 26–29）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e06_linear_span.py`（`AdvCalcE06ZH` / `AdvCalcE06EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[6]` / `FORMULAS_ADVCALC[6]`）
- 配音：`manim_lessons/samples/audio_e06/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.44 分（206 秒）／英文 2.87 分（172 秒）

---

## Beat 0 — 十二種算法，同一個終點 / twelve ways, one endpoint
*配音長度：中文 16.4s ／ 英文 14.2s*

**畫面公式**

```
十二種算法，同一個終點   |   twelve ways, one endpoint
( α₁ + α₂ ) + α₃  =  α₁ + ( α₂ + α₃ )  =  α₂ + ( α₃ + α₁ )  =  …
```

**旁白（繁中）**

> 因為加法有交換律與結合律，一個有限集合的向量和，跟你用什麼順序、怎麼分組去加完全無關。書上舉的例子是三個向量，一共有十二種算法，結果都一樣。

**Narration (EN)**

> Because addition is commutative and associative, the sum of a finite set of vectors is the same for all ways of adding them. The book's example is three vectors, which can be summed in twelve ways, all giving the same result.

**動畫**

三個向量、三種相加順序，畫成三條稍微錯開的折線，全部收在同一個終點；旁邊一個大大的 12。

## Beat 1 — 只要寫出指標集就沒有歧義 / the index set alone makes it unambiguous
*配音長度：中文 20.8s ／ 英文 13.3s*

**畫面公式**

```
只要寫出指標集就沒有歧義   |   the index set alone makes it unambiguous
Σ αᵢ    ( i ∈ I )
```

**旁白（繁中）**

> 既然如此，只要把指標集合寫出來，和就沒有歧義了。所以可以寫成對 I 裡的每個 i 把對應的向量加起來，完全不必說明是怎麼加的。一般來說，任何一個有限的、加了指標的向量集合，都唯一決定一個和向量。

**Narration (EN)**

> So writing down the index set makes the sum unambiguous: we can write the sum over i in I without saying how we got it. In general any finite indexed set of vectors determines a unique sum vector.

**動畫**

一個橢圓裡散著六支加了指標的向量，彼此沒有次序，箭頭指到右邊一個 Σ 方塊。

## Beat 2 — 有次序的指標，與沒有次序的 / ordered index sets, and unordered ones
*配音長度：中文 20.5s ／ 英文 17.8s*

**畫面公式**

```
有次序的指標，與沒有次序的   |   ordered index sets, and unordered ones
I = { 1 , … , n }        Σ cᵢⱼ sⁱ tʲ    ( i + j ≤ 5 )
```

**旁白（繁中）**

> 指標集常常就是一到 n 這一段整數，這時向量排成一個 n 元組，沒特別交代就照自然順序相加。不過經常會用到沒有次序的指標集：兩個變數、次數不超過五的一般多項式，它的單項式所成的集合就沒有自然次序。

**Narration (EN)**

> The index set is often a block of integers from one to n, and then the vectors form an n-tuple, added in their natural order unless directed otherwise. But unordered index sets come up often: the monomials of a general polynomial in two variables have no natural order.

**動畫**

左邊是一到五的方塊照順序排；右邊是 i+j ≤ 5 的單項式所排成的三角形點陣，完全沒有自然次序。

## Beat 3 — 兩種分法交出四小塊 / two splittings intersect into four pieces
*配音長度：中文 21.6s ／ 英文 16.5s*

**畫面公式**

```
兩種分法交出四小塊   |   two splittings intersect into four pieces
Lⱼₖ  =  Jⱼ ∩ Kₖ        ξⱼₖ  =  Σ αᵢ    ( i ∈ Lⱼₖ )
```

**旁白（繁中）**

> 書上把那個形式證明標了星號，只給有興趣的讀者。做法是對元素個數做歸納：兩種算法各自的最後一次加法，把指標集分成兩塊；取兩組分法的交集得到四小塊，再用歸納假設把四塊的和重新結合，兩邊就相等了。

**Narration (EN)**

> The book stars the formal proof and gives it only for the interested reader. It is an induction on the number of elements: the last addition in each computation splits the index set in two, intersecting the two splittings gives four pieces, and induction regroups them.

**動畫**

一個長方形被兩條線各切一次，交出 L₁₁ 到 L₂₂ 四小塊，上緣標 J₁ / J₂、左緣標 K₁ / K₂。

## Beat 4 — 線性組合 / a linear combination
*配音長度：中文 14.4s ／ 英文 11.7s*

**畫面公式**

```
線性組合   |   a linear combination
β  =  Σ xᵢ αᵢ    ,    αᵢ ∈ A
```

**旁白（繁中）**

> 有了和，就可以定義線性組合。一個向量叫做集合 A 的線性組合，如果它是有限個「純量乘上 A 裡的向量」加起來的結果，而那些純量是任意的。

**Narration (EN)**

> With sums in hand we can define a linear combination. A vector is a linear combination of a set A if it is a finite sum of scalars times vectors of A, where the scalars are arbitrary.

**動畫**

兩支向量各自乘上自己的係數之後首尾相接，粗橘線就是它們的線性組合。

## Beat 5 — 係數就是那個元組 / the coefficients are the tuple
*配音長度：中文 20.3s ／ 英文 18.1s*

**畫面公式**

```
係數就是那個元組   |   the coefficients are the tuple
Σ cᵢ tⁱ        3 · sin t + 0 · cos t + ( −1 ) · eᵗ    →    ⟨ 3 , 0 , −1 ⟩
```

**旁白（繁中）**

> 舉例來說，如果 A 是所有次方所成的集合，那麼線性組合就正好是多項式函數。如果 A 是正弦、餘弦與指數這三個函數，照這個順序排，那麼三倍正弦減掉指數，對應的係數三元組就是三、零、負一。

**Narration (EN)**

> For example, if A is the set of all powers, the linear combinations are exactly the polynomial functions. If A is sine, cosine and the exponential in that listed order, then three sine minus the exponential has coefficient triple three, zero, minus one.

**動畫**

正弦、餘弦、指數三條曲線，加上三倍正弦減掉指數的粗橘線；上方是對應顏色的圖例。

## Beat 6 — 兩個向量的所有線性組合 / all linear combinations of two vectors
*配音長度：中文 19.3s ／ 英文 16.6s*

**畫面公式**

```
兩個向量的所有線性組合   |   all linear combinations of two vectors
L  =  { ⟨ s , s + t , s − t ⟩  :  ⟨ s , t ⟩ ∈ ℝ² }
```

**旁白（繁中）**

> 再看一個具體的。取三維空間裡的兩個向量，它們所有的線性組合所成的集合，一眼就看得出對加法與數乘封閉，所以是一個子空間；而任何含有那兩個向量的子空間，一定也含有它們所有的線性組合。

**Narration (EN)**

> Here is a concrete one. Take two vectors in three-space. The set of all their linear combinations is plainly closed under addition and scaling, so it is a subspace; and any subspace containing the two vectors must contain all of their linear combinations.

**動畫**

軸測投影的一片過原點的平面 L，兩支生成向量與三個落在平面上的線性組合（座標都核對過在平面範圍內）。

## Beat 7 — 包含 A 的最小子空間 / the smallest subspace including A
*配音長度：中文 12.8s ／ 英文 12.1s*

**畫面公式**

```
包含 A 的最小子空間   |   the smallest subspace including A
L ( A )  ⊂  V        A ⊂ M  ⇒  L ( A ) ⊂ M
```

**旁白（繁中）**

> 把這件事寫成定理：如果 A 是向量空間的一個非空子集，那麼 A 的所有線性組合所成的集合是一個子空間，而且是包含 A 的最小的那個子空間。

**Narration (EN)**

> As a theorem: if A is a nonempty subset of a vector space, then the set of all linear combinations of vectors of A is a subspace, and it is the smallest subspace which includes A.

**動畫**

三層巢狀的橢圓：最內是 A 的點，中間是 L(A)，最外是任何含 A 的子空間 M。

## Beat 8 — 相加、數乘，都還在裡面 / closed under adding and under scaling
*配音長度：中文 21.9s ／ 英文 19.1s*

**畫面公式**

```
相加、數乘，都還在裡面   |   closed under adding and under scaling
( Σ xᵢαᵢ ) + ( Σ yᵢαᵢ ) = Σ ( xᵢ + yᵢ ) αᵢ        c ( Σ xᵢαᵢ ) = Σ ( cxᵢ ) αᵢ
```

**旁白（繁中）**

> 證明分兩半。封閉性：兩個線性組合相加，按指標合併同類項就還是線性組合；乘上一個純量，用分配律與歸納法也還是。至於最小：這個集合含有 A 的每一個元素，而任何含有 A 的子空間都得含有每一個線性組合。

**Narration (EN)**

> The proof has two halves. Closure: adding two linear combinations and collecting terms gives another, and scaling gives another by distributivity and induction. Smallest: the set contains each element of A, and any subspace including A must contain every linear combination.

**動畫**

兩排係數方塊 x 與 y，虛線往下合併成 x+y 的一排，示範按指標合併同類項。

## Beat 9 — A 無限也不影響 / an infinite A changes nothing
*配音長度：中文 15.2s ／ 英文 14.9s*

**畫面公式**

```
A 無限也不影響   |   an infinite A changes nothing
( Σ₁ⁿ xᵢαᵢ ) + ( Σ₁ᵐ yⱼβⱼ )  =  Σ₁ⁿ⁺ᵐ xᵢαᵢ
```

**旁白（繁中）**

> 如果 A 是無限集合，就沒辦法一次列完，但論證照樣走得通：兩個線性組合各自都是有限和，加起來仍然是有限個純量乘上 A 裡的向量，所以還是線性組合。

**Narration (EN)**

> If A is infinite we cannot list it in one go, but the argument still runs: two linear combinations are each finite sums, so their sum is again a finite sum of scalars times vectors of A, hence again a linear combination.

**動畫**

一個橢圓裡幾十個點代表無限的 A，其中兩組有限的點被打亮，說明兩個有限和加起來還是有限和。

## Beat 10 — 生成、有限維 / spanning, and finite dimension
*配音長度：中文 23.0s ／ 英文 17.9s*

**畫面公式**

```
生成、有限維   |   spanning, and finite dimension
δ ʲ  =  ⟨ 0 , … , 1 , … , 0 ⟩        x  =  Σ₁ⁿ xᵢ δ ⁱ
```

**旁白（繁中）**

> 這個子空間叫做 A 的線性擴張。如果它就是整個空間，就說 A 生成這個空間，而有有限生成集的空間叫有限維。n 維座標空間，由那些只有一個位置是一、其他都是零的向量生成。閉區間上的連續函數則沒有有限生成集。

**Narration (EN)**

> This subspace is the linear span of A. If it is the whole space, A spans the space, and a space with a finite spanning set is finite-dimensional. Coordinate n-space is spanned by the vectors with a single one and zeros elsewhere. Continuous functions on an interval are not.

**動畫**

左邊 δ¹、δ² 與它們張成的一個向量；右邊是 1, t, t², t³, t⁴ 一直往下的一列，配一支往下的箭頭。
