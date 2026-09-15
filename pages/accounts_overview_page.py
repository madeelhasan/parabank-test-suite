from playwright.sync_api import Page, expect


class AccountsOverviewPage:
    """Page Object for the Accounts Overview page (overview.htm)."""

    URL = "overview.htm"

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.locator("#showOverview h1.title")
        self.account_id_links = page.locator("#accountTable tbody td:first-child a")

    def navigate(self) -> "AccountsOverviewPage":
        self.page.goto(self.URL)
        self.page.wait_for_selector("#accountTable tbody td a")
        return self

    def expect_loaded(self) -> "AccountsOverviewPage":
        expect(self.heading).to_have_text("Accounts Overview")
        return self

    def get_account_ids(self) -> list[str]:
        """Every account id shown in the table (the "Total" row has no link, so
        it is naturally excluded)."""
        return self.account_id_links.all_inner_texts()
