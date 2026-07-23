import base64
import json
import re
from pathlib import Path
from typing import Optional

import anthropic
from pydantic import BaseModel

from src.config_schema import LLMConfig

import json
import base64

class SceneContent(BaseModel):
    transcript: str
    manim_code: str
    description: str


class ContentGenerationOutput(BaseModel):
    scenes: list[SceneContent]


class AnthropicClient:
    """
    Drop-in replacement for GeminiClient using Anthropic Claude.
    Matches GeminiClient's public interface exactly.
    """

    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.is_loaded = False

    def load(self):
        self.is_loaded = True

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        assert self.is_loaded, "Call load() first"

        response = self.client.messages.create(
            model=model or self.config.default_model,
            max_tokens=max_tokens or self.config.default_max_tokens or 8192,
            temperature=temperature if temperature is not None else self.config.default_temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def generate_with_image(
        self,
        prompt: str,
        image_path: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        assert self.is_loaded, "Call load() first"

        ext = Path(image_path).suffix.lower().lstrip(".")
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        response = self.client.messages.create(
            model=model or self.config.default_model,
            max_tokens=max_tokens or self.config.default_max_tokens or 8192,
            temperature=temperature if temperature is not None else self.config.default_temperature,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": image_data}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.content[0].text

    def generate_content(
        self,
        requirement_prompt: str,
        persona_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> ContentGenerationOutput:
        assert self.is_loaded, "Call load() first"

        user_prompt = f"""You are an expert instructional designer for a SPECIFIC student.

## Student Persona (READ CAREFULLY)
{persona_prompt}

## Topic Requirement
{requirement_prompt}

## HARD CONSTRAINTS — these are the most common failure modes, avoid them:

1. **Jargon discipline**: Before using ANY technical term that is NOT in the student's
   stated background knowledge, define it in ONE plain sentence. Example: instead of
   "use Ridge regression", say "use Ridge regression — a method that shrinks less
   important factors to keep the model simple — to avoid overfitting".

2. **No bare acronyms**: MSE, RMSE, AUC, p-value, etc. must be expanded and given
   intuition the FIRST time. e.g. "MSE (Mean Squared Error — basically the average
   of how wrong each prediction is, squared)".

3. **Concrete before abstract**: Whenever you introduce an evaluation metric or
   method, follow it with a tiny numeric example (3-4 numbers max). e.g. "If your
   predictions miss by 5, 10, 3, then RMSE ≈ 6.8 — small means accurate."

4. **One-thing-at-a-time**: Do not list multiple related techniques in one breath
   (e.g. "Ridge and Lasso and Elastic Net"). Pick ONE, explain it, move on.

5. **Persona alignment check**: After drafting, mentally verify each scene against
   the student's `Lacks` list. If a scene assumes knowledge they lack, rewrite it.

6. **Visual primitives, not text walls**: Manim has Circle, Line, Polygon, Arrow,
   Dot, NumberPlane, Axes, ImageMobject, Brace, etc. Use them. A scene that is
   80%+ Text() / Write(Text()) is a FAILURE — that's a slideshow, not animation.
   Every scene must contain at least ONE non-text visual element that illustrates
   the concept (a diagram, a graph, a shape transformation, a movement).

   Subject-specific guidance:
   - Math/Stats → Axes + plotted curves, geometric shapes, transformations
   - Biology → labeled diagrams (cells, organisms, anatomy via Polygon/Circle/Arrow)
   - Physics → vectors (Arrow), trajectories, free body diagrams
   - Geography/Spatial → maps via Polygon, Dots for locations
   - CS/Algo → boxes (Square) for data, Arrow for flow, animated rearrangement
   Text labels are fine ALONGSIDE these visuals, never INSTEAD of them.

7. **Specific, descriptive title**: When generating the first scene, use a
   concrete title that names the actual concept (e.g. "Speciation: How One
   Species Becomes Two", NOT "Evolution (1)" or "Biology Lesson"). Vague
   titles get penalized by reviewers.

8. **Manim Community 0.19 — CRITICAL API rule**:
   The single most common failure in this pipeline is passing `weight=` as a
   string. This crashes manimpango.str2weight and kills the entire scene render.

   FORBIDDEN (will crash):
       Text("Hi", weight="BOLD")
       Text("Hi", weight="bold")
       Text("Hi", weight="HEAVY")

   CORRECT options:
       Text("Hi", weight=BOLD)              # BOLD is a constant from `from manim import *`
       Text("Hi")                           # omit weight — default is fine
       MarkupText('<b>Hi</b>')              # use markup for bold

   Default rule: DO NOT pass weight= unless absolutely necessary. Plain Text()
   is the safe choice. If you must bold, use the BOLD constant, never a string.


9. **Terminology accuracy check**: For specialized terms (botany, anatomy,
   chemistry, etc.), verify before using. Common traps:
   - Plant stem bundles: "collateral" (xylem & phloem side-by-side), NOT
     "radial" (which is roots) or "concentric" (which is rare cases).
   - When unsure between two technical terms, use the more general/safer one
     or describe the structure in plain language instead of guessing the term.

## Manim & Transcript Guidelines
- Manim: from manim import *, Scene subclass, self-contained, English text only
- Transcript: English, 2-4 sentences per scene, conversational
"""

        tool = {
            "name": "submit_scenes",
            #"description": "Submit the generated scenes for the teaching video.",
            "description": "Submit the generated scenes. CRITICAL: the 'scenes' parameter MUST be a JSON array (list of objects), NOT a string. Do not wrap the array in quotes. Pass it as a native array.", 
            "input_schema": {
                "type": "object",
                "properties": {
                    "scenes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "transcript": {"type": "string"},
                                "manim_code": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["transcript", "manim_code", "description"],
                        },
                    }
                },
                "required": ["scenes"],
            },
        }

        #response = self.client.messages.create(
        #    model=model or self.config.default_model,
        #    max_tokens=max_tokens or self.config.default_max_tokens or 8192,
         #   temperature=temperature if temperature is not None else self.config.default_temperature,
        #    tools=[tool],
        #    tool_choice={"type": "tool", "name": "submit_scenes"},
        #    messages=[{"role": "user", "content": user_prompt}],
        #)

        with self.client.messages.stream(
            model=model or self.config.default_model,
            max_tokens=max_tokens or self.config.default_max_tokens or 8192,
            temperature=temperature if temperature is not None else self.config.default_temperature,
            tools=[tool],
            tool_choice={"type": "tool", "name": "submit_scenes"},
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            response = stream.get_final_message()

        #for block in response.content:
        #    if block.type == "tool_use" and block.name == "submit_scenes":
        #        return ContentGenerationOutput(**block.input)
        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_scenes":
                if not block.input or "scenes" not in block.input:
                    raise ValueError(
                        f"Empty tool input. stop_reason={response.stop_reason}, "
                        f"input={block.input}"
                    )

                #scenes = block.input["scenes"]
                #if isinstance(scenes, str):
                #    scenes = json.loads(scenes)
                #    block.input["scenes"] = scenes


                scenes = block.input["scenes"]
                if isinstance(scenes, str):
                    try:
                        scenes = json.loads(scenes)
                    except json.JSONDecodeError:
                        # 模型把 array 序列化時搞壞了，常見是用單引號或漏跳脫
                        # 試試 ast.literal_eval（吃 Python literal,容忍單引號）
                        import ast
                        try:
                            scenes = ast.literal_eval(scenes)
                        except (ValueError, SyntaxError) as e:
                            raise ValueError(
                                f"Could not parse scenes string. "
                                f"First 500 chars: {scenes[:500]!r}"
                            ) from e
                    block.input["scenes"] = scenes

                return ContentGenerationOutput(**block.input)
        raise ValueError("Model did not return tool_use block")
