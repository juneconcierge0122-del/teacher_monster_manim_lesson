# advcalc E50 — 第 3 章：函數相依性

Chapter 3: Functional Dependence

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 13 節「函數相依性」（書頁 175–179）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e50_dependence.py`（`AdvCalcE50ZH` / `AdvCalcE50EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[50]` / `FORMULAS_ADVCALC[50]`）
- 配音：`manim_lessons/samples/audio_e50/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.18 分（191 秒）／英文 3.13 分（188 秒）

## 兩個方向的例外，才是這一節的內容

「其中一個是不是其他幾個的函數」與「像是不是一個二維子流形」幾乎是同一個問題，
可是兩個方向各有一個例外，而例外正是這一節在處理的東西。畫面上每個判斷都是算出來的：

- **秩用消去法算**，不是手寫上去的。扭轉三次曲線的微分處處秩 1（相依卻只撐出一條曲線）；
  球面的參數化處處秩 2（像是曲面卻沒有整體的相依）；第三個例子秩 3（像裡含一整顆球）。
- **下半連續性兩半都驗**：秩 1 的矩陣旁邊任意近就有秩 2 的（秩跳得上去）；
  而 81 個擾動裡凡是範數小於 0.5 的，秩都沒有掉下來過（掉不下來）。
  **只演後面那一半，看起來就只是連續性**——「下半」兩個字的內容全在前面那一半。
- **推論的例子**：`f¹ = x+y`、`f² = x−y`、`f³ = x²−y²`。斷言四個取樣點上微分的秩都是 2，
  而且斷言 `f³` 恰好等於 `f¹·f²`——三減二等於一，正好一個函數是其餘的函數。
- **最後那個小麻煩**：書上那條螺旋曲線。斷言在原點附近，八個方向的投影每一個都至少來回 12 次，
  所以沒有一個方向是單調的；沒有單調的投影就沒有一塊。

probe 幀抓到三處：beat 5 四個矩陣擠成一排括號、數字小到看不清；
beat 6 三條長條的標籤放在自己那一條下面，讀起來每個標籤都像是下一條的；
beat 10 的螺旋畫了八圈，在那個半徑下糊成一團。

---

## Beat 0 — 誰是誰的函數 / which is a function of which
*配音長度：中文 15.6s ／ 英文 15.3s*

**畫面公式**

```
誰是誰的函數   |   which is a function of which
f ³ ( t )   =   g ( f ¹ ( t ) ,  f ² ( t ) )              t ∈ A
```

**旁白（繁中）**

> 第 13 節問一個很實際的問題：手上有一組連續函數，怎麼判斷其中某一個是不是其他幾個的函數？比方三個實值函數，怎麼知道第三個能不能寫成前兩個的函數？

**Narration (EN)**

> Section 13 asks a practical question: given a collection of continuous functions, how can we tell whether some of them are functions of the rest? Given three real-valued functions, how do we know whether the third is a function of the first two?

**動畫**

左邊三個方塊 f¹、f²、f³，一支往下的箭頭，下面一個加框的「f³ = g(f¹, f²)？」。
右側說明這一節就是把這個問題問清楚。

## Beat 1 — 換個問法：像是不是曲面 / restated: is the range a surface
*配音長度：中文 16.5s ／ 英文 14.3s*

**畫面公式**

```
換個問法：像是不是曲面   |   restated: is the range a surface
F  :  t  ↦  ⟨ f ¹ ( t ) , f ² ( t ) , f ³ ( t ) ⟩          S  =  F [ A ]
```

**旁白（繁中）**

> 這件事跟另一個問題幾乎一樣：把那三個函數併成一個映射，它的像是不是三維空間裡的一個二維子流形？幾乎一樣，可是兩邊都有例外，而例外才是這一節真正的內容。

**Narration (EN)**

> That is very nearly the same as asking whether the range of the mapping formed from the three is a two-dimensional submanifold of three-space. Very nearly, but each direction has an exception, and the exceptions are what this section is about.

**動畫**

左邊立體座標軸加一張藍色的網，代表把三個函數併成的映射的像。
右側說明兩個問題幾乎一樣，可是兩邊各有一個例外。

## Beat 2 — 例外一：相依，可是像只是一條曲線 / first exception: dependent, but only a curve
*配音長度：中文 16.9s ／ 英文 15.7s*

**畫面公式**

```
例外一：相依，可是像只是一條曲線   |   first exception: dependent, but only a curve
f ²  =  g ∘ f ¹ ,   f ³  =  h ∘ f ¹        ⇒        S  =  ⟨ s , g , h ⟩
```

**旁白（繁中）**

> 第一個方向：如果第三個真的依賴前兩個，像確實落在一個二維子流形上，可是它不見得撐出一個二維的東西。取第二、第三個都依賴第一個，像就縮成一條曲線，一維的。

**Narration (EN)**

> One direction: if the third really does depend on the first two, the range does lie on a two-dimensional submanifold, but it need not fill one out. Let the second and third both depend on the first and the range collapses to a curve, one-dimensional.

**動畫**

立體座標軸加一條紅色的曲線（t 送到 t、t 平方、t 立方）。
右側四行說明相依成立，可是像縮成一維。

## Beat 3 — 例外二：像是曲面，卻只有局部相依 / second: a surface, yet only locally dependent
*配音長度：中文 16.5s ／ 英文 16.5s*

**畫面公式**

```
例外二：像是曲面，卻只有局部相依   |   second: a surface, yet only locally dependent
dim  M  =  2                ¬ ∃ g  :  f ³  =  g ( f ¹ , f ² )
```

**旁白（繁中）**

> 另一個方向：像可以真的是一個二維子流形，而第三個並不整體地依賴前兩個。能說的只有局部——每一點附近三個裡總有一個是另外兩個的函數，但走遠一點要解的可能換一個。

**Narration (EN)**

> The other direction: the range can genuinely be a two-dimensional submanifold while the third is not globally a function of the first two. All one can say is locally: near each point one of the three is a function of the other two, though elsewhere it may be a different one.

**動畫**

球面加兩條緯線，右側同一條鉛垂線上兩個點（藍、紅）用灰色虛線連起來。
右側說明兩點的前兩個座標相同、第三個不同。

## Beat 4 — 秩是三就裝不進曲面 / rank three fits on no surface
*配音長度：中文 17.8s ／ 英文 16.4s*

**畫面公式**

```
秩是三就裝不進曲面   |   rank three fits on no surface
rank  dF ₐ  =  3        ⇒        S ᵣ ( F ( α ) )   ⊂   F [ A ]
```

**旁白（繁中）**

> 先給一個必要條件。如果那個映射的微分在某一點的秩是三，隱函數定理就說像裡含一整顆球。所以秩必須處處小於三；而秩處處等於二時，像基本上就是一個二維流形。

**Narration (EN)**

> First a necessary condition. If the differential has rank three somewhere, the implicit function theorem puts a whole ball inside the range. So the rank must everywhere be less than three; and where it is everywhere two, the range essentially is a surface.

**動畫**

立體座標軸加一組同心圓，代表像裡含一整顆球。
右側說明秩三就裝不進任何二維的東西。

## Beat 5 — 定理 13.1：秩跳得上去，掉不下來 / Theorem 13.1: rank rises, never falls
*配音長度：中文 17.0s ／ 英文 16.2s*

**畫面公式**

```
定理 13.1：秩跳得上去，掉不下來   |   Theorem 13.1: rank rises, never falls
‖ S  −  T ‖   <   ϵ            ⇒            rank S    ≥    rank T
```

**旁白（繁中）**

> 工具有兩個。第一個是定理 13.1：秩是下半連續的。給定一個線性映射 T，附近所有的 S 的秩都不小於 T 的秩。注意只有一邊——秩可以跳上去，跳不下來。

**Narration (EN)**

> There are two tools. The first is Theorem 13.1: rank is lower semicontinuous. Given a linear map T, every S near it has rank at least that of T. Note the one-sidedness: rank can jump up, but it cannot fall.

**動畫**

左右兩個加框的組：左邊秩 1 的矩陣經箭頭變成含 ε 的矩陣，右邊單位矩陣到單位矩陣。
框下分別標 rank 1 → 2 與 rank 2 → 2。

## Beat 6 — 證明：在補空間上有下界 / the proof: bounded below on a complement
*配音長度：中文 18.4s ／ 英文 20.0s*

**畫面公式**

```
證明：在補空間上有下界   |   the proof: bounded below on a complement
‖ T ( α ) ‖  ≥  m ‖ α ‖            ‖ ( S − T ) ( α ) ‖  ≤  ( m / 2 ) ‖ α ‖
```

**旁白（繁中）**

> 證明很短。取零空間的一個補空間 X，T 限制在 X 上是同構，所以有正的下界 m。只要 S 與 T 的距離小於 m 的一半，S 在 X 上也有下界，於是 S 在 X 上是單射，秩就不會比 T 小。

**Narration (EN)**

> The proof is short. Take a complement X of the null space; T restricted to X is an isomorphism and so is bounded below by some positive m. If S is within m over two of T, then S is bounded below on X too, hence injective on X, so its rank is at least T's.

**動畫**

三條長條圖，長度分別是 m、m/2、m/2，標籤統一放在右邊對齊。
右側說明 S 在補空間上仍有下界，仍是單射。

## Beat 7 — 定理 13.2：常秩就有一塊 / Theorem 13.2: constant rank gives a patch
*配音長度：中文 17.2s ／ 英文 18.6s*

**畫面公式**

```
定理 13.2：常秩就有一塊   |   Theorem 13.2: constant rank gives a patch
rank  dF ᵧ   ≡   r   <   dim W        ⇒        F [ U ]  ≅  L  ⊂  ℝ ʳ
```

**旁白（繁中）**

> 第二個工具是定理 13.2：如果 F 連續可微，而且微分的秩在整個定義域上都等於同一個 r，那麼每一點都有一個鄰域，使得它的像是 W 裡一塊 r 維的塊。常秩是關鍵的假設。

**Narration (EN)**

> The second tool is Theorem 13.2: if F is continuously differentiable and the rank of its differential equals the same r throughout the domain, then every point has a neighborhood whose image is an r-dimensional patch in W. Constant rank is the hypothesis that matters.

**動畫**

左邊兩個方塊（常秩 r、r 小於 dim W）經一支箭頭指向 F[U] ≅ L ⊂ ℝʳ。
右側說明常秩是關鍵的假設。

## Beat 8 — 證明的骨架 / the skeleton of the proof
*配音長度：中文 17.2s ／ 英文 19.4s*

**畫面公式**

```
證明的骨架   |   the skeleton of the proof
F    =    K  ∘  P  ∘  F                F ²    =    k  ∘  F ¹
```

**旁白（繁中）**

> 證明的骨架：把 W 拆成微分的像與一個補空間，投影 P 打到前者。用隱函數定理把 P 接上 F 反解出來，再證明剩下那一塊只依賴投影的值，最後收成 F 等於 K 接上 P 接上 F。

**Narration (EN)**

> The skeleton of the proof: split W into the range of the differential and a complement, with P the projection onto the first. Use the implicit function theorem to invert P after F, show what is left depends only on the projected value, and it closes as F equal to K after P after F.

**動畫**

左邊三行式子，下面一個加框的 F = K ∘ P ∘ F。
右側說明投影 P 在附近每一點都是同構。

## Beat 9 — 推論：這才是「函數相依」 / the corollary: dependence, made precise
*配音長度：中文 17.1s ／ 英文 17.8s*

**畫面公式**

```
推論：這才是「函數相依」   |   the corollary: dependence, made precise
f ʲ   =   k ʲ  ∘  ⟨ f ¹ , … , f ʳ ⟩              j = r + 1 , … , m
```

**旁白（繁中）**

> 推論就是原來那個問題的答案：m 個連續可微的實值函數，微分的秩處處等於 r，而 r 小於 m，那麼每一點附近，其中 m 減 r 個是剩下 r 個的函數。這就是函數相依的精確版本。

**Narration (EN)**

> The corollary answers the original question: for m continuously differentiable real-valued functions whose differential has constant rank r less than m, every point has a neighborhood on which m minus r of them are functions of the remaining r. That is dependence made precise.

**動畫**

左邊三個函數的定義，下面一張表：取樣點、f¹ 乘 f²、以及 f³。
右側說明三減二等於一，正好一個是其餘的函數。

## Beat 10 — 那個小麻煩 / the small difficulty
*配音長度：中文 20.8s ／ 英文 17.5s*

**畫面公式**

```
那個小麻煩   |   the small difficulty
Γ  :  ( − 1 , 1 )  ↪  ℝ ³            ∀ N ∋ 0        N ∩ Γ   ≇   L
```

**旁白（繁中）**

> 最後是那個小麻煩。常秩不保證整個像是子流形。書上那條曲線先沿 z 軸下來，轉個彎後在 xy 平面上繞原點螺旋內縮。它是一個區間的連續可微單射的像，可是原點附近怎麼取鄰域都不是一塊。

**Narration (EN)**

> Finally the small difficulty. Constant rank does not make the whole range a submanifold. The book's curve comes down the z-axis, turns over, then spirals in toward the origin. It is the injective image of an interval, yet no neighborhood of the origin meets it in a patch.

**動畫**

立體座標軸：藍色的曲線沿 z 軸下來、轉個彎，紅色的螺旋在平面上繞原點內縮，
原點打點並套一個圈。右側說明怎麼取鄰域交出來都不是一塊。

---

## 「基本上」那三個字

第 4 拍說「秩處處等於二時，像基本上就是一個二維流形」。那三個字要到最後一拍才交代：
常秩給的是「每一點都有一個鄰域，它的像是一塊」，可是那一塊不見得是像在該點的一整個鄰域——
像可能繞回來，擠進那一點的每一個鄰域裡。書上那條螺旋曲線就是這樣：
它是一個區間的連續可微單射的像，可是它在 ℝ³ 裡的嵌入方式壞掉了。

## 這條曲線本身沒有問題

書上特別說明：Γ 當成一維流形來看完全沒問題，出問題的是它嵌到 ℝ³ 的方式。
這個區別在後面談抽象流形時會變得重要——那時候根本沒有外面的空間，也就沒有嵌入可以出錯。
