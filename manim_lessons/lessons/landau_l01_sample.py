"""Bilingual audiovisual sample for Landau Volume 1, sections 1–2.

Both language scenes use the same geometry, equations, timing, and animation
logic. Only localized display text and captions differ.

Render:
    manim -ql lessons/landau_l01_sample.py LandauL01SampleZH
    manim -ql lessons/landau_l01_sample.py LandauL01SampleEN
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    Arc, Arrow, Axes, Circle, Create, DashedLine, Dot, DOWN,
    FadeIn, FadeOut, GrowArrow, LEFT, Line,
    ORIGIN, PI, RIGHT, Scene, Text, Transform, UP, ValueTracker,
    VGroup, Write, always_redraw,
)

from manim_lessons.lib.design_tokens import (
    ACCENT_A, ACCENT_B, ACCENT_C, BG, DIM, FS_BODY, FS_CAPTION, FS_H1,
    FS_SMALL, GHOST, INK, WARN, apply_global_config,
)
from manim_lessons.lib.narrator import Narrator
from manim_lessons.localization.landau_l01_sample import strings


class LandauL01SampleBase(Scene):
    LANGUAGE = "zh-TW"

    def setup(self):
        apply_global_config()
        self.s = strings(self.LANGUAGE)
        max_chars = 25 if self.LANGUAGE == "zh-TW" else 52
        self.narrator = Narrator(self, max_chars_per_line=max_chars)

    def label(self, key, size=FS_BODY, color=INK):
        mob = Text(self.s[key], font_size=size, color=color)
        if mob.width > 12.2:
            mob.scale_to_fit_width(12.2)
        return mob

    def construct(self):
        self.opening()
        self.pendulum_coordinates()
        self.derivation()
        self.state_and_question()
        self.recap()

    def opening(self):
        title = self.label("title", FS_H1, ACCENT_A).to_edge(UP, buff=0.7)
        objective = self.label("objective", FS_BODY, INK)
        prereq = self.label("prereq", FS_SMALL, DIM)
        cards = VGroup(objective, prereq).arrange(DOWN, buff=0.25)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(cards, shift=UP * 0.2), run_time=0.8)
        self.narrator.say(self.s["objective"], 3.0)
        self.narrator.say(self.s["prereq"], 2.5)
        self.narrator.clear()
        self.play(FadeOut(VGroup(title, cards)), run_time=0.6)

    def pendulum_coordinates(self):
        pivot = UP * 2.2 + LEFT * 2.5
        length = 2.7
        theta = ValueTracker(-0.65)
        bob_pos = lambda: pivot + length * np.array([
            np.sin(theta.get_value()), -np.cos(theta.get_value()), 0
        ])
        rod = always_redraw(lambda: Line(pivot, bob_pos(), color=INK, stroke_width=4))
        bob = always_redraw(lambda: Dot(bob_pos(), radius=0.18, color=ACCENT_A))
        vertical = DashedLine(pivot, pivot + DOWN * 3.0, color=GHOST)
        # Keep the angle marker static while the bob moves through zero;
        # a zero-length dynamically rebuilt Arc has no Bézier path in Manim.
        angle = Arc(
            radius=0.62, start_angle=-PI / 2,
            angle=-theta.get_value(), arc_center=pivot, color=ACCENT_B
        )
        theta_label = Text("q = θ", color=ACCENT_B, font_size=38).next_to(pivot, RIGHT)
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 1, 1],
            x_length=5.0, y_length=3.4, tips=True,
            axis_config={"color": GHOST, "stroke_width": 2},
        ).shift(RIGHT * 3.5 + UP * 0.15)
        xy_dot = always_redraw(lambda: Dot(
            axes.c2p(length * np.sin(theta.get_value()),
                     -length * np.cos(theta.get_value())),
            color=ACCENT_A, radius=0.12,
        ))
        x0 = length * np.sin(theta.get_value())
        y0 = -length * np.cos(theta.get_value())
        xy_lines = VGroup(
            DashedLine(axes.c2p(0, y0), axes.c2p(x0, y0), color=ACCENT_C),
            DashedLine(axes.c2p(x0, 0), axes.c2p(x0, y0), color=ACCENT_C),
        )
        xy = Text("x     y", color=ACCENT_C, font_size=34).next_to(axes, UP)

        hook = self.label("hook", FS_H1, INK).to_edge(UP, buff=0.4)
        self.play(Write(hook), run_time=1.0)
        self.play(Create(vertical), Create(rod), FadeIn(bob), Create(angle), Write(theta_label))
        self.narrator.say(self.s["hook"], 4.0)
        self.play(Create(axes), FadeIn(xy_dot), Create(xy_lines), Write(xy), run_time=1.2)
        redundant = self.label("redundant", FS_SMALL, DIM).move_to(RIGHT * 3.5 + DOWN * 2.05)
        constraint = Text(self.s["constraint"], color=WARN, font_size=32).next_to(redundant, DOWN, buff=0.12)
        self.play(Write(redundant), Write(constraint))
        self.narrator.say(self.s["redundant"], 3.5)
        self.play(theta.animate.set_value(0.65), run_time=2.0)
        self.play(theta.animate.set_value(-0.30), run_time=1.5)
        one = self.label("one_number", FS_BODY, ACCENT_B).to_edge(DOWN, buff=0.35)
        self.play(Write(one))
        self.narrator.say(self.s["one_number"], 3.5)
        self.narrator.clear()
        self.play(FadeOut(VGroup(hook, vertical, rod, bob, angle, theta_label,
                                 axes, xy_dot, xy_lines, xy, redundant,
                                 constraint, one)), run_time=0.8)

    def derivation(self):
        definition = self.label("generalized", FS_BODY, ACCENT_B).to_edge(UP, buff=0.55)
        q = Text(self.s["derive_1"], color=ACCENT_B, font_size=46)
        pos = Text(self.s["derive_2"], color=INK, font_size=40)
        vel = Text(self.s["derive_3"], color=ACCENT_A, font_size=38)
        steps = VGroup(q, pos, vel).arrange(DOWN, buff=0.65).shift(DOWN * 0.25)
        self.play(Write(definition))
        self.narrator.say(self.s["generalized"], 5.0)
        self.play(Write(q))
        self.narrator.say("q " + ("可以選成擺角 theta。" if self.LANGUAGE == "zh-TW" else "may be chosen as the angle theta."), 2.8)
        self.play(Write(pos), run_time=1.2)
        self.narrator.say(("幾何關係把角度轉成直角座標。" if self.LANGUAGE == "zh-TW" else "Geometry converts the angle into Cartesian coordinates."), 3.5)
        self.play(Write(vel), run_time=1.2)
        self.narrator.say(("對時間微分，廣義速度 q dot 就決定實際速度。" if self.LANGUAGE == "zh-TW" else "Differentiate in time: generalized velocity q dot fixes the physical velocity."), 4.2)
        self.narrator.clear()
        self.play(FadeOut(VGroup(definition, steps)), run_time=0.7)

    def state_and_question(self):
        state = Text(self.s["state"], color=ACCENT_A, font_size=44).to_edge(UP, buff=0.7)
        left_bob = Dot(LEFT * 2.7, color=ACCENT_A, radius=0.18)
        right_bob = left_bob.copy().shift(RIGHT * 5.4)
        arrow_l = Arrow(left_bob.get_center() + RIGHT * 0.4,
                        left_bob.get_center() + LEFT * 1.0, color=ACCENT_C)
        arrow_r = Arrow(right_bob.get_center() + LEFT * 0.4,
                        right_bob.get_center() + RIGHT * 1.0, color=ACCENT_C)
        same_q = Text("q = q₀", color=ACCENT_B, font_size=38).shift(DOWN * 1.1)
        velocities = Text("q̇ < 0                 q̇ > 0",
                          color=ACCENT_C, font_size=36).shift(DOWN * 2.1)
        self.play(Write(state), FadeIn(left_bob), FadeIn(right_bob))
        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r), Write(same_q), Write(velocities))
        self.narrator.say(self.s["question"], 5.0)
        answer = self.label("answer", FS_BODY, WARN).to_edge(DOWN, buff=0.35)
        self.play(Write(answer))
        self.narrator.say(self.s["answer"], 5.0)
        self.narrator.clear()
        self.play(FadeOut(VGroup(state, left_bob, right_bob, arrow_l, arrow_r,
                                 same_q, velocities, answer)), run_time=0.7)

    def recap(self):
        title_text = "本課摘要" if self.LANGUAGE == "zh-TW" else "Summary"
        title = Text(title_text, font_size=FS_H1, color=ACCENT_A).to_edge(UP, buff=0.65)
        dots = VGroup()
        for key, color in zip(("summary_1", "summary_2", "summary_3"),
                              (ACCENT_B, ACCENT_C, ACCENT_A)):
            marker = Circle(radius=0.08, color=color, fill_opacity=1)
            line = self.label(key, FS_BODY, INK)
            dots.add(VGroup(marker, line).arrange(RIGHT, buff=0.3))
        dots.arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(DOWN * 0.25)
        self.play(Write(title))
        for row, key in zip(dots, ("summary_1", "summary_2", "summary_3")):
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
            self.narrator.say(self.s[key], 3.2)
        self.narrator.clear()
        self.wait(1.0)


class LandauL01SampleZH(LandauL01SampleBase):
    LANGUAGE = "zh-TW"


class LandauL01SampleEN(LandauL01SampleBase):
    LANGUAGE = "en"
