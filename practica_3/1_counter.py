import os

import asyncio
import dotenv
from eth_typing import Address
from web3 import Web3, AsyncWeb3, WebSocketProvider

from .utils import Web3Proxy

dotenv.load_dotenv()

# Environment variables
NODE: str = os.getenv("NODE", "")
WS: str = os.getenv("WS", "")
PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")
ADDRESS: Address = os.getenv("ADDRESS", "")

if not all([NODE, WS, PRIVATE_KEY, ADDRESS]):
    exit("Missing environment variables")

# Web3 setup
w3 = Web3(Web3.HTTPProvider(NODE))

if not w3.is_connected():
    exit("Unable to connect to the network")

ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "by",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "operation",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "newValue",
                "type": "uint8",
            },
        ],
        "name": "CounterModified",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "address", "name": "_address", "type": "address"}],
        "name": "addToWhitelist",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decrement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "increment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_address", "type": "address"}],
        "name": "removeFromWhitelist",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "whitelist",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]


proxy: Web3Proxy = Web3Proxy(NODE, PRIVATE_KEY, ADDRESS)
contract = proxy.get_contract(
    address="0x5FbDB2315678afecb367f032d93F642f64180aa3", abi=ABI
)


async def suscribe_to_counter_event():
    """Listen to contract events asynchronously."""

    async with AsyncWeb3(WebSocketProvider(WS)) as async_w3:
        filter_params = {
            "address": contract.address,
            "topics": [w3.keccak(text="CounterModified(address,string,uint8)")],
        }
        subscription_id = await async_w3.eth.subscribe("logs", filter_params)
        print(
            f"Subscribing to counter events for contract {contract.address} at {subscription_id}"
        )

        async for payload in async_w3.socket.process_subscriptions():
            print()
            print(payload)
            print()


async def call_increment():
    """Call the increment function in a background thread."""
    await asyncio.to_thread(proxy.send_transaction, contract.functions.increment)


async def call_decrement():
    """Call the decrement function in a background thread."""
    await asyncio.to_thread(proxy.send_transaction, contract.functions.decrement)


async def main():
    listener_task: asyncio.Task = asyncio.create_task(suscribe_to_counter_event())
    try:
        await call_increment()
        await call_decrement()
        await listener_task
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        listener_task.cancel()
        await listener_task


if __name__ == "__main__":
    asyncio.run(main())
