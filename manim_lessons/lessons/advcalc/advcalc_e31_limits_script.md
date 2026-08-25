# advcalc E31 — 第 3 章：微分學的起點與 ε-δ

Chapter 3: Where the Differential Calculus Starts, and Epsilon-Delta

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章的開場（書頁 116）與第 1 節（書頁 117–120）。書頁 120 起是習題 1.1–1.16。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e31_limits.py`（`AdvCalcE31ZH` / `AdvCalcE31EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[31]` / `FORMULAS_ADVCALC[31]`）
- 配音：`manim_lessons/samples/audio_e31/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.13 分（188 秒）／英文 3.12 分（187 秒）

## ε-δ 的圖是算出來的，不是示意圖

書上 Fig 3.1 畫的是一條抽象的遞增曲線。依 `docs/PLAYBOOK.md` 第 8 節重畫時，這裡改成一個具體的
例子：`f ( x ) = x ²` 在 `a = 1`。δ 由 `|x² − 1| = |x − 1| |x + 1|` 這條界算出來——把 `|x − 1|`
壓在 1/2 以內，`|x + 1|` 就在 5/2 以內，於是 `δ = min ( 1/2 , 2ε/5 )`——而且用 `Fraction` 保持精確。

場景檔接著在整個 δ 區間上取樣，斷言圖形真的沒有跑出 ε 帶，並且斷言這個 δ 不是隨便放寬的
（把它加倍就會超出）。所以 beat 7 那兩張「ε 縮成三分之一，δ 也縮成三分之一」的圖，是兩組算出來的
數字，不是兩個畫得像的方框。

另外 `bounds.py` 在這一集抓到一件事：`x ²` 的曲線在原本的取樣範圍會衝到畫面外（頂到 +2.50），
所以 `_axes31` 現在會照實際可用的高度把曲線裁掉。

---

## Beat 0 — 微分學：用線性映射逼近非線性映射 / the calculus: linear approximations to nonlinear mappings
*配音長度：中文 17.6s ／ 英文 16.7s*

**畫面公式**

```
微分學：用線性映射逼近非線性映射   |   the calculus: linear approximations to nonlinear mappings
Δ F ( ξ )   =   d F ( ξ )   +   𝒪 ( ξ )        d F  ∈  Hom ( V , W )
```

**旁白（繁中）**

> 第 3 章開始講微分學。它的主旨用一句話講得完：微分學是「用線性映射去逼近非線性映射」的理論。前兩章把線性映射弄清楚了，現在要的是「逼近」這個詞的精確意思。

**Narration (EN)**

> Chapter three begins the differential calculus, and its subject fits in one sentence: it is the theory of linear approximations to nonlinear mappings. The first two chapters settled what linear mappings are; what is needed now is a precise meaning for approximation.

**動畫**

左邊一條 f ( x ) = x² 的曲線與它在 ( 1 , 1 ) 的切線——切線的斜率是真的導數 2。右邊三行說明「非線性的東西在一點附近長得像線性的」，那個線性映射就是微分。

## Beat 1 — 所以要先會量長度 / so length has to be measured first
*配音長度：中文 16.2s ／ 英文 16.2s*

**畫面公式**

```
所以要先會量長度   |   so length has to be measured first
‖ · ‖ : V → ℝ        ‖ Δ F ( ξ ) − d F ( ξ ) ‖  /  ‖ ξ ‖   →   0
```

**旁白（繁中）**

> 所以這一章從長度開始。要說一個逼近好不好，得先能量誤差有多大；向量空間上量長度的東西叫範數。有了範數才能談切近，談完切近才能定義微分。

**Narration (EN)**

> So the chapter starts with length. To say an approximation is good you must be able to measure how large the error is, and the thing that measures length on a vector space is called a norm. Norms come first, then tangency, and only then can a differential be defined.

**動畫**

一條曲線與一條直線，中間一支箭頭量它們的落差，標著 ‖ · ‖。右邊三行：誤差是向量不是數、要說它小得先能量長度、量長度的東西叫範數。

## Beat 2 — 這一章的路線 / the route through this chapter
*配音長度：中文 16.4s ／ 英文 16.7s*

**畫面公式**

```
這一章的路線   |   the route through this chapter
‖ · ‖   →   lim   →   d F   →   [ ∂ f ᵢ / ∂ x ⱼ ]
```

**旁白（繁中）**

> 路線圖是這樣：範數、連續、無窮小、微分與它的計算規則，然後是方向導數與偏導數。在座標空間裡，微分就是一個偏導數排成的矩陣，叫 Jacobian 矩陣。

**Narration (EN)**

> The route is: norms, continuity, infinitesimals, the differential and the rules for computing it, then directional and partial derivatives. In a Cartesian space the differential is a matrix of partial derivatives, called the Jacobian matrix of the mapping.

**動畫**

六個方框串成一條路線：範數、連續（lim）、無窮小、微分、偏導數、Jacobian 矩陣，每個方框下面有中英名稱，箭頭一路串下去。

## Beat 3 — 章末的兩個大定理 / the two large theorems at the end
*配音長度：中文 14.7s ／ 英文 15.4s*

**畫面公式**

```
章末的兩個大定理   |   the two large theorems at the end
F ( x , y ) = 0        ⇒        y = f ( x )
```

**旁白（繁中）**

> 章末的兩個大定理是反函數定理與隱函數定理。它們比前面所有東西都深，因為要用到實數的一個特別性質——完備性，那要等到第 4 章才正式處理。

**Narration (EN)**

> The chapter ends with two large theorems, the inverse-mapping theorem and the implicit-function theorem. They run deeper than anything before them, because they use a special property of the real numbers called completeness, which chapter four takes up properly.

**動畫**

左右兩個方框：左邊是反函數定理的假設（微分可逆），右邊是隱函數定理的假設（G ( x , y ) = 0），各配兩行說明。中間一條分隔線。底下說明兩者都要用到完備性。

## Beat 4 — ε-δ 的定義 / the epsilon-delta definition
*配音長度：中文 17.8s ／ 英文 19.1s*

**畫面公式**

```
ε-δ 的定義   |   the epsilon-delta definition
0 < | x − a | < δ        ⇒        | f ( x ) − l | < ϵ
```

**旁白（繁中）**

> 第 1 節先回到實數上複習極限。定義是：f ( x ) 趨近 l，如果對每一個正的 ε 都存在一個正的 δ，使得 x 跟 a 的距離落在 0 與 δ 之間時，f ( x ) 跟 l 的距離就小於 ε。

**Narration (EN)**

> Section one goes back to the real line to review limits. The definition: f of x approaches l if for every positive epsilon there is a positive delta such that whenever the distance from x to a lies strictly between zero and delta, the distance from f of x to l is less than epsilon.

**動畫**

ε-δ 的圖：f ( x ) = x² 在 a = 1，橫軸上一條寬 2δ 的帶子、縱軸上一條寬 2ε 的帶子，交點是 ( a , l )。δ 是算出來的（ε = 3/10 給 δ = 3/25），並驗過整段圖形沒有跑出 ε 帶。

## Beat 5 — 為什麼要挖掉 x = a 那一點 / why the point x = a is left out
*配音長度：中文 14.2s ／ 英文 11.9s*

**畫面公式**

```
為什麼要挖掉 x = a 那一點   |   why the point x = a is left out
x  ≠  a        lim ₓ → ₐ  f ( x )  =  l
```

**旁白（繁中）**

> 注意 x 等於 a 那一點被排除在外。這不是龜毛：微積分裡的差商在那一點根本沒定義，我們關心的正是它在附近的行為，而不是在那一點的值。

**Narration (EN)**

> Note that x equal to a is excluded. That is not fussiness: the difference quotients of calculus are not defined at that very point, and their behaviour near it is exactly what we care about.

**動畫**

一條數線，a 那一點畫成空心圓，兩側各一段粗線代表 0 < | x − a | < δ 的兩半。

## Beat 6 — 三個量詞的順序不能動 / the order of the three quantifiers is fixed
*配音長度：中文 18.6s ／ 英文 17.4s*

**畫面公式**

```
三個量詞的順序不能動   |   the order of the three quantifiers is fixed
( ∀ ϵ > 0 ) ( ∃ δ > 0 ) ( ∀ x )        ≠        ( ∀ ϵ > 0 ) ( ∀ x ) ( ∃ δ > 0 )
```

**旁白（繁中）**

> 這個句子真正的開頭是三個量詞：對所有 ε、存在 δ、對所有 x。順序不能動。把「存在 δ」搬到「對所有 x」後面，意思就變成 δ 可以隨 x 改，那是完全不同的敘述。

**Narration (EN)**

> The sentence really begins with three quantifiers: for every epsilon, there exists a delta, for every x. The order cannot move. Put the existence of delta after the quantifier on x and delta is allowed to depend on x, which is a different statement altogether.

**動畫**

上下兩排量詞方框：上排是正確的順序（∀ε、∃δ、∀x）打勾，下排是把 ∃δ 搬到 ∀x 後面打叉，各配一行說明它們的差別。

## Beat 7 — ε 變窄，δ 跟著窄 / narrower epsilon, narrower delta
*配音長度：中文 15.7s ／ 英文 17.9s*

**畫面公式**

```
ε 變窄，δ 跟著窄   |   narrower epsilon, narrower delta
ϵ  ↓        ⇒        δ  ↓
```

**旁白（繁中）**

> 圖上看很單純：在縱軸上取一條寬 2ε 的帶子，定義說得出橫軸上一條寬 2δ 的帶子，使得這一段的圖形整個落在那條橫帶裡。ε 越窄，δ 通常也得跟著窄。

**Narration (EN)**

> The picture is simple: take a band of width two epsilon about l on the vertical axis, and the definition says you can name a band of width two delta about a on the horizontal one, so that the graph over it lands inside the first band. Narrower epsilon usually forces narrower delta.

**動畫**

兩張同樣的 ε-δ 圖並排，左邊 ε = 3/10、δ = 3/25，右邊 ε = 1/10、δ = 1/25。兩個 δ 都是同一條公式算出來的，圖也是照著畫的。

## Beat 8 — 用法一：兩個一半 / first use: two halves
*配音長度：中文 19.5s ／ 英文 19.0s*

**畫面公式**

```
用法一：兩個一半   |   first use: two halves
| h − w |   ≤   | f − u |  +  | g − v |   <   ϵ / 2  +  ϵ / 2
```

**旁白（繁中）**

> 第一個用法：兩個函數相加。h 減 w 拆成兩塊，每一塊都小於 ε 的一半，加起來就小於 ε。兩個 δ 取小的那一個，兩邊的不等式就同時成立。這就是引理 1.1 的全部內容。

**Narration (EN)**

> The first use: adding two functions. Split h minus w into two pieces, make each smaller than half of epsilon, and their sum is smaller than epsilon. Take the smaller of the two deltas and both inequalities hold at once. That is the whole content of Lemma 1.1.

**動畫**

一條長棒分成首尾相接、各正好一半的兩段（| f − u | 與 | g − v |），每段標著 < ε / 2；底下一條整條的棒標著 | h − w | < ε。兩段真的加起來等於整條——圖本身就是那個論證。

## Beat 9 — 用法二：先把分母壓住 / second use: pin the denominator first
*配音長度：中文 18.4s ／ 英文 19.6s*

**畫面公式**

```
用法二：先把分母壓住   |   second use: pin the denominator first
h − w   =   ( u − f ) / ( f u )        | f |  >  | u | / 2
```

**旁白（繁中）**

> 第二個用法比較有意思：倒數。h 減 w 的分母裡有會動的 f ( x )，如果它太靠近零，分數就炸開。解法是先用一個 δ 把 f 逼在 u 的一半以外，分母就有了下界，再來估就穩了。

**Narration (EN)**

> The second use is more interesting: reciprocals. The denominator of h minus w contains f of x, which moves, and if it gets near zero the fraction blows up. The fix is to spend one delta keeping f away from zero, which bounds the denominator below and makes the estimate safe.

**動畫**

上方兩行寫出 h = 1 / f、w = 1 / u 與 h − w 的分式。底下一條數線標出 0、u 與 | u | / 2，一條粗線標出「f 被逼到這一側」的範圍，分母因此有了下界。

## Beat 10 — 最小上界性質 / the least upper bound property
*配音長度：中文 18.7s ／ 英文 17.5s*

**畫面公式**

```
最小上界性質   |   the least upper bound property
A ⊂ ( − ∞ , a )        ⇒        ∃ ! b  =  lub A        √ 2  =  lub { x : x ² < 2 }
```

**旁白（繁中）**

> 最後是實數的最小上界性質：一個非空、有上界的集合，一定有一個最小的上界。它看起來平凡，卻是後面所有事情的地基——像根號二就是「平方小於二的有理數」這個集合的最小上界。

**Narration (EN)**

> Last, the least upper bound property: a nonempty set of reals with an upper bound has a smallest one. It looks unremarkable and it is the foundation of everything that follows. The square root of two is the least upper bound of the rationals whose square is under two.

**動畫**

一條數線上一段粗線是集合 A，右端一個高亮的點是最小上界，再右邊兩個暗點是其他上界。底下兩行是四個具體例子（開區間、閉區間、1/n 的最小下界、平方小於二的有理數）。
