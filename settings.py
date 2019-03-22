import requests
wallets=[]
difficulty = 3
n = 3
capacity = 5
my_id = 0
ips = ["localhost:5000","localhost:5002","localhost:5001"]
ids = []
r=[0, 0, 0]

def broadcast(something, url, exclude):
    status=[]
    i=0
    for ip in ips:
        if (ip==exclude):
            continue
        print(ip)
        url = f"http://{ip}/{url}"
        headers = {'Content-type': 'application/json'}
        r[i] = requests.post(url, json=something, headers=headers)
        if (r[i].status_code == 200):
            status.append("Recieved")
        else:
            status.append(f"Not recieved, reason: {r[i].reason}, status code: {r[i].status_code}")
        i+=1
    return status

def send(something, url, node_ip):
    url = f"http://{node_ip}/{url}"
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=something, headers=headers)
    if (r.status_code == 200):
        return r.content
    else:
        return f"Not recieved, reason: {r.reason}, status code: {r.status_code}"
