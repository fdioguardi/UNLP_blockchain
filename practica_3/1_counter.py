import os

import asyncio
import dotenv
from eth_abi.abi import decode
from web3 import Web3, AsyncWeb3, WebSocketProvider, exceptions
from web3.types import TxReceipt

dotenv.load_dotenv()

# Environment variables
NODE: str = os.getenv("NODE")
WS: str = os.getenv("WS")
PRIVATE_KEY: str = os.getenv("PRIVATE_KEY")
ADDRESS: str = os.getenv("ADDRESS")

# Web3 setup
w3 = Web3(Web3.HTTPProvider(NODE))

if not w3.is_connected():
    exit("Unable to connect to the network")

ABI = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "by",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "operation",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "newValue",
				"type": "uint8"
			}
		],
		"name": "CounterModified",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "addToWhitelist",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decrement",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "increment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			}
		],
		"name": "removeFromWhitelist",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "whitelist",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = w3.eth.contract(address="0x03Ca1aF34709B73F07A3233E08b7Dbdae5d8AFB0", abi=ABI)


def send_transaction(func):
    """Send a transaction to the blockchain."""
    tx: dict = func.build_transaction({
        'chainId': 11155111,
        'from': ADDRESS,
        'value': 0,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(ADDRESS)
    })
    tx['gas'] = w3.eth.estimate_gas(tx)

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"Transaction sent! Hash: {tx_hash.hex()}")
    try:
        receipt: TxReceipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction confirmed! Receipt: {receipt}")
    except exceptions.TimeExhausted: 
        print("Transaction not confirmed in time")



async def suscribe_to_counter_event():
    """Listen to contract events asynchronously."""

    async with AsyncWeb3(WebSocketProvider(WS)) as async_w3:
        filter_params = {
            'address': contract.address,
            'topics': [w3.keccak(text="CounterModified(address,string,uint8)")]
        }
        subscription_id = await async_w3.eth.subscribe('logs', filter_params)
        print(f"Subscribing to counter events for contract {contract.address} at {subscription_id}")

        async for payload in async_w3.socket.process_subscriptions():
            print()
            print(payload)
            print()


async def call_increment():
    """Call the increment function in a background thread."""
    await asyncio.to_thread(send_transaction, contract.functions.increment)


async def call_decrement():
    """Call the decrement function in a background thread."""
    await asyncio.to_thread(send_transaction, contract.functions.decrement)


async def main():
    """Run the event listener and function calls concurrently."""
    # Run the event listener in the background
    listener_task = asyncio.create_task(suscribe_to_counter_event())

    # Simulate calls to increment and decrement
    await call_increment()
    await call_decrement()

    # Allow the listener to continue running
    await listener_task


if __name__ == "__main__":
    asyncio.run(main())