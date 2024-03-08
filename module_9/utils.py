from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

if TYPE_CHECKING:
    from selenium import webdriver


@retry(
    stop=stop_after_attempt(3),
    before=wait_fixed(1),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(
        (StaleElementReferenceException, ElementClickInterceptedException)
    ),
)
def click_with_retry(browser: "webdriver.Chrome", method: type["By"], locator: str):
    """
    Click web element with retry using @retry
    Arguments:
    browser - instance of Chrome where test is taking place
    method - By. selenium method of search (Name, ID, Class Name, etc)
    locator - locator of element
    """
    browser.find_element(method, locator).click()


def check_substring_in_element(
    browser: "webdriver.Chrome", method: type["By"], locator: str
) -> bool:
    """
    Returns True if element is found by locator-substring, otherwise False
    Arguments:
    browser - instance of Chrome where test is taking place
    method - By. selenium method of search (Link Text, Partial Link Text)
    locator - locator of element, basically a substring that will be searched for in element
    """
    try:
        browser.find_element(method, locator)
    except NoSuchElementException:
        return False
    return True


def check_substring_in_element_text(
    browser: "webdriver.Chrome", method: type["By"], locator: str, substring: str
) -> bool:
    """
    Returns True if substring is found in element text, otherwise False
    Arguments:
    browser - instance of Chrome where test is taking place
    method - By. selenium method of search (Name, ID, Class Name, etc)
    locator - locator of element
    substring - substring that will be searched for in element text
    """
    text = browser.find_element(method, locator).text
    return substring in text
