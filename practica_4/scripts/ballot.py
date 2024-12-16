from brownie import Ballot, network
from scripts.utils import get_account


def deploy():
    account = get_account()
    print(f"Deploying to {network.show_active()}...")
    ballot = Ballot.deploy(
        ["Alice", "Bob", "Charlie"],
        {"from": account},
    )
    print(f"Contract deployed at {ballot.address}")


def verify():
    ballot = Ballot[-1]
    breakpoint()
    Ballot.publish_source(ballot)
