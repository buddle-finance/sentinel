import os
from dotenv import load_dotenv
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.types.enums import BuddleContract


class ConfigManager:
    """
    This is a singleton class. Use the SingletonFactory to get an instance of this class.
    """

    def __init__(self, singletonFactory: SingletonFactory) -> None:
        dotenv_path = os.path.join(os.path.dirname(__file__), "./../../.env")
        load_dotenv(dotenv_path)

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
