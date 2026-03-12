from __future__ import annotations

import pytest
from playwright.sync_api import Page

from framework.pages.patients_page import PatientsPage


@pytest.mark.smoke
def test_send_patient_invitation(page: Page) -> None:
    page.goto("/dashboard", wait_until="domcontentloaded")
    patients = PatientsPage(page)
    patients.open_from_sidebar()
    patients.send_invitation(email="kuwarsatyam07@gmail.com")

