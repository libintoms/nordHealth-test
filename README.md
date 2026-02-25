# Python Playwright Tests (XYZ Bank Demo)

This project contains a Python `pytest-playwright` test suite for:

`https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login`

## Project Structure

- `pages/` Page Object Model classes for app screens
- `utils/` shared helper functions and test data builders
- `tests/` pytest test files and fixtures
- `reports/` generated HTML report output (created at runtime)
- `test-results/` Playwright traces and artifacts (created at runtime)

## Prerequisites

- Python 3.10+ (tested here with Python 3.14)

## Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

3. Install Playwright browser binaries (Chromium only):

```bash
.venv/bin/python -m playwright install chromium
```

## Run Tests

Run all tests:

```bash
.venv/bin/pytest
```

Run with the included `Makefile` shortcuts:

```bash
make install
make browsers
make test
```

Run headed mode:

```bash
make test-headed
```

Run in interactive UI/debug mode (Python equivalent):

```bash
make test-ui
```

This uses `PWDEBUG=1` with headed mode and `slowmo` so you can watch and inspect the test flow.

Open the latest HTML report:

```bash
make report
```

## Reporting and Traces

- HTML report is generated at `reports/report.html`
- Terminal list output is enabled via `-v` in `pytest.ini`
- Playwright tracing is enabled (`--tracing on`) and artifacts are written to `test-results/`

Note: the HTML report is generated only; it is not auto-opened.

## Code Quality and Pre-commit Hooks

This project uses the following tools to ensure code quality and consistency:

- **Prettier**: For automatic code formatting. Run `npm run format` to format all files, or `npm run format:check` to check formatting.
- **ESLint**: For JavaScript/TypeScript linting. Run `npm run lint` to check for lint errors.
- **Husky**: Git hooks manager. A pre-commit hook is set up to automatically run Prettier (check) and ESLint before each commit. This prevents commits with formatting or lint errors.

### How the Pre-commit Hook Works

On every `git commit`, Husky will:

1. Run `npm run format:check` to ensure code is formatted with Prettier.
2. Run `npm run lint` to ensure there are no lint errors.
3. If either step fails, the commit will be aborted.

You can find the hook script in `.husky/pre-commit`.

---

## Notes

- This is a Python Playwright project, so there is no `playwright.config.ts`
- Python configuration is handled through `pytest.ini` and fixtures in `tests/conftest.py`
- Python `pytest-playwright` does not have the Node Playwright Test "UI Mode"; `make test-ui` is the closest interactive workflow
