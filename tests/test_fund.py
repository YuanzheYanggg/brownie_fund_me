from scripts.fund_and_withdraw import fund
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy_fund_me import deploy_fund_me
import pytest
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdrawAll({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # if we run our script not in local blockchains, we will automatically skip it
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    fund_me = deploy_fund_me()
    account = get_account()
    bad_actor = accounts.add()

    # since a bad actor cannot withdraw money
    # we expect some revert error happening here, so we use pytest raise exceptions to catch the exception
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrawAll({"from": bad_actor})
