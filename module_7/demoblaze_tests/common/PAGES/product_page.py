from demoblaze_tests.common.PAGES.main_page import MainPage
from demoblaze_tests.common.locators import ProductPageLocators as p
from demoblaze_tests.common.constants import PRODUCT_ADDED_ALERT_MESSAGE


class ProductPage(MainPage):

    def should_be_correct_product_page(self, name: str, price: int):
        """Verifies that product page is opened for correct product
        Arguments:
        name - expected product name
        price - expected product price"""
        assert self.is_element_present(
            *p.name
        ), "Name of the product not found on ProductPage"
        actual_product_name = self.browser.find_element(*p.name).text
        assert (
            name == actual_product_name
        ), f"Expected product name {name}, got {actual_product_name} instead"

        assert self.is_element_present(
            *p.price
        ), "Price of the product not found on ProductPage"
        actual_price_text = self.browser.find_element(*p.price).text
        actual_price = self.get_price(actual_price_text)
        assert (
            price == actual_price
        ), f"Expected product price {price}, got {actual_price} instead"

    def add_to_cart(self):
        """Verifies that Add to cart button is present on the procust page and adds product to cart"""
        assert self.is_element_present(
            *p.add_to_cart_button
        ), "Add to cart button not found on ProductPage"
        self.browser.find_element(*p.add_to_cart_button).click()
        self.alert_accept(PRODUCT_ADDED_ALERT_MESSAGE)
