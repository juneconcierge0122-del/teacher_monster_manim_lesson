# advcalc E08 — 第 1 章：矩陣、核與同構

Chapter 1: Matrices, the Kernel and Isomorphism

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 1 節（書頁 32–36）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e08_matrices_kernel.py`（`AdvCalcE08ZH` / `AdvCalcE08EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[8]` / `FORMULAS_ADVCALC[8]`）
- 配音：`manim_lessons/samples/audio_e08/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.21 分（193 秒）／英文 2.93 分（176 秒）

---

## Beat 0 — 線性泛函：skeleton 是一組數 / a functional: the skeleton is numbers
*配音長度：中文 19.3s ／ 英文 17.3s*

**畫面公式**

```
線性泛函：skeleton 是一組數   |   a functional: the skeleton is numbers
bᵢ = F ( δ ⁱ )        F ( x )  =  Σ₁ⁿ bᵢ xᵢ
```

**旁白（繁中）**

> 先看最簡單的情形：上域是實數線。這時 skeleton 的每一個元素都只是一個數，所以整個 skeleton 就是一個數字 n 元組。把它寫成係數放在變數前面，這個線性泛函就是「係數乘座標再加起來」。

**Narration (EN)**

> Take the simplest case first: the codomain is the real line. Then every element of the skeleton is just a number, so the skeleton is an n-tuple of numbers. Written as coefficients in front of the variables, the functional is coefficients times coordinates, summed.

**動畫**

四個單位向量餵進 F，各自掉出一個數；底下用一個框把那四個數圈成一組係數。

## Beat 1 — 泛函與座標空間自然對應 / functionals correspond to the space itself
*配音長度：中文 15.0s ／ 英文 15.0s*

**畫面公式**

```
泛函與座標空間自然對應   |   functionals correspond to the space itself
{ F : ℝⁿ → ℝ }   ⟷   ℝⁿ
```

**旁白（繁中）**

> 所以 n 維座標空間上所有線性泛函，與這個空間自己有一個自然的一一對應：由泛函去取它在各個單位向量的值就得到那組係數，由係數去做加權和就得到泛函。

**Narration (EN)**

> So the linear functionals on coordinate n-space are in natural one-to-one correspondence with that space itself: evaluating a functional at the unit vectors gives the coefficients, and forming the weighted sum from the coefficients gives back the functional.

**動畫**

兩欄點一一對應：所有線性泛函，與座標空間自己。

## Beat 2 — 每一項是一個 m 元組 / each entry is an m-tuple
*配音長度：中文 16.0s ／ 英文 14.9s*

**畫面公式**

```
每一項是一個 m 元組   |   each entry is an m-tuple
βⱼ  =  T ( δ ʲ )  ∈  ℝᵐ        t  =  { tᵢⱼ }
```

**旁白（繁中）**

> 接著看上域是 m 維座標空間的情形。這時 skeleton 的每一個元素都是一個 m 元組。把每個 m 元組畫成一直行，n 個 m 元組並排，就得到一個長方形的數字陣列。

**Narration (EN)**

> Now let the codomain be coordinate m-space. Each element of the skeleton is then an m-tuple. Picture each m-tuple as a column, set the n of them side by side, and what appears is a rectangular array of numbers.

**動畫**

三個直行的數字方塊，每個上面標著 T 在該單位向量的值，並排就成了長方形陣列。

## Beat 3 — 矩陣的行就是 skeleton / the columns of the matrix are the skeleton
*配音長度：中文 11.9s ／ 英文 14.1s*

**畫面公式**

```
矩陣的行就是 skeleton   |   the columns of the matrix are the skeleton
t  :  m × n        columns ( t )  =  skeleton ( T )
```

**旁白（繁中）**

> 這個帶兩個指標的數組就叫 T 的矩陣，是 m 乘 n 的——m 列 n 行。矩陣唯一決定了 T，因為它的各行正好就是 T 的 skeleton。

**Narration (EN)**

> That doubly indexed array is called the matrix of T, an m by n matrix, with m rows and n columns. The matrix determines T uniquely, because its columns are exactly the skeleton of T.

**動畫**

同一個陣列，三行各自用一種顏色框起來，底下標回它對應的單位向量——行就是 skeleton。

## Beat 4 — 攤開成 m 個純量方程 / written out as m scalar equations
*配音長度：中文 17.2s ／ 英文 16.7s*

**畫面公式**

```
攤開成 m 個純量方程   |   written out as m scalar equations
yᵢ  =  Σⱼ₌₁ⁿ tᵢⱼ xⱼ        ( i = 1 , … , m )
```

**旁白（繁中）**

> 把線性組合映射攤開來算，就得到 m 個純量方程：第 i 個輸出等於「第 i 列的係數，分別乘上對應的輸入座標，再加起來」。這就是書上的定理，也是一般線性方程組的來歷。

**Narration (EN)**

> Writing the combination mapping out gives m scalar equations: the ith output is the coefficients in the ith row, each multiplied by the matching input coordinate, and summed. That is the book's theorem, and it is where a general system of linear equations comes from.

**動畫**

同一個陣列，第 i 列橫框、輸入向量直框，右邊等號後面是第 i 個輸出。

## Beat 5 — 矩陣與線性映射一一對應 / matrices and linear maps correspond
*配音長度：中文 13.9s ／ 英文 14.3s*

**畫面公式**

```
矩陣與線性映射一一對應   |   matrices and linear maps correspond
{ t : m × n }  ⟷  { T : ℝⁿ → ℝᵐ }        F  :  1 × n
```

**旁白（繁中）**

> 反過來，每一個 m 乘 n 的矩陣都決定一個線性映射，所以矩陣與線性映射之間也是雙射。線性泛函對應到只有一列的矩陣，也就是一列 n 行。

**Narration (EN)**

> Conversely every m by n matrix determines a linear map, so matrices and linear maps correspond bijectively too. A linear functional matches a matrix with a single row, that is one row and n columns.

**動畫**

兩欄點一一對應（矩陣與線性映射），底下多一列標出「只有一列的矩陣就是線性泛函」。

## Beat 6 — 座標泛函 / the coordinate functionals
*配音長度：中文 19.0s ／ 英文 15.9s*

**畫面公式**

```
座標泛函   |   the coordinate functionals
πᵢ ( f )  =  f ( i )        πᵢ ( s f + t g ) = s πᵢ ( f ) + t πᵢ ( g )
```

**旁白（繁中）**

> 還有一類特別的線性泛函叫座標泛函：在指標集上的函數空間裡，取第 i 個位置的值。它顯然是線性的——事實上，函數上的向量運算當初就是為了讓這些取值映射變成線性的，才那樣定義的。

**Narration (EN)**

> Another special family is the coordinate functionals: on a function space over an index set, take the value at the ith place. These are plainly linear. In fact the vector operations on functions were defined precisely to make these evaluations linear.

**動畫**

一條函數曲線，在指標 i 處拉一條虛線取值，箭頭把那個值拉出來。

## Beat 7 — 子空間的像還是子空間 / the image of a subspace is a subspace
*配音長度：中文 16.7s ／ 英文 15.1s*

**畫面公式**

```
子空間的像還是子空間   |   the image of a subspace is a subspace
T [ L ( A ) ]  =  L ( T [ A ] )        T ⁻¹ [ Y ]  ⊂  V
```

**旁白（繁中）**

> 接下來是幾個結構上的結果。線性把線性擴張送到像的線性擴張，所以子空間的像還是子空間；而且子空間的原像也還是子空間。這兩件事之後會一直用到。

**Narration (EN)**

> Now some structural results. A linear map carries a linear span onto the span of the images, so the image of a subspace is a subspace; and the preimage of a subspace is a subspace as well. Both facts get used constantly later.

**動畫**

左邊一片過原點的平面，被 T 壓成右邊的一條直線——降了一維，但仍然是子空間。

## Beat 8 — 核：被壓成零的那些向量 / the kernel: what collapses to zero
*配音長度：中文 21.2s ／ 英文 17.8s*

**畫面公式**

```
核：被壓成零的那些向量   |   the kernel: what collapses to zero
N ( T ) = T ⁻¹ ( 0 )        R ( T ) = T [ V ]        T  inj  ⇔  N ( T ) = { 0 }
```

**旁白（繁中）**

> 被 T 送到零向量的那些向量，自己構成一個子空間，叫做零空間或核；T 的值域則是整個定義域的像。有了核就有一個很方便的判準：T 是嵌射，若且唯若它的核只有零向量。這比逐一去比對兩個向量省事得多。

**Narration (EN)**

> The vectors sent to zero form a subspace, the null space or kernel, and the range of T is the image of the whole domain. The kernel gives a test: T is injective exactly when its kernel is only the zero vector, far less work than comparing vectors in pairs.

**動畫**

同一片平面，這次把被壓成零的那個方向用紅線標出來；右邊那條線上，原點被畫成紅點。

## Beat 9 — 同構：同一個空間的兩種寫法 / isomorphism: one space, two notations
*配音長度：中文 23.2s ／ 英文 17.9s*

**畫面公式**

```
同構：同一個空間的兩種寫法   |   isomorphism: one space, two notations
⟨ c₁ , … , cₙ ⟩  ↦  Σ₀ⁿ⁻¹ cᵢ₊₁ xⁱ        ℝⁿ  ≅  { deg < n }
```

**旁白（繁中）**

> 既線性又雙射的映射叫同構。兩個空間同構，意思是它們「有相同的形式」，作為抽象的向量空間根本就是同一個，只能靠它們有沒有的向量性質來區分。書上的例子是：n 維座標空間，與次數小於 n 的多項式所成的空間，是同構的。

**Narration (EN)**

> A map both linear and bijective is an isomorphism. Isomorphic spaces have the same form: as abstract spaces they are the same, told apart only by vector properties they do or do not have. The book pairs coordinate n-space with the polynomials of degree less than n.

**動畫**

左邊三個係數方塊，箭頭連到右邊對應的多項式項，一項對一項。

## Beat 10 — 特徵向量與特徵值 / eigenvectors and eigenvalues
*配音長度：中文 19.4s ／ 英文 17.1s*

**畫面公式**

```
特徵向量與特徵值   |   eigenvectors and eigenvalues
T ( α )  =  x α        α  :  eigenvector        x  :  eigenvalue
```

**旁白（繁中）**

> 最後，當線性映射是從 V 到它自己的時候，會發生一些特別的事。可能有某個向量被送到自己的倍數，這時這個向量叫做特徵向量，那個倍數叫做特徵值。這條線索到第二章與第五章會再展開。

**Narration (EN)**

> Finally, when a linear map goes from V to itself, special things can happen. Some vector may be carried to a multiple of itself, and then that vector is called an eigenvector and the multiple an eigenvalue. This thread is picked up again in chapters two and five.

**動畫**

一支向量被 T 送到同一條線上更遠的位置（特徵向量），另一支被轉離了原來的方向（不是）。
