"""Generate one independently verifiable audio clip per narration beat."""
import argparse
import asyncio
from pathlib import Path
import sys

import edge_tts

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from manim_lessons.localization.landau_l01_sample_v2 import LOCALES


async def generate(language: str, output: Path) -> None:
    locale = LOCALES[language]
    output.mkdir(parents=True, exist_ok=True)
    for index, sentence in enumerate(locale["narration"]):
        target = output / f"{index:02d}.mp3"
        communicator = edge_tts.Communicate(
            sentence, locale["voice"], rate="-4%"
        )
        await communicator.save(str(target))
        print(f"{language} {index:02d}: {target.name} | {sentence}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("language", choices=LOCALES)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    asyncio.run(generate(args.language, args.output))


if __name__ == "__main__":
    main()
