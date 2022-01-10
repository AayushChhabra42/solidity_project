from brownie import (accounts,network,config,MockV3Aggregator,VRFCoordinatorMock,LinkToken,Contract,interface,)
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
Contract_to_mock = {"eth_usd_price_feed":MockV3Aggregator,"vrf_coordinator":VRFCoordinatorMock,"link_token":LinkToken}
def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
            network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
            or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    """
    this function will grab contract address from brownie config if defined otherwise it will deploy mocks
        args:
            contract_name(string)

        returns:
            brownie.network.contract.ProjectContract:The most
    """
    contract_type= Contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

Decimals = 8
Initial_Value = 200000000000

def deploy_mocks(decimals=Decimals,initial_value=Initial_Value):
    account=get_account()
    mock_price_feed=MockV3Aggregator.deploy(decimals,initial_value,{"from":account})
    link_token= LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print("deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address,amount,{"from":account})
    # same thing using interfaces
    #link_token_contract = interface.LinkTokenInterface(link_token.address)
    #tx = link_token_contract.transfer(contract_address,amount,{"from:account"})
    tx.wait(1)
    print("fund contract!")
    return tx
