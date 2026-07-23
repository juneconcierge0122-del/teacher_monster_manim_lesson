"""Landau 04 — free-particle Lagrangian, story-first and caption-free."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import av, numpy as np
from manim import Axes, Create, Dot, FadeIn, FadeOut, Line, Scene, Text, UP, DOWN, LEFT, RIGHT, VGroup, ValueTracker, Write, linear, always_redraw
from manim_lessons.lib.design_tokens import ACCENT_A, ACCENT_B, ACCENT_C, DIM, FS_H1, GHOST, INK, apply_global_config
from manim_lessons.localization.landau_l04_l10 import TOPICS

class FreeParticleBase(Scene):
    LANGUAGE = "zh"
    def setup(self):
        apply_global_config(); self.title, self.narration = TOPICS[4][self.LANGUAGE]; self.clock=ValueTracker(0)
        lang = "zh-TW" if self.LANGUAGE == "zh" else "en"
        self.audio_dir = pathlib.Path(__file__).resolve().parents[1] / "samples" / "audio_l04" / lang
    def audio_duration(self, i):
        with av.open(str(self.audio_dir / f"{i:02d}.mp3")) as c: return float(c.duration / av.time_base)
    def formula(self, value, color=INK, size=48):
        m=Text(value,font_size=size,color=color)
        if m.width>11.8:m.scale_to_fit_width(11.8)
        return m
    def speak(self,i,*animations,hold=1.2,gap=2.0):
        duration=self.audio_duration(i); self.add_sound(str(self.audio_dir/f"{i:02d}.mp3"))
        if animations:
            reveal=min(hold,duration); self.play(*animations,run_time=reveal,rate_func=linear); duration-=reveal
        if duration:self.play(self.clock.animate.increment_value(1),run_time=duration,rate_func=linear)
        self.play(self.clock.animate.increment_value(1),run_time=gap,rate_func=linear)
    def construct(self):
        axes=Axes(x_range=[-5,5,1],y_range=[-2,2,1],x_length=10,y_length=3.2,axis_config={"color":GHOST,"stroke_width":2}).shift(DOWN*.4)
        title=self.formula(self.title,ACCENT_A,36).to_edge(UP,buff=.45)
        xdot=ValueTracker(-3.8)
        particle=always_redraw(lambda: Dot(axes.c2p(xdot.get_value(),0),color=ACCENT_A,radius=.2))
        trail=Line(axes.c2p(-4,0),axes.c2p(4,0),color=ACCENT_B,stroke_width=3)
        self.add(axes,particle)
        self.speak(0,Write(title),xdot.animate.set_value(3.8),hold=3.0)
        position=Text("x",font_size=34,color=ACCENT_C).next_to(axes.x_axis,RIGHT)
        self.speak(1,Create(trail),Write(position))
        symmetry=self.formula("L  不依賴  x  或方向",ACCENT_B,38) if self.LANGUAGE=="zh" else self.formula("L does not depend on position or direction",ACCENT_B,34)
        self.speak(2,FadeOut(position),Write(symmetry))
        location = self.formula("L  不依賴位置" if self.LANGUAGE=="zh" else "L ignores location", ACCENT_B, 38)
        self.speak(3,FadeOut(symmetry),Write(location))
        speed=self.formula("v²",ACCENT_C,56)
        self.speak(4,FadeOut(location),Write(speed))
        lag=self.formula("L = ½ m v²",ACCENT_A,58)
        mass=self.formula("m：質量",DIM,30) if self.LANGUAGE=="zh" else self.formula("m: mass",DIM,30)
        mass.next_to(lag,DOWN,buff=.35)
        self.speak(5,FadeOut(speed),Write(lag),Write(mass),hold=1.5)
        inertia=self.formula("自由粒子：慣性寫進 L",INK,38) if self.LANGUAGE=="zh" else self.formula("Free particle: inertia is built into L",INK,34)
        self.speak(6,FadeOut(VGroup(lag,mass)),Write(inertia))
        self.speak(7,FadeOut(inertia),xdot.animate.set_value(-3.8),hold=3.0)
        self.wait(.8)

class LandauL04FreeZH(FreeParticleBase): LANGUAGE="zh"
class LandauL04FreeEN(FreeParticleBase): LANGUAGE="en"
