from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from framework.locators.login_locators import LoginLocators
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Be flexible: apps often label the username field as Email / Email address / Username.
        username_by_label = page.get_by_label(re.compile(r"(email|username)", re.I))
        if username_by_label.count():
            self.username = username_by_label
        else:
            # Some apps don't provide accessible names; use resilient CSS fallbacks.
            self.username = page.locator(
                'input[type="email"], input[autocomplete="username"], input[name*="email" i], input[name*="user" i]'
            )

        password_by_label = page.get_by_label(re.compile(r"password", re.I))
        if password_by_label.count():
            self.password = password_by_label
        else:
            self.password = page.locator('input[type="password"], input[autocomplete="current-password"]')
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

