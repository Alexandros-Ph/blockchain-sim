import json

import wallet
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
        transaction_string = f'{self.sender}{self.recipient}{self.amount}{self.inputs}'.encode()
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
    def validate_transaction(trans, sender_id, receiver_id): #wallet_id is sender's id
        trans.verify_signature()          # a)validation of Signature

        verified_amount = 0
        for i in trans.inputs:                 # b)verify that inputs are current utxos of sender
            verified = False
            for c_utxos in wallets[sender_id].utxos:
                if (i['id'] == c_utxos['id'] and sender_id == c_utxos['to_who']):  #the input is verified as utxo
                    verified = True
                    verified_amount  += c_utxos['amount']
                    wallets[sender_id].utxos.remove(c_utxos)
                    break
            if (not verified): #in case that an input is not verified
                raise Exception('Input is not a UTXO')

        # if verified inputs are not enough for the transaction
        if verified_amount < trans.amount:
             raise Exception('Not enough money')

        #create transaction outputs
        temp = []
        if (verified_amount > trans.amount):      #in case of having utxos' sum bigger than transaction's amount
            temp.append({
                'id': trans.id,
                'to_who': trans.sender,
                'amount': verified_amount - trans.amount
            })
        temp.append({
           'id': trans.id,
           'to_who': trans.recipient,
           'amount': trans.amount
           })

        if (temp != trans.outputs):
             raise Exception('Wrong outputs')

        #insert outputs in UTXOs
        if(len (trans.outputs) == 2):
            wallets[sender_id].utxos.append(trans.outputs[0])
            wallets[receiver_id].utxos.append(trans.outputs[1])
        else:
            wallets[receiver_id].utxos.append(trans.outputs[0])

        return 'validated',trans



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


wallets = []
w = wallet.Wallet()
w.budget = 100
w.utxos=[{'id': 23,
    'to_who': 1,
    'amount': 40
    },{'id': 24,
    'to_who': 1,
    'amount': 60
    }]
wallets.append(w)
w2 = wallet.Wallet()
w2.budget = 50
w2.utxos=[{'id': 23,
    'to_who': 2,
    'amount': 30
    },{'id': 24,
    'to_who': 2,
    'amount': 20
    }]
wallets.append(w2)
# print(wallets[0].utxos)
temp = create_transaction(w, w2.public_key, 10)
# print(vars(temp))
msg, t = Transaction.validate_transaction(temp, 1, 2)
print(msg)


# print(privkey)
# first = temp.create_genesis_transaction(7, pubkey, privkey)
# print(temp.sign())
# print(temp.verify_signature())
# print(vars(temp))
