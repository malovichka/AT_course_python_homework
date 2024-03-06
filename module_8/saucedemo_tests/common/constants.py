BASE_URL = "https://www.saucedemo.com/"

CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}
LOGIN_ERROR_MESSAGES = {
    "bad credentials": "Epic sadface: Username and password do not match any user in this service",
    "missing password": "Epic sadface: Password is required",
    "missing username": "Epic sadface: Username is required",
}


INVENTORY_ENDPOINT = "inventory"
INVENTORY_TITLE = "Products"

CART_ENDPOINT = "cart"
CART_TITLE = "Your Cart"

CHECKOUT_1_ENDPOINT = "checkout-step-one"
CHECKOUT_1_TITLE = "Checkout: Your Information"
CHECKOUT_2_ENDPOINT = "checkout-step-two"
CHECKOUT_2_TITLE = "Checkout: Overview"
CHECKOUT_COMPLETE_ENDPOINT = "checkout-complete"
CHECKOUT_COMPLETE_TITLE = "Checkout: Complete!"
CHECKOUT_ERROR_MESSAGES = {
    "missing first name": "Error: First Name is required",
    "missing last name": "Error: Last Name is required",
    "missing zip": "Error: Postal Code is required",
}
