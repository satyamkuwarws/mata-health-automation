from __future__ import annotations

import logging
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, expect, sync_playwright

try:
    import allure  # type: ignore
except Exception:  # pragma: no cover
    allure = None

from framework.config.settings import Settings, get_settings
from framework.pages.login_page import LoginPage
from framework.utilities.artifacts import safe_filename
from framework.utilities.logging_utils import configure_logging


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("ui")
    group.addoption("--browser", action="store", default=None, help="chromium|firefox|webkit")
    group.addoption("--headed", action="store", default=None, help="true/false to override HEADLESS")
    group.addoption("--base-url", action="store", default=None, help="override BASE_URL")
    group.addoption("--slowmo", action="store", default=None, help="slow mo ms override")


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    s = get_settings()
    if pytestconfig.getoption("--browser"):
        s.browser = pytestconfig.getoption("--browser")  # type: ignore[misc]
    if pytestconfig.getoption("--headed") is not None:
        headed = str(pytestconfig.getoption("--headed")).lower() in ("1", "true", "yes", "y")
        s.headless = not headed
    if pytestconfig.getoption("--base-url"):
        s.base_url = pytestconfig.getoption("--base-url")
    if pytestconfig.getoption("--slowmo") is not None:
        s.slow_mo_ms = int(pytestconfig.getoption("--slowmo"))
    s.ensure_dirs()
    configure_logging(log_dir=s.log_dir, level=s.log_level)
    logging.getLogger(__name__).info(
        "Settings: browser=%s headless=%s base_url=%s", s.browser, s.headless, s.base_url
    )
    return s


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    browser_type = getattr(playwright_instance, settings.browser)
    b = browser_type.launch(headless=settings.headless, slow_mo=settings.slow_mo_ms)
    yield b
    b.close()


@pytest.fixture(scope="session")
def storage_state_path(settings: Settings, worker_id: str) -> Path:
    # One storage state per xdist worker to avoid cross-process file contention.
    filename = f"storage_state_{safe_filename(worker_id)}.json"
    return settings.storage_state_dir / filename


@pytest.fixture(scope="session")
def authenticated_storage_state(browser: Browser, settings: Settings, storage_state_path: Path) -> Path:
    if storage_state_path.exists():
        return storage_state_path

    ctx = browser.new_context(base_url=settings.base_url)
    page = ctx.new_page()
    page.set_default_timeout(settings.default_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    expect.set_options(timeout=settings.expect_timeout_ms)

    login = LoginPage(page)
    login.goto(settings.base_url)
    login.login(settings.admin_username, settings.admin_password)
    login.expect_logged_in()

    ctx.storage_state(path=str(storage_state_path))
    page.close()
    ctx.close()
    return storage_state_path


@pytest.fixture()
def context(
    browser: Browser, settings: Settings, authenticated_storage_state: Path, request: pytest.FixtureRequest
) -> Generator[BrowserContext, None, None]:
    test_id = safe_filename(request.node.nodeid)

    record_video_dir = settings.videos_dir / test_id
    record_video_dir.mkdir(parents=True, exist_ok=True)

    ctx = browser.new_context(
        base_url=settings.base_url,
        storage_state=str(authenticated_storage_state),
        record_video_dir=str(record_video_dir),
    )
    ctx.set_default_timeout(settings.default_timeout_ms)
    ctx.set_default_navigation_timeout(settings.navigation_timeout_ms)
    expect.set_options(timeout=settings.expect_timeout_ms)

    ctx.tracing.start(screenshots=True, snapshots=True, sources=False)
    yield ctx

    # Trace stop happens in `page` fixture (needs test outcome).
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext, settings: Settings, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p

    report = getattr(request.node, "rep_call", None)
    failed = bool(report and report.failed)
    test_id = safe_filename(request.node.nodeid)

    if failed:
        screenshot_path = settings.screenshots_dir / f"{test_id}.png"
        try:
            p.screenshot(path=str(screenshot_path), full_page=True)
            if allure:
                allure.attach.file(str(screenshot_path), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            logging.getLogger(__name__).exception("Failed to capture screenshot")

    try:
        if failed:
            trace_path = settings.traces_dir / f"{test_id}.zip"
            context.tracing.stop(path=str(trace_path))
            if allure:
                allure.attach.file(str(trace_path), name="trace", attachment_type=allure.attachment_type.ZIP)
        else:
            context.tracing.stop()
    except Exception:
        logging.getLogger(__name__).exception("Failed to stop trace")

    video_path = None
    try:
        v = p.video
        p.close()
        if v:
            video_path = Path(v.path())
            if failed and allure and video_path.exists():
                allure.attach.file(str(video_path), name="video", attachment_type=allure.attachment_type.WEBM)
    except Exception:
        logging.getLogger(__name__).exception("Failed to handle video")
        try:
            p.close()
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def worker_id(pytestconfig: pytest.Config) -> str:
    return getattr(pytestconfig, "workerinput", {}).get("workerid", "master")

