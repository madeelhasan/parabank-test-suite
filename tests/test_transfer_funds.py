from pages.transfer_funds_page import TransferFundsPage


def test_transfer_between_own_accounts_succeeds(logged_in_page, funded_account_ids):
    from_id, to_id = funded_account_ids

    transfer_page = TransferFundsPage(logged_in_page).navigate()
    transfer_page.transfer("1.00", from_id, to_id)

    transfer_page.expect_transfer_complete()
    assert transfer_page.amount_result.inner_text() == "$1.00"
    assert transfer_page.from_account_result.inner_text() == from_id
    assert transfer_page.to_account_result.inner_text() == to_id
