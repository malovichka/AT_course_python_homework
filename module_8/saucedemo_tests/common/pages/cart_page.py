from saucedemo_tests.common.constants import CART_ENDPOINT, CART_TITLE
from saucedemo_tests.common.pages.inventory_page import InventoryPage
from saucedemo_tests.common.locators import (
    CartPageLocators as cart,
    InventoryPageLocators as inv,
)


class CartPage(InventoryPage):
    """Class containing methods for actions on cart page"""

    def should_be_on_cart_page(self):
        """
        Verifies that cart is opened
        """
        self.should_be_on_page(CART_ENDPOINT, *inv.title, CART_TITLE)

    def should_exact_items_be_added(self, item_id: int, added_item_data: dict):
        """
        Verifies that items present in cart have expected name and price
        Arguments:
        item_id - product id used for getting initial unique locator
        added_item_data - information that item in cart is expected to have (name, price)
        """
        cart_item_data = self.get_item_data(cart, item_id)
        assert (
            added_item_data["name"] == cart_item_data["name"]
        ), f'Expected to have in cart {added_item_data["name"]}, got {cart_item_data["name"]} instead'
        assert (
            added_item_data["price"] == cart_item_data["price"]
        ), f'Expected item price to be {added_item_data["price"]}, got {cart_item_data["price"]} instead'

    def should_have_pieces_added(self, pieces: int):
        """
        Verifies that cart contains expected quantity of items and pices of each item
        Arguments:
        pieces - expected number of instance of each item
        """
        items_in_cart = self.browser.find_elements(*cart.cart_item)
        assert (
            len(items_in_cart) == pieces
        ), f"Expected to have {pieces} items in cart, got {len(items_in_cart)} instead"
        items_total = 0
        for item in items_in_cart:
            q_text = item.find_element(*cart.item_quantity).text
            items_total += self.get_int_from_text(q_text)
        assert (
            items_total == pieces
        ), f"Expected total items added to be {pieces}, got {items_total} instead"

    def go_to_checkout(self):
        """
        Proceeds to from cart checkout
        """
        assert self.is_element_present(
            *cart.checkout_button
        ), "Checkout button not found"
        self.browser.find_element(*cart.checkout_button).click()
