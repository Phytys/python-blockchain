import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "hash" : "genesis_hash",
    "data": [],
    "difficulty": 3,
    "nonce": "genesis_nonce"
}

class Block():
    """
    Block: a unit of storage.
    Store transactions in a blockchain, supporting a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data= data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block ('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes.
        """
        return self.__dict__


    # Static methods below (could be functions outside class)
    @staticmethod
    def mine_block(last_block, data):
        """
        Mine block based on last block and data. Need to find a hash
        that match the leading 0's proof of work requirements.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
        # In while loop, look at binary representation of the hash
        # so difficulty is num zeros in binary string
        while hex_to_binary(hash)[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
            
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Generate genesis block.
        """
        #return Block(
        #    GENESIS_DATA["timestamp"],
        #    GENESIS_DATA["last_hash"],
        #    GENESIS_DATA["hash"],
        #    GENESIS_DATA["data"],
        #    )
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        """
        De-serialize json representation
        back in to a block instance.
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calc and adjust difficulty based on MINE_RATE
        Increase difficulty if block is mine to quickly
        Decrease difficulty if mining takes too long
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty -1) > 0:
            return last_block.difficulty -1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing the following rules:
          - block must have the proper last_hash reference
          - block must meet the proof of work requirement
          - difficulty must only adjust by 1
          - block hash must be a valid combination of block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception("The block last_hash is not correct")

        if hex_to_binary(block.hash)[0:block.difficulty] != "0" * block.difficulty:
            raise Exception("The proof of work requirement not met")

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("Block difficullty must only adjust by 1")

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )
        #print("reconstr_hash",reconstructed_hash)
        if block.hash != reconstructed_hash:
            raise Exception("Block hash must be correct")


def main():
    # NOTE experimental code below
    # genesis_block = Block.genesis()
    # print(genesis_block)
    # block = Block.mine_block(genesis_block, "foo")
    # print(block)
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, "foo")
    print("bad_block.hash before: ",bad_block.hash)
    bad_block.hash = "modified_hash"
    print("bad_block.hash after: ",bad_block.hash)
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f"is_valid_block: {e}")

if __name__ == "__main__":
    main()