from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # current price is $1514.84 => 50/1514 ~ 0.033
    assert lottery.getEntranceFee() > Web3.toWei(0.031, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.040, "ether")
