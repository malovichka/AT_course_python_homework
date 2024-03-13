from typing import TYPE_CHECKING
import re
import random
import string
from selenium.common.exceptions import NoSuchElementException
from saucedemo_tests.common.locators import LoginPageLocators as login


if TYPE_CHECKING:
    from selenium.webdriver import Chrome
    from selenium.webdriver.common.by import By


class BasePage:
    """
    Class BasePage contains common methods for all pages and some helper functions. This is a parent class for all pages
    """

    def __init__(self, browser: "Chrome", url: str, *, timeout: int = 5):
        self.browser = browser
        self.url = url
        self.timeout = timeout

    def open(self):
        """
        Opens URL in browser window
        """
        self.browser.get(self.url)

    def is_element_present(self, how: type["By"], what: str) -> bool:
        """
        Verifies if element is present on the page, used in conjunction with assert.
        Arguments:
        how - selenium method By (id, css locator, xpath, etc.)
        what - locator
        """
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def get_random_id(self, id_range: int):
        """
        Return random integer in range fron 0 to passed id_range
        Arguments:
        id_range - top value of the range, not included
        """
        return random.randint(0, id_range)

    def should_be_on_page(
        self, endpoint: str, how: type["By"], what: str, expected_title: str
    ):
        """
        Verifies that expected page is opened
        Arguments:
        endpoint - string that is expected to be present in current URL
        how - selenium method By (id, css locator, xpath, etc.)
        what - locator
        expected title - title that should be present on expected page
        """
        assert (
            endpoint in self.browser.current_url
        ), f"Expected URL to contain {endpoint}, but current url is {self.browser.current_url}"
        page_title = self.browser.find_element(how, what).text
        assert (
            page_title == expected_title
        ), f"Expected page title to be {expected_title}, got {page_title} instead"

    def get_int_from_text(self, element_text: str) -> int:
        """
        Gets price as integer from price texts in the elements
        Arguments:
        price_text - text with price from locator
        """
        value = re.sub(r"[^0-9]", "", element_text)
        return int(value)

    def create_locator(
        self, locator_to_format: tuple[type["By"], str], data: str | int
    ) -> tuple[type["By"], str]:
        """
        Generates locator with xpath locator using formatting
        Arguments:
        locator_to_format - tuple with locator (how: By.CSS/XPATH/CLASS etc, what: locator string)
        data - string to be inserted in locator using format
        """
        method, locator = locator_to_format
        new_locator = locator.format(data)
        return method, new_locator

    def get_id_name_for_locator(self, name: str) -> str:
        """
        Formats name of the item for using it in locators
        Arguments:
        name - item name
        """
        id_name = name.lower().split()
        return ("-").join(id_name)

    def get_random_string(self, length: int) -> str:
        """
        Generates string of given legth from random ASCII symbols
        length - number of symbols for string to have
        """
        random_string = "".join(random.choice(string.ascii_lowercase) for i in range(length))
        return random_string

    def should_have_error_icons(self):
        """
        Verifies that icons indicating input error are present on page
        """
        error_icons = self.browser.find_elements(*login.error_icon)
        assert error_icons, "No error icons shown!"
