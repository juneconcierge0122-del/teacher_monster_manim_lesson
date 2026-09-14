# advcalc E72 — 第 5 章：正交變換

Chapter 5: Orthogonal Transformations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 4 節「正交變換」（書頁 262–263），**整節一集講完**。

習題 4.1–4.8 在書頁 263–264（依 PLAYBOOK 第 8 節不做解答），**§5「緊變換」從書頁 264 起，整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e72_orthogonal.py`（`AdvCalcE72ZH` / `AdvCalcE72EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[72]` / `FORMULAS_ADVCALC[72]`）
- 配音：`manim_lessons/samples/audio_e72/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 199.8 秒配音／英文 209.1 秒配音

## 這一節的兩件事

**第一件：把伴隨搬回 V 裡。** 第 2 節收在定理 2.4——θ 是同構的充要條件是 V 完備。
所以 V 是 Hilbert 空間時 θ 可逆，`Hom V *` 裡的伴隨就可以共軛回來：

```
θ ⁻ ¹ ∘ T * ∘ θ   ∈   Hom V
```

Hilbert 空間理論說的伴隨指的是**這個**。搬回來之後它由 ( T α , β ) = ( α , T * β ) 唯一決定，
矩陣是轉置，而「T 自伴」就簡化成一行 T = T *。書上還給了一個不繞共軛空間的直接定義：
固定 η，泛函 ξ ↦ ( T ξ , η ) 由唯一一個 β 代表，而 η ↦ β 就是 T *。

**第二件：正交變換。** T 正交的意思是保純量積，用伴隨恆等式改寫一次就等價於 **T * T = I**。
保純量積就保長度，所以單射，有限維時即可逆，而可逆之後條件寫成 T * = T ⁻ ¹。
寫成矩陣是各欄正交規範（定理 4.1）。接著兩個定理把上一集接過來：

- **定理 4.2**：對稱的 t 一定有正交的 b 使 b ⁻ ¹ t b 對角——就是 E71 的譜定理換個說法。
- **定理 4.3（極分解）**：可逆的 T 都寫成 R S，R 正交、S 自伴而且正。
  關鍵是 T * T 的特徵值 r ᵢ = ‖ T φ ᵢ ‖ ²，T 可逆時全都嚴格大於零，所以正的平方根 S 存在；
  然後 **S T ⁻ ¹ 正交**（五個等號），於是 T = ( S T ⁻ ¹ ) ⁻ ¹ S。

收在推論：任何非奇異矩陣 t = u d v，u 與 v 正交、d 對角。

## 這一集的具體數字

一個矩陣撐起大半集：**T = [[2, 0.6], [−0.4, 1.5]]**，可逆、既不對稱也不正交。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 伴隨恆等式 | ( T α , β ) 對 ( α , T * β ) | 兩邊都是 1.5940 |
| T 不自伴 | max \| t ᵢⱼ − t ⱼᵢ \| | 1.0000 |
| 泛函由唯一一個 β 代表 | 三個不同的 ξ | ( T ξ , η ) 與 ( ξ , β ) 逐列相同 |
| 泛函有界 | 單位圓上取樣 1440 個方向 | 上界 2.2078 = ‖ β ‖ |
| 正交保純量積 | 轉 0.6 弧度的 R、鏡射 F | 都是 1.1800 = ( α , β ) |
| 不正交的樣子 | N = diag(1.8, 0.5) | 1.4910 ≠ 1.1800 |
| 鏡射也是正交 | det R、det F | + 1 與 − 1 |
| 保長度 | 三個 α 的 ‖ α ‖ 與 ‖ R α ‖ | 逐列相同到 1e-12 |
| T * = T ⁻ ¹ | 轉置與反矩陣逐項比 | 0.0e+00 |
| 定理 4.1 | 三個矩陣的兩欄長度與內積 | rot／ref 是 1、1、0；dia 是 1.8、0.5、0 |
| 定理 4.2 | E71 的 [[2, 0.8], [0.8, 1.2]] | b ⁻ ¹ t b = diag(2.494427, 0.705573) |
| b ⁻ ¹ 就是轉置 | max \| b ⁻ ¹ ᵢⱼ − t * ᵢⱼ \| | 0.0e+00 |
| T * T 的特徵值是正的 | r ᵢ 對 ‖ T φ ᵢ ‖ ² | 4.365115 與 2.404885，兩欄相同 |
| S 是正的平方根 | max \| ( S ² ) ᵢⱼ − ( T * T ) ᵢⱼ \| | 4.0e-15 |
| S T ⁻ ¹ 正交 | 五個等號逐步算 | 每一步都是 1.1800 |
| T = R S | max \| ( R S ) ᵢⱼ − t ᵢⱼ \| | 4.4e-16，R 轉 −15.9454 度 |
| 兩個順序真的不同 | max \| ( T T * ) ᵢⱼ − ( T * T ) ᵢⱼ \| | 0.5000 |
| 推論 t = u d v | 三個因子乘回去 | 誤差 4.4e-16，d = diag(2.0893, 1.5508) |

**畫面的主角是「單位圓的像」。** 一個 2 × 2 矩陣長什麼樣子，畫它把單位圓送到哪裡最清楚：
正交的就送回圓，不正交的壓成橢圓，而極分解那三拍就是把橢圓拆成
「先撐開（S）再轉（R）」——三格並排，中間那一步是唯一改變形狀的。
第八拍的兩個半軸長 2.0893 與 1.5508 正好就是最後一拍 d 對角線上那兩個數。

## 這一輪抓到的錯

**英文第 10 拍的配音只有 7.2 秒。** 那一行有 276 個字元，應該是 19 秒左右。
`generate_advcalc_tts.py` 跑到一半被工具的 120 秒逾時搬到背景，最後一個 mp3 就寫壞了
（`av.open` 直接丟 `InvalidDataError`）。**規則：配音生成完一定要逐檔量長度，
不能只數檔案數**——11 個檔案都在，其中一個是壞的。重跑英文那一輪就好。

**兩支箭頭差 20 度就等於疊在一起。** 第二拍原本要畫 η 與 β = T * η 兩支箭頭，
可是這個 T * 的旋轉成分只有 16 度左右，兩支在 0.42 的尺度下完全分不開
（**E68 的 step function、E71 的 T ξ 都是同一類**）。
換成 Riesz 的標準圖：單位圓、β 的方向，以及 ( ξ , β ) = 1 那條虛線——
它垂直於 β、離原點 1 / ‖ β ‖，泛函愈大線就愈靠近原點。這張圖比兩支箭頭說得更多。

**「不正交」的反例差點看不出不正交。** 第一版用 N = diag(1.2, 0.8)，
內積 1.0752 對 1.1800 差不到 10%，畫面上單位圓的像幾乎還是圓。
換成 diag(1.8, 0.5)：內積 1.4910，而且圓被壓成明顯的扁橢圓。
**反例要挑到「錯得看得見」的程度。**

**單位球面不能叫 S。** 前三格的第一格原本標 `S`（想當成單位球面），
可是 S 在這一集正是極分解裡那個自伴的正因子——同一集裡同一個字母兩個意思。
改標 `‖ ξ ‖ = 1`。

**四個 `.replace(...)` 的假造字串。** 草稿裡想在符號列裡塞中文註解，
又知道 langscan 會抓，就寫成 `"... ( 定理 2 . 4 )".replace("( 定理 2 . 4 )", "")` 這種東西——
**和 `if False else` 完全同一類的殘留**，只是換了手法。寫完場景檔就一起 grep 掉。

**`langscan` 的白名單加了 `diag`。** 它跟 `det`、`dim` 一樣是運算子名稱，
中英文都寫成 `diag`，不是「有一半觀眾會讀錯的字」。加完回頭補掃
E49、E50、E52、E66–E71 都還是 0。

---

## Beat 0 — 把伴隨搬回 V 裡 / bringing the adjoint back into V
*配音長度：中文 17.1s ／ 英文 18.3s*

**畫面公式**

```
把伴隨搬回 V 裡   |   bringing the adjoint back into V
θ ⁻ ¹ ∘ T * ∘ θ          ( T α , β )  =  ( α , T * β )
```

**旁白（繁中）**

> V 是 Hilbert 空間時，θ 從 V 到 V 星是同構（定理 2.4），所以可以把 Hom V 星裡的 T 星換成 θ 反 合成 T 星 合成 θ，它落在 Hom V 裡。這個映射才是 Hilbert 空間理論說的伴隨。

**Narration (EN)**

> When V is a Hilbert space, theta from V to V star is an isomorphism by Theorem 2.4, so the adjoint living in Hom V star can be replaced by theta inverse composed with it composed with theta, which lands in Hom V. Hilbert space theory calls that map the adjoint of T.

**動畫**

V 與 V 星四個方塊組成的交換方塊：上排標 θ ⁻ ¹ ∘ T * ∘ θ，下排是 V 星裡的 T *，左側是 θ、右側是 θ ⁻ ¹（往上）。右側驗 ( T α , β ) = ( α , T * β ) = 1.5940。

---

## Beat 1 — 不繞共軛空間的定義 / the definition without the dual
*配音長度：中文 20.0s ／ 英文 20.7s*

**畫面公式**

```
不繞共軛空間的定義   |   the definition without the dual
( T ξ , η )   =   ( ξ , β )              β   =   T * η
```

**旁白（繁中）**

> 也可以不繞共軛空間直接定義。固定 η，映射「ξ 送到 (Tξ, η)」線性而且有界，所以是 V 星的元素；定理 2.4 說它由唯一一個 β 給出。而 η 送到 β 本身也是線性有界的，那就是 T 星。

**Narration (EN)**

> There is also a direct definition. Fix eta; the map sending xi to the product of T xi with eta is linear and bounded, so it is an element of the conjugate space, and Theorem 2.4 says a unique vector represents it. That correspondence is itself linear and bounded: it is T star.

**動畫**

單位圓、β 那支箭頭，以及 ( ξ , β ) = 1 那條虛線——它垂直於 β，離原點 1 / ‖ β ‖ = 0.4529。右側三個不同的 ξ 兩欄都相等，上界 2.2078 正好是 ‖ β ‖。

---

## Beat 2 — T 星的矩陣是轉置 / the matrix of the adjoint is the transpose
*配音長度：中文 17.3s ／ 英文 19.2s*

**畫面公式**

```
T 星的矩陣是轉置   |   the matrix of the adjoint is the transpose
t * ᵢⱼ    =    t ⱼᵢ
```

**旁白（繁中）**

> 引理 3.1 的矩陣計算一字不改地推廣過來：T 星在 Hom V 裡的矩陣，就是 T 的矩陣的轉置。T 自伴因此等價於 T 等於 T 星，也就等價於矩陣等於自己的轉置——正是上一集那個對稱。

**Narration (EN)**

> The matrix calculations of Lemma 3.1 generalise verbatim: the matrix of T star in Hom V is the transpose of the matrix of T. So T is self-adjoint exactly when T equals T star, which is exactly when its matrix equals its own transpose, last episode's symmetry.

**動畫**

兩個 2 × 2 矩陣與中間一支箭頭：t = [[2.0, 0.6], [−0.4, 1.5]] 轉置成 t * = [[2.0, −0.4], [0.6, 1.5]]，下面標出 t ₁₂ = 0.6 與 t * ₂₁ = 0.6。

---

## Beat 3 — 正交的定義 / what orthogonal means
*配音長度：中文 19.1s ／ 英文 18.4s*

**畫面公式**

```
正交的定義   |   what orthogonal means
( T α , T β )  =  ( α , β )        ⇔        T * T  =  I
```

**旁白（繁中）**

> 另一類很重要的變換是保純量積的。定義：T 叫正交，如果對每一對 α、β 都有 (Tα, Tβ) = (α, β)。用剛才那個伴隨恆等式改寫，它完全等價於 T 星 T 等於恆等。

**Narration (EN)**

> Another important type of transformation is one preserving the scalar product. Definition: T is orthogonal when the product of T alpha with T beta equals the product of alpha with beta for every pair. By the adjoint identity that is equivalent to T star T being the identity.

**動畫**

左右兩張圖：左邊 R 轉 0.6 弧度，α、β 與它們的像；右邊 N = diag(1.8, 0.5)，同一對向量被拉歪。右側四列內積，前三列都是 1.1800，第四列 1.4910。

---

## Beat 4 — 保長度 ⟹ 單射 / norms preserved, so injective
*配音長度：中文 14.9s ／ 英文 18.4s*

**畫面公式**

```
保長度 ⟹ 單射   |   norms preserved, so injective
‖ T α ‖ ²  =  ‖ α ‖ ²                T *  =  T ⁻ ¹
```

**旁白（繁中）**

> 正交的 T 一定單射，因為 ‖Tα‖ 的平方等於 ‖α‖ 的平方；V 有限維時單射就可逆。不論 V 有限維或不，只要 T 真的可逆，那個條件就寫成 T 星等於 T 的反元素。

**Narration (EN)**

> An orthogonal T is injective, since the squared norm of T alpha equals the squared norm of alpha, and in finite dimensions injective means invertible. Whether V is finite-dimensional or not, if T is invertible the condition becomes T star equals T inverse.

**動畫**

左邊 R 把單位圓送回單位圓（兩條線重合），右邊 N 把它壓成一個扁橢圓。右側三個 α 的 ‖ α ‖、‖ R α ‖、‖ N α ‖，前兩欄逐列相同。

---

## Beat 5 — 定理 4.1：各欄正交規範 / theorem 4.1: orthonormal columns
*配音長度：中文 17.4s ／ 英文 19.8s*

**畫面公式**

```
定理 4.1：各欄正交規範   |   theorem 4.1: orthonormal columns
Σ ₖ t ₖᵢ t ₖⱼ    =    δ ᵢⱼ
```

**旁白（繁中）**

> 在 Hom R n 裡，這個條件寫成矩陣就是 t 的轉置乘 t 等於單位矩陣，逐項就是第 i 欄與第 j 欄的內積等於 δ i j。定理 4.1：T 正交的充要條件是標準基的像又是一組正交規範基。

**Narration (EN)**

> In Hom R n the condition reads as the transpose of t times t being the identity matrix, which entry by entry says that the product of column i with column j is the Kronecker delta. Theorem 4.1: T is orthogonal exactly when the standard basis goes to another orthonormal basis.

**動畫**

單位圓上的 δ ¹、δ ² 與它們的像 T δ ¹、T δ ²（兩支粗箭頭，落在圓上、互相垂直）。右側三個矩陣的兩欄長度與內積：rot 與 ref 都是 1、1、0，dia 是 1.8、0.5、0。

---

## Beat 6 — 定理 4.2：對稱可正交對角化 / theorem 4.2: symmetric means diagonalisable
*配音長度：中文 19.9s ／ 英文 19.2s*

**畫面公式**

```
定理 4.2：對稱可正交對角化   |   theorem 4.2: symmetric means diagonalisable
b ⁻ ¹  t  b   =   d                b * b  =  I
```

**旁白（繁中）**

> 定理 4.2：對稱矩陣 t 一定存在正交矩陣 b，使得 b 反 t b 是對角的。證明就用上一集：t 給的 T 自伴，所以有正交規範的特徵基；把 b 的各欄取成那些特徵向量，b 就正交，對角線上就是特徵值。

**Narration (EN)**

> Theorem 4.2: for a symmetric matrix there is an orthogonal matrix conjugating it into a diagonal one. The proof is last episode's: the transformation is self-adjoint, so it has an orthonormal eigenbasis, and taking those eigenvectors as the columns makes that matrix orthogonal.

**動畫**

左邊是 b 的兩欄（E71 那組特徵向量）畫在單位圓上；右邊是 b ⁻ ¹ t b 這個矩陣，對角線 2.4944 與 0.7056，非對角 0.0000。

---

## Beat 7 — T 星 T 的特徵值都是正的 / the eigenvalues of T*T are positive
*配音長度：中文 19.6s ／ 英文 20.1s*

**畫面公式**

```
T 星 T 的特徵值都是正的   |   the eigenvalues of T*T are positive
( T * T ) *  =  T * T            S ²  =  T * T ,     S  >  0
```

**旁白（繁中）**

> 定理 4.3 的準備。對任何 T，T 星 T 都是自伴的。取它的正交規範特徵基，特徵值 r i 等於 ‖T φ i‖ 的平方，T 可逆時全都嚴格大於零，所以可以定義正的平方根 S：它自伴，平方就是 T 星 T。

**Narration (EN)**

> Preparation for Theorem 4.3. For any T the product T star T is self-adjoint. Take its orthonormal eigenbasis; each eigenvalue is the squared norm of T applied to that basis vector, so when T is invertible all of them are strictly positive, and a positive square root S can be defined.

**動畫**

T 把單位圓拉成的橢圓，兩支箭頭是它的兩個半軸 2.0893 與 1.5508；右邊是 T * T 這個矩陣。右側把 r ᵢ 與 ‖ T φ ᵢ ‖ ² 並排，逐列相同。

---

## Beat 8 — 五個等號 / five moves across the product
*配音長度：中文 16.6s ／ 英文 17.8s*

**畫面公式**

```
五個等號   |   five moves across the product
( S T ⁻ ¹ α , S T ⁻ ¹ β )    =    ( α , β )
```

**旁白（繁中）**

> 關鍵是 A = S T 反 這個變換正交。驗算是一串五個等號：把 S 搬過去變成 S 的平方，那就是 T 星 T，再把 T 星 搬過去、T 與 T 反 消掉，最後剩下 (α, β)。

**Narration (EN)**

> The key step is that S composed with T inverse is orthogonal. The check is a chain of five equalities: move S across to get S squared, which is T star T, then move T star across, cancel T against T inverse, and what is left is the product of alpha and beta.

**動畫**

三格：單位圓 → T ⁻ ¹ 拉成的橢圓 → 再作用 S 之後又是圓。右側把證明的五個等號逐步列出，每一步都是 1.1800。

---

## Beat 9 — 定理 4.3：極分解 / theorem 4.3: the polar decomposition
*配音長度：中文 18.5s ／ 英文 18.8s*

**畫面公式**

```
定理 4.3：極分解   |   theorem 4.3: the polar decomposition
T    =    R  S    =    S ′ R ′
```

**旁白（繁中）**

> 於是 T = A 反 S，取 R = A 反，就得到定理 4.3：有限維 Hilbert 空間上任何可逆的 T 都寫成 R S，R 正交、S 自伴而且正。這個分解唯一；從 T T 星 出發會得到另一個順序 T = S R。

**Narration (EN)**

> So T is that map's inverse composed with S, and calling the inverse R gives Theorem 4.3: any invertible T on a finite-dimensional Hilbert space is an orthogonal map times a positive self-adjoint one. It is unique, and starting from T T star gives the other order.

**動畫**

三格：單位圓 → S 撐成的橢圓 → R 再把它轉 −15.95 度，就是 T 的像。右側驗 ‖ R S − t ‖ = 4.4e-16，並顯示 T T * 與 T * T 差 0.5000。

---

## Beat 10 — 推論：t = u d v / the corollary
*配音長度：中文 19.4s ／ 英文 18.6s*

**畫面公式**

```
推論：t = u d v   |   the corollary
t   =   u  d  v            u * u  =  v * v  =  I
```

**旁白（繁中）**

> 書上叫這些極分解，因為它們的作用像複數的 z 等於 r 乘 e 的 i θ 次方。推論：任何非奇異的矩陣 t 都寫成 u d v，u 與 v 正交、d 對角。證明是把 t = r s 裡的對稱 s 用定理 4.2 對角化。

**Narration (EN)**

> The book calls these the polar decompositions, since they function somewhat like the polar factorisation of a complex number. Corollary: any nonsingular matrix is an orthogonal matrix times a diagonal one times another orthogonal matrix, by diagonalising the symmetric factor.

**動畫**

三格：v 作用完還是圓 → d v 把它壓成軸對齊的橢圓 → u d v 轉成 t 的橢圓。右側 d = diag(2.0893, 1.5508)，三個誤差都在 1e-15 等級。
