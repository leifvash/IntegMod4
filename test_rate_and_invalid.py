import requests, time

URL = "http://127.0.0.1:8000/api/payment-records/"
HEADERS = {"Content-Type": "application/json"}

invalid_body = {"card_number": "INVALID_PAYLOAD"} 
valid_body = {"card_number": "4111111111111111"}

#send invalid payload first
r = requests.post(URL, json=invalid_body, headers=HEADERS)
print("invalid:", r.status_code, r.text)

#small pause to ensure server processed and logged
time.sleep(1)

for i in range(7):   # if rate is 5/m, 6th should be 429
    r = requests.post(URL, json=valid_body, headers=HEADERS)
    print(f"{i+1}:", r.status_code)
    time.sleep(1)
