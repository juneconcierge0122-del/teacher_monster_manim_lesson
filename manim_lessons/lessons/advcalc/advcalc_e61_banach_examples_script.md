# advcalc E61 — 第 4 章：完備空間的例子與級數

Chapter 4: Examples of Complete Spaces, and Series

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 7 節「完備性」的後半（書頁 218–221，定理 7.5 到 7.11）。**第 7 節的內容收在書頁 221**，221–223 是習題 7.1–7.21，依 PLAYBOOK 第 8 節不做解答。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e61_banach_examples.py`（`AdvCalcE61ZH` / `AdvCalcE61EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[61]` / `FORMULAS_ADVCALC[61]`）
- 配音：`manim_lessons/samples/audio_e61/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.99 分（240 秒）／英文 3.58 分（215 秒）

## 一張清單，外加一招

E60 收在定理 7.4 與推論 2。這一集把第 7 節剩下的部分做完，內容其實是**一張 Banach 空間的清單**
加上**一招證明技巧**：

- 清單：有界函數（7.5）、有界線性映射（7.6）、有界又連續的函數（7.8 的推論）。
- 那一招是 ε 除以三：書上叫「上去、過去、下來」，用來證「均勻收斂保得住連續」。
- 中間插進「閉 ⟺ 完備」（7.7）與完備化，最後把緊緻拆成全有界加完備（7.9、引理 7.4、7.10），
  收在級數（7.11）與 Weierstrass 判別法。

**書上的 Fig. 4.3 畫的就是那一招**，依第 8 節，beat 4 的樓梯、標籤、數字全部自己重新設計，
沒有照書上的圖描。

七拍的數字都是算出來的：

- **beat 0 的一致範數是量出來的**：畫在螢幕上的成員是極限加上 sin 7x 除以 n，
  程式掃過整個區間求上確界，得到 0.500、0.250、0.125——正好是一除以 n。
- **beat 1 的斜率是收斂的**：1.60、1.35、1.22、1.15 → 1.10，驗過單調遞減、由上往下逼近。
- **beat 2 的序列驗過會逃走**：1／2、1／4、1／10、1／40 全都落在半開區間 (0, 1] 裡，
  彼此距離小於 0.08（所以是 Cauchy 的），可是極限 0 不在裡面。
- **beat 4 的三段各自小於 ε 除以三，加起來也小於 ε**：0.27 + 0.24 + 0.26 = 0.77 < 0.90。
- **beat 5 的極限真的不連續**：arctan(n x) 乘二除以 π，每一個成員都把 0 送到 0，
  可是在固定的 x = 0.25 上，值從 0.295 爬到 0.937，n 再大就逼近 1——極限是一個跳躍。
- **beat 7 的界是套出來的**：半徑一路 1、1／2、1／3、1／4，同一個半徑 1／4 的球裡
  任兩點相距不超過 0.5，這就是對角線那一支繼承到的 Cauchy 界。
- **beat 9 與 beat 10 的級數都真的加起來**：2 的負 i 次方的部分和 0.875 → 0.984 → 0.996；
  而 Weierstrass 那邊 **Σ 1／n² = 1.6449**，程式並且量出
  **‖σ₆ − σ₄‖∞ = 0.0671，確實不超過 M₅ + M₆ = 0.0678**。

## 三道檢查全過之後，probe 幀抓到六處

1. **beat 0 的「灰色細的兩條」其實有三條灰的**。原本畫四個成員（n = 1、2、4、8），
   第一個用 `DIM`，跟管子同色；而且 n = 1 的振幅是 1.0，是極限本身振幅的三倍多，
   整張圖被它蓋掉。改成三個成員（2、4、8）各給一個彩色，管子維持灰色，這樣註腳說的才對得上。
2. **beat 3 的箭頭指向空白**。ℚ 在 ℝ 裡的圖旁邊有一支箭頭，可是箭頭那一端什麼都沒有。刪掉。
3. **beat 4 的三段小到看不見**。原本 sy = 1.05、兩條曲線只差 0.17，三支箭頭各只有幾個像素。
   改成 sy = 1.55、差 0.30，並把兩個取樣點拉開，樓梯才讀得出來。
4. **beat 7 的球擠成一團**。原本四個球內切在同一個左緣，最小的那個半徑 0.24，
   裡面九個點糊成一坨，而且四個半徑標籤互相重疊、圓弧還穿過標籤。
   改成**同心**四個圓（半徑就是 1、1／2、1／3、1／4），標籤移到右邊排成一列。
5. **beat 8 的註腳說「往左」，可是畫面上沒有任何往左的箭頭**。公式列寫的是等價（⇔），
   圖上卻只有兩支往右的箭頭。改成雙向箭頭。
6. **beat 4 的表格顏色跟圖不一致**：圖上「上去」與「下來」是紅的、「過去」是紫的，
   表格裡三列卻都用紫色。改成逐列對上。

另外 **bounds 抓到三處**（beat 3 的標題、beat 7 最外圈的球、beat 10 的曲線超過 y = 1.30 的上限；
最後那個是因為 Σ sin(nx)／n² 的振幅實測是 1.10，比原本設的縮放大），
**collide 抓到十三處**，幾乎都是右側表格的最後一列壓到底下那行說明——
表格列數一多就會踩到，這一集有四拍都中了。

---

## Beat 0 — 定理 7.5：有界函數的空間 / Theorem 7.5: the bounded functions
*配音長度：中文 25.7s ／ 英文 21.2s*

**畫面公式**

```
定理 7.5：有界函數的空間   |   Theorem 7.5: the bounded functions
‖ f ‖ ∞  =  lub { ‖ f ( a ) ‖ : a ∈ A }            𝔅 ( A , W )
```

**旁白（繁中）**

> 第 7 節後半是一串例子，每一個都要證。定理 7.5：W 是 Banach 空間，A 是任意一個集合，那麼從 A 到 W 的所有有界函數，配上一致範數，也是 Banach 空間。做法是先讓每一點各自收斂得到極限函數，再用一致的控制證明它有界、而且真的是一致收斂過去。

**Narration (EN)**

> The rest of section 7 is a list of examples, and each one needs a proof. Theorem 7.5: if W is a Banach space and A is any set, the bounded functions from A to W, under the uniform norm, form a Banach space. Each point converges on its own, and the uniform control does the rest.

**動畫**

三條彩色的成員（n = 2、4、8）收進橘色那條粗的極限；灰色細的兩條是最後一個 n 的管子，
也就是一致範數下半徑 0.125 的球。右側的表列出三個 n 各自的 ‖fₙ − g‖∞。

## Beat 1 — 定理 7.6：極限還得是線性的 / Theorem 7.6: the limit must stay linear
*配音長度：中文 22.4s ／ 英文 21.2s*

**畫面公式**

```
定理 7.6：極限還得是線性的   |   Theorem 7.6: the limit must stay linear
W   Banach            ⇒            Hom ( V , W )   Banach
```

**旁白（繁中）**

> 定理 7.6 用同一套證明：V 是賦範空間、W 是 Banach 空間，那麼從 V 到 W 的有界線性映射也構成 Banach 空間。書上說方法一模一樣，留成習題，只多一件事要補——極限那個映射還得是線性的。第 8 節會一直用到這一條。

**Narration (EN)**

> Theorem 7.6 uses the same proof. If V is a normed space and W is Banach, the bounded linear maps from V to W form a Banach space. The book says the method is identical and leaves it as an exercise, with one extra thing to check: the limit map must be linear. Section 8 leans on it.

**動畫**

四條過原點的直線，斜率 1.60 → 1.15 一條比一條低，收到橘色那條斜率 1.10 的極限。
**每一條都是直的而且過原點**——這正是極限必須繼承的性質。

## Beat 2 — 定理 7.7：閉與完備互相換 / Theorem 7.7: closed and complete trade places
*配音長度：中文 18.9s ／ 英文 18.8s*

**畫面公式**

```
定理 7.7：閉與完備互相換   |   Theorem 7.7: closed and complete trade places
A ‾ = A  ⊂  B          ⟺          { x ₙ } ⊂ A  Cauchy  ⇒  x ₙ → a ∈ A
```

**旁白（繁中）**

> 定理 7.7 有兩半：完備空間的閉子集是完備的，而任何度量空間裡的完備子集一定是閉的。第二半有個很好的說法——完備的空間是絕對閉的：不管把它放進多大的空間裡，它在裡面永遠是閉集。

**Narration (EN)**

> Theorem 7.7 has two halves: a closed subset of a complete space is complete, and a complete subset of any metric space is closed. The second half reads nicely as this: a complete space is absolutely closed, staying closed inside however large a space you embed it in.

**動畫**

半開區間 (0, 1]：右端是實心點，左端是空心圈；1／2、1／4、1／10、1／40 的點一路往左端擠。
序列是 Cauchy 的，極限 0 卻不在集合裡——閉與完備在這裡一起壞掉。

## Beat 3 — 完備化，與「絕對閉」 / completion, and absolutely closed
*配音長度：中文 22.3s ／ 英文 16.8s*

**畫面公式**

```
完備化，與「絕對閉」   |   completion, and absolutely closed
ℚ   ⊂   ℝ                    ℚ ‾   =   ℝ   ≠   ℚ
```

**旁白（繁中）**

> 而這個性質其實跟完備等價。理由是：一個空間如果不完備，它可以被完備化，也就是造得出一個包含它的完備空間；它在那裡的閉包是完備的，跟它自己不一樣，所以它在那裡不是閉的。有理數配上實數就是最熟悉的例子。

**Narration (EN)**

> That property is equivalent to completeness. A space that is not complete can be completed: some complete space contains it, its closure there is complete and so differs from the space itself, so it is not closed there. Picture the rationals inside the reals.

**動畫**

一個方框（ℝ，完備）裡面套一個橢圓（ℚ）。ℚ 的閉包是整個方框，跟橢圓不一樣，
所以 ℚ 在 ℝ 裡不是閉的。

## Beat 4 — 定理 7.8：上去、過去、下來 / Theorem 7.8: up, over, and down
*配音長度：中文 21.0s ／ 英文 19.5s*

**畫面公式**

```
定理 7.8：上去、過去、下來   |   Theorem 7.8: up, over, and down
‖ g x − g a ‖    ≤    ϵ / 3   +   ϵ / 3   +   ϵ / 3    =    ϵ
```

**旁白（繁中）**

> 定理 7.8 是這一節最重要的一條：在有界函數空間裡，取那些同時連續的，得到的子空間是閉的。證明用一個經典的三段論證，書上叫「上去、過去、下來」——三段各壓在 ε 除以三以內，加起來剛好是 ε。

**Narration (EN)**

> Theorem 7.8 is the important one. Inside the bounded functions, take those that are also continuous, and that subspace is closed. The proof is the classical three-step argument the book calls up, over, and down: three pieces each held under a third of epsilon, adding to epsilon.

**動畫**

兩條曲線（下面橘色是極限 g，上面青色是 fₙ）與兩個取樣點 a、x。
三支箭頭走成一個樓梯：在 x 上去（紅）、沿著 fₙ 過去（紫）、在 a 下來（紅）。
右側的表列出三段的實際大小與合計 0.77 < 0.90。**這張圖是自己重新設計的，沒有照書上的 Fig. 4.3 描。**

## Beat 5 — 均勻收斂保得住連續 / uniform convergence keeps continuity
*配音長度：中文 21.6s ／ 英文 16.8s*

**畫面公式**

```
均勻收斂保得住連續   |   uniform convergence keeps continuity
‖ f ₙ − f ‖ ∞ → 0  ,  f ₙ ∈ 𝒞 ( A , W )        ⇒        f ∈ 𝒞 ( A , W )
```

**旁白（繁中）**

> 這條的傳統說法是：均勻收斂的連續函數列，極限函數也連續。書上特別提醒證明其實給得更多——只要每一個都在某一點連續，極限就在那一點連續。推論：又有界又連續的函數配上一致範數，是 Banach 空間。

**Narration (EN)**

> The classical statement: the limit of a uniformly convergent sequence of continuous functions is continuous. The book notes the proof gave more, that if each function is continuous at a point the limit is too. The bounded continuous functions are then a Banach space.

**動畫**

arctan(n x) 乘二除以 π，n = 2、8、40 三條曲線越站越直；橘色虛線畫出極限的兩段水平線，
中間是一個跳躍。**每一個成員都連續，逐點的極限卻不連續**——因為這一列不是均勻收斂的。

## Beat 6 — 定理 7.9：緊緻推得出完備 / Theorem 7.9: compact gives complete
*配音長度：中文 19.8s ／ 英文 19.8s*

**畫面公式**

```
定理 7.9：緊緻推得出完備   |   Theorem 7.9: compact gives complete
{ x ₙ }  Cauchy  ⊂  S  ∈  𝒦          ⇒          x ₙ   →   a   ∈   S
```

**旁白（繁中）**

> 定理 7.9：序列緊緻的度量空間一定完備。證明只有兩行——Cauchy 序列在序列緊緻的集合裡有收斂子序列，再引用引理 7.2 就結束了。反過來當然不成立：實數線完備，可是一點也不緊緻。

**Narration (EN)**

> Theorem 7.9: a sequentially compact metric space is complete. The proof is two lines. A Cauchy sequence in a sequentially compact set has a convergent subsequence, and Lemma 7.2 finishes it. The converse fails, of course: the line is complete and not compact at all.

**動畫**

一個橢圓（序列緊緻的集合）裡一條盤旋收進去的序列，四個放大的紅點是被抽出來的子序列，
中心的橘點是極限。

## Beat 7 — 引理 7.4：一層一層套下去 / Lemma 7.4: the nested construction
*配音長度：中文 22.3s ／ 英文 20.5s*

**畫面公式**

```
引理 7.4：一層一層套下去   |   Lemma 7.4: the nested construction
M ₁  ⊃  M ₂  ⊃  …  ⊃  M ₙ            r  =  1 ,  1 / 2 ,  … ,  1 / n
```

**旁白（繁中）**

> 缺的另一半是引理 7.4：全有界的集合裡，每個序列都有 Cauchy 子序列。證明是一層一層套下去的——先用有限多個半徑一的球，挑出裝了無窮多項的那一個；再換半徑二分之一、三分之一，一直套下去，最後沿著對角線挑出一支。

**Narration (EN)**

> The other half is Lemma 7.4: in a totally bounded set every sequence has a Cauchy subsequence. The proof nests. Cover with finitely many balls of radius one and keep one holding infinitely many terms; then radius a half, a third, and so on, and pick along the diagonal at the end.

**動畫**

四個同心圓，半徑就是 1、1／2、1／3、1／4，最裡面散著幾個點；右邊一列標出四個半徑。
同一個半徑 1／4 的球裡任兩點相距不超過 0.5——那就是對角線那一支繼承到的界。

## Beat 8 — 定理 7.10：緊緻拆成兩件事 / Theorem 7.10: compactness splits in two
*配音長度：中文 21.6s ／ 英文 21.0s*

**畫面公式**

```
定理 7.10：緊緻拆成兩件事   |   Theorem 7.10: compactness splits in two
S ∈ 𝒦      ⇔      S ⊂ B ᵣ [ F ] , | F | < ∞  ( ∀ r )      ∧      Cauchy ⇒ a ∈ S
```

**旁白（繁中）**

> 兩件合起來就是定理 7.10：一個度量空間序列緊緻，等價於它全有界而且完備。第 5 節證過緊緻推得出全有界，定理 7.9 補上完備；反過來則是引理 7.4 加上完備性。緊緻到這裡被拆成兩個獨立的條件。

**Narration (EN)**

> The two together give Theorem 7.10: a metric space is sequentially compact exactly when it is totally bounded and complete. Section 5 gave compact to totally bounded and Theorem 7.9 adds complete; the converse is Lemma 7.4 with completeness. Compactness splits in two.

**動畫**

左邊一個 𝒦 的框，右邊上下兩個框（全有界、完備），中間兩支**雙向**箭頭——
公式列寫的是等價，圖上就要兩個方向都畫出來。

## Beat 9 — 級數與絕對收斂 / series, and absolute convergence
*配音長度：中文 22.1s ／ 英文 20.5s*

**畫面公式**

```
級數與絕對收斂   |   series, and absolute convergence
σ ₙ  =  Σ ₁ ⁿ ξ ᵢ                Σ ₁ ∞ ‖ ξ ᵢ ‖  <  ∞        ⇒        σ ₙ  →  α
```

**旁白（繁中）**

> 最後講級數。賦範空間裡的級數收斂，意思是部分和的序列收斂。如果那些範數的級數在實數上收斂，就叫絕對收斂。定理 7.11：在 Banach 空間裡，絕對收斂的級數一定收斂，理由是部分和自己就是 Cauchy 的。

**Narration (EN)**

> Finally series. A series in a normed space converges when its partial sums do. If the series of norms converges in the reals, the series converges absolutely. Theorem 7.11: in a Banach space an absolutely convergent series converges, because the partial sums are Cauchy.

**動畫**

2 的負 i 次方的部分和畫成一道樓梯，一階一階逼近上方那條 Σ = 1 的虛線；
右側列出 σ₃ = 0.875、σ₆ = 0.984、σ₈ = 0.996。

## Beat 10 — Weierstrass 判別法 / the Weierstrass comparison test
*配音長度：中文 21.1s ／ 英文 17.6s*

**畫面公式**

```
Weierstrass 判別法   |   the Weierstrass comparison test
‖ f ₙ ‖ ∞  ≤  M ₙ            Σ M ₙ  <  ∞            ⇒            ‖ Σ f ₙ − s ‖ ∞  →  0
```

**旁白（繁中）**

> 書上說反過來也對，並且留成習題：一個賦範空間如果每個絕對收斂的級數都收斂，那它就完備。所以這個性質本身就刻畫了 Banach 空間。推論是古典的 Weierstrass 判別法：找得到一列常數蓋住，級數就均勻收斂。

**Narration (EN)**

> The book says the converse holds and leaves it as an exercise: if every absolutely convergent series in a normed space converges, that space is complete. So the property characterizes Banach spaces. The corollary is the classical Weierstrass comparison test.

**動畫**

Σ sin(n x)／n² 的前二、前四、前六項部分和，三條曲線**幾乎完全疊在一起**——
均勻收斂看起來就是這樣。右側把那個看不見的差變成數字：
Σ 1／n² = 1.6449，而 ‖σ₆ − σ₄‖∞ = 0.0671，確實不超過 M₅ + M₆ = 0.0678。
差是被常數蓋住的，跟 x 無關，這正是判別法的內容。
