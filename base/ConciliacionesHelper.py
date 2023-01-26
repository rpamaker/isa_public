import logging
import traceback
from logging import info, exception
from time import sleep

from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def get_driver():
    selib = BuiltIn().get_library_instance('RPA.Browser.Selenium')
    return selib.driver


def get_value_from_element(element: WebElement):
    try:
        elem = element.find_element(By.XPATH, 'center/input')
        return elem.get_attribute('value')
    except:
        exception('Something went wrong while fetching the value')
        return ''


def get_select_from_element(element: WebElement):
    elem = element.find_element(By.XPATH, 'center/select')
    return Select(elem)


def get_selected_value_from_element(element: WebElement):
    elem = element.find_element(By.XPATH, 'center/select')
    return Select(elem).first_selected_option.text


class ConciliacionesRow:
    def __init__(self, driver, cols):
        self.tipo = get_selected_value_from_element(cols[0])[:-5]
        self.fecha_emision = cols[1].text[:10]
        self.consolidada_select = get_select_from_element(cols[3])
        # self.serie = cols[4].text
        self.comprobante = get_value_from_element(cols[5])
        self.descripcion = get_value_from_element(cols[6])
        self.ingreso = get_value_from_element(cols[8])
        self.egreso = get_value_from_element(cols[9])
        # info('***PRESTRN***')
        # info(vars(self))
        self.ingreso = str_num_to_float(self.ingreso)
        self.egreso = str_num_to_float(self.egreso)
        # info('***CONCILIACIONES_VARS***')
        # info(vars(self))
        # self.conciliar()
        # self.saldo = cols[10]

    def conciliar(self):
        self.consolidada_select.select_by_value('true')
        sleep(1)

    def get_dict(self):
        return {
            "fecha_mov": self.fecha_emision,
            "descripcion": self.descripcion.strip(),
            "comprobante": self.comprobante.strip(),
            "debito": self.egreso,
            "credito": self.ingreso,
            "tipo": self.tipo
        }

    def compare_and_conciliate(self, movimientos):
        match = False
        if self.get_dict() in movimientos:
            self.conciliar()
            info('MATCH!!')
            match = True
            # info(self.get_dict())
        return match


class ConciliacionesTable:

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.table = driver.find_element(By.XPATH, "//*[@id='Form:panelTabla']/table")
        self.head = self.table.find_element(By.XPATH, "thead")
        # info('THEAD ')
        # info(self.head.text)
        self.headers = self.head.find_elements(By.XPATH, "tr/th")
        # info('THEADS CONTENT')
        # info(self.headers)
        self.body = self.table.find_element(By.XPATH, "tbody")
        # info('TBODY CONTENT')
        # info(self.body.text)

    def conciliar(self, movimientos):
        next_page = True
        save = False
        try:
            while next_page:
                rows_index = self.get_rows_pos()
                for row_index in rows_index:
                    row = self.get_rows()[row_index]
                    cols = row.find_elements(By.XPATH, 'td')
                    row_obj = ConciliacionesRow(self.driver, cols)
                    # info('FINAL OBJECT')
                    #                info(vars(row_obj))
                    match = row_obj.compare_and_conciliate(movimientos)
                    if match:
                        save = True

                next_btn = self.driver.find_elements(By.XPATH,
                                                     "//table[@id='Form:scroller_table']//td[last()-1][not(contains(@class,'dsbld'))]")
                if next_btn:
                    next_btn[0].click()
                    sleep(2)

                else:
                    next_page = False

            info(save)
            if save:
                guardar_btn = self.driver.find_element(By.ID, 'Form:btnGuardar')
                guardar_btn.click()
                sleep(2)
                aceptar_btn = self.driver.find_element(By.ID, 'formMensajes:j_id385')
                aceptar_btn.click()
        except Exception as err:
            logging.error(traceback.format_exc())
            raise err

    def get_rows_pos(self):
        rows = self.driver.find_elements(By.XPATH, "//*[@id='Form:panelTabla']/table/tbody/tr")
        rows_pos = list(range(0, len(rows)))
        # info(rows)
        # info(rows_pos)
        # info(len(rows))
        return rows_pos

    def get_rows(self):
        rows = self.driver.find_elements(By.XPATH, "//*[@id='Form:panelTabla']/table/tbody/tr")
        return rows


def str_num_to_float(str_num):
    # info('***str_num***')
    # info(str_num)
    num = float(str_num.replace('.', '').replace(',', '.'))
    # return str(num)
    return num


def conciliar_transacciones(movimientos):
    movimientos_updated = [
        {
            "fecha_mov": x['fecha_mov'],
            "descripcion": x['descripcion'],
            "comprobante": x['comprobante'],
            "debito": float(x['debito']),
            "credito": float(x['credito']),
            "tipo": x['tipo']
        }
        for x in movimientos
    ]

    driver: webdriver.Chrome = get_driver()
    table = ConciliacionesTable(driver=driver)
    info(movimientos_updated)
    table.conciliar(movimientos_updated)

    # ${columns}=  Get Element Count    xpath://*[@id='Form:panelTabla']/table/thead/tr/th
