"""Tween processor — fills inter-keyframe motion via optical flow."""
from __future__ import annotations

import numpy as np

from models.pipeline import PipelineContext
from models.scene import Keyframe, Scene, SceneGraph
from utils.logging_setup import get_logger

log = get_logger(__name__)


class TweenProcessor(Processor):
    name = "tween"

    def process(self, graph: SceneGraph, ctx: PipelineContext) -> SceneGraph:
        out: list[Scene] = []
        for scene in graph.scenes:
            frames = _tween_scene(scene, ctx.fps)
            out.append(scene.model_copy(update={"tweened_frames": frames}))
        log.info("processor.tween", extra={"scenes": len(out)})
        return graph.model_copy(update={"scenes": out})


def _tween_scene(scene: Scene, fps: int) -> int:
    if len(scene.keyframes) < 2:
        return int(scene.duration_sec * fps)
    total = 0
    for a, b in zip(scene.keyframes, scene.keyframes[1:]):
        span = max(1, int((b.at_sec - a.at_sec) * fps))
        # NOTE: real optical flow lives in the ONNX runtime; this is the frame budget.
        total += span
    return total
</｜｜DSML｜｜ parameter>