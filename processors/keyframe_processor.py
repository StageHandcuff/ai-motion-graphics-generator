"""Keyframe processor — picks anchor frames per scene for the diffuser."""
from __future__ import annotations

from models.pipeline import PipelineContext
from models.scene import Keyframe, Scene, SceneGraph
from services.model_router import ModelRouter
from utils.logging_setup import get_logger

log = get_logger(__name__)


class KeyframeProcessor(Processor):
    name = "keyframe"

    def process(self, graph: SceneGraph, ctx: PipelineContext) -> SceneGraph:
        router = ModelRouter.from_context(ctx)
        out: list[Scene] = []
        for scene in graph.scenes:
            anchors = _anchor_times(scene, ctx.keyframes_per_scene)
            kfs = [
                Keyframe(at_sec=t, prompt=_prompt_for(scene, t), image_bytes=router.render_keyframe(scene, t))
                for t in anchors
            ]
            out.append(scene.model_copy(update={"keyframes": kfs}))
        log.info("processor.keyframe", extra={"scenes": len(out)})
        return graph.model_copy(update={"scenes": out})


def _anchor_times(scene: Scene, n: int) -> list[float]:
    if n <= 1:
        return [scene.start_sec + scene.duration_sec / 2]
    step = scene.duration_sec / (n - 1)
    return [scene.start_sec + i * step for i in range(n)]


def _prompt_for(scene: Scene, t: float) -> str:
    text = " ".join(c.text for c in scene.cues) or scene.notes
    return f"{text} | t={t:.2f}s | style=motion-graphics"