# advcalc E65 — 第 4 章：參數化弧的積分

Chapter 4: The Integral of a Parametrized Arc

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 10 節「參數化弧的積分」（書頁 236–238）。

**§10 的內容收在書頁 238**，239–240 是習題 10.1–10.15，依 PLAYBOOK 第 8 節不做解答；第 11 節從書頁 240 起。**OUTLINE 把 §10 寫成 236–240，是把習題頁算了進去——那張表的頁碼第七次這樣錯。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e65_arc_integral.py`（`AdvCalcE65ZH` / `AdvCalcE65EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[65]` / `FORMULAS_ADVCALC[65]`）
- 配音：`manim_lessons/samples/audio_e65/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.39 分（204 秒）／英文 3.21 分（193 秒）

## 這一章的最後一塊拼圖

書上開宗明義：這是第 4 章對完備性的**最後一個應用**，而且說得很直白——
**之所以拖到現在才做積分，就是因為要證積分存在，非用值域的完備性不可。**

結構是「先造一把通用的工具，再拿它做一件具體的事」：

1. **定理 10.1** 是一條跟積分完全無關的一般結果：子空間上的有界線性映射，
   可以唯一地延拓到閉包上，**而且範數一模一樣**。
2. 然後把它套上去：積分對階梯函數是顯然的（就是 Σ αᵢΔtᵢ），
   那個映射被區間長度界住，連續函數落在階梯函數的閉包裡（**引理 10.1，緊緻性在這裡回來**），
   於是定理 10.2 把 Riemann 積分造出來。
3. 可加性與微積分基本定理（10.3）跟著出來。

**第 4 章到此結束**——完備性從 Cauchy 序列一路鋪到這裡，最後造出了積分。

## 整集跑同一段弧

用的是 f(t) = ⟨cos t, sin t⟩，從 0 積到 π／2，**積分剛好是 ⟨1, 1⟩**（解析解），
所以下面每一個誤差都是真的誤差，不是估的：

| 檢查 | 數字 |
|---|---|
| Riemann 和（4／8／16／32 段）對精確值的誤差 | 0.2783 → 0.1389 → 0.0694 → 0.0347 |
| 界：‖∫f‖ 對 ‖f‖∞(b−a) | 1.4142 ≤ 1.5708 |
| 階梯逼近：一致距離對網目（n = 4／8／16） | 0.3902 ≤ 0.3927、0.1960 ≤ 0.1963、0.0981 ≤ 0.0982 |
| 可加性 | ⟨0.7071, 0.2929⟩ + ⟨0.2929, 0.7071⟩ = ⟨1, 1⟩ |
| 差商（h = 0.1／0.01／0.001） | 0.049986 → 0.005000 → 0.000500 |

階梯逼近那一列特別值得看：**這段弧的速率是一，所以一致距離必然不超過網目**，
程式對每一段取 41 個取樣點掃過去驗證。這正是引理 10.1 的證明在做的事。

## 這一輪抓到的錯

**probe 幀抓到一處**：beat 4 的階梯函數第一段，畫的那個分量的值是 0，
所以那一段正好疊在座標軸上，看起來像「那一段什麼都沒有」。
把 α₁ 從 ⟨1, 0⟩ 改成 ⟨1, 0.5⟩ 之後三段才都看得見。
**這跟 E64 的「曲率太小畫不出差別」是同一類**：值本身沒錯，可是畫出來讀不到。

`bounds` 抓到兩處座標軸畫到 y = 1.31（只超過上限 0.01）。

**signed zero 又出現了。** 階梯函數第一個分量的和是 −5.55e-17，
`f"{v:.1f}"` 印成 `-0.0`。**這是 E63 記過的同一個坑**，這次不再在每個 f-string 上補 `abs()`，
而是加一個 `_clean()` 把捨入誤差級的值歸零：

```python
def _clean(v):
 """Round a rounding-error-sized value to a true zero, so it prints as 0.0."""
 return 0.0 if abs(v) < 1e-12 else v
```

---

## Beat 0 — 完備性的最後一個應用 / the last application of completeness
*配音長度：中文 24.5s ／ 英文 16.9s*

**畫面公式**

```
完備性的最後一個應用   |   the last application of completeness
∫ ₐ ᵇ  f ( t )  d t                    f  :  [ a , b ]  →  W
```

**旁白（繁中）**

> 第 10 節是這一章對完備性的最後一個應用。書上先證一個很一般的延拓定理，再拿它把 Riemann 積分造出來——把只對階梯函數有意義的初等積分，延拓到連續函數上。書上特別說明：之所以拖到現在才做，是因為要證積分存在，非用值域的完備性不可。

**Narration (EN)**

> Section 10 is the last application of completeness in the chapter. A very general extension theorem is proved first, and then used to build the Riemann integral of a continuous function as an extension of an elementary integral that only makes sense for step functions.

**動畫**

那一段四分之一圓弧，加上從原點指出去的積分向量 ⟨1, 1⟩——整集都用這一段弧。

## Beat 1 — 定理 10.1：延拓到閉包 / Theorem 10.1: extending to the closure
*配音長度：中文 16.3s ／ 英文 18.4s*

**畫面公式**

```
定理 10.1：延拓到閉包   |   Theorem 10.1: extending to the closure
T  ∈  Hom ( U , W )        ⇒        ∃ ! S  ∈  Hom ( U ‾ , W )  ,  ‖ S ‖ = ‖ T ‖
```

**旁白（繁中）**

> 定理 10.1：U 是某個賦範空間的子空間，T 是從 U 到 Banach 空間 W 的有界線性映射。那麼 T 可以唯一地延拓成閉包上的有界線性映射，而且延拓後的範數跟原來一樣。

**Narration (EN)**

> Theorem 10.1: let U be a subspace of a normed space and T a bounded linear map from U into a Banach space W. Then T extends, in exactly one way, to a bounded linear map on the closure of U, and the extension has the same norm as T.

**動畫**

U 套在閉包 Ū 裡，兩支箭頭指向 W：短的是 T（只從 U 出發），長的是 S（從整個閉包出發）。

## Beat 2 — 證明：Cauchy 送過去還是 Cauchy / the proof: Cauchy goes to Cauchy
*配音長度：中文 21.3s ／ 英文 18.2s*

**畫面公式**

```
證明：Cauchy 送過去還是 Cauchy   |   the proof: Cauchy goes to Cauchy
ξ ₙ  →  α          { T ( ξ ₙ ) }   Cauchy          T ( ξ ₙ )  →  β
```

**旁白（繁中）**

> 證明很短。取閉包裡的一點，再取 U 裡收斂到它的一個序列。那個序列是 Cauchy 的，所以照第 7 節的引理，它的像也是 Cauchy 的，而 W 完備就給出極限。換一個序列會得到同一個極限，所以那個值只跟點有關。

**Narration (EN)**

> The proof is short. Take a point of the closure and a sequence in U converging to it. That sequence is Cauchy, so its images are Cauchy by the lemmas of section 7, and completeness supplies a limit. A second sequence gives the same limit, so the value depends only on the point.

**動畫**

上下兩條線：上面是 ξₙ → α，下面是 T(ξₙ) → β，中間一支箭頭標著 T。
**用到的是第 7 節的引理 7.1 與 7.3——這一章前面鋪的每一塊都在這裡派上用場。**

## Beat 3 — 為什麼範數不會變 / why the norm does not change
*配音長度：中文 15.9s ／ 英文 16.4s*

**畫面公式**

```
為什麼範數不會變   |   why the norm does not change
‖ S ( α ) ‖  =  lim ‖ T ( ξ ₙ ) ‖  ≤  ‖ T ‖ ‖ α ‖
```

**旁白（繁中）**

> 範數相等的理由很乾淨：延拓在一點的範數是那些像的範數的極限，不超過 T 的範數乘上那一點的範數。所以 T 的範數界住延拓；而延拓又包含 T，兩者只能相等。

**Narration (EN)**

> The norms match for a clean reason. The norm of the extension at a point is the limit of the norms of the images, which is at most the norm of T times the norm of the point. So T bounds the extension, and since the extension includes T, the two norms are equal.

**動畫**

三列不等式加一條虛線與結論「S ⊃ T ⇒ ‖S‖ = ‖T‖」——兩邊夾起來，只能相等。

## Beat 4 — 分割與階梯函數 / partitions and step functions
*配音長度：中文 17.5s ／ 英文 15.2s*

**畫面公式**

```
分割與階梯函數   |   partitions and step functions
A  =  { t ᵢ } ₀ ⁿ        a = t ₀ < t ₁ < … < t ₙ = b        f  =  α ᵢ
```

**旁白（繁中）**

> 接下來是造法。一個區間的分割，就是一個含有兩個端點的有限點集。階梯函數是指：在某個分割的那些開區間上都是常數的函數；至於分點本身的值，可以是任何東西。

**Narration (EN)**

> Now the construction. A partition of an interval is a finite set of points containing both ends. A step function is one that is constant on the open intervals of some partition; the values at the dividing points themselves are allowed to be anything at all.

**動畫**

分割 {0, 0.3, 0.7, 1} 上的階梯函數，畫的是第二個分量；分點用紅點與虛線標出。
右側列出三個 ℝ² 的值。

## Beat 5 — 跟用哪個分割無關 / independent of the partition used
*配音長度：中文 19.9s ／ 英文 15.8s*

**畫面公式**

```
跟用哪個分割無關   |   independent of the partition used
∫ ₐ ᵇ  f    =    Σ ₁ ⁿ   α ᵢ  Δ t ᵢ                Δ t ᵢ  =  t ᵢ  −  t ᵢ ₋ ₁
```

**旁白（繁中）**

> 它的積分就是那個顯然的和：每個值乘上自己那一段的長度。要檢查的是這個和跟用哪個分割描述無關。加一個點會把一項拆成兩項，可是加回去還是原來那一項；任意兩個分割則透過共同細分來比。

**Narration (EN)**

> Its integral is the obvious sum: each value times the length of its interval. This has to be checked not to depend on the partition used. Adding one point splits one term into two that add back to it, and two partitions are compared through their common refinement.

**動畫**

同一個階梯函數，在 0.5 加一條紅色虛線；右側把兩個分割算出來的和並排：
Σ = ⟨0.00, 1.25⟩，Σ′ = ⟨0.00, 1.25⟩——**加一個點，和一點也沒變。**

## Beat 6 — 積分是有界線性映射 / integration is a bounded linear map
*配音長度：中文 18.1s ／ 英文 17.8s*

**畫面公式**

```
積分是有界線性映射   |   integration is a bounded linear map
‖ ∫ ₐ ᵇ  f ‖      ≤      ‖ f ‖ ∞  ( b − a )
```

**旁白（繁中）**

> 階梯函數構成一個向量空間，而積分在上面是線性的。真正關鍵的是那個界：積分的範數不超過函數的一致範數乘上區間長度。所以積分是一個有界線性映射，界就是區間的長度。

**Narration (EN)**

> The step functions form a vector space, and integration is linear on it. What matters is the bound: the norm of the integral is at most the uniform norm of the function times the length of the interval. So integration is a bounded linear map, with the length as its bound.

**動畫**

兩條長條並排：青色是實際的 ‖∫f‖ = 1.4142，紅色是上界 1.5708。**界是真的，而且不算鬆。**

## Beat 7 — 引理 10.1：連續函數在閉包裡 / Lemma 10.1: the continuous ones are in the closure
*配音長度：中文 17.7s ／ 英文 18.7s*

**畫面公式**

```
引理 10.1：連續函數在閉包裡   |   Lemma 10.1: the continuous ones are in the closure
𝒞 ( [ a , b ] , W )      ⊂      ℰ ‾
```

**旁白（繁中）**

> 引理 10.1：每一個連續函數都落在階梯函數的閉包裡。緊緻性在這裡回來了——閉區間上的連續函數均勻連續，所以只要分割夠細，就造得出一個處處與它相差不到 ε 的階梯函數。

**Narration (EN)**

> Lemma 10.1: every continuous function lies in the closure of the step functions. This is where compactness comes back. A continuous function on a closed interval is uniformly continuous, so a partition with a fine enough mesh gives a step function within epsilon of it everywhere.

**動畫**

弧的第一個分量（青色曲線）與取樣出來的階梯函數（紅色橫線）疊在一起；
右側列出三個 n 的網目 h 與實際量到的 ‖f − g‖∞——**一致距離永遠不超過網目。**

## Beat 8 — 定理 10.2：把前面重述一次 / Theorem 10.2: the recapitulation
*配音長度：中文 17.9s ／ 英文 18.7s*

**畫面公式**

```
定理 10.2：把前面重述一次   |   Theorem 10.2: the recapitulation
J ( f )  =  lim  ∫ ₐ ᵇ  f ₙ                ‖ J ‖    ≤    b  −  a
```

**旁白（繁中）**

> 定理 10.2 就是把前面重述一次。如果 W 是 Banach 空間，積分就唯一地延拓成連續函數上的有界線性映射，值是任何一列收斂到 f 的階梯函數的積分的極限，而它的範數不超過區間長度。

**Narration (EN)**

> Theorem 10.2 is the recapitulation. If W is a Banach space, the integral extends uniquely to a bounded linear map on the continuous functions, given by the limit of the integrals of any sequence of step functions converging to f, and its norm is at most the length.

**動畫**

對數尺度上一條下降的折線：四段、八段、十六段、三十二段的 Riemann 和對精確值的誤差，
右側列出實際數值 0.2783 → 0.0347。

## Beat 9 — 可加性，就是一個向量加法 / additivity is a vector addition
*配音長度：中文 17.0s ／ 英文 16.7s*

**畫面公式**

```
可加性，就是一個向量加法   |   additivity is a vector addition
∫ ₐ ᵇ  f      =      ∫ ₐ ᶜ  f    +    ∫ ᶜ ᵇ  f
```

**旁白（繁中）**

> 可加性跟著出來。對階梯函數而言，把和在中間某一點拆開是顯然的；對連續函數，那個等式就跟著極限傳過去。從 a 到 b 的積分，等於從 a 到 c 加上從 c 到 b。

**Narration (EN)**

> Additivity comes along. For a step function, splitting the sum at an interior point is immediate, and for a continuous function the identity passes to the limit. The integral from a to b is the integral from a to c plus the integral from c to b.

**動畫**

平面上一個**向量三角形**：青色 ⟨0.7071, 0.2929⟩ 接上紅色 ⟨0.2929, 0.7071⟩，
剛好是橘色的 ⟨1, 1⟩。切點取在四十五度。

## Beat 10 — 定理 10.3：基本定理還在 / Theorem 10.3: the fundamental theorem survives
*配音長度：中文 16.6s ／ 英文 19.1s*

**畫面公式**

```
定理 10.3：基本定理還在   |   Theorem 10.3: the fundamental theorem survives
F ( x )  =  ∫ ₐ ˣ  f ( t )  d t                F ′  =  f
```

**旁白（繁中）**

> 而微積分基本定理還在。定理 10.3：f 連續，F 是從左端點積到 x 的積分，那麼 F 可微而且導函數就是 f。讓差商收斂的，正好就是 f 在那一點的連續性。

**Narration (EN)**

> And the fundamental theorem of calculus is still with us. Theorem 10.3: if f is continuous and F is its integral from the left endpoint to x, then F is differentiable and its derivative is f. Continuity at a point is exactly what makes the difference quotient converge there.

**動畫**

青色是 F、紅色是 f，在 x = 0.6 用虛線標出對應的兩點——**F 的斜率就是 f 的高度**。
右側用三個步長把差商的誤差列出來：0.049986 → 0.005000 → 0.000500。
