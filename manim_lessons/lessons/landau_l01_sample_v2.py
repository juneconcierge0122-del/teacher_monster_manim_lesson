"""Story-driven, caption-free, sentence-synchronised Landau sample."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import av
import numpy as np
from manim import (
    Arc, Arrow, Axes, Create, DashedLine, Dot, DOWN, FadeIn, FadeOut,
    GrowArrow, LEFT, Line,
    PI, RIGHT, Scene, Text, Transform, UP, ValueTracker, VGroup, Write, always_redraw,
    linear,
)

from manim_lessons.lib.design_tokens import (
    ACCENT_A, ACCENT_B, ACCENT_C, DIM, FS_BODY, FS_H1, FS_SMALL, GHOST,
    INK, WARN, apply_global_config,
)
from manim_lessons.localization.landau_l01_sample_v2 import LOCALES


class LandauL01StoryBase(Scene):
    LANGUAGE = "zh-TW"

    def setup(self):
        apply_global_config()
        self.hold_clock = ValueTracker(0)
        self.copy = LOCALES[self.LANGUAGE]
        self.screen = self.copy["screen"]
        self.audio_dir = (
            pathlib.Path(__file__).resolve().parents[1]
            / "samples" / "audio_v2" / self.LANGUAGE
        )

    def text(self, key, size=FS_BODY, color=INK):
        mob = Text(self.screen[key], font_size=size, color=color)
        if mob.width > 11.8:
            mob.scale_to_fit_width(11.8)
        return mob

    def audio_duration(self, index):
        path = self.audio_dir / f"{index:02d}.mp3"
        with av.open(str(path)) as container:
            return float(container.duration / av.time_base)

    def speak(self, index, *animations, minimum=0.0, animation_time=1.2):
        """Start one sentence, reveal promptly, then hold for the narration.

        Audio controls the total beat length, but never stretches a Write or
        Fade across the whole sentence. This keeps the screen readable and
        avoids an apparently blank midpoint during long transitions.
        """
        path = self.audio_dir / f"{index:02d}.mp3"
        duration = max(self.audio_duration(index), minimum)
        self.add_sound(str(path))
        if animations:
            reveal_time = min(animation_time, duration)
            self.play(*animations, run_time=reveal_time)
            hold_time = max(duration - reveal_time, 0)
            if hold_time:
                # A real (invisible) animation keeps always_redraw geometry in
                # every encoded frame; Scene.wait may freeze it out.
                self.play(
                    self.hold_clock.animate.increment_value(1),
                    run_time=hold_time,
                    rate_func=linear,
                )
            return
        self.play(
            self.hold_clock.animate.increment_value(1),
            run_time=duration,
            rate_func=linear,
        )

    def construct(self):
        pivot = UP * 2.65
        length = 3.25
        theta = ValueTracker(-0.62)
        bob_pos = lambda: pivot + length * np.array([
            np.sin(theta.get_value()), -np.cos(theta.get_value()), 0
        ])
        rod = always_redraw(lambda: Line(pivot, bob_pos(), color=INK, stroke_width=4))
        bob = always_redraw(lambda: Dot(bob_pos(), radius=0.22, color=ACCENT_A))
        trail = Arc(radius=length, start_angle=-PI / 2 - 0.72, angle=1.44,
                    arc_center=pivot, color=GHOST, stroke_width=2)
        pivot_dot = Dot(pivot, radius=0.08, color=DIM)

        # A single visual story begins immediately; there is no title card.
        self.add(trail, pivot_dot, rod, bob)
        # Keep the physical object alive during the opening narration.  A
        # subtle oscillation prevents the 8-second setup beat from reading as
        # an empty screen while the voice introduces the problem.
        pendulum_motion = lambda m, dt: m.set_value(0.72 * np.sin(self.time * 1.35))
        theta.add_updater(pendulum_motion)
        self.speak(0)
        # The opening swing needs updaters; subsequent story panels need a
        # stable pendulum that Manim can cache without dropping it on holds.
        settled_pos = bob_pos()
        self.remove(rod, bob)
        rod = Line(pivot, settled_pos, color=INK, stroke_width=4)
        bob = Dot(settled_pos, radius=0.22, color=ACCENT_A)
        self.add(rod, bob)

        axes = Axes(
            x_range=[-4, 4, 1], y_range=[-4, 1, 1],
            x_length=7.0, y_length=4.2, tips=True,
            axis_config={"color": GHOST, "stroke_width": 2},
        ).shift(DOWN * 0.25)
        x_label = Text("x", font_size=28, color=ACCENT_C).next_to(axes.x_axis, RIGHT)
        y_label = Text("y", font_size=28, color=ACCENT_C).next_to(axes.y_axis, UP)
        two = self.text("xy", FS_H1, ACCENT_C).to_corner(UP + LEFT, buff=0.45)
        self.speak(1, FadeIn(axes), FadeIn(x_label), FadeIn(y_label), Write(two))
        theta.remove_updater(pendulum_motion)

        constraint = self.text("constraint", FS_H1, WARN).to_edge(DOWN, buff=0.7)
        dependent = self.text("not_independent", FS_BODY, DIM).next_to(constraint, UP, buff=0.25)
        self.speak(2, Write(constraint), FadeIn(dependent))

        vertical = DashedLine(pivot, pivot + DOWN * 3.5, color=GHOST)
        angle = Arc(radius=0.72, start_angle=-PI / 2,
                    angle=-theta.get_value(), arc_center=pivot, color=ACCENT_B)
        q_text = self.text("q", FS_H1, ACCENT_B).to_corner(UP + RIGHT, buff=0.45)
        self.speak(
            3,
            FadeOut(VGroup(axes, x_label, y_label, two, constraint, dependent)),
            Create(vertical), Create(angle), Write(q_text),
        )

        fixed = self.text("position", FS_BODY, ACCENT_B).to_edge(DOWN, buff=0.65)
        target_theta = -0.28
        target_pos = pivot + length * np.array([
            np.sin(target_theta), -np.cos(target_theta), 0
        ])
        self.speak(
            4,
            Transform(rod, Line(pivot, target_pos, color=INK, stroke_width=4)),
            Transform(bob, Dot(target_pos, radius=0.22, color=ACCENT_A)),
            Write(fixed),
            animation_time=2.0,
        )

        # Freeze the common position, then reveal two possible velocity arrows.
        center_pos = pivot + DOWN * length
        rod.become(Line(pivot, center_pos, color=INK, stroke_width=4))
        bob.become(Dot(center_pos, radius=0.22, color=ACCENT_A))
        left_arrow = Arrow(LEFT * 0.15 + DOWN * 0.65, LEFT * 2.1 + DOWN * 0.65,
                           color=ACCENT_C, buff=0)
        right_arrow = Arrow(RIGHT * 0.15 + DOWN * 0.65, RIGHT * 2.1 + DOWN * 0.65,
                            color=ACCENT_C, buff=0)
        same = self.text("same_position", FS_BODY, ACCENT_B).shift(DOWN * 1.45)
        opposite = self.text("opposite_motion", FS_BODY, ACCENT_C).to_edge(DOWN, buff=0.4)
        self.speak(5, FadeOut(fixed), GrowArrow(left_arrow), GrowArrow(right_arrow),
                   Write(same), Write(opposite))

        state = self.text("state", FS_H1, ACCENT_A).to_edge(UP, buff=0.5)
        self.speak(6, FadeOut(VGroup(q_text, same, opposite)), Write(state))

        ending = self.text("ending", FS_H1, INK).to_edge(DOWN, buff=0.55)
        end_theta = 0.58
        end_pos = pivot + length * np.array([
            np.sin(end_theta), -np.cos(end_theta), 0
        ])
        self.speak(
            7,
            FadeOut(VGroup(left_arrow, right_arrow, vertical, angle)),
            Transform(rod, Line(pivot, end_pos, color=INK, stroke_width=4)),
            Transform(bob, Dot(end_pos, radius=0.22, color=ACCENT_A)),
            Write(ending),
            animation_time=2.0,
        )
        self.wait(0.8)


class LandauL01StoryZH(LandauL01StoryBase):
    LANGUAGE = "zh-TW"


class LandauL01StoryEN(LandauL01StoryBase):
    LANGUAGE = "en"
