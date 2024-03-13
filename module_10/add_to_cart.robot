*** Settings ***
Resource    demoblaze.resource


*** Test Cases ***
Logged In User Adds Product To Cart 
    [Documentation]    Test verifies that logged in user can add product to cart.
    [Setup]    User Login Setup
    Open Monitors Category
    ${product_with_max_price_locator}    ${max_price}    ${product_name}=    Find Product With Highest price
    Click Element    ${product_with_max_price_locator}
    Should Be Correct Product Page    ${product_name}    ${max_price}
    Add To Cart
    Click Element    ${CART_HEADER_BUTTON}
    Should Be Added In Cart     ${product_name}    ${max_price}
    Check Total    ${max_price}
    [Teardown]    Log Out and Close Browser


  
*** Keywords ***
User Login Setup
    [Documentation]    Registers new user and loggs user in
    ${username}    ${password}=    Register New User
    Open Demoblaze
    Log In User    ${username}    ${password}
    Verify User Is Logged In    ${username}