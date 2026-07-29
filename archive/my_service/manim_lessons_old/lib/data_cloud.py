"""
Data Cloud
==========
1000 顆點代表整個資料集. 用於 Confusion Matrix / Regression / 任何
需要把「群體統計」具體化的場景.

提供:
  - DataCloud: N 顆點的網格, 可依 predicate 著色
  - animate_to_confusion_matrix: 把所有點重新分配到 2x2 格
"""
import numpy as np
import random
from manim import (
    VGroup, Dot, Rectangle, Text, ORIGIN, UP, DOWN, LEFT, RIGHT,
    AnimationGroup, FadeIn, Transform, MoveToTarget
)

from .design_tokens import (
    INK, DIM, GHOST, TRUE_CLR, FALSE_CLR, ACCENT_A, ACCENT_B,
    FS_SMALL, FS_BODY
)


class DataCloud(VGroup):
    """
    一團 N 顆 Dot 的資料雲. 預設排在矩形網格.

    每顆 dot 有 dot.case_id (int) 和 dot.label / dot.predicted (可選).
    """

    def __init__(self, n: int = 1000, layout: str = "grid",
                 grid_cols: int = 50, dot_radius: float = 0.045,
                 dot_color: str = DIM, area_size=(8.0, 4.0),
                 seed: int = 42, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.dot_color = dot_color
        self.dots = []
        random.seed(seed)
        np.random.seed(seed)

        if layout == "grid":
            self._layout_grid(n, grid_cols, dot_radius, dot_color, area_size)
        elif layout == "scatter":
            self._layout_scatter(n, dot_radius, dot_color, area_size)
        else:
            raise ValueError(f"未知 layout: {layout}")

    def _layout_grid(self, n, cols, radius, color, area):
        rows = (n + cols - 1) // cols
        w, h = area
        dx = w / cols
        dy = h / rows
        for i in range(n):
            r, c = divmod(i, cols)
            x = -w / 2 + dx / 2 + c * dx
            y = h / 2 - dy / 2 - r * dy
            d = Dot([x, y, 0], radius=radius, color=color)
            d.case_id = i
            d.label = None
            d.predicted = None
            self.dots.append(d)
            self.add(d)

    def _layout_scatter(self, n, radius, color, area):
        w, h = area
        for i in range(n):
            x = (np.random.rand() - 0.5) * w
            y = (np.random.rand() - 0.5) * h
            d = Dot([x, y, 0], radius=radius, color=color)
            d.case_id = i
            d.label = None
            d.predicted = None
            self.dots.append(d)
            self.add(d)

    # ── Labeling helpers ────────────────────────────────────────────
    def assign_labels(self, positive_ratio: float = 0.01):
        """
        隨機標記真實 label. positive_ratio 為正類比例.
        例如 positive_ratio=0.01 模擬「1% 的郵件是垃圾」.
        """
        n_pos = int(self.n * positive_ratio)
        positive_ids = set(random.sample(range(self.n), n_pos))
        for d in self.dots:
            d.label = (d.case_id in positive_ids)
        return self

    def predict(self, accuracy: float = 0.99,
                false_negative_rate: float = None):
        """
        模擬一個分類器預測.
        - accuracy: 整體準確率 (預設 0.99)
        - false_negative_rate: 漏掉正類的比例 (預設用 1-accuracy 當基準)
        """
        if false_negative_rate is None:
            false_negative_rate = 1 - accuracy

        for d in self.dots:
            if d.label is True:
                # 真實正類, 有機率被漏掉 (FN)
                d.predicted = (random.random() > false_negative_rate)
            else:
                # 真實負類, 有 (1-accuracy) 機率被誤判 (FP)
                d.predicted = (random.random() > accuracy)
        return self

    def confusion_category(self, dot) -> str:
        """回傳 'TP' / 'FP' / 'TN' / 'FN'."""
        if dot.label and dot.predicted: return "TP"
        if not dot.label and dot.predicted: return "FP"
        if not dot.label and not dot.predicted: return "TN"
        return "FN"

    def color_by_confusion(self,
                           tp_color=ACCENT_A,
                           tn_color=ACCENT_B,
                           fp_color=FALSE_CLR,
                           fn_color=FALSE_CLR):
        """依 confusion 分類給每顆點上色 (回傳 list of animations)."""
        anims = []
        cmap = {"TP": tp_color, "TN": tn_color, "FP": fp_color, "FN": fn_color}
        for d in self.dots:
            cat = self.confusion_category(d)
            anims.append(d.animate.set_color(cmap[cat]))
        return anims

    # ── Confusion matrix layout ────────────────────────────────────
    def make_confusion_matrix_targets(self,
                                      cell_size: float = 1.6,
                                      gap: float = 0.4,
                                      origin=ORIGIN) -> dict:
        """
        計算把每顆 dot 移動到 2x2 confusion matrix 的目標位置.
        回傳 dict 包含每個 cell 的中心座標 + Rectangles (給場景畫格子).
        """
        ox, oy, oz = np.array(origin, dtype=float)
        positions = {
            "TP": np.array([ox - cell_size / 2 - gap / 2,
                            oy + cell_size / 2 + gap / 2, 0]),
            "FP": np.array([ox + cell_size / 2 + gap / 2,
                            oy + cell_size / 2 + gap / 2, 0]),
            "FN": np.array([ox - cell_size / 2 - gap / 2,
                            oy - cell_size / 2 - gap / 2, 0]),
            "TN": np.array([ox + cell_size / 2 + gap / 2,
                            oy - cell_size / 2 - gap / 2, 0]),
        }

        # 把每類的點分散到 cell 內
        buckets = {"TP": [], "FP": [], "TN": [], "FN": []}
        for d in self.dots:
            buckets[self.confusion_category(d)].append(d)

        target_positions = {}
        for cat, cell_center in positions.items():
            cell_dots = buckets[cat]
            n_cell = len(cell_dots)
            if n_cell == 0:
                continue
            cols = max(1, int(np.ceil(np.sqrt(n_cell))))
            rows = (n_cell + cols - 1) // cols
            dx = cell_size / cols
            dy = cell_size / rows
            for i, dot in enumerate(cell_dots):
                r, c = divmod(i, cols)
                x = cell_center[0] - cell_size / 2 + dx / 2 + c * dx
                y = cell_center[1] + cell_size / 2 - dy / 2 - r * dy
                target_positions[dot.case_id] = np.array([x, y, 0])

        # Cell rectangles + labels (供 scene 顯示用)
        cells = {}
        for cat, center in positions.items():
            rect = Rectangle(width=cell_size, height=cell_size,
                             color=GHOST, stroke_width=1.5,
                             fill_opacity=0).move_to(center)
            label = Text(cat, font_size=FS_BODY, color=INK).move_to(
                center + np.array([0, cell_size / 2 + 0.25, 0]))
            cells[cat] = VGroup(rect, label)

        return {
            "positions": target_positions,
            "cells": cells,
            "cell_centers": positions,
            "buckets": buckets,
        }


# ─────────────────────────────────────────────────────────────────────
# Self-test scene
# ─────────────────────────────────────────────────────────────────────
try:
    from manim import Scene, FadeIn, AnimationGroup, LaggedStart

    class _DemoConfusionCloud(Scene):
        """1000 點 → confusion matrix. Run: manim -pql data_cloud.py _DemoConfusionCloud"""
        def construct(self):
            from .design_tokens import apply_global_config
            apply_global_config()

            cloud = DataCloud(n=500, grid_cols=40, area_size=(10, 5))
            cloud.assign_labels(positive_ratio=0.04)
            cloud.predict(accuracy=0.97, false_negative_rate=0.5)
            self.play(FadeIn(cloud, run_time=1.2))
            self.wait(0.5)

            # 上色
            self.play(*cloud.color_by_confusion(), run_time=1.5)
            self.wait(0.8)

            # 重排到 confusion matrix
            cm = cloud.make_confusion_matrix_targets(cell_size=2.0, gap=0.6)
            for cell in cm["cells"].values():
                self.play(FadeIn(cell, run_time=0.4))

            anims = []
            for d in cloud.dots:
                if d.case_id in cm["positions"]:
                    anims.append(d.animate.move_to(cm["positions"][d.case_id]))
            self.play(LaggedStart(*anims, lag_ratio=0.0005), run_time=2.5)
            self.wait(2)
except ImportError:
    pass
