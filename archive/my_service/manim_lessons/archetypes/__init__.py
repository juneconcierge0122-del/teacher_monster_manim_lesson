"""Archetype entry point."""
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
    "MisconceptionArchetype",
]
