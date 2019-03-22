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
    print(tr.Transaction.validate_transaction(temp_trans, 0, 1))
    return json.dumps(data)

@app.route('/wallet/get', methods=['POST'])
def rec_key():
    if not request.json:
        abort(400)
    #print(request.json)
    data_key = json.loads(json.dumps(request.json))    # dictionary
    temp_wall = wl.Wallet(None, data['public_key'], data['utxos'])
    print (vars(temp_wall))
    init.wallets.append(temp_wall)
    if (len(init.wallets)==st.n):
        init.wallets.sort(key=lambda x: x.utxos[0])
        print(init.wallets)
    return json.dumps(data_key)


# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host=st.ips[st.my_id], port=5000)
