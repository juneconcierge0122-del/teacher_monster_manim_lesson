# 第 39 課｜非慣性參考系：慣性力從哪裡來（Landau §39）

Lesson 39 — A non-inertial frame: where the inertia forces come from

- 場景檔：`manim_lessons/lessons/landau_l39_noninertial.py`（`LandauL39ZH` / `LandauL39EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[39]` 與 `FORMULAS[39]`
- 配音：`manim_lessons/samples/audio_l39/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 44 秒、英文約 2 分 38 秒

兩個實驗撐起這一課。先是加速車廂裡的擺，它沿著 g 減 W 的方向掛著，這正是慣性力等效於均勻力場的意思；再來是轉盤上的冰球，同一段運動畫兩次——慣性系裡是直線，轉動系裡是彎的，而彎曲的那條是把直線做座標變換得到的，不是硬畫上去的。

---

## 第 0 拍｜到目前為止都在慣性系裡

**畫面公式**：到目前為止都在慣性系裡　/　so far, always an inertial frame　/　`L₀ = ½ m v₀² − U`

**中文旁白**：到目前為止我們都在慣性系裡討論。單一質點在外場中的拉格朗日量是二分之一質量乘速度平方減去位能，由它導出的運動方程也只在慣性系裡成立。

**English**: Everything so far has been done in inertial frames: for one particle in an external field the Lagrangian is one-half m v-squared minus the potential energy, and the equation of motion that follows from it holds only in such a frame.

**動畫**：慣性系 K₀ 的兩根座標軸，一個質點以等速向右移動。

---

## 第 1 拍｜最小作用量原理不在乎座標系

**畫面公式**：最小作用量原理不在乎座標系　/　least action does not care about the frame　/　`d/dt ( ∂L/∂v ) = ∂L/∂r`

**中文旁白**：那在非慣性系裡會變成什麼樣？最小作用量原理並不在乎我們選哪個參考系，拉格朗日方程也照樣成立；要改的只有拉格朗日量本身，而我們分兩步來做。

**English**: What happens in a non-inertial frame? The principle of least action does not care which frame we choose, and Lagrange's equations still hold. Only the Lagrangian itself has to be transformed, and we do that in two steps.

**動畫**：同一張圖：最小作用量原理與座標系無關，只有 L 本身要改寫。

---

## 第 2 拍｜第一步：平移的參考系

**畫面公式**：第一步：平移的參考系　/　step one: a translating frame　/　`v₀ = v′ + V(t)` ／ `L′ = ½ m v′² + m v′ · V + ½ m V² − U`

**中文旁白**：第一步，取一個相對於慣性系以速度 V(t) 平移的參考系。兩個速度差一個 V，代進拉格朗日量後得到二分之一質量乘新速度平方，加上質量乘新速度點乘 V，再加二分之一質量乘 V 平方，最後減去位能。

**English**: First take a frame translating with velocity V of t relative to the inertial one. The two velocities differ by V, so substituting into the Lagrangian gives one-half m v-primed-squared, plus m v-primed dotted into V, plus one-half m V-squared, minus U.

**動畫**：一輛以 W 加速的車廂，車頂懸著一根擺，虛線標出鉛直方向。

---

## 第 3 拍｜全微分可以直接丟掉

**畫面公式**：全微分可以直接丟掉　/　total derivatives may simply be dropped　/　`½ m V² = d( … )/dt        m V · v′ = d( m V · r′ )/dt − m r′ · dV/dt`

**中文旁白**：V 平方那一項只是時間的已知函數，是個全微分，可以丟掉。中間那一項也能拆成一個全微分，加上一項含有參考系加速度的東西；把全微分丟掉之後就乾淨了。

**English**: The V-squared term is a given function of time, a total derivative, so it can be dropped. The middle term also splits into a total derivative plus a piece carrying the acceleration of the frame, and dropping that derivative leaves a clean Lagrangian.

**動畫**：同一個車廂：½ m V² 與全微分項都可以丟掉。

---

## 第 4 拍｜加速度等效於一個均勻力場

**畫面公式**：加速度等效於一個均勻力場　/　acceleration acts like a uniform force field　/　`L′ = ½ m v′² − m W(t) · r′ − U          W = dV/dt`

**中文旁白**：剩下的就是自由拉格朗日量，減去質量乘參考系加速度點乘位置，再減位能。所以平移加速度的效果，恰好等於加上一個均勻力場，大小是質量乘加速度，方向與加速度相反。

**English**: What is left is the free Lagrangian minus m times the frame acceleration dotted into the position, minus U. So an accelerated translation acts exactly like a uniform field of force, equal to the mass times the acceleration and pointing the opposite way.

**動畫**：擺沿著 g 減 W 的合成方向傾斜，青色的 g 與紅色的 −W 用虛線補成平行四邊形。

---

## 第 5 拍｜第二步：轉動的參考系

**畫面公式**：第二步：轉動的參考系　/　step two: a rotating frame　/　`v′ = v + Ω × r` ／ `L = ½ m v² + m v · ( Ω × r ) + ½ m ( Ω × r )² − m W · r − U`

**中文旁白**：接著再加一個原點相同、但以角速度 Ω 轉動的參考系。平移系裡的速度，等於轉動系裡的速度加上 Ω 與位置的叉積；代進去就得到適用於任意參考系的拉格朗日量。

**English**: Now add a second frame with the same origin, rotating with angular velocity Omega. The velocity in the translating frame is the velocity in the rotating one plus Omega crossed with the position, and substituting gives the general Lagrangian for any frame at all.

**動畫**：換成轉動的參考系：以 Ω 轉動的圓盤，位置向量 r 隨時間轉動，紅色的 Ω × r 始終與它垂直。

---

## 第 6 拍｜多出一項與速度成一次的項

**畫面公式**：多出一項與速度成一次的項　/　a term linear in the velocity appears　/　`∂L/∂v = m v + m Ω × r`

**中文旁白**：注意轉動帶來了什麼：多出一項與粒子速度成一次的項，這是我們之前寫過的拉格朗日量裡從來沒有的。把它要求的導數算出來代進拉格朗日方程，就得到運動方程。

**English**: Notice what the rotation did: it added a term linear in the velocity of the particle, which no Lagrangian we have written before contained. Taking the derivatives it calls for and putting them into Lagrange's equation gives the equation of motion.

**動畫**：同一張轉動圖，強調多出來的 m v · (Ω × r) 是與速度成一次的項。

---

## 第 7 拍｜三個慣性力

**畫面公式**：三個慣性力　/　three inertia forces　/　`m dv/dt = − ∂U/∂r − m W + m r × dΩ/dt + 2 m v × Ω + m Ω × ( r × Ω )`

**中文旁白**：結果出現三個慣性力。第一個是質量乘位置與角速度變化率的叉積，只有在轉動不均勻時才存在；另外兩個即使等速轉動也還在。

**English**: Three inertia forces appear. The first is m r crossed with the rate of change of Omega, and it is there only because the rotation is not uniform. The other two survive even for a perfectly steady rotation.

**動畫**：同一張轉動圖，右側逐條列出三個慣性力。

---

## 第 8 拍｜科氏力：直線看起來會彎

**畫面公式**：科氏力：直線看起來會彎　/　Coriolis: a straight line looks curved　/　`2 m v × Ω`

**中文旁白**：第二個是二倍質量乘速度與角速度的叉積，叫做科氏力。和之前所有的非耗散力都不同，它依賴粒子的速度：在慣性系裡走直線的東西，在轉動系裡看起來會彎掉。

**English**: The second is twice m v crossed with Omega, the Coriolis force. Unlike every other non-dissipative force so far, it depends on the velocity of the particle: something moving in a straight line in the inertial frame curves away in the rotating one.

**動畫**：轉盤上的冰球，左右兩個視角：慣性系裡是直線（青色），轉動系裡是彎的（紅色），兩者是同一段運動。

---

## 第 9 拍｜離心力：背離轉軸

**畫面公式**：離心力：背離轉軸　/　centrifugal: straight away from the axis　/　`m Ω × ( r × Ω )          | F | = m ρ Ω²`

**中文旁白**：第三個是質量乘角速度與位置和角速度的雙重叉積，叫做離心力。它位於位置與角速度張成的平面內，方向直接背離轉軸，大小是質量乘上到轉軸的距離再乘角速度平方。

**English**: The third is m Omega crossed with r crossed with Omega, the centrifugal force. It lies in the plane of r and Omega, points straight away from the axis of rotation, and its magnitude is m times the distance from that axis times Omega squared.

**動畫**：轉軸與位置向量張成的平面，ρ 是到軸的距離，紅色箭頭是背離軸的離心力 m ρ Ω²。

---
