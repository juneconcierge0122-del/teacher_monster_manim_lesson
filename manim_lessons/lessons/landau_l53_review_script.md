# 第 53 課｜《力學》全書總複習：一條原理長出整座力學（Landau 全書回顧）

Lesson 53 — Mechanics, the whole book: one principle, one subject

- 場景檔：`manim_lessons/lessons/landau_l53_review.py`（`LandauL53ZH` / `LandauL53EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[53]` 與 `FORMULAS[53]`
- 配音：`manim_lessons/samples/audio_l53/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 29 秒、英文約 2 分 38 秒

畫面下方是七章的方塊，一章一章亮起來；上方的小舞台則重播那一章真正在講的畫面：變分原理裡互相競爭的兩條路徑、守恆的箭頭、有效位能裡的進動軌道、彈性碰撞的兩個出射角、兩個耦合振子的簡正模態、繞著固定軸轉的剛體，以及相空間裡的封閉迴圈。每一段都是封閉形式的曲線，不需要數值積分。

---

## 第 0 拍｜一切從一條原理開始

**畫面公式**：一切從一條原理開始　/　it all starts from one principle　/　`S = ∫ L ( q , dq/dt , t ) dt          δS = 0`

**中文旁白**：整本《力學》其實只從一件事開始：在所有可能的路徑裡，真實的運動讓作用量取極值；而作用量是拉格朗日量沿著路徑的積分。

**English**: The whole of Mechanics starts from a single statement: among all possible paths, the real motion makes the action stationary, the action being the integral of the Lagrangian along the path.

**動畫**：兩條端點相同的路徑：灰色那條不斷變形，橘色那條不動——真實運動讓作用量取極值。

---

## 第 1 拍｜第一章：運動方程

**畫面公式**：第一章：運動方程　/　chapter I: the equations of motion　/　`d/dt ( ∂L/∂q̇ ) − ∂L/∂q = 0          L = ½ m v² − U`

**中文旁白**：把這個條件寫出來，就得到拉格朗日方程。再加上空間的均勻與各向同性、時間的均勻，就決定了自由粒子的拉格朗日量，也就決定了整個力學的形式。

**English**: Writing that condition out gives Lagrange's equations. Adding the homogeneity and isotropy of space and the homogeneity of time fixes the Lagrangian of a free particle, and with it the form of the whole subject.

**動畫**：第一章亮起：粒子沿著那條駐定路徑來回，速度箭頭跟著它。

---

## 第 2 拍｜第二章：守恆定律

**畫面公式**：第二章：守恆定律　/　chapter II: conservation laws　/　`E = Σ q̇ ( ∂L/∂q̇ ) − L      P = Σ ∂L/∂v      M = Σ r × p`

**中文旁白**：第二章把對稱換成守恆：時間平移給出能量，空間平移給出動量，轉動給出角動量。作用量的形式甚至決定了同一個運動在放大縮小之下怎麼變。

**English**: Chapter two turns symmetry into conservation: translation in time gives energy, translation in space gives momentum, rotation gives angular momentum. The form of the action even fixes how one and the same motion behaves when it is scaled up or down.

**動畫**：第二章亮起：一個三臂的物體轉動，代表角動量的紅色箭頭始終指著同一個方向。

---

## 第 3 拍｜第三章：把方程積出來

**畫面公式**：第三章：把方程積出來　/　chapter III: integrating the equations　/　`t = √(m/2) ∫ dr / √( E − U_eff )        U_eff = U + M² / 2 m r²`

**中文旁白**：第三章把方程積出來。一維運動可以直接化為求積；中心場裡用有效位能把問題壓成一維；克卜勒問題給出橢圓、拋物線與雙曲線三種軌道。

**English**: Chapter three integrates the equations. One-dimensional motion reduces straight to quadratures; a central field is squeezed down to one dimension by the effective potential; and the Kepler problem gives the ellipse, the parabola and the hyperbola.

**動畫**：第三章亮起：中心場裡的軌道在兩個迴轉半徑之間進動，兩個灰圈標出 r 的上下界。

---

## 第 4 拍｜第四章：粒子碰撞

**畫面公式**：第四章：粒子碰撞　/　chapter IV: collisions between particles　/　`dσ = 2π b db          dσ = ( α / 4E )² do / sin⁴ ( θ/2 )`

**中文旁白**：第四章看碰撞：粒子的衰變、彈性碰撞裡的角度關係、散射截面，最後是拉塞福公式。這些結論全部只靠守恆律和換一個參考系。

**English**: Chapter four is collisions: the disintegration of particles, the angles in an elastic collision, cross-sections, and finally Rutherford's formula. All of it rests on conservation laws and on changing the frame of reference.

**動畫**：第四章亮起：一顆粒子沿著虛線射入，撞上靜止的另一顆，兩者以固定的角度分開。

---

## 第 5 拍｜第五章：小振盪

**畫面公式**：第五章：小振盪　/　chapter V: small oscillations　/　`d²x/dt² + ω² x = 0          det | kᵢₖ − ω² mᵢₖ | = 0`

**中文旁白**：第五章是小振盪。位能極小附近一切都變成諧振子：受迫振盪與共振、多自由度的簡正模態、阻尼、參數共振，還有非線性帶來的頻率偏移與跳躍。

**English**: Chapter five is small oscillations. Near a minimum of the potential everything turns into an oscillator: forced motion and resonance, normal modes for many degrees of freedom, damping, parametric resonance, and the shifts and jumps that non-linearity brings.

**動畫**：第五章亮起：兩個質量以同一個頻率、固定的振幅比反向振動——一個簡正模態。

---

## 第 6 拍｜第六章：剛體運動

**畫面公式**：第六章：剛體運動　/　chapter VI: motion of a rigid body　/　`Mᵢ = Iᵢₖ Ωₖ          Iᵢ dΩᵢ/dt + ( Iₖ − Iⱼ ) Ωⱼ Ωₖ = Nᵢ`

**中文旁白**：第六章是剛體：角速度與慣性張量、歐拉方程、歐拉角、對稱陀螺的進動；再加上非慣性參考系裡冒出來的科氏力與離心力。

**English**: Chapter six is the rigid body: angular velocity and the inertia tensor, Euler's equations, the Eulerian angles, the precession of a symmetrical top, and the Coriolis and centrifugal forces that appear in a rotating frame.

**動畫**：第六章亮起：一個剛體繞著傾斜的固定軸旋轉，紅色箭頭是角速度 Ω。

---

## 第 7 拍｜第七章：正則方程

**畫面公式**：第七章：正則方程　/　chapter VII: the canonical equations　/　`H = Σ p q̇ − L      dq/dt = ∂H/∂p , dp/dt = − ∂H/∂q      ∫ dΓ = const`

**中文旁白**：第七章換一種語言。用勒讓德變換把速度換成動量，得到哈密頓方程；帕松括號寫出守恆量的代數；相空間的體積在運動下不變，這就是劉維定理。

**English**: Chapter seven changes the language. A Legendre transformation trades velocities for momenta and gives Hamilton's equations; Poisson brackets write down the algebra of the constants of the motion; and phase volume is carried unchanged by the flow, which is Liouville's theorem.

**動畫**：第七章亮起：相平面上一條封閉迴圈，四個代表點被相流一起帶著走。

---

## 第 8 拍｜第七章：漢彌頓－雅可比

**畫面公式**：第七章：漢彌頓－雅可比　/　chapter VII: Hamilton and Jacobi　/　`∂S/∂t + H ( q , ∂S/∂q , t ) = 0        S = Σ Sₖ ( qₖ ) − E t`

**中文旁白**：再往前一步，把作用量本身看成座標的函數，就得到漢彌頓－雅可比方程。變數能分離時，整個問題化成一串一維積分，這是求通解最有力的工具。

**English**: One step further, taking the action itself as a function of the coordinates, gives the Hamilton-Jacobi equation. When the variables separate, the whole problem falls apart into a chain of one-dimensional integrals: the most powerful route to a general solution.

**動畫**：同一張相空間圖：作用量當成座標的函數，就得到漢彌頓－雅可比方程。

---

## 第 9 拍｜一條原理，一整門力學

**畫面公式**：一條原理，一整門力學　/　one principle, one whole subject　/　`I = ∮ p dq / 2π = const          wᵢ = ωᵢ t + const`

**中文旁白**：最後是絕熱不變量：參數慢慢改變時，相軌跡圍出的面積不變；改用作用變數與角變數重寫，多自由度的有限運動就是條件週期運動。一條原理，加上空間與時間的對稱，長出了整座經典力學。

**English**: Last come the adiabatic invariants: when a parameter changes slowly, the area inside the phase path does not. In action and angle variables, finite motion with many degrees of freedom is conditionally periodic. One principle and a few symmetries: that is the whole subject.

**動畫**：七個章節方塊全部亮起：一條原理，加上空間與時間的對稱，長出了整座經典力學。

---
