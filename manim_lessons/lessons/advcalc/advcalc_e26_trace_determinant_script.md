# advcalc E26 — 第 2 章：跡與行列式

Chapter 2: Trace and Determinant

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 5 節（書頁 99–101），**第 5 節到此完結**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e26_trace_determinant.py`（`AdvCalcE26ZH` / `AdvCalcE26EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[26]` / `FORMULAS_ADVCALC[26]`）
- 配音：`manim_lessons/samples/audio_e26/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.31 分（199 秒）／英文 3.05 分（183 秒）

書頁 101–102 是習題 5.1–5.12，依 `docs/PLAYBOOK.md` 第 8 節不做解答；書頁 102 起是第 6 節「矩陣計算」，由 E27 接手。

**這一節有一件事必須講準：行列式的存在性書上沒有在這裡證，而是留到第 7 章。** 本節只是假設有這樣一個函數並列出它的五條性質。所以旁白與字幕一律寫「書上假設」，不寫成已經證出來的東西——跡的處境不同，它的存在性第 2 拍就實際造出來了。

符號沿用 E23 到 E25：β 是 V 的基底，t、s 是矩陣，T、S 是映射。λ 是跡泛函（E21、E22 用這個字母表示一般的泛函，這裡是這一節挑出來的那一個），Δ 是行列式，c 是唯一性論證裡那組係數的矩陣。

**書上的圖 2.3 是一個長方形配它被剪切後的像，這裡改成一疊會滑動的薄層**——依第 8 節，插圖自己重新設計，而且要能多做一件事：分層的畫法直接說出體積為什麼不變（沒有一層改變長度，只是移動）。

---

## Beat 0 — 兩個特別的實數值函數 / two special real-valued functions
*配音長度：中文 13.9s ／ 英文 15.2s*

**畫面公式**

```
兩個特別的實數值函數   |   two special real-valued functions
λ  ,  Δ   :   Hom ( V )  →  ℝ
```

**旁白（繁中）**

> 這一節很短，目標是 Hom(V) 上兩個特別的實數值函數：跡與行列式。兩個都把一個線性變換送到一個數，而且都跟基底的選擇無關。

**Narration (EN)**

> This is a short section, and its aim is two special real-valued functions on the space of linear transformations: the trace and the determinant. Both send a transformation to a number, and both are independent of the choice of basis.

**動畫**

左邊一個方框是所有線性變換所成的空間，兩個箭頭分岔到兩個方框：跡與行列式，各自落到右邊那條實數線上的一點。畫面把「兩個都是把變換送到一個數」直接排出來。

## Beat 1 — 定理 5.1：這三個條件只留下一個泛函 / theorem 5.1: three conditions leave one functional
*配音長度：中文 18.6s ／ 英文 17.1s*

**畫面公式**

```
定理 5.1：這三個條件只留下一個泛函   |   theorem 5.1: three conditions leave one functional
λ ( S ∘ T )  =  λ ( T ∘ S )        λ ( I )  =  n        λ ( T )  =  Σ₁ⁿ t ᵢᵢ
```

**旁白（繁中）**

> 先看跡。定理五點一說：在 n 維空間上恰好有一個線性泛函，交換兩個變換的合成順序時值不變，並且在單位變換上取值 n。而它在任何基底下，都等於矩陣主對角線上元素的和。

**Narration (EN)**

> The trace first. Theorem five point one: on an n-dimensional space there is exactly one linear functional unchanged when two transformations swap places in a composite and giving n on the identity. In any basis it is the sum down the main diagonal.

**動畫**

左邊三個方框由上而下是三個條件：線性、交換合成順序值不變、單位變換取值 n。一個標著唯一存在的箭頭指向右邊的矩陣，矩陣主對角線上三格被標出來。標出來的格子是由迴圈的對角條件產生的，不是手動擺的座標。

## Beat 2 — 存在性：同一堆乘積，兩種讀法 / existence: one set of products, read two ways
*配音長度：中文 18.3s ／ 英文 17.3s*

**畫面公式**

```
存在性：同一堆乘積，兩種讀法   |   existence: one set of products, read two ways
λ ( S ∘ T )  =  Σ ᵢ Σ ⱼ s ᵢⱼ t ⱼᵢ  =  Σ ᵢⱼ t ⱼᵢ s ᵢⱼ  =  λ ( T ∘ S )
```

**旁白（繁中）**

> 存在性很好證。選一組基底，把泛函定義成主對角線的和，線性顯然，單位變換給出 n。至於交換性，把合成的矩陣元素寫開，兩個和的指標對調一下，就看到兩邊一樣。

**Narration (EN)**

> Existence is easy. Choose a basis and define the functional as the diagonal sum. Linearity is clear and the identity gives n. For the swapping property, write out the entries of the composite and exchange the two summation indices; the two sides agree.

**動畫**

一個三乘三的格子，每一格寫著一個乘積。左側三個箭頭表示沿橫列加，上方三個箭頭表示沿直行加。兩種加法走的是同一堆格子，這就是交換性的全部理由——寫成一串連等號等於把公式列再抄一次。

## Beat 3 — 唯一性：條件把係數逼成單位矩陣 / uniqueness: the conditions force the coefficients
*配音長度：中文 20.2s ／ 英文 17.3s*

**畫面公式**

```
唯一性：條件把係數逼成單位矩陣   |   uniqueness: the conditions force the coefficients
ν ( t )  =  Σ c ᵢⱼ t ᵢⱼ        ν ( s t − t s ) = 0    ⇒    c ᵢⱼ = δ ᵢⱼ
```

**旁白（繁中）**

> 唯一性的骨架是這樣。透過矩陣與變換的同構，這個泛函在矩陣空間上也是泛函，由一組係數給出。把交換的條件代進去，係數被逼得對角線外全零、對角線上全相等，再用單位變換那條定住大小。

**Narration (EN)**

> Uniqueness goes like this. Through the isomorphism with matrices it is a functional on the matrix space, so a set of coefficients gives it. The swapping condition forces the off-diagonal ones to vanish and the diagonal ones to agree, and the identity fixes the size.

**動畫**

左邊由上往下三個方框：Hom 上的泛函、透過同構搬到矩陣空間、於是由一組係數給出。右邊是那組係數排成的矩陣，對角線被標出來，表示條件把它逼成單位矩陣的樣子。

## Beat 4 — 同一個變換，兩組基底，同一個跡 / one map, two bases, one trace
*配音長度：中文 14.5s ／ 英文 14.3s*

**畫面公式**

```
同一個變換，兩組基底，同一個跡   |   one map, two bases, one trace
λ ( T )  =  tr ( T )        t ′ = a t a ⁻¹    ⇒    Σ t ′ ᵢᵢ  =  Σ t ᵢᵢ
```

**旁白（繁中）**

> 所以這個泛函是唯一的，叫做跡。值得注意的是：定義它的時候選了基底，但定理說它不依賴那個選擇——這正是「跡與基底無關」真正的理由。

**Narration (EN)**

> So the functional is unique, and it is called the trace. Note what happened: a basis was chosen to define it, and the theorem says it does not depend on that choice. That is the real reason the trace is independent of the basis.

**動畫**

最上面一個方框是同一個變換 T，兩個箭頭往下分到兩組不同基底下的矩陣，兩個矩陣的主對角線都被標出來，再各自往下匯到同一個方框「跡」。這一拍刻意重用第 23 集「一個映射兩個矩陣」的構圖，因為跡與基底無關講的正是那一對矩陣。

## Beat 5 — 行列式的絕對值是體積的倍率 / the determinant's size is the volume factor
*配音長度：中文 14.3s ／ 英文 15.0s*

**畫面公式**

```
行列式的絕對值是體積的倍率   |   the determinant's size is the volume factor
v ( T [ A ] )  =  | Δ ( T ) |  ·  v ( A )
```

**旁白（繁中）**

> 接著是行列式。它複雜得多，書上明說存在性要到第 7 章才證。但幾何意義現在就能講：它的絕對值，是這個變換把體積放大的倍率。

**Narration (EN)**

> Now the determinant. It is much more complicated, and the book says its existence is not proved until chapter seven. The geometric meaning can be given now though: its absolute value is the factor by which the transformation multiplies volume.

**動畫**

左邊一個正方形與一個三角形，經過一個箭頭之後變成右邊兩個歪掉的圖形。兩個像都是把同一個矩陣作用在原始頂點上算出來的，不是照著感覺畫的——否則畫面等於在宣稱一個不成立的線性映射。

## Beat 6 — 正負號記錄定向 / the sign records orientation
*配音長度：中文 15.3s ／ 英文 14.4s*

**畫面公式**

```
正負號記錄定向   |   the sign records orientation
Δ ( T ) > 0   ,   Δ ( T ) < 0
```

**旁白（繁中）**

> 正負號則記錄定向。變換保持定向時是正的，把定向反過來時是負的。定向本身也要留到後面才講清楚，這裡先當成「有沒有把左右手對調」。

**Narration (EN)**

> The sign records orientation. It is positive when the transformation preserves orientation and negative when it reverses one. Orientation itself is explained later; for now read it as whether left and right have been swapped over.

**動畫**

左右兩個面板各畫一組兩個向量，中間一段弧線標出從第一個轉到第二個的轉向。左邊轉向不變、標著行列式為正，右邊轉向被反過來、標著為負。**兩組向量的行列式符號在程式裡用斷言釘住**——初稿右邊那組畫成往左上，行列式其實是正的，跟底下的標籤互相矛盾。

## Beat 7 — 書上假設的五條性質：乘法性與剪切 / five assumed properties: products and shearings
*配音長度：中文 21.9s ／ 英文 17.6s*

**畫面公式**

```
書上假設的五條性質：乘法性與剪切   |   five assumed properties: products and shearings
Δ ( S ∘ T )  =  Δ ( S ) Δ ( T )        T | N = I  ,  T | V / N = I    ⇒    Δ ( T ) = 1
```

**旁白（繁中）**

> 書上先假設行列式存在，列出五條性質。第一條，合成的行列式等於兩個行列式相乘。第二條，剪切的行列式是一；所謂剪切，是沿著平行於某個子空間的方向把空間推歪，每一層自己不變形，只是滑動。

**Narration (EN)**

> The book assumes the determinant exists and lists five properties. First, the determinant of a composite is the product of the determinants. Second, a shearing has determinant one: a shearing slides the space along planes parallel to a subspace, no layer deforming.

**動畫**

左上是合成的乘法性。左下把空間畫成一疊薄層，每一層長度相同、只是往右滑，底下一條線是那個不變子空間；右邊是一個正方形被推成平行四邊形。書上的圖 2.3 是一個長方形配它的像，這裡改成分層，是為了讓畫面說出「為什麼體積不變」，而不只是「體積不變」。

## Beat 8 — 直和、一維、二維互換 / direct sums, one dimension, a swap
*配音長度：中文 21.6s ／ 英文 18.7s*

**畫面公式**

```
直和、一維、二維互換   |   direct sums, one dimension, a swap
V = M ⊕ N   ⇒   Δ ᵥ ( T ) = Δ ᴹ ( R ) Δ ᴺ ( S )        d ( V ) = 1  ⇒  Δ ( T ) = c ᴛ        Δ = − 1
```

**旁白（繁中）**

> 第三條，空間拆成兩個不變子空間的直和時，行列式是兩塊各自的乘積。第四條，一維時變換就是乘一個常數，行列式就是那個常數。第五條，二維時把一對獨立向量互換，行列式是負一，純粹是定向。

**Narration (EN)**

> Third, when the space splits as a direct sum of invariant subspaces, the determinant is the product over the pieces. Fourth, in one dimension the map multiplies by a constant, and that constant is the determinant. Fifth, swapping two independent vectors in the plane gives minus one.

**動畫**

三個方框由上而下是第三、四、五條性質。右下角一對雙向箭頭畫出「互換一對獨立向量」，對應第五條那個純粹的定向性質。

## Beat 9 — 定理 5.2：二維的公式 / theorem 5.2: the two-dimensional formula
*配音長度：中文 18.5s ／ 英文 17.8s*

**畫面公式**

```
定理 5.2：二維的公式   |   theorem 5.2: the two-dimensional formula
Δ ( T )  =  t ₁₁ t ₂₂  −  t ₁₂ t ₂₁        n × n   :   n !
```

**旁白（繁中）**

> 定理五點二給出二維的公式：主對角線的乘積，減去另一條對角線的乘積。這是一般公式的特例；一般的公式有 n 階乘項，每項是矩陣裡 n 個數的乘積，n 大時不實用，n 等於三還算好用。

**Narration (EN)**

> Theorem five point two gives the two-dimensional formula: the product down the diagonal minus the product up the other one. It is a special case of a general formula with n factorial terms, each a product of n entries, impractical for large n but fine for three.

**動畫**

一個真的二乘二矩陣，兩條對角線各自用一個顏色連起來，箭頭指向右邊的公式方框。這一拍用二乘二不是與其他拍不一致——定理 5.2 講的就是二維的情形。

## Beat 10 — 轉置、可逆，與 Cramer 法則 / transposes, invertibility, and Cramer's rule
*配音長度：中文 21.6s ／ 英文 18.2s*

**畫面公式**

```
轉置、可逆，與 Cramer 法則   |   transposes, invertibility, and Cramer's rule
Δ ( T * ) = Δ ( T )        Δ ( θ ∘ T ∘ θ ⁻¹ ) = Δ ( T )        Δ ( T ) ≠ 0  ⇔  ∃ T ⁻¹        D ( t ) x ⱼ = D ( t | ⱼ y )
```

**旁白（繁中）**

> 最後三條。轉置不改變行列式，用同構把變換搬到另一個空間也不改變。變換可逆，若且唯若行列式不是零。最後是 Cramer 法則：把第 j 直行換成等號右邊那個向量，兩個行列式的比就是解的第 j 個座標。

**Narration (EN)**

> Three last results. Transposing leaves the determinant alone, and so does carrying the map elsewhere by an isomorphism. A map is invertible exactly when its determinant is not zero. Finally Cramer's rule: replace the jth column by the right hand side and take a ratio.

**動畫**

左邊三個方框是最後三條結果。右邊是 Cramer 法則：一個矩陣的第 j 直行被整條換掉，換上去的那一行用另一個顏色標出來並標著 y。
