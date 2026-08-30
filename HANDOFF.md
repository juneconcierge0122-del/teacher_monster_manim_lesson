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
| `series/advcalc/` | Loomis & Sternberg《Advanced Calculus》 | **進行中**：E00–E53 已上傳，E54–E58 待渲染（第 0 到 3 章完結，第 4 章做到第 4 節完） |

**現在的方向是 `advcalc`。**《力學》已完結；《場論》仍是空殼。
接手時先讀 `series/advcalc/STATUS.md`（進度、連結、踩過的坑）與
`series/advcalc/OUTLINE.md`（全書解析與 169 集規劃）。

**眼前第一件事是 E59**，接第 4 章第 5 節「緊緻性與均勻性」（書頁 210 起）。
E44–E48 已經把 §10 與 §11 收完了（定理 10.1、10.2、11.1 到 11.5：極值與臨界點、切平面、
隱函數的微分、反映射定理，以及那兩條定理的笛卡兒形式；實際收在書頁 169，
169–171 是習題 11.1–11.29，依第 8 節不做解答）。
**第 3 章不是到 §11 為止**——後面還有 §12 到 §17 共七集，寫收尾那一拍時
先回頭看一次 `OUTLINE.md` 的章節表（E48 的旁白初稿就把這件事寫錯了）。
OUTLINE 把 §9 排成兩集、§10 排成一集，實際上反過來；到 E48 為止總集數仍與 OUTLINE 一致。
**OUTLINE 的集數仍然是估的，動工前先照書核一次**——那張表的頁碼錯過四次（見 advcalc 的 STATUS.md）：
它的「書頁」欄含各節的習題頁，實際內容比表上少。

**有三道檢查，三道都要跑，而且都要跑到 0：**

```bash
cd manim_lessons
../.venv/bin/python tools/bounds.py   lessons/advcalc/<檔名>.py AdvCalcE<NN>  # 跑出畫面外
../.venv/bin/python tools/collide.py  lessons/advcalc/<檔名>.py AdvCalcE<NN>  # 疊在一起
../.venv/bin/python tools/langscan.py advcalc <NN>                            # 混語
```

`langscan.py` 是 2026-08-29 加的，掃 `FORMULAS` 與場景裡 `_sym`／`(label, colour)`
這兩種「兩個語言版本會渲染成同一個樣子」的字串。這類錯已經出現五次
（E42 的 `_sym` 夾中文、E47 的 `on M`／`injective`／`open`、E50 的 `on M` 與 `range dF`、
E52 表格裡的 `closed form`／`line`／`length`），而 `bounds` 與 `collide` 都看不到它，
在剛好對的那個語言下每一張 probe 幀也都正常。

**三道工具全過之後還要看 probe 幀**——這一輪五集裡，三道工具全是 0 的情況下，
probe 幀仍抓到十處版面問題（曲線間距太小糊成一條、矩陣擠成一排括號、
標籤放在自己那一列下面而讀成下一列的、刪除線畫在兩列之間、表頭建好卻沒傳進去、
省略號印在方塊上、兩個矩陣其實是同一個）。

`collide.py` 是 2026-08-25 加的，補 `bounds.py` 看不到的那一半（線壓在字上、字疊字）。
E27 與 E28 各為這類錯重渲過一次，一次 50 分鐘。

**但兩支工具都看不到「圖畫錯了」，所以 probe 幀還是要看。** E34–E38 這一輪裡，
兩支工具跑到 0 之後，probe 幀又抓到四件事：三支共線的箭頭互相蓋掉只剩一支看得見、
密的網格把疏的網格吃掉、曲線被 `min()` 截成平台加懸崖、一張圖小到讀不出內容。
規則是：**bounds → collide → probe 幀，三關都過才送 1080p。**

**probe 渲染要加 `--media_dir` 指到別的地方**，否則會跟正在跑的 1080p 搶 `media/texts` 這個
共用的字型快取。加了之後就能一邊渲染上一集、一邊 probe 下一集。

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
  **`queue.sh` 是用 `bash` 開新 shell 跑的，不會繼承 venv**——沒有先 activate 的話
  它會兩個場景都 `FAIL`，log 裡只有一行「manim：命令找不到」，看起來很像場景名錯了。
  在非互動環境（背景執行）裡直接帶：
  `PATH="$PWD/../.venv/bin:$PATH" SCENE_PREFIX=… bash tools/queue.sh …`。
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
