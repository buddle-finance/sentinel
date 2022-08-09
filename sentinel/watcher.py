from web3 import Web3
import time
import json

w3 = Web3(
    Web3.HTTPProvider(
        "https://arb-rinkeby.g.alchemy.com/v2/YvBKFI1Om2hFbF878J6mrwbxZYtY1VF6"
    )
)
# w3 = Web3(EthereumTesterProvider())
print(w3.isConnected())

sourceAbi = open("abi/BuddleSrc.json", "r")

with open("abi/BuddleSrc.json") as f:
    info_json = json.load(f)
abi = info_json

# arbi source - 0x9869Fc26826172eB8fB334b39B8D865Be36b01C3
# arbi destination - 0xcb122d5dFD3e2b16b07dd95F78AB745CaC086c00
# arbi Bridge rinkeby - 0xe396721BF9FD7c320c3c528077428847c4940C65

contractAddress = "0x9869Fc26826172eB8fB334b39B8D865Be36b01C3"
contract = w3.eth.contract(address=contractAddress, abi=abi)
accounts = w3.eth.accounts

print(contract.functions.CHAIN().call())


def handle_event(event):
    print("Event:", event["transactionHash"], end="\n\n")
    receipt = w3.eth.waitForTransactionReceipt(event["transactionHash"])
    print("Receipt:", receipt, end="\n\n")
    result = contract.events.TransferStarted().processReceipt(receipt)
    # print("Result[0]['args']"result[0]['args'], end="\n\n")
    print("Result:", result, end="\n\n")


def log_loop(event_filter, poll_interval):
    while True:
        print("Waiting for events...")
        for event in event_filter.get_new_entries():
            print("Handling event...")
            handle_event(event)

        time.sleep(poll_interval)


new_filter = contract.events.TransferStarted.createFilter(
    fromBlock="latest"
)  # 12110375
print(log_loop(new_filter, 10))

# block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
# log_loop(block_filter, 2)
