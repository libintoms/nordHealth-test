from pathlib import Path

import pytest

from pages.bank_manager_page import BankManagerPage
from pages.customer_account_page import CustomerAccountPage
from pages.customer_login_page import CustomerLoginPage
from pages.home_page import HomePage
from utils.helpers import full_name, unique_customer


def pytest_configure(config):
    Path("reports").mkdir(exist_ok=True)
    Path("test-results").mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def tune_page_timeouts(page):
    page.set_default_timeout(15000)
    page.set_default_navigation_timeout(30000)


@pytest.fixture
def home(page):
    view = HomePage(page)
    view.open()
    return view


@pytest.fixture
def manager_page(home):
    home.go_to_bank_manager_login()
    manager = BankManagerPage(home.page)
    manager.assert_loaded()
    return manager


@pytest.fixture
def customer_login_page(home):
    home.go_to_customer_login()
    login = CustomerLoginPage(home.page)
    login.assert_loaded()
    return login


@pytest.fixture
def provisioned_customer(page):
    home = HomePage(page)
    home.open()
    home.go_to_bank_manager_login()
    manager = BankManagerPage(page)
    manager.assert_loaded()

    customer = unique_customer()
    message = manager.add_customer(
        customer["first_name"], customer["last_name"], customer["post_code"]
    )
    customer["add_customer_alert"] = message
    customer["name"] = full_name(customer["first_name"], customer["last_name"])
    account_message = manager.open_account(customer["name"], "Dollar")
    customer["open_account_alert"] = account_message
    return customer


@pytest.fixture
def logged_in_customer(page, provisioned_customer):
    home = HomePage(page)
    home.open()
    home.go_to_customer_login()
    login = CustomerLoginPage(page)
    login.login_as(provisioned_customer["name"])
    account = CustomerAccountPage(page)
    account.assert_logged_in(provisioned_customer["first_name"])
    return {"account": account, "customer": provisioned_customer}
