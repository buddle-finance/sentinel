from threadManager import ThreadManager


class TransactionManager(ThreadManager):
    def __init__(self) -> None:
        pass

    def queueTransaction(self, transaction: Transaction) -> None:
        pass

    def processTransaction(self) -> None:
        pass

    def startProcessThread(self) -> None:
        pass
