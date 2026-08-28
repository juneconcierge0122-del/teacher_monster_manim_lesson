# advcalc E40 — 第 3 章：均值定理

Chapter 3: The Mean Value Theorem

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 7 節的後段（書頁 148–150）。書頁 151–152 是習題 7.1–7.15，第 8 節從書頁 152 起。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e40_mean_value.py`（`AdvCalcE40ZH` / `AdvCalcE40EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[40]` / `FORMULAS_ADVCALC[40]`）
- 配音：`manim_lessons/samples/audio_e40/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.19 分（191 秒）／英文 3.15 分（189 秒）

## 那條弧是挑過的，好讓「精確版是錯的」看得見

一元的均值定理說「兩端的差等於區間長度乘上某一點的導數」。要說明它在向量值的情形是錯的，
最好的辦法不是講理由，是找一條弧讓它一眼就錯。這一集用的是**速率恆等於一**的圓弧：

- 場景檔斷言速率確實恆等於一（掃 2001 個取樣點）。
- 於是每一個候選向量 `(b − a) f′(c)` 的長度**全部都是 2.2**（也斷言了）。
- 而兩端的直線距離是 1.78。長度就對不上，所以那個 c 不可能存在。
- 掃 4001 個 c，最接近的一個還差 0.31，這個數字直接放進旁白。

後半段的定理 7.4 也是量出來的：在半徑 0.8 的球上掃出微分算子範數的上確界（0.68），
再掃 180 × 3 × 72 組 (β, ξ) 求出實際變化量的最大商（0.43），斷言後者不超過前者。

**beat 5 的那一對 (β, ξ) 換過一次。** 初稿隨手挑的一對只用掉允許範圍的四分之一，
畫面上紅箭頭縮在紫圈中央，看起來像是定理什麼也沒說。改成掃出「最接近上界」的那一對，
現在紅箭頭填掉圓的 78%，並加了一條 `assert` 釘住這件事。

---

## Beat 0 — 精確的均值定理在這裡是錯的 / the exact theorem is false here
*配音長度：中文 18.2s ／ 英文 16.9s*

**畫面公式**

```
精確的均值定理在這裡是錯的   |   the exact theorem is false here
f ( b ) − f ( a )   ≠   ( b − a ) · f ′ ( c )              ( ∀ c )
```

**旁白（繁中）**

> 一元微積分的均值定理說，兩端的差等於區間長度乘上某一點的導數。這句話在向量值的情形是錯的：畫面上那條弧，不管挑哪一點的導數都湊不出兩端的差，最好的一點還差 0.31。

**Narration (EN)**

> The mean value theorem of one variable calculus says the difference of the endpoints equals the interval's length times the derivative somewhere. For vector values that is false: for the arc on screen no point's derivative reproduces it, and the best misses by 0.31.

**動畫**

灰色的圓是所有候選向量（長度全都一樣），紫色的線是其中八支，藍色是那條弧，紅色箭頭是真正要湊出來的兩端差。

## Beat 1 — 定理 7.3：改成一個不等式 / Theorem 7.3: an inequality instead
*配音長度：中文 15.7s ／ 英文 17.3s*

**畫面公式**

```
定理 7.3：改成一個不等式   |   Theorem 7.3: an inequality instead
‖ f ′ ( t ) ‖  ≤  m           ⇒           ‖ f ( b ) − f ( a ) ‖  ≤  m ( b − a )
```

**旁白（繁中）**

> 所以這裡改證一個不等式。定理 7.3：如果 f 在區間上連續、內部處處可導，而且導數的範數處處不超過 m，那麼兩端的距離就不超過 m 乘上區間的長度。

**Narration (EN)**

> So an inequality is proved instead. Theorem 7.3: if f is continuous on the interval, differentiable inside it, and the norm of its derivative never exceeds m, then the distance between the endpoints never exceeds m times the length of the interval.

**動畫**

同一條弧，加上半徑為 m 乘區間長度的紫色球——定理說終點一定落在裡面。

## Beat 2 — 速率乘時間，蓋得住直線距離 / speed times time covers the straight gap
*配音長度：中文 17.7s ／ 英文 17.4s*

**畫面公式**

```
速率乘時間，蓋得住直線距離   |   speed times time covers the straight gap
1.78    ≤    1 × 2.2
```

**旁白（繁中）**

> 幾何上這很直觀：走得多快乘上走了多久，一定不小於頭尾的直線距離。畫面上那條弧的速率恆等於一，走了 2.2 的時間，而頭尾的直線距離是 1.78，弧比直線多了兩成多。

**Narration (EN)**

> Geometrically that is plain: how fast you go times how long you go for is at least the straight line distance from start to finish. The arc on screen has speed exactly one and runs for 2.2, while the straight gap is 1.78, so the arc is about a fifth longer.

**動畫**

青色是「走到 x 為止的直線距離」，紫色是「速率上限乘上時間」，青色永遠壓在紫色下面。

## Beat 3 — 證明：先造一個集合 / the proof: build a set first
*配音長度：中文 16.1s ／ 英文 16.6s*

**畫面公式**

```
證明：先造一個集合   |   the proof: build a set first
A  =  { x  :  ‖ f ( x ) − f ( a ) ‖  ≤  ( m + ε ) ( x − a ) + ε }
```

**旁白（繁中）**

> 證明的骨架值得看一遍，因為它是「用最小上界逼到底」的標準寫法。固定一個正的 ε，把滿足那條放寬過的不等式的點收成一個集合，然後去看這個集合的最小上界。

**Narration (EN)**

> The proof is worth watching once, since it is the standard way of pushing a least upper bound to the end. Fix a positive epsilon, collect the points satisfying a slightly relaxed version of the inequality into a set, and look at that set's least upper bound.

**動畫**

同一張圖加上紅色的放寬上界（多一個 ε），底下橘色那一段是集合 A。

## Beat 4 — 它的上界只能是右端點 / its bound can only be the right endpoint
*配音長度：中文 19.8s ／ 英文 17.2s*

**畫面公式**

```
它的上界只能是右端點   |   its bound can only be the right endpoint
l  =  lub A              l  =  b
```

**旁白（繁中）**

> 由連續性，那個上界自己也在集合裡。接著證它一定是右端點：如果不是，在那一點導數還在，就還能再往前推一小段，推出來的點也在集合裡，這跟「它是上界」矛盾。最後讓 ε 趨於零。

**Narration (EN)**

> By continuity the bound itself belongs to the set. Then it must be the right endpoint: if it were not, the derivative still exists there, so one could push a little further and land in the set again, contradicting its being an upper bound. Finally let epsilon go to zero.

**動畫**

上界 l 的位置畫成紫色虛線，橘色箭頭表示還能往右推一小段——這就是矛盾的來源。

## Beat 5 — 定理 7.4：多變數的說法 / Theorem 7.4: the many variable form
*配音長度：中文 18.8s ／ 英文 18.6s*

**畫面公式**

```
定理 7.4：多變數的說法   |   Theorem 7.4: the many variable form
‖ dF ᵦ ‖  ≤  ε           ⇒           ‖ ΔF ᵦ ( ξ ) ‖  ≤  ε ‖ ξ ‖
```

**旁白（繁中）**

> 定理 7.4 是多變數的說法，也是後面真正會用到的形式。如果 F 在一顆球上可微，而且每一點的微分算子範數都不超過 ε，那麼球裡任兩點之間的變化量，範數就不超過 ε 乘上位移的範數。

**Narration (EN)**

> Theorem 7.4 is the many variable version, and the form actually used later. If F is differentiable on a ball and the operator norm of its differential never exceeds epsilon there, then the change between any two points of the ball has norm at most epsilon times the displacement.

**動畫**

左邊 V 裡球中的兩點與連起來的線段，右邊 W 裡是兩個像的差（紅箭頭）與半徑 ε‖ξ‖ 的紫圈。

## Beat 6 — 證明就是把上一集接上來 / the proof attaches the previous episode
*配音長度：中文 19.2s ／ 英文 19.5s*

**畫面公式**

```
證明就是把上一集接上來   |   the proof attaches the previous episode
γ ( t )  =  F ( β + t ξ )              ‖ γ ′ ( t ) ‖  ≤  ε ‖ ξ ‖
```

**旁白（繁中）**

> 證明只是把上一集接上來。從 β 走到 β 加 ξ 的線段本身是一條參數化弧；用定理 7.2，它的切向量就是微分作用在 ξ 上，範數不超過 ε 乘 ξ 的範數。再套定理 7.3 就結束了。

**Narration (EN)**

> The proof simply attaches the previous episode. The segment from beta to beta plus xi is itself a parametrized arc; by Theorem 7.2 its tangent vector is the differential applied to xi, of norm at most epsilon times the norm of xi. Theorem 7.3 then finishes it.

**動畫**

三行推導：線段是一條參數化弧、定理 7.2 給切向量、定理 7.3 收尾。

## Beat 7 — 用到的只有凸性 / only convexity was used
*配音長度：中文 14.4s ／ 英文 14.1s*

**畫面公式**

```
用到的只有凸性   |   only convexity was used
β , β + ξ  ∈  C           ⇒           [ β , β + ξ ]  ⊂  C
```

**旁白（繁中）**

> 這裡用到球的性質只有一條：球裡任兩點之間的線段，整條都在球裡。那正是凸性的定義，所以同一句話對任何凸集都成立，根本不必是球。

**Narration (EN)**

> Only one property of the ball is used: the segment joining any two of its points lies inside it. That is precisely the definition of convexity, so the same sentence holds for any convex set and never needed a ball at all.

**動畫**

左邊一個凸的形狀（線段在裡面），右邊一個月牙形（線段跑出去了）。

## Beat 8 — 推論：把一個固定的 T 減掉 / the corollary: subtract a fixed T
*配音長度：中文 16.4s ／ 英文 16.0s*

**畫面公式**

```
推論：把一個固定的 T 減掉   |   the corollary: subtract a fixed T
‖ dG ᵦ − T ‖  ≤  ε        ⇒        ‖ ΔG ᵦ ( ξ ) − T ( ξ ) ‖  ≤  ε ‖ ξ ‖
```

**旁白（繁中）**

> 推論把它變成最常用的形式。把一個固定的線性映射 T 減掉：如果每一點的微分跟 T 相差不超過 ε，那麼變化量跟 T 作用在 ξ 上的結果也相差不超過 ε 乘 ξ 的範數。

**Narration (EN)**

> A corollary turns it into the form most used. Subtract a fixed linear map T: if at every point the differential differs from T by at most epsilon, then the change differs from T applied to xi by at most epsilon times the norm of xi.

**動畫**

紫色是固定線性映射 T 的像，紅色是真正的變化量，兩者差多少由微分跟 T 差多少決定。

## Beat 9 — 記號：固定住的變數對調 / notation: which variable is pinned
*配音長度：中文 16.6s ／ 英文 17.7s*

**畫面公式**

```
記號：固定住的變數對調   |   notation: which variable is pinned
( D ξ F ) ( α )     =     dF ₐ ( ξ )     =     J F ( α ) ( ξ )
```

**旁白（繁中）**

> 最後講記號。方向導數寫成 D 下標 ξ 的 F 在 α，微分寫成 dF 下標 α 作用在 ξ，兩個是同一個數，可是固定住的變數剛好對調：一個把 α 固定，一個把 ξ 固定。

**Narration (EN)**

> Finally the notation. The directional derivative is written D sub xi of F at alpha, the differential as dF sub alpha applied to xi. The two are the same number, but the variable held fixed is swapped: one pins alpha down, the other pins xi down.

**動畫**

一個 (α, ξ) 的方格：藍色橫線是固定 α、紅色直線是固定 ξ，交點是同一個值。

## Beat 10 — dF 自己也可以再微分一次 / dF can be differentiated again
*配音長度：中文 18.3s ／ 英文 18.0s*

**畫面公式**

```
dF 自己也可以再微分一次   |   dF can be differentiated again
dF : A → Hom ( V , W )              d ² F ₐ  =  d ( dF ) ₐ              ω ( ξ , η )
```

**旁白（繁中）**

> 如果 F 在開集上每一點都可微，dF 本身就是一個從那個開集到 Hom 的映射，於是可以再問它可不可微。那就是二階微分；照對偶來看，它等價於一個雙線性映射。下一集講乘積空間。

**Narration (EN)**

> If F is differentiable at every point of an open set, dF is itself a map from that set into Hom, so one can ask whether it too is differentiable. That is the second differential; by duality it is equivalent to a bilinear map. Next time, product spaces.

**動畫**

三個方框串起來：V、Hom(V, W)、雙線性映射 ω，下方是二階微分的定義。

---

## 為什麼要花兩拍講證明

定理 7.3 的證明是實分析裡「用最小上界逼到底」的標準寫法：造一個集合、取它的最小上界、
證那個上界只能是右端點。這個套路在這本書後面還會出現好幾次，所以這裡拆成兩拍畫出來，
而不是一句「證明從略」。

## 凸性是唯一用到的性質

書上證完定理 7.4 之後補一句：球的性質只用到「任兩點的線段都在裡面」。這一拍就畫這件事——
一個凸的形狀與一個月牙形，同樣的兩點，線段一個在裡面一個跑出去。定理因此對任何凸集成立。
