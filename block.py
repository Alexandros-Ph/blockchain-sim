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
        block_dict = self.__dict__                                          # object to dictionary conversion
        del block_dict['current_hash']                                      # delete current hash key from dictionary
        block_string = json.dumps(block_dict, sort_keys=True).encode()      # dictionary to string conversion
        return hashlib.sha256(block_string).hexdigest()                     # string to sha256 hash


    def validate_block(self, prev_hash):
        # Validates current and previous hash of Block
        x = (self.previous_hash == prev_hash)
        y = (self.current_hash == self.hash())
        return (x and y)

'''
temp = Block(1, [], 1995)
print(vars(temp))
temp.current_hash = temp.hash()
print(vars(temp))
print(temp.validate_block(1995))
'''
