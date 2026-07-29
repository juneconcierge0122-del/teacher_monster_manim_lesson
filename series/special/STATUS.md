# SPECIAL — 特別篇

不屬於任何一本書的單集，編號用 `sNN`。目前只有一集。

| 項目 | 值 |
|---|---|
| 場景檔 | `manim_lessons/lessons/special/special_sNN_*.py` |
| 腳本 md | 同目錄的 `special_sNN_*_script.md` |
| 旁白／公式 | `manim_lessons/localization/special_topics.py` 的 `TOPICS_SPECIAL` 與 `FORMULAS_SPECIAL` |
| 配音 | `manim_lessons/samples/audio_sNN/`（未進 git） |
| 配音生成 | `manim_lessons/samples/generate_special_tts.py` |
| 場景類別 | `SpecialSNNZH` / `SpecialSNNEN` |
| manifest | `series/special/manifests/youtube_sNN_manifest.json` |

場景仍 subclass `manim_lessons/lessons/landau_l04_l10.py` 的 `LandauBatchBase`
（共用底層，不是 T1 專屬）。新的特別篇建議改用 `canonical_base.CanonicalBase`。

---

## 已完成

| 集 | 主題 | 中文 | 英文 |
|---|---|---|---|
| S01 | 可被說出的表徵：語言模型裡的全域工作空間（Anthropic 2026, Gurnee et al.） | 待補 | 待補 |

S01 原文：https://transformer-circuits.pub/2026/workspace/index.html

（S01 的 YouTube 連結沒有被記錄下來，manifest 只是上傳輸入、不含回傳的 video id。
到 YouTube Studio 的私人影片清單可以找到。）
