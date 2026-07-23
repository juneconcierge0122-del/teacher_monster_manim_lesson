import base64
import json
import re
from pathlib import Path
from typing import Optional

import anthropic
from pydantic import BaseModel

from src.config_schema import LLMConfig


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

        user_prompt = f"""You are an expert instructional designer and animation creator.
Generate teaching video content based on the requirement and persona below.

## Requirement
{requirement_prompt}

## Persona
{persona_prompt}

Guidelines for Manim code:
- Use: from manim import *
- Define a class inheriting from Scene
- Keep code self-contained and runnable
- Use English text only in all Text() and Tex() objects

Guidelines for transcript:
- Must be in English, 2-4 sentences per scene
- Match the visual content, engaging and clear
"""

        tool = {
            "name": "submit_scenes",
            "description": "Submit the generated scenes for the teaching video.",
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

        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_scenes":
                return ContentGenerationOutput(**block.input)

        raise ValueError("Model did not return tool_use block")
