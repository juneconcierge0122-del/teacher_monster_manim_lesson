# advcalc E68 — 第 5 章：純量積

Chapter 5: Scalar Products

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 1 節「純量積」（書頁 247–251），含章首引言。

**§1 的內容收在書頁 251**（251–252 是習題 1.1–1.10，依 PLAYBOOK 第 8 節不做解答），§2「正交投影」從書頁 252 起。

**這一集同時把第 5 章的細目表補進 `OUTLINE.md`**——那張表原本只有章層級的「248–266，5 節，6 集」。
新的細目表是照書一頁一頁核出來的，內容頁與習題頁分開標，並且記下一件事：
**§5「緊算子」整節沒有習題**，書頁 265 講完直接進第 6 章，這是這本書裡第三次
（前兩次是第 2 章的 *§7 與第 4 章的 *§12）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e68_scalar_products.py`（`AdvCalcE68ZH` / `AdvCalcE68EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[68]` / `FORMULAS_ADVCALC[68]`）
- 配音：`manim_lessons/samples/audio_e68/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.43 分（206 秒）／英文 3.34 分（200 秒）

## 這一節的結構

書上把整套東西一次擺出來，這一集照著走：

1. **章首的問題**：two-norm 背後是什麼？答案是純量積。
2. **三條定義**（對第一變數線性、對稱、正定），把第三條放寬就是半純量積。
3. **兩個例子**，它們正好解釋兩個 two-norm 從哪裡來。
4. **半純量積就是對稱雙線性泛函**，它的二次形式正定或半正定（第 2 章最後一節的語言）。
5. **定理 1.1 Schwarz**，一行證明：不變號的二次式判別式不能是正的。
6. **推論**：那個平方根是範數。三角不等式就是 Schwarz 用在中間項。
7. **pre-Hilbert / Hilbert / 歐氏 n 維空間**；有限維一定完備，連續函數配 two-norm 不完備。
8. **正交**、夾角、正交補；**引理 1.1**（正交補是閉子空間）。
9. **引理 1.2**（平行四邊形法則與畢氏定理）與**推論**（正交非零向量獨立）。

## 這一集的具體例子

兩個空間承擔畫面上所有數字：**平面配歐氏範數**，以及 **C([0,1]) 配 (f, g) = ∫ f g**。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 三條定義 | 在同一個例子（f = t、g = eᵗ、h = 1 − t）上逐條算 | 4.1548 = 4.1548、對稱差 0e+00、(f, f) = 0.3333 |
| Schwarz（幾乎成比例的一對） | 二次式的係數與判別式 | 判別式 -0.2594 ≤ 0，最低點 0.0203，比值 0.9691 |
| Schwarz（差得遠的一對） | 同一個算法 | 判別式 -0.3333，最低點 0.2500，比值 0.5000 |
| 三角不等式 | 兩對函數 | 2.3511 ≤ 2.3647（比值 0.9943）、1.0000 ≤ 1.1547 |
| 正定 vs 不定 | q 在 720 個方向上的最小值 | b = 0.8 時 0.5566；b = 2.0 時 -0.5616 |
| 夾角 | 從 (f, g) ／ ‖f‖‖g‖ 反餘弦 | 14.29°、60.00°、90.00° |
| two-norm 下不完備 | 習題 1.10 的斜坡列，閉式與細分黎曼和互核 | ‖fₙ − k‖₂ = 0.2041 → 0.0722 |
| 引理 1.1 | s₄ 與 s₁、s₂ 四組線性組合的內積 | 最大 3e-15 |
| 引理 1.2（正交族） | ‖Σ xᵢsᵢ‖² 對 Σ xᵢ²‖sᵢ‖² | 3.1102 = 3.1102 |
| 平行四邊形法則 | 同一對向量，四種範數 | 兩範數 5.3800 = 5.3800；一範數差 2.24；上界範數差 1.68 |
| 畢氏定理 | 正交的那一對 | 1.5000 = 1.5000 |

**第一拍問的問題，最後一拍回答。** 開場畫三個單位球面（圓、菱形、正方形，都是從範數本身算出來畫的）
並問「哪一個是從純量積來的」；結尾用平行四邊形法則回答：**同一對向量，兩範數兩邊相等，
一範數差 2.24，上界範數差 1.68。** 書上章首那句「two-norm 可以抽象地刻畫成從純量積來的那些」
指的就是這件事（反方向的定理書上沒證，這裡也只給反例，不宣稱刻畫）。

## 這一輪抓到的錯

### 一、圖說宣稱了一個數量關係，而那個關係是尺度相依的

beat 5 原本的圖說寫「最低點就是 Schwarz 的鬆緊」。可是 q(t*) = (f, f) − (f, g)²／(g, g)，
它等於**鬆緊除以 (g, g)**；而畫面上那兩對函數的 (g, g) 差了將近十倍（3.1945 對 0.3333），
所以把 0.0203 與 0.2500 並排當成「鬆緊」比較，是拿兩把不同的尺在量。
改成：圖說只說「最低點等於零才是等號成立」，註腳把兩欄各是什麼講清楚——
**比值那一欄才是跟尺度無關的，最低點還帶著 (g, g) 的大小。**

**這是 E63、E66 那一類錯的第三種變形**：前兩次是註腳講了一個畫面沒做的數量關係，
這次是註腳講了一個**成立但會誤導**的比較。規則再收緊一點：
**註腳只要把兩個數並排，就要先問「這兩個數是同一把尺量的嗎」。**

### 二、圖說說「三個圓」，而其中兩個不是圓

beat 0 畫的是三個單位球面：圓、菱形、正方形。註腳第一版寫「三個圓都是某個範數的單位球面」。
改成「三條曲線」。同一拍的問號原本放在菱形的正中央，看起來像在標那個菱形，移到三者上方。

### 三、beat 1 的三條曲線擠在一起

f、g、fg 畫在同一個框裡時，f 幾乎貼著軸、g 與 fg 在 t = 1 交會（因為 f(1) = 1），
三個標籤在右緣疊成一團。改成上下兩個框：上框放 f 與 g，下框放乘積與它下面的面積。
**兩條曲線在端點必然交會的時候，標籤沒有地方可以站——那就分框，不要硬擠。**

### 四、其他四處

- **bounds**：拋物線的 t 從 −0.25 起畫，x 跑到 −6.38（界是 −6.3）。改成 −0.20 並縮短橫向尺度。
- **collide**：beat 1 與 beat 2 的面積數字被畫面積的那些細線穿過；beat 10 的 α − β 標籤被它自己那支箭頭穿過。
  前者把數字移到曲線上方；後者把 α − β **改成從原點畫出**（平移過來的同一個向量），並在圖說裡說明——
  原本畫成 β 到 α 的那條對角線時，標籤能放的每個位置都被別的東西佔住了。
- **collide**：beat 3 的 1 ／ √a 標籤被橢圓穿過，往外挪。
- beat 4 的最低點數字原本放在 t 軸下方，看起來像「最低點是負的」，移到軸上方。

### 五、1080p 抽幀才抓到的兩件事（代價是重渲染一次）

**beat 7 的階梯函數被斜坡蓋掉了。** 三條斜坡在離跳躍點遠的地方跟 k **完全重合**，
而它們是後畫的，所以畫面上那條水平線是斜坡的顏色，不是 k 的青綠——
而註腳正好在點名「青綠色那條是階梯函數 k」。
**這跟 E67 beat 9 的切線／菱形邊重合是同一個病：兩個物件重合時後畫的贏，圖說就變成謊話。**
修法：把 k 移到最後畫，並在註腳講明「離跳躍點遠的地方斜坡與 k 完全重合，所以那裡只看得到 k」。

480p 探針裡這條線是看得到的，可是顏色混在一起，我當成了 k 的青綠；**1080p 才看清是誰蓋住誰。**
**所以「抽幀複查」要在 1080p 做，480p 只夠用來抓版面。**

**beat 6 的 ξ 標籤正好落在 η 那支箭頭的起點上**（`collide` 沒抓到——它比的是文字的 bounding box，
而那裡是文字對線條、且重疊量在門檻下）。同一拍的三邊長數字在圖下與註腳各印了一次，刪掉圖下那行。

這兩處都在第一次渲染之後才發現，於是重渲染一次（ZH 已渲完、EN 跑到一半時停掉重排）。

### 六、沒有 `if False`

連續五集之後第一次寫完沒有這個東西（寫完就先 `grep` 過）。
另外 `langscan` 的白名單加了 `Hilbert`——它在中文旁白裡也寫成拉丁字母（「Hilbert 空間」），
跟已經在名單上的 Cauchy、Banach 同一個理由。

---

## Beat 0 — two-norm 背後是什麼 / what lies behind the two-norms
*配音長度：中文 20.0s ／ 英文 17.3s*

**畫面公式**

```
two-norm 背後是什麼   |   what lies behind the two-norms
( ξ , η )    ⇒    ‖ ξ ‖ ,    ⊥ ,    θ
```

**旁白（繁中）**

> 第 5 章很短，可是它打開一整片新的線性分析。書上說：two-norm 背後的東西就是純量積，而這種範數是普通歐氏長度在有限與無限維的類比，帶著歐氏幾何幾乎所有概念——夾角、垂直、畢氏定理。

**Narration (EN)**

> Chapter 5 is short but opens a whole new branch of linear analysis. What lies behind two-norms, the book says, is the scalar product, and such norms are the finite and infinite-dimensional analogues of ordinary Euclidean length, carrying Euclidean geometry with them.

**動畫**

三條曲線：兩範數的圓（青綠）、一範數的菱形（紫）、上界範數的正方形（紅），每一條都是用 r = 1 ／ 範數(方向) 從那個範數本身算出來畫的。上方一個問號：哪一個是從純量積來的？

## Beat 1 — 三條定義，與半純量積 / three conditions, and the semiscalar case
*配音長度：中文 19.4s ／ 英文 18.4s*

**畫面公式**

```
三條定義，與半純量積   |   three conditions, and the semiscalar case
( ξ , η )  =  ( η , ξ )            ( ξ , ξ )  >  0            ( ξ , ξ )  ≥  0
```

**旁白（繁中）**

> 定義：實向量空間上的純量積是 V 乘 V 到 ℝ 的函數，要滿足三條——固定第二個變數時對第一個是線性的、對稱、以及正定。把正定換成「對每個向量都大於等於零」這個較弱的條件，就叫半純量積。

**Narration (EN)**

> The definition: a scalar product on a real vector space is a real-valued function of two vectors satisfying three conditions. It is linear in the first variable when the second is fixed, it is symmetric, and it is positive definite. Weakening the third gives a semiscalar product.

**動畫**

上框是 f(t) = t（青綠）與 g(t) = e^t（紫）；下框是它們的乘積（黃）加上垂直細線畫出的面積，那塊面積 1.0000 就是純量積的值。右側把三條定義逐條驗過。

## Beat 2 — 兩個例子 / the two examples
*配音長度：中文 17.7s ／ 英文 18.5s*

**畫面公式**

```
兩個例子   |   the two examples
( x , y )  =  Σ ᵢ x ᵢ y ᵢ                ( f , g )  =  ∫ ₐ ᵇ f g
```

**旁白（繁中）**

> 兩個重要的例子：ℝⁿ 上的座標乘積之和，以及連續函數空間上的 f 乘 g 的積分。複空間要把對稱換成 Hermitian 對稱，也就是交換兩個變數時取共軛。書上明說只做實數的情形。

**Narration (EN)**

> Two important examples: the sum of coordinate products on real n-space, and the integral of f times g on the continuous functions. On a complex space symmetry must be replaced by Hermitian symmetry, conjugating when the variables are swapped. The book studies only the real case.

**動畫**

左邊是平面上的例子：x 與 y 兩個向量，座標乘積加起來是 0.7800。右邊是同一個函數乘積的面積圖，1.0000。

## Beat 3 — 對稱雙線性泛函與它的二次形式 / a symmetric bilinear functional and its form
*配音長度：中文 20.5s ／ 英文 17.9s*

**畫面公式**

```
對稱雙線性泛函與它的二次形式   |   a symmetric bilinear functional and its form
q ( ξ )  =  ( ξ , ξ )        a x ₁ ²  +  2 b x ₁ x ₂  +  c x ₂ ²        b ²  <  a c
```

**旁白（繁中）**

> 由前兩條可以推出它對第二個變數也線性，所以半純量積就是一個對稱雙線性泛函，而它的二次形式 q 等於把兩個變數都放同一個向量，正定或半正定。這是第 2 章最後一節的語言，而定性這件事後果深遠。

**Narration (EN)**

> The first two conditions imply linearity in the second variable too, so a semiscalar product is a symmetric bilinear functional whose quadratic form, both variables set to the same vector, is positive definite or semidefinite. That is the language of the last section of chapter 2.

**動畫**

二次形式 q = 1 的水平集：一條傾斜的橢圓，也是用 r = 1 ／ 根號 q(方向) 算出來畫的。兩個軸上的交點標成 1 ／ √a 與 1 ／ √c。右側列出 b² < ac、q 在各方向的最小與最大值，以及把 b 改成 2.0 之後 q 變負的那個值。

## Beat 4 — 定理 1.1：Schwarz 不等式 / theorem 1.1: the Schwarz inequality
*配音長度：中文 17.3s ／ 英文 19.9s*

**畫面公式**

```
定理 1.1：Schwarz 不等式   |   theorem 1.1: the Schwarz inequality
| ( ξ , η ) |    ≤    √ ( ξ , ξ )  ·  √ ( η , η )
```

**旁白（繁中）**

> 定理 1.1，Schwarz 不等式：內積的絕對值不超過兩個自內積的平方根之積，對半純量積也成立。證明是把 ξ 減 t η 的自內積展開——那是不變號的二次式，判別式就不能是正的。

**Narration (EN)**

> Theorem 1.1 is the Schwarz inequality, valid for any semiscalar product: the product of two vectors is at most the square roots of their self-products. Expand the self-product of the first minus t times the second: that quadratic never changes sign, so its discriminant is not positive.

**動畫**

q(t) = (ξ − tη, ξ − tη) 的圖：一條開口向上的拋物線，最低點 0.0203 標在上方。它從來不碰 t 軸——這就是「判別式不能是正的」。

## Beat 5 — 同一個二次式的第二種讀法 / the same quadratic, read a second way
*配音長度：中文 17.8s ／ 英文 19.2s*

**畫面公式**

```
同一個二次式的第二種讀法   |   the same quadratic, read a second way
q ( t )  =  ( ξ − t η , ξ − t η )  ≥  0            t *  =  ( ξ , η ) / ( η , η )
```

**旁白（繁中）**

> 也可以直接算。如果 η 的自內積是正的，把 t 代成內積除以它，二次式就化簡成 Schwarz。如果 η 的自內積是零，那內積也必須是零，否則剛才那個不等式對某些 t 明顯不成立。

**Narration (EN)**

> One can also proceed directly. If the second self-product is positive, substituting the ratio for t simplifies the quadratic inequality into Schwarz. If it is zero, the product must be zero too, since otherwise the starting inequality fails for some t, and the conclusion is trivial.

**動畫**

同一張圖上兩條拋物線：青綠那對（t 與 e^t）最低點 0.0203，紫色那對（t 與 1 − t）最低點 0.2500，各自用虛線標出 t 星的位置。

## Beat 6 — 推論：那個平方根是範數 / the corollary: that square root is a norm
*配音長度：中文 19.5s ／ 英文 17.3s*

**畫面公式**

```
推論：那個平方根是範數   |   the corollary: that square root is a norm
‖ ξ ‖  =  √ ( ξ , ξ )            ‖ ξ + η ‖   ≤   ‖ ξ ‖  +  ‖ η ‖
```

**旁白（繁中）**

> 推論：純量積正定的時候，自內積的平方根是一個範數。三角不等式就是把和的平方展開，再用 Schwarz 換掉中間那一項；齊次性直接算。而 Schwarz 換句話說就是：這個雙線性泛函的界是一。

**Narration (EN)**

> The corollary: when the product is positive definite, the square root of the self-product is a norm. The triangle inequality is the expansion of the square of a sum with Schwarz applied to the middle term. Schwarz now just says the bilinear functional is bounded by one.

**動畫**

平面上的三角形：ξ（青綠）、從 ξ 的頭接出去的 η（紫）、以及 ξ + η（黃）。三邊長算出來是 2.0616 ≤ 1.2369 + 1.0770。右側是同一個不等式在連續函數空間裡的兩列數字。

## Beat 7 — pre-Hilbert 與 Hilbert / pre-Hilbert and Hilbert
*配音長度：中文 15.3s ／ 英文 17.5s*

**畫面公式**

```
pre-Hilbert 與 Hilbert   |   pre-Hilbert and Hilbert
‖ f ₙ  −  k ‖ ₂   →   0            dim V  <  ∞    ⇒    Hilbert
```

**旁白（繁中）**

> 範數這樣來的空間叫 pre-Hilbert 空間，完備的叫 Hilbert 空間；ℝⁿ 配這個範數就是歐氏 n 維空間。有限維一定完備所以一定是 Hilbert，可是連續函數配 two-norm 不完備。

**Narration (EN)**

> A normed space whose norm arises this way is a pre-Hilbert space, a complete one a Hilbert space, and real n-space under this norm is Euclidean n-space. Finite dimension forces completeness, so it always means Hilbert; the continuous functions are not.

**動畫**

階梯函數 k（青綠，中間跳一階）與三條寬度 1／n 的連續斜坡（n = 2、4、8）。右側列出 ‖ f n − k ‖ ₂ = 0.2041、0.1443、0.1021、0.0722。

## Beat 8 — 正交，以及純量積定出的夾角 / orthogonality, and the angle it defines
*配音長度：中文 17.7s ／ 英文 17.3s*

**畫面公式**

```
正交，以及純量積定出的夾角   |   orthogonality, and the angle it defines
( α , β )  =  0            ( ξ , η )  =  ‖ ξ ‖  ‖ η ‖  cos θ
```

**旁白（繁中）**

> 讓這套理論有味道的是正交：內積為零就說兩個向量垂直。靈感來自幾何——餘弦定理給出內積等於兩個長度乘上夾角的餘弦，所以可以照這樣定義夾角，不過書上說這門課用不到。

**Narration (EN)**

> What gives the theory its flavour is orthogonality: two vectors are orthogonal when their product is zero. The inspiration is geometric, since the law of cosines gives the product as the two lengths times the cosine of the angle, so one could define angles in general.

**動畫**

三對箭頭，夾角分別是 14.29°、60.00°、90.00°，每一對之間畫一段弧。箭頭只表示方向，長度沒有照比例；夾角是從純量積算出來的。

## Beat 9 — 引理 1.1：正交補是閉子空間 / lemma 1.1: the complement is closed
*配音長度：中文 18.8s ／ 英文 18.0s*

**畫面公式**

```
引理 1.1：正交補是閉子空間   |   lemma 1.1: the complement is closed
β  ⊥  A    ⇒    β  ⊥  L ( A ) ‾            A ⊥   =   { β  :  β ⊥ A }
```

**旁白（繁中）**

> 引理 1.1：如果 β 垂直集合 A，它就垂直 A 的線性包的閉包。理由是純量積對一個變數既線性又連續。於是任何子集的正交補都是閉子空間——「垂直」這個條件在取極限之下不會壞掉。

**Narration (EN)**

> Lemma 1.1: if a vector is orthogonal to a set, it is orthogonal to the closure of the linear span of that set. The reason is that the scalar product is both linear and continuous in one variable. So the orthogonal complement of any subset is a closed subspace.

**動畫**

[0, π] 上的四條正弦曲線 s ₁ 到 s ₄，s ₄ 用紅色加粗。右側列出 s ₄ 與 c ₁ s ₁ + c ₂ s ₂ 四組係數的內積，全部是 1e-15 等級，以及 (s ᵢ , s ᵢ) = 1.5708。

## Beat 10 — 引理 1.2 與推論 / lemma 1.2, and the corollary
*配音長度：中文 21.7s ／ 英文 19.2s*

**畫面公式**

```
引理 1.2 與推論   |   lemma 1.2, and the corollary
‖ α + β ‖ ²  +  ‖ α − β ‖ ²    =    2 ( ‖ α ‖ ²  +  ‖ β ‖ ² )
```

**旁白（繁中）**

> 引理 1.2：平行四邊形法則，以及畢氏定理——α 垂直 β 的充要條件就是和的平方等於兩個平方的和。彼此正交的一族也一樣，交叉項全部消掉。推論：有限多個彼此正交的非零向量必獨立，正交子空間也獨立。

**Narration (EN)**

> Lemma 1.2: the parallelogram law, and the Pythagorean theorem, which says two vectors are orthogonal exactly when the square of their sum splits. The same holds for an orthogonal family, the mixed terms all dropping out. The corollary: orthogonal nonzero vectors are independent.

**動畫**

平面上的平行四邊形：α（青綠）、β（紫）、α + β（黃）、α − β（紅，從原點畫出的同一個向量）。右側六列：四種範數各自的平行四邊形法則兩邊，以及正交族的 ‖ Σ x ᵢ s ᵢ ‖ ² = Σ x ᵢ ² ‖ s ᵢ ‖ ²。
