# advcalc E13 — 第 1 章：仿射子空間與商空間

Chapter 1: Affine Subspaces and Quotient Spaces

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 4 節（書頁 52–56）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e13_quotient.py`（`AdvCalcE13ZH` / `AdvCalcE13EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[13]` / `FORMULAS_ADVCALC[13]`）
- 配音：`manim_lessons/samples/audio_e13/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.12 分（187 秒）／英文 2.78 分（167 秒）

---

## Beat 0 — 向量空間裡的「平面」 / the planes in a vector space
*配音長度：中文 18.0s ／ 英文 16.7s*

**畫面公式**

```
向量空間裡的「平面」   |   the planes in a vector space
N ⊂ V          N + α
```

**旁白（繁中）**

> 這一節先看向量空間裡的「平面」，問它們被平移、彼此相交、被線性映射送過去之後會怎麼樣。然後把注意力縮到某個固定子空間的所有平移，會發現這一堆東西自己就是一個向量空間。

**Narration (EN)**

> This section looks at the planes in a vector space and asks what happens to them under translation, intersection with each other, and images under linear maps. Then it narrows to the translates of one fixed subspace and finds that set is itself a vector space.

**動畫**

三條平行線，過原點那一條打亮成子空間，其餘兩條是一般的「平面」。

## Beat 1 — 子空間平移過去，就是陪集 / a subspace shifted: a coset
*配音長度：中文 18.6s ／ 英文 16.3s*

**畫面公式**

```
子空間平移過去，就是陪集   |   a subspace shifted: a coset
N + α  =  { ξ + α  :  ξ ∈ N }        ᾱ  =  N + α
```

**旁白（繁中）**

> 定義是這樣：N 是子空間、α 是任意一個向量，那麼 N 的每個元素都加上 α 所成的集合，叫做含 α 的陪集，或者說過 α 且平行於 N 的仿射子空間。第二節說的平面，指的就是這種東西。

**Narration (EN)**

> The definition: for a subspace N and any vector, the set of everything in N shifted by that vector is called the coset containing it, or the affine subspace through it parallel to N. These are the general objects section two wanted to call planes.

**動畫**

過原點的 N 與它平移之後的那一條，中間一支箭頭是位移向量 α。

## Beat 2 — 要嘛相同，要嘛不交 / identical or disjoint, never in between
*配音長度：中文 21.0s ／ 英文 18.3s*

**畫面公式**

```
要嘛相同，要嘛不交   |   identical or disjoint, never in between
γ ∈ ᾱ  ⇒  γ̄ = ᾱ        ᾱ = β̄   or   ᾱ ∩ β̄ = ∅        α ∼ β ⇔ α − β ∈ N
```

**旁白（繁中）**

> 第一個性質：如果 γ 落在 α 的陪集裡，那麼 γ 的陪集跟 α 的陪集是同一個。第二個：任兩個陪集要嘛完全相同、要嘛不相交。這正是第零章那個等價關係的特例——兩個向量等價，若且唯若它們的差落在 N 裡。

**Narration (EN)**

> First property: if one vector lies in the coset of another, the two cosets are the same. Second: any two cosets are either identical or disjoint. This is the equivalence relation of chapter zero in a special case, with two vectors equivalent when their difference lies in N.

**動畫**

三條平行線上放 α、γ、β 三個點：α 與 γ 在同一條上，β 在另一條，兩條完全不交。

## Beat 3 — 交集與集合和 / intersections and set sums
*配音長度：中文 13.7s ／ 英文 12.5s*

**畫面公式**

```
交集與集合和   |   intersections and set sums
⋂ᵢ Aᵢ  :  ∅  or  affine        A + B  :  affine
```

**旁白（繁中）**

> 再來幾條。任意多個仿射子空間的交集，要嘛是空的、要嘛還是仿射子空間。兩個仿射子空間的集合和，還是仿射子空間。

**Narration (EN)**

> More of them: the intersection of any family of affine subspaces is either empty or an affine subspace, and the set sum of two affine subspaces is again an affine subspace.

**動畫**

左邊兩條線交於一點，右邊兩條線的集合和是一個平行四邊形。

## Beat 4 — 被線性映射送過去 / carried by a linear map
*配音長度：中文 10.8s ／ 英文 10.0s*

**畫面公式**

```
被線性映射送過去   |   carried by a linear map
T [ A ]  :  affine        T ⁻¹ [ B ]  :  ∅  or  affine
```

**旁白（繁中）**

> 線性映射把仿射子空間送到仿射子空間；反過來，仿射子空間的原像要嘛是空的、要嘛還是仿射子空間。

**Narration (EN)**

> A linear map carries an affine subspace to an affine subspace; and the preimage of an affine subspace is either empty or an affine subspace.

**動畫**

左右兩個橢圓 V 與 W，各自裡面有一條線段，中間是 T 的箭頭。

## Beat 5 — 平移不是線性的 / translation is not linear
*配音長度：中文 16.3s ／ 英文 15.3s*

**畫面公式**

```
平移不是線性的   |   translation is not linear
Sα ( ξ ) = ξ + α        Sα ( 0 ) = α  ≠  0        ξ ↦ T ( ξ ) + β
```

**旁白（繁中）**

> 平移本身不是線性的——它把零送到位移向量，而不是送到零。但它確實把仿射子空間送到仿射子空間。而「線性映射後面接一個平移」，就叫做仿射變換。

**Narration (EN)**

> Translation itself is not linear, since it carries zero to the shift vector rather than to zero. But it does carry affine subspaces to affine subspaces. A linear map followed by a translation is called an affine transformation.

**動畫**

原點與 α 之間一支箭頭，旁邊寫出零沒有被送到零，所以平移不是線性的。

## Beat 6 — 一族平行的直線 / a family of parallel lines
*配音長度：中文 14.7s ／ 英文 11.2s*

**畫面公式**

```
一族平行的直線   |   a family of parallel lines
N  =  { t a }        W  =  { N + α  :  α ∈ V }
```

**旁白（繁中）**

> 現在固定一個子空間，看它所有平移所成的集合。書上的例子是：如果它是三維空間裡過原點的一條直線，那麼這個集合就是所有平行於它的直線。

**Narration (EN)**

> Now fix a subspace and look at the set of all its translates. The book's example: if it is a line through the origin in three-space, that set is all the lines parallel to it.

**動畫**

五條平行線，過原點那條打亮——這一族就是某個子空間的所有平移。

## Beat 7 — 兩條相加，還是這一族裡的一條 / two of them add to a third
*配音長度：中文 18.2s ／ 英文 17.4s*

**畫面公式**

```
兩條相加，還是這一族裡的一條   |   two of them add to a third
ᾱ  +ₛ  β̄   =   α + β  ‾
```

**旁白（繁中）**

> 值得注意的是，這些平行直線自己構成一個向量空間：任兩條的集合和還是這一族裡的一條直線，非零倍數也是。這些平移把整個空間纖維化，而纖維所成的集合，自然就是一個向量空間。

**Narration (EN)**

> What is worth noticing is that these parallel lines form a vector space in their own right: the set sum of any two is another line in the family, and so is a nonzero multiple. The translates fiber the space, and the set of fibers is naturally a vector space.

**動畫**

從兩條線上各取一個點相加，落點用虛線標出，正好落在這一族的第三條線上（層數有 assert 過）。

## Beat 8 — 把向量送到它所在的那條 / sending a vector to its own line
*配音長度：中文 15.3s ／ 英文 16.1s*

**畫面公式**

```
把向量送到它所在的那條   |   sending a vector to its own line
π ( α + β ) = π ( α ) + π ( β )        π ( t α ) = t π ( α )        0̄ = N
```

**旁白（繁中）**

> 加法定義成集合和，數乘定義成集合的倍數，只有乘以零那一種要另外規定成 N 本身。於是「把向量送到它的陪集」這個自然映射，加法與數乘都保持。

**Narration (EN)**

> Addition is set addition and scalar multiplication is the set product, with only multiplication by zero needing a separate stipulation, namely the subspace itself. The natural map sending a vector to its coset then preserves both operations.

**動畫**

左邊五條平行線各一種顏色，箭頭指到右邊代表商空間的五個點。

## Beat 9 — 有滿射就夠了 / a surjection is enough
*配音長度：中文 19.7s ／ 英文 16.7s*

**畫面公式**

```
有滿射就夠了   |   a surjection is enough
T : V → W   onto ,  T ( sα + tβ ) = s T α + t T β   ⇒   W   vector space
```

**旁白（繁中）**

> 有一個定理省下逐條檢查的工夫：如果一個集合上有兩個像向量運算的運算，而且從某個向量空間有一個保持運算的滿射過去，那麼它就是向量空間。用它就知道商空間是向量空間，投影是滿的線性映射。

**Narration (EN)**

> A theorem saves the work of checking every law: if a set carries two vectorlike operations and some vector space maps onto it preserving them, it is a vector space. So the quotient space is a vector space and the projection is a surjective linear map.

**動畫**

左邊一個向量空間、右邊一個帶兩個運算的集合，中間一支保持運算的滿射箭頭。

## Beat 10 — 穿過商空間分解 / factoring through the quotient
*配音長度：中文 20.7s ／ 英文 16.6s*

**畫面公式**

```
穿過商空間分解   |   factoring through the quotient
M ⊂ N ( T )   ⇒   T = S ∘ π   ,   S ∈ Hom ( V / M , W )
```

**旁白（繁中）**

> 這一節的重點定理是：如果一個線性映射的零空間包含某個子空間，那麼它可以唯一地分解成「先投影到商空間，再接一個線性映射」。另外，如果某個子空間被 T 送進自己，那麼商空間上就有唯一一個與 T 相容的映射。

**Narration (EN)**

> The main theorem here: if the null space of a linear map includes a subspace, the map factors uniquely as the projection onto the quotient followed by a linear map. And if a subspace is carried into itself, there is a unique matching map on the quotient.

**動畫**

V、W、V/M 三個方框組成的三角形：T 走直路，π 接 S 走繞路，兩條路一樣。
