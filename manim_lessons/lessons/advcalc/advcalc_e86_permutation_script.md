# advcalc E86 — 第 7 章：置換與正負號

Chapter 7: Permutations and the Sign

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 7 章第 3 節「置換」與第 4 節「置換的正負號」（書頁 308 下半到 310 上半），從「A permutation on a set S is a bijection」起，到第 5 節「交錯張量的子空間」開始之前為止。**這兩節都沒有習題。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e86_permutation.py`（`AdvCalcE86ZH` / `AdvCalcE86EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[86]` / `FORMULAS_ADVCALC[86]`，由主控從 `nar_e86.py` 合併）
- 配音：`manim_lessons/samples/audio_e86/`（zh-TW `-4%`、en `-4%`）— 尚未產生
- 片長：中文 277.4 秒（4:37）／英文 198.1 秒（3:18）
- YouTube（私人）：中文 https://youtu.be/aGaCTI4amHo ／英文 https://youtu.be/6OVJ3enoSEI


## 這半節在做什麼

第 3 節與第 4 節併成一集，因為它們是同一個論證。**第 3 節是有限集合上的純群論**——封閉、
反元素、單位元、個數 n 階乘，再加上一個「固定一個元素右乘是雙射」的小引理（以後換和式的指標靠它）——
最後讓一個置換作用到多重線性泛函上：

```
( f · σ ) ( ξ )   =   f ( ξ ∘ σ ⁻ ¹ )
```

**第 4 節把這個作用套到一個特別的多項式上，讀出一個正負號**：

```
E ( x )   =   ∏  ( x ᵢ  −  x ₖ )            i  <  k
E ( x ∘ σ )   =   ( − 1 ) ʳ  E ( x )   =   ( sgn σ )  E ( x )
```

單看任何一半都撐不起一集；合起來正好是第 7 章需要的東西，因為**「交錯」就是用這個正負號定義的**，
而行列式是唯一的交錯 m 重形式。

書上有兩個地方看起來像排版、其實是全部的內容。

**第一個是定義裡那個反元素。** 如果用 σ 自己而不是 σ ⁻ ¹，引理 3.1 的順序就翻過來：

```
f ( ξ ∘ σ )        ⇒        f · ( σ ₁ σ ₂ )   =   ( f · σ ₂ ) · σ ₁
```

第 5 拍把兩種定義都算出來，並且數出有幾對不成立。

**第二個是定理 3.1 裡的「反」字。** T 把乘積的順序顛倒：

```
T ( ρ σ )   =   T ( σ )  ∘  T ( ρ )
```

要讓這個字在畫面上有證據，就得把錯的順序也算出來。第 6 拍兩條路線的終點真的不一樣，
而且右表給出差距的大小。為了讓上標好讀，畫面上把這個作用寫成**右作用** `f · σ` 而不是舉高的 σ：
一來那個字元（U+1D5F）沒有任何一集驗過，二來右作用正是這些算子反序複合的誠實理由。

## 這一集用的例子：全部用 itertools.permutations 真的列舉出來

**沒有任何一張寫死的表。** 群公理是對 S ₄ 的全部 576 對與 13824 組三元組驗的；
24 個置換全部實際分解成對換再乘回去；長度 5 以內的**所有**分解用廣度優先搜尋找出來，
所以「奇偶不變」是關於每一種分解的陳述，不是關於演算法剛好吐出來的那一種。

| 要驗的事 | 結果 |
|---|---|
| 複合之後還在 S ₄ 裡 | 576 / 576 |
| 每個都有雙邊反元素 | 24 / 24 |
| 結合律 | 13824 / 13824 |
| 24 個置換都分解得成對換 | 24 / 24（重組後逐一比對） |
| 長度 ≤ 5 的分解可以到達的置換 | 24 / 24 |
| **同一個 σ 的分解長度** | σ = ( 2 , 3 , 4 , 1 )：**只可能是 3 或 5**，奇偶一樣 |
| 最短長度的分布（k = 0,1,2,3） | 1 , 6 , 11 , 6 —— 合計 24 |
| 最短長度的奇偶 = 用顛倒數定義的 sgn | 24 / 24 |
| 右乘固定元素是雙射 | S ₃：6 / 6；S ₄：24 / 24（左乘 24 / 24） |
| n ! 對照列舉個數（n = 1…6） | 1 2 6 24 120 720（兩欄完全一樣） |
| 係數陣列作用 = 逐點定義 | 差 8.9e-16 |
| **引理 3.1（用 σ ⁻ ¹）** | 差 0.0e+00，36 / 36 成立 |
| **不用反元素** | 差 **3.009**，**18 / 36 不成立** |
| 不用反元素、但把順序寫反 | 差 0.0e+00，36 / 36 成立 |
| **反同態 T ( ρ σ ) = T ( σ ) ∘ T ( ρ )** | 差 0.0e+00，0 / 36 不成立 |
| **反過來的順序 T ( ρ ) ∘ T ( σ )** | 差 **3.009**，**18 / 36 不成立** |
| 不成立的對數 = 不可交換的對數 | 18 + 18 = 36 |
| T ( σ ⁻ ¹ ) ∘ T ( σ ) = I | 差 0.0e+00 |
| 引理 3.2：( μ ( p ) ) · σ = μ ( p ∘ σ ) | 48 / 48（m = 2、n = 3，S ₃ 的 6 個 × 8 個基底） |
| 那個 σ 把 8 個基底分成 | 兩個三元環 + 兩個不動點（畫成同一個圈上的八個點） |
| **E ( x ∘ σ ) = ( sgn σ ) E ( x )** | **S ₄ 全部 24 個**，最大差 2.7e-15 |
| σ 與 σ ⁻ ¹ 的顛倒數相同 | 24 / 24（所以用 x ∘ σ 或 x ∘ σ ⁻ ¹ 正負號一樣） |
| 交點數 = 顛倒數 | 第 9 拍的四條線：3 個交點，inversions = 3 |
| **sgn 的乘法性** | 全部 576 / 576 對；另外隨機 50 對也全過 |
| **對換的 sgn = − 1** | S ₄ 的全部 6 個對換 |
| 偶／奇各半，乘對換跳邊 | 12 / 12，且 τ 把偶的那半整個送到奇的那半 |
| Ω 的秩 = C ( m , n ) | (3,2) → 3、(3,3) → 1、(3,4) → 0 |
| Ω 是投影（Ω ∘ Ω = Ω） | 最大差 3e-17 |
| 投影後的陣列反對稱、對角線為零 | 兩者都 < 1e-12，且與平均公式算出來的一致 |

第 5、6 兩拍那四列粗體是這一集的重點：**「為什麼要反元素」與「為什麼是反同態」，
在畫面上都有一個算出來的非零差距當證據**，不是口頭宣稱。

## 這一輪抓到的錯

- **三個 `_table()` 呼叫漏掉外層的 tuple**（`_biject`、`_basis`、`_poly`），
  變成把七、八個 row 當成七、八個位置參數傳進去。直接的症狀是 `SyntaxError`，
  但**更危險的是它同時吞掉了 `dy=`**：只補括號而不補 `dy`，就會吃到預設的 `dy = 0.30`，
  七列的最後一列落在 0.90 − 6 × 0.30 = **−0.90**，正好壓在 `_cap` 上。補括號時一併把
  `y0 / dy / size` 補齊
  （七列 `dy=0.26`、八列 `dy=0.23`）。
- **廣度優先搜尋找到的「第二種分解」是補出來的，不是另一種。**
  長度 5 的 witness 是 `( 1 2 ) ( 1 2 ) ( 1 2 ) ( 2 3 ) ( 3 4 )` ——
  把同一個對換重複三次，數學上沒錯，但畫面上要講「寫法不只一種」時它等於沒說。
  `assert len(set(DEC[5])) == 5` 抓到，改成窮舉所有長度 5 的乘積、取五個互不相同的那一種。
  **規則：「不唯一」這種話，要給一個真的不一樣的見證。**
- **第 1 拍的說明話說「四個分數」，右表只有三個分數**（第四列是單位元，不是分數）。
  中英兩半同一次改成「三個」。
- **第 4 拍的選擇樹最右邊那片葉子標籤撞到右側的「× 1」**（兩者右緣只差 0.03）。
  把樹的間距從 0.55 收到 0.46、整棵往左挪，並讓每個第一層節點落在它那兩片葉子的中點上
  ——原本是寫死的三個 x，邊線只是「指向附近」而不是接到點上。
- **第 5 拍的 `σ ₂` 離它要標的那支箭頭有 1.1 個單位遠**，讀起來像在標別的東西。拉回到 −3.10。
- **第 8 拍有一個浮在半空、什麼都沒指的 `σ`**。刪掉——三角形的紅／藍邊色已經和底下三列的顏色對上了。
- 第 11 拍的陣列把 0 印成 `+0`。加一個 `cell()`，零就印 `0`。
- 第 2 拍最後兩列的欄位對不齊（`{m:<2d}` 遇到兩位數的 11 就散掉），改成同一個 `>6d` 欄寬，
  表頭與數字用同一個模板產生。
- **十一句英文旁白第一輪全部是 5 行**（上限 4 行），平均要砍掉 50 個字元。
  中文十一句一次就在 70–132 之間。
- 避開 U+1D5F（舉高的 σ）：全 repo 沒有任何一集用過它，`‴` 的前例說明 fontconfig 說有不代表畫得對。
  改用右作用 `f · σ`，順便讓反同態的理由變成畫面上看得見的事。

## 十一拍


### 第 1 拍 — 置換：在複合之下是一個群 / permutations: a group under composition

公式列：

```
σ , ρ  ∈  S      ⇒      σ ∘ ρ  ∈  S  ,    σ ⁻ ¹  ∈  S            I  ∈  S
```

中文旁白：集合上的置換就是這個集合到自己的一個一對一又映成的對應。所有置換合起來看，在複合之下是封閉的，每一個都有反元素，恆等映射也在裡面，而複合本來就滿足結合律。這四件事加起來說的正是一句話：它在複合之下是一個群。

English: A permutation of a set is a one to one correspondence of that set with itself. Taken together they are closed under composition, each has an inverse, the identity map is one of them, and composition is associative anyway. Those four statements say it is a group.


### 第 2 拍 — 對換，以及分解的不唯一 / transpositions, and factorisations that differ

公式列：

```
σ   =   τ ₁  ∘  τ ₂  ∘  ⋯  ∘  τ ₖ            τ   :   i   ↔   j
```

中文旁白：最簡單的非恆等置換，是把兩個元素互換、其他全部不動，這種叫做對換。任何置換都可以寫成若干個對換的乘積，而且寫法不只一種。左圖從恆等排列出發，每一步交換兩個位置，三步走到目標。右表另外給了一個五步的寫法，長度不同，但奇偶一樣。

English: The simplest permutation other than the identity swaps two elements and leaves the rest alone; that is a transposition. Every permutation is a product of them, in more than one way. The figure swaps two places per step, and the panel adds a longer factorisation of equal parity.


### 第 3 拍 — 固定一個元素，右乘是雙射 / one element fixed: translation is a bijection

公式列：

```
σ   ↦   σ ∘ ρ            σ ′   =   ( σ ′ ∘ ρ ⁻ ¹ )  ∘  ρ
```

中文旁白：接下來要一個很小、可是後面一直用得到的事實：把一個置換固定住，那麼把其他每個置換送到它們的複合，這個對應是置換群到自己的雙射。映成是因為任何目標都寫得成它先複合反元素、再複合回來；單射是因為右邊一起消去就得到兩者相等。

English: Next comes a small fact used over and over. Hold one permutation fixed and send every other one to their composite: that map is a bijection of the group onto itself. It is onto because any target is itself composed with the inverse first, and one to one because that factor cancels.


### 第 4 拍 — 個數是 n 階乘 / the count is n factorial

公式列：

```
| S ₙ |   =   n  ( n − 1 )  ( n − 2 )  ⋯  1   =   n !
```

中文旁白：置換的個數是 n 階乘，這是中學就算過的計數。第一個位置的像有 n 種選法，選定以後第二個位置只剩 n 減一種，接下來 n 減二種，一路乘下去就是 n 階乘。右表把 n 從一到六的階乘，和把置換真的一個一個列舉出來的個數並排，兩欄完全一樣。

English: The number of permutations is n factorial, the count from secondary school. The first place can be chosen in n ways, then the second in n minus one, then n minus two, and multiplying down gives n factorial. The panel sets those factorials beside counts from actual listing.


### 第 5 拍 — 作用在泛函上：為什麼是反元素 / the action on a functional: why the inverse

公式列：

```
( f · σ ) ( ξ )   =   f ( ξ ∘ σ ⁻ ¹ )        f · ( σ ₁ σ ₂ )  =  ( f · σ ₁ ) · σ ₂
```

中文旁白：置換也可以作用在多重線性泛函上：把輸入的那一串向量先用反元素重排，再餵給原來的泛函。為什麼用反元素而不是置換本身？因為只有這樣才會有引理 3.1：先用第一個作用、再用第二個，剛好等於直接用兩者的乘積作用。右表把不用反元素的版本也算了。

English: A permutation can act on a multilinear functional: rearrange the incoming vectors by the inverse first, then feed them in. Why the inverse and not the permutation itself? Because only then does the first lemma hold: acting by one then the other is acting by their product.


### 第 6 拍 — 定理 3.1：反同態 / theorem 3.1: an antihomomorphism

公式列：

```
T ( σ )  f   =   f · σ            T ( ρ σ )   =   T ( σ )  ∘  T ( ρ )
```

中文旁白：定理 3.1 說，把泛函送到它被作用後的那個算子是線性的，也是可逆的，所以它是個同構。但要很小心乘起來的順序：兩個置換的乘積對應的算子，等於先做前面那個再做後面那個，順序是顛倒的，書上因此叫它反同態。左圖兩條路的終點真的不一樣。

English: Theorem three point one says the operator carrying a functional to its image is linear and invertible, hence an isomorphism. The order needs care: the operator of a product is the second one after the first, in reverse order, which is why the book calls it an antihomomorphism.


### 第 7 拍 — 引理 3.2：基底只是被重排 / lemma 3.2: the basis is only rearranged

公式列：

```
μ ( p )  ·  σ   =   μ ( p ∘ σ )            p   ↦   p ∘ σ
```

中文旁白：引理 3.2 說，每一個這樣的算子都把張量積空間的那組基底送回基底自己，只是重新排列而已，沒有產生新的東西。算出來是：指標是某一串的那個基底元素，被送到指標為那一串複合置換的那一個。左圖取二維空間、三個位置，八個指標排在同一個圈上，被分成兩條三角路徑加兩個不動點。

English: The second lemma says each operator carries the basis into itself, merely rearranging it: the element indexed by a list goes to the one indexed by that list composed with the permutation, which on a circle of eight makes two triangles and leaves two in place.


### 第 8 拍 — 多項式 E / the polynomial E

公式列：

```
E ( x )   =   ∏  ( x ᵢ  −  x ₖ )            i  <  k
```

中文旁白：第 4 節先定義一個特別的多項式：把所有編號由小到大的配對，各取一個差，全部乘起來。三個變數的時候只有三個因式。用置換重排變數之後，每個因式還是某一對的差，配對沒有少也沒有多，只是其中幾對的大小順序被顛倒了，那幾個因式就差一個負號。

English: Section four starts from one polynomial: across every pair of indices in increasing order take the difference, and multiply them together. With three variables that is three factors. After permuting the variables each factor is still a difference, but some pairs come out reversed.


### 第 9 拍 — 正負號的定義 / the definition of the sign

公式列：

```
E ( x ∘ σ )   =   ( − 1 ) ʳ  E ( x )            sgn σ   =   ( − 1 ) ʳ
```

中文旁白：所以這個多項式被作用之後，只會整體差一個正負號：負一的「順序被顛倒的配對數」次方。這個正負號就叫做那個置換的正負號。左圖是同一件事的另一種看法：把置換畫成四條線，兩條線交叉一次就代表有一對的順序被顛倒，所以數交點就等於數顛倒。

English: So permuting the variables changes that polynomial by one overall sign: minus one raised to the number of pairs whose order got reversed. That sign is called the sign of the permutation. The figure draws four strands, where each crossing is exactly one reversed pair.


### 第 10 拍 — 正負號是同態 / the sign is a homomorphism

公式列：

```
sgn ( ρ σ )   =   ( sgn ρ ) ( sgn σ )            sgn τ   =   −  1
```

中文旁白：正負號是個同態：兩個置換乘起來的正負號，等於它們各自的正負號相乘。證明是把那個多項式在一個讓它不為零的點上求值，再把它約掉。另外，對換的正負號一定是負一。所以整個置換群被切成一樣大的兩半，乘上任何一個對換就會跳到另一邊去。

English: The sign is a homomorphism: the sign of a product is the product of the signs, proved by evaluating that polynomial where it does not vanish and cancelling it. A transposition always has sign minus one, so the group splits in half and any transposition jumps between halves.


### 第 11 拍 — 交錯：下一節的子空間 / alternating: the next section's subspace

公式列：

```
f · σ   =   ( sgn σ )  f            Ω f   =   ( 1 / n ! )  Σ  ( sgn σ )  f · σ
```

中文旁白：有了正負號就可以把「交錯」講清楚：一個泛函被任何置換作用之後，都等於那個置換的正負號乘上它自己；對稱則是作用之後完全不變。左圖把一個係數陣列投影過去，得到的那個對角線全是零、對稱位置互為相反數。下一集就做這個子空間。

English: With the sign in hand the word alternating can be said precisely. Acting by any permutation multiplies the functional by that permutation sign, while symmetric means nothing changes. The figure projects one array, leaving a vanishing diagonal with opposite entries across it.


## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 三排各四個編號，上面兩排之間是 σ 的箭頭，下面兩排之間是 σ ⁻ ¹ 的箭頭；整體走下來回到原位 |
| 2 | 四列排列由恆等出發，每一列右邊標出剛用掉的那個對換，被換掉的兩個數字標紅 |
| 3 | 左右兩欄都是 S ₃ 的同一份名單，六支箭頭把左欄接到右欄——箭頭交錯，但兩欄的內容一模一樣 |
| 4 | n = 3 的選擇樹：一個根、三個分枝、六片葉子，葉子標出六個排列；右側標 × 3、× 2、× 1 |
| 5 | f → f · σ ₁ → ( f · σ ₁ ) · σ ₂ 的直角路徑，加一條直接走 σ ₁ σ ₂ 的對角線；底下紅字是不用反元素的版本 |
| 6 | 上下兩條路線：上面先 T ( ρ ) 再 T ( σ )，下面反過來，兩個終點之間一個紅色的不等號 |
| 7 | 八個多重指標排在**同一個圈**上，各畫一個點；六支箭頭是兩條三角路徑（兩個三元環），兩個不動點外面再套一個圈 |
| 8 | 三個編號排成三角形，三條邊就是 E 的三個因式；被 σ 顛倒的兩條標紅，底下三列寫出每個因式的去向與正負號 |
| 9 | 四條線從上排連到下排，每個交點是一對順序被顛倒，紅點共三個——交點數就是 r |
| 10 | 兩個框（sgn = + 1 與 sgn = − 1）各 12 個元素，兩支紅箭頭表示乘上一個對換就跳到另一邊 |
| 11 | 左邊一個係數陣列，右邊是它被 Ω 投影後的樣子：對角線全是零（標紅），對稱位置互為相反數 |
