"""Typer CLI — the primary entry point for ai-motion-graphics-generator."""
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from models.job import RenderJob
from services.pipeline_service import PipelineService
from utils.logging_setup import get_logger

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()
log = get_logger(__name__)


@app.command()
def render(
    input: Path = typer.Option(..., "--input", "-i", exists=True, help="Text, storyboard, or clip."),
    preset: str = typer.Option("1080p60", "--preset", "-p"),
    driver: str = typer.Option("ffmpeg", "--driver", "-d"),
    out: Path = typer.Option(Path("./renders/out.mp4"), "--out", "-o"),
) -> None:
    """Run the full ingest → process → render pipeline once."""
    job = RenderJob.from_paths(input_path=input, preset=preset, driver=driver, out_path=out)
    svc = PipelineService.from_config()
    result = asyncio.run(svc.run(job))
    console.print(f"[bold green]rendered[/] {result.out_path} in {result.elapsed_sec:.2f}s")
    log.info("render.done", extra={"out": str(result.out_path), "frames": result.frame_count})


@app.command()
def watch(
    inbox: Path = typer.Option(Path("./inbox"), "--inbox"),
    preset: str = typer.Option("1080p60", "--preset"),
) -> None:
    """Watch a folder and render every new job file dropped into it."""
    svc = PipelineService.from_config()
    asyncio.run(svc.watch(inbox=inbox, preset=preset))


@app.command()
def version() -> None:
    from bootstrap import __version__
    console.print(__version__)


if __name__ == "__main__":
    app()