"""Pull probe frames, but refuse if the render is older than the scene file.

    python tools/freshframes.py advcalc 86 ZH /tmp/frames        # probe frames
    python tools/freshframes.py advcalc 86 ZH /tmp/frames --dur 6

Reading a stale frame has cost this project three separate rounds of wasted
review: once when a subagent kept editing its scene file after the probe had
been queued (three findings were against a superseded version, two of them
already fixed), and twice when frames were grabbed while a re-render was still
running. Every one of those looked exactly like a real defect.

The mistake is invisible by inspection -- a stale frame is a perfectly good PNG
of the wrong version -- so this compares the mp4's mtime against the scene
file's and refuses rather than hands back frames that cannot be trusted. It also
refuses while a render is still writing, since a half-written mp4 yields frames
from whatever part of the timeline happens to exist.

Exits nonzero on a stale or missing render, so it can gate a review the way
bounds and collide gate a render.

The scene file is not the only input. 2026-10-23 the E86 narration was fixed
and its audio regenerated at 01:43, but every one of the round's eight probe
renders predated that, so each frame carried a subtitle from the superseded
text -- and this script, which compared the mp4 against the scene file alone,
called all of them fresh. So the comparison is against everything the frame is
drawn from: the scene file, the series' localization module (the narration and
the subtitles come from there), and the shared lib.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def scene_file(series, n):
    hits = sorted(p for p in (ROOT / "lessons" / series).glob(f"*_e{int(n)}_*.py")
                  if not p.name.endswith("_script.md"))
    if len(hits) != 1:
        sys.exit(f"expected exactly one scene file for {series} e{n}, found {len(hits)}")
    return hits[0]


def sources(series, n):
    """Every file the rendered frame is drawn from, newest last."""
    srcs = [scene_file(series, n), ROOT / "localization" / f"{series}.py"]
    srcs += sorted((ROOT / "lib").glob("*.py"))
    return sorted((p for p in srcs if p.exists()), key=lambda p: p.stat().st_mtime)


def main(series, n, lang, out, dur="6.0", beats="11"):
    scene = scene_file(series, n)
    mp4 = ROOT / f"media/probe{int(n)}/videos/probe/480p10/Probe{lang.upper()}.mp4"
    if not mp4.exists():
        sys.exit(f"no probe render at {mp4} -- render it before grabbing frames")
    newest = sources(series, n)[-1]
    sm, vm = newest.stat().st_mtime, mp4.stat().st_mtime
    if vm < sm:
        sys.exit(f"STALE: {mp4.name} was written {sm - vm:.0f}s before "
                 f"{newest.name} was last edited.\nRe-render the probe; these frames "
                 f"would show a superseded version.")
    # a render still in progress keeps touching the file; give it a moment to settle
    import time
    time.sleep(1.5)
    if mp4.stat().st_mtime != vm:
        sys.exit(f"STILL WRITING: {mp4.name} changed while being checked -- "
                 f"wait for the render to finish")
    print(f"fresh: {mp4.name} is {vm - sm:.0f}s newer than {newest.name}")
    subprocess.run([sys.executable, str(ROOT / "tools/grab.py"), str(mp4), out, dur, beats],
                   check=True)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit(__doc__.split("\n\n")[1].strip())
    main(*sys.argv[1:5], *sys.argv[5:])
