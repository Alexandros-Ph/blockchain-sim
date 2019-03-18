import hashlib
import json
from time import time

class Block(object):

    def __init__(self, index, transactions, prev_hash):
        # Initialize a block
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.nonce = int()
        self.current_hash = str()
        self.previous_hash = prev_hash


    def hash(self):
        # Creates a SHA-256 hash of a Block
        block_dict = vars(self)                                             # object to dictionary conversion
        if 'current_hash' in block_dict:
            del block_dict['current_hash']                                  # delete current hash key from dictionary
        block_string = json.dumps(block_dict, sort_keys=True).encode()      # dictionary to string conversion
        return hashlib.sha256(block_string).hexdigest()                     # string to sha256 hash


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


    def broadcast_block(self):

        pass

# for testing purposes:
'''
temp = Block(1, [], 1995)
#print(vars(temp))
#temp.current_hash = temp.hash()
print(vars(temp))
#print(temp.validate_block(1995))
print(temp.mine_block(3))
print(vars(temp))
'''
