# 第 52 課｜條件週期運動：軌道永遠不閉合，卻無限接近（Landau §52）

Lesson 52 — Conditionally periodic motion: never closing, yet passing arbitrarily close

- 場景檔：`manim_lessons/lessons/landau_l52_conditional.py`（`LandauL52ZH` / `LandauL52EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[52]` 與 `FORMULAS[52]`
- 配音：`manim_lessons/samples/audio_l52/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 39 秒、英文約 2 分 42 秒

這一節唯一難的主張是：運動永遠不重複，卻會任意接近每一個狀態。而這其實是一張圖的主張——兩個角變數張成的正方形，左右與上下都接起來。一條斜率為無理數的直線一拍一拍地畫下去，始終不閉合，卻慢慢把整個正方形塗黑。把頻率比換成小整數比，它立刻閉合，這就是簡併；最後兩拍給簡併一個真實的例子：閉合的克卜勒橢圓，以及跟著它的那個多出來的守恆向量。

---

## 第 0 拍｜變數完全分離

**畫面公式**：變數完全分離　/　the variables separate completely　/　`S₀ = Σᵢ Sᵢ ( qᵢ )`

**中文旁白**：現在看任意多個自由度的系統，運動在每個座標上都是有限的，而且變數在漢彌頓－雅可比方程裡可以完全分離。簡略作用量就是每個座標各一項的和。

**English**: Take a system with any number of degrees of freedom, moving finitely in every coordinate, whose variables separate completely in the Hamilton-Jacobi treatment. The abbreviated action is then a sum of one function per coordinate.

**動畫**：兩個小小的封閉相軌跡並排，各自對應一個座標與它的動量。

---

## 第 1 拍｜每個座標一個作用變數

**畫面公式**：每個座標一個作用變數　/　one action variable per coordinate　/　`Sᵢ = ∫ pᵢ dqᵢ        Δᵢ S₀ = 2π Iᵢ        Iᵢ = ∮ pᵢ dqᵢ / 2π`

**中文旁白**：每一項都是那個座標的動量的積分，而且是多值的。座標在有限的範圍裡來回走一趟，作用量就增加二π乘上一個量；這樣就定義出 s 個作用變數。

**English**: Each is an integral of that momentum, and each is many-valued. When the coordinate runs there and back over its finite range, the action increases by two pi times a certain quantity, and that defines one action variable per degree of freedom.

**動畫**：兩塊面積各自標上 I₁ 與 I₂：每個自由度一個作用變數。

---

## 第 2 拍｜作用變數與角變數

**畫面公式**：作用變數與角變數　/　action variables and angle variables　/　`Iᵢ = const          wᵢ = [ ∂E ( I ) / ∂Iᵢ ] t + const`

**中文旁白**：接著做和單自由度時一樣的正則變換：作用變數與角變數。運動方程給出：每個作用變數都是常數，每個角變數都是自己的頻率乘時間再加常數。

**English**: Now make the same canonical transformation as for one degree of freedom: action variables and angle variables. The equations of motion say every action variable is constant, and every angle variable is its own frequency times the time plus a constant.

**動畫**：換成 w₁、w₂ 張成的正方形，一個點沿著固定斜率的直線走，走出邊界就從另一邊回來。

---

## 第 3 拍｜來回一趟只加 2π

**畫面公式**：來回一趟只加 2π　/　there and back adds just two pi　/　`Δᵢ wₖ = 2π δᵢₖ`

**中文旁白**：第 i 個座標來回一趟，只讓第 i 個角變數增加二π。所以任何座標與動量的單值函數，改用正則變數寫出來，就是每個角變數的週期函數，週期都是二π。

**English**: A there-and-back of one coordinate raises only its own angle variable, and by two pi. So any one-valued function of the coordinates and momenta, written in canonical variables, is periodic in every angle variable with period two pi.

**動畫**：直線一段一段累積：第 i 個座標來回一趟，只讓第 i 個角變數增加 2π。

---

## 第 4 拍｜多重傅立葉級數

**畫面公式**：多重傅立葉級數　/　a multiple Fourier series　/　`F = Σ A ( l₁ … l_s ) · exp [ i t ( l₁ ω₁ + … + l_s ω_s ) ]        ωₖ = ∂E/∂Iₖ`

**中文旁白**：把它展成多重傅立葉級數，再把角變數代成時間的線性函數，就會看到：時間依賴是一堆項的和，每一項的頻率是各個基本頻率的整數倍相加。

**English**: Expand it as a multiple Fourier series and put in the angle variables as linear functions of time. The time dependence is then a sum of terms, each with a frequency built from integer multiples of the fundamental frequencies added together.

**動畫**：軌跡越畫越密，卻沒有一段重疊。

---

## 第 5 拍｜頻率一般不可公度

**畫面公式**：頻率一般不可公度　/　the frequencies are incommensurable　/　`l₁ ω₁ + … + l_s ω_s        ω₁ : ω₂  ≠  n₁ : n₂`

**中文旁白**：這些頻率一般不可公度，所以整個和並不是週期函數，座標與動量也不是。也就是說，這種運動不論就整體或就任何單一座標而言，都不是嚴格週期的。

**English**: These frequencies are in general incommensurable, so the sum is not a periodic function, and neither are the coordinates and momenta. The motion is not strictly periodic, either as a whole or in any single coordinate.

**動畫**：正方形已經被畫線填滿大半，仍然找不到閉合的地方。

---

## 第 6 拍｜永遠不回來，卻無限接近

**畫面公式**：永遠不回來，卻無限接近　/　never returning, yet passing arbitrarily close　/　`q ( t + T ) ≠ q ( t )   ,   ∀ T        | Δq | , | Δp |   →   0`

**中文旁白**：系統經過某個狀態以後，不會在有限時間內再回到那個狀態；但只要時間夠長，它會任意接近那個狀態。這樣的運動就叫條件週期運動。

**English**: Having passed through a given state, the system does not return to that state in any finite time. But in the course of a long enough time it passes arbitrarily close to it. A motion of this kind is called conditionally periodic.

**動畫**：線條幾乎塗滿整個正方形：永遠不回到原點，卻任意接近每一點。

---

## 第 7 拍｜可公度就是簡併

**畫面公式**：可公度就是簡併　/　commensurable means degenerate　/　`n₁ ω₁ = n₂ ω₂     ⟹     E = E ( n₂ I₁ + n₁ I₂ , … )`

**中文旁白**：如果有幾個基本頻率彼此可公度，就叫簡併；若 s 個全部可公度，就是完全簡併，這時運動是週期的，軌道閉合。簡併還會減少能量真正依賴的獨立作用變數個數。

**English**: If several fundamental frequencies are commensurable, the motion is degenerate; if all of them are, it is completely degenerate, the motion is periodic and every path closes. Degeneracy also cuts down the number of independent action variables the energy depends on.

**動畫**：頻率比切成 3 比 2，同一條線立刻閉合成幾條平行線，之後只是重描。

---

## 第 8 拍｜簡併帶來更多單值積分

**畫面公式**：簡併帶來更多單值積分　/　degeneracy brings more one-valued integrals　/　`wᵢ/ωᵢ − wₖ/ωₖ = const        cos ( n₂ w₁ − n₁ w₂ ) = const`

**中文旁白**：簡併還有一個重要後果：單值的運動積分變多。沒有簡併時只有 s 個積分是單值的，其餘要寫成角變數除以頻率的差，並不單值。有簡併時，某個角變數的組合只差二π的整數倍，取它的三角函數就又是一個單值積分。

**English**: Degeneracy also increases the number of one-valued integrals. Without it, only s of them are one-valued; the rest are differences of angle over frequency, which are not. With it, a combination of angles is fixed up to multiples of two pi, and its cosine is one more.

**動畫**：同一張閉合圖：簡併時多出來的守恆量就是這種閉合的來源。

---

## 第 9 拍｜庫侖場：完全簡併

**畫面公式**：庫侖場：完全簡併　/　the Coulomb field: completely degenerate　/　`U = − α / r        r , θ , φ    and    ξ , η , φ`

**中文旁白**：庫侖場就是例子：它多出來的那個單值積分，正是專屬於它的那個向量；而克卜勒運動在球座標與拋物線座標下都能分離變數。最後補一句：多自由度時，每個作用變數同樣是絕熱不變量。

**English**: The Coulomb field is the example: its extra one-valued integral is the vector peculiar to that field, and Kepler motion separates in spherical and in parabolic coordinates alike. One last remark: with many degrees of freedom, every action variable is again an adiabatic invariant.

**動畫**：換成克卜勒橢圓：焦點上是吸引中心，軌道閉合，並畫出那個專屬於庫侖場的守恆向量 A。

---
