from playwright.sync_api import Page, expect


class OpenAccountPage:
    """Page Object for the Open New Account page (openaccount.htm)."""

    URL = "openaccount.htm"
    CHECKING = "0"
    SAVINGS = "1"

    def __init__(self, page: Page):
        self.page = page
        self.account_type_select = page.locator("#type")
        self.from_account_select = page.locator("#fromAccountId")
        self.open_account_button = page.locator("input[value='Open New Account']")
        self.result_panel = page.locator("#openAccountResult")
        self.new_account_link = page.locator("#newAccountId")

    def navigate(self) -> "OpenAccountPage":
        self.page.goto(self.URL)
        # The "transfer from" dropdown is populated asynchronously from the
        # accounts REST endpoint, so wait for it before selecting an option.
        # state="attached" because a closed <select>'s <option>s never count
        # as "visible" to Playwright's actionability checks.
        self.page.wait_for_selector("#fromAccountId option", state="attached")
        return self

    def open_account(self, account_type: str, from_account_id: str) -> str:
        """Submits the form and returns the newly created account id."""
        self.account_type_select.select_option(account_type)
        self.from_account_select.select_option(from_account_id)
        self.open_account_button.click()
        self.expect_account_opened()
        return self.new_account_link.inner_text()

    def expect_account_opened(self) -> "OpenAccountPage":
        expect(self.result_panel).to_be_visible()
        expect(self.new_account_link).not_to_have_text("")
        return self
