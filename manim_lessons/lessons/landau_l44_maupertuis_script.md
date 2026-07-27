# 第 44 課｜莫佩爾蒂原理：只問路徑，不問時間（Landau §44）

Lesson 44 — Maupertuis' principle: the path without the time

- 場景檔：`manim_lessons/lessons/landau_l44_maupertuis.py`（`LandauL44ZH` / `LandauL44EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[44]` 與 `FORMULAS[44]`
- 配音：`manim_lessons/samples/audio_l44/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 12 秒、英文約 2 分 16 秒

兩張圖。先是兩個固定端點之間的一束路徑，真實那條上串著等時間間隔的珠子——第 1 拍把珠子拿掉，拿掉的正是這個原理所拋棄的資訊；再來是 (44.10) 的收穫：質點越過交界進入位能較低的區域時像光線一樣折射，因為根號下 E 減 U 扮演的就是折射率。

---

## 第 0 拍｜完整的運動：路徑加上時刻

**畫面公式**：完整的運動：路徑加上時刻　/　the whole motion: the path and the timing　/　`H ( p , q ) = E = const`

**中文旁白**：最小作用量原理決定了整個運動：解出運動方程，我們既知道路徑的形狀，也知道什麼時刻走到哪裡。

**English**: The principle of least action determines the motion completely: solving the equations it gives us both the shape of the path and the position along it as a function of time.

**動畫**：兩個固定端點之間的真實路徑，上面串著等時間間隔的珠子，標出「什麼時刻走到哪裡」。

---

## 第 1 拍｜只想知道路徑的形狀

**畫面公式**：只想知道路徑的形狀　/　we want only the shape of the path　/　`δS = − H δt`

**中文旁白**：但如果問題比較簡單，只想知道路徑長什麼樣子，不管時間，就可以用一個簡化過的形式。

**English**: But if the problem is the more restricted one of finding only the path, with no reference to time, a simplified form of the principle can be used.

**動畫**：珠子消失，另外三條灰色的試探路徑出現——現在只關心路徑的形狀。

---

## 第 2 拍｜讓抵達的時刻可以變動

**畫面公式**：讓抵達的時刻可以變動　/　let the final time vary　/　`δS + E δt = 0`

**中文旁白**：先假設拉格朗日量不顯含時間，所以能量守恆。讓終點的時刻可以變動，位置固定，上一課告訴我們作用量的變分等於負的哈密頓量乘上時刻的變分。

**English**: Assume first that the Lagrangian, and so the Hamiltonian, does not contain the time, so the energy is conserved. Letting the final time vary with the coordinates held fixed, the last lesson gave the variation of the action as minus the Hamiltonian times the variation of the time.

**動畫**：路徑下方標出：所有拿來比較的路徑，能量都等於 E。

---

## 第 3 拍｜只比較能量相同的運動

**畫面公式**：只比較能量相同的運動　/　compare only paths of equal energy　/　`S = S₀ − E t          S₀ = ∫ Σ pᵢ dqᵢ`

**中文旁白**：現在只比較那些滿足能量守恆的運動。對這些路徑，哈密頓量就是常數 E，於是變分關係變成作用量的變分加上 E 乘時刻的變分等於零。

**English**: Now compare only those motions that satisfy conservation of energy. For such paths the Hamiltonian is the constant E, and the relation becomes the variation of the action plus E times the variation of the time equals zero.

**動畫**：同一束路徑，右側寫出 δS + E δt = 0。

---

## 第 4 拍｜兩項抵消，只剩簡略作用量

**畫面公式**：兩項抵消，只剩簡略作用量　/　the terms cancel, leaving the abbreviated action　/　`δS₀ = 0`

**中文旁白**：把作用量寫成簡略作用量減去 E 乘時間，代進去，兩項互相抵消，只剩下一句話：簡略作用量的變分等於零。

**English**: Write the action as the abbreviated action minus E times the time. Substituting, the two terms cancel and one statement is left: the variation of the abbreviated action vanishes.

**動畫**：同一束路徑：兩個 E δt 項互相抵消，只剩簡略作用量的變分為零。

---

## 第 5 拍｜簡略作用量取極小

**畫面公式**：簡略作用量取極小　/　the abbreviated action is least　/　`pᵢ = ∂L/∂q̇ᵢ        E ( q , dq/dt ) = E`

**中文旁白**：簡略作用量就是動量沿著路徑對座標的積分。所以在所有滿足能量守恆、而且通過終點的路徑裡，不管什麼時候抵達，真實的那一條讓這個積分取極小。

**English**: The abbreviated action is the integral of momentum along the path. So among all paths that conserve the energy and pass through the final point, whenever they arrive, the true one makes that integral least.

**動畫**：同一束路徑，強調真實那條讓 ∫Σp dq 取極小。

---

## 第 6 拍｜把動量用座標與其微分表示

**畫面公式**：把動量用座標與其微分表示　/　the momenta through q and dq　/　`S₀ = ∫ √[ 2 ( E − U ) Σ aᵢₖ dqᵢ dqₖ ]`

**中文旁白**：要真的用它，必須把動量用座標和座標的微分表示出來。辦法是用動量的定義，再用能量守恆把時間的微分消掉。

**English**: To use this we must express the momenta through the coordinates and their differentials. We do it with the definition of momentum, using conservation of energy to eliminate the differential of the time.

**動畫**：同一束路徑：用動量的定義與能量守恆把 dt 消掉。

---

## 第 7 拍｜動能減位能的情形

**畫面公式**：動能減位能的情形　/　for kinetic minus potential energy　/　`δ ∫ √[ 2 m ( E − U ) ] dl = 0`

**中文旁白**：對通常的拉格朗日量，也就是動能減位能，算出來的結果是：簡略作用量等於根號下二倍的能量減位能，再乘上動能的那個二次型。

**English**: For the usual Lagrangian, kinetic minus potential energy, the result is that the abbreviated action is the integral of the square root of twice the energy minus the potential, times the quadratic form of the kinetic energy.

**動畫**：同一束路徑，寫出動能減位能情形下的簡略作用量。

---

## 第 8 拍｜單個質點：雅可比形式

**畫面公式**：單個質點：雅可比形式　/　one particle: Jacobi's form　/　`U = 0     ⟹     δ ∫ dl = 0`

**中文旁白**：對單個質點，動能是二分之一質量乘速度平方，變分原理就變成：根號下二倍質量乘能量減位能，沿著路徑長度的積分取極小。這個形式是雅可比給的。

**English**: For a single particle the kinetic energy is one-half m v squared, and the principle becomes the integral of the square root of twice the mass times the energy minus the potential, taken along the element of path length. This form is due to Jacobi.

**動畫**：同一束路徑：單個質點沿路徑長度積分的雅可比形式。

---

## 第 9 拍｜√(E − U) 就是折射率

**畫面公式**：√(E − U) 就是折射率　/　the square root of E minus U is an index　/　`∂S₀/∂E = t − t₀`

**中文旁白**：自由運動時位能為零，積分就退化成路徑長度，質點走兩點間最短的路，也就是直線。有位能時，根號下能量減位能就扮演光學裡折射率的角色，路徑會彎——力學與幾何光學在這裡完全平行。

**English**: In free motion the potential vanishes and the integral is just the path length, so the particle takes the shortest route between two points: a straight line. With a potential, the square root of the energy minus the potential acts as a refractive index and the path bends.

**動畫**：換成折射圖：上下兩個位能不同的區域，青色入射線在交界上折成紅色的出射線，虛線是法線——路徑像光線一樣折射。

---
