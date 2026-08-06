# advcalc E16 — 第 1 章：解線性方程與 T 的多項式

Chapter 1: Solving a Linear Equation, and Polynomials in T

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 5 節（書頁 61–67）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e16_polynomials.py`（`AdvCalcE16ZH` / `AdvCalcE16EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[16]` / `FORMULAS_ADVCALC[16]`）
- 配音：`manim_lessons/samples/audio_e16/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.99 分（180 秒）／英文 2.72 分（163 秒）

---

## Beat 0 — 有解，就是目標落在值域裡 / solvable means the target is in the range
*配音長度：中文 15.2s ／ 英文 15.4s*

**畫面公式**

```
有解，就是目標落在值域裡   |   solvable means the target is in the range
T ( ξ )  =  η        η  ∈  R ( T )
```

**旁白（繁中）**

> 數學裡很多重要的問題都長成同一個樣子：給了一個線性算子與一個目標向量，要解出被送到目標的那個向量。有解的條件，正好就是目標落在 T 的值域裡。

**Narration (EN)**

> Many important problems in mathematics have the same shape: a linear operator is given, and for a given target vector the equation is to be solved. The condition for a solution to exist is exactly that the target lies in the range of the operator.

**動畫**

兩個橢圓 V 與 W，W 裡面再套一個 R(T)。值域內外各放一個點——內側的（ACCENT_B）有解，外側的（WARN）無解。

## Beat 1 — 把值域當成新的上域 / make the range the new codomain
*配音長度：中文 12.8s ／ 英文 11.5s*

**畫面公式**

```
把值域當成新的上域   |   make the range the new codomain
R ( T )  =  W        T  :  onto
```

**旁白（繁中）**

> 假設我們認得那個值域，那乾脆把值域當成新的上域，於是可以假設 T 是滿的。但「解出來」到底是什麼意思，還需要講清楚。

**Narration (EN)**

> Suppose we know how to recognize that range. Then we may as well make it the new codomain, and so assume the map is surjective. But what solving the equation means still has to be pinned down.

**動畫**

同一張圖，但 W 縮成剛好等於值域：把值域當成新的上域之後，T 就是滿的。

## Beat 2 — 求解程序就是一個右逆 / a solution process is a right inverse
*配音長度：中文 12.8s ／ 英文 13.4s*

**畫面公式**

```
求解程序就是一個右逆   |   a solution process is a right inverse
S  :  W → V        T ∘ S  =  I𝑤
```

**旁白（繁中）**

> 貫穿所有重要例子的原則是：一個求解程序，其實是在算 T 的一個右逆——一個從上域回到定義域的線性算子，跟 T 合起來剛好是恆等。

**Narration (EN)**

> The principle running through all the important instances is this: a solution process computes a right inverse of T, that is, a linear operator back from the codomain whose composition with T is the identity.

**動畫**

V 與 W 之間兩條反向的箭頭，T 往右、S 往左，兩條錯開上下排以免疊在一起。

## Beat 3 — 解要隨目標線性地變化 / the solution must vary linearly
*配音長度：中文 13.5s ／ 英文 12.0s*

**畫面公式**

```
解要隨目標線性地變化   |   the solution must vary linearly
η  ↦  ξ        linear
```

**旁白（繁中）**

> 換句話說，求解程序替每個目標挑一個解，而且挑法要讓那個解隨著目標線性地變化。把這個當作「解」的意思，就有了一個乾淨的說法。

**Narration (EN)**

> Put another way, a solution process picks one solution for each target, and picks it so that the solution varies linearly with the target. Taking that as the meaning of solving gives a clean statement.

**動畫**

不是一個點對一個點，而是**一整條線對一整條線**：W 裡三個共線的目標，各自連回 V 裡三個共線的解。「解隨目標線性變化」只有畫成線才看得出來。

## Beat 4 — 補空間與右逆一一對應 / complements match right inverses
*配音長度：中文 18.9s ／ 英文 18.5s*

**畫面公式**

```
補空間與右逆一一對應   |   complements match right inverses
M   complement of  N   ⇔   T ↾ M   iso        M  ↦  ( T ↾ M ) ⁻¹
```

**旁白（繁中）**

> 定理是這樣：T 是滿的線性映射、N 是它的零空間，那麼一個子空間是 N 的補空間，若且唯若 T 限制在它上面是同構。而「取那個限制的反函數」，正好是從所有這種補空間到所有線性右逆的雙射。

**Narration (EN)**

> The theorem: let T be a surjective linear map with null space N. Then a subspace is a complement of N exactly when the restriction of T to it is an isomorphism. And taking the inverse of that restriction is a bijection from all such complements onto all the linear right inverses.

**動畫**

軸測投影：N 畫成平面，補空間 M 畫成一條穿出平面的線。`assert MDIR[2] > 0.4` 釘住 M 真的離開了 N 的平面，否則圖會在說謊。

## Beat 5 — 把變數換成 T / substitute T for the variable
*配音長度：中文 15.5s ／ 英文 14.7s*

**畫面公式**

```
把變數換成 T   |   substitute T for the variable
q ( t ) = Σ₀ˡ cₖ tᵏ        q ( T ) = Σ₀ˡ cₖ Tᵏ        Tˡ = T ∘ … ∘ T
```

**旁白（繁中）**

> 接著換一個題目：T 的多項式。給定一個多項式與一個固定的算子，把變數換成那個算子，就得到一個新的算子；其中算子的次方，就是它跟自己合成那麼多次。

**Narration (EN)**

> Now a different subject: polynomials in T. Given a polynomial and a fixed operator, replace the variable by the operator and a new operator results, where a power of the operator means composing it with itself that many times.

**動畫**

上下兩個框：q(t) 與 q(T)，中間一支箭頭標 t ↦ T。次方就是自我合成。

## Beat 6 — 多項式相乘，對應算子合成 / multiplying polynomials is composing
*配音長度：中文 16.5s ／ 英文 16.5s*

**畫面公式**

```
多項式相乘，對應算子合成   |   multiplying polynomials is composing
p = p₁ p₂   ⇒   p ( T ) = p₁ ( T ) ∘ p₂ ( T )        p₁ ( T ) ∘ p₂ ( T ) = p₂ ( T ) ∘ p₁ ( T )
```

**旁白（繁中）**

> 合成的雙線性告訴我們：多項式相乘，對應到算子的合成。所以同一個 T 的任兩個多項式，在合成之下都可以交換次序。加法那邊更直接，直接對應過去。

**Narration (EN)**

> The bilinearity of composition tells us that multiplying polynomials corresponds to composing operators. So any two polynomials in the same T commute with each other under composition. Addition is more direct still, and carries over as it stands.

**動畫**

兩列相同的方框、次序相反（p₁∘p₂ 與 p₂∘p₁），右邊匯進同一個 p(T) 框：兩條路走到同一個算子，所以可交換。

## Beat 7 — 三個運算同時被保持 / all three operations preserved
*配音長度：中文 20.5s ／ 英文 18.2s*

**畫面公式**

```
三個運算同時被保持   |   all three operations preserved
p  ↦  p ( T )   :   homomorphism
```

**旁白（繁中）**

> 於是「把多項式送到對應算子」這個對應，同時保持加法、乘法與數乘。這種把一個代數系統的所有運算都保持住的映射，叫做代數同態。同態是個通用的詞——向量空間之間的同態，就是線性變換。

**Narration (EN)**

> So sending a polynomial to its operator preserves addition, multiplication and scalars at once. A map preserving all the operations of an algebraic system is called an algebra homomorphism. The word is general: a homomorphism of vector spaces is a linear transformation.

**動畫**

左右兩個大框（多項式的代數／算子的代數），中間三條橫箭頭把 p+q、p·q、cp 分別對到 P+Q、P∘Q、cP。三個運算並排，而不是用文字說「保持三個運算」。

## Beat 8 — 互質，就湊得出一 / relatively prime: the combination is one
*配音長度：中文 15.1s ／ 英文 12.6s*

**畫面公式**

```
互質，就湊得出一   |   relatively prime: the combination is one
p₁ , p₂   rel . prime   ⇒   a₁ p₁ + a₂ p₂ = 1
```

**旁白（繁中）**

> 接下來要用到一個代數上的事實：兩個多項式互質的時候，一定存在另外兩個多項式，讓它們的組合等於一。這件事書上直接假設，證明留給代數課。

**Narration (EN)**

> One algebraic fact is needed: when two polynomials are relatively prime, there are two further polynomials whose combination of them equals one. The book assumes this and leaves the proof to algebra.

**動畫**

一條被框起來的貝祖等式 a₁p₁ + a₂p₂ = 1，下面一行說明互質的意思。

## Beat 9 — 不變：T 把它送進自己 / invariant: T carries it into itself
*配音長度：中文 13.9s ／ 英文 11.7s*

**畫面公式**

```
不變：T 把它送進自己   |   invariant: T carries it into itself
T [ M ] ⊂ M        N = N ( q ( T ) )   invariant
```

**旁白（繁中）**

> 還要一個詞：子空間在 T 之下不變，意思是 T 把它送進它自己裡面。定理說，任何一個 T 的多項式，它的零空間在 T 之下都是不變的。

**Narration (EN)**

> One more word: a subspace is invariant under T if T carries it into itself. The theorem says that for any polynomial in T, its null space is invariant under T.

**動畫**

M 平面上一個向量，經 T 之後仍落在同一個平面裡，虛線連起像與原像：不變的意思就是「送進自己」。

## Beat 10 — 零空間裂成直和 / the null space splits into a direct sum
*配音長度：中文 24.2s ／ 英文 18.0s*

**畫面公式**

```
零空間裂成直和   |   the null space splits into a direct sum
q = q₁ q₂        N  =  N₁  ⊕  N₂        N = ⊕₁ᵐ Nᵢ
```

**旁白（繁中）**

> 而如果那個多項式分解成兩個互質的因子，零空間就正好是兩個因子各自零空間的直和。證明的關鍵，是拿剛才那條互質的式子造出一對投影。推論再用歸納推廣到任意多個互質因子——這條後面解常係數微分方程、證對稱矩陣可對角化都要用。

**Narration (EN)**

> And if that polynomial factors into two relatively prime factors, the null space is the direct sum of the null spaces of the factors. The proof turns the relatively prime equation into a pair of projections, and a corollary extends it by induction to any number of factors.

**動畫**

q = q₁q₂ 的框，加上軸測圖：N₁ 是平面、N₂ 是穿出去的線，兩塊直和成整個零空間。
