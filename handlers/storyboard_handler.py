"""Storyboard ingest — YAML/JSON panels with shot metadata."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from handlers.base import IngestHandler
from models.scene import Scene, SceneGraph
from utils.logging_setup import get_logger

log = get_logger(__name__)


class StoryboardIngestHandler(IngestHandler):
    name = "storyboard"

    def can_handle(self, source: Path) -> bool:
        return source.suffix.lower() in {".yaml", ".yml", ".json"} and "storyboard" in source.name.lower()

    def ingest(self, source: Path) -> SceneGraph:
        raw = source.read_text(encoding="utf-8")
        doc = yaml.safe_load(raw) if source.suffix.lower() in {".yaml", ".yml"} else json.loads(raw)
        panels = doc.get("panels") or []
        if not panels:
            raise ValueError(f"storyboard {source} has no panels")
        scenes = [
            Scene(
                index=i,
                cues=[],
                duration_sec=float(p.get("duration", 3.0)),
                notes=str(p.get("shot", "")),
            )
            for i, p in enumerate(panels)
        ]
        log.info("ingest.storyboard", extra={"source": str(source), "panels": len(scenes)})
        return SceneGraph(scenes=scenes)