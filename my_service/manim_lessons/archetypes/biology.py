"""
Biology Archetype (C)
=====================
給 Plant Anatomy / Speciation / 生物結構與動態題型.

提供:
  - 跨切面 (cross-section) 抽象視覺
  - 粒子流 (給 xylem/phloem 水分子糖分子)
  - 族群分裂時間軸 (給 speciation, 用 lib/timeline 的 VerticalDivergence)
"""
import numpy as np
from manim import (
    Text, VGroup, Circle, Annulus, Line, Dot, Polygon, Sector,
    Create, Write, FadeIn, FadeOut, MoveAlongPath, LaggedStart,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI
)

from ._base import LessonArchetype
from ..lib.timeline import VerticalDivergence
from ..lib.design_tokens import (
    INK, DIM, GHOST, ACCENT_A, ACCENT_B, ACCENT_C, WARN,
    FS_BODY, FS_SMALL, BEAT_M, BEAT_L, STROKE_NORMAL
)


class BiologyArchetype(LessonArchetype):
    """
    Helper methods 給 biology lesson.

    子類別 teach() 可以呼叫:
      self.draw_cross_section_dicot(radius=2)  # 雙子葉根/莖橫切
      self.draw_cross_section_monocot(radius=2)
      self.particle_flow(start, end, n=10, color=...)
      self.show_divergence(ancestor, branches)
    """
    ACCENT = ACCENT_B

    # ── 抽象橫切面 ─────────────────────────────────────────────────
    def draw_cross_section_dicot(self, radius: float = 2.0, position=ORIGIN):
        """
        雙子葉植物根的橫切: 中央是 X 形 xylem, 周圍環狀 phloem.
        所有 element 都用幾何近似而非寫實圖.
        """
        center = np.array(position)

        # 最外層: 表皮
        epidermis = Circle(radius=radius, color=DIM, stroke_width=2).move_to(center)
        # 皮層 (灰色填充)
        cortex = Circle(radius=radius * 0.8, color=GHOST,
                        fill_opacity=0.3, stroke_width=1).move_to(center)
        # 內皮層
        endodermis = Circle(radius=radius * 0.55, color=DIM,
                            stroke_width=1.5).move_to(center)

        # 中央維管束 (X 形): 4 條 xylem 像十字, phloem 在角落
        xylem_lines = VGroup()
        for angle in [0, PI / 2]:
            line = Line(
                center + np.array([np.cos(angle), np.sin(angle), 0]) * radius * 0.45,
                center - np.array([np.cos(angle), np.sin(angle), 0]) * radius * 0.45,
                color=ACCENT_A, stroke_width=5
            )
            xylem_lines.add(line)

        phloem_dots = VGroup()
        for angle in [PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4]:
            d = Dot(
                center + np.array([np.cos(angle), np.sin(angle), 0]) * radius * 0.3,
                color=ACCENT_B, radius=0.12
            )
            phloem_dots.add(d)

        labels = VGroup(
            Text("Xylem (運水)", font_size=FS_SMALL, color=ACCENT_A).next_to(
                center + np.array([radius + 0.5, radius * 0.4, 0]), RIGHT, buff=0),
            Text("Phloem (運糖)", font_size=FS_SMALL, color=ACCENT_B).next_to(
                center + np.array([radius + 0.5, -radius * 0.4, 0]), RIGHT, buff=0),
            Text("Cortex 皮層", font_size=FS_SMALL, color=DIM).next_to(
                center + np.array([-radius - 0.5, 0, 0]), LEFT, buff=0),
        )

        whole = VGroup(epidermis, cortex, endodermis, xylem_lines, phloem_dots, labels)
        self.play(Create(epidermis), run_time=0.6)
        self.play(FadeIn(cortex), Create(endodermis), run_time=0.8)
        self.play(Create(xylem_lines), FadeIn(phloem_dots), run_time=1.0)
        self.play(Write(labels), run_time=1.2)
        self.narrator.silent(BEAT_M)
        return whole

    def draw_cross_section_monocot(self, radius: float = 2.0, position=ORIGIN):
        """
        單子葉莖橫切: 維管束分散排列.
        """
        center = np.array(position)
        epidermis = Circle(radius=radius, color=DIM, stroke_width=2).move_to(center)
        cortex = Circle(radius=radius * 0.95, color=GHOST,
                        fill_opacity=0.3, stroke_width=0).move_to(center)

        # 散布的維管束: 每個是一小塊, xylem 黃 + phloem 青
        bundles = VGroup()
        np.random.seed(7)
        for _ in range(14):
            r = np.random.uniform(0.2, radius * 0.85)
            theta = np.random.uniform(0, 2 * PI)
            bx = center[0] + r * np.cos(theta)
            by = center[1] + r * np.sin(theta)
            bundle = VGroup(
                Dot([bx, by, 0], color=ACCENT_A, radius=0.10),  # xylem
                Dot([bx + 0.15, by, 0], color=ACCENT_B, radius=0.08),  # phloem
            )
            bundles.add(bundle)

        labels = VGroup(
            Text("分散式維管束 (典型單子葉)", font_size=FS_SMALL, color=DIM).next_to(
                center + np.array([0, -radius - 0.4, 0]), DOWN, buff=0.1),
        )

        whole = VGroup(epidermis, cortex, bundles, labels)
        self.play(Create(epidermis), FadeIn(cortex), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, scale=1.5) for b in bundles],
                              lag_ratio=0.05), run_time=1.5)
        self.play(Write(labels), run_time=0.8)
        return whole

    # ── 粒子流 (水/糖分子) ──────────────────────────────────────────
    def particle_flow(self, start, end, n: int = 8, color=ACCENT_A,
                      run_time: float = 2.5, particle_radius: float = 0.06):
        """從 start 流動到 end 的 n 顆粒子. 模擬 xylem 水分子向上."""
        path = Line(start, end)
        particles = VGroup(*[Dot(start, color=color, radius=particle_radius)
                             for _ in range(n)])
        self.add(particles)

        # 錯開出發時間 (delay each particle slightly via run_time scaling)
        from manim import AnimationGroup
        anims = []
        for i, p in enumerate(particles):
            offset_factor = i / max(n - 1, 1) * 0.5
            anims.append(MoveAlongPath(p, path,
                                        run_time=run_time,
                                        rate_func=lambda t, off=offset_factor:
                                            max(0, min(1, (t - off) / (1 - off + 1e-9)))
                                        if t > off else 0))
        # 同時動但有錯開效果. 為簡化用簡單版:
        from manim import AnimationGroup
        self.play(AnimationGroup(*anims, lag_ratio=0.15), run_time=run_time)
        self.remove(particles)

    # ── 族群分化 ──────────────────────────────────────────────────
    def show_divergence(self, ancestor: str, branches: list):
        """
        branches: list of {'label': str, 'color': str, 'angle_deg': float}
        例如:
            self.show_divergence("共同祖先", [
                {'label': '物種 A', 'color': ACCENT_A, 'angle_deg': 130},
                {'label': '物種 B', 'color': ACCENT_B, 'angle_deg': 50},
            ])
        """
        from manim import Create
        div = VerticalDivergence(ancestor, branches)
        self.play(FadeIn(div.ancestor), Create(div.trunk), run_time=1.0)
        self.narrator.silent(BEAT_M)
        div.grow_branches(self, run_time=1.5)
        self.narrator.silent(BEAT_L)
        return div
