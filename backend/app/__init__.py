from flask import Flask, jsonify, request
import os
import random
import requests
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain) # So balance always available
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route("/")
def route_default():

    return "Welcome to the blockchain"


@app.route("/blockchain")
def route_blockchain():

    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine():
    # Get transaction data from pool
    transaction_data = transaction_pool.transaction_data()
    # Append mining reward
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    # Mine block
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())


@app.route("/wallet/transact", methods=["POST"])
def route_wallet_transact():
    # Data posted as json, getting this data
    transaction_data = request.get_json()

    transaction = transaction_pool.existing_transaction(wallet.address)

    # Existing transaction? find if address already posted a transaction
    if transaction:
            transaction.update(
            wallet,
            transaction_data["recipient"],
            transaction_data["amount"]
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data["recipient"],
            transaction_data["amount"]
        )

    # Broadcasting transaction
    pubsub.broadcast_transaction(transaction)
    # NOTE Set transaction in own transaction pool since not broadcasting to self
    # In pubsub.py we are unsubscribing temporarly while publishing"
    transaction_pool.set_transaction(transaction)
    
    return jsonify(transaction.to_json())


@app.route("/wallet/info")
def route_wallet_info():
    return jsonify({
        "address": wallet.address,
        "balance": wallet.balance
    })


ROOT_PORT = 5000
PORT = ROOT_PORT
# Run a peer instance on a random port
if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)

    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    #print(f"result.json(): {result.json()}")

    result_blockchain = Blockchain.from_json(result.json())

    # Replace chain after validation
    try: 
        blockchain.replace_chain(result_blockchain.chain)
        print("\n -- Successfully synced local chain")
    except Exception as e:
        print(f"\ -- Error tying to sync: {e}")

app.run(port=PORT)