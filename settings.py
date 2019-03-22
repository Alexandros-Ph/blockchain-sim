import requests

difficulty = 3
n = 4
capacity = 5
my_id = 0
ips = ["192.168.0.1","192.168.0.3","192.168.0.4","192.168.0.5"]
ids = []

def broadcast(something, url, exclude):
    status=[]
    for ip in ips:
        if (ip==exclude):
            continue
        url = f"http://{ip}:5000/{url}"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, json=something, headers=headers)
        if (r.status_code == 200):
            status.append("Recieved")
        else:
            status.append(f"Not recieved, reason: {r.reason}, status code: {r.status_code}")
    return status

def send(something, url, node_ip):
    url = f"http://{node_ip}:5000/{url}"
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=something, headers=headers)
    if (r.status_code == 200):
        return r.content
    else:
        return f"Not recieved, reason: {r.reason}, status code: {r.status_code}"
