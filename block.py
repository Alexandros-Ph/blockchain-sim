import hashlib
from time import ti

class Block(object):
    # Initialize a block
    def __init__(self, index, prev_hash):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.nonce = int()
        self.current_hash = str()
        self.previous_hash = prev_hash

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    def validate_block(block, prev_hash):
        # Validates current and previous hash of Block
        pass

    
