## Mata Health UI Automation (Playwright + pytest)

Production-ready UI automation framework for a healthcare admin portal using:
- Python 3.11+
- Playwright **sync API**
- pytest

### Application Under Test

- Base app: `https://nimble-pasca-24ee4c.netlify.app/`
- Admin portal base URL (default): `https://nimble-pasca-24ee4c.netlify.app/admin` (configured via `BASE_URL`)

### Framework architecture

```text
framework/
  config/
  pages/
  locators/
  fixtures/
  services/
  utilities/
  factories/

tests/
  smoke/

test_data/
  smoke/
```

### Features

- Page Object Model
- Reusable pytest fixtures (incl. storage-state login reuse)
- Environment configuration via `.env`
- JSON test data
- Smoke test suite
- Artifacts on failure (screenshot, trace, video) + optional Allure attachments

### Quick start

1) Create and activate a virtualenv (Python 3.11+)

2) Install dependencies:

```bash
pip install -U pip
pip install -e ".[dev]"
playwright install --with-deps chromium
```

3) Create your env file:

```bash
cp .env.example .env
```

4) Run tests:

```bash
pytest
```

5) Run smoke tests (parallel):

```bash
pytest -m smoke --headed false --browser chromium -n auto
```

### Reporting

- Allure:

```bash
pytest --alluredir reports/allure-results
allure serve reports/allure-results
```

- pytest-html fallback:

```bash
pytest --html=reports/pytest-html/report.html --self-contained-html
```
