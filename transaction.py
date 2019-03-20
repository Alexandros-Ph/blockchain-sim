import json

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
            inputs.append(sender_wallet.utxos[i])
            i+=1

        trans = Transaction(sender_wallet.public_key, recipient_public, sender_wallet.private_key, amount, inputs)
        trans.sign()
        if (sum > amount):      #in case of having utxos' sum bigger than transaction's amount
            trans.outputs.append({
                'id': trans.id,
                'to_who': trans.sender,
                'amount': sum - trans.amount
            })
        trans.outputs.append({
           'id': trans.id,
           'to_who': trans.recipient,
           'amount': trans.amount
           })
        return trans

    except Exception as e:
        print(f"create_transaction: {e.__class__.__name__}: {e}")
        return None

class Transaction(object):

    def __init__(self, sender, recipient, sender_private_key, amount, inputs, id=None, signature=None):
        # Initialize a transaction
        self.sender = sender                #sender's public key
        self.recipient = recipient          #recipient's public key
        self.sender_private_key = sender_private_key
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

    @staticmethod
    def create_genesis_transaction(num_nodes, bootstrap_wallet):
         t = Transaction(str(), bootstrap_wallet.public_key, str(), 100*num_nodes, [])

         t.outputs = [{
            'id': t.id,
            'to_who': bootstrap_wallet.public_key,
            'amount': 100*num_nodes
            }]
         bootstrap_wallet.utxos.append(t.outputs)
         bootstrap_wallet.budget = 100*num_nodes
         return t


"""for testing"""

# print(vars(create_transaction(Wallet(), 9, 40)))
# private_key = RSA.generate(1024)
# privkey = private_key.exportKey('PEM').decode()
# pubkey = private_key.publickey().exportKey('PEM').decode()
# temp = Transaction(pubkey,2,privkey,10,[])
# print(privkey)
# first = temp.create_genesis_transaction(7, pubkey, privkey)
# print(temp.sign())
# print(temp.verify_signature())
# print(vars(temp))
