# 第 34 課｜剛體的運動方程：力與力矩（Landau §34）

Lesson 34 — The equations of motion of a rigid body: force and torque

- 場景檔：`manim_lessons/lessons/landau_l34_eom_rigid.py`（`LandauL34ZH` / `LandauL34EN`）
- 腳本與畫面公式：`manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[34]` 與 `FORMULAS[34]`
- 配音：`manim_lessons/samples/audio_l34/{zh-TW,en}`（edge-tts，`-4%`）
- 片長：中文約 3 分 04 秒、英文約 2 分 51 秒

---

## 第 0 拍｜兩個向量方程

**畫面公式**：六個自由度 ⇒ 六條方程　/　`dP/dt = F        dM/dt = K`

**中文旁白**：剛體有六個自由度，所以運動方程一共需要六條。它們可以寫成兩個向量的時間導數：一個是總動量，管質心怎麼移動；另一個是總角動量，管物體怎麼轉。

**English**: A rigid body has six degrees of freedom, so its equations of motion must be six in all. They can be put as the time derivatives of two vectors: the total momentum, which governs how the centre of mass moves, and the total angular momentum, which governs how the body turns.

**動畫**：左邊是一個緩慢自轉的多邊形剛體，質心標為 O，動量 P 以青色箭頭表示，角動量 M 以紫色弧形箭頭繞著物體。右邊列出「3 個平移自由度 + 3 個轉動自由度 = 六條運動方程」。

---

## 第 1 拍｜第一條方程：dP/dt = F

**畫面公式**：內力成對抵消，只剩外力　/　`P = μ V   ,   dP/dt = F = Σ f`

**中文旁白**：第一條方程只要把每個質點的動量變化率加起來。總動量等於總質量乘上質心速度，它的時間導數就是總力。這裡的總力只包含外力，因為質點之間的內力永遠成對出現、大小相等方向相反，加起來自動抵消。

**English**: The first equation comes from summing the momentum change over every particle. Total momentum is the total mass times the centre-of-mass velocity, and its time derivative is the total force. Only external forces count: internal ones cancel in equal and opposite pairs.

**動畫**：剛體一邊翻滾一邊沿著一條灰色虛線拋物線飛行，質心走的正是等加速度軌跡。質點之間畫出紅色成對的內力箭頭（大小相等、方向相反），兩支紫色外力箭頭作用在質點上，它們的合力就是質心上那支青色的 F。

---

## 第 2 拍｜外場中的力

**畫面公式**：勢能對質心座標的梯度　/　`F = − ∂U / ∂R        δU = − F · δR`

**中文旁白**：如果剛體處在外場中，只要把勢能對質心座標微分，就得到這個力。理由很簡單：把整個物體平移一小段，每一點的位置向量都改變同樣的量，勢能的變化就等於負的力點乘這段位移。

**English**: In an external field this force is the derivative of the potential energy with respect to the centre-of-mass coordinates. Translate the whole body slightly and every point shifts by the same amount, so the change in energy is minus the force dotted into that shift.

**動畫**：畫面中央是一組同心橢圓等勢面，中心標「U 最小」。剛體停在最外圈上緩慢起伏，F 箭頭永遠垂直等勢面、指向勢能下降的方向，旁邊用紅色虛線標出位移 δR。

---

## 第 3 拍｜第二條方程：dM/dt = K

**畫面公式**：力矩 = 位置 × 力　/　`dM/dt = K   ,   K = Σ r × f`

**中文旁白**：第二條方程給角動量的變化率。取一個此刻質心靜止的參考系來推導，位置向量的導數與動量平行，那個叉積為零，只剩下位置與力的叉積。這個總和就叫力矩，角動量的時間導數等於它。

**English**: The second equation gives the rate of change of the angular momentum. Work in a frame where the centre of mass is momentarily at rest: each position vector's derivative is parallel to the momentum, so that cross product drops out, leaving position crossed with force.

**動畫**：左右兩個相同的剛體。左邊的力正好通過質心，物體不轉；右邊同樣大小的力作用在偏離質心的點上、方向與 r 垂直，質心處出現一個表示出紙面的 ⊙ 記號（r × f），物體因此越轉越快。

---

## 第 4 拍｜力矩與原點

**畫面公式**：力矩與原點的選擇有關　/　`r′ = r − a     ⟹     K = K′ + a × F`

**中文旁白**：力矩和角動量一樣，要看你把原點取在哪裡。把原點移動一段距離，每一點的新位置向量都少掉這段位移，於是新的力矩等於原本的力矩，加上這段位移與總力的叉積。

**English**: Torque, like angular momentum, depends on where the origin is. Move the origin by some displacement and every position vector loses that displacement, so the new torque is the original torque plus that displacement crossed into the total force.

**動畫**：一個受力 f 的剛體，原點 O 固定在質心，第二個原點 O′ 沿水平方向來回滑動，位移 a 用灰色箭頭標出。右側三條橫向長條即時顯示 K（橘）、K′（青）與 a × F（紫）的帶正負號數值；O′ 移動時後兩條跟著變，而三者永遠滿足 K = K′ + a × F。

---

## 第 5 拍｜力偶

**畫面公式**：力偶：不推質心，只轉物體　/　`F = 0     ⟹     K = K′`

**中文旁白**：由此馬上看出一個特例：如果總力為零，力矩就與原點的選擇無關。這時物體受到的是一對大小相等、方向相反的力，我們說它受到一個力偶；力偶不推動質心，只讓物體轉動。

**English**: One special case follows at once: if the total force vanishes, the torque no longer depends on the choice of origin. The body is then acted on by a couple, a pair of equal and opposite forces. A couple does not push the centre of mass; it only makes the body turn.

**動畫**：沿用上一拍的畫面，第二支方向相反的力 −f 逐漸長出來。總力歸零之後，紫色的 a × F 長條縮到零，K′ 的長條也停止變化、與 K 完全等長——即使 O′ 還在滑動。

---

## 第 6 拍｜從拉格朗日量看

**畫面公式**：力矩是勢能對轉角的負斜率　/　`∂L/∂Ωᵢ = Mᵢ     ,     K = − ∂U / ∂φ`

**中文旁白**：這兩條方程也可以直接從拉格朗日量得到。把拉格朗日量對角速度的分量微分，得到的正是角動量的分量；而把物體轉過一個無限小的角度，勢能的變化等於負的力矩點乘這個角度。所以力矩就是勢能對轉角的負導數。

**English**: The Lagrangian gives both equations directly. Differentiating it by the components of the angular velocity returns the angular momentum. Rotating the body through a small angle changes the energy by minus the torque dotted into that angle, so torque is minus its derivative.

**動畫**：左邊一根像指南針的偶極在水平均勻場 E 中左右擺動，轉角 φ 標在中央，紫色弧形箭頭是回復力矩 K，方向隨 φ 的正負翻轉。右邊是 U(φ) 曲線，紅點跟著同一個 φ 移動，紫色切線顯示斜率，水平箭頭表示 K 等於負的斜率。

---

## 第 7 拍｜化成單一個力

**畫面公式**：化成沿一條直線作用的單一個力　/　`K · F = 0     ⟹     K = a × F`

**中文旁白**：還有一個漂亮的結果：假設總力與總力矩互相垂直，那麼一定能找到一段位移，讓新原點的力矩剛好為零。滿足條件的點不是一個點，而是一整條直線；所有作用力的效果，都可以化成沿著這條直線作用的單一個力。

**English**: One more elegant result. Suppose the total force and the total torque are perpendicular. Then some displacement always makes the torque about the new origin vanish. The points that work form a whole line, and all the applied forces reduce to one force acting along it.

**動畫**：剛體上有三支紫色的外力，紅色虛線畫出「作用線」。青色的合力 F 沿著這條線來回滑動，灰色虛線 a 從質心指向它此刻的作用點——不論滑到哪裡，力矩都一樣。右半邊把三支力首尾相接，直接量出它們的合力 F。

---

## 第 8 拍｜均勻場

**畫面公式**：均勻場：每個質點受同方向的力　/　`f = e E   ,   F = E Σ e   ,   K = Σ e r × E`

**中文旁白**：均勻場正是這種情形。每個質點受到的力都正比於同一個常向量，所以總力等於所有係數的總和乘上這個向量，而總力矩等於一個特別的位置向量與總力的叉積。

**English**: A uniform field is exactly this case. Every particle feels a force proportional to the same constant vector, so the total force is the sum of the coefficients times that vector, and the total torque is one special position vector crossed into the total force.

**動畫**：整個畫面佈滿向下的均勻場線 E。剛體緩慢自轉，四個質點的大小代表係數 e，各自帶著一支長度正比於 e 的紅色箭頭，方向永遠向下；加權平均點 r₀ 標成青色。右側把四支箭頭首尾相接，總長就是青色的 F。

---

## 第 9 拍｜效果集中在質心

**畫面公式**：重力的效果集中在質心　/　`r₀ = Σ e r / Σ e     ⟹     K = r₀ × F`

**中文旁白**：這個位置向量，就是用各質點的係數加權平均出來的點。在均勻重力場裡係數就是質量，這個點正好是質心；所以整個重力場的效果，就是一個作用在質心上的力，這也是為什麼重力可以畫成質心上的一支箭頭。

**English**: That position vector is simply the weighted average over the particles. In a uniform gravitational field the coefficient is the mass and the point is the centre of mass, so the field reduces to one force applied there: weight is a single arrow at the centre of mass.

**動畫**：左邊剛體吊在一個支點上像複擺一樣擺動，四支分散的重力箭頭合併成質心上唯一的一支 F。右邊用一根槓桿說明同一件事：四個大小不同的載重放在各自的位置，支點恰好落在加權平均的 r₀ 上，整根桿子剛好平衡。

---

## 製作備註

- `always_redraw` 裡不要用 `DashedLine`：它的虛線段數由長度決定，長度一變、submobject 數量就變，會打亂同一個 VGroup 被 `FadeIn` 時的家族對齊，導致相鄰 `Text` 的字母被靜默吃掉（英文版第 7 拍的字幕曾少掉開頭 7 個字母）。本課改用 `_dash()`，以固定 `num_dashes` 的 `DashedVMobject` 取代。
- 第 3 拍右側的力取成與 r 垂直的切向力，力矩才是定值，物體等角加速地轉起來，箭頭也不會穿過質心。
- 第 9 拍的槓桿只看 x 座標，所以 `PARTS` 的四個 x 值刻意拉開，避免兩個載重疊在一起。
