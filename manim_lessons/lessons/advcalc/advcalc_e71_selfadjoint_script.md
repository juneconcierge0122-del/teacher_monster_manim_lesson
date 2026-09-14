# advcalc E71 — 第 5 章：自伴變換

Chapter 5: Self-Adjoint Transformations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 3 節「自伴變換」（書頁 257–260），**整節一集講完**。

習題 3.1–3.14 在書頁 260–261（依 PLAYBOOK 第 8 節不做解答），**§4「正交變換」從書頁 262 起**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e71_selfadjoint.py`（`AdvCalcE71ZH` / `AdvCalcE71EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[71]` / `FORMULAS_ADVCALC[71]`）
- 配音：`manim_lessons/samples/audio_e71/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 219.6 秒配音／英文 211.7 秒配音

## 一個推論撐起整節

**這一節真正的樞紐是引理 3.2 的推論：( T ξ , ξ ) 一等於零，T ξ 就是零。**

自伴的定義是 T 可以在內積裡從一邊搬到另一邊。這句話有兩個等價的說法：
在嵌入 θ 底下 T 變成自己的伴隨（T * ∘ θ = θ ∘ T），
以及對**正交規範**基而言矩陣對稱（引理 3.1）。

自伴而且 ( T ξ , ξ ) 恆非負的 T 叫**非負**。這時 [ ξ , η ] = ( T ξ , η ) 是**半純量積**
——對稱來自自伴，非負來自假設——所以 Schwarz 不等式可以用，取 η = T ξ 就得到

```
‖ T ξ ‖ ²    ≤    ‖ T ‖  ( T ξ , ξ )
```

**定理 3.1 整個就是這一句的應用。** 在單位球面上取 m 為 ( T ξ , ξ ) 的上確界（球面緊緻，
所以取得到，在某個 α 上）。m − T 非負而且自伴，而「最大值在 α 取到」寫出來就是
( ( m − T ) α , α ) = 0，引理 3.2 於是逼出 ( m − T ) α = 0，也就是 **T α = m α**。
接著 α ₁ 的正交補在 T 底下不變（把 T 搬過去就看出來），在裡面重做一次，維數每次掉一，
最後得到一組**全由特徵向量組成的正交規範基**。

把相同的特徵值歸成一組得到 M ⱼ，引理 3.3 說每個特徵向量都落在某個 M ⱼ 裡，
所以**定理 3.2**：那個正交分解與那些 λ ⱼ 是唯一的（基向量本身不是）。
有了特徵基底，T ²、T ⁻ ¹、P ( T ) 全部退化成對特徵值做算術。

**最後是反面。** 一般的 T 可能連一個特徵向量都沒有：平面上轉九十度的那個 R，
特徵多項式 λ ² + 1 在實數上不可約。定理 3.3 說明還剩下什麼——
特徵值恰好是極小多項式的根。

## 這一集的具體數字

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 自伴的定義 | S = [[2, 0.8], [0.8, 1.2]] 對 α、β | ( T α , β ) = ( α , T β ) = 2.9680 |
| 不自伴的樣子 | 把 0.8 換成 −0.3 | 1.5380 對 2.7040，差 1.1660 |
| 差就是反對稱部分 | ( n ₁₂ − n ₂₁ )( α ₂ β ₁ − α ₁ β ₂ ) | 與上式差 < 1e-12 |
| T * ∘ θ = θ ∘ T | 兩條路徑各算一次 | 都是 2.9680 |
| 引理 3.1 | 標準基 ↔ b ₂ 拉長成兩倍 | 0.8 = 0.8 ↔ 1.6 ≠ 0.4 |
| 半純量積會退化 | P 是對角線上的投影，w = ⟨1, −1⟩ | ( P w , w ) = 0.0000 而 ‖ w ‖ = 1.4142 |
| 引理 3.2 | 四個 ξ 各算兩邊 | 4.6400 ≤ 4.9889、0.5904 ≤ 2.0654、0.4978 ≤ 1.7600 |
| 等號在哪裡 | ξ = α ₁ | 6.2222 = 6.2222 |
| 上確界取得到 | 取樣 12 / 360 / 3600 | 差 1.61e-03 → 4.35e-05 → 1.66e-07 |
| m − T 非負 | 3600 個方向 | min = 1.7e-07，max = 1.7889 |
| 最大值點是特徵向量 | 精確的 α ₁ | ( ( m − T ) α ₁ , α ₁ ) = 0.0e+00，‖ T α ₁ − m α ₁ ‖ = 0.0e+00 |
| 正交補不變 | 特徵值 5、3、1 的 T，ξ ⊥ α ₁ | ( ξ , α ₁ ) = −5.6e-17，( T ξ , α ₁ ) = −2.2e-16 |
| 特徵向量不唯一 | A 有重根 2，把 M ₂ 裡那一對轉 0.7 弧度 | ‖ T u ′ − 2 u ′ ‖ = 2.2e-16，( u , u ′ ) = 0.7648 |
| 多項式作用在特徵向量上 | P ( t ) = t ² − 3 t + 1 | P ( 5 ) = 11、P ( 2 ) = −1，殘量 ≤ 1.4e-16 |
| 轉九十度沒有特徵向量 | 1440 個方向 | max \| ( R ξ , ξ ) \| = 0.0e+00，min ‖ R ξ − ( R ξ , ξ ) ξ ‖ = 1.0000 |

**這一集用了三個自伴變換，各有各的差事。**

- **平面上的 S**（特徵值 2.4944、0.7056）撐起單位圓的那幾拍：Schwarz 的鬆緊、極座標圖、
  刺圖。它的兩個特徵值差了三倍多，所以極座標圖看得出腰身，刺圖也看得出「只在兩個方向歸零」。
- **三維、特徵值 5 / 3 / 1 的那一個**只用在歸納那一拍。**這裡不能用有重根的矩陣**：
  正交補上的限制若是純量乘法，T ξ 就會跟 ξ 共線，畫出來的兩支箭頭疊在一起，
  「落回同一個平面」這件事反而看不出來。
- **A = [[3,1,1],[1,3,1],[1,1,3]]**（特徵值 5、2、2）留給定理 3.2 那一拍，
  因為唯一性的重點正好需要一個重根。

## 這一輪抓到的錯

**歸納那一拍第一版畫錯了。** 原本三個維度都用 A，而 A 限制在 α ₁ 的正交補上就是 2 倍恆等，
所以 T ξ 與 ξ 必然共線——為了讓兩支箭頭不重疊，第一版把 T ξ 畫在平面「下面」一點，
結果畫面在說「T ξ 掉出那個平面」，剛好跟這一拍要證的事相反。
**修法不是改畫法而是改例子**：換成特徵值 5、3、1 的自伴變換，T ξ 與 ξ 自然不共線，
兩支箭頭可以都畫在平行四邊形裡面。`bounds` 與 `collide` 對這種錯完全無感。

**兩條平行線讀成一條斷掉的線。** 半純量積退化的那一拍，( P ξ , ξ ) = 1 的解是兩條平行線；
第一版把它們畫得太開，被畫框裁成一段在左上、一段在右下的兩截，
沿同一條斜向帶排列——看起來就是一條中間斷掉的線（**E67 的切線那次是同一類**）。
把尺度縮到 0.52 倍，兩段在 x 方向重疊，才讀得出是「兩條平行線」。

**特徵值那一拍的圖改了兩次，第二次是 1080p 才看出來的。** 第一版把 ( T ξ , ξ ) 畫成極座標圖，
半徑寫成 `0.62 + 0.30 * q / λ ₁`——變化幅度 0.30 而底是 0.62，出來是兩個幾乎同心的圓，什麼都讀不到。
第二版把底拿掉、半徑直接等於 `q / λ ₁`，480p 幀上看起來像個花生，過了。
**可是 1080p 上它讀成一個交叉的「8」**：λ ₂ / λ ₁ = 0.283，腰身細到兩側幾乎相碰，
看起來像曲線自己穿過原點——也就是像「這個值會變號」，正好跟這一拍要講的相反。
**第三版換掉座標系**：改畫 q 對方向角的函數圖，兩條虛線標 λ ₁ 與 λ ₂，
曲線在兩條之間起伏、只在兩個點碰到上面那條。沒有任何誤讀的空間。
**規則：極座標圖只適合 max / min 比值不大的量；比值一大，腰身就會讀成自交。**

**長條圖沒有圖例。** 兩種顏色的長條配在一起，右側的表卻兩欄同色，讀者無從對上。
補了兩段色條加符號的圖例。

**三張圖伸進註腳。** 特徵值、定理 3.2、轉九十度三拍的座標軸或圓伸到 y = −1.2 以下，
壓在第一行註腳上。`collide` 沒有報（線很細），是看 480p 幀看出來的。

**歸納那一拍的 ξ 標籤壓在自己的箭頭上**，也是 1080p 才看得出來——480p 上那個字小到看不出壓著。
把整張圖放大到 0.68 倍、標籤再往上挪 0.32，才分得開。
**這一集因此渲染了兩次**（第一次 55 分鐘），兩件事都是 `bounds` 與 `collide` 看不到的。

---

## Beat 0 — 自伴的定義 / what self-adjoint means
*配音長度：中文 20.5s ／ 英文 16.6s*

**畫面公式**

```
自伴的定義   |   what self-adjoint means
( T α , β )    =    ( α , T β )
```

**旁白（繁中）**

> V 是準 Hilbert 空間時，Hom V 裡的 T 叫自伴，如果對每一對 α、β 都有 (Tα, β) = (α, Tβ)。全體自伴變換記作 S A。換句話說，T 可以從內積的左邊搬到右邊，而且不留下任何痕跡。

**Narration (EN)**

> If V is a pre-Hilbert space, an element T of Hom V is called self-adjoint when the product of T alpha with beta equals the product of alpha with T beta, for every pair. T can be moved from one side of the scalar product to the other, leaving no trace.

**動畫**

α 與 β 兩支箭頭，加上細箭頭畫的 T α 與 T β。右側四列：自伴的 S 上下兩列都是 2.9680，換成 N 之後是 1.5380 對 2.7040，差 1.1660。

---

## Beat 1 — 在共軛空間裡的同一句話 / the same sentence inside the dual
*配音長度：中文 18.8s ／ 英文 17.4s*

**畫面公式**

```
在共軛空間裡的同一句話   |   the same sentence inside the dual
T * ∘ θ    =    θ ∘ T
```

**旁白（繁中）**

> 自伴其實是說：在 V 嵌入 V 星的那個映射 θ 底下，T 變成自己的伴隨。因為 (α, β) 就是 θ β 作用在 α 上，把定義的兩邊都改寫成泛函，得到的正是 T 星合成 θ 等於 θ 合成 T。

**Narration (EN)**

> Self-adjointness says T becomes its own adjoint under the injection theta of V into V star. Since the product of alpha and beta is theta beta applied to alpha, rewriting both sides as functionals gives T star composed with theta equals theta composed with T.

**動畫**

V 與 V 星四個方塊組成的交換方塊：上排是 T，下排是 T 星，兩側是 θ。右側把兩條路徑各算一次，都得到 2.9680。

---

## Beat 2 — 引理 3.1：矩陣對稱 / lemma 3.1: a symmetric matrix
*配音長度：中文 19.0s ／ 英文 20.4s*

**畫面公式**

```
引理 3.1：矩陣對稱   |   lemma 3.1: a symmetric matrix
t ᵢⱼ   =   t ⱼᵢ            ( φ ᵢ , φ ⱼ )  =  δ ᵢⱼ
```

**旁白（繁中）**

> 引理 3.1：V 是有限維 Hilbert 空間、那組 φ 是正交規範基時，T 自伴的充要條件是它對這組基的矩陣對稱。證明是把 α 與 β 的基底展開代進去，兩邊比對，條件就變成 t i j 等於 t j i。

**Narration (EN)**

> Lemma 3.1: if V is a finite-dimensional Hilbert space and the phis are an orthonormal basis, then T is self-adjoint exactly when its matrix in that basis is symmetric. Substituting the basis expansions and expanding turns the condition into t i j equals t j i.

**動畫**

兩個 2 × 2 矩陣。左邊對標準基（正交規範）是 2.0、0.8、0.8、1.2，對稱；右邊對 b ₁ = ⟨1,0⟩、b ₂ = ⟨0,2⟩ 是 2.0、1.6、0.4、1.2，不對稱。兩個是同一個 T。

---

## Beat 3 — 非負與半純量積 / nonnegative, and a semiscalar product
*配音長度：中文 21.3s ／ 英文 19.4s*

**畫面公式**

```
非負與半純量積   |   nonnegative, and a semiscalar product
[ ξ , η ]  =  ( T ξ , η )            ( T ξ , ξ )  ≥  0
```

**旁白（繁中）**

> 自伴的 T 如果對每個 ξ 都有 (Tξ, ξ) 大於等於零，就叫非負。這時候把 [ξ, η] 定成 (Tξ, η)，得到的是一個半純量積：對稱來自自伴，非負來自這個條件，而「半」是因為可能有非零向量長度為零。

**Narration (EN)**

> A self-adjoint T is called nonnegative when the product of T xi with xi is at least zero for every xi. Then the bracket of xi and eta, defined as the product of T xi with eta, is a semiscalar product: symmetric because T is self-adjoint, nonnegative by assumption.

**動畫**

左圖是 ( S ξ , ξ ) = 1 的橢圓；右圖是 ( P ξ , ξ ) = 1，退化成兩條平行線，中間那支紅箭頭 w = ⟨1,−1⟩ 的長度是 0.0000。

---

## Beat 4 — 引理 3.2 / lemma 3.2
*配音長度：中文 18.6s ／ 英文 20.2s*

**畫面公式**

```
引理 3.2   |   lemma 3.2
‖ T ξ ‖ ²     ≤     ‖ T ‖  ( T ξ , ξ )
```

**旁白（繁中）**

> 引理 3.2：T 非負而且自伴時，‖Tξ‖ 的平方不超過 ‖T‖ 乘上 (Tξ, ξ)。證明是對那個半純量積用 Schwarz 不等式，取 η 等於 Tξ。推論非常有用：(Tξ, ξ) 一等於零，Tξ 就被逼成零。

**Narration (EN)**

> Lemma 3.2: if T is nonnegative as well as self-adjoint, the squared norm of T xi is at most the norm of T times the product of T xi with xi. The proof applies Schwarz to that semiscalar product, with eta taken to be T xi. So T xi vanishes whenever that number does.

**動畫**

四對長條：青綠是 ‖ T ξ ‖ ²，紫是 ‖ T ‖ ( T ξ , ξ )。前三對右邊明顯高，最後一對（ξ = α ₁）兩根一樣高 6.2222。

---

## Beat 5 — 特徵值：單位球面上的最大值 / eigenvalues: a maximum on the sphere
*配音長度：中文 20.5s ／ 英文 19.0s*

**畫面公式**

```
特徵值：單位球面上的最大值   |   eigenvalues: a maximum on the sphere
T ( α )  =  c  α              m  =  lub  ( T ξ , ξ )
```

**旁白（繁中）**

> 特徵向量與特徵值的定義：α 不是零，而 T α 等於某個 c 乘 α。要把它找出來，書上看的是 (Tξ, ξ) 這個函數在單位球面上的樣子——它連續，球面有界閉所以緊緻，上確界 m 一定在某個 α 上取到。

**Narration (EN)**

> Now the definitions: alpha is an eigenvector with eigenvalue c when alpha is nonzero and T alpha is c times alpha. To produce one, the book studies the function sending xi to the product of T xi with xi on the unit sphere, continuous on a set that is bounded and closed.

**動畫**

( T ξ , ξ ) 隨方向轉一圈的變化曲線：兩條虛線是 λ ₁ 與 λ ₂ 那兩個高度，曲線在兩條之間起伏，只在 ± α ₁ 兩個方向碰到上面那條。右側是取樣 12、360、3600 的最大值與它離 λ ₁ 的差。

---

## Beat 6 — 定理 3.1 的關鍵一步 / the step theorem 3.1 turns on
*配音長度：中文 18.6s ／ 英文 18.6s*

**畫面公式**

```
定理 3.1 的關鍵一步   |   the step theorem 3.1 turns on
( ( m − T ) α , α )  =  0        ⇒        T α  =  m α
```

**旁白（繁中）**

> 關鍵的一步：m 減 T 是非負的自伴變換，而「(Tα, α) 等於 m」恰好就是「((m − T)α, α) 等於零」。引理 3.2 於是逼出 T α 等於 m α：那個最大值點自己就是特徵向量。

**Narration (EN)**

> The key step: m minus T is a nonnegative self-adjoint transformation, and saying that the product of T alpha with alpha equals m is exactly saying that m minus T applied to alpha, paired with alpha, is zero. Lemma 3.2 then forces T alpha to be m alpha.

**動畫**

單位圓上每隔六度一根刺，長度是 ( ( m − T ) ξ , ξ )。刺處處朝外（非負），只在 ± α ₁ 那兩個橘點縮成零。

---

## Beat 7 — 歸納：正交補不變 / the induction: the complement is invariant
*配音長度：中文 20.6s ／ 英文 20.4s*

**畫面公式**

```
歸納：正交補不變   |   the induction: the complement is invariant
ξ  ⊥  α ₁         ⇒         T ξ  ⊥  α ₁
```

**旁白（繁中）**

> 接著是歸納。取 V 2 為 α 1 的正交補，它在 T 底下不變：ξ 垂直 α 1 時，(Tξ, α 1) 等於 (ξ, Tα 1)，也就是 m 乘零。在 V 2 上重做同一件事，最後得到全由特徵向量組成的正交規範基。

**Narration (EN)**

> Then induction. Let V two be the orthogonal complement of alpha one. It is carried into itself by T, since for xi perpendicular to alpha one the product of T xi with alpha one is the product of xi with T alpha one, which is m times zero. Repeating gives an orthonormal eigenbasis.

**動畫**

平面 V ₂ 畫成一個平行四邊形，α ₁ 是垂直出來的箭頭。ξ 與 T ξ 兩支箭頭方向不同，可是都躺在那個平行四邊形裡。這一拍的 T 特徵值是 5、3、1。

---

## Beat 8 — 定理 3.2：分解唯一 / theorem 3.2: the decomposition is unique
*配音長度：中文 20.9s ／ 英文 21.3s*

**畫面公式**

```
定理 3.2：分解唯一   |   theorem 3.2: the decomposition is unique
V   =   ⊕ ⱼ M ⱼ             T | M ⱼ   =   λ ⱼ  I
```

**旁白（繁中）**

> 把相同的特徵值歸成一組：M j 是特徵值等於 λ j 的基向量張成的子空間。它們互相正交、直和是 V，T 限制在 M j 上就是 λ j 乘恆等。引理 3.3 說每個特徵向量都落在某個 M j 裡，所以 M j 唯一。

**Narration (EN)**

> Group the equal eigenvalues: M j is spanned by those basis vectors whose eigenvalue is lambda j. These subspaces are orthogonal, their sum is V, and T restricted to each one is that scalar times the identity. Lemma 3.3 puts every eigenvector inside one of them, so they are unique.

**動畫**

M ₂ 畫成一個圓，裡面兩組正交規範對：青綠的 u、v 與轉了 0.7 弧度的紅色 u ′。兩組都是特徵向量，( u , u ′ ) = 0.7648。

---

## Beat 9 — 特徵基底把計算變成算術 / an eigenbasis turns it into arithmetic
*配音長度：中文 19.2s ／ 英文 18.5s*

**畫面公式**

```
特徵基底把計算變成算術   |   an eigenbasis turns it into arithmetic
P ( T )  β ᵢ     =     P ( r ᵢ )  β ᵢ
```

**旁白（繁中）**

> 有了特徵向量組成的基，計算全部退化成一串數字。T 平方的特徵向量一樣，特徵值變平方；T 的反元素存在的充要條件是沒有特徵值等於零；任何多項式 P 都把 β i 送成 P(r i) 乘 β i。

**Narration (EN)**

> With a basis of eigenvectors every computation collapses to a list of numbers. T squared has the same eigenvectors with squared eigenvalues, the inverse exists exactly when no eigenvalue is zero, and any polynomial P sends beta i to P of r i times beta i.

**動畫**

一個 2 × 4 的數字格：列是兩個特徵值，欄是 T、T ²、T ⁻ ¹、P ( T )，內容是 5 / 25 / 0.2 / 11 與 2 / 4 / 0.5 / −1。下面是 P ( t ) = t ² − 3 t + 1。

---

## Beat 10 — 沒有自伴就可能一個都沒有 / without it there may be none at all
*配音長度：中文 21.4s ／ 英文 20.0s*

**畫面公式**

```
沒有自伴就可能一個都沒有   |   without it there may be none at all
λ ²  +  1   =   0             λ   =   ±  i
```

**旁白（繁中）**

> 可是一般的 T 可能一個特徵向量都沒有。平面上轉九十度就是：特徵多項式是 λ 平方加一，在實數上不可約。換到複二維空間，特徵值就成了正負 i。定理 3.3 收尾：特徵值恰好是極小多項式的根。

**Narration (EN)**

> But an arbitrary T need not have an eigenvector. The rotation of the plane by ninety degrees is the example: its characteristic polynomial is lambda squared plus one, with no real root, though over complex two-space the eigenvalues are plus and minus i. Theorem 3.3 then closes.

**動畫**

單位圓上三個方向的 ξ 與它們的像 R ξ，每一對都成直角。右側：max | ( R ξ , ξ ) | = 0.0e+00，min ‖ R ξ − ( R ξ , ξ ) ξ ‖ = 1.0000。
