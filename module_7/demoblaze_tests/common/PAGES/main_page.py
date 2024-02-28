import time
from typing import TYPE_CHECKING, Callable
import re
from selenium.common.exceptions import NoSuchElementException
from demoblaze_tests.common.locators import (
    MainPageLocators as main,
    SignUpDialogLocators as signup,
    LogInDialogLocators as login,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from demoblaze_tests.common.constants import (
    SUCCESSFUL_SIGN_UP_ALERT_MESSAGE,
    LOGGED_USER_HEADER_TEXT,
)

if TYPE_CHECKING:
    from selenium.webdriver import Chrome
    from selenium.webdriver.common.by import By


class MainPage:
    def __init__(self, browser: "Chrome", url: str):
        self.browser = browser
        self.url = url

    def open(self):
        """Opens URL in browser window"""
        self.browser.get(self.url)

    def is_element_present(self, how: type["By"], what: str) -> bool:
        """Verifies if element is present on the page, used in conjunction with assert.
        Arguments:
        how - selenium method By (id, css locator, xpath, etc.)
        what - locator"""
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def get_price(self, price_text: str) -> int:
        """Gets price as integer from price texts in the elements
        Arguments:
        price_text - text with price from locator"""
        price = re.sub(r"[^0-9]", "", price_text)
        return int(price)

    def create_locator(self, locator_to_format: tuple[type["By"], str], data: str) -> tuple[type["By"], str]:
        """Generates locator with xpath locator using formatting
        Arguments:
        locator_to_format - tuple with locator (how: By.CSS/XPATH/CLASS etc, what: locator string)
        data - string to be inserted in locator using format"""
        method, locator = locator_to_format
        new_locator = locator.format(data)
        return method, new_locator

    def retry_action(
        self,
        action: Callable,
        *,
        num_retries: int = 5,
        timeout: int = 1,
        exception: type[Exception] = Exception,
    ):
        """Retries function execution if exception occurs for not functional reasons: stale elements, loading, etc"
        Arguments:
        action - function to be retried
        num_retries = number of retries
        timeout - time to wait after each failed retry
        exception - exception that needs to be bypassed by retry"""
        retry_number = 0
        result = None
        while True:
            if retry_number > num_retries:
                raise ValueError("Max retries number is exceeded!")

            try:
                result = action()
            except exception:
                time.sleep(timeout)
                continue

            return result

    def dialog_actions(self, dialog_type: type, credentials: tuple[str, str]):
        """Verifies that opened dialog has all required elements and fills in data for SIGN UP/LOG IN actions depending on the type of dialog
        dialog_type - locators class
        credentials - tuple (username, password)"""
        assert self.is_element_present(
            *dialog_type.dialog
        ), f"{dialog_type} dialog was not found"
        assert self.is_element_present(
            *dialog_type.username
        ), f"{dialog_type} username field was not found"
        assert self.is_element_present(
            *dialog_type.password
        ), f"{dialog_type} password field was not found"
        assert self.is_element_present(
            *dialog_type.confirm_button
        ), f"{dialog_type} confirm button was not found"
        self.browser.find_element(*dialog_type.username).send_keys(credentials[0])
        self.browser.find_element(*dialog_type.password).send_keys(credentials[1])
        self.browser.find_element(*dialog_type.confirm_button).click()

    def alert_accept(self, message: str, timeout: int = 3):
        """Verifies text in alert and accepts it.
        Arguments:
        message - message that is expected to be in alert
        timeout - time to explicitly wait for alert to appear, default - 3 seconds"""
        WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        text_in_alert = alert.text
        assert (
            message in text_in_alert
        ), f"Expected {message} to be present in alert, got {text_in_alert} instead"
        alert.accept()

    def register_user(self, credentials: tuple[str, str]):
        """Registers user with given credentials.
        Arguments:
        credentials - tuple(username, password)"""
        assert self.is_element_present(
            *main.sign_up_header_button
        ), "Sign up button is not found!"
        self.browser.find_element(*main.sign_up_header_button).click()
        self.dialog_actions(signup, credentials)
        self.alert_accept(SUCCESSFUL_SIGN_UP_ALERT_MESSAGE)

    def login_user(self, credentials: tuple[str, str]):
        """Logs in user with given credentials
        Arguments:
        credentials - tuple(username, password)"""
        assert self.is_element_present(*main.log_in_header_button)
        self.browser.find_element(*main.log_in_header_button).click()
        self.dialog_actions(login, credentials)

    def should_be_logged_in(self, username: str, timeout: int = 5):
        """Verifies that user is successfully logged in.
        Arguments:
        username - users username
        timeout - time that browser will explicitly wait for header to load Welcome username element, default - 5 seconds.
        """

        WebDriverWait(self.browser, timeout).until(
            EC.text_to_be_present_in_element(
                (main.logged_in_username_header), text_=LOGGED_USER_HEADER_TEXT
            )
        )
        welcome_text = self.browser.find_element(*main.logged_in_username_header).text
        assert (
            username in welcome_text
        ), f"expected logged in user to be {username}, got {welcome_text} instead"
        assert self.is_element_present(
            *main.log_out_header_button
        ), "Log out button was not found!"

    def logout_user(self):
        """Log out user and verifies that user is logged out"""
        self.browser.find_element(*main.log_out_header_button).click()
        welcome_text = self.browser.find_element(*main.logged_in_username_header).text
        assert (
            not welcome_text
        ), f"Expected to be logged out, but got {welcome_text} in header"

    def go_to_category(self, category: str):
        """Navigates to given category with retries
        category - category name (Phones, Monitors, etc.)"""
        category_locator = self.create_locator(main.category, category)
        assert self.is_element_present(*category_locator), f"{category} not found!"

        def click_on_category():
            el = self.browser.find_element(*category_locator)
            el.click()

        self.retry_action(
            click_on_category, num_retries=5, exception=StaleElementReferenceException
        )

    def go_to_cart(self):
        """Navigates to cart"""
        assert self.is_element_present(*main.cart_header_button)
        self.browser.find_element(*main.cart_header_button).click()
