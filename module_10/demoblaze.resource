*** Settings ***
Documentation    Demoblaze.resource file provides keywords and variables for Demoblaze tests
Library    SeleniumLibrary
Library    String
Library    helpers/helpers.py

*** Variables ***
${BROWSER}    Chrome

# Constants
${URL}    https://www.demoblaze.com/
${SUCCESSFUL_SIGN_UP_ALERT_MESSAGE}    Sign up successful.
${PRODUCT_ADDED_ALERT_MESSAGE}    Product added.
${LOGGED_USER_HEADER_TEXT}    Welcome

# MainPageLocators
${SIGN_UP_HEADER_BUTTON}    id:signin2
${LOG_IN_HEADER_BUTTON}     id:login2
${CART_HEADER_BUTTON}       id:cartur
${LOG_OUT_HEADER_BUTTON}    id:logout2
${LOGGED_IN_USERNAME_HEADER}    id:nameofuser
${MONITORS}    xpath://*[@class="list-group-item" and contains(text(), "Monitors")]

# SignUpDialogLocators
${USERNAME_FIELD}    id:sign-username
${PASSWORD_FIELD}    id:sign-password
${CONFIRM_BUTTON}    css:[onclick="register()"]

# LogInDialogLocators
${LOG_IN_USERNAME}    id:loginusername
${LOG_IN_PASSWORD}    id:loginpassword
${LOG_IN_CONFIRM_BUTTON}    css:[onclick="logIn()"]

# CategoryPageLocators
${CATEGORY_PRODUCT_CARD}    class:card-block
${MAX_PRICE_PRODUCT}    xpath://*[@class="card-title"]//*[contains(text(), "{}")]

# ProductPageLocators
${PRODUCT_NAME}    css:#tbodyid > .name
${PRODUCT_PRICE}    css:#tbodyid > .price-container
${ADD_TO_CART_BUTTON}    class:btn-success

# CartPageLocators
${CART_TOTAL}    id:totalp
${CART_ADDED_PRODUCT_NAME}    css:#tbodyid > tr > td:nth-child(2)
${CART_ADDED_PRODUCT_PRICE}    css:#tbodyid > tr > td:nth-child(3)


*** Keywords ***
Generate Credentials
    [Documentation]    Generates unique username and password
    ${timestamp}=    Get Time    epoch
    ${username}=    Set Variable    user${timestamp}
    ${password}=    Set Variable    password${timestamp}
    RETURN    ${username}    ${password}


Open Demoblaze
    [Documentation]    Opens Chrome at demoblaze.com in incognito and fullscreen
    [Tags]    Screenshot
    ${chrome_options} =    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}    add_argument    --incognito
    Call Method    ${chrome_options}    add_argument    --start-maximized
    Open Browser    url=${URL}    browser=${BROWSER}    options=${chrome_options} 
    Set Selenium Implicit Wait    10 seconds 


Register New User
    [Documentation]    Keyword performs registration on demoblaze.com
    [Tags]    Screenshot
    Open Demoblaze
    ${username}    ${password}=    Generate Credentials
    Page Should Contain Element    ${SIGN_UP_HEADER_BUTTON} 
    Click Element    ${SIGN_UP_HEADER_BUTTON} 
    Input Text    ${USERNAME_FIELD}    ${username}
    Input Text    ${PASSWORD_FIELD}    ${password}
    Click Element    ${CONFIRM_BUTTON}
    Alert Should Be Present    text=${SUCCESSFUL_SIGN_UP_ALERT_MESSAGE}    action=ACCEPT
    Close Browser
    RETURN    ${username}    ${password}


Log In User
    [Arguments]    ${username}    ${password}
    [Documentation]    Keyword logs user in with given credentials 
    ...    Argquments:
    ...    _username_ - username 
    ...    _password_ - password 
    Page Should Contain Element    ${LOG_IN_HEADER_BUTTON}
    Click Element    ${LOG_IN_HEADER_BUTTON}
    Input Text    ${LOG_IN_USERNAME}    ${username}
    Input Text    ${LOG_IN_PASSWORD}    ${password}
    Click Element    ${LOG_IN_CONFIRM_BUTTON}


Verify User Is Logged In
    [Arguments]    ${expected_username}
    [Documentation]    Keyword verifies that user is logged in
    ...    Arguments:
    ...    _expected_username_ - username of logged in user, should be displayed in header
    [Tags]    Screenshot
    Wait Until Element Contains    ${LOGGED_IN_USERNAME_HEADER}    ${LOGGED_USER_HEADER_TEXT}
    ${welcome_username}=    Get Text    ${LOGGED_IN_USERNAME_HEADER}
    Should Contain    ${welcome_username}    ${expected_username}  


Log Out and Close Browser
    [Documentation]    Keyword logs out and closes current browser
    Click Element    ${LOG_OUT_HEADER_BUTTON}
    ${welcome_username}=    Get Text    ${LOGGED_IN_USERNAME_HEADER}
    Should Be Empty    ${welcome_username}
    Close Browser


Open Monitors Category 
    [Documentation]    Keyword opens monitor category
    [Tags]    Screenshot
    Wait Until Keyword Succeeds    5    1s    Click Element    ${MONITORS}
    Sleep    2s    # we cannot determine if the product list was rerendered, no correct locators, sleep is a must


Get All Products In Category
    [Documentation]    Collects list of products on page as WebEelements
    @{PRODUCTS}=    Get WebElements    ${CATEGORY_PRODUCT_CARD}
    RETURN    @{PRODUCTS}


Get Price 
    [Arguments]    ${price_text}
    [Documentation]    Keyword returns price as an integer from given string
    ...    Arguments:
    ...    _price_text_ - text inside WebElement that contains price info
    ${price}=    Replace String Using Regexp    ${price_text}    [^0-9]    ${EMPTY}
    RETURN    ${price}


Find Product With Highest price
    [Documentation]    Keyword finds product with the highest price and returns product data: locator, name, price
    @{ALL_PRODUCTS}=    Get All Products In Category
    ${max_price}=    Set Variable    0
    ${product_with_max_price}=    Set Variable    None
    FOR    ${element}    IN    @{ALL_PRODUCTS}
        ${price_text}=    Get Price From Block    ${element}
        ${price}=    Get Price    ${price_text}
        ${product_with_max_price}=    Set Variable If    ${price} > ${max_price}    ${element}    ${product_with_max_price}
        ${max_price}=    Set Variable If    ${price} > ${max_price}    ${price}    ${max_price}
    END
    ${product_name}=    Get Name From Block    ${product_with_max_price}
    ${product_with_max_price_locator}=    Format String    ${MAX_PRICE_PRODUCT}    ${product_name}
    RETURN    ${product_with_max_price_locator}    ${max_price}    ${product_name}   


Should Be Correct Product Page
    [Arguments]    ${expected_name}    ${expected_price}
    [Documentation]    Verifies that page contains correct product 
    ...    Arguments
    ...    _expected_name_ - name of the product that should be on page 
    ...    _expected_price_ - price of the product that should be on page 
    [Tags]    Screenshot
    ${actual_product_name}=    Get Text    ${PRODUCT_NAME}
    Should Be Equal    ${expected_name}    ${actual_product_name}
    ${actual_price_text}=    Get Text    ${PRODUCT_PRICE}
    ${actual_price}=    Get Price    ${actual_price_text}
    Should Be Equal    ${expected_price}    ${actual_price}


Add To Cart
    [Documentation]    Keyword adds product to cart
    Click Element    ${ADD_TO_CART_BUTTON}
    Alert Should Be Present    text=${PRODUCT_ADDED_ALERT_MESSAGE}    action=ACCEPT


Should Be Added In Cart
    [Arguments]    ${expected_name}    ${expected_price}
    [Documentation]    Verifies that product added in cart has correct name and price  
    ...    Arguments
    ...    _expected_name_ - name of the product that should be in cart  
    ...    _expected_price_ - price of the product that should be in cart
    [Tags]    Screenshot
    ${actual_product_name}=    Get Text    ${CART_ADDED_PRODUCT_NAME}
    Should Be Equal    ${expected_name}    ${actual_product_name}
    ${actual_price_text}=    Get Text    ${CART_ADDED_PRODUCT_PRICE}
    ${actual_price}=    Get Price    ${actual_price_text}
    Should Be Equal    ${expected_price}    ${actual_price}


Check Total
    [Arguments]    ${expected_total}
    [Documentation]    Keyword verifies that total is correct 
    ...    Arguments
    ...    _expected_total_ - total that should be displayed in cart
    [Tags]    Screenshot
    ${actual_price_text}=    Get Text    ${CART_TOTAL}
    ${actual_price}=    Get Price    ${actual_price_text}
    Should Be Equal    ${expected_total}    ${actual_price}
