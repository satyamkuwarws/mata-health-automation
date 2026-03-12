"""
Framework-level Playwright defaults (Python).

Note: The Node/TS Playwright runner uses `playwright.config.{ts,js}`.
This project uses Playwright **Python sync API** via pytest, so this file is
an internal convention to centralize browser/context defaults.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlaywrightDefaults:
    viewport_width: int = 1440
    viewport_height: int = 900
    locale: str = "en-US"
    timezone_id: str = "America/New_York"


DEFAULTS = PlaywrightDefaults()

