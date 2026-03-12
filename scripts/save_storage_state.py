from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description="Save Playwright storage-state after manual login.")
    parser.add_argument("--base-url", required=True, help="Admin base url, e.g. https://.../admin")
    parser.add_argument("--out", required=True, help="Where to write storage state json")
    parser.add_argument("--timeout-ms", type=int, default=180_000, help="Max time to wait for login")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(base_url=args.base_url)
        page = context.new_page()

        # Open the admin app and let the user complete login manually.
        page.goto(args.base_url, wait_until="domcontentloaded")

        # The framework uses this as the logged-in signal.
        expect(page.get_by_test_id("app-shell")).to_be_visible(timeout=args.timeout_ms)

        context.storage_state(path=str(out_path))
        context.close()
        browser.close()

    print(f"Saved storage state to: {out_path}")


if __name__ == "__main__":
    main()

