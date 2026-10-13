# Contributing to ai-motion-graphics-generator

Thanks for wanting to mash some frames with us. This repo is a Windows-first
desktop tool that turns text, storyboards, and reference clips into rendered
motion graphics via a pipeline of ingest handlers, processors, and output
drivers.

## Repo shape

```
ai-motion-graphics-generator/
├── bootstrap/          # entry points, CLI, app launcher
├── handlers/           # ingest handlers (one per input kind)
├── processors/         # pipeline stages (scene plan, keyframe, tween, render)
├── drivers/            # output drivers (ffmpeg, aftereffects, webm, gif)
├── services/           # long-lived services (queue, model router, cache)
├── models/             # dataclasses + pydantic schemas for jobs/scenes
├── utils/              # timing, logging, ffmpeg probe, frame math
├── config/             # default + schema
└── tests/              # pytest suite
```

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Running the pipeline locally

```powershell
python -m bootstrap.cli render --input examples/promo.txt --preset 1080p60 --driver ffmpeg
```

## Adding a new ingest handler

1. Subclass `handlers.base.IngestHandler`.
2. Implement `can_handle(source) -> bool` and `ingest(source) -> SceneGraph`.
3. Register it in `handlers/__init__.py::HANDLERS`.
4. Add a fixture under `tests/fixtures/` and a test in `tests/test_handlers.py`.

## Adding a new output driver

1. Subclass `drivers.base.OutputDriver`.
2. Implement `supports(codec) -> bool` and `emit(render_plan, out_path)`.
3. Register in `drivers/__init__.py::DRIVERS`.

## Code style

- `ruff` for lint, `mypy --strict` on `models/` and `utils/`.
- Type hints everywhere. No bare `except:`.
- Log via `utils.logging_setup.get_logger()`, never `print()` in library code.
- Keep processors pure where possible: `(SceneGraph, PipelineContext) -> SceneGraph`.

## PRs

- One feature per PR.
- Include a test for new processors and drivers.
- If you touch the render graph, include a 3-second sample render in the PR
  description (drop it in the description as a link, don't commit binaries).

## Commit messages

Conventional commits, scoped: `feat(processors): add optical-flow tween`,
`fix(drivers/ffmpeg): honor -vsync cfr on 23.976`.