# 第 46 課｜劉維定理：相空間的體積不會改變（Landau §46）

Lesson 46 — Liouville's theorem: phase volume never changes

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l46_liouville.py`（`LandauL46ZH` / `LandauL46EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[46]` 與 `FORMULAS[46]`
- 配音：`manim_lessons/samples/audio_l46/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 9 秒、英文約 2 分 11 秒

最後三拍才是這一課的重點，所以那裡放真正的計算：一小塊初始條件被單擺的相流帶著走，邊界在 import 時用 RK4 積分一次存成表，updater 只查表。方塊被剪切、拉長、扯成細絲，旁邊即時算出來的鞋帶公式面積卻始終不動——那就是定理本身。

---

## 第 0 拍｜相空間：座標與動量張成

**畫面公式**：相空間：座標與動量張成　/　phase space: coordinates and momenta　/　`dΓ = dq₁ … dq_s dp₁ … dp_s`

**中文旁白**：為了幾何地看力學現象，我們常常用相空間：一個二倍 s 維的空間，座標軸就是 s 個廣義座標和 s 個動量。每一點代表系統的一個確定狀態。

**English**: To look at mechanics geometrically we often use phase space: a space of two s dimensions whose axes are the s generalised coordinates and the s momenta. Each point of it corresponds to one definite state of the system.

**動畫**：相平面的座標軸、一條相軌跡，以及沿著它跑的代表點。

---

## 第 1 拍｜體積元 dΓ

**畫面公式**：體積元 dΓ　/　the volume element dΓ　/　`∫ dΓ`

**中文旁白**：系統運動時，代表它的點就在相空間裡畫出一條曲線，叫做相軌跡。而所有微分的乘積，可以看成相空間裡的體積元。

**English**: As the system moves, the point representing it traces out a curve called the phase path. The product of all the differentials may be regarded as an element of volume in this space.

**動畫**：軌跡旁邊多出一個紅色的小方塊，代表體積元 dΓ。

---

## 第 2 拍｜正則變換會改變體積嗎？

**畫面公式**：正則變換會改變體積嗎？　/　does a canonical transformation change it?　/　`∫∫ dQ dP = ∫∫ D dq dp        D = ∂ ( Q , P ) / ∂ ( q , p )`

**中文旁白**：考慮這個體積元在一塊區域上的積分，它就是那塊區域的體積。我們要證明的是：這個積分在正則變換下不變。

**English**: Consider the integral of that element over some region, which is simply the volume of the region. What we shall show is that this integral is invariant under canonical transformations.

**動畫**：換成兩塊區域的對照：左邊是 (q, p) 裡的一塊，右邊是它在正則變換下的像，問兩者面積是否相等。

---

## 第 3 拍｜只要證明雅可比行列式等於一

**畫面公式**：只要證明雅可比行列式等於一　/　it is enough that the Jacobian be one　/　`D = 1  ?`

**中文旁白**：多重積分換變數的時候要乘上雅可比行列式。所以要證的其實是：每一個正則變換的雅可比行列式都等於一。

**English**: Changing variables in a multiple integral brings in the Jacobian of the transformation. So what has to be proved is that the Jacobian of every canonical transformation is equal to one.

**動畫**：同一組對照圖：換變數要乘上雅可比，所以要證 D = 1。

---

## 第 4 拍｜雅可比可以當分數處理

**畫面公式**：雅可比可以當分數處理　/　Jacobians may be handled like fractions　/　`D = [ ∂ ( Q ) / ∂ ( q ) ]_P  /  [ ∂ ( p ) / ∂ ( P ) ]_q`

**中文旁白**：雅可比行列式有個好用的性質，可以像分數一樣處理。分子分母同時除以舊座標和新動量的組合，就化成兩個 s 階行列式的比。

**English**: Jacobians have a useful property: they can be handled somewhat like fractions. Dividing numerator and denominator by the old coordinates together with the new momenta reduces it to a ratio of two determinants of order s.

**動畫**：同一組對照圖：把雅可比當分數處理，化成兩個 s 階行列式的比。

---

## 第 5 拍｜用生成函數寫出矩陣元

**畫面公式**：用生成函數寫出矩陣元　/　the elements through the generating function　/　`∂Qᵢ/∂qₖ = ∂²Φ / ∂qₖ ∂Pᵢ`

**中文旁白**：用以舊座標和新動量為變數的生成函數寫出來，分子那個行列式的元素是生成函數對舊座標和新動量的二階偏導數。

**English**: Writing the transformation through the generating function of the old coordinates and the new momenta, the element of the determinant in the numerator is its second derivative by an old coordinate and a new momentum.

**動畫**：同一組對照圖：用生成函數寫出分子與分母的矩陣元。

---

## 第 6 拍｜只差行與列互換，所以相等

**畫面公式**：只差行與列互換，所以相等　/　rows and columns interchanged: equal　/　`∂pᵢ/∂Pₖ = ∂²Φ / ∂qᵢ ∂Pₖ       ⟹      D = 1`

**中文旁白**：分母那個行列式的元素也是同一個二階偏導數，只是把兩個指標對調。所以兩個行列式只差行與列互換，數值相等，比值就是一。證明完成。

**English**: The element of the determinant in the denominator is that same second derivative with the two indices interchanged. The determinants therefore differ only by an interchange of rows and columns, so they are equal and the ratio is one.

**動畫**：同一組對照圖：兩個行列式只差行列互換，所以 D = 1。

---

## 第 7 拍｜運動本身就是一串正則變換

**畫面公式**：運動本身就是一串正則變換　/　the motion is itself a chain of them　/　`q_t , p_t     ⟶     q_{t+τ} , p_{t+τ}`

**中文旁白**：接下來是關鍵的一步：上一課末尾說過，系統隨時間的演化本身就是一連串正則變換，它的生成函數正是負的作用量。

**English**: Now the key step: at the end of the last lesson we saw that the evolution of the system in time is itself a series of canonical transformations, whose generating function is minus the action.

**動畫**：換成真正的相流：一塊方形的初始條件出現，上方即時顯示它的面積。

---

## 第 8 拍｜形狀改變，體積不變

**畫面公式**：形狀改變，體積不變　/　the shape changes, the volume does not　/　`∫ dΓ = const`

**中文旁白**：所以，讓區域裡每一點都按運動方程走，整塊區域會跟著移動、被拉長、被剪切、纏成很細的形狀，但它的體積始終不變。這就是劉維定理。

**English**: So if every point of a region moves according to the equations of motion, the region moves too, and it may be stretched, sheared and drawn out into very fine filaments, yet its volume never changes. This is Liouville's theorem.

**動畫**：方塊被單擺的相流剪切、拉長，形狀完全走樣，上方的面積讀數卻停在原值不動。

---

## 第 9 拍｜相流像不可壓縮流體

**畫面公式**：相流像不可壓縮流體　/　the phase flow is incompressible　/　`∫∫ Σ dqᵢ dpᵢ   ,   ∫∫∫∫ Σ dqᵢ dqₖ dpᵢ dpₖ   ,   …`

**中文旁白**：換句話說，相流就像不可壓縮的流體。用同樣的辦法還可以證明二維、四維等等的積分也都不變，這些量叫做龐加萊積分不變量。

**English**: In other words the phase flow behaves like an incompressible fluid. The same argument shows that integrals over manifolds of two, four and more dimensions are invariant as well, and these are the Poincare integral invariants.

**動畫**：方塊繼續被扯成細絲，面積依然不變——相流就像不可壓縮的流體。

---
