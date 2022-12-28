import requests
import time
from backend.wallet.wallet import Wallet

## NOTE Testing the app. Make sure it is up and running on localhost

BASE_URL = "http://localhost:5000"

def get_blockchain():
    r = requests.get(f"{BASE_URL}/blockchain").json()
    return r

# to mine
def get_blockchain_mine():
    r = requests.get(f"{BASE_URL}/blockchain/mine").json()
    return r

# to post transaction
def post_wallet_transact(recipient, amount):
    p = requests.post(f"{BASE_URL}/wallet/transact",
        json={"recipient": recipient, "amount": amount}).json()
    return p

def get_wallet_info():
    r = requests.get(f"{BASE_URL}/wallet/info").json()
    return r


# View blockchain
start_blockchain = get_blockchain()
print(f"start_blockchain: {start_blockchain}")

recipent = Wallet().address

# post transaction 1
post_wallet_transact_1 = post_wallet_transact(recipent, 50)
print(f"\npost_wallet_transact_1: {post_wallet_transact_1}")

time.sleep(1)

# post transaction 2
post_wallet_transact_2 = post_wallet_transact(recipent, 52)
print(f"\npost_wallet_transact_2: {post_wallet_transact_2}")

time.sleep(1)

# Mine block
mine_block = get_blockchain_mine()
print(f"\nmine_block: {mine_block}")

# Wallet info
walletinfo = get_wallet_info()
print(f"\nWallet info: {walletinfo}")
