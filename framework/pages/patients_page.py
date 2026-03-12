from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from framework.locators.nav_locators import NavLocators
from framework.pages.base_page import BasePage


class PatientsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav_patients = page.get_by_role("link", name=NavLocators.PATIENTS_LINK_NAME)
        self.header = page.get_by_role("heading", name="Patients")
        self.invite_button = page.get_by_role("button", name=re.compile(r"^invite$", re.I))

    def open_from_sidebar(self) -> None:
        self.click(self.nav_patients)
        self.wait_for_network_idle()

    def expect_loaded(self) -> None:
        expect(self.header).to_be_visible()

    def send_invitation(self, *, email: str) -> None:
        """
        Sends a patient invitation from the Patients page.

        This targets the common UI pattern:
        - Click top-right "Invite"
        - Fill email in the dialog
        - Click a submit button (often "Invite" or "Send")
        - Verify the invited email appears in the invitations list
        """
        self.click(self.invite_button)

        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()

        # Email field varies by implementation; try label first, then placeholder-like textbox.
        email_input = dialog.get_by_label(re.compile(r"email", re.I))
        if email_input.count() == 0:
            email_input = dialog.get_by_role("textbox", name=re.compile(r"email", re.I))

        self.fill(email_input.first, email)

        submit = dialog.get_by_role("button", name=re.compile(r"(send|invite|submit|register)", re.I))
        self.click(submit.first)
        self.wait_for_network_idle()

        # Assert the invited email is now visible in the list/table.
        expect(self.page.get_by_role("cell", name=re.compile(re.escape(email), re.I))).to_be_visible()

