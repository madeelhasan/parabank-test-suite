"""
Shared fixtures for both the UI suite (/tests) and the API suite (/api_tests).

ParaBank's public demo is shared by everyone who tests against it, so account
balances drift constantly. Rather than hardcoding account IDs, `funded_account_ids`
picks accounts dynamically via the REST API so mutating flows (transfer, bill pay,
open account) don't fail just because someone else drained the first account.
"""
import os

import pytest

from api_tests.api_client import ParaBankApiClient
from pages.login_page import LoginPage

BASE_URL = os.getenv("PARABANK_BASE_URL", "https://parabank.parasoft.com/parabank/")
USERNAME = os.getenv("PARABANK_USERNAME", "john")
PASSWORD = os.getenv("PARABANK_PASSWORD", "demo")


@pytest.fixture(scope="session")
def base_url():
    """Overrides pytest-playwright's base_url fixture so every POM can call
    page.goto("/some.htm") without hardcoding the host."""
    return BASE_URL


@pytest.fixture(scope="session")
def credentials():
    return {"username": USERNAME, "password": PASSWORD}


@pytest.fixture(scope="session")
def api_client():
    return ParaBankApiClient(BASE_URL)


@pytest.fixture(scope="session")
def customer_id(api_client, credentials):
    response = api_client.login(credentials["username"], credentials["password"])
    response.raise_for_status()
    return response.json()["id"]


@pytest.fixture
def logged_in_page(page, credentials):
    """A Playwright page that has already completed the UI login flow."""
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])
    return page


@pytest.fixture
def funded_account_ids(api_client, customer_id):
    """(from_id, to_id) chosen by current balance, highest first, so the
    "from" account always clears ParaBank's minimum-balance checks."""
    accounts = api_client.get_customer_accounts(customer_id).json()
    by_balance = sorted(accounts, key=lambda acc: acc["balance"], reverse=True)
    from_account = by_balance[0]
    to_account = next(acc for acc in by_balance[1:] if acc["id"] != from_account["id"])
    return str(from_account["id"]), str(to_account["id"])
