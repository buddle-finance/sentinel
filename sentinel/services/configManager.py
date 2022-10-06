import json
import os

from sentinel.services.logManager import BuddleLogger
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.types.configTypes import BuddleConfig
from sentinel.types.enums import BuddleContract
from sentinel.types.exceptions import RequiredConfigMissingException


class ConfigManager:
    """
    This is a singleton class. Use the SingletonFactory to get an instance of this class.
    """

    def __init__(self, singletonFactory: SingletonFactory) -> None:
        self.logger = singletonFactory.getService(BuddleLogger)
        self.config: BuddleConfig = None
        self.configDict = {}
        if not self.readConfigFile():
            raise RequiredConfigMissingException("Error reading config file")
        self.logger.debug("ConfigManager initialized")

    def readConfigFile(self) -> bool:
        configPath = os.path.join(os.path.dirname(__file__), "./../../env.json")
        try:
            with open(configPath) as configFile:
                self.configDict = json.load(configFile)
                self.config = BuddleConfig(self.configDict)
        except Exception:
            self.logger.exception("Error reading config file")
            return False

        return True

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

    def getEnv(self, key: str) -> str:
        print("Type:  ", type(os.environ.get(key)))
        return self.configDict[key]
