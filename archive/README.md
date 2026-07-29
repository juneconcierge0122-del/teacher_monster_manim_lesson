# archive/

不再維護、但保留紀錄的東西。**不要從這裡 import，也不要拿它當範本。**

## my_service/

一個更早期的獨立專案（FastAPI 服務 + 用 LLM 自動產生 manim 課程的
`opus_lesson_writer.py`），與現在的雙語教學動畫系列沒有關係。

它自己夾帶了一份 `manim_lessons/` 的舊複本，還有 `manim_lessons_old/`
與 `manim_lessons.zip`。那些複本已經與工作區根目錄的 `manim_lessons/` 分岔，
**根目錄那份才是正在維護的版本**。

裡面的程式碼寫死了 `manim_lessons/lessons/` 這個舊的扁平路徑；
現在的課程檔已經依系列分到 `manim_lessons/lessons/<系列>/` 底下，所以就算重跑也對不上。
