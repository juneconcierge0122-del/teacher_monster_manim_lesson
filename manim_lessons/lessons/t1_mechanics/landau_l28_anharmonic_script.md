# Landau Mechanics 28 — Anharmonic oscillations: frequency depends on amplitude

> 《Landau–Lifshitz 經典力學》教學系列第 28 課
> 中文標題：非簡諧振盪：頻率會隨振幅改變

## 繁體中文旁白

之前的小振盪理論只保留了位能與動能的二次項；如果再保留更高次的項，就進入非簡諧、也就是非線性振盪。

把拉格朗日量展開到三次、四次項，就多了 x³ 和 x⁴ 這些非簡諧項。

對應的運動方程右邊也不再是零，而是出現 −αx² − βx³ 這些非線性項。

我們用逐次逼近法求解：先取最低階的 x = a cos(ωt)，再一項一項修正。

第一個新現象：運動不再是純正弦；非線性項會生出倍頻，也就是 2ω、3ω 的泛音，波形因此變形。

第二個、也是最重要的新現象：振盪的頻率會隨振幅改變，ω 等於 ω₀ 加上 κ 乘 a 平方。

所以振幅越大，頻率偏移越多；不同振幅的振子會漸漸失去同步，這正是非線性振盪的招牌特徵。

## English narration

The small-oscillation theory kept only the quadratic terms of the potential and kinetic energy; keeping higher terms gives anharmonic, or non-linear, oscillations.

Expanding the Lagrangian to third and fourth order adds anharmonic terms in x-cubed and x-to-the-fourth.

The equation of motion then gains non-linear terms on the right: minus alpha x-squared minus beta x-cubed.

We solve by successive approximation: start from the lowest order, x equals a cosine omega t, then correct it term by term.

The first new effect: the motion is no longer a pure sine; the non-linear terms generate overtones at two omega and three omega, so the waveform is distorted.

The second and most important effect: the oscillation frequency now depends on the amplitude, omega equals omega-zero plus kappa a-squared.

So the larger the amplitude, the larger the frequency shift; oscillators of different amplitude gradually fall out of step, the hallmark of non-linear oscillation.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於上方；主畫面為 x(t) 曲線動畫。

- 第 2 句 / line 2: `L = ½m ẋ² − ½m ω₀² x²      − ⅓m α x³ − ¼m β x⁴`
- 第 3 句 / line 3: `ẍ + ω₀² x = −α x² − β x³`
- 第 4 句 / line 4: `x = x⁽¹⁾ + x⁽²⁾ + … ,   x⁽¹⁾ = a cos(ω t)`
- 第 5 句 / line 5: `x⁽²⁾ = −α a² / 2ω₀²      + (α a² / 6ω₀²) cos(2ω t)`
- 第 6 句 / line 6: `ω = ω₀ + κ a²`
- 第 7 句 / line 7: `κ = 3β / 8ω₀ − 5α² / 12ω₀³`

## 動畫 / Animation

- 純正弦波（青）作為簡諧參考。
- 非簡諧波形（黃）：含 2ω 泛音、上下不對稱、波形變形。
- 頻率隨振幅：小振幅（青）與大振幅（紅）兩條波，起初同步、逐漸失步。
