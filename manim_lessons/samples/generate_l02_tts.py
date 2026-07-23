import argparse, asyncio, pathlib, sys
import edge_tts
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim_lessons.localization.landau_l02_action import LOCALES

async def main(lang, out):
    out.mkdir(parents=True, exist_ok=True)
    for i, sentence in enumerate(LOCALES[lang]["narration"]):
        await edge_tts.Communicate(sentence, LOCALES[lang]["voice"], rate="-4%").save(str(out / f"{i:02d}.mp3"))

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("language", choices=LOCALES); p.add_argument("output", type=pathlib.Path); a=p.parse_args(); asyncio.run(main(a.language,a.output))
