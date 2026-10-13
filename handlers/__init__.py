"""Ingest handler registry. Order matters — first match wins."""
from handlers.base import IngestHandler
from handlers.clip_handler import ClipIngestHandler
from handlers.script_handler import ScriptIngestHandler
from handlers.storyboard_handler import StoryboardIngestHandler

HANDLERS: list[IngestHandler] = [
    StoryboardIngestHandler(),
    ScriptIngestHandler(),
    ClipIngestHandler(),
]

__all__ = ["HANDLERS", "IngestHandler"]