from playwright.sync_api import Page, expect


class TransferFundsPage:
    """Page Object for the Transfer Funds page (transfer.htm)."""

    URL = "transfer.htm"

    def __init__(self, page: Page):
        self.page = page
        self.amount_input = page.locator("#amount")
        self.from_account_select = page.locator("#fromAccountId")
        self.to_account_select = page.locator("#toAccountId")
        self.transfer_button = page.locator("#transferForm input[type='submit']")
        self.result_panel = page.locator("#showResult")
        self.amount_result = page.locator("#amountResult")
        self.from_account_result = page.locator("#fromAccountIdResult")
        self.to_account_result = page.locator("#toAccountIdResult")

    def navigate(self) -> "TransferFundsPage":
        self.page.goto(self.URL)
        # The from/to dropdowns are populated asynchronously from the accounts
        # REST endpoint, so wait for the options rather than racing the fill().
        # state="attached" (not the default "visible") because Playwright
        # never considers a closed <select>'s <option> elements visible.
        self.page.wait_for_selector("#fromAccountId option", state="attached")
        self.page.wait_for_selector("#toAccountId option", state="attached")
        return self

    def transfer(self, amount: str, from_account_id: str, to_account_id: str) -> "TransferFundsPage":
        self.amount_input.fill(amount)
        self.from_account_select.select_option(from_account_id)
        self.to_account_select.select_option(to_account_id)
        self.transfer_button.click()
        return self

    def expect_transfer_complete(self) -> "TransferFundsPage":
        expect(self.result_panel).to_be_visible()
        expect(self.result_panel.locator("h1")).to_have_text("Transfer Complete!")
        return self
