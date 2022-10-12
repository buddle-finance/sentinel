from sentinel.services.buddleNetwork import BuddleNetwork
from sentinel.services.configManager import ConfigManager
from sentinel.services.singletonFactory import SingletonFactory
from web3 import Web3


class Web3Manager:
    def __init__(self, singletonFactory: SingletonFactory) -> None:
        self.networks: dict[int, BuddleNetwork] = {}
        self.web3Instances: dict[int, Web3] = {}
        self.singletonFactory: SingletonFactory = singletonFactory
        self.configService: ConfigManager = singletonFactory.getService(ConfigManager)

    def getNetwork(self, chainId: int) -> BuddleNetwork:
        buddleNetwork = self.networks.get(chainId)
        if not buddleNetwork:
            buddleNetwork = BuddleNetwork(self.singletonFactory, chainId)
            self.networks[chainId] = buddleNetwork

        return buddleNetwork

    def getInstance(self, chainId: int) -> Web3:
        web3Instance = self.web3Instances.get(chainId)
        if not web3Instance:
            web3Instance = Web3(
                Web3.HTTPProvider(self.configService.config.getNetwork(chainId).rpc)
            )
            self.web3Instances[chainId] = web3Instance
        return web3Instance
