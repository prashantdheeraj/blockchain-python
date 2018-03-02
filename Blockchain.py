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

    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass

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

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    '''
    --- START : staticmethod DECORATOR EXPLANATION ----------------
    The above code is equivalent to 
    hash = staticmethod(hash)
    --- END : staticmethod DECORATOR EXPLANATION ------------------
    '''
    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

