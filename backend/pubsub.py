import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-78070285-db89-4898-a7e7-d4731855cafa'
pnconfig.publish_key = 'pub-c-c12b168a-f8e1-4458-9413-522ec2713d12'
## Below for new version of pubsub (ran into issues so I downgraded)
#pnconfig.user_id = "g"
#pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR

CHANNELS = {
"TEST": "TEST",
"BLOCK": "BLOCK",
"TRANSACTION": "TRANSACTION"
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f"\n-- Channel: {message_object.channel}, Message: {message_object.message}")

        if message_object.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                # Clear transaction pool after new block (if transactions
                # already in a new block)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print("\n -- Successfully replaced local chain")
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")
        
        elif message_object.channel == CHANNELS["TRANSACTION"]:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print("\n -- Set the new transaction in transaction pool")

class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provide communication between nodes of the blockchain network.
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        # NOTE Unsubscribe before publish so that we do not receive
        # the block over pubsub. Block added locally already.
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        # Subscribe again
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcast_block(self, block):
        """
        Broadcast blockchain object to all nodes.
        """
        self.publish(CHANNELS["BLOCK"], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast transaction to all nodes.
        """
        self.publish(CHANNELS["TRANSACTION"], transaction.to_json())


# Experimental code
def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS["TEST"], {"foo": "bar"})

if __name__ == "__main__":
    main()