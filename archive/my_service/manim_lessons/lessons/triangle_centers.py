"""
Triangle Centers — Lesson
=========================
Topic:   Multi-scenario Applications of Triangle Centers
Persona: 9th grade, 15 min focus, has basic geometry, lacks centers
KLPs:    Incenter, Circumcenter, Optimization, Modeling

Render:
    cd manim_lessons
    manim -pqh lessons/triangle_centers.py FullLesson
    manim -pql lessons/triangle_centers.py FullLesson      # 預覽用

子場景單獨測試:
    manim -pql lessons/triangle_centers.py S02_Circumcenter
"""
import sys
import pathlib
# 讓 manim 直接跑 .py 也能 import package
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    Scene, Polygon, Text, Dot, VGroup, DashedLine, Rectangle, Circle,
    Create, Write, FadeIn, FadeOut, GrowFromCenter, Transform,
    LaggedStart, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT, ORIGIN
)

from manim_lessons.archetypes.geometry import GeometryArchetype
from manim_lessons.lib.design_tokens import (
    apply_global_config, INK, DIM, GHOST, VERTEX_CLR, SIDE_CLR, WARN,
    FS_TITLE, FS_H1, FS_BODY, FS_SMALL,
    STROKE_NORMAL, STROKE_THIN, BEAT_M, BEAT_L
)
from manim_lessons.lib.construction import (
    perpendicular_bisector, angle_bisector,
    circumcenter_of, incenter_of, inradius, circumradius,
    circumcircle_construction, incircle_construction,
    foot_of_perpendicular,
)
from manim_lessons.lib.narrator import Narrator


# ── Scene 1: Hook ─────────────────────────────────────────────────────
class S01_Hook(Scene):
    """30 秒. 真實情境引入: 三家咖啡店要建共同倉庫."""
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("三家咖啡店要建一個共同倉庫", font_size=FS_TITLE, color=INK).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        shop_pos = [LEFT * 4 + DOWN * 1, RIGHT * 3.5 + DOWN * 1.8, RIGHT * 0.5 + UP * 2]
        shops = VGroup()
        for pos, lbl in zip(shop_pos, ["A 店", "B 店", "C 店"]):
            dot = Dot(pos, radius=0.18, color=VERTEX_CLR)
            label = Text(lbl, font_size=FS_BODY, color=INK).next_to(dot, DOWN, buff=0.15)
            shops.add(VGroup(dot, label))
        self.play(LaggedStart(*[FadeIn(s, scale=1.5) for s in shops], lag_ratio=0.2))
        self.narrator.say("倉庫位置該怎麼決定？", duration=1.5)

        question = Text("?", font_size=80, color=WARN)
        self.play(FadeIn(question, scale=0.5))
        self.narrator.say("老闆們有一個簡單的要求", duration=1.5)

        constraint = Text("到三家店的距離要相等", font_size=FS_H1, color=SIDE_CLR).to_edge(DOWN, buff=0.6)
        self.play(Write(constraint))
        self.narrator.silent(BEAT_L)
        self.narrator.clear()

        self.play(FadeOut(question), FadeOut(constraint), FadeOut(title),
                  *[FadeOut(s[1]) for s in shops])
        triangle = Polygon(*shop_pos, color=VERTEX_CLR, stroke_width=STROKE_NORMAL)
        self.play(Create(triangle), run_time=1.2)
        self.wait(1)


# ── Scene 2: Circumcenter ──────────────────────────────────────────
class S02_Circumcenter(GeometryArchetype):
    HEADING = "外心 (Circumcenter)"
    DEFINITION = "到三個頂點等距離的點"
    ACCENT = VERTEX_CLR
    CONCLUSION = "倉庫蓋在外心 → 到三家店等距"

    def teach(self):
        A = LEFT * 4 + DOWN * 1
        B = RIGHT * 3.5 + DOWN * 1.8
        C = RIGHT * 0.5 + UP * 2

        triangle, labels = self.draw_triangle(A, B, C, color=VERTEX_CLR,
                                              label_chars=("A", "B", "C"))

        # 構造步驟 1
        self.narrator.say("先找 AB 的中垂線", duration=1.5)
        ab = DashedLine(A, B, color=GHOST, stroke_width=2)
        self.play(Create(ab), run_time=0.5)
        bisector_AB = perpendicular_bisector(A, B)
        midpoint_AB = Dot((np.array(A) + np.array(B)) / 2, color=WARN, radius=0.08)
        self.play(FadeIn(midpoint_AB, scale=2), Create(bisector_AB), run_time=1.5)
        self.narrator.silent(0.4)

        # 構造步驟 2
        self.narrator.say("再作 BC 的中垂線", duration=1.5)
        bc = DashedLine(B, C, color=GHOST, stroke_width=2)
        bisector_BC = perpendicular_bisector(B, C)
        midpoint_BC = Dot((np.array(B) + np.array(C)) / 2, color=WARN, radius=0.08)
        self.play(Create(bc), FadeIn(midpoint_BC, scale=2), Create(bisector_BC),
                  run_time=1.5)

        # 揭曉外心
        self.narrator.say("交點就是外心", duration=1.2)
        cc = circumcircle_construction(A, B, C, accent_color=VERTEX_CLR)
        self.play(GrowFromCenter(cc['center']))

        circumcenter_label = Text("外心", font_size=FS_BODY, color=VERTEX_CLR).next_to(
            cc['center'], RIGHT, buff=0.15)
        self.play(Write(circumcenter_label))

        # 三條等距虛線 + 距離數值
        dist_label = Text(f"r = {cc['radius']:.2f}", font_size=FS_BODY, color=INK).to_corner(
            DOWN + RIGHT, buff=0.5)
        self.narrator.say("到三個頂點的距離都一樣", duration=2.0)
        self.play(Create(cc['radii']), Write(dist_label), run_time=1.5)

        # 揭曉外接圓
        self.narrator.say("這個距離當半徑畫圓 — 三個頂點都在圓上", duration=2.5)
        circle_label = Text("外接圓", font_size=FS_BODY, color=VERTEX_CLR).next_to(
            cc['circle'], DOWN, buff=0.3)
        self.play(Create(cc['circle']), Write(circle_label), run_time=2)
        self.narrator.silent(BEAT_L)


# ── Scene 3: Different problem ─────────────────────────────────────
class S03_DifferentProblem(GeometryArchetype):
    HEADING = ""
    BRIDGE_HOOK = ""
    CONCLUSION = "不同問題 → 不同的中心"
    ACCENT = INK

    def teach(self):
        title = Text("但是…", font_size=FS_TITLE, color=INK).to_edge(UP)
        self.play(Write(title))

        # 左卡: 剛剛的情境
        left_box = Rectangle(width=5.5, height=4.5, color=VERTEX_CLR,
                              stroke_width=2).shift(LEFT * 3.5 + DOWN * 0.3)
        left_title = Text("剛才：到頂點等距", font_size=FS_BODY, color=VERTEX_CLR).move_to(
            left_box.get_top() + DOWN * 0.4)
        small_tri_L = Polygon([-0.7, -0.7, 0], [0.7, -0.7, 0], [0, 0.7, 0],
                              color=VERTEX_CLR, stroke_width=2).move_to(left_box.get_center())
        verts_L = VGroup(*[Dot(v, color=VERTEX_CLR, radius=0.06)
                            for v in small_tri_L.get_vertices()])
        center_L = Dot(small_tri_L.get_center(), color=VERTEX_CLR)
        radii_L = VGroup(*[
            DashedLine(small_tri_L.get_center(), v, color=VERTEX_CLR, stroke_width=1.5)
            for v in small_tri_L.get_vertices()
        ])
        left_label = Text("頂點 ↔ 倉庫", font_size=FS_SMALL, color=VERTEX_CLR).next_to(
            left_box, DOWN, buff=0.1)

        self.play(Create(left_box), Write(left_title))
        self.play(Create(small_tri_L), FadeIn(verts_L), FadeIn(center_L),
                  Create(radii_L), Write(left_label))
        self.narrator.silent(BEAT_M)

        # 右卡: 新情境
        right_box = Rectangle(width=5.5, height=4.5, color=SIDE_CLR,
                              stroke_width=2).shift(RIGHT * 3.5 + DOWN * 0.3)
        right_title = Text("新問題：到邊等距", font_size=FS_BODY, color=SIDE_CLR).move_to(
            right_box.get_top() + DOWN * 0.4)
        small_tri_R = Polygon([-0.7, -0.7, 0], [0.7, -0.7, 0], [0, 0.7, 0],
                              color=SIDE_CLR, stroke_width=2).move_to(right_box.get_center())
        v = small_tri_R.get_vertices()
        I = incenter_of(v[0], v[1], v[2])
        center_R = Dot(I, color=SIDE_CLR)
        perps_R = VGroup()
        for i in range(3):
            p1, p2 = v[i], v[(i + 1) % 3]
            foot = foot_of_perpendicular(I, p1, p2)
            perps_R.add(DashedLine(I, foot, color=SIDE_CLR, stroke_width=1.5))
        right_label = Text("邊 ↔ 灑水器", font_size=FS_SMALL, color=SIDE_CLR).next_to(
            right_box, DOWN, buff=0.1)

        self.narrator.say("換個情境：要把灑水器放公園正中央", duration=2.5)
        self.play(Create(right_box), Write(right_title))
        self.play(Create(small_tri_R), FadeIn(center_R), Create(perps_R),
                  Write(right_label))
        self.narrator.silent(BEAT_L)


# ── Scene 4: Incenter ──────────────────────────────────────────────
class S04_Incenter(GeometryArchetype):
    HEADING = "內心 (Incenter)"
    DEFINITION = "到三條邊等距離的點"
    ACCENT = SIDE_CLR
    CONCLUSION = "灑水器放內心 → 到三邊等距，整個公園都灑到"

    def teach(self):
        A = LEFT * 4 + DOWN * 1.5
        B = RIGHT * 4 + DOWN * 1.5
        C = RIGHT * 0.3 + UP * 2

        triangle = Polygon(A, B, C, color=SIDE_CLR, stroke_width=STROKE_NORMAL)
        edge_labels = VGroup(
            Text("a", color=SIDE_CLR, font_size=FS_BODY).move_to(
                (np.array(B) + np.array(C)) / 2 + RIGHT * 0.3),
            Text("b", color=SIDE_CLR, font_size=FS_BODY).move_to(
                (np.array(A) + np.array(C)) / 2 + LEFT * 0.3),
            Text("c", color=SIDE_CLR, font_size=FS_BODY).move_to(
                (np.array(A) + np.array(B)) / 2 + DOWN * 0.3),
        )
        self.add(triangle, edge_labels)

        self.narrator.say("這次作的不是中垂線 — 是角平分線", duration=2.5)
        bisector_A = angle_bisector(A, B, C)
        bisector_B = angle_bisector(B, A, C)
        self.play(Create(bisector_A), run_time=1.2)
        self.play(Create(bisector_B), run_time=1.2)

        self.narrator.say("交點就是內心", duration=1.2)
        ic = incircle_construction(A, B, C, accent_color=SIDE_CLR)
        I_label = Text("內心", font_size=FS_BODY, color=SIDE_CLR).next_to(
            ic['center'], UP * 0.5 + RIGHT, buff=0.1)
        self.play(GrowFromCenter(ic['center']), Write(I_label))

        dist_label = Text(f"r = {ic['radius']:.2f}", font_size=FS_BODY, color=INK).to_corner(
            DOWN + RIGHT, buff=0.5)
        self.narrator.say("到三條邊的垂直距離完全一樣", duration=2.5)
        self.play(Create(ic['perpendiculars']), Write(dist_label), run_time=1.5)

        self.narrator.say("把這個距離當半徑畫圓 — 圓剛好碰到三條邊", duration=2.5)
        circle_label = Text("內切圓", font_size=FS_BODY, color=SIDE_CLR).move_to(
            ic['center_pos'] + UP * 0.7 + LEFT * 1.3)
        self.play(Create(ic['circle']), Write(circle_label), run_time=2)
        self.narrator.silent(BEAT_L)


# ── Scene 5: Decision Table ────────────────────────────────────────
class S05_DecisionTable(GeometryArchetype):
    HEADING = ""
    CONCLUSION = "等距，是對誰？"
    ACCENT = INK

    def teach(self):
        title = Text("什麼時候用哪個？", font_size=FS_H1, color=INK).to_edge(UP)
        self.play(Write(title))

        rows = [
            ("🗼 廣播塔覆蓋三個社區", "到頂點等距", "外心", VERTEX_CLR),
            ("💧 三角公園灑水器", "到邊等距", "內心", SIDE_CLR),
            ("🚒 消防站離主幹道最近", "到邊等距", "內心", SIDE_CLR),
        ]
        self.show_decision_table(rows)
        self.narrator.silent(BEAT_L)


# ── Scene 6: Recap ─────────────────────────────────────────────────
class S06_Recap(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("同一個三角形，兩個中心", font_size=FS_H1, color=INK).to_edge(UP)
        self.play(Write(title))

        # 左: 外心
        A1, B1, C1 = LEFT * 5 + DOWN * 1.5, LEFT * 1.2 + DOWN * 1.5, LEFT * 3 + UP * 1
        tri1 = Polygon(A1, B1, C1, color=VERTEX_CLR, stroke_width=STROKE_NORMAL)
        cc = circumcircle_construction(A1, B1, C1, accent_color=VERTEX_CLR)
        label1 = Text("外心\n(到頂點等距)", font_size=FS_SMALL, color=VERTEX_CLR,
                       line_spacing=0.7).next_to(cc['circle'], DOWN, buff=0.4)

        # 右: 內心
        A2, B2, C2 = RIGHT * 1.2 + DOWN * 1.5, RIGHT * 5 + DOWN * 1.5, RIGHT * 3 + UP * 1
        tri2 = Polygon(A2, B2, C2, color=SIDE_CLR, stroke_width=STROKE_NORMAL)
        ic = incircle_construction(A2, B2, C2, accent_color=SIDE_CLR)
        label2 = Text("內心\n(到邊等距)", font_size=FS_SMALL, color=SIDE_CLR,
                       line_spacing=0.7).next_to(ic['circle'], DOWN, buff=0.4)

        self.play(Create(tri1), Create(tri2), run_time=1.0)
        self.play(Create(cc['circle']), GrowFromCenter(cc['center']),
                  Create(ic['circle']), GrowFromCenter(ic['center']),
                  run_time=1.5)
        self.play(Write(label1), Write(label2))

        self.narrator.say("下次看到三角形 — 你會先問：『等距』是對誰？",
                          duration=3.0)


# ── 完整課程 ────────────────────────────────────────────────────────
class FullLesson(Scene):
    """串接所有 scene. 約 5~6 分鐘."""
    def setup(self):
        apply_global_config()

    def construct(self):
        for SceneCls in [S01_Hook, S02_Circumcenter, S03_DifferentProblem,
                          S04_Incenter, S05_DecisionTable, S06_Recap]:
            scene_obj = SceneCls()
            scene_obj.renderer = self.renderer
            scene_obj.camera = self.camera
            scene_obj.setup()
            scene_obj.construct()
            self.wait(0.5)
            self.clear()
