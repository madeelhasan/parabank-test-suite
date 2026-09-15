"""Pays a bill through the UI, then verifies the resulting debit transaction
via the REST API. There is no dedicated bill-pay REST resource, so the
transactions list is the source of truth."""
from pages.bill_pay_page import BillPayPage

AMOUNT = "12.34"


def test_bill_payment_creates_debit_transaction(logged_in_page, funded_account_ids, api_client):
    from_id, _ = funded_account_ids
    transactions_before = api_client.get_transactions(from_id).json()

    bill_pay_page = BillPayPage(logged_in_page).navigate()
    bill_pay_page.pay_bill(
        payee_name="Acme Utilities",
        street="1 Infinite Loop",
        city="Cupertino",
        state="CA",
        zip_code="95014",
        phone="4085551234",
        account_number="888888888",
        amount=AMOUNT,
        from_account_id=from_id,
    )
    bill_pay_page.expect_payment_complete()

    transactions_after = api_client.get_transactions(from_id).json()
    assert len(transactions_after) == len(transactions_before) + 1

    newest = max(transactions_after, key=lambda t: t["id"])
    assert newest["type"] == "Debit"
    assert newest["amount"] == float(AMOUNT)
