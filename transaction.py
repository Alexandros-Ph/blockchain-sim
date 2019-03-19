import hashlib
import json
import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import base64


class Transaction(object):

    def __init__(self, sender, recipient, sender_private_key, amount, inputs, id=None, signature=None):
        # Initialize a transaction
        self.sender = sender
        self.recipient = recipient
        self.sender_private_key = sender_private_key
        self.amount = amount
        self.inputs = inputs
        self.id = id
        self.signature = signature
        self.outputs = []


    def to_dict(self):
        #convert transaction to dict without sender's private key
        return dict(
            sender=self.sender,
            recipient=self.recipient,
            amount=self.amount,
            inputs=self.inputs,
            id=self.id,
            signature=self.signature
        )

    def hash(self):
        '''convert to json string to calculate hash'''
        transaction_string = json.dumps(dict(
            sender=self.sender,
            recipient=self.recipient,
            amount=self.amount,
            inputs=self.inputs,
            ), sort_keys=True).encode()
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
# private_key = RSA.generate(1024)
# privkey = private_key.exportKey('PEM').decode()
# pubkey = private_key.publickey().exportKey('PEM').decode()
# temp = Transaction(pubkey,2,privkey,10,[])
# # print(privkey)
# first = temp.create_genesis_transaction(7, pubkey, privkey)
# print(temp.sign())
# print(temp.verify_signature())
