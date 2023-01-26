import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging


class ConciliacionesAPI:
    BASE_URL = "https://bancos.rpamaker.com/api"
    BASE_URL_NEW = "http://bancos.rpamaker.com/api"

    # BASE_URL = 'http://127.0.0.1:8000/api'

    def authenticate(self):
        url = f"{self.BASE_URL}/auth/"

        payload = {"username": "admin", "password": "admin"}
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, json=payload)

        if response.status_code == 200:
            self._token = response.json()["token"]
        else:
            raise Exception(f"Failed to authenticate API {response.status_code} {response.text}")

    def make_request(self, request_type, url, payload=None):
        self.authenticate()

        retry_strategy = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        headers = {
            "Authorization": f"Token {self._token}",
            "Content-Type": "application/json",
        }

        response = session.request(request_type, url, headers=headers, json=payload)
        return response

    def saldo_erp(self, saldos):
        url = f"{self.BASE_URL}/saldo_erp/"

        response = self.make_request("POST", url, saldos)
        return response

    def transacciones_erp(self, transacciones):
        url = f"{self.BASE_URL}/transacciones_erp/"

        response = self.make_request("POST", url, transacciones)
        return response

    def get_transacciones_to_change(self, empresa):
        url = f"{self.BASE_URL}/actualizar_erp/?empresa=" + str(empresa)

        response = self.make_request("GET", url)
        return response

    def set_conciliacion(self, id, empresa):
        url = f"{self.BASE_URL}/actualizar_erp/" + str(id) + "/?empresa=" + str(empresa)

        response = self.make_request("PATCH", url)
        return response

    def cuentas_erp(self, cuentas):
        url = f"{self.BASE_URL_NEW}/cuenta_erp/"

        response = self.make_request("POST", url, cuentas)
        return response


def send_saldo_erp(saldos, empresa):
    """
    test_data =
    [{'fecha': '05/06/2021', 'source': 'SCOTIABANK PESOS', 'saldo': '1.389.067,15'},
     {'fecha': '06/06/2021', 'source': 'SCOTIABANK PESOS', 'saldo': '1.586.931,15'},
     {'fecha': '07/06/2021', 'source': 'SCOTIABANK PESOS', 'saldo': '1.721.931,15'}]
    :param saldos:
    :return:
    """
    saldo_list = []
    for saldo in saldos:
        s = {
            "fecha": saldo["fecha"],
            "source": saldo["source"],
            "empresa": empresa,
        }
        saldo_str: str = saldo["saldo"]
        s["saldo"] = float(saldo_str.replace(".", "").replace(",", "."))

        saldo_list.append(s)

    return ConciliacionesAPI().saldo_erp(saldo_list)


def send_transacciones_erp(transacciones, source, empresa):
    from dateparser import parse

    data = []
    for x in transacciones:
        # Format descripcion
        d = x["F"].replace("\n", " ")
        d = " ".join(d.split())
        transac = {
            "empresa": empresa,
            "descripcion": d,
            "comprobante": x["C"],
            "tipo": x["E"],
            "moneda": "UYU",
            "source": source,
            "referencia": x["D"],
            "anulado": x["L"],
            "importe": float(x["G"]),
        }

        fecha: datetime.datetime = parse(x["A"])
        transac["fecha_mov"] = fecha.strftime("%d/%m/%Y")
        print(transac)
        data.append(transac)

    return ConciliacionesAPI().transacciones_erp(data)


def send_cuentas_erp(cuentas):
    data = []
    for x in cuentas:
        s = {
            "nombre": x["cuenta"],
            "descrip": x["nombre"],
            "empresa": int(x["empresa"]),
        }

        data.append(s)

    # return data
    return ConciliacionesAPI().cuentas_erp(data)


def get_transacciones_erp(empresa):
    response = ConciliacionesAPI().get_transacciones_to_change(empresa)
    return response.json()


def set_conciliacion_app(id, empresa):
    return ConciliacionesAPI().set_conciliacion(id, empresa)


#
if __name__ == "__main__":
    r = ConciliacionesAPI()
    r.authenticate()
    # str = "TRANSFERENCIA\nCAJA 77 11/08/2021"
    #
    # d = str.replace("\n", " ")
    # # d=" ".join(d.split())
    # print(str)
    # print(d)
    # response = r.cuentas_erp(
    # [{'cuenta': '50001', 'nombre': 'BANK BOSTON'}, {'cuenta': '23598573', 'nombre': 'BBVA PESOS 23598573'}])
    # print(response)
