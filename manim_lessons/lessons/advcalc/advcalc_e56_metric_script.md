# advcalc E56 — 第 4 章：度量空間、開集與閉集

Chapter 4: Metric Spaces, Open and Closed Sets

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 4 章第 1 節「度量空間；開集與閉集」（書頁 195–200，習題 1.1–1.15 在 200–201）。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e56_metric.py`（`AdvCalcE56ZH` / `AdvCalcE56EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[56]` / `FORMULAS_ADVCALC[56]`）
- 配音：`manim_lessons/samples/audio_e56/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.40 分（204 秒）／英文 3.23 分（194 秒）

## 抽掉向量運算之後還剩什麼

前面三章談收斂與連續時，其實只用到「兩點之間的距離」。把它抽出來就是三條公理，
而整個開集、閉集、閉包、邊界的機器都可以重建在上面。這一集的四個判斷是算出來的：

- **大圓距離真的是一個度量**：在球面上取九個點，把 729 組三元組的三角不等式全跑一遍，
  一次都沒壞。這個度量不是由任何範數給出來的。
- **引理 1.1 驗過**：在小球邊界上取 720 個點，斷言每一個到大球中心的距離都小於 r。
- **引理 1.2 的 Lipschitz 常數是 1，而且 1 取得到**：取樣的比值最大只到 0.497，
  所以另外用一組共線的點斷言比值正好是 1——**只取樣的話會誤以為常數比 1 小**。
- **正像不保持閉**：`2x/(1+x²)` 把正整數送成一列往零掉的數，
  斷言每一項都大於零、而第 100 項只剩 0.02，所以零在像的閉包裡卻不在像裡。
- **引理 1.5 為什麼改不好**：造出書上說的那種序列——連續的斜坡逼近一個指示函數——
  斷言它到子空間的距離一路往上（0.866 → 0.9585 → 0.9917 → 0.9983），
  **而且斷言它永遠小於 1**。這就是無窮維時「最近的點不存在」的有限影子。

probe 幀與三道工具抓到四處：beat 7 的橢圓超出左緣、兩張表的最後一列撞到說明文字，
還有 langscan 對 `"xyz"[k]` 這個寫法報了一次——那是誤報，可是改成 `("x","y","z")[k]` 之後
意圖也比較清楚。

---

## Beat 0 — 抽出來只剩三條 / what is left is three axioms
*配音長度：中文 21.5s ／ 英文 16.9s*

**畫面公式**

```
抽出來只剩三條   |   what is left is three axioms
ρ  :  A × A  →  ℝ                ρ ( x , z )   ≤   ρ ( x , y )  +  ρ ( y , z )
```

**旁白（繁中）**

> 第 4 章從度量空間開始。前面三章談收斂與連續時，其實只用到「兩點之間的距離」這件事。把它抽出來就是三條公理：不同點的距離為正、對稱、以及三角不等式。有了這三條就叫度量空間。

**Narration (EN)**

> Chapter 4 begins with metric spaces. Everything the last three chapters did with convergence and continuity used only the distance between two points. Distilled, that is three axioms: positive for distinct points, symmetric, and the triangle inequality.

**動畫**

左邊一個三角形，三個頂點標成 x、y、z。右側三行是三條公理。

## Beat 1 — 任何子集也是一個度量空間 / any subset is one too
*配音長度：中文 17.7s ／ 英文 17.1s*

**畫面公式**

```
任何子集也是一個度量空間   |   any subset is one too
ρ ( α , β )  =  ‖ α − β ‖              B  ⊂  A        ⇒        ( B ,  ρ ↾ B )
```

**旁白（繁中）**

> 賦範空間用範數當距離就是度量空間，而它的任何子集也是。這一點很要緊：從 ℝⁿ 裡挖一個奇怪的子集出來，得到的度量空間可以非常古怪，幾乎任何你想得到的性質它都可能沒有。

**Narration (EN)**

> A normed space is a metric space under the norm distance, and so is any subset of a metric space. That matters: carve a weird subset out of real n-space and the metric space you get can be very odd indeed, failing almost any property you can think of.

**動畫**

左邊一個灰色的方框，裡面散落八個紅點。
右側說明賦範空間與它的任何子集都是度量空間。

## Beat 2 — 不是每個度量都來自範數 / not every metric comes from a norm
*配音長度：中文 18.7s ／ 英文 13.8s*

**畫面公式**

```
不是每個度量都來自範數   |   not every metric comes from a norm
S  =  { x ∈ ℝ ³ : Σ x ᵢ ² = 1 }            ρ ( x , y )  =  cos ⁻¹ ⟨ x , y ⟩
```

**旁白（繁中）**

> 度量也不是只有範數這一種。書上舉的例子是三維裡的球面，距離取大圓的長度；更一般地，任何光滑曲面上兩點的距離可以取曲面內最短曲線的長度。這些都不是由某個範數給出來的。

**Narration (EN)**

> Metrics come from other places too. The book's example is a sphere in three-space with the great-circle distance, or more generally any smooth surface with the length of the shortest curve inside it. Neither of those comes from a norm.

**動畫**

左邊一顆球（輪廓加兩條緯線），球面上兩點之間畫一段紅色的大圓弧，以及一條灰色虛線的直線距離。
右側說明紅色那個才是這個度量空間的距離。

## Beat 3 — 球是開的 / a ball is open
*配音長度：中文 19.1s ／ 英文 18.9s*

**畫面公式**

```
球是開的   |   a ball is open
B ᵣ ( p )  =  { x : ρ ( x , p ) < r }              δ   =   r   −   ρ ( p , q )
```

**旁白（繁中）**

> 定義照搬：連續是給了 ε 就有 δ；半徑 r 的球是離中心小於 r 的點；一個集合是開的，如果它裡面每一點都是某個含在裡面的球的中心。引理 1.1 說每個球都是開的，而證明就是三角不等式。

**Narration (EN)**

> The definitions carry over: continuity is the epsilon-delta one, a ball of radius r is the points nearer than r to its centre, and a set is open if every point of it centres some ball inside it. Lemma 1.1 says every ball is open, and the proof is the triangle inequality.

**動畫**

左邊一個大圓與裡面一點，那點外面再畫一個半徑 δ 的小圓。
右側是 δ = r − ρ(p,q) 與四行說明。

## Beat 4 — 開集族的三條性質 / three properties of the open sets
*配音長度：中文 17.6s ／ 英文 18.3s*

**畫面公式**

```
開集族的三條性質   |   three properties of the open sets
∪ ᵢ A ᵢ  ∈  𝒯            A ∩ B  ∈  𝒯            ∅ ,  X  ∈  𝒯
```

**旁白（繁中）**

> 定理 1.1 把開集族的三條性質列出來：任意多個開集的聯集是開的，兩個開集的交是開的，空集與全空間是開的。推論很好記：一個集合是開的，等價於它是一堆開球的聯集。

**Narration (EN)**

> Theorem 1.1 lists three properties of the family of open sets: arbitrary unions are open, the intersection of two is open, and the empty set and the whole space are open. The corollary is easy to remember: a set is open exactly when it is a union of open balls.

**動畫**

左邊三張小圖分別畫聯集、交集、以及空集與全空間。
右側是開集族的三條性質。

## Beat 5 — 內部、閉包、邊界 / interior, closure, boundary
*配音長度：中文 17.3s ／ 英文 19.0s*

**畫面公式**

```
內部、閉包、邊界   |   interior, closure, boundary
∂ A    =    Ā    −    A ⁱⁿᵗ                ( Ā ) ′   =   ( A ′ ) ⁱⁿᵗ
```

**旁白（繁中）**

> 接下來一組互補的定義：內部是所有含在裡面的開集的聯集，也就是最大的那個開子集；閉集是補集為開的集合；閉包是所有包含它的閉集的交，也就是最小的閉超集；邊界是閉包減去內部。

**Narration (EN)**

> Then a complementary set of definitions: the interior is the union of all open subsets, the largest one; a set is closed when its complement is open; the closure is the intersection of all closed supersets, the smallest one; and the boundary is the closure minus the interior.

**動畫**

左邊一個不規則的閉曲線（閉包）套著另一個較小的（內部）。
右側是邊界的定義與三行說明。

## Beat 6 — 隨手一個集合通常兩者都不是 / a random set is usually neither
*配音長度：中文 17.4s ／ 英文 16.3s*

**畫面公式**

```
隨手一個集合通常兩者都不是   |   a random set is usually neither
p  ∈  Ā          ⇔          ∀ r > 0     B ᵣ ( p )  ∩  A   ≠   ∅
```

**旁白（繁中）**

> 有一個很好用的刻畫：一點落在閉包裡，等價於它周圍每一個球都跟那個集合相交。書上提醒：隨手拿一個集合，它通常既不開也不閉——把球面的一部分加進開球就是這樣的例子。

**Narration (EN)**

> One characterisation is very usable: a point lies in the closure exactly when every ball about it meets the set. The book warns that a set picked at random is generally neither open nor closed; adding part of a sphere to an open ball is such a set.

**動畫**

左邊一個虛線的圓，其中一段畫成實心紅色——開球加上邊界的一部分。
右側說明它既不開也不閉。

## Beat 7 — 連續：逆像保持開與閉 / continuity: inverse images behave
*配音長度：中文 17.7s ／ 英文 18.3s*

**畫面公式**

```
連續：逆像保持開與閉   |   continuity: inverse images behave
A  ∈  𝒯 ᵧ            ⇒            f ⁻¹ [ A ]   ∈   𝒯 ₓ
```

**旁白（繁中）**

> 引理 1.4 把連續性翻成集合的語言：f 連續，那麼開集的逆像是開的；推論是閉集的逆像是閉的。而且兩個的反面也成立，所以這其實可以當成連續的定義——第 2 節就會這樣做。

**Narration (EN)**

> Lemma 1.4 restates continuity in the language of sets: if f is continuous, the inverse image of an open set is open, and the corollary says the same for closed sets. Both converses hold too, so this could be taken as the definition, which is what section 2 does.

**動畫**

左邊兩團集合，各自裡面一個圓，兩支箭頭一來一往標成 f 與 f 的逆。
右側說明逆像保持開與閉。

## Beat 8 — 可是正像不保持 / forward images do not
*配音長度：中文 19.8s ／ 英文 19.1s*

**畫面公式**

```
可是正像不保持   |   forward images do not
f ( x )  =  2 x / ( 1 + x ² )              0   ∈   f [ ℤ ⁺ ] ‾   ∖   f [ ℤ ⁺ ]
```

**旁白（繁中）**

> 可是正像不保持。反正切函數的像是開區間，不是閉的。讀者可能覺得這例子取巧，那就換一個：f 取二 x 除以一加 x 平方，值域是閉區間，可是正整數這個閉集的像不閉——零在它的閉包裡。

**Narration (EN)**

> Forward images do not behave. The range of the arctangent is an open interval, not closed. If that feels like cheating, take two x over one plus x squared, whose range is closed; the image of the positive integers, a closed set, is not, since zero lies in its closure.

**動畫**

左邊反正切的曲線與它永遠碰不到的紅色虛線，右邊一張表：正整數在那個映射下的像往零掉。

## Beat 9 — 不相交也可以距離為零 / disjoint can still mean distance zero
*配音長度：中文 18.5s ／ 英文 17.6s*

**畫面公式**

```
不相交也可以距離為零   |   disjoint can still mean distance zero
ρ ( A , B )    =    glb  { ρ ( a , b )  :  a ∈ A ,  b ∈ B }
```

**旁白（繁中）**

> 兩個集合之間的距離取點對點距離的下確界。相交當然是零，可是不相交也可能是零：圓的內部與外部是不相交的開集，距離是零；x 軸與一除以 x 的圖形是不相交的閉集，距離也是零。

**Narration (EN)**

> The distance between two sets is the greatest lower bound of the point distances. Intersecting sets are at distance zero, but disjoint ones can be too: the inside and outside of a circle are disjoint open sets at distance zero, as are the axis and the graph of one over x.

**動畫**

左邊 x 軸與一除以 x 的圖形，中間幾條虛線標出縫隙。
右側說明兩個不相交的閉集距離是零。

## Beat 10 — 引理 1.5，以及它為什麼改不好 / Lemma 1.5, and why it cannot improve
*配音長度：中文 18.6s ／ 英文 18.7s*

**畫面公式**

```
引理 1.5，以及它為什麼改不好   |   Lemma 1.5, and why it cannot improve
‖ α ‖  =  1                    ρ ( α , N )    >    1  −  ϵ
```

**旁白（繁中）**

> 最後是引理 1.5：N 是一個真閉子空間，那麼對任何小於一的正數，都找得到一個單位向量，它到 N 的距離大於一減那個數。讀者會想「取最近的點不就好了」——可是無窮維時最近的點可能不存在。

**Narration (EN)**

> Finally Lemma 1.5: if N is a proper closed subspace, then for any positive number below one there is a unit vector whose distance to N exceeds one minus it. One wants to improve this by taking the nearest point of N, but in infinite dimensions a nearest point may not exist.

**動畫**

左邊一條往上爬的曲線與一條標在 1 的紅色虛線，右邊一張表列出四個 k 值與對應的距離。

---

## 一個只取樣會看錯的地方

引理 1.2 說「到定點的距離」是 Lipschitz 常數 1 的函數。在圓周上隨機取兩點算比值，
最大只到 0.497——如果只做這件事，會得出「常數是 0.5」的錯誤印象。
常數 1 只在共線的時候取得到，所以程式另外算了一組共線的點，斷言比值正好是 1。
**取樣證明不了「上界是最好的」，只有找到達到它的例子才行。**

## 引理 1.5 為什麼不能改成「等於一」

直覺會說：取 N 裡離 β 最近的那一點不就好了嗎？可是無窮維時那個最近的點可能不存在。
畫面上那條往上爬的曲線就是這件事的樣子：連續的斜坡越來越陡，
到子空間的距離一路逼近 1，可是每一項都嚴格小於 1，而極限那個「指示函數」不連續，
不在空間裡。有限維時一定取得到，Hilbert 空間也取得到；書上那個反例兩者都不是。
