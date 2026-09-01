# advcalc E60 — 第 4 章：等度連續與 Cauchy 序列

Chapter 4: Equicontinuity and Cauchy Sequences

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 6 節「等度連續」（書頁 215–216，**整節沒有習題**）與第 7 節「完備性」的前半（216–218，收在定理 7.4 與推論 2）。第 7 節的習題 7.1–7.21 在書頁 221–223，在這一集的範圍之後。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e60_completeness.py`（`AdvCalcE60ZH` / `AdvCalcE60EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[60]` / `FORMULAS_ADVCALC[60]`）
- 配音：`manim_lessons/samples/audio_e60/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.66 分（220 秒）／英文 3.35 分（201 秒）

## 同一個量詞把戲，第三次

這一集把「均勻」那個量詞把戲用到第三個地方。**均勻連續是「一個 δ 對很多點」，
等度連續是「一個 δ 對很多函數」，均勻等度連續是兩個一起。**
定理 6.1 說全有界從定義域與值域傳到那一族自己身上，證明是三個有限集拼出來的。
第 7 節換題目：項與項互相靠近的序列「應該」要收斂，什麼時候這個「應該」成立。

七拍的數字都是算出來的：

- **beat 0 那個共同的 δ 是驗過的**：四個成員 sin(kx)/k 各自在 δ 之內的擺動量都算出來，
  四個都小於 ε，所以「同一個 δ 對整族都行」不是畫上去的，是成立的。
- **beat 1 的楔形畫在真的導數界上**：三條曲線的 |f′| 逐點掃過，都不超過 m = 3；
  方框寬 δ = ε／m、高 ε，而斜率 ±m 的四條臂**剛好走到四個角**——
  這正是 δ = ε／m 的幾何意思，不是示意。
- **beat 3 的格子是數出來的**：四欄（#D = 4）三列（#E = 3），走法 3⁴ = 81 種。
  一條折線就是一個 D → E 的函數，「有限」這件事就是整個證明的支點。
- **beat 4 的三段驗過剛好收在 ε**：ε／4 + ε／2 + ε／4 = ε，一分不多一分不少。
- **beat 5 的 N 是搜出來的，不是湊的**：對 (−1)ⁿ／n 與 ε = 0.30，程式從 N = 1 往上找，
  第一個成立的是 **N = 6**（1／7 + 1／8 = 0.268 過得了，1／6 + 1／7 = 0.310 過不了）。
  **第一版寫 ε = 0.10 時搜出來的是 19，我原本猜 20** —— 搜尋才是準的。
- **beat 7 的兩列數字是同一批點**：1／20、1／40、1／80 彼此相距 0.038，
  它們在一除以 x 之下的像是 20、40、80，彼此相距 60。同一個序列，過去是 Cauchy，過來就不是。
- **beat 8 的每一項都是精確的分數**：用 `Fraction` 造 (1 + 1／n)ⁿ，
  得到 9／4、64／27、7776／3125 …，程式驗過每一項的分母都大於 1（真的是有理數）、
  數列遞增、都小於 e、而且尾巴三項彼此相距不到 0.10（所以真的是 Cauchy）。
  極限 e 不是有理數——**這就是「該收斂卻無處可去」**。

三道檢查（bounds / collide / langscan）都跑到 0，但 **probe 幀又抓到五處工具看不到的**：

1. **beat 8 整張圖是錯的**。原本把 1、1.4、1.41、1.414、1.4142 畫在數線上逼近 √2，
   可是後四項在螢幕上全落在同一個像素，看起來是「一個點停在一個圈上」，
   完全沒有「一步一步靠近」的樣子。改成把 (1 + 1／n)ⁿ 對 n 畫成折線圖，
   配一條 e 的漸近線與一個空心圈，才讀得出來。**收斂太快的例子畫不出收斂。**
2. **beat 1 的楔形沒有貼在任何一條曲線上**，浮在 x 軸中間，看起來像一段亂入的虛線。
   改成把方框與四條臂畫在中間那條曲線的一點上。
3. **beat 4 的分隔虛線畫成了刪除線**，正好穿過第三列 `ρ(h p, h p′) ≤ ε/4`。
4. **beat 2 的 r 球畫成了線上方的一排虛線**，讀起來像第二條線而不是「球蓋住這條線」；
   改成沿用 E59 beat 7 那種一串交疊的圓。**兩個語言的標籤本來放在線的上方，
   會壓到另一條線的球**，改成放在線的右側。
5. **beat 8 的 `(1 + 1/n)ⁿ` 標籤壓在漸近線上**，而漸近線又穿過那個空心圈，
   圈看起來像串在線上的珠子；標籤移到曲線下方，漸近線在圈之前就停住。

另外 **bounds 抓到兩處**（beat 3 的說明字與 beat 0 的引導虛線超過 y = 1.30 的上限），
以及 **beat 2 的標籤重排後再抓到一次**。

## 這一輪改了兩件工具與稿子的事

- **英文旁白十一句有七句超過四行**（最長 342 字元），照 STATUS 的規矩在產配音之前
  就用 `len(textwrap.wrap(s, 72)) <= 4` 掃出來、逐句改短，改完最長 278 字元。
- **`langscan.py` 的白名單加了專有名詞**：`Cauchy`、`Banach`、`Lipschitz`、`Lebesgue`、
  `Hausdorff`。這些字在中文旁白裡本來就原樣寫（「Cauchy 序列」「Banach 空間」），
  跟 `sin`、`det` 一樣是兩個語言共用的寫法，不是「某一半觀眾會看到外語」的那種漏。
  真正的漏（`全有界`、`diam`、`complete`）則改寫成純符號。

---

## Beat 0 — 等度連續：一個 δ 對整族 / equicontinuity: one delta for the family
*配音長度：中文 23.0s ／ 英文 19.1s*

**畫面公式**

```
等度連續：一個 δ 對整族   |   equicontinuity: one delta for the family
( ∀ ϵ ) ( ∃ δ ) ( ∀ f ∈ 𝔉 )        ρ ( p , p ₀ ) < δ  ⇒  ρ ( f p , f p ₀ ) < ϵ
```

**旁白（繁中）**

> 第 6 節很短，講等度連續。一族函數在某一點等度連續，意思是：它們每一個都在那點連續，而且給了 ε 之後，有一個 δ 對整族都行。注意這是「一個 δ 對很多函數」，跟均勻連續的「一個 δ 對很多點」是不同方向的統一。

**Narration (EN)**

> Section 6 is short and introduces equicontinuity. A family is equicontinuous at a point if each member is continuous there and one delta serves them all. Note the direction: one delta for many functions, where uniform continuity was one delta for many points.

**動畫**

四條曲線（sin kx／k，k = 1、2、3、5）各自帶一個框，框畫在同一個橫座標 p₀ 上。
**四個框寬度一模一樣**——那個共同的寬度就是 δ；高度是各自的 ε。

## Beat 1 — 均勻等度連續與均值定理 / uniform equicontinuity, via the mean value theorem
*配音長度：中文 17.4s ／ 英文 18.6s*

**畫面公式**

```
均勻等度連續與均值定理   |   uniform equicontinuity, via the mean value theorem
| f ′ |  ≤  m            ⇒            δ   =   ϵ / m
```

**旁白（繁中）**

> 如果那個 δ 連位置也不依賴，就叫均勻等度連續。書上給的例子很乾淨：一族導數的絕對值都不超過 m 的函數，由均值定理，δ 取 ε 除以 m 就對整族、對所有位置都成立。

**Narration (EN)**

> If that delta is independent of the point as well, the family is uniformly equicontinuous. The book's example is clean: a family whose derivatives are bounded by m, where the mean value theorem makes delta equal to epsilon over m work for every member at every point.

**動畫**

三條 |f′| ≤ 3 的曲線；中間那條上取一點，畫一個寬 δ、高 ε 的方框，
再從中心畫四條斜率 ±m 的臂——**四條臂剛好落在四個角上**，這就是 δ = ε／m。
右側的表列出 m = 1、3、10 各自對應的 δ。

## Beat 2 — 定理 6.1：全有界傳得下去 / Theorem 6.1: total boundedness passes on
*配音長度：中文 16.4s ／ 英文 16.7s*

**畫面公式**

```
定理 6.1：全有界傳得下去   |   Theorem 6.1: total boundedness passes on
∀ r > 0        ∃ F ⊂ A  ,  | F | < ∞        A   ⊂   B ᵣ [ F ]
```

**旁白（繁中）**

> 定理 6.1：定義域與值域都全有界，而且那一族是均勻等度連續的，那麼那一族在一致度量下也是全有界的。也就是說，有限多個一致範數的球就蓋得住整族函數。

**Narration (EN)**

> Theorem 6.1: if the domain and range are totally bounded and the family is uniformly equicontinuous, then the family is totally bounded in the uniform metric. That is, finitely many balls in the uniform norm cover the whole family of functions.

**動畫**

上下兩條線：上面是定義域 A（五個點、五個交疊的球），下面是值域 B（四個點、四個球）。
兩條線各自被自己那組球蓋滿，這就是兩邊全有界的意思。

## Beat 3 — 證明的骨架：三個有限集 / the proof rests on three finite sets
*配音長度：中文 17.6s ／ 英文 15.7s*

**畫面公式**

```
證明的骨架：三個有限集   |   the proof rests on three finite sets
D  ⊂  A   ( δ )              E  ⊂  B   ( ϵ / 4 )              G  =  E ᴰ
```

**旁白（繁中）**

> 證明的骨架是三個有限集：定義域裡取一個 δ 稠密的有限集 D，值域裡取一個 ε 除以四稠密的有限集 E，然後看所有從 D 到 E 的函數——那是一個有限的集合，元素個數是 E 的個數的 D 個數次方。

**Narration (EN)**

> The proof rests on three finite sets: a finite delta-dense subset of the domain, a finite quarter-epsilon-dense subset of the range, and then all functions from the first to the second, which is a finite collection of size the second raised to the first.

**動畫**

四欄三列的格子（D × E）。兩條彩色折線各自每欄挑一個點——
**一條折線就是一個 D → E 的函數**。右側數出 #D = 4、#E = 3、#G = 3⁴ = 81。

## Beat 4 — 四分之一 ε 拼成直徑 ε / quarters of epsilon make a diameter of epsilon
*配音長度：中文 23.2s ／ 英文 17.3s*

**畫面公式**

```
四分之一 ε 拼成直徑 ε   |   quarters of epsilon make a diameter of epsilon
𝔉 ᵍ  =  { f : ρ ( f p , g p ) < ϵ / 4 , p ∈ D }        ρ ( f , h )  ≤  ϵ
```

**旁白（繁中）**

> 每一個這樣的函數 g 收集那些「在 D 上跟它差不到 ε 除以四」的 f。要證的兩件事是：這些收集蓋住整族，而且每一個的直徑不超過 ε。書上在證完之後留了一句話——這個論證完全初等，可是很難；「精巧」與「困難」不是同一回事。

**Narration (EN)**

> Each such function collects the family members within a quarter epsilon of it on that finite set. Two things need proving: the collections cover the family, and each has diameter at most epsilon. The book calls the argument elementary and hard, and those are not the same thing.

**動畫**

三角不等式的三段疊成三列（ε／4、ε／2、ε／4），底下一條虛線，再一列合計 ≤ ε。

## Beat 5 — 第 7 節：Cauchy 序列 / Section 7: Cauchy sequences
*配音長度：中文 20.3s ／ 英文 18.8s*

**畫面公式**

```
第 7 節：Cauchy 序列   |   Section 7: Cauchy sequences
m , n  >  N            ⇒            ρ ( x ₘ , x ₙ )    <    ϵ
```

**旁白（繁中）**

> 第 7 節講完備性。如果一個序列收斂，它的項顯然會越靠越近；反過來，項越靠越近的序列「應該」要收斂。定義是這樣：對每個 ε 都有一個 N，使得兩個指標都大於 N 時距離小於 ε——這叫 Cauchy 序列。

**Narration (EN)**

> Section 7 is completeness. If a sequence converges its terms plainly get close to one another; conversely, terms that get close together ought to converge. The definition: for every epsilon there is an N beyond which any two terms are within epsilon. That is a Cauchy sequence.

**動畫**

(−1)ⁿ／n 對 n 畫成一排點；N = 6 之後的點是紅的，全部落在一條寬 ε 的帶子裡，
N 之前的灰點在帶子外面。那條垂直虛線標著 N = 6。

## Beat 6 — 引理 7.1 與 7.2 / Lemmas 7.1 and 7.2
*配音長度：中文 16.9s ／ 英文 17.0s*

**畫面公式**

```
引理 7.1 與 7.2   |   Lemmas 7.1 and 7.2
{ x ₙ }   →   a        ⇒        { x ₙ }   Cauchy
```

**旁白（繁中）**

> 引理 7.1：收斂的序列一定是 Cauchy 的，用三角不等式拆成兩半。引理 7.2 反過來補一半：Cauchy 序列只要有一支子序列收斂，整個就收斂。這條後面會一直用。

**Narration (EN)**

> Lemma 7.1: a convergent sequence is Cauchy, by splitting the triangle inequality in half. Lemma 7.2 supplies the other half: a Cauchy sequence with one convergent subsequence converges outright. That one gets used constantly later.

**動畫**

上面一條線：極限 a 與兩側的 xₘ、xₙ，底下寫 ε／2 + ε／2 = ε。
下面一條線：一串點，其中四個放大成紅色——那一支收斂，整個序列就跟著收斂。

## Beat 7 — Lipschitz 送得過去，連續不夠 / Lipschitz carries it over, continuity does not
*配音長度：中文 21.4s ／ 英文 19.8s*

**畫面公式**

```
Lipschitz 送得過去，連續不夠   |   Lipschitz carries it over, continuity does not
ρ ( T x , T y )  ≤  C ρ ( x , y )        ⇒        Cauchy  ↦  Cauchy
```

**旁白（繁中）**

> 引理 7.3：Lipschitz 映射把 Cauchy 序列送成 Cauchy 序列，有界線性映射是特例。定理 7.1 把它推廣到均勻連續。注意「連續」不夠：一除以 x 在半開區間上連續，可是它把一除以 n 這個 Cauchy 序列送成 n，那不是 Cauchy 的。

**Narration (EN)**

> Lemma 7.3: Lipschitz maps carry Cauchy sequences to Cauchy sequences, bounded linear maps being a special case, and Theorem 7.1 extends that to uniformly continuous ones. Continuity alone will not do: one over x sends one over n to n, which is not Cauchy.

**動畫**

上下兩條線：上面 1／20、1／40、1／80 擠在左端，下面它們的像 20、40、80 拉開，
三支箭頭把對應的點連起來（並且互相交叉）。右側的表列出兩排數字與兩邊的間距 0.038 對 60。

## Beat 8 — 完備，以及 Banach 空間 / complete, and Banach spaces
*配音長度：中文 20.7s ／ 英文 19.8s*

**畫面公式**

```
完備，以及 Banach 空間   |   complete, and Banach spaces
{ x ₙ }  Cauchy  ⊂  A         ⇒         ∃ a ∈ A  ,  x ₙ  →  a
```

**旁白（繁中）**

> 定義：一個度量空間完備，如果它裡面每個 Cauchy 序列都收斂到裡面的一點。完備的賦範空間叫 Banach 空間。定理 7.2 說實數線是完備的——證明是「Cauchy 序列有界，所以有收斂子序列」，再引用引理 7.2。

**Narration (EN)**

> The definition: a metric space is complete if every Cauchy sequence in it converges to a point of it. A complete normed space is a Banach space. Theorem 7.2 says the line is complete: a Cauchy sequence is bounded, so it has a convergent subsequence, and Lemma 7.2 finishes.

**動畫**

(1 + 1／n)ⁿ 對 n 的折線圖，一路往上逼近一條 e 的虛線；線的右端是一個**空心圈**，
標著 e ∉ ℚ。右側列出前幾項的精確分數 9／4、64／27、7776／3125。
每一項都是有理數，極限卻不是——這就是「該收斂卻無處可去」。

## Beat 9 — 定理 7.3：完備性搬得動 / Theorem 7.3: completeness travels
*配音長度：中文 19.9s ／ 英文 17.7s*

**畫面公式**

```
定理 7.3：完備性搬得動   |   Theorem 7.3: completeness travels
p  ≈  q        ⇒        ( ⟨ V , p ⟩  Banach    ⇔    ⟨ V , q ⟩  Banach )
```

**旁白（繁中）**

> 定理 7.3 說完備性搬得動：A 完備，f 連續雙射而且反函數 Lipschitz，那麼像也完備。特別地，可逆的有界線性映射把 Banach 空間送成 Banach 空間。推論是：等價的範數要嘛都完備，要嘛都不完備。

**Narration (EN)**

> Theorem 7.3 says completeness travels: if the domain is complete and the map is a continuous bijection whose inverse is Lipschitz, the image is complete too. So an invertible bounded linear map carries a Banach space to one, and equivalent norms go together.

**動畫**

兩個框（A 完備、B 完備）與一對反向的箭頭：往右標「f 連續、雙射」，
往左標「f ⁻¹ 是 Lipschitz 的」——兩個條件都要，才搬得動。

## Beat 10 — 有限維一定是 Banach 空間 / finite dimensions are always Banach
*配音長度：中文 22.2s ／ 英文 19.4s*

**畫面公式**

```
有限維一定是 Banach 空間   |   finite dimensions are always Banach
dim V  <  ∞            ⇒            V   Banach
```

**旁白（繁中）**

> 定理 7.4 說兩個 Banach 空間的乘積還是 Banach 空間，推廣到有限個乘積。第二個推論很要緊：每一個有限維向量空間，配上任何一個範數，都是 Banach 空間。理由是實數線完備、乘積保持完備、而有限維上所有範數等價。

**Narration (EN)**

> Theorem 7.4 says a product of two Banach spaces is one, and that extends to finite products. The second corollary matters: every finite-dimensional vector space, under any norm at all, is Banach. The line is complete, products preserve it, and all norms there agree.

**動畫**

四個框串成一條鏈：ℝ → ℝ × ℝ → ℝⁿ → dim V < ∞，
三支箭頭分別標定理 7.2、定理 7.4、推論 1；最後一步靠第 4 節的定理 4.6。
