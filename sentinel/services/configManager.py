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
        self._config: BuddleConfig = None
        self.configDict = {}
        if not self.readConfigFile():
            raise RequiredConfigMissingException("Error reading config file")
        self.logger.debug("ConfigManager initialized")

    def readConfigFile(self) -> bool:
        configPath = os.path.join(os.path.dirname(__file__), "./../../env.json")
        try:
            with open(configPath) as configFile:
                self.configDict = json.load(configFile)
                self._config = BuddleConfig(self.configDict)
        except Exception:
            self.logger.exception("Error reading config file")
            return False

        return True

    @property
    def config(self) -> BuddleConfig:
        return self._config

    def getPrivateKey(self, chainId: int) -> str:
        key = os.environ.get(f"PRIVATE_KEY_{chainId}")
        if not key:
            key = os.environ.get(f"PRIVATE_KEY_DEFAULT")

        return key

    def getEnv(self, key: str) -> str:
        print("Type:  ", type(os.environ.get(key)))
        return self.configDict[key]
