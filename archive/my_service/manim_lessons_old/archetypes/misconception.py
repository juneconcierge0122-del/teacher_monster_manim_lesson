from ._base import LessonArchetype
from ..lib.design_tokens import WARN, ACCENT_B, FS_H2, FS_BODY, INK
from manim import Text, VGroup, Rectangle, Cross, FadeIn, Write, Transform, DOWN, LEFT, RIGHT

class MisconceptionArchetype(LessonArchetype):
    """處理「先打破錯誤直覺再給正確概念」題型. e.g. Overfitting, Limits."""

    def show_misconception_then_fix(self, wrong_belief: str, correct_belief: str,
                                     example_wrong: str = "", example_right: str = ""):
        # 左: 錯誤直覺 (紅框 + ✗)
        wrong_box = Rectangle(width=5, height=2.5, color=WARN, stroke_width=2)
        wrong_label = Text("常見誤解", font_size=FS_BODY, color=WARN)
        wrong_text = Text(wrong_belief, font_size=FS_BODY, color=INK, line_spacing=0.8)
        wrong_group = VGroup(wrong_label, wrong_text).arrange(DOWN, buff=0.3)
        wrong_group.move_to(wrong_box.get_center())
        left = VGroup(wrong_box, wrong_group).shift(LEFT * 3.5)

        self.play(FadeIn(left), run_time=0.8)
        self.narrator.silent(2.0)   # 讓誤解先沉澱

        # 右: 正確概念 (綠框)
        right_box = Rectangle(width=5, height=2.5, color=ACCENT_B, stroke_width=2)
        right_label = Text("實際上", font_size=FS_BODY, color=ACCENT_B)
        right_text = Text(correct_belief, font_size=FS_BODY, color=INK, line_spacing=0.8)
        right_group = VGroup(right_label, right_text).arrange(DOWN, buff=0.3)
        right_group.move_to(right_box.get_center())
        right = VGroup(right_box, right_group).shift(RIGHT * 3.5)

        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=1.0)
        self.narrator.silent(2.5)
        return VGroup(left, right)
