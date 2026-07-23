"""Landau lesson 02: a story-driven, caption-free action principle video."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import av, numpy as np
from manim import Arc, Create, Dot, FadeIn, FadeOut, Line, ORIGIN, Scene, Text, UP, DOWN, LEFT, RIGHT, VGroup, Write, ValueTracker, linear
from manim_lessons.lib.design_tokens import ACCENT_A, ACCENT_B, ACCENT_C, DIM, FS_BODY, FS_H1, GHOST, INK, WARN, apply_global_config
from manim_lessons.localization.landau_l02_action import LOCALES

class ActionStoryBase(Scene):
    LANGUAGE="zh-TW"
    def setup(self):
        apply_global_config(); self.data=LOCALES[self.LANGUAGE]; self.screen=self.data["screen"]; self.clock=ValueTracker(0)
        self.audio_dir=pathlib.Path(__file__).resolve().parents[1]/"samples"/"audio_l02"/self.LANGUAGE
    def text(self,key,size=FS_BODY,color=INK):
        m=Text(self.screen[key],font_size=size,color=color)
        if m.width>11.8: m.scale_to_fit_width(11.8)
        return m
    def audio_duration(self,i):
        with av.open(str(self.audio_dir/f"{i:02d}.mp3")) as c: return float(c.duration/av.time_base)
    def speak(self,i,*anims,animation_time=1.2):
        d=self.audio_duration(i); self.add_sound(str(self.audio_dir/f"{i:02d}.mp3"))
        if anims:
            r=min(animation_time,d); self.play(*anims,run_time=r,rate_func=linear); remain=d-r
        else: remain=d
        if remain: self.play(self.clock.animate.increment_value(1),run_time=remain,rate_func=linear)
    def construct(self):
        A=LEFT*5+DOWN*1.2; B=RIGHT*5+UP*1.0
        start=Dot(A,color=ACCENT_A); end=Dot(B,color=ACCENT_B)
        guide=Line(A,B,color=GHOST,stroke_width=2)
        question=self.text("question",FS_H1,ACCENT_A).to_edge(UP,buff=.45)
        self.add(start,end); self.speak(0,Write(question),Create(guide))
        paths=VGroup(
            Line(A,B,color=DIM,stroke_width=2),
            Arc(radius=3.0,start_angle=0.55,angle=2.2,arc_center=ORIGIN,color=ACCENT_C,stroke_width=2).scale(.95),
            Arc(radius=2.6,start_angle=-1.0,angle=3.4,arc_center=LEFT*1.2+DOWN*.2,color=WARN,stroke_width=2).scale(1.1),
        )
        many=self.text("paths",FS_BODY,DIM).to_edge(DOWN,buff=.5)
        self.speak(1,FadeOut(VGroup(guide, question)),FadeIn(paths),Write(many))
        chosen=paths[1].copy().set_color(ACCENT_A).set_stroke(width=5)
        chosen_label=self.text("chosen",FS_BODY,ACCENT_A).to_edge(DOWN,buff=.5)
        self.speak(2,FadeOut(paths),Create(chosen),FadeOut(many),Write(chosen_label))
        lag=self.text("lag",FS_H1,ACCENT_B).to_edge(UP,buff=.5)
        kinetic=Text("T",font_size=54,color=ACCENT_A).shift(LEFT*1.4+DOWN*.6)
        minus=Text("−",font_size=48,color=DIM).shift(DOWN*.6)
        potential=Text("U",font_size=54,color=ACCENT_C).shift(RIGHT*1.4+DOWN*.6)
        self.speak(3,FadeOut(chosen_label),Write(lag),FadeIn(kinetic),FadeIn(minus),FadeIn(potential))
        action=self.text("action",FS_H1,ACCENT_A).to_edge(UP,buff=.5)
        timeline=Line(LEFT*3+DOWN*1.9,RIGHT*3+DOWN*1.9,color=GHOST)
        dots=VGroup(*[Dot(LEFT*3+RIGHT*i*1.0+DOWN*1.9,radius=.1,color=ACCENT_B) for i in range(7)])
        self.speak(4,FadeOut(VGroup(lag,kinetic,minus,potential)),Write(action),Create(timeline),FadeIn(dots))
        stationary=self.text("stationary",FS_H1,WARN).to_edge(DOWN,buff=.55)
        wiggle=chosen.copy().set_color(WARN).set_stroke(width=3).shift(UP*.35)
        self.speak(5,FadeOut(action),FadeOut(dots),Create(wiggle),Write(stationary))
        equation=Text("d/dt (∂L/∂q̇) − ∂L/∂q = 0",font_size=35,color=ACCENT_B).move_to(ORIGIN)
        self.speak(6,FadeOut(stationary),Write(equation))
        ending=self.text("ending",FS_H1,INK).to_edge(DOWN,buff=.55)
        self.speak(7,FadeOut(equation),FadeOut(wiggle),Create(chosen),Write(ending))
        self.wait(.8)

class LandauL02ActionZH(ActionStoryBase): LANGUAGE="zh-TW"
class LandauL02ActionEN(ActionStoryBase): LANGUAGE="en"
