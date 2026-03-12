from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from framework.pages.appointments_page import AppointmentsPage
from framework.pages.patients_page import PatientsPage
from framework.utilities.data_loader import load_json


@pytest.mark.smoke
class TestAdminSmoke:
    def test_admin_login_reuse(self, page: Page) -> None:
        # Storage-state fixture should already have authenticated the context.
        page.goto("/dashboard", wait_until="domcontentloaded")
        expect(page.get_by_test_id("app-shell")).to_be_visible()

    def test_dashboard_load(self, page: Page) -> None:
        expectations = load_json("test_data/smoke/portal_expectations.json")
        page.goto("/dashboard", wait_until="domcontentloaded")
        expect(page.get_by_role("heading", name=expectations["dashboard_heading"])).to_be_visible()

    def test_navigate_to_patients(self, page: Page) -> None:
        expectations = load_json("test_data/smoke/portal_expectations.json")
        page.goto("/dashboard", wait_until="domcontentloaded")
        patients = PatientsPage(page)
        patients.open_from_sidebar()
        expect(page.get_by_role("heading", name=expectations["patients_heading"])).to_be_visible()

    def test_navigate_to_appointments(self, page: Page) -> None:
        expectations = load_json("test_data/smoke/portal_expectations.json")
        page.goto("/dashboard", wait_until="domcontentloaded")
        appts = AppointmentsPage(page)
        appts.open_from_sidebar()
        expect(page.get_by_role("heading", name=expectations["appointments_heading"])).to_be_visible()

