# Mata Health QA Automation Framework

## Application Under Test
https://nimble-pasca-24ee4c.netlify.app/

## Tech Stack
Python
Playwright
Pytest

## Framework Architecture
framework/
   pages/
   locators/
   fixtures/
   services/
   utils/

tests/
   smoke/

## Features
Page Object Model
Reusable Fixtures
Environment Configuration
JSON Test Data
Smoke Test Suite

## Run Tests
pytest

## Run Smoke Suite
pytest tests/smoke

## Generate Playwright Report
pytest --html=report.html
