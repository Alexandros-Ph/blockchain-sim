import requests

difficulty = 3
n = 5
capacity = 5
my_id = 0
ips = ["192.168.0.1","192.168.0.2","192.168.0.3","192.168.0.4","192.168.0.5"]

def broadcast(something, url):
    status=[]
    for ip in ips:
        url = f"http://{ip}:5000/{url}"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, json=something, headers=headers)
        if (r.status_code == 200):
            status.append("Recieved")
        else:
            status.append(f"Not recieved, reason: {r.reason}, status code: {r.status_code}")
    return status

def send(something, url, node_id):
    url = f"http://{ips[node_id]}:5000/{url}"
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=something, headers=headers)
    if (r.status_code == 200):
        status.append("Recieved")
    else:
        status.append(f"Not recieved, reason: {r.reason}, status code: {r.status_code}")
    return status
