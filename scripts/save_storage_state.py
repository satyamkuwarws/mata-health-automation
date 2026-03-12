from __future__ import annotations

import argparse
import logging
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description="Save Playwright storage-state after manual OTP login.")
    parser.add_argument("--base-url", required=True, help="Admin base URL, e.g. https://.../admin")
    parser.add_argument(
        "--out",
        default="reports/artifacts/storage/storage_state_master.json",
        help="Where to write storage state json",
    )
    parser.add_argument("--admin-email", default=None, help="Optional: prefill the email field on the login screen")
    parser.add_argument("--timeout-ms", type=int, default=300_000, help="Max time to wait for OTP login")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger("save_storage_state")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        log.info("Launching browser (headed) for manual OTP login")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(base_url=args.base_url)
        page = context.new_page()

        log.info("Navigating to %s", args.base_url)
        page.goto(args.base_url, wait_until="domcontentloaded")

        if args.admin_email:
            # Best-effort prefill (UI may vary).
            for selector in [
                page.get_by_label("Email"),
                page.get_by_label("Email address"),
                page.locator('input[type="email"]'),
                page.locator('input[name*="email" i]'),
            ]:
                try:
                    if selector.count() > 0:
                        selector.first.fill(args.admin_email)
                        log.info("Prefilled email field")
                        break
                except Exception:
                    continue

        log.info("Waiting for login completion (expects test id: app-shell). Complete OTP flow in the browser.")
        expect(page.get_by_test_id("app-shell")).to_be_visible(timeout=args.timeout_ms)

        log.info("Login detected; saving storage state to %s", out_path)
        context.storage_state(path=str(out_path))
        context.close()
        browser.close()

    log.info("Saved storage state to: %s", out_path)


if __name__ == "__main__":
    main()

