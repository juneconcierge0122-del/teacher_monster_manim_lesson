# Landau Mechanics 23 — Oscillations with several degrees of freedom: normal modes

> 《Landau–Lifshitz 經典力學》教學系列第 23 課
> 中文標題：多自由度振盪：簡正模態

## 繁體中文旁白

前面談的是單一自由度；如果系統有很多個自由度、而且彼此耦合，運動看起來會很複雜。

但在穩定平衡附近，動能和位能都能寫成座標的二次型，拉格朗日量就是這兩者的差。

一樣假設每個座標都按同一個頻率 ω 做指數振盪，代入後得到一組線性代數方程。

要有非零解，係數的行列式必須為零；這個特徵方程的根，就是系統的固有頻率。

每個固有頻率對應一個簡正模態；第一個是同相模態：兩個質量一起往同方向擺動，頻率較低。

第二個是反相模態：兩個質量往相反方向擺動，中間的彈簧被拉得更緊，所以頻率較高。

一般運動就是這些簡正模態的疊加；在簡正座標下，每個模態各自獨立地簡諧振盪。

## English narration

So far we treated one degree of freedom; when a system has many coupled degrees of freedom, the motion can look complicated.

But near stable equilibrium both the kinetic and the potential energy are quadratic forms in the coordinates, and the Lagrangian is their difference.

Again we assume every coordinate oscillates at the same frequency omega, which turns the equations into a set of linear algebraic equations.

For a non-zero solution the determinant of the coefficients must vanish; the roots of this characteristic equation are the system's eigenfrequencies.

Each eigenfrequency gives a normal mode; the first is the in-phase mode, where the two masses swing together in the same direction, at the lower frequency.

The second is the out-of-phase mode, where the masses swing in opposite directions, stretching the middle spring more, so the frequency is higher.

The general motion is a superposition of these normal modes; in normal coordinates each mode oscillates independently and harmonically.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於畫面上方；主畫面為動畫（兩個耦合質量 + 三根彈簧）。

- 第 2 句 / line 2: `L = ½ Σ ( mᵢₖ ẋᵢ ẋₖ − kᵢₖ xᵢ xₖ )`
- 第 3 句 / line 3: `xₖ = Aₖ · exp( i ω t )`
- 第 4 句 / line 4: `det( kᵢₖ − ω² mᵢₖ ) = 0`
- 第 5 句 / line 5: `同相 in-phase :  ω₁ = √( k / m )`
- 第 6 句 / line 6: `反相 out-of-phase :  ω₂ = √( 3k / m )`
- 第 7 句 / line 7: `Θ̈ₐ + ωₐ² Θₐ = 0`

## 動畫 / Animation

- 兩個質量（青、紫）以三根彈簧連在兩牆之間。
- 同相模態：兩質量同方向擺動，中間彈簧幾乎不動，頻率 ω₁ = √(k/m)。
- 反相模態：兩質量反方向擺動，中間彈簧被拉伸最多，頻率 ω₂ = √(3k/m)。
- 一般運動：兩模態疊加（拍頻）。箭頭標示各質量瞬時位移方向。
