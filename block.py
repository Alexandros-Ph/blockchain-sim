import json
from time import time
from Crypto.Hash import SHA256

class Block(object):

    def __init__(self, index, transactions, prev_hash):
        # Initialize a block
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.nonce = int()
        self.current_hash = str()
        self.previous_hash = prev_hash

    @staticmethod
    def create_genesis_block(genesis_transaction):
        g_b = Block(0, [genesis_transaction], 1)
        return g_b

    def hash(self):
        # Creates a SHA-256 hash of a Block
        # object to string conversion:
        temp_string = f"{self.index}{self.timestamp}{self.transactions}{self.nonce}{self.previous_hash}"
        block_string = temp_string.encode()                              # encode string
        return SHA256.new(block_string).hexdigest()                      # string to sha256 hash


    def mine_block(self, diff):
        # Increment nonce till hash is valid
        self.nonce = 0
        guess = self.hash()
        while guess[:diff]!=('0'*diff):         # check if first X characters are zero, where X = diffculty
            self.nonce += 1
            guess = self.hash()
        self.current_hash = guess               # set the valid hash as block's current hash
        return self.nonce


    def validate_block(self, prev_hash):
        # Validates current and previous hash of Block
        x = (self.previous_hash == prev_hash)
        y = (self.current_hash == self.hash())
        return (x and y)


# for testing purposes:

#temp = Block(1, [], 1995)
#print(vars(temp))
#temp.current_hash = temp.hash()
#print(vars(temp))
#print(temp.validate_block(1995))
#print(temp.mine_block(3))
#print(vars(temp))
