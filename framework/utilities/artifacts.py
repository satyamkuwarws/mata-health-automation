from __future__ import annotations

import re
from pathlib import Path
from typing import Final


_INVALID: Final[re.Pattern[str]] = re.compile(r"[^a-zA-Z0-9_.-]+")


def safe_filename(value: str, *, max_len: int = 120) -> str:
    cleaned = _INVALID.sub("_", value).strip("._-")
    if not cleaned:
        cleaned = "artifact"
    return cleaned[:max_len]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

