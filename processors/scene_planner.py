"""Scene planner — lays out timing, camera, and text placement per scene."""
from __future__ import annotations

from models.pipeline import PipelineContext
from models.scene import Scene, SceneGraph
from utils.logging_setup import get_logger

log = get_logger(__name__)


class ScenePlanner(Processor):
    name = "scene_planner"

    def process(self, graph: SceneGraph, ctx: PipelineContext) -> SceneGraph:
        planned: list[Scene] = []
        t_cursor = 0.0
        for scene in graph.scenes:
            dur = max(scene.duration_sec, ctx.min_scene_sec)
            planned.append(
                Scene(
                    index=scene.index,
                    cues=scene.cues,
                    duration_sec=dur,
                    start_sec=t_cursor,
                    camera=ctx.default_camera,
                    notes=scene.notes,
                )
            )
            t_cursor += dur
        log.info("processor.scene_planner", extra={"scenes": len(planned), "total_sec": t_cursor})
        return SceneGraph(scenes=planned, total_duration_sec=t_cursor)