*** Settings ***
Resource    demoblaze.resource


*** Test Cases ***
Log In For Registered User
    [Documentation]    Test verifies that registered user can log in.
    [Setup]    User Register Setup    
    Open Demoblaze
    Log In User    ${test_username}    ${test_password}
    Verify User Is Logged In    ${test_username}
    [Teardown]    Log Out and Close Browser


*** Keywords ***
User Register Setup
    [Documentation]    Registering new user and returning credentials for further use
    ${username}    ${password}=    Register New User
    Set Test Variable    ${test_username}    ${username}
    Set Test Variable    ${test_password}    ${password}

