# manim_lessons

3Blue1Brown 風格的教學影片產線, 為比賽量身打造.

## Architecture

```
manim_lessons/
├── lib/                    # 基礎元件 (各 archetype 共用)
│   ├── design_tokens.py        — 顏色、字型、間距常數
│   ├── narrator.py             — 旁白 + 字幕同步
│   ├── construction.py         — 幾何構造 (中垂線、角平分線、外心、內心)
│   ├── value_panel.py          — 即時量條 (KE/PE)
│   ├── data_cloud.py           — 1000 點資料雲
│   ├── timeline.py             — 演進時間軸
│   └── checks.py               — 自動防呆 (placeholder / KLP coverage)
├── archetypes/             # 5 種 lesson 母模板
│   ├── _base.py                — LessonArchetype (處理 intro/outro)
│   ├── geometry.py             — A: 幾何題 (Triangle Centers, Quadratic)
│   ├── stats.py                — B: 資料統計 (Confusion Matrix, Regression)
│   ├── biology.py              — C: 生物結構 (Plant Anatomy, Speciation)
│   ├── physics.py              — D: 物理守恆 (Energy, Dimensional Analysis)
│   └── method_compare.py       — E: 方法演進 (AI Methods)
├── lessons/                # 每題一個檔案 (繼承對應 archetype)
│   ├── triangle_centers.py     — Geometry archetype 範例
│   └── confusion_matrix.py     — Stats archetype 範例
└── render.sh               # 批次渲染 + preflight checks
```

## Quick Start

```bash
# 安裝
pip install manim

# 預覽 (低畫質, 快)
./render.sh -l triangle_centers

# 全部高畫質渲染 (慢)
./render.sh -q h

# 單獨跑某個 scene
manim -pql lessons/triangle_centers.py S02_Circumcenter
```

## 自我測試各模組

每個 lib/ 檔案底部都附 `_DemoXxx` scene, 可以單獨跑:

```bash
manim -pql manim_lessons/lib/design_tokens.py _DemoSwatches
manim -pql manim_lessons/lib/construction.py _DemoConstruction
manim -pql manim_lessons/lib/value_panel.py _DemoEnergyPanel
manim -pql manim_lessons/lib/data_cloud.py _DemoConfusionCloud
manim -pql manim_lessons/lib/timeline.py _DemoTimeline
manim -pql manim_lessons/lib/timeline.py _DemoDivergence
manim -pql manim_lessons/lib/narrator.py _DemoNarrator
```

## 寫一個新 lesson (3 步驟)

### Step 1: 找對應的 archetype
| 題目類型 | Archetype |
|---|---|
| 三角形、函數圖形、幾何 | `GeometryArchetype` |
| 統計、機器學習指標、回歸 | `StatsArchetype` |
| 植物解剖、演化、生物結構 | `BiologyArchetype` |
| 能量守恆、量綱、Fermi | `PhysicsArchetype` |
| AI 方法演進、技術對比 | `MethodCompareArchetype` |

### Step 2: 在 `lessons/` 開新檔案

```python
# lessons/your_topic.py
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim_lessons.archetypes.geometry import GeometryArchetype
from manim_lessons.lib.design_tokens import VERTEX_CLR, INK

class FullLesson(GeometryArchetype):
    HEADING = "你的標題"
    DEFINITION = "一句話定義"
    ACCENT = VERTEX_CLR
    BRIDGE_HOOK = "從學生熟悉的概念出發..."   # Persona Has → Lacks
    CONCLUSION = "收尾的關鍵問題"

    def teach(self):
        # 寫真內容. 千萬不要寫 "Define X" 這種 meta 句!
        # 用 self.draw_triangle(...), self.show_decision_table(...) 之類的 helper
        pass
```

### Step 3: 寫對應的 `lessons/your_topic_script.md`
完整旁白稿. `render.sh` 會自動跑 preflight check, 確保:
- 沒有 placeholder 殘留
- 沒有截斷字 (`Defi`, `Bloo`, etc)
- 每個 KLP 都有覆蓋
- Topic 字眼出現次數足夠

## 設計原則 (從 ensemble_feedback 反推)

1. **每張畫面都動** — 純文字 = `Ineffective Visual −1.0`
2. **每個概念都有「定義 + 視覺化 + 例子」** — 缺一個 = scaffold fail
3. **顏色一致性** — 同一概念整支影片用同一顏色 (見 `design_tokens.py`)
4. **音畫對齊** — 用 `self.narrator.say(text, duration)` 而不是 `self.wait()`
5. **沒有 meta 句** — 不要寫 "Define the central term", 直接寫定義
6. **Persona 橋接** — `BRIDGE_HOOK` 從 `Has` 出發連到 `Lacks`

## 旁白後製建議

`narrator.say(text, duration)` 只控制字幕, 沒有實際聲音. 兩種對接方式:

**方案 A: 全自動 TTS (ElevenLabs)**
- 把所有 `narrator.say()` 抽出旁白文字 + duration
- 送 ElevenLabs API → 收 wav
- 用 `ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac out.mp4` 合成

**方案 B: 人工錄音 (engagement 滿分)**
- 用 `narrator.say()` 留白標記時間
- 對著影片時間碼錄
- 推薦工具: Audacity (免費), Descript (有 AI 修飾)

## License

寫完比賽要不要開源你決定. 我們等你拿冠軍 🏆
