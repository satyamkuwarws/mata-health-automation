## Mata Health UI Automation (Playwright + pytest)

Production-ready UI automation framework for a healthcare admin portal using:
- Python 3.11+
- Playwright **sync API**
- pytest

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

4) Run smoke tests:

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

