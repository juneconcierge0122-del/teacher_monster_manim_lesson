# advcalc E70 — 第 5 章：正交投影（下）

Chapter 5: Orthogonal Projection II

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 2 節「正交投影」的後半（書頁 254–256），**第 2 節到此結束**。

習題 2.1–2.11 在書頁 256–257（依 PLAYBOOK 第 8 節不做解答），**§3「自伴變換」從書頁 257 起**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e70_orthonormal.py`（`AdvCalcE70ZH` / `AdvCalcE70EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[70]` / `FORMULAS_ADVCALC[70]`）
- 配音：`manim_lessons/samples/audio_e70/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.24 分（194 秒）／英文 3.16 分（189 秒）

## 全部從一個等式長出來

這一段的結構異常乾淨：**一個等式，往兩邊各讀一次。**

```
‖ ξ − σ ₙ ‖ ²   =   ‖ ξ ‖ ²  −  Σ ₁ ⁿ x ᵢ ²
```

部分和 σ ₙ 是 ξ 在前 n 個向量張成的空間上的投影（**上一集的引理 2.3 與 2.4**），
所以 ξ − σ ₙ 垂直於 σ ₙ，畢氏定理直接給出上式。

- **往左讀**：左邊是長度平方，不可能為負 ⟹ **Bessel 不等式**。
- **往右讀**：σ ₙ → ξ ⟺ Σ x ᵢ ² → ‖ ξ ‖ ² ⟹ **Parseval 條件**。

後面接**基底的定義**（每個元素都是自己 Fourier 級數的和）、**定理 2.3**（⟺ 線性包稠密）、
**推論**（Hilbert 空間裡 ⟺ 正交補只有零）、**正交基為什麼被偏愛**、
**引理 2.5 Gram–Schmidt**，最後是**定理 2.4**：θ 是同構 ⟺ V 完備。

## 這一集的具體例子

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 正交規範 | [0, π] 上的 sin k t 乘 √(2/π) | ‖φ₁‖ = 1.000000，(φ₁, φ₂) = -2e-17 |
| 那個等式 | n = 1 到 7 逐項算兩欄相加 | 每一列都是 3.141593 = π |
| Bessel | 部分和 | 2.5465 → 2.9832，都 < 3.1416 |
| Parseval 還沒到 | n = 7 的殘量 | ‖ξ − σ₇‖² = 0.1583 |
| 最佳近似 | 把係數乘 0.80／1.25 | 0.6522／0.6993 > 0.5587 |
| 不是基底的那一組 | 只取偶數正弦 | 係數全 ≤ 1e-16，Σx² = 5e-33 ≪ 3.1416 |
| 正交補不是零 | (φ₁, φ₂ₖ) | ≤ 1e-16，而 φ₁ ≠ 0 |
| Gram–Schmidt | 平面上一步 | (φ₂, α₁) = 0e+00 |
| 書上的例子 | 1、x、x² 遞迴正交化 | 1、x − 0.5000、x² − x + 0.1667 |
| θ 是等距 | 單位圓上取樣 1440 個方向 | sup = 1.3000，‖β‖ = 1.3000 |

**要展開的向量選常數函數 1，是為了讓收斂慢到畫得出來。** 它的 Fourier 正弦級數是經典的方波展開，
偶數項全為零、奇數項像 1/n 掉，所以 n = 7 時係數平方和才走到 2.9832，
離 π 還有 0.1583——**兩端翹起來的那一塊在畫面上看得見**。
如果選一個收斂很快的函數，這一拍就會變成「兩條線疊在一起」，什麼都讀不到。

**反例那一組（只有偶數正弦）是這一集最有用的一張圖**：它是正交規範的，Bessel 也照樣成立，
可是常數函數在它上面的係數**全部是零**，Parseval 差了整個 ‖ξ‖²。
這正好把「Bessel 對任何正交規範集都成立」與「Parseval 只對基底成立」分開，
也把推論裡那句「正交補只有零」畫成一條紅色的 φ₁。

## 這一輪抓到的錯

**`if False else` 第六集出現，三處。** 這次跟上次一樣，在跑四道檢查之前先
`grep -n "if False"` 抓掉——這個習慣現在是寫完場景檔的固定動作。
留下來的那些是純符號的版本（`Σ ₁ ⁿ x ᵢ ² + ‖ ξ − σ ₙ ‖ ² = 3.1416`、`min = 0.5587`、`‖ θ ᵦ ‖ = ‖ β ‖`），
否則其中兩處的中文會被 langscan 抓出來。

**公式列差點用到兩個沒驗過的字元。** 第一版寫了 `Σ ₁ ᪲`（想當成「和到無窮」）與 `⅙`，
可是 `᪲` 是組合用記號、`⅙` 在這個專案從來沒出現過。改成 `Σ ᵢ` 與 `1 / 6`。
**規則：公式列只用 `localization/advcalc.py` 裡已經出現過的字元**，要用新的就先 grep 一次確認別集用過。

`collide` 報了 8 處，都是老問題的變形：六列的表撞到圖說（改列距）、
投影的標籤壓在它落下去的那條直線上、單位圓伸進註腳、以及單位向量的標籤壓在橫軸上。

---

## Beat 0 — 正交規範 / orthonormal
*配音長度：中文 15.7s ／ 英文 14.5s*

**畫面公式**

```
正交規範   |   orthonormal
( φ ᵢ , φ ⱼ )  =  0            ‖ φ ᵢ ‖  =  1
```

**旁白（繁中）**

> 一組正交向量如果每一個長度都是一，就叫正交規範。把 [0, π] 上的 sin k t 各乘上根號二除以 π，就是這樣一組——這一集的計算大半就在它上面做。

**Narration (EN)**

> A collection of orthogonal vectors is called orthonormal when each has length one. Multiplying the sines on the interval from zero to pi by the square root of two over pi gives such a collection, and most of this episode computes with it.

**動畫**

[0, π] 上的三條正規化正弦 φ ₁、φ ₂、φ ₃；右側驗證每一條的長度都是 1.000000，而互相的內積都在 1e-16 等級或更小。

## Beat 1 — 定理 2.2 的那一行計算 / the one line theorem 2.2 turns on
*配音長度：中文 18.6s ／ 英文 17.3s*

**畫面公式**

```
定理 2.2 的那一行計算   |   the one line theorem 2.2 turns on
‖ ξ − σ ₙ ‖ ²    =    ‖ ξ ‖ ²  −  Σ ₁ ⁿ x ᵢ ²
```

**旁白（繁中）**

> 定理 2.2 的關鍵是一行計算。前 n 項的部分和是 ξ 在那 n 個向量張成的空間上的投影，所以 ξ 減部分和垂直於它，畢氏定理就給出：那個差的平方，等於 ξ 的平方減掉前 n 個係數的平方和。

**Narration (EN)**

> Theorem 2.2 turns on one line. The partial sum of the first n terms is the projection on the span of those n, so the difference is orthogonal to it, and Pythagoras gives: the square of the difference is the squared norm minus the sum of the squares of the coefficients.

**動畫**

一個直角三角形：兩股是 ‖ σ ₃ ‖ = 1.6821 與 ‖ ξ − σ ₃ ‖ = 0.5587，斜邊是 ‖ ξ ‖ = 1.7725。右側的表把 n = 1 到 5 的兩欄與它們的和列出來，最後一欄永遠是 3.1416。

## Beat 2 — Bessel 不等式 / Bessel's inequality
*配音長度：中文 16.1s ／ 英文 16.8s*

**畫面公式**

```
Bessel 不等式   |   Bessel's inequality
Σ ₁ ⁿ x ᵢ ²    ≤    ‖ ξ ‖ ²              ∀ n
```

**旁白（繁中）**

> Bessel 不等式立刻掉出來：左邊是一個長度平方，不可能是負的，所以前 n 個係數的平方和對每個 n 都不超過 ξ 的平方。那個級數因此收斂，而且和不超過 ξ 的長度平方。

**Narration (EN)**

> Bessel's inequality falls out at once: the left side is a squared length and cannot be negative, so the sum of the squares of the first n coefficients is at most the square of the vector, for every n. That series therefore converges, with sum at most the squared norm.

**動畫**

七根柱子畫出前 n 個係數的平方和，上面一條黃色虛線是 ‖ ξ ‖ ² = 3.1416。偶數項係數是零，所以柱子每隔一根才長高。

## Beat 3 — Parseval：級數什麼時候收斂到 ξ / Parseval: when the series gets there
*配音長度：中文 17.7s ／ 英文 14.9s*

**畫面公式**

```
Parseval：級數什麼時候收斂到 ξ   |   Parseval: when the series gets there
σ ₙ   →   ξ          ⇔          Σ ᵢ x ᵢ ²   =   ‖ ξ ‖ ²
```

**旁白（繁中）**

> 同一個等式反過來讀就是 Parseval：部分和收斂到 ξ 的充要條件，是係數平方和收斂到 ξ 的長度平方。書上把那個形式級數叫做 ξ 的 Fourier 級數，而 Parseval 條件說的就是它收不收斂。

**Narration (EN)**

> Reading the same identity the other way gives Parseval: the partial sums converge to the vector exactly when the sum of the squares of the coefficients converges to its squared norm. The formal series is called the Fourier series of that vector.

**動畫**

同樣七個 n，兩組點：青綠色的是係數平方和（往上），紅色的是 ‖ ξ − σ ₙ ‖ ²（往下），兩者相加永遠是那條虛線的高度。

## Beat 4 — 基底的定義 / what a basis means here
*配音長度：中文 15.6s ／ 英文 15.7s*

**畫面公式**

```
基底的定義   |   what a basis means here
ξ    =    Σ ᵢ x ᵢ φ ᵢ            ∀ ξ  ∈  V
```

**旁白（繁中）**

> 基底的定義跟著來：一個無窮的正交規範序列，如果 V 裡每個元素都是自己 Fourier 級數的和，就叫 V 的基底。注意這是「級數收斂到它」的意思，不是有限的展開。

**Narration (EN)**

> The definition of a basis follows. An infinite orthonormal sequence is a basis for the space if every element is the sum of its own Fourier series. Note that this means the series converges to it, not that there is a finite expansion.

**動畫**

常數函數 ξ 畫成黃色虛線，三條曲線是 n = 1、3、7 的部分和——兩端翹起來的地方就是還沒追上的部分。

## Beat 5 — 定理 2.3：線性包稠密就夠了 / theorem 2.3: a dense span is enough
*配音長度：中文 18.5s ／ 英文 19.4s*

**畫面公式**

```
定理 2.3：線性包稠密就夠了   |   theorem 2.3: a dense span is enough
L ( { φ ᵢ } ) ‾    =    V
```

**旁白（繁中）**

> 定理 2.3：正交規範序列是基底的充要條件，是它的線性包稠密。證明很短：稠密給出某個有限組合能把 ξ 近似到 ε 以內，而同樣長度的 Fourier 部分和是最佳近似，所以只會更近。

**Narration (EN)**

> Theorem 2.3: an orthonormal sequence is a basis exactly when its linear span is dense. The proof is short: density gives a finite combination within epsilon of the vector, and the Fourier partial sum of the same length is the best approximation, so it can only be closer.

**動畫**

同一張圖：青綠色那條是 Fourier 部分和 σ ₃，兩條細的是把係數乘上 0.80 與 1.25 之後的樣子，右側列出三個距離，Fourier 那個最小。

## Beat 6 — 推論：正交補只有零 / the corollary: nothing but zero is orthogonal
*配音長度：中文 17.4s ／ 英文 19.5s*

**畫面公式**

```
推論：正交補只有零   |   the corollary: nothing but zero is orthogonal
{ φ ᵢ } ⊥   =   { 0 }
```

**旁白（繁中）**

> 推論：V 是 Hilbert 空間時，基底的充要條件是那組向量的正交補只有零。理由是取線性包的閉包 M，用 V = M 直和 M 的正交補，再加上引理 1.1——正交補只跟那組向量有關。

**Narration (EN)**

> The corollary: in a Hilbert space the sequence is a basis exactly when its orthogonal complement is zero. Take the closure of the linear span, use the decomposition into it and its complement, and add Lemma 1.1, which says the complement depends only on the vectors themselves.

**動畫**

只取偶數的那一組（φ ₂、φ ₄）加上紅色的 φ ₁。右側列出常數函數對偶數項的係數全是 1e-16 等級、平方和 2e-31，以及 φ ₁ 與它們的內積也都是零。

## Beat 7 — 正交基為什麼被偏愛 / why orthogonal bases are favoured
*配音長度：中文 18.1s ／ 英文 17.6s*

**畫面公式**

```
正交基為什麼被偏愛   |   why orthogonal bases are favoured
x ᵦ   =   ( ξ , β ) / ‖ β ‖ ²
```

**旁白（繁中）**

> 一句評註：用正交基的時候，ξ 在某個基向量上的係數就是 Fourier 係數，只由那個基向量決定，換掉其餘的基向量不會變。一般的基底不是這樣。這部分解釋了正交基被偏愛的地位。

**Narration (EN)**

> A remark. With an orthogonal basis the coefficient of a vector at a basis element is the Fourier coefficient and depends only on that element; replacing the other basis vectors does not change it. For an arbitrary basis it does, which partly explains the favoured position.

**動畫**

平面上三支箭頭：e ₁、e ₂（青綠）與 e ₁ + e ₂（紫），黃色那支是 ξ = e ₁ + e ₂。右側對照兩組基底下 e ₁ 的係數：1 與 0。

## Beat 8 — 引理 2.5：正交化 / lemma 2.5: orthogonalising
*配音長度：中文 18.4s ／ 英文 18.0s*

**畫面公式**

```
引理 2.5：正交化   |   lemma 2.5: orthogonalising
φ ₙ    =    α ₙ  −  P ( α ₙ )            M ₙ  =  L ( α ₁ , … , α ₙ )
```

**旁白（繁中）**

> 引理 2.5：獨立的序列都可以正交化，而且前 n 項張成的子空間完全一樣。作法就是上一集那個投影：把 α n 減掉它在前面那些向量張成的空間上的投影。實際計算是遞迴的。

**Narration (EN)**

> Lemma 2.5: any independent sequence can be orthogonalised, and the first n terms span the same subspace. The construction is the projection from last time: subtract from each vector its projection on the span of the earlier ones. The calculation is recursive.

**動畫**

Gram–Schmidt 的一步：α ₁ 與它張成的直線、α ₂、它在直線上的投影 μ（紅），以及從 μ 指到 α ₂ 的黃色箭頭 φ ₂。右側驗證 ( φ ₂ , α ₁ ) = 0e+00。

## Beat 9 — 書上的例子：1、x、x ² / the book's example
*配音長度：中文 18.9s ／ 英文 18.7s*

**畫面公式**

```
書上的例子：1、x、x ²   |   the book's example
1 ,      x  −  1 / 2 ,      x ²  −  x  +  1 / 6
```

**旁白（繁中）**

> 書上的例子是 C([0,1]) 上的 1、x、x 平方。正交化之後前三項是 1、x 減二分之一、x 平方減 x 加六分之一。書上說這個過程完全初等，可是再算幾項就很煩了。

**Narration (EN)**

> The book's example is one, x and x squared on the unit interval. Orthogonalising gives one, x minus a half, and x squared minus x plus a sixth. The book remarks that the process is completely elementary but that the calculations become burdensome after a few terms.

**動畫**

C([0,1]) 上正交化之後的三條：1（青綠）、x − 0.5（紫）、x ² − x + 0.1667（紅）。右側列出係數、互相的內積與長度 0.2887、0.0745。

## Beat 10 — 定理 2.4：同構 ⇔ 完備 / theorem 2.4: an isomorphism exactly when complete
*配音長度：中文 19.2s ／ 英文 16.9s*

**畫面公式**

```
定理 2.4：同構 ⇔ 完備   |   theorem 2.4: an isomorphism exactly when complete
θ ᵦ ( ξ )  =  ( ξ , β )            ‖ θ ᵦ ‖  =  ‖ β ‖
```

**旁白（繁中）**

> 最後是定理 2.4。把 β 送成「跟 β 取內積」這個泛函，得到的映射是線性的、單射的，而且是等距的。而它是同構的充要條件，就是 V 為 Hilbert 空間——完備性又一次是那個分界線。

**Narration (EN)**

> Last comes Theorem 2.4. Sending a vector to the functional that takes the product with it gives a map which is linear, injective and an isometry. And it is an isomorphism exactly when the space is a Hilbert space: completeness is again the dividing line.

**動畫**

單位圓、β 那支箭頭，以及 ± β 方向上的兩個紅點——|( ξ , β )| 的上界就在那裡取到。右側：上界 1.3000 = ‖ β ‖。
