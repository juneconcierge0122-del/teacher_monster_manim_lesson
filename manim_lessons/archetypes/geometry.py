"""
Geometry Archetype (A)
======================
給 Triangle Centers / Quadratic Vertices / 任何幾何題型.

提供:
  - 標準的「畫三角形 → 構造 → 顯示等距 → 畫圓」四步驟
  - 多情境決策表 (用於 Modeling KLP)
"""
import numpy as np
from manim import (
    Scene, Polygon, Text, Dot, VGroup, Create, GrowFromCenter, FadeIn,
    LaggedStart, Write, DashedLine, RIGHT, LEFT, UP, DOWN, ORIGIN
)

from ._base import LessonArchetype
from ..lib.design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, WARN,
    FS_BODY, FS_SMALL, FS_CAPTION, STROKE_NORMAL, STROKE_DASH, BEAT_M, BEAT_L
)


class GeometryArchetype(LessonArchetype):
    """
    Helper methods 給幾何 lesson.
    子類別 teach() 中可以呼叫:
      self.draw_triangle(A, B, C, color=...)
      self.show_construction(steps, narration_for_each)
      self.show_decision_table(rows)
    """
    ACCENT = ACCENT_A

    def draw_triangle(self, A, B, C, color=INK, label_chars=None):
        """畫三角形 + 標頂點. label_chars=('A','B','C') 之類."""
        tri = Polygon(A, B, C, color=color, stroke_width=STROKE_NORMAL)
        labels = VGroup()
        if label_chars:
            for vert, char, direction in zip(
                [A, B, C], label_chars,
                [LEFT + DOWN, RIGHT + DOWN, UP]
            ):
                lab = Text(char, color=color, font_size=FS_BODY).next_to(
                    np.array(vert) + np.zeros(3), direction, buff=0.15)
                labels.add(lab)
        self.play(Create(tri), Write(labels), run_time=1.2)
        return tri, labels

    def show_construction(self, mobjects: list, run_time_each: float = 1.2):
        """逐步顯示構造線 (中垂線 / 角平分線) — 會配字幕 narrator."""
        for m in mobjects:
            self.play(Create(m), run_time=run_time_each)

    def show_equidistant_lines(self, lines: VGroup, value_label: str):
        """顯示等距虛線 + 距離數值."""
        label = Text(value_label, font_size=FS_BODY, color=INK).to_corner(DOWN + RIGHT)
        self.play(Create(lines), Write(label), run_time=1.5)
        return label

    def show_decision_table(self, rows: list, header: tuple = None):
        """
        rows: list of (scenario_text, criterion_text, answer_text, color)
        最後一個 element 是答案的強調色.

        在 Modeling KLP 時很常用.
        """
        if header is None:
            header = ("情境", "等距條件", "答案")

        # 行
        row_groups = VGroup()
        for scenario, criterion, answer, color in rows:
            scen = Text(scenario, font_size=FS_BODY, color=INK)
            crit = Text(criterion, font_size=FS_BODY, color=DIM)
            ans = Text(answer, font_size=FS_BODY, color=color, weight="BOLD")
            row = VGroup(scen, crit, ans).arrange(RIGHT, buff=1.2)
            row_groups.add(row)
        row_groups.arrange(DOWN, buff=0.5)

        # 標題列
        head_group = VGroup(*[Text(h, font_size=FS_SMALL, color=DIM) for h in header])
        head_group.arrange(RIGHT, buff=1.2).next_to(row_groups, UP, buff=0.5)
        # 對齊每欄
        for j in range(3):
            head_group[j].move_to(
                [row_groups[0][j].get_center()[0],
                 head_group[j].get_center()[1], 0]
            )

        self.play(Write(head_group), run_time=0.8)
        for row in row_groups:
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in row],
                                   lag_ratio=0.3), run_time=0.8)
            self.narrator.silent(BEAT_M)

        return VGroup(head_group, row_groups)
