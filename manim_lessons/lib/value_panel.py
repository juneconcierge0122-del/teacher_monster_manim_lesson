"""
Value Panel
===========
即時量條和數字. 給 Energy Conservation / Physics lessons 用.

提供:
  - ValueBar: 一個垂直 / 水平的量條, 用 ValueTracker 驅動
  - LiveDecimal: 一個跟著 ValueTracker 變的數字顯示
  - EnergyPanel: KE + PE 並排, 自動顯示總和

用法:
    panel = EnergyPanel().to_edge(LEFT)
    self.add(panel)
    self.play(panel.set_KE(1.0), panel.set_PE(0.0), run_time=2)  # 動能轉位能
"""
import numpy as np
from manim import (
    VGroup, Rectangle, Text, Line, ValueTracker, DecimalNumber,
    always_redraw, ORIGIN, UP, DOWN, LEFT, RIGHT
)

from .design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ENERGY_KE, ENERGY_PE,
    FS_CAPTION, FS_BODY, FS_SMALL, STROKE_NORMAL
)


class ValueBar(VGroup):
    """
    一個量條, 高度 = max_height, 填滿比例 = tracker.get_value() / max_value.
    水平 (orientation='h') 或垂直 (orientation='v').
    """

    def __init__(self, label: str, max_value: float = 1.0,
                 max_height: float = 3.0, width: float = 0.6,
                 color: str = ACCENT_A, orientation: str = "v",
                 show_value: bool = True, value_format: str = "{:.2f}",
                 **kwargs):
        super().__init__(**kwargs)
        self.tracker = ValueTracker(0.0)
        self.max_value = max_value
        self.max_height = max_height
        self.width = width
        self.color = color
        self.orientation = orientation
        self.value_format = value_format

        # 框 (灰色背景)
        if orientation == "v":
            self.frame = Rectangle(width=width, height=max_height,
                                    color=GHOST, stroke_width=2)
        else:
            self.frame = Rectangle(width=max_height, height=width,
                                    color=GHOST, stroke_width=2)
        self.add(self.frame)

        # 填充條 (跟著 tracker 變)
        self.fill = always_redraw(self._make_fill)
        self.add(self.fill)

        # 標籤
        self.label = Text(label, font_size=FS_SMALL, color=INK)
        if orientation == "v":
            self.label.next_to(self.frame, DOWN, buff=0.15)
        else:
            self.label.next_to(self.frame, LEFT, buff=0.2)
        self.add(self.label)

        # 數值顯示
        if show_value:
            self.value_text = always_redraw(
                lambda: DecimalNumber(self.tracker.get_value(), num_decimal_places=2,
                                      font_size=FS_SMALL, color=INK)
                .next_to(self.frame, UP if orientation == "v" else RIGHT, buff=0.1)
            )
            self.add(self.value_text)

    def _make_fill(self) -> Rectangle:
        v = self.tracker.get_value()
        ratio = max(0.0, min(v / self.max_value, 1.0))
        if self.orientation == "v":
            h = self.max_height * ratio
            r = Rectangle(width=self.width, height=max(h, 0.001),
                          color=self.color, fill_color=self.color,
                          fill_opacity=0.85, stroke_width=0)
            r.next_to(self.frame.get_bottom(), UP, buff=0).align_to(self.frame, DOWN)
            return r
        else:
            w = self.max_height * ratio
            r = Rectangle(width=max(w, 0.001), height=self.width,
                          color=self.color, fill_color=self.color,
                          fill_opacity=0.85, stroke_width=0)
            r.next_to(self.frame.get_left(), RIGHT, buff=0).align_to(self.frame, LEFT)
            return r

    def set_value(self, v: float):
        """非動畫式設值 (用於 setup)."""
        self.tracker.set_value(v)
        return self

    def animate_to(self, v: float):
        """回傳 animation. 用 self.play(bar.animate_to(0.5))."""
        return self.tracker.animate.set_value(v)


class EnergyPanel(VGroup):
    """KE + PE 並排, 加上總和讀數. 給能量守恆題目用."""

    def __init__(self, max_value: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_value = max_value
        self.KE_bar = ValueBar("KE", max_value=max_value, color=ENERGY_KE)
        self.PE_bar = ValueBar("PE", max_value=max_value, color=ENERGY_PE)
        bars = VGroup(self.KE_bar, self.PE_bar).arrange(RIGHT, buff=1.0)
        self.add(bars)

        # 總和顯示 (應該守恆)
        self.total_text = always_redraw(
            lambda: VGroup(
                Text("總能", font_size=FS_SMALL, color=DIM),
                DecimalNumber(
                    self.KE_bar.tracker.get_value() + self.PE_bar.tracker.get_value(),
                    num_decimal_places=2, font_size=FS_BODY, color=INK
                )
            ).arrange(RIGHT, buff=0.2).next_to(bars, DOWN, buff=0.6)
        )
        self.add(self.total_text)

    def set_KE(self, v: float):
        return self.KE_bar.animate_to(v)

    def set_PE(self, v: float):
        return self.PE_bar.animate_to(v)


# ─────────────────────────────────────────────────────────────────────
# Self-test scene
# ─────────────────────────────────────────────────────────────────────
try:
    from manim import Scene, FadeIn

    class _DemoEnergyPanel(Scene):
        """擺鐘式能量轉換. Run: manim -pql value_panel.py _DemoEnergyPanel"""
        def construct(self):
            from .design_tokens import apply_global_config
            apply_global_config()

            panel = EnergyPanel(max_value=1.0)
            panel.KE_bar.set_value(0.0)
            panel.PE_bar.set_value(1.0)
            self.add(panel)
            self.wait(1)

            # 從最高點下落: PE -> KE
            self.play(panel.set_KE(1.0), panel.set_PE(0.0), run_time=2.0)
            self.wait(0.5)
            # 回升: KE -> PE
            self.play(panel.set_KE(0.0), panel.set_PE(1.0), run_time=2.0)
            self.wait(1)
except ImportError:
    pass
