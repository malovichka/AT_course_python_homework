from saucedemo_tests.common.pages.base_page import BasePage
from saucedemo_tests.common.locators import (
    LoginPageLocators as login,
    InventoryPageLocators as inv,
)
from saucedemo_tests.common.constants import (
    BASE_URL,
    INVENTORY_ENDPOINT,
    INVENTORY_TITLE,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):
    """
    Class containing methods for login functionality
    """

    def login(self, credentials: dict):
        """
        Logs in user with given credentials
        Arguments:
        credentials - dict {username: value, password: value}
        """
        assert self.is_element_present(
            *login.username
        ), "Username field not found on login page"
        assert self.is_element_present(
            *login.password
        ), "Password field not found on login page"
        assert self.is_element_present(
            *login.login_button
        ), "Login button not found on login page"
        self.browser.find_element(*login.username).send_keys(credentials["username"])
        self.browser.find_element(*login.password).send_keys(credentials["password"])
        self.browser.find_element(*login.login_button).click()

    def should_be_logged_in(self):
        """
        Verifies that user is successfully logged in.
        """
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.visibility_of_element_located((inv.menu_button))
            )
        except TimeoutException:
            raise TimeoutException("Menu button is not present")
        self.should_be_on_page(INVENTORY_ENDPOINT, *inv.title, INVENTORY_TITLE)

    def should_not_be_logged_in(self, error_message: str):
        """
        Verifies that user is not logged in
        Arguments:
        error-message - expected message to be seen on login page after failed login
        """
        assert (
            self.browser.current_url == BASE_URL
        ), f"Expected to be on login page, but URL is {self.browser.current_url}"
        self.should_have_error_icons()
        error_text = self.browser.find_element(*login.error_message).text
        assert (
            error_text == error_message
        ), f"Expected to have error {error_message}, got {error_text} instead"
