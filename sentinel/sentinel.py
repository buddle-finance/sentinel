from sentinel.services.singletonFactory import SingletonFactory
from sentinel.services.configManager import ConfigManager
from sentinel.services.logManager import BuddleLogger

import logging


class Sentinel:
    def __init__(self) -> None:
        self.singletonFactory = SingletonFactory()
        self.logger = BuddleLogger.setupLogger(None, "DEBUG")
        self.singletonFactory.addService(self.logger)
        self.configManager = self.singletonFactory.getService(ConfigManager)
        # self.logger = logging.getLogger(__name__)

    def start(self) -> None:
        self.logger.info("Staring Sentinel...")


# Start Sentinel
def main():
    sentinel = Sentinel()
    sentinel.start()


main()
