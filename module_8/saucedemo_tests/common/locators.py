from selenium.webdriver.common.by import By


class LoginPageLocators:
    username = (By.ID, "user-name")
    password = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.CLASS_NAME, "error-message-container")
    error_icon = (By.CLASS_NAME, "error_icon")


class InventoryPageLocators:
    title = (By.CLASS_NAME, "title")
    menu_button = (By.ID, "react-burger-menu-btn")
    menu_panel = (By.CLASS_NAME, "bm-menu-wrap")
    menu_panel_hidden = "hidden"
    menu_close = (By.ID, "react-burger-cross-btn")
    logout = (By.ID, "logout_sidebar_link")
    reset = (By.ID, "reset_sidebar_link")
    non_unique_item_locator = (By.CLASS_NAME, "inventory_item")  
    item_name = (By.XPATH, "//*[@id='item_{}_title_link']/div[@class='inventory_item_name ']")
    item_price = (By.XPATH, "//*[@id='add-to-cart-{}']/../*[@class='inventory_item_price']")
    add_to_cart = (By.ID, "add-to-cart-{}")
    remove = (By.CSS_SELECTOR, '[name="remove-{}"]')
    cart_button = (By.CLASS_NAME, "shopping_cart_link")


class CartPageLocators:
    cart_item = (By.CLASS_NAME, "cart_item")
    item_quantity = (By.CLASS_NAME, "cart_quantity")  
    checkout_button = (By.ID, "checkout")
    item_name = (By.XPATH, "//*[@id='item_{}_title_link']/div[@class='inventory_item_name']")
    item_price = (By.CSS_SELECTOR, "#item_{}_title_link ~ .item_pricebar")

class CheckoutPageLocators:
    first_name = (By.ID, "first-name")
    last_name = (By.ID, "last-name")
    postcode = (By.ID, "postal-code")
    continue_button = (By.ID, "continue")
    finish_button = (By.ID, "finish")
    item_total = (By.CLASS_NAME, "summary_subtotal_label")
    


