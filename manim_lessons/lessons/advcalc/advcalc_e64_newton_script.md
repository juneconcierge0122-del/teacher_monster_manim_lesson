# advcalc E64 — 第 4 章：迭代法與 Newton 法

Chapter 4: The Iteration, and Newton's Method

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 9 節的後半（書頁 231–234）：定理 9.4、迭代程序、與 Newton 法的比較，以及書末那個平面上的例子。書頁 234–236 是習題 9.1–9.13，依 PLAYBOOK 第 8 節不做解答；第 10 節從書頁 236 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e64_newton.py`（`AdvCalcE64ZH` / `AdvCalcE64EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[64]` / `FORMULAS_ADVCALC[64]`）
- 配音：`manim_lessons/samples/audio_e64/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.09 分（185 秒）／英文 3.19 分（191 秒）

## 這一節其實在講一件很實際的事

E63 收的是不動點定理本身。這一集分成三段：

1. **定理 9.4**：把定理 9.2 再往上加一層——K 可微，隱含定義出來的 F 也可微。
   證明很短，因為材料都在：Lipschitz 條件就是 ‖dK²‖ 有界，令 G = η − K 之後
   dG² = I − dK²，**第 8 節那條幾何級數第二次回收**讓它可逆，再引第 3 章的定理 11.1。
2. **不動點定理其實是一個演算法**。書上用星號標了這一段，因為這是整節最容易被讀過去的一句話：
   存在性的證明說「反覆作用 K」，而那句話本身就是可以拿去跑的程式。
   Newton 法則是把那個固定的 T⁻¹ 換成每一步當地的 S_i⁻¹。
3. **書末的例子**：平面上最素的反映射，迭代出來的多項式正好在算反函數的 Taylor 展開。

## 書上有一個印刷錯誤，這裡沒有照抄

書頁 234 印的是

> u(x, y) = x − y² **−** 2yx³ + ⋯

**可是書上自己上面兩行的 u₃ = x − (y − x³)² 展開就是 x − y² + 2yx³ − x⁶**，符號是加。
同一頁的 v 那一行（y − x³ + 3x²y² + ⋯）則是對的。

數值也站在加號那邊。在 (x, y) = (0.10, 0.08)：

| | 值 | 與收斂值的差 |
|---|---|---|
| 迭代到收斂 | 0.0937311 | — |
| 加號版截斷式 | 0.0937600 | 2.9e-05（正好是下一階項 −6x²y³ 的大小） |
| 書上印的減號版 | 0.0934400 | 2.9e-04（差一個數量級，而且方向相反） |

畫面上用的是正確的加號，註腳明說「書上第三項印的是減 2 y x³，可是它自己上面那行的 u₃
展開出來是加——數值也站在加號這邊」。程式裡不是用註解記著，而是**用一個機械檢查釘住**：

```python
assert abs(TAY_U - UEND) < abs(TAY_U_AS_PRINTED - UEND) / 5, \
    "the plus sign matches the iteration, and by a wide margin"
```

這樣如果哪天有人「照書修正」回減號，assert 會直接失敗。

## 所有數字都出自同一個具體的問題

G(y) = y² + y − 0.6，根是 0.4219544（解析解，所以誤差是真的誤差）。兩個方法都從 y₀ = 1.5 出發，
**第一步完全相同**（兩者都用 dG(y₀) = 4），之後分道揚鑣：

| i | 固定斜率的誤差 | Newton 的誤差 |
|---|---|---|
| 1 | 2.91e-01 | 2.91e-01 |
| 2 | 1.36e-01 | 3.48e-02 |
| 3 | 6.85e-02 | 6.33e-04 |
| 4 | 3.57e-02 | 2.17e-07 |
| 5 | 1.89e-02 | 2.56e-14 |

固定斜率的誤差每一步乘上約 0.51（程式驗過四個比值的散布小於 0.08，所以真的是幾何收斂）；
Newton 的每一步都把誤差平方（程式逐項驗過 Δᵢ ≤ K²Δᵢ₋₁²，K = 2 同時界住 ‖dG⁻¹‖ 與 ‖d²G‖）。

beat 8 的常數照書上的關係式算：τ = 3/2、K = 2 時 c = 1.8484，e^c = 6.35 ≥ 4，
尾巴的和 0.658 ≤ 1，最後條件收成 ‖G(0)‖ ≤ K⁻⁵ = 0.03125。

beat 9、10 的平面例子：H(u,v) = ⟨u + v², u³ + v⟩，Jacobian 在原點是單位矩陣，
差 J(u) = ⟨v², u³⟩ 只剩高階項。迭代 uₙ = x − J(uₙ₋₁) 從零出發，
程式驗過收斂之後 H 作用回去與原點的差小於 1e-14。

## 這一輪抓到的錯

**第一版的 beats 3、4 完全沒用。** 我原本選 G(y) = e^y − 1.3 畫在 y ∈ [−0.05, 0.45] 上，
可是 e^y 在那一小段幾乎是直線，**兩張圖看起來一模一樣**——而這兩拍唯一要講的事，
就是「固定斜率的線互相平行」對上「切線的斜率各不相同」。換成有明顯曲率的二次式、
從 y₀ = 1.5 出發之後，三條平行線與三條切線一眼就分得出來，Newton 的落點也明顯更靠近根。

**教訓**：挑範例函數時要先問「它在我要畫的那一段裡看起來是什麼形狀」，
而不是只看它數學上對不對。**E60 是「收斂太快畫不出收斂」，這次是「曲率太小畫不出差別」——
同一類病的兩個方向。**

其他三件：

- **又是 `if False else` 的 dead code 夾中文**，兩處。**這跟 E63 記下的是同一個錯，連續兩集出現**，
  代表是寫作習慣問題不是偶然。這次在跑檢查前就自己抓到了。
- **公式列有兩處符號打架**：指數寫成 `ᵗ`（因為沒有上標的 τ）而畫面與旁白都是 τ；
  beat 0 的 `C` 同時當 Lipschitz 常數與 C¹ 平滑度類。
  前者改用 `exp ( − c τ ⁿ )`，後者改成 `‖ d K ² ‖ ≤ C < 1 ⇒ ∃ d F`。
- **一句手打的註腳**（「第四步固定斜率是 1.1e-03，Newton 是 2.5e-07」）改成 f-string 從資料生成。
  **那正是 E63 那個 0.500／0.486 錯誤的成因**——註腳宣稱一個數字，而那個數字是別處算的。

`collide` 另外抓到兩處：beat 7 的誤差曲線從左上角出發，正好穿過座標軸的標籤；
beat 10 的最後一列壓到註腳。

---

## Beat 0 — 定理 9.4：反過來的方向 / Theorem 9.4: the other direction
*配音長度：中文 16.8s ／ 英文 17.3s*

**畫面公式**

```
定理 9.4：反過來的方向   |   Theorem 9.4: the other direction
‖ d K ² ‖   ≤   C   <   1              ⇒              ∃ d F
```

**旁白（繁中）**

> 定理 9.4 是反過來的方向：如果那個壓縮本身可微，而且滿足定理 9.2 的假設，那麼它隱含定義出來的函數也可微。推論再補一句：連續可微這件事也一樣傳得下去。

**Narration (EN)**

> Theorem 9.4 goes the other way. If the contraction is differentiable and satisfies the hypotheses of Theorem 9.2, then the function it defines implicitly is differentiable too, and the corollary adds that continuous differentiability is inherited as well.

**動畫**

兩個框「K 可微」→「F 可微」與一支箭頭標著定理 9.4，底下補一句推論。
右側點出：**假設可微的是 K 自己，不是 F。**

## Beat 1 — 證明：材料都備好了 / the proof: the pieces are already in place
*配音長度：中文 18.5s ／ 英文 20.2s*

**畫面公式**

```
證明：材料都備好了   |   the proof: the pieces are already in place
G  =  η  −  K              d G ²  =  I  −  d K ²            ∃ ( d G ² ) ⁻ ¹
```

**旁白（繁中）**

> 證明很短，因為材料都備好了。K 的 Lipschitz 條件就是它的微分有界，所以令 G 是 η 減去 K；G 的微分是單位映射減去 K 的微分，定理 8.1 保證它可逆，再引第 3 章的定理 11.1 就結束。

**Narration (EN)**

> The proof is short because the pieces are in place. The Lipschitz condition on K is a bound on its differential, so define G as eta minus K. The differential of G is the identity minus that of K, which Theorem 8.1 makes invertible, and Theorem 11.1 of chapter 3 finishes it.

**動畫**

三列推導加一條虛線與結論。註腳點出這是**第 8 節那條幾何級數的第二次回收**——
整個第 4 章到這裡扣成一串：完備、Banach 代數、不動點三件事互相支撐。

## Beat 2 — 不動點定理其實是一個演算法 / the fixed-point theorem is an algorithm
*配音長度：中文 16.2s ／ 英文 15.7s*

**畫面公式**

```
不動點定理其實是一個演算法   |   the fixed-point theorem is an algorithm
η ᵢ ₊ ₁   =   K ( ξ , η ᵢ )
```

**旁白（繁中）**

> 書上接著特別強調一件容易漏掉的事：不動點定理不只是「隱函數定理的推論」而已——它的證明還給出一個真正能把值算出來的迭代程序，只要中心那一點的反元素算得出來。

**Narration (EN)**

> The book then emphasises something easy to miss. The fixed-point theorem does not only have the implicit-function theorem as a consequence; its proof gives an iterative procedure for actually computing the value, once the one inverse at the center point is known.

**動畫**

迭代式往下展開成「減去固定的 T⁻¹ 乘 G」，並標明 **T 只算一次，之後每一步重複用**。

## Beat 3 — 固定斜率的那一道階梯 / the staircase of one fixed slope
*配音長度：中文 18.0s ／ 英文 17.0s*

**畫面公式**

```
固定斜率的那一道階梯   |   the staircase of one fixed slope
( η ᵢ ₊ ₁  −  η ᵢ )    =    −  T ⁻ ¹ G ( ξ , η ᵢ )
```

**旁白（繁中）**

> 寫出來就是：每一步都減去「那個固定的反元素」乘上 G 在當前點的值。在一維的情況下，圖像是一道階梯——從當前點沿著一條固定斜率的直線走到橫軸，那個橫座標就是下一點。

**Narration (EN)**

> Written out, each step moves by minus that fixed inverse applied to G at the current point. In one real dimension the picture is a staircase: from the current point, follow a line of one fixed slope down to the axis, and that horizontal position is the next point.

**動畫**

G(y) = y² + y − 0.6 的曲線與三段階梯：豎直走到曲線，再沿一條斜率固定為 T 的直線回到橫軸。
**三條斜線彼此平行**——這就是「固定斜率」的樣子。**書上畫成一張圖（Fig. 4.4），
這裡的曲線、階梯與標號都是自己重新設計的。**

## Beat 4 — Newton 法：改用當地的斜率 / Newton: use the local slope instead
*配音長度：中文 15.4s ／ 英文 15.0s*

**畫面公式**

```
Newton 法：改用當地的斜率   |   Newton: use the local slope instead
( η ᵢ ₊ ₁  −  η ᵢ )    =    −  S ᵢ ⁻ ¹ G ( ξ , η ᵢ )        S ᵢ = d G ² ₍ ξ , η ᵢ ₎
```

**旁白（繁中）**

> Newton 法把固定的斜率換成當地的斜率：每一步用的是 G 在當前點的微分，而不是中心那一點的。圖像就是熟悉的切線階梯，而且看得出來它逼近根的速度快得多。

**Narration (EN)**

> Newton's method replaces the fixed slope with the local one: at each step use the differential of G at the current point rather than at the center. The picture is the familiar tangent-line staircase, and the steps close in on the root visibly faster.

**動畫**

同一條曲線、同一個起點，可是**三條斜線的斜率各不相同**（各自是當地的切線），
落點明顯更靠近根。（Fig. 4.5 的自繪版本。）

## Beat 5 — 快，可是要付代價 / faster, but it has to be paid for
*配音長度：中文 16.1s ／ 英文 17.4s*

**畫面公式**

```
快，可是要付代價   |   faster, but it has to be paid for
T ⁻ ¹     ×  1                    S ᵢ ⁻ ¹     ×  ∞
```

**旁白（繁中）**

> 書上把代價講得很清楚：Newton 法能用的時候收斂快得多，可是它的缺點是必須算得出無窮多個線性變換的反元素，每一步一個；而前面那個程序只算一次，之後一直重複用。

**Narration (EN)**

> The trade is stated plainly. Newton converges much more rapidly when it works, but it suffers the disadvantage that the inverses of an infinite number of linear transformations must be computable, one for every step, where the first procedure inverts once and reuses it.

**動畫**

兩個框標出「要算幾個反元素」：固定斜率 × 1，Newton × ∞。
右側把兩個方法的誤差並排列出來——同一個問題，同一個起點。

## Beat 6 — 快多少：e 的負 c τ ⁿ / how much faster: e to the minus c tau to the n
*配音長度：中文 16.7s ／ 英文 17.9s*

**畫面公式**

```
快多少：e 的負 c τ ⁿ   |   how much faster: e to the minus c tau to the n
‖ d G ₓ ⁻ ¹ ‖ ≤ K , ‖ d ² G ₓ ‖ ≤ K        ‖ x ₙ − x ₙ ₋ ₁ ‖ ≤ exp ( − c τ ⁿ )
```

**旁白（繁中）**

> 快多少？假設在單位球上，微分的反元素與二階微分的範數都不超過 K。要證的是：對一到二之間的 τ 與某個常數 c，第 n 步的長度不超過 e 的負 c 乘 τ 的 n 次方。

**Narration (EN)**

> How much faster? Assume the inverse differential and the second differential are both bounded by K on the unit ball. The claim is that for tau between one and two, and some constant c, the steps satisfy that the n-th one is at most e to the minus c tau to the n.

**動畫**

三列假設加一條虛線與結論。註腳點明：**這不是幾何收斂**——幾何收斂是 e 的負 c n，
這裡的指數是 τ 的 n 次方，指數裡還有一個指數。

## Beat 7 — 每一步把誤差平方一次 / each step squares the error
*配音長度：中文 14.5s ／ 英文 17.3s*

**畫面公式**

```
每一步把誤差平方一次   |   each step squares the error
‖ x ₙ ₊ ₁ − x ₙ ‖      ≤      K ²  ‖ x ₙ − x ₙ ₋ ₁ ‖ ²
```

**旁白（繁中）**

> 歸納的關鍵一步是 Taylor 定理：一階項剛好消掉，剩下每一步不超過 K 平方乘上前一步的平方。每走一步誤差就平方一次——那正是 Newton 法買到的東西。

**Narration (EN)**

> The induction turns on Taylor's theorem. The first-order term cancels exactly, leaving each step bounded by K squared times the square of the previous one. Squaring the error at every step is what exponential-of-an-exponential convergence means, and it is what Newton buys.

**動畫**

對數尺度上兩條折線：紅色（固定斜率）幾乎是直的，紫色（Newton）明顯往下折。
右側逐項驗證 Δᵢ ≤ K²Δᵢ₋₁²，K = 2.000。

## Beat 8 — 取 τ 等於二分之三 / taking tau to be three halves
*配音長度：中文 17.2s ／ 英文 17.5s*

**畫面公式**

```
取 τ 等於二分之三   |   taking tau to be three halves
K ²   ≤   exp ( ( 2 − τ ) c τ ⁿ )                ‖ G ( 0 ) ‖   ≤   K ⁻ ⁵
```

**旁白（繁中）**

> 要讓歸納接得下去，K 平方必須不超過 e 的（二減 τ）乘 c 乘 τ 的 n 次方；因為 τ 小於二，把 c 取大就行。取 τ 等於二分之三時，所有條件會收斂成對起始值的一個要求。

**Narration (EN)**

> For the induction to close, K squared must be at most e to the two minus tau, times c tau to the n, which can be arranged by taking c large since tau is under two. With tau three halves the conditions collapse to a single requirement on the starting value.

**動畫**

照書上的關係式把常數算出來：K = 2、c = 1.8484、e^c = 6.35 ≥ 4，
尾巴的和 0.658 ≤ 1，最後 ‖G(0)‖ ≤ K⁻⁵ = 0.03125。

## Beat 9 — 平面上最簡單的反映射 / the simplest inverse mapping in the plane
*配音長度：中文 17.6s ／ 英文 17.5s*

**畫面公式**

```
平面上最簡單的反映射   |   the simplest inverse mapping in the plane
x  =  u  +  v ²   ,   y  =  u ³  +  v                J ( u )  =  ⟨ v ² , u ³ ⟩
```

**旁白（繁中）**

> 這一節收在一個盡可能簡單的例子：平面上的反映射。取 x 等於 u 加 v 平方，y 等於 u 立方加 v。Jacobian 矩陣在原點正好是單位矩陣，而映射與恆等映射的差只剩高階項。

**Narration (EN)**

> The section ends with the simplest possible example, an inverse mapping in the plane. Take x as u plus v squared and y as u cubed plus v. The Jacobian is the identity at the origin, and the difference between the map and the identity has only higher-order terms.

**動畫**

映射的兩式、dH₀ = I，以及 H(u) − u = J(u) = ⟨v², u³⟩。
**一階項在這裡被消掉了——這就是 dK² = 0 的實際樣貌。**

## Beat 10 — 迭代算出來的正是 Taylor 展開 / the iterates are computing Taylor expansions
*配音長度：中文 17.6s ／ 英文 17.6s*

**畫面公式**

```
迭代算出來的正是 Taylor 展開   |   the iterates are computing Taylor expansions
u  =  x  −  y ²  +  2 y x ³  + …            v  =  y  −  x ³  +  3 x ² y ²  + …
```

**旁白（繁中）**

> 那個消去，正是「微分在中心點等於零」的實際樣貌。從零出發，每一步的迭代都是多項式，而它們算的正是兩個反函數的 Taylor 展開：x 減 y 平方往下接，還有 y 減 x 立方往下接。

**Narration (EN)**

> That cancellation is the practical face of the differential vanishing at the center. Starting from zero, the iterates are polynomials, and they are computing the Taylor expansions of the two inverse functions: x minus y squared and onwards, y minus x cubed and onwards.

**動畫**

兩列 Taylor 展開（**u 那一列用的是正確的加號**），底下用 (x, y) = (0.10, 0.08)
把迭代到收斂的值 0.0937311 與加號版截斷式 0.0937600 擺在一起。
右側列出 u₁ 到 u₄、v₁ 到 v₄ 的實際數值，並註明 H 作用回去的誤差小於 1e-14。
**註腳明說書上第三項印的是減號，而書上自己的 u₃ 展開出來是加號。**
