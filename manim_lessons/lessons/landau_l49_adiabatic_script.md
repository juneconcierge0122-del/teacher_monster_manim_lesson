# 第 49 課｜絕熱不變量：慢慢改變參數，相軌跡的面積不變（Landau §49）

Lesson 49 — Adiabatic invariants: the area of the phase path does not change

- 場景檔：`manim_lessons/lessons/landau_l49_adiabatic.py`（`LandauL49ZH` / `LandauL49EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[49]` 與 `FORMULAS[49]`
- 配音：`manim_lessons/samples/audio_l49/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 38 秒、英文約 2 分 38 秒

兩張圖，照著論證的順序出場。先是一個被慢慢拉短的單擺：參數在許多個週期裡才改變一點點，所以能量會漂移、不再守恆。接著換成相平面，同樣的慢變化把橢圓拉得又高又窄，而它圍出的面積——絕熱不變量——就印在畫面上，數字始終不動。

---

## 第 0 拍｜慢慢改變的參數 λ

**畫面公式**：慢慢改變的參數 λ　/　a slowly varying parameter λ　/　`T ( dλ/dt )   ≪   λ`

**中文旁白**：一個系統在一維裡做有限運動，而它的某個參數隨時間慢慢改變。這裡的「慢」是指：在運動的一個週期裡，這個參數只變了很小的一點點。

**English**: A system performs a finite motion in one dimension, and one of its parameters changes slowly with time. By slowly we mean that the parameter varies only a little during one period of the motion.

**動畫**：單擺以固定的擺長來回擺動；下方標出「一個週期 T 很短，λ 幾乎沒動」。

---

## 第 1 拍｜λ 固定就是封閉系統

**畫面公式**：λ 固定就是封閉系統　/　with λ fixed the system is closed　/　`λ = const     ⟹     E = const   ,   T = T ( E )`

**中文旁白**：參數若固定，系統就是封閉的：能量守恆、運動嚴格週期，週期由能量決定。參數一旦會變，系統就不再封閉，能量也不再守恆。

**English**: If the parameter were fixed, the system would be closed: energy conserved, motion strictly periodic, the period set by the energy. Once the parameter varies, the system is no longer closed and the energy is not conserved.

**動畫**：同一個單擺，擺長仍然固定：這就是封閉系統、能量守恆的情形。

---

## 第 2 拍｜對一個週期取平均

**畫面公式**：對一個週期取平均　/　average over one period　/　`⟨ dE/dt ⟩   ∝   dλ/dt`

**中文旁白**：但參數變得很慢，能量的變化率也很小。把它對一個週期取平均，抹掉快速的抖動，剩下的就是能量緩慢而穩定的漂移，而且正比於參數的變化率。

**English**: But the parameter varies slowly, so the rate of change of the energy is small as well. Average that rate over one period, smoothing away the rapid fluctuations, and what is left is a steady slow drift proportional to the rate of change of the parameter.

**動畫**：右邊出現一根代表擺長 λ 的紫色長桿，並開始緩緩縮短；擺動的振幅與頻率跟著慢慢改變。

---

## 第 3 拍｜哪一個量保持不變？

**畫面公式**：哪一個量保持不變？　/　which quantity stays constant?　/　`I ( E , λ ) = const`

**中文旁白**：換句話說，這樣平均出來的能量其實是參數的一個函數。而這種依賴可以寫成：某個由能量和參數合成的量保持不變。這個量就叫絕熱不變量。

**English**: In other words, the energy taken in this averaged sense behaves as a function of the parameter. That dependence can be written as the constancy of some combination of the energy and the parameter, and this quantity is called an adiabatic invariant.

**動畫**：λ 繼續縮短，單擺越擺越快——能量確實在漂移，但每個週期裡只漂一點點。

---

## 第 4 拍｜能量的變化率

**畫面公式**：能量的變化率　/　the rate of change of the energy　/　`dE/dt = ∂H/∂t = ( ∂H/∂λ ) ( dλ/dt )`

**中文旁白**：要找出它，先寫下能量的變化率：它等於哈密頓量對參數的偏導數乘上參數的變化率。右邊除了慢變的參數，還含有快變的座標和動量，所以要對週期取平均。

**English**: To find it, start from the rate of change of the energy: it is the derivative of the Hamiltonian with respect to the parameter, times the rate of change of the parameter. The right-hand side still carries the fast coordinate and momentum, so we average over a period.

**動畫**：單擺淡出，換成相平面：座標與動量張成的平面上，代表點沿著一條封閉的橢圓軌跡繞行。

---

## 第 5 拍｜把時間積分換成座標積分

**畫面公式**：把時間積分換成座標積分　/　trade the time integral for the coordinate　/　`⟨ ∂H/∂λ ⟩ = ( 1/T ) ∮ ( ∂H/∂λ ) dt        T = ∮ dq / ( ∂H/∂p )`

**中文旁白**：平均就是對時間積分再除以週期。用哈密頓方程可以把時間積分換成座標積分：時間的微元等於座標微元除以速度，而週期就是同一個積分繞行一圈。

**English**: The average is an integral over time divided by the period. Hamilton's equation lets us trade the time integral for one over the coordinate: an element of time is an element of coordinate divided by the velocity, and the period is that same integral taken once round.

**動畫**：在橢圓上某個 q 的位置畫出一條窄縫 dq，以及該處的動量 p；這正是把時間積分換成座標積分的圖像。

---

## 第 6 拍｜沿著 λ 固定的那條軌道

**畫面公式**：沿著 λ 固定的那條軌道　/　along the path at fixed λ　/　`H ( q , p , λ ) = E     ⟹     ( ∂H/∂λ ) / ( ∂H/∂p ) = − ∂p/∂λ`

**中文旁白**：積分要沿著參數固定時的軌道走。沿著它哈密頓量等於能量，動量就是座標的函數，只帶能量和參數兩個常數。把這個關係對參數微分，被平均的量就換成了動量對參數的偏導數。

**English**: The integration follows the path for a fixed parameter. Along it the Hamiltonian equals the energy, so the momentum is a function of the coordinate with two constants in it. Differentiating that relation by the parameter turns the averaged quantity into a derivative of the momentum.

**動畫**：同一張圖：沿著這條 λ 固定的軌道，哈密頓量等於能量，動量就是座標的函數。

---

## 第 7 拍｜環積分除以 2π

**畫面公式**：環積分除以 2π　/　the loop integral over two pi　/　`∮ [ ( ∂p/∂E ) ( dE/dt ) + ( ∂p/∂λ ) ( dλ/dt ) ] dq = 0`

**中文旁白**：代回去以後，分子和分母的積分合成一條很漂亮的式子：動量沿軌道的環積分除以二π，它的時間導數等於零。這個量就是絕熱不變量。

**English**: Substituting, the numerator and the denominator combine into one clean statement: the loop integral of the momentum around the path, divided by two pi, has zero time derivative. That quantity is the adiabatic invariant.

**動畫**：窄縫淡出，橢圓內部整個填滿：這塊面積就是動量沿軌道的環積分。

---

## 第 8 拍｜相軌跡圍出來的面積

**畫面公式**：相軌跡圍出來的面積　/　the area enclosed by the phase path　/　`I = ∮ p dq / 2π = ∬ dp dq / 2π        2π ( ∂I/∂E ) = T`

**中文旁白**：它有很清楚的幾何意義。一個自由度的相空間就是座標和動量張成的平面，週期運動在上面畫出一條封閉曲線，而這個量正是曲線圍出的面積除以二π。它對能量微分就得到週期。

**English**: The meaning is geometrical. With one degree of freedom, phase space is the plane of coordinate and momentum, and a periodic motion draws a closed curve on it. The invariant is the area inside that curve divided by two pi, and differentiating it by the energy gives the period.

**動畫**：頻率開始緩慢上升，橢圓變得又高又窄；畫面上方即時顯示「面積 / 2π」，數字一直是 0.632。

---

## 第 9 拍｜諧振子：I = E / ω

**畫面公式**：諧振子：I = E / ω　/　the oscillator: I = E over ω　/　`∂E/∂I = ω        H = p²/2m + ½ m ω² q²     ⟹     I = E / ω`

**中文旁白**：倒過來，能量對它微分就是頻率。拿諧振子檢驗：相軌跡是一個橢圓，面積除以二π剛好等於能量除以頻率。所以參數慢慢改變時，能量會和頻率成正比地一起變。

**English**: The inverse derivative is the frequency. Test all this on the harmonic oscillator: its phase path is an ellipse, and the area inside divided by two pi is the energy over the frequency. So when the parameters change slowly, the energy stays proportional to the frequency.

**動畫**：同一個變形繼續，上面再加一行即時的 ω 與 E：兩者一起變大，比值不變，正是 I = E / ω。

---
