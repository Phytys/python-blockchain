#  1. Overview
This repo is based on this awesome course:
https://www.udemy.com/course/python-js-react-blockchain/

A python blockchain:
- Flask api as backend
- Broadcasts over PubSub channel (PubNub Python SDK)
- Mining and PoW
- Wallet and transaction pool
- Validation of blockchain, blocks and transactions


Backend built in Python.
Frontend built in React JS

# 2. Backend App & API

**Run flask application and API**
```
python3 -m  backend.app
```
 **Run a peer instance**
```
export PEER=True && python3 -m  backend.app
```
 **Seed the backend with data (added blocks)**
```
export SEED_DATA=True && python3 -m  backend.app
```
**Run tests**
```
python3 -m pytest backend/tests
```

## 2.1 API endpoints

#### Get - Current blockchain
- http://localhost:5000/blockchain

#### Get - Slice of current blockchain
- http://localhost:5000/blockchain/range?
- -> Example ?start=1&end=5

#### Get - Length of current blockchain
- http://localhost:5000/blockchain/length

#### Get - Known Addresses
- http://localhost:5000/known-addresses

#### Get - Transactions pool
- http://localhost:5000/transactions

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

--------------------------------------------------
# 3. Frontend

**Run frontend**
```
npm run start
```

-------------------------------------------
# 5. NOTES TO SELF

- Improvements to consider:
    - Sync without root node (!)
    - Sync blockchain fallen behind (!!)
    - Additional API endpoints e.g. difficulty
    - etc.
    
 