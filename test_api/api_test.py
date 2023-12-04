import os
import sys
import logging
import requests
import json

# setting up a logger to log all requests and their responses
LOGPATH = os.getcwd() + "/log"

if not os.path.exists(LOGPATH):
    os.mkdir(LOGPATH)

log = logging.getLogger("")
log.setLevel(logging.INFO)
format = logging.Formatter("%(levelname)s - %(message)s")

log_file = os.path.join(LOGPATH, "test.log")

if os.path.exists(log_file):
    open(log_file, "w").close()

logging.basicConfig(
    filename=os.path.join(LOGPATH, "test.log"),
    filemode="a",
    format="- %(message)s",
)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

# change these variables for changing which ID to view
VENDOR_ID = 1
ORDER_ID = 1

# you can change this if you want
VENDOR_POST_DATA = {
    "name": "New Vendor",
    "contact_details": "New Vendor Contact",
    "address": "New Vendor Address"
}
VENDOR_UPDATE_DATA = {
    "address": "Updated Address"
}
ORDER_POST_DATA = {
    "items": {
        "item1": 5
    },
    "quantity": 5,
    "vendor": 5
}
ORDER_UPDATE_DATA = {
    "status": "completed",
    "quality_rating": 4
}


# adding all request URLs
TOKEN_URL = "http://127.0.0.1:8000/api/token/"
VENDORS_URL = "http://127.0.0.1:8000/api/vendors/"
VENDOR_URL = f"http://127.0.0.1:8000/api/vendors/{VENDOR_ID}"
PERFORMANCE_URL = f"http://127.0.0.1:8000/api/vendors/{VENDOR_ID}/performance"
ORDERS_URL = "http://127.0.0.1:8000/api/purchase_orders/"
ORDER_URL = f"http://127.0.0.1:8000/api/purchase_orders/{ORDER_ID}/"
ORDERS_BY_VENDOR_URL = f"http://127.0.0.1:8000/api/purchase_orders/?vendor={VENDOR_ID}"


# header for the requests
headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': 'Token 872dd00d594ff92c164fc20bcfcdaff402250e2e'}


def test():
    logging.info(f"GET {TOKEN_URL}")
    logging.info("")
    response = requests.get(TOKEN_URL)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {VENDORS_URL}")
    logging.info("")
    response = requests.get(VENDORS_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {VENDOR_URL}")
    logging.info("")
    response = requests.get(VENDOR_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"POST {VENDORS_URL}")
    logging.info("")
    response = requests.post(VENDORS_URL, headers=headers, data=json.dumps(VENDOR_POST_DATA))
    VARIABLE_ID = response.json().get("id")
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")
    
    logging.info(f"PUT {VENDORS_URL}%d/" % VARIABLE_ID)
    logging.info("")
    response = requests.put(VENDORS_URL + "%d/" % VARIABLE_ID, headers=headers, data=json.dumps(VENDOR_UPDATE_DATA))
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")
    
    logging.info(f"DELETE {VENDORS_URL}%d/" % VARIABLE_ID)
    logging.info("")
    response = requests.delete(VENDORS_URL + "%d/" % VARIABLE_ID, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info("NO CONTENT")


    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {ORDERS_URL}")
    logging.info("")
    response = requests.get(ORDERS_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {ORDER_URL}")
    logging.info("")
    response = requests.get(ORDER_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {ORDERS_BY_VENDOR_URL}")
    logging.info("")
    response = requests.get(ORDERS_BY_VENDOR_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"POST {ORDERS_URL}")
    logging.info("")
    response = requests.post(ORDERS_URL, headers=headers, data=json.dumps(ORDER_POST_DATA))
    VARIABLE_ID = response.json().get("id")
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")
    
    logging.info(f"PUT {ORDERS_URL}%d/" % VARIABLE_ID)
    logging.info("")
    response = requests.put(ORDERS_URL + "%d/" % VARIABLE_ID, headers=headers, data=json.dumps(ORDER_UPDATE_DATA))
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"POST {ORDERS_URL}%d/acknowledge/" % VARIABLE_ID)
    logging.info("")
    response = requests.post(ORDERS_URL + "%d/acknowledge/" % VARIABLE_ID, headers=headers, data=None)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))

    logging.info("")
    logging.info("")
    logging.info("")
    
    logging.info(f"DELETE {ORDERS_URL}%d/" % VARIABLE_ID)
    logging.info("")
    response = requests.delete(ORDERS_URL + "%d/" % VARIABLE_ID, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info("NO CONTENT")

    logging.info("")
    logging.info("")
    logging.info("")

    logging.info(f"GET {PERFORMANCE_URL}")
    logging.info("")
    response = requests.get(PERFORMANCE_URL, headers=headers)
    logging.info(f"Response Code: {response.status_code}")
    logging.info(json.dumps(json.loads(response.text), indent=2))
    

test()