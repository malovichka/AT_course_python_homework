# Automated Test Suites for SauceDemo Website


### Test Suite 1: test_login.py - Login Functionality Verification

**Purpose:**

This test suite is designed to verify login functionality of the SauceDemo website (https://www.saucedemo.com/). It covers various scenarios to ensure that users can log in successfully and validate elements on the landing page after a successful login, and encounter appropriate error messages for invalid credentials scenarios

#### Test Cases:

```test_login_positive``` - Valid login, positive scenario

Flow:
1) Open https://www.saucedemo.com/
2) Input valid credentials and submit login
3) Verify that login was successfull -  Inventory Page is opened
4) Log out

```test_login_negative``` - parametrized test (passing invalid credentials set and expected error message), covers 4 negative scenarios:
- password is not provided
- username is not provided
- wrong username provided
- wrong password provided

Flow:
1) Open https://www.saucedemo.com/
2) Input invalid credentials and submit login
3) Verify that login was failed - page URL not changed. Verify that error message text is displayed according to credentials mismatch


### Test Suite 2: test_checkout.py - Shopping Cart Functionality and Checkout Process Verification

**Purpose:**

This test suite focuses on validating the shopping cart functionality of the SauceDemo website. It encompasses scenarios related to adding items to the cart, confirming cart contents, completing the checkout process, and handling negative scenarios where mandatory fields for checkout are not filled.

#### Test Cases:

```test_add_items_and_checkout``` - parametrized test (passing quantity of items to be added). Positive scenario for adding 1 or more items in cart and full checkout process

Flow:

- Preconditions - user is logged in and Inventory URL is opened
1) Given number of items is added in cart
2) Go to cart and check that name and price of items in cart - should be data of items from previous step
3) Proceed to checkout
4) Fill in all of the mandatory fields on first phase of checkout and continue
5) On second checkout phase verify that items at checkout match items that were added on main page
6) Verify that total was calculated accurately
7) Finish checkout
- Teardown - logout

```test_checkout_stops_when_missing_data``` - parametrized test (passing fields to fill and expected error message), covers 3 negative scenarios when provided checkout data is insufficient:
- postcode is not provided
- last name is not provided
- first name is not provided

Flow:

- Preconditions - user is logged in and Inventory URL is opened
1) Given number of items is added in cart
2) Go to cart and check that name and price of items in cart - should be data of items from previous step
3) Proceed to checkout
4) Fill in only 2 fields and continue
5) Verify that first checkout was not successfully completed, verify that error message indicates the reason of failure
- Teardown: logout



#### Technologies Used:

Selenium: The test suites are implemented using Selenium, a powerful browser automation tool.

Pytest: Pytest is utilized as the testing framework, providing easy test organization and execution.

Page Object Model (POM): The Page Object Model design pattern is implemented to enhance test maintainability and readability by encapsulating web page interactions into reusable classes.