from saucedemo_tests.common.constants import (
    CHECKOUT_1_ENDPOINT,
    CHECKOUT_1_TITLE,
    CHECKOUT_2_ENDPOINT,
    CHECKOUT_2_TITLE,
    CHECKOUT_COMPLETE_ENDPOINT,
    CHECKOUT_COMPLETE_TITLE,
)
from saucedemo_tests.common.pages.cart_page import CartPage
from saucedemo_tests.common.locators import (
    CheckoutPageLocators as co,
    InventoryPageLocators as inv,
    LoginPageLocators as login,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.common.by import By


class CheckoutPage(CartPage):
    """
    Class containing methods for action on checkout pages
    """

    mandatory_fields = (co.first_name, co.last_name, co.postcode)

    def should_be_on_first_checkout(self):
        """
        Verifies that current page is first checkout step
        """
        self.should_be_on_page(CHECKOUT_1_ENDPOINT, *inv.title, CHECKOUT_1_TITLE)

    def should_be_on_second_checkout(self):
        """
        Verifies that current page is second checkout step
        """
        self.should_be_on_page(CHECKOUT_2_ENDPOINT, *inv.title, CHECKOUT_2_TITLE)

    def should_be_completed_checkout(self):
        """
        Verifies that current page is checkout complete step
        """
        self.should_be_on_page(
            CHECKOUT_COMPLETE_ENDPOINT, *inv.title, CHECKOUT_COMPLETE_TITLE
        )

    def should_have_info_form(self):
        """
        Verifies that page contains all mandatory fields: first name, last name, postcode
        """
        for field in self.mandatory_fields:
            assert self.is_element_present(*field), f"Locator {field} not found"

    def enter_full_info(self):
        """
        Fills in all of the mandatory fields with generated 10-symbol string
        """
        self.should_have_info_form()
        user_data = self.get_random_string(
            10
        )  # hardcoded random length on purpose - no restrictions in fields, if there were - could be reused for boundary values testing
        for field in self.mandatory_fields:
            self.browser.find_element(*field).send_keys(user_data)

    def enter_partial_info(
        self, partial_user_info: tuple[tuple[type["By"], str], tuple[type["By"], str]]
    ):
        """Fills in only passed mandatory fileds with generated 10-symbol string
        Arguments:
        partial_user_info - tuple with locators for fields that should be filled in
        """
        self.should_have_info_form()
        user_data = self.get_random_string(10)
        for field in self.mandatory_fields:
            if field in partial_user_info:
                self.browser.find_element(*field).send_keys(user_data)

    def continue_checkout(self):
        """
        Proceed from first checkout step to the second checkout step
        """
        assert self.is_element_present(
            *co.continue_button
        ), "Continue button not found on first checkout page"
        self.browser.find_element(*co.continue_button).click()

    def finish_checkout(self):
        """
        Proceed from second checkout step to checkout completion
        """
        assert self.is_element_present(
            *co.finish_button
        ), "Finish button not found on second checkout page"
        self.browser.find_element(*co.finish_button).click()

    def should_be_item_total(self, expected_total: int):
        """
        Verifies that checkout page contains expected itam total
        expected_total - sum of product prices earlier added to cart
        """
        actual_total_text = self.browser.find_element(*co.item_total).text
        actual_total = self.get_int_from_text(actual_total_text)
        assert (
            expected_total == actual_total
        ), f"Expected item total (without tax) to be {expected_total}, got {actual_total} instead"

    def should_be_failed_first_checkout(self, error_message: str):
        """
        Verifies that first checkout step fails with specified reason
        Arguments:
        error_message - expected error-message indicating checkout failure reason
        """
        self.should_have_error_icons()
        error_text = self.browser.find_element(*login.error_message).text
        assert (
            error_text == error_message
        ), f"Expected to have error {error_message}, got {error_text} instead"
