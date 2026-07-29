# Persona 強制機制 — 補充說明

從 32 份 GPT feedback 看到 3 種反覆出現的扣分：
1. **節奏不對 grade**：「四個複雜概念在 30 秒內塞給 12 年級」
2. **Lacks 概念被當已知用**：MSE / regularization 沒定義就用
3. **Jargon 超載**：一支影片塞 8+ 個專有名詞給 9 年級

修正：在每個 lesson 設 `PERSONA` 並用 `self.teach_concept()` 引入 Lacks 概念。

## 必做兩件事

### 1. 設 `PERSONA`（從 course_requirement / student_persona 讀）

```python
from manim_lessons.lib.persona import Persona

class FullLesson(GeometryArchetype):
    PERSONA = Persona(
        grade=9,
        focus_minutes=15,
        has=["basic geometry", "triangle", "distance"],
        lacks=["incenter", "circumcenter", "optimization", "modeling"],
    )
    HEADING = "Triangle Centers"
    BRIDGE_HOOK = "三家咖啡店要建共同倉庫..."
    # ...
```

### 2. 用 `teach_concept()` 引入每個 Lacks 概念

```python
def teach(self):
    # 不是手寫 Text + Write — 用 teach_concept 強制三件套
    self.teach_concept(
        term="Circumcenter",
        definition="到三個頂點等距離的點",
        example="廣播塔覆蓋三個社區",
        visual=my_diagram,           # 可選, 任何 Mobject
        extra_dwell=2.0,              # 重要概念加碼停留
    )
    # ... 接下來就可以自由用 Circumcenter 一詞 ...
```

## 自動發生的事

`teach_concept` 會：
- **依 grade 強制 dwell**：9 年級 → 每概念 ≥ ~22s, 12 年級 → ~14s
- **登記** term 為已定義（避免「沒定義就用」扣分）
- **累積 jargon 計數**：超過 grade 預算（9→4, 10→5, 11→6, 12→7）就警告

`render` 結束時 console 會印違規清單，例如：
```
⚠ FullLesson Persona 違規清單:
   ❌ Lacks 概念從未被 teach_concept 引入: 'modeling'
   ⚠ 'incenter' 只 dwell 6.2s (建議 ≥22s)
```

## Persona 衍生數值（你不用算）

| Grade | min seconds/concept | jargon budget | 旁白語速 (中文字/分) |
|---|---|---|---|
| 9  | **20s** | 4 | 110 |
| 10 | **16s** | 5 | 125 |
| 11 | **13s** | 6 | 140 |
| 12 | **11s** | 7 | 155 |

數值是「每個 Lacks 概念至少要花的秒數」，不是平均。重要概念用 `extra_dwell=` 加碼。
影片總長度建議 ≈ `focus_minutes / 3`（剩下的時間留給學生做題）。

## 把舊 lesson 改造成 persona-aware（3 步）

1. 在 `class FullLesson` 上面加 `PERSONA = Persona(...)`
2. 找 `teach()` 裡引入新概念的 `Text(...) + Write(...)` 段落，改成 `self.teach_concept(term, definition, example=...)`
3. Render 後看 console — 若有違規，調整 dwell 或合併概念

> 一次只能改一個 lesson，但 `_base.py` 的 patch 是全包通用的。

## 題型 → Archetype 對照

| 題目類型 | Archetype |
|---|---|
| 三角形、函數圖形、幾何 | `GeometryArchetype` |
| 統計、機器學習指標、回歸 | `StatsArchetype` |
| 植物解剖、演化、生物結構 | `BiologyArchetype` |
| 能量守恆、量綱、Fermi | `PhysicsArchetype` |
| AI 方法演進、技術對比 | `MethodCompareArchetype` |
| **先打破誤解再給概念 (Overfitting / Limits / 任何 "misconception" 類)** | **`MisconceptionArchetype`** |
