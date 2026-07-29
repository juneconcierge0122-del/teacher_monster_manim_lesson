# HANDOFF — 雙語教學動畫工作區

貼到新 session 的接手 prompt。**先讀這一頁，再讀對應的兩份檔案：**

- `docs/PLAYBOOK.md` — 製作流程、版面實測值、manim 的坑。**跨系列共用，每次動工都要看。**
- `series/<系列>/STATUS.md` — 該系列的進度、檔案位置、YouTube 連結。

---

## 現在的狀態

| 系列 | 內容 | 狀態 |
|---|---|---|
| `series/t1_mechanics/` | Landau《力學》第 1–53 課 | **已完結**（第 52 課是本書最後一節，第 53 課是總複習） |
| `series/special/` | 特別篇 S01（Anthropic 全域工作空間論文） | 單集，可再加 |
| `series/t2_fields/` | Landau《場論》 | **尚未開始**，開工前的決定寫在它的 STATUS.md |

**《力學》已經做完，沒有「下一節」可接。** 下一步需要先決定方向：

- (a) 接《場論》T2 —— 見 `series/t2_fields/STATUS.md`，編號方式要先拍板；
- (b) 針對《力學》挑主題做加深的專題集（例如把每章的習題做成一集）；
- (c) 其他。

除非使用者已經指定，請先問清楚再動工。

---

## 工作區地圖

```
.
├── docs/PLAYBOOK.md              製作規範與踩雷筆記（跨系列）
├── series/<系列>/
│   ├── STATUS.md                 該系列的進度與 YouTube 連結
│   └── manifests/                youtube_*_manifest.json
├── books/                        課本 PDF（未進 git）
├── youtube_upload.py             上傳腳本（在 repo 根目錄執行）
├── manim_lessons/
│   ├── lessons/
│   │   ├── canonical_base.py     共用底層：CanonicalBase + make()
│   │   ├── landau_l04_l10.py     共用底層：LandauBatchBase + 公式舞台
│   │   ├── t1_mechanics/         《力學》場景檔 + 腳本 md
│   │   ├── special/              特別篇場景檔 + 腳本 md
│   │   └── sandbox/              早期的非 Landau demo（triangle_centers 等，已不維護）
│   ├── localization/             各課旁白與公式（TOPICS / FORMULAS）
│   ├── lib/                      design_tokens、narrator、checks…
│   ├── tools/                    probe / grab / subtop / queue
│   ├── samples/                  配音（audio_*）與輸出（output/），皆未進 git
│   └── media/                    manim 渲染快取，未進 git
└── archive/my_service/           舊專案，與本系列無關，僅保留紀錄
```

**新系列開工時**：在 `manim_lessons/lessons/` 底下開一個新的系列目錄（記得放 `__init__.py`），
manifest 放進 `series/<新系列>/manifests/`，並建一份 STATUS.md。共用底層留在 `lessons/` 根目錄。

---

## 環境

- 先 `source .venv/bin/activate`。
- 渲染指令在 `manim_lessons/` 目錄下執行：
  `manim -qh --fps 60 lessons/<系列>/<課名>.py <場景類別>`
  或 `bash tools/queue.sh NN:<課名>.py`（會自動在系列子目錄裡找檔案；
  換系列時用 `SCENE_PREFIX=` 換場景名前綴）。
- 上傳指令在 **repo 根目錄**執行（manifest 裡的 `file` 是相對於根目錄的路徑）。
- 系統無 ffprobe/ffmpeg，用 imageio_ffmpeg 附的：
  `/home/r08849002/miniconda3/envs/teacher-monster/lib/python3.10/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`

## Git 與憑證

- Git metadata 在 `.git-backup`，所有 git 指令要用：
  `git --git-dir=.git-backup --work-tree=. …`（推送用 `GIT_ASKPASS=.secrets/github-askpass.sh`）。
- YouTube、GitHub 憑證都在 `.secrets/`，**請勿顯示憑證內容**。
- YouTube token 只有上傳權限、**無法刪片**；被取代的舊版需人工在 YouTube Studio 刪除。
