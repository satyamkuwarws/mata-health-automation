from __future__ import annotations

import logging
import sys
from pathlib import Path


def configure_logging(*, log_dir: Path, level: str) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / "test-run.log"

    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    console.setLevel(root.level)

    fileh = logging.FileHandler(logfile, encoding="utf-8")
    fileh.setFormatter(fmt)
    fileh.setLevel(root.level)

    root.addHandler(console)
    root.addHandler(fileh)

