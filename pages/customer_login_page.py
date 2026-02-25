from playwright.sync_api import expect

from pages.base_page import BasePage


class CustomerLoginPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.name_label = self.page.get_by_text("Your Name :", exact=False)
        self.user_select = self.page.locator("#userSelect")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.login_submit_button = self.page.locator("form[ng-submit='showAccount()'] button[type='submit']")

    def assert_loaded(self) -> None:
        expect(self.name_label).to_be_visible()
        expect(self.user_select).to_be_visible()
        # Login stays hidden until a customer is selected.
        expect(self.login_submit_button).to_have_text("Login")

    def select_customer(self, full_name: str) -> None:
        self.user_select.select_option(label=full_name)

    def login_as(self, full_name: str) -> None:
        self.select_customer(full_name)
        self.login_button.click()

    def customer_names(self) -> list[str]:
        options = self.user_select.locator("option")
        names: list[str] = []
        for i in range(options.count()):
            text = " ".join((options.nth(i).text_content() or "").split())
            if text and text != "---Your Name---":
                names.append(text)
        return names
