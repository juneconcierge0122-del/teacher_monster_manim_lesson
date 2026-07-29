# 第 42 課｜帕松括號：守恆量的代數（Landau §42）

Lesson 42 — Poisson brackets: an algebra of conserved quantities

- 場景檔：`manim_lessons/lessons/t1_mechanics/landau_l42_poisson.py`（`LandauL42ZH` / `LandauL42EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[42]` 與 `FORMULAS[42]`
- 配音：`manim_lessons/samples/audio_l42/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 2 分 16 秒、英文約 2 分 8 秒

全課用同一張相空間圖：哈密頓方程給出的流場、沿著流走的代表點，以及守恆量的等值線——守恆量的等值線沿著流，不守恆量的等值線橫切過流。

---

## 第 0 拍｜任何一個相空間上的函數

**畫面公式**：任何一個相空間上的函數　/　any function on phase space　/　`df/dt = ∂f/∂t + Σ ( ∂f/∂qₖ ) q̇ₖ + Σ ( ∂f/∂pₖ ) ṗₖ`

**中文旁白**：取任何一個依賴座標、動量和時間的函數。它隨時間的全導數，是對時間的偏導數，再加上對每個座標和每個動量的偏導數，各自乘上它們的變化率。

**English**: Take any function of the coordinates, the momenta and the time. Its total time derivative is the partial derivative with respect to time, plus the derivative with respect to each coordinate and each momentum times their rates of change.

**動畫**：相空間的座標軸，右側寫出任意函數 f(p, q, t) 的全導數。

---

## 第 1 拍｜代入哈密頓方程，帕松括號就出現了

**畫面公式**：代入哈密頓方程，帕松括號就出現了　/　put in Hamilton's equations and the bracket appears　/　`df/dt = ∂f/∂t + [ H , f ]` ／ `[ H , f ] = Σ ( ∂H/∂pₖ ) ( ∂f/∂qₖ ) − ( ∂H/∂qₖ ) ( ∂f/∂pₖ )`

**中文旁白**：把哈密頓方程代進去，那些變化率就換成了哈密頓量的偏導數。整理之後，全導數等於對時間的偏導數，加上一個只由 H 和 f 的偏導數組成的組合——這個組合就叫帕松括號。

**English**: Substitute Hamilton's equations and those rates become derivatives of the Hamiltonian. Collecting terms, the total derivative is the partial one plus a combination built only from derivatives of H and f, and that combination is the Poisson bracket.

**動畫**：哈密頓方程給出的流場箭頭鋪滿相空間，剩下的組合就是帕松括號。

---

## 第 2 拍｜運動積分的條件

**畫面公式**：運動積分的條件　/　the condition for an integral of the motion　/　`∂f/∂t + [ H , f ] = 0`

**中文旁白**：於是守恆量的條件變得非常乾淨：一個量在運動中保持不變，等價於它對時間的偏導數，加上它和哈密頓量的帕松括號，等於零。

**English**: The condition for a conserved quantity is now very clean: a quantity stays constant during the motion exactly when its partial derivative with respect to time, plus its Poisson bracket with the Hamiltonian, vanishes.

**動畫**：流場加上沿流移動的代表點：守恆的條件就是 ∂f/∂t + [H, f] = 0。

---

## 第 3 拍｜等值線沿著流：所以它不變

**畫面公式**：等值線沿著流：所以它不變　/　level curves along the flow, so it cannot change　/　`[ H , f ] = 0`

**中文旁白**：如果這個量不顯含時間，條件就只剩下一句話：它和哈密頓量的帕松括號等於零。在相空間裡看，這表示它的等值線正好和演化的流向重合，所以沿著運動它不會改變。

**English**: If the quantity carries no explicit time, the condition is a single statement: its bracket with the Hamiltonian is zero. In phase space that means its level curves lie along the flow, so it cannot change as the system moves.

**動畫**：兩組等值線的對照——青色的守恆量等值線沿著流走，紅色的非守恆量等值線橫切過流。

---

## 第 4 拍｜任意兩個量的帕松括號

**畫面公式**：任意兩個量的帕松括號　/　the bracket of any two quantities　/　`[ f , g ] = Σ ( ∂f/∂pₖ ) ( ∂g/∂qₖ ) − ( ∂f/∂qₖ ) ( ∂g/∂pₖ )`

**中文旁白**：任何兩個量之間都可以照同樣的方式定義帕松括號：對每一對座標與動量，取交叉的偏導數相減，再全部加起來。

**English**: The bracket of any two quantities is defined the same way: for each coordinate and momentum pair take the crossed derivatives, subtract them, and add over all the pairs.

**動畫**：回到流場，寫出任意兩個量的帕松括號定義。

---

## 第 5 拍｜反對稱，而且對常數為零

**畫面公式**：反對稱，而且對常數為零　/　antisymmetric, and zero against a constant　/　`[ f , g ] = − [ g , f ]        [ f , c ] = 0`

**中文旁白**：它有幾個一看就懂的性質：把兩個函數對調，括號變號；其中一個是常數時，括號為零；而且對每個變數都是線性的。

**English**: It has a few properties you can read straight off. Swapping the two functions changes the sign; if one of them is a constant the bracket is zero; and it is linear in each argument.

**動畫**：同一張圖，列出反對稱、對常數為零、線性這幾個性質。

---

## 第 6 拍｜座標與動量之間的基本括號

**畫面公式**：座標與動量之間的基本括號　/　the fundamental brackets among q and p　/　`[ qᵢ , qₖ ] = 0    ,    [ pᵢ , pₖ ] = 0    ,    [ pᵢ , qₖ ] = δᵢₖ`

**中文旁白**：座標和動量彼此之間的括號特別簡單：兩個座標的括號是零，兩個動量的括號也是零，而一個動量和它自己對應的座標，括號等於一。

**English**: The brackets among the coordinates and momenta themselves are especially simple: two coordinates give zero, two momenta give zero, and a momentum with its own coordinate gives one.

**動畫**：同一張圖，列出座標與動量之間的基本括號。

---

## 第 7 拍｜雅可比恆等式

**畫面公式**：雅可比恆等式　/　Jacobi's identity　/　`[ f , [ g , h ] ] + [ g , [ h , f ] ] + [ h , [ f , g ] ] = 0`

**中文旁白**：還有一條稍微複雜、但非常重要的恆等式，叫做雅可比恆等式：把三個函數依序輪換寫成三重括號，三項加起來恆等於零。

**English**: There is one more identity, a little heavier but very important, called Jacobi's identity: write the three functions in a cyclic order as a nested bracket, and the three terms add up to zero.

**動畫**：同一張圖，寫出雅可比恆等式。

---

## 第 8 拍｜帕松定理

**畫面公式**：帕松定理　/　Poisson's theorem　/　`[ f , g ] = const`

**中文旁白**：由它可以推出帕松定理：如果兩個量都是運動積分，那麼它們的帕松括號也是運動積分。

**English**: From it follows Poisson's theorem: if two quantities are both integrals of the motion, then their Poisson bracket is an integral of the motion as well.

**動畫**：同一張圖：兩個運動積分的帕松括號也是運動積分。

---

## 第 9 拍｜已知的守恆量能生出新的

**畫面公式**：已知的守恆量能生出新的　/　known integrals can breed new ones　/　`[ H , f ] = 0  ,  [ H , g ] = 0     ⟹     [ H , [ f , g ] ] = 0`

**中文旁白**：證明很簡單：在雅可比恆等式裡把其中一個函數取成哈密頓量，另外兩個都與 H 的括號為零，剩下那一項就必須為零。所以已知的守恆量可以互相「相乘」，生出新的守恆量。

**English**: The proof is short. Put the Hamiltonian in for one of the three functions in Jacobi's identity; the other two have vanishing brackets with H, so the remaining term must vanish too. Known conserved quantities can thus breed new ones.

**動畫**：同一張圖：在雅可比恆等式裡取 h = H，於是守恆量可以互相生成。

---
