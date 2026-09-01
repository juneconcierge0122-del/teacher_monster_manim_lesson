"""Catch language leaking into the language-independent parts of an episode.

    python tools/langscan.py advcalc 44 45 46 47 48

FORMULAS_ADVCALC and the scenes' `_sym` rows are the two places that render
identically in both languages, so a word in either of them shows up in the wrong
language for half the audience.  It has happened three times: Chinese inside a
`_sym` proof line (E42), English inside FORMULAS (E47: `on M`, `injective`,
`open`), and English inside FORMULAS again (E50: `on M`).  Neither bounds.py nor
collide.py can see it, and it survives every probe frame in the language that
happens to match.

The whitelist is deliberately short: only symbols that are written with Latin
letters in both languages because they are operator names, not words.  Anything
else with two or more consecutive Latin letters is a hit, as is any CJK
character.  A real hit is fixed by moving the word into the scene's MODE_LABEL
or into a bilingual `_mid` row.

Exits nonzero if anything was found, so it can gate a render.
"""
import importlib
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

WHITELIST = {
    "Hom", "lub", "glb", "min", "max", "sup", "inf", "det", "lim", "dim",
    "rank", "Ch", "dF", "dG", "dH", "dK", "df", "dg", "dh", "dk", "id", "int",
    "sin", "cos", "tan", "log", "exp", "arg", "mod", "ev",
    # proper names, written in Latin letters in the Chinese narration too
    # ("Cauchy 序列", "Banach 空間"), so they are language-independent the way
    # an operator name is -- not words one half of the audience reads wrong.
    "Cauchy", "Banach", "Lipschitz", "Lebesgue", "Hausdorff",
}
WORD = re.compile(r"[A-Za-z]{2,}")
CJK = re.compile(r"[㐀-鿿　-〿＀-￯]")
# Both patterns keep the string body free of quotes and newlines on purpose: a
# lazy dot with DOTALL happily runs from one string to a colour name hundreds of
# lines below and reports the whole file as one hit.
SYM = re.compile(r"self\._sym\(\s*[^,\n]+,\s*f?(['\"])([^'\"\n]*)\1")
# ("...", ACCENT_B) rows, which is how _table and the `lines` blocks carry labels
ROW = re.compile(r"\(\s*f?(['\"])([^'\"\n]*)\1\s*,\s*(?:ACCENT_[ABC]|WARN|DIM|INK)\s*\)")
FIELD = re.compile(r"\{[^{}]*\}")


def hits(text):
    out = []
    if CJK.search(text):
        out.append("CJK")
    words = [w for w in WORD.findall(text) if w not in WHITELIST]
    if words:
        out.append("words " + ", ".join(sorted(set(words))))
    return out


def main(series, nums):
    mod = importlib.import_module(f"manim_lessons.localization.{series}")
    formulas = getattr(mod, f"FORMULAS_{series.upper()}")
    root = pathlib.Path(__file__).resolve().parents[1] / "lessons" / series
    bad = 0
    for n in nums:
        for i, line in sorted(formulas[int(n)].items()):
            for h in hits(line):
                print(f"{n} FORMULAS[{i}]  {h}\n     {line}")
                bad += 1
        for path in sorted(root.glob(f"advcalc_e{int(n)}_*.py")):
            if path.name.endswith("_script.md"):
                continue
            src = path.read_text()
            for tag, rx in (("_sym", SYM), ("row", ROW)):
                for m in rx.finditer(src):
                    # an f-string's replacement fields name Python variables, not
                    # anything that reaches the screen, so drop them first
                    text = FIELD.sub("", m.group(2))
                    for h in hits(text):
                        print(f"{n} {path.name} {tag}  {h}\n     {m.group(2)}")
                        bad += 1
    print(f"{series} {' '.join(str(n) for n in nums)}: {bad} language leaks")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
