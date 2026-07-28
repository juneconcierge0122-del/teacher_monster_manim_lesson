"""Fast layout harness: fixed beat length, no audio.

A whole lesson renders in well under a minute at -ql, so every one of the ten
beats can be sampled as a frame and checked for collisions before committing to
a -qh render (20-25 minutes per video). Run it from `manim_lessons/`:

    PROBE_MOD=manim_lessons.lessons.landau_l49_adiabatic \
    PROBE_CLS=AdiabaticBase PROBE_DUR=6 \
    manim -ql --fps 10 tools/probe.py ProbeEN

then pull one frame per beat with tools/grab.py. Raise PROBE_DUR when the point
of the check is a slow animation (a ramp, a curve filling in) rather than the
static composition.
"""
import importlib, os, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

_mod = importlib.import_module(os.environ["PROBE_MOD"])
_Base = getattr(_mod, os.environ["PROBE_CLS"])
_D = float(os.environ.get("PROBE_DUR", "1.2"))


class _P(_Base):
 def dur(self, i): return _D
 def add_sound(self, *a, **k): pass


ProbeZH = type("ProbeZH", (_P,), {"__module__": __name__, "LANGUAGE": "zh"})
ProbeEN = type("ProbeEN", (_P,), {"__module__": __name__, "LANGUAGE": "en"})
