from selenium.webdriver.common.by import By


class ReprName(type):
    def __repr__(cls):
        return cls.__name__


class MainPageLocators:
    sign_up_header_button = (By.ID, "signin2")
    log_in_header_button = (By.ID, "login2")
    cart_header_button = (By.ID, "cartur")
    log_out_header_button = (By.ID, "logout2")
    logged_in_username_header = (By.ID, "nameofuser")
    category = (By.XPATH, '//*[@class="list-group-item" and contains(text(), "{}")]')


class SignUpDialogLocators(metaclass=ReprName):
    dialog = (By.CSS_SELECTOR, "#signInModal > .modal-dialog > .modal-content")
    username = (By.ID, "sign-username")
    password = (By.ID, "sign-password")
    confirm_button = (By.CSS_SELECTOR, '[onclick="register()"]')


class LogInDialogLocators(metaclass=ReprName):
    dialog = (By.CSS_SELECTOR, "#logInModal > .modal-dialog > .modal-content")
    username = (By.ID, "loginusername")
    password = (By.ID, "loginpassword")
    confirm_button = (By.CSS_SELECTOR, '[onclick="logIn()"]')


class CategoryPageLocators:
    # product locators are NOT unique
    product_card = (By.CLASS_NAME, "card-block")
    product_link = (By.CSS_SELECTOR, ".card-title > a")
    product_price = (By.CSS_SELECTOR, "h5")
    max_price_product = (
        By.XPATH,
        '//*[@class="card-title"]//*[contains(text(), "{}")]',
    )


class ProductPageLocators:
    name = (By.CSS_SELECTOR, "#tbodyid > .name")
    price = (By.CSS_SELECTOR, "#tbodyid > .price-container")
    add_to_cart_button = (By.CLASS_NAME, "btn-success")


class CartPageLocators:
    cart_total = (By.ID, "totalp")
    cart_added_product_name = (By.CSS_SELECTOR, "#tbodyid > tr > td:nth-child(2)")
    cart_added_product_price = (By.CSS_SELECTOR, "#tbodyid > tr > td:nth-child(3)")
