# advcalc E82 — 第 6 章：邊界值問題與形式自伴

Chapter 6: The Boundary-Value Problem and Formal Self-Adjointness

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 6 章第 6 節「邊界值問題」的**前半**（書頁 294 下半–297 上半）。習題 6.1–6.12 在 300–301。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e82_boundary.py`（`AdvCalcE82ZH` / `AdvCalcE82EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[82]` / `FORMULAS_ADVCALC[82]`）
- 配音：`manim_lessons/samples/audio_e82/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 266.3 秒（4:26）／英文 201.7 秒（3:22）
- YouTube（私人）：中文 https://youtu.be/b33wWQW92TY ／英文 https://youtu.be/STb24Y9Y7ic

## 這半節在做什麼

**邊界值問題看起來像初值問題，性格完全不同**：初值在同一點給 f 與 f ′，邊值在兩端各給一個 f。
書上直說讀者從初值那套理論完全看不出該怎麼辦，得另造工具——而那個工具是純量積與自伴算子。

**形式伴隨來自分部積分**：把 f 身上的導數一次一個搬到 g 上，端點留下的值累積成 B。

```
( T f , g )   =   ( f , R g )   +   B ( f , g ) | ᵃ ᵇ
```

每做一次分部積分就帶一個負號，所以 R 的首項係數是 ( −1 ) ⁿ 乘 T 的——**n 必須是偶數**。
二階算出來之後得到 **引理 6.2**：

```
T 形式自伴   ⟺   c ₁ = c ₂ ′   ⟺   T f = ( c ₂ f ′ ) ′ + c ₀ f
B ( f , g )  =  c ₂ ( f ′ g − g ′ f )
```

**引理 6.1** 再把算子的性質換成邊界條件的性質：右逆自伴 ⟺ f , g ∈ M ⇒ B | ᵃ ᵇ = 0。
於是可以直接寫下四組自伴邊界條件。**引理 6.3** 把「M 是補」換成比較好驗的「T 在 M 上單射」。

## 這一集用的例子

主例是 c ₂ = 1 + t ²、c ₀ = −1 在 [ 0 , 1 ] 上（自伴），另備一組 c ₁ = 1（不自伴）作對照。

| 要驗的事 | 結果 |
|---|---|
| ( T f , g ) − ( f , R g ) = B \| ᵃ ᵇ | 差 < 1e-12 |
| **‖ R g − T g ‖（真的算，不是按奇偶填）** | n = 1：4.0000、n = 2：0、n = 3：9.8260、n = 4：0 |
| 自伴那組 R = T | 逐點相等 |
| 不自伴那組 R ≠ T | 差 2.400 |
| 四組邊界條件的 B \| ᵃ ᵇ | 全是 0（≤ 2.1e-15）|
| 一組**不滿足**的邊界條件 | B = −6.1723 |
| 三個行列式（引理 6.3）| 都不是零 |

## 這一輪抓到的錯

- **分部積分的第一列漏了 c ₂。** 三列原本是 `f ″ g` / `− f ′ ( c ₂ g ) ′` / `+ f ( c ₂ g ) ″`，
  可是書頁 296 是 `∫ c ₂ f ″ g = c ₂ f ′ g | ᵃ ᵇ − ∫ f ′ ( c ₂ g ) ′`；第一列若真是 `f ″ g`，
  搬一次只會得到 `− ∫ f ′ g ′`，**推不出第二列**。
- **`‖ R g − T g ‖` 那一欄是按 n 的奇偶寫死的**，而 assert 只是在驗那個寫法本身
  （`(s < 1e-15) == (n % 2 == 0)`）。改成把 R 與 T 建成函數再逐點相減，assert 也改成
  雙向檢查（偶數 < 1e-15、奇數 > 1）。
- **「允許的 λ」長條從一個本身不允許的點畫起。** 不允許的只有離散的幾個零點，
  λ = −5 完全合法卻落在橘線之外。改成畫滿整條軸、在紅點處斷開。
- **說明話指著一個不存在的差**：「倒數第二列是最大的差」，可是兩欄逐列相等。
  改成講「第三列的數值最大」。**中英兩半都改**（第一次只改了中文）。

## 十一拍

### 第 1 拍 — 邊界值問題：資料換了位置 / the boundary-value problem: the data moves

公式列：

```
T ( f )  =  g            f ( t ₀ )  ,  f ′ ( t ₀ )        ⟷        f ( a )  ,  f ( b )
```

中文旁白：現在換一種問題。要解的還是 T 作用在 f 上等於 g，但給定的條件換了位置：初始值問題在同一個點上給 f 的值與 f 一撇的值，邊界值問題則是在區間的兩個端點各給一個 f 的值。物理裡最重要的那些問題，幾乎都是後面這一種。

English: The equation is still T of f equals g, but the data moves. The initial-value problem gives a value and a slope at one single point. The boundary-value problem gives one value at each end of the interval. Most of the important problems in physics are of this second kind.

### 第 2 拍 — 同樣想拆成兩個子問題 / the same split into two subproblems

公式列：

```
M  =  { f ∈ 𝒞 ² [ a , b ]  :  f ( a )  =  f ( b )  =  0 }        M  ⊕  N ( T )  =  ?
```

中文旁白：邊界值問題看起來也能像初始值問題那樣拆成兩個子問題：只要那個在兩端都歸零的函數集合 M，恰好是 T 的零化空間的補空間就行。可是書上提醒，從初始值那一套理論完全看不出該怎麼判斷它是不是補空間，得另外造一套工具。

English: It looks as though this splits into two subproblems too, provided the set of functions vanishing at both ends is a complement of the null space of T. But the book warns that the initial-value theory gives no clue how to decide that, so new tools are needed.

### 第 3 拍 — 換個觀點：純量積與自伴 / a new viewpoint: scalar products and self-adjointness

公式列：

```
( f , g )   =   ∫ ᵃ ᵇ  f g  d t            S  :  𝒞 ⁰  →  M        S  =  S *
```

中文旁白：新工具是純量積與自伴算子。把兩個函數的乘積從 a 積到 b，當成它們的內積；如果 T 在這個內積下是自伴的，那麼適當選的 M 會讓右逆同時是自伴而且緊的算子，第 5 章定理 5.1 就能原封不動地搬過來用。

English: The new tools are the scalar product and self-adjoint operators. Integrate the product of two functions from a to b. If T is self-adjoint for that product, a good choice of M makes the right inverse self-adjoint and compact, and Theorem 5.1 of chapter 5 applies.

### 第 4 拍 — 分部積分把導數搬過去 / integration by parts moves the derivatives across

公式列：

```
( T f , g )   =   ( f , R g )   +   B ( f , g ) | ᵃ ᵇ
```

中文旁白：自伴到底是什麼意思，要先算出來。用分部積分，把 f 身上的導數一次搬一個到 g 身上；搬完以後 f 不帶導數，g 被某個 n 階算子 R 作用著，端點留下的值累積成一個 B。於是 T f 與 g 的內積，等於 f 與 R g 的內積加上 B 在兩端的差。

English: Integration by parts shifts the derivatives off f onto g one at a time. At the end f carries none, g is acted on by an operator R of order n, and the endpoint values pile up into a quantity B. So T f against g equals f against R g, plus B across the two ends.

### 第 5 拍 — 形式伴隨，以及 n 的奇偶 / the formal adjoint, and the parity of n

公式列：

```
R g   =   Σ ᵢ  ( − 1 ) ⁱ  ( a ᵢ g ) ⁽ ⁱ ⁾            ( − 1 ) ⁿ  a ₙ
```

中文旁白：R 叫做 T 的形式伴隨；如果 R 剛好就是 T，就說 T 是形式自伴的。每做一次分部積分都帶一個負號，所以 R 的首項係數是負一的 n 次方乘上 T 的。要讓兩個算子連最高階那一項都對得起來，n 就必須是偶數。畫面上是一階的情形，兩條曲線差一個負號。

English: That R is the formal adjoint of T, and if R is T itself we call T formally self-adjoint. Each integration by parts brings a sign change, so the leading coefficient of R is minus one to the n times that of T. For the two to agree there, n has to be even.

### 第 6 拍 — 二階的情形算出來 / the second-order case, computed

公式列：

```
T f  =  c ₂ f ″ + c ₁ f ′ + c ₀ f        R g  =  ( c ₂ g ) ″ − ( c ₁ g ) ′ + c ₀ g
```

中文旁白：以下只看二階。T f 是 c 二乘 f 兩撇加 c 一乘 f 一撇加 c 零乘 f。分部積分兩次後 R g 是 c 二 g 的二階導數減 c 一 g 的一階導數加 c 零 g。端點項是 c 二乘 f 一撇 g 減 g 一撇 f，加 c 一減 c 二一撇乘 f g。

English: From here on, only the second order. T f is c two times f double prime, plus c one f prime, plus c zero f. Two integrations by parts give R g as the second derivative of c two g, minus the first derivative of c one g, plus c zero g. The ends give B.

### 第 7 拍 — 引理 6.2：形式自伴的判準 / Lemma 6.2: the test for formal self-adjointness

公式列：

```
R  =  T      ⟺      c ₁  =  c ₂ ′            T f   =   ( c ₂ f ′ ) ′  +  c ₀ f
```

中文旁白：引理 6.2：二階算子形式自伴，若且唯若 c 一等於 c 二一撇。這時 T f 可以寫成 c 二 f 一撇的導數再加 c 零 f，端點項只剩 c 二乘上 f 一撇 g 減 g 一撇 f。畫面上畫的是 c 一減 c 二一撇這條差：自伴那組恆等於零，另一組是斜線。

English: Lemma 6.2: a second-order operator is formally self-adjoint exactly when c one is the derivative of c two. Then T f is the derivative of c two f prime, plus c zero f. The picture plots that difference of coefficients: zero everywhere for one example, a line for the other.

### 第 8 拍 — 引理 6.1：換成邊界條件 / Lemma 6.1: trade it for a boundary condition

公式列：

```
f , g  ∈  M      ⇒      B ( f , g ) | ᵃ ᵇ   =   0
```

中文旁白：引理 6.1 把算子的性質換成邊界條件的性質。設 T 形式自伴，而 M 是零化空間的補空間；那麼 M 決定的右逆是自伴算子，若且唯若 M 裡任意兩個函數的 B 在兩端的差都是零。推導只有一行：把兩個內積都展開，自伴的那一項自動相消，剩下來的就只有 B。

English: Lemma 6.1 trades a property of the operator for a property of the boundary condition. Let T be formally self-adjoint and M a complement of the null space. The right inverse it determines is self-adjoint exactly when B across the ends vanishes for every pair in M.

### 第 9 拍 — 四組自伴邊界條件 / four self-adjoint boundary conditions

公式列：

```
B ( f , g )   =   c ₂ ( f ′ g  −  g ′ f )
```

中文旁白：於是可以直接寫下好幾組自伴的邊界條件。第一組，兩端的函數值都是零。第二組，兩端的斜率都是零。第三組更一般，斜率在每一端各自正比於函數值，兩邊的比例可以不同。第四組要 c 二在兩端相等，條件是函數值與斜率都週期性地相等。右邊逐組算出來，全都是零。

English: Several self-adjoint boundary conditions follow at once. First, the function vanishes at both ends. Second, the slope vanishes at both ends. Third, the slope at each end is proportional to the value there, with unrelated ratios. Fourth, a periodic match at the ends.

### 第 10 拍 — 引理 6.3：補空間換成單射 / Lemma 6.3: complement becomes injective

公式列：

```
f   ↦   ⟨ l ₁ ( f ) , l ₂ ( f ) ⟩        N   ≅   ℝ ²        dim N  =  2
```

中文旁白：引理 6.3 說，條件 a，也就是 M 是零化空間的補，可以換成條件 a 一撇，也就是 T 限制在 M 上是單射。理由是：單射表示 M 與零化空間只交於零，於是那個把 f 送到兩個泛函值的映射在零化空間上也是單射；而零化空間是二維的，單射就等於是到平面的同構。

English: Lemma 6.3 replaces condition a, that M is a complement of the null space, by a prime, that T is injective on M. Injectivity means M meets the null space only at zero, so the map sending f to its two functional values is injective on a two-dimensional space.

### 第 11 拍 — 收尾：把 T 換成 T 減 λ / closing: replacing T by T minus lambda

公式列：

```
T  −  λ            ( 1 )  ,  ( 2 )  ,  ( 4 )            c ₂  ≥  m  >  0
```

中文旁白：最後補一句。前面那四組條件裡，第一、第二、第四組在 T 換成 T 減 λ 之後，單射這個性質仍然成立；第三組也成立，但證明比較難，書上略過。畫面上那條打靶函數的零點，就是少數幾個不能用的 λ。下一集就拿這些條件證出右逆真的是緊的自伴算子。

English: Of those four conditions, the first, second and fourth keep injectivity when T is replaced by T minus lambda; so does the third, by a harder argument the book omits. The zeros of the shooting function on screen are the few values of lambda not allowed.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 初值與邊值兩張小圖並排：一點給值與斜率 vs 兩端各給一個值 |
| 2 | 拆成兩個子問題的示意，紅色那一列是舊理論答不出來的那一句 |
| 3 | 純量積與自伴算子這條路線的方塊圖，第四列是「右逆同時自伴且緊」 |
| 4 | 分部積分的階梯：導數一次一個從 f 搬到 g，右表逐列比對兩種寫法 |
| 5 | T g = g ′ 與 R g = − g ′ 兩條互為負號；右表的 ‖ R g − T g ‖ 奇數列不是零 |
| 6 | c ₁ − c ₂ ′ 這條差：自伴那組恆為零、不自伴那組是斜線 |
| 7 | 引理 6.1 的兩欄對照，第四欄是不滿足的那一組 |
| 8 | 四組自伴邊界條件各畫一個函數，第五列是不滿足的對照組 |
| 9 | f ↦ ⟨ l ₁ ( f ) , l ₂ ( f ) ⟩ 在 N 上的單射示意，三個行列式都不是零 |
| 10 | 打靶函數 λ ↦ f ( b ) 的零點（紅點），橘色長條滿軸延伸、在紅點處斷開 |
