"""Walk every mobject a lesson stages and report the ones outside the frame.

    python tools/bounds.py lessons/advcalc/advcalc_e20_dimension.py AdvCalcE20

The stage area sits between the heading and the subtitle, so the usable box is
narrower than the 16:9 frame: |x| <= 6.3, -1.90 <= y <= 1.30. Both language
scenes are built and checked, since the two lay out differently.

No renderer involved. `stage()` is evaluated once, up front, and builds every
mobject the lesson will ever show, so calling it places them all in about a
second -- cheap enough to run on every edit. The per-beat callables only flip
`self.mode`, which changes how updaters move things at play time, not where
they start.

This finds things that run off the edge. It cannot see elements that are inside
the frame but crowding each other, or a picture that draws the wrong claim --
for those, render and use tools/grabbeats.py.
"""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from manim import ValueTracker

XMAX, YTOP, YBOT = 6.3, 1.30, -1.90

path, scene = pathlib.Path(sys.argv[1]), sys.argv[2]
mod = importlib.import_module(
    "manim_lessons." + str(path.with_suffix("")).replace("/", "."))

bad = 0
for lang in ("ZH", "EN"):
    sc = getattr(mod, f"{scene}{lang}")()
    sc.t, sc.t0 = ValueTracker(0.0), 0.0
    for i, entry in enumerate(sc.stage()):
        for m in entry[0]:
            for k in m.get_family():
                if not k.get_num_points():
                    continue
                x0, x1 = k.get_left()[0], k.get_right()[0]
                y0, y1 = k.get_bottom()[1], k.get_top()[1]
                off = []
                if min(x0, -x1) < -XMAX:
                    off.append(f"x [{x0:+.2f},{x1:+.2f}]")
                if y1 > YTOP:
                    off.append(f"top {y1:+.2f}")
                if y0 < YBOT:
                    off.append(f"bot {y0:+.2f}")
                if off:
                    bad += 1
                    print(f"  {scene}{lang} beat {i:2d} "
                          f"{type(k).__name__:<12} {'  '.join(off)}")
print(f"{scene}: {bad} out of frame")
sys.exit(1 if bad else 0)
