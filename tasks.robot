*** Settings ***
Library     RPA.Browser.Selenium
Library     RPA.Robocorp.WorkItems
Library     utils.py


*** Variables ***
@{default_site}=    https://portal.robocorp.com


*** Tasks ***
Product Screenshot as Artifact
    @{sites}=    Get Work Item Variable    sites    default=${default_site}
    Open Available Browser    about:blank    headless=True
    FOR    ${site}    IN    @{sites}
        Go To    ${site}
        Sleep    5s
        ${address}=    Get Address Without Dots    ${site}
        Screenshot    filename=%{ROBOT_ARTIFACTS}${/}${address}.png
    END
    Log    Done.
