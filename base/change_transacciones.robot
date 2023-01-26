*** Settings ***
Documentation   Template robot main suite.
Library         Collections
Resource        keywords.robot
Library         RPA.Browser.Selenium
Library         ConciliacionesAPIHelper
Library         ConciliacionesHelper
Library         DateHelper
Library         SelGridHelper
Library         String
Library         DateTime


*** Keywords ***
Table operations
    ${rows}=  Get Element Count    xpath://*[@id='Form:panelTabla']/table/tbody/tr
    ${columns}=  Get Element Count    xpath://*[@id='Form:panelTabla']/table/thead/tr/th


# +
*** Keywords ***
Go to conciliaciones
    [Arguments]    ${fecha_desde}   ${fecha_hasta}   ${cuenta_corriente}
    Go To    ${erp_url}/iJServ_Web/transacciones/libroDeBancoForm.jsf
    
    Input Text    id:Form:desdeInputDate     ${fecha_desde} 00:00
    Input Text    id:Form:hastaInputDate     ${fecha_hasta} 23:59
    Input Text    id:Form:codCuentaProveedor     ${cuenta_corriente}
    #Input Text    id:Form:desdeInputDate     20/06/2021 00:00
    #Input Text    id:Form:hastaInputDate     22/06/2021 23:59
    #Input Text    id:Form:codCuentaProveedor     SCOTIABANK PESOS

    Select Radio Button    Form:j_id209    Form:j_id209:1
    Select Radio Button    Form:filtrado    Form:filtrado:2
    Click Button    Consultar
    BuiltIn.Sleep   2
    ${res}=   Is Element Visible   id:formMensajes
    IF   ${res} 
        Click Button   //*[@id="formMensajes:j_id385"]        
    END

    Wait Until Page Contains Element    //*[@id="Form:saldoInicial" and text() != ""]

   
# -


*** Keywords ***
Test transacciones
    Open Browser     %{ERP_URL}    Chrome
    Set Browser Implicit Wait    5
    Log in ERP
    ${list_of_lists}=  Get Transacciones Erp   ${empresa}
    Log   ${list_of_lists}
    FOR    ${batch}    IN    @{list_of_lists}
         Log   ${batch}
         Go to conciliaciones  ${batch['fecha_desde']}    ${batch['fecha_hasta']}   ${batch['source']}
         Conciliar Transacciones   ${batch['movimientos']}
    END

# +
*** Tasks ***
Conciliar transacciones
    [Setup]   Open Remote Browser    ${erp_url}/iJServ_Web
    Log in ERP
    ${list_of_lists}=  Get Transacciones Erp   ${empresa}
    Log   ${list_of_lists}
    FOR    ${batch}    IN    @{list_of_lists}
        Log   ${batch}
        Go to conciliaciones  ${batch['fecha_desde']}    ${batch['fecha_hasta']}   ${batch['source']}
        Conciliar Transacciones   ${batch['movimientos']}
        ${response}=   Set Conciliacion App   ${batch['id_conciliacion']}   ${empresa}
        Log   ${response.content}
    END
	[Teardown]    Close All Browsers
