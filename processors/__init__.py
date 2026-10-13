"""Ordered pipeline stages. Each stage is (SceneGraph, Ctx) -> SceneGraph."""
from processors.base import Processor
from processors.keyframe_processor import KeyframeProcessor
from processors.scene_planner import ScenePlanner
from processors.tween_processor import TweenProcessor

PIPELINE: list[Processor] = [
    ScenePlanner(),
    KeyframeProcessor(),
    TweenProcessor(),
]

__all__ = ["PIPELINE", "Processor"]