# Landau Mechanics 25 — Damped oscillations: decay in a medium

> 《Landau–Lifshitz 經典力學》教學系列第 25 課
> 中文標題：阻尼振盪：在介質中衰減的振動

## 繁體中文旁白

前面都假設運動發生在真空中；真實的振子會受到介質的阻力，能量會慢慢耗散成熱。

對小振盪，阻力可近似為正比於速度；把它加進運動方程再除以質量，就得到阻尼振盪方程。

一樣代入指數解，得到特徵方程；它的根是負 λ 加減一個平方根，決定了系統的行為。

當阻尼較小、λ 小於 ω₀ 時，根是複數：運動仍是簡諧振盪，但振幅以 e 的負 λt 次方指數衰減。

因為振幅平方正比於能量，系統的平均能量以 e 的負 2λt 次方衰減。

當阻尼很強、λ 大於 ω₀ 時，兩個根都是負實數：運動不再振盪，而是非週期地慢慢回到平衡。

剛好在臨界阻尼、λ 等於 ω₀ 時，系統以不振盪的方式最快回到平衡；這就是三種阻尼行為。

## English narration

So far we assumed motion in a vacuum; a real oscillator feels resistance from the medium, and its energy is gradually dissipated as heat.

For small oscillations the friction is approximately proportional to velocity; adding it to the equation of motion and dividing by the mass gives the damped-oscillator equation.

Substituting an exponential solution gives the characteristic equation, whose roots are minus lambda plus or minus a square root that decides the behaviour.

For weak damping, lambda less than omega-zero, the roots are complex: the motion is a harmonic oscillation whose amplitude decays as e to the minus lambda t.

Since the squared amplitude is proportional to energy, the mean energy decays as e to the minus two lambda t.

For strong damping, lambda greater than omega-zero, both roots are real and negative: the motion no longer oscillates but returns to equilibrium aperiodically.

Exactly at critical damping, lambda equal to omega-zero, the system returns to equilibrium as fast as possible without oscillating; these are the three regimes of damping.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於上方（阻尼類型名稱依語言切換）；主畫面為 x(t) 曲線動畫。

- 第 2 句 / line 2: `m ẍ = −k x − α ẋ →   ẍ + 2λ ẋ + ω₀² x = 0` / `m ẍ = −k x − α ẋ →   ẍ + 2λ ẋ + ω₀² x = 0`
- 第 3 句 / line 3: `r² + 2λ r + ω₀² = 0 →   r = −λ ± √( λ² − ω₀² )` / `r² + 2λ r + ω₀² = 0 →   r = −λ ± √( λ² − ω₀² )`
- 第 4 句 / line 4: `欠阻尼  λ < ω₀ x = a · exp(−λt) · cos(ω t + φ) ,   ω = √( ω₀² − λ² )` / `underdamped,  λ < ω₀ x = a · exp(−λt) · cos(ω t + φ) ,   ω = √( ω₀² − λ² )`
- 第 5 句 / line 5: `E = E₀ · exp(−2λt)` / `E = E₀ · exp(−2λt)`
- 第 6 句 / line 6: `過阻尼  λ > ω₀ x = c₁ exp(r₁ t) + c₂ exp(r₂ t)` / `overdamped,  λ > ω₀ x = c₁ exp(r₁ t) + c₂ exp(r₂ t)`
- 第 7 句 / line 7: `臨界阻尼  λ = ω₀ x = (c₁ + c₂ t) · exp(−λt)` / `critical,  λ = ω₀ x = (c₁ + c₂ t) · exp(−λt)`

## 動畫 / Animation

- x(t) 圖：先畫無阻尼的等幅振盪作對照。
- 欠阻尼：衰減正弦曲線 + 紅色虛線指數包絡 ±e^(−λt)。
- 過阻尼：非週期單調衰減回平衡。
- 臨界阻尼：最快的非振盪回歸。
