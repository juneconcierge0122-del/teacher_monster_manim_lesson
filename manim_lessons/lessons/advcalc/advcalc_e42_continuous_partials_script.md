# advcalc E42 — 第 3 章：連續偏微分與乘積規則

Chapter 3: Continuous Partials and the Product Rule

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 8 節的後段（書頁 154–155）。書頁 155–156 是習題 8.1–8.10，第 9 節從書頁 156 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e42_continuous_partials.py`（`AdvCalcE42ZH` / `AdvCalcE42EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[42]` / `FORMULAS_ADVCALC[42]`）
- 配音：`manim_lessons/samples/audio_e42/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.08 分（185 秒）／英文 2.99 分（179 秒）

## 反例、兩步估計、雙線性映射，三段都算過

- **開場的反例** 是 `xy / (x² + y²)`，原點補零。場景檔斷言兩個偏導數在原點都是零、
  沿對角線的值恆等於 0.5、而它跟原點的值差超過 0.4——所以它連連續都不是，遑論可微。
  畫面用「單位圓上的值」把它畫出來：兩個座標軸方向是零（橘點），中間的紅點卻是 0.5。
- **定理 8.2 的兩步估計** 在 `sin(a)·b + a·b²` 上實際走了一遍：第一步只動第一個變數、
  第二步只動第二個，兩步各自的商與合起來的商都列在畫面上，並斷言三個序列都單調掉到零。
- **引理 8.3 的雙線性映射** 用的是平行四邊形的有向面積 `u₁v₂ − u₂v₁`。
  斷言它在單位圓上的界剛好是 1，斷言引理給的微分公式的餘項掉到零。
- **定理 8.4** 用 `g(t) = (t, t²)`、`h(t) = (1 + t, 3t)` 算：兩項是 2 與 −1，加起來 1，
  直接對合成微分也是 1。刻意讓其中一項是負的，並且斷言它是負的——
  免得看起來像「兩個正數相加」那種乘積規則。

**這一集修掉一個真的錯。** beat 8 初稿的三行算式裡混進了中文（而且是簡體），
可是那三行是用 `_sym` 畫的、語言無關，英文版就會出現中文。改成純符號，
文字全部移到底下的雙語列。這是 PLAYBOOK 第 7 節那條規則的又一次重演。

---

## Beat 0 — 偏微分存在，還是可能不可微 / partials can exist with no differential
*配音長度：中文 18.3s ／ 英文 17.4s*

**畫面公式**

```
偏微分存在，還是可能不可微   |   partials can exist with no differential
∂ f / ∂ x ( 0 )  =  ∂ f / ∂ y ( 0 )  =  0              f ( t , t )  =  1 / 2
```

**旁白（繁中）**

> 上一集留了一個問題：偏微分全部存在，能不能推出可微？答案一般是不行。畫面上這個函數在原點的兩個偏導數都是零，可是沿對角線走過去它恆等於二分之一，連連續都不是。

**Narration (EN)**

> The previous episode left a question: do all the partial differentials existing force differentiability? In general no. On screen a function whose two partial derivatives at the origin are both zero, yet which is one half all along the diagonal, so not even continuous.

**動畫**

藍色是反例在單位圓上的值：兩個橘點（座標軸方向）是零，紅點（對角線方向）是 0.5。

## Beat 1 — 定理 8.2：加上「連續」就夠了 / Theorem 8.2: continuity is enough
*配音長度：中文 15.1s ／ 英文 16.3s*

**畫面公式**

```
定理 8.2：加上「連續」就夠了   |   Theorem 8.2: continuity is enough
dF ⁱ :  A  →  Hom ( V ᵢ , W )              α  ↦  dF ⁱ ₐ
```

**旁白（繁中）**

> 但只要再要求一件事就夠了：偏微分不只在每一點存在，而且對那個點是連續的。定理 8.2 說這樣就推得出可微，而且推出來的微分本身也是連續的。

**Narration (EN)**

> One more requirement is enough: the partial differentials should not merely exist at each point but depend continuously on that point. Theorem 8.2 says that forces differentiability, and the resulting differential is itself continuous.

**動畫**

兩個偏微分的方框（各自是一個從 A 到 Hom 的映射），箭頭繞一圈指到整個微分的方框。

## Beat 2 — 候選的形式已經被鎖死 / the candidate's form is already pinned
*配音長度：中文 18.2s ／ 英文 17.1s*

**畫面公式**

```
候選的形式已經被鎖死   |   the candidate's form is already pinned
dF ₐ     =     Σ  dF ⁱ ₐ ∘ π ᵢ
```

**旁白（繁中）**

> 開始證之前先注意，形式已經被鎖死了：如果微分存在，引理 8.2 加上投影與嵌入的恆等式，就逼著它必須等於各偏微分接上投影再求和。所以要證的只剩「這個候選真的是微分」。

**Narration (EN)**

> Before the proof, notice the form is already pinned down. If the differential exists, Lemma 8.2 together with the projection and injection identities forces it to be the sum of the partials composed with the projections. Only that this candidate works is left to prove.

**動畫**

三行推導：引理 8.2、投影嵌入的恆等式、逼出候選的唯一形式。

## Beat 3 — 工具是上一集那條推論 / the tool is the previous corollary
*配音長度：中文 17.3s ／ 英文 16.2s*

**畫面公式**

```
工具是上一集那條推論   |   the tool is the previous corollary
‖ dG ᵦ − T ‖  ≤  ε        ⇒        ‖ ΔG ᵦ ( ξ ) − T ( ξ ) ‖  ≤  ε ‖ ξ ‖
```

**旁白（繁中）**

> 證明用的是上一集那條推論：微分跟一個固定的線性映射差不超過 ε，變化量跟它作用出來的結果也就差不超過 ε 乘上位移。這裡那個固定的映射，取的就是中心點的偏微分。

**Narration (EN)**

> The proof uses the previous episode's corollary: if the differential stays within epsilon of a fixed linear map, then the change stays within epsilon times the displacement of that map applied. Here the fixed map is taken to be the partial differential at the centre.

**動畫**

紫色是固定的線性映射 T 的像，紅色是真正的變化量，兩者相差多少由微分跟 T 差多少控制。

## Beat 4 — 走法：一次只動一個變數 / the route: one variable at a time
*配音長度：中文 15.7s ／ 英文 14.9s*

**畫面公式**

```
走法：一次只動一個變數   |   the route: one variable at a time
F ( α + ξ , β + η )   →   F ( α , β + η )   →   F ( α , β )
```

**旁白（繁中）**

> 走法是分兩步。第一步只動第一個變數，第二個變數先停在已經移好的位置；第二步再只動第二個變數。每一步都只剩一個變數在動，所以那條推論用得上。

**Narration (EN)**

> The route goes in two steps. First move only the first variable, leaving the second parked where it has already been moved to; then move only the second. Each step has one variable in motion, which is exactly what the corollary needs.

**動畫**

一個直角三角形：灰色虛線是真正要估的位移，兩支箭頭是實際走的兩步。

## Beat 5 — 兩步的誤差加起來還是小 / the two errors still add up small
*配音長度：中文 14.9s ／ 英文 14.8s*

**畫面公式**

```
兩步的誤差加起來還是小   |   the two errors still add up small
‖ ΔF ( ξ , η ) − T ( ξ , η ) ‖    ≤    ε ( ‖ ξ ‖ + ‖ η ‖ )
```

**旁白（繁中）**

> 兩步的誤差各不超過 ε 乘上那一步的位移，加起來就不超過 ε 乘上整個位移。畫面上那一列是實際算出來的商，三個取樣點確實一路掉到零。

**Narration (EN)**

> Each step's error is at most epsilon times that step's displacement, so together they are at most epsilon times the whole displacement. The column on screen holds the quotients actually computed, and across three samples they do fall to zero.

**動畫**

一張三欄的表：第一步的商、第二步的商、合起來的商，三個取樣點都掉到零。

## Beat 6 — 定理 8.3：n 個因子用歸納 / Theorem 8.3: n factors by induction
*配音長度：中文 15.0s ／ 英文 15.8s*

**畫面公式**

```
定理 8.3：n 個因子用歸納   |   Theorem 8.3: n factors by induction
V ₁ × V ₂ × V ₃    =    ( V ₁ × V ₂ ) × V ₃
```

**旁白（繁中）**

> 定理 8.3 把因子數推廣到 n 個，做法是歸納：先把前兩個因子併成一個，再一次多加一個。連續性讓每一步都接得上去，所以推廣不必重寫證明。

**Narration (EN)**

> Theorem 8.3 extends the factor count to n by induction: merge the first two factors into one, then add a factor at a time. Continuity is what lets each step attach to the last, so the extension needs no new proof.

**動畫**

三個因子的方框，兩兩合併的過程畫成兩層——歸納的每一步都是兩個因子的情形。

## Beat 7 — 引理 8.3：有界雙線性映射 / Lemma 8.3: bounded bilinear maps
*配音長度：中文 16.6s ／ 英文 16.9s*

**畫面公式**

```
引理 8.3：有界雙線性映射   |   Lemma 8.3: bounded bilinear maps
d ω ( ξ , η )     =     ω ( α , η )   +   ω ( ξ , β )
```

**旁白（繁中）**

> 接著是這一節的第二個主角：有界雙線性映射。引理 8.3 說它處處可微，而且微分就是「一邊固定、另一邊動」的那兩項相加，跟大家熟悉的乘法微分長得一模一樣。

**Narration (EN)**

> Then the section's second subject: bounded bilinear maps. Lemma 8.3 says such a map is everywhere differentiable and its differential is the sum of the two terms got by holding one side fixed and moving the other, exactly like the familiar product rule.

**動畫**

兩個向量與它們張成的平行四邊形（那就是這個雙線性映射的值），右邊是餘項的表。

## Beat 8 — 固定一邊，剩下的就是線性的 / hold one side and what is left is linear
*配音長度：中文 17.7s ／ 英文 15.5s*

**畫面公式**

```
固定一邊，剩下的就是線性的   |   hold one side and what is left is linear
‖ ω ( ξ , η ) ‖  ≤  b ‖ ξ ‖ ‖ η ‖              b  =  1
```

**旁白（繁中）**

> 證明很短。把一邊固定住，剩下的就是線性的，所以那個偏微分就是它自己；而「固定的那一邊」對點又是線性的，所以偏微分是連續的。定理 8.2 一套上去就完成了。

**Narration (EN)**

> The proof is short. Hold one side fixed and what remains is linear, so that partial differential is the map itself; and the held side depends linearly on the point, so the partial is continuous. Theorem 8.2 then closes it.

**動畫**

三行純符號的推導：固定一邊之後是線性映射、偏微分等於它自己、對點又是線性所以連續。

## Beat 9 — 定理 8.4：一般的乘積規則 / Theorem 8.4: the general product rule
*配音長度：中文 18.2s ／ 英文 18.4s*

**畫面公式**

```
定理 8.4：一般的乘積規則   |   Theorem 8.4: the general product rule
dF ᵦ ( ζ )  =  ω ( g ( β ) , dh ᵦ ( ζ ) )  +  ω ( dg ᵦ ( ζ ) , h ( β ) )
```

**旁白（繁中）**

> 定理 8.4 是一般的乘積規則：兩個可微的函數丟進一個有界雙線性映射，結果可微，而且微分是「前面配後面的微分」加上「前面的微分配後面」。畫面上算出來是二加負一等於一。

**Narration (EN)**

> Theorem 8.4 is the general product rule: feed two differentiable functions into a bounded bilinear map and the result is differentiable, with differential the first against the second's differential plus the first's differential against the second. On screen, two plus minus one.

**動畫**

A、X × Y、W 三個方框，下方是 2、−1、1 三個算出來的數。

## Beat 10 — 三條規則到齊，而且不用座標 / three rules, and no coordinates anywhere
*配音長度：中文 18.1s ／ 英文 15.8s*

**畫面公式**

```
三條規則到齊，而且不用座標   |   three rules, and no coordinates anywhere
d ( F + G )   ,    d ( G ∘ F )   ,    d ( F G )
```

**旁白（繁中）**

> 這一節到此結束。加法、合成、乘積三條規則，在賦範空間裡全部有了，而且完全不需要座標。下一集把它們搬到實數的 n 維空間，那裡才會出現偏導數與雅可比矩陣。

**Narration (EN)**

> That ends the section. Sums, composites and products all have their rules in a normed space now, and none of them needed coordinates. Next time they move to real n-space, where partial derivatives and the Jacobian matrix finally appear.

**動畫**

三個方框各寫一條規則：和、合成、乘積。

---

## 「連續」兩個字就是全部的代價

上一集的問題是「偏微分全部存在能不能推出可微」。答案是不能——開場那個反例的兩個偏導數
都存在，它卻連連續都不是。定理 8.2 補的條件只有一個詞：那些偏微分要對點連續。
這一集的前半段就是在說明為什麼這一個詞夠用。

## 乘積規則其實是雙線性映射的推論

書上不直接證乘積規則，而是先證「有界雙線性映射處處可微」（引理 8.3），
再把定理 8.1（值域是乘積）與鏈鎖規則接上去。這樣寫的好處是同一個證明涵蓋了所有的「乘積」——
數乘向量、內積、外積、矩陣乘法，只要它是有界雙線性的。
