from web3 import Web3
import time
import json
import asyncio
from dotenv import load_dotenv
from web3 import __version__

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "./../.env")
load_dotenv(dotenv_path)

private_key = os.environ.get("PRIVATE_KEY")
print(private_key)

w3 = Web3(
    # Web3.WebsocketProvider("wss://rinkeby.arbitrum.io/feed")
    Web3.HTTPProvider("https://rinkeby.arbitrum.io/rpc")
)

w3_l1 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth_rinkeby	"))

# w3 = Web3(EthereumTesterProvider())
print(w3.isConnected())
print(__version__)

sourceAbi = open("abi/BuddleSrc.json", "r")

with open("abi/BuddleSrc.json") as f:
    info_json = json.load(f)
abi = info_json

with open("abi/BuddleDest.json") as f:
    dest_json = json.load(f)
abiDest = dest_json

with open("abi/BuddleBridge.json") as f:
    bridge_json = json.load(f)
abiBridge = bridge_json

# arbi source - 0x9869Fc26826172eB8fB334b39B8D865Be36b01C3
# arbi destination - 0xcb122d5dFD3e2b16b07dd95F78AB745CaC086c00
# arbi Bridge rinkeby - 0xe396721BF9FD7c320c3c528077428847c4940C65

contractAddress = "0x9869Fc26826172eB8fB334b39B8D865Be36b01C3"
contract = w3.eth.contract(address=contractAddress, abi=abi)
accounts = w3.eth.accounts

me = w3.eth.account.privateKeyToAccount(private_key)

w3.eth.default_account = me

destination_contract_address = "0xcb122d5dFD3e2b16b07dd95F78AB745CaC086c00"
contractDestination = w3.eth.contract(address=destination_contract_address, abi=abiDest)


def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event["transactionHash"])
    result = contract.events.TransferStarted().processReceipt(receipt)
    # print("Result[0]['args']"result[0]['args'], end="\n\n")
    # print("Result:", result, end="\n\n")
    transferData = result[0]["args"]["transferData"]
    transferID = result[0]["args"]["transferID"]
    print("transferData:", transferData, end="\n\n")
    print(type(transferData[2]))

    depositTxn = contractDestination.functions.deposit(
        transferData, transferID, 421611
    ).buildTransaction(
        {
            "from": me.address,
            "value": transferData[2],
            "nonce": w3.eth.getTransactionCount(me.address),
        }
    )

    signed = w3.eth.account.signTransaction(depositTxn, private_key)
    test = w3.eth.sendRawTransaction(signed.rawTransaction)
    w3.eth.wait_for_transaction_receipt(test)

    print(test)


def log_loop(event_filter, poll_interval):
    while True:
        print("Waiting for events...")
        for event in event_filter.get_all_entries():  # get_new_entries():
            print("Handling event...")
            handle_event(event)
            break

        time.sleep(poll_interval)


new_filter = contract.events.TransferStarted.createFilter(fromBlock="0x0")
print(log_loop(new_filter, 10))

# transferData
# address tokenAddress;
# address destination;
# uint256 amount;
# uint256 fee;
# uint256 startTime;
# uint256 feeRampup;
# uint256 chain;

# TrabnsferID
# SourceChainID

# block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
# log_loop(block_filter, 2)
