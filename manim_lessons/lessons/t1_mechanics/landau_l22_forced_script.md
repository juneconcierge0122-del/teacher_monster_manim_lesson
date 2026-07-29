# Landau Mechanics 22 — Forced oscillations and resonance

> 《Landau–Lifshitz 經典力學》教學系列第 22 課
> 中文標題：受迫振盪與共振

## 繁體中文旁白

一個原本會自由振盪的系統，如果再受到一個隨時間變化的外力，運動會怎麼改變？

在運動方程的右邊加上這個外力：質量乘加速度，加上 k 乘位移，等於外力 F(t)。

最重要的情形是週期性外力：F(t) 以固定的驅動頻率 γ 做餘弦振盪。

穩定之後，系統會跟著驅動頻率 γ 擺動，振幅正比於一除以固有頻率平方減驅動頻率平方。

當驅動頻率接近固有頻率 ω，這個分母趨近於零，振幅急速放大，這就是共振。

剛好落在共振點上，振幅不再有限，而是隨時間線性成長：位移像一個越長越大的正弦波。

所以一般運動是兩部分疊加：系統自己的自由振盪，加上被外力牽著走的受迫振盪。

## English narration

If a system that would freely oscillate is also driven by a time-varying external force, how does its motion change?

We add that force to the right-hand side of the equation of motion: mass times acceleration plus k times displacement equals the force F(t).

The most important case is a periodic force: F(t) oscillates as a cosine at a fixed driving frequency gamma.

After it settles, the system swings at the driving frequency gamma, with an amplitude proportional to one over the natural frequency squared minus the driving frequency squared.

As the driving frequency approaches the natural frequency omega, that denominator tends to zero and the amplitude grows sharply: this is resonance.

Exactly at resonance the amplitude is no longer finite but grows linearly in time: the displacement looks like a sine wave that keeps getting taller.

So the general motion is a sum of two parts: the system's own free oscillation, plus the forced oscillation dragged along by the external force.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式顯示於畫面上方；主畫面為動畫（彈簧振子、驅動力、共振曲線）。

- 第 2 句 / line 2: `m ẍ + k x = F(t)`
- 第 3 句 / line 3: `F(t) = f · cos(γ t)`
- 第 4 句 / line 4: `x(t) = [ f / ( m (ω² − γ²) ) ] · cos(γ t)`
- 第 5 句 / line 5: `a(γ) = f / ( m · |ω² − γ²| )`
- 第 6 句 / line 6: `x(t) = ( f / (2 m ω) ) · t · sin(ω t)`

## 動畫 / Animation

- 彈簧-質量振子（左）：靜止 → 受驅動擺動 → 共振下振幅線性成長。
- 紅色驅動力箭頭隨 F(t) 改變方向與大小。
- 共振曲線（右）：振幅對驅動頻率 γ，在 γ = ω 處發散（紅色虛線）。
