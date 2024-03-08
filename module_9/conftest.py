import pytest
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