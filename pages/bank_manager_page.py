from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.messages import click_and_capture_alert


class BankManagerPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.add_customer_tab = self.page.locator("button[ng-click='addCust()']")
        self.open_account_tab = self.page.locator("button[ng-click='openAccount()']")
        self.customers_tab = self.page.locator("button[ng-click='showCust()']")
        self.first_name_input = self.page.locator("input[ng-model='fName']")
        self.last_name_input = self.page.locator("input[ng-model='lName']")
        self.post_code_input = self.page.locator("input[ng-model='postCd']")
        self.add_customer_submit_button = self.page.locator(
            "form[ng-submit='addCustomer()'] button[type='submit']"
        )
        self.user_select = self.page.locator("#userSelect")
        self.currency_select = self.page.locator("#currency")
        self.process_account_button = self.page.locator("form[ng-submit='process()'] button[type='submit']")
        self.inline_message = self.page.locator("span.error:visible").first
        self.customer_search_input = self.page.locator("input[ng-model='searchCustomer']")
        self.customer_rows_table = self.page.locator("table tbody tr")

    def assert_loaded(self) -> None:
        expect(self.add_customer_tab).to_be_visible()
        expect(self.open_account_tab).to_be_visible()
        expect(self.customers_tab).to_be_visible()

    def go_to_add_customer(self) -> None:
        self.add_customer_tab.click()

    def go_to_open_account(self) -> None:
        self.open_account_tab.click()

    def go_to_customers(self) -> None:
        self.customers_tab.click()

    def add_customer(self, first_name: str, last_name: str, post_code: str) -> str:
        self.go_to_add_customer()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.post_code_input.fill(post_code)
        message = click_and_capture_alert(
            self.page,
            lambda: self.add_customer_submit_button.click(),
        )
        if message:
            return message
        # App normally uses alert(); keep a fallback for flaky browser runs.
        if self.inline_message.count():
            return (self.inline_message.text_content() or "").strip()
        return ""

    def open_account(self, customer_name: str, currency: str = "Dollar") -> str:
        self.go_to_open_account()
        self.user_select.select_option(label=customer_name)
        self.currency_select.select_option(label=currency)
        message = click_and_capture_alert(
            self.page,
            lambda: self.process_account_button.click(),
        )
        if message:
            return message
        if self.inline_message.count():
            return (self.inline_message.text_content() or "").strip()
        return ""

    def search_customer(self, text: str) -> None:
        self.go_to_customers()
        self.customer_search_input.fill(text)

    def clear_customer_search(self) -> None:
        self.customer_search_input.fill("")

    def customer_rows(self):
        return self.customer_rows_table

    def row_for_customer(self, first_name: str, last_name: str):
        return self.customer_rows_table.filter(has_text=first_name).filter(has_text=last_name)

    def customer_exists(self, first_name: str, last_name: str) -> bool:
        self.go_to_customers()
        self.page.wait_for_timeout(200)
        return self.row_for_customer(first_name, last_name).count() > 0

    def delete_customer(self, first_name: str, last_name: str) -> None:
        self.go_to_customers()
        row = self.row_for_customer(first_name, last_name)
        expect(row).to_have_count(1)
        row.get_by_role("button", name="Delete").click()
        expect(row).to_have_count(0)
