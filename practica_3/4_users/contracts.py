import logging

from utils import Web3Proxy

LOGGER = logging.getLogger("user-registry")


class MessageBoard:
    def __init__(self, proxy: Web3Proxy, address, abi):
        self.contract = proxy.get_contract(address, abi)
        self.proxy: Web3Proxy = proxy

    def post_message(self, content: str):
        LOGGER.info(f"Posting message: {content}")
        self.proxy.send_transaction(self.contract.functions.postMessage(content))
        LOGGER.info("Message posted!")

    def fetch_messages(self) -> list:
        messages: list = []
        message_count: int = self.contract.functions.getMessagesLength().call()
        for i in range(message_count):
            message = self.contract.functions.messages(i).call()
            messages.append(
                {
                    "sender": message[0],
                    "content": message[1],
                    "timestamp": message[2],
                }
            )
        return messages


class UserRegistry:
    def __init__(self, proxy: Web3Proxy, address, abi):
        self.contract = proxy.get_contract(address, abi)
        self.proxy: Web3Proxy = proxy

    def register_user(self, username: str):
        LOGGER.info(f"Registering user: {username}")
        self.proxy.send_transaction(self.contract.functions.register(username))
        LOGGER.info("User registered!")

    def is_user(self, address):
        LOGGER.info(f"Checking if user is registered: {address}")
        return self.contract.functions.isUser(address).call()
