from __future__ import annotations

import logging
from pathlib import Path

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.log = logging.getLogger(self.__class__.__name__)

    def wait_for_network_idle(self, *, timeout_ms: int | None = None) -> None:
        self.page.wait_for_load_state("networkidle", timeout=timeout_ms)

    def wait_for_element(self, locator: Locator, *, timeout_ms: int | None = None) -> None:
        locator.wait_for(state="visible", timeout=timeout_ms)

    def click(self, locator: Locator, *, timeout_ms: int | None = None) -> None:
        self.wait_for_element(locator, timeout_ms=timeout_ms)
        locator.click()

    def fill(self, locator: Locator, value: str, *, timeout_ms: int | None = None, clear: bool = True) -> None:
        self.wait_for_element(locator, timeout_ms=timeout_ms)
        if clear:
            locator.fill("")
        locator.fill(value)

    def verify_text(self, locator: Locator, expected: str, *, timeout_ms: int | None = None) -> None:
        expect(locator).to_contain_text(expected, timeout=timeout_ms)

    def take_screenshot(self, path: Path, *, full_page: bool = True) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=full_page)
        return path

