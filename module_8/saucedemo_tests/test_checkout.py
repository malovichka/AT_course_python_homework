import pytest
from saucedemo_tests.common.pages.checkout_page import CheckoutPage
from saucedemo_tests.common.pages.inventory_page import InventoryPage
from saucedemo_tests.common.locators import InventoryPageLocators as inv, CheckoutPageLocators as co
from saucedemo_tests.common.pages.cart_page import CartPage
from saucedemo_tests.common.constants import CHECKOUT_ERROR_MESSAGES
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.common.by import By


@pytest.mark.parametrize("quantity", [(1), (2), (6)])  # up to 6
def test_add_items_and_checkout(logged_in_user_page: InventoryPage, quantity: int):
    page = logged_in_user_page
    added_products_data = []
    for i in range(quantity):
        item_data = page.get_item_data(inv, i)
        page.add_to_cart(item_data)
        added_products_data.append(item_data)

    page.should_have_items_in_cart_icon(quantity)
    page.go_to_cart()
    cart_page = CartPage(page.browser, page.browser.current_url)
    cart_page.should_be_on_cart_page()

    cart_total = 0
    for i in range(quantity):
        cart_page.should_exact_items_be_added(i, added_products_data[i])
        cart_total += added_products_data[i]["price"]
    cart_page.should_have_pieces_added(quantity)

    cart_page.go_to_checkout()
    first_checkout_page = CheckoutPage(page.browser, page.browser.current_url)
    first_checkout_page.should_be_on_first_checkout()
    first_checkout_page.enter_full_info()
    first_checkout_page.continue_checkout()
    second_checkout_page = CheckoutPage(page.browser, page.browser.current_url)
    second_checkout_page.should_be_on_second_checkout()

    for i in range(0, quantity):
        second_checkout_page.should_exact_items_be_added(i, added_products_data[i])
    second_checkout_page.should_have_pieces_added(quantity)
    second_checkout_page.should_be_item_total(cart_total)
    second_checkout_page.finish_checkout()
    second_checkout_page.should_be_completed_checkout()


@pytest.mark.parametrize(
    "provided_data, error_message",
    [
        ((co.first_name, co.last_name), CHECKOUT_ERROR_MESSAGES["missing zip"]),
        ((co.first_name, co.postcode), CHECKOUT_ERROR_MESSAGES["missing last name"]),
        ((co.last_name, co.postcode), CHECKOUT_ERROR_MESSAGES["missing first name"]),
    ],
)
def test_checkout_stops_when_missing_data(
    logged_in_user_page: InventoryPage,
    provided_data: tuple[tuple[type["By"], str], tuple[type["By"], str]],
    error_message: str,
):
    page = logged_in_user_page
    id = page.get_random_product_id()
    item_data = page.get_item_data(inv, id)
    page.add_to_cart(item_data)
    page.should_have_items_in_cart_icon(1)
    page.go_to_cart()
    cart_page = CartPage(page.browser, page.browser.current_url)
    cart_page.should_be_on_cart_page()
    cart_page.should_exact_items_be_added(id, item_data)
    cart_page.should_have_pieces_added(1)
    cart_page.go_to_checkout()
    first_checkout_page = CheckoutPage(page.browser, page.browser.current_url)
    first_checkout_page.should_be_on_first_checkout()
    first_checkout_page.enter_partial_info(provided_data)
    first_checkout_page.continue_checkout()
    first_checkout_page.should_be_failed_first_checkout(error_message)
    first_checkout_page.should_be_on_first_checkout()
