# advcalc E69 — 第 5 章：正交投影（上）

Chapter 5: Orthogonal Projection

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 2 節「正交投影」的前半（書頁 252–254）。

**§2 共 5 頁（252–256），分成兩集。** 本集收在書頁 254 上半，Fourier 係數剛被命名的地方；
E70 接正交規範集合、定理 2.2 Bessel 不等式、基底與定理 2.3、引理 2.5 Gram–Schmidt，
以及定理 2.4（θ 是同構 ⇔ V 是 Hilbert 空間）。習題 2.1–2.11 在書頁 256–257，依 PLAYBOOK 第 8 節不做解答。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e69_projection.py`（`AdvCalcE69ZH` / `AdvCalcE69EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[69]` / `FORMULAS_ADVCALC[69]`）
- 配音：`manim_lessons/samples/audio_e69/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.13 分（188 秒）／英文 3.07 分（184 秒）

## 這一段的結構

書上的順序就是一條線：**幾何直覺 → 兩個引理 → 一個定理 → 投影本身。**

1. **垂足**：M 裡使 α 減 μ 垂直 M 的那個 μ。「每個 α 都有垂足」等價於 **V = M ⊕ M⊥**。
2. **引理 2.1**：垂足 ⇔ 最佳近似（而且最近的點唯一）。
3. **引理 2.2**：極小化序列一定是 Cauchy——證明就是上一集的平行四邊形法則。
4. **定理 2.1**：M 完備 ⇒ V = M ⊕ M⊥。完備性正是這裡唯一用得到的地方。
5. **正交投影**：它同時是垂足與最佳近似，所以在所有投影裡被挑出來。
6. **引理 2.3**（投影可加）與**引理 2.4**（到一維子空間的投影）→ **Fourier 係數**。

## 這一集的具體例子

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 垂足 | 平面上 M 是過原點的直線 | ρ = 1.1217，( α − μ , η ) = 3e-16 |
| 最佳近似 | M 上另外兩點的距離 | 1.4240、1.3004，都大於 1.1217 |
| 畢氏定理 | 兩邊各算一次 | 2.0277 = 1.2581 + 0.7696 |
| 反過來那半 | 在 M 上取一個不是垂足的點 | 內積 -0.9620，二次式在 t = 0.8000 掉到 -0.7696 |
| 極小化序列 | 五個點的距離 | 1.5686 → 1.1238（ρ = 1.1217）|
| 引理 2.2 | 平行四邊形法則兩邊 | 0.534444 = 0.534444；中點距離 1.3389 ≥ ρ |
| 定理 2.1 | 殘差與三個基向量的內積 | 都 ≤ 4e-15 |
| 引理 2.3 | 三個一維投影之和對 M 上的投影 | 差 0e+00 |
| 引理 2.4 | 積分算出的 Fourier 係數 | 1.0000、0.6000、0.3500 |
| 最佳近似（函數空間） | 三個擾動過的係數組合 | 0.6542、0.6749、0.6632，都大於 ρ = 0.6267 |

**函數空間那個例子是倒著設計的**：α 拿四個正弦組出來（係數 1.0、0.6、0.3，
再加上 0.5 倍的第 5 個），而 M 只由前三個張成。這樣一來**積分算出的 Fourier 係數會原封不動
把當初組出來的數字還回來**，殘差則正好是第四個正弦，範數 0.6267 = 0.5 × √(π/2)。
**例子自己驗自己**，而且畫面上「投影幾乎貼著 α、差出來的是一條乾淨的高頻正弦」讀得出來。

## 這一輪的版面問題

這一集沒有數學上的錯，可是 `collide` 一口氣報了 16 處，全部是同一個原因：
**平面圖上要放的點太多，而每個點都要標籤。**

- **`_dash` 畫出來的虛線，它的每一段都是一個 `Line`**，所以 collide 報的「Line through 標籤」
  多半是虛線穿過標籤，不是實線。這一點以前沒記過。
- beat 6 原本取 n = 3、m = 5，兩點在直線上只差 0.12 個螢幕單位，**三個標籤疊成一團**。
  改成 n = 1、m = 3，並且**把中點的標籤整個拿掉，改用顏色在圖說裡點名**。
- 中點原本用青綠色，**跟直線 M 同色**——這正是 E68 beat 7 那個教訓的另一種形式：
  圖說點名一個顏色，畫面上那個顏色卻是別的東西。改成白色。
- 另外三處：正交補那條線畫得太長，**穿過下面的註腳**；距離的數字壓在它量的那條虛線上；
  α 的標籤離曲線頂點太近（0.26 不夠，改 0.40）。

---

## Beat 0 — 作垂線，取垂足 / dropping a perpendicular
*配音長度：中文 19.5s ／ 英文 16.8s*

**畫面公式**

```
作垂線，取垂足   |   dropping a perpendicular
μ  ∈  M ,        ( α − μ )   ⊥   M
```

**旁白（繁中）**

> 幾何裡最重要的手法之一，是從一點往一條線或一個平面作垂線，再用直角三角形論證；這一招在 pre-Hilbert 空間裡一樣重要。M 是子空間時，從 α 落到 M 的垂足，就是 M 裡使 α 減 μ 垂直 M 的那個 μ。

**Narration (EN)**

> One of the most important devices in geometry is dropping a perpendicular from a point to a line or a plane and arguing with right triangles. For a subspace M, the foot of that perpendicular is the vector in M whose difference from the given one is orthogonal to M.

**動畫**

平面上一條過原點的青綠色直線就是 M；黃色的點是 α，紅色的點是垂足 μ，兩者之間用紅色虛線連起來。垂足與距離都是算出來的。

## Beat 1 — 有垂足 ⇔ 直和分解 / a foot for every vector is the decomposition
*配音長度：中文 17.5s ／ 英文 16.1s*

**畫面公式**

```
有垂足 ⇔ 直和分解   |   a foot for every vector is the decomposition
α  =  μ  +  ( α − μ )            V   =   M  ⊕  M ⊥
```

**旁白（繁中）**

> 把 α 寫成 μ 加上 α 減 μ，就看得出來：每個 α 都有垂足，等價於直和分解 V 等於 M 直和它的正交補。而這個分解正是完備性保證的。先證一件幾何上很直觀的事。

**Narration (EN)**

> Writing the vector as the foot plus the difference shows that having a foot for every vector is the same as the direct sum decomposition of the space into M and its orthogonal complement. That decomposition is exactly what completeness guarantees.

**動畫**

同一張圖加上紫色的正交補直線，並把 α 畫成兩支箭頭的和：紅色那支是 μ（在 M 裡），紫色那支是 α 減 μ（垂直 M）。右側列出兩個分量與內積 3e-16。

## Beat 2 — 引理 2.1：垂足就是最佳近似 / lemma 2.1: the foot is the best approximation
*配音長度：中文 12.0s ／ 英文 13.1s*

**畫面公式**

```
引理 2.1：垂足就是最佳近似   |   lemma 2.1: the foot is the best approximation
( α − μ )  ⊥  M        ⇔        ‖ α − μ ‖   =   min
```

**旁白（繁中）**

> 引理 2.1：μ 在 M 裡的時候，α 減 μ 垂直 M 的充要條件是，μ 是 M 裡離 α 最近的唯一一點——也就是 α 在 M 裡的最佳近似。

**Narration (EN)**

> Lemma 2.1: for a vector in M, the difference being orthogonal to M is equivalent to its being the unique point of M closest to the given vector, that is, the best approximation in M.

**動畫**

α 到 M 上三個點的距離：垂足 1.1217，另外兩點 1.4240 與 1.3004，都用虛線畫出來並列在右側表格裡。

## Beat 3 — 一個方向：畢氏定理 / one direction: the Pythagorean theorem
*配音長度：中文 15.0s ／ 英文 14.9s*

**畫面公式**

```
一個方向：畢氏定理   |   one direction: the Pythagorean theorem
‖ α − ξ ‖ ²    =    ‖ α − μ ‖ ²  +  ‖ μ − ξ ‖ ²
```

**旁白（繁中）**

> 一個方向直接用畢氏定理：α 減任何其他一點 ξ 的長度平方，等於 α 減 μ 的平方加上 μ 減 ξ 的平方，所以嚴格大於 α 減 μ 的平方。最近點因此唯一。

**Narration (EN)**

> One direction is the Pythagorean theorem: the square of the distance to any other point of M is the square of the distance to the foot plus the square of the distance from the foot to that point, hence strictly larger. So the closest point is unique.

**動畫**

α、μ、ξ 三點構成的直角三角形，直角記號畫在垂足那裡。右側把畢氏定理兩邊各算一次：2.0277 = 1.2583 + 0.7695。

## Beat 4 — 反過來：那個二次式不能變號 / the converse: that quadratic cannot change sign
*配音長度：中文 18.6s ／ 英文 17.4s*

**畫面公式**

```
反過來：那個二次式不能變號   |   the converse: that quadratic cannot change sign
0   ≤   2 t ( α − μ , ξ )  +  t ² ‖ ξ ‖ ²          ∀ t  ∈  ℝ
```

**旁白（繁中）**

> 反過來。設 μ 是最近的點、ξ 是 M 裡任一非零向量，把 α 減 μ 再加 t ξ 的長度平方展開，得到一個對每個實數 t 都非負的式子。t 可以取跟那個內積反號的小數，所以內積只能是零。

**Narration (EN)**

> For the converse, let the foot be the closest point and take any nonzero vector in M. Expanding the square of the difference plus t times it gives an expression that is non-negative for every real t. A small t of the opposite sign then forces the product to vanish.

**動畫**

兩條拋物線：青綠色那條是垂足的 q(t) = 1.2025 t²，只在 t = 0 碰到零；紅色那條是 M 上另一點的，掉到 −0.7696。

## Beat 5 — 取極小化序列，關鍵在完備性 / a minimising sequence, and where completeness enters
*配音長度：中文 17.3s ／ 英文 17.8s*

**畫面公式**

```
取極小化序列，關鍵在完備性   |   a minimising sequence, and where completeness enters
‖ α − μ ₙ ‖     →     ρ ( α , M )
```

**旁白（繁中）**

> 於是找垂足的辦法就有了：取 M 裡一列 μ n，讓它們到 α 的距離趨近 M 到 α 的距離，再把 μ 定義成極限。關鍵在這裡：這種序列一定是 Cauchy，可是 M 不完備時極限可能不存在。

**Narration (EN)**

> So here is how to look for the foot: take a sequence in M whose distances to the vector tend to the distance from the vector to M, and define the foot as its limit. And here is the crux: such a sequence is always Cauchy, but its limit need not exist when M is not complete.

**動畫**

M 上五個點 μ n（n = 1、2、4、8、16）與它們到 α 的虛線；距離 1.5686 → 1.1238，右側表格最後一列是 ρ = 1.1217。

## Beat 6 — 引理 2.2：它一定是 Cauchy / lemma 2.2: such a sequence is Cauchy
*配音長度：中文 18.4s ／ 英文 16.7s*

**畫面公式**

```
引理 2.2：它一定是 Cauchy   |   lemma 2.2: such a sequence is Cauchy
‖ μ ₙ − μ ₘ ‖ ²  =  2 ( ‖ α − μ ₙ ‖ ² + ‖ α − μ ₘ ‖ ² )  −  ‖ 2 α − ( μ ₙ + μ ₘ ) ‖ ²
```

**旁白（繁中）**

> 引理 2.2 的證明就是平行四邊形法則：μ n 減 μ m 的平方，等於兩個距離平方和的兩倍，減掉 2α 減兩點之和的平方。前項趨近 4ρ 平方，後項永遠至少 4ρ 平方，因為中點也在 M 裡。

**Narration (EN)**

> The proof of Lemma 2.2 is the parallelogram law. The square of the difference of two terms is twice the sum of their squared distances minus the square of twice the vector minus their sum. The first tends to four rho squared, the second is always at least that.

**動畫**

μ n、μ m 與它們的中點（白色）都畫在 M 上，三條虛線連到 α。右側把平行四邊形法則兩邊各算一次，並列出中點的距離 1.3389 ≥ ρ。

## Beat 7 — 定理 2.1：V = M ⊕ M ⊥ / theorem 2.1: the decomposition
*配音長度：中文 15.6s ／ 英文 19.2s*

**畫面公式**

```
定理 2.1：V = M ⊕ M ⊥   |   theorem 2.1: the decomposition
V   =   M  ⊕  M ⊥              dim M  <  ∞
```

**旁白（繁中）**

> 定理 2.1：M 是完備子空間時，V 就分解成 M 與它的正交補的直和。特別是 pre-Hilbert 空間的任何有限維子空間、Hilbert 空間的任何閉子空間，都有這個分解。

**Narration (EN)**

> Theorem 2.1: if M is a complete subspace of a pre-Hilbert space, the space splits as the direct sum of M and its orthogonal complement. In particular this holds for every finite-dimensional subspace of a pre-Hilbert space and every closed subspace of a Hilbert space.

**動畫**

函數空間：黃色是 α，紅色是它在 M = span{sin t, sin 2t, sin 3t} 上的投影，紫色是兩者的差。右側驗證那個差跟三個基向量的內積都是 1e-15 等級。

## Beat 8 — 正交投影就是那個被挑出來的 / the orthogonal projection is the distinguished one
*配音長度：中文 16.7s ／ 英文 16.4s*

**畫面公式**

```
正交投影就是那個被挑出來的   |   the orthogonal projection is the distinguished one
P ( ξ )  =  μ            P ²  =  P ,        P ( V )  =  M
```

**旁白（繁中）**

> 有了分解，沿正交補到 M 的那個投影就叫正交投影。在 M 的各種補空間給出的投影裡，它是被挑出來的那一個，因為它同時是垂足與最佳近似——「投影」這個字就是從垂足來的。

**Narration (EN)**

> With the decomposition in hand, the projection on M along the orthogonal complement is called the orthogonal projection. Among all the projections on M it is the distinguished one, because it is at once the foot of the perpendicular and the best approximation.

**動畫**

同一個平面圖，兩個不同的向量 ξ ₁、ξ ₂ 各自畫出到 M 的虛線與紅色的垂足——同一個投影 P 作用在兩個向量上。

## Beat 9 — 引理 2.3：投影可以加起來 / lemma 2.3: projections add
*配音長度：中文 17.8s ／ 英文 17.8s*

**畫面公式**

```
引理 2.3：投影可以加起來   |   lemma 2.3: projections add
Σ ᵢ P ᵢ α   =   P α            M ᵢ  ⊥  M ⱼ
```

**旁白（繁中）**

> 引理 2.3：有限多個完備、兩兩正交的子空間，把 α 在每一個上面的投影加起來，就是 α 在直和上的投影。證明只要對每一個子空間分別驗證垂直，而交叉項因為正交都是零。

**Narration (EN)**

> Lemma 2.3: for finitely many complete, pairwise orthogonal subspaces, the projections of a vector on each of them add up to its projection on the direct sum. The proof only checks orthogonality against each subspace separately, and the cross terms vanish.

**動畫**

三條細曲線是 α 在三個一維子空間上的投影，粗的紅色那條是它們的和，也就是 α 在 M 上的投影；右側列出兩者的差 0e+00。

## Beat 10 — 引理 2.4 與 Fourier 係數 / lemma 2.4, and the Fourier coefficient
*配音長度：中文 19.0s ／ 英文 17.8s*

**畫面公式**

```
引理 2.4 與 Fourier 係數   |   lemma 2.4, and the Fourier coefficient
P ( ξ )    =    ( ( ξ , η ) / ‖ η ‖ ² )  η
```

**旁白（繁中）**

> 引理 2.4：到單一非零向量 η 張成的一維子空間的投影，是內積除以 η 的長度平方再乘 η。這個係數叫 Fourier 係數。於是一組正交向量的 Fourier 係數合起來就是投影，也就是最佳近似。

**Narration (EN)**

> Lemma 2.4: the projection on the span of a single nonzero vector is the product divided by its square norm, times that vector, and the number is called the Fourier coefficient. For an orthogonal collection those coefficients assemble the projection, the best approximation.

**動畫**

α 與三個逐步加項的投影 P ₁ α、P ₂ α、P ₃ α 畫在一起；右側是三個 Fourier 係數 1.0000、0.6000、0.3500 與對應的距離 1.0727 → 0.7649 → 0.6267。
