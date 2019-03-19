import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self,difficulty):
        self.difficulty = difficulty
        self.chain = []
        self.current_transactions = []
        self.append_block(previous_hash=1, nonce=0)

    def append_block(self, previous_hash, nonce):
        # Creates a new Block and adds it to the chain
        index = len(self.chain) + 1
        transactions = self.current_transactions
        block = Block(index,transactions,previous_hash)
        
        self.current_transactions = []
        self.chain.append(block)
        return block


    def add_transaction(self, sender_address, receiver_address, amount):
        self.current_transaction.append({
            'sender': sender_address,
            'recipient': receiver_address,
            'amount': amount,
        })
        return self.last_block['index'] +1



    def validate_chain(self):
        # Calls validate block for every block of the validate_chain
        for i in range (1,len(blockchain)):
            current_block = blockchain[i]
            previous_block_hash = blockchain[i-1].hash
            if (!validate_block(current_block,previous_block_hash)):
                return False
        reurn True

    @property
    def last_block(self):
        return self.chain[-1]

