"""Shared story animation for Landau episodes 04–10."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import av, numpy as np
from manim import Axes, Create, Dot, FadeIn, FadeOut, Line, Scene, Text, UP, DOWN, LEFT, RIGHT, VGroup, Write, ValueTracker, linear
from manim_lessons.lib.design_tokens import ACCENT_A, ACCENT_B, ACCENT_C, DIM, FS_BODY, FS_H1, GHOST, INK, apply_global_config
from manim_lessons.localization.landau_l04_l10 import TOPICS
class LandauBatchBase(Scene):
 EPISODE=4; LANGUAGE="zh"
 def setup(self):
  apply_global_config(); self.title,self.lines=TOPICS[self.EPISODE][self.LANGUAGE]; self.clock=ValueTracker(0); self.audio_dir=pathlib.Path(__file__).resolve().parents[1]/"samples"/f"audio_l{self.EPISODE:02d}"/("zh-TW" if self.LANGUAGE=="zh" else "en")
 def text(self,s,size=FS_BODY,color=INK):
  m=Text(s,font_size=size,color=color)
  if m.width>11.8:m.scale_to_fit_width(11.8)
  return m
 def dur(self,i):
  with av.open(str(self.audio_dir/f"{i:02d}.mp3")) as c:return float(c.duration/av.time_base)
 def speak(self,i,*an):
  d=self.dur(i);self.add_sound(str(self.audio_dir/f"{i:02d}.mp3"));r=min(1.2,d)
  if an:self.play(*an,run_time=r,rate_func=linear);d-=r
  if d:self.play(self.clock.animate.increment_value(1),run_time=d,rate_func=linear)
 def construct(self):
  heading=self.text(self.title,FS_H1,ACCENT_A).to_edge(UP,buff=.45)
  axes=Axes(x_range=[-5,5,1],y_range=[-2,3,1],x_length=9,y_length=4,axis_config={"color":GHOST,"stroke_width":2})
  dot=Dot(axes.c2p(-3,0),color=ACCENT_A,radius=.18); trail=Line(axes.c2p(-3,0),axes.c2p(3,0),color=ACCENT_B,stroke_width=3)
  self.add(axes,dot)
  for i,line in enumerate(self.lines):
   card=self.text(line,FS_BODY,INK).to_edge(DOWN,buff=.5)
   if i==0:self.speak(i,Write(heading),FadeIn(dot))
   elif i==1:self.speak(i,Create(trail),Write(card))
   elif i==2:self.speak(i,FadeOut(card),dot.animate.move_to(axes.c2p(0,1.8)),Write(card))
   elif i==3:self.speak(i,FadeOut(card),Write(card))
   if i<3:self.remove(card)
  self.wait(.8)
def make_scene(n,lang): return type(f"LandauL{n:02d}{'ZH' if lang=='zh' else 'EN'}",(LandauBatchBase,),{"EPISODE":n,"LANGUAGE":lang})
for _n in range(4,11):
 globals()[f"LandauL{_n:02d}ZH"]=make_scene(_n,"zh"); globals()[f"LandauL{_n:02d}EN"]=make_scene(_n,"en")
