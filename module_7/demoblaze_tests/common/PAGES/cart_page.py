from demoblaze_tests.common.PAGES.main_page import MainPage
from demoblaze_tests.common.locators import CartPageLocators as cart


class CartPage(MainPage):

    def should_be_added_in_cart(self, name: str, price: int):
        """Verifies that product is added to cart
        Arguments:
        name - expected product name
        price - expected product price"""
        assert self.is_element_present(
            *cart.cart_added_product_name
        ), "Product name element not found in the cart"
        actual_name = self.browser.find_element(*cart.cart_added_product_name).text
        assert (
            name == actual_name
        ), f"Expected cart to have product with name: {name} , got {actual_name} instead"
        price_text = self.browser.find_element(*cart.cart_added_product_price).text
        actual_price = self.get_price(price_text)
        assert (
            price == actual_price
        ), f"Expected cart to have product with price: {price}, got {actual_price} instead"

    def check_total(self, expected: int):
        """Verifies cart total
        Arguments
        expected - expected total"""
        actual_total_text = self.browser.find_element(*cart.cart_total).text
        actual_total = self.get_price(actual_total_text)
        assert (
            expected == actual_total
        ), f"Expected cart total to be {expected}, got {actual_total} instead"
