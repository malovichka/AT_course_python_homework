import time
from demoblaze_tests.common.PAGES.main_page import MainPage
from demoblaze_tests.common.PAGES.category_page import CategoryPage
from demoblaze_tests.common.PAGES.product_page import ProductPage
from demoblaze_tests.common.PAGES.cart_page import CartPage
from demoblaze_tests.common.constants import BASE_URL, CATEGORIES
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver import Chrome


def test_log_in_for_registered_user(
    user_creds: tuple[str, str], test_browser: "Chrome"
):
    """Test verifies that registered user can log in.
    Arguments:
    user_creds - login and password of registered user
    test_browser - new browser window"""
    page = MainPage(test_browser, BASE_URL)
    page.open()
    page.login_user(user_creds)
    page.should_be_logged_in(user_creds[0])
    page.logout_user()


def test_logged_in_user_adds_product_to_cart(logged_in_user_page: MainPage):
    """Test verifies that loggen in user can add product to cart.
    Arguments:
    logged_in_user_page - browser window where user already logged in"""
    page = logged_in_user_page
    page.go_to_category(CATEGORIES[-1])
    monitors_page = CategoryPage(page.browser, page.browser.current_url)
    # we cannot determine if the product list was rerendered, no correct locators, sleep is a must
    time.sleep(2)
    monitor_data = monitors_page.find_highest_price_product()
    monitors_page.go_to_product_page(monitor_data["product_locator"])
    product_page = ProductPage(page.browser, page.browser.current_url)
    product_page.should_be_correct_product_page(
        name=monitor_data["name"], price=monitor_data["price"]
    )
    product_page.add_to_cart()
    product_page.go_to_cart()
    cart_page = CartPage(page.browser, page.browser.current_url)
    cart_page.should_be_added_in_cart(
        name=monitor_data["name"], price=monitor_data["price"]
    )
    cart_page.check_total(expected=monitor_data["price"])
