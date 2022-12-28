import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

def test_transaction():
    sender_wallet = Wallet()
    recipient = "recipient"
    amount = 50

    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance -amount

    ## The input to the transaction
    # Time
    assert "timestamp" in transaction.input
    # Total amount that can be spent
    assert transaction.input["amount"] == sender_wallet.balance
    # Address and pub key
    assert transaction.input["address"] == sender_wallet.address
    assert transaction.input["public_key"] == sender_wallet.public_key

    # Verify signature based on the original public key and data
    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output, # transaction output is what is signed
        transaction.input["signature"]
    )

def test_transaction_exceed_balance():

    amount = 999
    # Check so you can not spend more then you have
    # In wallet STARTING_BALANCE was imported as 1000 from config
    assert amount < Wallet().balance

    with pytest.raises(Exception, match="Amount exceeds coin balance"):
        Transaction(Wallet(), "recipient", amount=1001)
        

def test_transaction_update_exceeds_balance():

    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "recipient", amount=50)
    
    with pytest.raises(Exception, match="Amount exceeds coin balance"):
        transaction.update(sender_wallet, "recipient", amount=951)
    
    with pytest.raises(Exception, match="Amount exceeds coin balance"):
        transaction.update(sender_wallet, "NEW_recipient", amount=951)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = "first_recipient"
    first_amount = 50
    next_recipient = "next_recipient"
    next_amount = 100

    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    # Ensure balance deducted with both original and updated amount
    assert transaction.output[sender_wallet.address] == \
         sender_wallet.balance - first_amount - next_amount

    # Verify signature after update (based on the original public key and data)
    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output, # transaction output is what is signed
        transaction.input["signature"]
    )

    change_first_amount = 25
    transaction.update(sender_wallet, first_recipient, change_first_amount)
    assert transaction.output[first_recipient] == first_amount + change_first_amount

     # Ensure balance deducted with both original and updated amount
    assert transaction.output[sender_wallet.address] == \
         sender_wallet.balance - first_amount - next_amount - change_first_amount
    
    # Verify signature again after update
    assert Wallet.verify(
        transaction.input["public_key"],
        transaction.output, # transaction output is what is signed
        transaction.input["signature"]
    )

def test_is_valid_transaction():

    Transaction.is_valid(Transaction(Wallet(), "recipient", 100))

def test_is_valid_transaction_invalid_output():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "recipient", 50)
    transaction.output[sender_wallet.address] = 1010
    with pytest.raises(Exception, match="Invalid transaction output values"):
        transaction.is_valid(transaction)

def test_is_valid_transaction_invalid_signature():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, "recipient", 50)
    transaction.input["signature"] = Wallet().sign("fake_output")
    with pytest.raises(Exception, match="Invalid signature"):
        transaction.is_valid(transaction)


def tests_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD


def test_valid_reward_transaction():
    reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid(reward_transaction)

def test_invalid_reward_transaction_extra_recipient():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output["ekstra_recipient"] = 100

    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid(reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    # Set wrong miner reward
    reward_transaction.output[miner_wallet.address] =500
    
    with pytest.raises(Exception, match="Invalid mining reward"):
        Transaction.is_valid(reward_transaction)
