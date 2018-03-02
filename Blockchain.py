'''
The initial code taken from Medium article @ https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
Orginally posted on Medium by Daniel van Flymen
Github: https://github.com/dvf/blockchain
'''


import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask


class Blockchain(object):

    def __init__(self):
        # List to store the blocks chain
        self.chain = []

        # List to store Transactions
        self.current_transactions = []

        # Create the genesis block. Gensis block is the first block in the chain with no predecessor.
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
                Create a new Block in the Blockchain
                :param proof: <int> The proof given by the Proof of Work algorithm
                :param previous_hash: (Optional) <str> Hash of previous Block
                :return: <dict> New Block
                """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        """
                Creates a new transaction to go into the next mined Block
                :param sender: <str> Address of the Sender
                :param recipient: <str> Address of the Recipient
                :param amount: <int> Amount
                :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    ''' 
    --- START: DECORATOR EXPLANATION ------------------
        testing git
        @ signifies a decorator which is used before a function definition as shown
        
        def decorator(func):
            return func
    
        @decorator
        def some_func():
            pass
    
        This is equivalent to
    
        def decorator(func):
            return func
    
        def some_func():
            pass
            
        some_func = decorator(some_func)
     --- END : DECORATOR EXPLANATION ------------------ 
     '''

    '''
       --- START : staticmethod DECORATOR EXPLANATION ----------------
       The below code is equivalent to 
       hash = staticmethod(hash)
       --- END : staticmethod DECORATOR EXPLANATION ------------------
       '''
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        '''
        About Encoding:
        the defualt python string are stored as Unicode object where non ASCII character are strored as hexadecimal.
        The str object's encode() can be used to convert from default Unicode encoding to byte litral
        
        About SHA256 hashing:
        SHA256 method of hashlib library converts a string to SHA256 hashing and stores as a memory address
        The hexdigest of the memory gives the hash
        >>> "prashant".encode()
        b'prashant'
        >>> hashlib.sha256("prashant".encode())
        <sha256 HASH object @ 0x03B3BCF8>
        >>> hashlib.sha256("prashant".encode()).hexdigest()
        'f173b46b650d9708d31b642021d04ed380c54db71fc9f0ab829d1c2597d37f3d'
        '''
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()



    @property
    def last_block(self):
        return self.chain[-1]

