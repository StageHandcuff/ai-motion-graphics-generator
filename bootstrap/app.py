"""Desktop launcher — wires the pipeline service to a tray icon / window."""
from __future__ import annotations

import sys

from services.pipeline_service import PipelineService
from utils.logging_setup import get_logger

log = get_logger(__name__)


def main() -> int:
    log.info("app.boot", extra={"argv": sys.argv[1:]})
    svc = PipelineService.from_config()
    try:
        svc.run_headless_loop()
    except KeyboardInterrupt:
        log.info("app.shutdown", extra={"reason": "sigint"})
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())