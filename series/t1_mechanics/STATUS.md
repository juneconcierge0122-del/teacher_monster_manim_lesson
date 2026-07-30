# T1 —《Landau–Lifshitz 力學》

**狀態：已完結。** 第 4–52 課涵蓋 §4–§52（第 52 課是本書最後一節，條件週期運動），
第 53 課是全書總複習特輯。沒有「下一節」可接。

| 項目 | 值 |
|---|---|
| 課本 | `books/Landau_Lifshitz_T1.pdf`（另有 `_short` 版） |
| 場景檔 | `manim_lessons/lessons/t1_mechanics/landau_lNN_*.py` |
| 腳本 md | 同目錄的 `landau_lNN_*_script.md` |
| 旁白／公式 | `manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[NN]` 與 `FORMULAS[NN]` |
| 配音 | `manim_lessons/samples/audio_lNN/`（未進 git） |
| 配音生成 | `python manim_lessons/samples/generate_l04_l10_tts.py NN zh\|en <out_dir>` |
| 場景類別 | `LandauLNNZH` / `LandauLNNEN` |
| manifest | `series/t1_mechanics/manifests/youtube_lNN_manifest.json` |

共用底層留在 `manim_lessons/lessons/`（不屬於任何單一系列）：
`canonical_base.py`（第七章起的 `CanonicalBase` + `make()`）與
`landau_l04_l10.py`（`LandauBatchBase` 與公式舞台）。

渲染：先 `source .venv/bin/activate`，在 `manim_lessons/` 目錄下執行
`manim -qh --fps 60 lessons/t1_mechanics/landau_lNN_xxx.py LandauLNNZH`，
或用 `bash tools/queue.sh NN:landau_lNN_xxx.py`（會自動在系列子目錄裡找檔案）。

---

## YouTube 連結（全部設為私人）

| 課 | 主題 | 中文 | 英文 |
|---|---|---|---|
| 18 | 散射：從撞擊參數到截面 | （未記錄，見下方說明） | https://youtu.be/_pwVHOsrsCE |
| 20 | 小角度散射 | https://youtu.be/aK-DwdW4rS8 | https://youtu.be/VbIcOEkqlCQ |
| 21 | 一維自由振盪 | https://youtu.be/GmDzxL7PAcA | https://youtu.be/m-oxGVpTm7U |
| 22 | 受迫振盪與共振 | https://youtu.be/qsK8XCD5gNw | https://youtu.be/OIl0t-W6li0 |
| 23 | 簡正模態 | https://youtu.be/6miIGMXBsXc | https://youtu.be/mDbGGpObURI |
| 24 | 分子振動 | https://youtu.be/OjNK_3IbxDY | https://youtu.be/p0Au7AZoV5k |
| 25 | 阻尼振盪 | https://youtu.be/Oaen2BnQQBE | https://youtu.be/w9aTXyLU1Tc |
| 26 | 有阻尼受迫振盪 | https://youtu.be/RmzMDDqFLQ4 | https://youtu.be/BzpcO36JqCM |
| 27 | 參數共振 | https://youtu.be/ET5SSwIyXhU | https://youtu.be/Ua9ybHdlvtA |
| 28 | 非簡諧振盪 | https://youtu.be/iYscNo42Dc4 | https://youtu.be/iNxn5bF4eXE |
| 29 | 非線性共振 | https://youtu.be/BkBcgQZwcSc | https://youtu.be/A9lG2zLZYxo |
| 30 | Kapitza 倒立擺 | https://youtu.be/Om57rf26yDw | https://youtu.be/j4-2t_-bwOE |
| 31 | 角速度 | https://youtu.be/WduZLL2jymU | https://youtu.be/sqnhVl7gIXc |
| 32 | 慣性張量 | https://youtu.be/qBjmrb3oiKU | https://youtu.be/9bgPfuZF0oo |
| 33 | 角動量與規則進動 | https://youtu.be/tECuBBc06gs | https://youtu.be/x6DMO4HarZM |
| 34 | 剛體的運動方程 | https://youtu.be/cid5YtyFHuU | https://youtu.be/B-yItNOgF4A |
| 35 | 歐拉角 | https://youtu.be/kYd9xZWIc0E | https://youtu.be/YUEIXlpMpMM |
| 36 | 歐拉方程 | https://youtu.be/9ToBnSaUuV4 | https://youtu.be/UPvR2bAlwFM |
| 37 | 非對稱陀螺 | https://youtu.be/5Yl5kUZyQkA | https://youtu.be/ukEX_x2E5Oc |
| 38 | 剛體的接觸 | https://youtu.be/hChLtxn6u2U | https://youtu.be/H-dW9IEYJSA |
| 39 | 非慣性參考系 | https://youtu.be/DF--KGsnPyU | https://youtu.be/rVcqs2_a6S8 |
| 40 | 哈密頓方程 | https://youtu.be/HhiC7ug1U94 | https://youtu.be/ipuTa9w51Ww |
| 41 | 勞斯函數 | https://youtu.be/4HvXmPOyYkc | https://youtu.be/iO0sGN8G2mA |
| 42 | 帕松括號 | https://youtu.be/pUGr6L8s7Sw | https://youtu.be/ppenRRKgDPo |
| 43 | 作用量作為座標的函數 | https://youtu.be/w9JPelcVQDc | https://youtu.be/_o_tSpf5x0c |
| 44 | 莫佩爾蒂原理 | https://youtu.be/SmYw_m1Odyg | https://youtu.be/ST0SPiKvBm4 |
| 45 | 正則變換 | https://youtu.be/AKHCY45Vf04 | https://youtu.be/fsAK9Wu0Mzg |
| 46 | 劉維定理 | https://youtu.be/LNEGaThsHUQ | https://youtu.be/ktkOhRzuk6g |
| 47 | 漢彌頓－雅可比方程 | https://youtu.be/ulwnWyHbJFM | https://youtu.be/xAxfqnot4Mk |
| 48 | 分離變數 | https://youtu.be/Sok6AnLh72A | https://youtu.be/VkZgGDm-gGc |
| 49 | 絕熱不變量 | https://youtu.be/62XMvPk1JOM | https://youtu.be/HRAa1GzTRE0 |
| 50 | 正則變數 | https://youtu.be/7Xw8YBp_Dwc | https://youtu.be/GEro0nbwzkI |
| 51 | 絕熱不變量守恆的精確度 | https://youtu.be/mvQkO2QzZLY | https://youtu.be/T7dCr75-jyo |
| 52 | 條件週期運動 | https://youtu.be/uucag1tAUPQ | https://youtu.be/KVkZWuaEKTA |
| 53 | 《力學》全書總複習 | https://youtu.be/vhYGB52e01A | https://youtu.be/cd1qd7mKKYo |

**第 4–19 課**亦已完成並上傳，但連結沒有被記錄在這裡也不在 manifest 裡
（manifest 只是上傳的輸入，不含回傳的 video id）。要找的話翻當時 session 的
`UPLOAD_OK` 輸出，或直接到 YouTube Studio 的私人影片清單查。

2026-07-29：發現第 18 課的英文版當初沒有上傳成功，已用 `LandauL18EN` 重新渲染
（89.1s／1080p60）並補傳，連結記在上表。素材都還在（`samples/audio_l18/en/`、
`localization/landau_l04_l10.py` 的 `TOPICS[18]`），要重來只需再跑一次
`manim -qh --fps 60 lessons/landau_l04_l10.py LandauL18EN`。
**第 4–19 課其餘各課的中英版是否都真的在 YouTube 上，沒有紀錄可佐證，值得逐一核對。**

第 1–3 課（`landau_l01_sample*`、`landau_l02_action`、`landau_l03_galileo`）
是早期的原型／樣片，格式與第 4 課之後不同，保留在同一個目錄裡作為紀錄。
