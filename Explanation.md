# Automation Submission Notes

## 1. Code + Brief Explanation of My Approach

### What I built

I implemented an end-to-end UI automation suite for the XYZ Bank demo app using:

- Python
- `pytest`
- `pytest-playwright` (Playwright browser automation with pytest integration)

The suite covers both key user roles:

- **Customer flow** (`tests/test_customer_flow.py`)
- **Bank Manager flow** (`tests/test_bank_manager_flow.py`)

### Approach (high level)

I used a **Page Object Model (POM)** approach to keep the tests readable and maintainable:

- `pages/` contains page classes and UI actions/assertions
- `tests/` contains business-flow test cases
- `tests/conftest.py` contains reusable fixtures and setup
- `utils/` contains reusable helpers (for example unique test data generation and alert handling)

This lets the tests read like business scenarios while UI selectors and interaction details stay centralized in page classes.

### Why this approach

- Improves maintainability when UI selectors change
- Reduces duplication across tests
- Makes tests easier to review (test intent is clearer than low-level UI code)
- Supports scaling the suite with new pages/flows over time

### Test design choices

- I used **fixtures** in `tests/conftest.py` to create reusable setup for:
  - home page
  - manager page
  - customer login page
  - provisioned/logged-in customer
- I generated **unique customer data** (`utils/helpers.py`) to reduce collisions and improve repeatability for CRUD scenarios.
- I added **basic resilience** in manager actions by capturing application alert messages and keeping a fallback path for inline messages if alerts are not available in a flaky run.

### What is validated

Customer-side examples:

- customer list is populated
- login works for a seeded customer
- account dashboard shows core account details
- deposit updates balance
- withdrawal updates balance
- transaction history shows both credit and debit entries

Manager-side examples:

- manager login/dashboard loads
- add customer
- open account for existing customer
- customer search/filter
- delete customer from customers table

## 2. How This Showcases My Automation Skills / Experience

This task demonstrates the following automation capabilities:

### Framework and architecture

- Designed a **structured automation framework** (POM + fixtures + utilities) instead of writing all logic directly in tests
- Separated concerns between:
  - test intent
  - page interactions/selectors
  - data generation/helpers

### Reliability and repeatability

- Added shared page timeout tuning in `tests/conftest.py`
- Used generated test data to avoid brittle dependencies on static records for manager CRUD tests
- Wrote assertions against both UI visibility/state and business outcomes (balance updates, transaction rows, success messages)

### Maintainability and developer experience

- Added `Makefile` commands for common workflows (`install`, `browsers`, `test`, `test-headed`, `test-ui`, `report`)
- Configured `pytest.ini` for:
  - HTML reporting
  - Playwright tracing
  - test output foldering
  - consistent browser execution defaults

### Debuggability and reporting

- Enabled **Playwright tracing** (`test-results/`) for post-failure analysis
- Enabled **HTML reports** (`reports/report.html`) for easy result sharing/review
- Added an interactive/debug workflow (`make test-ui`) using `PWDEBUG`

### Code quality workflow

- Added Node-based tooling (`package.json`) for:
  - Prettier formatting
  - ESLint checks
  - Husky pre-commit hooks
- This helps enforce consistency before code is committed

## Reviewer Notes

- The implementation is intentionally organized for readability and extensibility, not just to pass a small set of checks.
- If needed, I can extend this suite next with:
  - negative scenarios (invalid customer, insufficient funds)
  - cross-browser execution
  - CI pipeline integration
  - test markers/smoke-regression grouping
