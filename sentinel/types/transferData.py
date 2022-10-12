class TransferData:
    def __init__(self, rawData: tuple) -> None:
        self._rawData = rawData
        self._tokenAddress: str = rawData[0]
        self._destination: str = rawData[1]
        self._amount: int = rawData[2]
        self._fee: int = rawData[3]
        self._startTime: int = rawData[4]
        self._feeRampup: int = rawData[5]
        self._chain: int = rawData[6]

    @property
    def tokenAddress(self):
        return self._tokenAddress

    @property
    def destinationAddress(self):
        return self._destination

    @property
    def amount(self):
        return self._amount

    @property
    def fee(self):
        return self._fee

    @property
    def startTime(self):
        return self._startTime

    @property
    def feeRampup(self):
        return self._feeRampup

    @property
    def chain(self):
        return self._chain

    @property
    def rawData(self):
        return self._rawData

    def __str__(self) -> str:
        return str(self._rawData)

    def __repr__(self) -> str:
        return self.__str__()
