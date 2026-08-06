# HANDOFF — 雙語教學動畫工作區

貼到新 session 的接手 prompt。**先讀這一頁，再讀對應的兩份檔案：**

- `docs/PLAYBOOK.md` — 製作流程、版面實測值、manim 的坑。**跨系列共用，每次動工都要看。**
- `series/<系列>/STATUS.md` — 該系列的進度、檔案位置、YouTube 連結。

**每一集都要走一次 `docs/PLAYBOOK.md` 第 8 節「著作權」。** 這些系列都是照著仍在版權內的
教科書做的，那一節是在確保成品是**導讀而不是重製**：書頁影像一格都不進成品、插圖自己重畫、
旁白自己寫不逐句翻、不做整本習題解答、PDF 不進 git、描述結尾帶免責聲明、影片維持私人。
它是每一集的檢查項，不是一次性的設定。

---

## 現在的狀態

| 系列 | 內容 | 狀態 |
|---|---|---|
| `series/t1_mechanics/` | Landau《力學》第 1–53 課 | **已完結**（第 52 課是本書最後一節，第 53 課是總複習） |
| `series/special/` | 特別篇 S01（Anthropic 全域工作空間論文） | 單集，可再加 |
| `series/t2_fields/` | Landau《場論》 | **尚未開始**，開工前的決定寫在它的 STATUS.md |
| `series/advcalc/` | Loomis & Sternberg《Advanced Calculus》 | **進行中**：E00–E15 已上傳（第 0 章完結，第 1 章做到第 5 節中段） |

**現在的方向是 `advcalc`。**《力學》已完結；《場論》仍是空殼。
接手時先讀 `series/advcalc/STATUS.md`（進度、連結、踩過的坑）與
`series/advcalc/OUTLINE.md`（全書解析與 169 集規劃）。

**下一步是 E16**，第 1 章第 5 節的最後一段（書頁 61–67）：解線性方程與 Theorem 5.3、
T 的多項式、Theorem 5.4 與 5.5。做完第 5 節之後，第 6 節「雙線性」（書頁 67–71）是 E17。
到 E15 為止，實際集數都與 OUTLINE 的預估相符。
**OUTLINE 的集數仍然是估的，動工前先照書核一次**——那張表錯過一次（見 advcalc 的 STATUS.md）。

`advcalc` 有三件與其他系列不同、會踩雷的事：

- **取材不要用 `pdftotext`**：那個 PDF 是掃描 OCR 版，數學符號幾乎全毀、插圖全失。
  改用 Read 工具直接讀頁面影像（`pages="153-154"`，一次最多 20 頁）。**PDF 頁 = 書頁 + 12。**
- **`queue.sh` 要覆寫場景前綴**：`SCENE_PREFIX=AdvCalcE bash tools/queue.sh …`，
  預設的 `LandauL` 會找不到場景名而讓 manim 靜默改渲染 base class。
- **場景類別要用 `make(cls, "NN", prefix="AdvCalcE")`**，並在類別上覆寫
  `TOPICS_SRC` / `FORMULAS_SRC` / `AUDIO_PREFIX = "e"`。細節見 advcalc 的 STATUS.md。

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
  提交直接進 `main`，這個 repo 一直是這樣。
- YouTube、GitHub 憑證都在 `.secrets/`，**請勿顯示憑證內容**。
- YouTube token 只有上傳權限、**無法刪片**；被取代的舊版需人工在 YouTube Studio 刪除。

**兩個憑證都會定期失效，動工前先測，不要等到最後一步才發現：**

```bash
# YouTube：能 refresh 就可用
.venv/bin/python -c "
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
c=Credentials.from_authorized_user_file(Path('.secrets/youtube_token.json'),
  ['https://www.googleapis.com/auth/youtube.upload'])
c.refresh(Request()); Path('.secrets/youtube_token.json').write_text(c.to_json())
print('YouTube OK', c.expiry)"

# GitHub：200 才可用
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $(tr -d '\n' < .secrets/github_juneconcierge0122-del_teacher_monster_manim_lesson)" https://api.github.com/user
```

- **YouTube 的 refresh token 每 7 天就失效**，因為那個 OAuth app 在 Google Cloud Console
  的發布狀態還是「測試中」。失效時走兩段式重新授權（產生 authorization_url →
  使用者貼回 `http://localhost/?code=...` → `fetch_token`），注意 PKCE 的 `code_verifier`
  與 `state` 必須跨進程存下來，否則換不到 token。根治方式是把同意畫面改成「正式版」，
  但那要使用者自己在 Console 操作。
- GitHub 的 fine-grained PAT 也會過期（回 401）。需要使用者重發，權限是
  Contents: Read and write。
