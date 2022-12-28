import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Transaction():
    """
    Document of an exchange in currency from sender to one or
    more reciepints
    - sender_wallet,  an instance of the wallet class
    -  recipient,  another wallets adress string
    """
    def __init__(self,
        sender_wallet=None,
        recipient=None,
        amount=None,
        id=None,
        output=None,
        input=None
    ):
        # Transaction id,
        # if provided in init otherwise create it (or statement)
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)
    
    # Helper to self.output in __init__
    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data for the transaction.
        """
        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds coin balance")
        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    # Helper to self.input in __init__
    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction
        Sign the transaction and include sender's puplic key and adress
        """

        return {
            "timestamp" : time.time_ns(),
            "amount" : sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        """
        Update transaction with an existing or new recipient.
        """
        # Output is the new balance, so make sure not eceeded
        if amount > self.output[sender_wallet.address]:
            raise Exception("Amount exceeds coin balance")

        # Sending more to same recipient
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        # Or new recipient
        else:
            self.output[recipient] = amount

        # Update sender wallet balance
        self.output[sender_wallet.address] = \
            self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        """
        serialize the transaction
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize a transaction's json representation back
        into  a Transaction instance.
        """
        #return Transaction(
        #id=transaction_json["id"],
        #output=transaction_json["output"],
        #input=transaction_json["input"]
        #)
        # Same as below
        return Transaction(**transaction_json)


    @staticmethod
    def is_valid(transaction):
        """
        Validate transaction and raise exception if invalid.
        """
        # Validate mining reward transaction
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception("Invalid mining reward")
            return 

        # Validate all other transactions
        output_total = sum(transaction.output.values())

        if transaction.input["amount"] != output_total:
            raise Exception("Invalid transaction output values")
        # wallet/address balance shall match total output
        # (output include cahange back to own address)

        if not Wallet.verify(
            transaction.input["public_key"],
            transaction.output,
            transaction.input["signature"]
        ):
            raise Exception("Invalid signature")

    @staticmethod
    def reward_transaction(miner_wallet):
        """
        Generate reward transaction for miner.
        """
        output = {}
        output[miner_wallet.address] = MINING_REWARD
        return Transaction(input=MINING_REWARD_INPUT, output=output)



def main():
    transaction = Transaction(Wallet(), "recipient", 10)
    print(f"\n --transaction.__dict__: {transaction.__dict__}")

    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)

    print(f"\n --restored_transaction.__dict__: {restored_transaction.__dict__}")


if __name__ == "__main__":
    main()