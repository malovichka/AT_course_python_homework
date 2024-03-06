from saucedemo_tests.common.pages.base_page import BasePage
from saucedemo_tests.common.locators import (
    InventoryPageLocators as inv,
    LoginPageLocators as login,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class InventoryPage(BasePage):
    """
    Class containing methods for performing actions on the main page and getting information about placed items
    """

    def should_be_opened_menu(self):
        """
        Verifies that menu slide is in opened state
        """
        try:
            WebDriverWait(self.browser, self.timeout).until_not(
                EC.element_attribute_to_include(
                    (inv.menu_panel), attribute_=inv.menu_panel_hidden
                )
            )
        except TimeoutException:
            raise TimeoutException('Menu is not opened - "hidden" attribute not found')

    def should_be_closed_menu(self):
        """
        Verifies that menu slide is in closed state
        """
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.element_attribute_to_include(
                    (inv.menu_panel), attribute_=inv.menu_panel_hidden
                )
            )
        except TimeoutException as e:
            raise TimeoutException('Menu is not closed - "hidden" attribute is present')

    def get_items_quantity_on_page(self) -> int:
        """
        Finds out and returns number of items present on surrent page
        """
        items = self.browser.find_elements(*inv.non_unique_item_locator)
        return len(items)

    def get_random_product_id(self) -> int:
        """
        Returns id for a random product present on the page, further used to get a unique locators
        """
        id_range = self.get_items_quantity_on_page()
        id = self.get_random_id(id_range)
        return id

    def get_items_in_cart_quantity_badge(self) -> int:
        """
        Getting value from text inside item badge element (red circle with integer on cart icon). 
        If element is not present, returns 0.
        """
        quantity_text = self.browser.find_element(*inv.cart_button).text
        if quantity_text:
            return self.get_int_from_text(quantity_text)        
        return 0

    def should_have_items_in_cart_icon(self, expected_number: int):
        """
        Verifies that number in cart icon is expected
        """
        actual = self.get_items_in_cart_quantity_badge()
        assert (
            expected_number == actual
        ), f"Expected to have {expected_number}, got {actual} instead"

    def open_menu(self):
        """
        Opens menu slider
        """
        assert self.is_element_present(*inv.menu_button), "Menu button not found"
        self.should_be_closed_menu()
        self.browser.find_element(*inv.menu_button).click()
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located(inv.menu_close)
            )
        except TimeoutException:
            raise TimeoutException("Close button is not visible")
        self.should_be_opened_menu()

    def close_menu(self):
        """
        Closes menu slider
        """
        self.should_be_opened_menu()
        assert self.is_element_present(*inv.menu_close), "Close menu button not found"
        self.browser.find_element(*inv.menu_close).click()
        self.should_be_closed_menu()

    def logout(self):
        """
        Logs out via logout option in menu slider
        """
        self.open_menu()
        assert self.is_element_present(*inv.logout), "Logout option not found in menu"
        self.browser.find_element(*inv.logout).click()
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located(login.login_button)
            )
        except TimeoutException:
            raise TimeoutException("Login button is not present")

    def reset_app_state(self):
        """
        Resets app to state when nothing is added in cart
        """
        self.open_menu()
        assert self.is_element_present(*inv.reset)
        self.browser.find_element(*inv.reset).click()
        self.close_menu()
        self.should_have_items_in_cart_icon(0)
        self.browser.refresh()  # refresh is needed to remove "Remove" text from buttons - text is present even after reset

    def get_item_data(self, page_type: type, item_id: int) -> dict:
        """
        Gets item data and returns it as dictionary: 
        id_name - name in format 'formatted-item-name' to use it for unique locator generation
        name - item name
        price - item price
        Arguments:
        page_type - page class to identify locator class (InventoryPageLocators and CartPageLocators have different locators for name and price)
        item_id - product id used for getting initial unique locator
        """
        item_locator = self.create_locator(page_type.item_name, item_id)
        assert self.is_element_present(
            *item_locator
        ), f"Item locator {item_locator} not found!"
        item_name = self.browser.find_element(*item_locator).text
        id_name = self.get_id_name_for_locator(item_name)
        if page_type == inv:
            price_locator = self.create_locator(page_type.item_price, id_name)
        else:
            price_locator = self.create_locator(page_type.item_price, item_id)
        assert self.is_element_present(
            *price_locator
        ), f"Price locator for item {item_name} not found"
        price_text = self.browser.find_element(*price_locator).text
        price = self.get_int_from_text(price_text)
        item_data = {"id_name": id_name, "name": item_name, "price": price}
        return item_data

    def add_to_cart(self, item_data: dict) -> dict:
        """
        Adds item to cart
        Arguments:
        item_data - information about the item to be added
        """
        add_item_locator = self.create_locator(inv.add_to_cart, item_data["id_name"])
        assert self.is_element_present(
            *add_item_locator
        ), f"No 'Add to cart' button for this item: {item_data['name']}"
        self.browser.find_element(*add_item_locator).click()
        remove_item_locator = self.create_locator(inv.remove, item_data["id_name"])
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located(remove_item_locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f'Remove button is not present for {item_data["name"]}'
            )

    def go_to_cart(self):
        """
        Clicks on cart icon to go to the cart page
        """
        assert self.is_element_present(*inv.cart_button), "Cart icon not found"
        self.browser.find_element(*inv.cart_button).click()
