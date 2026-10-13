"""Processor ABC — pure where possible, side effects only via the context."""
from __future__ import annotations

from abc import ABC, abstractmethod

from models.pipeline import PipelineContext
from models.scene import SceneGraph


class Processor(ABC):
    name: str = "unnamed"

    @abstractmethod
    def process(self, graph: SceneGraph, ctx: PipelineContext) -> SceneGraph:
        """Return a new graph; do not mutate the input."""