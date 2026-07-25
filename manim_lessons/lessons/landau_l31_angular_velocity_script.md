# Landau Mechanics 31 — Angular velocity

> 《Landau–Lifshitz 經典力學》教學系列第 31 課（第六章「剛體運動」第一課，§31）
> 中文標題：角速度：剛體運動的第一步

## 繁體中文旁白

從這一章開始，我們研究剛體：一群彼此距離永遠不變的質點。要定出它的位置，需要三個座標指出質心在哪裡，再加三個角度指出它朝哪個方向。

所以剛體是一個有六個自由度的力學系統；描述它要用兩套座標系，一套是固定不動的慣性座標系，另一套牢牢黏在物體上、跟著它一起走，原點取在質心。

任何一個無限小的位移，都可以拆成兩步：先讓整個物體平移，把質心送到新位置；再繞著質心轉過一個無限小的角度。

把這個關係除以所花的時間，就得到剛體上任何一點的速度：質心的平移速度，加上角速度和該點位置向量的叉積。

這裡的角速度方向沿著轉軸，大小是每秒轉過的角度；離轉軸越遠的點，轉動貢獻的那一份速度就越大。

如果把黏在物體上的原點換到另一個點，平移速度會改變，但角速度完全不變；所以角速度是整個剛體的性質，我們可以直接叫它「物體的角速度」。

當平移速度垂直於角速度時，總能找到一個瞬間速度為零的點，通過它的軸就叫瞬時轉動軸；滾動的輪子就是最好的例子，接觸地面的那一點，在那一瞬間其實是靜止的。

## English narration

From this chapter on we study the rigid body: a set of particles whose mutual distances never change. Fixing its position takes three coordinates for where the centre of mass is, plus three angles for which way it faces.

So a rigid body is a mechanical system with six degrees of freedom, and describing it takes two coordinate systems: a fixed inertial frame, and a moving frame glued to the body itself, with its origin at the centre of mass.

Any infinitesimal displacement splits into two steps: first translate the whole body so the centre of mass reaches its new position, then rotate it through an infinitesimal angle about that centre.

Dividing this relation by the time it takes gives the velocity of any point of the body: the translational velocity of the centre of mass, plus the cross product of the angular velocity with that point's position vector.

The angular velocity points along the axis of rotation, and its magnitude is the angle turned per second; the farther a point sits from the axis, the more velocity rotation contributes.

If we move the body-fixed origin to some other point, the translational velocity changes, but the angular velocity does not change at all; it is a property of the whole body, which we simply call the angular velocity of the body.

When the translational velocity is perpendicular to the angular velocity, some point of the body always has zero velocity, and the axis through it is the instantaneous axis of rotation; on a rolling wheel, that is the point touching the ground.

## 畫面公式 / On-screen formulas

旁白為自然語言，數學式與名稱顯示於上方（名稱依語言切換）；主畫面為動畫。

- 第 0 句 / line 0: `| rᵢ − rₖ | = const`
- 第 1 句 / line 1: `3 平移 + 3 轉動` / `3 translations + 3 rotations` ＋ `3 + 3 = 6`
- 第 2 句 / line 2: `dr = dR + dφ × r`
- 第 3 句 / line 3: `v = V + Ω × r`
- 第 4 句 / line 4: `離軸越遠，轉動貢獻越大` / `farther from the axis, larger contribution` ＋ `Ω = dφ / dt`
- 第 5 句 / line 5: `角速度與原點的選擇無關` / `angular velocity is origin-independent` ＋ `V′ = V + Ω × a  ,   Ω′ = Ω`
- 第 6 句 / line 6: `瞬時轉動軸` / `instantaneous axis of rotation` ＋ `V′ = 0     ⟹     v = Ω × r′`

## 動畫 / Animation

主角是一塊在畫面中平移並自轉的剛體平板（四個質點 + 質心 O）。

- 第 0 句：質點間畫出虛線連桿，強調彼此距離恆定＝剛體條件。
- 第 1 句：左下角出現固定慣性座標系 X–Y（灰），質心處出現隨物體一起轉的體座標軸（青）。
- 第 2 句：畫出從固定原點到質心的向量 R，並在物體外圍加上一圈紫色轉動弧箭頭（標 dφ）——位移＝平移 R ＋ 繞質心轉 dφ。
- 第 3 句：取平板上一點 P，畫出向量三角形：由 P 出發的平移速度 V（青）＋ 轉動貢獻 Ω × r（紫）＝ 該點總速度 v（紅）；質心處另畫一支 V 作對照。
- 第 4 句：沿半徑方向排三個點（1/3、2/3、1 倍半徑），各自畫出 Ω × r；箭頭長度隨距離線性增長，轉動弧改標 Ω。
- 第 5 句：改用平板另一個點 O′ 當體座標原點，畫出 a 向量與同樣的三角形 V ＋ Ω × a ＝ V′；V′ 與 V 明顯不同，但轉動弧（Ω）只有一個。
- 第 6 句：切換到滾動的輪子——輪心速度 V（青）、輪頂速度 2V（紫）、與地面接觸點 v = 0（紅），該點即瞬時轉動軸。
