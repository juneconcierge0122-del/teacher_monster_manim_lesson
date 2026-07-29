# Landau Mechanics 32 — The inertia tensor

> 《Landau–Lifshitz 經典力學》教學系列第 32 課（第六章「剛體運動」第二課，§32）
> 中文標題：慣性張量：轉動能量的九個係數
> English title: The inertia tensor: nine coefficients for rotational energy

## 繁體中文旁白

要算剛體的動能，先把它看成一堆質點，總動能就是每個質點二分之一質量乘速度平方的總和；而每一點的速度，都是質心的平移速度加上角速度與位置向量的叉積。

把速度代進去展開會出現三項。因為原點取在質心，位置向量的質量加權和為零，交叉項剛好消失，動能就乾淨地分成平移動能與繞質心的轉動動能兩塊。

重點在轉動那一項。把叉積的平方展開後，它是角速度分量的二次式；所有和質量分布有關的訊息，全被收進九個係數裡，這組係數就叫慣性張量。

每個分量都是對所有質點求和：對角線三個是繞座標軸的轉動慣量，等於質量乘上到該軸垂直距離的平方；非對角線是質量乘兩個座標再取負號。這個張量對稱而且可加。

但這九個數字不是物體固有的，它們取決於我們把座標軸擺在哪個方向。把座標軸轉一圈，對角線的值跟著變，非對角線的分量也忽大忽小。

因為它是對稱張量，一定存在一組方向讓所有非對角線分量同時歸零。這組方向叫慣性主軸，剩下的三個數字叫主慣量；用主軸來寫，轉動動能就只剩三項平方和。

三個主慣量決定物體的類型：三個都不同是非對稱陀螺；兩個相等是對稱陀螺，垂直於對稱軸的那兩根主軸可以隨便選；三個都相等是球陀螺，任何三根互相垂直的軸都行。

兩個好用的特例：所有質點共面時，垂直於平面那根軸的主慣量剛好等於另外兩個之和；所有質點共線時，兩個主慣量相等、第三個等於零，這種轉子只有兩個轉動自由度。

最後，前面的公式要求原點取在質心，但有時候換個原點更好算；兩組張量只差一個由總質量與位移構成的修正項，減回去就得到以質心為原點的慣性張量。

## English narration

A rigid body's kinetic energy is the sum of one-half m v-squared over all its particles, and each velocity is the translation of the centre of mass plus the cross product of the angular velocity with the position vector.

Substituting and expanding gives three terms. Because the origin sits at the centre of mass, the mass-weighted sum of the position vectors vanishes, so the cross term drops out and the energy splits into translation plus rotation.

Expanding the squared cross product, the rotational part is a quadratic form in the components of the angular velocity, and the whole mass distribution collapses into nine coefficients: the inertia tensor.

Every component is a sum over the particles. The three diagonal ones are the moments of inertia about the axes, mass times squared perpendicular distance, while the off-diagonal ones are minus the mass times a product of two coordinates.

These nine numbers are not intrinsic to the body: they depend on where we point the axes. Turn the axes around and the diagonal values change, while the off-diagonal components grow and shrink.

Because the tensor is symmetric, some orientation always makes every off-diagonal component vanish at once. Those directions are the principal axes, the three numbers left are the principal moments, and the rotational energy becomes a sum of three squares.

The three principal moments classify the body: all different is an asymmetrical top; two equal is a symmetrical top, whose perpendicular pair of axes may be chosen freely; all three equal is a spherical top.

Two special cases: if the particles all lie in one plane, the principal moment about the perpendicular axis equals the sum of the other two; if they lie on a straight line, the third moment is zero and the rotator has only two rotational degrees of freedom.

Finally, the formulas above need the origin at the centre of mass, yet another origin is often easier to compute with: the two tensors differ only by a correction built from the total mass and the displacement.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式與名稱顯示於上方（名稱依語言切換）；主畫面為動畫。

- 第 0 句 / line 0: `T = ½ Σ m v²  ,   v = V + Ω × r`
- 第 1 句 / line 1: `T = ½ μ V² + ½ Σ m (Ω × r)²`
- 第 2 句 / line 2: `慣性張量` / `the inertia tensor` ＋ `Tᵣₒₜ = ½ Iᵢₖ Ωᵢ Ωₖ`
- 第 3 句 / line 3: `Iᵢₖ = Σ m ( r² δᵢₖ − xᵢ xₖ ) ／ I₁₁ = Σ m ( x₂² + x₃² ) ,   I₁₂ = − Σ m x₁ x₂`
- 第 4 句 / line 4: `座標軸一轉，九個分量就跟著變` / `turn the axes and all nine components change`
- 第 5 句 / line 5: `慣性主軸與主慣量` / `principal axes and principal moments` ＋ `Tᵣₒₜ = ½ ( I₁ Ω₁² + I₂ Ω₂² + I₃ Ω₃² )`
- 第 6 句 / line 6: `非對稱陀螺 ／ 對稱陀螺 ／ 球陀螺` / `asymmetrical / symmetrical / spherical top` ＋ `I₁ ≠ I₂ ≠ I₃    |    I₁ = I₂ ≠ I₃    |    I₁ = I₂ = I₃`
- 第 7 句 / line 7: `共面系統 ／ 共線系統（轉子）` / `coplanar system / collinear system (rotator)` ＋ `I₃ = I₁ + I₂        I₁ = I₂ , I₃ = 0`
- 第 8 句 / line 8: `換一個原點來算` / `computing about another origin` ＋ `I′ᵢₖ = Iᵢₖ + μ ( a² δᵢₖ − aᵢ aₖ )`

## 動畫 / Animation

主角是一塊由五個質點組成、會平移並自轉的平面剛體，右側是即時計算的慣性張量矩陣面板。

- 第 0 句：五個質點組成的剛體平板一邊平移、一邊自轉；每個質點畫出總速度 v（紅），外圈紫色弧箭頭標 Ω。
- 第 1 句：同樣的速度拆成兩段：由質點出發的平移速度 V（青）＋轉動貢獻 Ω × r（紫）頭尾相接；右側兩條能量長條即時顯示 ½μV²（會隨 V 脈動）與固定的轉動動能。
- 第 2 句：平移停止、物體定在原地自轉；出現黏在物體上的座標軸 x₁、x₂（青）與垂直紙面的 x₃（圓點記號），右側浮出 3 乘 3 矩陣：每格方塊的面積正比於該分量大小（對角橘、非對角依正負為青／紅）。
- 第 3 句：標出一個質點，畫出它到 x₁ 軸的垂直虛線（長度即 x₂），同時框住矩陣的 I₁₁ 格——轉動慣量就是質量乘垂直距離平方的總和。
- 第 4 句：座標軸相對物體慢慢轉動（α 從 0 掃到 2.55 弧度）：矩陣裡四個方塊即時脹縮，非對角格加紅框強調它們忽大忽小。
- 第 5 句：座標軸轉到主軸方向（α → π + 0.1195）：兩個非對角方塊同時縮成零，右側列出主慣量 I₁ = 3.3、I₂ = 8.1、I₃ = 11.5。
- 第 6 句：三個並排面板：不規則多邊形（非對稱陀螺，三根長條都不同）、正六邊形＋對稱軸（對稱陀螺，前兩根等高）、圓形＋三軸（球陀螺，三根等高）。
- 第 7 句：左：質點散布在一個平面上，垂直平面的 x₃ 軸；長條圖顯示 I₁ + I₂ = I₃。右：質點排成一直線（x₃ 軸），長條圖顯示 I₁ = I₂ 而 I₃ = 0。
- 第 8 句：剛體回到畫面，質心 O（青）之外再取一個體上固定的原點 O′，畫出位移向量 a（紅）；右側兩條長條比較 I₃ 與 I′₃，多出來的紅色段落標為 μa²。

矩陣面板的數值由場景直接以質點質量與座標算出（`_inertia(α)`），所以畫面上看到的脹縮與歸零都是真實的張量分量，不是示意動畫。
主軸角度 α\* = 0.1195 弧度由本例的質量分布解出，對應主慣量 (3.335, 8.134, 11.469)。
