# advcalc E67 — 第 4 章：弱方法

Chapter 4: Weak Methods

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章加星號的第 12 節「弱方法」（書頁 245–247）。

**§12 整節沒有習題**，書頁 247 講完直接進第 5 章「純量積空間」——這在這本書裡是第二次（第一次是第 2 章加星號的 §7）。**OUTLINE 把 §12 寫成 245–248，這次不是多算習題頁，而是多算進了下一章的開頭——那張表的頁碼第九次不能直接用。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e67_weak.py`（`AdvCalcE67ZH` / `AdvCalcE67EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[67]` / `FORMULAS_ADVCALC[67]`）
- 配音：`manim_lessons/samples/audio_e67/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.66 分（220 秒）／英文 3.18 分（191 秒）

## 這一節在做什麼

書上的動機講得很直白：所有範數在有限維空間上都等價，而定義域有限維的線性映射自動有界——那麼這種空間的極限理論，也許根本不需要範數。**做法是把向量值的 F，換成研究 {λ ∘ F : λ ∈ V*} 的全體。**

1. **定理 12.1**：有限維時，弱收斂與範數收斂是同一件事。容易的那一半靠「泛函自動連續」；反過來那一半只用一行——一範數就是座標泛函的差的絕對值之和。
2. **那 n 個泛函一個都不能少。** 書上沒有特別強調，這一集用 ηₙ = ⟨0, n⟩ 把它畫出來：只用 E₁ 去測，它看起來收斂到零，可是範數跑到無限大。
3. **積分與微分都用「跟泛函交換」來定義**，唯一性由 V** ≅ V（第 2 章定理 3.2）保證。
4. **微積分基本定理變成一行。**
5. **唯一拿不到的是範數不等式**，它要定理 12.2，而書上明說這門課不證。

## 這一集的具體例子

全部數字都在一個例子上算出來：**V 取平面配一範數**（這是定理 12.1 證明裡用的那個範數），所以 **V\* 上的對偶範數是上界範數，它的單位球面是一個正方形**；弧取 **f(t) = (cos t, sin t) 在 [0, π/2] 上**，積分是 ⟨1, 1⟩。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 積分的弱定義 | 五個泛函各做一次 Simpson 數值積分，跟 λ(⟨1,1⟩) 比 | 最大誤差 6e-15 |
| λ ↦ ∫λ∘f 是線性的 | 取 λ = 2λ₁ − 3λ₂ 兩邊分別算 | 1.2000 對 1.2000 |
| 微分的弱定義 | 中央差商，步長 0.1 / 0.01 / 0.001 | 誤差 1.7e-03 → 1.7e-05 → 1.7e-07 |
| 基本定理 | 對 F 做同樣的中央差商，五個泛函一起看 | 誤差 3e-11 |
| 定理 12.2 | 在對偶單位球面上取 64 點搜最大值 | sup = 2.0000 = ‖α‖₁，只有 ⟨1,1⟩ 與其負號取到 |
| 切線碰到球面的範圍 | 在球面上取 256 點數有幾點落在切線上 | 65 點，是一整條邊 |
| 最後的不等式 | ‖∫f‖₁ 對 (b−a)‖f‖∞ | 2.0000 ≤ 2.2214，比值 0.9003 |

**一範數選得有道理**：它讓定理 12.1 的證明變成一行，也讓定理 12.2 的「切超平面」有一個看得見的樣子——菱形的一整條邊。順帶也看得到一件書上沒講的事：**在這個範數下，切線碰到球面的不是一個點，而是一整條邊**；定理只要求它不進到球裡面。

## 這一輪抓到的錯

### 一、beat 9 的切線畫出來像被截斷

切線 x + y = 2 **跟菱形右上那條邊完全重合**，而邊是後畫的，所以紅色虛線只剩兩端露在外面——看起來像「線穿到菱形後面去了」，而不是「碰在一整條邊上」。**圖說的話跟圖畫的東西不一樣，這次在 480p 抽幀就抓到了**（E66 那次是 1080p 渲染完才抓到）。改成把那條接觸邊本身畫成紅色，只有延伸出去的兩段用虛線。

### 二、beat 7 的第一版圖讀不出東西

原本畫 λ₁∘f，它在整個區間裡只從 1.05 變到 0.81，**曲線幾乎是平的，切線疊上去看不出是切線**。改用 λ₂∘f（從 −0.4 掃到 1.0），並把切線加長加粗。**這是「數學上對但畫出來讀不到」的第四次**，前三次是 E60 的 √2、E64 的平坦曲線、E66 的十六個商。

### 三、`if False else` 第五集出現

寫 beat 9 表格時又寫了一次。這次在跑檢查前先 `grep -c "if False"` 抓掉——但它留下的 `2 nd` 又被 `langscan` 當成英文字抓出來（它是對的：`nd` 是字）。改成純符號的 `{SUP} > {SECOND} ( λ ≠ ± ⟨ 1 , 1 ⟩ )`。

### 四、`collide` 抓到 17 處

六列的表格（表頭加五列）撞到自己底下的圖說，四拍都一樣；beat 5 的面積陰影線穿過 `1.5000` 那個數字。修法：表格改用更密的列距與小一號字，圖說往下移；面積的數字挪到曲線上方。

### 五、圖說說了一個畫面沒有的方向

beat 4 原本寫「向上那個黃色箭頭」，可是那兩個箭頭一個向右、一個向左。另外英文註腳寫「two beats ago」，實際是三拍前。兩處都改掉。

---

## Beat 0 — 也許根本不需要範數 / perhaps no norms are needed at all
*配音長度：中文 19.9s ／ 英文 18.6s*

**畫面公式**

```
也許根本不需要範數   |   perhaps no norms are needed at all
F    ↦    { λ ∘ F  :  λ ∈ V * }
```

**旁白（繁中）**

> 加星號的第 12 節叫弱方法。有限維空間上範數都等價，有限維定義域的線性映射又自動有界，於是讓人懷疑：極限理論也許不需要範數。做法是把向量值的 F，換成所有由泛函得到的實值函數。

**Narration (EN)**

> Starred section 12 is called weak methods. All norms on a finite-dimensional space are equivalent, and a linear map with such a domain is automatically bounded, so the limit theory may need no norms. The idea: study a vector-valued map through the real functions functionals give.

**動畫**

左邊是弧 f（青綠色）在平面上的四分之一圓，三個取樣點畫成向量；右邊是兩條複合出來的實值函數 λ₁∘f（黃）與 λ₂∘f（紫），中間一個箭頭表示「拿泛函複合」這個動作。

## Beat 1 — 定理 12.1，容易的那一半 / theorem 12.1, the easy half
*配音長度：中文 19.3s ／ 英文 19.2s*

**畫面公式**

```
定理 12.1，容易的那一半   |   theorem 12.1, the easy half
| λ ( ξ ₙ ) − λ ( ξ ) |    ≤    ‖ λ ‖  ‖ ξ ₙ − ξ ‖
```

**旁白（繁中）**

> 定理 12.1：V 有限維時，一個序列收斂——用任何一個範數，因此用每一個——的充要條件是，對偶空間裡每個泛函都把它送成收斂的實數列。一半沒有內容：泛函自動連續，差被兩個範數的積壓著。

**Narration (EN)**

> Theorem 12.1: if V is finite-dimensional, a sequence converges, in any and so every norm, if and only if every functional in the dual carries it to a convergent sequence of reals. One half has no content: a functional is continuous, so norms bound the difference.

**動畫**

左邊十二個點沿著螺線收進 ξ（黃色），右邊一條實數線上是它們在 λ₁ 底下的影子，收進 λ₁(ξ)。右側表格列 n = 1、2、4、8、16 的 |λ₁(ξₙ−ξ)| 與 ‖λ₁‖‖ξₙ−ξ‖。

## Beat 2 — 反過來：對偶基那 n 個座標泛函 / the converse: the n coordinate functionals
*配音長度：中文 19.1s ／ 英文 18.1s*

**畫面公式**

```
反過來：對偶基那 n 個座標泛函   |   the converse: the n coordinate functionals
‖ ξ ₙ − ξ ‖ ₁    =    Σ ᵢ | E ᵢ ( ξ ₙ ) − E ᵢ ( ξ ) |    →    0
```

**旁白（繁中）**

> 反過來那一半是這節唯一的計算。取一組基，看對偶基那 n 個座標泛函。假設每個泛函都收斂，那 n 個也收斂；而一範數剛好是那 n 個座標差的絕對值之和，每一項趨近零，和也趨近零。

**Narration (EN)**

> The converse is the only computation here. Take a basis and the n coordinate functionals of the dual basis. If every functional converges then those n do, and the one-norm is exactly the sum of the absolute values of the n coordinate differences, each tending to zero.

**動畫**

ξ 與兩個序列點之間畫出「先橫再直」的兩段虛線：紅色是 n = 1、青綠色是 n = 2。兩段長度就是 |E₁| 與 |E₂|，加起來是那一列的一範數。

## Beat 3 — 少一個泛函就測不出來 / one functional short and the test fails
*配音長度：中文 18.6s ／ 英文 16.9s*

**畫面公式**

```
少一個泛函就測不出來   |   one functional short and the test fails
E ₁ ( η ₙ )  =  0            ‖ η ₙ ‖ ₁  =  n  →  ∞
```

**旁白（繁中）**

> 那 n 個泛函一個都不能少。畫面上這個序列第一個座標永遠是零，只用第一個泛函去測就看起來收斂；可是它的範數是 n，跑到無限大。漏掉哪個泛函，那個泛函的核就是測不到的方向。

**Narration (EN)**

> Not one of those n functionals can be dropped. The sequence on screen has first coordinate zero throughout, so the first functional alone reports convergence, while the norm is n and runs to infinity. Whichever is left out, its null space is what the test cannot see.

**動畫**

紅色的點沿著縱軸往上排（ηₙ = ⟨0, n⟩），上方一個箭頭表示繼續往上；橫軸上只有原點一個青綠色的點——那是 E₁ 看得到的全部。

## Beat 4 — 弱收斂，以及有限維的等價 / weak convergence, and the finite-dimensional equivalence
*配音長度：中文 21.4s ／ 英文 18.2s*

**畫面公式**

```
弱收斂，以及有限維的等價   |   weak convergence, and the finite-dimensional equivalence
ξ ₙ → ξ    ⇒    λ ( ξ ₙ ) → λ ( ξ )            dim V < ∞   ⇒   ⇔
```

**旁白（繁中）**

> 一般的賦範空間裡，對偶空間是有界線性泛函的集合，每個泛函作用上去都收斂就定義成弱收斂。範數收斂推得弱收斂，在任何賦範空間都成立，理由就是剛剛那行估計。定理 12.1 說有限維時反過來也對。

**Narration (EN)**

> In a general normed space the dual is the bounded linear functionals, and convergence under every one of them defines weak convergence. Norm convergence gives weak convergence anywhere, by the estimate just made. Theorem 12.1 says the converse holds in finite dimension.

**動畫**

兩個框：範數收斂與弱收斂。向右的黃色箭頭標「任何賦範空間」，向左的紅色箭頭標「有限維才有」。底下寫 V* = Hom(V, ℝ)。

## Beat 5 — 積分的弱定義 / the weak definition of the integral
*配音長度：中文 21.5s ／ 英文 17.2s*

**畫面公式**

```
積分的弱定義   |   the weak definition of the integral
λ ( ∫ ₐ ᵇ f )    =    ∫ ₐ ᵇ λ ( f ( t ) )  d t
```

**旁白（繁中）**

> 接下來用同一招，把參數化弧的積分與微分丟回單變數實函數的標準微積分。泛函一作用，複合就是實值連續函數，它的積分早就有。積分的弱定義是：∫f 是那個唯一的向量，每個泛函在它上面的值等於複合的積分。

**Narration (EN)**

> The same device throws the integration and differentiation of parametrized arcs back to the calculus of real functions of one variable. A functional applied gives a continuous real function whose integral we have; the weak integral is the vector matching those.

**動畫**

左邊弧 f 與它的積分向量 ⟨1, 1⟩（黃色箭頭）；右邊 λ₁∘f 的圖，底下打滿垂直細線表示面積，數值 1.5000 標在上方。右側表格把五個泛函的 ∫λ∘f 與 λ(∫f) 並排。

## Beat 6 — 為什麼那個向量唯一 / why that vector is unique
*配音長度：中文 20.3s ／ 英文 17.3s*

**畫面公式**

```
為什麼那個向量唯一   |   why that vector is unique
λ  ↦  ∫ ₐ ᵇ λ ∘ f    ∈    V * *    ≅    V
```

**旁白（繁中）**

> 唯一性要有理由。泛函映到那個積分的對應是線性的，所以它是二次對偶空間裡的元素；而第 2 章定理 3.2 說，那裡每個元素都由原空間唯一一個向量給出。於是這樣定義合法，積分天生跟泛函交換。

**Narration (EN)**

> Uniqueness needs a reason. Sending a functional to that integral is itself linear, so it lies in the second dual, and the natural isomorphism of chapter 2 says every element there comes from exactly one vector. So integration commutes with functionals by construction.

**動畫**

上排 V* →（λ ↦ ∫λ∘f）→ ℝ，下排 V** ≅ V，底下一行是線性的檢查：λ = 2λ₁ − 3λ₂ 時兩邊都是 1.2000。

## Beat 7 — 微分照抄同一句話 / differentiation reads the same way
*配音長度：中文 19.2s ／ 英文 14.6s*

**畫面公式**

```
微分照抄同一句話   |   differentiation reads the same way
( λ ∘ f ) ′ ( x ₀ )    =    λ ( f ′ ( x ₀ ) )
```

**旁白（繁中）**

> 微分照抄。如果所有複合都在一點可微，那把泛函映到那個導數也是線性的——導數對函數是線性的——所以同樣有唯一的向量對每個泛函成立。把它定義成 f 撇。微分也跟泛函交換。

**Narration (EN)**

> Differentiation reads the same way. If all the composites are differentiable at a point, sending a functional to that derivative is linear, since derivatives are linear in the function, so again one vector works for every functional.

**動畫**

λ₂∘f 的圖（青綠色）與它在 x₀ = 0.7 的切線（紅色），切點標成黃點。右側是三個步長的中央差商與誤差：1.7e-03 → 1.7e-05 → 1.7e-07。

## Beat 8 — 微積分基本定理變成一行 / the fundamental theorem in one line
*配音長度：中文 17.5s ／ 英文 17.4s*

**畫面公式**

```
微積分基本定理變成一行   |   the fundamental theorem in one line
F ( x ) = ∫ ₐ ˣ f    ⇒    ( λ ∘ F ) ′ = λ ∘ f    ⇒    F ′ = f
```

**旁白（繁中）**

> 微積分基本定理於是變成一行。設 F 是 f 從左端點積到 x，弱定義給出複合等於複合的積分；標準的基本定理把它微分掉；再用微分的弱定義翻回來，就得到 F 可微而 F 撇 等於 f。

**Narration (EN)**

> The fundamental theorem of calculus becomes one line. Let F integrate f from the left endpoint to x. The weak definition turns the composite into an integral, the standard theorem differentiates it, and the weak definition of the derivative turns the answer back into f.

**動畫**

同一個平面上兩條弧：f（青綠色）與 F（紫色）。F 在 x₀ 的紅色切向量與 f(x₀) 的青綠色位置向量平行且等長——這就是 F′ = f。右側是 λ₁∘F 的中央差商表。

## Beat 9 — 弱方法拿不到的那一個 / the one weak methods do not reach
*配音長度：中文 20.6s ／ 英文 16.2s*

**畫面公式**

```
弱方法拿不到的那一個   |   the one weak methods do not reach
‖ α * * ‖   =   ‖ α ‖            sup  | λ ( α ) | / ‖ λ ‖   =   ‖ α ‖
```

**旁白（繁中）**

> 有一個結論弱方法拿不到：積分的範數不超過區間長度乘上 f 的上界範數。它要的是定理 12.2——二次對偶像的範數等於原向量的範數。這要找到一個範數一的泛函把範數取到，幾何上是單位球面的切超平面。

**Narration (EN)**

> One conclusion weak methods do not reach: the norm of the integral is at most the length of the interval times the uniform norm. It needs Theorem 12.2, that the second dual image has the same norm, which asks for a functional of norm one attaining it.

**動畫**

左邊是一範數下半徑 2 的菱形（青綠色），右上那一整條邊畫成紅色——那就是切線碰到球面的地方，兩端再用紅色虛線延伸出去；α = ⟨1, 1⟩ 是那條邊的中點。右邊是 |λ(α)| 沿著對偶單位球面（正方形）一圈的圖，兩個尖峰正好碰到 2.0000 那條虛線。

## Beat 10 — 最後那一串不等式 / the chain that finishes it
*配音長度：中文 22.3s ／ 英文 17.0s*

**畫面公式**

```
最後那一串不等式   |   the chain that finishes it
‖ ∫ ₐ ᵇ f ‖    ≤    ( b − a )  ‖ f ‖ ∞
```

**旁白（繁中）**

> 書上說這種切平面顯然存在，可是這門課不證。假設了它，剩下是一串不等式：那個值不超過長度乘上複合的最大值，再不超過長度乘上泛函的範數乘上上界範數。兩端一比就是要的不等式。第 4 章到此結束。

**Narration (EN)**

> The book calls such tangent planes geometrically evident and drops the matter. Granting it, the rest is a chain: the value is at most the length times the maximum of the composite, then times the norm of the functional and the uniform norm. The two ends give the inequality.

**動畫**

兩條同尺的橫線：青綠色是 ‖∫f‖₁ = 2.0000，紅色是 (b−a)‖f‖∞ = 2.2214，虛線標出兩者的差；底下寫出比值 0.9003 與兩個因子。
