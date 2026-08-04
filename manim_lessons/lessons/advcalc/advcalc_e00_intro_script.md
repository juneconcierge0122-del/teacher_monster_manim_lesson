# advcalc E00 — 《高等微積分》導論：這本書是什麼

Advanced Calculus: What This Book Is

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990（原版 Addison-Wesley, 1968）。取材自書前的序言與目錄。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e00_intro.py`（`AdvCalcE00ZH` / `AdvCalcE00EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[0]` / `FORMULAS_ADVCALC[0]`）
- 配音：`manim_lessons/samples/audio_e00/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.37 分（202 秒）／英文 3.06 分（184 秒）

---

## Beat 0 — 哈佛榮譽班的講義 / notes from an honors course at Harvard
*配音長度：中文 21.0s ／ 英文 15.0s*

**畫面公式**

```
哈佛榮譽班的講義   |   notes from an honors course at Harvard
Loomis  ·  Sternberg      Harvard      1968  /  1990
```

**旁白（繁中）**

> 這本書封面寫著高等微積分，但它不是一般大學裡那門算偏導數與重積分的課。作者是 Loomis 與 Sternberg，兩位哈佛大學數學系的教授；書的內容來自他們在一九六零年代開的榮譽班，一九六八年出版，一九九零年出了修訂版。

**Narration (EN)**

> The cover says Advanced Calculus, but this is not the usual course in partial derivatives and multiple integrals. It is by Loomis and Sternberg, both of the Harvard mathematics department, and it grew out of an honors course they gave in the nineteen sixties.

**動畫**

章節帶（14 格，第 0 到 13 章）淡入，中央是代表本書的卡片。

## Beat 1 — 先修條件 / the prerequisites
*配音長度：中文 19.1s ／ 英文 17.0s*

**畫面公式**

```
先修條件   |   the prerequisites
f : ℝ → ℝ  ,  lim  ,  ϵ – δ        +        V  ,  dim V  ,  A x = b
```

**旁白（繁中）**

> 序言把門檻寫得很清楚。你需要嚴格觀點下的單變數微積分，還要一些線性代數，要熟悉極限與連續這類論證，並且對偏導數有一點經驗。作者建議的入門書是 Courant、Apostol、Spivak 與 Hardy。

**Narration (EN)**

> The preface states the prerequisites plainly. You need one variable calculus from a rigorous point of view, some linear algebra, comfort with limit and continuity arguments, and a little experience with partial derivatives. It suggests Courant, Apostol, Spivak and Hardy.

**動畫**

左側兩個先修條件標籤，箭頭指進書卡。卡片刻意縮小到 3.90 寬，好留出箭頭空間——`_arr` 在長度小於 0.05 時會回傳空 VGroup 而且不報錯。

## Beat 2 — 前半：賦範向量空間　　後半：流形 / first half: normed vector spaces / second half: manifolds
*配音長度：中文 19.4s ／ 英文 16.9s*

**畫面公式**

```
前半：賦範向量空間　　後半：流形   |   first half: normed vector spaces / second half: manifolds
Ch 1 – 8 :  ‖ · ‖          Ch 9 – 13 :  M
```

**旁白（繁中）**

> 全書大致分成兩半。前半把微分學整個建立在賦範向量空間上，後半處理可微流形上的微積分。這個安排決定了整本書的風格：先把空間本身的結構講清楚，再談在上面怎麼做微分與積分。

**Narration (EN)**

> The book divides roughly in half. The first half develops the calculus entirely in the setting of normed vector spaces. The second half deals with the calculus of differentiable manifolds. The structure of the space comes first, and doing calculus on it comes second.

**動畫**

章節帶上方畫出兩段虛線括號：第 0 到 11 章是一個邏輯整體，第 12、13 章獨立。說明文字放在 y = −0.72，離括號橫桿（−1.16）0.44，避免壓線。

## Beat 3 — 微分是最接近的那個線性逼近 / the differential is the closest linear approximation
*配音長度：中文 20.5s ／ 英文 16.8s*

**畫面公式**

```
微分是最接近的那個線性逼近   |   the differential is the closest linear approximation
ΔF ( ξ )  =  dF ( ξ )  +  𝒪 ( ξ )        dF  ∈  Hom ( V , W )
```

**旁白（繁中）**

> 核心的觀念轉換在這裡。在初等微積分裡，導數是一個數，是切線的斜率。在這本書裡，微分是一個線性映射，是最接近真實變化量的那一個線性逼近；它與真實變化的差，比位移本身還要小一個等級。

**Narration (EN)**

> Here is the central shift. In elementary calculus the derivative is a number, the slope of the tangent line. Here the differential is a linear map, the one linear approximation closest to the actual change, and the gap between them is of smaller order than the displacement.

**動畫**

書卡與括號淡出，中央換成課本 Fig. 3.8（書頁 141）：曲線是真實變化，直線是切線，紅色箭頭是兩者的差。三個名稱改放右側圖例欄——放在線旁邊時 df、Δf、𝒪(t) 會全部擠在 a+t 上方互相重疊。

## Beat 4 — 代數的準備 / algebraic preparation
*配音長度：中文 17.0s ／ 英文 17.8s*

**畫面公式**

```
代數的準備   |   algebraic preparation
Ch 0 :  ∀  ∃  ∈          Ch 1 – 2 :  V , V* , A
```

**旁白（繁中）**

> 第零章到第二章是代數的準備。第零章講邏輯、量詞與集合，作者說這章主要是給人回頭查閱用的；第一章與第二章建立向量空間、對偶空間、矩陣、跡與行列式。

**Narration (EN)**

> Chapters zero through two are algebraic preparation. Chapter zero covers logic, quantifiers and sets, and the authors say it is mainly there to be referred back to. Chapters one and two build vector spaces, the dual space, matrices, trace and determinant.

**動畫**

highlight 框移到第 0 到 2 格，中央列出該章群的四個重點。

## Beat 5 — 微分學本身 / the differential calculus itself
*配音長度：中文 17.1s ／ 英文 16.2s*

**畫面公式**

```
微分學本身   |   the differential calculus itself
Ch 3 :  ‖ · ‖  →  dF  →  F ( x , y ) = 0
```

**旁白（繁中）**

> 第三章是全書前半的重心，微分學本身。從範數與連續性開始，經過無窮小的三個類、微分、方向導數與均值定理，一路走到隱函數定理、子流形與拉格朗日乘子。

**Narration (EN)**

> Chapter three is the heart of the first half, the differential calculus itself. It starts from norms and continuity, passes through infinitesimals, the differential, directional derivatives and the mean value theorem, and reaches the implicit function theorem.

**動畫**

highlight 移到第 3 格（全書前半的重心）。

## Beat 6 — 分析的地基，與第一批應用 / analytic groundwork, and the first applications
*配音長度：中文 16.9s ／ 英文 17.1s*

**畫面公式**

```
分析的地基，與第一批應用   |   analytic groundwork, and the first applications
Ch 4 :  T ( x ) = x        Ch 5 :  ( α , β )        Ch 6 :  dx / dt = F
```

**旁白（繁中）**

> 第四章補上分析需要的地基：度量空間、緊緻性、完備性，還有壓縮映射不動點定理。第五章處理純量積空間，第六章把前面的工具用在微分方程與傅立葉級數上。

**Narration (EN)**

> Chapter four lays the analytic groundwork: metric spaces, compactness, completeness, and the contraction mapping fixed point theorem. Chapter five treats scalar product spaces, and chapter six turns those tools on differential equations and Fourier series.

**動畫**

highlight 移到第 4 到 6 格。

## Beat 7 — 多重線性代數與積分 / multilinear algebra and integration
*配音長度：中文 16.4s ／ 英文 16.4s*

**畫面公式**

```
多重線性代數與積分   |   multilinear algebra and integration
Ch 7 :  Λ V*  ,  det          Ch 8 :  ∫
```

**旁白（繁中）**

> 第七章是多重線性代數，交錯張量、行列式與外代數；作者自己說這章主要當作後面各章的參考。第八章建立黎曼積分的公理化理論，其中包含變數變換公式。

**Narration (EN)**

> Chapter seven is multilinear algebra, with alternating tensors, the determinant and the exterior algebra; the authors call it a reference chapter. Chapter eight builds the axiomatic theory of Riemann integration, including the change of variables formula.

**動畫**

highlight 移到第 7 到 8 格。

## Beat 8 — 流形上的微積分 / calculus on manifolds
*配音長度：中文 21.0s ／ 英文 17.5s*

**畫面公式**

```
流形上的微積分   |   calculus on manifolds
Ch 9 – 11 :  Tₚ M  ,  d          ∫ dω  =  ∫ ω
```

**旁白（繁中）**

> 第九章到第十一章是後半的主線。可微流形、切空間、向量場與李導數，接著是流形上的積分、單位分割與散度定理，最後匯集到外微積分與斯托克斯定理。序言提醒，第九章是學生最難吸收的一章。

**Narration (EN)**

> Chapters nine through eleven carry the second half: manifolds, the tangent space, vector fields and Lie derivatives, then integration on manifolds and the divergence theorem, and finally exterior calculus and Stokes theorem. The preface warns that chapter nine is the hardest.

**動畫**

highlight 移到第 9 到 11 格。

## Beat 9 — 兩章互相獨立的應用 / two independent applications
*配音長度：中文 18.2s ／ 英文 16.8s*

**畫面公式**

```
兩章互相獨立的應用   |   two independent applications
Ch 12 :  Δu = 0          Ch 13 :  T* ( M )  ,  ω = dθ
```

**旁白（繁中）**

> 第十二章與第十三章彼此獨立，是示範性質的應用。前者是位勢論，包含格林公式、卜瓦松積分與狄利克雷問題；後者用辛幾何重講一次古典力學，從餘切叢一路做到正則變換。

**Narration (EN)**

> Chapters twelve and thirteen are independent of each other and serve as illustrative applications. The first is potential theory, with Green's formulas, the Poisson integral and Dirichlet's problem. The second redoes classical mechanics using symplectic geometry.

**動畫**

highlight 移到第 12 到 13 格。

## Beat 10 — 這個系列的計畫 / the plan for this series
*配音長度：中文 15.6s ／ 英文 16.1s*

**畫面公式**

```
這個系列的計畫   |   the plan for this series
169  ·  2 – 4 pp / ep  ·  Ch 0 § 1 – 3
```

**旁白（繁中）**

> 這個系列會照著書的順序走，大約兩到四個書頁做成一集，加星號的進階節也不跳過，全書預計一百六十九集。下一集從第零章開始，講邏輯與量詞。

**Narration (EN)**

> This series follows the book in order, at roughly two to four printed pages per episode, and it does not skip the starred advanced sections. That comes to about one hundred and sixty nine episodes. The next one starts at chapter zero, with logic and quantifiers.

**動畫**

highlight 淡出，中央換成本系列的製作計畫與下一集預告。
