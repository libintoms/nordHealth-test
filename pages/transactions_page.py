from playwright.sync_api import expect

from pages.base_page import BasePage


class TransactionsPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.rows = self.page.locator("table tbody tr")
        self.back_button = self.page.get_by_role("button", name="Back")
        self.reset_button = self.page.get_by_role("button", name="Reset")

    def assert_loaded(self) -> None:
        expect(self.back_button).to_be_visible()
        expect(self.reset_button).to_be_visible()

    def row_texts(self) -> list[str]:
        items: list[str] = []
        for i in range(self.rows.count()):
            items.append((self.rows.nth(i).text_content() or "").strip())
        return items

    def reset(self) -> None:
        self.reset_button.click()

    def go_back(self) -> None:
        self.back_button.click()
