# advcalc E12 — 第 1 章：投影、注入與線性映射的拆裝

Chapter 1: Projections, Injections and Taking Maps Apart

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 3 節（書頁 46–52）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e12_injections.py`（`AdvCalcE12ZH` / `AdvCalcE12EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[12]` / `FORMULAS_ADVCALC[12]`）
- 配音：`manim_lessons/samples/audio_e12/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 2.98 分（179 秒）／英文 2.68 分（161 秒）

---

## Beat 0 — 拆成一堆各自獨立的問題 / split into independent questions
*配音長度：中文 16.4s ／ 英文 14.1s*

**畫面公式**

```
拆成一堆各自獨立的問題   |   split into independent questions
T : V → ∏ᵢ Wᵢ   linear   ⇔   πᵢ ∘ T   linear   ( ∀i )
```

**旁白（繁中）**

> 先看一個定理：如果上域是積空間，那麼一個映射是線性的，若且唯若每一個座標投影接在它後面之後都是線性的。這把「往積空間裡送」化約成一堆各自獨立的問題。

**Narration (EN)**

> Start from a theorem: if the codomain is a product space, a mapping is linear exactly when each coordinate projection composed after it is linear. That reduces mapping into a product to a set of independent questions.

**動畫**

左邊 V，一支箭頭送進積空間的三格方塊，右邊三支箭頭各自讀出一個 πᵢ∘T。

## Beat 1 — 第 i 個投影接上去，就是第 i 列 / the ith projection gives the ith row
*配音長度：中文 15.2s ／ 英文 14.0s*

**畫面公式**

```
第 i 個投影接上去，就是第 i 列   |   the ith projection gives the ith row
skeleton ( πᵢ ∘ T )  =  row i of  t
```

**旁白（繁中）**

> 這件事把上一節接了回來。從 n 維座標空間到 m 維座標空間的線性映射，第 i 個座標投影接上去之後，得到的線性泛函，它的 skeleton 正好是矩陣的第 i 列。

**Narration (EN)**

> It ties back to the last section. For a linear map from coordinate n-space to coordinate m-space, composing the ith coordinate projection after it gives the linear functional whose skeleton is the ith row of the matrix.

**動畫**

兩列三行的矩陣，第一列橫框起來，箭頭指到右邊那個線性泛函的 skeleton 三元組。

## Beat 2 — 一條向量方程換成 m 條純量方程 / one vector equation, m scalar ones
*配音長度：中文 16.6s ／ 英文 14.4s*

**畫面公式**

```
一條向量方程換成 m 條純量方程   |   one vector equation, m scalar ones
y = T ( x )        ⇔        yᵢ = Σⱼ tᵢⱼ xⱼ
```

**旁白（繁中）**

> 所以之前把一條向量方程換成 m 條純量方程時，我們做的就是「讀出第 i 個座標」。用代數的話說，是把一個線性映射換成一組線性映射，而剛才的定理保證這兩者等價。

**Narration (EN)**

> So when we replaced one vector equation by m scalar equations, what we were doing was reading off the ith coordinate. In algebraic terms, replacing one linear map by a set of them, which the theorem says is equivalent.

**動畫**

上面一條向量方程，箭頭分岔到下面兩條純量方程。

## Beat 3 — 向量空間，再加上一個乘法 / a vector space with a multiplication
*配音長度：中文 19.5s ／ 英文 16.2s*

**畫面公式**

```
向量空間，再加上一個乘法   |   a vector space with a multiplication
A ∘ ( B ∘ C ) = ( A ∘ B ) ∘ C        A ∘ ( B + C ) = A∘B + A∘C
```

**旁白（繁中）**

> 再看定義域與上域都是同一個 V 的情形。這個空間除了是向量空間，還對合成封閉，而合成永遠滿足結合律。加上分配律與純量的相容性，這種結構叫做代數。所以 Hom V 是一個代數。

**Narration (EN)**

> Now take the case where the domain and codomain are the same V. Besides being a vector space it is closed under composition, and composition is always associative. With the distributive laws and the scalar relation, that structure is called an algebra.

**動畫**

Hom(V) 的方框裡列出三個運算：前兩個是原本的向量運算，第三個合成是新的。

## Beat 4 — 但這個乘法不可交換 / but this multiplication does not commute
*配音長度：中文 13.8s ／ 英文 13.3s*

**畫面公式**

```
但這個乘法不可交換   |   but this multiplication does not commute
Hom ( V )   :   algebra        S ∘ T  ≠  T ∘ S
```

**旁白（繁中）**

> 之前見過的實值函數空間也是代數，但那裡的乘法是可交換的。Hom V 的乘法通常不可交換，除非 V 是零空間，或者跟實數線同構。

**Narration (EN)**

> The real-valued function spaces seen earlier are algebras too, but there multiplication is commutative. In Hom of V it is not, unless V is the trivial space or is isomorphic to the real line.

**動畫**

同一支向量分別經 S∘T 與 T∘S，兩支結果明顯落在不同位置——座標有 assert 過確實分得開。

## Beat 5 — 注入：放進第 j 格，其他放零 / an injection: into slot j, zeros elsewhere
*配音長度：中文 16.3s ／ 英文 14.9s*

**畫面公式**

```
注入：放進第 j 格，其他放零   |   an injection: into slot j, zeros elsewhere
θⱼ ( α )  =  ⟨ 0 , … , α , … , 0 ⟩
```

**旁白（繁中）**

> 除了座標投影，積空間上還有第二類基本的線性映射，叫做注入。第 j 個注入把第 j 個因子裡的一個向量，送到「在第 j 個位置放它、其他位置全放零」的那個元素。

**Narration (EN)**

> Besides the coordinate projections there is a second class of basic linear maps on a product: the injections. The jth injection takes a vector in the jth factor to the element having that value at index j and zero everywhere else.

**動畫**

左邊一個 W₂ 的橢圓，箭頭經 θ₂ 把它放進積空間方塊的第二格，其他格填零。

## Beat 6 — 投影與注入的三條等式 / three identities relating them
*配音長度：中文 17.2s ／ 英文 15.7s*

**畫面公式**

```
投影與注入的三條等式   |   three identities relating them
πⱼ ∘ θⱼ = Iⱼ        πⱼ ∘ θᵢ = 0   ( i ≠ j )        Σₖ θₖ ∘ πₖ = I
```

**旁白（繁中）**

> 投影與注入的關係就寫成兩條等式：投影接在自己的注入後面是恆等；接在別人的注入後面是零。而如果指標集是有限的，把每一個「注入接投影」加起來，正好就是恆等變換。

**Narration (EN)**

> Their relationship is two identities: a projection after its own injection is the identity, and after any other injection it is zero. And if the index set is finite, summing injection-after-projection over all indices gives the identity.

**動畫**

兩列小方塊：接自己的投影得到恆等，接別人的投影得到零。

## Beat 7 — 把 T 拆成兩個線性泛函 / T comes apart into two functionals
*配音長度：中文 16.4s ／ 英文 15.8s*

**畫面公式**

```
把 T 拆成兩個線性泛函   |   T comes apart into two functionals
t = [ 2 , −1 , 1 ; 1 , 1 , 4 ]        l₁ = π₁ ∘ T        l₂ = π₂ ∘ T
```

**旁白（繁中）**

> 舉個例子。一個從三維到二維的線性映射，矩陣是兩列三行。第一個座標投影接上去，得到的線性泛函的 skeleton 就是第一列，所以可以把它拆成兩個線性泛函。

**Narration (EN)**

> An example. Take a linear map from three-space to the plane with a two by three matrix. Composing the first coordinate projection gives the linear functional whose skeleton is the first row, so the map comes apart into two linear functionals.

**動畫**

兩列三行的矩陣畫兩次，各自框住第一列與第二列，箭頭指到兩個線性泛函。

## Beat 8 — 再用同一條等式裝回去 / and the same identity puts it back
*配音長度：中文 11.4s ／ 英文 10.9s*

**畫面公式**

```
再用同一條等式裝回去   |   and the same identity puts it back
( θ₁ ∘ π₁ + θ₂ ∘ π₂ ) ( T ( x ) )  =  T ( x )
```

**旁白（繁中）**

> 而把它們裝回去，用的正好就是剛才那條等式：兩個「注入接投影」加起來是恆等，套在原來的映射上就把它還原了。

**Narration (EN)**

> Putting them back together uses exactly that identity: the two injection-after-projection terms sum to the identity, and applied to the original map they reassemble it.

**動畫**

兩個泛函各自經 θ 再匯進一個 Σ 方塊，箭頭指回 T——拆開與裝回是同一條等式的兩個方向。

## Beat 9 — 一族映射，恰好裝成一個 / a family of maps, one assembly
*配音長度：中文 15.5s ／ 英文 14.5s*

**畫面公式**

```
一族映射，恰好裝成一個   |   a family of maps, one assembly
Tᵢ ∈ Hom ( V , Wᵢ )   ⇒   ∃ ! T ,   Tᵢ = πᵢ ∘ T        T = Σ θᵢ ∘ Tᵢ
```

**旁白（繁中）**

> 寫成一般形式：給定一族從共同定義域出發、分別到各個因子的線性映射，那麼恰好有一個到積空間的線性映射，使得每個座標投影接上去之後，得到的都是原來那一個。

**Narration (EN)**

> In general form: given a family of linear maps out of a common domain into the separate factors, there is exactly one linear map into the product such that composing each coordinate projection after it returns the one you started with.

**動畫**

左邊一疊 Tᵢ 方塊，箭頭全部收進右邊唯一的一個 T。

## Beat 10 — 定義域是積空間時的對稱說法 / the symmetric statement on the domain
*配音長度：中文 20.3s ／ 英文 16.8s*

**畫面公式**

```
定義域是積空間時的對稱說法   |   the symmetric statement on the domain
T = Σⱼ Tⱼ ∘ πⱼ        Tⱼ ∈ Hom ( Vⱼ , W )
```

**旁白（繁中）**

> 定義域是積空間的時候，也有一個對稱的說法。這個定理對任意積空間都成立，不管有限無限，而且它其實刻畫了積空間。書上承認這些看起來太形式，但說等到後面要處理更複雜的情況時就會用上。

**Narration (EN)**

> There is a symmetric statement when the domain is the product instead. The theorem holds for all product spaces, finite or not, and in fact characterizes them. The book grants this looks overly formal, but says it helps later in more complicated situations.

**動畫**

上下兩列：一列是上域為積空間，一列是定義域為積空間，兩者對稱。
