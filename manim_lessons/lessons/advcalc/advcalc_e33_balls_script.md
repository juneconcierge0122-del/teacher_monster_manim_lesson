# advcalc E33 — 第 3 章：球、開集與閉集

Chapter 3: Balls, Open Sets and Closed Sets

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 3 章第 2 節的後段（書頁 123–125）。書頁 125 起是習題 2.1–2.15。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e33_balls.py`（`AdvCalcE33ZH` / `AdvCalcE33EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[33]` / `FORMULAS_ADVCALC[33]`）
- 配音：`manim_lessons/samples/audio_e33/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 3.34 分（200 秒）／英文 2.99 分（179 秒）

## 三顆單位球是由範數畫出來的

書上 Fig 3.2 畫的是同樣三個形狀。依第 8 節重畫時，這裡不手寫任何座標：`_unit` 走一圈方向，
對每個方向問「這個範數的單位球在這個方向走多遠」，也就是 `1 / ‖ ( cos θ , sin θ ) ‖`。一段程式
畫三種球，形狀完全由定義決定。

場景檔接著斷言這一集要講的包含關係真的成立（每個方向上 `r₁ ≤ r₂ ≤ r∞`），並且檢查對角線方向上
下標一的球到 `1/√2`、下標無窮的到 `√2`。

**beat 9 的鋪球也是算的。** 初稿隨手放的六顆球有幾顆穿出了那團形狀的邊界——旁白說「開集是一堆
開球鋪成的」，圖卻畫成球跑到集合外面。現在改成用二分法找出每個球心「還留在形狀裡的最大半徑」，
再取 94%，並斷言每顆球的邊界取樣點都在裡面；順便發現原本第六顆球的位置離邊界太近，只塞得下
半徑 0.076，已經移到內側。

---

## Beat 0 — 開球：距離小於 r 的那些點 / the open ball: everything closer than r
*配音長度：中文 16.8s ／ 英文 15.2s*

**畫面公式**

```
開球：距離小於 r 的那些點   |   the open ball: everything closer than r
B ᵣ ( α )   =   { ξ   :   ‖ ξ − α ‖  <  r }
```

**旁白（繁中）**

> 有了範數就有距離，有了距離就可以講「附近」。以 α 為心、半徑 r 的開球，就是所有跟 α 的距離嚴格小於 r 的那些點。這是把上一集那個 δ 帶搬到向量空間的說法。

**Narration (EN)**

> A norm gives distances, and distances let us speak of nearby. The open ball of radius r about alpha is every point whose distance to alpha is less than r. It is the delta band of the last episode, moved onto a vector space.

**動畫**

一個圓、圓心 α、一支標著 r 的半徑箭頭，圓內一個點、圓外一個點。右邊三行說明「嚴格小於」與為什麼叫開球。

## Beat 1 — 平移與縮放對球做的事 / what translation and scaling do to a ball
*配音長度：中文 18.3s ／ 英文 18.2s*

**畫面公式**

```
平移與縮放對球做的事   |   what translation and scaling do to a ball
T ᵦ [ B ᵣ ( α ) ]  =  B ᵣ ( α + β )        c B ᵣ ( α )  =  B | c | ᵣ ( c α )
```

**旁白（繁中）**

> 球對平移與縮放的反應很乾淨。整個空間平移 β，球就跟著平移：球心加 β、半徑不變。乘上一個數 c，半徑就乘上 c 的絕對值。理由都只是把範數的公理代進去。

**Narration (EN)**

> Balls behave cleanly under translation and scaling. Translate the whole space by beta and the ball translates with it: same radius, centre moved by beta. Multiply by c and the radius is multiplied by the size of c. Both follow from the axioms and nothing else.

**動畫**

三顆球：原球、平移後的球（球心跟著走、半徑不變）、以及縮放後的球（原球用暗線留著對照）。

## Beat 2 — 三種範數，三種單位球 / three norms, three unit balls
*配音長度：中文 19.7s ／ 英文 18.0s*

**畫面公式**

```
三種範數，三種單位球   |   three norms, three unit balls
‖ x ‖ ₁ < 1        ‖ x ‖ ₂ < 1        ‖ x ‖ ∞ < 1
```

**旁白（繁中）**

> 但「球」這個字會騙人。同一個空間、三種範數，單位球長得完全不一樣：下標二那個是圓的，下標一那個是斜的正方形，下標無窮那個是正的正方形。三個都叫球，只有一個真的是圓的。

**Narration (EN)**

> But the word ball is misleading. On one space with three norms the unit balls look nothing alike: the subscript two one is round, the subscript one one is a tilted square, and the subscript infinity one is an upright square. All three are called balls and only one is round.

**動畫**

三顆單位球分開並排，各自配一組座標軸與名稱。三個形狀是同一段程式照著範數的定義畫的——對每個方向問這個範數的單位球走多遠。

## Beat 3 — 而且一個包一個 / and they nest, one inside the next
*配音長度：中文 22.3s ／ 英文 16.8s*

**畫面公式**

```
而且一個包一個   |   and they nest, one inside the next
‖ x ‖ ∞  ≤  ‖ x ‖ ₂  ≤  ‖ x ‖ ₁        ⇒        B ₁ ⊂ B ₂ ⊂ B ∞
```

**旁白（繁中）**

> 而且三者之間有大小關係：下標一的球最小、下標無窮的球最大、下標二的夾在中間。畫在同一張圖上就是一個正方形裡包著圓、圓裡再包著斜正方形。這後面會變成「有限維上所有範數等價」那個定理的具體樣子。

**Narration (EN)**

> They also nest: the subscript one ball is the smallest, the subscript infinity ball the largest, and the subscript two ball lies between them. Later that nesting becomes the concrete face of the theorem that all norms on a finite dimensional space are equivalent.

**動畫**

三顆單位球疊在同一組座標上：斜正方形在圓裡、圓在正方形裡，對角線方向上各標一個點。右邊列出三顆球沿對角線各走多遠（1/√2、1、√2）。

## Beat 4 — 有界：整個裝得進某一顆球 / bounded: it fits inside some ball
*配音長度：中文 15.1s ／ 英文 14.4s*

**畫面公式**

```
有界：整個裝得進某一顆球   |   bounded: it fits inside some ball
A ⊂ B ᵣ ( α )        ⇒        A ⊂ B ᵣ ₊ ‖ α ‖ ( 0 )
```

**旁白（繁中）**

> 一個集合如果整個裝得進某一顆球，就叫有界。裝得進以 α 為心的球，也就一定裝得進以原點為心、半徑加大一點的球——把三角不等式反過來用一次就得到。

**Narration (EN)**

> A set that fits inside some ball is called bounded. Fitting inside a ball about alpha forces it to fit inside a ball about the origin with a slightly larger radius, which is the triangle inequality used once, backwards.

**動畫**

一團不規則形狀 A 裝在以 α 為心的球裡，外面再套一顆以原點為心、半徑加大的球。

## Beat 5 — 點到集合的距離 / the distance from a point to a set
*配音長度：中文 17.6s ／ 英文 14.3s*

**畫面公式**

```
點到集合的距離   |   the distance from a point to a set
ρ ( β , A )   =   glb { ‖ ξ − β ‖   :   ξ ∈ A }
```

**旁白（繁中）**

> 一個點到一個集合的距離，定義成它到集合裡每一點的距離的最小下界。這就是「以那個點為心、碰不到那個集合的最大的球」的半徑。如果那個點本來就在集合裡，這個距離就是零。

**Narration (EN)**

> The distance from a point to a set is defined as the greatest lower bound of its distances to the points of the set. It is the radius of the largest ball about that point that does not touch the set, and it is zero when the point belongs to the set.

**動畫**

一個點 β 與一條曲線 A，一顆以 β 為心、剛好碰到 A 的球，以及從 β 連到最近點的線段。

## Beat 6 — 內點與開集 / interior points, and open sets
*配音長度：中文 15.4s ／ 英文 13.2s*

**畫面公式**

```
內點與開集   |   interior points, and open sets
∃ r > 0  :  B ᵣ ( α ) ⊂ A
```

**旁白（繁中）**

> 接下來是這一節真正的目標：開集與閉集。α 叫集合 A 的內點，如果有一顆以 α 為心的球整個落在 A 裡面。每一點都是內點的集合，就叫開集。

**Narration (EN)**

> Now the real target of the section: open and closed sets. A point alpha is an interior point of A if some ball about alpha lies entirely inside A. A set all of whose points are interior is called open.

**動畫**

一團不規則形狀 A，裡面一個內點配一顆整個落在裡面的小球；邊界上一個點配一顆有一半在外面的球。

## Beat 7 — 開球確實是開集 / an open ball really is an open set
*配音長度：中文 16.0s ／ 英文 17.1s*

**畫面公式**

```
開球確實是開集   |   an open ball really is an open set
β ∈ B ᵣ ( α )        δ  =  r − ‖ α − β ‖
```

**旁白（繁中）**

> 既然叫開球，開球最好真的是開集，這要證。取球裡的一點 β，它到球心的距離小於 r，剩下的空間就是 r 減掉那個距離；以這個為半徑的小球整個留在大球裡。

**Narration (EN)**

> Since they are called open balls, an open ball had better be an open set, and that needs proof. Take a point beta inside it; its distance to the centre is less than r, and the room left over is r minus that distance. A ball of that radius about beta stays inside.

**動畫**

一顆大球 B ᵣ ( α )，裡面一點 β，從球心到 β 的連線，以及以 β 為心、半徑等於剩下空間的小球。

## Beat 8 — 證明就是三角不等式 / the proof is the triangle inequality
*配音長度：中文 16.0s ／ 英文 15.8s*

**畫面公式**

```
證明就是三角不等式   |   the proof is the triangle inequality
‖ ξ − α ‖  ≤  ‖ ξ − β ‖ + ‖ β − α ‖  <  δ + ( r − δ )  =  r
```

**旁白（繁中）**

> 證的方法就是三角不等式：小球裡的點到球心的距離，不會超過它到 β 的距離加上 β 到球心的距離，兩段加起來還是小於 r。直覺很可靠，但還是要算一次。

**Narration (EN)**

> The proof is the triangle inequality: a point of the small ball is no further from the centre than its distance to beta plus beta's distance to the centre, and those two together are still less than r. The intuition is reliable, but it still gets checked.

**動畫**

同一張圖再加上小球裡的一點 ξ，三段線段畫出 ξ 到 β、β 到 α、ξ 到 α。右邊寫出三角不等式那一串，末端得到 < r。

## Beat 9 — 開集是一堆球鋪成的 / an open set is paved with balls
*配音長度：中文 21.3s ／ 英文 18.6s*

**畫面公式**

```
開集是一堆球鋪成的   |   an open set is paved with balls
A   =   ∪  B ᵣ ( α )
```

**旁白（繁中）**

> 開集的聯集還是開集，不管聯集有多少個。而任何開集都是一堆開球的聯集——這大概是想像開集最舒服的方式：一團形狀不規則的東西，由無數顆球鋪成。但交集不保證：無窮多顆開球的交集可以縮成一個點。

**Narration (EN)**

> A union of open sets is open, however many there are, and every open set is a union of open balls. That is the most comfortable way to picture one: an irregular shape paved with countless balls. Intersections carry no such guarantee; infinitely many can meet in one point.

**動畫**

一團不規則形狀裡鋪著六顆球。每顆球的半徑是程式用二分法算出「還留在形狀裡的最大值」再取 94%，並驗過每顆球的邊界取樣點確實都在裡面。

## Beat 10 — 閉集：補集是開的 / closed: the complement is open
*配音長度：中文 21.8s ／ 英文 17.5s*

**畫面公式**

```
閉集：補集是開的   |   closed: the complement is open
α ∉ C        ⇒        ρ ( α , C )  >  0
```

**旁白（繁中）**

> 補集是開集的集合叫閉集。等價的說法是：不在裡面的每一個點，到它的距離都是正的。閉球是閉集，證明又是三角不等式。要注意開與閉既不互斥也不窮盡，有些集合兩者都不是。下一集講連續。

**Narration (EN)**

> A set whose complement is open is called closed; equivalently, every point outside it lies at a positive distance from it. A closed ball is closed, by the triangle inequality again. Open and closed are neither exclusive nor exhaustive. Next time: continuity.

**動畫**

一顆閉球，外面一個點 α 配一顆碰不到它的小球，兩者之間一條連線——外面的每一點離它都有正的距離。
