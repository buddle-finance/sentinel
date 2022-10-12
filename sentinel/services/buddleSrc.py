from buddleNetwork import BuddleNetwork
from web3.utils.filters import LogFilter


class BuddleSrc(BuddleNetwork):
    def __init__(self, rpcUrl) -> None:
        super().__init__(rpcUrl)
        self.eventFilters: dict[str, LogFilter] = {}

    def readNewEvents(self, eventName: str):
        pass

    def readNewBlocks(self):
        pass
