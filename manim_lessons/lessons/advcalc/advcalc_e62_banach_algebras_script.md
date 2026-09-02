# advcalc E62 — 第 4 章：Banach 代數初探

Chapter 4: A First Look at Banach Algebras

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 8 節「Banach 代數初探」（書頁 223–226）。書頁 227–228 是習題 8.1–8.24，依 PLAYBOOK 第 8 節不做解答；第 9 節從書頁 228 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e62_banach_algebras.py`（`AdvCalcE62ZH` / `AdvCalcE62EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[62]` / `FORMULAS_ADVCALC[62]`）
- 配音：`manim_lessons/samples/audio_e62/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.88 分（233 秒）／英文 3.46 分（208 秒）

## 這一節是為了還第 3 章的帳

反映射定理當時用了一件事：**T 可逆，跟它夠靠近的 S 也可逆，而且反元素連續地依賴它**。
有限維可以靠行列式的連續性，一般的情況當時沒有工具。第 8 節就是來還這筆帳的，
而還帳的方式出乎意料地初等——**把問題丟回幾何級數**。

書上那句話是這一節的樞紐：把「它們是變換」這件複雜的事忘掉，只當成抽象代數裡的元素。
一旦這樣看，初等微積分裡「一減 x 分之一等於 x 的 n 次方的和」就原封不動地成立，
可逆元是開集、取反元素連續，兩件事都跟著掉出來。

後半轉向可微性：冪級數在球上收斂（8.3）、指數函數處處收斂、
極限的可微性（8.4）加上兩條引理讓冪級數可以逐項微分（8.5）。
**最值得注意的是答案的形狀**：F 在 y 的微分不是什麼複雜的線性變換，
就是「乘上某一個元素」，而那個元素正是 F 撇 y。

## 所有數字都建立在真的 2×2 矩陣上

這一集刻意不用示意圖。用的範數是**最大列和範數**——它是次可乘的（‖ST‖ ≤ ‖S‖‖T‖），
而且單位元的範數正好是 1，所以**畫面上那組 Banach 代數公理，就是這些數字真正滿足的公理**。

- **beat 1**：‖S‖ = 0.90、‖T‖ = 0.90、‖ST‖ = 0.45 ≤ 0.81。不等式是真的，而且是鬆的。
  分配律也用數值驗過（浮點所以比對範數差小於 1e-12，不是比對相等）。
- **beat 2**：‖x‖ = 0.50，幾何級數的部分和對精確反元素（用 2×2 反矩陣公式算的）
  誤差 3.18e-01 → 5.79e-02 → 6.33e-04 → 1.91e-05。
- **beat 3**：三個半徑各自把 x 縮放到範數剛好等於 r，量到的值與上界是
  0.239／0.250、0.586／0.667、1.102／1.500。
  **我原本的 assert 寫「上界很鬆」，跑出來被打臉**——比值是 0.96、0.88、0.74，
  最後一個不算鬆。assert 與畫面上的註腳都改成照實說：r = 0.60 量到 1.10，上界是 1.50。
- **beat 4**：y 的反元素範數 m = 1.50，所以保證半徑 1/m = 0.667；
  程式驗過半徑內的擾動確實還可逆，而且夠遠時（h 取成 y 自己）真的會壞掉。
- **beat 6**：δ = 1.0、s = 0.70、r = s/δ = 0.70、b = 1.00，逐項驗過 ‖aₙ‖sⁿ ≤ b rⁿ。
- **beat 7 與 beat 10 是同一個例子**：x 取旋轉的生成元 θJ，指數的部分和對真正的旋轉矩陣
  誤差 2.0e-01 → 1.6e-03 → 3.0e-06 → 1.2e-11。而 γ(t) = e^{tx} 打在單位圓上，
  **速度與半徑的內積算出來是 0.0**，所以「它是切的」是算出來的，不是註腳講的。

## 三道檢查全過之後，probe 幀抓到四處

1. **beat 9 的第三支箭頭落到右側面板旁邊**。三支箭頭本來要指在級數的三個項底下，
   x 座標算錯，最後一支跑到 x = 0.80，正好貼著面板第二行的文字，看起來像面板的一部分。
2. **beat 6 的「s = 0.70」壓在外圈圓弧上**。標籤放在內圈下方，可是那個位置正好是外圈的弧。
   移到圓的右側。
3. **beat 2 與 beat 7 的對數誤差圖，最後一點正好落在座標軸上**，看起來像「誤差變成 0」，
   可是實際是 1.91e-05 與 1.2e-11。兩張圖都在下緣加了留白。

`bounds` 另外抓到 21 處（beat 0 的說明字壓在 blob 上方而超出 y = 1.30、
beat 6 的 δ 標籤壓在已經頂到上限的圓上），`collide` 抓到 2 處
（**r/(1−r) 的曲線穿過自己的標籤**——曲線在右端爬到框頂，而標籤正好放在那裡；
改成放到左邊平坦那一段的上方）。

---

## Beat 0 — 第 3 章留下來的那個問題 / the question left over from chapter 3
*配音長度：中文 19.8s ／ 英文 17.4s*

**畫面公式**

```
第 3 章留下來的那個問題   |   the question left over from chapter 3
∃ T ⁻ ¹        ‖ S  −  T ‖  <  δ        ⇒        ∃ S ⁻ ¹
```

**旁白（繁中）**

> 第 8 節從第 3 章留下來的一個問題開始。反映射定理那裡用到一件事：T 可逆的話，跟它夠靠近的 S 也可逆，而且反元素還連續地依賴它。有限維可以靠行列式的連續性，可是一般的情況要另一套辦法。

**Narration (EN)**

> Section 8 starts from a question left over from chapter 3. The inverse mapping theorem used the fact that if T is invertible then so is every S close enough to it, and that the inverse depends continuously on it. In finite dimensions the determinant settles that.

**動畫**

一個不規則的區域代表「可逆元的全體」，裡面一個橘點 T，外面套一個紅圈——
那個紅圈就是要證明存在的半徑；圈裡的 S 都還在可逆元裡面。

## Beat 1 — Banach 代數的公理 / the axioms of a Banach algebra
*配音長度：中文 24.2s ／ 英文 18.1s*

**畫面公式**

```
Banach 代數的公理   |   the axioms of a Banach algebra
S ( T ₁ + T ₂ ) = S T ₁ + S T ₂        ‖ S T ‖ ≤ ‖ S ‖ ‖ T ‖        ‖ I ‖ = 1
```

**旁白（繁中）**

> 先把 Hom V 的性質整理一遍。它是 Banach 空間，而且帶著一個結合的乘法——就是合成。乘法對加法分配、跟純量相容，而且跟範數扣在一起：乘積的範數不超過兩個範數的乘積，單位映射的範數是一。這幾條合起來就是 Banach 代數的公理。

**Narration (EN)**

> First, the properties of Hom V. It is a Banach space, and it carries an associative multiplication, namely composition. The multiplication distributes over addition and ties to the norm: a product has norm at most the product of the norms, and the identity has norm one.

**動畫**

左邊四列公理，右邊用畫面上那兩個矩陣把最後一條驗一次：
‖S‖ = 0.90、‖T‖ = 0.90、‖ST‖ = 0.45，而 0.90 × 0.90 = 0.81。

## Beat 2 — 定理 8.1：幾何級數 / Theorem 8.1: the geometric series
*配音長度：中文 21.4s ／ 英文 19.5s*

**畫面公式**

```
定理 8.1：幾何級數   |   Theorem 8.1: the geometric series
‖ x ‖   <   1          ⇒          ( e − x ) ⁻ ¹    =    Σ ₀ ∞   x ⁿ
```

**旁白（繁中）**

> 書上接著說：把「它們是變換」這件複雜的事先忘掉，只當成抽象 Banach 代數裡的元素。定理 8.1：如果 x 的範數小於一，那麼 e 減 x 可逆，而且反元素就是幾何級數，x 的 n 次方的和——跟初等微積分那條一模一樣。

**Narration (EN)**

> The book then says to forget that these are transformations and treat them as elements of an abstract Banach algebra. Theorem 8.1: if the norm of x is under one, then e minus x is invertible and its inverse is the geometric series, exactly as in elementary calculus.

**動畫**

部分和對精確反元素的誤差，畫成對數尺度上的一條下降折線；
右側列出 n = 2、4、8、12 的實際數值。

## Beat 3 — 順便得到的誤差估計 / the estimate that comes along with it
*配音長度：中文 21.2s ／ 英文 19.2s*

**畫面公式**

```
順便得到的誤差估計   |   the estimate that comes along with it
‖ e  −  ( e − x ) ⁻ ¹ ‖      ≤      r / ( 1 − r )            r  =  ‖ x ‖
```

**旁白（繁中）**

> 證明只用到絕對收斂：x 的 n 次方的範數不超過範數的 n 次方，跟實數的幾何級數比較就收斂，而上一集的定理 7.11 保證它在 Banach 空間裡真的收斂。順便還得到誤差估計：e 減去那個反元素，範數不超過 r 除以一減 r。

**Narration (EN)**

> The proof only needs absolute convergence: the norm of a power is at most the power of the norm, so comparison with the real geometric series gives it, and Theorem 7.11 makes it converge. The estimate comes along too: e minus that inverse has norm at most r over one minus r.

**動畫**

r/(1−r) 的曲線，底下三個點是三個半徑上量到的實際值，各自帶一條虛線標出對應的上界。
三個點都在曲線下面。

## Beat 4 — 定理 8.2：可逆元是開集 / Theorem 8.2: the invertible elements are open
*配音長度：中文 18.5s ／ 英文 19.1s*

**畫面公式**

```
定理 8.2：可逆元是開集   |   Theorem 8.2: the invertible elements are open
‖ h ‖  <  1 / m        ⇒        ∃ ( y − h ) ⁻ ¹                m  =  ‖ y ⁻ ¹ ‖
```

**旁白（繁中）**

> 定理 8.2：可逆元的全體是一個開集，而且取反元素這個映射在上面連續。定量的說法是這樣：y 可逆，m 是 y 的反元素的範數，那麼只要 h 的範數小於 m 分之一，y 減 h 就一定可逆。

**Narration (EN)**

> Theorem 8.2: the set of invertible elements is open, and the map sending an element to its inverse is continuous on it. Quantitatively: if y is invertible and m is the norm of its inverse, then y minus h is invertible whenever the norm of h is less than one over m.

**動畫**

同一個區域，裡面一點 y 與一個半徑 1/m 的紅圈；右側列出 m = 1.50、1/m = 0.667，
以及畫面上那個擾動的 ‖h‖ = 0.633 < 1/m。

## Beat 5 — 一行代數，補上第 3 章的洞 / one line of algebra fills chapter 3's gap
*配音長度：中文 23.0s ／ 英文 20.8s*

**畫面公式**

```
一行代數，補上第 3 章的洞   |   one line of algebra fills chapter 3's gap
y − h  =  y ( e − x )  ,  x  =  y ⁻ ¹ h            ‖ x ‖  ≤  m ‖ h ‖  <  1
```

**旁白（繁中）**

> 證明的手法很漂亮：把 y 減 h 寫成 y 乘上 e 減 x，其中 x 是 y 的反元素乘 h。x 的範數不超過 m 乘 h 的範數，小於一，所以定理 8.1 直接可以用。推論就是第 3 章欠的那一條：可逆元構成開集，而取反元素在那上面連續。

**Narration (EN)**

> The trick is neat: write y minus h as y times e minus x, where x is the inverse of y times h. The norm of x is at most m times the norm of h, which is under one, so Theorem 8.1 applies. The corollary is what chapter 3 needed: inversion is continuous on an open set.

**動畫**

三列代數推導，底下一條虛線，再一列結論 (y − h)⁻¹ = (e − x)⁻¹ y⁻¹。
**整個過程沒有碰行列式。**

## Beat 6 — 定理 8.3：冪級數在球上 / Theorem 8.3: power series on a ball
*配音長度：中文 21.1s ／ 英文 19.6s*

**畫面公式**

```
定理 8.3：冪級數在球上   |   Theorem 8.3: power series on a ball
‖ a ₙ ‖ δ ⁿ  ≤  b            0 < s < δ            Σ a ₙ x ⁿ  ,  ‖ x ‖ ≤ s
```

**旁白（繁中）**

> 幾何級數只是一個例子。定理 8.3 說：如果 a n 乘 δ 的 n 次方那一列的範數有界，那麼 a n 乘 x 的 n 次方的級數在半徑 δ 的球裡收斂，而且在任何一個更小的球上均勻收斂。證明還是拿實數的幾何級數來比較。

**Narration (EN)**

> The geometric series is only one example. Theorem 8.3: if the norms of a-n times delta to the n stay bounded, the series of a-n times x to the n converges on the ball of that radius, and uniformly on any smaller one. The proof again compares with a real geometric series.

**動畫**

兩個同心圓：外圈是半徑 δ 的球，內圈是半徑 s 的小球。
右側列出 b = 1.00、r = s/δ = 0.70，以及比較級數的和 Σ b rⁿ = 3.33。

## Beat 7 — 指數函數，處處收斂 / the exponential, convergent everywhere
*配音長度：中文 16.7s ／ 英文 17.4s*

**畫面公式**

```
指數函數，處處收斂   |   the exponential, convergent everywhere
e ˣ    =    Σ ₀ ∞    x ⁿ  /  n !
```

**旁白（繁中）**

> 最想要的那個例子是指數函數：x 的 n 次方除以 n 階乘的和。初等微積分那套比較法整套搬過來就得到：這個級數對代數裡每一個 x 都收斂，而且在任何一個球上都均勻收斂。

**Narration (EN)**

> The example most wanted is the exponential, the sum of x to the n over n factorial. The usual comparison arguments of elementary calculus carry over unchanged and give that this series converges for every x in the algebra, and uniformly on any ball.

**動畫**

取 x 是旋轉的生成元，指數的部分和對真正的旋轉矩陣的誤差畫成對數折線：
2.0e-01 → 1.6e-03 → 3.0e-06 → 1.2e-11。**指數真的就是那個旋轉。**

## Beat 8 — 定理 8.4：極限的可微性 / Theorem 8.4: differentiating a limit
*配音長度：中文 20.2s ／ 英文 17.6s*

**畫面公式**

```
定理 8.4：極限的可微性   |   Theorem 8.4: differentiating a limit
F ⁿ   →   F              d F ⁿ ᵦ   →   d F ᵦ              ∀ β  ∈  B
```

**旁白（繁中）**

> 接下來問這些映射可不可微。定理 8.4 是一條關於「極限的可微性」的定理：一列映射逐點收斂到 F，而且它們的微分在每一點都收斂、關於那一點還是均勻的，那麼 F 可微，而且微分就是那些微分的極限。

**Narration (EN)**

> Then the question is whether these maps are differentiable. Theorem 8.4 is about the differentiability of a limit: if a sequence of maps converges pointwise to F and their differentials converge at each point, uniformly in that point, then F is differentiable.

**動畫**

三列：逐點收斂、關於 β 均勻收斂，一條虛線之後是結論。
右側說明微分的收斂必須是均勻的，逐點不夠。

## Beat 9 — 一項一項微分下去 / differentiating term by term
*配音長度：中文 23.5s ／ 英文 20.7s*

**畫面公式**

```
一項一項微分下去   |   differentiating term by term
d p ₍ a , b ₎ ( x , y )  =  a y  +  x b            d p ᵧ ( x )  =  n a y ⁿ ⁻ ¹ x
```

**旁白（繁中）**

> 有了它就能一項一項微分下去。引理 8.1：乘法本身可微，微分是 a y 加 x b。引理 8.2：交換代數上的單項式 a 乘 x 的 n 次方可微，微分是 n a y 的 n 減一次方再乘 x。定理 8.5 把兩件事接起來：冪級數在球裡可微。

**Narration (EN)**

> That lets the series be differentiated term by term. Lemma 8.1: multiplication itself is differentiable, with differential a y plus x b. Lemma 8.2: on a commutative algebra the monomial a x to the n has differential n a y to the n minus one, times x.

**動畫**

上下兩列：F(x) 的冪級數與 F′(y) 的逐項微分，三支箭頭**指在對應的項底下**
（a₁x → a₁、a₂x² → 2a₂y、a₃x³ → 3a₃y²）。

## Beat 10 — 微分就是「乘上 F 撇」 / the differential is multiplication by F prime
*配音長度：中文 22.6s ／ 英文 17.6s*

**畫面公式**

```
微分就是「乘上 F 撇」   |   the differential is multiplication by F prime
d F ᵧ ( x )   =   F ′ ( y )  ·  x                  e ˣ ⁺ ʸ   =   e ˣ  e ʸ
```

**旁白（繁中）**

> 這裡有一件很值得停下來看的事：F 在 y 的微分，就是「乘上某一個元素」這個線性變換，而那個元素正好是逐項微分得到的 F 撇 y。指數函數因此是自己的導數，指數律也跟著出來——不過要小心，那條要在交換的 Banach 代數上才成立。

**Narration (EN)**

> One thing is worth pausing on: the differential of F at y is multiplication by a single element of the algebra, namely the F prime that term-by-term differentiation produces. The exponential is its own derivative, and the law of exponents follows on a commutative algebra.

**動畫**

γ(t) = e^{tx} 在單位圓上的一點，加上切向的速度箭頭 γ′(t) = x e^{tx}。
右側把「它是切的」變成數字：γ(t) 與 γ′(t) 的內積是 0.0，而兩者的範數都是 1。
