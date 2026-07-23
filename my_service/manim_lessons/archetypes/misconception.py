"""
Misconception Archetype (F)
===========================
For topics where addressing a common wrong intuition is core to learning.
e.g. Overfitting (more complex != better), Limits (approaching != reaching),
Unit Circle (sin/cos are coordinates, not magic numbers).

Implements rules 3 + 4 of the 5-point recipe:
  R3: address misconception explicitly via show_misconception_panel()
  R4: end with analytical framework via show_analytical_framework()
"""
from manim import (
    Text, VGroup, Rectangle, Line, FadeIn, FadeOut, Write, Create,
    UP, DOWN, LEFT, RIGHT
)
from ._base import LessonArchetype
from ..lib.design_tokens import (
    INK, DIM, WARN, ACCENT_B, ACCENT_C,
    FS_H2, FS_BODY, FS_SMALL, BEAT_M, BEAT_L, STROKE_NORMAL
)


class MisconceptionArchetype(LessonArchetype):
    """處理「先打破錯誤直覺再給正確概念」題型."""
    ACCENT = ACCENT_C

    def show_misconception_panel(self, wrong_belief: str, correct_belief: str,
                                  why_wrong: str = "",
                                  pause_after_wrong: float = 2.0):
        """
        Left: red box 'Many think...'  Right: green box 'Actually...'
        Pause between for the wrong intuition to register first.
        """
        # 左: 錯誤
        wrong_box = Rectangle(width=5.4, height=2.8, color=WARN,
                              stroke_width=STROKE_NORMAL, fill_opacity=0.05,
                              fill_color=WARN)
        wrong_label = Text("Many think...", font_size=FS_SMALL, color=WARN)
        wrong_text = Text(wrong_belief, font_size=FS_BODY, color=INK,
                          line_spacing=0.8)
        wrong_group = VGroup(wrong_label, wrong_text).arrange(DOWN, buff=0.3)
        wrong_group.move_to(wrong_box.get_center())
        left = VGroup(wrong_box, wrong_group).shift(LEFT * 3.5)

        self.play(FadeIn(left), run_time=0.8)
        self.narrator.silent(pause_after_wrong)

        if why_wrong:
            why = Text(why_wrong, font_size=FS_SMALL, color=DIM)
            why.next_to(left, DOWN, buff=0.3)
            self.play(Write(why), run_time=0.8)
            self.narrator.silent(BEAT_M)

        # 右: 正確
        right_box = Rectangle(width=5.4, height=2.8, color=ACCENT_B,
                              stroke_width=STROKE_NORMAL, fill_opacity=0.05,
                              fill_color=ACCENT_B)
        right_label = Text("Actually...", font_size=FS_SMALL, color=ACCENT_B)
        right_text = Text(correct_belief, font_size=FS_BODY, color=INK,
                          line_spacing=0.8)
        right_group = VGroup(right_label, right_text).arrange(DOWN, buff=0.3)
        right_group.move_to(right_box.get_center())
        right = VGroup(right_box, right_group).shift(RIGHT * 3.5)

        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=1.0)
        self.narrator.silent(BEAT_L)
        return VGroup(left, right)

    def show_analytical_framework(self, title: str, steps: list,
                                   color: str = None):
        """
        Closing framework (NOT a fact recap). Numbered steps in a box.
        Implements R4 + R7 of the 5-point recipe.
        """
        if color is None:
            color = self.ACCENT
        framework_title = Text(title, font_size=FS_H2, color=color,
                                weight="BOLD")
        framework_title.to_edge(UP, buff=0.6)
        self.play(Write(framework_title), run_time=1.0)

        step_rows = VGroup()
        for i, step in enumerate(steps, start=1):
            num = Text(f"{i}.", font_size=FS_BODY, color=color, weight="BOLD")
            txt = Text(step, font_size=FS_BODY, color=INK)
            row = VGroup(num, txt).arrange(RIGHT, buff=0.3)
            step_rows.add(row)
        step_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        step_rows.next_to(framework_title, DOWN, buff=0.6)

        for row in step_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.7)
            self.narrator.silent(0.6)

        # Boxed conclusion (R7)
        box = Rectangle(width=step_rows.width + 1.0,
                        height=step_rows.height + 0.6,
                        color=color, stroke_width=STROKE_NORMAL)
        box.move_to(step_rows.get_center())
        self.play(Create(box), run_time=0.8)
        self.narrator.silent(BEAT_L)
        return VGroup(framework_title, step_rows, box)
