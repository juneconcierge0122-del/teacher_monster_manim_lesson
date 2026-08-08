"""Pull one frame per beat from a finished episode, at the real beat boundaries.

    python tools/grabbeats.py advcalc 19 en /tmp/frames

tools/grab.py takes a single beat length and multiplies it, which is right for a
probe render (fixed-length beats, no audio) but wrong for a finished episode:
there each beat runs as long as its own narration line, so a uniform sample
drifts further out of step with every beat and the late frames land in the wrong
beat entirely. Here the boundaries are the cumulative mp3 durations, which is
what the scene itself times against.

Still sampling 0.6 s before each boundary, for the reason grab.py gives: -ss
seeks forward, so asking for the last moment of a beat lands on the next beat's
first frame, where the callable has run and every animation clock has just
reset. That reads exactly like a bug.

Frames are what catch the things a bounds check cannot: elements that are inside
the frame but crowding each other, a picture that reads as the wrong claim, and
a formula bar that disagrees with the diagram underneath it.
"""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import av

ROOT = pathlib.Path(__file__).resolve().parents[1]
FF = ("/home/r08849002/miniconda3/envs/teacher-monster/lib/python3.10/site-packages/"
      "imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")

series, n, lang, out = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
ap = {"advcalc": "e"}.get(series, "l")
src = ROOT / f"samples/output/{series}_{ap}{n}_{lang}.mp4"
out.mkdir(parents=True, exist_ok=True)

t = 0.0
for i, f in enumerate(sorted((ROOT / f"samples/audio_{ap}{n}/{lang}").glob("*.mp3"))):
    with av.open(str(f)) as c:
        t += float(c.duration / av.time_base)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t - 0.60:.3f}",
                    "-i", str(src), "-frames:v", "1",
                    str(out / f"{ap}{n}_{lang}_beat{i:02d}.png")], check=True)
print(f"{n} {lang}: {i + 1} frames -> {out}")
