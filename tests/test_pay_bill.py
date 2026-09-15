from pages.bill_pay_page import BillPayPage


def test_pay_bill_from_existing_account(logged_in_page, funded_account_ids):
    from_id, _ = funded_account_ids

    bill_pay_page = BillPayPage(logged_in_page).navigate()
    bill_pay_page.pay_bill(
        payee_name="Acme Utilities",
        street="1 Infinite Loop",
        city="Cupertino",
        state="CA",
        zip_code="95014",
        phone="4085551234",
        account_number="999999999",
        amount="15.00",
        from_account_id=from_id,
    )

    bill_pay_page.expect_payment_complete()
