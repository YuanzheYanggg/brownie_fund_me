from unittest import mock
from brownie import FundMe, network, config
from scripts.helpful_scripts import (
    get_account,
    setup_mock,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"Active network is {network.show_active()}")
        print("Deploying Mocks")
        # we can always check how many contract deployment we have made on our end in build section
        # since this mock is just a functional contract to us
        # we only want to deploy it once
        mock_aggregator = setup_mock()
        print("Deploying done")
        price_feed_address = mock_aggregator.address

    # pass the pricefeed address to the FundMe contract
    fund_me = FundMe.deploy(
        # if we a on a persistant network, we can use this address
        # otherwise , deploy mock
        price_feed_address,
        {"from": account},
        # it determined whether or not we want to publish our deployment to public net
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"rinkeby eth/usd price {fund_me.getPrice()}")
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
