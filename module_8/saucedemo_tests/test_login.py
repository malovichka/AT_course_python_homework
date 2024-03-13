from saucedemo_tests.common.pages.inventory_page import InventoryPage
from saucedemo_tests.common.pages.login_page import LoginPage
from saucedemo_tests.common.constants import (
    BASE_URL,
    CREDENTIALS,
    LOGIN_ERROR_MESSAGES
)
import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium import webdriver

negative_scenarios = [
        (
            {"username": "", "password": CREDENTIALS["password"]},
            LOGIN_ERROR_MESSAGES["missing username"],
        ),
        (
            {"username": CREDENTIALS["username"], "password": ""},
            LOGIN_ERROR_MESSAGES["missing password"],
        ),
        (
            {
                "username": f'{CREDENTIALS["username"]}1',
                "password": CREDENTIALS["password"],
            },
            LOGIN_ERROR_MESSAGES["bad credentials"],
        ),
        (
            {
                "username": {CREDENTIALS["username"]},
                "password": f'{CREDENTIALS["password"]}1',
            },
            LOGIN_ERROR_MESSAGES["bad credentials"],
        ),
    ]

def test_login_positive(browser: "webdriver.Chrome"):
    """Test verifies login functionality - user can successfully log in:
    - positive scenario with correct credentials"""
    login_page = LoginPage(browser, BASE_URL)
    login_page.open()
    login_page.login(CREDENTIALS)
    login_page.should_be_logged_in()
    page = InventoryPage(login_page.browser, login_page.browser.current_url)
    page.logout()


@pytest.mark.parametrize(
    "creds, error_message",
    negative_scenarios,
)
def test_login_negative(browser: "webdriver.Chrome", creds: dict, error_message: str):
    """Test verifies login functionality - user login attempt should fail, negative scenarios:
    - password is not provided
    - username is not provided
    - wrong username provided
    - wrong password provided"""
    login_page = LoginPage(browser, BASE_URL)
    login_page.open()
    login_page.login(creds)
    login_page.should_not_be_logged_in(error_message)
