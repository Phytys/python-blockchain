from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.config import STRATING_BALANCE

def test_verify_valid_signature():
    data = {"foo": "test_data"}
    wallet = Wallet()
    signature = wallet.sign(data)
    public_key = wallet.public_key

    assert Wallet.verify(public_key, data, signature) == True

def test_verify_invalid_signature():
    data = {"foo": "test_data"}
    fake_data = {"foo": "fake_test_data"}
    wallet = Wallet()
    fake_signature = wallet.sign(fake_data)
    signature = wallet.sign(data)
    public_key = wallet.public_key

    # wrong pub key
    assert Wallet.verify(Wallet().public_key, data, signature) == False
    # wrong signature
    assert Wallet.verify(public_key, data, fake_signature) == False
    # wrong data
    assert Wallet.verify(public_key, fake_data, signature) == False


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()
    other_wallet = Wallet()
    # Starting balance
    assert wallet.calculate_balance(blockchain, wallet.address) == STRATING_BALANCE

    amount = 100
    transaction = Transaction(wallet, other_wallet.address, amount)
    blockchain.add_block([transaction.to_json()])
    # When wallet sends coins
    assert wallet.calculate_balance(blockchain, wallet.address) == STRATING_BALANCE - amount

    amount_2 =125
    amount_3 = 50
    transaction_2 = Transaction(other_wallet, wallet.address, amount_2)
    transaction_3 = Transaction(other_wallet, wallet.address, amount_3)
    blockchain.add_block([transaction_2.to_json(), transaction_3.to_json()])
    # When wallet receives coins
    assert wallet.calculate_balance(blockchain, wallet.address) == \
        STRATING_BALANCE - amount + amount_2 + amount_3
