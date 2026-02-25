from pages.customer_account_page import CustomerAccountPage
from pages.transactions_page import TransactionsPage


def test_customer_login_page_lists_seed_customers(customer_login_page):
    names = customer_login_page.customer_names()
    assert "Harry Potter" in names
    assert any(name in names for name in ["Hermoine Granger", "Hermione Granger"])


def test_customer_can_login_with_seed_customer(customer_login_page):
    customer_login_page.login_as("Harry Potter")
    account = CustomerAccountPage(customer_login_page.page)
    account.assert_logged_in("Harry Potter")


def test_customer_account_dashboard_shows_actions_and_account_details(logged_in_customer):
    account = logged_in_customer["account"]
    assert account.account_number_value.is_visible()
    assert account.balance_value.is_visible()
    assert account.currency_value.is_visible()


def test_customer_can_deposit_money_and_balance_updates(logged_in_customer):
    account = logged_in_customer["account"]
    starting_balance = account.current_balance()
    message = account.deposit(200)
    assert "deposit" in message.lower() and "success" in message.lower()
    assert account.current_balance() == starting_balance + 200


def test_customer_can_withdraw_valid_amount(logged_in_customer):
    account = logged_in_customer["account"]
    account.deposit(300)
    balance_after_deposit = account.current_balance()
    message = account.withdraw(120)
    assert "transaction" in message.lower() and "success" in message.lower()
    assert account.current_balance() == balance_after_deposit - 120


def test_customer_transactions_show_deposit_and_withdraw_entries(logged_in_customer):
    account = logged_in_customer["account"]
    account.deposit(250)
    account.withdraw(50)
    account.click_transactions_tab()

    transactions = TransactionsPage(account.page)
    transactions.assert_loaded()
    rows = transactions.row_texts()
    joined = " ".join(rows)

    assert "250" in joined
    assert "50" in joined
    assert "Credit" in joined
    assert "Debit" in joined
