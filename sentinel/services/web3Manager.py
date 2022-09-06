from web3 import Web3
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.services.configManager import ConfigManager


class Web3Manager:
    def __init__(self, singletonFactory: SingletonFactory) -> None:
        self.web3Instances: dict[int, Web3] = {}
        self.configService: ConfigManager = singletonFactory.getService(ConfigManager)

    def getInstance(self, chainId: int) -> Web3:
        web3Instance = self.web3Instances.get(chainId)
        if not web3Instance:
            web3Instance = Web3(
                Web3.HTTPProvider(self.configService.getRpcUrl(chainId))
            )
            self.web3Instances[chainId] = web3Instance
        return web3Instance
