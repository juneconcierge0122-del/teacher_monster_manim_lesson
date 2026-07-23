# Landau audiovisual samples

The samples are approval gates, not completed lessons. Both languages share
the scene class in `lessons/landau_l01_sample.py`; localized copy lives in
`localization/landau_l01_sample.py`.

Expected outputs:

- `output/landau_l01_sample_zh-TW.mp4`
- `output/landau_l01_sample_en.mp4`

Render the silent animation at low quality:

```bash
manim -ql lessons/landau_l01_sample.py LandauL01SampleZH
manim -ql lessons/landau_l01_sample.py LandauL01SampleEN
```

The final sample build adds Edge TTS narration and muxes it with ffmpeg.

## Version 2 approval samples

Version 2 is story-driven, contains no subtitle track or bottom captions, and
uses eight independent narration clips per language. Each animation beat reads
the real duration of its own audio clip before rendering.

- `output/landau_l01_story_v2_zh-TW.mp4`
- `output/landau_l01_story_v2_en.mp4`
- Scene: `lessons/landau_l01_sample_v2.py`
- Copy and narration: `localization/landau_l01_sample_v2.py`
- Audio clips: `audio_v2/{zh-TW,en}/00.mp3` through `07.mp3`

