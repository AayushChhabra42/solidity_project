import time

from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from":account},
    )
    print("Deployed lottery!")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn= lottery.StartLottery({"from":account})
    starting_txn.wait(1)
    print("lottery has started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.Get_Entrance_fee() + 100000000
    enter_txn = lottery.enter({"from":account,"value":value})
    enter_txn.wait(1)
    print("You have entered the lottery")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    #fun the contract with link
    #then end the lottery
    link_txn = fund_with_link(lottery.address)
    link_txn.wait(1)
    end_txn = lottery.EndLottery({"from":account})
    end_txn.wait(1)
    time.sleep(30)
    print(f"{lottery.recentWinner()}, is the recent winner")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()