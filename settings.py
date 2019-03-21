import requests

difficulty = 3
n = 5
capacity = 5
my_id = 1

def broadcast(something):
    url = "http://83.212.108.105:5000/transaction/get"
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=something, headers=headers)
    if (r.status_code == 200):
        return "Transaction recieved"
    else:
        return f"Transaction not recieved, reason: {r.reason}, status code: {r.status_code}"
