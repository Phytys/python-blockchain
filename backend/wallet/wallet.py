import json
import uuid
# UUID (Universally unique identifier). A version 4 UUID is randomly generated

from backend.config import STRATING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miners balance
    Allows miner to authorize transactions.
    """
    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
        # so that public key is initiated serialized
        # (overwrites self.public_key)

        # So that balance is always available up tp date
        # Requires blockchain instance to be passed to Wallet class
    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)


    def sign(self, data):
        """
        Generate a (decoded) signature based on the data using the
        local private key.
        Signature associated with wallet key pair.
        Can only be produces by key owner.
        Others should be able to verify that it is a valid signature,
        without knowing the private key.
        """
        data = json.dumps(data).encode("utf-8")

        return decode_dss_signature(
            self.private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
            )
        )
        # ECDSA - Eliptic Cryptogr. Dig. Sign. Algorithm

    def serialize_public_key(self):
        """
        Reset public key to serialized version.
        And so it can be jsonified.
        """
        self.public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
        decoded_public_key = self.public_key_bytes.decode("utf-8")
        # Assign decoded public key to self
        self.public_key = decoded_public_key

    
    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode("utf-8"),
            default_backend
        )
        # print(f"\n Signature--: {signature}")
        # function "sign" generate a decoded signature as a tuple (two long strings)
        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode("utf-8"),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        
        except InvalidSignature:
            return False


    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Claculate the balance for a wallet address on blockchain.
        The Balance is found by adding output values that belongs to
        the address since the most recent transaction by that address.
        """
        balance = STRATING_BALANCE

        # If blockchain instance not passed to wallet class
        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction["input"]["address"] == address:
                    # When address do a transaction (when address sends coins),
                    # the balance resets and is shown in output
                    balance = transaction["output"][address]
                    
                elif address in transaction["output"]:
                    # If not as transaction input address but seen in output,
                    # then add to balance (when address receive coins)
                    balance += transaction["output"][address]

        return balance



# Experimental code, if main
def main():
    wallet = Wallet()
    print(f"wallet.__dict__: {wallet.__dict__}")

    data = {"foo": "bar"}
    signature = wallet.sign(data)
    print(f"signature: {signature}")

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f"should_be_valid: {should_be_valid}")

    # Using a random wallet public key so should return false
    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f"should_be_invalid: {should_be_invalid}")

if __name__ == "__main__":
    main()