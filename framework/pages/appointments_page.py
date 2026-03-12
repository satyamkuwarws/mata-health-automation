from __future__ import annotations

from playwright.sync_api import Page, expect

from framework.locators.nav_locators import NavLocators
from framework.pages.base_page import BasePage


class AppointmentsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav_appointments = page.get_by_role("link", name=NavLocators.APPOINTMENTS_LINK_NAME)
        self.header = page.get_by_role("heading", name="Appointments")

    def open_from_sidebar(self) -> None:
        self.click(self.nav_appointments)
        self.wait_for_network_idle()

    def expect_loaded(self) -> None:
        expect(self.header).to_be_visible()

