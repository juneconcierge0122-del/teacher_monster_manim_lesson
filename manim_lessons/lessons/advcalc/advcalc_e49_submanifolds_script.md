# advcalc E49 — 第 3 章：子流形與 Lagrange 乘子

Chapter 3: Submanifolds and Lagrange Multipliers

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 12 節「子流形與 Lagrange 乘子」（書頁 172–175）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e49_submanifolds.py`（`AdvCalcE49ZH` / `AdvCalcE49EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[49]` / `FORMULAS_ADVCALC[49]`）
- 配音：`manim_lessons/samples/audio_e49/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.37 分（202 秒）／英文 3.40 分（204 秒）

## 一顆球面，貫穿整集

第 12 節做兩件事：定義子流形，以及在子流形上求極值。兩件事都用同一個例子——
三維裡的單位球面——而畫面上的每個數字都是程式算出來的：

- **定理 12.1 的假設真的成立**：球面上取四個點，用中央差商算 `G(x) = Σxᵢ² − 1` 的梯度，
  斷言每一個的長度都大於 1（值域是一維的，所以「滿射」就是「梯度不是零向量」）；
  再斷言唯一讓梯度為零的是原點，而原點不在球面上。
- **定理 12.2 有內容**：在最大值那一點 ⟨0, 1, 0⟩ 斷言 `dF` 與 `dG` 平行，比值恰好是 1/2；
  **並且**在球面上另取一點 (0.6, 0.8, 0)，斷言兩個梯度的叉積大於 0.5，也就是不平行。
  只演前者的話，那個條件看起來處處成立、什麼都沒說。
- **最大值真的在北極**：在球面上取樣掃過，斷言最大值就是 `F` 在 ⟨0, 1, 0⟩ 的值。
- **收尾接回 E44**：同一個「體積 8 的盒子」問題，這次用乘子解。
  斷言正方體那一點的兩個梯度比值正好是 2，表面積是 24——跟 E44 用代入法得到的一樣。

probe 幀抓到 beat 5：第一版把「兩條不同的曲線、同一個切向量」畫在球面上，
可是在那個半徑下兩條只差 0.04 個單位，出來是球頂上的一團。改成球面旁邊加一個放大框，
差別才看得見。beat 10 的兩個答案原本擠成一列，字縮到只有方程的一半大，改成各佔自己那一欄。

---

## Beat 0 — 一張圖形就是一塊 / a graph is a patch
*配音長度：中文 18.1s ／ 英文 18.7s*

**畫面公式**

```
一張圖形就是一塊   |   a graph is a patch
S  =  { ⟨ ξ , F ( ξ ) ⟩  :  ξ ∈ A }        ⊂        V × W
```

**旁白（繁中）**

> 第 12 節開始講流形。最簡單的情形是一個圖形：F 從 V 的開集映到 W，它的圖形住在 V 乘 W 裡，看起來像一張蓋在定義域上的 n 維曲面。書上把它叫做一塊，n 維的塊。

**Narration (EN)**

> Section 12 begins the theory of manifolds. The simplest case is a graph: F maps an open subset of V into W, and its graph lies in V times W looking like an n-dimensional surface spread over the domain. The book calls such an F an n-dimensional patch.

**動畫**

左邊一張立體示意圖：灰色稀疏的格子是 V 裡的開集，上方藍色較密的網是 F 的圖形。
右側三行說明它住在 V 乘 W 裡，書上把這樣的 F 叫做一塊。

## Beat 1 — 球面不是一張圖形 / the sphere is not a graph
*配音長度：中文 19.6s ／ 英文 17.7s*

**畫面公式**

```
球面不是一張圖形   |   the sphere is not a graph
S  =  { x ∈ ℝ ³  :  x ₁ ²  +  x ₂ ²  +  x ₃ ²  =  1 }
```

**旁白（繁中）**

> 可是有些曲面不是圖形。單位球面是三維裡的二維曲面，不管怎麼把空間拆成直和都寫不成一張圖形。但它顯然是一堆互相重疊的塊黏起來的：每一點附近取夠小的鄰域，交出來就是一塊。

**Narration (EN)**

> But some surfaces are not graphs. The unit sphere is a two-dimensional surface in three-space, and no way of writing that space as a direct sum makes it one. Yet it is plainly a union of overlapping patches: a small enough neighborhood of any point meets it in one.

**動畫**

球面（輪廓加兩條緯線、一條經線），上面兩個點各套一個圈，代表兩塊互相重疊的塊。
右側說明整顆球寫不成一張圖形，可是每一小塊都是。

## Beat 2 — 子流形：每一點附近都是一塊 / a submanifold: a patch near each point
*配音長度：中文 17.0s ／ 英文 18.5s*

**畫面公式**

```
子流形：每一點附近都是一塊   |   a submanifold: a patch near each point
∀ α ∈ S    ∃ N        N  ∩  S   ≅   A  ⊂  V
```

**旁白（繁中）**

> 這句話本身就是定義。S 叫 n 維子流形，如果它上面每一點在 X 裡都有一個鄰域，跟 S 交出來是一塊 n 維的塊。如果那些塊對應的函數都連續可微，就說 S 是光滑的。

**Narration (EN)**

> That observation is the definition. A subset S of X is an n-dimensional submanifold if every point of S has a neighborhood in X whose intersection with S is an n-dimensional patch. If the functions of all those patches are continuously differentiable, S is smooth.

**動畫**

同一顆球，一點打紅點並套一個較大的紅圈標成 N。
右側三行就是子流形的定義。

## Beat 3 — 定理 12.1：零集合什麼時候是子流形 / Theorem 12.1: when a zero set is one
*配音長度：中文 17.8s ／ 英文 19.2s*

**畫面公式**

```
定理 12.1：零集合什麼時候是子流形   |   Theorem 12.1: when a zero set is one
dG ᵧ  :  X  ↠  Y                S   =   G ⁻¹ ( 0 )
```

**旁白（繁中）**

> 子流形常常以零集合的樣子出現，球面就是。定理 12.1 的條件很乾淨：G 連續可微、從 n 加 m 維映到 m 維，只要零集合上每一點的微分都是滿射，那個零集合就是 n 維子流形。

**Narration (EN)**

> Submanifolds usually appear as zero sets of mappings, and the sphere is one. Theorem 12.1 is clean: if G is continuously differentiable from n plus m dimensions to m and its differential is onto at every point of the zero set, that set is a submanifold.

**動畫**

球面上四個取樣點各射出一支往外的紅色梯度箭頭。
右側是定理 12.1 的假設與結論，以及「球面上梯度處處不為零」。

## Beat 4 — 證明：零空間就是那個 V / the proof: the null space is the V
*配音長度：中文 18.8s ／ 英文 17.3s*

**畫面公式**

```
證明：零空間就是那個 V   |   the proof: the null space is the V
dim  N ( dG ᵧ )  =  n                X  =  V × W
```

**旁白（繁中）**

> 證明就是隱函數定理。微分滿射，所以它的零空間維數剛好是 n；取一個補空間當第二個因子，微分限制在上面就是同構，也就是第二個偏微分可逆。隱函數定理立刻交出一塊圖形。

**Narration (EN)**

> The proof is the implicit function theorem. Surjectivity makes the null space exactly n-dimensional; take any complement as the second factor and the differential restricted to it is an isomorphism, which is the second partial differential inverting. A graph comes straight back.

**動畫**

左邊三行式子：dG 是滿射、零空間的維數是 n、X 拆成 V 乘 W 而第二個偏微分可逆。
右側說明取零空間當 V、任一補空間當 W。

## Beat 5 — 切向量：曲線的等價類 / a tangent vector: a class of curves
*配音長度：中文 18.8s ／ 英文 18.8s*

**畫面公式**

```
切向量：曲線的等價類   |   a tangent vector: a class of curves
N   =   { γ ′ ( 0 )  :  γ ⊂ S ,  γ ( 0 ) = α }
```

**旁白（繁中）**

> 光滑子流形在每一點有唯一的 n 維切平面，平移到原點就是切空間。定理 10.2 說它的元素恰好是 S 上通過那一點的光滑曲線的切向量。這個說法後面會變成抽象流形上切向量的定義。

**Narration (EN)**

> A smooth submanifold has a unique n-dimensional tangent plane at each point, and translating it to the origin gives the tangent space. Theorem 10.2 says its elements are exactly the tangent vectors of smooth curves in S through that point. That reading later becomes the definition.

**動畫**

左邊一顆球標出一點並套小圈，一支灰色箭頭指向右邊一個加框的放大圖：
傾斜的格子代表曲面，上面兩條不同顏色的曲線交於一點，共用一支紅色的切向量。

## Beat 6 — 有約束時 dF 不會是零 / constrained, dF does not vanish
*配音長度：中文 18.2s ／ 英文 19.7s*

**畫面公式**

```
有約束時 dF 不會是零   |   constrained, dF does not vanish
F ( x )  =  x ₂        g ( x )  =  Σ x ᵢ ² − 1        dF  =  F  ≠  0
```

**旁白（繁中）**

> 接下來是古典的有約束極值問題：把 F 限制在 S 上求極大。這裡不能令 dF 等於零。球面上取 F 是第二個座標，最大值一在北極取到，可是 F 線性，dF 就是 F，永遠不是零。

**Narration (EN)**

> Now a classical constrained maximum problem: maximize F with the point confined to S. Setting dF equal to zero is no good. On the unit sphere take F to be the second coordinate; its maximum is one at the north pole, yet F is linear, so dF is F and never vanishes.

**動畫**

球面加四條水平的灰色虛線（F 的等高面），最上面一點打紅點，右側一支往上的藍色箭頭。
右側說明 F 線性，dF 永遠不是零。

## Beat 7 — 定理 12.2：換成 dF 等於 l 接上 dG / Theorem 12.2: dF becomes l after dG
*配音長度：中文 17.4s ／ 英文 18.1s*

**畫面公式**

```
定理 12.2：換成 dF 等於 l 接上 dG   |   Theorem 12.2: dF becomes l after dG
∃ l ∈ Y *          d ( F  −  l ∘ G ) ᵧ    =    0
```

**旁白（繁中）**

> 定理 12.2 就是解方：F 在 S 上某點取到極大，那麼 Y 的對偶空間裡存在一個泛函 l，使那一點是 F 減 l 接上 G 的臨界點。條件從「dF 是零」放寬成「dF 是某個 l 接上 dG」。

**Narration (EN)**

> Theorem 12.2 is the fix: if F attains a maximum on S at a point, then some functional l in the dual of Y makes that point a critical point of F minus l composed with G. The condition relaxes from dF vanishing to dF being l composed with dG.

**動畫**

左右兩個加框的小圖，各畫一個圓與圓上一點：左邊在最大值處紅藍兩支箭頭平行，
右邊換一點兩支箭頭夾角。框下分別標 dF = l∘dG 與 dF ≠ l∘dG。

## Beat 8 — 證明：還是隱函數定理 / the proof: the implicit function theorem again
*配音長度：中文 17.8s ／ 英文 20.1s*

**畫面公式**

```
證明：還是隱函數定理   |   the proof: the implicit function theorem again
K ( ξ )  =  F ( ξ , H ( ξ ) )            l  =  dF ²  ∘  ( dG ² ) ⁻¹
```

**旁白（繁中）**

> 證明還是隱函數定理。把 S 局部寫成圖形，限制上去的函數 K 在那點的微分是零；再對恆等式微分把 dH 解出來代掉，剩下的式子裡那個「dF 二接上 dG 二的反元素」就是要找的 l。

**Narration (EN)**

> The proof is again the implicit function theorem. Write S locally as a graph; the restricted function K has vanishing differential there. Differentiate the identity too, solve for dH and substitute, and what is left contains the l we want: dF two composed with the inverse of dG two.

**動畫**

左邊三行證明的式子，下面一個加框的 l = dF² ∘ (dG²)⁻¹。
右側說明兩式解掉 dH 之後剩下的就是那個 l。

## Beat 9 — 座標下就是乘子法 / in coordinates: the multiplier rule
*配音長度：中文 17.4s ／ 英文 18.6s*

**畫面公式**

```
座標下就是乘子法   |   in coordinates: the multiplier rule
∂F / ∂x ⱼ    −    Σ  c ᵢ  ∂g ⁱ / ∂x ⱼ    =    0            j = 1 , … , n
```

**旁白（繁中）**

> 翻成座標就是乘子法。對偶空間裡的泛函就是一組係數 c，條件變成 F 的偏導數減掉 c 乘各個 g 的偏導數之和等於零。這 n 個方程加上 G 那 m 個，剛好配 m 加 n 個未知數。

**Narration (EN)**

> In coordinates this is the multiplier rule. A functional on the dual is a tuple of coefficients, and the condition reads: the partial of F minus the sum of coefficients times the partials of the constraints is zero. Those n equations plus the m constraints match m plus n unknowns.

**動畫**

左邊兩條式子（乘子條件與約束本身），下面一個加框的「n 加 m 個方程、n 加 m 個未知數」。
右側說明未知數是座標加乘子。

## Beat 10 — 兩個例子，其中一個是 E44 / two examples, one of them E44's
*配音長度：中文 21.0s ／ 英文 17.6s*

**畫面公式**

```
兩個例子，其中一個是 E44   |   two examples, one of them E44's
x  =  ⟨ 0 , ± 1 , 0 ⟩ ,   c  =  ± 1 / 2            x = y = z = V ^ ( 1 / 3 )
```

**旁白（繁中）**

> 兩個例子。球面上求第二個座標的極大：前三式逼出第一與第三個座標是零，約束給出第二個座標是正負一，乘子是正負二分之一。另一個是 E44 那個盒子，這次用乘子解，前三式直接逼出三邊相等。

**Narration (EN)**

> Two examples. Maximising the second coordinate on the sphere: the equations force the first and third coordinates to vanish and the constraint gives plus or minus one, with multiplier one half. The other is E44's box, this time done by a multiplier.

**動畫**

左右兩欄方程組：左邊球面的四式、右邊盒子的四式，各自下方一行答案。
右側說明前三式逼出三邊相等，約束再給出邊長。

---

## 為什麼「另一點不平行」那一半非畫不可

定理 12.2 說的是「存在一個 l 使得 dF 等於 l 接上 dG」。如果只在最大值那一點畫兩支平行的箭頭，
看起來像是這件事到處都成立——那樣這條定理就什麼都沒說。所以第 7 拍是兩個框：
左邊平行、右邊不平行，而右邊那個點也在同一顆球面上。程式算出來的叉積是 1.20，不是小數點後的雜訊。

## 這一節整節沒有習題

第 12 節從書頁 172 講到 175 中段，接著直接進第 13 節，中間沒有習題。
這在這本書裡少見（第 2 章的 *§7 是另一個），而且第 12 到 15 節連續四節都是如此。
