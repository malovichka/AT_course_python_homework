from demoblaze_tests.common.PAGES.main_page import MainPage
from demoblaze_tests.common.locators import CategoryPageLocators as cat
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.common.by import By


class CategoryPage(MainPage):

    def get_all_products_in_category(self) -> list["WebElement"]:
        """Creates a list of products on the page"""
        products = self.browser.find_elements(*cat.product_card)
        return products

    def find_highest_price_product(self) -> dict:
        """Finds product with the highest price  on the page and returns dictionary product info - locator, name, price.
        If highest price is equal for >1 product, first product will be selected."""
        product_list = self.get_all_products_in_category()
        max_price = 0
        max_price_product = None
        for product in product_list:
            price_text = product.find_element(*cat.product_price).text
            price = self.get_price(price_text)
            if price > max_price:
                max_price = price
                max_price_product = product

        max_price_product_name = max_price_product.find_element(*cat.product_link).text
        product_locator = self.create_locator(cat.max_price_product, max_price_product_name)
        max_price_product_data = {
            "product_locator": product_locator,
            "price": max_price,
            "name": max_price_product_name,
        }

        return max_price_product_data

    def go_to_product_page(self, product: tuple[type["By"], str]):
        """Clicks on given product cart to get to product page
        Arguments:
        product - product locator"""
        self.browser.find_element(*product).click()
