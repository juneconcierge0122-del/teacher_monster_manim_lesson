# advcalc —《Advanced Calculus》(Loomis & Sternberg)

**狀態：E00–E03 已上傳（私人），涵蓋第 0 章 §1–9（書頁 1–15）。
下一集 E04 是第 0 章 §10–12（書頁 15–21），第 0 章還差這一集才算做完。**
全書解析與 169 集的分集規劃見 **[`OUTLINE.md`](OUTLINE.md)**。

## YouTube 連結（全部設為私人）

| 集 | 主題 | 對應書頁 | 片長（中／英） | 中文 | 英文 |
|---|---|---|---|---|---|
| E00 | 導論：這本書是什麼 | 序言與目錄 | 3:23 ／ 3:04 | https://youtu.be/LWLQa7elNII | https://youtu.be/15GYH9MB05U |
| E01 | 邏輯、量詞與連接詞 | 0.1–0.3（1–6） | 3:32 ／ 3:10 | https://youtu.be/5fo36U5Z5Js | https://youtu.be/Y0t9tJKJZYs |
| E02 | 集合、受限變數與關係 | 0.4–0.6（6–10） | 3:46 ／ 3:23 | https://youtu.be/lV2MJgo0PtQ | https://youtu.be/GQGSpeuBGvA |
| E03 | 函數、映射與合成 | 0.7–0.9（10–15） | 3:40 ／ 3:16 | https://youtu.be/f5ULzGZHEs0 | https://youtu.be/AE7ZSIrWG7E |

成品在 `manim_lessons/samples/output/advcalc_eNN_{zh-TW,en}.mp4`
（1920×1080、60 fps、H.264 + AAC）。每一支都核對過 log 的 `Rendered AdvCalcENNZH/EN`、
中英片長各自對得上自己的配音（若誤渲染成 base class，兩支片長會一模一樣），以及抽幀確認語言。

## 待處理：E03 的線上描述寫錯了

`youtube_e03_manifest.json` 的描述句尾寫「也是第 0 章的最後一集」／"finishing chapter 0"，
但第 0 章有 12 節、到書頁 21，E03 只做到 §9（書頁 15）。manifest 檔案已改正，
**但兩支影片已經上傳，線上描述還是舊的**。YouTube token 的 scope 只有
`youtube.upload`，改描述要 `youtube` 或 `youtube.force-ssl`，所以腳本改不動——
需要人工到 YouTube Studio 修這兩支的描述：
中文 https://youtu.be/f5ULzGZHEs0 、英文 https://youtu.be/AE7ZSIrWG7E

## 做這個系列時踩到的坑

- **分集規劃的加總要用腳本核，不要用眼睛加**。OUTLINE 原本第一階段小計寫 41 集、
  總計寫 155 集，實際逐節加總是 55 與 169；HANDOFF 也一度寫「第 1 章共 8 集」，
  實際是 13 集。連帶讓「第 0 章做完」這個錯誤說法一路寫進了 E03 的影片描述。
  改集數時，OUTLINE 的 E 編號欄、小計、總計三處要一起重排。

- **場景檔用到的 manim 類別沒 import，`import` 檢查抓不到**——那是方法內的執行期 `NameError`，
  只有真的渲染才會爆。更糟的是渲染失敗時 `tools/grab.py` 會照樣從**上一支殘留的
  `Probe*.mp4`** 抽幀，看起來像是新的構圖。probe 前先 `rm` 舊檔，並核對 `Rendered Probe<L>`；
  另外用 `python -m pyflakes lessons/advcalc/*.py` 靜態掃一遍，這類錯誤一次抓完。
- **畫面很容易變成把公式列再寫一次**。`formula()` 已經把 `MODE_LABEL` 與 `FORMULAS` 印在上方，
  中間的圖如果只是重排同樣的式子，那一拍等於沒有畫面。抽幀複查時要特別看這件事——
  E01 有三拍、E02 有兩拍、E03 有一拍都犯過。
- **英文字幕的 4 行上限要用 `textwrap` 實算，不能只看字元數**：285 字元的句子照樣可能換到 5 行。

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
