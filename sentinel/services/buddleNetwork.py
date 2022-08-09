from web3 import Web3
from web3.types import BlockData
from web3.contract import Contract


class BuddleNetwork:
    def __init__(self, rpcUrl: str) -> None:
        self.rpcUrl = rpcUrl
        self.connected = False
        self.w3 = None

    def connect(self) -> bool:
        if not self.w3.isConnected():
            self.w3 = Web3(Web3.HTTPProvider(self.rpcUrl))
            self.connected = True

        return self.connected

    def getBlock(self, blockNumber) -> BlockData:
        return self.w3.eth.get_block(blockNumber, full_transactions=True)

    def getContract(self, contractAddress, abi) -> Contract:
        return self.w3.eth.contract(address=contractAddress, abi=abi)
