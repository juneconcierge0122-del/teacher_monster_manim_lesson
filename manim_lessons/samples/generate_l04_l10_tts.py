import argparse,asyncio,pathlib,sys,edge_tts
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]))
from manim_lessons.localization.landau_l04_l10 import TOPICS
VOICES={"zh":"zh-TW-HsiaoChenNeural","en":"en-US-AndrewNeural"}
async def run(n,lang,out):
 out.mkdir(parents=True,exist_ok=True)
 for i,s in enumerate(TOPICS[n][lang][1]): await edge_tts.Communicate(s,VOICES[lang],rate="-4%").save(str(out/f"{i:02d}.mp3"))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("episode",type=int);p.add_argument("language",choices=["zh","en"]);p.add_argument("output",type=pathlib.Path);a=p.parse_args();asyncio.run(run(a.episode,a.language,a.output))
