# advcalc E46 — 第 3 章：隱函數的微分

Chapter 3: Differentiating an Implicit Function

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 11 節「隱函數定理」的前段（書頁 164–166）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e46_implicit.py`（`AdvCalcE46ZH` / `AdvCalcE46EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[46]` / `FORMULAS_ADVCALC[46]`）
- 配音：`manim_lessons/samples/audio_e46/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.25 分（195 秒）／英文 3.11 分（187 秒）

## 一條公式，三個層級

第 11 節開頭做的事是換一個角度看鏈鎖規則：古典的偏導數連鎖式
`∂zₖ/∂xⱼ = Σ (∂zₖ/∂yᵢ)(∂yᵢ/∂xⱼ)` 與一般的 `d(G∘F)ₐ = dG_β ∘ dFₐ`，
其實是同一條式子寫在三種語言裡——一維是乘一個數、有座標時是矩陣相乘、一般情形是合成。
把「倒數」換成「合成反元素」，反函數的導數公式就成立；
把同樣的翻譯用在隱函數上，就得到定理 11.1。

這一集三個層級各配一個算得出來的例子：

- **反映射**：取 `F(x₁, x₂) = (x₁ + x₂², x₂)`，它的反映射有封閉形式。
  斷言兩者在兩個取樣點上真的互為反函數，並斷言兩個雅可比矩陣相乘逐項等於單位矩陣。
- **純量隱函數**：圓 `x² + y² = 25` 上取點 (3, 4)。先斷言那點真的在圓上，
  再用中央差商算兩個偏導數，斷言 `−gₓ/g_y` 與顯式解 `√(25 − x²)` 的導數相同，
  而且斷言它等於 −3/4——畫面上印的就是這個分數，不是浮點數。
- **向量隱函數**：取 `G(ξ, η) = (η₁ + ξ₁η₂ − 3, η₂² + ξ₂ − 5)`。
  斷言取樣點滿足 `G = 0`，斷言第二個偏微分的行列式不為零，
  再把定理 11.1 那條公式算出來的 `dFₐ` 與顯式解 `F(ξ) = (3 − ξ₁√(5 − ξ₂), √(5 − ξ₂))`
  的雅可比逐項比對——這一條是整集的核心驗算。

`bounds.py` 抓到 beat 1 三個欄位的框往右超出。probe 幀抓到 beat 4 印出了原始浮點數
`-0.75`，改成畫面上的 `− 3 / 4`；同一次也清掉了一個誤打的 walrus 與兩段沒用到的英文字串。

---

## Beat 0 — 兩條公式長得一模一樣 / two formulas, one shape
*配音長度：中文 20.7s ／ 英文 17.8s*

**畫面公式**

```
兩條公式長得一模一樣   |   two formulas, one shape
∂ z ₖ / ∂ x ⱼ  =  Σ ( ∂ z ₖ / ∂ y ᵢ ) ( ∂ y ᵢ / ∂ x ⱼ )        d ( G ∘ F )  =  Σ dG ⁱ ∘ dF ⁱ
```

**旁白（繁中）**

> 這一節從一個觀察開始。上一集那條雅可比矩陣的連鎖公式，跟前面那條微分的鏈鎖規則，長得幾乎一模一樣。差別只在一個地方：雅可比那條裡是數字在相乘相加，微分那條裡是線性映射在合成相加。

**Narration (EN)**

> This section starts from an observation. The chain formula for Jacobian matrices and the chain rule for differentials look almost identical. The difference is one thing: the Jacobian formula multiplies and adds numbers, the differential rule composes and adds linear maps.

**動畫**

左邊上下兩條加框的式子：古典的偏導數連鎖式與一般的 d(G∘F) = dG ∘ dF。
右側說明差別只在「數字相乘」與「線性映射合成」。

## Beat 1 — 數 → 矩陣 → 線性映射 / number, matrix, linear map
*配音長度：中文 23.6s ／ 英文 17.8s*

**畫面公式**

```
數 → 矩陣 → 線性映射   |   number, matrix, linear map
dim = 1 :   · c               ℝ ⁿ :   [ t ᵢ ⱼ ]               V :   ∘
```

**旁白（繁中）**

> 整個微分學其實都是這樣走的。一元的時候，微分是從一維空間到自己的線性映射，也就是乘上一個數；多變數的時候，那些數排成一塊一塊的，就是雅可比矩陣；到了一般的向量空間，公式完全相同，只是數換成線性映射、乘法換成合成。

**Narration (EN)**

> The whole differential calculus runs this way. In one variable a differential maps a one dimensional space to itself, so it multiplies by a number. In many variables those numbers come in blocks, the Jacobian matrices. In general the same formulas hold with linear maps.

**動畫**

左邊三個並排的方塊：dim V = 1 配「· c」、V = ℝⁿ 配矩陣、V 配「∘」，兩支箭頭串起來。
右側三行對應三種語言。

## Beat 2 — 反映射：倒數換成合成反元素 / an inverse: reciprocal becomes composition inverse
*配音長度：中文 18.9s ／ 英文 17.7s*

**畫面公式**

```
反映射：倒數換成合成反元素   |   an inverse: reciprocal becomes composition inverse
g ′ ( b )  =  1 / f ′ ( a )              dG ᵦ  =  ( dF ₐ ) ⁻¹
```

**旁白（繁中）**

> 第一個例子是反函數。一元微積分說反函數的導數是原導數的倒數。一般的說法就是：反映射的微分，是原微分的合成反元素。畫面上兩個雅可比矩陣乘起來剛好是單位矩陣。

**Narration (EN)**

> The first example is the inverse function. One variable calculus says the derivative of an inverse is the reciprocal. The general statement is that the differential of an inverse map is the composition inverse of the differential. On screen the two Jacobians multiply to the identity.

**動畫**

左邊三個矩陣：dFₐ · dGᵦ = I，中間放「·」與「=」。
右側說明反映射的微分是微分的合成反元素，兩個雅可比乘起來剛好是單位矩陣。

## Beat 3 — 隱函數：把恆等式微分 / implicit: differentiate the identity
*配音長度：中文 13.2s ／ 英文 14.0s*

**畫面公式**

```
隱函數：把恆等式微分   |   implicit: differentiate the identity
g ( x , f ( x ) )   ≡   0
```

**旁白（繁中）**

> 第二個例子是隱函數，而且這才是這一節真正的主角。如果 g 等於零這個方程把 y 定成 x 的函數，古典的做法是把恆等式對 x 微分。

**Narration (EN)**

> The second example is the implicit function, and it is the real subject here. If the equation G equals zero defines y as a function of x, the classical move is to differentiate the identity with respect to x.

**動畫**

左邊一個座標十字與半徑 5 的圓，點 (3, 4) 打紅點，兩條灰色虛線標出座標。
右側說明方程把 y 定成 x 的函數。

## Beat 4 — 古典的那條式子 / the classical formula
*配音長度：中文 17.7s ／ 英文 15.8s*

**畫面公式**

```
古典的那條式子   |   the classical formula
∂g/∂x  +  ( ∂g/∂y ) f ′ ( a )  =  0              f ′ ( a )  =  − 3 / 4
```

**旁白（繁中）**

> 微分之後得到 g 對 x 的偏導數，加上 g 對 y 的偏導數乘以 f 的導數，等於零。解出來就是 f 的導數等於負的、兩個偏導數的商。畫面上那個圓的例子算出來是負的四分之三。

**Narration (EN)**

> That gives the partial derivative of g by x, plus the partial by y times the derivative of f, equal to zero. Solving, the derivative of f is minus the quotient of the two partials. For the circle on screen it comes out at minus three quarters.

**動畫**

同一個圓畫成灰色細線，紅點上加一條橘色的切線。
右側是隱微分的式子與 f′(a) = −3/4。

## Beat 5 — 一般情形一字不改 / the general case, word for word
*配音長度：中文 16.1s ／ 英文 17.3s*

**畫面公式**

```
一般情形一字不改   |   the general case, word for word
G ( ξ , F ( ξ ) )   ≡   0              dG ¹  +  dG ² ∘ dF ₐ  =  0
```

**旁白（繁中）**

> 一般的情形一字不改。設 G 等於零把 η 定成 ξ 的函數，把恆等式微分，用的是上一集那條一般鏈鎖規則，得到第一個偏微分加上第二個偏微分接上 dF，等於零。

**Narration (EN)**

> The general case needs no change of wording. If G equals zero defines eta as a function of xi, differentiate the identity using last episode's general chain rule and get the first partial differential plus the second composed with dF, equal to zero.

**動畫**

左邊三行：恆等式、寫成合成、以及對它微分得到的 dG¹ + dG² ∘ dFₐ = 0。
右側說明每個偏微分各配一支內函數。

## Beat 6 — 解出 dF / solving for dF
*配音長度：中文 16.1s ／ 英文 16.7s*

**畫面公式**

```
解出 dF   |   solving for dF
dF ₐ    =    − ( dG ² ) ⁻¹  ∘  dG ¹
```

**旁白（繁中）**

> 只要第二個偏微分可逆，就解得出來：dF 等於負的、第二個偏微分的反元素接上第一個偏微分。跟一元那條式子形式完全相同，只是除法換成了合成反元素。

**Narration (EN)**

> Provided the second partial differential is invertible, this can be solved: dF is minus the inverse of the second partial differential composed with the first. The form matches the one variable formula exactly, with division replaced by composition inverse.

**動畫**

左邊兩條加框的式子：dG² ∘ dFₐ = −dG¹ 與解出來的 dFₐ = −(dG²)⁻¹ ∘ dG¹，
下面灰色一行是一維的樣子，拿來對照。

## Beat 7 — 定理 11.1 / Theorem 11.1
*配音長度：中文 18.7s ／ 英文 19.7s*

**畫面公式**

```
定理 11.1   |   Theorem 11.1
G ( α , β ) = 0   ,   ( dG ² ) ⁻¹  ∃         ⇒         dF ₐ  ∃
```

**旁白（繁中）**

> 定理 11.1 把這件事寫成定理。它的假設是：隱函數已經存在而且連續，G 在那一點可微，而且第二個偏微分可逆。結論是：那個隱函數在該點可微，微分就是剛才那個式子。

**Narration (EN)**

> Theorem 11.1 states this. Its hypotheses: the implicit function already exists and is continuous, G is differentiable at the point, and the second partial differential is invertible. Its conclusion: the implicit function is differentiable there, with that formula as its differential.

**動畫**

左邊三個假設方塊（恆等式、F 連續、第二個偏微分可逆）用一支箭頭指向結論方塊 dFₐ 存在。
右側說明「F 存在」是假設而不是結論。

## Beat 8 — 證明：把 η 也當成未知數 / the proof: eta is an unknown too
*配音長度：中文 17.9s ／ 英文 21.1s*

**畫面公式**

```
證明：把 η 也當成未知數   |   the proof: eta is an unknown too
η  =  O ( ξ )  +  o ( ⟨ ξ , η ⟩ )              η  =  S ( ξ )  +  o ( ξ )
```

**旁白（繁中）**

> 證明的關鍵是把 η 也當成未知數。先得到「η 等於一個大 O 加上一個關於 ξ 與 η 的小 o」，再用 E37 的引理 5.1 推出 η 本身是 ξ 的大 O，於是那一對也是大 O，式子就收乾淨了。

**Narration (EN)**

> The key to the proof is treating eta as an unknown too. First comes eta equals a big oh plus a little oh in the pair, and then E37's Lemma 5.1 gives that eta is itself a big oh of xi, hence so is the pair; little oh after big oh is little oh, and the expression closes up.

**動畫**

左邊三行：ΔG 展開、把 η 解出來得到大 O、再收成 η = S(ξ) + o(ξ)。
右側說明用到的是 E37 的引理 5.1。

## Beat 9 — 一個向量的例子，核對過 / a vector example, checked
*配音長度：中文 19.4s ／ 英文 16.7s*

**畫面公式**

```
一個向量的例子，核對過   |   a vector example, checked
dF ₐ   =   ( ( − 2 , 1 / 4 ) , ( 0 , − 1 / 4 ) )
```

**旁白（繁中）**

> 注意這條定理只說「如果隱函數存在而且連續，那它可微」。存在性本身沒有證，那要用第 4 章的不動點定理。畫面上那個向量的例子，程式把顯式解也算出來核對過，兩邊完全相同。

**Narration (EN)**

> Note the theorem only says that if the implicit function exists and is continuous then it is differentiable. Existence is not proved; that needs the fixed point theorem of chapter four. For the vector example the code also solves explicitly and checks the two agree.

**動畫**

左邊三個矩陣：dG¹、dG²，一支箭頭之後是公式算出來的 dFₐ。
右側說明第二個的行列式是 4、可逆。

## Beat 10 — 存在性還沒證 / existence is still open
*配音長度：中文 12.8s ／ 英文 12.2s*

**畫面公式**

```
存在性還沒證   |   existence is still open
∃ F  ?               →               Ch 4
```

**旁白（繁中）**

> 下一集就講存在性：定理 11.2，以及它的特例——反映射定理。這一節到此把「隱函數如果存在會長什麼樣」交代完了。

**Narration (EN)**

> Existence is next time: Theorem 11.2 and its special case, the inverse mapping theorem. What this section settles is what an implicit function must look like if it exists at all.

**動畫**

左邊兩個方塊（dFₐ 存在、F 存在），上面那支箭頭指向 Ch 3，下面那支是虛線並打上叉，指向 Ch 4。
右側說明存在性要用第 4 章的不動點定理。

---

## 這條定理不製造隱函數

定理 11.1 的假設裡就寫著「F 存在而且連續」。它說的是：既然有這麼一個東西，
那它一定可微，而且微分只能長成 `−(dG²)⁻¹ ∘ dG¹`。
存在性完全沒證——那要等第 4 章的不動點定理，下一集會把這條界線再畫一次。

## 順序變得要緊

一維的 `f′ = −gₓ/g_y` 是除法，除法可以左右不分。
一般情形是合成的反元素，`(dG²)⁻¹` 必須寫在 `dG¹` 的左邊。
這是「把數換成線性映射」時唯一真的會改變的地方，值得多看一眼。
