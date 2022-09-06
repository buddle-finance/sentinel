from sentinel.services.web3Manager import Web3Manager
from threadManager import ThreadManager
from eth_account.datastructures import SignedTransaction
from sentinel.services.singletonFactory import SingletonFactory


class TransactionManager(ThreadManager):
    """
    This is a singleton class. Use the SingletonFactory to get an instance of this class.
    """

    def __init__(self, singletonFactory: SingletonFactory) -> None:
        self.web3Service: Web3Manager = singletonFactory.getService(Web3Manager)

    def queueTransaction(self, txn: SignedTransaction, chainId: int) -> str:
        # TODO: This is test code. Write code to use a separate thread for transaction processing

        txnHash = self.web3Service.getInstance(chainId).eth.send_raw_transaction(
            txn.rawTransaction
        )
        self.web3Service.getInstance(chainId).eth.wait_for_transaction_receipt(txnHash)

        print(txnHash)

    def processTransaction(self) -> None:
        pass

    def startProcessThread(self) -> None:
        pass
