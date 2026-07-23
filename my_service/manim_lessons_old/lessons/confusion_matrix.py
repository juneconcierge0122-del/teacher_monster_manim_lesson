"""
Confusion Matrix — Lesson
=========================
Topic:   Why 99% Accuracy Can Still Be a Bad Model
Persona: 10th grade, 15 min focus, has percentages, lacks confusion matrix
KLPs:    confusion matrix; false positives vs false negatives;
         precision; recall; task-dependent error cost

Render:
    cd manim_lessons
    manim -pqh lessons/confusion_matrix.py FullLesson
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    Scene, Text, VGroup, Rectangle, Dot, FadeIn, FadeOut, Write,
    Create, LaggedStart, Transform, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT, ORIGIN
)

from manim_lessons.archetypes.stats import StatsArchetype
from manim_lessons.lib.design_tokens import (
    apply_global_config, INK, DIM, GHOST, ACCENT_A, ACCENT_B, WARN,
    TRUE_CLR, FALSE_CLR, FS_TITLE, FS_H1, FS_BODY, FS_SMALL,
    BEAT_M, BEAT_L
)
from manim_lessons.lib.narrator import Narrator
from manim_lessons.lib.data_cloud import DataCloud


# ── Scene 1: Bridge Hook (10th grade — Has 百分比, Lacks confusion matrix) ─
class S01_Hook(Scene):
    """30 秒. 用「99% 準確」這個直覺挑戰學生."""
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        # Persona 橋接: 從「百分比」這個 Has 概念出發
        bridge = VGroup(
            Text("99% 是什麼意思？", font_size=FS_TITLE, color=INK),
            Text("1000 封郵件裡面，990 封猜對。", font_size=FS_BODY, color=DIM),
        ).arrange(DOWN, buff=0.5)
        self.play(Write(bridge[0]), run_time=1.5)
        self.narrator.silent(BEAT_M)
        self.play(Write(bridge[1]), run_time=1.2)
        self.narrator.silent(BEAT_M)

        # Twist: 這個指標可能完全沒抓到問題
        twist = Text("但這個 99%，可能是個爛模型。",
                     font_size=FS_H1, color=WARN).to_edge(DOWN, buff=1.0)
        self.play(Write(twist), run_time=1.5)
        self.narrator.silent(BEAT_L)
        self.play(FadeOut(bridge), FadeOut(twist), run_time=0.6)


# ── Scene 2: 視覺化 1000 案例 + 99% 分類器 ─────────────────────────
class S02_VisualizeAccuracy(StatsArchetype):
    HEADING = ""
    CONCLUSION = ""
    ACCENT = ACCENT_A

    def teach(self):
        # 1000 顆點 = 1000 封郵件
        title = Text("1000 封郵件", font_size=FS_H1, color=INK).to_edge(UP)
        self.play(Write(title), run_time=0.8)

        cloud = self.show_data_cloud(
            n=1000, positive_ratio=0.01,   # 只有 1% 是癌症檢測陽性
            accuracy=0.99,                  # 模型整體準確率 99%
            false_negative_rate=0.5,        # 但漏掉一半的真陽性 (FN)
            area_size=(11, 4.5), grid_cols=50,
        )

        # 顯示「990 封猜對」的直覺
        accuracy_text = Text("整體準確率：99% (990/1000)", font_size=FS_BODY,
                             color=ACCENT_A).next_to(cloud, DOWN, buff=0.5)
        self.play(Write(accuracy_text))
        self.narrator.silent(BEAT_M)

        # 上色: TP=綠, TN=灰, FP/FN=紅
        self.color_by_classification(cloud, tp_color=TRUE_CLR, tn_color=DIM,
                                     fp_color=FALSE_CLR, fn_color=FALSE_CLR)

        # 把錯誤點標出來 (FN 是最致命的: 真有病但被判沒病)
        warning = Text("紅色 = 分類錯誤", font_size=FS_BODY, color=WARN).next_to(
            cloud, DOWN, buff=0.1)
        self.play(ReplacementTransform(accuracy_text, warning), run_time=0.6)
        self.narrator.silent(BEAT_M)

        # 把錯誤點集中到一個區域強調
        # 此處留給下一場景處理 — 把所有點拆到 confusion matrix
        self._cloud = cloud   # 讓 FullLesson 可以接著用


# ── Scene 3: Confusion Matrix 視覺化 ───────────────────────────────
class S03_ConfusionMatrix(StatsArchetype):
    HEADING = "Confusion Matrix"
    DEFINITION = "把預測結果分成四類: TP / FP / FN / TN"
    ACCENT = ACCENT_A
    CONCLUSION = "Precision 看右上, Recall 看左下"

    def teach(self):
        # 重建一個 cloud 並重排到 2x2
        cloud = DataCloud(n=300, layout="grid", grid_cols=30,
                          area_size=(8, 3))
        cloud.assign_labels(positive_ratio=0.10)
        cloud.predict(accuracy=0.85, false_negative_rate=0.5)
        cloud.color_by_confusion(tp_color=TRUE_CLR, tn_color=DIM,
                                  fp_color=FALSE_CLR, fn_color=FALSE_CLR)
        # 直接 set color (不要動畫)
        for d in cloud.dots:
            cat = cloud.confusion_category(d)
            color_map = {"TP": TRUE_CLR, "TN": DIM, "FP": FALSE_CLR, "FN": FALSE_CLR}
            d.set_color(color_map[cat])
        self.play(FadeIn(cloud), run_time=1.0)

        cm = self.animate_to_confusion_matrix(cloud, cell_size=1.6, gap=0.5)

        # 計算統計
        tp = sum(1 for d in cloud.dots if d.label and d.predicted)
        fp = sum(1 for d in cloud.dots if not d.label and d.predicted)
        tn = sum(1 for d in cloud.dots if not d.label and not d.predicted)
        fn = sum(1 for d in cloud.dots if d.label and not d.predicted)

        self.narrator.say(f"TP={tp}, FP={fp}, FN={fn}, TN={tn}", duration=2.0)

        panel = self.show_metric_panel(tp, fp, tn, fn)
        self.narrator.silent(BEAT_L)


# ── Scene 4: 兩個情境的成本不對稱 ────────────────────────────────
class S04_CostAsymmetry(Scene):
    """關鍵 KLP: task-dependent error cost.

    展示同一個 99% 準確的模型, 用在垃圾郵件 vs 癌症篩檢結果天差地遠.
    """
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("99% 準確 — 但代價不一樣", font_size=FS_H1, color=INK).to_edge(UP)
        self.play(Write(title))

        # 並排兩張卡
        # 左: 垃圾郵件 (FP 痛, FN 沒事)
        left_box = Rectangle(width=5.5, height=4.5, color=ACCENT_B,
                              stroke_width=2).shift(LEFT * 3.5 + DOWN * 0.3)
        left_title = Text("垃圾郵件過濾", font_size=FS_BODY, color=ACCENT_B,
                          weight="BOLD").move_to(left_box.get_top() + DOWN * 0.4)
        left_content = VGroup(
            Text("FP (誤判正常為垃圾)", font_size=FS_SMALL, color=WARN),
            Text("→ 重要信件被埋", font_size=FS_SMALL, color=DIM),
            Text("", font_size=FS_SMALL),
            Text("FN (漏掉垃圾)", font_size=FS_SMALL, color=DIM),
            Text("→ 多看一封廣告", font_size=FS_SMALL, color=DIM),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(left_box.get_center())

        # 右: 癌症篩檢 (FN 致命, FP 只是嚇一跳)
        right_box = Rectangle(width=5.5, height=4.5, color=ACCENT_A,
                              stroke_width=2).shift(RIGHT * 3.5 + DOWN * 0.3)
        right_title = Text("癌症篩檢", font_size=FS_BODY, color=ACCENT_A,
                           weight="BOLD").move_to(right_box.get_top() + DOWN * 0.4)
        right_content = VGroup(
            Text("FP (誤判健康為癌症)", font_size=FS_SMALL, color=DIM),
            Text("→ 多做一次檢查", font_size=FS_SMALL, color=DIM),
            Text("", font_size=FS_SMALL),
            Text("FN (漏掉真癌症)", font_size=FS_SMALL, color=WARN, weight="BOLD"),
            Text("→ 患者錯過治療", font_size=FS_SMALL, color=WARN),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(right_box.get_center())

        self.play(Create(left_box), Write(left_title))
        self.play(LaggedStart(*[FadeIn(t) for t in left_content], lag_ratio=0.3),
                  run_time=1.5)
        self.narrator.silent(BEAT_M)

        self.play(Create(right_box), Write(right_title))
        self.play(LaggedStart(*[FadeIn(t) for t in right_content], lag_ratio=0.3),
                  run_time=1.5)
        self.narrator.silent(BEAT_M)

        takeaway = Text("同一個指標 — 不同任務 — 完全不同的痛感",
                        font_size=FS_BODY, color=INK).to_edge(DOWN, buff=0.4)
        self.play(Write(takeaway))
        self.narrator.silent(BEAT_L)


# ── Scene 5: Recap ─────────────────────────────────────────────────
class S05_Recap(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("下次看到 99% 準確 — 你會問什麼？",
                     font_size=FS_H1, color=INK).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        questions = VGroup(
            Text("1. 它在哪一類錯了？(FP 還是 FN？)", font_size=FS_BODY, color=ACCENT_A),
            Text("2. 這個錯誤的代價有多高？", font_size=FS_BODY, color=ACCENT_B),
            Text("3. 我該看 Precision 還是 Recall？", font_size=FS_BODY, color=WARN),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(DOWN * 0.5)

        for q in questions:
            self.play(FadeIn(q, shift=RIGHT * 0.3), run_time=0.8)
            self.narrator.silent(BEAT_M)
        self.narrator.silent(BEAT_L)


# ── 完整課程 ───────────────────────────────────────────────────────
class FullLesson(Scene):
    def setup(self):
        apply_global_config()

    def construct(self):
        for SceneCls in [S01_Hook, S02_VisualizeAccuracy,
                          S03_ConfusionMatrix, S04_CostAsymmetry, S05_Recap]:
            scene_obj = SceneCls()
            scene_obj.renderer = self.renderer
            scene_obj.camera = self.camera
            scene_obj.setup()
            scene_obj.construct()
            self.wait(0.5)
            self.clear()
