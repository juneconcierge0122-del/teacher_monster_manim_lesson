# advcalc E15 — 第 1 章：直和與投影算子

Chapter 1: Direct Sums and Projection Operators

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 5 節（書頁 58–61）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e15_projections.py`（`AdvCalcE15ZH` / `AdvCalcE15EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[15]` / `FORMULAS_ADVCALC[15]`）
- 配音：`manim_lessons/samples/audio_e15/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.95 分（177 秒）／英文 2.78 分（167 秒）

---

## Beat 0 — 獨立可以疊起來 / independence stacks
*配音長度：中文 13.9s ／ 英文 12.7s*

**畫面公式**

```
獨立可以疊起來   |   independence stacks
V₁ , V₀   ind .        V₀ = ⊕₂ⁿ Vᵢ        ⇒   { Vᵢ }₁ⁿ   ind .
```

**旁白（繁中）**

> 先補一個技術性的引理：如果兩個子空間獨立，而其中第二個自己又分解成一族獨立的子空間，那麼把它們全部合起來的那一族，在 V 裡也是獨立的。

**Narration (EN)**

> First a technically useful lemma: if two subspaces are independent, and the second of them is itself split into an independent family, then the whole collection taken together is independent in V.

**動畫**

巢狀的橢圓：V 裡面是 V₁ 與 V₀，而 V₀ 裡面又有三個小的。

## Beat 1 — 直和可以一層一層拆 / direct sums come apart in layers
*配音長度：中文 14.1s ／ 英文 13.5s*

**畫面公式**

```
直和可以一層一層拆   |   direct sums come apart in layers
V = V₁ ⊕ V₀   &   V₀ = ⊕₂ⁿ Vᵢ    ⇒    V = ⊕₁ⁿ Vᵢ
```

**旁白（繁中）**

> 推論是：V 是前兩者的直和、而第二個又是後面那些的直和，兩件事合起來就得到 V 是全部這些的直和。所以直和可以一層一層拆下去。

**Narration (EN)**

> The corollary: V being the direct sum of the first two, together with the second being the direct sum of the rest, gives V as the direct sum of all of them. So direct sums can be taken apart a layer at a time.

**動畫**

三個方框由上往下排：V、V₁⊕V₀、V₁⊕V₂⊕…，一層一層拆下去。

## Beat 2 — 同構有反函數，接上投影 / invert the isomorphism, then project
*配音長度：中文 17.5s ／ 英文 16.3s*

**畫面公式**

```
同構有反函數，接上投影   |   invert the isomorphism, then project
Pⱼ  =  πⱼ ∘ π ⁻¹   :   V → Vⱼ
```

**旁白（繁中）**

> 現在定義投影。V 是一族子空間的直和時，那個從乘積到 V 的映射是同構，所以有反函數。把第 j 個座標投影接在反函數後面，就得到一個從 V 到第 j 個子空間的線性映射。

**Narration (EN)**

> Now the projections. When V is the direct sum of a family, the map from the product to V is an isomorphism, so it has an inverse. Composing the jth coordinate projection after that inverse gives a linear map from V into the jth subspace.

**動畫**

V、乘積、Vⱼ 三個方框：上排是先取反函數再接座標投影，下排是合成之後的 Pⱼ。

## Beat 3 — 送到它在第 j 個子空間的那一份 / to its own share in the jth subspace
*配音長度：中文 18.2s ／ 英文 15.4s*

**畫面公式**

```
送到它在第 j 個子空間的那一份   |   to its own share in the jth subspace
α = Σ₁ⁿ αᵢ        Pⱼ ( α )  =  αⱼ
```

**旁白（繁中）**

> 因為每個向量都唯一地寫成各子空間各出一項的和，這個映射就是把一個向量送到它在第 j 個子空間裡的那一份。書上把這一份叫做該向量的第 j 個分量，把這個映射叫做 V 到第 j 個子空間的投影。

**Narration (EN)**

> Since every vector is uniquely a sum with one term from each subspace, that map sends a vector to its own share in the jth one. The book calls that share the jth component, and the map the projection of V onto the jth subspace.

**動畫**

兩條斜的參考線與一個向量，投影只留下沿著第一條線的那一段。

## Beat 4 — 「投影」在這本書有三個意思 / three things called projection
*配音長度：中文 16.7s ／ 英文 14.9s*

**畫面公式**

```
「投影」在這本書有三個意思   |   three things called projection
∏ Wᵢ  :  πⱼ          V / N  :  π          ⊕ Vᵢ  :  Pⱼ
```

**旁白（繁中）**

> 要注意「投影」這個詞在書裡已經出現三種不同的意思：笛卡兒積上的座標投影、商空間上的投影，還有現在這一個。三者互相有關，但確實不同；靠上下文分辨就好。

**Narration (EN)**

> Note that the word projection now has three different meanings in this book: the coordinate projection on a Cartesian product, the projection onto a quotient space, and this one. They are related but distinct, and context settles which is meant.

**動畫**

三個小圖並排：積空間的座標投影、商空間的投影、沿補空間的投影——同一個詞，三個意思。

## Beat 5 — 值域、相接為零、加起來是恆等 / ranges, zero composites, summing to I
*配音長度：中文 14.5s ／ 英文 14.7s*

**畫面公式**

```
值域、相接為零、加起來是恆等   |   ranges, zero composites, summing to I
R ( Pᵢ ) = Vᵢ        Pᵢ ∘ Pⱼ = 0  ( i ≠ j )        Σ₁ⁿ Pᵢ = I
```

**旁白（繁中）**

> 定理是：這些投影的值域正好就是那些子空間、不同的兩個相接是零、而且全部加起來是恆等。這三條，正是積空間上那組等式在 V 裡的倒影。

**Narration (EN)**

> The theorem: the ranges of these projections are exactly those subspaces, different ones compose to zero, and all of them sum to the identity. Those three are the reflection in V of the identities that held on the product space.

**動畫**

左邊三條等式，箭頭指向右邊的「V 是直和」。

## Beat 6 — 反過來也成立 / and the converse holds
*配音長度：中文 16.5s ／ 英文 14.2s*

**畫面公式**

```
反過來也成立   |   and the converse holds
Σ₁ⁿ Pᵢ = I  &  Pᵢ ∘ Pⱼ = 0    ⇒    V = ⊕₁ⁿ R ( Pᵢ )
```

**旁白（繁中）**

> 反過來的定理也成立。如果 V 上的一族線性映射滿足「加起來是恆等」與「不同的相接是零」，那麼把它們的值域取出來，V 就是這些值域的直和，而它們正好是對應的投影。

**Narration (EN)**

> The converse holds as well. If a family of maps on V sums to the identity and different ones compose to zero, then taking their ranges, V is the direct sum of those ranges and the maps are the corresponding projections.

**動畫**

同樣的圖，箭頭方向反過來——這是反過來的那個定理。

## Beat 7 — 冪等：再做一次什麼也沒動 / idempotent: doing it twice moves nothing
*配音長度：中文 16.2s ／ 英文 16.2s*

**畫面公式**

```
冪等：再做一次什麼也沒動   |   idempotent: doing it twice moves nothing
Pᵢ ∘ Pᵢ  =  Pᵢ        N ( Pᵢ )  =  Σⱼ ≠ ᵢ Vⱼ
```

**旁白（繁中）**

> 這給了投影一個內在的刻畫。投影是冪等的——自己接自己還是自己；等價地說，它在自己的值域上就是恆等。而它的零空間，正好是其他那些子空間的和。

**Narration (EN)**

> That gives projections an intrinsic characterization. They are idempotent: each composed with itself gives itself, equivalently each is the identity on its own range. And the null space of one is the sum of all the other subspaces.

**動畫**

一個向量投影下來，再投影一次完全沒有動。兩次的落點在建圖時 assert 過是同一點。

## Beat 8 — 冪等，就是投影 / idempotent is the same as projection
*配音長度：中文 16.0s ／ 英文 16.5s*

**畫面公式**

```
冪等，就是投影   |   idempotent is the same as projection
P ∘ P = P    ⇒    V  =  R ( P )  ⊕  N ( P )
```

**旁白（繁中）**

> 反過來也對：只要 V 上一個線性映射是冪等的，那麼 V 就是它的值域與零空間的直和，而它正好是值域上的投影。所以「冪等」與「是一個投影」，講的是同一件事。

**Narration (EN)**

> The converse holds too: if any linear map on V is idempotent, then V is the direct sum of its range and its null space, and the map is the projection onto its range. So being idempotent and being a projection are the same thing.

**動畫**

「冪等」與「是一個投影」兩個方框，中間一對雙向箭頭，底下是值域與零空間的直和。

## Beat 9 — 設 Q 是恆等減去 P / set Q to be the identity minus P
*配音長度：中文 13.7s ／ 英文 14.5s*

**畫面公式**

```
設 Q 是恆等減去 P   |   set Q to be the identity minus P
Q = I − P        P ∘ Q  =  P − P ∘ P  =  0        R ( Q ) = N ( P )
```

**旁白（繁中）**

> 證明很短。設 Q 是恆等減去 P，那麼 P 接 Q 等於 P 減去 P 的平方，也就是零，於是套用前一個定理；而 Q 的值域正好是 P 的零空間。

**Narration (EN)**

> The proof is short. Set Q to be the identity minus P; then P composed with Q is P minus P squared, which is zero, so the previous theorem applies, and the range of Q is exactly the null space of P.

**動畫**

四行式子由上往下：Q 是恆等減 P、兩者相接、結果是零、Q 的值域就是 P 的零空間。

## Beat 10 — 一對互補投影 / a pair of complementary projections
*配音長度：中文 19.7s ／ 英文 17.7s*

**畫面公式**

```
一對互補投影   |   a pair of complementary projections
P + Q = I        P ∘ Q = Q ∘ P = 0        π̄ⱼ = ιⱼ ∘ πⱼ
```

**旁白（繁中）**

> 兩個相加等於恆等、而且兩邊相接都是零的映射，叫做一對互補投影。最後書上補了一個細節：嚴格說，把那些投影加起來時上域對不上，要引進一個把子空間看成 V 的子集的恆等注入，才算完全嚴密。

**Narration (EN)**

> A pair of maps summing to the identity whose composites both ways are zero is called a pair of complementary projections. The book closes on a fine point: strictly, summing those projections mismatches the codomains, and an identity injection is needed to make it exact.

**動畫**

兩條斜線上各一支投影向量與原向量，構成一對互補投影。
