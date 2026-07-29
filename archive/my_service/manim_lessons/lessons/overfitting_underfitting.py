"""
Overfitting vs Underfitting — Lesson
====================================
Topic:   Why the Best Model Is Not Always the Most Complex
Persona: 8th grade, 10 min focus
         Has:   scatter plots, line graphs
         Lacks: NO idea what "model" means; no stats; no functions beyond arithmetic
KLPs:    training vs test error; generalization; model complexity;
         bias-variance trade-off (conceptual); overfitting signs;
         underfitting signs

5-point recipe coverage:
  R1 deeper layer:   bias-variance U-curve as the integrating frame
  R2 multi-context:  3-student analogy + ML scatter side-by-side
  R3 misconception:  "more complex = better" -> wrong
  R4 framework:      3-step diagnostic at end (boxed)
  R5 signaling:      every term has a synced visual highlight
  R6 colors:         GREEN=sweet spot, RED=failure (over+under both bad),
                     YELLOW=neutral/complexity axis
  R7 boxed answers:  framework + key conclusions framed

Render:
    manim -qm lessons/overfitting_underfitting.py FullLesson
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    Scene, Text, VGroup, Rectangle, Dot, Line, Axes,
    FadeIn, FadeOut, Write, Create, GrowFromCenter,
    LaggedStart, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT, ORIGIN
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
GOOD = ACCENT_B   # green: sweet spot, correct
BAD = WARN        # red: failure (over- or under-fit)
NEU = ACCENT_A    # yellow: neutral / complexity / new

PERSONA_DEF = Persona(
    grade=8, focus_minutes=10,
    has=["scatter plot", "line graph"],
    lacks=["model", "training error", "test error",
           "complexity", "overfitting", "underfitting"],
)


# ── S01: Hook — three students before an exam ───────────────────────
class S01_Hook(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("3 students before a math test",
                     font_size=FS_H1, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.narrator.silent(1.2)

        # 3 students, side by side
        students_data = [
            ("Anna", "didn't\nstudy", BAD),
            ("Ben", "memorized\nevery past quiz\nword for word", NEU),
            ("Cathy", "understood\nthe concepts", GOOD),
        ]
        student_groups = []
        for i, (name, desc, color) in enumerate(students_data):
            box = Rectangle(width=3.5, height=2.5, color=color,
                            stroke_width=STROKE_NORMAL,
                            fill_color=color, fill_opacity=0.1)
            name_t = Text(name, font_size=FS_H2, color=color, weight="BOLD")
            desc_t = Text(desc, font_size=FS_SMALL, color=INK, line_spacing=0.8)
            inner = VGroup(name_t, desc_t).arrange(DOWN, buff=0.25)
            inner.move_to(box.get_center())
            group = VGroup(box, inner).shift(LEFT * 4.5 + RIGHT * i * 4.5 + DOWN * 0.3)
            student_groups.append(group)

        for s in student_groups:
            self.play(FadeIn(s, shift=UP * 0.3), run_time=0.7)
            self.narrator.silent(0.6)

        question = Text("Who passes on NEW questions they haven't seen?",
                        font_size=FS_BODY, color=NEU).to_edge(DOWN, buff=0.5)
        self.play(Write(question), run_time=1.2)
        self.narrator.silent(BEAT_L)
        self.narrator.silent(BEAT_M)


# ── S02: Define "model" — critical because persona has no clue ──────
class S02_WhatsAModel(LessonArchetype):
    HEADING = "What is a 'model'?"
    ACCENT = NEU
    PERSONA = PERSONA_DEF

    def teach(self):
        # Define model (counts toward lacks coverage)
        self.teach_concept(
            term="Model",
            definition="A RULE that takes input and gives a prediction",
            example="red, round fruit → guess: 'apple'",
            extra_dwell=2.0,
        )
        # Visualize: input → rule → output flow
        flow = self._flow_diagram()
        self.play(FadeIn(flow), run_time=1.0)
        self.narrator.silent(BEAT_L)

    def _flow_diagram(self):
        positions = [LEFT * 4.5, ORIGIN, RIGHT * 4.5]
        labels = [("Input", "red, round\nfruit"),
                  ("Model\n(the rule)", "if red & round\n→ apple"),
                  ("Output", '"apple"')]
        colors = [DIM, GOOD, NEU]
        boxes = []
        for pos, (head, body), col in zip(positions, labels, colors):
            box = Rectangle(width=2.8, height=1.8, color=col, stroke_width=2,
                            fill_color=col, fill_opacity=0.08)
            head_t = Text(head, font_size=FS_SMALL, color=col, weight="BOLD")
            body_t = Text(body, font_size=FS_SMALL, color=INK, line_spacing=0.8)
            inner = VGroup(head_t, body_t).arrange(DOWN, buff=0.15)
            inner.move_to(box.get_center())
            grp = VGroup(box, inner).move_to(pos + DOWN * 1.2)
            boxes.append(grp)
        arrows = VGroup(
            Line(boxes[0].get_right(), boxes[1].get_left(), color=DIM,
                 stroke_width=2).add_tip(tip_length=0.15),
            Line(boxes[1].get_right(), boxes[2].get_left(), color=DIM,
                 stroke_width=2).add_tip(tip_length=0.15),
        )
        return VGroup(*boxes, arrows)


# ── S03: Misconception — "more complex = better" ────────────────────
class S03_Misconception(MisconceptionArchetype):
    HEADING = ""
    PERSONA = PERSONA_DEF

    def teach(self):
        title = Text("So... should our rule be as fancy as possible?",
                     font_size=FS_H1, color=INK).to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.narrator.silent(1.0)

        # Build a scatter and fit two curves
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2],
                  x_length=6, y_length=3.8,
                  axis_config={"color": DIM, "include_tip": False,
                               "include_numbers": False}).shift(DOWN * 0.5)
        np.random.seed(0)
        xs = np.linspace(1, 9, 7)
        ys = xs + np.random.randn(7) * 0.6
        dots = VGroup(*[Dot(ax.c2p(x, y), color=INK, radius=0.08)
                         for x, y in zip(xs, ys)])
        ax_label = Text("practice problems we've seen",
                        font_size=FS_SMALL, color=DIM).next_to(ax, DOWN, buff=0.3)
        self.play(Create(ax), FadeIn(dots), Write(ax_label), run_time=1.5)
        self.narrator.silent(BEAT_M)

        # Simple straight line
        simple = ax.plot(lambda x: x, x_range=[0.5, 9.5],
                         color=GOOD, stroke_width=3.5)
        simple_label = Text("simple rule\n(one straight line)",
                            font_size=FS_SMALL, color=GOOD, line_spacing=0.8)
        simple_label.next_to(ax, RIGHT, buff=0.4).shift(UP * 1.0)
        self.play(Create(simple), Write(simple_label), run_time=1.5)
        self.narrator.silent(BEAT_M)

        # Squiggly overfit polynomial through every point
        coeffs = np.polyfit(xs, ys, deg=6)
        squiggly = ax.plot(lambda x: float(np.polyval(coeffs, x)),
                           x_range=[1.0, 9.0],
                           color=BAD, stroke_width=3.5)
        complex_label = Text("fancy rule\n(touches every dot)",
                             font_size=FS_SMALL, color=BAD, line_spacing=0.8)
        complex_label.next_to(ax, RIGHT, buff=0.4).shift(DOWN * 1.0)
        self.play(Create(squiggly), Write(complex_label), run_time=1.8)
        self.narrator.silent(BEAT_L)

        # New question appears off the curve
        new_dot = Dot(ax.c2p(5.5, 5.2), color=NEU, radius=0.13)
        new_tag = Text("← NEW question", font_size=FS_SMALL,
                       color=NEU).next_to(new_dot, RIGHT, buff=0.15)
        self.play(GrowFromCenter(new_dot), Write(new_tag), run_time=1.0)
        self.narrator.silent(BEAT_L)

        # Fade scatter then show misconception panel
        self.play(FadeOut(VGroup(title, ax, dots, simple, simple_label,
                                  squiggly, complex_label, new_dot, new_tag,
                                  ax_label)),
                  run_time=0.6)
        self.show_misconception_panel(
            wrong_belief="A more complex rule\nis always better.",
            correct_belief="Complex rules MEMORIZE old data\nbut fail on NEW data.",
            why_wrong="(it touches every old dot, but the new dot is far away)",
        )


# ── S04: The U-curve — the centerpiece ──────────────────────────────
class S04_UCurve(LessonArchetype):
    HEADING = "Two kinds of error"
    ACCENT = NEU
    PERSONA = PERSONA_DEF

    def teach(self):
        # Define both error types (covers 2 lacks concepts)
        self.teach_concept(
            term="Training error",
            definition="How wrong on OLD problems we've practiced",
            example="quiz questions Cathy has already seen",
        )
        self.teach_concept(
            term="Test error",
            definition="How wrong on NEW problems we haven't seen",
            example="fresh exam questions on test day",
        )
        # Also covers 'complexity' (third lacks)
        self.teach_concept(
            term="Complexity",
            definition="How 'fancy' the rule is — more wiggles = more complex",
            example="a straight line is simple, a wavy curve is complex",
        )

        # Build the U-curve
        self.play(FadeOut(*[m for m in self.mobjects]), run_time=0.4)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 5, 1],
                  x_length=9, y_length=4.5,
                  axis_config={"color": DIM, "include_tip": False,
                               "include_numbers": False}).shift(DOWN * 0.3)
        x_label = Text("complexity →", font_size=FS_SMALL, color=DIM)
        x_label.next_to(ax, DOWN, buff=0.25)
        y_label = Text("error", font_size=FS_SMALL, color=DIM)
        y_label.next_to(ax, LEFT, buff=0.2).rotate(np.pi / 2)
        self.play(Create(ax), Write(x_label), Write(y_label), run_time=1.2)
        self.narrator.silent(BEAT_M)

        # Training error: always decreasing (R5 signaling: written as drawn)
        train_curve = ax.plot(lambda x: 4 * np.exp(-0.35 * x) + 0.2,
                              x_range=[0.3, 9.7],
                              color=GOOD, stroke_width=3.5)
        train_label = Text("training error", font_size=FS_SMALL, color=GOOD)
        train_label.move_to(ax.c2p(8.5, 0.7))
        self.play(Create(train_curve), Write(train_label), run_time=1.8)
        self.narrator.silent(BEAT_M)

        # Test error: U-shaped
        test_curve = ax.plot(lambda x: 0.16 * (x - 4) ** 2 + 0.7,
                             x_range=[0.3, 9.7],
                             color=BAD, stroke_width=3.5)
        test_label = Text("test error", font_size=FS_SMALL, color=BAD)
        test_label.move_to(ax.c2p(8.5, 3.4))
        self.play(Create(test_curve), Write(test_label), run_time=1.8)
        self.narrator.silent(BEAT_L)

        # Three regions, each with semantic color (R6) and labels (R5)
        bands = [
            (1.0, 2.8, "underfit", BAD),
            (3.2, 5.0, "sweet spot", GOOD),
            (5.4, 9.5, "overfit", BAD),
        ]
        for x_lo, x_hi, tag, col in bands:
            band = Rectangle(
                width=ax.c2p(x_hi, 0)[0] - ax.c2p(x_lo, 0)[0],
                height=ax.c2p(0, 5)[1] - ax.c2p(0, 0)[1],
                color=col, fill_color=col, fill_opacity=0.12, stroke_width=0,
            )
            band.move_to([(ax.c2p(x_lo, 2.5)[0] + ax.c2p(x_hi, 2.5)[0]) / 2,
                          ax.c2p(0, 2.5)[1], 0])
            tag_t = Text(tag, font_size=FS_SMALL, color=col,
                         weight="BOLD" if tag == "sweet spot" else "NORMAL")
            tag_t.next_to(band, UP, buff=0.08)
            self.play(FadeIn(band), Write(tag_t), run_time=0.7)
            self.narrator.silent(0.6)

        # Final reveal: the sweet spot is where test error is minimum
        sweet_dot = Dot(ax.c2p(4, 0.7), color=GOOD, radius=0.13)
        sweet_arrow = Line(ax.c2p(4, -0.5), ax.c2p(4, 0.6),
                           color=GOOD, stroke_width=3).add_tip(tip_length=0.15)
        sweet_msg = Text("← lowest test error", font_size=FS_SMALL, color=GOOD)
        sweet_msg.next_to(sweet_arrow, DOWN, buff=0.05)
        self.play(GrowFromCenter(sweet_dot), Create(sweet_arrow),
                  Write(sweet_msg), run_time=1.2)
        self.narrator.silent(BEAT_L)


# ── S05: Map back to the 3 students (R2: multi-context) ─────────────
class S05_ConnectStudents(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("Same idea, in plain words",
                     font_size=FS_H1, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.narrator.silent(1.0)

        rows_data = [
            ("Anna (didn't study)",  "→ underfit",  "both errors HIGH",     BAD),
            ("Ben (memorized everything)", "→ overfit",   "train LOW, test HIGH", BAD),
            ("Cathy (understood)",    "→ sweet spot","both errors LOW",      GOOD),
        ]
        rows = VGroup()
        for who, label, sig, col in rows_data:
            who_t = Text(who, font_size=FS_BODY, color=INK)
            arrow_t = Text(label, font_size=FS_BODY, color=col, weight="BOLD")
            sig_t = Text(sig, font_size=FS_SMALL, color=DIM)
            row = VGroup(who_t, arrow_t, sig_t).arrange(RIGHT, buff=0.5)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(DOWN * 0.3)

        for row in rows:
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in row],
                                   lag_ratio=0.25), run_time=0.9)
            self.narrator.silent(0.8)
        self.narrator.silent(BEAT_L)


# ── S06: Diagnostic framework (R4 + R7) ─────────────────────────────
class S06_Framework(MisconceptionArchetype):
    HEADING = ""
    PERSONA = PERSONA_DEF

    def teach(self):
        self.show_analytical_framework(
            title="Got a new model? Ask these 3 things.",
            steps=[
                "Is training error high?  → underfit (rule too simple)",
                "Train low but test high?  → overfit (rule memorized)",
                "Both low?  → sweet spot — ship it.",
            ],
            color=GOOD,
        )


# ── FullLesson ──────────────────────────────────────────────────────
class FullLesson(Scene):
    def setup(self):
        apply_global_config()

    def construct(self):
        for SceneCls in [S01_Hook, S02_WhatsAModel, S03_Misconception,
                          S04_UCurve, S05_ConnectStudents, S06_Framework]:
            scene_obj = SceneCls()
            scene_obj.renderer = self.renderer
            scene_obj.camera = self.camera
            scene_obj.setup()
            scene_obj.construct()
            self.wait(0.5)
            self.clear()
