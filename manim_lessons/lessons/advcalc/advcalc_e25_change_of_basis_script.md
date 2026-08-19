# advcalc E25 — 第 2 章：行向量、換基底與 Hom 的標準基底

Chapter 2: Column Vectors, Change of Basis and a Basis for Hom

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 4 節的最後一段（書頁 93–96），**第 4 節到此完結**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e25_change_of_basis.py`（`AdvCalcE25ZH` / `AdvCalcE25EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[25]` / `FORMULAS_ADVCALC[25]`）
- 配音：`manim_lessons/samples/audio_e25/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.26 分（196 秒）／英文 3.01 分（181 秒）

書頁 96–98 是習題 4.1–4.26，依 `docs/PLAYBOOK.md` 第 8 節不做解答；書頁 99 起是第 5 節「跡與行列式」，由 E26 接手。

符號沿用 E23 與 E24：β 與 β′ 是 V 的兩組基底、γ 與 γ′ 是 W 的兩組、ε 是對偶基底。φ 與 ψ 是 E23 那兩個基底同構，這裡按兩組選擇編號；a 與 b 是換座標矩陣，t′ 與 t″ 是 T 對兩組基底的矩陣。T′ 仍然是 T 的座標空間版本，跟 E23 用撇號的角色一樣。

**書上圖 2.2 畫成一個立體稜柱，這裡改成三列的排法**——依第 8 節，插圖一律自己重新設計，不照著書上的圖描。第 5 拍建立這張圖，第 6 拍在同一張圖上標出兩條路徑，等式就從圖上讀出來。

陣列繪圖工具與 E23、E24 共用 `manim_lessons/lessons/advcalc/arrays.py`。

---

## Beat 0 — 一個 n 元組的兩種讀法 / two ways to read an n-tuple
*配音長度：中文 17.9s ／ 英文 17.3s*

**畫面公式**

```
一個 n 元組的兩種讀法   |   two ways to read an n-tuple
x  =  ⟨ x₁ , … , xₙ ⟩        x  :  n × 1        x *  :  1 × n
```

**旁白（繁中）**

> 先講一個看似瑣碎、其實很有用的認同。一個 n 元組可以看成 n 列一行的矩陣，叫行向量；也可以看成一列 n 行的，叫列向量。兩種都是自然同構，書上取行向量為標準。

**Narration (EN)**

> First an identification that looks trivial and is not. An n-tuple can be read as an n by 1 matrix, called a column vector, or as a 1 by n matrix, called a row vector. Both are natural isomorphisms, and the book takes the column vector as standard.

**動畫**

中間是一個寫成角括號的 n 元組，兩個箭頭把它帶往兩種讀法：左下是 n 列一行的行向量，右下是一列 n 行的列向量，各自標著形狀。兩個讀法的元素由同一個下標常數產生，所以不可能列出不同的內容。

## Beat 1 — 映射就是左乘一個矩陣 / a map is left multiplication by a matrix
*配音長度：中文 17.0s ／ 英文 17.3s*

**畫面公式**

```
映射就是左乘一個矩陣   |   a map is left multiplication by a matrix
y ᵢ  =  Σ₁ⁿ t ᵢⱼ x ⱼ        y  =  t · x        T   :   x  ↦  t x
```

**旁白（繁中）**

> 這麼一來，上一集那組純量方程正好是說：輸出的行向量等於矩陣乘上輸入的行向量。於是座標空間之間的線性映射，就變成左乘一個固定的矩陣，映射與乘法完全合一。

**Narration (EN)**

> With that, last episode's scalar equations say exactly this: the output column vector is the matrix times the input column vector. So a linear map between Cartesian spaces becomes left multiplication by one fixed matrix, and map and product coincide.

**動畫**

左邊是矩陣乘行向量等於行向量，矩陣的第 i 橫列被標出來，對應到輸出被標出來的那一格。右邊一個方框寫著「映射就是左乘 t」——上一集的純量方程與這一集的乘法，在畫面上並排。

## Beat 2 — 泛函就是列向量 / a functional is a row vector
*配音長度：中文 15.3s ／ 英文 14.5s*

**畫面公式**

```
泛函就是列向量   |   a functional is a row vector
L a ( x )  =  Σ₁ⁿ a ᵢ x ᵢ  =  a * · x        a *  :  1 × n        a * x  :  1 × 1
```

**旁白（繁中）**

> 泛函那邊呢？一個泛函的矩陣是一列 n 行，所以泛函就是列向量。把它作用在輸入上，就是列向量乘行向量，得到一乘一的矩陣，也就是一個數。

**Narration (EN)**

> What about functionals? The matrix of a functional is 1 by n, so a functional is a row vector. Applying it to an input is a row vector times a column vector, giving a 1 by 1 matrix, which is to say a number.

**動畫**

一列 n 行的列向量乘上 n 列一行的行向量，等於一乘一的矩陣。三個物件上方各自標著形狀，讓「為什麼結果是一個數」由形狀自己說出來，而不是用講的。

## Beat 3 — 伴隨算子變成右乘 / the adjoint becomes right multiplication
*配音長度：中文 20.1s ／ 英文 16.5s*

**畫面公式**

```
伴隨算子變成右乘   |   the adjoint becomes right multiplication
L a ( T ( x ) )  =  a * t x        T * ( L a )  =  a * t        T *  :  t *
```

**旁白（繁中）**

> 再看伴隨算子。泛函先走映射再取值，對應到的是列向量右乘矩陣。所以泛函寫成列向量時，伴隨算子是右乘；轉置換回行向量，就變成左乘轉置矩陣。這是那條定理的第二個證明。

**Narration (EN)**

> Now the adjoint. A functional composed with the map corresponds to that row vector multiplied on the right by the matrix. So with functionals as rows the adjoint is right multiplication, and transposing back to columns makes it left multiplication by the transpose.

**動畫**

左半邊由上往下兩個方框：泛函先走映射再取值，等於那個列向量右乘矩陣。右半邊上下兩個方框對照「列向量時右乘」與「行向量時左乘轉置」。中間一條線把兩種寫法分開。

## Beat 4 — 換座標，不是空間上的映射 / a change of coordinates, not a map on the space
*配音長度：中文 19.2s ／ 英文 16.8s*

**畫面公式**

```
換座標，不是空間上的映射   |   a change of coordinates, not a map on the space
φ : x ↦ Σ xᵢ βᵢ        θ : y ↦ Σ yᵢ βᵢ′        A = θ ⁻¹ ∘ φ   :   y = a x
```

**旁白（繁中）**

> 接著換基底。同一個空間取兩組基底就有兩個基底同構，一個接上另一個的反函數，得到的是座標之間的換算。小心別跟另一個像的映射搞混：那一個把第一組基底送到第二組，是空間上的映射。

**Narration (EN)**

> Now change of basis. Two bases for one space give two basis isomorphisms, and following one with the inverse of the other changes coordinates into coordinates. Do not confuse it with the map sending the first basis to the second, which acts on the space itself.

**動畫**

左半邊是一個三角形：兩個座標空間各自透過基底同構連到 V，換座標的映射沿著左邊直接把上面的座標空間送到下面的。右半邊只有一個箭頭，從 V 到 V，把第一組基底送到第二組。兩者形狀不同，就是書上提醒不要搞混的那件事。

## Beat 5 — 兩層的圖：九個映射 / the two-storey diagram: nine maps
*配音長度：中文 17.6s ／ 英文 16.6s*

**畫面公式**

```
兩層的圖：九個映射   |   the two-storey diagram: nine maps
T ′ = ψ₁ ⁻¹ ∘ T ∘ φ₁        T ″ = ψ₂ ⁻¹ ∘ T ∘ φ₂        A = φ₂ ⁻¹ ∘ φ₁  ,  B = ψ₂ ⁻¹ ∘ ψ₁
```

**旁白（繁中）**

> 書上為此畫了一張兩層的圖。上下兩層都是座標空間，中間夾著抽象的兩個空間，四個基底同構把它們接起來，兩個換座標的映射站在兩側。九個映射，彼此牽制。

**Narration (EN)**

> For this the book draws a two-storey diagram. Both storeys are Cartesian spaces, the abstract spaces sit between them, four basis isomorphisms join them up, and the two changes of coordinates stand at the sides. Nine maps, all constraining each other.

**動畫**

書上圖 2.2 那九個映射，這裡排成三列：上下兩列是座標空間，中間一列是抽象的 V 與 W，四個基底同構垂直連接，兩個換座標的映射走外側。書上是畫成一個立體的稜柱，這個構圖刻意不是那個。

## Beat 6 — 兩條路一樣，等式就讀出來了 / two paths agree, and the identity falls out
*配音長度：中文 16.6s ／ 英文 14.5s*

**畫面公式**

```
兩條路一樣，等式就讀出來了   |   two paths agree, and the identity falls out
T ″  =  B ∘ T ′ ∘ A ⁻¹        t ″  =  b t ′ a ⁻¹
```

**旁白（繁中）**

> 這張圖可交換，意思是任何兩點之間的兩條路都代表同一個映射。挑一對路徑就讀出一條等式：新矩陣等於右側的換座標矩陣，乘上舊矩陣，再乘左側那個的反矩陣。

**Narration (EN)**

> The diagram commutes: any two paths between two points are the same map. Pick a pair and read off an identity. The new matrix is the change matrix on the right, times the old matrix, times the inverse of the one on the left.

**動畫**

同一張圖，這次把兩條路標出來：一條沿外側繞上去、橫越上層、再沿外側繞下來，另一條直接走下層。兩條路代表同一個映射，等式就直接讀出來，放在圖的正下方。

## Beat 7 — 同一個空間，與實數那一側 / one space, and the real line side
*配音長度：中文 19.2s ／ 英文 16.3s*

**畫面公式**

```
同一個空間，與實數那一側   |   one space, and the real line side
W = V   ⇒   t ″ = a t ′ a ⁻¹        b = e   ⇒   f ″ = ( a ⁻¹ ) * f ′        x ″ = a x ′
```

**旁白（繁中）**

> 如果兩端是同一個空間，只有一組基底要換，式子就變成相似變換。再看泛函：實數那邊沒有基底要換，所以泛函的座標是乘上換座標矩陣的反矩陣的轉置——跟向量比，兩者往相反方向變。

**Narration (EN)**

> If both ends are the same space there is one basis change and the formula becomes a similarity. For functionals nothing changes on the real line, so their coordinates get the transpose of the inverse change matrix. Compare a vector: the two go opposite ways.

**動畫**

左右兩個情形各自由上往下推：左邊是兩端同一個空間，只有一組基底要換，得到相似變換；右邊是值域為實數，那一側的換座標矩陣是單位矩陣，於是泛函的座標乘的是反矩陣的轉置。

## Beat 8 — 共變與逆變：同一個換基底，兩條反向的規則 / covariant and contravariant: one change, two inverse rules
*配音長度：中文 16.5s ／ 英文 16.2s*

**畫面公式**

```
共變與逆變：同一個換基底，兩條反向的規則   |   covariant and contravariant: one change, two inverse rules
ξ ∈ V   :   x ″ = a x ′        F ∈ V *   :   f ″ = ( a ⁻¹ ) * f ′
```

**旁白（繁中）**

> 因為這個緣故，古典張量分析把泛函叫做共變向量，把空間裡的向量叫做逆變向量。這兩個詞在微分幾何裡會一直出現，而它們的來歷就是剛剛那兩條方向相反的式子。

**Narration (EN)**

> For this reason classical tensor analysis calls functionals covariant vectors and calls the vectors of the space contravariant. Both words recur throughout differential geometry, and their whole origin is those two formulas running in opposite directions.

**動畫**

一個換基底矩陣放在上方，兩個箭頭分岔到兩條規則：左邊是向量的座標乘上它本身，右邊是泛函的座標乘上它的反矩陣的轉置。兩個方框之間用一條虛線標著取反矩陣，說明兩條規則互為反向——這就是共變與逆變兩個詞的全部內容。

## Beat 9 — Hom(V, W) 的標準基底 / the standard basis of Hom(V, W)
*配音長度：中文 17.9s ／ 英文 18.0s*

**畫面公式**

```
Hom(V, W) 的標準基底   |   the standard basis of Hom(V, W)
δ ᵏˡ ( i , j ) = 0  ,  δ ᵏˡ ( k , l ) = 1        D ₖₗ ( βⱼ ) = 0   ( j ≠ l )  ,  D ₖₗ ( βₗ ) = γₖ
```

**旁白（繁中）**

> 最後一件事。矩陣空間有它的標準基底，透過同構搬過去，就是所有線性映射所成空間的標準基底。第 k l 個做的事很單純：把第 l 個基底向量送到第 k 個，其他送到零。

**Narration (EN)**

> One last thing. The space of matrices has a standard basis, and carrying it across the isomorphism gives a standard basis for the space of all linear maps. The k l th one does something simple: it sends the l th basis vector to the k th and the rest to zero.

**動畫**

左邊 V 裡三個基底向量，只有第三個被標出來，另外兩個旁邊直接寫著送到零；被標出來的那個沿一條箭頭送到 W 裡的第二個基底向量。右邊是對應的矩陣，只有第二列第三行那一格是一。矩陣裡那個一的位置與左邊被標出來的兩個下標由同一組常數決定。

## Beat 10 — 矩陣元素就是這組基底下的座標 / the entries were the coordinates all along
*配音長度：中文 18.3s ／ 英文 16.7s*

**畫面公式**

```
矩陣元素就是這組基底下的座標   |   the entries were the coordinates all along
T ( ξ )  =  Σ ᵢⱼ t ᵢⱼ D ᵢⱼ ( ξ )        T  =  Σ ᵢⱼ t ᵢⱼ D ᵢⱼ        D ₗ  =  ε ₗ
```

**旁白（繁中）**

> 把一個映射用這組基底展開，係數自己跑出來，正好就是它的矩陣元素——矩陣元素本來就是這組基底下的座標。對偶基底只是特例。第 4 節到此結束，下一集講跡與行列式。

**Narration (EN)**

> Expand a map in that basis and the coefficients come out on their own as its matrix entries, so the entries were the coordinates in this basis all along. The dual basis is one special case. Section four ends here; next time, trace and determinant.

**動畫**

左半邊由上往下：把映射作用在向量上展開，係數自己跑出來，於是得到映射本身的展開式。右半邊是特例：值域取實數時，這組基底就退化成對偶基底。
