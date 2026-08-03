# advcalc E03 — 第 0 章：函數、映射與合成

Chapter 0: Functions, Mappings and Composition

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 0 章第 7 到 9 節（書頁 10–15）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e03_functions.py`（`AdvCalcE03ZH` / `AdvCalcE03EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[3]` / `FORMULAS_ADVCALC[3]`）
- 配音：`manim_lessons/samples/audio_e03/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.65 分（219 秒）／英文 3.25 分（195 秒）

---

## Beat 0 — 函數是一種特別的關係 / a function is a special kind of relation
*配音長度：中文 18.6s ／ 英文 18.9s*

**畫面公式**

```
函數是一種特別的關係   |   a function is a special kind of relation
⟨x,y⟩ ∈ f  &  ⟨x,z⟩ ∈ f  ⇒  y = z        y = f ( x )  ⇔  ⟨x,y⟩ ∈ f
```

**旁白（繁中）**

> 函數是一種特別的關係：定義域裡的每一個 x，恰好只配上一個值域元素 y。寫成條件就是，如果 x 配 y 而且 x 也配 z，那麼 y 就等於 z。由 f 與 x 唯一決定的那個 y，就寫成 f 括號 x。

**Narration (EN)**

> A function is a special kind of relation: each element x of the domain is paired with exactly one range element y. As a condition: if x is paired with y and x is also paired with z, then y equals z. The y thus uniquely determined by f and x is written f of x.

**動畫**

兩組雙欄箭頭圖並排：左邊每個 x 恰好一條箭頭（是函數），右邊有一個 x 分岔出兩條（不是函數）。

## Beat 1 — 主動的函數，被動的關係 / the function active, the relation passive
*配音長度：中文 20.5s ／ 英文 17.1s*

**畫面公式**

```
主動的函數，被動的關係   |   the function active, the relation passive
f  :  x  ↦  f ( x )
```

**旁白（繁中）**

> 人們傾向把函數看成主動的，把不是函數的關係看成被動的。函數作用在定義域裡的一個元素上，給出一個值；我們拿 x 來套用 f，所以也常把函數叫做算子。而一般的關係並沒有特定的 y，配對就比較被動。

**Narration (EN)**

> One tends to think of a function as active and a relation that is not a function as passive. A function acts on an element of its domain to give a value; we take x and apply f to it, so a function is often called an operator. A plain relation pairs more passively.

**動畫**

保留左邊的函數圖，右側三行說明主動與被動的對比，以及為什麼函數也被叫做算子。

## Beat 2 — 帶尾巴的箭頭記法 / the stopped arrow notation
*配音長度：中文 18.2s ／ 英文 17.4s*

**畫面公式**

```
帶尾巴的箭頭記法   |   the stopped arrow notation
x  ↦  x²
```

**旁白（繁中）**

> 我們常常是靠指定每一點的值來定義函數，這時會用一種帶尾巴的箭頭表示配對。x 對應到 x 的平方，就是把每個數配上它的平方的那個函數。要讓這個記法有意義，定義域必須是清楚的。

**Narration (EN)**

> Often we define a function by specifying its value at each point, and then a stopped arrow notation indicates the pairing. x stopped-arrow x squared is the function assigning to each number its square. For this notation to mean anything, the domain must be understood.

**動畫**

四組具體配對：1 對 1、2 對 4、3 對 9、−2 對 4。最後一行用紅字，因為 2 與 −2 同時落在 4，正是下一拍反關係分岔的原因。右側說明定義域必須清楚。

## Beat 3 — 反關係通常不是函數 / the inverse is usually not a function
*配音長度：中文 19.3s ／ 英文 18.0s*

**畫面公式**

```
反關係通常不是函數   |   the inverse is usually not a function
f : x ↦ x²        f ⁻¹  ⊃  ⟨ 4 , 2 ⟩ , ⟨ 4 , −2 ⟩
```

**旁白（繁中）**

> 如果 f 是函數，它的反關係一定是關係，但通常不是函數。平方就是例子：它的反關係同時含有四配二與四配負二這兩對，所以不是函數。反關係也是函數的那種 f，就叫做一對一。

**Narration (EN)**

> If f is a function its relational inverse is certainly a relation, but in general not a function. Squaring is the example: its inverse contains both four paired with two and four paired with minus two, so it is not a function. An f whose inverse is a function is called one-to-one.

**動畫**

書上 Fig. 0.3：左邊是開口向上的拋物線（平方函數），右邊是側躺的反關係，並在 4 的位置標出上下兩個紅點——同一個 4 配上兩個值。右圖的水平軸刻意放在畫面中段，否則下半支會穿過說明文字掉進字幕區。

## Beat 4 — 從 A 到 B 的函數，隱含三件事 / f from A to B implies three things
*配音長度：中文 19.9s ／ 英文 19.7s*

**畫面公式**

```
從 A 到 B 的函數，隱含三件事   |   f from A to B implies three things
f : A → B        ⟨ f , A , B ⟩        dom f = A  ,  range f ⊂ B
```

**旁白（繁中）**

> 從 A 到 B 的函數這個記法，隱含了三件事：f 是函數、f 的定義域正好是 A、而且 f 的值域包含於 B。很多人覺得函數本來就該包含這三樣，也就是應該看成 f、A、B 這個有序三元組，其中 B 叫做上域。

**Narration (EN)**

> The notation f from A to B implies three things: that f is a function, that its domain is exactly A, and that its range is included in B. Many feel a function should include all of this, that is, be considered the ordered triple f, A, B, where B is called the codomain.

**動畫**

雙欄圖，A 有四點、B 有五點，右側三行拆解「從 A 到 B 的函數」隱含的三件事，並點出 B 叫上域。

## Beat 5 — 嵌射、滿射、雙射 / injective, surjective, bijective
*配音長度：中文 22.0s ／ 英文 18.3s*

**畫面公式**

```
嵌射、滿射、雙射   |   injective, surjective, bijective
1–1 : inj        range f = B : surj        inj & surj : bij
```

**旁白（繁中）**

> 書上把映射、變換這些詞留給這個三元組。一個映射如果是一對一的就叫嵌射，如果值域正好等於上域就叫滿射，兩者都成立就叫雙射。函數對它自己的值域永遠是滿的，說它是滿射，指的是值域等於那個講好的上域。

**Narration (EN)**

> The book keeps the words map, mapping and transformation for that triple. A mapping is injective if it is one-to-one, surjective if its range equals the codomain, and bijective if both. A function is always onto its own range, so surjective refers to the stated codomain.

**動畫**

三組雙欄圖並排，分別是嵌射、滿射、雙射；每組下方各自標註（不是用空格排版，否則英文會對不準）。

## Beat 6 — 所有這種對象所成的集合 / the set of all such objects
*配音長度：中文 22.8s ／ 英文 19.8s*

**畫面公式**

```
所有這種對象所成的集合   |   the set of all such objects
{ f : A → S }        χ : S → { 0 , 1 }
```

**旁白（繁中）**

> 現代數學有個習慣：一種新的對象一出現，馬上就去看所有這種對象所成的集合。有了從 A 到 S 的函數，自然就去看所有這種函數所成的集合。子集則對應到特徵函數，取值只有零與一，所以所有子集所成的集合寫成二的 S 次方。

**Narration (EN)**

> A habit of the modern mathematician: once a new object appears, look at the set of all such objects. Having functions from A to S, consider the set of them all. Subsets correspond to characteristic functions taking only zero and one, so the set of all subsets is written two to the S.

**動畫**

上方是所有從 A 到 S 的函數所成的集合，下方是特徵函數的寫法，說明子集如何對應到取值零與一的函數。

## Beat 7 — 有序三元組 / the ordered triple
*配音長度：中文 22.5s ／ 英文 17.2s*

**畫面公式**

```
有序三元組   |   the ordered triple
⟨ x , y , z ⟩  =  ⟨ ⟨ x , y ⟩ , z ⟩        ℝ³  =  ( ℝ × ℝ ) × ℝ
```

**旁白（繁中）**

> 有序三元組通常定義成前兩個先配成對、再與第三個配對。理由是兩個變數的函數，通常被看成單一個有序對變數的函數。於是三維空間就定義成平面再乘上實數線；不過三元組也可以讀成長度三的序列，那是另一個對象。

**Narration (EN)**

> An ordered triple is usually defined as the first two paired, then paired with the third, because a function of two variables is read as a function of one ordered pair variable. So three-space is the plane crossed with the line, though a triple can also be read as a sequence.

**動畫**

兩行公式：有序三元組定義成前兩個先配對，以及三維空間由此定義；下方解釋為什麼要這樣定。

## Beat 8 — 為精確付出的代價；指標集合 / the price of precision; indexed sets
*配音長度：中文 19.0s ／ 英文 17.2s*

**畫面公式**

```
為精確付出的代價；指標集合   |   the price of precision; indexed sets
{ xᵢ : i ∈ I }        i  ↦  xᵢ
```

**旁白（繁中）**

> 這種把其實不同的兩個對象視為同一的含糊，是為了精確而付出的必要代價；在數學還比較模糊的年代，本來就只有一個籠統的概念。指標集合也一樣：一個加了指標的集合，其實就是那個指標函數。

**Narration (EN)**

> This blurring, identifying two objects that are really distinct, is a necessary price for deciding exactly what things are; when mathematics was vaguer there was one fuzzy notion instead. Indexed sets are the same: an indexed set is really just the indexing function.

**動畫**

五組上下對應的點與箭頭，上排是指標 i₁ 到 i₅，下排是被指到的對象——加了指標的集合其實就是那個指標函數。

## Beat 9 — 一般的笛卡兒積 / the general Cartesian product
*配音長度：中文 15.3s ／ 英文 12.9s*

**畫面公式**

```
一般的笛卡兒積   |   the general Cartesian product
∏ Sᵢ  =  { f  :  dom f = I  ,  f ( i ) ∈ Sᵢ }
```

**旁白（繁中）**

> 一般的笛卡兒積就由此定義。一族用 I 編號的集合，它們的乘積是所有這樣的函數所成的集合：定義域是 I，而且在每一個 i 上取的值都落在對應的那個集合裡。

**Narration (EN)**

> The general Cartesian product is defined from this. For a collection of sets indexed by I, their product is the set of all functions with domain I whose value at each i lies in the corresponding set.

**動畫**

一般笛卡兒積的定義式，下方兩行拆解「定義域是 I」與「每個 i 上的值落在對應集合裡」。

## Beat 10 — 合成、恆等、反映射 / composition, the identity, the inverse
*配音長度：中文 21.1s ／ 英文 18.7s*

**畫面公式**

```
合成、恆等、反映射   |   composition, the identity, the inverse
( g ∘ f ) ( x ) = g ( f ( x ) )        f ∘ ( g ∘ h ) = ( f ∘ g ) ∘ h
```

**旁白（繁中）**

> 最後是合成。g 與 f 的合成，把 x 送到 g 括號 f 括號 x。這大概是數學裡最基本的二元運算，而且滿足結合律。恆等映射把每個元素送回它自己。而一個映射有反映射，若且唯若它是雙射。

**Narration (EN)**

> Finally composition. The composition of g with f sends x to g of f of x. It is perhaps the basic binary operation of mathematics, and it is associative. The identity map sends each element to itself, and a mapping has an inverse exactly when it is bijective.

**動畫**

兩組雙欄圖串成 A 到 B 到 C，底下一條長箭頭標成 g 圈 f；上方點出有反映射若且唯若是雙射。
