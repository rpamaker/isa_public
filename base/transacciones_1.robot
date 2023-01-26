*** Settings ***
Documentation   Template robot main suite.
Library         Collections
Resource        keywords.robot
Library         RPA.Browser.Selenium
Library         ConciliacionesAPIHelper
Library         DateHelper
Library         SelGridHelper
Library         String
Library         DateTime

#*** Variables ***
#${erp_username}
#${erp_password}
#${erp_url}
#${source}
#${config}


# +
*** Keywords ***
    
Log in ERP
    Input Text    id:loginForm:usuario    ${erp_username}
    Input Password    id:loginForm:password   ${erp_password}
    Click Button    Ingresar

# +
*** Keywords ***
Get saldo fecha
    [Arguments]    ${fecha}    ${cuenta_corriente}
    Go To    ${erp_url}/iJServ_Web/transacciones/libroDeBancoForm.jsf
    
    Input Text    id:Form:desdeInputDate     ${fecha} 00:00
    Input Text    id:Form:hastaInputDate     ${fecha} 23:59
    Input Text    id:Form:codCuentaProveedor     ${cuenta_corriente}
    Select Radio Button    Form:j_id230    Form:j_id230:1
    Click Button    Consultar
    
    Wait Until Page Contains Element    //*[@id="Form:saldoInicial" and text() != ""]
    ${saldo}=   Get Text    id:Form:saldoInicial
    
    Log    ${saldo}
    [Return]    ${saldo}  
    

# -

*** Keywords ***
Get transacciones desde hasta    
    [Arguments]    ${fecha_desde}    ${fecha_hasta}    ${cuenta_corriente}     ${erp_url}
    Go To    ${erp_url}/iJServ_Web/transacciones/transaccionForm.jsf
    
    Input Text    id:FormBusqueda:desdeInputDate     ${fecha_desde}
    Input Text    id:FormBusqueda:hastaInputDate     ${fecha_hasta}
    Input Text    id:FormBusqueda:codCuentaProveedor     ${cuenta_corriente}
    
    Click Button    Consultar
    Sleep  2
    #Este boton es el que descarga el excel
    Click Element    //input[@src='/iJServ_Web/resources/imagenes/XLS.png']    
    # create unique folder

*** Tasks ***
Get transacciones from EXCEL task
#   ${config}=   Evaluate   dict(${config})
#
#   Set Global Variable    ${erp_url}    ${config['erp_url']}
#   Set Global Variable    ${erp_username}    ${config['erp_username']}
#   Set Global Variable    ${erp_password}    ${config['erp_password']}
#   Set Global Variable    ${source}    ${config['source']}
#   Set Global Variable    ${source}    ${config['source_id']}
#   Set Global Variable    ${source}    ${config['source']}
   Open Remote Browser    ${erp_url}/iJServ_Web
   Log in ERP

   
   #Mientras no este orquestador se toma fecha de ejecucion
    ${fecha_hasta}=    Get Current Date   result_format=%d/%m/%Y  
    #${fecha_hasta}   Set Variable   22/07/2021   
    #${fecha_desde}=    Subtract Time From Date     ${fecha_hasta}     10 days   result_format=%d/%m/%Y   date_format=%d/%m/%Y
    #End

   Get transacciones desde hasta    ${fecha} 00:00    ${fecha} 23:59    ${source}    ${erp_url}
   #Get transacciones desde hasta    ${fecha_desde} 00:00    ${fecha_hasta} 23:59    ${source}    ${erp_url}
   Sleep    50
   ${file}=    Wait Until Keyword Succeeds    1 min    2 sec   Get Downloaded Files
   Length Should Be    ${file}    1    Should be only one file in the download folder   
  # ${file}=    Wait Until Keyword Succeeds    1 min    2 sec    Download should be done    ${download_directory}
   ${tabla_transacciones}=    Read Datos de Excel as Table    ${file}[0]

   ${response}=    Send Transacciones Erp   ${tabla_transacciones}    ${source_id}   ${empresa}
   Log   ${tabla_transacciones}
   #Log   ${response.content}


   [Teardown]    Close All Browsers

