# advcalc E47 — 第 3 章：反映射定理

Chapter 3: The Inverse Mapping Theorem

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 11 節「隱函數定理」的中段（書頁 166–167）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e47_inverse_mapping.py`（`AdvCalcE47ZH` / `AdvCalcE47EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[47]` / `FORMULAS_ADVCALC[47]`）
- 配音：`manim_lessons/samples/audio_e47/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.03 分（182 秒）／英文 2.93 分（176 秒）

## 存在性，以及一個「局部」到底有多局部的例子

上一集的定理 11.1 假設隱函數已經存在。這一集講定理 11.2——它反過來製造那個函數，
代價是要求空間完備（有限維一定完備，所以在 ℝⁿ 上是白得的），而證明本身留到第 4 章。
定理 11.3 是它的特例：反映射定理。證明只有一行——令 `G(ξ, η) = ξ − H(η)`，
它對第二個變數的偏微分就是 `−dH_β`，可逆，隱函數定理直接套上去。

三個例子都算過：

- **分支**：`η² = ξ` 有正負兩支。取三個點 (1, 1)、(1, −1)、(0, 0)，
  用中央差商算第二個偏微分，斷言前兩個的絕對值大於 1（可逆）、第三個是零（不可逆），
  而且斷言前兩個異號——這樣「兩支」在畫面上才有意義。
- **原點確實壞掉**：那正是兩支黏起來、沒有單值解的地方。所以「可逆」不是裝飾，
  它剛好排除掉分支交會的位置。
- **局部而非全域**：取 E43 那個複數平方映射 `H(x) = (x₁² − x₂², 2x₁x₂)`，
  斷言 (1, 0.5) 與 (−1, −0.5) 有同一個像、而且兩點不同——所以全域不是單射；
  斷言它在 (1, 0.5) 的行列式等於 `4‖x‖²`（也就是 5），在原點是零；
  再用牛頓法把局部反函數逼出來，斷言它從像回到原來那一點，
  而且斷言它的雅可比矩陣（也是中央差商算的）等於原矩陣的反矩陣。

`bounds.py` 與 `collide.py` 都是零，可是 probe 幀抓到 beat 10：
兩個座標十字並排、中間沒有間隔，在畫面上糊成一個平面加一條多餘的直線，
完全看不出哪邊是定義域、哪邊是像。改成各自加一個淡框、中間留出一段空白、
並在框下標名字才讀得懂。

---

## Beat 0 — 上一集留下的缺口 / the gap the last episode left
*配音長度：中文 17.1s ／ 英文 16.6s*

**畫面公式**

```
上一集留下的缺口   |   the gap the last episode left
∃ F  ?               Ch 4
```

**旁白（繁中）**

> 上一集停在一個缺口：隱函數如果存在而且連續，那它可微；可是存在性本身沒有證。定理 11.2 就是那條存在性定理，這一集把它的內容講清楚，證明留到第 4 章。

**Narration (EN)**

> The previous episode stopped at a gap: an implicit function that exists and is continuous is differentiable, but existence itself was not proved. Theorem 11.2 is that existence theorem, and this episode states it, leaving the proof to chapter four.

**動畫**

左邊兩個方塊（dFₐ 存在、F 存在）各自用箭頭指向 E 46 與 E 47。
右側說明這一集講下面那一條，但證明仍留到第 4 章。

## Beat 1 — 定理 11.2：存在性 / Theorem 11.2: existence
*配音長度：中文 19.1s ／ 英文 19.2s*

**畫面公式**

```
定理 11.2：存在性   |   Theorem 11.2: existence
G ( α , β ) = 0  ,  ( dG ² ) ⁻¹ ∃           ⇒           ∃ ! F  :  M → B
```

**旁白（繁中）**

> 假設有四條：空間是有限維或者完備的、G 連續可微、在那一點 G 等於零、而且第二個偏微分在那一點可逆。結論是：α 附近有一顆球，上面存在唯一一個連續可微的 F，滿足那個恆等式。

**Narration (EN)**

> Four hypotheses: the spaces are finite dimensional or complete, G is continuously differentiable, G vanishes at the point, and the second partial differential inverts there. The conclusion: a ball about alpha carries a unique continuously differentiable F satisfying the identity.

**動畫**

左邊四個假設方塊由上而下排（空間完備、G ∈ C¹、G(α, β) = 0、(dG²)⁻¹ 存在），
一支箭頭指向右邊的結論方塊 ∃! F : M → B。

## Beat 2 — 「唯一」是局部的 / unique means locally unique
*配音長度：中文 16.8s ／ 英文 15.5s*

**畫面公式**

```
「唯一」是局部的   |   unique means locally unique
η ²  =  ξ                η  =  ± √ ξ
```

**旁白（繁中）**

> 「唯一」是局部的意思，不是全域的。畫面上 η 平方等於 ξ 這個方程，在 ξ 等於一附近有兩支解：正的根號與負的根號。挑哪一支，是由你指定的那個 β 決定的。

**Narration (EN)**

> Unique means locally unique, not globally. On screen the equation eta squared equals xi has two branches near xi equal to one, the positive and the negative root. Which branch you get is decided by the beta you named.

**動畫**

左邊一個座標十字，畫出側躺拋物線的上下兩支（不同顏色），
各自的取樣點打點並套一個小圓，表示定理只保證那顆球上唯一。

## Beat 3 — 兩支黏起來的地方 / where the branches join
*配音長度：中文 14.9s ／ 英文 14.7s*

**畫面公式**

```
兩支黏起來的地方   |   where the branches join
dG ²  =  2 η  =  0                  ⟨ 0 , 0 ⟩
```

**旁白（繁中）**

> 而在原點，第二個偏微分等於零，兩支解在那裡黏起來，定理就不適用了。所以「可逆」這個條件不是技術性的裝飾，它剛好排除掉分支交會的地方。

**Narration (EN)**

> At the origin the second partial differential vanishes and the two branches join, so the theorem does not apply there. Invertibility is therefore not a technical decoration: it excludes exactly the places where branches meet.

**動畫**

同一條拋物線整條畫成灰色，原點打紅點並套一個紅圈。
右側印出 dG² = 2η = 0，說明那裡定理不適用，而且確實沒有單值解。

## Beat 4 — 為什麼微分也連續 / why the differential is continuous too
*配音長度：中文 17.7s ／ 英文 15.8s*

**畫面公式**

```
為什麼微分也連續   |   why the differential is continuous too
dF   =   − ( dG ² ) ⁻¹ ∘ dG ¹                T  ↦  T ⁻¹
```

**旁白（繁中）**

> 為什麼結論裡的 F 不只可微、還連續可微？因為上一集那條公式裡出現的東西全都是連續的，而且「取反元素」這件事本身在算子範數下也是連續的，所以整條公式對點連續。

**Narration (EN)**

> Why is the F in the conclusion continuously differentiable and not merely differentiable? Because everything in the previous formula is continuous, and taking an inverse is continuous in the operator norm, so the whole formula depends continuously on the point.

**動畫**

左邊兩行式子（dF 的公式，以及兩個連續的映射 μ ↦ dG¹(μ) 與 T ↦ T⁻¹），
下面一個加框的 dF ∈ C⁰。

## Beat 5 — 一點可逆，附近都可逆 / invertible at a point, invertible nearby
*配音長度：中文 13.2s ／ 英文 12.1s*

**畫面公式**

```
一點可逆，附近都可逆   |   invertible at a point, invertible nearby
( dG ² ) ⁻¹ ∃   ⟨ α , β ⟩           ⇒           ( dG ² ) ⁻¹ ∃   ⟨ μ , ν ⟩
```

**旁白（繁中）**

> 所以第二個偏微分在一點可逆，就在附近整片都可逆，於是上一集的定理在整個鄰域上都適用，F 就在整個鄰域上可微，而且微分連續。

**Narration (EN)**

> So the second partial differential being invertible at one point makes it invertible on a whole neighborhood, the previous theorem applies throughout it, and F is differentiable there with a continuous differential.

**動畫**

左邊一團定義域，裡面一顆紅點套一個紅圈，圈內另有三顆小點。
右側說明可逆是開條件，所以一點的假設撐出一整片的結論。

## Beat 6 — 定理 11.3：反映射定理 / Theorem 11.3: the inverse mapping theorem
*配音長度：中文 15.1s ／ 英文 15.5s*

**畫面公式**

```
定理 11.3：反映射定理   |   Theorem 11.3: the inverse mapping theorem
( dH ᵦ ) ⁻¹  ∃                ⇒                ∃ H ⁻¹  :  M → B
```

**旁白（繁中）**

> 定理 11.3 是這條定理的一個特例，可是它有自己的名字：反映射定理。它說的是，如果 H 連續可微而且微分在一點可逆，那 H 在那一點附近就可逆。

**Narration (EN)**

> Theorem 11.3 is a special case with a name of its own: the inverse mapping theorem. It says that if H is continuously differentiable and its differential is invertible at a point, then H itself is invertible near that point.

**動畫**

左邊兩團（定義域與值域），上下各一支箭頭，上面標 H、下面標 F。
右側是定理 11.3 的假設與結論。

## Beat 7 — 證明只有一行 / the proof takes one line
*配音長度：中文 15.5s ／ 英文 17.3s*

**畫面公式**

```
證明只有一行   |   the proof takes one line
G ( ξ , η )    =    ξ   −   H ( η )
```

**旁白（繁中）**

> 證明只有一行：令 G 等於 ξ 減掉 H 作用在 η 上。這個 G 連續可微，而且它對第二個變數的偏微分就是負的 dH，題設說 dH 可逆，那負的它當然也可逆。

**Narration (EN)**

> The proof takes one line: set G to be xi minus H applied to eta. That G is continuously differentiable, and its partial differential in the second variable is minus dH; the hypothesis says dH inverts, so minus it inverts too.

**動畫**

左邊一個加框的 G(ξ, η) = ξ − H(η)，下面是 dG² = −dHᵦ。
右側說明把要證的東西寫成一個隱函數問題。

## Beat 8 — 隱函數定理一套就完成 / the implicit function theorem finishes it
*配音長度：中文 16.2s ／ 英文 16.6s*

**畫面公式**

```
隱函數定理一套就完成   |   the implicit function theorem finishes it
dG ²  =  − dH ᵦ              H ( F ( ξ ) )  =  ξ
```

**旁白（繁中）**

> 把隱函數定理套上去，得到的 F 就滿足「ξ 減掉 H 作用在 F 上等於零」，也就是 H 接上 F 是恆等映射。這正是「H 在那一點附近可逆」的意思，而 F 就是局部的反函數。

**Narration (EN)**

> Applying the implicit function theorem, the F it returns satisfies xi minus H of F equals zero, which says H composed with F is the identity. That is exactly what it means for H to be invertible near the point, and F is the local inverse.

**動畫**

左邊三行：隱函數定理交出來的恆等式、代回 G 的定義、收成 H ∘ F = I。
右側說明 F 就是 H 的局部反函數。

## Beat 9 — 推論：熟悉的那個說法 / the corollary: the familiar wording
*配音長度：中文 17.2s ／ 英文 15.0s*

**畫面公式**

```
推論：熟悉的那個說法   |   the corollary: the familiar wording
H  :  U  ↪  V                N  =  H [ U ]                N °  =  N
```

**旁白（繁中）**

> 推論是大家比較熟悉的說法：β 有一個開鄰域使得 H 在上面是單射，它的像是一個開集，而且反函數在那個開集上連續可微。要注意的是每一句都是局部的，沒有一句是全域的。

**Narration (EN)**

> The corollary is the familiar formulation: beta has an open neighborhood on which H is injective, its image is an open set, and the inverse is continuously differentiable there. Every clause is local and none of them is global.

**動畫**

左邊兩團灰色的集合，左邊團裡畫一個藍圈 U、右邊團裡畫一個紅色不規則的像 N = H[U]，
兩支箭頭一來一往。右側說明每一句都是局部的。

## Beat 10 — 局部可逆，不是全域 / locally invertible, not globally
*配音長度：中文 18.8s ／ 英文 17.5s*

**畫面公式**

```
局部可逆，不是全域   |   locally invertible, not globally
dF ₐ   =   ( dH ᵦ ) ⁻¹              H ( x )  =  H ( − x )
```

**旁白（繁中）**

> 畫面上那個映射就是 E43 那一個。它在每個非原點的地方都局部可逆，可是全域不是單射——兩個相反的點有同一個像。而反函數的微分就是原微分的反元素，回到上一集的第一個例子。

**Narration (EN)**

> The map on screen is the one from E43. It is locally invertible away from the origin, yet globally it is not injective: two opposite points share an image. And the inverse's differential is the inverse of the original's, back to last episode's first example.

**動畫**

左右各一個加框的座標平面（各自標上 ⟨x₁, x₂⟩ 與 H(x)）：左邊兩顆相反的點，
兩支箭頭同時指向右邊同一顆紅點。右側是 dHᵦ 與它的反矩陣。

---

## 「局部」在這一集出現了三次

三次的意思都不一樣，值得分開記：

1. **定理 11.2 的唯一性**是在球 M 上唯一，不是整條曲線上唯一（第 2 拍的兩支拋物線）。
2. **定理 11.3 的可逆**是在 β 的某個鄰域上可逆，不是在整個定義域上可逆（第 10 拍的例子）。
3. **推論裡的開集**：U 是 β 的開鄰域、H[U] 是開集、反函數在 H[U] 上連續可微。
   三句話全是局部的，沒有一句是全域的。

## 證明只有一行，可是不是白給的

`G(ξ, η) = ξ − H(η)` 這個改寫很便宜，貴的是它背後的定理 11.2，
而定理 11.2 的證明要用第 4 章的不動點定理。這一章從頭到尾都是這個模式：
陳述先給，存在性的證明押後。
