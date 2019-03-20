import json
import wallet as wl
import transaction as tr
import settings as sets
import block as bl
#from uuid import uuid4

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

    @staticmethod
    def genesis_chain(wallets):
        genesis_transaction = tr.Transaction.create_genesis_transaction(sets.n, wallets[0])
        genesis_block = bl.Block.create_genesis_block(genesis_transaction)
        start_chain = Blockchain()
        start_chain.chain.append(genesis_block)
        return start_chain

    def append_block(self):
        # Creates and Adds a block to the chain
        block = Block(len(self.chain), self.current_transactions[:capacity], self.last_block().current_hash)

        del self.current_transactions[:capacity]
        self.chain.append(block)
        return block


    def validate_chain(self):
        # Calls validate block for every block of the validate_chain
        for i in range (1, len(self.chain)):
            current_block = self.chain[i]
            previous_block_hash = self.chain[i-1].hash
            if ( not validate_block(current_block,previous_block_hash)):
                return False
        return True

    @property
    def last_block(self):
        return self.chain[-1]


""" testing
w = wl.Wallet()
wallets = [w]
s = Blockchain.genesis_chain(wallets)
print(len(s.chain))
print(vars(s.chain[0]))
print(len(s.chain[0].transactions))
print(vars(s.chain[0].transactions[0]))
print(vars(w))
"""
