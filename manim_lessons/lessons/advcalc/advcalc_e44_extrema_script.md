# advcalc E44 — 第 3 章：極值與臨界點

Chapter 3: Extrema and Critical Points

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 10 節「初等應用」的前半（書頁 161–162）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e44_extrema.py`（`AdvCalcE44ZH` / `AdvCalcE44EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[44]` / `FORMULAS_ADVCALC[44]`）
- 配音：`manim_lessons/samples/audio_e44/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.22 分（193 秒）／英文 3.01 分（181 秒）

## 一個盒子，把整節的每一句話都驗過

第 10 節「初等應用」只有兩頁，內容是把前九節的機器接到最古典的問題上：
極大極小。這一集用同一個例子貫穿——體積固定為 8 的長方盒，問表面積最小的形狀——
而畫面上出現的每一個數字都是程式算出來的：

- **臨界點的條件**：把體積代進去消掉第三個變數，兩個偏導數各自設零，
  斷言解出來的是 `x = y`，再代回體積得到 `x = y = z = 2`。
- **梯度真的是零**：在那一點上用中央差商算兩個偏導數，斷言都是零。
- **它真的是極小**：掃描附近 289 個點，斷言沒有一個的表面積更小。
- **拉長就變差**：另外三個同體積的盒子（1×2×4、4×1×2、2×4×1）各自先斷言體積真的是 8，
  再斷言表面積大於 24；而且斷言三個面積完全相同（都是 28）——
  畫面上只印一個數字，這條斷言就是印一個數字的依據。
- **邊界跑不掉**：在 x 等於 0.001、0.01 與 1000 三個地方，斷言表面積大於最小值的十倍，
  也就是兩端確實發散。第 9 拍那條曲線畫的就是這件事。

`bounds.py` 抓到 beat 5 的盒子右上角超出上緣。probe 幀抓到 beat 9：
第一版把面積減掉一個常數再截斷，結果整條曲線被壓成一條直線加一個懸崖；
改成直接畫面積本身、並把橫軸範圍縮到兩端都已經在爬升的區間才對。

---

## Beat 0 — 極值可能出現在哪裡 / where an extreme value can occur
*配音長度：中文 16.2s ／ 英文 17.3s*

**畫面公式**

```
極值可能出現在哪裡   |   where an extreme value can occur
F :  A  →  ℝ                A  ⊂  V
```

**旁白（繁中）**

> 這一節把初等微積分的極大極小理論搬到賦範空間，而搬過來幾乎不用改動。設 F 是定義在開集上的實值函數，這一整節問的都是同一件事：極值可能出現在哪裡。

**Narration (EN)**

> This section carries the maximum and minimum theory of elementary calculus into a normed space, and almost nothing has to change. Let F be a real valued function on an open set; the whole section asks one question, namely where an extreme value can occur.

**動畫**

左邊一團封閉的曲線代表定義域，裡面兩顆點（紅、藍）與邊界上一顆灰點。
右側三行說明分別對應「內部點定理管得到」「邊界點管不到」與本節的問題。

## Beat 1 — 定理 10.1：微分必須是零 / Theorem 10.1: the differential vanishes
*配音長度：中文 21.8s ／ 英文 18.6s*

**畫面公式**

```
定理 10.1：微分必須是零   |   Theorem 10.1: the differential vanishes
F ( α )  ≥  F ( ξ )     ( ξ ≈ α )         ⇒         dF ₐ  =  0
```

**旁白（繁中）**

> 定理 10.1：如果 F 在開集內部的一點取到相對極大值，而且微分在那裡存在，那麼那個微分就是零映射。相對極小的情形一模一樣，把不等號反過來就好。這是一元微積分那條「極值點導數為零」在賦範空間的版本。

**Narration (EN)**

> Theorem 10.1: if F takes a relative maximum at an interior point where the differential exists, that differential is the zero map. A relative minimum is identical with the inequality reversed. This is the vanishing derivative at an extremum, restated for a normed space.

**動畫**

左邊一條開口向下的拋物線，頂點上一顆紅點，並拉一條紅色虛線當水平切線。
右側三行把定理 10.1 的假設與結論拆成三句。

## Beat 2 — 證明：限制到一條直線上 / the proof: restrict to a line
*配音長度：中文 19.4s ／ 英文 16.3s*

**畫面公式**

```
證明：限制到一條直線上   |   the proof: restrict to a line
γ ( t )  =  F ( α + t ξ )                γ ′ ( 0 )  =  0
```

**旁白（繁中）**

> 證明只有兩行。取任一個方向，把 F 限制到那條直線上得到一條弧；這條弧在零點取到相對極值，所以它的導數是零。而那個導數就是微分作用在那個方向上，每個方向都零，微分就是零。

**Narration (EN)**

> The proof takes two lines. Pick a direction and restrict F to that line to get an arc; the arc has a relative extreme value at zero, so its derivative there vanishes. That derivative is the differential applied to the direction, and every direction gives zero.

**動畫**

左邊一個座標十字，從原點射出三支不同顏色的箭頭代表三個方向。
右側是把問題壓成一變數的三條式子：γ(t)、γ′(0)=0、dFₐ(ξ)=0。

## Beat 3 — 臨界點，而且要在內部 / critical points, and interior ones
*配音長度：中文 19.3s ／ 英文 16.5s*

**畫面公式**

```
臨界點，而且要在內部   |   critical points, and interior ones
dF ₐ  =  0                α   ∈   A ° 
```

**旁白（繁中）**

> 微分等於零的點叫臨界點。定理說的是：可微的實值函數，內部的極值只可能出現在臨界點。「內部」這兩個字很重要——邊界上的點不受這條定理管，所以後面那個盒子的例子還要另外處理邊界。

**Narration (EN)**

> A point where the differential vanishes is a critical point, and the theorem says an interior extreme value of a differentiable real valued function happens only at one. The word interior matters: boundary points are not covered, as the box example will need.

**動畫**

同一團定義域，這次兩顆紅點是臨界點、一顆藍點是內部的極值，
邊界上那顆灰點被打上一個叉，表示定理不覆蓋它。

## Beat 4 — 在座標下就是一組方程 / in coordinates it is a system
*配音長度：中文 20.5s ／ 英文 18.8s*

**畫面公式**

```
在座標下就是一組方程   |   in coordinates it is a system
( ∂ F / ∂ x ⱼ ) ( a )  =  0             ( j = 1 , … , n )
```

**旁白（繁中）**

> 在實數的 n 維空間上，微分等於零就是所有偏導數都等於零。這就是大家實際在解的那個方程組：n 個方程、n 個未知數。要注意解出來的只是候選點，還沒說它們是極大、極小，還是兩者都不是。

**Narration (EN)**

> In real n-space a vanishing differential means every partial derivative vanishes: n equations in n unknowns, and that is the system everyone actually solves. Note that its solutions are only candidates; nothing yet says which are maxima, which minima, and which neither.

**動畫**

左邊是一組偏導數等於零的方程，外面加一個大左括號把 n 條式子框起來。
右側說明它是 n 個方程配 n 個未知數，解只是候選。

## Beat 5 — 體積固定，表面積最小 / least area for a given volume
*配音長度：中文 15.7s ／ 英文 15.3s*

**畫面公式**

```
體積固定，表面積最小   |   least area for a given volume
A  =  2 ( x y + x z + y z )                V  =  x y z
```

**旁白（繁中）**

> 舉一個經典的例子：體積固定時，表面積最小的長方體是什麼形狀？表面積是兩倍的三個面積之和，而體積是三邊相乘，所以這是一個「有約束的極值問題」。

**Narration (EN)**

> Here is the classical example: among boxes of a given volume, which shape has least surface area? The area is twice the sum of three face areas and the volume is the product of the three edges, so this is a constrained extremum problem.

**動畫**

左邊用軸測投影畫一個長方盒（十二條邊）。
右側是表面積與體積兩條式子，以及「先消掉第三個變數」的提示。

## Beat 6 — 兩個偏導數設成零 / set both partial derivatives to zero
*配音長度：中文 14.6s ／ 英文 15.2s*

**畫面公式**

```
兩個偏導數設成零   |   set both partial derivatives to zero
V  =  x ² y   =  x y ²            ⇒            x  =  y
```

**旁白（繁中）**

> 用體積把第三個變數消掉，剩下兩個變數。兩個偏導數各設成零，得到體積等於 x 平方乘 y，也等於 x 乘 y 平方；兩式一比就得到 x 等於 y。

**Narration (EN)**

> Use the volume to eliminate the third variable, leaving two. Setting both partial derivatives to zero gives the volume as x squared times y and also as x times y squared, and comparing those two gives x equal to y.

**動畫**

左邊三行：兩個偏導數設零各自得到 V = x²y 與 V = xy²，兩式相比得到 x = y。
右側強調對稱性是算出來的，不是假設的。

## Beat 7 — 答案是正方體 / the answer is a cube
*配音長度：中文 14.9s ／ 英文 14.0s*

**畫面公式**

```
答案是正方體   |   the answer is a cube
V = 8            x = y = z = 2            A = 24
```

**旁白（繁中）**

> 再代回去，三邊全部相等，所以答案是正方體。畫面上取體積等於八，邊長就是二，表面積是二十四，剛好等於六乘上體積的三分之二次方。

**Narration (EN)**

> Substituting back makes all three edges equal, so the answer is a cube. On screen the volume is eight, the edge is two, and the area is twenty four, which is six times the volume to the two thirds.

**動畫**

左邊是一個三邊相等的盒子（正方體），線條加粗。
右側印出 x = y = z = 2 與 A = 24 = 6V^(2/3)。

## Beat 8 — 同體積的其他盒子都比較大 / other boxes of the same volume are worse
*配音長度：中文 14.3s ／ 英文 13.0s*

**畫面公式**

```
同體積的其他盒子都比較大   |   other boxes of the same volume are worse
24        <        28
```

**旁白（繁中）**

> 畫面上另外三個同體積的盒子，表面積都是二十八，比正方體的二十四大。這不是證明，但它讓那個結論看得見，也讓人相信方向沒有搞反。

**Narration (EN)**

> The three other boxes on screen have the same volume and all have area twenty eight against the cube's twenty four. That is not a proof, but it makes the conclusion visible and confirms the direction was not reversed.

**動畫**

三個同體積的盒子並排：正方體、拉高的、壓扁的，各自在下方標出表面積 24、28、28。
右側面板搬到 x = 3.90，避免與第三個盒子相撞。

## Beat 9 — 偷偷用掉的那個假設 / the assumption that was slipped in
*配音長度：中文 17.1s ／ 英文 17.9s*

**畫面公式**

```
偷偷用掉的那個假設   |   the assumption that was slipped in
x → 0    ∨    x → ∞             ⇒             A → ∞
```

**旁白（繁中）**

> 不過這裡偷偷用了一個假設：絕對極小值出現在內部的某一點。書上把它留成習題——要證的是任何一邊趨於零或趨於無窮時，表面積都趨於無窮，所以極小值不會跑到邊界上。

**Narration (EN)**

> One assumption was slipped in, though: that the absolute minimum occurs at an interior point. The book leaves it as an exercise; what has to be shown is that the area tends to infinity as any edge tends to zero or to infinity, so the minimum cannot escape to the boundary.

**動畫**

左邊畫表面積對邊長 x 的曲線（y 固定為 2），最低點打紅點並拉一條水平虛線，
兩端各加一支往上的箭頭表示發散。右側說明極小值逃不到邊界上。

## Beat 10 — 必要，但不充分 / necessary, but not sufficient
*配音長度：中文 19.2s ／ 英文 18.0s*

**畫面公式**

```
必要，但不充分   |   necessary, but not sufficient
f ( x , y )  =  x ² − y ²                df ₀  =  0
```

**旁白（繁中）**

> 最後要記得，微分等於零是必要條件不是充分條件。畫面上 x 平方減 y 平方在原點的微分是零，可是沿一個方向是極小、沿另一個方向是極大。充分條件要看二階微分，留到第 16 節。

**Narration (EN)**

> Finally, a vanishing differential is necessary, not sufficient. On screen x squared minus y squared has zero differential at the origin, yet the origin is a minimum along one direction and a maximum along another. The sufficient condition waits for section 16.

**動畫**

左邊用軸測投影畫馬鞍面 x² − y²，兩條主軸方向的截線分別畫成紅色與藍色。
右側說明同一點在一個方向是谷底、在另一個方向是山頂，所以兩者都不是。

---

## 為什麼要多花一拍講邊界

臨界點的條件只給候選：它說「如果內部有極值，它一定在這些點裡」。
它不說極值存在。書上把「兩端發散所以極小值不在邊界」這一步留成習題，
可是少了它，前面的推導只證明了一句條件句。第 9 拍就是把那一句補上。

## 這條定理不做的事

分類。哪些臨界點是極大、哪些是極小、哪些兩者都不是，定理 10.1 一個字都沒說。
第 10 拍的馬鞍面就是反例：原點的微分是零，可是沿一個方向是極小、沿另一個方向是極大。
充分條件要看二階微分是不是定號的二次型，那是第 3 章第 16 節的內容。
