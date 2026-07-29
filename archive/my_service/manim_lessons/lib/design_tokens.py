"""
Design Tokens
=============
所有 lesson 都從這裡 import 顏色和尺寸. 改一處全部變.
3B1B-inspired but slightly warmer for accessibility.
"""
try:
    from manim import config
except ImportError:
    config = None   # 容忍沒 manim 的環境 (給 lib/checks.py 用)

# ── Background & Ink ────────────────────────────────────────────────────────
BG          = "#0E0E0E"
INK         = "#F5F5F5"      # 主文字
DIM         = "#9A9A9A"      # 次要說明
GHOST       = "#3A3A3A"      # 背景參考線

# ── Concept Accents (4 主色 max — 全部影片共用) ─────────────────────────────
ACCENT_A    = "#F2B14F"      # 暖黃 — 主概念 A (e.g., 外心 / vertices / TP)
ACCENT_B    = "#5BC0BE"      # 青綠 — 主概念 B (e.g., 內心 / sides / TN)
ACCENT_C    = "#9B6FE0"      # 紫色 — 主概念 C (e.g., 第三類 / FN)
WARN        = "#E2585B"      # 紅色 — 構造線 / 重點 / 錯誤

# ── 子族色 (同概念的不同變體, 自動降彩度) ─────────────────────────────────
ACCENT_A_LIGHT = "#F8D196"
ACCENT_B_LIGHT = "#9CDDDB"

# ── Topic-specific aliases (語意比 ACCENT_A 更易讀) ────────────────────────
VERTEX_CLR  = ACCENT_A       # 頂點 (用於 Triangle Centers, Quadratic vertex)
SIDE_CLR    = ACCENT_B       # 邊 (用於 Triangle Centers, decision boundary)
ENERGY_KE   = ACCENT_A       # KE (動能)
ENERGY_PE   = ACCENT_B       # PE (位能)
TRUE_CLR    = ACCENT_B       # True positive/negative (正確分類)
FALSE_CLR   = WARN           # False positive/negative (錯誤分類)

# ── Font sizes (固定 6 階) ───────────────────────────────────────────────
FS_TITLE    = 44
FS_H1       = 36
FS_H2       = 28
FS_BODY     = 22
FS_CAPTION  = 18             # 字幕用
FS_SMALL    = 16

# ── Spacing ─────────────────────────────────────────────────────────────
PAD         = 0.4
PAD_S       = 0.2
PAD_L       = 0.8

# ── Stroke ──────────────────────────────────────────────────────────────
STROKE_THIN     = 1.5
STROKE_NORMAL   = 2.5
STROKE_BOLD     = 4.0
STROKE_DASH     = 2.0

# ── Run-time wait conventions (對齊旁白) ───────────────────────────────
BEAT_S      = 0.4    # 短停頓 (一個概念之間)
BEAT_M      = 1.0    # 中停頓 (一句完整訊息結尾)
BEAT_L      = 2.0    # 長停頓 (一個 scene 結尾)

# ── Apply to manim config ──────────────────────────────────────────────
def apply_global_config():
    """在 lesson 檔案最開頭呼叫一次."""
    if config is None:
        return   # manim 沒裝 (preflight 環境), 直接略過
    config.background_color = BG
    config.frame_height = 8.0


# ─────────────────────────────────────────────────────────────────────
# Self-test scene: manim -pql lib/design_tokens.py _DemoSwatches
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pass

try:
    from manim import Scene, Rectangle, Text, VGroup, RIGHT, DOWN, UP, LEFT, Write, FadeIn, LaggedStart
    
    class _DemoSwatches(Scene):
        """檢查所有色票. Run: manim -pql design_tokens.py _DemoSwatches"""
        def construct(self):
            apply_global_config()
            colors = [
                ("BG", BG), ("INK", INK), ("DIM", DIM), ("GHOST", GHOST),
                ("ACCENT_A", ACCENT_A), ("ACCENT_B", ACCENT_B),
                ("ACCENT_C", ACCENT_C), ("WARN", WARN),
            ]
            swatches = VGroup()
            for name, hex_code in colors:
                rect = Rectangle(width=2, height=1, color=hex_code, fill_opacity=1, stroke_width=0)
                label = Text(name, font_size=FS_SMALL, color=INK).next_to(rect, DOWN, buff=0.1)
                code = Text(hex_code, font_size=FS_SMALL - 2, color=DIM).next_to(label, DOWN, buff=0.05)
                swatches.add(VGroup(rect, label, code))
            swatches.arrange_in_grid(rows=2, cols=4, buff=0.5)
            self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in swatches], lag_ratio=0.1))
            self.wait(2)
except ImportError:
    pass
