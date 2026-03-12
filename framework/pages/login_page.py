from __future__ import annotations

from playwright.sync_api import Page, expect

from framework.locators.login_locators import LoginLocators
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.get_by_label(LoginLocators.USERNAME_LABEL)
        self.password = page.get_by_label(LoginLocators.PASSWORD_LABEL)
        self.sign_in = page.get_by_role("button", name=LoginLocators.SIGN_IN_ROLE_NAME)

    def goto(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/login", wait_until="domcontentloaded")

    def login(self, username: str, password: str) -> None:
        self.fill(self.username, username)
        self.fill(self.password, password)
        self.click(self.sign_in)

    def expect_logged_in(self) -> None:
        # Prefer a stable test id for the authenticated shell.
        expect(self.page.get_by_test_id(LoginLocators.APP_SHELL_TEST_ID)).to_be_visible()

