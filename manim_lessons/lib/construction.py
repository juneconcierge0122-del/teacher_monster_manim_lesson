"""
Construction
============
幾何構造工具. 給 Triangle Centers / Quadratic / 其他幾何 lesson 用.

每個函式回傳 Manim Mobject (可以直接 self.add 或 Create), 不直接 mutate scene.
"""
import numpy as np
from manim import (
    Line, DashedLine, Dot, VGroup, Circle, Arc,
    ORIGIN, RIGHT, UP, LEFT, DOWN
)

from .design_tokens import (
    WARN, GHOST, INK, STROKE_THIN, STROKE_NORMAL, STROKE_DASH
)

# ── Vector helpers ─────────────────────────────────────────────────────
def _to_np(p):
    """確保座標是 3D np.array (Manim 用 z=0)."""
    p = np.array(p, dtype=float)
    if p.shape == (2,):
        p = np.array([p[0], p[1], 0.0])
    return p

def _normalize(v, eps=1e-9):
    n = np.linalg.norm(v)
    return v / n if n > eps else v


# ── 幾何構造線 (Mobject 工廠) ─────────────────────────────────────────────
def perpendicular_bisector(p1, p2, length: float = 10.0,
                           color=WARN, stroke=STROKE_NORMAL) -> Line:
    """兩點之間的中垂線 (用於 Circumcenter 構造)."""
    p1, p2 = _to_np(p1), _to_np(p2)
    mid = (p1 + p2) / 2
    direction = p2 - p1
    perp = np.array([-direction[1], direction[0], 0.0])
    perp = _normalize(perp) * (length / 2)
    return Line(mid - perp, mid + perp, color=color, stroke_width=stroke)


def angle_bisector(vertex, p1, p2, length: float = 8.0,
                   color=WARN, stroke=STROKE_NORMAL) -> Line:
    """以 vertex 為頂點, 朝 p1 / p2 兩臂的角平分線 (用於 Incenter 構造)."""
    vertex, p1, p2 = _to_np(vertex), _to_np(p1), _to_np(p2)
    v1 = _normalize(p1 - vertex)
    v2 = _normalize(p2 - vertex)
    bisector_dir = _normalize(v1 + v2)
    return Line(vertex, vertex + bisector_dir * length, color=color, stroke_width=stroke)


def median(vertex, p1, p2, color=WARN, stroke=STROKE_NORMAL) -> Line:
    """中線: 從 vertex 到 p1-p2 中點."""
    vertex, p1, p2 = _to_np(vertex), _to_np(p1), _to_np(p2)
    return Line(vertex, (p1 + p2) / 2, color=color, stroke_width=stroke)


def altitude(vertex, line_p1, line_p2, color=WARN, stroke=STROKE_NORMAL) -> Line:
    """高: 從 vertex 垂直落到 line_p1-line_p2 上的線段."""
    vertex = _to_np(vertex)
    foot = foot_of_perpendicular(vertex, line_p1, line_p2)
    return Line(vertex, foot, color=color, stroke_width=stroke)


def foot_of_perpendicular(point, line_p1, line_p2) -> np.ndarray:
    """點 point 投影到直線 (line_p1, line_p2) 上的垂足座標."""
    point, p1, p2 = _to_np(point), _to_np(line_p1), _to_np(line_p2)
    edge_dir = _normalize(p2 - p1)
    t = np.dot(point - p1, edge_dir)
    return p1 + t * edge_dir


def perpendicular_to_segment(point, line_p1, line_p2,
                             color=WARN, stroke=STROKE_DASH) -> DashedLine:
    """從 point 到線段 line_p1-line_p2 的垂直線 (虛線, 表示距離量度)."""
    foot = foot_of_perpendicular(point, line_p1, line_p2)
    return DashedLine(_to_np(point), foot, color=color, stroke_width=stroke)


# ── 三角形特殊點 (純座標計算) ────────────────────────────────────────────
def circumcenter_of(A, B, C) -> np.ndarray:
    """外心: 三點外接圓圓心. 用兩條中垂線交點解析求解."""
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    ax, ay = A[0], A[1]
    bx, by = B[0], B[1]
    cx, cy = C[0], C[1]
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        raise ValueError("三點共線, 無外心")
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / d
    return np.array([ux, uy, 0.0])


def incenter_of(A, B, C) -> np.ndarray:
    """內心: 三邊角平分線交點. 公式: 邊長加權平均."""
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    a = np.linalg.norm(B - C)   # 對 A 的邊
    b = np.linalg.norm(A - C)   # 對 B 的邊
    c = np.linalg.norm(A - B)   # 對 C 的邊
    return (a * A + b * B + c * C) / (a + b + c)


def centroid_of(A, B, C) -> np.ndarray:
    """重心: 三頂點算術平均."""
    return (_to_np(A) + _to_np(B) + _to_np(C)) / 3


def orthocenter_of(A, B, C) -> np.ndarray:
    """垂心 (三高交點). 用歐拉線性質: O + H = 3G − 2O … 直接解析也可以."""
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    # 垂心 = A + B + C − 2 * 外心
    O = circumcenter_of(A, B, C)
    return A + B + C - 2 * O


def circumradius(A, B, C) -> float:
    """外接圓半徑."""
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    O = circumcenter_of(A, B, C)
    return float(np.linalg.norm(O - A))


def inradius(A, B, C) -> float:
    """內切圓半徑 = 面積 / 半周長."""
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    a = np.linalg.norm(B - C)
    b = np.linalg.norm(A - C)
    c = np.linalg.norm(A - B)
    s = (a + b + c) / 2
    area = abs((B[0] - A[0]) * (C[1] - A[1]) -
               (C[0] - A[0]) * (B[1] - A[1])) / 2
    return float(area / s)


# ── 高階組合: 一鍵產生「外心 + 外接圓 + 三條等距線」 ──────────────────────
def circumcircle_construction(A, B, C, accent_color, dash_color=None) -> dict:
    """
    回傳 dict 包含:
      'center' (Dot), 'circle' (Circle), 'radii' (VGroup of DashedLines)
    用法:
      from .construction import circumcircle_construction
      pieces = circumcircle_construction(A, B, C, VERTEX_CLR)
      self.play(GrowFromCenter(pieces['center']))
      self.play(Create(pieces['circle']))
    """
    if dash_color is None:
        dash_color = accent_color
    O = circumcenter_of(A, B, C)
    r = circumradius(A, B, C)
    return {
        'center_pos': O,
        'center': Dot(O, color=accent_color, radius=0.13),
        'circle': Circle(radius=r, color=accent_color,
                         stroke_width=STROKE_NORMAL).move_to(O),
        'radius': r,
        'radii': VGroup(
            DashedLine(O, _to_np(A), color=dash_color, stroke_width=STROKE_DASH),
            DashedLine(O, _to_np(B), color=dash_color, stroke_width=STROKE_DASH),
            DashedLine(O, _to_np(C), color=dash_color, stroke_width=STROKE_DASH),
        ),
    }


def incircle_construction(A, B, C, accent_color, dash_color=None) -> dict:
    """
    回傳 dict 包含:
      'center' (Dot), 'circle' (Circle), 'perpendiculars' (VGroup)
    """
    if dash_color is None:
        dash_color = accent_color
    A, B, C = _to_np(A), _to_np(B), _to_np(C)
    I = incenter_of(A, B, C)
    r = inradius(A, B, C)
    perps = VGroup()
    for p1, p2 in [(A, B), (B, C), (C, A)]:
        foot = foot_of_perpendicular(I, p1, p2)
        perps.add(DashedLine(I, foot, color=dash_color, stroke_width=STROKE_DASH))
    return {
        'center_pos': I,
        'center': Dot(I, color=accent_color, radius=0.13),
        'circle': Circle(radius=r, color=accent_color,
                         stroke_width=STROKE_NORMAL).move_to(I),
        'radius': r,
        'perpendiculars': perps,
    }


# ─────────────────────────────────────────────────────────────────────
# Self-test scene
# ─────────────────────────────────────────────────────────────────────
try:
    from manim import Scene, Polygon, Create, GrowFromCenter, Text

    class _DemoConstruction(Scene):
        """測試所有構造函式. Run: manim -pql construction.py _DemoConstruction"""
        def construct(self):
            from .design_tokens import apply_global_config, VERTEX_CLR, SIDE_CLR, INK, FS_BODY
            apply_global_config()

            A, B, C = LEFT * 4 + DOWN * 1.5, RIGHT * 4 + DOWN * 1.5, RIGHT * 0.5 + UP * 2
            tri = Polygon(A, B, C, color=INK, stroke_width=STROKE_NORMAL)
            self.play(Create(tri))

            # 外心系列
            cc = circumcircle_construction(A, B, C, VERTEX_CLR)
            self.play(GrowFromCenter(cc['center']),
                      Create(cc['radii']),
                      Create(cc['circle']))
            label_O = Text("外心", font_size=FS_BODY, color=VERTEX_CLR).next_to(cc['center'], UP, buff=0.1)
            self.play(Create(label_O))
            self.wait(1)

            # 切到內心
            self.play(*[m.animate.set_opacity(0.2) for m in [cc['center'], cc['circle'], cc['radii'], label_O]])
            ic = incircle_construction(A, B, C, SIDE_CLR)
            self.play(GrowFromCenter(ic['center']),
                      Create(ic['perpendiculars']),
                      Create(ic['circle']))
            self.wait(2)
except ImportError:
    pass
