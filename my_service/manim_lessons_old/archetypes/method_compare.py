"""
Method Comparison Archetype (E)
================================
給 AI Methods (rule-based → LLM) / 任何要對比多種方法的 lesson.

提供:
  - 演進時間軸 (從 lib.timeline)
  - 每種方法的迷你示範框 (mini-demo card)
  - 方法比較表
"""
import numpy as np
from manim import (
    Text, VGroup, Rectangle, Line, Dot, Polygon, MathTex,
    Create, Write, FadeIn, FadeOut, GrowFromCenter, LaggedStart,
    UP, DOWN, LEFT, RIGHT, ORIGIN
)

from ._base import LessonArchetype
from ..lib.timeline import HorizontalTimeline
from ..lib.design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ACCENT_C, WARN,
    FS_BODY, FS_SMALL, FS_CAPTION, BEAT_M, BEAT_L
)


class MethodCompareArchetype(LessonArchetype):
    """
    Helper methods 給 method comparison lesson.

    子類別可呼叫:
      self.show_evolution_timeline(eras)
      self.mini_demo_card(title, demo_func, position)
      self.method_comparison_table(rows)
    """
    ACCENT = ACCENT_C

    def show_evolution_timeline(self, eras: list, length: float = 11.0):
        """
        eras: list of {'year': str, 'label': str, 'color': str}
        逐一 reveal.
        """
        tl = HorizontalTimeline(eras, length=length)
        self.play(Create(tl.axis), run_time=0.8)
        for i in range(len(eras)):
            tl.reveal_node(self, i, run_time=0.7)
            self.narrator.silent(0.3)
        return tl

    def mini_demo_card(self, title: str, position=ORIGIN,
                       width: float = 3.0, height: float = 2.5,
                       color: str = ACCENT_A):
        """
        產生一張迷你示範卡: 標題 + 框. 內容由 caller 自己填入框內.
        回傳 (card_VGroup, content_anchor_position).
        """
        rect = Rectangle(width=width, height=height, color=color,
                         stroke_width=2, fill_opacity=0.05,
                         fill_color=color)
        title_text = Text(title, font_size=FS_BODY, color=color)
        title_text.move_to(rect.get_top() + DOWN * 0.3)
        card = VGroup(rect, title_text).move_to(position)
        return card, rect.get_center() + DOWN * 0.2

    def method_comparison_table(self, columns: list, rows: list):
        """
        columns: list of method 名稱 (str)
        rows: list of (criterion_name, [value_for_each_method])

        例如:
          columns = ['Rule-based', 'ML', 'LLM']
          rows = [
            ('資料需求', ['少', '多', '極多']),
            ('可解釋性', ['高', '中', '低']),
          ]
        """
        # 建表 (以 Text + 對齊)
        n_cols = len(columns)
        col_width = 2.5
        row_height = 0.7

        # 標題列
        header_cells = VGroup(
            Text("", font_size=FS_BODY),  # 左上空格
            *[Text(c, font_size=FS_BODY, color=ACCENT_A) for c in columns]
        )
        for i, cell in enumerate(header_cells):
            cell.move_to([(i - n_cols / 2) * col_width, 2, 0])

        # 資料列
        all_rows = VGroup(header_cells)
        for r_idx, (criterion, values) in enumerate(rows):
            y = 2 - (r_idx + 1) * row_height
            row = VGroup(
                Text(criterion, font_size=FS_SMALL, color=DIM),
                *[Text(v, font_size=FS_BODY, color=INK) for v in values]
            )
            for i, cell in enumerate(row):
                cell.move_to([(i - n_cols / 2) * col_width, y, 0])
            all_rows.add(row)

        # 動畫: header 先, 然後逐 row
        self.play(LaggedStart(*[Write(c) for c in header_cells], lag_ratio=0.1),
                  run_time=1.2)
        for row in all_rows[1:]:
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in row],
                                   lag_ratio=0.2), run_time=0.8)
            self.narrator.silent(0.4)

        return all_rows
