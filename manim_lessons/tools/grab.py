"""Pull one frame near the end of each beat out of a probe render.

    python tools/grab.py media/videos/probe/480p10/ProbeEN.mp4 /tmp/frames 6.0

The sample sits 0.6 s before the beat boundary on purpose: `-ss` seeks to the
first frame at or after the given time, so asking for the last moment of a beat
lands on the *next* beat's opening frame -- where the callable has already run
and every animation clock has just reset. That reads exactly like a bug.
"""
import pathlib, subprocess, sys

FF = ("/home/r08849002/miniconda3/envs/teacher-monster/lib/python3.10/site-packages/"
      "imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")

src, out, dur = sys.argv[1], pathlib.Path(sys.argv[2]), float(sys.argv[3])
n = int(sys.argv[4]) if len(sys.argv) > 4 else 10
out.mkdir(parents=True, exist_ok=True)
for i in range(n):
 subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{dur * i + dur - 0.60:.3f}",
                 "-i", src, "-frames:v", "1", str(out / f"beat{i}.png")], check=True)
print("wrote", n, "frames to", out)
