# advcalc E09 — 第 1 章：座標對應與純量積

Chapter 1: The Coordinate Correspondence and the Scalar Product

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 1 章第 2 節（書頁 36–39）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e09_coordinates.py`（`AdvCalcE09ZH` / `AdvCalcE09EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[9]` / `FORMULAS_ADVCALC[9]`）
- 配音：`manim_lessons/samples/audio_e09/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.46 分（208 秒）／英文 3.03 分（182 秒）

---

## Beat 0 — 把座標系接回向量空間 / coordinates, back onto vector spaces
*配音長度：中文 19.5s ／ 英文 17.8s*

**畫面公式**

```
把座標系接回向量空間   |   coordinates, back onto vector spaces
𝔼³   ⟷   ℝ³
```

**旁白（繁中）**

> 這一節要把解析幾何的座標系接回向量空間。座標系讓我們能用向量的語言談直線與平面這些幾何對象，而這些幾何直觀反過來也會幫我們理解向量空間。所以先複習一下座標對應是怎麼建立的。

**Narration (EN)**

> This section connects the coordinate systems of analytic geometry back to vector spaces. Coordinates let us treat lines and planes in vector terms, and the geometry repays us in intuition about vector spaces. We begin by reviewing how the correspondence is set up.

**動畫**

兩個方框「幾何空間」與「座標空間」，中間兩支反方向的箭頭。

## Beat 1 — 直線上的座標對應 / the correspondence on a line
*配音長度：中文 19.1s ／ 英文 15.0s*

**畫面公式**

```
直線上的座標對應   |   the correspondence on a line
O  ,  Q        X  ↦  x        | x |  =  | OX | / | OQ |
```

**旁白（繁中）**

> 先看直線。在一條直線上任選一個零點與一個相異的單位點，那麼線上每個點都對應到一個數：它的絕對值是該點到零點的距離，以零點到單位點那一段為單位；正負則看它與單位點在不在零點的同一側。

**Narration (EN)**

> Start with a line. Choose on it a zero point and a distinct unit point. Then each point gets a number: its size is the distance from the zero point, measured in units of the segment to the unit point, and its sign says which side it lies on.

**動畫**

一條直線上的 O、Q 與座標 2、−0.7 這幾個點，底下標出被當作單位的那一段。

## Beat 2 — 原點與三個單位點 / an origin and three unit points
*配音長度：中文 17.4s ／ 英文 16.8s*

**畫面公式**

```
原點與三個單位點   |   an origin and three unit points
O , Q₁ , Q₂ , Q₃        L₁ , L₂ , L₃
```

**旁白（繁中）**

> 三維的作法一樣。任選一個原點與三個單位點，四個點不共平面。每個單位點決定一條過原點的直線，這三條就是座標軸，而且每條軸上都已經有了剛才那種座標對應。

**Narration (EN)**

> Three dimensions go the same way. Choose an origin and three unit points, the four not lying in a plane. Each unit point determines a line through the origin, and these three are the coordinate axes, each already carrying a correspondence of the kind just described.

**動畫**

軸測投影的三條座標軸，加上三個單位點 Q₁、Q₂、Q₃。

## Beat 3 — 每個點決定一個三元組 / each point determines a triple
*配音長度：中文 20.5s ／ 英文 16.9s*

**畫面公式**

```
每個點決定一個三元組   |   each point determines a triple
θ  :  X  ↦  x  =  ⟨ x₁ , x₂ , x₃ ⟩
```

**旁白（繁中）**

> 現在給空間中任何一個點。過它、平行於第二與第三軸的那個平面，會交第一軸於一點，於是給出第一個座標；同樣的作法給出另外兩個。所以每個點決定一個三元組，這個對應就叫做這組軸系定義的座標對應。

**Narration (EN)**

> Now take any point of space. The plane through it parallel to the second and third axes meets the first axis, giving the first coordinate; the same construction gives the other two. So every point determines a triple, and that is the correspondence defined by the axis system.

**動畫**

書上的 Fig. 1.4：點 X 與它在三條軸上的三個投影足，虛線連回 X。

## Beat 4 — 單位點對到單位向量 / unit points go to unit vectors
*配音長度：中文 13.0s ／ 英文 10.7s*

**畫面公式**

```
單位點對到單位向量   |   unit points go to unit vectors
θ ( Q₁ ) = δ ¹    θ ( Q₂ ) = δ ²    θ ( Q₃ ) = δ ³
```

**旁白（繁中）**

> 值得注意的是，三個單位點的座標三元組，正好就是那三個「只有一個位置是一、其他都是零」的向量。這一點等一下會反覆用到。

**Narration (EN)**

> Worth noticing: the coordinate triples of the three unit points are exactly the vectors with a single one and zeros elsewhere. That fact gets used again and again shortly.

**動畫**

同一組軸，三個單位點旁邊各標出自己的座標三元組——正好就是三個單位向量。

## Beat 5 — 假設一：這是個雙射 / assumption one: it is a bijection
*配音長度：中文 21.6s ／ 英文 16.8s*

**畫面公式**

```
假設一：這是個雙射   |   assumption one: it is a bijection
1 )  θ  :  𝔼³ → ℝ³
```

**旁白（繁中）**

> 接下來有四件關於座標對應的基本事實。嚴格說，它們要先當成幾何定理證出來，才能拿座標去處理幾何問題。但書上說這些幾何定理相當棘手，用中學那套幾何幾乎沒辦法講清楚，所以直接假設它們成立。

**Narration (EN)**

> There are four basic facts about the correspondence. Strictly they must be proved as geometry before coordinates can be used on geometric questions. But the book calls them tricky and almost impossible to discuss on the usual school treatment, so it simply assumes them.

**動畫**

兩欄點一一對應：幾何空間的點，與三元組。

## Beat 6 — 假設二：等價的有向線段 / assumption two: equivalent directed segments
*配音長度：中文 22.6s ／ 英文 18.6s*

**畫面公式**

```
假設二：等價的有向線段   |   assumption two: equivalent directed segments
2 )   AB ∼ XY   ⇔   b − a  =  y − x
```

**旁白（繁中）**

> 第一件：這個座標對應是空間到三維座標空間的雙射。第二件：兩條線段等長、平行而且方向相同，若且唯若它們終點座標減起點座標的結果相同。把有向線段這個概念形式化之後，第二件事就寫成「兩條有向線段等價」。

**Narration (EN)**

> First: the correspondence is a bijection from space onto coordinate three-space. Second: two segments are equal in length, parallel and similarly directed exactly when endpoint minus starting coordinates agree. Formalized, that says the two directed segments are equivalent.

**動畫**

兩條等長、平行、同向的有向線段，畫在畫面的不同位置。

## Beat 7 — 假設三：同一條線上就是純量倍數 / assumption three: on one line means a multiple
*配音長度：中文 17.2s ／ 英文 17.7s*

**畫面公式**

```
假設三：同一條線上就是純量倍數   |   assumption three: on one line means a multiple
3 )   Y ∈ OX   ⇔   y  =  t x        t  =  coord ( Y )
```

**旁白（繁中）**

> 第三件：如果一個點不是原點，那麼另一個點落在過原點與它的那條直線上，若且唯若後者的座標是前者的純量倍數；而且那個純量正好就是後者在這條線上、以前者為單位點時的座標。

**Narration (EN)**

> Third: if a point is not the origin, then another point lies on the line through the origin and it exactly when the second set of coordinates is a scalar multiple of the first. Moreover that scalar is the coordinate of the second point on that line, taking the first as its unit point.

**動畫**

一條過 O 的直線上有 X、Y、Z 三個點，各自是 X 的純量倍數，其中一個是負的。

## Beat 8 — 假設四：畢氏定理給出長度 / assumption four: Pythagoras gives the length
*配音長度：中文 19.2s ／ 英文 16.9s*

**畫面公式**

```
假設四：畢氏定理給出長度   |   assumption four: Pythagoras gives the length
4 )   | OX |  =  ( Σ₁³ xᵢ² ) ¹ᐟ²
```

**旁白（繁中）**

> 第四件要求軸系是笛卡兒的，也就是三軸互相垂直、而且共用同一個長度單位。這時一段從原點出發的線段長度，就由歐氏範數給出——各座標平方和再開根號。這直接來自畢氏定理。

**Narration (EN)**

> The fourth assumes the axes are Cartesian: mutually perpendicular, with a common unit of distance. Then the length of a segment from the origin is the Euclidean norm, the square root of the sum of the squared coordinates. This follows directly from the Pythagorean theorem.

**動畫**

書上的 Fig. 1.5 左半：底面的直角三角形加上直立的那一段，畢氏定理用兩次。

## Beat 9 — 垂直，就是純量積為零 / perpendicular means the scalar product is zero
*配音長度：中文 17.7s ／ 英文 17.1s*

**畫面公式**

```
垂直，就是純量積為零   |   perpendicular means the scalar product is zero
OX ⊥ OY   ⇔   ( x , y ) = 0        ( x , y )  =  Σ₁³ xᵢ yᵢ
```

**旁白（繁中）**

> 把畢氏定理再用一次到原點與兩個點所成的三角形，就得到另一件事：兩段從原點出發的線段互相垂直，若且唯若它們座標的純量積等於零。純量積就是對應座標相乘再加起來。

**Narration (EN)**

> Applying Pythagoras again, to the triangle on the origin and two points, gives another fact: two segments from the origin are perpendicular exactly when the scalar product of their coordinates is zero, that product being corresponding coordinates multiplied and summed.

**動畫**

書上的 Fig. 1.5 右半：三角形 OXY，原點處畫出直角記號。

## Beat 10 — 直線的方程 / the equation of a line
*配音長度：中文 19.8s ／ 英文 17.6s*

**畫面公式**

```
直線的方程   |   the equation of a line
( c x + d y , z ) = c ( x , z ) + d ( y , z )        x  =  t a + b
```

**旁白（繁中）**

> 還有一個很好用的性質：把純量積的其中一個變數固定住，它對另一個變數是線性的。有了這個，直線的方程就出來了：過某一點、平行於某個方向的直線包含一個點，若且唯若座標差是那個方向的純量倍數。

**Narration (EN)**

> One more property is useful: hold either variable of the scalar product fixed and it is linear in the other. Then the equation of a line drops out: the line through a point parallel to a direction contains a point exactly when the coordinate difference is a multiple of that direction.

**動畫**

書上的 Fig. 1.6：過 B 且平行於 OA 的直線，畫出 OA、OB 與線上的一點 X。
