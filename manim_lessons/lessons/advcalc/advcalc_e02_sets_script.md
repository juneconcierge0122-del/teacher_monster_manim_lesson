# advcalc E02 — 第 0 章：集合、受限變數與關係

Chapter 0: Sets, Restricted Variables and Relations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 0 章第 4 到 6 節（書頁 6–10）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e02_sets.py`（`AdvCalcE02ZH` / `AdvCalcE02EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[2]` / `FORMULAS_ADVCALC[2]`）
- 配音：`manim_lessons/samples/audio_e02/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.75 分（225 秒）／英文 3.36 分（202 秒）

---

## Beat 0 — 集合與成員 / sets and membership
*配音長度：中文 21.4s ／ 英文 18.1s*

**畫面公式**

```
集合與成員   |   sets and membership
x  ∈  A
```

**旁白（繁中）**

> 現在的數學把每一個對象都定義成某種集合，所以要先把這個最基本的概念看清楚。集合是一堆對象的聚集，而這個聚集本身也被當成一個實體。裡面的對象叫做元素或成員，表示屬於的符號是一個像大寫希臘字母的記號。

**Narration (EN)**

> Modern practice defines every mathematical object as a set of some kind, so this notion must be examined first. A set is a collection of objects that is itself considered an entity. Its objects are its elements, and the membership symbol is a sort of capital epsilon.

**動畫**

左邊一個圓（集合 A）裡有四個點，外面另有一個灰點 x，示範成員與非成員。

## Beat 1 — 兩個集合什麼時候是同一個 / when two sets are the same object
*配音長度：中文 19.0s ／ 英文 17.7s*

**畫面公式**

```
兩個集合什麼時候是同一個   |   when two sets are the same object
A = B    ⇔    ( ∀x ) ( x ∈ A  ⇔  x ∈ B )
```

**旁白（繁中）**

> 等號在數學裡表示邏輯上的同一。兩個集合被視為同一個對象，若且唯若它們的成員完全相同。所以集合相等這件事，整個化約成一句話：對每一個 x，x 屬於 A 若且唯若 x 屬於 B。

**Narration (EN)**

> The equals sign means logical identity. Two sets are considered the same object if and only if they have exactly the same members. So set equality reduces entirely to one line: for every x, x belongs to A if and only if x belongs to B.

**動畫**

兩個大小相同的圓 A 與 B，中間一個大等號：成員完全相同就是同一個對象。

## Beat 2 — 子集與包含 / subsets and inclusion
*配音長度：中文 18.4s ／ 英文 18.4s*

**畫面公式**

```
子集與包含   |   subsets and inclusion
A ⊂ B  :  ( ∀x ) ( x ∈ A ⇒ x ∈ B )      ( A = B ) ⇔ ( A ⊂ B ) & ( B ⊂ A )
```

**旁白（繁中）**

> 如果 A 的每個元素都是 B 的元素，就說 A 是 B 的子集，或說 A 包含於 B。於是 A 等於 B 等價於 A 包含於 B 而且 B 包含於 A。這是證明兩個集合相等最常用的辦法：分別證明兩個方向的包含。

**Narration (EN)**

> If every element of A is an element of B, then A is a subset of B, or A is included in B. So A equals B is equivalent to A included in B together with B included in A. That is the usual way of establishing set identity: prove both inclusions.

**動畫**

小圓 A 畫在大圓 B 裡面，右側兩行說明雙向包含，以及這正是證明集合相等的辦法。

## Beat 3 — 怎麼指定一個集合 / how a set gets specified
*配音長度：中文 21.6s ／ 英文 18.6s*

**畫面公式**

```
怎麼指定一個集合   |   how a set gets specified
{ 1 , 4 , 7 }    { x }    { x , y }        { x : x² < 9 }  =  ( −3 , 3 )
```

**旁白（繁中）**

> 有限集可以直接把成員列出來，用大括號框起來；只有一個成員的叫單元集，兩個的叫對集。無限集通常用敘述框架來定義，寫成滿足 P 的所有 x 所成的集合。例如平方小於九的所有實數，就是開區間負三到三。

**Narration (EN)**

> A finite set can have its members listed inside braces: one member gives a unit set, two a pair set. Infinite sets are generally defined by statement frames, the set of all x such that P of x. The reals whose square is under nine form the open interval minus three to three.

**動畫**

左欄列出四種指定集合的寫法（列舉、單元集、對集、敘述框架），右側是書上的例子：平方小於九等於開區間負三到三。

## Beat 4 — 空集 / the empty set
*配音長度：中文 20.4s ／ 英文 18.5s*

**畫面公式**

```
空集   |   the empty set
{ x : x ≠ x }  =  ∅        4 = { 0 , 1 , 2 , 3 }    1 = { 0 }    0 = ∅
```

**旁白（繁中）**

> 我們需要空集，就像算術裡需要零一樣。如果 P 從來不成立，那麼滿足 P 的集合就是空集；例如不等於自己的那些 x，構成的就是空集。作者順帶提到，四這個數本身通常定義成零一二三所成的集合。

**Narration (EN)**

> We need the empty set much as arithmetic needs zero. If P is never true, the set of x satisfying it is empty; the x that differ from themselves form the empty set. In passing, the authors note that the number four is usually defined as the set of zero, one, two and three.

**動畫**

空集用一個裡面只有 ∅ 記號的圓表示；右側列出書上把 4、1、0 定義成集合的寫法。

## Beat 5 — 受限變數與定義域 / restricted variables and the domain
*配音長度：中文 19.8s ／ 英文 17.8s*

**畫面公式**

```
受限變數與定義域   |   restricted variables and the domain
x  ∈  A  =  dom
```

**旁白（繁中）**

> 為了不讓集合這個詞過勞，書上還用類、聚集、族、總體這些同義詞。接下來是受限變數。數學裡的變數不能拿任意對象當值，它只能取某個集合裡的成員，這個集合就叫做該變數的定義域。

**Narration (EN)**

> To avoid overworking the word set, the book also uses class, collection, family and aggregate. Next, restricted variables. A variable is not allowed to take all objects as values; it can only take members of a certain set, called the domain of the variable.

**動畫**

一個標著 ℤ 的方框代表定義域，右側說明變數只能取這個集合裡的成員。

## Beat 6 — 受限量詞 / restricted quantifiers
*配音長度：中文 21.5s ／ 英文 18.0s*

**畫面公式**

```
受限量詞   |   restricted quantifiers
( ∀n ∈ ℤ ) P ( n )        { n ∈ ℤ : P ( n ) }
```

**旁白（繁中）**

> 定義域有時明講，更多時候是隱含的。例如字母 n 通常就代表整數。有疑慮的時候就明白寫出來，讀成對每一個屬於整數集的 n。注意這裡的屬於符號要讀成介系詞「在」。這種量詞叫做受限量詞。

**Narration (EN)**

> The domain is sometimes stated and more often implied: the letter n customarily means an integer. In case of doubt we write it out, read as for every n in the integers. Note that the membership symbol is read here as the preposition in. Such quantifiers are called restricted.

**動畫**

一個大的淡橢圓代表「所有對象」，裡面是標著 ℤ 的實線方框與五個整數點；右側一條箭頭指進方框，說明量詞只伸進定義域。刻意不重複公式列上的兩行寫法。

## Beat 7 — 展開成無限制變數 / unfolding into unrestricted variables
*配音長度：中文 21.2s ／ 英文 21.7s*

**畫面公式**

```
展開成無限制變數   |   unfolding into unrestricted variables
( ∀x ∈ A ) P ⇔ ( ∀x ) ( x ∈ A ⇒ P )      ( ∃x ∈ A ) P ⇔ ( ∃x ) ( x ∈ A & P )
```

**旁白（繁中）**

> 受限變數其實只是無限制變數的縮寫。全稱的情形展開成：對每一個 x，如果 x 屬於 A 就有 P。存在的情形展開成：存在一個 x，x 屬於 A 而且 P。一個用蘊涵、一個用而且，這兩者不能弄混。

**Narration (EN)**

> Restricted variables are just abbreviations of unrestricted ones. The universal case unfolds as: for every x, if x is in A then P. The existential case unfolds as: there exists an x with x in A and P. One uses implication, the other uses and; they must not be mixed up.

**動畫**

左右各一個放大的連接詞符號（蘊涵與而且）對比全稱與存在兩種展開；下方放書頁 8 第三條顯示式——受限的集合寫法，這條公式列沒位置放。

## Beat 8 — 有序對 / ordered pairs
*配音長度：中文 19.6s ／ 英文 16.8s*

**畫面公式**

```
有序對   |   ordered pairs
⟨ x , y ⟩ = ⟨ a , b ⟩  ⇔  x = a  &  y = b        ⟨ 1 , 3 ⟩  ≠  ⟨ 3 , 1 ⟩
```

**旁白（繁中）**

> 接著是有序對。它同樣被定義成某種集合，但我們不在乎是哪一種，只要它保證那個關鍵性質就好：兩個有序對相等，若且唯若第一個元素相等而且第二個元素相等。所以一三這個有序對不等於三一。

**Narration (EN)**

> Then ordered pairs. A pair is again taken to be some set, but we do not care which, so long as it guarantees the crucial property: two ordered pairs are equal exactly when their first elements agree and their second elements agree. So one three is not three one.

**動畫**

座標軸淡入，一個點加上兩條虛線引到兩軸，標成有序對；右欄強調順序是關鍵性質。

## Beat 9 — 關係就是一組有序對 / a relation is simply a set of ordered pairs
*配音長度：中文 19.6s ／ 英文 18.4s*

**畫面公式**

```
關係就是一組有序對   |   a relation is simply a set of ordered pairs
x R y    ⇔    ⟨ x , y ⟩  ∈  R
```

**旁白（繁中）**

> 對應或說關係，以及它的特例映射，是數學裡最基本的概念。既然關係的圖形是一組有序對，而現在的做法是把每個數學對象都看成集合，那就乾脆讓關係就是它的圖形：一個關係就是一組有序對。

**Narration (EN)**

> Correspondence, or relation, and its special case, mapping, are fundamental. Since the graph of a relation is a set of ordered pairs, and every object is now regarded as a set, it is efficient to take the graph to be the relation: a relation is simply a set of ordered pairs.

**動畫**

同一組座標軸上散佈七個點——關係就是它的圖形，一組有序對。

## Beat 10 — 定義域、值域、笛卡兒積 / domain, range, the Cartesian product
*配音長度：中文 22.6s ／ 英文 17.7s*

**畫面公式**

```
定義域、值域、笛卡兒積   |   domain, range, the Cartesian product
dom R = { x : (∃y) ⟨x,y⟩ ∈ R }        A × B = { ⟨x,y⟩ : x ∈ A & y ∈ B }
```

**旁白（繁中）**

> 由此就能定義：定義域是所有第一元素所成的集合，值域是所有第二元素所成的集合，反關係是把每一對顛倒過來。而第一元素在 A、第二元素在 B 的所有有序對所成的集合，叫做 A 與 B 的笛卡兒積；實數平面就是實數線乘上實數線。

**Narration (EN)**

> From this: the domain is the set of all first elements, the range the set of all second elements, and the inverse reverses every pair. All pairs with first element in A and second in B form the Cartesian product; the analytic plane is the reals times the reals.

**動畫**

在那七個點外面框出 A × B 的矩形，並把它們投影到兩軸上，分別標成 dom R（青）與 range R（紫）。
