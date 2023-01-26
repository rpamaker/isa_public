import requests
from robot.libraries.BuiltIn import BuiltIn


# +
# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# +


# def get_file(path, file):
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     pem = paramiko.RSAKey.from_private_key_file(PATH_PK)

#     ssh.connect("50.17.126.196", username="ubuntu", pkey=pem)
#     sftp = ssh.open_sftp()
#     sftp.get(path, "/home/downloads/" + file)

#     sftp.close()
#     ssh.close()


def get_session_ip_test(session_id, hostname):
    session_url = hostname + "/grid/api/testsession?session=" + session_id
    response = requests.get(session_url, verify=False)
    json_response = response.json()
    if json_response["success"]:
        return json_response["proxyId"]
    raise Exception("Failed to retrieve session ip")


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
