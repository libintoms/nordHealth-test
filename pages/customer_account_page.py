import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.messages import click_and_capture_alert


class CustomerAccountPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.logout_button = self.page.get_by_role("button", name="Logout")
        self.transactions_button = self.page.get_by_role("button", name="Transactions")
        self.deposit_button = self.page.get_by_role("button", name="Deposit")
        self.withdrawl_button = self.page.get_by_role("button", name="Withdrawl")
        self.welcome_label = self.page.locator("span.fontBig.ng-binding")
        self.account_number_value = self.page.locator(".center strong").nth(0)
        self.balance_value = self.page.locator(".center strong").nth(1)
        self.currency_value = self.page.locator(".center strong").nth(2)
        self.message_label = self.page.locator(".error:visible, .center .ng-binding:visible").last
        self.status_message = self.page.locator("span.error:visible")
        self.deposit_tab_button = self.page.locator("button[ng-click='deposit()']")
        self.withdraw_tab_button = self.page.locator("button[ng-click='withdrawl()']")
        self.transactions_tab_button = self.page.locator("button[ng-click='transactions()']")
        self.deposit_amount_input = self.page.locator("form[ng-submit='deposit()'] input[ng-model='amount']")
        self.withdraw_amount_input = self.page.locator(
            "form[ng-submit='withdrawl()'] input[ng-model='amount']"
        )
        self.deposit_submit_button = self.page.locator("form[ng-submit='deposit()'] button[type='submit']")
        self.withdraw_submit_button = self.page.locator(
            "form[ng-submit='withdrawl()'] button[type='submit']"
        )

    def assert_logged_in(self, customer_name: str) -> None:
        expect(self.logout_button).to_be_visible()
        expect(self.transactions_button).to_be_visible()
        expect(self.deposit_button).to_be_visible()
        expect(self.withdrawl_button).to_be_visible()
        expect(self.welcome_label).to_contain_text(customer_name)

    def current_balance(self) -> int:
        raw = (self.balance_value.text_content() or "0").strip()
        digits = re.sub(r"[^\d-]", "", raw) or "0"
        return int(digits)

    def click_deposit_tab(self) -> None:
        self.deposit_tab_button.click()

    def click_withdraw_tab(self) -> None:
        self.withdraw_tab_button.click()

    def click_transactions_tab(self) -> None:
        self.transactions_tab_button.click()

    def deposit(self, amount: int) -> str:
        before = self.current_balance()
        self.click_deposit_tab()
        self.deposit_amount_input.fill(str(amount))
        alert_message = click_and_capture_alert(self.page, lambda: self.deposit_submit_button.click())
        if alert_message:
            expect(self.balance_value).to_have_text(str(before + amount))
            return alert_message.strip()
        expect(self.status_message).to_be_visible()
        expect(self.balance_value).to_have_text(str(before + amount))
        return (self.status_message.text_content() or "").strip()

    def withdraw(self, amount: int) -> str:
        before = self.current_balance()
        self.click_withdraw_tab()
        self.withdraw_amount_input.fill(str(amount))
        alert_message = click_and_capture_alert(self.page, lambda: self.withdraw_submit_button.click())
        if alert_message:
            expect(self.balance_value).to_have_text(str(before - amount))
            return alert_message.strip()
        expect(self.status_message).to_be_visible()
        if "success" in (self.status_message.text_content() or "").lower():
            expect(self.balance_value).to_have_text(str(before - amount))
        return (self.status_message.text_content() or "").strip()
