# Landau Mechanics 29 — Non-linear resonance: the leaning peak and jumps

> 《Landau–Lifshitz 經典力學》教學系列第 29 課
> 中文標題：非線性共振：傾斜的共振峰與跳變

## 繁體中文旁白

如果被驅動的振子本身是非線性的，共振就會出現全新的現象；這是把受迫、阻尼與非簡諧合在一起。

在線性近似下，靠近共振的振幅 b 是一條對稱的共振峰，峰值落在 ε 等於零的地方。

但非線性讓固有頻率隨振幅改變，ω = ω₀ + κb²，於是共振條件本身也會隨振幅移動。

把這個關係代回共振公式，整條共振峰就向一側傾斜、彎了過去。

當驅動力夠大，曲線會折返：同一個頻率下出現三個振幅，其中中間那一支是不穩定的。

這造成跳變與遲滯：頻率往上掃時振幅沿上支增加、到折點突然跳下；往下掃時則在另一點跳上。

所以非線性共振不再是對稱的尖峰，而是傾斜、折疊、還帶有跳變的曲線，這在真實振子中很常見。

## English narration

If the driven oscillator is itself non-linear, resonance shows entirely new features; this combines forcing, friction, and anharmonicity.

In the linear approximation the near-resonance amplitude b is a symmetric peak, with its maximum at epsilon equal to zero.

But non-linearity makes the eigenfrequency depend on amplitude, omega equals omega-zero plus kappa b-squared, so the resonance condition itself shifts with amplitude.

Substituting this back into the resonance relation, the whole peak leans to one side and bends over.

When the driving force is large enough the curve folds back: at one frequency three amplitudes appear, and the middle one is unstable.

This produces jumps and hysteresis: sweeping the frequency up, the amplitude rises along the upper branch and drops abruptly at the fold; sweeping down, it jumps up at a different point.

So non-linear resonance is no longer a symmetric spike but a leaning, folded curve with jumps, something very common in real oscillators.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式與模態名稱顯示於上方（名稱依語言切換）；主畫面為共振曲線動畫。

- 第 2 句 / line 2: `b² ( ε² + λ² ) = f² / ( 4 m² ω₀² )` / `b² ( ε² + λ² ) = f² / ( 4 m² ω₀² )`
- 第 3 句 / line 3: `ω = ω₀ + κ b²` / `ω = ω₀ + κ b²`
- 第 4 句 / line 4: `b² [ (ε − κ b²)² + λ² ] = f² / ( 4 m² ω₀² )` / `b² [ (ε − κ b²)² + λ² ] = f² / ( 4 m² ω₀² )`
- 第 5 句 / line 5: `三個振幅：中間分支不穩定` / `three amplitudes: middle branch unstable`
- 第 6 句 / line 6: `跳變與遲滯` / `jumps and hysteresis`
- 第 7 句 / line 7: `b_max = f / ( 2 m ω₀ λ )` / `b_max = f / ( 2 m ω₀ λ )`

## 動畫 / Animation

- 共振曲線 b 對 ε：對稱峰（青，線性）→ 傾斜峰（黃，非線性）→ 折疊曲線（紅，強驅動）。
- 折疊區同一頻率有三個振幅，中間分支不穩定。
- 跳變箭頭：往上/往下掃頻在不同折點跳變（遲滯）。
