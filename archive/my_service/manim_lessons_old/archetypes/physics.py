"""
Physics Archetype (D)
=====================
給 Energy Conservation / Dimensional Analysis / Fermi Estimation.

提供:
  - 即時能量量條 (KE/PE) — 從 lib.value_panel
  - 單位積木 (給量綱分析)
  - 數量級拆解 (給 Fermi)
"""
import numpy as np
from manim import (
    Text, VGroup, Rectangle, Line, Arrow, MathTex, DecimalNumber,
    Create, Write, FadeIn, FadeOut, Transform, GrowFromCenter,
    UP, DOWN, LEFT, RIGHT, ORIGIN, ValueTracker, always_redraw
)

from ._base import LessonArchetype
from ..lib.value_panel import EnergyPanel
from ..lib.design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ACCENT_C, WARN,
    ENERGY_KE, ENERGY_PE, FS_BODY, FS_SMALL, BEAT_M, BEAT_L
)


class PhysicsArchetype(LessonArchetype):
    """
    Helper methods 給 physics lesson.

    子類別可呼叫:
      self.add_energy_panel(max_value=...)        # 加一個 KE/PE 量條
      self.unit_blocks(units=['m','m','s'])        # 量綱積木
      self.fermi_decomposition(question, factors)  # Fermi 估算
    """
    ACCENT = ACCENT_A

    # ── 能量量條 (能量守恆題) ──────────────────────────────────
    def add_energy_panel(self, max_value: float = 1.0,
                         position=None, KE_init: float = 0.0,
                         PE_init: float = 1.0):
        panel = EnergyPanel(max_value=max_value)
        if position is None:
            panel.to_edge(LEFT, buff=1.0)
        else:
            panel.move_to(position)
        panel.KE_bar.set_value(KE_init)
        panel.PE_bar.set_value(PE_init)
        self.play(FadeIn(panel), run_time=0.8)
        return panel

    def transfer_energy(self, panel: EnergyPanel,
                        KE_target: float, PE_target: float,
                        run_time: float = 2.0):
        """演示能量轉換 (例如下落: PE → KE)."""
        self.play(panel.set_KE(KE_target), panel.set_PE(PE_target),
                  run_time=run_time)
        self.narrator.silent(BEAT_M)

    # ── 單位積木 (量綱分析) ──────────────────────────────────────
    def unit_blocks(self, units: list, position=None,
                    block_size: float = 0.7, color: str = ACCENT_A):
        """
        把 units (e.g. ['kg', 'm', 's^-2']) 視覺化成一排積木.
        用於展示 F = ma 的量綱合成.
        """
        blocks = VGroup()
        for u in units:
            rect = Rectangle(width=block_size * 1.4, height=block_size,
                             color=color, stroke_width=2,
                             fill_color=color, fill_opacity=0.2)
            label = MathTex(u, color=INK, font_size=28)
            block = VGroup(rect, label)
            label.move_to(rect.get_center())
            blocks.add(block)
        blocks.arrange(RIGHT, buff=0.15)
        if position is not None:
            blocks.move_to(position)
        self.play(FadeIn(blocks, shift=UP * 0.3), run_time=0.8)
        return blocks

    def combine_units(self, blocks: VGroup, result_label: str,
                      run_time: float = 1.5):
        """把 unit_blocks 合併成一個結果 (展示量綱推導完成)."""
        result = MathTex(result_label, color=ACCENT_A, font_size=44)
        result.move_to(blocks.get_center())
        self.play(Transform(blocks, result), run_time=run_time)
        self.narrator.silent(BEAT_M)
        return result

    # ── Fermi 估算 (數量級拆解) ──────────────────────────────────
    def fermi_decomposition(self, question: str,
                            factors: list, position=None):
        """
        question: e.g. "How many cells in your hand?"
        factors:  list of (name, value, unit). 會顯示成 question = factor1 × factor2 × ...

        Each factor 是 dict: {'name': '體積', 'value': '0.5 L', 'estimate': '500 cm^3'}
        """
        # 上方顯示問題
        q_text = Text(question, font_size=FS_BODY, color=INK).to_edge(UP, buff=0.6)
        self.play(Write(q_text), run_time=1.2)
        self.narrator.silent(BEAT_M)

        # 中間顯示因子 (依序 fade in)
        factor_groups = VGroup()
        for f in factors:
            group = VGroup(
                Text(f['name'], font_size=FS_SMALL, color=DIM),
                Text(f['value'], font_size=FS_BODY, color=ACCENT_A),
                Text(f['estimate'], font_size=FS_SMALL, color=DIM),
            ).arrange(DOWN, buff=0.1)
            factor_groups.add(group)
        factor_groups.arrange(RIGHT, buff=1.5)
        if position is None:
            factor_groups.move_to(ORIGIN)
        else:
            factor_groups.move_to(position)

        # 因子之間放 × 符號
        x_signs = VGroup()
        for i in range(len(factor_groups) - 1):
            mid_x = (factor_groups[i].get_right()[0] +
                     factor_groups[i + 1].get_left()[0]) / 2
            sign = MathTex(r"\times", color=DIM, font_size=36).move_to(
                [mid_x, factor_groups[0].get_center()[1], 0])
            x_signs.add(sign)

        for i, fg in enumerate(factor_groups):
            self.play(FadeIn(fg, shift=DOWN * 0.2), run_time=0.6)
            if i < len(x_signs):
                self.play(Write(x_signs[i]), run_time=0.3)
            self.narrator.silent(0.4)

        return VGroup(q_text, factor_groups, x_signs)
