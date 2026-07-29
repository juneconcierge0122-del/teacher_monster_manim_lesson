# 第 51 課｜絕熱不變量守恆的精確度：指數式地小（Landau §51）

Lesson 51 — Accuracy of conservation of the adiabatic invariant: exponentially small

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l51_accuracy.py`（`LandauL51ZH` / `LandauL51EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[51]` 與 `FORMULAS[51]`
- 配音：`manim_lessons/samples/audio_l51/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 24 秒、英文約 2 分 24 秒

四張圖，一張對應論證的一個階段。先畫 Λ 隨角變數的週期變化，把一個週期的兩端釘在同樣的高度——這就是它的導數平均為零的全部理由。接著是參數的爬升曲線，作用變數在底下抖動，最後停在幾乎、但不完全相同的高度。再來是書上圖 56 的複角變數平面：路徑被抬離實軸、被奇點勾成一個個圈，並量出最近那個奇點的虛部。最後用三種變化速度下的 ΔI 長條圖收尾。

---

## 第 0 拍｜同一條方程的另一個用法

**畫面公式**：同一條方程的另一個用法　/　the same equation used again　/　`dI/dt = − ( ∂Λ/∂w ) ( dλ/dt )`

**中文旁白**：上一課最後那條方程還可以給絕熱不變性另一個證明，而且順便告訴我們它有多準。

**English**: The last equation of the previous lesson gives another proof of adiabatic invariance, and tells us on the way how accurate the invariance is.

**動畫**：Λ 隨角變數 w 的曲線，一個亮點沿著它跑：這是一個週期函數。

---

## 第 1 拍｜Λ 是單值的，所以是週期的

**畫面公式**：Λ 是單值的，所以是週期的　/　Λ is single-valued, hence periodic　/　`Λ = ( ∂S₀/∂λ )_I        Λ ( w + 2π ) = Λ ( w )`

**中文旁白**：簡略作用量對座標不是單值的，但那個多出來的量卻是單值的：微分是在固定作用變數下做的，多值的增量剛好消掉。既然單值，它就是角變數的週期函數。

**English**: The abbreviated action is not a single-valued function of the coordinate, but the extra quantity is, because the differentiation is at constant action variable and the many-valued increments cancel. Being single-valued, it is a periodic function of the angle variable.

**動畫**：在相距一個週期的兩點各放一個紅點，高度完全相同。

---

## 第 2 拍｜週期函數導數的平均是零

**畫面公式**：週期函數導數的平均是零　/　a periodic derivative averages to zero　/　`⟨ ∂Λ/∂w ⟩ = 0     ⟹     ⟨ dI/dt ⟩ = 0`

**中文旁白**：而一個週期函數的導數，對一個週期取平均一定是零。把方程平均起來，再把緩變的參數變化率提到平均外面，就得到作用變數的平均變化率為零。

**English**: And the mean value over a period of the derivative of a periodic function is zero. Averaging the equation, with the slowly varying rate taken outside the mean, leaves the mean rate of change of the action variable equal to zero.

**動畫**：兩點之間拉一條箭頭標出「一個週期」：兩端等高，所以總變化是零。

---

## 第 3 拍｜整段過程總共變了多少？

**畫面公式**：整段過程總共變了多少？　/　how much does it change in all?　/　`λ → λ₋ ( t → −∞ )   ,   λ → λ₊ ( t → +∞ )        ΔI = I₊ − I₋`

**中文旁白**：接下來問精確度。假設參數在很久以前和很久以後都趨近固定值，給定一開始的作用變數，問整段過程總共變了多少。

**English**: Now for the accuracy. Let the parameter tend to constant limits long before and long after, and let the action variable be given at the start. The question is how much it has changed in total by the end.

**動畫**：換成兩張疊起來的小圖：上面是 λ(t) 從 λ₋ 爬到 λ₊，下面是 I(t)。

---

## 第 4 拍｜展成傅立葉級數

**畫面公式**：展成傅立葉級數　/　expand it in a Fourier series　/　`ΔI = − ∫ ( ∂Λ/∂w ) ( dλ/dt ) dt        Λ = Σ_l Λ_l · exp ( i l w )`

**中文旁白**：這個總變化就是把那個負的偏導數乘上參數變化率，對全部時間積分。那個量是角變數的週期函數，所以先把它展成傅立葉級數。

**English**: That total change is the integral over all time of minus the derivative by the angle, times the rate of change of the parameter. The quantity is periodic in the angle, so we first expand it in a Fourier series.

**動畫**：兩條曲線一起往右長出來；I 在中途抖動，λ 平滑地爬升。

---

## 第 5 拍｜把積分變數換成 w

**畫面公式**：把積分變數換成 w　/　change the variable to w　/　`dw/dt > 0        ∫ … dt   ⟶   ∫ … dw`

**中文旁白**：只要參數變得夠慢，角變數就隨時間單調增加，於是可以把積分變數從時間換成角變數，而積分上下限不變。

**English**: Provided the parameter varies slowly enough, the angle variable increases monotonically with the time, so we may change the variable of integration from the time to the angle without altering the limits.

**動畫**：曲線畫完，右端用一支短箭頭標出 ΔI：小得不成比例。

---

## 第 6 拍｜把 w 當成複變數

**畫面公式**：把 w 當成複變數　/　treat w as a complex variable　/　`w  complex        contour  ⟶  upper half-plane`

**中文旁白**：現在把角變數當成複變數。假設被積函數在實軸上沒有奇點，就把積分路徑往上半平面推。路徑會被奇點勾住，繞著它們形成一個個圈。

**English**: Now treat the angle as a complex variable. Assuming the integrand has no singularity on the real axis, we push the contour up into the upper half-plane. The contour is caught on the singularities and forms a loop around each of them.

**動畫**：換成複角變數平面：積分路徑被推進上半平面，被三個奇點勾成三個圈。

---

## 第 7 拍｜離實軸最近的那個奇點

**畫面公式**：離實軸最近的那個奇點　/　the singularity nearest the real axis　/　`ΔI  ~  exp ( − Im w₀ )`

**中文旁白**：設離實軸最近的那個奇點是 w₀。主要的貢獻來自它附近，級數每一項都帶一個指數因子；只留下衰減最慢的那一項，總變化的量級就是 e 的負 w₀ 虛部次方。

**English**: Let the singularity nearest the real axis be the one that matters. The main contribution comes from its neighbourhood, and every term of the series brings an exponential factor. Keeping only the slowest-decaying term, the total change is of order e to the minus its imaginary part.

**動畫**：最靠近實軸的那個奇點改用紅色標出，並用一支箭頭量出它的虛部 im w₀。

---

## 第 8 拍｜這個指數非常大

**畫面公式**：這個指數非常大　/　and that exponent is large　/　`| t₀ |  ~  τ        Im w₀  ~  ω τ  ~  τ / T`

**中文旁白**：設對應的複「時刻」是 t₀，它的量級就是參數變化的特徵時間。於是那個指數的量級是頻率乘特徵時間，也就是特徵時間除以週期。既然特徵時間遠大於週期，這個指數很大。

**English**: Let the corresponding complex instant be the point where the angle takes that value. Its magnitude is of the order of the characteristic time over which the parameters vary, so the exponent is of order the frequency times that time, that is, the time divided by the period.

**動畫**：同一張圖：這個虛部的量級是頻率乘上參數變化的特徵時間，也就是 τ / T。

---

## 第 9 拍｜越慢，漂移越指數式地小

**畫面公式**：越慢，漂移越指數式地小　/　slower means exponentially smaller　/　`dw/dt = ω ( I , λ ( t ) )        w₀ = ∫ ω dt   ( t → t₀ )`

**中文旁白**：所以參數變得越慢，作用變數的總變化就指數式地變小。要算到最低階，可以在角變數的方程裡丟掉那個小修正項，把頻率直接對時間積到 t₀。真正決定答案的，是那個量和頻率倒數在複平面上的奇點。

**English**: Since the characteristic time is far longer than the period, the exponent is large: the slower the change, the more exponentially small the total drift of the action variable. To leading order, drop the small correction and integrate the frequency up to that instant.

**動畫**：換成長條圖：τ/T 等於 2、5、9 時的 ΔI，一根比一根矮得多——指數式地小。

---
