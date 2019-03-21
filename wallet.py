import Crypto
from Crypto.PublicKey import RSA


class Wallet(object):

    def __init__(self, private_key, public_key, utxos):
        # Initialize a Wallet
        self.private_key = private_key
        self.public_key = public_key
        self.utxos = utxos
        sum = 0
        for i in self.utxos:
            sum += self.utxos['amount']
        self.budget = sum
