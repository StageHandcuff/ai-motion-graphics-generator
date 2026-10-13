"""Plain-text script ingest — the simplest path into the pipeline."""
from __future__ import annotations

import re
from pathlib import Path

from handlers.base import IngestHandler
from models.scene import Scene, SceneGraph, TextCue
from utils.logging_setup import get_logger

log = get_logger(__name__)

_CUE_RE = re.compile(r"^\s*(?:\[(?P<time>\d{1,2}:\d{2}(?:\.\d{1,3})?)\]\s*)?(?P<text>.+)$")


class ScriptIngestHandler(IngestHandler):
    name = "script"

    def can_handle(self, source: Path) -> bool:
        return source.suffix.lower() in {".txt", ".md", ".fountain"}

    def ingest(self, source: Path) -> SceneGraph:
        cues: list[TextCue] = []
        for lineno, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            m = _CUE_RE.match(raw)
            if not m or not m.group("text").strip():
                continue
            cues.append(TextCue(line=lineno, text=m.group("text").strip(),
                                at_sec=_parse_time(m.group("time"))))
        if not cues:
            raise ValueError(f"no usable cues in {source}")
        log.info("ingest.script", extra={"source": str(source), "cues": len(cues)})
        return SceneGraph(scenes=[Scene(index=0, cues=cues, duration_sec=max(c.at_sec for c in cues) or 5.0)])


def _parse_time(t: str | None) -> float:
    if not t:
        return 0.0
    mm, ss = t.split(":")
    return int(mm) * 60 + float(ss)