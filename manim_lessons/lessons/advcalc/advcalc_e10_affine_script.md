# advcalc E10 — 第 1 章：平面、平行移動與仿射子空間

Chapter 1: Planes, Parallel Translation and Affine Subspaces

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 2 節（書頁 39–43）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e10_affine.py`（`AdvCalcE10ZH` / `AdvCalcE10EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[10]` / `FORMULAS_ADVCALC[10]`）
- 配音：`manim_lessons/samples/audio_e10/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.64 分（218 秒）／英文 3.08 分（185 秒）

---

## Beat 0 — 垂直於一個方向的平面 / the plane perpendicular to a direction
*配音長度：中文 19.8s ／ 英文 16.0s*

**畫面公式**

```
垂直於一個方向的平面   |   the plane perpendicular to a direction
( x − b , a )  =  0
```

**旁白（繁中）**

> 現在換平面。過某一點、而且垂直於某個方向的平面，包含另一個點，若且唯若連接這兩點的線段垂直於那個方向。用上一集的第二與第四件事翻譯過來，就是「座標差與那個方向的純量積等於零」。

**Narration (EN)**

> Now for planes. The plane through a point and perpendicular to a direction contains another point exactly when the segment joining them is perpendicular to that direction. By the second and fourth facts of the last episode, that means one scalar product is zero.

**動畫**

軸測投影的一片平面垂直於 OA，B 在平面上，X 也在平面上，BX 用紅線畫出來。

## Beat 1 — 展開成係數乘座標 / expanded into coefficients times coordinates
*配音長度：中文 23.9s ／ 英文 17.9s*

**畫面公式**

```
展開成係數乘座標   |   expanded into coefficients times coordinates
( x , a )  =  l        Σ₁³ aᵢ xᵢ  =  l
```

**旁白（繁中）**

> 把純量積對第一個變數的線性拿來展開，再把定值那一項記成一個數，平面的方程就變成「座標與方向的純量積等於某個常數」，也就是三個係數分別乘上三個座標再加起來等於常數。反過來，只要方向不是零向量，滿足這個方程的點集就是一個平面。

**Narration (EN)**

> Expanding by linearity in the first variable and naming the constant, the equation becomes the scalar product of coordinates with direction equal to that constant: three coefficients times three coordinates, summed. Conversely, if the direction is nonzero, that locus is a plane.

**動畫**

同一張圖，右側說明怎麼用純量積對第一個變數的線性把方程展開。

## Beat 2 — 但一般空間沒有純量積 / but a general space has no scalar product
*配音長度：中文 20.6s ／ 英文 17.2s*

**畫面公式**

```
但一般空間沒有純量積   |   but a general space has no scalar product
ℝ³  :  ( x , y )          V  :  —
```

**旁白（繁中）**

> 但這裡有個問題。三維座標空間有一個自然的純量積，這在代數與幾何上都非常重要；可是大部分的向量空間並沒有自然的純量積。書上因此刻意在早期的向量理論裡完全不用它，要到第五章才回頭處理。

**Narration (EN)**

> But there is a problem. Coordinate three-space has a natural scalar product, extremely important both algebraically and geometrically; most vector spaces have none at all. The book therefore deliberately neglects it in the early vector theory, returning to it only in chapter five.

**動畫**

兩個方框：左邊座標三維空間裡寫著純量積的式子，右邊一般向量空間打一個大叉。

## Beat 3 — 改用線性泛函描述同一個平面 / the same plane, described by a functional
*配音長度：中文 21.5s ／ 英文 16.6s*

**畫面公式**

```
改用線性泛函描述同一個平面   |   the same plane, described by a functional
f ( x )  =  l        f  :  ℝ³ → ℝ  ,  f ≠ 0
```

**旁白（繁中）**

> 所以要換一個解讀方式。係數乘座標再加起來這個東西，第一節已經講過：它就是三維座標空間上最一般的線性泛函。於是平面的方程可以完全不提純量積，改寫成「一個非零線性泛函在該點的值等於某個常數」。

**Narration (EN)**

> So we look for another reading. Coefficients times coordinates, summed, is what section one identified as the most general linear functional on coordinate three-space. So the equation of a plane can drop the scalar product and become a functional taking a constant value.

**動畫**

同一片平面再畫一次（換成主色）。重點是平面本身完全沒有變，只是換了一個描述方式。

## Beat 4 — 係數隨時讀得回來 / the coefficients read back off f
*配音長度：中文 16.6s ／ 英文 15.2s*

**畫面公式**

```
係數隨時讀得回來   |   the coefficients read back off f
aᵢ  =  f ( δ ⁱ )        f ( x ) = f ( Σ xᵢ δ ⁱ ) = Σ xᵢ aᵢ
```

**旁白（繁中）**

> 反過來也成立：給定任何一個非零線性泛函與任何一個數，滿足那個方程的點集都是一個平面。而係數三元組隨時可以從泛函讀回來——把三個單位向量分別餵進去就是了。

**Narration (EN)**

> The converse holds too: given any nonzero linear functional and any number, the locus of that equation is a plane. And the coefficient triple can always be read back off the functional, by feeding in the three unit vectors.

**動畫**

三個單位向量餵進 f，各自掉出一個係數。

## Beat 5 — 每條有向線段滑到等價的線段 / every directed segment slides to an equivalent one
*配音長度：中文 16.1s ／ 英文 16.7s*

**畫面公式**

```
每條有向線段滑到等價的線段   |   every directed segment slides to an equivalent one
OX  ∼  BY
```

**旁白（繁中）**

> 接著找平行移動的向量形式。平面幾何裡談兩個平行而且同向的全等圖形時，常說把其中一個「沿著平面滑動」得到另一個，滑動時所有直線都保持與原來平行。

**Narration (EN)**

> Next, the vector form of parallel translation. In plane geometry, when two congruent figures are parallel and similarly oriented, we often speak of obtaining one from the other by sliding the plane along itself so that every line stays parallel to where it was.

**動畫**

一個三角形與它滑動之後的副本，三個頂點各畫一支箭頭——三支完全一樣，這正是等價的條件。

## Beat 6 — 座標之間差一個固定向量 / the coordinates differ by one fixed vector
*配音長度：中文 18.1s ／ 英文 17.9s*

**畫面公式**

```
座標之間差一個固定向量   |   the coordinates differ by one fixed vector
x  =  y − b
```

**旁白（繁中）**

> 這個描述可以講得更漂亮：所謂平行移動，就是每一條有向線段都滑到與它等價的線段。如果某個點滑到另一個點、原點滑到某個點，那麼由等價的條件，座標之間差的就是一個固定的向量。

**Narration (EN)**

> That description can be put more elegantly: a parallel translation is one in which every directed segment slides to an equivalent segment. If one point slides to another and the origin slides to some point, then by the equivalence condition the coordinates differ by one fixed vector.

**動畫**

O、X、B、Y 四個點與四支箭頭，顯示 OX 與 BY 等價、座標之間差的是同一個向量。

## Beat 7 — 平行移動就是加上常向量 / a translation is adding a constant vector
*配音長度：中文 16.2s ／ 英文 14.0s*

**畫面公式**

```
平行移動就是加上常向量   |   a translation is adding a constant vector
x  ↦  y  =  x + b
```

**旁白（繁中）**

> 所以平行移動的座標形式，就是「加上一個常向量」。反過來，任何一個常向量給出的這種映射，都確實是一個平行移動。這件事在平面與空間都一樣成立。

**Narration (EN)**

> So in coordinates a parallel translation is simply adding a constant vector. Conversely, the mapping given by any constant vector really is a parallel translation. This holds equally for the plane and for space.

**動畫**

一整片格點，每一點都被同一支箭頭推到新位置。

## Beat 8 — 平移後還是一個平面 / the translate is again a plane
*配音長度：中文 22.1s ／ 英文 17.0s*

**畫面公式**

```
平移後還是一個平面   |   the translate is again a plane
f ( y − b ) = l   ⇔   f ( y ) = l + f ( b )        N  =  M + b
```

**旁白（繁中）**

> 幾何上很明顯，平行移動把平面送到平面、直線送到直線；現在也可以給一個純代數的證明。方程是某個泛函等於常數的那個平面，經過平移之後，方程變成同一個泛函等於「原來的常數加上泛函在位移向量的值」，還是一個平面。

**Narration (EN)**

> Geometrically it is clear that translations carry planes to planes, and now we can prove it algebraically. Take the plane whose equation is a functional equal to a constant; translating gives the same functional equal to that constant plus the functional at the shift vector.

**動畫**

兩片平行的平面，中間一支箭頭代表位移向量。

## Beat 9 — 平面與直線都是子空間的平移 / planes and lines are translates of subspaces
*配音長度：中文 21.3s ／ 英文 17.1s*

**畫面公式**

```
平面與直線都是子空間的平移   |   planes and lines are translates of subspaces
l = 0   ⇔   0 ∈ M        M  =  N ( f )  +  b        { t a + b }  =  { t a } + b
```

**旁白（繁中）**

> 現在把這些幾何名詞搬到座標空間上。方程是泛函等於某個常數的那個平面，通過原點若且唯若那個常數是零——而這時它正好是泛函的零空間，是一個子空間。所以座標空間裡的平面與直線，都是子空間的平移。

**Narration (EN)**

> Now carry the terminology over to coordinate space. A plane whose equation is a functional equal to a constant passes through the origin exactly when that constant is zero, and then it is the null space of the functional. So planes and lines are translates of subspaces.

**動畫**

過原點的那一片平面畫成實色，它的一個平移畫成淡色，中間一支箭頭連起來。

## Beat 10 — 超平面 / the hyperplane
*配音長度：中文 22.1s ／ 英文 19.0s*

**畫面公式**

```
超平面   |   the hyperplane
dim N ( f )  =  n − 1        ℝ³  :  plane          ℝ²  :  line
```

**旁白（繁中）**

> 這些推廣到任意實向量空間，就叫做仿射子空間——子空間的平移。非零線性泛函的零空間永遠是 n 減一維的，這種東西叫超平面。在三維座標空間裡超平面就是普通的幾何平面，但在平面裡，超平面是直線。

**Narration (EN)**

> In any real vector space these are the affine subspaces, translates of subspaces. The null space of a nonzero functional always has dimension n minus one, and such a set is a hyperplane. In coordinate three-space a hyperplane is an ordinary plane, but in the plane it is a line.

**動畫**

左邊是三維空間裡的一片平面，右邊是平面上的一條直線——兩者都是超平面。
