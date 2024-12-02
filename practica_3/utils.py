from logging import Logger
from web3 import Web3
from eth_typing import Address
from web3.types import TxParams, TxReceipt

LOGGER = Logger("web3-utils")


class Web3Proxy:
    """Helper class to interact with the Ethereum blockchain."""

    def __init__(self, node: str, private_key: str, address: Address):
        self.node = node
        self.private_key = private_key
        self.address = address

        self.w3 = Web3(Web3.HTTPProvider(self.node))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to the Ethereum node.")

    def get_contract(self, address: Address, abi: list):
        """
        Get a contract instance.
        :param address: Address of the contract
        :param abi: ABI of the contract
        :return: Contract instance
        """
        return self.w3.eth.contract(address=address, abi=abi)

    def send_transaction(self, func, value=0) -> TxReceipt:
        """
        Helper function to send a transaction.
        :param func: The contract function to invoke
        :param value: Amount of Ether to send (in wei)
        :return: Transaction receipt
        """
        tx: TxParams = func.build_transaction(
            {
                "from": self.address,
                "value": value,
                "gasPrice": self.w3.eth.gas_price,
                "nonce": self.w3.eth.get_transaction_count(self.address),
            }
        )
        tx["gas"] = self.w3.eth.estimate_gas(tx)

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        LOGGER.info(f"Transaction sent! Hash: {tx_hash.hex()}")
        receipt: TxReceipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        LOGGER.info(f"Transaction confirmed! Receipt: {receipt}")
        return receipt
