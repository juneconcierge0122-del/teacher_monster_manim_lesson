# 第 36 課｜歐拉方程：在動座標系裡寫運動方程（Landau §36）

Lesson 36 — Euler's equations: the equations of motion in the moving frame

- 場景檔：`manim_lessons/lessons/landau_l36_euler_equations.py`（`LandauL36ZH` / `LandauL36EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[36]` 與 `FORMULAS[36]`
- 配音：`manim_lessons/samples/audio_l36/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中英文都約 2 分 35 秒

和第 35 課相反：這一課整個站在**物體座標系**裡，所以三根主軸在畫面上是靜止的，動的是角速度向量。

---

## 第 0 拍｜為什麼要換座標系

**畫面公式**：只有在慣性主軸上才這麼簡單　/　`M₁ = I₁ Ω₁ , M₂ = I₂ Ω₂ , M₃ = I₃ Ω₃`

**中文旁白**：上一課的運動方程寫在固定座標系裡，但角動量和角速度之間最簡單的關係，出現在跟著物體轉、而且沿著慣性主軸的座標系裡。所以我們要先把方程換到動座標系。

**English**: The equations of motion of the last lesson refer to the fixed frame, but the simplest relation between angular momentum and angular velocity holds in the moving frame along the principal axes. So we first transform them to the moving coordinates.

**動畫**：三根主軸上畫出角速度 Ω（紫）與角動量 M（青），兩者明顯不平行——正是第 33 課的結論。右側對比「固定座標系：dM/dt = K」與「主軸座標系：Mᵢ = Iᵢ Ωᵢ」。

---

## 第 1 拍｜轉換規則

**畫面公式**：固定在物體上的向量，只會被轉動帶著走　/　`dA/dt = d′A/dt + Ω × A`

**中文旁白**：任何一個向量都適用同一條規則。如果這個向量在動座標系裡不變，它在固定座標系裡的變化就純粹來自轉動，等於角速度和它的叉積；一般情況再加上它在動座標系裡自己的變化率。

**English**: One rule covers any vector. If the vector does not change in the moving frame, its rate of change in the fixed frame comes purely from the rotation, and equals the cross product of the angular velocity with it. In general we add its own rate in the moving frame.

**動畫**：一支釘在物體上的向量 A 繞著 Ω 掃出圓錐，尖端沿虛線圓周走；紅色箭頭 Ω × A 永遠與圓周相切，正是尖端的速度。

---

## 第 2 拍｜用到 P 與 M 上

**畫面公式**：把規則用到 P 與 M 上　/　`d′P/dt + Ω × P = F          d′M/dt + Ω × M = K`

**中文旁白**：把這條規則用到動量和角動量上，兩條運動方程就變成：在動座標系裡的變化率，加上角速度和該向量的叉積，等於力或者力矩。

**English**: Applying that rule to the momentum and the angular momentum, the two equations of motion become: the rate of change in the moving frame, plus the cross product of the angular velocity with that vector, equals the force or the torque.

**動畫**：右上列出兩條方程，右下用一個向量三角形說明一般情況：d′A/dt（青）接上 Ω × A（紅），合起來就是 dA/dt（白）。

---

## 第 3 拍｜分量與指標輪換

**畫面公式**：三條方程只是指標的輪換　/　`μ ( dV₁/dt + Ω₂ V₃ − Ω₃ V₂ ) = F₁       ( 1 → 2 → 3 → 1 )`

**中文旁白**：第一條取分量、並把動量寫成質量乘速度，就得到三條方程。每一條裡都出現一個角速度分量乘上一個速度分量，這正是叉積帶來的。

**English**: Taking components of the first, with the momentum written as mass times velocity, gives three equations. Each carries a product of one angular velocity component with one velocity component, which is exactly what the cross product contributes.

**動畫**：右側列出三行叉積分量，一個白點依序在三行之間跳動，把 1 → 2 → 3 → 1 的輪換講清楚。

---

## 第 4 拍｜歐拉方程

**畫面公式**：乘積項就是 Ω × M 的分量　/　`I₁ dΩ₁/dt + ( I₃ − I₂ ) Ω₂ Ω₃ = K₁` ／ `I₂ dΩ₂/dt + ( I₁ − I₃ ) Ω₃ Ω₁ = K₂ ,   I₃ dΩ₃/dt + ( I₂ − I₁ ) Ω₁ Ω₂ = K₃`

**中文旁白**：第二條在主軸上最漂亮：角動量的每個分量，就是主慣量乘上對應的角速度分量。代進去整理，就得到歐拉方程；裡面的乘積項全都來自那個叉積。

**English**: The second is prettiest in the principal axes, where each component of the angular momentum is a principal moment times the matching component of the angular velocity. Substituting gives Euler's equations, whose product terms come from that cross product.

**動畫**：左邊在 Ω 與 M 之間補上紅色的 Ω × M；右邊同樣用跳動的白點列出三個乘積項，並標明它們就是 ( Ω × M )ᵢ。

---

## 第 5 拍｜自由轉動與 polhode

**畫面公式**：非對稱陀螺：Ω 在物體上畫出一條閉曲線　/　`K = 0 ⟹ dΩ₁/dt = − ( I₃ − I₂ ) Ω₂ Ω₃ / I₁      ( 1 → 2 → 3 → 1 )`

**中文旁白**：如果沒有外力矩，右邊全部為零，三條方程就只剩下角速度自己。這三個分量彼此耦合：任何一個的變化率，都由另外兩個的乘積決定。

**English**: With no external torque the right-hand sides vanish and the three equations involve only the angular velocity. The components stay coupled: the rate of change of any one is set by the product of the other two.

**動畫**：這一拍的軌跡是**真的解出來的**——以 I = (1.0, 1.7, 2.6)、Ω₀ = (0.55, 0.30, 0.80) 對無力矩的歐拉方程做 RK4 積分（在 import 時算一次），得到繞 x₃ 的閉合 polhode，週期約 8.8 秒。Ω 箭頭的尖端就沿著這條灰色曲線跑。

---

## 第 6 拍｜對稱陀螺：Ω₃ 是常數

**畫面公式**：對稱陀螺：沿軸的分量是常數　/　`I₁ = I₂ ⟹ dΩ₃/dt = 0 , Ω₃ = const`

**中文旁白**：拿對稱陀螺來試。兩個橫向主慣量相等，第三條方程的乘積項就消失，於是沿對稱軸的那個角速度分量是個常數。

**English**: Try a symmetrical top. The two transverse principal moments are equal, so the product term in the third equation drops out, and the component of the angular velocity along the symmetry axis is constant.

**動畫**：polhode 換成一個標準的圓：Ω 的尖端在固定高度上繞 x₃ 畫圓。青色的 Ω₃ 箭頭固定不動，橘色虛線標出從軸到尖端的橫向部分。

---

## 第 7 拍｜耦合的一對方程

**畫面公式**：兩個橫向分量互相驅動　/　`dΩ₁/dt = − ω Ω₂ , dΩ₂/dt = ω Ω₁` ／ `ω = Ω₃ ( I₃ − I₁ ) / I₁`

**中文旁白**：剩下兩條變成一對簡單的耦合方程：第一個分量的變化率等於負的頻率乘第二個分量，第二個的變化率等於頻率乘第一個。這個頻率由沿軸的分量和兩個主慣量的差決定。

**English**: The remaining two become a simple coupled pair: the rate of the first component is minus a frequency times the second, and the rate of the second is that frequency times the first. The frequency is set by the axial component and the difference of the moments.

**動畫**：右側開一個 (Ω₁, Ω₂) 平面，向量的尖端沿著虛線圓等速轉動，直接看出 A = √(Ω₁² + Ω₂²) 是定值。

---

## 第 8 拍｜解：餘弦與正弦

**畫面公式**：橫向部分大小固定，等速旋轉　/　`Ω₁ = A cos ωt , Ω₂ = A sin ωt , A = √( Ω₁² + Ω₂² )`

**中文旁白**：解出來就是一個等速旋轉：第一個分量是振幅乘餘弦，第二個是同樣的振幅乘正弦。所以角速度垂直於對稱軸的那一部分，大小固定，並以這個頻率繞著對稱軸轉。

**English**: The solution is a uniform rotation: the first component is an amplitude times a cosine, the second the same amplitude times a sine. So the part of the angular velocity across the symmetry axis keeps a fixed magnitude and turns about that axis at this frequency.

**動畫**：右側換成兩條波形，Ω₁ 是餘弦（橘）、Ω₂ 是正弦（青），兩個小圓點同步移動，相位差正好四分之一週期。

---

## 第 9 拍｜從物體上看到的規則進動

**畫面公式**：從物體上看到的規則進動　/　`| Ω | = const , Ω ⟳ x₃ , ω = Ω₃ ( I₃ − I₁ ) / I₁`

**中文旁白**：再加上沿軸的分量也是常數，結論就是：在跟著物體轉的座標系裡看，角速度的大小不變，並繞著物體自己的對稱軸等速旋轉，角動量也做同樣的運動。這就是前兩課的規則進動，只是換成從物體上看。

**English**: Since the axial component is constant too, in the frame turning with the body the angular velocity keeps its magnitude and rotates uniformly about the body's own symmetry axis, and so does the angular momentum. It is the regular precession seen from the body.

**動畫**：Ω 拖出一條紫色的尾跡，沿著圓錐繞 x₃ 轉。右側把兩種觀點並排：物體座標系裡 Ω 繞 x₃ 轉，固定座標系（第 33 課）裡 x₃ 繞 M 轉——同一個運動的兩種看法。

---

## 製作備註

- **第 5 拍的 polhode 是真的積分出來的**：`_polhode()` 在 import 時用 RK4 解一次無力矩的歐拉方程，存成陣列給 updater 查表。這樣既真實又可重現，也不會有逐格積分的漂移。2T 與 |M|² 在整段軌跡上守恆到 12 位數。
- 初始條件要挑**離分界線夠遠**的：一開始用 Ω₀ = (0.92, 0.30, 0.52) 時 |M|² 只比 2T·I₂ 大一點點，軌跡幾乎貼著分界線橫掃整個球面，畫面亂成一團；改成 (0.55, 0.30, 0.80) 之後才是一條乾淨的閉曲線。
- 各拍的運動一樣用 `self.mode` 分派（見第 35 課的備註）。
- **三行公式的下緣壓得很低**：第 4 拍的公式共三行，x₃ 的軸標籤本來放在軸尖正上方會被壓到，改成放在軸尖**右側**（offset 從 (0.02, 0.20) 改成 (0.26, 0.02)）並把軸長縮到 1.32 才淨空。
- 英文標籤寬度務必逐條量：本課第 9 拍原本三行英文都超出 x = 6.3，其中一行直接被畫面切掉。用一個覆寫 `_row()` / `_txt()` 並印出 `get_right()` 的 subclass 跑一次 `-s`，一次就能抓出全部。
