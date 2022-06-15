from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8  # meaning the last 8 digits of our large numbers are decimal digits
STARTING_PRICE = 200000000000  # Eleven 0s this is meaning we have 2000 ether
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
    # return accounts.add(os.getenv("PRIVATE_KEY"))


def setup_mock():
    if len(MockV3Aggregator) <= 0:
        # the Web3.toWei converts some number of ether to wei which means it will multiply by 1e18
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
    else:
        mock_aggregator = MockV3Aggregator[-1]
    return mock_aggregator
