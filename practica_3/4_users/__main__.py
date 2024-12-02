import os
import dotenv
import logging

from utils import Web3Proxy
from .contracts import UserRegistry, MessageBoard

LOGGER = logging.getLogger("user-registry")
LOGGER.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to LOGGER
LOGGER.addHandler(ch)

dotenv.load_dotenv()

# Environment setup
NODE = os.getenv("NODE", "")
ADDRESS = os.getenv("ADDRESS", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

if not all([NODE, ADDRESS, PRIVATE_KEY]):
    raise ValueError(
        "`NODE`, `ADDRESS`, and `PRIVATE_KEY` must be set in the environment"
    )


USER_REGISTRY_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "_address",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "_username",
                "type": "string",
            },
        ],
        "name": "UserRegistered",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "address", "name": "_address", "type": "address"}],
        "name": "isUser",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "username", "type": "string"}],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "users",
        "outputs": [
            {"internalType": "address", "name": "_address", "type": "address"},
            {"internalType": "string", "name": "_username", "type": "string"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

MESSAGE_BOARD_ABI = [
    {
        "inputs": [{"internalType": "string", "name": "message", "type": "string"}],
        "name": "postMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_userRegistry", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "inputs": [],
        "name": "getMessagesLength",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "messages",
        "outputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "string", "name": "content", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "registry",
        "outputs": [
            {"internalType": "contract UserRegistry", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

if __name__ == "__main__":
    proxy = Web3Proxy(NODE, PRIVATE_KEY, ADDRESS)

    user_registry = UserRegistry(
        proxy, "0x5dC38fa35AC605519EFd294721a1554A52EbCc3c", USER_REGISTRY_ABI
    )
    LOGGER.debug("User registry created")

    if not user_registry.is_user(ADDRESS):
        user_registry.register_user("Alice")
    else:
        LOGGER.debug("User already registered, skipping...")

    message_board = MessageBoard(
        proxy, "0x7c803e7d4FB71C5be2FB18B0bA2a66D82079e89A", MESSAGE_BOARD_ABI
    )
    message_board.post_message("Hello, Ethereum!")
    messages = message_board.fetch_messages()
    print(f"Messages: {messages}")
