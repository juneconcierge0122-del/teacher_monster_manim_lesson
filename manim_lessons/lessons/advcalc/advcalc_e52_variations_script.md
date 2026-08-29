# advcalc E52 — 第 3 章：變分法

Chapter 3: The Calculus of Variations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 15 節「變分法」（書頁 182–185）。**這一節整節沒有習題**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e52_variations.py`（`AdvCalcE52ZH` / `AdvCalcE52EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[52]` / `FORMULAS_ADVCALC[52]`）
- 配音：`manim_lessons/samples/audio_e52/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.22 分（193 秒）／英文 3.06 分（184 秒）

## 第一變分，用兩種算法算過

變分問題就是臨界點問題，只是定義域是一個無窮維的弧空間。這一集的核心是第一變分那條公式，
而它是驗過的，不是宣告的：

- **兩種算法，同一個數字**：取弧長泛函與端點 (0,0)、(1,2)，在一條**不是解**的弧上
  （直線加上 0.30 倍的正弦），把第一變分算兩次——一次是泛函沿 h 的差商，
  一次是定理給的那個積分——兩個都是 **0.162160**，六位小數相同。
  **而且刻意選在非解的弧上算**：在解上兩邊都是零，那樣什麼都驗不出來。
- **解上確實是零**：同樣的差商在直線上算出來是 −7.9 × 10⁻⁹。
- **Euler 殘差**：在直線上是 0，在擾動過的弧上是 0.4522。
- **Du Bois-Reymond 那一步也驗過**：`∂F/∂y` 沿直線的變化幅度小於 10⁻⁶（是常數），
  沿擾動弧則大於 0.05（不是常數）——常數這件事正是那一步的結論。
- **四條擾動弧都量過**，每一條都比直線長。這不是證明，可是它確認方向沒有搞反。

probe 幀抓到三處：beat 6 的刪除線畫在兩列之間、什麼都沒劃到；
beat 9 的表頭建好了卻沒有傳進 `_table`（整列標題不見）；beats 0 與 2 的示意弧
用了跟第 9 拍量測時一樣小的振幅，三條糊成一條。
另外 `collide.py` 會把「故意畫上去的刪除線」也算成碰撞，所以那一步改成在左邊空白處打一個叉。

---

## Beat 0 — 臨界點問題，只是定義域無窮維 / a critical-point problem, in infinite dimensions
*配音長度：中文 18.3s ／ 英文 19.1s*

**畫面公式**

```
臨界點問題，只是定義域無窮維   |   a critical-point problem, in infinite dimensions
G ( f )    =    ∫ ₐ ᵇ  F ( f ( t ) ,  f ′ ( t ) ,  t )   d t
```

**旁白（繁中）**

> 第 15 節講變分法。書上的說法很直接：變分問題就是臨界點問題，只是定義域是一個無窮維的空間，而且用「微分等於零」的方式帶了一個特別的轉折。這一節只證一條標準定理。

**Narration (EN)**

> Section 15 is the calculus of variations. The book's line is blunt: variational problems are simply critical-point problems, with the domain an infinite-dimensional space and one characteristic twist in how the vanishing of the differential is used. One standard theorem is proved.

**動畫**

左邊一組固定端點之間的候選弧（直線加上下兩條擾動的）。
右側說明這是一個臨界點問題，只是定義域無窮維。

## Beat 1 — 約束是一個閉平面 / the constraint is a closed plane
*配音長度：中文 19.7s ／ 英文 17.2s*

**畫面公式**

```
約束是一個閉平面   |   the constraint is a closed plane
S  =  M  +  α                    dF ᵦ ↾ M    =    0
```

**旁白（繁中）**

> 有約束的極值本來要一個更一般的乘子定理，可是這裡不必。約束是一個閉平面，也就是某個子空間平移過去的。限制上去的函數就是子空間上的函數，所以條件只是微分在那個子空間上等於零。

**Narration (EN)**

> A constrained maximum would in general want a more general multiplier theorem, but not here. The constraint set is a closed plane, a subspace translated. Restricting to it gives a function on that subspace, so the condition is just that the differential vanish on the subspace.

**動畫**

左邊兩條斜線（下面灰色的 M、上面紅色的 S = M + α）與一支標 α 的箭頭。
右側說明約束是一個閉平面。

## Beat 2 — 弧的空間 / the space of arcs
*配音長度：中文 18.0s ／ 英文 17.9s*

**畫面公式**

```
弧的空間   |   the space of arcs
V  =  C ¹ ( [ a , b ] , W )            ‖ f ‖  =  ‖ f ‖ ∞  +  ‖ f ′ ‖ ∞
```

**旁白（繁中）**

> 設定：F 是三個變數的實值函數，第三個是時間。V 是區間上連續可微的弧構成的空間，範數取函數與導數兩個上確界之和。要極大化的是那個積分，而且兩個端點固定。

**Narration (EN)**

> The setup: F is a real-valued function of three variables, the third of them time. V is the space of continuously differentiable arcs on an interval, normed by the two uniform norms added. The functional to maximize is the integral, with both endpoints held fixed.

**動畫**

左邊四條弧，右側是 V 的定義與那個範數。
說明導數也要算進範數。

## Beat 3 — 泛函為什麼可微 / why the functional is differentiable
*配音長度：中文 17.8s ／ 英文 17.0s*

**畫面公式**

```
泛函為什麼可微   |   why the functional is differentiable
K ( f , g )    =    ∫ ₐ ᵇ  F ( f , g , t )   d t
```

**旁白（繁中）**

> 先要證那個泛函可微。用的正是上一集的定理 14.3：把 F 接上去是一個可微的映射，而積分是一個有界線性泛函，它的微分就是它自己。合成規則一套，泛函就可微了。

**Narration (EN)**

> First the functional has to be shown differentiable, and that uses the previous episode's Theorem 14.3: composing with F is a differentiable map, while integration is a bounded linear functional and so is its own differential. The composite rule then does it.

**動畫**

左邊兩個加框的映射（接上 F、積分），一支箭頭之後是加框的 K。
右側說明合成規則一套，泛函就可微了。

## Beat 4 — 第一變分 / the first variation
*配音長度：中文 14.6s ／ 英文 14.6s*

**畫面公式**

```
第一變分   |   the first variation
dG ( h )    =    ∫ ₐ ᵇ  [ dF ¹ ( h )  +  dF ² ( h ′ ) ]   d t
```

**旁白（繁中）**

> 得到的就是第一變分：把 h 送到那個積分，被積函數是兩個偏微分各配一支——一支配 h，一支配 h 的導數。這正是上一集最後那個乘積版本的公式。

**Narration (EN)**

> What comes out is the first variation: h goes to that integral, whose integrand is one partial differential for h and another for the derivative of h. That is exactly the product version of the formula the last episode closed with.

**動畫**

左邊一個加框的第一變分公式，下面一張表列出兩種算法的數值。
兩個數字六位小數相同。

## Beat 5 — 兩端釘住的那些 h / the h that are pinned at both ends
*配音長度：中文 18.7s ／ 英文 17.3s*

**畫面公式**

```
兩端釘住的那些 h   |   the h that are pinned at both ends
M  =  { h ∈ V  :  h ( a ) = h ( b ) = 0 }              dG ( h )  =  0
```

**旁白（繁中）**

> 端點固定給出一個閉平面：兩個取值映射都是有界的，交出來就是那個平面。它是子空間 M 的平移，而 M 裡的弧兩端都是零。於是臨界點的條件是：第一變分對 M 裡每一個 h 都等於零。

**Narration (EN)**

> Fixed endpoints give a closed plane: both evaluation maps are bounded and the plane is where they meet. It is a translate of the subspace of arcs vanishing at both ends, so the critical-point condition is that the first variation vanish for every h in that subspace.

**動畫**

左邊灰色的候選弧，加上三條兩端釘住的彩色弧。
右側說明臨界點就是對每一個這樣的 h 第一變分都是零。

## Beat 6 — 分部積分，端點項消掉 / integrate by parts and the endpoint term goes
*配音長度：中文 14.4s ／ 英文 13.9s*

**畫面公式**

```
分部積分，端點項消掉   |   integrate by parts and the endpoint term goes
∫ ₐ ᵇ  ( ∂F / ∂y   −   ∫ ∂F / ∂x )  g    =    0                g  =  h ′
```

**旁白（繁中）**

> 接下來是變分法的招牌手法，叫 Du Bois-Reymond 引理。把積分裡的第一項分部積分，端點的項因為 h 兩端是零而消掉，剩下的整個式子只剩下 h 的導數。

**Narration (EN)**

> Now the trademark trick, the lemma of Du Bois-Reymond. Integrate the first term of the integral by parts; the endpoint term drops because h vanishes at both ends, and what is left involves only the derivative of h.

**動畫**

左邊三行分部積分的式子，端點那一行左邊打一個紅色的叉。
右側說明端點項因為 h 兩端是零而消掉。

## Beat 7 — 只受一個限制，所以只能是常數 / one constraint only, so it is constant
*配音長度：中文 17.8s ／ 英文 16.3s*

**畫面公式**

```
只受一個限制，所以只能是常數   |   one constraint only, so it is constant
∫ ₐ ᵇ  g  =  0        ⇒        ∂F / ∂y   =   ∫ ₀ ᵗ  ∂F / ∂x   d s   +   C
```

**旁白（繁中）**

> 而 h 的導數是任意的連續函數，唯一的限制是它的積分為零。也就是說剩下那個東西正交於那個線性泛函的零空間，而零空間的正交補是一維的常數函數。所以它只能是常數。

**Narration (EN)**

> But the derivative of h is an arbitrary continuous function subject only to having integral zero. So what is left is orthogonal to the null space of that functional, and the orthogonal complement is the one-dimensional space of constants. It can only be a constant.

**動畫**

左邊三行推理，下面一個加框的常數式。
右側說明那個零空間的正交補是一維的常數。

## Beat 8 — Euler 方程 / the Euler equation
*配音長度：中文 18.1s ／ 英文 17.1s*

**畫面公式**

```
Euler 方程   |   the Euler equation
d / d t    ∂F / ∂y        =        ∂F / ∂x
```

**旁白（繁中）**

> 把常數那條式子再微分一次，就得到 Euler 方程：F 對 y 的偏導數沿著弧的時間導數，等於 F 對 x 的偏導數。順帶還推出左邊真的可微——這件事本來看不出來，因為只假設了導數連續。

**Narration (EN)**

> Differentiating the constant identity once more gives the Euler equation: the time derivative of the partial in y equals the partial in x. It also shows the left side really is differentiable, which was not apparent, since only continuity of the derivative was assumed.

**動畫**

左邊一個加框的 Euler 方程與它的展開式，下面一張殘差表。
在解上是零，在擾動過的弧上不是。

## Beat 9 — 例子：兩點之間最短的路 / an example: the shortest path
*配音長度：中文 19.8s ／ 英文 16.5s*

**畫面公式**

```
例子：兩點之間最短的路   |   an example: the shortest path
F  =  √ ( 1 + y ² )          ∂F / ∂x  =  0          ⇒          f ″  =  0
```

**旁白（繁中）**

> 一個算得出來的例子：兩點之間的最短路徑。被積函數是根號一加導數平方，對 x 的偏導數是零，所以 Euler 方程說對 y 的偏導數是常數，導數也是常數——直線。程式把幾條擾動過的弧都量過。

**Narration (EN)**

> A computable example: the shortest path between two points. The integrand is the root of one plus the derivative squared, its partial in x vanishes, so Euler makes the derivative constant, hence a straight line. Perturbed arcs are measured here as a check.

**動畫**

左邊直線加四條擾動過的弧，右邊一張 ε 與長度的表。
每一條擾動弧都比直線長。

## Beat 10 — 端點不固定時多兩個條件 / free endpoints add two conditions
*配音長度：中文 15.9s ／ 英文 16.9s*

**畫面公式**

```
端點不固定時多兩個條件   |   free endpoints add two conditions
∂F / ∂y  ( a )      =      ∂F / ∂y  ( b )      =      0
```

**旁白（繁中）**

> 如果端點不固定，h 就跑遍整個 V，分部積分留下的端點項不再消失。結論是 Euler 方程照樣成立，另外還要加上兩個端點條件：F 對 y 的偏導數在兩端都等於零。

**Narration (EN)**

> With the endpoints not fixed, h ranges over the whole space and the endpoint term from the integration by parts no longer drops. The conclusion is that the Euler equation still holds, together with two endpoint conditions: the partial in y vanishes at each end.

**動畫**

左邊兩條端點不固定的弧，右側四行說明多出來的兩個端點條件。

---

## 為什麼要在「不是解」的弧上驗

第一變分那條公式如果只在解上驗，兩邊都是零，等式自動成立——那樣驗不出公式對不對。
所以第 5 拍算的是一條刻意偏離的弧，兩邊都是 0.162160，離零很遠。
解上的零則另外驗了一次，那是第 9 拍那條直線。

## 這一節留下的問題

Euler 方程給的是臨界點，不是極大或極小。要判斷是哪一種，得看第二變分——
也就是泛函的二階微分。那正是下一節的主題，而下一集就從二階微分講起。
端點既不固定也不完全自由的情形，書上留到第 13 章講力學時才處理。
