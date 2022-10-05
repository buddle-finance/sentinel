from sentinel.services.singletonFactory import SingletonFactory
from sentinel.services.configManager import ConfigManager


class Sentinel:
    def __init__(self) -> None:
        self.singletonFactory = SingletonFactory()
        self.configManager = self.singletonFactory.getService(ConfigManager)

    def start(self) -> None:
        threadManager = self.singletonFactory.getService("ThreadManager")
