from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks, data sets of transactions.
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f"Blockchain: {self.chain}"

    def replace_chain(self, chain):
        """
        Replace local chain with incoming chain if following applies:
          - Incoming chain is longer then local chain.
          - Incoming chain is valid.
        """
        if len(chain) <= len(self.chain):
            raise Exception("Cannot replace. The incoming chain must be longer.")
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f"Cannot replace. Incoming chain is invalid: {e}")
        # if no exception, replace chain
        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """
        # return list(map(lambda block: block.to_json(), self.chain))

        serialize_chain = []
        for block in self.chain:
            serialize_chain.append(block.to_json())

        return serialize_chain

    def from_json(chain_json):
        """
        De-serialize list of serialized blocks to a block instance.
        The result will contain a chain list of Block instances
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )
        # for block_json in chain_json ..
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate incoming chain
        Enforce the following rules of the blockchain:
        - chain must start with genesis block
        - blocks must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception("Gesesis block must be valid")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce rules of a chain composed of blocks of transactions.
          - Each transaction can only appear once in the chain.
          - Only one mining reward per block.
          - Each transaction must be valid.
        """
        # Sets cannot have two items with the same value.
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_rewards = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                # Check for duplicated transactions
                if transaction.id in transaction_ids:
                    raise Exception(f"Transaction {transaction.id} is not unique")
                # Add transaction to set (it will then be checked for duplicate)
                transaction_ids.add(transaction.id)


                # Check for more than one mining rewards
                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_rewards == True:
                        raise Exception(f"Duplicate mining rewards. \Check block with hash: {block.hash}")
                    has_mining_rewards = True

                # Check wallet balance so transaction input amount match blockchain balance
                else:
                    # Run if transaction is Not a mining transaction
                    # Make historic_blockchain a Blockchain instance,
                    # then copy in slice of chain
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input["address"]
                        )

                    if historic_balance != transaction.input["amount"]:
                        raise Exception(
                            f"Transaction {transaction.id} has "\
                            "an invalid input amount"
                        )

                # Check that the transaction is valid
                Transaction.is_valid(transaction)



def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")

    print(blockchain)
    print(f"blockchain.py__name__: {__name__}")

if __name__ == "__main__":
    main()