# advcalc E39 — 第 3 章：方向導數

Chapter 3: Directional Derivatives

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 7 節的前段（書頁 146–148）。書頁 151–152 是習題 7.1–7.15，均值定理留給 E40。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e39_directional.py`（`AdvCalcE39ZH` / `AdvCalcE39EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[39]` / `FORMULAS_ADVCALC[39]`）
- 配音：`manim_lessons/samples/audio_e39/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.25 分（195 秒）／英文 3.10 分（186 秒）

## 兩個映射貫串全集，每個方向導數都是量出來的

這一集用的第一個映射，就是 E38 講鏈鎖規則時那一個，所以它的雅可比矩陣已經眼熟；
第二個是書上自己給的最小反例。場景檔在 import 時把畫面宣稱的事全部算一遍：

- **每個方向導數都用中央差商算**，再斷言它等於雅可比矩陣乘上那個向量。三個方向都驗過。
- **beat 5 斷言「同一個方向、三個不同的導數」**：把 ξ 乘上 1、2、3，導數也乘上 1、2、3，
  而且斷言三個確實不同——這一拍的全部內容就是這件事。
- **beat 6 用一條真的彎的弧**（不是直線），斷言合成之後的切向量等於雅可比矩陣乘上原來的切向量，
  也就是定理 7.2。
- **反例驗了四件事**：齊次（三個方向、三個倍數）、每個方向導數等於函數在 ξ 的值、
  在原點連續（單位圓上的值不超過半徑）、以及**不可加**——`F(1,0) + F(0,1) = 1` 但 `F(1,1) = 0.5`。
  最後那一條是整個反例的支點，所以斷言差距要大於 0.4。

**beat 10 的圖改過一次。** 初稿把反例畫成極座標圖，可是 `cos³θ` 在 θ 過 90 度之後半徑變負，
點會翻到另一側，整條曲線變成同一個透鏡形被描兩遍，看不出在說什麼。改成直角座標：
畫 `F` 在單位圓上的值（藍），再疊上「如果它是線性的，該長什麼樣」的那條 `a cos θ + b sin θ`（紅）。
兩條在四個座標軸方向剛好重合（橘點），中間差距最大 0.38——那個差距就是不可加的量。

---

## Beat 0 — 從區間到賦範空間的函數 / a function from an interval into a normed space
*配音長度：中文 17.5s ／ 英文 16.7s*

**畫面公式**

```
從區間到賦範空間的函數   |   a function from an interval into a normed space
f ′ ( x )    =    lim ( t → 0 )   [ f ( x + t ) − f ( x ) ] / t
```

**旁白（繁中）**

> 這一節把微分接回一元微積分的導數。先看最簡單的情形：從一個區間映到賦範空間的連續函數。導數的定義一個字都不用改，還是差商取極限，只是分子現在是一個向量。

**Narration (EN)**

> This section connects the differential back to the derivative of one variable calculus. Start with the simplest case, a continuous function from an interval into a normed space. The definition of the derivative needs no change at all; the numerator is now a vector.

**動畫**

左邊一條實數線標著 x 與 x + t，右邊是那兩點的像與連起來的割線（橘色），中間一支標著 f 的箭頭。

## Beat 1 — 參數化弧與它的切向量 / a parametrized arc, and its tangent vector
*配音長度：中文 16.1s ／ 英文 14.5s*

**畫面公式**

```
參數化弧與它的切向量   |   a parametrized arc, and its tangent vector
γ : [ a , b ]  →  V              γ ′ ( x )  =  α
```

**旁白（繁中）**

> 這種函數的值域是一條曲線，習慣叫它參數化弧，而導數就叫弧在那一點的切向量。切向量存在，就說弧在那一點光滑；每一點都光滑，就說整條弧光滑。

**Narration (EN)**

> The range of such a function is a curve, conventionally called a parametrized arc, and the derivative is called the tangent vector to the arc at that point. If it exists the arc is smooth there, and an arc smooth at every point is called smooth.

**動畫**

同一條弧，加上在一點畫出的切向量（橘色箭頭）與另外三個點。

## Beat 2 — 定理 7.1：切向量就是骨架 / Theorem 7.1: the tangent vector is the skeleton
*配音長度：中文 17.5s ／ 英文 18.1s*

**畫面公式**

```
定理 7.1：切向量就是骨架   |   Theorem 7.1: the tangent vector is the skeleton
dγ ₓ ( h )    =    h · γ ′ ( x )    =    h α
```

**旁白（繁中）**

> 定理 7.1 把兩件事對上：弧在一點可微，恰好等於切向量在那一點存在，而且這時微分就是「乘上那個切向量」。切向量正是微分的骨架——一維的定義域讓微分退化成一個乘法。

**Narration (EN)**

> Theorem 7.1 matches the two up: the arc is differentiable at a point exactly when the tangent vector exists there, and the differential is then multiplication by that vector. The tangent vector is the skeleton, so a one dimensional domain collapses the differential to a product.

**動畫**

左邊一條 h 的實數線上兩個點，右邊是它們的像：同一個切向量的一倍與兩倍。

## Beat 3 — 一次只看一條直線 / one straight line at a time
*配音長度：中文 19.1s ／ 英文 16.5s*

**畫面公式**

```
一次只看一條直線   |   one straight line at a time
λ ( t )  =  α + t ξ              γ ( t )  =  F ( α + t ξ )
```

**旁白（繁中）**

> 接著是這一節的主角。要研究 F 在 α 附近的行為，一個辦法是每次只看一條穿過 α 的直線。取一個非零的 ξ，那條直線就是 t 對應到 α 加 t 乘 ξ，把 F 限制上去就得到一條參數化弧。

**Narration (EN)**

> Now the main object. To study F near alpha, one approach is to look at a single straight line through alpha at a time. Pick a nonzero xi; the line sends t to alpha plus t times xi, and restricting F to it produces a parametrized arc.

**動畫**

左邊 V 面板一條紫色直線穿過 α，右邊 W 面板是這條直線在 F 底下的像——一條彎的弧。

## Beat 4 — 方向導數的定義 / the directional derivative
*配音長度：中文 16.8s ／ 英文 17.6s*

**畫面公式**

```
方向導數的定義   |   the directional derivative
D ξ F ( α )   =   lim ( t → 0 )   [ F ( α + t ξ ) − F ( α ) ] / t
```

**旁白（繁中）**

> 這條弧在 t 等於零的切向量，如果存在，就叫 F 在 α 沿 ξ 的方向導數。寫出來還是那個差商：F 在 α 加 t 乘 ξ 的值，減掉 F 在 α 的值，除以 t，再讓 t 趨於零。

**Narration (EN)**

> The tangent vector of that arc at t equal to zero, if it exists, is called the derivative of F at alpha in the direction xi. Written out it is the same difference quotient: the value at alpha plus t xi minus the value at alpha, over t, as t goes to zero.

**動畫**

同一條弧，兩條割線（灰、紫）與極限的切向量（橘色）。

## Beat 5 — 「方向」其實用錯了字 / direction is the wrong word
*配音長度：中文 18.1s ／ 英文 17.3s*

**畫面公式**

```
「方向」其實用錯了字   |   direction is the wrong word
η = c ξ              D η F ( α )   =   c · D ξ F ( α )
```

**旁白（繁中）**

> 「方向」這個詞其實用錯了。把 ξ 乘上一個正數，指的方向沒變，可是方向導數會跟著乘上同一個數。真正成立的是：方向導數對 ξ 是線性的，畫面上那三個值就差一個倍數。

**Narration (EN)**

> The word direction is really a misuse. Scaling xi by a positive number does not change where it points, yet the directional derivative is scaled by the same factor. What actually holds is that it is linear in xi; the three values on screen differ by exactly that factor.

**動畫**

左邊一支箭頭上三顆點標著 ξ、2ξ、3ξ，右邊一支箭頭上三顆對應的點標著 1×、2×、3×。

## Beat 6 — 定理 7.2：沿光滑弧走還是光滑 / Theorem 7.2: smooth arcs stay smooth
*配音長度：中文 18.2s ／ 英文 16.7s*

**畫面公式**

```
定理 7.2：沿光滑弧走還是光滑   |   Theorem 7.2: smooth arcs stay smooth
γ  =  F ∘ λ              γ ′ ( x )  =  dF ₐ ( λ ′ ( x ) )
```

**旁白（繁中）**

> 定理 7.2 說：如果 F 在 α 可微，那麼沿任何一條穿過 α 的光滑弧走過去，得到的還是光滑弧，而且它的切向量就是把原來那條弧的切向量丟進微分裡。這只是鏈鎖規則換一個說法。

**Narration (EN)**

> Theorem 7.2 says that if F is differentiable at alpha then travelling along any smooth arc through alpha gives another smooth arc, whose tangent vector is the original tangent vector fed into the differential. That is the chain rule in different clothing.

**動畫**

左邊 V 裡一條彎的光滑弧與它的切向量，右邊 W 裡是它的像與像的切向量。

## Beat 7 — 微分可以一個方向一個方向讀 / the differential, one direction at a time
*配音長度：中文 16.5s ／ 英文 15.7s*

**畫面公式**

```
微分可以一個方向一個方向讀   |   the differential, one direction at a time
D ξ F ( α )    =    dF ₐ ( ξ )
```

**旁白（繁中）**

> 取直線當那條弧，就得到最常用的特例：每一個方向導數都存在，而且等於微分作用在 ξ 上。所以微分可以一個方向一個方向地讀出來，這也是實際計算時真正在做的事。

**Narration (EN)**

> Taking the arc to be a straight line gives the case everyone uses: every directional derivative exists and equals the differential applied to xi. So the differential can be read off one direction at a time, which is what computing it actually amounts to.

**動畫**

左邊三支不同方向的箭頭，右邊三支對應的像，中間是雅可比矩陣。

## Beat 8 — 齊次函數：限制到直線就是直線 / homogeneous: a line restricts to a line
*配音長度：中文 19.8s ／ 英文 17.6s*

**畫面公式**

```
齊次函數：限制到直線就是直線   |   homogeneous: a line restricts to a line
F ( x ξ )  =  x F ( ξ )              D ξ F ( 0 )  =  F ( ξ )
```

**旁白（繁中）**

> 反過來就不成立了。齊次函數是說把向量放大幾倍，值就跟著放大幾倍。這種函數在原點沿每一個方向都有導數，而且那個導數正好等於函數本身在 ξ 的值，因為限制到直線上它就是一條直線。

**Narration (EN)**

> The converse fails. A homogeneous function is one where scaling the vector scales the value by the same factor. Such a function has a derivative at the origin in every direction, equal to the function's own value at xi, because restricted to a line it simply is a line.

**動畫**

左邊三個方向的箭頭，右邊是把齊次函數限制到那三條直線上得到的三條直線，斜率各不相同。

## Beat 9 — 可微的齊次函數只能是線性的 / a differentiable homogeneous map must be linear
*配音長度：中文 15.2s ／ 英文 16.3s*

**畫面公式**

```
可微的齊次函數只能是線性的   |   a differentiable homogeneous map must be linear
dF ₀ ( ξ )  =  F ( ξ )           ⇒           F  ∈  Hom ( V , W )
```

**旁白（繁中）**

> 可是如果它同時可微，微分就必須等於函數本身，於是這個函數只能是線性的。所以任何非線性的齊次函數，都是「方向導數全部存在卻不可微」的反例。

**Narration (EN)**

> But if it is differentiable as well, the differential must equal the function itself, and so the function can only be linear. Hence every nonlinear homogeneous function is a counterexample: all directional derivatives exist and no differential does.

**動畫**

三行推導：齊次給出方向導數、定理 7.2 給出它等於微分、兩式一比就得到函數必須線性。

## Beat 10 — 所以非線性的齊次函數就是反例 / so any nonlinear one is a counterexample
*配音長度：中文 20.2s ／ 英文 19.0s*

**畫面公式**

```
所以非線性的齊次函數就是反例   |   so any nonlinear one is a counterexample
F ( x , y )  =  x ³ / ( x ² + y ² )              1 + 0  ≠  1 / 2
```

**旁白（繁中）**

> 最短的例子是 x 三次方除以 x 平方加 y 平方，在原點補上零。它連續、齊次、每個方向導數都存在，可是不是線性的，畫面上兩個值相加就對不起來。正面的結果要用均值定理，下一集講。

**Narration (EN)**

> The shortest example is x cubed over x squared plus y squared, set to zero at the origin. It is continuous, homogeneous, and has every directional derivative, yet is not linear: on screen two of its values refuse to add up. The positive result needs the mean value theorem.

**動畫**

藍色是反例在單位圓上的值，紅色是同時通過四個座標軸方向的線性函數。四個橘點重合，中間分開。

---

## 為什麼「方向」是用錯的字

書上特地點出來：把 ξ 乘上一個正數，指的方向沒變，可是方向導數會跟著乘上同一個數。
真正成立的是「對 ξ 線性」。這一拍畫成一支箭頭加三顆點——三支共線的箭頭會互相蓋掉，
這是上一輪學到的教訓。

## 反例只有在「不可加」那一步真的失敗

齊次、連續、每個方向導數都存在，這三件事那個反例全都做到了。它唯一失敗的是可加性，
而可加性正是線性的另一半。所以場景檔把「不可加」這件事斷言得最嚴（差距大於 0.4），
並且在畫面上用兩條曲線把它畫出來。
