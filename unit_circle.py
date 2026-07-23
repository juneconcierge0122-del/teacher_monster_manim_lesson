"""
Unit Circle — Lesson
====================
Topic:   Unit Circle (sin/cos as coordinates, radians, connection to graphs)
Persona: 12th grade, 15 min focus
         Has:   basic trigonometry
         Lacks: conceptual understanding of the unit circle
KLPs:    sine/cosine as coordinates, radians, connection to graphs
Misconception to address: sin/cos are memorized values rather than coordinates

5-point recipe coverage:
  R1 deeper layer:  three linked representations — angle ↔ point ↔ wave
  R2 multi-context: rotation + sine wave + cosine wave moving together
  R3 misconception: "sin 30° is a number to memorize" → it's a y-coordinate
  R4 framework:     two-direction framework at end (boxed)
  R5 signaling:     point on circle highlights as angle slider moves
  R6 colors:        BLUE for cosine (x), YELLOW for sine (y), throughout
  R7 boxed results: framework boxed

Render:
    manim -qm lessons/unit_circle.py FullLesson
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    Scene, Text, MathTex, VGroup, Rectangle, Circle, Dot, Line, DashedLine,
    Arc, Axes, ValueTracker, always_redraw, DecimalNumber
    FadeIn, FadeOut, Write, Create, GrowFromCenter,
    LaggedStart, ReplacementTransform, Transform,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI
)

from manim_lessons.archetypes import LessonArchetype, MisconceptionArchetype
from manim_lessons.lib.design_tokens import (
    apply_global_config, INK, DIM, GHOST,
    ACCENT_A, ACCENT_B, WARN,
    FS_TITLE, FS_H1, FS_H2, FS_BODY, FS_SMALL,
    BEAT_M, BEAT_L, STROKE_NORMAL
)
from manim_lessons.lib.narrator import Narrator
from manim_lessons.lib.persona import Persona


# ── Semantic colors (R6) ────────────────────────────────────────────
COS_CLR = ACCENT_B   # blue: x-coordinate, cosine
SIN_CLR = ACCENT_A   # yellow: y-coordinate, sine
ANGLE_CLR = WARN     # red: angle / arc

PERSONA_DEF = Persona(
    grade=12, focus_minutes=15,
    has=["basic trigonometry", "sine", "cosine"],
    lacks=["unit circle", "sine as coordinate", "cosine as coordinate", "radians"],
)


# ── S01: Hook — the memorization trap ──────────────────────────────
class S01_Hook(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        # Show the memorization table
        title = Text("Quick — what's sin 30°?",
                     font_size=FS_TITLE, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.narrator.silent(1.5)

        # Common memorized values
        values = VGroup(
            MathTex(r"\sin 30^\circ = \tfrac{1}{2}", font_size=44, color=INK),
            MathTex(r"\sin 45^\circ = \tfrac{\sqrt{2}}{2}", font_size=44, color=INK),
            MathTex(r"\sin 60^\circ = \tfrac{\sqrt{3}}{2}", font_size=44, color=INK),
        ).arrange(DOWN, buff=0.6).shift(DOWN * 0.3)

        for v in values:
            self.play(Write(v), run_time=0.8)
            self.narrator.silent(0.5)
        self.narrator.silent(BEAT_M)

        # The question
        question = Text("...but why THESE numbers?",
                        font_size=FS_H2, color=WARN).to_edge(DOWN, buff=0.5)
        self.play(Write(question), run_time=1.0)
        self.narrator.silent(BEAT_L)
        self.narrator.silent(BEAT_M)


# ── S02: Define the unit circle ─────────────────────────────────────
class S02_DefineUnitCircle(LessonArchetype):
    HEADING = "The Unit Circle"
    ACCENT = INK
    PERSONA = PERSONA_DEF

    def teach(self):
        self.teach_concept(
            term="Unit circle",
            definition="A circle centered at the origin with radius 1",
            example="Every point (x, y) on it satisfies x² + y² = 1",
            extra_dwell=1.5,
        )

        # Draw it
        self.fade_heading()
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                  x_length=5, y_length=5,
                  axis_config={"color": DIM, "include_tip": True,
                               "include_numbers": False}).shift(LEFT * 2)
        circ = Circle(radius=1.25, color=INK,
                      stroke_width=STROKE_NORMAL).move_to(ax.c2p(0, 0))
        radius_label = MathTex("r = 1", color=INK, font_size=32)
        radius_label.next_to(ax, RIGHT, buff=0.5).shift(UP * 0.5)
        eq = MathTex("x^2 + y^2 = 1", color=INK, font_size=36)
        eq.next_to(radius_label, DOWN, buff=0.5)

        self.play(Create(ax), run_time=1.0)
        self.play(Create(circ), Write(radius_label), run_time=1.5)
        self.narrator.silent(BEAT_M)
        self.play(Write(eq), run_time=1.0)
        self.narrator.silent(BEAT_L)


# ── S03: sin/cos AS coordinates (the main reveal) ──────────────────
class S03_SinCosAsCoords(LessonArchetype):
    HEADING = ""
    ACCENT = SIN_CLR
    PERSONA = PERSONA_DEF

    def teach(self):
        # Setup the unit circle
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                  x_length=5, y_length=5,
                  axis_config={"color": DIM, "include_tip": True,
                               "include_numbers": False}).shift(LEFT * 2.5)
        circ = Circle(radius=1.25, color=DIM,
                      stroke_width=STROKE_NORMAL).move_to(ax.c2p(0, 0))
        self.add(ax, circ)

        # Animate angle slider
        theta = ValueTracker(0.5)  # start at ~30 degrees

        def point_on_circle():
            t = theta.get_value()
            return ax.c2p(np.cos(t), np.sin(t))

        # Moving objects
        radius_line = always_redraw(lambda: Line(
            ax.c2p(0, 0), point_on_circle(),
            color=ANGLE_CLR, stroke_width=3))
        p_dot = always_redraw(lambda: Dot(point_on_circle(),
                                           color=INK, radius=0.10))
        # Angle arc
        arc = always_redraw(lambda: Arc(
            radius=0.4, start_angle=0, angle=theta.get_value(),
            color=ANGLE_CLR, stroke_width=3,
            arc_center=ax.c2p(0, 0)))
        theta_label = always_redraw(lambda: MathTex(
            r"\theta", color=ANGLE_CLR, font_size=32).move_to(
                ax.c2p(0.55 * np.cos(theta.get_value() / 2),
                       0.55 * np.sin(theta.get_value() / 2))))

        self.play(Create(radius_line), GrowFromCenter(p_dot), run_time=1.0)
        self.play(Create(arc), Write(theta_label), run_time=0.8)
        self.narrator.silent(BEAT_M)

        # Now reveal: this point has coordinates (cos θ, sin θ)
        x_drop = always_redraw(lambda: DashedLine(
            point_on_circle(),
            ax.c2p(np.cos(theta.get_value()), 0),
            color=COS_CLR, stroke_width=2.5))
        y_drop = always_redraw(lambda: DashedLine(
            point_on_circle(),
            ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, stroke_width=2.5))
        x_tick = always_redraw(lambda: Dot(
            ax.c2p(np.cos(theta.get_value()), 0),
            color=COS_CLR, radius=0.08))
        y_tick = always_redraw(lambda: Dot(
            ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, radius=0.08))

        self.play(Create(x_drop), GrowFromCenter(x_tick), run_time=1.0)
        self.play(Create(y_drop), GrowFromCenter(y_tick), run_time=1.0)
        self.narrator.silent(BEAT_M)

        # The coordinate readout (R5: live signaling)
        #x_readout = always_redraw(lambda: MathTex(
        #    f"x = \\cos\\theta = {np.cos(theta.get_value()):.2f}",
        #    color=COS_CLR, font_size=30).move_to(RIGHT * 3.5 + UP * 1.2))
        #y_readout = always_redraw(lambda: MathTex(
        #    f"y = \\sin\\theta = {np.sin(theta.get_value()):.2f}",
        #    color=SIN_CLR, font_size=30).move_to(RIGHT * 3.5 + UP * 0.3))


        x_label = MathTex(r"x = \cos\theta = ", color=COS_CLR, font_size=30)
        x_num = DecimalNumber(
            np.cos(theta.get_value()),
            num_decimal_places=2,
            include_sign=True,                 # 保證字寬恆定,負號永遠在
            color=COS_CLR, font_size=30,
        )
        x_num.add_updater(lambda m: m.set_value(np.cos(theta.get_value())))
        x_readout = VGroup(x_label, x_num).arrange(RIGHT, buff=0.1).move_to(RIGHT * 3.5 + UP * 1.2)

        y_label = MathTex(r"y = \sin\theta = ", color=SIN_CLR, font_size=30)
        y_num = DecimalNumber(
            np.sin(theta.get_value()),
            num_decimal_places=2,
            include_sign=True,
            color=SIN_CLR, font_size=30,
        )
        y_num.add_updater(lambda m: m.set_value(np.sin(theta.get_value())))
        y_readout = VGroup(y_label, y_num).arrange(RIGHT, buff=0.1).move_to(RIGHT * 3.5 + UP * 0.3)


        self.play(Write(x_readout), Write(y_readout), run_time=1.2)
        self.narrator.silent(BEAT_L)

        # Now: teach_concept for each (covers 2 lacks)
        # Sweep angle while narrating
        self.play(theta.animate.set_value(PI / 6), run_time=1.5)
        annotation_30 = MathTex(r"\theta = 30^\circ",
                                color=ANGLE_CLR, font_size=28).move_to(RIGHT * 3.5 + DOWN * 0.8)
        self.play(Write(annotation_30), run_time=0.8)
        self.narrator.silent(BEAT_L)

        # Sweep further
        self.play(theta.animate.set_value(PI / 4), run_time=1.2)
        self.narrator.silent(BEAT_M)
        self.play(theta.animate.set_value(PI / 3), run_time=1.2)
        self.narrator.silent(BEAT_M)


# ── S04: Misconception — they're coordinates, not magic numbers ────
class S04_Misconception(MisconceptionArchetype):
    HEADING = ""
    PERSONA = PERSONA_DEF

    def teach(self):
        title = Text("Back to that question...",
                     font_size=FS_H1, color=INK).to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.narrator.silent(1.0)

        # Recall the original puzzle
        recall = MathTex(r"\sin 30^\circ = \tfrac{1}{2}",
                         font_size=44, color=INK).shift(UP * 1.2)
        self.play(Write(recall), run_time=0.8)
        self.narrator.silent(BEAT_M)

        self.play(FadeOut(title), recall.animate.to_edge(UP, buff=0.5),
                  run_time=0.5)

        # Misconception panel
        self.show_misconception_panel(
            wrong_belief='"½" is a magic number you memorize.',
            correct_belief='"½" is just the y-coordinate of the point\non the unit circle at angle 30°.',
            why_wrong="(There's nothing special — it's just a height.)",
        )


# ── S05: Connect to the wave graph ─────────────────────────────────
class S05_ConnectGraph(LessonArchetype):
    HEADING = "Where does the wave come from?"
    ACCENT = SIN_CLR
    PERSONA = PERSONA_DEF

    def teach(self):
        self.fade_heading()
        # Left side: small unit circle
        circ_ax = Axes(x_range=[-1.2, 1.2, 1], y_range=[-1.2, 1.2, 1],
                       x_length=3, y_length=3,
                       axis_config={"color": DIM, "include_tip": False,
                                    "include_numbers": False}).shift(LEFT * 5)
        circ = Circle(radius=0.75, color=DIM,
                      stroke_width=2).move_to(circ_ax.c2p(0, 0))
        self.add(circ_ax, circ)

        # Right side: the sine wave axes
        wave_ax = Axes(x_range=[0, 2 * PI, PI / 2],
                       y_range=[-1.2, 1.2, 1],
                       x_length=8, y_length=3,
                       axis_config={"color": DIM, "include_tip": False,
                                    "include_numbers": False}).shift(RIGHT * 1.5)
        wave_x_label = Text("angle θ", font_size=FS_SMALL, color=DIM)
        wave_x_label.next_to(wave_ax, DOWN, buff=0.15)
        wave_y_label = Text("y", font_size=FS_SMALL, color=SIN_CLR)
        wave_y_label.next_to(wave_ax, LEFT, buff=0.15)
        self.play(Create(wave_ax), Write(wave_x_label), Write(wave_y_label),
                  run_time=1.0)
        self.narrator.silent(BEAT_M)

        # Sweep angle and trace the wave
        theta = ValueTracker(0.0)

        def circ_pt():
            t = theta.get_value()
            return circ_ax.c2p(np.cos(t), np.sin(t))

        radius_line = always_redraw(lambda: Line(
            circ_ax.c2p(0, 0), circ_pt(),
            color=ANGLE_CLR, stroke_width=2.5))
        p_dot = always_redraw(lambda: Dot(circ_pt(),
                                           color=INK, radius=0.08))
        y_drop = always_redraw(lambda: DashedLine(
            circ_pt(),
            circ_ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, stroke_width=2))
        y_marker = always_redraw(lambda: Dot(
            circ_ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, radius=0.07))

        # Wave dot tracks (angle, sin(angle))
        wave_dot = always_redraw(lambda: Dot(
            wave_ax.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=SIN_CLR, radius=0.09))
        # Horizontal connector
        connector = always_redraw(lambda: DashedLine(
            circ_ax.c2p(0, np.sin(theta.get_value())),
            wave_ax.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=SIN_CLR, stroke_width=1.5))

        self.add(radius_line, p_dot, y_drop, y_marker, wave_dot, connector)

        # Pre-build the full wave path that gets drawn as theta sweeps
        wave_path = wave_ax.plot(np.sin, x_range=[0, 0.01], color=SIN_CLR,
                                  stroke_width=3)
        self.add(wave_path)

        # Sweep
        self.narrator.silent(0.8)
        target_t = 2 * PI
        # Use updater to extend the path as theta moves
        def update_path(mob):
            t = theta.get_value()
            new_path = wave_ax.plot(np.sin,
                                     x_range=[0, max(t, 0.01)],
                                     color=SIN_CLR, stroke_width=3)
            mob.become(new_path)
        wave_path.add_updater(update_path)

        self.play(theta.animate.set_value(target_t), run_time=4.0)
        wave_path.remove_updater(update_path)
        self.narrator.silent(BEAT_L)

        # Reveal label
        wave_label = MathTex(r"y = \sin\theta", color=SIN_CLR,
                              font_size=36).next_to(wave_ax, UP, buff=0.2)
        self.play(Write(wave_label), run_time=1.0)
        self.narrator.silent(BEAT_L)


# ── S06: Radians ────────────────────────────────────────────────────
class S06_Radians(LessonArchetype):
    HEADING = "Radians"
    DEFINITION = "Measuring angle by arc length on the unit circle"
    ACCENT = ANGLE_CLR
    PERSONA = PERSONA_DEF

    def teach(self):
        self.teach_concept(
            term="Radians",
            definition="The arc length on a unit circle equals the angle in radians",
            example="A full circle = 2π radians (because circumference = 2π)",
            extra_dwell=2.0,
        )

        # Visualize: arc length = angle
        self.fade_heading()
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                  x_length=4.5, y_length=4.5,
                  axis_config={"color": DIM, "include_tip": False,
                               "include_numbers": False}).shift(LEFT * 2.5)
        circ = Circle(radius=1.15, color=DIM,
                      stroke_width=2).move_to(ax.c2p(0, 0))
        self.add(ax, circ)

        # Highlight an arc and label its length
        arc_30 = Arc(radius=1.15, start_angle=0, angle=PI / 6,
                     color=ANGLE_CLR, stroke_width=5,
                     arc_center=ax.c2p(0, 0))
        arc_label = MathTex(r"\text{arc} = \tfrac{\pi}{6}",
                            color=ANGLE_CLR, font_size=30)
        arc_label.next_to(ax, RIGHT, buff=0.5).shift(UP * 1.5)
        deg_label = MathTex(r"= 30^\circ", color=INK, font_size=30)
        deg_label.next_to(arc_label, DOWN, buff=0.3)

        self.play(Create(arc_30), Write(arc_label), run_time=1.2)
        self.narrator.silent(BEAT_M)
        self.play(Write(deg_label), run_time=0.8)
        self.narrator.silent(BEAT_L)

        # Show common conversions
        conversions = VGroup(
            MathTex(r"180^\circ = \pi", color=INK, font_size=28),
            MathTex(r"360^\circ = 2\pi", color=INK, font_size=28),
            MathTex(r"90^\circ = \tfrac{\pi}{2}", color=INK, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conversions.next_to(deg_label, DOWN, buff=0.6)
        for c in conversions:
            self.play(Write(c), run_time=0.6)
            self.narrator.silent(0.4)
        self.narrator.silent(BEAT_L)


# ── S07: Two-direction framework ────────────────────────────────────
class S07_Framework(MisconceptionArchetype):
    HEADING = ""
    PERSONA = PERSONA_DEF

    def teach(self):
        self.show_analytical_framework(
            title="From now on, just remember:",
            steps=[
                "Given angle θ:  find the point (cos θ, sin θ) on the unit circle",
                "Given a point (x, y) on the circle:  the angle is what got you there",
                "Both directions — same picture, no memorization needed",
            ],
            color=SIN_CLR,
        )


# ── FullLesson ──────────────────────────────────────────────────────
class FullLesson(Scene):
    def setup(self):
        apply_global_config()

    def construct(self):
        for SceneCls in [S01_Hook, S02_DefineUnitCircle, S03_SinCosAsCoords,
                          S04_Misconception, S05_ConnectGraph, S06_Radians,
                          S07_Framework]:
            scene_obj = SceneCls()
            scene_obj.renderer = self.renderer
            scene_obj.camera = self.camera
            scene_obj.setup()
            scene_obj.construct()
            self.wait(0.5)
            self.clear()
