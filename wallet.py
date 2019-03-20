import Crypto
from Crypto.PublicKey import RSA


class Wallet(object):

    def __init__(self):
        # Initialize a Wallet
        rsa_key = RSA.generate(1024)
        self.private_key = rsa_key.exportKey('PEM').decode()
        self.public_key = rsa_key.publickey().exportKey('PEM').decode()
        self.budget = 0
        self.utxos = []
