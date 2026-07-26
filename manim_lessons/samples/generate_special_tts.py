import argparse,asyncio,pathlib,sys,edge_tts
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]))
from manim_lessons.localization.special_topics import TOPICS_SPECIAL
VOICES={"zh":"zh-TW-HsiaoChenNeural","en":"en-US-AndrewNeural"}
RATES={"zh":"-4%","en":"-8%"}   # English is slowed a little more to match the Chinese pacing
async def run(n,lang,out):
 out.mkdir(parents=True,exist_ok=True)
 for i,s in enumerate(TOPICS_SPECIAL[n][lang][1]):
  for attempt in range(5):
   try:
    await edge_tts.Communicate(s,VOICES[lang],rate=RATES[lang]).save(str(out/f"{i:02d}.mp3")); break
   except Exception: await asyncio.sleep(3)
  else: raise SystemExit(f"TTS failed on beat {i}")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("episode",type=int);p.add_argument("language",choices=["zh","en"]);p.add_argument("output",type=pathlib.Path);a=p.parse_args();asyncio.run(run(a.episode,a.language,a.output))
