import requests
from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn

__all__ = ["get_driver", "quit", "get_downloaded_files"]

load_dotenv()  # take environment variables from .env.


def get_driver():
    selib = BuiltIn().get_library_instance("RPA.Browser.Selenium")
    return selib.driver


def quit(session_id, hostname):
    selib = BuiltIn().get_library_instance("RPA.Browser.Selenium")
    selib.driver.close()
    # http://grid.rpamaker.com:4444/session/5714a2f01fbfe582204b1061a45a44db
    session_url = hostname + "/session/" + session_id
    response = requests.delete(session_url, verify=False)

    # selib.driver.quit()


def get_downloaded_files():
    driver = get_driver()
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")

    return driver.execute_script(
        "return  document.querySelector('downloads-manager')  "
        " .shadowRoot.querySelector('#downloadsList')         "
        " .items.filter(e => e.state === 'COMPLETE')          "
        " .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url); "
    )
