# Landau Mechanics 33 — Angular momentum of a rigid body

> 《Landau–Lifshitz 經典力學》教學系列第 33 課（第六章「剛體運動」第三課，§33）
> 中文標題：角動量：為什麼 M 通常不平行於 Ω
> English title: Angular momentum: why M is usually not parallel to Ω

## 繁體中文旁白

剛體的角動量以質心為原點來定義最方便。把每個質點的速度換成角速度與位置向量的叉積，再代進角動量的定義，就得到一個只和角速度與質量分布有關的式子。

把這個二重叉積展開再整理成分量，括號裡出現的正是上一課的慣性張量。所以角動量的每個分量，都是慣性張量作用在角速度上：慣性張量把角速度映射成角動量。

用慣性主軸來寫最簡潔：角動量的三個分量，分別是三個主慣量乘上角速度的對應分量。

關鍵來了：三個分量各自被不同的主慣量放大，所以角動量一般不會和角速度同方向。只有球陀螺三個主慣量相等時兩者才恆平行，或者角速度剛好沿著某一根主軸時也平行。

現在看自由轉動。沒有外力矩時角動量守恆，大小和方向都固定在空間中。球陀螺因此角速度也固定，就是繞著空間中固定的一根軸等速轉動；轉子則是在一個平面內等速旋轉。

對稱陀螺就有趣了。因為垂直於對稱軸的兩根主軸可以任選，我們把第二根主軸取成垂直於角動量與對稱軸所張的平面；於是角動量的第二個分量為零，角速度的第二個分量也跟著為零。

這表示角動量、角速度與對稱軸永遠共面。角動量在空間中不動，所以這個平面繞著角動量轉；對稱軸因此掃出一個以角動量為軸的圓錐，這叫規則進動，同時陀螺還繞著自己的軸自轉。

兩個轉速都能直接寫出來：繞自己軸的自轉角速度，是角動量除以第三個主慣量再乘上夾角的餘弦；進動的角速度更簡單，就是角動量的大小除以第一個主慣量。

## English narration

The angular momentum of a rigid body is best defined about the centre of mass. Replacing each particle's velocity by the cross product of the angular velocity with its position vector builds it from the angular velocity and the mass distribution alone.

Expanding that double cross product and collecting components, the bracket which appears is exactly last lesson's inertia tensor. Each component of the angular momentum is the tensor acting on the angular velocity: the tensor maps omega to M.

In the principal axes it is simplest of all: the three components of the angular momentum are the three principal moments times the matching components of the angular velocity.

Here is the key point. Each component is stretched by a different principal moment, so the angular momentum is generally not parallel to the angular velocity. They stay parallel only for a spherical top, or when omega lies along a principal axis.

Now take free rotation. With no external torque the angular momentum is conserved, fixed in magnitude and direction. A spherical top then has a constant angular velocity, a uniform rotation about an axis fixed in space, and a rotator turns uniformly in one plane.

A symmetrical top is more interesting. The two principal axes perpendicular to the symmetry axis may be chosen freely, so we take the second one perpendicular to the plane holding M and the symmetry axis. Its component of M vanishes, and so does its component of omega.

So the angular momentum, the angular velocity and the symmetry axis always lie in one plane. M is fixed in space, so that plane turns about it and the symmetry axis sweeps out a circular cone: this is regular precession, while the top also spins about its own axis.

Both rates follow at once. The spin about the top's own axis is the angular momentum divided by the third principal moment, times the cosine of the angle; and the precession rate is simply the angular momentum divided by the first principal moment.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式與名稱顯示於上方（名稱依語言切換）；主畫面為動畫。

- 第 0 句 / line 0: `M = Σ m r × v  ,   v = Ω × r`
- 第 1 句 / line 1: `M = Σ m [ r² Ω − r ( r · Ω ) ] ／ Mᵢ = Iᵢₖ Ωₖ`
- 第 2 句 / line 2: `M₁ = I₁ Ω₁ ,   M₂ = I₂ Ω₂ ,   M₃ = I₃ Ω₃`
- 第 3 句 / line 3: `只有球陀螺才恆平行` / `parallel only for a spherical top` ＋ `I₁ = I₂ = I₃   ⟹   M = I Ω`
- 第 4 句 / line 4: `自由轉動：角動量守恆` / `free rotation: M is conserved` ＋ `dM/dt = 0     ⟹     M = const`
- 第 5 句 / line 5: `M、Ω 與對稱軸永遠共面` / `M, Ω and the symmetry axis stay coplanar` ＋ `M₂ = 0     ⟹     Ω₂ = 0`
- 第 6 句 / line 6: `規則進動：對稱軸繞 M 掃出圓錐` / `regular precession: the axis sweeps a cone about M` ＋ `Ω = Ωₚᵣ + Ω₃`
- 第 7 句 / line 7: `自轉與進動的角速度` / `the spin rate and the precession rate` ＋ `Ω₃ = ( M / I₃ ) cos θ    ,    Ωₚᵣ = M / I₁`

## 動畫 / Animation

第 0–3 句是「M、Ω 與對稱軸共面」那個平面的側視圖；第 4–7 句改用軸測投影呈現自由轉動與規則進動。

- 第 0 句：側視圖：畫面就是「對稱軸與角速度所張的平面」。細長的陀螺（長橢圓）擺在左側，質心 O 在中心，紫色箭頭是角速度 Ω，方向會在 13 度到 71 度之間來回掃描。三個質點畫出 r 向量，各自的速度 v = Ω × r 垂直於畫面，因此用紅色的 ⊙（指出畫面）與 ⊗（指入畫面）表示，圓圈大小正比於速度大小。
- 第 1 句：青色的角動量 M 出現：它由同一個角速度算出，但方向明顯和 Ω 不同。
- 第 2 句：畫出兩根慣性主軸 x₃（對稱軸）與 x₁，並用虛線把 Ω 與 M 投影到兩根軸上；右側長條圖即時比較 Ω₃ 與 M₃ = I₃Ω₃（乘 0.45 變短）、Ω₁ 與 M₁ = I₁Ω₁（乘 1.00 不變），一眼看出「不同分量被不同倍率拉伸」。
- 第 3 句：在 Ω 與 M 之間畫出紅色夾角弧，強調兩者不平行；右側出現球陀螺：M（粗青）與 Ω（紫）完全同向。
- 第 4 句：自由轉動的兩個簡單情形：左邊球陀螺繞空間中固定的軸等速自轉（赤道上的紅點顯示自轉），右邊轉子在畫面平面內等速旋轉，其 M 與 Ω 垂直畫面（⊙ 記號）。
- 第 5 句：換成軸測投影：質心固定，青色 M 垂直向上，橘色為陀螺的對稱軸與轉子環，紫色為 Ω。灰色三角形是 M 與對稱軸所張的平面，第二根主軸 x₂ 垂直於這個平面（灰箭頭），θ 弧標出 M 與對稱軸的夾角。
- 第 6 句：開始進動：整個平面繞 M 旋轉，對稱軸沿著虛線圓錐掃一圈；轉子上的紅點同時以 (I₁/I₃)cos θ 倍的速率自轉，兩個轉速的比值與公式一致。
- 第 7 句：在進動中加上分解：紫色虛線顯示 Ω = Ωₚᵣ（沿 M）+ Ω₃（沿對稱軸）。

陀螺取 I₁ = 1.00、I₃ = 0.45（長條形的對稱陀螺），夾角 θ = 35°。畫面上的進動速率與自轉速率之比直接由 Ω₃/Ωₚᵣ = (I₁/I₃)cos θ 設定，所以動畫中兩個轉速的關係就是 §33 的兩條公式。
