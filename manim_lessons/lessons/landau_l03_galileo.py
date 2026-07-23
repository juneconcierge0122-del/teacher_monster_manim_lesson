import pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]))
import av,numpy as np
from manim import Arrow,Create,DashedLine,Dot,FadeIn,FadeOut,Line,Rectangle,Scene,Text,UP,DOWN,LEFT,RIGHT,VGroup,Write,ValueTracker,linear
from manim_lessons.lib.design_tokens import ACCENT_A,ACCENT_B,ACCENT_C,DIM,FS_BODY,FS_H1,GHOST,INK,WARN,apply_global_config
from manim_lessons.localization.landau_l03_galileo import LOCALES
class GalileoBase(Scene):
 LANGUAGE="zh-TW"
 def setup(self):
  apply_global_config();self.data=LOCALES[self.LANGUAGE];self.s=self.data["screen"];self.clock=ValueTracker(0);self.audio_dir=pathlib.Path(__file__).resolve().parents[1]/"samples"/"audio_l03"/self.LANGUAGE
 def text(self,k,size=FS_BODY,color=INK):
  m=Text(self.s[k],font_size=size,color=color)
  if m.width>11.8:m.scale_to_fit_width(11.8)
  return m
 def dur(self,i):
  with av.open(str(self.audio_dir/f"{i:02d}.mp3")) as c:return float(c.duration/av.time_base)
 def speak(self,i,*an,animation_time=1.2):
  d=self.dur(i);self.add_sound(str(self.audio_dir/f"{i:02d}.mp3"));r=min(d,animation_time)
  if an:self.play(*an,run_time=r,rate_func=linear);d-=r
  if d:self.play(self.clock.animate.increment_value(1),run_time=d,rate_func=linear)
 def construct(self):
  ground=Line(LEFT*6+DOWN*2.2,RIGHT*6+DOWN*2.2,color=GHOST); self.add(ground)
  ball=Dot(LEFT*3+DOWN*.4,color=ACCENT_A,radius=.18); passenger=Dot(LEFT*3+DOWN*.4,color=ACCENT_B,radius=.12)
  train=Rectangle(width=5.5,height=2.0,color=ACCENT_B).shift(RIGHT*1.2+DOWN*1.2); roof=Text("K′",font_size=28,color=ACCENT_B).move_to(train.get_top()+DOWN*.3)
  title=self.text("question",FS_H1,ACCENT_A).to_edge(UP,buff=.45)
  self.speak(0,Write(title),Create(ground),FadeIn(ball),FadeIn(passenger))
  path1=DashedLine(LEFT*3+DOWN*.4,LEFT*3+UP*1.7,color=ACCENT_B); path2=DashedLine(LEFT*3+DOWN*.4,RIGHT*1.0+UP*1.7,color=ACCENT_A)
  self.speak(1,Create(train),Write(roof),Create(path1),Create(path2))
  labels=VGroup(self.text("platform",FS_BODY,ACCENT_A).to_corner(UP+LEFT,buff=.4),self.text("train",FS_BODY,ACCENT_B).to_corner(UP+RIGHT,buff=.4))
  self.speak(2,FadeOut(title),Write(labels))
  pos=self.text("position",FS_H1,ACCENT_A).to_edge(DOWN,buff=.55); self.speak(3,Write(pos))
  time=self.text("time",FS_H1,ACCENT_B).to_edge(DOWN,buff=.55);self.speak(4,FadeOut(pos),Write(time))
  vel=self.text("velocity",FS_H1,ACCENT_C).to_edge(DOWN,buff=.55);v_arrow=Arrow(LEFT*2+DOWN*1.1,RIGHT*2+DOWN*1.1,color=ACCENT_C)
  self.speak(5,FadeOut(time),Write(vel),Create(v_arrow))
  acc=self.text("accel",FS_H1,WARN).to_edge(DOWN,buff=.55); self.speak(6,FadeOut(vel),FadeOut(v_arrow),Write(acc))
  end=self.text("ending",FS_H1,INK).to_edge(DOWN,buff=.55);self.speak(7,FadeOut(acc),Write(end));self.wait(.8)
class LandauL03GalileoZH(GalileoBase):LANGUAGE="zh-TW"
class LandauL03GalileoEN(GalileoBase):LANGUAGE="en"
