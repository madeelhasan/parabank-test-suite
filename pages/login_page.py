from playwright.sync_api import Page, expect

DEFAULT_ERROR = "The username and password could not be verified."


class LoginPage:
    """Page Object for the ParaBank login form (index.htm)."""

    URL = "index.htm"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("input[value='Log In']")
        self.error_message = page.locator("p.error")

    def navigate(self) -> "LoginPage":
        self.page.goto(self.URL)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def expect_login_error(self, message: str = DEFAULT_ERROR) -> None:
        expect(self.error_message).to_have_text(message)
