# advcalc E59 — 第 4 章：緊緻性與均勻性

Chapter 4: Compactness and Uniformity

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 5 節「緊緻性與均勻性」（書頁 210–214，習題 5.1–5.14 在 214–215）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e59_uniformity.py`（`AdvCalcE59ZH` / `AdvCalcE59EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[59]` / `FORMULAS_ADVCALC[59]`）
- 配音：`manim_lessons/samples/audio_e59/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.46 分（208 秒）／英文 3.38 分（203 秒）

## 「均勻」就是把量詞反過來

這一節的主題只有一句話：**逐點的性質是「對每個 y 存在一個 d」，均勻的性質是「存在一個 d 對每個 y」**——
差別只在兩個量詞的順序。均勻連續、均勻收斂、均勻等度連續都是同一個模式的三次套用。
接著問的是「什麼時候逐點會自動升級成均勻」，答案是緊緻性——但只對連續有效，對收斂無效。

畫面上五拍的數字都是算出來的，不是畫個示意圖：

- **三個標準反例各自算出讓它失敗的那組數**。x 的 n 次方：在 x = 0.5 掉到 8.9e-16，
  同一個 n 在 x = 0.99 還有 0.605，所以上確界不掉。一除以 x 與 sin 一除以 x：
  **後者才是有意思的那個**，程式挑出成對的點 x − y = 0.00008 而函數值始終差 2.0，
  所以它連續、有界，仍然不均勻連續——**缺的不是有界，是緊緻**。
- **帳篷函數驗過「緊緻救不了收斂」**：底邊一除以 n 到二除以 n，程式驗到每一個的上確界都是 1.000，
  而在固定的 x = 0.7 上，n = 2 是 0.800、n = 6 與 n = 20 都是 0.000。
  定義域是閉區間零到一，緊緻；逐點收斂到零；一致範數下的距離卻不掉。
- **書上那族尖峰是兩兩驗過的**：第 n 個的底邊是 1/(2n+2) 到 1/(2n)，尖點在 1/(2n+1)。
  取樣時**要把尖點本身加進取樣集**，否則均勻格點會報出一個略小於 1 的上確界。
  程式驗過四個尖峰兩兩不重疊、每個高度都是 1，所以任兩個的一致距離都是 1。
- **Lebesgue 數是真的算出來的**：對覆蓋 (0, 0.6) 與 (0.4, 1)，r = 0.09 在 2001 個取樣點上都成立，
  r = 0.11 在中點就失敗——這正是引理 5.3 要的那個常數。
- **r 稠密那張圖也驗過**：7 個等分點在整個區間上是 1/8 稠密的。

probe 幀抓到兩處工具看不到的錯（bounds、collide、langscan 都是 0）：
beat 1 的註腳寫成「三條彩色的曲線貼近**黑色**那條」，可是極限那條是用 `ACCENT_A` 畫的橘色，
畫面上根本沒有黑色的曲線；beat 6 把 `ACCENT_B`（青綠）的圓說成「**藍色**那個圓」。
兩處都是「文字說的顏色跟畫出來的顏色不一樣」，兩個語言版本一起錯。

---

## Beat 0 — 「均勻」就是把量詞反過來 / uniform means reversing quantifiers
*配音長度：中文 21.0s ／ 英文 18.5s*

**畫面公式**

```
「均勻」就是把量詞反過來   |   uniform means reversing quantifiers
( ∀ y ∈ A ) ( ∀ c ) ( ∃ d )  Q          ( ∀ c ) ( ∃ d ) ( ∀ y ∈ A )  Q
```

**旁白（繁中）**

> 第 5 節講「均勻」這個詞。粗略地說，它針對的是一個逐點的性質：對每個 y，存在一個 d 使得某件事成立。而那個 d 一般同時依賴 y 與 c。均勻的意思就是把量詞的順序反過來——d 可以取得跟 y 無關。

**Narration (EN)**

> Section 5 is about the word uniform. Roughly, it concerns a pointwise property: for each y there is a d making something hold, and that d generally depends on both y and c. Uniform means reversing the order of the quantifiers, so that d can be chosen independently of y.

**動畫**

左邊上下兩個框，上面是逐點的量詞順序（灰），下面是均勻的（紅），中間一支向下的箭頭。
右側三行說明：上面那一行讓 d 隨 y 變、下面那一行要一個 d 對所有 y 都行、差別只在順序。

## Beat 1 — 逐點收斂與均勻收斂 / pointwise and uniform convergence
*配音長度：中文 16.6s ／ 英文 17.8s*

**畫面公式**

```
逐點收斂與均勻收斂   |   pointwise and uniform convergence
n > N        ⇒        ρ ( f ₙ ( p ) , f ( p ) )  ≤  ϵ            ∀ p ∈ A
```

**旁白（繁中）**

> 均勻連續就是這樣來的：δ 只依賴 ε，不依賴那個「主張連續的點」。同樣的模式也用在函數序列上：逐點收斂是每個點各有各的 N，均勻收斂是有一個 N 對所有點都行。

**Narration (EN)**

> Uniform continuity is exactly that: delta depends on epsilon alone and not on the point at which continuity is asserted. The same pattern applies to sequences of functions: pointwise convergence gives each point its own N, uniform convergence one N for all of them.

**動畫**

左邊一個極限函數（橘）與三條逐漸貼近它的曲線（青、紫、紅），
每一條都在原函數上加一個越來越小、但仍然全域起伏的擾動——貼近的方式才是重點。

## Beat 2 — 逐點推不出均勻 / pointwise does not give uniform
*配音長度：中文 18.1s ／ 英文 17.6s*

**畫面公式**

```
逐點推不出均勻   |   pointwise does not give uniform
‖ f ₙ  −  f ‖ ∞    →    0                    f ₙ ( x )   =   x ⁿ
```

**旁白（繁中）**

> 均勻收斂等價於一致範數下的距離掉到零——這就是那個上確界範數叫一致範數的原因。而逐點收斂推不出均勻收斂：x 的 n 次方在開區間零到一上逐點收斂到零，可是上確界永遠是一。

**Narration (EN)**

> Uniform convergence is the same as the distance in the uniform norm falling to zero, which is why that least upper bound norm carries the name. And pointwise does not give uniform: x to the n on the open unit interval tends to zero pointwise while its supremum stays at one.

**動畫**

左邊三條 x 的 n 次方（n = 2、10、50），上緣一條虛線標出高度一；
右側一張三列的表：同一個 n 在 x = 0.5 與 x = 0.99 的值差了十幾個數量級。

## Beat 3 — 連續、有界，仍然不均勻 / continuous, bounded, still not uniform
*配音長度：中文 17.0s ／ 英文 17.9s*

**畫面公式**

```
連續、有界，仍然不均勻   |   continuous, bounded, still not uniform
f ( x )  =  1 / x   ,    sin ( 1 / x )                    ( 0 , 1 )
```

**旁白（繁中）**

> 連續也推不出均勻連續。一除以 x 在開區間上連續，可是不均勻；更有意思的是 sin 一除以 x——它連續而且有界，一樣不均勻連續。緊緻性會改變後面這件事。

**Narration (EN)**

> Continuity does not give uniform continuity either. One over x is continuous on that interval but not uniformly so; more interestingly, the sine of one over x is continuous and bounded and still not uniformly continuous. Compactness changes the second of those.

**動畫**

左邊 sin 一除以 x 的曲線（紫，取樣 3000 點），上下兩條紅色虛線標出 ±1 的界；
右側的表列出三組越靠越近的點對（相距 0.01286 → 0.00008），函數值卻始終差 2.0。

## Beat 4 — 定理 5.1：緊緻就補得起來 / Theorem 5.1: compactness repairs it
*配音長度：中文 20.4s ／ 英文 19.4s*

**畫面公式**

```
定理 5.1：緊緻就補得起來   |   Theorem 5.1: compactness repairs it
ρ ( x ₙ , y ₙ ) < 1 / n              ρ ( f ( x ₙ ) , f ( y ₙ ) )  ≥  ϵ
```

**旁白（繁中）**

> 定理 5.1：緊緻集上的連續函數一定均勻連續。證明又是那套自動的否定法：否定均勻連續得到一個 ε 與兩列點，距離小於一除以 n 而像的距離不小於 ε；緊緻性抽出收斂子序列，連續性就逼出矛盾。

**Narration (EN)**

> Theorem 5.1: a continuous function on a compact set is uniformly continuous. The proof is that automatic negation again: denying uniformity gives two sequences at distance under one over n whose images stay apart, and compactness with continuity forces a contradiction.

**動畫**

左邊把證明排成四列：否定的量詞式（青）、令 δ 等於一除以 n（紫）、
兩支子序列收到同一點（紅），最後一列框起來的是矛盾（橘）。右側三行對應三個步驟。

## Beat 5 — 可是收斂補不起來 / but it does not repair convergence
*配音長度：中文 19.3s ／ 英文 17.9s*

**畫面公式**

```
可是收斂補不起來   |   but it does not repair convergence
‖ f ₙ ‖ ∞  =  1                  f ₙ ( p )   →   0              ∀ p
```

**旁白（繁中）**

> 可是緊緻性不會自動把逐點收斂變成均勻收斂。書上畫了一族帳篷函數：底邊從一除以 n 到二除以 n，高度是一。定義域零到一是緊緻的，函數逐點收斂到零，可是每一個的上確界都是一。

**Narration (EN)**

> But compactness does not turn pointwise convergence into uniform convergence. The book draws a family of tent functions with base from one over n to two over n and height one. The domain is compact and the functions tend to zero pointwise, yet every supremum is one.

**動畫**

左邊三個帳篷（n = 2、6、20）越來越窄、越來越靠左，高度都頂到那條虛線；
x 軸下面一條粗橘線標出緊緻的定義域。右側的表：上確界都是 1.000，而 f(0.7) 掉到 0.000。

## Beat 6 — 定理 5.2：距離變成正的 / Theorem 5.2: the distance turns positive
*配音長度：中文 15.4s ／ 英文 16.1s*

**畫面公式**

```
定理 5.2：距離變成正的   |   Theorem 5.2: the distance turns positive
A  ∩  C  =  ∅              ⇒              ρ ( A , C )    >    0
```

**旁白（繁中）**

> 定理 5.2：兩個不相交的非空閉集，只要有一個是緊緻的，距離就一定是正的。上一集看過兩個不相交的閉集距離為零的例子——差別就在那裡兩個都不緊緻。

**Narration (EN)**

> Theorem 5.2: two disjoint nonempty closed sets, one of them compact, are a positive distance apart. The last episode showed disjoint closed sets at distance zero, and the difference is exactly that neither of those was compact.

**動畫**

左邊一個青色的圓（緊緻）與上方一條紅色的直線（閉），中間一支箭頭標著距離 1，
這個 1 是程式在 720 個圓周取樣點上算出來的最小距離。

## Beat 7 — r 稠密與全有界 / r-dense, and totally bounded
*配音長度：中文 18.5s ／ 英文 18.1s*

**畫面公式**

```
r 稠密與全有界   |   r-dense, and totally bounded
B ᵣ [ A ]  =  ∪ { B ᵣ ( a ) : a ∈ A }                S   ⊂   B ᵣ [ A ]
```

**旁白（繁中）**

> 接下來一組定義。r 稠密是說每一點都離某個 a 不到 r；稠密就是閉包等於全空間；而全有界是說：對每個正的 r，都找得到一個有限集是 r 稠密的——換句話說，有限多個半徑 r 的球就蓋得住。

**Narration (EN)**

> Then some definitions. A set is r-dense if every point is within r of one of its members; dense means the closure is everything; and totally bounded means that for every positive r some finite set is r-dense, that is, finitely many balls of radius r cover it.

**動畫**

左邊一條線段上七個等分的紅點，每個點外面畫一個半徑 1/8 的紫圈，圈與圈交疊著蓋滿整條線段。

## Beat 8 — 無窮維的單位球蓋不住 / the infinite-dimensional ball resists
*配音長度：中文 20.2s ／ 英文 19.1s*

**畫面公式**

```
無窮維的單位球蓋不住   |   the infinite-dimensional ball resists
‖ f ₙ  −  f ₘ ‖ ∞    =    1                    n   ≠   m
```

**旁白（繁中）**

> 全有界比有界強得多。引理 5.1：無窮維賦範空間的閉單位球蓋不住——用有限多個半徑三分之一的球辦不到。書上給了具體的例子：連續函數空間裡一族互不重疊的尖峰函數，兩兩的一致距離都是一。

**Narration (EN)**

> Total boundedness is much stronger. Lemma 5.1: the closed unit ball of an infinite-dimensional normed space cannot be covered by finitely many balls of radius one third. The book's concrete example is a family of non-overlapping peaks whose uniform distances are all one.

**動畫**

左邊四個互不重疊的尖峰（n = 1、2、3、5），底邊 1/(2n+2) 到 1/(2n)，高度都頂到那條虛線；
越靠近零的尖峰越窄，所以無窮多個塞得下——這正是「有界卻不全有界」的圖像。

## Beat 9 — 有限維的分界線 / where finite dimensions end
*配音長度：中文 19.0s ／ 英文 19.1s*

**畫面公式**

```
有限維的分界線   |   where finite dimensions end
dim V   <   ∞              ⇔              B ₁ ‾    ∈    𝒦
```

**旁白（繁中）**

> 引理 5.2 說序列緊緻的集合一定全有界。跟定理 4.4 合起來就得到一條漂亮的推論：一個賦範空間是有限維的，等價於它的閉單位球序列緊緻。無窮維與有限維的分界線就落在這裡。

**Narration (EN)**

> Lemma 5.2 says a sequentially compact set is totally bounded. With Theorem 4.4 that gives a beautiful corollary: a normed space is finite-dimensional exactly when its closed unit ball is sequentially compact. The line between finite and infinite dimensions falls right there.

**動畫**

左邊兩個框（「dim V 小於無窮」與「閉單位球緊緻」）中間一對反向的箭頭：
往右那支標定理 4.4，往左那支標這一節的引理 5.1 與 5.2——兩支合起來才是那個等價。

## Beat 10 — Lebesgue 數，兩種緊緻接起來 / a Lebesgue number joins the two
*配音長度：中文 21.4s ／ 英文 20.6s*

**畫面公式**

```
Lebesgue 數，兩種緊緻接起來   |   a Lebesgue number joins the two
∀ p ∈ A      ∃ j      B ᵣ ( p )    ⊂    E ⱼ
```

**旁白（繁中）**

> 最後兩條把兩種緊緻接起來。引理 5.3 給出一個 Lebesgue 數：開覆蓋之下有一個 r，使得每一點的 r 球都整個落在某一個開集裡。定理 5.3 與 5.4 因此說：在度量空間上，序列緊緻與有限子覆蓋是同一件事。

**Narration (EN)**

> Two results join the two notions. Lemma 5.3 produces a Lebesgue number: given an open covering there is an r such that every ball of that radius lies inside one of the sets. Theorems 5.3 and 5.4 then say that on a metric space, sequential compactness and finite subcovers agree.

**動畫**

最上面一條灰線是整個區間，底下兩條彩色線段（青、紫）是一個開覆蓋，兩者在中間重疊；
最下面紅色那一段是中點的 r 球（r = 0.09），它整個落在上面那一段裡——這就是 Lebesgue 數。
