# advcalc E14 — 第 1 章：直和與補空間

Chapter 1: Direct Sums and Complements

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 5 節（書頁 56–58）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e14_direct_sums.py`（`AdvCalcE14ZH` / `AdvCalcE14EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[14]` / `FORMULAS_ADVCALC[14]`）
- 配音：`manim_lessons/samples/audio_e14/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.94 分（177 秒）／英文 2.68 分（161 秒）

---

## Beat 0 — 一族子空間，乘積就是整個空間 / a family of subspaces, product is the whole
*配音長度：中文 15.7s ／ 英文 14.1s*

**畫面公式**

```
一族子空間，乘積就是整個空間   |   a family of subspaces, product is the whole
V  ≅  ∏₁ⁿ Vᵢ
```

**旁白（繁中）**

> 書上說，現在到了這一章的核心。經常會發生這種事：研究某個向量空間上的現象時，冒出一族有限多個子空間，使得整個空間自然地同構於它們的乘積。

**Narration (EN)**

> The book says we now come to the heart of the chapter. It frequently happens that studying some phenomenon on a vector space turns up a finite collection of subspaces such that the space is naturally isomorphic to their product.

**動畫**

左邊 V 的橢圓，右邊三個 Vᵢ 的方塊，中間一對雙向箭頭代表同構。

## Beat 1 — 積空間的等式，在 V 裡的倒影 / the product identities, reflected in V
*配音長度：中文 19.9s ／ 英文 18.4s*

**畫面公式**

```
積空間的等式，在 V 裡的倒影   |   the product identities, reflected in V
Σ Pᵢ = I        Pⱼ ∘ Pⱼ = Pⱼ        Pᵢ ∘ Pⱼ = 0  ( i ≠ j )        Vᵢ = R ( Pᵢ )
```

**旁白（繁中）**

> 在這個同構之下，積空間上的「注入接投影」變成 V 上的一族映射，而投影注入的等式就反映成三條：全部加起來是恆等、每一個接自己還是自己、不同的兩個相接是零。而那些子空間，就是它們各自的值域。

**Narration (EN)**

> Under that isomorphism, injection-after-projection on the product becomes a family of maps on V, and the identities are reflected as: they sum to the identity, each composed with itself gives itself, and different ones compose to zero. Each subspace is one of their ranges.

**動畫**

三個方框各寫一條等式：加起來是恆等、接自己還是自己、不同的相接是零。

## Beat 2 — 把元組送到它們的和 / sending a tuple to its sum
*配音長度：中文 19.2s ／ 英文 17.5s*

**畫面公式**

```
把元組送到它們的和   |   sending a tuple to its sum
π : ⟨ α₁ , … , αₙ ⟩ ↦ Σ₁ⁿ αᵢ        π  inj :  independent
```

**旁白（繁中）**

> 定義是這樣：給定 V 的一族子空間，把「每個子空間各取一個向量」的元組送到它們的和，這是一個從乘積到 V 的線性映射。如果它是嵌射，就說這些子空間獨立；如果它是同構，就說 V 是它們的直和。

**Narration (EN)**

> The definition: given a family of subspaces, sending a tuple of vectors, one from each, to their sum is a linear map from the product into V. If that map is injective the subspaces are called independent; if it is an isomorphism, V is their direct sum.

**動畫**

左邊三個 αᵢ 的方塊，經 π 送到右邊三支首尾相接的向量與它們的和。

## Beat 3 — 既獨立，又生成 / both independent and spanning
*配音長度：中文 16.9s ／ 英文 16.8s*

**畫面公式**

```
既獨立，又生成   |   both independent and spanning
V  =  V₁ ⊕ … ⊕ Vₙ   ⇔   π   iso
```

**旁白（繁中）**

> 所以 V 是直和，若且唯若這個映射既是嵌射又是滿射，也就是這些子空間既獨立、又生成整個 V。換個說法：V 裡每一個向量，都能唯一地寫成「每個子空間各出一項」的和。

**Narration (EN)**

> So V is the direct sum exactly when the map is both injective and surjective, that is, when the subspaces are both independent and span V. Restated: every vector of V is uniquely expressible as a sum with one term from each subspace.

**動畫**

「嵌射＝獨立」與「滿射＝生成」兩個方框，箭頭匯到底下的「V 是它們的直和」。

## Beat 4 — 存在來自生成，唯一來自獨立 / existence from spanning, uniqueness from independence
*配音長度：中文 10.8s ／ 英文 8.2s*

**畫面公式**

```
存在來自生成，唯一來自獨立   |   existence from spanning, uniqueness from independence
α  =  Σ₁ⁿ αᵢ   ,   αᵢ ∈ Vᵢ   ,   unique
```

**旁白（繁中）**

> 這樣的寫法存在，是因為它們生成 V；寫法唯一，是因為它們獨立。要兩件事同時成立才是直和。

**Narration (EN)**

> Such an expression exists because they span V, and it is unique because they are independent. It takes both to have a direct sum.

**動畫**

兩條斜的參考線與一個向量，拆成沿著兩條線的兩段。

## Beat 5 — 偶函數與奇函數 / the even and the odd functions
*配音長度：中文 14.5s ／ 英文 12.0s*

**畫面公式**

```
偶函數與奇函數   |   the even and the odd functions
V = 𝒞 ( ℝ )        Vₑ : f ( −x ) = f ( x )        Vₒ : f ( −x ) = − f ( x )
```

**旁白（繁中）**

> 書上的例子很漂亮。取實數線上所有連續函數，偶函數所成的子集是子空間，奇函數所成的子集也是，而整個空間正好是這兩個的直和。

**Narration (EN)**

> The book's example is a pretty one. In the space of continuous functions on the line, the even functions form a subspace and so do the odd ones, and the whole space is the direct sum of the two.

**動畫**

一條函數曲線與它的鏡像，疊在同一組座標軸上。

## Beat 6 — 跟自己的鏡像平均起來 / average it with its own reflection
*配音長度：中文 21.0s ／ 英文 18.4s*

**畫面公式**

```
跟自己的鏡像平均起來   |   average it with its own reflection
eˣ  =  ( eˣ + e⁻ˣ ) / 2  +  ( eˣ − e⁻ˣ ) / 2  =  cosh x + sinh x
```

**旁白（繁中）**

> 作法是：任何一個函數，跟自己的鏡像平均起來就得到偶的部分，相減再除以二就得到奇的部分。而分解是唯一的，因為同時是偶又是奇的函數只有零。指數函數的偶奇分量，正好就是雙曲餘弦與雙曲正弦。

**Narration (EN)**

> Given any function, averaging it with its own reflection gives the even part, and half the difference gives the odd part. The decomposition is unique because the only function both even and odd is zero. The even and odd parts of the exponential are the hyperbolic cosine and sine.

**動畫**

同一條曲線加上偶部與奇部兩條曲線。三者的關係（相加還原、偶、奇）在建圖時都 assert 驗過。

## Beat 7 — 加起來是零，就每個都是零 / if they sum to zero, each is zero
*配音長度：中文 13.2s ／ 英文 14.0s*

**畫面公式**

```
加起來是零，就每個都是零   |   if they sum to zero, each is zero
αᵢ ∈ Vᵢ  &  Σ₁ⁿ αᵢ = 0   ⇒   αᵢ = 0   ( ∀i )
```

**旁白（繁中）**

> 因為嵌射等價於零空間只有零向量，獨立性就有一個好用的等價說法：如果每個子空間各取一個向量、加起來等於零，那麼每一個都必須是零。

**Narration (EN)**

> Since injectivity is the same as having only zero in the null space, independence gets a convenient restatement: if one vector is taken from each subspace and they sum to zero, then every one of them is zero.

**動畫**

三個 α 方塊相加等於零，箭頭往下，每一個都變成零。

## Beat 8 — 兩個子空間：只交於零 / two subspaces: meeting only at zero
*配音長度：中文 15.5s ／ 英文 15.7s*

**畫面公式**

```
兩個子空間：只交於零   |   two subspaces: meeting only at zero
M , N   independent   ⇔   M ∩ N = { 0 }
```

**旁白（繁中）**

> 兩個子空間的情形特別簡單：它們獨立，若且唯若交集只有零向量。所以 V 是兩個子空間的直和，若且唯若 V 等於它們的和、而且它們只在零向量處相交。

**Narration (EN)**

> For two subspaces it is especially simple: they are independent exactly when their intersection is only the zero vector. So V is the direct sum of two subspaces exactly when V is their sum and they meet only at zero.

**動畫**

左邊兩個橢圓只交於一點（獨立），右邊兩個有一大塊重疊（不獨立）。

## Beat 9 — 補空間不唯一 / a complement is not unique
*配音長度：中文 16.1s ／ 英文 14.5s*

**畫面公式**

```
補空間不唯一   |   a complement is not unique
V = M ⊕ N   ⇔   V = M + N   &   M ∩ N = { 0 }
```

**旁白（繁中）**

> 這時這兩個子空間互稱補空間。但要小心：一個子空間的補空間通常不唯一。在三維座標空間裡，真子空間就只有過原點的平面與過原點的直線兩種。

**Narration (EN)**

> Two such subspaces are called complements of each other. But a warning: a subspace does not have a unique complement. In coordinate three-space the only proper subspaces are the planes through the origin and the lines through the origin.

**動畫**

軸測投影的一個平面，配上三條不同的直線，每一條都補得起來——三條都 assert 過不落在平面內。

## Beat 10 — 平面配上不在它裡面的直線 / a plane and a line not lying in it
*配音長度：中文 13.9s ／ 英文 11.2s*

**畫面公式**

```
平面配上不在它裡面的直線   |   a plane and a line not lying in it
ℝ³  =  N ⊕ L        ξ  =  η + λ
```

**旁白（繁中）**

> 如果兩個真子空間裡，一個是平面、另一個是不落在該平面上的直線，那麼它們互為補空間；而且在三維空間裡，這是唯一一種非平凡的互補配對。

**Narration (EN)**

> If two proper subspaces are one plane and one line not lying in that plane, then they are complementary; and in three-space those are the only nontrivial complementary pairs.

**動畫**

書上的 Fig. 1.9：平面 N 與直線 L，一個向量拆成 η 與 λ 兩段。
