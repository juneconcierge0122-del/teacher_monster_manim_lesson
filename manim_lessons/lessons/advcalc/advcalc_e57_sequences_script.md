# advcalc E57 — 第 4 章：拓撲與序列收斂

Chapter 4: Topology and Sequential Convergence

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 2 節「拓撲」與第 3 節「序列收斂」（書頁 201–204，習題 3.1–3.15 在 204–205）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e57_sequences.py`（`AdvCalcE57ZH` / `AdvCalcE57EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[57]` / `FORMULAS_ADVCALC[57]`）
- 配音：`manim_lessons/samples/audio_e57/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.31 分（199 秒）／英文 3.29 分（197 秒）

## 兩節併一集：一節太短，一節是後面的工具

第 2 節只有一頁多：把開集族的三條性質抽出來當公理，然後分辨哪些概念是純拓撲的、
哪些要用到距離。有點意外的結論是——連續雖然是用度量定義的，它其實是拓撲的。

第 3 節才是後面真正會用的：序列收斂。這一集的三個判斷是算出來的：

- **定理 3.3 兩個方向都驗**：平面上三個標準範數互相夾住，比值正好介於 1 與 2 之間，
  所以它們兩兩等價；而一個「高度不動、面積掉到零」的尖峰序列在一個範數下收斂、
  在另一個下不收斂，所以那兩個範數不等價。
- **定理 3.2 的反例**：`xy/(x²+y²)`。斷言沿兩個座標軸走函數恆等於零，
  沿對角線走恆等於二分之一，而原點的值是零——所以它在原點不連續，
  儘管每個變數各自都連續。
- **反方向的證法**：那條對角線上的點就是證明會造出來的序列。
  斷言距離掉到零（0.0141）而像停在 0.5，兩件事同時成立。

probe 幀與 bounds 抓到五處：兩處圖形超出左緣、beat 4 的 ε 圓穿過項的標籤、
beat 8 第一個對角點跑出上緣（它在 (1,1)，尺度沒有考慮到）、beat 10 的表格多一列撞到方塊。

---

## Beat 0 — 把開集族抽出來當公理 / the open sets, taken as axioms
*配音長度：中文 18.8s ／ 英文 18.4s*

**畫面公式**

```
把開集族抽出來當公理   |   the open sets, taken as axioms
∪ ᵢ A ᵢ  ∈  𝒯            A ∩ B  ∈  𝒯            ∅ ,  X  ∈  𝒯
```

**旁白（繁中）**

> 第 2 節很短。把定理 1.1 那三條性質抽出來當公理：X 是任意集合，𝒯 是滿足那三條的一族子集，就叫一個拓撲。度量空間的開集族因此是拓撲，而研究這件事的後果就叫一般拓撲學。

**Narration (EN)**

> Section 2 is short. Take the three properties of Theorem 1.1 as axioms: X any set and a family of subsets satisfying them is called a topology on X. The open sets of a metric space therefore form one, and studying the consequences is general topology.

**動畫**

左邊一個灰框，裡面四個大小不一的圓，下面標一個 𝒯。
右側三行是拓撲的定義。

## Beat 1 — 哪些是拓撲的，哪些是度量的 / which notions are which
*配音長度：中文 18.6s ／ 英文 18.3s*

**畫面公式**

```
哪些是拓撲的，哪些是度量的   |   which notions are which
A ⁱⁿᵗ ,  Ā ,  ∂ A    :    𝒯                B ᵣ ( p ) ,  ϵ – δ    :    ρ
```

**旁白（繁中）**

> 接下來要分辨哪些概念是純拓撲的。內部、閉集、閉包，還有定理 1.2 與那條互補的恆等式，都只用到 𝒯，所以是拓撲的。可是球與 ε-δ 的連續是度量的定義，只有度量空間才有。

**Narration (EN)**

> Next, which notions are purely topological. Interior, closed set and closure, together with Theorem 1.2 and the complementary identity, use only the family of open sets and so are topological. Balls and the epsilon-delta definition of continuity are metric.

**動畫**

左邊兩欄方塊：左欄是內部、閉包、邊界，右欄是球與 ε-δ，各自下方標「只用到 𝒯」與「要用到 ρ」。

## Beat 2 — 連續其實是拓撲的 / continuity turns out topological
*配音長度：中文 18.7s ／ 英文 16.8s*

**畫面公式**

```
連續其實是拓撲的   |   continuity turns out topological
f ( p ) ∈ A ∈ 𝒯        ⇒        ∃ B ∈ 𝒯 ,   p ∈ B ,   f [ B ] ⊂ A
```

**旁白（繁中）**

> 有點意外的是：雖然連續是用度量定義的，它其實有純拓撲的刻畫。只要記得「開集就是球的聯集」就看得出來：f 在 p 連續，等價於含 f(p) 的每個開集，都有一個含 p 的開集被送進去。

**Narration (EN)**

> It comes as a surprise that although continuity was defined metrically it has a purely topological characterisation. Remembering that an open set is a union of balls makes it visible: every open set about the image must swallow the image of some open set about p.

**動畫**

左邊兩團集合，各自裡面一個圓，中間一支箭頭；框下標 B 與 A。
右側說明含著像的每個開集都吞得下某個含 p 的開集的像。

## Beat 3 — 鄰域的講法，以及全域的版本 / neighborhoods, and the global form
*配音長度：中文 18.8s ／ 英文 18.9s*

**畫面公式**

```
鄰域的講法，以及全域的版本   |   neighborhoods, and the global form
f  ⁻¹ [ A ]   ∈   𝒯            ⇔            f   ∈   C ⁰
```

**旁白（繁中）**

> 用鄰域講更順：A 是 p 的鄰域，如果 p 落在 A 的內部。那麼 f 在 p 連續，等價於 f(p) 的每個鄰域的逆像都是 p 的鄰域。全域的版本更漂亮：f 連續，等價於開集的逆像都是開的。

**Narration (EN)**

> Neighborhoods say it more fluently: A is a neighborhood of p if p lies in its interior. Then f is continuous at p exactly when the inverse image of every neighborhood of the value is one of p. Globally: f is continuous exactly when inverse images of open sets are open.

**動畫**

左邊兩個方塊（鄰域 → 逆像也是鄰域）與一個加框的全域版本。
右側說明局部用鄰域講最順。

## Beat 4 — 序列收斂：三個量詞 / convergence: three quantifiers
*配音長度：中文 19.4s ／ 英文 18.2s*

**畫面公式**

```
序列收斂：三個量詞   |   convergence: three quantifiers
( ∀ ϵ ) ( ∃ N ) ( ∀ n > N )            ρ ( x ₙ , a )    <    ϵ
```

**旁白（繁中）**

> 第 3 節加進序列收斂。定義是三個量詞：給了 ε，存在 N，使得 n 大於 N 時距離小於 ε。書上提供一個比較順口的講法：說一件事對「幾乎所有 n」成立，意思是只有有限多個 n 不成立。

**Narration (EN)**

> Section 3 adds sequential convergence. The definition has three quantifiers: given epsilon there is an N beyond which the distance is below epsilon. The book offers a more idiomatic phrasing: a statement holds for almost all n if it fails for only finitely many.

**動畫**

左邊一條數線，上面一串點往右邊的極限靠攏，極限外面套一個小圓。
右側是三個量詞的定義與「幾乎所有 n」。

## Beat 5 — N 取 max，不是 δ 取 min / N is a maximum, not a minimum
*配音長度：中文 17.9s ／ 英文 18.7s*

**畫面公式**

```
N 取 max，不是 δ 取 min   |   N is a maximum, not a minimum
N   =   max { N ₁ , N ₂ }                    δ   =   min { δ ₁ , δ ₂ }
```

**旁白（繁中）**

> 於是收斂就等於「極限周圍每個球都含幾乎所有的項」。引理 3.1 與 3.2 把和與純量積搬過來，證明跟第 3 章幾乎一樣——唯一的差別是 N 取兩個的最大值，而不是 δ 取最小值。

**Narration (EN)**

> So convergence is that every ball about the limit contains almost all the terms. Lemmas 3.1 and 3.2 carry sums and scalar multiples across, and the proofs are nearly those of chapter 3 — the only change is taking N as a maximum instead of delta as a minimum.

**動畫**

左邊兩個加框的式子：序列取 N 的最大值、函數取 δ 的最小值，各自標明用在哪裡。
右側是引理 3.1 與 3.2。

## Beat 6 — 定理 3.1：閉包就是極限 / Theorem 3.1: closure by limits
*配音長度：中文 18.4s ／ 英文 17.9s*

**畫面公式**

```
定理 3.1：閉包就是極限   |   Theorem 3.1: closure by limits
x  ∈  Ā            ⇔            ∃ { x ₙ }  ⊂  A ,     x ₙ  →  x
```

**旁白（繁中）**

> 定理 3.1 是這一節最好用的一條：一點落在 A 的閉包裡，等價於 A 裡有一個序列收斂到它。往這個方向是引理 1.3；反過來是在半徑一除以 n 的球裡各挑一點，挑出來的序列就收斂到那一點。

**Narration (EN)**

> Theorem 3.1 is the most usable result here: a point lies in the closure of a set exactly when some sequence in the set converges to it. One direction is Lemma 1.3; the other picks a point from the ball of radius one over n, and those picks converge.

**動畫**

左邊一團集合，外面一點打紅點，那點周圍四個越來越小的圓，每個圓裡挑一個集合裡的點。
右側是定理 3.1。

## Beat 7 — 閉集：極限不准跑出去 / closed: no limit escapes
*配音長度：中文 15.9s ／ 英文 17.0s*

**畫面公式**

```
閉集：極限不准跑出去   |   closed: no limit escapes
A  =  Ā        ⇔        ( { x ₙ } ⊂ A ,  x ₙ → x    ⇒    x ∈ A )
```

**旁白（繁中）**

> 推出來的第二句更常用：一個集合是閉的，等價於裡面每個收斂序列的極限都還在裡面。開區間零到一就不是閉的——一除以 n 整個在裡面，可是極限零跑出去了。

**Narration (EN)**

> The second half is used even more: a set is closed exactly when every convergent sequence lying in it has its limit in it. The open interval from zero to one is not closed, since one over n lies entirely inside while the limit zero escapes.

**動畫**

左邊一條藍色的線段（開區間，兩端畫空心圈），上方一串點往左端靠攏並畫一支箭頭。
右側說明極限跑到外面，所以不是閉的。

## Beat 8 — 定理 3.2：連續的序列刻畫 / Theorem 3.2: continuity by sequences
*配音長度：中文 15.9s ／ 英文 17.4s*

**畫面公式**

```
定理 3.2：連續的序列刻畫   |   Theorem 3.2: continuity by sequences
x ₙ   →   a            ⇒            f ( x ₙ )    →    f ( a )
```

**旁白（繁中）**

> 定理 3.2 是連續的序列刻畫：f 在 a 連續，等價於每一個收斂到 a 的序列，像也收斂到 f 在 a 的值。這個刻畫實際用起來比 ε-δ 靈活得多，這一章之後會一直用它。

**Narration (EN)**

> Theorem 3.2 is the sequential characterisation of continuity: f is continuous at a exactly when every sequence converging to a has its image converging to the value there. In practice it is far more flexible than epsilon-delta, and the chapter leans on it.

**動畫**

左邊一個座標十字與一條紅色的對角線，線上三個點越來越靠近原點。
右側說明沿軸恆為零、沿對角線恆為二分之一。

## Beat 9 — 讓 δ 跑遍 1 / n / let delta run through one over n
*配音長度：中文 16.9s ／ 英文 15.3s*

**畫面公式**

```
讓 δ 跑遍 1 / n   |   let delta run through one over n
ρ ( x ₙ , a )  <  1 / n              ρ ( f ( x ₙ ) , f ( a ) )   ≥   ϵ
```

**旁白（繁中）**

> 反方向的證法值得記：要否定連續，先把量詞的否定寫清楚，然後讓 δ 跑遍一除以 n，每個 n 挑一個對應的點。書上說這幾乎是一套自動的證明程序，後面會反覆出現。

**Narration (EN)**

> The proof of the converse is worth remembering: to deny continuity, write the negation of the quantifiers out, then let delta run through one over n and pick a point for each n. The book says this almost amounts to an automatic proof procedure.

**動畫**

左邊三行量詞的否定與 δ := 1/n，右邊一張表：距離掉到零而像停在二分之一。

## Beat 10 — 等價範數＝同一批收斂序列 / equivalent norms, same sequences
*配音長度：中文 19.4s ／ 英文 20.4s*

**畫面公式**

```
等價範數＝同一批收斂序列   |   equivalent norms, same sequences
p   ≈   q              ⇔              C ( p )    =    C ( q )
```

**旁白（繁中）**

> 最後兩條：定理 3.3 說兩個範數等價，等價於它們給出完全同一批收斂序列。定理 3.4 說乘積範數就是那些「逐分量收斂等價於整體收斂」的範數。兩條都是定理 3.2 的直接應用。

**Narration (EN)**

> Two results close the section. Theorem 3.3: two norms are equivalent exactly when they yield the same collection of convergent sequences. Theorem 3.4: a product norm is any norm for which componentwise convergence is the same as convergence. Both apply Theorem 3.2.

**動畫**

左邊一張表（尖峰序列在兩個範數下的值）與一個加框的定理 3.3。
右側說明那兩個範數不等價。

---

## 為什麼把兩節併成一集

第 2 節只有一頁多，而且它做的事是「回頭整理」：把已經有的概念分成拓撲的與度量的。
單獨成一集會很空，可是丟掉又可惜——因為「連續其實是拓撲的」這件事，
正好說明為什麼第 3 節之後可以一直用序列而不必回到 ε-δ。所以兩節併成一集。

## 這一集最實用的一句話

定理 3.1 的第二半：一個集合是閉的，等價於裡面每個收斂序列的極限都還在裡面。
實際判斷「閉不閉」時用的就是它——找一個序列，看極限跑不跑掉。
開區間零到一不是閉的，因為一除以 n 整個在裡面而極限零跑出去了。
