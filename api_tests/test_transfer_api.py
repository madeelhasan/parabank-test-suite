"""Performs a transfer through the UI, then verifies the balance change via
the REST API — the hybrid pattern this suite is built to demonstrate."""
import pytest

from pages.transfer_funds_page import TransferFundsPage

AMOUNT = 1.00


def test_transfer_updates_balances_on_both_accounts(logged_in_page, funded_account_ids, api_client):
    from_id, to_id = funded_account_ids
    from_before = api_client.get_account(from_id).json()["balance"]
    to_before = api_client.get_account(to_id).json()["balance"]

    transfer_page = TransferFundsPage(logged_in_page).navigate()
    transfer_page.transfer(f"{AMOUNT:.2f}", from_id, to_id)
    transfer_page.expect_transfer_complete()

    from_after = api_client.get_account(from_id).json()["balance"]
    to_after = api_client.get_account(to_id).json()["balance"]

    assert from_after == pytest.approx(from_before - AMOUNT, abs=0.01)
    assert to_after == pytest.approx(to_before + AMOUNT, abs=0.01)
