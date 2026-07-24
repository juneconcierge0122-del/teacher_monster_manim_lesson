# Landau Mechanics 20 — Small-angle scattering: deflection by perturbation

> 《Landau–Lifshitz 經典力學》教學系列第 20 課
> 中文標題：小角度散射：用微擾法直接算偏轉

## 繁體中文旁白

當撞擊參數 b 很大、位能很弱時，粒子只被輕輕推偏；這種小角度散射可以直接用微擾法計算，而且在實驗室系就能完成。

把 x 軸取在入射動量方向；偏轉很小時，散射角約等於垂直方向獲得的動量除以入射動量，而入射動量是質量乘上無限遠速度。

這個垂直動量，來自整段路徑上的橫向力對時間的積分，沿粒子的直線軌跡慢慢累積。

因為這個積分本身已經很小，可以假設粒子沿直線等速前進；橫向力就是位能的徑向梯度乘上一個幾何因子，時間則換成沿路徑的位移。

再把對 x 的積分換成對 r 的積分，就得到一條只依撞擊參數與位能的散射角公式。

這條公式最實用的地方是：只要知道位能，不必解出完整軌道，就能算出散射角如何隨撞擊參數變化。

最後把它代回一般截面公式，就得到小角度區的微分截面，這正是弱場散射最實用的近似。

## English narration

When the impact parameter b is large, the potential is weak and the particle is barely nudged; such small-angle scattering follows directly from perturbation, in the laboratory frame.

Take the x-axis along the incident momentum; for a small deflection the scattering angle is roughly the transverse momentum gained divided by the incident momentum, which is mass times the speed at infinity.

That transverse momentum is the time integral of the sideways force, built up along the particle's straight-line path.

Since the integral is already small, we let the particle move straight at constant speed; the sideways force is the radial gradient of the potential times a geometric factor, and time turns into displacement along the path.

Converting the x-integral into an r-integral then gives a scattering angle that depends only on the impact parameter and the potential.

The real payoff is that knowing the potential alone yields the scattering angle as a function of impact parameter, without ever solving the full orbit.

Substituting it back into the general cross-section gives the differential cross-section at small angles, the most useful weak-field approximation.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式以放大字體顯示於畫面中央（按旁白行對應）：

- 第 2 句 / line 2: `χ ≈ Δp⊥ / p        (p = m × v∞)`
- 第 3 句 / line 3: `Δp⊥ = ∫ F⊥ dt`
- 第 4 句 / line 4: `F⊥ = −(dU/dr) × (b / r) dt = dx / v∞`
- 第 5 句 / line 5: `χ = −[ 2b / (m × v∞²) ]       × ∫ (dU/dr) dr / √(r² − b²)`
- 第 7 句 / line 7: `dσ = (b / χ) × |db/dχ| × dΩ`
