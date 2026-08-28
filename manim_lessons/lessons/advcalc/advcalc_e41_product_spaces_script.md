# advcalc E41 — 第 3 章：微分與乘積空間

Chapter 3: The Differential and Product Spaces

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 8 節的前段（書頁 152–153）。書頁 155–156 是習題 8.1–8.10，後半段留給 E42。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e41_product_spaces.py`（`AdvCalcE41ZH` / `AdvCalcE41EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[41]` / `FORMULAS_ADVCALC[41]`）
- 配音：`manim_lessons/samples/audio_e41/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.01 分（181 秒）／英文 2.87 分（172 秒）

## 一個「最小的誠實例子」：內積

要講「定義域是乘積」，需要一個真的吃兩個向量變數的函數。內積是最小的那一個：
它雙線性、算得出來、兩個偏微分都寫得出封閉形式，而餘項剛好是 `ω(ξ, η)`，
一眼看得出是小 o。場景檔用它把這一節的每一句話都驗過：

- **兩個偏微分寫成 `ξ ↦ ξ·b` 與 `η ↦ a·η`**，斷言兩者之和跟真正的變化量差一個掉到零的餘項
  （三個取樣點，0.0167 → 0.00167 → 0.000167）。
- **另外一條路也走過一次**：把第二個變數固定住，對第一個變數做中央差商，斷言結果等於
  `ξ ↦ ξ·b`。這就是「偏微分的兩個定義是同一個東西」，程式而不是旁白在保證。
- **一般鏈鎖規則**用兩支內函數 `g¹(t) = (t, t²)`、`g²(t) = (1 − t, 2t)` 算：
  兩個偏微分接上兩支內函數的微分，得到 4 與 1，加起來 5；直接對合成微分也是 5。
  並且斷言兩項不相等（不然畫面上分不出誰是誰）。
- **值域是乘積那一半**用一個平面到平面的映射：兩個分量各自求梯度，疊成矩陣，
  再拿它去做餘項測試，斷言商掉到零。

`bounds.py` 抓到 beat 3 的軸測弧衝出上緣；`collide.py` 抓到 beat 6 的數字表壓到收尾字幕、
beat 8 的「固定住的變數」標籤壓到英文字幕。probe 幀又抓到 beat 7 的三行算式排太低。

---

## Beat 0 — m 個函數，就是一個 m 元組值的函數 / m functions are one tuple-valued function
*配音長度：中文 17.1s ／ 英文 16.4s*

**畫面公式**

```
m 個函數，就是一個 m 元組值的函數   |   m functions are one tuple-valued function
F  =  ⟨ F ¹ , … , F ᵐ ⟩ :  A  →  W  =  ∏ W ᵢ
```

**旁白（繁中）**

> 這一節把微分規則接到乘積空間。先看容易的一半：值域是乘積。定義在同一個定義域上的 m 個函數，跟一個取 m 元組值的函數，本來就是同一件事，只是寫法不同。

**Narration (EN)**

> This section carries the rules of differentiation over to product spaces. Take the easy half first, where the range is a product. An m-tuple of functions on one domain and a single m-tuple-valued function are already the same thing, written two ways.

**動畫**

左邊一個定義域的圓，兩支箭頭各自到 W₁ 與 W₂；右邊同一個定義域一支箭頭到堆疊起來的乘積空間。

## Beat 1 — 定理 8.1：分量可微就整體可微 / Theorem 8.1: componentwise is enough
*配音長度：中文 12.8s ／ 英文 13.6s*

**畫面公式**

```
定理 8.1：分量可微就整體可微   |   Theorem 8.1: componentwise is enough
dF ₐ     =     ⟨ dF ¹ ₐ , … , dF ᵐ ₐ ⟩
```

**旁白（繁中）**

> 定理 8.1 說這件事對可微也成立：F 在 α 可微，恰好等於每一個分量都在 α 可微，而且這時整個微分就是各分量微分排成的一組。

**Narration (EN)**

> Theorem 8.1 says the same holds for differentiability: F is differentiable at alpha exactly when every component is, and the whole differential is then the components' differentials gathered into a tuple.

**動畫**

兩個分量各自的微分（兩個列向量），下方疊成一個矩陣，右邊是餘項的商的表。

## Beat 2 — 證明靠嵌入與投影都是線性的 / the proof: injections and projections are linear
*配音長度：中文 15.1s ／ 英文 16.1s*

**畫面公式**

```
證明靠嵌入與投影都是線性的   |   the proof: injections and projections are linear
F  =  Σ  θ ⱼ ∘ F ʲ              F ʲ  =  π ⱼ ∘ F
```

**旁白（繁中）**

> 證明只有兩行，靠的是嵌入與投影都是線性的。把 F 寫成「嵌入接上分量」的和，每一項都可微；反過來把分量寫成「投影接上 F」，也是同樣的理由。

**Narration (EN)**

> The proof takes two lines and rests on the injections and projections being linear. Write F as a sum of injections composed with components, and every term is differentiable; conversely a component is a projection composed with F, for the same reason.

**動畫**

一個交換三角形：A 到 Wⱼ 是分量、Wⱼ 到 W 是嵌入、A 到 W 是 F 本身。

## Beat 3 — 引理 8.1：弧的切向量逐分量算 / Lemma 8.1: a tangent vector, component by component
*配音長度：中文 14.9s ／ 英文 15.1s*

**畫面公式**

```
引理 8.1：弧的切向量逐分量算   |   Lemma 8.1: a tangent vector, component by component
f ′ ( x )    =    ⟨ f ₁ ′ ( x ) , … , f ₙ ′ ( x ) ⟩
```

**旁白（繁中）**

> 弧是這件事的特例：一條取 n 元組值的弧可導，恰好等於每個分量可導，而切向量就是各分量導數排成的一組。這正是大家在座標下算切向量的做法。

**Narration (EN)**

> An arc is the special case: an n-tuple-valued arc is differentiable exactly when each component is, and the tangent vector is the components' derivatives gathered up. That is precisely how anyone computes a tangent vector in coordinates.

**動畫**

軸測投影的三維螺旋弧與它在一點的切向量，右邊是切向量的三個分量。

## Beat 4 — 定義域是乘積就沒這麼好 / a product domain is harder
*配音長度：中文 18.7s ／ 英文 18.0s*

**畫面公式**

```
定義域是乘積就沒這麼好   |   a product domain is harder
F ( ξ ₁ , … , ξ ₙ )              V  =  ∏ V ⱼ
```

**旁白（繁中）**

> 但定義域是乘積時就沒這麼好了。一個吃 n 個向量變數的函數，本身不會拆成 n 個函數：兩個變數的函數帶的資訊，比兩個一變數的函數多得多。它只有一個，只是輸入被切成了好幾塊。

**Narration (EN)**

> When the domain is a product it is not so easy. A function of n vector variables does not itself split into n functions: a function of two variables carries far more than two functions of one variable can. There is only one function; the input has been cut into pieces.

**動畫**

左邊一個被切成兩半的方框（V₁ × V₂），一支箭頭到右邊的 W——輸入分塊，函數只有一個。

## Beat 5 — 偏微分：把微分限制到一個因子 / a partial differential is a restriction
*配音長度：中文 13.6s ／ 英文 13.7s*

**畫面公式**

```
偏微分：把微分限制到一個因子   |   a partial differential is a restriction
dF ʲ ₐ     =     dF ₐ ∘ θ ⱼ      ∈   Hom ( V ⱼ , W )
```

**旁白（繁中）**

> 不過它的微分會拆。把 α 的微分限制到第 j 個因子上，得到的就叫 F 在 α 的第 j 個偏微分，它是一個從第 j 個因子到值域的有界線性映射。

**Narration (EN)**

> Its differential does split, though. Restrict the differential at alpha to the jth factor and what comes back is called the jth partial differential of F at alpha, a bounded linear map from that factor into the range.

**動畫**

同一個方框，藍色粗線是第二個因子那一條，一支箭頭出去代表限制在那條線上的微分。

## Beat 6 — 微分等於各偏微分之和 / the differential is the sum of the partials
*配音長度：中文 20.8s ／ 英文 17.0s*

**畫面公式**

```
微分等於各偏微分之和   |   the differential is the sum of the partials
dF ₐ ( ξ )     =     Σ  dF ⁱ ₐ ( ξ ᵢ )
```

**旁白（繁中）**

> 因為任何向量都寫得成各分量嵌入之和，而微分是線性的，作用在它身上就等於各偏微分作用在各分量上再加起來。這是有限和，項數就是因子的個數。這就是「多變數的微分等於偏微分之和」的精確版本。

**Narration (EN)**

> Since any vector is the sum of its components injected back in, and the differential is linear, applying it gives the sum of the partial differentials applied to the components. It is a finite sum, one term per factor, and it is the precise version of the familiar formula.

**動畫**

一個向量拆成兩個分量的三角形，右邊是兩條式子與內積例子的餘項表。

## Beat 7 — 一般鏈鎖規則 / the general chain rule
*配音長度：中文 15.8s ／ 英文 15.0s*

**畫面公式**

```
一般鏈鎖規則   |   the general chain rule
d ( F ∘ G ) ᵧ    =    Σ  dF ⁱ ∘ dg ⁱ              4 + 1  =  5
```

**旁白（繁中）**

> 把它跟鏈鎖規則接起來，就得到一般的鏈鎖規則：合成的微分等於各個偏微分接上各個內函數的微分再求和。畫面上是一個內積的例子，算出來是四加一等於五。

**Narration (EN)**

> Joining this to the chain rule gives the general chain rule: the differential of a composite is the sum of each partial differential composed with the corresponding inner differential. On screen an inner product example works out to four plus one.

**動畫**

ℝ 到 V₁ × V₂ 到 ℝ 的三個方框，下方是 4、1、5 三個算出來的數。

## Beat 8 — 把其他變數固定住，也得到同一個東西 / freezing the others gives the same object
*配音長度：中文 15.0s ／ 英文 15.1s*

**畫面公式**

```
把其他變數固定住，也得到同一個東西   |   freezing the others gives the same object
ΔF ₐ ∘ θ ⱼ     =     T ⱼ    +    o
```

**旁白（繁中）**

> 偏微分還有一個更直接的定義，而且那才是實際遇到的：把其他變數固定住，剩下的那個一變數函數的微分，就是偏微分。兩個定義講的是同一個東西。

**Narration (EN)**

> There is a more direct definition of a partial differential, and it is the one met in practice: hold the other variables fixed and take the differential of the one variable function that remains. The two definitions describe the same object.

**動畫**

一個格子，紅色那一橫排代表「第二個變數釘住」，只剩第一個能動。

## Beat 9 — 實務上先遇到的是偏微分 / in practice the partials come first
*配音長度：中文 20.3s ／ 英文 15.4s*

**畫面公式**

```
實務上先遇到的是偏微分   |   in practice the partials come first
ξ ᵢ  =  α ᵢ    ( i ≠ j )              ∂ F / ∂ x ⱼ
```

**旁白（繁中）**

> 為什麼要強調這件事？因為實務上先算得出來的幾乎都是偏微分，每次只動一個變數，其他的當常數。整個微分反而是後來才拼出來的——順序跟定義的順序剛好相反，這也是下一集那個定理要處理的問題。

**Narration (EN)**

> Why insist on this? Because in practice the partial differentials are what can be computed first, one variable moved at a time with the rest held constant. The whole differential is assembled afterwards, in the reverse of the order the definitions came in.

**動畫**

左邊兩個偏微分的方框，兩支箭頭指向右邊整個微分的方框——實務上的計算方向。

## Beat 10 — 引理 8.2：只有一個方向成立 / Lemma 8.2: only one direction holds
*配音長度：中文 16.8s ／ 英文 16.5s*

**畫面公式**

```
引理 8.2：只有一個方向成立   |   Lemma 8.2: only one direction holds
dF ₐ  ∃              ⇒              dF ⁱ ₐ  ∃     ( ∀ i )
```

**旁白（繁中）**

> 引理 8.2 把方向講清楚：可微一定推得出所有偏微分都存在，而且等於那個限制。反過來——偏微分全部存在能不能推出可微——一般是不行的，下一集講要補什麼條件。

**Narration (EN)**

> Lemma 8.2 fixes the direction: differentiable forces every partial differential to exist and to equal that restriction. The converse, whether all the partials force differentiability, generally fails; next time, what has to be added.

**動畫**

一支往右的粗箭頭與一支被打叉的往左箭頭，下方是引理 8.2 的等式。

---

## 值域可以拆，定義域不行

這一集真正要講的是這個不對稱。值域是乘積時，「到乘積去」等於「分別到每個因子去」，
所以定理 8.1 幾乎是定義的重述。定義域是乘積時，「從乘積出發」不等於「分別從每個因子出發」——
兩個變數的函數帶的資訊，比兩個一變數的函數多得多。所以那一側只有偏微分，沒有對應的定理。

## 偏微分的兩個定義

一個是「把整個微分限制到一個因子」（定義用的），一個是「把其他變數固定住再微分」（實際算的）。
書上特別說明後者才是實務上先遇到的，所以把它當成真正的定義。場景檔在內積那個例子上
把兩條路各走一次，確認結果相同。
