# 第 48 課｜分離變數：把偏微分方程化成一串一維積分（Landau §48）

Lesson 48 — Separation of the variables: reducing the equation to quadratures

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l48_separation.py`（`LandauL48ZH` / `LandauL48EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[48]` 與 `FORMULAS[48]`
- 配音：`manim_lessons/samples/audio_l48/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 9 秒、英文約 2 分 10 秒

把記帳的過程畫出來：漢彌頓－雅可比方程是一個裝著所有變數的大盒子，接著一次剝下一塊磚，每一塊帶走自己的常數，變成一個一維積分。到最後大盒子空了，下面那一排小積分就是完全積分——這正是「化為求積」的意思。

---

## 第 0 拍｜完全積分怎麼求？

**畫面公式**：完全積分怎麼求？　/　how is a complete integral found?　/　`H ( q ; ∂S/∂q ) = E`

**中文旁白**：在許多重要的情形裡，漢彌頓－雅可比方程的完全積分可以用一個叫做分離變數的辦法求出來。

**English**: In a number of important cases a complete integral of the Hamilton-Jacobi equation can be found by a method called separating the variables.

**動畫**：一個大盒子裝著四塊磚 q₁、q₂、q₃、t——漢彌頓－雅可比方程裡的全部變數。

---

## 第 1 拍｜某個座標只以一個組合出現

**畫面公式**：某個座標只以一個組合出現　/　one coordinate appears only in one combination　/　`Φ { qᵢ , t , ∂S/∂qᵢ , ∂S/∂t , φ ( q₁ , ∂S/∂q₁ ) } = 0`

**中文旁白**：假設某一個座標，比如第一個，和作用量對它的導數，只以某一個組合的形式出現，而且這個組合裡不含其他座標、不含時間、也不含其他導數。

**English**: Suppose some coordinate, say the first, and the derivative of the action with respect to it appear only in one particular combination, and that this combination involves no other coordinate, no time and no other derivative.

**動畫**：同一張圖：假設 q₁ 只以一個組合 φ 出現。

---

## 第 2 拍｜把 S 拆成兩部分

**畫面公式**：把 S 拆成兩部分　/　split S into two pieces　/　`S = S′ ( qᵢ , t ) + S₁ ( q₁ )`

**中文旁白**：這時就試著把作用量拆成兩部分：一個只依賴那個座標，另一個含其餘的變數和時間。

**English**: Then we look for a solution as a sum of two pieces: one depending on that coordinate alone, and one carrying all the remaining variables and the time.

**動畫**：同一張圖：把 S 拆成只含 q₁ 的一部分加上其餘。

---

## 第 3 拍｜那個組合必須是常數

**畫面公式**：那個組合必須是常數　/　the combination must be a constant　/　`q₁  varies     ⟹     φ = const`

**中文旁白**：把這個拆法代回方程，它必須對那個座標的任何值都成立。可是那個座標一變，只有那個組合會變，所以那個組合必須是一個常數。

**English**: Substituting this into the equation, it must hold identically for every value of that coordinate. But when the coordinate changes, only the combination changes, so the combination must be a constant.

**動畫**：同一張圖：q₁ 一變只有 φ 會變，所以 φ 必須是常數。

---

## 第 4 拍｜一條常微分方程

**畫面公式**：一條常微分方程　/　an ordinary differential equation　/　`φ ( q₁ , dS₁/dq₁ ) = α₁`

**中文旁白**：於是原本一條方程分成了兩條。第一條說那個組合等於一個任意常數，它是一條常微分方程，直接積分就得到那一部分的作用量。

**English**: So the single equation splits into two. The first says the combination equals an arbitrary constant; it is an ordinary differential equation, and simple integration gives that part of the action.

**動畫**：第一塊磚 q₁ 從大盒子裡掉下來，帶著它自己的常數 α₁ 成為一個一維積分。

---

## 第 5 拍｜剩下的方程少一個變數

**畫面公式**：剩下的方程少一個變數　/　one independent variable fewer remains　/　`Φ { qᵢ , t , ∂S′/∂qᵢ , ∂S′/∂t ; α₁ } = 0`

**中文旁白**：第二條還是偏微分方程，但獨立變數少了一個。這樣一個一個分離下去，求完全積分就化成了一串一維積分，也就是所謂的化為求積。

**English**: The second is still a partial differential equation, but with one independent variable fewer. Separating one variable after another this way reduces the search for a complete integral to a chain of one-dimensional integrals, which is to say to quadratures.

**動畫**：第二塊磚 q₂ 掉下來，大盒子又縮小一格。

---

## 第 6 拍｜保守系統的完全積分

**畫面公式**：保守系統的完全積分　/　the complete integral, conservative case　/　`S = Σ Sₖ ( qₖ ; α₁ … α_s ) − E t`

**中文旁白**：對保守系統，實際上只要分離 s 個座標。分離完成之後，完全積分就是每個座標各自那一項加起來，再減去能量乘時間。

**English**: For a conservative system only the s coordinates have to be separated in practice. Once the separation is complete, the integral is the sum of one term per coordinate, minus the energy times the time.

**動畫**：第三塊磚 q₃ 與時間 t 也掉下來，大盒子空了，下面排出完整的一串一維積分。

---

## 第 7 拍｜循環座標是最簡單的特例

**畫面公式**：循環座標是最簡單的特例　/　a cyclic coordinate is the simplest case　/　`q₁ cyclic     ⟹     S₁ = α₁ q₁   ,   α₁ = p₁`

**中文旁白**：循環座標是最簡單的特例：它根本不出現在哈密頓量裡，那個組合就退化成作用量對它的導數本身，於是那一項就是常數乘座標，而這個常數正是循環座標對應的守恆動量。

**English**: A cyclic coordinate is the simplest special case: it does not appear in the Hamiltonian at all, the combination reduces to the derivative of the action alone, and that term is just a constant times the coordinate, the constant being the conserved momentum belonging to it.

**動畫**：第一塊磚換成紅色並標上 α₁ = p₁——循環座標的特例。

---

## 第 8 拍｜時間也是一個「循環變數」

**畫面公式**：時間也是一個「循環變數」　/　the time separates as a cyclic variable too　/　`− E t :  the time separated as a cyclic variable`

**中文旁白**：保守系統裡減去能量乘時間的那一項，其實就是把時間當成一個循環變數分離出來的結果。

**English**: The term with minus the energy times the time, in a conservative system, is exactly what comes of separating the time as a cyclic variable of its own.

**動畫**：同一排積分：減去 E t 的那一項就是把時間當成循環變數分離出來。

---

## 第 9 拍｜球座標、拋物線座標……

**畫面公式**：球座標、拋物線座標……　/　spherical, parabolic, and more　/　`spherical , parabolic , …`

**中文旁白**：所以以前所有用循環座標做的簡化，全部都被分離變數法包含進去；而且還多出一些變數並不循環、卻仍然可以分離的情形，像是球座標與拋物線座標下的運動。這使得漢彌頓－雅可比方法成為求通解最有力的工具。

**English**: So every earlier simplification made with cyclic coordinates is contained in this method, and to those are added cases that separate without being cyclic at all, such as spherical or parabolic coordinates. This makes Hamilton-Jacobi the most powerful route to the general integral.

**動畫**：同一排積分，右側列出球座標、拋物線座標等仍可分離的情形。

---
