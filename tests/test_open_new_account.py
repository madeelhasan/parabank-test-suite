from pages.accounts_overview_page import AccountsOverviewPage
from pages.open_account_page import OpenAccountPage


def test_open_new_savings_account(logged_in_page, funded_account_ids):
    from_id, _ = funded_account_ids

    open_account_page = OpenAccountPage(logged_in_page).navigate()
    new_account_id = open_account_page.open_account(OpenAccountPage.SAVINGS, from_id)

    assert new_account_id.isdigit()

    overview = AccountsOverviewPage(logged_in_page).navigate()
    assert new_account_id in overview.get_account_ids()
