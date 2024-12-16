from brownie import accounts, config


def get_account():
    return accounts.add(config["deployer"])
