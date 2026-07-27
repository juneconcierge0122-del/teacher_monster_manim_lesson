# 第 41 課｜勞斯函數：一半哈密頓，一半拉格朗日（Landau §41）

Lesson 41 — The Routhian: half Hamiltonian, half Lagrangian

- 場景檔：`manim_lessons/lessons/landau_l41_routhian.py`（`LandauL41ZH` / `LandauL41EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[41]` 與 `FORMULAS[41]`
- 配音：`manim_lessons/samples/audio_l41/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 23 秒、英文約 2 分 17 秒

前半是一張對照圖：左邊的 (q, p) 換成了動量、右邊的 (ξ, v) 保留速度，所以勞斯函數對左邊像哈密頓量、對右邊像拉格朗日量。後半換成中心力場——角度是循環座標，它的動量凍結成常數，剩下的就是有效位能裡的一維徑向運動。

---

## 第 0 拍｜只換掉一部分的速度

**畫面公式**：只換掉一部分的速度　/　replace only some of the velocities　/　`( q , q̇ , ξ , v )     ⟶     ( q , p , ξ , v )        v = dξ/dt`

**中文旁白**：有時候換變數時，我們只想把一部分的廣義速度換成動量，另一部分維持原樣。做法和上一課完全一樣，只是做一半。

**English**: Sometimes, in changing variables, we want to replace only some of the generalised velocities by momenta and leave the rest alone. The transformation is exactly the one of the last lesson, carried out only half way.

**動畫**：左右對照：左邊的 (q, p) 換成動量，右邊的 (ξ, v) 保留速度。

---

## 第 1 拍｜一個座標要換，一個保持不變

**畫面公式**：一個座標要換，一個保持不變　/　one coordinate transformed, one left alone　/　`dL = ṗ dq + p dq̇ + ( ∂L/∂ξ ) dξ + ( ∂L/∂v ) dv`

**中文旁白**：為了式子簡單，先假設只有兩個座標：一個叫 q，要換掉；另一個叫 ξ，保持不變。照樣先寫下拉格朗日量的全微分，四項各對應一個變數。

**English**: To keep the formulas short, suppose there are just two coordinates: one called q, which we will transform, and one called xi, which stays. Write the total differential of the Lagrangian, one term for each of the four variables.

**動畫**：同一張對照圖，寫出四個變數的全微分。

---

## 第 2 拍｜把含速度微分的那一項移過去

**畫面公式**：把含速度微分的那一項移過去　/　move the velocity differential across　/　`d ( L − p q̇ ) = ṗ dq − q̇ dp + ( ∂L/∂ξ ) dξ + ( ∂L/∂v ) dv`

**中文旁白**：用動量的定義和拉格朗日方程，把前兩項換掉，再把含速度微分的那一項移過去，就得到一個新的量的全微分。

**English**: Use the definition of the momentum and Lagrange's equation on the first two terms, then move the term carrying the velocity differential across, and the result is the total differential of a new quantity.

**動畫**：同一張對照圖，把含 dq̇ 的那一項移到左邊。

---

## 第 3 拍｜勞斯函數

**畫面公式**：勞斯函數　/　the Routhian　/　`R ( q , p , ξ , v ) = p q̇ − L`

**中文旁白**：這個量就叫勞斯函數：動量乘上要換掉的那個速度，再減去拉格朗日量；其中的速度要用動量表示出來。

**English**: That quantity is the Routhian: the momentum times the velocity being replaced, minus the Lagrangian, with the velocity itself written in terms of the momentum.

**動畫**：同一張對照圖，定義出勞斯函數 R = p q̇ − L。

---

## 第 4 拍｜對 q 與 p：哈密頓方程的形式

**畫面公式**：對 q 與 p：哈密頓方程的形式　/　for q and p: Hamilton's equations　/　`q̇ = ∂R/∂p        ṗ = − ∂R/∂q`

**中文旁白**：從它的全微分讀出係數，對 q 和 p 這一組，得到的正是哈密頓方程的形式：速度等於勞斯函數對動量的偏導數，動量的變化率等於對座標的偏導數取負號。

**English**: Reading the coefficients off its differential, the q and p pair behaves exactly as in Hamilton's equations: the velocity is the derivative of the Routhian by the momentum, and the rate of change of the momentum is minus its derivative by the coordinate.

**動畫**：左半出現兩條哈密頓形式的方程。

---

## 第 5 拍｜對 ξ：拉格朗日方程的形式

**畫面公式**：對 ξ：拉格朗日方程的形式　/　for xi: Lagrange's equation　/　`d/dt ( ∂R/∂v ) = ∂R/∂ξ            v = dξ/dt`

**中文旁白**：對另一組就不一樣了。勞斯函數對 ξ 和它的速度的偏導數，剛好是拉格朗日量對應偏導數的負值；代進拉格朗日方程，形式完全沒變。所以勞斯函數對 q 是哈密頓量，對 ξ 是拉格朗日量。

**English**: The other pair behaves differently. The derivatives of the Routhian with respect to xi and its velocity are minus the corresponding derivatives of the Lagrangian, so Lagrange's equation for xi keeps its form. The Routhian is a Hamiltonian in q and a Lagrangian in xi.

**動畫**：右半出現一條拉格朗日形式的方程。

---

## 第 6 拍｜能量也可以用它寫出來

**畫面公式**：能量也可以用它寫出來　/　the energy, written with it　/　`E = R − v ( ∂R/∂v )`

**中文旁白**：系統的能量也可以用它寫出來：能量等於勞斯函數，減去 ξ 的速度乘上勞斯函數對這個速度的偏導數。

**English**: The energy can be written with it too: the energy is the Routhian minus the velocity of xi times the derivative of the Routhian with respect to that velocity.

**動畫**：兩邊都在，右側寫出用 R 表示的能量。

---

## 第 7 拍｜真正的用處：循環座標

**畫面公式**：真正的用處：循環座標　/　where it earns its keep: cyclic coordinates　/　`q cyclic     ⟹     R = R ( p , ξ , v )`

**中文旁白**：勞斯函數最有用的場合，是有循環座標的時候。循環座標根本不出現在拉格朗日量裡，因此也不出現在勞斯函數裡，勞斯函數只依賴動量、剩下的座標和它的速度。

**English**: The Routhian earns its keep when some coordinates are cyclic. A cyclic coordinate does not appear in the Lagrangian, and therefore not in the Routhian either, which then depends only on the momentum, the remaining coordinate and its velocity.

**動畫**：換成中心力場：質點沿橢圓軌道運行，紅色圓弧標出角度 φ，紫色線段是半徑 r。

---

## 第 8 拍｜循環座標的動量是常數

**畫面公式**：循環座標的動量是常數　/　the momentum of a cyclic coordinate is constant　/　`p = const`

**中文旁白**：而循環座標對應的動量是常數。把這個常數值代進去之後，剩下的方程就只含剩下的座標了——循環座標被完全消掉，自由度真的少了一個。

**English**: And the momentum belonging to a cyclic coordinate is a constant. Once that constant value is put in, the remaining equations contain only the remaining coordinates: the cyclic coordinate has been eliminated completely.

**動畫**：右邊多出有效位能曲線 U_eff(r)，上面的點跟著真實軌道的半徑上下移動。

---

## 第 9 拍｜循環座標被完全消掉

**畫面公式**：循環座標被完全消掉　/　the cyclic coordinate is gone　/　`ξ ( t )     ⟶     q̇ = ∂R/∂p     ⟶     q ( t )`

**中文旁白**：解出剩下座標隨時間的變化，再把它代回速度等於勞斯函數對動量的偏導數那條式子，循環座標就能直接積分出來。中心力場就是最典型的例子：角度是循環的，角動量守恆，剩下的只是一維的徑向運動。

**English**: Solve those for the remaining coordinate, and the cyclic one then follows by direct integration. A central field is the classic case: the angle is cyclic, its momentum is the conserved angular momentum, and only radial motion is left.

**動畫**：同一組圖：解出 r(t) 之後再積分就得到 φ(t)。

---
