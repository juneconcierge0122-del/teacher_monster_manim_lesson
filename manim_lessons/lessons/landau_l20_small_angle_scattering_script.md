# Landau Mechanics 20 — Small-angle scattering: deflection by perturbation

> 《Landau–Lifshitz 經典力學》教學系列第 20 課
> 中文標題：小角度散射：用微擾法直接算偏轉

## 繁體中文旁白

當撞擊參數 b 很大、位能很弱時，粒子只被輕輕推偏；這種小角度散射可以直接用微擾法計算，而且在實驗室系就能完成。

把 x 軸取在入射動量方向；偏轉很小時，散射角近似為 χ ≈ Δp⊥ / p，其中 p = m × v∞ 是入射動量。

垂直方向的動量增量，來自整段路徑上的橫向力：Δp⊥ = ∫ F⊥ dt，積分沿整條直線軌跡進行。

因為這個積分本身已經很小，可假設粒子沿直線 y = b 等速前進；於是 F⊥ = −(dU/dr) × (b / r)，dt = dx / v∞。

把對 x 的積分換成對 r 的積分（利用 r² = x² + b²），得到 χ = −[2b / (m × v∞²)] × ∫ (dU/dr) × dr / √(r² − b²)，積分下限為 b。

這條公式把散射角直接寫成撞擊參數與位能的單一積分；只要知道 U(r)，不必解出完整軌道就能得到 χ(b)。

最後代回一般截面公式 dσ = (b / χ) × |db/dχ| × dΩ，就得到小角度區的微分截面，這正是弱場散射最實用的近似。

## English narration

When the impact parameter b is large, the potential is weak and the particle is barely nudged; the deflection then follows directly from perturbation, in the laboratory frame.

Take the x-axis along the incident momentum; for a small deflection the scattering angle is χ ≈ Δp⊥ / p, where p = m × v∞ is the incident momentum.

The transverse momentum comes from the sideways force: Δp⊥ = ∫ F⊥ dt, taken over the straight-line path.

Because the integral already contains the small potential, we let the particle move in a straight line y = b at constant speed, so F⊥ = −(dU/dr) × (b / r) and dt = dx / v∞.

Turning the x-integral into an r-integral through r² = x² + b² gives χ = −[2b / (m × v∞²)] × ∫ (dU/dr) × dr / √(r² − b²), with lower limit b.

This writes the scattering angle as one integral of impact parameter and potential; U(r) alone gives χ(b) without solving the full orbit.

Substituting into dσ = (b / χ) × |db/dχ| × dΩ gives the differential cross-section at small angles, the most useful weak-field approximation.
