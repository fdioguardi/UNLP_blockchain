import os
import dotenv

from utils import Web3Proxy


dotenv.load_dotenv()

# Contract ABI
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
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
        ],
        "name": "Deposit",
        "type": "event",
    },
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
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
        ],
        "name": "Withdrawal",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address payable", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_amount", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

# Environment variables
NODE = os.getenv("NODE", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
ADDRESS = os.getenv("ADDRESS", "")

if not all([NODE, PRIVATE_KEY, ADDRESS]):
    exit("Missing environment variables")

# Initialize Web3Proxy
web3_utils = Web3Proxy(NODE, PRIVATE_KEY, ADDRESS)
contract = web3_utils.get_contract("0x292640f16412F0beF5A6efcC9717C95D656CA46D", ABI)


def get_balance():
    balance = contract.functions.getBalance().call()
    print(f"Contract Balance: {web3_utils.w3.from_wei(balance, 'ether')} ETH")


def deposit(amount_eth):
    value = web3_utils.w3.to_wei(amount_eth, "ether")
    print(f"Depositing {amount_eth} ETH...")
    web3_utils.send_transaction(contract.functions.deposit(), value=value)


def withdraw(amount_eth):
    value = web3_utils.w3.to_wei(amount_eth, "ether")
    print(f"Withdrawing {amount_eth} ETH...")
    web3_utils.send_transaction(contract.functions.withdraw(value))


if __name__ == "__main__":
    get_balance()
    deposit(0.1)
    get_balance()

    print("Withdrawing 0.05 ETH...")
    withdraw(0.05)

    print("Reading final balance...")
    get_balance()
