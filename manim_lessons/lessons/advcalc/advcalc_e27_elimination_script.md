# advcalc E27 — 第 2 章：消去法與列簡化階梯形

Chapter 2: Elimination and Row-Reduced Echelon Form

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 2 章第 6 節的前段（書頁 102–105）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e27_elimination.py`（`AdvCalcE27ZH` / `AdvCalcE27EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[27]` / `FORMULAS_ADVCALC[27]`）
- 配音：`manim_lessons/samples/audio_e27/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.28 分（197 秒）／英文 3.04 分（182 秒）

§6 的內容到書頁 109，其餘（初等矩陣、反矩陣、行列式的計算）留給 E28；書頁 109 起是習題 6.1 以下，依 `docs/PLAYBOOK.md` 第 8 節不做解答。

## 這一集的範例是自己的，而且是算出來的

書上第 104 頁有一個 3×4 的範例，第 105 頁有 Fig 2.4。依第 8 節，兩者都自己重做，而且要**多做一件事**。

這一集的範例：

```
    1   -1    2    1
   -1    1   -3   -2
    0    0    2    2
```

秩是 2、階是 1 與 3（不連號），做完之後第三列變成一整列的零：

```
    1   -1    0   -1
    0    0    1    1
    0    0    0    0
```

一個例子同時展示了三條結構性質（階遞增、多出來的零列、樞紐直行是 δ ʲ），而且歸零的那一列**真的**是另外兩列的組合（α₃ = −2α₁ − 2α₂），所以第 9 拍可以直接指著它講。

**中間每一個矩陣都是模組載入時跑 `_reduce()` 用 `Fraction` 精確算出來的，沒有一個是手寫的。** 場景檔頂端還把旁白宣稱的每一件事寫成 `assert`：過程不出現分數、鏈剛好四個矩陣、階是 1 與 3、樞紐直行等於標準基底向量、第三列等於那個組合。改動 `START` 會讓這一集直接 import 失敗，而不是安靜地畫出一個不再說明那些性質的矩陣。

---

## Beat 0 — 一個程序，四個問題 / one procedure, four problems
*配音長度：中文 19.4s ／ 英文 18.3s*

**畫面公式**

```
一個程序，四個問題   |   one procedure, four problems
L ( α₁ , … , α ₘ )  ,  d ( V )  ,  Δ  ,  a ⁻¹
```

**旁白（繁中）**

> 第 6 節的氣質跟前面幾節很不一樣。它從一個大家中學就學過的程序開始：把未知數一個一個消掉。而這個程序一次解決四個問題——線性擴張的基底、子空間的維數、行列式，還有反矩陣。

**Narration (EN)**

> Section six has a different character from the ones before it. It starts from a procedure everyone learned at school, eliminating unknowns one at a time, and that one procedure solves four problems at once: a basis for a span, the dimension of a subspace, determinants and inverses.

**動畫**

左邊一個方框是一串向量，一個箭頭進到右邊四個並排的方框：線性擴張的基底、維數、行列式、反矩陣。一個程序、四個出口，把這一節要交代的事先攤開。

## Beat 1 — 引理 6.1：三種運算不改變線性擴張 / lemma 6.1: three operations that preserve the span
*配音長度：中文 17.9s ／ 英文 16.2s*

**畫面公式**

```
引理 6.1：三種運算不改變線性擴張   |   lemma 6.1: three operations that preserve the span
α ᵢ  ↔  α ⱼ        α ᵢ  →  x α ᵢ   ( x ≠ 0 )        α ᵢ  →  α ᵢ − x α ⱼ   ( j ≠ i )
```

**旁白（繁中）**

> 先立一條引理。對一串向量做三種運算：把兩個對調、把某一個乘上非零的數、把某一個減去另一個的倍數——注意是另一個，不能減自己。這三種都不會改變它們生成的空間。

**Narration (EN)**

> First a lemma. Take a list of vectors and do one of three things: interchange two of them, multiply one by a nonzero number, or subtract a multiple of one from another one, not from itself. None of the three changes the space they span.

**動畫**

三個方框由上而下是三種初等運算，左邊各標著編號，右邊各配一句白話。第三條特別標出 j 不等於 i 的限制。

## Beat 2 — 理由是每一種都做得回去 / because every one of them can be undone
*配音長度：中文 20.2s ／ 英文 17.3s*

**畫面公式**

```
理由是每一種都做得回去   |   because every one of them can be undone
L ( { β ᵢ } )  =  L ( { α ᵢ } )
```

**旁白（繁中）**

> 理由很簡單：每一種運算都做得回去。對調再對調就回來，乘上非零的數就再除回去，減掉倍數就再加回來。既然兩串互相做得到對方，就互相落在對方的線性擴張裡，生成的空間只好一樣。

**Narration (EN)**

> The reason is simple: every one of them can be undone. Interchange twice and you are back; multiply by a nonzero number and divide again; subtract a multiple and add it back. Since each list can be reached from the other, each sits inside the other's span.

**動畫**

左邊兩個方框是兩串向量，中間兩個方向相反的箭頭表示彼此都做得到對方；底下三列把每一種運算與它的反運算配成對。右邊一個方框寫出結論：兩者的線性擴張相等。

## Beat 3 — 階：第一個非零座標的位置 / order: where the first nonzero entry sits
*配音長度：中文 19.7s ／ 英文 20.6s*

**畫面公式**

```
階：第一個非零座標的位置   |   order: where the first nonzero entry sits
x  =  ⟨ 0 , 0 , 0 , 2 , − 1 , 0 ⟩        n ( x )  =  4
```

**旁白（繁中）**

> 把這三種運算用在矩陣的橫列上，就叫初等列運算。接著定義一個詞：一個非零元組的階，是它第一個非零座標的位置。像零零零二負一零，階就是四。階越小，代表左邊的零越少。

**Narration (EN)**

> Applied to the rows of a matrix these are the elementary row operations. Then a definition: the order of a nonzero tuple is the position of its first nonzero entry. For zero, zero, zero, two, minus one, zero the order is four. Smaller order means fewer zeros on the left.

**動畫**

一個六元組橫著排開，上方標著每個位置的序號，第一個非零的那一格反白，底下一個箭頭指上來並寫出它的階。定義是位置，不是數值，所以畫面標的是位置。

## Beat 4 — 演算法的一步 / one step of the algorithm
*配音長度：中文 16.5s ／ 英文 15.7s*

**畫面公式**

```
演算法的一步   |   one step of the algorithm
α ₁  →  α ₁ / c ₁        α ᵢ  →  α ᵢ − a ᵢ₁ α ₁
```

**旁白（繁中）**

> 演算法是這樣。在所有橫列裡找階最小的那一條搬到最上面，把它的首項除成一，再把它的倍數從其他每一列減掉，讓那一直行只剩最上面那個一，其他位置全是零。

**Narration (EN)**

> The algorithm runs like this. Among all the rows find one of least order, move it to the top, divide it by its leading entry, and subtract multiples of it from every other row, so that its column is left with that leading one and nothing but zeros.

**動畫**

起始矩陣，第一橫列與第一直行用顏色標出來，記號放在括號外面（畫在數字上會把數字蓋掉，初稿就是這樣）。右邊三行字對應演算法的三個動作。

## Beat 5 — 一個例子，從頭走到尾 / one example, start to finish
*配音長度：中文 19.8s ／ 英文 17.4s*

**畫面公式**

```
一個例子，從頭走到尾   |   one example, start to finish
n ₁ < n ₂ < … < n ₖ
```

**旁白（繁中）**

> 然後對剩下的列重複同一件事：鎖定下一個出現的階，把那一列搬到第二列，同樣把它的直行清乾淨。我們看一個實際的三乘四例子從頭走到尾。這個例子剛好不需要對調，因為第一列的階本來就最小。

**Narration (EN)**

> Then repeat on what is left: fix on the next order that occurs, bring that row into second place, and clear its column the same way. Let us watch one three by four example run start to finish. This one needs no interchange, since the first row already has least order.

**動畫**

四個矩陣排成一列，箭頭之間標著用了哪一種運算。**這四個矩陣是模組載入時用精確整數算出來的**，不是手寫；程式裡還斷言過整個過程不會出現分數、最後的階是 1 與 3、樞紐直行等於標準基底向量。

## Beat 6 — 做完之後的三個性質 / three properties of what you end with
*配音長度：中文 16.3s ／ 英文 17.3s*

**畫面公式**

```
做完之後的三個性質   |   three properties of what you end with
n ( α ⱼ ) = n ⱼ        α ⱼ = 0   ( j > k )        δ ʲ   :   n ⱼ
```

**旁白（繁中）**

> 做完之後的矩陣有三個性質。前 k 條橫列裡，第 j 條的階是第 j 小的那個；如果 k 比列數少，剩下的列全是零；而第 nⱼ 個直行，正好是標準基底的第 j 個向量。

**Narration (EN)**

> The matrix you end with has three properties. Among the first k rows, the jth has the jth smallest order; if k is less than the number of rows, the remaining rows are all zero; and the n-j-th column is exactly the jth standard basis vector.

**動畫**

最終矩陣，兩個樞紐直行整行反白、上方各有一個箭頭標著它的階；歸零的那一列也反白，左邊一個箭頭指著它。三條性質各配一句話在右邊。

## Beat 7 — 為什麼那些橫列是獨立的 / why those rows are independent
*配音長度：中文 17.5s ／ 英文 16.6s*

**畫面公式**

```
為什麼那些橫列是獨立的   |   why those rows are independent
Σ ₁ᵏ c ⱼ α ⱼ  =  0        ⇒   c ⱼ  =  0   ( ∀ j )
```

**旁白（繁中）**

> 為什麼前 k 列是基底？取它們的一個線性組合。因為第 nⱼ 直行只有第 j 列是一，這個組合在第 nⱼ 個位置就正好等於第 j 個係數。要整個是零，每個係數只好都是零。

**Narration (EN)**

> Why are those k rows a basis? Take a linear combination of them. Since the n-j-th column has a one only in row j, the combination has exactly the jth coefficient in that position. For the whole thing to vanish, every coefficient must be zero.

**動畫**

上方一個方框寫著係數組合等於零。底下是最終矩陣的前兩列，兩個樞紐直行的下方各有一個箭頭標著對應的係數——因為那一行只有這一列是 1，組合在那個位置就正好是那個係數。

## Beat 8 — 四個問題裡的前兩個解決了 / the first two of the four problems, settled
*配音長度：中文 15.9s ／ 英文 14.5s*

**畫面公式**

```
四個問題裡的前兩個解決了   |   the first two of the four problems, settled
{ α ₁ , … , α ₖ }  ⊂  V        d ( V )  =  k
```

**旁白（繁中）**

> 所以那 k 條橫列彼此獨立，又生成整個列空間，就是它的一組基底。一開始說的四個問題裡，第一個與第二個就同時解決了：基底可以直接讀出來，維數就是 k。

**Narration (EN)**

> So those k rows are independent and they span the row space, which makes them a basis for it. Of the four problems named at the start, the first two are now settled at once: the basis reads straight off, and the dimension is k.

**動畫**

四個問題的方框再出現一次，前兩個打勾、後兩個標著留給下一集。這一拍是把第 0 拍的承諾兌現一半。

## Beat 9 — 那條看不出來的相依列 / the dependent row you could not see
*配音長度：中文 14.9s ／ 英文 14.3s*

**畫面公式**

```
那條看不出來的相依列   |   the dependent row you could not see
α ₃  =  − 2 α ₁ − 2 α ₂        ⇒    d ( V ) = 2
```

**旁白（繁中）**

> 剛剛那個例子還說明了一件事。原來的三條列裡，有一條其實是另外兩條的組合，肉眼看不出來；消去之後它變成一整列的零，維數是二而不是三。

**Narration (EN)**

> The example showed something else too. One of the three original rows was a combination of the other two, which the eye cannot see; after the elimination it became a row of zeros, and the dimension turned out to be two rather than three.

**動畫**

左邊是原始矩陣、右邊是最終矩陣，兩邊的第三列都反白。中間一個方框寫出那條相依關係。原始的三條列看不出誰依賴誰，消去把它變成一整列的零。

## Beat 10 — 列簡化階梯形與典範基底 / row-reduced echelon form and the canonical basis
*配音長度：中文 18.8s ／ 英文 14.1s*

**畫面公式**

```
列簡化階梯形與典範基底   |   row-reduced echelon form and the canonical basis
r  =  r ( V )
```

**旁白（繁中）**

> 最後的矩陣叫做列簡化階梯形。可以證明它完全由列空間決定，跟從哪個矩陣開始、按什麼順序做都無關；它的那些橫列就叫這個空間的典範基底。下一集把這些運算翻譯成矩陣乘法。

**Narration (EN)**

> The final matrix is called row-reduced echelon form. It can be shown to be determined by the row space alone, whatever matrix you started from and in whatever order you worked. Its rows are called the canonical basis of that space.

**動畫**

一個較大的示意矩陣：每一列的第一個 1 逐列往右移，一條階梯線沿著這些 1 的左側與下方畫過去，線底下全是零，每個 1 所在的直行其他位置也是零。書上 Fig 2.4 是 8×11 的另一個圖樣，這裡是自己選的尺寸與樣式。
