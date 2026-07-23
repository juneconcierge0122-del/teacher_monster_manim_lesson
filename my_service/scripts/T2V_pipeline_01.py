"""
VideoGenerationPipeline Module - New Architecture

This module implements the new pipeline:
1. Content Generator (Gemini API) → transcript + manim code
2. Manim Renderer → video segments (flash-without-dub)
3. edge-tts API → audio + SRT subtitles
4. MoviePy → composite final video

Folder Structure:
  tmp/
    transcript/    → scenes.json, transcripts.json
    manim/
      scripts/    → scene_1.py, scene_2.py, ...
      flash-without-dub/ → 1.mp4, 2.mp4, ...
    audio/        → 1.mp3, 2.mp3, ...
    subtitle/     → 1.srt, 2.srt, ...
    final/        → final_video.mp4
  output/
    final_video.mp4
"""

import argparse
import os
import shutil
from typing import List

import yaml
from PIL import Image
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
)
import json

from src import AppConfig, GeminiClient
from src.content_generator import ContentGenerator
from src.manim_renderer import ManimRenderer
from src.tts.tts import TTSModule

from src.opus_lesson_writer import generate_lesson
import subprocess, os, uuid, re


import re

# Patterns that crash Manim's align_points mid-render. The LLM keeps reaching
# for these because they read naturally, but they rebuild a Tex/MathTex every
# frame and `align_points` blows up with IndexError as soon as the string
# structure changes (sign flip, decimal width, leading zero). Symptom: render
# dies around the frame where a tracked value crosses zero or changes magnitude.
# Fix: DecimalNumber + add_updater for the numeric part, static MathTex for the label.
_UNSAFE_REDRAW_TEX = re.compile(
    r"""always_redraw \s* \( \s*           # always_redraw(
        lambda \b [^:)]* : \s*             # lambda ...:
        (?: MathTex | Tex ) \s* \( \s*     # MathTex( or Tex(
        (?: r? f | f r? ) ["']             # f-string (any of: f"  f'  rf"  fr"  ...)
    """,
    re.VERBOSE | re.DOTALL,
)

# Same problem, slightly different shape: a `def` that returns a fresh MathTex
# and is then fed into always_redraw. Catches both `always_redraw(make_label)`
# and the `add_updater(lambda m: m.become(MathTex(f"...")))` variant.
_UNSAFE_BECOME_TEX = re.compile(
    r"""\. become \s* \( \s*
        (?: MathTex | Tex ) \s* \( \s*
        (?: r? f | f r? ) ["']
    """,
    re.VERBOSE | re.DOTALL,
)

_BANNED_BECOME_TEXT = re.compile(
    r"""\. become \s* \( \s*
        (?: [^)]*? \b )?                   # optional VGroup/wrapping nesting
        (?: MathTex | Tex | Text | MarkupText |
            Title | DecimalNumber | Integer | Variable )
        \s* \(
    """,
    re.VERBOSE | re.DOTALL,
)

_BANNED_VARIABLE_CLASS = re.compile(r"\bVariable\s*\(")

BANNED_SELF_METHODS = re.compile(
    r"\bself\.(show_comparison_rows|show_table|render_table|"
    r"comparison_table|build_rows|show_rows|display_comparison|"
    r"show_comparison|build_table|make_table|draw_table)\s*\("
)

_ALWAYS_REDRAW_CALL = re.compile(r"\balways_redraw\s*\(")

def sanitize_lesson_code(py_path: str):
    """攔截 Opus 已知會犯的 Manim 錯誤。"""
    text = open(py_path, encoding="utf-8").read()

    # 1. VGroup 接受非 VMobject → 改 Group
    text = text.replace("VGroup(*self.mobjects)", "Group(*self.mobjects)")

    # 2. Persona 亂傳 kwargs (上次的 bug)
    text = re.sub(r",\s*jargon_budget\s*=\s*\d+", "", text)
    text = re.sub(r",\s*speech_chars_per_min\s*=\s*\d+", "", text)

    # 3. 確保 Group 有 import (若用到)
    if "Group(" in text and "Group" not in text.split("from manim import")[1].split("\n")[0]:
        text = text.replace("from manim import (", "from manim import (\n    Group,", 1)

    # 4. 偵測 always_redraw(lambda: MathTex(f"...")) — 會在 zero crossing 時炸 align_points
    #    (見 03_triangle_centers / unit_circle S03 的 IndexError)
    bad_redraw = _UNSAFE_REDRAW_TEX.findall(text)
    bad_become = _UNSAFE_BECOME_TEX.findall(text)
    if bad_redraw or bad_become:
        raise ValueError(
            f"UNSAFE_DYNAMIC_TEX in {py_path}: "
            f"found {len(bad_redraw)} always_redraw+f-Tex and {len(bad_become)} become+f-Tex pattern(s). "
            f"These crash Manim's align_points mid-animation when the string structure changes "
            f"(sign flip, decimal width). Use DecimalNumber + add_updater for the numeric part, "
            f"paired with a static MathTex label in a VGroup. "
            f"Example:\n"
            f"  x_num = DecimalNumber(0, num_decimal_places=2, include_sign=True)\n"
            f"  x_num.add_updater(lambda m: m.set_value(np.cos(theta.get_value())))\n"
            f"  readout = VGroup(MathTex(r'x = '), x_num).arrange(RIGHT)"
        )

    # 5. 確保 DecimalNumber 有 import (若用到)
    if "DecimalNumber(" in text:
        first_import_line = text.split("from manim import")[1].split("\n")[0]
        if "DecimalNumber" not in first_import_line:
            text = text.replace("from manim import (", "from manim import (\n    DecimalNumber,", 1)

    hits = _ALWAYS_REDRAW_CALL.findall(text)
    if hits:
        raise ValueError(
            f"BANNED_PATTERN in {py_path}: found {len(hits)} always_redraw() "
            f"call(s). always_redraw is forbidden because it triggers "
            f"IndexError in align_points when rebuilt mobjects have varying "
            f"subpath counts (any text content that changes string structure). "
            f"Use add_updater + become for geometric shapes, "
            f"or DecimalNumber.add_updater(set_value) for numeric readouts."
        )

    # 6. ← 新增：幻覺 helper methods
    bad_methods = BANNED_SELF_METHODS.findall(text)
    if bad_methods:
        raise ValueError(
            f"HALLUCINATED_METHOD in {py_path}: {set(bad_methods)}. "
            f"These methods do not exist on any archetype. "
            f"Build comparison tables manually with VGroup+Text."
        )

    # 7. DecimalNumber import
    if "DecimalNumber(" in text:
        first_import_line = text.split("from manim import")[1].split("\n")[0]
        if "DecimalNumber" not in first_import_line:
            text = text.replace("from manim import (", "from manim import (\n    DecimalNumber,", 1)

    open(py_path, "w", encoding="utf-8").write(text)

import ast, importlib.util

def validate_lesson(py_path: str):
    text = open(py_path, encoding="utf-8").read()
    # 語法
    try:
        ast.parse(text)
    except SyntaxError as e:
        raise RuntimeError(f"Lesson has syntax error: {e}")
    # Import 可解析 (不真的執行)
    spec = importlib.util.spec_from_file_location("lesson_check", py_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        raise RuntimeError(f"Lesson import failed: {type(e).__name__}: {e}")


class VideoGenerationPipeline:
    """
    End-to-end pipeline with built-in renderer.
    """

    def __init__(
        self,
        llm_client,
        app_config: AppConfig,
        output_video_name: str = "final_video.mp4",
        final_video_dir: str = "./output",
        tmp_dir: str = "./tmp",
    ):
        self.app_config = app_config
        self.llm_client = llm_client
        self.tmp_dir = tmp_dir
        self.final_video_dir = final_video_dir
        self.video_output_name = output_video_name

        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(final_video_dir, exist_ok=True)

        self.fps = 15

        self.content_generator = ContentGenerator(llm_client, output_root=tmp_dir)
        self.manim_renderer = ManimRenderer(
            output_root=os.path.join(tmp_dir, "manim", "flash-without-dub")
        )
        self.tts_module = TTSModule(output_root=tmp_dir)

    def load(self):
        """Initialize heavy resources."""
        self.content_generator.load()
        self.manim_renderer.load()
        self.tts_module.load()

    def run(
        self,
        requirement_prompt: str,
        persona_prompt: str,
    ) -> dict:
        """
        Orchestrates the full generation process from text to MP4.
        """
        # =============================
        #  Step 1 + 2: Opus 寫 lesson + 渲染 per-scene
        # =============================
        import uuid
        job = uuid.uuid4().hex[:8]
        job_tmp = os.path.join(self.tmp_dir, "jobs", job)
        
        #job_dir = os.path.join(self.tmp_dir, "lessons", os.urandom(4).hex())
        #os.makedirs(job_dir, exist_ok=True)

        MAX_RETRIES = 2
        for attempt in range(MAX_RETRIES + 1):
            py_path, md_path = generate_lesson(
                course_req=requirement_prompt,
                persona=persona_prompt,
                output_dir=os.path.join(job_tmp, "lessons"),
            )
            try:
                sanitize_lesson_code(py_path)
                validate_lesson(py_path)
                subprocess.run(
                    ["manim", "-ql", py_path, "S01_Hook", "--media_dir", "/tmp/probe"],
                    check=True, capture_output=True, timeout=120,
                )
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    raise
                print(f"⚠ Attempt {attempt+1} failed: {e}. Regenerating...")


        # 1a. 解析 scene class 順序
        py_text = open(py_path, encoding="utf-8").read()
        scene_names = re.findall(r"^class\s+(S\d{2}_\w+)\s*\(", py_text, re.MULTILINE)

        # 1b. 解析旁白 (script.md 用 "## Scene N" 分段, "> " 開頭是旁白)
        md_text = open(md_path, encoding="utf-8").read()
        blocks = re.split(r"^##\s+Scene\s+\d+", md_text, flags=re.MULTILINE)[1:]
        transcripts = []
        for b in blocks:
            narration = " ".join(
                l.lstrip("> ").strip()
                for l in b.split("\n")
                if l.lstrip().startswith(">")
            )
            transcripts.append(narration)

        assert len(scene_names) == len(transcripts), \
            f"Scene 數對不上: {len(scene_names)} classes vs {len(transcripts)} narrations"

        # 1c. 個別渲染每個 scene class
        #manim_folder = os.path.join(self.tmp_dir, "manim", "flash-without-dub")
        manim_folder = os.path.join(job_tmp, "manim", "flash-without-dub")
        os.makedirs(manim_folder, exist_ok=True)
        #raw_media = os.path.join(self.tmp_dir, "manim_raw")
        raw_media = os.path.join(job_tmp, "manim_raw")

        video_paths = []
        for idx, scene_name in enumerate(scene_names, start=1):
            subprocess.run(
                ["manim", "-qm", py_path, scene_name, "--media_dir", raw_media],
                check=True,
            )
            # manim 通常輸出到 <raw_media>/videos/<py_stem>/<quality>/<scene>.mp4
            src = None
            for root, _, files in os.walk(raw_media):
                if f"{scene_name}.mp4" in files:
                    src = os.path.join(root, f"{scene_name}.mp4")
                    break
            if src is None:
                raise FileNotFoundError(f"找不到 {scene_name}.mp4 (在 {raw_media})")

            dst = os.path.join(manim_folder, f"{idx}.mp4")
            shutil.copy(src, dst)
            video_paths.append(dst)

        scenes_struct = [{"description": s} for s in scene_names]

        # =============================
        # Step 3: TTS Generation (edge-tts)
        # =============================
        audio_dir, subtitle_dir, word_timings = self.tts_module.run(transcripts)

        audio_paths = [
            os.path.join(audio_dir, f"{i}.mp3") for i in range(1, len(transcripts) + 1)
        ]

        # =============================
        # Step 4: Video Compositing
        # =============================
        #final_dir = os.path.join(self.tmp_dir, "final")
        final_dir = os.path.join(job_tmp, "final")
        os.makedirs(final_dir, exist_ok=True)

        video_clips = []

        for slide_idx in range(len(video_paths)):
            vid_path = video_paths[slide_idx]
            audio_path = audio_paths[slide_idx]

            if not os.path.exists(audio_path):
                print(f"Warning: Audio not found for scene {slide_idx + 1}")
                continue

            audio_clip = AudioFileClip(audio_path).set_fps(44100)
            slide_duration = audio_clip.duration

            if vid_path.endswith(".mp4"):
                base_clip = VideoFileClip(vid_path).set_duration(slide_duration)
            else:
                from moviepy.editor import ImageClip
                base_clip = ImageClip(vid_path).set_duration(slide_duration)

            video_clips.append(base_clip.set_audio(audio_clip))

        if not video_clips:
            raise ValueError("No video clips to composite")

        final_video = concatenate_videoclips(video_clips, method="compose")
        final_output_path = os.path.join(final_dir, self.video_output_name)
        final_video.write_videofile(
            final_output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
        )

        final_video.close()
        for clip in video_clips:
            clip.close()
            if hasattr(clip, "audio") and clip.audio:
                clip.audio.close()

        # =============================
        # Step 5: Copy to output folder
        # =============================
        output_path = os.path.join(self.final_video_dir, self.video_output_name)
        shutil.copy(final_output_path, output_path)

        return {
            "scenes": scenes_struct,
            "transcripts": transcripts,
            "manim_folder": manim_folder,
            "audio_folder": audio_dir,
            "subtitle_folder": subtitle_dir,
            "word_timings": word_timings,
            "final_video_path": output_path,
        }

    def _create_placeholder_image(self, idx: int, description: str) -> str:
        """Create a placeholder image when Manim rendering fails."""
        manim_folder = self.manim_renderer.output_root
        from PIL import Image, ImageDraw, ImageFont

        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#1a1a2e")
        draw = ImageDraw.Draw(img)

        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        draw.text((width // 2 - 100, height // 2 - 50), f"Scene {idx}", fill="white", font=font_title)

        desc_text = (description[:50] + "...") if len(description) > 50 else description
        draw.text((width // 2 - 200, height // 2 + 20), desc_text, fill="#888888", font=font_text)

        placeholder_path = os.path.join(manim_folder, f"{idx}.png")
        img.save(placeholder_path)
        return placeholder_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pipeline with prompts and video path"
    )

    parser.add_argument(
        "-r",
        "--requirement-prompt",
        type=str,
        default="Explain machine learning basics",
        help="Main requirement prompt",
    )

    parser.add_argument(
        "-p",
        "--persona-prompt",
        type=str,
        default="Friendly instructor",
        help="Persona prompt",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config/default.yaml",
        help="Generation config",
    )

    parser.add_argument(
        "-o",
        "--output-video-name",
        type=str,
        default="final_video.mp4",
        help="Output video file name",
    )

    parser.add_argument(
        "-d",
        "--final-video-dir",
        type=str,
        default=None,
        help="Directory for final video output",
    )

    args = parser.parse_args()

    print("\n=== Input ===")
    print(f"Requirement prompt: {args.requirement_prompt}")
    print(f"Persona prompt: {args.persona_prompt}")

    print("\n=== Loading ===")
    with open(args.config, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        config = AppConfig(**data)

    client = GeminiClient(config.llm)

    pipeline = VideoGenerationPipeline(
        llm_client=client,
        app_config=config,
        output_video_name=args.output_video_name,
        final_video_dir=args.final_video_dir or config.output.final_video_dir,
    )

    pipeline.load()

    print("\n=== Run ===")
    assets = pipeline.run(
        requirement_prompt=args.requirement_prompt,
        persona_prompt=args.persona_prompt,
    )

    print("\n=== Final Output ===")
    print("Final video:", assets["final_video_path"])
