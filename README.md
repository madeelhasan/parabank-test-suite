# ParaBank Test Suite

A Python test automation portfolio project targeting the [ParaBank demo banking site](https://parabank.parasoft.com/parabank/index.htm). This is a portfolio project demonstrating AI-assisted test automation: every flow below is one I'd have tested by hand on a real banking app, rewritten as a maintainable, CI-driven suite.

## What this demonstrates

- **Page Object Model design** — each UI flow (`/pages`) is a small class that owns its locators and actions. Tests read like test cases, not scripts full of CSS selectors.
- **Hybrid UI + API testing** — `/api_tests` performs an action through the browser (e.g. a fund transfer) and then verifies the result by calling ParaBank's REST API directly. This is the same pattern used to catch bugs that only show up in the data layer, not the UI.
- **Resilient test data handling** — ParaBank's public demo is shared by everyone testing against it, so account balances drift constantly. Instead of hardcoding account IDs, fixtures in `conftest.py` pick accounts dynamically via the REST API (highest balance first) so tests don't fail just because another tester emptied the first account in the list.
- **CI/CD integration** — GitHub Actions runs the full suite headless on every push and PR, uploads Playwright traces/screenshots on failure, and publishes an Allure HTML report to GitHub Pages.

### Flows covered

| Flow | Page Object | UI test | API verification |
|---|---|---|---|
| Login (valid + invalid) | `pages/login_page.py` | `tests/test_login.py` | `api_tests/test_login_api.py` |
| Transfer funds | `pages/transfer_funds_page.py` | `tests/test_transfer_funds.py` | `api_tests/test_transfer_api.py` (balance delta) |
| Pay a bill | `pages/bill_pay_page.py` | `tests/test_pay_bill.py` | `api_tests/test_pay_bill_api.py` (debit transaction) |
| Open a new account | `pages/open_account_page.py` | `tests/test_open_new_account.py` | `api_tests/test_open_account_api.py` (account exists) |

Four flows, done completely, beat ten flows done halfway — this suite intentionally stays small.

## Project structure

```
pages/          Page Object classes (Playwright)
tests/          UI test files (pytest)
api_tests/      API tests + a thin requests-based ParaBank REST client
reports/        Allure results / HTML report output (git-ignored)
conftest.py     Shared fixtures: base URL, credentials, REST client, account selection
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install

pytest                           # runs both tests/ and api_tests/
pytest tests/                    # UI only
pytest api_tests/                # API only
pytest --headed                  # watch the browser while it runs
```

By default the suite runs against `https://parabank.parasoft.com/parabank` using ParaBank's seeded demo user (`john` / `demo`). Override either with environment variables:

```bash
export PARABANK_BASE_URL=https://parabank.parasoft.com/parabank
export PARABANK_USERNAME=john
export PARABANK_PASSWORD=demo
```

### Generating the Allure report locally

```bash
pytest                                             # writes results to reports/allure-results
allure serve reports/allure-results                # opens the report in your browser
# or, without the Allure CLI installed:
pip install allure-pytest && pytest --alluredir=reports/allure-results
```

(Requires the [Allure commandline](https://allurereport.org/docs/install/) tool for `allure serve`/`allure generate`.)

## How CI works

`.github/workflows/tests.yml` runs on every push and pull request:

1. Installs Python dependencies from `requirements.txt`.
2. Runs `playwright install --with-deps` to provision browsers on the runner.
3. Runs the full pytest suite headless with `--screenshot only-on-failure --tracing retain-on-failure`.
4. Generates the Allure HTML report and uploads it as a build artifact (always).
5. Uploads Playwright screenshots/traces as a build artifact when the run fails.
6. On pushes to `main`, publishes the Allure report to the `gh-pages` branch.

### Publishing the report via GitHub Pages

1. In the repo, go to **Settings → Pages** and set the source to the `gh-pages` branch (created automatically by the workflow's publish step after the first successful run on `main`).
2. Push to `main` — the workflow builds the Allure report and pushes it to `gh-pages`.
3. The live report is then available at `https://<your-username>.github.io/<repo-name>/`.
4. To inspect a failed run's Playwright trace instead, download the `playwright-failure-artifacts` artifact from the Actions run and open `trace.zip` with `playwright show-trace trace.zip`.

## A note on test data

This suite runs against a **shared public demo**, not a sandboxed environment — that's a deliberate tradeoff, not an oversight. `funded_account_ids` (in `conftest.py`) always picks the customer's best-funded account as the "from" account so transfers, bill payments, and new-account funding don't fail against an account someone else has drained. Small, fixed amounts ($1–$15) are used throughout to keep the demo data usable for the next person.
