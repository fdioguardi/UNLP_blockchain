import os
import dotenv
from utils import Web3Proxy

dotenv.load_dotenv()

NODE = os.getenv("NODE", "")
WS = os.getenv("WS", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
ADDRESS = os.getenv("ADDRESS", "")

if not all([NODE, WS, PRIVATE_KEY, ADDRESS]):
    raise ValueError(
        "`NODE`, `WS`, `PRIVATE_KEY`, and `ADDRESS` must be set in .env file"
    )

ABI = [
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
                "name": "candidate",
                "type": "string",
            },
        ],
        "name": "Voted",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "closeBallot",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "candidateIndex", "type": "uint256"}
        ],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string[]", "name": "candidateNames", "type": "string[]"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "candidates",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "uint8", "name": "voteCount", "type": "uint8"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getCandidateCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getWinner",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "hasVoted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "isOpen",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

proxy = Web3Proxy(NODE, PRIVATE_KEY, ADDRESS)
contract = proxy.get_contract(
    address="0xc82e4c9E25f6fc5DF761ff0046b70566542abF4d", abi=ABI
)


def list_candidates():
    """
    Lists all candidates and their vote counts.
    """
    candidate_count = contract.functions.getCandidateCount().call()
    print("Candidates:")
    for i in range(candidate_count):
        candidate = contract.functions.candidates(i).call()
        print(f"{i}: {candidate[0]} - Votes: {candidate[1]}")


def vote(candidate_index):
    """
    Votes for a candidate by index.
    """
    print(f"Voting for candidate at index {candidate_index}...")
    proxy.send_transaction(contract.functions.vote(candidate_index))


def close_ballot():
    """
    Closes the ballot.
    """
    print("Closing the ballot...")
    proxy.send_transaction(contract.functions.closeBallot())


def get_winner():
    """
    Gets the winner of the ballot.
    """
    winner = contract.functions.getWinner().call()
    print(f"The winner is: {winner}")


if __name__ == "__main__":
    list_candidates()
    vote(0)
    list_candidates()
    close_ballot()
    get_winner()
