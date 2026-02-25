from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.title_label = self.page.get_by_text("XYZ Bank", exact=False)
        self.home_button = self.page.get_by_role("button", name="Home")
        self.customer_login_button = self.page.get_by_role("button", name="Customer Login")
        self.bank_manager_login_button = self.page.get_by_role("button", name="Bank Manager Login")

    def open(self) -> None:
        self.page.goto("/angularJs-protractor/BankingProject/#/login", wait_until="domcontentloaded")

    def assert_loaded(self) -> None:
        expect(self.title_label).to_be_visible()
        expect(self.customer_login_button).to_be_visible()
        expect(self.bank_manager_login_button).to_be_visible()

    def go_to_customer_login(self) -> None:
        self.customer_login_button.click()

    def go_to_bank_manager_login(self) -> None:
        self.bank_manager_login_button.click()
