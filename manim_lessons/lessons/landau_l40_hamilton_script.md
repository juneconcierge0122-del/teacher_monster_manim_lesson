# 第 40 課｜哈密頓方程：把速度換成動量（Landau §40）

Lesson 40 — Hamilton's equations: trading velocities for momenta

- 場景檔：`manim_lessons/lessons/landau_l40_hamilton.py`（`LandauL40ZH` / `LandauL40EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[40]` 與 `FORMULAS[40]`
- 配音：`manim_lessons/samples/audio_l40/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 35 秒、英文約 2 分 27 秒

左邊是勒讓德變換的幾何意義：一條 L 對速度的曲線，切線的斜率是動量、截距是負的哈密頓量；右邊是相空間，等能量曲線加上處處給定方向的流場，說明 2s 條一階方程就是一個流。

---

## 第 0 拍｜換一組獨立變數

**畫面公式**：換一組獨立變數　/　a different pair of variables　/　`( q , dq/dt )     ⟶     ( q , p )`

**中文旁白**：用拉格朗日量來寫力學，前提是用廣義座標和廣義速度來描述系統的狀態。但這不是唯一的描述方式。改用廣義座標和廣義動量，在處理一般性問題時有不少好處；那麼運動方程會長什麼樣子？

**English**: Writing mechanics with the Lagrangian assumes the state of a system is given by its generalised coordinates and velocities. That is not the only choice. Describing it by coordinates and momenta has real advantages, so what do the equations of motion become?

**動畫**：左側是 (q, dq/dt) 與 (q, p) 的對照：s 個二階方程對上 2s 個一階方程。

---

## 第 1 拍｜勒讓德變換：從 L 的全微分出發

**畫面公式**：勒讓德變換：從 L 的全微分出發　/　Legendre: start from the differential of L　/　`dL = Σ ( ∂L/∂qᵢ ) dqᵢ + Σ ( ∂L/∂q̇ᵢ ) dq̇ᵢ`

**中文旁白**：從一組獨立變數換到另一組，用的是數學上所謂的勒讓德變換。先寫下拉格朗日量的全微分：每個座標的偏導數乘上座標的微分，加上每個速度的偏導數乘上速度的微分。

**English**: Passing from one set of independent variables to another is what mathematics calls a Legendre transformation. Start from the total differential of the Lagrangian: a term in each coordinate differential, and a term in each velocity differential.

**動畫**：同一張對照圖，從 L 的全微分出發。

---

## 第 2 拍｜用動量的定義與拉格朗日方程改寫

**畫面公式**：用動量的定義與拉格朗日方程改寫　/　rewrite it with p and Lagrange's equations　/　`pᵢ = ∂L/∂q̇ᵢ   ,   ṗᵢ = ∂L/∂qᵢ` ／ `dL = Σ ṗᵢ dqᵢ + Σ pᵢ dq̇ᵢ`

**中文旁白**：按定義，對速度的偏導數就是廣義動量；而由拉格朗日方程，對座標的偏導數就是那個動量的時間導數。所以全微分變成動量變化率乘座標微分，加上動量乘速度微分。

**English**: By definition the derivative with respect to a velocity is the generalised momentum, and by Lagrange's equations the derivative with respect to a coordinate is the rate of change of that momentum. So the differential becomes p-dot d q plus p d q-dot.

**動畫**：同一張對照圖，用動量的定義與拉格朗日方程改寫成 ṗ dq + p dq̇。

---

## 第 3 拍｜把速度的微分挪到左邊

**畫面公式**：把速度的微分挪到左邊　/　move the velocity differential across　/　`Σ pᵢ dq̇ᵢ = d ( Σ pᵢ q̇ᵢ ) − Σ q̇ᵢ dpᵢ`

**中文旁白**：關鍵的一步：把第二項寫成動量乘速度之和的微分，減去速度乘動量微分。把那個微分移到等號左邊，再把符號整個反過來，就出現一個新的微分關係。

**English**: Now the key step. Write the second group as the differential of the sum of p times q-dot, minus q-dot times d p. Move that differential to the left-hand side and reverse the signs, and a new differential relation appears.

**動畫**：同一張對照圖，把 Σ p dq̇ 寫成全微分減去 Σ q̇ dp。

---

## 第 4 拍｜哈密頓量：切線的截距

**畫面公式**：哈密頓量：切線的截距　/　the Hamiltonian: the intercept of the tangent　/　`H ( p , q , t ) = Σ pᵢ q̇ᵢ − L`

**中文旁白**：被微分的那個量，正是用座標和動量寫出來的能量，我們叫它哈密頓函數。從幾何上看這就是勒讓德變換：把切線的斜率當成新變數，切線的截距就是新的函數。

**English**: The quantity being differentiated is the energy of the system written in coordinates and momenta: the Hamiltonian. Geometrically this is the Legendre transform, taking the slope of the tangent as the new variable and the intercept as the new function.

**動畫**：勒讓德變換的幾何：L 對速度的曲線、一條切線，斜率標為 p，截距標為 −H。

---

## 第 5 拍｜獨立變數已經換成 q 與 p

**畫面公式**：獨立變數已經換成 q 與 p　/　the independent variables are now q and p　/　`dH = − Σ ṗᵢ dqᵢ + Σ q̇ᵢ dpᵢ`

**中文旁白**：新的關係式裡獨立變數已經換成座標和動量，所以直接讀出係數就行：速度等於哈密頓量對動量的偏導數，動量的變化率等於哈密頓量對座標的偏導數再取負號。

**English**: In the new relation the independent variables are the coordinates and the momenta, so we can read off the coefficients. The velocity is the derivative of the Hamiltonian by the momentum, and the rate of change of the momentum is minus its derivative by the coordinate.

**動畫**：換到相空間：q–p 平面上的等能量曲線。

---

## 第 6 拍｜哈密頓方程，又叫正則方程

**畫面公式**：哈密頓方程，又叫正則方程　/　Hamilton's equations, also called canonical　/　`dqᵢ/dt = ∂H/∂pᵢ        dpᵢ/dt = − ∂H/∂qᵢ`

**中文旁白**：這就是哈密頓方程。原本 s 條二階方程，現在換成 2s 條一階方程；因為形式簡潔又對稱，它們也叫做正則方程。

**English**: These are Hamilton's equations. The s second-order equations of the Lagrangian treatment are replaced by two s first-order ones, and because the pair is so simple and symmetric they are also called the canonical equations.

**動畫**：同一張相空間圖，從 dH 讀出兩條正則方程。

---

## 第 7 拍｜在相空間裡就是一個流

**畫面公式**：在相空間裡就是一個流　/　in phase space it is simply a flow　/　`s × 2nd order     ⟶     2s × 1st order`

**中文旁白**：它們在相空間裡有很漂亮的意義。相空間就是座標和動量張成的平面；平面上每一點的前進方向都由哈密頓量的偏導數決定，於是整個系統的演化就是一個流。

**English**: They have a lovely meaning in phase space, the plane spanned by the coordinate and the momentum. At every point the derivatives of the Hamiltonian fix the direction of travel, so the whole evolution of the system is a flow.

**動畫**：相空間裡加上流場箭頭：每一點都有一個方向，整個演化就是一個流。

---

## 第 8 拍｜中間兩項剛好抵消

**畫面公式**：中間兩項剛好抵消　/　the two middle terms cancel　/　`dH/dt = ∂H/∂t`

**中文旁白**：再看哈密頓量自己隨時間怎麼變。把它的全導數展開，再把正則方程代進去，中間兩項剛好完全抵消，只剩下對時間的偏導數。

**English**: Now look at how the Hamiltonian itself changes. Expand its total time derivative and substitute the canonical equations: the two middle terms cancel exactly, leaving only the partial derivative with respect to time.

**動畫**：代表點沿著等能量曲線移動，中間兩項互相抵消。

---

## 第 9 拍｜不顯含時間就守恆

**畫面公式**：不顯含時間就守恆　/　no explicit time, so it is conserved　/　`∂H/∂t = 0     ⟹     H = const`

**中文旁白**：所以只要哈密頓量不顯含時間，它就守恆，這正是能量守恆。在相空間裡看，代表系統的那個點會永遠待在同一條等能量曲線上。

**English**: So if the Hamiltonian does not contain the time explicitly, it is conserved, which is conservation of energy. In phase space the representative point stays for ever on one curve of constant energy.

**動畫**：同一張圖：H 不顯含時間時，代表點永遠留在同一條能量曲線上。

---
