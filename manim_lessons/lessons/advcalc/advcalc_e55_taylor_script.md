# advcalc E55 — 第 3 章：Taylor 公式

Chapter 3: The Taylor Formula

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 17 節「Taylor 公式」（書頁 191–194）。**這一節整節沒有習題，第 3 章到此結束**。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e55_taylor.py`（`AdvCalcE55ZH` / `AdvCalcE55EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[55]` / `FORMULAS_ADVCALC[55]`）
- 配音：`manim_lessons/samples/audio_e55/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.30 分（198 秒）／英文 3.24 分（195 秒）

## 同一個數字，三種算法；同一條餘項，把 k 解出來

這一集的驗算建在一件事上：F 是多項式時，把它限制到一條直線上得到的 λ 也是多項式，
所以 λ 的 Taylor 係數可以用五個取樣點**精確地**解出來，一點截斷誤差都沒有。
有了這個，這一集的每一句話都變得可驗：

- **定理 16.1 往上推**：三個方向的六種排法，六個值完全相同（3.240000）；
  而三重的中央差商算出來也是 3.240000。
- **餘項的均值形式**：取 m 等於 2，把那個「存在某個 k」真的解出來，
  得到 **k = 0.25**，斷言它嚴格落在零與一之間，再代回去驗等式兩邊到小數點後九位相同。
  定理只說「存在」，這裡把它找出來了。
- **多重指標的係數**：斷言 `Σ_{|k|=m} (m,k)` 等於 n 的 m 次方，也就是原來那個展開的項數。
- **書上自己的例子**：`sin(x + y²)` 的展開式。尺度減半，誤差掉 154、141、134 倍，
  一路收斂到 128——也就是 2 的 7 次方，因為第一個沒寫出來的項是七次。

probe 幀與三道工具一起抓到五處表格排版：四張表的最後一列都撞到註腳，
還有 beat 9 表頭的最後一欄原本寫成英文的 `ratio`（langscan 抓的）。

---

## Beat 0 — 一直往上疊 / stacking upward
*配音長度：中文 17.9s ／ 英文 16.8s*

**畫面公式**

```
一直往上疊   |   stacking upward
dF  :  A  →  Hom ( V , W )            d ² F  :  A  →  Hom ² ( V , W )
```

**旁白（繁中）**

> 第 17 節是第 3 章的最後一節。微分 dF 是一個從 A 到 Hom 的映射；如果它可微，那個微分就是二階微分，落在雙線性映射的空間裡。同樣的動作可以一直往上疊，沒有上限。

**Narration (EN)**

> Section 17 closes chapter 3. The differential of F is a map from the domain into Hom; if that map is differentiable, its differential is the second differential, living in the space of bilinear maps. The same move stacks upward without limit.

**動畫**

左邊四行式子由上而下：F、dF、d²F、d³F 各自的型別，旁邊一列小箭頭串起來，最後一個省略號。
右側說明每一層都是上一層的微分。

## Beat 1 — n 階微分是對稱的 n 重線性映射 / symmetric n-linear
*配音長度：中文 18.0s ／ 英文 14.8s*

**畫面公式**

```
n 階微分是對稱的 n 重線性映射   |   symmetric n-linear
d ⁿ F   :   A   →   Hom ⁿ ( V , W )
```

**旁白（繁中）**

> 第 n 階微分是一個從 A 到 n 重線性映射那個空間的映射。而且上一集那條「二階微分對稱」可以用歸納法往上推：第 n 階微分是一個對稱的 n 重線性映射。書上把這個證明省略了。

**Narration (EN)**

> The nth differential is a map from the domain into the space of n-linear maps. And the previous episode's symmetry theorem extends by induction: the nth differential is a symmetric n-linear map. The book omits that proof.

**動畫**

左邊一張表：三個方向的六種排列，以及對應的 d³F 值——六個完全相同。
右側說明 n 階微分是對稱的 n 重線性映射。

## Beat 2 — 就是連續 n 次方向導數 / the nested directional derivative
*配音長度：中文 18.0s ／ 英文 16.3s*

**畫面公式**

```
就是連續 n 次方向導數   |   the nested directional derivative
D ξ ₁  …  D ξ ₙ  F ( α )      =      d ⁿ F ₐ ( ξ ₁ , … , ξ ₙ )
```

**旁白（繁中）**

> 上一集那條「二階微分就是混合方向導數」也一樣往上推：連續作用 n 次方向導數，結果就是第 n 階微分吃那 n 個方向。證明從最左邊那一項出發，反覆用取值映射與合成規則。

**Narration (EN)**

> The identification of the second differential with the nested directional derivative also lifts: taking n directional derivatives in a row gives the nth differential on those n directions. The proof starts from the leftmost term and repeats the evaluation trick.

**動畫**

左邊一個加框的定理 16.1，下面一張表列出三種算法的數值。
右側說明從最左邊那一項出發、反覆用取值映射。

## Beat 3 — 座標下的多重求和 / the multiple sum in coordinates
*配音長度：中文 15.6s ／ 英文 18.0s*

**畫面公式**

```
座標下的多重求和   |   the multiple sum in coordinates
d ᵐ F ₐ ( c ¹ , … , c ᵐ )   =   Σ  c ¹ ᵢ … c ᵐ ⱼ   ∂ ᵐ F / ∂x ᵢ … ∂x ⱼ
```

**旁白（繁中）**

> 座標下跟前面平行：F 到 m 階為止的微分都連續，等價於所有 m 階偏導數存在而且連續；而 m 階微分吃 m 個向量的結果，就是那些偏導數配上 m 組分量的多重求和。

**Narration (EN)**

> In coordinates the pattern continues: F has continuous differentials through order m exactly when all mth-order partial derivatives exist and are continuous, and the value of the mth differential on m vectors is the multiple sum of those partials weighted by the components.

**動畫**

左邊一個加框的多重求和公式，下面兩個方塊（偏導數連續 → 微分連續）。
右側說明跟第 9 節同一個模式。

## Beat 4 — 沿一條直線走 / along one line
*配音長度：中文 21.0s ／ 英文 19.0s*

**畫面公式**

```
沿一條直線走   |   along one line
λ ( t )  =  F ( α + t η )          d ʲ λ / d t ʲ  =  ( D η ) ʲ F ( α + t η )
```

**旁白（繁中）**

> 接下來看 F 沿一條直線的行為。令 λ 是把 t 送到 F 在 α 加 t η 的值。用歸納法可以證明：λ 的第 j 階導數，就是沿 η 的方向導數作用 j 次之後在那一點的值。j 等於一那一步就是定理 7.2。

**Narration (EN)**

> Now the behaviour of F along a line. Let lambda send t to the value of F at alpha plus t eta. By induction the jth derivative of lambda is the directional derivative along eta applied j times, evaluated there. The case j equal to one is Theorem 7.2.

**動畫**

左邊 λ 限制到一條直線之後的曲線，兩端打點。
右側是 λ 的定義與它的第 j 階導數。

## Beat 5 — 一般的 Taylor 公式 / the general Taylor formula
*配音長度：中文 19.1s ／ 英文 19.2s*

**畫面公式**

```
一般的 Taylor 公式   |   the general Taylor formula
F ( α + η )  =  F ( α ) + D η F ( α ) + … + ( 1 / m ! ) D η ᵐ F ( α ) + R
```

**旁白（繁中）**

> 如果 F 是實值的，λ 就是一元的實值函數，一元的 Taylor 公式直接可用。取 t 等於一再代回去，就得到賦範空間裡的一般 Taylor 公式：前 m 項是方向導數，最後一項是餘項，在中間某一點取值。

**Narration (EN)**

> If F is real-valued, lambda is a real function of one variable and the ordinary Taylor formula applies. Taking t equal to one and substituting back gives the general Taylor formula in a normed space: m terms of directional derivatives and a remainder evaluated somewhere between.

**動畫**

左邊一個加框的 Taylor 公式，下面一張表：前三項與餘項的數值，四個相加正好是函數值。

## Beat 6 — 餘項落在中間某一點 / the remainder sits between
*配音長度：中文 14.7s ／ 英文 16.2s*

**畫面公式**

```
餘項落在中間某一點   |   the remainder sits between
R    =    ( 1 / ( m + 1 ) ! )    d ᵐ ⁺ ¹ F  ( η , … , η )              0 < k < 1
```

**旁白（繁中）**

> 用微分寫出來更整齊：第 m 項是 m 階微分吃 m 個相同的 η，除以 m 階乘；餘項是第 m 加一階微分，在 α 加 k 倍 η 那一點取值，而 k 落在零與一之間。

**Narration (EN)**

> Written with differentials it is tidier: the mth term is the mth differential on m copies of eta divided by m factorial, and the remainder is the next differential taken at a point between, with the parameter somewhere in the unit interval.

**動畫**

左邊一條從 0 到 1 的線段，中間標出解出來的 k = 0.2500。
右側說明均值形式只說存在，這裡把它找出來了。

## Beat 7 — m = n = 2 的樣子 / the case m equals n equals two
*配音長度：中文 17.9s ／ 英文 18.9s*

**畫面公式**

```
m = n = 2 的樣子   |   the case m equals n equals two
( 1 / 2 ! ) D ₛ ² F ( a )   =   ½ [ s ² F ₓₓ  +  2 s t F ₓᵧ  +  t ² F ᵧᵧ ]
```

**旁白（繁中）**

> 翻成座標，一般項就是那個熟悉的「求和符號的 m 次方」。m 與 n 都等於二時展開，就是 s 平方乘對 x 的二階偏導、加二倍 s t 乘混合偏導、加 t 平方乘對 y 的二階偏導，全部除以二。

**Narration (EN)**

> In coordinates the general term is the familiar mth power of a sum of partials. Expanding it when m and n are both two gives s squared times the second partial in x, plus twice s t times the mixed partial, plus t squared times the second partial in y, all halved.

**動畫**

左邊一個加框的 m = n = 2 展開式，下面是一般項的「求和符號的 m 次方」。
右側說明中間那個 2 來自兩個相同的混合項。

## Beat 8 — 多重指標記號 / multi-index notation
*配音長度：中文 19.7s ／ 英文 19.6s*

**畫面公式**

```
多重指標記號   |   multi-index notation
( 1 / m ! )    Σ  | k | = m    ( m ,  k )    D ᵏ F ( a )    x ᵏ
```

**旁白（繁中）**

> 這樣寫邏輯上簡單，可是很浪費：同樣的項會重複出現。所以有多重指標記號：k 是一組非負整數，用直槓記總和、上標記單項式、D 的 k 次方記反覆求偏導。整個第 m 項就縮成一行。

**Narration (EN)**

> That description is logically simple but wasteful, since identical terms repeat. Hence multi-index notation: a tuple of nonnegative integers, its total written with bars, a monomial written as a power, and repeated differentiation written as one operator. The mth term becomes one line.

**動畫**

左邊兩行多重指標的定義，一個加框的第 m 項，下面一張表驗證係數之和等於 n 的 m 次方。

## Beat 9 — 實際上不這樣算 / nobody computes it this way
*配音長度：中文 16.0s ／ 英文 16.9s*

**畫面公式**

```
實際上不這樣算   |   nobody computes it this way
sin ( x + y ² )  =  x + y ² − x ³ / 3 ! − x ² y ² / 2 + …
```

**旁白（繁中）**

> 可是實際上沒有人這樣算。書上說一般的 Taylor 公式太笨重，主要是理論上的價值；真正在算的展開式都是用別的辦法得到的，例如把一個多項式代進一個已知的冪級數。

**Narration (EN)**

> In practice nobody computes that way. The book says the general formula is too cumbersome to be of much use and is principally of theoretical value; the expansions actually computed come by other means, such as substituting a polynomial into a known power series.

**動畫**

左邊書上那個 sin(x + y²) 的兩行展開式，下面一張表：三個尺度的誤差與它們的比值。

## Beat 10 — C 上標 k 與 C 無窮 / the classes C k and C infinity
*配音長度：中文 20.3s ／ 英文 19.0s*

**畫面公式**

```
C 上標 k 與 C 無窮   |   the classes C k and C infinity
C ᵏ ( A , W )                    C ᵏ  ∘  C ᵏ    ⊂    C ᵏ
```

**旁白（繁中）**

> 最後是 C 上標 k：到 k 階為止的微分都存在而且連續。它是一個向量空間，合成與乘積都保持它；下一章會證取反元素也保持，於是隱函數定理交出來的函數也同一類。對每個 k 都成立就叫 C 無窮。

**Narration (EN)**

> Finally the notation: a map whose differentials through order k exist and are continuous is of class C k. That class is a vector space closed under composition and products, and the next chapter adds inversion, so an implicit function inherits the class. For every k it is C infinity.

**動畫**

左邊四個方塊（和、合成、乘積、取反元素）指向 C 上標 k，下面一行 C 無窮。
右側說明下一章會補上取反元素那一個。

---

## 為什麼用多項式

高階的數值微分很容易被截斷誤差淹掉：三階的中央差商誤差是 h 平方乘上五階導數。
可是 F 取成四次多項式時，限制到直線上的 λ 也是四次，而四次多項式的五階導數是零——
所以那個差商是精確的。更好的是：λ 的五個係數可以用五個取樣點解一個線性方程組直接得到，
連差商都不必用。這一集所有的數字都是這樣來的。

## 第 3 章到此結束

書頁 194。這一章從賦範空間的範數講到 Taylor 公式，中間補進了隱函數定理、
子流形、變分法與二階微分。下一集開第 4 章：緊緻性與完備性——
也就是把「極限存在」這件事本身當成研究對象。
