from playwright.sync_api import Page, expect


class BillPayPage:
    """Page Object for the Bill Pay page (billpay.htm)."""

    URL = "billpay.htm"

    def __init__(self, page: Page):
        self.page = page
        self.payee_name = page.locator("input[name='payee.name']")
        self.payee_street = page.locator("input[name='payee.address.street']")
        self.payee_city = page.locator("input[name='payee.address.city']")
        self.payee_state = page.locator("input[name='payee.address.state']")
        self.payee_zip = page.locator("input[name='payee.address.zipCode']")
        self.payee_phone = page.locator("input[name='payee.phoneNumber']")
        self.payee_account_number = page.locator("input[name='payee.accountNumber']")
        self.verify_account_number = page.locator("input[name='verifyAccount']")
        self.amount_input = page.locator("input[name='amount']")
        self.from_account_select = page.locator("select[name='fromAccountId']")
        self.send_payment_button = page.locator("input[value='Send Payment']")
        self.result_panel = page.locator("#billpayResult")

    def navigate(self) -> "BillPayPage":
        self.page.goto(self.URL)
        return self

    def pay_bill(
        self,
        *,
        payee_name: str,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        phone: str,
        account_number: str,
        amount: str,
        from_account_id: str,
    ) -> "BillPayPage":
        self.payee_name.fill(payee_name)
        self.payee_street.fill(street)
        self.payee_city.fill(city)
        self.payee_state.fill(state)
        self.payee_zip.fill(zip_code)
        self.payee_phone.fill(phone)
        self.payee_account_number.fill(account_number)
        self.verify_account_number.fill(account_number)
        self.amount_input.fill(amount)
        self.from_account_select.select_option(from_account_id)
        self.send_payment_button.click()
        return self

    def expect_payment_complete(self) -> "BillPayPage":
        expect(self.result_panel).to_be_visible()
        expect(self.result_panel).to_contain_text("was successful")
        return self
