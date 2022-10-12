import json

from eth_account.account import LocalAccount
from eth_account.datastructures import SignedTransaction
from sentinel.services.configManager import ConfigManager
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.services.transactionManager import TransactionManager
from sentinel.types.configTypes import Network
from sentinel.types.enums import BuddleContract
from sentinel.types.transferData import TransferData
from web3 import Web3
from web3.contract import Contract
from web3.types import BlockData


class BuddleNetwork:
    def __init__(self, singletonFactory: SingletonFactory, chainID: int) -> None:
        self.chainId = chainID
        self.connected = False
        self.w3 = None
        self.contracts: dict[str, Contract] = {}
        self._account: LocalAccount = None
        self.configService: ConfigManager = singletonFactory.getService(ConfigManager)
        self.transactionService: TransactionManager = singletonFactory.getService(
            TransactionManager
        )
        self.network: Network = self.configService.config.getNetwork(self.chainId)

    def connect(self) -> bool:
        if not self.w3.isConnected():
            self.rpcUrl = self.network.rpc
            self.w3 = Web3(Web3.HTTPProvider(self.rpcUrl))
            self.connected = True

        return self.connected

    def getBlock(self, blockNumber) -> BlockData:
        return self.w3.eth.get_block(blockNumber, full_transactions=True)

    def readAbi(self, buddleContract: BuddleContract) -> dict:
        with open(f"./../abi/{buddleContract.value}.json") as f:
            info_json = json.load(f)

        return info_json

    def getContract(self, buddleContract: BuddleContract) -> Contract:
        contract = self.contracts.get(buddleContract.name)
        if not contract:
            contract = self.w3.eth.contract(
                address=self.network.getContractAddress(buddleContract),
                abi=self.readAbi(buddleContract),
            )
            self.contracts[buddleContract.name] = contract

        return contract

    @property
    def account(self) -> LocalAccount:
        if not self._account:
            privateKey = self.network.privateKey
            self._account = self.w3.eth.account.privateKeyToAccount(privateKey)

        return self._account

    # TODO: Relocate
    def depositOnDestination(
        self, transferData: TransferData, transferId: int, chainId: int
    ) -> SignedTransaction:
        contract = self.getContract(BuddleContract.DESTINATION)
        tx = contract.functions.deposit(
            transferData.rawData, transferId, chainId
        ).buildTransaction(
            {
                "from": self.account.address,
                "value": transferData[2],
                "nonce": self.w3.eth.get_transaction_count(
                    self.configService.getPrivateKey(self.chainId)
                ),
            }
        )
        signedTx = self.w3.eth.account.sign_transaction(
            tx, private_key=self.configService.getPrivateKey(self.chainId)
        )

        return signedTx
