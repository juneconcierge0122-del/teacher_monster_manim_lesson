# advcalc E58 — 第 4 章：序列緊緻性

Chapter 4: Sequential Compactness

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 4 節「序列緊緻性」（書頁 205–209，習題 4.1–4.16 在 209–210）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e58_compactness.py`（`AdvCalcE58ZH` / `AdvCalcE58EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[58]` / `FORMULAS_ADVCALC[58]`）
- 配音：`manim_lessons/samples/audio_e58/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.47 分（208 秒）／英文 3.42 分（205 秒）

## 「無中生有地造出收斂」

序列緊緻的定義是：裡面每一個序列都有子序列收斂到裡面的一點。書上的話很傳神——
這裡等於是無中生有地造出收斂。這一集的四個判斷是算出來的：

- **峰項是真的找出來的，而且避開了截斷的陷阱**。「x_n 是峰項」是關於整個無窮尾巴的敘述，
  所以程式拿前 40 項對著後面 800 項比。**如果只拿 40 項自己比，最後那一項會無條件變成峰項**，
  那是截斷造成的假峰，不是序列的性質。算出來是 3 個峰項，走「有限多個」那一支，
  之後挑出一支四項的嚴格遞增子序列（0.103 → 0.274 → 0.996 → 1.020）。
  **原來的序列根本沒有極限，可是這一支有**——這就是「無中生有」的意思。
- **緊緻這個假設不能省**：把 `[0, 2π)` 繞成圓。斷言兩個參數差了 6.283，
  可是它們的像只差 0.0002，所以反函數不連續。少了緊緻，定理 4.2 就是錯的。
- **定理 4.6 的兩個常數是掃出來的**：取一個刻意不對稱的範數，
  在一範數的單位球面上掃出最小值 0.3333 與最大值 3.0000，再在球面外四個點上驗那個夾擊。

這一節的定理 4.6 補上第 3 章欠的那個洞——第 4 節用了「有限維上所有範數等價」，
證明要等緊緻性才給得出來。

probe 幀與 bounds 抓到兩處：beats 7 與 8 的第一項將近 2.5，垂直尺度沒考慮到而跑出上緣；
beat 9 最下面那個方塊壓到註腳的第一行。

---

## Beat 0 — 子序列 / subsequences
*配音長度：中文 19.6s ／ 英文 18.6s*

**畫面公式**

```
子序列   |   subsequences
{ x ₙ ₍ ₘ ₎ }              n ( m + 1 )   >   n ( m )
```

**旁白（繁中）**

> 第 4 節講序列緊緻性。先把子序列說清楚：從一個序列裡挑出無窮多項，按原來的順序排好。正式一點就是接上一個嚴格遞增的指標函數。任何零一序列都是零一零一那個序列的子序列。

**Narration (EN)**

> Section 4 is about sequential compactness. First subsequences: pick infinitely many terms out of a sequence, keeping the order. Formally that is composing with a strictly increasing index function. Any sequence of zeros and ones is a subsequence of zero one zero one.

**動畫**

上下兩條數線：上面是原序列，紅色的是被挑中的項；下面是挑出來的子序列，中間用細箭頭連起來。

## Beat 1 — 引理 4.1：一條看起來很怪的話 / Lemma 4.1: an unlikely-sounding one
*配音長度：中文 19.0s ／ 英文 16.5s*

**畫面公式**

```
引理 4.1：一條看起來很怪的話   |   Lemma 4.1: an unlikely-sounding one
ρ ( x ₙ ₍ ᵢ ₎ , a )   ≥   ϵ                ∀ i
```

**旁白（繁中）**

> 有一個看起來很怪的引理。如果 x_n 不收斂到 a，就存在一個 ε，可以挑出一整支子序列，每一項都離 a 至少 ε 遠——而那一支的任何子序列也收斂不到 a。反過來寫就是引理 4.1。

**Narration (EN)**

> There is a lemma that sounds unlikely. If the terms do not converge to a, some epsilon lets one pick a whole subsequence every term of which is at least epsilon away, and no subsequence of that one converges to a either. Turned around, that is Lemma 4.1.

**動畫**

左邊一條數線，極限打橘點並用兩條虛線標出 ε 帶，帶外一串紅點。
右側說明那一支的任何子序列也收斂不到那一點。

## Beat 2 — 無中生有地造出收斂 / convergence out of nothing
*配音長度：中文 19.1s ／ 英文 18.8s*

**畫面公式**

```
無中生有地造出收斂   |   convergence out of nothing
∀ { x ₙ }  ⊂  A          ∃ { x ₙ ₍ ᵢ ₎ }  →  a   ∈   A
```

**旁白（繁中）**

> 定義：一個子集是序列緊緻的，如果它裡面每一個序列都有子序列收斂到它裡面的一點。書上的話很傳神：這裡等於是無中生有地造出收斂。ℝⁿ 的有界閉集都是，可是無窮維時就罕見得多。

**Narration (EN)**

> The definition: a subset is sequentially compact if every sequence in it has a subsequence converging to a point of it. The book puts it well: here we create convergence out of nothing. Bounded closed subsets of real n-space are compact, but in infinite dimensions this is far rarer.

**動畫**

左邊一團集合，裡面散落幾個點，其中三個各有一支箭頭指向同一個橘點。
右側是序列緊緻的定義。

## Beat 3 — 引理 4.2：又閉又有界 / Lemma 4.2: closed and bounded
*配音長度：中文 17.5s ／ 英文 18.5s*

**畫面公式**

```
引理 4.2：又閉又有界   |   Lemma 4.2: closed and bounded
A   ∈   𝒦            ⇒            A  =  Ā   ,    A   ⊂   B ᵣ ( b )
```

**旁白（繁中）**

> 引理 4.2：序列緊緻的集合一定又閉又有界。閉是因為收斂序列的極限被子序列抓回集合裡；有界是因為不然就可以挑出離某一點越來越遠的點，而它的收斂子序列會跟這件事矛盾。

**Narration (EN)**

> Lemma 4.2: a sequentially compact set is closed and bounded. Closed because a subsequence drags the limit of any convergent sequence back into the set; bounded because otherwise one could pick points ever further from a fixed one, and a convergent subsequence contradicts that.

**動畫**

左邊一個 A ∈ 𝒦 的方塊，兩支箭頭指向「閉」與「有界」兩個方塊。
右側是兩件事各自的理由。

## Beat 4 — 最大最小值取得到 / the extremes are attained
*配音長度：中文 21.3s ／ 英文 20.0s*

**畫面公式**

```
最大最小值取得到   |   the extremes are attained
A  ∈  𝒦  ,   f  ∈  C ⁰            ⇒            f [ A ]   ∈   𝒦
```

**旁白（繁中）**

> 定理 4.1 說連續映射把緊緻集送成緊緻集。而實數線上的緊緻集含著最大與最小元——上確界是集合裡某個序列的極限，而集合是閉的。合起來就是那條熟悉的推論：連續函數在緊緻定義域上取得到極值。

**Narration (EN)**

> Theorem 4.1 says continuous maps carry compact sets to compact ones. A nonempty compact subset of the line contains its largest element, the least upper bound being a limit of points of a closed set. Together: a continuous function on a compact domain attains its extremes.

**動畫**

左邊一條曲線，最高點與最低點各打一點並拉虛線到縱軸，橫軸下方畫一段粗線代表緊緻的定義域。

## Beat 5 — 定理 4.2：反函數也連續 / Theorem 4.2: the inverse is continuous
*配音長度：中文 18.1s ／ 英文 18.2s*

**畫面公式**

```
定理 4.2：反函數也連續   |   Theorem 4.2: the inverse is continuous
f  :  A  ↔  B  ,    f  ∈  C ⁰            ⇒            f ⁻¹  ∈  C ⁰
```

**旁白（繁中）**

> 定理 4.2：如果 f 連續、是雙射，而且定義域序列緊緻，那麼反函數也連續。證明正是用剛才那條怪引理：要證某個序列收斂，就證它的每一支子序列都有一支再收斂到同一點。

**Narration (EN)**

> Theorem 4.2: if f is continuous and bijective with sequentially compact domain, the inverse is continuous too. The proof is where that odd lemma earns its place: to prove a sequence converges, show every subsequence has a further one converging to the same point.

**動畫**

左邊三行式子（yₙ → y、子子序列收斂、極限只能是那一點），下面一個加框的結論。

## Beat 6 — 少了緊緻就不成立 / without compactness it fails
*配音長度：中文 17.9s ／ 英文 16.8s*

**畫面公式**

```
少了緊緻就不成立   |   without compactness it fails
[ 0 , 2 π )   →   S ¹                    f ⁻¹   ∉   C ⁰
```

**旁白（繁中）**

> 緊緻這個假設不能省。把區間零到二 π 那一段（不含右端）繞成一個圓，映射連續而且是雙射，可是反函數在一那一點不連續：圓上靠近一的點，原像有的靠近零、有的靠近二 π。

**Narration (EN)**

> Compactness cannot be dropped. Wrap the interval from zero to two pi, right end excluded, around a circle: the map is continuous and bijective, yet the inverse is not continuous at one, since points near it come from near zero and from near two pi.

**動畫**

左邊一條線段（右端畫空心圈）經箭頭繞成一個圓，圓上一點附近兩個不同顏色的點。
右側說明反函數在那一點不連續。

## Beat 7 — 峰項 / peak terms
*配音長度：中文 20.0s ／ 英文 20.1s*

**畫面公式**

```
峰項   |   peak terms
x ₙ  ≤  x ₙ ₊ ₁          l   =   lub  { x ₙ }
```

**旁白（繁中）**

> 接下來證 ℝⁿ 的有界閉集是緊緻的。先證實數線。引理 4.3：有界的單調序列收斂，用上確界。引理 4.4：任何實數列都有單調子序列，用「峰項」——大於等於它後面所有項的那些項。

**Narration (EN)**

> Now for bounded closed sets in real n-space. The line first. Lemma 4.3: a bounded monotone sequence converges, by least upper bound. Lemma 4.4: any real sequence has a monotone subsequence, via peak terms, the terms at least as large as everything after them.

**動畫**

左邊一串散點，其中幾個標成紅色並各拉一小段虛線——那些是峰項。
右側說明峰項只有有限多個。

## Beat 8 — 任何實數列都有單調子序列 / every real sequence has a monotone one
*配音長度：中文 19.6s ／ 英文 19.0s*

**畫面公式**

```
任何實數列都有單調子序列   |   every real sequence has a monotone one
x ₙ   ≥   x ₘ            ∀ m > n
```

**旁白（繁中）**

> 峰項有無窮多個的話，它們本身就是一支遞減的子序列；只有有限多個的話，最後一個之後每一項都還有更大的在後面，於是挑得出嚴格遞增的一支。合起來就是定理 4.3：有界實數列必有收斂子序列。

**Narration (EN)**

> Infinitely many peaks already form a decreasing subsequence; if only finitely many, then past the last one every term is topped by a later one, so a strictly increasing one can be built. Together that is Theorem 4.3: a bounded real sequence has a convergent subsequence.

**動畫**

同一串散點，最後一個峰項之後的記錄高點用藍線連成一支遞增的子序列，右邊列出它的四個值。

## Beat 9 — 推到 ℝⁿ / lifting it to n dimensions
*配音長度：中文 16.5s ／ 英文 19.7s*

**畫面公式**

```
推到 ℝⁿ   |   lifting it to n dimensions
ℝ ⁿ   =   ℝ ⁿ ⁻ ¹  ×  ℝ
```

**旁白（繁中）**

> 定理 4.4 用歸納推到 ℝⁿ：把它看成 n 減一維乘上 ℝ，先對前面那一塊用歸納假設取子序列，再對最後一個座標取一次。定理 4.5 隨即得到：ℝⁿ 的有界閉集是序列緊緻的。

**Narration (EN)**

> Theorem 4.4 lifts it to n dimensions by induction, viewing the space as one of dimension n minus one times the line, taking a subsequence for the first block and then for the last coordinate. Theorem 4.5 follows: bounded closed sets in real n-space are sequentially compact.

**動畫**

左邊一個加框的 ℝⁿ = ℝⁿ⁻¹ × ℝ，往下兩個方塊（兩個分量各自收斂）再指向整體收斂。

## Beat 10 — 定理 4.6：補上第 3 章的洞 / Theorem 4.6: the gap is filled
*配音長度：中文 19.4s ／ 英文 19.1s*

**畫面公式**

```
定理 4.6：補上第 3 章的洞   |   Theorem 4.6: the gap is filled
m ‖ x ‖ ₁      ≤      ‖ x ‖      ≤      a ‖ x ‖ ₁
```

**旁白（繁中）**

> 最後補上第 3 章欠的那個洞。定理 4.6：ℝⁿ 上所有範數等價。一個方向是三角不等式直接給的；另一個方向是把範數限制到一範數的單位球面上，那是緊緻集，所以最小值取得到而且不是零。

**Narration (EN)**

> Finally the gap left in chapter 3 gets filled. Theorem 4.6: all norms on real n-space are equivalent. One inequality falls out of the triangle inequality; the other restricts the norm to the unit sphere of the one-norm, which is compact, so a nonzero minimum is attained.

**動畫**

左邊一個菱形（一範數的單位球面），上面兩個點是掃出來的最小值與最大值。
右側是那個夾擊與兩個常數的值。

---

## 一個關於「有限窗口」的陷阱

峰項的定義是「大於等於它後面的每一項」——這是關於整個無窮尾巴的敘述。
第一版的程式拿 40 項自己比，結果最後一項無條件成了峰項，
而「最後一個峰項之後」就只剩一項，遞增子序列長度是 1，斷言直接掛掉。
真正的修法不是放寬斷言，而是**把測試的尾巴拉長**：拿前 40 項對著 800 項比。
這樣算出來的 3 個峰項才是序列的性質，不是視窗的性質。

## 補上第 3 章的洞

第 3 章第 4 節講等價範數時用了「有限維上所有範數等價」這個事實，
可是當時沒有工具證它——證明要用「一範數的單位球面是緊緻的」，而緊緻性要等到這一章。
定理 4.6 就是那個證明：一個方向是三角不等式直接給的，
另一個方向是把任意範數限制到那個球面上取最小值，而最小值不可能是零，因為球面不含原點。
