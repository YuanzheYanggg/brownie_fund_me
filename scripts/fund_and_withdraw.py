from brownie import FundMe
from scripts.helpful_scripts import get_account

# we use this file to interact with our contract
# notice that before we run this script, we need to make sure that we already depoly our contract
def fund():
    # always get the latest deployment
    fund_me = FundMe[-1]
    account = get_account()
    price = fund_me.getPrice()
    print("price: ", price)
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"Print out entrance_fee {entrance_fee}")
    print("Funding")
    # the value here will be corresponding to msg.value, which is
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdrawAll({"from": account})


def main():
    fund()
    withdraw()
