# advcalc E73 — 第 5 章：緊變換

Chapter 5: Compact Transformations

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 5 章第 5 節「緊變換」（書頁 264–265），**整節一集講完，第 5 章到此結束**。

**這一節整節沒有習題**，書頁 265 講完直接進第 6 章「微分方程」（266 頁起）。這在這本書裡是第三次（前兩次是第 2 章的 *§7 與第 4 章的 *§12）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e73_compact.py`（`AdvCalcE73ZH` / `AdvCalcE73EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[73]` / `FORMULAS_ADVCALC[73]`）
- 配音：`manim_lessons/samples/audio_e73/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 218.9 秒配音／英文 199.6 秒配音

## 定理 3.1 壞在哪裡，又怎麼救回來

**無窮維時定理 3.1 失效。** 自伴的有界算子可能連一個特徵向量都沒有：
把 f ( x ) 送成 x f ( x ) 的乘法算子就是標準見證——[0, 1] 裡每個點都在它的譜裡，
可是沒有一個是特徵值。這就是「連續譜」，也是 Hilbert 空間理論要留到研究所的原因。

**救回來的條件是緊。** S 是單位球，T 緊的意思是 T [ S ] 的閉包序列緊緻。
**定理 5.1**：T 自伴而且緊時，T 的像有一組完全由特徵向量構成的正交規範基，
而特徵值序列收斂到零（或只有有限個）。

**證明是定理 3.1 的那一套，換個起手。** 取 m = ‖ T ‖ 與一列長度為一、像的長度趨近 m 的 ξ ₙ：

```
( ( m ² − T ² ) ξ ₙ , ξ ₙ )   =   m ²  −  ‖ T ξ ₙ ‖ ²    ⟶    0
```

**上一集的引理 3.2 在這裡第二次付現**：m ² − T ² 非負而且自伴，所以那個*數*趨近零
就逼出那個*向量* ( m ² − T ² )( ξ ₙ ) 趨近零。接著緊性登場：T ξ ₙ 收斂到某個 β，
於是 T ² ξ ₙ 與 m ² ξ ₙ 都趨近 T β，**ξ ₙ 因此被自己的像拖著收斂**，
而 ‖ β ‖ = m ≠ 0 滿足 T ² β = m ² β。把 m ² − T ² 分解成 ( m − T )( m + T )，
兩個分支都交出一個 | r ₁ | = m 的特徵向量，剩下的歸納跟定理 3.1 一字不差。

**緊性第二次登場在證 | r ₙ | → 0。** 若 | r ₙ | 都不小於某個 b > 0，那麼

```
‖ T φ ᵢ  −  T φ ⱼ ‖ ²   =   r ᵢ ²  +  r ⱼ ²   ≥   2 b ²
```

像就永遠擠不在一起，抽不出收斂子列，與緊性矛盾。最後 b ₙ = r ₙ a ₙ 給出
‖ β − 前 n 項 ‖ ≤ | r ₙ ₊ ₁ | ‖ α ‖，而右邊趨近零，所以那組 φ 是像的基底。

## 這一集用的算子

**整集的計算都在 Dirichlet 問題的 Green 算子上做**，這正是書上預告的「下一章出人意料的應用」：

```
K ( x , y )   =   min ( x , y ) ( 1 − max ( x , y ) )
```

它對稱，所以自伴；它緊；而它的特徵向量正是正規化的正弦，特徵值是 1 / ( n π ) ²。

| 要驗的事 | 怎麼驗 | 結果 |
|---|---|---|
| 核對稱 | 21 × 21 個取樣點 | 差 0.0 |
| 自伴 | ( T f , g ) 對 ( f , T g ) | 兩邊都是 0.04142202 |
| 特徵向量 | n = 1 到 4 的 ‖ T φ ₙ − r ₙ φ ₙ ‖ | ≤ 1.4e-10 |
| 特徵值 | r ₙ | 0.10132118、0.02533030、0.01125791、0.00633257 |
| 乘法算子沒有特徵向量 | 四個寬度的隆起 | ‖ f ‖ 都是 1.0000，‖ ( M − λ ) f ‖ 從 0.070724 掉到 0.008841 |
| 半寬減半，像也減半 | 前兩列相除 | 2.00 |
| 恆等映射不緊 | ‖ φ ᵢ − φ ⱼ ‖ ² | 2.0000，永遠 |
| T 的像擠得起來 | ‖ T φ ᵢ − T φ ⱼ ‖ ² | 0.0109076 → 0.0000243（(1,2) 到 (5,6)） |
| 那個平方距離的公式 | 對 r ᵢ ² + r ⱼ ² | 四對都相同到 1e-8 |
| 極大化序列 | ξ ₙ = ( φ ₁ + φ ₂ / n ) 正規化 | ‖ T ξ ₙ ‖ 爬到 0.10058785 |
| 引理 3.2 的數與向量 | 兩欄並排 | 4.812e-03 → 1.481e-04；6.805e-03 → 1.194e-03 |
| b ₙ = r ₙ a ₙ | α 取常數函數 1 | 後兩欄逐列相同到 1e-8 |
| 尾巴估計 | n = 1 到 5 | 藍色永遠在紅色底下，3.470e-03 → 3.071e-04 |

## 這一輪抓到的錯

**緊性那一拍第一版的圖在說反話。** 原本畫三格點陣：第一格 ξ ₙ 散開、第二格 T ξ ₙ 收斂、
第三格 β。可是這一拍的**結論**正是「ξ ₙ 也收斂」——畫面卻停在「ξ ₙ 不收斂」，
跟旁白最後一句矛盾。**修法是換成真的曲線**：左邊畫 ξ ₙ（n = 1、2、4、8）與極限 φ ₁，
右邊畫 T ξ ₙ 與極限 β，兩組都收斂，而右邊明顯擠得更緊。
（**跟 E71 歸納那一拍是同一類**：為了讓畫面好看而把數學畫錯。）

**虛線標成 2 b ² 卻剛好切在第一根長條頂端。** | r ₙ | → 0 那一拍，b 是個**假設**的下界，
論證是「若每根都不低於 2 b ²，就抽不出收斂子列」。第一版把虛線畫在最高那根的頂端，
讀起來變成「2 b ² 就等於第一個值」。把線降到三成高度，畫面才說出該說的話：
第一根在線上，其餘三根都掉到線底下，所以沒有這樣的 b。

**一段 `for ... : pass` 的死迴圈。** 草稿裡先寫了圖例的迴圈、後來改成兩行手寫的，
迴圈本體就只剩 `pass` 留在那裡。跟 `if False else`、`.replace(...)` 同一類。
現在寫完場景檔要 grep 的有三樣：`if False`、`.replace(`、`  pass$`。

**配音這次逐檔量過長度了**（上一集英文有一個檔案寫壞只有 7.2 秒）。
11 個檔案每個都超過 10 秒，assert 直接寫進檢查裡。

---

## Beat 0 — 無窮維時定理 3.1 失效 / in infinite dimensions theorem 3.1 fails
*配音長度：中文 20.9s ／ 英文 16.4s*

**畫面公式**

```
無窮維時定理 3.1 失效   |   in infinite dimensions theorem 3.1 fails
( M f ) ( x )  =  x  f ( x )            ( x − λ )  f ( x )  ≡  0
```

**旁白（繁中）**

> 無窮維時定理 3.1 就不成立了。自伴的 T 一般沒有足夠多的特徵向量張成基底，除了離散譜還要處理連續譜，需要更細緻的分析。這正是 Hilbert 空間理論要留到研究所，也是量子力學數學結構複雜的來源之一。

**Narration (EN)**

> In infinite dimensions Theorem 3.1 breaks down. A self-adjoint T need not have enough eigenvectors to form a basis, and a continuous spectrum as well as a discrete one must be handled. That is why Hilbert space theory is studied at the graduate level.

**動畫**

四個寬度不同的隆起，全都擠在 λ = 0.5 那條虛線附近，愈窄的愈高。右側四列：‖ f ‖ 永遠是 1.0000，可是 ‖ ( M − λ ) f ‖ 從 0.070724 一路掉到 0.008841。

---

## Beat 1 — 緊的定義 / what compact means
*配音長度：中文 20.1s ／ 英文 18.1s*

**畫面公式**

```
緊的定義   |   what compact means
S  =  { ξ  :  ‖ ξ ‖  ≤  1 }                T [ S ] ‾
```

**旁白（繁中）**

> 不過有一個很重要的特例，特徵基定理仍然成立，而且下一章會有一個出人意料的應用。定義：S 是 V 的單位球，T 在 Hom(V, W) 裡叫緊，如果 T 作用在 S 上的像在 W 裡的閉包是序列緊緻的。

**Narration (EN)**

> There is however one very important special case in which the eigenbasis theorem is available, and which will have a startling application in the next chapter. Definition: with S the unit ball of V, a transformation is compact when the closure of the image of S is sequentially compact.

**動畫**

兩排長條：左邊六根是 φ ₙ 的長度，永遠頂在 ‖ φ ₙ ‖ = 1 那條虛線上；右邊六根是 T φ ₙ 的長度，一路掉下去。右側列出 ‖ φ ᵢ − φ ⱼ ‖ ² = 2.0000 與 T 之後的兩個對應值。

---

## Beat 2 — 定理 5.1 / theorem 5.1
*配音長度：中文 18.0s ／ 英文 21.4s*

**畫面公式**

```
定理 5.1   |   theorem 5.1
T φ ᵢ  =  r ᵢ φ ᵢ            r ᵢ  ⟶  0
```

**旁白（繁中）**

> 定理 5.1：V 是任何準 Hilbert 空間，T 在 Hom V 裡自伴而且緊。那麼 T 的像作為準 Hilbert 空間，有一組完全由特徵向量構成的正交規範基，而對應的特徵值序列收斂到零，或者只有有限個。

**Narration (EN)**

> Theorem 5.1: let V be any pre-Hilbert space and let T in Hom V be self-adjoint and compact. Then the range of T, as a pre-Hilbert space, has an orthonormal basis consisting entirely of eigenvectors of T, and the corresponding sequence of eigenvalues converges to zero, or is finite.

**動畫**

[0, 1] 上的三條正規化正弦 φ ₁、φ ₂、φ ₃。右側是 n = 1 到 4 的特徵值與 ‖ T φ ₙ − r ₙ φ ₙ ‖，殘量都在 1e-8 以下，最後一列是 m = ‖ T ‖ = r ₁。

---

## Beat 3 — 證明的起手 / how the proof opens
*配音長度：中文 19.4s ／ 英文 19.0s*

**畫面公式**

```
證明的起手   |   how the proof opens
m  =  ‖ T ‖         ( ( m ² − T ² ) ξ ₙ , ξ ₙ )  =  m ² − ‖ T ξ ₙ ‖ ²
```

**旁白（繁中）**

> 證明跟定理 3.1 幾乎一樣，只是起手不同。取 m 為 ‖T‖，挑一列長度都是一的 ξ n，使 ‖T ξ n‖ 趨近 m。那麼 ((m 平方減 T 平方) ξ n, ξ n) 等於 m 平方減 ‖T ξ n‖ 平方，趨近零。

**Narration (EN)**

> The proof runs like Theorem 3.1's, but starts differently. Let m be the norm of T, the supremum of the norm of T xi over the unit sphere, and choose unit vectors whose images have norms tending to m. That scalar is m squared minus those squared norms, so it tends to zero.

**動畫**

四根長條爬向 m = ‖ T ‖ 那條虛線，頂端各有一個點。右側是 n = 1、2、4、8 的 ‖ T ξ ₙ ‖ 與 m ² − ‖ T ξ ₙ ‖ ²，後者從 4.812e-03 掉到 1.481e-04。

---

## Beat 4 — 引理 3.2 第二次付現 / lemma 3.2 pays off again
*配音長度：中文 17.9s ／ 英文 16.0s*

**畫面公式**

```
引理 3.2 第二次付現   |   lemma 3.2 pays off again
( m ² − T ² ) ( ξ ₙ )     ⟶     0
```

**旁白（繁中）**

> m 平方減 T 平方是非負的自伴變換，所以引理 3.2 可以用。上一集那個推論在這裡第二次付現：那個數趨近零，就逼出 (m 平方減 T 平方) 作用在 ξ n 上的那個向量也趨近零。

**Narration (EN)**

> Now m squared minus T squared is a nonnegative self-adjoint transformation, so Lemma 3.2 applies. Last episode's consequence pays off a second time: the number tending to zero forces the vector it came from to tend to zero as well.

**動畫**

四組雙色長條：藍色是 ( ( m ² − T ² ) ξ ₙ , ξ ₙ ) 這個數，青色是 ‖ ( m ² − T ² ) ξ ₙ ‖ 這個向量的長度，兩排一起掉。左上角有兩段色條當圖例。

---

## Beat 5 — 緊性第一次用上 / compactness, first use
*配音長度：中文 20.5s ／ 英文 17.9s*

**畫面公式**

```
緊性第一次用上   |   compactness, first use
T ξ ₙ   ⟶   β                 T ² ( β )   =   m ² β
```

**旁白（繁中）**

> 緊性在這裡第一次用上。T 緊，必要時取子列可以假設 T ξ n 收斂到 β。於是 T 平方 ξ n 趨近 T β，而剛才那一步說 m 平方乘 ξ n 也趨近 T β，所以 ξ n 自己也收斂，而且 T 平方 β 等於 m 平方 β。

**Narration (EN)**

> Compactness enters here for the first time. Passing to a subsequence, the images converge, say to beta. Then T squared applied to them tends to T beta, and by the previous step so does m squared times them, so the vectors converge and T squared beta is m squared beta.

**動畫**

兩張函數圖：左邊是 ξ ₙ（n = 1、2、4、8）與它們的極限 φ ₁（粗橘線），右邊是 T ξ ₙ 與極限 β。右邊那一組明顯擠得比左邊緊。兩張的縱向尺度不同。

---

## Beat 6 — 把 m ² − T ² 分解掉 / factoring the difference
*配音長度：中文 22.2s ／ 英文 19.9s*

**畫面公式**

```
把 m ² − T ² 分解掉   |   factoring the difference
0   =   ( m − T ) ( m + T ) ( α )                | r ₁ |  =  m
```

**旁白（繁中）**

> 因為 ‖β‖ 等於 ‖T ξ n‖ 的極限 m，β 不是零。取 α 為 β 除以長度，就得到 0 = (m 減 T)(m 加 T)(α)。兩個分支：(m 加 T)α 是零時 T α 等於負 m α，否則 γ = (m 加 T)α 就是特徵值 m 的特徵向量。

**Narration (EN)**

> Since the norm of beta is the limit m, beta is not zero, and dividing by its norm gives a unit vector killed by m minus T composed with m plus T. Two branches: either m plus T kills it, and the eigenvalue is minus m, or what comes out is nonzero and has eigenvalue m.

**動畫**

一個方塊寫 ( m − T )( m + T ) α = 0，兩支箭頭往下分成兩支：左邊 ( m + T ) α = 0 給出 T α = − m α，右邊 γ = ( m + T ) α ≠ 0 給出 T γ = m γ。

---

## Beat 7 — 歸納 / the induction
*配音長度：中文 21.1s ／ 英文 19.3s*

**畫面公式**

```
歸納   |   the induction
V ₙ  =  { φ ₁ , … , φ ₙ ₋ ₁ } ⊥            | r ₙ |  =  ‖ T ↾ V ₙ ‖
```

**旁白（繁中）**

> 接下來跟定理 3.1 一樣歸納。V 2 取 φ 1 的正交補，它在 T 底下不變，而且 T 限制在上面仍然緊、仍然自伴，所以又生出 φ 2。一直做下去得到正交規範序列，其中 |r n| 就是 T 限制在 V n 上的範數。

**Narration (EN)**

> From here the induction is Theorem 3.1's. Take the orthogonal complement of the first eigenvector; it is carried into itself, and the restriction to it is still compact and still self-adjoint, so it produces the next one. Continuing gives an orthonormal sequence of eigenvectors.

**動畫**

φ ₁（細灰）與 φ ₂（青）、φ ₃（藍）三條曲線。右側：( φ ₁ , φ ₂ ) = −9e-17，以及 | r ₂ |、| r ₃ |、| r ₄ | 逐層變小。

---

## Beat 8 — 為什麼 | r ₙ | 必須趨近零 / why the eigenvalues must die away
*配音長度：中文 19.4s ／ 英文 17.4s*

**畫面公式**

```
為什麼 | r ₙ | 必須趨近零   |   why the eigenvalues must die away
‖ T φ ᵢ − T φ ⱼ ‖ ²   =   r ᵢ ² + r ⱼ ²   ≥   2 b ²
```

**旁白（繁中）**

> |r n| 本來就遞減，因為每次都在更小的集合上取上確界。若它不趨近零，就有 b 大於零使每個 |r n| 不小於 b；可是 ‖T φ i 減 T φ j‖ 的平方等於 r i 平方加 r j 平方，不小於二倍 b 平方，與緊性矛盾。

**Narration (EN)**

> The eigenvalues decrease in absolute value anyway, each supremum being over a smaller set. If they did not tend to zero there would be a positive lower bound; but the squared distance between two images is the sum of their squared eigenvalues, so the images stay apart.

**動畫**

四根長條對應 (i, j) = (1,2)、(2,3)、(3,4)、(5,6)，第一根遠高於虛線 2 b ²，其餘三根都掉到線底下。右側把 ‖ T φ ᵢ − T φ ⱼ ‖ ² 與 r ᵢ ² + r ⱼ ² 並排，逐列相同。

---

## Beat 9 — 係數的關係 / how the coefficients relate
*配音長度：中文 18.8s ／ 英文 15.9s*

**畫面公式**

```
係數的關係   |   how the coefficients relate
b ₙ    =    r ₙ  a ₙ
```

**旁白（繁中）**

> 最後要證那組 φ 是 T 的像的基底。設 β = T α，兩者的 Fourier 係數滿足 b n 等於 r n 乘 a n，把 T 搬到內積另一邊就看出來。於是 β 減掉前 n 項，等於 T 作用在 α 減掉前 n 項上。

**Narration (EN)**

> Finally the eigenvectors form a basis for the range. If beta is the image of alpha, their Fourier coefficients are related by the eigenvalue, which follows by moving T across the product. So the tail of beta is T applied to the tail of alpha.

**動畫**

六組雙色長條：青色是 a ₙ、紫色是 b ₙ，兩排各自正規化。右側四列列出 a ₙ、b ₙ 與 r ₙ a ₙ，後兩欄逐列完全相同。

---

## Beat 10 — 尾巴的估計，與第 5 章的結束 / the tail estimate, and the end of chapter 5
*配音長度：中文 20.4s ／ 英文 18.3s*

**畫面公式**

```
尾巴的估計，與第 5 章的結束   |   the tail estimate, and the end of chapter 5
‖ β − Σ ₁ ⁿ b ᵢ φ ᵢ ‖    ≤    | r ₙ ₊ ₁ |  ‖ α ‖
```

**旁白（繁中）**

> 所以 β 減前 n 項的長度不超過 |r n 加一| 乘 ‖α‖，而那個係數趨近零，級數就收斂到 β。又因為 T 自伴，T 的核就是像的正交補；若某個 r n 是零，像就是有限維的。下一章會用這個定理生出 Fourier 級數。

**Narration (EN)**

> So the tail of beta is bounded by the next eigenvalue times the norm of alpha, and since those tend to zero the series converges to beta. Since T is self-adjoint the null space is the orthogonal complement of the range, and if some eigenvalue vanishes the range is finite-dimensional.

**動畫**

五組雙色長條：藍色是 ‖ β − 前 n 項 ‖、紅色是 | r ₙ ₊ ₁ | ‖ α ‖，藍色永遠在紅色底下，而且兩排一起掉向零。右側最後一列是 N ( T ) = R ( T ) ⊥。
