import pytest
from saucedemo_tests.common.pages.inventory_page import InventoryPage
from saucedemo_tests.common.pages.login_page import LoginPage
from saucedemo_tests.common.constants import BASE_URL, CREDENTIALS
from selenium import webdriver
from typing import Generator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def browser() -> Generator[webdriver.Chrome, None, None]:
    """
    Setup: Setting browser Chrome
    Teardown: quitting Chrome
    """
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(10)
        yield browser
    except Exception as e:
        logger.error(f"Exception during browser setup: {e}")
        raise e
    finally:
        try:
            browser.quit()
        except Exception as e:
            logger.error(f"Exception during browser cleanup: {e}")    


@pytest.fixture(scope="function")
def logged_in_user_page(browser: webdriver.Chrome
) -> Generator[InventoryPage, None, None]:
    """
    Setup: Logging user in
    Teardown: Logging user out
    """
    login_page = LoginPage(browser, BASE_URL)
    login_page.open()
    login_page.login(CREDENTIALS)
    login_page.should_be_logged_in()
    page = InventoryPage(login_page.browser, login_page.browser.current_url)
    page.reset_app_state()
    yield page
    page.logout()