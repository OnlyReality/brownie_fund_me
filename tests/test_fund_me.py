from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions, FundMe
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()

    entrance_fee = fund_me.getEntranceFee() + 100 # just incase LOL
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing.")

    account = get_account()
    deploy_fund_me()
    fund_me = FundMe[-1]
    bad_actor = accounts.add()

    print(f"Fund Me Contract: {fund_me}")
    print(f"Bad Actor: {bad_actor}")

    with pytest.raises(AttributeError):

        fund_me.withdraw({"from": bad_actor})
