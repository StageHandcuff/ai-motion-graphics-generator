"""Base class every ingest handler implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from models.scene import SceneGraph


class IngestHandler(ABC):
    """Turns a raw source (path or URL) into a SceneGraph."""

    name: str = "unnamed"

    @abstractmethod
    def can_handle(self, source: Path) -> bool:
        """Cheap predicate — no I/O beyond stat()."""

    @abstractmethod
    def ingest(self, source: Path) -> SceneGraph:
        """Parse the source into a normalized scene graph."""