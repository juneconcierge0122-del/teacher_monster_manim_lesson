# 第 37 課｜非對稱陀螺：橢球與球面交出的路徑（Landau §37）

Lesson 37 — The asymmetrical top: paths cut by an ellipsoid and a sphere

- 場景檔：`manim_lessons/lessons/landau_l37_asym_top.py`（`LandauL37ZH` / `LandauL37EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[37]` 與 `FORMULAS[37]`
- 配音：`manim_lessons/samples/audio_l37/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 57 秒、英文約 2 分 35 秒

全課共用一張圖：M 空間裡的能量橢球、常數 |M| 的球面，以及兩者交出的曲線族——也就是 Landau 的 Fig. 51。

---

## 第 0 拍｜兩個守恆量

**畫面公式**：三個主慣量都不同，而且沒有外力矩　/　`I₃ > I₂ > I₁ , K = 0`

**中文旁白**：現在把歐拉方程用到最複雜的情形：三個主慣量都不相同的非對稱陀螺，而且沒有外力矩。為了確定，我們把三個主慣量由小到大排好。這時已經有兩個守恆量可以用：能量，還有角動量的大小。

**English**: Now apply Euler's equations to the hardest case: a free asymmetrical top, whose three principal moments are all different. For definiteness we order them from smallest to largest. Two integrals are already available: the energy and the magnitude of M.

**動畫**：三根慣性主軸，右側列出兩個守恆量。

---

## 第 1 拍｜橢球面與球面

**畫面公式**：能量給橢球面，角動量給球面　/　`M₁²/I₁ + M₂²/I₂ + M₃²/I₃ = 2E` ／ `M₁² + M₂² + M₃² = M²`

**中文旁白**：把這兩個守恆律用角動量的分量寫出來。能量守恆給出一個橢球面，三個半軸分別是二倍能量乘上各個主慣量再開根號；角動量守恆給出一個球面，半徑就是角動量的大小。

**English**: Write both conservation laws in the components of the angular momentum. Energy conservation gives an ellipsoid whose three semiaxes are the square roots of twice the energy times each principal moment. Conservation of M gives a sphere of radius M.

**動畫**：灰色線框畫出能量橢球，青色線框畫出常數 |M| 的球面，兩者同心疊在一起。

---

## 第 2 拍｜交線就是 M 的路徑

**畫面公式**：M 的尖端走在兩個面的交線上　/　`2E I₁ < M² < 2E I₃`

**中文旁白**：所以角動量向量的尖端，必須同時待在橢球面和球面上，也就是走在這兩個面的交線上。要有交線，球的半徑必須落在橢球最短和最長的半軸之間。

**English**: So the tip of the angular momentum must lie on the ellipsoid and on the sphere at once, which means it travels along their curve of intersection. For that curve to exist, the radius of the sphere must fall between the shortest and longest semiaxes.

**動畫**：交線以紅色描出（一對繞 x₁ 的閉圈），青色的 M 箭頭尖端就在其中一圈上移動。

---

## 第 3 拍｜整族路徑（Fig. 51）

**畫面公式**：固定能量、改變 M：一整族路徑　/　`M² → 2E I₁ ⟳ x₁          M² = 2E I₂          M² → 2E I₃ ⟳ x₃`

**中文旁白**：固定能量、改變角動量的大小，這些交線會怎麼變？角動量最小時，是繞著最小主軸的兩個小圈；角動量變大，圈也跟著變大；到某個臨界值時，它們變成兩條通過中間主軸的平面曲線；再大下去，就變成繞著最大主軸的兩個小圈。

**English**: Keep the energy fixed and vary M. At the smallest M the intersections are two little loops about the axis of least moment; as M grows they widen; at one critical value they become plane curves through the middle axis; beyond that, loops about the greatest axis.

**動畫**：整族 polhode 一次畫出（紫色），分界線以紅色加粗——正是書上 Fig. 51 的圖。

---

## 第 4 拍｜封閉即週期

**畫面公式**：路徑封閉 ⇒ 相對於物體是週期運動　/　`M ( t + T ) = M ( t )`

**中文旁白**：這些路徑都是閉曲線，所以角動量相對於物體的運動是週期的：走完一圈，它會回到原來的位置，中間掃出一個錐面。

**English**: All these paths are closed, so the motion of the angular momentum relative to the body is periodic: after one circuit it returns to where it started, having swept out a conical surface.

**動畫**：從原點拉出一把等間隔的細線連到路徑上的過去位置，隨著 M 前進掃出錐面。

---

## 第 5 拍｜中間軸不穩定

**畫面公式**：中間那根軸不穩定　/　`x₁ , x₃ ✓          x₂ ✗`

**中文旁白**：但是靠近三根軸的路徑，性質很不一樣。靠近最小和最大主軸的路徑，整條都待在那根軸附近；而經過中間主軸的路徑，卻會跑到離它很遠的地方。這就是為什麼繞最小和最大主軸的轉動是穩定的，繞中間那根軸卻不穩定。

**English**: But the paths near the three axes differ sharply. Those near the least and greatest axes stay entirely close to them, while the ones through the middle axis run far away. That is why rotation about the least and greatest axes is stable, and the middle one is not.

**動畫**：兩條真實積分出來的軌跡並列：青色那條從 x₁ 旁邊出發，整條都黏在 x₁ 附近；紅色那條從 x₂ 旁邊出發（只偏了千分之一），卻繞到球面的另一側去。這就是網球拍定理。

---

## 第 6 拍｜消去兩個分量

**畫面公式**：用兩個守恆律消掉兩個分量　/　`Ω₁² = [ ( 2E I₃ − M² ) − I₂ ( I₃ − I₂ ) Ω₂² ] / I₁ ( I₃ − I₁ )` ／ `Ω₃² = [ ( M² − 2E I₁ ) − I₂ ( I₂ − I₁ ) Ω₂² ] / I₃ ( I₃ − I₁ )`

**中文旁白**：要算出隨時間的變化，就回到歐拉方程。先用兩個守恆律，把第一個和第三個角速度分量用第二個表示出來，代進第二條歐拉方程，就只剩一條只含第二個分量的一階方程。

**English**: For the time dependence we go back to Euler's equations. The two conservation laws give the first and third components in terms of the second; substituting into the second Euler equation leaves one first-order equation in that component alone.

---

## 第 7 拍｜橢圓積分

**畫面公式**：積出來是橢圓積分　/　`τ = ∫ ds / √[ ( 1 − s² ) ( 1 − k² s² ) ]     ⟹     s = sn τ`

**中文旁白**：把它積分，得到的是一個橢圓積分。換成適當的無因次變數，並定義一個介於零和一之間的模數，這個積分就是標準形式；把它反過來解，就得到雅可比橢圓函數。

**English**: Integrating it gives an elliptic integral. In suitable dimensionless variables, with a modulus between zero and one, the integral takes its standard form, and inverting it gives a Jacobian elliptic function.

---

## 第 8 拍｜cn、sn、dn

**畫面公式**：三個雅可比橢圓函數　/　`Ω₁ ∝ cn τ , Ω₂ ∝ sn τ , Ω₃ ∝ dn τ        τ : 4K`

**中文旁白**：於是三個分量分別正比於三個雅可比函數：第一個是 cn，第二個是 sn，第三個是 dn。它們都是週期函數，週期由第一類完全橢圓積分決定。

**English**: So the three components are proportional to three Jacobian functions: the first to cn, the second to sn, the third to dn. All are periodic, with a period fixed by the complete elliptic integral of the first kind.

**動畫**：右側畫出三條波形。這三條**不是**用橢圓函數庫算的，而是直接把同一條數值積分軌跡的三個分量除以主慣量畫出來——它們本來就是 cn、sn、dn。dn 明顯不過零、只在正值間起伏，和 cn、sn 一眼就分得出來。

---

## 第 9 拍｜退化回對稱陀螺

**畫面公式**：兩個主慣量相等時退化回對稱陀螺　/　`k² → 0 :   cn → cos ,   sn → sin ,   dn → 1`

**中文旁白**：當兩個主慣量趨於相等時，模數趨近於零，這三個函數就退化成餘弦、正弦和常數，回到上一課的對稱陀螺。最後要注意：經過一個週期後，角速度相對於物體回到原位，但物體本身在空間中並沒有回到原來的方向。

**English**: As two of the moments approach each other the modulus tends to zero, the functions degenerate into cosine, sine and a constant, and we are back to the symmetrical top. After one period Ω returns relative to the body, but the body has not returned in space.

---

## 製作備註

- **所有曲線都是真的**：`dM/dt = M × Ω`（Ω_i = M_i / I_i）在 import 時用 RK4 積分，`_closed()` 會偵測軌跡何時回到起點以截出剛好一個週期。
- **分界線改用解析解**：在 M² = 2E I₂ 時兩個二次曲面相減得到 M₁²(1/a₁² − 1/a₂²) = M₃²(1/a₂² − 1/a₃²)，也就是 M₃ = ±c M₁ 兩個平面；交線正好是球面上的兩個大圓。數值積分在分界線上會無限趨近 x₂ 而永遠走不完，畫不出完整的曲線。
- **點數是這一課最大的效能陷阱**：積分出來的軌跡有六千多點，直接餵給 `set_points_as_corners()` 會讓 480p15 的預覽跑不完。`_curve()` 現在一律先降到 170 點以內，橢球線框、球面、波形的取樣數也都調降。同一張圖上有二十幾條曲線時，這件事一定要做。
- 軸標籤的高度要用 `_p()` 實際算過再放：這課的 `_p()` 多了一層 `MS` 縮放，第一次憑印象估位置就讓 x₃ 標籤壓進了三行公式裡。
- **被追蹤的那條軌跡必須是繞 x₃ 的圈**（M² 大於 2E I₂）。書上 (37.10) 的 Ω₁ ∝ cn、Ω₂ ∝ sn、Ω₃ ∝ dn 是在這個前提下寫的；Landau 也明說「若不等式反向，下標 1 和 3 互換」。第一次出片時挑到繞 x₁ 的圈，結果畫面上標成 cn 的那條曲線其實從不過零（是 dn 的行為），標成 dn 的反而過零——物理標錯了，必須重算。驗收波形時的簡單檢查：cn 與 sn 一定要穿越零線，dn 一定不穿越。
