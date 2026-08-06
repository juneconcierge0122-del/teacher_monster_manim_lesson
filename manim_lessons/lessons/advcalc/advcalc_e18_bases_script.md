# advcalc E18 — 第 2 章：基底與座標同構

Chapter 2: Bases and the Coordinate Isomorphism

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 1 節（書頁 71–74）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e18_bases.py`（`AdvCalcE18ZH` / `AdvCalcE18EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[18]` / `FORMULAS_ADVCALC[18]`）
- 配音：`manim_lessons/samples/audio_e18/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.28 分（197 秒）／英文 2.95 分（177 秒）

---

## Beat 0 — 第 2 章：有限維空間 / chapter 2: the finite-dimensional spaces
*配音長度：中文 16.1s ／ 英文 16.5s*

**畫面公式**

```
第 2 章：有限維空間   |   chapter 2: the finite-dimensional spaces
dim V  =  n
```

**旁白（繁中）**

> 第二章把注意力放在有限維的空間。核心的事情是：可以給每一個有限維空間指定一個整數，叫做維數；它符合我們對維度的直覺，而且是後面深入探討的主要工具。

**Narration (EN)**

> Chapter two turns attention to finite-dimensional spaces. The central thing is that each such space can be assigned a unique integer, its dimension, which satisfies our intuitive requirements about dimensionality and becomes the principal tool for what follows.

**動畫**

大橢圓 V 裡套一個實心的小橢圓，標「有限維」。整章的目標：給每個這樣的空間配一個整數。

## Beat 1 — 搬到座標空間，就取得矩陣 / transferred to coordinates, it becomes a matrix
*配音長度：中文 19.2s ／ 英文 16.2s*

**畫面公式**

```
搬到座標空間，就取得矩陣   |   transferred to coordinates, it becomes a matrix
V  ≅  ℝⁿ        T  ↦  t
```

**旁白（繁中）**

> 有限維空間可以刻畫成「與某個座標空間同構」。而這樣一個同構，讓一個算子被搬到座標空間上，在那裡它取得一個矩陣。所以有限維空間上的線性變換理論，完全被矩陣的理論映照出來。

**Narration (EN)**

> A finite-dimensional space can be characterized as one isomorphic to some coordinate space. Such an isomorphism transfers an operator there, where it acquires a matrix. So linear transformations on such spaces are mirrored completely by matrices.

**動畫**

V ≅ ℝⁿ 的箭頭，再往右接到一個矩陣框：算子被搬到座標空間之後取得矩陣。

## Beat 2 — 嵌射是獨立，同構是基底 / injective is independent, iso is a basis
*配音長度：中文 20.7s ／ 英文 17.6s*

**畫面公式**

```
嵌射是獨立，同構是基底   |   injective is independent, iso is a basis
L α : x ↦ Σ xᵢ αᵢ        inj : independent        iso : basis
```

**旁白（繁中）**

> 回到第一章那個線性組合映射。定義：一個有限的、加了指標的向量集合叫做獨立，如果那個映射是嵌射；而如果那個映射是同構，就叫做 V 的一個基底。指標集是一到 n 的時候，就叫有序基底，或者框架。

**Narration (EN)**

> Back to the linear combination map of chapter one. The definition: a finite indexed set of vectors is independent if that map is injective, and is a basis for V if that map is an isomorphism. When the index set is one to n it is called an ordered basis, or a frame.

**動畫**

兩個並排的框，同一個線性組合映射 Lα 配兩個條件（嵌射／同構），對到兩個名字（獨立／基底）。

## Beat 3 — 每個向量唯一一組係數 / one set of coefficients per vector
*配音長度：中文 13.0s ／ 英文 12.5s*

**畫面公式**

```
每個向量唯一一組係數   |   one set of coefficients per vector
ξ  =  Σ xᵢ αᵢ   ,   x   unique
```

**旁白（繁中）**

> 所以是基底，若且唯若 V 裡每一個向量都有唯一一組係數。係數存在，是因為這些向量生成 V；係數唯一，是因為它們獨立。

**Narration (EN)**

> So it is a basis exactly when every vector of V has a unique set of coefficients. The coefficients exist because the vectors span V, and they are unique because the vectors are independent.

**動畫**

平面上一個目標向量，用兩個基底向量分解：先走 u 再走 v，虛線補完平行四邊形。存在是因為生成，唯一是因為獨立。

## Beat 4 — 驗一個具體的例子 / checking a concrete one
*配音長度：中文 16.0s ／ 英文 15.8s*

**畫面公式**

```
驗一個具體的例子   |   checking a concrete one
b ¹ = ⟨ 2 , 1 ⟩  ,  b ² = ⟨ 1 , −3 ⟩        y = ⟨ 2x₁+x₂ , x₁−3x₂ ⟩
```

**旁白（繁中）**

> 書上舉了個例子：平面上兩個具體的向量。要驗它們是基底，就是驗那條向量方程對每個目標都有唯一解——拆成兩條純量方程，用中學的消去法解出來就行。

**Narration (EN)**

> The book gives an example: two concrete vectors in the plane. Checking that they form a basis is checking that the vector equation has a unique solution for every target, which splits into two scalar equations and yields to secondary school elimination.

**動畫**

書上那個具體例子：兩個平面向量畫成箭頭，並把 det 算出來顯示在畫面上。`assert abs(det) > 1e-9` 釘住它們真的是基底——這一拍在宣稱一件可算的事，就要算給它看。

## Beat 5 — 比較常見的那個定義 / the more usual definition
*配音長度：中文 16.7s ／ 英文 15.5s*

**畫面公式**

```
比較常見的那個定義   |   the more usual definition
Σ xᵢ αᵢ = 0   ⇒   xᵢ = 0   ( ∀i )
```

**旁白（繁中）**

> 比較常見的那個獨立性定義，在這裡其實是個推論：這組向量獨立，若且唯若係數乘向量加起來等於零時，每個係數都必須是零。因為那正好是說零空間只有零向量。

**Narration (EN)**

> The more usual definition of independence is here a corollary: the vectors are independent exactly when coefficients times vectors summing to zero forces every coefficient to be zero. That says precisely that the null space contains only zero.

**動畫**

上排是 x₁+x₂+…=0 的方框列，往下一排全部變成 0：獨立的常見定義其實是推論。

## Beat 6 — 基底同構與座標同構 / the basis and coordinate isomorphisms
*配音長度：中文 17.2s ／ 英文 17.5s*

**畫面公式**

```
基底同構與座標同構   |   the basis and coordinate isomorphisms
L α  :  basis iso        L α ⁻¹  :  coordinate iso        ξ ↦ xⱼ
```

**旁白（繁中）**

> 有序基底給每個向量一組唯一的係數，叫做它的座標元組。線性組合映射叫基底同構，它的反函數叫座標同構。而「取第 j 個座標」是一個線性泛函，叫座標泛函。

**Narration (EN)**

> An ordered basis gives each vector a unique set of coefficients, called its coordinate tuple. The combination map is called the basis isomorphism and its inverse the coordinate isomorphism. Taking the jth coordinate is a linear functional, the jth coordinate functional.

**動畫**

ℝⁿ 與 V 之間兩條反向箭頭（Lα 與 Lα⁻¹），右邊再接一支箭頭取第 j 個座標。基底同構、座標同構、座標泛函三個名字一次到位。

## Beat 7 — 兩件小事 / two small remarks
*配音長度：中文 15.1s ／ 英文 14.4s*

**畫面公式**

```
兩件小事   |   two small remarks
αₖ = αₗ  ⇒  dependent        J ⊂ I ,  { αᵢ }ᵢ ind .  ⇒  { αᵢ }ⱼ ind .
```

**旁白（繁中）**

> 現在要證每個有限維空間都有基底。先注意兩件小事：一個加了指標的集合要獨立，指標本身必須是嵌射的；另外，獨立集合的子集也還是獨立的。

**Narration (EN)**

> Now to show every finite-dimensional space has a basis. Two small remarks first: an indexed set can be independent only if the indexing is injective; and any subset of an independent set is independent.

**動畫**

上半：一排方框裡有兩個標籤重複，用 WARN 斜線劃掉——指標重複就一定不獨立。下半：從一組獨立集合裡框出一個子集，仍然獨立。

## Beat 8 — 擴張外面的向量，加進去還獨立 / a vector outside the span keeps it independent
*配音長度：中文 21.0s ／ 英文 16.5s*

**畫面公式**

```
擴張外面的向量，加進去還獨立   |   a vector outside the span keeps it independent
β  ∉  L ( B )    ⇒    B ∪ { β }   independent
```

**旁白（繁中）**

> 引理：如果 B 是獨立的、而某個向量不在 B 的線性擴張裡，那麼把它加進 B 之後還是獨立的。證明是：若有非零組合等於零，那個新向量的係數不能是零，否則會跟 B 的獨立性矛盾；於是可以解出它落在擴張裡，矛盾。

**Narration (EN)**

> The lemma: if a set is independent and some vector is not in its span, adjoining that vector leaves it independent. For if a nontrivial combination vanished, the new vector's coefficient could not be zero, and then it could be solved for, putting it in the span.

**動畫**

一條線 L(B) 與一個離開它的向量 β。把 β 加進去仍然獨立；若不然，β 的係數不能是零，就解得出 β 落在線上——矛盾。

## Beat 9 — 留下讓擴張變大的那些 / keep the ones that enlarge the span
*配音長度：中文 16.8s ／ 英文 14.5s*

**畫面公式**

```
留下讓擴張變大的那些   |   keep the ones that enlarge the span
L ( α₁ ) ⊊ L ( α₁ , α₂ ) ⊊ …
```

**旁白（繁中）**

> 有了這個引理，就能從一個有限生成集裡挑出基底：一個一個看過去，留下那些讓線性擴張真的變大的。這個作法很直觀，但要嚴格寫下來相當麻煩，所以書上換了個方式。

**Narration (EN)**

> With that lemma one can pick a basis out of a finite spanning set by running through it and keeping the members that actually enlarge the linear span. That is intuitive but messy to set up rigorously, so the book proceeds differently.

**動畫**

三個一層層變大的橢圓，各自多吃進一個 α 點：一個一個看過去，留下讓擴張真的變大的。這就是那個「直觀但難嚴格寫」的作法，畫出來剛好是一串維度逐一長大的巢狀子空間。

## Beat 10 — 極小的生成集就是基底 / a minimal spanning set is a basis
*配音長度：中文 24.2s ／ 英文 19.2s*

**畫面公式**

```
極小的生成集就是基底   |   a minimal spanning set is a basis
δ ʲ ( i )  =  1  if  i = j ,  else  0        L δ  =  I
```

**旁白（繁中）**

> 定理：任何極小的有限生成集就是基底，所以任何有限維空間都有基底。更一般地，有限維空間的任何有限獨立子集，都能擴充成基底。而座標空間自己有一組很特別的基底：Kronecker 的 delta 函數；它的基底同構正好就是恆等，所以叫標準基底。

**Narration (EN)**

> The theorem: any minimal finite spanning set is a basis, so any finite-dimensional space has one, and any finite independent subset can be extended to a basis. Coordinate space has one special basis, the Kronecker delta functions, whose basis isomorphism is the identity.

**動畫**

極小生成集就是基底；標準基底（Kronecker delta）的基底同構正好是恆等。
