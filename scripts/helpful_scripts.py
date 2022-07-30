from brownie import (
    Contract,
    network,
    config,
    accounts,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3


# ganache-fundme was added as a new blockchain under Ethereum network
FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_DEVELOPMENT = ["development", "ganache-fundme"]

DECIMALS = 18
STARTING_PRICE = 2000 * 10**18  # in Wei


def get_account():
    # 3 ways to get accounts
    # 1) accounts[0] 2) accounts.add("env") 3) accounts.load("id") user created accounts
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENT
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined,
    otherwise it will deploy mock version of that contract and return that mock contracts.

    Args: contract_name: string

    Returns: brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
    e.g. MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        if len(contract_type) <= 0:
            # OR MockV3Aggregator.length<=0
            deploy_mocks()

        # get the latest contract
        contract = contract_type[-1]  # same as MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # we have the address and abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mock Deployed!")
