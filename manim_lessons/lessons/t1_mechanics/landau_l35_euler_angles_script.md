# 第 35 課｜歐拉角：用三個角度描述剛體的方向（Landau §35）

Lesson 35 — Eulerian angles: three angles for the orientation of a rigid body

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l35_euler_angles.py`（`LandauL35ZH` / `LandauL35EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[35]` 與 `FORMULAS[35]`
- 配音：`manim_lessons/samples/audio_l35/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 3 分 03 秒、英文約 2 分 52 秒

整課共用同一張軸測投影圖：固定座標系 X、Y、Z（灰）與隨物體轉的 x₁、x₂、x₃（橘）共用一個原點。角度用取樣點畫的大圓弧表示，平面用取樣點畫的圓環表示。

---

## 第 0 拍｜兩個座標系

**畫面公式**：兩個座標系，共同原點　/　`X , Y , Z    ↔    x₁ , x₂ , x₃`

**中文旁白**：剛體的位置由質心的三個座標，加上三個決定方向的角度來描述。最常用的一組角度就是歐拉角。因為現在只關心座標軸之間的夾角，我們把固定座標系和跟著物體轉的座標系的原點放在一起。

**English**: The position of a rigid body is fixed by three coordinates for its centre of mass plus three angles for its orientation. The most convenient set of angles is the Eulerian angles. Since only the angles between the axes matter, we let both frames share one origin.

**動畫**：兩組座標軸從同一個原點射出，灰色的是固定座標系，橘色的是隨物體轉的座標系；整體緩慢飄移，讓立體感讀得出來。

---

## 第 1 拍｜節線

**畫面公式**：節線：兩個平面的交線　/　`ON ∥ z × x₃          ON ⊥ Z , ON ⊥ x₃`

**中文旁白**：跟著物體轉的那個平面，會和固定的水平面交出一條直線，這條線叫做節線。它同時垂直於固定的鉛直軸和物體的第三軸，正方向取成這兩個單位向量的叉積。

**English**: The plane carried by the body cuts the fixed horizontal plane along a straight line, the line of nodes. It is perpendicular to both the fixed vertical axis and the third axis of the body, and its positive direction is the cross product of those two unit vectors.

**動畫**：畫出固定的 XY 平面（灰色圓環）與物體的 x₁x₂ 平面（橘色圓環）；兩者的交線以紅色粗線標成 ON，並在 ON 與 Z、ON 與 x₃ 之間畫出直角記號。

---

## 第 2 拍｜三個歐拉角

**畫面公式**：三個歐拉角　/　`θ : 0 → π , φ : 0 → 2π , ψ : 0 → 2π`

**中文旁白**：三個歐拉角就這樣定出來：第一個角是鉛直軸和物體第三軸之間的夾角，第二個角是從固定的第一軸量到節線，第三個角是從節線量到物體的第一軸；後兩個角分別繞鉛直軸和物體第三軸，依右手螺旋的方向量。

**English**: The three Eulerian angles follow. The first is the angle between the vertical axis and the body's third axis. The second runs from the fixed first axis to the line of nodes, the third from the line of nodes to the body's first axis, each by the corkscrew rule.

**動畫**：三段圓弧同時出現並隨姿態變化：θ（青）從 Z 到 x₃、φ（紫）在 XY 平面內從 X 到節線、ψ（橘）在 x₁x₂ 平面內從節線到 x₁。右側以同樣的顏色列出三個角的定義。

---

## 第 3 拍｜三次接續的轉動

**畫面公式**：三次接續的轉動　/　`φ ⟳ Z      →      θ ⟳ ON      →      ψ ⟳ x₃`

**中文旁白**：所以任何一個方向，都可以由三次接續的轉動得到：先繞鉛直軸轉，把節線擺到位置上；再繞節線轉，把物體的軸壓下一個傾角；最後繞物體自己的軸轉過第三個角。

**English**: So any orientation is reached by three successive rotations: first about the vertical axis, which swings the line of nodes into place; then about the line of nodes, which tilts the body's axis down; and last about the body's own axis.

**動畫**：本課的關鍵動畫。兩個座標系從完全重合開始，依序做三次轉動，每 8 秒循環一次；右側三個步驟旁有一個白點標出目前正在轉的是哪一個角。

---

## 第 4 拍｜角速度的三個來源

**畫面公式**：角速度拆成三份，軸並不互相垂直　/　`Ω = (dθ/dt) ON + (dφ/dt) Z + (dψ/dt) x₃`

**中文旁白**：接下來把角速度用歐拉角寫出來。它可以拆成三份：傾角的變化率沿著節線，第二個角的變化率沿著固定的鉛直軸，第三個角的變化率沿著物體自己的軸。要注意這三根軸並不互相垂直。

**English**: Now write the angular velocity in these angles. It splits into three parts: the rate of the tilt along the line of nodes, the rate of the second angle along the fixed vertical axis, and the rate of the third along the body's own axis. These three axes are not perpendicular.

**動畫**：兩個平面圓環淡出，讓向量看得清楚。三支箭頭從原點射出：紅色沿節線、青色沿 Z、紫色沿 x₃，長度正比於各自的角度變化率；白色粗箭頭是三者的向量和 Ω。物體同時做穩定進動加自轉，傾角則來回章動，所以紅色箭頭會週期性地反向。

---

## 第 5 拍｜投影到物體的三根軸

**畫面公式**（三行）：`Ω₁ = (dφ/dt) sinθ sinψ + (dθ/dt) cosψ` ／ `Ω₂ = (dφ/dt) sinθ cosψ − (dθ/dt) sinψ` ／ `Ω₃ = (dφ/dt) cosθ + dψ/dt`

**中文旁白**：把這三份各自投影到物體的三根軸上再加起來，就得到角速度的三個分量。前兩個分量都同時混了傾角與進動的貢獻，第三個分量則是進動沿著物體軸的投影，再加上自轉。

**English**: Projecting each part onto the three body axes and adding them gives the components of the angular velocity. The first two each mix a tilt contribution with a precession contribution, while the third is the precession projected on the body axis plus the spin.

**動畫**：右側三條帶正負號的堆疊長條圖即時顯示 Ω₁、Ω₂、Ω₃，每一條由兩段組成——青色是 dφ/dt 的貢獻，紅色是 dθ/dt 的貢獻（Ω₃ 的第二段是紫色的 dψ/dt）。隨著 ψ 增加，可以直接看見 sinψ 與 cosψ 在兩條之間交換角色。

---

## 第 6 拍｜對稱陀螺的轉動動能

**畫面公式**：對稱陀螺的轉動動能　/　`T = ½ I₁ [ (dθ/dt)² + (dφ/dt)² sin²θ ] + ½ I₃ [ (dφ/dt) cosθ + dψ/dt ]²`

**中文旁白**：如果這三根軸取成慣性主軸，把這組式子代進轉動動能，就得到用歐拉角寫的動能。對稱陀螺的結果特別簡潔，因為垂直於對稱軸的那兩根主軸可以任意選。

**English**: If those axes are the principal axes of inertia, substituting into the rotational kinetic energy expresses it in Eulerian angles. For a symmetrical top the result is especially compact, because the two axes perpendicular to the symmetry axis may be chosen freely.

**動畫**：物體換上對稱陀螺的樣子——繞 x₃ 的兩個同心圓環。右側兩條長條圖即時顯示動能的兩個部分：½I₁ 的橫向部分與 ½I₃ 的沿軸部分。

---

## 第 7 拍｜把 x₁ 放到節線上

**畫面公式**：把 x₁ 取在節線上　/　`ψ = 0 ⟹ Ω₁ = dθ/dt , Ω₂ = (dφ/dt) sinθ , Ω₃ = (dφ/dt) cosθ + dψ/dt`

**中文旁白**：利用這個自由度，把物體的第一軸就取在節線上，也就是讓第三個角為零。這時三個分量變得非常簡單：第一個是傾角的變化率，第二個是進動率乘上傾角的正弦，第三個是進動沿著軸的投影加上自轉。

**English**: Using that freedom, put the body's first axis right on the line of nodes, so the third angle is zero. The components then become very simple: the rate of the tilt, the precession rate times the sine of the tilt, and the precession projected on the axis plus the spin.

**動畫**：ψ 設為零，x₁ 軸直接貼到紅色的節線上；右側列出化簡後的三個分量，顏色與前面的貢獻對應。

---

## 第 8 拍｜角動量的分量

**畫面公式**：取 Z 沿著守恆的角動量　/　`M₁ = I₁ (dθ/dt) , M₂ = I₁ (dφ/dt) sinθ , M₃ = I₃ Ω₃` ／ `M₁ = 0 , M₂ = M sinθ , M₃ = M cosθ`

**中文旁白**：拿它來重算對稱陀螺的自由轉動。把固定座標系的鉛直軸取在守恆的角動量方向上，再把物體的第一軸取在節線上。因為這根軸垂直於角動量，角動量的三個分量分別是零、大小乘正弦、大小乘餘弦。

**English**: Use this to redo the free motion of a symmetrical top. Take the vertical axis along the conserved angular momentum and the body's first axis along the line of nodes. Since that axis is perpendicular to the momentum, its components are zero, M sine theta, M cosine theta.

**動畫**：青色粗箭頭 M 沿著 Z 畫出，並以紫色（沿 x₃，M cosθ）與紅色（沿 x₂，M sinθ）畫出它的兩個分量，虛線補上直角關係。右側用一個平面直角三角形把同一件事再說一次：斜邊 M、鉛直邊 M cosθ、水平邊 M sinθ、夾角 θ。

---

## 第 9 拍｜回到規則進動

**畫面公式**：規則進動，與第 33 課一致　/　`dθ/dt = 0 , dφ/dt = M / I₁ , Ω₃ = ( M / I₃ ) cosθ`

**中文旁白**：比較兩組式子就得到三個結論：傾角完全不變，所以物體軸與角動量的夾角固定；進動率等於角動量除以第一個主慣量；自轉則等於角動量除以第三個主慣量，再乘上這個夾角的餘弦。這正是前兩課用幾何得到的規則進動。

**English**: Comparing the two sets gives three results: the tilt never changes, so the angle between the body axis and the angular momentum is constant; the precession rate is M over the first principal moment; and the spin is M over the third, times the cosine of that angle.

**動畫**：θ 鎖定成固定值，φ 以 M / I₁ 穩定增加、ψ 以 (M / I₃) cosθ 增加，於是 x₃ 軸掃出一個以 M 為軸的圓錐——圓錐的邊緣以灰色虛線圓標出。這正好重現第 33 課的規則進動。

---

## 製作備註

- 軸測投影用 `_p()`（EX、EY、EZ 三個螢幕基向量），角度弧與平面圓環都以取樣點 + `set_points_as_corners` 畫。
- 歐拉角採 z–x–z 慣例，`_frame()` 由 (φ, θ, ψ) 直接給出節線與三根物體軸；此慣例下 `z × x₃ ∝ ON`，與書上的正方向定義一致。
- 各拍的姿態由 `self.mode` 切換（`_ang()` / `_rates()` 依 mode 回傳不同的時間函數）。因為 manim 是在 `play()` 當下求值 updater，在每個 `run()` 之前設好 `self.mode` 與 `self.t0` 即可。
- 沿用第 34 課的教訓：`always_redraw` 裡一律不用 `DashedLine`，改用固定 `num_dashes` 的 `_dash()`。
- 第 4 拍起把兩個平面圓環淡出，否則向量會被圓環蓋住；第 8 拍起把節線淡出，因為 x₁ 已經躺在上面。
