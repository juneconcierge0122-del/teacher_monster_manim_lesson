# advcalc E22 — 第 2 章：零化子與伴隨算子

Chapter 2: Annihilators and the Adjoint

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 3 節的後半（書頁 83–86）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e22_annihilators.py`（`AdvCalcE22ZH` / `AdvCalcE22EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[22]` / `FORMULAS_ADVCALC[22]`）
- 配音：`manim_lessons/samples/audio_e22/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.38 分（203 秒）／英文 3.15 分（189 秒）

書頁 87–88 是習題，依 `docs/PLAYBOOK.md` 第 8 節不做解答。第 4 節「矩陣」從書頁 88 起，留給 E23。

符號沿用 E21：β 是 V 的基底、ε 是對偶基底、λ 是泛函。書上定理 3.3 的對偶基底寫成 λ，會跟四拍之後 dyad 的 λ 撞名，所以改用 ε；dyad 在 W 裡的向量也改用 η 而不是書上的 β。

---

## Beat 0 — 零化子：對偶版本的正交 / the annihilator: orthogonality in the dual
*配音長度：中文 19.7s ／ 英文 16.8s*

**畫面公式**

```
零化子：對偶版本的正交   |   the annihilator: orthogonality in the dual
A ⊂ V        A °  =  { f ∈ V * :  f ( α ) = 0   ∀ α ∈ A }
```

**旁白（繁中）**

> 上一集建立了對偶空間。現在問：給一個子集，對偶空間裡哪些泛函在它上面整個取零？這些泛函的集合，書上叫做它的零化子。正交第一次自然出現就在這裡，那個詞留到第 5 章。

**Narration (EN)**

> The last episode built the dual space. Next question: given a subset, which functionals in the dual vanish on all of it? The book calls that set the annihilator of the subset. Orthogonality first appears in this dual setting, but the word waits for chapter five.

**動畫**

V 畫成橢圓，裡面標出子集 A；A 裡的三個向量沿箭頭全部落到實數線上的同一點零。右邊另一個橢圓是 V 的對偶空間，裡面反白的那一塊就是 A 的零化子。重點是「整個取零」——只要有一個向量沒被送到零，那個泛函就不在裡面。

## Beat 1 — 反過來的定義，與五條性質 / the definition the other way, and five properties
*配音長度：中文 18.9s ／ 英文 16.9s*

**畫面公式**

```
反過來的定義，與五條性質   |   the definition the other way, and five properties
A ⊂ V *   ⇒   A °  =  { α ∈ V :  f ( α ) = 0   ∀ f ∈ A }        ( L ( A ) ) ° = A °        A ⊂ A ° °
```

**旁白（繁中）**

> 定義也有反過來的方向：對偶空間裡一個子集，被它每個泛函都送到零的向量，同樣構成零化子。五條性質留作習題，兩條等一下要用：換成線性擴張零化子不變，集合都包在雙重零化子裡。

**Narration (EN)**

> The definition runs the other way too: the vectors that every functional in a subset of the dual sends to zero also form an annihilator. Two of the five exercises matter here: the span changes nothing, and every set sits inside its double annihilator.

**動畫**

兩列對照：上一列是子集在 V 裡、零化子跑到對偶空間；下一列反過來，子集在對偶空間裡、零化子跑回 V。顏色跟著空間走，所以兩列的配色恰好對調。

## Beat 2 — 維數在子空間與零化子之間分完 / the dimensions split between the two
*配音長度：中文 19.0s ／ 英文 18.0s*

**畫面公式**

```
維數在子空間與零化子之間分完   |   the dimensions split between the two
β₁ … βₘ   :   W        β₁ … βₙ   :   V        εₘ₊₁ … εₙ   :   W °        d ( V ) = d ( W ) + d ( W ° )
```

**旁白（繁中）**

> 接著是一條維數等式。W 是 V 的子空間的話，V 的維數等於 W 的維數加上零化子的維數。證明是把 W 的基底延長成 V 的，再看對偶基底：延長那一段對應的泛函正好是零化子的基底。

**Narration (EN)**

> Then a dimension identity. If W is a subspace of V, the dimension of V is that of W plus that of its annihilator. The proof extends a basis for W to a basis for V and looks at the dual basis: the functionals matching the added vectors span the annihilator.

**動畫**

定理的證明就是這張圖。把 V 的基底排成一列，在 W 停下來的地方切一刀（虛線）；下面那一列是對偶基底，切點右邊的那一段亮起來，正是零化子的基底。左邊那一段畫暗，因為它們在 W 上不取零，進不了零化子。兩段的長度加起來就是維數等式。

## Beat 3 — 零化兩次得到線性擴張 / annihilating twice gives the linear span
*配音長度：中文 14.4s ／ 英文 16.4s*

**畫面公式**

```
零化兩次得到線性擴張   |   annihilating twice gives the linear span
A ° °  =  L ( A )
```

**旁白（繁中）**

> 推論馬上跟著來：任何子集的雙重零化子就是它的線性擴張。維數等式用兩次夾出兩邊維數相同，而線性擴張本來就包在裡面，只好一樣。

**Narration (EN)**

> A corollary follows at once: the double annihilator of any subset is its linear span. Apply the identity twice and the two have the same dimension. The span already sits inside the double annihilator, and with equal dimensions they must coincide.

**動畫**

包含鏈 A ⊂ L(A) ⊂ A°°，接著把維數等式用兩次得到中間那一條，最後夾成等號。畫成由上往下三層，是因為這個推論的重點是「包含加上維數相等就逼出相等」這個推理形狀，不是等式本身。

## Beat 4 — 伴隨算子：把泛函沿著映射拉回來 / the adjoint: pull functionals back along the map
*配音長度：中文 18.7s ／ 英文 17.4s*

**畫面公式**

```
伴隨算子：把泛函沿著映射拉回來   |   the adjoint: pull functionals back along the map
l ∈ W *   ⇒   l ∘ T ∈ V *        T * ( l ) = l ∘ T   :   Hom ( W * , V * )
```

**旁白（繁中）**

> 換到伴隨算子。取一個從 V 到 W 的線性映射，再取 W 上的一個泛函，一合成就得到 V 上的泛函。這個對應是從 W 的對偶到 V 的對偶，書上叫它伴隨算子。注意箭頭反過來了。

**Narration (EN)**

> Now the adjoint. Take a linear map from V to W and a functional on W. Compose them and you have a functional on V. The correspondence this defines is a linear map from the dual of W to the dual of V, and it is called the adjoint. Notice the arrow has reversed.

**動畫**

上排是 V 到 W 再到實數線，合成的那一條畫在下面，標成 l 之後接 T。下排把對應的對偶空間畫出來，箭頭刻意畫成由右往左，跟上排反向——這是這一拍唯一要記住的事。

## Beat 5 — 這個對應本身就是同構 / the correspondence is itself an isomorphism
*配音長度：中文 20.3s ／ 英文 17.9s*

**畫面公式**

```
這個對應本身就是同構   |   the correspondence is itself an isomorphism
T  ↦  T *   :   Hom ( V , W )  ≅  Hom ( W * , V * )        d = m n
```

**旁白（繁中）**

> 第一條定理說，把映射送到伴隨算子，這個對應本身就是同構。線性來自合成的雙線性。映射不是零的話，找個向量讓它在上面不是零，再找個泛函在像上不取零，就有嵌射。維數又相同。

**Narration (EN)**

> The first theorem: sending a map to its adjoint is itself an isomorphism. Linearity comes from composition being bilinear. If the map is not zero, find a vector it does not kill and a functional nonzero on the image. That gives injectivity, and the dimensions match.

**動畫**

左右兩個 Hom 空間，中間是 T 送到伴隨算子的箭頭，底下標著兩邊都是 m 乘 n。下方那條三格鏈是嵌射的論證：映射不是零，就找得到一個向量的像不是零，再找得到一個泛函在那個像上不取零。

## Beat 6 — 合成的順序會反過來 / composition reverses the order
*配音長度：中文 17.6s ／ 英文 16.0s*

**畫面公式**

```
合成的順序會反過來   |   composition reverses the order
( T ∘ S ) *  =  S *  ∘  T *
```

**旁白（繁中）**

> 同一條定理還有第二半：兩個映射先後合成，取伴隨算子時順序反過來。這不是巧合。伴隨算子是把泛函沿著映射往回拉，往回走時最後施加的那一步最先被遇到。

**Narration (EN)**

> The same theorem has a second half: for two maps composed in turn, taking adjoints reverses the order. That is no accident. The adjoint pulls functionals backwards along the map, and going backwards, the step applied last is the one met first.

**動畫**

上排 U 到 V 到 W，下排是對應的對偶空間。S 與 S*、T 與 T* 各自同色，所以順序反過來這件事是用顏色看出來的：上排先青後紫，下排先紫後青。

## Beat 7 — 零空間與值域互換 / null spaces and ranges trade places
*配音長度：中文 17.7s ／ 英文 16.7s*

**畫面公式**

```
零空間與值域互換   |   null spaces and ranges trade places
N ( T * )  =  ( R ( T ) ) °        ( R ( T * ) ) °  =  N ( T )
```

**旁白（繁中）**

> 第二條定理把零空間與值域對調。伴隨算子的零空間正好是原映射值域的零化子，反過來，伴隨算子值域的零化子正好是原映射的零空間。證明只是把定義一層層拆開。

**Narration (EN)**

> The second theorem trades null spaces for ranges. The null space of the adjoint is exactly the annihilator of the range of the original map, and the annihilator of the range of the adjoint is exactly its null space. The proof only unwinds the definitions.

**動畫**

左邊橢圓是 W，裡面是 T 的值域；右邊是 W 的對偶空間，裡面是伴隨算子的零空間；中間的箭頭就是取零化子。底下那一條是證明本身——三個敘述用等價符號串起來，每一步都只是把定義換句話說。

## Beat 8 — 秩相等 / the ranks are equal
*配音長度：中文 17.4s ／ 英文 16.7s*

**畫面公式**

```
秩相等   |   the ranks are equal
d ( R ( T * ) )  =  d ( R ( T ) )
```

**旁白（繁中）**

> 線性變換的值域維數叫做它的秩。兩條定理合起來就得到伴隨算子的秩等於原映射的秩。這後面會變成矩陣的著名事實：橫列生成的空間跟直行生成的空間維數相同。

**Narration (EN)**

> The dimension of the range of a linear transformation is its rank. Putting the last two theorems together, the adjoint has the same rank as the map it came from. Later this becomes a known fact about matrices: rows and columns span spaces of the same dimension.

**動畫**

矩陣畫成一組點加一對括號（不畫格線，避免看起來像表格）：橫過去的一條與直下來的一條各自標出橫列與直行生成的空間。底下那一條式子是關鍵——兩邊都等於 V 的維數減去零空間的維數，所以被夾成同一個數。

## Beat 9 — 值域一維的映射就是 dyad / a one-dimensional range makes a dyad
*配音長度：中文 18.8s ／ 英文 18.2s*

**畫面公式**

```
值域一維的映射就是 dyad   |   a one-dimensional range makes a dyad
T ( ξ ) = λ ( ξ ) η        T = λ ( · ) η        T * = η * * ( · ) λ
```

**旁白（繁中）**

> 再看一個特別情形：值域只有一維的映射。取值域裡一個非零向量，映射就把每個輸入送到某個係數乘它，而係數對輸入是線性的，就是一個泛函。書上叫這種映射 dyad，伴隨算子也是。

**Narration (EN)**

> A special case: a map with a one dimensional range. Pick a nonzero vector in it. The map sends each input to a coefficient times that vector, and the coefficient is linear in the input, so it is a functional. The book calls this a dyad, and its adjoint is one too.

**動畫**

左邊是 V，右邊是 W，而 T 的值域在 W 裡只是一條線。三個輸入的像全部落在那條線上（座標由程式算出來，保證真的在線上），所以整個映射可以拆成先取一個係數、再乘上線上的一個固定向量兩步。

## Beat 10 — 自然的意思：這張圖可交換 / what natural means: the square commutes
*配音長度：中文 20.3s ／ 英文 18.1s*

**畫面公式**

```
自然的意思：這張圖可交換   |   what natural means: the square commutes
ψ ∘ T  =  T * * ∘ φ        φ : V ≅ V * *  ,  ψ : W ≅ W * *
```

**旁白（繁中）**

> 最後把自然這個詞講清楚。每個空間都有通往第二共軛空間的同構。取一個從 V 到 W 的映射畫成方框：上面是它，下面是伴隨算子的伴隨算子，兩邊是同構。自然就是這方框永遠可交換。

**Narration (EN)**

> Finally, what natural means. Every space has its own isomorphism onto its second conjugate. Take any map from V to W and draw a square: the map along the top, the adjoint of its adjoint along the bottom, the isomorphisms down the sides. It always commutes.

**動畫**

四個角落是 V、W 與它們的第二共軛空間，上下兩條橫的是 T 與它的兩次伴隨，左右兩條直的是那兩個自然同構。自然的意思就是這個方框可交換——沿著上面再往下，跟先往下再沿著下面，結果一樣。
