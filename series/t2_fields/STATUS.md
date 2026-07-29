# T2 —《Landau–Lifshitz 場論》

**狀態：尚未開始。** 這是預先開好的空殼，開工前先確認下面的決定。

| 項目 | 值 |
|---|---|
| 課本 | `books/Landau_Lifshitz_T2.pdf`（另有 `_short` 版） |
| 場景檔 | `manim_lessons/lessons/t2_fields/`（尚未建立） |
| manifest | `series/t2_fields/manifests/` |

## 開工前要決定的事

1. **編號怎麼接。** 兩種選擇：
   - 接續 T1 從第 54 課開始（`landau_l54_*`、`LandauL54ZH`）——
     好處是 YouTube 上一條連續的課號；壞處是課號與《場論》的節號對不起來。
   - T2 自己從 1 開始（`t2_l01_*`、`T2L01ZH`）——
     好處是課號 = 節號、系列邊界乾淨；壞處是與已上傳的 53 課編號重疊，標題要寫清楚是哪一本。

   **建議走第二種**，並在標題前綴「《場論》第 N 課」。目錄與 manifest 已經照系列分開，
   所以檔名重疊不會有問題；`tools/queue.sh` 也支援用 `SCENE_PREFIX=T2L` 換場景名前綴。

2. **localization 檔怎麼放。** T1 的 `TOPICS`／`FORMULAS` 全擠在
   `manim_lessons/localization/landau_l04_l10.py` 一個檔裡（50 課、很大）。
   T2 建議另開 `manim_lessons/localization/t2_fields.py`，別再往同一個檔堆。

3. **底層要不要動。** `canonical_base.CanonicalBase` 是語言／學科無關的，直接沿用即可。
   `EPISODE` 目前只用來查 `FORMULAS` 與組配音目錄名，換 localization 檔時要一併確認。

製作規範一律見 `docs/PLAYBOOK.md`。
