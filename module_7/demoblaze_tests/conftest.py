import pytest
from selenium import webdriver
from demoblaze_tests.common.PAGES.main_page import MainPage
from demoblaze_tests.common.constants import BASE_URL
from demoblaze_tests.common import utils
from typing import Generator


def get_browser() -> webdriver.Chrome:
    """Setting browser Chrome"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)
    return browser


@pytest.fixture(scope="module")
def user_creds() -> Generator[tuple[str, str], None, None]:
    """Registering new user and returning credentials for further use"""
    browser = get_browser()
    credentials = utils.generate_credentials()
    page = MainPage(browser, BASE_URL)
    page.open()
    page.register_user(credentials)
    browser.quit()
    yield credentials
    # Teardown - delete registered user


@pytest.fixture(scope="function")
def test_browser() -> Generator[webdriver.Chrome, None, None]:
    browser = get_browser()
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def logged_in_user_page(
    test_browser: webdriver.Chrome, user_creds: tuple[str, str]
) -> Generator[MainPage, None, None]:
    """Setup - log in in registered user and yield browser with logged in user. Teardown - log out user.
    Arguments:
    user_creds - login and password of registered user
    test_browser - new browser window"""
    page = MainPage(test_browser, BASE_URL)
    page.open()
    page.login_user(user_creds)
    yield page
    page.logout_user()
