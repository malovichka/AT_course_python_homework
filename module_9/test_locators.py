import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from typing import TYPE_CHECKING
import locators as l
from utils import *

if TYPE_CHECKING:
    from selenium import webdriver

URL = "https://www.epam.com/"


@pytest.mark.parametrize("keyword, desired_location", [("python", "All Locations")])
def test_search_for_position_based_on_criteria(
    browser: "webdriver.Chrome", keyword: str, desired_location: str
):
    """
    Verifies that the user can search for a position based on criteria.
    Arguments:
    browser - browser to run test
    keyword - parameter for vacancy search, like programming language
    desired_location - location for vacancy search
    """
    # 1.	Navigate to https://www.epam.com/
    browser.get(URL)

    # 2.	Find a link “Carriers” and click on it
    click_with_retry(browser, By.LINK_TEXT, l.careers_link)

    # 3.	Write the name of any programming language in the field “Keywords” (should be taken from test parameter)
    keyword_field = browser.find_element(By.ID, l.keyword_field)
    browser.execute_script("arguments[0].scrollIntoView();", keyword_field)
    keyword_field.send_keys(keyword)
    keyword_field.send_keys(Keys.ENTER)

    # 4.	Select “All Locations” in the “Location” field (should be taken from the test parameter)
    click_with_retry(browser, By.CLASS_NAME, l.location_field)
    location_option = By.CSS_SELECTOR, l.location_option.format(desired_location)
    browser.execute_script(
        "arguments[0].scrollIntoView();", browser.find_element(*location_option)
    )
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located(location_option)
    )
    click_with_retry(browser, *location_option)

    # 5.	Select the option “Remote”
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, l.remote))
    )
    click_with_retry(browser, By.XPATH, l.remote)

    # 6.	Click on the button “Find”
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.XPATH, l.find_button))
    )
    click_with_retry(browser, By.XPATH, l.find_button)

    # 7.	Find the latest element in the list of results
    browser.execute_script(
        "arguments[0].scrollIntoView();",
        browser.find_element(By.CLASS_NAME, l.search_result_list),
    )
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, l.search_result_list))
    )
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, l.search_result_item))
    )

    # 8.	Click on the button “View and apply”
    click_with_retry(browser, By.XPATH, l.view_apply_button)

    # 9.	Validate that the programming language mentioned in the step above is on a page
    vacancy = browser.find_element(By.TAG_NAME, l.vacancy_header).text.lower()
    assert (
        keyword in vacancy
    ), f"Expected {keyword} to be present in header, actual header {vacancy}"


@pytest.mark.parametrize(
    "search_query",
    [
        pytest.param(
            "BLOCKCHAIN",
            marks=pytest.mark.xfail(reason="related article without substring present"),
        ),
        "Cloud",
        pytest.param(
            "Automation",
            marks=pytest.mark.xfail(reason="related article without substring present"),
        ),
    ],
)
def test_global_search(browser: "webdriver.Chrome", search_query: str):
    """
    Verififes that global search returns corresponding results
    browser - browser to run test
    search_query - search query to put in search box
    """
    # 1.	Navigate to https://www.epam.com/
    browser.get(URL)

    # 2.	Find a magnifier icon and click on it
    click_with_retry(browser, By.CLASS_NAME, l.search_icon)

    # 3.	Find a search string and put there “BLOCKCHAIN”/”Cloud”/”Automation” (use as a parameter for a test)
    WebDriverWait(browser, timeout=10).until(
        EC.visibility_of_element_located((By.NAME, l.search_box))
    )
    browser.find_element(By.NAME, l.search_box).send_keys(search_query)

    # 4.	Click “Find” button
    click_with_retry(browser, By.CLASS_NAME, l.global_search_find_button)

    # 5.	Validate that all links in a list contain the word “BLOCKCHAIN”/”Cloud”/”Automation” in the text.
    articles = browser.find_elements(By.TAG_NAME, l.article)
    search_query_options = (
        search_query.lower(),
        search_query.upper(),
        search_query.capitalize(),
    )

    for article in articles:
        article_link = article.find_element(
            By.CLASS_NAME, l.article_link
        ).get_attribute("href")
        article_description = article.find_element(
            By.CLASS_NAME, l.article_description
        ).text
        for query in search_query_options:
            if check_substring_in_element(
                article, By.PARTIAL_LINK_TEXT, l.link_text.format(query)
            ) or check_substring_in_element_text(
                article, By.CLASS_NAME, l.article_description, query
            ):
                break
        else:
            raise AssertionError(
                f"Text {search_query} not found in article link or description : \n"
                f"link to article: {article_link}, \n"
                f"article description: {article_description}"
            )
