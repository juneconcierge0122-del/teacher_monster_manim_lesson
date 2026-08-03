# advcalc E01 — 第 0 章：邏輯、量詞與連接詞

Chapter 0: Logic, Quantifiers and the Connectives

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 0 章第 1 到 3 節（書頁 1–6）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e01_quantifiers.py`（`AdvCalcE01ZH` / `AdvCalcE01EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[1]` / `FORMULAS_ADVCALC[1]`）
- 配音：`manim_lessons/samples/audio_e01/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.52 分（211 秒）／英文 3.15 分（189 秒）

---

## Beat 0 — 敘述與敘述框架 / statements and statement frames
*配音長度：中文 23.0s ／ 英文 18.0s*

**畫面公式**

```
敘述與敘述框架   |   statements and statement frames
P ( x ) :  x < 4          P ( 5 ) :  5 < 4
```

**旁白（繁中）**

> 這一集開始讀第 0 章。作者說這章主要是給人回頭查閱用的，但其中有一件事非讀不可，就是量詞的順序。先從最基本的說起：一個句子如果當下就能判斷真假，叫做敘述；含有變數、要給了值才能判斷的，叫做敘述框架。

**Narration (EN)**

> This episode starts chapter zero. The authors say it is mainly there to be referred back to, but one thing in it must be read: the order of quantifiers. First the basics. A sentence that is true or false as it stands is a statement; one containing a variable is a statement frame.

**動畫**

左右兩個面板：左邊「敘述」（1 小於 2 為真、4 加 3 等於 5 為假），右邊「敘述框架」（x 小於 4、x 小於 y、3x² 加 y² 等於 10）。兩組例子都取自書頁 1；面板內的列垂直置中，兩欄行數不同也能對齊。

## Beat 1 — 全稱量詞 / the universal quantifier
*配音長度：中文 17.9s ／ 英文 17.1s*

**畫面公式**

```
全稱量詞   |   the universal quantifier
( ∀x ) P ( x )          ( ∀x ) ( x < 4 )
```

**旁白（繁中）**

> 從框架變出敘述有兩條路。第一條是給變數一個值。第二條是宣告它永遠為真，也就是在前面加上「對每一個 x」，這叫全稱量詞；同義的說法有「對所有的 x」與「對每個 x」。

**Narration (EN)**

> There are two ways to turn a frame into a statement. One is to give the variable a value. The other is to assert that it is always true, by prefixing 'for every x'. That prefix is the universal quantifier; 'for each x' and 'for all x' say the same thing.

**動畫**

中央是框架方塊，兩條箭頭往左下與右下分岔：左邊「給 x 一個值」得到 P(5)，右邊「宣告永遠為真」得到全稱量詞。

## Beat 2 — 存在量詞；束縛變數與自由變數 / the existential quantifier; bound and free
*配音長度：中文 19.4s ／ 英文 17.3s*

**畫面公式**

```
存在量詞；束縛變數與自由變數   |   the existential quantifier; bound and free
( ∃x ) P ( x )          ( ∀x ) ( x < 4 )  :  x  bound
```

**旁白（繁中）**

> 另一條路是宣告它有時為真，寫成「存在一個 x 使得」，這叫存在量詞。被量詞綁住的變數叫束縛變數，沒被綁住的叫自由變數。加上量詞以後 x 還留在句子裡，但它已經不能再被賦值了。

**Narration (EN)**

> The other way is to assert that it is sometimes true, written 'there exists an x such that'. That is the existential quantifier. A quantified variable is called bound, an unquantified one free. The x is still in the sentence, but it can no longer be given values.

**動畫**

右下再長出第三條：「宣告有時為真」得到存在量詞；左下標出 x 自由與 x 束縛的對比。

## Beat 3 — 兩種量詞混用時，順序會改變意思 / with both kinds, the order changes the meaning
*配音長度：中文 13.6s ／ 英文 12.3s*

**畫面公式**

```
兩種量詞混用時，順序會改變意思   |   with both kinds, the order changes the meaning
( ∃y ) ( ∀x ) P ( x , y )        ≠        ( ∀x ) ( ∃y ) P ( x , y )
```

**旁白（繁中）**

> 現在來到這一節最重要的地方。如果句子裡有兩個自由變數，就需要兩個量詞；而當兩種量詞混用時，寫的順序會改變整句話的意思。

**Narration (EN)**

> Now the most important point in this section. A sentence with two free variables needs two quantifiers, and when quantifiers of both kinds are used, the order in which they are written changes what the sentence says.

**動畫**

上方數線淡入：四個 x（橘）各自配一個 y（青），每個 x 上方有自己的小箭頭指向它的 y——y 跟著 x 跑。右端標 T。

## Beat 4 — 書上的例子 / the book's own example
*配音長度：中文 18.3s ／ 英文 16.9s*

**畫面公式**

```
書上的例子   |   the book's own example
( ∀x ) ( ∃y ) ( x < y )  =  T          ( ∃y ) ( ∀x ) ( x < y )  =  F
```

**旁白（繁中）**

> 書上的例子是這樣。對每一個 x 都存在一個 y 使得 x 小於 y，這是真的，y 取 x 加一就行。但存在一個 y 使得對每一個 x 都有 x 小於 y，這是假的，因為那個 y 加一就不小於它自己。

**Narration (EN)**

> Here is the book's example. For every x there exists a y with x less than y is true: take y to be x plus one. But there exists a y such that for every x, x is less than y is false, because that y plus one is not less than itself.

**動畫**

下方數線淡入：同樣四個 x，但只有一個固定的 y₀（紫），旁邊畫出 y₀ + 1（紅）——它不小於自己，整句話垮掉。右端標 F。

## Beat 5 — 第二句強得多 / the second is by far the stronger statement
*配音長度：中文 19.3s ／ 英文 16.7s*

**畫面公式**

```
第二句強得多   |   the second is by far the stronger statement
y  =  x + 1          y₀ + 1  ≮  y₀
```

**旁白（繁中）**

> 差別在於，第一句裡的 y 可以跟著 x 改變，第二句卻要求同一個 y 對所有 x 都成立，所以第二句強得多。作者在這裡寫了一句很重的話：讀者必須把這一點弄得絕對清楚，他往後的整個數學生涯都繫於此。

**Narration (EN)**

> The difference is that in the first the y may change with x, while the second demands a single y that works for every x, which is far stronger. The authors put it bluntly: the reader must be absolutely clear on this point, his whole mathematical future is at stake.

**動畫**

畫面不變，兩條數線並置，讓旁白講「第二句強得多」時可以直接對照上下兩排。這是刻意不換圖的一拍。

## Beat 6 — 同種量詞可交換；收斂的定義 / same kind commutes; the definition of convergence
*配音長度：中文 21.2s ／ 英文 18.1s*

**畫面公式**

```
同種量詞可交換；收斂的定義   |   same kind commutes; the definition of convergence
( ∀x ) ( ∀y )  =  ( ∀x , y )        ( ∀ε ) ( ∃N ) ( ∀n > N ) | xₙ − x | < ε
```

**旁白（繁中）**

> 反過來，同一種量詞連在一起時，順序不影響意思，可以縮寫成一個量詞符號。而收斂與連續的定義都用到三個量詞：數列收斂是對每個誤差都存在一個項數，使得之後每一項都夠接近；函數連續的定義形式完全一樣。

**Narration (EN)**

> Among quantifiers of the same kind the order does not matter, and they can be abbreviated into one symbol. Convergence and continuity both need three quantifiers: for every error there is an index beyond which every term is close enough, and continuity has exactly the same shape.

**動畫**

兩條數線淡出，換成三個量詞的收斂定義，上下各一行說明：同種量詞可交換、收斂與連續形式相同。

## Beat 7 — 而且、或 / and, or
*配音長度：中文 19.3s ／ 英文 17.8s*

**畫面公式**

```
而且、或   |   and, or
P & Q :  T F F F          P or Q :  T T T F
```

**旁白（繁中）**

> 接著是連接詞。「而且」只有兩邊都真的時候才真。「或」在日常語言裡有排他與相容兩種用法，數學不能容忍這種歧義，所以數學裡的「或」永遠是相容的：至少一個為真，兩個都真也算。

**Narration (EN)**

> Next, the connectives. And is true only when both sides are true. Or is used in ordinary speech both exclusively and inclusively; mathematics cannot tolerate that ambiguity, so in mathematics or is always inclusive: at least one is true, and possibly both.

**動畫**

兩張真值表並排：而且（TFFF）與或（TTTT），下方強調數學裡的「或」永遠是相容的。

## Beat 8 — 最麻煩的「如果就」 / the troublesome if-then
*配音長度：中文 18.6s ／ 英文 16.8s*

**畫面公式**

```
最麻煩的「如果就」   |   the troublesome if-then
P ⇒ Q :  T F T T          F  ⟺  P = T  &  Q = F
```

**旁白（繁中）**

> 最麻煩的是「如果就」。因為「若 x 小於三則 x 小於五」對每一個 x 都成立，我們被迫承認前提為假時整句話仍然是真的。所以只有在前提真、而結論假的時候，這個句子才是假的。

**Narration (EN)**

> The troublesome one is if-then. Since if x is less than three then x is less than five holds for every x, we are forced to accept that the whole sentence is true whenever the premise is false. So it is false only when the premise is true and the conclusion false.

**動畫**

換成蘊涵的真值表（TFTT），右側列出書頁 4 的三個代入例：2 小於 3、4 小於 3、6 小於 3，全部為真，逼出「前提為假時整句為真」。

## Beat 9 — 恆真式與三條常用等價 / tautologies and three useful equivalences
*配音長度：中文 20.6s ／ 英文 20.8s*

**畫面公式**

```
恆真式與三條常用等價   |   tautologies and three useful equivalences
∼( P or Q ) ⇔ (∼P) & (∼Q)        ∼( P ⇒ Q ) ⇔ P & (∼Q)
```

**旁白（繁中）**

> 真值表永遠為真的形式叫恆真式；任何不涉及量詞的有效推理原則，都必須用恆真式表達。常用的等價有三條：非「P 或 Q」等於非 P 且非 Q；「P 蘊涵 Q」等於「Q 或非 P」；非「P 蘊涵 Q」等於「P 且非 Q」。

**Narration (EN)**

> A form whose truth table is always true is called a tautology, and any valid principle of reasoning not involving quantifiers must be expressed by one. Three useful equivalences: not P or Q is not P and not Q; P implies Q is Q or not P; not of P implies Q is P and not Q.

**動畫**

左側是「P 或非 P」的真值表，整欄都是 T，示範什麼叫恆真式；右側放公式列沒位置放的第三條等價。

## Beat 10 — 量詞的否定 / negating a string of quantifiers
*配音長度：中文 20.1s ／ 英文 17.4s*

**畫面公式**

```
量詞的否定   |   negating a string of quantifiers
∼(∀x)(∃y)(∀z) P ( x , y , z )   ⇔   (∃x)(∀y)(∃z) ∼P ( x , y , z )
```

**旁白（繁中）**

> 最後是量詞的否定。「並非總是真」與「有時為假」意思相同，這條規則可以把否定號一路推過整串量詞。實用的規則是：取否定時，把每個量詞換成相反的那一種，再把否定號移到整串的最後面。

**Narration (EN)**

> Finally, negating quantifiers. Not always true means the same as sometimes false, and that lets a negation sign move past a whole string of quantifiers. The practical rule: change each quantifier to the opposite kind, and move the negation sign to the end of the string.

**動畫**

上下兩行：帶否定號的量詞串，箭頭往下，變成每個量詞都翻面、否定號跑到最後。
