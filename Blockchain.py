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
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests



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
        The str object's encode() can be used to convert from default Unicode encoding to byte litral.
        json.dumps() function converts the python dictornary into a jason file (sorted) 
        json.loads() does the reverse i.e. converts a json structure in python dictonary
        
        About SHA256 hashing:
        The SHA (Secure Hash Algorithm) is a cryptographic hash functions. SHA-256 algorithm generates an unique, 
        fixed size 256-bit (32-byte) hash.
        SHA256 method of hashlib library converts a string to SHA256 hashing and stores as a memory address
        The hexdigest of the memory gives the hash as
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

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        '''
        What is Proof of Work (POW): 
        Proof of work is a puzzle that needs to be solved in order to mine the coin. The solution to the puzzle 
        should be difficult to find bu easy to verify.
        
        Why We need Proof of Work (POW) :
        There will be many miners who will be working to add a block to the blockchain for the reward.
        Whoever solves this puzzle (POW) first and broadcast it to the network gets to add the block and receive the reward
        
        POW principle: 
        Given a number (Say N1) , find another number (say N2) such that a combined operation invvolvin two numbers
        (say N1 X N2) has a particular pattern (say end in 0). Once the puzzle is solved, for next round N2 becomes N1 and N2 needs to be
        found. 
        e.g. Situation 1: reuires the pattern to end in one 0.
        Round 1: N1 = 5, then N2 is 2 so that N1XN2 is 10 with last digit as 0 (the loop has to run twice to achieve the result)
        Round 2: N1 = 10, then N2 has to be 1 so that N1XN2 ends in 0
        Roud 3:  N1 = 1 , then N2 has to be 10 so that N1XN2 ends in 0
        
        Situation 2: to increase the difficulty of puzzle we say that the result should have  two zeroes at end instead of one i.e 00.
        N1 = 5, then N2 is 20 so that N1XN2 is 100 with last two digit 00  (the loop has to run 20 times)
        Round 2: N1 = 100, then N2 has to be 1 so that N1XN2 ends in 00
        Roud 3: N1 = 1 , then N2 has to be 100 so that N1XN2 ends in 00
        
        When difficulty is increased in second situation, the program has to run 10 times more to find the result for round 1 
        compared to 10 times in first situation. If we increase the difficulty by making the pattern match to three zeroes i.e. 000
        the the loop needs to run 200 time in round 1 to find 1000. 
        
        The above example is for understandig purpose. For blockchain, instead of simple operation (N1XN2) we use the hash of the 
        operation. This makes the problem computationally very difficult.
         >>> hashlib.sha256(f'{N1*N2}'.encode()).hexdigest()[-1] == 0
        
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
