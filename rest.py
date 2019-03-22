import requests
from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS
import json


import block
import blockchain as bl_ch
import wallet as wl
import transaction as tr
import settings as st
import init


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK


app = Flask(__name__)
CORS(app)


#.......................................................................................



# get all transactions in the blockchain
'''
@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200
'''

@app.route('/transaction/get', methods=['POST'])
def reciever():
    if not request.json:
        abort(400)
    #print(request.json)
    data = json.loads(json.dumps(request.json))    # dictionary
    temp_trans = tr.Transaction(data['sender'], data['recipient'], None, data['amount'], data['inputs'], data['outputs'], data['id'], data['signature'])
    for j in range (3):
        if (temp_trans.sender==st.wallets[j].public_key):
            send_id = j
        if (temp_trans.recipient==st.wallets[j].public_key):
            rec_id = j
    print(tr.Transaction.validate_transaction(temp_trans, send_id, rec_id))
    return json.dumps(data)

@app.route('/wallet/get', methods=['POST'])
def rec_key():
    if not request.json:
        abort(400)
    #print(request.json)
    data = json.loads(json.dumps(request.json))    # dictionary
    temp_wall = wl.Wallet(None, data['public_key'], data['utxos'])
    st.ids.append(data['node_id'])
    print (vars(temp_wall))
    st.wallets.append(temp_wall)
    if (len(st.wallets)==st.n):
        for wall in st.wallets:
            print(vars(wall))
            init.wall_list.append(vars(wall))
        print(st.ids)
    #    return st.broadcast(init.wall_list, "wallet/all", st.ips[st.my_id])
    return "Wallet ok"

@app.route('/wallet/all', methods=['POST'])
def rec_wall():
    if not request.json:
        abort(400)
    #print(request.json)
    data = json.loads(json.dumps(request.json))    # list
    for wall in data:
        print(wall)
    for wall in data:
        temp_wall = wl.Wallet(None, wall['public_key'], wall['utxos'])
        st.wallets.append(temp_wall)
    print(st.wallets)
    return json.dumps(data)


# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='localhost', port=5000, threaded=True)
