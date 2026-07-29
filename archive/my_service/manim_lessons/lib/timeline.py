"""
Timeline
========
時間軸元件. 給 AI methods (rule-based → LLM) / Speciation /
任何要呈現「演進 / 分支」的 lesson 用.

提供:
  - HorizontalTimeline: 一條橫線, 上面有 N 個 era
  - VerticalDivergence: 從一個共同祖先分裂出多個分支 (給 speciation)
"""
import numpy as np
from manim import (
    VGroup, Line, Dot, Text, Arrow, MathTex, Polygon,
    DashedLine, FadeIn, Create, GrowFromCenter, Write,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI
)

from .design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ACCENT_C, WARN,
    FS_SMALL, FS_BODY, FS_CAPTION, STROKE_NORMAL, STROKE_THIN
)


class HorizontalTimeline(VGroup):
    """
    一條水平時間軸 + N 個事件節點.
    eras: list of dict, each: {'year': int|str, 'label': str, 'color': str}
    """

    def __init__(self, eras: list, length: float = 10.0,
                 axis_color: str = DIM, **kwargs):
        super().__init__(**kwargs)
        self.eras = eras
        self.length = length
        self.axis_color = axis_color

        # 軸線
        self.axis = Line(LEFT * length / 2, RIGHT * length / 2,
                         color=axis_color, stroke_width=STROKE_NORMAL)
        self.add(self.axis)

        # 等距分配節點
        self.nodes = []
        n = len(eras)
        if n == 0:
            return
        if n == 1:
            x_positions = [0.0]
        else:
            x_positions = np.linspace(-length / 2 + 0.4,
                                      length / 2 - 0.4, n)

        for x, era in zip(x_positions, eras):
            color = era.get('color', ACCENT_A)
            dot = Dot([x, 0, 0], color=color, radius=0.10)
            year_label = Text(str(era['year']), font_size=FS_SMALL, color=DIM)
            year_label.next_to(dot, DOWN, buff=0.2)
            name_label = Text(era['label'], font_size=FS_BODY, color=INK)
            name_label.next_to(dot, UP, buff=0.3)
            node = VGroup(dot, year_label, name_label)
            node.dot = dot
            node.year_label = year_label
            node.name_label = name_label
            node.x = x
            self.nodes.append(node)
            self.add(node)

    def reveal_node(self, scene, idx: int, run_time: float = 0.8):
        """逐一顯示節點. 通常配合 narrator.say() 用."""
        node = self.nodes[idx]
        scene.play(GrowFromCenter(node.dot),
                   FadeIn(node.year_label),
                   Write(node.name_label),
                   run_time=run_time)

    def get_node_position(self, idx: int) -> np.ndarray:
        """取得節點座標 (用於連線到 sub-scene)."""
        return self.nodes[idx].dot.get_center()


class VerticalDivergence(VGroup):
    """
    從一個共同祖先分裂出多個分支. 給 Speciation 用.
    branches: list of dict {'label': str, 'color': str, 'angle_deg': float}
    """

    def __init__(self, ancestor_label: str, branches: list,
                 trunk_height: float = 2.0, branch_length: float = 2.5,
                 trunk_color: str = DIM, **kwargs):
        super().__init__(**kwargs)

        # 祖先在底部
        anchor_bottom = DOWN * trunk_height / 2
        anchor_top = UP * trunk_height / 2

        ancestor_dot = Dot(anchor_bottom, color=trunk_color, radius=0.12)
        ancestor_text = Text(ancestor_label, font_size=FS_BODY, color=INK)
        ancestor_text.next_to(ancestor_dot, DOWN, buff=0.2)
        self.ancestor = VGroup(ancestor_dot, ancestor_text)

        # 主幹
        self.trunk = Line(anchor_bottom, anchor_top,
                          color=trunk_color, stroke_width=STROKE_NORMAL)

        # 分支點 (從主幹頂端發散)
        self.branches = []
        for br in branches:
            angle_rad = br['angle_deg'] * PI / 180
            end = anchor_top + RIGHT * branch_length * np.cos(angle_rad) + \
                                 UP * branch_length * np.sin(angle_rad)
            color = br.get('color', ACCENT_A)
            branch_line = Line(anchor_top, end,
                               color=color, stroke_width=STROKE_NORMAL)
            branch_dot = Dot(end, color=color, radius=0.10)
            branch_label = Text(br['label'], font_size=FS_BODY, color=color)
            branch_label.next_to(branch_dot, UP if angle_rad > 0 else DOWN, buff=0.2)
            branch_group = VGroup(branch_line, branch_dot, branch_label)
            branch_group.line = branch_line
            branch_group.dot = branch_dot
            branch_group.label = branch_label
            self.branches.append(branch_group)

        # 不直接 add 全部, 讓 scene 控制顯示順序
        self.add(self.ancestor, self.trunk)

    def grow_branches(self, scene, run_time: float = 1.5):
        """同時長出所有分支."""
        anims = []
        for br in self.branches:
            scene.add(br)
            anims += [Create(br.line), GrowFromCenter(br.dot), Write(br.label)]
        scene.play(*anims, run_time=run_time)


# ─────────────────────────────────────────────────────────────────────
# Self-test scene
# ─────────────────────────────────────────────────────────────────────
try:
    from manim import Scene, FadeIn

    class _DemoTimeline(Scene):
        """AI methods 時間軸. Run: manim -pql timeline.py _DemoTimeline"""
        def construct(self):
            from .design_tokens import apply_global_config
            apply_global_config()

            eras = [
                {'year': '1950s', 'label': 'Rule-based', 'color': ACCENT_A},
                {'year': '1980s', 'label': 'Expert\nSystems', 'color': ACCENT_A},
                {'year': '2000s', 'label': 'ML', 'color': ACCENT_B},
                {'year': '2010s', 'label': 'Deep\nLearning', 'color': ACCENT_B},
                {'year': '2020s', 'label': 'LLM', 'color': ACCENT_C},
            ]
            tl = HorizontalTimeline(eras)
            self.play(Create(tl.axis), run_time=0.8)
            for i in range(len(eras)):
                tl.reveal_node(self, i, run_time=0.6)
            self.wait(2)

    class _DemoDivergence(Scene):
        """族群分化. Run: manim -pql timeline.py _DemoDivergence"""
        def construct(self):
            from .design_tokens import apply_global_config
            apply_global_config()
            div = VerticalDivergence(
                "共同祖先",
                branches=[
                    {'label': '物種 A', 'color': ACCENT_A, 'angle_deg': 130},
                    {'label': '物種 B', 'color': ACCENT_B, 'angle_deg': 50},
                ],
            )
            self.play(FadeIn(div.ancestor), Create(div.trunk))
            self.wait(0.5)
            div.grow_branches(self)
            self.wait(2)
except ImportError:
    pass
