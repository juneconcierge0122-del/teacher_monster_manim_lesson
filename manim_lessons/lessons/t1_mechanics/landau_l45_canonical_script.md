# 第 45 課｜正則變換：座標與動量可以互換（Landau §45）

Lesson 45 — Canonical transformations: coordinates and momenta may trade places

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l45_canonical.py`（`LandauL45ZH` / `LandauL45EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[45]` 與 `FORMULAS[45]`
- 配音：`manim_lessons/samples/audio_l45/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 32 秒、英文約 2 分 36 秒

全課用同一張圖：左右兩個相平面，舊的那個標出一小塊方格，右邊是它的像。點變換只動到 q，方格只會左右移動；正則變換同時攪動 q 與 p，方格被剪切；最後一拍把它整整轉九十度——那個變換做的事就只是把動量改名叫座標。

---

## 第 0 拍｜只換座標：點變換

**畫面公式**：只換座標：點變換　/　coordinates only: a point transformation　/　`Qᵢ = Qᵢ ( q , t )`

**中文旁白**：廣義座標的選擇本來就沒有任何限制，只要能唯一決定系統的位置就好。換到另外一組獨立的量，拉格朗日方程的形式完全不變，這種變換叫做點變換。

**English**: The choice of generalised coordinates is subject to no restriction: they may be any quantities that fix the position of the system. Passing to any other independent set leaves the form of Lagrange's equations unchanged, and such a change is called a point transformation.

**動畫**：左右兩個相平面，左邊標出一小塊方格，右邊是它在點變換下的像：只有 q 被動到。

---

## 第 1 拍｜動量和座標地位平等

**畫面公式**：動量和座標地位平等　/　momenta and coordinates rank equally　/　`Qᵢ = Qᵢ ( p , q , t )   ,   Pᵢ = Pᵢ ( p , q , t )`

**中文旁白**：既然拉格朗日方程不變，哈密頓方程當然也不變。但哈密頓的寫法其實允許更廣的變換，因為在這裡動量和座標是地位平等的獨立變數。

**English**: Since Lagrange's equations are unchanged, Hamilton's equations are unchanged too. But the Hamiltonian treatment in fact allows a much wider range of transformations, because there the momenta are variables independent of and on an equal footing with the coordinates.

**動畫**：同一張圖：哈密頓方程允許更廣的變換。

---

## 第 2 拍｜把全部 2s 個變數一起換

**畫面公式**：把全部 2s 個變數一起換　/　transform all two s variables together　/　`dQᵢ/dt = ∂H′/∂Pᵢ        dPᵢ/dt = − ∂H′/∂Qᵢ`

**中文旁白**：所以我們可以把全部二倍 s 個變數一起換掉：新的座標和新的動量，都同時依賴舊的座標和舊的動量。這種自由度是哈密頓寫法的一大好處。

**English**: So we may transform all two s of the variables together: the new coordinates and the new momenta may each depend on the old coordinates and the old momenta. This enlargement is one of the important advantages of the Hamiltonian treatment.

**動畫**：方格開始被剪切——正則變換把 q 與 p 攪在一起，但面積不變。

---

## 第 3 拍｜要求新變數也滿足哈密頓方程

**畫面公式**：要求新變數也滿足哈密頓方程　/　demand Hamilton's equations in the new variables　/　`δ ∫ ( Σ pᵢ dqᵢ − H dt ) = 0`

**中文旁白**：不過並不是所有這種變換都保持正則的形式。我們來找出條件：要讓新變數也滿足哈密頓方程，需要什麼？

**English**: Not every such transformation keeps the equations in canonical form, however. Let us find the condition: what is needed for the new variables to satisfy Hamilton's equations as well?

**動畫**：同一張圖，右側問：保持正則形式的條件是什麼？

---

## 第 4 拍｜被積函數只能差一個全微分

**畫面公式**：被積函數只能差一個全微分　/　the integrands may differ only by a total differential　/　`Σ pᵢ dqᵢ − H dt = Σ Pᵢ dQᵢ − H′ dt + dF`

**中文旁白**：上一課末尾說過，哈密頓方程可以由最小作用量原理導出，變分對座標和動量各自獨立進行。新變數若也滿足哈密頓方程，同樣的原理也必須成立。

**English**: At the end of the last lesson we saw that Hamilton's equations follow from the principle of least action, with coordinates and momenta varied independently. If the new variables also obey them, the same principle must hold in the new variables.

**動畫**：同一張圖：兩個被積函數只能差一個全微分 dF。

---

## 第 5 拍｜生成函數 F ( q , Q , t )

**畫面公式**：生成函數 F ( q , Q , t )　/　the generating function F ( q , Q , t )　/　`pᵢ = ∂F/∂qᵢ   ,   Pᵢ = − ∂F/∂Qᵢ   ,   H′ = H + ∂F/∂t`

**中文旁白**：兩個形式要等價，只要它們的被積函數相差某個函數的全微分就行——差別只是端點上的常數，不影響變分。滿足這個條件的變換就叫正則變換，那個函數叫生成函數。

**English**: The two forms are equivalent if their integrands differ by the total differential of some function: the difference is then a constant fixed at the endpoints, which cannot affect the variation. Such a transformation is called canonical, and that function is its generating function.

**動畫**：同一張圖，右側讀出 p、P 與 H′ 和生成函數 F 的關係。

---

## 第 6 拍｜把關係式整理一下就能直接

**畫面公式**：`Φ ( q , P , t ) = F + Σ PᵢQᵢ` ／ `pᵢ = ∂Φ/∂qᵢ   ,   Qᵢ = ∂Φ/∂Pᵢ   ,   H′ = H + ∂Φ/∂t`

**中文旁白**：把關係式整理一下就能直接讀出係數：舊動量是生成函數對舊座標的偏導數，新動量是它對新座標的偏導數再取負號，而新舊哈密頓量差一個對時間的偏導數。

**English**: Rearranging that relation lets the coefficients be read off directly: the old momentum is the derivative of the generating function by the old coordinate, the new momentum is minus its derivative by the new coordinate, and the two Hamiltonians differ by its time derivative.

**動畫**：同一張圖，換成以 q 與 P 為變數的生成函數 Φ。

---

## 第 7 拍｜生成函數不含時間時

**畫面公式**：生成函數不含時間時　/　when it carries no time　/　`∂Φ/∂t = 0     ⟹     H′ = H`

**中文旁白**：有時候用舊座標和新動量當自變數比較方便。做一次勒讓德變換，就得到另一個生成函數，這時舊動量是它對舊座標的偏導數，新座標是它對新動量的偏導數。

**English**: Sometimes the old coordinates and the new momenta are the more convenient variables. One Legendre transformation gives a second generating function, whose derivative by the old coordinate is the old momentum and whose derivative by the new momentum is the new coordinate.

**動畫**：同一張圖：生成函數不含時間時 H′ = H。

---

## 第 8 拍｜座標與動量只差一個名字

**畫面公式**：座標與動量只差一個名字　/　coordinate and momentum differ only in name　/　`Qᵢ = pᵢ   ,   Pᵢ = − qᵢ`

**中文旁白**：無論用哪一種，新舊哈密頓量的差永遠是生成函數對時間的偏導數。所以生成函數不顯含時間時，新哈密頓量就是把舊的直接換成新變數。

**English**: Whichever form is used, the difference of the two Hamiltonians is always the partial derivative of the generating function with respect to time. So if it does not contain the time, the new Hamiltonian is the old one with the new variables substituted in.

**動畫**：方格整整轉過九十度——這就是 Q = p、P = −q，把座標和動量對調。

---

## 第 9 拍｜用帕松括號寫出正則的條件

**畫面公式**：用帕松括號寫出正則的條件　/　the canonical condition in Poisson brackets　/　`[ Qᵢ , Qₖ ] = 0  ,  [ Pᵢ , Pₖ ] = 0  ,  [ Pᵢ , Qₖ ] = δᵢₖ`

**中文旁白**：正則變換的範圍這麼廣，座標和動量的區別幾乎只剩下名字：取新座標等於舊動量、新動量等於負的舊座標，就只是把兩者對調而已。所以一般就叫它們正則共軛量，而正則的條件可以用帕松括號乾淨地寫出來。

**English**: The range is so wide that the distinction between coordinates and momenta is little more than a name: one such transformation simply interchanges them. Hence they are called canonically conjugate quantities, and the canonical condition is written cleanly with Poisson brackets.

**動畫**：同一張圖，下方點出面積始終不變，正好接到下一課的劉維定理。

---
