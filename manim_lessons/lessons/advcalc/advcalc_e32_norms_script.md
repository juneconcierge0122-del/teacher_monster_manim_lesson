# advcalc E32 — 第 3 章：範數

Chapter 3: Norms

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 2 節的前段（書頁 121–123）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e32_norms.py`（`AdvCalcE32ZH` / `AdvCalcE32EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[32]` / `FORMULAS_ADVCALC[32]`）
- 配音：`manim_lessons/samples/audio_e32/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.21 分（193 秒）／英文 2.96 分（177 秒）

## 兩種「大小」的例子是算出來的

`TALL` 是一個底邊只有 0.2 的尖峰（最高點 1、面積 1/10），`WIDE` 是一條高 1/4 的平台
（最高點 1/4、面積 1/4）。四個數字都由場景檔用梯形法在 `Fraction` 上精確算出來，圖也是照著同一組
座標畫的。

`assert` 在這裡救了一次：初稿的 `TALL` 是底邊佔滿整個區間的三角形，面積 1/2，**比平台的 1/4 還大**
——旁白說的「尖峰面積小」在圖上是反的。斷言擋下來之後才改成真正的尖峰。

---

## Beat 0 — 絕對值只被用到三件事 / the absolute value was used for exactly three things
*配音長度：中文 16.4s ／ 英文 18.3s*

**畫面公式**

```
絕對值只被用到三件事   |   the absolute value was used for exactly three things
| x | > 0   ( x ≠ 0 )        | x y | = | x | | y |        | x + y | ≤ | x | + | y |
```

**旁白（繁中）**

> 上一節的證明裡，絕對值只被用到三件事：不是零的東西絕對值為正、乘積的絕對值是絕對值的乘積、以及三角不等式。這一節把這三條抽出來，搬到向量空間上。

**Narration (EN)**

> In last section's proofs the absolute value was used for exactly three things: a nonzero number has positive absolute value, the absolute value of a product is the product of the absolute values, and the triangle inequality. This section lifts those three onto a vector space.

**動畫**

三個方框寫出絕對值被用到的三條性質，右邊各配一句白話：非零的量出正數、縮放乘進去、三角不等式。

## Beat 1 — 「多大」不只一種答案 / how large has more than one answer
*配音長度：中文 15.3s ／ 英文 14.7s*

**畫面公式**

```
「多大」不只一種答案   |   how large has more than one answer
p ( f )  =  max | f |        q ( f )  =  ∫ ₐᵇ | f |
```

**旁白（繁中）**

> 但高維度有個新問題：大小不只一種說法。拿一個定義在區間上的正連續函數，問它「多大」，至少有兩個合理的答案——曲線的最高點，還有曲線底下的面積。

**Narration (EN)**

> But dimension brings a new problem: size has more than one meaning. Take a positive continuous function on an interval and ask how large it is. At least two answers are reasonable: the highest point of the curve, and the area underneath it.

**動畫**

左邊一條高瘦的折線標著 max，右邊同一條折線畫上底下的填色標著 ∫——同一個函數，兩個都合理的「多大」。

## Beat 2 — 兩種大小不會一起變小 / the two sizes do not shrink together
*配音長度：中文 18.6s ／ 英文 13.1s*

**畫面公式**

```
兩種大小不會一起變小   |   the two sizes do not shrink together
p ( f )  小        ⇎        q ( f )  小
```

**旁白（繁中）**

> 這兩個答案不會一起變小。一個又高又細的尖峰，面積可以很小，但最高點很大；反過來一條低而長的曲線，最高點小，面積卻不小。所以不能只留一種，兩種各有各適用的問題。

**Narration (EN)**

> The two do not shrink together. A tall thin spike has small area and a large maximum; a low broad curve has a small maximum and an area that is not small. So neither answer can simply replace the other.

**動畫**

兩條自己造的折線並排並填色：左邊高瘦尖峰（max = 1、∫ = 1/10），右邊低而長的平台（max = 1/4、∫ = 1/4）。四個數字都是照著畫出來的折線用梯形法精確算的。

## Beat 3 — 範數的三條公理 / the three axioms of a norm
*配音長度：中文 18.9s ／ 英文 16.1s*

**畫面公式**

```
範數的三條公理   |   the three axioms of a norm
n1 :  p ( α ) > 0   ( α ≠ 0 )        n2 :  p ( x α ) = | x | p ( α )        n3 :  p ( α + β ) ≤ p ( α ) + p ( β )
```

**旁白（繁中）**

> 範數的定義就只要求這三條。第一，非零向量的範數是正的。第二，把向量乘上一個數，範數就乘上那個數的絕對值。第三，兩個向量相加，範數不會超過各自範數的和。

**Narration (EN)**

> The definition asks for only three things. First, a nonzero vector has positive norm. Second, multiplying a vector by a number multiplies its norm by the size of that number. Third, the norm of a sum is at most the sum of the norms.

**動畫**

n1、n2、n3 三個方框寫出三條公理，右邊各配中英名稱：正性、齊次性、三角不等式。

## Beat 4 — 賦範線性空間與距離 / a normed linear space, and distance
*配音長度：中文 16.5s ／ 英文 16.4s*

**畫面公式**

```
賦範線性空間與距離   |   a normed linear space, and distance
⟨ V , p ⟩        ‖ α ‖        ‖ ξ − ζ ‖  ≤  ‖ ξ − η ‖  +  ‖ η − ζ ‖
```

**旁白（繁中）**

> 一個向量空間配上一個範數，叫賦範線性空間。範數常寫成兩條直線包起來。把 α 減 β 的範數當成兩點的距離，第三條就變成幾何裡熟悉的三角不等式。

**Narration (EN)**

> A vector space together with a norm is a normed linear space. The norm is usually written between double bars. Read the norm of alpha minus beta as the distance between two points and the third axiom becomes the triangle inequality of ordinary geometry.

**動畫**

上方一個 ⟨ V , p ⟩ 的方框，底下三個點 ξ、η、ζ 連成一個三角形，直的那一邊與繞路的兩邊用不同顏色。

## Beat 5 — 座標空間上最常用的三個 / the three in common use on a Cartesian space
*配音長度：中文 16.3s ／ 英文 15.1s*

**畫面公式**

```
座標空間上最常用的三個   |   the three in common use on a Cartesian space
‖ x ‖ ₁ = Σ | x ᵢ |        ‖ x ‖ ₂ = ( Σ x ᵢ² ) ¹ᐟ²        ‖ x ‖ ∞ = max | x ᵢ |
```

**旁白（繁中）**

> 座標空間上最常用的有三個：所有座標的絕對值相加、平方和開根號、以及只取最大的那一個。它們分別記成下標一、下標二、下標無窮，三個都在後面會用到。

**Narration (EN)**

> On a Cartesian space three norms are in common use: add the sizes of all the coordinates; add their squares and take the root; or take the largest of them. They are written with subscript one, subscript two and subscript infinity.

**動畫**

一個具體向量 ⟨ 3 , −4 ⟩，三行分別是下標一、下標二、下標無窮的公式與它在這個向量上的值（7、5、4）。

## Beat 6 — 同樣三個，換成函數空間 / the same three on a space of functions
*配音長度：中文 16.3s ／ 英文 15.8s*

**畫面公式**

```
同樣三個，換成函數空間   |   the same three on a space of functions
‖ f ‖ ₁ = ∫ | f |        ‖ f ‖ ₂ = ( ∫ | f | ² ) ¹ᐟ²        ‖ f ‖ ∞ = max | f |
```

**旁白（繁中）**

> 同一組寫法搬到連續函數空間也成立，只要把求和換成積分：絕對值的積分、平方積分再開根號、還有函數的最大值。三個都是範數，量的卻是不同的事情。

**Narration (EN)**

> The same three transfer to a space of continuous functions, with integrals in place of sums: the integral of the absolute value, the square integral under a root, and the maximum of the function. All three are norms, and they measure different things.

**動畫**

同樣三行換成函數空間的版本：絕對值的積分、平方積分開根號、最大值，左邊一支箭頭標著「求和換成積分」。

## Beat 7 — 哪個好證，哪個要等第 5 章 / which are easy, and which waits for chapter five
*配音長度：中文 18.8s ／ 英文 19.4s*

**畫面公式**

```
哪個好證，哪個要等第 5 章   |   which are easy, and which waits for chapter five
‖ · ‖ ₂        ⇐        ( α , β )        ( Ch 5 )
```

**旁白（繁中）**

> 難易差很多。下標一那個直接就能驗；下標無窮的下一拍講；下標二最麻煩，它的三角不等式要靠內積，那是第 5 章的事。至於實數線上，絕對值是唯一的範數，差一個常數倍。

**Narration (EN)**

> They differ in difficulty. Subscript one is checked directly; subscript infinity is next; subscript two is the awkward one, since its triangle inequality rests on scalar products, which wait for chapter five. On the line the absolute value is the only norm, up to a constant.

**動畫**

三個方框由易到難排下來：下標一直接可驗、下標無窮下一拍、下標二要等第 5 章的內積。

## Beat 8 — 引理 2.1：把範數搬到別的空間 / lemma 2.1: carrying a norm to another space
*配音長度：中文 17.3s ／ 英文 17.3s*

**畫面公式**

```
引理 2.1：把範數搬到別的空間   |   lemma 2.1: carrying a norm to another space
T : V → W   ,   null T = { 0 }        ⇒        p ∘ T   :   V → ℝ
```

**旁白（繁中）**

> 引理 2.1 是個省事的工具：如果 p 是 W 上的範數，而 T 是從 V 到 W 的單射線性映射，那麼先做 T 再取 p，就是 V 上的一個範數。單射是必要的，否則非零向量會量出零。

**Narration (EN)**

> Lemma 2.1 is a labour-saving tool: if p is a norm on W and T is an injective linear map from V to W, then doing T first and then p is a norm on V. Injectivity is needed, or a nonzero vector would be measured as zero.

**動畫**

V → W → ℝ 三個方框串起來，T 與 p 標在箭頭上，底下一條線把整條合成標成 p ∘ T。

## Beat 9 — 有界函數構成一個向量空間 / the bounded functions form a vector space
*配音長度：中文 17.6s ／ 英文 14.7s*

**畫面公式**

```
有界函數構成一個向量空間   |   the bounded functions form a vector space
ℬ ( A , ℝ )        | f |  ⊂  [ 0 , b ]
```

**旁白（繁中）**

> 最後看下標無窮這一族。取任意一個非空集合 A，考慮 A 上所有有界的實值函數。它們構成一個向量空間，因為兩個有界函數的線性組合還是有界的——界加起來就是新的界。

**Narration (EN)**

> Now the subscript infinity family. Take any nonempty set A and the real-valued functions on it that are bounded. They form a vector space, because a linear combination of bounded functions is bounded: the bounds simply add.

**動畫**

一條上下振盪的曲線，上下兩條虛線是 ± b，說明 ℬ ( A , ℝ ) 收的是被夾住的那些函數。

## Beat 10 — 均勻範數：用最小上界定義 / the uniform norm, defined by a least upper bound
*配音長度：中文 20.8s ／ 英文 16.6s*

**畫面公式**

```
均勻範數：用最小上界定義   |   the uniform norm, defined by a least upper bound
‖ f ‖ ∞  =  lub { | f ( p ) |  :  p ∈ A }        | f + g | ≤ ‖ f ‖ ∞ + ‖ g ‖ ∞
```

**旁白（繁中）**

> 在這上面定義：f 的範數是所有函數值絕對值的最小上界。三角不等式的驗證很典型——先逐點放大成兩個範數的和，那個和就成了一個界，而最小上界比任何界都小或相等。這個兩步的手法後面會一再出現。

**Narration (EN)**

> On that space the norm of f is the least upper bound of the sizes of its values. Checking the triangle inequality is typical of the subject: enlarge pointwise to the sum of the two norms, so that sum is a bound, and the least upper bound is at most any bound.

**動畫**

一條鋸齒狀的曲線，一條虛線壓在它的峰頂上標著 ‖ f ‖ ∞，更上面一條較鬆的界標著 b——最小上界就是壓得最低的那一條。
