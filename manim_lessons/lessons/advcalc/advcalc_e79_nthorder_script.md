# advcalc E79 — 第 6 章：n 階方程與降階法

Chapter 6: The nth-Order Equation and Reduction of Order

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 4 節「n 階線性方程」的**前半**（書頁 281–284 上半，收在「We now turn to an important tractable case」之前）。習題 4.1–4.19 在 287。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e79_nthorder.py`（`AdvCalcE79ZH` / `AdvCalcE79EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[79]` / `FORMULAS_ADVCALC[79]`）
- 配音：`manim_lessons/samples/audio_e79/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 244.2 秒（4:04）／英文 199.6 秒（3:20）
- YouTube（私人）：中文 https://youtu.be/3RKcCeJwXDk ／英文 https://youtu.be/cpqPJplV7ms

## 切點為什麼在這裡

HANDOFF 原本建議切在**定理 4.1 之後**，但那樣前半只有書頁 281–282、後半 283–287，差太多。
實際的分界在書頁 284 中間那句「We now turn to an important tractable case」：
前面是**沒有常係數時能做什麼**（一階的顯式解、降階法），後面是**常係數的完整顯式答案**。
兩件事的性質不同，切在這裡兩集都是滿的。

## 這半節在做什麼

**先把 n 階壓平成一階。** 這是第 1 節對一階方程做過的事再做一次：

```
ψ f   =   ⟨ f , f ′ , … , f ⁽ ⁿ ⁻ ¹ ⁾ ⟩              ψ  :  N   ≅   𝒩
```

第 1 節定理 1.5 的證明其實已經說完了這件事。而排導數這個動作本身是線性的，
**回頭只要取第一個座標**，所以它是同構，不只是雙射。於是第 3 節的結論全部搬過來：

```
π ₜ ∘ ψ  :  f  ↦  ⟨ f ( t ) , … , f ⁽ ⁿ ⁻ ¹ ⁾ ( t ) ⟩            N   ≅   W ⁿ
```

這就是「**n 個初始值決定唯一一個解**」。

**取 W = ℝ 之後，整件事是一個算子的零化空間。**

```
( L f ) ( t )   =   aₙ ( t ) f ⁽ ⁿ ⁾ ( t )   +   ⋯   +   a ₀ ( t ) f ( t )
```

最高階係數處處不為零就除掉（**正則**）；某個 t 讓它變成零的**奇異**情形要另外的理論，
這本書不碰。**定理 4.1** 把一般理論在這裡的樣子收攏：L 是滿射、N 的維數是 n、
在任一時刻取值都是 N ≅ ℝⁿ、而 M ₜ ₀ 是補並決定一個線性右反元素。

**然後轉向實務，而且很老實。** 找 N 的基底**沒有一般的方法**。三件事有用：

1. **一階直接積出來**：y ′ / y 就是 ( log y ) ′，所以 y = exp ( − ∫ a )。
2. **常係數有完整答案**——那是 E80。
3. **中間：降階法。** 已知一個解 u，找 v = c u：

```
L ( v )   =   c L ( u )   +   S ( c ′ )   =   S ( c ′ )
```

不帶 c 的導數的那些項合起來是 c L ( u )，**正好是零**，剩下的是一個 n − 1 階的 S 作用在 c ′ 上。
取 S 零化空間的基底 g ᵢ、令 c ᵢ = ∫ g ᵢ，就得到 n − 1 個新解，與 u 一起獨立。

**但這個手法不能往上疊。** 書上說它「works off the top instead of off the bottom」——
要疊得先從一個 n 階算子找出 N ( S ) ⊂ N ( L ) 的一階 S，一般辦不到。
**所以二階特別好**：找到一個解就全部解完，因為剩下的是一階。

## 這一集用的例子

主例是書上的 **y ″ − 2 y / t ² = 0**（區間不含原點，因為 a ₀ = − 2 / t ² 在那裡不連續），
一眼看出 u = t ²，降階後得到 v = 1 / t。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| t ² 與 1 / t 都是解 | 四個 t 的數值二階導數 | 殘差 < 1e-6 |
| 兩者獨立 | u v ′ − u ′ v 在四個 t | 一直是 **− 3** |
| 同值不同導數 | t ₀ = 1 | u = v = 1，u ′ = +2、v ′ = −1 |
| 取值矩陣可逆 | 2 × 2 行列式 | −3（= Wronskian）|
| 三個初始斜率各給一個解 | A、B 解出來再代回 | 三組 A 互不相同 |
| 定理 4.1 的右反元素 | L ( R g ) 對 g = 1 | 差 < 1e-4，且 R g ( t ₀ ) = R g ′ ( t ₀ ) = 0 |
| 仿射家族 | R g + A t ² + B / t 四組 | 全部解同一個非齊次方程 |
| 一階公式 | a = 1 / t 與 a = 2 t | y ′ + a y 殘差 < 1e-6 |
| **降階等式**（關鍵）| **拿一個不是答案的 c = sin t**，比 L ( c u ) 與 S ( c ′ ) | 逐列相同（< 2e-3）|
| 降階後的方程 | S ( t ⁻ ⁴ ) | < 1e-6 |
| c u 就是 1 / t | 差一個純量 −1/3 | 完全相同 |

**降階那一條是刻意拿「不是答案的 c」去驗的。** 用答案驗只證明答案對，
用任意的 c 驗才證明「c L ( u ) 那一塊真的消掉、剩下的真的只含 c ′ 」這個**恆等式**。

奇異的例子是 **t y ″ + y ′ = 0**（a ₂ ( t ) = t 在原點變成零）。第一積分是 ( t y ′ ) ′ = 0，
所以 y ′ = k / t：

| t | y = log t | y ′ |
|---|---|---|
| 0.50 | −0.6931 | 2.00 |
| 0.20 | −1.6094 | 5.00 |
| 0.05 | −2.9957 | 20.00 |
| 0.01 | −4.6052 | 100.00 |

**除了常數解以外 y ′ 在原點附近爆掉**，所以解空間在不含原點的區間上是 2 維，
一含進原點就掉成 1 維。這正是正則那個假設在買的東西。

## 這一輪抓到的錯

- **五張表的最後一列壓到說明話。** 八列的表用 `dy = 0.26`、`y0 = 0.90`，
  最後一列落在 −0.92，而 `_cap` 在 −0.90。收成 `dy = 0.23`（最後一列 −0.71）。
  這是這個版面反覆出現的一類，**列數一多就要重算最後一列的 y**，不能沿用別拍的間距。
- **刪除線畫在方塊自己的字上。** 第 9 拍原本用一條 WARN 線把「c L ( u )」劃掉，
  collide 直接報 `stroke/text Line through 'c L(u)'`。
  改成**把零說出來**：方塊直接寫「c L ( u ) = 0」並塗成 WARN，線拿掉。
  （劃在字上會被判成碰撞，劃在兩列之間就是 E52 那個錯——這類記號不要用線畫。）
- **第 9 拍的標籤頂到 y = 1.31。** 上限是 1.30。整張圖的 `oy` 從 0.34 降到 0.26。
- **`_column` 的括號比內容窄，字被穿過去（只有 1080p 看得出來）。** 第 1 拍那一欄的最後一項
  `f ⁽ ⁿ ⁻ ¹ ⁾` 寬 0.71，而 `arrays.py` 的 `_column` 把括號固定放在中心 ±0.34。
  480p 的 probe 幀看不出來，1080p 一眼就看到。改成在場景裡自己排那一欄、
  再用 `_brackets` 依內容給 ±0.50。**為此重渲了一次（兩支約一小時）。**
  規則：`_column` 只適合窄內容，長一點的自己排。
- **`_plot` 這個 helper 是為了 E75 那個錯寫的。** E75 有一個 helper 裡 `ox` 是「t = 0 的位置」、
  另一個裡是「左邊界」，兩拍的曲線因此跑出畫面。這一集的 `_plot` 把 t 的範圍當參數，
  **ta 固定映到圖的左邊界**，畫面上哪裡是 t = 0 不必假設。

## 十一拍

### 第 1 拍 — 第 4 節：n 階線性方程 / section 4: the nth-order equation

公式列：

```
d ⁿ α / d t ⁿ   =   G ( t , α , d α / d t , … , d ⁿ ⁻ ¹ α / d t ⁿ ⁻ ¹ )
```

中文旁白：第 6 章第 4 節：n 階線性方程。方程是 α 的 n 階導數等於 G，而 G 對 α 與它的各階導數是線性的。老辦法照樣管用：把 f 和它的前 n 減一階導數排成一個 n 元組，n 階方程就變成第 3 節那種一階系統。

English: Section 4 of chapter 6: the nth-order linear equation. The nth derivative of alpha equals G, which is linear in alpha and its lower derivatives. The old device works: line f up with its first n minus one derivatives and it becomes a first-order system.

### 第 2 拍 — ψ 把兩個解空間接起來 / psi joins the two solution spaces

公式列：

```
ψ f  =  ⟨ f , f ′ , … , f ⁽ ⁿ ⁻ ¹ ⁾ ⟩              ψ  :  N   ≅   𝒩
```

中文旁白：第 1 節定理 1.5 的證明其實已經把這件事說完了：f 是 n 階方程的解，若且唯若那個 n 元組是一階系統的解。而排導數這個動作本身是線性的，所以 ψ 把 n 階方程的解空間同構地搬到一階系統的解空間上。

English: The proof of Theorem 1.5 already said this: f solves the nth-order equation exactly when that n-tuple solves the first-order system. Lining up derivatives is itself linear, so psi carries the solution space isomorphically onto the first-order one.

### 第 3 拍 — n 個初始值決定唯一一個解 / n initial values, exactly one solution

公式列：

```
π ₜ ∘ ψ  :  f  ↦  ⟨ f ( t ) , … , f ⁽ ⁿ ⁻ ¹ ⁾ ( t ) ⟩            N   ≅   W ⁿ
```

中文旁白：第 3 節說一階系統的解由它在某一個時刻的值唯一決定。兩件事合起來：把 f 送成它在 t 的值連同前 n 減一階導數在 t 的值，是解空間到 W 的 n 次冪的同構。這就是「n 個初始值決定唯一一個解」這句話。

English: Section 3 said a solution of the system is fixed by its value at one instant. Putting the two together, sending f to its value at t together with its first n minus one derivatives there is an isomorphism onto W to the n: n initial values, exactly one solution.

### 第 4 拍 — 取 W 是實數線：一個算子 L / taking W real: a single operator

公式列：

```
( L f ) ( t )  =  aₙ ( t ) f ⁽ ⁿ ⁾ ( t )  +  ⋯  +  a ₀ ( t ) f ( t )
```

中文旁白：接著取 W 是實數線。這時 G 在每個 t 是一個線性函數，係數是 n 個連續函數，於是解空間正好是一個線性變換 L 的零化空間。把指標挪一挪對齊導數的階數，L 就寫成 a n 乘 f 的 n 階導數，一路加到 a 零乘 f。

English: Now take W to be the real line. Then G is a linear function at each t with n continuous coefficients, so the solution space is exactly the null space of a linear transformation. Shifting indices to match the orders, it runs from the nth derivative down to f.

### 第 5 拍 — 正則與奇異 / regular and singular

公式列：

```
t  y ″  +  y ′  =  0        a ₂ ( t )  =  t        dim N  =  2  →  1
```

中文旁白：最高階的係數如果處處不為零，就可以把它除掉，這叫正則的情形；某個 t 讓它變成零的奇異情形要另外的理論，這本書不碰。左邊是個奇異的例子：在不含原點的區間上解空間是二維的，一把原點含進來就掉成一維。

English: If the top coefficient never vanishes we divide it out: the regular case. The singular case needs further study and the book leaves it alone. The example on the left is singular: its solution space is two-dimensional away from the origin, one-dimensional once the origin is in.

### 第 6 拍 — 定理 4.1 / theorem 4.1

公式列：

```
L [ 𝒞 ⁿ ( I ) ]  =  𝒞 ⁰ ( I )        𝒞 ⁿ ( I )  =  N  ⊕  M ₜ ₀        dim N  =  n
```

中文旁白：定理 4.1 把一般理論在這裡的樣子收攏起來：L 是從 n 次連續可微函數到連續函數的滿射；零化空間就是解空間，維數是 n；在任一個時刻取值都給出它到 n 維空間的同構；而在那個時刻連同前 n 減一階導數全為零的函數構成一個補，並決定 L 的一個線性右反元素。

English: Theorem 4.1 gathers what the general theory says here. The operator is onto the continuous functions; its null space is the solution space, of dimension n; evaluation at one instant is an isomorphism onto n-space; and the functions vanishing there form a complement.

### 第 7 拍 — 實務上分成兩件事 / the problem splits in two

公式列：

```
L ( f )  =  g            L ( v )  =  g            f   ∈   v  +  N
```

中文旁白：從這裡開始是實務問題。要解 L 作用在 f 上等於 g，得分成兩件事：一是找出解空間的一組基底，也就是解齊次方程；二是找出 L 的一個右反元素，也就是替每個 g 挑一個解。有了一個特解，全部的解就是解空間平移過去的仿射子空間。

English: From here the problem is practical. Solving the equation splits in two: find a basis for the solution space, which is the homogeneous problem, and find a right inverse, which picks one solution for each right-hand side. With one particular solution, all of them form an affine subspace.

### 第 8 拍 — 一階：直接積出來 / order one: integrated outright

公式列：

```
y ′  +  a ( t ) y  =  0              y  =  exp ( − ∫ a ( t ) d t )
```

中文旁白：先看第一件。很遺憾沒有一般的方法，只能部分成功。一階的情形可以直接解：y 一撇加 a 乘 y 等於零，而 y 一撇除以 y 就是 log y 的導數，所以 y 等於 e 的「負 a 的積分」次方。書上那個例子的解是 t 的倒數，也可以一眼看出來。

English: Take the first part. Unhappily there is no general method, only partial success. The first-order case goes through directly: since y prime over y is the derivative of log y, the solution is the exponential of minus the integral of the coefficient. The book's example gives one over t.

### 第 9 拍 — 降階法 / reduction of order

公式列：

```
v  =  c u            L ( v )  =  c L ( u )  +  S ( c ′ )  =  S ( c ′ )
```

中文旁白：再看 n 階。假設已經知道一個解 u，就找 c 乘 u 這種形式的第二個解。把各階導數用 Leibniz 公式展開代進 L，不帶 c 的導數的那些項合起來是 c 乘 L 作用在 u 上，那一塊是零；剩下的可以寫成一個 n 減一階的算子作用在 c 一撇上。

English: Now order n. Suppose one solution is known and look for a second of the form c times it. Expand by Leibniz and substitute: the terms with no derivative of c add up to c times the operator applied to the known solution, which is zero. The rest has order n minus one.

### 第 10 拍 — 為什麼低一階就夠了 / why one order less suffices

公式列：

```
c ᵢ ( t )  =  ∫ g ᵢ ( s ) d s          L ( c ᵢ u )  =  S ( g ᵢ )  =  0
```

中文旁白：所以解 S f 等於零這個低一階的方程就夠了。取 S 的零化空間的一組基底，各自積分得到係數函數，那麼 L 作用在係數乘 u 上等於 S 作用在基底上等於零，而 u 與這些新解一起是獨立的。要注意這個手法不能一層層疊下去：它是從上面削，不是從下面長。

English: So it is enough to solve that lower-order equation. Take a basis of its null space, integrate each one, and the operator kills each coefficient times the known solution, which is independent of it. It does not stack up though: it works off the top, not the bottom.

### 第 11 拍 — 二階：找到一個解就全解完了 / order two: one solution finishes it

公式列：

```
y ″  −  2 y / t ²  =  0              N  =  ⟨ t ²  ,  1 / t ⟩
```

中文旁白：二階的情形因此只要找到一個解就全部解決，因為剩下的是一階方程。書上的例子看一眼就知道 t 平方是一個解；代進去之後方程變成 c 一撇的一階方程，解出來第二個解是 t 的倒數。兩個解在某一點的值相同也沒關係，重要的是值與導數配成的對。

English: A second-order equation is therefore completely solved once one solution is found, since what remains is first order. In the book's example one solution is visible by inspection, substituting turns the problem into a first-order one for c prime, and the second solution is one over t.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | f 一個方塊 → ⟨ f , f ′ , ⋮ , f ⁽ ⁿ ⁻ ¹ ⁾ ⟩ 一個帶括號的欄，再往下接 W ⁿ |
| 2 | N 與 𝒩 兩個方塊，上箭頭 ψ、下箭頭 π ¹——**兩個箭頭互為反元素才是同構** |
| 3 | 三條解在 t ₀ 交於同一點，斜率 +2 / −1 / +0.5；右表列出各自的 A、B |
| 4 | a ₂ ≡ 1 一條水平線、a ₀ = −2 / t ² 一條曲線。**a ₁ ≡ 0 沒有畫**，因為它就是那條軸 |
| 5 | y = 1 與 y = log t 兩條；右表的 y ′ 欄 2 → 5 → 20 → 100 一路衝上去 |
| 6 | 𝒞 ⁿ ( I ) ⇄ 𝒞 ⁰ ( I ) 兩個方塊（L 去、R 回），下面 N ⊕ M ₜ ₀ 把左邊拆成兩半 |
| 7 | 橘線是 R g（在 t ₀ 值與斜率都是零），三條灰線是它加上齊次解——只差一個 N 的元素 |
| 8 | 1 / t 與 exp ( − t ² ) 兩條，分別對應 a = 1 / t 與 a = 2 t；右表是代回去的殘差 |
| 9 | L ( c u ) 分成上下兩個方塊：上面「c L ( u ) = 0」塗成紅、下面 S ( c ′ ) 標著 n − 1 |
| 10 | L : 2 與 S : 1 兩個方塊，往下的箭頭可以走、往上的被紅叉打掉，底下問 N ( S ) ⊂ N ( L ) ? |
| 11 | t ² 與 1 / t 在 t ₀ 交叉，交點上兩支箭頭朝不同方向（斜率 +2 與 −1）；右表行列式一直是 −3 |
