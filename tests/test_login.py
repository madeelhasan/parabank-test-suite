from pages.accounts_overview_page import AccountsOverviewPage
from pages.login_page import LoginPage


def test_valid_credentials_land_on_accounts_overview(page, credentials):
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])

    AccountsOverviewPage(page).expect_loaded()
    assert "overview.htm" in page.url


def test_invalid_credentials_show_an_error(page):
    login_page = LoginPage(page).navigate()
    login_page.login("invalid_user_1234", "wrong-password")

    login_page.expect_login_error()
    assert "overview.htm" not in page.url
