# Landau Mechanics 26 — Forced oscillations with friction: the resonance curve

> 《Landau–Lifshitz 經典力學》教學系列第 26 課
> 中文標題：有阻尼的受迫振盪與共振曲線

## 繁體中文旁白

把一個週期性外力加到有阻尼的振子上；運動方程的右邊，就多了一項 f cos(γt) 除以質量，等於把受迫振盪和阻尼合在一起。

過渡項會隨時間指數衰減掉，經過一段時間後只剩下穩態：系統以驅動頻率 γ 持續振盪。

這個穩態振幅 b 會隨驅動頻率而變，由一個同時含有頻率差與阻尼 λ 的分母決定。

和無阻尼的情形不同，阻尼讓分母永遠不為零，所以共振峰不再發散、而是有限的，峰值大約落在固有頻率 ω₀ 附近。

關鍵在於阻尼的大小：阻尼越小，分母在共振處就越小，共振峰也就越高、越尖。

峰的尖銳程度可以用品質因子 Q 來衡量，它等於 ω₀ 除以 2λ；阻尼越小，Q 越大、共振也越尖銳。

此外，振盪總是落後外力一個相位；遠低於共振時幾乎同相，遠高於共振時接近反相，而在共振點恰好落後 90 度，阻尼把這個相位跳變抹平。

## English narration

We now drive the damped oscillator with a periodic force; the right-hand side of the equation gains a term f cos(gamma t) divided by the mass, combining forced motion with friction.

The transient part decays away exponentially, so after some time only the steady state remains: the system oscillates at the driving frequency gamma.

This steady amplitude b varies with the driving frequency, set by a denominator that contains both the frequency mismatch and the damping lambda.

Unlike the frictionless case, damping keeps the denominator from ever reaching zero, so the resonance peak is finite instead of infinite, and it sits close to the natural frequency omega-zero.

The key is the amount of damping: the smaller the damping, the smaller the denominator at resonance, and the taller and sharper the peak.

The sharpness of the peak is measured by the quality factor Q, equal to omega-zero over two lambda; less damping means a larger Q and a sharper resonance.

The oscillation also always lags the force by a phase; far below resonance they are nearly in phase, far above nearly opposite, and exactly at resonance the lag is ninety degrees, with friction smoothing the jump.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於上方；主畫面為共振曲線動畫。

- 第 1 句 / line 1: `ẍ + 2λ ẋ + ω₀² x = (f / m) cos(γ t)`
- 第 2 句 / line 2: `x = b · cos(γ t + δ)`
- 第 3 句 / line 3: `b = f / ( m √( (ω₀² − γ²)² + 4λ²γ² ) )`
- 第 4 句 / line 4: `γₘₐₓ = √( ω₀² − 2λ² )`
- 第 5 句 / line 5: `bₘₐₓ ≈ f / ( 2 m λ ω₀ )`
- 第 6 句 / line 6: `Q = ω₀ / ( 2λ )`
- 第 7 句 / line 7: `tan δ = 2λγ / ( γ² − ω₀² )`

## 動畫 / Animation

- 振幅 b 對驅動頻率 γ 作圖，虛線標出固有頻率 ω₀。
- 共振曲線族：λ 由大到小畫出四條，峰值越來越高、越尖。
- 對應品質因子 Q = ω₀ / 2λ：阻尼越小 Q 越大、共振越尖。
