# 第 47 課｜漢彌頓－雅可比方程：把力學變成一條偏微分方程（Landau §47）

Lesson 47 — The Hamilton-Jacobi equation: mechanics as one partial differential equation

- 場景檔：`manim_lessons/lessons/landau_l47_hamilton_jacobi.py`（`LandauL47ZH` / `LandauL47EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[47]` 與 `FORMULAS[47]`
- 配音：`manim_lessons/samples/audio_l47/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 9 秒、英文約 2 分 16 秒

中段給了它應得的畫面：左右兩個平面，左邊是普通的相平面，代表點沿著軌道跑；右邊是 (α, β) 平面，同一個運動在那裡是一個完全不動的點。這就是整套方法的內容——一個把運動變成常數的正則變換。最後一拍回到光學圖像，S 的等值面像波前一樣一層層推出去。

---

## 第 0 拍｜上一課的兩個結果

**畫面公式**：上一課的兩個結果　/　two results from the last lesson　/　`∂S/∂t + H = 0        ∂S/∂qᵢ = pᵢ`

**中文旁白**：上一課得到兩個結果：作用量對時間的偏導數加上哈密頓量等於零，而作用量對每個座標的偏導數就是對應的動量。

**English**: The last lesson gave two results: the derivative of the action with respect to time plus the Hamiltonian is zero, and the derivative of the action with respect to each coordinate is the corresponding momentum.

**動畫**：左邊的相平面上，代表點沿著軌道不停地跑。

---

## 第 1 拍｜把動量換成 S 的導數

**畫面公式**：把動量換成 S 的導數　/　replace each momentum by a derivative of S　/　`∂S/∂t + H ( q₁ … q_s ; ∂S/∂q₁ … ∂S/∂q_s ; t ) = 0`

**中文旁白**：把哈密頓量裡的動量全部換成作用量對座標的偏導數，就得到一條只含作用量本身的一階偏微分方程。這就是漢彌頓－雅可比方程。

**English**: Replacing every momentum in the Hamiltonian by the derivative of the action with respect to that coordinate gives a first-order partial differential equation containing only the action itself. This is the Hamilton-Jacobi equation.

**動畫**：同一張圖，右側寫出只含 S 的一階偏微分方程。

---

## 第 2 拍｜一整套積分方法的出發點

**畫面公式**：一整套積分方法的出發點　/　the basis of a general method　/　`S = S ( q , t )`

**中文旁白**：它和拉格朗日方程、正則方程一樣，是一整套積分運動方程的方法的出發點。

**English**: Like Lagrange's equations and the canonical equations, it is the starting point of a general method for integrating the equations of motion.

**動畫**：同一張圖：它和拉格朗日方程、正則方程並列。

---

## 第 3 拍｜要的是完全積分

**畫面公式**：要的是完全積分　/　what we want is a complete integral　/　`S = f ( t , q ; α₁ … α_s ) + A`

**中文旁白**：一階偏微分方程有個含任意函數的通解，但在力學裡我們要的不是它，而是完全積分：含有和獨立變數一樣多的獨立任意常數。

**English**: A first-order partial differential equation has a general integral depending on an arbitrary function, but in mechanics what we want is a complete integral: one carrying as many independent arbitrary constants as there are independent variables.

**動畫**：同一張圖：我們要的是含 s + 1 個常數的完全積分。

---

## 第 4 拍｜把它當成生成函數

**畫面公式**：把它當成生成函數　/　take it as a generating function　/　`f ( t , q ; α )  as generating function        Pᵢ = αᵢ`

**中文旁白**：獨立變數是時間和 s 個座標，所以完全積分要有 s 加一個常數；而作用量只以導數的形式出現，所以其中一個必定是相加的常數。

**English**: The independent variables are the time and the s coordinates, so a complete integral needs s plus one constants; and since the action enters only through its derivatives, one of them must be simply additive.

**動畫**：右邊出現第二個平面 (α, β)：同一個運動在那裡是一個完全不動的點，中間用箭頭連起來。

---

## 第 5 拍｜新的哈密頓量等於零

**畫面公式**：新的哈密頓量等於零　/　the new Hamiltonian vanishes　/　`H′ = H + ∂f/∂t = 0`

**中文旁白**：關鍵的一步是：把完全積分當成生成函數，把那 s 個任意常數當成新的動量，做一次正則變換。

**English**: Here is the key step. Take the complete integral as a generating function and the s arbitrary constants as the new momenta, and carry out one canonical transformation.

**動畫**：兩個平面並列，右側指出新的哈密頓量等於零。

---

## 第 6 拍｜所有新變數都是常數

**畫面公式**：所有新變數都是常數　/　so every new variable is a constant　/　`dαᵢ/dt = 0   ,   dβᵢ/dt = 0`

**中文旁白**：因為這個函數滿足漢彌頓－雅可比方程，新的哈密頓量正好等於零。哈密頓量為零，正則方程就說：新的座標和新的動量全都是常數。

**English**: Because that function satisfies the Hamilton-Jacobi equation, the new Hamiltonian is exactly zero. With a vanishing Hamiltonian the canonical equations say that all the new coordinates and momenta are constants.

**動畫**：兩個平面並列：H′ = 0，所以 α 與 β 全是常數。

---

## 第 7 拍｜解出座標隨時間的變化

**畫面公式**：解出座標隨時間的變化　/　solve for the coordinates in time　/　`∂f/∂αᵢ = βᵢ        pᵢ = ∂S/∂qᵢ`

**中文旁白**：於是把完全積分對每個常數求偏導數，令它等於另一個常數，就得到 s 條代數方程，把座標表示成時間和二倍 s 個常數的函數——這正是運動方程的通解。動量再由作用量對座標的偏導數得到。

**English**: So differentiating the complete integral by each constant and setting the result equal to a new constant gives s algebraic equations, expressing the coordinates through the time and two s constants. That is the general integral, and the momenta follow from the action.

**動畫**：兩個平面並列：∂f/∂αᵢ = βᵢ 這 s 條代數方程解出 q(t)。

---

## 第 8 拍｜系統保守時方程更簡單：時

**畫面公式**：`S = S₀ ( q ) − E t` ／ `H ( q₁ … q_s ; ∂S₀/∂q₁ … ∂S₀/∂q_s ) = E`

**中文旁白**：系統保守時方程更簡單：時間只以減去能量乘時間的形式出現，代進去就得到只含座標的方程，也就是簡略作用量滿足的漢彌頓－雅可比方程。

**English**: For a conservative system the equation is simpler: the time enters only as minus the energy times the time, and substituting leaves an equation in the coordinates alone, the Hamilton-Jacobi equation for the abbreviated action.

**動畫**：兩個平面並列：保守系統時 S = S₀ − E t。

---

## 第 9 拍｜等值面是波前，動量是光線

**畫面公式**：等值面是波前，動量是光線　/　level surfaces are wavefronts, momenta are rays　/　`S = const :  wavefronts        p = ∇S :  rays`

**中文旁白**：這條方程的幾何意義很漂亮：作用量的等值面就是波前，動量處處垂直於它們，質點的運動就像波前一層層往外傳。力學與光學在這裡真正合而為一。

**English**: The geometry behind it is lovely: the level surfaces of the action are wavefronts, the momenta stand perpendicular to them everywhere, and the motion of the particle is the advance of those wavefronts. Here mechanics and optics genuinely become one subject.

**動畫**：換成波前圖：青色的等值面一層層向外推進，紅色的光線垂直穿過它們。

---
