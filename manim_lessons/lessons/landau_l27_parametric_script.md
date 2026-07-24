# Landau Mechanics 27 — Parametric resonance: exciting a system by changing its parameters

> 《Landau–Lifshitz 經典力學》教學系列第 27 課
> 中文標題：參數共振：週期性改變參數就能激振

## 繁體中文旁白

有一種系統不靠外力驅動，只要週期性地改變它自己的參數，就能被激發起振盪；盪鞦韆就是最好的例子。

這類系統的運動方程是 ẍ + ω²(t) x = 0，其中頻率 ω 會隨時間週期性地變化。

最重要的情形是頻率被輕微地週期調變：ω²(t) = ω₀²(1 + h cos(γt))，其中 h 很小。

參數共振最強的條件很特別：調變頻率要接近固有頻率的兩倍，也就是 γ 約等於 2ω₀。

這時平衡點變得不穩定：任何微小擾動都會讓振幅以指數成長，x 正比於 e 的 st 次方，這和普通共振只線性成長很不一樣。

成長率與共振範圍都由 h 決定：不穩定帶落在 2ω₀ 的兩側，半寬大約是二分之一 h ω₀，帶寬和成長率都正比於 h。

摩擦會對抗它：淨成長變成 e 的 s 減 λ 乘 t 次方，所以成長率 s 必須大於阻尼 λ 才會發生，阻尼也讓不穩定帶變窄。

## English narration

Some systems are excited not by an external force but simply by varying their own parameters periodically; pumping a swing is the classic example.

The equation of motion for such a system is x-double-dot plus omega-squared-of-t times x equals zero, where the frequency omega varies periodically in time.

The most important case is a small periodic modulation of the frequency: omega-squared of t equals omega-zero-squared times one plus h cosine gamma t, with h small.

Parametric resonance is strongest under a special condition: the modulation frequency must be near twice the natural frequency, gamma close to two omega-zero.

Then the equilibrium becomes unstable: any tiny disturbance makes the amplitude grow exponentially, x proportional to e to the s t, unlike ordinary resonance which grows only linearly.

The growth rate and the resonance range are both set by h: the unstable band lies on either side of two omega-zero with a half-width of about one half h omega-zero, both width and growth proportional to h.

Friction opposes it: the net growth becomes e to the s minus lambda times t, so the growth rate s must exceed the damping lambda, and friction also narrows the unstable band.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於上方；主畫面為動畫（被泵動的鞦韆）。

- 第 2 句 / line 2: `ẍ + ω²(t) · x = 0`
- 第 3 句 / line 3: `ω²(t) = ω₀² · ( 1 + h · cos(γ t) )`
- 第 4 句 / line 4: `γ ≈ 2 ω₀`
- 第 5 句 / line 5: `x ∝ exp( s t )`
- 第 6 句 / line 6: `s² = ¼ [ (½ h ω₀)² − ε² ] |ε| < ½ h ω₀`
- 第 7 句 / line 7: `x ∝ exp( (s − λ) t )`

## 動畫 / Animation

- 單擺（鞦韆）：擺長在每個週期被調變兩次（頻率 2ω₀）。
- 每一段旁白中，擺角振幅都從很小指數成長到很大，示範參數共振。
- 對照：普通共振只線性成長，參數共振是指數成長。
