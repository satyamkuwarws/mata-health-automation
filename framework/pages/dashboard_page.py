from __future__ import annotations

from playwright.sync_api import Page, expect

from framework.pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.get_by_role("heading", name="Dashboard")

    def goto(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/dashboard", wait_until="domcontentloaded")

    def expect_loaded(self) -> None:
        expect(self.header).to_be_visible()

