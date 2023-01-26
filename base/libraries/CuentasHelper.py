import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

def encoding(QUERY):
    return urllib.parse.quote(QUERY)

def get_cuentas(JSESSIONID,VSTATE, BASE_URL, EMPRESA):
    url = f"{BASE_URL}/iJServ_Web/transacciones/libroDeBancoForm.jsf"
    payload = f"AJAXREQUEST=_viewRoot&Form=Form&Form%3Aj_id209=true&Form%3AdesdeInputDate=05%2F08%2F2021%2000%3A00&Form%3AdesdeInputCurrentDate=08%2F2021&Form%3AhastaInputDate=05%2F08%2F2021%2023%3A59&Form%3AhastaInputCurrentDate=08%2F2021&Form%3AcodCuentaProveedor=%20&Form%3AidC=&Form%3AsuggestionCuenta_selection=&Form%3Afiltrado=Todas%20las%20transacciones&javax.faces.ViewState={VSTATE}&Form%3AsuggestionCuenta=Form%3AsuggestionCuenta&ajaxSingle=Form%3AsuggestionCuenta&inputvalue=&inputvaluerequest=null&AJAX%3AEVENTS_COUNT=1&"
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': BASE_URL,
        'Referer': url,
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': f'JSESSIONID={JSESSIONID}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(id='_ajax:data')
    data = str(data).strip('<span id="_ajax:data"><![CDATA').strip(']></span>').replace("'", '"')
    
    res = json.loads(data)
    data=[]
    for cuenta in res['suggestionObjects']:
        if cuenta['esCreditoBloqueado']==False:
            nodo={"cuenta":cuenta['codigoCuenta'],"nombre":cuenta['nombreTitular'],"empresa":EMPRESA}
            data.append(nodo)
        
    return data
        

if __name__ == "__main__":
    query=urllib.parse.quote('-8999488004514876764:9122811160045687079')
    print (query)
    print(get_cuentas('5DB8C0A0FAAC200071DF0E2D11D58720',query,'http://axionlegamar.ijservuruguay.com:8080'))