import json
import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64


def create_transaction(sender_wallet, recipient_public, amount):
    sum = 0
    inputs = []
    i=0
    try:
        if (sender_wallet.budget < amount):
            raise Exception("Not enough money")

        while (sum < amount):
            sum += sender_wallet.utxos[i]["amount"]
            inputs.append(i)
            i+=1

        trans = Transaction(sender_public, recipient_public, amount, inputs)
        trans.sign()

        return trans

    except Exception as e:
        print(f"create_transaction: {e.__class__.__name__}: {e}")
        return None

class Transaction(object):

    def __init__(self, sender, recipient, amount, inputs, id=None, signature=None):
        # Initialize a transaction
        self.sender = sender                #sender's public key
        self.recipient = recipient          #recipient's public key
        self.sender_private_key = str()
        self.amount = amount
        self.inputs = inputs                #list of UTXOs
        self.id = id
        self.signature = signature
        self.outputs = []


    def hash(self):
        '''convert to json string to calculate hash'''
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.inputs}".encode()
        #hash the transaction
        return SHA256.new(transaction_string)

    def sign(self):
        """
        Sign transaction with private key
        """
        hash_obj = self.hash()
        private_key = RSA.importKey(self.sender_private_key)
        signer = PKCS1_v1_5.new(private_key)
        self.id = hash_obj.hexdigest()
        self.signature = base64.b64encode(signer.sign(hash_obj)).decode()
        return self.signature

    def verify_signature(self):
        """
        verify the signature of input transaction
        """
        rsa_key = RSA.importKey(self.sender.encode())
        verifier = PKCS1_v1_5.new(rsa_key)

        hash_obj = self.hash()
        return verifier.verify(hash_obj, base64.b64decode(self.signature))

    def create_genesis_transaction(self, num_nodes, sender, sender_private_key):
         t = Transaction(
            sender = sender,
            recipient = sender,
            sender_private_key = sender_private_key,
            amount = 100*num_nodes,
            inputs = []
        )
         t.sign()

         t.outputs = [{
            'id': t.id,
            'to_who': t.sender,
            'amount': t.amount
            }]
         return t


"""for testing"""
private_key = RSA.generate(1024)
privkey = private_key.exportKey('PEM').decode()
pubkey = private_key.publickey().exportKey('PEM').decode()
temp = Transaction(pubkey,2,privkey,10,[])
# print(privkey)
# first = temp.create_genesis_transaction(7, pubkey, privkey)
print(temp.sign())
print(temp.verify_signature())
print(vars(temp))
