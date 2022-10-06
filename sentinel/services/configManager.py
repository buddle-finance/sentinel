import os
import json
from sentinel.services.logManager import BuddleLogger
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.types.enums import BuddleContract
import logging


class ConfigManager:
    """
    This is a singleton class. Use the SingletonFactory to get an instance of this class.
    """

    def __init__(self, singletonFactory: SingletonFactory) -> None:
        configPath = os.path.join(os.path.dirname(__file__), "./../../env.json")
        configDict = {}
        self.logger = singletonFactory.getService(BuddleLogger)
        self.logger.debug("ConfigManager initialized")

    def getPrivateKey(self, chainId: int) -> str:
        key = os.environ.get(f"PRIVATE_KEY_{chainId}")
        if not key:
            key = os.environ.get(f"PRIVATE_KEY_DEFAULT")

        return key

    def getRpcUrl(self, chainId: int) -> str:
        return os.environ.get(f"RPC_URL_{chainId}")

    def getContractAddress(self, buddleContract: BuddleContract, chainId: int) -> str:
        value = os.environ.get(f"CONTRACT_ADDRESS_{buddleContract.name}_{chainId}")

        # Bridge contract for each chain MUST have a valid address in config as it is unique
        if not value and buddleContract != BuddleContract.BUDDLE_BRIDGE:
            value = os.environ.get(f"CONTRACT_ADDRESS_{buddleContract.name}_DEFAULT")

        return value

    def getEnv(self, key: str) -> any:
        return os.environ.get(key)
