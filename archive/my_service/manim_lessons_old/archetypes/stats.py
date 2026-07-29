"""
Stats Archetype (B)
===================
給 Confusion Matrix / Regression / 任何資料統計題型.

提供:
  - 1000 點資料雲 + 動態分類
  - 對比兩個情境 (e.g. spam vs cancer screening) 用同一個 dataset 看出指標差異
  - 散點 + 回歸線 (給 explanation/prediction 題)
"""
import numpy as np
from manim import (
    Scene, Text, VGroup, Rectangle, Dot, Line, Create, Write, FadeIn, FadeOut,
    LaggedStart, RIGHT, LEFT, UP, DOWN, ORIGIN, Axes, ParametricFunction
)

from ._base import LessonArchetype
from ..lib.data_cloud import DataCloud
from ..lib.design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ACCENT_C, WARN, TRUE_CLR, FALSE_CLR,
    FS_BODY, FS_SMALL, BEAT_M, BEAT_L
)


class StatsArchetype(LessonArchetype):
    """
    資料統計 lesson 的 base.
    子類別 teach() 可以用:
      self.show_data_cloud(n=..., positive_ratio=..., accuracy=...)
      self.animate_to_confusion_matrix(cloud)
      self.show_metric_panel(tp, fp, tn, fn)
      self.compare_scenarios(left_data, right_data)
    """
    ACCENT = ACCENT_A

    def show_data_cloud(self, n: int = 500, positive_ratio: float = 0.04,
                        accuracy: float = 0.97, false_negative_rate: float = 0.5,
                        area_size=(10, 4), grid_cols: int = 40):
        """產生並顯示一個資料雲. 回傳 cloud 物件."""
        cloud = DataCloud(n=n, layout="grid",
                          grid_cols=grid_cols, area_size=area_size)
        cloud.assign_labels(positive_ratio=positive_ratio)
        cloud.predict(accuracy=accuracy, false_negative_rate=false_negative_rate)
        self.play(FadeIn(cloud, run_time=1.2))
        self.narrator.silent(BEAT_M)
        return cloud

    def color_by_classification(self, cloud: DataCloud,
                                tp_color=TRUE_CLR, tn_color=DIM,
                                fp_color=FALSE_CLR, fn_color=FALSE_CLR,
                                run_time: float = 1.5):
        """依分類結果上色. 把錯誤 (FP/FN) 漆紅, 對的漆綠/灰."""
        anims = cloud.color_by_confusion(
            tp_color=tp_color, tn_color=tn_color,
            fp_color=fp_color, fn_color=fn_color
        )
        self.play(*anims, run_time=run_time)

    def animate_to_confusion_matrix(self, cloud: DataCloud,
                                     cell_size: float = 1.6,
                                     gap: float = 0.4,
                                     origin=None):
        """把 cloud 的點重排到 2x2 confusion matrix."""
        if origin is None:
            origin = ORIGIN
        cm = cloud.make_confusion_matrix_targets(cell_size=cell_size, gap=gap, origin=origin)

        for cell in cm["cells"].values():
            self.play(FadeIn(cell, run_time=0.3))

        anims = []
        for d in cloud.dots:
            if d.case_id in cm["positions"]:
                anims.append(d.animate.move_to(cm["positions"][d.case_id]))
        self.play(LaggedStart(*anims, lag_ratio=0.0008), run_time=2.5)
        self.narrator.silent(BEAT_M)
        return cm

    def show_metric_panel(self, tp: int, fp: int, tn: int, fn: int,
                          position=None):
        """顯示 accuracy / precision / recall 三個指標的動態值."""
        total = tp + fp + tn + fn
        if total == 0:
            return None
        acc = (tp + tn) / total
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0

        items = VGroup(
            VGroup(Text("Accuracy", font_size=FS_SMALL, color=DIM),
                   Text(f"{acc:.1%}", font_size=FS_BODY, color=INK)).arrange(RIGHT, buff=0.3),
            VGroup(Text("Precision", font_size=FS_SMALL, color=DIM),
                   Text(f"{prec:.1%}", font_size=FS_BODY, color=ACCENT_A)).arrange(RIGHT, buff=0.3),
            VGroup(Text("Recall", font_size=FS_SMALL, color=DIM),
                   Text(f"{rec:.1%}", font_size=FS_BODY, color=WARN)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        if position is None:
            items.to_corner(DOWN + LEFT, buff=0.5)
        else:
            items.move_to(position)

        self.play(LaggedStart(*[FadeIn(it, shift=UP * 0.2) for it in items],
                              lag_ratio=0.3), run_time=1.2)
        return items

    def show_regression_split(self, x_data, y_data,
                              left_emphasis: str = "explanation",
                              right_emphasis: str = "prediction"):
        """
        並排兩張散點圖: 左邊強調 explanation (係數), 右邊強調 prediction.
        x_data, y_data: list of float.
        """
        left_axes = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2],
                         x_length=4, y_length=3,
                         axis_config={"color": DIM, "stroke_width": 2})
        right_axes = left_axes.copy()
        left_axes.shift(LEFT * 3.5)
        right_axes.shift(RIGHT * 3.5)

        left_dots = VGroup(*[Dot(left_axes.c2p(x, y), radius=0.05, color=INK)
                              for x, y in zip(x_data, y_data)])
        right_dots = VGroup(*[Dot(right_axes.c2p(x, y), radius=0.05, color=INK)
                               for x, y in zip(x_data, y_data)])

        # 線性回歸 (簡單 numpy)
        a, b = np.polyfit(x_data, y_data, 1)
        line_left = left_axes.plot(lambda x: a * x + b, x_range=[0, 10], color=ACCENT_A)
        line_right = right_axes.plot(lambda x: a * x + b, x_range=[0, 10], color=ACCENT_B)

        left_label = Text(f"Explanation\n強調係數 a={a:.2f}",
                          font_size=FS_SMALL, color=ACCENT_A,
                          line_spacing=0.7).next_to(left_axes, DOWN, buff=0.3)
        right_label = Text(f"Prediction\n強調 ŷ 與殘差",
                           font_size=FS_SMALL, color=ACCENT_B,
                           line_spacing=0.7).next_to(right_axes, DOWN, buff=0.3)

        self.play(Create(left_axes), Create(right_axes), run_time=1.0)
        self.play(FadeIn(left_dots), FadeIn(right_dots), run_time=0.8)
        self.play(Create(line_left), Create(line_right), run_time=1.0)
        self.play(Write(left_label), Write(right_label), run_time=1.0)
        self.narrator.silent(BEAT_L)
        return VGroup(left_axes, right_axes, left_dots, right_dots,
                      line_left, line_right, left_label, right_label)
