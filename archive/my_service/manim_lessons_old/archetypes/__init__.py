"""Archetype 入口. 子 lesson 直接 from ..archetypes import GeometryArchetype."""
from ._base import LessonArchetype
from .geometry import GeometryArchetype
from .stats import StatsArchetype
from .biology import BiologyArchetype
from .physics import PhysicsArchetype
from .method_compare import MethodCompareArchetype

from .misconception import MisconceptionArchetype

__all__ = [
    "LessonArchetype",
    "GeometryArchetype",
    "StatsArchetype",
    "BiologyArchetype",
    "PhysicsArchetype",
    "MethodCompareArchetype",
]
