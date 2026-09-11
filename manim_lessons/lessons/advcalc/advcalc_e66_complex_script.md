# advcalc E66 — 第 4 章：複數系統

Chapter 4: The Complex Number System

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 11 節「複數系統」（書頁 240–243）。

**§11 的內容收在書頁 243**，243–245 是習題 11.1–11.19，依 PLAYBOOK 第 8 節不做解答；加星號的第 12 節「弱方法」從書頁 245 起。**OUTLINE 把 §11 寫成 240–245，是把習題頁算了進去——那張表的頁碼第八次這樣錯。**

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e66_complex.py`（`AdvCalcE66ZH` / `AdvCalcE66EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[66]` / `FORMULAS_ADVCALC[66]`）
- 配音：`manim_lessons/samples/audio_e66/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.30 分（198 秒）／英文 3.18 分（191 秒）

## 一個運算換到整套理論

書上的敘述有一個很清楚的結構，這一集照著走：

1. 平面本來就是實向量空間。**把它變成複數系統的，只是多出來的那一個乘法運算。**
2. 有了乘法，⟨1,0⟩ 是唯一的乘法單位元，而每個非零元素都可逆——**所以它是一個域。**
3. **域這個性質不是裝飾**：它就是「拿 ℂ 當純量域，第 1、2 章把 ℝ 處處換成 ℂ 之後整套重跑一遍」的理由。
4. 然後是 ℝ 以子域坐在裡面、i、共軛是唯一非平凡的固定 ℝ 的自同構、絕對值的可乘性，
   最後是**實可微與複可微之間的落差**，收在代數基本定理與複指數。

## beats 8、9 是脊梁：同一個計算跑兩次

這一集最想講清楚的一件事，是用同一個差商計算做對比：

| | 共軛 z ↦ z̄ | 冪級數 F(ξ) = Σ ξⁿ |
|---|---|---|
| 差商 | h̄／h | (F(β+h) − F(β))／h |
| 十六個方向的值 | **掃滿整個單位圓** | **擠成一個點** |
| 散布 | 2.00 | 0.117 |
| 沿實軸 / 沿虛軸 | +1 ／ −1 | 一樣 |

共軛是實線性的（程式驗過它跟實純量交換），可是不複線性——**見證就是它跟「乘 i」不交換**，
畫面上那個差是 2.4。而冪級數的微分是「乘上 F′(β)」，那在一維複向量空間上是複線性的運算，
所以差商跟方向無關；又因為非零複數可以拿來除，差商自己就收斂，導數變回一個真正的商。

其他算出來的東西：複乘的長度相乘／角度相加（兩邊逐項對過）、反元素 ξ̄／|ξ|² 驗過 ξξ⁻¹ = 1、
共軛保和保積的誤差都在 1e-16 級、絕對值可乘性三組都對到 1e-14、
x²+1 = (x+i)(x−i) 在三個點上驗過、複指數的級數部分和對 e^x(cos y + i sin y) 的誤差
8.3e-02 → 9.1e-05 → 1.4e-08 → 0。

## 這一輪抓到的錯

### 一、beat 9 的圖第一版是空的

16 個商擠得太密，**畫出來只剩一個孤點**——看起來像空圖，而不是「同樣十六個方向現在收成一個答案」。
改成把偏差**放大 12 倍**，並在畫面上標「× 12」。**放大是可以的，但不能不說。**

**這跟 E60 的「√2 收斂太快畫不出收斂」、E64 的「曲率太小畫不出差別」是同一類病的第三次。**
現在這條在 STATUS 裡有三個實例，應該算是這個專案最常犯的錯：**數學上對，不代表畫出來讀得到。**

### 二、註腳說了一件畫面沒做的事（而且是重渲染之後才抓到的）

第一次渲染完、四道檢查全過、1080p 抽幀時才發現 beat 9 的第二行註腳寫著：

> 灰色虛線圓的半徑就是那個散布：上一拍是 2.00，這一拍只有 0.12

**兩處都錯**：beat 9 那個圓的半徑是十六個商離 F′(β) 的**最大距離 0.060**，不是散布 0.117；
而 beat 8 根本沒有半徑 2.00 的圓——那裡是單位圓，2.00 是它的直徑。改成照實說。

**這跟 E63 那個「常數量到 0.500」是同一個成因**：註腳宣稱一個數量關係，而那個關係從來沒跟
畫它的程式對過。E63 之後我把註腳裡的數字改成 f-string 從資料取，可是
**「半徑等於散布」這種結構性的宣稱，f-string 擋不住**——只能逐句核。

所以這次重渲染之前，我把這一集畫面上所有中文宣稱（十一拍約三十句）抓出來跟程式對了一遍，
確認只有那一行有問題，才重渲染一次。**這個動作應該變成固定流程的一部分。**

### 三、`collide` 抓到 14 處，全是同一個原因

複平面的圖裡，**向量標籤跟圓弧、座標軸擠在一起**。四種修法都用上了：
標籤依虛部正負換上下、把數值移進右側表格、縮小圓的半徑讓它離註腳有空間、把標籤挪開座標軸。

### 四、`if False else` 這個寫法我第四次寫出來

E63 記過、E64 又犯、E65 沒犯、E66 再犯兩處。這次在跑檢查前就自己抓掉了，
但連續出現代表是改不掉的習慣，不是偶然。

---

## Beat 0 — 第三個基本數域 / the third basic number field
*配音長度：中文 18.7s ／ 英文 17.2s*

**畫面公式**

```
第三個基本數域   |   the third basic number field
ℂ    =    ℝ ²    +    ( × )
```

**旁白（繁中）**

> 第 11 節講複數系統——繼有理數與實數之後，第三個必須研究的基本數域。書上說幾乎每個人本來就把一個複數看成等同於一對實數，所以這個系統就是笛卡兒平面，再加上一些額外的結構。

**Narration (EN)**

> Section 11 is the complex number system, the third basic number field after the rationals and the reals. Almost everybody already views a complex number as equivalent to a pair of real numbers, so the system is the Cartesian plane carrying some further structure.

**動畫**

複平面上一點 ξ = ⟨1.2, 0.5⟩，兩條虛線投影到兩軸——就是「一對實數」。

## Beat 1 — 多出來的那一個運算 / the one extra operation
*配音長度：中文 15.6s ／ 英文 16.5s*

**畫面公式**

```
多出來的那一個運算   |   the one extra operation
⟨ x ₁ , x ₂ ⟩ ⟨ y ₁ , y ₂ ⟩  =  ⟨ x ₁ y ₁ − x ₂ y ₂ ,  x ₁ y ₂ + x ₂ y ₁ ⟩
```

**旁白（繁中）**

> 把它跟那個向量底層區別開來的，是多出來的那一個運算：複數乘法。定義的動機是把一對數寫成 x 加 i y、令 i 的平方等於負一，再照普通的代數規則乘開來。

**Narration (EN)**

> What distinguishes it from that vector substratum is one extra operation: complex multiplication. The definition is motivated by writing a pair as x plus i y with i squared equal to minus one, and then multiplying out by the ordinary laws of algebra.

**動畫**

ξ、γ 與 ξγ 三個向量；右側把「長度相乘、角度相加」兩個等式的兩邊都算出來對照。

## Beat 2 — 單位元與反元素：所以它是個域 / an identity and inverses: so it is a field
*配音長度：中文 19.2s ／ 英文 18.6s*

**畫面公式**

```
單位元與反元素：所以它是個域   |   an identity and inverses: so it is a field
⟨ 1 , 0 ⟩  ·  ξ   =   ξ                ξ  ≠  0    ⇒    ∃ ξ ⁻ ¹
```

**旁白（繁中）**

> 向量的運算加上這個乘法，讓平面成為一個交換代數。而且不只如此：一和零那一對是唯一的乘法單位元，而每一個非零元素都有乘法反元素。把這幾件事總結起來，就是說這個系統是一個域。

**Narration (EN)**

> The vector operations together with this multiplication make the plane a commutative algebra. More than that: the pair one, zero is the unique multiplicative identity, and every nonzero element has a multiplicative inverse. Those facts are summarised by saying the system is a field.

**動畫**

ξ 與 ξ⁻¹ 分居單位圓內外（長度互為倒數、角度相反），加上 1 的向量；右側驗 ξξ⁻¹ = 1。

## Beat 3 — 拿 ℂ 當純量域，前兩章重跑一遍 / as a scalar field, chapters 1 and 2 run again
*配音長度：中文 18.8s ／ 英文 17.4s*

**畫面公式**

```
拿 ℂ 當純量域，前兩章重跑一遍   |   as a scalar field, chapters 1 and 2 run again
ℝ    ↦    ℂ                    ℂ ⁿ   =   { ⟨ ξ ₁ , … , ξ ₙ ⟩ }
```

**旁白（繁中）**

> 這一點就換到了整節的全部。因為它是一個域，就可以拿來當向量空間理論裡新的純量域——第 1 章與第 2 章的整套發展，把實數處處換成複數之後仍然成立。純量乘法現在是複數乘法。

**Narration (EN)**

> That is what buys the whole section. Because it is a field, it can be used as a new scalar field in vector space theory, and the entire development of chapters 1 and 2 stays valid with the reals replaced everywhere by the complex numbers. Scalar multiplication is now complex.

**動畫**

兩列平行的框：ℝ → Ch 1–2 與 ℂ → Ch 1–2，底下是 ℂⁿ。

## Beat 4 — ℝ 坐在裡面，而 i 的平方是負一 / the reals sit inside, and i squared is minus one
*配音長度：中文 18.0s ／ 英文 16.9s*

**畫面公式**

```
ℝ 坐在裡面，而 i 的平方是負一   |   the reals sit inside, and i squared is minus one
i   =   ⟨ 0 , 1 ⟩                i ²   =   ⟨ − 1 , 0 ⟩   =   − 1
```

**旁白（繁中）**

> 把一個實數送成第二個分量為零的那一對，這個映射保和也保積，所以實數是以子域的身分坐在裡面的，而習慣上就把兩者認同。那個神祕的 i 就是零和一那一對，它的平方真的是負一。

**Narration (EN)**

> The map sending a real number to the pair with second entry zero preserves both sums and products, so the reals sit inside as a subfield and it is conventional to identify them. The mysterious i is the pair zero, one, whose square really is minus one.

**動畫**

青色加粗的實軸，1、i、−1 三個點，以及兩段 π／2 的弧——**乘 i 就是轉四分之一圈，轉兩次到 −1。**

## Beat 5 — 共軛是一個自同構 / conjugation is an automorphism
*配音長度：中文 16.4s ／ 英文 17.4s*

**畫面公式**

```
共軛是一個自同構   |   conjugation is an automorphism
ξ  +  η  ‾   =   ξ ‾  +  η ‾                ξ η ‾   =   ξ ‾  η ‾
```

**旁白（繁中）**

> 把 x 加 i y 送成 x 減 i y 的那個映射，也保和保積，所以它是這個域到自己的一個自同構。它叫複共軛，而且除了恆等映射之外，它是唯一一個讓每個實數都不動的自同構。

**Narration (EN)**

> The map sending x plus i y to x minus i y preserves sums and products too, so it is an automorphism of the field with itself. It is called complex conjugation, and it is the only automorphism besides the identity that leaves every real number fixed.

**動畫**

ξ 與 ξ̄ 對實軸鏡射，中間一條虛線；右側把保和與保積的誤差列出來（都是 1e-16 級）。

## Beat 6 — 絕對值，以及它為什麼可乘 / the absolute value, and why it multiplies
*配音長度：中文 19.3s ／ 英文 16.8s*

**畫面公式**

```
絕對值，以及它為什麼可乘   |   the absolute value, and why it multiplies
ξ  ξ ‾   =   | ξ | ²                | ξ γ |   =   | ξ |  | γ |                ξ ⁻ ¹  =  ξ ‾ / | ξ | ²
```

**旁白（繁中）**

> 歐氏範數在這裡叫絕對值，而它是可乘的。硬把它平方再乘開來也能驗，可是有一個漂亮得多的做法：注意到一個數乘上它的共軛，就是它絕對值的平方。同一個等式順便也把反元素交出來。

**Narration (EN)**

> The Euclidean norm is called the absolute value, and it is multiplicative. Squaring and multiplying out would verify that, but it is much more elegant to notice that a number times its conjugate is the square of its absolute value. The same identity hands over the inverse.

**動畫**

ξ、ξ̄ 與落在實軸上的 ξξ̄；右側三組 |ab| 與 |a||b| 並排，都對得上。

## Beat 7 — 複線性推得出實線性，反過來不行 / complex linear gives real linear, not the reverse
*配音長度：中文 18.6s ／ 英文 18.4s*

**畫面公式**

```
複線性推得出實線性，反過來不行   |   complex linear gives real linear, not the reverse
ℂ  ⇒  ℝ                    ℝ   ⇏   ℂ
```

**旁白（繁中）**

> 接下來是一個警告。因為實數是子域，每個複向量空間自動也是實向量空間，每個複線性映射自動也是實線性的。反過來不成立：平面到自己的實線性映射，一般而言不是複線性的。

**Narration (EN)**

> Now a warning. Since the reals are a subfield, every complex vector space is automatically a real one and every complex linear map is automatically real linear. The converse fails: a real linear map of the plane to itself is in general not complex linear.

**動畫**

兩個框與一支單向箭頭，反方向打上 ⇏；底下是那個見證的實際數字：(iξ)‾ − i ξ̄ 的大小是 2.4。

## Beat 8 — 共軛的差商掃出整個圓 / the quotient for conjugation sweeps the circle
*配音長度：中文 19.3s ／ 英文 17.9s*

**畫面公式**

```
共軛的差商掃出整個圓   |   the quotient for conjugation sweeps the circle
Δ F ( ξ ) / ξ   =   ξ ‾ / ξ            →  1  ,    →  − 1
```

**旁白（繁中）**

> 共軛就是那個見證。它是實線性的，可是不是複線性的，而差商把理由講得很清楚：沿著實數方向走，它趨近一；沿著虛數方向走，它趨近負一。所以一個映射可以實可微而不複可微。

**Narration (EN)**

> Conjugation is the witness. It is real linear, but it is not complex linear, and the difference quotient shows why: along the real direction it tends to one, and along the imaginary direction to minus one. A map can be real differentiable without being complex differentiable.

**動畫**

十六個趨近方向的商畫在單位圓上，**掃滿一整圈**；+1 與 −1 兩點放大標出。
右側列出沿實軸、沿虛軸的值與散布 2.00。

## Beat 9 — 冪級數的差商縮成一點 / for a power series the quotient collapses
*配音長度：中文 17.1s ／ 英文 17.1s*

**畫面公式**

```
冪級數的差商縮成一點   |   for a power series the quotient collapses
d F ᵦ ( ξ )   =   F ′ ( β )  ·  ξ
```

**旁白（繁中）**

> 反過來說，冪級數自動就是複可微的。第 8 節已經給出：它在一點的微分就是「乘上逐項微分得到的那個數」，而乘上一個複數，在一維的複向量空間上是一個複線性的運算。

**Narration (EN)**

> Power series, on the other hand, are automatically complex differentiable. Section 8 gave that the differential at a point is multiplication by the term-by-term derivative, and multiplication by one complex number is a complex linear operation on a one-dimensional space.

**動畫**

同樣十六個方向的商，**全部擠在 F′(β) 附近**——散布只有 0.117，所以畫面把偏差**放大 12 倍**
（螢幕上標著「× 12」）才看得見。灰圓的半徑是那十六個商離 F′(β) 最遠的距離 0.060。
右側列出步長縮小時的最大偏差 0.1570 → 0.0296 → 0.0058。

## Beat 10 — 代數基本定理，與複指數 / the fundamental theorem of algebra, and the exponential
*配音長度：中文 16.0s ／ 英文 15.6s*

**畫面公式**

```
代數基本定理，與複指數   |   the fundamental theorem of algebra, and the exponential
x ²  +  1   =   ( x + i ) ( x − i )        e ˣ ⁺ ⁱ ʸ  =  e ˣ ( cos y + i sin y )
```

**旁白（繁中）**

> 而且還可以更進一步。非零的複數可以拿來除，所以差商自己就收斂到導數——導數又變回一個真正的商了。這一節收在代數基本定理，以及複數的指數函數。

**Narration (EN)**

> And one can go further. A nonzero complex number can be divided by, so the difference quotient itself converges to the derivative, which is an honest quotient again. The section closes with the fundamental theorem of algebra and the complex exponential.

**動畫**

兩個等式，底下用 z = 0.4 + 1.1i 把複指數的級數部分和與 e^x(cos y + i sin y) 對照：
誤差 8.3e-02 → 9.1e-05 → 1.4e-08 → 0。
