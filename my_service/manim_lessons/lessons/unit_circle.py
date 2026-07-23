"""
Unit Circle — Lesson (always_redraw-FREE rewrite)
==================================================
Topic:   Unit Circle (sin/cos as coordinates, radians, connection to graphs)
Persona: 12th grade, 15 min focus

Why this rewrite exists:
  Manim's `always_redraw(lambda: ...)` calls `.become(func())` every frame.
  When the rebuilt object contains ANY text mobject (MathTex, Tex, Text,
  DecimalNumber, ...), the old vs new svg-subpath counts can differ as the
  string content changes (sign flip, decimal width, glyph swap), and
  `align_points` crashes with `IndexError: list index out of range`
  partway through the animation (typically near zero-crossings).

  This version uses NO always_redraw. Instead:
    - Geometric mobjects (Line, Dot, Arc, DashedLine) get `add_updater` that
      mutates them in place via `become(...)` of a same-type, same-#-points
      replacement. These never crash align_points because they have fixed
      subpath structure.
    - Numeric readouts use `DecimalNumber.add_updater(set_value(...))`.
      `set_value` only edits the underlying number — no `.become()` is
      called, so align_points is never invoked on the text.
    - Static labels (MathTex, Text) are built once and `self.add(...)`-ed.
      They never get rebuilt.

Render:
    manim -qm lessons/unit_circle.py FullLesson
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    Scene, Text, MathTex, VGroup, Rectangle, Circle, Dot, Line, DashedLine,
    Arc, Axes, ValueTracker, DecimalNumber,
    FadeIn, FadeOut, Write, Create, GrowFromCenter,
    LaggedStart, ReplacementTransform, Transform,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI,
)

from manim_lessons.archetypes import LessonArchetype, MisconceptionArchetype
from manim_lessons.lib.design_tokens import (
    apply_global_config, INK, DIM, GHOST,
    ACCENT_A, ACCENT_B, WARN,
    FS_TITLE, FS_H1, FS_H2, FS_BODY, FS_SMALL,
    BEAT_M, BEAT_L, STROKE_NORMAL,
)
from manim_lessons.lib.narrator import Narrator
from manim_lessons.lib.persona import Persona


# ── Semantic colors ────────────────────────────────────────────────
COS_CLR = ACCENT_B   # blue: x-coordinate, cosine
SIN_CLR = ACCENT_A   # yellow: y-coordinate, sine
ANGLE_CLR = WARN     # red: angle / arc

PERSONA_DEF = Persona(
    grade=12, focus_minutes=15,
    has=["basic trigonometry", "sine", "cosine"],
    lacks=["unit circle", "sine as coordinate", "cosine as coordinate", "radians"],
)


# ── Safe geometric updaters (factories) ────────────────────────────
# Each factory returns an updater function `f(mob)` that mutates a Line/Dot/
# Arc/DashedLine in place using `become(...)` of a same-shape replacement.
# These are safe because Line/Dot/Arc/DashedLine have fixed point counts —
# `align_points` will always succeed.

def _radius_line_updater(ax, theta):
    def upd(mob):
        t = theta.get_value()
        mob.become(Line(
            ax.c2p(0, 0),
            ax.c2p(np.cos(t), np.sin(t)),
            color=ANGLE_CLR, stroke_width=3,
        ))
    return upd


def _circle_point_updater(ax, theta, color=INK, radius=0.10):
    def upd(mob):
        t = theta.get_value()
        mob.become(Dot(
            ax.c2p(np.cos(t), np.sin(t)),
            color=color, radius=radius,
        ))
    return upd


def _angle_arc_updater(ax, theta):
    def upd(mob):
        t = theta.get_value()
        # Manim's Arc clamps to >=0; we clamp to a tiny positive number to keep
        # the subpath count stable when theta is exactly 0.
        safe_t = max(t, 1e-4)
        mob.become(Arc(
            radius=0.4, start_angle=0, angle=safe_t,
            color=ANGLE_CLR, stroke_width=3,
            arc_center=ax.c2p(0, 0),
        ))
    return upd


def _x_drop_updater(ax, theta):
    """DashedLine from (cos t, sin t) down to (cos t, 0)."""
    def upd(mob):
        t = theta.get_value()
        mob.become(DashedLine(
            ax.c2p(np.cos(t), np.sin(t)),
            ax.c2p(np.cos(t), 0),
            color=COS_CLR, stroke_width=2.5,
        ))
    return upd


def _y_drop_updater(ax, theta):
    """DashedLine from (cos t, sin t) over to (0, sin t)."""
    def upd(mob):
        t = theta.get_value()
        mob.become(DashedLine(
            ax.c2p(np.cos(t), np.sin(t)),
            ax.c2p(0, np.sin(t)),
            color=SIN_CLR, stroke_width=2.5,
        ))
    return upd


def _axis_tick_updater(ax, theta, axis: str, color):
    """A Dot sliding along the x- or y-axis tracking cos/sin."""
    def upd(mob):
        t = theta.get_value()
        pos = ax.c2p(np.cos(t), 0) if axis == "x" else ax.c2p(0, np.sin(t))
        mob.become(Dot(pos, color=color, radius=0.08))
    return upd


def _theta_label_pos_updater(ax, theta, label_mob):
    """Move (don't rebuild) a static \theta label to follow the arc midpoint."""
    def upd(mob):
        t = theta.get_value()
        half = t / 2
        mob.move_to(ax.c2p(0.55 * np.cos(half), 0.55 * np.sin(half)))
    return upd


# ── S01: Hook — the memorization trap ──────────────────────────────
class S01_Hook(Scene):
    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)

    def construct(self):
        title = Text("Quick — what's sin 30°?",
                     font_size=FS_TITLE, color=INK).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.narrator.silent(1.5)

        values = VGroup(
            MathTex(r"\sin 30^\circ = \tfrac{1}{2}", font_size=44, color=INK),
            MathTex(r"\sin 45^\circ = \tfrac{\sqrt{2}}{2}", font_size=44, color=INK),
            MathTex(r"\sin 60^\circ = \tfrac{\sqrt{3}}{2}", font_size=44, color=INK),
        ).arrange(DOWN, buff=0.6).shift(DOWN * 0.3)

        for v in values:
            self.play(Write(v), run_time=0.8)
            self.narrator.silent(0.5)
        self.narrator.silent(BEAT_M)

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


# ── S03: sin/cos AS coordinates (always_redraw-free) ───────────────
class S03_SinCosAsCoords(LessonArchetype):
    HEADING = ""
    ACCENT = SIN_CLR
    PERSONA = PERSONA_DEF

    def teach(self):
        # Axes & static circle
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                  x_length=5, y_length=5,
                  axis_config={"color": DIM, "include_tip": True,
                               "include_numbers": False}).shift(LEFT * 2.5)
        circ = Circle(radius=1.25, color=DIM,
                      stroke_width=STROKE_NORMAL).move_to(ax.c2p(0, 0))
        self.add(ax, circ)

        theta = ValueTracker(0.5)

        # ── Live geometric mobjects (build once, mutate via add_updater) ──
        t0 = theta.get_value()

        radius_line = Line(
            ax.c2p(0, 0),
            ax.c2p(np.cos(t0), np.sin(t0)),
            color=ANGLE_CLR, stroke_width=3,
        )
        radius_line.add_updater(_radius_line_updater(ax, theta))

        p_dot = Dot(
            ax.c2p(np.cos(t0), np.sin(t0)),
            color=INK, radius=0.10,
        )
        p_dot.add_updater(_circle_point_updater(ax, theta))

        arc = Arc(
            radius=0.4, start_angle=0, angle=max(t0, 1e-4),
            color=ANGLE_CLR, stroke_width=3,
            arc_center=ax.c2p(0, 0),
        )
        arc.add_updater(_angle_arc_updater(ax, theta))

        # Static theta label — only its *position* updates, content is fixed
        theta_label = MathTex(r"\theta", color=ANGLE_CLR, font_size=32)
        theta_label.move_to(ax.c2p(0.55 * np.cos(t0 / 2),
                                    0.55 * np.sin(t0 / 2)))
        theta_label.add_updater(_theta_label_pos_updater(ax, theta, theta_label))

        self.play(Create(radius_line), GrowFromCenter(p_dot), run_time=1.0)
        self.play(Create(arc), Write(theta_label), run_time=0.8)
        self.narrator.silent(BEAT_M)

        # ── Drop lines + axis ticks ──
        x_drop = DashedLine(
            ax.c2p(np.cos(t0), np.sin(t0)),
            ax.c2p(np.cos(t0), 0),
            color=COS_CLR, stroke_width=2.5,
        )
        x_drop.add_updater(_x_drop_updater(ax, theta))

        y_drop = DashedLine(
            ax.c2p(np.cos(t0), np.sin(t0)),
            ax.c2p(0, np.sin(t0)),
            color=SIN_CLR, stroke_width=2.5,
        )
        y_drop.add_updater(_y_drop_updater(ax, theta))

        x_tick = Dot(ax.c2p(np.cos(t0), 0), color=COS_CLR, radius=0.08)
        x_tick.add_updater(_axis_tick_updater(ax, theta, "x", COS_CLR))

        y_tick = Dot(ax.c2p(0, np.sin(t0)), color=SIN_CLR, radius=0.08)
        y_tick.add_updater(_axis_tick_updater(ax, theta, "y", SIN_CLR))

        self.play(Create(x_drop), GrowFromCenter(x_tick), run_time=1.0)
        self.play(Create(y_drop), GrowFromCenter(y_tick), run_time=1.0)
        self.narrator.silent(BEAT_M)

        # ── Numeric readout: STATIC label + DecimalNumber w/ set_value ──
        # CRITICAL: build the VGroup ONCE, add to scene, never wrap in
        # always_redraw. DecimalNumber.add_updater uses set_value internally,
        # which does NOT call .become(), so align_points is never invoked.

        x_label = MathTex(r"x = \cos\theta = ", color=COS_CLR, font_size=30)
        x_num = DecimalNumber(
            np.cos(t0),
            num_decimal_places=2,
            include_sign=True,     # +1.00 / -0.50 — fixed glyph width
            color=COS_CLR, font_size=30,
        )
        # set_value is safe: it mutates the existing DecimalNumber's submobjects
        # rather than constructing a new one, so no align_points pass happens.
        x_num.add_updater(lambda m: m.set_value(np.cos(theta.get_value())))
        x_readout = VGroup(x_label, x_num).arrange(RIGHT, buff=0.1)
        x_readout.move_to(RIGHT * 3.5 + UP * 1.2)

        y_label = MathTex(r"y = \sin\theta = ", color=SIN_CLR, font_size=30)
        y_num = DecimalNumber(
            np.sin(t0),
            num_decimal_places=2,
            include_sign=True,
            color=SIN_CLR, font_size=30,
        )
        y_num.add_updater(lambda m: m.set_value(np.sin(theta.get_value())))
        y_readout = VGroup(y_label, y_num).arrange(RIGHT, buff=0.1)
        y_readout.move_to(RIGHT * 3.5 + UP * 0.3)

        self.play(Write(x_readout), Write(y_readout), run_time=1.2)
        self.narrator.silent(BEAT_L)

        # ── Sweep through the classic angles ──
        # These sweeps cross zero (cos goes from + to -, sin keeps growing).
        # With the old always_redraw(MathTex(f"..."))) code, this is where the
        # IndexError happened. With DecimalNumber.set_value, it's safe.
        self.play(theta.animate.set_value(PI / 6), run_time=1.5)
        annotation_30 = MathTex(r"\theta = 30^\circ",
                                color=ANGLE_CLR, font_size=28)
        annotation_30.move_to(RIGHT * 3.5 + DOWN * 0.8)
        self.play(Write(annotation_30), run_time=0.8)
        self.narrator.silent(BEAT_L)

        self.play(theta.animate.set_value(PI / 4), run_time=1.2)
        self.narrator.silent(BEAT_M)
        self.play(theta.animate.set_value(PI / 3), run_time=1.2)
        self.narrator.silent(BEAT_M)
        # If you want to extend further (this is what crashed last time):
        # self.play(theta.animate.set_value(2 * PI / 3), run_time=2.0)  # safe now
        # self.play(theta.animate.set_value(PI), run_time=1.5)

        # Clean up updaters before leaving the scene — good hygiene, prevents
        # carryover if the renderer reuses the camera between scenes.
        for m in (radius_line, p_dot, arc, theta_label,
                  x_drop, y_drop, x_tick, y_tick, x_num, y_num):
            m.clear_updaters()


# ── S04: Misconception — they're coordinates, not magic numbers ────
class S04_Misconception(MisconceptionArchetype):
    HEADING = ""
    PERSONA = PERSONA_DEF

    def teach(self):
        title = Text("Back to that question...",
                     font_size=FS_H1, color=INK).to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.narrator.silent(1.0)

        recall = MathTex(r"\sin 30^\circ = \tfrac{1}{2}",
                         font_size=44, color=INK).shift(UP * 1.2)
        self.play(Write(recall), run_time=0.8)
        self.narrator.silent(BEAT_M)

        self.play(FadeOut(title), recall.animate.to_edge(UP, buff=0.5),
                  run_time=0.5)

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

        circ_ax = Axes(x_range=[-1.2, 1.2, 1], y_range=[-1.2, 1.2, 1],
                       x_length=3, y_length=3,
                       axis_config={"color": DIM, "include_tip": False,
                                    "include_numbers": False}).shift(LEFT * 5)
        circ = Circle(radius=0.75, color=DIM,
                      stroke_width=2).move_to(circ_ax.c2p(0, 0))
        self.add(circ_ax, circ)

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

        theta = ValueTracker(0.0)

        # ── Live geometric mobjects on the circle side ──
        t0 = theta.get_value()

        # Scale conversion helper — the small circle has radius 0.75 in user
        # units mapped to a 3-unit axes, so a unit-circle (cos t, sin t) maps
        # naturally through circ_ax.c2p (which goes [-1.2, 1.2] -> screen).
        def circ_pt(t):
            return circ_ax.c2p(np.cos(t), np.sin(t))

        radius_line = Line(circ_ax.c2p(0, 0), circ_pt(t0),
                            color=ANGLE_CLR, stroke_width=2.5)
        radius_line.add_updater(lambda m: m.become(Line(
            circ_ax.c2p(0, 0), circ_pt(theta.get_value()),
            color=ANGLE_CLR, stroke_width=2.5)))

        p_dot = Dot(circ_pt(t0), color=INK, radius=0.08)
        p_dot.add_updater(lambda m: m.become(Dot(
            circ_pt(theta.get_value()), color=INK, radius=0.08)))

        y_drop = DashedLine(circ_pt(t0),
                             circ_ax.c2p(0, np.sin(t0)),
                             color=SIN_CLR, stroke_width=2)
        y_drop.add_updater(lambda m: m.become(DashedLine(
            circ_pt(theta.get_value()),
            circ_ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, stroke_width=2)))

        y_marker = Dot(circ_ax.c2p(0, np.sin(t0)),
                        color=SIN_CLR, radius=0.07)
        y_marker.add_updater(lambda m: m.become(Dot(
            circ_ax.c2p(0, np.sin(theta.get_value())),
            color=SIN_CLR, radius=0.07)))

        # ── Wave dot tracks (theta, sin(theta)) on the right ──
        wave_dot = Dot(
            wave_ax.c2p(t0, np.sin(t0)),
            color=SIN_CLR, radius=0.09,
        )
        wave_dot.add_updater(lambda m: m.become(Dot(
            wave_ax.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=SIN_CLR, radius=0.09)))

        connector = DashedLine(
            circ_ax.c2p(0, np.sin(t0)),
            wave_ax.c2p(t0, np.sin(t0)),
            color=SIN_CLR, stroke_width=1.5,
        )
        connector.add_updater(lambda m: m.become(DashedLine(
            circ_ax.c2p(0, np.sin(theta.get_value())),
            wave_ax.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=SIN_CLR, stroke_width=1.5)))

        self.add(radius_line, p_dot, y_drop, y_marker, wave_dot, connector)

        # ── The growing wave path ──
        # plot() returns a ParametricFunction — also geometric, no Tex inside.
        # We use add_updater + become to grow it as theta sweeps.
        wave_path = wave_ax.plot(np.sin, x_range=[0, 0.01],
                                  color=SIN_CLR, stroke_width=3)

        def grow_wave(mob):
            t = theta.get_value()
            mob.become(wave_ax.plot(
                np.sin, x_range=[0, max(t, 0.01)],
                color=SIN_CLR, stroke_width=3,
            ))
        wave_path.add_updater(grow_wave)
        self.add(wave_path)

        self.narrator.silent(0.8)
        self.play(theta.animate.set_value(2 * PI), run_time=4.0)

        # Stop all updaters before adding the label
        for m in (radius_line, p_dot, y_drop, y_marker,
                  wave_dot, connector, wave_path):
            m.clear_updaters()
        self.narrator.silent(BEAT_L)

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

        self.fade_heading()
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                  x_length=4.5, y_length=4.5,
                  axis_config={"color": DIM, "include_tip": False,
                               "include_numbers": False}).shift(LEFT * 2.5)
        circ = Circle(radius=1.15, color=DIM,
                      stroke_width=2).move_to(ax.c2p(0, 0))
        self.add(ax, circ)

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
