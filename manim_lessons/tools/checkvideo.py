"""Check rendered episodes before they go anywhere near YouTube.

    python tools/checkvideo.py advcalc 16 17 18 19 20

Four checks, because each catches something the other three cannot:

  coverage   the audio track actually reaches the end of the video. This is the
             one that matters. `Scene.add_sound` returns early when
             `skip_animations` is set, which is exactly what manim sets when it
             reuses a cached partial movie file, so re-rendering a lesson drops
             the narration for every beat that hits the cache. The result is a
             full-length video with a real AAC track that goes silent a few
             seconds in. Comparing the video's length against the narration's
             total length passes. Only the timestamp of the last audio frame
             sees it.
  ZH != EN   identical durations mean manim resolved neither scene name and
             rendered the base class twice.
  narration  the video is at least as long as its own narration.
  streams    1920x1080p60, h264 + aac, as uploaded.

Exits nonzero if anything failed, so it can gate an upload.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
import av

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "samples/output"


def probe(path):
    with av.open(str(path)) as c:
        vs = [s for s in c.streams if s.type == "video"][0]
        aus = [s for s in c.streams if s.type == "audio"]
        i = dict(dur=float(c.duration / av.time_base), w=vs.width, h=vs.height,
                 fps=float(vs.average_rate), vcodec=vs.codec_context.name,
                 acodec=aus[0].codec_context.name if aus else None)
        i["last"] = (max(float(fr.time or 0) for fr in c.decode(aus[0])) if aus else 0.0)
    i["cov"] = i["last"] / i["dur"] if i["dur"] else 0.0
    return i


def narration(series, n, lang):
    tot = 0.0
    for f in sorted((ROOT / f"samples/audio_{series}{n}/{lang}").glob("*.mp3")):
        with av.open(str(f)) as c:
            tot += float(c.duration / av.time_base)
    return tot


def main(prefix, audio_prefix, nums):
    bad = 0
    for n in nums:
        z = OUT / f"{prefix}_{audio_prefix}{n}_zh-TW.mp4"
        e = OUT / f"{prefix}_{audio_prefix}{n}_en.mp4"
        if not (z.exists() and e.exists()):
            print(f"{n}  MISSING {z.name if not z.exists() else ''} "
                  f"{e.name if not e.exists() else ''}")
            bad += 1
            continue
        iz, ie = probe(z), probe(e)
        for lang, i in (("zh-TW", iz), ("en", ie)):
            nar = narration(audio_prefix, n, lang)
            flags = []
            if i["cov"] < 0.95:
                flags.append(f"COVERAGE {i['cov']:.0%}")
            if (i["w"], i["h"], round(i["fps"])) != (1920, 1080, 60):
                flags.append(f"FORMAT {i['w']}x{i['h']}@{i['fps']:.0f}")
            if (i["vcodec"], i["acodec"]) != ("h264", "aac"):
                flags.append(f"CODEC {i['vcodec']}/{i['acodec']}")
            if i["dur"] < nar:
                flags.append(f"SHORTER THAN NARRATION {i['dur']:.0f}s < {nar:.0f}s")
            bad += len(flags)
            print(f"{n} {lang:5s} {i['dur']:6.1f}s  audio to {i['last']:6.1f}s "
                  f"({i['cov']:.0%})  narration {nar:5.1f}s  "
                  f"{i['w']}x{i['h']}@{i['fps']:.0f} {i['vcodec']}/{i['acodec']}"
                  f"  {'  '.join(flags) or 'ok'}")
        if abs(iz["dur"] - ie["dur"]) < 0.05:
            print(f"{n}  IDENTICAL DURATIONS -- the base class was rendered twice")
            bad += 1
    print(f"\n{f'FAIL: {bad} problems' if bad else 'all checks passed'}")
    return 1 if bad else 0


if __name__ == "__main__":
    series = sys.argv[1]
    sys.exit(main(series, {"advcalc": "e"}.get(series, "l"), sys.argv[2:]))
