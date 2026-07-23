"""
Base Lesson Archetype
=====================
所有 archetype 的共同 base. 處理 intro/outro + Persona 強制機制.
"""
from manim import (
    Scene, Text, VGroup, Write, FadeIn, FadeOut, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT
)

from ..lib.design_tokens import (
    BG, INK, DIM, ACCENT_A, FS_TITLE, FS_H1, FS_H2, FS_BODY,
    PAD, BEAT_M, BEAT_L, apply_global_config
)
from ..lib.narrator import Narrator
from ..lib.persona import Persona, PersonaTracker


class LessonArchetype(Scene):
    """
    通用 base. 子類別必須:
      1. 設 PERSONA (Persona 物件) — 沒設會印警告
      2. 覆寫 teach()
      3. 在 teach() 裡用 self.teach_concept(term, definition, example=...)
         引入每個 PERSONA.lacks 概念

    Class attrs:
      HEADING / DEFINITION / ACCENT / BRIDGE_HOOK / CONCLUSION : str
      PERSONA: Persona     # ← 新增. 沒設會印警告.
    """
    HEADING = ""
    DEFINITION = ""
    ACCENT = ACCENT_A
    BRIDGE_HOOK = ""
    CONCLUSION = ""
    PERSONA: Persona = None

    def setup(self):
        apply_global_config()
        self.narrator = Narrator(self)
        self._heading_group = None
        if self.PERSONA is None:
            print(f"⚠ {type(self).__name__}: 沒設 PERSONA — "
                  "Adaptability 會被扣分. 加: PERSONA = Persona(grade=..., ...)")
            self.tracker = None
        else:
            self.tracker = PersonaTracker(self.PERSONA)
            print(f"▸ {type(self).__name__}: {self.PERSONA.summary()}")

    def construct(self):
        if self.BRIDGE_HOOK:
            self.intro_bridge()
        if self.HEADING:
            self.intro_heading()
        self.teach()
        if self.CONCLUSION:
            self.outro()
        # 收尾報告
        if self.tracker:
            problems = self.tracker.report()
            if problems:
                print(f"\n⚠ {type(self).__name__} Persona 違規清單:")
                for p in problems:
                    print(f"   {p}")

    # ── Reusable scene blocks ───────────────────────────────────────
    def intro_bridge(self):
        bridge = Text(self.BRIDGE_HOOK, font_size=FS_H2, color=INK,
                      line_spacing=0.8)
        self.play(Write(bridge), run_time=1.5)
        self.narrator.silent(BEAT_L)
        self.play(FadeOut(bridge), run_time=0.5)

    def intro_heading(self):
        heading = Text(self.HEADING, font_size=FS_H1, color=self.ACCENT)
        heading.to_edge(UP, buff=0.5)
        self.play(Write(heading), run_time=1.0)
        if self.DEFINITION:
            defn = Text(self.DEFINITION, font_size=FS_BODY, color=INK)
            defn.next_to(heading, DOWN, buff=0.2)
            self.play(Write(defn), run_time=1.0)
            self._heading_group = VGroup(heading, defn)
        else:
            self._heading_group = VGroup(heading)
        self.narrator.silent(BEAT_M)

    def fade_heading(self):
        if self._heading_group is not None:
            self.play(FadeOut(self._heading_group), run_time=0.4)
            self._heading_group = None

    def outro(self):
        text = Text(self.CONCLUSION, font_size=FS_BODY, color=self.ACCENT)
        text.to_edge(DOWN, buff=0.4)
        self.play(Write(text), run_time=1.0)
        self.narrator.silent(BEAT_L)

    # ── Persona-enforced teaching ──────────────────────────────────
    def teach_concept(self, term: str, definition: str,
                      example: str = "", visual=None,
                      extra_dwell: float = 0.0):
        """
        引入一個概念. **強制三件套** (定義 + 視覺 + 例子) 並計時.

        - term: 概念名稱 (應對應 PERSONA.lacks 中的一個)
        - definition: 一句話定義
        - example: 具體例子 (給 adaptability 加分)
        - visual: 可選 Mobject (圖示)
        - extra_dwell: 額外停留秒數 (重要概念加碼)

        若 PERSONA 已設, 會自動:
          - 登記 term 為 defined
          - 累積 dwell time
          - 加總到 jargon 計數
        """
        # 1. 顯示 term + definition
        term_mob = Text(term, font_size=FS_H2, color=self.ACCENT, weight="BOLD")
        defn_mob = Text(definition, font_size=FS_BODY, color=INK)
        block = VGroup(term_mob, defn_mob).arrange(DOWN, buff=0.25)
        self.play(Write(term_mob), run_time=0.7)
        self.play(Write(defn_mob), run_time=1.0)

        # 2. 視覺化
        if visual is not None:
            visual.next_to(block, DOWN, buff=0.5)
            self.play(FadeIn(visual), run_time=0.8)

        # 3. 例子
        if example:
            ex = Text(f"例：{example}", font_size=FS_BODY, color=DIM)
            anchor = visual if visual is not None else block
            ex.next_to(anchor, DOWN, buff=0.4)
            self.play(Write(ex), run_time=1.0)

        # 4. 強制 dwell (依 persona 計算)
        if self.PERSONA:
            target = self.PERSONA.seconds_per_lacks_concept
            # 已花約 3 秒在 play; dwell 補到 60% 預算 + extra
            dwell = max(target * 0.6 - 3, 1.0) + extra_dwell
            self.narrator.silent(dwell)
            self.tracker.register_definition(term)
            self.tracker.add_dwell(term, 3.0 + dwell)
        else:
            self.narrator.silent(2.0 + extra_dwell)

        return block

    # ── Hook for subclasses ────────────────────────────────────────
    def teach(self):
        raise NotImplementedError(
            "子類別必須覆寫 teach(). 在 teach() 裡, 對每個 PERSONA.lacks 概念都呼叫 "
            "self.teach_concept(term, definition, example=...)."
        )
