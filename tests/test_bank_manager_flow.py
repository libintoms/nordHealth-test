from utils.helpers import unique_customer


def test_home_page_shows_primary_actions(home):
    home.assert_loaded()
    assert home.home_button.is_visible()


def test_bank_manager_login_lands_on_manager_dashboard(manager_page):
    manager_page.assert_loaded()


def test_manager_can_add_customer(manager_page):
    customer = unique_customer()
    alert_message = manager_page.add_customer(
        customer["first_name"], customer["last_name"], customer["post_code"]
    )
    assert "customer" in alert_message.lower() and "success" in alert_message.lower()


def test_manager_can_open_account_for_existing_customer(manager_page):
    alert_message = manager_page.open_account("Harry Potter", "Dollar")
    assert "account" in alert_message.lower() and "success" in alert_message.lower()


def test_manager_customers_search_filters_results(manager_page):
    customer = unique_customer()
    manager_page.add_customer(customer["first_name"], customer["last_name"], customer["post_code"])
    manager_page.search_customer(customer["first_name"])
    row = manager_page.row_for_customer(customer["first_name"], customer["last_name"])
    assert row.count() == 1


def test_manager_can_delete_customer_from_customers_table(manager_page):
    customer = unique_customer()
    manager_page.add_customer(customer["first_name"], customer["last_name"], customer["post_code"])
    manager_page.delete_customer(customer["first_name"], customer["last_name"])
    assert not manager_page.customer_exists(customer["first_name"], customer["last_name"])
