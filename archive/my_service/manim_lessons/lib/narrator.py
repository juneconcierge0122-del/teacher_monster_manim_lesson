"""
Narrator
========
旁白 + 字幕同步. 把 self.wait(2) 換成 narrator.say("...", 2.0),
字幕自動出現/消失, 而且方便日後接 ElevenLabs / OpenAI TTS API.

Usage in a Scene:
    self.narrator = Narrator(self)
    self.narrator.say("我們來看一個例子", duration=1.8)
    # ... 動畫 ...
    self.narrator.say("這就是答案了", duration=2.0)
"""
from manim import (
    Scene, Text, VGroup, Rectangle, FadeIn, FadeOut, DOWN, UP,
    AnimationGroup, ReplacementTransform
)

from .design_tokens import INK, DIM, FS_CAPTION, BG, PAD


class Narrator:
    """
    管理一個固定位置的字幕條, 在 say() 時切換內容.
    duration 是這句話 *說完所需的時間* (秒). Scene 會在 duration 內等待.
    """

    def __init__(self, scene: Scene, position="bottom", max_chars_per_line=24):
        self.scene = scene
        self.position = position
        self.max_chars = max_chars_per_line
        self._current_caption = None

    def _wrap(self, text: str) -> str:
        """簡易斷行: 中文按 max_chars 切, 不破壞 punctuation 太多."""
        if len(text) <= self.max_chars:
            return text
        # 中文情境: 直接按字數切
        lines = []
        i = 0
        while i < len(text):
            # 在標點處優先換行
            chunk = text[i:i + self.max_chars]
            i += self.max_chars
            lines.append(chunk)
        return "\n".join(lines)

    def _make_caption(self, text: str) -> Text:
        wrapped = self._wrap(text)
        cap = Text(wrapped, font_size=FS_CAPTION, color=INK,
                   line_spacing=0.7)
        if self.position == "bottom":
            cap.to_edge(DOWN, buff=0.4)
        else:
            cap.to_edge(UP, buff=0.4)
        return cap

    def say(self, text: str, duration: float = 1.5, fade_in: float = 0.25):
        """無視覺版：只等候 duration 秒，給音訊預留時間，不顯示字幕。"""
        self.scene.wait(duration)

    def say_show(self, text: str, duration: float = 1.5, fade_in: float = 0.25):
        """顯示一句字幕並等候 duration 秒."""
        new_cap = self._make_caption(text)
        if self._current_caption is None:
            self.scene.play(FadeIn(new_cap, run_time=fade_in))
        else:
            # 平滑切換
            self.scene.play(
                ReplacementTransform(self._current_caption, new_cap, run_time=fade_in)
            )
        self._current_caption = new_cap
        self.scene.wait(max(duration - fade_in, 0.1))

    def silent(self, duration: float = 1.0):
        """無字幕等候 (例如純動畫過場)."""
        self.scene.wait(duration)

    def clear(self, fade_out: float = 0.3):
        """淡出字幕."""
        if self._current_caption is not None:
            self.scene.play(FadeOut(self._current_caption, run_time=fade_out))
            self._current_caption = None


# ─────────────────────────────────────────────────────────────────────
# Self-test scene
# ─────────────────────────────────────────────────────────────────────
try:
    from manim import Scene, Circle, GrowFromCenter

    class _DemoNarrator(Scene):
        """測試字幕切換. Run: manim -pql narrator.py _DemoNarrator"""
        def construct(self):
            from .design_tokens import apply_global_config, ACCENT_A
            apply_global_config()
            n = Narrator(self)

            n.say("我們來看一個例子", duration=1.8)
            c = Circle(radius=1.5, color=ACCENT_A)
            self.play(GrowFromCenter(c), run_time=1.0)
            n.say("這就是一個圓形", duration=1.5)
            n.say("它的特點是所有點到圓心的距離都相等", duration=2.5)
            n.clear()
            self.wait(0.5)
except ImportError:
    pass
