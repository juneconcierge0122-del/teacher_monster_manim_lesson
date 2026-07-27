# HANDOFF — Landau–Lifshitz 雙語教學影片

貼到新 session 的接手 prompt。**進度：已完成第 48 課（第七章「正則方程」§48 分離變數）。下一步：第 49 課（§49 絕熱不變量）。**

---

請繼續製作 Landau–Lifshitz《經典力學》雙語教學影片。

專案路徑：
/datadrive/r08849002/teacher_monster_manim_lesson

目前已完成到第 48 課（第七章「正則方程」§48 分離變數）。請從**第 49 課**開始（§49 絕熱不變量）。

請沿用既有流程：
1. 先查看專案、Git 狀態與上一課設定；用 pdftotext 讀 books/Landau_Lifshitz_T1.pdf 取得下一節內容。
2. 依書中下一節撰寫繁體中文及英文腳本，寫進 `manim_lessons/localization/landau_l04_l10.py` 的 `TOPICS[課號]`，公式寫進同檔的 `FORMULAS[課號]`。
3. 每個版本控制在 5 分鐘以內（第 32 課起放寬；先用 `av` 估算配音總長）。舊規範為 60–100 秒（先用 `av` 估算配音總長 + 0.6~0.8 秒尾巴；太短就補充旁白、太長就精簡）。
4. **旁白＝字幕＝配音用白話自然語言**（不要把 ∫、√、⊥ 等符號塞進旁白，TTS 會念錯）；數學式用放大的 unicode Text 放在畫面上方（`FS_H2`、`ACCENT_A`）。乘號用 ×、清楚的括號與上下標間距，二階導數用 Leibniz 記法 `d²x/dt²`（避免組合雙點在大寫字母上變淡）。
5. 英文字幕固定 22pt（`FS_BODY`），長句由 `self.text()` 自動 textwrap 換行，不縮太小。
6. **盡量用真實動畫解釋物理**（這是這系列的重點）：簡單主題可用「公式舞台」（見 `landau_l04_l10.py` 的 `_construct_formula_stage`）；有物理圖像的主題請新開客製場景檔 `manim_lessons/lessons/landau_lNN_xxx.py`，subclass `LandauBatchBase`，用 `ValueTracker` 時間軸 + updater / `always_redraw` 做動畫（可參考 l22 彈簧共振、l23 簡正模態、l25 阻尼曲線、l27 鞦韆、l29 折疊共振、l30 Kapitza 倒立擺、l31 剛體平板與滾動輪、l32 即時慣性張量矩陣、l33 軸測投影的進動陀螺、l34 拋物飛行的剛體與即時力矩長條圖、l35 兩個座標系與三次接續轉動的歐拉角、l36 數值積分出來的 polhode、l37 橢球與球面交出的整族 polhode、l38 沿封閉路徑滾一圈換了朝向的球、l39 轉盤上同一段運動的兩個視角、l40 勒讓德變換的切線幾何與相空間流、l41 循環座標與有效位能、l42 守恆量等值線沿著流、l43 波前與光線＋q–t 圖上累積的作用量）。
   - **第七章起請 subclass `manim_lessons/lessons/canonical_base.py` 的 `CanonicalBase`**：它已經包含 `beat()`、`formula()`、`sub()`、`_row()`／`_mid()`（會自動縮到 x ≤ 6.3）、`_arr()`／`_dash()`／`_curve()`（會自動降取樣）、`_axes()` 與 `construct()`。新課只要設 `EPISODE`、`MODE_LABEL`，並實作 `stage()` 回傳十組 `(fin, fout)`，最後用 `make(cls, NN)` 產生 ZH／EN 兩個場景類別（見 l42–l48）。
   - `stage()` 的每一組可以加**第三個元素：一個在該拍開始前執行的 callable**。`stage()` 只在一開始求值一次，所以要在拍與拍之間改變狀態（例如 `self.mode`，或記下某個動畫自己的起始時間）只能用它——寫在 `stage()` 裡面會在建構當下就全部執行完（見 l45 的 `mode()` 與 l46 的 `tflow0`）。
7. 產生中英文配音（`python manim_lessons/samples/generate_l04_l10_tts.py NN zh|en <out_dir>`）並渲染 1080p60、H.264/AAC。**先用 `-ql --fps 15` 低畫質試算除錯、抽幾張關鍵幀確認動畫**，再用 `-qh --fps 60` 出正式版。
8. 抽查中英文字幕、數學式、片長及畫面（用 imageio_ffmpeg 的 ffmpeg 抽幀；系統無 ffprobe/ffmpeg，路徑：`/home/r08849002/miniconda3/envs/teacher-monster/lib/python3.10/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`）。
9. 把畫面公式裡任何「語言相關的文字」（模態名稱等）用場景內的 `MODE_LABEL` 字典依語言切換，**不要寫死在共用的 `FORMULAS` 裡**（否則英文版會出現中文）。
10. 建 `youtube_lNN_manifest.json`（**簡介與標題不可含 `<`、`>`，YouTube 會擋 invalidDescription**；用「小於／大於」或「smaller/larger than」）。用既有憑證上傳兩部影片，設為私人：`python youtube_upload.py --client-secret .secrets/youtube_client_secret.json --token .secrets/youtube_token.json --manifest youtube_lNN_manifest.json`。
11. 產生每課獨立雙語腳本 md（`manim_lessons/lessons/landau_lNN_xxx_script.md`，含旁白、畫面公式、動畫說明）。
12. 將程式碼、腳本、manifest 提交並推送到既有 GitHub repository。
13. 上一課確認後，清除該課的本機影片與 Manim 渲染快取（`rm -rf manim_lessons/media/videos/landau_lNN_xxx` 及 `samples/output/landau_lNN_*.mp4`），但**保留程式碼與配音**（`samples/audio_lNN`）。
14. 完成後提供中英文 YouTube 連結、片長及 Git commit。

重要狀態：
- 第 48 課中文：https://youtu.be/Sok6AnLh72A
- 第 48 課英文：https://youtu.be/VkZgGDm-gGc
- 最新 Git commit：見 git log（第 43 課）
- YouTube、GitHub 憑證都在專案的 `.secrets` 內，請勿顯示憑證內容。
- Git metadata 位於 `.git-backup`，Git 指令需使用：`git --git-dir=.git-backup --work-tree=.`（推送用 `GIT_ASKPASS=.secrets/github-askpass.sh`）。
- 環境：先 `source .venv/bin/activate`。渲染指令在 `manim_lessons/` 目錄下執行（`manim -qh --fps 60 lessons/landau_lNN_xxx.py LandauLNNZH`）。
- 目前設計慣例：標題在上、公式在上方、白話字幕在下、動畫置中；顏色用 `manim_lessons/lib/design_tokens.py`（`ACCENT_A` 橘黃、`ACCENT_B` 青、`ACCENT_C` 紫、`WARN` 紅、`DIM/GHOST` 灰）。
- YouTube token 只有上傳權限、無法刪片；被取代的舊版需人工在 YouTube Studio 刪除。
- **英文字幕行數上限 4 行**：`self.text()` 對英文以 72 字元 textwrap，5 行時字幕頂端會升到 y ≈ −1.7 蓋住動畫；英文每句請控制在 ~285 字元內，動畫元素也盡量保持在 y ≥ −1.75。
- `beat()` 內的 `self.play()` **不要**在 play 層傳 `rate_func`，會覆蓋各動畫自己的 rate_func（改用 `tracker.animate(rate_func=...)`）。
- **公式區三行會撞到標題**：`formula()` 已改成行數大於 2 時自動下移；仍建議一課最多兩行。三行公式的下緣約在 y ≈ 1.45，**動畫元素與標籤要壓在 y ≤ 1.3**（l35 因為這樣把軸長從 1.72 縮到 1.50；第 8 拍的 x₃ 標籤在物體軸接近鉛直時仍會擦到公式，可接受但下次可再留多一點）。
- **英文標籤比中文寬約兩倍**：畫面內的雙語標籤（`self.lab()`）要分別檢查英文版是否貼到邊緣（安全範圍 |x| ≤ 6.3）。
- 3D 感的場景可用軸測投影（見 l33 的 `_proj()`：EX/EY/EZ 三個螢幕基向量），球面／圓錐用取樣點 + `set_points_as_corners` 畫。
- **`always_redraw` 裡絕對不要用 `DashedLine`**：虛線段數由長度決定，長度一變 submobject 數就變，會打亂同一個 VGroup 被 `FadeIn` 時的家族對齊，**相鄰 `Text` 的字母會被靜默吃掉**（l34 英文版第 7 拍字幕曾少掉開頭 7 個字母，中文版因為字數較少而正常）。改用固定 `num_dashes` 的 `DashedVMobject`（見 l34 的 `_dash()`）。同理，任何在 `always_redraw` 裡會改變 submobject 數量的物件都要避免。
- 除錯這類「畫面元素被吃掉」的問題時，可用一個 subclass 覆寫 `dur()` 回傳固定 1.2 秒、`add_sound()` 設成 no-op，就能在一分鐘內重跑整支影片抽幀比對。**每一課都建議先用這個快速 harness 檢查十拍構圖，再送 `-qh`**（1080p60 一支要 20~25 分鐘）。
- **英文標籤寬度要逐條量**：寫一個 subclass 覆寫產生面板文字的方法（`_row()` / `_txt()`）並印出 `get_right()`，用 `-s` 跑一次就能一次抓出所有超出 x = 6.3 的行（l36 第 9 拍原本三行全超出，其中一行直接被畫面切掉）。
- 需要真實軌跡時（如 l36 的 polhode），在 import 時用 RK4 積分一次存成陣列，updater 只查表：既可重現又不會有逐格積分的漂移。選初始條件時要離分界線夠遠，否則軌跡會亂掃整個相空間。
- **數值積分出來的曲線一定要先降取樣再畫**：軌跡動輒數千點，直接餵給 `set_points_as_corners()` 會讓渲染慢到不可用（l37 一開始 480p15 預覽十分鐘都跑不完）。170 點以內就夠平滑；同一張圖上有二十幾條曲線時尤其要注意。
- 一課裡若各拍要用不同的運動方式，可用一個 `self.mode` 屬性 + `_ang()` 之類的分派函數（見 l35）；manim 是在 `play()` 當下才求值 updater，所以在每個 `run()` 之前設好 `self.mode` 與 `self.t0` 就會生效，不必為每一拍複製整組 mobject。
- **三行公式的下緣實測在 y = 1.40**（兩行是 1.93）。任何在該拍出現的動畫元素與標籤都要壓在 y ≤ 1.30，包含箭頭尖端與它旁邊的文字（l39 第 5 拍的 Ω 標籤原本在 y = 1.35，正好被公式第三行蓋住）。
- **同一張圖裡的兩個標籤也會互撞**，不是只有「公式 vs 動畫」：l41 第 8 拍的座標軸標籤 `U_eff`（y = 1.50）和面板小標題（y = 1.45）疊在一起。新加軸標籤時要順手檢查同高度有沒有別的字。
- **不要讓後半段的畫面空掉**：l43 原本第 5 拍以後把所有圖都 fade out，左半邊連續五拍全黑。若後半段的內容偏代數，就另外設計一張圖（l43 補了一張 q–t 圖：同一個 q、不同抵達時刻的世界線，作用量沿線累積，再把 (43.6) 的兩個微分畫成一步 t 和一步 q）。
- **`self._tau()` 在每一拍開頭都會歸零**（`construct()` 每拍重設 `self.t0`）。單拍內的循環動畫用它剛好，但**跨拍要連續演化的動畫不能用**，否則每到下一拍就跳回起點。改用絕對時間減去自己記下的起始值（見 l46 的 `tflow0`，由第 7 拍的 callable 設定）。
- **`_arr()` 在長度小於 0.05 時回傳空的 `VGroup`，不會報錯**。兩個並排面板中間的連接箭頭最容易踩到：面板中心相距 3.5、座標軸半寬 1.5，扣掉之後只剩 0.5，箭頭幾乎看不見（l45、l47 都發生過）。畫之前先把「中心距離 − 兩邊半寬」算出來，並且**把箭頭放在面板下方**，因為中心高度上有 x 軸和它的標籤。
- **畫折射／光線類比時要核對彎曲方向**：進入 √(E − U) 較大（位能較低）的區域時路徑要**偏向法線**，所以第二個角要比第一個小；而且入射線要從交界的**另一側**畫過來（l44 兩個錯都犯過：先是角度反了，改完又把入射線畫到同一側）。
- **不要同時跑多個 `manim -qh`**：`media/texts/*.svg` 是共用快取，兩個 process 同時要同一個未快取的字串時會 `FileNotFoundError`。用序列佇列（見 `scratchpad/queue.sh` 的做法：一次一支、失敗重試一次），或至少錯開啟動時間。
- **用 `type()` 動態產生場景類別時一定要設 `__module__`**：manim 只收集 `__module__` 與它被指到的檔案相符的場景。`canonical_base.make()` 一開始沒設，於是 `LandauL42ZH` / `LandauL43EN` 這些類別在 manim 眼中不存在，**它會安靜地改渲染 base class**——`manim ... LandauL43EN` 產出的是 `ActionOfQBase.mp4`，而且因為 base 的 `LANGUAGE` 預設 `zh`，中英文兩次渲染寫進同一個檔案、內容都是中文版。現在 `make()` 會把 `cls.__module__` 帶過去。**渲染完務必核對 log 裡的 `Rendered <名字>` 與輸出檔名**，別只看有沒有 mp4。（在課程檔案內就地定義的 `_mk()` 沒有這個問題，因為 `type()` 會自動取得該模組名。）

---

## 已完成課程 YouTube 連結（私人）

| 課 | 主題 | 中文 | 英文 |
|---|---|---|---|
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

（第 4–19 課亦已完成並上傳；連結見各自的 `youtube_lNN_manifest.json` 與 Git 歷史。）
