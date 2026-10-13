"""Reference-clip ingest — probes a video and emits a scene graph from shots."""
from __future__ import annotations

from pathlib import Path

from handlers.base import IngestHandler
from models.scene import Scene, SceneGraph
from utils.ffmpeg_probe import probe_duration_sec, probe_scene_cuts
from utils.logging_setup import get_logger

log = get_logger(__name__)

_VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}


class ClipIngestHandler(IngestHandler):
    name = "clip"

    def can_handle(self, source: Path) -> bool:
        return source.suffix.lower() in _VIDEO_EXTS

    def ingest(self, source: Path) -> SceneGraph:
        duration = probe_duration_sec(source)
        cuts = probe_scene_cuts(source) or [0.0, duration]
        scenes: list[Scene] = []
        for i in range(len(cuts) - 1):
            scenes.append(Scene(index=i, cues=[], duration_sec=cuts[i + 1] - cuts[i]))
        log.info("ingest.clip", extra={"source": str(source), "scenes": len(scenes)})
        return SceneGraph(scenes=scenes)