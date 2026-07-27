# 第 43 課｜作用量作為座標的函數（Landau §43）

Lesson 43 — The action as a function of the coordinates

- 場景檔：`manim_lessons/lessons/landau_l43_action_of_q.py`（`LandauL43ZH` / `LandauL43EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[43]` 與 `FORMULAS[43]`
- 配音：`manim_lessons/samples/audio_l43/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 20 秒、英文約 2 分 15 秒

三張圖。先是同一起點出發、終點散開的一族真實路徑，作用量因此成為終點座標的函數；再來是 (43.3) 真正的意思——作用量的等值面畫成波前，動量就是垂直於它們的光線；最後是一張 q–t 圖：同一個位置、不同抵達時刻的世界線，作用量沿線累積，以及 (43.6) 的兩個微分——固定 q 走一步 t，固定 t 走一步 q。

---

## 第 0 拍｜兩個端點都固定

**畫面公式**：兩個端點都固定　/　both endpoints held fixed　/　`S = ∫ L dt        q(t₁) = q⁽¹⁾ ,   q(t₂) = q⁽²⁾`

**中文旁白**：當初講最小作用量原理時，我們把作用量看成沿著一條路徑的積分，兩個端點的位置和時刻都是給定的；在所有這些路徑裡，真實運動走的那一條讓積分最小。

**English**: When we set up the principle of least action, the action was an integral along a path whose two endpoints were both fixed in position and in time. Among all those paths, the true motion is the one that makes the integral least.

**動畫**：一條青色的真實路徑，兩個端點都固定。

---

## 第 1 拍｜改讓終點自由跑

**畫面公式**：改讓終點自由跑　/　now let the far end move　/　`S = S ( q , t )`

**中文旁白**：現在換一個角度看作用量。固定起點不動，但讓終點跑到不同的位置去。於是作用量變成終點座標的函數，而且我們只沿著真實的運動路徑來算它。

**English**: Now look at the action differently. Keep the starting point fixed but let the far end move to different places. The action then becomes a function of the final coordinates, evaluated always along the true path of the motion.

**動畫**：同一個起點散開成一族紫色路徑，終點落在不同位置——作用量成為終點座標的函數。

---

## 第 2 拍｜真實路徑讓積分項消失

**畫面公式**：真實路徑讓積分項消失　/　on the true path the integral drops out　/　`δS = [ ( ∂L/∂q̇ ) δq ]  +  ∫ [ ∂L/∂q − d/dt ( ∂L/∂q̇ ) ] δq dt`

**中文旁白**：把作用量做變分，會得到兩部分：一個邊界項，加上一個積分。因為真實路徑滿足拉格朗日方程，那個積分恆等於零。

**English**: Varying the action produces two pieces: a boundary term and an integral. Because the true path satisfies Lagrange's equations, that integral vanishes identically.

**動畫**：同一族路徑，變分拆成邊界項與積分項。

---

## 第 3 拍｜只剩下邊界項

**畫面公式**：只剩下邊界項　/　only the boundary term survives　/　`δS = Σ pᵢ δqᵢ`

**中文旁白**：起點固定，所以起點的變分是零；剩下的邊界項就是動量乘上終點的變分。對多個自由度也一樣，每個座標配上它自己的動量。

**English**: The start is fixed, so its variation is zero, and the boundary term that survives is the momentum times the variation of the endpoint. With several degrees of freedom each coordinate carries its own momentum.

**動畫**：同一族路徑：起點的變分為零，只剩下邊界項。

---

## 第 4 拍｜動量就是作用量的梯度

**畫面公式**：動量就是作用量的梯度　/　momentum is the gradient of the action　/　`∂S/∂qᵢ = pᵢ            p = ∇S`

**中文旁白**：由此得到一個漂亮的結論：作用量對座標的偏導數，就等於對應的動量。換句話說，動量是作用量的梯度。在位形空間裡畫出作用量的等值面，動量就處處垂直於它們——就像光學裡的波前與光線。

**English**: That gives a beautiful result: the derivative of the action with respect to a coordinate is the corresponding momentum, so momentum is the gradient of the action. Draw the level surfaces of the action and the momenta stand perpendicular to them, like wavefronts and rays in optics.

**動畫**：換成波前圖：青色的等值面一層層向外，紅色的光線垂直穿過它們——動量就是作用量的梯度。

---

## 第 5 拍｜也讓抵達的時刻變動

**畫面公式**：也讓抵達的時刻變動　/　now let the arrival time vary too　/　`S = S ( q , t )`

**中文旁白**：同樣地，也可以讓終點的時刻變動：起點與終點的位置都固定，但抵達的時刻不同，這樣作用量又成了時間的函數。

**English**: In the same way we can let the arrival time vary: both endpoints fixed in place, but reached at different instants, which makes the action a function of the time as well.

**動畫**：換成 q–t 圖：三條世界線從同一起點出發，抵達同一個 q，但時刻不同（虛線標出 q 固定）。

---

## 第 6 拍｜沿著路徑，dS/dt 就是 L

**畫面公式**：沿著路徑，dS/dt 就是 L　/　along the path, dS/dt is just L　/　`dS/dt = L`

**中文旁白**：要算它對時間的偏導數，最簡單的辦法是這樣：按定義，沿著路徑走，作用量的全時間導數就等於拉格朗日量。

**English**: To find its partial derivative with respect to time, the shortest route is this: by the very definition of the action, its total time derivative along the path is just the Lagrangian.

**動畫**：一個點沿著中間那條世界線往上走，青色的粗線在後面累積出來——這就是 S 沿路的累積。

---

## 第 7 拍｜另一邊用鏈鎖法則展開

**畫面公式**：另一邊用鏈鎖法則展開　/　expand the same derivative by the chain rule　/　`dS/dt = ∂S/∂t + Σ ( ∂S/∂qᵢ ) q̇ᵢ = ∂S/∂t + Σ pᵢ q̇ᵢ`

**中文旁白**：另一方面，把作用量看成座標與時間的函數，全導數等於對時間的偏導數，加上對每個座標的偏導數乘上速度；而剛才已經知道那些偏導數就是動量。

**English**: On the other hand, treating the action as a function of coordinates and time, the total derivative is the partial one plus the derivative with respect to each coordinate times the velocity, and we already know those derivatives are the momenta.

**動畫**：同一張 q–t 圖，把全導數用鏈鎖法則展開。

---

## 第 8 拍｜兩邊比較

**畫面公式**：兩邊比較　/　compare the two　/　`∂S/∂t = L − Σ pᵢ q̇ᵢ = − H`

**中文旁白**：兩邊一比較，就得到作用量對時間的偏導數，等於拉格朗日量減去動量乘速度的總和——那正好是哈密頓量的負值。

**English**: Comparing the two expressions, the partial derivative of the action with respect to time equals the Lagrangian minus the sum of momentum times velocity, and that is precisely minus the Hamiltonian.

**動畫**：在抵達事件上豎起一支紅色箭頭：固定 q 而讓時刻變動，作用量的改變是 −H dt。

---

## 第 9 拍｜作用量的全微分

**畫面公式**：作用量的全微分　/　the total differential of the action　/　`dS = Σ pᵢ dqᵢ − H dt`

**中文旁白**：把兩個結果合起來，作用量的全微分就是：動量乘座標的微分加總，再減去哈密頓量乘時間的微分。作用量因此成了一座橋：它對座標的梯度是動量，對時間的導數是負的能量。

**English**: Putting both results together, the total differential of the action is the sum of momentum times the coordinate differential, minus the Hamiltonian times the time differential. The action is a bridge: its gradient is momentum, its time derivative minus the energy.

**動畫**：再加上一支水平的青色箭頭：固定時刻而讓位置變動，作用量的改變是 +p dq。

---
