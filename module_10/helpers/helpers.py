from robot.api.deco import keyword
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


@keyword("Get Price From Block")
def get_price_from_block(product: "WebElement"):
    """
    Gets text with price from product block element
    Arguments:
    product - search for locator happens inside this web element
    """
    return product.find_element(By.CSS_SELECTOR, "h5").text

@keyword("Get Name From Block")
def get_name_from_block(product: "WebElement"):
    """
    Gets name of the product from product block element
    Arguments:
    product - search for locator happens inside this web element
    """
    return product.find_element(By.CSS_SELECTOR, ".card-title > a").text