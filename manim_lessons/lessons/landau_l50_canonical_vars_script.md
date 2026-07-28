# 第 50 課｜正則變數：作用變數與角變數（Landau §50）

Lesson 50 — Canonical variables: the action variable and the angle variable

- 場景檔：`manim_lessons/lessons/landau_l50_canonical_vars.py`（`LandauL50ZH` / `LandauL50EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[50]` 與 `FORMULAS[50]`
- 配音：`manim_lessons/samples/audio_l50/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 34 秒、英文約 2 分 24 秒

整堂課只用一張圖：一條歪斜的封閉相軌跡，加上一個與它面積相同的虛線圓。相軌跡上的點跑得忽快忽慢，圓上的指針——角變數——卻是勻速轉動，兩者鎖在一起。於是每一句話都變成看得見的東西：陰影是簡略作用量在累積，指針轉一圈就是那個 2π，最後幾拍參數隨時間變化，軌跡的形狀變了，圓卻沒動。

---

## 第 0 拍｜把 I 當成新的動量

**畫面公式**：把 I 當成新的動量　/　take I as the new momentum　/　`( q , p )     ⟶     ( w , I )`

**中文旁白**：現在把參數固定住，系統又是封閉的。我們來做一個正則變換，把上一課那個絕熱不變量本身當成新的「動量」。

**English**: Now hold the parameter fixed, so the system is closed again. We make a canonical transformation that takes the adiabatic invariant of the last lesson as the new momentum.

**動畫**：相平面上一條明顯不是圓的封閉軌跡，這就是 λ 固定時系統走的路。

---

## 第 1 拍｜生成函數是簡略作用量

**畫面公式**：生成函數是簡略作用量　/　the generating function is the abbreviated action　/　`S₀ ( q , E ; λ ) = ∫ p ( q , E ; λ ) dq`

**中文旁白**：生成函數就取簡略作用量：動量沿著座標的積分，在給定的能量與參數下計算。

**English**: The generating function is the abbreviated action: the integral of the momentum over the coordinate, computed for a given energy and a given parameter.

**動畫**：陰影從左邊的迴轉點開始往右掃過上半支：掃過的面積就是簡略作用量 ∫ p dq。

---

## 第 2 拍｜第一條正則變換公式

**畫面公式**：第一條正則變換公式　/　the first transformation formula　/　`I = I ( E )     ⟹     S₀ = S₀ ( q , I ; λ )        p = ∂S₀/∂q`

**中文旁白**：對封閉系統，那個不變量只是能量的函數，所以簡略作用量同樣可以寫成座標和它的函數；而且固定能量微分與固定它微分是同一回事。於是動量就等於簡略作用量對座標的偏導數。

**English**: For a closed system the invariant is a function of the energy alone, so the abbreviated action can also be written through the coordinate and the invariant. Differentiating at fixed energy is then the same as at fixed invariant, and the momentum is that derivative.

**動畫**：同一張圖：陰影的高度就是動量，也就是簡略作用量對座標的偏導數。

---

## 第 3 拍｜第二條給出角變數

**畫面公式**：第二條給出角變數　/　the second gives the angle variable　/　`w = ∂S₀ ( q , I ; λ ) / ∂I`

**中文旁白**：正則變換的第二條公式給出新的「座標」，我們叫它角變數。這一對變數就叫正則變數：一個是作用變數，一個是角變數。

**English**: The second formula of the canonical transformation supplies the new coordinate, which we call the angle variable. Together the two are the canonical variables: one action variable and one angle variable.

**動畫**：與軌跡面積相同的虛線圓出現，圓心拉出一根指針，指針與 x 軸的夾角就是角變數 w。

---

## 第 4 拍｜新的哈密頓量就是 E ( I )

**畫面公式**：新的哈密頓量就是 E ( I )　/　the new Hamiltonian is just E of I　/　`H′ = E ( I )        dI/dt = 0   ,   dw/dt = dE ( I ) / dI`

**中文旁白**：生成函數不顯含時間，所以新的哈密頓量就是原來的能量，只是改用作用變數表示。於是運動方程變得極簡單：作用變數的時間導數是零，角變數的時間導數是能量對作用變數的導數。

**English**: The generating function has no explicit time, so the new Hamiltonian is just the old energy written through the action variable. Hamilton's equations become very simple: the action variable has zero time derivative, and the angle variable has the derivative of the energy.

**動畫**：兩個點同時走：軌跡上的點忽快忽慢，圓上的指針勻速——這正是新的哈密頓量只含 I 的結果。

---

## 第 5 拍｜角變數隨時間線性增加

**畫面公式**：角變數隨時間線性增加　/　the angle variable grows linearly in time　/　`w = ω ( I ) t + const        ω = dE/dI`

**中文旁白**：第一條說作用變數是常數，本來就該如此。第二條說角變數是時間的線性函數：頻率乘時間再加一個常數。它正是振盪的相位。

**English**: The first says the action variable is constant, as it should be. The second says the angle variable is a linear function of time: the frequency times the time, plus a constant. It is the phase of the oscillation.

**動畫**：指針持續勻速轉動，說明角變數是時間的線性函數。

---

## 第 6 拍｜繞一圈：S₀ 加 2π I，w 加 2π

**畫面公式**：繞一圈：S₀ 加 2π I，w 加 2π　/　one turn: S₀ by two pi I, w by two pi　/　`ΔS₀ = 2π I     ⟹     Δw = ∂ ( ΔS₀ ) / ∂I = 2π`

**中文旁白**：簡略作用量是座標的多值函數：每繞一個週期，它就增加二π乘上作用變數。因此同一段時間裡，角變數剛好增加二π。

**English**: The abbreviated action is a many-valued function of the coordinate: over each period it increases by two pi times the action variable. In that same time, therefore, the angle variable increases by exactly two pi.

**動畫**：一道紅色的圓弧從指針目前的位置開始，剛好掃滿一整圈：S₀ 增加 2π I，w 增加 2π。

---

## 第 7 拍｜單值函數是 w 的週期函數

**畫面公式**：單值函數是 w 的週期函數　/　a one-valued function is periodic in w　/　`F ( q , p ) = F ( w + 2π , I )`

**中文旁白**：反過來說，把座標和動量、或任何它們的單值函數改用正則變數表示，角變數增加二π時它們都回到原值。也就是說，任何單值函數都是角變數的週期函數，週期是二π。

**English**: Conversely, write the coordinate and momentum, or any one-valued function of them, in canonical variables, and they return to their old values when the angle variable increases by two pi. Every one-valued function is periodic in the angle variable with period two pi.

**動畫**：指針回到原處，軌跡上的點也回到原處：單值函數以 2π 為週期。

---

## 第 8 拍｜如果 λ 隨時間變

**畫面公式**：如果 λ 隨時間變　/　if λ does depend on the time　/　`H′ = E ( I ; λ ) + Λ ( dλ/dt )        Λ = ( ∂S₀/∂λ )_I`

**中文旁白**：如果參數隨時間變化，同樣的變換照樣可以做，只是生成函數現在顯含時間。新的哈密頓量因此多出一項：能量再加上一個量乘上參數的變化率，那個量是簡略作用量在固定作用變數下對參數的偏導數。

**English**: If the parameter does depend on time, the same transformation still works, but the generating function now contains the time explicitly. So the new Hamiltonian gains a term: the energy, plus a quantity times the rate of change of the parameter.

**動畫**：參數開始隨時間變化，封閉軌跡的形狀慢慢改變，虛線圓卻維持原來的大小。

---

## 第 9 拍｜正則變數裡的運動方程

**畫面公式**：正則變數裡的運動方程　/　the equations in canonical variables　/　`dI/dt = − ( ∂Λ/∂w ) ( dλ/dt )      dw/dt = ω + ( ∂Λ/∂I ) ( dλ/dt )`

**中文旁白**：運動方程於是變成：作用變數的變化率等於那個量對角變數的偏導數乘上參數變化率再取負號；角變數的變化率則是頻率再加一個小修正。對頻率緩變的諧振子，座標與動量就是正弦與餘弦，那個量正比於二倍角的正弦。

**English**: The equations become these: the action variable changes at minus the derivative of that quantity by the angle, times the rate of change of the parameter, while the angle variable runs at the frequency plus a small correction. For an oscillator it goes as the sine of twice the angle.

**動畫**：形狀繼續變形，圓仍然不動：作用變數的變化只來自那個小小的修正項。

---
