*** Settings ***
Documentation       Template keyword resource.
Library         RPA.Browser.Selenium
Library         OperatingSystem
Library         RPA.Excel.Files
Library         libraries/SelGridHelper

# +
*** Keywords ***
Open Remote Browser
    [Arguments]    ${url}
    ${now}    Get Time    epoch
    ${download_directory}=     Convert To String    %{DOWNLOADS_PATH}
    Set Global Variable    ${download_directory}	
    
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
	Log  ${chrome_options}
    ${prefs}    Create Dictionary    download.prompt_for_download=False   plugins.always_open_pdf_externally=True   safebrowsing_for_trusted_sources_enabled=False

	Log  ${prefs}
    Call Method    ${chrome_options}    add_experimental_option    prefs    ${prefs}
    
    ${desired_capabilities}    Create Dictionary    browserName=chrome

    Open Browser     ${url}    Chrome    
    ...  options=${chrome_options}
    ...  remote_url=%{HOSTNAME}/wd/hub
    ...  desired_capabilities=${desired_capabilities}
    
    ${session_id}=    Get Session Id
    #${session_ip}=    Get Session Ip Test    ${session_id}   %{HOSTNAME}
    #Set Global Variable    ${session_ip}

Open Remote Browser Firefox
    [Arguments]    ${url}
    ${now}    Get Time    epoch
    ${download_directory}=     Convert To String    %{DOWNLOADS_PATH}
    Set Global Variable    ${download_directory}	
    
    ${chrome_options}=    sys.modules['selenium.webdriver'].FirefoxOptions()
	Log  ${chrome_options}
    ${prefs}    Create Dictionary    download.prompt_for_download=False   plugins.always_open_pdf_externally=True   safebrowsing_for_trusted_sources_enabled=False

	#Log  ${prefs}
    #Call Method    ${chrome_options}    add_experimental_option    prefs    ${prefs}
    
    ${desired_capabilities}    Create Dictionary    browserName=firefox

    Open Browser     ${url}    Firefox    
    ...  options=${chrome_options}
    ...  remote_url=%{HOSTNAME}/wd/hub
    ...  desired_capabilities=${desired_capabilities}
    
    ${session_id}=    Get Session Id
    #${session_ip}=    Get Session Ip Test    ${session_id}   %{HOSTNAME}
    #Set Global Variable    ${session_ip}
    
Open Local Browser    
    [Arguments]    ${url}
    ${now}    Get Time    epoch
    ${download_directory}    Join Path    %{DOWNLOADS_PATH}    downloads_${now}
    #${download directory}=    Convert To String    ${download directory}
    Set Global Variable    ${download_directory}

    Create Directory    ${download_directory}
    
    ${chrome options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    ${prefs}    Create Dictionary    download.default_directory=${download_directory}
    Call Method    ${chrome options}    add_experimental_option    prefs    ${prefs}
    
    Open Browser     ${url}    Chrome    
    ...   options=${chromeOptions}
# -
# +
*** Keywords ***
    
Log in ERP
    Input Text    id:loginForm:usuario    ${erp_username}
    Input Password    id:loginForm:password   ${erp_password}
    Click Button    Ingresar
# -

*** Keywords ***
Download should be done
    [Arguments]    ${directory}
    [Documentation]    Verifies that the directory has only one folder and it is not a temp file.
    ...
    ...    Returns path to the file
    ${files}    List Files In Directory    ${directory}
    Length Should Be    ${files}    1    Should be only one file in the download folder
    Should Not Match Regexp    ${files[0]}    (?i).*\\.tmp    Chrome is still downloading a file
    ${file}    Join Path    ${directory}    ${files[0]}
    Log    File was successfully downloaded to ${file}
    [Return]    ${file}

*** Keywords ***
Read Datos de Excel as Table
    [Arguments]    ${file_path}
    
    RPA.Excel.Files.Open Workbook    %{DOWNLOADS_PATH}/${file_path}
        ${tabla} =    Read Worksheet As Table
    Close Workbook
     
    [Return]    ${tabla} 
