#  1. Overview
This repo is based on this awesome course:
https://www.udemy.com/course/python-js-react-blockchain/

A python blockchain:
- Flask api as backend
- Broadcasts over PubSub channel (PubNub Python SDK)
- Mining and PoW
- Wallet and transaction pool
- Validation of blockchain, blocks and transactions

# 2. Backend App & API

**Run flask application and API**
```
python3 -m  backend.app
```
 **Run a peer instance**
```
export PEER=True && python3 -m  backend.app
```
**Run tests**
```
python3 -m pytest backend/tests
```

## 2.1 API endpoints

#### Get - Current blockchain
- http://localhost:5000/blockchain

#### Post - Transaction
- http://localhost:5000/wallet/transact

```
{
    "recipient": "the-address",
    "amount": 20
}
```
#### Get - Mine new block
- http://localhost:5000/blockchain/mine

#### Get - Wallet balance
- http://localhost:5000/wallet/info

------------------------------------------------------
# 3. Frontend

To be added


-------------------------------------------
# 5. NOTES TO SELF
- Follow up on PubNub connection problems. "Exception in subscribe loop"
    
 