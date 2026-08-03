# advcalc —《Advanced Calculus》(Loomis & Sternberg)

**狀態：E00 已上傳（私人）。下一集 E01 從第 0 章第 1–3 節開始。**
全書解析與 155 集的分集規劃見 **[`OUTLINE.md`](OUTLINE.md)**。

## YouTube 連結（全部設為私人）

| 集 | 主題 | 對應書頁 | 片長（中／英） | 中文 | 英文 |
|---|---|---|---|---|---|
| E00 | 導論：這本書是什麼 | 序言與目錄 | 3:23 ／ 3:04 | https://youtu.be/LWLQa7elNII | https://youtu.be/15GYH9MB05U |

E00 的成品在 `manim_lessons/samples/output/advcalc_e00_{zh-TW,en}.mp4`
（1920×1080、60 fps、H.264 + AAC，已核對 log 的 `Rendered AdvCalcE00ZH/EN` 與兩支的實際語言）。

| 項目 | 值 |
|---|---|
| 課本 | `books/Advanced_Calculus.pdf`（Loomis & Sternberg, rev. ed. 1990，592 頁） |
| 場景檔 | `manim_lessons/lessons/advcalc/advcalc_eNN_*.py` |
| 腳本 md | 同目錄的 `advcalc_eNN_*_script.md` |
| 旁白／公式 | `manim_lessons/localization/advcalc.py` 的 `TOPICS_ADVCALC[NN]` 與 `FORMULAS_ADVCALC[NN]` |
| 配音 | `manim_lessons/samples/audio_eNN/`（未進 git） |
| 場景類別 | `AdvCalcENNZH` / `AdvCalcENNEN` |
| manifest | `series/advcalc/manifests/youtube_eNN_manifest.json` |

## 命名與編號

- 課號**自己從 1 開始**，寫成 `E01`、`E02`…（`e` = episode）。不接續 T1 的 53 課。
- 課號**不等於書上的節號**——這本書一節動輒 5–15 頁，依「切細」的方針一節會切成 1–3 集，
  所以每一集的標題與 manifest 描述裡都要寫清楚對應的**章.節與書頁**，例如
  「第 3 章第 6 節・書頁 140–146」。對應表在 `OUTLINE.md`。
- YouTube 標題前綴用「《高等微積分》第 N 集」／"Advanced Calculus, Episode N"，
  與 T1 的《力學》系列區隔。

渲染：先 `source .venv/bin/activate`，在 `manim_lessons/` 目錄下執行
`manim -qh --fps 60 lessons/advcalc/advcalc_eNN_xxx.py AdvCalcENNZH`，
或用 **`SCENE_PREFIX=AdvCalcE bash tools/queue.sh NN:advcalc_eNN_xxx.py`**
（`queue.sh` 預設前綴是 `LandauL`，這個系列一定要覆寫，否則會找不到場景名而靜默渲染 base class）。

## 取材：直接讀 PDF 頁面，**不要用 pdftotext**

PDF 是掃描 OCR 版，`pdftotext` 的數學符號幾乎全毀（`Δf_a`→`!!.fa`、`ℝ²`→`~2`、`α`→`Ci`），
插圖也整個消失。改成用 Read 工具直接讀頁面影像，一次最多 20 頁：

```
Read  books/Advanced_Calculus.pdf  pages="153-154"
```

**頁碼換算：PDF 頁 = 書頁 + 12。** 詳見 `OUTLINE.md`。

## 這個系列的動畫方向與 T1 不同

T1《力學》靠真實物理動畫；這本書前半是賦範向量空間上的抽象分析，沒有物理圖像。
動畫要改成解釋**結構**——映射的箭頭圖、包含與商的關係、誤差項如何隨 ‖ξ‖ 收縮、
座標卡的重疊、微分形式的拉回。到第 13 章回到古典力學時可以接回 T1 的視覺語言。

## 底層怎麼接（2026-07-31 已改好）

原本 `LandauBatchBase` 與 `canonical_base` 把 T1 的資料來源寫死了，現在抽成三個類別屬性
＋一個參數，**預設值完全等於原本的行為**，所以 T1 不受影響：

| 覆寫項目 | advcalc 的值 | 作用 |
|---|---|---|
| `TOPICS_SRC` | `TOPICS_ADVCALC` | 旁白與標題的來源 |
| `FORMULAS_SRC` | `FORMULAS_ADVCALC` | 畫面公式的來源 |
| `AUDIO_PREFIX` | `"e"` | 配音目錄變成 `samples/audio_e00/` |
| `make(cls, n, prefix=…)` | `make(cls, "00", prefix="AdvCalcE")` | 場景名 `AdvCalcE00ZH/EN` |

`make()` 的 `n` 是**原樣**貼進類別名的，所以要零填補就傳字串 `"00"`，而且傳什麼就要跟
`tools/queue.sh` 的編號一致（queue.sh 是字串串接）。`make()` 裡設 `__module__` 那行保留著，
那是防止 manim 靜默改渲染 base class 的關鍵。

配音生成器：`manim_lessons/samples/generate_advcalc_tts.py`（用法與 T1 那支相同）

```bash
python manim_lessons/samples/generate_advcalc_tts.py 0 zh manim_lessons/samples/audio_e00/zh-TW
python manim_lessons/samples/generate_advcalc_tts.py 0 en manim_lessons/samples/audio_e00/en
```

同一次改動也修好了 `LandauBatchBase._wrap_cjk`：它原本只看顯示寬度斷行，會把中文句子裡的
英文字拆開（`Courant` 斷成 `Cou` / `rant`）。現在遇到 ASCII 英數字連續段會整段推到下一行。
實測 386 條中文旁白（E00 + T1 全部）只有 2 條斷行結果改變，正好就是原本拆到英文字的那兩條。

製作規範一律見 `docs/PLAYBOOK.md`。
