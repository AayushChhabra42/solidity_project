from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.StartLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.Get_Entrance_fee()})
    lottery.enter({"from": account, "value": lottery.Get_Entrance_fee() })
    fund_with_link(lottery)
    lottery.EndLottery({"from": account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0