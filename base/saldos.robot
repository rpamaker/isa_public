*** Settings ***
Documentation   Template robot main suite.
Library         Collections
Resource        keywords.robot
Library         RPA.Browser.Selenium
Library         ConciliacionesAPIHelper
Library         DateHelper
Library         DateTime
Library         SelGridHelper


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

    Sleep  2
    Select Radio Button    Form:j_id209    Form:j_id209:1

    Sleep  2
    Click Button    Consultar
    Sleep  2

    ${res}=   Is Element Visible   id:formMensajes
    IF   ${res} 
        Click Button   //*[@id="formMensajes:j_id385"]        
    END
        
    Wait Until Page Contains Element    //*[@id="Form:saldoInicial" and text() != ""]
    ${saldo}=   Get Text    id:Form:saldoInicial
    
    Log    ${saldo}
    [Return]    ${saldo}  
    

# -

*** Keywords ***
Get transacciones desde hasta    
    [Arguments]    ${fecha_desde}    ${fecha_hasta}    ${cuenta_corriente}
    Go To    ${erp_url}/iJServ_Web/transacciones/transaccionForm.jsf
    
    Input Text    id:FormBusqueda:desdeInputDate     ${fecha_desde}
    Input Text    id:FormBusqueda:hastaInputDate     ${fecha_hasta}
    Input Text    id:FormBusqueda:codCuentaProveedor     ${cuenta_corriente}
    
    Click Button    Consultar

    Click Element    name:Form:j_id354
    
    # create unique folder

# +
*** Tasks ***
Get saldos task
    Open Remote Browser     ${erp_url}/iJServ_Web
    ${session_id}=    Get Session Id
    Log in ERP
    #Mientras no este orquestador se toma fecha de ejecucion
    ${fecha_hasta}=    Get Current Date   result_format=%d/%m/%Y    
    ${fecha_desde}=    Subtract Time From Date     ${fecha_hasta}     10 days   result_format=%d/%m/%Y   date_format=%d/%m/%Y
    #End

    ${saldos_list}=   Create List
    @{date_range}=    Get Date Range    ${fecha_desde}    ${fecha_hasta}

    FOR    ${saldo_date}  IN   @{date_range}
        ${saldo}=    Get saldo fecha    ${saldo_date}    ${source}

        ${saldo_dict}=  Create Dictionary    fecha=${saldo_date}    source=${source_id}   saldo=${saldo}

        Append To List     ${saldos_list}   ${saldo_dict}
    END
    Log   ${saldos_list}
    ${response}=    Send Saldo Erp    ${saldos_list}   ${empresa}

    Log   ${response.content}

    [Teardown]    Close All Browsers
    
#    [Teardown]    Quit   ${session_id}   %{HOSTNAME}


# -

# *** Tasks ***
# Get transacciones from EXCEL task
#    [Setup]   Open Local Browser    %{ERP_URL}
#    Log in ERP
#    Get transacciones desde hasta    ${fecha} 00:00    ${fecha} 23:59    ${source}
#    ${file}=    Wait Until Keyword Succeeds    1 min    2 sec    Download should be done    ${download_directory}
#    ${tabla_transacciones}=    Read Datos de Excel as Table    ${file}
#
#
#    ${response}=    Send Transacciones Erp   ${tabla_transacciones}    ${source_id}
#    Log   ${tabla_transacciones}
#    Log   ${response.content}
#
#    [Teardown]    Close All Browsers

