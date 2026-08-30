# advcalc E54 — 第 3 章：臨界點的分類

Chapter 3: The Classification of Critical Points

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 16 節「二階微分與臨界點的分類」的後半（書頁 189–191）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e54_classification.py`（`AdvCalcE54ZH` / `AdvCalcE54EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[54]` / `FORMULAS_ADVCALC[54]`）
- 配音：`manim_lessons/samples/audio_e54/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.30 分（198 秒）／英文 3.26 分（196 秒）

## 三個臨界點，兩種分類方法，結論一致

假設有兩個：那一點是臨界點，而且二階微分非奇異。有了這兩個，那一點就落進 n 加一類的其中一類，
而 p——正號的個數——就是分類的全部內容。畫面上每個判斷都是算出來的：

- **ω 正交基是真的算出來的**：用帶正負號的 Gram–Schmidt，斷言配對結果是 1、0、0、−1，
  也就是 p 等於 1。
- **三個臨界點各用兩種方法分類**：一種是行列式的規則（正的看 f_xx 的符號，負的是鞍點），
  另一種是在半徑 0.05 的圓上取樣看函數是全升、全降、還是兩者都有。
  **兩種方法在三個例子上結論完全相同**，所以那條規則不是背下來的，是驗過的。
- **定理 16.4 的夾擊在 216 個點上驗過**：取一個二階微分正好是單位矩陣的函數，
  斷言增量夾在 (1±ε)/2 乘上長度平方之間，ε 取 0.11。
  **而且斷言那個 ε 不是隨便取寬的**：在邊界上實際的偏差已經用掉它的一半以上。

probe 幀抓到三處：beat 3 三張二次曲面各自往兩側伸出 1.5 個單位，最左邊那張跑出畫面、
三張還互相重疊；beat 6 的夾擊原本畫到 t 等於一，可是那個夾擊只在 ‖x‖ 小於 δ 時成立，
畫出去的部分正好是定理沒有宣稱的地方；beat 7 兩張曲面同樣太寬。

---

## Beat 0 — 兩個假設 / two hypotheses
*配音長度：中文 18.0s ／ 英文 17.9s*

**畫面公式**

```
兩個假設   |   two hypotheses
df ₐ   =   0                    ( d ² f ₐ ) ⁻¹    ∃
```

**旁白（繁中）**

> 第 16 節的後半是臨界點的分類。假設有兩個：那一點是臨界點，微分等於零；而且二階微分存在、而且非奇異——也就是它對應的那個雙線性形式，在任何一組基底下的矩陣都可逆。

**Narration (EN)**

> The second half of section 16 classifies critical points. Two hypotheses: the point is critical, so the differential vanishes; and the second differential exists and is nonsingular, meaning the bilinear form it corresponds to has an invertible matrix in any basis.

**動畫**

左邊一個三角形，三個頂點標成 x、y、z，三條邊各一個顏色。
右側三行就是度量的三條公理。

## Beat 1 — ω 正交基：化成有正負號的平方和 / an omega-orthonormal basis
*配音長度：中文 19.6s ／ 英文 17.8s*

**畫面公式**

```
ω 正交基：化成有正負號的平方和   |   an omega-orthonormal basis
ω ( α ᵢ , α ⱼ )  =  0    ( i ≠ j )            ω ( α ᵢ , α ᵢ )  =  ± 1
```

**旁白（繁中）**

> 工具是第 2 章的定理 7.1：任何一個對稱雙線性形式都有一組 ω 正交的基底。在那組基底下，不同的兩個基向量配出來是零，同一個配自己是正一或負一。二次型就化成有正負號的平方和。

**Narration (EN)**

> The tool is Theorem 7.1 of chapter 2: every symmetric bilinear form has an omega-orthonormal basis. In it two different basis vectors pair to zero, and each pairs with itself to plus or minus one. The quadratic form becomes a sum of squares with signs.

**動畫**

左邊兩個加框的假設（dFₐ = 0 與二階微分可逆），一支箭頭指向 p 落在 0 到 n 之間。
右側說明有了這兩個，那一點就落進 n 加一類的其中一類。

## Beat 2 — 對角線上不能有零 / no zero on the diagonal
*配音長度：中文 17.2s ／ 英文 17.7s*

**畫面公式**

```
對角線上不能有零   |   no zero on the diagonal
ω ( α ᵢ , α ᵢ )  =  0            ⇒            det  [ t ᵢ ⱼ ]  =  0
```

**旁白（繁中）**

> 對角線上不可能出現零。如果某個基向量配自己是零，那一整欄就都是零，矩陣的秩掉到 n 減一以下，就奇異了。所以非奇異這個假設，正好是「只有正一與負一」的保證。

**Narration (EN)**

> No zero can appear on the diagonal. If some basis vector paired with itself gave zero, that whole column would vanish, the rank would drop below n, and the matrix would be singular. So nonsingularity is exactly what guarantees only plus and minus ones.

**動畫**

左邊 ω 的矩陣經一支箭頭變成對角的 1 與 −1，下面印出算出來的那組基底。
右側說明第 2 章的定理 7.1 給的正交基。

## Beat 3 — p 從 0 到 n，共 n + 1 種 / p from zero to n: n plus one cases
*配音長度：中文 18.9s ／ 英文 19.0s*

**畫面公式**

```
p 從 0 到 n，共 n + 1 種   |   p from zero to n: n plus one cases
q ( x )    =    Σ ₁ ᵖ  x ᵢ ²    −    Σ ᵖ ⁺ ¹ ⁿ  x ᵢ ²              p  =  0 , … , n
```

**旁白（繁中）**

> 換到座標上：混合的二階偏導數全是零，對角線上前 p 個是正一、其餘是負一。p 可以從零跑到 n，所以一共有 n 加一種可能。兩個變數的時候就是三種：極小、鞍點、極大。

**Narration (EN)**

> In coordinates: all the mixed second partials vanish, and the diagonal carries plus one in the first p places and minus one in the rest. Since p runs from zero to n there are n plus one possibilities. For two variables that is three: minimum, saddle, maximum.

**動畫**

左邊一個 3×3 的矩陣，中間那格是零並用紅框圈起一整欄，下面印出 det = 0。
右側說明對角線上不能有零。

## Beat 4 — 定理 16.4：正定就是極小 / Theorem 16.4: positive definite means minimum
*配音長度：中文 15.7s ／ 英文 16.5s*

**畫面公式**

```
定理 16.4：正定就是極小   |   Theorem 16.4: positive definite means minimum
q   ≻   0                ⇒                Δ f ₐ    ≥    0
```

**旁白（繁中）**

> 定理 16.4：如果那一點是臨界點，而且二階微分正定，那麼函數在那裡取到相對極小。正定就是 p 等於 n，也就是那個二次型對每一個非零向量都是正的。

**Narration (EN)**

> Theorem 16.4: if the point is critical and the second differential there is positive definite, the function has a relative minimum at it. Positive definite means p equals n, that is, the quadratic form is positive on every nonzero vector.

**動畫**

左邊三張二次曲面（碗、鞍、倒碗），各自下方標 p = 2、1、0。
右側是 q(x) 的標準形與「共 n 加一種」。

## Beat 5 — 證明：把導數夾起來 / the proof: squeeze the derivative
*配音長度：中文 17.7s ／ 英文 16.7s*

**畫面公式**

```
證明：把導數夾起來   |   the proof: squeeze the derivative
( 1 − ϵ )  t ‖ x ‖ ²      ≤      h ′ ( t )      ≤      ( 1 + ϵ )  t ‖ x ‖ ²
```

**旁白（繁中）**

> 證明是一維的手法。二階微分的定義給出一個估計；因為微分在那一點是零，估計就變成：沿著射線走的那個一元函數，它的導數被夾在一減 ε 與一加 ε 乘上 t 與長度平方之間。

**Narration (EN)**

> The proof is a one-variable manoeuvre. The definition of the second differential gives an estimate, and since the differential vanishes there it becomes: the derivative along a ray is squeezed between one minus and one plus epsilon, times t times the squared length.

**動畫**

左邊一個碗形曲面，最低點打紅點。右側是加框的「正定就是極小」與兩行說明。

## Beat 6 — 積分之後：夾在兩個拋物面之間 / integrate: between two paraboloids
*配音長度：中文 18.5s ／ 英文 18.1s*

**畫面公式**

```
積分之後：夾在兩個拋物面之間   |   integrate: between two paraboloids
( 1 − ϵ ) ‖ x ‖ ² / 2      ≤      Δ f ₐ ( x )      ≤      ( 1 + ϵ ) ‖ x ‖ ² / 2
```

**旁白（繁中）**

> 把那個夾擊對 t 從零積到一，左邊就是函數的增量。得到的是：增量夾在二分之一減 ε 與二分之一加 ε 乘上長度平方之間。不只是極小——增量夾在兩個非常接近的拋物面之間。

**Narration (EN)**

> Integrating that squeeze from zero to one puts the increment of the function on the left. The result is that the increment lies between one half minus epsilon and one half plus epsilon times the squared length. Not merely a minimum: it lies between two very close paraboloids.

**動畫**

左邊三條近乎重合的直線（斜率 1−ε、1、1+ε）與一條夾在中間的紅色曲線。
右側說明夾擊來自二階微分的定義加上微分為零。

## Beat 7 — 一般的 p：夾在兩個同型的曲面之間 / general p: two surfaces of one type
*配音長度：中文 17.2s ／ 英文 17.4s*

**畫面公式**

```
一般的 p：夾在兩個同型的曲面之間   |   general p: two surfaces of one type
( q ( x ) − ϵ ‖ x ‖ ² ) / 2    ≤    Δ f ₐ ( x )    ≤    ( q ( x ) + ϵ ‖ x ‖ ² ) / 2
```

**旁白（繁中）**

> 一般的 p 完全一樣，只要把絕對值裡的長度平方換成那個二次型。得到的是：增量夾在兩個同型的二次曲面之間，前 p 個座標的係數是一減 ε 與一加 ε，後面那些反過來。

**Narration (EN)**

> The general p works the same way: replace the squared length inside the absolute values by the quadratic form. The increment then lies between two quadratic surfaces of the same type, the first p coefficients being one minus and one plus epsilon and the rest reversed.

**動畫**

左邊兩條拋物線與夾在中間的紅色曲線，畫的範圍是 ‖x‖ 小於 δ 那一段。
右側是那條夾擊不等式與「在 216 個點上驗過」。

## Beat 8 — 鞍點：往下那一片有幾維 / a saddle: how many dimensions go down
*配音長度：中文 18.2s ／ 英文 16.9s*

**畫面公式**

```
鞍點：往下那一片有幾維   |   a saddle: how many dimensions go down
V ₁  =  L ( δ ¹ , … , δ ᵖ )              V ₂  =  L ( δ ᵖ ⁺ ¹ , … , δ ⁿ )
```

**旁白（繁中）**

> 於是鞍點的結構就出來了。如果 p 在一與 n 減一之間，函數在前 p 個座標張成的子空間上有相對極小，在互補的那個子空間上有相對極大。往下那個子空間有幾維，就是 n 減 p。

**Narration (EN)**

> That gives the structure of a saddle. If p lies between one and n minus one, the function has a relative minimum on the subspace spanned by the first p coordinates and a relative maximum on the complementary one. The downward subspace has dimension n minus p.

**動畫**

左邊兩張同型的鞍面（上界與下界），形狀相同只差一點點。
右側是把長度平方換成二次型之後的夾擊。

## Beat 9 — 兩個變數的捷徑 / the shortcut for two variables
*配音長度：中文 18.9s ／ 英文 18.2s*

**畫面公式**

```
兩個變數的捷徑   |   the shortcut for two variables
t ₁₁ t ₂₂  −  ( t ₁₂ ) ²    =    f ₓₓ  f ᵧᵧ   −   ( f ₓᵧ ) ²
```

**旁白（繁中）**

> 兩個變數有捷徑，不必真的正交化。看那個二階偏導數矩陣的行列式：正的就是極大或極小，沿一條直線走一下就知道是哪一個；負的就是鞍點。這是第 2 章第 7 節末尾那段的直接應用。

**Narration (EN)**

> For two variables there is a shortcut that avoids orthonormalising. Look at the determinant of the matrix of second partials: positive means a maximum or a minimum, and following one line says which; negative means a saddle. That is section 2.7's closing remark applied.

**動畫**

左邊一張鞍面，兩條主軸方向的截線分別畫成藍色與紅色，中心打橘點。
右側說明 V₁ 上極小、V₂ 上極大，往下那一片是 n 減 p 維。

## Beat 10 — 換到完備空間上照樣成立 / it survives on a complete space
*配音長度：中文 18.2s ／ 英文 19.6s*

**畫面公式**

```
換到完備空間上照樣成立   |   it survives on a complete space
q   ≻   0                    q ¹ ᐟ ²     ≈     ‖ · ‖
```

**旁白（繁中）**

> 最後一句對變分法很要緊：定理 16.4 在定義域換成完備空間時照樣成立。假設改成那個二次型正定，而且它開出來的純量積範數與原來的範數等價。證明幾乎一個字都不用改。

**Narration (EN)**

> One closing remark matters for the calculus of variations: Theorem 16.4 stays true when the domain is a complete space. The hypotheses become that the quadratic form is positive definite and that the scalar product norm it defines is equivalent to the given one. The proof is unchanged.

**動畫**

左邊三個 2×2 的二階偏導數矩陣，各自下方印出行列式與 f_xx。
右側是行列式規則的三句話。

---

## 為什麼兩種分類方法都要跑

行列式的規則是課本上背的東西：正的就是極大或極小、負的就是鞍點。
可是「背得對」與「用得對」是兩件事。所以這一集的三個例子都跑了第二種方法——
在臨界點周圍取一圈點，直接看函數是全升、全降、還是兩者都有——再斷言兩種結論相同。
三個例子涵蓋三種情形，這樣那條規則就不是宣告的，是驗過的。

## 這一節給的比它宣稱的多

定理 16.4 的結論只寫「相對極小」。可是證明裡那個夾擊給的更強：
增量夾在兩個非常接近的拋物面之間，而 ε 可以任意小。
一般的 p 也一樣——夾住它的兩個曲面跟它自己是同一種二次曲面。
「同型」這兩個字才是這一節真正的內容。
