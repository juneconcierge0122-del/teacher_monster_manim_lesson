# advcalc E45 — 第 3 章：切平面

Chapter 3: The Tangent Plane

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 10 節「初等應用」的後半（書頁 162–163）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e45_tangent_plane.py`（`AdvCalcE45ZH` / `AdvCalcE45EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[45]` / `FORMULAS_ADVCALC[45]`）
- 配音：`manim_lessons/samples/audio_e45/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.12 分（187 秒）／英文 2.99 分（180 秒）

## 切平面：一個定義、一個幾何刻畫、一個算得出來的例子

第 10 節的後半只有兩頁，可是它把「切」這個字講清楚了：
切平面不是靠幾何直覺定義的，而是「唯一一個貼合到小 o 等級的仿射子空間」。
定理 10.2 再回過頭給它一個純幾何的說法——它就是曲面上所有切向量的集合。

這一集用一個平面到平面的映射 `F(x₁, x₂) = (x₁x₂, x₁² − x₂)` 當例子，
它的圖形住在四維裡，畫不出來，可是每個數字都算得出來：

- **雅可比矩陣**在點 (2, 1) 上用中央差商算出來，斷言是 `[[1, 2], [4, −1]]`，函數值是 (2, 3)。
- **切平面的兩條方程**不是手寫上去的：程式先用矩陣與函數值組出那個仿射映射 `G`，
  再在三個離接觸點很遠的點上，斷言它與畫面上印的那兩條方程逐項相同。
- **貼合真的是小 o 等級**：第 9 拍那一欄是 `|F − G| / ‖ξ‖` 在三個越來越小的 `t` 上的值，
  斷言它單調遞減而且最後掉到 10⁻² 以下。
- **定理 10.2 在一條真的彎的弧上驗過**：取 `λ(t) = (2 + t, 1 + t²)`，
  斷言它抬到圖形上之後的切向量（四個分量，中央差商算的）等於「前兩個分量是 λ′、
  後兩個分量是 dFₐ 作用在 λ′ 上」，也就是定理 10.2 說的樣子；並斷言那四個數都是整數，
  畫面才印得乾淨。

畫面上前八拍共用同一張立體示意圖（一個高度函數 `0.34(x² − 0.6y²) + 0.62` 撐起的曲面），
它只是示意——真正的驗算全在數字上。

`bounds.py` 抓到 beat 2 的切平面右上角超出上緣。probe 幀抓到一個老問題：
定義域的格子與曲面的格子密度相同時，兩張網會糊成一團；把定義域畫稀畫細、
曲面畫密畫粗，並把曲面抬高，才分得開。

---

## Beat 0 — 把映射看成一張曲面 / a map seen as a surface
*配音長度：中文 21.0s ／ 英文 17.3s*

**畫面公式**

```
把映射看成一張曲面   |   a map seen as a surface
S   =   { ⟨ ξ , F ( ξ ) ⟩   :   ξ ∈ A }       ⊂       V × W
```

**旁白（繁中）**

> 這一節的後半段把「切平面」講清楚。把 F 看成 V 乘 W 裡的一個圖形：每個 ξ 對應到一個點，那些點合起來是一張蓋在定義域上面的曲面。實值函數在平面上的圖形是三維空間裡的曲面，這裡只是把維數放開。

**Narration (EN)**

> The rest of the section makes the tangent plane precise. View F as a graph inside V times W: each xi gives a point, and together they form a surface lying over the domain. It is the graph of a function of two variables with the dimensions set free.

**動畫**

左邊是一張立體示意圖：灰色稀疏的格子是定義域，上方藍色密一點的網是 F 的圖形。
右側三行說明圖形住在 V 乘 W 裡。

## Beat 1 — 兩個投影 / the two projections
*配音長度：中文 16.8s ／ 英文 16.7s*

**畫面公式**

```
兩個投影   |   the two projections
π ₁ ( ⟨ ξ , F ( ξ ) ⟩ )   =   ξ
```

**旁白（繁中）**

> 兩個投影把這件事說得更清楚：第一個投影把曲面壓回定義域，而 ξ 對應到曲面上正對著它的那一點。幾何上習慣把 V 想成「水平的那一層」，值域的方向想成「垂直的」。

**Narration (EN)**

> Two projections say it more clearly. The first pushes the surface back down onto the domain, and xi corresponds to the point of the surface lying directly over it. Geometrically one thinks of V as the horizontal layer and the range direction as vertical.

**動畫**

同一張圖，曲面上一點打紅點、正下方定義域上打紫點，中間一支紫色箭頭往下。
右側說明第一個投影把曲面壓回定義域，兩者一一對應。

## Beat 2 — 切平面：微分的圖形，平移過去 / the tangent plane: the differential, translated
*配音長度：中文 16.6s ／ 英文 15.7s*

**畫面公式**

```
切平面：微分的圖形，平移過去   |   the tangent plane: the differential, translated
M    =    ⟨ α , F ( α ) ⟩   +   dF ₐ
```

**旁白（繁中）**

> 現在假設 F 在 α 可微。微分本身是一個線性映射，它的圖形是 V 乘 W 裡過原點的一個子空間。把這個子空間平移到接觸點，得到的就是曲面在那一點的切平面。

**Narration (EN)**

> Now suppose F is differentiable at alpha. The differential is a linear map, so its graph is a subspace of V times W through the origin. Translate that subspace to the point of contact and what you get is the tangent plane to the surface there.

**動畫**

曲面畫細，紅色的平行四邊形片貼在接觸點上，接觸點打橘點。
右側三行：微分的圖形過原點，平移過去就是切平面。

## Beat 3 — 切平面的方程式 / the equation of the tangent plane
*配音長度：中文 16.3s ／ 英文 17.1s*

**畫面公式**

```
切平面的方程式   |   the equation of the tangent plane
η   −   F ( α )      =      dF ₐ ( ξ  −  α )
```

**旁白（繁中）**

> 寫成方程式就是：η 減掉 F 在 α 的值，等於微分作用在 ξ 減 α 上。換句話說，切平面是一個仿射映射的圖形——線性部分是微分，常數項是接觸點的值。

**Narration (EN)**

> As an equation: eta minus the value at alpha equals the differential applied to xi minus alpha. In other words the tangent plane is the graph of an affine map, whose linear part is the differential and whose constant term is the value at the point of contact.

**動畫**

左邊三行式子：點斜式、仿射映射 G、以及切平面 M 的集合寫法。
右側說明線性部分是微分、常數項是函數值。

## Beat 4 — 它是唯一貼合得夠好的平面 / the only plane that fits closely enough
*配音長度：中文 19.1s ／ 英文 16.7s*

**畫面公式**

```
它是唯一貼合得夠好的平面   |   the only plane that fits closely enough
F ( ξ )   −   G ( ξ )       ∈       o ( ξ − α )
```

**旁白（繁中）**

> 這個仿射映射是唯一的。因為微分是唯一使得「變化量等於它加上一個小 o」的線性映射，所以那個仿射映射也是唯一使得「函數減掉它落在小 o 裡」的。切平面因此是唯一「貼合得夠好」的平面。

**Narration (EN)**

> That affine map is unique. The differential is the only linear map whose sum with a little oh is the change, so the affine map is the only one whose difference from F is a little oh. The tangent plane is therefore the only plane that fits closely enough.

**動畫**

左邊三行：ΔFₐ = T + o、Hom ∩ o = {0}、F − G ∈ o。
右側說明微分唯一，所以那個仿射映射也唯一。

## Beat 5 — 定理 10.2：所有切線的聯集 / Theorem 10.2: the union of the tangent lines
*配音長度：中文 15.9s ／ 英文 17.2s*

**畫面公式**

```
定理 10.2：所有切線的聯集   |   Theorem 10.2: the union of the tangent lines
M     =     ∪   γ ′ ( t ₀ )
```

**旁白（繁中）**

> 定理 10.2 給這件事一個純幾何的說法：那個平面剛好是所有切線的聯集。更精確地說，微分的圖形裡的向量，恰好就是曲面上通過那一點的光滑曲線的切向量。

**Narration (EN)**

> Theorem 10.2 gives this a purely geometric reading: that plane is exactly the union of all the tangent lines. More precisely, the vectors in the graph of the differential are exactly the tangent vectors of smooth curves lying in the surface through that point.

**動畫**

曲面畫成灰色細線，紅色切平面片留著，接觸點射出三支不同顏色的箭頭。
右側說明平面上每個向量都是某條曲線的切向量，反過來也成立。

## Beat 6 — 一個方向：沿直線抬上去 / one way: lift a straight line
*配音長度：中文 15.0s ／ 英文 16.6s*

**畫面公式**

```
一個方向：沿直線抬上去   |   one way: lift a straight line
γ ( t ) = ⟨ α + t ξ , F ( α + t ξ ) ⟩        γ ′ ( 0 ) = ⟨ ξ , dF ₐ ( ξ ) ⟩
```

**旁白（繁中）**

> 一個方向很容易。任取平面上的一個向量，沿定義域裡的直線走，把它抬到曲面上，得到的曲線的切向量就正好是它——用的是引理 8.1 加上定理 7.2。

**Narration (EN)**

> One direction is easy. Take any vector of the plane, travel along the straight line it gives in the domain, lift that line onto the surface, and the resulting curve has exactly that vector as its tangent — by Lemma 8.1 and Theorem 7.2.

**動畫**

定義域上一條紫色直線，抬到曲面上變成藍色曲線，接觸點射出一支紅色切向量。
右側說明抬升用的是引理 8.1 與定理 7.2。

## Beat 7 — 另一個方向：任何曲線都在裡面 / the other: every curve lands inside
*配音長度：中文 17.8s ／ 英文 14.5s*

**畫面公式**

```
另一個方向：任何曲線都在裡面   |   the other: every curve lands inside
γ ( t ) = ⟨ λ ( t ) , F ( λ ( t ) ) ⟩        γ ′ = ⟨ λ ′ , dF ₐ ( λ ′ ) ⟩
```

**旁白（繁中）**

> 另一個方向也一樣短。曲面上任何一條通過那點的光滑曲線，寫出來就是把定義域裡一條曲線抬上去；它的切向量是「原來的切向量」配上「微分作用在它上面」，本來就在平面裡。

**Narration (EN)**

> The other direction is just as short. Any smooth curve in the surface through the point is a curve in the domain lifted up, and its tangent vector is the original tangent paired with the differential applied to it, which lies in the plane already.

**動畫**

這次定義域上畫的是一條真的彎的紫色曲線（拋物線），抬上去仍是藍色曲線。
右側四行說明任何曲面上的光滑曲線都是抬上去的，切向量本來就在平面裡。

## Beat 8 — 一個具體的例子 / a concrete example
*配音長度：中文 16.3s ／ 英文 15.5s*

**畫面公式**

```
一個具體的例子   |   a concrete example
F ( x ₁ , x ₂ ) = ⟨ x ₁ x ₂ , x ₁ ² − x ₂ ⟩              a = ⟨ 2 , 1 ⟩
```

**旁白（繁中）**

> 看一個具體的例子。取一個從平面到平面的映射，它的圖形住在四維空間裡。在 2 與 1 那一點，雅可比矩陣是一、二、四、負一，而函數值是二與三。

**Narration (EN)**

> Here is a concrete example: a map of the plane to the plane, whose graph lives in four dimensions. At the point two and one the Jacobian matrix reads one, two, four, minus one, and the value of the function is two and three.

**動畫**

左邊並排兩個矩陣：雅可比 dFₐ 與函數值 F(a)，各自標上名字。
右側說明這是平面到平面的映射，圖形住在四維裡。

## Beat 9 — 兩條純量方程 / two scalar equations
*配音長度：中文 14.8s ／ 英文 16.1s*

**畫面公式**

```
兩條純量方程   |   two scalar equations
y ₁ = x ₁ + 2 x ₂ − 2              y ₂ = 4 x ₁ − x ₂ − 4
```

**旁白（繁中）**

> 把這些代進切平面的方程式，得到兩條純量方程：y 一等於 x 一加二倍 x 二減二，y 二等於四倍 x 一減 x 二減四。這兩條就是切平面的完整描述。

**Narration (EN)**

> Substituting into the equation of the tangent plane gives two scalar equations: y one equals x one plus twice x two minus two, and y two equals four x one minus x two minus four. Those two are the whole description of the plane.

**動畫**

左邊兩條加框的純量方程 y₁ = x₁ + 2x₂ − 2、y₂ = 4x₁ − x₂ − 4。
右側是一張表：t 與餘項商 |F − G| / ‖ξ‖ 在四個取樣點上的值。

## Beat 10 — 四維裡兩個超平面的交 / two hyperplanes in four dimensions
*配音長度：中文 18.0s ／ 英文 16.2s*

**畫面公式**

```
四維裡兩個超平面的交   |   two hyperplanes in four dimensions
x ₁ + 2 x ₂ − y ₁ = 2              4 x ₁ − x ₂ − y ₂ = 4
```

**旁白（繁中）**

> 換個角度看，這兩條方程各自定義四維空間裡的一個超平面，而切平面就是它們的交。畫面上那一列是餘項的商，程式算的，確實一路掉到零。下一集開始講隱函數定理。

**Narration (EN)**

> Read another way, each of those equations defines a hyperplane in four dimensions, and the tangent plane is their intersection. The column on screen is the remainder quotient, computed here, and it does fall to zero. Next time, the implicit function theorem.

**動畫**

左邊兩條加框的超平面方程，下面印出那條曲線的切向量四個分量。
右側說明兩個條件、四個變數，交出來是二維。

---

## 「切」在這裡是逼近，不是直覺

切平面的定義沒有用到任何幾何直觀：它是唯一一個與 F 的差落在小 o 裡的仿射映射的圖形，
而唯一性來自 E37 最後那條「線性映射裡只有零是小 o」。
定理 10.2 是事後才給它一個幾何的說法，兩個方向都要證，這一集第 6、7 拍各做一個方向。

## 為什麼例子挑一個畫不出來的

平面到平面的映射，圖形是四維裡的二維曲面。挑它不是為了刁難，
而是為了說明那條方程完全不依賴維數：切平面照樣寫得出來、餘項照樣算得出來、
切向量照樣驗得出來。畫面上的立體圖只是示意用的道具。
