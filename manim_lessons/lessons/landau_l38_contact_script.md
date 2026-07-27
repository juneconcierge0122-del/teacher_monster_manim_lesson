# 第 38 課｜剛體的接觸：滾動與非完整約束（Landau §38）

Lesson 38 — Rigid bodies in contact: rolling and non-holonomic constraints

- 場景檔：`manim_lessons/lessons/landau_l38_contact.py`（`LandauL38ZH` / `LandauL38EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[38]` 與 `FORMULAS[38]`
- 配音：`manim_lessons/samples/audio_l38/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 51 秒、英文約 2 分 38 秒

全課圍繞接觸點：先是靜力平衡與成對的反作用力，接著是光滑面上的滑動與粗糙面上的純滾動，最後用一顆球沿封閉路徑滾一圈回到原地卻換了朝向，說明什麼叫非完整約束。

---

## 第 0 拍｜平衡：總力與總力矩都為零

**畫面公式**：平衡：總力與總力矩都為零　/　equilibrium: total force and torque both vanish　/　`Σ f = 0     ,     Σ r × f = 0`

**中文旁白**：先看平衡。剛體的運動方程告訴我們，平衡的條件就是作用在物體上的總力和總力矩都等於零。因為總力為零時力矩與原點的選擇無關，取哪一點當原點都可以。

**English**: Start with equilibrium. The equations of motion say the conditions are simply that the total force and the total torque on the body both vanish. Since the torque is independent of the origin when the total force is zero, any origin will do.

**動畫**：一塊多邊形剛體，三個外力箭頭作用在不同點上，右側列出平衡的兩個條件。

---

## 第 1 拍｜接觸點上的反作用力成對出現

**畫面公式**：接觸點上的反作用力成對出現　/　reactions come in equal and opposite pairs　/　`f₁₂  =  − f₂₁`

**中文旁白**：如果有好幾個剛體互相接觸，每一個都必須各自滿足這兩個條件，而且要把接觸點上其他物體施加的力算進去。這些接觸力叫做反作用力；任意兩個物體之間的反作用力大小相等、方向相反。

**English**: If several rigid bodies are in contact, each must satisfy both conditions on its own, counting the forces the others exert at the points of contact. These contact forces are called reactions, and the reactions between any two bodies are equal and opposite.

**動畫**：兩塊疊在一起的物體，接觸面上一對大小相等、方向相反的紅色反作用力箭頭。

---

## 第 2 拍｜能自由滑動時，反作用力垂直於接觸面

**畫面公式**：能自由滑動時，反作用力垂直於接觸面　/　free to slide: the reaction is normal to it　/　`N  ⊥  surface`

**中文旁白**：反作用力的大小和方向，一般要把所有物體的平衡方程聯立解出來。但有些情況方向是已知的：例如兩個物體可以自由地在彼此表面上滑動時，反作用力就垂直於接觸面。

**English**: In general the magnitudes and directions of the reactions follow from solving the equilibrium equations for all the bodies together. Sometimes the direction is given: if two bodies can slide freely on each other, the reaction is normal to the surface.

**動畫**：斜面上的方塊，青色的法向反作用力垂直於斜面。

---

## 第 3 拍｜滑動：反作用力垂直，摩擦力沿切線

**畫面公式**：滑動：反作用力垂直，摩擦力沿切線　/　sliding: reaction normal, friction tangential　/　`N ⊥ surface   ,   F_fric ∥ surface`

**中文旁白**：兩個接觸的物體如果有相對運動，除了反作用力還會出現摩擦。接觸物體的運動有兩種：滑動和滾動。滑動時反作用力垂直於接觸面，摩擦力沿著切線方向。

**English**: When two bodies in contact move relative to each other, friction appears alongside the reaction. There are two kinds of motion: sliding and rolling. In sliding the reaction is perpendicular to the surfaces and the friction is tangential.

**動畫**：同一個斜面，法向力之外多出一支沿斜面的紅色摩擦力箭頭，方向與運動相反。

---

## 第 4 拍｜純滾動：接觸點瞬間靜止

**畫面公式**：純滾動：接觸點瞬間靜止　/　pure rolling: the contact point is at rest　/　`v ( contact ) = 0`

**中文旁白**：純滾動則完全不同：接觸點上沒有相對運動，滾動的物體在每一瞬間就像被釘在接觸點上一樣。這時反作用力可以指向任何方向，不必垂直於接觸面；滾動摩擦則表現成一個阻礙滾動的力矩。

**English**: Pure rolling is quite different: there is no relative motion at the point of contact, so at every instant the rolling body is as if fixed to that point. The reaction may then point in any direction, and rolling friction appears as a torque opposing the roll.

**動畫**：一個滾動的圓輪，輪面上不同高度的速度箭頭長短不一，接觸點的速度為零（紅點）。

---

## 第 5 拍｜完全光滑與完全粗糙

**畫面公式**：完全光滑與完全粗糙　/　perfectly smooth and perfectly rough　/　`smooth :  no sliding friction        rough :  rolling only`

**中文旁白**：如果滑動摩擦小到可以忽略，就說表面是完全光滑的；如果只能純滾動、而且滾動摩擦可以忽略，就說表面是完全粗糙的。這兩種情況下摩擦力都不會明顯出現在問題裡，問題就是純粹的力學問題。

**English**: If sliding friction is negligible the surfaces are called perfectly smooth; if only pure rolling is possible and rolling friction is negligible they are called perfectly rough. In both cases friction never appears explicitly and the problem stays purely mechanical.

**動畫**：左右對照：完全光滑面上的方塊只滑不轉，完全粗糙面上的圓輪只滾不滑。

---

## 第 6 拍｜接觸會減少自由度

**畫面公式**：接觸會減少自由度　/　contact removes degrees of freedom　/　`contact     ⟹     fewer degrees of freedom`

**中文旁白**：接觸會減少自由度。以前我們都直接用剛好等於自由度數目的座標；但在滾動的問題裡，這樣選座標可能根本做不到。

**English**: Contact reduces the number of degrees of freedom. Until now we have simply used coordinates matching the true number of degrees of freedom, but for rolling such a choice of coordinates may be impossible.

**動畫**：自由剛體六個自由度，放到面上剩五個，純滾動的球只剩三個——數字逐級遞減。

---

## 第 7 拍｜滾動條件是速度之間的關係

**畫面公式**：滾動條件是速度之間的關係　/　the rolling condition relates the velocities　/　`Σ cₐᵢ ( dqᵢ/dt ) = 0`

**中文旁白**：滾動的條件是：接觸點的速度必須相等；物體在固定面上滾動時，接觸點的速度就是零。一般寫成一組速度之間的線性關係，係數只依賴座標。

**English**: The rolling condition is that the contact points have equal velocities; on a fixed surface the contact point is at rest. In general this is a set of linear relations among the velocities whose coefficients depend only on the coordinates.

**動畫**：只有公式與說明：滾動條件是速度之間的線性關係，係數只依賴座標。

---

## 第 8 拍｜繞一圈回到原處，方向卻變了

**畫面公式**：繞一圈回到原處，方向卻變了　/　back to the same place, pointing elsewhere　/　`V − a Ω × n = 0`

**中文旁白**：如果這些式子的左邊不是某個座標函數的全微分，就積不出來，也就不能化成只含座標的關係、拿來減少座標數目。這種約束叫做非完整約束，球在平面上滾動正是最好的例子。

**English**: If those left-hand sides are not total time derivatives, the relations cannot be integrated into relations between coordinates alone, so they cannot reduce the number of coordinates. Such constraints are called non-holonomic. A sphere rolling on a plane is the example.

**動畫**：一顆球沿著虛線的封閉方形路徑滾一圈，回到原地時球面上的標記已經轉到別的方向。

---

## 第 9 拍｜拉格朗日乘子，或達朗貝爾原理

**畫面公式**：拉格朗日乘子，或達朗貝爾原理　/　multipliers, or d'Alembert's principle　/　`d/dt ( ∂L/∂q̇ᵢ ) − ∂L/∂qᵢ = Σ λₐ cₐᵢ` ／ `dP/dt = Σ f   ,   dM/dt = Σ r × f`

**中文旁白**：所以只好保留不獨立的座標。回到最小作用量原理，用待定乘子把約束加進去，運動方程就多出一項乘子。另一種做法是達朗貝爾原理：直接把反作用力明白地寫進動量和角動量的方程裡。

**English**: So we must keep coordinates that are not independent. Returning to least action and adding the constraints with undetermined multipliers gives equations of motion carrying one extra multiplier term. Alternatively d'Alembert's principle writes the reactions in explicitly.

**動畫**：把約束用不定乘子加進拉格朗日方程，右側同時列出動量與角動量的方程。

---
